#!/usr/bin/env python3
"""Search small safe coordinate quotients for the remaining E22 direction.

This is reconnaissance only.  It keeps the endpoint-ordered matching and
cylinder implementation used by the audited adjacent-line proofs, but tries
arbitrary retained subsets of the nine A23 coordinate blocks.  A record is
reported when the projected direct tensor belongs to each four-cut normal
and at least two diagonal target words remain outside that normal.
"""

from __future__ import annotations

import argparse
import itertools

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


Q = full.Q
DIAGONAL_BITS = {0: 0, 1: 4, 2: 8}


def select_e22():
    adjacent.T_CELL = (2, 2)
    adjacent.T_BLOCK, adjacent.T_DETAILS = adjacent.variable_coordinate_block(
        adjacent.T_EDGE, adjacent.T_CELL
    )


def x_character_rows():
    fixed = (
        ((0, 1), (0, 0)), ((4, 5), (0, 0)),
        ((0, 2), (1, 1)), ((1, 4), (1, 1)),
        ((0, 4), (2, 2)), ((1, 3), (2, 2)),
        ((2, 5), (0, 0)), ((3, 5), (1, 0)),
    )
    constraints = sp.Matrix.vstack(*(
        adjacent.cell_weight(edge, cell) for edge, cell in fixed
    ))
    kernel = sp.Matrix.hstack(*constraints.nullspace())
    return tuple(
        adjacent.cell_weight((2, 3), cell) * kernel for cell in full.CELLS
    )


def independent_support(support, rows):
    selected = [rows[bit] for bit in support]
    if not selected:
        return True
    return sp.Matrix.vstack(*selected).rank() == len(selected)


def geometry(retained, support):
    coefficients = {full.CELLS[bit]: Q(1) for bit in support}
    blocks = adjacent.blocks_for(coefficients, Q(1))
    killed = adjacent.quotient_killed(retained, retain_t=True)
    hs = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, blocks), killed
    )
    records = []
    for cut in (0, 1, 5):
        normal = full.projected_cylinder_intersection(
            (2, 3, 4, cut), blocks, killed
        )
        span = equations.cylinders.echelon(normal)
        active = tuple(
            colour for colour, bit in DIAGONAL_BITS.items()
            if bit in retained
            and (colour,) * 6 not in killed
            and not equations.cylinders.member({(colour,) * 6: Q(1)}, span)
        )
        direct = equations.cylinders.member(hs, span)
        records.append((cut, len(normal), active, direct))
    return tuple(records), len(killed)


def masks(bits):
    bits = tuple(bits)
    for selector in range(1 << len(bits)):
        yield tuple(bits[index] for index in range(len(bits)) if selector & (1 << index))


def atom_vector(terms, p_endpoint, q_endpoint):
    answer = {}
    for word, values in terms.items():
        total = Q(0)
        for (left, right), coefficient in values:
            if left == p_endpoint and right == q_endpoint:
                total += coefficient
            if right == p_endpoint and left == q_endpoint:
                total += coefficient
        if total:
            answer[word] = total
    return answer


def subtract_target(vector, colour):
    answer = dict(vector)
    equations.cylinders.add(answer, (colour,) * 6, Q(-1))
    return answer


def sparse_point(retained=(0, 1, 4), support=(0, 1)):
    blocks = adjacent.blocks_for(
        {full.CELLS[bit]: Q(1) for bit in support}, Q(1)
    )
    killed = adjacent.quotient_killed(retained, retain_t=True)
    terms = adjacent.projected_terms(blocks, killed)
    normal = full.projected_cylinder_intersection((2, 3, 4, 0), blocks, killed)
    span = equations.cylinders.echelon(normal)
    endpoints = tuple(itertools.product(full.SIX, full.COLOURS))
    atoms = {
        (left, right): atom_vector(terms, left, right)
        for left in endpoints for right in endpoints
    }
    diagonal = {
        colour: tuple(
            (left, right) for left in endpoints for right in endpoints
            if equations.cylinders.member(
                subtract_target(atoms[left, right], colour), span
            )
        )
        for colour in (0, 1)
    }
    zero = {
        pair for pair, vector in atoms.items()
        if equations.cylinders.member(vector, span)
    }
    print("SPARSE", "retained", retained, "support", support,
          "diagonal_counts", {c: len(v) for c, v in diagonal.items()},
          "zero_pairs", len(zero))
    for p0, q0 in diagonal[0]:
        for p1, q1 in diagonal[1]:
            if (p0, q1) in zero and (p1, q0) in zero:
                print("SPARSE_POINT", "p0", p0, "q0", q0,
                      "p1", p1, "q1", q1)
                audit_sparse_point(
                    blocks, killed, terms, normal, p0, q0, p1, q1
                )
                return
    print("SPARSE_POINT none")


def remainder(vector, basis):
    answer = dict(vector)
    for pivot, row in equations.cylinders.echelon(basis).items():
        if pivot not in answer:
            continue
        multiple = answer[pivot]
        for word, coefficient in row.items():
            equations.cylinders.add(answer, word, -multiple * coefficient)
    return answer


