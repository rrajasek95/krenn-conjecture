#!/usr/bin/env python3
"""W21-M2-GEO step 8: the per-word EXHAUSTIVE CASE ANALYSIS.

For an L-free word x the 81 permanent equations are exactly
        per == 0 on V_4^x x V_5^x x V_6^x x V_7^x .
Two independent inputs are combined here.

(A)  WHAT THE DEAD CELLS ALLOW.  P^j_{r,x_r} = P^j_{t,x_t} forces the two rows
     to be proportional, hence to have the SAME zero pattern.  Each block has
     at most one dead cell, so the pair is possible iff both rows carry their
     dead cell in the same column (or neither carries one).  This gives, at
     each site j, the ALLOWED coincidence graph A_j(x) on the four L-sites.
     The coincidence relation is an equivalence, so the realisable graphs are
        dim 1 : all six pairs (all four transversal points equal)
        dim 2 : {} , one edge, a perfect matching, or a triangle
        dim 3 : {} or ONE edge (ker a with supp(a) = that pair)
     and each must be a subgraph of A_j(x).

(B)  WHAT per == 0 ALLOWS: the exhaustive classification of per-null
     quadruples (m2profile2.py) -- the list of (dim, coincidence graph)
     signatures, complete up to the (torus x S_4) symmetry.

A word is KILLED when no signature can be realised inside the allowed graphs.
"""
from __future__ import annotations

import ast
import json
import os
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m2geo as X                                                   # noqa: E402

L, R = X.L, X.R
PAIRS = list(combinations(range(4), 2))


# ------------------------------------------------------- realisable graphs
def graphs_for_dim(d):
    """coincidence graphs (as frozensets of pairs) a subspace of dim d can
    have: the graph is the union of cliques of a partition of {0,1,2,3}."""
    parts = []
    # all set partitions of {0,1,2,3}
    def rec(i, blocks):
        if i == 4:
            parts.append([list(b) for b in blocks])
            return
        for b in blocks:
            b.append(i)
            rec(i + 1, blocks)
            b.pop()
        blocks.append([i])
        rec(i + 1, blocks)
        blocks.pop()
    rec(0, [])
    out = set()
    for P in parts:
        g = frozenset(tuple(sorted(p)) for b in P
                      for p in combinations(sorted(b), 2))
        nb = len(P)
        if d == 1 and nb == 1:
            out.add(g)
        elif d == 2 and nb >= 2 and max(len(b) for b in P) <= 3:
            out.add(g)
        elif d == 3 and len(g) <= 1:
            out.add(g)
    return sorted(out, key=lambda g: (len(g), sorted(g)))


GRAPHS = {d: graphs_for_dim(d) for d in (1, 2, 3)}


# ------------------------------------------------------------ allowed graphs
def dead_col(j, i, c):
    dd = X.DEAD.get((i, j))
    return dd[1] if (dd is not None and dd[0] == c) else None


def allowed_R(x, j):
    return frozenset(p for p in PAIRS
                     if dead_col(j, p[0], x[p[0]]) ==
                     dead_col(j, p[1], x[p[1]]))


def dead_row(i, j, d):
    dd = X.DEAD.get((i, j))
    return dd[0] if (dd is not None and dd[1] == d) else None


def allowed_L(y, i):
    return frozenset(p for p in PAIRS
                     if dead_row(i, R[p[0]], y[p[0]]) ==
                     dead_row(i, R[p[1]], y[p[1]]))


def relabel(g, perm):
    return frozenset(tuple(sorted((perm[p[0]], perm[p[1]]))) for p in g)


def load_signatures(path):
    d = json.load(open(path))
    sigs = []
    for k in d["signatures"]:
        t = ast.literal_eval(k)
        sigs.append(tuple((dd, frozenset(tuple(e) for e in gg))
                          for dd, gg in t))
    return sigs


def word_survives(allowed, sigs):
    """allowed = list of 4 allowed graphs (one per site).  Is there a
    signature, a coordinate relabelling and a slot assignment fitting?"""
    for sig in sigs:
        for perm in permutations(range(4)):            # coordinate relabelling
            slots = [(dd, relabel(gg, perm)) for dd, gg in sig]
            for asg in permutations(range(4)):         # slot -> site
                ok = True
                for s in range(4):
                    dd, gg = slots[s]
                    site = asg[s]
                    if not (gg <= allowed[site]) or gg not in GRAPHS[dd]:
                        ok = False
                        break
                if ok:
                    return True, (sig, perm, asg)
    return False, None


def main(sigpath=None):
    sigpath = sigpath or os.path.join(HERE, "results_profile2_q5.json")
    sigs = load_signatures(sigpath)
    print("loaded %d per-null signatures from %s"
          % (len(sigs), os.path.basename(sigpath)))
    res = {"_header": "UNAUDITED W21-M2-GEO per-word case analysis.",
           "signature_source": os.path.basename(sigpath),
           "n_signatures": len(sigs)}

    killed = []
    for x in X.LFREE:
        allowed = [allowed_R(x, j) for j in R]
        surv, cert = word_survives(allowed, sigs)
        if not surv:
            killed.append((x, [sorted(a) for a in allowed]))
    print("L-free words KILLED by the dead-cell / per-null incompatibility: "
          "%d of 30" % len(killed))
    for x, al in killed:
        print("   x = %s   allowed coincidence graphs per site 4..7: %s"
              % (str(x), al))
    res["killed_Lfree"] = [[list(x), al] for x, al in killed]

    killedR = []
    for y in X.RFREE:
        allowed = [allowed_L(y, i) for i in L]
        surv, cert = word_survives(allowed, sigs)
        if not surv:
            killedR.append((y, [sorted(a) for a in allowed]))
    print("R-free words KILLED: %d of 30" % len(killedR))
    for y, al in killedR:
        print("   y = %s   allowed graphs per L-site 0..3: %s" % (str(y), al))
    res["killed_Rfree"] = [[list(y), al] for y, al in killedR]

    # ---------------------------------------------------------- CONTROLS ---
    # MUTATION CONTROL 1: if the dead cells are ignored (every pair allowed),
    # NO word may be killed.
    full = frozenset(PAIRS)
    bad = sum(1 for x in X.LFREE
              if not word_survives([full] * 4, sigs)[0])
    print("MUTATION control (all coincidences allowed): %d words killed "
          "(want 0)" % bad)
    res["mutation_all_allowed_killed"] = bad
    # MUTATION CONTROL 2: if NO coincidence is allowed anywhere, EVERY word
    # must be killed (the signature list contains no coincidence-free entry).
    emp = frozenset()
    bad2 = sum(1 for x in X.LFREE if word_survives([emp] * 4, sigs)[0])
    print("MUTATION control (no coincidence allowed): %d words survive "
          "(want 0)" % bad2)
    res["mutation_none_allowed_survive"] = bad2

    json.dump(res, open(os.path.join(HERE, "results_kill.json"), "w"),
              indent=1, default=str)
    print("done")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
