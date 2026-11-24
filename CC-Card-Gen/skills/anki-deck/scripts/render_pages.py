#!/usr/bin/env python3
"""Render PDF pages to PNG so figures, tables, equations and handwritten notes can be viewed.

Usage: python render_pages.py <file.pdf> <out_dir> [--pages 3,5-9] [--sparse] [--zoom 1.6]

  --pages   comma-separated page numbers / ranges (1-based). Default: all pages.
  --sparse  only pages with little extractable text (usually the image-only slides).
  --zoom    render scale (1.6 is readable for slides; raise it to zoom into small print).

Prints the PNG paths; open them with the Read tool to look at them. The Read tool's own
PDF reader needs poppler, which is often not installed, so use this script instead.
"""
import argparse
import os


def parse_pages(spec, n):
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a), int(b) + 1))
        else:
            pages.add(int(part))
    return sorted(p for p in pages if 1 <= p <= n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out_dir")
    ap.add_argument("--pages")
    ap.add_argument("--sparse", action="store_true")
    ap.add_argument("--zoom", type=float, default=1.6)
    args = ap.parse_args()

    import pymupdf
    os.makedirs(args.out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.pdf))[0].replace(" ", "_")
    with pymupdf.open(args.pdf) as doc:
        pages = parse_pages(args.pages, doc.page_count) if args.pages else list(range(1, doc.page_count + 1))
        if args.sparse:
            pages = [p for p in pages if len(doc[p - 1].get_text().strip()) < 40]
        for p in pages:
            path = os.path.join(args.out_dir, f"{stem}_p{p}.png")
            doc[p - 1].get_pixmap(matrix=pymupdf.Matrix(args.zoom, args.zoom)).save(path)
            print(path)
    if not pages:
        print("(no pages matched)")


if __name__ == "__main__":
    main()
