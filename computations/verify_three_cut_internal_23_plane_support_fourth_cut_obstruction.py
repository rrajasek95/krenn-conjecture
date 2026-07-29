#!/usr/bin/env python3
"""Exact Q/C obstruction for the full five-cell A_23 plane-normal locus.

The block on 23 may have arbitrary complex support in

    L = {(0,0), (0,1), (0,2), (1,1), (2,1)}.

An invertible fixed-cell-preserving colour torus reduces this to 32 support
orbits.  Rather than run 32 unrelated eliminations, pairwise-disjoint output
blocks for the five cells give five parameter-independent quotient classes.
For each class a necessary two-colour shared-star subsystem has unit ideal
over Q.  The script also reconstructs every cylinder and checks quotient
invariance for all 32 representatives.
"""

from __future__ import annotations

import itertools
import shutil
import subprocess
import time

import sympy as sp

import explore_three_cut_internal_23_perturbation as equations
import explore_three_cut_internal_23_plane_supports as supports
import explore_three_cut_internal_23_universal_projection as projection
import test_three_cut_internal_23_plane_support_component as worker


Q = equations.Q
SIX = equations.SIX
COLOURS = equations.COLOURS


# (name, maximal mask, variable cell blocks retained, necessary colours,
#  expected killed coordinates, projected words, projected atoms,
#  projected plane-normal dimension, generator count)
CLASS_SPECS = (
    ("no_x00", 30, (), (0, 2), 141, 53, 54, 0, 216),
    ("x00_no_x11_no_x21", 7, (), (1, 2), 107, 66, 71, 0, 268),
    ("x00_no_x11_with_x21", 23, (0, 4), (1, 2), 72, 127, 153, 1, 504),
    ("x00_x11_no_x21", 15, (0, 3), (1, 2), 71, 123, 156, 2, 484),
    ("x00_x11_with_x21", 31, (0, 3, 4), (1, 2), 71, 149, 192, 2, 588),
)


def class_name(mask: int) -> str:
    x00 = bool(mask & (1 << 0))
    x11 = bool(mask & (1 << 3))
    x21 = bool(mask & (1 << 4))
    if not x00:
        return "no_x00"
    if not x11:
        return "x00_no_x11_with_x21" if x21 else "x00_no_x11_no_x21"
    return "x00_x11_with_x21" if x21 else "x00_x11_no_x21"


