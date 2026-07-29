#!/usr/bin/env python3
"""Exact Q[lambda] unit test for the sole full-block torus invariant.

On the x12-first outside stratum, the four retained nonzero cells

    x12 = x11 = x22 = 1,  x21 = lambda

carry the cross-ratio invariant lambda.  The projected cylinder at each
lambda is contained in the parameter-independent intersection obtained by
spanning the lambda=0 and lambda=1 cylinders first.  This script tests the
complete selected (1,2) fibre packet modulo that larger normal with lambda
an ordinary polynomial variable.  A unit basis therefore covers every
complex lambda, including zero.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import shutil
import subprocess
import time

import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_plane_support_component as worker


Q = full.Q
COLOURS = (1, 2)
RETAINED = (4, 5, 7, 8)
MAXIMAL = (1 << 9) - 1
E_WORD = (0, 0, 2, 1, 0, 0)
A_WORD = (0, 0, 1, 1, 0, 0)


def coefficient_maps(word_terms):
    answer = {}
    for word, terms in word_terms.items():
        data = collections.defaultdict(lambda: Q(0))
        for endpoints, coefficient in terms:
            data[endpoints] += coefficient
        answer[word] = dict(data)
    return answer


def affine_text(constant, value_at_one):
    slope = value_at_one - constant
    pieces = []
    if constant:
        pieces.append(equations.qtext(constant))
    if slope:
        pieces.append("lam*(" + equations.qtext(slope) + ")")
    return "+".join(pieces) if pieces else "0"


def bilinear(base, one, a, b, word):
    left_map = base.get(word, {})
    right_map = one.get(word, {})
    endpoints = sorted(set(left_map) | set(right_map))
    terms = []
    for left, right in endpoints:
        coefficient = affine_text(
            left_map.get((left, right), Q(0)),
            right_map.get((left, right), Q(0)),
        )
        if coefficient == "0":
            continue
        terms.append(
            "(" + coefficient + ")*("
            + equations.variable("p", a, left) + "*"
            + equations.variable("q", b, right) + "+"
            + equations.variable("p", a, right) + "*"
            + equations.variable("q", b, left) + ")"
        )
    return "+".join(terms) if terms else "0"


def fibre_equations(base, one, basis, coordinates, a, b, target):
    rows = equations.membership_rows(basis, coordinates)
    answer = []
    target_word = (target,) * 6 if target is not None else None
    for row in rows:
        terms = []
        constant = Q(0)
        for word, row_coefficient in row.items():
            expression = bilinear(base, one, a, b, word)
            if expression != "0":
                terms.append(
                    "(" + equations.qtext(row_coefficient) + ")*("
                    + expression + ")"
                )
            if word == target_word:
                constant -= row_coefficient
        if constant:
            terms.append(equations.qtext(constant))
        answer.append("+".join(terms) if terms else "0")
    return answer


def scalar_expression(base, one, a, b, word, target_word):
    expression = bilinear(base, one, a, b, word)
    pieces = [] if expression == "0" else ["(" + expression + ")"]
    if word == target_word:
        pieces.append("-1")
    return "+".join(pieces) if pieces else "0"


def line_fibre_equations(base, one, h_base, h_one, coordinates, a, b, target):
    constant_pivots = [
        word for word in coordinates
        if h_base.get(word, Q(0)) == 1 and h_one.get(word, Q(0)) == 1
    ]
    assert constant_pivots
    pivot = min(constant_pivots)
    target_word = (target,) * 6 if target is not None else None
    pivot_expression = scalar_expression(base, one, a, b, pivot, target_word)
    answer = []
    for word in coordinates:
        if word == pivot:
            continue
        value = affine_text(
            h_base.get(word, Q(0)), h_one.get(word, Q(0))
        )
        expression = scalar_expression(base, one, a, b, word, target_word)
        answer.append(
            "(" + expression + ")-(" + value + ")*("
            + pivot_expression + ")"
        )
    return answer


def raw_projected_cylinder_columns(z, blocks, killed):
    u_sites = tuple(site for site in full.SIX if site != z)
    five_columns = []
    for hole in u_sites:
        rest = tuple(site for site in u_sites if site != hole)
        cofactor = equations.cylinders.matching_tensor(rest, blocks)
        for colour in range(3):
            column = {}
            for rest_word, coefficient in cofactor.items():
                assignment = dict(zip(rest, rest_word))
                assignment[hole] = colour
                equations.cylinders.add(
                    column,
                    tuple(assignment[site] for site in u_sites),
                    coefficient,
                )
            five_columns.append(column)
    assert len(five_columns) == 15
    answer = []
    for colour_z in range(3):
        for column in five_columns:
            lifted = {}
            for u_word, coefficient in column.items():
                assignment = dict(zip(u_sites, u_word))
                assignment[z] = colour_z
                word = tuple(assignment[site] for site in full.SIX)
                if word not in killed:
                    equations.cylinders.add(lifted, word, coefficient)
            answer.append(lifted)
    assert len(answer) == 45
    return answer


def build_problem(normal_mode):
    base_coefficients = {
        full.CELLS[5]: Q(1),  # x12
        full.CELLS[4]: Q(1),  # x11
        full.CELLS[8]: Q(1),  # x22
    }
    one_coefficients = dict(base_coefficients)
    one_coefficients[full.CELLS[7]] = Q(1)  # x21
    _projected, killed, _line = full.projected_problem(
        one_coefficients, MAXIMAL, RETAINED, normal="line"
    )
    base_blocks = full.blocks_for_coefficients(base_coefficients)
    one_blocks = full.blocks_for_coefficients(one_coefficients)
    normals = [
        full.expanded_projected_cylinder_intersection(
            (2, 3, 4, cut), (base_blocks, one_blocks), killed
        )
        for cut in (0, 1, 5)
    ]
    assert equations.same_span(normals[0], normals[1])
    assert equations.same_span(normals[0], normals[2])
    basis = normals[0]
    assert len(equations.cylinders.echelon(basis)) == 2
    explicit_plane = [
        {E_WORD: Q(1)},
        {
            (1, 2, 1, 2, 0, 0): Q(1),
            (0, 0, 1, 1, 0, 0): Q(1),
            (0, 0, 1, 2, 0, 0): Q(1),
            (0, 0, 2, 2, 0, 0): Q(1),
            (1, 1, 1, 1, 1, 0): Q(1),
        },
    ]
    assert equations.same_span(basis, explicit_plane)

    # On each possible fourth cut the functional
    #     ell_lambda = [E_WORD]^* - lambda [A_WORD]^*
    # annihilates every projected cylinder column.  A column is affine in
    # lambda, so checking its three polynomial coefficients is exact.
    for cut in (0, 1, 5):
        at_zero = raw_projected_cylinder_columns(cut, base_blocks, killed)
        at_one = raw_projected_cylinder_columns(cut, one_blocks, killed)
        for column_zero, column_one in zip(at_zero, at_one):
            delta_e = column_one.get(E_WORD, Q(0)) - column_zero.get(E_WORD, Q(0))
            delta_a = column_one.get(A_WORD, Q(0)) - column_zero.get(A_WORD, Q(0))
            assert column_zero.get(E_WORD, Q(0)) == 0
            assert delta_e - column_zero.get(A_WORD, Q(0)) == 0
            assert delta_a == 0

    base_terms = coefficient_maps(equations.reconstruct_word_terms(base_blocks))
    one_terms = coefficient_maps(equations.reconstruct_word_terms(one_blocks))
    h_base = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, base_blocks), killed
    )
    h_one = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, one_blocks), killed
    )
    coordinates = tuple(sorted(
        set(base_terms) | set(one_terms)
        | {word for vector in basis for word in vector}
        | {(colour,) * 6 for colour in COLOURS}
    ))
    coordinates = tuple(word for word in coordinates if word not in killed)
    span = equations.cylinders.echelon(basis)
    for colour in COLOURS:
        word = (colour,) * 6
        assert word in coordinates
        assert not equations.cylinders.member({word: Q(1)}, span)

    generators = []
    for a, b in itertools.product(COLOURS, repeat=2):
        if normal_mode == "expanded":
            generators.extend(fibre_equations(
                base_terms, one_terms, basis, coordinates,
                a, b, a if a == b else None,
            ))
        else:
            generators.extend(line_fibre_equations(
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
    assert len(names) == 73 and len(set(names)) == 73
    code = "ring r=0,(" + ",".join(names) + "),dp;\n"
    code += "option(redSB);\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += "ideal G=std(I);\n"
    code += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
    code += 'print("GBSIZE"); size(G);\n'
    normal_dimension = 2 if normal_mode == "expanded" else 1
    return code, len(generators), len(coordinates), killed, normal_dimension


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--normal", choices=("line", "expanded"), default="line")
    args = parser.parse_args()
    code, generators, coordinates, killed, normal_dimension = build_problem(args.normal)
    print(
        "START", f"generators={generators}", f"coordinates={coordinates}",
        f"killed={len(killed)}", f"normal_dim={normal_dimension}", flush=True,
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
    unit = worker.marker_values(completed.stdout, "UNIT", 1)[0]
    size = worker.marker_values(completed.stdout, "GBSIZE", 1)[0]
    print(
        "RESULT", f"unit={unit}", f"gbsize={size}",
        f"seconds={time.monotonic()-started:.3f}", flush=True,
    )


if __name__ == "__main__":
    main()
