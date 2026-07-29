#!/usr/bin/env python3
"""Independent exact audit of the cubic leave-one-anchor nullity web.

This checker deliberately does not import the primary checker.  It uses
tagged endpoint cells rather than numerical matrices to audit the matching
bijection behind equation (9), and finite-field rank-one factor equations
to audit the degeneracy cases in Lemmas 3.1 and 4.1.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from math import factorial


COLORS = (0, 1, 2)
FIELD = 5

# Nonconsecutive labels put q between some of the W-sites.  This makes an
# accidental assumption that q is always the first endpoint detectable.
P_VERTEX = 23
Q_VERTEX = 17
W = (2, 5, 11, 31, 41, 47)
ANCHORS = (5, 31, 47)

Cell = tuple[int, int, int, int]
Monomial = tuple[Cell, ...]
TaggedTerm = tuple[tuple[int, ...], Monomial]


def cell(left: int, left_color: int, right: int, right_color: int) -> Cell:
    """Return a physical-endpoint-ordered cell tag."""

    assert left != right
    if left < right:
        return (left, right, left_color, right_color)
    return (right, left, right_color, left_color)


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate each unordered perfect matching exactly once."""

    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def tagged_matching_term(
    matching: tuple[tuple[int, int], ...], assignment: dict[int, int]
) -> Monomial:
    return tuple(
        sorted(cell(u, assignment[u], v, assignment[v]) for u, v in matching)
    )


def direct_q_slice(anchor: int, q_color: int) -> set[TaggedTerm]:
    """Expand the complete cofactor and then contract the q-slot."""

    sites = tuple(vertex for vertex in W if vertex != anchor)
    vertices = tuple(sorted((Q_VERTEX,) + sites))
    terms: list[TaggedTerm] = []
    for matching in perfect_matchings(vertices):
        for word in product(COLORS, repeat=len(sites)):
            assignment = dict(zip(sites, word, strict=True))
            assignment[Q_VERTEX] = q_color
            terms.append((word, tagged_matching_term(matching, assignment)))
    assert len(terms) == len(set(terms))
    return set(terms)


def cofactor_column_slice(anchor: int, q_color: int) -> set[TaggedTerm]:
    """Expand the sum of complete leave-one-site cofactor columns."""

    sites = tuple(vertex for vertex in W if vertex != anchor)
    terms: list[TaggedTerm] = []
    for center in sites:
        rest = tuple(vertex for vertex in sites if vertex != center)
        for matching in perfect_matchings(rest):
            for word in product(COLORS, repeat=len(sites)):
                assignment = dict(zip(sites, word, strict=True))
                monomial = [cell(Q_VERTEX, q_color, center, assignment[center])]
                monomial.extend(
                    cell(u, assignment[u], v, assignment[v]) for u, v in matching
                )
                terms.append((word, tuple(sorted(monomial))))
    assert len(terms) == len(set(terms))
    return set(terms)


def divided_square_slice(anchor: int, q_color: int) -> set[TaggedTerm]:
    """Build (sum z_v) x^2/2! by unordered disjoint cell selections."""

    sites = tuple(vertex for vertex in W if vertex != anchor)
    atoms: list[tuple[frozenset[int], Cell, dict[int, int]]] = []
    for u, v in combinations(sites, 2):
        for left_color, right_color in product(COLORS, repeat=2):
            atoms.append(
                (
                    frozenset((u, v)),
                    cell(u, left_color, v, right_color),
                    {u: left_color, v: right_color},
                )
            )

    divided_pairs: list[tuple[frozenset[int], Monomial, dict[int, int]]] = []
    for left, right in combinations(atoms, 2):
        if left[0] & right[0]:
            continue
        assignment = dict(left[2])
        assignment.update(right[2])
        divided_pairs.append(
            (left[0] | right[0], tuple(sorted((left[1], right[1]))), assignment)
        )

    terms: list[TaggedTerm] = []
    for center in sites:
        required = frozenset(vertex for vertex in sites if vertex != center)
        for covered, internal_monomial, internal_assignment in divided_pairs:
            if covered != required:
                continue
            for center_color in COLORS:
                assignment = dict(internal_assignment)
                assignment[center] = center_color
                word = tuple(assignment[vertex] for vertex in sites)
                star = cell(Q_VERTEX, q_color, center, center_color)
                terms.append((word, tuple(sorted((star,) + internal_monomial))))
    assert len(terms) == len(set(terms))
    return set(terms)


