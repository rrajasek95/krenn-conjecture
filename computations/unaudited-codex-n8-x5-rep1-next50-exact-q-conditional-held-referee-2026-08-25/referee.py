#!/usr/bin/env python3
"""Independent referee for the non-launchable conditional rep1 next-50 package."""
import ast, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELD = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-conditional-held-2026-08-25"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
NEXT25_HELD = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-2026-08-25"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

pins = {
    HELD / "MANIFEST.sha256": "db8aa8acd4977934273c28249ffba8930c102cec2fc10bad9d86edb7fa51423d",
    HELD / "source_ledger.json": "1888166e62d1e475d745283e1b5c5225ed1aac8d5ac14a4be3543972d881e172",
    HELD / "run_next50.py": "eba736280a2d724cc1c46370d85292d7543f7bfd46a7e51e813c5bfe6ce0b66e",
    HELD / "future_next25_dependency.json": "aba4c9792cd2874269722f678864130cfde27c30caa47d505249a77ada82c896",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    NEXT25_HELD / "MANIFEST.sha256": "79052e97d726b5dfc6bf5c4831af27638548bf5cf3a79ade3948a94059470810",
    NEXT25_HELD / "source_ledger.json": "67376d9ddc96b65f0c34d0f746c85703417d0fb3be88ce5d2cf90a601945c833",
}
for path, expected in pins.items(): assert sha(path) == expected, (path, sha(path), expected)

def replay(path, base):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        expected, raw = line.split(None, 1); target = Path(raw.strip())
        if not target.is_absolute(): target = ROOT / target if raw.strip().startswith("computations/") else base / target
        assert target.is_file() and sha(target) == expected, target
        count += 1
    return count

manifest_counts = {"held": replay(HELD / "MANIFEST.sha256", HELD), "census": replay(CENSUS / "MANIFEST.sha256", CENSUS), "next25_held": replay(NEXT25_HELD / "MANIFEST.sha256", NEXT25_HELD)}
SELECTED = list(range(38, 88))
ledger = json.loads((HELD / "source_ledger.json").read_text())
schedule = json.loads((HELD / "held_schedule.json").read_text())
census = json.loads((CENSUS / "results_canonical_census.json").read_text())
records = {record["group_id"]: record for record in census["enumeration"]["records"]}
assert sorted(records) == list(range(162))
assert ledger["selection"] == {"assumed_closed_group_ids": list(range(38)), "dependency": "future exact next25 terminal referee PASS", "rule": "50 lowest canonical group IDs remaining after conditional closure of groups 0..37", "selected_group_ids": SELECTED}
lanes = ledger["lanes"]
assert [lane["group_id"] for lane in lanes] == SELECTED and [lane["ordinal"] for lane in lanes] == list(range(1, 51))

def top_count(body):
    depth = 0; count = 1
    for char in body:
        if char == "(": depth += 1
        elif char == ")": depth -= 1; assert depth >= 0
        elif char == "," and depth == 0: count += 1
    assert depth == 0
    return count

total_bytes = 0
for lane in lanes:
    record = records[lane["group_id"]]
    assert lane["canonical_chart"] == record["canonical_chart"]
    assert lane["source_sha256"] == record["exact_Q_source_sha256"]
    assert lane["source_bytes"] == record["exact_Q_source_bytes"]
    source = HELD / lane["source_path"]
    assert sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
    text = source.read_text(); total_bytes += source.stat().st_size
    assert text.count("ring r=0,(") == text.count("ideal G=slimgb(I);") == text.count("poly remainder=reduce(1,G);") == text.count("quit;") == 1
    a = text.index("ring r=0,(") + len("ring r=0,("); b = text.index("),dp;", a)
    variables = [value.strip() for value in text[a:b].split(",")]
    i = text.index("ideal I=") + len("ideal I="); j = text.index(';\nprint("INPUT_GENERATORS=', i)
    assert len(variables) == len(set(variables)) == lane["variables"] == 91
    assert top_count(text[i:j]) == lane["generators"] == 6577
assert total_bytes == 89221420

