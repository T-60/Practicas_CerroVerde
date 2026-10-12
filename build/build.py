import json, re, sys, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
S = sys.argv[1] if len(sys.argv) > 1 else ROOT
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "index.html")
B = os.path.join(S, "banco")
ALLOWED = r"(?:/?(?:b|i|br|p|table|thead|tbody|tr|th|td|code|sub|sup|u|em|strong|span)\b[^<>]*>)"
def san(s):
    if not isinstance(s, str) or s.lstrip().lower().startswith("<svg"): return s
    return re.sub(r"<(?!" + ALLOWED + ")", "&lt;", s)
bank = {}
probs = []
for name in ["verbal_ingles", "numerico_logico", "espacial", "excel_competencias", "parentesco"]:
    p = os.path.join(B, name + ".json")
    if not os.path.exists(p): probs.append("missing " + name); continue
    bank[name] = json.load(open(p))
def chk(items):
    for q in items:
        q["prompt"] = san(q.get("prompt", "")); q["explanation"] = san(q.get("explanation", ""))
        q["options"] = [san(o) for o in q["options"]]
        if not (0 <= q["answer"] < len(q["options"])): probs.append(q["id"] + " bad answer")
        if q["area"] not in ["verbal","numerico","logico","espacial","ingles","excel"]: probs.append(q["id"] + " area " + q["area"])
for k in ["verbal_ingles", "numerico_logico", "espacial", "parentesco"]:
    if k in bank: chk(bank[k])
ec = bank.get("excel_competencias")
if ec:
    chk(ec["excel"])
    for s in ec["sjt"]:
        if s["best"] == s["worst"] or not (0 <= s["best"] < len(s["options"])) or not (0 <= s["worst"] < len(s["options"])): probs.append(s["id"] + " sjt idx")
    from collections import Counter
    c = Counter(p["pair"] for p in ec["personalidad"])
    bad = [k for k, v in c.items() if v != 2]
    if bad: probs.append("pairs " + str(bad))
ids = [q["id"] for k in ["verbal_ingles","numerico_logico","espacial","parentesco"] if k in bank for q in bank[k]] + ([q["id"] for q in ec["excel"]] if ec else [])
if len(ids) != len(set(ids)): probs.append("duplicate ids")
data = json.dumps(bank, ensure_ascii=False).replace("</", "<\\/")
tpl = open(os.path.join(S, "build", "template.html")).read()
open(OUT, "w").write(tpl.replace("/*__BANK__*/null", data))
print("problems:", probs or "none"); print({k: (len(v) if isinstance(v, list) else {kk: len(vv) for kk, vv in v.items()}) for k, v in bank.items()})
print("size KB", os.path.getsize(OUT) // 1024)
