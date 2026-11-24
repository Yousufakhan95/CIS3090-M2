# CIS*3090 Midterm 2: predicted questions

---

Blueprints written by the card writers before they wrote the cards. Each answer is a full-mark answer.

---

# b01 Parallel hardware and data layout (cram)

Scope: Textbook Ch 2 (2.2.1 caching basics, 2.3.1 to 2.3.4 up to shared-memory interconnects), Lecture 7 slides 11-16 (data layout), Lecture 14 Part 1 (PDF pages 1-24). Expected share of the exam: about 4 to 6 of 27 questions. The study guide names Flynn's taxonomy, vector processors (how they work, benefits, drawbacks), locality, and moving data in one contiguous block.

## Lecture 14 Part 1: parallel systems architectures

1. [high] Classify a system with Flynn's taxonomy: a single-core von Neumann machine, a vector processor, a multicore CPU or cluster. (evidence: rung 1, study guide "Flynn's taxonomy - SISD, SIMD, MISD, MIMD"; L14 p.3-11)
   Full-mark answer: Flynn counts simultaneous instruction streams and data streams. Serial von Neumann is SISD. Vector processor is SIMD. Multicore and clusters are MIMD. MISD has almost no real systems.
2. [high] Select all that apply: benefits and drawbacks of vector processors. (evidence: rung 1, study guide "how they work, and their benefits and drawbacks"; L14 p.8)
   Full-mark answer: benefits are fast and easy to use, compilers find vectorizable loops and explain failures, high memory bandwidth, every loaded item is used. Drawbacks are poor handling of irregular data structures and poor scaling because longer vectors are not useful.
3. [high] How does a vector processor work? (evidence: rung 1; L14 p.7, textbook p.32-33)
   Full-mark answer: vector registers of fixed length, 4 to 256 elements of 64 bits. Same operation on every element, so it is SIMD. One load, add and store per block of elements instead of per element.
4. [high] Which statement about SIMD is true? (evidence: rung 5, L14 p.5-6; textbook p.31-32)
   Full-mark answer: one control unit broadcasts to many ALUs. Classical ALUs are synchronous and store no instructions. Good for data parallelism over large arrays, weak elsewhere. A branch leaves some datapaths idle.
5. [high] Which statement about MIMD is true? (evidence: L14 p.9-10)
   Full-mark answer: independent cores with their own control unit and ALU, asynchronous, shared memory with implicit communication or distributed memory with explicit messages.
6. [high] UMA vs NUMA. (evidence: L14 p.12-18, four slides of build-up)
   Full-mark answer: UMA has equal access time for all cores and is easier to program. NUMA gives faster access to memory attached to the core's own chip, slower access to another chip, and supports more memory.
7. [high] Bus vs crossbar. (evidence: L14 p.20-24)
   Full-mark answer: bus wires are shared, cheap and flexible, contention grows with processor count. Crossbar switches select among multiple paths, processors run simultaneously, conflict only on the same memory module, faster but more expensive.
8. [high] Cluster, hybrid system, grid. (evidence: L14 p.19)
   Full-mark answer: a cluster is commodity machines on a commodity network. Nodes are shared-memory, so it is a hybrid system. A grid spans clusters over a wide geographic area and is often heterogeneous.

## Lecture 7 data layout and textbook caching

1. [high] Why is a flat contiguous array faster than a linked list? (evidence: rung 1, study guide "Locality: contiguous arrays vs pointer-chasing"; L7 p.1)
   Full-mark answer: adjacent array elements are adjacent in memory, so a loop gets spatial locality. Linked-list nodes can be far apart. One cache line brings in several neighbours at once.
2. [high] Why do parallel programs use contiguous data for transfers? (evidence: rung 1, study guide "one large contiguous block can be moved in one piece, as an MPI message or a copy to the GPU"; L7 p.2, p.5)
   Full-mark answer: you move N bytes from address M in one block. Distributed-memory and CPU/GPU programs must move large blocks, so they use flat, low-level structures with index arithmetic.
3. [high] Lecture 7's tips for contiguous memory. (evidence: rung 4, L7 p.6 TL;DR slide)
   Full-mark answer: structs instead of objects, no pointers in structs, contiguous arrays instead of linked data.
4. [high] Spatial vs temporal locality and cache lines. (evidence: textbook p.21-22)
   Full-mark answer: spatial means a nearby location next, temporal means soon. Memory moves to cache in lines, for example 16 floats, so the next 15 reads of the array hit.
5. [high] How is a 2D array or 3D model stored in parallel code? (evidence: L7 p.2-4)
   Full-mark answer: a 2D array is a 1D array with index arithmetic. A complex object, such as a 3D model, is several 1D buffers.
