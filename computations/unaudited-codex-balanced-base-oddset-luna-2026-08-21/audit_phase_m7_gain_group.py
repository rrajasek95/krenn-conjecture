#!/usr/bin/env python3
"""Census the coefficient/gain group for complete binary m=7 binomial states."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_balanced_base_oddset_luna import ONE, qlabel, qmul  # noqa: E402
from emit_phase_m7_1222_k4_support_smt import build_polynomials  # noqa: E402


OUT = HERE / "results_phase_m7_gain_group.json"


def qneg(value):
    return -value[0], -value[1]


def qinv(value):
    a, b = value
    norm = a * a - a * b + b * b
    return (a - b) / norm, -b / norm


def qdiv(left, right):
    return qmul(left, qinv(right))


def qpow(value, exponent):
    answer = ONE
    for _ in range(exponent):
        answer = qmul(answer, value)
    return answer


def norm(value):
    a, b = value
    return a * a - a * b + b * b


def factor_integer(value):
    value = abs(value)
    answer = Counter()
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            answer[divisor] += 1
            value //= divisor
        divisor += 1
    if value > 1:
        answer[value] += 1
    return answer


def factor_fraction(value):
    answer = factor_integer(value.numerator)
    for prime, exponent in factor_integer(value.denominator).items():
        answer[prime] -= exponent
    return {str(prime): exponent for prime, exponent in sorted(answer.items()) if exponent}


def torsion_order(value):
    for order in range(1, 13):
        if qpow(value, order) == ONE:
            return order
    return None


def main():
    polynomials, raw = build_polynomials(False)
    coefficient_counts = Counter()
    gain_counts = Counter()
    pair_states = 0
    for (word, _degree), terms in polynomials.items():
        if word in ((0,) * 8, (1,) * 8):
            continue
        coefficients = [coefficient for _monomial, coefficient in terms]
        coefficient_counts.update(coefficients)
        histogram = Counter(coefficients)
        values = sorted(histogram)
        for left_index, left in enumerate(values):
            same_pairs = histogram[left] * (histogram[left] - 1) // 2
            if same_pairs:
                gain_counts[qneg(ONE)] += same_pairs
                pair_states += same_pairs
            for right in values[left_index + 1:]:
                multiplicity = histogram[left] * histogram[right]
                gain = qneg(qdiv(right, left))
                gain_counts[gain] += multiplicity
                pair_states += multiplicity
    gains = []
    norm_primes = set()
    for value, count in sorted(gain_counts.items(), key=lambda item: qlabel(item[0])):
        value_norm = norm(value)
        factors = factor_fraction(value_norm)
        norm_primes.update(factors)
        gains.append({
            "value": qlabel(value),
            "count": count,
            "norm": str(value_norm),
            "norm_prime_exponents": factors,
            "torsion_order_le_12": torsion_order(value),
        })
    output = {
        "raw_matching_terms": raw,
        "distinct_coefficients": [
            {"value": qlabel(value), "count": count, "norm": str(norm(value))}
            for value, count in sorted(coefficient_counts.items(), key=lambda item: qlabel(item[0]))
        ],
        "potential_binomial_pair_states": pair_states,
        "distinct_gains": gains,
        "norm_primes": sorted(norm_primes, key=int),
        "all_gains_torsion": all(item["torsion_order_le_12"] is not None for item in gains),
        "guard": (
            "Pair states range over every pair of exact Laurent monomials in a "
            "literal mixed row; support guards are not imposed in this census."
        ),
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "coefficients": len(output["distinct_coefficients"]),
        "pair_states": pair_states,
        "gains": len(gains),
        "norm_primes": output["norm_primes"],
        "all_torsion": output["all_gains_torsion"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
