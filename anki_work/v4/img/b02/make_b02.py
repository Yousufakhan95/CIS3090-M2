import json

L14 = "01c_lecture_14_performance.pdf"
TB = "02_ch02_performance_amdahl.pdf"
T = "b02_performance"

def card(text, extra, sub, source, figure=None):
    c = {"text": text, "extra": extra, "tags": [T, sub], "source": source, "yield": "high"}
    if figure:
        c["figure"] = figure
    return c

cards = [
    card(
        r"You time the serial program and the parallel program on the same input. Speedup is \(S = {{c1::\frac{T_{\text{serial} } }{T_{\text{parallel} } } }}\).",
        r"A speedup of 4 means the parallel version finishes in a quarter of the serial time.",
        "speedup", f"{L14} p.26",
    ),
    card(
        r"Linear speedup is the best case. With \(p\) cores, \(S = {{c1::p}}\), so \(T_{\text{parallel} } = {{c2::T_{\text{serial} }/p}}\).",
        r"Lecture 14 says linear speedup does not normally happen, because real programs pay overheads that grow with \(p\).",
        "linear_speedup", f"{L14} p.27",
    ),
    card(
        r"Efficiency is the speedup you get per core, \(E = {{c1::\frac{S}{p} }} = {{c2::\frac{T_{\text{serial} } }{p \cdot T_{\text{parallel} } } }}\).",
        r"Linear speedup gives \(E = 1\). Lecture 14 writes the first fraction as \(S/P\) with a capital P, but P and \(p\) are both the core count.",
        "efficiency", f"{L14} p.35",
    ),
    card(
        r"Lecture 14 defines efficiency as the fraction of parallel run-time each core spends {{c1::on the actual problem}}. That fraction is the core's {{c2::utilization}}.",
        r"The rest of the run-time is parallel overhead. With \(T_{\text{serial} } = 24\) ms, \(p = 8\) and \(T_{\text{parallel} } = 4\) ms, \(E = 3/4\), so each core spends 3 ms on the problem and 1 ms on overhead.",
        "efficiency", f"{L14} p.35",
    ),
    card(
        r"A program takes 100 s on 1 core, 40 s on 4 cores and 25 s on 8 cores. Speedup grows from {{c1::2.5}} to {{c1::4}}, and efficiency drops from {{c2::0.625}} to {{c2::0.5}}.",
        r"\(S = 100/40 = 2.5\) and \(E = 2.5/4\). \(S = 100/25 = 4\) and \(E = 4/8\). This is study guide practice question 5.",
        "speedup_efficiency_calc", f"{L14} p.36",
    ),
    card(
        r"Add more cores to the same problem and speedup {{c1::rises}}, but efficiency {{c2::falls}}, because the overheads {{c3::grow with the number of threads or processes}}.",
        r"In the Lecture 14 table, \(S\) goes 1, 1.9, 3.6, 6.5, 10.8 for \(p = 1, 2, 4, 8, 16\), while \(E\) goes 1, 0.95, 0.9, 0.81, 0.675.",
        "efficiency", f"{L14} p.36",
    ),
    card(
        r"Lecture 14 lists the overheads that slow a parallel program. For threads, they are managing the threads, {{c1::critical sections}}, and calls to {{c2::mutex functions}}.",
        r"A mutex makes the threads run the critical section one at a time. A serial program has none of these costs.",
        "overheads", f"{L14} p.29",
    ),
    card(
        r"Lecture 14 also counts {{c1::network I/O}} in distributed systems and {{c2::file I/O}} as overheads that slow a parallel program.",
        r"Network transfers are much slower than local memory access, and more processes usually means more data sent over the network.",
        "overheads", f"{L14} p.29",
    ),
    card(
        r"Lecture 14 writes parallel run-time as \(T_{\text{parallel} } = {{c1::\frac{T_{\text{serial} } }{p} }} + {{c2::T_{\text{overhead} } }}\).",
        r"The first term is the ideal time with the work split evenly. The second is the added time to manage the parallel operations.",
        "overhead_model", f"{L14} p.37",
    ),
    card(
        r"Keep \(p\) fixed and make the problem bigger. The overhead grows {{c1::more slowly}} than \(T_{\text{serial} }\), so speedup and efficiency both {{c2::increase}}.",
        r"In textbook Table 2.5 at \(p = 16\), efficiency is 0.39 for half size, 0.68 for the original size and 0.89 for double size.",
        "problem_size", f"{TB} p.4",
        {"file": TB, "page": 4},
    ),
    card(
        r"Amdahl's law says that unless {{c1::virtually all}} of a serial program is parallelized, the speedup is very limited {{c2::regardless of the number of cores}}.",
        r"The inherently serial part runs at the same speed on any number of cores, so the parallel run-time can never drop below the time of the serial part.",
        "amdahl_law", f"{L14} p.40",
    ),
    card(
        r"Lecture 14 writes Amdahl's law as \[S = \frac{1}{ {{c1::\frac{\text{parallelizable portion} }{\text{perfect speedup} } }} + {{c2::\text{inherently serial portion} }} }\]",
        r"The two portions add up to 1, and the perfect speedup of the parallelizable part is \(p\).",
        "amdahl_law", f"{L14} p.44",
    ),
    card(
        r"With serial fraction \(a\) on \(p\) cores, Amdahl's law gives \(S = {{c1::\frac{1}{(1-a)/p + a} }}\).",
        r"This is the study guide's form. \(1-a\) is the parallelizable portion. The textbook calls the serial fraction \(r\) instead of \(a\).",
        "amdahl_law", f"{L14} p.46",
    ),
    card(
        r"As \(p\) keeps growing, the Amdahl speedup approaches {{c1::\(1/a\)}}, where \(a\) is the {{c2::inherently serial}} fraction of the work.",
        r"The \((1-a)/p\) term goes to 0, so only \(a\) is left in the denominator. Past some point, extra cores add almost nothing.",
        "amdahl_limit", f"{L14} p.46",
    ),
    card(
        r"A program that is 90% parallelizable can never get a speedup above {{c1::10}}, even on 1000 cores. At 95% the cap is {{c2::20}}, and at 99% it is {{c3::100}}.",
        r"The cap is \(1/a\), so \(1/0.1 = 10\), \(1/0.05 = 20\) and \(1/0.01 = 100\). A program that is 50% parallelizable caps at 2.",
        "amdahl_limit", f"{L14} p.47",
        {"file": L14, "page": 47},
    ),
    card(
        r"A program takes 20 s serially, and 90% of it parallelizes perfectly. On \(p\) cores it takes \(T_{\text{parallel} } = {{c1::18/p + 2}}\) seconds, so it never runs faster than {{c2::2}} seconds.",
        r"The parallel part is \(0.9 \times 20 / p\) and the serial part is \(0.1 \times 20\). The 2-second serial part gives the cap \(S \le 20/2 = 10\).",
        "amdahl_example", f"{L14} p.42",
    ),
    card(
        r"With serial fraction 0.1 on 8 cores, Amdahl's law gives \(S = 1/(0.9/8 + 0.1) \approx {{c1::4.7}}\), so efficiency is only about {{c2::0.59}}.",
        r"The same program gets \(S \approx 1.82\) on 2 cores and 6.4 on 16 cores, with efficiency 0.91 and 0.40.",
        "amdahl_example", f"{L14} p.45",
    ),
    card(
        r"Lecture 14 says Amdahl's law rules out {{c1::super-linear}} speedup, at least as a result of parallelization. With an inherently serial portion of 0, the law gives \(S = {{c2::p}}\).",
        r"This follows from the formula. \((1-a)/p + a\) is never smaller than \(1/p\), so \(S\) never exceeds \(p\).",
        "amdahl_law", f"{L14} p.48",
    ),
    card(
        r"Time the inherently serial part over several trial runs and Amdahl's law gives the {{c1::maximum speedup}}. That tells you how many {{c2::execution units}} your program can use before extra ones stop adding speedup.",
        r"Lecture 14 uses this for a cost and benefit analysis of what hardware or cloud compute to buy.",
        "amdahl_use", f"{L14} p.49",
    ),
    card(
        r"Amdahl's law ignores {{c1::problem size}}. For many problems the inherently serial fraction {{c2::shrinks}} as the problem grows, which is Gustafson's law.",
        r"The textbook gives this as the first reason not to give up because of Amdahl's law.",
        "amdahl_limitations", f"{TB} p.6",
    ),
]

out = r"C:\github\CIS3090-M2\anki_work\v4\cards\b02.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
print(len(cards), "cards written")
