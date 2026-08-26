#!/usr/bin/env python3
"""A7 -- independent audit of MECHANISM W16-B ("a factoring site kills").

STATEMENT (re-derived here).  Suppose site t factors: every Gamma block at t
is rank one with a COMMON site-t vector gamma (gamma has no zero entry, all
cells of a Gamma block being nonzero).  Every M in F(Gamma) uses exactly one
edge at t, so prod_{uv in M} A_uv[w_u][w_v] = gamma[w_t] * (a factor free of
w_t).  Hence

        Phi_w = gamma[w_t] * Psi(w restricted off t).                    (F)

If w is mixed and effectively clean, H_w = Phi_w = 0, and gamma[w_t] != 0,
so Psi(w_{-t}) = 0; by (F) Phi vanishes at EVERY word of the t-fibre of w.
If some word w' of that fibre is mixed with exactly ONE extra matching then
H_{w'} = Phi_{w'} + (one monomial in occupied cells) = 0 forces that monomial
to vanish -- impossible for a source.  KILL.
With exactly TWO extras one gets a binomial mon1 + mon2 = 0.

This module computes, for each template and each site t, the exact inventory
of (clean word, k=1 fibre-mate) and (clean word, k=2 fibre-mate) pairs, plus
a MUTATION CONTROL (a fake "clean" predicate must destroy the inventory).
"""
from __future__ import annotations
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import (W8_IMMUNE, MIXED, WORDS, F_gamma, k_of, gamma_edges,
                     EDGES, PM_E, cell_index, extras)

HERE = os.path.dirname(os.path.abspath(__file__))


def pair_inventory(T, verbose=False):
    Fg = F_gamma(T)
    kmap = {w: k_of(T, w, Fg) for w in WORDS}
    mixed = set(MIXED)
    deg = {u: sum(1 for e in gamma_edges(T) if u in e) for u in range(8)}
    out = {}
    for t in range(8):
        k1, k2 = [], []
        for w in MIXED:
            if kmap[w] != 0:
                continue
            for c in range(3):
                if c == w[t]:
                    continue
                w2 = w[:t] + (c,) + w[t + 1:]
                if w2 not in mixed:
                    continue
                if kmap[w2] == 1:
                    k1.append((w, w2))
                elif kmap[w2] == 2:
                    k2.append((w, w2))
        out[t] = dict(gamma_degree=deg[t], n_k1_pairs=len(k1),
                      n_k2_pairs=len(k2),
                      example_k1=("".join(map(str, k1[0][0])),
                                  "".join(map(str, k1[0][1]))) if k1 else None,
                      example_k2=("".join(map(str, k2[0][0])),
                                  "".join(map(str, k2[0][1]))) if k2 else None)
    return out


def verify_factorisation_identity(T, t):
    """CONTROL: check (F) symbolically on a planted factoring configuration --
    i.e. that Phi_w / gamma[w_t] is independent of w_t, for a random exact
    assignment in which site t factors."""
    from fractions import Fraction
    import random
    rnd = random.Random(1000 + t)
    Fg = F_gamma(T)
    G = set()
    for e in gamma_edges(T):
        G.add(e)
    # build blocks: Gamma blocks at t are rank one with common t-vector gamma
    gamma = [Fraction(rnd.randrange(1, 7)) for _ in range(3)]
    A = {}
    for ei, e in enumerate(EDGES):
        if T[ei] == 0:
            continue
        u, v = e
        if T[ei] == 511 and t in e:
            other = [Fraction(rnd.randrange(1, 7)) for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    val = gamma[i] * other[j] if u == t else other[i] * gamma[j]
                    A[(ei, 3 * i + j)] = val
        else:
            for c in range(9):
                if (T[ei] >> c) & 1:
                    A[(ei, c)] = Fraction(rnd.randrange(1, 9))
    def Phi(w):
        tot = Fraction(0)
        for mi in Fg:
            p = Fraction(1)
            for e in PM_E[mi]:
                p *= A[(e, cell_index(e, w))]
            tot += p
        return tot
    bad = 0
    tested = 0
    for _ in range(300):
        w = tuple(rnd.randrange(3) for _ in range(8))
        vals = []
        for c in range(3):
            w2 = w[:t] + (c,) + w[t + 1:]
            vals.append(Phi(w2) / gamma[c])
        tested += 1
        if len(set(vals)) != 1:
            bad += 1
    return dict(tested=tested, mismatches=bad)


def mutation_control(T):
    """A deliberately WRONG clean predicate (k <= 1 counted as clean) must
    change the k=1 inventory -- the detector must be sensitive."""
    Fg = F_gamma(T)
    kmap = {w: k_of(T, w, Fg) for w in WORDS}
    mixed = set(MIXED)
    real = fake = 0
    for w in MIXED:
        for t in range(8):
            for c in range(3):
                if c == w[t]:
                    continue
                w2 = w[:t] + (c,) + w[t + 1:]
                if w2 not in mixed:
                    continue
                if kmap[w] == 0 and kmap[w2] == 1:
                    real += 1
                if kmap[w] <= 1 and kmap[w2] == 1:
                    fake += 1
    return dict(real=real, fake=fake, fired=(real != fake))


def main():
    res = {}
    for m in range(24, 29):
        T = W8_IMMUNE[m]
        inv = pair_inventory(T)
        res["m%d" % m] = inv
        print("m=%d" % m)
        for t in range(8):
            d = inv[t]
            print("   site %d (deg %d): k=1 pairs %5d   k=2 pairs %5d  ex1=%s"
                  % (t, d["gamma_degree"], d["n_k1_pairs"], d["n_k2_pairs"],
                     d["example_k1"]))
    res["identity_control_m25_site6"] = verify_factorisation_identity(
        W8_IMMUNE[25], 6)
    print("CONTROL (F) at m=25 site 6:", res["identity_control_m25_site6"])
    res["identity_control_m28_site0"] = verify_factorisation_identity(
        W8_IMMUNE[28], 0)
    print("CONTROL (F) at m=28 site 0:", res["identity_control_m28_site0"])
    res["mutation_control_m25"] = mutation_control(W8_IMMUNE[25])
    print("MUTATION control m=25:", res["mutation_control_m25"])
    json.dump(res, open(os.path.join(HERE, "results_factoring.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
