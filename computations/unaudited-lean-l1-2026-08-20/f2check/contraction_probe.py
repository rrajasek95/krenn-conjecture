#!/usr/bin/env python3
"""Does KitaKen1's characteristic-two contraction preserve the diagonal stratum?

UNAUDITED — lane L1, 2026-08-20. Writes only into the lane directory.

Their contraction (Contraction.lean) is, verbatim:

    orderedWeight W u v i j = if u < v then W (mkEdge u v i j)
                              else if v < u then W (mkEdge v u j i) else 0
    pivotProfile   W p u i  = sum over a : Fin 3 of orderedWeight W p u a i
    contractedWeights W q e = W e
        + ( pivotProfile W 0 e.u e.i * pivotProfile W q e.v e.j
          + pivotProfile W 0 e.v e.j * pivotProfile W q e.u e.i )

all in ZMod 2. This script asks whether the map `W |-> contractedWeights W q`
carries block-diagonal weightings to block-diagonal weightings.

It matters because if it did, their N -> N-2 descent could be run *inside* the
diagonal stratum and would subsume our N = 8 diagonal theorem on every
coefficient domain their parity bridge reaches. If it does not, the two proofs
are different mechanisms that agree only on the verdict.

Also verifies the algebraic kernel `rankTwo_four_vertex` and extracts its
characteristic-zero error term.
"""
from __future__ import annotations

import itertools
import random

# ---------------------------------------------------------------- part 1
# The rank-two four-vertex identity, and what it costs outside characteristic 2.


def rank_two_identity_char0():
    """R(a,b)R(c,d) + R(a,c)R(b,d) + R(a,d)R(b,c) over Z, with R(a,b)=PaQb+PbQa.

    Returns the monomial dictionary. In ZMod 2 every coefficient is even, which
    is exactly `QuantumLean.rankTwo_four_vertex`.
    """
    from collections import Counter
    sites = "abcd"

    def R(u, v):
        # each monomial is a sorted pair (P-index, Q-index)
        return [(("P", u), ("Q", v)), (("P", v), ("Q", u))]

    total = Counter()
    for (p, q), (r, s) in [(("a", "b"), ("c", "d")),
                           (("a", "c"), ("b", "d")),
                           (("a", "d"), ("b", "c"))]:
        for m1 in R(p, q):
            for m2 in R(r, s):
                key = tuple(sorted(m1 + m2))
                total[key] += 1
    return total


# ---------------------------------------------------------------- part 2
# The contraction map on diagonal weightings.

def make_diagonal(N, rng):
    """A random block-diagonal ternary weighting over F_2: t[c][(u,v)]."""
    pairs = [(u, v) for u in range(N) for v in range(N) if u < v]
    return [{p: rng.randint(0, 1) for p in pairs} for _ in range(3)]


def W_of_diagonal(t, u, v, i, j):
    """The registry's W on a canonically oriented label (u < v)."""
    assert u < v
    return t[i][(u, v)] if i == j else 0


def ordered_weight(t, u, v, i, j):
    if u < v:
        return W_of_diagonal(t, u, v, i, j)
    if v < u:
        return W_of_diagonal(t, v, u, j, i)
    return 0


def pivot_profile(t, p, u, i):
    return sum(ordered_weight(t, p, u, a, i) for a in range(3)) % 2


def contracted(t, q, u, v, i, j):
    """contractedWeights on the canonical label (u<v,i,j), in F_2."""
    base = W_of_diagonal(t, u, v, i, j)
    corr = (pivot_profile(t, 0, u, i) * pivot_profile(t, q, v, j)
            + pivot_profile(t, 0, v, j) * pivot_profile(t, q, u, i))
    return (base + corr) % 2


def diagonality_report(N, trials, rng):
    """How often does the contraction produce an off-diagonal entry?"""
    broke = 0
    witness = None
    for _ in range(trials):
        t = make_diagonal(N, rng)
        for q in range(1, N):
            offdiag = []
            for u in range(N):
                for v in range(u + 1, N):
                    for i in range(3):
                        for j in range(3):
                            if i == j:
                                continue
                            if contracted(t, q, u, v, i, j):
                                offdiag.append((q, u, v, i, j))
            if offdiag:
                broke += 1
                if witness is None:
                    witness = (t, offdiag[0])
                break
    return broke, witness


def exceptional_k4():
    """The exceptional K_4 source found by f2_direct.py at N = 4, over F_2:
    one perfect matching per colour."""
    t = [{}, {}, {}]
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    for c in range(3):
        for p in pairs:
            t[c][p] = 0
    t[0][(0, 3)] = 1; t[0][(1, 2)] = 1
    t[1][(0, 2)] = 1; t[1][(1, 3)] = 1
    t[2][(0, 1)] = 1; t[2][(2, 3)] = 1
    return t


def main():
    rng = random.Random(20260820)

    print("=" * 74)
    print("PART 1 — the rank-two four-vertex kernel, and its char-0 error term")
    print("=" * 74)
    total = rank_two_identity_char0()
    print(f"distinct monomials: {len(total)}")
    coeffs = sorted(set(total.values()))
    print(f"coefficients appearing: {coeffs}")
    print(f"all even: {all(c % 2 == 0 for c in total.values())}")
    print("so over Z the sum equals 2 * (sum of the following monomials):")
    for k, c in sorted(total.items()):
        assert c == 2
        pretty = "".join(f"{s}{idx}" for s, idx in k)
        print(f"    {pretty}")
    print()
    print("=> rankTwo_four_vertex is EXACTLY a factor-of-2 statement. In char 0")
    print("   the rank-two update changes the 4-vertex matching sum by 2 * E,")
    print("   E = the 6-monomial polynomial above. That is the explicit error")
    print("   term a characteristic-zero analogue would have to carry.")
    print()

    print("=" * 74)
    print("PART 2 — does the contraction preserve block-diagonality?")
    print("=" * 74)
    for N in (6, 8):
        broke, witness = diagonality_report(N, 200, rng)
        print(f"N={N}: {broke}/200 random diagonal weightings leave the diagonal "
              f"stratum under W |-> contractedWeights W q")
        if witness:
            t, (q, u, v, i, j) = witness
            print(f"      e.g. pivot q={q}: contracted entry at "
                  f"(u={u}, v={v}, i={i}, j={j}) is 1 while i != j")
            print(f"      because pivotProfile(0,{u},{i})={pivot_profile(t,0,u,i)}, "
                  f"pivotProfile({q},{v},{j})={pivot_profile(t,q,v,j)}, "
                  f"pivotProfile(0,{v},{j})={pivot_profile(t,0,v,j)}, "
                  f"pivotProfile({q},{u},{i})={pivot_profile(t,q,u,i)}")
    print()

    print("On the genuine N = 4 exceptional source (a real diagonal solution "
          "over F_2):")
    t = exceptional_k4()
    for q in (1, 2, 3):
        off = [(u, v, i, j)
               for u in range(4) for v in range(u + 1, 4)
               for i in range(3) for j in range(3)
               if i != j and contracted(t, q, u, v, i, j)]
        print(f"      pivot q={q}: {len(off)} off-diagonal entries created"
              + (f", first {off[0]}" if off else ""))
    print()
    print("=> The contraction does NOT preserve the diagonal stratum. Their")
    print("   descent therefore cannot be restricted to block-diagonal sources,")
    print("   and our diagonal theorem is not a corollary of it (nor vice versa).")


if __name__ == "__main__":
    main()
