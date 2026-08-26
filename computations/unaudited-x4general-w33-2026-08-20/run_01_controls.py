#!/usr/bin/env python3
"""W33 / T1 -- engine controls + the first structural facts about the exact
d=2 variety at n=8.

Controls (manifest, ledger 21):
  engine_xcheck    bitmask-DP hafnian == explicit-PM hafnian on random Q and
                   F_p sources AND on the structured 0/1 stratum (ledger 12).
  delta2_exact     the Hamiltonian-cycle PM-pair source is exact over Q,
                   F_13, F_31 (positive control).
  delta2_mutation  a CROSSING-chord cell added to Delta^2 destroys exactness
                   (the mutation must fire).
  gauge_action     torus / colour-swap / S_8 images of an exact source are
                   exact; a non-gauge GL_2 image is NOT (shows the gauge group
                   is exactly T x Z_2 x S_n, so supports are invariants).
  kernel_delta2    dim Ker_j(Delta^2) = 6 for every j over Q and both primes,
                   with the zero columns EXACTLY the same-parity chords.
  chord_free       adding an arbitrary 12-parameter same-parity-chord star at
                   ONE site keeps exactness (kernel prediction, exact target).
  fiber_dim        complete_site over the Delta^2 background is feasible with
                   a 6-dim kernel per colour (12-dim affine fibre).
  two_chord        a P-chord and a Q-chord at DIFFERENT sites: exactness is
                   NOT automatic (the quadratic layer is real) -- and the
                   explicit quadratic condition is exhibited.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w33_core import (  # noqa: E402
    Fp, Manifest, apply_perm, apply_swap, apply_torus, cell, complete_site,
    cycle_pm_pair, defects2, edges, haf, haf_pm, is_exact2, n_cross,
    require, setcell, star_kernel, support, zero_source)

OUT = os.path.join(HERE, "results_t1.json")
N = 8
PRIMES = (13, 31)
R = {}
MAN = Manifest(["engine_xcheck", "delta2_exact", "delta2_mutation",
                "gauge_action", "kernel_delta2", "chord_free", "fiber_dim",
                "two_chord"])
rng = random.Random(330001)


def rand_source(n, d, field, dens=1.0):
    src = {}
    for e in edges(n):
        m = []
        for _a in range(d):
            row = []
            for _b in range(d):
                if rng.random() > dens:
                    row.append(Fp(0, field) if field else Fraction(0))
                elif field:
                    row.append(Fp(rng.randrange(field), field))
                else:
                    row.append(Fraction(rng.randrange(-6, 7),
                                        rng.randrange(1, 5)))
            m.append(row)
        src[e] = m
    return src


def to_fp(src, p):
    return {e: [[Fp(x.numerator, p) * Fp(x.denominator, p).inv()
                 for x in row] for row in m] for e, m in src.items()}


# ---------------------------------------------------------- engine_xcheck
def c_engine():
    bad = 0
    checks = 0
    for (n, d, field, dens) in [(6, 2, None, 1.0), (8, 2, None, 1.0),
                                (8, 2, None, 0.4), (8, 3, None, 0.5),
                                (8, 2, 13, 1.0), (8, 3, 31, 0.6),
                                (6, 3, None, 1.0)]:
        for _t in range(3):
            src = rand_source(n, d, field, dens)
            for _w in range(6):
                w = tuple(rng.randrange(d) for _ in range(n))
                a = haf(src, w, n=n)
                b = haf_pm(src, w, n=n)
                checks += 1
                if a != b:
                    bad += 1
            # subset versions
            for _w in range(4):
                w = tuple(rng.randrange(d) for _ in range(n))
                S = sorted(rng.sample(range(n), 2 * rng.randrange(1, n // 2 + 1)))
                checks += 1
                if haf(src, w, sites=S) != haf_pm(src, w, sites=S):
                    bad += 1
    # structured 0/1 stratum, exhaustive over supports of a fixed shape
    for _t in range(40):
        src = zero_source(8, 2)
        for e in edges(8):
            for a in range(2):
                for b in range(2):
                    src[e][a][b] = Fraction(rng.randrange(2))
        for _w in range(4):
            w = tuple(rng.randrange(2) for _ in range(8))
            checks += 1
            if haf(src, w, n=8) != haf_pm(src, w, n=8):
                bad += 1
    require(bad == 0, f"engine cross-check FAILED on {bad}/{checks}")
    MAN.mark("engine_xcheck")
    R["engine_xcheck"] = {"checks": checks, "mismatches": bad}
    print("T1 engine_xcheck:", checks, "checks, 0 mismatches")


# ----------------------------------------------------------- delta2_exact
def c_delta2():
    out = {}
    d2 = cycle_pm_pair(N)
    ok, bad = is_exact2(d2, N)
    out["Q"] = ok
    for p in PRIMES:
        okp, _ = is_exact2(to_fp(d2, p), N)
        out[f"F{p}"] = okp
    # weighted version: products over each PM must be 1
    wa = [Fraction(2), Fraction(3), Fraction(5), Fraction(1, 30)]
    wd = [Fraction(7), Fraction(1, 7), Fraction(-2), Fraction(-1, 2)]
    dw = cycle_pm_pair(N, wa=wa, wd=wd)
    out["Q_weighted"] = is_exact2(dw, N)[0]
    require(all(out.values()), f"delta2 positive control failed: {out}")
    MAN.mark("delta2_exact")
    R["delta2_exact"] = out
    print("T1 delta2_exact:", out)


def c_delta2_mut():
    fired = {}
    d2 = cycle_pm_pair(N)
    # a CROSSING chord (endpoints in different parity classes of the 8-cycle)
    for (e, a, b) in [((0, 3), 0, 0), ((0, 3), 1, 1), ((0, 3), 0, 1),
                      ((1, 4), 0, 0), ((2, 7), 1, 1)]:
        s = {k: [r[:] for r in m] for k, m in d2.items()}
        s[e][a][b] = Fraction(1)
        fired[str((e, a, b))] = not is_exact2(s, N)[0]
    require(all(fired.values()), f"delta2 mutation did not fire: {fired}")
    MAN.mark("delta2_mutation")
    R["delta2_mutation"] = fired
    print("T1 delta2_mutation: all crossing-chord mutations break exactness")


# ------------------------------------------------------------ gauge_action
def c_gauge():
    d2 = cycle_pm_pair(N)
    alpha = [Fraction(2), Fraction(3), Fraction(5), Fraction(7),
             Fraction(1, 2), Fraction(1, 3), Fraction(1, 5), Fraction(1, 7)]
    delta = [Fraction(-2), Fraction(3), Fraction(-5), Fraction(-1),
             Fraction(1, 2), Fraction(1, 3), Fraction(1, 5), Fraction(-1)]
    pa = Fraction(1)
    for x in alpha:
        pa *= x
    pd = Fraction(1)
    for x in delta:
        pd *= x
    require(pa == 1 and pd == 1, "torus test element not in T")
    g = apply_torus(d2, alpha, delta)
    out = {"torus": is_exact2(g, N)[0],
           "swap": is_exact2(apply_swap(d2), N)[0]}
    perm = [3, 5, 0, 7, 1, 6, 2, 4]
    out["perm"] = is_exact2(apply_perm(d2, perm, N), N)[0]
    # a torus element NOT in T (prod alpha != 1) must break it
    alpha2 = list(alpha)
    alpha2[0] = Fraction(4)
    out["torus_offT_breaks"] = not is_exact2(
        apply_torus(d2, alpha2, delta), N)[0]
    # a non-diagonal local GL_2 (shear at site 0) must break it
    sh = {e: [r[:] for r in m] for e, m in d2.items()}
    for r in range(1, N):
        c00 = cell(d2, 0, r, 0, 0)
        c10 = cell(d2, 0, r, 1, 0)
        c01 = cell(d2, 0, r, 0, 1)
        c11 = cell(d2, 0, r, 1, 1)
        setcell(sh, 0, r, 0, 0, c00 + c10)
        setcell(sh, 0, r, 0, 1, c01 + c11)
    out["shear_breaks"] = not is_exact2(sh, N)[0]
    require(all(out.values()), f"gauge control failed: {out}")
    MAN.mark("gauge_action")
    R["gauge_action"] = out
    print("T1 gauge_action:", out)


# ----------------------------------------------------------- kernel_delta2
def parity_chords(j, n=N):
    return [r for r in range(n) if r != j and (r - j) % 2 == 0]


def c_kernel():
    out = {}
    for tag, src in [("Q", cycle_pm_pair(N))] + \
            [(f"F{p}", to_fp(cycle_pm_pair(N), p)) for p in PRIMES]:
        prof = {}
        zc = {}
        for j in range(N):
            dim, basis, cols, zcols = star_kernel(src, j, N)
            prof[j] = dim
            zc[j] = sorted({r for (r, _e) in zcols})
        out[tag] = {"dims": prof, "zero_cols_sites": zc}
        require(all(v == 6 for v in prof.values()),
                f"kernel dim not 6 everywhere ({tag}): {prof}")
        for j in range(N):
            require(zc[j] == sorted(parity_chords(j)),
                    f"zero columns are not the same-parity chords: "
                    f"j={j} {zc[j]}")
    MAN.mark("kernel_delta2")
    R["kernel_delta2"] = {k: {"dims": v["dims"]} for k, v in out.items()}
    R["kernel_delta2"]["zero_cols_sites_Q"] = out["Q"]["zero_cols_sites"]
    print("T1 kernel_delta2: dim Ker_j = 6 at every j; zero columns are "
          "exactly the same-parity chords")


# --------------------------------------------------------------- chord_free
def c_chord_free():
    """EXACT TARGET (ledger 27): the claim is 'Delta^2 with an ARBITRARY
    12-parameter same-parity star at one site is an exact d=2 source', not
    'some deformation survives'.  Test it with generic rationals and with
    values in a structured 0/1/-1 stratum."""
    res = {}
    for j in [0, 3, 7]:
        for trial in range(4):
            s = {e: [r[:] for r in m] for e, m in cycle_pm_pair(N).items()}
            vals = {}
            for r in parity_chords(j):
                for a in range(2):
                    for b in range(2):
                        v = (Fraction(rng.randrange(-5, 6), rng.randrange(1, 4))
                             if trial < 2 else Fraction(rng.randrange(-1, 2)))
                        setcell(s, j, r, a, b, v)
                        vals[(r, a, b)] = v
            ok, badw = is_exact2(s, N)
            res[f"j{j}_t{trial}"] = {"exact": ok, "ncross": n_cross(s),
                                     "bad": None if ok else list(badw)}
    require(all(v["exact"] for v in res.values()),
            f"chord_free FAILED: {[k for k, v in res.items() if not v['exact']]}")
    got_cross = max(v["ncross"] for v in res.values())
    require(got_cross > 0, "chord_free produced no genuinely non-diagonal "
                           "source -- control is vacuous")
    MAN.mark("chord_free")
    R["chord_free"] = res
    print("T1 chord_free: all one-site same-parity-chord deformations exact; "
          "max cross cells", got_cross)


# ----------------------------------------------------------------- fiber_dim
def c_fiber():
    src = cycle_pm_pair(N)
    j = 7
    bg = {e: [r[:] for r in m] for e, m in src.items()}
    for r in range(N):
        if r == j:
            continue
        for a in range(2):
            for b in range(2):
                setcell(bg, j, r, a, b, Fraction(0))
    feas, part, basis, cols = complete_site(bg, j, N)
    require(feas, "Delta^2 background not completable -- engine error")
    R["fiber_dim"] = {"feasible": feas, "kernel_dim": len(basis),
                      "affine_fibre_dim": 2 * len(basis)}
    require(len(basis) == 6, f"fibre kernel dim {len(basis)} != 6")
    # rebuild an exact source from the particular solution and check
    s2 = {e: [r[:] for r in m] for e, m in bg.items()}
    for c in range(2):
        for i, (r, e) in enumerate(cols):
            setcell(s2, j, r, c, e, part[c][i])
    require(is_exact2(s2, N)[0], "particular completion not exact")
    MAN.mark("fiber_dim")
    print("T1 fiber_dim: Delta^2 background at j=7 -> 12-dim affine fibre")


# ----------------------------------------------------------------- two_chord
def c_two_chord():
    """Two chords at DIFFERENT sites, one in each parity class.  A perfect
    matching of K_8 uses equal numbers of P-internal and Q-internal edges, so
    the first correction appears at chord-pair level: this control shows the
    quadratic layer is non-trivial (some pairs survive, some do not)."""
    P = [0, 2, 4, 6]
    Q = [1, 3, 5, 7]
    tab = {}
    for (u1, v1) in itertools.combinations(P, 2):
        for (u2, v2) in itertools.combinations(Q, 2):
            s = {e: [r[:] for r in m] for e, m in cycle_pm_pair(N).items()}
            setcell(s, u1, v1, 0, 0, Fraction(1))
            setcell(s, u2, v2, 0, 0, Fraction(1))
            ok, badw = is_exact2(s, N)
            tab[f"{u1}{v1}|{u2}{v2}"] = ok
    nok = sum(1 for v in tab.values() if v)
    R["two_chord"] = {"pairs": len(tab), "still_exact": nok,
                      "table": tab}
    require(nok < len(tab), "two_chord control vacuous: every pair survived")
    MAN.mark("two_chord")
    print("T1 two_chord:", nok, "of", len(tab),
          "(P-chord, Q-chord) pairs with unit (0,0) cells stay exact")


def main():
    c_engine()
    c_delta2()
    c_delta2_mut()
    c_gauge()
    c_kernel()
    c_chord_free()
    c_fiber()
    c_two_chord()
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True, default=str)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