6. [high] Shared memory vs distributed or heterogeneous programs: what does data layout buy each? (evidence: L7 p.5)
   Full-mark answer: shared memory transfers little but still needs cache locality. Distributed and CPU/GPU programs need efficient large block transfers.

---

## Lecture 14 Part 2 and Textbook 2.6.1-2.6.2: speedup, efficiency, overhead, Amdahl's law

1. [high] Given run times on 1, 4 and 8 cores, compute speedup and efficiency and say which way each moves. (evidence: rung 2, study guide practice question 5, answer A; rung 1, study guide lists "speedup, linear speedup, efficiency" as formula items)
   Full-mark answer: $S = T_{serial}/T_{parallel}$, so $100/40 = 2.5$ and $100/25 = 4$. $E = S/p$, so $2.5/4 = 0.625$ and $4/8 = 0.5$. Speedup rises while efficiency falls.

2. [high] Given a serial fraction $a$ and $p$ cores, compute the Amdahl speedup, or the maximum speedup as $p$ grows. (evidence: rung 1, study guide "Amdahl's law and its limit 1/a"; rung 3, L14 p.41-46 worked example)
   Full-mark answer: $S = \dfrac{1}{(1-a)/p + a}$. As $p \to \infty$, $S \to 1/a$. 90% parallelizable caps at 10, 95% at 20, 99% at 100, 50% at 2. With $a = 0.1$ and $p = 8$, $S \approx 4.7$ and $E \approx 0.59$.

3. [high] What is linear speedup, and why do real programs fall short of it? (evidence: rung 1, study guide; L14 p.27-29)
   Full-mark answer: linear speedup is $S = p$, so $T_{parallel} = T_{serial}/p$ and $E = 1$. Real programs pay overheads that grow with $p$.

4. [high] Select all that apply: which of these are overheads that slow a parallel program and grow with $p$? (evidence: rung 1, study guide lists them verbatim; L14 p.29)
   Full-mark answer: managing threads, critical sections, mutex functions, network I/O in distributed systems, file I/O.

5. [high] As $p$ increases on a fixed problem, what happens to $S$ and $E$? (evidence: L14 p.30-36 table with "Increases" and "Decreased" arrows; study guide "why efficiency usually drops as p grows")
   Full-mark answer: $S$ increases, $E$ decreases. Each added core adds less speedup than the one before.

6. [high] What does Amdahl's law tell you, and what does it rule out? (evidence: L14 p.40, p.48; textbook p.65)
   Full-mark answer: unless virtually all of the program is parallelized, speedup is very limited regardless of core count. Super-linear speedup won't come from parallelization. With serial portion 0, $S = p$.

7. [high] With $T_{parallel} = T_{serial}/p + T_{overhead}$, what happens to $S$ and $E$ when the problem size grows at fixed $p$? (evidence: L14 p.37-39; textbook Table 2.5, Fig 2.18-2.19)
   Full-mark answer: overhead grows more slowly than $T_{serial}$, so speedup and efficiency both increase.

8. [high] What does efficiency measure? (evidence: L14 p.35-36; textbook p.62-63)
   Full-mark answer: the fraction of parallel run-time each core spends on the actual problem, its utilization. The rest is parallel overhead. Example: $T_{serial} = 24$ ms, $p = 8$, $T_{parallel} = 4$ ms gives $E = 3/4$, 3 ms on the problem and 1 ms overhead.

9. [high] How do you use Amdahl's law in practice? (evidence: rung 1, study guide "use it to understand the upper bound of the payoff and choose p sensibly"; L14 p.49)
   Full-mark answer: measure the inherently serial share over trial runs, compute the speedup limit, and pick the number of execution units or hardware to buy with a cost and benefit analysis.

10. [medium, kept as high because it is a likely distractor] Why is Amdahl's law less discouraging than it looks? (evidence: textbook p.66 only)
    Full-mark answer: it ignores problem size. For many problems the inherently serial fraction shrinks as the problem grows, which is Gustafson's law.

---

## MPI basics: Lecture 9 and Pacheco 3.1-3.3

Scope note: collectives (Bcast, Reduce, Allreduce, Gather, Barrier) are covered by the other MPI writer. Lecture 9 slide 11 mentions them only in passing.

1. [high] A manager calls `MPI_Recv(buf, 256, MPI_CHAR, MPI_ANY_SOURCE, TAG_RESULT, MPI_COMM_WORLD, &status)`. How does it learn the sender and how many characters arrived? (evidence: rung 1-2, study guide practice Q2, A2 section 4.3 reference to Pacheco 3.1; Pacheco p.98-99)
   Full-mark answer: read `status.MPI_SOURCE` for the sender (and `status.MPI_TAG` for the tag). Call `MPI_Get_count(&status, MPI_CHAR, &n)` for the element count. The count is not a status field because it depends on the datatype. `MPI_Recv` returns an error code (`MPI_SUCCESS`), not a count, and it does not overwrite the source argument. The count argument of `MPI_Recv` is only the buffer capacity.

