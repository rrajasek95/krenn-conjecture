#!/usr/bin/env python3
r"""Exact staged audit of the five-site witness-union stratum at n=8.

Masks encode exact zero-cross colors at the six sites:
0=empty, 1={0}, 2={1}, 3={0,1}, ..., 7={0,1,2}.

The audit checks

* 61 incidence orbits and 49 hard-capacity survivors;
* the original exact-double two-hole criterion (18 orbitwise exclusions);
* the strengthened nontriple two-hole rank criterion (33 exclusions);
* a binary-target/free-plane monomial criterion (3 further exclusions);
* the exact list of 13 residual orbits and 36 residual hard assignments;
* full-five-hole anchor-chart counts on those residual assignments; and
* the triple-hard/nontriple row locks and the resulting finite charts.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, combinations_with_replacement, permutations, product

import sympy as sp


COLORS = tuple(range(3))
SITES = tuple(range(6))
NONE = -1
TRIPLE = 7


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[color]
        for color in COLORS
        if mask & (1 << color)
    )


def canonical(masks: tuple[int, ...]) -> tuple[int, ...]:
    """Quotient sorted sites by the remaining S_3 color action."""

    return min(
        tuple(sorted(permute_mask(mask, permutation) for mask in masks))
        for permutation in permutations(COLORS)
    )


def color_degrees(masks: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(bool(mask & (1 << color)) for mask in masks)
        for color in COLORS
    )


def incidence_orbits() -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(
            {
                canonical(masks)
                for masks in combinations_with_replacement(range(8), 6)
                if sum(mask != 0 for mask in masks) == 5
                and min(color_degrees(masks)) >= 2
            }
        )
    )


def hard_assignments(masks: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Enumerate the exact hard-capacity possibilities.

    At a nontriple site, the hard mask equals the witness mask.  At a
    triple-zero site, the hard mask is empty or one coordinate bit.  Keep
    precisely the assignments having at least two hard sites per color.
    """

    triple_sites = tuple(i for i, mask in enumerate(masks) if mask == TRIPLE)
    answer = []
    for choices in product((0, 1, 2, 4), repeat=len(triple_sites)):
        hard = [0 if mask == TRIPLE else mask for mask in masks]
        for site, choice in zip(triple_sites, choices, strict=True):
            hard[site] = choice
        if all(
            sum(bool(mask & (1 << color)) for mask in hard) >= 2
            for color in COLORS
        ):
            answer.append(tuple(hard))
    return tuple(answer)


def active_colors(hard: tuple[int, ...], holes: tuple[int, int]) -> int:
    """Return the target-color mask surviving after contracting nonholes."""

    outside = set(SITES) - set(holes)
    return sum(
        1 << color
        for color in COLORS
        if all(not (hard[site] & (1 << color)) for site in outside)
    )


def rank_two_certificate(
    masks: tuple[int, ...],
    hard: tuple[int, ...],
    *,
    exact_double_only: bool = False,
):
    """Find two nontriple holes leaving exactly one active target color."""

    for color in COLORS:
        holes = tuple(
            site for site in SITES if hard[site] & (1 << color)
        )
        if len(holes) != 2:
            continue
        if exact_double_only:
            if not all(masks[site].bit_count() == 2 for site in holes):
                continue
        elif not all(masks[site] != TRIPLE for site in holes):
            continue
        if active_colors(hard, holes) == 1 << color:
            return color, holes
    return None


def free_plane_monomial_certificate(
    masks: tuple[int, ...], hard: tuple[int, ...]
):
    """Find a binary target with a contracted free coordinate plane.

    The holes have the same exact double mask {r,s}; both r and s remain
    active.  A contracted triple site hard for the missing color t has
    annihilator e_t^perp, so its r- and s-coordinates are independent.
    """

    for holes in combinations(SITES, 2):
        u, v = holes
        if masks[u] != masks[v] or masks[u].bit_count() != 2:
            continue
        if active_colors(hard, holes) != masks[u]:
            continue
        missing = next(
            color for color in COLORS if not (masks[u] & (1 << color))
        )
        for site in set(SITES) - set(holes):
            if masks[site] == TRIPLE and hard[site] == 1 << missing:
                return holes, masks[u], site, missing
    return None


