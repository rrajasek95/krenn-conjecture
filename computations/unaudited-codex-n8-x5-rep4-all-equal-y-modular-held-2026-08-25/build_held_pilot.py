#!/usr/bin/env python3
"""Materialize and seal the rep4 F_32003 input; never launch Singular."""
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
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-referee-2026-08-25"
Q_SOURCE = DESIGN / "rep4_guard_minor_tiny_y_Q.sing"
SOURCE = HERE / "rep4_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
RUNNER = HERE / "run_one_lane.py"
PINS = {
    DESIGN / "MANIFEST.sha256": "7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02",
    DESIGN / "generate_design.py": "b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a",
    DESIGN / "results_rep4_contraction_design.json": "7e96874cca1afaaa377aa3001d8e00b73ed4fe9322381ec269c4a46b9144bf0c",
    Q_SOURCE: "d46cdf77b9edafbc17a92ec851badba2db63640ec7324e024a83e29da04e121b",
    REFEREE / "FINAL_MANIFEST.sha256": "185b51b8107d5dcf12e7194a7d806157e0df6a2b6d047cf4adc6c8ac400fa4ae",
    REFEREE / "ONE_CHART_MODULAR_HELD_PLAN.json": "ee484b5a58d63cef6ed60c81760a790b06be363426678f50031f9891fb149203",
    REFEREE / "results_referee.json": "279565e76618b8fa8c4eb08f513f8109a018d23ed1e9fe11acb0489dd82bb863",
    Path("/usr/local/bin/Singular"): "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    Path("/usr/local/bin/gtimeout"): "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}
