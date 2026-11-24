import json, re

cs = json.load(open(r"C:\github\CIS3090-M2\anki_work\v4\cards\b03b.json", encoding="utf-8"))
bad = ["additionally", "crucial", "delve", "enhance", "foster", "landscape", "pivotal",
       "showcase", "testament", "underscore", "vibrant", "serves as", "utilize", "leverage"]
for i, c in enumerate(cs):
    for f in ("text", "extra"):
        s = c[f]
        nomath = re.sub(r"\\\(.*?\\\)", "M", s)
        nocloze = re.sub(r"\{\{c\d::", "", nomath)
        probs = []
        if re.search(r"\{\{c\d::(?:(?!\}\}).)*::", s):
            probs.append("hint")
        if re.search("[\u2013\u2014]| - ", s):
            probs.append("dash")
        if ";" in nomath:
            probs.append("semicolon")
        if ":" in nocloze:
            probs.append("colon")
        if "(" in nomath or ")" in nomath:
            probs.append("paren")
        if any(b in s.lower() for b in bad):
            probs.append("vocab")
        if probs:
            print(i, f, probs, nocloze[:100])
print("checked", len(cs))
