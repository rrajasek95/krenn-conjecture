#!/usr/bin/env python3
"""Reconcile T12 with the orbit-D4 and pointed K_Eq comparisons.

The first-hit statement ``[T12]=[R_E14]`` does not define a second
construction problem once the source-labelled central placement

    E=(H0-u)e_Eq  -->  R_E14

exists.  The old physical unary row is exactly ``U=T12-R_E14``, so the
placed return and U supply all twelve tails.

The moving-target D4 top reaches the same occurrence ``g=R_E14`` on the
silent fibre, but only after forgetting the source-domain/central-Eq row.
Its source is the centered occurrence/orbit cube, not E.  This checker
freezes the exact missing comparison and scopes the old first-hit/D1--D3
dual: adjoining R raises the first-hit rank and kills that dual, whereas
the D4 occurrence top alone still lacks one central-Eq direction.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_d4_unary_moving_target_bicomplex_gate.py":
        "facdbbdcb4f85011c34eeab94c4219b995360381667c6ab790b39612ec397f77",
    "notes/h3-e14-d4-unary-moving-target-bicomplex-gate.md":
        "b79421dd10aaf55fa8a4bffcfa8881193ba5930e1542e4215a575e05c3155114",
    "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py":
        "754038f33ae07329e0fc6a8825df9f1695664a40df91afbb77e52dedb1e1aae1",
    "notes/h3-e14-cplus-keq-companion-assembly-gate.md":
        "8548c1db8ec362fce0876c0f67d77efc96f141ebd4c82b6564069e3a089eff3a",
    "computations/verify_h3_e14_augp2_post_residue_master_local_reduction.py":
        "5924fbd6559514c1b9a46b5df658c0cc98dfe4dc33de1d5c78d940974012eccb",
    "notes/h3-e14-augp2-post-residue-master-local-reduction.md":
        "22d3e112f34f5c325ea7bc297609f20c392e92b8d07756c464adbd37ab2a051f",
    "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
    "notes/h3-e14-orbit-relative-d4-target-cone-gate.md":
        "6268689c54144cc09b6be596b81d8b4aa741e0590a83e664ec3f6e65b89187bf",
    "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py":
        "5eef4dff45be6e8993808ef5bcb533d62143dd4bc833a16e2015b48e7bc408d8",
    "notes/h3-e14-keq-private-placement-pointedness-gate.md":
        "59111d6a2dda8a16785cab6c6d129c806ea7e01a2a6d54e092c8841f6521c6c0",
}
EXPECTED_LEDGER_SHA256 = "107c6e3e10bd3dd4c9ac6bd76e27defbcd138a205e9eb9470934baacce0c9b94"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    width = len(columns[0])
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, width)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(width):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def first_hit_after_private_placement() -> dict[str, object]:
    assembly = load(
        "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py",
        "t12_reconcile_assembly",
    )
    endpoint_q = assembly.load(
        "computations/verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py",
        "t12_reconcile_endpoint_q",
    )
    data, identity = assembly.e14_spair_identity(endpoint_q)
    target = data["target"]
    columns = data["columns"]
    unary = columns[data["selected_name"]]
    private_return = assembly.RETURN
    first = data["first"]

    require(assembly.sparse_add((1, unary), (1, private_return)) == target
            and identity["exact_identity"]
                == "B_E14=U[000101]*v24_11+R_E14",
            "the exact unary/private companion identity changed")

    old_pivots = {}
    for column in columns.values():
        first.add_exact_column(column, old_pivots)
    old_remainder = first.exact_reduce(target, old_pivots)
    require(len(columns) == len(old_pivots) == 269
            and old_remainder == private_return,
            ("the old first-hit quotient changed", len(columns),
             len(old_pivots), old_remainder))

    placed_pivots = dict(old_pivots)
    private_raises_rank = first.add_exact_column(
        private_return, placed_pivots)
    placed_remainder = first.exact_reduce(target, placed_pivots)
    require(private_raises_rank
            and len(placed_pivots) == 270
            and not placed_remainder,
            ("private placement stopped closing T12", len(placed_pivots),
             placed_remainder))
    require(endpoint_q.pair(data["dual"], private_return) == -1
            and endpoint_q.pair(data["dual"], target) == -1,
            "the first-hit dual stopped seeing exactly the private return")

    # Let C be the exact first-hit source combination with T12-C=R.  The
    # selected old unary column U already satisfies T12-U=R.  Since the 269
    # source columns are independent, C=U in the free source module.  Thus
    # the tempting Schreyer cycle Z=U-C is literally zero; its standard
    # Schreyer/Koszul representation is the empty combination.
    source_kernel_dimension = len(columns) - len(old_pivots)
    require(source_kernel_dimension == 0
            and first.exact_reduce(unary, old_pivots) == {}
            and assembly.sparse_add((1, target), (-1, unary))
                == private_return,
            "the unique first-hit lift stopped being the old unary column")
    return {
        "old_first_hit_columns_rank": [len(columns), len(old_pivots)],
        "old_quotient_identity": "[T12]=[R_E14]",
        "old_primitive_dual_values": {"T12": -1, "R_E14": -1},
        "adjoining_source_labelled_R_raises_rank": True,
        "rank_after_R_placement": len(placed_pivots),
        "T12_remainder_after_R_placement": 0,
        "exact_physical_identity": "T12=U[000101]*v24_11+R_E14",
        "all_twelve_word_resolved_tails_supplied_by_old_U_plus_R": True,
        "new_T12_direction_after_R_placement": False,
        "old_first_hit_dual_survives_after_R_placement": False,
        "unique_first_hit_lift_C": "U[000101]*v24_11",
        "source_kernel_dimension_before_R": source_kernel_dimension,
        "candidate_Schreyer_cycle": "Z=U-C=0",
        "candidate_Z_support": 0,
        "candidate_Z_word_counts": {},
        "candidate_Z_multiplier_counts": {},
        "candidate_Z_in_standard_Schreyer_Koszul_module": True,
        "candidate_Z_membership_certificate": "empty (zero vector)",
        "nonzero_higher_syzygy_for_T12": False,
    }


def orbit_top_versus_central_placement() -> dict[str, object]:
    orbit = load(
        "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py",
        "t12_reconcile_orbit",
    )
    orbit_ledger, orbit_digest = orbit.audit()
    require(orbit_digest == orbit.EXPECTED_LEDGER_SHA256,
            "the orbit-D4 ledger changed")
    occurrence = orbit_ledger["marked_occurrence_local_system"]
    require(occurrence["formal_D4_of_c_f"] == "c_g"
            and not occurrence["bottom_P_f_constructed_by_orbit_cube"],
            ("the orbit occurrence scope changed", occurrence))

    pointed = load(
        "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py",
        "t12_reconcile_pointed",
    )
    pointed_ledger, pointed_digest = pointed.audit()
    require(pointed_digest == pointed.EXPECTED_LEDGER_SHA256,
            "the pointed placement ledger changed")
    candidate = pointed_ledger["dependencies"]["selected_chain_assignment"]
    require(candidate["F=H0-u"] == "1-v04_00"
            and candidate["image"] == "R_E14",
            ("the central private placement changed", candidate))

    # Necessary forgetful quotient.  Rows are (private occurrence R,
    # central Eq-input incidence).  The silent orbit top has the right first
    # coordinate, but its domain is the centered occurrence/root cube and it
    # has no central Eq-input coordinate.  The required placement has both.
    orbit_occurrence_top = (Q(1), Q(0))
    required_E_to_R = (Q(1), Q(1))
    horizontal_cap_graph = (Q(0), Q(0))
    central_eq_dual = (Q(0), Q(1))
    require(rank((orbit_occurrence_top,)) == 1
            and rank((orbit_occurrence_top, required_E_to_R)) == 2
            and sum(a * b for a, b in
                    zip(central_eq_dual, orbit_occurrence_top, strict=True)) == 0
            and sum(a * b for a, b in
                    zip(central_eq_dual, horizontal_cap_graph, strict=True)) == 0
            and sum(a * b for a, b in
                    zip(central_eq_dual, required_E_to_R, strict=True)) == 1,
            "the D4/central-Eq separator changed")
    return {
        "forgetful_rows": ["private occurrence R", "central Eq-input E"],
        "silent_orbit_D4_top": [1, 0],
        "required_E_to_R_placement": [1, 1],
        "horizontal_cap_graph": [0, 0],
        "rank_orbit_top": 1,
        "rank_with_required_placement": 2,
        "primitive_missing_dual": [0, 1],
        "coefficient_projection_agrees_on_silent_fibre": "g=R_E14",
        "source_domains_agree": False,
        "D4_top_domain": (
            "centered occurrence c_f/P_f over the moving 110000->111111 "
            "target orbit"
        ),
        "required_domain": "E=(H0-u)e_Eq in the central K_Eq comparison",
        "horizontal_T_plus_rho_supplies_missing_Eq_incidence": False,
        "exact_missing_equality": (
            "Phi_orb((H0-u)e_Eq)=R_E14 as a source-labelled full-row "
            "boundary, not merely pi_occ(Phi_orb)=g at v04=0"
        ),
        "interpretation": (
            "the moving-target cone solves the affine target-normal defect, "
            "but a comparison from the central Eq product to its marked D4 "
            "top is still required"
        ),
    }


def master_and_d1d3_scope() -> dict[str, object]:
    bicomplex = load(
        "computations/verify_h3_e14_d4_unary_moving_target_bicomplex_gate.py",
        "t12_reconcile_bicomplex",
    )
    bicomplex_ledger, bicomplex_digest = bicomplex.audit()
    require(bicomplex_digest == bicomplex.EXPECTED_LEDGER_SHA256,
            "the D1--D3 bicomplex ledger changed")
    exact = bicomplex_ledger["literal_and_complete_D1_D3_test"]
    require(exact["reduced_T12"] == "R_E14=g-v04_00*g"
            and not exact["existing_D1_D3_cancel_T12"],
            ("the D1--D3 scope changed", exact))

    master = load(
        "computations/verify_h3_e14_augp2_post_residue_master_local_reduction.py",
        "t12_reconcile_master",
    )
    master_ledger, master_digest = master.audit()
    require(master_digest == master.EXPECTED_LEDGER_SHA256,
            "the post-residue master ledger changed")
    main = master_ledger["post_residue_main_quotient"]
    require(not main["new_residue_coefficient_direction"]
            and all(value == 0 for value in main["main_rows_after_grants"].values()),
            ("a main row survived the master grants", main))
    return {
        "D1_D3_no_go_correct_scope": (
            "old D1--D3 rows do not construct the missing R placement; "
            "their surviving class [T12]=[R] is the same private class"
        ),
        "D1_D3_no_go_proves_independent_T12_cell_needed": False,
        "after_full_E_to_R_placement": (
            "old U supplies T12, rooted d_even cancels the exact labelled "
            "residue, and all main occurrence/Eq/lower/target/ores rows vanish"
        ),
        "remaining_T12_specific_anchor_q_ridge_rows": [],
        "physical_q_scope": (
            "handled by the existing defect/transport alternative once the "
            "full source-labelled P2 comparison is physical"
        ),
        "ridge_scope": (
            "the labelled shifted ridge remains a face of the master AugP2 "
            "schema, not a new face caused by T12"
        ),
        "presentation_syzygy_U_minus_C": (
            "may measure coherence between two old presentations, but is "
            "not required for the minimal E14 companion boundary theorem"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14 T12/central-placement/orbit-D4 reconciliation",
        "pins": PINS,
        "first_hit_after_private_placement":
            first_hit_after_private_placement(),
        "orbit_top_versus_central_placement":
            orbit_top_versus_central_placement(),
        "master_and_D1_D3_scope": master_and_d1d3_scope(),
        "verdict": (
            "T12 is not an independent companion obstruction.  Adjoining "
            "the source-labelled central placement E=(H0-u)e_Eq->R_E14 "
            "raises the first-hit rank 269->270, kills its primitive dual, "
            "and the old unary row supplies all twelve tails.  The moving-"
            "target D4 top currently supplies only the coefficient/occurrence "
            "shadow g=R on the silent fibre.  Its domain has zero central-Eq "
            "incidence, so the one missing equality is the full source-"
            "labelled comparison Phi_orb(E)=R_E14"
        ),
        "scope": (
            "canonical h=3 chart-(1,1), silent v04=0 E14 packet.  The rank "
            "and unary identities are exact.  This does not construct the "
            "central-Eq-to-orbit comparison; it removes T12 as a separate "
            "theorem only conditional on that full placement"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    first_hit = ledger["first_hit_after_private_placement"]
    print("T12 after source-labelled E->R placement: CLOSED BY OLD U")
    print("first-hit rank: 269 -> 270; old dual killed")
    print("candidate Z=U-C: support="
          + str(first_hit["candidate_Z_support"])
          + ", word_counts=" + str(first_hit["candidate_Z_word_counts"]))
    print("standard Schreyer/Koszul membership: ZERO CERTIFICATE")
    print("orbit D4 top: occurrence g=R YES / central Eq incidence NO")
    print("single missing equality: Phi_orb((H0-u)eEq)=R_E14")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
