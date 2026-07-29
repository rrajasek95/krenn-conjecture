#!/usr/bin/env python3
"""Exact fixed-interior theorem for arbitrary A_23 and A_25=E_00+tE_11.

For t=0 this invokes the scope of the independently audited arbitrary-A_23
theorem.  For t!=0, a sixth independent stabilizer character normalizes t
to one.  The 512 A_23 supports split into the old five-cell locus (32 masks,
five quotient classes) and its complement (480 masks, 27 finite retained
charts and one Q[lambda] chart).  Every necessary shared-star ideal is a
unit over Q.
"""

from __future__ import annotations

import collections
import concurrent.futures
import itertools
import shutil
import subprocess
import time

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_adjacent_25_11_x12_crossratio_symbolic as symbolic
import test_three_cut_internal_23_plane_support_component as worker
import verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction as old_full
import verify_three_cut_internal_23_plane_support_fourth_cut_obstruction as old_locus


Q = full.Q
ACTIVE = (1, 2)
LOCAL_TO_FULL = (0, 1, 2, 4, 7)


OUTSIDE_GENERATORS = {
    "x10": {
        (0, 0): 380, (0, 1): 484,
        (2, 0): 432, (2, 1): 536,
        (4, 0): 492, (4, 1): 596,
        (6, 0): 544, (6, 1): 648,
    },
    "x12": {
        (0, 0): 384, (0, 1): 488,
        (2, 0): 436, (2, 1): 540,
        (4, 0): 496, (4, 1): 600,
        (6, 0): 548,
    },
    "x20": {
        (0, 0): 440, (0, 1): 544,
        (2, 0): 492, (2, 1): 596,
        (4, 0): 552, (4, 1): 656,
        (6, 0): 604, (6, 1): 708,
    },
    "x22": {
        (4, 0): 496, (4, 1): 600,
        (6, 0): 548, (6, 1): 652,
    },
}


OLD_CLASS_EXPECTED = {
    "no_x00": (16, 1, 141, 73, 292),
    "x00_no_x11_no_x21": (4, 1, 107, 94, 376),
    "x00_no_x11_with_x21": (4, 2, 72, 155, 612),
    "x00_x11_no_x21": (4, 3, 71, 143, 560),
    "x00_x11_with_x21": (4, 3, 71, 169, 664),
}


def audit_torus_supports_and_coordinate_blocks():
    _constraints, x_rows, t_row = adjacent.stabilizer_audit()
    assert x_rows.rank() == 5
    assert sp.Matrix.vstack(x_rows, t_row).rank() == 6

    # Full-support orbit dimensions are recorded honestly.  Coordinate
    # quotients, not a false finite-orbit claim, remove all but one modulus.
    moduli = collections.Counter()
    ranks = collections.Counter()
    for mask in range(1 << 9):
        rows = [
            x_rows.row(bit) for bit in range(9) if mask & (1 << bit)
        ]
        rank = sp.Matrix.vstack(*rows).rank() if rows else 0
        ranks[rank] += 1
        moduli[mask.bit_count() - rank] += 1
    assert dict(sorted(moduli.items())) == {
        0: 328, 1: 132, 2: 42, 3: 9, 4: 1,
    }
    assert dict(sorted(ranks.items())) == {
        0: 1, 1: 9, 2: 36, 3: 93, 4: 168, 5: 205,
    }

    # An explicit six-character effective action.  The other stabilizer
    # characters act only on coordinates that remain arbitrary.
    r0, c0, c2, r1, r2, tau = sp.symbols(
        "r0 c0 c2 r1 r2 tau", nonzero=True
    )
    g = {
        (site, colour): sp.Integer(1)
        for site in range(8) for colour in full.COLOURS
    }
    g[2, 0], g[3, 1], g[5, 0], g[4, 0] = r0, r0, 1 / r0, r0
    g[3, 0], g[3, 2], g[2, 1], g[2, 2] = c0, c2, r1, r2
    g[0, 1], g[1, 2] = 1 / r1, 1 / c2
    g[5, 1] = tau / r1
    fixed = (
        (0, 1, 0, 0), (4, 5, 0, 0), (0, 2, 1, 1),
        (1, 4, 1, 1), (0, 4, 2, 2), (1, 3, 2, 2),
        (2, 5, 0, 0), (3, 5, 1, 0),
    )
    assert all(
        sp.simplify(g[i, a] * g[j, b]) == 1
        for i, j, a, b in fixed
    )
    factors = tuple(
        sp.simplify(g[2, a] * g[3, b]) for a, b in full.CELLS
    )
    assert factors == (
        r0*c0, r0**2, r0*c2,
        r1*c0, r1*r0, r1*c2,
        r2*c0, r2*r0, r2*c2,
    )
    assert sp.simplify(g[2, 1] * g[5, 1]) == tau
    for colour in full.COLOURS:
        g[6, colour] = 1
        g[7, colour] = 1 / sp.prod(
            g[site, colour] for site in full.SIX
        )
        assert sp.simplify(
            sp.prod(g[site, colour] for site in range(8))
        ) == 1

    adjacent.no_mixed_x_t_terms()
    assert tuple(len(block) for block in adjacent.X_BLOCKS) == (35,) * 9
    assert len(adjacent.T_BLOCK) == 35
    assert tuple(adjacent.T_DETAILS) == ((0, 3), (0, 4), (1, 3), (3, 4))
    assert tuple(
        len(adjacent.T_BLOCK & block) for block in adjacent.X_BLOCKS
    ) == (0, 0, 0, 9, 9, 9, 0, 0, 0)
    assert not adjacent.T_BLOCK & set(full.UPLUS)
    targets = tuple((colour,) * 6 for colour in full.COLOURS)
    assert tuple(word in adjacent.T_BLOCK for word in targets) == (
        False, True, False,
    )


