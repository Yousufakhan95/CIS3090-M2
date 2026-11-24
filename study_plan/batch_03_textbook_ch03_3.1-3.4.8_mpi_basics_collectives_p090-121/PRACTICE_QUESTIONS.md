# Batch 3 practice questions

This batch is the biggest one, so it gets four. Try them before you look at the answers at the bottom.

## Question 1. Study guide practice question 1

A program uses MPI on \(p\) processes to compute the sum of \(g(a[i])\) over a large array. The processes run on different machines connected by a slow network, so every message is expensive. Which design is the best fit?

- A. Rank 0 sends each element to a worker, and the worker sends that element's result straight back.
- B. Every rank reads the whole array from stdin and computes the full sum itself, so no messages are needed.
- C. Each rank works on its own block and calls `MPI_Allreduce` after every element to keep a running total.
- D. Each rank computes a local sum over its own block, and one `MPI_Reduce` combines the local sums on rank 0.

## Question 2. Study guide practice question 2

A manager process receives a result from any worker with

```c
MPI_Recv(buf, 256, MPI_CHAR, MPI_ANY_SOURCE, TAG_RESULT, MPI_COMM_WORLD, &status);
```

The result may be shorter than 256 characters. How does the manager find out which worker sent it, and how many characters it contains?

- A. It reads `status.MPI_SOURCE`, and calls `MPI_Get_count(&status, MPI_CHAR, &n)` for the number of characters.
- B. `MPI_Recv` returns the number of characters, and MPI overwrites the source argument with the sender's rank.
- C. It reads `status.MPI_TAG`, which MPI sets to the sender's rank, and uses `sizeof(buf)` for the number of characters.
- D. It cannot find the sender, so each worker must include its rank in the message, and `sizeof(buf)` gives the count.

## Question 3. Textbook exercise 3.1 (p. 148)

In the greetings program from Lecture 9, each worker sends its string with a count of `strlen(greeting)+1`.

a. What happens if the workers send `strlen(greeting)` instead?

b. What happens if they send `MAX_STRING` instead?

## Question 4. Textbook exercise 3.7 (p. 149)

What do `MPI_Bcast`, `MPI_Reduce`, `MPI_Allreduce`, `MPI_Scatter`, and `MPI_Gather` do if the communicator contains a single process?

---

## Answers

**Question 1. D.** One local sum per rank and a single Reduce sends one value per process. Option A sends two messages per element. Option B breaks the rule that only rank 0 reads stdin. Option C calls a collective once per element, which means many small messages.

**Question 2. A.** After a receive with `MPI_ANY_SOURCE`, the sender is in `status.MPI_SOURCE` and the tag is in `status.MPI_TAG`. The element count is not a field of the status, so you call `MPI_Get_count`. `MPI_Recv` returns an error code, not a count, and the 256 you passed is only the buffer's capacity.

**Question 3.**

a. The terminating `'\0'` never gets sent. Rank 0's buffer holds the characters with no terminator after them, so `printf` keeps reading whatever bytes sit after them. That may print garbage, or leftover text from an earlier, longer message.

b. It still works. The string is terminated inside the buffer, and rank 0's receive count of `MAX_STRING` is large enough. It sends extra unused bytes on every message, which wastes network time.

**Question 4.** They all still work. A collective only needs every process in the communicator to call it, and here that is one process.

- `MPI_Bcast` does nothing visible, because the root already has the data.
- `MPI_Reduce` and `MPI_Allreduce` copy the single input into the output, since the sum of one value is that value.
- `MPI_Scatter` copies the whole send buffer into the one process's receive buffer.
- `MPI_Gather` copies the one process's chunk into the receive buffer.
