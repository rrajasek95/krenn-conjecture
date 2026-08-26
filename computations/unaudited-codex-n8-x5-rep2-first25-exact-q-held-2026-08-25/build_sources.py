#!/usr/bin/env python3
"""Regenerate the authoritative rep2 162-group census and first strict Q batch; never solve."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"
DESIGN_REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-contraction-modular-held-referee-2026-08-25"
CLOSED = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25"
CLOSED_REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-second-referee-2026-08-25"
PINS = {
    DESIGN / "MANIFEST.sha256": "ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2",
    DESIGN / "generate_design.py": "ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc",
    DESIGN / "chart_orbit_ledger.json": "dac85725f217b45cbaae7b9b434640309cc5ed6e0b40e846534c8a26409bd4d8",
    DESIGN / "results_rep2_corrected_contraction_design.json": "ed37c2e0da8088e08fb6891e60768d98fbbbf031935f752b4e4af280dfe27b26",
    DESIGN_REF / "FINAL_MANIFEST.sha256": "986f819fcb4bcaa17bebaa60047624b16187f755d94897397acc372db6328692",
    DESIGN_REF / "results_referee.json": "ff67c84c8882f3ee8b404319b737a773ac89dca0977f289f6c119aa0f08c9892",
    CLOSED / "FINAL_MANIFEST.sha256": "c9298394d37022b384e8117280bfcdc39422ca24f57173da699a39dac11fb62a",
    CLOSED / "results_independent_referee.json": "a3d3738b22c98c23ffaad2d5cd6c94b4ad9724acbcfeeebfbe4d89c98b39f39c",
    CLOSED / "rep2_corrected_all_equal_y_Q.sing": "5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf",
    CLOSED_REF / "FINAL_MANIFEST.sha256": "c856fae641e355a94684c1c9304ead831d213ecc90f579c0a751c93002c10562",
    CLOSED_REF / "results_referee.json": "806e5b7b0ef72ca39fe725248cca1055342c0ea64577af6944945ab48702e9a2",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def load_design():
    spec = importlib.util.spec_from_file_location("sealed_rep2_design", DESIGN / "generate_design.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
design_result = json.loads((DESIGN / "results_rep2_corrected_contraction_design.json").read_text())
design_ref = json.loads((DESIGN_REF / "results_referee.json").read_text())
closed = json.loads((CLOSED / "results_independent_referee.json").read_text())
closed_ref = json.loads((CLOSED_REF / "results_referee.json").read_text())
assert design_result["status"] == "PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN"
assert design_result["chart_census"] == {"raw": 972, "S3_orbits": 162, "orbit_size": 6, "y_orbits": 81, "z_orbits": 81}
assert design_ref["design_manifest_sha256"] == PINS[DESIGN / "MANIFEST.sha256"]
assert design_ref["design_result_sha256"] == PINS[DESIGN / "results_rep2_corrected_contraction_design.json"]
assert design_ref["chart_census"] == {"raw": 972, "orbits": 162, "orbit_size": 6, "y_orbits": 81, "z_orbits": 81}
assert closed["status"] == "PASS_EXACT_Q_ONE_REFINED_CHART_ONLY" and closed["same_chart_closed"] is True
assert closed_ref["status"] == "PASS_EXACT_Q_ONE_REFINED_REP2_CHART_ONLY" and closed_ref["unit_ideal"] is True
assert closed_ref["chart"] == closed["chart"] == "all-equal-y/i0/p00/x0/y0/d01"
assert closed_ref["source_sha256"] == closed["source_sha256"] == PINS[CLOSED / "rep2_corrected_all_equal_y_Q.sing"]

module = load_design()
engine = module.load_engine()
module.configure_engine(engine)
raw, groups = engine.orbit_ledger()
ordered = sorted(groups.items())
sealed_ledger = json.loads((DESIGN / "chart_orbit_ledger.json").read_text())
assert len(raw) == 972 and len(ordered) == 162
assert sealed_ledger["raw"] == 972 and len(sealed_ledger["groups"]) == 162
assert [list(rep) for rep, _ in ordered] == [entry["representative"] for entry in sealed_ledger["groups"]]
assert [[list(member) for member in sorted(members)] for _, members in ordered] == [entry["members"] for entry in sealed_ledger["groups"]]

solver_epilogue = """ideal G=slimgb(I);
print(\"GROEBNER_SIZE=\"+string(size(G)));
poly remainder=reduce(1,G);
print(\"UNIT_REMAINDER=\"+string(remainder));
if (remainder==0) { print(\"STATUS=UNIT_IDEAL\"); } else { print(\"STATUS=NONUNIT_OR_UNRESOLVED\"); }
quit;
"""
census = []
for group_id, (representative, members) in enumerate(ordered):
    design_program = module.build_program(engine, representative)
    assert design_program.endswith("quit;\n") and design_program.count("quit;") == 1
    q_program = design_program[:-len("quit;\n")] + solver_epilogue
    census.append({
        "group_id": group_id,
        "canonical_chart": list(representative),
        "family": representative[4],
        "raw_members": [list(member) for member in sorted(members)],
        "raw_member_count": len(members),
        "exact_Q_source_sha256": hashlib.sha256(q_program.encode()).hexdigest(),
        "exact_Q_source_bytes": len(q_program.encode()),
    })

matches = [entry for entry in census if entry["exact_Q_source_sha256"] == closed_ref["source_sha256"]]
assert len(matches) == 1
closed_group = matches[0]
assert closed_group["group_id"] == 0
assert closed_group["canonical_chart"] == [0, 0, 0, 0, "y", 0, 0, 1]
assert closed_group["canonical_chart"] == sealed_ledger["groups"][0]["representative"]

selected = [entry for entry in census if entry["group_id"] != closed_group["group_id"]][:25]
assert [entry["group_id"] for entry in selected] == list(range(1, 26))
lanes = []
for ordinal, entry in enumerate(selected, 1):
    representative = tuple(entry["canonical_chart"])
    design_program = module.build_program(engine, representative)
    q_program = design_program[:-len("quit;\n")] + solver_epilogue
    path = HERE / "sources" / f"rep2_group{entry['group_id']:03d}_Q.sing"
    atomic(path, q_program)
    assert sha256(path) == entry["exact_Q_source_sha256"]
    assert path.stat().st_size == entry["exact_Q_source_bytes"]
    assert q_program.count("ring r=0,") == q_program.count("ideal G=slimgb(I);") == q_program.count("poly remainder=reduce(1,G);") == q_program.count("quit;") == 1
    lanes.append({
        "ordinal": ordinal,
        "group_id": entry["group_id"],
        "canonical_chart": entry["canonical_chart"],
        "family": entry["family"],
        "source_path": str(path.relative_to(HERE)),
        "source_sha256": sha256(path),
        "source_bytes": path.stat().st_size,
        "variables": 91,
        "generators": 6577,
    })

census_result = {
    "schema": "KRENN_X5_REP2_CORRECTED_CANONICAL_162_CENSUS_V1",
    "status": "PASS_REGENERATED_AUTHORITATIVE_972_TO_162_CENSUS",
    "counts": {"raw": 972, "canonical_groups": 162, "members_each": 6, "y_groups": 81, "z_groups": 81},
    "closed_group_identification": {
        "group_id": 0,
        "method": "unique exact-Q source SHA match to independently sealed all-equal-y chart",
        "chart": closed_group["canonical_chart"],
        "source_sha256": closed_group["exact_Q_source_sha256"],
        "first_seal_manifest_sha256": PINS[CLOSED / "FINAL_MANIFEST.sha256"],
        "second_referee_manifest_sha256": PINS[CLOSED_REF / "FINAL_MANIFEST.sha256"],
    },
    "groups": census,
}
atomic(HERE / "canonical_census.json", json.dumps(census_result, indent=2, sort_keys=True) + "\n")
ledger = {
    "schema": "KRENN_X5_REP2_FIRST25_EXACT_Q_SOURCE_LEDGER_V1",
    "status": "PASS_REGENERATED_SOURCES_ZERO_SOLVES",
    "selection": {
        "excluded_proven_group_ids": [0],
        "rule": "25 lowest canonical group IDs after excluding exactly the sealed all-equal-y group",
        "selected_group_ids": list(range(1, 26)),
    },
    "closed_dependency": census_result["closed_group_identification"],
    "lanes": lanes,
    "canonical_census": {"path": "canonical_census.json", "sha256": sha256(HERE / "canonical_census.json")},
    "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    "scope": {"source_files_materialized": 25, "solver_launches": 0, "results_materialized": 0, "clearances_materialized": 0, "mathematical_coverage_added": False, "rep2_closed": False},
}
atomic(HERE / "source_ledger.json", json.dumps(ledger, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": ledger["status"], "closed_group": 0, "selected": list(range(1, 26)), "census_sha256": sha256(HERE / "canonical_census.json"), "ledger_sha256": sha256(HERE / "source_ledger.json"), "bytes": sum(lane["source_bytes"] for lane in lanes)}, sort_keys=True))
