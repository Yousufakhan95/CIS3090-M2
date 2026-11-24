#!/usr/bin/env python3
r"""Validate card JSON files written by the card-writing subagents.

Usage: python validate_cards.py <cards_dir or file.json>... [--source-dir DIR] [--depth full|exam|cram]

Errors (exit code 1): invalid JSON, missing/broken cloze syntax, nested clozes, HTML tags,
braces in "extra", bad tags, bad "yield", figure references to missing files/pages, and
math problems: pseudo-math written in Unicode/ASCII instead of MathJax (θ_A, √(NL/π), β̂,
x^2), single-backslash LaTeX mangled by JSON (\frac -> form feed), unbalanced braces or
\( \) delimiters, clozes straddling math delimiters, unescaped % # $ & inside math,
line breaks inside math, $...$ delimiters, TeX commands outside math.
Warnings: long cards, >3 deletions, near-duplicate cards (within and across files),
yield levels that don't belong in the chosen depth, unknown TeX commands, words or
function names typeset as italic variables inside math, hints on clozes inside math.
"""
import argparse
import collections
import difflib
import json
import os
import re
import sys

CLOZE = re.compile(r"\{\{c(\d+)::(.*?)\}\}", re.S)
HTML = re.compile(r"<\s*/?\s*(b|i|u|br|div|span|p|sub|sup|img|font|li|ul|ol)\b", re.I)
YIELDS = {"high", "medium", "low"}

# ---------------------------------------------------------------- math checks
MATH_SPAN = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
UNICODE_MATH = re.compile(
    "[\u0370-\u03ff"                                        # Greek letters
    "\u2070-\u209f\u00b2\u00b3\u00b9\u1d62-\u1d6a\u2c7c"    # super/subscript digits & letters
    "\u0300-\u036f"                                         # combining accents: β̂ t̄ Q̃
    "\u221a\u2211\u220f\u2202\u222b\u221e\u2264\u2265\u2260\u2248"  # √ ∑ ∏ ∂ ∫ ∞ ≤ ≥ ≠ ≈
    "\u00d7\u00f7\u2208\u21d2\u21d4\u2032\u2033\u00b7]"            # × ÷ ∈ ⇒ ⇔ ′ ″ ·
)
ASCII_SUB_SUP = re.compile(r"[A-Za-z0-9)\]}*]\s?[_^]\s?[A-Za-z0-9{(\\*+\-]")
SQRT_WORD = re.compile(r"\bsqrt\s*\(", re.I)
PRIME_FN = re.compile(r"(?<![A-Za-z])[A-Za-z]'+\s?\(")   # r'(d), U''(x) written as prose
# $x_i$-style math; checked outside \( \) spans, and "$4,000 ... $1,000" money is not a match
DOLLAR_MATH = re.compile(r"(?<![\\\w])\$(?![\d\s])[^$\n]*?[\\^_][^$\n]*?(?<!\s)\$(?!\d)")
TEX_CMD = re.compile(r"\\([A-Za-z]+)")
CONTROL = re.compile(r"[\x00-\x09\x0b-\x1f]")
MANGLED_NEWLINE = re.compile(r"\n(eq|u|abla|ot|eg|ewline|leq|geq)(?![A-Za-z])")
TEXT_CMD = re.compile(r"\\(text|textbf|textit|textrm|mathrm|mathbf|mathit|operatorname|mathcal|mathbb|label|tag)\s*\{[^{}]*\}")
FUNC_WORD = re.compile(r"(?<![\\A-Za-z])(ln|log|exp|max|min|lim|sin|cos|tan|det|argmax|argmin)(?![A-Za-z])")
LONG_WORD = re.compile(r"(?<![\\A-Za-z])([A-Za-z]{3,})(?![A-Za-z])")
FILE_REF = re.compile(r"\b[\w .-]+\.(pdf|pptx|docx)\b|\bch_?\d+\w*", re.I)
CTRL_HINT = {"\x0c": r"\f (\frac?)", "\x09": r"\t (\theta, \tau, \text, \times?)",
             "\x08": r"\b (\beta, \bar, \big?)", "\x0d": r"\r (\rho, \right?)"}
