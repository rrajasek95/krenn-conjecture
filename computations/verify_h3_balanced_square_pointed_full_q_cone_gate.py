#!/usr/bin/env python3
"""Test whether fixed-target/pointed/full-q data cone the balanced square.

The balanced signless K2,2 incidence has missing charge

    delta=(1,1,-1,-1).

After multiplying the second shore by -1, its columns are ordinary oriented
incidences and delta becomes the constant vector.  Hence a new column cones
the square exactly when its gauged vertex augmentation is nonzero.

Fixed pure-target normalization only sets du=0.  The full simultaneous-q
calculation supplies 135 genuine q-Jacobian columns and the three-term
product-rule anchor conormal, but neither datum is a column in the relative
chart-square output.  This checker freezes the resulting no-implication
guard.  It also strengthens the known cap/Cartan packet by adjoining both
normalized pure-target selectors.  A primitive augmented dual still detects
the balanced B-delta face while vanishing on q, P_f, ridge and eta/sigma.

The universal full-q polynomial Jacobian may therefore be carried as a
direct summand without killing the class.  This is a sharp compatibility
guard, not a complete GHZ source: the missing physical datum is precisely a
cross-grade column whose square projection has nonzero augmentation and
whose q/anchor/ridge faces are the faces of that same source cell.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_balanced_chart_square_master_obstruction.py":
        "306980dc569795fa3ec2c8e6fdbdf2b67fa5d85cd75ebebe62be7db15b1e1a59",
    "notes/uniform-balanced-chart-square-master-obstruction.md":
        "c758fb43f88d9c02f5200921c6c50637bfe04402536edc3e947f74d108fbd93b",
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
    "notes/h3-trapped-carrier-full-q-six-term-extension.md":
        "a5b1a81c834095e69c403d054a38d9f34ebb8b0b3f1d3ce720a27f0b275d04a5",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "notes/h3-gate-ii-chiw-nonfill-full-augmented-dual.md":
        "f7fd790075f7cf3d31b9d4a6035fa6bc476a3bdc16ce4bda97b777b153664568",
    "computations/verify_h3_centered_pointed_face_fixed_target_correction.py":
        "a566c0e285e1c68c346cd89a36dd13300298898b7020647ca90a39b9c2aea70c",
    "notes/h3-centered-pointed-fixed-target-normalization-correction.md":
        "c8cd4add2c0205993a1d5976102e8616913843d0ba5ee6740aae492763cfa4c9",
    "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py":
        "6f791c41e743a94279ccf9e4924af11a42c278baa7737a5eed108bf85136f499",
    "notes/h3-gate-ii-cartan-full-q-pointed-character-gate.md":
        "3ffd0d0894dfbb81cb672f87548b3b7a2da28ac1b36a6466bbef6ad149cf0933",
}
EXPECTED_LEDGER_SHA256 = (
    "721148070b0687f52e23f1c0ba36561a24a21892c552bd01d60802a6511edae7"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def gauged_square_and_cone_criterion() -> dict[str, object]:
    # Vertex order A0,A1,B0,B1.  The four signless K2,2 edge columns are
    # exactly the flat complete-row/mate square from 0ffc23a.
    signless = (
        (Q(1), Q(0), Q(1), Q(0)),
        (Q(1), Q(0), Q(0), Q(1)),
        (Q(0), Q(1), Q(1), Q(0)),
        (Q(0), Q(1), Q(0), Q(1)),
    )
    delta = tuple(map(Q, (1, 1, -1, -1)))
    gauge = delta
    ordinary = tuple(tuple(gauge[index] * entry
                           for index, entry in enumerate(column))
                     for column in signless)
    constant = (Q(1),) * 4
    gauged_delta = tuple(gauge[index] * delta[index]
                         for index in range(4))
    require(rank(signless) == rank(ordinary) == 3
            and all(dot(delta, column) == 0 for column in signless)
            and all(dot(constant, column) == 0 for column in ordinary)
            and gauged_delta == constant,
            "the signless-to-ordinary square gauge changed")

    # im(d_square)=ker(augmentation), because both spaces have dimension 3.
    # Test both a literal cone vertex and the requested dE=delta column.
    cone_vertex = (Q(1), Q(0), Q(0), Q(0))
    requested_boundary = gauged_delta
    require(sum(cone_vertex) == 1 and sum(requested_boundary) == 4
            and rank(ordinary + (cone_vertex,)) == 4
            and rank(ordinary + (requested_boundary,)) == 4,
            "the augmentation/cone criterion changed")

    # Conversely, representative zero-augmentation columns remain in the
    # existing image and cannot kill H0.
    zero_augmentation_samples = (
        (Q(2), Q(-3), Q(1), Q(0)),
        (Q(0), Q(5), Q(-2), Q(-3)),
        (Q(-7), Q(1), Q(2), Q(4)),
    )
    require(all(sum(column) == 0 for column in zero_augmentation_samples)
            and all(rank(ordinary + (column,)) == 3
                    for column in zero_augmentation_samples),
            "a zero-augmentation sample left the ordinary incidence image")
    return {
        "vertex_order": ["A0", "A1", "B0", "B1"],
        "signless_left_kernel": [1, 1, -1, -1],
        "shore_sign_gauge": [1, 1, -1, -1],
        "gauged_class": [1, 1, 1, 1],
        "ordinary_incidence_rank": 3,
        "ordinary_image": "kernel of vertex augmentation sum",
        "cone_criterion": (
            "an added square-output column kills the class iff its gauged "
            "vertex augmentation is nonzero"
        ),
        "requested_dE_equals_delta_gauged_augmentation": 4,
        "one_vertex_cone_gauged_augmentation": 1,
    }


def fixed_target_and_pure_rows_audit(fixed_target, cartan):
    relative = fixed_target.absolute_and_relative_audit()
    remaining = fixed_target.remaining_physical_scope()
    target = cartan.target_defect_audit()
    require(relative["physical_affine_fibre"]["relative_cotangent"] == "du=0"
            and remaining["physical_Pf_status"] == "OPEN"
            and not target["pure_targets_cancel_defect"]
            and target["mixed_target_directions_remaining_after_pure_correction"]
            == 2,
            (relative, remaining, target))
    return {
        "physical_pure_normalization": "u=1, hence du=0",
        "what_it_removes": "the radial target-scale tangent",
        "what_it_does_not_construct": (
            "P_f or a degree-one source cell with nonzero square augmentation"
        ),
        "fixed_target_centered_identity_after_granting_Pf":
            "gamma_c=90*P_f-B",
        "normalized_pure_target_word_span": target[
            "normalized_pure_target_span"],
        "mixed_square_target_defect": target["root_only_target_defect"],
        "pure_rows_fill_mixed_defect": False,
    }


def full_q_type_audit(full_q):
    # This is the actual universal physical polynomial Jacobian, checked both
    # by the cofactor formulas and by literal occurrence differentiation.
    jacobian = full_q.audit_q_jacobian()
    anchor = full_q.marked_anchor_gradient()
    require(jacobian["q_columns"] == 135
            and jacobian["full_fixed_right_domain_columns"] == 171
            and jacobian["unary"]["rows"] == 729
            and jacobian["four_responses"]["rows"] == 2916
            and len(anchor["full_pq_differential_nonzero_coordinates"]) == 3,
            (jacobian, anchor))
    return {
        "actual_physical_Jacobian": jacobian,
        "actual_product_rule_anchor": anchor,
        "variance": {
            "Jacobian_columns": (
                "scalar-source tangents -> unary/response coefficient rows"
            ),
            "anchor_H": "a cotangent row on the same 171-column domain",
            "needed_cone_cell": (
                "a source column -> relative chart-operation square output"
            ),
        },
        "cross_grade_square_face_supplied_by_Jq_formula": False,
        "reason": (
            "the verified q formulas have unary/response word codomain; no "
            "operation-tag/chart-square face map is among their data"
        ),
    }


def pure_safe_full_row_counterguard(nonfill):
    # Use the exact known cap/Cartan source columns.  Add the two normalized
    # pure-target selectors as actual columns, which is stronger than merely
    # fixing their affine right-hand sides.  Corner order is the four-word
    # order used by the Gate-II target audit; corners 2,3 are the pure words.
    columns = nonfill.cap_cartan_columns()
    pure_columns = (
        ("pure_target_2", nonfill.vector(target2=1)),
        ("pure_target_3", nonfill.vector(target3=1)),
    )
    all_columns = columns + pure_columns
    delta = nonfill.DELTA
    candidate = nonfill.vector(**{
        **{f"B{corner}": delta[corner] for corner in range(4)}
    })

    # The original covariant detector is changed by the pure columns.  The
    # following primitive correction kills them while retaining the balanced
    # B charge.  The Eq correction is forced only on the two pure corners.
    dual = nonfill.vector(**{
        **{f"B{corner}": delta[corner] for corner in range(4)},
        "Eq2": 1, "Eq3": 1,
        "target0": -1, "target1": -1,
        "W0": -1, "W1": -1,
        "ores0": 1, "ores1": 1,
    })
    require(all(dot(dual, value) == 0 for _name, value in all_columns)
            and dot(dual, candidate) == 4
            and rank(tuple(value for _name, value in all_columns)
                     + (candidate,))
            == rank(tuple(value for _name, value in all_columns)) + 1,
            "the pure-safe augmented balanced detector changed")

    protected_zero_labels = (
        "M", "ainc", "q", "P_f", "ridge", "eta_constant",
        "eta_u_over_t", "sigma_q22", "W_global", "common_tail_escape",
    )
    require(all(dual[nonfill.LABELS.index(label)] == 0
                for label in protected_zero_labels)
            and dot(nonfill.ALPHA, (Q(1), Q(1), Q(0), Q(0))) == 0,
            "a protected face entered the pure-safe detector")
    return {
        "known_source_columns": [name for name, _value in columns],
        "adjoined_normalized_pure_target_columns": [
            name for name, _value in pure_columns],
        "column_count": len(all_columns),
        "rank_before_balanced_face": rank(tuple(
            value for _name, value in all_columns)),
        "rank_after_balanced_face": rank(tuple(
            value for _name, value in all_columns) + (candidate,)),
        "primitive_detector_signature": {
            "B": [1, 1, -1, -1],
            "Eq": [0, 0, 1, 1],
            "target": [-1, -1, 0, 0],
            "W": [-1, -1, 0, 0],
            "ordinary_residue": [1, 1, 0, 0],
            "M_ainc_q_Pf": [0, 0, 0, 0],
            "ridge_eta_sigma": [0, 0, 0, 0],
        },
        "detector_value_on_balanced_B_face": "4",
        "q_identity": "literal q=M-ainc in every r0 corner",
        "anchor_values": (
            "arbitrary P_f values are allowed because the detector has "
            "P_f coefficient zero"
        ),
        "ridge_cancellation": "alpha.(1,1,0,0)=0, so ridge=eta=sigma=0",
        "consequence": (
            "all named cap/Cartan, pure-target, q, anchor and ridge faces "
            "are compatible with a surviving balanced class"
        ),
    }


def direct_sum_scope() -> dict[str, object]:
    # If psi kills J_aug, then (psi,0) kills J_aug direct-sum J_q.  This
    # elementary construction is the exact logical counterguard to deriving
    # a chart cone from the mere simultaneous presence of the two maps.
    left_columns = ((Q(1), Q(0)),)
    right_columns = ((Q(0), Q(0), Q(1)), (Q(0), Q(0), Q(2)))
    left_dual = (Q(0), Q(1))
    embedded_left = tuple(column + (Q(0),) * 3 for column in left_columns)
    embedded_right = tuple((Q(0),) * 2 + column for column in right_columns)
    extended_dual = left_dual + (Q(0),) * 3
    require(all(dot(extended_dual, column) == 0
                for column in embedded_left + embedded_right),
            "the direct-sum annihilator law changed")
    return {
        "exact_guard": "J_aug direct-sum J_q",
        "surviving_dual": "psi_balanced direct-sum 0",
        "what_this_refutes": (
            "an implication from separate availability of the full q "
            "Jacobian, normalized pure rows and the balanced-square packet"
        ),
        "what_this_does_not_refute": (
            "a physical cross-grade restriction/insertion square coupling "
            "one q source cell to the relative chart square"
        ),
        "full_GHZ_source_point": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    full_q = load(
        "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py",
        "balanced_square_full_q",
    )
    nonfill = load(
        "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py",
        "balanced_square_nonfill",
    )
    fixed_target = load(
        "computations/verify_h3_centered_pointed_face_fixed_target_correction.py",
        "balanced_square_fixed_target",
    )
    cartan = load(
        "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py",
        "balanced_square_cartan",
    )
    ledger = {
        "theorem": "h3 balanced-square pointed/full-q cone gate",
        "pins": PINS,
        "gauged_square": gauged_square_and_cone_criterion(),
        "fixed_target_and_pure_rows":
            fixed_target_and_pure_rows_audit(fixed_target, cartan),
        "simultaneous_q": full_q_type_audit(full_q),
        "smallest_named_full_row_counterguard":
            pure_safe_full_row_counterguard(nonfill),
        "direct_sum_full_q_guard": direct_sum_scope(),
        "verdict": (
            "After the shore-sign gauge the balanced class is the constant "
            "H0 class, and it is killed exactly by a square-output column "
            "of nonzero augmentation.  Fixed pure-target normalization only "
            "sets du=0.  The actual 171-column simultaneous-q Jacobian and "
            "its three-entry product-rule anchor are respectively a "
            "scalar-source map and a conormal row; they do not themselves "
            "supply the missing relative chart-square column.  The exact "
            "15-column cap/Cartan-plus-pure packet retains a primitive "
            "balanced detector with q, P_f, ridge and eta/sigma coefficient "
            "zero.  Thus the shortest positive input is one source-valid "
            "cross-grade cone cell whose square face has nonzero augmentation"
        ),
        "scope": (
            "exact h=3 universal q-Jacobian audit, fixed-target/pure-row "
            "typing theorem, and named augmented linear compatibility guard. "
            "The direct-sum packet is not a complete GHZ tensor or a Krenn "
            "counterexample; it isolates the missing physical cross-grade "
            "restriction/insertion face"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("balanced-square/full-q ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("balanced square gauge: CONSTANT H0 CLASS")
    print("pure target normalization: du=0, NO CONE COLUMN")
    print("full 171-column q Jacobian: ROW/TYPE DATA, NO SQUARE CONE")
    print("cap/Cartan + two pure targets: BALANCED CLASS SURVIVES")
    print("missing input: one cross-grade column of nonzero augmentation")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