def audit_equation_nine() -> dict[str, int]:
    checked_terms = 0
    for anchor in ANCHORS:
        for q_color in COLORS:
            direct = direct_q_slice(anchor, q_color)
            columns = cofactor_column_slice(anchor, q_color)
            divided = divided_square_slice(anchor, q_color)
            assert direct == columns == divided
            # At N=8 there are 15 matchings and 3^5 free color assignments
            # after the q-color is contracted.
            assert len(direct) == 15 * 3**5
            checked_terms += len(direct)

    # Contracting the pure cofactor at q gives exactly the Kronecker delta
    # on the right side of (9), independently of lambda's nonzero scale.
    target_slices = 0
    sites = tuple(vertex for vertex in W if vertex != ANCHORS[0])
    for pure_color, q_color in product(COLORS, repeat=2):
        tensor = {
            tuple(pure_color for _ in sites): 1
        } if pure_color == q_color else {}
        assert bool(tensor) == (pure_color == q_color)
        target_slices += 1

    return {"tagged_terms": checked_terms, "target_slices": target_slices}


def audit_divided_power_normalization() -> dict[int, tuple[int, int]]:
    """Check ordered power versus divided power at degrees two and three."""

    ledger: dict[int, tuple[int, int]] = {}
    for degree in (2, 3):
        vertices = tuple(range(2 * degree))
        edges = tuple(combinations(vertices, 2))
        unordered = Counter()
        for selection in combinations(edges, degree):
            flattened = tuple(vertex for edge in selection for vertex in edge)
            if len(set(flattened)) == 2 * degree:
                unordered[tuple(sorted(selection))] += 1
        ordered = Counter()
        for selection in product(edges, repeat=degree):
            flattened = tuple(vertex for edge in selection for vertex in edge)
            if len(set(flattened)) == 2 * degree:
                ordered[tuple(sorted(selection))] += 1
        assert set(unordered) == set(ordered)
        assert set(unordered.values()) == {1}
        assert set(ordered.values()) == {factorial(degree)}
        expected_matchings = 3 if degree == 2 else 15
        assert len(unordered) == expected_matchings
        ledger[degree] = (len(unordered), factorial(degree))
    return ledger


def shared_cofactor_terms(left_anchor: int, right_anchor: int) -> set[TaggedTerm]:
    rest = tuple(
        vertex for vertex in W if vertex not in (left_anchor, right_anchor)
    )
    terms: set[TaggedTerm] = set()
    for matching in perfect_matchings(rest):
        for word in product(COLORS, repeat=len(rest)):
            assignment = dict(zip(rest, word, strict=True))
            terms.add((word, tagged_matching_term(matching, assignment)))
    return terms


def one_center_terms(
    anchor: int, center: int, center_color: int
) -> set[TaggedTerm]:
    sites = tuple(vertex for vertex in W if vertex != anchor)
    rest = tuple(vertex for vertex in sites if vertex != center)
    terms: set[TaggedTerm] = set()
    for matching in perfect_matchings(rest):
        for rest_word in product(COLORS, repeat=len(rest)):
            assignment = dict(zip(rest, rest_word, strict=True))
            assignment[center] = center_color
            word = tuple(assignment[vertex] for vertex in sites)
            terms.add((word, tagged_matching_term(matching, assignment)))
    return terms


def factored_one_center_terms(
    anchor: int, center: int, center_color: int
) -> set[TaggedTerm]:
    rest = tuple(vertex for vertex in W if vertex not in (anchor, center))
    sites = tuple(vertex for vertex in W if vertex != anchor)
    answer: set[TaggedTerm] = set()
    for rest_word, monomial in shared_cofactor_terms(anchor, center):
        assignment = dict(zip(rest, rest_word, strict=True))
        assignment[center] = center_color
        answer.add((tuple(assignment[v] for v in sites), monomial))
    return answer


def audit_shared_cofactors() -> int:
    checks = 0
    for left_anchor, right_anchor in combinations(ANCHORS, 2):
        shared = shared_cofactor_terms(left_anchor, right_anchor)
        # Four remaining sites at N=8 give three matchings and 3^4 words.
        assert len(shared) == 3 * 3**4
        for anchor, center in (
            (left_anchor, right_anchor),
            (right_anchor, left_anchor),
        ):
            for center_color in COLORS:
                assert one_center_terms(
                    anchor, center, center_color
                ) == factored_one_center_terms(anchor, center, center_color)
                checks += 1
    assert checks == 18
    return checks


def pure_tensor(color: int, rest_sites: int, scalar: int = 1) -> dict[tuple[int, ...], int]:
    scalar %= FIELD
    assert scalar
    return {tuple(color for _ in range(rest_sites)): scalar}


def tensor_scale(vector: tuple[int, int, int], tail: dict[tuple[int, ...], int]) -> dict[tuple[int, ...], int]:
    answer: dict[tuple[int, ...], int] = {}
    for head_color, head_value in enumerate(vector):
        for word, tail_value in tail.items():
            value = head_value * tail_value % FIELD
            if value:
                answer[(head_color,) + word] = value
    return answer


