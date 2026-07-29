#!/usr/bin/env python3
"""Exact local obstruction for A23 arbitrary and A25=E00+t E22.

This verifier uses only full, unprojected cylinder normals.

* t=0 is the previously audited arbitrary-A23 theorem.
* For t!=0, normalize t=1.  On x00!=0 a constant full-cylinder minor and
  one symbolic shared-star unit ideal cover all remaining A23 entries.
* On x00=0 and away from {x01,x11,x21}, five first-nonzero charts have
  constant full-cylinder minors for cuts 0 and 1 and symbolic unit ideals.
* The exceptional three-cell locus has eight exact torus representatives;
  their true line/plane normals all give unit ideals.
* For final cut 5, a separate full-cylinder argument proves the normal is
  the direct-tensor line for every A23, including all rank-jump loci.

The conclusion is local to the displayed fixed six-site interior.  It is
not a theorem for arbitrary A25 and not the global Krenn conjecture.
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

import derive_three_cut_internal_23_adjacent_25_22_cut5_line as cut5_line
import derive_three_cut_internal_23_adjacent_25_22_x00_zero_line_minors as off_minors
import derive_three_cut_internal_23_adjacent_25_22_x00_open_line_minors as x00_minors
import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_adjacent_25_22_x00_open_symbolic_star_ideal as x00_ideal
import test_three_cut_internal_23_adjacent_25_22_x00_zero_line_chart_star_ideals as off_ideals
import verify_three_cut_internal_23_adjacent_25_22_exceptional_locus as exceptional


Q = full.Q
ACTIVE = (0, 1)
E22 = (2, 2)
EXPECTED_RANK_LEDGER_SHA256 = (
    "d167275b9c85c03c04e1455e752f0fbd38c6bf43cecb41a9468e448686a87825"
)
EXPECTED_IDEAL_LEDGER_SHA256 = (
    "58c54259ed83211c25704d2987900d405e40af507b96fa041d0975c0bb667efa"
)


def select_e22():
    adjacent.T_CELL = E22
    adjacent.T_BLOCK, adjacent.T_DETAILS = adjacent.variable_coordinate_block(
        adjacent.T_EDGE, adjacent.T_CELL
    )


def stabilizer_rows():
    fixed = (
        ((0, 1), (0, 0)), ((4, 5), (0, 0)),
        ((0, 2), (1, 1)), ((1, 4), (1, 1)),
        ((0, 4), (2, 2)), ((1, 3), (2, 2)),
        ((2, 5), (0, 0)), ((3, 5), (1, 0)),
    )
    constraints = sp.Matrix.vstack(*(
        adjacent.cell_weight(edge, cell) for edge, cell in fixed
    ))
    assert constraints.rank() == 8
    kernel = sp.Matrix.hstack(*constraints.nullspace())
    assert kernel.shape == (18, 10)
    x_rows = tuple(
        adjacent.cell_weight((2, 3), cell) * kernel for cell in full.CELLS
    )
    t_row = adjacent.cell_weight((2, 5), E22) * kernel
    assert sp.Matrix.vstack(*x_rows).rank() == 5
    assert sp.Matrix.vstack(*x_rows, t_row).rank() == 6
    for mask in range(1 << 9):
        selected = [x_rows[bit] for bit in range(9) if mask & (1 << bit)]
        x_rank = sp.Matrix.vstack(*selected).rank() if selected else 0
        assert sp.Matrix.vstack(*(selected + [t_row])).rank() == x_rank + 1
    return x_rows, t_row


def audit_torus_cover(x_rows, t_row):
    assert sp.Matrix.vstack(x_rows[0], t_row).rank() == 2
    counts = {"x00_open": 0, "exceptional": 0}
    counts.update({full.CELL_NAMES[bit]: 0 for bit in off_minors.OFF_EXCEPTIONAL_BITS})
    for mask in range(1 << 9):
        if mask & 1:
            counts["x00_open"] += 1
            continue
        pivot = next(
            (bit for bit in off_minors.OFF_EXCEPTIONAL_BITS if mask & (1 << bit)),
            None,
        )
        if pivot is None:
            counts["exceptional"] += 1
        else:
            counts[full.CELL_NAMES[pivot]] += 1
    assert counts == {
        "x00_open": 256, "exceptional": 8,
        "x02": 128, "x10": 64, "x12": 32, "x20": 16, "x22": 8,
    }
    for pivot in off_minors.OFF_EXCEPTIONAL_BITS:
        assert sp.Matrix.vstack(x_rows[pivot], t_row).rank() == 2
    for support in exceptional.support_patterns():
        rows = [x_rows[bit] for bit in support] + [t_row]
        assert sp.Matrix.vstack(*rows).rank() == len(rows)
    return counts


def audit_direction_geometry():
    select_e22()
    adjacent.no_mixed_x_t_terms()
    assert len(adjacent.T_BLOCK) == 35
    assert tuple(adjacent.T_DETAILS) == ((0, 3), (0, 4), (1, 3), (3, 4))
    assert tuple(
        len(adjacent.T_BLOCK & block) for block in adjacent.X_BLOCKS
    ) == (0, 0, 0, 0, 0, 0, 9, 9, 9)
    assert not adjacent.T_BLOCK & set(full.UPLUS)
    assert tuple((colour,) * 6 in adjacent.T_BLOCK for colour in full.COLOURS) == (
        False, False, True,
    )
    sample = {cell: Q(bit + 2) for bit, cell in enumerate(full.CELLS)}
    assert adjacent.blocks_for(sample, Q(0)) == full.blocks_for_coefficients(sample)


def audit_literal_boundary_identity():
    coefficients = {cell: Q(2001 + bit) for bit, cell in enumerate(full.CELLS)}
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


def label_hash(row_labels, column_labels, rows, columns):
    payload = repr((
        tuple(row_labels[index] for index in rows),
        tuple(column_labels[index] for index in columns),
    ))
    return hashlib.sha256(payload.encode()).hexdigest()


def audit_rank_certificates():
    records = []
    for cut in (0, 1, 5):
        matrix, row_labels, column_labels = x00_minors.representation_matrix(
            cut, x00_minors.PARAMETERS
        )
        rows, columns = x00_minors.select_minor(matrix)
        minor = matrix.extract(rows, columns)
        determinant = sp.factor(minor.det(method="domain-ge"))
        assert determinant in (1, -1)
        records.append((
            "x00_open", cut, matrix.shape, minor.shape, len(minor.todok()),
            str(determinant), label_hash(
                row_labels, column_labels, rows, columns
            ),
        ))
    for pivot in off_minors.OFF_EXCEPTIONAL_BITS:
        _zero_bits, _parameter_bits, parameters = off_minors.chart_data(pivot)
        for cut in (0, 1):
            matrix, row_labels, column_labels = off_minors.representation_matrix(
                cut, pivot, parameters
            )
            rows, columns = off_minors.select_minor(matrix, parameters)
            minor = matrix.extract(rows, columns)
            determinant = sp.factor(minor.det(method="domain-ge"))
            assert determinant in (1, -1)
            records.append((
                full.CELL_NAMES[pivot], cut, matrix.shape, minor.shape,
                len(minor.todok()), str(determinant), label_hash(
                    row_labels, column_labels, rows, columns
                ),
            ))

    blocks = cut5_line.symbolic_blocks()
    tail, hs = cut5_line.tail_and_direct_tensor(blocks)
    matrix, row_labels, column_labels, columns2, columns3 = (
        cut5_line.two_cylinder_matrix(blocks)
    )
    rows, columns = cut5_line.select_minor(matrix)
    minor = matrix.extract(rows, columns)
    determinant = sp.factor(minor.det(method="domain-ge"))
    assert determinant in (1, -1)
    hits = cut5_line.audit_common_ten_space(
        blocks, tail, hs, columns2, columns3
    )
    nonzero, expected = cut5_line.audit_cut5_probe(blocks, hs)
    assert nonzero == (12,) and expected[cut5_line.TAIL_PROBE] == 1
    records.append((
        "cut5_all_A23", 5, matrix.shape, minor.shape, len(minor.todok()),
        str(determinant), label_hash(row_labels, column_labels, rows, columns),
        tuple(hits[2]), tuple(hits[3]), nonzero,
    ))

    digest = hashlib.sha256("\n".join(map(repr, records)).encode()).hexdigest()
    if EXPECTED_RANK_LEDGER_SHA256:
        assert digest == EXPECTED_RANK_LEDGER_SHA256, digest
    return records, digest


def build_ideal_jobs():
    jobs = []
    program, generators, variables, coordinates = x00_ideal.build_program()
    jobs.append({
        "name": "x00_open", "coverage": "cuts_0_1_5",
        "program": program, "generators": generators,
        "variables": variables, "coordinates": coordinates,
    })
    for pivot in off_minors.OFF_EXCEPTIONAL_BITS:
        program, generators, variables, coordinates = off_ideals.build_program(pivot)
        jobs.append({
            "name": full.CELL_NAMES[pivot], "coverage": "cuts_0_1_5",
            "program": program, "generators": generators,
            "variables": variables, "coordinates": coordinates,
        })
    exceptional.select_e22()
    for support in exceptional.support_patterns():
        for cut in (0, 1, 5):
            job = exceptional.build_job(support, cut)
            jobs.append({
                "name": "exceptional_" + (
                    "zero" if not support else "_".join(
                        full.CELL_NAMES[bit] for bit in support
                    )
                ),
                "coverage": f"cut_{cut}",
                "program": job["program"],
                "generators": job["generators"],
                "variables": job["variables"],
                "coordinates": -1,
                "normal_dimension": job["normal_dimension"],
            })
    for job in jobs:
        job["sha256"] = hashlib.sha256(job["program"].encode()).hexdigest()
    assert len(jobs) == 30
    return jobs


def ideal_ledger_hash(jobs):
    rows = [
        (
            job["name"], job["coverage"], job["variables"],
            job["coordinates"], job["generators"],
            job.get("normal_dimension"), job["sha256"],
        )
        for job in jobs
    ]
    return hashlib.sha256("\n".join(map(repr, rows)).encode()).hexdigest()


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_program(program, timeout):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    unit = marker(completed.stdout, "UNIT")
    size = marker(completed.stdout, "GBSIZE")
    assert (unit, size) == (1, 1), (unit, size)
    return time.monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry-only", action="store_true")
    parser.add_argument("--skip-ranks", action="store_true")
    parser.add_argument("--skip-singular", action="store_true")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()

    started_all = time.monotonic()
    audit_direction_geometry()
    x_rows, t_row = stabilizer_rows()
    counts = audit_torus_cover(x_rows, t_row)
    audit_literal_boundary_identity()
    print("GEOMETRY", "pass=1", "support_counts=" + repr(counts), flush=True)
    if args.geometry_only:
        return

    rank_records = []
    rank_digest = "skipped"
    if not args.skip_ranks:
        rank_records, rank_digest = audit_rank_certificates()
        for record in rank_records:
            print("RANK", repr(record), flush=True)
        print("RANK_LEDGER_SHA256", rank_digest, flush=True)

    jobs = build_ideal_jobs()
    ideal_digest = ideal_ledger_hash(jobs)
    if EXPECTED_IDEAL_LEDGER_SHA256:
        assert ideal_digest == EXPECTED_IDEAL_LEDGER_SHA256, ideal_digest
    templates = {}
    for job in jobs:
        templates.setdefault(job["sha256"], job["program"])
    print(
        "IDEAL_LEDGER", f"jobs={len(jobs)}", f"unique={len(templates)}",
        f"sha256={ideal_digest}", flush=True,
    )
    for job in jobs:
        print(
            "IDEAL", job["name"], job["coverage"],
            f'variables={job["variables"]}',
            f'coordinates={job["coordinates"]}',
            f'generators={job["generators"]}',
            f'sha256={job["sha256"]}', flush=True,
        )
    if args.skip_singular:
        return

    started_exact = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        elapsed = dict(zip(
            templates,
            executor.map(
                lambda program: run_program(program, args.timeout),
                templates.values(),
            ),
        ))
    exact_wall = time.monotonic() - started_exact
    print("A23 arbitrary plus A25=E00+tE22 local fourth-cut obstruction: PASS")
    print("t=0 inherited; t!=0 torus cover 256+128+64+32+16+8+8: PASS")
    print("full unprojected normals for cuts 0,1,5: PASS")
    print("30 chart/cut ideals, all exact characteristic-zero units: PASS")
    print("endpoint order, shared stars, ordered fibres, arbitrary A67: PASS")
    print(f"rank ledger SHA256: {rank_digest}")
    print(f"ideal ledger SHA256: {ideal_digest}")
    print(f"unique Singular programs: {len(templates)}")
    print(f"maximum Singular time: {max(elapsed.values()):.3f}s")
    print(f"parallel Singular wall time: {exact_wall:.3f}s")
    print(f"total wall time: {time.monotonic()-started_all:.3f}s")


if __name__ == "__main__":
    main()
