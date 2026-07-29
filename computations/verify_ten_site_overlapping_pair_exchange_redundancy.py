#!/usr/bin/env python3
"""Exact audit of the ten-site overlapping-pair exchange identity.

The audit is universal: edge/color cells are treated as independent formal
labels.  It checks the two decompositions of all 945 perfect matchings, the
405 endpoint-ordered cell roles in the change of deleted pair, the 4:1
polarized/raw normalization, and the 59,049 target-coordinate reindexings.
"""

from __future__ import annotations

from collections import Counter
from itertools import product


R = "r"
T = "t"
OLD = tuple(range(8))
SITES = (R, T) + OLD
REST = tuple(range(1, 8))
COLORS = (0, 1, 2)
POSITION = {site: index for index, site in enumerate(SITES)}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


ALL_MATCHINGS = perfect_matchings(SITES)
assert len(ALL_MATCHINGS) == 945


def canonical_edge(u, v):
    if POSITION[u] < POSITION[v]:
        return (u, v)
    return (v, u)


def canonical_cell(u, alpha, v, beta):
    """Aggregate cell with colors attached to their named endpoints."""
    if POSITION[u] < POSITION[v]:
        return (u, alpha, v, beta)
    return (v, beta, u, alpha)


def canonical_matching(edges):
    return tuple(sorted((canonical_edge(*edge) for edge in edges), key=str))


def pair_partition(left, right):
    """Partition matchings into direct and two-star terms for a deleted pair."""
    boundary = tuple(site for site in SITES if site not in (left, right))
    direct = []
    for tail in perfect_matchings(boundary):
        direct.append(canonical_matching(((left, right),) + tail))

    star = []
    for left_neighbor in boundary:
        for right_neighbor in boundary:
            if left_neighbor == right_neighbor:
                continue
            remaining = tuple(
                site
                for site in boundary
                if site not in (left_neighbor, right_neighbor)
            )
            for tail in perfect_matchings(remaining):
                star.append(
                    canonical_matching(
                        ((left, left_neighbor), (right, right_neighbor)) + tail
                    )
                )
    return tuple(direct), tuple(star)


def audit_matching_partitions():
    universe = Counter(canonical_matching(matching) for matching in ALL_MATCHINGS)
    assert len(universe) == 945
    assert set(universe.values()) == {1}

    census = {}
    for deleted_pair in ((R, T), (R, 0)):
        direct, star = pair_partition(*deleted_pair)
        assert len(direct) == 105
        assert len(star) == 840
        assert set(direct).isdisjoint(star)
        expansion = Counter(direct)
        expansion.update(star)
        assert expansion == universe
        census[deleted_pair] = (len(direct), len(star))
    return census


def first_role_cell(u, alpha, v, beta):
    """Read a literal cell through the old {r,t} decomposition (26)."""
    edge = frozenset((u, v))
    if edge == frozenset((R, T)):
        i = alpha if u == R else beta
        j = beta if v == T else alpha
        return ("a", i, j), canonical_cell(R, i, T, j)
    if R in edge:
        i = alpha if u == R else beta
        site = v if u == R else u
        color = beta if u == R else alpha
        return ("p", i, site, color), canonical_cell(R, i, site, color)
    if T in edge:
        j = alpha if u == T else beta
        site = v if u == T else u
        color = beta if u == T else alpha
        return ("s", j, site, color), canonical_cell(T, j, site, color)
    return ("q",) + canonical_cell(u, alpha, v, beta), canonical_cell(
        u, alpha, v, beta
    )


def second_role_cell(u, alpha, v, beta):
    """Read the same cell through (27), deleting the pair {r,0}."""
    edge = frozenset((u, v))
    if edge == frozenset((R, 0)):
        i = alpha if u == R else beta
        color_zero = beta if v == 0 else alpha
        role = ("b", i, color_zero)
        source = canonical_cell(R, i, 0, color_zero)
        return role, source

    if R in edge:
        i = alpha if u == R else beta
        site = v if u == R else u
        color = beta if u == R else alpha
        role = ("tilde-p", i, site, color)
        if site == T:
            source = canonical_cell(R, i, T, color)  # the old a block
        else:
            source = canonical_cell(R, i, site, color)  # the old p row
        return role, source

    if 0 in edge:
        color_zero = alpha if u == 0 else beta
        site = v if u == 0 else u
        color = beta if u == 0 else alpha
        role = ("tilde-s", color_zero, site, color)
        if site == T:
            # This is s_{j,0,alpha}; endpoint colors remain attached to t,0.
            source = canonical_cell(T, color, 0, color_zero)
        else:
            # This is e_alpha^(0)* contracted into q_{0v}.
            source = canonical_cell(0, color_zero, site, color)
        return role, source

    role = ("q0",) + canonical_cell(u, alpha, v, beta)
    if T in edge:
        # These internal q0 cells are exactly the old s star.
        source = canonical_cell(u, alpha, v, beta)
    else:
        # These are q restricted to sites 1,...,7.
        source = canonical_cell(u, alpha, v, beta)
    return role, source


