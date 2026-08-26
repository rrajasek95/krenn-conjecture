#!/usr/bin/env python3
"""UNAUDITED REPAIR PROBE -- item 5 (B) + item 4 equivariance check.
HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d.

(1) LITERAL EQUIVARIANCE of the audited rows.  The order-6 label group of
    probe_a2 is realized by literal automorphisms of the direct-free
    presentation.  We check LITERALLY that each such automorphism carries
    the j-th selected private matching feature to the sigma(j)-th, and
    preserves the pure-aggregate marker.  This is what licenses transporting
    the ONE placed physical Cartan/M_v packet around the orbit: the
    lower/ainc readouts are equivariant on committed data.  (The ores
    readout has no committed definition -- see the REPORT.)

(2) CORANK of every object the bordered theorem could be applied to that is
    actually constructible from committed data:
      (a) the literal 288-column protected incidence map on the canonical
          faces-(3,5) packet: exact rank, column-kernel, row-cokernel;
      (b) its two-chart form;
      (c) the 25-row projected cone at each inventory (probe_a4);
      (d) the hardcoded 3x3 anchor-dark block itself.
    Plus the corank-1 sensitivity of the bordered factorization.
"""
from __future__ import annotations

import importlib.util
import json
import random
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path

SNAP = Path("/private/tmp/claude-501/-Users-rishi/f8396279-dd28-41de-876d-5c03a4d8d65a/scratchpad/repair45/snap")
HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, SNAP / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


base = load("computations/verify_h3_direct_free_complete_first_fine_degree_membership.py", "b")
complete = load("computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py", "c")
absolute = load("computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py", "a")

left, right, lc, _ = complete.CUBIC_PAIRS[1]
td = complete.degree_add(base.lambda_degree(left),
                         complete.cell_degree(complete.CYCLE_CELLS[lc]))
comp = complete.component(base, td)
pure_indices, selected = absolute.selected_private_features(comp)
pure_labels = [comp["columns"][i][1] for i in pure_indices]
pure_index_of = {m: j for j, m in enumerate(pure_labels)}
DF = set(base.DIRECT_FREE_PAIR)
report = {"head": HEAD}

# ---------------- (1) literal equivariance ---------------------------
def act_cell(cell, sigma, tau):
    l, r, a, b = cell
    l2, a2 = sigma[l], tau[l][a]
    r2, b2 = sigma[r], tau[r][b]
    return (l2, r2, a2, b2) if l2 < r2 else (r2, l2, b2, a2)


def act_mon(mon, sigma, tau):
    return tuple(sorted(act_cell(c, sigma, tau) for c in mon))


def act_word(word, sigma, tau):
    out = [0] * 8
    for s, c in enumerate(word):
        out[sigma[s]] = tau[s][c]
    return tuple(out)


colour_perms = list(permutations(range(3)))
group = []
for p in permutations(range(8)):
    sigma = tuple(p)
    if {sigma[s] for s in DF} != DF:
        continue
    per, ok = [], True
    for s in range(8):
        good = [t for t in colour_perms
                if all(td[3 * sigma[s] + t[c]] == td[3 * s + c] for c in range(3))]
        if not good:
            ok = False
            break
        per.append(good)
    if ok:
        for tau in product(*per):
            group.append((sigma, tuple(tau)))
stab = [g for g in group if act_word(complete.PURE_WORD, *g) == complete.PURE_WORD]

# private-feature SETS (selected[j] is min() of this set -- an arbitrary
# tie-break, so equivariance must be tested on the SET, not on the min)
from collections import defaultdict
owners = defaultdict(list)
for ci, (_w, _m, b) in enumerate(comp["columns"]):
    for f in b:
        owners[f].append(ci)
private_sets = [frozenset(f for f in comp["columns"][i][2] if owners[f] == [i])
                for i in pure_indices]

checked = 0
set_equivariance_failures = 0
min_equivariance_failures = 0
feature_equivariance_failures = 0
marker_failures = 0
column_set = {(w, m) for w, m, _ in comp["columns"]}
for sigma, tau in stab:
    lab = tuple(pure_index_of[act_mon(m, sigma, tau)] for m in pure_labels)
    for j in range(6):
        if frozenset(act_mon(f, sigma, tau) for f in private_sets[j]) != private_sets[lab[j]]:
            set_equivariance_failures += 1
        if act_mon(selected[j], sigma, tau) != selected[lab[j]]:
            min_equivariance_failures += 1
        checked += 1
    # the pure-aggregate marker is the predicate word == PURE_WORD; the
    # automorphism must permute the 288 columns preserving that predicate
    images = {(act_word(w, sigma, tau), act_mon(m, sigma, tau))
              for w, m, _ in comp["columns"]}
    if images != column_set:
        marker_failures += 1

feature_equivariance_failures = set_equivariance_failures

report["literal_row_equivariance"] = {
    "pure_word_stabilizer_order": len(stab),
    "selected_private_feature_checks": checked,
    "private_feature_SET_equivariance_failures": set_equivariance_failures,
    "min_tiebreak_equivariance_failures_(artifact_of_min())": min_equivariance_failures,
    "column_set_permutation_failures_(pure_aggregate_marker)": marker_failures,
    "verdict": ("the lower_B private-feature blocks and the ainc marker are "
                "LITERALLY equivariant for the whole order-6 label group"
                if feature_equivariance_failures == 0 and marker_failures == 0
                else "NOT equivariant"),
}

# ---------------- (2a,b) literal protected incidence map -------------
cols = comp["columns"]
features = sorted({f for _, _, b in cols for f in b}, key=repr)
findex = {f: i for i, f in enumerate(features)}