2. [high] When does a send match a receive? (evidence: rung 1, study guide "communicator, source, and tag must all agree"; Pacheco p.97 message matching; Lecture 9 p.28, p.36)
   Full-mark answer: same communicator, same tag, the send's `dest` is the receiver's rank, the receive's `source` is the sender's rank. For success the buffers must be compatible: same type and receive size at least the send size. A message sent on one communicator cannot be received on another.

3. [high] Which statements about wildcards are true? (SAA trap) (evidence: Pacheco p.98)
   Full-mark answer: only receivers can use wildcards (`MPI_ANY_SOURCE`, `MPI_ANY_TAG`). Senders always name a rank and a nonnegative tag, so MPI is "push". There is no wildcard for the communicator. `MPI_ANY_SOURCE` lets rank 0 take results in finishing order instead of blocking on a slow worker.

4. [high] What ordering does MPI guarantee? (evidence: rung 1, study guide "nonovertaking for the same sender, no global order"; Pacheco p.11; Lecture 9 p.35)
   Full-mark answer: messages from one sender to one receiver are non-overtaking. Messages from different senders have no guaranteed arrival order.

5. [high] What can go wrong with blocking send and receive? (evidence: rung 1, study guide blocking pitfalls; Pacheco p.11; Lecture 9 p.36)
   Full-mark answer: `MPI_Recv` always blocks, so a receive with no matching send hangs forever. Mismatched tag or rank: the receiver hangs or matches the wrong send. A blocking send with no receive hangs. A buffered send with no receive loses the message.

6. [high] What does `MPI_Send` do, and what do you know when it returns? (evidence: Pacheco p.10-11; Lecture 9 p.34)
   Full-mark answer: it may buffer and return, or block until transmission can start. Implementation dependent, typically small messages below a cutoff are buffered and large ones block. On return you only know the send buffer can be reused, not that the message was transmitted.

7. [high] Which ranks can use stdin and stdout? (evidence: rung 1, study guide "assume only rank 0 reads stdin. Printing from multiple ranks is not ordered"; A2 "only rank 0 opens input files"; Pacheco p.16-18; Lecture 9 p.37-42)
   Full-mark answer: only rank 0 of `MPI_COMM_WORLD` reads stdin, then sends the values to the other ranks. All ranks may print, but output order is nondeterministic and lines can interleave. To order output, send it to rank 0 and print there in rank order.

8. [high] What do `MPI_Init`, `MPI_Comm_size`, `MPI_Comm_rank`, `MPI_Finalize` do? (evidence: rung 1, study guide "Initialization"; Pacheco p.4-5; Lecture 9 p.14, p.21)
   Full-mark answer: `MPI_Init` sets up MPI and creates `MPI_COMM_WORLD`. No MPI calls before it or after `MPI_Finalize`. `MPI_Comm_size` gives the number of processes $p$, `MPI_Comm_rank` gives this process's rank, $0$ to $p-1$.

9. [high] What is the role of a tag? (evidence: rung 1, study guide "use tags to distinguish message types, as in A2"; A2 section 4.3; Pacheco p.6-7)
   Full-mark answer: a nonnegative int that distinguishes otherwise identical messages. In A2 the tag gives the purpose (`TAG_REQUEST`, `TAG_RESULT`, `TAG_WORK`, `TAG_STOP`) and the buffer carries the payload.

10. [high] MPI vs Pthreads, and when distributed memory pays off. (evidence: rung 1, study guide compare/contrast section; Lecture 9 p.5, p.8, p.9)
    Full-mark answer: Pthreads assumes shared memory and uses threads. MPI assumes distributed memory and uses processes, so all data must be sent explicitly. Distributed memory only pays off when machines compute much longer than they communicate.

11. [high] SPMD and the greetings and trapezoid patterns. (evidence: study guide "classic send/gather pattern from our basic examples"; Pacheco p.5, p.13-15; Lecture 9 p.15, p.23)
    Full-mark answer: one program, each process branches on its rank. Rank 0 receives and prints or sums, other ranks send to rank 0. Trapezoid partition: $h = (b-a)/n$, $\text{local\_n} = n/\text{comm\_sz}$, $\text{local\_a} = a + \text{my\_rank} \cdot \text{local\_n} \cdot h$.

