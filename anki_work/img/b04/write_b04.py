import json
from pathlib import Path

cards = [
    {
        "text": (
            r"Speedup: \({{c1::S(n,p) = \frac{T_{\mathrm{serial} }(n)}{T_{\mathrm{parallel} }(n,p)} }}\). "
            r"Efficiency: \({{c2::E(n,p) = S(n,p)/p }}\). "
            r"Linear speedup means \(S = {{c3::p}}\) (so \(E = 1\))."
        ),
        "extra": r"Study-guide / §3.6.3. In practice \(S\) is usually below \(p\) and \(E\) below 1.",
        "tags": ["b04_mpi_performance", "speedup_efficiency"],
        "source": "04_ch03_mpi_performance.pdf p.7",
        "yield": "high",
    },
    {
        "text": (
            r"For parallel MPI timings use {{c1::wall clock::CPU or wall clock?}} time (function MPI Wtime), "
            r"not CPU time, because wall clock includes {{c2::idle / wait::what CPU time omits}} time "
            r"(e.g. blocked in MPI Recv)."
        ),
        "extra": "C clock excludes idle; idle can dominate parallel run-time, so speedup would be wrong without it.",
        "tags": ["b04_mpi_performance", "wall_clock_vs_cpu"],
        "source": "04_ch03_mpi_performance.pdf p.3",
        "yield": "high",
    },
    {
        "text": (
            r"To report one parallel elapsed time: call {{c1::MPI Barrier::collective sync}} so processes start together, "
            r"time with MPI Wtime, then {{c2::MPI Reduce::collective}} with {{c3::MPI MAX::op}} on each local elapsed time "
            r"(time of the slowest process)."
        ),
        "extra": "Ideal parallel time is until the last process finishes; Barrier only approximates a simultaneous start.",
        "tags": ["b04_mpi_performance", "mpi_timing_idiom"],
        "source": "04_ch03_mpi_performance.pdf p.4",
        "yield": "high",
    },
    {
        "text": (
            r"Across repeated identical MPI runs, report the {{c1::minimum::min/mean/median?}} run-time, "
            r"because OS interaction almost never makes the program {{c2::faster::faster or slower?}} than on a quiet system."
        ),
        "extra": "Mean/median mix in noise that only slows you; min approximates the quiet-system time.",
        "tags": ["b04_mpi_performance", "report_minimum"],
        "source": "04_ch03_mpi_performance.pdf p.4",
        "yield": "high",
    },
    {
        "text": (
            r"Usual parallel model: \({{c1::T_{\mathrm{parallel} }(n,p) = T_{\mathrm{serial} }(n)/p + T_{\mathrm{overhead} } }}\). "
            r"In MPI, overhead is typically {{c2::communication}} (e.g. Allgather in mat-vec)."
        ),
        "extra": r"Local work falls by about \(p\); communication can depend on both \(n\) and \(p\).",
        "tags": ["b04_mpi_performance", "parallel_overhead_model"],
        "source": "04_ch03_mpi_performance.pdf p.5",
        "yield": "high",
    },
    {
        "text": (
            r"In mat-vec MPI timings, for {{c1::small n and large p::regime}} communication overhead dominates, "
            r"so adding processes gives little or no speedup; for small p and large n, "
            r"{{c2::serial work divided by p::which term?}} dominates (near-linear speedup)."
        ),
        "extra": (
            r"Work-dominant term: \(T_{\mathrm{serial} }/p\). Overhead term: Allgather. "
            r"Example: n=1024, p=8 to 16 run-time unchanged; worst S=2.4 at n=1024, p=16."
        ),
        "tags": ["b04_mpi_performance", "overhead_dominates"],
        "source": "04_ch03_mpi_performance.pdf p.7",
        "yield": "high",
    },
    {
        "text": (
            r"Practice: \(T_{\mathrm{serial} }=100\) s, \(T_4=40\) s, \(T_8=25\) s. "
            r"Speedups are {{c1::2.5 then 4::S at 4 then 8}}; "
            r"efficiencies are {{c2::0.625 then 0.5::E at 4 then 8}} "
            r"(E {{c3::drops::rises or drops?}})."
        ),
        "extra": (
            r"\(S_4=100/40=2.5\), \(E_4=2.5/4=0.625\); \(S_8=100/25=4\), \(E_8=4/8=0.5\). "
            r"Study-guide practice Q5 answer A."
        ),
        "tags": ["b04_mpi_performance", "speedup_efficiency_practice"],
        "source": "08_m2_study_guide.pdf p.5",
        "yield": "high",
    },
    {
        "text": (
            r"Roughly, a parallel program is {{c1::scalable}} if the {{c2::problem size}} can be increased at a rate "
            r"so that {{c3::efficiency}} does not decrease as the number of processes increases."
        ),
        "extra": "Mat-vec: fixing n and raising p drops E; doubling both n and p (for larger p) usually holds or raises E.",
        "tags": ["b04_mpi_performance", "scalability"],
        "source": "04_ch03_mpi_performance.pdf p.8",
        "yield": "high",
    },
]

out = Path(r"C:\github\CIS3090-M2\anki_work\cards\b04.json")
with out.open("w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
    f.write("\n")

# sanity: Anki should see single backslash
loaded = json.loads(out.read_text(encoding="utf-8"))
assert loaded[0]["text"].startswith("Speedup: \\("), repr(loaded[0]["text"][:30])
print("wrote", len(cards), "cards; sample:", loaded[0]["text"][:60])
