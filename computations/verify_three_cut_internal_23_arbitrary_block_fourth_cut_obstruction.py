#!/usr/bin/env python3
"""Exact arbitrary-complex theorem for a full 3x3 A_23 block.

The other eight internal cells remain fixed.  The prior five-cell theorem
covers supports with x10=x12=x20=x22=0.  Here the 480 remaining supports are
partitioned by their first nonzero outside cell.  Coordinate quotients kill
all continuous parameters except one x12 rectangle cross ratio.  Twenty-seven
finite orbit ideals and one Q[lambda] ideal are checked exactly.
"""

from __future__ import annotations

import concurrent.futures
import itertools
import shutil
import subprocess
import time

import sympy as sp

import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_plane_support_component as worker
import test_three_cut_internal_23_x12_crossratio_symbolic as symbolic


Q = full.Q
MAXIMAL = (1 << 9) - 1
SELECTED_COLOURS = (1, 2)


FAMILIES = {
    "x10": {
        "outside": 3,
        "retained": (3, 4, 7, 8),
        "patterns": (0, 2, 4, 6),
        "x21": (0, 1),
        "forced_zero": (),
        "free_killed": (0, 1, 2, 5, 6),
        "generators": {
            (0, 0): 328, (0, 1): 432,
            (2, 0): 412, (2, 1): 516,
            (4, 0): 440, (4, 1): 544,
            (6, 0): 524, (6, 1): 628,
        },
    },
    "x12": {
        "outside": 5,
        "retained": (4, 5, 7, 8),
        "patterns": (0, 2, 4, 6),
        "x21": (0, 1),
        "forced_zero": (3,),
        "free_killed": (0, 1, 2, 6),
        "generators": {
            (0, 0): 332, (0, 1): 436,
            (2, 0): 416, (2, 1): 520,
            (4, 0): 444, (4, 1): 548,
            (6, 0): 528,
            # (6,1) is replaced by the Q[lambda] certificate.
        },
    },
    "x20": {
        "outside": 6,
        "retained": (3, 4, 6, 7, 8),
        "patterns": (0, 2, 4, 6),
        "x21": (0, 1),
        "forced_zero": (3, 5),
        "free_killed": (0, 1, 2),
        "generators": {
            (0, 0): 356, (0, 1): 460,
            (2, 0): 440, (2, 1): 544,
            (4, 0): 468, (4, 1): 572,
            (6, 0): 552, (6, 1): 656,
        },
    },
    "x22": {
        "outside": 8,
        "retained": (3, 4, 5, 6, 7, 8),
        "patterns": (4, 6),
        "x21": (0, 1),
        "forced_zero": (3, 5, 6),
        "free_killed": (0, 1, 2),
        "generators": {
            (4, 0): 384, (4, 1): 488,
            (6, 0): 468, (6, 1): 572,
        },
    },
}


def coefficients_for_case(spec, pattern, x21):
    coefficients = {full.CELLS[spec["outside"]]: Q(1)}
    if pattern & 2:
        coefficients[full.CELLS[4]] = Q(1)
    if pattern & 4:
        coefficients[full.CELLS[8]] = Q(1)
    if x21:
        coefficients[full.CELLS[7]] = Q(1)
    return coefficients


def projected_terms(blocks, killed):
    terms = equations.reconstruct_word_terms(blocks)
    return {
        word: tuple(values) for word, values in terms.items() if word not in killed
    }


def audit_support_partition_and_torus():
    outside_order = (3, 5, 6, 8)
    counts = {name: 0 for name in FAMILIES}
    family_for_outside = dict(zip(outside_order, FAMILIES))
    for mask in range(1 << 9):
        present = [bit for bit in outside_order if mask & (1 << bit)]
        if not present:
            continue
        name = family_for_outside[present[0]]
        counts[name] += 1
        spec = FAMILIES[name]
        assert mask & (1 << spec["outside"])
        assert all(not mask & (1 << bit) for bit in spec["forced_zero"])
    assert counts == {"x10": 256, "x12": 128, "x20": 64, "x22": 32}
    assert sum(counts.values()) == 480

    # Every finite retained support is one complex torus orbit.  The sole
    # circuit is x12+x21=x11+x22, giving the cross ratio lambda.
    exponent = {bit: sp.Matrix(full.torus_exponent(full.CELLS[bit])).T
                for bit in range(9)}
    for name, spec in FAMILIES.items():
        for pattern in spec["patterns"]:
            for x21 in spec["x21"]:
                nonzero = [spec["outside"]]
                if pattern & 2:
                    nonzero.append(4)
                if pattern & 4 and spec["outside"] != 8:
                    nonzero.append(8)
                if x21:
                    nonzero.append(7)
                matrix = sp.Matrix.vstack(*(exponent[bit] for bit in nonzero))
                if name == "x12" and pattern == 6 and x21:
                    assert matrix.rank() == 3 and len(nonzero) == 4
                    assert (
                        exponent[5] + exponent[7]
                        - exponent[4] - exponent[8]
                    ) == sp.zeros(1, 5)
                else:
                    assert matrix.rank() == len(nonzero)