EXPECTED_SOURCE_SHA = "9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524"
EXPECTED_SOURCE_BYTES = 1_764_288


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def validate(value: dict) -> None:
    assert value["schema"] == "KRENN_X5_REP4_ALL_EQUAL_Y_MODULAR_HELD_V1"
    assert value["status"] == "HELD_PENDING_EXPLICIT_CLEARANCE"
    assert value["lane"] == {
        "representative": "rep4",
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
        "rep4_closed": False,
        "transport_claimed": False,
        "cross_representative_equivalence_used": False,
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
    design = json.loads((DESIGN / "results_rep4_contraction_design.json").read_text())
    referee = json.loads((REFEREE / "results_referee.json").read_text())
    held_referee = json.loads((REFEREE / "ONE_CHART_MODULAR_HELD_PLAN.json").read_text())
    assert design["schema"] == "KRENN_X5_REP4_GUARD_MINOR_CONTRACTION_DESIGN_V1"
    assert design["counts"]["new_variables"] == 91 and design["counts"]["new_generators"] == 6577
    assert design["materialized_inputs"]["y"]["chart"] == [0, 0, 0, 0, "y", 0, 0, 1]
    assert design["materialized_inputs"]["y"]["sha256"] == PINS[Q_SOURCE]
    assert design["scope"]["ideal_runs"] == 0 and not design["scope"]["transport_claimed"]
    assert referee["status"] == "PASS_STRICT_SMALLER_EXACT_DESIGN_NO_RUN_NO_CLOSURE"
    assert referee["counts"] == design["counts"]
    assert referee["support_guard_carrier_regenerated"] is True
    assert referee["ideal_runs"] == 0 and referee["rep4_closed"] is False
    assert held_referee["status"] == "HELD_NOT_RUN_RESOURCE_BLOCKED"
    assert held_referee["p32003_solver_source_expected_sha256"] == EXPECTED_SOURCE_SHA
    assert held_referee["p32003_solver_source_expected_bytes"] == EXPECTED_SOURCE_BYTES
    assert held_referee["chart"] == [0, 0, 0, 0, "y", 0, 0, 1]
    assert held_referee["variables"] == 91 and held_referee["generators"] == 6577
    assert held_referee["solver_launches"] == 0 and held_referee["launch_authorized"] is False
    assert design["source_reconstruction"]["fixed"] == ["03", "16", "27", "45"]
    assert design["source_reconstruction"]["variable"] == ["04", "12", "35", "67"]
    assert design["source_reconstruction"]["added"] == ["06", "15", "17", "23", "26", "46", "47"]
    assert design["source_reconstruction"]["carrier"] == "A06^T*K*[A23^T|A35]"
    assert design["source_reconstruction"]["guard"] == ["A06*A47^T=0", "(I-A17*A26)*A47^T=0"]

    q_program = Q_SOURCE.read_text()
    assert q_program.count("ring r=0,") == 1 and "ring r=32003," not in q_program
    assert q_program.count("quit;") == 1 and "slimgb" not in q_program and "reduce(1" not in q_program
    epilogue = "\n".join([
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ])
    modular = q_program.replace("ring r=0,", "ring r=32003,", 1).replace("quit;", epilogue, 1)
    temporary_source = SOURCE.with_suffix(".sing.tmp")
    temporary_source.write_text(modular)
    os.replace(temporary_source, SOURCE)
    assert sha256(SOURCE) == EXPECTED_SOURCE_SHA
    assert SOURCE.stat().st_size == EXPECTED_SOURCE_BYTES
    assert SOURCE.read_text().count("slimgb(I)") == 1
    assert SOURCE.read_text().count("reduce(1,G)") == 1

    result = {
        "schema": "KRENN_X5_REP4_ALL_EQUAL_Y_MODULAR_HELD_V1",
        "status": "HELD_PENDING_EXPLICIT_CLEARANCE",
        "lane": {
            "representative": "rep4",
            "chart": "all-equal-y/i0/p00/x0/y0/d01",
            "field": "F_32003",
            "variables": 91,
            "generators": 6577,
            "maximum_lane_count": 1,
        },
        "rep4_derivation": {
            "support": design["source_reconstruction"],
            "orientation": design["orientation_audit"],
            "full_x5_digest": design["source_reconstruction"]["full_x5_digest"],
            "independent_referee_regenerated": True,
            "cross_representative_source_or_equivalence_used": False,
        },
        "solver_source_derivation": {
            "exact_Q_source": str(Q_SOURCE.relative_to(ROOT)),
            "exact_Q_source_sha256": PINS[Q_SOURCE],
            "ring_substitution": "unique literal ring r=0, -> ring r=32003,",
            "epilogue": "single slimgb, basis size, reduce(1), remainder, unit/nonunit status, quit",
            "other_polynomial_or_order_changes": 0,
            "expected_hash_from_independent_plan_matched": True,
        },
        "modular_source": {
            "path": SOURCE.name,
            "sha256": sha256(SOURCE),
            "bytes": SOURCE.stat().st_size,
            "ring": "F_32003",
            "slimgb_calls": 1,
            "reduce_one_calls": 1,
        },
        "runner_contract": {
            "path": RUNNER.name,
            "sha256": sha256(RUNNER),
            "launch_command_after_both_clearances": "gtimeout 195 python3 run_one_lane.py",
            "rss_measurement": "direct Darwin libproc process-group census plus per-pid PROC_PID_RUSAGE_INFO_V2",
            "process_isolation": "new process group; TERM then KILL after five seconds",
            "output": "fresh result.json via same-directory temporary plus os.replace",
            "refusal": "missing/malformed exact referee plan, manager clearance, pin, or fresh-output condition aborts before Popen",
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
            "independent_referee_acceptance": "must be byte-identical to pinned rep4 ONE_CHART_MODULAR_HELD_PLAN.json",
            "manager_clearance_schema": "KRENN_X5_REP4_ALL_EQUAL_Y_EXPLICIT_LAUNCH_CLEARANCE_V1",
            "resource_tightening_from_referee_plan": "requested 180/195 replaces referee plan 240/255; 8 GiB unchanged; clearance must bind tighter limits",
            "runner_refuses_without_both": True,
        },
        "interpretation": {
            "unit": "one rep4 mod-p localized-chart diagnostic only; no Q, rep4, family, or conjecture closure",
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
            "rep4_closed": False,
            "transport_claimed": False,
            "cross_representative_equivalence_used": False,
            "mathematical_coverage": False,
        },
    }
    validate(result)
    tests = {
        "launch_injection": hostile(result, lambda value: value["scope"].__setitem__("launched", True)),
        "authorization_injection": hostile(result, lambda value: value["scope"].__setitem__("modular_lanes_authorized", 1)),
        "Q_injection": hostile(result, lambda value: value["scope"].__setitem__("exact_Q_authorized", True)),
        "second_lane_injection": hostile(result, lambda value: value["scope"].__setitem__("second_lane_authorized", True)),
        "cross_rep_injection": hostile(result, lambda value: value["scope"].__setitem__("cross_representative_equivalence_used", True)),
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
