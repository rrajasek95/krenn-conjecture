#!/usr/bin/env python3
"""Design-only exact refinement of the sealed representative-1114 rank-one chart."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-nine-block-exception1114-incidence-cover-design-2026-08-26"
PINS = {
    "parent_manifest": (PARENT / "MANIFEST.sha256", "ef1ce39252f0a0f45811f40c9c5eeede027ee17d03ea42df17ef42d5304720ab"),
    "parent_result": (PARENT / "results_exception1114_design.json", "210de2136a12a8a87faf51af77ff7c91a0103befc0ae54839d3220c481c503b6"),
    "parent_source": (PARENT / "rep1114_rank1_canonical_Q.sing", "273a246e6cd8747401da95f56086686bd9b0b91ae70e1c54671c1aaca8b311e6"),
    "parent_builder": (PARENT / "build_design.py", "89c6e6b21d47a11f57aeedb2cf30c910d36fc00377637113fdd4f32d56bf523a"),
    "parent_torus_basis": (PARENT / "torus_nullspace_basis.json", "38ae09a1f7074e477ae27f68d465944c6ebb683663d0332a6da50faf8be81a55"),
}


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


for pin_name, (pin_path, expected) in PINS.items():
    require(pin_path.is_file() and sha(pin_path) == expected, (pin_name, pin_path))

spec = importlib.util.spec_from_file_location("parent_rank1_design", PINS["parent_builder"][0])
require(spec is not None and spec.loader is not None)
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)

MATCHINGS = parent.MATCHINGS
FIXED = parent.FIXED
M34 = ("01", "25", "34", "67")
require(M34 in MATCHINGS)

# Sparse exact polynomials: monomial tuple of variable names -> rational coefficient.
def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def const(value):
    value = Fraction(value)
    return {(): value} if value else {}


def var(name):
    return {(name,): Fraction(1)}


def add(*polys):
    result = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def scale(poly, coefficient):
    return clean({monomial: Fraction(coefficient) * value for monomial, value in poly.items()})


def mul(*polys):
    result = {(): Fraction(1)}
    for poly in polys:
        next_result = {}
        for left, left_coefficient in result.items():
            for right, right_coefficient in poly.items():
                monomial = tuple(sorted(left + right))
                next_result[monomial] = next_result.get(monomial, 0) + left_coefficient * right_coefficient
        result = clean(next_result)
    return result


ONE = const(1)
ZERO = const(0)

NORMALIZED = {
    "a01_00", "a25_00", "a67_00",  # exact four-dimensional block-torus cover
    # The six full-torus coordinates below were chosen to include every
    # proper common factor exposed after the monic reductions.
    "a35_00", "a35_10", "a35_20", "a04_01", "a04_02", "a26_12",
}


def raw_matrix(edge, i, j):
    name = f"a{edge}_{i}{j}"
    return ONE if name in NORMALIZED else var(name)


U = (ONE, var("u1"), var("u2"))


def z2_poly():
    return add(*(mul(raw_matrix("17", 2, k), U[k]) for k in range(3)))


def a17_entry(i, j):
    # The z1=1 block-torus normalization eliminates a17_10.
    if i == 1 and j == 0:
        return add(ONE, scale(mul(raw_matrix("17", 1, 1), U[1]), -1), scale(mul(raw_matrix("17", 1, 2), U[2]), -1))
    # u^T A17 u = z0+u1*z1+u2*z2=0 eliminates a17_00.
    if i == 0 and j == 0:
        return add(
            scale(U[1], -1), scale(mul(U[2], z2_poly()), -1),
            scale(mul(raw_matrix("17", 0, 1), U[1]), -1),
            scale(mul(raw_matrix("17", 0, 2), U[2]), -1),
        )
    return raw_matrix("17", i, j)


def z_poly(i):
    return add(*(mul(a17_entry(i, k), U[k]) for k in range(3)))


require(z_poly(1) == ONE)
require(add(z_poly(0), mul(U[1], z_poly(1)), mul(U[2], z_poly(2))) == ZERO)


def a26_entry(i, j):
    # z1=1 makes the three equations A26*z=u monic in column one.
    if j == 1:
        return add(
            U[i], scale(mul(raw_matrix("26", i, 0), z_poly(0)), -1),
            scale(mul(raw_matrix("26", i, 2), z_poly(2)), -1),
        )
    return raw_matrix("26", i, j)


def entry_without_a34(edge, i, j):
    if tuple(map(int, edge)) in FIXED:
        return ONE if i == j else ZERO
    if edge in ("01", "04", "25", "35", "67"):
        return raw_matrix(edge, i, j)
    if edge == "17":
        return a17_entry(i, j)
    if edge == "26":
        return a26_entry(i, j)
    if edge in ("36", "46"):
        return mul(var(f"v{edge}_{i}"), U[j])
    if edge in ("37", "47"):
        source = "36" if edge == "37" else "46"
        return scale(mul(var(f"v{source}_{i}"), z_poly(j)), -1)
    if edge == "34":
        raise RuntimeError("a34 requested before its monic substitution")
    raise RuntimeError((edge, i, j))


def matching_term(matching, word, entry_function):
    return mul(*(entry_function(edge, word[int(edge[0])], word[int(edge[1])]) for edge in matching))


def a34_entry(i, j):
    # Pivot word 000ij000 has coefficient a01_00*a25_00*a67_00=1.
    word = (0, 0, 0, i, j, 0, 0, 0)
    other = add(*(matching_term(matching, word, entry_without_a34) for matching in MATCHINGS if matching != M34))
    target = ONE if len(set(word)) == 1 else ZERO
    return add(target, scale(other, -1))


def final_entry(edge, i, j):
    return a34_entry(i, j) if edge == "34" else entry_without_a34(edge, i, j)


PIVOT_WORDS = frozenset((0, 0, 0, i, j, 0, 0, 0) for i in range(3) for j in range(3))


def amplitude_equation(word):
    value = add(*(matching_term(matching, word, final_entry) for matching in MATCHINGS))
    if len(set(word)) == 1:
        value = add(value, scale(ONE, -1))
    return value


def determinant(edge, entry_function):
    positive = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    negative = [(2, 1, 0), (1, 0, 2), (0, 2, 1)]
    return add(
        *(mul(*(entry_function(edge, i, permutation[i]) for i in range(3))) for permutation in positive),
        *(scale(mul(*(entry_function(edge, i, permutation[i]) for i in range(3))), -1) for permutation in negative),
    )


def all_equations():
    equations = []
    for word in itertools.product(range(3), repeat=8):
        equation = amplitude_equation(word)
        if word in PIVOT_WORDS:
            require(equation == ZERO, ("pivot did not replay", word, len(equation)))
        else:
            equations.append(equation)
    saturation = mul(
        determinant("04", final_entry), determinant("17", final_entry), determinant("35", final_entry), determinant("26", final_entry),
        var("v36_0"), var("v46_0"), var("a04_00"), var("sat"),
    )
    # On the selected diagnostic branch a04_00 is nonzero.  Divide every
    # literal common a04_00 factor before appending its localization.
    divided = []
    for equation in equations:
        common_power = min(monomial.count("a04_00") for monomial in equation)
        if common_power:
            equation = {
                tuple(name for name in monomial if name != "a04_00") + ("a04_00",) * (monomial.count("a04_00") - common_power): coefficient
                for monomial, coefficient in equation.items()
            }
            equation = {tuple(sorted(monomial)): coefficient for monomial, coefficient in equation.items()}
        divided.append(equation)
    equations = divided
    equations.append(add(saturation, scale(ONE, -1)))
    require(len(equations) == 6553 and all(equations))
    return equations


VARIABLES = tuple(
    [f"a01_{i}{j}" for i in range(3) for j in range(3) if f"a01_{i}{j}" not in NORMALIZED]
    + [f"a04_{i}{j}" for i in range(3) for j in range(3) if f"a04_{i}{j}" not in NORMALIZED]
    + [f"a17_{i}{j}" for i in range(3) for j in range(3) if (i, j) not in ((0, 0), (1, 0))]
    + [f"a25_{i}{j}" for i in range(3) for j in range(3) if f"a25_{i}{j}" not in NORMALIZED]
    + [f"a26_{i}{j}" for i in range(3) for j in range(3) if j != 1 and f"a26_{i}{j}" not in NORMALIZED]
    + [f"a35_{i}{j}" for i in range(3) for j in range(3) if f"a35_{i}{j}" not in NORMALIZED]
    + [f"a67_{i}{j}" for i in range(3) for j in range(3) if f"a67_{i}{j}" not in NORMALIZED]
    + ["u1", "u2", "v36_0", "v36_1", "v36_2", "v46_0", "v46_1", "v46_2", "sat"]
)
require(len(VARIABLES) == 58 and len(set(VARIABLES)) == 58)


def coefficient_text(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def polynomial_text(poly):
    terms = []
    for monomial, coefficient in sorted(poly.items(), key=lambda item: (len(item[0]), item[0])):
        factor = "*".join(monomial) if monomial else "1"
        terms.append(f"({coefficient_text(coefficient)})*({factor})")
    return "+".join(terms) if terms else "0"


def build_program(equations):
    return "\n".join([
        "// HELD DIAGNOSTIC ONLY: rep1114 rank1 z1/full-torus canonical chart; no ideal run authorized.",
        "option(noredefine);", f"ring r=0,({','.join(VARIABLES)}),dp;",
        "ideal I=" + ",\n".join(polynomial_text(equation) for equation in equations) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));', 'print("INPUT_GENERATORS="+string(size(I)));', "quit;", "",
    ])


def monic_scan(equations):
    hits = []
    variable_set = set(VARIABLES)
    for equation_index, equation in enumerate(equations):
        for monomial, coefficient in equation.items():
            if len(monomial) != 1 or monomial[0] not in variable_set or not coefficient:
                continue
            name = monomial[0]
            if all(name not in other for other in equation if other != monomial):
                hits.append({"equation": equation_index, "variable": name, "coefficient": coefficient_text(coefficient), "terms": len(equation)})
    return hits


def common_factor_scan(equations):
    factored = []
    for equation_index, equation in enumerate(equations[:-1]):
        common = Counter(next(iter(equation)))
        for monomial in equation:
            common &= Counter(monomial)
        if common:
            factored.append({"equation": equation_index, "factor": dict(common)})
    return factored


def modular_row_rank(rows, columns, prime=1000003):
    basis = {}
    for dense in rows:
        row = [value % prime for value in dense]
        while True:
            pivot = next((index for index, value in enumerate(row) if value), None)
            if pivot is None:
                break
            if pivot not in basis:
                inverse = pow(row[pivot], prime - 2, prime)
                basis[pivot] = [(value * inverse) % prime for value in row]
                break
            factor = row[pivot]
            old = basis[pivot]
            row = [(left - factor * right) % prime for left, right in zip(row, old)]
        if len(basis) == columns:
            break
    return len(basis)


def rank_diagnostics(equations):
    index = {name: position for position, name in enumerate(VARIABLES)}
    exponent_rows = []
    for equation in equations:
        monomials = list(equation)
        reference = Counter(monomials[0])
        for monomial in monomials[1:]:
            difference = Counter(monomial)
            difference.subtract(reference)
            exponent_rows.append([difference.get(name, 0) for name in VARIABLES])
    grading_rank = modular_row_rank(exponent_rows, len(VARIABLES))

    prime = 1000003
    jacobian_trials = []
    for offset in (2, 101):
        values = {name: position + offset for position, name in enumerate(VARIABLES)}
        jacobian_rows = []
        for equation in equations:
            row = [0] * len(VARIABLES)
            for monomial, coefficient in equation.items():
                coefficient_mod = coefficient.numerator * pow(coefficient.denominator, prime - 2, prime) % prime
                powers = Counter(monomial)
                value = coefficient_mod
                for name, exponent in powers.items():
                    value = value * pow(values[name], exponent, prime) % prime
                for name, exponent in powers.items():
                    contribution = value * exponent * pow(values[name], prime - 2, prime) % prime
                    row[index[name]] = (row[index[name]] + contribution) % prime
            jacobian_rows.append(row)
        jacobian_trials.append({"offset": offset, "rank": modular_row_rank(jacobian_rows, len(VARIABLES))})
    jacobian_rank = max(trial["rank"] for trial in jacobian_trials)
    require(grading_rank == len(VARIABLES) and jacobian_rank >= 57, ("rank diagnostic", grading_rank, jacobian_trials, len(VARIABLES)))
    occurrences = Counter(name for equation in equations for monomial in equation for name in set(monomial))
    require(set(occurrences) == set(VARIABLES))
    return {
        "variables": len(VARIABLES), "all_variables_active": True,
        "exponent_difference_rank_mod_1000003": grading_rank,
        "residual_grading_nullity": len(VARIABLES) - grading_rank,
        "jacobian_modular_trials": jacobian_trials,
        "jacobian_rank_lower_bound_over_Q": jacobian_rank,
        "rank_scope": "nonzero modular minors prove corresponding integer exponent/Jacobian minors are nonzero over Q; the Jacobian value is only a lower bound on generic rank and is not ideal consistency or unit-ideal evidence",
    }


def determinant_fraction(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    determinant_value = Fraction(1)
    for column in range(len(matrix)):
        pivot = next((row for row in range(column, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant_value *= -1
        divisor = matrix[column][column]
        determinant_value *= divisor
        for j in range(column, len(matrix)):
            matrix[column][j] /= divisor
        for row in range(column + 1, len(matrix)):
            factor = matrix[row][column]
            for j in range(column, len(matrix)):
                matrix[row][j] -= factor * matrix[column][j]
    return determinant_value


def torus_certificate():
    basis_data = json.loads(PINS["parent_torus_basis"][0].read_text())
    basis = basis_data["basis"]

    def weight(variable_name):
        return [vector.get(variable_name, 0) for vector in basis]

    z1_weight = []
    rank_preserving = True
    for vector in basis:
        get = lambda edge, i, j: vector.get(f"a{edge}_{i}{j}", 0)
        for edge in parent.MATRIX_EDGES:
            for i in range(3):
                for j in range(3):
                    rank_preserving &= get(edge, i, j) - get(edge, i, 0) - get(edge, 0, j) + get(edge, 0, 0) == 0
        u_weights = [get("36", 0, j) - get("36", 0, 0) for j in range(3)]
        z_weights = {get("17", 1, k) + u_weights[k] for k in range(3)}
        require(len(z_weights) == 1)
        z1_weight.append(z_weights.pop())
    require(rank_preserving)
    block_pivots = ["a01_00", "a25_00", "a67_00", "z1"]
    block_rows = [weight(name) for name in block_pivots[:3]] + [z1_weight]
    block_character_matrix = [[-1, 0, 1, 0], [0, 0, -1, 0], [0, 0, 0, 1], [0, -1, 1, 0]]
    block_determinant = determinant_fraction(block_character_matrix)
    require(abs(block_determinant) == 1)
    extra = ["a35_00", "a35_10", "a35_20", "a04_01", "a04_02", "a26_12"]
    determinant_value = determinant_fraction(block_rows + [weight(name) for name in extra])
    require(abs(determinant_value) == 1)
    return {
        "parent_torus_dimension": 10,
        "rank_preserving": rank_preserving,
        "exact_block_torus_pivots": block_pivots,
        "block_character_matrix": block_character_matrix,
        "block_character_determinant": str(block_determinant),
        "held_full_torus_extra_pivots": extra,
        "ten_by_ten_weight_determinant": str(determinant_value),
        "meaning": "the ten chosen nonzero coordinates are a unimodular character basis, so their normalization is reversible over Q without root extraction",
    }


def make_result():
    parent_result = json.loads(PINS["parent_result"][0].read_text())
    require(parent_result["transport"]["records"] == [1114, 1978, 2014, 2036])
    require(parent_result["held_smallest_chart"]["source_sha256"] == PINS["parent_source"][1])
    equations = all_equations()
    program = build_program(equations)
    source_path = HERE / "rep1114_rank1_z1_fulltorus_Q.sing"
    temporary = source_path.with_suffix(".sing.tmp")
    temporary.write_text(program)
    os.replace(temporary, source_path)
    monic = monic_scan(equations)
    factors = common_factor_scan(equations)
    torus = torus_certificate()
    ranks = rank_diagnostics(equations)
    held = {
        "schema": "n8-x5-rep1114-rank1-z1-fulltorus-q-held-v1",
        "status": "HELD_DIAGNOSTIC_ZERO_RUN",
        "scope": "one canonical subchart of record1114; other three records only by the sealed four-record transport orbit",
        "dependencies": {"independent_referee_manifest": None, "resource_clearance": None, "explicit_launch_clearance": None},
        "source": {"path": source_path.name, "sha256": sha(source_path), "variables": len(VARIABLES), "generators": len(equations), "ring": "Q"},
        "acceptance": "future exact-Q UNIT_IDEAL plus reduce(1,G)=0 and literal source replay; every other outcome is diagnostic zero coverage",
        "refusal": "no Singular, modular pilot, sibling chart, transport promotion, or relaunch without all dependencies and a fresh explicit clearance",
    }
    held_path = HERE / "held_smallest_diagnostic_plan.json"
    held_path.write_text(json.dumps(held, indent=2, sort_keys=True) + "\n")
    return {
        "schema": "n8-x5-exception1114-rank1-refinement-design-v1",
        "status": "PASS_EXACT_REFINEMENT_ZERO_RUN",
        "pins": {name: {"path": str(path), "sha256": expected} for name, (path, expected) in PINS.items()},
        "transport_scope": {"representative": 1114, "records": [1114, 1978, 2014, 2036], "transport_orbits": 1, "no_cross_orbit_claim": True},
        "parent_chart": {"variables": 81, "generators": 6566, "source_sha256": PINS["parent_source"][1]},
        "reversible_reductions": {
            "rank_gauge": "from parent v36_0=1,u0!=0 use u'=u/u0 and v'=u0*v; set u'_0=1 and require v36_0*v46_0!=0",
            "scalar_guard": "u^T(A17+A17^T)u=0 is 2*u^T*A17*u=0; after u0=1 it eliminates a17_00 monically",
            "z_cover": "z=A17*u is nonzero because det(A17)!=0; choose z_r!=0 for r=0,1,2 and use the fourth block-torus character to set z_r=1",
            "A26_cramer": "A26*z=u then eliminates column r of A26 without division after z_r=1",
            "A34_monic": "choose nonzero entries of A01,A25,A67, normalize them to one with the other three block-torus characters, and use words 000ij000 to eliminate all nine A34 entries",
            "block_torus_character_determinant": "1",
        },
        "exact_block_torus_cover": {
            "raw_profiles": 2187,
            "residual_color_S2_orbits": 1094,
            "derivation": "3 z choices times 9^3 nonzero-entry choices; the residual swap 1<->2 has exactly one fixed profile",
            "z0_orbits": 365, "z12_orbits": 729,
            "z0_counts": {"variables": 65, "generators": 6554},
            "z12_counts": {"variables": 64, "generators": 6553},
            "cover_scope": "exactly the sealed canonical rank(H)=1 chart, not the other nine H-rank1 S3 charts and not rank2/rank3",
        },
        "torus": torus,
        "held_full_torus_subchart": {
            "z": "z1=1", "normalized_source_coordinates": sorted(NORMALIZED),
            "nonzero_coordinate_chart": "the ten coordinates in the torus certificate are nonzero and normalized to one; this is a diagnostic subchart, not a determinant-term cover",
            "additional_factor_localization": "a04_00!=0; four exposed common factors are divided and a04_00 is included in the existing saturation",
            "variables": 58, "generators": 6553,
            "equation_sha256": canonical_hash([{','.join(monomial): str(coefficient) for monomial, coefficient in sorted(equation.items())} for equation in equations]),
            "source_path": source_path.name, "source_sha256": sha(source_path),
            "monic_scan_after_reduction": {"hits": len(monic), "records": monic},
            "proper_common_factor_scan": {"hits": len(factors), "records": factors},
            "plan_path": held_path.name, "plan_sha256": sha(held_path),
        },
        "irreducibility_diagnosis": {
            "statement": "after the reversible gauge/Cramer/A34/full-torus substitutions, no remaining nonsaturation generator has a common monomial factor; any surviving monic hit is listed explicitly rather than silently promoted",
            "rank_diagnostics": ranks,
            "remaining_rank_splits": "A04,A17,A35,A26 are rank3 by saturation; v36_0*v46_0 and the chosen source coordinates are nonzero; optional ranks of A01,A25,A67 are not forced and would only create a new determinantal cover",
            "full_Groebner_or_unit_claim": False,
        },
        "scope": {"singular_runs": 0, "sat_runs": 0, "large_cnf_reads": 0, "records_closed": 0, "full_conjecture_claim": False},
    }


if __name__ == "__main__":
    result = make_result()
    (HERE / "results_rank1_refinement.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"], "cover": result["exact_block_torus_cover"],
        "held": {key: result["held_full_torus_subchart"][key] for key in ("variables", "generators", "source_sha256")},
        "monic_hits": result["held_full_torus_subchart"]["monic_scan_after_reduction"]["hits"],
        "factor_hits": result["held_full_torus_subchart"]["proper_common_factor_scan"]["hits"],
        "scope": result["scope"],
    }, indent=2, sort_keys=True))
