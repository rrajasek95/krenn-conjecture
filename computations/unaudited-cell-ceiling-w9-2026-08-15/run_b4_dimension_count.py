#!/usr/bin/env python3
"""W9 Task B4 -- MECHANISM (4') : the OVERDETERMINATION (dimension) count.
This is the only mechanism found that produces a CEILING in the right
direction, because the number of equations grows with the number of cells.

SET-UP.  Fix a template T (cell pattern).  Sources with that template form
(C^*)^Sigma.  The exactness conditions are
        E(T) := #{mixed words w : fibre_T(w) >= 1}     mixed equations
      + 3                                              pure equations
(mixed words of fibre 0 are vacuous; fibre 1 is instantly fatal -- O2).
The gauge group (C^*)^24 acts by A_uv -> D_u A_uv D_v^T; its orbit through a
source of template T has dimension
        r(T) := rank over Q of the Sigma x 24 cell/slot incidence matrix
                (row for cell (a,b) on uv has 1 in columns (u,a) and (v,b)).
Gauge multiplies the pure value H(c^N) by prod_u d_{u,c}, so the subgroup
preserving exactness has dimension r(T) - 3 (when the three pure characters
are independent on the orbit).  The exact locus inside (C^*)^Sigma therefore
has EXPECTED dimension Sigma - E(T) - 3 and must contain those orbits:

        (DC)   Sigma(T)  >=  E(T) + r(T).

(DC) is a TRANSVERSALITY HEURISTIC, not a theorem: the E+3 equations may be
dependent.  It is reported as such.  What makes it worth measuring is that
it is the ONLY available mechanism whose right-hand side GROWS with the
cell count, and that it is exactly checkable on every certificate.

CALIBRATION: the committed near-exact source must SATISFY (DC) -- it exists.
"""
from __future__ import annotations
import importlib, json, os, random, sys
from fractions import Fraction as F
from itertools import combinations, product
import w9_core as w9, w9_template as wt
from w9_core import COLORS, cells

EDGES = tuple(combinations(range(8), 2))


def gauge_rank(template):
    """rank over Q of the cell/slot incidence matrix (24 columns)."""
    col = {(u, a): 8 * 0 + 3 * u + a for u in range(8) for a in COLORS}
    rows = []
    for (u, v), sup in template.items():
        for a, b in sup:
            r = [0] * 24
            r[col[(u, a)]] += 1
            r[col[(v, b)]] += 1
            rows.append([F(x) for x in r])
    # exact Gaussian elimination
    rank = 0
    piv_rows = []
    for r in rows:
        r = list(r)
        for pr, pc in piv_rows:
            if r[pc]:
                f = r[pc] / pr[pc]
                r = [x - f * y for x, y in zip(r, pr)]
        nz = next((c for c in range(24) if r[c] != 0), None)
        if nz is not None:
            piv_rows.append((r, nz))
            rank += 1
    return rank


def supported_mixed(template):
    f = wt.fibres(template)
    E = sum(1 for w, n in f.items() if n >= 1 and len(set(w)) > 1)
    E2 = sum(1 for w, n in f.items() if n >= 2 and len(set(w)) > 1)
    sing = sum(1 for w, n in f.items() if n == 1 and len(set(w)) > 1)
    pures = [f[(c,) * 8] for c in COLORS]
    return E, E2, sing, pures


def dc_row(label, template):
    Sigma = sum(len(s) for s in template.values())
    m = sum(1 for s in template.values() if s)
    E, E2, sing, pures = supported_mixed(template)
    r = gauge_rank(template)
    slack = Sigma - E - r
    return {"label": label, "m": m, "Sigma": Sigma, "E": E, "E_fibre>=2": E2,
            "singletons": sing, "pure_fibres": pures, "gauge_rank": r,
            "DC_slack": slack, "DC_holds": slack >= 0}


