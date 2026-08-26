#!/usr/bin/env python3
"""Exact torus quotient and exhaustive residual cover of consumed rep5 k2/t1; never solve."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
from fractions import Fraction
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions are load-bearing")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25"
DESIGN_REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-referee-2026-08-25"
MODULAR = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26"
MODULAR_REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26"

PINS = {
    DESIGN / "MANIFEST.sha256": "50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1",
    DESIGN / "generate_design_v2.py": "5f1c16d4307776a1f294b06cfeb1139a3d0c8ac8cb22064782b3b59709b67699",
    DESIGN / "rep5_p00_guardpivot_k2_rank2_t1_Q.sing": "1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e",
    DESIGN_REF / "FINAL_MANIFEST.sha256": "3eef6a5bec2f260625189285cdaf171dbfa36530a1f67086528583e4f96db4c6",
    MODULAR / "MANIFEST.sha256": "687dd47c10265ad82421cd06e015db4a88982710dbdba370ac0fee82f5f5596b",
    MODULAR / "rep5_rank2_k2_t1_p32003.sing": "fd182135d5da6eda87e284a4f38f147fbf13bef14016c1ee300bb9bde6713c5a",
    MODULAR / "ATTEMPT.json": "d06dbcab99c5907fac247beacb6e0bf182a9c50f96f56cd476a6e7aa7076510b",
    MODULAR / "result.json": "eb9ced6f5a6e04d38a84c0b03817245b8af6ae08fbaf262f6eb136a8492fce6e",
    MODULAR / "TERMINAL_MANIFEST.sha256": "aa18079a9f35fa858b52343a8f727282ccc8462ab5f801644c188a535533d851",
    MODULAR_REF / "results_referee.json": "e41849050e8486c061970cd342b68d4b6d6855b606548d4ca09d456f61f59d7a",
    MODULAR_REF / "FINAL_MANIFEST.sha256": "0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def atomic(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary.write_text(text)
    os.replace(temporary, path)


def replay_manifest(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(None, 1)
        target = (path.parent / relative.strip()).resolve()
        assert target.is_file() and sha(target) == digest, (target, digest)
        count += 1
    return count


def parse_program(text: str) -> tuple[list[str], list[str]]:
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    equations: list[str] = []
    depth = 0
    start = 0
    for position, character in enumerate(body):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            assert depth >= 0
        elif character == "," and depth == 0:
            equations.append(body[start:position].strip())
            start = position + 1
    equations.append(body[start:].strip())
    assert depth == 0
    return variables, equations


def normalize_row(row: dict[int, int]) -> tuple[tuple[int, int], ...] | None:
    row = {key: value for key, value in row.items() if value}
    if not row:
        return None
    divisor = 0
    for value in row.values():
        divisor = math.gcd(divisor, abs(value))
    row = {key: value // divisor for key, value in row.items()}
    first = min(row)
    if row[first] < 0:
        row = {key: -value for key, value in row.items()}
    return tuple(sorted(row.items()))


class WeightParser:
    """Infer exact multigradings from homogeneous expression structure."""

    def __init__(self, text: str, index: dict[str, int], constraints: set[tuple[tuple[int, int], ...]]):
        self.tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]", text)
        self.position = 0
        self.index = index
        self.constraints = constraints

    def expression(self) -> dict[int, int] | None:
        terms = [self.term()]
        while self.position < len(self.tokens) and self.tokens[self.position] in "+-":
            self.position += 1
            terms.append(self.term())
        terms = [term for term in terms if term is not None]
        if not terms:
            return None
        for term in terms[1:]:
            row = normalize_row({
                key: terms[0].get(key, 0) - term.get(key, 0)
                for key in set(terms[0]) | set(term)
            })
            if row:
                self.constraints.add(row)
        return terms[0]

    def term(self) -> dict[int, int] | None:
        value = self.factor()
        while self.position < len(self.tokens) and self.tokens[self.position] == "*":
            self.position += 1
            factor = self.factor()
            if value is None or factor is None:
                value = None
            else:
                value = {
                    key: value.get(key, 0) + factor.get(key, 0)
                    for key in set(value) | set(factor)
                }
        return value

    def factor(self) -> dict[int, int] | None:
        token = self.tokens[self.position]
        if token == "-":
            self.position += 1
            return self.factor()
        if token == "(":
            self.position += 1
            value = self.expression()
            assert self.tokens[self.position] == ")"
            self.position += 1
            return value
        self.position += 1
        if token.isdigit():
            return None if int(token) == 0 else {}
        return {self.index[token]: 1}


def exact_grading_basis(variables: list[str], equations: list[str]) -> tuple[list[list[int]], dict]:
    index = {variable: position for position, variable in enumerate(variables)}
    constraints: set[tuple[tuple[int, int], ...]] = set()
    for equation in equations:
        parser = WeightParser(equation, index, constraints)
        parser.expression()
        assert parser.position == len(parser.tokens)
    pivots: dict[int, dict[int, Fraction]] = {}
    for sparse in sorted(constraints, key=lambda value: (len(value), value)):
        row = {key: Fraction(value) for key, value in sparse}
        while row:
            column = min(row)
            if column not in pivots:
                pivot = row[column]
                pivots[column] = {key: value / pivot for key, value in row.items()}
                break
            factor = row[column]
            known = pivots[column]
            row = {
                key: row.get(key, Fraction()) - factor * known.get(key, Fraction())
                for key in set(row) | set(known)
            }
            row = {key: value for key, value in row.items() if value}
    free = [position for position in range(len(variables)) if position not in pivots]
    basis: list[list[int]] = []
    for free_position in free:
        vector: dict[int, Fraction] = {free_position: Fraction(1)}
        for column in sorted(pivots, reverse=True):
            vector[column] = -sum(
                value * vector.get(other, Fraction())
                for other, value in pivots[column].items()
                if other != column
            )
        assert all(value.denominator == 1 for value in vector.values())
        basis.append([int(vector.get(position, 0)) for position in range(len(variables))])
    for sparse in constraints:
        for vector in basis:
            assert sum(value * vector[position] for position, value in sparse) == 0
    metadata = {
        "constraint_count": len(constraints),
        "rank": len(pivots),
        "nullity": len(basis),
        "free_variables": [variables[position] for position in free],
        "basis_sha256": hashlib.sha256(json.dumps(basis, separators=(",", ":")).encode()).hexdigest(),
    }
    return basis, metadata


def nullspace(matrix: list[list[int]]) -> tuple[list[int], list[list[int]]]:
    rows = [[Fraction(value) for value in row] for row in matrix]
    row_count, column_count = len(rows), len(rows[0])
    rank = 0
    pivots: list[int] = []
    for column in range(column_count):
        selected = next((position for position in range(rank, row_count) if rows[position][column]), None)
        if selected is None:
            continue
        rows[rank], rows[selected] = rows[selected], rows[rank]
        pivot = rows[rank][column]
        rows[rank] = [value / pivot for value in rows[rank]]
        for position in range(row_count):
            if position != rank and rows[position][column]:
                factor = rows[position][column]
                rows[position] = [a - factor * b for a, b in zip(rows[position], rows[rank])]
        pivots.append(column)
        rank += 1
    free = [column for column in range(column_count) if column not in pivots]
    basis: list[list[int]] = []
    for free_column in free:
        vector = [Fraction()] * column_count
        vector[free_column] = Fraction(1)
        for row_position, pivot_column in reversed(list(enumerate(pivots))):
            vector[pivot_column] = -sum(rows[row_position][j] * vector[j] for j in free)
        denominator = 1
        for value in vector:
            denominator = denominator * value.denominator // math.gcd(denominator, value.denominator)
        integers = [int(value * denominator) for value in vector]
        divisor = 0
        for value in integers:
            divisor = math.gcd(divisor, abs(value))
        basis.append([value // divisor for value in integers])
    return pivots, basis


def determinant(matrix: list[list[int]]) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(rows)):
        selected = next((position for position in range(column, len(rows)) if rows[position][column]), None)
        if selected is None:
            return 0
        if selected != column:
            rows[column], rows[selected] = rows[selected], rows[column]
            result = -result
        pivot = rows[column][column]
        result *= pivot
        rows[column] = [value / pivot for value in rows[column]]
        for position in range(column + 1, len(rows)):
            factor = rows[position][column]
            rows[position] = [a - factor * b for a, b in zip(rows[position], rows[column])]
    assert result.denominator == 1
    return int(result)


for path, digest in PINS.items():
    assert sha(path) == digest, (path, sha(path), digest)
terminal_lines = replay_manifest(MODULAR / "TERMINAL_MANIFEST.sha256")
referee_lines = replay_manifest(MODULAR_REF / "FINAL_MANIFEST.sha256")

q_source = (DESIGN / "rep5_p00_guardpivot_k2_rank2_t1_Q.sing").read_text()
p_source = (MODULAR / "rep5_rank2_k2_t1_p32003.sing").read_text()
assert q_source.replace("ring r=0,(", "ring r=32003,(", 1) == p_source
variables, equations = parse_program(q_source)
assert len(variables) == 84 and len(equations) == len(set(equations)) == 6562
assert equations[-1] == "(abar*beta*a37_00*(a37_01-(xn1*a37_00)))*(a26_20*a37_00+a26_21*a37_01+a26_22*a37_02)*t1*sat-1"

timeout = json.loads((MODULAR / "result.json").read_text())
attempt = json.loads((MODULAR / "ATTEMPT.json").read_text())
referee = json.loads((MODULAR_REF / "results_referee.json").read_text())
assert timeout["status"] == "FAIL_CLOSED_RESOURCE_GATE"
assert timeout["termination"] == "NATIVE_WALL_CAP_300"
assert timeout["mathematical_coverage"] is False and timeout["automatic_relaunch"] is False
assert attempt["status"] == "ATTEMPT_CONSUMED" and attempt["relaunch_forbidden_even_if_no_result"] is True
assert referee["status"] == "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE"
assert referee["result_sha256"] == PINS[MODULAR / "result.json"]

basis, grading = exact_grading_basis(variables, equations)
assert grading["rank"] == 74 and grading["nullity"] == 10
assert grading["free_variables"] == ["yn1", "yn2", "zn0", "zn1", "zn2", "beta", "t0", "t1", "t2", "sat"]
index = {variable: position for position, variable in enumerate(variables)}


def character(variable: str) -> list[int]:
    return [vector[index[variable]] for vector in basis]


d_character = character("a37_01")
b_character = [a + b for a, b in zip(character("a26_20"), character("a37_00"))]
unit_names = ["beta", "abar", "a37_00", "t1", "sat", "d"]
unit_characters = [character(name) if name != "d" else d_character for name in unit_names]
selected_columns = [2, 3, 4, 5, 7, 9]
minor = [[row[column] for column in selected_columns] for row in unit_characters]
assert abs(determinant(minor)) == 1
assert [sum(values) for values in zip(
    character("beta"), character("abar"), character("a37_00"), d_character,
    b_character, character("t1"), character("sat")
)] == [0] * 10
pivots, residual_basis = nullspace(unit_characters)
assert len(pivots) == 6 and len(residual_basis) == 4


def residual_character(variable: str) -> list[int]:
    original = character(variable)
    return [sum(original[i] * residual[i] for i in range(10)) for residual in residual_basis]


assert residual_character("yn1") == [1, 0, 0, 0]
assert residual_character("yn2") == [0, 1, 0, 0]
assert residual_character("t0") == [0, 0, 1, 0]
assert residual_character("t2") == [0, 0, 0, 1]

# Six unit gauges are root-free because the chosen character minor is unimodular.
# With v=a37_00 and d=a37_01-xn1*v, the selected torus parameters are:
# lambda_beta=beta^-1, lambda_t1=t1^-1, lambda_sat=sat^-1,
# lambda_zn0=v/beta, lambda_zn1=d/beta, lambda_zn2=abar*v/beta.
# The saturation identity then forces b2=1.  The last two replacements are
# triangular polynomial coordinates after v=d=1.
global_substitution = {
    "beta": "1",
    "abar": "1",
    "a37_00": "1",
    "t1": "1",
    "sat": "1",
    "a37_01": "(xn1+1)",
    "a26_20": "(1-a26_21*(xn1+1)-a26_22*a37_02)",
}
assert len(global_substitution) == 7
assert "a37_01-(xn1*a37_00)" in equations[-1]
assert "a26_20*a37_00+a26_21*a37_01+a26_22*a37_02" in equations[-1]

residual_coordinates = ["yn1", "yn2", "t0", "t2"]
removed = set(global_substitution) | set(residual_coordinates)
remaining_variables = [variable for variable in variables if variable not in removed]
assert len(remaining_variables) == 73
pattern = re.compile(r"\b(?:" + "|".join(map(re.escape, sorted(removed, key=len, reverse=True))) + r")\b")
sources = []
for bits in itertools.product((0, 1), repeat=4):
    residual_substitution = dict(zip(residual_coordinates, map(str, bits)))
    substitution = {**global_substitution, **residual_substitution}
    reduced_equations = [pattern.sub(lambda match: substitution[match.group()], equation) for equation in equations[:-1]]
    assert len(reduced_equations) == len(set(reduced_equations)) == 6561
    assert all(equation not in ("0", "1", "-1") for equation in reduced_equations)
    identifiers = set(re.findall(r"\b(?:a\d\d_\d\d|xn\d|yn\d|zn\d|abar|beta|t\d|sat)\b", "\n".join(reduced_equations)))
    assert identifiers <= set(remaining_variables)
    label = "_".join(f"{name}{value}" for name, value in zip(residual_coordinates, bits))
    path = HERE / "sources" / f"rep5_k2_t1_gauge_{label}_Q_design.sing"
    program = "\n".join([
        "// EXACT Q DESIGN INPUT ONLY: zero Singular or ideal runs authorized.",
        "option(noredefine);",
        f"ring r=0,({','.join(remaining_variables)}),dp;",
        "ideal I=" + ",\n".join(reduced_equations) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ])
    atomic(path, program)
    sources.append({
        "path": str(path.relative_to(HERE)),
        "sha256": sha(path),
        "bytes": path.stat().st_size,
        "variables": len(remaining_variables),
        "generators": len(reduced_equations),
        "unique_generators": len(set(reduced_equations)),
        "residual_assignment": residual_substitution,
        "branch": {name: (f"D({name})/gauge {name}=1" if value else f"V({name})/{name}=0") for name, value in zip(residual_coordinates, bits)},
    })

result = {
    "schema": "KRENN_X5_REP5_K2_T1_OPEN84_TORUS_COVER_DESIGN_V1",
    "status": "PASS_EXACT_16_CHART_73_VARIABLE_COVER_ZERO_SOLVES",
    "consumed_timeout": {
        "source_Q_sha256": PINS[DESIGN / "rep5_p00_guardpivot_k2_rank2_t1_Q.sing"],
        "source_p32003_sha256": PINS[MODULAR / "rep5_rank2_k2_t1_p32003.sing"],
        "result_sha256": PINS[MODULAR / "result.json"],
        "attempt_sha256": PINS[MODULAR / "ATTEMPT.json"],
        "terminal_manifest_sha256": PINS[MODULAR / "TERMINAL_MANIFEST.sha256"],
        "independent_referee_result_sha256": PINS[MODULAR_REF / "results_referee.json"],
        "independent_referee_manifest_sha256": PINS[MODULAR_REF / "FINAL_MANIFEST.sha256"],
        "status": timeout["status"],
        "termination": timeout["termination"],
        "wall_seconds": timeout["wall_seconds"],
        "peak_group_rss_bytes": timeout["peak_group_rss_bytes"],
        "mathematical_coverage": False,
        "consumed_no_reuse_no_retry": True,
    },
    "original": {
        "variables": 84,
        "generators": 6562,
        "source_bytes": len(q_source.encode()),
        "source_sha256": sha(DESIGN / "rep5_p00_guardpivot_k2_rank2_t1_Q.sing"),
        "ring_transport_to_p32003_byte_exact": True,
        "order": "dp",
    },
    "grading": {
        **grading,
        "all_6562_expressions_homogeneous": True,
        "unit_coordinates": unit_names,
        "unit_character_matrix": unit_characters,
        "selected_unimodular_columns": selected_columns,
        "selected_minor": minor,
        "selected_minor_determinant": determinant(minor),
        "b2_character": b_character,
        "saturation_character_sum_zero": True,
        "residual_basis": residual_basis,
    },
    "global_gauge": {
        "localization_already_in_source": "D(abar*beta*a37_00*d*b2*t1*sat)",
        "d_definition": "d=a37_01-xn1*a37_00",
        "b2_definition": "b2=a26_20*a37_00+a26_21*a37_01+a26_22*a37_02",
        "torus_parameters": {
            "lambda_beta": "beta^-1",
            "lambda_t1": "t1^-1",
            "lambda_sat": "sat^-1",
            "lambda_zn0": "a37_00/beta",
            "lambda_zn1": "d/beta",
            "lambda_zn2": "abar*a37_00/beta",
        },
        "normalized_units": ["beta", "abar", "a37_00", "t1", "sat", "d", "b2"],
        "forward_triangular_substitution": global_substitution,
        "reverse_triangular_substitution": {
            "a37_01": "xn1+d*a37_00",
            "a26_20": "(b2-a26_21*a37_01-a26_22*a37_02)/a37_00",
        },
        "variables_after_global_gauge_and_saturation_elimination": 77,
        "generators_after_saturation_elimination": 6561,
        "root_extraction": False,
    },
    "residual_cover": {
        "residual_torus_rank": 4,
        "primitive_coordinates": residual_coordinates,
        "primitive_character_matrix": [residual_character(name) for name in residual_coordinates],
        "identity": "product over q in {yn1,yn2,t0,t2} of (D(q) union V(q))",
        "charts": 16,
        "variables_each": 73,
        "generators_each": 6561,
        "sources": sources,
        "forward": "use each independent residual G_m factor to set a nonzero primitive coordinate to 1; set it to 0 on its closed complement",
        "reverse": "restore the six global torus parameters and each residual open-chart parameter; closed branches are literal coordinate-zero subvarieties",
    },
    "order_and_scope": {
        "emitted_order": "dp",
        "alternative_order_performance_claim": False,
        "block_elimination_run": False,
        "guard_pivot_transport_to_other_strata": False,
        "same_stratum_transport_assumed": False,
        "singular_runs": 0,
        "ideal_runs": 0,
        "modular_retries": 0,
        "mathematical_coverage": False,
        "rep5_closed": False,
        "next_valid_step": "independent exact design audit; any fresh chart pilot requires a new held package and manager clearance",
    },
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "manifest_replay": {"timeout_terminal_lines": terminal_lines, "timeout_referee_lines": referee_lines},
}
atomic(HERE / "results_design.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "charts": 16, "variables": 73, "generators": 6561, "solver_runs": 0}, sort_keys=True))
