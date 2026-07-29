#!/usr/bin/env python3
"""Independent exact audit of the five-cell A_23 plane-locus theorem.

This checker imports no project module.  It reconstructs endpoint-ordered
perfect-matching tensors, insertion-cylinder intersections, the complex torus
normalization, the literal two-boundary-star expansion, the five coordinate
quotients, and five characteristic-zero unit ideals.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
import shutil
import subprocess
import time

import sympy as sp


Q = Fraction
INTERIOR = tuple(range(6))
ALL_SITES = tuple(range(8))
COLOURS = (0, 1, 2)
WORDS5 = tuple(product(COLOURS, repeat=5))
WORDS6 = tuple(product(COLOURS, repeat=6))

# Every cell is endpoint ordered: the first colour belongs to the lower site.
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
CELLS = ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1))
CELL_NAMES = ("x00", "x01", "x02", "x11", "x21")
VARIABLE_PAIRS = ((0, 1), (0, 5), (1, 5), (4, 5))
UPLUS_WORDS = (
    (1, 2, 1, 2, 0, 0),
    (1, 1, 1, 1, 1, 0),
    (2, 2, 0, 2, 2, 0),
)

# name, maximal mask M, mandatory retained bits P, selected colours,
# killed coordinates, projected words, projected atoms, normal dimension,
# number of generated fibre equations.
CLASS_SPECS = (
    ("no_x00", 30, (), (0, 2), 141, 53, 54, 0, 216),
    ("x00_no_x11_no_x21", 7, (), (1, 2), 107, 66, 71, 0, 268),
    ("x00_no_x11_with_x21", 23, (0, 4), (1, 2), 72, 127, 153, 1, 504),
    ("x00_x11_no_x21", 15, (0, 3), (1, 2), 71, 123, 156, 2, 484),
    ("x00_x11_with_x21", 31, (0, 3, 4), (1, 2), 71, 149, 192, 2, 588),
)


def add(container, key, value):
    value = Q(value)
    total = container.get(key, Q(0)) + value
    if total:
        container[key] = total
    else:
        container.pop(key, None)


def vector_sum(*vectors):
    answer = {}
    for vector in vectors:
        for word, coefficient in vector.items():
            add(answer, word, coefficient)
    return answer


def subtract(left, right):
    answer = dict(left)
    for word, coefficient in right.items():
        add(answer, word, -coefficient)
    return answer


def unit(word):
    return {word: Q(1)}


def support(mask):
    return tuple(cell for bit, cell in enumerate(CELLS) if mask & (1 << bit))


def blocks_for_mask(mask):
    blocks = {}
    for left, right, colour_left, colour_right in FIXED_SOURCES:
        blocks.setdefault((left, right), {})[colour_left, colour_right] = Q(1)
    blocks[2, 3] = {cell: Q(1) for cell in support(mask)}
    return blocks


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        mate = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, mate),) + tail)
    return tuple(answer)


def matching_tensor(vertices, blocks):
    vertices = tuple(vertices)
    position = {site: index for index, site in enumerate(vertices)}
    answer = {}
    for matching in perfect_matchings(vertices):
        choices = [tuple(blocks.get(edge, {}).items()) for edge in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = Q(1)
            for (left, right), ((colour_left, colour_right), weight) in zip(
                matching, selected
            ):
                word[position[left]] = colour_left
                word[position[right]] = colour_right
                coefficient *= weight
            add(answer, tuple(word), coefficient)
    return answer


def span_basis(vectors):
    """Sparse exact echelon basis keyed by lexicographically first pivots."""
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
    remainder = {key: Q(value) for key, value in vector.items() if value}
    while remainder:
        pivot = min(remainder)
        if pivot not in basis:
            return False
        multiple = remainder[pivot]
        for key, value in basis[pivot].items():
            updated = remainder.get(key, Q(0)) - multiple * value
            if updated:
                remainder[key] = updated
            else:
                remainder.pop(key, None)
    return True


def same_span(left, right):
    left_basis = span_basis(left)
    right_basis = span_basis(right)
    return (
        len(left_basis) == len(right_basis)
        and all(in_span(vector, left_basis) for vector in right)
        and all(in_span(vector, right_basis) for vector in left)
    )


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
    rows, pivots = rref(vectors, coordinates)
    pivot_set = set(pivots)
    answer = []
    for free in coordinates:
        if free in pivot_set:
            continue
        functional = {free: Q(1)}
        for row, pivot in zip(rows, pivots):
            coefficient = -row.get(free, Q(0))
            if coefficient:
                functional[pivot] = coefficient
        answer.append(functional)
    return answer


def dot(functional, vector):
    return sum(
        coefficient * vector.get(word, Q(0))
        for word, coefficient in functional.items()
    )


def insertion_vectors(five_sites, blocks):
    answer = []
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
                answer.append(vector)
    return answer


def cylinder_constraints(cut, blocks):
    five_sites = tuple(site for site in INTERIOR if site != cut)
    five_dual = annihilator(insertion_vectors(five_sites, blocks), WORDS5)
    answer = []
    for cut_colour in COLOURS:
        for functional in five_dual:
            lifted = {}
            for word5, coefficient in functional.items():
                assignment = dict(zip(five_sites, word5))
                assignment[cut] = cut_colour
                lifted[tuple(assignment[site] for site in INTERIOR)] = coefficient
            answer.append(lifted)
    return answer


def assert_intersection(constraints, cuts, expected):
    equations = [row for cut in cuts for row in constraints[cut]]
    rank = len(span_basis(equations))
    expected_rank = len(span_basis(expected))
    assert len(WORDS6) - rank == expected_rank
    assert all(dot(row, vector) == 0 for row in equations for vector in expected)


def normal_vectors(mask):
    zero = matching_tensor(INTERIOR, blocks_for_mask(0))
    hs = matching_tensor(INTERIOR, blocks_for_mask(mask))
    moving = subtract(hs, zero)
    plane = [moving, zero] if moving else [zero]
    return hs, moving, zero, plane, [hs]


def audit_cylinders():
    expected_uplus = {word: Q(1) for word in UPLUS_WORDS}
    for mask in range(32):
        blocks = blocks_for_mask(mask)
        hs, moving, uplus, plane, line = normal_vectors(mask)
        assert uplus == expected_uplus
        expected_moving = {
            (0, 0, colour_left, colour_right, 0, 0): Q(1)
            for colour_left, colour_right in support(mask)
        }
        assert moving == expected_moving
        assert hs == vector_sum(moving, uplus)
        constraints = {
            cut: cylinder_constraints(cut, blocks) for cut in INTERIOR
        }
        assert_intersection(constraints, (2, 3, 4, 0), plane)
        assert_intersection(constraints, (2, 3, 4, 1), plane)
        assert_intersection(constraints, (2, 3, 4, 5), line)
        assert in_span(hs, span_basis(plane))
        assert in_span(hs, span_basis(line))


def audit_torus_and_discrete_stabilizer():
    exponent = sp.Matrix(
        [
            [1, 1, 0, 0, 0],
            [2, 0, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
        ]
    )
    assert abs(exponent.det()) == 2

    # The explicit inverse is: choose r0 with r0^2=y01, then divide the
    # other desired cell factors by r0.  Such an r0 exists for every
    # y01 in C*; this proves surjectivity over C, not merely finite index.
    r0, c0, c2, r1, r2 = sp.symbols("r0 c0 c2 r1 r2", nonzero=True)
    g = {
        (site, colour): sp.Integer(1)
        for site in ALL_SITES
        for colour in COLOURS
    }
    g[2, 0] = g[3, 1] = g[4, 0] = r0
    g[5, 0] = 1 / r0
    g[3, 0] = c0
    g[3, 2] = c2
    g[2, 1] = r1
    g[2, 2] = r2
    g[0, 1] = 1 / r1
    g[1, 2] = 1 / c2
    for left, right, colour_left, colour_right in FIXED_SOURCES:
        assert sp.simplify(g[left, colour_left] * g[right, colour_right]) == 1
    factors = tuple(
        sp.simplify(g[2, left] * g[3, right]) for left, right in CELLS
    )
    assert factors == (r0 * c0, r0**2, r0 * c2, r0 * r1, r0 * r2)
    for colour in COLOURS:
        g[6, colour] = 1
        g[7, colour] = 1 / sp.prod(g[site, colour] for site in INTERIOR)
        assert sp.simplify(sp.prod(g[site, colour] for site in ALL_SITES)) == 1

    fixed_set = set(FIXED_SOURCES)
    locus = set(CELLS)
    stabilizers = []
    for site_permutation in permutations(INTERIOR):
        for colour_permutation in permutations(COLOURS):
            image = set()
            for left, right, colour_left, colour_right in FIXED_SOURCES:
                new_left, new_right = site_permutation[left], site_permutation[right]
                new_cleft = colour_permutation[colour_left]
                new_cright = colour_permutation[colour_right]
                if new_left > new_right:
                    new_left, new_right = new_right, new_left
                    new_cleft, new_cright = new_cright, new_cleft
                image.add((new_left, new_right, new_cleft, new_cright))
            if image != fixed_set:
                continue
            left, right = site_permutation[2], site_permutation[3]
            reversed_edge = left > right
            if reversed_edge:
                left, right = right, left
            if (left, right) != (2, 3):
                continue
            locus_image = {
                (colour_permutation[right_colour], colour_permutation[left_colour])
                if reversed_edge
                else (colour_permutation[left_colour], colour_permutation[right_colour])
                for left_colour, right_colour in CELLS
            }
            if locus_image == locus:
                stabilizers.append((site_permutation, colour_permutation))
    assert stabilizers == [(INTERIOR, COLOURS)]


def cofactor_atoms(mask):
    blocks = blocks_for_mask(mask)
    atoms = defaultdict(list)
    cofactors = {}
    for left, right in combinations(INTERIOR, 2):
        rest = tuple(site for site in INTERIOR if site not in (left, right))
        cofactor = matching_tensor(rest, blocks)
        cofactors[left, right] = cofactor
        for rest_word, coefficient in cofactor.items():
            for colour_left, colour_right in product(COLOURS, repeat=2):
                assignment = dict(zip(rest, rest_word))
                assignment[left] = colour_left
                assignment[right] = colour_right
                full_word = tuple(assignment[site] for site in INTERIOR)
                atoms[full_word].append(
                    (left, colour_left, right, colour_right, Q(coefficient))
                )
    return dict(atoms), cofactors


def variable_coordinate_block(bit):
    zero_cofactors = cofactor_atoms(0)[1]
    one_cofactors = cofactor_atoms(1 << bit)[1]
    coordinates = set()
    changed = []
    for pair in combinations(INTERIOR, 2):
        variable = subtract(one_cofactors[pair], zero_cofactors[pair])
        if not variable:
            continue
        changed.append(pair)
        left, right = pair
        rest = tuple(site for site in INTERIOR if site not in pair)
        for rest_word in variable:
            for colour_left, colour_right in product(COLOURS, repeat=2):
                assignment = dict(zip(rest, rest_word))
                assignment[left] = colour_left
                assignment[right] = colour_right
                coordinates.add(tuple(assignment[site] for site in INTERIOR))
    assert tuple(changed) == VARIABLE_PAIRS
    return coordinates


def audit_literal_boundary_identity():
    x = {
        (a, site, colour): Q(11 + 101 * a + 7 * site + colour, 17)
        for a, site, colour in product(COLOURS, INTERIOR, COLOURS)
    }
    y = {
        (b, site, colour): Q(401 + 103 * b + 11 * site + colour, 19)
        for b, site, colour in product(COLOURS, INTERIOR, COLOURS)
    }
    r = {
        (a, b): Q(907 + 13 * a + 17 * b, 23)
        for a, b in product(COLOURS, repeat=2)
    }
    targets = {(colour,) * 6 for colour in COLOURS}
    for mask in range(32):
        internal = blocks_for_mask(mask)
        atoms, _ = cofactor_atoms(mask)
        assert targets <= set(atoms)
        blocks = {edge: dict(cells) for edge, cells in internal.items()}
        for site in INTERIOR:
            blocks[site, 6] = {
                (internal_colour, boundary_colour): x[
                    boundary_colour, site, internal_colour
                ]
                for internal_colour, boundary_colour in product(COLOURS, repeat=2)
            }
            blocks[site, 7] = {
                (internal_colour, boundary_colour): y[
                    boundary_colour, site, internal_colour
                ]
                for internal_colour, boundary_colour in product(COLOURS, repeat=2)
            }
        blocks[6, 7] = dict(r)
        observed8 = matching_tensor(ALL_SITES, blocks)
        hs = matching_tensor(INTERIOR, internal)
        for a, b in product(COLOURS, repeat=2):
            observed = {
                word[:6]: Q(coefficient)
                for word, coefficient in observed8.items()
                if word[6:] == (a, b)
            }
            predicted = {}
            for word, coefficient in hs.items():
                add(predicted, word, r[a, b] * coefficient)
            for word, word_atoms in atoms.items():
                for left, colour_left, right, colour_right, coefficient in word_atoms:
                    add(
                        predicted,
                        word,
                        coefficient
                        * (
                            x[a, left, colour_left] * y[b, right, colour_right]
                            + x[a, right, colour_right] * y[b, left, colour_left]
                        ),
                    )
            assert observed == predicted


def class_name(mask):
    if not mask & 1:
        return "no_x00"
    has_x11 = bool(mask & (1 << 3))
    has_x21 = bool(mask & (1 << 4))
    if not has_x11:
        return "x00_no_x11_with_x21" if has_x21 else "x00_no_x11_no_x21"
    return "x00_x11_with_x21" if has_x21 else "x00_x11_no_x21"


def project_vector(vector, killed):
    return {word: coefficient for word, coefficient in vector.items() if word not in killed}


def quotient_for_spec(spec, cell_blocks):
    name, maximal, retained, colours, *_ = spec
    killed = set()
    for bit in range(5):
        if maximal & (1 << bit):
            killed.update(cell_blocks[bit])
    killed.update(UPLUS_WORDS)
    for bit in retained:
        killed.difference_update(cell_blocks[bit])
    atoms, _ = cofactor_atoms(maximal)
    projected_atoms = {
        word: tuple(terms) for word, terms in atoms.items() if word not in killed
    }
    hs, moving, uplus, _, _ = normal_vectors(maximal)
    projected_normal = [
        vector
        for vector in (
            project_vector(moving, killed),
            project_vector(uplus, killed),
        )
        if vector
    ]
    return killed, projected_atoms, projected_normal


def variable(side, boundary, site, colour):
    # Deliberately differs from the primary checker's variable ordering.
    return f"{side}{site}{colour}{boundary}"


def qtext(value):
    value = Q(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def coordinate_polynomial(atoms, a, b, word):
    terms = []
    for left, colour_left, right, colour_right, coefficient in atoms.get(word, ()):
        factor = qtext(coefficient)
        terms.append(
            factor
            + "*"
            + variable("x", a, left, colour_left)
            + "*"
            + variable("y", b, right, colour_right)
        )
        terms.append(
            factor
            + "*"
            + variable("x", a, right, colour_right)
            + "*"
            + variable("y", b, left, colour_left)
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
    equations = []
    target_word = (target,) * 6 if target is not None else None
    for functional in annihilator(normal, coordinates):
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
        equations.append("+".join(parts) if parts else "0")
    return equations


def singular_program(atoms, normal, active):
    variables = [
        variable(side, boundary, site, colour)
        for boundary in active
        for site, colour in product(INTERIOR, COLOURS)
        for side in ("x", "y")
    ]
    assert len(variables) == len(set(variables)) == 72
    generators = []
    for a, b in product(active, repeat=2):
        generators.extend(
            fibre_equations(atoms, normal, a, b, a if a == b else None)
        )
    lines = [
        "ring R=0,(" + ",".join(variables) + "),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(generators) + ";",
        "ideal G=std(I);",
        'print("UNIT"); if(reduce(1,G)==0){1;}else{0;}',
        'print("GBSIZE"); size(G);',
    ]
    return "\n".join(lines) + "\n", len(generators)


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def audit_quotients_and_build_programs():
    cell_blocks = [variable_coordinate_block(bit) for bit in range(5)]
    assert all(len(block) == 35 for block in cell_blocks)
    assert all(
        left.isdisjoint(right) for left, right in combinations(cell_blocks, 2)
    )
    assert len(set().union(*cell_blocks)) == 175

    members = {spec[0]: [] for spec in CLASS_SPECS}
    for mask in range(32):
        members[class_name(mask)].append(mask)
    assert sorted(mask for masks in members.values() for mask in masks) == list(range(32))
    assert tuple(len(members[spec[0]]) for spec in CLASS_SPECS) == (16, 4, 4, 4, 4)

    programs = {}
    for spec in CLASS_SPECS:
        (
            name,
            maximal,
            retained,
            active,
            killed_count,
            word_count,
            atom_count,
            normal_dimension,
            generator_count,
        ) = spec
        killed, projected_atoms, projected_normal = quotient_for_spec(spec, cell_blocks)
        assert len(killed) == killed_count
        assert len(projected_atoms) == word_count
        assert sum(map(len, projected_atoms.values())) == atom_count
        assert len(span_basis(projected_normal)) == normal_dimension

        for mask in members[name]:
            assert mask & maximal == mask
            assert all(mask & (1 << bit) for bit in retained)
            atoms, _ = cofactor_atoms(mask)
            observed_atoms = {
                word: tuple(terms) for word, terms in atoms.items() if word not in killed
            }
            assert observed_atoms == projected_atoms
            _, moving, uplus, _, _ = normal_vectors(mask)
            observed_normal = [
                vector
                for vector in (
                    project_vector(moving, killed),
                    project_vector(uplus, killed),
                )
                if vector
            ]
            assert same_span(observed_normal, projected_normal)

        normal_basis = span_basis(projected_normal)
        for colour in active:
            target = (colour,) * 6
            assert target not in killed
            assert not in_span(unit(target), normal_basis)

        program, observed_generators = singular_program(
            projected_atoms, projected_normal, active
        )
        assert observed_generators == generator_count
        programs[name] = program
    return programs


def audit_unit_ideals(programs):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for the independent exact-Q audit")
    elapsed = {}
    for name, program in programs.items():
        started = time.monotonic()
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
        assert marker(completed.stdout, "UNIT") == 1
        assert marker(completed.stdout, "GBSIZE") == 1
        elapsed[name] = time.monotonic() - started
    return elapsed


def main():
    audit_torus_and_discrete_stabilizer()
    audit_cylinders()
    audit_literal_boundary_identity()
    programs = audit_quotients_and_build_programs()
    elapsed = audit_unit_ideals(programs)
    print("independent full five-cell A23 plane-locus audit: PASS")
    print("32 complex support orbits and identity site/global-colour stabilizer: PASS")
    print("all 96 four-cut cylinder intersections reconstructed over Q: PASS")
    print("all nine shared-star fibres and arbitrary direct 67 absorption: PASS")
    print("five disjoint 35-coordinate blocks and five support classes: PASS")
    for spec in CLASS_SPECS:
        name, *_, generators = spec
        print(f"{name}: {generators} generators, exact-Q unit ({elapsed[name]:.3f}s): PASS")


if __name__ == "__main__":
    main()
