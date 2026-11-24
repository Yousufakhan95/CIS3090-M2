import json

L16 = "05a_lecture_16_image_basics.pdf"
L17 = "05b_lecture_17_image_filters.pdf"
OUT = r"C:\github\CIS3090-M2\anki_work\v4\cards\b05.json"


def card(text, extra, tag, src, fig=None):
    c = {"text": text, "extra": extra, "tags": ["b05_image", tag], "source": src, "yield": "high"}
    if fig:
        c["figure"] = {"file": fig[0], "page": fig[1]}
    return c


cards = [
    # Lecture 16
    card(r"In discrete convolution, each output pixel is a {{c1::weighted sum}} of the input intensities in the neighbourhood around it. The weights are the coefficients of the {{c2::kernel}}, also called a mask or filter.",
         r"For a \(3 \times 3\) kernel, \(g(x,y) = \sum_{i=-1}^{1} \sum_{j=-1}^{1} w(i,j)\, f(x+i, y+j)\). A kernel centred on a pixel needs odd dimensions, such as \(3 \times 3\) or \(5 \times 5\).",
         "convolution", f"{L16} p.6, p.15"),
    card(r"A \(3 \times 3\) mean filter covers the pixels with values 131, 134, 193, 251, 249, 221, 220, 206 and 230. They sum to 1835, so the output pixel is 1835 times {{c1::\(\frac{1}{9}\)}}, which is {{c2::204}}.",
         r"Every weight in a \(3 \times 3\) mean filter is \(\frac{1}{9}\), so the output is the plain average of the 9 pixels under the kernel.",
         "convolution", f"{L16} p.17", (L16, 17)),
    card(r"Kernel normalization divides every coefficient by the {{c1::sum of the coefficients}}. A smoothing kernel then sums to {{c2::1}}, so an area of constant intensity keeps its {{c3::same value}} after filtering.",
         r"Lecture 16 says normalization prevents bias, so the original and filtered images have the same sum of pixel values. The study guide says the normalized kernel preserves mean intensity.",
         "kernel_normalization", f"{L16} p.12"),
    card(r"A student writes a \(3 \times 3\) mean filter with every weight 1 instead of \(\frac{1}{9}\). On an 8-bit image, the output comes out about {{c1::nine times brighter}}, and most pixels {{c2::clip at 255}}.",
         r"The kernel now sums to 9, so each output pixel is the neighbourhood sum instead of its average. This is study guide practice question 4, answer B.",
         "kernel_normalization", f"{L16} p.12"),
    card(r"At the border, part of the kernel falls outside the image. On an \(M \times N\) image, a \(5 \times 5\) kernel can only process a {{c1::\((M-4) \times (N-4)\)}} region, with its origin at {{c2::\((2,2)\)}}.",
         r"A \(3 \times 3\) kernel processes \((M-2) \times (N-2)\) from \((1,1)\), and a \(7 \times 7\) kernel processes \((M-6) \times (N-6)\) from \((3,3)\).",
         "image_borders", f"{L16} p.19-21"),
    card(r"With the copy of input pixels border strategy, the output keeps the {{c1::same size}} as the input. Its border pixels are {{c2::unprocessed copies}} of the input pixels.",
         r"The filter copies the input value wherever convolution is not possible, so the result has a border of unprocessed pixels.",
         "image_borders", f"{L16} p.22"),
    card(r"With truncation of the image, the filter removes every pixel it cannot convolve. The output is {{c1::smaller than}} the input and {{c2::offset}} relative to it.",
         r"A \(3 \times 3\) kernel on an \(M \times N\) image gives an \((M-2) \times (N-2)\) output, which starts at input pixel \((1,1)\).",
         "image_borders", f"{L16} p.21-22"),
    card(r"Truncation of the kernel treats border pixels as a special case and convolves them with a {{c1::modified kernel}} that leaves out the cells outside the image. Lecture 16 says this adds {{c2::considerable complexity}} to convolution.",
         r"A corner pixel gets a \(2 \times 2\) piece of the \(3 \times 3\) kernel, and an edge pixel gets a \(3 \times 2\) or \(2 \times 3\) piece. Every pixel is processed, so the output keeps the input's size.",
         "image_borders", f"{L16} p.23"),
    card(r"Reflected indexing checks whether a neighbour coordinate falls outside the image and, if it does, {{c1::reflects it back into the image}}. This simulates {{c2::mirroring}} the image at its borders.",
         r"Every pixel gets a full neighbourhood, so the output keeps the input's size and its border pixels are filtered too.",
         "image_borders", f"{L16} p.24"),
    card(r"Lecture 16 calls {{c1::reflected indexing}} the most useful border option. {{c2::Circular indexing}}, which treats the image as repeating endlessly in all directions, is rarely used in image processing.",
         r"Both are forms of the reflection strategy. Circular indexing takes a missing neighbour from the opposite side of the image.",
         "image_borders", f"{L16} p.24-25"),
    # Lecture 17
    card(r"A low-pass filter smooths an image by removing closely spaced intensity fluctuations. The fluctuations it removes include unwanted {{c1::noise}} and wanted {{c2::fine detail}}.",
         r"Low-pass means the filter passes low spatial frequencies. A high-pass filter is the difference between the image and its low-pass version.",
         "low_high_pass", f"{L17} p.4"),
    card(r"An omnidirectional high-pass sharpening kernel has {{c1::positive}} coefficients near its centre and {{c2::negative}} coefficients in its periphery. Its coefficients sum to {{c3::zero}}.",
         r"Lecture 17's example has \(8\) at the centre and \(-1\) in the other eight cells. Over a constant area the output is zero, and where intensity changes fast the output is large.",
         "sharpening", f"{L17} p.6-7"),
    card(r"Unsharp masking first builds an edge image \(g(x,y) = {{c1::f(x,y) - S(f(x,y))}}\), where \(S(f(x,y))\) is a {{c2::blurred}} version of the original image \(f(x,y)\).",
         r"Subtracting the blurred image removes the low spatial frequencies, so the edges and fine detail remain.",
         "unsharp_masking", f"{L17} p.9-10"),
    card(r"Unsharp masking adds the edge image \(g\) back to the original \(f\), so the sharpened image is \(f_{\text{UM} }(x,y) = {{c1::f(x,y) + k\,g(x,y)}}\).",
         r"Here \(k\) is a scaling constant. The study guide writes this as \(f_{\text{UM} } = f + kg\).",
         "unsharp_masking", f"{L17} p.11"),
    card(r"In unsharp masking, a larger \(k\) gives {{c1::more}} sharpening. Lecture 17 gives reasonable values of \(k\) between {{c2::0.2 and 0.7}}. With \(k > 1\), unsharp masking is called a {{c3::high-boost}} filter.",
         r"The edge image holds the high frequencies, so \(k\) sets how much of them goes back into the image.",
         "unsharp_masking", f"{L17} p.9, p.11"),
    card(r"Unsharp masking has two inherent limitations: {{c1::noise sensitivity}} and {{c2::overshoot}} on sharp details.",
         r"Noise has a strong high-frequency component, so sharpening makes it more prominent and you remove noise first. UM makes an edge steeper by making it taller, so bright details come out brighter than in the original.",
         "unsharp_masking", f"{L17} p.7, p.16-18"),
    card(r"A mean filter reduces noise but {{c1::blurs edges}}, because noise and edges are both sharp intensity transitions. A {{c2::larger kernel}}, or repeated application of a small one, gives stronger smoothing.",
         r"The \(3 \times 3\) and \(5 \times 5\) mean kernels sum their region and divide by 9 and 25. Lecture 17 says the mean filter works well against Gaussian noise.",
         "mean_filter", f"{L17} p.22-25"),
    card(r"A Gaussian filter is a smoothing filter with a {{c1::nonuniform}} kernel whose weights get {{c2::smaller}} with distance from the centre. The kernel is {{c3::isotropic}}, so it smooths the same amount in every direction.",
         r"The weights are \(w(i,j) = e^{-\frac{i^2 + j^2}{2\sigma^2} }\), so central pixels get more weight than pixels at the edge of the neighbourhood.",
         "gaussian_filter", f"{L17} p.27-30"),
    card(r"In a Gaussian filter, a larger \(\sigma\) gives {{c1::more blurring}} and a larger kernel. The kernel spans \(-[3\sigma]\) to \([3\sigma]\) in each direction, so \(\sigma = 1\) gives a {{c2::\(7 \times 7\)}} kernel.",
         r"Lecture 17 stops at \(\pm 3\sigma\) because the Gaussian weights are negligible beyond it. The \(7 \times 7\) size is worked out from that range, and it matches the slide's kernel for \(\sigma^2 = 1\).",
         "gaussian_filter", f"{L17} p.28-30"),
    card(r"A median filter sorts the intensities in the neighbourhood and replaces the pixel with the {{c1::middle-ranked}} value. It is a {{c2::non-linear}} filter from the rank, or order-statistic, family.",
         r"Lecture 17 splits noise suppression filters into mean-based filters and order-statistic filters.",
         "median_filter", f"{L17} p.21, p.34-35"),
    card(r"A median filter removes any structure that covers {{c1::less than half}} of the neighbourhood. That removes {{c2::impulse}} noise, and it also removes real thin lines and small objects.",
         r"When the noisy pixels are fewer than half, the median comes from the clean majority. Lecture 17 calls median filtering non-specific for this reason.",
         "median_filter", f"{L17} p.35"),
    card(r"Unlike a mean filter, a median filter does not {{c1::compress the brightness range}} in the neighbourhood, so it {{c2::preserves sharp edges}}.",
         r"Lecture 17 says it also preserves straight edge boundaries. Repeated median filtering can cause posterization.",
         "median_filter", f"{L17} p.38-39"),
    card(r"A \(5 \times 5\) median filter sorts the 25 neighbourhood values and outputs the {{c1::13th}} one. In Lecture 17's example, the centre pixel 104 becomes {{c2::98}}.",
         r"In the sorted list, twelve values are below 98 and twelve are above it.",
         "median_filter", f"{L17} p.36", (L17, 36)),
]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
print(len(cards), "cards written")
