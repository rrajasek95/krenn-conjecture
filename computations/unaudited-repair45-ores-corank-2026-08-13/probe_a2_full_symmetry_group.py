#!/usr/bin/env python3
"""UNAUDITED REPAIR PROBE -- item 4 (A-III, complete).

Pinned HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d.

Largest symmetry group of the COMMITTED literal presentation fixing the
canonical faces-(3,5) fine degree: pairs (sigma,tau), sigma a site
permutation preserving DIRECT_FREE_PAIR={3,6} setwise, tau a per-site colour
relabelling, with td[3*sigma(s)+tau_s(c)] == td[3*s+c] for all s,c.

Equivariance of base.full_row is checked in two exact pieces:
 (i)  m -> sigma(m) is a bijection of the 90 direct-free matchings  (ALL
      group elements);
 (ii) act_monomial(matching_monomial(m,word)) ==
      matching_monomial(sigma(m), act_word(word))  -- verified on ALL 3^8
      words for the generating set and a random control sample.

Then: the subgroup fixing the pure word, its induced permutation action on
the six pure multiplier labels, and the resulting orbit span of the one
physically constructed endpoint-odd Cartan residue placement.
"""
from __future__ import annotations

import importlib.util
import json
import random
from collections import Counter
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

left, right, left_cell, _ = complete.CUBIC_PAIRS[1]
td = complete.degree_add(base.lambda_degree(left),
                         complete.cell_degree(complete.CYCLE_CELLS[left_cell]))
comp = complete.component(base, td)
pure_indices, selected = absolute.selected_private_features(comp)
pure_labels = [comp["columns"][i][1] for i in pure_indices]
pure_index_of = {m: j for j, m in enumerate(pure_labels)}
DIRECT_FREE = set(base.DIRECT_FREE_PAIR)

DIRECT_FREE_MATCHINGS = tuple(
    m for m in base.matchings(base.ALL_SITES)
    if not any(frozenset(p) == base.DIRECT_FREE_PAIR for p in m))
assert len(DIRECT_FREE_MATCHINGS) == 90


def act_cell(cell, sigma, tau):
    l, r, a, b = cell
    l2, a2 = sigma[l], tau[l][a]
    r2, b2 = sigma[r], tau[r][b]
    return (l2, r2, a2, b2) if l2 < r2 else (r2, l2, b2, a2)


def act_monomial(mon, sigma, tau):
    return tuple(sorted(act_cell(c, sigma, tau) for c in mon))


def act_word(word, sigma, tau):
    out = [0] * 8
    for s, c in enumerate(word):
        out[sigma[s]] = tau[s][c]
    return tuple(out)


def act_matching(m, sigma):
    return tuple(sorted(tuple(sorted((sigma[a], sigma[b]))) for a, b in m))


# ---- build the group -------------------------------------------------
colour_perms = list(permutations(range(3)))
group = []
for perm in permutations(range(8)):
    sigma = tuple(perm)
    if {sigma[s] for s in DIRECT_FREE} != DIRECT_FREE:
        continue
    per_site = []
    ok = True
    for s in range(8):
        good = [t for t in colour_perms
                if all(td[3 * sigma[s] + t[c]] == td[3 * s + c] for c in range(3))]
        if not good:
            ok = False
            break
        per_site.append(good)
    if not ok:
        continue
    for tau in product(*per_site):
        group.append((sigma, tuple(tau)))

# ---- (i) matching bijection, ALL elements ----------------------------
canonical = {tuple(sorted(tuple(sorted(p)) for p in m)) for m in DIRECT_FREE_MATCHINGS}
bijection_failures = 0
for sigma, _ in group:
    images = {act_matching(m, sigma) for m in DIRECT_FREE_MATCHINGS}
    if len(images) != 90 or images != canonical:
        bijection_failures += 1

# ---- (ii) full literal equivariance on all 3^8 words, sampled elements
random.seed(20260813)
sample = group[:1] + [g for g in group if g[0] != group[0][0]][:3] + random.sample(group, 6)
equivariance_failures = 0
words_checked = 0
for sigma, tau in sample:
    for word in product(range(3), repeat=8):
        got = Counter(act_monomial(m, sigma, tau) for m in base.full_row(word))
        if got != Counter(base.full_row(act_word(word, sigma, tau))):
            equivariance_failures += 1
            break
        words_checked += 1

