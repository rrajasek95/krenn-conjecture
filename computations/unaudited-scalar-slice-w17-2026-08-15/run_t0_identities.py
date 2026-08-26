#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T0: identity + cross-check + mutation controls.

C1  three W17 evaluators agree (direct / closed form / cap identity), h=2,3.
C2  rank-one error == general-K error at K = u (x) v (h=2 and h=3).
C3  cross-check against P2's 81 quadrics (h=2, keyed by word).
C4  cross-check against P1's direct_error_tensor (h=3, keyed by word).
C5  h=2 structure theorem W17.1 predicate == (E == 0), on random AND on
    engineered degenerate instances (|I| = 0,1,2,3,4 realised).
C6  mutation controls: single-entry perturbations flip the verdicts.
C7  W5 scalar shadow: the monochrome component of the rank-one error at the
    diagonal cap u = v = e_c reproduces slice_core.slice_error.
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

from w17_core import (COLORS, alpha_beta, cap_scalars, ekey, ghz_coefficient,
                      h2_structure_predicate, oriented, rank_one_error_closed,
                      rank_one_error_direct, rank_one_error_identity,
                      site_rank, require)
from w17_general import general_cap_error, outer

RESULTS = {}
FAILS = []


def check(name, condition, detail=""):
    if condition:
        RESULTS.setdefault(name, {"pass": 0, "fail": 0})["pass"] += 1
    else:
        RESULTS.setdefault(name, {"pass": 0, "fail": 0})["fail"] += 1
        FAILS.append((name, str(detail)[:400]))


def random_source(rng, n, lo=-4, hi=4, zero_prob=0.0):
    src = {}
    for u, v in combinations(range(n), 2):
        src[(u, v)] = [[Fraction(0) if rng.random() < zero_prob
                        else Fraction(rng.randint(lo, hi))
                        for _ in range(3)] for _ in range(3)]
    return src


def random_vec(rng, lo=-4, hi=4):
    while True:
        w = [Fraction(rng.randint(lo, hi)) for _ in range(3)]
        if any(x != 0 for x in w):
            return w


def sites_of(n, p, q):
    return tuple(a for a in range(n) if a not in (p, q))


# ------------------------------------------------------------------ C1/C2


def c1_c2(rng, trials=12):
    for n in (6, 8):
        for _ in range(trials):
            src = random_source(rng, n)
            p, q = rng.sample(range(n), 2)
            p, q = min(p, q), max(p, q)
            U = sites_of(n, p, q)
            u, v = random_vec(rng), random_vec(rng)
            e1 = rank_one_error_direct(src, p, q, u, v, U)
            e2 = rank_one_error_closed(src, p, q, u, v, U)
            check(f"C1_direct_vs_closed_n{n}", e1 == e2, (p, q, u, v))
            s, _ = cap_scalars(src, p, q, u, v)
            if s != 0:
                e3 = rank_one_error_identity(src, p, q, u, v, U)
                check(f"C1_direct_vs_identity_n{n}", e1 == e3, (p, q, u, v))
            eg = general_cap_error(src, p, q, outer(u, v), U)
            check(f"C2_rankone_vs_general_n{n}", e1 == eg, (p, q, u, v))


# --------------------------------------------------------------------- C3


def c3(rng, trials=8):
    sys.path.insert(0, os.path.join(REPO, "unaudited-witness-splitting-p2-"
                                          "2026-08-15"))
    import wsplit_core as P2
    for _ in range(trials):
        src = random_source(rng, 6)
        blocks = {k: [[x for x in row] for row in v] for k, v in src.items()}
        p2src = P2.Source(blocks)
        p, q = rng.sample(range(6), 2)
        p, q = min(p, q), max(p, q)
        U = sites_of(6, p, q)
        pd = P2.PairData(p2src, p, q)
        u, v = random_vec(rng), random_vec(rng)
        K = outer(u, v)
        # P2's word order: for w0..w3 over pd.U in order; keep only nonzero.
        p2vals = {}
        idx = 0
        for word in product(range(3), repeat=4):
            quad = {}
            a, b, c, d = pd.U
            position = {a: 0, b: 1, c: 2, d: 3}
            for (e1, e2) in pd.matchings:
                lin1 = pd.R[e1][word[position[e1[0]]]][word[position[e1[1]]]]
                lin2 = pd.R[e2][word[position[e2[0]]]][word[position[e2[1]]]]
                if P2.lin_is_zero(lin1) or P2.lin_is_zero(lin2):
                    continue
                P2.quad_add(quad, P2.lin_mul(lin1, lin2))
            value = Fraction(0)
            flatK = [K[i][j] for i in range(3) for j in range(3)]
            for (i, j), coeff in quad.items():
                value += coeff * flatK[i] * flatK[j]
            if value != 0:
                p2vals[word] = value
            idx += 1
        mine = rank_one_error_direct(src, p, q, u, v, U)
        check("C3_vs_P2_quadrics", mine == p2vals,
              (p, q, sorted(mine.items())[:2], sorted(p2vals.items())[:2]))


# --------------------------------------------------------------------- C4


