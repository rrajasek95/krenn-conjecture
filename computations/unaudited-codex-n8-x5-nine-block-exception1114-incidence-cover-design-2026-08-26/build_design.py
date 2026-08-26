#!/usr/bin/env python3
"""Exact design-only reduction of the four exceptional nine-block records."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
from math import gcd, lcm
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions are required by the builder")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-nine-block-residual538-max17-held-design-2026-08-26"
PINS = {
    "parent_manifest": (PARENT / "MANIFEST.sha256", "b5494d96a6850f44891c8d23503b06c04d758e5332a1008a75d0233fa8bd0f91"),
    "parent_result": (PARENT / "results_residual538_design.json", "412b54923e54cc284e0787e03e603b51fbf67af1d6b90e39b656aab206072d5b"),
    "parent_builder": (PARENT / "build_design.py", "e83c9ceea89ebbe48aab11b6f390b6215309503a1c0b1e98e2167add89b16566"),
}


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


for pin_name, (pin_path, expected) in PINS.items():
    require(pin_path.is_file(), (pin_name, "missing"))
    require(sha(pin_path) == expected, (pin_name, sha(pin_path), expected))

spec = importlib.util.spec_from_file_location("parent_exception_design", PINS["parent_builder"][0])
require(spec is not None and spec.loader is not None)
parent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent_module)
carrier = parent_module.carrier

FIXED = frozenset((tuple(map(int, edge)) for edge in ("03", "16", "27", "45")))
SUPPORT = frozenset((tuple(map(int, edge)) for edge in (
    "01", "03", "04", "16", "17", "25", "26", "27",
    "34", "35", "36", "37", "45", "46", "47", "67",
)))
MATRIX_EDGES = tuple(sorted("".join(map(str, edge)) for edge in SUPPORT - FIXED))
MATCHINGS = tuple(
    tuple(sorted("".join(map(str, edge)) for edge in matching))
    for matching in carrier.five.core.PM8 if set(matching) <= SUPPORT
)
require(len(MATCHINGS) == 15)


def matrix_name(edge, i, j):
    return f"a{edge}_{i}{j}"


def original_entry(edge, i, j):
    if tuple(map(int, edge)) in FIXED:
        return "1" if i == j else "0"
    return matrix_name(edge, i, j)


def add_expr(terms):
    kept = [term for term in terms if term not in ("0", "")]
    return "0" if not kept else "+".join(f"({term})" for term in kept)


def mul_expr(terms):
    if any(term == "0" for term in terms):
        return "0"
    kept = [term for term in terms if term != "1"]
    return "1" if not kept else "*".join(f"({term})" for term in kept)


def difference(value, target):
    if target == "0":
        return value
    return f"({value})-({target})"


def amplitude(entry, word):
    terms = []
    for matching in MATCHINGS:
        factors = []
        for edge in matching:
            p, q = map(int, edge)
            factors.append(entry(edge, word[p], word[q]))
        product = mul_expr(factors)
        if product != "0":
            terms.append(product)
    return add_expr(terms)


def full_x5_equations(entry):
    equations = []
    for word in itertools.product(range(3), repeat=8):
        target = "1" if len(set(word)) == 1 else "0"
        equations.append(difference(amplitude(entry, word), target))
    require(len(equations) == 6561)
    return equations


def transpose_product(left, right, i, j):
    return add_expr(mul_expr((matrix_name(left, i, k), matrix_name(right, j, k))) for k in range(3))


def original_guards():
    equations = []
    for i in range(3):
        for j in range(3):
            equations.append(add_expr((matrix_name("37", j, i), transpose_product("17", "36", i, j))))
            equations.append(add_expr((matrix_name("47", j, i), transpose_product("17", "46", i, j))))
            equations.append(add_expr((
                matrix_name("36", j, i),
                add_expr(mul_expr((matrix_name("26", i, k), matrix_name("37", j, k))) for k in range(3)),
            )))
            equations.append(add_expr((
                matrix_name("46", j, i),
                add_expr(mul_expr((matrix_name("26", i, k), matrix_name("47", j, k))) for k in range(3)),
            )))
            equations.append(add_expr((
                add_expr(mul_expr((matrix_name("36", i, k), matrix_name("47", j, k))) for k in range(3)),
                add_expr(mul_expr((matrix_name("37", i, k), matrix_name("46", j, k))) for k in range(3)),
            )))
    require(len(equations) == 45)
    return equations


def determinant(edge):
    a = lambda i, j: matrix_name(edge, i, j)
    positive = [mul_expr((a(0, 0), a(1, 1), a(2, 2))), mul_expr((a(0, 1), a(1, 2), a(2, 0))), mul_expr((a(0, 2), a(1, 0), a(2, 1)))]
    negative = [mul_expr((a(0, 2), a(1, 1), a(2, 0))), mul_expr((a(0, 1), a(1, 0), a(2, 2))), mul_expr((a(0, 0), a(1, 2), a(2, 1)))]
    return add_expr(positive + [f"-({term})" for term in negative])


def rank1_entry(edge, i, j):
    if tuple(map(int, edge)) in FIXED:
        return "1" if i == j else "0"
    if edge in ("01", "04", "17", "25", "26", "34", "35", "67"):
        return matrix_name(edge, i, j)
    vblock = {"36": "v36", "46": "v46"}
    if edge in vblock:
        return mul_expr(("1" if (edge == "36" and i == 0) else f"{vblock[edge]}_{i}", f"u{j}"))
    if edge in ("37", "47"):
        v = "1" if (edge == "37" and i == 0) else f"v{'36' if edge == '37' else '46'}_{i}"
        inner = add_expr(mul_expr((f"u{k}", matrix_name("17", j, k))) for k in range(3))
        return f"-({mul_expr((v, inner))})"
    raise RuntimeError(("unexpected edge", edge))


def rank1_program():
    matrix_variables = [matrix_name(edge, i, j) for edge in ("01", "04", "17", "25", "26", "34", "35", "67") for i in range(3) for j in range(3)]
    variables = matrix_variables + ["u0", "u1", "u2", "v36_1", "v36_2", "v46_0", "v46_1", "v46_2", "sat"]
    require(len(variables) == 81 and len(set(variables)) == 81)
    equations = full_x5_equations(rank1_entry)
    # M u = (I-A26*A17)u = 0, the residual of G23/G24 after H=u v^T.
    for i in range(3):
        correction = add_expr(
            mul_expr((matrix_name("26", i, j), matrix_name("17", j, k), f"u{k}"))
            for j in range(3) for k in range(3)
        )
        equations.append(f"u{i}-({correction})")
    # Both v halves are nonzero on this chart, so G34 is exactly this scalar.
    equations.append(add_expr(
        mul_expr((f"u{i}", add_expr((matrix_name("17", i, j), matrix_name("17", j, i))), f"u{j}"))
        for i in range(3) for j in range(3)
    ))
    nonzero = mul_expr((determinant("04"), determinant("17"), determinant("35"), determinant("26"), "u0", "v46_0", "sat"))
    equations.append(f"({nonzero})-1")
    require(len(equations) == 6566)
    lines = [
        "// HELD DESIGN INPUT ONLY: representative 1114, rank(H)=1 canonical chart; no ideal run authorized.",
        "option(noredefine);",
        f"ring r=0,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ]
    return "\n".join(lines), variables, equations


def carrier_ledger():
    ledger = []
    for cap in sorted(SUPPORT):
        residual = tuple(site for site in range(8) if site not in cap)
        definitions = [("triangle", defining) for defining in itertools.combinations(residual, 3)] + [("star", (center,)) for center in residual]
        for kind, defining in definitions:
            allowed = set(itertools.combinations(defining, 2)) if kind == "triangle" else {edge for edge in itertools.combinations(residual, 2) if defining[0] in edge}
            responses = []
            for response in itertools.combinations(residual, 2):
                if response in allowed:
                    continue
                terms = parent_module.response_terms(SUPPORT, cap, response)
                if terms:
                    responses.append({"response": "".join(map(str, response)), "terms": terms})
            ledger.append({
                "cap": "".join(map(str, cap)), "kind": kind, "defining": "".join(map(str, defining)),
                "load": sum(len(row["terms"]) for row in responses), "nonzero_forbidden_responses": responses,
            })
    require(len(ledger) == 416)
    require(Counter(row["load"] for row in ledger) == {2: 16, 3: 32, 4: 44, 5: 72, 6: 72, 7: 40, 8: 8, 10: 56, 11: 32, 12: 44})
    return ledger


PROFILE_LABELS = ("I", "C", "D0", "D1", "D2")


def permute_profile(profile, permutation):
    return tuple(label if label in ("I", "C") else f"D{permutation[int(label[1:])]}" for label in profile)


def incidence_orbits():
    raw = set(itertools.product(PROFILE_LABELS, repeat=4))
    group = tuple(itertools.permutations(range(3)))
    seen = set()
    orbits = []
    for profile in sorted(raw):
        if profile in seen:
            continue
        orbit = sorted({permute_profile(profile, permutation) for permutation in group})
        seen.update(orbit)
        n_i = profile.count("I")
        n_d = sum(label.startswith("D") for label in profile)
        n_c = profile.count("C")
        added = (1 if n_i else 0) + 3 * n_d + 9 * n_c
        orbits.append({
            "representative": list(profile), "members": [list(member) for member in orbit],
            "uncontracted_variables": 90 + added, "uncontracted_generators": 6588 + added,
        })
    require(len(seen) == 625 and len(orbits) == 150)
    require(Counter(len(row["members"]) for row in orbits) == {1: 16, 3: 65, 6: 69})
    return orbits


def h_minor_orbits():
    labels = tuple((block, color) for block in (36, 46) for color in range(3))
    group = tuple(itertools.permutations(range(3)))
    raw = set(itertools.combinations(labels, 3))
    seen = set()
    orbits = []
    for subset in sorted(raw):
        key = frozenset(subset)
        if key in seen:
            continue
        orbit = {frozenset((block, permutation[color]) for block, color in key) for permutation in group}
        seen.update(orbit)
        orbits.append({"representative": [list(item) for item in sorted(min(orbit, key=lambda value: sorted(value)))], "orbit_size": len(orbit)})
    require(len(seen) == 20 and len(orbits) == 6)
    require(Counter(row["orbit_size"] for row in orbits) == {1: 2, 3: 2, 6: 2})
    return orbits


def modular_independent_rows(rows, columns, prime=1000003):
    basis = {}
    selected = []
    for sparse in rows:
        row = [0] * columns
        for column, coefficient in sparse.items():
            row[column] = coefficient % prime
        while True:
            pivot = next((index for index, value in enumerate(row) if value), None)
            if pivot is None:
                break
            if pivot not in basis:
                inverse = pow(row[pivot], prime - 2, prime)
                basis[pivot] = [(value * inverse) % prime for value in row]
                selected.append(sparse)
                break
            factor = row[pivot]
            old = basis[pivot]
            row = [(left - factor * right) % prime for left, right in zip(row, old)]
    return selected


def grading_rank():
    variables = [matrix_name(edge, i, j) for edge in MATRIX_EDGES for i in range(3) for j in range(3)]
    index = {name: position for position, name in enumerate(variables)}
    rows = []

    def monomial(edge, i, j):
        if tuple(map(int, edge)) in FIXED:
            return () if i == j else None
        return (index[matrix_name(edge, i, j)],)

    for word in itertools.product(range(3), repeat=8):
        coefficients = Counter()
        for matching in MATCHINGS:
            current = []
            for edge in matching:
                p, q = map(int, edge)
                value = monomial(edge, word[p], word[q])
                if value is None:
                    current = None
                    break
                current += value
            if current is not None:
                coefficients[tuple(sorted(current))] += 1
        if len(set(word)) == 1:
            coefficients[()] -= 1
        monomials = [monomial_value for monomial_value, coefficient in coefficients.items() if coefficient]
        if monomials:
            reference = monomials[0]
            for value in monomials[1:]:
                row = Counter(value)
                row.subtract(reference)
                rows.append({key: coefficient for key, coefficient in row.items() if coefficient})
    # Guard homogeneity constraints can be generated directly from their source monomials.
    guard_terms = []
    for i in range(3):
        for j in range(3):
            guard_terms.extend([
                [(index[matrix_name("37", j, i)],)] + [tuple(sorted((index[matrix_name("17", i, k)], index[matrix_name("36", j, k)]))) for k in range(3)],
                [(index[matrix_name("47", j, i)],)] + [tuple(sorted((index[matrix_name("17", i, k)], index[matrix_name("46", j, k)]))) for k in range(3)],
                [(index[matrix_name("36", j, i)],)] + [tuple(sorted((index[matrix_name("26", i, k)], index[matrix_name("37", j, k)]))) for k in range(3)],
                [(index[matrix_name("46", j, i)],)] + [tuple(sorted((index[matrix_name("26", i, k)], index[matrix_name("47", j, k)]))) for k in range(3)],
                [tuple(sorted((index[matrix_name("36", i, k)], index[matrix_name("47", j, k)]))) for k in range(3)] + [tuple(sorted((index[matrix_name("37", i, k)], index[matrix_name("46", j, k)]))) for k in range(3)],
            ])
    for terms in guard_terms:
        reference = terms[0]
        for value in terms[1:]:
            row = Counter(value)
            row.subtract(reference)
            rows.append({key: coefficient for key, coefficient in row.items() if coefficient})
    selected = modular_independent_rows(rows, len(variables))
    require(len(selected) == 98)
    matrix = [[Fraction(row.get(column, 0)) for column in range(len(variables))] for row in selected]
    pivot_columns = []
    pivot_row = 0
    for column in range(len(variables)):
        selected_row = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column]), None)
        if selected_row is None:
            continue
        matrix[pivot_row], matrix[selected_row] = matrix[selected_row], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [value / divisor for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [left - factor * right for left, right in zip(matrix[row], matrix[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
    require(len(pivot_columns) == 98)
    free_columns = [column for column in range(len(variables)) if column not in pivot_columns]
    integer_basis = []
    for free in free_columns:
        vector = [Fraction(0) for _ in variables]
        vector[free] = 1
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -matrix[row][free]
        denominator = 1
        for value in vector:
            denominator = lcm(denominator, value.denominator)
        integers = [int(value * denominator) for value in vector]
        common = 0
        for value in integers:
            common = gcd(common, abs(value))
        require(common > 0)
        integers = [value // common for value in integers]
        require(all(sum(coefficient * integers[column] for column, coefficient in row.items()) == 0 for row in rows))
        integer_basis.append({variables[column]: value for column, value in enumerate(integers) if value})
    require(len(integer_basis) == 10)
    basis_path = HERE / "torus_nullspace_basis.json"
    basis_path.write_text(json.dumps({"variable_order": variables, "basis": integer_basis}, indent=2, sort_keys=True) + "\n")
    return {
        "variables": 108, "homogeneity_constraints": len(rows), "rank_over_p1000003": 98,
        "exact_rank_over_Q": 98, "torus_nullity": 10,
        "rank_proof": "98 rows are independent modulo 1000003 (hence over Q); ten independent primitive integer null vectors replay every integer constraint (hence rank at most 98)",
        "nullspace_basis_path": basis_path.name, "nullspace_basis_sha256": sha(basis_path),
    }


def make_result():
    parent = json.loads(PINS["parent_result"][0].read_text())
    exceptions = parent["exact16_no_degree4"]
    require(exceptions["representative_record"] == 1114)
    require(set(exceptions["transport_from_representative"]) == {"1114", "1978", "2014", "2036"})
    representative = next(record for record in exceptions["records_detail"] if record["record_index"] == 1114)
    require(tuple(representative["supported_perfect_matchings"]) == tuple("|".join(matching) for matching in MATCHINGS))

    ledger = carrier_ledger()
    minimum = [row for row in ledger if row["load"] == 2]
    require(len(minimum) == 16)
    minimum_by_key = {(row["cap"], row["kind"], row["defining"]): row for row in minimum}
    selected_factorizations = {
        "F04": minimum_by_key[("01", "star", "3")],
        "F17": minimum_by_key[("01", "star", "6")],
        "F26": minimum_by_key[("25", "star", "7")],
        "F35": minimum_by_key[("25", "star", "4")],
    }
    require(selected_factorizations["F04"]["nonzero_forbidden_responses"] == [
        {"response": "46", "terms": [{"kind": "direct", "source_edges": ["04", "16"]}]},
        {"response": "47", "terms": [{"kind": "direct", "source_edges": ["04", "17"]}]},
    ])
    require(selected_factorizations["F17"]["nonzero_forbidden_responses"] == [
        {"response": "37", "terms": [{"kind": "direct", "source_edges": ["03", "17"]}]},
        {"response": "47", "terms": [{"kind": "direct", "source_edges": ["04", "17"]}]},
    ])
    require(selected_factorizations["F26"]["nonzero_forbidden_responses"] == [
        {"response": "36", "terms": [{"kind": "switched", "source_edges": ["26", "35"]}]},
        {"response": "46", "terms": [{"kind": "switched", "source_edges": ["26", "45"]}]},
    ])
    require(selected_factorizations["F35"]["nonzero_forbidden_responses"] == [
        {"response": "36", "terms": [{"kind": "switched", "source_edges": ["26", "35"]}]},
        {"response": "37", "terms": [{"kind": "switched", "source_edges": ["27", "35"]}]},
    ])
    carrier_path = HERE / "carrier_ledger.json"
    carrier_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    full_equations = full_x5_equations(original_entry)
    guards = original_guards()
    program, variables, rank1_equations = rank1_program()
    program_path = HERE / "rep1114_rank1_canonical_Q.sing"
    temporary = program_path.with_suffix(".sing.tmp")
    temporary.write_text(program)
    os.replace(temporary, program_path)

    incidence = incidence_orbits()
    incidence_path = HERE / "incidence_cover_ledger.json"
    incidence_path.write_text(json.dumps(incidence, indent=2, sort_keys=True) + "\n")
    minors = h_minor_orbits()

    held = {
        "schema": "n8-x5-rep1114-rank1-smallest-q-held-v1",
        "status": "HELD_DESIGN_ONLY_NO_CLEARANCE",
        "scope": "record1114 and its exact four-record source-site transport orbit; canonical rank(H)=1 chart only",
        "dependencies": {"independent_design_referee_manifest": None, "max16_terminal_resource_clear": None, "explicit_launch_clearance": None},
        "source": {"path": program_path.name, "sha256": sha(program_path), "variables": len(variables), "generators": len(rank1_equations), "ring": "Q"},
        "chart": {
            "H": "[A36^T|A46^T]=u*(v36^T|v46^T)", "normalization": "v36_0=1",
            "nonzero_factors": ["det(A04)", "det(A17)", "det(A35)", "det(A26)", "u0", "v46_0"],
            "combined_saturation": "det(A04)*det(A17)*det(A35)*det(A26)*u0*v46_0*sat-1",
        },
        "future_acceptance": "only a proof-producing exact-Q UNIT_IDEAL transcript with reduce(1,G)=0 and literal regeneration/replay; any other outcome is diagnostic zero coverage",
        "refusal": "no Singular, modular pilot, Q solve, sibling chart, or transport promotion without all dependencies and a fresh clearance",
    }
    held_path = HERE / "held_smallest_chart_plan.json"
    held_path.write_text(json.dumps(held, indent=2, sort_keys=True) + "\n")

    result = {
        "schema": "n8-x5-nine-block-exception1114-incidence-cover-design-v1",
        "status": "PASS_DESIGN_ONLY_ZERO_IDEAL_RUNS",
        "pins": {name: {"path": str(path), "sha256": expected} for name, (path, expected) in PINS.items()},
        "transport": {
            "representative": 1114, "records": [1114, 1978, 2014, 2036], "orbit_count": 1,
            "site_maps": exceptions["transport_from_representative"], "group_order": exceptions["source_site_transport_group_order"],
            "proof": exceptions["transport_proof"],
            "scope_guard": "site relabeling transports each record's source-labelled carrier/guard instance; it is not used to identify distinct incidence profiles inside record1114",
        },
        "source_system": {
            "support": sorted("".join(map(str, edge)) for edge in SUPPORT), "fixed_identity_edges": ["03", "16", "27", "45"],
            "matrix_edges": list(MATRIX_EDGES), "matrix_variables_before_reduction": 108,
            "supported_matchings": ["|".join(matching) for matching in MATCHINGS], "matching_count": 15,
            "entry_convention": "matching m contributes product Auv[c_u,c_v], fixed 03/16/27/45 are I3, and the sum equals GHZ on every word in {0,1,2}^8",
            "full_x5_equations": 6561, "full_x5_equation_sha256": canonical_hash(full_equations),
            "guards": [
                "A37^T+A17*A36^T=0", "A47^T+A17*A46^T=0",
                "A26*A37^T+A36^T=0", "A26*A47^T+A46^T=0",
                "A36*A47^T+A37*A46^T=0",
            ],
            "guard_scalar_equations": 45, "guard_equation_sha256": canonical_hash(guards),
        },
        "linear_reduction": {
            "substitutions": ["A37=-A36*A17^T", "A47=-A46*A17^T"],
            "remaining_matrices": ["A01", "A04", "A17", "A25", "A26", "A34", "A35", "A36", "A46", "A67"],
            "variables": 90,
            "residual_guards": ["(I-A26*A17)*A36^T=0", "(I-A26*A17)*A46^T=0", "A36*(A17+A17^T)*A46^T=0"],
            "residual_guard_scalars": 27, "base_generators_with_full_x5": 6588,
        },
        "carriers": {
            "all_supported_carriers": 416, "load_histogram": {str(key): value for key, value in sorted(Counter(row["load"] for row in ledger).items())},
            "minimum_load": 2, "minimum_carriers": 16, "ledger_path": carrier_path.name, "ledger_sha256": sha(carrier_path),
            "selected_factorization_source_terms": selected_factorizations,
            "selected_literal_maps": {
                "F04": "cap01/star3: (R46,R47)=(A04^T*K, A04^T*K*A17)",
                "F17": "cap01/star6: (R37,R47)=(K*A17, A04^T*K*A17); transpose K/output for the unified factor",
                "F26": "cap25/star7: (R36,R46)=(A35*K^T*A26, K^T*A26)",
                "F35": "cap25/star4: (R36,R37)=(A35*K^T*A26, A35*K^T); transpose K/output for the unified factor",
            },
            "useful_oriented_factors": {
                "F04": {"factor": "A04", "cap_coefficient": "A01", "annihilator": "Col(A04) tensor Q3"},
                "F17": {"factor": "A17", "cap_coefficient": "A01^T", "annihilator": "Col(A17) tensor Q3 after output/K transpose"},
                "F26": {"factor": "A26", "cap_coefficient": "A25", "annihilator": "Col(A26) tensor Q3"},
                "F35": {"factor": "A35^T", "cap_coefficient": "A25^T", "annihilator": "Col(A35^T) tensor Q3"},
            },
            "activity_criterion": "for each oriented pair (F,C), the carrier is active iff rank(F)<3, every e_i is outside Col(F), and Col(C) is not contained in Col(F)",
        },
        "rank_and_incidence_cover": {
            "factor_order": ["F04", "F17", "F26", "F35"],
            "per_factor_failure_labels": {"I": "det(F)!=0", "D_i": "F*x=e_i", "C": "F*Y=C"},
            "logical_equivalence": "a useful carrier fails activity exactly on the union I or some D_i or C; taking the product over four factors gives 5^4 raw profiles",
            "raw_profiles": 625, "simultaneous_color_S3_orbits": 150,
            "orbit_size_census": {"1": 16, "3": 65, "6": 69},
            "ledger_path": incidence_path.name, "ledger_sha256": sha(incidence_path),
            "uncontracted_count_range": {"variables": [91, 126], "generators": [6589, 6624]},
            "cramer": {
                "axis_chart": "choose x_r!=0, set w=x/x_r with w_r=1 and alpha=1/x_r, substitute F[:,r]=alpha*e_i-sum_{j!=r}F[:,j]w_j",
                "reverse": "alpha!=0 gives x=w/alpha and exactly F*x=e_i",
                "containment": "substitute C=F*Y; if both factors share C, substitute once and retain the second equality",
                "raw_pivot_charts": 14641, "S3_orbits": 2486,
                "verdict": "exact but expands the cover and does not improve the global minimum 91/6589 before the H-rank split",
            },
        },
        "H_rank_split_inside_all_invertible": {
            "H": "[A36^T|A46^T]", "guard": "(I-A26*A17)*H=0", "exact_support_excludes_rank0": True,
            "rank3": {
                "raw_minor_charts": 20, "S3_minor_orbits": 6, "minor_orbits": minors,
                "consequence": "rank(H)=3 forces A26*A17=I; set A26=u*adj(A17), u*det(A17)=1",
                "counts_after_substitution": {"variables": 83, "generators": 6572},
            },
            "rank2": {
                "exact_parameterization": "H=U*V, U is 3x2; choose a nonzero U row minor, gauge it to I2, and choose a nonzero V column minor",
                "full_half_rank_subcharts": {"raw": 27, "S3_orbits": 5, "variables": 87, "generators": 6572},
                "boundary": "rank(V36),rank(V46) in {(2,1),(1,2),(1,1)} remains a finite lower-dimensional split",
            },
            "rank1": {
                "parameterization": "H=u*(v36^T|v46^T), normalize one v entry; exact support requires both v halves nonzero",
                "raw_charts": 54, "S3_orbits": 10,
                "residual_guards": ["(I-A26*A17)u=0", "u^T*(A17+A17^T)*u=0"],
                "counts": {"variables": 81, "generators": 6566},
                "selected_canonical_chart": {"v36_0": 1, "nonzero_u": "u0", "nonzero_other_half": "v46_0"},
            },
            "rank_le2_fail_closed_chart": {"variables": 91, "generators": 6609, "extra_equations": "all twenty 3x3 minors of H"},
            "refined_complete_cover": {"raw_branches": 645, "S3_orbit_branches": 156, "derivation": "replace the all-I profile by one rank(H)<=2 branch and the 20 rank3 minor charts (6 S3 orbits)"},
        },
        "torus": {
            **grading_rank(),
            "block_scaling_subtorus_dimension": 4,
            "unimodular_block_pivots_example": ["A04", "A17", "A36", "A67"],
            "decision": "normalizing entries requires a nonzero-entry cover (already 9^4 raw/1094 S3 orbits for the four block pivots) and cross-multiplication with the incidence cover; it is exact but not the smallest finite cover and was not materialized",
        },
        "held_smallest_chart": {"plan_path": held_path.name, "plan_sha256": sha(held_path), "source_path": program_path.name, "source_sha256": sha(program_path), "variables": 81, "generators": 6566},
        "scope": {"transport_orbits": 1, "ideal_runs": 0, "singular_runs": 0, "large_cnf_reads": 0, "records_closed": 0, "conjecture_claim": False},
    }
    return result


if __name__ == "__main__":
    output = make_result()
    result_path = HERE / "results_exception1114_design.json"
    result_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": output["status"], "incidence_orbits": output["rank_and_incidence_cover"]["simultaneous_color_S3_orbits"],
        "refined_orbits": output["H_rank_split_inside_all_invertible"]["refined_complete_cover"]["S3_orbit_branches"],
        "held": output["held_smallest_chart"], "scope": output["scope"],
    }, indent=2, sort_keys=True))
