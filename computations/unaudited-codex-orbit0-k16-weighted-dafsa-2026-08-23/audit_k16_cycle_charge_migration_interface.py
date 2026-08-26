#!/usr/bin/env python3
"""Audit whether the frozen K14->K16 provider exposes the full charge stream.

This is deliberately an interface audit.  It does not reconstruct the missing
K17..K24 residual, because doing so would replace the frozen reduction by a new
large expansion.  The exact conclusion is therefore a blocker plus the scalar
charge forced by conservation.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COLLECT = ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/collect_orbit0_k16_literal_residual.py"
COLLECT_RESULT = ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json"
TELESCOPE = ROOT / "computations/unaudited-codex-n8-orbit0-t2-graded-2026-08-20/results_orbit0_chart_target_anchor_telescoping.json"
CUTOFF8 = ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/results_orbit0_cutoff8_sparse_full_certificate.json"
CYCLE = HERE / "results_k16_cycle_partition_quotient.json"
OUT = HERE / "results_k16_cycle_charge_migration_interface.json"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def file_sha(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def build() -> dict:
    collect_source = COLLECT.read_text()
    telescope = json.loads(TELESCOPE.read_text())
    cutoff8 = json.loads(CUTOFF8.read_text())
    cycle = json.loads(CYCLE.read_text())

    # Load-bearing source guard: the frozen reducer deliberately retains only
    # the K2 terms of a mixed word after its K0 singleton pivot.
    k2_filter = "tails = tuple(term for term in terms if F.row_k_degree(term) == 2)"
    require(k2_filter in collect_source, "frozen reducer no longer has the audited K2-only tail filter")
    require("fully coefficient-collected irreducible K16 residual" in collect_source,
            "frozen reducer output scope changed")

    profiles = telescope["anchor_word_K_profiles"]
    require(len(profiles) == 3, profiles)
    expected_profile = {"0": 1, "2": 12, "3": 32, "4": 60}
    require(all(profile == expected_profile for profile in profiles), profiles)
    require("leading K14 residual is -R8'*E0_2*E1_2*E2_2" in telescope["consequence"],
            telescope["consequence"])
    require(cutoff8["cutoff"] == 8 and cutoff8["nonzero_source_terms"] == 236,
            (cutoff8["cutoff"], cutoff8["nonzero_source_terms"]))

    k16_charge = cycle["exact_target_pairing"]
    structured_charge = cycle["original_structured_aT_pairing"]
    require(k16_charge == -311_258_112, k16_charge)
    require(structured_charge == 0, structured_charge)
    omitted_charge = structured_charge - k16_charge

    result = {
        "schema": "orbit0-k16-cycle-charge-migration-interface-v1",
        "status": "BLOCKED_MISSING_COMPLETE_FILTERED_RESIDUAL_STREAM",
        "audited_available_interface": {
            "cutoff8_source_certificate_nonzero_terms": cutoff8["nonzero_source_terms"],
            "full_mixed_generator_K_profile_per_colour_factor": expected_profile,
            "frozen_factored_leading_input": "-R8prime*E0_2*E1_2*E2_2 at K14",
            "frozen_reducer_retained_tail_K_degrees": [2],
            "frozen_reducer_serialized_output_K_degrees": [16],
            "frozen_K16_cycle_charge": k16_charge,
            "structured_a_times_T_cycle_charge": structured_charge,
        },
        "forced_conservation_consequence": {
            "omitted_K17_through_K24_total_cycle_charge": omitted_charge,
            "proof": "lambda(a*T)=0 and lambda(K16 residual)=-311258112",
            "degree_distribution": "not determined by the frozen interface",
        },
        "exact_missing_interface": [
            "a factorized iterator for the full R=T-S layers K8..K12 from the cutoff-8 certificate",
            "the full E0*E1*E2 packet retaining each factor's K2, K3, and K4 terms",
            "the exact chosen K14 singleton-pivot averaging with every K2/K3/K4 tail",
            "a collected/canonical residual stream by K-degree K16..K24 with orbit-mass provenance",
        ],
        "requested_49_dimensional_normal_form": {
            "status": "BLOCKED_BY_SAME_MISSING_STREAM",
            "reason": "the 49 quotient coordinates can be accumulated cheaply only after complete residual terms by K-degree are exposed",
            "known_cycle_profile_rank": 271,
            "known_cycle_partition_coordinates": cycle["cycle_partition_coordinates"],
        },
        "scope_guard": (
            "The omitted total scalar charge is exact, but assigning it among K17..K24 or "
            "computing the 49-dimensional normal-form vector would require a new broad reconstruction; "
            "neither is present in the frozen K14->K16 provider."
        ),
        "inputs": {
            "collector_source": str(COLLECT.relative_to(ROOT)),
            "collector_source_sha256": file_sha(COLLECT),
            "collector_result": str(COLLECT_RESULT.relative_to(ROOT)),
            "collector_result_sha256": file_sha(COLLECT_RESULT),
            "telescoping_result": str(TELESCOPE.relative_to(ROOT)),
            "telescoping_result_sha256": file_sha(TELESCOPE),
            "cutoff8_certificate": str(CUTOFF8.relative_to(ROOT)),
            "cutoff8_certificate_sha256": file_sha(CUTOFF8),
            "cycle_quotient_result": str(CYCLE.relative_to(ROOT)),
            "cycle_quotient_result_sha256": file_sha(CYCLE),
        },
    }
    logical = dict(result)
    result["logical_sha256"] = sha256(
        json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return result


def main() -> None:
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--verify" in sys.argv:
        require(OUT.read_text() == payload, "stored result differs from exact replay")
    else:
        OUT.write_text(payload)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
