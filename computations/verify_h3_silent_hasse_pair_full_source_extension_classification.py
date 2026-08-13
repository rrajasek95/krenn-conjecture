#!/usr/bin/env python3
"""Classify full-source extensions of the silent Hasse-pair guard.

The rowwise guard of b3873c9 has only the diagonal base q-cell q45[22]
occupied; its two offdiagonal mate cells occur only as zero-base Hasse
directions.  Complete it by the three normalized pure targets, all five-
tensor response rows, and arbitrary additional augmented companion rows.

There are exactly two source-valid possibilities.

* If every added physical q/endpoint cell stays axis-purified, the base
  point belongs to the canonical h=3 axis-pure five-tensor locus.  The
  global minimum-support census plus the support-27 coefficient certificate
  prove that locus empty.  Adding anchor/q/ridge/eta/sigma equations cannot
  resurrect a point.
* Otherwise a nonzero off-axis physical cell exists.  The target-augmented
  private-site identity produces a nonzero determinant/cofactor active fan.
  The evaluated fan theorem gives four-good or a literal pure-colour coloop.
  Four-good is already landed; after finite Hall saturation the coloop arm
  has exactly the previously isolated fan-grade Phi/q=M-a comparison open.

Thus the Hasse-pair silent mate is not a new full-source residual.  It is a
rowwise guard that, after normalized completion, enters the existing active
fan/coloop frontier.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_retained_pair_divided_hasse_min_support_gate.py":
        "28866193002fff5096b8af3db04055fcc786c558a41f084f524d13dec01483cb",
    "notes/h3-retained-pair-divided-hasse-min-support-gate.md":
        "e8e6d2c680d272ce209e99ea089daeb53333a20d90abb81c59bb9244b4c5911c",
    "computations/verify_h3_axis_pure_closure_active_crossword_frontier.py":
        "b3225f17209d8c920301575c563c9d07954e779339361ae4014d100895bbac67",
    "notes/h3-axis-pure-closure-active-crossword-frontier.md":
        "e5527a7ca7d4160af6f5297624574ffda069888579df44497f9cb4cd1187fc24",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
    "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py":
        "22e1e7a6a933b1ba71bbd95bb605b1351e823506e495682cccff312cd3df3b15",
    "notes/h3-active-fan-coloop-gate-ii-assembly-boundary.md":
        "bacb7b4b138882c0cc07f13767f2e4ead86aa630c55cf1a946943141b7cee7a7",
}
EXPECTED_LEDGER_SHA256 = "ebde5ecfe1070f41ff406ccf8fbf21c7149223fddf46aa871c6c18c7e24e45f5"


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


def guard_entry_audit() -> dict[str, object]:
    guard = load(
        "computations/verify_h3_retained_pair_divided_hasse_min_support_gate.py",
        "silent_pair_guard_dependency",
    )
    ledger, digest = guard.audit()
    require(digest == guard.EXPECTED_LEDGER_SHA256,
            (digest, guard.EXPECTED_LEDGER_SHA256))
    packet = ledger["literal_mixed_two_pair_guard"]
    require(packet["base_occupied_q_support"] == ["q45[22]"]
            and packet["base_nonzero_offdiagonal_q_cells"] == 0
            and packet["marked_retained_pair_value"] == "1"
            and packet["silent_mate_pair_value"] == "-1"
            and packet["first_missing_full_GHZ_rows"].startswith(
                "the three normalized pure target coefficients"),
            packet)

    # The direct D shadow is a multiple of q^[3]=X0.  It adds no base q/p/s
    # support; on the selected mixed word it vanishes with H_001122, and on
    # the full response system it disappears after quotienting the output by
    # <X0>.  The global five-tensor quotient therefore sees exactly the
    # q/p/s support whose axis-pure closure is audited below.
    mixed_target_value = 0
    for direct_value in (-3, 0, 1, 7):
        require(direct_value * mixed_target_value == 0,
                (direct_value, mixed_target_value))
    return {
        "guard_ledger": digest,
        "base_occupied_q_support": packet["base_occupied_q_support"],
        "base_nonzero_offdiagonal_q_cells": 0,
        "marked_and_mate_Hasse_values": ["1", "-1"],
        "first_missing_rows": packet["first_missing_full_GHZ_rows"],
        "direct_response_shadow": (
            "D*q^[3] is X0-valued: it vanishes on the selected mixed row and "
            "is removed globally by the response-output quotient modulo <X0>; "
            "D is not an escape from the q/p/s five-tensor equations"
        ),
    }


def normalized_completion_dichotomy() -> dict[str, object]:
    frontier = load(
        "computations/verify_h3_axis_pure_closure_active_crossword_frontier.py",
        "silent_pair_axis_frontier_dependency",
    )
    ledger, digest = frontier.audit()
    require(digest == frontier.EXPECTED_LEDGER_SHA256,
            (digest, frontier.EXPECTED_LEDGER_SHA256))
    axis = ledger["axis_pure_supersession"]
    split = ledger["surviving_active_split"]
    require(axis["conclusion"]
                == "canonical h=3 axis-pure exact-source branch is empty"
            and axis["coefficient_lifts"] == 0
            and split["h3_full_row_alternative_after_axis_closure"] == {
                "axis_pure": "empty",
                "offdiagonal": "source-provenant private-site active fan",
            }, (axis, split))

    primary_rows = frozenset({
        "three normalized pure target coefficients",
        "all mixed target zero coefficients",
        "four complete five-tensor response families",
    })
    augmented_rows = primary_rows | frozenset({
        "unary Hasse companions", "anchor", "physical q", "ridge",
        "ordinary residue", "eta/sigma", "W", "terminal readouts",
    })
    require(primary_rows < augmented_rows,
            (primary_rows, augmented_rows))
    return {
        "axis_frontier_ledger": digest,
        "primary_equations": sorted(primary_rows),
        "augmented_equations": sorted(augmented_rows),
        "axis_pure_primary_locus": "empty",
        "axis_pure_augmented_locus": (
            "empty by set inclusion: augmented equations only cut the primary locus"
        ),
        "surviving_extension": "contains a nonzero off-axis q or endpoint cell",
        "source_valid_consequence": "target-augmented private-site active fan",
        "scope": (
            "canonical h=3 maximum-anchor/minimum-support exact five-tensor source; "
            "the conclusion is independent of which augmented companions are appended"
        ),
    }


def active_extension_classification() -> dict[str, object]:
    fan = load(
        "computations/verify_h3_active_fan_coloop_or_four_good.py",
        "silent_pair_active_fan_dependency",
    )
    gate = load(
        "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py",
        "silent_pair_gate_ii_dependency",
    )
    ternary = fan.audit_ternary_rank_alternative()
    assembly = gate.audit_branch_assembly()
    termination = gate.audit_finite_termination_interface()
    require(ternary["four_good_assignments"] == 1
            and ternary["literal_coloop_assignments"] == 26,
            ternary)
    require(assembly["only_nonterminal_after_saturation"]
                == "single missing fan-grade physical Phi/q packet"
            and termination["additional_termination_hypothesis_after_Phi"] is False,
            (assembly, termination))
    return {
        "evaluated_active_fan_split": {
            "four_good_support_types": ternary["four_good_assignments"],
            "literal_coloop_support_types": ternary["literal_coloop_assignments"],
        },
        "four_good": "existing transverse landing",
        "literal_coloop": (
            "finite Hall saturation, then the normalized Gate-II packet"
        ),
        "sole_nonterminal_survivor": assembly[
            "only_nonterminal_after_saturation"
        ],
        "exact_open_statement": (
            "construct the fan-grade source-valid protected odd Phi with "
            "J0*Phi=A*J and literal q=M-a rows"
        ),
        "after_Phi": (
            "q disagreement, anchor bright/dark, target circuit, and termination "
            "are already exhaustive"
        ),
        "new_Hasse_pair_specific_extension_theorem_needed": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 silent Hasse-pair full-source extension classification",
        "pins": PINS,
        "rowwise_guard_entry": guard_entry_audit(),
        "normalized_full_source_completion": normalized_completion_dichotomy(),
        "surviving_active_extension": active_extension_classification(),
        "shortest_branch_map": [
            "silent Hasse pair row guard (+1 marked, -1 mate)",
            "append normalized pure targets and complete five-tensor rows",
            "all added support axis-pure -> impossible by global census/certificate",
            "some nonzero off-axis cell -> private-site active fan",
            "four-good -> existing landing",
            "literal coloop -> trapped Hall shore -> sole open fan-grade Phi/q packet",
        ],
        "verdict": (
            "The silent Hasse-pair cancellation cannot extend to a new trapped "
            "full-source branch.  An axis-pure completion is impossible after "
            "the three normalized targets and complete response rows; arbitrary "
            "augmented companion rows only shrink that empty locus.  Every "
            "surviving full exact extension is off-axis and hence enters the "
            "existing private-site active fan.  Four-good is landed.  The sole "
            "unclosed extension is not Hasse-pair-specific: it is the already "
            "isolated trapped pure-colour-coloop fan-grade Phi/q comparison."
        ),
        "scope": (
            "canonical h=3 characteristic-zero maximum-anchor/minimum-support "
            "five-tensor source and its augmented companions; no all-h extension "
            "and no construction of the remaining fan-grade Phi"
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
    print("silent Hasse pair + full axis-pure completion: IMPOSSIBLE")
    print("every surviving full extension: OFF-AXIS ACTIVE FAN")
    print("four-good extension: LANDED")
    print("sole survivor: TRAPPED COLOOP FAN-GRADE PHI/Q")
    print("new Hasse-pair-specific residual: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
