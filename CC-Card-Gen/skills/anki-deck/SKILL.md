---
name: anki-deck
description: Turn a folder of lecture slides or notes (PDF, PPTX, DOCX) into a ready-to-import Anki cloze deck (.apkg), using parallel subagents that read every slide, including figures. Has a depth setting. depth=full covers everything, with each card tagged by how likely it is to be tested. depth=exam predicts what the exam will actually test and makes cards only on that, skipping history, background and trivia. depth=cram keeps only the highest-yield cards. Use this whenever the user wants Anki cards, flashcards, cloze cards, a study deck, spaced-repetition material, or exam or midterm prep built from course materials, lectures, slides or notes, even if they don't say "Anki" or "cloze".
---

# Anki deck from lecture materials

This skill turns a folder of course materials into an Anki cloze deck, packaged as a
`.apkg` file with one subdeck per lecture. Subagents read the lectures in parallel and
write cards as JSON. The bundled scripts extract the text, render slide images, validate
the cards and package them.

## Arguments

`/anki-deck <folder> [depth=full|exam|cram] [scope=...] [exam="Midterm 2"] [out=<path>]`

The arguments may also arrive as plain language, e.g. "exam mode, just chapters 5–10".
If no folder is given, ask for one.

| depth | What the deck contains |
|---|---|
| `full` (default) | Every substantive fact. Each card is tagged `yield::high`, `yield::medium` or `yield::low`, so the student can study high-yield cards first with an Anki filter such as `tag:yield::high`. |
| `exam` | Only what the exam is likely to test (high and medium yield). It is built from a blueprint of predicted exam questions, and skips backdrop such as history, background statistics, anecdotes and rankings. |
| `cram` | High-yield cards only, for the last day or two before the exam. |

Treat "exam mode", "to the test", "focused" and "high-yield" as `exam`, and "everything"
or "comprehensive" as `full`. If the user gives no depth, use `full` without asking, and
mention that `exam` exists.

## Workflow

Let SKILL_DIR be the directory containing this file. WORK is a fresh folder in your
session scratchpad (or the system temp dir), for example `anki-<course>`. Use `python`,
or `python3` where that is the command available.

### 1. Install dependencies (only what is missing)

```
python -m pip install pymupdf chevron frozendict cached-property
python -m pip install --no-deps genanki
python -m pip install python-pptx python-docx     # only if the folder has .pptx/.docx
```

Install genanki with `--no-deps` because its `pyyaml` dependency often fails to build on
new Python versions. `build_deck.py` stubs out yaml, which genanki doesn't actually need here.

### 2. Extract and take inventory

```
python SKILL_DIR/scripts/extract_text.py "<folder>" WORK/text
```

This prints each file's page count, character count, sparse pages (probably figures or
equations) and a role hint (syllabus, assessment, assignment or lecture). The hints are
guesses, so confirm them by reading.

### 3. Pin down the exam (read the syllabus yourself)

Read the syllabus or course outline, and skim anything that looks like an assignment,
quiz, past exam or review sheet. Work out:

- **Which exam is next.** Compare today's date with the schedule. If there is no final,
  "my exam" means the next midterm.
- **Its format:** multiple choice, short answer, calculations or essay; which aids are
  allowed; and what it draws on (e.g. "assignments and lecture notes").
- **Its scope:** which lectures it covers.
- **Exam-signal documents:** assignments, quizzes, past or practice exams, review sheets.
  These are the strongest evidence of what gets tested, so every subagent gets their paths.

If the scope is still unclear after reading, ask the user one question with concrete
options (e.g. "Ch 5–10 / Ch 6–10 / all of Ch 1–10"). A deck on the wrong chapters wastes
study time, so don't guess scope silently. Leave the syllabus and admin files out of the
deck itself.

Write a 2–5 sentence EXAM CONTEXT summary. It goes into every subagent brief.

### 4. Plan the batches

