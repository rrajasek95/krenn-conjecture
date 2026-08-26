#!/usr/bin/env python3
"""Independent exact-Q result referee for the rank(A47)=3 adjugate chart."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rectangle-rank3-adjugate-p32003-diagnostic-referee-2026-08-25"
RUN = PARENT / "exact_q_run"
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-rectangle-rank3-adjugate-ideal-referee-2026-08-25"
INDEP = ROOT / "computations/unaudited-codex-n8-x5-rectangle-rank3-adjugate-independent-referee-2026-08-25"
OUT = HERE / "results_referee.json"

EXPECTED = {
    RUN / "MANIFEST.sha256": "586df8668047a5d62a2714825807f246792df2a11d616515d5c658bd79d49b80",
    RUN / "RESULT.json": "c742220543ab6a45c9c751e7454031146c62e7ea85f62f7d3de34d47aedea081",
    RUN / "rectangle_rank3_adjugate_Q.sing": "e2739688ea9986d59c56e17e6f0058154d9ddb7930bf9617a1d3a3a8167538f5",
    RUN / "LAUNCH_RECORD.json": "eeaec161d608f7c034bfb23b76025b98f1f5472597772a3ab5833484502a5c7c",
    RUN / "run_singular_exact_q_watchdog.py": "b8ec2d5f0497ed2b0d7b6f54c9e870b45154805d5ef1f3b7b8a43caacdc36ae2",
    RUN / "watchdog.json": "ab6c78df174d6e728c92d22f94948d75e2ec264bde9ec4a84a6f8597a6e453a5",
    RUN / "stdout.log": "d48762b27d8e7351ded227e6ce87d6b3c54e3cd3348303894ec1a9b3e5d85c85",
    RUN / "stderr.log": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    PARENT / "EXACT_Q_HELD_PLAN.json": "56618e1848b7809db58f86103f1c9a3a33a31d3f8fd97b3a1b744eff15d52faa",
    PARENT / "FINAL_MANIFEST.sha256": "45fad912e746c13792dfa0b35e92ffa975266d6bb01732cbef8101a324bec6f6",
    PRODUCER / "MANIFEST.sha256": "c2fbb2ba00a1dc854b66ea7791cfb0fdad7b3b1747ee71b01e7c9f62a65ee8e5",
    PRODUCER / "results_adjugate_referee.json": "6cf2d19e4e9a65348a7792227055be14d415f4a1a205b71ad417f2b7b90d7b08",
    INDEP / "FINAL_MANIFEST.sha256": "873d47c348464c0f03dbd8011463d7bcef9df2732c4b6fecafa56e7e121b0a42",
    INDEP / "results_referee.json": "bd6babf5038f5faa8533cc3183edb0d2b4be0d4fec3d3c9a4d15bd56b9bdee95",
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def replay_manifest(path):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        assert sha(path.parent / rel.strip()) == digest, (path, rel)
        count += 1
    return count


def top_level_count(body):
    depth = 0
    count = 1 if body.strip() else 0
    for char in body:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0:
            count += 1
    assert depth == 0
    return count


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
manifest_entries = replay_manifest(RUN / "MANIFEST.sha256")

source = (RUN / "rectangle_rank3_adjugate_Q.sing").read_text()
assert source == (PRODUCER / "rectangle_rank3_adjugate_Q.sing").read_text()
assert source.count("ring r=0,") == 1 and "ring r=32003," not in source
ring_start = source.index("ring r=0,(") + len("ring r=0,(")
ring_end = source.index("),dp;", ring_start)
variables = [x.strip() for x in source[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 56
ideal_start = source.index("ideal I=(") + len("ideal I=")
ideal_end = source.index(";\nprint(\"INPUT_VARIABLES=", ideal_start)
generators = top_level_count(source[ideal_start:ideal_end])
assert generators == 6563
assert source.count("ideal G=slimgb(I);") == 1
assert source.count("poly remainder=reduce(1,G);") == 1

launch = json.loads((RUN / "LAUNCH_RECORD.json").read_text())
watchdog = json.loads((RUN / "watchdog.json").read_text())
result = json.loads((RUN / "RESULT.json").read_text())
assert launch["status"] == "CLEARED_PRELAUNCH"
assert launch["scope"] == "Exactly one exact-Q Singular lane; no second lane or relaunch."
assert launch["process_census"]["pass"] is True
assert launch["source"]["sha256"] == EXPECTED[RUN / "rectangle_rank3_adjugate_Q.sing"]
assert launch["source"]["variables"] == 56 and launch["source"]["generators"] == 6563
assert launch["terminal_rule"].startswith("Stop and seal after any terminal outcome")

assert watchdog["schema"] == "KRENN_X5_RECTANGLE_RANK3_ADJUGATE_EXACT_Q_WATCHDOG_V1"
assert watchdog["status"] == "PASS" and watchdog["field"] == "Q"
assert watchdog["returncode"] == 0 and watchdog["terminal_reason"] is None
assert watchdog["parsed_stdout"] == {
    "GROEBNER_SIZE": "1", "INPUT_GENERATORS": "6563", "INPUT_VARIABLES": "56",
    "STATUS": "UNIT_IDEAL", "UNIT_REMAINDER": "0"
}
assert watchdog["elapsed_seconds"] == 0.519554
assert watchdog["peak_rss_kib"] == 23160
assert watchdog["native_wall_seconds"] == 480 and watchdog["wrapper_wall_seconds"] == 510
assert watchdog["rss_limit_kib"] == 8 * 1024 * 1024
assert watchdog["logs_atomic"] is True
assert watchdog["q_lane_launched"] is True
assert watchdog["second_lane_launched"] is False and watchdog["automatic_relaunch"] is False
assert watchdog["stdout_sha256"] == EXPECTED[RUN / "stdout.log"]
assert watchdog["stderr_sha256"] == EXPECTED[RUN / "stderr.log"]

assert result["schema"] == "KRENN_X5_RECTANGLE_RANK3_ADJUGATE_EXACT_Q_RESULT_V1"
assert result["status"] == "PASS_EXACT_Q_UNIT_IDEAL_CHART_CLOSED"
assert result["source"] == {
    "sha256": EXPECTED[RUN / "rectangle_rank3_adjugate_Q.sing"],
    "bytes": 724948, "field": "Q", "variables": 56, "generators": 6563
}
assert result["singular_result"]["groebner_size"] == 1
assert result["singular_result"]["unit_remainder"] == 0
assert result["singular_result"]["terminal_status"] == "UNIT_IDEAL"
assert result["resource_evidence"]["elapsed_seconds"] == 0.519554
assert result["resource_evidence"]["peak_rss_kib"] == 23160
assert result["resource_evidence"]["logs_atomic"] is True
assert result["resource_evidence"]["temporary_logs_absent"] is True
assert result["scope"]["singular_lanes"] == 1
assert result["scope"]["second_lanes"] == 0 and result["scope"]["relaunches"] == 0
assert result["scope"]["closed"] == [
    "rank(A47)=3 adjugate chart",
    "A12-absent amplitude-inactive lift",
    "A12-present amplitude-inactive lift",
]
assert result["scope"]["not_closed"] == [
    "rank(A47)<=2", "unmapped16 outside this chart", "seven-block branch", "the full conjecture"
]
assert not list(RUN.glob("*.tmp"))

# The independent design proof is required for transport from the adjugate
# ideal to precisely these two physical lifts; it does not transport farther.
design = json.loads((INDEP / "results_referee.json").read_text())
assert design["status"] == "PASS_EXACT_EQUIVALENT_DESIGN_NO_SOLVE_NO_CLOSURE"
assert design["Q_source_sha256"] == EXPECTED[RUN / "rectangle_rank3_adjugate_Q.sing"]
assert design["counts"] == {"full_x5": 6561, "generators": 6563, "saturations": 2, "variables": 56}
assert design["variants"]["amplitude_and_guard_inactive"] is True
assert design["scope"] == {"A12_variants_closed": False, "rank3_closed": False, "solver_launches": 0}

audit = {
    "schema": "KRENN_X5_RECTANGLE_RANK3_ADJUGATE_EXACT_Q_REFEREE_V1",
    "status": "PASS_EXACT_Q_UNIT_IDEAL_RANK3_TWO_LIFTS_ONLY",
    "producer_manifest_sha256": EXPECTED[RUN / "MANIFEST.sha256"],
    "producer_result_sha256": EXPECTED[RUN / "RESULT.json"],
    "source_Q_sha256": EXPECTED[RUN / "rectangle_rank3_adjugate_Q.sing"],
    "manifest_entries_replayed": manifest_entries,
    "variables": len(variables),
    "input_generators": generators,
    "groebner_basis_size": 1,
    "unit_remainder": 0,
    "wall_seconds": watchdog["elapsed_seconds"],
    "peak_rss_kib": watchdog["peak_rss_kib"],
    "atomic_no_tmp": True,
    "observed_second_lane_or_relaunch": False,
    "scope": {
        "closed": result["scope"]["closed"],
        "not_closed": result["scope"]["not_closed"],
        "transport_basis": "pinned forward/reverse adjugate equivalence and amplitude inactivity",
    },
    "no_singular_rerun_by_referee": True,
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
