#!/usr/bin/env python3
"""Clean-room audit of the ten-site pair-slice exchange theorem.

This file deliberately does not import the primary checker.  It uses a
bit-mask perfect-matching generator and a reversible, generic deleted-pair
chart.  The finite checks certify the universal source-polynomial identity;
the separate ternary loop certifies all 3^10 row/boundary reindexings and
GHZ target residuals.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path


PRIMARY_NOTE = "notes/ten-site-overlapping-pair-exchange-redundancy.md"
PRIMARY_CHECKER = (
    "computations/verify_ten_site_overlapping_pair_exchange_redundancy.py"
)
PRIMARY_NOTE_SHA256 = (
    "f482941b671deead2a9e410d2f2e46fd1dc7fbd31e3da7d74a89eeb187b2527b"
)
PRIMARY_CHECKER_SHA256 = (
    "1828193d419455704025b693a6eb9d0dc406d9fcc0abff1949d50c1f518d61c5"
)

# Numeric order is intentional.  In the second chart, the right deleted
# endpoint Z=2 lies after its boundary neighbor T=1.  Thus the audit really
# exercises reversal of a stored physical block's endpoint order.
R, T, Z = 0, 1, 2
TAIL = tuple(range(3, 10))
SITES = tuple(range(10))
COLORS = (0, 1, 2)
FULL_MASK = (1 << len(SITES)) - 1


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def audit_primary_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    assert file_sha256(root / PRIMARY_NOTE) == PRIMARY_NOTE_SHA256
    assert file_sha256(root / PRIMARY_CHECKER) == PRIMARY_CHECKER_SHA256


def edge(u: int, v: int) -> tuple[int, int]:
    assert u != v
    return (u, v) if u < v else (v, u)


def normalize_matching(pairs) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(edge(u, v) for u, v in pairs))


@lru_cache(maxsize=None)
def matchings(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Perfect matchings from a bit mask, independently of chart formulas."""
    if mask == 0:
        return ((),)
    assert mask.bit_count() % 2 == 0
    low_bit = mask & -mask
    u = low_bit.bit_length() - 1
    rest = mask ^ low_bit
    answer = []
    candidates = rest
    while candidates:
        v_bit = candidates & -candidates
        v = v_bit.bit_length() - 1
        for tail in matchings(rest ^ v_bit):
            answer.append(normalize_matching(((u, v),) + tail))
        candidates ^= v_bit
    return tuple(answer)


def mask_of(vertices) -> int:
    answer = 0
    for vertex in vertices:
        answer |= 1 << vertex
    return answer


def chart_expansion(left: int, right: int):
    """Generate the cap and ordered-two-star expansion from scratch."""
    boundary = tuple(u for u in SITES if u not in (left, right))
    boundary_mask = mask_of(boundary)

    direct = []
    for tail in matchings(boundary_mask):
        direct.append(normalize_matching(((left, right),) + tail))

    two_star = []
    for left_neighbor in boundary:
        for right_neighbor in boundary:
            if left_neighbor == right_neighbor:
                continue
            tail_mask = boundary_mask ^ (1 << left_neighbor) ^ (1 << right_neighbor)
            for tail in matchings(tail_mask):
                two_star.append(
                    normalize_matching(
                        (
                            (left, left_neighbor),
                            (right, right_neighbor),
                        )
                        + tail
                    )
                )
    return tuple(direct), tuple(two_star)


def audit_matching_partitions():
    universe = Counter(matchings(FULL_MASK))
    assert len(universe) == 945
    assert set(universe.values()) == {1}

    census = {}
    expansions = {}
    for pair in ((R, T), (R, Z)):
        direct, two_star = chart_expansion(*pair)
        assert len(direct) == 105
        assert len(two_star) == 840
        assert set(direct).isdisjoint(two_star)
        expansion = Counter(direct)
        expansion.update(two_star)
        assert expansion == universe
        census[pair] = (len(direct), len(two_star))
        expansions[pair] = (direct, two_star)
    return universe, expansions, census


