#!/usr/bin/env python3
"""Exact D(a04_11)/V(a04_11) split of the residual a57_01=0 chart."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/analyze.py"
TEMPLATE_MANIFEST = TEMPLATE.parent / "MANIFEST.sha256"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Vt1Vt2Dt0-residual-torus-design-2026-08-26"
SOURCE = PARENT / "sources/rep2_group16_Dt1_a57_01_V0_Q_design.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(TEMPLATE_MANIFEST) == "aab19d2f51693fed67f587d83fe0d2e108888d626d788e4d00a9362a3be978be"
assert sha(PARENT / "MANIFEST.sha256") == "0b355f51e249d82b8a1aea45687a8a6b6ebaab83fd5256e541d9acf7985d1bba"
assert sha(SOURCE) == "15ee90435e4f6148c708525b757de4f8b6ff9a1aba0a66fc2402b8846ffb964c"

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
    'SOURCE = UPSTREAM / "sources/rep2_group16_Dt1_a57_01_V0_Q_design.sing"',
    1,
)
program = program.replace(
    'SOURCE_SHA = "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244"',
    'SOURCE_SHA = "15ee90435e4f6148c708525b757de4f8b6ff9a1aba0a66fc2402b8846ffb964c"',
    1,
)
program = program.replace('assert sha(UPSTREAM / "results/lane2_Dt1.json") == TIMEOUT_RESULT_SHA', "", 1)
program = program.replace('assert sha(UPSTREAM / "TERMINAL_MANIFEST.sha256") == TIMEOUT_MANIFEST_SHA', "", 1)
program = program.replace(
    "assert len(variables) == 64 and len(equations) == len(set(equations)) == 6569",
    "assert len(variables) == 60 and len(equations) == len(set(equations)) == 6568",
    1,
)
program = program.replace(
    "objective, basis_index, position = min(candidates)",
    'objective, basis_index, position = next(item for item in candidates if variables[item[2]] == "a04_11")',
    1,
)
program = program.replace(
    '"timeout_binding": {"result_sha256": sha(UPSTREAM / "results/lane2_Dt1.json"), "terminal_manifest_sha256": sha(UPSTREAM / "TERMINAL_MANIFEST.sha256"), "rerun": False},',
    '"timeout_binding": {"result_sha256": "not_applicable", "terminal_manifest_sha256": "not_applicable", "rerun": False},',
    1,
)

namespace = {"__name__": "__rep2_a04_11_exact_analyzer__", "__file__": str(HERE / "_pinned_template_replay.py")}
exec(compile(program, namespace["__file__"], "exec"), namespace)

variables = namespace["variables"]
polynomials = namespace["polynomials"]
position = variables.index("a04_11")
complete_factor_count = sum(
    1 for polynomial in polynomials if all(position in monomial for monomial in polynomial)
)
assert complete_factor_count == 504

result_path = HERE / "results_design.json"
result = json.loads(result_path.read_text())
assert result["status"] == "PASS_EXACT_PRIMITIVE_TORUS_DV_COVER"
assert result["cover"]["selected"]["coordinate"] == "a04_11"
result["schema"] = "KRENN_X5_REP2_GROUP16_A57V0_A04_11_RESIDUAL_SPLIT_DESIGN_V1"
result.pop("timeout_binding")
result["parent_binding"] = {
    "manifest_sha256": sha(PARENT / "MANIFEST.sha256"),
    "source_sha256": sha(SOURCE),
    "parent_branch": "V(a57_01)",
    "parent_chart_previously_launched": False,
}
result["factor_census"] = {
    "coordinate": "a04_11",
    "source_generators_divisible_by_coordinate": complete_factor_count,
    "source_generators": len(polynomials),
}
result["global_cover_update"] = {
    "parent_identity": "D(a57_01) union V(a57_01)",
    "refined_identity": [
        "D(a57_01)",
        "V(a57_01) intersection D(a04_11)",
        "V(a57_01,a04_11)",
    ],
    "leaf_count_before": 2,
    "leaf_count_after": 3,
    "exhaustive": True,
}
result["conclusion"] = {
    "singular_runs": 0,
    "mathematical_coverage": False,
    "exhaustive_two_chart_refinement": True,
    "parent_chart_previously_launched": False,
}
temporary = result_path.with_suffix(".json.tmp")
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, result_path)
print(json.dumps({
    "status": result["status"],
    "selected": result["cover"]["selected"],
    "factor_count": complete_factor_count,
    "sources": [
        [source["branch"], source["variables"], source["generators"], source["total_terms"]]
        for source in result["cover"]["sources"]
    ],
    "solver_runs": 0,
}, sort_keys=True))