12. [high] How do you compile and run an MPI program? (evidence: Lecture 9 p.25; Pacheco p.3; A2 execution format)
    Full-mark answer: `mpicc` is a wrapper script around the C compiler. `mpiexec -n 4 ./prog` starts 4 processes.

---

## Collective communication in MPI (Lecture 10, Pacheco 3.4.1 to 3.4.8)

1. [high] Which ranks call $\mathrm{MPI\_Bcast}$, $\mathrm{MPI\_Reduce}$ and $\mathrm{MPI\_Allreduce}$, and where does the result end up? (evidence: rung 1, study guide collectives bullet; Lecture 10 p.10, p.13 to p.17)
   Full-mark answer: every process in the communicator calls the collective, rank 0 included. Bcast copies the source's data to every process. Reduce leaves the combined result only on dest_process. Allreduce leaves it on every process and has no dest_process argument.
2. [high] Practice question 1: on a slow network, what is the best design to sum $g(a[i])$ over a large array? (evidence: rung 1, study guide practice Q1, answer D)
   Full-mark answer: each rank computes a local sum over its own block, then one $\mathrm{MPI\_Reduce}$ combines the local sums on rank 0. Per-element messages and an Allreduce after every element send far too many messages. Only rank 0 reads stdin.
3. [high] Select all that apply: how do collectives differ from point-to-point calls? (evidence: rung 5, Pacheco 3.4.3 numbered list)
   Full-mark answer: all processes must call the same collective. Arguments must be compatible, for example the same dest_process. The output buffer is only used on dest_process, but every rank must pass one, even NULL. Collectives use no tags and match by communicator and call order.
4. [high] Table 3.3 trace: ranks call $\mathrm{MPI\_Reduce}$ in different orders on a and c. What are b and d on rank 0? (evidence: rung 3, Pacheco worked example)
   Full-mark answer: matching is by call order, not buffer names, so $b = 1 + 2 + 1 = 4$ and $d = 2 + 1 + 2 = 5$.
5. [high] Why is a tree-structured global sum faster than rank 0 receiving from everyone? (evidence: Lecture 10 p.4, p.11 diagrams; Pacheco 3.4.1)
   Full-mark answer: with 8 processes rank 0 does 3 receives and adds instead of 7, and the pairs in each phase work at the same time. With 1024 processes it is 10 instead of 1023, about $\log_2 p$.
6. [high] Why does MPI provide $\mathrm{MPI\_Reduce}$ instead of letting each programmer write the tree? (evidence: Lecture 10 p.12; Pacheco 3.4.2)
   Full-mark answer: the best pairing depends on the hardware and system, so the MPI implementer, who knows the system, tunes it.
7. [high] Bcast vs Scatter vs Gather: which sends the same data, which splits, which assembles? What do send_count and recv_count mean? (evidence: Lecture 10 p.21 to p.24; Pacheco 3.4.7, 3.4.8)
   Full-mark answer: Bcast sends the same data to all. Scatter sends a different chunk to each process, the source included. Gather assembles one chunk per process on dest_process only. Both counts are per process, not totals.
8. [high] How does Assignment 2 use collectives? (evidence: rung 2, A2 sections 4.2 and 4.4)
   Full-mark answer: $\mathrm{MPI\_Bcast}$ for the word list, $\mathrm{MPI\_Gather}$ for per-rank statistics, $\mathrm{MPI\_Barrier}$ then $\mathrm{MPI\_Reduce}$ with $\mathrm{MPI\_MAX}$ for elapsed time. Every rank, the manager included, must reach each collective or the program may hang.
9. [high] Bcast code reading: where do the Bcast calls go in Get_input, and what does data_p mean on each rank? (evidence: Lecture 10 p.18 to p.20; Pacheco Program 3.6)
   Full-mark answer: only rank 0 reads with scanf inside the `my_rank == 0` test, but every rank calls $\mathrm{MPI\_Bcast}$ outside it. data_p is input on the source and output elsewhere.
10. [medium] Pitfall: is $\mathrm{MPI\_Reduce}$ with the same buffer for input and output legal? (evidence: Pacheco 3.4.3)
   Full-mark answer: no, it aliases an output argument, so the result is unpredictable.

## Reduce in action, the trapezoidal rule (Lecture 11)

1. [high] What two collective calls improve the first MPI trapezoid program, and what does each replace? (evidence: Lecture 11 p.21 to p.24)
   Full-mark answer: $\mathrm{MPI\_Bcast}$ replaces rank 0's loop of sends of a, b, n. $\mathrm{MPI\_Reduce}$ with $\mathrm{MPI\_SUM}$ to rank 0 replaces the linear receive-and-add loop.
