#!/usr/bin/env python3
"""Exact first boundary counterguard for signed matching holonomy.

Three edge-disjoint, unit-weight, constant-colour matchings on K6 have a
minimum possible union with exactly one further perfect matching.  Its mixed
occurrence is a singleton.  The cheapest primitive C4 repair adds two
decorated cells on the colour-zero matching.  Giving both new cells weight i
cancels the forced occurrence, but creates two nonzero boundary singletons.

The calculation proves the uniform local identity

    L * R = B * D = -B * F,

where B is the normalized anchor, D is the diagonal repair, F is the forced
opposite matching, and L,R are the two one-edge boundary faces.  Thus a
nonzero diagonal repair cannot close by itself.  Its sole binomial exponent
row has no circuit, so it has trivial signed holonomy; both boundary fibres
must be retained by any global propagation theorem.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json


EXPECTED_DIGEST = "6e34e6ef4852fdfba8253bbd4fd7f0e6dafe62780e8d1a19a47329107ce83ee8"

# Exact Gaussian integers, represented by (real, imaginary).
ZERO = (0, 0)
ONE = (1, 0)
I = (0, 1)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def gadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def gmul(left, right):
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gneg(value):
    return -value[0], -value[1]


def gsum(values):
    answer = ZERO
    for value in values:
        answer = gadd(answer, value)
    return answer


def gtext(value):
    names = {ZERO: "0", ONE: "1", (-1, 0): "-1", I: "i", (0, -1): "-i"}
    return names.get(value, f"({value[0]}+{value[1]}i)")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return left, right, left_colour, right_colour


def matching_term(cells, matching, word):
    value = ONE
    labels = []
    for left, right in matching:
        label = cell(left, right, word[left], word[right])
        factor = cells.get(label, ZERO)
        if factor == ZERO:
            return ZERO, ()
        value = gmul(value, factor)
        labels.append(label)
    return value, tuple(labels)


def live_fibres(cells, order):
    matchings = tuple(perfect_matchings(range(order)))
    answer = {}
    for word in itertools.product(range(3), repeat=order):
        terms = []
        for matching in matchings:
            value, labels = matching_term(cells, matching, word)
            if value != ZERO:
                terms.append((matching, value, labels))
        if terms:
            answer[word] = tuple(terms)
    return answer


def audit_first_relevant_order():
    # On K4 the three perfect matchings themselves give exact ternary GHZ,
    # so there is no forced mixed occurrence.  K6 is the first relevant order.
    k4 = tuple(perfect_matchings(range(4)))
    require(len(k4) == 3, "the K4 matching count changed")
    k4_union = set().union(*(set(matching) for matching in k4))
    require(sum(set(matching) <= k4_union for matching in k4) == 3,
            "the K4 anchors acquired a fourth matching")

    # Exhaust all unordered edge-disjoint triples on K6.  The least possible
    # number of extra union matchings is one; the selected triple attains it.
    k6 = tuple(perfect_matchings(range(6)))
    require(len(k6) == 15, "the K6 matching count changed")
    histogram = Counter()
    triples = 0
    for indices in itertools.combinations(range(len(k6)), 3):
        supports = tuple(set(k6[index]) for index in indices)
        if any(supports[i] & supports[j]
               for i in range(3) for j in range(i)):
            continue
        triples += 1
        union = set().union(*supports)
        extras = sum(set(matching) <= union for matching in k6) - 3
        histogram[extras] += 1
    require(triples == 80 and histogram == Counter({1: 60, 3: 20}),
            f"the K6 one-factor-triple census changed: {triples}, {histogram}")
    return {
        "K4_perfect_matchings": 3,
        "K4_forced_mixed_occurrences": 0,
        "K6_edge_disjoint_anchor_triples": triples,
        "K6_extra_union_matching_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "minimum_extra_union_matchings": 1,
    }


def anchor_data():
    anchors = {
        0: ((0, 1), (2, 3), (4, 5)),
        1: ((0, 2), (1, 4), (3, 5)),
        2: ((0, 3), (1, 5), (2, 4)),
    }
    forced = ((0, 1), (2, 4), (3, 5))
    forced_word = (0, 0, 2, 1, 2, 1)
    cells = {}
    for colour, matching in anchors.items():
        for left, right in matching:
            cells[cell(left, right, colour, colour)] = ONE
    return anchors, forced, forced_word, cells


def count_new_cells_for_occurrence(cells, matching, word):
    return sum(cell(left, right, word[left], word[right]) not in cells
               for left, right in matching)


def audit_minimal_primitive_repair():
    anchors, forced, word, cells = anchor_data()
    matchings = tuple(perfect_matchings(range(6)))
    require(forced in matchings, "the forced matching disappeared")

    compatible = []
    for matching in matchings:
        if matching == forced:
            continue
        compatible.append((matching,
                           count_new_cells_for_occurrence(cells, matching, word)))
    census = Counter(count for _, count in compatible)
    require(census == Counter({2: 6, 3: 8}),
            f"the first repair-cell census changed: {census}")
    require(min(census) == 2,
            "the forced mixed occurrence acquired a one-cell repair")

    repair = anchors[0]
    common = set(repair) & set(forced)
    symmetric = set(repair) ^ set(forced)
    require(common == {(0, 1)} and len(symmetric) == 4,
            "the selected repair stopped being a primitive tail+C4 flip")
    return {
        "forced_word": "002121",
        "forced_matching": [list(edge) for edge in forced],
        "candidate_repair_new_cell_census": {
            str(key): value for key, value in sorted(census.items())
        },
        "minimum_new_decorated_cells": 2,
        "selected_repair_matching": [list(edge) for edge in repair],
        "common_tail": "01",
        "alternating_component": "C4 on 2,3,4,5",
    }


def exponent_vector(labels, universe):
    count = Counter(labels)
    return tuple(count[label] for label in universe)


def audit_exact_boundary_counterguard():
    anchors, forced, top_word, cells = anchor_data()

    # The two diagonal C4 repair cells have phase i, so their product is -1.
    # The forced occurrence has weight +1 and the top mixed coefficient is 0.
    cells[cell(2, 3, 2, 1)] = I
    cells[cell(4, 5, 2, 1)] = I
    fibres = live_fibres(cells, 6)

    expected = {
        "000000": (ONE,),
        "000021": (I,),
        "002100": (I,),
        "002121": ((-1, 0), ONE),
        "111111": (ONE,),
        "222222": (ONE,),
    }
    actual = {
        "".join(map(str, word)): tuple(term[1] for term in terms)
        for word, terms in fibres.items()
    }
    require(actual == expected,
            f"the exact boundary counterguard changed: {actual}")
    require(gsum(actual["002121"]) == ZERO,
            "the primitive C4 fibre stopped cancelling")
    require(gsum(actual["000021"]) == I
            and gsum(actual["002100"]) == I,
            "a codimension-one boundary debt vanished")

    # Freeze the literal boundary-square identity.  B is the pure anchor,
    # D the diagonal repair term, F the forced opposite term, and L,R the
    # two partial recolourings.  L*R=B*D=-B*F exactly.
    base = actual["000000"][0]
    left = actual["002100"][0]
    right = actual["000021"][0]
    forced_weight = next(term[1] for term in fibres[top_word]
                         if term[0] == forced)
    repair_weight = next(term[1] for term in fibres[top_word]
                         if term[0] == anchors[0])
    require(gmul(left, right) == gmul(base, repair_weight)
            == gneg(gmul(base, forced_weight)),
            "the C4 boundary identity changed")

    # There is one binomial exponent row.  It is nonzero and therefore has
    # no nonzero integral dependency: no closed circuit, odd or even.
    top_terms = fibres[top_word]
    universe = tuple(sorted(cells))
    vectors = tuple(exponent_vector(term[2], universe) for term in top_terms)
    row = tuple(vectors[0][index] - vectors[1][index]
                for index in range(len(universe)))
    require(any(row), "the primitive binomial exponent row became zero")
    require(sum(value > 0 for value in row) == 2
            and sum(value < 0 for value in row) == 2,
            f"the C4 exponent shape changed: {row}")

    mixed = {
        word: terms for word, terms in fibres.items() if len(set(word)) > 1
    }
    histogram = Counter(len(terms) for terms in mixed.values())
    require(histogram == Counter({1: 2, 2: 1}),
            f"the mixed boundary histogram changed: {histogram}")
    return {
        "nonzero_fibres": {
            word: [gtext(value) for value in values]
            for word, values in sorted(actual.items())
        },
        "normalized_constant_colour_coefficients": ["1", "1", "1"],
        "cancelled_primitive_fibre": "002121: 1+i^2=0",
        "boundary_singletons": {"002100": "i", "000021": "i"},
        "mixed_fibre_histogram": {"singleton": 2, "binomial": 1},
        "boundary_identity": "L*R=B*D=-B*F=-1",
        "binomial_exponent_rank": 1,
        "binomial_integer_kernel_rank": 0,
        "closed_holonomy_circuits": 0,
        "verdict": (
            "the cheapest exact primitive cancellation is sign-flat and "
            "exports two nonzero boundary fibres"
        ),
    }


def audit_uniform_identity():
    # Verify the exponent identity symbolically in the free commutative
    # monoid.  The tail t may contain any matching on N-4 other sites, so the
    # statement is uniform in every even order.
    symbols = ("t", "x0", "y0", "x", "y", "u", "v")

    def monomial(*names):
        count = Counter(names)
        return tuple(count[name] for name in symbols)

    base = monomial("t", "x0", "y0")
    diagonal = monomial("t", "x", "y")
    left = monomial("t", "x", "y0")
    right = monomial("t", "x0", "y")
    forced = monomial("t", "u", "v")
    add_exp = lambda a, b: tuple(x + y for x, y in zip(a, b, strict=True))
    require(add_exp(left, right) == add_exp(base, diagonal),
            "the free-monoid boundary identity failed")
    return {
        "arbitrary_even_order_common_tail": "t",
        "definitions": {
            "B": "t*x0*y0", "D": "t*x*y", "F": "t*u*v",
            "L": "t*x*y0", "R": "t*x0*y",
        },
        "free_monoid_identity": "L*R=B*D",
        "with_top_cancellation_D_plus_F_zero": "L*R=-B*F",
        "consequence": (
            "if B and F are nonzero, both boundary occurrences L and R "
            "are nonzero; a full source must supply cancellation mates"
        ),
    }


def signed_weyl_pair(word, pair, plane=(0, 1)):
    """Apply e_a -> -e_b, e_b -> e_a at both sites of ``pair``."""
    first_colour, second_colour = plane
    answer = list(word)
    sign = 1
    for site in pair:
        if answer[site] == first_colour:
            answer[site] = second_colour
            sign *= -1
        elif answer[site] == second_colour:
            answer[site] = first_colour
    return tuple(answer), sign


def apply_weyl_prefix(word, pairs, length):
    answer = tuple(word)
    coefficient = 1
    for pair in pairs[:length]:
        answer, sign = signed_weyl_pair(answer, pair)
        coefficient *= sign
    return answer, coefficient


def audit_global_paired_weyl_telescope(order):
    """Audit H_W=sum P_(j-1)h_j, dH_W=P_m-1 on every word."""
    require(order >= 4 and order % 2 == 0,
            "the global Weyl telescope needs positive even order")
    pairs = tuple((site, site + 1) for site in range(0, order, 2))
    words = tuple(itertools.product(range(3), repeat=order))
    for word in words:
        boundary = Counter()
        for index in range(len(pairs)):
            old_word, old_sign = apply_weyl_prefix(word, pairs, index)
            new_word, new_sign = apply_weyl_prefix(word, pairs, index + 1)
            boundary[new_word] += new_sign
            boundary[old_word] -= old_sign
        boundary = Counter({key: value for key, value in boundary.items()
                            if value})

        final_word, final_sign = apply_weyl_prefix(
            word, pairs, len(pairs))
        expected = Counter()
        expected[final_word] += final_sign
        expected[word] -= 1
        expected = Counter({key: value for key, value in expected.items()
                            if value})
        require(boundary == expected,
                f"the paired Weyl telescope failed on {word}")

    delta = Counter({(colour,) * order: 1 for colour in range(3)})
    image = Counter()
    for word, coefficient in delta.items():
        changed, sign = apply_weyl_prefix(word, pairs, len(pairs))
        image[changed] += coefficient * sign
    require(image == delta,
            f"the global paired Weyl stopped fixing ternary GHZ at {order}")

    # Colour Weyl actions change no physical edge.  Therefore every complete
    # h_j has the all-ones profile in the matching factor.  Any centered
    # occurrence selector kills it, including the first singleton-vs-rest
    # detector below.
    matchings = tuple(perfect_matchings(range(order)))
    matching_profile = tuple(1 for _ in matchings)
    centered = (len(matchings) - 1,) + (-1,) * (len(matchings) - 1)
    require(sum(left * right for left, right in
                zip(matching_profile, centered, strict=True)) == 0,
            "the complete Weyl telescope acquired a pointed matching part")
    return {
        "order": order,
        "site_pairs": [list(pair) for pair in pairs],
        "wordwise_telescope_checks": len(words),
        "identity": "dH_W+H_Wd=W_1*...*W_(N/2)-1",
        "global_Weyl_fixes_ternary_GHZ": True,
        "perfect_matching_occurrences": len(matchings),
        "matching_profile_rank": 1,
        "centered_occurrence_projection": 0,
    }


def main():
    ledger = {
        "first_relevant_order": audit_first_relevant_order(),
        "minimal_primitive_repair": audit_minimal_primitive_repair(),
        "exact_boundary_counterguard": audit_exact_boundary_counterguard(),
        "uniform_boundary_identity": audit_uniform_identity(),
        "global_paired_weyl_telescope": [
            audit_global_paired_weyl_telescope(order) for order in (6, 8)
        ],
        "scope": (
            "counterguard to normalized anchors plus one alternating-fibre "
            "cancellation implying odd holonomy; not a ternary GHZ source"
        ),
        "missing_hypothesis": (
            "boundary-face completeness: every codimension-one recolouring "
            "fibre exported by a diagonal C4 repair must remain in the "
            "global signed exponent complex"
        ),
        "weyl_telescope_scope": (
            "the target-safe global telescope constructs the pure-Weyl "
            "marginal uniformly, but its complete response rows are constant "
            "in the matching-occurrence factor; a pointed/component "
            "splitter remains necessary"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"signed-boundary ledger changed: {digest}")

    print("uniform signed matching-holonomy boundary counterguard: PASS")
    print("K6 minimum anchor-union extra matchings: 1")
    print("minimum primitive repair cells: 2")
    print("mixed fibres after repair: 1 cancelling binomial + 2 singletons")
    print("holonomy circuits in repaired packet: 0")
    print("boundary identity: L*R=B*D=-B*F")
    print("global paired-Weyl telescope: TARGET SAFE, MATCHING CONSTANT")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
