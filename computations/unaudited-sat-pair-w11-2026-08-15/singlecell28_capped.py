"""UNAUDITED (W11).  Control 1b: enumerate ALL m=28 single-cell admissible
zero-singleton templates.

In the single-cell regime each edge carries one cell, so a perfect matching M
determines the word it supports outright (each vertex lies on exactly one edge
of M).  Hence every matching supports exactly one word, the fibre of w is
{M : w_M = w}, and

    zero singletons  <=>  no matching generates a MIXED word all by itself.

That collapses the 6558 word constraints to 105 constraints over the 105
matchings, giving a tiny CNF.  Verdicts are re-checked with krenn_core.audit.
"""
import json, time
from pysat.formula import IDPool
from pysat.solvers import Cadical195
import krenn_core as K

pool = IDPool(); cls = []
def x(e, c): return pool.id(("x", e, c[0], c[1]))
def add(c): cls.append(c)

for e in range(K.NE):
    cs = [x(e, c) for c in K.CELLS]
    add(cs)                                   # exactly one cell per edge
    for a in range(9):
        for b in range(a+1, 9):
            add([-cs[a], -cs[b]])

# colour of vertex v under matching M
def col(M, v, k):
    for ei in M:
        u, w = K.EDGES[ei]
        if v in (u, w):
            return [x(ei, c) for c in K.CELLS if (c[0] if v == u else c[1]) == k]
    raise AssertionError

def cvar(mi, v, k): return pool.id(("c", mi, v, k))
for mi, M in enumerate(K.MATCHINGS):
    for v in range(8):
        for k in range(3):
            lits = col(M, v, k)
            add([-cvar(mi, v, k)] + lits)     # c -> some cell giving colour k
            for l in lits:
                add([-l, cvar(mi, v, k)])     # and conversely

# (SC): some incident edge pj whose cell carries colour r at j
for p in range(8):
    for r in range(3):
        dis = []
        for (ei, j) in K.INCIDENT[p]:
            g = pool.id(("g", p, r, ei)); dis.append(g)
            same, other = K.far_cells(p, j, r)
            for c in other: add([-g, -x(ei, c)])
            add([-g] + [x(ei, c) for c in same])
        add(dis)

# constant word c has nonempty fibre: some M generates it
def kk(c, mi): return pool.id(("k", c, mi))
for c in range(3):
    dis = []
    for mi, M in enumerate(K.MATCHINGS):
        dis.append(kk(c, mi))
        for ei in M: add([-kk(c, mi), x(ei, (c, c))])
    add(dis)

# zero singletons: every matching's word is constant, or shared with another
def eq(a, b): return pool.id(("eq", min(a,b), max(a,b)))
def con(mi):  return pool.id(("con", mi))
for mi in range(K.NM):
    add([-con(mi)] + [])                      # placeholder, refined below
cls.pop()
for mi in range(K.NM):
    # con[mi] -> all eight vertices share a colour: use 3 colour options
    opts = []
    for k in range(3):
        o = pool.id(("cst", mi, k)); opts.append(o)
        for v in range(8): add([-o, cvar(mi, v, k)])
    add([-con(mi)] + opts)
for a in range(K.NM):
    for b in range(K.NM):
        if a == b: continue
        for v in range(8):
            for k in range(3):
                add([-eq(a, b), -cvar(a, v, k), cvar(b, v, k)])
for mi in range(K.NM):
    add([con(mi)] + [eq(mi, mj) for mj in range(K.NM) if mj != mi])

print("CNF: %d vars %d clauses" % (pool.top, len(cls)), flush=True)
s = Cadical195(bootstrap_with=cls); found = []
t0 = time.time()
import sys
while s.solve():
    if len(found)>=60 or time.time()-t0>600: print("CAP/BUDGET reached"); break
    pos = set(l for l in s.get_model() if l > 0)
    T = K.template_from_sets([{c for c in K.CELLS if x(e, c) in pos}
                              for e in range(K.NE)])
    a = K.audit(T)
    assert a["admissible"] and a["zero_singleton"] and a["support"] == 28 \
        and all(len(S) == 1 for S in T), a
    found.append((T, a))
    blk = []
    for e in range(K.NE):
        for c in K.CELLS:
            v = x(e, c); blk.append(-v if c in T[e] else v)
    s.add_clause(blk)
s.delete()
print("m=28 single-cell admissible zero-singleton templates: %d  (%.1fs)"
      % (len(found), time.time() - t0))
print("Sigma values:", sorted(set(a["sigma"] for _T, a in found)))
json.dump([K.template_to_json(T) for T, _a in found],
          open("results/control1b_m28_singlecell.json", "w"))
