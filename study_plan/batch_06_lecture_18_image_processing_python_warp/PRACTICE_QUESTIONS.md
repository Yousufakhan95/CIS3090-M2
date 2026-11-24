# Batch 6 practice questions

These are written from the study guide's Warp bullets on the image pipeline, image modes, and constants, in the exam's format. Neither the study guide nor the textbook has practice questions for Lecture 18.

## Question 1. Put the steps in order

You filter a photo on disk with a Warp kernel and save the result. Put these steps in order.

- `wp.launch(...)`
- `Image.fromarray(...)` and save
- `Image.open(...)` and check `image.mode`
- `wp.zeros_like(...)` for the output
- `np.asarray(image, dtype=np.float32)`
- `.numpy()` on the output array
- `wp.array(...)` on the NumPy array

## Question 2. Single answer

A kernel sharpens an RGBA image. The output array comes from `wp.zeros_like`. The kernel writes to channels \(k < 3\) and does nothing for channel 3. What does the saved image look like?

- A. Correct, because alpha is ignored when the image is saved.
- B. Fully transparent, because alpha stays 0 from `wp.zeros_like`.
- C. Greyscale, because only three channels were written.
- D. Correct, but the colours are blurred instead of sharpened.

## Question 3. Single answer

You want to pass the unsharp masking strength \(k = 0.6\) into a Warp kernel and try other values later. What is the right way?

- A. Set a global Python variable and read it inside the kernel.
- B. Add a typed parameter such as `k: float` to the kernel and pass the value in `inputs=` at launch.
- C. Hard-code 0.6 in the kernel and edit the source for each new value.
- D. Store it in the output array before the launch and read it back with `wp.tid()`.

---

## Answers

**Question 1.**

1. `Image.open(...)` and check `image.mode`
2. `np.asarray(image, dtype=np.float32)`
3. `wp.array(...)` on the NumPy array
4. `wp.zeros_like(...)` for the output
5. `wp.launch(...)`
6. `.numpy()` on the output array
7. `Image.fromarray(...)` and save

Lecture 18 follows this order, with NumPy in the middle both ways.

**Question 2. B.** The kernel has to copy alpha from the input unchanged. If it skips alpha, every pixel keeps the 0 from `wp.zeros_like`, and 0 alpha means fully transparent. Mode L has shape \((h, w)\), RGB \((h, w, 3)\), and RGBA \((h, w, 4)\), with alpha at channel index 3.

**Question 3. B.** The study guide and Lecture 18 pass constants as typed kernel arguments. Warp reads the value at launch, so you can change it without recompiling the kernel.
