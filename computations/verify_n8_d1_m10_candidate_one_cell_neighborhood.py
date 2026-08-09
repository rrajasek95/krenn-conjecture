#!/usr/bin/env python3
"""Exact coefficient closure of every one-cell extension of the m=10 support."""

from __future__ import annotations

import hashlib
import importlib
import os
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED = {
    "verify_n8_d1_m10_334_branch63_candidate.py":
        "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca",
    "verify_n8_d1_m10_334_branch63_ideal_closure.py":
        "884a453002824eb99fe4cda57f1adfbf14d64f636d91cef441b4721c63d96fe5",
    "verify_n8_d1_m11_six_candidate_closure.py":
        "e4c09bc532109109c42b286218d91fd8e0043a03377ce401ee77560872c0168e",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned D1 coefficient source changed: " + filename)

C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
K = importlib.import_module("verify_n8_d1_m10_334_branch63_ideal_closure")
E = importlib.import_module("verify_n8_d1_m11_six_candidate_closure")
D = C.D

EXPECTED_LEDGER_SHA256 = (
    "bf2eab98ffb22213c7cce1951670ab5d13d36e22c3e2400eacfa767dd17db899"
)


def monomial_poly(monomial, coefficient=1):
    return {tuple(sorted(monomial)): Fraction(coefficient)}


def monomial_product(*monomials):
    return tuple(sorted(name for monomial in monomials for name in monomial))


def exponent_difference(first, second):
    difference = Counter(first)
    difference.subtract(second)
    return tuple(sorted((name, exponent)
                        for name, exponent in difference.items()
                        if exponent))


def scale_difference(difference, scalar):
    return tuple((name, scalar * exponent) for name, exponent in difference)


def add_differences(left, right):
    result = Counter(dict(left))
    result.update(dict(right))
    return tuple(sorted((name, exponent)
                        for name, exponent in result.items()
                        if exponent))


def full_binomials(records):
    rows = []
    for index, record in enumerate(records):
        if "full_exactness" not in record["families"]:
            continue
        polynomial = K.artifact_polynomial(record)
        if len(polynomial) != 2 or set(polynomial.values()) != {Fraction(1)}:
            continue
        first, second = sorted(polynomial)
        rows.append({
            "index": index,
            "record": record,
            "polynomial": polynomial,
            "first": first,
            "second": second,
            "difference": exponent_difference(first, second),
        })
    return rows


def first_odd_circuit(records, support_names):
    rows = full_binomials(records)
    by_difference = defaultdict(list)
    for row in rows:
        by_difference[row["difference"]].append(row)
    choice = None
    for first_position, first in enumerate(rows):
        for second in rows[first_position + 1:]:
            for second_sign in (1, -1):
                subtotal = add_differences(
                    first["difference"],
                    scale_difference(second["difference"], second_sign),
                )
                target = scale_difference(subtotal, -1)
                for third_sign, lookup in (
                    (1, target), (-1, scale_difference(target, -1))
                ):
                    for third in by_difference.get(lookup, ()):
                        if third["index"] in (first["index"], second["index"]):
                            continue
                        choice = ((first, 1), (second, second_sign),
                                  (third, third_sign))
                        break
                    if choice is not None:
                        break
                if choice is not None:
                    break
            if choice is not None:
                break
        if choice is not None:
            break
    require(choice is not None, "no three-binomial odd circuit was found")

    oriented = []
    total_difference = ()
    for row, sign in choice:
        first, second = row["first"], row["second"]
        if sign == -1:
            first, second = second, first
        oriented.append((row, first, second))
        total_difference = add_differences(
            total_difference, exponent_difference(first, second)
        )
    require(not total_difference, "the selected odd circuit does not close")

    (row1, a1, b1), (row2, a2, b2), (row3, a3, b3) = oriented
    first_product = monomial_product(a1, a2, a3)
    second_product = monomial_product(b1, b2, b3)
    require(first_product == second_product,
            "the odd circuit products do not agree")

    # (a1+b1)a2a3 - b1(a2+b2)a3 + b1b2(a3+b3) = 2 a1a2a3.
    cofactors = (
        monomial_poly(monomial_product(a2, a3)),
        monomial_poly(monomial_product(b1, a3), -1),
        monomial_poly(monomial_product(b1, b2)),
    )
    generators = (row1["polynomial"], row2["polynomial"],
                  row3["polynomial"])
    compact = D.p_const(0)
    for cofactor, generator in zip(cofactors, generators):
        compact = D.p_add(compact, D.p_mul(cofactor, generator))
    twice_product = monomial_poly(first_product, 2)
    require(compact == twice_product,
            "the compact odd-circuit certificate failed")
    require(set(first_product) <= set(support_names),
            "the compact certificate uses a nonlocalized variable")

    product_counts = Counter(first_product)
    saturation_power = max(product_counts.values())
    u_power = tuple(sorted(name for name in support_names
                           for _repeat in range(saturation_power)))
    quotient = K.monomial_quotient(
        u_power, first_product, Fraction(1, 2)
    )
    certificate = D.p_const(0)
    for cofactor, generator in zip(cofactors, generators):
        certificate = D.p_add(
            certificate,
            D.p_mul(D.p_mul(quotient, cofactor), generator),
        )
    require(certificate == monomial_poly(u_power),
            "the ordinary-ring saturation certificate failed")

    return {
        "full_binomials": len(rows),
        "generator_indices": [row["index"] for row, _sign in choice],
        "generator_sha256": D.content_hash(
            [row["record"] for row, _sign in choice]
        ),
        "orientation_signs": [sign for _row, sign in choice],
        "compact_monomial_degree": len(first_product),
        "ordinary_saturation_power": saturation_power,
    }


def audit():
    started = monotonic()
    inherited_ledger, inherited_digest, _seconds = E.audit()
    artifact = C.build_artifact()
    base_support = {
        tuple(entry) for entry in artifact["localized_nonzero_cells"]
    }
    _state, _extras, _support, admissible, _stats = C.candidate_input()
    invisible = {
        tuple(entry) for entry in inherited_ledger[
            "maximal_witness_invisible_subcube"
        ]["invisible_cells"]
    }
    visible_boundary = sorted((admissible - base_support) - invisible)
    require(len(base_support) == 77 and len(admissible - base_support) == 140,
            "the candidate one-cell neighborhood changed")
    require(len(invisible) == 107 and len(visible_boundary) == 33,
            "the visible/invisible boundary split changed")

    rows = []
    for cell in visible_boundary:
        support = base_support | {cell}
        records = C.coefficient_generators(support)
        support_names = tuple("x_%d%d_%d%d" % entry
                              for entry in sorted(support))
        circuit = first_odd_circuit(records, support_names)
        rows.append({
            "extension": list(cell),
            "coefficient_generators": len(records),
            **circuit,
        })
    require(len(rows) == 33,
            "not every visible one-cell extension was certified")
    require(all(row["ordinary_saturation_power"] <= 3 for row in rows),
            "a selected circuit exceeded the frozen saturation exponent")

    ledger = {
        "pinned_sources": PINNED,
        "base_localized_variables": len(base_support),
        "admissible_one_cell_extensions": len(admissible - base_support),
        "inherited_invisible_extensions": len(invisible),
        "inherited_ledger_sha256": inherited_digest,
        "new_visible_extensions": len(rows),
        "visible_rows": rows,
        "certificate_identity": (
            "(a1+b1)a2a3-b1(a2+b2)a3+b1b2(a3+b3)=2a1a2a3"
        ),
        "characteristic_scope": "empty over every field of characteristic != 2",
        "status": (
            "all 140 admissible one-cell extensions of the m10 semantic "
            "support have empty localized coefficient ideals"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the one-cell-neighborhood ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 m10 candidate one-cell neighborhood: PASS (exact)")
    print("inherited invisible extensions:",
          ledger["inherited_invisible_extensions"])
    print("new visible odd-circuit extensions:",
          ledger["new_visible_extensions"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
