#!/usr/bin/env python3
"""Replay an exact pure-product certificate on the normalized n=8 chart.

In the 48-variable slice obtained by normalizing the twelve boundary
coordinates and zeroing coordinates outside the audited 60-edge set, this
checker proves the literal integer polynomial identity

    sum_i A_i H_{c_i} = 2 H_0 H_1 H_2,

where every c_i is mixed.  Thus, in characteristic zero, the pure product
already belongs to the restricted mixed ideal; its saturation is the unit
ideal.  The sparse certificate has 73 mixed generators and 282 multiplier
terms and is replayed without a computer-algebra dependency.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
SPARSE_CHECKER = HERE / "verify_n8_localized_dual_edge_sparse_no_go.py"
SPEC = importlib.util.spec_from_file_location("n8_sparse", SPARSE_CHECKER)
SPARSE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SPARSE)

CERTIFICATE_PATH = (
    HERE / "certificates" / "n8_60_edge_pure_product_certificate.json"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "e90d1cee54a33aee9ce46b7f1fffd5b6e580bcd5f324375fbd09e780252538bb"
)
EXPECTED_LEDGER_SHA256 = (
    "99d1811c80b3cf24ee7e0b54c404283cfa6a17c1e07ad512c4e98fa10a19cb78"
)


def clean(polynomial):
    return {monomial: coefficient for monomial, coefficient
            in polynomial.items() if coefficient}


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
    return clean(answer)


def as_polynomial(coefficient):
    return clean(dict(coefficient))


def audit():
    certificate_bytes = CERTIFICATE_PATH.read_bytes()
    certificate_digest = sha256(certificate_bytes).hexdigest()
    certificate = json.loads(certificate_bytes)
    require(certificate["index_base"] == 1, "certificate index base")
    require(certificate["mixed_polynomial_count"] == 900,
            "certificate mixed-polynomial count")

    mixed_by_polynomial = defaultdict(list)
    for word in product(SPARSE.COLOURS, repeat=8):
        if len(set(word)) == 1:
            continue
        polynomial = SPARSE.coefficient(word)
        if polynomial:
            mixed_by_polynomial[polynomial].append(word)
    mixed_polynomials = tuple(sorted(mixed_by_polynomial, key=repr))
    require(len(mixed_polynomials) == 900,
            "restricted distinct mixed coefficient count changed")

    pure_polynomials = tuple(
        as_polynomial(SPARSE.coefficient((colour,) * 8))
        for colour in SPARSE.COLOURS
    )
    pure_product = {(): 1}
    for pure in pure_polynomials:
        pure_product = multiply(pure_product, pure)

    image = {}
    used_indices = []
    multiplier_term_count = 0
    multiplier_degree_histogram = Counter()
    representative_words = []
    for index, raw_terms in certificate["entries"]:
        require(1 <= index <= len(mixed_polynomials),
                "certificate generator index out of range")
        multiplier = defaultdict(int)
        for coefficient, monomial in raw_terms:
            require(all(0 <= variable < len(SPARSE.EXTRA_VARIABLES)
                        for variable in monomial),
                    "certificate multiplier variable out of range")
            multiplier[tuple(sorted(monomial))] += coefficient
            multiplier_degree_histogram[len(monomial)] += 1
        multiplier = clean(multiplier)
        require(multiplier, "zero multiplier in sparse certificate")
        generator = as_polynomial(mixed_polynomials[index - 1])
        add_polynomial(image, multiply(multiplier, generator))
        used_indices.append(index)
        multiplier_term_count += len(multiplier)
        representative_words.append(
            list(min(mixed_by_polynomial[mixed_polynomials[index - 1]]))
        )

    require(len(used_indices) == len(set(used_indices)) == 73,
            "certificate generator support changed")
    require(multiplier_term_count == 282,
            "certificate multiplier term count changed")
    expected_image = {
        monomial: 2 * coefficient
        for monomial, coefficient in pure_product.items()
    }
    require(image == expected_image,
            "exact pure-product certificate replay failed")

    ledger = {
        "normalized_boundary_coordinates": 12,
        "allowed_edge_coordinates": 60,
        "slice_variables": len(SPARSE.EXTRA_VARIABLES),
        "distinct_mixed_generators": len(mixed_polynomials),
        "used_mixed_generators": len(used_indices),
        "multiplier_terms": multiplier_term_count,
        "multiplier_degree_histogram": dict(sorted(
            multiplier_degree_histogram.items()
        )),
        "pure_product_terms": len(pure_product),
        "certificate_scalar": 2,
        "used_generator_indices": used_indices,
        "representative_mixed_words": representative_words,
        "certificate_sha256": certificate_digest,
        "identity": "sum A_i H_mixed_i = 2 H_0 H_1 H_2",
        "conclusion": (
            "H_0 H_1 H_2 belongs to the normalized 60-edge mixed ideal "
            "over characteristic zero"
        ),
    }
    return ledger


def main():
    ledger = audit()
    require(ledger["certificate_sha256"] == EXPECTED_CERTIFICATE_SHA256,
            "frozen certificate file digest changed")
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen pure-product ledger digest changed")
    print(
        "n=8 normalized 60-edge pure product: PASS; "
        f"generators={ledger['used_mixed_generators']}, "
        f"multiplier_terms={ledger['multiplier_terms']}, "
        f"scalar={ledger['certificate_scalar']}"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
