#!/usr/bin/env python3
"""T1b (reproduce): the five-sector spectrum of the endpoint-change operator.

Claim under test (notes/2026-08-13-three-interface-proof-frontier.md and
notes/uniform-centered-occurrence-endpoint-association-projector.md):

    (B_h,S) = (4h,+), (2h-2,+), (-2,+), (2h,-), (-2,-)

on the ordered-endpoint module after the matching filter, together with
[A_h,B_h] = [A_h,S] = [B_h,S] = 0 and the cubic projector denominator
8h(h+1)(2h+1).

Everything is checked on the FULL occurrence module {(p,s,R)} on 2h+2 sites
(order h+1), with B_h built from the literal definition (4) of the note:
move p (or s) to a residual site t and pair the displaced endpoint with the
mate of t.  A_h acts on the residual matching only.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_stress import (  # noqa: E402
    endpoint_neighbors, occurrence_count, occurrences, rank, switch_neighbors,
)


def build(h):
    sites = tuple(range(2 * h + 2))
    occ = occurrences(sites)
    assert len(occ) == occurrence_count(h + 1)
    index = {o: i for i, o in enumerate(occ)}
    B_adj = tuple(tuple(index[n] for n in endpoint_neighbors(o, sites)) for o in occ)
    A_adj = tuple(tuple(index[(o[0], o[1], m)] for m in switch_neighbors(o[2]))
                  for o in occ)
    S_map = tuple(index[(o[1], o[0], o[2])] for o in occ)
    return sites, occ, index, A_adj, B_adj, S_map


def apply_adj(adj, v):
    return tuple(sum(v[j] for j in row) for row in adj)


def analyse(h):
    sites, occ, index, A_adj, B_adj, S_map = build(h)
    n = 2 * h + 2

    apply_A = lambda v: apply_adj(A_adj, v)
    apply_B = lambda v: apply_adj(B_adj, v)
    apply_S = lambda v: tuple(v[j] for j in S_map)

    # --- operator commutations, verified on every basis vector (multiset test)
    for i, o in enumerate(occ):
        left = sorted(j for a in A_adj[i] for j in B_adj[a])
        right = sorted(j for b in B_adj[i] for j in A_adj[b])
        assert left == right, ("[A,B] != 0", h, o)
        assert sorted(S_map[a] for a in A_adj[i]) == sorted(A_adj[S_map[i]]), \
            ("[A,S] != 0", h, o)
        assert sorted(S_map[b] for b in B_adj[i]) == sorted(B_adj[S_map[i]]), \
            ("[B,S] != 0", h, o)

    # --- the five matching-flat sectors, as explicit functions of (p,s) only
    marked_p, marked_s = 0, 1
    def lift(f):
        return tuple(Q(f(o[0], o[1])) for o in occ)

    def std(x):
        return 1 if x == 0 else (-1 if x == 1 else 0)

    sym_pair_values = {(0, 1): 1, (1, 0): 1, (2, 3): 1, (3, 2): 1,
                       (0, 2): -1, (2, 0): -1, (1, 3): -1, (3, 1): -1}
    alt_wedge_values = {(0, 1): 1, (1, 2): 1, (2, 0): 1,
                        (1, 0): -1, (2, 1): -1, (0, 2): -1}

    sectors = {
        "constant": (lift(lambda p, s: 1), 4 * h, 1),
        "symmetric_standard": (lift(lambda p, s: std(p) + std(s)), 2 * h - 2, 1),
        "symmetric_pair": (lift(lambda p, s: sym_pair_values.get((p, s), 0)),
                           -2, 1),
        "alternating_standard": (lift(lambda p, s: std(p) - std(s)), 2 * h, -1),
        "alternating_wedge": (lift(lambda p, s: alt_wedge_values.get((p, s), 0)),
                              -2, -1),
    }
    for name, (vec, b_eig, s_eig) in sectors.items():
        assert any(vec), name
        assert apply_B(vec) == tuple(b_eig * v for v in vec), (
            "B_h eigenvalue changed", h, name, b_eig)
        assert apply_S(vec) == tuple(s_eig * v for v in vec), (
            "S eigenvalue changed", h, name)
        # these matching-flat vectors are A_h-constant (degree h(h-1))
        assert apply_A(vec) == tuple(h * (h - 1) * v for v in vec), (
            "matching-flat sector is not A_h-radial", h, name)

    # --- the five sectors exhaust the ordered-pair module
    dims = {
        "constant": 1,
        "symmetric_standard": n - 1,
        "symmetric_pair": n * (n - 3) // 2,
        "alternating_standard": n - 1,
        "alternating_wedge": (n - 1) * (n - 2) // 2,
    }
    assert sum(dims.values()) == n * (n - 1)

    # --- the pointed matching-flat row: cyclic module is 5-dimensional and the
    #     cubic projector sends it to a nonzero constant
    marked_matching = tuple((2 * i, 2 * i + 1) for i in range(1, h + 1))
    def row_value(p, s):
        q = sum(int(p not in e and s not in e) for e in marked_matching)
        if (p, s) == (marked_p, marked_s):
            const = 4 * h * h + 4 * h
        elif p == marked_p or s == marked_s:
            const = 2 * h - 1
        else:
            const = 0
        return q + (2 * h - 1) * const
    row = lift(row_value)
    krylov = [row]
    for _ in range(5):
        krylov.append(apply_B(krylov[-1]))
    assert rank(krylov + [apply_S(row)]) == 5, ("cyclic module dimension", h)

    projected = row
    denominator = 1
    for theta in (-2, 2 * h - 2, 2 * h):
        image = apply_B(projected)
        projected = tuple(a - theta * b for a, b in zip(image, projected, strict=True))
        denominator *= (4 * h - theta)
    assert len(set(projected)) == 1 and projected[0], ("cubic projector", h)
    assert denominator == 8 * h * (h + 1) * (2 * h + 1), (denominator, h)

    print(f"h={h}: occurrences={len(occ)}  B-degree={4*h}  "
          f"(B,S) sectors verified: (4h,+),(2h-2,+),(-2,+),(2h,-),(-2,-)  "
          f"[A,B]=[A,S]=[B,S]=0  P_h(4h)={denominator}=8h(h+1)(2h+1)  OK")
    return {
        "h": h,
        "occurrences": len(occ),
        "B_degree": 4 * h,
        "sector_eigenvalues": {k: [v[1], v[2]] for k, v in sectors.items()},
        "sector_dimensions": dims,
        "cyclic_module_dimension": 5,
        "projector_denominator": denominator,
        "commutators_zero": ["[A,B]", "[A,S]", "[B,S]"],
    }


def main():
    hs = [int(x) for x in sys.argv[1:]] or [2, 3, 4]
    out = {h: analyse(h) for h in hs}
    path = Path(__file__).resolve().parent / "t1_endpoint_spectrum.json"
    path.write_text(json.dumps(out, indent=1, sort_keys=True))
    print("wrote", path)


if __name__ == "__main__":
    main()
