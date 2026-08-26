#!/usr/bin/env python3
"""Fail-closed small-artifact validator; no Singular invocation."""
import hashlib
import json
from collections import Counter
from pathlib import Path

H = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


r = json.loads((H / "results_referee.json").read_text())
assert r["status"] == "PASS_EXACT_16_CHART_TORUS_COVER_REFEREE_ZERO_SOLVES"
assert r["producer"] == {
    "manifest_sha256": "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e",
    "result_sha256": "9a42d532e2b007001d0411e470867fc31195ceb67d39633dd1a6da9bee83d916",
    "manifest_entries_replayed": r["producer"]["manifest_entries_replayed"],
}
assert r["original"]["variables"] == 84 and r["original"]["generators"] == 6562
assert r["original"]["ring_transport_byte_exact"]
grading = r["grading"]
assert (grading["rank"], grading["nullity"], grading["constraint_count"]) == (74, 10, 11954)
assert grading["selected_minor_determinant"] == 1 and grading["saturation_character_zero"]
gauge = r["global_gauge"]
assert gauge["unit_count"] == 6 and gauge["unimodular"] and gauge["root_free_parameter_formulas_verified"]
assert gauge["saturation_forces_b2_one"] and (gauge["variables_after"], gauge["generators_after"]) == (77, 6561)
assert gauge["all_removed_identifiers_absent"] and gauge["all_generators_unique_nontrivial"]
cover = r["residual_cover"]
assert cover["primitive_character_matrix"] == [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
assert (cover["chart_count"], cover["variables_each"], cover["generators_each"]) == (16, 73, 6561)
assert len(cover["sources"]) == 16
assert Counter(tuple(source["assignment"][name] for name in cover["primitive_coordinates"]) for source in cover["sources"]) == Counter({bits: 1 for bits in __import__("itertools").product((0, 1), repeat=4)})
assert cover["all_assignments_present_once"] and cover["all_sources_byte_rebuilt"]
assert cover["all_removed_identifiers_absent"] and cover["all_generators_unique_nontrivial"]
assert r["hostiles"] == {"count": 14, "mutation_list_recounted": 14, "all_pass": True, "solver_runs": 0}
timeout = r["timeout_binding"]
assert timeout["termination"] == "NATIVE_WALL_CAP_300" and timeout["attempt_consumed"]
assert timeout["mathematical_coverage"] is False and timeout["reuse_or_relaunch_authorized"] is False
assert r["scope"] == {"design_referee_only": True, "singular_runs": 0, "ideal_runs": 0, "chart_closed": False, "rep5_closed": False, "pilot_launch_authorized": False}
assert not list(H.rglob("*.tmp")) and not list(H.rglob("__pycache__"))
if (H / "MANIFEST.sha256").exists():
    for line in (H / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (H / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest, (path, digest, sha(path))
print(json.dumps({"status": "PASS_REP5_TORUS_COVER_REFEREE_VALIDATED", "grading": [74, 10], "charts": 16, "shape": [73, 6561], "solver_runs": 0}, sort_keys=True))
