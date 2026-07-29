#!/usr/bin/env python3
"""Exact toric-binomial refinement for the f=3 rank-graph cases.

The support formula knows only whether a perfect-matching monomial is zero.
Whenever a mixed coefficient has exactly two nonzero monomials, however, its
actual coefficient equation is a binomial ``x^a+x^b=0``.  Integer products
and quotients of these equations can force 2x2 minors of an exceptional
matrix to vanish.  This checker finds such certificates, verifies every one
over the integers, and adds a clause excluding precisely the support fibers
used by the certificate.

SciPy's MILP routine is used only to *find* short integer certificates.  A
candidate is accepted only after exact integer multiplication verifies both
the exponent identity and the required even sign parity.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass

import numpy as np
import sympy as sp
from pysat.solvers import Solver
from scipy.optimize import Bounds, LinearConstraint, milp

import search_f5_support_sat as base
import verify_f4_support_obstruction as previous
import verify_color_sensitive_support_obstruction as color_sensitive


LOWER_EDGE_GRAPHS = {
    "6P1": set(),
    "P2+4P1": {(0, 1)},
    "2P2+2P1": {(0, 1), (2, 3)},
    "P3+3P1": {(0, 1), (1, 2)},
}

RESIDUAL_GRAPHS = LOWER_EDGE_GRAPHS | base.THREE_EDGE_GRAPHS


def pfaffian_matching_sign(matching):
    """Return the standard Pfaffian crossing sign in vertex order."""
    edges = tuple(sorted(tuple(sorted(edge)) for edge in matching))
    crossings = sum(
        u < x < v < y or x < u < y < v
        for position, (u, v) in enumerate(edges)
        for x, y in edges[position + 1 :]
    )
    return -1 if crossings % 2 else 1


PFAFFIAN_TERM_SIGNS = tuple(
    pfaffian_matching_sign(matching) for matching in base.MATCHINGS
)
USE_PFAFFIAN_SIGNS = False


def term_sign(matching_index):
    return PFAFFIAN_TERM_SIGNS[matching_index] if USE_PFAFFIAN_SIGNS else 1


def relation_character(relations, coefficients):
    """Evaluate the exact {+1,-1} character of a Laurent combination."""
    answer = 1
    for relation, coefficient in zip(relations, coefficients, strict=True):
        # Do not use ``(-1) ** coefficient`` here: Python promotes a
        # negative integer power to a float (``(-1) ** -1 == -1.0``).
        # Parity is the exact character calculation for arbitrary positive
        # or negative integer coefficients.
        assert isinstance(coefficient, (int, sp.Integer))
        if relation.value == -1 and int(coefficient) % 2:
            answer = -answer
    assert isinstance(answer, int) and answer in (-1, 1)
    return answer


@dataclass(frozen=True)
class BinomialRelation:
    difference: tuple[int, ...]
    coloring: tuple[int, ...]
    supported: tuple[int, int]
    # For a signed two-term equation s_a*x^a+s_b*x^b=0, this is
    # x^(a-b)=-s_b/s_a.  It is -1 in the historical unsigned system.
    value: int = -1


def formal_keys(exceptional: set[tuple[int, int]]):
    """Return keys in exactly the order used by ``formal_signatures``."""
    rank_one = set(base.ALL_EDGES) - exceptional
    keys = []
    for edge in exceptional:
        for i, j in base.CELLS:
            keys.append(("entry", edge, i, j))
    for u, v in rank_one:
        for color in base.COLORS:
            keys.extend(
                [
                    ("factor_value", v, u, color),
                    ("factor_value", u, v, color),
                ]
            )
    return sorted(set(keys), key=repr)


def positive_model(solver: Solver):
    assert solver.solve()
    return {literal for literal in solver.get_model() if literal > 0}


def exact_binomial_relations(pool, signatures, model):
    """Collect one source fiber for each oriented signed exponent relation."""
    by_relation = {}
    for coloring in base.COLORINGS:
        if len(set(coloring)) == 1:
            continue
        supported = tuple(
            index
            for index in range(len(base.MATCHINGS))
            if pool.id(("monomial", coloring, index)) in model
        )
        if len(supported) != 2:
            continue
        first, second = supported
        difference = tuple(
            a - b
            for a, b in zip(
                signatures[coloring, first],
                signatures[coloring, second],
                strict=True,
            )
        )
        value = -term_sign(second) * term_sign(first)
        by_relation.setdefault(
            (difference, value),
            BinomialRelation(difference, coloring, supported, value),
        )
    return tuple(by_relation.values())


def odd_short_binomial_certificate(
    relations: tuple[BinomialRelation, ...],
):
    """Find an exact one- or three-fiber ``1=-1`` certificate.

    A relation says ``x^difference=value`` in the Laurent torus.  A product
    whose exponent is zero and whose exact value is -1 is inconsistent.
    Searching length at most three is enough for the historical residual
    charts and is deliberately exact and finite.
    """
    zero = (0,) * (len(relations[0].difference) if relations else 0)
    for relation in relations:
        if relation.difference == zero and relation.value == -1:
            return ((relation, 1),)

    by_difference = {}
    for index, relation in enumerate(relations):
        by_difference.setdefault(relation.difference, []).append(
            (index, relation)
        )
    for first_index, first in enumerate(relations):
        for second_index in range(first_index + 1, len(relations)):
            second = relations[second_index]
            for first_sign, second_sign in itertools.product((-1, 1), repeat=2):
                needed = tuple(
                    -(first_sign * a + second_sign * b)
                    for a, b in zip(
                        first.difference, second.difference, strict=True
                    )
                )
                found = by_difference.get(needed, ())
                if not found:
                    continue
                for third_index, third in found:
                    if third_index in (first_index, second_index):
                        continue
                    certificate = (
                        (first, first_sign),
                        (second, second_sign),
                        (third, 1),
                    )
                    exact_sum = tuple(
                        sum(
                            coefficient * relation.difference[position]
                            for relation, coefficient in certificate
                        )
                        for position in range(len(zero))
                    )
                    assert exact_sum == zero
                    if relation_character(
                        tuple(relation for relation, _ in certificate),
                        tuple(coefficient for _, coefficient in certificate),
                    ) == -1:
                        return certificate
    return None


def find_odd_integer_certificate(
    relations: tuple[BinomialRelation, ...],
    coefficient_bound: int = 4,
):
    """Find and exactly verify any bounded odd Laurent sign cycle.

    The MILP is only a proposal mechanism.  Both the zero exponent sum and
    the odd coefficient sum are checked with Python integers before the
    certificate is returned.
    """
    if not relations:
        return None
    differences = np.asarray(
        [relation.difference for relation in relations], dtype=np.int64
    ).T
    dimension, count = differences.shape
    constraint = np.zeros((dimension + 1, 2 * count + 1), dtype=float)
    constraint[:dimension, :count] = differences
    constraint[:dimension, count : 2 * count] = -differences
    character_bits = np.asarray(
        [int(relation.value == -1) for relation in relations], dtype=float
    )
    constraint[-1, :count] = character_bits
    constraint[-1, count : 2 * count] = -character_bits
    constraint[-1, -1] = -2
    right_hand_side = np.asarray((*([0] * dimension), 1), dtype=float)
    objective = np.asarray((*([1.0] * (2 * count)), 0.0))
    lower = np.asarray((*([0.0] * (2 * count)), -100.0))
    upper = np.asarray(
        (*([float(coefficient_bound)] * (2 * count)), 100.0)
    )
    result = milp(
        objective,
        integrality=np.ones(2 * count + 1),
        bounds=Bounds(lower, upper),
        constraints=LinearConstraint(
            constraint, right_hand_side, right_hand_side
        ),
        options={"time_limit": 10.0},
    )
    if not result.success:
        return None

    rounded = np.rint(result.x).astype(np.int64)
    coefficients = rounded[:count] - rounded[count : 2 * count]
    exact_product = differences @ coefficients
    assert all(int(value) == 0 for value in exact_product)
    assert relation_character(relations, tuple(map(int, coefficients))) == -1
    assert np.any(coefficients)
    return tuple(
        (relations[index], int(coefficient))
        for index, coefficient in enumerate(coefficients)
        if coefficient
    )


def trinomial_sign_conflict(pool, signatures, model):
    """Find two translated three-term fibers with incompatible signs.

    Binomial fibers define a sign character on their exponent lattice.  If
    two three-term fibers have the same two normalized exponent differences
    modulo that lattice, but at least one comparison has odd sign, their
    equations become ``1+r+s=0`` and ``1+/-r+/-s=0`` with a nontrivial sign
    change.  Adding or subtracting gives twice a nonzero Laurent monomial.

    For a compact exact membership oracle we select independent binomial
    rows having a unimodular coordinate minor.  If this chart does not offer
    such a minor, the routine conservatively returns no cut.
    """
    relations = exact_binomial_relations(pool, signatures, model)
    if not relations:
        return None
    difference_matrix = sp.Matrix(
        [relation.difference for relation in relations]
    )
    _rref, basis_indices = difference_matrix.T.rref()
    basis_indices = tuple(basis_indices)
    basis = difference_matrix[list(basis_indices), :]
    _rref, coordinate_columns = basis.rref()
    coordinate_columns = tuple(coordinate_columns)
    coordinate_minor = basis[:, list(coordinate_columns)]
    if abs(int(coordinate_minor.det())) != 1:
        return None
    inverse_minor = coordinate_minor.inv()

    def lattice_coordinates(target):
        target_row = sp.Matrix(1, len(target), target)
        coefficients = (
            target_row[:, list(coordinate_columns)] * inverse_minor
        )
        if any(value.q != 1 for value in coefficients):
            return None
        if coefficients * basis != target_row:
            return None
        return tuple(int(value) for value in coefficients)

    basis_relations = tuple(relations[index] for index in basis_indices)

    def lattice_character(coordinates):
        return relation_character(basis_relations, coordinates)

    trinomial_fibers = []
    for coloring in base.COLORINGS:
        if len(set(coloring)) == 1:
            continue
        supported = tuple(
            index
            for index in range(len(base.MATCHINGS))
            if pool.id(("monomial", coloring, index)) in model
        )
        if len(supported) == 3:
            trinomial_fibers.append((coloring, supported))

    for first_index, (first_coloring, first_supported) in enumerate(
        trinomial_fibers
    ):
        first_exponents = [
            signatures[first_coloring, index] for index in first_supported
        ]
        first_differences = [
            tuple(
                a - b
                for a, b in zip(
                    first_exponents[position], first_exponents[0], strict=True
                )
            )
            for position in (1, 2)
        ]
        for second_coloring, second_supported in trinomial_fibers[
            first_index + 1 :
        ]:
            second_exponents_unordered = [
                signatures[second_coloring, index]
                for index in second_supported
            ]
            for permutation in itertools.permutations(range(3)):
                second_exponents = [
                    second_exponents_unordered[index]
                    for index in permutation
                ]
                second_supported_ordered = [
                    second_supported[index] for index in permutation
                ]
                certificates = []
                parities = []
                for position in (1, 2):
                    target = tuple(
                        first_difference - (second_value - second_base)
                        for first_difference, second_value, second_base in zip(
                            first_differences[position - 1],
                            second_exponents[position],
                            second_exponents[0],
                            strict=True,
                        )
                    )
                    coefficients = lattice_coordinates(target)
                    if coefficients is None:
                        break
                    certificate = tuple(
                        (relations[basis_indices[index]], coefficient)
                        for index, coefficient in enumerate(coefficients)
                        if coefficient
                    )
                    exact_sum = tuple(
                        sum(
                            coefficient * relation.difference[coordinate]
                            for relation, coefficient in certificate
                        )
                        for coordinate in range(len(target))
                    )
                    assert exact_sum == target
                    certificates.append(certificate)
                    first_relative_sign = (
                        term_sign(first_supported[position])
                        * term_sign(first_supported[0])
                    )
                    second_relative_sign = (
                        term_sign(second_supported_ordered[position])
                        * term_sign(second_supported_ordered[0])
                    )
                    comparison = (
                        first_relative_sign
                        * lattice_character(coefficients)
                        * second_relative_sign
                    )
                    assert comparison in (-1, 1)
                    parities.append(int(comparison == -1))
                if len(certificates) != 2 or not any(parities):
                    continue
                used_fibers = {
                    first_coloring: first_supported,
                    second_coloring: second_supported,
                }
                for certificate in certificates:
                    for relation, _coefficient in certificate:
                        used_fibers[relation.coloring] = relation.supported
                return (
                    used_fibers,
                    first_coloring,
                    second_coloring,
                    tuple(parities),
                    len(certificates[0]),
                    len(certificates[1]),
                )
    return None


def single_fiber_laurent_conflict(pool, signatures, model):
    """Find one mixed fiber reduced to one nonzero Laurent class.

    Every exact two-term mixed fiber supplies a relation ``x^d=-1``.
    Select an independent row basis whose pivot-coordinate minor is
    unimodular.  It then spans the *integer* relation lattice, and the
    parity of the integral coordinates records the sign of every Laurent
    ratio in that lattice.

    In any other mixed fiber, group terms whose exponent differences lie
    in this lattice and add their forced signs.  If precisely one group has
    nonzero signed multiplicity, the coefficient equation is a nonzero
    integer times a nonzero Laurent monomial, which is impossible over
    characteristic zero.  The returned dictionary lists only the exact
    coefficient fibers used by the certificate.
    """
    relations = exact_binomial_relations(pool, signatures, model)
    if not relations:
        return None

    relation_matrix = sp.Matrix(
        [relation.difference for relation in relations]
    )
    _rref, basis_indices = relation_matrix.T.rref()
    basis_indices = tuple(basis_indices)
    basis = relation_matrix[list(basis_indices), :]
    _basis_rref, coordinate_columns = basis.rref()
    coordinate_columns = tuple(coordinate_columns)
    coordinate_minor = basis[:, list(coordinate_columns)]
    if abs(int(coordinate_minor.det())) != 1:
        # Decline rather than infer an equality only in the saturation of
        # the actual binomial lattice.
        return None
    inverse_minor = coordinate_minor.inv()

    def lattice_coordinates(target):
        target_row = sp.Matrix(1, len(target), target)
        coefficients = target_row[:, list(coordinate_columns)] * inverse_minor
        if any(value.q != 1 for value in coefficients):
            return None
        if coefficients * basis != target_row:
            return None
        return tuple(int(value) for value in coefficients)

    basis_relations = tuple(relations[index] for index in basis_indices)

    def lattice_character(coordinates):
        return relation_character(basis_relations, coordinates)

    # First audit that every redundant binomial has the sign dictated by
    # the selected basis.  A mismatch is already an odd Laurent cycle.
    for relation in relations:
        coordinates = lattice_coordinates(relation.difference)
        assert coordinates is not None
        if lattice_character(coordinates) != relation.value:
            used = {
                relations[index].coloring: relations[index].supported
                for index, coefficient in zip(
                    basis_indices, coordinates, strict=True
                )
                if coefficient
            }
            used[relation.coloring] = relation.supported
            return used, relation.coloring, (1,), "odd-binomial"

    for coloring in base.COLORINGS:
        if len(set(coloring)) == 1:
            continue
        supported = tuple(
            index
            for index in range(len(base.MATCHINGS))
            if pool.id(("monomial", coloring, index)) in model
        )
        if len(supported) < 3:
            continue

        exponents = [signatures[coloring, index] for index in supported]
        # A class is represented by its first term.  ``class_sums`` stores
        # the signed multiplicity forced by the binomial character.
        classes = []
        term_certificates = []
        for term_position, exponent in enumerate(exponents):
            placed = False
            for class_index, representative_position in enumerate(classes):
                difference = tuple(
                    a - b
                    for a, b in zip(
                        exponent,
                        exponents[representative_position],
                        strict=True,
                    )
                )
                coordinates = lattice_coordinates(difference)
                if coordinates is None:
                    continue
                term_certificates.append(
                    (term_position, class_index, coordinates)
                )
                placed = True
                break
            if not placed:
                classes.append(term_position)
                term_certificates.append(
                    (term_position, len(classes) - 1, (0,) * len(basis_indices))
                )

        class_sums = [0] * len(classes)
        for term_position, class_index, coordinates in term_certificates:
            class_sums[class_index] += (
                term_sign(supported[term_position])
                * lattice_character(coordinates)
            )
        nonzero_classes = tuple(
            index for index, value in enumerate(class_sums) if value
        )
        if len(nonzero_classes) != 1:
            continue

        used = {coloring: supported}
        for _term_position, _class_index, coordinates in term_certificates:
            for basis_position, coefficient in enumerate(coordinates):
                if coefficient:
                    relation = relations[basis_indices[basis_position]]
                    used[relation.coloring] = relation.supported
        return (
            used,
            coloring,
            tuple(class_sums),
            "single-laurent-class",
        )
    return None


def minor_target(key_index, edge, row_pair, column_pair):
    i, k = row_pair
    j, ell = column_pair
    target = [0] * len(key_index)
    for cell, coefficient in (
        ((i, j), 1),
        ((k, ell), 1),
        ((i, ell), -1),
        ((k, j), -1),
    ):
        target[key_index[("entry", edge, *cell)]] += coefficient
    return tuple(target)


def find_even_integer_certificate(
    relations: tuple[BinomialRelation, ...],
    target: tuple[int, ...],
    coefficient_bound: int = 4,
):
    """Find z with sum(z_r)d_r=target and sum(z_r)=0 mod 2.

    Write z=p-n with nonnegative integral p,n.  The final integral variable
    records half the coefficient sum.  Bounds merely keep the heuristic
    search small; failure to find a certificate never produces a cut.
    """
    if not relations:
        return None
    differences = np.asarray(
        [relation.difference for relation in relations], dtype=np.int64
    ).T
    dimension, count = differences.shape
    constraint = np.zeros((dimension + 1, 2 * count + 1), dtype=float)
    constraint[:dimension, :count] = differences
    constraint[:dimension, count : 2 * count] = -differences
    character_bits = np.asarray(
        [int(relation.value == -1) for relation in relations], dtype=float
    )
    constraint[-1, :count] = character_bits
    constraint[-1, count : 2 * count] = -character_bits
    constraint[-1, -1] = -2
    right_hand_side = np.asarray((*target, 0), dtype=float)
    objective = np.asarray((*([1.0] * (2 * count)), 0.0))
    lower = np.asarray((*([0.0] * (2 * count)), -100.0))
    upper = np.asarray(
        (*([float(coefficient_bound)] * (2 * count)), 100.0)
    )
    result = milp(
        objective,
        integrality=np.ones(2 * count + 1),
        bounds=Bounds(lower, upper),
        constraints=LinearConstraint(
            constraint, right_hand_side, right_hand_side
        ),
        options={"time_limit": 10.0},
    )
    if not result.success:
        return None

    rounded = np.rint(result.x).astype(np.int64)
    coefficients = rounded[:count] - rounded[count : 2 * count]

    # The floating-point optimizer is never trusted as a proof oracle.
    exact_product = differences @ coefficients
    assert tuple(int(value) for value in exact_product) == target
    assert relation_character(relations, tuple(map(int, coefficients))) == 1
    assert np.any(coefficients)
    return tuple(
        (relations[index], int(coefficient))
        for index, coefficient in enumerate(coefficients)
        if coefficient
    )


def edge_support(pool, model, edge):
    return {
        (i, j)
        for i, j in base.CELLS
        if pool.id(("entry", edge, i, j)) in model
    }


def is_two_closed(support):
    color_pairs = tuple(itertools.combinations(base.COLORS, 2))
    for i, k in color_pairs:
        for j, ell in color_pairs:
            for diagonal, cross in (
                (((i, j), (k, ell)), ((i, ell), (k, j))),
                (((i, ell), (k, j)), ((i, j), (k, ell))),
            ):
                if all(cell in support for cell in diagonal) and not all(
                    cell in support for cell in cross
                ):
                    return False
    return True


def exact_entry_support_block(pool, edge, support):
    return [
        (
            -pool.id(("entry", edge, i, j))
            if (i, j) in support
            else pool.id(("entry", edge, i, j))
        )
        for i, j in base.CELLS
    ]


def add_minor_witnesses(formula, pool, exceptional, active):
    """Add a conservative witness for a genuinely nonzero 2x2 minor.

    An active matrix has rank at least two, so at least one of its nine
    minors is nonzero.  The auxiliary variable records which one.  We impose
    only the necessary support condition that at least one diagonal product
    of that minor is nonzero.  Any actual realization therefore extends to
    a satisfying assignment of these variables.
    """
    color_pairs = tuple(itertools.combinations(base.COLORS, 2))
    witnesses = {}
    for edge in sorted(exceptional):
        edge_witnesses = []
        for row_pair in color_pairs:
            for column_pair in color_pairs:
                witness = pool.id(
                    ("nonzero_minor", edge, row_pair, column_pair)
                )
                witnesses[edge, row_pair, column_pair] = witness
                edge_witnesses.append(witness)
                i, k = row_pair
                j, ell = column_pair
                a = pool.id(("entry", edge, i, j))
                b = pool.id(("entry", edge, k, ell))
                c = pool.id(("entry", edge, i, ell))
                d = pool.id(("entry", edge, k, j))
                # witness -> ((a and b) or (c and d)).
                for first in (a, b):
                    for second in (c, d):
                        formula.append([-witness, first, second])
        formula.append([-active[edge]] + edge_witnesses)
    return witnesses


def toric_witness_cut(
    pool,
    signatures,
    exceptional,
    witnesses,
    model,
    allowed_witness_keys=None,
):
    """Forbid a selected nonzero-minor witness killed by binomial fibers."""
    relations = exact_binomial_relations(pool, signatures, model)
    keys = formal_keys(exceptional)
    key_index = {key: index for index, key in enumerate(keys)}
    assert len(keys) == len(next(iter(signatures.values())))

    for (edge, row_pair, column_pair), witness in sorted(
        witnesses.items(), key=lambda item: repr(item[0])
    ):
        if (
            allowed_witness_keys is not None
            and (edge, row_pair, column_pair) not in allowed_witness_keys
        ):
            continue
        if witness not in model:
            continue
        support = edge_support(pool, model, edge)
        i, k = row_pair
        j, ell = column_pair
        cells = ((i, j), (i, ell), (k, j), (k, ell))
        if not all(cell in support for cell in cells):
            continue
        target = minor_target(key_index, edge, row_pair, column_pair)
        certificate = find_even_integer_certificate(relations, target)
        if certificate is None:
            continue

        used_fibers = {
            relation.coloring: relation.supported
            for relation, _ in certificate
        }
        clause = [-witness]
        for coloring, supported in used_fibers.items():
            clause.extend(
                previous.exact_support_block(
                    pool, coloring, set(supported)
                )
            )
        return (
            clause,
            edge,
            row_pair,
            column_pair,
            used_fibers,
        )
    return None


def graph_automorphisms(exceptional):
    answer = []
    for permutation in itertools.permutations(base.VERTICES):
        image = {
            tuple(sorted((permutation[u], permutation[v])))
            for u, v in exceptional
        }
        if image == exceptional:
            answer.append(permutation)
    return tuple(answer)


def add_support_lex_leaders(formula, pool, exceptional, automorphisms):
    """Keep a lexicographically least support in every chart symmetry orbit.

    The base support formula is invariant under graph automorphisms and one
    simultaneous global color permutation.  Requiring the ordered support
    bit vector to be no larger than each of its images therefore preserves
    at least one representative of every orbit.  This is ordinary exact
    symmetry breaking; it is useful when adding one direct Laurent cut at a
    time, because those cuts then enumerate support/fiber orbits rather than
    all their labelled copies.
    """
    variables = []
    metadata = []
    for edge in sorted(base.ALL_EDGES):
        if edge in exceptional:
            for a, b in base.CELLS:
                variables.append(pool.id(("entry", edge, a, b)))
                metadata.append(("entry", edge, a, b))
        else:
            u, v = edge
            for color in base.COLORS:
                variables.append(pool.id(("factor", v, u, color)))
                metadata.append(("factor", v, u, color))
            for color in base.COLORS:
                variables.append(pool.id(("factor", u, v, color)))
                metadata.append(("factor", u, v, color))

    def mapped_variable(item, vertex_permutation, color_permutation):
        if item[0] == "factor":
            _, other, center, color = item
            return pool.id(
                (
                    "factor",
                    vertex_permutation[other],
                    vertex_permutation[center],
                    color_permutation[color],
                )
            )
        _, (u, v), a, b = item
        uu, vv = vertex_permutation[u], vertex_permutation[v]
        aa, bb = color_permutation[a], color_permutation[b]
        if uu > vv:
            uu, vv = vv, uu
            aa, bb = bb, aa
        return pool.id(("entry", (uu, vv), aa, bb))

    identity_vertices = tuple(base.VERTICES)
    identity_colors = tuple(base.COLORS)
    comparisons = 0
    for vertex_permutation in automorphisms:
        for color_permutation in itertools.permutations(base.COLORS):
            if (
                vertex_permutation == identity_vertices
                and color_permutation == identity_colors
            ):
                continue
            image = [
                mapped_variable(item, vertex_permutation, color_permutation)
                for item in metadata
            ]
            prefix = pool.id(
                ("lex_prefix", comparisons, 0)
            )
            formula.append([prefix])
            for position, (left, right) in enumerate(
                zip(variables, image, strict=True)
            ):
                # Equal prefixes may not be followed by 1 on the left and
                # 0 on the right.
                formula.append([-prefix, -left, right])
                if left == right:
                    next_prefix = prefix
                    continue
                equal = pool.id(("lex_equal", comparisons, position))
                formula.extend(
                    [
                        [-equal, -left, right],
                        [-equal, left, -right],
                        [left, right, equal],
                        [-left, -right, equal],
                    ]
                )
                next_prefix = pool.id(
                    ("lex_prefix", comparisons, position + 1)
                )
                formula.extend(
                    [
                        [-next_prefix, prefix],
                        [-next_prefix, equal],
                        [-prefix, -equal, next_prefix],
                    ]
                )
                prefix = next_prefix
            comparisons += 1
    return comparisons


def transform_fiber(coloring, supported, vertex_permutation, color_permutation):
    transformed_coloring = [None] * len(base.VERTICES)
    for vertex, color in enumerate(coloring):
        transformed_coloring[vertex_permutation[vertex]] = color_permutation[color]

    matching_index = {
        frozenset(matching): index
        for index, matching in enumerate(base.MATCHINGS)
    }
    transformed_supported = []
    for index in supported:
        transformed_matching = frozenset(
            tuple(
                sorted((vertex_permutation[u], vertex_permutation[v]))
            )
            for u, v in base.MATCHINGS[index]
        )
        transformed_supported.append(matching_index[transformed_matching])
    return tuple(transformed_coloring), tuple(sorted(transformed_supported))


def fiber_indicator(
    solver, pool, cache, coloring, supported, clause_sink=None
):
    """Return a Tseitin variable equivalent to one exact fiber support."""
    key = (coloring, supported)
    if key in cache:
        return cache[key]
    indicator = pool.id(("exact_fiber", coloring, supported))
    cache[key] = indicator
    pattern_literals = [
        (
            pool.id(("monomial", coloring, index))
            if index in supported
            else -pool.id(("monomial", coloring, index))
        )
        for index in range(len(base.MATCHINGS))
    ]
    for literal in pattern_literals:
        clause = [-indicator, literal]
        solver.add_clause(clause)
        if clause_sink is not None:
            clause_sink.append(clause)
    clause = [indicator] + [-literal for literal in pattern_literals]
    solver.add_clause(clause)
    if clause_sink is not None:
        clause_sink.append(clause)
    return indicator


def toric_cut_orbit(
    solver,
    pool,
    fiber_indicator_cache,
    clause_sink,
    witnesses,
    automorphisms,
    edge,
    row_pair,
    column_pair,
    used_fibers,
):
    """Apply edge-image representatives and every global color permutation.

    The full stabilizer orbit is sound but unnecessarily burdens the SAT
    solver.  One representative for each ordered image of the target edge
    retains the useful edge/endpoint symmetry at a modest clause cost.
    """
    u, v = edge
    clauses = set()
    representatives = {}
    for vertex_permutation in automorphisms:
        representatives.setdefault(
            (vertex_permutation[u], vertex_permutation[v]),
            vertex_permutation,
        )
    for vertex_permutation in representatives.values():
        mapped_u = vertex_permutation[u]
        mapped_v = vertex_permutation[v]
        mapped_edge = tuple(sorted((mapped_u, mapped_v)))
        reversed_endpoints = mapped_u > mapped_v
        for color_permutation in itertools.permutations(base.COLORS):
            mapped_rows = tuple(
                sorted(color_permutation[color] for color in row_pair)
            )
            mapped_columns = tuple(
                sorted(color_permutation[color] for color in column_pair)
            )
            if reversed_endpoints:
                mapped_rows, mapped_columns = mapped_columns, mapped_rows
            mapped_witness = witnesses[
                mapped_edge, mapped_rows, mapped_columns
            ]
            clause = [-mapped_witness]
            for coloring, supported in used_fibers.items():
                mapped_coloring, mapped_supported = transform_fiber(
                    coloring,
                    supported,
                    vertex_permutation,
                    color_permutation,
                )
                clause.append(
                    -fiber_indicator(
                        solver,
                        pool,
                        fiber_indicator_cache,
                        mapped_coloring,
                        mapped_supported,
                        clause_sink,
                    )
                )
            clauses.add(tuple(clause))
    return tuple(clauses)


def exact_fiber_cut_orbit(
    solver,
    pool,
    fiber_indicator_cache,
    clause_sink,
    automorphisms,
    source_fibers,
    use_symmetry_orbit=True,
):
    """Forbid every symmetry image of a contradictory fiber collection."""
    clauses = set()
    vertex_permutations = (
        automorphisms
        if use_symmetry_orbit
        else (tuple(base.VERTICES),)
    )
    color_permutations = (
        tuple(itertools.permutations(base.COLORS))
        if use_symmetry_orbit
        else (tuple(base.COLORS),)
    )
    for vertex_permutation in vertex_permutations:
        for color_permutation in color_permutations:
            clause = []
            for coloring, supported in source_fibers.items():
                mapped_coloring, mapped_supported = transform_fiber(
                    coloring,
                    supported,
                    vertex_permutation,
                    color_permutation,
                )
                clause.append(
                    -fiber_indicator(
                        solver,
                        pool,
                        fiber_indicator_cache,
                        mapped_coloring,
                        mapped_supported,
                        clause_sink,
                    )
                )
            clauses.add(tuple(sorted(clause)))
    return tuple(clauses)


def odd_binomial_cut_orbit(
    solver,
    pool,
    fiber_indicator_cache,
    clause_sink,
    automorphisms,
    certificate,
    use_symmetry_orbit=True,
):
    """Forbid every symmetry image of an odd Laurent sign cycle."""
    source_fibers = {
        relation.coloring: relation.supported
        for relation, _coefficient in certificate
    }
    return exact_fiber_cut_orbit(
        solver,
        pool,
        fiber_indicator_cache,
        clause_sink,
        automorphisms,
        source_fibers,
        use_symmetry_orbit,
    )


def toric_rank_cut(pool, signatures, exceptional, active, model):
    """Return a sound clause if binomials force an active edge to rank one."""
    relations = exact_binomial_relations(pool, signatures, model)
    keys = formal_keys(exceptional)
    key_index = {key: index for index, key in enumerate(keys)}
    assert len(keys) == len(next(iter(signatures.values())))
    color_pairs = tuple(itertools.combinations(base.COLORS, 2))

    for edge in sorted(exceptional):
        if active[edge] not in model:
            continue
        support = edge_support(pool, model, edge)
        if not is_two_closed(support):
            continue

        certificates = []
        failed = False
        for row_pair in color_pairs:
            for column_pair in color_pairs:
                i, k = row_pair
                j, ell = column_pair
                cells = ((i, j), (i, ell), (k, j), (k, ell))
                if not all(cell in support for cell in cells):
                    continue
                target = minor_target(
                    key_index, edge, row_pair, column_pair
                )
                certificate = find_even_integer_certificate(
                    relations, target
                )
                if certificate is None:
                    failed = True
                    break
                certificates.append(certificate)
            if failed:
                break
        if failed:
            continue

        # Two-closure deals with minors having a zero cell; the certificates
        # kill every fully supported minor.  Thus this active matrix has rank
        # at most one, contradicting the active/rank-at-least-two condition.
        used_fibers = {}
        for certificate in certificates:
            for relation, _ in certificate:
                used_fibers[relation.coloring] = relation.supported

        clause = [-active[edge]]
        clause.extend(exact_entry_support_block(pool, edge, support))
        for coloring, supported in used_fibers.items():
            clause.extend(
                previous.exact_support_block(
                    pool, coloring, set(supported)
                )
            )
        assert clause
        return clause, edge, len(certificates), len(used_fibers)
    return None


def audit_graph(
    name,
    exceptional,
    cut_limit=10000,
    solver_name="cadical195",
    fixed_witness=None,
    use_symmetry_orbit=True,
    static_rebuild_interval=100,
    automorphism_limit=None,
    use_lex_leaders=False,
    artifact_sink=None,
    use_support_cuts=True,
):
    # Lazy import avoids a module-initialization cycle: the reusable engine
    # imports this file for the exact BinomialRelation data type.
    import generalized_laurent_elimination as generalized

    formula, pool, active = base.support_formula(exceptional)
    witnesses = add_minor_witnesses(
        formula, pool, exceptional, active
    )
    if fixed_witness is not None:
        formula.append([witnesses[fixed_witness]])
    signatures = previous.formal_signatures(exceptional, pool)
    automorphisms = graph_automorphisms(exceptional)
    if automorphism_limit is not None:
        assert automorphism_limit >= 1
        automorphisms = automorphisms[:automorphism_limit]
    if use_lex_leaders:
        comparisons = add_support_lex_leaders(
            formula, pool, exceptional, automorphisms
        )
        print(
            f"{name}: installed {comparisons} exact support lex leaders",
            flush=True,
        )
    transfer_total = 0
    toric_cuts = 0
    odd_cuts = 0
    trinomial_cuts = 0
    single_fiber_cuts = 0
    translated_trinomial_cuts = 0
    generalized_cuts = 0
    support_cuts = 0
    semantic_records = []

    def named_fibers(fibers):
        return tuple(
            (tuple(coloring), tuple(supported))
            for coloring, supported in sorted(fibers.items())
        )

    def audit_counts():
        return (
            f"transfers={transfer_total}, toric_rank_cuts={toric_cuts}, "
            f"odd_cuts={odd_cuts}, single_fiber_cuts={single_fiber_cuts}, "
            f"translated_trinomial_cuts={translated_trinomial_cuts}, "
            f"generalized_cuts={generalized_cuts}, "
            f"support_cuts={support_cuts}"
        )

    fiber_indicator_cache = {}
    recorded_clauses = [list(clause) for clause in formula.clauses]

    def conclude(value):
        if artifact_sink is not None:
            artifact_sink.clear()
            artifact_sink.update(
                records=semantic_records,
                variables=pool.top,
                clauses=recorded_clauses,
                counts={
                    "transfers": transfer_total,
                    "toric_rank_cuts": toric_cuts,
                    "odd_cuts": odd_cuts,
                    "single_fiber_cuts": single_fiber_cuts,
                    "translated_trinomial_cuts": translated_trinomial_cuts,
                    "generalized_cuts": generalized_cuts,
                    "support_cuts": support_cuts,
                },
            )
        return value

    with Solver(name=solver_name, bootstrap_with=formula) as solver:
        survives, transfers = previous.add_cancellation_transfers(
            solver,
            pool,
            signatures,
            clause_sink=recorded_clauses,
            term_signs=(PFAFFIAN_TERM_SIGNS if USE_PFAFFIAN_SIGNS else None),
            semantic_sink=semantic_records,
        )
        transfer_total += transfers
        if not survives:
            print(f"{name}: UNSAT; {audit_counts()}")
            return conclude(True)
        while True:
            # Kissat is exceptionally effective on the accumulated static
            # formula but does not support incremental calls.  Periodically
            # rebuild it for one exact solve, then continue learning in the
            # incremental solver from the returned model.
            static_model = None
            learned_cuts = (
                toric_cuts + odd_cuts + trinomial_cuts + support_cuts
            )
            if (
                static_rebuild_interval
                and learned_cuts
                and learned_cuts % static_rebuild_interval == 0
            ):
                with Solver(
                    name="kissat404", bootstrap_with=recorded_clauses
                ) as static_solver:
                    static_sat = static_solver.solve()
                    if static_sat:
                        static_model = {
                            literal
                            for literal in static_solver.get_model()
                            if literal > 0
                        }
                if not static_sat:
                    print(f"{name}: UNSAT; {audit_counts()}")
                    return conclude(True)
            if static_model is None and not solver.solve():
                print(f"{name}: UNSAT; {audit_counts()}")
                return conclude(True)
            model = static_model or {
                literal for literal in solver.get_model() if literal > 0
            }

            # Cheap sign-independent tensor/support witnesses are stronger
            # than the Laurent refinements and should be installed first.
            # This is particularly effective in the signed F=0 audit,
            # where many SAT charts already collapse to two edge partitions.
            supports = color_sensitive.extract_supports(
                pool, model, exceptional
            )
            early_kind = None
            early_witness = color_sensitive.deletion_witness(supports)
            if early_witness is not None:
                early_kind = "partition-rank"
            if early_witness is None:
                early_witness = color_sensitive.triangle_rank_witness(
                    supports, exceptional
                )
                if early_witness is not None:
                    early_kind = "triangle-rank"
            if early_witness is None:
                early_witness = (
                    color_sensitive.rainbow_triangle_cofactor_witness(
                        supports, exceptional
                    )
                )
                if early_witness is not None:
                    early_kind = "rainbow-triangle-cofactor"
            if early_witness is None:
                early_witness = (
                    color_sensitive.rectangle_cancellation_witness(
                        supports, exceptional
                    )
                )
                if early_witness is not None:
                    early_kind = "rectangle-cancellation"
            if early_witness is None:
                early_witness = color_sensitive.cycle_cancellation_witness(
                    supports, exceptional
                )
                if early_witness is not None:
                    early_kind = "cycle-cancellation"
            if not use_support_cuts:
                early_witness = None
            if early_witness is not None:
                orbit_clauses = set()
                for vertex_permutation in automorphisms:
                    for color_permutation in itertools.permutations(
                        base.COLORS
                    ):
                        mapped = color_sensitive.transform_supports(
                            supports,
                            vertex_permutation,
                            color_permutation,
                        )
                        if early_kind in {
                            "partition-rank",
                            "triangle-rank",
                        }:
                            support_clause = (
                                color_sensitive.subsupport_escape_clause(
                                    pool, exceptional, mapped
                                )
                            )
                        else:
                            # The rectangle/cycle/rainbow implications are
                            # exact for this support chart.  Blocking the
                            # chart itself gives shorter CNF clauses than a
                            # large conjunction of exact fiber indicators.
                            support_clause = (
                                color_sensitive.exact_support_clause(
                                    pool, exceptional, mapped
                                )
                            )
                        orbit_clauses.add(tuple(support_clause))
                for support_clause in orbit_clauses:
                    solver.add_clause(list(support_clause))
                    recorded_clauses.append(list(support_clause))
                support_cuts += 1
                if support_cuts <= 5 or support_cuts % 25 == 0:
                    print(
                        f"{name}: early support cut {support_cuts}; "
                        f"kind={early_kind}, orbit={len(orbit_clauses)}",
                        flush=True,
                    )
                continue

            single_fiber_conflict = single_fiber_laurent_conflict(
                pool, signatures, model
            )
            if single_fiber_conflict is not None:
                used_fibers, coloring, class_sums, conflict_kind = (
                    single_fiber_conflict
                )
                semantic_records.append(
                    {
                        "kind": "single_fiber",
                        "fibers": named_fibers(used_fibers),
                        "target": tuple(coloring),
                        "class_sums": tuple(class_sums),
                        "conflict_kind": conflict_kind,
                    }
                )
                orbit = exact_fiber_cut_orbit(
                    solver,
                    pool,
                    fiber_indicator_cache,
                    recorded_clauses,
                    automorphisms,
                    used_fibers,
                    use_symmetry_orbit,
                )
                for orbit_clause in orbit:
                    solver.add_clause(list(orbit_clause))
                    recorded_clauses.append(list(orbit_clause))
                trinomial_cuts += 1
                single_fiber_cuts += 1
                if trinomial_cuts <= 5 or trinomial_cuts % 25 == 0:
                    print(
                        f"{name}: single-fiber Laurent cut "
                        f"{trinomial_cuts}; kind={conflict_kind}, "
                        f"color={coloring}, class_sums={class_sums}, "
                        f"fibers={len(used_fibers)}, orbit={len(orbit)}",
                        flush=True,
                    )
                continue
            odd_certificate = odd_short_binomial_certificate(
                exact_binomial_relations(pool, signatures, model)
            )
            if odd_certificate is not None:
                orbit = odd_binomial_cut_orbit(
                    solver,
                    pool,
                    fiber_indicator_cache,
                    recorded_clauses,
                    automorphisms,
                    odd_certificate,
                    use_symmetry_orbit,
                )
                for orbit_clause in orbit:
                    solver.add_clause(list(orbit_clause))
                    recorded_clauses.append(list(orbit_clause))
                odd_cuts += 1
                if odd_cuts <= 5 or odd_cuts % 25 == 0:
                    print(
                        f"{name}: odd-binomial cut {odd_cuts}; "
                        f"fibers={len(odd_certificate)}, orbit={len(orbit)}",
                        flush=True,
                    )
                continue
            trinomial_conflict = trinomial_sign_conflict(
                pool, signatures, model
            )
            if trinomial_conflict is not None:
                (
                    used_fibers,
                    first_coloring,
                    second_coloring,
                    parities,
                    first_certificate_size,
                    second_certificate_size,
                ) = trinomial_conflict
                semantic_records.append(
                    {
                        "kind": "translated_trinomial",
                        "fibers": named_fibers(used_fibers),
                        "first": tuple(first_coloring),
                        "second": tuple(second_coloring),
                        "parities": tuple(parities),
                    }
                )
                orbit = exact_fiber_cut_orbit(
                    solver,
                    pool,
                    fiber_indicator_cache,
                    recorded_clauses,
                    automorphisms,
                    used_fibers,
                    use_symmetry_orbit,
                )
                for orbit_clause in orbit:
                    solver.add_clause(list(orbit_clause))
                    recorded_clauses.append(list(orbit_clause))
                trinomial_cuts += 1
                translated_trinomial_cuts += 1
                # These genuinely two-fiber certificates are rare and
                # logically distinct from the single-fiber Laurent cuts.
                # Always expose them in the audit transcript.
                print(
                    f"{name}: trinomial-sign cut {trinomial_cuts}; "
                    f"colors={first_coloring},{second_coloring}, "
                    f"parities={parities}, certificates="
                    f"{first_certificate_size},{second_certificate_size}, "
                    f"fibers={len(used_fibers)}, orbit={len(orbit)}",
                    flush=True,
                )
                continue
            generalized_conflict = generalized.generalized_laurent_conflict(
                pool,
                signatures,
                model,
                (
                    PFAFFIAN_TERM_SIGNS
                    if USE_PFAFFIAN_SIGNS
                    else None
                ),
            )
            if generalized_conflict is not None:
                used_fibers = dict(generalized_conflict.used_fibers)
                orbit = exact_fiber_cut_orbit(
                    solver,
                    pool,
                    fiber_indicator_cache,
                    recorded_clauses,
                    automorphisms,
                    used_fibers,
                    use_symmetry_orbit,
                )
                for orbit_clause in orbit:
                    solver.add_clause(list(orbit_clause))
                    recorded_clauses.append(list(orbit_clause))
                generalized_cuts += 1
                if generalized_cuts <= 5 or generalized_cuts % 25 == 0:
                    print(
                        f"{name}: generalized Laurent cut "
                        f"{generalized_cuts}; kind="
                        f"{generalized_conflict.kind}, scalar="
                        f"{generalized_conflict.scalar}, "
                        f"fibers={len(used_fibers)}, orbit={len(orbit)}",
                        flush=True,
                    )
                continue
            cut = toric_witness_cut(
                pool,
                signatures,
                exceptional,
                witnesses,
                model,
                ({fixed_witness} if fixed_witness is not None else None),
            )
            if cut is None:
                # A toric-stable chart may expose a new translated-fiber
                # contradiction.  Saturate those only at phase boundaries,
                # rather than rescanning them after every toric clause.
                survives, transfers = previous.add_cancellation_transfers(
                    solver,
                    pool,
                    signatures,
                    clause_sink=recorded_clauses,
                    term_signs=(
                        PFAFFIAN_TERM_SIGNS if USE_PFAFFIAN_SIGNS else None
                    ),
                    semantic_sink=semantic_records,
                )
                transfer_total += transfers
                if not survives:
                    print(f"{name}: UNSAT; {audit_counts()}")
                    return conclude(True)
                # ``add_cancellation_transfers`` may finish on a different
                # support model from the one checked above.  Inspect exactly
                # that retained model before declaring a survivor.
                model = {
                    literal for literal in solver.get_model() if literal > 0
                }
                single_fiber_conflict = single_fiber_laurent_conflict(
                    pool, signatures, model
                )
                if single_fiber_conflict is not None:
                    used_fibers, coloring, class_sums, conflict_kind = (
                        single_fiber_conflict
                    )
                    semantic_records.append(
                        {
                            "kind": "single_fiber",
                            "fibers": named_fibers(used_fibers),
                            "target": tuple(coloring),
                            "class_sums": tuple(class_sums),
                            "conflict_kind": conflict_kind,
                        }
                    )
                    orbit = exact_fiber_cut_orbit(
                        solver,
                        pool,
                        fiber_indicator_cache,
                        recorded_clauses,
                        automorphisms,
                        used_fibers,
                        use_symmetry_orbit,
                    )
                    for orbit_clause in orbit:
                        solver.add_clause(list(orbit_clause))
                        recorded_clauses.append(list(orbit_clause))
                    trinomial_cuts += 1
                    single_fiber_cuts += 1
                    print(
                        f"{name}: single-fiber Laurent cut "
                        f"{trinomial_cuts}; kind={conflict_kind}, "
                        f"color={coloring}, class_sums={class_sums}, "
                        f"fibers={len(used_fibers)}, orbit={len(orbit)}",
                        flush=True,
                    )
                    continue
                odd_certificate = odd_short_binomial_certificate(
                    exact_binomial_relations(pool, signatures, model)
                )
                if odd_certificate is not None:
                    orbit = odd_binomial_cut_orbit(
                        solver,
                        pool,
                        fiber_indicator_cache,
                        recorded_clauses,
                        automorphisms,
                        odd_certificate,
                        use_symmetry_orbit,
                    )
                    for orbit_clause in orbit:
                        solver.add_clause(list(orbit_clause))
                        recorded_clauses.append(list(orbit_clause))
                    odd_cuts += 1
                    if odd_cuts <= 5 or odd_cuts % 25 == 0:
                        print(
                            f"{name}: odd-binomial cut {odd_cuts}; "
                            f"fibers={len(odd_certificate)}, "
                            f"orbit={len(orbit)}",
                            flush=True,
                        )
                    continue
                odd_certificate = find_odd_integer_certificate(
                    exact_binomial_relations(pool, signatures, model)
                )
                if odd_certificate is not None:
                    orbit = odd_binomial_cut_orbit(
                        solver,
                        pool,
                        fiber_indicator_cache,
                        recorded_clauses,
                        automorphisms,
                        odd_certificate,
                        use_symmetry_orbit,
                    )
                    for orbit_clause in orbit:
                        solver.add_clause(list(orbit_clause))
                        recorded_clauses.append(list(orbit_clause))
                    odd_cuts += 1
                    print(
                        f"{name}: general odd-binomial cut {odd_cuts}; "
                        f"fibers={len(odd_certificate)}, orbit={len(orbit)}",
                        flush=True,
                    )
                    continue
                trinomial_conflict = trinomial_sign_conflict(
                    pool, signatures, model
                )
                if trinomial_conflict is not None:
                    (
                        used_fibers,
                        first_coloring,
                        second_coloring,
                        parities,
                        first_certificate_size,
                        second_certificate_size,
                    ) = trinomial_conflict
                    semantic_records.append(
                        {
                            "kind": "translated_trinomial",
                            "fibers": named_fibers(used_fibers),
                            "first": tuple(first_coloring),
                            "second": tuple(second_coloring),
                            "parities": tuple(parities),
                        }
                    )
                    orbit = exact_fiber_cut_orbit(
                        solver,
                        pool,
                        fiber_indicator_cache,
                        recorded_clauses,
                        automorphisms,
                        used_fibers,
                        use_symmetry_orbit,
                    )
                    for orbit_clause in orbit:
                        solver.add_clause(list(orbit_clause))
                        recorded_clauses.append(list(orbit_clause))
                    trinomial_cuts += 1
                    translated_trinomial_cuts += 1
                    print(
                        f"{name}: trinomial-sign cut {trinomial_cuts}; "
                        f"colors={first_coloring},{second_coloring}, "
                        f"parities={parities}, certificates="
                        f"{first_certificate_size},{second_certificate_size}, "
                        f"fibers={len(used_fibers)}, orbit={len(orbit)}",
                        flush=True,
                    )
                    continue
                generalized_conflict = (
                    generalized.generalized_laurent_conflict(
                        pool,
                        signatures,
                        model,
                        (
                            PFAFFIAN_TERM_SIGNS
                            if USE_PFAFFIAN_SIGNS
                            else None
                        ),
                    )
                )
                if generalized_conflict is not None:
                    used_fibers = dict(generalized_conflict.used_fibers)
                    orbit = exact_fiber_cut_orbit(
                        solver,
                        pool,
                        fiber_indicator_cache,
                        recorded_clauses,
                        automorphisms,
                        used_fibers,
                        use_symmetry_orbit,
                    )
                    for orbit_clause in orbit:
                        solver.add_clause(list(orbit_clause))
                        recorded_clauses.append(list(orbit_clause))
                    generalized_cuts += 1
                    print(
                        f"{name}: generalized Laurent cut "
                        f"{generalized_cuts}; kind="
                        f"{generalized_conflict.kind}, scalar="
                        f"{generalized_conflict.scalar}, "
                        f"fibers={len(used_fibers)}, orbit={len(orbit)}",
                        flush=True,
                    )
                    continue
                cut = toric_witness_cut(
                    pool,
                    signatures,
                    exceptional,
                    witnesses,
                    model,
                    ({fixed_witness} if fixed_witness is not None else None),
                )
                if cut is not None:
                    pass
                else:
                    supports = color_sensitive.extract_supports(
                        pool, model, exceptional
                    )
                    support_kind = None
                    support_witness = color_sensitive.deletion_witness(supports)
                    if support_witness is not None:
                        support_kind = "partition-rank"
                    if support_witness is None:
                        support_witness = color_sensitive.triangle_rank_witness(
                            supports, exceptional
                        )
                        if support_witness is not None:
                            support_kind = "triangle-rank"
                    if support_witness is None:
                        rainbow_witness = (
                            color_sensitive.rainbow_triangle_cofactor_witness(
                                supports, exceptional
                            )
                        )
                        if rainbow_witness is not None:
                            support_witness = rainbow_witness
                            support_kind = "rainbow-triangle-cofactor"
                    if support_witness is None:
                        rectangle_witness = (
                            color_sensitive.rectangle_cancellation_witness(
                                supports, exceptional
                            )
                        )
                        if rectangle_witness is not None:
                            support_witness = rectangle_witness
                            support_kind = "rectangle-cancellation"
                    if support_witness is None:
                        cycle_witness = color_sensitive.cycle_cancellation_witness(
                            supports, exceptional
                        )
                        if cycle_witness is not None:
                            support_witness = cycle_witness
                            support_kind = "cycle-cancellation"
                    if not use_support_cuts:
                        support_witness = None
                    if support_witness is not None:
                        orbit_clauses = set()
                        for vertex_permutation in automorphisms:
                            for color_permutation in itertools.permutations(base.COLORS):
                                mapped = color_sensitive.transform_supports(
                                    supports,
                                    vertex_permutation,
                                    color_permutation,
                                )
                                if support_kind in {
                                    "partition-rank",
                                    "triangle-rank",
                                }:
                                    support_clause = (
                                        color_sensitive.subsupport_escape_clause(
                                            pool, exceptional, mapped
                                        )
                                    )
                                else:
                                    support_clause = (
                                        color_sensitive.exact_support_clause(
                                            pool, exceptional, mapped
                                        )
                                    )
                                orbit_clauses.add(
                                    tuple(support_clause)
                                )
                        for support_clause in orbit_clauses:
                            solver.add_clause(list(support_clause))
                            recorded_clauses.append(list(support_clause))
                        support_cuts += 1
                        if support_cuts <= 5 or support_cuts % 25 == 0:
                            print(
                                f"{name}: support cut {support_cuts}; "
                                f"kind={support_kind}, orbit={len(orbit_clauses)}",
                                flush=True,
                            )
                        continue
                    active_edges = [
                        edge
                        for edge in sorted(exceptional)
                        if active[edge] in model
                    ]
                    print(
                        f"{name}: survivor; {audit_counts()}, "
                        f"active={active_edges}"
                    )
                    if fixed_witness is not None or USE_PFAFFIAN_SIGNS:
                        exceptional_supports = {
                            edge: "".join(
                                f"{i}{j}"
                                for i, j in base.CELLS
                                if pool.id(("entry", edge, i, j)) in model
                            )
                            for edge in sorted(exceptional)
                        }
                        factor_supports = {}
                        for u, v in sorted(
                            set(base.ALL_EDGES) - exceptional
                        ):
                            at_u = "".join(
                                str(color)
                                for color in base.COLORS
                                if pool.id(("factor", v, u, color)) in model
                            )
                            at_v = "".join(
                                str(color)
                                for color in base.COLORS
                                if pool.id(("factor", u, v, color)) in model
                            )
                            factor_supports[u, v] = (at_u, at_v)
                        relation_count = len(
                            exact_binomial_relations(pool, signatures, model)
                        )
                        print(
                            f"{name}: exceptional_supports="
                            f"{exceptional_supports}"
                        )
                        print(f"{name}: factor_supports={factor_supports}")
                        print(
                            f"{name}: binomial_relations={relation_count}"
                        )
                    return conclude(False)
            (
                _direct_clause,
                edge,
                row_pair,
                column_pair,
                used_fibers,
            ) = cut
            if use_symmetry_orbit:
                orbit = toric_cut_orbit(
                    solver,
                    pool,
                    fiber_indicator_cache,
                    recorded_clauses,
                    witnesses,
                    automorphisms,
                    edge,
                    row_pair,
                    column_pair,
                    used_fibers,
                )
            else:
                direct = [-witnesses[edge, row_pair, column_pair]]
                for coloring, supported in used_fibers.items():
                    direct.append(
                        -fiber_indicator(
                            solver,
                            pool,
                            fiber_indicator_cache,
                            coloring,
                            supported,
                            recorded_clauses,
                        )
                    )
                orbit = (tuple(direct),)
            for orbit_clause in orbit:
                solver.add_clause(list(orbit_clause))
                recorded_clauses.append(list(orbit_clause))
            toric_cuts += 1
            if toric_cuts <= 5 or toric_cuts % 25 == 0:
                print(
                    f"{name}: toric cut {toric_cuts} on {edge}; "
                    f"minor={row_pair}x{column_pair}, "
                    f"fibers={len(used_fibers)}, orbit={len(orbit)}",
                    flush=True,
                )
            assert toric_cuts < cut_limit


def verify_documented_3p2_certificate():
    """Check equations (4)--(5) of notes/toric-binomial-rank.md."""
    exceptional = base.THREE_EDGE_GRAPHS["3P2"]
    formula, pool, _ = base.support_formula(exceptional)
    del formula
    signatures = previous.formal_signatures(exceptional, pool)
    first = base.MATCHINGS.index(((0, 1), (2, 3), (4, 5)))
    second = base.MATCHINGS.index(((0, 2), (1, 4), (3, 5)))
    signed_colorings = (
        (1, (0, 0, 1, 2, 1, 2)),
        (-1, (0, 1, 1, 2, 1, 1)),
        (-1, (1, 0, 2, 2, 1, 2)),
        (1, (1, 1, 2, 2, 1, 1)),
    )
    total = [0] * len(next(iter(signatures.values())))
    for coefficient, coloring in signed_colorings:
        for position, (a, b) in enumerate(
            zip(
                signatures[coloring, first],
                signatures[coloring, second],
                strict=True,
            )
        ):
            total[position] += coefficient * (a - b)
    key_index = {
        key: index
        for index, key in enumerate(formal_keys(exceptional))
    }
    target = minor_target(
        key_index, (0, 1), (0, 1), (0, 1)
    )
    assert tuple(total) == target
    assert sum(coefficient for coefficient, _ in signed_colorings) % 2 == 0
    print("documented 3P2 four-binomial minor certificate verified")


def main():
    global USE_PFAFFIAN_SIGNS
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph",
        action="append",
        choices=tuple(RESIDUAL_GRAPHS),
        help="audit one residual graph (repeatable)",
    )
    parser.add_argument(
        "--all-residual",
        action="store_true",
        help="include the four isomorphism types with zero, one, or two edges",
    )
    parser.add_argument("--cut-limit", type=int, default=10000)
    parser.add_argument("--no-symmetry", action="store_true")
    parser.add_argument(
        "--pfaffian-signs",
        action="store_true",
        help="audit signed Pfaffian matching coefficients instead of +1",
    )
    parser.add_argument(
        "--automorphism-limit",
        type=int,
        help=(
            "use only this many graph automorphisms per learned orbit; "
            "each retained image is independently sound"
        ),
    )
    parser.add_argument(
        "--no-static-rebuild",
        action="store_true",
        help="keep the incremental CaDiCaL solver instead of periodic Kissat checks",
    )
    args = parser.parse_args()
    USE_PFAFFIAN_SIGNS = args.pfaffian_signs
    if USE_PFAFFIAN_SIGNS:
        print(f"Pfaffian term signs: {PFAFFIAN_TERM_SIGNS}")
    verify_documented_3p2_certificate()
    if args.graph:
        graphs = {name: RESIDUAL_GRAPHS[name] for name in args.graph}
    elif args.all_residual:
        graphs = RESIDUAL_GRAPHS
    else:
        graphs = base.THREE_EDGE_GRAPHS
    closed = []
    for name, exceptional in graphs.items():
        if audit_graph(
            name,
            exceptional,
            cut_limit=args.cut_limit,
            use_symmetry_orbit=not args.no_symmetry,
            static_rebuild_interval=(
                0
                if args.no_static_rebuild
                else (25 if USE_PFAFFIAN_SIGNS else 100)
            ),
            automorphism_limit=args.automorphism_limit,
        ):
            closed.append(name)
    print(f"closed {len(closed)}/{len(graphs)}: {closed}")


if __name__ == "__main__":
    main()
