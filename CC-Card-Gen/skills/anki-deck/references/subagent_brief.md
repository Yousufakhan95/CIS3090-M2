# Card-writer brief template

Fill in everything in `<...>` and send the result as the subagent's prompt. Each subagent
starts with no context, so the brief has to stand on its own. Don't add your own guesses
about which topics a lecture covers. Agents given topic lists in testing spent effort
reporting "topic X isn't in the slides". Let them read the slides and decide.

---

You are writing Anki cloze flashcards for <course code and name> (<institution>, <term>).

EXAM CONTEXT: <2–5 sentences: which exam, its format (e.g. 4–5 short-answer questions,
no aids, calculators allowed), what it draws on (e.g. "assignments and lecture notes"),
anything the instructor said about scope or emphasis.>

DEPTH: <full | exam | cram>
<one of:>
- full: Cover every substantive slide. Rate every card's yield; the student will filter by it.
- exam: Write only cards you rate high or medium yield. Your job is to predict what this
  exam will test and cover that thoroughly, skipping backdrop such as history, background
  stats, anecdotes and trivia. Write the blueprint first.
- cram: Write only high-yield cards: the things most likely to cost marks if not known.
  Write the blueprint first.

Before starting, read these two files. They define the card format and the yield rubric:
- <SKILL_DIR>/references/card_writing.md
- <SKILL_DIR>/references/exam_focus.md

All math (formulas, and any variable with a subscript, accent or Greek letter) must be
typeset in MathJax, `\( ... \)` or `\[ ... \]`, never written as Unicode or ASCII
pseudo-math. Follow "Math: always MathJax" in card_writing.md, including its JSON
backslash rule. The validator rejects pseudo-math.

YOUR LECTURE(S):
- <Lecture title>
  - Extracted text (read all of it): <path to .txt> (pages are delimited by "===== PAGE N =====")
  - Source file: <path> (<N> pages). Sparse-text pages to render and view: <list>
  - Output: <WORK>/cards/<key>.json. The first tag is exactly "<chNN_topic>". Write source as "<file name> p.N".
  <- Blueprint (exam/cram only): <WORK>/blueprints/<key>.md>
<repeat for a second lecture if batched>

EXAM-SIGNAL DOCUMENTS (assignments, quizzes, past exams). Skim them for questions on
your lectures and treat those questions as top-priority material: <paths to extracted
.txt files, or "none available">

Scratch folder for rendered page images: <WORK>/img/<key>
Python: <python command>. Skill scripts are in <SKILL_DIR>/scripts.

When done, reply with:
- the card count per file and its yield breakdown
- the subtopics covered
- any slide errors or contradictions you found, and how you handled them
- content you deliberately skipped, and why
- any pages you couldn't read

Don't paste the cards into your reply.
