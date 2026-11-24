import json

T = "b03_mpi"
L9 = "03c_lecture_09_mpi_intro.pdf"
CH = "03_ch03_mpi.pdf"
A2 = "A2_mpi.txt"


def M(name):
    return r"\(\mathrm{" + name.replace("_", r"\_") + r"}\)"


def c(n, ans):
    return "{{c%d::%s}}" % (n, ans)


def card(sub, src, text, extra=""):
    d = {"text": text, "tags": [T, sub], "source": src, "yield": "high"}
    if extra:
        d["extra"] = extra
    return d


cards = [
    # Receiving from any source, status, count
    card("status_any_source", CH + " p.10",
         "A manager receives with " + M("MPI_ANY_SOURCE") + " as the source. After the call, it reads "
         + c(1, M("status.MPI_SOURCE")) + " to learn which rank sent the message, and "
         + c(2, M("status.MPI_TAG")) + " to learn its tag.",
         "MPI does not overwrite the source argument you passed in. The sender's rank is only in the "
         + M("MPI_Status") + " struct, which has at least the members " + M("MPI_SOURCE") + ", "
         + M("MPI_TAG") + " and " + M("MPI_ERROR") + "."),
    card("status_any_source", CH + " p.10",
         "The count you pass to " + M("MPI_Recv") + " is only the buffer capacity. To get the number of "
         "elements that arrived, the receiver calls " + c(1, M("MPI_Get_count")) + " with the status and "
         "the receive datatype.",
         "The count is not a member of the status struct because it depends on the datatype. It is the "
         "bytes received divided by the bytes per element, so MPI computes it only when you ask."),
    card("status_any_source", L9 + " p.33",
         M("MPI_Send") + " and " + M("MPI_Recv") + " return " + c(1, "an error code") + ", which is "
         + c(2, M("MPI_SUCCESS")) + " on success. They do not return the number of elements received.",
         "This is the trap in study guide practice question 2. The element count comes from "
         + M("MPI_Get_count") + "."),
    card("status_any_source", CH + " p.9",
         "Workers finish in an unpredictable order. If rank 0 receives in rank order, it "
         + c(1, "blocks on a slow worker") + " while finished results wait. With "
         + c(2, M("MPI_ANY_SOURCE")) + " it takes results in the order the workers finish.",
         "A2 uses this for its work queue. The manager receives each request with "
         + M("MPI_ANY_SOURCE") + " and then reads the sender from the status."),

    # Matching
    card("message_matching", CH + " p.8",
         "Process q sends and process r receives. The receive matches only if both use the same "
         + c(1, "communicator") + " and the same " + c(2, "tag") + ", the send's dest is r, and the "
         "receive's source is " + c(3, "q") + ".",
         "The study guide says communicator, source and tag must all agree. If any one differs, the "
         "receive never completes."),
    card("message_matching", CH + " p.8",
         "Once the communicator, tag and ranks match, the receive succeeds if the receive type equals the "
         "send type and the receive buffer size is " + c(1, "at least") + " the send size.",
         "The greetings program sends 31 chars into a 100 char buffer, which is fine."),
    card("message_matching", CH + " p.7",
         "A message sent on one communicator " + c(1, "cannot be received") + " on a different "
         "communicator. Passing separate communicators to two libraries keeps their messages apart.",
         "Pacheco gives an atmosphere library and an ocean library their own communicators. Splitting "
         "the tag range between them would also work, but it is harder to manage."),
    card("message_matching", CH + " p.9",
         "Only the " + c(1, "receiver") + " can use a wildcard such as " + M("MPI_ANY_TAG")
         + ". The sender always names a rank and a tag, so MPI uses a " + c(2, "push")
         + " mechanism. There is no wildcard for the " + c(3, "communicator") + ".",
         "The two receive wildcards are " + M("MPI_ANY_SOURCE") + " and " + M("MPI_ANY_TAG") + "."),

    # Tags
    card("tags", CH + " p.7",
         "A tag is a " + c(1, "nonnegative int") + " that tells apart messages that are otherwise "
         "identical, for example floats to print versus floats to use in a computation.",
         "Process 1 can send the floats to print with tag 0 and the floats for the computation with "
         "tag 1."),
    card("tags", A2 + " p.3",
         "In A2 the tag gives the message's purpose and the buffer carries the payload. The manager "
         "answers each worker request with " + c(1, M("TAG_WORK")) + " and a ciphertext, or with "
         + c(2, M("TAG_STOP")) + " once the batch is empty.",
         "Workers send " + M("TAG_REQUEST") + " with a count, then one " + M("TAG_RESULT")
         + " message per valid decryption."),

    # Ordering
    card("message_ordering", CH + " p.11",
         "Messages from one sender to one receiver are " + c(1, "non-overtaking") + ", so they arrive in "
         "the order they were sent. Messages from different senders have " + c(2, "no guaranteed order")
         + ".",
         "MPI cannot control network speed. If q runs on Mars and t runs on the same machine as r, q's "
         "earlier message may still arrive after t's."),

    # Send and receive semantics
    card("send_recv_semantics", CH + " p.10",
         M("MPI_Send") + " may " + c(1, "buffer") + " the message and return, or " + c(2, "block")
         + " until it can start transmitting. Which one happens depends on the MPI implementation.",
         "Typical implementations buffer messages smaller than a cutoff size and block on larger ones."),
    card("send_recv_semantics", CH + " p.10",
         "When " + M("MPI_Send") + " returns, you only know that the " + c(1, "send buffer can be reused")
         + ". You do not know whether the message was transmitted.",
         "A buffered send returns as soon as MPI has copied the data and envelope into its own storage."),
    card("blocking_pitfalls", CH + " p.11",
         M("MPI_Recv") + " " + c(1, "always blocks") + " until a matching message arrives. So a receive "
         "with no matching send makes the process " + c(2, "hang") + " forever.",
         "Lecture 9 says the number of sends and receives must be equal for this reason."),
    card("blocking_pitfalls", CH + " p.11",
         "If the tag or rank in a receive doesn't match the intended send, the receiver may hang, or it "
         "may " + c(1, "match the wrong send") + ".",
         "Pacheco calls the wrong match perhaps worse than a hang."),
    card("blocking_pitfalls", CH + " p.11",
         "A send with no matching receive makes the sender " + c(1, "hang") + " if " + M("MPI_Send")
         + " blocks. If the send was buffered, the message is " + c(2, "lost") + "."),

    # I/O
    card("mpi_io", CH + " p.18",
         "Most MPI implementations let only " + c(1, "rank 0") + " of " + M("MPI_COMM_WORLD")
         + " read stdin. That rank reads the input and " + c(2, "sends it to the other ranks") + ".",
         "If several processes could read stdin, there would be no rule for which one gets which part of "
         "the input. A2 applies the same rule to input files."),
    card("mpi_io", CH + " p.16",
         "Every rank may print to stdout, but the order of the lines is " + c(1, "nondeterministic")
         + ", and one rank's output can " + c(2, "interrupt") + " another's.",
         "The processes compete for stdout and MPI does not schedule access to it, so the order changes "
         "from run to run."),
    card("mpi_io", CH + " p.18",
         "To print in rank order, the other ranks " + c(1, "send their output to rank 0")
         + ", and rank 0 prints it in rank order. The greetings program does this."),

    # Setup
    card("init_size_rank", CH + " p.4",
         c(1, M("MPI_Init")) + " sets up MPI and creates " + M("MPI_COMM_WORLD")
         + ". No MPI call should come before it, and none after " + c(2, M("MPI_Finalize")) + ".",
         M("MPI_Finalize") + " frees the resources MPI allocated."),
    card("init_size_rank", CH + " p.5",
         "You start 4 processes. Each one calls " + M("MPI_Comm_size") + " and gets " + c(1, "4")
         + ". Each one calls " + M("MPI_Comm_rank") + " and gets its own rank, from " + c(2, "0 to 3")
         + ".",
         "The rank plays the role of a process ID, but MPI keeps it system independent."),
    card("init_size_rank", CH + " p.5",
         "MPI programs are SPMD. You compile " + c(1, "one program") + ", and each process "
         + c(2, "branches on its rank") + " to do different work.",
         "SPMD means single program, multiple data. Write the program to run with any number of "
         "processes, because you rarely know the core count in advance."),
    card("init_size_rank", L9 + " p.25",
         "You compile an MPI program with " + c(1, "mpicc") + ", a wrapper script around the C compiler. "
         "You start 4 processes with " + c(2, "mpiexec -n 4") + "."),

    # MPI vs Pthreads, distributed memory
    card("distributed_memory", L9 + " p.8",
         "Pthreads assumes " + c(1, "shared memory") + " and works with threads. MPI assumes "
         + c(2, "distributed memory") + " and works with " + c(3, "processes") + ".",
         "MPI processes share nothing, so every piece of data a process needs must be sent to it "
         "explicitly."),
    card("distributed_memory", L9 + " p.5",
         "A distributed memory system only makes sense when the machines spend more time "
         + c(1, "computing") + " than " + c(2, "communicating") + ".",
         "Sending data over the network takes much longer than sharing data between threads, so long "
         "data-parallel computations fit best."),

    # Trapezoid partition
    card("trapezoid_partition", CH + " p.14",
         r"In the parallel trapezoidal rule with \(h = (b-a)/n\), each rank gets "
         r"\(\mathrm{local\_n} = {{c1::n / \mathrm{comm\_sz} }}\) trapezoids. Its interval starts at "
         r"\(\mathrm{local\_a} = {{c2::a + \mathrm{my\_rank} \cdot \mathrm{local\_n} \cdot h}}\).",
         r"This assumes \(\mathrm{comm\_sz}\) divides \(n\) evenly. Each rank other than 0 then sends "
         r"its local integral to rank 0, which adds them up."),
]

with open(r"C:\github\CIS3090-M2\anki_work\v4\cards\b03a.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
print(len(cards))
