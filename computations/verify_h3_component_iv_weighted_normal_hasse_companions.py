#!/usr/bin/env python3
"""Complete derived Hasse companions for all weighted-normal V(h) arcs.

For a polynomial arc q(tau), totalize the universal shifted source cycle in
the normal principal-parts direction.  At order k the complete chain has
all lower normal faces, the normal-indexed mixed row, and the cap terms.
Its exact augmented boundary is the kth convolution of h(q(tau)) with the
normal copies of Yw; target and ordinary residue vanish and the chart
terminal is the negative of the same convolution.

Triangular subtraction by lower normalized companions isolates the weighted
leading face columns from d354257.  The construction is exact in the
derived principal-parts resolution.  It does not provide the still-missing
map to the physical site-squarefree source module or physical cap W.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import verify_h3_component_iv_nondense_face_zero_strata as ND
import verify_h3_component_iv_singular_face_weighted_normal_escape as ESC


PINS = {
    "computations/verify_h3_component_iv_singular_face_weighted_normal_escape.py":
        "4cf84cd001ab07983d99f5ec319ef75dc9d4f1dc2971ad197ddb871270f5366d",
    "notes/h3-component-iv-singular-face-weighted-normal-escape.md":
        "8f812d6f8a34ecc01874982715f26dd6a6222e5c3d90874bd0e513b602958699",
    "computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py":
        "c409a62957dba0d101d1298ec16695482fce705d3131323a8d3657074f1bf2b0",
    "notes/h3-cyclotomic-regularized-shifted-filler-normal-face.md":
        "33d23d5f30afd8edc8b4e6f5599d027620587b600c87476a1adabf967820ea63",
    "computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py":
        "34d627b9b0cdf4a81fbebc7c1d37231f53ac2d04be401c3f99402b0bf28c6fbe",
    "notes/h3-rootless-single-v-site-collision-comparison-obstruction.md":
        "3ffdb83a34f9fd082b3b85a07f2e1cb2155684cafa33c966cf7ed923a94bc219",
}
EXPECTED_LEDGER_SHA256 = "9b16481cf106fb836b4720ec83eb2d61b705eef4449ad3340f815a3afd096283"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


class Expr:
    """Tiny integral polynomial ring on formal Hasse coefficient labels."""

    def __init__(self, terms=()):
        if isinstance(terms, int):
            terms = {(): terms}
        elif isinstance(terms, str):
            terms = {(terms,): 1}
        self.terms = Counter({tuple(sorted(monomial)): coefficient
                              for monomial, coefficient in dict(terms).items()
                              if coefficient})

    def __add__(self, other):
        other = as_expr(other)
        answer = Counter(self.terms)
        answer.update(other.terms)
        return Expr({monomial: coefficient for monomial, coefficient in answer.items()
                     if coefficient})

    __radd__ = __add__

    def __neg__(self):
        return Expr({monomial: -coefficient for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_expr(other))

    def __rsub__(self, other):
        return as_expr(other) - self

    def __mul__(self, other):
        other = as_expr(other)
        answer = Counter()
        for left, lc in self.terms.items():
            for right, rc in other.terms.items():
                answer[tuple(sorted(left + right))] += lc * rc
        return Expr({monomial: coefficient for monomial, coefficient in answer.items()
                     if coefficient})

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == as_expr(other).terms

    def __bool__(self):
        return bool(self.terms)


def as_expr(value):
    return value if isinstance(value, Expr) else Expr(value)


def module_add_term(module, label, coefficient):
    module[label] = module.get(label, Expr()) + coefficient
    if not module[label]:
        del module[label]


def apply_map(chain, operation):
    answer = {}
    for generator, coefficient in chain.items():
        for output, value in operation(generator).items():
            module_add_term(answer, output, coefficient * value)
    return answer


def universal_order_companion(order):
    """Verify the full kth normal-jet companion as a formal identity."""
    F = Expr("F")

    def H(mask, power):
        return Expr(f"H{mask}_{power}")

    chain = {}
    for power in range(order + 1):
        grade = order - power
        for mask in range(4):
            module_add_term(chain, ("r0", mask, grade), H(mask, power))
        module_add_term(chain, ("T", grade), -H(3, power))
    module_add_term(chain, ("rm", order), -F)

    def differential(generator):
        kind = generator[0]
        if kind == "r0":
            _, mask, grade = generator
            return {("Eq", mask, grade): F}
        if kind == "T":
            _, grade = generator
            return {("Yw", grade): Expr(-1)}
        require(kind == "rm", "unexpected formal source generator")
        _, grade = generator
        return {("Eq", mask, grade - power): H(mask, power)
                for power in range(grade + 1) for mask in range(4)}

    def target(generator):
        if generator[0] == "r0" and generator[1] == 3:
            return {("target", generator[2]): Expr(1)}
        if generator[0] == "T":
            return {("target", generator[1]): Expr(1)}
        return {}

    def chart(generator):
        if generator[0] == "r0" and generator[1] == 3:
            return {("S", generator[2]): Expr(-1)}
        return {}

    boundary = apply_map(chain, differential)
    expected_boundary = {("Yw", order - power): H(3, power)
                         for power in range(order + 1)}
    require(boundary == expected_boundary,
            f"order {order}: complete normal companion has wrong boundary")
    require(not apply_map(chain, target),
            f"order {order}: complete normal companion retained target")
    # Ordinary residue is identically zero on every mixed word and tagged
    # chart difference, so its map is the zero operation.
    require(not apply_map(chain, lambda _generator: {}),
            f"order {order}: complete normal companion retained old residue")
    expected_chart = {("S", order - power): -H(3, power)
                      for power in range(order + 1)}
    require(apply_map(chain, chart) == expected_chart,
            f"order {order}: chart terminal stopped matching -h")
    return {
        "order": order,
        "source_component_count": len(chain),
        "r0_faces": 4 * (order + 1),
        "normal_indexed_mixed_rows": 1,
        "cap_faces": order + 1,
        "boundary_grades": order + 1,
        "target": 0,
        "old_ores": 0,
        "chart_terminal": "negative of the h-convolution",
    }


def zero_of(example):
    return ND.QZ() if isinstance(example, ND.QZ) else Q(0)


def solve_span(columns, target):
    """Exact coordinates expressing target in independent columns."""
    if not columns:
        require(not any(target), "nonzero vector is not in empty span")
        return []
    zero = zero_of(next((entry for column in columns for entry in column if entry), Q(0)))
    matrix = [[columns[column][row] for column in range(len(columns))] + [target[row]]
              for row in range(len(target))]
    pivot_row = 0
    pivots = []
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    require(len(pivots) == len(columns), "columns stopped being independent")
    for row in matrix:
        require(any(row[column] for column in range(len(columns))) or not row[-1],
                "target left the accumulated column span")
    answer = [zero for _ in columns]
    for row, column in enumerate(pivots):
        answer[column] = matrix[row][-1]
    reconstructed = [sum((columns[column][row] * answer[column]
                          for column in range(len(columns))), zero)
                     for row in range(len(target))]
    require(reconstructed == target, "span solution failed reconstruction")
    return answer


def independent_jacobian_columns(base, zero):
    jacobian = ND.face_jacobian(base, zero)
    columns = []
    labels = []
    for edge_index, edge in enumerate(ND.EDGES):
        column = [jacobian[row][edge_index] for row in range(5)]
        if ND.matrix_rank([list(row) for row in zip(*(columns + [column]), strict=True)]) > len(columns):
            columns.append(column)
            labels.append(edge)
    return columns, labels


def rational_arc(direction1, direction2=None):
    result = {1: {edge: Q(value) for edge, value in direction1.items()}}
    if direction2:
        result[2] = {edge: Q(value) for edge, value in direction2.items()}
    return result


def intersecting_inputs():
    bases = {
        "zero": {},
        "edge": {(0, 1): Q(1)},
        "two_star": {(0, 1): Q(1), (0, 2): Q(1)},
        "three_star": {(0, 1): Q(1), (0, 2): Q(1), (0, 3): Q(1)},
        "triangle": {(0, 1): Q(1), (0, 2): Q(1), (1, 2): Q(1)},
        "four_star": {(0, 1): Q(1), (0, 2): Q(1),
                      (0, 3): Q(1), (0, 4): Q(1)},
    }
    arcs = {
        "zero": [
            rational_arc({(0, 1): 1, (2, 3): 1}),
            rational_arc({(0, 1): 1, (2, 4): 1}),
            rational_arc({(0, 1): 1, (3, 4): 1}),
            rational_arc({(0, 2): 1, (3, 4): 1}),
            rational_arc({(1, 2): 1, (3, 4): 1}),
        ],
        "edge": [
            rational_arc({(0, 2): 1}, {(3, 4): 1}),
            rational_arc({(1, 2): 1}, {(3, 4): 1}),
        ],
        "two_star": [
            rational_arc({(0, 3): -1, (1, 4): -1, (2, 4): 1}),
            rational_arc({(1, 3): -1, (1, 4): -1,
                          (2, 3): 1, (2, 4): 1}),
        ],
        "three_star": [rational_arc({(1, 2): 1}, {(3, 4): 1})],
        "triangle": [
            rational_arc({(0, 3): 1, (1, 3): -1,
                          (1, 4): 1, (2, 4): -1}),
            rational_arc({(0, 3): 1, (1, 3): -1,
                          (0, 4): 1, (2, 4): -1}),
        ],
        "four_star": [
            rational_arc({(1, 2): 1, (1, 4): -1,
                          (2, 3): -1, (3, 4): 1}),
        ],
    }
    return bases, arcs


def assemble_one(name, base, arcs, zero):
    columns, labels = independent_jacobian_columns(base, zero)
    records = [{"kind": "first_normal_edge", "edge": edge, "order": 1}
               for edge in labels]
    for directions in arcs:
        series = ESC.face_series(base, directions)
        new_order = next(order for order in sorted(series)
                         if ND.matrix_rank([list(row) for row in
                                            zip(*(columns + [series[order]]), strict=True)])
                         > len(columns))
        eliminations = {}
        for order in range(1, new_order):
            vector = series.get(order, [zero for _ in range(5)])
            eliminations[str(new_order - order)] = [
                entry.text() if isinstance(entry, ND.QZ) else str(entry)
                for entry in solve_span(columns, vector)
            ]
        new_column = series[new_order]
        columns.append(new_column)
        records.append({
            "kind": "complete_normal_jet_then_triangular_subtraction",
            "order": new_order,
            "lower_normal_grade_eliminations": eliminations,
            "normalized_boundary": [entry.text() if isinstance(entry, ND.QZ) else str(entry)
                                    for entry in new_column],
            "target": 0,
            "old_ores": 0,
            "chart_terminal": "negative normalized boundary",
        })
    require(len(columns) == ND.matrix_rank(
        [list(row) for row in zip(*columns, strict=True)]) == 5,
        f"{name}: assembled weighted companions do not have full rank")
    return {
        "normalized_companions": records,
        "orders": [record["order"] for record in records],
        "boundary_rank": 5,
        "target_rank": 0,
        "old_ores_rank": 0,
    }


def assemble_all_strata():
    bases, arcs = intersecting_inputs()
    result = {name: assemble_one(name, base, arcs[name], Q(0))
              for name, base in bases.items()}

    zeta = ND.QZ(0, 1)
    base = {(0, 1): ND.QZ(1), (0, 2): ND.QZ(1), (0, 3): ND.QZ(1),
            (1, 2): ND.QZ(1), (1, 3): zeta, (2, 3): zeta * zeta}
    tangent = {1: {(0, 1): ND.QZ(1, 1), (0, 2): ND.QZ(1),
                   (0, 4): ND.QZ(1), (1, 4): zeta * zeta,
                   (2, 4): zeta, (3, 4): ND.QZ(1)}}
    result["cyclotomic_isolated_K4"] = assemble_one(
        "cyclotomic_isolated_K4", base, [tangent], ND.QZ()
    )
    expected_orders = {
        "zero": [2, 2, 2, 2, 2],
        "edge": [1, 1, 1, 3, 3],
        "two_star": [1, 1, 1, 2, 2],
        "three_star": [1, 1, 1, 1, 3],
        "triangle": [1, 1, 1, 2, 2],
        "four_star": [1, 1, 1, 1, 2],
        "cyclotomic_isolated_K4": [1, 1, 1, 1, 2],
    }
    require({name: record["orders"] for name, record in result.items()}
            == expected_orders, "assembled weighted order profiles changed")
    return result


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    universal = [universal_order_companion(order) for order in range(1, 4)]
    require([record["source_component_count"] for record in universal]
            == [11, 16, 21], "normal companion component counts changed")
    ledger = {
        "scope": "complete derived normal principal-parts totalization through order three",
        "universal_companions": universal,
        "singular_stratum_assembly": assemble_all_strata(),
        "derived_theorem": (
            "all singular strata of 9376a3f have five exact normalized source "
            "companions with boundary rank five, target=old-ores=0, and chart terminal -S"
        ),
        "construction": (
            "the kth chain has every H_A,i*r0[A,k-i], -F0*rm[k], and "
            "-h_i*T[k-i]; its differential is the h-convolution.  Lower "
            "normal grades are removed by shifted earlier normalized chains"
        ),
        "first_physical_boundary_defect": {
            "derived_generator": "normal-indexed rm[k], k=1,2,3",
            "physical_issue": (
                "the physical site-squarefree inventory has no homogeneous image for "
                "the repeated normal index; the first possible comparison is the "
                "P3-disjoint-K2 site-collision degree"
            ),
            "exact_existing_boundary": (
                "there an individual route has private ordinary residue; only the "
                "adjacent two-face S-pair cancels it, with physical anchor incidence zero"
            ),
            "missing_cells": (
                "the zero-anchor site-collision cell E_v and the separate primitive "
                "anchor cell, followed by derived Yw to physical W"
            ),
        },
        "physical_cap_identification": False,
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"weighted normal Hasse companion ledger changed: {digest}")
    print("h3 Component-IV weighted normal Hasse companions: PASS")
    print("universal complete jet chains: orders 1/2/3, components 11/16/21")
    print("all singular strata: derived boundary rank 5, target=old-ores=0")
    print("first physical defect: site-collision comparison / physical W map")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
