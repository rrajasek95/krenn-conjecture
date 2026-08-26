#!/usr/bin/env python3
"""Static fail-closed audit of the held D11 recovery design."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT_PACKAGE = REPO / "computations/unaudited-codex-n8-x5-four-d11-seeded-support-repair-2026-08-25"
PARENT = PARENT_PACKAGE / "src/main.rs"
SOURCE = HERE / "src/main.rs"
PINS = {
    "parent_source": "57127904ab633bb5e9c58af1e66fe41cfae169659a32220a4460c998c54ef66d",
    "source": "521e8f503f900c15b9b0668f60095fae120b6f47e44666076179fbc2058d9120",
    "binary": "a2ce6120a4d04683ef4238ef3ec2b4733ad1c2df186e5a838f740fd524f4d5f8",
    "watchdog": "4418ffadb5cc45ec4bdec1427850810d66438d7d09679520eab7d5fba142291e",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "selected": "3eab0267866718ca21259e9daffac6f15161438b6348a25fe3de3ded08aaf10a",
    "dual": "4eb560af124b6f046ae67b447988c0b0713822da852f2a1f6fa0307f6ca390b0",
}

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    assert sha(PARENT) == PINS["parent_source"] and sha(SOURCE) == PINS["source"]
    assert sha(HERE / "x5_d11_triangle_recovery") == PINS["binary"]
    assert sha(HERE / "watchdog12_600_recovery.py") == PINS["watchdog"]
    provider = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
    selected = PARENT_PACKAGE / "seed_triangle_endpoint_colour_p1073741827/selected.tsv"
    dual = PARENT_PACKAGE / "seed_triangle_endpoint_colour_p1073741827/transported_d10_dual.tsv"
    assert sha(provider) == PINS["provider"] and sha(selected) == PINS["selected"] and sha(dual) == PINS["dual"]
    parent, child = PARENT.read_text(), SOURCE.read_text()
    expected = parent.replace("wall_seconds > 175", "wall_seconds > 590", 1)
    expected = expected.replace("    let mut rounds = Vec::<RoundRecord>::new();\n", "    let mut rounds = Vec::<RoundRecord>::new();\n    let mut last_checkpoint_seconds = 0u64;\n", 1)
    marker = """        rounds.push(RoundRecord {
            round,
            columns_before,
            incident_columns_checked: scan.incident_checked,
            new_violations: scan.violations.len(),
            columns_after: selected.len(),
            support_after,
            incidence_seconds,
            solve_seconds,
        });
"""
    addition = marker + """        let checkpoint_seconds = started.elapsed().as_secs();
        if candidate.is_some() && checkpoint_seconds >= last_checkpoint_seconds + 30 {
            // Dual first makes every observable pair restart-safe: if killed
            // between the two renames, the newer dual still annihilates the
            // older selected subset; main revalidates the pair on resume.
            write_dual(&config.dual, config.prime, candidate.as_ref());
            write_selected(&config.selected, &provider, &selected);
            last_checkpoint_seconds = checkpoint_seconds;
        }
"""
    assert marker in expected
    expected = expected.replace(marker, addition, 1)
    assert child == expected
    contract = json.loads((HERE / "LAUNCH_CONTRACT.json").read_text())
    assert contract["status"] == "HOLD_PENDING_EXCLUSIVE_SLOT_CLEARANCE"
    assert contract["native_wall_seconds"] == 590 and contract["wrapper_wall_seconds"] == 600
    assert contract["rss_gib"] == 12 and contract["column_cap"] == 500000
    assert not (HERE / "CLEARANCE.json").exists()
    assert not (HERE / "production_p1073741827_triangle_endpoint_colour").exists()
    held = subprocess.run([sys.executable, str(HERE / "run_recovery.py")], cwd=HERE, text=True, capture_output=True, check=False)
    assert held.returncode != 0 and "HOLD: missing explicit exclusive-slot" in held.stderr
    assert not (HERE / "production_p1073741827_triangle_endpoint_colour").exists()
    result = {"schema": "KRENN_X5_D11_TRIANGLE_RECOVERY_DESIGN_AUDIT_V1", "status": "PASS_HELD",
              "source_diff": {"math_or_provider_changes": 0, "wall_guard_changes": 1,
                              "checkpoint_instrumentation_blocks": 2},
              "branch": "triangle_endpoint_colour", "prime": 1073741827,
              "native_wall_seconds": 590, "wrapper_wall_seconds": 600, "rss_gib": 12,
              "column_cap": 500000, "checkpoint_interval_seconds": 30,
              "restart_safety": "dual rename precedes selected rename; resume performs full selected-pair verification",
              "prior_peak_rss_kib": 8397664, "prior_elapsed_seconds": 174.594452,
              "linear_rss_projection_to_12g_seconds": 261.8,
              "projection_warning": "linear projection is diagnostic only; terminality is not projected",
              "clearance_required": True, "clearance_present": False,
              "arithmetic_launched": False, "second_prime_launched": False, "degree_twelve_launched": False}
    atomic(HERE / "results_design_audit.json", result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
