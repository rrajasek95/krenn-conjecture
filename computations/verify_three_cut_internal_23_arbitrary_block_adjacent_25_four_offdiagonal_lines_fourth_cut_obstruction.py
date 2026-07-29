#!/usr/bin/env python3
"""Exact theorem for four off-diagonal one-cell lines in A25.

Keep the seven fixed internal cells and the E00 base cell in A25 from the
audited adjacent-line theorem.  Let A23 be arbitrary and let

    A25 = E00 + t E_cd,   cd in {01,02,12,21}.

For t=0 the audited arbitrary-A23 theorem applies.  For t!=0, the moving
cell supplies an independent sixth torus character.  The same 512 support
partition gives five old-locus, twenty-seven finite outside-locus, and one
Q[lambda] shared-star ideal for each direction.  Every ideal is checked over
characteristic zero by Singular.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import shutil
import subprocess
import time

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_plane_support_component as worker
import test_three_cut_internal_23_x12_crossratio_symbolic as old_symbolic
import verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction as old_full
import verify_three_cut_internal_23_plane_support_fourth_cut_obstruction as old_locus


Q = full.Q
DIRECTIONS = ((0, 1), (0, 2), (1, 2), (2, 1))
ACTIVE = (1, 2)
LOCAL_TO_FULL = (0, 1, 2, 4, 7)
EXPECTED_LEDGER_SHA256 = "e9d1bd6f2fbe5f1f4a106cd8251ec6f3c9a38725000e441080def5c49fab3f75"
EXPECTED_DIRECTION_SHA256 = {
    (0, 1): "d93f7fb5193e21208405229f372ebbc289796947fc5ba448f6f8c6b059c88c67",
    (0, 2): "3847216772aa78b9570c656dcd2babfa14acb51adfb1575e8e6693221167d0f5",
    (1, 2): "c05a76ce4d969850335cee96bd7502eeadc3e1933245af3025bce15a8b287b4c",
    (2, 1): "8eec1a312d973e9b50f8c73572b00bff0db81f216059e440e10930793c5931fd",
}
OUTSIDE_NORMAL_DIMENSIONS = {
    (0, 1): {"x10": 2, "x12": 1, "x20": 2, "x22": 1},
    (0, 2): {"x10": 2, "x12": 1, "x20": 2, "x22": 1},
    (1, 2): {"x10": 2, "x12": 1, "x20": 2, "x22": 1},
    (2, 1): {"x10": 3, "x12": 1, "x20": 3, "x22": 1},
}


def select_direction(cell):
    adjacent.T_CELL = cell
    adjacent.T_BLOCK, adjacent.T_DETAILS = adjacent.variable_coordinate_block(
        adjacent.T_EDGE, cell
    )


def torus_data(cell):
    fixed = (
        ((0, 1), (0, 0)), ((4, 5), (0, 0)),
        ((0, 2), (1, 1)), ((1, 4), (1, 1)),
        ((0, 4), (2, 2)), ((1, 3), (2, 2)),
        ((2, 5), (0, 0)), ((3, 5), (1, 0)),
    )
    constraints = sp.Matrix.vstack(*(
        adjacent.cell_weight(edge, fixed_cell)
        for edge, fixed_cell in fixed
    ))
    assert constraints.rank() == 8
    kernel = sp.Matrix.hstack(*constraints.nullspace())
    assert kernel.shape == (18, 10)
    x_rows = sp.Matrix.vstack(*(
        adjacent.cell_weight((2, 3), x_cell) * kernel
        for x_cell in full.CELLS
    ))
    t_row = adjacent.cell_weight((2, 5), cell) * kernel
    assert x_rows.rank() == 5
    assert sp.Matrix.vstack(x_rows, t_row).rank() == 6
    for mask in range(1 << 9):
        rows = [x_rows.row(bit) for bit in range(9) if mask & (1 << bit)]
        x_rank = sp.Matrix.vstack(*rows).rank() if rows else 0
        assert sp.Matrix.vstack(*(rows + [t_row])).rank() == x_rank + 1
    return x_rows, t_row


def audit_direction_geometry(cell):
    select_direction(cell)
    torus_data(cell)
    adjacent.no_mixed_x_t_terms()
    assert len(adjacent.T_BLOCK) == 35
    assert tuple(adjacent.T_DETAILS) == ((0, 3), (0, 4), (1, 3), (3, 4))
    expected_row = cell[0]
    assert tuple(
        len(adjacent.T_BLOCK & block) for block in adjacent.X_BLOCKS
    ) == tuple(9 if bit // 3 == expected_row else 0 for bit in range(9))
    assert not adjacent.T_BLOCK & set(full.UPLUS)
    assert not any((colour,) * 6 in adjacent.T_BLOCK for colour in full.COLOURS)

    # The t=0 member is literally independent of the selected direction.
    sample = {x_cell: Q(index + 2) for index, x_cell in enumerate(full.CELLS)}
    assert adjacent.blocks_for(sample, Q(0)) == full.blocks_for_coefficients(sample)


def audit_literal_boundary_identity(cell):
    select_direction(cell)
    coefficients = {
        x_cell: Q(2001 + bit) for bit, x_cell in enumerate(full.CELLS)
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


def assert_targets_and_direct(normal, killed, blocks, active):
    span = equations.cylinders.echelon(normal)
    for colour in active:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, span)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    assert equations.cylinders.member(full.project_vector(hs, killed), span)


def build_outside_case(cell, name, spec, pattern, x21):
    select_direction(cell)
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
    expected_dimension = OUTSIDE_NORMAL_DIMENSIONS[cell][name]
    assert len(normal) == expected_dimension

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
    assert_targets_and_direct(normal, killed, blocks, ACTIVE)
    program, generators = worker.direct_program(terms, normal, ACTIVE, 0)
    return (
        f"{cell[0]}{cell[1]}_outside_{name}_d{pattern}_b{x21}",
        program, generators, len(normal), cell,
    )


def local_full_bits(mask):
    return tuple(
        LOCAL_TO_FULL[bit] for bit in range(5) if mask & (1 << bit)
    )


def local_blocks(mask):
    return adjacent.blocks_for(
        {full.CELLS[bit]: Q(1) for bit in local_full_bits(mask)}, Q(1)
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


def build_old_class(cell, spec):
    select_direction(cell)
    name, maximal, retained_local, active = spec[:4]
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

    members = [mask for mask in range(32) if old_locus.class_name(mask) == name]
    for mask in members:
        assert mask & maximal == mask
        assert all(mask & (1 << bit) for bit in retained_local)
        actual_blocks = local_blocks(mask)
        assert adjacent.projected_terms(actual_blocks, killed) == terms
        for cut_index, cut in enumerate((0, 1, 5)):
            actual_normal = full.projected_cylinder_intersection(
                (2, 3, 4, cut), actual_blocks, killed
            )
            assert equations.same_span(actual_normal, normals[cut_index])

    assert_targets_and_direct(normal, killed, blocks, active)
    program, generators = worker.direct_program(terms, normal, active, 0)
    return (
        f"{cell[0]}{cell[1]}_old_{name}", program, generators,
        len(normal), cell,
    )


def build_crossratio(cell):
    select_direction(cell)
    retained = (4, 5, 7, 8)
    base_coefficients = {
        full.CELLS[5]: Q(1), full.CELLS[4]: Q(1), full.CELLS[8]: Q(1),
    }
    one_coefficients = dict(base_coefficients)
    one_coefficients[full.CELLS[7]] = Q(1)
    killed = adjacent.quotient_killed(retained, retain_t=True)
    base_blocks = adjacent.blocks_for(base_coefficients, Q(1))
    one_blocks = adjacent.blocks_for(one_coefficients, Q(1))
    normals = tuple(
        full.expanded_projected_cylinder_intersection(
            (2, 3, 4, cut), (base_blocks, one_blocks), killed
        )
        for cut in (0, 1, 5)
    )
    assert equations.same_span(normals[0], normals[1])
    assert equations.same_span(normals[0], normals[2])
    basis = normals[0]
    h_base = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, base_blocks), killed
    )
    h_one = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, one_blocks), killed
    )
    e = {old_symbolic.E_WORD: Q(1)}
    assert equations.same_span(basis, (e, h_base))
    assert adjacent.subtract(h_one, h_base) == e

    # The coefficientwise functional ell_lambda=E*-lambda A* locks the safe
    # expanded plane to the actual direct-tensor line for every lambda.
    for cut in (0, 1, 5):
        at_zero = old_symbolic.raw_projected_cylinder_columns(
            cut, base_blocks, killed
        )
        at_one = old_symbolic.raw_projected_cylinder_columns(
            cut, one_blocks, killed
        )
        for column_zero, column_one in zip(at_zero, at_one):
            delta_e = (
                column_one.get(old_symbolic.E_WORD, Q(0))
                - column_zero.get(old_symbolic.E_WORD, Q(0))
            )
            delta_a = (
                column_one.get(old_symbolic.A_WORD, Q(0))
                - column_zero.get(old_symbolic.A_WORD, Q(0))
            )
            assert column_zero.get(old_symbolic.E_WORD, Q(0)) == 0
            assert delta_e - column_zero.get(old_symbolic.A_WORD, Q(0)) == 0
            assert delta_a == 0

    base_terms = old_symbolic.coefficient_maps(
        equations.reconstruct_word_terms(base_blocks)
    )
    one_terms = old_symbolic.coefficient_maps(
        equations.reconstruct_word_terms(one_blocks)
    )
    base_terms = {word: value for word, value in base_terms.items() if word not in killed}
    one_terms = {word: value for word, value in one_terms.items() if word not in killed}
    for bit in range(9):
        if bit in retained:
            continue
        for coefficients, reference_terms, reference_blocks in (
            (base_coefficients, base_terms, base_blocks),
            (one_coefficients, one_terms, one_blocks),
        ):
            augmented = dict(coefficients)
            augmented[full.CELLS[bit]] = Q(1)
            augmented_blocks = adjacent.blocks_for(augmented, Q(1))
            augmented_terms = old_symbolic.coefficient_maps(
                equations.reconstruct_word_terms(augmented_blocks)
            )
            augmented_terms = {
                word: value for word, value in augmented_terms.items()
                if word not in killed
            }
            assert augmented_terms == reference_terms
            for cut in range(6):
                assert equations.same_span(
                    full.projected_cylinder_columns(cut, augmented_blocks, killed),
                    full.projected_cylinder_columns(cut, reference_blocks, killed),
                )

    coordinates = tuple(sorted(
        set(base_terms) | set(one_terms)
        | {word for vector in basis for word in vector}
        | {(colour,) * 6 for colour in ACTIVE}
    ))
    span = equations.cylinders.echelon(basis)
    for colour in ACTIVE:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, span)

    generators = []
    for a, b in itertools.product(ACTIVE, repeat=2):
        generators.extend(old_symbolic.line_fibre_equations(
            base_terms, one_terms, h_base, h_one, coordinates,
            a, b, a if a == b else None,
        ))
    endpoints = tuple(itertools.product(range(6), range(3)))
    names = ["lam"] + [
        equations.variable(kind, boundary, endpoint)
        for kind in ("p", "q") for boundary in ACTIVE for endpoint in endpoints
    ]
    program = "ring r=0,(" + ",".join(names) + "),dp;\n"
    program += "option(redSB);\n"
    program += "ideal I=" + ",".join(generators) + ";\n"
    program += "ideal G=std(I);\n"
    program += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
    program += 'print("GBSIZE"); size(G);\n'
    return (
        f"{cell[0]}{cell[1]}_outside_x12_crossratio_lambda",
        program, len(generators), 1, cell,
    )


def build_jobs():
    jobs = []
    for cell in DIRECTIONS:
        audit_direction_geometry(cell)
        audit_literal_boundary_identity(cell)
        for name in ("x22", "x12", "x20", "x10"):
            spec = old_full.FAMILIES[name]
            for pattern in spec["patterns"]:
                for x21 in spec["x21"]:
                    if name == "x12" and pattern == 6 and x21:
                        continue
                    jobs.append(build_outside_case(cell, name, spec, pattern, x21))
        assert len([job for job in jobs if job[4] == cell]) == 27
        jobs.extend(build_old_class(cell, spec) for spec in old_locus.CLASS_SPECS)
        jobs.append(build_crossratio(cell))
        assert len([job for job in jobs if job[4] == cell]) == 33
    assert len(jobs) == 132
    return jobs


def run_unit(job):
    name, program, generators, normal_dimension, cell = job
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
    unit = worker.marker_values(completed.stdout, "UNIT", 1)[0]
    size = worker.marker_values(completed.stdout, "GBSIZE", 1)[0]
    assert (unit, size) == (1, 1), (name, unit, size)
    return (
        name, generators, normal_dimension,
        hashlib.sha256(program.encode()).hexdigest(),
        time.monotonic() - started, cell,
    )


def ledger_hash(jobs):
    rows = [
        f"{name}|{generators}|{normal_dimension}|"
        f"{hashlib.sha256(program.encode()).hexdigest()}"
        for name, program, generators, normal_dimension, _cell in sorted(jobs)
    ]
    return hashlib.sha256("\n".join(rows).encode()).hexdigest()


def selected_ledger_hash(jobs, cell):
    return ledger_hash([job for job in jobs if job[4] == cell])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry-only", action="store_true")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    old_full.audit_support_partition_and_torus()
    started_build = time.monotonic()
    jobs = build_jobs()
    build_elapsed = time.monotonic() - started_build
    digest = ledger_hash(jobs)
    assert digest == EXPECTED_LEDGER_SHA256
    global_templates = {
        hashlib.sha256(job[1].encode()).hexdigest() for job in jobs
    }
    assert len(global_templates) == 102
    print(
        "four off-diagonal A25 lines geometry: PASS",
        f"jobs={len(jobs)}", f"build_seconds={build_elapsed:.3f}",
        f"global_program_templates={len(global_templates)}",
        f"ledger_sha256={digest}", flush=True,
    )
    for cell in DIRECTIONS:
        selected = [job for job in jobs if job[4] == cell]
        direction_digest = selected_ledger_hash(jobs, cell)
        assert direction_digest == EXPECTED_DIRECTION_SHA256[cell]
        counts = tuple(job[2] for job in selected)
        print(
            f"direction={cell[0]}{cell[1]}", "ideals=33",
            f"generator_min={min(counts)}", f"generator_max={max(counts)}",
            f"program_templates={len({hashlib.sha256(job[1].encode()).hexdigest() for job in selected})}",
            f"ledger_sha256={direction_digest}",
            flush=True,
        )
    if args.geometry_only:
        return

    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(run_unit, jobs))
    elapsed = time.monotonic() - started
    print("four off-diagonal A25 lines fourth-cut obstruction: PASS")
    print("t=0 inherited arbitrary-A23 theorem; t!=0 normalized: PASS")
    print("4*(5 old + 27 finite + 1 Q[lambda]) unit ideals: PASS")
    print("all supports, arbitrary killed coefficients, and literal fibres: PASS")
    for cell in DIRECTIONS:
        selected = [result for result in results if result[5] == cell]
        print(
            f"direction={cell[0]}{cell[1]}",
            f"exact_wall_max={max(result[4] for result in selected):.3f}s",
            f"certificate_hashes={len({result[3] for result in selected})}",
        )
    print(f"parallel exact-Q wall time: {elapsed:.3f}s")
    print(f"certificate ledger SHA256: {digest}")


if __name__ == "__main__":
    main()
