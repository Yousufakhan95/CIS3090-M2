# Voice and style for this deck (overrides card_writing.md where they conflict)

The student reads these cards like a sharp classmate explaining things out loud. Conversational and concrete, story style when it helps, but no blabbering and no quiz or hint vibe. If a sentence feels like a riddle, rewrite it as a plain statement.

## Voice
- Short scene when it makes the fact stick: "You start 4 processes. Each one calls ... and learns ...". One scene per card at most.
- One idea per sentence. Split anything the reader has to reread.
- Active voice. Name the actor: the process, rank 0, the kernel, the core.
- Plain words. "use", never "utilize" or "leverage".
- Whole sentences with articles and verbs. Spell out arrows and abbreviations in prose.

## Cloze rules that override card_writing.md
- NEVER use cloze hints. No `{{c1::answer::hint}}` anywhere. The sentence around the blank must make the answer obvious.
- No prompt-style text such as "sign or not?", "grows or shrinks?", "Practice:", "Q:".
- Cloze only the load-bearing fact. 1 to 3 deletions per card.
- Front under 40 words. Extra is 1 to 2 plain sentences that add the "why".

## Unslop rules (apply to text AND extra)
- No em dashes, en dashes, or hyphens used as dashes. No parentheses used as dashes or asides. Use a period or a comma. Hyphenated words like "shared-memory" are fine. A real minus sign inside MathJax is fine.
- A colon only goes before a list or an example, never mid-sentence as a connector. No semicolons.
- No AI vocabulary: additionally, crucial, delve, enhance, foster, landscape, pivotal, showcase, testament, underscore, vibrant.
- Say "is" or "has", not "serves as", "stands as", "boasts", "features".
- No "not just X, but Y". No forced lists of three.
- One name per thing. Use the course's name and repeat it.
- No trailing "-ing" phrases that add nothing ("..., ensuring that ...").
- No vague attributions. Name the source: "Lecture 14 says", "the study guide says".
- Cut filler and adverbs. Give the number instead.
- No metaphors, personified code, or figurative verbs ("slams", "dies", "wins", "shines", "kills", "tax", "cranks up"). Use the literal verb.
- At most one hedge per card, and it is "may".
- Straight quotes only. No emojis. No HTML.

## Bad vs good
Bad: `Efficiency usually {{c1::drops::direction}} as \(p\) grows because of overheads that grow with \(p\).`
Good: `Add more processes and efficiency \(E = S/p\) usually {{c1::falls}}, because more time goes to coordination and messaging.`

Bad: `An MPI send matches a receive only if communicator, {{c1::tag}}, and {{c2::source}} agree.`
Good: `A receive only matches a message sent on the same communicator, with the same {{c1::tag}}, from the expected {{c2::source}} rank.`

Bad: `Warp dies on excessive copies — tiny problems can't amortize them.`
Good: `On a small problem, the copy to the GPU can take longer than the compute it saves.`

## MPI names in math
Function and constant names with underscores must go inside MathJax with escaped underscores, for example `\\(\\mathrm{MPI\\_Comm\\_rank}\\)` in the JSON file. A bare `MPI_Send` in prose fails validation. Python identifiers with underscores do the same: `\\(\\text{wp.zeros\\_like}\\)`.
