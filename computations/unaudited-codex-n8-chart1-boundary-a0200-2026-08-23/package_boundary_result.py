#!/usr/bin/env python3
"""Freeze the bounded chart1-boundary gate and exact D12 root interface."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORT = HERE / "results_chart1_boundary_export.json"
ROOT = HERE / "results_d12_root_interface.json"
MANIFEST = HERE / "boundary_gate_p1073741827.manifest.json"
RESULT = HERE / "results_chart1_boundary_a0200.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    export = json.loads(EXPORT.read_text())
    root = json.loads(ROOT.read_text())
    manifest = json.loads(MANIFEST.read_text())
    stage = manifest["stages"][0]
    require(export["input"]["sha256"] == manifest["input"]["file_sha256"]
            and manifest["input"]["logical_sha256"]
            == "8d312aca0f4802264680a45b6c0d02896aee8a171ecdbda5a246cff853fc3ff8",
            "gate input disagrees with exact export")
    require(stage["status"] == "timeout"
            and 300 <= stage["elapsed_seconds"] <= 302
            and stage["returncode"] == -15
            and stage["output"]["bytes"] == 0,
            "bounded timeout ledger changed")
    require(root["logical_sha256"]
            == "75b1ea0c4fe0d5e48b858e3aaaa34f46b94722ca366dc48bae9de146d1c3fe83"
            and root["finite_dual"]["new_violating_column_orbits"] == 130,
            "exact root interface changed")
    payload = {
        "format": "n8-chart1-boundary-a0200-terminal-v1",
        "status": "UNRESOLVED_AFTER_BOUNDED_GATE_EXACT_D12_ROOT_CORE_FROZEN",
        "branch": {
            "chart": 1,
            "normalization": "all 12 cells of three copies of 01|23|45|67 equal 1",
            "boundary": "A_02[0,0]=0",
            "free_source_variables": 239,
            "mixed_generators": 6558,
            "pure_live_inverse_rows": 3,
        },
        "modular_gate": {
            "prime": manifest["input"]["characteristic"],
            "variables_with_inverses": len(manifest["input"]["variables"]),
            "equations": manifest["input"]["polynomial_count"],
            "elapsed_seconds": stage["elapsed_seconds"],
            "status": stage["status"],
            "returncode": stage["returncode"],
            "output_bytes": stage["output"]["bytes"],
            "inference": "NONE",
        },
        "exact_d12_root_core": {
            key: root[key] for key in (
                "boundary_stabilizer_order", "constant_mixed_word_codes",
                "constant_mixed_word_orbits", "root_interface_rows",
                "root_interface_columns", "root_interface_rank",
                "target_rows_on_interface", "target_projection_member",
                "finite_dual",
            )
        },
        "smallest_next_exact_target": (
            "Adjoin the 130 source-labelled D12 column orbits that kill the five-row root "
            "dual, close their row incidence in the order-32 invariant quotient, and rerun "
            "exact/modular span. Do not repeat the 242-variable one-shot gate."
        ),
        "theorem_status": (
            "No member/nonmember/unit result. The full gate timed out. The finite root "
            "projection is nonmember but its five-row dual is explicitly killed by 130 next "
            "cells, so it supplies only a replayable unresolved core."
        ),
        "scope": (
            "First chart-atlas singleton boundary only. Modular timeout and finite projected "
            "nonmembership make no claim about the full homogeneous D12 ideal, saturation, "
            "radical membership, or any other atlas branch."
        ),
        "artifacts_sha256": {
            path.name: sha256(path.read_bytes()).hexdigest()
            for path in (EXPORT, ROOT, MANIFEST)
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