KNOWN_TEX = set("""
alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi
pi varpi rho varrho sigma varsigma tau upsilon phi varphi chi psi omega Gamma Delta Theta
Lambda Xi Pi Sigma Upsilon Phi Psi Omega
hat bar tilde widehat widetilde overline underline vec dot ddot check breve acute grave
overbrace underbrace overset underset stackrel
frac dfrac tfrac sqrt left right big Big bigg Bigg bigl bigr Bigl Bigr biggl biggr middle
text textbf textit textrm mathrm mathbf mathit mathcal mathbb mathsf operatorname boldsymbol
sum prod int iint oint lim limsup liminf max min sup inf arg ln log exp sin cos
tan det Pr partial nabla infty limits nolimits displaystyle textstyle scriptstyle
le leq ge geq ne neq approx equiv sim simeq cong propto lt gt ll gg subset subseteq supset
supseteq in notin ni forall exists mid nmid not
to rightarrow leftarrow Rightarrow Leftarrow leftrightarrow Leftrightarrow iff implies
uparrow downarrow Uparrow Downarrow mapsto longrightarrow Longrightarrow longleftarrow
nearrow searrow
times cdot div pm mp ast star circ bullet cup cap setminus wedge vee oplus otimes
ldots cdots dots vdots ddots quad qquad hspace kern
prime emptyset varnothing angle perp parallel neg lnot land lor top bot ell hbar Re Im
langle rangle lfloor rfloor lceil rceil lbrace rbrace vert Vert lvert rvert lVert rVert
begin end cancel color boxed phantom mathop substack checkmark square therefore because
""".split())


def _balanced(m):
    depth = 0
    for ch in re.sub(r"\\[{}\\]", "", m):
        depth += (ch == "{") - (ch == "}")
        if depth < 0:
            return False
    return depth == 0


