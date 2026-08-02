#!/usr/bin/env python3
"""Exact one-generator pure-product identity on the chart-25 carrier."""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DUAL_PATH = HERE / "verify_n8_chart25_boundary_dual.py"
SPEC = importlib.util.spec_from_file_location("n8_chart25_dual", DUAL_PATH)
DUAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DUAL)
FULL = DUAL.FULL

EXPECTED_LEDGER_SHA256 = (
    "343a85a8d70e9cc7c80be8f0ca82cb2d2886dca9ce354c11dc107668c138e310"
)
MIXED_WORD = (1, 1, 1, 1, 2, 2, 2, 2)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_polynomial(target, source, scalar=1):
    for monomial, coefficient in source.items():
        value = target.get(monomial, 0) + scalar * coefficient
        if value:
            target[monomial] = value
        else:
            target.pop(monomial, None)


def multiply(left, right):
    answer = defaultdict(int)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return dict(answer)


def expanded_dual():
    certificate = [
        {"sign": value, "row": [list(variable) for variable in row]}
        for value, row in DUAL.EXACT_DUAL
    ]
    return FULL.expanded_rational_functional(certificate)


def restricted_coefficient(word, allowed):
    answer = defaultdict(int)
    for term in FULL.word_terms(word):
        if all(variable in allowed for variable in term):
            answer[term] += 1
    return dict(answer)


def support_completion(extra_monomial, word):
    degrees = Counter((vertex, word[vertex]) for vertex in range(8))
    for left, right, left_colour, right_colour in extra_monomial:
        degrees[left, left_colour] += 1
        degrees[right, right_colour] += 1
    completion = []
    for variable in FULL.SUPPORT_PRODUCT:
        left, right, left_colour, right_colour = variable
        require(degrees[left, left_colour] == degrees[right, right_colour],
                "normalized multiplier term has no support completion")
        exponent = 1 - degrees[left, left_colour]
        require(exponent in (0, 1),
                "chart 25 certificate unexpectedly needs a denominator")
        completion.extend((variable,) * exponent)
    return tuple(completion)


