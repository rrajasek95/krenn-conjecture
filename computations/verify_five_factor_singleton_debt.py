#!/usr/bin/env python3
"""Audit the exact singleton-debt theorem for five coordinate factors.

For three pure coordinate one-factors P0,P1,P2 and two arbitrarily
coordinate-decorated one-factors S,T, every perfect matching R in the pure
union defines a word c_R.  At that word the full compatible graph is exactly
R together with the compatible S,T edges.  This script checks the theorem,
its two-anchor cofactor double count, the 12-site even-holonomy module, and
an 8-site example where edge cardinality alone misses the cycle obstruction.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Iterator, Sequence


Edge = tuple[int, int]
Matching = frozenset[Edge]
Word = tuple[int, ...]
Decoration = dict[Edge, tuple[int, int]]


def edge(u: int, v: int) -> Edge:
    assert u != v
    return (u, v) if u < v else (v, u)


def factor(order: int, raw_edges: Iterable[tuple[int, int]]) -> Matching:
    result = frozenset(edge(u, v) for u, v in raw_edges)
    assert len(result) == order // 2
    assert Counter(v for uv in result for v in uv) == Counter(range(order))
    return result


def perfect_matchings(vertices: Sequence[int], support: set[Edge]) -> Iterator[Matching]:
    vertices = tuple(vertices)
    if not vertices:
        yield frozenset()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], start=1):
        candidate = edge(first, second)
        if candidate not in support:
            continue
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder, support):
            yield tail | {candidate}


def endpoint_colours(e: Edge, word: Word) -> tuple[int, int]:
    return word[e[0]], word[e[1]]


def pure_word(order: int, pure: Sequence[Matching], mate: Matching) -> Word:
    word = [-1] * order
    for e in mate:
        colour = next(i for i, one_factor in enumerate(pure) if e in one_factor)
        word[e[0]] = colour
        word[e[1]] = colour
    assert all(colour >= 0 for colour in word)
    return tuple(word)


def compatible_extra(word: Word, decorated: Decoration) -> set[Edge]:
    return {
        e
        for e, colours in decorated.items()
        if colours == endpoint_colours(e, word)
    }


def alternating_cycle_exists(mate: Matching, extra: set[Edge]) -> bool:
    """Find a simple cycle alternating extra, mate, extra, mate, ... ."""

    partner: dict[int, int] = {}
    for u, v in mate:
        partner[u] = v
        partner[v] = u

    adjacent: dict[int, list[int]] = {v: [] for v in partner}
    for u, v in extra:
        adjacent[u].append(v)
        adjacent[v].append(u)

    def search(start: int, current: int, used: frozenset[int]) -> bool:
        for across in adjacent[current]:
            if across in used:
                continue
            after_mate = partner[across]
            if after_mate == start:
                return True
            if after_mate in used:
                continue
            if search(start, after_mate, used | {across, after_mate}):
                return True
        return False

    return any(search(start, start, frozenset({start})) for start in partner)


def factor_partner(one_factor: Matching, vertex: int) -> int:
    incident = [other for e in one_factor if vertex in e for other in e if other != vertex]
    assert len(incident) == 1
    return incident[0]


def mixed_cofactor_incidence(
    order: int,
    pure: Sequence[Matching],
    extra_edge: Edge,
    colours: tuple[int, int],
) -> int:
    """Evaluate formula (11), including removal of the one pure matching."""

    u, v = extra_edge
    a, b = colours
    forced_u = edge(u, factor_partner(pure[a], u))
    forced_v = edge(v, factor_partner(pure[b], v))
    # Extra and pure factors are edge-disjoint, so equality cannot occur.
    assert forced_u != forced_v
    if set(forced_u) & set(forced_v):
        return 0
    deleted = set(forced_u) | set(forced_v)
    remaining = tuple(vertex for vertex in range(order) if vertex not in deleted)
    pure_union = set().union(*pure)
    count = sum(1 for _ in perfect_matchings(remaining, pure_union))
    if a == b:
        count -= 1
    assert count >= 0
    return count


def audit_instance(
    order: int,
    pure: Sequence[Matching],
    extras: Sequence[Matching],
    decorated: Decoration,
) -> dict[str, object]:
    all_factors = tuple(pure) + tuple(extras)
    assert len(pure) == 3 and len(extras) == 2
    assert len(set().union(*all_factors)) == 5 * order // 2
    assert set(decorated) == set().union(*extras)

    pure_union = set().union(*pure)
    full_support = set().union(*all_factors)
    pure_matchings = list(perfect_matchings(tuple(range(order)), pure_union))

    words: dict[Word, Matching] = {}
    mixed_records: list[tuple[Matching, Word, set[Edge], list[Matching], bool]] = []
    for mate in pure_matchings:
        word = pure_word(order, pure, mate)
        assert word not in words
        words[word] = mate

        # The compatible pure support is exactly the originating matching.
        compatible_pure = {
            e
            for colour, one_factor in enumerate(pure)
            for e in one_factor
            if endpoint_colours(e, word) == (colour, colour)
        }
        assert compatible_pure == set(mate)

        extra = compatible_extra(word, decorated)
        compatible_full = {
            e
            for e in full_support
            if (
                e in decorated
                and decorated[e] == endpoint_colours(e, word)
            )
            or (
                e not in decorated
                and any(
                    e in one_factor
                    and endpoint_colours(e, word) == (colour, colour)
                    for colour, one_factor in enumerate(pure)
                )
            )
        }
        assert compatible_full == set(mate) | extra

        fibre = list(perfect_matchings(tuple(range(order)), compatible_full))
        assert mate in fibre
        has_cycle = alternating_cycle_exists(mate, extra)
        assert (len(fibre) > 1) == has_cycle
        for other in fibre:
            if other == mate:
                continue
            symmetric = set(mate ^ other)
            assert symmetric & set(mate) <= set(mate)
            assert symmetric - set(mate) <= extra

        if len(set(word)) > 1:
            mixed_records.append((mate, word, extra, fibre, has_cycle))

    # Direct incidences agree edgewise with the two-anchor cofactor formula.
    for e, colours in decorated.items():
        direct = sum(
            1
            for mate, _, extra, _, _ in mixed_records
            if e in extra
        )
        assert direct == mixed_cofactor_incidence(order, pure, e, colours)

    incidence_sum = sum(len(extra) for _, _, extra, _, _ in mixed_records)
    transposed_sum = sum(
        mixed_cofactor_incidence(order, pure, e, colours)
        for e, colours in decorated.items()
    )
    assert incidence_sum == transposed_sum

    singleton_count = sum(len(fibre) == 1 for _, _, _, fibre, _ in mixed_records)
    cycle_bound = sum(not has_cycle for _, _, _, _, has_cycle in mixed_records)
    at_most_one_bound = sum(len(extra) <= 1 for _, _, extra, _, _ in mixed_records)
    crude_bound = max(0, len(mixed_records) - incidence_sum // 2)
    assert singleton_count == cycle_bound
    assert singleton_count >= at_most_one_bound >= crude_bound

    return {
        "pure_matching_count": len(pure_matchings),
        "mixed_count": len(mixed_records),
        "g_histogram": Counter(len(extra) for _, _, extra, _, _ in mixed_records),
        "fibre_histogram": Counter(len(fibre) for _, _, _, fibre, _ in mixed_records),
        "incidence_sum": incidence_sum,
        "cycle_bound": cycle_bound,
        "at_most_one_bound": at_most_one_bound,
        "crude_bound": crude_bound,
        "records": mixed_records,
    }


def twelve_site_module() -> tuple[int, tuple[Matching, ...], tuple[Matching, ...], Decoration]:
    order = 12
    p = factor(order, [(1, 4), (2, 5), (0, 6), (3, 7), (8, 9), (10, 11)])
    w = factor(order, [(4, 2), (5, 1), (6, 3), (7, 0), (9, 10), (11, 8)])
    q = factor(order, [(0, 2), (1, 3), (4, 8), (5, 9), (6, 10), (7, 11)])
    p0 = factor(order, [(0, 4), (1, 6), (2, 8), (3, 10), (5, 7), (9, 11)])
    p2 = factor(order, [(0, 1), (2, 3), (4, 5), (6, 11), (7, 9), (8, 10)])
    c_word = (0, 0, 0, 0) + (1,) * 8
    decorated = {e: endpoint_colours(e, c_word) for e in w}
    decorated.update({e: (1, 1) for e in q})
    return order, (p0, p, p2), (w, q), decorated


def cyclic_factor(order: int, index: int) -> Matching:
    """Round-robin one-factorization with vertex order-1 at infinity."""

    modulus = order - 1
    raw = [(order - 1, index)]
    raw.extend(
        ((index - delta) % modulus, (index + delta) % modulus)
        for delta in range(1, (modulus + 1) // 2)
    )
    return factor(order, raw)


def eight_site_port_example() -> tuple[int, tuple[Matching, ...], tuple[Matching, ...], Decoration]:
    order = 8
    factors = tuple(cyclic_factor(order, index) for index in range(5))
    word_s = (2, 1, 0, 1, 2, 2, 1, 0)
    word_t = (0, 1, 0, 1, 0, 1, 1, 1)
    decorated = {e: endpoint_colours(e, word_s) for e in factors[3]}
    decorated.update({e: endpoint_colours(e, word_t) for e in factors[4]})
    return order, factors[:3], factors[3:], decorated


def main() -> None:
    stats12 = audit_instance(*twelve_site_module())
    assert stats12["pure_matching_count"] == 12
    assert stats12["mixed_count"] == 9
    assert stats12["g_histogram"] == Counter({2: 4, 0: 3, 6: 1, 4: 1})
    assert stats12["fibre_histogram"] == Counter({1: 6, 2: 3})
    assert stats12["incidence_sum"] == 18
    assert stats12["cycle_bound"] == 6
    assert stats12["at_most_one_bound"] == 3
    assert stats12["crude_bound"] == 0

    records12 = stats12["records"]
    threshold_word = (0, 0, 2, 2, 0, 0, 0, 0, 1, 1, 1, 1)
    threshold = next(record for record in records12 if record[1] == threshold_word)
    assert len(threshold[2]) == 2 and len(threshold[3]) == 2

    stats8 = audit_instance(*eight_site_port_example())
    assert stats8["pure_matching_count"] == 5
    assert stats8["mixed_count"] == 2
    assert stats8["g_histogram"] == Counter({2: 1, 3: 1})
    assert stats8["fibre_histogram"] == Counter({1: 2})
    assert stats8["cycle_bound"] == 2
    assert stats8["at_most_one_bound"] == 0

    print("PASS five-coordinate-factor singleton debt")
    print("exact fibre formula and two-anchor cofactor double count verified")
    print("n=12: 9 pure-core mixed words, g-sum 18, singleton bounds 0 < 3 < 6")
    print("n=8: g-values 2 and 3 but both fibres singleton (port-cycle obstruction)")


if __name__ == "__main__":
    main()
