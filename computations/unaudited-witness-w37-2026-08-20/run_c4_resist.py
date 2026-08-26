"""W37 / C4 -- WHICH X_4 EQUATIONS RESIST AT F8 (fast exact rank version).

For each site z, RREF the X_3 site system ONCE, then for every off-count-4
word u reduce its single row against that RREF: the augmented system is
inconsistent exactly when the reduction leaves 0 = (nonzero).  A word that
is inconsistent at EVERY site is LOCALLY UNREMOVABLE at F8 -- the precise
sense in which an X_4 equation resists.
"""
import json, os, sys, time
from collections import Counter
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w37_core as C
from run_c1_builder import rref, site_rows, words_upto

OUT = os.path.join(HERE, "results_c4_resist.json")
src = C.parse_source(json.load(open(os.path.join(HERE, "..",
      "unaudited-x3core-w25-2026-08-15",
      "OBJECT_W25-F8_n8_allblocked_X3.json")))["blocks"], 8)
N = 8; W3 = words_upto(3)
t0 = time.time()
base = {}
for z in range(N):
    rows, rhs, idx, nc = site_rows(src, z, W3)
    red, piv = rref([r + [b] for r, b in zip(rows, rhs)], nc)
    base[z] = (red, piv, idx, nc)
    print(f"  site {z}: rank {len(piv)} (built {round(time.time()-t0,1)}s)", flush=True)

def row_for(z, u):
    red, piv, idx, nc = base[z]
    row = [Fraction(0)] * (nc + 1)
    for y in range(N):
        if y == z: continue
        rest = tuple(t for t in range(N) if t not in (z, y))
        hv = C.haf_word(src, u, rest)
        if hv != 0: row[idx[(y, u[z], u[y])]] += hv
    return row

def consistent_with(z, u):
    red, piv, idx, nc = base[z]
    row = row_for(z, u)
    for i, c in enumerate(piv):
        if row[c] != 0:
            f = row[c]
            row = [a - f * b for a, b in zip(row, red[i])]
    return not (all(row[c] == 0 for c in range(nc)) and row[nc] != 0)

# CONTROL (ledger 28): a word already satisfied by F8 must be consistent
_, bad = C.defects(src, 8)
ctrl_ok = [u for u in C.all_words(8) if C.offcount(u) == 4 and u not in bad][:5]
assert all(consistent_with(z, u) for u in ctrl_ok for z in range(N)), \
    "CONTROL FAILED: an already-satisfied word reads inconsistent"
print(f"  control: 5 already-satisfied off-4 words consistent at all 8 sites")

off4 = [u for u in C.all_words(8) if C.offcount(u) == 4]
rem, stuck = Counter(), Counter()
stuck_words, rem_sites = [], Counter()
for n, u in enumerate(off4):
    hit = None
    for z in range(N):
        if consistent_with(z, u):
            hit = z; break
    if hit is None:
        stuck[C.profile(u)] += 1; stuck_words.append(list(u))
    else:
        rem[C.profile(u)] += 1; rem_sites[hit] += 1
    if n % 400 == 0:
        print(f"   {n}/{len(off4)}  stuck {sum(stuck.values())}", flush=True)
res = {"n_off4": len(off4), "removable": {str(k): v for k, v in rem.items()},
       "stuck": {str(k): v for k, v in stuck.items()},
       "n_removable": sum(rem.values()), "n_stuck": sum(stuck.values()),
       "violated_now": len([w for w in bad if C.offcount(w) == 4]),
       "violated_and_stuck": len([w for w in bad if list(w) in stuck_words]),
       "first_site_hit": dict(rem_sites), "stuck_sample": stuck_words[:60],
       "seconds": round(time.time() - t0, 1)}
C.ckpt(OUT, res)
print(json.dumps({k: v for k, v in res.items() if k != "stuck_sample"})[:900])
