#!/usr/bin/env python3
"""UNAUDITED REPAIR PROBE -- item 4 (A-II) and item 5 (B, cone corank).

Pinned HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d.

Exact membership problems in the 25-row projected cone of
verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py
(row order lower_B0..B5 | ainc | W_B0..B5 | target_B0..B5 | ores_B0..B5).

For each escalating column inventory we ask, exactly over Q:
  (Q1) is the labelwise pure-ores section d_j = (ores=e_j) in the span?
  (Q2) is the target-normalized near-hit x_v = (lower=v, ainc=-1) in it,
       for the four normalized shared repair directions v?
  (Q3) if not, produce a SEPARATOR certificate: a covector vanishing on
       every column of the inventory and nonzero on the target.
  (Q4) weaker section: allow the section to carry extra lower/ainc/W/target
       output and ask whether the leftover is correctable inside the
       inventory (this is exactly membership of x_v again, so it is decided
       by the same certificate; we additionally report which relaxations
       are and are not harmless).

Inventories:
  GRANTED   = the repo's dichotomy cone (six labelwise pure-ores GRANTED)
  PHYS1     = physical: 1 aggregate ores column + the ONE placed Cartan
              residue line the scope guard admits
  PHYSORB   = physical + the full orbit of that placed Cartan line under the
              order-6 label group realized by literal source automorphisms
              (probe_a2)
  PHYS15    = physical + all 15 alpha placements (strictly stronger than
              anything the source construction supplies; upper bound)
"""
from __future__ import annotations

import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"
N = 6
ROWS = 4 * N + 1
LOWER, AINC, W, TARGET, ORES = 0, 6, 7, 13, 19
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))
CARTAN_LINE = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
LABEL_GROUP = ((0, 1, 2, 3, 4, 5), (0, 2, 1, 3, 5, 4), (4, 2, 3, 1, 5, 0),
               (4, 3, 2, 1, 0, 5), (5, 1, 3, 2, 4, 0), (5, 3, 1, 2, 0, 4))


def vec(lower=None, ainc=0, w=None, target=None, ores=None):
    a = [Q(0)] * ROWS
    for off, val in ((LOWER, lower), (W, w), (TARGET, target), (ORES, ores)):
        if val:
            for i, x in enumerate(val):
                a[off + i] += Q(x)
    a[AINC] += Q(ainc)
    return tuple(a)


def e(i):
    return tuple(Q(int(j == i)) for j in range(N))


def apply_perm(v, p):
    out = [Q(0)] * N
    for i, x in enumerate(v):
        out[p[i]] += x
    return tuple(out)


