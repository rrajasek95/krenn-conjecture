#!/usr/bin/env python3
"""Exact grading/linear/factor census and next reversible cover of the strict leaf."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/analyze.py"
TEMPLATE_MANIFEST = TEMPLATE.parent / "MANIFEST.sha256"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11-residual-split-design-2026-08-26"
SOURCE = PARENT / "sources/rep2_group16_Dt1_a04_11_V0_Q_design.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(TEMPLATE_MANIFEST) == "aab19d2f51693fed67f587d83fe0d2e108888d626d788e4d00a9362a3be978be"
assert sha(PARENT / "MANIFEST.sha256") == "8c4b3e4c82076e7cd8b61cd40e86eaa8a8ea3bd10ace7c1f8ac7f8c4ce52b835"
assert sha(SOURCE) == "f0bae713992e827d827fd3d6998710cb8e602a607f19ee379d775ee0032294ea"

program = TEMPLATE.read_text()
program = program.replace("HERE = Path(__file__).resolve().parent", f"HERE = Path({str(HERE)!r})", 1)
program = program.replace("ROOT = HERE.parents[1]", f"ROOT = Path({str(ROOT)!r})", 1)
program = program.replace(
    'UPSTREAM = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"',
    f"UPSTREAM = Path({str(PARENT)!r})",
    1,
)
program = program.replace(
    'SOURCE = UPSTREAM / "sources/rep2_group016_67_Dt1_runtime_Q.sing"',
    'SOURCE = UPSTREAM / "sources/rep2_group16_Dt1_a04_11_V0_Q_design.sing"',
    1,
)
program = program.replace(
    'SOURCE_SHA = "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244"',
    'SOURCE_SHA = "f0bae713992e827d827fd3d6998710cb8e602a607f19ee379d775ee0032294ea"',
    1,
)
program = program.replace('assert sha(UPSTREAM / "results/lane2_Dt1.json") == TIMEOUT_RESULT_SHA', "", 1)
program = program.replace('assert sha(UPSTREAM / "TERMINAL_MANIFEST.sha256") == TIMEOUT_MANIFEST_SHA', "", 1)
program = program.replace(
    "assert len(variables) == 64 and len(equations) == len(set(equations)) == 6569",
    "assert len(variables) == 59 and len(equations) == len(set(equations)) == 6064",
    1,
)
program = program.replace(
    '"timeout_binding": {"result_sha256": sha(UPSTREAM / "results/lane2_Dt1.json"), "terminal_manifest_sha256": sha(UPSTREAM / "TERMINAL_MANIFEST.sha256"), "rerun": False},',
    '"timeout_binding": {"result_sha256": "not_applicable", "terminal_manifest_sha256": "not_applicable", "rerun": False},',
    1,
)

namespace = {"__name__": "__rep2_strict_leaf_exact_analyzer__", "__file__": str(HERE / "_pinned_template_replay.py")}
exec(compile(program, namespace["__file__"], "exec"), namespace)

variables = namespace["variables"]
polynomials = namespace["polynomials"]
factor_census = []
for position, variable in enumerate(variables):
    complete = sum(1 for polynomial in polynomials if all(position in monomial for monomial in polynomial))
    containing = sum(1 for polynomial in polynomials if any(position in monomial for monomial in polynomial))
    factor_census.append({"coordinate": variable, "complete_factor_generators": complete, "containing_generators": containing})
factor_census.sort(key=lambda record: (-record["complete_factor_generators"], -record["containing_generators"], record["coordinate"]))

result_path = HERE / "results_design.json"
result = json.loads(result_path.read_text())
assert result["status"] in ("PASS_EXACT_PRIMITIVE_TORUS_DV_COVER", "PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE")
result["schema"] = "KRENN_X5_REP2_GROUP16_A57V0_A04_11V0_NEXT_COVER_DESIGN_V1"
result.pop("timeout_binding")
result["parent_binding"] = {
    "manifest_sha256": sha(PARENT / "MANIFEST.sha256"),
    "source_sha256": sha(SOURCE),
    "parent_branch": "V(a57_01,a04_11)",
    "parent_chart_previously_launched": False,
}
result["factor_census"] = {
    "coordinates": factor_census,
    "positive_complete_factor_coordinates": sum(record["complete_factor_generators"] > 0 for record in factor_census),
    "maximum_complete_factor_generators": factor_census[0]["complete_factor_generators"],
}
selected_coordinate = result["cover"]["selected"]["coordinate"]
result["global_cover_update"] = {
    "previous_leaves": [
        "D(a57_01)",
        "V(a57_01) intersection D(a04_11)",
        "V(a57_01,a04_11)",
    ],
    "refined_leaf": "V(a57_01,a04_11)",
    "replacement": [
        f"V(a57_01,a04_11) intersection D({selected_coordinate})",
        f"V(a57_01,a04_11,{selected_coordinate})",
    ],
    "leaf_count_before": 3,
    "leaf_count_after": 4,
    "exhaustive": True,
}
result["conclusion"] = {
    "singular_runs": 0,
    "mathematical_coverage": False,
    "exact_reversible_next_cover": True,
    "parent_chart_previously_launched": False,
}
temporary = result_path.with_suffix(".json.tmp")
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, result_path)
print(json.dumps({
    "status": result["status"],
    "grading": [result["grading"]["rank"], result["grading"]["nullity"]],
    "linear": {
        "monic": len(result["linear_census"]["unit_coefficient_graph_substitutions"]),
        "affine_rank": result["linear_census"]["affine_linear_rank"],
        "all_linear_rank": result["linear_census"]["all_linear_part_rank"],
    },
    "top_factors": factor_census[:6],
    "selected": result["cover"]["selected"],
    "sources": [[source["branch"], source["variables"], source["generators"], source["total_terms"]] for source in result["cover"]["sources"]],
    "solver_runs": 0,
}, sort_keys=True))
