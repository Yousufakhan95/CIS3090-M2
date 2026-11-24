# Batch 2 practice questions

Try these before you look at the answers at the bottom.

## Question 1. Study guide practice question 5

A program takes 100 s on one core, 40 s on 4 cores, and 25 s on 8 cores. Which statement about its speedup and efficiency is correct?

- A. Speedup grows from 2.5 to 4, and efficiency drops from 0.625 to 0.5.
- B. Speedup grows from 2.5 to 4, and efficiency rises from 0.5 to 0.625.
- C. Speedup grows from 2.5 to 4, and efficiency drops from 0.4 to 0.25.
- D. Speedup grows from 2.5 to 4, which is linear, so efficiency stays at 1.

## Question 2. Textbook exercise 2.15a (p. 86), done by hand

A serial program takes \(T_{\text{serial}} = n^2\) microseconds. Its parallel version takes \(T_{\text{parallel}} = n^2/p + \log_2 p\) microseconds.

Fill in speedup \(S\) and efficiency \(E\) for these cases:

| \(n\) | \(p\) | \(S\) | \(E\) |
|---|---|---|---|
| 10 | 2 | | |
| 10 | 8 | | |
| 10 | 128 | | |
| 320 | 8 | | |
| 320 | 128 | | |

Then answer two questions. What happens to \(S\) and \(E\) when \(p\) grows and \(n\) stays fixed? What happens when \(n\) grows and \(p\) stays fixed?

## Question 3. Study guide, Amdahl's law

20% of a program is inherently serial, so \(a = 0.2\), and the rest parallelizes perfectly.

a. What speedup does Amdahl's law give on 4 cores?

b. What is the largest speedup you could ever get, no matter how many cores you add?

c. You can buy 4 cores or 64 cores. What does Amdahl's law tell you about that choice?

---

## Answers

**Question 1. A.** \(S_4 = 100/40 = 2.5\) and \(S_8 = 100/25 = 4\). \(E_4 = 2.5/4 = 0.625\) and \(E_8 = 4/8 = 0.5\). Speedup rises while efficiency falls, because the overheads grow with \(p\).

**Question 2.**

| \(n\) | \(p\) | \(T_{\text{parallel}}\) | \(S\) | \(E\) |
|---|---|---|---|---|
| 10 | 2 | 50 + 1 = 51 | 1.96 | 0.98 |
| 10 | 8 | 12.5 + 3 = 15.5 | 6.45 | 0.81 |
| 10 | 128 | 0.78 + 7 = 7.78 | 12.9 | 0.10 |
| 320 | 8 | 12800 + 3 = 12803 | 8.00 | 1.00 |
| 320 | 128 | 800 + 7 = 807 | 126.9 | 0.99 |

With \(n\) fixed and \(p\) growing, speedup rises but efficiency falls, because the \(\log_2 p\) overhead becomes a bigger share of the run time. With \(p\) fixed and \(n\) growing, speedup and efficiency both rise. The overhead grows more slowly than \(T_{\text{serial}}\), which matches Lecture 14 slide 39.

**Question 3.**

a. \(S = 1/((1 - 0.2)/4 + 0.2) = 1/(0.2 + 0.2) = 2.5\).

b. The limit is \(1/a = 1/0.2 = 5\).

c. 64 cores give \(S = 1/(0.8/64 + 0.2) \approx 4.7\), barely better than 2.5 on 4 cores and close to the cap of 5. Lecture 14 says to use Amdahl's law this way, to pick a sensible number of cores before you pay for hardware.
