#!/usr/bin/env python3
r"""Package validated card JSON files into an Anki .apkg (cloze note type, one subdeck per lecture).

Usage: python build_deck.py <manifest.json> [--pin-guids]

manifest.json:
{
  "deck_name": "BIOL 2100 Cell Biology (Midterm 2 - exam focus)",
  "out": "/path/to/lectures/BIOL2100_Midterm2_exam.apkg",
  "source_dir": "/path/to/lectures",                  # where figure PDFs live
  "include_yield": ["high", "medium"],                # optional filter; default: all
  "subdecks": [
    {"title": "01 Intro to Cities", "cards": "C:/.../cards/ch01.json"},
    ...
  ]
}

Each card: {"text", "extra"?, "tags", "source"?, "yield", "figure"?: {"file"|"pdf": name, "page": N}, "guid"?}.
Text and extra may contain MathJax (\( ... \) and \[ ... \]); Anki typesets it natively.
Figures are rendered from the source PDF page to JPEG and shown on the back of the card.
Note IDs come from a card's "guid" field if present, else from deck_name + card text, so
re-importing a rebuilt deck updates existing notes (keeping review history) instead of
duplicating them.

--pin-guids: build nothing; instead write each card's current note ID into a "guid" field
in its JSON file. Run this before rewriting the text of cards the student has already
imported, so the rewritten cards still update the same notes.
The script re-opens the written package and prints note/card counts as a check.
"""
import hashlib
import html
import json
import os
import sqlite3
import sys
import tempfile
import types
import zipfile

try:
    import yaml  # noqa: F401
except ImportError:  # genanki imports yaml but only uses it for string templates; we pass lists
    sys.modules["yaml"] = types.ModuleType("yaml")
import genanki  # noqa: E402

MODEL_ID = 1872203391  # stable so all decks made by this skill share one note type
CSS = """
.card { font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif; font-size: 21px;
        line-height: 1.45; text-align: left; color: #1d1d1f; background: #fbfbfa; padding: 8px 14px; }
.cloze { font-weight: 700; color: #1a5fb4; }
.extra { margin-top: 16px; padding: 10px 12px; border-left: 4px solid #e5a50a; background: #fdf6e3;
         font-size: 17px; color: #3a3a3a; }
.fig img { max-width: 100%; margin-top: 12px; border: 1px solid #ccc; border-radius: 4px; }
.source { margin-top: 12px; font-size: 13px; color: #888; }
.nightMode.card, .night_mode .card { color: #e8e8e8; background: #1e1e1e; }
.nightMode .cloze, .night_mode .cloze { color: #8ab4f8; }
.nightMode .extra, .night_mode .extra { background: #2b2618; color: #ddd; border-left-color: #c49000; }
.nightMode .fig img, .night_mode .fig img { border-color: #444; }
"""
MODEL = genanki.Model(
    MODEL_ID, "Lecture Cloze (anki-deck skill)",
    fields=[{"name": "Text"}, {"name": "Back Extra"}, {"name": "Figure"}, {"name": "Source"}],
    templates=[{
        "name": "Cloze",
        "qfmt": "{{cloze:Text}}",
        "afmt": "{{cloze:Text}}"
                "{{#Back Extra}}<div class=extra>{{Back Extra}}</div>{{/Back Extra}}"
                "{{#Figure}}<div class=fig>{{Figure}}</div>{{/Figure}}"
                "<div class=source>{{Source}}</div>",
    }],
    css=CSS, model_type=genanki.Model.CLOZE,
)


def stable_id(*parts):
    return int(hashlib.sha1("|".join(parts).encode()).hexdigest()[:9], 16) + (1 << 30)


def esc(s):
    return html.escape(s or "", quote=False).replace("\n", "<br>")


def pin_guids(man):
    for sub in man["subdecks"]:
        cards = json.load(open(sub["cards"], encoding="utf-8"))
        added = 0
        for c in cards:
            if not c.get("guid"):
                c["guid"] = genanki.guid_for(man["deck_name"], c["text"])
                added += 1
        with open(sub["cards"], "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=1)
        print(f"{sub['title']}: pinned {added} guids ({len(cards)} cards)")


def main():
    args = [a for a in sys.argv[1:] if a != "--pin-guids"]
    if len(args) != 1:
        sys.exit(__doc__)
    man = json.load(open(args[0], encoding="utf-8"))
    if "--pin-guids" in sys.argv:
        return pin_guids(man)
    deck_name, out, src = man["deck_name"], man["out"], man.get("source_dir", "")
    keep = set(man.get("include_yield") or ["high", "medium", "low"])
    media_dir = os.path.join(os.path.dirname(os.path.abspath(args[0])), "media")
    os.makedirs(media_dir, exist_ok=True)
    slug = hashlib.sha1(deck_name.encode()).hexdigest()[:6]

    docs, media, decks, total_cards, dropped = {}, [], [], 0, 0
    for sub in man["subdecks"]:
        deck = genanki.Deck(stable_id(deck_name, sub["title"]), f"{deck_name}::{sub['title']}")
        n_notes = 0
        for c in json.load(open(sub["cards"], encoding="utf-8")):
            y = c.get("yield", "medium")
            if y not in keep:
                dropped += 1
                continue
            fig_html, fig = "", c.get("figure")
            fname = fig and (fig.get("file") or fig.get("pdf"))
            if fname and fname.lower().endswith(".pdf"):
                page = int(fig["page"])
                img = f"ankideck_{slug}_" + os.path.splitext(fname)[0].replace(" ", "_") + f"_p{page}.jpg"
                path = os.path.join(media_dir, img)
                if not os.path.exists(path):
                    import pymupdf
                    if fname not in docs:
                        docs[fname] = pymupdf.open(os.path.join(src, fname))
                    pg = docs[fname][page - 1]
                    zoom = min(2.0, 1100 / pg.rect.width)
                    pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).save(path, jpg_quality=82)
                if path not in media:
                    media.append(path)
                fig_html = f'<img src="{img}">'
            elif fname:
                print(f"note: figure from non-PDF file {fname} skipped")
            tags = [t.replace(" ", "_") for t in c.get("tags", [])] + [f"yield::{y}"]
            note = genanki.Note(
                model=MODEL,
                fields=[esc(c["text"]), esc(c.get("extra")), fig_html, esc(c.get("source"))],
                tags=tags,
                guid=c.get("guid") or genanki.guid_for(deck_name, c["text"]),
            )
            deck.add_note(note)
            n_notes += 1
            total_cards += len(note.cards)
        decks.append(deck)
        print(f"{sub['title']}: {n_notes} notes")

    pkg = genanki.Package(decks)
    pkg.media_files = media
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    pkg.write_to_file(out)

    # Re-open the package to confirm what Anki will import.
    with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(out) as z:
        z.extract("collection.anki2", tmp)
        db = sqlite3.connect(os.path.join(tmp, "collection.anki2"))
        n_notes = db.execute("select count(*) from notes").fetchone()[0]
        n_cards = db.execute("select count(*) from cards").fetchone()[0]
        db.close()
        n_media = len(json.loads(z.read("media")))
    print(f"\nWrote {out} ({os.path.getsize(out) / 1e6:.1f} MB): {n_notes} notes -> {n_cards} cards, "
          f"{n_media} images" + (f"; {dropped} cards excluded by include_yield" if dropped else ""))


if __name__ == "__main__":
    main()