dependency = json.loads((HELD / "future_next25_dependency.json").read_text())
assert dependency["status"] == "UNSATISFIED_PLACEHOLDER_BLOCKS_LAUNCH"
assert dependency["satisfied"] is False
assert dependency["current_future_manifest_sha256"] is None and dependency["current_future_result_sha256"] is None
assert dependency["expected_closed_group_ids"] == [11, 12, 14] + list(range(16, 38))
assert dependency["expected_closed_union_after_pass"] == list(range(38))
future_manifest = ROOT / dependency["future_manifest_path"]
future_result = ROOT / dependency["future_result_path"]
assert not future_manifest.exists() and not future_result.exists()
assert schedule["future_dependency"] == {"currently_satisfied": False, "future_manifest_hash_placeholder": None, "future_result_hash_placeholder": None, "path": "future_next25_dependency.json", "runner_requires_later_acceptance_to_bind_both_exact_hashes": True, "sha256": pins[HELD / "future_next25_dependency.json"]}

runner_path = HELD / "run_next50.py"; runner = runner_path.read_text(); ast.parse(runner)
tokens = (
    "SELECTED=tuple(range(38,88))", "proc_listpgrppids", "group_rss(process.pid,True)",
    "rusage failure for live member", "NATIVE_WALL=240", "WRAPPER_WALL=250", "RSS_CAP=8*1024**3",
    "future_manifest.is_file() and future_result.is_file()", "UNSATISFIED_PLACEHOLDER_BLOCKS_LAUNCH",
    "current_future_manifest_sha256", "current_future_result_sha256",
    "future_manifest_sha=sha(future_manifest)", "future_result_sha=sha(future_result)",
    "future['groups_closed']==dependency['expected_closed_group_ids']",
    "future['closed_union']==dependency['expected_closed_union_after_pass']",
    "next25_terminal_manifest_sha256", "next25_terminal_result_sha256",
    "exclusive(HERE/'BATCH_ATTEMPT.json'", "for lane in lanes:", "if not unit:stop=", "break",
    "atomic(HERE/'results'/", "'parallel':False", "'relaunch':False",
)
for token in tokens: assert token in runner, token
assert runner.index("assert manifest.is_file() and acceptance.is_file() and clearance.is_file()") < runner.index("future_manifest.is_file() and future_result.is_file()")
assert runner.index("future_manifest.is_file() and future_result.is_file()") < runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'") < runner.index("subprocess.Popen(")
assert runner.count("subprocess.Popen(") == 1
execution = schedule["execution"]
assert execution["order"] == SELECTED and execution["maximum_lane_count"] == 50
assert execution["parallel"] is execution["skip"] is execution["reorder"] is execution["relaunch"] is False
assert execution["native_wall_seconds_each"] == 240 and execution["wrapper_wall_seconds_each"] == 250 and execution["rss_cap_bytes_each"] == 8589934592
assert execution["stop_whole_batch_on"] == ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"]
for schema_name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((HELD / schema_name).read_text())
    assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"])
    assert schema["properties"]["next25_terminal_manifest_sha256"]["pattern"] == "^[0-9a-f]{64}$"
    assert schema["properties"]["next25_terminal_result_sha256"]["pattern"] == "^[0-9a-f]{64}$"
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HELD / absent).exists(), absent
assert not any(HELD.glob("*.tmp"))
assert schedule["scope"] == {"attempt_markers": 0, "clearances": 0, "groups_newly_closed": 0, "mathematical_coverage": False, "representative_closed": False, "result_files": 0, "solver_launches": 0, "source_regeneration_only": True}

print(json.dumps({
    "status": "PASS_CONDITIONAL_HELD_NEXT50_BLOCKED_PENDING_NEW_DEPENDENCY_BINDING_AUDIT",
    "selected_group_ids": SELECTED, "sources_verified": 50, "total_source_bytes": total_bytes,
    "variables_each": 91, "generators_each": 6577, "dependency_sha256": sha(HELD / "future_next25_dependency.json"),
    "dependency_satisfied": False, "future_hashes": [None, None], "manifest_counts": manifest_counts,
    "scope": {"launch_authorized": False, "solver_runs": 0, "mathematical_coverage": False},
}, sort_keys=True))
