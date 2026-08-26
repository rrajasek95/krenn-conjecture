#!/usr/bin/env python3
"""A7 SUB-AUDIT -- ITEM B: the L-FREE / R-FREE reduction on the C_8 member.

W20's claim (REPORT.md):
  "L-FREE/R-FREE REDUCTION [proved, 0/4,860 mismatches]: 30 L-free words x 81
   (and mirror) give H = per B(x,y) -- 3,960 of 6,558 mixed equations are PURE
   4x4 PERMANENT conditions on the 16 cross blocks; the 12 single cells drop
   out."

MODEL (re-implemented here from the definition, NOT imported from W20):
  N = 8 sites, 28 edges = itertools.combinations(range(8),2) in lex order.
  A template T is 28 nine-bit masks; bit 3*i+j of T[e] set <=> cell (i,j) of
  block A_e is occupied; for e = (u,v) with u < v the ROW index is the colour
  at u and the COLUMN index is the colour at v.
  H_w(A) = sum over the 105 perfect matchings M of K_8 all of whose cells are
  occupied at w, of prod_{uv in M} A_uv[w_u][w_v].

CLAIM UNDER TEST (B2): with L = {0,1,2,3}, R = {4,5,6,7} and x = w|_L,
y = w|_R, for every L-FREE x and EVERY y,
        H_(x,y)  ==  per B(x,y),   B(x,y)[a][b] = A_{L[a],R[b]}[x_a][y_b]
exactly (dead cross cells read as 0), and no intra-L / intra-R (single) cell
occurs in H.  Mirror statement for R-free y.

Everything below is exact: polynomials are dicts monomial -> integer
coefficient, values are Fractions.  No floats.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations, permutations, product

HERE = os.path.dirname(os.path.abspath(__file__))
W20 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                   "unaudited-lasttwo-w20-2026-08-15")

N = 8
Q = 3
FULLMASK = 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
L = (0, 1, 2, 3)
R = (4, 5, 6, 7)

# the C_8 member template, transcribed from w20_core.C8_MEMBER (data, not code)
C8 = (1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
      383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1)


# ------------------------------------------------------------ my engine ----
def all_perfect_matchings(vertices):
    """perfect matchings of the complete graph on `vertices` (my own
    recursion: always pair the smallest remaining vertex)."""
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for k in range(1, len(vertices)):
        b = vertices[k]
        rest = vertices[1:k] + vertices[k + 1:]
        for m in all_perfect_matchings(rest):
            yield ((a, b),) + m


PMS = tuple(tuple(sorted(m)) for m in all_perfect_matchings(tuple(range(N))))
PM_EDGE_IDS = tuple(tuple(EIDX[e] for e in m) for m in PMS)
WORDS = tuple(product(range(Q), repeat=N))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)


def cell_of(ei, w):
    u, v = EDGES[ei]
    return 3 * w[u] + w[v]


def occupied(T, ei, w):
    return (T[ei] >> cell_of(ei, w)) & 1


def support_ids(T, w):
    return [mi for mi, es in enumerate(PM_EDGE_IDS)
            if all((T[e] >> cell_of(e, w)) & 1 for e in es)]


def H_poly(T, w):
    """H_w as an exact polynomial: dict {frozenset of (edge,cell)} -> int."""
    out = {}
    for mi in support_ids(T, w):
        mon = tuple(sorted((e, cell_of(e, w)) for e in PM_EDGE_IDS[mi]))
        out[mon] = out.get(mon, 0) + 1
    return out


def H_value(T, w, vals):
    tot = Fraction(0)
    for mi in support_ids(T, w):
        p = Fraction(1)
        for e in PM_EDGE_IDS[mi]:
            p *= vals[(e, cell_of(e, w))]
        tot += p
    return tot


# SECOND, INDEPENDENT engine: subset DP over the 8 sites (hafnian style).
def H_value_dp(T, w, vals):
    """H_w by dynamic programming over subsets: pair the lowest free site
    with each other free site.  Never enumerates the 105 matchings."""
    memo = {}

    def rec_memo(mask):
        if mask in memo:
            return memo[mask]
        if mask == 0:
            return Fraction(1)
        lo = (mask & -mask).bit_length() - 1
        rest = mask & ~(1 << lo)
        tot = Fraction(0)
        m = rest
        while m:
            bit = m & -m
            j = bit.bit_length() - 1
            m ^= bit
            u, v = (lo, j) if lo < j else (j, lo)
            ei = EIDX[(u, v)]
            c = cell_of(ei, w)
            if (T[ei] >> c) & 1:
                tot += vals[(ei, c)] * rec_memo(rest & ~bit)
        memo[mask] = tot
        return tot

    return rec_memo((1 << N) - 1)


def block_class(mask):
    if mask == 0:
        return "zero"
    cs = [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]
    if len(cs) == 1:
        return "single"
    if mask == FULLMASK:
        return "full"
    rows = {i for i, _ in cs}
    cols = {j for _, j in cs}
    return "thin" if (len(rows) == 1 or len(cols) == 1) else "fat"


def gamma_edges(T):
    return [EDGES[i] for i, t in enumerate(T) if t == FULLMASK]


# ================================================================== B1 =====
def B1_engine_controls():
    out = {}
    out["n_edges"] = len(EDGES)
    out["edges_lex_ok"] = list(EDGES) == sorted(EDGES)
    out["n_perfect_matchings"] = len(PMS)
    out["pms_distinct"] = len(set(PMS)) == len(PMS)
    out["pms_are_perfect"] = all(
        sorted(v for e in m for v in e) == list(range(N)) for m in PMS)
    out["n_words"] = len(WORDS)
    out["n_mixed"] = len(MIXED)
    # my two engines must agree per word (all 6561 words, random values)
    rng = random.Random(4242)
    vals = {}
    for ei in range(len(EDGES)):
        for c in range(9):
            if (C8[ei] >> c) & 1:
                vals[(ei, c)] = Fraction(rng.randint(-9, 9) or 3,
                                         rng.randint(1, 5))
    dis = 0
    for w in WORDS:
        if H_value(C8, w, vals) != H_value_dp(C8, w, vals):
            dis += 1
    out["engineA_vs_engineB_per_word_mismatches"] = dis
    out["engineA_vs_engineB_words_compared"] = len(WORDS)
    # audit invariants of the C_8 member vs W20's stored numbers
    ge = gamma_edges(C8)
    fib = {w: len(support_ids(C8, w)) for w in WORDS}
    fullm = set(mi for mi, m in enumerate(PMS)
                if all(tuple(sorted(e)) in set(map(tuple, ge)) for e in m))
    khist = {}
    for w in MIXED:
        k = len([mi for mi in support_ids(C8, w) if mi not in fullm])
        khist[k] = khist.get(k, 0) + 1
    cls = {}
    for t in C8:
        cls[block_class(t)] = cls.get(block_class(t), 0) + 1
    mine = dict(m=sum(1 for t in C8 if t),
                sigma=sum(bin(t).count("1") for t in C8),
                n_gamma=len(ge), gamma=[list(e) for e in ge],
                n_F=len(fullm),
                F_matchings=[[list(e) for e in PMS[mi]] for mi in
                             sorted(fullm)],
                min_mixed_fibre=min(fib[w] for w in MIXED),
                max_mixed_fibre=max(fib[w] for w in MIXED),
                min_const_fibre=min(fib[(c,) * N] for c in range(Q)),
                total_fibre=sum(fib.values()),
                classes=cls,
                n_eff_clean=sum(1 for w in MIXED
                                if not [mi for mi in support_ids(C8, w)
                                        if mi not in fullm]),
                k_histogram_mixed={str(k): v for k, v in sorted(khist.items())})
    out["my_C8_audit"] = mine
    stored = json.load(open(os.path.join(W20, "results_controls.json")))
    st = stored["C2_c8_audit"]
    cmp_keys = ["m", "sigma", "n_gamma", "gamma", "n_F", "F_matchings",
                "min_mixed_fibre", "max_mixed_fibre", "min_const_fibre",
                "total_fibre", "classes", "n_eff_clean", "k_histogram_mixed"]
    diffs = {k: dict(mine=mine[k], w20=st[k]) for k in cmp_keys
             if mine[k] != st[k]}
    out["vs_W20_stored_C2"] = dict(compared=cmp_keys, n_disagreements=len(diffs),
                                   disagreements=diffs)
    out["hamilton_cycle_check"] = hamilton_order(ge)
    # a genuine per-word record: fibre sizes of 250 sampled words
    rs = random.Random(99)
    sample = rs.sample(list(WORDS), 250)
    out["per_word_fibre_sample_250"] = {
        "".join(map(str, w)): fib[w] for w in sample[:250]}
    out["per_word_khist_bins_matched"] = (
        mine["k_histogram_mixed"] == st["k_histogram_mixed"])
    out["words_constrained_by_khist"] = sum(st["k_histogram_mixed"].values())
    return out


def hamilton_order(ge):
    adj = {v: [] for v in range(N)}
    for u, v in ge:
        adj[u].append(v)
        adj[v].append(u)
    if any(len(a) != 2 for a in adj.values()):
        return dict(is_2_regular=False)
    order = [0, adj[0][0]]
    while len(order) < N:
        cur, prev = order[-1], order[-2]
        nxt = [z for z in adj[cur] if z != prev]
        order.append(nxt[0])
    closed = order[0] in adj[order[-1]]
    return dict(is_2_regular=True, cycle=order, closes=closed,
                is_hamilton_cycle=(closed and sorted(order) == list(range(N))))


# ================================================================== B2 =====
def singles_inside(T, side):
    out = {}
    for ei, (u, v) in enumerate(EDGES):
        if u in side and v in side and block_class(T[ei]) == "single":
            c = [c for c in range(9) if (T[ei] >> c) & 1][0]
            out[(u, v)] = (c // 3, c % 3)
    return out


def free_words(side, sing):
    pos = {s: k for k, s in enumerate(side)}
    out = []
    for z in product(range(Q), repeat=4):
        if all(not (z[pos[u]] == i and z[pos[v]] == j)
               for (u, v), (i, j) in sing.items()):
            out.append(z)
    return out


def cross_cells_live(T, a, b, xa, yb):
    return (T[EIDX[(L[a], R[b])]] >> (3 * xa + yb)) & 1


def perB_poly(T, x, y):
    """per B(x,y) as an exact polynomial (dict monomial -> int)."""
    out = {}
    for p in permutations(range(4)):
        mon = []
        ok = True
        for a in range(4):
            b = p[a]
            ei = EIDX[(L[a], R[b])]
            c = 3 * x[a] + y[b]
            if not (T[ei] >> c) & 1:
                ok = False
                break
            mon.append((ei, c))
        if ok:
            k = tuple(sorted(mon))
            out[k] = out.get(k, 0) + 1
    return out


def perB_value(T, x, y, vals):
    tot = Fraction(0)
    for p in permutations(range(4)):
        pr = Fraction(1)
        ok = True
        for a in range(4):
            b = p[a]
            ei = EIDX[(L[a], R[b])]
            c = 3 * x[a] + y[b]
            if not (T[ei] >> c) & 1:
                ok = False
                break
            pr *= vals[(ei, c)]
        if ok:
            tot += pr
    return tot


SINGLE_EDGE_IDS = None


def single_cell_keys(T):
    keys = []
    for ei, (u, v) in enumerate(EDGES):
        if (u in L) == (v in L) and block_class(T[ei]) == "single":
            c = [c for c in range(9) if (T[ei] >> c) & 1][0]
            keys.append((ei, c))
    return keys


def B2_reduction(T=C8):
    out = {}
    LS = singles_inside(T, L)
    RS = singles_inside(T, R)
    out["L_singles"] = {str(k): list(v) for k, v in LS.items()}
    out["R_singles"] = {str(k): list(v) for k, v in RS.items()}
    out["n_L_singles"] = len(LS)
    out["n_R_singles"] = len(RS)
    # is the single pattern the proper 3-edge-colouring, cell (r,r)?
    colouring = {}
    ok3 = True
    for (u, v), (i, j) in LS.items():
        if i != j:
            ok3 = False
        colouring[(u, v)] = i
    classes = {}
    for e, r in colouring.items():
        classes.setdefault(r, []).append(e)
    out["L_single_diagonal_and_3colouring"] = dict(
        all_cells_diagonal=ok3,
        classes={str(r): [list(e) for e in es] for r, es in classes.items()},
        is_perfect_matching_classes=all(
            sorted(v for e in es for v in e) == sorted(L)
            for es in classes.values()))
    LFREE = free_words(L, LS)
    RFREE = free_words(R, RS)
    out["n_Lfree"] = len(LFREE)
    out["n_Rfree"] = len(RFREE)
    out["Lfree_words"] = [list(x) for x in LFREE]
    stored = json.load(open(os.path.join(W20, "results_c8.json")))
    out["Lfree_matches_W20"] = (sorted(map(list, LFREE))
                                == sorted(stored["Lfree_words"]))
    out["Rfree_matches_W20"] = (sorted(map(list, RFREE))
                                == sorted(stored["Rfree_words"]))
    single_keys = set(single_cell_keys(T))
    out["n_single_cells"] = len(single_keys)

    # ---- the identity, as an EXACT POLYNOMIAL identity, on ALL pairs -------
    def run_side(freewords, side_is_L):
        tested = 0
        poly_mismatch = []
        noncross = []
        single_leak = []
        for z in freewords:
            for other in product(range(Q), repeat=4):
                x, y = (z, other) if side_is_L else (other, z)
                w = tuple(x) + tuple(y)
                tested += 1
                hp = H_poly(T, w)
                bp = perB_poly(T, x, y)
                if hp != bp:
                    poly_mismatch.append(dict(w=list(w), nH=len(hp),
                                              nB=len(bp)))
                for mi in support_ids(T, w):
                    if sum(1 for (u, v) in PMS[mi]
                           if (u in L) != (v in L)) != 4:
                        noncross.append(list(w))
                        break
                if any(k in single_keys for mon in hp for k in mon):
                    single_leak.append(list(w))
        return dict(tested=tested, polynomial_mismatches=len(poly_mismatch),
                    mismatch_samples=poly_mismatch[:5],
                    words_with_a_non_4cross_matching=len(noncross),
                    words_where_a_single_cell_occurs=len(single_leak))

    out["Lfree_identity_all_2430"] = run_side(LFREE, True)
    out["Rfree_identity_all_2430"] = run_side(RFREE, False)
    out["total_pair_tests"] = (out["Lfree_identity_all_2430"]["tested"]
                               + out["Rfree_identity_all_2430"]["tested"])

    # ---- numeric exact check at random rational assignments, >= 200 pairs --
    rng = random.Random(20260815)
    numeric = []
    for trial in range(3):
        vals = {}
        for ei in range(len(EDGES)):
            for c in range(9):
                if (T[ei] >> c) & 1:
                    vals[(ei, c)] = Fraction(rng.randint(-9, 9) or 7,
                                             rng.randint(1, 6))
        pairs = [(x, tuple(rng.randrange(Q) for _ in range(4)))
                 for x in LFREE for _ in range(9)]
        bad = 0
        for x, y in pairs:
            w = tuple(x) + tuple(y)
            if H_value(T, w, vals) != perB_value(T, x, y, vals):
                bad += 1
        numeric.append(dict(trial=trial, pairs=len(pairs), mismatches=bad))
    out["numeric_random_value_checks"] = numeric

    # ---- the counting claim 3,960 / 4,860 ---------------------------------
    LF = set(tuple(x) for x in LFREE)
    RF = set(tuple(y) for y in RFREE)
    union = set()
    for x in LF:
        for y in product(range(Q), repeat=4):
            union.add(tuple(x) + tuple(y))
    for y in RF:
        for x in product(range(Q), repeat=4):
            union.add(tuple(x) + tuple(y))
    both = set(tuple(x) + tuple(y) for x in LF for y in RF)
    out["counting"] = dict(
        n_Lfree_times_81=len(LF) * 81, n_Rfree_times_81=len(RF) * 81,
        n_both=len(both), union=len(union),
        union_formula="30*81 + 30*81 - 30*30 = 2430 + 2430 - 900 = 3960",
        union_all_mixed=all(len(set(w)) > 1 for w in union),
        n_mixed_total=len(MIXED),
        w20_4860_is_2430_plus_2430_double_counting_the_900=(
            2430 + 2430 == out["total_pair_tests"]))
    return out, LFREE, RFREE, LS, RS


# ================================================================== B3 =====
def B3_mutations(T=C8, LFREE=None):
    out = {}
    rng = random.Random(31337)
    vals = {}
    for ei in range(len(EDGES)):
        for c in range(9):
            if (T[ei] >> c) & 1:
                vals[(ei, c)] = Fraction(rng.randint(-9, 9) or 4,
                                         rng.randint(1, 6))
    pairs = [(x, y) for x in LFREE for y in product(range(Q), repeat=4)]
    baseline = 0
    for x, y in pairs:
        if H_value(T, tuple(x) + tuple(y), vals) != perB_value(T, x, y, vals):
            baseline += 1
    out["baseline_mismatches_over_2430"] = baseline

    # MUT1: corrupt ONE CROSS-BLOCK entry (in the per B side only).
    cross_keys = [(EIDX[(i, j)], c) for i in L for j in R for c in range(9)
                  if (T[EIDX[(i, j)]] >> c) & 1]
    mut1 = []
    for key in [cross_keys[0], cross_keys[7], cross_keys[40],
                cross_keys[len(cross_keys) // 2], cross_keys[-1]]:
        v2 = dict(vals)
        v2[key] = v2[key] + 1
        bad = 0
        for x, y in pairs:
            if H_value(T, tuple(x) + tuple(y), vals) != perB_value(T, x, y, v2):
                bad += 1
        mut1.append(dict(corrupted_cell=dict(edge=list(EDGES[key[0]]),
                                             cell=[key[1] // 3, key[1] % 3]),
                         mismatches_over_2430=bad, FIRES=bad > 0))
    out["MUT1_cross_block_entry"] = mut1

    # MUT2: corrupt ONE SINGLE cell -- H must NOT change on L-free words.
    sk = single_cell_keys(T)
    mut2 = []
    for key in sk:
        v2 = dict(vals)
        v2[key] = v2[key] + 1
        changed_free = 0
        for x, y in pairs:
            w = tuple(x) + tuple(y)
            if H_value(T, w, vals) != H_value(T, w, v2):
                changed_free += 1
        # the perturbation must be REAL: some word where H does change
        changed_any = 0
        for w in MIXED:
            if H_value(T, w, vals) != H_value(T, w, v2):
                changed_any += 1
                if changed_any > 3:
                    break
        mut2.append(dict(corrupted_cell=dict(edge=list(EDGES[key[0]]),
                                             cell=[key[1] // 3, key[1] % 3]),
                         Lfree_words_changed=changed_free,
                         perturbation_is_real_some_word_changes=changed_any > 0,
                         DOES_NOT_FIRE=(changed_free == 0)))
    out["MUT2_single_cell_entry"] = mut2

    # MUT3: template mutation -- relocate one L-single, so the L-free set
    # changes; a word that was L-free must then LOSE the identity.
    LS = singles_inside(T, L)
    e0 = sorted(LS)[0]
    old_cell = LS[e0]
    ei0 = EIDX[e0]
    newcell = ((old_cell[0] + 1) % 3, (old_cell[1] + 1) % 3)
    T2 = list(T)
    T2[ei0] = 1 << (3 * newcell[0] + newcell[1])
    T2 = tuple(T2)
    LS2 = singles_inside(T2, L)
    LF2 = set(free_words(L, LS2))
    lost = [x for x in LFREE if tuple(x) not in LF2]
    broke = 0
    tested3 = 0
    for x in lost:
        for y in product(range(Q), repeat=4):
            tested3 += 1
            w = tuple(x) + tuple(y)
            if H_poly(T2, w) != perB_poly(T2, x, y):
                broke += 1
    # and the identity must HOLD on the new L-free set
    held = 0
    tested3b = 0
    for x in sorted(LF2):
        for y in product(range(Q), repeat=4):
            tested3b += 1
            if H_poly(T2, tuple(x) + tuple(y)) != perB_poly(T2, x, y):
                held += 1
    out["MUT3_relocate_an_L_single"] = dict(
        edge=list(e0), old_cell=list(old_cell), new_cell=list(newcell),
        n_Lfree_new=len(LF2),
        words_that_lost_L_freeness=len(lost),
        pairs_tested_on_lost_words=tested3,
        identity_failures_on_lost_words=broke,
        FIRES=broke > 0,
        pairs_tested_on_new_Lfree=tested3b,
        identity_failures_on_new_Lfree=held)

    # MUT4: the L-free hypothesis is NECESSARY -- on NON-L-free x the
    # identity must fail for at least some y.
    allx = list(product(range(Q), repeat=4))
    nonfree = [x for x in allx if tuple(x) not in set(map(tuple, LFREE))]
    fails = 0
    checked = 0
    per_word = []
    for x in nonfree:
        bad = 0
        for y in product(range(Q), repeat=4):
            checked += 1
            if H_poly(T, tuple(x) + tuple(y)) != perB_poly(T, x, y):
                bad += 1
        fails += (bad > 0)
        per_word.append(bad)
    out["MUT4_non_Lfree_x_breaks_identity"] = dict(
        n_non_Lfree_x=len(nonfree), pairs_checked=checked,
        n_non_Lfree_x_with_at_least_one_failure=fails,
        min_failures_per_x=min(per_word), max_failures_per_x=max(per_word),
        FIRES=(fails == len(nonfree)))
    return out


def main():
    res = {"_header": "A7 SUB-AUDIT -- ITEM B, L-free/R-free reduction on the "
                      "C_8 member.  Independent engine, exact arithmetic."}
    res["B1"] = B1_engine_controls()
    print("B1 engine controls:", json.dumps(
        {k: v for k, v in res["B1"].items()
         if k not in ("my_C8_audit", "per_word_fibre_sample_250")},
        indent=1, default=str), flush=True)
    b2, LFREE, RFREE, LS, RS = B2_reduction()
    res["B2"] = b2
    print("B2:", json.dumps({k: v for k, v in b2.items()
                             if k != "Lfree_words"}, indent=1, default=str),
          flush=True)
    res["B3"] = B3_mutations(C8, LFREE)
    print("B3:", json.dumps(res["B3"], indent=1, default=str), flush=True)
    json.dump(res, open(os.path.join(HERE, "a7_results_B_c8.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
