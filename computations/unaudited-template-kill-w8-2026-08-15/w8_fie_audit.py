#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- audit W6's zero-singleton certificates against the
committed FORCED INCIDENT-EDGE THEOREM.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

W6 defined its admissible template space by
    "three constant fibres nonempty, every (vertex,colour) SLOT covered,
     min degree >= 3, beta = max(0, 3N - m) single cells"
(w6_task2_sigmamin.py docstring; CEIL.structural_ok).  "Slot covered" is the
NEAR-end condition: some cell at v uses colour c.

The committed forced incident-edge theorem (notes/slice-cover.md sec. 2,
eq. (6)) is the FAR-end condition and is strictly stronger:

  (FIE) for every vertex p and colour r there is a neighbour j with
        A_pj = a (x) e_r^{(j)}, C_pj != 0

-- the whole block on pj must be supported in the single column r at j.
W6 itself imports this as premise (S1) of the J.1d budget derivation
(w6_task2_counting.py) but only uses its consequence d_R(v) >= 3.

This script re-reads W6's saved certificates and reports, per m: the near-end
slot condition, min degree, the J.1d floor, and FIE.

Run: python3 w8_fie_audit.py
"""

from __future__ import annotations

import json
import sys

import w8_core as C

W6 = "/Users/rishi/workplace/krenn-conjecture/computations/" \
     "unaudited-bridge-w6-2026-08-15/"


def from_cells(cell_lists):
    template = [0] * 28
    for e, cells in enumerate(cell_lists):
        mask = 0
        for i, j in cells:
            mask |= 1 << (3 * i + j)
        template[e] = mask
    return tuple(template)


def slots_ok(geo, template):
    """W6's near-end condition: every (vertex, colour) appears in some cell."""
    slots = set()
    for e, mask in enumerate(template):
        u, v = geo.edges[e]
        for i, j in C.cells(mask):
            slots.add((u, i))
            slots.add((v, j))
    return len(slots) == 24


def degrees(geo, template):
    deg = [0] * 8
    for e, mask in enumerate(template):
        if mask:
            u, v = geo.edges[e]
            deg[u] += 1
            deg[v] += 1
    return deg


def report(geo, name, m, template):
    compat = C.compat_matrix(geo, template)
    a = C.audit(geo, template, compat)
    deg = degrees(geo, template)
    missing = [k for k, v in C.fie_demands(geo, template).items() if not v]
    row = {"source": name, "m_claimed": m, "m": a["m"], "sigma": a["sigma"],
           "beta_single": a["beta"], "thin": a["thin"], "fat": a["fat"],
           "mixed_singletons": a["mixed_singletons"],
           "constants_ok": a["constants"], "slots_ok": slots_ok(geo, template),
           "min_degree": min(deg), "budget_floor_ok": a["budget_floor_ok"],
           "FIE": a["fie"], "FIE_demands_unserved": len(missing),
           "FIE_first_unserved": missing[:4]}
    return row


def main():
    geo = C.geometry(8)
    rows = []

    band = json.load(open(W6 + "results_band_certificates.json"))
    for record in band:
        if record["template"] in (None, "None"):
            continue
        template = from_cells(json.loads(record["template"].replace("'", '"'))
                              if isinstance(record["template"], str)
                              else record["template"])
        rows.append(report(geo, "band_certificates", int(record["m"]),
                           template))

    sig = json.load(open(W6 + "results_sigmamin_N8.json"))
    for record in sig["rows"]:
        if not record["template"]:
            continue
        rows.append(report(geo, "sigmamin", record["m"],
                           from_cells(record["template"])))

    print(f"{'src':<20}{'m':>3}{'Sig':>5}{'beta':>5}{'thin':>5}{'fat':>5}"
          f"{'sing':>6}{'const':>7}{'slots':>7}{'deg':>5}{'floor':>7}"
          f"{'FIE':>6}{'unserved':>10}")
    for row in rows:
        print(f"{row['source']:<20}{row['m']:>3}{row['sigma']:>5}"
              f"{row['beta_single']:>5}{row['thin']:>5}{row['fat']:>5}"
              f"{row['mixed_singletons']:>6}{str(row['constants_ok']):>7}"
              f"{str(row['slots_ok']):>7}{row['min_degree']:>5}"
              f"{str(row['budget_floor_ok']):>7}{str(row['FIE']):>6}"
              f"{row['FIE_demands_unserved']:>10}")

    total = len(rows)
    fie = sum(1 for r in rows if r["FIE"])
    zero = sum(1 for r in rows if r["mixed_singletons"] == 0)
    print(f"\nW6 certificates re-checked: {total}; zero-singleton confirmed: "
          f"{zero}; FIE-admissible: {fie}")
    json.dump({"rows": rows, "total": total, "fie_admissible": fie,
               "zero_singleton_confirmed": zero},
              open("results_fie_audit.json", "w"), indent=1)
    print("wrote results_fie_audit.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