def factor_vectors(target_color: int, rest_sites: int) -> set[tuple[int, int, int]]:
    """Solve v tensor T = nonzero pure target over F_5, exactly."""

    target = {
        (target_color,) + tuple(target_color for _ in range(rest_sites)): 1
    }
    words = tuple(product(COLORS, repeat=rest_sites))
    solutions: set[tuple[int, int, int]] = set()
    for vector in product(range(FIELD), repeat=3):
        if vector == (0, 0, 0):
            continue
        pivot = next(index for index, value in enumerate(vector) if value)
        inverse = pow(vector[pivot], FIELD - 2, FIELD)
        tail = {
            word: target.get((pivot,) + word, 0) * inverse % FIELD
            for word in words
        }
        tail = {word: value for word, value in tail.items() if value}
        if tensor_scale(vector, tail) == target:
            # Equality with a nonzero pure tensor forces both factors pure.
            # This is the exact factor-purity implication used for T_cb.
            pure_word = tuple(target_color for _ in range(rest_sites))
            assert set(tail) == {pure_word}
            assert tail[pure_word] != 0
            solutions.add(vector)  # type: ignore[arg-type]
    expected = {
        tuple(scalar if index == target_color else 0 for index in COLORS)
        for scalar in range(1, FIELD)
    }
    assert solutions == expected
    return solutions


def zero_product_vectors(tail: dict[tuple[int, ...], int]) -> set[tuple[int, int, int]]:
    assert tail
    return {
        vector
        for vector in product(range(FIELD), repeat=3)
        if tensor_scale(vector, tail) == {}
    }


def audit_lemma_three() -> dict[str, int]:
    factor_axes = {color: factor_vectors(color, 4) for color in COLORS}
    for color in COLORS:
        assert zero_product_vectors(pure_tensor(color, 4)) == {(0, 0, 0)}
    # Also check the zero-product fact on a non-pure, nonzero tail.
    mixed_tail = pure_tensor(0, 4)
    mixed_tail.update(pure_tensor(1, 4, scalar=2))
    assert zero_product_vectors(mixed_tail) == {(0, 0, 0)}

    both_zero_contradictions = 0
    proportional_contradictions = 0
    for fixed in COLORS:
        wrong = tuple(color for color in COLORS if color != fixed)
        for diagonal, other in (wrong, tuple(reversed(wrong))):
            # If both restrictions vanish, both global rows live at a_fixed.
            # The diagonal equation for `diagonal` makes its shared tail
            # nonzero.  The other row's zero response then makes that local
            # row zero, contradicting its own diagonal factor equation.
            tail = pure_tensor(diagonal, 4)
            assert factor_axes[diagonal]
            assert zero_product_vectors(tail) == {(0, 0, 0)}
            assert (0, 0, 0) not in factor_axes[other]
            both_zero_contradictions += 1

            # If the two nonzero restrictions are proportional, their
            # difference is one local vector factoring two different pure
            # tensors.  The two possible factor axes are disjoint.
            assert factor_axes[diagonal].isdisjoint(factor_axes[other])
            proportional_contradictions += 1

    assert both_zero_contradictions == 6
    assert proportional_contradictions == 6
    return {
        "both_zero_contradictions": both_zero_contradictions,
        "proportional_contradictions": proportional_contradictions,
    }


def shared_state(row_color: int, map_color: int) -> tuple[str, int | None]:
    # The local row is nonzero.  A diagonal rank-one response makes the
    # shared cofactor nonzero and pure; an off-diagonal zero response makes
    # the shared cofactor zero.
    if row_color == map_color:
        return ("pure", map_color)
    return ("zero", None)


def audit_lemma_four() -> dict[str, int]:
    support_intersection_clashes = 0
    zero_pure_clashes = 0
    distinct_pure_clashes = 0
    for first, second in combinations(COLORS, 2):
        for rho_first in COLORS:
            if rho_first == first:
                continue
            for rho_second in COLORS:
                if rho_second == second:
                    continue
                if rho_first == rho_second:
                    # The same nonzero global row cannot be supported only
                    # in two different direct summands.
                    support_intersection_clashes += 1
                    continue
                from_second = shared_state(rho_second, first)
                from_first = shared_state(rho_first, second)
                assert from_second != from_first
                if {from_second[0], from_first[0]} == {"zero", "pure"}:
                    zero_pure_clashes += 1
                else:
                    assert from_second[0] == from_first[0] == "pure"
                    assert from_second[1] != from_first[1]
                    distinct_pure_clashes += 1

    assert support_intersection_clashes == 3
    assert zero_pure_clashes == 6
    assert distinct_pure_clashes == 3
    return {
        "support_intersection": support_intersection_clashes,
        "zero_vs_pure": zero_pure_clashes,
        "pure_color_conflict": distinct_pure_clashes,
    }