# ---- pure-word stabilizer and induced label action -------------------
pure_word = complete.PURE_WORD
stab = [(s, t) for s, t in group if act_word(pure_word, s, t) == pure_word]
label_images = {}
leaves_pure_set = 0
for sigma, tau in stab:
    img = tuple(pure_index_of.get(act_monomial(m, sigma, tau)) for m in pure_labels)
    if any(x is None for x in img):
        leaves_pure_set += 1
        continue
    label_images.setdefault(img, 0)
    label_images[img] += 1

TARGET_ACTION = (5, 1, 3, 2, 4, 0)

# ---- orbit of the physically constructed Cartan residue placement ----
# scope guard's literal placement of the endpoint-odd Cartan residue
CARTAN_LINE = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
DIAGONAL = (Q(1),) * 6
# the dichotomy's own convention: ALPHA=(-1,1,1,-1) placed in increasing
# label order on a 4-subset
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))


def apply_label_perm(vector, perm):
    out = [Q(0)] * 6
    for i, v in enumerate(vector):
        out[perm[i]] += v
    return tuple(out)


def rank(vectors):
    rows = [list(v) for v in vectors]
    piv = 0
    for col in range(6):
        p = next((r for r in range(piv, len(rows)) if rows[r][col]), None)
        if p is None:
            continue
        rows[piv], rows[p] = rows[p], rows[piv]
        val = rows[piv][col]
        rows[piv] = [x / val for x in rows[piv]]
        for r in range(len(rows)):
            if r != piv and rows[r][col]:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[piv])]
        piv += 1
    return piv


orbit = {apply_label_perm(CARTAN_LINE, p) for p in label_images}
span_basis = list(orbit) + [DIAGONAL]
candidates = {
    "fixed_B1": tuple(Q(int(i == 1)) for i in range(6)),
    "fixed_B4": tuple(Q(int(i == 4)) for i in range(6)),
    "paired_B0_B5": tuple(Q(int(i in (0, 5)), 2) for i in range(6)),
    "paired_B2_B3": tuple(Q(int(i in (2, 3)), 2) for i in range(6)),
}
membership = {n: rank(span_basis) == rank(span_basis + [c])
              for n, c in candidates.items()}

# all 15 alpha placements, for comparison (the dichotomy's generous grant)
all_placements = []
for sel in permutations(range(6), 4):
    if list(sel) != sorted(sel):
        continue
    vec = [Q(0)] * 6
    for a, i in zip(ALPHA, sel):
        vec[i] += a
    all_placements.append(tuple(vec))

report = {
    "head": HEAD,
    "group": {
        "order_(sigma,tau)_preserving_presentation_and_canonical_grade": len(group),
        "matching_bijection_failures_all_elements": bijection_failures,
        "literal_full_row_equivariance_elements_sampled": len(sample),
        "literal_full_row_words_checked": words_checked,
        "literal_full_row_equivariance_failures": equivariance_failures,
    },
    "pure_word_stabilizer_order": len(stab),
    "stabilizer_elements_leaving_the_pure_label_set": leaves_pure_set,
    "induced_label_permutations": {str(list(k)): v for k, v in
                                   sorted(label_images.items(), key=repr)},
    "induced_label_group_order": len(label_images),
    "TARGET_ACTION_is_induced": TARGET_ACTION in label_images,
    "cartan_orbit": {
        "physical_placement_scope_guard": [str(x) for x in CARTAN_LINE],
        "orbit_size": len(orbit),
        "orbit": [[str(x) for x in v] for v in sorted(orbit, key=repr)],
        "rank_of_span(orbit + diagonal)": rank(span_basis),
        "rank_of_span(all_15_alpha_placements + diagonal)":
            rank(all_placements + [DIAGONAL]),
        "rank_of_span(all_15_alpha_placements)": rank(all_placements),
    },
    "repair_direction_in_physical_ores_span": membership,
}
print(json.dumps(report, indent=2))
Path(__file__).with_name("out_a2.json").write_text(json.dumps(report, indent=2))
