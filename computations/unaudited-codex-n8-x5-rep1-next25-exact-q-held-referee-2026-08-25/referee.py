#!/usr/bin/env python3
"""Read-only referee for the strict rep1 next-25 exact-Q held schedule."""
import ast, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELD = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-2026-08-25"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
G13 = ROOT / "computations/unaudited-codex-n8-x5-rep1-group13-exact-q-referee-2026-08-25"
G15 = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-exact-q-terminal-referee-2026-08-25"
NEXT10 = ROOT / "computations/unaudited-codex-n8-x5-rep1-next10-exact-q-terminal-referee-2026-08-25"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

pins = {
    HELD / "MANIFEST.sha256": "79052e97d726b5dfc6bf5c4831af27638548bf5cf3a79ade3948a94059470810",
    HELD / "held_schedule.json": "014466d27be2e661653ba2d957389d55053aec511197b310b2667dcfa4cb6a36",
    HELD / "source_ledger.json": "67376d9ddc96b65f0c34d0f746c85703417d0fb3be88ce5d2cf90a601945c833",
    HELD / "run_next25.py": "ad655676b830652681cddd7aa7af46987713984bb63db7dc68157bf88800c268",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    G13 / "FINAL_MANIFEST.sha256": "aa7e6ef6457d18b8020dc1ece2566b83155a4f6d44bb569242e56c345f60a16e",
    G13 / "results_referee.json": "f156dd0fec67dcfe894e182a33778f4c0a688e39d71bf2d12b92d1cf4f377401",
    G15 / "FINAL_MANIFEST.sha256": "e9606d922c52dc79809249dbd6df98a0e61caa5a25bcc52d4d781f1d9a46c23d",
    G15 / "results_referee.json": "66d20e4a7991529826ee80288500c41707866d1fa7f0840bd680db927eb0f8a2",
    NEXT10 / "FINAL_MANIFEST.sha256": "3f3e91a3c63872371ad57014fada848ded4dd6bca0b829b824ed7d79d0f50b00",
    NEXT10 / "results_referee.json": "136d01596dc624804ae2073fec1e0227ecfe8ca2f7092994b84356871f919627",
}
for path, expected in pins.items(): assert sha(path) == expected, (path, sha(path), expected)

def replay(path, base):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        expected, raw = line.split(None, 1)
        target = Path(raw.strip())
        if not target.is_absolute():
            target = ROOT / target if raw.strip().startswith("computations/") else base / target
        assert target.is_file() and sha(target) == expected, target
        count += 1
    return count

manifest_counts = {
    "held": replay(HELD / "MANIFEST.sha256", HELD),
    "census": replay(CENSUS / "MANIFEST.sha256", CENSUS),
    "group13": replay(G13 / "FINAL_MANIFEST.sha256", G13),
    "group15": replay(G15 / "FINAL_MANIFEST.sha256", G15),
    "next10": replay(NEXT10 / "FINAL_MANIFEST.sha256", NEXT10),
}

SELECTED = [11, 12, 14] + list(range(16, 38))
CLOSED = list(range(0, 11)) + [13, 15]
assert len(SELECTED) == 25 and len(CLOSED) == 13
assert not set(SELECTED) & set(CLOSED)
assert sorted(SELECTED + CLOSED) == list(range(38))

g13 = json.loads((G13 / "results_referee.json").read_text())
g15 = json.loads((G15 / "results_referee.json").read_text())
next10 = json.loads((NEXT10 / "results_referee.json").read_text())
assert g13["status"] == "PASS_EXACT_Q_UNIT_IDEAL_GROUP13_ONLY" and g13["closed_groups"] == [0, 13]
assert g15["status"] == "PASS_UNIT_IDEAL_EXACT_Q_GROUP15_ONLY"
assert next10["status"] == "PASS_ALL_TEN_EXACT_Q_UNIT_IDEALS" and next10["groups_closed"] == list(range(1, 11))
assert sorted(set(g13["closed_groups"] + next10["groups_closed"] + [15])) == CLOSED

ledger = json.loads((HELD / "source_ledger.json").read_text())
schedule = json.loads((HELD / "held_schedule.json").read_text())
census = json.loads((CENSUS / "results_canonical_census.json").read_text())
records = {record["group_id"]: record for record in census["enumeration"]["records"]}
assert sorted(records) == list(range(162))
assert ledger["selection"] == {"excluded_closed_groups": CLOSED, "rule": "25 lowest eligible canonical group IDs in strict ascending order", "selected_group_ids": SELECTED}
assert schedule["selection"] == ledger["selection"]
lanes = ledger["lanes"]
assert [lane["group_id"] for lane in lanes] == SELECTED
assert [lane["ordinal"] for lane in lanes] == list(range(1, 26))