def sparse_rank(columns, nrows):
    """Exact rank over Q of sparse {row: value} columns."""
    piv = {}
    r = 0
    for col in columns:
        v = dict(col)
        while v:
            p = min(v)
            if p in piv:
                f = v[p] / piv[p][p]
                for k, x in piv[p].items():
                    v[k] = v.get(k, Q(0)) - f * x
                    if v[k] == 0:
                        del v[k]
            else:
                piv[p] = v
                r += 1
                break
    return r


sparse_cols = [{findex[f]: Q(1) for f in b} for _, _, b in cols]
rk = sparse_rank(sparse_cols, len(features))
two_chart = sparse_cols + sparse_cols
rk2 = sparse_rank(two_chart, len(features))
report["literal_protected_incidence_map_canonical_packet"] = {
    "faces": [left, right],
    "rows_(distinct_literal_matching_features)": len(features),
    "columns": len(cols),
    "exact_rank_over_Q": rk,
    "column_kernel_dimension_(corank_on_the_source_side)": len(cols) - rk,
    "row_cokernel_dimension": len(features) - rk,
    "two_chart_columns": len(two_chart),
    "two_chart_exact_rank": rk2,
    "two_chart_kernel_dimension": len(two_chart) - rk2,
    "corank_one_holds": (len(cols) - rk) == 1,
}

# ---------------- (2d) the hardcoded anchor-dark block ---------------
def rank_dense(M):
    M = [list(map(Q, r)) for r in M]
    r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        v = M[r][c]
        M[r] = [x / v for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


RESPONSE = ((4, -2, -1), (3, -2, 0), (0, 0, 0))
CIRCUIT = (2, 3, 2)
report["anchor_dark_bordered_block"] = {
    "source": "hardcoded literal in verify_h3_anchor_dark_bordered_cartan_alternative.py",
    "matrix": [list(r) for r in RESPONSE],
    "rank": rank_dense(RESPONSE),
    "corank": 3 - rank_dense(RESPONSE),
    "kernel_generator_k": list(CIRCUIT),
    "A_k_is_zero": all(sum(a * b for a, b in zip(row, CIRCUIT)) == 0
                       for row in RESPONSE),
    "third_row_is_padding": list(RESPONSE[2]) == [0, 0, 0],
    "built_from_committed_literal_data": False,
}

# corank sensitivity of the bordered factorization h(k)=0 => h = lam*A
random.seed(20260813)
stats = {1: [0, 0], 2: [0, 0], 3: [0, 0]}
for _ in range(3000):
    for target_corank in (1, 2, 3):
        n = 4
        r = n - target_corank
        Aa = [[Q(random.randint(-3, 3)) for _ in range(r)] for _ in range(n)]
        Bb = [[Q(random.randint(-3, 3)) for _ in range(n)] for _ in range(r)]
        A = [[sum(Aa[i][t] * Bb[t][j] for t in range(r)) for j in range(n)]
             for i in range(n)]
        if rank_dense(A) != r:
            continue
        # kernel basis
        ker = []
        Mt = [list(row) for row in zip(*A)]
        # solve A x = 0 by rref on A
        M = [list(row) for row in A]
        piv, rr = [], 0
        for c in range(n):
            p = next((i for i in range(rr, n) if M[i][c]), None)
            if p is None:
                continue
            M[rr], M[p] = M[p], M[rr]
            v = M[rr][c]
            M[rr] = [x / v for x in M[rr]]
            for i in range(n):
                if i != rr and M[i][c]:
                    f = M[i][c]
                    M[i] = [a - f * b for a, b in zip(M[i], M[rr])]
            piv.append(c)
            rr += 1
        for f in [c for c in range(n) if c not in piv]:
            x = [Q(0)] * n
            x[f] = Q(1)
            for i, p in enumerate(piv):
                x[p] = -M[i][f]
            ker.append(x)
        # The bordered hypothesis is h(k)=0 for the ONE distinguished circuit
        # k, not h|ker(A)=0.  (h|ker(A)=0 implies h=lam*A at every corank --
        # that is the trivial fact and is NOT what the theorem uses.)
        kk = ker[0]
        h = None
        for _ in range(200):
            cand = [Q(random.randint(-3, 3)) for _ in range(n)]
            if sum(a * b for a, b in zip(cand, kk)) == 0 and any(cand):
                h = cand
                break
        if h is None:
            continue
        stats[target_corank][1] += 1
        # does h factor as lam * A ?
        aug = [[A[i][j] for i in range(n)] + [h[j]] for j in range(n)]
        rr2, piv2 = 0, []
        for c in range(n + 1):
            p = next((i for i in range(rr2, n) if aug[i][c]), None)
            if p is None:
                continue
            aug[rr2], aug[p] = aug[p], aug[rr2]
            v = aug[rr2][c]
            aug[rr2] = [x / v for x in aug[rr2]]
            for i in range(n):
                if i != rr2 and aug[i][c]:
                    f = aug[i][c]
                    aug[i] = [a - f * b for a, b in zip(aug[i], aug[rr2])]
            piv2.append(c)
            rr2 += 1
        if n not in piv2:
            stats[target_corank][0] += 1
report["bordered_factorization_corank_sensitivity"] = {
    "model": "random rank-deficient n=4 blocks A; ONE distinguished kernel vector k; random covector h with h(k)=0; does h=lam*A?",
    "per_corank": {str(k): {"trials": v[1], "factored": v[0],
                            "failure_rate": (f"{(v[1]-v[0])}/{v[1]}"
                                             if v[1] else "n/a")}
                   for k, v in stats.items()},
}

print(json.dumps(report, indent=2))
Path(__file__).with_name("out_b1.json").write_text(json.dumps(report, indent=2))
