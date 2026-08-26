#!/usr/bin/env python3
"""Exact graph elimination followed by grading/factor census and D/V cover."""
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
INTERMEDIATE = HERE / "intermediate/rep2_group16_a57V0_a04_11V0_a26_00_GRAPH_ELIMINATED_Q_design.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(TEMPLATE_MANIFEST) == "aab19d2f51693fed67f587d83fe0d2e108888d626d788e4d00a9362a3be978be"
assert sha(PARENT / "MANIFEST.sha256") == "8c4b3e4c82076e7cd8b61cd40e86eaa8a8ea3bd10ace7c1f8ac7f8c4ce52b835"
assert sha(SOURCE) == "f0bae713992e827d827fd3d6998710cb8e602a607f19ee379d775ee0032294ea"


def pinned_program(source: Path, variable_count: int, generator_count: int, output_here: Path) -> str:
    program = TEMPLATE.read_text()
    program = program.replace("HERE = Path(__file__).resolve().parent", f"HERE = Path({str(output_here)!r})", 1)
    program = program.replace("ROOT = HERE.parents[1]", f"ROOT = Path({str(ROOT)!r})", 1)
    program = program.replace(
        'UPSTREAM = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"',
        f"UPSTREAM = Path({str(source.parent)!r})",
        1,
    )
    program = program.replace(
        'SOURCE = UPSTREAM / "sources/rep2_group016_67_Dt1_runtime_Q.sing"',
        f"SOURCE = Path({str(source)!r})",
        1,
    )
    program = program.replace(
        'SOURCE_SHA = "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244"',
        f'SOURCE_SHA = "{sha(source)}"',
        1,
    )
    program = program.replace('assert sha(UPSTREAM / "results/lane2_Dt1.json") == TIMEOUT_RESULT_SHA', "", 1)
    program = program.replace('assert sha(UPSTREAM / "TERMINAL_MANIFEST.sha256") == TIMEOUT_MANIFEST_SHA', "", 1)
    program = program.replace(
        "assert len(variables) == 64 and len(equations) == len(set(equations)) == 6569",
        f"assert len(variables) == {variable_count} and len(equations) == len(set(equations)) == {generator_count}",
        1,
    )
    program = program.replace(
        '"timeout_binding": {"result_sha256": sha(UPSTREAM / "results/lane2_Dt1.json"), "terminal_manifest_sha256": sha(UPSTREAM / "TERMINAL_MANIFEST.sha256"), "rerun": False},',
        '"timeout_binding": {"result_sha256": "not_applicable", "terminal_manifest_sha256": "not_applicable", "rerun": False},',
        1,
    )
    return program


# First replay the strict parent exactly.  The template also emits a provisional
# cover, which the second pass deletes and replaces after graph elimination.
first_namespace = {"__name__": "__rep2_strict_graph_input__", "__file__": str(HERE / "_strict_input_replay.py")}
exec(compile(pinned_program(SOURCE, 59, 6064, HERE), first_namespace["__file__"], "exec"), first_namespace)
variables: list[str] = first_namespace["variables"]
polynomials = first_namespace["polynomials"]
add = first_namespace["add"]
multiply = first_namespace["multiply"]
serialize = first_namespace["serialize"]

graph_position = variables.index("a26_00")
partner_left = variables.index("a26_02")
partner_right = variables.index("a57_02")
graph_candidates = [
    record for record in first_namespace["monic_candidates"]
    if record["variable"] == "a26_00"
]
assert graph_candidates == [{"equation": 6063, "variable": "a26_00", "coefficient": -1, "terms": 3}]
graph = polynomials[6063]
assert graph == {(): -1, (graph_position,): -1, tuple(sorted((partner_left, partner_right))): -1}
replacement = {(): -1, tuple(sorted((partner_left, partner_right))): -1}


def substitute_graph(polynomial):
    reduced = {}
    for monomial, coefficient in polynomial.items():
        exponent = monomial.count(graph_position)
        base = {tuple(position for position in monomial if position != graph_position): coefficient}
        term = base
        for _ in range(exponent):
            term = multiply(term, replacement)
        reduced = add(reduced, term)
    return reduced


eliminated = []
seen = set()
for equation_index, polynomial in enumerate(polynomials):
    if equation_index == 6063:
        continue
    reduced = substitute_graph(polynomial)
    assert reduced
    if len(reduced) == 1 and () in reduced:
        raise AssertionError("graph elimination produced the unit ideal")
    key = tuple(sorted(reduced.items()))
    if key not in seen:
        seen.add(key)
        eliminated.append(reduced)
