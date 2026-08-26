#!/usr/bin/env python3
"""UNAUDITED PROBE (W19-CENSUS) -- verification of the machinery + controls.

UNAUDITED.  Nothing here is a proved claim of the repository.

Checks, in order:
  V1  my_fibre (independent PM enumeration) == len(w19_core.support) on ALL
      6561 words for a battery of templates            [the reformulation]
  V2  my_sc_ok (token calculus) == w19_core.sc_ok       [the (SC) calculus]
  V3  my_in_R == w19_core.in_R == fast_in_R (numpy int)
  V4  MUTATION CONTROLS: four deliberate corruptions, each REQUIRED to break
      the corresponding agreement.
  V5  EQUIVARIANCE: site permutations S_8, global colour permutations S_3,
      and per-site colour permutations S_3^8 -- which of them preserve (R)?
  V6  EXPLICIT-POINT CONTROL: the cubic-skeleton construction really lands
      in (R), and the SC-completion counting formula agrees with brute force
      on small sub-problems.
"""
from __future__ import annotations

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, FULL, N, WORDS, MIXED, CONSTS, W8_IMMUNE, NE,
    support, sc_ok, in_R, spanning_2conn, block_class, cells_of,
    my_fibre, my_sc_ok, my_in_R, my_tokens, my_npm_graph,
    fast_in_R, fibres_all_words, fast_audit,
    apply_site_perm, apply_colour_perms, S3, count_sc_completions,
    edges_to_mask, graph_canon, graph_aut, pms_inside,
)
from itertools import permutations, product  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = {}
FAIL = []


def check(name, cond, extra=None):
    R[name] = bool(cond)
    if extra is not None:
        R[name + "_detail"] = extra
    if not cond:
        FAIL.append(name)
    print(("  OK  " if cond else "  FAIL") + "  " + name +
          ("" if extra is None else "   " + str(extra)[:160]), flush=True)


# --------------------------------------------------------------- fixtures --
CUBE = [(0, 4), (1, 5), (2, 6), (3, 7), (0, 5), (1, 6), (2, 7), (3, 4),
        (0, 6), (1, 7), (2, 4), (3, 5)]


def incidences(C):
    inc = {v: [] for v in range(N)}
    for e in C:
        u, v = min(e), max(e)
        inc[u].append((u, v))
        inc[v].append((u, v))
    return inc


def build_cubic_template(C, sigma, gamma_edges_list=None):
    """sigma[v] : dict edge -> colour, a bijection on the 3 edges at v.
    The colour sigma[v][e] is the colour that v SEES through e (the token
    a_v).  Cell of e=(u,v) is then (i,j) = (sigma[v][e], sigma[u][e])."""
    T = [0] * NE
    for e in C:
        u, v = min(e), max(e)
        i = sigma[v][(u, v)]
        j = sigma[u][(u, v)]
        T[EIDX[(u, v)]] = 1 << (3 * i + j)
    if gamma_edges_list is None:
        Cs = set((min(a, b), max(a, b)) for (a, b) in C)
        gamma_edges_list = [e for e in EDGES if e not in Cs]
    for (u, v) in gamma_edges_list:
        T[EIDX[(min(u, v), max(u, v))]] = FULL
    return T


def diag_sigma(C, chi):
    """chi: dict edge -> colour, a proper 3-edge-colouring; the diagonal case."""
    inc = incidences(C)
    return {v: {e: chi[e] for e in inc[v]} for v in range(N)}


def proper_colouring(C):
    C = [(min(u, v), max(u, v)) for (u, v) in C]
    inc = incidences(C)
    col = {}
    def rec(i):
        if i == len(C):
            return dict(col)
        e = C[i]
        used = set()
        for x in e:
            for f in inc[x]:
                if f in col:
                    used.add(col[f])
        for c in range(3):
            if c in used:
                continue
            col[e] = c
            r = rec(i + 1)
            if r is not None:
                return r
            del col[e]
        return None
    return rec(0)


