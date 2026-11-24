# Batch 1 practice questions

Try these before you look at the answers at the bottom.

## Question 1. Textbook exercise 2.8 (p. 85)

Each test `my_rank == ...` and each function `A` to `F` takes 1 unit of time.

```c
for (i = 0; i < n; i++) {
   if (my_rank == 0) {
      A(&args1, i);
      B(&args2, i);
   } else if (my_rank == 1) {
      C(&args3, i);
      D(&args4, i);
   } else if (my_rank == 2) {
      E(&args5, i);
      F(&args6, i);
   }
}
```

a. Three threads run this on a SIMD system. Make a table for one iteration that shows what each thread does in each time unit and when it sits idle.

b. Now three threads run it on a MIMD system. Make the same table.

## Question 2. Textbook exercise 2.10 (p. 85)

Flynn's taxonomy has a fourth type, multiple instruction, single data, or MISD. How would an MISD system work? Give an example.

## Question 3. Study guide, data layout (Lecture 7)

A simulation stores its particles as a linked list. Each node is a struct with pointers to its position and velocity. The program now has to send all particles to other ranks with MPI and copy them to a GPU. Which change helps most?

- A. Keep the linked list, but send each node in its own MPI message.
- B. Store the particles in flat contiguous arrays of plain values, so each array moves as one block.
- C. Add more pointers so each node can find its neighbours faster.
- D. Keep the layout, because MPI and the GPU copy follow pointers automatically.

---

## Answers

**Question 1a. SIMD, 9 time units.** Every datapath follows the same instruction stream, so the branches run one after another.

| Time | Thread 0 | Thread 1 | Thread 2 |
|---|---|---|---|
| 1 | test rank 0 | test rank 0 | test rank 0 |
| 2 | A | idle | idle |
| 3 | B | idle | idle |
| 4 | idle | test rank 1 | test rank 1 |
| 5 | idle | C | idle |
| 6 | idle | D | idle |
| 7 | idle | idle | test rank 2 |
| 8 | idle | idle | E |
| 9 | idle | idle | F |

**Question 1b. MIMD, 5 time units.** Each thread runs on its own and never waits for the others.

| Time | Thread 0 | Thread 1 | Thread 2 |
|---|---|---|---|
| 1 | test rank 0 | test rank 0 | test rank 0 |
| 2 | A | test rank 1 | test rank 1 |
| 3 | B | C | test rank 2 |
| 4 | done | D | E |
| 5 | done | done | F |

The lesson is the one from Lecture 14. SIMD is good for simple loops over arrays. When the threads take different branches, most datapaths sit idle.

**Question 2.** Several processing units run different instructions on the same data stream. A common example is fault-tolerant redundant computing, where several units compute on the same input and their results get compared. Lecture 14 says hardly any real systems work this way.

**Question 3. B.** Lecture 7 says contiguous data is easy to cache and easy to transfer, because you move N bytes starting from address M in one block. Pointers scatter the data across memory. One message per node, as in option A, adds a lot of communication overhead.
