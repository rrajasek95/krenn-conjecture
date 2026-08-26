#!/usr/bin/env python3
"""Independent audit of the fixed twisted-4+4 integer certificate.

This checker deliberately does not import the producer.  It enumerates perfect
matchings as the 4-edge subsets of K8 having vertex degree one, and represents
polynomials by exponent vectors.  The only producer artifacts read are the
human-readable certificate JSON and its stated word labels.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path


N = 8
COLORS = range(3)
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CERTIFICATE = (
    REPO
    / "computations"
    / "unaudited-codex-twisted44-audit-2026-08-20"
    / "certificate.json"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "50eb546c0e6d0382e3376204aa82788725994605a9c3152c0a11d57d7b46eba5"
)
EXPECTED_SOURCE_REBUILD_SHA256 = (
    "6916c2fa2fbefe6878c3158d67933d3290f16ff5ca041bc80f126cf3a2314a75"
)
EXPECTED_RAW_EQUATIONS_SHA256 = (
    "44d0b3e832f0208756eb103c12ad9e0c1fc70f8f87e01037612a2c9192f2fb74"
)
EXPECTED_NORMALIZED_EQUATIONS_SHA256 = (
    "f935a5361c80a26315614ac9ed29baa1504e7eb99da953f693dda5989c62bb22"
)


class AuditFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditFailure(message)


# Fixed endpoint-ordered binary representative.  Every unlisted binary cell is
# zero; every cell containing color 2 is an independent indeterminate.
FIXED = {
    (0, 1, 0, 0): 1,
    (2, 3, 0, 0): 1,
    (4, 5, 0, 0): 1,
    (6, 7, 0, 0): 1,
    (0, 3, 1, 1): 1,
    (1, 2, 1, 1): 1,
    (4, 7, 1, 1): 1,
    (5, 6, 1, 1): 1,
    (0, 4, 0, 1): 1,
    (0, 5, 1, 0): 1,
    (1, 7, 0, 1): -1,
    (3, 4, 1, 0): -1,
}

EDGES = tuple(combinations(range(N), 2))


def enumerate_matchings_by_edge_subsets():
    """Use C(28,4), not first-vertex recursion or a subset DP."""
    out = []
    for candidate in combinations(EDGES, N // 2):
        degree = [0] * N
        for u, v in candidate:
            degree[u] += 1
            degree[v] += 1
        if degree == [1] * N:
            out.append(candidate)
    return tuple(out)


MATCHINGS = enumerate_matchings_by_edge_subsets()

VARIABLE_NAMES = tuple(
    f"x{u}{v}{a}{b}"
    for u, v in EDGES
    for a, b in product(COLORS, repeat=2)
    if a == 2 or b == 2
)
VAR_ID = {name: index for index, name in enumerate(VARIABLE_NAMES)}

# A monomial is ((variable_index, exponent), ...), sorted by variable index.
UNIT_MONOMIAL = ()


def exponent_vector(variable_ids):
    counts = Counter(variable_ids)
    return tuple(sorted(counts.items()))


def multiply_monomials(left, right):
    counts = Counter(dict(left))
    counts.update(dict(right))
    return tuple(sorted((index, exponent) for index, exponent in counts.items() if exponent))


def add_term(poly, monomial, coefficient):
    if coefficient == 0:
        return
    new_value = poly.get(monomial, 0) + coefficient
    if new_value:
        poly[monomial] = new_value
    else:
        poly.pop(monomial, None)


def multiply_polynomials(left, right):
    out = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            add_term(out, multiply_monomials(lm, rm), lc * rc)
    return out


def canonical_sign_normalize(poly):
    """Choose the generator sign by its smallest exponent-vector monomial."""
    require(poly, "cannot normalize the zero polynomial")
    first_monomial = min(poly)
    sign = 1 if poly[first_monomial] > 0 else -1
    return {monomial: sign * coefficient for monomial, coefficient in poly.items()}, sign


def cell_factor(u, v, a, b, fixed=FIXED, transpose=False):
    if transpose:
        a, b = b, a
    if a == 2 or b == 2:
        name = f"x{u}{v}{a}{b}"
        return 1, VAR_ID[name]
    return fixed.get((u, v, a, b), 0), None


def raw_equation(word, fixed=FIXED, transpose=False, target_sign=-1):
    """Return H_word - delta_word by default."""
    letters = tuple(int(letter) for letter in word)
    require(len(letters) == N and set(letters) <= set(COLORS), f"bad word {word}")
    poly = {}
    for matching in MATCHINGS:
        coefficient = 1
        variables = []
        for u, v in matching:
            scalar, variable = cell_factor(
                u, v, letters[u], letters[v], fixed=fixed, transpose=transpose
            )
            coefficient *= scalar
            if coefficient == 0:
                break
            if variable is not None:
                variables.append(variable)
        if coefficient:
            add_term(poly, exponent_vector(variables), coefficient)
    if len(set(letters)) == 1:
        add_term(poly, UNIT_MONOMIAL, target_sign)
    return poly


def binary_amplitude(word, fixed=FIXED, transpose=False):
    letters = tuple(int(letter) for letter in word)
    total = 0
    for matching in MATCHINGS:
        term = 1
        for u, v in matching:
            a, b = letters[u], letters[v]
            if transpose:
                a, b = b, a
            term *= fixed.get((u, v, a, b), 0)
            if not term:
                break
        total += term
    return total


def parse_multiplier(entries):
    out = {}
    for entry in entries:
        ids = []
        for name in entry["monomial"]:
            require(name in VAR_ID, f"unknown certificate variable {name}")
            ids.append(VAR_ID[name])
        add_term(out, exponent_vector(ids), int(entry["coefficient"]))
    return out


def monomial_names(monomial):
    return tuple((VARIABLE_NAMES[index], exponent) for index, exponent in monomial)


def serialize_poly(poly):
    return [
        {
            "coefficient": coefficient,
            "monomial": monomial_names(monomial),
        }
        for monomial, coefficient in sorted(poly.items())
    ]


def reduced_by_zero_variables(poly, zero_names):
    zero_ids = {VAR_ID[name] for name in zero_names}
    return {
        monomial: coefficient
        for monomial, coefficient in poly.items()
        if all(index not in zero_ids for index, _ in monomial)
    }


def single_unit_variable(poly):
    if len(poly) != 1:
        return None
    monomial, coefficient = next(iter(poly.items()))
    if len(monomial) != 1 or monomial[0][1] != 1 or abs(coefficient) != 1:
        return None
    return VARIABLE_NAMES[monomial[0][0]], coefficient


def word_profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def canonical_digest(value):
    blob = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(blob).hexdigest()


def evaluate_assignment(word, assignment, fixed=FIXED):
    letters = tuple(int(letter) for letter in word)
    total = Fraction(0)
    for matching in MATCHINGS:
        term = Fraction(1)
        for u, v in matching:
            a, b = letters[u], letters[v]
            if a == 2 or b == 2:
                term *= assignment[f"x{u}{v}{a}{b}"]
            else:
                term *= fixed.get((u, v, a, b), 0)
            if not term:
                break
        total += term
    return total


def gauge_numeric_check():
    # Deterministic nonzero rational point and target-preserving diagonal gauge.
    assignment = {
        name: Fraction((index % 7) + 1, (index % 5) + 1)
        for index, name in enumerate(VARIABLE_NAMES)
    }
    lambdas = {}
    for color in COLORS:
        running = Fraction(1)
        for vertex in range(N - 1):
            value = Fraction(vertex + color + 2, vertex + color + 3)
            lambdas[(vertex, color)] = value
            running *= value
        lambdas[(N - 1, color)] = 1 / running

    transformed_fixed = {}
    for (u, v, a, b), value in FIXED.items():
        transformed_fixed[(u, v, a, b)] = (
            value * lambdas[(u, a)] * lambdas[(v, b)]
        )
    transformed_assignment = {}
    for u, v in EDGES:
        for a, b in product(COLORS, repeat=2):
            if a == 2 or b == 2:
                name = f"x{u}{v}{a}{b}"
                transformed_assignment[name] = (
                    assignment[name] * lambdas[(u, a)] * lambdas[(v, b)]
                )

    # Check all 3^8 amplitudes, not a sample.
    for letters in product(COLORS, repeat=N):
        word = "".join(map(str, letters))
        scale = Fraction(1)
        for vertex, color in enumerate(letters):
            scale *= lambdas[(vertex, color)]
        lhs = evaluate_assignment(word, transformed_assignment, transformed_fixed)
        rhs = scale * evaluate_assignment(word, assignment, FIXED)
        require(lhs == rhs, f"gauge factorization failed at {word}")
    products = {
        str(color): str(
            _fraction_product(lambdas[(vertex, color)] for vertex in range(N))
        )
        for color in COLORS
    }
    return products


def _fraction_product(values):
    out = Fraction(1)
    for value in values:
        out *= value
    return out


def run_audit():
    declared_controls = [
        "matching_and_ring_counts",
        "fixed_binary_exactness",
        "fixed_sign_mutation",
        "endpoint_transpose_mutation",
        "certificate_digest_and_shape",
        "integer_certificate_identity",
        "raw_equation_metadata_diagnostic",
        "certificate_equation_sign_mutation",
        "certificate_multiplier_delete_mutation",
        "pure_target_sign_mutation",
        "triangular_rederivation",
        "all_field_reductions",
        "gauge_factorization_all_words",
        "target_symmetry_scope",
    ]
    executed_controls = []
    details = {}

    def done(name, value=True):
        require(name in declared_controls, f"undeclared control {name}")
        require(name not in executed_controls, f"duplicate control {name}")
        executed_controls.append(name)
        details[name] = value

    require(len(MATCHINGS) == 105, f"matching count {len(MATCHINGS)} != 105")
    require(len(set(MATCHINGS)) == 105, "duplicate perfect matching")
    require(len(VARIABLE_NAMES) == 140, "wrong variable count")
    require(len(set(VARIABLE_NAMES)) == 140, "duplicate variable name")
    done(
        "matching_and_ring_counts",
        {"perfect_matchings": len(MATCHINGS), "variables": len(VARIABLE_NAMES)},
    )

    binary_failures = []
    for letters in product(range(2), repeat=N):
        word = "".join(map(str, letters))
        expected = 1 if len(set(letters)) == 1 else 0
        actual = binary_amplitude(word)
        if actual != expected:
            binary_failures.append({"word": word, "expected": expected, "actual": actual})
    require(not binary_failures, f"fixed binary representative is not exact: {binary_failures[:3]}")
    done("fixed_binary_exactness", {"words_checked": 2**N, "failures": 0})

    sign_mutant = dict(FIXED)
    sign_mutant[(3, 4, 1, 0)] = 1
    sign_fires = []
    transpose_fires = []
    for letters in product(range(2), repeat=N):
        word = "".join(map(str, letters))
        expected = 1 if len(set(letters)) == 1 else 0
        mutated = binary_amplitude(word, fixed=sign_mutant)
        transposed = binary_amplitude(word, transpose=True)
        if mutated != expected:
            sign_fires.append({"word": word, "expected": expected, "actual": mutated})
        if transposed != expected:
            transpose_fires.append(
                {"word": word, "expected": expected, "actual": transposed}
            )
    require(sign_fires, "fixed-sign mutation did not fire")
    require(transpose_fires, "endpoint-transpose mutation did not fire")
    done(
        "fixed_sign_mutation",
        {"firing_words": len(sign_fires), "first": sign_fires[0]},
    )
    done(
        "endpoint_transpose_mutation",
        {"firing_words": len(transpose_fires), "first": transpose_fires[0]},
    )

    certificate_bytes = CERTIFICATE.read_bytes()
    certificate_sha = sha256(certificate_bytes).hexdigest()
    require(
        certificate_sha == EXPECTED_CERTIFICATE_SHA256,
        f"certificate digest drift: {certificate_sha}",
    )
    certificate = json.loads(certificate_bytes)
    generator_words = certificate["generator_words"]
    multiplier_records = certificate["multipliers"]
    require(set(generator_words) == set(multiplier_records), "generator/multiplier key mismatch")
    require(len(generator_words) == 21, "certificate does not use 21 equations")
    require(certificate.get("n_generators_used") == 21, "certificate generator count drift")
    expected_ring = "Z[" + ",".join(VARIABLE_NAMES) + "]"
    require(certificate.get("ring") == expected_ring, "certificate ring/order mismatch")
    multiplier_term_count = sum(len(entries) for entries in multiplier_records.values())
    require(multiplier_term_count == 781, "certificate does not have 781 multiplier terms")
    done(
        "certificate_digest_and_shape",
        {
            "sha256": certificate_sha,
            "generators": len(generator_words),
            "multiplier_terms": multiplier_term_count,
        },
    )

    raw_equations = {
        gid: raw_equation(word)
        for gid, word in generator_words.items()
    }
    normalized_pairs = {
        gid: canonical_sign_normalize(raw_equations[gid])
        for gid in generator_words
    }
    equations = {gid: pair[0] for gid, pair in normalized_pairs.items()}
    generator_signs = {gid: pair[1] for gid, pair in normalized_pairs.items()}
    multipliers = {
        gid: parse_multiplier(multiplier_records[gid])
        for gid in generator_words
    }
    identity = {}
    for gid in generator_words:
        for monomial, coefficient in multiply_polynomials(
            multipliers[gid], equations[gid]
        ).items():
            add_term(identity, monomial, coefficient)
    require(identity == {UNIT_MONOMIAL: 1}, "stored integer certificate is not 1")
    equation_digest = canonical_digest(
        {gid: serialize_poly(equations[gid]) for gid in sorted(equations)}
    )
    raw_equation_digest = canonical_digest(
        {gid: serialize_poly(raw_equations[gid]) for gid in sorted(raw_equations)}
    )
    require(
        equation_digest == EXPECTED_NORMALIZED_EQUATIONS_SHA256,
        f"normalized equation digest drift: {equation_digest}",
    )
    require(
        raw_equation_digest == EXPECTED_RAW_EQUATIONS_SHA256,
        f"raw equation digest drift: {raw_equation_digest}",
    )
    done(
        "integer_certificate_identity",
        {
            "identity": "1",
            "equation_digest": equation_digest,
            "raw_equation_digest": raw_equation_digest,
            "generator_signs": generator_signs,
            "normalization": "smallest exponent-vector monomial has positive coefficient",
            "nonzero_residual_terms": 1,
        },
    )

    raw_claimed_identity = {}
    for gid in generator_words:
        for monomial, coefficient in multiply_polynomials(
            multipliers[gid], raw_equations[gid]
        ).items():
            add_term(raw_claimed_identity, monomial, coefficient)
    require(
        raw_claimed_identity != {UNIT_MONOMIAL: 1},
        "unexpectedly, omitted generator signs were unnecessary",
    )
    require(
        len(raw_claimed_identity) == 346
        and raw_claimed_identity.get(UNIT_MONOMIAL) == -1,
        "raw-equation diagnostic drifted",
    )
    done(
        "raw_equation_metadata_diagnostic",
        {
            "verdict": "stored multipliers do not apply literally to H_word-delta_word",
            "nonzero_terms": len(raw_claimed_identity),
            "constant": raw_claimed_identity.get(UNIT_MONOMIAL),
            "residual_sha256": canonical_digest(serialize_poly(raw_claimed_identity)),
            "repair": "apply the recorded per-generator canonical sign before each multiplier",
        },
    )

    selected_gid = "3773"
    require(selected_gid in equations, "pure-2 generator absent")
    sign_mutated_identity = dict(identity)
    selected_product = multiply_polynomials(
        multipliers[selected_gid], equations[selected_gid]
    )
    for monomial, coefficient in selected_product.items():
        add_term(sign_mutated_identity, monomial, -2 * coefficient)
    require(
        sign_mutated_identity != {UNIT_MONOMIAL: 1},
        "certificate equation-sign mutation did not fire",
    )
    done(
        "certificate_equation_sign_mutation",
        {"generator": selected_gid, "residual_terms": len(sign_mutated_identity)},
    )

    deleted_multiplier_identity = dict(identity)
    for monomial, coefficient in selected_product.items():
        add_term(deleted_multiplier_identity, monomial, -coefficient)
    require(
        deleted_multiplier_identity != {UNIT_MONOMIAL: 1},
        "certificate multiplier-deletion mutation did not fire",
    )
    done(
        "certificate_multiplier_delete_mutation",
        {"generator": selected_gid, "residual_terms": len(deleted_multiplier_identity)},
    )

    wrong_target_equations = dict(equations)
    wrong_target_raw = raw_equation(generator_words[selected_gid], target_sign=1)
    wrong_target_equations[selected_gid] = canonical_sign_normalize(wrong_target_raw)[0]
    wrong_target_identity = {}
    for gid in generator_words:
        for monomial, coefficient in multiply_polynomials(
            multipliers[gid], wrong_target_equations[gid]
        ).items():
            add_term(wrong_target_identity, monomial, coefficient)
    require(
        wrong_target_identity != {UNIT_MONOMIAL: 1},
        "pure target-sign mutation did not fire over Z",
    )
    pure_raw_equation = raw_equations[selected_gid]
    pure_equation = equations[selected_gid]
    require(
        pure_raw_equation.get(UNIT_MONOMIAL) == -1,
        "raw pure equation target is not H-1",
    )
    require(
        pure_equation.get(UNIT_MONOMIAL) == 1,
        "normalized pure generator target is not 1-H",
    )
    require(len(pure_equation) == 106, "pure equation should be -1 plus 105 matchings")
    require(
        all(coefficient == -1 for monomial, coefficient in pure_equation.items() if monomial),
        "normalized pure matching coefficient is not -1",
    )
    done(
        "pure_target_sign_mutation",
        {
            "correct_convention": "H_word - delta_word",
            "raw_pure_constant": -1,
            "normalized_pure_constant": 1,
            "pure_matching_monomials": 105,
            "wrong_sign_residual_terms": len(wrong_target_identity),
        },
    )

    # Stage 1: discover all literal unit rows among the cited equations.
    literal_rows = []
    initial_zero_names = set()
    for gid, poly in equations.items():
        unit = single_unit_variable(poly)
        if unit is not None:
            name, coefficient = unit
            literal_rows.append(
                {
                    "generator": gid,
                    "word": generator_words[gid],
                    "variable": name,
                    "coefficient": coefficient,
                }
            )
            initial_zero_names.add(name)
    require(len(literal_rows) == 12, f"found {len(literal_rows)} literal rows, not 12")

    # Stage 2: discover a binomial with one known-zero term and one new unit term.
    binomial_candidates = []
    for gid, poly in equations.items():
        if len(poly) != 2:
            continue
        terms = []
        valid = True
        for monomial, coefficient in poly.items():
            unit = single_unit_variable({monomial: coefficient})
            if unit is None:
                valid = False
                break
            terms.append(unit)
        if not valid:
            continue
        known = [term for term in terms if term[0] in initial_zero_names]
        new = [term for term in terms if term[0] not in initial_zero_names]
        if len(known) == 1 and len(new) == 1:
            binomial_candidates.append((gid, known[0], new[0]))
    require(len(binomial_candidates) == 1, f"binomial candidates: {binomial_candidates}")
    binomial_gid, binomial_known, binomial_new = binomial_candidates[0]
    require(generator_words[binomial_gid] == "21110000", "unexpected binomial word")
    require(binomial_known[0] == "x0321", "unexpected known binomial variable")
    require(binomial_new[0] == "x0520", "unexpected derived binomial variable")
    stage_zero_names = set(initial_zero_names)
    stage_zero_names.add(binomial_new[0])

    # Stage 3: reduce cited rows by the 13 known zeros and discover the seven
    # vertex-0 pure-2 edge variables as unit pivots.
    expected_pure_edges = {f"x0{j}22" for j in range(1, N)}
    seven_rows = []
    discovered_pure_edges = set()
    for gid, poly in equations.items():
        reduced = reduced_by_zero_variables(poly, stage_zero_names)
        unit = single_unit_variable(reduced)
        if unit is None or unit[0] not in expected_pure_edges:
            continue
        name, coefficient = unit
        seven_rows.append(
            {
                "generator": gid,
                "word": generator_words[gid],
                "profile": word_profile(generator_words[gid]),
                "variable": name,
                "coefficient": coefficient,
                "terms_before_reduction": len(poly),
            }
        )
        discovered_pure_edges.add(name)
    require(discovered_pure_edges == expected_pure_edges, "seven pure-edge pivots incomplete")
    require(len(seven_rows) == 7, f"found {len(seven_rows)} pure-edge rows, not 7")

    profile_332_rows = [row for row in seven_rows if tuple(row["profile"]) == (3, 3, 2)]
    require(
        {(row["word"], row["variable"], row["coefficient"]) for row in profile_332_rows}
        == {("20002111", "x0422", -1), ("21110200", "x0522", 1)},
        f"unexpected (3,3,2) rows: {profile_332_rows}",
    )

    final_zero_names = stage_zero_names | discovered_pure_edges
    reduced_pure = reduced_by_zero_variables(pure_equation, final_zero_names)
    require(
        reduced_pure == {UNIT_MONOMIAL: 1},
        f"normalized pure equation did not reduce to 1: {serialize_poly(reduced_pure)}",
    )
    require(len(final_zero_names) == 20, "triangular proof should establish 20 zeros")
    done(
        "triangular_rederivation",
        {
            "literal_rows": sorted(literal_rows, key=lambda row: row["word"]),
            "binomial_row": {
                "generator": binomial_gid,
                "word": generator_words[binomial_gid],
                "known_term": binomial_known,
                "new_term": binomial_new,
            },
            "pure_edge_rows": sorted(seven_rows, key=lambda row: row["variable"]),
            "profile_3_3_2_rows": sorted(profile_332_rows, key=lambda row: row["word"]),
            "pure_remainder": 1,
        },
    )

    modular = {}
    for prime in (2, 3, 5, 7):
        reduced_identity = {
            monomial: coefficient % prime
            for monomial, coefficient in identity.items()
            if coefficient % prime
        }
        require(
            reduced_identity == {UNIT_MONOMIAL: 1},
            f"certificate does not reduce to 1 mod {prime}",
        )
        modular[str(prime)] = "1"
    require(
        all(abs(row["coefficient"]) == 1 for row in literal_rows + seven_rows),
        "triangular pivot is not an integer unit",
    )
    require(abs(binomial_new[1]) == 1, "binomial pivot is not an integer unit")
    done(
        "all_field_reductions",
        {
            "sample_prime_reductions": modular,
            "proof": "integer identity 1 and division-free unit pivots",
        },
    )

    gauge_products = gauge_numeric_check()
    require(gauge_products == {"0": "1", "1": "1", "2": "1"}, "bad gauge")
    done(
        "gauge_factorization_all_words",
        {
            "words_checked": 3**N,
            "matchings_per_word": len(MATCHINGS),
            "pure_products": gauge_products,
        },
    )

    site_permutations = sum(1 for _ in permutations(range(N)))
    palette_permutations = sum(1 for _ in permutations(COLORS))
    require(site_permutations == 40320, "site permutation enumeration failed")
    require(palette_permutations == 6, "palette permutation enumeration failed")
    done(
        "target_symmetry_scope",
        {
            "diagonal_gauge": (
                "all nonzero lambda_(v,c) with product_v lambda_(v,c)=1 "
                "for each color occurring in the normalized target"
            ),
            "site_permutations": site_permutations,
            "global_palette_permutations": palette_permutations,
            "fixed_01_stabilizer_palette_permutations": 2,
            "excluded": [
                "independent sitewise palette permutations",
                "non-diagonal color mixing",
                "combinatorial-stratum members without a proved orbit map",
            ],
        },
    )

    require(
        executed_controls == declared_controls,
        f"control manifest mismatch: declared={declared_controls}, executed={executed_controls}",
    )
    source_digest = canonical_digest(
        {
            "fixed": sorted((list(key), value) for key, value in FIXED.items()),
            "variables": VARIABLE_NAMES,
            "matchings": MATCHINGS,
        }
    )
    require(
        source_digest == EXPECTED_SOURCE_REBUILD_SHA256,
        f"source rebuild digest drift: {source_digest}",
    )
    result = {
        "verdict": "PASS_FIXED_REPRESENTATIVE_AND_EXPLICIT_ORBIT_ONLY",
        "certificate_input": str(CERTIFICATE.relative_to(REPO)),
        "certificate_sha256": certificate_sha,
        "source_rebuild_sha256": source_digest,
        "equations_sha256": equation_digest,
        "controls_declared": declared_controls,
        "controls_executed": executed_controls,
        "details": details,
        "theorem_scope": {
            "proved": (
                "No fully exact ternary N=8 source extends the displayed fixed "
                "endpoint-ordered binary representative, over any field; the same "
                "holds on its target-preserving diagonal-gauge/site-permutation/global-"
                "palette-relabeling orbit."
            ),
            "not_proved": (
                "All binary sources with the twisted-4+4 combinatorial support belong "
                "to that orbit."
            ),
        },
    }
    result["result_sha256"] = canonical_digest(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        (HERE / "results.json").write_text(rendered, encoding="utf-8")
    print("PASS fixed twisted-4+4 certificate and explicit symmetry orbit")
    print(f"certificate_sha256={result['certificate_sha256']}")
    print(f"source_rebuild_sha256={result['source_rebuild_sha256']}")
    print(f"equations_sha256={result['equations_sha256']}")
    print(f"result_sha256={result['result_sha256']}")


if __name__ == "__main__":
    main()
