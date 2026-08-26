#!/usr/bin/env python3
"""W21-M1-TENSOR -- INDEPENDENT VERIFICATION of the zero-factoring clean
point at m=28 (seed 3).  UNAUDITED.  Exact only."""
import json, os, random, sys
from fractions import Fraction
from itertools import product, combinations
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); PAR = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, PAR)
import w21_core as K, w21_site as SI

m = 28; T = K.W8_IMMUNE[m]; gam = K.gamma_edges(T); clean = K.clean_words(T)
rng = random.Random(int(os.environ.get("SEED","3")) * 977)
order = list(range(8)); rng.shuffle(order)
bl = SI.descent(gam, clean, rng, order=order, passes=3)
print("descent order used:", order)

# ---------- INDEPENDENT ENGINE: hafnian from the definition, no shared code
EDGES = tuple(combinations(range(8), 2))
def pms(vs):
    if not vs: return [()]
    a, rest = vs[0], vs[1:]
    o = []
    for i, b in enumerate(rest):
        for mm in pms(rest[:i] + rest[i+1:]): o.append(((a, b),) + mm)
    return o
PMS = [tuple(sorted(mm)) for mm in pms(tuple(range(8)))]
G = set(gam)
def Phi(w):
    t = Fraction(0)
    for mm in PMS:
        if all(e in G for e in mm):
            p = Fraction(1)
            for (u, v) in mm: p *= bl[(u, v)][w[u]][w[v]]
            t += p
    return t

n_clean_ok = sum(1 for w in clean if Phi(w) == 0)
allnz = all(bl[e][i][j] != 0 for e in gam for i in range(3) for j in range(3))
print("clean equations satisfied (independent engine): %d / %d" % (n_clean_ok, len(clean)))
print("all 16*9 = 144 Gamma cells nonzero: %s" % allnz)

# ---------- INDEPENDENT factoring test: rank of the 3 x 3deg matrix -------
def rank(M):
    M = [[Fraction(x) for x in r] for r in M]; r = 0; nr = len(M); nc = len(M[0])
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if M[i][c]: piv = i; break
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(nr):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        r += 1
        if r == nr: break
    return r
prof = {}
for t in range(8):
    nb = sorted(s for e in gam for s in e if t in e and s != t)
    V = []
    for c in range(3):
        row = []
        for s in nb:
            e = (min(t, s), max(t, s))
            for d in range(3):
                row.append(bl[e][c][d] if e[0] == t else bl[e][d][c])
        V.append(row)
    prof[t] = rank(V)
print("rank of the 3 x 3deg site matrix per site (1 = FACTORS):", [prof[t] for t in range(8)])
print("sites that factor (independent):", [t for t in range(8) if prof[t] == 1])
print("sites that factor (w21_core):", [t for t in range(8) if K.factors_at(bl, gam, t)])

# ---------- the OTHER 4406 mixed equations and the constants -------------
def H(w):
    t = Fraction(0)
    for mm in PMS:
        ok = True
        for (u, v) in mm:
            if not (T[K.EIDX[(u,v)]] >> (3*w[u]+w[v])) & 1: ok = False; break
        if not ok: continue
        p = Fraction(1)
        for (u, v) in mm:
            e = (u, v)
            p *= bl[e][w[u]][w[v]] if e in bl else Fraction(0)
        t += p
    return t
# the single cells are NOT part of the clean layer; the point only assigns
# Gamma blocks, so H is evaluated with the 12 single cells set to zero.
nonclean = [w for w in K.MIXED if w not in set(clean)]
bad = sum(1 for w in nonclean if H(w) != 0)
print("non-clean mixed words with H != 0 (single cells = 0): %d / %d"
      % (bad, len(nonclean)))
print("constants H:", [str(H((c,)*8)) for c in range(3)])

json.dump({"clean_ok": n_clean_ok, "n_clean": len(clean), "all_nonzero": allnz,
           "site_ranks": prof, "order": order,
           "point": {str(e): [[str(x) for x in r] for r in bl[e]] for e in gam}},
          open(os.path.join(HERE, "results_zero_%s.json" % os.environ.get("SEED","3")), "w"), indent=1)
