#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1 task C: which of the 20 patterns are realizable?

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Rank-one star families give the entire rank-1 stratum reachable by this
probe.  Write A_{p,a} = pi^a (x) u^a and A_{q,b} = chi^b (x) v^b (rank-one
blocks).  Then

    R_{a,b}(w) = u^a_{w_a} v^b_{w_b} * L_{ab},      L_{ab}(K) = pi^a . K . chi^b

so on a K_{m,n} r-support the cap error is a fixed scalar weight times a
PERMANENT of the matrix of linear forms L:

    K_{1,1}:  r^2 = 0                       ->  E == 0            (case (c))
    K_{2,2}:  E_w = s * x_e(w) * weight * per_2(L)
    K_{3,3}:  E_w = 6 * weight * per_3(L)                (x == 0 on U)

Since K -> (pi^a . K . chi^b) is a surjection onto m x n matrices when the
pi's and the chi's are independent, and the generic 2x2 / 3x3 permanent is
irreducible, a splitting FORCES the pi's (or the chi's) to be proportional.
Chasing that degeneracy gives the prediction

    realizable patterns  =  the 10 COLOUR-DIAGONAL ones
        kappa_a^3,  s kappa_a^2,  s^2 kappa_a  (a = 0,1,2),  s^3
    not realizable       =  the 10 MIXED-COLOUR ones
        kappa_a kappa_b kappa_c (not all equal),  s kappa_a kappa_b (a != b)

This module (i) realizes each of the 10 colour-diagonal patterns by an
explicit exact source, and (ii) searches randomly for any mixed-colour
pattern over the same family.  Result of (ii) is reported, not assumed.

