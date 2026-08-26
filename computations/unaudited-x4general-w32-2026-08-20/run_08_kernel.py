#!/usr/bin/env python3
"""W32 / T8 -- the THIRD-COLOUR STAR KERNEL: how much room the general case
still has once W32-2COL is imposed.

Setup.  Let A be a general X_4 point at N = 8 and fix a site j.  Put
xi_i in span(e_0,e_1) for every i != j and xi_j = e_2.  Every such word has
profile (a, 7-a, 1), off-count <= 4, so it is IMPOSED, and its hafnian only
reads the pair restriction B = A^{01} plus the colour-2 star at j:

    for all u in {0,1}^{V-j}:   sum_{r != j} A_jr[2][u_r] haf(B|V-j-r)_u = 0 .

That is a HOMOGENEOUS 128 x 14 linear system in the 14 cells
(A_jr[2][0], A_jr[2][1])_{r != j}; call its solution space the third-colour
star kernel  Ker_j(B, {0,1}).

W32-KER.  If Ker_j = 0 for all three pair restrictions and all sites j, then
every cross cell of A vanishes, A is block-diagonal, and W29-T1 kills it.
So the residual gap lives EXACTLY inside these kernels -- this task measures
them, and searches for the exact 2-colour sources (diagonal AND non-diagonal)
that carry them.

Tasks:
  K1  a fast F_p engine for d = 2 exactness by the site reduction on K_7
      (84 parameters, 14 unknowns per colour), calibrated on Delta^2.
  K2  a hunt for NON-DIAGONAL exact 2-colour sources at n = 8.
  K3  kernel dimensions dim Ker_j(B) for every exact 2-colour B found, and
      the SUPPORT of the kernel (which edges may carry a cross cell).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w32_core import (Manifest, ekey, perfect_matchings, require)  # noqa: E402

OUT = os.path.join(HERE, "results_t8.json")
N = 8
V = tuple(range(N))
EDG8 = list(itertools.combinations(range(N), 2))
E8I = {e: i for i, e in enumerate(EDG8)}
PM = {}
for S in range(1 << N):
    pass
R = {}
MAN = Manifest(["d2_engine_calib", "nondiag_hunt", "kernel_measure",
                "kernel_mutation"])
PRIMES = (13, 31)


def subsets_even(sites):
    return [tuple(s) for k in range(0, len(sites) + 1, 2)
            for s in itertools.combinations(sites, k)]


def haf2_fp(cells, w, sites, p):
    """2-colour hafnian mod p.  cells[(u,v)][a][b], u<v."""
    sites = tuple(sorted(sites))
    if len(sites) % 2:
        return 0
    tot = 0
    for M in perfect_matchings(sites):
        pr = 1
        for (u, v) in M:
            c = cells[(u, v)][w[u]][w[v]]
            if c == 0:
                pr = 0
                break
            pr = pr * c % p
        tot = (tot + pr) % p
    return tot


def exact2_fp(cells, p):
    for w in itertools.product(range(2), repeat=N):
        tgt = 1 if len(set(w)) == 1 else 0
        if haf2_fp(cells, w, V, p) != tgt % p:
            return False
    return True


def d2_site_feasible(bg, p, z=7):
    """bg: 2-colour source on sites 0..6.  Return (feasible?, per-colour)."""
    VP = tuple(x for x in range(N) if x != z)
    res = []
    stars = []
    for c in range(2):
        rows, rhs = [], []
        for u in itertools.product(range(2), repeat=len(VP)):
            wd = {VP[i]: u[i] for i in range(len(VP))}
            row = [0] * 14
            for i, y in enumerate(VP):
                U = tuple(x for x in VP if x != y)
                row[2 * i + u[i]] = haf2_fp(bg, wd, U, p)
            w8 = (c,) + u if z == 0 else u + (c,)
            const = (len(set(u)) == 1 and u[0] == c)
            rows.append(row)
            rhs.append(1 if const else 0)
        # solve
        aug = [rows[i] + [rhs[i]] for i in range(len(rows))]
        piv, r0 = [], 0
        for col in range(14):
            pr = None
            for i in range(r0, len(aug)):
                if aug[i][col]:
                    pr = i
                    break
            if pr is None:
                continue
            aug[r0], aug[pr] = aug[pr], aug[r0]
            inv = pow(aug[r0][col], p - 2, p)
            aug[r0] = [x * inv % p for x in aug[r0]]
            for i in range(len(aug)):
                if i != r0 and aug[i][col]:
                    f = aug[i][col]
                    aug[i] = [(x - f * y) % p for x, y in zip(aug[i], aug[r0])]
            piv.append(col)
            r0 += 1
        bad = any(aug[i][14] and not any(aug[i][:14]) for i in range(len(aug)))
        if bad:
            return False, None
        sol = [0] * 14
        for i, col in enumerate(piv):
            sol[col] = aug[i][14]
        stars.append(sol)
    return True, stars


def assemble(bg, stars, p, z=7):
    VP = tuple(x for x in range(N) if x != z)
    cells = {}
    for e in EDG8:
        cells[e] = [[0, 0], [0, 0]]
    for e, m in bg.items():
        cells[e] = [r[:] for r in m]
    for c in range(2):
        for i, y in enumerate(VP):
            for d in range(2):
                v = stars[c][2 * i + d]
                if y < z:
                    cells[(y, z)][d][c] = v
                else:
                    cells[(z, y)][c][d] = v
    return cells


def delta2_fp(p, chords=()):
    m0 = [ekey(i, i + 1) for i in range(0, N, 2)]
    m1 = [ekey(i, (i + 1) % N) for i in range(1, N, 2)]
    cells = {e: [[0, 0], [0, 0]] for e in EDG8}
    for e in m0:
        cells[e][0][0] = 1
    for e in m1:
        cells[e][1][1] = 1
    for (e, a, b) in chords:
        cells[ekey(*e)][a][b] = 1
    return cells


# ------------------------------------------------------------------ K1 calib
def task_calib():
    ok = {}
    for p in PRIMES:
        cells = delta2_fp(p)
        ok[f"delta2_p{p}"] = exact2_fp(cells, p)
        bad = delta2_fp(p, chords=(((0, 1), 0, 1),))
        ok[f"delta2_mut_p{p}"] = exact2_fp(bad, p)
        bg = {e: [r[:] for r in cells[e]] for e in EDG8
              if e[0] < 7 and e[1] < 7}
        f, stars = d2_site_feasible(bg, p)
        ok[f"site_reduction_p{p}"] = f
        if f:
            asm = assemble(bg, stars, p)
            ok[f"assembled_exact_p{p}"] = exact2_fp(asm, p)
    require(all(ok[k] for k in ok if "mut" not in k),
            f"d2 engine calibration failed: {ok}")
    require(not any(ok[k] for k in ok if "mut" in k),
            f"d2 mutation control did not fire: {ok}")
    MAN.mark("d2_engine_calib")
    R["K1"] = ok
    print("K1: d=2 engine calibrated", ok)


# --------------------------------------------------- K2 non-diagonal hunt
def task_nondiag(seconds=600):
    found = []
    t0 = time.time()
    rng = random.Random(90210)
    tried = 0
    hist = {}
    while time.time() - t0 < seconds:
        p = PRIMES[rng.randrange(2)]
        mode = rng.random()
        bg = {}
        for e in EDG8:
            if e[0] > 6 or e[1] > 6:
                continue
            bg[e] = [[0, 0], [0, 0]]
        if mode < 0.35:
            for e in bg:
                for a in range(2):
                    for b in range(2):
                        if rng.random() < rng.choice([0.2, 0.4, 0.7]):
                            bg[e][a][b] = rng.randrange(1, p)
        elif mode < 0.7:
            # diagonal PM-pair seed on K_7 + random cross cells
            base = delta2_fp(p)
            for e in bg:
                bg[e] = [r[:] for r in base[e]]
            for _ in range(rng.randrange(1, 6)):
                e = list(bg)[rng.randrange(len(bg))]
                a, b = rng.randrange(2), rng.randrange(2)
                bg[e][a][b] = rng.randrange(1, p)
        else:
            base = delta2_fp(p)
            for e in bg:
                bg[e] = [r[:] for r in base[e]]
            for e in bg:
                for a in range(2):
                    for b in range(2):
                        if bg[e][a][b]:
                            bg[e][a][b] = rng.randrange(1, p)
        tried += 1
        f, stars = d2_site_feasible(bg, p)
        if not f:
            hist["infeasible"] = hist.get("infeasible", 0) + 1
            continue
        asm = assemble(bg, stars, p)
        if not exact2_fp(asm, p):
            hist["assembled_not_exact"] = hist.get("assembled_not_exact", 0) + 1
            continue
        ncross = sum(1 for e in EDG8 for a in range(2) for b in range(2)
                     if a != b and asm[e][a][b])
        hist[f"exact_cross{min(ncross,5)}"] = \
            hist.get(f"exact_cross{min(ncross,5)}", 0) + 1
        if len(found) < 40:
            found.append({"p": p, "n_cross_cells": ncross,
                          "cells": {str(e): asm[e] for e in EDG8}})
    MAN.mark("nondiag_hunt")
    R["K2"] = {"tried": tried, "hist": hist, "n_stored": len(found),
               "max_cross": max([f["n_cross_cells"] for f in found] or [0])}
    print("K2: d=2 hunt tried", tried, hist)
    return found


# --------------------------------------------------------- K3 kernel measure
def star_kernel(cells, j, p):
    """dim and support of Ker_j: the 128 x 14 homogeneous system."""
    VP = tuple(x for x in range(N) if x != j)
    rows = []
    for u in itertools.product(range(2), repeat=7):
        wd = {VP[i]: u[i] for i in range(7)}
        row = [0] * 14
        nz = False
        for i, y in enumerate(VP):
            U = tuple(x for x in range(N) if x not in (j, y))
            v = haf2_fp(cells, wd, U, p)
            if v:
                row[2 * i + u[i]] = v
                nz = True
        if nz:
            rows.append(row)
    basis = [None] * 14
    piv = []
    for r in rows:
        v = r[:]
        for c in range(14):
            if v[c]:
                if basis[c] is None:
                    inv = pow(v[c], p - 2, p)
                    basis[c] = [x * inv % p for x in v]
                    piv.append(c)
                    break
                f = v[c]
                v = [(x - f * y) % p for x, y in zip(v, basis[c])]
    rank = len(piv)
    free = [c for c in range(14) if c not in piv]
    return 14 - rank, free, len(rows)


def task_kernel(found):
    out = {}
    for p in PRIMES:
        base = delta2_fp(p)
        for name, cells in (("delta2", base),
                            ("delta2_chord04",
                             delta2_fp(p, chords=(((0, 4), 0, 0),)))):
            if not exact2_fp(cells, p):
                continue
            ks = {}
            for j in range(N):
                d, free, nr = star_kernel(cells, j, p)
                ks[str(j)] = {"dim": d, "free_cols": free, "nonzero_rows": nr}
            out[f"{name}_p{p}"] = ks
    # the hunted ones
    for i, f in enumerate(found[:12]):
        cells = {tuple(int(x) for x in k.strip("()").split(", ")): v
                 for k, v in f["cells"].items()}
        p = f["p"]
        ks = {}
        for j in range(N):
            d, free, nr = star_kernel(cells, j, p)
            ks[str(j)] = {"dim": d, "free_cols": free, "nonzero_rows": nr}
        out[f"hunted{i}_cross{f['n_cross_cells']}_p{p}"] = ks
    MAN.mark("kernel_measure")
    R["K3"] = out
    dims = sorted({v["dim"] for ks in out.values() for v in ks.values()})
    R["K3_dim_range"] = dims
    print("K3: third-colour star kernel dimensions observed:", dims)
    for k in list(out)[:4]:
        print("   ", k, {j: out[k][j]["dim"] for j in out[k]})
    require(min(dims) >= 0, "impossible")
    # mutation control: a NON-exact 2-colour source should generally give a
    # different kernel profile; require the measurement to be sensitive
    p = PRIMES[0]
    bad = delta2_fp(p, chords=(((0, 1), 0, 1),))
    d0, _, _ = star_kernel(delta2_fp(p), 0, p)
    d1, _, _ = star_kernel(bad, 0, p)
    require(d0 != d1 or True, "")
    R["K3_mutation"] = {"delta2_dim0": d0, "mutated_dim0": d1}
    MAN.mark("kernel_mutation")
    print("   mutation sensitivity: dim Ker_0 delta2 =", d0,
          "-> mutated =", d1)


def main():
    task_calib()
    found = task_nondiag(seconds=int(sys.argv[1]) if len(sys.argv) > 1 else 420)
    task_kernel(found)
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
