#!/usr/bin/env python3
"""UNAUDITED PROBE - Task B: independent exact reconstruction of Gate I data.

Rebuilds, from scratch and in exact rational arithmetic:
  (i)   the 18 -> 15 direction-forgetting map F and its 3-dim kernel;
  (ii)  the 12-supported lower chain u and the identity J_col(u) = -v;
  (iii) the doubled-chart 576-column literal matrix for the canonical
        faces-3/5 component (and all five components);
  (iv)  the target vector J(M_v) with its full augmented signature.

Nothing in this file is imported by the repo.  It uses the repo modules only
as *data sources* (matching lists, full-nine rows, degrees); all linear
algebra is re-implemented here.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = {}


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- linear algebra
def rref(rows):
    """Return (rref rows, pivot columns).  rows is a list of lists of Q."""
    work = [list(r) for r in rows]
    if not work:
        return [], []
    ncol = len(work[0])
    pivots = []
    r = 0
    for c in range(ncol):
        p = next((i for i in range(r, len(work)) if work[i][c]), None)
        if p is None:
            continue
        work[r], work[p] = work[p], work[r]
        v = work[r][c]
        work[r] = [x / v for x in work[r]]
        for i in range(len(work)):
            if i != r and work[i][c]:
                f = work[i][c]
                work[i] = [a - f * b for a, b in zip(work[i], work[r])]
        pivots.append(c)
        r += 1
        if r == len(work):
            break
    return work[:r], pivots


def rank_rows(rows):
    return len(rref(rows)[0])


def nullspace(rows, ncol):
    """Exact basis of {x : rows . x = 0}."""
    red, piv = rref(rows)
    free = [c for c in range(ncol) if c not in piv]
    basis = []
    for f in free:
        v = [Q(0)] * ncol
        v[f] = Q(1)
        for i, c in enumerate(piv):
            v[c] = -red[i][f]
        basis.append(v)
    return basis


def solve_in_span(columns, target):
    """columns: list of vectors (each length h).  Return coeffs or None."""
    if not columns:
        return None if any(target) else []
    h = len(target)
    w = len(columns)
    aug = [[Q(columns[j][i]) for j in range(w)] + [Q(target[i])] for i in range(h)]
    red, piv = rref(aug)
    if w in piv:                      # inconsistent
        return None
    coeff = [Q(0)] * w
    for i, c in enumerate(piv):
        coeff[c] = red[i][w]
    # verify
    chk = [sum((coeff[j] * Q(columns[j][i]) for j in range(w)), Q(0)) for i in range(h)]
    assert chk == [Q(x) for x in target], "solve_in_span reconstruction failed"
    return coeff


PRIME = (1 << 61) - 1


def rank_mod_p_sparse(sparse_cols, nrows, p=PRIME):
    """Rank over F_p of the 0/1 matrix whose columns are given by row-index lists.

    rank_Fp(M) <= rank_Q(M) always (a Q-dependence clears denominators to an
    integer dependence, which reduces mod p).  So a full mod-p rank is an
    exact certificate of full rational rank.
    """
    dense = [dict.fromkeys(c, 1) for c in sparse_cols]     # column -> {row:1}
    pivot_of_row = {}
    rank = 0
    for col in dense:
        cur = dict(col)
        while cur:
            r = min(cur)
            if r in pivot_of_row:
                other, oval = pivot_of_row[r]
                f = cur[r] * pow(oval, p - 2, p) % p
                for rr, vv in other.items():
                    nv = (cur.get(rr, 0) - f * vv) % p
                    if nv:
                        cur[rr] = nv
                    else:
                        cur.pop(rr, None)
            else:
                pivot_of_row[r] = (cur, cur[r])
                rank += 1
                break
    return rank


def left_null_reading_one(columns, target, height):
    """Find covector L with L.column=0 for all columns and L.target=1, or None."""
    rows = [list(map(Q, c)) for c in columns]
    ker = nullspace(rows, height)     # vectors killing every column
    if not ker:
        return None
    # need combination of ker basis with nonzero pairing on target
    vals = [sum((k[i] * Q(target[i]) for i in range(height)), Q(0)) for k in ker]
    for k, v in zip(ker, vals):
        if v:
            return [x / v for x in k]
    return None


# =========================================================== (i) and (ii)
def taskB_input_side():
    tangent = load("computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
                   "probe_tangent")

    def lower_labels(cut):
        cs = set(cut)
        out = []
        for mi, m in enumerate(tangent.MATCHINGS):
            if tangent.crosses_cut(m, cut):
                continue
            rep = tuple(e for e in m if set(e) <= cs)
            assert len(rep) == 1
            out.append((tuple(cut), mi, rep[0]))
        return tuple(out)

    base_cut = tangent.CUTS[0]      # 012
    other_cut = tangent.CUTS[5]     # 024
    assert base_cut == (0, 1, 2) and other_cut == (0, 2, 4)
    other_labels = lower_labels(other_cut)
    base_labels = lower_labels(base_cut)
    assert len(other_labels) == len(base_labels) == 9
    direction_labels = other_labels + base_labels          # 18
    # signed lower chain: +1 on the 024 cube, -1 on the 012 cube
    lower_vec = [Q(1)] * 9 + [Q(-1)] * 9

    key = lambda L: (L[1], L[2])
    phys = tuple(sorted({key(L) for L in direction_labels}))
    pidx = {p: i for i, p in enumerate(phys)}
    assert len(phys) == 15

    # F : k^18 -> k^15  (15 x 18)
    F = [[Q(0)] * 18 for _ in range(15)]
    for j, L in enumerate(direction_labels):
        F[pidx[key(L)]][j] = Q(1)

    rk = rank_rows(F)
    ker = nullspace(F, 18)
    shared = tuple(sorted(set(map(key, other_labels)) & set(map(key, base_labels))))
    assert len(shared) == 3

    # explicit chart-difference generators
    chart_diffs = []
    for p in shared:
        v = [Q(0)] * 18
        a = next(j for j in range(9) if key(direction_labels[j]) == p)
        b = next(j for j in range(9, 18) if key(direction_labels[j]) == p)
        v[a] = Q(1)
        v[b] = Q(-1)
        chart_diffs.append(v)
    # kernel of F equals span of chart differences (both directions)
    same_span = (rank_rows(ker) == rank_rows(chart_diffs)
                 == rank_rows(ker + chart_diffs) == 3)

    u = [sum((F[i][j] * lower_vec[j] for j in range(18)), Q(0)) for i in range(15)]
    support12 = sum(1 for x in u if x)

    # J_col : forget the repeated edge -> 15 matching coordinates
    Jcol = [[Q(0)] * 15 for _ in range(15)]
    for j, (mi, _edge) in enumerate(phys):
        Jcol[mi][j] = Q(1)
    shadow = [sum((Jcol[i][j] * u[j] for j in range(15)), Q(0)) for i in range(15)]

    perms = [tangent.cut_permanent(c) for c in tangent.CUTS]
    v = [Q(a) - Q(b) for a, b in zip(perms[5], perms[0])]   # P_024 - P_012
    minus_v = [-x for x in v]
    ok_shadow = shadow == minus_v
    rep_edges = sorted({e for _m, e in phys})

    # coherence test material: which physical labels are hit from which cut
    from_other = {key(L) for L in other_labels}
    from_base = {key(L) for L in base_labels}

    OUT["taskB_i_ii"] = {
        "direction_labels": 18,
        "physical_labels": len(phys),
        "rank_F": rk,
        "dim_ker_F": len(ker),
        "shared_labels": [list(map(list, [s[1]])) + [s[0]] for s in shared],
        "shared_labels_raw": [[s[0], list(s[1])] for s in shared],
        "kernel_equals_chart_difference_span": same_span,
        "u_support": support12,
        "u_vector": [str(x) for x in u],
        "J_col_u_equals_minus_v": ok_shadow,
        "minus_v_support": sum(1 for x in minus_v for _ in [0] if x),
        "repeated_edges": [list(e) for e in rep_edges],
        "n_repeated_edges": len(rep_edges),
    }
    return dict(direction_labels=direction_labels, F=F, chart_diffs=chart_diffs,
                phys=phys, u=u, minus_v=minus_v, lower_vec=lower_vec,
                other_labels=other_labels, base_labels=base_labels,
                shared=shared, from_other=from_other, from_base=from_base,
                tangent=tangent)


# =========================================================== (iii)
def taskB_literal_module():
    complete = load("computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
                    "probe_complete")
    base = load("computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
                "probe_base")

    records = []
    for ci, (lf, rf, lc, _rc) in enumerate(complete.CUBIC_PAIRS):
        deg = complete.degree_add(base.lambda_degree(lf),
                                  complete.cell_degree(complete.CYCLE_CELLS[lc]))
        rec = complete.component(base, deg)
        cols = rec["columns"]
        # Build the literal boundary matrix MYSELF over the feature basis.
        feats = sorted({f for _w, _m, b in cols for f in b}, key=repr)
        fidx = {f: i for i, f in enumerate(feats)}
        n = len(cols)
        sparse_cols = [sorted(fidx[f] for f in cols[j][2]) for j in range(n)]
        # (a) exact combinatorial injectivity certificate: unique private pivots
        owners = defaultdict(list)
        for j in range(n):
            for f in cols[j][2]:
                owners[f].append(j)
        privates = {j: [f for f in cols[j][2] if owners[f] == [j]] for j in range(n)}
        every_column_private = all(privates[j] for j in range(n))
        min_private = min(len(privates[j]) for j in range(n))
        # (b) independent rank certificate mod a large prime.  rank_Fp <= rank_Q
        #     and rank_Q <= n, so rank_Fp == n proves rank_Q == n exactly.
        r1 = rank_mod_p_sparse(sparse_cols, len(feats))
        # doubled chart [B B]: ker = {(x,y) : B(x+y)=0} = {(x,-x)} when ker B = 0,
        # i.e. exactly the pairwise pq-pr presentation differences.
        r2 = r1
        ker_eq_pres = (r1 == n)
        records.append({
            "component": ci, "faces": [lf, rf],
            "features": len(feats),
            "one_chart_columns": n,
            "one_chart_rank_modp_certificate": r1,
            "one_chart_rank_over_Q": r1 if r1 == n else "NOT CERTIFIED",
            "one_chart_kernel": n - r1,
            "every_column_has_private_pivot": every_column_private,
            "min_private_features_per_column": min_private,
            "two_chart_columns": 2 * n, "two_chart_rank": r2,
            "two_chart_kernel": 2 * n - r2,
            "two_chart_kernel_equals_presentation_differences": ker_eq_pres,
            "presentation_difference_dim": n,
        })
        if ci == 0:
            first = dict(cols=cols, feats=feats, fidx=fidx,
                         complete=complete, rec=rec, privates=privates)
    OUT["taskB_iii_literal_two_chart"] = records
    return first, complete, base


# =========================================================== (iv)
CORNERS = ("P+q00", "P-q00", "P+q11", "P-q11")
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))
BASE_ROWS = tuple(f"{k}_{c}" for c in CORNERS
                  for k in ("private", "Eq", "W", "target", "R")) + ("ainc",)
TERMINAL_ROWS = tuple(f"eta{f}_constant" for f in range(1, 6)) + (
    "eta1_U1", "sigma_qpq22")
SIG_ROWS = BASE_ROWS + TERMINAL_ROWS          # 28 rows


def sig(**e):
    assert set(e) <= set(SIG_ROWS), e
    return tuple(Q(e.get(r, 0)) for r in SIG_ROWS)


def sadd(*vs):
    return tuple(sum(x, Q(0)) for x in zip(*vs))


def sscale(a, v):
    return tuple(Q(a) * x for x in v)


def taskB_target_and_separator():
    cols, names = [], []
    per = {}
    for c in CORNERS:
        r0 = sig(**{f"private_{c}": 1, f"Eq_{c}": 1, f"target_{c}": 1, "ainc": -1})
        T = sig(**{f"W_{c}": -1, f"target_{c}": 1})
        rho = sig(**{f"W_{c}": 1, f"R_{c}": 1})
        Cproj = sig(**{f"Eq_{c}": -1})
        per[c] = {"r0_pq": r0, "r0_pr": r0, "T": T, "rho": rho, "C_projected": Cproj}
        for n, col in per[c].items():
            names.append(f"{n}:{c}")
            cols.append(col)

    terminal = {**{f"eta{f}_constant": 1 for f in range(1, 6)},
                "eta1_U1": 1, "sigma_qpq22": -1}
    literal_c = {c: sig(**{f"private_{c}": -1, f"Eq_{c}": -1}) for c in CORNERS}
    # J(M_v): the required one-cell image
    JMv = sadd(*(sscale(-ALPHA[i], literal_c[c]) for i, c in enumerate(CORNERS)),
               sig(**terminal))
    desired_residue_only = sig(**{f"R_{c}": ALPHA[i] for i, c in enumerate(CORNERS)})
    desired_full = sadd(desired_residue_only, sig(**terminal))
    old_agg = sadd(*(sscale(ALPHA[i], sadd(sscale(-1, per[c]["r0_pq"]),
                                           per[c]["T"], per[c]["rho"]))
                     for i, c in enumerate(CORNERS)))

    # primitive separators
    seps = {}
    for i, c in enumerate(CORNERS):
        phi = sig(**{f"private_{c}": 1, f"W_{c}": -1, f"target_{c}": -1, f"R_{c}": 1})
        seps[c] = phi

    def dot(a, b):
        return sum((x * y for x, y in zip(a, b)), Q(0))

    # chart-difference columns are literally zero in this model (r0_pq == r0_pr)
    chart_diff_cols = [tuple(a - b for a, b in zip(per[c]["r0_pq"], per[c]["r0_pr"]))
                       for c in CORNERS]

    r_old = rank_rows([list(c) for c in zip(*cols)]) if cols else 0
    # rank via rows=SIG_ROWS
    rows_old = [[cols[j][i] for j in range(len(cols))] for i in range(len(SIG_ROWS))]
    r_old = rank_rows(rows_old)
    rows_ext = [[(cols + [JMv])[j][i] for j in range(len(cols) + 1)]
                for i in range(len(SIG_ROWS))]
    r_ext = rank_rows(rows_ext)

    OUT["taskB_iv_target_signature"] = {
        "rows": list(SIG_ROWS),
        "alpha": [str(a) for a in ALPHA],
        "J(M_v)": {r: str(x) for r, x in zip(SIG_ROWS, JMv) if x},
        "desired_full_fiber_target": {r: str(x) for r, x in zip(SIG_ROWS, desired_full) if x},
        "old_cap_aggregate": {r: str(x) for r, x in zip(SIG_ROWS, old_agg) if x},
        "old_agg_plus_JMv_equals_desired_full":
            sadd(old_agg, JMv) == desired_full,
        "old_column_count": len(cols),
        "old_rank": r_old,
        "rank_with_JMv": r_ext,
        "JMv_in_old_span": r_ext == r_old,
        "separators": {
            c: {"formula": "private-W-target+R",
                "kills_all_old_columns": all(dot(seps[c], col) == 0 for col in cols),
                "kills_chart_differences": all(dot(seps[c], d) == 0
                                               for d in chart_diff_cols),
                "value_on_desired_residue_only": str(dot(seps[c], desired_residue_only)),
                "value_on_J(M_v)": str(dot(seps[c], JMv)),
                "value_on_desired_full": str(dot(seps[c], desired_full)),
                "value_on_Eq_only_columns": [str(dot(seps[c], per[cc]["C_projected"]))
                                             for cc in CORNERS]}
            for c in CORNERS},
        "chart_difference_columns_are_identically_zero":
            all(not any(d) for d in chart_diff_cols),
    }
    return dict(cols=cols, names=names, per=per, JMv=JMv,
                desired_full=desired_full, desired_residue_only=desired_residue_only,
                old_agg=old_agg, seps=seps, terminal=terminal, literal_c=literal_c)


if __name__ == "__main__":
    inp = taskB_input_side()
    first, complete, base = taskB_literal_module()
    outp = taskB_target_and_separator()
    print(json.dumps(OUT, indent=2, sort_keys=True))
