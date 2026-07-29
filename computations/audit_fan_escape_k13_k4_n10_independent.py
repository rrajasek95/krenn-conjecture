#!/usr/bin/env python3
"""Clean-room audit of the N=10 K_{1,3} disjoint K_4 escape chart.

This checker deliberately imports no project module.  It reconstructs the
support-pattern census from the stated necessary conditions, identifies the
single symmetry orbit, and proves that every residual pattern has a
six-site zero cofactor.  The resulting nine-dimensional block-variation
space lies in the source Hessian kernel and is disjoint from the gauge
space, contradicting gauge rigidity.

All combinatorics are exhaustive.  Linear ranks are computed over Q with
``fractions.Fraction``.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json


SITES = tuple(range(8))
CENTER = 0
LEAVES = frozenset((1, 2, 3))
OUTSIDE = frozenset((4, 5, 6, 7))
K0 = frozenset((CENTER, *LEAVES))

# The defect vector for K_{1,3}: the centre is the positive shore, the
# leaves are the negative shore, and the nonbipartite K_4 has value zero.
ZETA = {CENTER: 1, 1: -1, 2: -1, 3: -1, 4: 0, 5: 0, 6: 0, 7: 0}

STAR_EDGES = frozenset((CENTER, leaf) for leaf in LEAVES)
K4_EDGES = frozenset(combinations(sorted(OUTSIDE), 2))
RANK3_EDGES = STAR_EDGES | K4_EDGES
ALL_PAIRS = tuple(combinations(SITES, 2))


def pair(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def perfect_matchings(vertices: tuple[int, ...]):
    """Enumerate labelled perfect matchings without duplication."""

    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield (pair(first, second),) + tail


def exact_rank(rows: list[list[Fraction | int]]) -> int:
    """Fraction-free-in-spirit Gaussian rank over Q."""

    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [entry / scale for entry in matrix[rank]]
        for row in range(row_count):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def support_families() -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(support)
        for size in (1, 2)
        for support in combinations(SITES, size)
    )


def live_product(i: int, j: int, p_support, s_support) -> bool:
    return (i in p_support and j in s_support) or (
        i in s_support and j in p_support
    )


def single_product(i: int, j: int, p_support, s_support) -> bool:
    return (i in p_support and j in s_support) != (
        i in s_support and j in p_support
    )


def reconstruct_residual_patterns():
    """Rebuild the defect-one support census from its necessary filters.

    F1: a live single product on a zeta-invisible pair dies.
    F2: at least one zeta-visible product is live.
    F3: every site has at least three available nonzero-block partners.
    F4: a proper defect component has a live interface block.
    """

    survivors = []
    supports = support_families()
    for p_support, s_support in product(supports, repeat=2):
        some_visible = False
        live_interface = False
        failed = False
        for i, j in ALL_PAIRS:
            visible = ZETA[i] + ZETA[j] != 0
            if not live_product(i, j, p_support, s_support):
                continue
            if not visible and single_product(i, j, p_support, s_support):
                failed = True
                break
            if visible:
                some_visible = True
                if (i in K0) != (j in K0):
                    live_interface = True
        if failed or not some_visible or not live_interface:
            continue

        for site in SITES:
            partners = set()
            for i, j in ALL_PAIRS:
                if site not in (i, j):
                    continue
                mate = j if site == i else i
                edge = pair(i, j)
                visible = ZETA[i] + ZETA[j] != 0
                if edge in RANK3_EDGES:
                    partners.add(mate)
                elif visible:
                    if live_product(i, j, p_support, s_support):
                        partners.add(mate)
                else:
                    # An invisible non-rank-three block is unrestricted by
                    # the product equation, so count it adversarially.
                    partners.add(mate)
            if len(partners) < 3:
                failed = True
                break
        if not failed:
            survivors.append((p_support, s_support))
    return tuple(survivors)


def symmetry_orbit():
    """Orbit of ({1,2},{3,4}) under S_3 x S_4 and p/s exchange."""

    base_p = frozenset((1, 2))
    base_s = frozenset((3, 4))
    orbit = set()
    for leaves_image in permutations(sorted(LEAVES)):
        for outside_image in permutations(sorted(OUTSIDE)):
            relabel = {CENTER: CENTER}
            relabel.update(dict(zip(sorted(LEAVES), leaves_image)))
            relabel.update(dict(zip(sorted(OUTSIDE), outside_image)))
            p_image = frozenset(relabel[site] for site in base_p)
            s_image = frozenset(relabel[site] for site in base_s)
            orbit.add((p_image, s_image))
            orbit.add((s_image, p_image))
    return frozenset(orbit)


def pattern_normal_form(p_support, s_support):
    """Return (two leaves, distinguished leaf, outside port)."""

    if p_support <= LEAVES and len(p_support) == 2:
        leaf_pair, mixed = p_support, s_support
    elif s_support <= LEAVES and len(s_support) == 2:
        leaf_pair, mixed = s_support, p_support
    else:
        raise AssertionError((p_support, s_support))
    distinguished = mixed & LEAVES
    outside = mixed & OUTSIDE
    assert len(distinguished) == len(outside) == 1
    assert leaf_pair | distinguished == LEAVES
    assert not (leaf_pair & distinguished)
    return leaf_pair, next(iter(distinguished)), next(iter(outside))


def allowed_q_support(p_support, s_support):
    """Physical block support allowed by the residual product equation."""

    invisible = {
        pair(i, j) for i, j in ALL_PAIRS if ZETA[i] + ZETA[j] == 0
    }
    # For this graph the invisible pairs are exactly the prescribed
    # rank-three K_{1,3} disjoint K_4 edges; record this load-bearing fact.
    assert invisible == set(RANK3_EDGES)
    live_visible = {
        pair(i, j)
        for i, j in ALL_PAIRS
        if ZETA[i] + ZETA[j] != 0
        and live_product(i, j, p_support, s_support)
    }
    return frozenset(invisible | live_visible)


def matrix_unit(a: int, b: int):
    return tuple(
        tuple(Fraction(int(row == a and column == b)) for column in range(3))
        for row in range(3)
    )


def block_variation_basis(deleted_pair):
    return tuple(
        {deleted_pair: matrix_unit(a, b)} for a in range(3) for b in range(3)
    )


def cofactor_matching_support(remaining, q_support):
    matchings = tuple(perfect_matchings(tuple(sorted(remaining))))
    supported = tuple(
        matching
        for matching in matchings
        if all(edge in q_support for edge in matching)
    )
    return matchings, supported


def hessian_image_support(variation, remaining_supported_matchings):
    """Support of Z q^[3]; empty matching support means exact zero tensor."""

    assert len(variation) == 1
    if not remaining_supported_matchings:
        return frozenset()
    varied_pair = next(iter(variation))
    return frozenset((varied_pair, matching) for matching in remaining_supported_matchings)


def gauge_intersection_nullity(q_support, varied_pair):
    """Bound gauges supported on one block by exact scalar constraints.

    A gauge is Z^alpha_ij=(alpha_i+alpha_j)q_ij with sum alpha_i=0.
    If it is supported on ``varied_pair``, alpha_i+alpha_j=0 on every
    guaranteed nonzero q block other than that pair.
    """

    rows = [[Fraction(1) for _ in SITES]]
    for i, j in sorted(q_support - {varied_pair}):
        row = [Fraction(0) for _ in SITES]
        row[i] = 1
        row[j] = 1
        rows.append(row)
    return len(SITES) - exact_rank(rows)


def main():
    patterns = reconstruct_residual_patterns()
    assert len(patterns) == 24, len(patterns)
    pattern_set = frozenset(patterns)
    orbit = symmetry_orbit()
    assert len(orbit) == 24
    assert pattern_set == orbit

    total_matchings = 0
    total_supported = 0
    total_kernel_directions = 0
    gauge_nullities = []
    ledger = []

    for p_support, s_support in patterns:
        leaf_pair, distinguished, outside = pattern_normal_form(
            p_support, s_support
        )
        deleted_pair = pair(CENTER, distinguished)
        remaining = frozenset(SITES) - frozenset(deleted_pair)
        q_support = allowed_q_support(p_support, s_support)

        # Once centre and distinguished leaf are deleted, each leaf in
        # leaf_pair has the sole possible mate ``outside``.  Thus no perfect
        # matching exists on the six remaining sites.
        for leaf in leaf_pair:
            remaining_mates = {
                mate
                for mate in remaining - {leaf}
                if pair(leaf, mate) in q_support
            }
            assert remaining_mates == {outside}

        matchings, supported = cofactor_matching_support(remaining, q_support)
        assert len(matchings) == 15
        assert not supported
        total_matchings += len(matchings)
        total_supported += len(supported)

        variations = block_variation_basis(deleted_pair)
        assert len(variations) == 9
        variation_rows = [
            [entry for row in next(iter(variation.values())) for entry in row]
            for variation in variations
        ]
        assert exact_rank(variation_rows) == 9
        for variation in variations:
            assert not hessian_image_support(variation, supported)
        total_kernel_directions += len(variations)

        nullity = gauge_intersection_nullity(q_support, deleted_pair)
        assert nullity <= 1
        gauge_nullities.append(nullity)
        # Here the guaranteed blocks make the intersection actually zero.
        assert nullity == 0

        ledger.append(
            {
                "p": sorted(p_support),
                "s": sorted(s_support),
                "leaf_pair": sorted(leaf_pair),
                "distinguished": distinguished,
                "outside": outside,
                "deleted_pair": list(deleted_pair),
                "remaining_matchings": len(matchings),
                "supported_matchings": len(supported),
                "block_kernel_dimension": len(variations),
                "gauge_intersection_nullity": nullity,
            }
        )

    assert total_matchings == 24 * 15 == 360
    assert total_supported == 0
    assert total_kernel_directions == 24 * 9 == 216
    assert set(gauge_nullities) == {0}

    # The zero-sum alpha parameter space has dimension seven.  A
    # nine-dimensional Hessian-kernel subspace, even with intersection at
    # most one, cannot be the gauge kernel.  The exact calculation is
    # stronger here: the intersection is zero in every pattern.
    gauge_dimension_upper_bound = len(SITES) - 1
    block_kernel_dimension = 9
    assert block_kernel_dimension > gauge_dimension_upper_bound

    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    print("independent N=10 K13+K4 escape audit: PASS")
    print("support census: 24 of 1296 patterns; one S3 x S4 x C2 orbit")
    print(
        "six-site cofactor ledger: "
        f"{total_matchings} perfect matchings tested, {total_supported} supported"
    )
    print(
        "block-variation kernel: 9 directions per pattern, "
        f"{total_kernel_directions} exact zero images total"
    )
    print(
        "gauge comparison: intersection nullity 0 in all 24 patterns; "
        "block kernel dimension 9 > gauge upper bound 7"
    )
    print(f"independent ledger sha256: {digest}")


if __name__ == "__main__":
    main()
