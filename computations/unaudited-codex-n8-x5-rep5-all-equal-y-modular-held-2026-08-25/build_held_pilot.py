#!/usr/bin/env python3
"""Seal the source-faithful rep5 modular pilot contract without launching it."""
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
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25"
ORIGINAL_SOURCE = DESIGN / "rep5_guard_minor_tiny_y_p32003.sing"
SOURCE = HERE / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
RUNNER = HERE / "run_one_lane.py"
PINS = {
    DESIGN / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    DESIGN / "generate_design.py": "3844eadf4a9e21c2feb012cbd684c22ca7611f4d22f87659e19952d0381614f4",
    DESIGN / "results_rep5_contraction_design.json": "b2ba095f4f702ac2138cb40d45b7721a8df9b338900282020e83b791264df59b",
    ORIGINAL_SOURCE: "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
    REFEREE / "FINAL_MANIFEST.sha256": "ad86daeae93aaa154ef9ade124c719c8e683c3ae1b95130f948a2d90c0fc495a",
    REFEREE / "HELD_MODULAR_PILOT.json": "0df5f63b08cb3f601a5d77d22f07293e557f6dae6b7e727849916d943e5b70c7",
    REFEREE / "results_independent_referee.json": "451159d198b0188ee2780c7468797b6a438d04e041212e36a0cc2b1469b73292",
    Path("/usr/local/bin/Singular"): "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    Path("/usr/local/bin/gtimeout"): "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def validate(value: dict) -> None:
    assert value["schema"] == "KRENN_X5_REP5_ALL_EQUAL_Y_MODULAR_HELD_V1"
    assert value["status"] == "HELD_PENDING_EXPLICIT_CLEARANCE"
    assert value["lane"] == {
        "representative": "rep5",
        "chart": "all-equal-y/i0/p00/x0/y0/d01",
        "field": "F_32003",
        "variables": 91,
        "generators": 6577,
        "maximum_lane_count": 1,
    }
    assert value["limits"] == {
        "native_wall_seconds": 180,
        "wrapper_wall_seconds": 195,
        "rss_cap_bytes": 8 * 1024**3,
        "poll_seconds": 0.1,
        "term_then_kill_seconds": 5,
    }
    assert value["scope"] == {
        "launched": False,
        "ideal_runs": 0,
        "modular_lanes_authorized": 0,
        "exact_Q_authorized": False,
        "second_lane_authorized": False,
        "automatic_relaunch_authorized": False,
        "rep5_closed": False,
        "transport_claimed": False,
        "rep2_equivalence_used": False,
        "mathematical_coverage": False,
    }


def hostile(value: dict, mutation) -> bool:
    candidate = copy.deepcopy(value)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main() -> None:
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    assert SOURCE.read_bytes() == ORIGINAL_SOURCE.read_bytes()
    assert sha256(SOURCE) == PINS[ORIGINAL_SOURCE]

    design = json.loads((DESIGN / "results_rep5_contraction_design.json").read_text())
    referee = json.loads((REFEREE / "results_independent_referee.json").read_text())
    held_referee = json.loads((REFEREE / "HELD_MODULAR_PILOT.json").read_text())
    assert design["schema"] == "KRENN_X5_REP5_GUARD_MINOR_CONTRACTION_DESIGN_V1"
    assert design["counts"]["new_variables"] == 91
    assert design["counts"]["new_generators"] == 6577
    assert design["materialized_inputs"]["y"]["chart"] == [0, 0, 0, 0, "y", 0, 0, 1]
    assert design["materialized_inputs"]["y"]["sha256"] == PINS[ORIGINAL_SOURCE]
    assert design["scope"]["ideal_runs"] == 0 and not design["scope"]["transport_claimed"]
    assert referee["status"] == "PASS_INDEPENDENT_EXACT_DESIGN_NO_IDEAL_RUN"
    assert referee["counts"] == design["counts"]
    assert referee["scope"]["ideal_runs"] == 0 and not referee["scope"]["transport_claimed"]
    assert held_referee["status"] == "HELD_NOT_LAUNCHED"
    assert held_referee["source"]["sha256"] == PINS[ORIGINAL_SOURCE]
    assert held_referee["source"]["variables"] == 91 and held_referee["source"]["generators"] == 6577
    assert referee["support"] == {
        "fixed": ["03", "16", "27", "45"],
        "variable": ["04", "12", "35", "67"],
        "added": ["06", "15", "17", "24", "26", "36", "37"],
        "perfect_matchings_total": 105,
        "supported": 12,
        "supported_matching_sha256": "ca7dc986266a3d3a9702b6d4bfff722094374666aa1f11adba83348cc2513f9c",
    }
    assert referee["carrier"]["factorization"] == "A06^T*K*[A35|A37]"
    assert referee["orientation"]["guards"] == ["A06*A37^T=0", "(I-A17*A26)*A37^T=0"]

    program = SOURCE.read_text()
    assert program.count("ring r=32003,") == 1 and "ring r=0," not in program
    for token in (
        "ideal G=slimgb(I);", "poly remainder=reduce(1,G);",
        "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED",
        "INPUT_VARIABLES=", "INPUT_GENERATORS=", "quit;",
    ):
        assert program.count(token) == 1, token

    result = {
        "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_MODULAR_HELD_V1",
        "status": "HELD_PENDING_EXPLICIT_CLEARANCE",
        "lane": {
            "representative": "rep5",
            "chart": "all-equal-y/i0/p00/x0/y0/d01",
            "field": "F_32003",
            "variables": 91,
            "generators": 6577,
            "maximum_lane_count": 1,
        },
        "rep5_derivation": {
            "source_support": referee["support"],
            "guard_orientation": referee["orientation"],
            "carrier": referee["carrier"],
            "exact_source_byte_match": True,
            "rep2_source_or_equivalence_used": False,
        },
        "modular_source": {
            "path": SOURCE.name,
            "sha256": sha256(SOURCE),
            "bytes": SOURCE.stat().st_size,
            "ring": "F_32003",
            "slimgb_calls": 1,
            "reduce_one_calls": 1,
        },
        "solver_epilogue": {
            "basis": "ideal G=slimgb(I)",
            "unit_test": "poly remainder=reduce(1,G)",
            "terminal_statuses": ["STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED"],
            "exactly_one_quit": True,
        },
        "runner_contract": {
            "path": RUNNER.name,
            "sha256": sha256(RUNNER),
            "launch_command_after_both_clearances": "gtimeout 195 python3 run_one_lane.py",
            "rss_measurement": "direct Darwin libproc PROC_PIDTASKINFO on the Singular child",
            "process_isolation": "new process group; TERM then KILL after five seconds",
            "output": "fresh result.json via same-directory temporary plus os.replace",
            "refusal": "missing/malformed exact referee acceptance, launch clearance, pin, or fresh-output condition aborts before Popen",
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
            "independent_referee_acceptance": "must be byte-identical to pinned rep5 HELD_MODULAR_PILOT.json",
            "manager_clearance_schema": "KRENN_X5_REP5_ALL_EQUAL_Y_EXPLICIT_LAUNCH_CLEARANCE_V1",
            "manager_must_pin": ["held manifest", "referee final manifest", "referee acceptance", "source", "runner", "Singular", "gtimeout", "180/195/8GiB", "one lane", "no Q/second/relaunch"],
            "wrapper_difference_from_referee_plan": "outer watchdog 195s instead of referee's 190s; native Singular cap remains exactly 180s; explicit manager clearance must bind 195s",
            "runner_refuses_without_both": True,
        },
        "interpretation": {
            "unit": "one rep5 mod-p localized-chart diagnostic only; no Q, rep5, family, or conjecture closure",
            "nonunit": "diagnostic only; no closure",
            "timeout_rss_process_schema_failure": "fail closed with zero mathematical coverage",
        },
        "pins": {str(path if str(path).startswith("/usr/") else path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {
            "launched": False,
            "ideal_runs": 0,
            "modular_lanes_authorized": 0,
            "exact_Q_authorized": False,
            "second_lane_authorized": False,
            "automatic_relaunch_authorized": False,
            "rep5_closed": False,
            "transport_claimed": False,
            "rep2_equivalence_used": False,
            "mathematical_coverage": False,
        },
    }
    validate(result)
    tests = {
        "launch_injection": hostile(result, lambda value: value["scope"].__setitem__("launched", True)),
        "authorization_injection": hostile(result, lambda value: value["scope"].__setitem__("modular_lanes_authorized", 1)),
        "Q_injection": hostile(result, lambda value: value["scope"].__setitem__("exact_Q_authorized", True)),
        "second_lane_injection": hostile(result, lambda value: value["scope"].__setitem__("second_lane_authorized", True)),
        "rep2_transport_injection": hostile(result, lambda value: value["scope"].__setitem__("rep2_equivalence_used", True)),
        "wall_widening": hostile(result, lambda value: value["limits"].__setitem__("native_wall_seconds", 181)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    output = HERE / "held_pilot.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({"status": result["status"], "source_sha256": sha256(SOURCE), "launched": False}, sort_keys=True))


if __name__ == "__main__":
    main()
