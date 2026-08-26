"""AUDIT A1 / CLAIM 4: W3's PHASE-ONLY REDUCTION.

W3 (REPORT headline 4, adopted verbatim into master-plan v5):

  "x = 0 (all moduli 1) satisfies every modulus-level condition on any
   support with >= 2-term mixed fibres; ... the ENTIRE modulus-level content
   of the GHZ system is {M9 singleton, M8 missing pure}; everything else is
   PHASE ... searches may fix all moduli to 1 and work on the phase torus."

The operative, testable form of the CONSEQUENCE is:

  (PO)  if the (mixed) GHZ system is solvable on a support S with cells all
        nonzero, then it is solvable on S with all |a_s| = 1.

("all moduli 1" is the right normal form: the mixed equations are homogeneous
 and gauge-covariant, so a solution whose modulus vector lies in the gauge
 orbit of all-ones can be gauged to |a_s| = 1 exactly.)

KEY OBSERVATION (mine, and it is W3's own L1 turned against the claim): by
L1 every matching of a fixed word gets the SAME gauge weight.  Hence on the
gauge orbit of all-ones every fibre is EQUILATERAL -- all terms of one fibre
have equal modulus.  So (PO) asserts that solvability never needs a
non-equilateral fibre.  That is a strong, and testable, statement.

This module searches for a support where the general complex system is
solvable and the unit-modulus system is not.
"""

from __future__ import annotations

import itertools
import random

import numpy as np
from scipy.optimize import least_squares

from a1_core import COLS, all_cells, all_words, cellkey

# ------------------------------------------------------------------ fibres


def perfect_matchings(verts):
    if not verts:
        yield ()
        return
    head, rest = verts[0], verts[1:]
    for k, p in enumerate(rest):
        for tail in perfect_matchings(rest[:k] + rest[k + 1:]):
            yield ((head, p),) + tail


def fibres(n, S):
    """word -> list of matchings (each a tuple of cell keys), live in S."""
    S = set(S)
    MS = list(perfect_matchings(tuple(range(n))))
    out = {}
    for w in all_words(n):
        terms = []
        for M in MS:
            ks = [cellkey(u, v, w[u], w[v]) for (u, v) in M]
            if all(k in S for k in ks):
                terms.append(tuple(sorted(ks)))
        if terms:
            out[w] = terms
    return out


def is_mixed(w):
    return len(set(w)) > 1


# ------------------------------------------------------- residual machinery


def make_residual(n, S, fib, unit):
    Sl = sorted(S)
    idx = {s: i for i, s in enumerate(Sl)}
    mixed = [(w, terms) for w, terms in fib.items() if is_mixed(w)]
    rows = [[[idx[k] for k in M] for M in terms] for _, terms in mixed]

    def resid(p):
        if unit:
            u = np.zeros(len(Sl))
            th = p
        else:
            u = p[: len(Sl)]
            th = p[len(Sl):]
        z = np.exp(u + 1j * th)
        out = []
        for terms in rows:
            vals = np.array([np.prod(z[t]) for t in terms])
            den = np.sum(np.abs(vals))
            r = vals.sum() / den
            out.append(r.real)
            out.append(r.imag)
        return np.array(out)

    nvar = len(Sl) if unit else 2 * len(Sl)
    return resid, nvar, mixed