def audit():
    DUAL.configure_chart25()
    functional = expanded_dual()
    allowed = frozenset(variable for row in functional for variable in row)
    require(len(allowed) == 36 and FULL.SUPPORT_SET <= allowed,
            "chart 25 coordinate carrier changed")
    extras = tuple(sorted(allowed - FULL.SUPPORT_SET))
    require(len(extras) == 24, "chart 25 normalized variable count changed")

    # These four normalized monomials are
    # (1+x_3 x_12)(1+x_16 x_19) in one-based extra-variable notation.
    normalized_multiplier = (
        (),
        (extras[2], extras[11]),
        (extras[15], extras[18]),
        (extras[2], extras[11], extras[15], extras[18]),
    )
    multiplier = {}
    completion_sizes = []
    for monomial in normalized_multiplier:
        completion = support_completion(monomial, MIXED_WORD)
        full_monomial = tuple(sorted(monomial + completion))
        require(len(full_monomial) == 8,
                "rehomogenized multiplier has wrong degree")
        multiplier[full_monomial] = 1
        completion_sizes.append(len(completion))
    require(len(multiplier) == 4 and sorted(completion_sizes) == [4, 6, 6, 8],
            "chart 25 multiplier census changed")

    mixed = restricted_coefficient(MIXED_WORD, allowed)
    pure = tuple(
        restricted_coefficient((colour,) * 8, allowed)
        for colour in range(3)
    )
    target = {(): 1}
    for polynomial in pure:
        target = multiply(target, polynomial)
    image = multiply(multiplier, mixed)
    require(image == target,
            "chart 25 exact pure-product identity failed")
    require(len(mixed) == 4 and tuple(map(len, pure)) == (1, 4, 4)
            and len(target) == 16,
            "chart 25 polynomial census changed")

    # Restore all 252 variables and find the first nonzero off-chart tail
    # without materializing the 105^3 pure-product rows.
    full_image = {}
    for multiplier_monomial in multiplier:
        for term in FULL.word_terms(MIXED_WORD):
            row = tuple(sorted(multiplier_monomial + term))
            full_image[row] = full_image.get(row, 0) + 1
    pure_terms = tuple(FULL.word_terms((colour,) * 8) for colour in range(3))
    pure_degree_counts = []
    for terms in pure_terms:
        pure_degree_counts.append(Counter(
            sum(variable not in allowed for variable in term) for term in terms
        ))
    target_degree_counts = Counter()
    for first_degree, first_count in pure_degree_counts[0].items():
        for second_degree, second_count in pure_degree_counts[1].items():
            for third_degree, third_count in pure_degree_counts[2].items():
                target_degree_counts[
                    first_degree + second_degree + third_degree
                ] += first_count * second_count * third_count
    require(sum(target_degree_counts.values()) == 105 ** 3,
            "full pure-product target census changed")
    residual_histograms = {
        degree: Counter({-1: count})
        for degree, count in target_degree_counts.items()
    }
    for row, coefficient in full_image.items():
        degree = sum(variable not in allowed for variable in row)
        histogram = residual_histograms.setdefault(degree, Counter())
        diagonal = all(variable[2] == variable[3] for variable in row)
        if diagonal:
            histogram[-1] -= 1
            if coefficient != 1:
                histogram[coefficient - 1] += 1
        else:
            histogram[coefficient] += 1
    residual_histograms = {
        degree: {value: count for value, count in histogram.items() if count}
        for degree, histogram in residual_histograms.items()
    }
    first_residual_degree = min(
        degree for degree, histogram in residual_histograms.items()
        if histogram
    )
    require(not residual_histograms.get(0)
            and not residual_histograms.get(1)
            and first_residual_degree >= 2,
            "chart 25 full lift acquired a lower residual")

    # Count every distinct restricted mixed polynomial independently.
    distinct_mixed = set()
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        polynomial = restricted_coefficient(word, allowed)
        if polynomial:
            distinct_mixed.add(tuple(sorted(polynomial.items())))
    require(len(distinct_mixed) == 254,
            "chart 25 distinct mixed-polynomial count changed")

    ledger = {
        "chart": 25,
        "allowed_coordinates": len(allowed),
        "support_coordinates": len(FULL.SUPPORT_SET),
        "normalized_variables": len(extras),
        "distinct_mixed_polynomials": len(distinct_mixed),
        "certificate_mixed_generators": 1,
        "certificate_multiplier_terms": len(multiplier),
        "certificate_multiplier_completion_sizes": sorted(completion_sizes),
        "certificate_denominators": 0,
        "mixed_terms": len(mixed),
        "pure_term_counts": tuple(map(len, pure)),
        "pure_product_terms": len(target),
        "full_target_degree_counts": dict(sorted(target_degree_counts.items())),
        "full_mixed_image_rows": len(full_image),
        "first_full_lift_residual_degree": first_residual_degree,
        "first_full_lift_residual_rows": sum(
            residual_histograms[first_residual_degree].values()
        ),
        "first_full_lift_coefficient_histogram": dict(sorted(
            residual_histograms[first_residual_degree].items()
        )),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "chart 25 pure-product ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 pure-product membership: PASS")
    print("allowed coordinates:", ledger["allowed_coordinates"])
    print("normalized variables:", ledger["normalized_variables"])
    print("mixed generators used:", ledger["certificate_mixed_generators"])
    print("multiplier terms:", ledger["certificate_multiplier_terms"])
    print("pure-product terms:", ledger["pure_product_terms"])
    print("first full-lift residual rows:",
          ledger["first_full_lift_residual_rows"])
    print("first full-lift residual degree:",
          ledger["first_full_lift_residual_degree"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