def local_anchor_options(mask: int, hard_mask: int):
    """Possible (p-label,q-label) pairs at one full-five-hole site."""

    if mask == TRIPLE:
        # Every nonzero star block at a hard-c triple site is a c-anchor,
        # and at least one of the two blocks is nonzero.
        assert hard_mask in (1, 2, 4)
        color = hard_mask.bit_length() - 1
        return ((color, NONE), (NONE, color), (color, color))

    colors = tuple(color for color in COLORS if mask & (1 << color))
    answer = []
    for p_label in (NONE,) + colors:
        for q_label in (NONE,) + colors:
            if p_label != NONE and q_label != NONE:
                forced = (
                    TRIPLE
                    if p_label == q_label
                    else (1 << p_label) | (1 << q_label)
                )
                if mask != forced:
                    continue
            answer.append((p_label, q_label))
    return tuple(answer)


def anchor_chart_counts(masks: tuple[int, ...], hard: tuple[int, ...]):
    """Count full endpoint coverage, and the collision-free subcount.

    The state records p-coverage, q-coverage, and colors for which p and q
    anchors occur at distinct sites.  The latter is an optional stronger
    filter; the proof uses only the first two masks.
    """

    states = {(0, 0, 0): 1}
    for site, mask in enumerate(masks):
        if mask == 0:
            continue
        updated = defaultdict(int)
        for (p_seen, q_seen, distinct), count in states.items():
            for p_label, q_label in local_anchor_options(mask, hard[site]):
                new_p = p_seen
                new_q = q_seen
                new_distinct = distinct
                if p_label != NONE:
                    new_p |= 1 << p_label
                    if q_seen & (1 << p_label):
                        new_distinct |= 1 << p_label
                if q_label != NONE:
                    new_q |= 1 << q_label
                    if p_seen & (1 << q_label):
                        new_distinct |= 1 << q_label
                updated[new_p, new_q, new_distinct] += count
        states = updated

    covered = sum(
        count for (p_seen, q_seen, _), count in states.items()
        if p_seen == q_seen == TRIPLE
    )
    collision_free = sum(
        count for state, count in states.items()
        if state == (TRIPLE, TRIPLE, TRIPLE)
    )
    return covered, collision_free


P_ONLY = "P"
Q_ONLY = "Q"
BOTH = "B"
TRIPLE_TYPES = (P_ONLY, Q_ONLY, BOTH)


def active_triple_nontriple_pairs(
    masks: tuple[int, ...], hard: tuple[int, ...]
):
    """List one-active-color pairs with one triple and one nontriple hole."""

    answer = []
    for color in COLORS:
        holes = tuple(
            site for site in SITES if hard[site] & (1 << color)
        )
        if len(holes) != 2 or active_colors(hard, holes) != 1 << color:
            continue
        triple_sites = tuple(site for site in holes if masks[site] == TRIPLE)
        nontriple_sites = tuple(site for site in holes if masks[site] != TRIPLE)
        if len(triple_sites) == len(nontriple_sites) == 1:
            answer.append((color, triple_sites[0], nontriple_sites[0]))
    return tuple(answer)


def locked_columns(mask: int, hard_color: int) -> frozenset[int]:
    """Nonzero off-color columns forced in the two-sided row-lock case."""

    assert mask != TRIPLE and mask & (1 << hard_color)
    if mask.bit_count() == 1:
        return frozenset(set(COLORS) - {hard_color})
    assert mask.bit_count() == 2
    return frozenset(
        color for color in COLORS
        if color != hard_color and mask & (1 << color)
    )