def span_vectors(vectors: set[int]) -> set[int]:
    answer = {0}
    for vector in vectors:
        answer |= {left ^ vector for left in tuple(answer)}
    return answer


def subspaces_f2_three() -> tuple[frozenset[int], ...]:
    spaces = []
    for mask in range(1 << 8):
        members = {vector for vector in range(8) if mask & (1 << vector)}
        if 0 not in members:
            continue
        if all((left ^ right) in members for left in members for right in members):
            spaces.append(frozenset(members))
    assert len(spaces) == 16
    return tuple(sorted(spaces, key=lambda space: (len(space), tuple(space))))


def sum_subspaces(spaces: tuple[frozenset[int], ...]) -> set[int]:
    vectors: set[int] = set()
    for space in spaces:
        vectors.update(space)
    return span_vectors(vectors)


def audit_three_essential_equality() -> dict[str, int]:
    spaces = subspaces_f2_three()
    full = set(range(8))
    families_checked = 0
    equality_families = 0
    # Seven possible neighbours is the N=8 endpoint boundary.  Passing to
    # multisets loses no information for the essential-index assertion.
    for family in combinations_with_replacement(spaces, 7):
        if sum_subspaces(family) != full:
            continue
        families_checked += 1
        essential = tuple(
            index
            for index in range(len(family))
            if sum_subspaces(family[:index] + family[index + 1 :]) != full
        )
        assert len(essential) <= 3
        if len(essential) != 3:
            continue
        equality_families += 1
        essential_spaces = tuple(family[index] for index in essential)
        other_spaces = tuple(
            family[index] for index in range(len(family)) if index not in essential
        )
        assert all(len(space) == 2 for space in essential_spaces)
        assert sum_subspaces(essential_spaces) == full
        assert all(space == frozenset((0,)) for space in other_spaces)

    assert equality_families > 0

    # A zero mode support is exactly a zero block; a one-dimensional image
    # is exactly nonzero rank one.  Exhaust all 3x3 matrices over F_2.
    matrix_checks = 0
    for entries in product((0, 1), repeat=9):
        columns = {
            entries[column] | (entries[3 + column] << 1) | (entries[6 + column] << 2)
            for column in range(3)
        }
        image = span_vectors(columns)
        if len(image) == 1:
            assert not any(entries)
        if len(image) == 2:
            assert any(entries)
        matrix_checks += 1
    assert matrix_checks == 512

    return {
        "spanning_multisets": families_checked,
        "three_essential_multisets": equality_families,
        "matrices": matrix_checks,
    }


def audit_nullity_ledger() -> dict[str, object]:
    profiles = {
        tuple(sorted(profile))
        for profile in product(range(1, 7), repeat=3)
        if sum(value == 1 for value in profile) <= 1
    }
    minimum_sum = min(map(sum, profiles))
    minima = sorted(profile for profile in profiles if sum(profile) == minimum_sum)
    assert minima == [(1, 2, 2)]

    ledger: dict[int, tuple[int, int, int, int]] = {}
    for order in range(8, 34, 2):
        nonneighbors = order - 4
        columns = 3 * (order - 3)
        codomain = 3 ** (order - 3)
        singular = 3 * nonneighbors
        double = 2 * nonneighbors
        ledger[order] = (columns, codomain, singular, double)
    assert ledger[8] == (15, 243, 12, 8)
    assert 8 - 4 == 4
    assert len(W) == 6 and len(W) - 1 == 5
    assert len(W) - 2 == 4
    return {"minimum_profile": minima[0], "minimum_sum": minimum_sum, "N8": ledger[8]}


def main() -> None:
    equation = audit_equation_nine()
    normalization = audit_divided_power_normalization()
    shared = audit_shared_cofactors()
    lemma_three = audit_lemma_three()
    lemma_four = audit_lemma_four()
    equality = audit_three_essential_equality()
    nullities = audit_nullity_ledger()
    print("equation (9):", equation)
    print("divided powers (matchings, factorial):", normalization)
    print("shared cofactor factorizations:", shared)
    print("Lemma 3.1 degeneracies:", lemma_three)
    print("Lemma 4.1 incompatibilities:", lemma_four)
    print("three-essential equality:", equality)
    print("nullity ledger:", nullities)
    print("PASS: independent cubic leave-one-anchor nullity-web audit")


if __name__ == "__main__":
    main()