def top_count(body):
    depth = 0; count = 1
    for char in body:
        if char == "(": depth += 1
        elif char == ")": depth -= 1; assert depth >= 0
        elif char == "," and depth == 0: count += 1
    assert depth == 0
    return count

source_census = []
for lane in lanes:
    gid = lane["group_id"]; record = records[gid]
    assert lane["canonical_chart"] == record["canonical_chart"]
    assert lane["source_sha256"] == record["exact_Q_source_sha256"]
    assert lane["source_bytes"] == record["exact_Q_source_bytes"]
    source = HELD / lane["source_path"]
    assert sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
    text = source.read_text()
    assert text.count("ring r=0,(") == text.count("ideal G=slimgb(I);") == text.count("poly remainder=reduce(1,G);") == text.count("quit;") == 1
    a = text.index("ring r=0,(") + len("ring r=0,("); b = text.index("),dp;", a)
    variables = [value.strip() for value in text[a:b].split(",")]
    i = text.index("ideal I=") + len("ideal I="); j = text.index(';\nprint("INPUT_GENERATORS=', i)
    generators = top_count(text[i:j])
    assert len(variables) == len(set(variables)) == lane["variables"] == 91
    assert generators == lane["generators"] == 6577
    source_census.append({"group_id": gid, "sha256": lane["source_sha256"], "variables": 91, "generators": 6577})

runner = (HELD / "run_next25.py").read_text(); ast.parse(runner)
tokens = (
    "proc_listpgrppids", "group_rss(process.pid,True)", "rusage failure for live member",
    "NATIVE_WALL=240", "WRAPPER_WALL=250", "RSS_CAP=8*1024**3",
    "command=[str(GTIMEOUT)", "--kill-after={KILL_AFTER}s", "start_new_session=True",
    "exclusive(HERE/'BATCH_ATTEMPT.json'", "for lane in lanes:",
    "if not unit:stop=", "break", "os.replace(t,p)",
    "assert [x['group_id'] for x in batch]==list(SELECTED[:len(batch)])",
    "'parallel':False", "'relaunch':False",
)
for token in tokens: assert token in runner, token
marker = runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'")
loop = runner.index("for lane in lanes:", marker)
popen = runner.index("process=subprocess.Popen", loop)
assert runner.count("subprocess.Popen(") == 1 and marker < loop < popen
execution = schedule["execution"]
assert execution["order"] == SELECTED and execution["maximum_lane_count"] == 25
assert execution["parallel"] is execution["skip"] is execution["reorder"] is execution["relaunch"] is False
assert execution["stop_whole_batch_on"] == ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"]
assert execution["native_wall_seconds_each"] == 240 and execution["wrapper_wall_seconds_each"] == 250 and execution["rss_cap_bytes_each"] == 8589934592

for schema_name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((HELD / schema_name).read_text())
    assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"])
acceptance = json.loads((HERE / "independent_referee_acceptance.json").read_text())
schema = json.loads((HELD / "independent_referee_acceptance.schema.json").read_text())
assert set(acceptance) == set(schema["required"])
for key, value in acceptance.items():
    if "const" in schema["properties"][key]: assert value == schema["properties"][key]["const"]
for absent in ("independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HELD / absent).exists(), absent
assert not any(HELD.glob("*.tmp"))
assert schedule["scope"] == {"attempt_markers": 0, "clearances": 0, "groups_newly_closed": 0, "mathematical_coverage": False, "representative_closed": False, "result_files": 0, "solver_launches": 0, "source_regeneration_only": True}

print(json.dumps({
    "status": "PASS_APPROVED_HELD_STRICT_REP1_NEXT25_ZERO_RUNS",
    "closed_baseline_group_ids": CLOSED, "selected_group_ids": SELECTED,
    "sources_verified": len(source_census), "variables_each": 91, "generators_each": 6577,
    "source_ledger_sha256": sha(HELD / "source_ledger.json"), "runner_sha256": sha(HELD / "run_next25.py"),
    "acceptance_sha256": sha(HERE / "independent_referee_acceptance.json"), "manifest_counts": manifest_counts,
    "scope": {"solver_runs": 0, "mathematical_coverage": False, "representative_closed": False},
}, sort_keys=True))
