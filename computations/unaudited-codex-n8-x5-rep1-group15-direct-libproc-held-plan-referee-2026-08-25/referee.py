#!/usr/bin/env python3
"""Independent held-contract referee for the wholly new group15 lane."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-direct-libproc-held-plan-2026-08-25"
OLD = ROOT / "computations/unaudited-codex-n8-x5-rep1-next3-exact-q-batch-2026-08-25"
OLD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-next3-zero-coverage-failure-referee-2026-08-25"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
CENSUS_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25"
MINOR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
OUT = HERE / "results_referee.json"

EXPECTED = {
    PROD / "MANIFEST.sha256": "2a0d0426ee8eb9e836ca493ab3154e127f705d2e78cdb94600b612abb31cf337",
    PROD / "HELD_GROUP15_PLAN.json": "e778f68f78c087a2d63f4491e0d67d9920302dc55cd2d39e80abc380f66c6ce4",
    OLD / "MANIFEST.sha256": "e7d3e6bb528cf3614690aaf0b8f246975c87d9f6c8a681a8bc2f5c536037af32",
    OLD / "BATCH_FAILURE.json": "d6c039db2db4154be5b0ef4afaa78d81314666284e5b025ded604bac41aa85fb",
    OLD_REF / "FINAL_MANIFEST.sha256": "2a22ca10d0121d79028955fa68106223d3815b4d81a4d69d8e116fd4a41f60d3",
    OLD_REF / "DISTINCT_GROUP15_DIRECT_LIBPROC_ADVICE.json": "babc0f9e3893fc87f0ec3237960607182a25efe817a0df1125151e1523d88605",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    CENSUS_REF / "FINAL_MANIFEST.sha256": "f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a",
    MINOR / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    MINOR / "generate_minor_quotient.py": "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def validate_plan(plan):
    assert plan["schema"] == "KRENN_X5_REP1_GROUP15_EXACT_Q_DIRECT_LIBPROC_HELD_PLAN_V1"
    assert plan["status"] == "HELD_NOT_LAUNCHED"
    assert plan["relationship_to_old_batch"] == {
        "old_batch_manifest_sha256": EXPECTED[OLD / "MANIFEST.sha256"],
        "old_batch_audit_manifest_sha256": EXPECTED[OLD_REF / "FINAL_MANIFEST.sha256"],
        "old_batch_status": "TERMINAL_ZERO_COVERAGE",
        "old_batch_reused_or_resumed": False,
        "old_batch_patch_or_relaunch_authorized": False,
        "this_design": "wholly new sibling, one group15 lane only",
    }
    assert plan["authority"]["poincare_advice_sha256"] == EXPECTED[OLD_REF / "DISTINCT_GROUP15_DIRECT_LIBPROC_ADVICE.json"]
    assert plan["authority"]["advice_manifest_sha256"] == EXPECTED[OLD_REF / "FINAL_MANIFEST.sha256"]
    assert plan["authority"]["launch_authorized"] is False
    assert plan["authority"]["fresh_manager_and_resource_clearance_required"] is True
    lane = plan["lane"]
    assert lane == {
        "maximum_lanes": 1, "group_id": 15, "field": "Q",
        "canonical_chart": [0, 0, 0, 1, "z", 1, 0, 2],
        "source_sha256": "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04",
        "source_bytes": 1841468, "variables": 91, "generators": 6577,
        "native_wall_seconds": 240, "wrapper_wall_seconds": 250,
        "rss_limit_bytes": 8589934592, "poll_seconds": 0.25,
    }
    process = plan["process_contract"]
    assert process["prelaunch_census"] == "Darwin libproc proc_listpids plus proc_pidpath in the runner process"
    assert process["rss_observer"] == "Darwin libproc PROC_PIDTASKINFO summed over the Singular process group"
    assert process["external_process_listing_commands"] == []
    assert all(process[key] is True for key in (
        "fresh_lane_directory", "source_materialized_atomically_after_census",
        "source_rehashed_before_child_creation", "child_starts_new_process_group",
        "telemetry_includes_all_successful_samples", "observer_failure_is_terminal",
    ))
    assert all(plan["atomic_outputs"].values())
    assert plan["stop_policy"] == {
        "stop_after_any_terminal_outcome": True, "automatic_relaunch": False,
        "second_lane": False, "group17_or_group25": False, "patch_in_place": False,
    }
    assert plan["scope"] == {
        "launched": False, "singular_process_created": False,
        "source_materialized": False, "accepted_coverage": 0,
        "representative_1_closed": False,
    }


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
manifest_entries = replay_manifest(PROD / "MANIFEST.sha256")
plan = json.loads((PROD / "HELD_GROUP15_PLAN.json").read_text())
validate_plan(plan)

# The old package remains terminal and unmodified: only an empty group15
# directory exists and there is no resumable attempt state.
old_failure = json.loads((OLD / "BATCH_FAILURE.json").read_text())
assert old_failure["accepted_coverage"] == 0 and old_failure["launched_groups"] == []
assert old_failure["disposition"]["patched_relaunch"] is False
assert old_failure["disposition"]["further_groups_launched"] is False
assert (OLD / "group15").is_dir() and list((OLD / "group15").iterdir()) == []
assert not (OLD / "BATCH_RESULT.json").exists()
assert PROD.resolve() != OLD.resolve()

# Independently regenerate the exact Q source in memory from the pinned
# generator and compare it with the sealed census record; do not materialize.
spec = importlib.util.spec_from_file_location("sealed_minor", MINOR / "generate_minor_quotient.py")
assert spec and spec.loader
minor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(minor)
base = minor.load_base()
chart_tuple = (0, 0, 0, 1, "z", 1, 0, 2)
coordinate, p, q, r, kind, s, a, b = chart_tuple
chart = {"coordinate": coordinate, "outside": (p, q), "x_pivot": r, "q_kind": kind, "q_pivot": s, "minor_pair": (a, b)}
source = minor.build_program(base, chart, "0")
assert len(source.encode()) == 1841468
assert hashlib.sha256(source.encode()).hexdigest() == plan["lane"]["source_sha256"]
assert source.count("ring r=0,") == 1
ring_start = source.index("ring r=0,(") + len("ring r=0,(")
ring_end = source.index("),dp;", ring_start)
variables = [value.strip() for value in source[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 91
ideal_start = source.index("ideal I=(") + len("ideal I=")
ideal_end = source.index(";\nprint(\"INPUT_GENERATORS=", ideal_start)
assert top_level_count(source[ideal_start:ideal_end]) == 6577
for token in ("ideal G=slimgb(I);", "poly remainder=reduce(1,G);", "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED"):
    assert source.count(token) == 1
census = json.loads((CENSUS / "results_canonical_census.json").read_text())
record = next(item for item in census["enumeration"]["records"] if item["group_id"] == 15)
assert record["canonical_chart"] == list(chart_tuple)
assert record["exact_Q_source_sha256"] == hashlib.sha256(source.encode()).hexdigest()
assert record["exact_Q_source_bytes"] == len(source.encode())

# The held package contains no runner or source and makes no external process
# listing call. A future runner remains a separate clearance/audit obligation.
files = sorted(path.name for path in PROD.iterdir())
assert files == ["HELD_GROUP15_PLAN.json", "MANIFEST.sha256", "REPORT.md", "validate.py"]
text = "\n".join(path.read_text() for path in PROD.iterdir() if path.is_file())
assert "/bin/ps" not in text and "subprocess.run" not in text and "subprocess.Popen" not in text

hostiles = {}
for name, mutation in {
    "old_batch_reuse": lambda p: p["relationship_to_old_batch"].__setitem__("old_batch_reused_or_resumed", True),
    "external_ps": lambda p: p["process_contract"].__setitem__("external_process_listing_commands", ["/bin/ps"]),
    "second_lane": lambda p: p["stop_policy"].__setitem__("second_lane", True),
    "launch_flip": lambda p: p["authority"].__setitem__("launch_authorized", True),
}.items():
    candidate = copy.deepcopy(plan)
    mutation(candidate)
    try:
        validate_plan(candidate)
    except AssertionError:
        hostiles[name] = True
    else:
        hostiles[name] = False
assert all(hostiles.values())

audit = {
    "schema": "KRENN_X5_REP1_GROUP15_DIRECT_LIBPROC_HELD_PLAN_REFEREE_V1",
    "status": "APPROVE_HELD_CONTRACT_ONLY_NOT_LAUNCHED",
    "producer_manifest_sha256": EXPECTED[PROD / "MANIFEST.sha256"],
    "producer_plan_sha256": EXPECTED[PROD / "HELD_GROUP15_PLAN.json"],
    "manifest_entries_replayed": manifest_entries,
    "wholly_new_sibling_no_old_attempt_reuse": True,
    "old_batch_terminal_zero_coverage": True,
    "external_process_listing_commands": [],
    "source_regenerated_sha256": hashlib.sha256(source.encode()).hexdigest(),
    "source_counts": {"variables": len(variables), "generators": 6577},
    "lane": {"group_id": 15, "field": "Q", "maximum_lanes": 1, "native_wall_seconds": 240, "wrapper_wall_seconds": 250, "rss_limit_bytes": 8589934592},
    "atomic_and_stop_contract": "PASS",
    "hostile_tests": hostiles,
    "launch_authorized": False,
    "runner_present": False,
    "runner_requires_separate_pin_and_clearance": True,
    "scope_if_pass": "group15 only; 3/162 closed; representative 1 remains open",
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
