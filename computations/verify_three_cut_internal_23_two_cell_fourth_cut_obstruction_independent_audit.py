#!/usr/bin/env python3
"""Independent exact audit of the two-cell A_23 perturbation theorem.

This file imports none of the primary project modules.  It reconstructs the
endpoint-ordered matching tensors, five-site insertion spaces, four-cut
cylinder intersections, boundary-star bilinear equations, torus reduction,
and all componentwise unit certificates over Q.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import shutil
import subprocess

import sympy as sp


Q = Fraction
INTERIOR = tuple(range(6))
ALL_SITES = tuple(range(8))
COLOURS = (0, 1, 2)
WORDS5 = tuple(product(COLOURS, repeat=5))
WORDS6 = tuple(product(COLOURS, repeat=6))

# Endpoint order is literal: the first colour is placed at the lower endpoint.
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

E0 = (0, 0, 0, 0, 0, 0)
U0 = (0, 0, 2, 1, 0, 0)
U1 = (1, 2, 1, 2, 0, 0)
U2 = (1, 1, 1, 1, 1, 0)
U3 = (2, 2, 0, 2, 2, 0)
UPLUS_WORDS = (U1, U2, U3)


def add(result, key, value):
    total = result.get(key, 0) + value
    if total != 0:
        result[key] = total
    else:
        result.pop(key, None)


def unit(word, coefficient=Q(1)):
    return {word: coefficient}


def vector_sum(*vectors):
    result = {}
    for vector in vectors:
        for word, coefficient in vector.items():
            add(result, word, coefficient)
    return result


def blocks_at(t, s):
    blocks = {}
    for left, right, colour_left, colour_right in FIXED_SOURCES:
        blocks.setdefault((left, right), {})[colour_left, colour_right] = 1
    moving = {}
    if t != 0:
        moving[2, 1] = t
    if s != 0:
        moving[0, 0] = s
    blocks[2, 3] = moving
    return blocks


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        mate = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            result.append(((first, mate),) + tail)
    return tuple(result)


def matching_tensor(vertices, blocks):
    """Enumerate aggregate-cell choices in every perfect matching."""
    vertices = tuple(vertices)
    positions = {site: index for index, site in enumerate(vertices)}
    result = {}
    for matching in perfect_matchings(vertices):
        choices = [tuple(blocks.get(edge, {}).items()) for edge in matching]
        if any(not values for values in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = 1
            for (left, right), ((colour_left, colour_right), weight) in zip(
                matching, selected
            ):
                word[positions[left]] = colour_left
                word[positions[right]] = colour_right
                coefficient *= weight
            add(result, tuple(word), coefficient)
    return result


def span_basis(vectors):
    """Sparse exact row-echelon basis, keyed by lexicographic pivots."""
    basis = {}
    for supplied in vectors:
        row = {key: Q(value) for key, value in supplied.items() if value}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                basis[pivot] = {key: value / scale for key, value in row.items()}
                break
            multiple = row[pivot]
            for key, value in basis[pivot].items():
                updated = row.get(key, Q(0)) - multiple * value
                if updated:
                    row[key] = updated
                else:
                    row.pop(key, None)
    return basis


def in_span(vector, basis):
    row = {key: Q(value) for key, value in vector.items() if value}
    while row:
        pivot = min(row)
        if pivot not in basis:
            return False
        multiple = row[pivot]
        for key, value in basis[pivot].items():
            updated = row.get(key, Q(0)) - multiple * value
            if updated:
                row[key] = updated
            else:
                row.pop(key, None)
    return True


def rref(vectors, coordinates):
    rows = [
        {key: Q(value) for key, value in supplied.items() if value}
        for supplied in vectors
    ]
    rows = [row for row in rows if row]
    pivots = []
    active = 0
    for coordinate in coordinates:
        found = next(
            (
                index
                for index in range(active, len(rows))
                if rows[index].get(coordinate, Q(0))
            ),
            None,
        )
        if found is None:
            continue
        rows[active], rows[found] = rows[found], rows[active]
        scale = rows[active][coordinate]
        rows[active] = {
            key: value / scale for key, value in rows[active].items()
        }
        for index, row in enumerate(rows):
            if index == active:
                continue
            multiple = row.get(coordinate, Q(0))
            if not multiple:
                continue
            for key, value in rows[active].items():
                updated = row.get(key, Q(0)) - multiple * value
                if updated:
                    row[key] = updated
                else:
                    row.pop(key, None)
        pivots.append(coordinate)
        active += 1
        if active == len(rows):
            break
    assert all(not row for row in rows[active:])
    return rows[:active], tuple(pivots)


def annihilator(vectors, coordinates):
    """Basis of coordinate functionals vanishing on all supplied vectors."""
    rows, pivots = rref(vectors, coordinates)
    pivot_set = set(pivots)
    result = []
    for free in coordinates:
        if free in pivot_set:
            continue
        functional = {free: Q(1)}
        for row, pivot in zip(rows, pivots):
            coefficient = -row.get(free, Q(0))
            if coefficient:
                functional[pivot] = coefficient
        result.append(functional)
    return result


def insertion_vectors(five_sites, blocks):
    """Span generators e_c^(hole) tensor H_(five_sites minus hole)."""
    result = []
    for hole in five_sites:
        rest = tuple(site for site in five_sites if site != hole)
        cofactor = matching_tensor(rest, blocks)
        for colour in COLOURS:
            vector = {}
            for rest_word, coefficient in cofactor.items():
                assignment = dict(zip(rest, rest_word))
                assignment[hole] = colour
                add(
                    vector,
                    tuple(assignment[site] for site in five_sites),
                    coefficient,
                )
            if vector:
                result.append(vector)
    return result


def cylinder_constraints(cut, blocks):
    five_sites = tuple(site for site in INTERIOR if site != cut)
    five_annihilator = annihilator(insertion_vectors(five_sites, blocks), WORDS5)
    result = []
    for cut_colour in COLOURS:
        for functional in five_annihilator:
            lifted = {}
            for word5, coefficient in functional.items():
                assignment = dict(zip(five_sites, word5))
                assignment[cut] = cut_colour
                lifted[tuple(assignment[site] for site in INTERIOR)] = coefficient
            result.append(lifted)
    return result


def dot(functional, vector):
    return sum(
        coefficient * vector.get(word, Q(0))
        for word, coefficient in functional.items()
    )


def assert_intersection(constraints_by_cut, cuts, expected):
    constraints = [
        row for cut in cuts for row in constraints_by_cut[cut]
    ]
    constraint_rank = len(span_basis(constraints))
    expected_rank = len(span_basis(expected))
    assert 729 - constraint_rank == expected_rank
    assert all(dot(row, vector) == 0 for row in constraints for vector in expected)


def expected_cofactors(t, s):
    data = {
        (0, 1): [((2, 1, 0, 0), t), ((0, 0, 0, 0), s)],
        (0, 2): [((1, 1, 1, 0), 1), ((2, 2, 0, 0), 1)],
        (0, 3): [((1, 0, 1, 0), 1)],
        (0, 4): [((2, 0, 2, 0), 1)],
        (0, 5): [((1, 2, 1, 1), t), ((1, 0, 0, 1), s)],
        (1, 2): [((2, 1, 2, 0), 1)],
        (1, 3): [((1, 1, 0, 0), 1), ((2, 0, 2, 0), 1)],
        (1, 4): [((1, 1, 1, 0), 1)],
        (1, 5): [((2, 2, 1, 2), t), ((2, 0, 0, 2), s)],
        (2, 3): [((0, 0, 0, 0), 1)],
        (2, 4): [((0, 0, 1, 0), 1)],
        (2, 5): [((2, 2, 2, 2), 1)],
        (3, 4): [((0, 0, 0, 0), 1)],
        (3, 5): [((1, 1, 1, 1), 1)],
        (4, 5): [
            ((1, 2, 1, 2), 1),
            ((0, 0, 2, 1), t),
            ((0, 0, 0, 0), s),
        ],
    }
    result = {}
    for pair, terms in data.items():
        cofactor = {}
        for word, coefficient in terms:
            if coefficient:
                add(cofactor, word, Q(coefficient))
        result[pair] = cofactor
    return result


REPRESENTATIVE_COUNTS = {
    (0, 0): (100, 126, {1: 78, 2: 18, 3: 4}),
    (1, 0): (126, 162, {1: 96, 2: 25, 3: 4, 4: 1}),
    (0, 1): (126, 162, {1: 96, 2: 25, 3: 4, 4: 1}),
    (1, 1): (152, 198, {1: 114, 2: 32, 3: 4, 4: 2}),
}


def reconstruct_atoms(t, s, blocks):
    expected = expected_cofactors(t, s)
    atoms = defaultdict(list)
    observed = {}
    for left, right in combinations(INTERIOR, 2):
        rest = tuple(site for site in INTERIOR if site not in (left, right))
        cofactor = {
            word: Q(coefficient)
            for word, coefficient in matching_tensor(rest, blocks).items()
        }
        observed[left, right] = cofactor
        for rest_word, coefficient in cofactor.items():
            for colour_left, colour_right in product(COLOURS, repeat=2):
                assignment = dict(zip(rest, rest_word))
                assignment[left] = colour_left
                assignment[right] = colour_right
                full_word = tuple(assignment[site] for site in INTERIOR)
                atoms[full_word].append(
                    (left, colour_left, right, colour_right, coefficient)
                )
    assert observed == expected
    expected_words, expected_weighted, expected_multiplicities = (
        REPRESENTATIVE_COUNTS[t, s]
    )
    assert len(atoms) == expected_words
    assert sum(map(len, atoms.values())) == expected_weighted
    assert Counter(map(len, atoms.values())) == expected_multiplicities
    assert all((colour,) * 6 in atoms for colour in COLOURS)
    return dict(atoms)


def normal_vectors(t, s, kind):
    moving = {}
    if t:
        moving[U0] = Q(t)
    if s:
        moving[E0] = Q(s)
    uplus = {word: Q(1) for word in UPLUS_WORDS}
    hs = vector_sum(moving, uplus)
    if kind == "line":
        return [hs]
    if kind == "plane":
        return [moving, uplus] if moving else [uplus]
    raise AssertionError(kind)


def audit_cylinders_and_cofactors(t, s):
    blocks = blocks_at(Q(t), Q(s))
    hs = matching_tensor(INTERIOR, blocks)
    assert hs == vector_sum(*normal_vectors(t, s, "line"))

    constraints_by_cut = {
        cut: cylinder_constraints(cut, blocks) for cut in INTERIOR
    }
    plane = normal_vectors(t, s, "plane")
    line = normal_vectors(t, s, "line")
    assert_intersection(constraints_by_cut, (2, 3, 4, 0), plane)
    assert_intersection(constraints_by_cut, (2, 3, 4, 1), plane)
    assert_intersection(constraints_by_cut, (2, 3, 4, 5), line)

    # Each candidate fourth cut has a nonzero pure-diagonal quotient defect.
    for cut in (0, 1, 5):
        five_sites = tuple(site for site in INTERIOR if site != cut)
        insertion = insertion_vectors(five_sites, blocks)
        insertion_basis = span_basis(insertion)
        pure = [unit((colour,) * 5) for colour in COLOURS]
        defect = len(span_basis(insertion + pure)) - len(insertion_basis)
        assert defect > 0

    atoms = reconstruct_atoms(t, s, blocks)
    return blocks, atoms, plane, line


def boundary_value(side, boundary_colour, site, internal_colour):
    offset = 3 * site + internal_colour + 1
    if side == "x":
        return Q(17 * (boundary_colour + 1) + offset, 11)
    return Q(23 * (boundary_colour + 1) + 2 * offset, 13)


def audit_literal_eight_site_expansion(blocks, atoms):
    """Compare the shared-star formula with a fresh eight-site expansion."""
    full_blocks = {
        edge: dict(cells) for edge, cells in blocks.items()
    }
    for site in INTERIOR:
        full_blocks[site, 6] = {
            (internal, boundary): boundary_value(
                "x", boundary, site, internal
            )
            for internal, boundary in product(COLOURS, repeat=2)
        }
        full_blocks[site, 7] = {
            (internal, boundary): boundary_value(
                "y", boundary, site, internal
            )
            for internal, boundary in product(COLOURS, repeat=2)
        }
    full_blocks[6, 7] = {
        (left, right): Q(31 + 5 * left + 7 * right, 17)
        for left, right in product(COLOURS, repeat=2)
    }
    observed8 = matching_tensor(ALL_SITES, full_blocks)
    hs = matching_tensor(INTERIOR, blocks)
    for a, b in product(COLOURS, repeat=2):
        observed = {
            word[:6]: Q(coefficient)
            for word, coefficient in observed8.items()
            if word[6:] == (a, b)
        }
        predicted = {}
        r = full_blocks[6, 7][a, b]
        for word, coefficient in hs.items():
            add(predicted, word, r * coefficient)
        for word, word_atoms in atoms.items():
            for left, colour_left, right, colour_right, coefficient in word_atoms:
                term = coefficient * (
                    boundary_value("x", a, left, colour_left)
                    * boundary_value("y", b, right, colour_right)
                    + boundary_value("x", a, right, colour_right)
                    * boundary_value("y", b, left, colour_left)
                )
                add(predicted, word, term)
        assert observed == predicted


def variable(side, site, internal_colour, boundary_colour):
    # Deliberately different names and order from the primary checker.
    return f"{side}_{site}_{internal_colour}_{boundary_colour}"


def qtext(value):
    value = Q(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def coordinate_polynomial(atoms, a, b, word):
    terms = []
    for left, colour_left, right, colour_right, coefficient in atoms.get(word, ()):
        terms.append(
            qtext(coefficient)
            + "*"
            + variable("x", left, colour_left, a)
            + "*"
            + variable("y", right, colour_right, b)
        )
        terms.append(
            qtext(coefficient)
            + "*"
            + variable("x", right, colour_right, a)
            + "*"
            + variable("y", left, colour_left, b)
        )
    return "+".join(terms) if terms else "0"


def fibre_equations(atoms, normal, a, b, target):
    coordinates = tuple(
        sorted(
            set(atoms)
            | {word for vector in normal for word in vector}
            | {(colour,) * 6 for colour in COLOURS}
        )
    )
    functionals = annihilator(normal, coordinates)
    target_word = (target,) * 6 if target is not None else None
    equations = []
    for functional in functionals:
        parts = []
        for word, coefficient in functional.items():
            parts.append(
                qtext(coefficient)
                + "*("
                + coordinate_polynomial(atoms, a, b, word)
                + ")"
            )
        constant = -functional.get(target_word, Q(0)) if target_word else Q(0)
        if constant:
            parts.append(qtext(constant))
        polynomial = "+".join(parts) if parts else "0"
        assert polynomial != "0"
        equations.append(polynomial)
    return equations


CASES = (
    # t, s, normal, active colours, equations/fibre, components
    (0, 0, "line", (0, 1, 2), 99, (9, 12, 9)),
    (1, 0, "plane", (0, 1, 2), 124, (15, 13, 14)),
    (1, 0, "line", (0, 1, 2), 125, (9, 11, 9)),
    (0, 1, "plane", (1, 2), 124, (13, 10)),
    (0, 1, "line", (0, 1, 2), 125, (31, 11, 9)),
    (1, 1, "plane", (0, 1, 2), 150, (25, 13, 10)),
    (1, 1, "line", (0, 1, 2), 151, (10, 11, 9)),
)


def singular_program(atoms, normal, active_colours, equations_per_fibre):
    variables = [
        variable(side, site, internal, boundary)
        for boundary in active_colours
        for site, internal in product(INTERIOR, COLOURS)
        for side in ("x", "y")
    ]
    assert len(variables) == len(set(variables))
    diagonal = {
        colour: fibre_equations(
            atoms, normal, colour, colour, colour
        )
        for colour in active_colours
    }
    off_diagonal = []
    for a, b in product(active_colours, repeat=2):
        if a != b:
            off_diagonal.extend(fibre_equations(atoms, normal, a, b, None))
    assert all(
        len(diagonal[colour]) == equations_per_fibre
        for colour in active_colours
    )
    assert len(off_diagonal) == (
        len(active_colours) * (len(active_colours) - 1) * equations_per_fibre
    )

    lines = [
        "ring R=0,(" + ",".join(variables) + "),dp;",
        'LIB "primdec.lib";',
    ]
    for colour in active_colours:
        lines.append(
            f"ideal D{colour}=" + ",".join(diagonal[colour]) + ";"
        )
        lines.append(f"list M{colour}=minAssGTZ(D{colour});")
    lines.append("ideal OFF=" + ",".join(off_diagonal) + ";")
    lines.append("int i,j,k,total,units,nonunits; ideal J,G;")
    if len(active_colours) == 3:
        lines.extend(
            [
                "for(i=1;i<=size(M0);i++){",
                " for(j=1;j<=size(M1);j++){",
                "  for(k=1;k<=size(M2);k++){",
                "   total++; J=M0[i]+M1[j]+M2[k]+OFF; G=std(J);",
                "   if(reduce(1,G)==0){units++;}else{nonunits++;}",
                "}}}",
                'print("COMPONENTS"); size(M0); size(M1); size(M2);',
            ]
        )
    else:
        left, right = active_colours
        lines.extend(
            [
                f"for(i=1;i<=size(M{left});i++){{",
                f" for(j=1;j<=size(M{right});j++){{",
                f"  total++; J=M{left}[i]+M{right}[j]+OFF; G=std(J);",
                "  if(reduce(1,G)==0){units++;}else{nonunits++;}",
                "}}",
                f'print("COMPONENTS"); size(M{left}); size(M{right});',
            ]
        )
    lines.extend(
        [
            'print("TOTAL"); total;',
            'print("UNITS"); units;',
            'print("NONUNITS"); nonunits;',
        ]
    )
    return "\n".join(lines) + "\n"


def marker_values(output, marker, count):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    start = lines.index(marker) + 1
    return tuple(int(lines[start + offset]) for offset in range(count))


def run_component_certificate(
    singular, t, s, kind, active_colours, equation_count, expected_components, atoms
):
    normal = normal_vectors(t, s, kind)
    program = singular_program(atoms, normal, active_colours, equation_count)
    completed = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=1200,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    expected_tuples = 1
    for count in expected_components:
        expected_tuples *= count
    assert marker_values(
        completed.stdout, "COMPONENTS", len(expected_components)
    ) == expected_components
    assert marker_values(completed.stdout, "TOTAL", 1) == (expected_tuples,)
    assert marker_values(completed.stdout, "UNITS", 1) == (expected_tuples,)
    assert marker_values(completed.stdout, "NONUNITS", 1) == (0,)
    return expected_tuples


def audit_torus_reduction():
    tau, sigma, a = sp.symbols("tau sigma a", nonzero=True)
    for has_t, has_s in ((False, False), (True, False), (False, True), (True, True)):
        t = tau if has_t else sp.Integer(0)
        s = sigma if has_s else sp.Integer(0)
        g = {
            (site, colour): sp.Integer(1)
            for site in ALL_SITES
            for colour in COLOURS
        }
        if has_t or has_s:
            g[5, 0] = a
            g[4, 0] = 1 / a
            g[2, 0] = 1 / a
            g[3, 1] = 1 / a
        if has_t:
            g[2, 2] = a / tau
        if has_s:
            g[3, 0] = a / sigma

        for left, right, colour_left, colour_right in FIXED_SOURCES:
            assert sp.simplify(
                g[left, colour_left] * g[right, colour_right]
            ) == 1
        if has_t:
            assert sp.simplify(t * g[2, 2] * g[3, 1]) == 1
        if has_s:
            assert sp.simplify(s * g[2, 0] * g[3, 0]) == 1

        for colour in COLOURS:
            internal_product = sp.prod(g[site, colour] for site in INTERIOR)
            g[6, colour] = 1
            g[7, colour] = 1 / internal_product
            assert sp.simplify(
                sp.prod(g[site, colour] for site in ALL_SITES)
            ) == 1

        original = blocks_at(t, s)
        transformed = {}
        for edge, cells in original.items():
            left, right = edge
            transformed[edge] = {
                colours: sp.simplify(
                    weight * g[left, colours[0]] * g[right, colours[1]]
                )
                for colours, weight in cells.items()
            }
        target_rep = blocks_at(int(has_t), int(has_s))
        assert transformed == target_rep

        # Directly test cylinder covariance on every even internal subset.
        for size in (0, 2, 4, 6):
            for sites in combinations(INTERIOR, size):
                before = matching_tensor(sites, original)
                after = matching_tensor(sites, transformed)
                words = set(before) | set(after)
                for word in words:
                    scale = sp.prod(
                        g[site, colour] for site, colour in zip(sites, word)
                    )
                    assert sp.simplify(
                        after.get(word, 0) - scale * before.get(word, 0)
                    ) == 0

    # The five-cell plane locus has a finite-index, hence surjective over C,
    # monomial torus action on each fixed support.
    exponent_matrix = sp.Matrix(
        [
            [1, 1, 0, 0, 0],
            [2, 0, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
        ]
    )
    assert abs(exponent_matrix.det()) == 2

    # Verify that the five independent factors used in that exponent matrix
    # really extend to the stabilizer of all eight fixed cells.  Boundary
    # sites can again restore every coefficient of Delta.
    r0, c0, c2, r1, r2 = sp.symbols("r0 c0 c2 r1 r2", nonzero=True)
    stabilizer = {
        (site, colour): sp.Integer(1)
        for site in ALL_SITES
        for colour in COLOURS
    }
    stabilizer[2, 0] = r0
    stabilizer[3, 1] = r0
    stabilizer[4, 0] = r0
    stabilizer[5, 0] = 1 / r0
    stabilizer[3, 0] = c0
    stabilizer[3, 2] = c2
    stabilizer[1, 2] = 1 / c2
    stabilizer[2, 1] = r1
    stabilizer[0, 1] = 1 / r1
    stabilizer[2, 2] = r2
    for left, right, colour_left, colour_right in FIXED_SOURCES:
        assert sp.simplify(
            stabilizer[left, colour_left]
            * stabilizer[right, colour_right]
        ) == 1
    observed_factors = tuple(
        sp.simplify(stabilizer[2, row] * stabilizer[3, column])
        for row, column in ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1))
    )
    assert observed_factors == (
        r0 * c0,
        r0**2,
        r0 * c2,
        r1 * r0,
        r2 * r0,
    )
    for colour in COLOURS:
        internal_product = sp.prod(
            stabilizer[site, colour] for site in INTERIOR
        )
        stabilizer[6, colour] = 1
        stabilizer[7, colour] = 1 / internal_product
        assert sp.simplify(
            sp.prod(stabilizer[site, colour] for site in ALL_SITES)
        ) == 1


def audit_zero_colour_equivalence(atoms):
    normal = normal_vectors(0, 1, "plane")
    normal_basis = span_basis(normal)
    assert in_span(unit(E0), normal_basis)
    assert not in_span(unit((1,) * 6), normal_basis)
    assert not in_span(unit((2,) * 6), normal_basis)

    coordinates = tuple(
        sorted(
            set(atoms)
            | {word for vector in normal for word in vector}
            | {(colour,) * 6 for colour in COLOURS}
        )
    )
    functionals = annihilator(normal, coordinates)
    assert all(functional.get(E0, Q(0)) == 0 for functional in functionals)

    # Setting p^0=q^0=0 makes every fibre involving boundary colour zero
    # have beta=0, since each term contains one of those factors.  Its only
    # possible target is e_0^6 on fibre 00, annihilated by every row above.
    # This mechanically proves extension of every {1,2}-subsystem solution.
    for a, b in product(COLOURS, repeat=2):
        if 0 not in (a, b):
            continue
        beta_is_zero = a == 0 or b == 0
        assert beta_is_zero
        target = unit(E0) if a == b == 0 else {}
        assert all(dot(functional, target) == 0 for functional in functionals)


def main():
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for this independent audit")

    audit_torus_reduction()
    reconstructed = {}
    for t, s in REPRESENTATIVE_COUNTS:
        blocks, atoms, plane, line = audit_cylinders_and_cofactors(t, s)
        assert in_span(matching_tensor(INTERIOR, blocks), span_basis(plane))
        assert in_span(matching_tensor(INTERIOR, blocks), span_basis(line))
        audit_literal_eight_site_expansion(blocks, atoms)
        reconstructed[t, s] = atoms
    audit_zero_colour_equivalence(reconstructed[0, 1])

    total_tuples = 0
    for t, s, kind, active, equation_count, components in CASES:
        print(
            f"checking stratum {(t, s)} {kind} components {components}",
            flush=True,
        )
        total_tuples += run_component_certificate(
            singular,
            t,
            s,
            kind,
            active,
            equation_count,
            components,
            reconstructed[t, s],
        )
    assert total_tuples == 12032

    print("independent A23=tE21+sE00 obstruction audit: PASS")
    print("endpoint cylinders and four zero/nonzero torus strata: PASS")
    print("cofactor atoms/reachable words 126/100, 162/126, 198/152: PASS")
    print("all 12032 component tuples have exact unit standard basis: PASS")
    print("cuts 2340, 2341, 2345 excluded for every complex (t,s): PASS")


if __name__ == "__main__":
    main()
