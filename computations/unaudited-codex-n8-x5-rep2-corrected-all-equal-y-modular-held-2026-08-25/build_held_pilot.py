#!/usr/bin/env python3
"""Materialize the single held rep2 all-equal-y F_32003 pilot; never launch it."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"
Q_SOURCE = DESIGN / "rep2_corrected_guard_minor_tiny_y_Q.sing"
PINS = {
    DESIGN / "MANIFEST.sha256": "ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2",
    DESIGN / "generate_design.py": "ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc",
    DESIGN / "results_rep2_corrected_contraction_design.json": "ed37c2e0da8088e08fb6891e60768d98fbbbf031935f752b4e4af280dfe27b26",
    Q_SOURCE: "0285c34fcae56db7dc60830197d645799f5f1c90d84467868436ee453916aedf",
    Path("/usr/local/bin/Singular"): "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    Path("/usr/local/bin/gtimeout"): "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def validate(result):
    assert result["schema"] == "KRENN_X5_REP2_ALL_EQUAL_Y_MODULAR_HELD_V1"
    assert result["status"] == "HELD_PENDING_INDEPENDENT_REFEREE_AND_EXPLICIT_CLEARANCE"
    assert result["lane"] == {
        "chart": "all-equal-y/i0/p00/x0/y0/d01",
        "field": "F_32003",
        "variables": 91,
        "generators": 6577,
        "maximum_lane_count": 1,
    }
    assert result["limits"] == {
        "native_wall_seconds": 180,
        "wrapper_wall_seconds": 195,
        "rss_cap_bytes": 8 * 1024**3,
        "poll_seconds": 0.1,
        "term_then_kill_seconds": 5,
    }
    assert result["scope"] == {
        "launched": False,
        "modular_lanes_authorized": 0,
        "exact_Q_authorized": False,
        "second_lane_authorized": False,
        "automatic_relaunch_authorized": False,
        "mathematical_coverage": False,
    }


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    design = json.loads((DESIGN / "results_rep2_corrected_contraction_design.json").read_text())
    source_meta = design["materialized_inputs"]["y"]
    assert source_meta["chart"] == [0, 0, 0, 0, "y", 0, 0, 1]
    assert source_meta["sha256"] == PINS[Q_SOURCE]
    assert design["counts"]["new_variables"] == 91 and design["counts"]["new_generators"] == 6577
    assert design["scope"]["ideal_runs"] == 0

    q_program = Q_SOURCE.read_text()
    assert q_program.count("ring r=0,") == 1
    assert q_program.count("quit;") == 1
    assert "slimgb" not in q_program and "reduce(1" not in q_program
    epilogue = "\n".join([
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ])
    modular = q_program.replace("ring r=0,", "ring r=32003,", 1).replace("quit;", epilogue, 1)
    assert modular.count("ring r=32003,") == 1 and "ring r=0," not in modular
    assert modular.count("slimgb(I)") == 1 and modular.count("reduce(1,G)") == 1
    assert modular.count("STATUS=UNIT_IDEAL") == 1 and modular.count("STATUS=NONUNIT_OR_UNRESOLVED") == 1
    assert modular.count("quit;") == 1
    source = HERE / "rep2_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
    temporary = source.with_suffix(".sing.tmp")
    temporary.write_text(modular)
    os.replace(temporary, source)

    result = {
        "schema": "KRENN_X5_REP2_ALL_EQUAL_Y_MODULAR_HELD_V1",
        "status": "HELD_PENDING_INDEPENDENT_REFEREE_AND_EXPLICIT_CLEARANCE",
        "lane": {
            "chart": "all-equal-y/i0/p00/x0/y0/d01",
            "field": "F_32003",
            "variables": 91,
            "generators": 6577,
            "maximum_lane_count": 1,
        },
        "derivation": {
            "exact_Q_source": str(Q_SOURCE.relative_to(ROOT)),
            "exact_Q_source_sha256": PINS[Q_SOURCE],
            "ring_substitution": "unique literal ring r=0, -> ring r=32003,",
            "epilogue": [
                "G=slimgb(I)",
                "remainder=reduce(1,G)",
                "print basis size, literal remainder, and fail-closed UNIT/NONUNIT status",
            ],
            "other_polynomial_or_order_changes": 0,
        },
        "modular_source": {
            "path": source.name,
            "sha256": sha256(source),
            "bytes": source.stat().st_size,
            "slimgb_calls": 1,
            "reduce_one_calls": 1,
        },
        "runner_contract": {
            "path": "run_one_lane.py",
            "sha256": sha256(HERE / "run_one_lane.py"),
            "launch_command_after_both_clearances": "gtimeout 195 python3 run_one_lane.py",
            "rss_measurement": "direct /usr/lib/libproc.dylib proc_pid_rusage on the live Singular child",
            "process_isolation": "new process group; TERM then KILL after five seconds",
            "output": "fresh result.json via same-directory temporary plus os.replace",
            "stdout_stderr": "captured verbatim in atomic result",
            "refusal": "missing/malformed referee acceptance, launch clearance, pin, or pre-existing result aborts before Popen",
        },
        "limits": {
            "native_wall_seconds": 180,
            "wrapper_wall_seconds": 195,
            "rss_cap_bytes": 8 * 1024**3,
            "poll_seconds": 0.1,
            "term_then_kill_seconds": 5,
        },
        "clearance_contract": {
            "required_files_absent_at_seal": ["independent_referee_acceptance.json", "launch_clearance.json"],
            "referee_must_pin": ["held MANIFEST.sha256 hash", "modular source hash", "runner hash", "Singular hash", "91/6577 counts", "one diagnostic lane only"],
            "manager_clearance_must_pin": ["held MANIFEST.sha256 hash", "referee acceptance artifact hash", "one explicit launch", "no Q/second/relaunch"],
            "runner_refuses_without_both": True,
        },
        "interpretation": {
            "unit": "one mod-p localized-chart diagnostic only; no characteristic-zero, representative, family, or conjecture closure",
            "nonunit": "diagnostic only; no closure",
            "timeout_rss_process_schema_failure": "fail closed with zero mathematical coverage",
        },
        "pins": {str(path if path.is_absolute() and str(path).startswith("/usr") else path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {
            "launched": False,
            "modular_lanes_authorized": 0,
            "exact_Q_authorized": False,
            "second_lane_authorized": False,
            "automatic_relaunch_authorized": False,
            "mathematical_coverage": False,
        },
    }
    validate(result)
    tests = {
        "launch_injection": hostile(result, lambda value: value["scope"].__setitem__("launched", True)),
        "authorization_injection": hostile(result, lambda value: value["scope"].__setitem__("modular_lanes_authorized", 1)),
        "second_lane_injection": hostile(result, lambda value: value["scope"].__setitem__("second_lane_authorized", True)),
        "Q_injection": hostile(result, lambda value: value["scope"].__setitem__("exact_Q_authorized", True)),
        "wall_widening": hostile(result, lambda value: value["limits"].__setitem__("native_wall_seconds", 181)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    output = HERE / "held_pilot.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({"status": result["status"], "source_sha256": result["modular_source"]["sha256"], "launched": False}, sort_keys=True))


if __name__ == "__main__":
    main()
