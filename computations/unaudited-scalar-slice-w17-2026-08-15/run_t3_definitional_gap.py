#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T3(a): the DEFINITIONAL GAP between W5's scalar
slice error and cleanliness of a rank-one cap.

Lemma W17.10 (verified here).  On the ALL-DEGENERATE stratum (every site of
U has alpha_a || beta_a, alpha_a = lambda_a gamma_a, beta_a = mu_a gamma_a)
and for any word w with gamma_a[w_a] != 0 for all a,

   E_w  =  (prod_a gamma_a[w_a])  *  E^{W5}_{pq}( scalar data )

where the scalar data is  u_a = lambda_a, v_a = mu_a, s = u^T A_pq v and
w_ab = A_ab[w_a][w_b] / (gamma_a[w_a] gamma_b[w_b]).  So W5's scalar slice
error is exactly ONE COMPONENT of the tensor cap error.

Consequences checked:
  * h = 2: every component is the SAME scalar times prod gamma, so on the
    all-degenerate stratum "W5-scalar-clean" == "cap-clean";
  * h >= 3: FALSE -- explicit admissible caps with W5 scalar error zero and
    cap error nonzero (the internal blocks enter with all nine components);
  * the torus-average idea: E is bihomogeneous of bidegree (h,h), so every
    monomial has positive multidegree in u and in v and the average over
    the coordinate torus vanishes identically -- no information.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(REPO, "unaudited-slice-dirtiness-w5-2026-08-15"))

import slice_core as W5
import w17_h3 as H3
from w17_core import (COLORS, alpha_beta, cap_scalars, ekey, oriented,
                      rank_one_error_direct, site_rank, site_ratio)

RESULTS = {}
FAILS = []


def check(name, cond, detail=""):
    RESULTS.setdefault(name, {"pass": 0, "fail": 0})
    RESULTS[name]["pass" if cond else "fail"] += 1
    if not cond:
        FAILS.append((name, str(detail)[:300]))


def random_source(rng, n, lo=-4, hi=4):
    return {(u, v): [[Fraction(rng.randint(lo, hi)) for _ in range(3)]
                     for _ in range(3)]
            for u, v in combinations(range(n), 2)}


def make_all_degenerate(rng, n, p, q, u, v):
    src = random_source(rng, n)
    U = tuple(a for a in range(n) if a not in (p, q))
    cv = next(c for c in COLORS if v[c] != 0)
    for a in U:
        apa = oriented(src, p, a)
        al = [sum(u[i] * apa[i][c] for i in range(3)) for c in COLORS]
        if all(x == 0 for x in al):
            return None
        mm = Fraction(rng.randint(1, 4))
        table = [[Fraction(0)] * 3 for _ in range(3)]
        for c in COLORS:
            table[cv][c] = mm * al[c] / v[cv]
        key = ekey(q, a)
        src[key] = (table if q < a
                    else [[table[j][i] for j in range(3)] for i in range(3)])
    return src, U


def scalar_data(source, p, q, U, u, v, word):
    """W5 scalar weighting attached to a word w with gamma_a[w_a] != 0."""
    alpha, beta = alpha_beta(source, p, q, u, v, U)
    gam = {}
    lam, mu = {}, {}
    for a in U:
        if site_rank(alpha[a], beta[a]) != 1:
            return None
        gam[a] = alpha[a] if any(x != 0 for x in alpha[a]) else beta[a]
        lam[a], mu[a] = site_ratio(alpha[a], beta[a])
    if any(gam[a][word[n]] == 0 for n, a in enumerate(U)):
        return None
    s, _ = cap_scalars(source, p, q, u, v)
    scal = {ekey(p, q): s}
    for n, a in enumerate(U):
        scal[ekey(p, a)] = lam[a]
        scal[ekey(q, a)] = mu[a]
    for i, a in enumerate(U):
        for j, b in enumerate(U):
            if a < b:
                scal[(a, b)] = (Fraction(oriented(source, a, b)[word[i]][word[j]])
                                / (gam[a][word[i]] * gam[b][word[j]]))
    factor = Fraction(1)
    for n, a in enumerate(U):
        factor *= gam[a][word[n]]
    return scal, factor


