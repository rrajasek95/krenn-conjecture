#!/usr/bin/env python3
"""T1a (reproduce): the A_h eigenvalue h^2-3h+1 on the [2h-2,2] summand.

Three independent confirmations per order h:

  (i)  the two-switch graph IS the association-scheme relation of coset type
       (2,1^{h-2}) and has degree h(h-1);
  (ii) the centered edge indicators phi_e - 1/(2h-1) are exact A_h
       eigenvectors with eigenvalue h^2-3h+1 and span a space of dimension
       h(2h-3) = dim S^{[2h-2,2]};
  (iii) the exact eigenvalue table of the whole scheme, computed from
       intersection numbers, has exactly one eigenspace of multiplicity
       f^{[2h-2,2]} = h(2h-3) and level h-lam_1 = 1, and its A_h eigenvalue
       is h^2-3h+1.

Also prints the full eigenvalue table (input for T2).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_stress import hook_dimension, rank  # noqa: E402
from scheme import Scheme  # noqa: E402


def analyse(h: int, full=True):
    s = Scheme(h, full=full)
    space = s.space
    switch_class = tuple(sorted([2] + [1] * (h - 2), reverse=True))

    # (i) two-switch graph == relation of coset type (2,1^{h-2})
    from lib_stress import coset_type
    base = space.points[0]
    assert set(space.adjacency[0]) == {
        space.index[m] for m in space.points if coset_type(base, m) == switch_class
    }, "two-switch graph is not the (2,1^{h-2}) relation"
    assert s.valency[switch_class] == h * (h - 1)

    # (ii) direct eigenvector check on centered edge indicators
    claim = h * h - 3 * h + 1
    centered = []
    c = Q(1, 2 * h - 1)
    for e in combinations(space.vertices, 2):
        vec = tuple(v - c for v in space.edge_indicator(e))
        assert space.apply_A(vec) == tuple(claim * v for v in vec), (
            "centered edge indicator not an A_h eigenvector", h, e)
        centered.append(vec)
    e1_dim = rank(centered)
    target_dim = hook_dimension((2 * h - 2, 2))
    assert e1_dim == h * (2 * h - 3) == target_dim

    # (iii) scheme-level identification
    hits = [j for j in range(len(s.P)) if s.multiplicity[j] == target_dim]
    assert len(hits) == 1, ("multiplicity f^[2h-2,2] is not unique", hits)
    j1 = hits[0]
    assert s.eigenvalue(j1, 2) == claim
    if full:
        assert s.level[j1] == 1
        assert s.shape[j1] == tuple([h - 1, 1])

    table = []
    for j in range(len(s.P)):
        lam = s.shape.get(j)
        table.append({
            "shape_2lam": list(2 * p for p in lam) if lam else None,
            "A_eigenvalue": str(s.eigenvalue(j, 2)),
            "multiplicity": s.multiplicity[j],
            "level": s.level.get(j),
        })
    print(f"h={h}: |PM|={len(space.points)}  degree={h*(h-1)}  "
          f"A on [{2*h-2},2] = {claim} = h^2-3h+1  dim={e1_dim}=h(2h-3)  OK"
          + ("" if full else "   (light labelling)"))
    for row in sorted(table, key=lambda r: (r["level"] is None, r["level"] or 0)):
        print(f"    2lam={str(row['shape_2lam']):>22}  A={row['A_eigenvalue']:>6}"
              f"  mult={row['multiplicity']:>7}  level={row['level']}")
    return {
        "h": h,
        "matchings": len(space.points),
        "two_switch_degree": h * (h - 1),
        "claimed_A_eigenvalue_on_2h_2_2": claim,
        "E1_dimension": e1_dim,
        "dim_S_2h_2_2": target_dim,
        "eigen_table": table,
        "labelling": "full" if full else "multiplicity-only",
    }


def main():
    args = [int(x) for x in sys.argv[1:]] or [3, 4, 5, 6]
    out = {}
    for h in args:
        out[h] = analyse(h, full=(h <= 6))
    path = Path(__file__).resolve().parent / "t1_matching_scheme.json"
    path.write_text(json.dumps(out, indent=1, sort_keys=True))
    print("wrote", path)


if __name__ == "__main__":
    main()
