#!/usr/bin/env python3
"""Independent exact referee of the rep5 k2/t1 torus-cover design; zero solve."""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import math
import os
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26"
DES = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25"
MOD = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26"
MODREF = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26"
PINS = {
    PROD / "MANIFEST.sha256": "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e",
    PROD / "results_design.json": "9a42d532e2b007001d0411e470867fc31195ceb67d39633dd1a6da9bee83d916",
    PROD / "results_hostiles.json": "ebc93d255945b782f82a69040ff185f5cbb1e09021fe36095c1bee4f25d7ea7b",
    PROD / "build_design.py": "d9ab05f8a278467d79eeb816e032abc713525d4863cc5dc5f3ce25210b7efb22",
    PROD / "test_design.py": "7b6a336d8fdef23de4197bd811a00b5d78ac9fdc5628ca7780d38c99edf52702",
    DES / "MANIFEST.sha256": "50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1",
    DES / "rep5_p00_guardpivot_k2_rank2_t1_Q.sing": "1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e",
    MOD / "MANIFEST.sha256": "687dd47c10265ad82421cd06e015db4a88982710dbdba370ac0fee82f5f5596b",
    MOD / "rep5_rank2_k2_t1_p32003.sing": "fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a",
    MOD / "ATTEMPT.json": "d06dbcab99c5907fac247beacb6e0bf182a9c50f96f56cd476a6e7aa7076510b",
    MOD / "result.json": "eb9ced6f5a6e04d38a84c0b03817245b8af6ae08fbaf262f6eb136a8492fce6e",
    MOD / "TERMINAL_MANIFEST.sha256": "aa18079a9f35fa858b52343a8f727282ccc8462ab5f801644c188a535533d851",
    MODREF / "results_referee.json": "e41849050e8486c061970cd342b68d4b6d6855b606548d4ca09d456f61f59d7a",
    MODREF / "FINAL_MANIFEST.sha256": "0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def atomic(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def replay(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        target = (path.parent / name.strip()).resolve()
        assert target.is_file() and sha(target) == digest, (target, digest, sha(target))
        count += 1
    return count


def parse(text: str) -> tuple[list[str], list[str]]:
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(";\nprint", 1)[0]
    equations = []
    depth = 0
    start = 0
    for position, character in enumerate(body):
        depth += character == "("
        depth -= character == ")"
        if character == "," and depth == 0:
            equations.append(body[start:position].strip())
            start = position + 1
    equations.append(body[start:].strip())
    assert depth == 0
    return variables, equations


def normalized(row: dict[int, int]) -> tuple[tuple[int, int], ...] | None:
    row = {column: value for column, value in row.items() if value}
    if not row:
        return None
    divisor = math.gcd(*[abs(value) for value in row.values()])
    row = {column: value // divisor for column, value in row.items()}
    if row[min(row)] < 0:
        row = {column: -value for column, value in row.items()}
    return tuple(sorted(row.items()))


class MonomialWeightParser:
    def __init__(self, expression: str, variable_index: dict[str, int], constraints: set):
        self.tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]", expression)
        self.cursor = 0
        self.variable_index = variable_index
        self.constraints = constraints

    def expression(self) -> dict[int, int] | None:
        terms = [self.term()]
        while self.cursor < len(self.tokens) and self.tokens[self.cursor] in "+-":
            self.cursor += 1
            terms.append(self.term())
        terms = [term for term in terms if term is not None]
        if not terms:
            return None
        for term in terms[1:]:
            relation = normalized({
                key: terms[0].get(key, 0) - term.get(key, 0)
                for key in set(terms[0]) | set(term)
            })
            if relation:
                self.constraints.add(relation)
        return terms[0]

    def term(self) -> dict[int, int] | None:
        value = self.factor()
        while self.cursor < len(self.tokens) and self.tokens[self.cursor] == "*":
            self.cursor += 1
            factor = self.factor()
            if value is None or factor is None:
                value = None
            else:
                value = {key: value.get(key, 0) + factor.get(key, 0) for key in set(value) | set(factor)}
        return value

    def factor(self) -> dict[int, int] | None:
        token = self.tokens[self.cursor]
        if token == "-":
            self.cursor += 1
            return self.factor()
        if token == "(":
            self.cursor += 1
            value = self.expression()
            assert self.tokens[self.cursor] == ")"
            self.cursor += 1
            return value
        self.cursor += 1
        if token.isdigit():
            return None if int(token) == 0 else {}
        return {self.variable_index[token]: 1}


def exact_grading(variables: list[str], equations: list[str]) -> tuple[list[list[int]], dict]:
    index = {variable: position for position, variable in enumerate(variables)}
    constraints: set[tuple[tuple[int, int], ...]] = set()
    for equation in equations:
        parser = MonomialWeightParser(equation, index, constraints)
        parser.expression()
        assert parser.cursor == len(parser.tokens)
    echelon: dict[int, dict[int, Fraction]] = {}
    for relation in sorted(constraints, key=lambda item: (len(item), item)):
        row = {column: Fraction(value) for column, value in relation}
        while row:
            lead = min(row)
            if lead not in echelon:
                scale = row[lead]
                echelon[lead] = {column: value / scale for column, value in row.items()}
                break
            scale = row[lead]
            old = echelon[lead]
            row = {column: row.get(column, 0) - scale * old.get(column, 0) for column in set(row) | set(old)}
            row = {column: value for column, value in row.items() if value}
    free = [column for column in range(len(variables)) if column not in echelon]
    basis = []
    for free_column in free:
        vector: dict[int, Fraction] = {free_column: Fraction(1)}
        for lead in sorted(echelon, reverse=True):
            vector[lead] = -sum(value * vector.get(column, 0) for column, value in echelon[lead].items() if column != lead)
        assert all(value.denominator == 1 for value in vector.values())
        basis.append([int(vector.get(column, 0)) for column in range(len(variables))])
    for relation in constraints:
        assert all(sum(value * vector[column] for column, value in relation) == 0 for vector in basis)
    return basis, {
        "constraint_count": len(constraints), "rank": len(echelon), "nullity": len(basis),
        "free_variables": [variables[column] for column in free],
        "basis_sha256": hashlib.sha256(json.dumps(basis, separators=(",", ":")).encode()).hexdigest(),
    }


def matrix_det(matrix: list[list[int]]) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    determinant = Fraction(1)
    for column in range(len(rows)):
        pivot = next((row for row in range(column, len(rows)) if rows[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            determinant = -determinant
        value = rows[column][column]
        determinant *= value
        rows[column] = [entry / value for entry in rows[column]]
        for row in range(column + 1, len(rows)):
            factor = rows[row][column]
            rows[row] = [left - factor * right for left, right in zip(rows[row], rows[column])]
    assert determinant.denominator == 1
    return int(determinant)


def kernel(matrix: list[list[int]]) -> list[list[int]]:
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    pivots = []
    for column in range(len(rows[0])):
        selected = next((row for row in range(rank, len(rows)) if rows[row][column]), None)
        if selected is None:
            continue
        rows[rank], rows[selected] = rows[selected], rows[rank]
        pivot = rows[rank][column]
        rows[rank] = [value / pivot for value in rows[rank]]
        for row in range(len(rows)):
            if row != rank and rows[row][column]:
                factor = rows[row][column]
                rows[row] = [left - factor * right for left, right in zip(rows[row], rows[rank])]
        pivots.append(column)
        rank += 1
    free = [column for column in range(len(rows[0])) if column not in pivots]
    result = []
    for free_column in free:
        vector = [Fraction()] * len(rows[0])
        vector[free_column] = 1
        for row, pivot in reversed(list(enumerate(pivots))):
            vector[pivot] = -sum(rows[row][column] * vector[column] for column in free)
        denominator = math.lcm(*[value.denominator for value in vector])
        integers = [int(value * denominator) for value in vector]
        divisor = math.gcd(*[abs(value) for value in integers if value])
        result.append([value // divisor for value in integers])
    return result


def substitute(text: str, mapping: dict[str, str]) -> str:
    pattern = r"\b(?:" + "|".join(map(re.escape, sorted(mapping, key=len, reverse=True))) + r")\b"
    return re.sub(pattern, lambda match: mapping[match.group()], text)


def identifiers(text: str) -> set[str]:
    return set(re.findall(r"\b(?:a\d\d_\d\d|xn\d|yn\d|zn\d|abar|beta|t\d|sat)\b", text))


for path, digest in PINS.items():
    assert path.is_file() and sha(path) == digest, (path, sha(path), digest)
producer_manifest_lines = replay(PROD / "MANIFEST.sha256")
terminal_manifest_lines = replay(MOD / "TERMINAL_MANIFEST.sha256")
timeout_referee_lines = replay(MODREF / "FINAL_MANIFEST.sha256")
producer = json.loads((PROD / "results_design.json").read_text())
assert producer["status"] == "PASS_EXACT_16_CHART_73_VARIABLE_COVER_ZERO_SOLVES"

q_path = DES / "rep5_p00_guardpivot_k2_rank2_t1_Q.sing"
p_path = MOD / "rep5_rank2_k2_t1_p32003.sing"
q_text, p_text = q_path.read_text(), p_path.read_text()
assert q_text.replace("ring r=0,(", "ring r=32003,(", 1) == p_text
variables, equations = parse(q_text)
assert len(variables) == 84 and len(equations) == len(set(equations)) == 6562

basis, grading = exact_grading(variables, equations)
assert grading == {
    "constraint_count": 11954, "rank": 74, "nullity": 10,
    "free_variables": ["yn1", "yn2", "zn0", "zn1", "zn2", "beta", "t0", "t1", "t2", "sat"],
    "basis_sha256": "0ff4ee92a6748429af1dbcae3b6b6391f1c71acc40cbb757ec8cddd72929a954",
}
index = {variable: position for position, variable in enumerate(variables)}
char = lambda variable: [vector[index[variable]] for vector in basis]
d_char = char("a37_01")
assert d_char == [a + b for a, b in zip(char("xn1"), char("a37_00"))]
b2_char = [a + b for a, b in zip(char("a26_20"), char("a37_00"))]
for row in range(3):
    assert [a + b for a, b in zip(char(f"a26_2{row}"), char(f"a37_0{row}"))] == b2_char
unit_names = ["beta", "abar", "a37_00", "t1", "sat", "d"]
unit_matrix = [char(name) if name != "d" else d_char for name in unit_names]
minor_columns = [2, 3, 4, 5, 7, 9]
minor = [[row[column] for column in minor_columns] for row in unit_matrix]
assert matrix_det(minor) == 1
assert [sum(row) for row in zip(char("beta"), char("abar"), char("a37_00"), d_char, b2_char, char("t1"), char("sat"))] == [0] * 10
residual_basis = kernel(unit_matrix)
assert len(residual_basis) == 4
residual_char = lambda variable: [sum(char(variable)[i] * row[i] for i in range(10)) for row in residual_basis]
assert [residual_char(name) for name in ("yn1", "yn2", "t0", "t2")] == [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

# Verify the six root-free torus parameter monomials exactly.  Columns here are
# exponents in (beta, abar, v=a37_00, d, t1, sat).
coordinate_order = ["beta", "abar", "v", "d", "t1", "sat"]
parameter_exponents = [[0] * 6 for _ in range(10)]
parameter_exponents[2] = [-1, 0, 1, 0, 0, 0]   # lambda_zn0=v/beta
parameter_exponents[3] = [-1, 0, 0, 1, 0, 0]   # lambda_zn1=d/beta
parameter_exponents[4] = [-1, 1, 1, 0, 0, 0]   # lambda_zn2=abar*v/beta
parameter_exponents[5] = [-1, 0, 0, 0, 0, 0]   # lambda_beta=beta^-1
parameter_exponents[7] = [0, 0, 0, 0, -1, 0]   # lambda_t1=t1^-1
parameter_exponents[9] = [0, 0, 0, 0, 0, -1]   # lambda_sat=sat^-1
unit_coordinate_column = [0, 1, 2, 4, 5, 3]  # unit_matrix order beta,abar,v,t1,sat,d
for unit_index, character in enumerate(unit_matrix):
    transformed = [int(i == unit_coordinate_column[unit_index]) for i in range(6)]
    for parameter, exponent in zip(character, parameter_exponents):
        transformed = [left + parameter * right for left, right in zip(transformed, exponent)]
    assert transformed == [0] * 6, (coordinate_order[unit_index], transformed)

global_mapping = {
    "beta": "1", "abar": "1", "a37_00": "1", "t1": "1", "sat": "1",
    "a37_01": "(xn1+1)",
    "a26_20": "(1-a26_21*(xn1+1)-a26_22*a37_02)",
}
intermediate_variables = [variable for variable in variables if variable not in global_mapping]
intermediate_equations = [substitute(equation, global_mapping) for equation in equations[:-1]]
assert len(intermediate_variables) == 77
assert len(intermediate_equations) == len(set(intermediate_equations)) == 6561
assert all(equation not in {"0", "1", "-1"} for equation in intermediate_equations)
assert not (identifiers("\n".join(intermediate_equations)) & set(global_mapping))
saturation_after = substitute(equations[-1], global_mapping)
assert saturation_after == "(1*1*1*((xn1+1)-(xn1*1)))*((1-a26_21*(xn1+1)-a26_22*a37_02)*1+a26_21*(xn1+1)+a26_22*a37_02)*1*1-1"
# The first parenthesis is 1 and the second is 1 by literal cancellation, so
# the removed saturation generator is exactly zero after the triangular map.

residual_names = ["yn1", "yn2", "t0", "t2"]
remaining_variables = [variable for variable in intermediate_variables if variable not in residual_names]
assert len(remaining_variables) == 73
producer_sources = {tuple(int(entry["residual_assignment"][name]) for name in residual_names): entry for entry in producer["residual_cover"]["sources"]}
rebuilt_sources = []
for bits in itertools.product((0, 1), repeat=4):
    mapping = dict(zip(residual_names, map(str, bits)))
    reduced = [substitute(equation, mapping) for equation in intermediate_equations]
    assert len(reduced) == len(set(reduced)) == 6561
    assert all(equation not in {"0", "1", "-1"} for equation in reduced)
    assert identifiers("\n".join(reduced)) <= set(remaining_variables)
    label = "_".join(f"{name}{value}" for name, value in zip(residual_names, bits))
    path = PROD / "sources" / f"rep5_k2_t1_gauge_{label}_Q_design.sing"
    expected = "\n".join([
        "// EXACT Q DESIGN INPUT ONLY: zero Singular or ideal runs authorized.",
        "option(noredefine);", f"ring r=0,({','.join(remaining_variables)}),dp;",
        "ideal I=" + ",\n".join(reduced) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));', "quit;", "",
    ])
    assert path.read_text() == expected
    entry = producer_sources[bits]
    assert sha(path) == entry["sha256"] and path.stat().st_size == entry["bytes"]
    assert entry["variables"] == 73 and entry["generators"] == entry["unique_generators"] == 6561
    rebuilt_sources.append({"assignment": dict(zip(residual_names, bits)), "path": str(path.relative_to(PROD)), "sha256": sha(path), "removed_identifiers_absent": True})
assert len(rebuilt_sources) == 16 and len({tuple(item["assignment"].values()) for item in rebuilt_sources}) == 16

timeout = json.loads((MOD / "result.json").read_text())
attempt = json.loads((MOD / "ATTEMPT.json").read_text())
timeout_referee = json.loads((MODREF / "results_referee.json").read_text())
assert timeout["status"] == "FAIL_CLOSED_RESOURCE_GATE" and timeout["termination"] == "NATIVE_WALL_CAP_300"
assert timeout["mathematical_coverage"] is False and timeout["automatic_relaunch"] is False
assert attempt["status"] == "ATTEMPT_CONSUMED" and attempt["relaunch_forbidden_even_if_no_result"] is True
assert timeout_referee["status"] == "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE"
assert timeout_referee["result_sha256"] == sha(MOD / "result.json")
hostiles = json.loads((PROD / "results_hostiles.json").read_text())
test_tree = ast.parse((PROD / "test_design.py").read_text())
mutation_list = next(node.value for node in ast.walk(test_tree) if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "mutations" for target in node.targets))
assert isinstance(mutation_list, ast.List) and len(mutation_list.elts) == 14
assert hostiles == {"schema": "KRENN_X5_REP5_K2_T1_TORUS_COVER_HOSTILES_V1", "status": "PASS_14_HOSTILES_ZERO_RUN", "hostiles": 14, "solver_runs": 0}

result = {
    "schema": "KRENN_X5_REP5_K2_T1_OPEN84_TORUS_COVER_INDEPENDENT_REFEREE_V1",
    "status": "PASS_EXACT_16_CHART_TORUS_COVER_REFEREE_ZERO_SOLVES",
    "producer": {"manifest_sha256": sha(PROD / "MANIFEST.sha256"), "result_sha256": sha(PROD / "results_design.json"), "manifest_entries_replayed": producer_manifest_lines},
    "original": {"source_Q_sha256": sha(q_path), "source_p32003_sha256": sha(p_path), "ring_transport_byte_exact": True, "variables": 84, "generators": 6562},
    "grading": {**grading, "unit_character_matrix": unit_matrix, "selected_minor_columns": minor_columns, "selected_minor": minor, "selected_minor_determinant": matrix_det(minor), "saturation_character_zero": True, "residual_basis": residual_basis},
    "global_gauge": {
        "unit_coordinates": unit_names, "unit_count": 6, "unimodular": True,
        "root_free_parameter_formulas_verified": True, "saturation_forces_b2_one": True,
        "forward_substitution": global_mapping,
        "reverse": {"a37_01": "xn1+d*a37_00", "a26_20": "(b2-a26_21*a37_01-a26_22*a37_02)/a37_00"},
        "variables_after": 77, "generators_after": 6561,
        "all_removed_identifiers_absent": True, "all_generators_unique_nontrivial": True,
    },
    "residual_cover": {
        "primitive_coordinates": residual_names, "primitive_character_matrix": [residual_char(name) for name in residual_names],
        "cover": "product_q (D(q) union V(q))", "chart_count": 16,
        "variables_each": 73, "generators_each": 6561,
        "all_assignments_present_once": True, "all_sources_byte_rebuilt": True,
        "all_removed_identifiers_absent": True, "all_generators_unique_nontrivial": True,
        "sources": rebuilt_sources,
    },
    "hostiles": {"count": 14, "mutation_list_recounted": 14, "all_pass": True, "solver_runs": 0},
    "timeout_binding": {
        "terminal_manifest_sha256": sha(MOD / "TERMINAL_MANIFEST.sha256"),
        "terminal_manifest_entries_replayed": terminal_manifest_lines,
        "referee_manifest_sha256": sha(MODREF / "FINAL_MANIFEST.sha256"),
        "referee_manifest_entries_replayed": timeout_referee_lines,
        "termination": timeout["termination"], "attempt_consumed": True,
        "mathematical_coverage": False, "reuse_or_relaunch_authorized": False,
    },
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "scope": {"design_referee_only": True, "singular_runs": 0, "ideal_runs": 0, "chart_closed": False, "rep5_closed": False, "pilot_launch_authorized": False},
}
atomic(H / "results_referee.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
report = f"""# Rep5 k2/t1 open84 torus-cover independent referee

Status: **{result['status']}**.

The 84-variable/6,562-generator Q source and its p32003 transport replay.  An
independent exact grading reconstruction gives rank 74, nullity 10, and the
pinned basis hash.  The six chosen unit-coordinate characters contain a
determinant-one minor; direct exponent replay verifies the six root-free torus
parameter formulas.  The saturation equation then forces `b2=1`, and its
triangular elimination gives exactly 77 variables and 6,561 unique nontrivial
generators.

The residual characters of `yn1,yn2,t0,t2` are the 4x4 identity.  Their complete
`D(q) union V(q)` product has 16 assignments.  All 16 emitted 73-variable/6,561-
generator sources were independently reconstructed byte-for-byte, with every
removed identifier absent.

The 14 hostile mutations replay structurally.  The prior p32003 attempt remains
a consumed native-300-second wall failure with zero mathematical coverage and no
reuse/relaunch.  No Singular or ideal computation was run by this referee.
"""
atomic(H / "REPORT.md", report)
print(json.dumps({"status": result["status"], "grading": [74, 10], "charts": 16, "source_shape": [73, 6561], "solver_runs": 0}, sort_keys=True))
