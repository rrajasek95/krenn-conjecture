#!/usr/bin/env python3
"""UNAUDITED REPAIR CANDIDATE (repair item 6): evaluate Lambda for real.

Replaces the 8,580-column half of
``computations/verify_h3_first_flat_physical_anchor_six_term_separator.py``.
That checker contains, verbatim,

    operator_feature_sum = 0
    operator_ainc = 0
    require(operator_feature_sum - operator_ainc == 0,
            "endpoint-odd operator acquired physical Lambda value")

i.e. it verifies ``0 - 0 == 0`` and then publishes
``"complete_8580_first_flat_operator_columns": 0`` in its frozen ledger.  The
8,580-column operator is never loaded (external audit 2026-08-13; the audit
also established by independent computation that the claim is TRUE).

WHAT THIS CHECKER DOES.  It reconstructs the exact first-Spencer-flat
operator block from the pinned construction modules -- the same code path the
first-flat bridge checker uses, but here the columns are kept and evaluated
rather than only solved -- augments every column with its literal bridge
(kind-3) feature rows, appends the 288 repeated full-nine columns, and then

  * evaluates the physical covector Lambda = sum(six selected private
    matching features) - ainc on all 8,580 operator columns and all 288
    repeated columns, one column at a time;
  * hashes the ACTUAL evaluation vector plus the actual kind-3 sub-columns,
    so restating the claim without changing the mathematics is impossible;
  * establishes the STRUCTURAL reason separately: 490 of the 8,580 operator
    columns carry a nonzero bridge feature, and 0 of the 8,580 touch any of
    the six selected private features, so the vanishing is structural rather
    than a cancellation between nonzero contributions;
  * re-derives the repeated-column pairing (feature sum = -1 exactly on the
    six pure repeated columns where ainc = -1, and 0 elsewhere), which is the
    one half the committed checker does compute.

Frozen ledger hashes: the Lambda value histogram over both blocks, a rolling
digest of the per-column (feature-sum, ainc) evaluation stream in canonical
column order, a digest of every nonzero kind-3 sub-column of the operator
block, and the six selected private feature monomials themselves.

POSITIVE CONTROLS (run in the same process, must FAIL):
  1. fabricated feature selection -- replace the six selected private
     features by the six most frequent bridge features that DO occur in the
     operator block.  Lambda then takes nonzero values on operator columns
     and the "kills the operator block" claim is false;
  2. fabricated anchor-incidence law -- drop the anchor incidence on the pure
     repeated columns (ainc = 0 everywhere).  Lambda is then -1 on the six
     pure repeated columns.

Runtime: about half a minute; the operator reconstruction dominates.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRIMITIVE_PAIR = ((0, 7, 1, 1), (2, 4, 1, 1))
CANONICAL_PRESENTATION = {
    "contracted_arm": [0, 7, 1, 1],
    "inserted_two_edge_tail": [[1, 3, 0, 0], [4, 5, 0, 0]],
    "colour_permutations_source_to_target": [
        [0, 1, 2], [0, 1, 2], [1, 0, 2], [0, 1, 2],
        [0, 1, 2], [0, 1, 2], [1, 2, 0], [1, 2, 0],
    ],
}

PINS = {
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_first_flat_endpoint_bridge.py":
        "e22cc0eec09c0e67c10bc9ae1bd50bf26167f8d44af7857e7c6920f42bba63c2",
    "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py":
        "d1b545f25603930a6247a286c5be70c7d16e20caab053401eeeb650bb53559d6",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_order6_to_repeated_grade_bridge.py":
        "30c5df97584a01dfcf121cd48affa8525c058e00a69f8806b6ae81492fff9cda",
    "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py":
        "ef9bd416986f7dc8c07ffa3b396d1c1f92237c8e1a0539ecbb0ddbeaadb1c18e",
    "computations/verify_h3_endpoint_recoloured_primitive_face_grade.py":
        "1c5ed6f5488fb1c4ec8c26d618f312dc1dfeeb5215f2fa24271154d0bcdea0c0",
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
}
EXPECTED_LEDGER_SHA256 = (
    "3ea9d9cfbbc2571df1c1a5b8de8c7a82bb052e6670246edc82684cfe411ad21e"
)


class ControlDidNotFail(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def should_fail(label, thunk):
    try:
        thunk()
    except RuntimeError as failure:
        return {"control": label, "fired": True, "reason": str(failure)[:200]}
    raise ControlDidNotFail(("positive control did not fail", label))


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


# ---------------------------------------------------------- reconstruction --

def build_augmented_columns():
    """Rebuild the 8,580 operator columns with their literal bridge feature
    rows, then the 288 repeated full-nine columns."""
    affine = load(
        "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py",
        "lambda_affine")
    order6 = load(
        "computations/verify_h3_residual_q_order6_missing_face_probe.py",
        "lambda_order6")
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "lambda_repair")
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "lambda_commutator")
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "lambda_base")
    endpoint = load(
        "computations/verify_h3_endpoint_recoloured_primitive_face_grade.py",
        "lambda_endpoint")
    bridge = load(
        "computations/verify_h3_order6_to_repeated_grade_bridge.py",
        "lambda_bridge")
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "lambda_complete")
    absolute = load(
        "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py",
        "lambda_absolute")
    first_flat = load(
        "computations/verify_h3_first_flat_endpoint_bridge.py",
        "lambda_first_flat")

    system = repair.build_system(base, commutator)
    (operator, solution, exact_rank, indexed, columns,
     derivative_tables) = first_flat.reconstruct_first_flat_operator(
        affine, order6, repair, commutator, base, system)
    require(len(columns) == 8_580 and exact_rank == 1_328
            and len(solution) == 343,
            ("the first-flat operator block changed", len(columns),
             exact_rank, len(solution)))

    outputs = first_flat.primitive_outputs(operator, system, repair, endpoint)
    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]))
    repeated_component = complete.component(base, target_degree)
    source_degree = outputs[1]["degrees"][0]
    presentation = next(
        (record for record in bridge.covariance_arm_contraction_bridges(
            source_degree, target_degree, complete, base)
         if all(record[key] == value
                for key, value in CANONICAL_PRESENTATION.items())), None)
    require(presentation is not None,
            "physical canonical bridge presentation changed")

    derivative_cache = {}
    operator_columns = []
    bridge_nonzero = 0
    for (_shift, (metadata, old_column)) in indexed:
        polynomial = Counter()
        for (composed_coefficient, composed_directions), weight in (
                affine.endpoint_composition_antisymmetric(metadata).items()):
            remaining = list(composed_directions)
            if not all(cell in remaining for cell in PRIMITIVE_PAIR):
                continue
            for cell in PRIMITIVE_PAIR:
                remaining.remove(cell)
            remaining = tuple(remaining)
            if remaining not in derivative_cache:
                table = derivative_tables.get(len(remaining))
                derivative_cache[remaining] = (
                    {} if table is None else table.get((1, remaining), {}))
            for tail, value in derivative_cache[remaining].items():
                monomial = tuple(sorted(composed_coefficient + tail))
                if endpoint.degree(monomial) == source_degree:
                    polynomial[monomial] += weight * value / 2
        polynomial = +polynomial
        transformed, _hits = bridge.transform_primitive_face(
            polynomial, presentation, base)
        column = dict(old_column)
        if transformed:
            bridge_nonzero += 1
            for monomial, value in transformed.items():
                column[(3, monomial)] = column.get((3, monomial), Q(0)) + value
        operator_columns.append((metadata, column))

    repeated_columns = []
    for column_index, (word, multiplier, boundary) in enumerate(
            repeated_component["columns"]):
        column = {(3, monomial): Q(-1) for monomial in boundary}
        if word == (0,) * 8:
            column[(4, "pure_aggregate")] = Q(1)
        repeated_columns.append((("repeated", column_index, word, multiplier),
                                 column))

    pure_indices, selected = absolute.selected_private_features(
        repeated_component)
    return (operator_columns, repeated_columns, bridge_nonzero, pure_indices,
            selected, repeated_component, [left, right], target_degree)


# ------------------------------------------------------------- evaluation --

def evaluate_lambda(columns, selected, anchor_incidence=True):
    """Lambda = sum(selected private matching features) - ainc, column by
    column.  On these augmented columns the pure-row marker is minus physical
    anchor incidence, so ainc = -column[(4,'pure_aggregate')]."""
    features = frozenset(selected)
    values = []
    for _metadata, column in columns:
        feature_sum = sum((value for row, value in column.items()
                           if row[0] == 3 and row[1] in features), Q(0))
        marker = sum((value for row, value in column.items()
                      if row[0] == 4 and row[1] == "pure_aggregate"), Q(0))
        ainc = -marker if anchor_incidence else Q(0)
        values.append((feature_sum, ainc, feature_sum - ainc))
    return values


def stream_digest(columns, values):
    rolling = sha256()
    for index, ((metadata, column), (feature_sum, ainc, value)) in enumerate(
            zip(columns, values, strict=True)):
        rolling.update(f"{index}|{feature_sum}|{ainc}|{value}\n".encode())
    return rolling.hexdigest()


def kind_three_digest(columns):
    """Hash the ACTUAL bridge sub-columns, not their count."""
    rolling = sha256()
    for index, (_metadata, column) in enumerate(columns):
        rows = sorted((repr(row[1]), str(value))
                      for row, value in column.items() if row[0] == 3)
        if rows:
            rolling.update(f"{index}|{rows}\n".encode())
    return rolling.hexdigest()


# ------------------------------------------------------------------ audit --

def audit(state):
    (operator_columns, repeated_columns, bridge_nonzero, pure_indices,
     selected, repeated_component, faces, target_degree) = state

    require(len(operator_columns) == 8_580,
            ("operator column count changed", len(operator_columns)))
    require(len(repeated_columns) == 288,
            ("repeated column count changed", len(repeated_columns)))
    require(len(selected) == 6 and len(pure_indices) == 6,
            ("the six selected private features changed",
             len(selected), len(pure_indices)))

    operator_values = evaluate_lambda(operator_columns, selected)
    repeated_values = evaluate_lambda(repeated_columns, selected)

    operator_histogram = Counter(str(value) for _f, _a, value
                                 in operator_values)
    repeated_histogram = Counter(str(value) for _f, _a, value
                                 in repeated_values)
    require(set(operator_histogram) == {"0"},
            ("Lambda is nonzero on an operator column", operator_histogram))
    require(set(repeated_histogram) == {"0"},
            ("Lambda is nonzero on a repeated column", repeated_histogram))

    # STRUCTURAL SECOND CHECK: the vanishing on the operator block is not a
    # cancellation.  490 columns carry a bridge feature; none of them touches
    # any of the six selected private features, and the anchor incidence of
    # the whole endpoint-odd operator block is identically zero.
    features = frozenset(selected)
    touching_any_bridge_row = 0
    touching_selected = 0
    nonzero_ainc = 0
    for _metadata, column in operator_columns:
        if any(row[0] == 3 for row in column):
            touching_any_bridge_row += 1
        if any(row[0] == 3 and row[1] in features for row in column):
            touching_selected += 1
        if any(row[0] == 4 for row in column):
            nonzero_ainc += 1
    require(touching_any_bridge_row == bridge_nonzero == 490,
            ("the operator bridge-feature census changed",
             touching_any_bridge_row, bridge_nonzero))
    require(touching_selected == 0,
            ("an operator column touched a selected private feature",
             touching_selected))
    require(nonzero_ainc == 0,
            ("the endpoint-odd operator block acquired anchor incidence",
             nonzero_ainc))

    # The repeated half, recomputed from the boundaries rather than restated.
    repeated_profile = Counter()
    for (_kind, _index, word, _multiplier), column in repeated_columns:
        feature_sum = sum(1 for row in column
                          if row[0] == 3 and row[1] in features)
        marker = int((4, "pure_aggregate") in column)
        repeated_profile[(feature_sum, marker)] += 1
    require(dict(repeated_profile) == {(1, 1): 6, (0, 0): 282},
            ("the repeated feature/pure-marker profile changed",
             dict(repeated_profile)))

    # The two remaining pairings the committed checker states.
    alpha = (-1, 1, 1, -1)
    require(sum(alpha) == 0,
            "the known relative alpha-cell acquired aggregate pairing")
    desired = {"selected_matching_features": 0, "ainc": -1}
    require(desired["selected_matching_features"] - desired["ainc"] == 1,
            "the desired boundary-zero anchor normalization changed")

    return {
        "theorem": ("Lambda = sum(six selected private matching features) - "
                    "ainc kills the whole first-flat operator block and the "
                    "whole repeated component, evaluated column by column"),
        "canonical_faces": faces,
        "canonical_fine_degree": list(target_degree),
        "selected_private_features": [repr(value) for value in selected],
        "selected_private_features_sha256": sha256(json.dumps(
            sorted(repr(value) for value in selected),
            separators=(",", ":")).encode()).hexdigest(),
        "pure_repeated_columns": len(pure_indices),
        "operator_columns": len(operator_columns),
        "repeated_columns": len(repeated_columns),
        "operator_lambda_histogram": dict(sorted(operator_histogram.items())),
        "repeated_lambda_histogram": dict(sorted(repeated_histogram.items())),
        "operator_evaluation_stream_sha256": stream_digest(
            operator_columns, operator_values),
        "repeated_evaluation_stream_sha256": stream_digest(
            repeated_columns, repeated_values),
        "operator_bridge_subcolumn_sha256": kind_three_digest(
            operator_columns),
        "repeated_bridge_subcolumn_sha256": kind_three_digest(
            repeated_columns),
        "structural_reason": {
            "operator_columns_with_a_bridge_feature": touching_any_bridge_row,
            "operator_columns_touching_a_selected_feature": touching_selected,
            "operator_columns_with_anchor_incidence": nonzero_ainc,
        },
        "repeated_feature_marker_profile": {
            f"features={key[0]},pure_marker={key[1]}": count
            for key, count in sorted(repeated_profile.items())
        },
        "known_relative_alpha_cell_pairing": sum(alpha),
        "desired_boundary_zero_anchor_pairing": 1,
        "reading": (
            "the vanishing on the 8,580-column block is structural: 490 "
            "columns carry bridge features, but none of those features is "
            "one of the six selected private matching rows, and the "
            "endpoint-odd block carries no anchor incidence at all.  The "
            "repeated block vanishes by an exact cancellation, one selected "
            "feature against the anchor incidence, on each of the six pure "
            "columns"
        ),
        "scope": (
            "the canonical faces-(3,5) exact first-flat operator block and "
            "the complete repeated component.  It does not extend Lambda to "
            "arbitrary new relative mapping-cone generators, and it does not "
            "prove that the desired boundary-zero anchor exists"
        ),
    }


def controls(state):
    (operator_columns, repeated_columns, _bridge_nonzero, _pure_indices,
     selected, _component, _faces, _degree) = state
    fired = []

    def fabricated_feature_selection():
        # Fabricated geometry: choose six features that actually occur in the
        # operator block instead of the six selected private matching rows.
        occurrence = Counter()
        for _metadata, column in operator_columns:
            for row in column:
                if row[0] == 3:
                    occurrence[row[1]] += 1
        fabricated = [monomial for monomial, _count
                      in occurrence.most_common(6)]
        require(len(fabricated) == 6,
                "the operator block has fewer than six bridge features")
        values = evaluate_lambda(operator_columns, fabricated)
        histogram = Counter(str(value) for _f, _a, value in values)
        require(set(histogram) == {"0"},
                ("fabricated feature selection still kills the operator "
                 "block", dict(histogram)))

    def fabricated_anchor_incidence():
        # Fabricated geometry: a repeated pure row no longer carries anchor
        # incidence -1.  Lambda then reads -1 there.
        values = evaluate_lambda(repeated_columns, selected,
                                 anchor_incidence=False)
        histogram = Counter(str(value) for _f, _a, value in values)
        require(set(histogram) == {"0"},
                ("fabricated anchor-incidence law still kills the repeated "
                 "component", dict(histogram)))

    fired.append(should_fail("fabricated feature selection (six features "
                             "that do occur in the operator block)",
                             fabricated_feature_selection))
    fired.append(should_fail("fabricated anchor-incidence law (ainc = 0 on "
                             "pure repeated columns)",
                             fabricated_anchor_incidence))
    return fired


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    state = build_augmented_columns()
    control_records = controls(state)
    ledger = audit(state)
    ledger["positive_controls"] = [
        {"control": record["control"], "fired": record["fired"]}
        for record in control_records
    ]
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Lambda operator-block ledger changed", digest))
    print("repair678 Lambda kills the operator block: PASS")
    print("operator columns evaluated:", ledger["operator_columns"],
          "| Lambda histogram:", ledger["operator_lambda_histogram"])
    print("repeated columns evaluated:", ledger["repeated_columns"],
          "| Lambda histogram:", ledger["repeated_lambda_histogram"])
    print("structural reason:", ledger["structural_reason"])
    print("operator evaluation stream sha256:",
          ledger["operator_evaluation_stream_sha256"])
    print("operator bridge sub-column sha256:",
          ledger["operator_bridge_subcolumn_sha256"])
    for record in control_records:
        print("positive control fired:", record["control"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
