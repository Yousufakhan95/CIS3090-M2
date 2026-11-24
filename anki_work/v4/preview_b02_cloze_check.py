"""Read-only HTML preview of b02 cards to check cloze blue-highlight vs MathJax."""
import html
import json
import re
from pathlib import Path

CARDS = Path(__file__).with_name("cards") / "b02.json"
OUT = Path(__file__).with_name("preview_b02_cloze_check.html")
CLOZE = re.compile(r"\{\{c(\d+)::((?:(?!\}\}).)*?)\}\}")


def cloze_inside_math(text: str) -> list[int]:
    hits = []
    for m in CLOZE.finditer(text):
        before = text[: m.start()]
        opens = before.count(r"\(") - before.count(r"\)")
        if opens > 0:
            hits.append(int(m.group(1)))
    return sorted(set(hits))


def cloze_to_html(text: str, active_n: int, reveal: bool) -> str:
    parts: list[tuple[str, str]] = []
    last = 0
    for m in CLOZE.finditer(text):
        parts.append(("t", text[last : m.start()]))
        n, body = m.group(1), m.group(2)
        ans = body.split("::")[0]
        if n == str(active_n):
            parts.append(("c", ans if reveal else "[...]"))
        else:
            parts.append(("t", ans))
        last = m.end()
    parts.append(("t", text[last:]))
    out = []
    for kind, s in parts:
        if kind == "c":
            out.append(f'<span class="cloze">{html.escape(s)}</span>')
        else:
            out.append(html.escape(s))
    return "".join(out)


def main() -> None:
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    rows = []
    affected = []
    for i, c in enumerate(cards):
        t = c["text"]
        inside = cloze_inside_math(t)
        nums = sorted({int(n) for n in re.findall(r"\{\{c(\d+)::", t)})
        active = nums[0]
        front = cloze_to_html(t, active, reveal=False)
        back = cloze_to_html(t, active, reveal=True)
        if inside:
            affected.append((i, inside, t))
            diag = (
                f'<div class="diag">Card {i}: cloze(s) c{inside} sit <b>inside</b> '
                r"MathJax \(...\). Anki still blanks them, but MathJax re-typesets "
                "the span so the blue .cloze color often disappears.</div>"
            )
        else:
            diag = (
                f'<div class="diag ok">Card {i}: cloze(s) are outside math — '
                "blue highlight should show normally.</div>"
            )
        tags = ", ".join(c.get("tags", []))
        extra = html.escape(c.get("extra", ""))
        rows.append(
            f"""
<div class="cardwrap">
  <div class="hdr">b02 #{i} · tags: {tags} · showing cloze c{active}</div>
  {diag}
  <div class="card side"><b>Front:</b><br>{front}</div>
  <hr>
  <div class="card side"><b>Back:</b><br>{back}
    <div class="extra">{extra}</div>
  </div>
</div>"""
        )

    doc = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>b02 preview (copy) — cloze highlight check</title>
<style>
.card {{ font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif; font-size: 21px;
        line-height: 1.45; text-align: left; color: #1d1d1f; background: #fbfbfa; padding: 8px 14px; }}
.cloze {{ font-weight: 700; color: #1a5fb4; }}
.extra {{ margin-top: 16px; padding: 10px 12px; border-left: 4px solid #e5a50a; background: #fdf6e3;
         font-size: 17px; color: #3a3a3a; }}
.diag {{ margin: 8px 0 16px; padding: 8px 10px; background: #fff3cd; border: 1px solid #e0c36a; font-size: 14px; }}
.ok {{ background: #e8f5e9; border-color: #81c784; }}
.cardwrap {{ border: 1px solid #ddd; border-radius: 8px; margin: 18px 0; overflow: hidden; }}
.hdr {{ background: #eee; padding: 6px 12px; font-size: 13px; color: #444; }}
.side {{ padding: 4px 0; }}
h1 {{ font-size: 22px; }}
.note {{ max-width: 820px; margin: 0 auto; padding: 20px; }}
</style>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] }}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
</head><body><div class="note">
<h1>Preview copy: 02 Speedup efficiency Amdahl</h1>
<p>This is a <b>read-only HTML copy</b> of the card JSON. The Anki deck / .apkg was not edited.</p>
<p>Blue text = <code>.cloze</code> highlight (<code>#1a5fb4</code>). Yellow flags =
blank lives inside MathJax, which is why the blue often fails in Anki too.</p>
{''.join(rows)}
</div></body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT.resolve()}")
    print(f"\nAffected cards: {len(affected)} / {len(cards)}")
    for i, inside, t in affected:
        print(f"  #{i}: c{inside}")
        print(f"      {t[:110]}...")


if __name__ == "__main__":
    main()
