#!/usr/bin/env python3
"""T2d: is the note's closed-form transfer row uniform in h?

The committed checkers verify the matching-flat row only at h=3 (and then
*assume* the closed form when testing the endpoint projector at h=2,3,4).
Here the Gram row is evaluated pointwise at arbitrary h through the exact
chart-preimage routine

    k_f(g) = sum_{c : m_c(f)>0} m_c(f) * |preimages(g,c)|,

so no order-(h+1) occurrence set ever has to be materialised.  Tested against

    k_f(g)  =  |F cap R_g| + C_{p,s},                             (13)-(14)
    (A_h - lambda_h) k_f  =  q_{p,s} + (2h-1) C_{p,s}   on each fibre.  (15)

Fibres are checked exhaustively (every residual matching) where feasible and
by random sampling above that.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_stress import (  # noqa: E402
    charts, double_factorial_odd, marked_occurrence, perfect_matchings,
    switch_neighbors,
)
from transfer import preimages  # noqa: E402


def relevant_charts(h, marked, sites):
    out = []
    for chart in charts(sites):
        small = tuple(v for v in sites if v not in chart[0])
        pre = preimages(marked, chart, small)
        if pre:
            out.append((chart, small, len(pre)))
    assert sum(m for _, _, m in out) == 7 * h, ("column count", h)
    return out


def row_value(g, relevant):
    return sum(mult * len(preimages(g, chart, small))
               for chart, small, mult in relevant)


def predicted(g, marked, h):
    p, s, matching = g
    mp, ms, F = marked
    overlap = len(set(matching) & set(F))
    if (p, s) == (mp, ms):
        c = 4 * h * h + 4 * h
    elif p == mp or s == ms:
        c = 2 * h - 1
    else:
        c = 0
    return overlap + c


def q_value(p, s, marked):
    return sum(int(p not in e and s not in e) for e in marked[2])


def analyse(h, exhaustive_limit=11000, samples=300, seed=11):
    rng = random.Random(seed)
    sites = tuple(range(2 * h + 2))
    marked = marked_occurrence(h)
    relevant = relevant_charts(h, marked, sites)
    lam = h * h - 3 * h + 1

    fibre_specs = [
        ("pf,sf", (0, 1)),
        ("sf,pf", (1, 0)),
        ("pf,r", (0, 2)),
        ("r,sf", (2, 1)),
        ("r,r,mates", (2, 3)),
        ("r,r,apart", (2, 4)) if h >= 2 else None,
    ]
    fibre_specs = [f for f in fibre_specs if f]
    records = {}
    all_ok = True
    for name, (p, s) in fibre_specs:
        rest = tuple(v for v in sites if v not in (p, s))
        count = double_factorial_odd(2 * h - 1)
        exhaustive = count <= exhaustive_limit
        matchings = (list(perfect_matchings(rest)) if exhaustive else None)
        if exhaustive:
            chosen = matchings
        else:
            chosen = []
            pool = None
            for _ in range(samples):
                vertices = list(rest)
                rng.shuffle(vertices)
                m = tuple(sorted(
                    (min(vertices[2 * i], vertices[2 * i + 1]),
                     max(vertices[2 * i], vertices[2 * i + 1]))
                    for i in range(len(vertices) // 2)))
                chosen.append(m)
        formula_ok = True
        for m in chosen:
            g = (p, s, m)
            if row_value(g, relevant) != predicted(g, marked, h):
                formula_ok = False
                break
        # flatness of (A-lambda)k_f on this fibre
        flat_values = set()
        flat_sample = chosen if exhaustive else chosen[:40]
        for m in flat_sample:
            total = sum(row_value((p, s, n), relevant) for n in switch_neighbors(m))
            flat_values.add(total - lam * row_value((p, s, m), relevant))
        if (p, s) == (marked[0], marked[1]):
            c = 4 * h * h + 4 * h
        elif p == marked[0] or s == marked[1]:
            c = 2 * h - 1
        else:
            c = 0
        expected_flat = q_value(p, s, marked) + (2 * h - 1) * c
        flat_ok = flat_values == {expected_flat}
        all_ok = all_ok and formula_ok and flat_ok
        records[name] = {
            "endpoints": [p, s],
            "checked": "exhaustive" if exhaustive else f"{len(chosen)} random",
            "closed_form_holds": formula_ok,
            "flattened_constant": flat_ok,
            "flattened_value": str(sorted(flat_values)),
            "expected": expected_flat,
        }
        print(f"  h={h} fibre {name:<11} ({records[name]['checked']:>18}): "
              f"closed form {formula_ok}, flat {flat_ok} "
              f"value={sorted(flat_values)} expected={expected_flat}")
    return {"h": h, "all_ok": all_ok, "fibres": records}


def main():
    hs = [int(x) for x in sys.argv[1:]] or [3, 4, 5, 6, 7, 8, 10, 12]
    out = {}
    for h in hs:
        out[h] = analyse(h)
    path = Path(__file__).resolve().parent / "t2d_row_formula_high_h.json"
    path.write_text(json.dumps(out, indent=1, sort_keys=True))
    print("wrote", path)


if __name__ == "__main__":
    main()
