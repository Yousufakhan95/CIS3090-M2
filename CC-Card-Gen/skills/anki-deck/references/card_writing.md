# Writing the cards

## Output file

Write a JSON array (UTF-8) to the path in your brief. Each element:

```json
{
  "text": "Omitted variable bias: if the omitted variable is positively correlated with both X and Y, the OLS slope is biased {{c1::upward}}.",
  "extra": "The coefficient picks up the omitted variable's effect on Y because it moves with X.",
  "tags": ["ch02_empirical_methods", "omitted_variable_bias"],
  "source": "ch_2.pdf p.31",
  "yield": "high",
  "figure": {"file": "ch_2.pdf", "page": 31}
}
```

- `text` (required): the cloze sentence.
- `extra` (optional): 1–2 sentences of explanation or intuition, shown on the back. Use it
  for the "why", and for supporting details that don't deserve their own card.
- `tags` (required): the first tag is exactly the chapter tag from your brief; the second
  tag is a snake_case subtopic. Don't use spaces.
- `source` (required): the slide page(s) the fact comes from.
- `yield` (required): high, medium or low. Rate it using `exam_focus.md`.
- `guid` (only on existing cards): links the card to a note already in the student's
  Anki, so re-importing updates that note. If you are editing a card that has one, keep
  it unchanged. Never add one yourself.
- `figure` (optional): include it when a diagram, graph or table on that slide is the
  thing to learn. The slide image is shown on the back. Use it sparingly, for at most
  about 1 card in 10. `file` is the exact source file name (PDF only).

## Cloze rules

1. **Plain text plus MathJax.** Don't use HTML tags. Literal `<`, `>` and `&` are fine,
   because they are escaped at build time. Use `\n` for a line break if you really need
   one, but never inside math. All math is MathJax: see "Math: always MathJax" below.
2. **One atomic fact per deletion.** Cloze the meaningful term, number, direction or
   mechanism, never filler words. Use 1–3 deletions per card.
3. **Choose cloze numbers on purpose.** Use c1, c2 and c3 for facts that should be tested on
   separate cards. Reuse a number only when the items must be recalled together, such as
   a short two-item list.
4. **Make the answer unambiguous from the context.** If several answers could fit, add a hint:
   `{{c1::positive::sign}}`.
5. **Keep cards short**, ideally 35 words or fewer on the front. Split a long idea into
   several cards instead of writing a wall of text.
6. **Math is always typeset with MathJax**, in both `text` and `extra`. Follow the section
   below. Fake math in Unicode or ASCII is an error.
7. **Facts come from the materials**, stated the way the lecture states them. Don't invent
   numbers, dates or findings. Intuition you add in `extra` must agree with the slides.
   If you derive a result the slides only imply, such as a comparative static, say so in
   `extra`.
8. **Slides that contradict themselves.** When a caption disagrees with its own table, or a
   formula has an obvious typo, follow the table or the corrected formula (instructor
   annotations count as evidence). Say so in `extra`, and mention it in your final report.

Good and bad examples:

- Bad, clozes filler: `The {{c1::model}} shows that rents fall with distance.`
- Bad, the answer can't be pinned down: `{{c1::Toronto}} is a large city.`
- Bad, a list of six things clozed as one deletion. Split it, or cloze the 2–3 that matter.
- Good, a mechanism: `Agglomeration raises productivity through {{c1::sharing}}, {{c2::matching}} and {{c3::learning}} (Duranton–Puga).`
- Good, practice: `Practice: \(\hat{\beta} = -0.2\) with SE 0.05 gives a 95% CI of about {{c1::\((-0.3,\ -0.1)\)}}, so the effect is {{c2::statistically significant::significant or not?}}.`

(Examples show the card text as Anki receives it. In the JSON file every backslash is
doubled; see "JSON escaping" below.)

## Math: always MathJax

Anki typesets LaTeX through MathJax. **Every piece of math goes inside MathJax
delimiters**: formulas, equations, fractions, roots, logs, derivatives, sums, and any
variable that has a subscript, superscript, accent or Greek letter, even when it appears
alone in a sentence. Never fake math with Unicode or ASCII, such as `θ_A`, `G₁^L`,
`√(NL/π)`, `β̂`, `t̄`, `x²`, `r′(d)`, `ε_ijt` or `ln Q̃ = ...`. It renders as an
unreadable jumble, and the validator rejects it.

- **Delimiters.** Inline math: `\( ... \)`. Display math (a key formula on its own line):
  `\[ ... \]`. Never use `$...$`: Anki doesn't render it, and its cloze logic only works
  with `\(` and `\[`.
- **What stays plain text.** Ordinary numbers, percentages and money in prose: `12%`,
  `$22,000`, `about 0.17 fewer homes per acre`. Single plain letters used as names can
  stay plain (`X causes Y`), but anything with structure is math: `\(\beta_1\)`,
  `\(\theta_A\)`, `\(G^E\)`.