remaining = [position for position in range(len(variables)) if position != graph_position]
intermediate_program = "\n".join((
    "// EXACT Q DESIGN INPUT ONLY: no solver run authorized.",
    "// Exact graph elimination a26_00=-1-a26_02*a57_02.",
    "option(noredefine);",
    f"ring r=0,({','.join(variables[position] for position in remaining)}),dp;",
    "ideal I=" + ",\n".join(serialize(polynomial) for polynomial in eliminated) + ";",
    'print("INPUT_VARIABLES="+string(nvars(r)));',
    'print("INPUT_GENERATORS="+string(size(I)));',
    "quit;",
    "",
))
INTERMEDIATE.parent.mkdir(exist_ok=True)
temporary = INTERMEDIATE.with_suffix(".sing.tmp")
temporary.write_text(intermediate_program)
os.replace(temporary, INTERMEDIATE)

# Replay the eliminated source from scratch before selecting the smallest exact
# primitive torus D/V refinement.
second_namespace = {"__name__": "__rep2_strict_graph_eliminated__", "__file__": str(HERE / "_eliminated_replay.py")}
exec(compile(pinned_program(INTERMEDIATE, 58, len(eliminated), HERE), second_namespace["__file__"], "exec"), second_namespace)
reduced_variables = second_namespace["variables"]
reduced_polynomials = second_namespace["polynomials"]
factor_census = []
for position, variable in enumerate(reduced_variables):
    complete = sum(1 for polynomial in reduced_polynomials if all(position in monomial for monomial in polynomial))
    containing = sum(1 for polynomial in reduced_polynomials if any(position in monomial for monomial in polynomial))
    factor_census.append({"coordinate": variable, "complete_factor_generators": complete, "containing_generators": containing})
factor_census.sort(key=lambda record: (-record["complete_factor_generators"], -record["containing_generators"], record["coordinate"]))

result_path = HERE / "results_design.json"
result = json.loads(result_path.read_text())
assert result["status"] == "PASS_EXACT_PRIMITIVE_TORUS_DV_COVER"
result["schema"] = "KRENN_X5_REP2_GROUP16_A57V0_A04_11V0_MONIC_NEXT_COVER_DESIGN_V1"
result.pop("timeout_binding")
result["original_parent_binding"] = {
    "manifest_sha256": sha(PARENT / "MANIFEST.sha256"),
    "source_sha256": sha(SOURCE),
    "parent_branch": "V(a57_01,a04_11)",
    "parent_chart_previously_launched": False,
}
result["graph_elimination"] = {
    "equation_index_zero_based": 6063,
    "equation": "-1-a26_00-a26_02*a57_02",
    "substitution": "a26_00=-1-a26_02*a57_02",
    "unit_coefficient": -1,
    "forward_reverse_exact": True,
    "source_variables_before_after": [59, 58],
    "source_generators_before_after": [6064, len(eliminated)],
    "source_terms_before_after": [sum(map(len, polynomials)), sum(map(len, eliminated))],
    "intermediate_path": str(INTERMEDIATE.relative_to(HERE)),
    "intermediate_sha256": sha(INTERMEDIATE),
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
    "exact_graph_isomorphism_first": "a26_00=-1-a26_02*a57_02",
    "empty_open_branch": f"V(a57_01,a04_11) intersection D({selected_coordinate})",
    "replacement_nonempty_leaf": f"V(a57_01,a04_11,{selected_coordinate})",
    "forced_zero": f"{selected_coordinate}=0",
    "leaf_count_before": 3,
    "leaf_count_after": 3,
    "exhaustive": True,
}
result["conclusion"] = {
    "singular_runs": 0,
    "mathematical_coverage": False,
    "exact_graph_elimination": True,
    "exact_reversible_next_cover": True,
    "open_branch_structural_unit_ideal": True,
    "forced_zero_reduction": f"{selected_coordinate}=0",
    "parent_chart_previously_launched": False,
}
temporary = result_path.with_suffix(".json.tmp")
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, result_path)
print(json.dumps({
    "status": result["status"],
    "graph": result["graph_elimination"],
    "grading": [result["grading"]["rank"], result["grading"]["nullity"]],
    "linear": {
        "monic_after": len(result["linear_census"]["unit_coefficient_graph_substitutions"]),
        "affine_rank": result["linear_census"]["affine_linear_rank"],
        "all_linear_rank": result["linear_census"]["all_linear_part_rank"],
    },
    "top_factors": factor_census[:6],
    "selected": result["cover"]["selected"],
    "sources": [[source["branch"], source["variables"], source["generators"], source["total_terms"]] for source in result["cover"]["sources"]],
    "solver_runs": 0,
}, sort_keys=True))