def feasible(n, S, fib, unit, tries=40, seed=0, tol=1e-11, bound=3.0):
    """Feasibility of the MIXED system with all cells nonzero.

    `bound` caps |log|a_s|| so the optimiser cannot fake a solution by
    letting a cell modulus run to 0 (which would silently shrink the
    support).  With unit=True the moduli are pinned to 1.
    """
    resid, nvar, mixed = make_residual(n, S, fib, unit)
    if not mixed:
        return True, 0.0, None
    rng = np.random.default_rng(seed)
    m = len(S)
    if unit:
        lo, hi = -np.inf, np.inf
    else:
        lo = np.concatenate([np.full(m, -bound), np.full(m, -np.inf)])
        hi = np.concatenate([np.full(m, bound), np.full(m, np.inf)])
    best = np.inf
    bestp = None
    for _ in range(tries):
        p0 = rng.uniform(-np.pi, np.pi, nvar)
        if not unit:
            p0[:m] = rng.uniform(-1.0, 1.0, m)
        try:
            sol = least_squares(resid, p0, bounds=(lo, hi), xtol=1e-15,
                                ftol=1e-15, gtol=1e-15, max_nfev=4000)
        except Exception:                                 # noqa: BLE001
            continue
        c = float(np.max(np.abs(sol.fun)))
        if c < best:
            best = c
            bestp = sol.x
        if best < tol:
            break
    return best < tol, best, bestp


# --------------------------------------------------------------- generators


def gen_random(n, rng, k):
    C = all_cells(n)
    return frozenset(rng.sample(C, k))


def gen_matching_union(n, rng, nm):
    """Union of the cells of `nm` random (matching, word) monomials -- gives
    supports whose fibres are small and interesting."""
    MS = list(perfect_matchings(tuple(range(n))))
    S = set()
    for _ in range(nm):
        M = rng.choice(MS)
        w = [rng.randrange(3) for _ in range(n)]
        for (u, v) in M:
            S.add(cellkey(u, v, w[u], w[v]))
    return frozenset(S)


def repair_singletons(n, S, rng, max_steps=400):
    """Delete cells until no mixed fibre is a singleton (W3's M9 silent).
    Terminates: every step removes one cell."""
    S = set(S)
    for _ in range(max_steps):
        fib = fibres(n, S)
        bad = [(w, t) for w, t in fib.items() if is_mixed(w) and len(t) == 1]
        if not bad:
            return frozenset(S), fib
        w, terms = rng.choice(bad)
        S.discard(rng.choice(list(terms[0])))
    return frozenset(S), fibres(n, S)


def no_singleton_mixed(fib):
    for w, terms in fib.items():
        if is_mixed(w) and len(terms) == 1:
            return False
    return True


def summarise(n, S, fib):
    sizes = {}
    for w, terms in fib.items():
        if is_mixed(w):
            sizes[len(terms)] = sizes.get(len(terms), 0) + 1
    return sizes


if __name__ == "__main__":
    import sys

    n = 6 if len(sys.argv) < 2 else int(sys.argv[1])
    print(f"AUDIT A1 / claim 4: hunting a support where the general complex")
    print(f"mixed system is solvable but the all-moduli-1 system is not (n={n}).")
    print("=" * 78)
    rng = random.Random(9001)
    found = []
    tested = 0
    for trial in range(400):
        mode = trial % 3
        if mode == 0:
            S0 = gen_matching_union(n, rng, rng.randint(4, 9))
        elif mode == 1:
            S0 = gen_random(n, rng, rng.randint(10, 22))
        else:
            S0 = gen_random(n, rng, rng.randint(22, 40))
        S, fib = repair_singletons(n, S0, rng)
        if not no_singleton_mixed(fib):
            continue
        mixed = [(w, t) for w, t in fib.items() if is_mixed(w)]
        if not mixed:
            continue
        tested += 1
        okU, resU, _ = feasible(n, S, fib, unit=True, tries=25, seed=trial)
        if okU:
            continue
        okG, resG, pG = feasible(n, S, fib, unit=False, tries=25, seed=trial)
        if okG and not okU:
            found.append((S, fib, resU, resG))
            print(f"  *** CANDIDATE (trial {trial}): |S|={len(S)} "
                  f"mixed fibres={len(mixed)} sizes={summarise(n,S,fib)} "
                  f"unit_resid={resU:.3e} general_resid={resG:.3e}")
            if len(found) >= 5:
                break
    print(f"tested {tested} singleton-free supports; candidates: {len(found)}")
    if found:
        S, fib, resU, resG = found[0]
        print("first candidate support (cells):")
        for s in sorted(S):
            print("   ", s)
