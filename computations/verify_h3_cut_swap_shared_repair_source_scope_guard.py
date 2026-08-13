#!/usr/bin/env python3
"""Audit the two source assumptions in the shared-repair anchor fibre.

The physical Cartan assumption is proved: the source-orbit theorem constructs
the endpoint-odd Cartan cell in the canonical endpoint-recoloured faces-(3,5)
repeated grade, and the literal M_v theorem places its protected-zero residue
packet in the same complete correction component used by all four repair
directions.

The labelwise pure-ordinary-residue assumption is not proved.  The clean
separator inventory contains one aggregate scalar ores column, and the
abcde normalization uses the same five-row scalar symbol.  Neither artifact
defines a section from that scalar row to the six pure multiplier labels.
The six columns d_ores,i in the anchor-fibre checker were explicitly a
generous grant.  Therefore the Gate-I assembly remains conditional on two
rho-equivariant labelled residue images: one for the fixed shared orbit and
one for the paired orbit (modulo the already physical Cartan residue line).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py":
        "ee04e571ccd6eba9bac1bfbd9233a0d2adeb30c275e4156adefe75570c8911e6",
    "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py":
        "bd20b6320172f846d7c4aa38ec6ebba0c0cfea4c056b8758df19d31b5ab20231",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py":
        "af9a69ad996bd4390ff3fe9139e357a3bb765292ec969350a948612d9b824fa7",
    "computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py":
        "7abab46d3ae648dd309c2fec3266e70dec5b95c5fd150fea2c8c6035840e9bd3",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
}
EXPECTED_LEDGER_SHA256 = "bdad46b583b0fcab4065314bf8bb957bd79b5b502e2e76680d438519857b671a"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
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
        pivot_row += 1
    return pivot_row


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "repair_scope_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "repair_scope_base",
    )
    cartan = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "repair_scope_cartan",
    )
    clean = load(
        "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py",
        "repair_scope_clean",
    )
    abcde = load(
        "computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py",
        "repair_scope_abcde",
    )
    anchor_fibre = load(
        "computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py",
        "repair_scope_anchor_fibre",
    )

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    require((left, right) == (3, 5) and len(pure) == 6,
            "the canonical repair component changed")

    candidates = {
        "fixed_B1": (Q(0), Q(1), Q(0), Q(0), Q(0), Q(0)),
        "fixed_B4": (Q(0), Q(0), Q(0), Q(0), Q(1), Q(0)),
        "paired_B0_B5": (Q(1, 2), Q(0), Q(0), Q(0), Q(0), Q(1, 2)),
        "paired_B2_B3": (Q(0), Q(0), Q(1, 2), Q(1, 2), Q(0), Q(0)),
    }
    require(all(sum(value) == 1 for value in candidates.values()),
            "a shared repair direction lost residue augmentation one")

    # Positive Cartan scope.  This audit is deliberately replayed rather
    # than inferred from a coarse signature: it checks literal root
    # covariance and the physical endpoint source involution.
    cartan_ledger = cartan.audit()
    packet = cartan_ledger["physical_packet"]
    require(packet["ordinary_residue"] == [-1, 1, 1, -1]
            and packet["protected_D_W_target_anchor_Eq"] == 0
            and packet["common_repeated_grade"]
                == "canonical endpoint-recoloured faces-(3,5) bridge",
            "the physical Cartan packet left the repair grade")
    require(cartan_ledger["literal_root_covariance"]["complete_words_checked"]
            == 8748
            and cartan_ledger["literal_endpoint_involution"]
                ["complete_words_checked"] == 6561,
            "the source-provenance Cartan census changed")

    # The clean inventory has exactly one scalar ores coordinate/column in
    # its aggregate nine-row module.  It does not expose six multiplier-
    # labelled residue coordinates or a section from the scalar row.
    clean_typed = clean.typed_inventory_audit()
    clean_stabilizer = clean.stabilizer_kernel_no_go()
    require(clean_typed["row_order"]
            == ["Omega", "Q", "ridge", "Eq", "W", "target", "ores",
                "ainc", "chart"]
            and clean_stabilizer["pure_ordinary_residue_columns"] == 1,
            "the committed scalar pure-residue inventory changed")

    # The target-normalization theorem likewise uses a scalar five-row
    # symbol d_ores.  Its own scope is coarse common-abcde typing, not a
    # six-label section in the canonical cubic component.
    abcde_records = abcde.target_normalized_lift()
    require(len(abcde_records) == 4
            and {record["formula"] for record in abcde_records}
                == {"x=R-T-Y*rho+Y*d_ores"},
            "the scalar target-normalization formula changed")

    # The anchor-fibre theorem itself records the six d_i as a strengthening.
    # This is a logically safe no-go but not a positive source construction.
    fibre_ledger, fibre_digest = anchor_fibre.audit()
    cone = fibre_ledger["generous_complete_projected_cone"]
    require(fibre_digest == anchor_fibre.EXPECTED_LEDGER_SHA256
            and cone["column_families"]["pure_ores_Cartan_companion"] == 6
            and cone["strengthening"].startswith(
                "all labelwise pure-ores companions"),
            "the six labelwise residue columns stopped being an explicit grant")

    # Even under the strongest natural guess that the scalar column lifts to
    # the diagonal vector, the physical Cartan supplies only its established
    # endpoint-odd residue line.  This rank-two space contains none of the
    # four repair directions, so scalar aggregate information cannot silently
    # stand in for the missing section.
    diagonal = (Q(1),) * 6
    cartan_line = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    require(rank((diagonal, cartan_line)) == 2,
            "the scalar/Cartan residue guard changed rank")
    for name, candidate in candidates.items():
        require(rank((diagonal, cartan_line))
                < rank((diagonal, cartan_line, candidate)),
                ("a repair direction entered the guessed scalar/Cartan lift",
                 name))

    ledger = {
        "theorem": "shared-repair source scope guard",
        "pins": PINS,
        "pinned_commits": {
            "physical_Cartan_source_descent": "f746560",
            "literal_Mv_cap_Cartan_composition": "271df91",
            "aggregate_clean_separator_inventory": "d7ff17d",
            "scalar_abcde_target_normalization": "c094bbb",
            "conditional_anchor_fibre": "8e1f858",
        },
        "canonical_repair_component": {
            "faces": [left, right],
            "fine_degree": list(target_degree),
            "complete_columns": len(component["columns"]),
            "pure_multiplier_labels": len(pure),
            "fixed_and_paired_directions": {
                name: [str(entry) for entry in value]
                for name, value in candidates.items()
            },
        },
        "Cartan_scope": {
            "source_provenant": True,
            "physical_grade": packet["common_repeated_grade"],
            "ordinary_residue": packet["ordinary_residue"],
            "protected_D_W_target_anchor_Eq": 0,
            "applies_to_all_four_repair_directions": True,
            "reason": (
                "all four are pure multiplier labels in the same canonical "
                "faces-(3,5) homogeneous component; the bordered alternative "
                "needs one placed physical Cartan column in that component, "
                "not a separate Cartan construction for each basis vector"
            ),
        },
        "pure_ores_scope": {
            "physical_scalar_aggregate_column": True,
            "scalar_ores_coordinates_in_clean_inventory": 1,
            "scalar_target_normalization_formula": "R-T-Y*rho+Y*d_ores",
            "six_multiplier_label_section_constructed": False,
            "six_columns_in_8e1f858": "explicit generous grant",
            "diagonal_scalar_plus_physical_Cartan_line_rank": 2,
            "four_repair_directions_in_that_rank_two_span": False,
            "sharp_missing_statement": (
                "construct two rho-equivariant source chains d_fixed and "
                "d_pair in the canonical faces-(3,5) grade, with zero lower/"
                "W/target/ainc output and labelled ordinary residue equal to "
                "one chosen fixed direction (B1 or B4) and one chosen paired "
                "direction ((B0+B5)/2 or (B2+B3)/2), modulo the already "
                "physical Cartan residue line"
            ),
        },
        "Gate_I_assembly_now": False,
        "reason": (
            "the Cartan side is fully physical, but x_v=R_v-T_v-rho_v+"
            "d_ores,v is not yet source-defined for either shared rho orbit. "
            "Without x_v, U_v-x_v is not a typed J0-kernel element and the "
            "anchor generator/separator dichotomy cannot yet be applied"
        ),
        "scope": (
            "exact audit of the committed canonical Cartan construction and "
            "the committed residue inventories.  It does not prove that the "
            "two labelled residue chains do not exist in a larger relative "
            "source resolution"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("shared repair source-scope ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 shared-repair source scope: ONE MISSING STATEMENT")
    print("physical Cartan in all four repair directions: YES")
    print("labelwise pure-ores section: NOT CONSTRUCTED")
    print("aggregate scalar ores column: one; required equivariant images: two")
    print("Gate-I assembly now: NO (conditional anchor fibre remains valid)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