def row_lock_chart_signatures(
    masks: tuple[int, ...], hard: tuple[int, ...], *, collision_free: bool
):
    """Enumerate anchor labels after all active-one row locks.

    A hard-c triple is P-only, Q-only, or two-sided.  A Q-only triple
    forces a p-side c-anchor at its paired nontriple hole; P-only forces
    the q-side analogue.  A two-sided triple locks every prescribed
    nonzero off-c column at the nontriple hole to the corresponding triple
    endpoint line.  The returned signature records these line sources as
    well as every anchor label.
    """

    triple_sites = tuple(
        site for site, mask in enumerate(masks) if mask == TRIPLE
    )
    active_pairs = active_triple_nontriple_pairs(masks, hard)
    signatures = set()

    for type_choice in product(TRIPLE_TYPES, repeat=len(triple_sites)):
        triple_type = dict(zip(triple_sites, type_choice, strict=True))
        p_labels = {}
        q_labels = {}
        forced_p = {site: set() for site in SITES}
        forced_q = {site: set() for site in SITES}
        p_locks = {site: defaultdict(set) for site in SITES}
        q_locks = {site: defaultdict(set) for site in SITES}

        for site in triple_sites:
            assert hard[site] in (1, 2, 4)
            color = hard[site].bit_length() - 1
            kind = triple_type[site]
            p_labels[site] = NONE if kind == Q_ONLY else color
            q_labels[site] = NONE if kind == P_ONLY else color

        for color, triple_site, nontriple_site in active_pairs:
            kind = triple_type[triple_site]
            if kind == Q_ONLY:
                forced_p[nontriple_site].add(color)
            elif kind == P_ONLY:
                forced_q[nontriple_site].add(color)
            else:
                for column in locked_columns(masks[nontriple_site], color):
                    p_locks[nontriple_site][column].add(triple_site)
                    q_locks[nontriple_site][column].add(triple_site)

        site_options = {}
        valid = True
        for site, mask in enumerate(masks):
            if mask in (0, TRIPLE):
                continue
            witness_colors = tuple(
                color for color in COLORS if mask & (1 << color)
            )

            def side_options(forced, locks):
                if len(forced) > 1:
                    return ()
                nonzero_columns = set(locks)
                if forced:
                    color = next(iter(forced))
                    if color not in witness_colors or not nonzero_columns <= {color}:
                        return ()
                    return (color,)
                return (NONE,) + tuple(
                    color for color in witness_colors
                    if nonzero_columns <= {color}
                )

            p_options = side_options(forced_p[site], p_locks[site])
            q_options = side_options(forced_q[site], q_locks[site])
            pairs = []
            for p_label in p_options:
                for q_label in q_options:
                    if p_label != NONE and q_label != NONE:
                        forced_mask = (
                            TRIPLE
                            if p_label == q_label
                            else (1 << p_label) | (1 << q_label)
                        )
                        if mask != forced_mask:
                            continue
                    pairs.append((p_label, q_label))
            if not pairs:
                valid = False
                break
            site_options[site] = tuple(pairs)
        if not valid:
            continue

        variable_sites = tuple(site_options)
        for labels in product(*(site_options[site] for site in variable_sites)):
            chart_p = dict(p_labels)
            chart_q = dict(q_labels)
            for site, (p_label, q_label) in zip(
                variable_sites, labels, strict=True
            ):
                chart_p[site] = p_label
                chart_q[site] = q_label

            if {
                label for label in chart_p.values() if label != NONE
            } != set(COLORS):
                continue
            if {
                label for label in chart_q.values() if label != NONE
            } != set(COLORS):
                continue
            if collision_free and any(
                not any(
                    chart_p.get(u) == color
                    and chart_q.get(v) == color
                    and u != v
                    for u in SITES
                    for v in SITES
                )
                for color in COLORS
            ):
                continue

            lock_signature = tuple(
                (endpoint, site, column, tuple(sorted(sources)))
                for endpoint, locks in (("p", p_locks), ("q", q_locks))
                for site in SITES
                for column, sources in sorted(locks[site].items())
            )
            signatures.add(
                (
                    tuple((site, triple_type[site]) for site in triple_sites),
                    tuple(
                        (site, chart_p[site], chart_q[site])
                        for site, mask in enumerate(masks)
                        if mask != 0
                    ),
                    lock_signature,
                )
            )

    return frozenset(signatures)


