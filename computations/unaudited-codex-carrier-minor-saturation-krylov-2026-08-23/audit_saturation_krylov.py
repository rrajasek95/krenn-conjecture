#!/usr/bin/env python3
"""Exact bounded multiplication-by-F0 audit for the carrier-minor quotient."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
K1_SOURCE = ROOT / "unaudited-codex-carrier-minor-pure-amplitude-degree13-x5-2026-08-23" / "audit_pure_amplitude_carrier_minor_separator.py"
K2_SOURCE = ROOT / "unaudited-codex-carrier-minor-pure-square-degree17-rust-2026-08-23" / "audit_pure_square_separator_exact.py"
K1_RESULT = K1_SOURCE.parent / "results_pure_amplitude_carrier_minor_separator_exact.json"
K2_RESULT = K2_SOURCE.parent / "results_pure_square_separator_exact.json"
K0_RESULT = ROOT / "unaudited-codex-carrier-minor-degree9-x5-2026-08-23" / "results_carrier_minor_degree9_x5.json"
OUT = HERE / "results_saturation_krylov.json"
PRIMES = (32003, 32009)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


K1 = load_module("carrier_k1_exact", K1_SOURCE)
K2 = load_module("carrier_k2_exact", K2_SOURCE)
C = K1.C
D9 = K1.D9


def frozen_functionals():
    degree9 = json.loads(K0_RESULT.read_text())
    lambda0 = {
        K1.parse_monomial(entry["monomial"]): entry["coefficient"]
        for entry in degree9["integer_separator"]["entries"]
    }
    modular1 = json.loads(K1.MODULAR.read_text())
    _, lambda1, _, _ = K1.primitive_integer_lift(
        modular1["centered_integer_replay"]["entries"]
    )
    modular2 = json.loads(K2.RUST_RESULT.read_text())
    _, lambda2, _, _ = K2.integer_separator(modular2)
    return lambda0, lambda1, lambda2


def contract_by_polynomial(functional, terms):
    """Transpose of multiplication: (F0^* lambda)(q)=lambda(F0*q)."""
    out = Counter()
    for monomial, coefficient in functional.items():
        for term in terms:
            quotient = C.divides(monomial, term)
            if quotient is not None:
                out[quotient] += coefficient
    return {monomial: coefficient for monomial, coefficient in out.items()
            if coefficient}


def touching_rows(functional, generators):
    labels = set()
    for monomial in functional:
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = C.divides(monomial, term)
                if quotient is not None:
                    labels.add((word_index, quotient))
    return tuple(sorted(labels))


def row_matrix(support, labels, generators):
    column = {monomial: index for index, monomial in enumerate(support)}
    rows = []
    for label in labels:
        counts = Counter(C.row_monomials(label, generators))
        row = [0] * len(support)
        for monomial, coefficient in counts.items():
            if monomial in column:
                row[column[monomial]] = coefficient
        require(any(row), ("empty touching row", label))
        rows.append(row)
    return rows


def rank_mod_p(rows, prime):
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next((index for index in range(rank, len(matrix))
                      if matrix[index][column] % prime), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column] % prime, prime - 2, prime)
        matrix[rank] = [(value * inverse) % prime for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or matrix[index][column] % prime == 0:
                continue
            scale = matrix[index][column] % prime
            matrix[index] = [
                (left - scale * right) % prime
                for left, right in zip(matrix[index], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def rank_over_q(rows):
    basis = {}
    for dense in rows:
        row = {index: Fraction(value) for index, value in enumerate(dense)
               if value}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {index: value / scale for index, value in row.items()}
                basis[pivot] = row
                break
            scale = row[pivot]
            pivot_row = basis[pivot]
            for index, value in pivot_row.items():
                updated = row.get(index, Fraction(0)) - scale * value
                if updated:
                    row[index] = updated
                else:
                    row.pop(index, None)
    return len(basis)


def annihilates(rows, functional, support):
    coefficients = [functional.get(monomial, 0) for monomial in support]
    return all(sum(left * right for left, right in zip(row, coefficients)) == 0
               for row in rows)


def proportional(left, right):
    support = set(left) | set(right)
    pivot = next((monomial for monomial in sorted(support)
                  if right.get(monomial, 0)), None)
    require(pivot is not None, "zero comparison functional")
    numerator = left.get(pivot, 0)
    denominator = right[pivot]
    if denominator == 0 or any(
        left.get(monomial, 0) * denominator
        != right.get(monomial, 0) * numerator
        for monomial in support
    ):
        return None
    require(numerator % denominator == 0,
            ("nonintegral proportionality", numerator, denominator))
    return numerator // denominator


def entries_digest(functional):
    entries = [
        [D9.monomial_text(monomial), coefficient]
        for monomial, coefficient in sorted(functional.items())
    ]
    return sha256(json.dumps(entries, separators=(",", ":")).encode()).hexdigest()


def audit(mutate_lambda2=False):
    lambda0, lambda1, lambda2 = frozen_functionals()
    if mutate_lambda2:
        lambda2[min(lambda2)] += 1
    require((len(lambda0), len(lambda1), len(lambda2)) == (1, 44, 102),
            (len(lambda0), len(lambda1), len(lambda2)))
    pure_terms = tuple(D9.amplitude((0,) * 8))
    require(len(pure_terms) == 105, len(pure_terms))
    contraction10 = contract_by_polynomial(lambda1, pure_terms)
    transition10 = proportional(contraction10, lambda0)
    contraction = contract_by_polynomial(lambda2, pure_terms)
    transition_scalar = proportional(contraction, lambda1)

    generators = tuple(tuple(D9.amplitude(word)) for word in C.WORDS)
    contraction10_support = tuple(sorted(contraction10))
    contraction10_labels = touching_rows(contraction10, generators)
    contraction10_matrix = row_matrix(
        contraction10_support, contraction10_labels, generators
    )
    contraction10_ranks = tuple(rank_mod_p(contraction10_matrix, prime)
                                for prime in PRIMES)
    contraction10_rational_rank = rank_over_q(contraction10_matrix)
    require(contraction10_ranks[0] == contraction10_ranks[1]
            == contraction10_rational_rank, contraction10_ranks)
    require(annihilates(
        contraction10_matrix, contraction10, contraction10_support
    ), "degree9 contraction does not annihilate mixed rows")
    union0_support = tuple(sorted(set(lambda0) | set(contraction10)))
    union0_labels = touching_rows(
        {monomial: 1 for monomial in union0_support}, generators
    )
    union0_matrix = row_matrix(union0_support, union0_labels, generators)
    union0_ranks = tuple(rank_mod_p(union0_matrix, prime) for prime in PRIMES)
    union0_rational_rank = rank_over_q(union0_matrix)
    require(union0_ranks[0] == union0_ranks[1] == union0_rational_rank,
            union0_ranks)
    supports = (tuple(sorted(lambda1)), tuple(sorted(lambda2)))
    labels = (
        touching_rows(lambda1, generators),
        touching_rows(lambda2, generators),
    )
    matrices = (
        row_matrix(supports[0], labels[0], generators),
        row_matrix(supports[1], labels[1], generators),
    )
    ranks = tuple(tuple(rank_mod_p(matrix, prime) for prime in PRIMES)
                  for matrix in matrices)
    rational_ranks = tuple(rank_over_q(matrix) for matrix in matrices)
    nullities = tuple(len(support) - rational_rank
                      for support, rational_rank in zip(supports, rational_ranks))
    require(all(pair[0] == pair[1] for pair in ranks), ranks)
    require(all(rational_rank == pair[0]
                for rational_rank, pair in zip(rational_ranks, ranks)),
            (rational_ranks, ranks))
    require((rational_ranks, nullities) == ((43, 101), (1, 1)),
            (rational_ranks, nullities))

    contraction_support = tuple(sorted(contraction))
    contraction_labels = touching_rows(contraction, generators)
    contraction_matrix = row_matrix(
        contraction_support, contraction_labels, generators
    )
    contraction_ranks = tuple(rank_mod_p(contraction_matrix, prime)
                              for prime in PRIMES)
    contraction_rational_rank = rank_over_q(contraction_matrix)
    require(contraction_ranks[0] == contraction_ranks[1], contraction_ranks)
    require(contraction_rational_rank == contraction_ranks[0],
            (contraction_rational_rank, contraction_ranks))
    require(annihilates(contraction_matrix, contraction, contraction_support),
            "contracted functional does not annihilate degree-13 rows")
    require((len(contraction_support), len(contraction_labels),
             contraction_rational_rank) == (108, 85, 77),
            (len(contraction_support), len(contraction_labels),
             contraction_rational_rank))
    union_support = tuple(sorted(set(lambda1) | set(contraction)))
    union_labels = touching_rows(
        {monomial: 1 for monomial in union_support}, generators
    )
    union_matrix = row_matrix(union_support, union_labels, generators)
    union_ranks = tuple(rank_mod_p(union_matrix, prime) for prime in PRIMES)
    union_rational_rank = rank_over_q(union_matrix)
    require(union_ranks[0] == union_ranks[1], union_ranks)
    require(union_rational_rank == union_ranks[0],
            (union_rational_rank, union_ranks))
    require(annihilates(union_matrix, lambda1, union_support),
            "lambda1 not in union annihilator")
    require(annihilates(union_matrix, contraction, union_support),
            "contraction not in union annihilator")
    require((len(union_support), len(union_labels), union_rational_rank)
            == (145, 125, 109),
            (len(union_support), len(union_labels), union_rational_rank))
    restriction = {
        monomial: contraction.get(monomial, 0) for monomial in lambda1
        if contraction.get(monomial, 0)
    }
    restriction_scalar = proportional(restriction, lambda1)

    k1_result = json.loads(K1_RESULT.read_text())
    k2_result = json.loads(K2_RESULT.read_text())
    k0_result = json.loads(K0_RESULT.read_text())
    pairings = (
        k0_result["integer_separator"]["target_pairing"],
        k1_result["exact_separator"]["target_pairing"],
        k2_result["exact_separator"]["target_pairing"],
    )
    target1 = K1.S.target_polynomial()
    target0 = D9.target_minor()
    contraction10_pairing = sum(
        coefficient * contraction10.get(monomial, 0)
        for monomial, coefficient in target0.items()
    )
    require(contraction10_pairing == pairings[1],
            (contraction10_pairing, pairings[1]))
    contraction_pairing = sum(
        coefficient * contraction.get(monomial, 0)
        for monomial, coefficient in target1.items()
    )
    require(contraction_pairing == pairings[2],
            (contraction_pairing, pairings[2]))
    require((transition10, transition_scalar, pairings) ==
            (None, None, (1, 2, 28)),
            (transition10, transition_scalar, pairings))
    require((len(contraction10_support), len(contraction10_labels),
             contraction10_rational_rank) == (21, 7, 7),
            (len(contraction10_support), len(contraction10_labels),
             contraction10_rational_rank))
    require((len(union0_support), len(union0_labels), union0_rational_rank)
            == (22, 7, 7),
            (len(union0_support), len(union0_labels), union0_rational_rank))
    result = {
        "status": "BOUNDED exact Krylov audit",
        "quotient": "Q=Q[A_e,ab]/(all homogeneous mixed X5 amplitudes)",
        "classes": ["[Delta]", "[F0*Delta]", "[F0^2*Delta]"],
        "fine_graded_dual_shells": [
            {
                "degree": 13,
                "separator_support": len(lambda1),
                "touching_rows": len(labels[0]),
                "row_ranks": dict(zip(map(str, PRIMES), ranks[0])),
                "rational_row_rank": rational_ranks[0],
                "exact_nullity": nullities[0],
                "separator_digest": entries_digest(lambda1),
                "target_pairing": pairings[1],
            },
            {
                "degree": 17,
                "separator_support": len(lambda2),
                "touching_rows": len(labels[1]),
                "row_ranks": dict(zip(map(str, PRIMES), ranks[1])),
                "rational_row_rank": rational_ranks[1],
                "exact_nullity": nullities[1],
                "separator_digest": entries_digest(lambda2),
                "target_pairing": pairings[2],
            },
        ],
        "multiplication_by_F0_dual": {
            "definition": "m_F0^*(lambda)(q)=lambda(F0*q)",
            "pure_terms": len(pure_terms),
            "degree13_to_degree9": {
                "contracted_support": len(contraction10),
                "contracted_digest": entries_digest(contraction10),
                "proportional_to_degree9_separator": transition10 is not None,
                "transition_scalar": transition10,
                "touching_rows": len(contraction10_labels),
                "row_ranks": dict(zip(map(str, PRIMES), contraction10_ranks)),
                "rational_row_rank": contraction10_rational_rank,
                "exact_shell_nullity": (
                    len(contraction10_support) - contraction10_rational_rank
                ),
                "target_pairing": contraction10_pairing,
                "pairing_consistency": (
                    None if transition10 is None
                    else transition10 * pairings[0] == pairings[1]
                ),
            },
            "degree17_to_degree13": {
            "contracted_support": len(contraction),
            "contracted_digest": entries_digest(contraction),
            "proportional_to_degree13_separator": transition_scalar is not None,
            "transition_scalar": transition_scalar,
            "support_overlap_with_frozen_degree13_separator": len(
                set(contraction) & set(lambda1)
            ),
            "restriction_to_frozen_support_scalar": restriction_scalar,
            "touching_rows": len(contraction_labels),
            "row_ranks": dict(zip(map(str, PRIMES), contraction_ranks)),
            "rational_row_rank": contraction_rational_rank,
            "exact_shell_nullity": (
                len(contraction_support) - contraction_rational_rank
            ),
            "target_pairing": contraction_pairing,
            "pairing_consistency": (
                None if transition_scalar is None
                else transition_scalar * pairings[1] == pairings[2]
            ),
            },
        },
        "primal_cyclic_line_maps": [
            {
                "map": "[Delta] -> [F0*Delta]",
                "source_nonzero": pairings[0] != 0,
                "image_nonzero": pairings[1] != 0,
                "rank_on_source_line": 1,
                "injective_on_source_line": True,
            },
            {
                "map": "[F0*Delta] -> [F0^2*Delta]",
                "source_nonzero": pairings[1] != 0,
                "image_nonzero": pairings[2] != 0,
                "rank_on_source_line": 1,
                "injective_on_source_line": True,
            },
        ],
        "krylov": {
            "observed_pairing_sequence": list(pairings),
            "observed_krylov_dimension": 3,
            "first_transition_scalar": transition10,
            "observed_transition_scalar": transition_scalar,
            "observed_minimal_polynomial": (
                None if transition_scalar is None else f"t-{transition_scalar}"
            ),
            "scope": "three nonzero classes through degree 17; two dual contractions",
            "degree9_union_support": len(union0_support),
            "degree9_union_touching_rows": len(union0_labels),
            "degree9_union_row_ranks": dict(zip(map(str, PRIMES), union0_ranks)),
            "degree9_union_rational_row_rank": union0_rational_rank,
            "degree9_union_exact_nullity": len(union0_support) - union0_rational_rank,
            "degree13_union_support": len(union_support),
            "degree13_union_touching_rows": len(union_labels),
            "degree13_union_row_ranks": dict(zip(map(str, PRIMES), union_ranks)),
            "degree13_union_rational_row_rank": union_rational_rank,
            "degree13_union_exact_nullity": len(union_support) - union_rational_rank,
            "minimal_polynomial_constraint": (
                "The quotient is graded and deg(F0)=4, so a scalar polynomial "
                "annihilating [Delta] must be a monomial t^m. The three frozen "
                "nonzero classes force m>=3; the data do not decide whether "
                "t^3[Delta] vanishes."
            ),
        },
        "verdict": None,
        "source_sha256": {
            "k1_source": sha256(K1_SOURCE.read_bytes()).hexdigest(),
            "k2_source": sha256(K2_SOURCE.read_bytes()).hexdigest(),
            "k1_result": sha256(K1_RESULT.read_bytes()).hexdigest(),
            "k2_result": sha256(K2_RESULT.read_bytes()).hexdigest(),
            "k0_result": sha256(K0_RESULT.read_bytes()).hexdigest(),
        },
    }
    if transition_scalar is not None and nullities == (1, 1):
        result["verdict"] = (
            "The two frozen separator shells form a one-dimensional dual "
            "transition on which m_F0^* is nonzero, so multiplication is "
            "injective on this k=1 to k=2 cyclic quotient line. This does "
            "not make the line stable at k=3: no degree-21 shell or lift is "
            "defined by the two-step data, so all-k nonvanishing does not follow."
        )
    else:
        result["verdict"] = (
            "The degree-17 separator contracts to a distinct degree-13 dual "
            "direction rather than preserving the frozen separator line. The "
            "preceding degree13-to-degree9 contraction also leaves its frozen "
            "separator line, so no rank-one transition is present even at the "
            "first dual step. The "
            "combined support actually has a 36-dimensional exact annihilator, "
            "so the two known directions do not define a closed Krylov block. "
            "Both displayed primal line maps are individually injective, but "
            "no uniform injective/stable submodule is determined. The only "
            "possible minimal polynomial is t^m with m>=3, so k=3 is "
            "genuinely new."
        )
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-lambda2", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate_lambda2)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(text)
    if args.check_results:
        require(OUT.exists() and OUT.read_text() == text,
                "stored saturation/Krylov result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
