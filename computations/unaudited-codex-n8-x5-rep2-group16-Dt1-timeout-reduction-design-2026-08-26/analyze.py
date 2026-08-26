#!/usr/bin/env python3
"""Exact source-level reduction census for the timed-out rep2 group16 D(t1) chart."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"
SOURCE = UPSTREAM / "sources/rep2_group016_67_Dt1_runtime_Q.sing"
SOURCE_SHA = "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244"
TIMEOUT_RESULT_SHA = "b4656dd9e74e31b38a63af40404e8b0d0291f5a5d31e471dde104ab59d2e0c8f"
TIMEOUT_MANIFEST_SHA = "5d9fdcbfea5aab0245ffde35ab62b4ab3626c99d8b88d09b5a8554ae8bd49551"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(SOURCE) == SOURCE_SHA
assert sha(UPSTREAM / "results/lane2_Dt1.json") == TIMEOUT_RESULT_SHA
assert sha(UPSTREAM / "TERMINAL_MANIFEST.sha256") == TIMEOUT_MANIFEST_SHA


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


Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]


def add(left: Polynomial, right: Polynomial, sign: int = 1) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + sign * coefficient
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


class PolynomialParser:
    def __init__(self, expression: str, index: dict[str, int]):
        self.tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]", expression)
        self.cursor = 0
        self.index = index

    def expression(self) -> Polynomial:
        value = self.term()
        while self.cursor < len(self.tokens) and self.tokens[self.cursor] in ("+", "-"):
            sign = 1 if self.tokens[self.cursor] == "+" else -1
            self.cursor += 1
            value = add(value, self.term(), sign)
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


def echelon_sparse(rows: list[dict[int, int]]) -> dict[int, dict[int, Fraction]]:
    echelon: dict[int, dict[int, Fraction]] = {}
    for raw in rows:
        row = {column: Fraction(value) for column, value in raw.items() if value}
        while row:
            column = min(row)
            if column not in echelon:
                pivot = row[column]
                echelon[column] = {key: value / pivot for key, value in row.items()}
                break
            factor = row[column]
            known = echelon[column]
            row = {
                key: row.get(key, Fraction()) - factor * known.get(key, Fraction())
                for key in set(row) | set(known)
            }
            row = {key: value for key, value in row.items() if value}
    return echelon


def integer_nullspace(echelon: dict[int, dict[int, Fraction]], columns: int) -> list[list[int]]:
    free = [column for column in range(columns) if column not in echelon]
    basis: list[list[int]] = []
    for free_column in free:
        vector: dict[int, Fraction] = {free_column: Fraction(1)}
        for pivot in sorted(echelon, reverse=True):
            row = echelon[pivot]
            vector[pivot] = -sum(value * vector.get(column, Fraction()) for column, value in row.items() if column != pivot)
        denominator = 1
        for value in vector.values():
            denominator = denominator * value.denominator // math.gcd(denominator, value.denominator)
        integers = [int(vector.get(column, Fraction()) * denominator) for column in range(columns)]
        divisor = 0
        for value in integers:
            divisor = math.gcd(divisor, abs(value))
        integers = [value // divisor for value in integers]
        first = next(value for value in integers if value)
        if first < 0:
            integers = [-value for value in integers]
        basis.append(integers)
    return basis


text = SOURCE.read_text()
variables, equations = parse_program(text)
assert len(variables) == 64 and len(equations) == len(set(equations)) == 6569
index = {variable: position for position, variable in enumerate(variables)}
polynomials: list[Polynomial] = []
for equation in equations:
    parser = PolynomialParser(equation, index)
    polynomial = parser.expression()
    assert parser.cursor == len(parser.tokens) and polynomial
    polynomials.append(polynomial)

occurrences = Counter()
max_exponents = Counter()
monic_candidates: list[dict] = []
linear_rows: list[dict[int, int]] = []
affine_rows: list[dict[int, int]] = []
term_histogram = Counter()
degree_histogram = Counter()
for equation_index, polynomial in enumerate(polynomials):
    term_histogram[len(polynomial)] += 1
    maximum_degree = max(map(len, polynomial))
    degree_histogram[maximum_degree] += 1
    linear = {monomial[0]: coefficient for monomial, coefficient in polynomial.items() if len(monomial) == 1}
    if linear:
        linear_rows.append(linear)
    if maximum_degree <= 1:
        row = dict(linear)
        if polynomial.get((), 0):
            row[len(variables)] = polynomial[()]
        affine_rows.append(row)
    for monomial in polynomial:
        for position in set(monomial):
            occurrences[position] += 1
            max_exponents[position] = max(max_exponents[position], monomial.count(position))
    for position in range(len(variables)):
        coefficient = polynomial.get((position,), 0)
        if abs(coefficient) == 1 and not any(position in monomial for monomial in polynomial if monomial != (position,)):
            monic_candidates.append({"equation": equation_index, "variable": variables[position], "coefficient": coefficient, "terms": len(polynomial)})

grading_rows: list[dict[int, int]] = []
for polynomial in polynomials:
    monomials = sorted(polynomial)
    base = Counter(monomials[0])
    for monomial in monomials[1:]:
        current = Counter(monomial)
        row = {position: base[position] - current[position] for position in set(base) | set(current)}
        row = {position: value for position, value in row.items() if value}
        if row:
            grading_rows.append(row)
grading_echelon = echelon_sparse(grading_rows)
grading_basis = integer_nullspace(grading_echelon, len(variables))

# A coordinate is globally invertible when some source generator has constant
# term +/-1 and every other monomial contains that coordinate.  This is an
# exact ideal-theoretic witness q*h=1, not a generic-open assumption.
global_unit_witnesses: dict[int, list[int]] = {}
for equation_index, polynomial in enumerate(polynomials):
    if abs(polynomial.get((), 0)) != 1:
        continue
    nonconstant = [set(monomial) for monomial in polynomial if monomial]
    if not nonconstant:
        continue
    common = set.intersection(*nonconstant)
    for position in common:
        global_unit_witnesses.setdefault(position, []).append(equation_index)


def determinant(matrix: list[list[int]]) -> int:
    if not matrix:
        return 1
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        (-1 if column % 2 else 1) * matrix[0][column] * determinant([
            row[:column] + row[column + 1:] for row in matrix[1:]
        ])
        for column in range(len(matrix))
    )


def primitive_weight_rows(positions: tuple[int, ...]) -> bool:
    size = len(positions)
    rows = [[grading_basis[basis][position] for basis in range(len(grading_basis))] for position in positions]
    divisor = 0
    for columns in itertools.combinations(range(len(grading_basis)), size):
        minor = determinant([[row[column] for column in columns] for row in rows])
        divisor = math.gcd(divisor, abs(minor))
    return divisor == 1


unit_positions = sorted(global_unit_witnesses, key=lambda position: variables[position])
global_gauge_positions: tuple[int, ...] = ()
for size in range(min(len(unit_positions), len(grading_basis)), 0, -1):
    choices = [choice for choice in itertools.combinations(unit_positions, size) if primitive_weight_rows(choice)]
    if choices:
        global_gauge_positions = min(choices, key=lambda choice: tuple(variables[position] for position in choice))
        break


def specialize(assignments: dict[int, int]) -> list[Polynomial]:
    specialized: list[Polynomial] = []
    seen = set()
    zero = {position for position, value in assignments.items() if value == 0}
    one = set(assignments) - zero
    for polynomial in polynomials:
        reduced: Polynomial = {}
        for monomial, coefficient in polynomial.items():
            if zero.intersection(monomial):
                continue
            new_monomial = tuple(position for position in monomial if position not in one)
            reduced[new_monomial] = reduced.get(new_monomial, 0) + coefficient
        reduced = {monomial: coefficient for monomial, coefficient in reduced.items() if coefficient}
        if not reduced:
            continue
        if len(reduced) == 1 and () in reduced:
            return [{(): 1}]
        key = tuple(sorted(reduced.items()))
        if key not in seen:
            seen.add(key)
            specialized.append(reduced)
    return specialized


def branch_stats(polys: list[Polynomial], assignments: dict[int, int]) -> dict:
    remaining = set(range(len(variables))) - set(assignments)
    active = {position for polynomial in polys for monomial in polynomial for position in monomial}
    return {
        "variables": len(remaining),
        "generators": len(polys),
        "total_terms": sum(map(len, polys)),
        "maximum_terms": max(map(len, polys)),
        "inactive": sorted(variables[position] for position in remaining - active),
        "unit_ideal_structural": polys == [{(): 1}],
    }


def serialize(polynomial: Polynomial) -> str:
    pieces: list[str] = []
    for monomial, coefficient in sorted(polynomial.items(), key=lambda item: (len(item[0]), item[0])):
        factors = "*".join(variables[position] for position in monomial)
        magnitude = abs(coefficient)
        body = str(magnitude) if not factors else factors if magnitude == 1 else f"{magnitude}*{factors}"
        pieces.append((("-" if coefficient < 0 else "+") if pieces else ("-" if coefficient < 0 else "")) + body)
    return "".join(pieces)


# A primitive grading coordinate gives an exact root-free D/V cover.  Score all
# weight +/-1 coordinates over every grading basis vector, then choose the
# smallest worst specialized syntax.  If no such coordinate exists, record the
# obstruction without inventing a gauge.
candidates: list[tuple[tuple, int, int]] = []
candidate_ledger: list[dict] = []
for basis_index, vector in enumerate(grading_basis):
    for position, weight in enumerate(vector):
        if abs(weight) != 1:
            continue
        open_polys = specialize({position: 1})
        closed_polys = specialize({position: 0})
        open_stats = branch_stats(open_polys, {position: 1})
        closed_stats = branch_stats(closed_polys, {position: 0})
        objective = (
            max(open_stats["total_terms"], closed_stats["total_terms"]),
            open_stats["total_terms"] + closed_stats["total_terms"],
            max(open_stats["generators"], closed_stats["generators"]),
            variables[position],
        )
        candidates.append((objective, basis_index, position))
        candidate_ledger.append({
            "basis_index": basis_index, "coordinate": variables[position], "weight": weight,
            "D_unit_stats": open_stats, "V_zero_stats": closed_stats,
            "objective": list(objective[:-1]),
        })

cover_sources: list[dict] = []
selected = None
inverse_partner = None
if candidates:
    objective, basis_index, position = min(candidates)
    selected = {"basis_index": basis_index, "coordinate": variables[position], "weight": grading_basis[basis_index][position], "objective": list(objective[:-1])}
    # The selected coordinate is already globally invertible when the source
    # contains q*r-1.  In that case V(q) is empty, and the primitive torus
    # gauge q=1 also forces r=1.  Eliminate both coordinates and the now-zero
    # inverse equation in one reversible step.
    for partner in range(len(variables)):
        if partner == position:
            continue
        inverse = {(): -1, tuple(sorted((position, partner))): 1}
        if inverse in polynomials or {(): 1, tuple(sorted((position, partner))): -1} in polynomials:
            inverse_partner = partner
            break
    sources = HERE / "sources"
    sources.mkdir(exist_ok=True)
    for stale in sources.glob("*.sing"):
        stale.unlink()
    global_assignments = {current: 1 for current in global_gauge_positions}
    # Close exact variable inverse equations q*r=1 after fixing either factor.
    changed = True
    while changed:
        changed = False
        for left in list(global_assignments):
            for right in range(len(variables)):
                if right in global_assignments or right == left:
                    continue
                inverse = {(): -1, tuple(sorted((left, right))): 1}
                if inverse in polynomials or {(): 1, tuple(sorted((left, right))): -1} in polynomials:
                    global_assignments[right] = 1
                    changed = True
    branches = (("GLOBAL_UNIT_GAUGE", global_assignments),) if global_gauge_positions else (("D1", {position: 1}), ("V0", {position: 0}))
    for label, assignments in branches:
        polys = specialize(assignments)
        remaining = [current for current in range(len(variables)) if current not in assignments]
        path = sources / f"rep2_group16_Dt1_{variables[position]}_{label}_Q_design.sing"
        program = "\n".join((
            "// EXACT Q DESIGN INPUT ONLY: no solver run authorized.",
            "// Exact primitive-torus D/V specialization of consumed timeout chart.",
            "option(noredefine);",
            f"ring r=0,({','.join(variables[current] for current in remaining)}),dp;",
            "ideal I=" + ",\n".join(serialize(polynomial) for polynomial in polys) + ";",
            'print("INPUT_VARIABLES="+string(nvars(r)));',
            'print("INPUT_GENERATORS="+string(size(I)));',
            "quit;",
            "",
        ))
        temporary = path.with_suffix(".sing.tmp")
        temporary.write_text(program)
        os.replace(temporary, path)
        rebuilt_variables, rebuilt_equations = parse_program(program)
        assert rebuilt_variables == [variables[current] for current in remaining]
        rebuilt: list[Polynomial] = []
        for expression in rebuilt_equations:
            parser = PolynomialParser(expression, index)
            polynomial = parser.expression()
            assert parser.cursor == len(parser.tokens)
            rebuilt.append(polynomial)
        assert rebuilt == polys
        cover_sources.append({
            "branch": label, "assignment": {variables[current]: value for current, value in assignments.items()},
            "path": str(path.relative_to(HERE)), "sha256": sha(path),
            **branch_stats(polys, assignments),
        })

adjacency = [set() for _ in variables]
for polynomial in polynomials:
    support = {position for monomial in polynomial for position in monomial}
    for position in support:
        adjacency[position].update(support - {position})
components: list[list[str]] = []
unseen = set(range(len(variables)))
while unseen:
    root = min(unseen)
    queue = deque([root])
    component: set[int] = set()
    while queue:
        position = queue.popleft()
        if position in component:
            continue
        component.add(position)
        queue.extend(adjacency[position] - component)
    unseen -= component
    components.append(sorted(variables[position] for position in component))

result = {
    "schema": "KRENN_X5_REP2_GROUP16_DT1_TIMEOUT_REDUCTION_DESIGN_V1",
    "status": "PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE" if global_gauge_positions else "PASS_EXACT_PRIMITIVE_TORUS_DV_COVER" if selected else "PASS_EXACT_CENSUS_NO_PRIMITIVE_TORUS_COVER",
    "source": {"path": str(SOURCE.relative_to(ROOT)), "sha256": sha(SOURCE), "bytes": SOURCE.stat().st_size, "variables": len(variables), "generators": len(equations), "field": "Q"},
    "timeout_binding": {"result_sha256": sha(UPSTREAM / "results/lane2_Dt1.json"), "terminal_manifest_sha256": sha(UPSTREAM / "TERMINAL_MANIFEST.sha256"), "rerun": False},
    "grading": {
        "constraint_rows": len(grading_rows), "rank": len(grading_echelon), "nullity": len(grading_basis),
        "basis": grading_basis,
        "nonzero_weights": [{variables[position]: weight for position, weight in enumerate(vector) if weight} for vector in grading_basis],
    },
    "linear_census": {
        "inactive": sorted(variables[position] for position in range(len(variables)) if not occurrences[position]),
        "unit_coefficient_graph_substitutions": monic_candidates,
        "affine_linear_generator_count": len(affine_rows), "affine_linear_rank": len(echelon_sparse(affine_rows)),
        "all_linear_part_rank": len(echelon_sparse(linear_rows)),
        "variables_affine_in_every_occurrence": sorted(variables[position] for position in range(len(variables)) if max_exponents[position] <= 1),
    },
    "expanded": {
        "total_terms": sum(map(len, polynomials)), "minimum_terms": min(map(len, polynomials)), "maximum_terms": max(map(len, polynomials)),
        "term_histogram": dict(sorted(term_histogram.items())), "degree_histogram": dict(sorted(degree_histogram.items())),
    },
    "interaction": {"components": len(components), "component_sizes": [len(component) for component in components], "members": components},
    "cover": {
        "identity": "D(q) union V(q)", "root_free": True, "selected": selected,
        "global_unit_witnesses": {
            variables[current]: {"equation_indices": equations, "weights": [basis[current] for basis in grading_basis]}
            for current, equations in sorted(global_unit_witnesses.items(), key=lambda item: variables[item[0]])
        },
        "maximal_primitive_global_gauge_coordinates": [variables[current] for current in global_gauge_positions],
        "maximal_primitive_global_gauge_weight_rows": [
            [basis[current] for basis in grading_basis] for current in global_gauge_positions
        ],
        "global_gauge_assignments_including_inverse_partners": {
            variables[current]: value for current, value in sorted(global_assignments.items())
        } if global_gauge_positions else {},
        "global_inverse_partner": variables[inverse_partner] if inverse_partner is not None else None,
        "global_inverse_equation": f"{variables[position]}*{variables[inverse_partner]}-1" if inverse_partner is not None else None,
        "closed_branch_empty": inverse_partner is not None,
        "candidate_ledger": sorted(candidate_ledger, key=lambda record: (record["basis_index"], record["coordinate"])),
        "sources": cover_sources,
        "forward": "for primitive torus weight +/-1, act by q inverse to set q=1 on D(q); V(q) is q=0",
        "reverse": "restore the torus parameter with the exact integer weight vector; no root extraction",
    },
    "conclusion": {"singular_runs": 0, "mathematical_coverage": False, "old_timeout_consumed": True, "old_chart_relaunch": False},
}

temporary = HERE / "results_design.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_design.json")
print(json.dumps({
    "status": result["status"], "grading_rank": result["grading"]["rank"], "grading_nullity": result["grading"]["nullity"],
    "monic": len(monic_candidates), "inactive": len(result["linear_census"]["inactive"]), "selected": selected,
    "source_shapes": [[source["variables"], source["generators"], source["total_terms"]] for source in cover_sources],
}, sort_keys=True))
