import json

T = "b01_hardware"
TB = "01_ch02_hardware.pdf"
L7 = "01b_lecture_07_data_layout.pdf"
L14 = "01c_lecture_14_performance.pdf"


def card(text, extra, sub, source, fig=None):
    c = {"text": text, "extra": extra, "tags": [T, sub], "source": source, "yield": "high"}
    if fig:
        c["figure"] = {"file": fig[0], "page": fig[1]}
    return c


cards = [
    # Flynn's taxonomy
    card("Flynn's taxonomy classifies a computer by how many {{c1::instruction streams}} and how many {{c2::data streams}} it can run at the same time.",
         "Crossing single and multiple for each gives the four classes SISD, SIMD, MISD and MIMD.",
         "flynn_taxonomy", f"{L14} p.3"),
    card("A traditional single-core von Neumann computer runs one instruction on one piece of data at a time, so Flynn's taxonomy calls it {{c1::SISD}}.",
         "SISD means single instruction, single data. It is the serial baseline every other class is compared against.",
         "flynn_taxonomy", f"{L14} p.4"),
    card("Very few real systems are {{c1::MISD}}, which would run multiple instructions on a single piece of data.",
         "Lecture 14 lists MISD for completeness and says there aren't many systems of this kind.",
         "flynn_taxonomy", f"{L14} p.11"),
    card("A SIMD system has one {{c1::control unit}} that broadcasts each instruction to many {{c2::ALUs}}, and each ALU applies that instruction to its own data item.",
         "SIMD means single instruction, multiple data. With m ALUs, Lecture 14 says arithmetic can run up to m times faster.",
         "simd", f"{L14} p.5"),
    card("In a classical SIMD system, the ALUs run {{c1::synchronously}} and cannot {{c2::store instructions}}, so each ALU waits for the controller to broadcast the next one.",
         "Lecture 14 says the ALUs are tied to the controller. No ALU can save an instruction and run it later.",
         "simd", f"{L14} p.6"),
    card("SIMD fits {{c1::data parallelism}}, such as a simple loop over a large array, and does poorly on most other kinds of parallel problems.",
         "Data parallelism means you split the data among processors and each one applies the same instructions to its share.",
         "simd", f"{L14} p.6"),
    card("A SIMD loop runs x[i] += y[i] only when y[i] > 0. Every datapath whose y[i] is not positive sits {{c1::idle}} while the others do the addition.",
         "All datapaths must run the same instruction or do nothing, so a branch wastes the datapaths that take the other path.",
         "simd", f"{TB} p.5"),
    card("A vector processor holds operands in {{c1::vector registers}} and applies the same operation to every element at once, so it is a {{c2::SIMD}} system.",
         "The vector length is fixed by the system, usually 4 to 256 elements of 64 bits each. A conventional CPU operates on one scalar at a time.",
         "vector_processors", f"{L14} p.7"),
    card("With vector instructions, the loop x[i] += y[i] needs one load, add and store per {{c1::block of vector-length elements}}. A conventional CPU needs one load, add and store per {{c2::element}}.",
         "This is where the vector processor's speed comes from. One instruction covers a whole block of the array.",
         "vector_processors", f"{TB} p.6"),
    card("Lecture 14 lists two benefits of vector processors. The compiler finds loops to vectorize and {{c1::reports why}} a loop can't be vectorized, and {{c2::every data item}} the processor loads is used.",
         "A cache-based system may load a full cache line and use only part of it. Lecture 14 also lists high memory bandwidth and ease of use as benefits.",
         "vector_processors", f"{L14} p.8"),
    card("Lecture 14 gives two drawbacks of vector processors. They handle {{c1::irregular data structures}} poorly, and they are hard to {{c2::scale}} because longer vectors aren't very useful.",
         "Irregular means anything other than arrays. The textbook adds that systems scale by adding more vector processors, not longer vectors.",
         "vector_processors", f"{L14} p.8"),
    card("A GPU core uses SIMD datapaths, but a GPU also runs many independent instruction streams on its cores. So a GPU is {{c1::neither purely SIMD nor purely MIMD}}.",
         "The textbook says current GPUs can run more than one instruction stream per core and have dozens of cores.",
         "gpu_classification", f"{TB} p.7"),
    # MIMD and memory
    card("A MIMD system has independent cores, each with its own {{c1::control unit and ALU}}. The cores run {{c2::asynchronously}}, each at its own pace.",
         "Without synchronization that the programmer adds, two cores running the same code may be on different statements at any instant.",
         "mimd", f"{L14} p.9"),
    card("In a shared-memory MIMD system, cores communicate {{c1::implicitly}} through shared data structures. In a distributed-memory system, each processor has private memory and communicates {{c2::explicitly}} by sending messages over a network.",
         "Lecture 14 draws shared memory as CPUs on one bus to one memory, and distributed memory as CPU and memory pairs on a network.",
         "mimd", f"{TB} p.8", fig=(L14, 10)),
    card("In a {{c1::UMA}} system, every core takes the same time to reach every memory location. This makes it {{c2::easier to program}}.",
         "UMA means uniform memory access. The programmer does not have to think about where data lives.",
         "uma_numa", f"{L14} p.14"),
    card("In a NUMA system, a core reaches memory attached to {{c1::its own chip}} faster than memory attached to another chip. NUMA systems can also hold {{c2::more memory}} than UMA systems.",
         "NUMA means nonuniform memory access. Each chip has its own block of memory, and other chips reach it through special hardware.",
         "uma_numa", f"{L14} p.18", fig=(L14, 18)),
    card("A cluster is a collection of commodity computers on a commodity network such as Ethernet. Its nodes are usually shared-memory systems, so a cluster is also called a {{c1::hybrid}} system.",
         "Hybrid means the system mixes shared memory inside each node with distributed memory between nodes.",
         "clusters_grids", f"{L14} p.19"),
    card("A grid joins clusters spread over a large geographic area. Its nodes are often {{c1::heterogeneous}}, meaning they use different hardware and operating systems.",
         "The textbook says a grid turns geographically distributed computers into one distributed-memory system.",
         "clusters_grids", f"{L14} p.19"),
    # Interconnects
    card("On a bus, all connected devices share the same {{c1::communication wires}}. As you add processors, they {{c2::wait longer}} to access memory, so bus performance drops.",
         "A bus has low cost and flexibility. Lecture 14 calls the bus the most common interconnect, but the textbook says buses are being replaced by switched interconnects as systems grow.",
         "interconnects", f"{L14} p.20"),
    card("In a crossbar, switches choose among multiple data paths. Two CPUs conflict only when they access the {{c1::same memory module}}. A crossbar is faster than a bus, but it is {{c2::more expensive}}.",
         "The slide shows CPU 1 on Memory 4, CPU 2 on Memory 3, CPU 3 on Memory 1 and CPU 4 on Memory 2, all at the same time. The switches and links are what cost more.",
         "interconnects", f"{L14} p.24", fig=(L14, 23)),
    # Locality and caching
    card("A program that accesses one memory location will likely access a nearby location soon. The nearby part is {{c1::spatial}} locality, and the soon part is {{c2::temporal}} locality.",
         "Caches rely on both. A loop over an array is the textbook's example of spatial locality.",
         "locality", f"{TB} p.2"),
    card("Memory moves into the cache in blocks called {{c1::cache lines}}. If a line holds 16 floats, reading z[0] also brings in z[1] through z[15], so the next 15 reads {{c2::hit the cache}}.",
         "The first read may stall the processor while the line comes from memory. The textbook says a line usually holds 8 to 16 times one memory location.",
         "locality", f"{TB} p.2"),
    card("Adjacent elements of an array are adjacent in memory, but adjacent elements of a {{c1::linked list}} can be far apart. So a loop over a flat array gets spatial locality for free.",
         "Following pointers from node to node jumps around memory, so each cache line brings in less useful data.",
         "data_layout", f"{L7} p.1"),
    card("Value types such as structs are easier to cache than {{c1::reference types}}, such as pointers to structs or structs made of pointers.",
         "A struct's fields sit next to each other in memory. A pointer sends the CPU to a different address.",
         "data_layout", f"{L7} p.1"),
    card("Contiguous data is easy to transfer, because you move {{c1::N bytes starting from address M}} in one block.",
         "This is why one flat array can go out as a single MPI message or a single copy to the GPU.",
         "data_layout", f"{L7} p.2"),
    card("Parallel code stores a 2D array as a {{c1::1D array}} with index arithmetic, and it represents a complex object as {{c2::several 1D arrays}}.",
         "Lecture 7 gives a 3D model as the example. A game engine stores it as a vertex buffer, an index buffer and a texture buffer, each one a flat array.",
         "data_layout", f"{L7} p.2"),
    card("Shared-memory programs rarely transfer data, but they still need {{c1::cache locality}}. Distributed-memory and CPU/GPU programs must move {{c2::large blocks of data}}, so they use simple flat structures.",
         "Lecture 7 says performance is the reason to write parallel code at all, so transfer overhead has to stay small.",
         "data_layout", f"{L7} p.5"),
    card("Lecture 7's tips for contiguous memory are to use {{c1::structs}} instead of objects, put no {{c2::pointers}} in structs, and use {{c3::contiguous arrays}} instead of linked data.",
         "All three keep the data in one block, which is easy to cache and easy to transfer.",
         "data_layout", f"{L7} p.6"),
]

with open(r"C:\github\CIS3090-M2\anki_work\v4\cards\b01.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
print(len(cards))
