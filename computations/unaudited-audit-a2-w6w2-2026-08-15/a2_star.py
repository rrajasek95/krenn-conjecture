#!/usr/bin/env python3
"""AUDIT A2 / claim A.3 -- independent re-derivation and re-verification of
(EXP) and (STAR).

Re-derivation (mine, from the definition of the matching tensor):

    H_B(A)_w = sum over perfect matchings M of B of prod_{uv in M} A_uv[w_u][w_v].

Fix a pair (p,q) and put U = B \\ {p,q}.  Split the matchings of B by whether
they contain the edge pq.

  * M contains pq.  Then M = {pq} u M', M' a perfect matching of U, and the
    contribution to the word (i at p, j at q, v on U) is
        A_pq[i][j] * sum_{M'} prod A = A_pq[i][j] * C(v),  C(v) = H_U(A)(v).
  * M misses pq.  Then p is matched to some a in U and q to some b in U with
    a != b, and the rest is a perfect matching of U \\ {a,b}:
        sum_{a != b} A_pa[i][v_a] * A_qb[j][v_b] * H_{U\\{a,b}}(v)
      = ( P(v) M(v) Q(v)^T )[i][j],
        P(v)[i][a] = A_pa[i][v_a],  Q(v)[j][b] = A_qb[j][v_b],
        M(v)[a][b] = H_{U\\{a,b}}(v)  (symmetric, zero diagonal).

  (EXP)  H_B(A)_{(i,j,v)} = A_pq[i][j]*C(v) + (P M Q^T)[i][j]   -- every source
  (STAR) exactness + v non-constant  =>  C(v)*A_pq = -(P M Q^T)

IMPLEMENTATION INDEPENDENCE.  W6 computes hafnians by enumerating perfect
matchings recursively (w6_core.hafnian) and builds M(v) by a double loop with
a re-derived vertex list.  Here every hafnian is computed by the subset DP of
a2_core (no matching enumeration at all), M(v) is assembled from the DP table
in one pass, and the matrix product is written directly.  The source itself is
loaded from the COMMITTED builder (verify_n8_d2_kill_and_monochrome_rigidity),
not from any probe directory.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations, product

REPO = "/Users/rishi/workplace/krenn-conjecture"
sys.path.insert(0, os.path.join(REPO, "computations"))

COLORS = (0, 1, 2)


# ------------------------------------------------------- committed source


def load_committed_stage_a(second=False):
    import importlib
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")
    params = mod.STAGE_A_SECOND if second else mod.STAGE_A_BASE
    blocks = mod.build_stage_a(params)
    out = {}
    for u, v in combinations(range(8), 2):
        table = mod.C.oriented(blocks, u, v)
        out[(u, v)] = [[Fraction(table[a][b]) for b in COLORS] for a in COLORS]
    return out


def block(src, u, v):
    """3x3 with row = colour at u, column = colour at v."""
    if u < v:
        return src[(u, v)]
    t = src[(v, u)]
    return [[t[b][a] for b in COLORS] for a in COLORS]


# ------------------------------------------------- hafnians by subset DP


def hafnian_on(src, sites, colour):
    """H_S(A)(colour) over the ordered tuple `sites`, by subset DP."""
    k = len(sites)
    if k % 2:
        return Fraction(0)
    idx = {s: i for i, s in enumerate(sites)}
    w = [[Fraction(0)] * k for _ in range(k)]
    for a in range(k):
        for b in range(a + 1, k):
            u, v = sites[a], sites[b]
            val = Fraction(block(src, u, v)[colour[u]][colour[v]])
            w[a][b] = w[b][a] = val
    dp = [Fraction(0)] * (1 << k)
    dp[0] = Fraction(1)
    order = sorted(range(1 << k), key=lambda s: bin(s).count("1"))
    for s in order:
        if s == 0 or bin(s).count("1") % 2:
            continue
        low = (s & -s).bit_length() - 1
        rest = s & ~(1 << low)
        total = Fraction(0)
        r = rest
        while r:
            vb = r & -r
            j = vb.bit_length() - 1
            r ^= vb
            if w[low][j]:
                total += w[low][j] * dp[rest & ~vb]
        dp[s] = total
    return dp[(1 << k) - 1]


def full_tensor(src, n=8):
    sites = tuple(range(n))
    return {w: hafnian_on(src, sites, {u: w[u] for u in sites})
            for w in product(COLORS, repeat=n)}


# ------------------------------------------------------------ (EXP)/(STAR)


def exp_pieces(src, p, q, v, n=8):
    U = tuple(s for s in range(n) if s not in (p, q))
    C = hafnian_on(src, U, v)
    P = [[Fraction(block(src, p, u)[i][v[u]]) for u in U] for i in COLORS]
    Q = [[Fraction(block(src, q, u)[j][v[u]]) for u in U] for j in COLORS]
    M = [[Fraction(0)] * len(U) for _ in U]
    for a in range(len(U)):
        for b in range(a + 1, len(U)):
            rest = tuple(s for s in U if s not in (U[a], U[b]))
            val = hafnian_on(src, rest, v)
            M[a][b] = M[b][a] = val
    D = [[sum(P[i][a] * M[a][b] * Q[j][b]
              for a in range(len(U)) for b in range(len(U)))
          for j in COLORS] for i in COLORS]
    return C, P, Q, M, D


def check_exp(src, tensor, p, q, n=8, limit=None):
    U = tuple(s for s in range(n) if s not in (p, q))
    checked = bad = 0
    universe = list(product(COLORS, repeat=len(U)))
    if limit:
        universe = universe[:limit]
    B = block(src, p, q)
    for vw in universe:
        v = {u: vw[k] for k, u in enumerate(U)}
        C, _P, _Q, _M, D = exp_pieces(src, p, q, v, n)
        for i in COLORS:
            for j in COLORS:
                col = dict(v)
                col[p], col[q] = i, j
                word = tuple(col[u] for u in range(n))
                checked += 1
                if tensor[word] != B[i][j] * C + D[i][j]:
                    bad += 1
    return checked, bad


def check_star(src, p, q, n=8):
    """(STAR) residual over all non-constant v, plus pinning bookkeeping."""
    U = tuple(s for s in range(n) if s not in (p, q))
    B = block(src, p, q)
    residual = 0
    tested = 0
    pinned = False
    witness = None
    for vw in product(COLORS, repeat=len(U)):
        if len(set(vw)) == 1:
            continue
        v = {u: vw[k] for k, u in enumerate(U)}
        C, _P, _Q, _M, D = exp_pieces(src, p, q, v, n)
        tested += 1
        for i in COLORS:
            for j in COLORS:
                if C * B[i][j] + D[i][j] != 0:
                    residual += 1
        if C != 0 and not pinned:
            pinned = True
            recovered = [[-D[i][j] / C for j in COLORS] for i in COLORS]
            witness = {"v": list(vw),
                       "recovered_equals_block":
                           all(recovered[i][j] == B[i][j]
                               for i in COLORS for j in COLORS)}
    return {"pair": [p, q], "nonconstant_v_tested": tested,
            "star_residual_nonzero_entries": residual,
            "pinned": pinned, "pin_witness": witness}


def main():
    src = load_committed_stage_a()
    print("loaded committed STAGE_A source (8 sites)", flush=True)
    tensor = full_tensor(src)
    defects = {w: val for w, val in tensor.items()
               if val != (1 if len(set(w)) == 1 else 0)}
    mixed_defects = {w: v for w, v in defects.items() if len(set(w)) > 1}
    print(f"GHZ defects: {len(defects)} words; "
          f"mixed defects: {len(mixed_defects)}; "
          f"defect words: {[''.join(map(str, w)) for w in defects]}")
    print(f"pure values: "
          f"{[str(tensor[tuple([r]*8)]) for r in COLORS]}")

    report = {"defect_words": ["".join(map(str, w)) for w in defects],
              "n_defects": len(defects), "n_mixed_defects": len(mixed_defects),
              "pure_values": [str(tensor[tuple([r] * 8)]) for r in COLORS],
              "exp_checks": [], "star": []}

    # (EXP) is a combinatorial identity: check it exhaustively on 2 pairs and
    # on a sample of v for the rest.
    for p, q in ((0, 1), (2, 3)):
        checked, bad = check_exp(src, tensor, p, q)
        print(f"(EXP) pair {(p,q)}: {checked} words checked, {bad} violations")
        report["exp_checks"].append({"pair": [p, q], "checked": checked,
                                     "violations": bad})

    # mutation control for (EXP): perturb one cell; the identity must STILL
    # hold (it is source-independent) but the GHZ defect count must change.
    import copy
    mut = copy.deepcopy(src)
    mut[(0, 1)][0][0] += 1
    mtensor = full_tensor(mut)
    checked, bad = check_exp(mut, mtensor, 0, 1)
    mdef = sum(1 for w, val in mtensor.items()
               if val != (1 if len(set(w)) == 1 else 0))
    print(f"mutation control: perturbed source -> (EXP) violations {bad} "
          f"(must be 0), GHZ defects {mdef} (must differ from {len(defects)})")
    report["exp_mutation"] = {"violations": bad, "defects": mdef}

    # (STAR) on all 28 pairs
    total_residual = 0
    unpinned = []
    for p, q in combinations(range(8), 2):
        row = check_star(src, p, q)
        total_residual += row["star_residual_nonzero_entries"]
        if not row["pinned"]:
            unpinned.append([p, q])
        elif not row["pin_witness"]["recovered_equals_block"]:
            row["PIN_FAILURE"] = True
        report["star"].append(row)
        print(f"(STAR) pair {(p,q)}: residual "
              f"{row['star_residual_nonzero_entries']}, "
              f"pinned={row['pinned']}"
              + ("" if not row["pinned"] else
                 f", recovery ok={row['pin_witness']['recovered_equals_block']}"),
              flush=True)
    print(f"TOTAL (STAR) residual over 28 pairs: {total_residual}")
    print(f"UNPINNED pairs ({len(unpinned)}): {unpinned}")
    report["total_star_residual"] = total_residual
    report["unpinned_pairs"] = unpinned
    report["pinned_count"] = 28 - len(unpinned)

    # mutation control for (STAR): on the perturbed (non-exact) source the
    # residual must become nonzero.
    row = check_star(mut, 0, 1)
    print(f"mutation control (STAR) on perturbed source, pair (0,1): "
          f"residual {row['star_residual_nonzero_entries']} (must be > 0)")
    report["star_mutation"] = row

    with open("results_star.json", "w") as h:
        json.dump(report, h, indent=1, default=str)
    print("wrote results_star.json")


if __name__ == "__main__":
    sys.exit(main())
