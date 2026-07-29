#!/usr/bin/env python3
"""Exact audit of the matching-hole directed-cycle obstruction.

For two pure hole-matching edges, enumerate the oriented supports between
their four sites.  If both opposite Schur-cap corrections can be nonzero,
the support is one of the two alternating directed 4-cycles.  For each such
cycle this checker expands the paired Pfaffians over Z.  The four three-site
faces kill all four particle cross blocks, after which every four-site
coefficient is a single nonzero product of the four directed star entries.
"""

from __future__ import annotations

import itertools
from collections import Counter


SITES = tuple(range(4))
COLORS = (0, 1)
GROUP_A = (0, 1)
GROUP_B = (2, 3)
CROSS_EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))


# Sparse integer polynomials: monomial (a sorted tuple of variable labels)
# -> coefficient.
def constant(value: int) -> Counter:
    return Counter({(): value}) if value else Counter()


def variable(label: str) -> Counter:
    return Counter({(label,): 1})


def normalize(polynomial: Counter) -> Counter:
    return Counter(
        {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
    )


def add(left: Counter, right: Counter) -> Counter:
    answer = left.copy()
    answer.update(right)
    return normalize(answer)


def scale(value: int, polynomial: Counter) -> Counter:
    return normalize(Counter({monomial: value * coefficient for monomial, coefficient in polynomial.items()}))


def multiply(left: Counter, right: Counter) -> Counter:
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return normalize(answer)


def pfaffian(nodes, entry) -> Counter:
    if not nodes:
        return constant(1)
    first = nodes[0]
    answer = Counter()
    for position in range(1, len(nodes)):
        second = nodes[position]
        rest = nodes[1:position] + nodes[position + 1 :]
        term = multiply(entry(first, second), pfaffian(rest, entry))
        answer = add(answer, scale((-1) ** (position + 1), term))
    return answer


def has_directed_perfect_matching(states, direction: int) -> bool:
    return (
        states[(0, 2)] == direction and states[(1, 3)] == direction
    ) or (
        states[(0, 3)] == direction and states[(1, 2)] == direction
    )


def alternating_supports():
    answer = []
    for values in itertools.product((-1, 0, 1), repeat=4):
        states = dict(zip(CROSS_EDGES, values))
        if has_directed_perfect_matching(states, 1) and has_directed_perfect_matching(
            states, -1
        ):
            answer.append(states)
    return answer


def audit_cycle(states) -> None:
    # State +1 orients A -> B, and state -1 orients B -> A.
    directed = {}
    for (left, right), state in states.items():
        if state == 1:
            directed[left, right] = tuple(
                variable(f"m{left}{right}{color}") for color in COLORS
            )
        elif state == -1:
            directed[right, left] = tuple(
                variable(f"m{right}{left}{color}") for color in COLORS
            )

    q = {
        (left, right, left_color, right_color): variable(
            f"q{left}{right}{left_color}{right_color}"
        )
        for left, right in CROSS_EDGES
        for left_color in COLORS
        for right_color in COLORS
    }

    def entry(first, second) -> Counter:
        if first == second:
            return Counter()
        first_kind, first_site, *first_tail = first
        second_kind, second_site, *second_tail = second

        if first_kind == second_kind == "h":
            if first_site > second_site:
                return scale(-1, entry(second, first))
            return constant(int((first_site, second_site) in ((0, 1), (2, 3))))

        if first_kind == "h" and second_kind == "p":
            vector = directed.get((first_site, second_site))
            return vector[second_tail[0]] if vector is not None else Counter()
        if first_kind == "p" and second_kind == "h":
            return scale(-1, entry(second, first))

        first_color, second_color = first_tail[0], second_tail[0]
        if first_site > second_site:
            return scale(-1, entry(second, first))
        return q.get((first_site, second_site, first_color, second_color), Counter())

    def coefficient(selected_sites, coloring) -> Counter:
        nodes = []
        for site, color in zip(selected_sites, coloring):
            nodes.extend((("h", site), ("p", site, color)))
        return pfaffian(tuple(nodes), entry)

    # Each three-site face contains one hole-matching edge and one singleton.
    # In an alternating cycle its eight equations are q_entry*m_component=0.
    # Check that every entry of every particle cross block occurs multiplied
    # by both components of one nonzero directed star.
    seen = {label: set() for label in (f"q{u}{v}{a}{b}" for u, v in CROSS_EDGES for a in COLORS for b in COLORS)}
    for selected in itertools.combinations(SITES, 3):
        for coloring in itertools.product(COLORS, repeat=3):
            polynomial = coefficient(selected, coloring)
            assert len(polynomial) == 1
            (monomial, coefficient_value), = polynomial.items()
            assert abs(coefficient_value) == 1
            assert len(monomial) == 2
            q_label = next(label for label in monomial if label.startswith("q"))
            m_label = next(label for label in monomial if label.startswith("m"))
            seen[q_label].add(m_label)

    assert all(len(star_components) == 2 for star_components in seen.values())
    assert all(
        component[:-1] == next(iter(star_components))[:-1]
        for star_components in seen.values()
        for component in star_components
    )

    # The three-site equations therefore set every q block to zero.  With q
    # removed, each four-site coefficient is exactly the product of the four
    # directed star coordinates targeting the selected particle colors.
    q_labels = set(seen)
    for coloring in itertools.product(COLORS, repeat=4):
        polynomial = coefficient(SITES, coloring)
        q_free = Counter(
            {
                monomial: coefficient_value
                for monomial, coefficient_value in polynomial.items()
                if not any(label in q_labels for label in monomial)
            }
        )
        assert len(q_free) == 1
        (monomial, coefficient_value), = q_free.items()
        assert abs(coefficient_value) == 1
        assert len(monomial) == 4
        assert all(label.startswith("m") for label in monomial)


def main() -> None:
    supports = alternating_supports()
    assert len(supports) == 2
    for states in supports:
        assert all(state != 0 for state in states.values())
        audit_cycle(states)
    print("enumerated all 3^4 directed cross supports")
    print("both opposite Schur caps can be supported only on 2 alternating cycles")
    print("exact paired-Pfaffian expansion over Z excludes both cycles")


if __name__ == "__main__":
    main()