def random_sigma(C, rng):
    inc = incidences(C)
    return {v: dict(zip(inc[v], rng.sample([0, 1, 2], 3))) for v in range(N)}


rng = random.Random(20260815)

FIXTURES = []
for m, T in W8_IMMUNE.items():
    FIXTURES.append(("W8_m%d" % m, list(T)))
chi = proper_colouring(CUBE)
FIXTURES.append(("cube_diag", build_cubic_template(CUBE, diag_sigma(CUBE, chi))))
for k in range(4):
    FIXTURES.append(("cube_rand%d" % k,
                     build_cubic_template(CUBE, random_sigma(CUBE, rng))))
for k in range(20):
    FIXTURES.append(("rand%d" % k, [rng.randrange(512) for _ in range(NE)]))
for k in range(10):
    T = [rng.choice([0, FULL, 1 << rng.randrange(9)]) for _ in range(NE)]
    FIXTURES.append(("randstruct%d" % k, T))

print("fixtures:", len(FIXTURES), flush=True)

# --------------------------------------------------------------------- V1 --
bad = []
for nm, T in FIXTURES[:8]:
    for w in WORDS:
        a = len(support(T, w))
        b = my_fibre(T, w)
        if a != b:
            bad.append((nm, w, a, b))
            break
check("V1_fibre_reformulation_all_words", not bad, bad[:3])

bad = []
for nm, T in FIXTURES:
    f = fibres_all_words(T)
    for wi in rng.sample(range(6561), 60):
        if int(f[wi]) != len(support(T, WORDS[wi])):
            bad.append((nm, wi))
check("V1b_numpy_fibre_bank_matches_support", not bad, bad[:3])

# --------------------------------------------------------------------- V2 --
bad = []
for nm, T in FIXTURES:
    if my_sc_ok(T) != sc_ok(T):
        bad.append(nm)
check("V2_token_calculus_matches_sc_ok", not bad, bad[:5])

# every mask on one edge, all other edges arranged to serve everything
bad = []
for mask in range(512):
    tk = my_tokens(mask)
    cs = cells_of(mask)
    cols = set(j for _, j in cs)
    rows = set(i for i, _ in cs)
    want = (next(iter(cols)) if len(cols) == 1 else None,
            next(iter(rows)) if len(rows) == 1 else None)
    if tk != want:
        bad.append(mask)
    # cross-check against w19_core.far_thin_colour on edge (0,1)
    from w19_core import far_thin_colour
    if tk[0] != far_thin_colour(mask, at_second=True):
        bad.append(("u", mask))
    if tk[1] != far_thin_colour(mask, at_second=False):
        bad.append(("v", mask))
check("V2b_tokens_vs_far_thin_colour_all_512_masks", not bad, bad[:5])

# taxonomy: #demands served by class
tally = {}
for mask in range(512):
    k = sum(1 for t in my_tokens(mask) if t is not None)
    tally.setdefault(block_class(mask), set()).add(k)
check("V2c_taxonomy_single2_thin1_fat0",
      tally.get("single") == {2} and tally.get("thin") == {1}
      and tally.get("fat") == {0} and tally.get("full") == {0}
      and tally.get("zero") == {0},
      {k: sorted(v) for k, v in tally.items()})

# --------------------------------------------------------------------- V3 --
bad = []
for nm, T in FIXTURES:
    a, b, c = in_R(T), my_in_R(T), fast_in_R(T)
    if not (a == b == c):
        bad.append((nm, a, b, c))
check("V3_in_R_three_implementations_agree", not bad, bad[:5])
R["V3_in_R_true_fixtures"] = sorted(nm for nm, T in FIXTURES if fast_in_R(T))

# --------------------------------------------------------------------- V4 --
# mutation 1: swap the two token coordinates
def mut_tokens(mask):
    a, b = my_tokens(mask)
    return (b, a)