if __name__ == "__main__":
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

    def build(params):
        blocks = mod.build_stage_a(params)
        return {(u, v): [[F(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
                for u, v in combinations(range(8), 2)}
    BEST = ((F(-7), F(-9)), (F(7), F(8)), F(5,3), F(-7,4), F(-1,5), F(-8,5),
            (F(-7,4), F(-4), F(7,5)), (F(-3,2), F(-5,4), F(-9)),
            (F(1,5), F(8,3), F(-1,5)), (F(-9,2), F(1), F(3,4)), F(6), F(-9))

    print("=" * 92)
    print("B4  the overdetermination count (DC):  Sigma >= E + r   [transversality heuristic]")
    print("=" * 92)
    rows = []
    print("\n-- CALIBRATION: objects that EXIST must satisfy (DC) --")
    print(f"{'object':28s} {'m':>3} {'Sigma':>6} {'E':>6} {'r':>4} {'slack':>7}  holds")
    for lbl, src in (("STAGE_A_BASE", w9.load_stage_a()),
                     ("STAGE_A_SECOND", w9.load_stage_a(True)),
                     ("STAGE_A_GENERIC", build(BEST))):
        row = dc_row(lbl, wt.template_of(src))
        rows.append(row)
        print(f"{lbl:28s} {row['m']:3d} {row['Sigma']:6d} {row['E']:6d}"
              f" {row['gauge_rank']:4d} {row['DC_slack']:+7d}  {row['DC_holds']}")

    print("\n-- W6's Sigma_min certificates (templates an EXACT source could have) --")
    blob = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                       "results_sigmamin_N8.json")))
    print(f"{'m':>3} {'Sigma_min':>9} {'E':>7} {'r':>4} {'slack=Sigma-E-r':>16}  (DC) holds")
    for rec in blob["rows"]:
        if rec["template"] is None:
            continue
        T = {EDGES[n]: frozenset(tuple(c) for c in s)
             for n, s in enumerate(rec["template"])}
        row = dc_row(f"sigmamin_m{rec['m']}", T)
        rows.append(row)
        print(f"{rec['m']:3d} {row['Sigma']:9d} {row['E']:7d} {row['gauge_rank']:4d}"
              f" {row['DC_slack']:16d}  {row['DC_holds']}")

    print("\n-- W6's zero-singleton band certificates (results_band_certificates) --")
    try:
        band = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                           "results_band_certificates.json")))
        cnt = 0
        keys = band if isinstance(band, dict) else {}
        def walk(o):
            if isinstance(o, dict):
                if "template" in o and isinstance(o["template"], list) and o["template"]:
                    yield o
                for v in o.values():
                    yield from walk(v)
            elif isinstance(o, list):
                for v in o:
                    yield from walk(v)
        seen = []
        for o in walk(band):
            tpl = o["template"]
            if not (isinstance(tpl, list) and len(tpl) == 28):
                continue
            try:
                T = {EDGES[n]: frozenset(tuple(c) for c in s)
                     for n, s in enumerate(tpl)}
            except Exception:
                continue
            row = dc_row(f"band_m{o.get('m','?')}", T)
            seen.append(row)
            cnt += 1
            if cnt > 40:
                break
        if seen:
            print(f"{'m':>3} {'Sigma':>6} {'E':>7} {'r':>4} {'slack':>7}  holds")
            for row in sorted(seen, key=lambda z: z["m"]):
                print(f"{row['m']:3d} {row['Sigma']:6d} {row['E']:7d}"
                      f" {row['gauge_rank']:4d} {row['DC_slack']:+7d}  {row['DC_holds']}")
            rows.extend(seen)
        else:
            print("   (no 28-block templates found in that file)")
    except FileNotFoundError:
        print("   (file absent)")

    with open("results_b4_dimension_count.json", "w") as fh:
        json.dump({"rows": rows}, fh, indent=1, default=str)
    print("\nwrote results_b4_dimension_count.json")
