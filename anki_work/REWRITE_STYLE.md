# Card rewrite style

Write for a student who is hearing this out loud from a sharp classmate.
Not a textbook. Not a chatbot. Not a riddle.

## Voice
- Conversational and concrete. Tell a tiny scene when it helps ("you fire four workers, they each finish a chunk, then...").
- One idea per sentence.
- Active voice. Name the actor.
- Plain words. Say "use", not "utilize".
- Straight quotes. No em dashes, en dashes, or hyphen-as-dash. Use a period or a comma.
- No AI filler: additionally, crucial, delve, enhance, foster, landscape, pivotal, showcase, testament, underscore, vibrant.
- No "not just X but Y". No forced lists of three. No chatbot closers.
- At most one hedge: "may".

## Cloze
- Cloze the load-bearing fact only.
- Never use Anki cloze hints (`{{c1::answer::hint}}`). Context in the sentence must make the blank obvious.
- Do not write "sign or not?", "grows or shrinks?", or quizzy prompt vibe.
- Keep MathJax for real math: `\\( ... \\)` with doubled backslashes in JSON.
- Front ideally under 40 words. Back Extra: 1 to 2 plain sentences that add the why.

## Depth
- high yield only. Same topics as before. Keep the note count within ±2 of the old file.
- Facts from the source materials only.

## Bad vs good
Bad: `Efficiency usually {{c1::drops::direction}} as \(p\) grows because of overheads that grow with \(p\).`
Good: `Add more processes and efficiency \(E = S/p\) usually {{c1::falls}}, because you spend more time on coordination and messaging.`

Bad: `An MPI send matches a receive only if communicator, {{c1::tag}}, and {{c2::source}} agree.`
Good: `A receive only wakes up when the message hits the same communicator, the same {{c1::tag}}, and the expected {{c2::source}} rank.`
