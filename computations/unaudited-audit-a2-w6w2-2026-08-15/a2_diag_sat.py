#!/usr/bin/env python3
"""AUDIT A2 / claim A.5 -- EXACT decision of the diagonal regime by SAT.

W6 decided the diagonal regime by simulated annealing, which can only ever
give evidence.  In the diagonal regime the question is exactly decidable and
small, so it is decided here.

MODEL (re-derived).  A diagonal template gives every edge e a palette
P(e) subset {0,1,2} (the block is diag over the colours in P(e)); the
support is {e : P(e) nonempty}.  A perfect matching M supports the word w
iff w is constant on every edge of M and that colour lies in the palette.
Hence a supported (M,w) pair is exactly a matching M together with a colour
for each of its four edges, and

    fibre(w) = #{M : every uv in M has w_u = w_v in P(uv)}.

VARIABLES  x[e][c]        edge e admits colour c            (28*3)
           z[M][w]        matching M supports word w        (105*81)
CLAUSES    z -> the four x's;  the four x's -> z            (equivalence)
           every edge of the support nonempty
           for each colour c: some M has all four edges admitting c
                              (the constant fibre is nonempty)
           for every MIXED word w and every M in Z_w:
                              z[M][w] -> OR_{M' != M} z[M'][w]
                              ("no mixed singleton": count != 1)
           cardinality: exactly m present edges

UNSAT at support m  ==  no zero-singleton diagonal template at support m
(with the three constant fibres nonempty), which is strictly STRONGER than
W6's claim (no min-degree / slot constraints are imposed).

Run: python3 a2_diag_sat.py [--from 12] [--to 28] [--mindeg]
"""

from __future__ import annotations

import json
import sys
from itertools import combinations, product

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

N = 8
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


def perfect_matchings(vs):
    if not vs:
        return [()]
    first, out = vs[0], []
    for i in range(1, len(vs)):
        rest = vs[1:i] + vs[i + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vs[i]),) + tail)
    return out


MATCHINGS = perfect_matchings(tuple(range(N)))


def build(m, mindeg=False, exact_support=True, slotforce=False):
    pool = IDPool()
    x = {(e, c): pool.id(("x", e, c)) for e in range(len(EDGES))
         for c in range(3)}
    present = {e: pool.id(("p", e)) for e in range(len(EDGES))}
    clauses = []
    for e in range(len(EDGES)):
        clauses.append([-present[e]] + [x[(e, c)] for c in range(3)])
        for c in range(3):
            clauses.append([-x[(e, c)], present[e]])

    # z[M][w]: matching M supports word w (w determined by M + colour choice)
    words = {}                      # word -> list of z literals
    for mi, M in enumerate(MATCHINGS):
        for choice in product(range(3), repeat=4):
            w = [0] * N
            for (u, v), c in zip(M, choice):
                w[u] = w[v] = c
            w = tuple(w)
            z = pool.id(("z", mi, w))
            lits = [x[(EIDX[e], c)] for e, c in zip(M, choice)]
            for lit in lits:                       # z -> x
                clauses.append([-z, lit])
            clauses.append([z] + [-lit for lit in lits])   # x's -> z
            words.setdefault(w, []).append(z)

    # constant fibres nonempty
    for c in range(3):
        w = tuple([c] * N)
        clauses.append(list(words[w]))

    # no mixed singleton: for every mixed word, the count of true z is != 1
    for w, zs in words.items():
        if len(set(w)) == 1:
            continue
        for z in zs:
            clauses.append([-z] + [other for other in zs if other != z])

    # support cardinality
    lits = [present[e] for e in range(len(EDGES))]
    if exact_support:
        card = CardEnc.equals(lits=lits, bound=m, vpool=pool,
                              encoding=EncType.seqcounter)
        clauses.extend([list(c) for c in card.clauses])

    if mindeg:
        for v in range(N):
            inc = [present[EIDX[e]] for e in EDGES if v in e]
            card = CardEnc.atleast(lits=inc, bound=3, vpool=pool,
                                   encoding=EncType.seqcounter)
            clauses.extend([list(c) for c in card.clauses])

    if slotforce:
        # Slice-cover admissibility inside the diagonal regime.  A block with
        # palette of size >= 2 is diag with two nonzero diagonal entries, hence
        # rank >= 2, hence cannot be the a (x) e_r of the forced-incident-edge
        # theorem.  So for every (vertex, colour) some incident edge must have
        # palette EXACTLY {colour}.  (This implies beta >= 3N/2 = 12, which is
        # also what W6's budget beta >= 3N - m + |H| gives with |H| = m - beta,
        # and it is W5's diagonal corollary.)
        sc = {}
        for e in range(len(EDGES)):
            for c in range(3):
                v_ = sc[(e, c)] = pool.id(("s", e, c))
                clauses.append([-v_, x[(e, c)]])
                for other in range(3):
                    if other != c:
                        clauses.append([-v_, -x[(e, other)]])
        for v in range(N):
            for c in range(3):
                clauses.append([sc[(EIDX[e], c)] for e in EDGES if v in e])
    return clauses, x, present, pool


def decode(model, x, present):
    pos = {l for l in model if l > 0}
    palettes = []
    for e in range(len(EDGES)):
        palettes.append(sorted(c for c in range(3) if x[(e, c)] in pos))
    return palettes


def main():
    args = sys.argv[1:]
    lo = int(args[args.index("--from") + 1]) if "--from" in args else 12
    slotforce = "--slotforce" in args
    tag = args[args.index("--tag") + 1] if "--tag" in args else ""
    hi = int(args[args.index("--to") + 1]) if "--to" in args else 28
    mindeg = "--mindeg" in args
    rows = []
    for m in range(lo, hi + 1):
        clauses, x, present, pool = build(m, mindeg=mindeg, slotforce=slotforce)
        with Solver(name="cadical195", bootstrap_with=clauses) as s:
            sat = s.solve()
            model = s.get_model() if sat else None
        row = {"m": m, "mindeg_constraint": mindeg,
               "slotforce": slotforce,
               "status": "SAT" if sat else "UNSAT",
               "clauses": len(clauses), "vars": pool.top}
        if sat:
            row["palettes"] = decode(model, x, present)
        rows.append(row)
        print(f"  m={m:2d}: {row['status']}  ({len(clauses)} clauses, "
              f"{pool.top} vars)", flush=True)
        with open(f"results_diag_sat{tag}.json", "w") as h:
            json.dump({"N": N, "rows": rows}, h, indent=1)
    print("done")


if __name__ == "__main__":
    sys.exit(main())