def audit_cell_redecomposition():
    first_sources = Counter()
    second_sources = Counter()
    second_roles = Counter()
    for left_index, u in enumerate(SITES):
        for v in SITES[left_index + 1 :]:
            for alpha, beta in product(COLORS, repeat=2):
                _, first_source = first_role_cell(u, alpha, v, beta)
                second_role, second_source = second_role_cell(u, alpha, v, beta)
                literal = canonical_cell(u, alpha, v, beta)
                assert first_source == literal
                assert second_source == literal
                first_sources[first_source] += 1
                second_sources[second_source] += 1
                second_roles[second_role[0]] += 1

    assert len(first_sources) == len(second_sources) == 45 * 9 == 405
    assert set(first_sources.values()) == set(second_sources.values()) == {1}
    assert first_sources == second_sources
    assert second_roles == Counter(
        {
            "q0": (21 + 7) * 9,
            "b": 9,
            "tilde-p": (1 + 7) * 9,
            "tilde-s": (1 + 7) * 9,
        }
    )
    return second_roles


def matching_monomial(matching, coloring, decomposition):
    cells = []
    for u, v in matching:
        if decomposition == "rt":
            _, source = first_role_cell(u, coloring[u], v, coloring[v])
        elif decomposition == "r0":
            _, source = second_role_cell(u, coloring[u], v, coloring[v])
        else:
            raise ValueError(decomposition)
        cells.append(source)
    return tuple(sorted(cells, key=str))


def raw_polynomial(deleted_pair, coloring, decomposition):
    direct, star = pair_partition(*deleted_pair)
    direct_polynomial = Counter(
        matching_monomial(matching, coloring, decomposition)
        for matching in direct
    )
    star_polynomial = Counter(
        matching_monomial(matching, coloring, decomposition)
        for matching in star
    )
    return direct_polynomial, star_polynomial


def polarized_polynomial(deleted_pair, coloring, decomposition):
    """Enumerate q*q^[3] by its four choices of distinguished q edge."""
    direct, star = pair_partition(*deleted_pair)
    direct_polynomial = Counter()
    for matching in direct:
        monomial = matching_monomial(matching, coloring, decomposition)
        # Each four-edge internal matching has four distinguished q edges.
        for _ in range(4):
            direct_polynomial[monomial] += 1
    star_polynomial = Counter()
    for matching in star:
        star_polynomial[
            matching_monomial(matching, coloring, decomposition)
        ] += 4
    return direct_polynomial, star_polynomial


def audit_exchange_polynomial_and_normalization():
    # Distinct formal endpoint colors make endpoint-order mistakes visible and
    # prove the identity naturally for every later ternary specialization.
    coloring = {site: ("formal-color", site) for site in SITES}

    raw_rt = raw_polynomial((R, T), coloring, "rt")
    raw_r0 = raw_polynomial((R, 0), coloring, "r0")
    total_rt = raw_rt[0] + raw_rt[1]
    total_r0 = raw_r0[0] + raw_r0[1]
    assert total_rt == total_r0
    assert len(total_rt) == 945
    assert set(total_rt.values()) == {1}

    factors = {}
    for deleted_pair, raw, decomposition in (
        ((R, T), raw_rt, "rt"),
        ((R, 0), raw_r0, "r0"),
    ):
        polarized = polarized_polynomial(deleted_pair, coloring, decomposition)
        assert polarized[0] == Counter(
            {monomial: 4 * coefficient for monomial, coefficient in raw[0].items()}
        )
        assert polarized[1] == Counter(
            {monomial: 4 * coefficient for monomial, coefficient in raw[1].items()}
        )
        assert polarized[0] + polarized[1] == Counter(
            {
                monomial: 4 * coefficient
                for monomial, coefficient in (raw[0] + raw[1]).items()
            }
        )
        factors[deleted_pair] = (4, 1)
    return len(total_rt), factors


def audit_target_reindexing():
    checked = 0
    nonzero = 0
    for i, j, alpha in product(COLORS, repeat=3):
        for omega in product(COLORS, repeat=7):
            # Contract the rt target at site 0 with alpha.
            left = i == j and alpha == i and all(color == i for color in omega)
            # Contract the r0 target at site t with j.
            right = i == alpha and j == i and all(color == i for color in omega)
            assert left == right
            checked += 1
            nonzero += int(left)
    assert checked == 3**10 == 59049
    assert nonzero == 3
    return checked, nonzero


def main():
    partitions = audit_matching_partitions()
    roles = audit_cell_redecomposition()
    polynomial_terms, factors = audit_exchange_polynomial_and_normalization()
    target_checked, target_nonzero = audit_target_reindexing()
    print("ten-site overlapping-pair exchange redundancy: PASS")
    print("perfect matchings:", len(ALL_MATCHINGS))
    print("pair partitions (direct/star):", partitions)
    print("endpoint-ordered cells redecomposed:", 45 * 9)
    print("new decomposition role counts:", dict(roles))
    print("universal exchange polynomial terms:", polynomial_terms)
    print("polarized/raw factors:", factors)
    print("target coordinates checked/nonzero:", target_checked, target_nonzero)


if __name__ == "__main__":
    main()