def rref(rows):
    rows = [list(r) for r in rows]
    piv = []
    r = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        val = rows[r][c]
        rows[r] = [x / val for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
        if r == len(rows):
            break
    return rows[:r], piv


def rank_of_columns(cols):
    if not cols:
        return 0
    rows = [[c[i] for c in cols] for i in range(ROWS)]
    red, _ = rref(rows)
    return len(red)


def left_kernel(cols):
    """All covectors (length ROWS) vanishing on every column."""
    # solve y^T A = 0  <=>  A^T y = 0
    at = [[c[i] for i in range(ROWS)] for c in cols]  # len(cols) x ROWS
    red, piv = rref(at)
    free = [c for c in range(ROWS) if c not in piv]
    basis = []
    for f in free:
        y = [Q(0)] * ROWS
        y[f] = Q(1)
        for i, p in enumerate(piv):
            y[p] = -red[i][f]
        basis.append(tuple(y))
    return basis


def in_span(cols, x):
    return rank_of_columns(cols) == rank_of_columns(list(cols) + [x])


def separator(cols, x):
    for y in left_kernel(cols):
        val = sum(a * b for a, b in zip(y, x))
        if val:
            return y, val
    return None, Q(0)


# ---------------- inventories ----------------------------------------
r0 = [vec(lower=e(i), ainc=-1, target=e(i)) for i in range(N)]
T = [vec(w=tuple(-x for x in e(i)), target=e(i)) for i in range(N)]
rho = [vec(w=e(i), ores=e(i)) for i in range(N)]
pure_lab = [vec(ores=e(i)) for i in range(N)]
agg_ores = [vec(ores=(Q(1),) * N)]
coll = [vec(lower=tuple(a - b for a, b in zip(e(i), e(j))))
        for i, j in combinations(range(N), 2)]
mv, cartan15 = [], []
for sel in combinations(range(N), 4):
    al = [Q(0)] * N
    for a, i in zip(ALPHA, sel):
        al[i] += a
    mv.append(vec(lower=tuple(al)))
    cartan15.append(vec(ores=tuple(al)))
cartan1 = [vec(ores=CARTAN_LINE)]
cartan_orbit = [vec(ores=v) for v in {apply_perm(CARTAN_LINE, p)
                                      for p in LABEL_GROUP}]

INVENTORIES = {
    "GRANTED_repo_dichotomy_cone": r0 + T + rho + pure_lab + coll + mv + cartan15,
    "PHYS1_one_placed_cartan": r0 + T + rho + agg_ores + coll + mv + cartan1,
    "PHYSORB_cartan_symmetry_orbit": r0 + T + rho + agg_ores + coll + mv + cartan_orbit,
    "PHYS15_all_alpha_placements": r0 + T + rho + agg_ores + coll + mv + cartan15,
}

CANDIDATES = {
    "fixed_B1": e(1),
    "fixed_B4": e(4),
    "paired_B0_B5": tuple(Q(int(i in (0, 5)), 2) for i in range(N)),
    "paired_B2_B3": tuple(Q(int(i in (2, 3)), 2) for i in range(N)),
}
NU = vec(lower=(Q(1),) * N, ainc=1)

report = {"head": HEAD, "row_order":
          "lower_B0..B5 | ainc | W_B0..B5 | target_B0..B5 | ores_B0..B5",
          "inventories": {}}

for name, cols in INVENTORIES.items():
    rk = rank_of_columns(cols)
    lk = left_kernel(cols)
    entry = {
        "columns": len(cols),
        "rank": rk,
        "corank_in_25_rows": ROWS - rk,
        "left_kernel_dimension": len(lk),
        "nu_kills_every_column": all(
            sum(a * b for a, b in zip(NU, c)) == 0 for c in cols),
    }
    # per-label labelwise pure-ores section
    per_label = {}
    for j in range(N):
        d = vec(ores=e(j))
        ok = in_span(cols, d)
        rec = {"constructed": ok}
        if not ok:
            y, val = separator(cols, d)
            rec["separator_certificate"] = {
                "covector": [str(x) for x in y],
                "value_on_d_ores_Bj": str(val),
            }
        per_label[f"B{j}"] = rec
    entry["labelwise_pure_ores_section"] = per_label
    # near-hit x_v
    per_v = {}
    for vname, v in CANDIDATES.items():
        x = vec(lower=v, ainc=-1)
        U = vec(lower=v)
        rec = {"x_v_in_span": in_span(cols, x), "U_v_in_span": in_span(cols, U)}
        if not rec["x_v_in_span"]:
            y, val = separator(cols, x)
            rec["separator_certificate"] = {
                "covector": [str(t) for t in y], "value_on_x_v": str(val)}
        per_v[vname] = rec
    entry["near_hit_x_v"] = per_v
    # ores-block reachability (rows 19..24) with zero lower/ainc/W/target
    ores_only = [c for c in cols if not any(c[:ORES])]
    entry["columns_with_output_only_in_the_ores_block"] = len(ores_only)
    entry["rank_of_pure_ores_block"] = (
        rank_of_columns(ores_only) if ores_only else 0)
    report["inventories"][name] = entry

# --------- Q4: which relaxations of the section are harmless ----------
# Any added column c must satisfy nu(c)=0 (nu kills the whole granted cone
# and every literal 288-column readout), so ainc(c) = -sum(lower(c)) is
# FORCED.  Test explicitly which relaxed sections still deliver x_v.
relax = {}
base_cols = INVENTORIES["PHYSORB_cartan_symmetry_orbit"]
for vname, v in CANDIDATES.items():
    x = vec(lower=v, ainc=-1)
    tests = {}
    # (a) section with ores=v and an arbitrary zero-augmentation lower defect
    d_a = vec(ores=v, lower=tuple(a - b for a, b in zip(e(0), e(1))))
    tests["ores=v_plus_zero_augmentation_lower_defect"] = in_span(base_cols + [d_a], x)
    # (b) section with ores=v and augmentation-one lower defect, ainc=-1
    d_b = vec(ores=v, lower=e(0), ainc=-1)
    tests["ores=v_plus_augmentation_one_lower_defect_and_ainc"] = in_span(base_cols + [d_b], x)
    # (c) section with ores=v and nonzero W
    d_c = vec(ores=v, w=e(0))
    tests["ores=v_plus_W_defect"] = in_span(base_cols + [d_c], x)
    # (d) section with ores=v and nonzero target
    d_d = vec(ores=v, target=e(0))
    tests["ores=v_plus_target_defect"] = in_span(base_cols + [d_d], x)
    # (e) section with nonzero ainc only (nu-violating)
    d_e = vec(ores=v, ainc=1)
    tests["ores=v_plus_bare_ainc_(nu_violating)"] = in_span(base_cols + [d_e], x)
    relax[vname] = tests
report["Q4_weaker_section_relaxations"] = relax

# --------- minimal number of new ores directions needed ---------------
need = {}
for vname, v in CANDIDATES.items():
    x = vec(lower=v, ainc=-1)
    need[vname] = {
        "adding_only_d_ores_v_suffices":
            in_span(base_cols + [vec(ores=v)], x),
        "physical_ores_span_rank_without_it":
            rank_of_columns([c for c in base_cols if not any(c[:ORES])]),
    }
report["minimal_addition"] = need

print(json.dumps(report, indent=2))
Path(__file__).with_name("out_a3.json").write_text(json.dumps(report, indent=2))
