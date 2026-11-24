# CC Card Gen

**Claude Code card generation:** turn a folder of lecture slides or notes into a
ready-to-import [Anki](https://apps.ankiweb.net/) cloze deck, with an **exam-focused mode**
that predicts what your exam will actually test.

Point it at a folder of PDFs (or PPTX/DOCX) and it will:

1. extract every lecture and work out which pages are figures, tables or equations;
2. read your syllabus to find the exam format, the scope and the assessment materials;
3. split the lectures across **parallel Claude Code subagents**, which read every slide
   (viewing figure pages as images) and write cloze cards;
4. validate the cards (cloze syntax, MathJax math formatting, duplicates, figure
   references, yield levels);
5. package everything into one `.apkg` with a subdeck per lecture and slide images on
   the back of the cards that need them.

```
/anki-deck "C:\Users\me\Desktop\BIOL2100" depth=exam
```

## Depth setting

| depth | What you get |
|---|---|
| `full` (default) | Every substantive fact. Each card is tagged `yield::high`, `yield::medium` or `yield::low`, so you can study high-yield cards first. |
| `exam` | Only what the exam is likely to test. The skill writes a blueprint of predicted exam questions and their full-mark answers, then makes cards covering those answers. It skips history, background statistics, anecdotes and other backdrop. |
| `cram` | High-yield cards only, for the night before the exam. |

Exam mode ranks its evidence for what will be tested, strongest first:

1. instructor statements and the syllabus
2. past exams, quizzes and assignments
3. worked examples and practice slides
4. summary slides
5. emphasis (how much time a topic gets)
6. what exams in the discipline normally ask

It also shapes cards to the exam format: "explain why" cards for short answer, fine
distinctions for multiple choice, formula and worked-example cards for problem sets. In
exam and cram mode, the predicted questions are also saved as a Markdown study sheet next
to the deck.

"History" is relative to the course. A historical case study in an economics course
gets cards on its economic lesson, not its timeline; in a history course the dates are
the content, and they stay.

## Requirements

- [Claude Code](https://docs.claude.com/en/docs/claude-code)
- Python 3.9+ with `pymupdf` and `genanki` (the skill installs these on first run, or
  use the install scripts below)
- Anki desktop, to import the `.apkg`
- Optional: `python-pptx` / `python-docx` for PowerPoint or Word lecture files

## Install

### Option A: Claude Code plugin

In Claude Code:

```
/plugin marketplace add AshtonLong/CC-Card-Gen
/plugin install cc-card-gen@cc-card-gen
```

Plugin skills are namespaced, so invoke it as `/cc-card-gen:anki-deck`. Claude will also
pick it up automatically when you ask for flashcards or an Anki deck from your lectures.

### Option B: install script (personal skill)

```bash
git clone https://github.com/AshtonLong/CC-Card-Gen.git
cd CC-Card-Gen
./install.sh                                         # macOS / Linux / Git Bash
powershell -ExecutionPolicy Bypass -File install.ps1  # Windows PowerShell
```

This copies `skills/anki-deck` to `~/.claude/skills/anki-deck` and installs the Python
dependencies. Invoke it as `/anki-deck`.

### Option C: manual

Copy `skills/anki-deck/` into `~/.claude/skills/` (personal) or `<project>/.claude/skills/`
(one project), then:

```bash
python -m pip install pymupdf chevron frozendict cached-property
python -m pip install --no-deps genanki   # see Troubleshooting for why --no-deps
```

## Usage

```
/anki-deck <folder> [depth=full|exam|cram] [scope=...] [exam="Midterm 2"] [out=<path>]
```

Plain language works too:

- `make me an anki deck from ~/school/chem1040, exam mode`
- `/anki-deck ./lectures depth=cram scope=ch5-10`
- `flashcards for my midterm from the slides in D:\Psych\Lectures, only weeks 6-12`

If the syllabus doesn't make the exam's scope clear, Claude asks you once with concrete
options. The deck is written to the lecture folder unless you pass `out=`.

### What you get

- `<Course>_<depth>.apkg` with one subdeck per lecture. Double-click it to import, or use
  File → Import in Anki.
- **The cards**: each card uses the "Lecture Cloze (anki-deck skill)" note type, with these fields:
  - **Text**: the cloze sentence. Formulas and symbols are typeset with MathJax
    (`\( ... \)`), which Anki renders natively, and clozes can sit inside a formula.
  - **Back Extra**: a short explanation or intuition
  - **Figure**: the slide image, when a graph or table is the thing to learn
  - **Source**: the file and page the card came from
- **Tags**: a chapter tag, a subtopic tag and `yield::<level>`. To study the most
  testable cards first, make a filtered deck with `tag:yield::high`.
- **Predicted questions (exam/cram)**: `<course>_predicted_questions.md` lists the
  predicted exam questions, with full-mark answer outlines.
- **Rebuilding**: note IDs are stable, so re-importing a rebuilt deck updates the
  existing notes and keeps your review history. Before rewriting the text of cards you
  have already imported, run `build_deck.py <manifest> --pin-guids` so the edited cards
  keep their IDs.

A full-depth deck for a 10-lecture course is often 600–800 notes (1,000+ cards). Anki
introduces 20 new cards a day by default, so raise that limit if your exam is soon.

### Cost

Each card-writing subagent typically uses 150–250k tokens. A 10-lecture course runs
6–8 subagents in parallel, about 1–1.5M tokens and 10–15 minutes in total. Exam mode
saves study time, not generation cost: it reads everything, then writes fewer cards.

## How it works

```
skills/anki-deck/
├── SKILL.md                   # the orchestration workflow Claude follows
├── references/
│   ├── subagent_brief.md      # prompt template for each card-writing subagent
│   ├── card_writing.md        # card JSON format, cloze rules, MathJax math, figures
│   └── exam_focus.md          # yield rubric, evidence ladder, predicted-question blueprint
└── scripts/
    ├── extract_text.py        # PDF/PPTX/DOCX/TXT -> text with page markers + inventory
    ├── render_pages.py        # PDF pages -> PNG for viewing figures and equations
    ├── validate_cards.py      # checks cloze syntax, math, tags, yield, figures, duplicates
    └── build_deck.py          # manifest -> .apkg (genanki), with figure images
```

The main Claude Code session acts as the orchestrator. It reads the syllabus, plans
batches of 1–2 lectures each, and spawns one subagent per batch. Each subagent reads
`card_writing.md` and `exam_focus.md`, writes its cards as JSON and validates them. The
orchestrator then cross-checks for duplicates, spot-checks quality, and builds the deck.

### Using the scripts on their own

```bash
S=skills/anki-deck/scripts
python $S/extract_text.py ./lectures ./work/text
python $S/render_pages.py ./lectures/week3.pdf ./work/img --sparse
python $S/validate_cards.py ./work/cards --source-dir ./lectures --depth exam
python $S/build_deck.py ./work/manifest.json
```

The card JSON format is one array per lecture:

```json
[
  {
    "text": "If the omitted variable is positively correlated with both X and Y, the OLS slope is biased {{c1::upward}}.",
    "extra": "The coefficient picks up the omitted variable's effect on Y.",
    "tags": ["ch02_regression", "omitted_variable_bias"],
    "source": "week2.pdf p.31",
    "yield": "high",
    "figure": {"file": "week2.pdf", "page": 31}
  }
]
```

The manifest is one JSON object:

```json
{
  "deck_name": "BIOL 2100 Cell Biology (Midterm 2 - exam focus)",
  "out": "./lectures/BIOL2100_Midterm2_exam.apkg",
  "source_dir": "./lectures",
  "include_yield": ["high", "medium"],
  "subdecks": [
    {"title": "01 Membranes", "cards": "./work/cards/ch01.json"},
    {"title": "02 Signalling", "cards": "./work/cards/ch02.json"}
  ]
}
```

## Troubleshooting

- **`pip install genanki` fails building `pyyaml`.** Install genanki with `--no-deps`
  plus `chevron frozendict cached-property`. genanki only needs yaml for string templates,
  which this project doesn't use, and `build_deck.py` stubs it out.
- **Claude can't open PDF pages with its Read tool.** That reader needs poppler. The
  skill uses `render_pages.py` (PyMuPDF) instead, so nothing else needs installing.
- **Scanned PDFs with no text layer.** Every page shows up as sparse, and the subagents
  read the rendered page images instead. This works, but it is slower and uses more tokens.
- **PowerPoint figures.** `.pptx` text and speaker notes are extracted, but slides can't
  be rendered as images. Export to PDF first if the figures matter.

## Privacy and copyright

Lecture materials are usually copyrighted by your instructor or institution. Use the
generated decks for your own study, and don't commit lecture files or decks to public
repositories. The `.gitignore` excludes `*.pdf`, `*.pptx`, `*.docx` and `*.apkg` for that
reason.

## License

[MIT](LICENSE)
