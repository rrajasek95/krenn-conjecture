#!/usr/bin/env python3
"""Exact audit of the two large-C order-eight flat-core lemmas.

The three selected constant fibres are labelled occurrence matchings.
Thus differently coloured sources on the same physical X--X pair remain
distinct.  The first factor is normalized only by permutations preserving
the cut; all labelled choices of the other two factors are retained.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


VERTICES = tuple(range(8))


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:]):
        rest = vertices[1:position + 1] + vertices[position + 2:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(u, v),) + tail))


MATCHINGS = tuple(perfect_matchings(VERTICES))


def cut_size(matching, C: frozenset[int]) -> int:
    return sum((u in C) != (v in C) for u, v in matching)


def representative(C: frozenset[int], crossings: int):
    """One cut-stabilizer representative with the prescribed cut size."""
    X = frozenset(VERTICES) - C
    c_cross = tuple(sorted(C))[:crossings]
    x_cross = tuple(sorted(X))[:crossings]
    result = [edge(u, v) for u, v in zip(c_cross, x_cross)]
    c_rest = tuple(sorted(C - frozenset(c_cross)))
    x_rest = tuple(sorted(X - frozenset(x_cross)))
    result.extend(edge(c_rest[i], c_rest[i + 1])
                  for i in range(0, len(c_rest), 2))
    result.extend(edge(x_rest[i], x_rest[i + 1])
                  for i in range(0, len(x_rest), 2))
    return tuple(sorted(result))


def partner(matching, u: int) -> int:
    pair = next(pair for pair in matching if u in pair)
    return pair[0] if pair[1] == u else pair[1]


def distinct_c_neighbours(factors, C: frozenset[int]) -> bool:
    return all(len({partner(matching, u) for matching in factors}) == 3
               for u in C)


def cross_occurrences(factors, C: frozenset[int]):
    answer = []
    for colour, matching in enumerate(factors):
        for u, v in matching:
            if (u in C) != (v in C):
                c, x = (u, v) if u in C else (v, u)
                answer.append((colour, c, x))
    return tuple(answer)


def cross_degrees(factors, C: frozenset[int]) -> Counter:
    return Counter(x for _colour, _c, x in cross_occurrences(factors, C))


def boundary_degree_feasible(factors, C: frozenset[int]) -> bool:
    """The pointwise order-eight bound r_x >= |C|-2."""
    X = frozenset(VERTICES) - C
    degrees = cross_degrees(factors, C)
    return all(degrees[x] >= len(C) - 2 for x in X)


def occurrence_matchings(factors):
    """Enumerate perfect matchings in the occurrence multigraph."""
    incidences = {u: [] for u in VERTICES}
    selected = set()
    for colour, matching in enumerate(factors):
        selected_matching = []
        for u, v in matching:
            occurrence = (colour, u, v)
            selected_matching.append(occurrence)
            incidences[u].append(occurrence)
            incidences[v].append(occurrence)
        selected.add(tuple(sorted(selected_matching)))

    answer = []

    def visit(uncovered: frozenset[int], chosen: tuple):
        if not uncovered:
            matching = tuple(sorted(chosen))
            if matching not in selected:
                answer.append(matching)
            return
        u = min(uncovered)
        for occurrence in incidences[u]:
            _colour, a, b = occurrence
            v = b if a == u else a
            if v in uncovered:
                visit(uncovered - {u, v}, chosen + (occurrence,))

    visit(frozenset(VERTICES), ())
    return tuple(answer)


def occurrence_cut_size(matching, C: frozenset[int]) -> int:
    return sum((u in C) != (v in C) for _colour, u, v in matching)


def c3_forced_zero_pairs(factors, C: frozenset[int]):
    """Pairs forced zero by one-edge exchanges from an all-cross colour."""
    X = frozenset(VERTICES) - C
    high = next(colour for colour, matching in enumerate(factors)
                if cut_size(matching, C) == 3)
    base = factors[high]
    y = {c: partner(base, c) for c in C}
    leftovers = tuple(sorted(X - frozenset(y.values())))
    require(
        len(leftovers) == 2,
        "len(leftovers) == 2",
    )
    p, q = leftovers
    forced_zero = set()
    for colour, c, x in cross_occurrences(factors, C):
        if x == p:
            require(
                colour != high,
                "colour != high",
            )
            forced_zero.add(edge(q, y[c]))
        elif x == q:
            require(
                colour != high,
                "colour != high",
            )
            forced_zero.add(edge(p, y[c]))
    return frozenset(forced_zero)


def has_bad_x_graph_avoiding(forced_zero, factors, C) -> bool:
    """Can the X-bad graph meet degree >=5 while avoiding forced zeros?"""
    X = tuple(sorted(frozenset(VERTICES) - C))
    degrees_cross = cross_degrees(factors, C)
    available = [pair for pair in combinations(X, 2)
                 if pair not in forced_zero]
    for mask in range(1 << len(available)):
        degrees_x = Counter()
        for index, (x, y) in enumerate(available):
            if mask >> index & 1:
                degrees_x[x] += 1
                degrees_x[y] += 1
        if all(degrees_cross[x] + degrees_x[x] >= 5 for x in X):
            return True
    return False


def normalized_triples(C_size: int):
    C = frozenset(range(C_size))
    possible = range(C_size % 2, min(C_size, 8 - C_size) + 1, 2)
    for first_cut in possible:
        first = representative(C, first_cut)
        for second in MATCHINGS:
            for third in MATCHINGS:
                factors = (first, second, third)
                if distinct_c_neighbours(factors, C):
                    yield C, factors


def audit_c4() -> tuple[int, Counter]:
    checked = 0
    profiles = Counter()
    for C, factors in normalized_triples(4):
        if not boundary_degree_feasible(factors, C):
            continue
        checked += 1
        profiles[tuple(cut_size(matching, C) for matching in factors)] += 1
        fourth = occurrence_matchings(factors)
        require(
            any(occurrence_cut_size(matching, C) in (2, 4)
                       for matching in fourth),
            "any(occurrence_cut_size(matching, C) in (2, 4) for matchi...",
        )
    return checked, profiles


def audit_c3() -> tuple[int, Counter]:
    checked = 0
    profiles = Counter()
    for C, factors in normalized_triples(3):
        if not boundary_degree_feasible(factors, C):
            continue
        checked += 1
        profile = tuple(cut_size(matching, C) for matching in factors)
        profiles[profile] += 1
        require(
            sum(profile) >= 5,
            "sum(profile) >= 5",
        )
        require(
            3 in profile,
            "3 in profile",
        )
        forced_zero = c3_forced_zero_pairs(factors, C)
        require(
            not has_bad_x_graph_avoiding(forced_zero, factors, C),
            "not has_bad_x_graph_avoiding(forced_zero, factors, C)",
        )
    return checked, profiles


def main() -> None:
    checked4, profiles4 = audit_c4()
    checked3, profiles3 = audit_c3()
    print(f"|C|=4: {checked4} normalized degree-feasible triples; "
          f"{len(profiles4)} labelled cut profiles")
    print(f"|C|=3: {checked3} normalized degree-feasible triples; "
          f"{len(profiles3)} labelled cut profiles")
    print("order-eight large-C matching-cut obstruction: PASS")


if __name__ == "__main__":
    main()
