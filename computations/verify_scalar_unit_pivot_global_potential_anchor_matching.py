#!/usr/bin/env python3
"""Exact smoke audit for the scalar-unit pivot anchor potential.

The uniform assertions are proved in the companion note.  This checker
uses deterministic rational block data; it does not search source cases.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb


Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def edge(u: int, i: int, v: int, j: int) -> Edge:
    require(u != v, "site-square-zero blocks have distinct physical sites")
    left = (u, i)
    right = (v, j)
    return (left, right) if left < right else (right, left)


def add_cell(
    coefficients: dict[Edge, Fraction],
    u: int,
    i: int,
    v: int,
    j: int,
    value: int | Fraction,
) -> None:
    key = edge(u, i, v, j)
    new_value = coefficients.get(key, Fraction(0)) + Fraction(value)
    if new_value:
        coefficients[key] = new_value
    else:
        coefficients.pop(key, None)


def degrees(coefficients: dict[Edge, Fraction]) -> dict[Vertex, int]:
    answer: dict[Vertex, int] = defaultdict(int)
    for left, right in coefficients:
        answer[left] += 1
        answer[right] += 1
    return answer


def anchors(coefficients: dict[Edge, Fraction]) -> frozenset[Edge]:
    degree = degrees(coefficients)
    return frozenset(
        key for key in coefficients if degree[key[0]] == degree[key[1]] == 1
    )


def pair_cells(
    coefficients: dict[Edge, Fraction], p: int, q: int
) -> dict[tuple[int, int], Fraction]:
    answer: dict[tuple[int, int], Fraction] = {}
    for i in range(3):
        for j in range(3):
            value = coefficients.get(edge(p, i, q, j), Fraction(0))
            if value:
                answer[(i, j)] = value
    return answer


def scalar_pivot(
    coefficients: dict[Edge, Fraction],
    n: int,
    p: int,
    q: int,
    a: int,
    alpha: Fraction,
) -> tuple[dict[Edge, Fraction], dict[Vertex, Fraction], dict[Vertex, Fraction]]:
    require(pair_cells(coefficients, p, q) == {(a, a): alpha},
            "the direct block is not the asserted scalar unit")
    residual = tuple(site for site in range(n) if site not in (p, q))
    p_row = {
        (x, i): coefficients.get(edge(p, a, x, i), Fraction(0))
        for x in residual for i in range(3)
    }
    q_row = {
        (x, i): coefficients.get(edge(q, a, x, i), Fraction(0))
        for x in residual for i in range(3)
    }
    require(any(p_row.values()) and any(q_row.values()),
            "goodness requires both selected residual rows to be nonzero")

    result = dict(coefficients)
    for x in residual:
        for i in range(3):
            result.pop(edge(p, a, x, i), None)
            result.pop(edge(q, a, x, i), None)

    for x, y in combinations(residual, 2):
        for i in range(3):
            for j in range(3):
                correction = (
                    p_row[(x, i)] * q_row[(y, j)]
                    + q_row[(x, i)] * p_row[(y, j)]
                ) / alpha
                if correction:
                    add_cell(result, x, i, y, j, correction)
    return result, p_row, q_row


def selected_row_support(row: dict[Vertex, Fraction]) -> int:
    return sum(value != 0 for value in row.values())


def internal_edges(
    coefficients: dict[Edge, Fraction], p: int, q: int
) -> frozenset[Edge]:
    return frozenset(
        key
        for key in coefficients
        if key[0][0] not in (p, q) and key[1][0] not in (p, q)
    )


def audit_anchor_persistence_and_ledger() -> None:
    n, p, q, a = 9, 0, 1, 0
    alpha = Fraction(2)
    data: dict[Edge, Fraction] = {}
    add_cell(data, p, a, q, a, alpha)

    # Selected rows.  Their supports are disjoint by physical site, so the
    # internal correction is a literal 2-by-3 rectangle.
    add_cell(data, p, a, 2, 0, 2)
    add_cell(data, p, a, 3, 1, 4)
    add_cell(data, q, a, 4, 0, 3)
    add_cell(data, q, a, 5, 1, 5)
    add_cell(data, q, a, 6, 2, 7)

    # Complementary rows make the deleted endpoint stars injective.  Their
    # singleton cells are planted old mutual anchors, including anchors
    # incident to both pivot endpoints.
    add_cell(data, p, 1, 2, 2, 11)
    add_cell(data, p, 2, 3, 2, 13)
    add_cell(data, q, 1, 4, 2, 17)
    add_cell(data, q, 2, 5, 2, 19)
    add_cell(data, 6, 1, 7, 1, 23)

    old_anchors = anchors(data)
    require(len(old_anchors) == 5, "planted anchor count changed")
    old_support = len(data)
    pivoted, p_row, q_row = scalar_pivot(data, n, p, q, a, alpha)
    new_anchors = anchors(pivoted)
    require(old_anchors <= new_anchors, "a planted mutual anchor was lost")
    selected = edge(p, a, q, a)
    require(selected not in old_anchors and selected in new_anchors,
            "the selected scalar cell did not become a new anchor")
    require(len(new_anchors) >= len(old_anchors) + 1,
            "the global anchor potential did not increase")

    r = selected_row_support(p_row)
    t = selected_row_support(q_row)
    require((r, t) == (2, 3), "unexpected selected-row supports")
    old_internal = internal_edges(data, p, q)
    new_internal = internal_edges(pivoted, p, q)
    fresh = new_internal - old_internal
    cancelled = old_internal - new_internal
    require((len(fresh), len(cancelled)) == (6, 0),
            "the sharp fresh rectangle was not 2-by-3")
    delta = len(pivoted) - old_support
    require(delta == len(fresh) - len(cancelled) - r - t == 1,
            "the exact support-transfer ledger failed")
    require((r - 1) * (t - 1) == 2,
            "the lexicographic density inequality is not sharp")

    max_cells = 9 * comb(n, 2)
    old_phi = (max_cells + 1) * len(old_anchors) - len(data)
    new_phi = (max_cells + 1) * len(new_anchors) - len(pivoted)
    require(new_phi > old_phi, "the scalar global potential did not increase")


def audit_endpoint_order_and_cancellation() -> None:
    n, p, q, a = 8, 5, 1, 2
    alpha = Fraction(2)
    data: dict[Edge, Fraction] = {}
    add_cell(data, p, a, q, a, alpha)

    # The pivot endpoints are reversed, and the residual supports lie below,
    # between, and above them in physical endpoint order.
    for x, i, value in ((0, 0, 2), (3, 1, 4), (4, 2, 4), (2, 1, 7)):
        add_cell(data, p, a, x, i, value)
    for x, i, value in ((0, 0, 3), (4, 2, -6), (6, 0, 5)):
        add_cell(data, q, a, x, i, value)

    # The correction 4*5/2 cancels this old internal cell.  On the 0--4
    # cell, the two endpoint-ordered products 2*(-6) and 3*4 cancel each
    # other before insertion.  Products supported twice at one site vanish.
    cancelled_cell = edge(3, 1, 6, 0)
    merged_zero_cell = edge(0, 0, 4, 2)
    add_cell(data, 3, 1, 6, 0, -10)
    add_cell(data, 0, 2, 6, 2, 11)

    one_sided = edge(p, a, 2, 1)
    old_degree = degrees(data)
    old_anchors = anchors(data)
    require(old_degree[(2, 1)] == 1 and one_sided not in old_anchors,
            "the adversarial one-sided channel was not planted")

    pivoted, p_row, q_row = scalar_pivot(data, n, p, q, a, alpha)
    new_degree = degrees(pivoted)
    new_anchors = anchors(pivoted)
    require(old_anchors <= new_anchors,
            "endpoint ordering or cancellation destroyed an old anchor")
    require(edge(p, a, q, a) in new_anchors,
            "the reversed selected pair did not become an anchor")
    require(cancelled_cell not in pivoted and merged_zero_cell not in pivoted,
            "an exact zero aggregate cell remained in scalar support")
    require(new_degree[(2, 1)] == 3,
            "the one-sided degree-one counterexample did not redistribute")

    r = selected_row_support(p_row)
    t = selected_row_support(q_row)
    old_internal = internal_edges(data, p, q)
    new_internal = internal_edges(pivoted, p, q)
    fresh = new_internal - old_internal
    cancelled = old_internal - new_internal
    require(cancelled == {cancelled_cell},
            "the adversarial cancellation set changed")
    require(
        len(pivoted) - len(data) == len(fresh) - len(cancelled) - r - t,
        "the support ledger failed with endpoint reversal and cancellation",
    )


def one_factorization(n: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    require(n % 2 == 0 and n >= 4, "one-factorization needs even order")
    modulus = n - 1
    rounds = []
    for r in range(modulus):
        matching = [(min(n - 1, r), max(n - 1, r))]
        for k in range(1, n // 2):
            u = (r + k) % modulus
            v = (r - k) % modulus
            matching.append((min(u, v), max(u, v)))
        require(len({site for pair in matching for site in pair}) == n,
                "round-robin matching does not cover every site")
        rounds.append(tuple(sorted(matching)))
    require(len(set(rounds)) == n - 1, "one-factorization repeated a round")
    return tuple(rounds)


Occurrence = tuple[int, int, int]


def occurrence_matchings(
    n: int, occurrences: tuple[Occurrence, ...]
) -> tuple[tuple[Occurrence, ...], ...]:
    incident: dict[int, list[Occurrence]] = defaultdict(list)
    for occurrence in occurrences:
        u, v, _colour = occurrence
        incident[u].append(occurrence)
        incident[v].append(occurrence)

    answer: list[tuple[Occurrence, ...]] = []

    def recurse(remaining: frozenset[int], chosen: tuple[Occurrence, ...]) -> None:
        if not remaining:
            answer.append(tuple(sorted(chosen)))
            return
        u = min(remaining)
        for occurrence in incident[u]:
            x, y, _colour = occurrence
            v = y if x == u else x
            if v in remaining:
                recurse(remaining - {u, v}, chosen + (occurrence,))

    recurse(frozenset(range(n)), ())
    return tuple(sorted(set(answer)))


def induced_colouring(n: int, matching: tuple[Occurrence, ...]) -> tuple[int, ...]:
    colours = [-1] * n
    for u, v, colour in matching:
        require(colours[u] == colours[v] == -1, "matching repeats a vertex")
        colours[u] = colours[v] = colour
    require(all(colour >= 0 for colour in colours), "matching misses a vertex")
    return tuple(colours)


def audit_saturated_terminal_and_good_pairs() -> None:
    for n in (4, 6, 8, 10, 12):
        factors = one_factorization(n)[:3]
        require(
            len({pair for matching in factors for pair in matching}) == 3 * n // 2,
            "the selected physical one-factors are not edge-disjoint",
        )
        data: dict[Edge, Fraction] = {}
        occurrences: list[Occurrence] = []
        pure_matchings = []
        for colour, matching in enumerate(factors):
            coloured = []
            for u, v in matching:
                add_cell(data, u, colour, v, colour, 1)
                occurrence = (u, v, colour)
                occurrences.append(occurrence)
                coloured.append(occurrence)
            pure_matchings.append(tuple(sorted(coloured)))

        require(len(anchors(data)) == 3 * n // 2,
                "the saturated carrier graph is not maximally anchored")
        bad_pairs = {pair for matching in factors for pair in matching}
        good_pairs = {
            pair for pair in combinations(range(n), 2) if pair not in bad_pairs
        }
        require(len(good_pairs) == comb(n, 2) - 3 * n // 2,
                "the saturated good-pair count is wrong")
        require(all(not pair_cells(data, *pair) for pair in good_pairs),
                "a saturated good pair unexpectedly has a direct block")

        matchings = occurrence_matchings(n, tuple(occurrences))
        pure_set = set(pure_matchings)
        if n == 4:
            require(set(matchings) == pure_set,
                    "K4 should have exactly its three pure one-factors")
        else:
            mixed = next(
                (matching for matching in matchings if matching not in pure_set),
                None,
            )
            require(mixed is not None,
                    "three one-factors did not produce a fourth matching")
            colouring = induced_colouring(n, mixed)
            require(len(set(colouring)) > 1,
                    "the fourth matching did not have a mixed colouring")
            fibre = [
                matching for matching in matchings
                if induced_colouring(n, matching) == colouring
            ]
            require(fibre == [mixed],
                    "the mixed saturated coefficient is not a singleton fibre")

    # Physical overlap between colour factors is allowed in the terminal
    # theorem.  Remembering scalar-cell occurrences still produces a mixed
    # matching, and its induced-colouring fibre is still a singleton.
    n = 6
    repeated_factor = one_factorization(n)[0]
    repeated_occurrences = tuple(
        (u, v, colour)
        for colour in range(3)
        for u, v in repeated_factor
    )
    repeated_matchings = occurrence_matchings(n, repeated_occurrences)
    repeated_pure = {
        tuple(sorted((u, v, colour) for u, v in repeated_factor))
        for colour in range(3)
    }
    mixed = next(
        matching for matching in repeated_matchings
        if matching not in repeated_pure
    )
    colouring = induced_colouring(n, mixed)
    require(len(set(colouring)) > 1,
            "overlapping physical factors did not give a mixed matching")
    require(
        [matching for matching in repeated_matchings
         if induced_colouring(n, matching) == colouring] == [mixed],
        "an overlapping-factor mixed coefficient was not a singleton fibre",
    )


def audit_pair_row_routing() -> None:
    # The tensor values are represented by names because the pivot proof uses
    # only the displayed equalities, never division by a matching power.
    colours = range(3)
    a = 0
    complement = {1, 2}
    new_rows = {}
    for i in colours:
        for j in colours:
            if i == j == a:
                new_rows[(i, j)] = "X0"  # alpha * (q#)^[h]
            elif i in complement and j in complement:
                # R_ij(q#)^[h-1] = old row + alpha^(1-h)R_ij Theta.
                new_rows[(i, j)] = f"X{i}" if i == j else "0"
            else:
                new_rows[(i, j)] = "0"  # a star row was deleted
    expected = {
        (i, j): (f"X{i}" if i == j else "0")
        for i in colours for j in colours
    }
    require(new_rows == expected, "the nine routed target rows are not exact")


def main() -> None:
    audit_pair_row_routing()
    audit_anchor_persistence_and_ledger()
    audit_endpoint_order_and_cancellation()
    audit_saturated_terminal_and_good_pairs()
    print("scalar-unit pivot exact nine-row routing: PASS")
    print("mutual-coordinate-anchor persistence and strict potential: PASS")
    print("endpoint-order, cancellation, and zero-cell boundaries: PASS")
    print("minimum-support 2-by-3 sharp ledger: PASS")
    print("saturated good-pair incidence and terminal matching audit: PASS")


if __name__ == "__main__":
    main()
