#!/usr/bin/env python3
"""UNAUDITED REPAIR PROBE -- item 4 (A, decisive) and item 5 (B, cone corank).

Pinned HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d.

The scope guard argues that x_v is not source-typed because the ORES BLOCK
alone (aggregate diagonal + one placed Cartan residue line) has rank two and
misses the four repair directions.  That is a statement about the ores block
in isolation.  Membership of x_v=(lower=v,ainc=-1) in the 25-row cone does
NOT require a column equal to (ores=v): the ores defect of R_v-T_v-rho_v can
be routed through the lower/target blocks.  This probe computes the exact
lattice: which inventories put x_v (and each labelwise section d_ores,Bj) in
the span, with explicit rational certificates, over Q, plus mutation
controls.

Label-group orbits are the order-6 group realized by literal source
automorphisms of the canonical faces-(3,5) grade (probe_a2).
"""
from __future__ import annotations

import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"
N, ROWS = 6, 25
LOWER, AINC, W, TARGET, ORES = 0, 6, 7, 13, 19
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))
LABEL_GROUP = ((0, 1, 2, 3, 4, 5), (0, 2, 1, 3, 5, 4), (4, 2, 3, 1, 5, 0),
               (4, 3, 2, 1, 0, 5), (5, 1, 3, 2, 4, 0), (5, 3, 1, 2, 0, 4))
SCOPE_GUARD_CARTAN = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))


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


def perm(v, p):
    out = [Q(0)] * N
    for i, x in enumerate(v):
        out[p[i]] += x
    return tuple(out)


def solve(cols, x):
    """Exact: return coefficient dict if x is in span(cols), else None."""
    m = len(cols)
    aug = [[cols[j][i] for j in range(m)] + [x[i]] for i in range(ROWS)]
    piv = []
    r = 0
    for c in range(m):
        p = next((i for i in range(r, ROWS) if aug[i][c]), None)
        if p is None:
            continue
        aug[r], aug[p] = aug[p], aug[r]
        v = aug[r][c]
        aug[r] = [t / v for t in aug[r]]
        for i in range(ROWS):
            if i != r and aug[i][c]:
                f = aug[i][c]
                aug[i] = [a - f * b for a, b in zip(aug[i], aug[r])]
        piv.append(c)
        r += 1
        if r == ROWS:
            break
    for i in range(r, ROWS):
        if aug[i][m]:
            return None
    coef = [Q(0)] * m
    for i, c in enumerate(piv):
        coef[c] = aug[i][m]
    return coef


def rank_cols(cols):
    if not cols:
        return 0
    return len(cols) - len([c for c in [solve(cols[:i], cols[i])
                                        for i in range(len(cols))] if c is not None])


