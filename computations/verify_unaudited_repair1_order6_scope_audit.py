#!/usr/bin/env python3
"""Scope-audit the external repair-1 order-six comparison probe.

The probe proves an exact equality only after projecting both constructions
to the ungraded codimension-two pair shadow.  Its domain is the 8,580-column
order-six coefficient-operator block, not the fifteen collision-label
complex, and its target shadow is not the 90/360-term full-nine boundary.
Consequently it neither proves nor disproves the selected equation

    J3(M_v) = A J_col(u_024-u_012).

The probe does expose two useful obstructions.  The chosen operator class
has raw fine-shift supports 39 and 24, while the displayed physical K has
word-row supports 10 and 10; only their grade-forgotten totals agree.  And
the universal attainable D2 space has a nonzero projection to site-repeating
pair coordinates, so no comparison to the direct-free target can exist on
the whole operator kernel without enlarging the target.  The reported
153-dimensional size is a matching two-prime modular rank, not an exact
rational dimension certificate.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE = "computations/unaudited-repair1-k-chain-map-2026-08-13"
PINS = {
    f"{PROBE}/REPORT.md":
        "53bd84a6ccd13ee848a24320b309ed41db99cc08bbdace70a2e5958647fd1075",
    f"{PROBE}/step1_physical.json":
        "a90f56c251affbed5a5b4962f1730863ee7a6cdf611092d836d7598bf23770ce",
    f"{PROBE}/step2_operator.json":
        "52c2bbea7763a2c88431580a04cd599138c3d090bb29b836e6d6861cca30cbc0",
    f"{PROBE}/step5_refined.json":
        "464694841fcec6a50edb41cdfbc90d5920ee8014b1fba70680e5b2507b1950f2",
    f"{PROBE}/step6_characterise.json":
        "fd3a426e71bcc5cc0427d9fe090179954a3a554d31e517452a6e806b05de73f6",
    f"{PROBE}/step7_ranks.json":
        "63ea2b4c5f25830a2501134161da98aadb8f01aea8f818334671c7d980eaff25",
    f"{PROBE}/step9_obstruction.json":
        "82960f5a7a26b6c97a41f41037d3b1070ebc8b3b502c551097e8dbec587ef56b",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py":
        "ea45c09a8347c312ea9721475d54a4b4f9aad21d8d51cb9d4d297aeaa99ba429",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py":
        "a1c7868bee94baf12f0f4915305bb1e21cdc3f6732ccec9adf3d68768d3d90b0",
}
EXPECTED_LEDGER_SHA256 = (
    "f4b46116dc1b766c6d5e9777169fa7d67ac9785214e8ccd860d9f585af01a2de"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def read_json(name: str):
    return json.loads((ROOT / PROBE / name).read_text())


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    physical = read_json("step1_physical.json")
    operator = read_json("step2_operator.json")
    refined = read_json("step5_refined.json")
    freedom = read_json("step6_characterise.json")
    ranks = read_json("step7_ranks.json")
    obstruction = read_json("step9_obstruction.json")

    require(physical["committed_alpha"] == ["-1", "1", "1", "-1"]
            and physical["derived_alpha_from_(1-s)(w-1)_on_physical_corner"]
                == ["-1", "1", "1", "-1"]
            and physical["shadow2_K_phys_equals_expected_second_shadow"]
            and physical["shadow2_K_phys_support"] == 16,
            "the grade-forgotten physical K shadow changed")
    require(operator["columns"] == 8580
            and operator["source_output_support"] == 0
            and operator["d1_output_support"] == 0
            and operator["d2_output_support"] == 16
            and operator["d2_equals_expected_second_shadow"],
            "the selected order-six D2 class changed")
    require(refined["operator_component_supports"] == [24, 39]
            and refined["physical_component_supports"]
                == {"mixed_word_grade": 10, "pure_word_grade": 10}
            and refined["fine_shift_splitting_matches_word_grade_splitting"]
                is False
            and all(not record["matching_physical_grade"]
                    for record in refined["component_pairing"]),
            "the raw fine-shift/physical-word mismatch changed")
    require(freedom["raw_freedom"] == 21
            and freedom["rank_of_all_committed_readouts_on_freedom"] == 14
            and freedom["residual_freedom_after_all_readouts"] == 7
            and all(record["shadow2_is_zero"]
                    for record in freedom["residual_vectors"]),
            "the K-shadow indeterminacy changed")
    require({(record["rank_full_block"],
              record["rank_constraint_projection_source_plus_D1"],
              record["dim_attainable_D2_on_ker(source,D1)"])
             for record in ranks} == {(1328, 840, 488)},
            "the two-prime operator ranks changed")
    require({(record["dim_S"],
              record["rank_of_S_projected_to_NON-physical_pair_coordinates"],
              record["S_is_contained_in_physical_coordinates"])
             for record in obstruction} == {(488, 153, False)},
            "the modular nonphysical-coordinate obstruction changed")

    report = (ROOT / PROBE / "REPORT.md").read_text()
    for phrase in (
        "shadow_2(K_phys) = D2(operator",
        "fine-shift split of D2 (39+24)",
        "equality holds only after forgetting",
        "153-dimensional separator family",
        "eta/sigma",
    ):
        require(phrase in report, ("probe report statement changed", phrase))

    ledger = {
        "theorem": "scope audit of the unaudited repair-1 order-six probe",
        "pins": PINS,
        "independently_useful_positive": {
            "domain": "8580-column order-six coefficient-operator block",
            "constraints": "literal source=0 and D1=0 on the selected 343-term class",
            "comparison": "shadow_2(K_phys)=D2(selected operator class)",
            "support": 16,
            "alpha_derived_from_actions": [-1, 1, 1, -1],
            "grade_status": "equality only after forgetting the two raw fine shifts",
        },
        "not_the_Gate_I_one_chain_equation": {
            "Gate_I_domain": (
                "the line generated by l=u_024-u_012 in the 15-label "
                "collision/repeated-edge module"
            ),
            "Gate_I_codomain": (
                "complete 360-feature seven-edge repeated-P3+K2 boundary "
                "plus Eq,target,ainc,ores,eta/sigma"
            ),
            "probe_domain": "order-six coefficient operators",
            "probe_codomain": "codimension-two coloured cell-pair shadow",
            "Jcol_l_evaluated": False,
            "literal_90_360_boundary_evaluated": False,
            "augmented_rows_evaluated": False,
            "verdict": "neither proves nor disproves J3(M_v)=A Jcol(l)",
        },
        "fine_grade_obstruction": {
            "operator_raw_shift_supports": [39, 24],
            "displayed_K_word_row_supports": [10, 10],
            "matching_raw_components": 0,
            "exact_consequence": (
                "the identity-on-raw-grade refinement of this selected D2 "
                "comparison fails; a shifted tail/total-degree translation "
                "would be additional data"
            ),
            "nonconsequence": (
                "this does not obstruct the collision line comparison, whose "
                "domain and shift A are absent from the probe"
            ),
        },
        "K_indeterminacy": {
            "raw_shadow_fibre": 21,
            "committed_readout_rank": 14,
            "residual_shadow_zero_freedom": 7,
            "meaning": (
                "pair shadow, parity, corner residue, and the encoded coarse "
                "readouts do not pin a termwise physical K; a full-nine or "
                "equivalent higher readout is required"
            ),
        },
        "universal_operator_obstruction": {
            "attainable_D2_dimension_mod_primes": 488,
            "nonphysical_projection_rank_mod_primes": 153,
            "primes": [record["prime"] for record in obstruction],
            "robust_consequence": (
                "the naive whole-kernel comparison to a target containing "
                "only direct-free disjoint-cell pairs is obstructed in both "
                "reductions; an enlarged site-repeating target is indicated"
            ),
            "precision_guard": (
                "153 is a matching two-prime modular rank, not a proved exact "
                "rational dimension; the probe supplies no rational left-null "
                "certificate for that full dimension"
            ),
        },
        "sharp_interpretation": (
            "the external computation strengthens the associated-graded "
            "evidence and rules out a naive grade-preserving universal "
            "order-six comparison.  It leaves the selected Gate-I full-row "
            "equation exactly open; the next exact datum is still Jcol(l) in "
            "the literal augmented repeated grade, not another order-six "
            "pair-shadow calculation"
        ),
        "scope": (
            "read-only audit of an unaudited external probe.  The JSON ranks "
            "are accepted only with the precision qualifications stated above"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("repair-1 scope ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("unaudited repair-1 order6 probe: SCOPE AUDITED")
    print("ungraded D2=shadow2(K): YES (16 terms)")
    print("raw fine-grade refinement: NO (39/24 versus 10/10)")
    print("selected J3(Mv)=A Jcol(l): NOT TESTED")
    print("universal direct-free comparison: MODULARLY OBSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
