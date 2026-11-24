import json

T = "b07_m2_compare"
P3 = "07_m2_study_guide.pdf p.3"
P4 = "07_m2_study_guide.pdf p.4"
P34 = "07_m2_study_guide.pdf p.3-4"


def card(text, extra, sub, src):
    return {"text": text, "extra": extra, "tags": [T, sub], "source": src, "yield": "high"}


cards = [
    # Memory and communication model
    card(
        r"In Pthreads, every thread works in one {{c1::shared address space}}. The threads synchronize with {{c2::mutexes}}, condition variables and atomics.",
        r"Any thread can read or write any shared variable, so shared data needs a lock or an atomic update.",
        "memory_model", P3),
    card(
        r"MPI runs {{c1::separate processes}} that share no memory. The processes exchange data only by {{c2::message passing}}, either point-to-point or with collectives.",
        r"Lecture 9 says the data each process works on must be explicitly sent to it.",
        "memory_model", P3),
    card(
        r"Warp keeps {{c1::host and device}} memory separate. Your data is {{c2::copied to the device}} first, and the kernels then operate on GPU device memory.",
        r"Lecture 9 says CPU code sees main memory and GPU code sees GPU memory, so the two need explicit transfers.",
        "memory_model", P3),
    card(
        r"Of Pthreads, MPI and Warp, the two that need explicit data movement before the work starts are {{c1::MPI}} and {{c1::Warp}}.",
        r"MPI sends the data as messages and Warp copies it from host to device. Pthreads threads read shared memory directly.",
        "memory_model", P3),
    # Execution targets
    card(
        r"Pthreads runs {{c1::threads}} on a single {{c2::shared-memory}} machine.",
        r"Lecture 9 calls Pthreads a low-level, OS-specific API that assumes shared memory.",
        "execution_target", P3),
    card(
        r"MPI runs {{c1::processes}} across {{c2::one or more}} nodes.",
        r"Lecture 9 says the processes can run on different machines, on the same machine, or both, and the MPI code is the same either way.",
        "execution_target", P3),
    card(
        r"Warp targets a heterogeneous system with a CPU host and an {{c1::NVIDIA GPU}} device. Without a GPU, Warp can still run the kernel on the {{c2::CPU}} as a fallback.",
        r'The fallback is device="cpu", which runs serially for portability. device="cuda" runs in parallel on the NVIDIA GPU.',
        "execution_target", P3),
    # Built-in facilities
    card(
        r"The built-in Pthreads call that makes each thread wait until all the threads reach the same point is {{c1::\(\mathrm{pthread\_barrier\_wait}\)}}.",
        r"The study guide lists the barrier as the main built-in Pthreads facility for parallel work.",
        "built_ins", P4),
    card(
        r"Pthreads has {{c1::no collectives}}. To combine values from all the threads, you write the {{c2::reduction}} yourself.",
        r"Lecture 9 says Pthreads was designed for concurrency rather than parallel computation, so you do everything by hand.",
        "built_ins", P4),
    card(
        r"Of Pthreads, MPI and Warp, only {{c1::MPI}} has a rich set of built-in collectives such as Bcast, Reduce, Allreduce and Gather.",
        r"Lecture 9 says MPI was designed with parallel computation in mind, and Pthreads was not.",
        "built_ins", P4),
    card(
        r"Warp's built-in facility is a {{c1::kernel launch}} over {{c2::N elements}}.",
        r"Each thread calls wp.tid() to get the index of the element it works on.",
        "built_ins", P4),
    # Best-fit workloads
    card(
        r"Pthreads is the best fit for {{c1::fine-grained}} updates to {{c2::shared state}}, as long as you synchronize them carefully.",
        r"Threads see the same memory, so small frequent updates need no messages or copies.",
        "best_fit", P4),
    card(
        r"MPI is the best fit when the work splits into {{c1::large independent chunks}} with only {{c2::modest communication}} between steps.",
        r"Lecture 9 says machines on a network must spend more time computing than communicating, or the speedup is small.",
        "best_fit", P4),
    card(
        r"Warp is the best fit for large {{c1::data-parallel maps}} where every element gets {{c2::uniform}} work.",
        r"Every GPU thread runs the same kernel on its own element, so uneven work leaves threads idle.",
        "best_fit", P4),
    card(
        r"A Warp job is only worth it when each element has {{c1::enough work}} to pay for the {{c2::copies}} between host and device.",
        r"The copy to the GPU and back is a fixed cost that the compute time must outweigh.",
        "best_fit", P4),
    # Common pitfalls
    card(
        r"The common Pthreads pitfalls are {{c1::data races}}, deadlocks and {{c2::oversubscription}}.",
        r"Oversubscription means you start more threads than the machine has cores, so the threads take turns on the same cores.",
        "pitfalls", P4),
    card(
        r"The common MPI pitfalls are mismatched {{c1::tags or ranks}}, deadlocks and {{c2::frequent small messages}} between machines.",
        r"A receive with the wrong tag or rank never matches its send and can hang. Every message between machines costs network time.",
        "pitfalls", P4),
    card(
        r"The common Warp pitfalls are excessive {{c1::host-device copies}}, {{c2::non-contiguous}} data, and problems too {{c3::small}} to pay for the copies.",
        r"Lecture 7 says a flat contiguous array moves to the GPU in one block, and scattered data does not.",
        "pitfalls", P4),
    card(
        r"The study guide lists {{c1::deadlock}} as a pitfall for both Pthreads and MPI, but not for Warp.",
        r"Pthreads threads deadlock on locks. MPI processes deadlock when a blocking send or receive never finds its partner.",
        "pitfalls", P4),
    card(
        r"The study guide lists data races as a pitfall for {{c1::Pthreads}} only.",
        r"Pthreads threads share one address space, so two threads can write the same variable at once. MPI processes share no memory.",
        "pitfalls", P34),
]

with open(r"C:\github\CIS3090-M2\anki_work\v4\cards\b07.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
print(len(cards))
