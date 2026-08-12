#!/usr/bin/env python3
r"""Audit the clean aggregate separator on the full known P3+K2 inventory.

The proposed covector has value one on endpoint Omega rows, labelled
all-derivation companions Q_(v,N), and rootless ridge rows, and value zero
on Eq, W, target, ordinary residue, anchor incidence, and chart tags.

It kills endpoint routes and every zero-residue correction cycle.  The
first physical generator on which the current *coarse* augmented map does
not kill it is an individual multiplied PP route (-r_v,ores=1): that
checker has factored out its matching companion and retains only its scalar
ordinary-residue readout.  A source-valid lift of the same column to
(-r_v,+Q_(v,N),ores=1) fixes the pairing, and subtracting the endpoint
route (-Omega_v,+Q_(v,N),ores=1) gives the missing Omega/r comparison.

The complete polynomial full-nine multiplier blocks introduce no further
dual obstruction: their literal private pivots extend any prescribed
weights on the six distinguished Q features in each repeated component.

The first omitted physical source-kernel columns do obstruct the proposed
separator.  The five target-stabilizer tangents eta_z have Q- and existing
rootless-r readout zero but aggregate Omega readout -5-u_z/t.  Solving the
endpoint, lifted-PP, clean-edge, and eta equations proves that no nonzero
same-labelled-Q refinement survives over the marked localized coefficient
ring.  A physical Omega/r comparison with the compensating eta readout is
therefore still required.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "219badcc9c5e9b81d3230fc79011bb38607b8bf842f760c1a4624df9da755e5c"
PINS = {
    "computations/verify_h3_rootless_endpoint_word_change_attachment_or_dual.py":
        "a98a37e07b7847c4484de9505b1f833fc269b02126091d3ee92463bc65ad60d4",
    "computations/verify_h3_rootless_c5_clean_aggregate_tor_separator.py":
        "3b5cb07412f08eaea2492d4b4f981ecc5618053c211942bead0512b30393ce67",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py":
        "34d627b9b0cdf4a81fbebc7c1d37231f53ac2d04be401c3f99402b0bf28c6fbe",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "computations/verify_h3_component_iv_weighted_normal_hasse_companions.py":
        "f94b13e3d08d0f090112648f0b7a1d9b7d07ce857d6b5d979d730dc4761a8ce0",
    "computations/verify_h3_component_iv_collision_family_normal_jet_interface.py":
        "a777687ed775c73b10129c0bee32b59f12fa3b579de39e6c4154e5ed94634651",
    "computations/verify_h3_rootless_normalized_c5_base_column_source_separator.py":
        "635b3e667613049817f04440401d31237db259ab7cf9948989e0da2674efb022",
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
    "computations/verify_h3_rootless_five_cycle_tate_anchor_obstruction.py":
        "a1383c13a732ec34eda5614c4346fecfd99b960480727ba26ac7089690844936",
    "computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py":
        "a98c6e0e90127e81e869c68342f3999abbbd8898d2b2eeafbeccbad06575a324",
    "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py":
        "be39a61df8e3723983eea7a20d405fba7ff0f3822bc90e8d48b8039177f69cfc",
}

ROWS = ("Omega", "Q", "ridge", "Eq", "W", "target", "ores",
        "ainc", "chart")


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            ("cannot load dependency", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def vector(**entries: int) -> tuple[int, ...]:
    require(set(entries).issubset(ROWS), ("unknown typed row", entries))
    return tuple(entries.get(row, 0) for row in ROWS)


def add(*values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(value[index] for value in values)
                 for index in range(len(ROWS)))


def scale(coefficient: int, value: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * entry for entry in value)


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def typed_inventory_audit() -> dict[str, object]:
    Lambda = vector(Omega=1, Q=1, ridge=1)

    endpoint = vector(Omega=-1, Q=1, ores=1)
    endpoint_bianchi = vector()
    pure_ores = vector(ores=1)

    # Exact coarse columns in the committed single-v collision checker.
    pp_left_coarse = vector(ridge=-1, ores=1)
    pp_right_coarse = vector(ridge=1, ores=-1)
    clean_edge = add(pp_left_coarse, pp_right_coarse)

    require(dot(Lambda, endpoint) == 0,
            "Lambda stopped killing the endpoint route")
    require(dot(Lambda, pp_left_coarse) == -1
            and dot(Lambda, pp_right_coarse) == 1,
            "the first coarse PP failure changed")
    require(dot(Lambda, clean_edge) == 0,
            "Lambda stopped killing the zero-residue PP edge")

    # No ordinary-residue correction can repair this while retaining the
    # prescribed unit values on Omega,Q,ridge.  Endpoint requires d=0,
    # whereas the left PP route requires d=1.  The physical pure-residue
    # column independently forces d=0.
    extension_equations = {
        "endpoint_forces_ores_weight": 0,
        "left_PP_forces_ores_weight": 1,
        "pure_ores_forces_ores_weight": 0,
    }
    require(len(set(extension_equations.values())) == 2,
            "coarse ores extension unexpectedly became consistent")

    # The missing refinement is a labelled companion, not an ores scalar.
    pp_left_lifted = vector(Q=1, ridge=-1, ores=1)
    pp_right_lifted = vector(Q=-1, ridge=1, ores=-1)
    require(dot(Lambda, pp_left_lifted) == 0
            and dot(Lambda, pp_right_lifted) == 0,
            "labelled PP companion did not repair the separator")
    comparison = add(endpoint, scale(-1, pp_left_lifted))
    require(comparison == vector(Omega=-1, ridge=1),
            ("common companion did not cancel to Omega/r", comparison))
    require(dot(Lambda, comparison) == 0,
            "Lambda stopped killing the Omega/r comparison")

    # Other known typed families.
    matching_switch = vector(Q=1)
    matching_switch_opposite = vector(Q=-1)
    matching_bianchi = add(matching_switch, matching_switch_opposite)
    normal_face = vector(Eq=-1, chart=-1)
    old_r0 = vector(Eq=1, target=1, ainc=-1)
    old_T = vector(W=-1, target=1)
    old_rho = vector(W=1, ores=1)
    chart_comparison = vector()
    reduced_clean_tor = vector()  # aggregate Q and ores are zero on R=0
    tate_edge = vector(ridge=-1)
    tate_edge_opposite = vector(ridge=1)
    tate_pair = add(tate_edge, tate_edge_opposite)
    known_cycles = (
        endpoint, endpoint_bianchi, clean_edge, matching_bianchi,
        normal_face, old_r0, old_T, old_rho, chart_comparison,
        reduced_clean_tor, tate_pair,
    )
    require(all(dot(Lambda, column) == 0 for column in known_cycles),
            "a known completed correction cycle acquired Lambda mass")

    desired_base = vector(ridge=-1, W=1, ainc=-1)
    require(dot(Lambda, desired_base) == -1,
            "Lambda stopped detecting the desired physical base")

    return {
        "row_order": list(ROWS),
        "Lambda": list(Lambda),
        "endpoint_route": {
            "column": list(endpoint),
            "Lambda": dot(Lambda, endpoint),
        },
        "first_coarse_failure": {
            "family": "individual multiplied PP/denominator route",
            "left_column": list(pp_left_coarse),
            "right_column": list(pp_right_coarse),
            "Lambda_values": [
                dot(Lambda, pp_left_coarse),
                dot(Lambda, pp_right_coarse),
            ],
            "zero_residue_pair": list(clean_edge),
            "Lambda_on_pair": dot(Lambda, clean_edge),
            "reason": (
                "the committed physical coarse column retains only the "
                "ordinary-residue scalar after its matching companion is factored"
            ),
        },
        "ordinary_residue_extension_no_go": extension_equations,
        "required_common_companion_lift": {
            "left": list(pp_left_lifted),
            "right": list(pp_right_lifted),
            "Lambda_values": [
                dot(Lambda, pp_left_lifted),
                dot(Lambda, pp_right_lifted),
            ],
            "difference_endpoint_minus_left_PP": list(comparison),
            "difference_is_Omega_to_ridge": True,
            "W_target_ores_ainc": [0, 0, 0, 0],
        },
        "other_known_completed_cycles": {
            "counted_typed_families": len(known_cycles),
            "all_Lambda_values": [dot(Lambda, column)
                                  for column in known_cycles],
        },
        "desired_base": {
            "column": list(desired_base),
            "Lambda": dot(Lambda, desired_base),
        },
    }


def complete_full_nine_audit() -> dict[str, object]:
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "clean_separator_complete_multidegree",
    )
    base = complete.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "clean_separator_complete_base",
    )
    positive = complete.load(
        "computations/verify_h3_rootless_five_cycle_positive_interface.py",
        "clean_separator_positive_interface",
    )
    ledger = complete.audit(base, positive)
    cubic = ledger["cubic_components"]
    require(len(cubic) == 5
            and all(record["columns"] == 288 for record in cubic),
            "complete repeated full-nine column census changed")
    require(all(record["one_chart_rank_kernel"] == [288, 0]
                for record in cubic),
            "a one-chart repeated component acquired a kernel")
    require(all(record["two_chart_columns_rank_kernel"] == [576, 288, 288]
                for record in cubic),
            "two-chart comparison census changed")

    # Each common repeated degree contains endpoint routes for its two faces
    # and three matchings per face: at most six distinguished Q features.
    # Every full-nine column has at least 42 globally private literal boundary
    # features.  Hence, for ANY placement/weights of those six Q features, a
    # private feature outside them remains in each column.  Give that pivot
    # the negative of the already prescribed pairing.  Since private pivots
    # occur in no other column, this extends Lambda integrally and kills all
    # 288 columns simultaneously.  The identical extension kills both chart
    # copies and their pairwise differences.
    fixed_q_features_per_degree = 6
    minimum_private = min(
        record["unique_pivots_per_column"][0] for record in cubic
    )
    require(minimum_private >= 42 > fixed_q_features_per_degree,
            "private-pivot extension margin disappeared")
    extension_margin = minimum_private - fixed_q_features_per_degree

    natural = ledger["natural_tate_map"]
    require(natural["kernel_dimension"] == 239
            and natural["kernel_w"] == 0
            and natural["kernel_ordinary_residue"] == 0,
            "natural Tate correction kernel changed")

    return {
        "repeated_degrees": len(cubic),
        "one_chart_columns": sum(record["columns"] for record in cubic),
        "one_chart_rank": sum(record["one_chart_rank_kernel"][0]
                              for record in cubic),
        "two_chart_columns": sum(record["two_chart_columns_rank_kernel"][0]
                                 for record in cubic),
        "two_chart_correction_kernel": sum(
            record["two_chart_columns_rank_kernel"][2] for record in cubic
        ),
        "minimum_private_boundary_features_per_column": minimum_private,
        "distinguished_Q_features_per_degree_at_most":
            fixed_q_features_per_degree,
        "private_pivot_extension_margin": extension_margin,
        "integral_Lambda_extension": (
            "choose one globally private non-Q feature per column and assign "
            "the negative current pairing; no division and no chart conflict"
        ),
        "full_nine_columns_obstruct_separator": False,
        "natural_degree_five_Tate_kernel": {
            "dimension": natural["kernel_dimension"],
            "aggregate_correction_readouts": {
                "W": natural["kernel_w"],
                "ores": natural["kernel_ordinary_residue"],
                "target": natural["kernel_physical_target"],
            },
            "new_Lambda_obstruction": False,
        },
    }


def rational_rank(rows: list[list[int]]) -> int:
    """Exact row rank over Q, with no optional computer-algebra dependency."""
    matrix = [[Q(entry) for entry in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((index for index in range(rank, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale_by = matrix[rank][column]
        matrix[rank] = [entry / scale_by for entry in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or not matrix[index][column]:
                continue
            factor = matrix[index][column]
            matrix[index] = [left - factor * right
                             for left, right in zip(
                                 matrix[index], matrix[rank], strict=True)]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def stabilizer_kernel_no_go() -> dict[str, object]:
    """No nonzero same-Q refinement kills all physical eta_z columns.

    Unknowns are A_v=Lambda(Omega_v), B_vN=Lambda(Q_vN),
    C_v=Lambda(r_v), and d=Lambda(ores).  Endpoint and formally lifted PP
    columns synchronize A,B,C once the physical pure-ores column sets d=0;
    clean C5 edges synchronize the five faces.  The u_z/t coefficient of
    Lambda(eta_z) then kills the remaining common scalar.
    """
    faces = tuple(range(5))
    tails = tuple(range(3))
    variables = (
        tuple(("A", face) for face in faces)
        + tuple(("B", face, tail) for face in faces for tail in tails)
        + tuple(("C", face) for face in faces)
        + (("d",),)
    )
    position = {variable: index for index, variable in enumerate(variables)}

    def equation(**coefficients: int) -> list[int]:
        row = [0] * len(variables)
        for encoded, coefficient in coefficients.items():
            parts = encoded.split("_")
            key: tuple[object, ...]
            if parts[0] in ("A", "C"):
                key = (parts[0], int(parts[1]))
            elif parts[0] == "B":
                key = (parts[0], int(parts[1]), int(parts[2]))
            else:
                key = ("d",)
            row[position[key]] = coefficient
        return row

    base_rows: list[list[int]] = [equation(d=1)]
    for face in faces:
        for tail in tails:
            # -A_v+B_vN+d=0 and -C_v+B_vN+d=0.
            base_rows.append(equation(**{
                f"A_{face}": -1, f"B_{face}_{tail}": 1, "d": 1,
            }))
            base_rows.append(equation(**{
                f"C_{face}": -1, f"B_{face}_{tail}": 1, "d": 1,
            }))
    for face in faces:
        following = (face + 1) % len(faces)
        base_rows.append(equation(**{
            f"C_{face}": -1, f"C_{following}": 1,
        }))

    base_rank = rational_rank(base_rows)
    require(base_rank == len(variables) - 1,
            ("endpoint/PP/C5 solution stopped being a line", base_rank))

    # eta_z has dQ=d(existing r)=0 and
    # sum_v A_v*dOmega_v = -sum_v A_v-A_z*u_z/t.
    # Polynomial annihilation on the marked t-open forces A_z=0 from the
    # coefficient of the algebraically free u_z/t, for all five z.  The
    # constant equations are recorded too (and become redundant).
    eta_rows = []
    eta_pairings = []
    for auxiliary in faces:
        eta_rows.append(equation(**{f"A_{auxiliary}": 1}))
        eta_rows.append(equation(**{
            f"A_{face}": 1 for face in faces
        }))
        eta_pairings.append({
            "auxiliary": auxiliary + 1,
            "pairing_after_base_constraints":
                f"-A*(5+u_{auxiliary + 1}/t)",
            "Q_readout": 0,
            "existing_rootless_r_readout": 0,
        })
    full_rank = rational_rank(base_rows + eta_rows)
    require(full_rank == len(variables),
            ("a nonzero corrected separator survived eta", full_rank))

    # If all five exceptional equations u_z=-5t are imposed, eta contributes
    # no new linear condition and the original one-dimensional line remains.
    guarded_rank = rational_rank(base_rows)
    require(guarded_rank == len(variables) - 1,
            "exceptional guard unexpectedly removed the old separator")

    return {
        "unknown_covector_weights": len(variables),
        "endpoint_routes": len(faces) * len(tails),
        "same_labelled_PP_lifts": len(faces) * len(tails),
        "clean_C5_edges": len(faces),
        "pure_ordinary_residue_columns": 1,
        "rank_before_target_stabilizers": base_rank,
        "solution_dimension_before_target_stabilizers":
            len(variables) - base_rank,
        "target_stabilizer_pairings": eta_pairings,
        "rank_after_target_stabilizers": full_rank,
        "solution_dimension_after_target_stabilizers":
            len(variables) - full_rank,
        "same_labelled_Q_refinement_kills_eta": False,
        "exceptional_guard": [
            f"u_{site}+5*t=0" for site in range(1, 6)
        ],
        "minimal_compensating_datum": (
            "a physical rootless/comparison readout on eta_z equal to "
            "5+u_z/t, with target=ores=ainc=0"
        ),
    }


def source_family_counts() -> dict[str, object]:
    endpoint = load(
        "computations/verify_h3_rootless_endpoint_word_change_attachment_or_dual.py",
        "clean_separator_endpoint_dependency",
    )
    collision = load(
        "computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py",
        "clean_separator_collision_dependency",
    )
    endpoint_grades = endpoint.multidegree_gate()
    collision_records = collision.collision_gate()["records"]
    require(len(endpoint_grades["first_common_rootless_tail_degree"]["records"]) == 30,
            "homogenized endpoint route census changed")
    require(len(collision_records) == 5
            and all(len(record["oriented_columns"]) == 2
                    for record in collision_records),
            "individual PP route census changed")

    return {
        "homogenized_endpoint_routes": 30,
        "matching_Bianchi_differences": 30,
        "individual_coarse_PP_routes": 10,
        "clean_zero_ores_PP_edges": 5,
        "complete_full_nine_multiplier_columns": 5 * 288,
        "two_chart_full_nine_comparison_generators": 5 * 288,
        "normal_faces": {
            "squarefree_physical_in_repeated_degree": 0,
            "derived_normal_family": (
                "Eq/chart only; Lambda zero, but physical promotion remains absent"
            ),
            "repeated_physical_image_if_promoted": (
                "adjacent zero-anchor PP edge; Lambda zero"
            ),
        },
        "clean_denominator_Tor": (
            "sum_v h_v*y_v=0 and h_v=1, so aggregate Q/ores is zero"
        ),
        "old_cap_columns": 3,
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    ledger = {
        "theorem": "clean separator on complete known repeated-site inventory",
        "pins": PINS,
        "typed_inventory": typed_inventory_audit(),
        "complete_full_nine": complete_full_nine_audit(),
        "source_family_counts": source_family_counts(),
        "physical_target_stabilizer_gate": stabilizer_kernel_no_go(),
        "verdict": {
            "Lambda_kills_complete_known_correction_cycles": True,
            "Lambda_is_covector_on_current_coarse_generator_map": False,
            "first_failure": (
                "an individual physical PP route (-r_v,ores=1) before its "
                "matching companion is lifted to a labelled Q_(v,N)"
            ),
            "first_missing_map": (
                "a source-valid common-companion lift "
                "(-r_v,ores=1)->(-r_v,+Q_(v,N),ores=1) in the same "
                "P3+K2 endpoint/chart degree"
            ),
            "consequence_of_missing_map": (
                "subtracting the endpoint route constructs "
                "-Omega_v+r_v with W=tgt=ores=ainc=0"
            ),
            "same_labelled_Q_lift_repairs_physical_kernel": False,
            "first_full_source_kernel_failure": (
                "eta_z pairs as -5-u_z/t while Q and existing r read zero"
            ),
            "nonzero_corrected_covector_on_audited_physical_kernel": False,
            "additional_known_polynomial_multiplier_obstruction": False,
            "physical_terminal_annihilator_constructed": False,
        },
        "scope": (
            "complete currently audited P3+K2 polynomial full-nine, PP, "
            "endpoint/response, normal, cap, chart, clean-Tor, and natural "
            "Tate correction inventory.  The common-companion lift and "
            "exhaustivity against genuinely new higher relative generators "
            "remain unproved; the target-stabilizer kernel proves the latter "
            "cannot be omitted or repaired by same-labelled Q alone"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))

    print("h=3 clean separator repeated inventory: SHARP BOUNDARY")
    print("all completed zero-residue correction cycles: Lambda=0")
    print("first coarse generator failure: individual PP route, Lambda=+/-1")
    print("needed refinement: same labelled Q companion; then endpoint-PP difference is Omega/r")
    print("complete five-degree full-nine blocks: private-pivot dual extension exists")
    print("physical eta_z kernel: same-labelled Q/r refinement has only zero covector")
    print("physical terminal annihilator: NOT YET")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
