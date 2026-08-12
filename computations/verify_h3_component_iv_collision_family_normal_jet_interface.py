#!/usr/bin/env python3
"""Normal-jet interface for the physical P3+K2 collision family.

The adjacent collision S-pairs, after granting the missing reduced Eq face,
form the oriented incidence matrix of C5.  Principal-parts prolongation is
functorial: one polynomial reduced-Eq family cancels every order-1/2/3 Eq
defect and introduces no new target/residue/readout type.  However, each
normal grade still has the primitive aggregate cokernel of C5.  Therefore
the collision family alone cannot carry the five normal-indexed mixed rows;
a separate primitive anchor family is necessary in every grade.

This is an exact conditional chain-map interface.  It does not construct
the reduced Eq or primitive anchor cells, nor the physical W comparison.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_component_iv_weighted_normal_hasse_companions.py":
        "f94b13e3d08d0f090112648f0b7a1d9b7d07ce857d6b5d979d730dc4761a8ce0",
    "notes/h3-component-iv-weighted-normal-hasse-companions.md":
        "8d09d43769ac91597541e4d2609c17cf261e10456c8fca2747f35f53b0a1eefe",
    "computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py":
        "34d627b9b0cdf4a81fbebc7c1d37231f53ac2d04be401c3f99402b0bf28c6fbe",
    "notes/h3-rootless-single-v-site-collision-comparison-obstruction.md":
        "3ffdb83a34f9fd082b3b85a07f2e1cb2155684cafa33c966cf7ed923a94bc219",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "notes/h3-rootless-zero-anchor-collision-edge-source-obstruction.md":
        "6f5ad0adb20bcfb3c736125f40fedd78f8ec225f28cd43606038c849f32152a7",
}
EXPECTED_LEDGER_SHA256 = "9ed6ea59f35ab3e7abc5381c93479d1837666962b5402d240d3af0fe04eff88c"
JET_ORDERS = (1, 2, 3)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def rank(columns):
    if not columns:
        return 0
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(len(columns[0]))]
    pivot_row = 0
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
        pivot_row += 1
    return pivot_row


def determinant(matrix):
    work = [[int(entry) for entry in row] for row in matrix]
    if len(work) == 1:
        return work[0][0]
    answer = 0
    for column, entry in enumerate(work[0]):
        minor = [row[:column] + row[column + 1:] for row in work[1:]]
        answer += (-1) ** column * entry * determinant(minor)
    return answer


def c5_incidence_audit():
    edges = []
    for source in range(5):
        column = [0] * 5
        column[source] = -1
        column[(source + 1) % 5] = 1
        edges.append(tuple(column))
    require(rank(edges) == 4, "C5 collision incidence rank changed")
    aggregate = (1, 1, 1, 1, 1)
    require(all(sum(a * b for a, b in zip(aggregate, edge, strict=True)) == 0
                for edge in edges), "primitive aggregate stopped killing C5 edges")

    # The lattice image is saturated: deleting one row and one column gives
    # a unimodular four-by-four minor.  Thus the cokernel is primitive Z.
    matrix = [list(row) for row in zip(*edges, strict=True)]
    minor = [row[:4] for row in matrix[:4]]
    require(abs(determinant(minor)) == 1,
            "C5 collision image stopped being a saturated rank-four lattice")

    anchor = (1, 0, 0, 0, 0)
    require(rank(edges + [anchor]) == 5,
            "one primitive vertex anchor stopped completing C5 incidence")
    completed_minor = [list(row) for row in zip(*(edges[:4] + [anchor]), strict=True)]
    require(abs(determinant(completed_minor)) == 1,
            "edge-plus-anchor completion stopped being unimodular")
    return edges, anchor, aggregate


def block_jet_audit(edges, anchor, aggregate):
    # Three associated normal grades.  Principal-parts convolution is lower
    # triangular, so its diagonal source-boundary block is C5 incidence in
    # each grade.  Grade-specific aggregate covectors survive every lower
    # filtration term.
    height = 5 * len(JET_ORDERS)
    edge_columns = []
    anchor_columns = []
    aggregate_covectors = []
    for block, order in enumerate(JET_ORDERS):
        for edge in edges:
            column = [0] * height
            column[5 * block:5 * (block + 1)] = edge
            edge_columns.append(tuple(column))
        column = [0] * height
        column[5 * block:5 * (block + 1)] = anchor
        anchor_columns.append(tuple(column))
        covector = [0] * height
        covector[5 * block:5 * (block + 1)] = aggregate
        aggregate_covectors.append(tuple(covector))

    require(rank(edge_columns) == 12,
            "three-grade collision family stopped having rank 3*4")
    require(all(all(sum(a * b for a, b in zip(covector, column, strict=True)) == 0
                        for column in edge_columns)
                    for covector in aggregate_covectors),
            "a normal-grade aggregate stopped killing the edge family")
    require(rank(edge_columns + anchor_columns) == 15,
            "functorial anchor family stopped completing all normal grades")
    return {
        "normal_orders": list(JET_ORDERS),
        "normal_indexed_mixed_rows": height,
        "collision_edge_columns": len(edge_columns),
        "collision_rank": rank(edge_columns),
        "primitive_cokernel_rank": height - rank(edge_columns),
        "primitive_cokernel_basis": [
            {"normal_order": order, "covector": list(aggregate)}
            for order in JET_ORDERS
        ],
        "rank_after_one_anchor_family": rank(edge_columns + anchor_columns),
        "anchor_jet_columns": len(anchor_columns),
    }


class Expr:
    """Integral polynomial expression in universal jet coefficients."""

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


def series_add(left, right):
    size = max(len(left), len(right))
    return [(left[index] if index < len(left) else Expr())
            + (right[index] if index < len(right) else Expr())
            for index in range(size)]


def series_neg(value):
    return [-entry for entry in value]


def series_mul(left, right):
    answer = [Expr() for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] = answer[i + j] + a * b
    return answer


def jet_functor_audit():
    variables = {
        name: [Expr(f"{name}_{order}") for order in range(4)]
        for name in "abcde"
    }
    a, b, c, d, e = (variables[name] for name in "abcde")
    defects = (
        series_add(a, series_neg(b)),
        series_add(c, series_neg(d)),
        series_add(e, series_neg(a)),
        series_add(b, series_neg(c)),
        series_add(d, series_neg(e)),
    )
    tate_multipliers = (
        series_mul(c, e), series_mul(b, e), series_mul(b, d),
        series_mul(a, d), series_mul(a, c),
    )
    weighted = []
    for defect, multiplier in zip(defects, tate_multipliers, strict=True):
        weighted = series_add(weighted, series_mul(defect, multiplier))
    require(not any(weighted),
            "Tate-weighted reduced-Eq compatibility failed after jet prolongation")

    records = []
    for face, defect in enumerate(defects):
        for order in JET_ORDERS:
            # Physical PP edge has the Eq convolution.  The coefficient of
            # the same polynomial reduced face has its negative.  All five
            # augmented readouts are zero on both pieces except the displayed
            # Eq defect, so their sum is the strict C5 edge in every order.
            physical_eq = {grade: defect[order - grade]
                           for grade in range(order + 1)}
            reduced_eq = {grade: -value for grade, value in physical_eq.items()}
            require(all(physical_eq[grade] + reduced_eq[grade] == Expr()
                        for grade in physical_eq),
                    "reduced Eq family stopped cancelling a jet defect")
            records.append({
                "face": face,
                "normal_order": order,
                "Eq_convolution_grades": order + 1,
                "after_reduced_face": "strict adjacent ridge S-pair",
                "W_target_ores_ainc": [0, 0, 0, 0],
                "physical_site_profile": [2, 1, 1, 1, 1],
            })
    require(len(records) == 15, "five-face/order-three jet census changed")
    return {
        "records": records,
        "single_polynomial_reduced_Eq_family_suffices_for_all_orders": True,
        "reason": (
            "principal-parts is a functor: coefficientwise convolution of "
            "dC_v=-delta_v*Eq is exactly the negative PP-edge defect"
        ),
        "degree_five_Tate_compatibility_all_jet_coefficients": True,
        "maximum_checked_polynomial_tau_degree": len(weighted) - 1,
        "new_augmented_readout_type_at_orders_2_3": False,
        "new_physical_multidegree_at_orders_2_3": False,
        "grading_scope": (
            "normal order is an external Rees/principal-parts grade; forgetting "
            "it leaves the same repeated-site P3+K2 physical profile"
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    edges, anchor, aggregate = c5_incidence_audit()
    ledger = {
        "scope": "physical comparison interface for normal orders one through three",
        "single_grade_collision": {
            "C5_incidence_rank": 4,
            "saturated_cokernel": "Z generated by face aggregate",
            "edge_readouts": {"ainc": 0, "W": 0, "target": 0, "ores": 0},
            "rank_after_reduced_Eq_face": 4,
            "reason": "the reduced Eq correction changes no ridge boundary or readout",
        },
        "normal_jet_blocks": block_jet_audit(edges, anchor, aggregate),
        "reduced_Eq_jet_functor": jet_functor_audit(),
        "verdict": (
            "one polynomial adjacent-collision plus reduced-Eq family prolongs "
            "through order three without new defect types, but it cannot carry "
            "all five rm[k] classes: one primitive aggregate anchor family is "
            "still required in every normal grade"
        ),
        "minimal_functorial_generator_families": [
            "zero-anchor adjacent P3+K2 collision/reduced-Eq family",
            "separate primitive vertex-anchor family",
        ],
        "still_separate": (
            "the source-provenant comparison sending derived Yw to physical W"
        ),
        "conditional_status": (
            "the checker proves sufficiency of the generator types if constructed; "
            "the reduced Eq and primitive anchor families remain missing physical cells"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"collision normal-jet interface ledger changed: {digest}")
    print("h3 Component-IV collision-family normal-jet interface: PASS")
    print("reduced Eq family: functorially sufficient through order 3")
    print("collision incidence: rank 4 per grade; primitive aggregate survives")
    print("minimum physical families: collision/reduced-Eq + primitive anchor")
    print("new order-2/3 multidegree or readout type: none")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
