#!/usr/bin/env python3
"""Regenerate strict rep1 groups 38..87 from the canonical census; never solve."""
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
NEXT25_HELD = ROOT / "computations/unaudited-codex-n8-x5-rep1-next25-exact-q-held-2026-08-25"
PINS = {
    BASE / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    BASE / "generate_minor_quotient.py": "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    CENSUS_REF / "FINAL_MANIFEST.sha256": "f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a",
    NEXT25_HELD / "MANIFEST.sha256": "79052e97d726b5dfc6bf5c4831af27638548bf5cf3a79ade3948a94059470810",
    NEXT25_HELD / "source_ledger.json": "67376d9ddc96b65f0c34d0f746c85703417d0fb3be88ce5d2cf90a601945c833",
}
SELECTED = tuple(range(38, 88))
ASSUMED_CLOSED = tuple(range(38))


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def atomic_text(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def load_generator():
    spec = importlib.util.spec_from_file_location("sealed_rep1_generator", BASE / "generate_minor_quotient.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chart_dict(value):
    coordinate, p, q, r, kind, s, a, b = value
    return {"coordinate": coordinate, "outside": (p, q), "x_pivot": r, "q_kind": kind, "q_pivot": s, "minor_pair": (a, b)}


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
census = json.loads((CENSUS / "results_canonical_census.json").read_text())
records = census["enumeration"]["records"]
assert [record["group_id"] for record in records] == list(range(162))
assert tuple(record["group_id"] for record in records if record["group_id"] not in ASSUMED_CLOSED)[:50] == SELECTED
minor = load_generator()
base = minor.load_base()
(HERE / "sources").mkdir(exist_ok=True)
lanes = []
for ordinal, gid in enumerate(SELECTED, 1):
    record = records[gid]
    chart = record["canonical_chart"]
    program = minor.build_program(base, chart_dict(chart), "0")
    payload = program.encode()
    assert hashlib.sha256(payload).hexdigest() == record["exact_Q_source_sha256"]
    assert len(payload) == record["exact_Q_source_bytes"]
    assert program.count("ring r=0,") == 1
    assert program.count("ideal G=slimgb(I);") == 1
    assert program.count("poly remainder=reduce(1,G);") == 1
    assert program.count("quit;") == 1
    path = HERE / "sources" / f"rep1_group{gid:03d}_Q.sing"
    atomic_text(path, program)
    assert sha256(path) == record["exact_Q_source_sha256"]
    lanes.append({
        "ordinal": ordinal, "group_id": gid, "canonical_chart": chart,
        "source_path": str(path.relative_to(HERE)), "source_sha256": sha256(path),
        "source_bytes": path.stat().st_size, "variables": 91, "generators": 6577,
    })
ledger = {
    "schema": "KRENN_X5_REP1_NEXT50_EXACT_Q_CONDITIONAL_SOURCE_LEDGER_V1",
    "status": "PASS_REGENERATED_SOURCES_ZERO_SOLVES_CONDITIONAL_ON_NEXT25",
    "selection": {
        "assumed_closed_group_ids": list(ASSUMED_CLOSED),
        "dependency": "future exact next25 terminal referee PASS",
        "rule": "50 lowest canonical group IDs remaining after conditional closure of groups 0..37",
        "selected_group_ids": list(SELECTED),
    },
    "lanes": lanes,
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "scope": {"source_files_materialized": 50, "solver_launches": 0, "results_materialized": 0, "clearances_materialized": 0, "mathematical_coverage": False},
}
atomic_text(HERE / "source_ledger.json", json.dumps(ledger, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": ledger["status"], "groups": list(SELECTED), "source_ledger_sha256": sha256(HERE / "source_ledger.json"), "total_bytes": sum(lane["source_bytes"] for lane in lanes)}, sort_keys=True))
