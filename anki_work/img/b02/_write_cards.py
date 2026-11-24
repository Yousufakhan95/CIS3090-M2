import json
from collections import Counter
from pathlib import Path

cards = [
 {
  "text": r"Speedup of a parallel program is \(S = {{c1::T_{\mathrm{serial} }/T_{\mathrm{parallel} } }}\).",
  "extra": r"Ideal case with equal work and no overhead is linear speedup \(S = p\).",
  "tags": ["b02_performance_amdahl", "speedup"],
  "source": "02_ch02_performance_amdahl.pdf p.2",
  "yield": "high",
 },
 {
  "text": r"Linear speedup means a parallel run on \(p\) cores achieves \(S = {{c1::p}}\).",
  "extra": r"Best possible: work split evenly and no parallel overhead.",
  "tags": ["b02_performance_amdahl", "linear_speedup"],
  "source": "02_ch02_performance_amdahl.pdf p.2",
  "yield": "high",
 },
 {
  "text": r"Efficiency is \(E = {{c1::S/p}} = {{c2::T_{\mathrm{serial} }/(p \cdot T_{\mathrm{parallel} }) }}\).",
  "extra": r"Interpreted as average fraction of parallel run-time each core spends on the original problem.",
  "tags": ["b02_performance_amdahl", "efficiency"],
  "source": "02_ch02_performance_amdahl.pdf p.2",
  "yield": "high",
 },
 {
  "text": r"As \(p\) grows, parallel overhead usually {{c1::increases::grows or shrinks?}}, so efficiency \(E = S/p\) usually {{c2::decreases}}.",
  "extra": r"Typical overheads: critical sections/mutexes, network messages, thread management, file I/O. These make \(S\) a smaller fraction of ideal \(p\).",
  "tags": ["b02_performance_amdahl", "overhead_vs_p"],
  "source": "02_ch02_performance_amdahl.pdf p.2",
  "yield": "high",
 },
 {
  "text": r"Amdahl's law with serial fraction \(a\): \(S = {{c1::1/((1 - a)/p + a) }}\).",
  "extra": r"Assumes the parallelizable fraction \(1 - a\) speeds up perfectly by \(p\). Textbook uses \(r\) for the same serial fraction.",
  "tags": ["b02_performance_amdahl", "amdahl_formula"],
  "source": "02_ch02_performance_amdahl.pdf p.5",
  "yield": "high",
 },
 {
  "text": r"Under Amdahl's law, as \(p \to \infty\) the speedup approaches \(S \to {{c1::1/a}}\) (serial fraction \(a\)).",
  "extra": r"Extra cores cannot shrink the serial remainder. Equivalent textbook form: if fraction \(r\) stays serial, \(S \le 1/r\).",
  "tags": ["b02_performance_amdahl", "amdahl_limit"],
  "source": "02_ch02_performance_amdahl.pdf p.5",
  "yield": "high",
 },
 {
  "text": r"If 90% of a program is perfectly parallelized (serial fraction \(a = 0.1\)), Amdahl's law bounds speedup by \(S \le {{c1::10}}\).",
  "extra": r"Limit is \(1/a = 10\), even with thousands of cores.",
  "tags": ["b02_performance_amdahl", "amdahl_example"],
  "source": "02_ch02_performance_amdahl.pdf p.5",
  "yield": "high",
 },
 {
  "text": r"Practice: \(T_{\mathrm{serial} } = 100\) s and \(T_{\mathrm{parallel} } = 40\) s on \(p = 4\). Then \(S = {{c1::2.5}}\) and \(E = {{c2::0.625}}\).",
  "extra": r"\(S = 100/40 = 2.5\), \(E = 2.5/4 = 0.625\). Study-guide practice Q5 at 4 cores.",
  "tags": ["b02_performance_amdahl", "speedup_efficiency_calc"],
  "source": "02_ch02_performance_amdahl.pdf p.2",
  "yield": "high",
 },
 {
  "text": r"Practice: \(T_{\mathrm{serial} } = 100\) s and \(T_{\mathrm{parallel} } = 25\) s on \(p = 8\). Then \(S = {{c1::4}}\) and \(E = {{c2::0.5}}\).",
  "extra": r"Versus 4 cores (\(S = 2.5\), \(E = 0.625\)): speedup rose but efficiency fell — classic overhead-with-\(p\) pattern. Study-guide Q5.",
  "tags": ["b02_performance_amdahl", "speedup_efficiency_calc"],
  "source": "02_ch02_performance_amdahl.pdf p.2",
  "yield": "high",
 },
 {
  "text": r"With even work split plus overhead, \(T_{\mathrm{parallel} } = {{c1::T_{\mathrm{serial} }/p + T_{\mathrm{overhead} } }}\).",
  "extra": r"Then \(E\) is the fraction of parallel run-time spent on the original problem; the rest is overhead.",
  "tags": ["b02_performance_amdahl", "t_parallel_overhead"],
  "source": "02_ch02_performance_amdahl.pdf p.3",
  "yield": "high",
 },
]

out = Path(r"C:\github\CIS3090-M2\anki_work\cards\b02.json")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=1)
    f.write("\n")

print(len(cards), dict(Counter(c["yield"] for c in cards)))
print(dict(Counter(c["tags"][1] for c in cards)))