def audit_rank_algebra() -> None:
    """Audit all selected-minor factorizations of the rank-two correction."""

    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    X = sp.symbols("X0:3")
    Y = sp.symbols("Y0:3")
    left = sp.Matrix.hstack(sp.Matrix(x), sp.Matrix(y))
    right = sp.Matrix.vstack(sp.Matrix(Y).T, sp.Matrix(X).T)
    correction = left * right
    for rows in combinations(COLORS, 2):
        for columns in combinations(COLORS, 2):
            lhs = correction.extract(rows, columns).det()
            first_cross = sp.Matrix(
                [[x[rows[0]], y[rows[0]]], [x[rows[1]], y[rows[1]]]]
            ).det()
            second_cross = sp.Matrix(
                [[Y[columns[0]], X[columns[0]]],
                 [Y[columns[1]], X[columns[1]]]]
            ).det()
            assert sp.expand(lhs - first_cross * second_cross) == 0

    zr, zs, cr, cs, rr, ss = sp.symbols(
        "zr zs cr cs Rrr Rss", nonzero=True
    )
    # Eliminating the one common scalar from the two binary diagonal
    # equations would equate two distinct free-plane monomials.
    obstruction = sp.Poly(cr * ss * zr - cs * rr * zs, zr, zs)
    assert obstruction.terms() == [((1, 0), cr * ss), ((0, 1), -cs * rr)]


def audit_row_lock_algebra() -> None:
    """Audit the rank bound and cross-coordinate formulas behind row locks."""

    a = sp.Matrix(sp.symbols("a0:3"))
    b = sp.Matrix(sp.symbols("b0:3"))
    p = sp.Matrix(sp.symbols("p0:3"))
    q = sp.Matrix(sp.symbols("q0:3"))
    coefficient = a * q.T + p * b.T
    # A sum of two rank-one matrices cannot be a nonzero multiple of the
    # rank-three deleted block.  Its determinant vanishes identically.
    assert sp.expand(coefficient.det()) == 0

    # In the two-sided case, rank-one factor uniqueness gives the indicated
    # paired columns.  For r=0 the two remaining cross coordinates are a
    # common nonzero correction entry times the opposite lock scalar.
    A, B, C, D, lambda_1, lambda_2 = sp.symbols(
        "A B C D lambda_1 lambda_2"
    )
    x = sp.Matrix([C, lambda_1 * A, lambda_2 * A])
    y = sp.Matrix([D, -lambda_1 * B, -lambda_2 * B])
    correction_00 = A * D + B * C
    expected_cross = sp.Matrix(
        [0, lambda_2 * correction_00, -lambda_1 * correction_00]
    )
    assert all(
        sp.expand(entry) == 0 for entry in x.cross(y) - expected_cross
    )


EXPECTED_BINARY_STAGE = {
    (0, 1, 1, 6, 6, 7),
    (0, 1, 6, 6, 7, 7),
    (0, 3, 3, 7, 7, 7),
}


EXPECTED_RESIDUAL = {
    (0, 1, 1, 1, 6, 6): (1, 1, (24, 24)),
    (0, 1, 3, 3, 6, 7): (1, 1, (212, 148)),
    (0, 1, 3, 5, 6, 6): (1, 1, (334, 334)),
    (0, 1, 3, 5, 7, 7): (2, 2, (132, 64)),
    (0, 1, 6, 6, 6, 7): (1, 1, (240, 192)),
    (0, 1, 6, 7, 7, 7): (6, 6, (85, 32)),
    (0, 3, 3, 3, 5, 7): (1, 1, (708, 504)),
    (0, 3, 3, 3, 7, 7): (1, 1, (336, 336)),
    (0, 3, 3, 5, 5, 6): (1, 1, (1070, 1070)),
    (0, 3, 3, 5, 6, 7): (4, 1, (582, 518)),
    (0, 3, 3, 5, 7, 7): (7, 2, (362, 224)),
    (0, 3, 5, 7, 7, 7): (18, 6, (235, 104)),
    (0, 3, 7, 7, 7, 7): (12, 12, (119, 56)),
}