2. [high] Trapezoid formulas: $h = (b-a)/n$, one trapezoid has area $\frac{h}{2}(f(x_i) + f(x_{i+1}))$. (evidence: Lecture 11 p.6, p.9)
3. [high] Each rank's share: $\mathrm{local\_n} = n/\mathrm{comm\_sz}$, $\mathrm{local\_a} = a + \mathrm{my\_rank} \cdot \mathrm{local\_n} \cdot h$, $\mathrm{local\_b} = \mathrm{local\_a} + \mathrm{local\_n} \cdot h$. (evidence: Lecture 11 p.17, p.24)
   Full-mark answer also notes the slides assume n divides evenly by comm_sz.
4. [high] Concave function: trapezoid underestimates. Convex: overestimates. (evidence: Lecture 11 p.8, both terms underlined on the slide)

---

## Lecture 15: GPGPU and intro to Warp

Estimated share of Midterm 2: about 3 to 5 of 27 questions, shared with Lecture 18. The study guide's "GPGPU with Warp" section and practice question 3 are the main evidence.

1. [high] A Warp kernel must run over an array of $N$ elements on an Nvidia GPU. What do you pass to `wp.launch`? (evidence: rung 1, study guide practice question 3, answer C; p.42)
   Full-mark answer: the kernel, `dim=N` (one thread per element), the kernel's arguments in `inputs=[...]` in parameter order, and `device="cuda"`. Warp does not pick the thread count or a number of cores on its own. The device is optional and defaults to Warp's default device.
2. [high] Which statements about `@wp.kernel` functions are true? (select all that apply) (evidence: rung 1, study guide "static types, no return"; p.35-38)
   Full-mark answer: Warp is statically typed, so every parameter has a declared type such as `wp.array(dtype=float)`. A kernel returns nothing and writes results into an output array argument. You write the body for one element, and Warp launches one thread per element.
3. [high] What does `wp.tid()` return, and how is it used? (evidence: rung 1, study guide "Indexing"; p.37-38)
   Full-mark answer: the thread's unique index, like a rank in MPI. The array-add kernel computes $z[tid] = x[tid] + y[tid]$.
4. [high] Why can a naive GPU port run slower than the CPU original? (evidence: rung 1, study guide "cost of copying data"; p.28)
   Full-mark answer: the CPU and GPU usually have separate memory spaces, so data must be copied over the bus. On a small problem that copy can be the dominant cost.
5. [high] Why is GPGPU called heterogeneous computing, and Pthreads or MPI homogeneous? (evidence: rung 1, study guide; p.26-27)
   Full-mark answer: Pthreads and MPI run only on compatible CPU cores. GPGPU splits work between a CPU host program and a GPU device with a different architecture. The host loads data, sends it to the GPU, runs kernels, and copies results back.
6. [high] What happens with `device="cpu"` versus `device="cuda"`? (evidence: rung 1, study guide "Devices"; A3 requires `device="cpu"`; p.31)
   Full-mark answer: "cpu" runs the kernel as a single-thread serial program with identical semantics, so there is no speedup on Docker. "cuda" runs it in parallel on an Nvidia GPU.
7. [high] Which data layout and workload suit a GPU, and what does branch divergence cost? (evidence: rung 1, study guide "Design"; p.25)
   Full-mark answer: one flat contiguous buffer with uniform work per thread. When threads in a lockstep group branch differently, the group runs both paths and masks inactive lanes, so the cost is the sum of both branches.