Run: python3 wsplit_realizability.py [--trials N]
"""

from __future__ import annotations

import json
import random
import sys

import wsplit_core as core
import wsplit_sources as sources
from wsplit_core import CUBIC_MONOMIALS, COLORS, dense_rows, error_matrix, require
from wsplit_dichotomy import PATTERNS, linear_forms, split_pattern

COLOUR_DIAGONAL = tuple(
    p for p in PATTERNS
    if len({name for name in p if name.startswith("kappa")}) <= 1
)
MIXED = tuple(p for p in PATTERNS if p not in COLOUR_DIAGONAL)
require(len(COLOUR_DIAGONAL) == 10 and len(MIXED) == 10,
        (len(COLOUR_DIAGONAL), len(MIXED)))


def general_star(pairs, pis, chis, ups, vps, x_blocks=None, apq=None) -> dict:
    """Rank-one star source: A_{p,ps} = pi (x) u, A_{q,qs} = chi (x) v."""
    src = core.zero_source()
    if apq is not None:
        src[(core.P, core.Q)] = [list(row) for row in apq]
    for n, (psite, qsite) in enumerate(pairs):
        for i in COLORS:
            for a in COLORS:
                src[core.edge_key(core.P, psite)][i][a] = pis[n][i] * ups[n][a]
        for j in COLORS:
            for b in COLORS:
                src[core.edge_key(core.Q, qsite)][j][b] = chis[n][j] * vps[n][b]
    for edge, table in (x_blocks or {}).items():
        src[edge] = [list(row) for row in table]
    return src


def outer(pi, chi):
    return tuple(tuple(pi[i] * chi[j] for j in COLORS) for i in COLORS)


def basis_vector(c: int):
    return tuple(1 if i == c else 0 for i in COLORS)


def patterns_of(source):
    matrix = error_matrix(source)
    rows = [r for r in dense_rows(matrix) if any(r)]
    if not rows:
        return "E==0", []
    first = rows[0]
    for row in rows[1:]:
        # exact rank-1 test
        pivot = next(c for c in range(len(first)) if first[c])
        for c in range(len(row)):
            if first[pivot] * row[c] - first[c] * row[pivot]:
                return "rank>=2", []
    f = {CUBIC_MONOMIALS[c]: v for c, v in enumerate(first) if v}
    return "rank1", [p["pattern"] for p in split_pattern(f, linear_forms(source))]


X67 = ((1, 0, 2), (0, 1, 1), (3, 1, 0))
U1, U2, U3 = (1, 2, -1), (2, -1, 1), (1, 1, 3)
V1, V2, V3 = (3, 1, 1), (1, 2, -1), (2, 1, 1)
GENERIC = (1, 2, -1)


def constructions() -> list:
    """One explicit exact source per colour-diagonal pattern."""
    out = []
    for a in COLORS:
        ea = basis_vector(a)
        # kappa_a^3 : K_{3,3}, all pi = chi = e_a, x == 0 on U
        out.append((("kappa_%d" % a,) * 3,
                    general_star(((2, 3), (4, 5), (6, 7)), (ea, ea, ea),
                                 (ea, ea, ea), (U1, U2, U3), (V1, V2, V3),
                                 {}, ((1, 2, 0), (0, 3, 1), (2, 0, 1)))))
        # s * kappa_a^2 : K_{2,2}, pi = chi = e_a, A_pq generic
        out.append((("s", "kappa_%d" % a, "kappa_%d" % a),
                    general_star(((2, 3), (4, 5)), (ea, ea), (ea, ea),
                                 (U1, U2), (V1, V2), {(6, 7): X67},
                                 ((1, 0, 0), (0, 2, 0), (0, 0, 3)))))
        # s^2 * kappa_a : K_{2,2}, pi^1 = pi^2 = e_a, chi^1 = e_a,
        # chi^2 generic and A_pq = e_a (x) chi^2 so that pi.K.chi^2 = s
        out.append((("s", "s", "kappa_%d" % a),
                    general_star(((2, 3), (4, 5)), (ea, ea), (ea, GENERIC),
                                 (U1, U2), (V1, V2), {(6, 7): X67},
                                 outer(ea, GENERIC))))
    # s^3 : K_{3,3}, all pi equal, all chi equal, A_pq = pi (x) chi
    pi, chi = (1, 2, -1), (2, 1, 1)
    out.append((("s", "s", "s"),
                general_star(((2, 3), (4, 5), (6, 7)), (pi, pi, pi),
                             (chi, chi, chi), (U1, U2, U3), (V1, V2, V3),
                             {}, outer(pi, chi))))
    return out


def random_search(trials: int, seed: int = 20260815) -> dict:
    """Look for ANY pattern, especially a mixed-colour one, at random."""
    rng = random.Random(seed)
    pool = [basis_vector(c) for c in COLORS] + [
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1), (1, 2, -1), (2, -1, 1)]
    found = {}
    stats = {"rank0": 0, "rank1": 0, "rank>=2": 0}
    for _ in range(trials):
        size = rng.choice((2, 2, 3))
        pairs = ((2, 3), (4, 5), (6, 7))[:size]
        pis = [rng.choice(pool) for _ in range(size)]
        chis = [rng.choice(pool) for _ in range(size)]
        if rng.random() < 0.5:                 # force a degeneracy sometimes
            pis[1] = pis[0]
        if rng.random() < 0.5:
            chis[1] = chis[0]
        ups = [tuple(rng.randint(-2, 2) for _ in COLORS) for _ in range(size)]
        vps = [tuple(rng.randint(-2, 2) for _ in COLORS) for _ in range(size)]
        apq_kind = rng.random()
        if apq_kind < 0.4:
            apq = outer(pis[0], chis[rng.randrange(size)])
        elif apq_kind < 0.7:
            apq = outer(rng.choice(pool), rng.choice(pool))
        else:
            apq = tuple(tuple(rng.randint(-2, 2) for _ in COLORS)
                        for _ in COLORS)
        xb = {} if size == 3 else {(6, 7): X67}
        src = general_star(pairs, pis, chis, ups, vps, xb, apq)
        kind, pats = patterns_of(src)
        stats["rank0" if kind == "E==0" else
              ("rank1" if kind == "rank1" else "rank>=2")] += 1
        for pat in pats:
            found.setdefault(tuple(pat), 0)
            found[tuple(pat)] += 1
    return {"stats": stats,
            "patterns_found": {"*".join(k): v for k, v in sorted(found.items())}}


def main() -> int:
    args = sys.argv[1:]
    trials = int(args[args.index("--trials") + 1]) if "--trials" in args else 3000

    print("== realizability of the 20 patterns ==")
    realized = {}
    for target, src in constructions():
        kind, pats = patterns_of(src)
        ok = tuple(target) in {tuple(p) for p in pats}
        realized["*".join(target)] = {"realized": ok, "C_kind": kind,
                                      "patterns": ["*".join(p) for p in pats]}
        print(f"  target {'*'.join(target):24s} -> {kind:8s} "
              f"patterns {['*'.join(p) for p in pats]}  ok={ok}")
        require(ok, ("construction failed for", target, pats))

    search = random_search(trials)
    print(f"  random star search ({trials} sources): {search['stats']}")
    print(f"    patterns hit: {sorted(search['patterns_found'])}")
    mixed_hits = [k for k in search["patterns_found"]
                  if tuple(k.split("*")) in MIXED]
    print(f"    MIXED-colour patterns hit: {mixed_hits or 'none'}")

    payload = {"colour_diagonal": ["*".join(p) for p in COLOUR_DIAGONAL],
               "mixed": ["*".join(p) for p in MIXED],
               "constructions": realized,
               "random_search": search,
               "mixed_hits": mixed_hits}
    with open("realizability.json", "w") as handle:
        json.dump(payload, handle, indent=1, sort_keys=True, default=str)
    print("wrote realizability.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
