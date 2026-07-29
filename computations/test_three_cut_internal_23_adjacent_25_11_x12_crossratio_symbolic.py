#!/usr/bin/env python3
"""Exact Q[lambda] discovery test with A_25=E_00+E_11.

The retained A_23 rectangle is normalized to

    x12=x11=x22=1, x21=lambda,

while the independent nonzero A_25 coefficient is normalized to one.
The projected common normal is locked to its direct-tensor line before the
shared-star ideal is tested over Q[lambda].
"""

from __future__ import annotations

import itertools
import shutil
import subprocess
import time

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_plane_support_component as worker
import test_three_cut_internal_23_x12_crossratio_symbolic as old_symbolic


Q = full.Q
COLOURS = (1, 2)
RETAINED = (4, 5, 7, 8)
E_WORD = old_symbolic.E_WORD
A_WORD = old_symbolic.A_WORD
T_WORD = (2, 2, 1, 2, 2, 1)


def build_problem():
    base_coefficients = {
        full.CELLS[5]: Q(1),
        full.CELLS[4]: Q(1),
        full.CELLS[8]: Q(1),
    }
    one_coefficients = dict(base_coefficients)
    one_coefficients[full.CELLS[7]] = Q(1)
    killed = adjacent.quotient_killed(RETAINED, retain_t=True)
    base_blocks = adjacent.blocks_for(base_coefficients, Q(1))
    one_blocks = adjacent.blocks_for(one_coefficients, Q(1))
    normals = [
        full.expanded_projected_cylinder_intersection(
            (2, 3, 4, cut), (base_blocks, one_blocks), killed
        )
        for cut in (0, 1, 5)
    ]
    assert equations.same_span(normals[0], normals[1])
    assert equations.same_span(normals[0], normals[2])
    basis = normals[0]
    explicit_plane = [
        {E_WORD: Q(1)},
        {
            (1, 2, 1, 2, 0, 0): Q(1),
            (0, 0, 1, 1, 0, 0): Q(1),
            (0, 0, 1, 2, 0, 0): Q(1),
            (0, 0, 2, 2, 0, 0): Q(1),
            (1, 1, 1, 1, 1, 0): Q(1),
            T_WORD: Q(1),
        },
    ]
    assert equations.same_span(basis, explicit_plane)

    # The same coefficientwise functional locks the expanded plane to the
    # actual line.  The new t-coordinate has zero coefficient in it.
    for cut in (0, 1, 5):
        at_zero = old_symbolic.raw_projected_cylinder_columns(
            cut, base_blocks, killed
        )
        at_one = old_symbolic.raw_projected_cylinder_columns(
            cut, one_blocks, killed
        )
        for column_zero, column_one in zip(at_zero, at_one):
            delta_e = (
                column_one.get(E_WORD, Q(0))
                - column_zero.get(E_WORD, Q(0))
            )
            delta_a = (
                column_one.get(A_WORD, Q(0))
                - column_zero.get(A_WORD, Q(0))
            )
            assert column_zero.get(E_WORD, Q(0)) == 0
            assert delta_e - column_zero.get(A_WORD, Q(0)) == 0
            assert delta_a == 0

    base_terms = old_symbolic.coefficient_maps(
        equations.reconstruct_word_terms(base_blocks)
    )
    one_terms = old_symbolic.coefficient_maps(
        equations.reconstruct_word_terms(one_blocks)
    )
    base_terms = {
        word: values for word, values in base_terms.items() if word not in killed
    }
    one_terms = {
        word: values for word, values in one_terms.items() if word not in killed
    }
    # All five omitted A_23 coefficients remain arbitrary, including the
    # x10/x12-row coordinate overlaps with the retained t block.
    for bit in range(9):
        if bit in RETAINED:
            continue
        for coefficients, reference_terms in (
            (base_coefficients, base_terms),
            (one_coefficients, one_terms),
        ):
            augmented = dict(coefficients)
            augmented[full.CELLS[bit]] = Q(1)
            augmented_blocks = adjacent.blocks_for(augmented, Q(1))
            augmented_terms = old_symbolic.coefficient_maps(
                equations.reconstruct_word_terms(augmented_blocks)
            )
            augmented_terms = {
                word: values for word, values in augmented_terms.items()
                if word not in killed
            }
            assert augmented_terms == reference_terms
            reference_blocks = (
                base_blocks if coefficients is base_coefficients else one_blocks
            )
            for cut in range(6):
                assert equations.same_span(
                    full.projected_cylinder_columns(
                        cut, augmented_blocks, killed
                    ),
                    full.projected_cylinder_columns(
                        cut, reference_blocks, killed
                    ),
                )
    h_base = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, base_blocks), killed
    )
    h_one = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, one_blocks), killed
    )
    assert h_base == explicit_plane[1]
    assert h_one == {
        **explicit_plane[1],
        E_WORD: Q(1),
    }
    coordinates = tuple(sorted(
        set(base_terms) | set(one_terms)
        | {word for vector in basis for word in vector}
        | {(colour,) * 6 for colour in COLOURS}
    ))
    span = equations.cylinders.echelon(basis)
    for colour in COLOURS:
        word = (colour,) * 6
        assert word not in killed
        assert not equations.cylinders.member({word: Q(1)}, span)

    generators = []
    for a, b in itertools.product(COLOURS, repeat=2):
        generators.extend(old_symbolic.line_fibre_equations(
            base_terms, one_terms, h_base, h_one, coordinates,
            a, b, a if a == b else None,
        ))
    endpoints = tuple(itertools.product(range(6), range(3)))
    names = ["lam"] + [
        equations.variable(kind, boundary, endpoint)
        for kind in ("p", "q")
        for boundary in COLOURS
        for endpoint in endpoints
    ]
    code = "ring r=0,(" + ",".join(names) + "),dp;\n"
    code += "option(redSB);\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += "ideal G=std(I);\n"
    code += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
    code += 'print("GBSIZE"); size(G);\n'
    return code, len(generators), len(coordinates), len(killed)


def main():
    code, generators, coordinates, killed = build_problem()
    print(
        "START", f"generators={generators}", f"coordinates={coordinates}",
        f"killed={killed}", "normal_dim=1", flush=True,
    )
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=code, text=True, capture_output=True,
        check=True, timeout=3600,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    print(
        "RESULT",
        f"unit={worker.marker_values(completed.stdout, 'UNIT', 1)[0]}",
        f"gbsize={worker.marker_values(completed.stdout, 'GBSIZE', 1)[0]}",
        f"seconds={time.monotonic() - started:.3f}",
    )


if __name__ == "__main__":
    main()
