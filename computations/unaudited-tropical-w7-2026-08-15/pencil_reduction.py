#!/usr/bin/env python3
"""UNAUDITED PROBE (W7 / Route T.1) -- the diagonal reduction verdict.

Pinned HEAD: a41949965d41e5c63fb4bc1caf7b20c0df017856

TASK A's KEY QUESTION was whether the initial system at the central colour-form
cone is "a diagonal-pencil-type system".  Two things have to be separated,
because the committed material separates them and the brief did not:

  T(k)  TERMWISE:  h_r(V) != 0 for r=0,1,2 and h_0(S_0)h_1(S_1)h_2(S_2) = 0 for
        every proper ordered even split.  This is system (2) of
        proofs/diagonal-hafnian-recurrence-obstruction.md and is PROVED
        INSOLUBLE, characteristic-free, for n in {6,8,10}.

  P(k)  SUMMED PENCIL:  haf(x_0 W_0 + x_1 W_1 + x_2 W_2) = x_0^k + x_1^k + x_2^k.
        notes/diagonal-termwise-census-and-pencil-guard.md sections 1-2 prove
        T(k) => P(k) and that the converse FAILS: P(k) is SOLUBLE for every
        k >= 2 (alternating 2k-cycle), so -- in that note's words -- "no route
        through 'the pencil equation is unsatisfiable' can exist".

This script verifies EXACTLY which of the two the initial system reproduces, by
comparing monomial sets, not by asserting it.

CLAIM VERIFIED HERE.  Let g_ab > 0 for all a<b (the chamber where every
bichromatic colour pair is strictly expensive) and let f(c,c) = 0.  Then

  (1) for every mixed content with all n_c EVEN, the argmin type is uniquely
      (0,0,0) -- every edge monochromatic -- and
          in_w(Phi_chi) = h_0(S_0) h_1(S_1) h_2(S_2)
      as a polynomial identity in the diagonal cells W_c(u,v) = x[(u,v),c,c];
  (2) the pure initial forms are h_c(V) - 1;
  (3) the words of (1) realise EVERY proper ordered even split of the N sites.

So the initial system at that cone CONTAINS system (2) verbatim, and the
committed theorem applies: the cone is dead at N = 6, 8 (and 10).  It is the
TERMWISE system, not the pencil equation.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from initial_system_probe import Instance, perfect_matchings  # noqa: E402


def support(inst, chi, M):
    return tuple(inst.cell((u, v), chi[u], chi[v]) for u, v in M)


def haf_monomials(inst, subset, colour):
    """Monomial set (as frozensets of cell indices) of haf(W_colour[subset])."""
    out = set()
    for M in perfect_matchings(subset):
        out.add(frozenset(inst.cell(tuple(sorted(e)), colour, colour) for e in M))
    return out


def product_monomials(sets):
    out = {frozenset()}
    for s in sets:
        out = {a | b for a in out for b in s}
    return out


def check(nsites):
    inst = Instance(nsites, (1, 1, 1), (0, 0, 0))     # g > 0, f(c,c) = 0
    matchings = inst.matchings
    seen_splits = set()
    checked = 0
    for chi in product(range(3), repeat=nsites):
        n = tuple(sum(1 for c in chi if c == a) for a in range(3))
        if len(set(chi)) == 1:
            continue
        weights = [sum(inst.f[(chi[u], chi[v])] for u, v in M) for M in matchings]
        best = min(weights)
        sel = [M for M, wt in zip(matchings, weights) if wt == best]
        init = {frozenset(support(inst, chi, M)) for M in sel}
        if all(v % 2 == 0 for v in n):
            parts = [tuple(u for u in range(nsites) if chi[u] == c)
                     for c in range(3)]
            expect = product_monomials(
                [haf_monomials(inst, parts[c], c) for c in range(3)])
            if init != expect:
                raise AssertionError(
                    "initial form != split product at chi=%s" % (chi,))
            seen_splits.add(tuple(parts))
            checked += 1
        else:
            # odd content: the initial form MUST use off-diagonal cells
            uses_off = any(
                any(idx % 9 not in (0, 4, 8) for idx in mono) for mono in init)
            if not uses_off:
                raise AssertionError("odd content with a purely diagonal initial"
                                     " form at chi=%s" % (chi,))
    # every proper ordered even split realised?
    allsplits = set()
    for assign in product(range(3), repeat=nsites):
        parts = tuple(tuple(u for u in range(nsites) if assign[u] == c)
                      for c in range(3))
        if any(len(p) % 2 for p in parts):
            continue
        if max(len(p) for p in parts) == nsites:
            continue                                   # not a proper split
        allsplits.add(parts)
    return checked, len(seen_splits), len(allsplits), seen_splits == allsplits


def pure_check(nsites):
    inst = Instance(nsites, (1, 1, 1), (0, 0, 0))
    for c in range(3):
        chi = (c,) * nsites
        weights = [sum(inst.f[(chi[u], chi[v])] for u, v in M)
                   for M in inst.matchings]
        if min(weights) != 0 or weights.count(0) != len(weights):
            return False
    return True


def main():
    print("UNAUDITED PROBE (W7) -- diagonal reduction at the g>0 chamber")
    for nsites in (6, 8):
        checked, seen, total, ok = check(nsites)
        print("N = %d" % nsites)
        print("   even-content mixed words whose initial form is EXACTLY the"
              " split product h_0 h_1 h_2 : %d (all of them)" % checked)
        print("   proper ordered even splits realised: %d of %d  -> %s"
              % (seen, total, "ALL" if ok else "MISSING SOME"))
        print("   odd-content words: initial form always uses off-diagonal"
              " cells (extra equations, not needed): verified")
        print("   pure words: all matchings tie at weight 0, so"
              " in_w(Phi_c - 1) = h_c(V) - 1 : %s" % pure_check(nsites))
        print("   => the initial system CONTAINS committed system (2) at n = %d,"
              " which proofs/diagonal-hafnian-recurrence-obstruction.md proves"
              " INSOLUBLE." % nsites)
        print()
    print("VERDICT: the reduction is to the TERMWISE system T(k), not to the")
    print("summed pencil equation P(k).  P(k) is soluble at every k (committed")
    print("guard, notes/diagonal-termwise-census-and-pencil-guard.md sec.2), so a")
    print("reduction to P(k) would have been worthless.  The brief's premise")
    print("('the repo proved the pencil system insoluble') is incorrect as")
    print("stated; the correct citation is the termwise system.")


if __name__ == "__main__":
    main()