Group the in-scope lectures into batches of about 30–50k extracted characters (1–2
lectures each). Split a lecture longer than about 60k characters by page range. Use 8
subagents at most. Give each lecture a key and a first tag, such as `ch03` and
`ch03_agglomeration`, plus a subdeck title such as `03 Agglomeration & Productivity`.

### 5. Spawn the card writers in parallel

Send one message containing one Agent call (general-purpose) per batch, all in the
foreground, so they run at the same time. Build each prompt from
`references/subagent_brief.md`. Each agent reads `references/card_writing.md` and
`references/exam_focus.md`, and writes `WORK/cards/<key>.json`. For exam and cram, each
also writes `WORK/blueprints/<key>.md`.

Subagents are worth it because each lecture needs a careful full read plus figure pages
viewed as images. Running them in parallel keeps the job fast and keeps hundreds of slide
images out of your own context.

### 6. Validate and check quality

```
python SKILL_DIR/scripts/validate_cards.py WORK/cards --source-dir "<folder>" --depth <depth>
```

Fix errors yourself; they are usually one-line JSON edits, so don't respawn an agent for
them. For near-duplicate pairs across files, delete the weaker copy. Then read about 4
random cards per file and ask:

- Does each card test one meaningful fact, and is the answer unambiguous?
- At exam or cram depth, would this card plausibly earn marks?
- Is every formula and symbol typeset in MathJax (`\( ... \)`), with no Unicode or ASCII
  pseudo-math such as `θ_A`, `√(NL/π)` or `β̂`? The validator catches most of these as
  errors, but also read the math in the sampled cards for TeX that won't render.

If a whole file misses the bar (wrong depth, padded with trivia), send that agent a
correction with SendMessage, quoting the specific cards, rather than rewriting it yourself.

### 7. Build

Write `WORK/manifest.json` and run `python SKILL_DIR/scripts/build_deck.py WORK/manifest.json`:

```json
{
  "deck_name": "BIOL 2100 Cell Biology (Midterm 2 - exam focus)",
  "out": "<folder>/BIOL2100_Midterm2_exam.apkg",
  "source_dir": "<folder>",
  "include_yield": ["high", "medium"],
  "subdecks": [{"title": "01 Intro to Cities", "cards": "WORK/cards/ch01.json"}]
}
```

- **Deck name.** Use the course name for `full`. Add "(<exam> - exam focus)" or "(<exam> -
  cram)" for the other depths, so the student can keep both decks side by side.
- **Output location.** Save the `.apkg` in the lecture folder unless the user said otherwise.
- **`include_yield`.** Set `["high","medium"]` for exam and `["high"]` for cram, as a backstop
  for stray low-yield cards. Omit it for full.
- **What the build does.** It renders figure slides into the cards and gives notes stable
  IDs, so re-importing a rebuilt deck updates the existing notes instead of duplicating
  them. It also re-opens the package and prints note and card counts.
- **Editing cards after the student has imported them.** Note IDs come from the card
  text. If you are about to rewrite card text, for example to fix formatting, first run
  `python SKILL_DIR/scripts/build_deck.py WORK/manifest.json --pin-guids`. It stores each
  card's current ID in a `guid` field, so the edited deck updates the student's existing
  notes and keeps their review history. Without it the import creates duplicates.
- **Blueprints (exam/cram).** Also join the blueprints into
  `<folder>/<course>_predicted_questions.md`. The predicted questions and their full-mark
  answers are a useful study sheet in their own right.

### 8. Report

Tell the user:

- the `.apkg` path, and how to import it (double-click it, or File → Import)
- a table of subdecks with note counts, plus the total card count (each cloze deletion
  becomes its own card)
- the depth used, and what kinds of material it left out
- for exam or cram depth, the top 3–5 predicted questions and the path to the
  predicted-questions file
- slide errors or contradictions the agents found, and which version the cards follow
- topics the user might expect but that aren't in the materials, and so have no cards
- if there are more than about 300 cards: Anki's default limit is 20 new cards a day, so
  they should raise it or use Custom Study if the exam is soon
