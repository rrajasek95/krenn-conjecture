#!/usr/bin/env python3
"""UNAUDITED PROBE -- W5 task B2: EIGHT-SITE EXACTNESS PUSH vs SLICE DIRTINESS.

Pinned HEAD: 181a4c084a91f1518c2bdfe2f574b9a7df1b1830

The question J.1b actually asks: as the mixed GHZ equations are imposed,
does slice-cleanliness get FORCED at some full-rank pair?  Task A shows the
pure normalisations cannot force it; task B shows every available
near-exact / all-blocked data set satisfies it for SUPPORT reasons.  Here we
push complex eight-site sources toward exactness numerically and watch the
(colour x full-rank pair) dirtiness pattern along the trajectory.

FLOATING POINT IS USED ONLY FOR THE SEARCH.  Every reported structural
quantity is a scale-invariant ratio

    rho(c, p, q) = |E^(c)_pq| / E^(c)_pq(|w|)   in [0, 1],

which is invariant under the site-scaling gauge, is 0 exactly at
cleanliness, and is 0/0 (reported as "support-dead") when the error
polynomial has no surviving monomial at all.  Endpoints are re-examined
with exact rational arithmetic after rounding.

Run: python3 run_b2_push.py [--starts 6] [--maxiter 200]
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations, product

import numpy as np
from scipy.optimize import least_squares

import slice_core as sc

N = 8
SITES = tuple(range(N))
EDGES = list(combinations(SITES, 2))
EIDX = {e: n for n, e in enumerate(EDGES)}
MATCHINGS = sc.perfect_matchings(SITES)
WORDS = list(product(range(3), repeat=N))
LETTERS = "abcdefgh"
TARGET = np.zeros((3,) * N, dtype=complex)
for c in range(3):
    TARGET[(c,) * N] = 1.0


def matching_tensor(blocks):
    """H_B(A) as a 3^8 complex tensor; blocks is (28, 3, 3)."""
    total = np.zeros((3,) * N, dtype=complex)
    for matching in MATCHINGS:
        subs = []
        arrs = []
        for a, b in matching:
            subs.append(LETTERS[a] + LETTERS[b])
            arrs.append(blocks[EIDX[(a, b)]])
        expr = ",".join(subs) + "->" + LETTERS
        total += np.einsum(expr, *arrs, optimize=True)
    return total


def sub_tensors(blocks):
    """For each edge e: H_{B\\e}(A), a 3^6 tensor on the remaining sites."""
    out = {}
    for e in EDGES:
        rest = tuple(s for s in SITES if s not in e)
        letters = "".join(LETTERS[s] for s in rest)
        acc = np.zeros((3,) * 6, dtype=complex)
        for matching in sc.perfect_matchings(rest):
            subs = []
            arrs = []
            for a, b in matching:
                subs.append(LETTERS[a] + LETTERS[b])
                arrs.append(blocks[EIDX[(a, b)]])
            acc += np.einsum(",".join(subs) + "->" + letters, *arrs,
                             optimize=True)
        out[e] = acc
    return out


def pack(blocks):
    z = blocks.reshape(-1)
    return np.concatenate([z.real, z.imag])


def unpack(x):
    half = x.size // 2
    z = x[:half] + 1j * x[half:]
    return z.reshape(28, 3, 3)


def residual(x):
    blocks = unpack(x)
    diff = (matching_tensor(blocks) - TARGET).reshape(-1)
    return np.concatenate([diff.real, diff.imag])


def jacobian(x):
    blocks = unpack(x)
    subs = sub_tensors(blocks)
    ncomplex = 28 * 9
    J = np.zeros((3 ** N, ncomplex), dtype=complex)
    for e in EDGES:
        a, b = e
        rest = [s for s in SITES if s not in e]
        # place the 6-tensor into the 8-tensor with axes a, b appended
        order = rest + [a, b]
        big = np.zeros((3,) * N, dtype=complex)
        for i in range(3):
            for j in range(3):
                col = np.zeros((3,) * N, dtype=complex)
                # index with slices: axis a = i, axis b = j
                idx = [slice(None)] * N
                idx[a] = i
                idx[b] = j
                col[tuple(idx)] = subs[e]
                J[:, EIDX[e] * 9 + i * 3 + j] = col.reshape(-1)
        del big, order
    top = np.concatenate([J.real, -J.imag], axis=1)
    bot = np.concatenate([J.imag, J.real], axis=1)
    return np.concatenate([top, bot], axis=0)


# ------------------------------------------------------------ slice metrics


def slice_metrics(blocks):
    """rho(c,p,q), det A_pq, per pair -- all in floating point."""
    out = {}
    for pair in EDGES:
        U = tuple(s for s in SITES if s not in pair)
        det = np.linalg.det(blocks[EIDX[pair]])
        rhos = []
        for c in range(3):
            w = {e: blocks[EIDX[e]][c][c] for e in EDGES}
            wa = {e: abs(v) for e, v in w.items()}
            num = abs(sc.slice_error_rank2(w, pair[0], pair[1], U))
            den = sc.slice_error_rank2(wa, pair[0], pair[1], U)
            rhos.append(float(num / den) if den > 0 else None)
        out[pair] = {"det": abs(det), "rho": rhos}
    return out


def summarise(blocks, tol_det=1e-6, tol_rho=1e-8, tol_eq=1e-7):
    m = slice_metrics(blocks)
    scale = max(abs(blocks).max(), 1e-300)
    full = [p for p in EDGES if m[p]["det"] > tol_det * scale ** 3]
    all_dirty = []
    min_rho = None
    for p in full:
        rr = [r for r in m[p]["rho"] if r is not None]
        dead = [r for r in m[p]["rho"] if r is None]
        if dead:
            continue                      # a support-dead slice = clean
        if all(r > tol_rho for r in rr):
            all_dirty.append(p)
        cand = min(rr) if rr else None
        if cand is not None and (min_rho is None or cand < min_rho):
            min_rho = cand
    # which GHZ equations fail, and in particular the three PURE ones?
    tensor = matching_tensor(blocks)
    diff = np.abs(tensor - TARGET)
    bad = int((diff > tol_eq).sum())
    pure = [abs(tensor[(c,) * N] - 1.0) for c in range(3)]
    pure_ok = [bool(v <= tol_eq) for v in pure]
    return {"full_rank_pairs": len(full),
            "full_rank_all_three_dirty": len(all_dirty),
            "min_rho_over_full_rank_pairs": min_rho,
            "defective_words": bad,
            "pure_values": [complex(tensor[(c,) * N]) for c in range(3)],
            "all_three_pure_ok": all(pure_ok),
            "falsifier_shape": bool(all(pure_ok) and all_dirty),
            "max_abs_entry": float(abs(blocks).max())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--starts", type=int, default=6)
    ap.add_argument("--maxiter", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260815)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    records = []
    print("== B2  exactness push at N = 8 (complex, 252 complex unknowns) ==")
    print("   start: random dense source; target: H_B(A) = Delta_{B,3}")
    for start in range(args.starts):
        blocks = (rng.normal(size=(28, 3, 3))
                  + 1j * rng.normal(size=(28, 3, 3))) / 2.0
        before = summarise(blocks)
        r0 = float(np.linalg.norm(residual(pack(blocks))))
        sol = least_squares(residual, pack(blocks), jac=jacobian,
                            method="lm", max_nfev=args.maxiter,
                            xtol=1e-13, ftol=1e-13, gtol=1e-13)
        blocks1 = unpack(sol.x)
        after = summarise(blocks1)
        r1 = float(np.linalg.norm(sol.fun))
        rec = {"start": start, "residual_before": r0, "residual_after": r1,
               "before": before, "after": after, "status": int(sol.status),
               "nfev": int(sol.nfev)}
        records.append(rec)
        print(f"  start {start}: |res| {r0:.2e} -> {r1:.4f}; full-rank pairs "
              f"{before['full_rank_pairs']} -> {after['full_rank_pairs']}; "
              f"all-three-dirty {before['full_rank_all_three_dirty']} -> "
              f"{after['full_rank_all_three_dirty']}; defective words "
              f"{after['defective_words']}; all three pure OK "
              f"{after['all_three_pure_ok']}; FALSIFIER-SHAPE "
              f"{after['falsifier_shape']}", flush=True)
        with open("results_b2_push.json", "w") as fh:      # dump incrementally
            json.dump({"note": "UNAUDITED PROBE W5 task B2 (float search)",
                       "head": "181a4c084a91f1518c2bdfe2f574b9a7df1b1830",
                       "records": records}, fh, indent=1, default=str)
    # aggregate
    plateau = min((r["residual_after"] for r in records), default=None)
    fal = [r for r in records if r["after"]["falsifier_shape"]]
    print(f"  best residual reached: {plateau}")
    print(f"  runs ending with (all three pure equations exact) AND (a "
          f"full-rank pair with all three slices dirty): {len(fal)}/"
          f"{len(records)}")
    with open("results_b2_push.json", "w") as fh:
        json.dump({"note": "UNAUDITED PROBE W5 task B2 (float search)",
                   "head": "181a4c084a91f1518c2bdfe2f574b9a7df1b1830",
                   "records": records}, fh, indent=1, default=str)
    print("wrote results_b2_push.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
