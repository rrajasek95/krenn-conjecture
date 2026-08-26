#!/usr/bin/env python3
"""Regenerate canonical exact-Q sources for conditional rep1 groups 88..137."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
CENSUS_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25"
CLOSED37 = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25"
PINS = {
    BASE / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    BASE / "generate_minor_quotient.py": "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    CENSUS_REF / "FINAL_MANIFEST.sha256": "f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a",
    CLOSED37 / "MANIFEST.sha256": "7b66f582d1edf79e1e75c4ca328808f3f77548f840f5c42cc082dcd0f53764da",
    CLOSED37 / "normalized_next25_dependency.json": "29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76",
}
SELECTED = tuple(range(88, 138))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_text(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def chart_dict(value):
    coordinate, p, q, r, kind, s, a, b = value
    return {"coordinate": coordinate, "outside": (p, q), "x_pivot": r, "q_kind": kind, "q_pivot": s, "minor_pair": (a, b)}


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
closed37 = json.loads((CLOSED37 / "normalized_next25_dependency.json").read_text())
assert closed37["closed_union"] == list(range(38))
spec = importlib.util.spec_from_file_location("sealed_rep1_generator", BASE / "generate_minor_quotient.py")
assert spec and spec.loader
minor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(minor)
base = minor.load_base()
census = json.loads((CENSUS / "results_canonical_census.json").read_text())
records = census["enumeration"]["records"]
assert [record["group_id"] for record in records] == list(range(162))
assert tuple(record["group_id"] for record in records if record["group_id"] not in tuple(range(88)))[:50] == SELECTED
(HERE / "sources").mkdir(exist_ok=True)
lanes = []
for ordinal, gid in enumerate(SELECTED, 1):
    record = records[gid]
    chart = record["canonical_chart"]
    program = minor.build_program(base, chart_dict(chart), "0")
    payload = program.encode()
    assert hashlib.sha256(payload).hexdigest() == record["exact_Q_source_sha256"]
    assert len(payload) == record["exact_Q_source_bytes"]
    assert program.count("ring r=0,") == program.count("ideal G=slimgb(I);") == program.count("poly remainder=reduce(1,G);") == program.count("quit;") == 1
    path = HERE / "sources" / f"rep1_group{gid:03d}_Q.sing"
    atomic_text(path, program)
    assert sha256(path) == record["exact_Q_source_sha256"]
    lanes.append({"ordinal": ordinal, "group_id": gid, "canonical_chart": chart, "source_path": str(path.relative_to(HERE)), "source_sha256": sha256(path), "source_bytes": path.stat().st_size, "variables": 91, "generators": 6577})
ledger = {
    "schema": "KRENN_X5_REP1_GROUPS88_137_EXACT_Q_CONDITIONAL_SOURCE_LEDGER_V1",
    "status": "PASS_REGENERATED_50_SOURCES_ZERO_SOLVES_CONDITIONAL_ON_GROUPS38_87",
    "selection": {"proven_closed_group_ids": list(range(38)), "conditionally_closed_group_ids": list(range(38, 88)), "required_closed_union": list(range(88)), "rule": "50 lowest group IDs after conditional closure 0..87", "selected_group_ids": list(SELECTED)},
    "lanes": lanes,
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "scope": {"source_files_materialized": 50, "solver_launches": 0, "results_materialized": 0, "clearances_materialized": 0, "mathematical_coverage": False},
}
atomic_text(HERE / "source_ledger.json", json.dumps(ledger, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": ledger["status"], "groups": list(SELECTED), "source_ledger_sha256": sha256(HERE / "source_ledger.json"), "total_bytes": sum(lane["source_bytes"] for lane in lanes)}, sort_keys=True))