- **Use TeX commands, never Unicode symbols, inside math.**

  | Want | Write |
  |---|---|
  | Greek letters | `\alpha \beta \gamma \delta \Delta \varepsilon \theta \lambda \pi \sigma \tau \omega` |
  | accents | `\hat{\beta}`, `\bar{t}`, `\underline{t}`, `\tilde{Q}`, `\bar{d}` |
  | subscripts / superscripts | `x_i`, `\varepsilon_{ijt}` (braces for more than one character), `G^{E}`, `G_1^{L}`, `x^2` |
  | prime | `r'(d)` |
  | fraction, root | `\frac{2m\alpha}{c}`, `\sqrt{NL/\pi}` |
  | operators | `\le \ge \ne \approx \times \cdot \pm \to \Rightarrow \infty \partial \sum_{i=1}^{N} \ln \log \exp \max \min` |
  | words inside math | `\text{MRS}_1 + \text{MRS}_2 = \text{MC}`, `\text{Post} \times \text{Treat}` |
  | minus | plain `-` (not `−`) |

- **Escape TeX special characters inside math:** `\%`, `\$`, `\#`, `\&`. An unescaped `%`
  starts a TeX comment and swallows the rest of the formula.
- **No line breaks inside math**, and every `{` must have its matching `}`.
- **Prefer short inline formulas.** If a derivation has several steps, give each step its
  own card, or put the steps in `extra` as a short chain: `\(a = b \Rightarrow c = d\)`.

### Clozes and math

- Cloze a whole expression: `{{c1::\(G^E = \frac{2m\alpha}{c}\)}}`.
- Or cloze part of a formula with the cloze **entirely inside** the math:
  `\(G^E = {{c1::\frac{2m\alpha}{c} }}\)`. A cloze must never straddle `\(` or `\)`.
- **`{{` and `}}` appear only as cloze markup.** Wherever two TeX braces would touch,
  add a space: `\bar{Y}_{\text{post} }`, `\frac{a}{\sqrt{b} }`, `{{c1::\frac{a}{b} }}`
  and `x^{ {{c1::2}} }`. TeX ignores the space, but without it Anki ends the cloze at
  the wrong brace.
- Don't put a hint on a cloze that sits inside math. The hint would be typeset as math, so
  its words run together. Give the context in the prose around the formula instead, or
  cloze the whole expression and hint that: `{{c1::\(-t/L\)::sign and form}}`. Never use
  `::` inside the math itself.

### JSON escaping

Inside the JSON file **every backslash is doubled**. Write `"\\(\\frac{t}{L}\\)"`, and
Anki receives `\(\frac{t}{L}\)`. A single backslash either breaks the JSON (`\(`,
`\alpha`) or, worse, silently turns into a control character: `\frac` becomes a form
feed, `\theta` and `\tau` a tab, `\beta` and `\bar` a backspace, `\rho` and `\right` a
carriage return, and `\nu` and `\neq` a newline. The validator catches all of these. A
safe habit is to write the file with Python (`json.dump(cards, f, ensure_ascii=False,
indent=1)`), so you write each backslash once inside a raw string `r"..."`.

### Before and after

- Bad: `Decentralized FOC: ∂U_i/∂G_i = {{c1::2(θ_i − G_i)}} = 0, so G_i* = {{c2::θ_i}}.`
- Good: `Decentralized FOC: \(\frac{\partial U_i}{\partial G_i} = {{c1::2(\theta_i - G_i)}} = 0\), so \(G_i^* = {{c2::\theta_i}}\).`
- Bad: `the city radius is d̄ = {{c1::√(NL/π)}}`
- Good: `the city radius is \(\bar{d} = {{c1::\sqrt{NL/\pi} }}\)`
- Bad: `DID estimate = {{c1::(Ȳ_T,post − Ȳ_T,pre) − (Ȳ_C,post − Ȳ_C,pre)}}`
- Good: `\[\text{DID} = {{c1::(\bar{Y}_{T,1} - \bar{Y}_{T,0}) - (\bar{Y}_{C,1} - \bar{Y}_{C,0})}}\]` (1 = after, 0 = before)

## What to cover and what to skip

Cover every substantive slide, to the extent your depth allows (see `exam_focus.md`):
definitions, mechanisms, models and their assumptions, formulas and how to apply them,
how to interpret results, studies (design + finding), worked examples, and policies with
their effects. Turn any assignment, quiz or discussion questions that appear in the
slides, with their answers, into cards, because these are the instructor's own questions.

Skip course admin, polls, "introduce yourself" prompts, video links with no content, and
decorative slides.

Don't duplicate facts within your files.

## Reading figures and image-only slides

Extracted text loses graphs, tables, equations and handwriting. For every page your brief
lists as sparse, and any page whose text mentions a figure, table or equation, render it
and look at it:

```
python <SKILL_DIR>/scripts/render_pages.py "<source.pdf>" "<your image dir>" --pages 4,9-12
```

Then open the printed PNG paths with the Read tool. Use `--zoom 2.5` for small print.
Don't skip this step: in lecture slides the key result is often only in the figure.

## Check your work

Before replying, validate your file(s):

```
python <SKILL_DIR>/scripts/validate_cards.py "<your cards file>" --source-dir "<lecture folder>" --depth <depth>
```

Fix every ERROR. Read the WARN lines and fix the ones that are real problems.
