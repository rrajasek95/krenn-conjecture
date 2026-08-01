#!/usr/bin/env python3
"""Clean-room finite audit of the one-/two-line-field obstruction.

This file imports neither the primary verifier nor project code.  It uses
bit masks for both site sets and coordinate supports, a direct Cartesian-box
enumeration for the three-frame lemma, a finite-field flattening audit, and a
four-factor tensor expansion for the Segre-secant step.

The finite calculations check the combinatorics and representative exact
linear algebra.  The dimension-independent arguments are written out in the
companion independent-audit note.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb

import sympy as sp


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


N_SITES = 6
N_COLOURS = 3
ALL_SITES = (1 << N_SITES) - 1
ALL_COLOURS = (1 << N_COLOURS) - 1


def masks_of_weight(width: int, weight: int) -> tuple[int, ...]:
    return tuple(mask for mask in range(1 << width) if mask.bit_count() == weight)


SITE_PAIRS = masks_of_weight(N_SITES, 2)
SITE_TRIPLES = masks_of_weight(N_SITES, 3)
MOVING_AT_MOST_TWO = tuple(
    mask for mask in range(1 << N_SITES) if mask.bit_count() <= 2
)


def colours_in(support: int) -> tuple[int, ...]:
    return tuple(
        colour for colour in range(N_COLOURS) if support & (1 << colour)
    )


def audit_quotient_survivors() -> None:
    """A three-site quotient kills O_2; a two-site quotient isolates its pair."""
    require(
        len(MOVING_AT_MOST_TWO) == 1 + N_SITES + comb(N_SITES, 2) == 22,
        "len(MOVING_AT_MOST_TWO) == 1 + N_SITES + comb(N_SITES, 2)...",
    )

    for quotient_sites in SITE_TRIPLES:
        for moving_sites in MOVING_AT_MOST_TWO:
            # At least one quotient site still carries the fixed field line.
            require(
                quotient_sites & ~moving_sites,
                "quotient_sites & ~moving_sites",
            )

    isolated = 0
    for quotient_pair in SITE_PAIRS:
        survivors = tuple(
            moving_sites
            for moving_sites in MOVING_AT_MOST_TWO
            if quotient_pair & ~moving_sites == 0
        )
        require(
            survivors == (quotient_pair,),
            "survivors == (quotient_pair,)",
        )
        isolated += len(survivors)
    require(
        isolated == 15,
        "isolated == 15",
    )


def audit_plane_incidence_and_partition() -> int:
    """Exhaust all target-axis incidence patterns allowed by a 2-plane."""
    # A local mask records which of the three independent target axes lie in
    # W_u.  The full mask is forbidden because dim(W_u) <= 2.
    local_planes = tuple(mask for mask in range(1 << N_COLOURS) if mask != ALL_COLOURS)
    require(
        len(local_planes) == 7,
        "len(local_planes) == 7",
    )

    equality_cases = 0
    assignment_checks = 0
    for planes in product(local_planes, repeat=N_SITES):
        incidences = tuple(
            sum(bool(plane & (1 << colour)) for plane in planes)
            for colour in range(N_COLOURS)
        )
        if min(incidences) < 4:
            continue

        equality_cases += 1
        require(
            incidences == (4, 4, 4),
            "incidences == (4, 4, 4)",
        )
        require(
            all(plane.bit_count() == 2 for plane in planes),
            "all(plane.bit_count() == 2 for plane in planes)",
        )

        omitted_pairs = tuple(
            sum(
                1 << site
                for site, plane in enumerate(planes)
                if not (plane & (1 << colour))
            )
            for colour in range(N_COLOURS)
        )
        require(
            all(pair in SITE_PAIRS for pair in omitted_pairs),
            "all(pair in SITE_PAIRS for pair in omitted_pairs)",
        )
        require(
            omitted_pairs[0] | omitted_pairs[1] | omitted_pairs[2] == ALL_SITES,
            "omitted_pairs[0] | omitted_pairs[1] | omitted_pairs[2] ==...",
        )
        require(
            not (omitted_pairs[0] & omitted_pairs[1]),
            "not (omitted_pairs[0] & omitted_pairs[1])",
        )
        require(
            not (omitted_pairs[0] & omitted_pairs[2]),
            "not (omitted_pairs[0] & omitted_pairs[2])",
        )
        require(
            not (omitted_pairs[1] & omitted_pairs[2]),
            "not (omitted_pairs[1] & omitted_pairs[2])",
        )

        complements = tuple(ALL_SITES ^ pair for pair in omitted_pairs)
        for field_assignment in product(range(2), repeat=N_COLOURS):
            repeated = tuple(
                (left, right)
                for left, right in combinations(range(N_COLOURS), 2)
                if field_assignment[left] == field_assignment[right]
            )
            require(
                repeated,
                "repeated",
            )
            # Every repeated-field pair has two common complement sites.
            for left, right in repeated:
                require(
                    (complements[left] & complements[right]).bit_count() == 2,
                    "(complements[left] & complements[right]).bit_count() == 2",
                )
            assignment_checks += 1

    # Equivalently choose, at each site, the unique omitted colour, with each
    # colour omitted exactly twice: 6!/(2!2!2!) = 90.
    require(
        equality_cases == 90,
        "equality_cases == 90",
    )
    require(
        assignment_checks == 90 * 2**3,
        "assignment_checks == 90 * 2**3",
    )
    return equality_cases


def audit_rank_one_flattening() -> int:
    """Check the coefficient separation in (12) over an exact finite field."""
    # Put the independent right factors L_C,M_C in the first two coordinates.
    # If A tensor x has no columns outside their span, nonzero A forces the
    # other coordinates of x to vanish; its first two columns are multiples
    # of A.  Dimension 3 x 4 is deliberately larger than the minimal 2 x 2
    # picture used in the primary verifier.
    modulus = 5
    checked = 0
    for left_factor in product(range(modulus), repeat=3):
        if not any(left_factor):
            continue
        for right_factor in product(range(modulus), repeat=4):
            matrix = tuple(
                tuple((a * x) % modulus for x in right_factor)
                for a in left_factor
            )
            if any(matrix[row][column] for row in range(3) for column in (2, 3)):
                continue
            require(
                right_factor[2:] == (0, 0),
                "right_factor[2:] == (0, 0)",
            )
            z_l = tuple(matrix[row][0] for row in range(3))
            z_m = tuple(matrix[row][1] for row in range(3))
            require(
                z_l == tuple((right_factor[0] * a) % modulus for a in left_factor),
                "z_l == tuple((right_factor[0] * a) % modulus for a in lef...",
            )
            require(
                z_m == tuple((right_factor[1] * a) % modulus for a in left_factor),
                "z_m == tuple((right_factor[1] * a) % modulus for a in lef...",
            )
            checked += 1

    require(
        checked == (modulus**3 - 1) * modulus**2,
        "checked == (modulus**3 - 1) * modulus**2",
    )
    return checked


def tensor_product_mod3(factors: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    coefficients = []
    for word in product(range(2), repeat=len(factors)):
        coefficient = 1
        for factor, coordinate in zip(factors, word):
            coefficient = coefficient * factor[coordinate] % 3
        coefficients.append(coefficient)
    return tuple(coefficients)


def audit_four_site_secant() -> None:
    """Symbolically and finitely exclude a third pure point on the secant."""
    alpha, beta = sp.symbols("alpha beta")
    flattening = sp.zeros(2, 8)
    flattening[0, 0] = alpha
    flattening[1, 7] = beta
    require(
        flattening.extract((0, 1), (0, 7)).det() == alpha * beta,
        "flattening.extract((0, 1), (0, 7)).det() == alpha * beta",
    )

    # The four projective points of P^1(F_3).  After independent local basis
    # changes, the two field products are 0000 and 1111.  Exhaust all 4^4
    # pure tensors and confirm that only these endpoints lie on their line.
    projective_line = ((1, 0), (0, 1), (1, 1), (1, 2))
    pure_points_on_secant = []
    for factors in product(projective_line, repeat=4):
        tensor = tensor_product_mod3(factors)
        if any(tensor[index] for index in range(16) if index not in (0, 15)):
            continue
        pure_points_on_secant.append(tensor)
        require(
            tensor[0] == 0 or tensor[15] == 0,
            "tensor[0] == 0 or tensor[15] == 0",
        )
    require(
        len(pure_points_on_secant) == 2,
        "len(pure_points_on_secant) == 2",
    )


def hamming(word: tuple[int, ...], centre: tuple[int, ...]) -> int:
    return sum(left != right for left, right in zip(word, centre))


def audit_genuine_two_ball_bridge() -> None:
    # L=(0,0,0,0,0,0), while M differs only at site 0.  The two coordinate
    # words are the expansion of a pure tensor whose site-0 factor has both
    # L and M coordinates and whose last two factors are transverse.
    centre_l = (0, 0, 0, 0, 0, 0)
    centre_m = (1, 0, 0, 0, 0, 0)
    l_term = (0, 0, 0, 0, 2, 2)
    m_term = (1, 0, 0, 0, 2, 2)

    require(
        hamming(l_term, centre_l) == 2,
        "hamming(l_term, centre_l) == 2",
    )
    require(
        hamming(m_term, centre_m) == 2,
        "hamming(m_term, centre_m) == 2",
    )
    require(
        hamming(l_term, centre_m) == 3,
        "hamming(l_term, centre_m) == 3",
    )
    require(
        hamming(m_term, centre_l) == 3,
        "hamming(m_term, centre_l) == 3",
    )

    # Membership of a vector in a coordinate-word subspace is termwise.
    support = {l_term, m_term}
    ball_l = {
        word for word in product(range(3), repeat=6) if hamming(word, centre_l) <= 2
    }
    ball_m = {
        word for word in product(range(3), repeat=6) if hamming(word, centre_m) <= 2
    }
    require(
        support <= ball_l | ball_m,
        "support <= ball_l | ball_m",
    )
    require(
        not support <= ball_l,
        "not support <= ball_l",
    )
    require(
        not support <= ball_m,
        "not support <= ball_m",
    )


def hall_fails(supports: tuple[int, ...]) -> bool:
    """Hall failure after replacing each colour by three capacity slots."""
    for site_set in range(1, 1 << N_SITES):
        neighbour_colours = 0
        for site in range(N_SITES):
            if site_set & (1 << site):
                neighbour_colours |= supports[site]
        if site_set.bit_count() > 3 * neighbour_colours.bit_count():
            return True
    return False


def audit_three_frame_hall_and_boxes() -> tuple[int, int]:
    """Directly enumerate all 7^6 support boxes, not via dynamic programming."""
    nonempty_supports = tuple(range(1, 1 << N_COLOURS))
    boxes = 0
    trapped_boxes = 0

    for supports in product(nonempty_supports, repeat=N_SITES):
        boxes += 1
        choices = tuple(colours_in(support) for support in supports)

        balanced_word_exists = False
        for word in product(*choices):
            counts = tuple(word.count(colour) for colour in range(N_COLOURS))
            if max(counts) <= 3:
                balanced_word_exists = True
                break

        trapped_in_union = not balanced_word_exists
        singleton_counts = tuple(
            sum(support == (1 << colour) for support in supports)
            for colour in range(N_COLOURS)
        )
        four_fixed_sites = max(singleton_counts) >= 4

        require(
            hall_fails(supports) == four_fixed_sites,
            "hall_fails(supports) == four_fixed_sites",
        )
        require(
            trapped_in_union == four_fixed_sites,
            "trapped_in_union == four_fixed_sites",
        )
        if trapped_in_union:
            trapped_boxes += 1

    expected_trapped = N_COLOURS * (
        comb(6, 4) * 6**2 + comb(6, 5) * 6 + 1
    )
    require(
        boxes == 7**6 == 117_649,
        "boxes == 7**6 == 117_649",
    )
    require(
        trapped_boxes == expected_trapped == 1_731,
        "trapped_boxes == expected_trapped == 1_731",
    )
    return boxes, trapped_boxes


def audit_three_frame_direct_sum() -> int:
    words = tuple(product(range(N_COLOURS), repeat=N_SITES))
    centres = tuple((colour,) * N_SITES for colour in range(N_COLOURS))
    balls = tuple(
        {word for word in words if hamming(word, centre) <= 2}
        for centre in centres
    )

    expected_size = sum(comb(N_SITES, changes) * 2**changes for changes in range(3))
    require(
        expected_size == 73,
        "expected_size == 73",
    )
    require(
        all(len(ball) == expected_size for ball in balls),
        "all(len(ball) == expected_size for ball in balls)",
    )
    require(
        all(
            balls[left].isdisjoint(balls[right])
            for left, right in combinations(range(N_COLOURS), 2)
        ),
        "all( balls[left].isdisjoint(balls[right]) for left, right...",
    )

    # Multiplying a four-site field term by two arbitrary endpoint factors
    # generates exactly its radius-two coordinate ball.
    for colour in range(N_COLOURS):
        generated = set()
        for missing_pair in SITE_PAIRS:
            endpoints = tuple(
                site for site in range(N_SITES) if missing_pair & (1 << site)
            )
            for endpoint_values in product(range(N_COLOURS), repeat=2):
                word = [colour] * N_SITES
                for site, value in zip(endpoints, endpoint_values):
                    word[site] = value
                generated.add(tuple(word))
        require(
            generated == balls[colour],
            "generated == balls[colour]",
        )

    # If four local factors are singleton-supported on a field coordinate,
    # every coordinate word of the pure tensor is in that field's ball and
    # in no other field's ball.  This is the exact support statement used in
    # the componentwise splitting of the response equations.
    checked_aligned_boxes = 0
    for colour in range(N_COLOURS):
        for fixed_sites in combinations(range(N_SITES), 4):
            residual_sites = tuple(site for site in range(N_SITES) if site not in fixed_sites)
            for residual_supports in product(range(1, 1 << N_COLOURS), repeat=2):
                supports = [1 << colour] * N_SITES
                for site, support in zip(residual_sites, residual_supports):
                    supports[site] = support
                for word in product(*(colours_in(support) for support in supports)):
                    require(
                        word in balls[colour],
                        "word in balls[colour]",
                    )
                    require(
                        all(
                            word not in balls[other]
                            for other in range(N_COLOURS)
                            if other != colour
                        ),
                        "all( word not in balls[other] for other in range(N_COLOUR...",
                    )
                checked_aligned_boxes += 1
    require(
        checked_aligned_boxes == 3 * comb(6, 4) * 7**2,
        "checked_aligned_boxes == 3 * comb(6, 4) * 7**2",
    )
    return sum(len(ball) for ball in balls)


def main() -> None:
    audit_quotient_survivors()
    equality_cases = audit_plane_incidence_and_partition()
    flattenings = audit_rank_one_flattening()
    audit_four_site_secant()
    audit_genuine_two_ball_bridge()
    boxes, trapped = audit_three_frame_hall_and_boxes()
    direct_sum_dimension = audit_three_frame_direct_sum()

    print("clean-room one-/two-line-field obstruction audit: PASS")
    print(f"plane-incidence equality cases: {equality_cases}")
    print(f"finite-field rank-one flattenings: {flattenings}")
    print("four-site Segre secant: only its two endpoints are pure")
    print(f"three-frame support boxes: {boxes}; trapped: {trapped}")
    print(f"three radius-two balls: direct coordinate dimension {direct_sum_dimension}")
    print("scope: (24) uses all nine responses; the alignment lemma uses only three diagonals")


if __name__ == "__main__":
    main()
