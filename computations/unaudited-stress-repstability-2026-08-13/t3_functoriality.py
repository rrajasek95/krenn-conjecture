#!/usr/bin/env python3
"""T3: is the spectator inclusion an FI-module generator statement?

iota: PM(K_2h) -> PM(K_{2h+2}),  R |-> R + {spectator edge (2h,2h+1)}.

Tested exactly:
  (1) A_{h+1} iota = iota A_h + D, with D the "break the spectator" operator;
      D is computed and its rank/support characterised.
  (2) pi A_{h+1} iota = A_h exactly, where pi is the adjoint of iota
      (restriction to matchings containing the spectator edge).  This is the
      corrected intertwining.
  (3) FI-generation: the S_{2h+2}-shapes occurring in iota(v) for v in the
      constant line and in E1_h=[2h-2,2], and in D(v).  A rep-stability route
      needs these to be a bounded padded list; unbounded mixing kills it.
  (4) the eigenvalue shift lambda_{h+1}-lambda_h = 2h-2 on the transported
      summand.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_stress import edge, rank, switch_neighbors  # noqa: E402
from scheme import Scheme  # noqa: E402


def analyse(h, broken=False):
    small = Scheme(h)
    big = Scheme(h + 1)
    spectator = edge(2 * h, 2 * h + 1)

    def iota(matching):
        if broken:      # T4 mutation: wrong spectator attachment
            return tuple(sorted(matching + (edge(2 * h, 2 * h + 1),)))[::-1]
        return tuple(sorted(matching + (spectator,)))

    embed = {}
    for m in small.points:
        image = iota(m)
        assert image in big.index, ("spectator image is not a matching", m)
        embed[small.index[m]] = big.index[image]

    def push(vector):
        out = [Q(0)] * len(big.points)
        for i, value in enumerate(vector):
            out[embed[i]] += value
        return tuple(out)

    def pull(vector):
        return tuple(vector[embed[i]] for i in range(len(small.points)))

    # ---- (1)(2) exact intertwining with correction
    lam_small = h * h - 3 * h + 1
    lam_big = (h + 1) ** 2 - 3 * (h + 1) + 1
    mixing = []
    for i, m in enumerate(small.points):
        image = iota(m)
        big_nbrs = sorted(big.index[n] for n in switch_neighbors(image))
        transported = sorted(embed[small.index[n]] for n in switch_neighbors(m))
        residual = list(big_nbrs)
        for value in transported:
            assert value in residual, ("iota A_h is not part of A_{h+1} iota", m)
            residual.remove(value)
        # every residual neighbour must have broken the spectator edge
        assert all(spectator not in big.points[j] for j in residual), (
            "correction term kept the spectator edge", m)
        assert len(residual) == 2 * h, ("correction degree changed", len(residual))
        mixing.append(len(residual))
    assert set(mixing) == {2 * h}

    # pi A_{h+1} iota == A_h.  The multiset identity just proved (every extra
    # A_{h+1}-neighbour of iota(m) has destroyed the spectator edge, hence lies
    # outside im(iota) = {matchings containing the spectator}) already proves
    # this; the linear-algebra loop below re-checks it basis vector by basis
    # vector, and is run in full only where it is cheap.
    basis_checked = len(small.points) if h <= 4 else 25
    for i in range(basis_checked):
        basis = [Q(0)] * len(small.points)
        basis[i] = Q(1)
        left = pull(tuple(sum(push(basis)[j] for j in row)
                          for row in big.space.adjacency))
        right = small.space.apply_A(basis)
        assert left == right, ("pi A_{h+1} iota != A_h", i)

    # ---- (3) FI-generation: shapes of the transported summands
    constant = small.space.constant()
    # The centered edge indicators span E1 and lie in a single S_{2h}-orbit;
    # iota is S_{2h}-equivariant and shape content is S_{2h+2}-invariant, so
    # all of them have the same content.  Verified on the full set for h<=4.
    all_e1 = []
    c = Q(1, 2 * h - 1)
    for e in combinations(small.space.vertices, 2):
        all_e1.append(tuple(v - c for v in small.space.edge_indicator(e)))
    assert rank(all_e1) == h * (2 * h - 3)
    e1_vectors = all_e1 if h <= 4 else all_e1[:3]

    content_constant = big.shape_content(push(constant))
    content_e1 = set()
    for v in e1_vectors:
        content_e1 |= set(big.shape_content(push(v)))
    content_e1 = sorted(content_e1)

    # correction operator applied to the same vectors
    def correction(vector):
        pushed = push(vector)
        full = tuple(sum(pushed[j] for j in row) for row in big.space.adjacency)
        return tuple(a - b for a, b in
                     zip(full, push(small.space.apply_A(vector)), strict=True))

    content_dc = big.shape_content(correction(constant))
    content_d1 = set()
    for v in e1_vectors:
        content_d1 |= set(big.shape_content(correction(v)))
    content_d1 = sorted(content_d1)

    # ---- (4) eigenvalue transport
    target = big.by_shape[(h, 1)] if (h, 1) in big.by_shape else None
    transported_eigen = big.eigenvalue(target, 2) if target is not None else None

    print(f"h={h} -> {h+1}:")
    print(f"  A_(h+1) iota = iota A_h + D, deg D = {2*h} = 2h, "
          f"D lands entirely outside im(iota)")
    print(f"  pi A_(h+1) iota = A_h  EXACTLY (no correction)")
    print(f"  shapes of iota(1)          : {[list(s) for s in content_constant]}")
    print(f"  shapes of iota(E1_h)       : {[list(s) for s in content_e1]}")
    print(f"  shapes of D(1)             : {[list(s) for s in content_dc]}")
    print(f"  shapes of D(E1_h)          : {[list(s) for s in content_d1]}")
    print(f"  lambda_h={lam_small}, lambda_(h+1)={transported_eigen}, "
          f"shift={transported_eigen - lam_small if transported_eigen is not None else None}"
          f" (2h-2={2*h-2})")
    return {
        "h": h,
        "correction_degree": 2 * h,
        "correction_outside_image": True,
        "pi_A_iota_equals_A": True,
        "shapes_iota_constant": [list(s) for s in content_constant],
        "shapes_iota_E1": [list(s) for s in content_e1],
        "shapes_D_constant": [list(s) for s in content_dc],
        "shapes_D_E1": [list(s) for s in content_d1],
        "lambda_h": lam_small,
        "lambda_h_plus_1": str(transported_eigen),
        "shift": str(transported_eigen - lam_small),
        "shift_is_2h_minus_2": transported_eigen - lam_small == 2 * h - 2,
    }


def main():
    hs = [int(x) for x in sys.argv[1:] if not x.startswith("-")] or [3, 4]
    out = {h: analyse(h) for h in hs}
    path = Path(__file__).resolve().parent / "t3_functoriality.json"
    path.write_text(json.dumps(out, indent=1, sort_keys=True))
    print("wrote", path)


if __name__ == "__main__":
    main()
