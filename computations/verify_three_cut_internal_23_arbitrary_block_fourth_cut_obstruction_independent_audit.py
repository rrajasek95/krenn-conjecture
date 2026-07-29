#!/usr/bin/env python3
"""Clean-room exact audit of the arbitrary internal-A23 obstruction.

This file deliberately imports no project module.  It rebuilds endpoint-
ordered perfect matchings, insertion cylinders, the nine disjoint coordinate
blocks, all 480 outside-locus support masks, the four torus charts, the
cross-ratio line lock, and the characteristic-zero fibre ideals.

The implementation also differs computationally from the primary verifier:
it enumerates matchings by vertex bitmasks, uses greatest-coordinate sparse
elimination, obtains projected intersections from coefficient kernels of
column spaces, and reverses the star-variable order in the Singular rings.
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import os
import shutil
import subprocess
import time


Q = Fraction
COLOURS = (0, 1, 2)
INTERIOR = tuple(range(6))
ALL_SITES = tuple(range(8))
WORDS6 = tuple(product(COLOURS, repeat=6))

# Every colour pair is endpoint ordered: first colour at the lower endpoint.
FIXED_SOURCES = (
    (0, 1, 0, 0),
    (4, 5, 0, 0),
    (0, 2, 1, 1),
    (1, 4, 1, 1),
    (0, 4, 2, 2),
    (1, 3, 2, 2),
    (2, 5, 0, 0),
    (3, 5, 1, 0),
)

CELLS = tuple(product(COLOURS, repeat=2))
CELL_NAME = tuple(f"x{a}{b}" for a, b in CELLS)
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}

X00, X01, X02, X10, X11, X12, X20, X21, X22 = range(9)
OUTSIDE_ORDER = (X10, X12, X20, X22)
FIVE_CELL_LOCUS = frozenset((X00, X01, X02, X11, X21))
VARIABLE_COFACTOR_PAIRS = ((0, 1), (0, 5), (1, 5), (4, 5))

# Coordinates used in the uniform cross-ratio lock.
E_WORD = (0, 0, 2, 1, 0, 0)
V_WORDS = (
    (1, 2, 1, 2, 0, 0),
    (0, 0, 1, 1, 0, 0),
    (0, 0, 1, 2, 0, 0),
    (0, 0, 2, 2, 0, 0),
    (1, 1, 1, 1, 1, 0),
)

# Weights in the independent torus coordinates (r0,r1,r2,c0,c2).
TORUS_WEIGHTS = (
    (1, 0, 0, 1, 0),  # x00
    (2, 0, 0, 0, 0),  # x01
    (1, 0, 0, 0, 1),  # x02
    (0, 1, 0, 1, 0),  # x10
    (1, 1, 0, 0, 0),  # x11
    (0, 1, 0, 0, 1),  # x12
    (0, 0, 1, 1, 0),  # x20
    (1, 0, 1, 0, 0),  # x21
    (0, 0, 1, 0, 1),  # x22
)


@dataclass(frozen=True)
class Chart:
    name: str
    first: int
    retained: frozenset[int]
    optional: tuple[int, ...]
    normal_dimension: int


CHARTS = (
    Chart("x10", X10, frozenset((X10, X11, X21, X22)), (X11, X21, X22), 2),
    Chart("x12", X12, frozenset((X12, X11, X21, X22)), (X11, X21, X22), 1),
    Chart("x20", X20, frozenset((X10, X20, X11, X21, X22)), (X11, X21, X22), 2),
    Chart("x22", X22, frozenset((X10, X12, X20, X11, X21, X22)), (X11, X21), 1),
)
CHART_BY_FIRST = {chart.first: chart for chart in CHARTS}

EXPECTED_GENERATORS = {
    "x10": {
        (0, 0): 328, (0, 1): 432, (2, 0): 412, (2, 1): 516,
        (4, 0): 440, (4, 1): 544, (6, 0): 524, (6, 1): 628,
    },
    "x12": {
        (0, 0): 332, (0, 1): 436, (2, 0): 416, (2, 1): 520,
        (4, 0): 444, (4, 1): 548, (6, 0): 528,
    },
    "x20": {
        (0, 0): 356, (0, 1): 460, (2, 0): 440, (2, 1): 544,
        (4, 0): 468, (4, 1): 572, (6, 0): 552, (6, 1): 656,
    },
    "x22": {
        (4, 0): 384, (4, 1): 488, (6, 0): 468, (6, 1): 572,
    },
}


def add(vector, key, value):
    """Accumulate a rational sparse-vector entry."""
    value = Q(value)
    total = vector.get(key, Q(0)) + value
    if total:
        vector[key] = total
    else:
        vector.pop(key, None)


def scale(vector, scalar):
    scalar = Q(scalar)
    return {key: scalar * value for key, value in vector.items() if scalar * value}


def combine(vectors_and_scalars):
    result = {}
    for vector, scalar in vectors_and_scalars:
        for key, value in vector.items():
            add(result, key, Q(scalar) * value)
    return result


def subtract(left, right):
    return combine(((left, Q(1)), (right, Q(-1))))


def project_vector(vector, killed):
    return {key: value for key, value in vector.items() if key not in killed}


def canonical_basis(vectors):
    """Exact sparse echelon basis, pivoting from greatest coordinate down."""
    basis = {}
    for supplied in vectors:
        row = {key: Q(value) for key, value in supplied.items() if value}
        while row:
            pivot = max(row)
            if pivot not in basis:
                pivot_value = row[pivot]
                basis[pivot] = {
                    key: value / pivot_value for key, value in row.items()
                }
                break
            multiple = row[pivot]
            for key, value in basis[pivot].items():
                add(row, key, -multiple * value)
    return tuple(basis[key] for key in sorted(basis, reverse=True))


def in_span(vector, basis):
    row = {key: Q(value) for key, value in vector.items() if value}
    pivot_rows = {max(item): item for item in canonical_basis(basis)}
    while row:
        pivot = max(row)
        if pivot not in pivot_rows:
            return False
        multiple = row[pivot]
        for key, value in pivot_rows[pivot].items():
            add(row, key, -multiple * value)
    return True


def same_span(left, right):
    left_basis = canonical_basis(left)
    right_basis = canonical_basis(right)
    return (
        len(left_basis) == len(right_basis)
        and all(in_span(row, right_basis) for row in left_basis)
        and all(in_span(row, left_basis) for row in right_basis)
    )


def nullspace_rows(rows, columns):
    """Nullspace of a rational row matrix, returned as sparse row vectors."""
    reduced = [dict(row) for row in canonical_basis(rows)]
    pivot_to_row = {max(row): row for row in reduced}
    pivots = set(pivot_to_row)
    answer = []
    # With greatest-coordinate pivots, solve each free coordinate directly.
    for free in columns:
        if free in pivots:
            continue
        vector = {free: Q(1)}
        # Reduced-by-earlier rows is echelon, not RREF.  Back-substitute from
        # smallest pivot upward because each pivot row has only smaller tails.
        for pivot in sorted(pivots):
            row = pivot_to_row[pivot]
            contribution = sum(
                coefficient * vector.get(column, Q(0))
                for column, coefficient in row.items()
                if column != pivot
            )
            if contribution:
                vector[pivot] = -contribution
        answer.append(vector)
    for row in rows:
        for vector in answer:
            assert sum(row.get(c, 0) * vector.get(c, 0) for c in columns) == 0
    return tuple(answer)


def intersection_two(left, right):
    """Intersect two column spans via the kernel of [left | -right]."""
    u = canonical_basis(left)
    v = canonical_basis(right)
    if not u or not v:
        return ()
    coordinates = sorted(set().union(*(set(row) for row in u + v)))
    coefficient_rows = []
    for coordinate in coordinates:
        equation = {}
        for index, row in enumerate(u):
            if coordinate in row:
                equation[index] = row[coordinate]
        for index, row in enumerate(v):
            if coordinate in row:
                equation[len(u) + index] = -row[coordinate]
        if equation:
            coefficient_rows.append(equation)
    kernel = nullspace_rows(coefficient_rows, tuple(range(len(u) + len(v))))
    result = []
    for relation in kernel:
        vector = combine(
            (u[index], relation.get(index, Q(0))) for index in range(len(u))
        )
        assert vector
        assert in_span(vector, v)
        result.append(vector)
    return canonical_basis(result)


def intersection_many(spaces):
    result = canonical_basis(spaces[0])
    for space in spaces[1:]:
        result = intersection_two(result, space)
    return result


def matrix_rank(rows):
    return len(canonical_basis(
        {column: Q(value) for column, value in enumerate(row) if value}
        for row in rows
    ))


@lru_cache(maxsize=None)
def matchings_mask(mask):
    """Perfect matchings of the set bits, represented by ordered site pairs."""
    if mask == 0:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remaining = mask ^ first_bit
    answer = []
    scan = remaining
    while scan:
        mate_bit = scan & -scan
        mate = mate_bit.bit_length() - 1
        rest = remaining ^ mate_bit
        for tail in matchings_mask(rest):
            answer.append(((first, mate),) + tail)
        scan ^= mate_bit
    return tuple(answer)


def perfect_matchings(vertices):
    mask = sum(1 << site for site in vertices)
    return matchings_mask(mask)


def internal_blocks(coefficients):
    blocks = defaultdict(dict)
    for left, right, colour_left, colour_right in FIXED_SOURCES:
        blocks[left, right][colour_left, colour_right] = Q(1)
    for index, coefficient in enumerate(coefficients):
        if coefficient:
            blocks[2, 3][CELLS[index]] = Q(coefficient)
    return dict(blocks)


def matching_tensor(vertices, blocks):
    vertices = tuple(vertices)
    position = {site: index for index, site in enumerate(vertices)}
    answer = {}
    for matching in perfect_matchings(vertices):
        choices = [tuple(blocks.get(edge, {}).items()) for edge in matching]
        if any(not available for available in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = Q(1)
            for (left, right), ((left_colour, right_colour), weight) in zip(
                matching, selected
            ):
                word[position[left]] = left_colour
                word[position[right]] = right_colour
                coefficient *= weight
            add(answer, tuple(word), coefficient)
    return answer


def coefficients_for(indices, values=None):
    result = [Q(0)] * 9
    if values is None:
        values = [Q(1)] * len(indices)
    for index, value in zip(indices, values):
        result[index] = Q(value)
    return tuple(result)


def mask_coefficients(mask):
    return tuple(Q(1) if mask & (1 << index) else Q(0) for index in range(9))


def insertion_columns(cut, coefficients):
    """A fixed ordered list of 45 raw columns spanning C_cut."""
    blocks = internal_blocks(coefficients)
    five_sites = tuple(site for site in INTERIOR if site != cut)
    columns = []
    for cut_colour in COLOURS:
        for hole in five_sites:
            rest = tuple(site for site in five_sites if site != hole)
            cofactor = matching_tensor(rest, blocks)
            for hole_colour in COLOURS:
                vector = {}
                for rest_word, coefficient in cofactor.items():
                    assignment = dict(zip(rest, rest_word))
                    assignment[hole] = hole_colour
                    assignment[cut] = cut_colour
                    add(
                        vector,
                        tuple(assignment[site] for site in INTERIOR),
                        coefficient,
                    )
                columns.append(vector)
    assert len(columns) == 45
    return tuple(columns)


def projected_cylinder(cut, coefficients, killed):
    return canonical_basis(
        project_vector(column, killed)
        for column in insertion_columns(cut, coefficients)
    )


def four_cut_normal(coefficients, killed, final_cut):
    spaces = [
        projected_cylinder(cut, coefficients, killed)
        for cut in (2, 3, 4, final_cut)
    ]
    return intersection_many(spaces)


def atom_map(coefficients):
    """Endpoint-insertion atoms keyed by word and both ordered endpoints."""
    blocks = internal_blocks(coefficients)
    atoms = {}
    for left, right in combinations(INTERIOR, 2):
        rest = tuple(site for site in INTERIOR if site not in (left, right))
        cofactor = matching_tensor(rest, blocks)
        for rest_word, coefficient in cofactor.items():
            for left_colour, right_colour in product(COLOURS, repeat=2):
                assignment = dict(zip(rest, rest_word))
                assignment[left] = left_colour
                assignment[right] = right_colour
                word = tuple(assignment[site] for site in INTERIOR)
                key = (word, left, left_colour, right, right_colour)
                assert key not in atoms
                atoms[key] = coefficient
    return atoms


def project_atoms(atoms, killed):
    return {key: value for key, value in atoms.items() if key[0] not in killed}


def atoms_by_word(atoms):
    grouped = defaultdict(list)
    for (word, left, left_colour, right, right_colour), coefficient in atoms.items():
        grouped[word].append(
            (left, left_colour, right, right_colour, coefficient)
        )
    return {word: tuple(terms) for word, terms in grouped.items()}


def coordinate_blocks():
    zero = coefficients_for(())
    zero_atoms = atom_map(zero)
    blocks = []
    changed_pairs_by_cell = []
    for cell in range(9):
        delta_atoms = atom_map(coefficients_for((cell,)))
        differing_keys = {
            key for key in set(zero_atoms) | set(delta_atoms)
            if delta_atoms.get(key, Q(0)) != zero_atoms.get(key, Q(0))
        }
        coordinates = {key[0] for key in differing_keys}
        blocks.append(frozenset(coordinates))
        changed_pairs_by_cell.append(tuple(sorted({(key[1], key[3]) for key in differing_keys})))
    assert all(len(block) == 35 for block in blocks)
    assert all(left.isdisjoint(right) for left, right in combinations(blocks, 2))
    assert len(set().union(*blocks)) == 315
    assert all(pairs == VARIABLE_COFACTOR_PAIRS for pairs in changed_pairs_by_cell)
    assert (0,) * 6 in blocks[X00]
    assert (1,) * 6 in blocks[X11]
    assert (2,) * 6 in blocks[X22]
    for cell, block in enumerate(blocks):
        for colour in COLOURS:
            assert (((colour,) * 6) in block) == (
                cell == CELL_INDEX[(colour, colour)]
            )
    return tuple(blocks)


def first_outside(mask):
    for index in OUTSIDE_ORDER:
        if mask & (1 << index):
            return index
    return None


def family_signature(mask):
    d = 2 * bool(mask & (1 << X11)) + 4 * bool(mask & (1 << X22))
    b = int(bool(mask & (1 << X21)))
    return d, b


def representative_indices(chart, signature):
    d, b = signature
    answer = {chart.first}
    if d & 2:
        answer.add(X11)
    if d & 4:
        answer.add(X22)
    if b:
        answer.add(X21)
    return frozenset(answer)


def killed_coordinates(chart, blocks):
    killed_cells = set(range(9)) - set(chart.retained)
    return frozenset().union(*(blocks[cell] for cell in killed_cells))


def audit_support_partition_and_torus():
    masks_by_chart = defaultdict(list)
    for mask in range(1 << 9):
        first = first_outside(mask)
        if first is not None:
            masks_by_chart[CHART_BY_FIRST[first].name].append(mask)
    assert sum(map(len, masks_by_chart.values())) == 480
    assert tuple(len(masks_by_chart[chart.name]) for chart in CHARTS) == (
        256, 128, 64, 32
    )

    finite_families = []
    cross_ratio_masks = []
    for chart in CHARTS:
        signatures = sorted({family_signature(mask) for mask in masks_by_chart[chart.name]})
        expected = set(EXPECTED_GENERATORS[chart.name])
        if chart.name == "x12":
            assert set(signatures) == expected | {(6, 1)}
        else:
            assert set(signatures) == expected
        for signature in signatures:
            retained_support = representative_indices(chart, signature)
            weight_rows = [TORUS_WEIGHTS[index] for index in sorted(retained_support)]
            if chart.name == "x12" and signature == (6, 1):
                assert retained_support == frozenset((X11, X12, X21, X22))
                assert matrix_rank(weight_rows) == 3
                rectangle = (X11, X12, X21, X22)
                relation = (-1, 1, 1, -1)
                assert all(
                    sum(relation[i] * TORUS_WEIGHTS[rectangle[i]][j] for i in range(4)) == 0
                    for j in range(5)
                )
                # The chosen gauge x12=x11=x22=1 is legitimate; its three
                # weight rows are independent and the surviving normalized
                # x21 coefficient is exactly the displayed invariant.
                assert matrix_rank(
                    [TORUS_WEIGHTS[index] for index in (X12, X11, X22)]
                ) == 3
                cross_ratio_masks.extend(
                    mask for mask in masks_by_chart[chart.name]
                    if family_signature(mask) == signature
                )
            else:
                assert matrix_rank(weight_rows) == len(weight_rows)
                finite_families.append((chart, signature, retained_support))

    assert len(finite_families) == 27
    assert len(cross_ratio_masks) == 16  # four rectangle bits fixed, four killed bits free
    return masks_by_chart, tuple(finite_families), tuple(cross_ratio_masks)


def audit_torus_extension():
    """Check the weight table and preservation of all diagonal targets."""
    # Exponents g_(site,colour) in the five torus coordinates.
    zero = (0, 0, 0, 0, 0)
    exponents = {(site, colour): zero for site in ALL_SITES for colour in COLOURS}
    exponents[2, 0] = exponents[3, 1] = exponents[4, 0] = (1, 0, 0, 0, 0)
    exponents[5, 0] = (-1, 0, 0, 0, 0)
    exponents[3, 0] = (0, 0, 0, 1, 0)
    exponents[3, 2] = (0, 0, 0, 0, 1)
    exponents[2, 1] = (0, 1, 0, 0, 0)
    exponents[2, 2] = (0, 0, 1, 0, 0)
    exponents[0, 1] = (0, -1, 0, 0, 0)
    exponents[1, 2] = (0, 0, 0, 0, -1)

    def plus(*rows):
        return tuple(sum(row[j] for row in rows) for j in range(5))

    for left, right, left_colour, right_colour in FIXED_SOURCES:
        assert plus(exponents[left, left_colour], exponents[right, right_colour]) == zero
    observed = tuple(
        plus(exponents[2, a], exponents[3, b]) for a, b in CELLS
    )
    assert observed == TORUS_WEIGHTS
    for colour in COLOURS:
        interior_total = plus(*(exponents[site, colour] for site in INTERIOR))
        exponents[6, colour] = zero
        exponents[7, colour] = tuple(-entry for entry in interior_total)
        assert plus(*(exponents[site, colour] for site in ALL_SITES)) == zero


def audit_literal_eight_site_identity():
    """Use all 108 star entries and all nine A67 entries literally."""
    coefficients = tuple(Q(17 + 3 * index, 29 + index) for index in range(9))
    p = {
        (boundary, site, colour): Q(101 + 47 * boundary + 7 * site + colour, 37)
        for boundary, site, colour in product(COLOURS, INTERIOR, COLOURS)
    }
    q = {
        (boundary, site, colour): Q(401 + 53 * boundary + 11 * site + colour, 41)
        for boundary, site, colour in product(COLOURS, INTERIOR, COLOURS)
    }
    direct = {
        (a, b): Q(809 + 13 * a + 17 * b, 43)
        for a, b in product(COLOURS, repeat=2)
    }
    blocks = internal_blocks(coefficients)
    for site in INTERIOR:
        blocks[site, 6] = {
            (colour, boundary): p[boundary, site, colour]
            for colour, boundary in product(COLOURS, repeat=2)
        }
        blocks[site, 7] = {
            (colour, boundary): q[boundary, site, colour]
            for colour, boundary in product(COLOURS, repeat=2)
        }
    blocks[6, 7] = dict(direct)

    observed8 = matching_tensor(ALL_SITES, blocks)
    hs = matching_tensor(INTERIOR, internal_blocks(coefficients))
    grouped = atoms_by_word(atom_map(coefficients))
    for a, b in product(COLOURS, repeat=2):
        observed = {
            word[:6]: value for word, value in observed8.items()
            if word[6:] == (a, b)
        }
        predicted = scale(hs, direct[a, b])
        for word, terms in grouped.items():
            for left, left_colour, right, right_colour, coefficient in terms:
                add(
                    predicted,
                    word,
                    coefficient * (
                        p[a, left, left_colour] * q[b, right, right_colour]
                        + p[a, right, right_colour] * q[b, left, left_colour]
                    ),
                )
        assert observed == predicted


def qtext(value):
    value = Q(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def star_variable(side, boundary, site, colour):
    return f"{side}{boundary}s{site}c{colour}"


def reversed_star_variables():
    return [
        star_variable(side, boundary, site, colour)
        for side in ("q", "p")
        for boundary in (2, 1)
        for site in reversed(INTERIOR)
        for colour in reversed(COLOURS)
    ]


def coordinate_polynomial(grouped_atoms, a, b, word, symbolic=False):
    terms = []
    for left, left_colour, right, right_colour, coefficient in grouped_atoms.get(word, ()):
        if symbolic:
            constant, linear = coefficient
            if not constant and not linear:
                continue
            coefficient_text = qtext(constant)
            if linear:
                linear_text = qtext(linear)
                coefficient_text = f"({coefficient_text}+({linear_text})*lam)"
        else:
            coefficient_text = qtext(coefficient)
        terms.append(
            f"({coefficient_text})*{star_variable('p', a, left, left_colour)}*"
            f"{star_variable('q', b, right, right_colour)}"
        )
        terms.append(
            f"({coefficient_text})*{star_variable('p', a, right, right_colour)}*"
            f"{star_variable('q', b, left, left_colour)}"
        )
    return "+".join(terms) if terms else "0"


def finite_fibre_equations(grouped_atoms, normal, a, b):
    # Keep the complete three-colour target coordinate set even though the
    # contradiction uses colours 1 and 2.  The colour-zero equation can be a
    # literal zero generator in a severe quotient; retaining it makes the
    # ambient quotient audit transparent and keeps counts comparable.
    targets = tuple((colour,) * 6 for colour in COLOURS)
    coordinates = tuple(sorted(set(grouped_atoms) | set(targets) | set().union(*(set(v) for v in normal))))
    annihilator = nullspace_rows(normal, coordinates)
    target = (a,) * 6 if a == b else None
    equations = []
    for functional in annihilator:
        parts = []
        for word, coefficient in functional.items():
            parts.append(
                f"({qtext(coefficient)})*({coordinate_polynomial(grouped_atoms, a, b, word)})"
            )
        if target is not None and functional.get(target, Q(0)):
            parts.append(qtext(-functional[target]))
        equations.append("+".join(parts) if parts else "0")
    return equations


def finite_singular_program(grouped_atoms, normal):
    variables = reversed_star_variables()
    assert len(variables) == len(set(variables)) == 72
    generators = []
    # Ordered packet: 11, 12, 21, 22, with the same variables reused.
    for a, b in ((1, 1), (1, 2), (2, 1), (2, 2)):
        generators.extend(finite_fibre_equations(grouped_atoms, normal, a, b))
    lines = [
        "ring R=0,(" + ",".join(variables) + "),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(generators) + ";",
        "ideal G=std(I);",
        'print("AUDIT_UNIT"); if(reduce(1,G)==0){1;}else{0;}',
        'print("AUDIT_SIZE"); size(G);',
    ]
    return "\n".join(lines) + "\n", len(generators)


def linear_atom_map(atoms0, atoms1):
    answer = {}
    for key in set(atoms0) | set(atoms1):
        constant = atoms0.get(key, Q(0))
        linear = atoms1.get(key, Q(0)) - constant
        if constant or linear:
            answer[key] = (constant, linear)
    return answer


def symbolic_line_equations(grouped_atoms, a, b):
    targets = ((1,) * 6, (2,) * 6)
    line_words = set(V_WORDS) | {E_WORD}
    coordinates = tuple(sorted(set(grouped_atoms) | set(targets) | line_words))
    pivot = V_WORDS[0]
    target = (a,) * 6 if a == b else None
    pivot_beta = coordinate_polynomial(grouped_atoms, a, b, pivot, symbolic=True)
    pivot_target = Q(1) if target == pivot else Q(0)
    equations = []
    for word in coordinates:
        if word == pivot:
            continue
        beta = coordinate_polynomial(grouped_atoms, a, b, word, symbolic=True)
        target_value = Q(1) if target == word else Q(0)
        if word == E_WORD:
            normal_coefficient = "lam"
        elif word in V_WORDS:
            normal_coefficient = "1"
        else:
            normal_coefficient = "0"
        equation = (
            f"({beta})-({qtext(target_value)})-({normal_coefficient})*"
            f"(({pivot_beta})-({qtext(pivot_target)}))"
        )
        equations.append(equation)
    return equations


def symbolic_singular_program(grouped_atoms):
    variables = ["lam"] + reversed_star_variables()
    generators = []
    for a, b in ((1, 1), (1, 2), (2, 1), (2, 2)):
        generators.extend(symbolic_line_equations(grouped_atoms, a, b))
    lines = [
        "ring R=0,(" + ",".join(variables) + "),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(generators) + ";",
        "ideal G=std(I);",
        'print("AUDIT_UNIT"); if(reduce(1,G)==0){1;}else{0;}',
        'print("AUDIT_SIZE"); size(G);',
    ]
    return "\n".join(lines) + "\n", len(generators)


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_singular_job(item):
    name, program = item
    singular = shutil.which("Singular")
    if singular is None:
        raise RuntimeError("Singular is required for this exact-Q audit")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=1800,
    )
    if completed.stderr.strip():
        raise AssertionError(f"{name}: {completed.stderr}")
    assert marker(completed.stdout, "AUDIT_UNIT") == 1
    assert marker(completed.stdout, "AUDIT_SIZE") == 1
    return name, time.monotonic() - started


def finite_family_data(chart, signature, retained_support, coordinate_blocks_):
    killed = killed_coordinates(chart, coordinate_blocks_)
    coefficients = coefficients_for(sorted(retained_support))
    normals = {
        final: four_cut_normal(coefficients, killed, final)
        for final in (0, 1, 5)
    }
    assert all(len(normal) == chart.normal_dimension for normal in normals.values())
    assert same_span(normals[0], normals[1])
    assert same_span(normals[0], normals[5])
    normal = normals[0]
    hs = project_vector(matching_tensor(INTERIOR, internal_blocks(coefficients)), killed)
    assert in_span(hs, normal)
    for colour in (1, 2):
        target = {(colour,) * 6: Q(1)}
        assert (colour,) * 6 not in killed
        assert not in_span(target, normal)
    atoms = project_atoms(atom_map(coefficients), killed)
    grouped = atoms_by_word(atoms)
    program, generators = finite_singular_program(grouped, normal)
    assert generators == EXPECTED_GENERATORS[chart.name][signature], (
        chart.name, signature, generators,
        EXPECTED_GENERATORS[chart.name][signature], len(grouped), len(normal)
    )
    return {
        "chart": chart,
        "signature": signature,
        "support": retained_support,
        "coefficients": coefficients,
        "killed": killed,
        "normal": normal,
        "hs": hs,
        "atoms": atoms,
        "columns": {
            cut: tuple(project_vector(column, killed) for column in insertion_columns(cut, coefficients))
            for cut in INTERIOR
        },
        "program": program,
        "generators": generators,
    }


def audit_cross_ratio(coordinate_blocks_):
    chart = next(item for item in CHARTS if item.name == "x12")
    killed = killed_coordinates(chart, coordinate_blocks_)
    support0 = (X11, X12, X22)
    coefficients0 = coefficients_for(support0)
    coefficients1 = coefficients_for((X11, X12, X21, X22))
    coefficients2 = coefficients_for(
        (X11, X12, X21, X22), (Q(1), Q(1), Q(2), Q(1))
    )

    expanded = {}
    for cut in INTERIOR:
        columns0 = [project_vector(column, killed) for column in insertion_columns(cut, coefficients0)]
        columns1 = [project_vector(column, killed) for column in insertion_columns(cut, coefficients1)]
        columns2 = [project_vector(column, killed) for column in insertion_columns(cut, coefficients2)]
        for at_zero, at_one, at_two in zip(columns0, columns1, columns2):
            assert at_two == combine(((at_one, Q(2)), (at_zero, Q(-1))))
        expanded[cut] = canonical_basis(columns0 + columns1)
    expected_e = {E_WORD: Q(1)}
    expected_v = {word: Q(1) for word in V_WORDS}
    expected_plane = (expected_e, expected_v)
    for final in (0, 1, 5):
        upper = intersection_many([expanded[cut] for cut in (2, 3, 4, final)])
        assert len(upper) == 2
        assert same_span(upper, expected_plane)

    # The lambda-dependent functional e* - lambda [001100]* kills every
    # raw column of the final cylinder coefficient by coefficient.
    lock_word = (0, 0, 1, 1, 0, 0)
    for final in (0, 1, 5):
        columns0 = [project_vector(column, killed) for column in insertion_columns(final, coefficients0)]
        columns1 = [project_vector(column, killed) for column in insertion_columns(final, coefficients1)]
        assert len(columns0) == len(columns1) == 45
        for at_zero, at_one in zip(columns0, columns1):
            slope = subtract(at_one, at_zero)
            constant_coefficient = at_zero.get(E_WORD, Q(0))
            linear_coefficient = slope.get(E_WORD, Q(0)) - at_zero.get(lock_word, Q(0))
            quadratic_coefficient = -slope.get(lock_word, Q(0))
            assert (constant_coefficient, linear_coefficient, quadratic_coefficient) == (0, 0, 0)

    hs0 = project_vector(matching_tensor(INTERIOR, internal_blocks(coefficients0)), killed)
    hs1 = project_vector(matching_tensor(INTERIOR, internal_blocks(coefficients1)), killed)
    assert hs0 == expected_v
    assert subtract(hs1, hs0) == expected_e

    atoms0 = project_atoms(atom_map(coefficients0), killed)
    atoms1 = project_atoms(atom_map(coefficients1), killed)
    atoms2 = project_atoms(atom_map(coefficients2), killed)
    for key in set(atoms0) | set(atoms1) | set(atoms2):
        assert atoms2.get(key, Q(0)) == (
            2 * atoms1.get(key, Q(0)) - atoms0.get(key, Q(0))
        )
    symbolic_atoms = linear_atom_map(atoms0, atoms1)
    grouped = atoms_by_word(symbolic_atoms)
    program, generators = symbolic_singular_program(grouped)
    assert generators == 628, (generators, len(grouped))
    return {
        "chart": chart,
        "killed": killed,
        "coefficients0": coefficients0,
        "coefficients1": coefficients1,
        "hs0": hs0,
        "hs1": hs1,
        "atoms0": atoms0,
        "atoms1": atoms1,
        "columns0": {
            cut: tuple(project_vector(column, killed) for column in insertion_columns(cut, coefficients0))
            for cut in INTERIOR
        },
        "columns1": {
            cut: tuple(project_vector(column, killed) for column in insertion_columns(cut, coefficients1))
            for cut in INTERIOR
        },
        "program": program,
        "generators": generators,
    }


def audit_killed_cells_termwise(coordinate_blocks_):
    zero = coefficients_for(())
    zero_h = matching_tensor(INTERIOR, internal_blocks(zero))
    zero_atoms = atom_map(zero)
    zero_columns = {cut: insertion_columns(cut, zero) for cut in INTERIOR}
    for chart in CHARTS:
        killed = killed_coordinates(chart, coordinate_blocks_)
        for cell in set(range(9)) - set(chart.retained):
            one = coefficients_for((cell,))
            assert not project_vector(
                subtract(matching_tensor(INTERIOR, internal_blocks(one)), zero_h), killed
            )
            one_atoms = atom_map(one)
            delta_atom_keys = set(zero_atoms) | set(one_atoms)
            assert all(
                key[0] in killed
                for key in delta_atom_keys
                if one_atoms.get(key, Q(0)) != zero_atoms.get(key, Q(0))
            )
            for cut in INTERIOR:
                one_columns = insertion_columns(cut, one)
                for base_column, cell_column in zip(zero_columns[cut], one_columns):
                    assert not project_vector(subtract(cell_column, base_column), killed)


def audit_all_480_masks(masks_by_chart, finite_data, cross_data):
    finite_lookup = {
        (data["chart"].name, data["signature"]): data for data in finite_data
    }
    checked = 0
    for chart in CHARTS:
        for mask in masks_by_chart[chart.name]:
            signature = family_signature(mask)
            coefficients = mask_coefficients(mask)
            if chart.name == "x12" and signature == (6, 1):
                data = cross_data
                # A zero/one support has lambda=1 after the retained entries
                # are normalized, while killed entries are invisible.
                reference_coefficients = data["coefficients1"]
                reference_h = data["hs1"]
                reference_atoms = data["atoms1"]
                reference_columns = data["columns1"]
            else:
                data = finite_lookup[chart.name, signature]
                reference_coefficients = data["coefficients"]
                reference_h = data["hs"]
                reference_atoms = data["atoms"]
                reference_columns = data["columns"]
            killed = data["killed"]
            assert all(
                coefficients[index] == reference_coefficients[index]
                for index in chart.retained
            )
            observed_h = project_vector(
                matching_tensor(INTERIOR, internal_blocks(coefficients)), killed
            )
            assert observed_h == reference_h
            assert project_atoms(atom_map(coefficients), killed) == reference_atoms
            for cut in INTERIOR:
                observed_columns = tuple(
                    project_vector(column, killed)
                    for column in insertion_columns(cut, coefficients)
                )
                assert observed_columns == reference_columns[cut]
            checked += 1
    assert checked == 480


def audit_unit_ideals(finite_data, cross_data):
    jobs = {
        f"{data['chart'].name}_d{data['signature'][0]}_b{data['signature'][1]}": data["program"]
        for data in finite_data
    }
    jobs["x12_crossratio_lambda"] = cross_data["program"]
    elapsed = {}
    workers = min(12, max(1, os.cpu_count() or 1), len(jobs))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(run_singular_job, item): item[0]
            for item in jobs.items()
        }
        for future in as_completed(futures):
            name, duration = future.result()
            elapsed[name] = duration
    assert set(elapsed) == set(jobs)
    return elapsed


def main():
    started = time.monotonic()
    coordinate_blocks_ = coordinate_blocks()
    masks_by_chart, finite_families, cross_ratio_masks = audit_support_partition_and_torus()
    audit_torus_extension()
    audit_literal_eight_site_identity()
    audit_killed_cells_termwise(coordinate_blocks_)

    finite_data = [
        finite_family_data(chart, signature, retained, coordinate_blocks_)
        for chart, signature, retained in finite_families
    ]
    cross_data = audit_cross_ratio(coordinate_blocks_)
    audit_all_480_masks(masks_by_chart, finite_data, cross_data)
    elapsed = audit_unit_ideals(finite_data, cross_data)

    print("independent arbitrary-A23 fixed-interior audit: PASS")
    print("480 masks partitioned 256+128+64+32; 27 finite charts + lambda: PASS")
    print("nine disjoint 35-coordinate blocks; killed terms vanish coefficientwise: PASS")
    print("projected cut-0/1/5 intersections and x12 Q[lambda] line lock: PASS")
    print("endpoint order, 108 shared-star entries, ordered four-fibre packet, A67: PASS")
    for data in finite_data:
        name = f"{data['chart'].name}_d{data['signature'][0]}_b{data['signature'][1]}"
        print(f"{name}: {data['generators']} generators, exact-Q unit ({elapsed[name]:.3f}s): PASS")
    name = "x12_crossratio_lambda"
    print(f"{name}: {cross_data['generators']} generators, exact-Q[lambda] unit ({elapsed[name]:.3f}s): PASS")
    print(f"independent audit wall time: {time.monotonic() - started:.3f}s")


if __name__ == "__main__":
    main()