def audit_literal_boundary_identity():
    coefficients = {
        cell: Q(2001 + bit) for bit, cell in enumerate(full.CELLS)
    }
    internal = adjacent.blocks_for(coefficients, Q(2501))
    p = {
        (a, i, c): Q(1 + 100*a + 10*i + c)
        for a in full.COLOURS for i in full.SIX for c in full.COLOURS
    }
    q = {
        (b, i, c): Q(701 + 100*b + 10*i + c)
        for b in full.COLOURS for i in full.SIX for c in full.COLOURS
    }
    r = {
        (a, b): Q(1301 + 10*a + b)
        for a in full.COLOURS for b in full.COLOURS
    }
    blocks = {edge: dict(block) for edge, block in internal.items()}
    for i in full.SIX:
        blocks[i, 6] = {
            (c, a): p[a, i, c]
            for c in full.COLOURS for a in full.COLOURS
        }
        blocks[i, 7] = {
            (c, b): q[b, i, c]
            for c in full.COLOURS for b in full.COLOURS
        }
    blocks[6, 7] = dict(r)
    observed_full = equations.cylinders.matching_tensor(tuple(range(8)), blocks)
    hs = equations.cylinders.matching_tensor(full.SIX, internal)
    word_terms = equations.reconstruct_word_terms(internal)
    for a, b in itertools.product(full.COLOURS, repeat=2):
        observed = {
            word[:6]: value for word, value in observed_full.items()
            if word[6:] == (a, b)
        }
        expected = {}
        for word, value in hs.items():
            equations.cylinders.add(expected, word, r[a, b] * value)
        for word, values in word_terms.items():
            total = Q(0)
            for ((i, c), (j, d)), value in values:
                total += value * (
                    p[a, i, c] * q[b, j, d]
                    + p[a, j, d] * q[b, i, c]
                )
            equations.cylinders.add(expected, word, total)
        assert observed == expected


def build_outside_case(name, spec, pattern, x21):
    coefficients = old_full.coefficients_for_case(spec, pattern, x21)
    blocks = adjacent.blocks_for(coefficients, Q(1))
    killed = adjacent.quotient_killed(spec["retained"], retain_t=True)
    terms = adjacent.projected_terms(blocks, killed)
    normals = tuple(
        full.projected_cylinder_intersection((2, 3, 4, cut), blocks, killed)
        for cut in (0, 1, 5)
    )
    assert equations.same_span(normals[0], normals[1])
    assert equations.same_span(normals[0], normals[2])
    normal = normals[0]
    expected_dimension = {"x10": 2, "x12": 1, "x20": 2, "x22": 1}[name]
    assert len(normal) == expected_dimension

    # All omitted coefficients are arbitrary, not specialized to zero.
    for bit in range(9):
        if bit in spec["retained"]:
            continue
        augmented = dict(coefficients)
        augmented[full.CELLS[bit]] = Q(1)
        augmented_blocks = adjacent.blocks_for(augmented, Q(1))
        assert adjacent.projected_terms(augmented_blocks, killed) == terms
        for cut in range(6):
            assert equations.same_span(
                full.projected_cylinder_columns(cut, augmented_blocks, killed),
                full.projected_cylinder_columns(cut, blocks, killed),
            )

    span = equations.cylinders.echelon(normal)
    for colour in ACTIVE:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, span)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    assert equations.cylinders.member(full.project_vector(hs, killed), span)
    program, generators = worker.direct_program(terms, normal, ACTIVE, 0)
    assert generators == OUTSIDE_GENERATORS[name][pattern, x21]
    return (
        f"outside_{name}_d{pattern}_b{x21}",
        program, generators, len(normal),
    )


def local_full_bits(mask):
    return tuple(
        LOCAL_TO_FULL[bit] for bit in range(5) if mask & (1 << bit)
    )


