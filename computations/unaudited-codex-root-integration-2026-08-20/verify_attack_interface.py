#!/usr/bin/env python3
"""Dependency-free structural audit of ATTACK_INTERFACE.md.

This does not decide clean-cap existence.  It checks the N=8 divided-power
coefficient formula and the exact size of the binary/trichromatic boundary.
"""

from __future__ import annotations

import itertools
import json
from collections import defaultdict
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    a = vertices[0]
    out = []
    for i in range(1, len(vertices)):
        b = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest):
            out.append((((a, b),) + tail))
    return tuple(out)


def multiply(left, right):
    out = defaultdict(Fraction)
    for lm, lc in left.items():
        lsites = {v for _, edge in lm for v in edge}
        for rm, rc in right.items():
            rsites = {v for _, edge in rm for v in edge}
            if lsites & rsites:
                continue
            monomial = tuple(sorted(lm + rm))
            out[monomial] += lc * rc
    return dict(out)


def power(poly, exponent):
    out = {(): Fraction(1)}
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def divide(poly, denominator):
    return {m: c / denominator for m, c in poly.items()}


def cap_error_profile(r2_denominator=2, r3_denominator=6):
    vertices = tuple(range(6))
    edges = tuple(itertools.combinations(vertices, 2))
    r = {(('R', edge),): Fraction(1) for edge in edges}
    x = {(('A', edge),): Fraction(1) for edge in edges}
    r2x = divide(multiply(power(r, 2), x), r2_denominator)
    r3 = divide(power(r, 3), r3_denominator)
    combined = defaultdict(Fraction)
    for monomial, coefficient in r2x.items():
        combined[tuple(sorted((('s', (-1, -1)),) + monomial))] += coefficient
    for monomial, coefficient in r3.items():
        combined[monomial] += coefficient
    return dict(combined)


def expected_profile():
    out = {}
    for matching in perfect_matchings(range(6)):
        for a_index in range(3):
            monomial = []
            for index, edge in enumerate(matching):
                monomial.append(('A' if index == a_index else 'R', edge))
            out[tuple(sorted((('s', (-1, -1)),) + tuple(monomial)))] = Fraction(1)
        out[tuple(sorted(('R', edge) for edge in matching))] = Fraction(1)
    return out


def off_count(word):
    return len(word) - max(word.count(c) for c in range(3))


def main():
    declared = [
        'matching_count',
        'divided_power_formula',
        'factorial_mutations_fire',
        'word_boundary',
        'cap_degree',
    ]
    ran = []
    report = {'_controls_declared': declared, '_controls_run': ran}

    matchings = perfect_matchings(range(6))
    require(len(matchings) == 15, 'six-site perfect-matching count changed')
    ran.append('matching_count')
    report['matching_count'] = len(matchings)

    actual = cap_error_profile()
    expected = expected_profile()
    require(actual == expected, 'divided-power cap-error coefficients changed')
    require(len(actual) == 60, 'expected four typed terms per matching')
    ran.append('divided_power_formula')
    report['cap_error_typed_terms_per_word'] = len(actual)

    require(cap_error_profile(r2_denominator=1) != expected,
            'r^2/2 mutation failed to fire')
    require(cap_error_profile(r3_denominator=1) != expected,
            'r^3/6 mutation failed to fire')
    ran.append('factorial_mutations_fire')

    words = tuple(itertools.product(range(3), repeat=8))
    binary = sum(1 for w in words if len(set(w)) <= 2)
    off_le_4 = sum(1 for w in words if off_count(w) <= 4)
    off_5 = sum(1 for w in words if off_count(w) == 5)
    require((len(words), binary, off_le_4, off_5) == (6561, 765, 4881, 1680),
            'N=8 word boundary changed')
    require(off_le_4 + off_5 == len(words), 'level partition is incomplete')
    ran.append('word_boundary')
    report['words'] = {
        'all': len(words),
        'using_at_most_two_colours': binary,
        'off_count_at_most_4': off_le_4,
        'profile_3_3_2_off_count_5': off_5,
    }

    # s and every R entry are linear in the nine K coordinates.  Every
    # structural monomial above therefore has K-degree three; activity is
    # s*kappa_0*kappa_1*kappa_2 and has degree four.
    require(all(sum(1 for tag, _ in monomial if tag in ('s', 'R')) == 3
                for monomial in actual), 'cap-error K-degree is not uniform')
    ran.append('cap_degree')
    report['degrees_in_cap_coordinates'] = {'E': 3, 'activity': 4}

    require(ran == declared, 'control manifest incomplete')
    report['_manifest_ok'] = True
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
