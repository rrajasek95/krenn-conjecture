#!/usr/bin/env python3
"""Independent read-only referee for the conditional final rep1 24-lane package."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELD = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups138-161-exact-q-conditional-held-2026-08-25"
BASE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
CENSUS_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25"
PREVIOUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25"

PINS = {
    HELD / "MANIFEST.sha256": "25a708451a790a3984052519a5fd129182a54b3fbe65dbc85279b998d0667bf5",
    HELD / "source_ledger.json": "ed416a9cc138abae890447995f04e084223fccfe0629da47c9e234e5c02e76be",
    HELD / "normalize_future_dependency.py": "907519564535bc533e060dbef4545ccf2635234041af5d7e0a320db503991568",
    HELD / "results_adapter_tests.json": "4ad1323a6c4367dd124d37eb7fa4a61a7aaa17e9cace285ae7d57550ff3717a9",
    HELD / "run_groups138_161.py": "a942eb6a12512f334bc6bdbf1b023c1428c8372fda46032dbddfb84dcf554f8b",
    BASE / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    BASE / "generate_minor_quotient.py": "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    CENSUS_REF / "FINAL_MANIFEST.sha256": "f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a",
    PREVIOUS / "MANIFEST.sha256": "07ab0d198fc80b91025df7c892081f2aaaa94158014052246d7700095c054450",
    PREVIOUS / "source_ledger.json": "2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b",
}
SELECTED = list(range(138, 162))


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def replay_manifest(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        expected, raw = line.split(None, 1)
        target = Path(raw.strip())
        if not target.is_absolute():
            local = (path.parent / target).resolve()
            rooted = (ROOT / target).resolve()
            target = local if local.is_file() else rooted
        assert target.is_file() and sha(target) == expected, target
        count += 1
    return count


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chart_dict(value):
    coordinate, p, q, r, kind, s, a, b = value
    return {
        "coordinate": coordinate,
        "outside": (p, q),
        "x_pivot": r,
        "q_kind": kind,
        "q_pivot": s,
        "minor_pair": (a, b),
    }


def parse_counts(text: str) -> tuple[int, int]:
    ring = next(line for line in text.splitlines() if line.startswith("ring r="))
    variables = ring.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    depth = 0
    generators = 1
    for char in body:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0:
            generators += 1
    assert depth == 0
    return len(variables), generators


for path, expected in PINS.items():
    assert sha(path) == expected, (path, sha(path), expected)
manifest_counts = {
    "held": replay_manifest(HELD / "MANIFEST.sha256"),
    "base": replay_manifest(BASE / "MANIFEST.sha256"),
    "census": replay_manifest(CENSUS / "MANIFEST.sha256"),
    "census_referee": replay_manifest(CENSUS_REF / "FINAL_MANIFEST.sha256"),
    "previous_conditional": replay_manifest(PREVIOUS / "MANIFEST.sha256"),
}

ledger = json.loads((HELD / "source_ledger.json").read_text())
plan = json.loads((HELD / "held_schedule.json").read_text())
dependency = json.loads((HELD / "future_groups88_137_dependency.json").read_text())
producer_tests = json.loads((HELD / "results_adapter_tests.json").read_text())
census = json.loads((CENSUS / "results_canonical_census.json").read_text())
records = census["enumeration"]["records"]
assert [record["group_id"] for record in records] == list(range(162))
assert [lane["group_id"] for lane in ledger["lanes"]] == SELECTED
assert [lane["ordinal"] for lane in ledger["lanes"]] == list(range(1, 25))
assert ledger["selection"]["selected_group_ids"] == SELECTED
assert ledger["selection"]["conditionally_required_closed_union"] == list(range(138))
assert ledger["selection"]["required_future_groups_closed"] == list(range(88, 138))

# Regenerate every exact-Q source in memory from the independently pinned
# authoritative generator and canonical census; do not write or solve it.
minor = load_module("independent_rep1_minor_generator", BASE / "generate_minor_quotient.py")
base = minor.load_base()
source_audit = []
total_bytes = 0
for lane in ledger["lanes"]:
    gid = lane["group_id"]
    record = records[gid]
    assert record["group_id"] == gid and record["closed"] is False
    assert record["canonical_chart"] == lane["canonical_chart"]
    generated = minor.build_program(base, chart_dict(record["canonical_chart"]), "0")
    payload = generated.encode()
    digest = hashlib.sha256(payload).hexdigest()
    path = HELD / lane["source_path"]
    assert digest == record["exact_Q_source_sha256"] == lane["source_sha256"] == sha(path)
    assert len(payload) == record["exact_Q_source_bytes"] == lane["source_bytes"] == path.stat().st_size
    assert generated == path.read_text()
    assert parse_counts(generated) == (91, 6577) == (lane["variables"], lane["generators"])
    assert generated.count("ring r=0,") == generated.count("ideal G=slimgb(I);") == generated.count("poly remainder=reduce(1,G);") == generated.count("quit;") == 1
    assert record["raw_member_count"] == len(record["raw_members"]) == 6
    source_audit.append({"group_id": gid, "sha256": digest, "bytes": len(payload), "variables": 91, "generators": 6577, "canonical_chart": record["canonical_chart"], "raw_member_count": 6})
    total_bytes += len(payload)
assert total_bytes == 42_769_236

# Independently execute the adapter's pure normalization function against one
# valid synthetic dependency and the same twelve hostile classes.
adapter = load_module("independent_future_dependency_adapter", HELD / "normalize_future_dependency.py")
spec = dependency
good = {
    "schema": spec["required_future_result_schema"],
    "status": spec["required_future_result_status"],
    "new_groups_closed": 50,
    "strict_order": True,
    "parallel": False,
    "skipped": False,
    "relaunch": False,
    "baseline_closed_union": list(range(88)),
    "groups_closed": list(range(88, 138)),
    "closed_union": list(range(138)),
}
normalized = adapter.normalize_record(copy.deepcopy(good), copy.deepcopy(spec))
assert normalized["closed_union"] == list(range(138))
hostiles = {}


def reject(name, mutation):
    terminal = copy.deepcopy(good)
    dependency_copy = copy.deepcopy(spec)
    mutation(terminal, dependency_copy)
    try:
        adapter.normalize_record(terminal, dependency_copy)
    except (AssertionError, KeyError, TypeError):
        hostiles[name] = True
    else:
        hostiles[name] = False


reject("baseline_missing", lambda t, s: t["baseline_closed_union"].pop())
reject("baseline_duplicate", lambda t, s: t["baseline_closed_union"].append(87))
reject("future_missing", lambda t, s: t["groups_closed"].pop())
reject("future_duplicate", lambda t, s: t["groups_closed"].append(137))
reject("future_extra", lambda t, s: t["groups_closed"].append(162))
reject("future_overlap", lambda t, s: t["groups_closed"].__setitem__(0, 87))
reject("future_reorder", lambda t, s: t["groups_closed"].reverse())
reject("wrong_closed_union", lambda t, s: t["closed_union"].pop())
reject("wrong_status", lambda t, s: t.__setitem__("status", "PASS_WRONG"))
reject("skipped", lambda t, s: t.__setitem__("skipped", True))
reject("parallel", lambda t, s: t.__setitem__("parallel", True))
reject("relaunch", lambda t, s: t.__setitem__("relaunch", True))
assert len(hostiles) == 12 and all(hostiles.values())
assert producer_tests["hostile_tests"] == hostiles

# The terminal dependency is deliberately null and absent.  Hence this audit
# approves only the held design; it does not materialize launch acceptance.
assert dependency["status"] == "UNSATISFIED_NULL_HASHES_BLOCK_LAUNCH"
assert dependency["future_manifest_sha256"] is None and dependency["future_result_sha256"] is None
assert dependency["satisfied"] is False
assert dependency["expected_baseline_closed_union"] == list(range(88))
assert dependency["expected_future_groups_closed"] == list(range(88, 138))
assert dependency["required_closed_union"] == list(range(138))
future_manifest = ROOT / dependency["future_manifest_path"]
future_result = ROOT / dependency["future_result_path"]
assert not future_manifest.exists() and not future_result.exists()

assert plan["status"] == "HELD_ZERO_RUNS_FUTURE_GROUPS88_137_HASHES_ABSENT"
assert plan["execution"] == {
    "native_wall_seconds_each": 240,
    "wrapper_wall_seconds_each": 250,
    "rss_cap_bytes_each": 8589934592,
    "maximum_lane_count": 24,
    "order": SELECTED,
    "parallel": False,
    "skip": False,
    "reorder": False,
    "relaunch": False,
    "stop_whole_batch_on": ["NONUNIT", "RESOURCE", "PROCESS", "SCHEMA_OR_TRANSCRIPT_MISMATCH"],
}

runner = (HELD / "run_groups138_161.py").read_text()
compile(runner, str(HELD / "run_groups138_161.py"), "exec")
tokens = (
    "SELECTED=tuple(range(138,162))",
    "NATIVE_WALL=240; WRAPPER_WALL=250; RSS_CAP=8*1024**3",
    "proc_listpgrppids",
    "proc_pid_rusage",
    "live wrapper has no observable group members",
    "rusage failure for live member",
    "start_new_session=True",
    "load_and_normalize(future_manifest_sha,future_result_sha)",
    "normalized['closed_union']==list(range(138))",
    "for lane in lanes:",
    "if not unit:stop=",
    "break",
    "[x['group_id'] for x in batch]==list(SELECTED[:len(batch)])",
    "O_EXCL",
    "os.replace(t,p)",
    "'parallel':False",
    "'relaunch':False",
)
for token in tokens:
    assert token in runner, token
assert runner.count("subprocess.Popen(") == 1
assert not re.search(r"\b(?:threading|multiprocessing|concurrent\.futures)\b", runner)
assert runner.index("normalized=load_and_normalize") < runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'") < runner.rindex("for lane in lanes:")
assert runner.index("atomic(HERE/'results'/") < runner.index("if not unit:stop=")

for absent in (
    "independent_referee_acceptance.json",
    "launch_clearance.json",
    "BATCH_ATTEMPT.json",
    "batch_result.json",
    "results",
):
    assert not (HELD / absent).exists(), absent
assert not list(HELD.glob("*.tmp"))

result = {
    "schema": "KRENN_X5_REP1_GROUPS138_161_EXACT_Q_CONDITIONAL_HELD_REFEREE_V1",
    "status": "PASS_HELD_ONLY_FINAL_24_EXACT_Q_SOURCES_DEPENDENCY_ABSENT",
    "producer_manifest_sha256": PINS[HELD / "MANIFEST.sha256"],
    "source_ledger_sha256": PINS[HELD / "source_ledger.json"],
    "dependency_adapter_sha256": PINS[HELD / "normalize_future_dependency.py"],
    "producer_adapter_tests_sha256": PINS[HELD / "results_adapter_tests.json"],
    "runner_sha256": PINS[HELD / "run_groups138_161.py"],
    "selection": {"group_ids": SELECTED, "count": 24, "strict_order": True, "total_source_bytes": total_bytes},
    "source_regeneration": {"all_24_byte_exact": True, "all_24_census_exact": True, "variables_each": 91, "generators_each": 6577, "sources": source_audit},
    "dependency": {
        "adapter_valid_mock_pass": True,
        "hostile_count": 12,
        "hostile_tests": hostiles,
        "required_union": list(range(138)),
        "future_groups": list(range(88, 138)),
        "future_manifest_sha256": None,
        "future_result_sha256": None,
        "future_files_absent": True,
        "satisfied": False,
    },
    "runner_contract": {
        "native_wall_seconds_each": 240,
        "wrapper_wall_seconds_each": 250,
        "rss_cap_bytes_each": 8589934592,
        "direct_libproc_process_group_rss": True,
        "strict_sequential": True,
        "stop_first": True,
        "atomic_per_lane": True,
        "single_use_exclusive_attempt": True,
        "parallel": False,
        "skip": False,
        "reorder": False,
        "relaunch": False,
    },
    "manifest_counts": manifest_counts,
    "scope": {
        "held_approval_only": True,
        "launch_acceptance_materialized": False,
        "launch_clearance_materialized": False,
        "solver_runs": 0,
        "result_files": 0,
        "groups_newly_closed": 0,
        "mathematical_coverage": False,
    },
}
(HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "sources": 24, "hostiles": 12, "solver_runs": 0}, sort_keys=True))
