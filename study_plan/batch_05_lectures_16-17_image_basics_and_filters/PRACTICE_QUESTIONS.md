# Batch 5 practice questions

Question 1 is the study guide's own practice question. Questions 2 and 3 are written from the study guide's "Image processing basics" bullet list, in the exam's format. The textbook has no image processing exercises.

## Question 1. Study guide practice question 4

A student writes a \(3 \times 3\) mean filter but forgets to divide by 9, so every kernel weight is 1 instead of \(1/9\). What happens when this filter is applied to an 8-bit greyscale image, and the output is clipped to 0 to 255?

- A. The image is blurred exactly as before, because only the relative sizes of the weights matter.
- B. The image becomes about nine times brighter, so most of it ends up at 255 after clipping.
- C. The image is sharpened instead of blurred, because the larger weights emphasize the edges.
- D. Only the border pixels change, because the interior pixels are averaged either way.

## Question 2. Border strategies

You apply a \(5 \times 5\) kernel to an \(M \times N\) image. For each border strategy, give the output size and say what happens to the border pixels.

a. Copy of input pixels

b. Truncation of the image

c. Truncation of the kernel

d. Reflection

## Question 3. Unsharp masking

At one pixel, the original image has \(f = 100\) and the blurred image has \(S(f) = 80\). You use unsharp masking with \(k = 0.5\).

a. What is the edge image value \(g\) at this pixel?

b. What is \(f_{UM}\) at this pixel?

c. You raise \(k\) to 2. What changes, and what is the method sometimes called then?

---

## Answers

**Question 1. B.** The weights now sum to 9 instead of 1, so each output pixel is the neighbourhood's sum, not its average. A smoothing kernel has to sum to 1 to keep the mean intensity the same.

**Question 2.** A \(5 \times 5\) kernel reaches 2 pixels past its centre, so it fits only from \((2, 2)\) inward.

a. Copy keeps the size \(M \times N\). The 2-pixel border is copied from the input unprocessed.

b. Truncation of the image gives a smaller output, \((M - 4) \times (N - 4)\), offset from the input.

c. Truncation of the kernel keeps \(M \times N\). The border pixels are filtered with a cut-down kernel that covers only the pixels inside the image. Lecture 16 says this adds a lot of complexity.

d. Reflection keeps \(M \times N\). Coordinates outside the image are mirrored back inside, and every pixel gets filtered. Lecture 16 calls this the most useful option.

**Question 3.**

a. \(g = f - S(f) = 100 - 80 = 20\).

b. \(f_{UM} = f + k \cdot g = 100 + 0.5 \cdot 20 = 110\).

c. The sharpening gets stronger, and \(f_{UM} = 100 + 2 \cdot 20 = 140\). With \(k > 1\) the method is sometimes called high-boost filtering. Lecture 17 gives 0.2 to 0.7 as typical values.
