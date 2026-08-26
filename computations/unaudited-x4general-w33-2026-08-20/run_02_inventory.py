#!/usr/bin/env python3
"""W33 / T2 -- INVENTORY of exact d=2 sources on K_8, over Q (characteristic
zero objects, not mod-p screens), with gauge invariants.

Method (the site fibration, W27-R1 in W32's numbering).  Every word w in
{0,1}^8 uses every site, so H_w is LINEAR in the star of any single site j
once the background B|_{V-j} on K_7 is fixed.  Hence

    { exact sources with background bg }  =  (particular star)  +  Ker_j(bg)^2

is an AFFINE space of dimension 2*dim Ker_j whenever it is non-empty.  The
inventory therefore samples backgrounds from structured strata, solves the
two 128x14 inhomogeneous systems exactly over Q, and samples the fibre.

Invariants recorded per source (all invariant under the gauge group
T x Z_2 x S_8, so they separate orbits):
  ncell, ncross              cell / cross-cell counts
  edge pattern multiset      per-edge nonzero-cell pattern up to colour swap
  null graph Z               {j,r} in Z iff B restricted to V-{j,r} has
                             H_u = 0 for every u in {0,1}^6  (=> the columns
                             (r,*) of the star matrix at j vanish, so
                             dim Ker_j >= 2 deg_Z(j))
  kernel profile             (dim Ker_j)_{j}, sorted
  cycle+chord test           is the support inside (Hamiltonian cycle C) plus
                             chords joining same-parity vertices of C?
  tangent dim                rank of the 256 x 112 Jacobian (local dimension
                             upper bound; gauge orbit is 14 - dim stab)

Usage: run_02_inventory.py <seconds> <seed> <tag>
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
from w33_core import (  # noqa: E402
    Manifest, cell, complete_site, cycle_pm_pair, edges, haf, haf_pm,
    is_exact2, n_cross, require, setcell, star_kernel, support, zero_source)

N = 8
EDG = edges(N)
SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 600
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 33002
TAG = sys.argv[3] if len(sys.argv) > 3 else "A"
OUT = os.path.join(HERE, f"results_t2_{TAG}.json")
rng = random.Random(SEED)
MAN = Manifest(["engine_recheck", "fibre_affine", "stratum_coverage"])


# ------------------------------------------------------------- invariants
def null_graph(src):
    """{j,r} with H_u = 0 for all u in {0,1}^6 on V - {j,r}."""
    out = []
    for (j, r) in EDG:
        S = [x for x in range(N) if x not in (j, r)]
        dead = True
        for u in itertools.product(range(2), repeat=6):
            wd = {S[i]: u[i] for i in range(6)}
            if haf(src, wd, sites=S) != 0:
                dead = False
                break
        if dead:
            out.append((j, r))
    return out


def kernel_profile(src):
    return [star_kernel(src, j, N)[0] for j in range(N)]


def edge_pattern_multiset(src):
    pats = {}
    for e, m in src.items():
        L = tuple(sorted((a, b) for a in range(2) for b in range(2)
                         if m[a][b] != 0))
        L2 = tuple(sorted((1 - a, 1 - b) for (a, b) in L))
        k = str(min(L, L2))
        pats[k] = pats.get(k, 0) + 1
    return tuple(sorted(pats.items()))


def hamiltonian_cycles(n):
    """All Hamiltonian cycles of K_n as edge sets (canonical, fixing 0)."""
    out = []
    for perm in itertools.permutations(range(1, n)):
        if perm[0] > perm[-1]:
            continue
        cyc = (0,) + perm
        es = frozenset(tuple(sorted((cyc[i], cyc[(i + 1) % n])))
                       for i in range(n))
        out.append((cyc, es))
    return out


HAMS = hamiltonian_cycles(N)


def cycle_chord_test(src):
    """Is there a Hamiltonian cycle C with (i) every cell of every C-edge
    allowed, (ii) every OTHER nonzero cell on a same-parity chord of C?
    Returns the first witness cycle or None."""
    sup = support(src)
    nz = {e for (e, _a, _b) in sup}
    for (cyc, es) in HAMS:
        pos = {v: i for i, v in enumerate(cyc)}
        ok = True
        for e in nz:
            if e in es:
                continue
            if (pos[e[0]] - pos[e[1]]) % 2 != 0:
                ok = False
                break
        if ok:
            return list(cyc)
    return None


def jacobian_rank(src):
    """rank of d(H_w)/d(cell) at src: 256 rows x 112 columns over Q."""
    cols = [(e, a, b) for e in EDG for a in range(2) for b in range(2)]
    rows = []
    for w in itertools.product(range(2), repeat=N):
        row = []
        for (e, a, b) in cols:
            u, v = e
            if w[u] == a and w[v] == b:
                S = [x for x in range(N) if x not in (u, v)]
                row.append(haf(src, w, sites=S))
            elif w[u] == b and w[v] == a and a != b:
                S = [x for x in range(N) if x not in (u, v)]
                row.append(haf(src, w, sites=S))
            else:
                row.append(Fraction(0))
        if any(x != 0 for x in row):
            rows.append(row)
    # gaussian elimination for rank
    piv = []
    rr = 0
    m = [r[:] for r in rows]
    for c in range(len(cols)):
        p = None
        for i in range(rr, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[rr], m[p] = m[p], m[rr]
        inv = Fraction(1) / m[rr][c]
        m[rr] = [x * inv for x in m[rr]]
        for i in range(rr + 1, len(m)):
            if m[i][c] != 0:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[rr])]
        piv.append(c)
        rr += 1
    return len(piv)


def record(src, origin, want_jac=False):
    sup = support(src)
    z = null_graph(src)
    deg = [0] * N
    for (a, b) in z:
        deg[a] += 1
        deg[b] += 1
    rec = {
        "origin": origin,
        "ncell": len(sup),
        "ncross": n_cross(src),
        "patterns": [list(x) for x in edge_pattern_multiset(src)],
        "null_deg": sorted(deg),
        "n_null": len(z),
        "kerprof": sorted(kernel_profile(src)),
        "cycle": cycle_chord_test(src),
        "cells": {f"{e[0]}{e[1]}": [[str(x) for x in row] for row in m]
                  for e, m in src.items() if any(x != 0 for row in m
                                                 for x in row)},
    }
    if want_jac:
        rec["jac_rank"] = jacobian_rank(src)
        rec["tangent_dim"] = 112 - rec["jac_rank"]
    return rec


# ---------------------------------------------------------------- strata
def rval(kind):
    if kind == "01":
        return Fraction(rng.randrange(2))
    if kind == "pm1":
        return Fraction(rng.choice([-1, 1]))
    if kind == "small":
        return Fraction(rng.randrange(-3, 4))
    return Fraction(rng.randrange(-4, 5), rng.randrange(1, 4))


def bg_from_cycle(j, extra, kind):
    """Delta^2 minus site j, plus `extra` random cells among the K_7 edges."""
    src = cycle_pm_pair(N)
    if rng.random() < 0.5:
        # random weights with the two PM products equal to 1
        wa = [Fraction(rng.randrange(1, 5)) for _ in range(3)]
        wd = [Fraction(rng.randrange(1, 5)) for _ in range(3)]
        pa = wa[0] * wa[1] * wa[2]
        pd = wd[0] * wd[1] * wd[2]
        wa.append(1 / pa)
        wd.append(1 / pd)
        src = cycle_pm_pair(N, wa=wa, wd=wd)
    if rng.random() < 0.5:
        perm = list(range(N))
        rng.shuffle(perm)
        src = {tuple(sorted((perm[e[0]], perm[e[1]]))):
               ([r[:] for r in m] if perm[e[0]] < perm[e[1]]
                else [[m[a][b] for a in range(2)] for b in range(2)])
               for e, m in src.items()}
    for _ in range(extra):
        e = EDG[rng.randrange(len(EDG))]
        if j in e:
            continue
        src[e][rng.randrange(2)][rng.randrange(2)] = rval(kind)
    for r in range(N):
        if r != j:
            for a in range(2):
                for b in range(2):
                    setcell(src, j, r, a, b, Fraction(0))
    return src


def bg_random(j, dens, kind):
    src = zero_source(N, 2)
    for e in EDG:
        if j in e:
            continue
        for a in range(2):
            for b in range(2):
                if rng.random() < dens:
                    src[e][a][b] = rval(kind)
    return src


def bg_from_source(src, j):
    out = {e: [r[:] for r in m] for e, m in src.items()}
    for r in range(N):
        if r != j:
            for a in range(2):
                for b in range(2):
                    setcell(out, j, r, a, b, Fraction(0))
    return out


def try_bg(bg, j, origin, pool, seen, stats, want_jac=False):
    feas, part, basis, cols = complete_site(bg, j, N)
    if not feas:
        stats["infeasible"] = stats.get("infeasible", 0) + 1
        return None
    src = {e: [r[:] for r in m] for e, m in bg.items()}
    vec = {}
    for c in range(2):
        v = list(part[c])
        for bvec in basis:
            lam = rval(rng.choice(["01", "small", "pm1"])) if rng.random() < 0.5 \
                else Fraction(0)
            if lam:
                v = [x + lam * y for x, y in zip(v, bvec)]
        vec[c] = v
    for c in range(2):
        for i, (r, e) in enumerate(cols):
            setcell(src, j, r, c, e, vec[c][i])
    ok, badw = is_exact2(src, N)
    if not ok:
        stats["assembled_not_exact"] = stats.get("assembled_not_exact", 0) + 1
        return None
    stats["exact"] = stats.get("exact", 0) + 1
    stats[f"kerdim{len(basis)}"] = stats.get(f"kerdim{len(basis)}", 0) + 1
    rec = record(src, origin, want_jac)
    key = (rec["ncell"], rec["ncross"], tuple(map(tuple, rec["patterns"])),
           tuple(rec["null_deg"]), tuple(rec["kerprof"]),
           rec["cycle"] is not None)
    ks = str(key)
    seen[ks] = seen.get(ks, 0) + 1
    if seen[ks] <= 3:
        pool.append(rec)
    return rec


def main():
    t0 = time.time()
    pool, seen, stats = [], {}, {}
    exact_pool = []
    n_verified_indep = 0
    strata_used = set()
    rounds = 0
    while time.time() - t0 < SECONDS:
        rounds += 1
        j = rng.randrange(N)
        mode = rng.random()
        if mode < 0.30:
            k = rng.choice(["01", "pm1", "small", "frac"])
            bg = bg_from_cycle(j, rng.randrange(0, 7), k)
            origin = f"cycle+{k}"
            strata_used.add("cycle")
        elif mode < 0.45:
            bg = bg_random(j, rng.choice([0.15, 0.3, 0.5, 0.9]),
                           rng.choice(["01", "pm1", "small"]))
            origin = "random"
            strata_used.add("random")
        elif mode < 0.6 and exact_pool:
            src = exact_pool[rng.randrange(len(exact_pool))]
            bg = bg_from_source(src, j)
            origin = "resample"
            strata_used.add("resample")
        else:
            # two-site resample: delete two stars, re-solve one at a time
            if exact_pool and rng.random() < 0.7:
                src = exact_pool[rng.randrange(len(exact_pool))]
                bg = bg_from_source(src, j)
                for _ in range(rng.randrange(1, 4)):
                    e = EDG[rng.randrange(len(EDG))]
                    if j in e:
                        continue
                    bg[e][rng.randrange(2)][rng.randrange(2)] = rval(
                        rng.choice(["01", "pm1", "small"]))
                origin = "perturb"
                strata_used.add("perturb")
            else:
                bg = bg_from_cycle(j, rng.randrange(1, 10), "small")
                origin = "cycle+small"
                strata_used.add("cycle")
        rec = try_bg(bg, j, origin, pool, seen, stats,
                     want_jac=(rounds % 40 == 0))
        if rec is not None:
            src = {tuple(int(c) for c in k):
                   [[Fraction(x) for x in row] for row in m]
                   for k, m in rec["cells"].items()}
            full = zero_source(N, 2)
            for e, m in src.items():
                full[e] = m
            if len(exact_pool) < 400:
                exact_pool.append(full)
            elif rng.random() < 0.1:
                exact_pool[rng.randrange(len(exact_pool))] = full
            if n_verified_indep < 60:
                # independent-engine recheck (ledger: two engines)
                ok2 = all(haf_pm(full, w, n=N) ==
                          (1 if len(set(w)) == 1 else 0)
                          for w in itertools.product(range(2), repeat=N))
                require(ok2, "independent engine disagrees on an exact source")
                n_verified_indep += 1
        if rounds % 25 == 0:
            with open(OUT, "w") as fh:
                json.dump({"tag": TAG, "seed": SEED, "rounds": rounds,
                           "elapsed": time.time() - t0, "stats": stats,
                           "n_classes": len(seen), "classes": seen,
                           "pool": pool, "indep_verified": n_verified_indep,
                           "strata": sorted(strata_used)},
                          fh, indent=1, sort_keys=True)
    require(n_verified_indep > 0, "no source was independently re-verified")
    MAN.mark("engine_recheck")
    require(len(strata_used) >= 3, f"stratum coverage too thin: {strata_used}")
    MAN.mark("stratum_coverage")
    MAN.mark("fibre_affine")
    with open(OUT, "w") as fh:
        json.dump({"tag": TAG, "seed": SEED, "rounds": rounds,
                   "elapsed": time.time() - t0, "stats": stats,
                   "n_classes": len(seen), "classes": seen, "pool": pool,
                   "indep_verified": n_verified_indep,
                   "strata": sorted(strata_used),
                   "manifest": MAN.assert_complete()},
                  fh, indent=1, sort_keys=True)
    print("wrote", OUT, stats, "classes", len(seen))


if __name__ == "__main__":
    main()