def raw_projected_columns(z, blocks, killed):
    # Echelon bases are sufficient here: adding a killed cell must leave the
    # projected cylinder span unchanged, not the chosen raw presentation.
    return full.projected_cylinder_columns(z, blocks, killed)


def build_finite_case(name, spec, pattern, x21):
    coefficients = coefficients_for_case(spec, pattern, x21)
    blocks = full.blocks_for_coefficients(coefficients)
    killed = full.killed_coordinates(MAXIMAL, spec["retained"])
    terms = projected_terms(blocks, killed)
    normals = [
        full.projected_cylinder_intersection((2, 3, 4, cut), blocks, killed)
        for cut in (0, 1, 5)
    ]
    assert equations.same_span(normals[0], normals[1])
    assert equations.same_span(normals[0], normals[2])
    normal = normals[0]

    # All coefficients outside the retained chart disappear termwise after
    # projection.  The projected cylinders also remain identical, so these
    # coefficients are genuinely arbitrary, not normalized or sampled.
    for bit in spec["free_killed"]:
        augmented = dict(coefficients)
        augmented[full.CELLS[bit]] = Q(1)
        augmented_blocks = full.blocks_for_coefficients(augmented)
        assert projected_terms(augmented_blocks, killed) == terms
        for cut in (0, 1, 2, 3, 4, 5):
            assert equations.same_span(
                raw_projected_columns(cut, augmented_blocks, killed),
                raw_projected_columns(cut, blocks, killed),
            )

    normal_span = equations.cylinders.echelon(normal)
    for colour in SELECTED_COLOURS:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, normal_span)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    projected_hs = full.project_vector(hs, killed)
    assert equations.cylinders.member(projected_hs, normal_span)

    program, generators = worker.direct_program(
        terms, normal, SELECTED_COLOURS, characteristic=0
    )
    expected = spec["generators"][pattern, x21]
    assert generators == expected
    return f"{name}_d{pattern}_b{x21}", program, generators, len(normal)


def audit_literal_boundary_identity():
    coefficients = {
        cell: Q(bit + 1) for bit, cell in enumerate(full.CELLS)
    }
    internal = full.blocks_for_coefficients(coefficients)
    p = {(a, i, c): Q(1 + 100*a + 10*i + c)
         for a in range(3) for i in range(6) for c in range(3)}
    q = {(b, i, c): Q(701 + 100*b + 10*i + c)
         for b in range(3) for i in range(6) for c in range(3)}
    r = {(a, b): Q(1301 + 10*a + b) for a in range(3) for b in range(3)}
    blocks = {edge: dict(block) for edge, block in internal.items()}
    for i in range(6):
        blocks[i, 6] = {(c, a): p[a, i, c] for c in range(3) for a in range(3)}
        blocks[i, 7] = {(c, b): q[b, i, c] for c in range(3) for b in range(3)}
    blocks[6, 7] = dict(r)
    full_tensor = equations.cylinders.matching_tensor(tuple(range(8)), blocks)
    hs = equations.cylinders.matching_tensor(full.SIX, internal)
    word_terms = equations.reconstruct_word_terms(internal)
    for a, b in itertools.product(range(3), repeat=2):
        observed = {
            word[:6]: value for word, value in full_tensor.items()
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


def run_unit(name, program, generators, normal_dimension):
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
    audit_support_partition_and_torus()
    audit_literal_boundary_identity()
    jobs = []
    for name, spec in FAMILIES.items():
        for pattern in spec["patterns"]:
            for x21 in spec["x21"]:
                if name == "x12" and pattern == 6 and x21:
                    continue
                jobs.append(build_finite_case(name, spec, pattern, x21))
    assert len(jobs) == 27

    symbolic_program, symbolic_generators, _coordinates, _killed, normal_dimension = (
        symbolic.build_problem("line")
    )
    assert symbolic_generators == 628 and normal_dimension == 1
    jobs.append(("x12_crossratio_lambda", symbolic_program,
                 symbolic_generators, normal_dimension))

    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda args: run_unit(*args), jobs))
    elapsed = time.monotonic() - started
    print("arbitrary A23 outside-locus fourth-cut obstruction: PASS")
    print("480 support masks partitioned 256+128+64+32: PASS")
    print("27 finite complex torus orbits plus Q[lambda] cross ratio: PASS")
    print("projected cut-0/1/5 normals and arbitrary killed coefficients: PASS")
    print("endpoint order, 108 shared-star entries, ordered fibres, A67: PASS")
    for name, generators, normal_dimension, seconds in results:
        print(f"{name}: N={normal_dimension}, generators={generators}, {seconds:.3f}s: PASS")
    print(f"parallel exact-Q wall time: {elapsed:.3f}s")


if __name__ == "__main__":
    main()
