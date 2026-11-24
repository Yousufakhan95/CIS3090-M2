import json
from pathlib import Path

T = "b07_warp_images"

cards = [
    {
        "text": "Warp image pipeline: PIL Image.open, check mode, NumPy {{c1::float32}}, {{c2::wp.array}} on device, zeroed output, launch kernel, {{c3::.numpy()}}, then Image.fromarray and save.",
        "extra": "Study-guide order: PIL to NumPy to Warp to kernel to NumPy to PIL. NumPy bridges both directions.",
        "tags": [T, "pipeline_order"],
        "source": "07_lecture_18_warp_images.pdf p.3",
        "yield": "high",
    },
    {
        "text": "PIL modes: L is greyscale shape {{c1::(h, w)}}; RGB is {{c2::(h, w, 3)}}; RGBA is {{c3::(h, w, 4)}}.",
        "extra": "Each channel is an 8-bit unsigned integer. Always check image.mode.",
        "tags": [T, "image_modes"],
        "source": "07_lecture_18_warp_images.pdf p.5",
        "yield": "high",
    },
    {
        "text": "Pillow image.size is {{c1::(w, h)}}, but colour NumPy shape is {{c2::(h, w, c)}}. Expand greyscale to {{c3::(h, w, 1)}} for one 3D kernel; strip the channel before saving mode L.",
        "extra": "PIL will not build a greyscale image from shape (h, w, 1). Launch with dim equal to the 3D array shape.",
        "tags": [T, "size_vs_shape"],
        "source": "07_lecture_18_warp_images.pdf p.8",
        "yield": "high",
    },
    {
        "text": "On RGBA, filter only channels with {{c1::k < 3}} and {{c2::copy alpha unchanged}}. Leaving alpha at 0 (from zeros) saves a {{c3::fully transparent}} image.",
        "extra": "Filtering alpha is meaningless but often looks fine if the image is opaque, so the bug is silent.",
        "tags": [T, "rgba_alpha"],
        "source": "07_lecture_18_warp_images.pdf p.19",
        "yield": "high",
        "figure": {"file": "07_lecture_18_warp_images.pdf", "page": 19},
    },
    {
        "text": 'Warp device: Docker on a laptop uses {{c1::"cpu"}}; Nvidia GPU or Colab uses {{c2::"cuda"}}.',
        "extra": "cpu is the portable serial fallback; cuda runs the kernel in parallel on the GPU.",
        "tags": [T, "device"],
        "source": "07_lecture_18_warp_images.pdf p.4",
        "yield": "high",
    },
    {
        "text": "Input Warp buffer: {{c1::wp.array}}(npInData, dtype=wp.float32, device=device). Output: {{c2::wp.zeros_like}}(inWarpImage) — same shape, dtype, and device, filled with zeros.",
        "extra": "Study guide also lists wp.zeros(...). On cuda, wp.array uploads host memory to the device.",
        "tags": [T, "wp_array"],
        "source": "07_lecture_18_warp_images.pdf p.12",
        "yield": "high",
    },
    {
        "text": "Pass neighbourhood size, unsharp k, or Gaussian sigma into a Warp kernel as {{c1::typed arguments}}; the value is read at {{c2::launch}} and can change without recompiling.",
        "extra": "Example: factor: float in the signature, then pass 2.0 in inputs=. Closures are not needed in this course.",
        "tags": [T, "kernel_constants"],
        "source": "07_lecture_18_warp_images.pdf p.13",
        "yield": "high",
    },
]

assert len(cards) <= 10
assert all(c["yield"] == "high" for c in cards)

out = Path(r"C:\github\CIS3090-M2\anki_work\cards\b07.json")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
print(len(cards))
