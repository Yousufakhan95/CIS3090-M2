#!/usr/bin/env python3
"""Extract text from course materials, one .txt per file with page markers.

Usage: python extract_text.py <input_dir> <out_dir>

Writes <out_dir>/<stem>.txt (pages separated by "===== PAGE N =====") and
<out_dir>/inventory.json, and prints one line per file with: page count, characters,
sparse pages (little extractable text -> probably figures, tables, equations or
handwriting worth viewing as images), and a role hint (syllabus / assessment /
assignment / lecture). The role hint is a guess from the filename and first page;
confirm it by reading.

Supports .pdf (PyMuPDF), .pptx (python-pptx), .docx (python-docx), .txt / .md.
"""
import json
import os
import re
import sys

SPARSE_CHARS = 40
SYLLABUS = r"syllabus|course outline|course information|course assessment|learning outcomes|grading scheme"
NAME_ROLES = [
    ("assessment", r"midterm|final|quiz|exam|review|practice|sample"),
    ("assignment", r"assign|problem.?set|pset|homework|hw\d|exercise|tutorial"),
]
TITLE_ROLES = [
    ("assessment", r"\b(midterm|final exam|quiz|practice exam|sample exam|exam review|review sheet)\b"),
    ("assignment", r"\b(assignment|problem set|homework)\s*#?\d*\s*$"),
]


def pdf_pages(path):
    import pymupdf
    with pymupdf.open(path) as doc:
        return [page.get_text() for page in doc]


def _shape_text(shape):
    out = []
    if getattr(shape, "shape_type", None) == 6:  # MSO_SHAPE_TYPE.GROUP
        for sub in shape.shapes:
            out += _shape_text(sub)
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
        out.append(shape.text_frame.text)
    if getattr(shape, "has_table", False) and shape.has_table:
        out += [" | ".join(cell.text for cell in row.cells) for row in shape.table.rows]
    return out


def pptx_pages(path):
    from pptx import Presentation
    pages = []
    for slide in Presentation(path).slides:
        parts = []
        for shape in slide.shapes:
            parts += _shape_text(shape)
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
            if notes:
                parts.append("[Speaker notes] " + notes)
        pages.append("\n".join(parts))
    return pages


def docx_pages(path):
    import docx
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for table in d.tables:
        parts += [" | ".join(c.text for c in row.cells) for row in table.rows]
    return ["\n".join(parts)]


def text_pages(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return [fh.read()]


READERS = {".pdf": pdf_pages, ".pptx": pptx_pages, ".docx": docx_pages, ".txt": text_pages, ".md": text_pages}


def role_hint(filename, pages):
    name = os.path.splitext(filename)[0].lower()
    for role, pat in NAME_ROLES:
        if re.search(pat, name):
            return role
    head = "\n".join(pages[:4])[:5000].lower()
    if re.search(SYLLABUS, head):
        return "syllabus"
    title = next((p.strip() for p in pages if p.strip()), "")[:300].lower()
    for role, pat in TITLE_ROLES:
        if re.search(pat, title, re.M):
            return role
    return "lecture"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    inventory, used_stems, skipped = [], set(), []
    for fname in sorted(os.listdir(src)):
        path = os.path.join(src, fname)
        ext = os.path.splitext(fname)[1].lower()
        if not os.path.isfile(path):
            continue
        if ext not in READERS:
            skipped.append(fname)
            continue
        try:
            pages = READERS[ext](path)
        except ImportError as e:
            print(f"!! {fname}: missing library ({e}). Install it and rerun.")
            continue
        except Exception as e:  # corrupt or password-protected file
            print(f"!! {fname}: could not read ({e})")
            continue
        stem = re.sub(r"[^A-Za-z0-9._-]+", "_", os.path.splitext(fname)[0]).strip("_") or "file"
        base, n = stem, 2
        while stem in used_stems:
            stem, n = f"{base}_{n}", n + 1
        used_stems.add(stem)
        txt_path = os.path.join(out, stem + ".txt")
        with open(txt_path, "w", encoding="utf-8") as fh:
            for i, t in enumerate(pages, 1):
                fh.write(f"\n===== PAGE {i} =====\n{t}")
        sparse = [i for i, t in enumerate(pages, 1) if len(t.strip()) < SPARSE_CHARS]
        chars = sum(len(t.strip()) for t in pages)
        entry = {"file": fname, "path": os.path.abspath(path), "txt": os.path.abspath(txt_path),
                 "type": ext[1:], "pages": len(pages), "chars": chars,
                 "sparse_pages": sparse, "role_hint": role_hint(fname, pages)}
        inventory.append(entry)
        print(f"{fname}: {entry['pages']} pages, {chars} chars, role={entry['role_hint']}, "
              f"sparse pages={sparse if len(sparse) <= 25 else str(len(sparse)) + ' pages'}")
    with open(os.path.join(out, "inventory.json"), "w", encoding="utf-8") as fh:
        json.dump(inventory, fh, indent=1)
    if skipped:
        print("Skipped (unsupported type):", ", ".join(skipped))
    print(f"\n{len(inventory)} files, {sum(e['chars'] for e in inventory)} chars total "
          f"-> {os.path.join(out, 'inventory.json')}")


if __name__ == "__main__":
    main()