8. [high] Distinguish SIMD from SIMT, and match multi-core CPU, x86 SSE and GPU to their execution models. (evidence: rung 5, four slides p.17-21; links to Flynn's taxonomy in the study guide)
   Full-mark answer: SIMD is one thread with one register file of very wide registers. SIMT is multiple lockstep threads with one program counter and separate register files. Multi-core CPUs run independent threads, SSE is SIMD, GPUs are SIMT.
9. [high] What is a kernel in the stream programming model, and what restriction makes it data parallel? (evidence: rung 5, p.11-15)
   Full-mark answer: a stream is an ordered set of same-type data. A kernel is a small function that operates on entire streams, most often as a map. A thread may read any input element, but its output may not depend on another thread's output.
10. [high] Why does Warp keep everything in Python, and what does it do behind the scenes? (evidence: rung 5, p.32-33)
    Full-mark answer: both CPU and kernel code are Python. Warp converts them just-in-time to C++/CUDA and compiles them at runtime, and it manages data transfer between CPU and GPU.
11. [high] List the CPU-side steps of a Warp program. (evidence: rung 1, study guide "Data prep"; p.34, 40-43)
    Full-mark answer: create the host data such as a NumPy array, convert it with `wp.array(...)`, allocate the output with `wp.zeros(...)`, launch the kernel, convert the output back with `.numpy()`.

---

# b05 Image processing basics and filters (cram)

Scope: Lecture 16, basics of image processing (25 pages), and Lecture 17, sharpening and blurring (39 pages). Expected share of the exam: about 3 to 4 of 27 questions. The study guide's "Image processing basics" section names discrete convolution, normalized smoothing kernels, the four border strategies and what each does to the output's size and border pixels, unsharp masking $f_{UM} = f + kg$, and Gaussian and median filtering. Practice question 4 is a mean filter missing its $\frac{1}{9}$.

## Lecture 16: convolution, kernels and image borders

1. [high] A student's $3 \times 3$ mean filter has every weight 1 instead of $\frac{1}{9}$. What happens on an 8-bit image clipped to 0 to 255? (evidence: rung 1, study guide practice question 4, answer B; L16 p.12)
   Full-mark answer: the kernel sums to 9, so each output pixel is the neighbourhood sum instead of its average. The image comes out about nine times brighter, and most pixels clip at 255.
2. [high] Select all that apply: what each border strategy does to the output's size and border pixels. (evidence: rung 1, study guide "know what each one does to the output's size and its border pixels"; L16 p.22-25)
   Full-mark answer: copy of input pixels keeps the size, and the border is unprocessed input pixels. Truncation of the image removes the pixels it cannot convolve, so the output is smaller and offset. Reflection maps out-of-range coordinates back into the image, as if mirrored, and keeps the size. Reflected indexing is the most useful option, and circular indexing is rarely used. Truncation of the kernel uses a modified kernel at the border and adds considerable complexity.
3. [high] Why is a smoothing kernel normalized? (evidence: rung 1, study guide "sum of all kernel weights = 1 to preserve mean intensity"; L16 p.12)
   Full-mark answer: each coefficient is divided by the sum of the coefficients, so the kernel sums to 1. An area of constant intensity keeps its value, and the sum of pixel values does not change, so filtering adds no bias.
4. [high] Define discrete convolution, or compute one output pixel of a mean filter. (evidence: rung 1, study guide "weighted sum over an n x n neighbourhood"; L16 p.6, p.15-18 worked example)
   Full-mark answer: the output pixel is a weighted sum of the neighbourhood intensities, with weights from the kernel, $g(x,y) = \sum_{i=-1}^{1}\sum_{j=-1}^{1} w(i,j)\,f(x+i,y+j)$. A centred kernel has odd dimensions. In the slide example the nine values sum to 1835, and $\frac{1835}{9} \approx 204$.
5. [high] Which region of an $M \times N$ image can a $k \times k$ kernel process? (evidence: L16 p.19-21)
   Full-mark answer: $3 \times 3$ gives $(M-2) \times (N-2)$ from origin $(1,1)$. $5 \times 5$ gives $(M-4) \times (N-4)$ from $(2,2)$. $7 \times 7$ gives $(M-6) \times (N-6)$ from $(3,3)$.

## Lecture 17: sharpening, unsharp masking and noise suppression

1. [high] Unsharp masking: the edge image, the output formula, and the role of $k$. (evidence: rung 1, study guide "f_UM = f + k*g ... k controls sharpening strength"; L17 p.9-11)
   Full-mark answer: $g = f - S(f)$, where $S(f)$ is a blurred version of $f$. $f_{UM} = f + kg$. Larger $k$ gives more sharpening, with reasonable values from 0.2 to 0.7. With $k > 1$ it is called a high-boost filter.
2. [high] Select all that apply: properties of mean, Gaussian and median filters. (evidence: rung 1, study guide "Gaussian and median filtering"; L17 p.22-38)
   Full-mark answer: the mean filter reduces noise but blurs edges, and a larger kernel or repeated passes blur more. The Gaussian kernel is nonuniform, weights fall with distance, it is isotropic, and a larger $\sigma$ blurs more and needs a larger kernel. The median filter is a non-linear rank filter, removes impulse noise, and preserves sharp edges.
3. [high] Why does a median filter remove impulse noise, and what else does it remove? (evidence: L17 p.35, its longest explanatory slide)
   Full-mark answer: when noisy pixels cover less than half the neighbourhood, the median comes from the clean majority. Any real structure smaller than half the neighbourhood, such as thin lines, is removed too.
4. [high] Why does a median filter preserve edges when a mean filter does not? (evidence: L17 p.23, p.38)
   Full-mark answer: averaging compresses the brightness range in the neighbourhood, and the median does not, so sharp edge boundaries survive.
5. [high] Unsharp masking limitations. (evidence: L17 p.16-18)
   Full-mark answer: noise sensitivity, because UM emphasizes high frequencies, and overshoot, because it makes an edge steeper by making it taller.
6. [high] Properties of a high-pass sharpening kernel. (evidence: L17 p.5-7)
   Full-mark answer: positive centre, negative periphery, coefficients sum to zero. Constant areas give zero output and rapid changes give a large output. Sharpening makes noise more prominent, so denoise first.
7. [high] Gaussian kernel size from $\sigma$. (evidence: L17 p.28-30)
   Full-mark answer: $i, j$ run from $-[3\sigma]$ to $[3\sigma]$ because the weights are negligible beyond $\pm 3\sigma$, so $\sigma = 1$ gives a $7 \times 7$ kernel, which matches the slide's $\sigma^2 = 1$ kernel.
8. [high] Compute the median of a $5 \times 5$ neighbourhood. (evidence: rung 3, L17 p.36 worked example)
   Full-mark answer: sort the 25 values and take the 13th. In the slide example the centre pixel 104 becomes 98.
9. [high] What does a low-pass filter remove? (evidence: L17 p.4)
   Full-mark answer: closely spaced intensity fluctuations, which include noise and wanted fine detail. A high-pass filter is the image minus its low-pass version.

## Not carded (cram)

- 4-neighbours and 8-neighbours (L16 p.8-10), kernel shape names such as pill-box, pyramidal and cone (L16 p.13-14), omnidirectional, uniform and nonuniform definitions (L16 p.11).
- PIL loading and RGB channel handling (L16 p.2-3), which the Warp batch covers through the study guide's image pipeline.
- Causes of blur and noise, the Schreiber history of unsharp masking, the example photographs, and posterization (kept only as an extra on a median card).

---

## Lecture 18, Image processing with Python and Warp

Expected share of Midterm 2: about 3 to 4 of 27 questions, alongside Lecture 15. The study guide names three Lecture 18 items explicitly (constants as typed kernel arguments, the PIL to NumPy to Warp pipeline, image modes and the alpha channel), and A3 is built on this exact pipeline.

1. [high] How do you pass a constant, such as $k$ for unsharp masking or $\sigma$ for a Gaussian, to a Warp kernel? (evidence: rung 1, study guide "constants as typed kernel arguments"; p.13)
   Full-mark answer: pass it as an ordinary kernel argument with a type annotation, for example `factor: float`. Put it in `inputs=` in the same position as in the signature. Warp reads the value at launch, so you can change it without recompiling. Closures are only for values needed at compile time, and the course doesn't need them.

2. [high] What should a filter do with the alpha channel of an RGBA image, and what goes wrong otherwise? (evidence: rung 1, study guide "what to do with the alpha channel"; rung 2, A3 "for RGBA images, leave the alpha channel unchanged"; p.7, p.19)
   Full-mark answer: filter only the colour channels, $k < 3$, and copy alpha (index 3) from the input. If the filter also blurs alpha, nothing fails, and a fully opaque image looks correct, so the bug is invisible. If the kernel skips alpha without copying it, the output from `wp.zeros_like` keeps alpha at 0 and the saved image is fully transparent.

3. [high] Put the steps of the image pipeline in order. (evidence: rung 1, study guide "PIL Image.open -> NumPy (float32) -> Warp arrays -> kernel -> NumPy -> Image.fromarray"; p.3, p.6, p.12, p.16)
   Full-mark answer: `Image.open`, check `image.mode`, `np.asarray(image, dtype=np.float32)`, `wp.array(...)`, `wp.zeros_like(...)` for the output, `wp.launch`, `.numpy()`, `Image.fromarray(...)`, `save`. NumPy is the intermediate format in both directions.

4. [high] Which PIL mode and NumPy shape go together? (evidence: rung 1, study guide "image modes (L, RGB, RGBA)"; rung 2, A3 tests exactly these three modes; p.5, p.7, p.8)
   Full-mark answer: L is greyscale, one 8-bit value per pixel, shape $(h, w)$. RGB has 3 values per pixel, shape $(h, w, 3)$. RGBA has 4, shape $(h, w, 4)$. Pillow's `image.size` is $(w, h)$, but the NumPy shape starts with height.

5. [high] Why add a size-1 channel axis to a greyscale image, and what must be undone before saving? (evidence: rung 2, A3 requires greyscale and colour and the same output mode; p.10, p.11)
   Full-mark answer: $(h, w)$ becomes $(h, w, 1)$, so one 3D kernel indexed by `i, j, k = wp.tid()` handles all three modes. PIL won't build an image from $(h, w, 1)$, so drop the axis with `npOutData[:, :, 0]` before saving a mode L result.

6. [high] Which statements about `wp.launch` are true? Likely select-all-that-apply. (evidence: rung 3, study guide practice Q3 on `wp.launch`; p.14, p.15)
   Full-mark answer: `inputs=` and `outputs=` are joined into the kernel's positional arguments in order. Warp doesn't check which arrays the kernel writes, so `outputs=` is documentation. `dim` is the launch grid, not an array shape. Arrays don't have to share a shape.

7. [high] Why is end-to-end GPU speedup much lower than kernel-only speedup, and which filter gains more from the GPU? (evidence: rung 1, study guide "the cost of copying data to the GPU" and Warp best fit "enough work per element to pay for the copies"; p.22, p.24 to p.26)
   Full-mark answer: `wp.array` copies host memory to device memory and `.numpy()` copies it back. A $3000 \times 4000$ RGB image as float32 is $3000 \times 4000 \times 3 \times 4$ bytes $= 144$ MB each way. Sharpen is about 555x faster in the kernel but only about 37x end-to-end, because 94% of GPU time is data transfer. Median moves the same 144 MB but does more compute per byte, so it reaches about 134x.

8. [high] Why must the output be clipped before converting to `np.uint8`? (evidence: rung 5, explicit "Why np.clip?" slide; p.16)
   Full-mark answer: unsharp masking overshoots above 255 and below 0 at strong edges. `np.uint8` doesn't clamp, so without `np.clip` you see salt-and-pepper noise along edges.

9. [high] Why does the blur kernel run without any synchronization? (evidence: rung 1, compare/contrast Pthreads vs Warp; p.21)
   Full-mark answer: each thread writes exactly one output cell and reads only the input array, so no two threads write the same location.

### Slide error
- p.24 timing table: the header row is shifted one cell to the left. "sharpen" sits over the row labels, so the data columns read "median" and "Gaussian". Pages 25 and 26 quote the first column (555x, 37x) as sharpen and the second (134x) as median. The cards follow pages 25 and 26.

---

## Study guide: Pthreads vs MPI vs Warp

1. [high] Select all that apply: which statements about Pthreads are true? (evidence: rung 1, study guide pp.3-4 comparison section)
   Full-mark answer: one shared address space. Synchronize with mutexes, condition variables, atomics. Runs threads on one shared-memory machine. Has barriers (`pthread_barrier_wait`) but no collectives, so reductions are DIY. Best fit is fine-grained shared-state updates with careful synchronization. Pitfalls are data races, deadlocks, oversubscription.
2. [high] Select all that apply: which statements about MPI are true? (evidence: rung 1, study guide pp.3-4)
   Full-mark answer: separate processes, no shared memory. Communicate by message passing, point-to-point and collectives. Processes run across one or more nodes. Rich collectives (Bcast, Reduce, Allreduce, Gather). Best fit is large independent chunks with modest communication between steps. Pitfalls are mismatched tags or ranks, deadlocks, frequent small messages between machines.
3. [high] Select all that apply: which statements about Warp are true? (evidence: rung 1, study guide pp.3-4)
   Full-mark answer: separate host and device memory. Data is copied to the device and kernels work on GPU device memory. Heterogeneous CPU host plus NVIDIA GPU, with CPU fallback. Built-in facility is a kernel launch over $N$ elements. Best fit is large data-parallel maps with uniform work and enough work per element to pay for the copies. Pitfalls are excessive host-device copies, non-contiguous data, problems too small to pay for the copies.
4. [high] Which approach has built-in collective operations? (evidence: rung 1, p.4 built-in facilities)
   Full-mark answer: only MPI. Pthreads has barriers but you write reductions yourself. Warp's facility is the kernel launch. Lecture 9 slide 8 adds that Pthreads was designed for concurrency, not parallel computation.
5. [high] Which pitfall is shared by Pthreads and MPI but not listed for Warp? (evidence: rung 1, p.4 common pitfalls)
   Full-mark answer: deadlock.
6. [high] A workload is described. Which approach is the best fit? (evidence: rung 1, p.4 best-fit workloads)
   Full-mark answer: fine-grained shared state, Pthreads. Large independent chunks with little communication, MPI. Large uniform data-parallel map with enough work per element, Warp.
7. [high] Which approaches need explicit data movement before work can start? (evidence: rung 1, p.3 memory model, Lecture 9 slides 2 and 9)
   Full-mark answer: MPI (send messages) and Warp (copy host to device). Pthreads threads read shared memory directly.
8. [high] Why does Warp perform badly on a tiny problem or on non-contiguous data? (evidence: rung 1, p.4 pitfalls and best fit)
   Full-mark answer: copy cost between host and device is fixed overhead. A small problem has too little compute to pay for it. Non-contiguous data cannot move in one block.
9. [high] Why are frequent small messages an MPI pitfall? (evidence: rung 1, p.4, Lecture 9 slide 5)
   Full-mark answer: every message between machines costs network time. The machines must spend more time computing than communicating.
