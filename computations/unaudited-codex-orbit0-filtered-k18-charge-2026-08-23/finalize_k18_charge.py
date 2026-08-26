#!/usr/bin/env python3
"""Freeze and replay the exact charge-only K18 computation."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = HERE / "results_k18_charge_raw.json"
OUT = HERE / "results_k18_charge.json"
SOURCES = [
    HERE / "run_k18_charge.rs",
    HERE / "export_k18_k4.py",
    HERE / "filtered_k18_k4.bin",
    ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin",
    ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin",
    ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin",
    ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin",
    ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/frozen_k14_k2_response.bin",
]

def frac(n, d):
    q = Fraction(n, d)
    return {"numerator": q.numerator, "denominator": q.denominator,
            "text": str(q)}

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def main(write=False):
    raw = json.loads(RAW.read_text())
    scale = raw["scale"]
    names = ("direct", "K14_K4", "K15_K3", "K16_K2")
    expected_full = {
        "direct": 152_251_200,
        "K14_K4": 397_156_800,
        "K15_K3": 1_789_890_560,
        "K16_K2": 1_559_270_244,
    }
    components = {}
    for name in names:
        full_n, irr_n, full_q, irr_q = raw[name]
        assert full_n == expected_full[name]
        assert 0 <= irr_n <= full_n
        components[name] = {
            "full_compact_occurrences": full_n,
            "K18_irreducible_occurrences": irr_n,
            "full_charge_scaled": full_q,
            "K18_irreducible_charge_scaled": irr_q,
            "full_charge": frac(full_q, scale),
            "K18_irreducible_charge": frac(irr_q, scale),
        }
    full_q = sum(raw[name][2] for name in names)
    irr_q = sum(raw[name][3] for name in names)
    result = {
        "status": "PASS_EXACT_K18_CHARGE_ONLY_NO_ROW_COLLECTION",
        "scale": scale,
        "components": components,
        "total": {
            "full_compact_occurrences": sum(raw[n][0] for n in names),
            "K18_irreducible_occurrences": sum(raw[n][1] for n in names),
            "full_charge_scaled": full_q,
            "K18_irreducible_charge_scaled": irr_q,
            "full_charge": frac(full_q, scale),
            "K18_irreducible_charge": frac(irr_q, scale),
        },
        "cache": {
            "entries_across_eight_thread_local_maps": raw["cache_entries"],
            "key": "(four-path/closed-cycle profile, anchor signature, pivot, tail degree)",
            "soundness": (
                "The profile retains the labelled eight cut endpoints and every path "
                "length plus closed-cycle multiset, so attaching a fixed pivot tail "
                "determines the child cycle partition.  The anchor signature separately "
                "determines K18 pivotability."
            ),
        },
        "elapsed_seconds": raw["elapsed_seconds"],
        "K17_guard": "Every pivot tail raises K by at least 2, hence K17 first feeds K19, not K18.",
        "scope": (
            "Exact value of the frozen 77-cycle functional before and after removing "
            "K18-pivotable children, componentwise. This is a charge computation only; "
            "it is not a K18 residual collection or ideal-membership verdict."
        ),
        "compact_level_guard": (
            "The 44,342,881 K15 value is a collected H-orbit pivot-use count, while "
            "55,934,080 is the precollection compact source-pair pivot-use count used "
            "by this source-linear stream. Its 1,789,890,560 K3 evaluations are exact "
            "for this implementation, but cross-component occurrence totals mix compact "
            "levels and are engineering counts, not a common literal census."
        ),
        "hardening_guard": (
            "The run source did not assert the K15 division remainder or parse two aux "
            "magic strings; S is the audited LCM and all input/source hashes are pinned. "
            "This is replay hardening, not a failure of the exact charge arithmetic."
        ),
        "pinned": {str(p.relative_to(ROOT)): digest(p) for p in SOURCES},
    }
    logical = digest_bytes = sha256(json.dumps(result, sort_keys=True,
                                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "total": result["total"],
                      "logical_sha256": logical}, indent=2))

if __name__ == "__main__":
    import sys
    main("--write-results" in sys.argv)