def math_issues(field, value, has_clozes):
    """Return (errors, warnings) about math formatting in one field."""
    errs, warns = [], []
    if not value:
        return errs, warns
    for ch in sorted(set(CONTROL.findall(value))):
        errs.append(f"{field}: control character {ch!r} - a single-backslash LaTeX command was "
                    f"mangled by JSON ({CTRL_HINT.get(ch, 'escape sequence')}); double every "
                    "backslash in the JSON file")
    mn = MANGLED_NEWLINE.search(value)
    if mn:
        errs.append(f"{field}: newline followed by '{mn.group(1)}' - probably \\neq/\\nu/\\nabla/"
                    "\\not written with one backslash; double it")
    if value.count("\\(") != value.count("\\)"):
        errs.append(f"{field}: unbalanced MathJax \\( \\)")
    if value.count("\\[") != value.count("\\]"):
        errs.append(f"{field}: unbalanced MathJax \\[ \\]")
    if "{{{" in value or "}}}" in value:
        errs.append(f"{field}: three braces touch; add a space between the TeX brace and the "
                    "cloze braces, e.g. '\\frac{a}{b} }}'")

    # Clozes vs math delimiters.
    if has_clozes:
        for _, body in CLOZE.findall(value):
            ans = body.split("::")[0]
            if ans.count("\\(") != ans.count("\\)") or ans.count("\\[") != ans.count("\\]"):
                errs.append(f"{field}: cloze straddles a math delimiter ('{ans[:40]}'); a cloze "
                            "must wrap a whole \\( \\) or sit entirely inside one")
            elif not _balanced(ans):
                errs.append(f"{field}: unbalanced braces inside cloze '{ans[:40]}' - a TeX '}}' "
                            "probably touched the cloze's '}}'; add a space before '}}'")

    # Math spans: check the TeX as rendered (cloze markup replaced by the answer).
    outside = value
    for mt in MATH_SPAN.finditer(value):
        raw = mt.group(1) if mt.group(1) is not None else mt.group(2)
        outside = outside.replace(mt.group(0), " ", 1)
        if has_clozes and re.search(r"\{\{c\d+::(?:(?!\}\}).)*?::", raw):
            warns.append(f"{field}: hint on a cloze inside math ('{raw[:40]}') - the hint is "
                         "typeset as math; move it outside or cloze the whole expression")
        tex = CLOZE.sub(lambda m: m.group(2).split("::")[0], raw)
        if not tex.strip():
            errs.append(f"{field}: empty math span")
            continue
        if "\n" in tex:
            errs.append(f"{field}: line break inside math '{tex[:40]}'")
        if not _balanced(tex):
            errs.append(f"{field}: unbalanced braces in math '{tex[:50]}'")
        if re.search(r"(?<!\\)[%#$]", tex):
            errs.append(f"{field}: unescaped % # or $ inside math '{tex[:50]}' - write \\% \\# \\$")
        if re.search(r"(?<!\\)&", tex) and "\\begin" not in tex:
            errs.append(f"{field}: unescaped & inside math '{tex[:50]}' - write \\&")
        um = UNICODE_MATH.search(tex)
        if um:
            errs.append(f"{field}: Unicode symbol '{um.group(0)}' inside math '{tex[:50]}' - use "
                        "the TeX command (\\theta, \\hat{}, ^2, \\le, \\sqrt, ' ...)")
        for cmd in sorted(set(TEX_CMD.findall(tex))):
            if cmd not in KNOWN_TEX:
                warns.append(f"{field}: unknown TeX command \\{cmd} - check MathJax supports it")
        bare = TEXT_CMD.sub(" ", tex)
        fn = FUNC_WORD.search(bare)
        if fn:
            warns.append(f"{field}: '{fn.group(1)}' in math without backslash - write \\{fn.group(1)}")
        for wm in LONG_WORD.finditer(bare):
            before = bare[max(0, wm.start() - 2):wm.start()]
            if wm.group(1) in KNOWN_TEX or "_" in before or "^" in before:
                continue
            warns.append(f"{field}: word '{wm.group(1)}' in math renders as italic variables - "
                         "wrap it in \\text{}")
            break

    # Outside math: no pseudo-math, no stray TeX.
    plain = CLOZE.sub(lambda m: " " + m.group(2) + " ", outside) if has_clozes else outside
    plain = FILE_REF.sub(" ", plain)
    if DOLLAR_MATH.search(plain):
        errs.append(f"{field}: $...$ math - Anki doesn't render it; use \\( ... \\)")
    u = UNICODE_MATH.search(plain)
    if u:
        ctx = plain[max(0, u.start() - 15):u.end() + 15].strip()
        errs.append(f"{field}: pseudo-math '{u.group(0)}' outside MathJax (...{ctx}...) - typeset "
                    "it as \\( ... \\) with TeX commands")
    a = ASCII_SUB_SUP.search(plain) or SQRT_WORD.search(plain) or PRIME_FN.search(plain)
    if a:
        ctx = plain[max(0, a.start() - 15):a.end() + 15].strip()
        errs.append(f"{field}: ASCII math '{a.group(0)}' outside MathJax (...{ctx}...) - typeset "
                    "it as \\( ... \\)")
    c = TEX_CMD.search(plain)
    if c:
        errs.append(f"{field}: TeX command \\{c.group(1)} outside \\( \\) - wrap the math in delimiters")
    return errs, warns
ALLOWED = {"full": YIELDS, "exam": {"high", "medium"}, "cram": {"high"}}


