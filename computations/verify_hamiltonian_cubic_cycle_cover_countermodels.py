#!/usr/bin/env python3
"""Verify exact countermodels to the pure-core alternating-cycle cover claim.

The main examples have a connected cubic pure union U=P0+P1+P2 in which
every pair of factors is Hamiltonian.  Every mixed perfect matching of U has
an exact, canceling binomial fibre supplied by two extra coordinate factors.
The script also exhausts colored cubic cores and underlying extra-factor
pairs at orders six and eight.  Its finite CSP uses only deterministic
backtracking; no SAT package or floating-point computation is involved.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Iterator, Sequence
from itertools import combinations, product


Edge = tuple[int, int]
Matching = frozenset[Edge]
Word = tuple[int, ...]
Variable = tuple[int, int]  # (extra-factor index, vertex)


def edge(u: int, v: int) -> Edge:
    assert u != v
    return (u, v) if u < v else (v, u)


def factor(order: int, raw_edges: Iterable[tuple[int, int]]) -> Matching:
    result = frozenset(edge(u, v) for u, v in raw_edges)
    assert len(result) == order // 2
    assert Counter(vertex for e in result for vertex in e) == Counter(range(order))
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


def is_connected(order: int, support: set[Edge]) -> bool:
    adjacent = {vertex: [] for vertex in range(order)}
    for u, v in support:
        adjacent[u].append(v)
        adjacent[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        for neighbor in adjacent[stack.pop()]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == order


def pair_is_hamiltonian(order: int, first: Matching, second: Matching) -> bool:
    assert not first & second
    return is_connected(order, set(first | second))


def pure_word(order: int, pure: Sequence[Matching], mate: Matching) -> Word:
    answer = [-1] * order
    for e in mate:
        colour = next(index for index, one_factor in enumerate(pure) if e in one_factor)
        answer[e[0]] = colour
        answer[e[1]] = colour
    assert all(colour >= 0 for colour in answer)
    return tuple(answer)


def difference_components(difference: set[Edge]) -> tuple[frozenset[Edge], ...]:
    remaining = set(difference)
    components: list[frozenset[Edge]] = []
    while remaining:
        start = next(iter(remaining))[0]
        vertices = {start}
        stack = [start]
        component: set[Edge] = set()
        while stack:
            current = stack.pop()
            for e in tuple(remaining):
                if current not in e:
                    continue
                remaining.remove(e)
                component.add(e)
                other = e[0] if e[1] == current else e[1]
                if other not in vertices:
                    vertices.add(other)
                    stack.append(other)
        components.append(frozenset(component))
    return tuple(components)


def alternating_cycles(
    order: int, mate: Matching, first_extra: Matching, second_extra: Matching
) -> tuple[frozenset[Edge], ...]:
    """Return each possible alternating cycle by its external edge set."""

    support = set(mate | first_extra | second_extra)
    cycles: set[frozenset[Edge]] = set()
    for other in perfect_matchings(tuple(range(order)), support):
        if other == mate:
            continue
        for component in difference_components(set(mate ^ other)):
            external = frozenset(component - mate)
            assert len(external) >= 2
            cycles.add(external)
    return tuple(sorted(cycles, key=lambda cycle: tuple(sorted(cycle))))


def cycle_requirements(
    cycle: frozenset[Edge],
    word: Word,
    factor_of_edge: dict[Edge, int],
) -> dict[Variable, int]:
    requirements: dict[Variable, int] = {}
    for e in cycle:
        factor_index = factor_of_edge[e]
        for vertex in e:
            variable = (factor_index, vertex)
            required = word[vertex]
            assert variable not in requirements or requirements[variable] == required
            requirements[variable] = required
    return requirements


def parity_solution(
    selected_cycles: Sequence[frozenset[Edge]], external_edges: Sequence[Edge]
) -> frozenset[Edge] | None:
    """Solve product(cycle-edge signs)=-1 for all selected cycles over GF(2)."""

    edge_index = {e: index for index, e in enumerate(external_edges)}
    width = len(external_edges)
    basis: dict[int, tuple[int, int]] = {}
    for cycle in selected_cycles:
        mask = sum(1 << edge_index[e] for e in cycle)
        right = 1
        while mask:
            pivot = (mask & -mask).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, right)
                break
            other_mask, other_right = basis[pivot]
            mask ^= other_mask
            right ^= other_right
        if mask == 0 and right:
            return None

    values = [0] * width
    for pivot in sorted(basis, reverse=True):
        mask, right = basis[pivot]
        known = sum(values[index] for index in range(pivot + 1, width) if mask >> index & 1)
        values[pivot] = right ^ (known & 1)
    return frozenset(e for e, value in zip(external_edges, values, strict=True) if value)


def solve_label_constraints(
    variables: Sequence[Variable],
    forced: dict[Variable, int],
    inequalities: Sequence[tuple[Variable, Variable]],
    forbidden_patterns: Sequence[dict[Variable, int]],
) -> dict[Variable, int] | None:
    """Solve a three-valued CSP by propagation and deterministic branching."""

    initial = {variable: {0, 1, 2} for variable in variables}
    for variable, value in forced.items():
        initial[variable] = {value}

    def propagate(domains: dict[Variable, set[int]]) -> bool:
        changed = True
        while changed:
            changed = False
            if any(not domain for domain in domains.values()):
                return False
            for left, right in inequalities:
                if len(domains[left]) == 1:
                    value = next(iter(domains[left]))
                    if value in domains[right]:
                        if len(domains[right]) == 1:
                            return False
                        domains[right].remove(value)
                        changed = True
                if len(domains[right]) == 1:
                    value = next(iter(domains[right]))
                    if value in domains[left]:
                        if len(domains[left]) == 1:
                            return False
                        domains[left].remove(value)
                        changed = True

            for pattern in forbidden_patterns:
                # A pattern is already false if one required value is absent.
                if any(value not in domains[variable] for variable, value in pattern.items()):
                    continue
                undecided = [
                    variable
                    for variable, value in pattern.items()
                    if domains[variable] != {value}
                ]
                if not undecided:
                    return False
                if len(undecided) == 1:
                    variable = undecided[0]
                    value = pattern[variable]
                    domains[variable].remove(value)
                    changed = True
        return True

    def search(domains: dict[Variable, set[int]]) -> dict[Variable, int] | None:
        if not propagate(domains):
            return None
        unresolved = [variable for variable in variables if len(domains[variable]) > 1]
        if not unresolved:
            return {variable: next(iter(domains[variable])) for variable in variables}
        variable = min(unresolved, key=lambda item: (len(domains[item]), item))
        for value in sorted(domains[variable]):
            branch = {item: set(domain) for item, domain in domains.items()}
            branch[variable] = {value}
            answer = search(branch)
            if answer is not None:
                return answer
        return None

    return search(initial)


def find_strong_cover(
    order: int,
    pure: Sequence[Matching],
    extras: Sequence[Matching],
    require_phase: bool,
) -> tuple[tuple[Word, Word], tuple[frozenset[Edge], ...], frozenset[Edge]] | None:
    """Find pure-separated labels with exactly one cycle per mixed core word."""

    pure_union = set().union(*pure)
    mixed = sorted(
        (
            (pure_word(order, pure, mate), mate)
            for mate in perfect_matchings(tuple(range(order)), pure_union)
            if len(set(pure_word(order, pure, mate))) > 1
        ),
        key=lambda item: item[0],
    )
    factor_of_edge = {e: index for index, one_factor in enumerate(extras) for e in one_factor}
    options = [
        alternating_cycles(order, mate, extras[0], extras[1])
        for _, mate in mixed
    ]
    if any(not cycles for cycles in options):
        return None

    variables = tuple((index, vertex) for index in range(2) for vertex in range(order))
    inequalities = tuple(
        ((index, e[0]), (index, e[1]))
        for index, one_factor in enumerate(extras)
        for e in one_factor
    )
    external_edges = tuple(sorted(set().union(*extras)))

    for selected in product(*options):
        negative = parity_solution(selected, external_edges)
        if require_phase and negative is None:
            continue

        forced: dict[Variable, int] = {}
        conflict = False
        forbidden: list[dict[Variable, int]] = []
        for (word, _), cycles, chosen in zip(mixed, options, selected, strict=True):
            chosen_requirements = cycle_requirements(chosen, word, factor_of_edge)
            for variable, value in chosen_requirements.items():
                if variable in forced and forced[variable] != value:
                    conflict = True
                    break
                forced[variable] = value
            if conflict:
                break
            forbidden.extend(
                cycle_requirements(cycle, word, factor_of_edge)
                for cycle in cycles
                if cycle != chosen
            )
        if conflict:
            continue

        labels = solve_label_constraints(variables, forced, inequalities, forbidden)
        if labels is None:
            continue
        words = tuple(
            tuple(labels[index, vertex] for vertex in range(order))
            for index in range(2)
        )
        return (words[0], words[1]), tuple(selected), negative or frozenset()
    return None


def canonical_third_factor(order: int, one_factor: Matching) -> tuple[Edge, ...]:
    forms = []
    for sign in (1, -1):
        for shift in range(order):
            forms.append(
                tuple(
                    sorted(
                        edge((sign * u + shift) % order, (sign * v + shift) % order)
                        for u, v in one_factor
                    )
                )
            )
    return min(forms)


def colored_core_representatives(order: int) -> tuple[tuple[Matching, Matching, Matching], ...]:
    all_edges = set(combinations(range(order), 2))
    p0 = factor(order, ((vertex, vertex + 1) for vertex in range(0, order, 2)))
    p1 = factor(
        order,
        list((vertex, vertex + 1) for vertex in range(1, order - 1, 2))
        + [(order - 1, 0)],
    )
    representatives = {
        canonical_third_factor(order, p2)
        for p2 in perfect_matchings(tuple(range(order)), all_edges - set(p0 | p1))
        if pair_is_hamiltonian(order, p0, p2)
        and pair_is_hamiltonian(order, p1, p2)
    }
    return tuple((p0, p1, frozenset(raw)) for raw in sorted(representatives))


def extra_factor_pairs(order: int, pure: Sequence[Matching]):
    available = set(combinations(range(order), 2)) - set().union(*pure)
    pairs = []
    for first in perfect_matchings(tuple(range(order)), available):
        for second in perfect_matchings(tuple(range(order)), available - set(first)):
            if tuple(sorted(first)) < tuple(sorted(second)):
                pairs.append((first, second))
    return tuple(pairs)


def classify_small_orders() -> None:
    expected = {
        6: ((1, 1, 1, 1), (3, 0, 0, 0)),
        8: ((2, 39, 39, 39), (3, 36, 6, 6), (2, 39, 39, 39)),
    }
    for order in (6, 8):
        rows = []
        for pure in colored_core_representatives(order):
            pure_union = set().union(*pure)
            mixed_count = (
                sum(1 for _ in perfect_matchings(tuple(range(order)), pure_union)) - 3
            )
            extra_pairs = extra_factor_pairs(order, pure)
            cover_count = sum(
                find_strong_cover(order, pure, extras, require_phase=False) is not None
                for extras in extra_pairs
            )
            phase_count = sum(
                find_strong_cover(order, pure, extras, require_phase=True) is not None
                for extras in extra_pairs
            )
            rows.append((mixed_count, len(extra_pairs), cover_count, phase_count))
        assert tuple(rows) == expected[order]


def source_fibres(
    order: int,
    pure: Sequence[Matching],
    extras: Sequence[Matching],
    extra_words: Sequence[Word],
    negative_edges: set[Edge],
):
    cells: dict[Edge, tuple[int, int, int]] = {}
    for colour, one_factor in enumerate(pure):
        for e in one_factor:
            cells[e] = (colour, colour, 1)
    for one_factor, word in zip(extras, extra_words, strict=True):
        for e in one_factor:
            cells[e] = (word[e[0]], word[e[1]], -1 if e in negative_edges else 1)

    fibres: dict[Word, list[tuple[Matching, int]]] = defaultdict(list)
    for mate in perfect_matchings(tuple(range(order)), set(cells)):
        word = [-1] * order
        weight = 1
        for e in mate:
            word[e[0]], word[e[1]] = cells[e][:2]
            weight *= cells[e][2]
        fibres[tuple(word)].append((mate, weight))
    return fibres


def audit_six_site_minimal_module() -> None:
    order = 6
    pure = (
        factor(order, [(0, 1), (2, 3), (4, 5)]),
        factor(order, [(1, 2), (3, 4), (0, 5)]),
        factor(order, [(0, 2), (1, 4), (3, 5)]),
    )
    extras = (
        factor(order, [(0, 3), (1, 5), (2, 4)]),
        factor(order, [(0, 4), (1, 3), (2, 5)]),
    )
    extra_words = ((0, 0, 0, 1, 2, 2), (0, 2, 1, 0, 1, 0))
    fibres = source_fibres(order, pure, extras, extra_words, {edge(2, 4)})

    assert all(pair_is_hamiltonian(order, *pair) for pair in combinations(pure, 2))
    assert [len(fibres[(colour,) * order]) for colour in range(3)] == [1, 1, 1]
    assert [sum(weight for _, weight in fibres[(colour,) * order]) for colour in range(3)] == [1, 1, 1]
    mixed_histogram = Counter(
        len(fibre) for word, fibre in fibres.items() if len(set(word)) > 1
    )
    assert mixed_histogram == Counter({1: 10, 2: 1})
    core_mixed_word = (1, 2, 0, 0, 2, 1)
    assert sorted(weight for _, weight in fibres[core_mixed_word]) == [-1, 1]


def audit_eight_site_module() -> None:
    order = 8
    pure = (
        factor(order, [(0, 1), (2, 3), (4, 5), (6, 7)]),
        factor(order, [(1, 2), (3, 4), (5, 6), (0, 7)]),
        factor(order, [(0, 2), (1, 4), (3, 6), (5, 7)]),
    )
    extras = (
        factor(order, [(0, 3), (1, 5), (2, 6), (4, 7)]),
        factor(order, [(0, 4), (1, 6), (2, 5), (3, 7)]),
    )
    word_s = (1, 2, 0, 0, 2, 1, 1, 1)
    word_t = (1, 1, 1, 2, 0, 0, 2, 1)
    fibres = source_fibres(
        order, pure, extras, (word_s, word_t), {edge(0, 3), edge(0, 4)}
    )

    assert all(pair_is_hamiltonian(order, *pair) for pair in combinations(pure, 2))
    pure_core = list(perfect_matchings(tuple(range(order)), set().union(*pure)))
    mixed_core = [
        mate for mate in pure_core if len(set(pure_word(order, pure, mate))) > 1
    ]
    assert len(pure_core) == 5 and len(mixed_core) == 2
    assert {pure_word(order, pure, mate) for mate in mixed_core} == {word_s, word_t}

    # Every external edge is bichromatic, so no external edge enters a pure fibre.
    for one_factor, word in zip(extras, (word_s, word_t), strict=True):
        assert all(word[e[0]] != word[e[1]] for e in one_factor)
    assert all(len(fibres[(colour,) * order]) == 1 for colour in range(3))
    assert all(
        sum(weight for _, weight in fibres[(colour,) * order]) == 1
        for colour in range(3)
    )

    # Cross compatibility is empty.  Each originating matching plus its whole
    # assigned extra factor is one Hamilton cycle and hence an exact binomial.
    for mate in mixed_core:
        word = pure_word(order, pure, mate)
        assigned = extras[0] if word == word_s else extras[1]
        other = extras[1] if word == word_s else extras[0]
        assert pair_is_hamiltonian(order, mate, assigned)
        assert all(
            (word[e[0]], word[e[1]])
            != ((word_t if word == word_s else word_s)[e[0]],
                (word_t if word == word_s else word_s)[e[1]])
            for e in other
        )
        assert {entry[0] for entry in fibres[word]} == {mate, assigned}
        assert sorted(weight for _, weight in fibres[word]) == [-1, 1]

    mixed_histogram = Counter(
        len(fibre) for word, fibre in fibres.items() if len(set(word)) > 1
    )
    assert mixed_histogram == Counter({1: 24, 2: 2})

    # The two Laurent rows are independent: each has private external support.
    first_row_external = set(extras[0])
    second_row_external = set(extras[1])
    assert first_row_external and second_row_external
    assert not first_row_external & second_row_external


def main() -> None:
    classify_small_orders()
    audit_six_site_minimal_module()
    audit_eight_site_module()
    print("PASS Hamiltonian cubic cycle-cover countermodels")
    print("n=6 colored cores: (mixed, extras, strong, phased)=(1,1,1,1),(3,0,0,0)")
    print("n=8 colored cores: (2,39,39,39),(3,36,6,6),(2,39,39,39)")
    print("explicit n=8 module: pure=(1,1,1), mixed histogram={1:24,2:2}")
    print("both canonical binomials cancel and their Laurent rows are independent")


if __name__ == "__main__":
    main()
