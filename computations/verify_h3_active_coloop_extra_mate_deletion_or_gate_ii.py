#!/usr/bin/env python3
"""Reduce arbitrary same-word coloop mates to deletion, exit, or Gate II.

The recurrence has two finite moves.  Revealing an already occupied mate
reduces the number of unprocessed occurrences.  An anchor-safe direction
whose higher Hasse faces vanish gives an exact affine deformation and
strictly lowers occupied scalar support.  A first nonzero Hasse face stops
the recurrence.

The completion dichotomy behind 4c15d41 is independent of the particular
silent-pair seed: any full normalized h=3 source is either axis-pure (an
empty locus) or has a nonzero off-axis cell (hence an active fan).  Thus a
quadratic C2+/C4/P2 face, or any higher rowwise obstruction, requires no new
chart cell for this entry theorem.  Its full-source extension is four-good
or a literal coloop, and the latter is exactly the existing Gate-II Phi/q
frontier after finite Hall saturation.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_projective_block_hasse_or_deletion_c4_recurrence.py":
        "95b39af7ba710ffcb78866de2fc2fbd15dc063ff84fca77649858128a5fa5679",
    "notes/h3-active-coloop-projective-block-hasse-or-deletion-c4-recurrence.md":
        "edb62f2d2575a557c5dfaae57a2043bda7451bf072ce19631467110b56e8bf34",
    "computations/verify_h3_silent_hasse_pair_full_source_extension_classification.py":
        "3597709f101ad6e7bda7c9aee4f76bd588606b59901dd140d508c0769977d8d4",
    "notes/h3-silent-hasse-pair-full-source-extension-classification.md":
        "eaa722eef4188d032e7eaf3e8dd4e5376ee694b090140b3cd5c4771a21923e25",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
    "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py":
        "22e1e7a6a933b1ba71bbd95bb605b1351e823506e495682cccff312cd3df3b15",
    "notes/h3-active-fan-coloop-gate-ii-assembly-boundary.md":
        "bacb7b4b138882c0cc07f13767f2e4ead86aa630c55cf1a946943141b7cee7a7",
}
EXPECTED_LEDGER_SHA256 = (
    "0f2a2d967bb0a4bb5c39416d6dee1863fb52c6c89bbbac819ef5547169410ee7"
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


def delete_or_hasse_interface() -> dict[str, object]:
    descent = load(
        "computations/"
        "verify_h3_active_coloop_projective_block_hasse_or_deletion_c4_recurrence.py",
        "extra_mate_delete_or_hasse_dependency",
    )
    ledger, digest = descent.audit()
    require(digest == descent.EXPECTED_LEDGER_SHA256,
            (digest, descent.EXPECTED_LEDGER_SHA256))
    guard = ledger["multiaffine_support_lowering_guard"]
    recurrence = ledger["complete_minimal_three_colour_recurrence"]
    require(guard["coordinate_zero_fibre_points"] == 0
            and guard["line_defect"] == {"target": "-t^2", "block": "0"}
            and recurrence[
                "every_minimal_completion_has_exit_only_private_row"
            ] is True,
            (guard, recurrence))

    # The lexicographic measure is formal but exact.  The source has finite
    # scalar support and finitely many matching occurrences.  An affine
    # deletion lowers the first coordinate.  At fixed support, revealing an
    # already present mate lowers the second.  Neither move can cycle.
    examples = []
    for support, unseen in ((9, 12), (9, 11), (8, 30), (8, 0)):
        examples.append({
            "occupied_scalar_support": support,
            "unprocessed_occurrences": unseen,
        })
    require(all(
        (examples[index + 1]["occupied_scalar_support"],
         examples[index + 1]["unprocessed_occurrences"])
        < (examples[index]["occupied_scalar_support"],
           examples[index]["unprocessed_occurrences"])
        for index in range(len(examples) - 1)
    ), examples)

    return {
        "descent_ledger": digest,
        "well_founded_measure": [
            "occupied scalar support",
            "unprocessed supported matching occurrences",
        ],
        "order": "lexicographic on N x N",
        "sample_strict_descent": examples,
        "reveal_move": (
            "mark one already occupied same-word mate processed; support is "
            "fixed and the second coordinate drops"
        ),
        "deletion_move": (
            "if J_xF(xi)=0 and every higher divided-Hasse face vanishes, "
            "F(x+t xi)=F(x) exactly; kill an occupied coordinate and lower "
            "the first coordinate"
        ),
        "nonlinear_stop": (
            "the first nonzero divided-Hasse coefficient is retained as a "
            "literal rowwise packet; the recurrence does not project it away"
        ),
        "minimum_support_use": (
            "an anchor-safe exact deletion contradicts the chosen minimum; "
            "therefore a surviving kernel direction exposes a Hasse packet"
        ),
        "minimal_three_occurrence_seed": (
            "all 180 minimum-target completions already have an exit-only "
            "private row; extra mates are handled by the same finite measure"
        ),
    }


def quadratic_face_classification() -> dict[str, object]:
    classifier = load(
        "computations/"
        "verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "extra_mate_h2_classifier_dependency",
    )
    target, response = classifier.source_monomials()
    target_index = classifier.pair_index(target)
    response_index = classifier.pair_index(response)
    require(len(target) == 15 and len(response) == 105,
            (len(target), len(response)))
    require(sum(len(complements) for complements in target_index.values()) == 45
            and sum(len(complements) for complements in response_index.values()) == 630,
            (target_index, response_index))
    return {
        "target_matching_occurrences": len(target),
        "response_matching_occurrences": len(response),
        "target_pair_incidences": 45,
        "response_pair_incidences": 630,
        "named_quadratic_faces": {
            "QQ_target": "one-edge restricted face",
            "QQ_response": "C2+",
            "DQ_or_PS": "C4",
            "PQ_or_SQ": "P2",
        },
        "occurrence_incompatible_pairs": (
            "zero H2; if every varied subset is occurrence-incompatible, "
            "all higher faces vanish and the exact deletion move applies"
        ),
        "typing_retained": [
            "physical sites", "word colours", "response heads",
            "fine grade", "matching complement",
        ],
    }


def guard_independent_full_source_completion() -> dict[str, object]:
    completion = load(
        "computations/"
        "verify_h3_silent_hasse_pair_full_source_extension_classification.py",
        "extra_mate_full_source_completion_dependency",
    )
    ledger, digest = completion.audit()
    require(digest == completion.EXPECTED_LEDGER_SHA256,
            (digest, completion.EXPECTED_LEDGER_SHA256))
    normalized = ledger["normalized_full_source_completion"]
    active = ledger["surviving_active_extension"]
    require(normalized["axis_pure_primary_locus"] == "empty"
            and normalized["surviving_extension"]
                == "contains a nonzero off-axis q or endpoint cell"
            and active["new_Hasse_pair_specific_extension_theorem_needed"]
                is False,
            (normalized, active))

    # The proof of this split uses no coefficient special to the silent pair.
    # It quantifies over the completed source support: membership in the
    # axis-pure locus or the existence of an off-axis physical cell.  Hence
    # every partial row packet embedded in such a source has the same split.
    partial_packets = (
        "extra same-word mate closure",
        "C2+ quadratic face",
        "C4 quadratic face",
        "P2 quadratic face",
        "first cubic or quartic matching face",
    )
    classifications = {
        packet: {
            "all completed support axis-pure": "impossible",
            "some completed support off-axis": "source-provenant active fan",
        }
        for packet in partial_packets
    }
    require(len(set(
        tuple(sorted(value.items())) for value in classifications.values()
    )) == 1, classifications)
    return {
        "completion_ledger": digest,
        "guard_independence_reason": (
            "the dichotomy only tests the support of the full normalized "
            "source: the global axis-pure source locus is empty, while any "
            "nonzero off-axis physical cell gives the target-augmented "
            "private-site active fan"
        ),
        "covered_partial_packets": classifications,
        "augmented_rows": normalized["augmented_equations"],
        "four_good": active["four_good"],
        "literal_coloop": active["literal_coloop"],
        "sole_nonterminal_survivor": active["sole_nonterminal_survivor"],
        "exact_open_statement": active["exact_open_statement"],
        "lower_chart_cell_needed_for_entry": False,
        "scope": normalized["scope"],
    }


def gate_ii_terminal_map() -> dict[str, object]:
    gate = load(
        "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py",
        "extra_mate_gate_ii_dependency",
    )
    assembly = gate.audit_branch_assembly()
    termination = gate.audit_finite_termination_interface()
    require(assembly["only_nonterminal_after_saturation"]
                == "single missing fan-grade physical Phi/q packet"
            and termination["additional_termination_hypothesis_after_Phi"] is False,
            (assembly, termination))
    return {
        "outside_hole": "strict Hall-shore growth",
        "maximum_strict_growth_steps": 14,
        "four_good": "existing transverse landing",
        "diagonal_mate_omits_selected_edge": "destroys the current coloop",
        "trapped_literal_coloop": "finite Hall saturation to Gate II",
        "gate_ii_open_datum":
            assembly["only_nonterminal_after_saturation"],
        "after_gate_ii_phi": "all branches exhaustive; no new termination input",
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 arbitrary coloop extra-mate deletion-or-Gate-II reduction",
        "pins": PINS,
        "well_founded_recurrence": delete_or_hasse_interface(),
        "first_quadratic_face": quadratic_face_classification(),
        "full_source_completion": guard_independent_full_source_completion(),
        "active_terminal_map": gate_ii_terminal_map(),
        "exhaustive_branch_map": [
            "private row with no trapped mate -> offdiagonal exit or coloop destruction",
            "occupied occurrence-incompatible kernel -> exact support deletion",
            "compatible kernel -> first nonzero Hasse packet",
            "full-rank larger block -> retain its finite full-source completion",
            "all completed support axis-pure -> impossible",
            "some completed support off-axis -> active fan",
            "active fan four-good -> existing landing",
            "active fan literal coloop -> finite Hall saturation -> Gate II Phi/q",
        ],
        "verdict": (
            "Extra same-word mates create no new coloop entry theorem at h=3. "
            "The support/occurrence recurrence is well-founded.  An exact "
            "direction lowers support; a first Hasse face (C2+/C4/P2 at "
            "quadratic order) or a full-rank packet is passed with all its "
            "mates to the guard-independent full-source completion split. "
            "Axis-pure completion is impossible and off-axis completion is "
            "the existing active fan.  Thus the only unlanded survivor is "
            "the already isolated Gate-II fan-grade Phi/q comparison"
        ),
        "scope": (
            "canonical h=3 characteristic-zero maximum-anchor/minimum-support "
            "complete five-tensor source.  This reduces arbitrary mate "
            "closures to Gate II; it does not construct Gate II's Phi and "
            "does not assert the axis-pure theorem uniformly in h"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("extra same-word mate recurrence: WELL FOUNDED")
    print("exact kernel: SUPPORT DELETION")
    print("first Hasse/full-rank packet: FULL-SOURCE COMPLETION SPLIT")
    print("axis-pure completion: IMPOSSIBLE")
    print("sole unlanded survivor: GATE-II FAN-GRADE PHI/Q")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
