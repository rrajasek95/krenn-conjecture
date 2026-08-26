#!/usr/bin/env python3
"""Exhaust exact monic graphs and torus gauges on the strict rep2 survivor."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/analyze.py"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11-residual-split-design-2026-08-26"
SOURCE = PARENT / "sources/rep2_group16_Dt1_a04_11_D1_Q_design.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(TEMPLATE.parent / "MANIFEST.sha256") == "aab19d2f51693fed67f587d83fe0d2e108888d626d788e4d00a9362a3be978be"
assert sha(PARENT / "MANIFEST.sha256") == "8c4b3e4c82076e7cd8b61cd40e86eaa8a8ea3bd10ace7c1f8ac7f8c4ce52b835"
assert sha(SOURCE) == "2998353c04d390b7dadae6a2bb364d5ad9866b1911d39dfb9f039b40cef70bab"

Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(sorted(lm + rm))
            result[monomial] = result.get(monomial, 0) + lc * rc
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


class Parser:
    def __init__(self, expression: str, index: dict[str, int]):
        self.tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]", expression)
        self.cursor = 0
        self.index = index

    def expression(self) -> Polynomial:
        value = self.term()
        while self.cursor < len(self.tokens) and self.tokens[self.cursor] in ("+", "-"):
            sign = 1 if self.tokens[self.cursor] == "+" else -1
            self.cursor += 1
            term = self.term()
            if sign < 0:
                term = {monomial: -coefficient for monomial, coefficient in term.items()}
            value = add(value, term)
        return value

    def term(self) -> Polynomial:
        value = self.factor()
        while self.cursor < len(self.tokens) and self.tokens[self.cursor] == "*":
            self.cursor += 1
            value = multiply(value, self.factor())
        return value

    def factor(self) -> Polynomial:
        token = self.tokens[self.cursor]
        if token == "-":
            self.cursor += 1
            return {monomial: -coefficient for monomial, coefficient in self.factor().items()}
        if token == "(":
            self.cursor += 1
            value = self.expression()
            assert self.tokens[self.cursor] == ")"
            self.cursor += 1
            return value
        self.cursor += 1
        if token.isdigit():
            value = int(token)
            return {} if value == 0 else {(): value}
        return {(self.index[token],): 1}


def parse_program(path: Path) -> tuple[list[str], list[Polynomial]]:
    text = path.read_text()
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    expressions: list[str] = []
    depth = 0
    start = 0
    for position, character in enumerate(body):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            expressions.append(body[start:position].strip())
            start = position + 1
    expressions.append(body[start:].strip())
    assert depth == 0 and len(expressions) == len(set(expressions))
    index = {variable: position for position, variable in enumerate(variables)}
    polynomials: list[Polynomial] = []
    for expression in expressions:
        parser = Parser(expression, index)
        polynomial = parser.expression()
        assert parser.cursor == len(parser.tokens) and polynomial
        polynomials.append(polynomial)
    return variables, polynomials


def serialize(polynomial: Polynomial, variables: list[str]) -> str:
    pieces = []
    for monomial, coefficient in sorted(polynomial.items(), key=lambda item: (len(item[0]), item[0])):
        factors = "*".join(variables[position] for position in monomial)
        magnitude = abs(coefficient)
        body = str(magnitude) if not factors else factors if magnitude == 1 else f"{magnitude}*{factors}"
        pieces.append((("-" if coefficient < 0 else "+") if pieces else ("-" if coefficient < 0 else "")) + body)
    return "".join(pieces)


def write_source(path: Path, variables: list[str], polynomials: list[Polynomial], note: str) -> None:
    program = "\n".join((
        "// EXACT Q DESIGN INPUT ONLY: no solver run authorized.",
        f"// {note}",
        "option(noredefine);",
        f"ring r=0,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(serialize(polynomial, variables) for polynomial in polynomials) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".sing.tmp")
    temporary.write_text(program)
    os.replace(temporary, path)


def stats(variables: list[str], polynomials: list[Polynomial]) -> dict:
    return {
        "variables": len(variables),
        "generators": len(polynomials),
        "terms": sum(map(len, polynomials)),
        "maximum_terms": max(map(len, polynomials)),
        "sha256": None,
    }


def deduplicate(polynomials: list[Polynomial]) -> tuple[list[Polynomial], bool]:
    result = []
    seen = set()
    for polynomial in polynomials:
        polynomial = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
        if not polynomial:
            continue
        if len(polynomial) == 1 and () in polynomial:
            return [{(): 1}], True
        key = tuple(sorted(polynomial.items()))
        if key not in seen:
            seen.add(key)
            result.append(polynomial)
    return result, False


def monic_candidates(variables: list[str], polynomials: list[Polynomial]) -> list[tuple]:
    occurrences = [0] * len(variables)
    for polynomial in polynomials:
        for position in {position for monomial in polynomial for position in monomial}:
            occurrences[position] += 1
    candidates = []
    for equation_index, polynomial in enumerate(polynomials):
        for position in range(len(variables)):
            coefficient = polynomial.get((position,), 0)
            if abs(coefficient) != 1:
                continue
            if any(position in monomial for monomial in polynomial if monomial != (position,)):
                continue
            candidates.append((len(polynomial), occurrences[position], variables[position], equation_index, position, coefficient))
    return sorted(candidates)


def eliminate_graph(variables: list[str], polynomials: list[Polynomial], candidate: tuple) -> tuple[list[str], list[Polynomial], dict, bool]:
    _, _, variable, equation_index, position, coefficient = candidate
    graph = polynomials[equation_index]
    rest = {monomial: value for monomial, value in graph.items() if monomial != (position,)}
    replacement = {monomial: -value // coefficient for monomial, value in rest.items()}
    assert all((-value) % coefficient == 0 for value in rest.values())
    transformed = []
    for current_index, polynomial in enumerate(polynomials):
        if current_index == equation_index:
            continue
        reduced: Polynomial = {}
        for monomial, value in polynomial.items():
            exponent = monomial.count(position)
            term: Polynomial = {tuple(entry for entry in monomial if entry != position): value}
            for _ in range(exponent):
                term = multiply(term, replacement)
            reduced = add(reduced, term)
        transformed.append(reduced)
    transformed, unit = deduplicate(transformed)
    remaining_positions = [current for current in range(len(variables)) if current != position]
    remap = {old: new for new, old in enumerate(remaining_positions)}
    remapped = [
        {tuple(remap[entry] for entry in monomial): value for monomial, value in polynomial.items()}
        for polynomial in transformed
    ]
    step = {
        "kind": "forced_zero" if not replacement else "monic_graph",
        "variable": variable,
        "equation_index_zero_based": equation_index,
        "coefficient": coefficient,
        "graph_terms": len(graph),
        "replacement": serialize(replacement, variables) if replacement else "0",
        "unit_after": unit,
    }
    return [variables[position] for position in remaining_positions], remapped, step, unit


def patched_template(source: Path, output_here: Path, variables: int, generators: int) -> str:
    program = TEMPLATE.read_text()
    program = program.replace("HERE = Path(__file__).resolve().parent", f"HERE = Path({str(output_here)!r})", 1)
    program = program.replace("ROOT = HERE.parents[1]", f"ROOT = Path({str(ROOT)!r})", 1)
    program = program.replace('UPSTREAM = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"', f"UPSTREAM = Path({str(source.parent)!r})", 1)
    program = program.replace('SOURCE = UPSTREAM / "sources/rep2_group016_67_Dt1_runtime_Q.sing"', f"SOURCE = Path({str(source)!r})", 1)
    program = program.replace('SOURCE_SHA = "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244"', f'SOURCE_SHA = "{sha(source)}"', 1)
    program = program.replace('assert sha(UPSTREAM / "results/lane2_Dt1.json") == TIMEOUT_RESULT_SHA', "", 1)
    program = program.replace('assert sha(UPSTREAM / "TERMINAL_MANIFEST.sha256") == TIMEOUT_MANIFEST_SHA', "", 1)
    program = program.replace("assert len(variables) == 64 and len(equations) == len(set(equations)) == 6569", f"assert len(variables) == {variables} and len(equations) == len(set(equations)) == {generators}", 1)
    program = program.replace('"timeout_binding": {"result_sha256": sha(UPSTREAM / "results/lane2_Dt1.json"), "terminal_manifest_sha256": sha(UPSTREAM / "TERMINAL_MANIFEST.sha256"), "rerun": False},', '"timeout_binding": {"result_sha256":"na","terminal_manifest_sha256":"na","rerun":False},', 1)
    return program


def factor_census(variables: list[str], polynomials: list[Polynomial]) -> list[dict]:
    records = []
    for position, variable in enumerate(variables):
        complete = sum(all(position in monomial for monomial in polynomial) for polynomial in polynomials)
        containing = sum(any(position in monomial for monomial in polynomial) for polynomial in polynomials)
        records.append({"coordinate": variable, "complete_factor_generators": complete, "containing_generators": containing})
    return sorted(records, key=lambda record: (-record["complete_factor_generators"], -record["containing_generators"], record["coordinate"]))


ledger = []
current = SOURCE
terminal = None
final_probe = None
for cycle in range(32):
    variables, polynomials = parse_program(current)
    before = stats(variables, polynomials)
    before["sha256"] = sha(current)
    candidates = monic_candidates(variables, polynomials)
    if candidates:
        variables, polynomials, step, unit = eliminate_graph(variables, polynomials, candidates[0])
        step_path = HERE / f"intermediate/step{len(ledger)+1:02d}_{step['kind']}_{step['variable']}.sing"
        write_source(step_path, variables, polynomials, f"Exact {step['kind']} elimination of {step['variable']}.")
        after = stats(variables, polynomials)
        after["sha256"] = sha(step_path)
        step.update({"before": before, "after": after, "path": str(step_path.relative_to(HERE))})
        ledger.append(step)
        current = step_path
        if unit:
            terminal = "STRUCTURAL_UNIT_AFTER_GRAPH_ELIMINATION"
            break
        continue

    probe_dir = HERE / f"intermediate/torus_probe_{len(ledger)+1:02d}"
    probe_dir.mkdir(parents=True, exist_ok=True)
    namespace = {"__name__": f"__strict_torus_probe_{cycle}__", "__file__": str(probe_dir / "_replay.py")}
    exec(compile(patched_template(current, probe_dir, len(variables), len(polynomials)), namespace["__file__"], "exec"), namespace)
    probe = json.loads((probe_dir / "results_design.json").read_text())
    final_probe = probe
    sources = probe["cover"]["sources"]
    status = probe["status"]
    if status == "PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE":
        assert len(sources) == 1 and sources[0]["unit_ideal_structural"] is False
        selected_source = probe_dir / sources[0]["path"]
        step_path = HERE / f"intermediate/step{len(ledger)+1:02d}_global_unit_gauge.sing"
        shutil.copyfile(selected_source, step_path)
        ledger.append({
            "kind": "global_unit_torus_gauge",
            "coordinates": probe["cover"]["maximal_primitive_global_gauge_coordinates"],
            "assignments": probe["cover"]["global_gauge_assignments_including_inverse_partners"],
            "grading_rank_nullity": [probe["grading"]["rank"], probe["grading"]["nullity"]],
            "before": before,
            "after": {**stats(*parse_program(step_path)), "sha256": sha(step_path)},
            "path": str(step_path.relative_to(HERE)),
        })
        current = step_path
        continue
    if status == "PASS_EXACT_PRIMITIVE_TORUS_DV_COVER":
        unit_sources = [source for source in sources if source["unit_ideal_structural"]]
        nonunit_sources = [source for source in sources if not source["unit_ideal_structural"]]
        if len(unit_sources) == 1 and len(nonunit_sources) == 1:
            selected_source = probe_dir / nonunit_sources[0]["path"]
            coordinate = probe["cover"]["selected"]["coordinate"]
            forced_value = 0 if unit_sources[0]["branch"] == "D1" else "nonzero"
            step_path = HERE / f"intermediate/step{len(ledger)+1:02d}_torus_forced_{coordinate}_{forced_value}.sing"
            shutil.copyfile(selected_source, step_path)
            ledger.append({
                "kind": "torus_forced_value",
                "coordinate": coordinate,
                "primitive_weight": probe["cover"]["selected"]["weight"],
                "empty_branch": unit_sources[0]["branch"],
                "forced_value": forced_value,
                "grading_rank_nullity": [probe["grading"]["rank"], probe["grading"]["nullity"]],
                "before": before,
                "after": {**stats(*parse_program(step_path)), "sha256": sha(step_path)},
                "path": str(step_path.relative_to(HERE)),
            })
            current = step_path
            continue
        if len(unit_sources) == 2:
            terminal = "STRUCTURAL_UNIT_BOTH_TORUS_BRANCHES"
            break
        terminal = "HELD_EXACT_TWO_BRANCH_PRIMITIVE_TORUS_COVER"
        (HERE / "sources").mkdir(exist_ok=True)
        for source in sources:
            source_path = probe_dir / source["path"]
            held_path = HERE / f"sources/held_{source['branch']}_{probe['cover']['selected']['coordinate']}.sing"
            shutil.copyfile(source_path, held_path)
            source["held_path"] = str(held_path.relative_to(HERE))
            source["held_sha256"] = sha(held_path)
        break
    assert status == "PASS_EXACT_CENSUS_NO_PRIMITIVE_TORUS_COVER"
    terminal = "HELD_NO_FURTHER_MONIC_OR_PRIMITIVE_TORUS_REDUCTION"
    break
else:
    raise AssertionError("reduction cycle limit exceeded")

assert terminal is not None
final_variables, final_polynomials = parse_program(current)
final_stats = stats(final_variables, final_polynomials)
final_stats["sha256"] = sha(current)
final_stats["path"] = str(current.relative_to(HERE)) if current.is_relative_to(HERE) else str(current.relative_to(ROOT))
factors = factor_census(final_variables, final_polynomials)
result = {
    "schema": "KRENN_X5_REP2_GROUP16_A57V0_A04_11D1_EXHAUSTIVE_REDUCTION_V1",
    "status": terminal,
    "parent": {
        "manifest_sha256": sha(PARENT / "MANIFEST.sha256"),
        "source_sha256": sha(SOURCE),
        "source_shape": [59, 6568, 174407],
        "branch": "V(a57_01) intersection D(a04_11)",
    },
    "ledger": ledger,
    "final": final_stats,
    "final_factor_census": factors,
    "final_linear_candidates": monic_candidates(final_variables, final_polynomials),
    "final_probe": final_probe,
    "global_cover": {
        "unchanged_leaves": ["D(a57_01)"],
        "refined_strict_leaf": "V(a57_01) intersection D(a04_11)",
        "terminal_status": terminal,
        "strict_leaf_closed": terminal.startswith("STRUCTURAL_UNIT"),
        "nonempty_leaf_count_before_after": [2, 1] if terminal.startswith("STRUCTURAL_UNIT") else [2, 3],
        "remaining_nonempty_leaves": ["D(a57_01)"] if terminal.startswith("STRUCTURAL_UNIT") else [
            "D(a57_01)",
            "V(a57_01) intersection D(a04_11,a04_12)",
            "V(a57_01,a04_12) intersection D(a04_11)",
        ],
    },
    "conclusion": {
        "singular_runs": 0,
        "all_monic_graph_reductions_exhausted": not monic_candidates(final_variables, final_polynomials),
        "mathematical_coverage": terminal.startswith("STRUCTURAL_UNIT"),
        "no_unproved_root_extraction": True,
    },
}
temporary = HERE / "results_design.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_design.json")
print(json.dumps({
    "status": terminal,
    "steps": len(ledger),
    "step_kinds": [step["kind"] for step in ledger],
    "final": final_stats,
    "top_factors": factors[:6],
    "solver_runs": 0,
}, sort_keys=True))
