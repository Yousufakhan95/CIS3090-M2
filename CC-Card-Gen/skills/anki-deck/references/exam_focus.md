# Predicting what gets tested: yield ratings and exam-focused cards

Every card gets a `yield` rating (high / medium / low), whatever the depth. At `depth=full`
you write all three levels and the rating becomes a tag the student can filter on. At
`depth=exam` you write only high and medium, and at `depth=cram` only high. In exam and cram
mode you are not summarizing the lecture: you are betting on the exam. Write the deck
that maximizes marks per minute of study, and be decisive about it. A student using this
mode has explicitly asked you to skip material you judge unlikely to be tested.

## How instructors actually write exams

Most instructors write an exam by going back over their own learning objectives,
assignments, quizzes and the slides they spent the most time on. Then they write questions
that make students *use* the material:

- define a core concept, or distinguish two that are easy to confuse
- explain a mechanism (why X leads to Y)
- state a model's assumptions, set it up, and derive or describe its predictions
- run comparative statics (what happens to the equilibrium when a parameter changes)
- compute something with a formula from the lecture, often a worked example with the numbers changed
- interpret a result: a regression coefficient, a graph, a table, a study's finding
- evaluate a research design or a policy (does it identify a causal effect? what are the trade-offs?)
- apply a framework to a new scenario the lecture did not cover

They seldom ask students to reproduce background and motivation: historical narrative,
timelines and dates, statistics shown for colour, rankings, anecdotes, biographical
details, minor names, what a video showed, or material the slides mark "not required".

## Evidence ladder (strongest first)

1. **Explicit statements**: "this will be on the exam", "you need to know", "not required in
   this class", the exam's stated format and scope, review sheets, learning objectives.
2. **Past exams, practice exams, quizzes, assignments** (with solutions if given). Exams
   reuse their question types and sometimes the questions themselves. A syllabus line like
   "quizzes serve as mock midterms" or "content is from assignments and lecture notes"
   makes these the main blueprint.
3. **Practice or worked-example slides, and slides quoting assignment questions with
   model answers.** These are the instructor's own sample questions.
4. **Summary, conclusion and "key takeaway" slides.**
5. **Emphasis**: how many slides a topic gets, repetition across lectures, boxed or bold
   statements, handwritten annotations, "important"/"remember" markers.
6. **Discipline norms**: what exams in this subject and at this level usually ask.

When signals conflict, the higher rung wins. Material explicitly excluded (rung 1) is
excluded even if it occupies many slides.

## Yield rubric

**high**: the lecture's core concepts, models and methods; anything that appears on rungs
1–3; formulas and how to apply them; mechanisms and causal chains; assumptions and what
breaks when they fail; comparative statics; how to read the lecture's key graph or
regression output; distinctions between commonly confused ideas; a study's design and
headline finding when the study teaches a method or carries the lecture's main conclusion.

**medium**: supporting concepts; the *lesson* of a case study or example (not its
details); the direction and rough size of headline findings from secondary studies;
pros/cons lists for policies the lecture discusses; definitions that a short answer
would need in passing.

**low**: history and timelines, dates, background statistics, rankings, exact figures
from motivation slides, names of minor people and places, anecdotes, institutional detail
that the lecture doesn't analyse, numbers that aren't a central result, and anything the
slides mark as not required.

### "Avoid history" is relative to the course

Content is low-yield when it is *backdrop*, not when it happens to involve the past. In a
history course chronology is the subject and dates are high-yield. In an economics,
science or engineering course, a historical case study is there to illustrate an idea:
card the idea, not the story.

- Low (skip in exam mode): `At the end of 1974 NYC faced a projected budget shortfall of {{c1::$1.5B}}.`
- High (the lesson the case teaches): `NYC's 1975 fiscal crisis came from years of {{c1::borrowing to cover operating costs}}, which produced {{c2::huge deficits}} once the economy stagnated.`
- Low: `TomTom 2025: {{c1::London}} has the world's longest average travel time per 10 km.`
- High: `In the monocentric city model with fixed lot size \(L\), the rent gradient is \(r'(d) = {{c1::-t/L}}\), so higher commuting costs make rents fall {{c2::faster}} with distance from the CBD.`

A number belongs in an exam-mode deck when it *is* the lesson: a study's headline
estimate that the lecture builds its conclusion on, a threshold that defines a method
(e.g. a GPA cutoff in a regression-discontinuity example), or a parameter in a worked
example the student must be able to reproduce.

## Match the exam format

Read the format from the syllabus or exam context and bend the cards toward it.

- **Short answer or written response**: build the parts of a full-mark answer. Use
  "Explain why…" cards, split multi-reason answers into one cloze per reason, and pair each
  assumption with its consequence. Include the definition sentence a marker expects to see.
- **Multiple choice**: fine distinctions, common traps, near-miss concepts, signs and
  directions, "which of these is NOT…".
- **Calculations and problem sets**: formula cards (cloze each component separately), setup
  cards (what to compute first), worked examples with the actual numbers, and comparative
  statics in words ("if t rises, the gradient becomes steeper").
- **Graph-based questions**: what shifts, what slopes which way, where equilibrium moves.
  Attach the slide figure.
- **Essays**: frameworks, argument structures, the strongest evidence for each side.

## Blueprint first (exam and cram mode)

Before writing any cards, write the blueprint file you were given: for each lecture, list
6–12 questions you predict could appear on the exam, most likely first. The blueprints
become a Markdown study sheet, so write their math as Markdown LaTeX (`$\bar{d} =
\sqrt{NL/\pi}$`, `$$...$$` for display), never as Unicode pseudo-math. (The `$`
delimiters are for blueprints only; cards use `\( ... \)`.) Use this format:

```
## <Lecture title>
1. [high] Explain why regression discontinuity estimates are "local". (evidence: rung 3,
   p.14 practice slide; quoted Assignment 1 answer p.2)
   Full-mark answer: compares units just above/below cutoff; identifies effect only at the
   cutoff; may not generalize to units far from it.
2. ...
```

Then write cards so that every key point of every full-mark answer is covered by at least
one cloze. Finally, add high-yield cards for anything the exam needs that no predicted
question captured, such as core definitions. Working from the blueprint keeps the cards as
answers to likely questions rather than restatements of slides. It is also a useful study
sheet in its own right.

## Calibration

There is no quota, but card count should follow the exam, not the slide count. Use your
blueprint to estimate how much of the exam this lecture will account for, and size its
cards to that share. If you predict at most one question from a lecture, cover the
answers to that question and its close variants well, and stop there. A 60-slide
introduction can deserve fewer cards than a 30-slide lecture on the course's central model.

As a rough guide, exam mode keeps about a third to a half of what full mode would produce.
A dense methods lecture might keep 70%, and a motivation-heavy introduction 25–40%. Cram
mode is usually 10–25%. Medium yield is for material a full-mark answer would use, not a
holding pen for interesting material you're reluctant to drop. If you find yourself
writing an exam-mode card you would rate low, delete it.
