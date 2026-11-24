# CIS*3090 Midterm 2 Study Plan

**Exam:** Thursday, November 26, 2026  
**Book:** *An Introduction to Parallel Programming* (Pacheco & Malensek, 2nd ed.)

Course materials live under `Content/` (week folders + textbook excerpts).  
For Midterm 2 readings go straight to `Content/11_week11_midterm2/textbook_m2_readings/`, or work through `study_plan/` batch by batch.

Every reading below is something a lecture slide covers. The textbook pages replace the matching slides. Anything the slides don't teach is cut.

Total textbook reading: **49 pages**, plus 6 slides from Lecture 7 and Lectures 15 to 18.

---

## Batches

| Batch | What to read | Replaces |
|------:|--------------|----------|
| 1 | Textbook pp. **21–23** and **31–38**, plus Lecture 7 slides **11–16** | Lecture 7 data layout, Lecture 14 part 1 |
| 2 | Textbook pp. **61–66** (§§2.6.1–2.6.2) | Lecture 14 part 2 |
| 3 | Textbook pp. **90–121** (§§3.1–3.4.8, skip §3.4.6) | Lectures 9, 10, 11 |
| 4 | Lecture 15 slides | none, slides only |
| 5 | Lectures 16 and 17 slides | none, slides only |
| 6 | Lecture 18 slides | none, slides only |
| 7 | M2 study guide, once as a checklist | none |

Each textbook batch folder has a `READ_THESE_PAGES.txt` with the exact start and stop headings.  
Every batch folder has a `PRACTICE_QUESTIONS.md` with three questions, or four for batch 3. Answers are at the bottom. The questions come from the study guide's practice set, the textbook's end-of-chapter exercises, or the study guide's topic bullets written in its exam format.

### Where to stop inside a page

- Batch 1: stop on p. 23 at "2.2.2 Cache mappings". Stop on p. 38 at "Distributed-memory interconnects".
- Batch 2: stop on p. 66 at "2.6.3 Scalability".
- Batch 3: skip §3.4.6 Data distributions (bottom of p. 116 to p. 117). Stop on p. 121 at "3.4.9 Allgather".

### Do not read

- pp. 17–20 and 23–31: von Neumann, cache mappings, virtual memory, ILP, hardware multithreading. The M2 guide tests only the data layout part of Lecture 7.
- pp. 38–49 after "Distributed-memory interconnects": ring, mesh, hypercube, bisection width, cache coherence. No slide covers these.
- pp. 66–70: scalability, taking timings, GPU performance. Lecture 14 cites only §§2.6.1–2.6.2.
- pp. 121–134: Allgather, matrix-vector, derived datatypes, MPI performance evaluation. Not on any M2 slide or the guide.
- pp. 135+: odd-even sort, Lectures 12–13. Not on the midterm.
- Chapter 4 (Pthreads): the M2 guide's compare table is enough.

### Slides you can skip

Lectures 9, 10, 11, 14, and Lecture 7 apart from slides 11–16. The batch readings cover them.  
Lectures 12–13 are out of scope.

---

## Anki deck

`study_plan/CIS3090_Midterm2_cram.apkg` has 139 notes, 263 cards, and 8 subdecks that match the batches. Batch 3 is split into 03a basics and 03b collectives.  
It was built with Ashton Long's anki-deck skill at cram depth, with `anki_work/v4/STYLE.md` as the voice and unslop rules.  
Card sources: `anki_work/v4/cards/`. Untrimmed writer output: `anki_work/v4/cards_full/`. Rebuild with `python <anki-deck skill>/scripts/build_deck.py anki_work/v4/manifest.json`.  
Predicted questions with full-mark answers: `study_plan/CIS3090_Midterm2_predicted_questions.md`.

## Formulas to know

- Speedup: \(S = T_{\text{serial}} / T_{\text{parallel}}\)
- Efficiency: \(E = S / p\)
- Linear speedup: \(S = p\)
- Amdahl: \(S = 1 / ((1 - a)/p + a)\), limit \(1/a\)
