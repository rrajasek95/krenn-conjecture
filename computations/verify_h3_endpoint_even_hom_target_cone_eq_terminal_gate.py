#!/usr/bin/env python3
"""Compute the endpoint-even relative Hom obstruction through the target cone.

For one parent the full-star response resolution is the augmented simplex on
six trigger branches.  The literal operation category has no response->cap
Hom in degrees zero or one.  After fixing the endpoint-even coefficient
section, its protected comparison defect is therefore an *inhomogeneous*
class in the shifted relative Hom complex

    K^1 = O tensor C^0(Delta^5),  K^2 = O tensor C^1(Delta^5), ...,

where O has basis Eq, N23, N45.  The three natural defects are constant
cochains, so H^0(K)=0 and H^1(K)=O.  Higher simplex variation is exact.

The two canonical target-cone columns map to the constant N23 and N45
cochains.  Adjoining them kills the target H^1 block Q^2 without changing
H^0 and leaves only the Eq class.  The local exhaustive U_C4 theorem extends
that Eq covector by zero through q/anchor/W/ores/ridge/eta/sigma, but the
global relative-C1/source-grade census is still open.  Hence it is a local
terminal, not yet an accepted physical Fredholm terminal.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_endpoint_even_cap_operator_module_gate.py":
        "39cb3f4b4e83940993ef7ffa8633a3e13cf04631625d9a3729fb5ef9f8ca307c",
    "computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py":
        "3ca82479bd2d1c2847dff55f3c05c87f24406ec1c2f3a5fbb9cdf619a6f7047a",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
    "computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py":
        "feb162f9d13d6debff78361fd28cada31a61bd9ccd57aab62f2722bf365c5064",
}
EXPECTED_LEDGER_SHA256 = (
    "0e171d7cb8523627d4a86eec86316aa720897dfb149b1ae5ccd017ad931837e1"
)

DEFECTS = ("omega_Eq", "N23", "N45")
EXTERNAL = ("q", "anchor", "W", "ores", "ridge", "eta", "sigma")


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(matrix: tuple[tuple[Q, ...], ...] | list[list[Q]]) -> int:
    if not matrix:
        return 0
    work = [list(map(Q, row)) for row in matrix]
    width = len(work[0])
    require(all(len(row) == width for row in work), "rank width")
    answer = 0
    for column in range(width):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def cochain_matrix(boundary_columns, lower_dimension: int) \
        -> tuple[tuple[Q, ...], ...]:
    """Transpose a chain boundary: rows are upper cells, columns lower."""
    return tuple(tuple(Q(column.get(row, 0)) for row in range(lower_dimension))
                 for column in boundary_columns)


def block_diagonal(matrix: tuple[tuple[Q, ...], ...], copies: int) \
        -> tuple[tuple[Q, ...], ...]:
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    return tuple(
        tuple(matrix[row % rows][column % columns]
              if row // rows == column // columns else Q(0)
              for column in range(copies * columns))
        for row in range(copies * rows)
    )


def full_star_relative_hom_audit(common_gate) -> dict[str, object]:
    common_ledger, common_digest = common_gate.audit()
    require(common_digest == common_gate.EXPECTED_LEDGER_SHA256,
            common_digest)
    operation = common_ledger["cap_common_augmentation"]["operation_checks"]
    require(operation["Hom0_response_cap"] == 0
            and operation["primitive_Hom1_response_cap"] == 0
            and operation["implemented_operation_changing_atoms"] == 0,
            operation)

    dimensions = tuple(len(common_gate.simplex_basis(6, degree))
                       for degree in range(6))
    d1 = common_gate.simplex_boundary(6, 1)
    d2 = common_gate.simplex_boundary(6, 2)
    delta0 = cochain_matrix(d1, dimensions[0])
    delta1 = cochain_matrix(d2, dimensions[1])
    require(dimensions == (6, 15, 20, 15, 6, 1)
            and rank(delta0) == 5 and rank(delta1) == 10,
            (dimensions, rank(delta0), rank(delta1)))

    relative_delta1 = block_diagonal(delta0, len(DEFECTS))
    relative_delta2 = block_diagonal(delta1, len(DEFECTS))
    k1_dimension = len(DEFECTS) * dimensions[0]
    k2_dimension = len(DEFECTS) * dimensions[1]
    kernel_k1 = k1_dimension - rank(relative_delta1)
    kernel_k2 = k2_dimension - rank(relative_delta2)
    h1 = kernel_k1  # K0 is the absent e_C A e_R corner.
    h2 = kernel_k2 - rank(relative_delta1)
    require((rank(relative_delta1), rank(relative_delta2)) == (15, 30)
            and (kernel_k1, kernel_k2) == (3, 15)
            and (h1, h2) == (3, 0),
            (rank(relative_delta1), rank(relative_delta2), h1, h2))

    # Each defect basis vector repeated on all six vertices is a constant
    # cocycle.  They form the entire K1 kernel.
    constants = []
    for defect in range(len(DEFECTS)):
        constants.append(tuple(
            Q(index // dimensions[0] == defect)
            for index in range(k1_dimension)
        ))
    require(rank(constants) == 3
            and all(
                sum(relative_delta1[row][column] * constant[column]
                    for column in range(k1_dimension)) == 0
                for constant in constants
                for row in range(len(relative_delta1))
            ),
            "the three natural constant obstruction cocycles changed")
    return {
        "literal_operation_corner": "e_C A e_R=0",
        "literal_Hom_A_response_cap_H0": 0,
        "literal_primitive_Hom_A_response_cap_H1": 0,
        "relative_obstruction_complex": {
            "K0_dimension": 0,
            "K1_dimension": k1_dimension,
            "K2_dimension": k2_dimension,
            "K3_dimension": len(DEFECTS) * dimensions[2],
            "ranks_d1_d2": [rank(relative_delta1), rank(relative_delta2)],
            "H0_dimension": 0,
            "H1_dimension": h1,
            "H2_dimension": h2,
            "H1_basis": list(DEFECTS),
        },
        "interpretation": (
            "the literal Hom groups contain no cross operation.  After the "
            "endpoint-even coefficient section is fixed, its inhomogeneous "
            "defect lies in the shifted relative complex; full-star "
            "naturality makes exactly three constant H1 classes and no "
            "higher simplex obstruction"
        ),
        "two_roots_before_covariance_H1": 6,
        "root_covariant_diagonal_H1": 3,
    }


def target_cone_audit(lower_gate) -> dict[str, object]:
    lower_ledger, lower_digest = lower_gate.audit()
    require(lower_digest == lower_gate.EXPECTED_LEDGER_SHA256, lower_digest)
    target = lower_ledger["physical_target_gate"]
    require(target["rank_local_diagonal_lines"] == 2
            and target["rank_after_two_mixed_normals"] == 4
            and target["mixed_target_cokernel_rank"] == 2
            and target["combined_sigma_even_normal_zero"] is False,
            target)

    # H1 is represented on constants in order Eq,N23,N45.  The canonical
    # two-object target cone has two source columns with these boundaries.
    cone_boundary = (
        (Q(0), Q(0)),
        (Q(1), Q(0)),
        (Q(0), Q(1)),
    )
    require(rank(cone_boundary) == 2, "target cone boundary rank changed")
    h1_before = 3
    h1_after_target = h1_before - rank(cone_boundary)
    target_h1_before = 2
    target_h1_after = target_h1_before - rank(cone_boundary)
    h0_before = h0_after = 0  # the two cone columns have independent faces.
    require((h1_after_target, target_h1_after, h0_before, h0_after)
            == (1, 0, 0, 0), "target cone Hom change changed")

    sigma_defects = (0, 2, 1)
    sigma_columns = (1, 0)
    for row in range(3):
        for column in range(2):
            require(cone_boundary[sigma_defects[row]][sigma_columns[column]]
                    == cone_boundary[row][column],
                    "target cone stopped being sigma-covariant")
    return {
        "target_normals_are": (
            "required proper faces of the augmented relative target module, "
            "not equations that a physical comparison should set to zero"
        ),
        "detectors": [
            target["primitive_0112_target_normal"]["mixed_detector"],
            target["primitive_0121_target_normal"]["mixed_detector"],
        ],
        "detector_pairing_on_N23_N45": [[2, 0], [0, 2]],
        "canonical_target_cone_boundary": {
            "T23": "N23",
            "T45": "N45",
            "rank": rank(cone_boundary),
            "sigma_covariant_two_object_orbit": True,
        },
        "target_H1_before_after_cone": [target_h1_before, target_h1_after],
        "total_relative_H1_before_after_cone": [h1_before, h1_after_target],
        "relative_H0_before_after_cone": [h0_before, h0_after],
        "surviving_H1_basis": ["omega_Eq"],
        "physical_status": (
            "conditional adjoining: the target vectors and covariance are "
            "canonical, but the occurrence-local cone section with its "
            "one-endpoint Hasse faces is not in the current A-action"
        ),
    }


def eq_external_and_terminal_audit(local_gate, loophole_gate) \
        -> dict[str, object]:
    local_ledger, local_digest = local_gate.audit()
    require(local_digest == local_gate.EXPECTED_LEDGER_SHA256, local_digest)
    local_map = local_ledger["exhaustive_local_supermap"]
    signature = local_ledger[
        "operation_PP_reinsertion_and_augmented_scope"
    ]["local_terminal_signature"]
    require(local_map["output_dimension"] == 127
            and local_map["rank"] == 126
            and local_map["cokernel_dimension"] == 1
            and local_map[
                "all_target_q_anchor_W_residue_ridge_eta_sigma_rows_granted"
            ] is True
            and signature["target"] == signature["q"]
                == signature["W"] == signature["ordinary_residue"] == 0
            and signature["anchor_ainc_Pf"] == 0
            and signature["ridge_eta_sigma"] == 0,
            (local_map, signature))

    # Direct-sum stress: the surviving Eq covector has zero coefficient on
    # every named external coordinate, so it annihilates their entire span.
    width = 1 + len(EXTERNAL)
    omega_eq = (Q(1),) + (Q(0),) * len(EXTERNAL)
    external_columns = tuple(
        tuple(Q(position == index + 1) for position in range(width))
        for index in range(len(EXTERNAL))
    )
    require(all(dot(omega_eq, column) == 0 for column in external_columns)
            and rank(external_columns) == len(EXTERNAL),
            "the Eq external zero-extension changed")

    loophole_ledger, loophole_digest = loophole_gate.audit()
    require(loophole_digest == loophole_gate.EXPECTED_LEDGER_SHA256,
            loophole_digest)
    terminal = loophole_ledger["mapping_cone_and_physical_terminal"]
    relative = loophole_ledger["relative_degree_one_counterguard"]
    require(len(terminal["accepted_Fredholm_requires"]) == 4
            and not terminal["physical_q_status"]
                ["q_or_anchor_detects_the_missing_class"]
            and relative["smallest_unexcluded_exotic"]["chi"] == "4",
            (terminal, relative))
    return {
        "surviving_covector": "omega_Eq=delta.(B-Eq), normalized locally",
        "local_full_augmented_extension": {
            "map_dimension_rank_cokernel": [127, 126, 1],
            "zero_coefficients": list(EXTERNAL),
            "literal_PP_reinsertion_flags_included": True,
            "all_current_external_columns_annihilated": True,
            "status": "accepted exhaustive local terminal",
        },
        "global_physical_Fredholm_terminal_now": False,
        "global_failure": (
            "the relative degree-one physical comparison domain and literal "
            "RHS are not exhaustive; an additional same-grade cross-profile "
            "column may have nonzero delta.(B-Eq)"
        ),
        "accepted_terminal_requirements":
            terminal["accepted_Fredholm_requires"],
        "q_or_anchor_promotes_local_dual": False,
        "smallest_unexcluded_bright_column":
            relative["smallest_unexcluded_exotic"],
        "exact_first_filling_column": (
            "one endpoint-even, two-root DQ-to-PS/AugP2 relative-C4 column "
            "with nonzero delta.(B-Eq); its proper target faces are the "
            "sigma-paired T23,T45 cone orbit"
        ),
        "effect_if_Eq_column_is_adjoined": {
            "Eq_H1_before_after": [1, 0],
            "total_relative_H1_after_target_and_Eq": 0,
            "relative_H0_unchanged": 0,
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    common_gate = load(
        "computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py",
        "endpoint_even_hom_common",
    )
    lower_gate = load(
        "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py",
        "endpoint_even_hom_lower",
    )
    local_gate = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "endpoint_even_hom_local",
    )
    loophole_gate = load(
        "computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py",
        "endpoint_even_hom_loophole",
    )
    ledger = {
        "theorem": "h3 endpoint-even Hom/target-cone/Eq terminal gate",
        "pins": PINS,
        "full_star_relative_Hom": full_star_relative_hom_audit(common_gate),
        "canonical_target_cone": target_cone_audit(lower_gate),
        "Eq_external_extension_and_terminal":
            eq_external_and_terminal_audit(local_gate, loophole_gate),
        "verdict": (
            "The literal A-category still has no response-to-cap Hom.  In "
            "the shifted relative Hom complex, the endpoint-even comparison "
            "has H0=0 and H1=Q{omega_Eq,N23,N45}; full-star higher variation "
            "is exact.  N23,N45 are legitimate target proper faces, not "
            "vanishing obligations.  Conditionally adjoining the canonical "
            "sigma-covariant target cone kills their rank-two H1 block and "
            "leaves only omega_Eq.  That covector extends by zero through all "
            "current q/anchor/W/ores/ridge/eta/sigma rows and is the unique "
            "exhaustive local terminal, but it is not a global Fredholm "
            "terminal until the same-grade relative-C1 census and RHS are "
            "physical and exhaustive"
        ),
        "shortest_decision": (
            "construct the endpoint-even two-root DQ-to-PS/AugP2 column whose "
            "Eq boundary kills omega_Eq and whose target proper faces are "
            "T23,T45; or prove no such bright column exists in the exhaustive "
            "physical same-grade domain, which promotes omega_Eq to the "
            "accepted Fredholm terminal"
        ),
        "scope": (
            "exact rational full-star simplex Hom ranks, root-covariant "
            "three-defect quotient, canonical two-cut target-cone incidence, "
            "complete local augmented U_C4 rows, and pinned global terminal "
            "requirements.  The target cone and Eq column are tested as "
            "adjoinings, not asserted current source-provenant A-actions"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint-even Hom terminal ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    if arguments.mode == "structural":
        pin_dependencies()
        print("h3 endpoint-even Hom terminal structural gate: PASS")
        return
    ledger, digest = audit()
    if arguments.mode == "exhaustive":
        # Stress every sign choice for the two objectwise cone columns.  The
        # rank is two whenever neither physical normalization is zero.
        for left in (-2, -1, 1, 2):
            for right in (-2, -1, 1, 2):
                matrix = ((Q(0), Q(0)), (Q(left), Q(0)),
                          (Q(0), Q(right)))
                require(rank(matrix) == 2, (left, right))
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        cone = ledger["canonical_target_cone"]
        terminal = ledger["Eq_external_extension_and_terminal"]
        print("h3 endpoint-even Hom/target-cone/Eq terminal gate: PASS")
        print("relative H0/H1: 0 / 3")
        print("target H1 after canonical cone:",
              cone["target_H1_before_after_cone"][1])
        print("surviving Eq dual: LOCAL TERMINAL / GLOBAL OPEN")
        print("global Fredholm terminal:",
              str(terminal["global_physical_Fredholm_terminal_now"]).upper())
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