def cell(u: int, color_u, v: int, color_v):
    """Literal edge cell with colors kept at their named endpoints."""
    if u < v:
        return (u, color_u, v, color_v)
    return (v, color_v, u, color_u)


def chart_role(pair: tuple[int, int], literal_cell):
    """Encode one cell in a generic ordered deleted-pair chart."""
    left, right = pair
    u, color_u, v, color_v = literal_cell
    colors = {u: color_u, v: color_v}
    endpoints = {u, v}
    if endpoints == {left, right}:
        return ("cap", colors[left], colors[right])
    if left in endpoints:
        neighbor = v if u == left else u
        return ("left-star", colors[left], neighbor, colors[neighbor])
    if right in endpoints:
        neighbor = v if u == right else u
        return ("right-star", colors[right], neighbor, colors[neighbor])
    return ("internal", literal_cell)


def role_cell(pair: tuple[int, int], role):
    """Decode a chart role back to its literal endpoint-ordered cell."""
    left, right = pair
    kind = role[0]
    if kind == "cap":
        _, left_color, right_color = role
        return cell(left, left_color, right, right_color)
    if kind == "left-star":
        _, left_color, neighbor, neighbor_color = role
        return cell(left, left_color, neighbor, neighbor_color)
    if kind == "right-star":
        _, right_color, neighbor, neighbor_color = role
        return cell(right, right_color, neighbor, neighbor_color)
    assert kind == "internal"
    return role[1]


def audit_endpoint_order_redecomposition():
    old_pair = (R, T)
    new_pair = (R, Z)
    old_roles = Counter()
    new_roles = Counter()
    transitions = Counter()
    old_role_keys = Counter()
    new_role_keys = Counter()

    for u in SITES:
        for v in range(u + 1, len(SITES)):
            for color_u, color_v in product(COLORS, repeat=2):
                literal = cell(u, color_u, v, color_v)
                old_role = chart_role(old_pair, literal)
                new_role = chart_role(new_pair, literal)
                assert role_cell(old_pair, old_role) == literal
                assert role_cell(new_pair, new_role) == literal
                old_roles[old_role[0]] += 1
                new_roles[new_role[0]] += 1
                transitions[(old_role[0], new_role[0])] += 1
                old_role_keys[old_role] += 1
                new_role_keys[new_role] += 1

    assert len(old_role_keys) == len(new_role_keys) == 405
    assert set(old_role_keys.values()) == set(new_role_keys.values()) == {1}
    expected_roles = Counter(
        {"cap": 9, "left-star": 72, "right-star": 72, "internal": 252}
    )
    assert old_roles == new_roles == expected_roles
    assert transitions == Counter(
        {
            ("cap", "left-star"): 9,       # old a_{ij}
            ("left-star", "cap"): 9,       # old p at site 0
            ("left-star", "left-star"): 63,
            ("right-star", "right-star"): 9,  # old s at site 0
            ("right-star", "internal"): 63,
            ("internal", "right-star"): 63,
            ("internal", "internal"): 189,
        }
    )
    return old_roles, transitions


def monomial_through_chart(matching, pair, coloring):
    factors = []
    for u, v in matching:
        literal = cell(u, coloring[u], v, coloring[v])
        encoded = chart_role(pair, literal)
        decoded = role_cell(pair, encoded)
        assert decoded == literal
        factors.append(decoded)
    return tuple(sorted(factors, key=repr))


def audit_universal_exchange(expansions):
    # Algebraically independent endpoint tags make this a universal monomial
    # comparison.  The preceding 405-cell audit then specializes it to every
    # ternary coloring without losing endpoint order.
    formal_coloring = {u: ("endpoint-tag", u) for u in SITES}
    polynomials = {}
    for pair in ((R, T), (R, Z)):
        direct, two_star = expansions[pair]
        polynomial = Counter(
            monomial_through_chart(matching, pair, formal_coloring)
            for matching in direct + two_star
        )
        assert len(polynomial) == 945
        assert set(polynomial.values()) == {1}
        polynomials[pair] = polynomial
    assert polynomials[(R, T)] == polynomials[(R, Z)]
    return len(polynomials[(R, T)])