def local_blocks(mask):
    return adjacent.blocks_for(
        {
            full.CELLS[bit]: Q(1)
            for bit in local_full_bits(mask)
        },
        Q(1),
    )


def old_class_killed(maximal, retained_local):
    maximal_full = set(local_full_bits(maximal))
    retained_full = {LOCAL_TO_FULL[bit] for bit in retained_local}
    retained_union = set(adjacent.T_BLOCK)
    for bit in retained_full:
        retained_union.update(adjacent.X_BLOCKS[bit])
    killed = set(full.UPLUS) - retained_union
    for bit in maximal_full - retained_full:
        killed.update(adjacent.X_BLOCKS[bit])
    return killed


def build_old_class(spec):
    (
        name, maximal, retained_local, colours,
        _old_killed, _old_words, _old_atoms, _old_normal, _old_generators,
    ) = spec
    representative = sum(1 << bit for bit in retained_local)
    killed = old_class_killed(maximal, retained_local)
    blocks = local_blocks(representative)
    terms = adjacent.projected_terms(blocks, killed)
    normals = tuple(
        full.projected_cylinder_intersection((2, 3, 4, cut), blocks, killed)
        for cut in (0, 1, 5)
    )
    assert equations.same_span(normals[0], normals[1])
    assert equations.same_span(normals[0], normals[2])
    normal = normals[0]
    members = [
        mask for mask in range(32) if old_locus.class_name(mask) == name
    ]
    expected_members, expected_dimension, expected_killed, expected_words, (
        expected_generators
    ) = OLD_CLASS_EXPECTED[name]
    assert len(members) == expected_members
    assert len(normal) == expected_dimension
    assert len(killed) == expected_killed
    assert len(terms) == expected_words

    projected_hs = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, blocks), killed
    )
    for mask in members:
        assert mask & maximal == mask
        assert all(mask & (1 << bit) for bit in retained_local)
        actual_blocks = local_blocks(mask)
        assert adjacent.projected_terms(actual_blocks, killed) == terms
        assert full.project_vector(
            equations.cylinders.matching_tensor(full.SIX, actual_blocks),
            killed,
        ) == projected_hs
        for cut_index, cut in enumerate((0, 1, 5)):
            actual_normal = full.projected_cylinder_intersection(
                (2, 3, 4, cut), actual_blocks, killed
            )
            assert equations.same_span(actual_normal, normals[cut_index])

    span = equations.cylinders.echelon(normal)
    assert equations.cylinders.member(projected_hs, span)
    for colour in colours:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, span)
    program, generators = worker.direct_program(terms, normal, colours, 0)
    assert generators == expected_generators
    return f"old_{name}", program, generators, len(normal)


def run_unit(job):
    name, program, generators, normal_dimension = job
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=3600,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    assert worker.marker_values(completed.stdout, "UNIT", 1) == (1,)
    assert worker.marker_values(completed.stdout, "GBSIZE", 1) == (1,)
    return name, generators, normal_dimension, time.monotonic() - started


def main():
    audit_torus_supports_and_coordinate_blocks()
    audit_literal_boundary_identity()
    old_full.audit_support_partition_and_torus()

    # Schedule the empirically heavier exact jobs first.
    jobs = []
    symbolic_program, symbolic_generators, coordinates, killed = (
        symbolic.build_problem()
    )
    assert (symbolic_generators, coordinates, killed) == (648, 163, 175)
    jobs.append(("outside_x12_crossratio_lambda", symbolic_program, 648, 1))

    for name in ("x22", "x12", "x20", "x10"):
        spec = old_full.FAMILIES[name]
        for pattern in spec["patterns"]:
            for x21 in spec["x21"]:
                if name == "x12" and pattern == 6 and x21:
                    continue
                jobs.append(build_outside_case(name, spec, pattern, x21))
    assert len(jobs) == 28
    jobs.extend(build_old_class(spec) for spec in old_locus.CLASS_SPECS)
    assert len(jobs) == 33

    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(run_unit, jobs))
    elapsed = time.monotonic() - started

    print("arbitrary A23 plus A25=E00+tE11 fourth-cut obstruction: PASS")
    print("t=0 inherited audited theorem; t!=0 normalized independently: PASS")
    print("512 A23 masks partitioned 32+480; full modulus census exact: PASS")
    print("35-cell t block, overlaps 9+9+9, and no X*t terms: PASS")
    print("5 old-locus + 27 finite outside + Q[lambda] ideals: PASS")
    print("projected normals and every killed arbitrary coefficient: PASS")
    print("endpoint order, 108 shared-star entries, ordered fibres, A67: PASS")
    for name, generators, normal_dimension, seconds in sorted(results):
        print(
            f"{name}: N={normal_dimension}, generators={generators}, "
            f"{seconds:.3f}s: PASS"
        )
    print(f"parallel exact-Q wall time: {elapsed:.3f}s")


if __name__ == "__main__":
    main()
