# Batch 4 practice questions

Question 1 is the study guide's own practice question. Questions 2 and 3 are written from the study guide's "GPGPU with Warp" bullet list, in the exam's format. The textbook has no Warp exercises.

## Question 1. Study guide practice question 3

A Warp kernel needs to run over an array of \(N\) elements on an Nvidia GPU. What do you pass to `wp.launch`?

- A. Only the kernel, because Warp works out the number of threads, the arguments, and the device on its own.
- B. The kernel, its arguments, and the number of GPU cores to use, since Warp splits the array among them.
- C. The kernel, `dim=N`, the kernel's arguments in `inputs=` in order, and `device="cuda"`.
- D. The kernel's arguments and the device, since Warp finds the right kernel from the arguments' types.

## Question 2. Single answer

A student moves a loop over 1,000 floats from NumPy into a Warp kernel with `device="cuda"`. The Warp version runs slower than the NumPy version. What is the most likely reason?

- A. With `device="cuda"`, Warp runs the kernel as single-thread serial code.
- B. Copying the data between host memory and GPU memory takes longer than the compute the GPU saves.
- C. The kernel has to return its result, and returning values from a GPU is slow.
- D. `wp.tid()` gives every thread the same index, so all threads do the same work.

## Question 3. Select all that apply

Which statements about a function marked `@wp.kernel` are true?

- A. Every parameter needs a declared type.
- B. It returns its result with a `return` statement.
- C. It calls `wp.tid()` to get the index of the element this thread handles.
- D. You write the body for one element, and Warp launches one thread per element.
- E. A thread can safely read another thread's output from the same launch.

---

## Answers

**Question 1. C.** You pass the kernel, `dim=N` for the number of threads, the arguments in `inputs=` in parameter order, and the device. The device is optional and defaults to Warp's default device.

**Question 2. B.** The CPU and GPU have separate memory, so the data crosses the bus to the GPU and back. On a small problem, that copy costs more than the parallel compute saves. Option A describes `device="cpu"`, not `"cuda"`.

**Question 3. A, C, D.** Kernels are statically typed and write their results into an output array instead of returning them. A thread's output may depend only on the inputs, never on another thread's output. On the exam, choosing B or E on a select-all question scores 0 for the whole question.
