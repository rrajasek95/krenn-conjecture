#!/usr/bin/env python3
"""UNAUDITED REPAIR PROBE -- item 4 (A-I / A-III).

Pinned HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d (snapshot via git archive).

A-I  Literal readout of every column of the canonical faces-(3,5) repeated
     component on the rows that actually exist literally: the six selected
     private matching features (-> lower_B) and the pure-aggregate marker
     (-> ainc).  Answers: which 25-row-model columns are literally realized,
     and how many literal columns are invisible to (lower, ainc).

A-III Realized symmetry group.  A site permutation is an automorphism of the
     direct-free matching presentation iff it preserves DIRECT_FREE_PAIR
     {3,6}; it stays inside the canonical grade iff it preserves the fine
     target degree.  We verify full_row equivariance LITERALLY on all 3^8
     words for every candidate, then read off the induced permutation of the
     six pure multiplier labels B_0..B_5.  This bounds the orbit of the one
     physically constructed Cartan residue placement.
"""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path

SNAP = Path("/private/tmp/claude-501/-Users-rishi/f8396279-dd28-41de-876d-5c03a4d8d65a/scratchpad/repair45/snap")
HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, SNAP / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load("computations/verify_h3_direct_free_complete_first_fine_degree_membership.py", "b")
complete = load("computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py", "c")
absolute = load("computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py", "a")

left, right, left_cell, _ = complete.CUBIC_PAIRS[1]
td = complete.degree_add(base.lambda_degree(left),
                         complete.cell_degree(complete.CYCLE_CELLS[left_cell]))
comp = complete.component(base, td)
pure_indices, selected = absolute.selected_private_features(comp)
pure_labels = [comp["columns"][i][1] for i in pure_indices]

report = {"head": HEAD, "faces": [left, right], "target_degree": list(td)}

# ---------------------------------------------------------------- A-I
# Bridge sign convention (verify_h3_first_flat_endpoint_bridge.py:455,458):
#   column[(3, monomial)] = -1 for each boundary monomial
#   column[(4, "pure_aggregate")] = +1 iff word == PURE_WORD
# Dichotomy identification: lower_B = -(selected feature readout),
#   ainc = -(pure aggregate readout).
readouts = Counter()
per_column = []
for index, (word, multiplier, boundary) in enumerate(comp["columns"]):
    features = tuple(-1 if f in set(boundary) else 0 for f in selected)
    pure_aggregate = 1 if word == complete.PURE_WORD else 0
    lower = tuple(-v for v in features)
    ainc = -pure_aggregate
    nu = sum(lower) + ainc
    per_column.append((index, lower, ainc, nu))
    readouts[(lower, ainc)] += 1
report["A_I_literal_readout"] = {
    "columns": len(comp["columns"]),
    "distinct_(lower,ainc)_readouts": {
        f"lower={list(k[0])},ainc={k[1]}": v for k, v in
        sorted(readouts.items(), key=lambda kv: (-kv[1], repr(kv[0])))},
    "nu_values": sorted({c[3] for c in per_column}),
    "columns_invisible_to_lower_and_ainc":
        sum(1 for _, lower, ainc, _ in per_column if not any(lower) and not ainc),
    "columns_equal_to_r0_j": sum(1 for _, lower, ainc, _ in per_column
                                 if sum(lower) == 1 and ainc == -1),
}

# ---------------------------------------------------------------- A-III
DIRECT_FREE = set(base.DIRECT_FREE_PAIR)


def permute_cell(cell, sigma):
    l, r, a, b = cell
    l, r = sigma[l], sigma[r]
    if l < r:
        return (l, r, a, b)
    return (r, l, b, a)


def permute_monomial(monomial, sigma):
    return tuple(sorted(permute_cell(c, sigma) for c in monomial))


def permute_word(word, sigma):
    out = [0] * 8
    for site, colour in enumerate(word):
        out[sigma[site]] = colour
    return tuple(out)


def preserves_degree(sigma):
    for site in range(8):
        for colour in range(3):
            if td[3 * sigma[site] + colour] != td[3 * site + colour]:
                return False
    return True


# Candidate automorphisms: permutations of the 8 sites preserving {3,6}
# setwise (the direct-free forbidden pair) AND the canonical fine degree.
candidates = []
for perm in permutations(range(8)):
    sigma = list(perm)
    if {sigma[s] for s in DIRECT_FREE} != DIRECT_FREE:
        continue
    if not preserves_degree(sigma):
        continue
    candidates.append(tuple(sigma))

# Literal equivariance check on ALL 3^8 words (the same census the committed
# Cartan-descent checker runs for the single swap 0<->1).
verified = []
for sigma in candidates:
    ok = True
    for word in product(range(3), repeat=8):
        transported = Counter(permute_monomial(m, sigma) for m in base.full_row(word))
        if transported != Counter(base.full_row(permute_word(word, sigma))):
            ok = False
            break
    if ok:
        verified.append(sigma)

pure_set = {m: j for j, m in enumerate(pure_labels)}
label_perms = {}
for sigma in verified:
    images = []
    for m in pure_labels:
        image = permute_monomial(m, sigma)
        images.append(pure_set.get(image))
    label_perms[sigma] = tuple(images)

report["A_III_symmetry"] = {
    "direct_free_pair": sorted(DIRECT_FREE),
    "site_permutations_preserving_pair_and_grade": len(candidates),
    "of_those_literally_equivariant_on_all_6561_words": len(verified),
    "verified_site_permutations": [list(s) for s in verified],
    "induced_label_permutations": {
        str(list(s)): (list(p) if all(x is not None for x in p)
                       else "leaves the six pure labels")
        for s, p in label_perms.items()},
}

# The rho / target action the dichotomy uses on the six labels.
report["A_III_symmetry"]["dichotomy_TARGET_ACTION"] = list((5, 1, 3, 2, 4, 0))
report["A_III_symmetry"]["TARGET_ACTION_realized_by_a_site_automorphism"] = any(
    p == (5, 1, 3, 2, 4, 0) for p in label_perms.values())

print(json.dumps(report, indent=2, sort_keys=False))
Path(__file__).with_name("out_a1.json").write_text(json.dumps(report, indent=2))
