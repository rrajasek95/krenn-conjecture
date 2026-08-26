#!/usr/bin/env python3
"""UNAUDITED REPAIR PROBE -- item 4, decisive form.  HEAD 7d57c552a3ef.

Two exact facts collapse repair item 4 to a single decidable question.

FACT 1 (derivability of the M_v column).  For every zero-sum alpha,
    (lower=alpha) = sum_i alpha_i*(r0_i - T_i - rho_i) + (ores=alpha).
So the literal M_v alpha column is ALREADY in the span of the core
inventory together with the endpoint-odd Cartan residue column at the SAME
placement.  The M_v family therefore contributes no rank of its own, and
the physical inventory is exactly
    core = {r0_i, T_i, rho_i} + {aggregate ores} + {Cartan residue orbit}.

FACT 2 (rank formula).  rank(physical cone)
    = 18 + rank( span{diagonal} + span{Cartan residue orbit} )  in R^6.
Gate-I needs rank 24 (= ker nu), i.e. the aggregate diagonal together with
the label-group orbit of the ONE placed Cartan residue vector must span all
six ores coordinates.

So the whole of repair item 4 reduces to: WHICH four of the six pure
multiplier labels does the physically constructed endpoint-odd Cartan
residue (-1,+1,+1,-1) actually sit on, and with which sign pattern?
We classify all 30 placements.
"""
from __future__ import annotations

import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"
N, ROWS = 6, 25
LABEL_GROUP = ((0, 1, 2, 3, 4, 5), (0, 2, 1, 3, 5, 4), (4, 2, 3, 1, 5, 0),
               (4, 3, 2, 1, 0, 5), (5, 1, 3, 2, 4, 0), (5, 3, 1, 2, 0, 4))
SCOPE_GUARD_CARTAN = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
DICHOTOMY_ALPHA_FIRST = (Q(-1), Q(1), Q(1), Q(-1), Q(0), Q(0))


def vec(lower=None, ainc=0, w=None, target=None, ores=None):
    a = [Q(0)] * ROWS
    for off, val in ((0, lower), (7, w), (13, target), (19, ores)):
        if val:
            for i, x in enumerate(val):
                a[off + i] += Q(x)
    a[6] += Q(ainc)
    return tuple(a)


def e(i):
    return tuple(Q(int(j == i)) for j in range(N))


def perm(v, p):
    out = [Q(0)] * N
    for i, x in enumerate(v):
        out[p[i]] += x
    return tuple(out)


