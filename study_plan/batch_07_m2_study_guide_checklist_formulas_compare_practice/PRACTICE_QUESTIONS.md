# Batch 7 practice questions

These come from the study guide's table "Pthreads vs MPI vs Warp". Questions 1 and 2 are select-all-that-apply, the format the exam uses for this kind of table. Remember the scoring. You get partial credit for picking some correct options, but any wrong pick scores 0 for the whole question.

## Question 1. Select all that apply

Which statements are true of MPI?

- A. It runs separate processes that exchange data by message passing.
- B. All its processes share one address space.
- C. It has built-in collectives such as `MPI_Bcast`, `MPI_Reduce`, and `MPI_Allreduce`.
- D. Frequent small messages between machines are one of its common pitfalls.
- E. It only runs on a single shared-memory machine.

## Question 2. Select all that apply

Which are common pitfalls of Warp, according to the study guide?

- A. Too many copies between host and device
- B. Non-contiguous data
- C. Oversubscription
- D. Problems too small to pay for the copies
- E. Mismatched tags

## Question 3. Single answer

Which workload best fits each model? Match them, then pick the option that gets all three right.

Workloads:

1. Many threads on one multicore machine update a shared hash table, with careful locking.
2. A large simulation splits into big independent chunks that exchange boundary values once per time step, across several machines.
3. The same arithmetic runs on each pixel of a 4K image.

- A. 1 Pthreads, 2 MPI, 3 Warp
- B. 1 MPI, 2 Pthreads, 3 Warp
- C. 1 Warp, 2 MPI, 3 Pthreads
- D. 1 Pthreads, 2 Warp, 3 MPI

---

## Answers

**Question 1. A, C, D.** B describes Pthreads. E is wrong because MPI processes run across one or more nodes.

**Question 2. A, B, D.** Oversubscription is a Pthreads pitfall, and mismatched tags are an MPI pitfall. Picking either one scores 0.

**Question 3. A.** The study guide says Pthreads fits fine-grained shared-state updates with careful synchronization. MPI fits large independent chunks with modest communication between steps. Warp fits large data-parallel maps with uniform work and enough of it to pay for the copies.