def audit_sparse_point(blocks, killed, terms, safe_normal, p0, q0, p1, q1):
    full_terms = equations.reconstruct_word_terms(blocks)
    full_atoms = {
        pair: atom_vector(full_terms, *pair)
        for pair in ((p0, q0), (p1, q1), (p0, q1), (p1, q0))
    }
    residuals = {
        "00": subtract_target(full_atoms[p0, q0], 0),
        "11": subtract_target(full_atoms[p1, q1], 1),
        "01": full_atoms[p0, q1],
        "10": full_atoms[p1, q0],
    }
    projected_residuals = {
        name: full.project_vector(vector, killed)
        for name, vector in residuals.items()
    }
    safe_span = equations.cylinders.echelon(safe_normal)
    assert all(
        equations.cylinders.member(vector, safe_span)
        for vector in projected_residuals.values()
    )
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    for cut in (0, 1, 5):
        actual = full.projected_cylinder_intersection(
            (2, 3, 4, cut), blocks, set()
        )
        actual_span = equations.cylinders.echelon(actual)
        projected_actual = [full.project_vector(vector, killed) for vector in actual]
        projected_actual = [vector for vector in projected_actual if vector]
        projected_actual_span = equations.cylinders.echelon(projected_actual)
        print(
            "UNREDUCED", "cut", cut,
            "normal_dim", len(actual),
            "projected_actual_dim", len(projected_actual_span),
            "safe_dim", len(safe_normal),
            "hs_in", equations.cylinders.member(hs, actual_span),
            "target_absorbed", tuple(
                equations.cylinders.member({(c,) * 6: Q(1)}, actual_span)
                for c in full.COLOURS
            ),
        )
        for name, vector in residuals.items():
            projected = projected_residuals[name]
            rem = remainder(vector, actual)
            print(
                " RESIDUAL", name,
                "actual_member", equations.cylinders.member(vector, actual_span),
                "projected_actual_member",
                equations.cylinders.member(projected, projected_actual_span),
                "safe_member", equations.cylinders.member(projected, safe_span),
                "remainder_terms", len(rem),
                "remainder", tuple(sorted(rem.items())),
            )


def canonical(vector, basis):
    return tuple(sorted(remainder(vector, basis).items()))


def add_scaled(target, source, scalar):
    for word, coefficient in source.items():
        equations.cylinders.add(target, word, scalar * coefficient)


def small_vectors(endpoints, level):
    answer = []
    for endpoint in endpoints:
        for sign in (-1, 1):
            answer.append(((endpoint, sign),))
    if level >= 2:
        for left, right in itertools.combinations(endpoints, 2):
            for left_sign, right_sign in itertools.product((-1, 1), repeat=2):
                answer.append(((left, left_sign), (right, right_sign)))
    return tuple(answer)


def bilinear_from_atoms(atoms, left, right):
    answer = {}
    for left_endpoint, left_value in left:
        for right_endpoint, right_value in right:
            add_scaled(
                answer, atoms[left_endpoint, right_endpoint],
                Q(left_value * right_value),
            )
    return answer


def sparse_level_point(retained, support, level):
    blocks = adjacent.blocks_for(
        {full.CELLS[bit]: Q(1) for bit in support}, Q(1)
    )
    killed = adjacent.quotient_killed(retained, retain_t=True)
    terms = adjacent.projected_terms(blocks, killed)
    normal = full.projected_cylinder_intersection((2, 3, 4, 0), blocks, killed)
    endpoints = tuple(itertools.product(full.SIX, full.COLOURS))
    atoms = {
        (left, right): atom_vector(terms, left, right)
        for left in endpoints for right in endpoints
    }
    vectors = small_vectors(endpoints, level)
    targets = {
        colour: canonical({(colour,) * 6: Q(1)}, normal)
        for colour in (0, 1)
    }
    diagonal = {0: [], 1: []}
    zero_pairs = set()
    for left_index, left in enumerate(vectors):
        for right_index, right in enumerate(vectors):
            value = canonical(bilinear_from_atoms(atoms, left, right), normal)
            if not value:
                zero_pairs.add((left_index, right_index))
            for colour in (0, 1):
                if value == targets[colour]:
                    diagonal[colour].append((left_index, right_index))
    print(
        "SPARSE_LEVEL", level, "vectors", len(vectors),
        "diagonal_counts", {c: len(v) for c, v in diagonal.items()},
        "zero_pairs", len(zero_pairs), flush=True,
    )
    for p0_index, q0_index in diagonal[0]:
        for p1_index, q1_index in diagonal[1]:
            if (
                (p0_index, q1_index) in zero_pairs
                and (p1_index, q0_index) in zero_pairs
            ):
                print(
                    "SPARSE_LEVEL_POINT",
                    "p0", vectors[p0_index], "q0", vectors[q0_index],
                    "p1", vectors[p1_index], "q1", vectors[q1_index],
                )
                audit_vector_point(
                    blocks, killed, normal, vectors[p0_index],
                    vectors[q0_index], vectors[p1_index], vectors[q1_index],
                )
                return
    print("SPARSE_LEVEL_POINT none")