def audit_torus_and_discrete_symmetry():
    exponent_matrix = sp.Matrix([
        [1, 1, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ])
    assert abs(exponent_matrix.det()) == 2

    # The five free factors really extend to a stabilizer of all eight fixed
    # cells.  Check this symbolically, then compensate at sites 6,7 so every
    # diagonal target coefficient is exactly fixed.
    r0, c0, c2, r1, r2 = sp.symbols("r0 c0 c2 r1 r2", nonzero=True)
    g = {(site, colour): sp.Integer(1) for site in range(8) for colour in COLOURS}
    g[2, 0], g[3, 1], g[5, 0], g[4, 0] = r0, r0, 1 / r0, r0
    g[3, 0], g[3, 2], g[2, 1], g[2, 2] = c0, c2, r1, r2
    g[0, 1], g[1, 2] = 1 / r1, 1 / c2
    fixed = (
        (0, 1, 0, 0), (4, 5, 0, 0), (0, 2, 1, 1),
        (1, 4, 1, 1), (0, 4, 2, 2), (1, 3, 2, 2),
        (2, 5, 0, 0), (3, 5, 1, 0),
    )
    assert all(sp.simplify(g[i, a] * g[j, b]) == 1 for i, j, a, b in fixed)
    factors = tuple(sp.simplify(g[2, a] * g[3, b]) for a, b in supports.CELLS)
    assert factors == (r0 * c0, r0**2, r0 * c2, r0 * r1, r0 * r2)
    for colour in COLOURS:
        g[6, colour] = 1
        g[7, colour] = 1 / sp.prod(g[site, colour] for site in SIX)
        assert sp.simplify(sp.prod(g[site, colour] for site in range(8))) == 1

    # There is no further site/global-colour permutation collapse hidden in
    # the 32 supports.  The identity is the complete stabilizer of both the
    # fixed cells and the oriented L block.
    fixed_set = set(fixed)
    locus = set(supports.CELLS)
    stabilizers = []
    for site_permutation in itertools.permutations(SIX):
        for colour_permutation in itertools.permutations(COLOURS):
            image = set()
            for i, j, a, b in fixed:
                ii, jj = site_permutation[i], site_permutation[j]
                aa, bb = colour_permutation[a], colour_permutation[b]
                if ii > jj:
                    ii, jj, aa, bb = jj, ii, bb, aa
                image.add((ii, jj, aa, bb))
            if image != fixed_set:
                continue
            ii, jj = site_permutation[2], site_permutation[3]
            reverse = ii > jj
            if reverse:
                ii, jj = jj, ii
            if (ii, jj) != (2, 3):
                continue
            locus_image = {
                (colour_permutation[b], colour_permutation[a]) if reverse
                else (colour_permutation[a], colour_permutation[b])
                for a, b in locus
            }
            if locus_image == locus:
                stabilizers.append((site_permutation, colour_permutation))
    assert stabilizers == [(SIX, COLOURS)]


def projected_terms_for_mask(mask, killed):
    actual = equations.reconstruct_word_terms(supports.blocks_for_mask(mask))
    return {word: tuple(terms) for word, terms in actual.items() if word not in killed}


def projected_plane_basis(mask, killed):
    blocks = supports.blocks_for_mask(mask)
    hs = equations.cylinders.matching_tensor(SIX, blocks)
    uplus = equations.cylinders.matching_tensor(SIX, supports.blocks_for_mask(0))
    moving = projection.subtract(hs, uplus)
    basis = [projection.project_vector(vector, killed) for vector in (moving, uplus)]
    return [vector for vector in basis if vector]


def audit_cell_blocks():
    blocks = []
    for bit in range(5):
        coordinates, details = projection.variable_coordinate_span(1 << bit)
        assert len(coordinates) == 35
        assert tuple(details) == projection.VARIABLE_PAIRS
        assert all(len(tensor) == 1 for tensor in details.values())
        blocks.append(coordinates)
    for left, right in itertools.combinations(blocks, 2):
        assert left.isdisjoint(right)
    assert len(set().union(*blocks)) == 175


def audit_literal_boundary_identity():
    """Compare (9) with direct eight-site matching enumeration on all masks."""
    p = {
        (a, i, c): Q(1 + 100 * a + 10 * i + c)
        for a in COLOURS for i in SIX for c in COLOURS
    }
    q = {
        (b, i, c): Q(701 + 100 * b + 10 * i + c)
        for b in COLOURS for i in SIX for c in COLOURS
    }
    r = {(a, b): Q(1301 + 10 * a + b) for a in COLOURS for b in COLOURS}

    for mask in range(32):
        internal = supports.blocks_for_mask(mask)
        blocks = {edge: dict(block) for edge, block in internal.items()}
        for i in SIX:
            blocks[i, 6] = {
                (c, a): value for (a, site, c), value in p.items() if site == i
            }
            blocks[i, 7] = {
                (c, b): value for (b, site, c), value in q.items() if site == i
            }
        blocks[6, 7] = dict(r)
        full = equations.cylinders.matching_tensor(tuple(range(8)), blocks)
        hs = equations.cylinders.matching_tensor(SIX, internal)
        word_terms = equations.reconstruct_word_terms(internal)
        for a, b in itertools.product(COLOURS, repeat=2):
            observed = {
                word[:6]: coefficient
                for word, coefficient in full.items()
                if word[6:] == (a, b)
            }
            expected = {}
            for word, coefficient in hs.items():
                equations.cylinders.add(expected, word, r[a, b] * coefficient)
            for word, terms in word_terms.items():
                value = Q(0)
                for ((i, c), (j, d)), coefficient in terms:
                    value += coefficient * (
                        p[a, i, c] * q[b, j, d]
                        + p[a, j, d] * q[b, i, c]
                    )
                equations.cylinders.add(expected, word, value)
            assert observed == expected


def audit_cylinders_and_class_invariance():
    specs = {spec[0]: spec for spec in CLASS_SPECS}
    class_members = {name: [] for name in specs}
    zero_blocks = supports.blocks_for_mask(0)
    uplus = equations.cylinders.matching_tensor(SIX, zero_blocks)

    for mask in range(32):
        name = class_name(mask)
        class_members[name].append(mask)
        blocks = supports.blocks_for_mask(mask)
        hs = equations.cylinders.matching_tensor(SIX, blocks)
        moving = projection.subtract(hs, uplus)
        plane = [moving, uplus] if moving else [uplus]
        line = [hs]
        for cut in (0, 1):
            observed = equations.cylinders.cylinder_intersection((2, 3, 4, cut), blocks)
            assert equations.same_span(observed, plane)
        observed = equations.cylinders.cylinder_intersection((2, 3, 4, 5), blocks)
        assert equations.same_span(observed, line)
        plane_span = equations.cylinders.echelon(plane)
        assert equations.cylinders.member(hs, plane_span)
        assert equations.cylinders.member(hs, equations.cylinders.echelon(line))

    assert sorted(itertools.chain.from_iterable(class_members.values())) == list(range(32))
    assert tuple(map(len, class_members.values())) == (16, 4, 4, 4, 4)

    problems = {}
    for spec in CLASS_SPECS:
        name, maximal, retained, colours, killed_count, words, atoms, normal_dim, generators = spec
        projected, killed, details, basis = projection.projected_problem(
            maximal, preserve_cells=retained, normal="plane"
        )
        assert len(killed) == killed_count
        assert len(projected) == words
        assert sum(map(len, projected.values())) == atoms
        assert len(equations.cylinders.echelon(basis)) == normal_dim
        assert tuple(details) == projection.VARIABLE_PAIRS

        representative_terms = {word: tuple(terms) for word, terms in projected.items()}
        for mask in class_members[name]:
            assert mask & maximal == mask
            assert all(mask & (1 << bit) for bit in retained)
            assert projected_terms_for_mask(mask, killed) == representative_terms
            assert equations.same_span(projected_plane_basis(mask, killed), basis)

        normal_span = equations.cylinders.echelon(basis)
        for colour in colours:
            word = (colour,) * 6
            assert word not in killed
            assert not equations.cylinders.member({word: Q(1)}, normal_span)

        program, observed_generators = worker.direct_program(
            projected, basis, colours, characteristic=0
        )
        assert observed_generators == generators
        # Two diagonal target fibres and both ordered off-diagonal fibres are
        # present.  A full 108-star-variable solution necessarily restricts
        # to these 72 variables, so this is a valid necessary subsystem.
        names = {
            equations.variable(kind, boundary, endpoint)
            for kind in ("p", "q")
            for boundary in colours
            for endpoint in itertools.product(SIX, COLOURS)
        }
        assert len(names) == 72
        problems[name] = (program, generators)
    return problems


def exact_unit_tests(problems):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for the exact Q audit")
    results = {}
    for name, (program, generators) in problems.items():
        started = time.monotonic()
        completed = subprocess.run(
            [singular, "-q"], input=program, text=True, capture_output=True,
            check=True, timeout=1200,
        )
        if completed.stderr.strip():
            raise AssertionError(completed.stderr)
        assert worker.marker_values(completed.stdout, "UNIT", 1) == (1,)
        assert worker.marker_values(completed.stdout, "GBSIZE", 1) == (1,)
        results[name] = (generators, time.monotonic() - started)
    return results


def main():
    audit_torus_and_discrete_symmetry()
    audit_cell_blocks()
    audit_literal_boundary_identity()
    problems = audit_cylinders_and_class_invariance()
    results = exact_unit_tests(problems)
    print("full five-cell A23 plane-locus fourth-cut obstruction: PASS")
    print("32 complex support orbits and identity discrete stabilizer: PASS")
    print("all cuts 2340/2341 plane normals and 2345 line normals: PASS")
    for name, (generators, elapsed) in results.items():
        print(f"{name}: {generators} exact-Q generators, unit ideal ({elapsed:.3f}s): PASS")
    print("all 108 shared-star entries, ordered cross fibres, and arbitrary A67: PASS")


if __name__ == "__main__":
    main()