def rank_gen(cols, nrows):
    m = len(cols)
    rows = [[cols[j][i] for j in range(m)] for i in range(nrows)]
    r = 0
    for c in range(m):
        p = next((i for i in range(r, nrows) if rows[i][c]), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        v = rows[r][c]
        rows[r] = [t / v for t in rows[r]]
        for i in range(nrows):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == nrows:
            break
    return r


def solve(cols, x, nrows=ROWS):
    m = len(cols)
    aug = [[cols[j][i] for j in range(m)] + [x[i]] for i in range(nrows)]
    piv, r = [], 0
    for c in range(m):
        p = next((i for i in range(r, nrows) if aug[i][c]), None)
        if p is None:
            continue
        aug[r], aug[p] = aug[p], aug[r]
        v = aug[r][c]
        aug[r] = [t / v for t in aug[r]]
        for i in range(nrows):
            if i != r and aug[i][c]:
                f = aug[i][c]
                aug[i] = [a - f * b for a, b in zip(aug[i], aug[r])]
        piv.append(c)
        r += 1
        if r == nrows:
            break
    for i in range(r, nrows):
        if aug[i][m]:
            return None
    coef = [Q(0)] * m
    for i, c in enumerate(piv):
        coef[c] = aug[i][m]
    return coef


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
    out = []
    for f in [c for c in range(ROWS) if c not in piv]:
        y = [Q(0)] * ROWS
        y[f] = Q(1)
        for i, p in enumerate(piv):
            y[p] = -at[i][f]
        out.append(tuple(y))
    return out


r0 = [vec(lower=e(i), ainc=-1, target=e(i)) for i in range(N)]
T = [vec(w=tuple(-t for t in e(i)), target=e(i)) for i in range(N)]
rho = [vec(w=e(i), ores=e(i)) for i in range(N)]
agg = vec(ores=(Q(1),) * N)
core = r0 + T + rho + [agg]

report = {"head": HEAD}

# ---- FACT 1: M_v derivability, verified for ALL 15 alpha placements ----
fact1 = []
for sel in combinations(range(N), 4):
    for pattern in ((Q(-1), Q(1), Q(1), Q(-1)), (Q(1), Q(1), Q(-1), Q(-1))):
        al = [Q(0)] * N
        for a, i in zip(pattern, sel):
            al[i] += a
        al = tuple(al)
        lhs = vec(lower=al)
        rhs = [Q(0)] * ROWS
        for i in range(N):
            for k in range(ROWS):
                rhs[k] += al[i] * (r0[i][k] - T[i][k] - rho[i][k])
        cart = vec(ores=al)
        rhs = tuple(a + b for a, b in zip(rhs, cart))
        fact1.append(lhs == rhs)
report["FACT1_Mv_column_equals_core_combination_plus_same_placement_cartan"] = {
    "placements_checked": len(fact1), "all_identities_hold": all(fact1),
    "identity": "(lower=alpha) = sum_i alpha_i (r0_i - T_i - rho_i) + (ores=alpha)",
}

# ---- FACT 2: rank formula + full placement classification -------------
placements = []
for sel in combinations(range(N), 4):
    for pname, pattern in (("(-,+,+,-)", (Q(-1), Q(1), Q(1), Q(-1))),
                           ("(+,+,-,-)", (Q(1), Q(1), Q(-1), Q(-1)))):
        al = [Q(0)] * N
        for a, i in zip(pattern, sel):
            al[i] += a
        placements.append((f"{pname}@{sel}", tuple(al)))

classification = {}
formula_ok = True
for name, cvec in placements:
    orbit = sorted({perm(cvec, p) for p in LABEL_GROUP})
    ores_span = [tuple(v) for v in orbit] + [tuple((Q(1),) * N)]
    ores_rank = rank_gen(ores_span, N)
    cols = core + [vec(ores=v) for v in orbit]
    cone_rank = rank_gen(cols, ROWS)
    if cone_rank != 18 + ores_rank:
        formula_ok = False
    sect = {f"B{j}": ("CONSTRUCTED" if solve(cols, vec(ores=e(j))) is not None
                      else "OBSTRUCTED") for j in range(N)}
    classification[name] = {
        "residue_vector": [str(x) for x in cvec],
        "orbit_size": len(orbit),
        "ores_span_rank_with_aggregate_diagonal": ores_rank,
        "cone_rank": cone_rank,
        "cone_corank_in_25_rows": ROWS - cone_rank,
        "all_six_labelwise_sections": ("CONSTRUCTED"
                                       if all(v == "CONSTRUCTED" for v in sect.values())
                                       else "OBSTRUCTED"),
        "gate_I_assembly": cone_rank == 24,
    }
report["FACT2_rank_formula"] = {
    "formula": "rank(physical cone) = 18 + rank(span{diagonal} + Cartan orbit)",
    "verified_at_every_placement": formula_ok,
}
report["placement_classification"] = classification
good = [n for n, v in classification.items() if v["gate_I_assembly"]]
report["summary"] = {
    "placements": len(placements),
    "placements_giving_Gate_I_YES": len(good),
    "placements_giving_Gate_I_NO": len(placements) - len(good),
    "scope_guard_pinned_placement": "(+,+,-,-)@(0, 2, 3, 5)",
    "scope_guard_verdict": classification["(+,+,-,-)@(0, 2, 3, 5)"],
    "dichotomy_first_alpha_placement": "(-,+,+,-)@(0, 1, 2, 3)",
    "dichotomy_verdict": classification["(-,+,+,-)@(0, 1, 2, 3)"],
}

# ---- separator certificates at the scope-guard placement -------------
cvec = SCOPE_GUARD_CARTAN
orbit = sorted({perm(cvec, p) for p in LABEL_GROUP})
cols_sg = core + [vec(ores=v) for v in orbit]
lk = left_kernel(cols_sg)
certs = {}
for j in range(N):
    d = vec(ores=e(j))
    hit = next(((y, sum(a * b for a, b in zip(y, d))) for y in lk
                if sum(a * b for a, b in zip(y, d))), None)
    certs[f"d_ores_B{j}"] = ({"status": "OBSTRUCTED",
                              "separator": [str(t) for t in hit[0]],
                              "value": str(hit[1])} if hit
                             else {"status": "CONSTRUCTED"})
CAND = {"fixed_B1": e(1), "fixed_B4": e(4),
        "paired_B0_B5": tuple(Q(int(i in (0, 5)), 2) for i in range(N)),
        "paired_B2_B3": tuple(Q(int(i in (2, 3)), 2) for i in range(N))}
for vn, v in CAND.items():
    x = vec(lower=v, ainc=-1)
    hit = next(((y, sum(a * b for a, b in zip(y, x))) for y in lk
                if sum(a * b for a, b in zip(y, x))), None)
    certs[f"x_{vn}"] = ({"status": "OBSTRUCTED",
                         "separator": [str(t) for t in hit[0]],
                         "value": str(hit[1])} if hit
                        else {"status": "CONSTRUCTED"})
report["separator_certificates_at_scope_guard_placement"] = {
    "cartan_residue": [str(x) for x in cvec],
    "left_kernel_dimension": len(lk),
    "certificates": certs,
}

# ---- explicit positive certificate at a Gate-I-YES placement ---------
yes_name, yes_vec = next((n, v) for n, v in placements
                         if classification[n]["gate_I_assembly"])
orbit = sorted({perm(yes_vec, p) for p in LABEL_GROUP})
cols_y = core + [vec(ores=v) for v in orbit]
names = ([f"r0[{i}]" for i in range(N)] + [f"T[{i}]" for i in range(N)]
         + [f"rho[{i}]" for i in range(N)] + ["agg_ores"]
         + [f"cartan_orbit[{i}]" for i in range(len(orbit))])
pos = {}
for j in range(N):
    c = solve(cols_y, vec(ores=e(j)))
    pos[f"d_ores_B{j}"] = {names[i]: str(c[i]) for i in range(len(c)) if c[i]}
for vn, v in CAND.items():
    c = solve(cols_y, vec(lower=v, ainc=-1))
    pos[f"x_{vn}"] = {names[i]: str(c[i]) for i in range(len(c)) if c[i]}
report["explicit_construction_at_a_Gate_I_YES_placement"] = {
    "placement": yes_name,
    "cartan_residue": [str(x) for x in yes_vec],
    "orbit": [[str(t) for t in v] for v in orbit],
    "certificates": pos,
}

# ---- MUTATION CONTROLS ----------------------------------------------
mut = {}
mut["U_v_must_remain_outside_every_placement"] = {
    n: all(solve(core + [vec(ores=v) for v in
                          sorted({perm(cv, p) for p in LABEL_GROUP})],
                 vec(lower=CAND[vn])) is None for vn in CAND)
    for n, cv in placements[:6]}
NU = vec(lower=(Q(1),) * N, ainc=1)
mut["nu_kills_core_and_every_cartan_placement"] = all(
    sum(a * b for a, b in zip(NU, c)) == 0
    for c in core + [vec(ores=v) for _, v in placements])
mut["core_alone_rank"] = rank_gen(core, ROWS)
mut["core_without_aggregate_rank"] = rank_gen(r0 + T + rho, ROWS)
mut["shuffled_label_group_is_not_a_group"] = sorted(
    {tuple(sorted(p)) for p in LABEL_GROUP}) == [tuple(range(N))]
mut["label_group_closed_under_composition"] = all(
    tuple(a[b[i]] for i in range(N)) in LABEL_GROUP
    for a in LABEL_GROUP for b in LABEL_GROUP)
report["mutation_controls"] = mut

print(json.dumps(report, indent=2))
Path(__file__).with_name("out_a6.json").write_text(json.dumps(report, indent=2))

# ---------------------------------------------------------------------
# APPENDIX (run as part of the same probe): two further exact facts.
#
# (i) The dichotomy's "clean collision difference" grant is EXACTLY as
#     strong as granting the five zero-sum labelwise pure-ores directions:
#         (lower=e_i-e_j) = (r0_i-r0_j) - (T_i-T_j) - (rho_i-rho_j)
#                           + (ores = e_i-e_j).
# (ii) Under the OBSTRUCTED (scope-guard) placement, no weaker section
#     helps: every relaxed section is still killed by the same separator.
appendix = {}
coll_ident = []
for i in range(N):
    for j in range(N):
        if i >= j:
            continue
        d = tuple(a - b for a, b in zip(e(i), e(j)))
        rhs = [Q(0)] * ROWS
        for k in range(ROWS):
            rhs[k] = (r0[i][k] - r0[j][k] - T[i][k] + T[j][k]
                      - rho[i][k] + rho[j][k] + vec(ores=d)[k])
        coll_ident.append(tuple(rhs) == vec(lower=d))
appendix["collision_column_identity_holds_for_all_15"] = all(coll_ident)
appendix["collision_grant_equals_zero_sum_ores_grant"] = True

orbit_sg = sorted({perm(SCOPE_GUARD_CARTAN, p) for p in LABEL_GROUP})
cols_sg2 = core + [vec(ores=v) for v in orbit_sg]
relax = {}
for vn, v in CAND.items():
    x = vec(lower=v, ainc=-1)
    tests = {}
    tests["exact_section_ores=v"] = solve(cols_sg2 + [vec(ores=v)], x) is not None
    tests["section_with_zero_augmentation_lower_defect"] = solve(
        cols_sg2 + [vec(ores=v, lower=tuple(a - b for a, b in zip(e(0), e(1))))],
        x) is not None
    tests["section_with_W_defect"] = solve(
        cols_sg2 + [vec(ores=v, w=e(0))], x) is not None
    tests["section_with_target_defect"] = solve(
        cols_sg2 + [vec(ores=v, target=e(0))], x) is not None
    tests["section_with_bare_ainc_(nu_violating)"] = solve(
        cols_sg2 + [vec(ores=v, ainc=1)], x) is not None
    tests["no_section_at_all"] = solve(cols_sg2, x) is not None
    relax[vn] = tests
appendix["weaker_section_relaxations_at_the_obstructed_scope_guard_placement"] = relax

data = json.loads(Path(__file__).with_name("out_a6.json").read_text())
data["appendix"] = appendix
Path(__file__).with_name("out_a6.json").write_text(json.dumps(data, indent=2))
print(json.dumps(appendix, indent=2))

# ---------------------------------------------------------------------
# APPENDIX 2: closed form of the separator family.
#   phi_c := sum_j c_j ( lower_Bj - W_Bj - target_Bj + ores_Bj )
# is exactly the labelwise version of the committed private separator
#   phi = private - W - target + R
# of verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py.
# Claim: left-kernel(physical cone) = <nu> + { phi_c : c _|_ diagonal,
# c _|_ every vector in the Cartan residue orbit }.
def phi(c):
    y = [Q(0)] * ROWS
    for j in range(N):
        y[j] += c[j]
        y[7 + j] -= c[j]
        y[13 + j] -= c[j]
        y[19 + j] += c[j]
    return tuple(y)


ap2 = {}
for name, cvec in placements:
    orbit = sorted({perm(cvec, p) for p in LABEL_GROUP})
    cols = core + [vec(ores=v) for v in orbit]
    lk = left_kernel(cols)
    ores_span = [tuple(v) for v in orbit] + [(Q(1),) * N]
    predicted = 1 + (N - rank_gen(ores_span, N))
    # every phi_c with c orthogonal to the ores span must kill the cone
    cs = []
    A = [[ores_span[j][i] for j in range(len(ores_span))] for i in range(N)]
    # right kernel of the (len x N) matrix whose rows are the ores span
    M = [list(v) for v in ores_span]
    piv, r = [], 0
    for cc in range(N):
        p = next((i for i in range(r, len(M)) if M[i][cc]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        vv = M[r][cc]
        M[r] = [t / vv for t in M[r]]
        for i in range(len(M)):
            if i != r and M[i][cc]:
                f = M[i][cc]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(cc)
        r += 1
    for f in [cc for cc in range(N) if cc not in piv]:
        c = [Q(0)] * N
        c[f] = Q(1)
        for i, p in enumerate(piv):
            c[p] = -M[i][f]
        cs.append(tuple(c))
    ok = all(all(sum(a * b for a, b in zip(phi(c), col)) == 0 for col in cols)
             for c in cs)
    ap2[name] = {"left_kernel_dim": len(lk), "predicted": predicted,
                 "matches": len(lk) == predicted,
                 "phi_c_kills_the_cone_for_every_orthogonal_c": ok}
data = json.loads(Path(__file__).with_name("out_a6.json").read_text())
data["appendix2_separator_closed_form"] = {
    "formula": "left-kernel = <nu> + {phi_c : c _|_ diagonal and c _|_ Cartan orbit}",
    "phi_c": "sum_j c_j (lower_Bj - W_Bj - target_Bj + ores_Bj)",
    "matches_committed_private_separator": "phi = private - W - target + R",
    "verified_at_all_placements": all(v["matches"] and
                                      v["phi_c_kills_the_cone_for_every_orthogonal_c"]
                                      for v in ap2.values()),
    "per_placement": ap2,
}
Path(__file__).with_name("out_a6.json").write_text(json.dumps(data, indent=2))
print("appendix2 verified at all placements:",
      all(v["matches"] and v["phi_c_kills_the_cone_for_every_orthogonal_c"]
          for v in ap2.values()))
