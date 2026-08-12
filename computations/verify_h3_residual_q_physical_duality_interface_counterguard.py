#!/usr/bin/env python3
r"""Physical-duality interface for the single residual-q repeated grade.

The mixed curvature/rootless-bar near-hit leaves the four-corner residue

    delta = (P+ q00, P- q00, P+ q11, P- q11)
          = (1,-1,-1,1).

This file separates three statements which must not be conflated:

* delta is a nonzero class in the committed endpoint-even residue block;
* a left dual for that bounded residue block is not yet a physical rootless
  Fredholm covector; and
* failure of the bounded lift does not by itself make a kernel-relative
  generator.

The exact obstruction to promotion is already physical.  The target
stabilizers eta_z have zero selected-tail/q readout but endpoint aggregate
readout -5-u_z/t.  The complete committed Omega/Q/r/ores constraint matrix
has a one-dimensional dual before eta and zero-dimensional dual after eta.
Thus the residue dual and the rootless terminal dual live in two different
presentations until a source-provenant comparison supplies the eta law.

The final finite linear-algebra audit gives the sharp interface.  For a
complete physically typed matrix J and terminal row tau, exactly one first
event occurs: the target is outside im(J) and has a left separator; or it
is in im(J), in which case nonzero tau on ker(J) normalizes to the relative
generator, while zero tau on ker(J) makes the lift terminal value
well-defined.  Three completions of the same committed even block realize
all three outcomes, proving that bounded failure alone decides none of them.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "4d6bd576c9adff697dcc9c5dfe3ea68c60d90f7a301fd0c555d4de46492fbdbe"
PINS = {
    "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py":
        "00db2478df3162a374434ea7d0ab285f770510d33b72619377560404c96b16e8",
    "computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py":
        "13aef43505fa09d3c43cf0098598dc62a690598759637820a29672d195139d71",
    "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py":
        "af9a69ad996bd4390ff3fe9139e357a3bb765292ec969350a948612d9b824fa7",
    "computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py":
        "a98c6e0e90127e81e869c68342f3999abbbd8898d2b2eeafbeccbad06575a324",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
}

RESIDUE_ROWS = ("P+q00", "P-q00", "P+q11", "P-q11")
DELTA = (Q(1), Q(-1), Q(-1), Q(1))
NEGATIVE_DELTA = tuple(-entry for entry in DELTA)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def matvec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def transpose(columns, height: int):
    return [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]


def rref(matrix, width: int):
    work = [list(map(Q, row)) for row in matrix]
    require(all(len(row) == width for row in work), "ragged matrix")
    pivots = []
    pivot_row = 0
    for column in range(width):
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
            work[row] = [left - value * right for left, right in zip(
                work[row], work[pivot_row], strict=True
            )]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, pivots


def rank(matrix, width: int) -> int:
    return len(rref(matrix, width)[1])


def kernel_basis(matrix, width: int):
    reduced, pivots = rref(matrix, width)
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        require(not any(matvec(matrix, vector)), "kernel basis failed")
        basis.append(tuple(vector))
    return tuple(basis)


def in_column_span(columns, target, height: int) -> bool:
    matrix = transpose(columns, height)
    old_rank = rank(matrix, len(columns))
    enlarged = [row + [Q(target[index])] for index, row in enumerate(matrix)]
    return rank(enlarged, len(columns) + 1) == old_rank


def left_kernel_basis(columns, height: int):
    # lambda kills every column iff columns^T lambda=0.
    return kernel_basis([list(map(Q, column)) for column in columns], height)


def solve(columns, target, height: int):
    """Return one exact solution of J*x=target, or None."""
    width = len(columns)
    equations = [row + [Q(target[index])] for index, row in enumerate(
        transpose(columns, height)
    )]
    reduced, pivots = rref(equations, width + 1)
    if any(not any(row[:width]) and row[width] for row in reduced):
        return None
    require(width not in pivots, "inconsistent system lost its guard")
    solution = [Q(0)] * width
    for row, pivot in enumerate(pivots):
        if pivot < width:
            solution[pivot] = reduced[row][width]
    require(matvec(transpose(columns, height), solution)
            == list(map(Q, target)), "solution reconstruction failed")
    return tuple(solution)


def residual_grade_audit() -> dict[str, object]:
    shared = load(
        "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py",
        "residual_q_shared_boundary",
    )
    reciprocal = load(
        "computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py",
        "residual_q_reciprocal_parity",
    )
    shared_ledger, shared_digest = shared.audit()
    require(shared_digest == shared.EXPECTED_LEDGER_SHA256,
            "shared four-term ledger changed")
    curvature = shared_ledger["curvature_Kodaira_Spencer_candidate"]
    candidate = curvature["combined_candidate"]
    require(candidate["residue_vector"] == [1, -1, -1, 1],
            "pure/mixed residual vector changed")
    require(candidate["same_word_and_total_polynomial_degree"],
            "curvature and bar left their common degree")
    require(curvature["mixed_bar_curvature"]["rootless_word_with_x_removed"]
            == "1211222", "common source word changed")

    parity = reciprocal.parity_and_residue_gate()
    require(parity["ordinary_residue_of_every_endpoint_odd_response"] == 0,
            "endpoint-odd response acquired old residue")
    require(parity["first_missing_correction"] == ["0", "0", "0", "0", "0", "1"],
            "reduced-residue correction signature changed")

    # The old response/residue image is endpoint-even separately on the pure
    # and mixed tail.  delta is odd on both pairs and is therefore outside.
    pure_even = (Q(1), Q(1), Q(0), Q(0))
    mixed_even = (Q(0), Q(0), Q(1), Q(1))
    bounded_columns = (pure_even, mixed_even)
    require(not in_column_span(bounded_columns, DELTA, len(RESIDUE_ROWS)),
            "delta entered the committed endpoint-even residue block")
    residue_dual = DELTA
    require(all(dot(residue_dual, column) == 0
                for column in bounded_columns),
            "residue dual stopped killing endpoint-even columns")
    require(dot(residue_dual, DELTA) == 4,
            "residue dual stopped detecting delta")

    return {
        "common_word_after_exposed_x_deletion": "1211222",
        "coarse_operation_grade": {"p": 1, "s": 1, "q": 2},
        "first_common_fine_grade": "labelled repeated P3+K2",
        "residue_row_order": list(RESIDUE_ROWS),
        "curvature_minus_bar_residual_delta": [int(x) for x in DELTA],
        "required_KS_correction": [int(x) for x in NEGATIVE_DELTA],
        "protected_readouts": {"W": 0, "target": 0, "ainc": 0},
        "bounded_endpoint_even_columns": [
            [int(x) for x in column] for column in bounded_columns
        ],
        "bounded_residue_dual": [int(x) for x in residue_dual],
        "bounded_dual_pairing_with_delta": int(dot(residue_dual, DELTA)),
        "bounded_residual_class_nonzero": True,
        "source_resolution_exhaustive": False,
    }


def physical_stabilizer_promotion_gate() -> dict[str, object]:
    inventory = load(
        "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py",
        "residual_q_repeated_inventory",
    )
    endpoint_kernel = load(
        "computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py",
        "residual_q_endpoint_kernel",
    )
    gate = inventory.stabilizer_kernel_no_go()
    eta = endpoint_kernel.aggregate_pairing_audit()
    require(gate["rank_before_target_stabilizers"] == 25
            and gate["solution_dimension_before_target_stabilizers"] == 1,
            "pre-eta rootless dual line changed")
    require(gate["rank_after_target_stabilizers"] == 26
            and gate["solution_dimension_after_target_stabilizers"] == 0,
            "eta stopped killing the rootless dual line")
    require(all(record["five_face_pairing"] == f"-5-u_{index}/t"
                for index, record in enumerate(eta["records"], 1)),
            "eta aggregate signs changed")

    # Each eta_z uses only colour-zero weights, while all four residual-tail
    # corners use selected internal colours 1/2.  Consequently eta is zero
    # on the local residue block.  This does not promote its dual: promotion
    # also has to identify the Omega/Q/r presentation, where eta is nonzero.
    return {
        "committed_rootless_augmented_covector_variables":
            gate["unknown_covector_weights"],
        "rank_before_eta": gate["rank_before_target_stabilizers"],
        "dual_dimension_before_eta":
            gate["solution_dimension_before_target_stabilizers"],
        "eta_family_count": 5,
        "eta_selected_tail_and_q_readout": 0,
        "eta_existing_rootless_r_readout": 0,
        "eta_Omega_face_law": {
            "v_not_equal_z": "-1",
            "v_equal_z": "-1-u_z/t",
            "five_face_aggregate": "-5-u_z/t",
        },
        "rank_after_eta": gate["rank_after_target_stabilizers"],
        "dual_dimension_after_eta":
            gate["solution_dimension_after_target_stabilizers"],
        "same_labelled_Q_repairs_promotion": False,
        "needed_terminal_comparison_law": (
            "d r_v(eta_z)=d Omega_v(eta_z) facewise, equivalently the "
            "aggregate rootless correction reads 5+u_z/t"
        ),
        "residue_dual_is_already_physical_rootless_dual": False,
        "reason": (
            "the residue and Omega/Q/r covectors have not been identified "
            "by a source-provenant chain map; the latter has no nonzero "
            "extension across the known physical eta relations"
        ),
    }


def classify(columns, target, terminal, height: int):
    """The exact attachment-or-dual/generator decision for a complete J."""
    if not in_column_span(columns, target, height):
        separators = [vector for vector in left_kernel_basis(columns, height)
                      if dot(vector, target)]
        require(separators, "inconsistent finite system lost Farkas dual")
        return {
            "branch": "left_separator",
            "separator": [str(x) for x in separators[0]],
            "pairing": str(dot(separators[0], target)),
        }

    solution = solve(columns, target, height)
    require(solution is not None, "solvable system has no solution")
    matrix = transpose(columns, height)
    kernel = kernel_basis(matrix, len(columns))
    witness = next((vector for vector in kernel if dot(terminal, vector)), None)
    if witness is not None:
        value = dot(terminal, witness)
        normalized = tuple(-entry / value for entry in witness)
        require(not any(matvec(matrix, normalized)),
                "relative generator left the correction kernel")
        require(dot(terminal, normalized) == -1,
                "relative generator normalization changed")
        return {
            "branch": "kernel_relative_generator",
            "generator": [str(x) for x in normalized],
            "terminal": "-1",
        }

    return {
        "branch": "zero_indeterminate_lift",
        "solution": [str(x) for x in solution],
        "well_defined_terminal": str(dot(terminal, solution)),
    }


def completion_counterguard() -> dict[str, object]:
    pure_even = (Q(1), Q(1), Q(0), Q(0))
    mixed_even = (Q(0), Q(0), Q(1), Q(1))
    base = (pure_even, mixed_even)

    # All three maps restrict to precisely the same committed even residue
    # block.  They differ only by still-unconstructed source generators.
    no_new_source = classify(base, NEGATIVE_DELTA, (Q(0), Q(0)), 4)

    one_ks_lift = base + (NEGATIVE_DELTA,)
    unique_lift = classify(
        one_ks_lift, NEGATIVE_DELTA, (Q(0), Q(0), Q(0)), 4
    )

    two_ks_lifts = base + (NEGATIVE_DELTA, NEGATIVE_DELTA)
    nonzero_terminal = (Q(0), Q(0), Q(0), Q(1))
    relative_generator = classify(
        two_ks_lifts, NEGATIVE_DELTA, nonzero_terminal, 4
    )

    require(no_new_source["branch"] == "left_separator",
            "no-lift completion changed branch")
    require(unique_lift["branch"] == "zero_indeterminate_lift",
            "single-lift completion changed branch")
    require(relative_generator["branch"] == "kernel_relative_generator",
            "double-lift completion changed branch")

    return {
        "common_committed_submatrix": {
            "rows": list(RESIDUE_ROWS),
            "columns": [
                [int(x) for x in pure_even],
                [int(x) for x in mixed_even],
            ],
        },
        "completion_with_no_new_source": no_new_source,
        "completion_with_one_KS_source": unique_lift,
        "completion_with_two_KS_sources_and_terminal_difference":
            relative_generator,
        "logical_conclusion": (
            "the committed bounded block is compatible with all three "
            "physical outcomes; only an exhaustive source-labelled J and "
            "its physical terminal row choose the branch"
        ),
    }


def exact_interface() -> dict[str, object]:
    return {
        "domain_required": (
            "every source-provenant correction generator and relation in "
            "the literal word 1211222 and labelled repeated P3+K2 grade"
        ),
        "codomain_rows_required": [
            "literal boundary coordinates including E+/E-/Omega/qcomp",
            "four separate residue corners P+q00/P-q00/P+q11/P-q11",
            "physical W", "target", "anchor incidence",
            "source word and chart labels",
        ],
        "relations_required": [
            "all target-stabilizer eta_z columns",
            "endpoint/bar and PP common-companion relations",
            "higher collision/mapping-cone rows capable of this grade",
        ],
        "terminal_row_required": (
            "physical rootless/polar landing, not the derived chart scalar"
        ),
        "decision": [
            "rank(J)<rank([J|-delta]) => genuine physical left separator",
            "-delta in im(J) and terminal(ker J)!=0 => normalized relative generator",
            "-delta in im(J) and terminal(ker J)=0 => zero-indeterminate lift",
        ],
        "current_instantiation": {
            "bounded_residue_block": True,
            "physical_eta_relations": True,
            "complete_source_census_in_this_grade": False,
            "source_provenant_residue_to_rootless_comparison": False,
            "physical_terminal_row": False,
        },
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    ledger = {
        "theorem": "single residual-q physical-duality interface counterguard",
        "residual_grade": residual_grade_audit(),
        "physical_stabilizer_promotion_gate":
            physical_stabilizer_promotion_gate(),
        "completion_counterguard": completion_counterguard(),
        "complete_map_interface": exact_interface(),
        "verdict": {
            "bounded_residual_class": "nonzero",
            "genuine_physical_left_separator_constructed": False,
            "kernel_relative_generator_constructed": False,
            "sharp_reason": (
                "the local four-corner residue dual and the full rootless "
                "Omega/Q/r dual are not connected by a physical chain map; "
                "eta_z kills every same-Q extension of the latter"
            ),
            "smallest_next_theorem": (
                "construct the source-provenant residual-q comparison with "
                "correction -delta and facewise eta law d r=d Omega, or "
                "prove an exhaustive physical source census excluding it"
            ),
        },
        "scope": (
            "exact for the pinned committed residual block and physical "
            "eta relations.  This is a counterguard against promoting the "
            "bounded dual, not an all-resolution nonexistence theorem"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))

    print("h3 single residual-q physical duality interface: COUNTERGUARD")
    print("residual delta: (1,-1,-1,1); required KS correction: (-1,1,1,-1)")
    print("bounded endpoint-even residue block: delta is a nonzero cokernel class")
    print("rootless dual dimension before/after physical eta: 1/0")
    print("bounded failure => physical separator or generator: NOT DETERMINED")
    print("next datum: exhaustive source map plus eta-compatible physical terminal")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
