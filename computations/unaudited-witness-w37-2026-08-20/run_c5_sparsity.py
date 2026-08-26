"""W37 / C5 -- IS THE SURVIVING-EQUATION COUNT THE WITNESS INVARIANT?

For every live pair of every X_3 object this lane holds at N=8, record
nEq = the number of words on U whose cap-error polynomial in the nine cap
unknowns is not identically zero, against the exact verdict.  W27-S3
observed that the N=8 witness set is constant across weight points and
called the responsible invariant 'unidentified'; nEq is a candidate,
being a function of which monomials survive.
"""
import json, os, re, sys, glob, time
from collections import Counter
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w37_core as C
OUT = os.path.join(HERE, "results_c5_sparsity.json")
rows = []
seen = set(); files = []
for f in sorted(glob.glob(os.path.join(HERE, "OBJECT_W37_X3witness_*.json"))):
    m = re.search(r"X3witness_(\d+)_(\d+)_", f)
    if (m.group(1), m.group(2)) in seen: continue
    seen.add((m.group(1), m.group(2))); files.append(f)
t0 = time.time()
for f in files:
    d = json.load(open(f)); s = C.parse_source(d["blocks"], 8)
    wp = {tuple(x) for x in d["witness_pairs"]}
    for p, q in combinations(range(8), 2):
        if not C.is_live(s, p, q): continue
        U = tuple(x for x in range(8) if x not in (p, q))
        polys, _ = C.sym_cap_system(s, p, q, U)
        rows.append({"obj": os.path.basename(f), "pair": [p, q],
                     "nEq": len(polys),
                     "verdict": "WITNESS" if (p, q) in wp else "BLOCKED"})
    print(f"  {os.path.basename(f)} done ({round(time.time()-t0,1)}s)", flush=True)
    C.ckpt(OUT, {"rows": rows})
f8 = C.parse_source(json.load(open(os.path.join(HERE, "..",
      "unaudited-x3core-w25-2026-08-15",
      "OBJECT_W25-F8_n8_allblocked_X3.json")))["blocks"], 8)
for p, q in combinations(range(8), 2):
    if not C.is_live(f8, p, q): continue
    U = tuple(x for x in range(8) if x not in (p, q))
    polys, _ = C.sym_cap_system(f8, p, q, U)
    rows.append({"obj": "W25-F8", "pair": [p, q], "nEq": len(polys),
                 "verdict": "BLOCKED"})
w = [r["nEq"] for r in rows if r["verdict"] == "WITNESS"]
b = [r["nEq"] for r in rows if r["verdict"] == "BLOCKED"]
summ = {"n_objects": len(set(r["obj"] for r in rows)), "n_pairs": len(rows),
        "witness_nEq": sorted(Counter(w).items()),
        "blocked_nEq_low": sorted((k, v) for k, v in Counter(b).items() if k <= 10),
        "max_witness_nEq": max(w) if w else None,
        "max_blocked_nEq": max(b),
        "blocked_at_or_below_max_witness": sum(1 for n in b if n <= (max(w) if w else -1)),
        "n_blocked": len(b), "n_witness": len(w),
        "seconds": round(time.time() - t0, 1)}
C.ckpt(OUT, {"rows": rows, "summary": summ})
print(json.dumps(summ))
