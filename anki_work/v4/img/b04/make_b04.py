import json, os

SRC = "04_lecture_15_gpgpu_warp.pdf"
T = "b04_gpgpu_warp"

def c(text, extra, sub, pages, fig=None):
    d = {"text": text, "extra": extra, "tags": [T, sub],
         "source": f"{SRC} p.{pages}", "yield": "high"}
    if fig:
        d["figure"] = {"file": SRC, "page": fig}
    return d

cards = [
    c(r"""You want a Warp kernel to run over \(N\) array elements on an Nvidia GPU. You pass wp.launch the kernel, {{c1::\(\text{dim} = N\)}}, the kernel's arguments in {{c2::\(\text{inputs}\) in parameter order}}, and {{c3::device="cuda"}}.""",
      r"""This is the study guide's practice question 3, answer C. Warp never works out the thread count by itself, and the device argument is optional and defaults to Warp's default device.""",
      "wp_launch", "42"),
    c(r"""The \(\text{dim}\) argument of wp.launch is the number of {{c1::threads}} to start. For a simple map over one array, it equals the array's {{c2::length}}.""",
      r"""The array-add example passes \(\text{dim} = \text{len}(z)\), one thread per element. You never pass a number of GPU cores.""",
      "wp_launch", "42"),
    c(r"""Warp is {{c1::statically}} typed, so every kernel parameter needs a declared type, for example \(\text{wp.array(dtype=float)}\) for an array of floats.""",
      r"""The function also needs the @wp.kernel decorator. The array-add kernel declares x, y and z this way.""",
      "wp_kernel", "36,38", fig=38),
    c(r"""A Warp kernel does not {{c1::return}} a value. It writes its results into an {{c2::output array}} that is passed in as one of its arguments.""",
      r"""The array-add kernel takes x, y and the output array z, and stores each sum in z.""",
      "wp_kernel", "36"),
    c(r"""You write the body of a Warp kernel for a {{c1::single element}}. Warp then launches one {{c2::thread}} per element.""",
      r"""Conceptually the kernel applies to the whole stream. Syntactically it describes the work for one element.""",
      "wp_kernel", "35"),
    c(r"""Inside a Warp kernel, each thread calls {{c1::wp.tid()}} to get its unique thread index, the same role the rank has for an MPI process.""",
      r"""The array-add kernel uses it as \(z[\text{tid}] = x[\text{tid}] + y[\text{tid}]\), so each thread adds one pair of elements.""",
      "wp_tid", "37,38"),
    c(r"""A kernel thread may read any element of the input arrays. Its output may not depend on {{c1::another thread's output}}.""",
      r"""This independence lets the GPU run what looks like a serial kernel on data-parallel hardware.""",
      "kernel_independence", "14"),
    c(r"""Pthreads and MPI are {{c1::homogeneous}} computing, because every execution unit is a compatible CPU core. GPGPU is {{c2::heterogeneous}} computing, because a CPU host and a GPU device run different parts of the program.""",
      r"""The host program loads the data, sends it to the GPU, runs the kernels there, and copies the result back. Mixing Intel and ARM CPUs in one MPI job fails because the code is compiled for one architecture.""",
      "heterogeneous_computing", "26,27"),
    c(r"""Kernels access GPU memory directly, as threads do in shared-memory programming. GPGPU also borrows from {{c1::distributed-memory}} programming, because the CPU and the GPU usually have {{c2::separate memory spaces}}.""",
      r"""Direct access on the GPU means data races are still possible. The separate memory spaces mean every input must be copied to the GPU first.""",
      "host_device_copy", "28"),
    c(r"""Moving data to the GPU is a copy over the bus. On a small problem that copy can be the {{c1::dominant}} cost, so a naive GPU port can run {{c2::slower}} than the original CPU code.""",
      r"""The GPU only pays off when there is enough work per element to cover the copies. Keep host and device transfers to a minimum.""",
      "host_device_copy", "28"),
    c(r"""With device="cpu", Warp runs the kernel as a {{c1::single-thread serial}} program. With device="cuda", it runs the kernel in {{c2::parallel}} on an Nvidia GPU.""",
      r"""The code and its semantics are identical on both devices. On the course Docker container you use device="cpu", so you learn GPGPU but get no speedup.""",
      "warp_devices", "31"),
    c(r"""In Warp you write both the CPU code and the kernel in {{c1::Python}}. At runtime Warp converts them just-in-time to {{c2::C++ and CUDA}} code and compiles it.""",
      r"""In plain CUDA or OpenCL, the CPU code is in C and the kernel is in a separate kernel language. Warp also manages the data transfer between CPU and GPU.""",
      "warp_overview", "32,33"),
    c(r"""The CPU side of a Warp program converts host data such as a NumPy array with {{c1::wp.array}}, allocates the output with {{c2::wp.zeros}}, launches the kernel, and copies the result back with {{c3::.numpy()}}.""",
      r"""The output array must have the same length as the inputs. The slides declare the NumPy arrays as \(\text{np.float32}\) because 32-bit floats are what the GPU uses.""",
      "warp_host_steps", "34,39-43"),
    c(r"""Lecture 15 maps each data-parallel model to hardware. Multi-core CPUs run {{c1::multiple independent threads}}, x86 SSE vector units run {{c2::one thread with a wide data path}}, and GPUs run {{c3::multiple lockstep threads}}.""",
      r"""The middle model is SIMD and the GPU model is SIMT.""",
      "simd_vs_simt", "19,20", fig=20),
    c(r"""SIMD uses {{c1::one thread}} with one register file of very wide registers. SIMT uses multiple lockstep threads that share {{c2::one program counter}} but each have their own {{c3::register file}}.""",
      r"""Both split identical, independent work over execution lanes and save repeated fetch and decode. GPUs work on the SIMT model.""",
      "simd_vs_simt", "17,18,21"),
    c(r"""Threads in a lockstep group take different branches. The group runs {{c1::both paths}} and masks off the inactive lanes, so the divergent code costs the {{c2::sum}} of both branches.""",
      r"""Anything that breaks the uniformity of the threads costs performance.""",
      "gpu_data_design", "25"),
    c(r"""A GPU performs best when you load {{c1::one flat data buffer}} and every thread runs the same kernel with {{c2::uniform}} work.""",
      r"""GPUs are built for lockstep threads working on pre-loaded data. Branchy or non-contiguous data breaks that pattern.""",
      "gpu_data_design", "25"),
    c(r"""In the stream programming model, a stream is an ordered set of data of the {{c1::same type}}. A {{c2::kernel}} is a small function that operates on entire streams.""",
      r"""Streams usually hold thousands of elements or more. Only one kernel can be applied to a stream at a time, so several kernels run in sequence.""",
      "stream_model", "11,12,15"),
    c(r"""The most common kernel is a {{c1::map}}, which evaluates one function on each element of the input stream.""",
      r"""Other kernel operations are expansions with several outputs per input, reductions that combine many elements into one, and filters that output a subset.""",
      "stream_model", "12,13"),
]

out = r"C:\github\CIS3090-M2\anki_work\v4\cards\b04.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
print(len(cards))