def rank2(cols):
    m = len(cols)
    rows = [[cols[j][i] for j in range(m)] for i in range(ROWS)]
    r = 0
    for c in range(m):
        p = next((i for i in range(r, ROWS) if rows[i][c]), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        v = rows[r][c]
        rows[r] = [t / v for t in rows[r]]
        for i in range(ROWS):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == ROWS:
            break
    return r


def left_kernel(cols):
    m = len(cols)
    at = [[cols[j][i] for i in range(ROWS)] for j in range(m)]
    piv, r = [], 0
    for c in range(ROWS):
        p = next((i for i in range(r, m) if at[i][c]), None)
        if p is None:
            continue
        at[r], at[p] = at[p], at[r]
        v = at[r][c]
        at[r] = [t / v for t in at[r]]
        for i in range(m):
            if i != r and at[i][c]:
                f = at[i][c]
                at[i] = [a - f * b for a, b in zip(at[i], at[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    basis = []
    for f in [c for c in range(ROWS) if c not in piv]:
        y = [Q(0)] * ROWS
        y[f] = Q(1)
        for i, p in enumerate(piv):
            y[p] = -at[i][f]
        basis.append(tuple(y))
    return basis


def separator(cols, x):
    for y in left_kernel(cols):
        val = sum(a * b for a, b in zip(y, x))
        if val:
            return y, val
    return None, Q(0)


# ---------------- families -------------------------------------------
fam = {}
fam["r0"] = [vec(lower=e(i), ainc=-1, target=e(i)) for i in range(N)]
fam["T"] = [vec(w=tuple(-t for t in e(i)), target=e(i)) for i in range(N)]
fam["rho"] = [vec(w=e(i), ores=e(i)) for i in range(N)]
fam["agg_ores"] = [vec(ores=(Q(1),) * N)]
fam["coll15"] = [vec(lower=tuple(a - b for a, b in zip(e(i), e(j))))
                 for i, j in combinations(range(N), 2)]
alphas = []
for sel in combinations(range(N), 4):
    al = [Q(0)] * N
    for a, i in zip(ALPHA, sel):
        al[i] += a
    alphas.append(tuple(al))
fam["mv15"] = [vec(lower=a) for a in alphas]
fam["cartan15"] = [vec(ores=a) for a in alphas]
# the ONE placed physical packet and its literal-automorphism orbit
mv_placed = alphas[0]
fam["mv1"] = [vec(lower=mv_placed)]
fam["mv_orbit"] = [vec(lower=v) for v in sorted({perm(mv_placed, p)
                                                 for p in LABEL_GROUP})]
fam["cartan1"] = [vec(ores=SCOPE_GUARD_CARTAN)]
fam["cartan_orbit"] = [vec(ores=v) for v in sorted({perm(SCOPE_GUARD_CARTAN, p)
                                                    for p in LABEL_GROUP})]
fam["cartan1_alt"] = [vec(ores=alphas[0])]
fam["cartan_orbit_alt"] = [vec(ores=v) for v in sorted({perm(alphas[0], p)
                                                        for p in LABEL_GROUP})]
fam["pure_lab6"] = [vec(ores=e(i)) for i in range(N)]

CAND = {
    "fixed_B1": e(1), "fixed_B4": e(4),
    "paired_B0_B5": tuple(Q(int(i in (0, 5)), 2) for i in range(N)),
    "paired_B2_B3": tuple(Q(int(i in (2, 3)), 2) for i in range(N)),
}
NU = vec(lower=(Q(1),) * N, ainc=1)

LATTICE = [
    ("REPO_GRANTED  r0+T+rho+pure_lab6+coll15+mv15+cartan15",
     ["r0", "T", "rho", "pure_lab6", "coll15", "mv15", "cartan15"]),
    ("core          r0+T+rho", ["r0", "T", "rho"]),
    ("core+agg      r0+T+rho+agg_ores", ["r0", "T", "rho", "agg_ores"]),
    ("core+agg+cartan1", ["r0", "T", "rho", "agg_ores", "cartan1"]),
    ("core+agg+cartan_orbit", ["r0", "T", "rho", "agg_ores", "cartan_orbit"]),
    ("core+agg+cartan15", ["r0", "T", "rho", "agg_ores", "cartan15"]),
    ("core+agg+mv1", ["r0", "T", "rho", "agg_ores", "mv1"]),
    ("core+agg+mv_orbit", ["r0", "T", "rho", "agg_ores", "mv_orbit"]),
    ("core+agg+mv15", ["r0", "T", "rho", "agg_ores", "mv15"]),
    ("core+agg+coll15", ["r0", "T", "rho", "agg_ores", "coll15"]),
    ("PHYSICAL(minimal placed): core+agg+mv1+cartan1",
     ["r0", "T", "rho", "agg_ores", "mv1", "cartan1"]),
    ("PHYSICAL(orbits): core+agg+mv_orbit+cartan_orbit",
     ["r0", "T", "rho", "agg_ores", "mv_orbit", "cartan_orbit"]),
    ("PHYSICAL(orbits,alt cartan): core+agg+mv_orbit+cartan_orbit_alt",
     ["r0", "T", "rho", "agg_ores", "mv_orbit", "cartan_orbit_alt"]),
    ("core+coll15 (no ores at all)", ["r0", "T", "rho", "coll15"]),
]

report = {"head": HEAD, "lattice": {}}
for label, keys in LATTICE:
    cols = [c for k in keys for c in fam[k]]
    rk = rank2(cols)
    entry = {
        "families": keys, "columns": len(cols), "rank": rk,
        "corank_in_25_rows": ROWS - rk,
        "nu_kills_every_column": all(
            sum(a * b for a, b in zip(NU, c)) == 0 for c in cols),
        "cone_equals_ker_nu": rk == 24,
    }
    sect = {}
    for j in range(N):
        d = vec(ores=e(j))
        c = solve(cols, d)
        sect[f"B{j}"] = "CONSTRUCTED" if c is not None else "OBSTRUCTED"
    entry["labelwise_pure_ores_sections"] = sect
    xs = {}
    for vn, v in CAND.items():
        x = vec(lower=v, ainc=-1)
        c = solve(cols, x)
        rec = {"x_v": "CONSTRUCTED" if c is not None else "OBSTRUCTED",
               "U_v_in_span": solve(cols, vec(lower=v)) is not None}
        if c is None:
            y, val = separator(cols, x)
            rec["separator"] = {"covector": [str(t) for t in y],
                                "value_on_x_v": str(val)}
        xs[vn] = rec
    entry["near_hit_x_v"] = xs
    report["lattice"][label] = entry

# explicit certificate in the minimal placed physical inventory
keys = ["r0", "T", "rho", "agg_ores", "mv1", "cartan1"]
cols = [c for k in keys for c in fam[k]]
names = [f"{k}[{i}]" for k in keys for i in range(len(fam[k]))]
certs = {}
for vn, v in CAND.items():
    c = solve(cols, vec(lower=v, ainc=-1))
    certs[vn] = ({names[i]: str(c[i]) for i in range(len(c)) if c[i]}
                 if c is not None else "OBSTRUCTED")
for j in range(N):
    c = solve(cols, vec(ores=e(j)))
    certs[f"d_ores_B{j}"] = ({names[i]: str(c[i]) for i in range(len(c)) if c[i]}
                             if c is not None else "OBSTRUCTED")
report["explicit_certificates_in_minimal_placed_physical_inventory"] = {
    "families": keys, "certificates": certs}

# MUTATION CONTROLS
mut = {}
bad_cone = [c for k in ["r0", "T", "rho", "agg_ores", "coll15"] for c in fam[k]]
mut["control_removing_agg_ores_from_the_rank24_inventory"] = {
    "rank": rank2([c for k in ["r0", "T", "rho", "coll15"] for c in fam[k]]),
    "expect_below_24": True}
mut["control_x_v_with_ainc_0_must_stay_out"] = {
    vn: solve(bad_cone, vec(lower=v)) is not None for vn, v in CAND.items()}
mut["control_perturbed_x_v_ainc_minus_2"] = {
    vn: solve(bad_cone, vec(lower=v, ainc=-2)) is not None
    for vn, v in CAND.items()}
mut["control_nu_is_the_unique_cokernel_of_the_rank24_inventory"] = [
    [str(t) for t in y] for y in left_kernel(bad_cone)]
mut["control_random_nu_zero_vector_is_in_the_rank24_inventory"] = solve(
    bad_cone, vec(lower=(Q(3), Q(-1), Q(0), Q(2), Q(0), Q(0)), ainc=-4,
                  w=(Q(1),) * N, target=e(2), ores=e(5))) is not None
report["mutation_controls"] = mut

print(json.dumps(report, indent=2))
Path(__file__).with_name("out_a4.json").write_text(json.dumps(report, indent=2))
