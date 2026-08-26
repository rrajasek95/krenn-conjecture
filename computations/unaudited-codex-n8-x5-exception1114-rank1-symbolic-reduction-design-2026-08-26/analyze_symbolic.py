#!/usr/bin/env python3
"""Exact/design-only diagnostics for the sealed exception-1114 58-variable chart."""

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-exception1114-rank1-refinement-design-2026-08-26"
PINS = {
    "manifest": (PARENT / "MANIFEST.sha256", "aea0841b7b1b6fe0773cfb5087a930329c4da5d94951ad23d559de6d61cddb46"),
    "result": (PARENT / "results_rank1_refinement.json", "3da9583ca3c8ed49b0983960f1147238def7fe19b43905f3d5cef57811c6e99b"),
    "builder": (PARENT / "build_refinement.py", None),
    "source": (PARENT / "rep1114_rank1_z1_fulltorus_Q.sing", "7b20f216cf2313f7abe82f4c1b29d7084a5a82716e457f1554262c5e46ce82f8"),
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


for label, (path, expected) in PINS.items():
    if not path.is_file() or (expected is not None and sha(path) != expected):
        raise RuntimeError((label, path, sha(path) if path.is_file() else None, expected))

spec = importlib.util.spec_from_file_location("sealed_refinement", PINS["builder"][0])
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import sealed builder")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
V = b.VARIABLES
INDEX = {name: i for i, name in enumerate(V)}


def coefficient_mod(value, prime):
    return value.numerator * pow(value.denominator, prime - 2, prime) % prime


def jacobian(equations, values, prime):
    rows = []
    for equation in equations:
        row = [0] * len(V)
        for monomial, coefficient in equation.items():
            powers = Counter(monomial)
            coefficient = coefficient_mod(coefficient, prime)
            for name, exponent in powers.items():
                # Product rule without division, hence valid even at zero coordinates.
                term = coefficient * exponent % prime
                for other, other_exponent in powers.items():
                    term = term * pow(values[other], other_exponent - (other == name), prime) % prime
                row[INDEX[name]] = (row[INDEX[name]] + term) % prime
        rows.append(row)
    return rows


def rref(rows, columns, prime):
    basis = {}
    source_rows = {}
    for source_index, dense in enumerate(rows):
        row = [x % prime for x in dense]
        while True:
            pivot = next((i for i, x in enumerate(row) if x), None)
            if pivot is None:
                break
            if pivot not in basis:
                inverse = pow(row[pivot], prime - 2, prime)
                basis[pivot] = [(x * inverse) % prime for x in row]
                source_rows[pivot] = source_index
                break
            factor = row[pivot]
            old = basis[pivot]
            row = [(x - factor * y) % prime for x, y in zip(row, old)]
        if len(basis) == columns:
            break
    return basis, source_rows


def right_null_vector(basis, columns, prime):
    free = [i for i in range(columns) if i not in basis]
    if len(free) != 1:
        return None
    f = free[0]
    result = [0] * columns
    result[f] = 1
    for pivot in sorted(basis, reverse=True):
        result[pivot] = -sum(basis[pivot][j] * result[j] for j in range(pivot + 1, columns)) % prime
    return result


def determinant_mod(matrix, prime):
    matrix = [[x % prime for x in row] for row in matrix]
    answer = 1
    for column in range(len(matrix)):
        pivot = next((row for row in range(column, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            answer = -answer % prime
        value = matrix[column][column]
        answer = answer * value % prime
        inverse = pow(value, prime - 2, prime)
        matrix[column] = [x * inverse % prime for x in matrix[column]]
        for row in range(column + 1, len(matrix)):
            factor = matrix[row][column]
            if factor:
                matrix[row] = [(x - factor * y) % prime for x, y in zip(matrix[row], matrix[column])]
    return answer


def sparse_nonlinear_rank(equations, prime=1000003):
    """Rank of generator rows restricted to monomials of degree >=2."""
    basis = {}
    max_terms = 0
    for equation in equations:
        row = {m: coefficient_mod(c, prime) for m, c in equation.items() if len(m) >= 2}
        row = {m: c for m, c in row.items() if c}
        while row:
            # Degree-first lex is a legal fixed column order.  A full row rank
            # certificate is independent of the chosen ordering.
            pivot = max(row, key=lambda m: (len(m), m))
            if pivot not in basis:
                inverse = pow(row[pivot], prime - 2, prime)
                row = {m: c * inverse % prime for m, c in row.items()}
                basis[pivot] = row
                max_terms = max(max_terms, len(row))
                break
            factor = row[pivot]
            old = basis[pivot]
            for monomial, coefficient in old.items():
                row[monomial] = (row.get(monomial, 0) - factor * coefficient) % prime
                if not row[monomial]:
                    del row[monomial]
        if len(basis) == len(equations):
            break
    return {"prime": prime, "rank": len(basis), "rows": len(equations), "maximum_echelon_row_terms": max_terms}


def localized_monic_scan(equations):
    individually_invertible = {"a04_00", "v36_0", "v46_0", "sat"}
    determinant_units = {
        edge: b.determinant(edge, b.final_entry) for edge in ("04", "17", "35", "26")
    }

    def normalize(poly):
        if not poly:
            return None
        first = poly[min(poly, key=lambda monomial: (len(monomial), monomial))]
        return tuple(sorted((monomial, coefficient / first) for monomial, coefficient in poly.items()))

    determinant_signatures = {normalize(poly): edge for edge, poly in determinant_units.items()}
    hits = []
    for equation_index, equation in enumerate(equations):
        for name in V:
            containing = [(monomial, coefficient) for monomial, coefficient in equation.items() if name in monomial]
            if not containing or any(monomial.count(name) != 1 for monomial, _ in containing):
                continue
            coefficients = []
            for monomial, coefficient in containing:
                reduced = list(monomial)
                reduced.remove(name)
                coefficients.append((tuple(reduced), coefficient))
            coefficient_poly = {monomial: coefficient for monomial, coefficient in coefficients}
            unit_reason = None
            if len(coefficients) == 1 and set(coefficients[0][0]) <= individually_invertible:
                unit_reason = "invertible coordinate monomial"
            else:
                common = Counter(coefficients[0][0])
                for monomial, _ in coefficients[1:]:
                    common &= Counter(monomial)
                common_invertible = Counter({name: power for name, power in common.items() if name in individually_invertible})
                reduced_poly = {}
                for monomial, coefficient in coefficients:
                    remainder = list(monomial)
                    for factor, power in common_invertible.items():
                        for _ in range(power):
                            remainder.remove(factor)
                    reduced_poly[tuple(sorted(remainder))] = coefficient
                edge = determinant_signatures.get(normalize(reduced_poly))
                if edge is not None:
                    unit_reason = f"det(A{edge}) times invertible coordinate monomial"
            if unit_reason is not None:
                hits.append({
                    "equation": equation_index,
                    "variable": name,
                    "localized_coefficient_monomial": list(coefficients[0][0]),
                    "coefficient": str(coefficients[0][1]),
                    "terms": len(equation),
                    "unit_reason": unit_reason,
                })
    return {
        "hits": hits,
        "individually_invertible_coordinates": sorted(individually_invertible),
        "determinant_units": sorted(determinant_units),
        "proof_scope": "literal one-generator eliminations whose coefficient is a localized determinant times a monomial in individually localized coordinates",
    }


def rank_strata_design():
    matrices = ("A01", "A25", "A67")
    return {
        "optional_matrices": list(matrices),
        "normalized_entry": "each has A[0,0]=1, hence rank zero is excluded",
        "per_matrix_exact_cover": {
            "rank1": "all nine 2x2 minors vanish; Aij=Ai0*A0j gives four parameters instead of eight",
            "rank2": "det(A)=0 and one of nine 2x2 minors is nonzero (nine overlapping Cramer charts)",
            "rank3": "det(A)!=0",
        },
        "rank_profiles": 27,
        "raw_minor_charts": 11 ** 3,
        "variable_counts_by_number_rank1_blocks": {"0": 58, "1": 54, "2": 50, "3": 46},
        "verdict": "only rank1 strata shrink; the rank2/rank3 branches remain 58-variable, so this is not a uniformly smaller exact cover",
    }


def source_site_symmetry():
    import itertools
    fixed = {tuple(map(int, edge)) for edge in ("03", "16", "27", "45")}
    active = {tuple(map(int, edge)) for edge in ("04", "35", "67")}
    support = {tuple(map(int, edge)) for edge in ("01", "03", "04", "16", "17", "25", "26", "27", "34", "35", "36", "37", "45", "46", "47", "67")}

    def edge_map(edge, permutation):
        return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))

    def set_map(edges, permutation):
        return {edge_map(edge, permutation) for edge in edges}

    group = [permutation for permutation in itertools.permutations(range(8)) if set_map(fixed, permutation) == fixed and set_map(active, permutation) == active]
    stabilizer = [permutation for permutation in group if set_map(support, permutation) == support]
    images = [{
        "permutation": list(permutation),
        "cap67_image": list(edge_map((6, 7), permutation)),
        "triangle012_image": sorted(permutation[i] for i in (0, 1, 2)),
    } for permutation in stabilizer]
    return {
        "full_source_site_group_order": len(group),
        "record1114_support_stabilizer_order": len(stabilizer),
        "stabilizer_images": images,
        "formal_guard_stabilizer_order": sum(row["cap67_image"] == [6, 7] and row["triangle012_image"] == [0, 1, 2] for row in images),
        "conclusion": "the sole nonidentity record stabilizer fixes cap67 but sends triangle012 to triangle125, so it does not act on the fixed formal-guard/rank1 chart; no further site quotient of the 1094 residual-colour orbits is certified",
    }


def random_values(prime, seed):
    rng = random.Random(seed)
    return {name: rng.randrange(prime) for name in V}


def linear_elimination_profile(equations):
    """Constant-coefficient echelon profile, without polynomial multiplication."""
    # Any exact Q-linear combination lives in the coefficient row span.  Row-reduce
    # sparse equations by a monomial order that puts nonlinear monomials before
    # linear variables; a row supported on {1,x} is a valid affine substitution.
    monomials = sorted(
        {m for equation in equations for m in equation},
        key=lambda m: (len(m) <= 1, -len(m), m),
    )
    column = {m: i for i, m in enumerate(monomials)}
    # Only rows with modest support can cheaply enter exact sparse elimination.
    candidates = [(i, e) for i, e in enumerate(equations) if len(e) <= 32]
    basis = {}
    provenance = {}
    hits = []
    for equation_index, equation in candidates:
        row = {column[m]: c for m, c in equation.items()}
        while row:
            pivot = min(row)
            if pivot not in basis:
                factor = row[pivot]
                row = {j: c / factor for j, c in row.items()}
                basis[pivot] = row
                provenance[pivot] = equation_index
                break
            factor = row[pivot]
            old = basis[pivot]
            for j, c in old.items():
                row[j] = row.get(j, 0) - factor * c
                if not row[j]:
                    del row[j]
        if row:
            support = [monomials[j] for j in row]
            linear = [m for m in support if len(m) == 1 and m[0] in INDEX]
            nonlinear = [m for m in support if len(m) > 1]
            if len(linear) == 1 and not nonlinear:
                hits.append({"source_equation": equation_index, "variable": linear[0][0], "terms": len(row)})
    return {
        "monomial_columns": len(monomials),
        "candidate_rows_terms_le_32": len(candidates),
        "echelon_rank": len(basis),
        "affine_monic_hits": hits,
        "scope": "exact Q-linear combinations of equations having <=32 terms; no polynomial multiples",
    }


def main():
    equations = b.all_equations()
    primes = (1000003, 1000033)
    trials = []
    full_minor = None
    for prime in primes:
        value_sets = [
            ("offset2", {name: i + 2 for i, name in enumerate(V)}),
            ("offset101", {name: i + 101 for i, name in enumerate(V)}),
        ] + [(f"random{seed}", random_values(prime, seed)) for seed in range(1, 7)]
        for label, values in value_sets:
            rows = jacobian(equations, values, prime)
            basis, source_rows = rref(rows, len(V), prime)
            null = right_null_vector(basis, len(V), prime)
            trial = {
                "prime": prime,
                "point": label,
                "rank": len(basis),
                "pivot_source_rows": [source_rows[i] for i in sorted(source_rows)],
            }
            if null is not None:
                trial["right_null_nonzero"] = {V[i]: x for i, x in enumerate(null) if x}
            trials.append(trial)
            if len(basis) == len(V) and full_minor is None:
                selected = [source_rows[i] for i in range(len(V))]
                determinant = determinant_mod([rows[i] for i in selected], prime)
                if determinant == 0:
                    raise RuntimeError("selected full-rank rows unexpectedly singular")
                full_minor = {
                    "prime": prime,
                    "point": label,
                    "point_rule": "python random.Random(seed).randrange(prime) in VARIABLES order" if label.startswith("random") else "VARIABLES index plus displayed offset",
                    "point_value_sha256": hashlib.sha256(json.dumps([values[name] for name in V], separators=(",", ":")).encode()).hexdigest(),
                    "source_equation_indices": selected,
                    "determinant_mod_prime": determinant,
                    "proof": "the selected 58x58 Jacobian minor is nonzero modulo this prime, hence its integer/rational determinant is nonzero",
                }
    ranks = Counter(trial["rank"] for trial in trials)
    if full_minor is None:
        conclusion = "NO_FULL_RANK_MINOR_FOUND"
    else:
        conclusion = "GENERIC_JACOBIAN_FULL_RANK_CERTIFIED"
    result = {
        "status": "PASS_DESIGN_ONLY",
        "parent_manifest": PINS["manifest"][1],
        "parent_source_sha256": PINS["source"][1],
        "variables": len(V),
        "generators": len(equations),
        "jacobian": {
            "conclusion": conclusion,
            "rank_histogram": {str(k): v for k, v in sorted(ranks.items())},
            "trials": trials,
            "full_rank_minor": full_minor,
        },
        "linear_elimination": linear_elimination_profile(equations),
        "nonlinear_row_independence": sparse_nonlinear_rank(equations),
        "localized_monic_scan": localized_monic_scan(equations),
        "determinantal_rank_strata": rank_strata_design(),
        "source_site_symmetry": source_site_symmetry(),
    }
    path = HERE / "symbolic_diagnostics.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"conclusion": conclusion, "ranks": result["jacobian"]["rank_histogram"], "linear": result["linear_elimination"]}, indent=2))


if __name__ == "__main__":
    main()
