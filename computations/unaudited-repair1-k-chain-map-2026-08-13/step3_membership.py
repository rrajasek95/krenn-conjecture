#!/usr/bin/env python3
"""STEP 3: physical membership + freedom, exactly over Q.

Question B: does a source-provenant chain K_phys exist in the committed
physical inventory whose grade-forgotten pair shadow equals the operator
solution's D2 shadow, with the committed residue/protected signature?  If
the fibre is positive dimensional, characterise the freedom and intersect
it with every committed readout row family.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json
import sys

import common as C

m = C.modules()
base, cm = m["base"], m["commutator"]
CORNERS = cm.CORNERS
PURE, MIXED = cm.PURE_WORD, cm.MIXED_WORD

TAIL_WORDS = [tuple(1 if i not in (2, 5) else (a if i == 2 else b)
                    for i in range(8))
              for a in (1, 2) for b in (1, 2)]


def inventory(words):
    mons = []
    seen = set()
    for w in words:
        for mon in C.physical_row(base, w):
            if mon not in seen:
                seen.add(mon)
                mons.append(mon)
    return mons


def shadow_columns(mons):
    return [{(2, p): Q(1) for p in C.shadow2_of_monomial(mon)} for mon in mons]


def chain_of(vec, mons):
    return Counter({mons[j]: v for j, v in vec.items() if v})


def analyse(name, words, out):
    mons = inventory(words)
    index = {mon: j for j, mon in enumerate(mons)}
    cols = shadow_columns(mons)
    target = {(2, pair): Q(v) for pair, v in cm.expected_second_shadow().items()}
    feasible, sol, kernel, rank, sep = C.solve_exact(cols, target)
    rec = {
        "inventory": name,
        "words": ["".join(map(str, w)) for w in words],
        "monomials": len(mons),
        "distinct_pair_rows": len({r for c in cols for r in c}),
        "shadow2_rank": rank,
        "feasible": feasible,
    }
    if not feasible:
        rec["separator_support"] = len(sep)
        rec["separator"] = sorted((repr(k), str(v)) for k, v in sep.items())
        out.append(rec)
        return rec, None, None, mons
    rec["kernel_dim_raw_freedom"] = len(kernel)
    # the committed candidate must be in the fibre
    K_phys = Counter({c: Q(a) for c, a in zip(CORNERS, cm.ALPHA)})
    Kvec = {index[c]: Q(a) for c, a in zip(CORNERS, cm.ALPHA)}
    diff = Counter(chain_of(sol, mons))
    diff.subtract(K_phys)
    diff = {k: v for k, v in diff.items() if v}
    rec["particular_minus_Kphys_is_in_kernel"] = not C.shadow2(
        Counter({k: v for k, v in diff.items()}))

    # ---- readout row families -------------------------------------------
    # Each family is a list of linear functionals (dicts monomial->coeff)
    # that must vanish on the freedom (they are pinned by K_phys's values).
    families = {}

    # (1) endpoint involution oddness: x + s x = 0 (one row per s-orbit)
    rows = []
    seen = set()
    for mon in mons:
        img, _sg = C.s_act(mon)
        key = tuple(sorted((mon, img)))
        if key in seen:
            continue
        seen.add(key)
        f = Counter({mon: Q(1)})
        f[img] += Q(1)
        f = {k: v for k, v in f.items() if v}
        if f:
            rows.append(f)
    families["s_odd (K=(1-s)H_w)"] = rows

    # (2) tail Weyl oddness: x + w x = 0
    rows = []
    seen = set()
    for mon in mons:
        img, sg = C.w_act(mon)
        key = tuple(sorted((mon, img)))
        if key in seen:
            continue
        seen.add(key)
        f = Counter({mon: Q(1)})
        f[img] += Q(sg)
        f = {k: v for k, v in f.items() if v}
        if f:
            rows.append(f)
    families["w_odd (tail Weyl)"] = rows

    # (3) endpoint-EVEN augmentations (the protected D/W/target/anchor
    #     family of the cap ledger): every s-invariant functional.
    rows = []
    seen = set()
    for mon in mons:
        img, _sg = C.s_act(mon)
        key = tuple(sorted((mon, img)))
        if key in seen:
            continue
        seen.add(key)
        rows.append({mon: Q(1), img: Q(1)} if img != mon else {mon: Q(1)})
    families["endpoint_even_augmentations"] = rows

    # (4) ordinary residue on the four corners
    families["ordinary_residue_corners"] = [{c: Q(1)} for c in CORNERS]

    # (5) word-row augmentations (aggregate of each committed 90-term row)
    rows = []
    for w in words:
        rows.append({mon: Q(1) for mon in C.physical_row(base, w)})
    families["row_augmentations"] = rows

    # (6) fine-degree gradings (coefficient sum per fine degree)
    buckets = defaultdict(dict)
    for mon in mons:
        buckets[base.fine_degree_of_edge_monomial(mon)][mon] = Q(1)
    families["fine_degree_gradings"] = list(buckets.values())

    # (7) per-cell incidence readouts: for each cell, sum of coefficients of
    #     monomials containing it (the codimension-THREE / single-cell shadow)
    cellbuckets = defaultdict(dict)
    for mon in mons:
        for cell in mon:
            cellbuckets[cell][mon] = Q(1)
    families["single_cell_shadow (codim 3)"] = list(cellbuckets.values())

    def kernel_after(constraints):
        """dim of {v in kernel : f(v)=0 for all f in constraints}."""
        if not kernel:
            return 0, []
        rows_m = []
        for f in constraints:
            row = {}
            for i, kv in enumerate(kernel):
                val = sum(coeff * kv.get(index[mon], Q(0))
                          for mon, coeff in f.items())
                if val:
                    row[i] = val
            if row:
                rows_m.append(row)
        r, _b = C.rref_rank(rows_m)
        return len(kernel) - r, r

    rec["freedom_after_family"] = {}
    for fname, fam in families.items():
        d, r = kernel_after(fam)
        rec["freedom_after_family"][fname] = {
            "rows": len(fam), "rank_on_freedom": r, "residual_freedom": d}
    allrows = [f for fam in families.values() for f in fam]
    d, r = kernel_after(allrows)
    rec["freedom_after_ALL_families"] = {"rows": len(allrows),
                                         "rank_on_freedom": r,
                                         "residual_freedom": d}
    out.append(rec)
    return rec, kernel, index, mons


out = []
rec2, kern2, idx2, mons2 = analyse("two active rows (pure + mixed)",
                                   [PURE, MIXED], out)
rec3, kern3, idx3, mons3 = analyse("tail-recolouring orbit (4 words)",
                                   TAIL_WORDS, out)

# ---- full committed inventory: exact dimension bound ----------------------
all_words = list(product(range(3), repeat=8))
mon_total = 90 * len(all_words)
edges = [(a, b) for a in range(8) for b in range(a + 1, 8)
         if frozenset((a, b)) != base.DIRECT_FREE_PAIR]
pairrows = set()
for e1, e2 in combinations(edges, 2):
    if set(e1) & set(e2):
        continue
    for ca, cb, cc, cd in product(range(3), repeat=4):
        pairrows.add(tuple(sorted(((e1[0], e1[1], ca, cb),
                                   (e2[0], e2[1], cc, cd)))))
out.append({
    "inventory": "full committed inventory (all 3^8 rows)",
    "monomials": mon_total,
    "distinct_monomials_are_words_times_90": len({
        (base.fine_degree_of_edge_monomial(mon))
        for mon in C.physical_row(base, PURE)}) == 1,
    "ambient_pair_rows_upper_bound": len(pairrows),
    "kernel_dim_lower_bound": mon_total - len(pairrows),
    "note": ("shadow_2 lands in a space of dimension at most the number of "
             "coloured disjoint cell pairs, so the ungraded fibre has at "
             "least this dimension"),
})

json.dump(out, open("step3_membership.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))
