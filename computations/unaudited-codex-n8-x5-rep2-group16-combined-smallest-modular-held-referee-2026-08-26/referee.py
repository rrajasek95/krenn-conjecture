#!/usr/bin/env python3
"""Independent zero-run referee for the rep2 group16 combined modular held lane."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import re
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions are load-bearing")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELD = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-held-2026-08-26"
TIMEOUT = ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-terminal-referee-2026-08-26"
TORUS = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26"
COMPARE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26"
GUARD = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-isomorphism-guard-pivot-design-2026-08-26"

PINS = {
    HELD / "MANIFEST.sha256": "6842f4f8c70570772d2b3602682b103af4953c2cec67b88510f2df72aeef8fa8",
    HELD / "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing": "66bdb9277c9bff605e0d8a808ca65beb5967afaaf8ae494193286a60338355c6",
    HELD / "run_one_lane.py": "cec7089a43ddb82dc5f9654b5338a0dcc21f30fe2ace5640b8421dd7ef6ce656",
    HELD / "held_pilot.json": "d6e6ef59581e3cd208ae6364858a8b0a434dc366344f249317372e7f082afbeb",
    HELD / "source_derivation.json": "1e08d3d13f7c069a3991e6a2871838c7960ba31dc2a923ac673270207fa297ad",
    HELD / "refusal_contract.json": "80314e0ee1f8a7d511d627126d308c6ba19d1a5f1976d3871bde274ea2ece050",
    HELD / "independent_referee_acceptance.schema.json": "130da27e95c239f53577d280374a3f457ea52c2f538fb8d3de7e5670c41fb786",
    HELD / "launch_clearance.schema.json": "7438ed97b4a730d24df852658afda36f76a996226b65dce0b4aabd95583580fa",
    TIMEOUT / "FINAL_MANIFEST.sha256": "066347c8af9a579b8f09d1c1eebf0197e819753da839f30708616287c4336196",
    TORUS / "MANIFEST.sha256": "1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282",
    COMPARE / "MANIFEST.sha256": "1a2dcba289d5f31e39be48c4f98ff44a6b0c6891841fd345df52f06abfd5525a",
    COMPARE / "results_referee_comparison.json": "46adce91fb2d361cb506046c706e4e849ecc0e4bb23b2df7193ed04073ebd9c7",
    COMPARE / "rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing": "2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339",
    GUARD / "MANIFEST.sha256": "6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def replay(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(None, 1)
        target = (path.parent / relative.strip()).resolve()
        assert target.is_file() and sha(target) == digest, (target, digest)
        count += 1
    return count


for path, digest in PINS.items():
    assert sha(path) == digest, (path, sha(path), digest)
held_manifest_lines = replay(HELD / "MANIFEST.sha256")

q_path = COMPARE / "rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing"
p_path = HELD / "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing"
q_bytes, p_bytes = q_path.read_bytes(), p_path.read_bytes()
assert q_bytes.count(b"ring r=0,(") == p_bytes.count(b"ring r=32003,(") == 1
assert q_bytes.replace(b"ring r=0,(", b"ring r=32003,(", 1) == p_bytes
assert p_bytes.replace(b"ring r=32003,(", b"ring r=0,(", 1) == q_bytes
epilogue = (
    b"ideal G=slimgb(I);\nprint(\"GROEBNER_SIZE=\"+string(size(G)));\n"
    b"poly remainder=reduce(1,G);\nprint(\"UNIT_REMAINDER=\"+string(remainder));\n"
    b"if (remainder==0) { print(\"STATUS=UNIT_IDEAL\"); } else { print(\"STATUS=NONUNIT_OR_UNRESOLVED\"); }\nquit;\n"
)
assert q_bytes.endswith(epilogue) and p_bytes.endswith(epilogue)

text = q_bytes.decode()
variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
depth = 0
generators = 1
for character in body:
    if character == "(":
        depth += 1
    elif character == ")":
        depth -= 1
    elif character == "," and depth == 0:
        generators += 1
    assert depth >= 0
assert depth == 0 and len(variables) == 67 and generators == 6574

held = json.loads((HELD / "held_pilot.json").read_text())
derivation = json.loads((HELD / "source_derivation.json").read_text())
refusal = json.loads((HELD / "refusal_contract.json").read_text())
comparison = json.loads((COMPARE / "results_referee_comparison.json").read_text())
assert held["status"] == "HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE"
assert held["scope"] == {
    "attempts": 0, "group16_closed": False, "mathematical_coverage": False,
    "prior_timeout_reused": False, "results": 0, "solver_runs": 0,
}
assert held["chart"] == {
    "guard_pivot_k": 0, "logical_scope": "V(A67,A12) intersect D(b0)",
    "single_chart_closes_group16": False, "torus_stratum": "A67=A12=0",
}
assert derivation["status"] == "PASS_SOLE_Q_TO_P32003_RING_SUBSTITUTION_ZERO_RUN"
assert derivation["transformation"] == {
    "inverse_byte_replay": True, "new_literal": "ring r=32003,(",
    "non_ring_bytes_identical": True, "occurrences_replaced": 1,
    "old_literal": "ring r=0,(", "strong_solver_epilogue_preserved": True,
}
assert refusal["status"] == "HELD_FAIL_CLOSED_ZERO_RUN" and refusal["solver_runs"] == 0
assert refusal["present_acceptance_files"] == refusal["present_clearance_files"] == 0
assert comparison["exact_comparison"]["intersection_chart_count"] == 57
assert comparison["exact_comparison"]["intersection_histogram"] == {
    "67_variables_6574_generators": 3,
    "75_variables_6574_generators": 27,
    "84_variables_6574_generators": 27,
}
assert comparison["exact_comparison"]["single_chart_closes_group16"] is False
assert comparison["guard_pivot_audit"]["cover"] == "D(b0) union D(b1) union D(b2)"

for forbidden in (
    "independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json",
    "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json",
    "RUN_EXCLUSIVE.lock",
):
    assert not (HELD / forbidden).exists(), forbidden
assert not list(HELD.glob("*.tmp")) and not list(HELD.rglob("__pycache__"))

runner_path = HELD / "run_one_lane.py"
runner_text = runner_path.read_text()
tree = ast.parse(runner_text)
assert tree and "/bin/ps" not in runner_text and "subprocess.run" not in runner_text
for literal in (
    "NATIVE_WALL = 240", "WRAPPER_WALL = 255", "RSS_CAP = 8 * 1024**3",
    "proc_listallpids", "proc_pidpath", "proc_listpgrppids", "proc_pid_rusage",
    "fresh_process_census()", "process_group_rss_bytes(process.pid, True)",
    'exclusive_json(HERE / "RUN_EXCLUSIVE.lock"', 'exclusive_json(HERE / "ATTEMPT.json"',
    'atomic_json(HERE / "result.json", result)', '"GROEBNER_SIZE=1"',
    '"UNIT_REMAINDER=0"', '"STATUS=UNIT_IDEAL"',
    '"mathematical_coverage": False', '"prior_timeout_reused": False',
    '"automatic_relaunch": False',
):
    assert literal in runner_text, literal
assert "start_new_session=True" in runner_text and "os.killpg" in runner_text
assert "os.O_EXCL" in runner_text and "MAX_CLEARANCE_LIFETIME_SECONDS = 600" in runner_text

acceptance_schema = json.loads((HELD / "independent_referee_acceptance.schema.json").read_text())
clearance_schema = json.loads((HELD / "launch_clearance.schema.json").read_text())
for schema in (acceptance_schema, clearance_schema):
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(schema["properties"])
assert acceptance_schema["properties"]["maximum_lane_count"]["const"] == 1
assert acceptance_schema["properties"]["exact_Q_authorized"]["const"] is False
assert acceptance_schema["properties"]["other_chart_authorized"]["const"] is False
assert acceptance_schema["properties"]["automatic_relaunch_authorized"]["const"] is False
assert clearance_schema["properties"]["native_wall_seconds"]["const"] == 240
assert clearance_schema["properties"]["wrapper_wall_seconds"]["const"] == 255
assert clearance_schema["properties"]["rss_cap_bytes"]["const"] == 8589934592


def contract(value: dict) -> None:
    assert value["held_manifest_sha256"] == PINS[HELD / "MANIFEST.sha256"]
    assert value["source_sha256"] == PINS[p_path]
    assert value["runner_sha256"] == PINS[runner_path]
    assert value["variables"] == 67 and value["generators"] == 6574
    assert value["scope"] == "V(A67,A12) intersect D(b0) only"
    assert value["intersection_chart_count"] == 57
    assert value["maximum_lane_count"] == 1
    assert value["solver_runs"] == 0 and value["attempts"] == 0
    assert value["group16_closed"] is value["mathematical_coverage"] is False
    assert value["exact_Q_authorized"] is value["other_chart_authorized"] is value["automatic_relaunch_authorized"] is False


acceptance = {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_REFEREE_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_HELD_ONE_COMBINED_P32003_DIAGNOSTIC_ONLY",
    "held_manifest_sha256": PINS[HELD / "MANIFEST.sha256"],
    "source_sha256": PINS[p_path], "runner_sha256": PINS[runner_path],
    "variables": 67, "generators": 6574,
    "scope": "V(A67,A12) intersect D(b0) only", "intersection_chart_count": 57,
    "maximum_lane_count": 1, "solver_runs": 0, "attempts": 0,
    "group16_closed": False, "mathematical_coverage": False,
    "exact_Q_authorized": False, "other_chart_authorized": False,
    "automatic_relaunch_authorized": False,
}
contract(acceptance)

mutations = [
    lambda x: x.update(held_manifest_sha256="0" * 64),
    lambda x: x.update(source_sha256="0" * 64),
    lambda x: x.update(runner_sha256="0" * 64),
    lambda x: x.update(variables=68),
    lambda x: x.update(generators=6573),
    lambda x: x.update(scope="group16"),
    lambda x: x.update(intersection_chart_count=1),
    lambda x: x.update(maximum_lane_count=2),
    lambda x: x.update(solver_runs=1),
    lambda x: x.update(group16_closed=True),
    lambda x: x.update(exact_Q_authorized=True),
    lambda x: x.update(automatic_relaunch_authorized=True),
]
passed = 0
for mutation in mutations:
    candidate = copy.deepcopy(acceptance)
    mutation(candidate)
    try:
        contract(candidate)
    except (AssertionError, KeyError, TypeError):
        passed += 1
assert passed == len(mutations)

(HERE / "independent_referee_acceptance.json").write_text(json.dumps(acceptance, indent=2, sort_keys=True) + "\n")
result = {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_HELD_REFEREE_V1",
    "status": "PASS_HELD_APPROVAL_ONLY_ZERO_RUN",
    "source": {
        "Q_sha256": PINS[q_path], "p32003_sha256": PINS[p_path],
        "Q_bytes": len(q_bytes), "p32003_bytes": len(p_bytes),
        "variables": 67, "generators": 6574,
        "sole_ring_substitution": True, "strong_epilogue_preserved": True,
    },
    "scope": {
        "logical_chart": "V(A67,A12) intersect D(b0)",
        "full_intersections": 57, "single_chart_closes_group16": False,
        "mathematical_coverage": False, "solver_runs": 0, "attempts": 0,
    },
    "runner": {
        "sha256": PINS[runner_path], "native_wall_seconds": 240,
        "wrapper_wall_seconds": 255, "rss_cap_bytes": 8589934592,
        "direct_libproc_group_rss": True, "fresh_libproc_census": True,
        "exclusive_attempt_before_popen": True, "atomic_result": True,
        "process_group_termination": True, "maximum_lane_count": 1,
    },
    "refusal": {
        "acceptance_present_in_held": False, "clearance_present_in_held": False,
        "stale_artifacts": 0, "tmp_artifacts": 0, "prior_timeout_reused": False,
        "exact_Q_authorized": False, "other_chart_authorized": False,
        "automatic_relaunch_authorized": False,
    },
    "hostiles": {"count": passed, "all_pass": True},
    "acceptance_path": "independent_referee_acceptance.json",
    "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"),
    "producer_manifest_lines_replayed": held_manifest_lines,
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
}
(HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "hostiles": passed, "solver_runs": 0}, sort_keys=True))
