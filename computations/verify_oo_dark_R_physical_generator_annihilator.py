#!/usr/bin/env python3
"""Resolve a fully typed dark residual by physical Fredholm duality.

For complete lifted columns C, a Cartan connector G, and a component
potential y, put R=G-Cy.  Component-exactness only gives pi_M R=0.  This
checker starts after the stronger physical statement J0 R=0, where J0 is
the complete protected map in one fine grade, and classifies the value of
the physical six-term/anchor readout q.

* q(R) != 0: normalize R to the protected-zero relative anchor.
* q(R) = 0 but q is nonzero elsewhere on ker J0: another kernel class is
  the relative anchor; R alone does not decide the branch.
* q kills all of ker J0: q=lambda J0, and (-lambda,1) is the complete left
  separator of (J0,q).

An arbitrary component or chart charge cannot replace q.  The smallest
guard has one protected row and a two-dimensional kernel: a component
charge detects R while physical anchor incidence detects a different kernel
class.  Normalizing by the component charge gives no physical generator.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    # a60ee53
    "computations/verify_oo_dark_potential_source_promotion_counterguard.py":
        "76bdd6c8ce19cc466995b235bade9114d7d2779b74bfcd25eea703c2d1de3db2",
    # 0373033
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
    # 6824c9e
    "computations/verify_uniform_cartan_critical_component_placement_gate.py":
        "68c56c1a9144dd92fa803962697de60b78b58a125191450f1af1abcd1befe2a1",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
}
EXPECTED_LEDGER_SHA256 = "65ecec226f94bf8771af9d10ccabad41e95e6b43bcb1b12a4d5de4f462b3bf74"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rref(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return work, ()
    pivots = []
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, tuple(pivots)


def rank(rows):
    return len(rref(rows)[1]) if rows else 0


def nullspace(rows, width):
    if not rows:
        return tuple(tuple(Q(int(column == free)) for column in range(width))
                     for free in range(width))
    reduced, pivots = rref(rows)
    free_columns = tuple(column for column in range(width)
                         if column not in pivots)
    answer = []
    for free in free_columns:
        vector = [Q(0)] * width
        vector[free] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        answer.append(tuple(vector))
    require(all(all(dot(row, vector) == 0 for row in rows)
                for vector in answer), "nullspace reconstruction failed")
    return tuple(answer)


def solve_row_combination(rows, target):
    """Return lambda with lambda*rows=target, or None."""
    if not rows:
        return () if not any(target) else None
    variables = len(rows)
    equations = [list(column) + [Q(value)] for column, value in
                 zip(zip(*rows, strict=True), target, strict=True)]
    reduced, pivots = rref(equations)
    if any(not any(row[:variables]) and row[variables] for row in reduced):
        return None
    answer = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            answer[pivot] = reduced[row][variables]
    require(all(sum(answer[row] * Q(rows[row][column])
                    for row in range(variables)) == Q(target[column])
                for column in range(len(target))),
            "row factorization reconstruction failed")
    return tuple(answer)


def classify(rows, physical_q, residual):
    width = len(physical_q)
    require(len(residual) == width
            and all(len(row) == width for row in rows), "width changed")
    require(all(dot(row, residual) == 0 for row in rows),
            "R is not a protected kernel class")
    residual_value = dot(physical_q, residual)
    kernel = nullspace(rows, width)
    if residual_value:
        generator = tuple(value / residual_value for value in residual)
        require(all(dot(row, generator) == 0 for row in rows)
                and dot(physical_q, generator) == 1,
                "R normalization failed")
        return "R_generator", generator, None

    other = next((vector for vector in kernel if dot(physical_q, vector)), None)
    if other is not None:
        value = dot(physical_q, other)
        generator = tuple(entry / value for entry in other)
        require(all(dot(row, generator) == 0 for row in rows)
                and dot(physical_q, generator) == 1,
                "other-kernel normalization failed")
        return "other_kernel_generator", generator, None

    factor = solve_row_combination(rows, physical_q)
    require(factor is not None,
            "q killed the kernel but did not factor through J0")
    # The augmented column of x is (J0*x,q*x); (-lambda,1) kills it.
    for column in range(width):
        value = -sum(factor[row] * Q(rows[row][column])
                     for row in range(len(rows))) + Q(physical_q[column])
        require(value == 0, "left Fredholm separator changed")
    return "physical_left_separator", None, factor


def audit_three_exact_branches():
    rows = ((Q(1), Q(0), Q(0)),)
    residual = (Q(0), Q(1), Q(0))

    r_visible = classify(rows, (Q(0), Q(1), Q(0)), residual)
    other_visible = classify(rows, (Q(0), Q(0), Q(1)), residual)
    separator = classify(rows, (Q(1), Q(0), Q(0)), residual)
    require(r_visible == ("R_generator", residual, None),
            "the R-visible branch changed")
    require(other_visible == (
        "other_kernel_generator", (Q(0), Q(0), Q(1)), None
    ), "the R-dark/other-visible branch changed")
    require(separator == (
        "physical_left_separator", None, (Q(1),)
    ), "the separator branch changed")

    # Smallest useful typing guard: chi is a critical-component charge,
    # q_anchor is the physical six-term/anchor row.  The former sees R while
    # the latter sees a different protected kernel class.
    component_charge = (Q(0), Q(1), Q(0))
    physical_anchor = (Q(0), Q(0), Q(1))
    require(dot(component_charge, residual) == 1
            and dot(physical_anchor, residual) == 0,
            "component/physical readout guard changed")
    component_normalized = residual
    require(dot(physical_anchor, component_normalized) == 0,
            "a component generator became a physical anchor")

    return {
        "protected_map": [[1, 0, 0]],
        "protected_kernel_dimension": 2,
        "dark_residual_R": [0, 1, 0],
        "R_visible_physical_q": {
            "q": [0, 1, 0], "outcome": r_visible[0],
        },
        "R_killed_but_other_kernel_visible": {
            "q": [0, 0, 1], "outcome": other_visible[0],
            "consequence": "q(R)=0 does not imply a separator",
        },
        "whole_kernel_killed": {
            "q": [1, 0, 0], "outcome": separator[0],
            "lambda": [1], "left_separator": [-1, 1],
        },
        "arbitrary_component_charge_guard": {
            "component_charge": [0, 1, 0],
            "physical_anchor": [0, 0, 1],
            "component_charge_on_R": 1,
            "physical_anchor_on_R": 0,
            "verdict": (
                "normalization by a component charge produces no physical "
                "anchor; the readout must be the physically typed q"
            ),
        },
    }


def exhaustive_binary_R_guard():
    counts = Counter()
    cases = 0
    for height in range(3):
        for width in range(1, 5):
            for matrix_bits in product((0, 1), repeat=height * width):
                rows = tuple(tuple(Q(matrix_bits[row * width + column])
                                   for column in range(width))
                             for row in range(height))
                kernel = nullspace(rows, width)
                # Enumerate the complete binary subset of ker J0, including
                # zero; rational kernel witnesses are still used by classify.
                residuals = tuple(
                    tuple(Q(value) for value in values)
                    for values in product((0, 1), repeat=width)
                    if all(dot(row, values) == 0 for row in rows)
                )
                require(residuals, "a protected map lost zero residual")
                for q_values in product((0, 1), repeat=width):
                    physical_q = tuple(Q(value) for value in q_values)
                    for residual in residuals:
                        branch, generator, factor = classify(
                            rows, physical_q, residual
                        )
                        if branch.endswith("generator"):
                            require(generator is not None
                                    and factor is None,
                                    "a generator branch acquired lambda")
                        else:
                            require(generator is None and factor is not None,
                                    "a separator branch lost lambda")
                        # If this R is dark but another kernel class is seen,
                        # the result must be the middle branch.
                        if dot(physical_q, residual) == 0:
                            visible_elsewhere = any(
                                dot(physical_q, vector) for vector in kernel
                            )
                            require((branch == "other_kernel_generator")
                                    == visible_elsewhere,
                                    "R-dark global-kernel test changed")
                        counts[branch] += 1
                        cases += 1
    require(cases == 13004 and counts == Counter({
        "other_kernel_generator": 5640,
        "R_generator": 4724,
        "physical_left_separator": 2640,
    }),
            ("binary R census changed", cases, counts))
    return {
        "packets": cases,
        "branches": dict(sorted(counts.items())),
        "exhausted_heights": [0, 1, 2],
        "exhausted_widths": [1, 2, 3, 4],
    }


def audit_pinned_interfaces(dark, derived, placement, six_term, anchor):
    type_split = dark.audit_smallest_type_split_counterguard()
    unsaturated = dark.audit_unsaturated_projection_counterguard()
    require(not type_split["same_row_kernel_available"]
            and not type_split["literal_outside_contaminant"],
            "a60ee53 type-split guard changed")
    require(not unsaturated["projection_component_saturated"]
            and not unsaturated["typed_exit_valid"],
            "a60ee53 saturation guard changed")

    _packets, derived_branches = derived.physical_dichotomy_mutation_guard()
    require(set(derived_branches) == {
        "zero_indeterminate", "relative_generator"
    }, "0373033 physical dichotomy changed")

    placed = placement.audit_saturated_exit_interface()
    dark_boundary = placement.audit_dark_boundary(dark)
    require(placed["critical_projection_nonzero"]
            and "R=G-Cy" in dark_boundary["dark_branch_identity"],
            "6824c9e critical placement/dark identity changed")

    six_matrix = six_term.audit_binary_matrices()
    require(six_matrix["binary_complete_maps"] == 5050,
            "the exhaustive six-term alternative changed")

    physical = anchor.audit()
    require(physical["physical_covector"]
            == "Lambda=sum_6 selected matching rows - ainc"
            and physical["pairings"]["desired_boundary_zero_anchor"] == 1,
            "the physical anchor covector changed")

    return {
        "pinned_commits": {
            "a60ee53": (
                "R=G-Cy complete-lift/type-split and saturation guards"
            ),
            "0373033": (
                "zero-indeterminacy or normalized relative generator"
            ),
            "6824c9e": (
                "nonzero exact-fine-label Cartan critical placement"
            ),
        },
        "dark_complete_lift_guard": type_split["verdict"],
        "unsaturated_projection_guard": unsaturated["verdict"],
        "critical_projection_nonzero":
            placed["critical_projection_nonzero"],
        "physical_readout": physical["physical_covector"],
        "physical_readout_on_desired_anchor":
            physical["pairings"]["desired_boundary_zero_anchor"],
        "exhaustive_relative_maps_audited":
            six_matrix["binary_complete_maps"],
    }


def main():
    pin_dependencies()
    dark = load(
        "computations/verify_oo_dark_potential_source_promotion_counterguard.py",
        "dark_R_dark",
    )
    derived = load(
        "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py",
        "dark_R_derived",
    )
    placement = load(
        "computations/verify_uniform_cartan_critical_component_placement_gate.py",
        "dark_R_placement",
    )
    six_term = load(
        "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py",
        "dark_R_six_term",
    )
    anchor = load(
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py",
        "dark_R_anchor",
    )

    ledger = {
        "theorem": "dark complete-kernel physical generator/annihilator alternative",
        "pinned_interfaces": audit_pinned_interfaces(
            dark, derived, placement, six_term, anchor
        ),
        "three_exact_branches": audit_three_exact_branches(),
        "binary_R_mutation_guard": exhaustive_binary_R_guard(),
        "physical_theorem": (
            "let R=G-Cy lie in ker J0 for the complete protected physical "
            "map in one fine grade, and let q=sum_6(m_i)-ainc be the physical "
            "anchor readout.  If q(R)!=0, R/q(R) is the protected-zero "
            "relative anchor.  If q(R)=0, inspect all of ker J0: another "
            "q-visible class is the generator, while q(ker J0)=0 is "
            "equivalent to q=lambda J0 and gives the left separator "
            "(-lambda,1) of (J0,q)"
        ),
        "required_typing": [
            "C,G,y and R are defined in one physical word/fine/repeated grade",
            "J0 retains literal boundary,D,W,target,ordinary-residue,Eq and every required protected row",
            "J0(G)=J0(C)y; pi_M(R)=0 alone is insufficient",
            "q is the physical six-term/pentagon anchor readout on the whole relative domain, not a component charge or chart-odd marked value",
            "on protected-zero classes q=sum_6(m_i)-ainc=-ainc, so q=1 has physical ainc=-1",
            "the kernel test ranges over the exhaustive relative source complex; a restricted kernel gives only a bounded separator",
            "for cyclic assembly the five face readouts share the same physical typing and characteristic zero permits division by five",
        ],
        "sharp_scope": (
            "the Fredholm decision is complete once J0 and q have the stated "
            "typing.  The canonical face has this physical q, and the marked "
            "Cartan occurrence is nonzero.  An arbitrary component grade "
            "still needs its augmented comparison identifying its terminal "
            "with that physical anchor; neither component charge nor raw "
            "derived chart value supplies the identification"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("dark R physical alternative ledger changed", digest))

    print("OO dark R physical generator/annihilator: CLASSIFIED")
    print("q(R)!=0 -> R generator")
    print("q(R)=0 + q visible elsewhere on ker J0 -> other kernel generator")
    print("q(ker J0)=0 -> q=lambda J0 -> physical left separator")
    print("component/chart charge is not a physical anchor readout")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