def main():
    t0 = time.time()
    rng = random.Random(4242)
    print("== W17 T3(a): W5 scalar predicate vs rank-one cap cleanliness ==")
    out = {"gap_instances": []}

    # ---- Lemma W17.10 on random all-degenerate instances
    for n in (6, 8):
        made = 0
        for _ in range(600):
            u = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
            v = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
            if any(x == 0 for x in u) or any(x == 0 for x in v):
                continue
            inst = make_all_degenerate(rng, n, 0, 1, u, v)
            if inst is None:
                continue
            src, U = inst
            s, kappa = cap_scalars(src, 0, 1, u, v)
            if s == 0 or any(k == 0 for k in kappa):
                continue
            err = rank_one_error_direct(src, 0, 1, u, v, U)
            for word in list(product(COLORS, repeat=len(U)))[:40]:
                data = scalar_data(src, 0, 1, U, u, v, word)
                if data is None:
                    continue
                scal, factor = data
                lhs = err.get(word, Fraction(0))
                rhs = factor * W5.slice_error_rank2(scal, 0, 1, tuple(U))
                check(f"W1710_component_identity_n{n}", lhs == rhs,
                      (word, lhs, rhs))
            made += 1
            if made >= 8:
                break

    # ---- h = 2: all components proportional  =>  scalar predicate suffices
    prop = 0
    for _ in range(400):
        u = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
        v = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
        if any(x == 0 for x in u) or any(x == 0 for x in v):
            continue
        inst = make_all_degenerate(rng, 6, 0, 1, u, v)
        if inst is None:
            continue
        src, U = inst
        err = rank_one_error_direct(src, 0, 1, u, v, U)
        alpha, beta = alpha_beta(src, 0, 1, u, v, U)
        gam = {a: (alpha[a] if any(x != 0 for x in alpha[a]) else beta[a])
               for a in U}
        base = None
        ok = True
        for word in product(COLORS, repeat=4):
            fac = Fraction(1)
            for nn, a in enumerate(U):
                fac *= gam[a][word[nn]]
            val = err.get(word, Fraction(0))
            if fac == 0:
                ok = ok and val == 0
                continue
            ratio = val / fac
            if base is None:
                base = ratio
            elif ratio != base:
                ok = False
        check("h2_all_components_proportional", ok, base)
        prop += 1
        if prop >= 12:
            break

    # ---- h = 3: construct the GAP (scalar error zero, cap error nonzero)
    found = 0
    for _ in range(4000):
        u = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
        v = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
        if any(x == 0 for x in u) or any(x == 0 for x in v):
            continue
        inst = make_all_degenerate(rng, 8, 0, 1, u, v)
        if inst is None:
            continue
        src, U = inst
        s, kappa = cap_scalars(src, 0, 1, u, v)
        if s == 0 or any(k == 0 for k in kappa):
            continue
        word = (0,) * 6
        data = scalar_data(src, 0, 1, U, u, v, word)
        if data is None:
            continue
        scal, factor = data
        # solve the single W5 scalar equation for one internal gamma-weight
        a0, b0 = U[0], U[1]
        rest = tuple(t for t in U if t not in (a0, b0))
        base = dict(scal)
        base[(a0, b0)] = Fraction(0)
        e0 = W5.slice_error_rank2(base, 0, 1, tuple(U))
        base[(a0, b0)] = Fraction(1)
        e1 = W5.slice_error_rank2(base, 0, 1, tuple(U))
        if e1 == e0:
            continue
        wsol = -e0 / (e1 - e0)
        alpha, beta = alpha_beta(src, 0, 1, u, v, U)
        gam = {a: (alpha[a] if any(x != 0 for x in alpha[a]) else beta[a])
               for a in U}
        newval = wsol * gam[a0][word[0]] * gam[b0][word[1]]
        src[ekey(a0, b0)][word[0]][word[1]] = newval
        data = scalar_data(src, 0, 1, U, u, v, word)
        scal, factor = data
        scalar_err = W5.slice_error_rank2(scal, 0, 1, tuple(U))
        err = rank_one_error_direct(src, 0, 1, u, v, U)
        check("gap_scalar_zero", scalar_err == 0, scalar_err)
        check("gap_component_zero", err.get(word, Fraction(0)) == 0,
              err.get(word))
        if scalar_err == 0 and err:
            found += 1
            if found <= 2:
                out["gap_instances"].append(
                    {"n": 8, "u": [str(x) for x in u], "v": [str(x) for x in v],
                     "scalar_error": "0",
                     "cap_error_nonzero_components": len(err),
                     "blocks": {f"{a},{b}": [[str(x) for x in row]
                                             for row in src[(a, b)]]
                                for a, b in combinations(range(8), 2)}})
        if found >= 6:
            break
    print(f"  h=3 gap instances (W5 scalar error ZERO, cap error NONZERO): "
          f"{found}")
    if out["gap_instances"]:
        g = out["gap_instances"][0]
        print(f"    example: u = {g['u']}, v = {g['v']}, cap error has "
              f"{g['cap_error_nonzero_components']} nonzero components of 729")

    # ---- bihomogeneity (the torus-average observation)
    src = random_source(rng, 8)
    eqs, _s = H3.rank_one_equations_h3(src, 0, 1, tuple(range(2, 8)))
    bideg = set()
    for f in eqs.values():
        for (mu2, mv2), _c in f.items():
            bideg.add((sum(mu2), sum(mv2)))
    print(f"  bidegrees present in the h=3 rank-one error: {sorted(bideg)} "
          f"(all (3,3) => every monomial has positive multidegree in u and "
          f"in v => the coordinate-torus average is identically zero)")
    out["bidegrees_h3"] = sorted(bideg)
    check("bihomogeneous_h3", bideg == {(3, 3)}, bideg)

    print("\n-- results --")
    for name in sorted(RESULTS):
        r = RESULTS[name]
        print(f"  {name:36s} pass {r['pass']:5d} fail {r['fail']:5d}")
    for name, detail in FAILS[:8]:
        print(f"   FAIL {name}: {detail}")
    out["results"] = RESULTS
    out["fails"] = FAILS[:20]
    with open(os.path.join(HERE, "results_t3_definitional_gap.json"),
              "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"\nwrote results_t3_definitional_gap.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