def x01_lift_census():
    retained = (0, 1, 4)
    killed = adjacent.quotient_killed(retained, retain_t=True)
    later = (2, 3, 5, 6, 7, 8)
    census = {}
    failures = []
    for selector in range(1 << len(later)):
        support = (0, 1) + tuple(
            bit for index, bit in enumerate(later) if selector & (1 << index)
        )
        coefficients = {full.CELLS[bit]: Q(1) for bit in support}
        blocks = adjacent.blocks_for(coefficients, Q(1))
        hs = full.project_vector(
            equations.cylinders.matching_tensor(full.SIX, blocks), killed
        )
        for cut in (0, 1, 5):
            actual = full.projected_cylinder_intersection(
                (2, 3, 4, cut), blocks, set()
            )
            projected = [full.project_vector(vector, killed) for vector in actual]
            projected = [vector for vector in projected if vector]
            projected = list(equations.cylinders.echelon(projected).values())
            key = (len(actual), len(projected))
            census[key] = census.get(key, 0) + 1
            if not equations.same_span(projected, (hs,)):
                failures.append((support, cut, key, projected, hs))
    print("X01_LIFT_CENSUS", census, "failures", len(failures))
    for failure in failures[:10]:
        print(" LIFT_FAILURE", failure)


def full_normal_census():
    census = {}
    failures = []
    for mask in range(1 << 9):
        coefficients = {
            full.CELLS[bit]: Q(1) for bit in range(9) if mask & (1 << bit)
        }
        blocks = adjacent.blocks_for(coefficients, Q(1))
        hs = equations.cylinders.matching_tensor(full.SIX, blocks)
        for cut in (0, 1, 5):
            normal = full.projected_cylinder_intersection(
                (2, 3, 4, cut), blocks, set()
            )
            census[len(normal)] = census.get(len(normal), 0) + 1
            if not equations.same_span(normal, (hs,)):
                failures.append((mask, cut, len(normal)))
    print("FULL_NORMAL_CENSUS", census, "failures", len(failures))
    print(" FULL_NORMAL_FAILURES", failures[:80])


def audit_vector_point(blocks, killed, safe_normal, p0, q0, p1, q1):
    full_terms = equations.reconstruct_word_terms(blocks)
    endpoints = tuple(itertools.product(full.SIX, full.COLOURS))
    full_atoms = {
        (left, right): atom_vector(full_terms, left, right)
        for left in endpoints for right in endpoints
    }
    residuals = {
        "00": subtract_target(bilinear_from_atoms(full_atoms, p0, q0), 0),
        "11": subtract_target(bilinear_from_atoms(full_atoms, p1, q1), 1),
        "01": bilinear_from_atoms(full_atoms, p0, q1),
        "10": bilinear_from_atoms(full_atoms, p1, q0),
    }
    safe_span = equations.cylinders.echelon(safe_normal)
    projected_residuals = {
        name: full.project_vector(vector, killed)
        for name, vector in residuals.items()
    }
    assert all(
        equations.cylinders.member(vector, safe_span)
        for vector in projected_residuals.values()
    )
    for cut in (0, 1, 5):
        actual = full.projected_cylinder_intersection(
            (2, 3, 4, cut), blocks, set()
        )
        actual_span = equations.cylinders.echelon(actual)
        print("VECTOR_UNREDUCED", "cut", cut, "normal_dim", len(actual))
        for name, vector in residuals.items():
            rem = remainder(vector, actual)
            print(
                " VECTOR_RESIDUAL", name,
                "actual_member", equations.cylinders.member(vector, actual_span),
                "remainder_terms", len(rem),
                "remainder", tuple(sorted(rem.items())),
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-retained", type=int, default=5)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--sparse-point", action="store_true")
    parser.add_argument("--retained", default="0,1,4")
    parser.add_argument("--support", default="0,1")
    parser.add_argument("--sparse-level", type=int, default=1)
    parser.add_argument("--lift-census", action="store_true")
    parser.add_argument("--full-normal-census", action="store_true")
    args = parser.parse_args()
    select_e22()
    if args.lift_census:
        x01_lift_census()
        return
    if args.full_normal_census:
        full_normal_census()
        return
    if args.sparse_point:
        retained = tuple(map(int, args.retained.split(","))) if args.retained else ()
        support = tuple(map(int, args.support.split(","))) if args.support else ()
        if args.sparse_level == 1:
            sparse_point(retained, support)
        else:
            sparse_level_point(retained, support, args.sparse_level)
        return
    rows = x_character_rows()
    safe = []
    for size in range(2, min(9, args.max_retained) + 1):
        for retained in itertools.combinations(range(9), size):
            if sum(bit in retained for bit in DIAGONAL_BITS.values()) < 2:
                continue
            for support in masks(retained):
                if not independent_support(support, rows):
                    continue
                records, killed = geometry(retained, support)
                if all(direct and len(active) >= 2 for _cut, _dim, active, direct in records):
                    safe.append((retained, support, records, killed))
                    if args.all:
                        print("SAFE", retained, support, records, "killed", killed)
    print("safe_count", len(safe))
    for record in safe[:80]:
        print("SAFE", *record)


if __name__ == "__main__":
    main()