def answer_text(t):
    return CLOZE.sub(lambda m: m.group(2).split("::")[0], t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--source-dir", help="folder with the original lecture files (checks figure refs)")
    ap.add_argument("--depth", choices=sorted(ALLOWED), default=None)
    args = ap.parse_args()

    files = []
    for p in args.paths:
        if os.path.isdir(p):
            files += sorted(os.path.join(p, f) for f in os.listdir(p) if f.endswith(".json"))
        else:
            files.append(p)

    page_counts = {}
    errors, warnings, everything = [], [], []
    for path in files:
        name = os.path.basename(path)
        try:
            cards = json.load(open(path, encoding="utf-8"))
            assert isinstance(cards, list)
        except Exception as e:
            hint = (" - LaTeX backslashes must be doubled inside JSON strings"
                    if "escape" in str(e).lower() else "")
            errors.append(f"{name}: not a JSON array of cards ({e}){hint}")
            continue
        ycount, figs = collections.Counter(), 0
        for i, c in enumerate(cards):
            key = f"{name}#{i}"
            t = c.get("text", "") if isinstance(c, dict) else ""
            clozes = CLOZE.findall(t)
            if not clozes:
                errors.append(f"{key}: no {{{{cN::...}}}} cloze")
            if t.count("{{") != len(clozes) or t.count("}}") != len(clozes):
                errors.append(f"{key}: stray '{{{{' or '}}}}' (put a space between closing braces in math)")
            for _, body in clozes:
                if "{{" in body:
                    errors.append(f"{key}: nested cloze")
                if not body.split("::")[0].strip():
                    errors.append(f"{key}: empty cloze")
            if len({n for n, _ in clozes}) > 3:
                warnings.append(f"{key}: more than 3 cloze numbers")
            extra = c.get("extra", "") or ""
            for field, value in (("text", t), ("extra", extra)):
                e_, w_ = math_issues(field, value, field == "text")
                errors += [f"{key}: {m}" for m in e_]
                warnings += [f"{key}: {m}" for m in w_]
            if HTML.search(t + extra):
                errors.append(f"{key}: HTML tag (use plain text)")
            if "{{" in extra or "}}" in extra:
                errors.append(f"{key}: '{{{{' or '}}}}' in extra")
            tags = c.get("tags") or []
            if not tags or any((not isinstance(x, str)) or " " in x for x in tags):
                errors.append(f"{key}: tags must be a non-empty list of strings without spaces")
            y = c.get("yield")
            if y not in YIELDS:
                errors.append(f"{key}: yield must be high/medium/low, got {y!r}")
            else:
                ycount[y] += 1
                if args.depth and y not in ALLOWED[args.depth]:
                    warnings.append(f"{key}: yield={y} doesn't belong in depth={args.depth}")
            fig = c.get("figure")
            if fig:
                figs += 1
                fname, page = fig.get("file") or fig.get("pdf"), fig.get("page")
                if args.source_dir and fname:
                    fpath = os.path.join(args.source_dir, fname)
                    if not os.path.exists(fpath):
                        errors.append(f"{key}: figure file not found: {fname}")
                    elif fname.lower().endswith(".pdf"):
                        if fpath not in page_counts:
                            import pymupdf
                            with pymupdf.open(fpath) as d:
                                page_counts[fpath] = d.page_count
                        if not isinstance(page, int) or not 1 <= page <= page_counts[fpath]:
                            errors.append(f"{key}: figure page {page!r} out of range")
            words = len(answer_text(t).split())
            if words > 45:
                warnings.append(f"{key}: long card ({words} words)")
            everything.append((key, re.sub(r"\W+", " ", answer_text(t)).lower().strip()))
        print(f"{name}: {len(cards)} cards, yield={dict(ycount)}, figures={figs}")

    for a in range(len(everything)):
        ka, ta = everything[a]
        for b in range(a + 1, len(everything)):
            kb, tb = everything[b]
            m = difflib.SequenceMatcher(None, ta, tb)
            if m.real_quick_ratio() > 0.85 and m.quick_ratio() > 0.85 and m.ratio() > 0.85:
                warnings.append(f"near-duplicate: {ka} ~ {kb}: {ta[:70]!r}")

    print(f"\nTOTAL {len(everything)} cards in {len(files)} files")
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