def mut_sc_ok(T):
    have = [set() for _ in range(N)]
    for ei, (u, v) in enumerate(EDGES):
        au, av = mut_tokens(T[ei])
        if au is not None:
            have[u].add(au)
        if av is not None:
            have[v].add(av)
    return all(len(s) == 3 for s in have)


diff = sum(1 for nm, T in FIXTURES if mut_sc_ok(T) != sc_ok(T))
check("V4a_mutation_swapped_tokens_DISAGREES", diff > 0, diff)

# mutation 2: drop one perfect matching from the PM bank
import numpy as np  # noqa: E402
import w19c_lib as L  # noqa: E402
saveP = L.PM_EMASK.copy()
L.PM_EMASK = saveP[:-1].copy()
diff = 0
for nm, T in FIXTURES[:14]:
    f = L.fibres_all_words(T)
    for wi in range(0, 6561, 97):
        if int(f[wi]) != len(support(T, WORDS[wi])):
            diff += 1
L.PM_EMASK = saveP
check("V4b_mutation_dropped_matching_DISAGREES", diff > 0, diff)

# mutation 3: transpose the cell index (row<->col) in the fibre bank
saveC = L.CELLI.copy()
L.CELLI = (saveC % 3) * 3 + (saveC // 3)
diff = 0
for nm, T in FIXTURES[:14]:
    f = L.fibres_all_words(T)
    for wi in range(0, 6561, 53):
        if int(f[wi]) != len(support(T, WORDS[wi])):
            diff += 1
L.CELLI = saveC
check("V4c_mutation_transposed_cells_DISAGREES", diff > 0, diff)

# mutation 4: corrupt ONE cell of a known (R) member and require it to leave
# (R) (the predicate must actually depend on every cell it claims to).
T_ok = build_cubic_template(CUBE, diag_sigma(CUBE, chi))
assert in_R(T_ok)   # pure w19_core call, once
leaves = 0
tried = 0
for ei in range(NE):
    for bit in range(9):
        T2 = list(T_ok)
        T2[ei] ^= (1 << bit)
        tried += 1
        if not fast_in_R(T2):
            leaves += 1
check("V4d_mutation_single_cell_flips_leave_R", leaves > 0,
      "%d of %d single-cell flips leave (R)" % (leaves, tried))

# --------------------------------------------------------------------- V5 --
# equivariance of in_R under the three candidate groups
def orbit_test(T, kind, trials=40):
    outs = []
    for _ in range(trials):
        if kind == "site":
            p = list(range(N))
            rng.shuffle(p)
            T2 = apply_site_perm(T, tuple(p))
        elif kind == "gcol":
            pi = rng.choice(S3)
            T2 = apply_colour_perms(T, [pi] * N)
        else:
            T2 = apply_colour_perms(T, [rng.choice(S3) for _ in range(N)])
        outs.append(fast_in_R(T2))
    return outs


posT = [T for nm, T in FIXTURES if fast_in_R(T)]
R["n_positive_fixtures"] = len(posT)
for kind in ("site", "gcol", "persite"):
    allsame = True
    counter = None
    for T in posT:
        o = orbit_test(T, kind)
        if not all(o):
            allsame = False
            counter = (kind, sum(o), len(o))
            break
    check("V5_%s_preserves_R" % kind, allsame, counter)

# exhaustive per-site check on ONE positive template: all 6^8 too many; do
# all 6 permutations at a single site, for each site.
if posT:
    T0 = posT[0]
    tbl = {}
    for p in range(N):
        cnt = 0
        for pi in S3:
            pis = [tuple(range(3))] * N
            pis = list(pis)
            pis[p] = pi
            if fast_in_R(apply_colour_perms(T0, pis)):
                cnt += 1
        tbl[p] = cnt
    R["V5_single_site_colour_perm_preserving_count"] = tbl
    print("   single-site colour perms preserving (R):", tbl, "(out of 6 each)")

# --------------------------------------------------------------------- V6 --
# EXPLICIT-POINT CONTROL for the counting formula: brute force the number of
# (SC)-admissible completions on a SMALL sub-problem (a template where all
# but k edges are pinned) and compare with the closed form on that instance.
def brute_sc_count_small(free_edges, fixed):
    """fixed: dict edge_index -> mask for every edge NOT in free_edges."""
    tot = 0
    for combo in product(range(511), repeat=len(free_edges)):
        T = [0] * NE
        for ei, m in fixed.items():
            T[ei] = m
        for ei, m in zip(free_edges, combo):
            T[ei] = m
        if my_sc_ok(T):
            tot += 1
    return tot


# mask-token census (the four numbers in sc_mask_count), brute forced
cnt = {"single": 0, "colthin": 0, "rowthin": 0, "none": 0}
for m in range(511):
    au, av = my_tokens(m)
    if au is not None and av is not None:
        cnt["single"] += 1
    elif au is not None:
        cnt["colthin"] += 1
    elif av is not None:
        cnt["rowthin"] += 1
    else:
        cnt["none"] += 1
check("V6_mask_token_census_9_12_12_478",
      cnt == {"single": 9, "colthin": 12, "rowthin": 12, "none": 478}, cnt)

# per (a_u,a_v) refinement: exactly 1 mask per (i,j); 4 per column; 4 per row
per = {}
for m in range(511):
    per[my_tokens(m)] = per.get(my_tokens(m), 0) + 1
ok = all(per[(j, i)] == 1 for i in range(3) for j in range(3))
ok = ok and all(per[(j, None)] == 4 for j in range(3))
ok = ok and all(per[(None, i)] == 4 for i in range(3))
ok = ok and per[(None, None)] == 478
check("V6a_mask_token_refined_counts", ok,
      {str(k): v for k, v in sorted(per.items(), key=lambda t: str(t[0]))})

# the closed form sc_mask_count(k_u,k_v) must equal a brute-force count
from w19c_lib import sc_mask_count  # noqa: E402
bad = []
for ku in range(4):
    for kv in range(4):
        Au = set(range(ku))          # colours a_u is allowed to take
        Av = set(range(kv))
        bf2 = 0
        for m in range(511):
            au, av = my_tokens(m)
            if (au is None or au in Au) and (av is None or av in Av):
                bf2 += 1
        if bf2 != sc_mask_count(ku, kv):
            bad.append((ku, kv, bf2, sc_mask_count(ku, kv)))
check("V6b0_sc_mask_count_closed_form", not bad, bad)

# real control: count completions on a 1-edge-free instance both ways
fixed = {}
Tbase = build_cubic_template(CUBE, diag_sigma(CUBE, chi))
for ei in range(NE):
    fixed[ei] = Tbase[ei]
freei = EIDX[(0, 4)]
del fixed[freei]
bf = 0
for m in range(511):
    T = [0] * NE
    for ei, mm in fixed.items():
        T[ei] = mm
    T[freei] = m
    if my_sc_ok(T):
        bf += 1
# closed form: edge (0,4) must supply token a_0 = sigma[0][(0,4)] and
# a_4 = sigma[4][(0,4)] (both demands are otherwise unmet) -> exactly the
# single cell, i.e. 1 mask.
check("V6b_one_free_edge_count", bf == 1, bf)

# EXPLICIT-POINT CONTROL: known (R) member found by the search machinery
Tpt = build_cubic_template(CUBE, diag_sigma(CUBE, chi))
a = fast_audit(Tpt)
check("V6c_explicit_point_cube_in_R", a["in_R"], a)

json.dump(R, open(os.path.join(HERE, "results_verify.json"), "w"), indent=1)
print("\nFAILURES:", FAIL if FAIL else "none")
