#!/usr/bin/env python3
"""Exact source-level reduction census for the selected 73/6561 rep5 torus chart."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/sources/rep5_k2_t1_gauge_yn11_yn21_t01_t20_Q_design.sing"
SOURCE_SHA = "13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0"
TORUS_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/MANIFEST.sha256"
TORUS_REF_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26/MANIFEST.sha256"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(SOURCE) == SOURCE_SHA
assert sha(TORUS_MANIFEST) == "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e"
assert sha(TORUS_REF_MANIFEST) == "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff"


def parse_program(text: str) -> tuple[list[str], list[str]]:
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    equations = []
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
    if not left or not right:
        return {}
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


def rank_sparse(rows: list[dict[int, int]]) -> int:
    return len(echelon_sparse(rows))


def integer_nullspace(echelon: dict[int, dict[int, Fraction]], columns: int) -> list[list[int]]:
    free = [column for column in range(columns) if column not in echelon]
    basis = []
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
assert len(variables) == 73 and len(equations) == len(set(equations)) == 6561
index = {variable: position for position, variable in enumerate(variables)}
polynomials: list[Polynomial] = []
for equation in equations:
    parser = PolynomialParser(equation, index)
    polynomial = parser.expression()
    assert parser.cursor == len(parser.tokens) and polynomial
    polynomials.append(polynomial)

# Exact variable use, expanded size, graph substitutions, and affine-linear ranks.
occurrences = Counter()
max_exponents = Counter()
degree_histogram = Counter()
term_histogram = Counter()
monomial_universe: set[Monomial] = set()
monic_candidates = []
affine_rows = []
linear_part_rows = []
for equation_index, polynomial in enumerate(polynomials):
    term_histogram[len(polynomial)] += 1
    maximum_degree = max(map(len, polynomial))
    degree_histogram[maximum_degree] += 1
    monomial_universe.update(polynomial)
    linear = {}
    for monomial, coefficient in polynomial.items():
        for variable in set(monomial):
            occurrences[variable] += 1
            max_exponents[variable] = max(max_exponents[variable], monomial.count(variable))
        if len(monomial) == 1:
            linear[monomial[0]] = coefficient
    if linear:
        linear_part_rows.append(linear)
    if maximum_degree <= 1:
        row = {variable: coefficient for (variable,), coefficient in polynomial.items() if len((variable,)) == 1}
        if polynomial.get((), 0):
            row[len(variables)] = polynomial[()]
        affine_rows.append(row)
    for variable in range(len(variables)):
        coefficient = polynomial.get((variable,), 0)
        if abs(coefficient) != 1:
            continue
        if any(variable in monomial for monomial in polynomial if monomial != (variable,)):
            continue
        monic_candidates.append({"equation": equation_index, "variable": variables[variable], "coefficient": coefficient, "terms": len(polynomial)})

inactive = [variables[position] for position in range(len(variables)) if not occurrences[position]]
linear_part_rank = rank_sparse(linear_part_rows)
affine_linear_rank = rank_sparse(affine_rows)

# Homogeneous grading rank from all expanded monomial-difference rows.
grading_rows = []
for polynomial in polynomials:
    monomials = sorted(polynomial)
    base = Counter(monomials[0])
    for monomial in monomials[1:]:
        current = Counter(monomial)
        row = {variable: base[variable] - current[variable] for variable in set(base) | set(current)}
        row = {variable: coefficient for variable, coefficient in row.items() if coefficient}
        if row:
            grading_rows.append(row)
grading_echelon = echelon_sparse(grading_rows)
grading_rank = len(grading_echelon)
grading_nullity = len(variables) - grading_rank
grading_basis = integer_nullspace(grading_echelon, len(variables))
assert len(grading_basis) == grading_nullity
grading_weights = [
    {variables[position]: weight for position, weight in enumerate(vector) if weight}
    for vector in grading_basis
]
assert grading_nullity == 1
weight_vector = grading_basis[0]
weighted_positions = [position for position, weight in enumerate(weight_vector) if weight]
assert len(weighted_positions) == 6 and all(abs(weight_vector[position]) == 1 for position in weighted_positions)


def specialize(assignments: dict[int, int]) -> list[Polynomial]:
    specialized = []
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


def specialized_stats(polys: list[Polynomial], assignments: dict[int, int]) -> dict:
    remaining = [position for position in range(len(variables)) if position not in assignments]
    active = {position for polynomial in polys for monomial in polynomial for position in monomial}
    monic = []
    for equation_index, polynomial in enumerate(polys):
        for position in remaining:
            coefficient = polynomial.get((position,), 0)
            if abs(coefficient) == 1 and not any(position in monomial for monomial in polynomial if monomial != (position,)):
                monic.append({"equation": equation_index, "variable": variables[position], "coefficient": coefficient, "terms": len(polynomial)})
    return {
        "variables": len(remaining), "generators": len(polys), "total_terms": sum(map(len, polys)),
        "maximum_terms": max(map(len, polys)), "inactive": sorted(variables[position] for position in set(remaining) - active),
        "monic_graph_substitutions": monic, "unit_ideal_structural": polys == [{(): 1}],
    }


# Select the best single primitive weight-one coordinate.  D(q)/q=1 and V(q)/q=0
# are an exhaustive, root-free two-chart cover; the closed chart may retain an
# emergent grading and is intentionally not recursively stratified here.
cache: dict[tuple[tuple[int, ...], int | None], tuple[list[Polynomial], dict]] = {}


def branch(zeros: tuple[int, ...], unit: int | None) -> tuple[list[Polynomial], dict]:
    key = (tuple(sorted(zeros)), unit)
    if key not in cache:
        assignments = {position: 0 for position in zeros}
        if unit is not None:
            assert unit not in assignments
            assignments[unit] = 1
        polys = specialize(assignments)
        cache[key] = (polys, specialized_stats(polys, assignments))
    return cache[key]


best = None
candidate_ledger = []
for position in weighted_positions:
    records = [branch((), position)[1], branch((position,), None)[1]]
    objective = (
        max(record["total_terms"] for record in records),
        sum(record["total_terms"] for record in records),
        max(record["generators"] for record in records),
        sum(record["generators"] for record in records),
        variables[position],
    )
    candidate_ledger.append({
        "coordinate": variables[position], "weight": weight_vector[position],
        "D_unit_stats": records[0], "V_zero_stats": records[1],
        "objective": list(objective[:-1]),
    })
    if best is None or objective < best[0]:
        best = (objective, position)
assert best is not None
cover_objective, cover_coordinate = best


def serialize_polynomial(polynomial: Polynomial) -> str:
    pieces = []
    for monomial, coefficient in sorted(polynomial.items(), key=lambda item: (len(item[0]), item[0])):
        factors = "*".join(variables[position] for position in monomial)
        magnitude = abs(coefficient)
        body = str(magnitude) if not factors else factors if magnitude == 1 else f"{magnitude}*{factors}"
        if not pieces:
            pieces.append(("-" if coefficient < 0 else "") + body)
        else:
            pieces.append(("-" if coefficient < 0 else "+") + body)
    return "".join(pieces)


def modular_rank(rows: list[dict[int, int]], columns: list[int], prime: int) -> int:
    relabel = {column: position for position, column in enumerate(columns)}
    echelon: dict[int, dict[int, int]] = {}
    for raw in rows:
        row = {relabel[column]: value % prime for column, value in raw.items() if column in relabel and value % prime}
        while row:
            column = min(row)
            if column not in echelon:
                inverse = pow(row[column], -1, prime)
                echelon[column] = {key: value * inverse % prime for key, value in row.items()}
                break
            factor = row[column]
            known = echelon[column]
            row = {key: (row.get(key, 0) - factor * known.get(key, 0)) % prime for key in set(row) | set(known)}
            row = {key: value for key, value in row.items() if value}
    return len(echelon)


def grading_rows_for(polys: list[Polynomial]) -> list[dict[int, int]]:
    rows = []
    for polynomial in polys:
        monomials = sorted(polynomial)
        base = Counter(monomials[0])
        for monomial in monomials[1:]:
            current = Counter(monomial)
            row = {position: base[position] - current[position] for position in set(base) | set(current)}
            row = {position: value for position, value in row.items() if value}
            if row:
                rows.append(row)
    return rows


sources_dir = HERE / "sources"
sources_dir.mkdir(exist_ok=True)
for stale in sources_dir.glob("*.sing"):
    stale.unlink()
cover_sources = []
for stage, (zeros, unit) in enumerate((((), cover_coordinate), ((cover_coordinate,), None))):
    assignments = {position: 0 for position in zeros}
    if unit is not None:
        assignments[unit] = 1
    polys, stats = branch(zeros, unit)
    remaining = [position for position in range(len(variables)) if position not in assignments]
    rows = grading_rows_for(polys)
    ranks = [modular_rank(rows, remaining, prime) for prime in (32003, 65521)]
    assert ranks[0] == ranks[1]
    exact_rank = len(remaining) if ranks[0] == len(remaining) else len(echelon_sparse(rows))
    assert exact_rank >= ranks[0]
    stats["grading_modular_ranks"] = ranks
    stats["grading_rank_over_Q"] = exact_rank
    stats["grading_nullity_over_Q"] = len(remaining) - exact_rank
    labels = [f"{variables[position]}0" for position in zeros]
    labels.append(f"{variables[unit]}1" if unit is not None else "closed")
    path = sources_dir / (f"stage{stage}_" + "_".join(labels) + "_Q_design.sing")
    program = "\n".join((
        "// EXACT Q DESIGN INPUT ONLY: no Singular/ideal run authorized.",
        "// Exact residual one-torus D/V cover; source-labelled specialization.",
        "option(noredefine);",
        f"ring r=0,({','.join(variables[position] for position in remaining)}),dp;",
        "ideal I=" + ",\n".join(serialize_polynomial(polynomial) for polynomial in polys) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ))
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(program)
    os.replace(temporary, path)
    rebuilt_variables, rebuilt_equations = parse_program(program)
    assert rebuilt_variables == [variables[position] for position in remaining]
    rebuilt = []
    for expression in rebuilt_equations:
        parser = PolynomialParser(expression, index)
        polynomial = parser.expression()
        assert parser.cursor == len(parser.tokens)
        rebuilt.append(polynomial)
    assert rebuilt == polys
    cover_sources.append({
        "stage": stage, "path": str(path.relative_to(HERE)), "sha256": sha(path),
        "zeros": [variables[position] for position in zeros], "unit": variables[unit] if unit is not None else None,
        "unit_weight": weight_vector[unit] if unit is not None else None, **stats,
    })

# Variable co-occurrence graph gives the exact source-level independent-block census.
adjacency = [set() for _ in variables]
for polynomial in polynomials:
    support = set(variable for monomial in polynomial for variable in monomial)
    for variable in support:
        adjacency[variable].update(support - {variable})
components = []
unseen = set(range(len(variables)))
while unseen:
    root = min(unseen)
    queue = deque([root])
    component = set()
    while queue:
        variable = queue.popleft()
        if variable in component:
            continue
        component.add(variable)
        queue.extend(adjacency[variable] - component)
    unseen -= component
    components.append(sorted(variables[position] for position in component))

# A source-variable appears affinely if its maximum exponent is one; this is not a
# graph elimination unless one of the unit-coefficient generator tests above passes.
affine_in_each_occurrence = sorted(variables[position] for position in range(len(variables)) if max_exponents[position] <= 1)
nonlinear_variables = sorted(set(variables) - set(affine_in_each_occurrence))

result = {
    "schema": "KRENN_X5_REP5_TORUS_SELECTED_FURTHER_REDUCTION_DESIGN_V1",
    "status": "PASS_EXACT_TWO_CHART_RESIDUAL_ONE_TORUS_COVER",
    "source": {"sha256": sha(SOURCE), "bytes": SOURCE.stat().st_size, "variables": 73, "generators": 6561, "field": "Q", "order": "dp"},
    "chart": {"assignment": {"yn1": 1, "yn2": 1, "t0": 1, "t2": 0}, "existing_cover_members": 16, "selected_member_only": True},
    "grading": {
        "constraint_rows": len(grading_rows), "rank": grading_rank, "nullity": grading_nullity,
        "basis": grading_basis, "nonzero_weights": grading_weights,
        "primitive_weight_one_coordinates": sorted(
            variables[position] for vector in grading_basis for position, weight in enumerate(vector) if abs(weight) == 1
        ),
        "residual_one_torus_detected": True,
    },
    "residual_torus_cover": {
        "identity": "D(q) union V(q)",
        "root_free": True,
        "selected_coordinate": variables[cover_coordinate],
        "selected_weight": weight_vector[cover_coordinate],
        "candidate_ledger": sorted(candidate_ledger, key=lambda entry: entry["coordinate"]),
        "objective": {
            "maximum_total_terms": cover_objective[0], "sum_total_terms": cover_objective[1],
            "maximum_generators": cover_objective[2], "sum_generators": cover_objective[3],
        },
        "forward": "on D(q), act by lambda=q^(-1/w) for primitive weight w=+/-1 to set q=1; V(q) is literal q=0",
        "reverse": "restore q=lambda^w and every coordinate x by x -> lambda^(weight(x))*x; no root extraction",
        "sources": cover_sources,
    },
    "expanded_polynomials": {
        "distinct_monomials": len(monomial_universe), "total_terms": sum(len(polynomial) for polynomial in polynomials),
        "term_count_min": min(map(len, polynomials)), "term_count_max": max(map(len, polynomials)),
        "term_count_histogram": dict(sorted(term_histogram.items())), "degree_histogram": dict(sorted(degree_histogram.items())),
    },
    "linear_reduction": {
        "amplitude_inactive_coordinates": inactive, "active_coordinates": len(variables) - len(inactive),
        "unit_coefficient_graph_substitutions": monic_candidates,
        "affine_linear_generator_count": len(affine_rows), "affine_linear_generator_rank": affine_linear_rank,
        "all_generator_linear_part_rank": linear_part_rank,
        "variables_affine_in_every_occurrence": affine_in_each_occurrence,
        "variables_with_nonlinear_occurrence": nonlinear_variables,
    },
    "block_structure": {"variable_interaction_components": len(components), "component_sizes": [len(component) for component in components], "components": components},
    "localization": {
        "existing_global_units_already_eliminated": ["beta", "abar", "a37_00", "t1", "sat", "d", "b2"],
        "existing_residual_D_or_V_assignments": {"yn1": "D/gauge=1", "yn2": "D/gauge=1", "t0": "D/gauge=1", "t2": "V/=0"},
        "new_reversible_minor_or_determinant_localization": False,
        "reason": "no additional determinant/minor is globally invertible; the only new exact reduction is the explicitly materialized two-chart residual one-torus cover",
    },
    "order": {
        "current": "dp", "exact_block_decomposition_available_before_cover": len(components) > 1,
        "block_order_performance_claim": False, "solver_benchmark_run": False,
        "note": "ordering can be benchmarked later but does not reduce the exact ideal or chart count",
    },
    "conclusion": {
        "smaller_exhaustive_cover_materialized": True,
        "cover_chart_count": 2,
        "reason": "one primitive residual torus survives on exactly six weight-one coordinates; D(q)/q=1 and V(q)/q=0 are exhaustive and root-free",
        "after_cover_all_chart_grading_nullities": [source["grading_nullity_over_Q"] for source in cover_sources],
        "after_cover_total_monic_graph_substitutions": sum(len(source["monic_graph_substitutions"]) for source in cover_sources),
        "after_cover_total_inactive_coordinates": sum(len(source["inactive"]) for source in cover_sources),
        "mathematical_coverage": False, "singular_runs": 0,
    },
}
temporary = HERE / "results_design.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_design.json")
print(json.dumps({
    "status": result["status"], "grading": [grading_rank, grading_nullity],
    "monic": len(monic_candidates), "inactive": len(inactive), "components": [len(component) for component in components],
    "terms": result["expanded_polynomials"]["total_terms"], "singular_runs": 0,
}, sort_keys=True))