def load_module(name, path):
    """Load a module from an explicit file, registering it under `name`
    (P1 and P2 both ship a module called wsplit_core)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def c4(rng, trials=5):
    d = os.path.join(REPO, "unaudited-witness-splitting-p1-2026-08-15")
    saved = sys.modules.pop("wsplit_core", None)
    P1 = load_module("wsplit_core", os.path.join(d, "wsplit_core.py"))
    P1S = load_module("wsplit_sources", os.path.join(d, "wsplit_sources.py"))
    for _ in range(trials):
        src = random_source(rng, 8)
        p, q = rng.sample(range(8), 2)
        p, q = min(p, q), max(p, q)
        U = sites_of(8, p, q)
        u, v = random_vec(rng), random_vec(rng)
        charted = P1S.rechart(src, p, q)
        cap = tuple(u[i] * v[j] for i in range(3) for j in range(3))
        p1 = P1.direct_error_tensor(charted, cap)
        mine = rank_one_error_direct(src, p, q, u, v, U)
        # P1 words are indexed by its U = (2..7) in order == sorted physical U
        p1keyed = {w: val for w, val in p1.items() if val != 0}
        check("C4_vs_P1_tensor", mine == p1keyed,
              (p, q, len(mine), len(p1keyed)))
    sys.modules.pop("wsplit_core", None)
    sys.modules.pop("wsplit_sources", None)
    if saved is not None:
        sys.modules["wsplit_core"] = saved


# --------------------------------------------------------------------- C5


def engineered_degenerate(rng, n, p, q, u, v, ndegen):
    """A source whose first `ndegen` U-sites have alpha_a || beta_a."""
    src = random_source(rng, n)
    U = sites_of(n, p, q)
    # pick c with v_c != 0
    cv = next(c for c in COLORS if v[c] != 0)
    for a in U[:ndegen]:
        apa = oriented(src, p, a)
        alpha_a = [sum(u[i] * apa[i][c] for i in range(3)) for c in COLORS]
        mu = Fraction(rng.randint(-3, 3))
        # A_qa = e_cv/v_cv (x) (mu*alpha_a)  =>  A_qa^T v = mu*alpha_a
        table = [[Fraction(0)] * 3 for _ in range(3)]
        for c in COLORS:
            table[cv][c] = mu * alpha_a[c] / v[cv]
        if q < a:
            src[(q, a)] = table
        else:
            src[(a, q)] = [[table[j][i] for j in range(3)] for i in range(3)]
    return src


def c5(rng, trials=40):
    seen_I = {}
    for _ in range(trials):
        for ndeg in (0, 1, 2, 3, 4):
            p, q = 0, 1
            u, v = random_vec(rng), random_vec(rng)
            src = engineered_degenerate(rng, 6, p, q, u, v, ndeg)
            U = sites_of(6, p, q)
            e = rank_one_error_direct(src, p, q, u, v, U)
            ok, diag = h2_structure_predicate(src, p, q, u, v, U)
            check("C5_h2_structure", ok == (len(e) == 0),
                  (ndeg, ok, len(e), diag["ranks"]))
            seen_I[len(diag["I"])] = seen_I.get(len(diag["I"]), 0) + 1
    return seen_I


def forced_clean_instance(rng, branch="I0"):
    """A six-site source + rank-one cap with E_pq(u (x) v) = 0.

    branch "I0": beta_a = m_a alpha_a at all four sites with e_2(m) = 0
                 (Theorem W17.1, |I| = 0 branch: e_2^hom(1,m) = e_2(m)).
    branch "I1": three sites degenerate with e_1 = e_2 = 0 on the ratios
                 (needs a primitive cube root of unity: done over Q(w) is
                 impossible, so we use t = (1, w, w^2) only symbolically;
                 the rational branch instead uses a ZERO ratio pattern).
    """
    p, q = 0, 1
    U = sites_of(6, p, q)
    u, v = random_vec(rng), random_vec(rng)
    cv = next(c for c in COLORS if v[c] != 0)
    src = random_source(rng, 6)
    m = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
    if m[0] + m[1] + m[2] == 0:
        return None
    m.append(-(m[0] * m[1] + m[0] * m[2] + m[1] * m[2])
             / (m[0] + m[1] + m[2]))
    for n, a in enumerate(U):
        apa = oriented(src, p, a)
        alpha_a = [sum(u[i] * apa[i][c] for i in range(3)) for c in COLORS]
        if all(x == 0 for x in alpha_a):
            return None
        table = [[Fraction(0)] * 3 for _ in range(3)]
        for c in COLORS:
            table[cv][c] = m[n] * alpha_a[c] / v[cv]
        if q < a:
            src[(q, a)] = table
        else:
            src[(a, q)] = [[table[j][i] for j in range(3)] for i in range(3)]
    return src, p, q, u, v, U


def c5_forced_clean(rng, trials=25):
    made = {"I0": 0, "admissible": 0}
    for _ in range(trials):
        inst = forced_clean_instance(rng)
        if inst is None:
            continue
        src, p, q, u, v, U = inst
        e = rank_one_error_direct(src, p, q, u, v, U)
        ok, diag = h2_structure_predicate(src, p, q, u, v, U)
        check("C5b_forced_clean_I0", len(e) == 0 and ok,
              (len(e), ok, diag["conditions"]))
        if len(diag["I"]) == 0:
            made["I0"] += 1
        s, kappa = cap_scalars(src, p, q, u, v)
        if s != 0 and all(k != 0 for k in kappa):
            made["admissible"] += 1
    return made


# --------------------------------------------------------------------- C6


def c6(rng, trials=25):
    """Mutation controls on genuinely clean rank-one instances:
    M1 perturbing a q-block entry dirties;  M2 perturbing a p-block entry
    dirties;  M3 perturbing an INTERNAL U-block does NOT (h=2 error is
    x-free -- the structural fact that separates h=2 from h>=3);
    M4 perturbing A_pq does not (h=2 error is s-free)."""
    stats = {"tested": 0, "M1": 0, "M2": 0, "M3_invariant": 0,
             "M4_invariant": 0}
    for _ in range(trials):
        inst = forced_clean_instance(rng)
        if inst is None:
            continue
        src, p, q, u, v, U = inst
        e = rank_one_error_direct(src, p, q, u, v, U)
        check("C6_base_clean", len(e) == 0, len(e))
        if len(e) != 0:
            continue
        stats["tested"] += 1
        for tag, key in (("M1", ekey(q, U[0])), ("M2", ekey(p, U[0]))):
            mutated = {k: [list(r) for r in val] for k, val in src.items()}
            mutated[key][0][0] += 1
            e2 = rank_one_error_direct(mutated, p, q, u, v, U)
            ok2, _ = h2_structure_predicate(mutated, p, q, u, v, U)
            check(f"C6_{tag}_mutation_dirties", (len(e2) != 0) == (not ok2),
                  (len(e2), ok2))
            if len(e2) != 0:
                stats[tag] += 1
        for tag, key in (("M3", ekey(U[0], U[1])), ("M4", ekey(p, q))):
            mutated = {k: [list(r) for r in val] for k, val in src.items()}
            mutated[key][0][0] += 1
            e2 = rank_one_error_direct(mutated, p, q, u, v, U)
            check(f"C6_{tag}_h2_invariance", len(e2) == 0, (tag, len(e2)))
            if len(e2) == 0:
                stats[f"{tag}_invariant"] += 1
    return stats


# --------------------------------------------------------------------- C7


def c7(rng, trials=10):
    """W5 shadow: with u = v = e_c the rank-one cap is the pure diagonal
    cap K = e_c (x) e_c and the (c,c,..,c) component of E must equal W5's
    scalar slice error of the colour-c weighting."""
    sys.path.insert(0, os.path.join(REPO,
                                    "unaudited-slice-dirtiness-w5-2026-08-15"))
    import slice_core as W5
    for n in (6, 8):
        for _ in range(trials):
            src = random_source(rng, n)
            p, q = 0, 1
            U = sites_of(n, p, q)
            for c in COLORS:
                u = [Fraction(1) if i == c else Fraction(0) for i in range(3)]
                v = list(u)
                e = rank_one_error_direct(src, p, q, u, v, U)
                mine = e.get((c,) * len(U), Fraction(0))
                w = {ekey(a, b): oriented(src, a, b)[c][c]
                     for a, b in combinations(range(n), 2)}
                theirs = W5.slice_error(w, p, q, U, check=True)
                check(f"C7_w5_scalar_shadow_n{n}", mine == theirs,
                      (c, mine, theirs))


def main():
    t0 = time.time()
    rng = random.Random(17)
    print("== W17 T0: identities, cross-checks, controls ==")
    c1_c2(rng)
    print(f"  C1/C2 done [{time.time() - t0:.0f}s]")
    c3(rng)
    print(f"  C3 done [{time.time() - t0:.0f}s]")
    c4(rng)
    print(f"  C4 done [{time.time() - t0:.0f}s]")
    seen = c5(rng)
    print(f"  C5 done, |I| histogram {seen} [{time.time() - t0:.0f}s]")
    made = c5_forced_clean(rng)
    print(f"  C5b done {made} [{time.time() - t0:.0f}s]")
    mut = c6(rng)
    print(f"  C6 done {mut} [{time.time() - t0:.0f}s]")
    c7(rng)
    print(f"  C7 done [{time.time() - t0:.0f}s]")
    print("\n-- results --")
    for name in sorted(RESULTS):
        r = RESULTS[name]
        print(f"  {name:34s} pass {r['pass']:4d}  fail {r['fail']:4d}")
    if FAILS:
        print("\n-- failures --")
        for name, detail in FAILS[:20]:
            print(f"  {name}: {detail}")
    with open(os.path.join(HERE, "results_t0_identities.json"), "w") as fh:
        json.dump({"results": RESULTS, "fails": FAILS[:50],
                   "I_histogram": {str(k): v for k, v in seen.items()}},
                  fh, indent=1, default=str)
    print(f"\nwrote results_t0_identities.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
