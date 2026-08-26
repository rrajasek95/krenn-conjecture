#!/usr/bin/env python3
"""UNAUDITED PROBE (W7) -- independent brute-force control for the colour-form
reduction of colour_form_fan.py.

Pinned HEAD: a41949965d41e5c63fb4bc1caf7b20c0df017856

This script re-derives, WITHOUT the type/multiplicity combinatorics, the two
facts the fan enumeration rests on, by enumerating actual matchings and actual
cells exactly as W4's tropical_scout.py does:

  1. for a colour form w[(u,v),i,j] = f(i,j) with f symmetric, the multiset of
     matching weights of the word chi agrees with the type-based prediction
     sum_m count(m) * <m, g> + const(chi)  --- checked as multisets;
  2. the mixed-singleton verdict of the fan agrees with the direct scan over
     all 3^N words and all (N-1)!! matchings;
  3. CONTROLS: (a) a NON-symmetric colour form is not covered by the reduction
     and does produce singletons (so "symmetric" is load bearing, matching
     W4's 21 = 18 + 6 - 3 dimension count); (b) a random ambient weight has
     singletons; (c) mutation: perturbing one cell off the colour-form shape
     must break agreement in (1).
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from colour_form_fan import types_for_content, contents, build  # noqa: E402


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vertices[index]),) + tail)
    return tuple(out)


def word_weights(f, chi, matchings):
    """Exact multiset of matching weights for the colour form f."""
    return sorted(sum(f[(chi[u], chi[v])] for u, v in M) for M in matchings)


def predicted_weights(f, chi, nsites):
    """Same multiset, predicted from the type table and g."""
    n = tuple(sum(1 for c in chi if c == a) for a in range(3))
    g = {(a, b): f[(a, b)] - (f[(a, a)] + f[(b, b)]) * Fraction(1, 2)
         for a, b in ((0, 1), (0, 2), (1, 2))}
    const = sum(Fraction(n[c]) * f[(c, c)] for c in range(3)) * Fraction(1, 2)
    out = []
    for m, cnt in types_for_content(n).items():
        val = (m[0] * g[(0, 1)] + m[1] * g[(0, 2)] + m[2] * g[(1, 2)] + const)
        out.extend([val] * cnt)
    return sorted(out)


def symmetric_form(rng, span=6):
    f = {}
    for a in range(3):
        for b in range(a, 3):
            v = Fraction(rng.randint(-span, span))
            f[(a, b)] = v
            f[(b, a)] = v
    return f


def asymmetric_form(rng, span=6):
    f = {}
    for a in range(3):
        for b in range(3):
            f[(a, b)] = Fraction(rng.randint(-span, span))
    return f


def has_mixed_singleton(f, words, matchings):
    for chi in words:
        if len(set(chi)) == 1:
            continue
        vals = word_weights(f, chi, matchings)
        if vals.count(vals[0]) == 1:
            return True, chi
    return False, None


def main():
    rng = random.Random(20260815)
    for nsites in (6, 8):
        sites = tuple(range(nsites))
        matchings = perfect_matchings(sites)
        words = tuple(product(range(3), repeat=nsites))
        print("N = %d: %d matchings, %d words" % (nsites, len(matchings),
                                                  len(words)))

        # ---- 1. multiset agreement, symmetric forms
        bad = 0
        for trial in range(40):
            f = symmetric_form(rng)
            for chi in words[::7]:
                if word_weights(f, chi, matchings) != predicted_weights(
                        f, chi, nsites):
                    bad += 1
        print("   (1) type-based weight multiset == brute force : "
              "%s  (mismatches %d)" % (bad == 0, bad))
        if bad:
            raise AssertionError("colour-form reduction disagrees with brute force")

        # ---- mutation control M1: break the colour-form shape on one cell
        f = symmetric_form(rng)
        broken = dict(f)
        caught = False
        for chi in words:
            direct = sorted(sum((broken[(chi[u], chi[v])]
                                 + (Fraction(1) if (u, v) == (0, 1) else 0))
                                for u, v in M) for M in matchings)
            if direct != predicted_weights(f, chi, nsites):
                caught = True
                break
        print("   (M1) perturbing one edge off the colour-form shape is caught"
              " : %s" % caught)
        if not caught:
            raise AssertionError("mutation control M1 silent")

        # ---- 2. singleton verdict agreement with the fan
        data = build(nsites, verbose=False)
        agree = 0
        checked = 0
        for rec in data["faces"]:
            g = rec["point"]
            f = {}
            for a in range(3):
                f[(a, a)] = Fraction(0)
            f[(0, 1)] = f[(1, 0)] = g[0]
            f[(0, 2)] = f[(2, 0)] = g[1]
            f[(1, 2)] = f[(2, 1)] = g[2]
            fan_says = any(rec["mincount"][n] == 1 for n in data["mixed"])
            direct, _ = has_mixed_singleton(f, words, matchings)
            checked += 1
            agree += (fan_says == direct)
        print("   (2) fan singleton verdict == direct scan on all %d faces : %s"
              % (checked, agree == checked))
        if agree != checked:
            raise AssertionError("fan/brute-force singleton verdicts disagree")

        # ---- 3. controls
        asym_hits = 0
        for _ in range(60):
            f = asymmetric_form(rng)
            ok, _ = has_mixed_singleton(f, words, matchings)
            asym_hits += ok
        print("   (3a) NON-symmetric colour forms with a mixed singleton : "
              "%d/60" % asym_hits)
        amb_hits = 0
        for _ in range(20):
            wcell = {}
            for e in combinations(sites, 2):
                for i in range(3):
                    for j in range(3):
                        wcell[(e, i, j)] = Fraction(rng.randint(-40, 40))
            hit = False
            for chi in words:
                if len(set(chi)) == 1:
                    continue
                vals = sorted(sum(wcell[((u, v), chi[u], chi[v])]
                                  for u, v in M) for M in matchings)
                if vals.count(vals[0]) == 1:
                    hit = True
                    break
            amb_hits += hit
        print("   (3b) random ambient weights with a mixed singleton : %d/20"
              % amb_hits)
        print()


if __name__ == "__main__":
    main()
