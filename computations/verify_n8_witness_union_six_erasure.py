#!/usr/bin/env python3
"""Exact finite audit of erasing colours on the union-six stratum.

This extends the union-five enumeration to witness masks with no empty
site.  It records both the raw hard-capacity boundary and the boundary
remaining after the already-proved nontriple two-hole and free-plane
criteria.  A certificate is a nonconstant erasing pattern on five sites
(a three-word zero fibre) or on four sites (a nine-word zero fibre).  In
the four-site case the common four-site cofactor also vanishes when both
un-erased sites are nontriple.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, combinations_with_replacement, product

from verify_n8_witness_union_five_stages import (
    COLORS,
    SITES,
    TRIPLE,
    canonical,
    color_degrees,
    free_plane_monomial_certificate,
    hard_assignments,
    rank_two_certificate,
)


def incidence_orbits_union_six() -> tuple[tuple[int, ...], ...]:
    """Canonical six-site masks with every site a witness."""

    return tuple(
        sorted(
            {
                canonical(masks)
                for masks in combinations_with_replacement(range(1, 8), 6)
                if min(color_degrees(masks)) >= 2
            }
        )
    )


def erasing_colors(mask: int, hard_mask: int) -> tuple[int, ...]:
    """Colours whose two deleted-star columns vanish at this site."""

    if mask.bit_count() == 2:
        return tuple(color for color in COLORS if not mask & (1 << color))
    if mask == TRIPLE and hard_mask in (1, 2, 4):
        hard_color = hard_mask.bit_length() - 1
        return tuple(color for color in COLORS if color != hard_color)
    return ()


def erasure_certificate(masks: tuple[int, ...], hard: tuple[int, ...]):
    """Return a strongest five/four-site nonconstant erasing pattern.

    Five erasures leave at most one active star site and hence force a
    three-word internal fibre to zero.  Four erasures leave two sites; the
    correction has rank at most two, so the nine-word fibre vanishes.  If
    both remaining sites are nontriple, the zero-block classification also
    forces the common four-site cofactor to vanish.
    """

    options = tuple(
        erasing_colors(mask, hard_mask)
        for mask, hard_mask in zip(masks, hard, strict=True)
    )
    for size in (5, 4):
        for erased in combinations(SITES, size):
            if any(not options[site] for site in erased):
                continue
            for colors in product(*(options[site] for site in erased)):
                if len(set(colors)) < 2:
                    continue
                remaining = tuple(site for site in SITES if site not in erased)
                cofactor_zero = size == 4 and all(
                    masks[site] != TRIPLE for site in remaining
                )
                return erased, colors, cofactor_zero
    return None


EXPECTED_SURVIVORS = {
    (1, 1, 1, 1, 6, 6): ((1, 1, 1, 1, 6, 6),),
    (1, 1, 1, 6, 6, 6): ((1, 1, 1, 6, 6, 6),),
    (1, 1, 1, 6, 6, 7): ((1, 1, 1, 6, 6, 0),),
    (1, 1, 1, 6, 7, 7): (
        (1, 1, 1, 6, 2, 4),
        (1, 1, 1, 6, 4, 2),
    ),
    (1, 1, 2, 3, 6, 7): ((1, 1, 2, 3, 6, 4),),
    (1, 1, 2, 5, 6, 6): ((1, 1, 2, 5, 6, 6),),
    (1, 1, 2, 5, 7, 7): (
        (1, 1, 2, 5, 2, 4),
        (1, 1, 2, 5, 4, 2),
    ),
    (1, 2, 3, 3, 4, 7): ((1, 2, 3, 3, 4, 4),),
    (1, 2, 3, 4, 5, 6): ((1, 2, 3, 4, 5, 6),),
    (1, 2, 4, 7, 7, 7): tuple(
        (1, 2, 4) + permutation
        for permutation in (
            (1, 2, 4),
            (1, 4, 2),
            (2, 1, 4),
            (2, 4, 1),
            (4, 1, 2),
            (4, 2, 1),
        )
    ),
}


def contains_exceptional_union_five_core(masks: tuple[int, ...]) -> bool:
    """Whether a componentwise subincidence is colour-equivalent to 011166."""

    for color in COLORS:
        singleton_sites = {
            site for site, mask in enumerate(masks)
            if mask & (1 << color)
        }
        complementary_double = 7 ^ (1 << color)
        double_sites = tuple(
            site for site, mask in enumerate(masks)
            if mask & complementary_double == complementary_double
        )
        for selected_doubles in combinations(double_sites, 2):
            if len(singleton_sites - set(selected_doubles)) >= 3:
                return True
    return False


def main() -> None:
    # Six selector colours always create at least three equal-colour
    # omitted pairs; equality is the balanced 2+2+2 distribution.
    selector_pair_counts = {
        sum(count * (count - 1) // 2 for count in counts)
        for counts in product(range(7), repeat=3)
        if sum(counts) == 6
    }
    assert min(selector_pair_counts) == 3

    orbits = incidence_orbits_union_six()
    assert len(orbits) == 138

    assignments = {
        masks: hard_assignments(masks)
        for masks in orbits
    }
    capacity = {
        masks: choices for masks, choices in assignments.items() if choices
    }
    assert len(capacity) == 130
    assert sum(map(len, capacity.values())) == 1133

    raw_rows = tuple(
        (masks, hard)
        for masks, choices in capacity.items()
        for hard in choices
    )
    raw_counts = Counter(
        len(certificate[0]) if certificate is not None else 0
        for masks, hard in raw_rows
        for certificate in (erasure_certificate(masks, hard),)
    )
    assert raw_counts == Counter({5: 748, 4: 252, 0: 133})

    residual_rows = tuple(
        (masks, hard)
        for masks, hard in raw_rows
        if rank_two_certificate(masks, hard) is None
        and free_plane_monomial_certificate(masks, hard) is None
    )
    assert len(residual_rows) == 597
    assert len({masks for masks, _ in residual_rows}) == 72

    residual_counts = Counter(
        (
            len(certificate[0]) if certificate is not None else 0,
            bool(certificate is not None and certificate[2]),
        )
        for masks, hard in residual_rows
        for certificate in (erasure_certificate(masks, hard),)
    )
    assert residual_counts == Counter(
        {
            (5, False): 498,
            (4, False): 35,
            (4, True): 47,
            (0, False): 17,
        }
    )

    survivors = {
        masks: tuple(
            hard
            for row_masks, hard in residual_rows
            if row_masks == masks and erasure_certificate(masks, hard) is None
        )
        for masks in {row_masks for row_masks, _ in residual_rows}
    }
    survivors = {
        masks: choices for masks, choices in survivors.items() if choices
    }
    assert survivors == EXPECTED_SURVIVORS
    exceptional_core_rows = {
        masks for masks in survivors
        if contains_exceptional_union_five_core(masks)
    }
    assert exceptional_core_rows == {
        (1, 1, 1, 1, 6, 6),
        (1, 1, 1, 6, 6, 6),
        (1, 1, 1, 6, 6, 7),
        (1, 1, 1, 6, 7, 7),
        (1, 1, 2, 3, 6, 7),
        (1, 1, 2, 5, 6, 6),
        (1, 1, 2, 5, 7, 7),
    }

    # Audit each finite certificate directly against the erasing-colour
    # rules and the asserted leftover/cofactor classification.
    for masks, hard in residual_rows:
        certificate = erasure_certificate(masks, hard)
        if certificate is None:
            continue
        erased, colors, cofactor_zero = certificate
        assert len(erased) in (4, 5)
        assert len(set(colors)) >= 2
        assert all(
            color in erasing_colors(masks[site], hard[site])
            for site, color in zip(erased, colors, strict=True)
        )
        remaining = tuple(site for site in SITES if site not in erased)
        assert cofactor_zero == (
            len(erased) == 4
            and all(masks[site] != TRIPLE for site in remaining)
        )

    print("union-six incidence orbits:", len(orbits))
    print("hard-capacity orbits / assignments:", len(capacity), "/", 1133)
    print("after two-hole/free-plane filters: 72 /", len(residual_rows))
    print("five-erasure three-word fibres:", residual_counts[5, False])
    print("four-erasure nine-word fibres:",
          residual_counts[4, False] + residual_counts[4, True])
    print("four-erasure cofactors also zero:", residual_counts[4, True])
    print("no erasure certificate: 10 orbits /", residual_counts[0, False])
    print("no-certificate orbits containing a selected 011166 core:",
          len(exceptional_core_rows))


if __name__ == "__main__":
    main()