EXPECTED_ROW_LOCK_COUNTS = {
    (0, 1, 1, 1, 6, 6): (24, 24),
    (0, 1, 3, 3, 6, 7): (138, 74),
    (0, 1, 3, 5, 6, 6): (334, 334),
    (0, 1, 3, 5, 7, 7): (56, 16),
    (0, 1, 6, 6, 6, 7): (144, 96),
    (0, 1, 6, 7, 7, 7): (21, 4),
    (0, 3, 3, 3, 5, 7): (456, 252),
    (0, 3, 3, 3, 7, 7): (336, 336),
    (0, 3, 3, 5, 5, 6): (1070, 1070),
    (0, 3, 3, 5, 6, 7): (582, 518),
    (0, 3, 3, 5, 7, 7): (236, 112),
    (0, 3, 5, 7, 7, 7): (97, 26),
    (0, 3, 7, 7, 7, 7): (49, 14),
}


def main() -> None:
    audit_rank_algebra()
    audit_row_lock_algebra()
    orbits = incidence_orbits()
    assert len(orbits) == 61

    assignments = {masks: hard_assignments(masks) for masks in orbits}
    capacity_survivors = {
        masks: choices for masks, choices in assignments.items() if choices
    }
    assert len(capacity_survivors) == 49
    assert sum(map(len, capacity_survivors.values())) == 147

    exact_double_closed = {
        masks for masks, choices in capacity_survivors.items()
        if all(
            rank_two_certificate(masks, hard, exact_double_only=True)
            for hard in choices
        )
    }
    rank_two_closed = {
        masks for masks, choices in capacity_survivors.items()
        if all(rank_two_certificate(masks, hard) for hard in choices)
    }
    assert len(exact_double_closed) == 18
    assert len(rank_two_closed) == 33

    binary_closed = {
        masks for masks, choices in capacity_survivors.items()
        if masks not in rank_two_closed
        and all(
            rank_two_certificate(masks, hard)
            or free_plane_monomial_certificate(masks, hard)
            for hard in choices
        )
    }
    assert binary_closed == EXPECTED_BINARY_STAGE

    residual = {}
    row_lock_counts = {}
    for masks, choices in capacity_survivors.items():
        remaining = tuple(
            hard for hard in choices
            if not rank_two_certificate(masks, hard)
            and not free_plane_monomial_certificate(masks, hard)
        )
        if remaining:
            counts = {anchor_chart_counts(masks, hard) for hard in remaining}
            assert len(counts) == 1
            residual[masks] = (len(choices), len(remaining), counts.pop())
            locked_counts = {
                (
                    len(row_lock_chart_signatures(
                        masks, hard, collision_free=False
                    )),
                    len(row_lock_chart_signatures(
                        masks, hard, collision_free=True
                    )),
                )
                for hard in remaining
            }
            assert len(locked_counts) == 1
            row_lock_counts[masks] = locked_counts.pop()

    assert residual == EXPECTED_RESIDUAL
    assert row_lock_counts == EXPECTED_ROW_LOCK_COUNTS
    assert sum(data[1] for data in residual.values()) == 36
    assert sum(
        bool(rank_two_certificate(masks, hard))
        for masks, choices in capacity_survivors.items()
        for hard in choices
    ) == 103
    assert sum(
        bool(free_plane_monomial_certificate(masks, hard))
        for masks, choices in capacity_survivors.items()
        for hard in choices
        if not rank_two_certificate(masks, hard)
    ) == 8

    print("five-site incidence orbits:", len(orbits))
    print("hard-capacity survivors:", len(capacity_survivors))
    print("closed by exact-double rank criterion:", len(exact_double_closed))
    print("closed by nontriple rank criterion:", len(rank_two_closed))
    print("additional binary/free-plane closures:", len(binary_closed))
    print("residual orbits / hard assignments:", len(residual), "/", 36)
    for masks, data in residual.items():
        print(masks, "assignments(total,residual)=", data[:2],
              "anchor charts=", data[2],
              "row-lock charts=", row_lock_counts[masks])


if __name__ == "__main__":
    main()