def audit_polarized_raw_factors(expansions):
    factors = {}
    for pair in ((R, T), (R, Z)):
        direct, two_star = expansions[pair]

        raw = Counter(direct)
        raw.update(two_star)
        assert len(raw) == 945 and set(raw.values()) == {1}

        # In b*q*q^[3], project away the choice of the distinguished q edge.
        # Each four-edge boundary matching has exactly four choices.
        polarized = Counter()
        cap_edge = edge(*pair)
        for matching in direct:
            boundary_edges = tuple(e for e in matching if e != cap_edge)
            assert len(boundary_edges) == 4
            for _distinguished_edge in boundary_edges:
                polarized[matching] += 1

        # The polarized two-star term is explicitly 4*p*s*q^[3].
        for matching in two_star:
            for _copy in range(4):
                polarized[matching] += 1

        assert polarized == Counter({matching: 4 for matching in raw})
        factors[pair] = (4, 1)
    return factors


def chart_coordinate(pair, row_colors, boundary_colors):
    boundary = tuple(u for u in SITES if u not in pair)
    assert len(row_colors) == 2 and len(boundary_colors) == 8
    word = [None] * 10
    word[pair[0]], word[pair[1]] = row_colors
    for site, color_value in zip(boundary, boundary_colors):
        word[site] = color_value
    return tuple(word)


def chart_ghz_target(row_colors, boundary_colors):
    color_value = row_colors[0]
    return int(row_colors[1] == color_value and all(c == color_value for c in boundary_colors))


def audit_all_residual_coordinates():
    old_seen = set()
    new_seen = set()
    nonzero_targets = 0

    # omega colors sites 1,...,7 in the notation of the primary note, namely
    # numeric sites 3,...,9 here.
    for i, j, alpha in product(COLORS, repeat=3):
        for omega in product(COLORS, repeat=7):
            old_row = (i, j)
            old_boundary = (alpha,) + omega       # Z, then the seven-tail
            new_row = (i, alpha)
            new_boundary = (j,) + omega           # T, then the seven-tail

            old_word = chart_coordinate((R, T), old_row, old_boundary)
            new_word = chart_coordinate((R, Z), new_row, new_boundary)
            assert old_word == new_word

            old_target = chart_ghz_target(old_row, old_boundary)
            new_target = chart_ghz_target(new_row, new_boundary)
            assert old_target == new_target
            assert old_target == int(len(set(old_word)) == 1)

            # The universal source polynomial was proved identical above.
            # Equality of these exact coordinate descriptors therefore means
            # equality, not merely equal numerical evaluation, of residuals.
            old_descriptor = (old_word, old_target)
            new_descriptor = (new_word, new_target)
            assert old_descriptor == new_descriptor

            old_seen.add((old_row, old_boundary))
            new_seen.add((new_row, new_boundary))
            nonzero_targets += old_target

    assert len(old_seen) == len(new_seen) == 3**10 == 59049
    assert nonzero_targets == 3
    return len(old_seen), nonzero_targets


def main() -> None:
    audit_primary_snapshot()
    _, expansions, census = audit_matching_partitions()
    roles, transitions = audit_endpoint_order_redecomposition()
    universal_terms = audit_universal_exchange(expansions)
    factors = audit_polarized_raw_factors(expansions)
    coordinates, nonzero_targets = audit_all_residual_coordinates()

    print("independent ten-site pair-slice exchange audit: PASS")
    print("frozen primary note/checker: PASS")
    print("perfect matchings and chart partitions:", 945, census)
    print("reversible endpoint-ordered cells:", sum(roles.values()))
    print("old/new role transition census:", dict(transitions))
    print("universal exchange monomials:", universal_terms)
    print("polarized/raw factors:", factors)
    print("residual coordinates/nonzero GHZ targets:", coordinates, nonzero_targets)


if __name__ == "__main__":
    main()
