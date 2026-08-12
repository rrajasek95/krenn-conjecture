#!/usr/bin/env python3
"""Verify the universal Euler contraction behind the order-six lift.

The coefficient-prolonging faces of a normally ordered differential
operator are the de Rham differential in its commuting differential symbols
``xi_i``.  On a monomial ``xi^alpha dxi_I`` the Euler contraction satisfies

    d i_E + i_E d = (|alpha| + |I|) id.

Over characteristic zero this contracts every positive-total-degree piece.
The audit is exhaustive for five symbols, polynomial degree at most six,
and every exterior degree.  It is a universal Spencer statement, not a
physical labelled-quotient descent.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py":
        "164d67345fe7a83d0ace581ba4417b31e3166dc5a88e487bd5ee6f2a15e5c824",
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "edc3e79ff56a63e0005a449fb100c6dbc4ec2dd02a40f75ca8c23a5095730f26",
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
}
EXPECTED_LEDGER_SHA256 = (
    "c8e88a844687b5f4855a9e160403cb73aa9ffd3398518de8ba60cd1126a74af7"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def weak_compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for remainder in weak_compositions(total - first, length - 1):
            yield (first,) + remainder


def add_scaled(target, source, scalar=1):
    for basis, value in source.items():
        target[basis] += scalar * value
        if not target[basis]:
            del target[basis]


def exterior_derivative(basis):
    """d(xi^alpha dxi_I)."""
    alpha, wedge = basis
    output = Counter()
    wedge_set = set(wedge)
    for index, exponent in enumerate(alpha):
        if not exponent or index in wedge_set:
            continue
        sign = -1 if sum(entry < index for entry in wedge) % 2 else 1
        next_alpha = list(alpha)
        next_alpha[index] -= 1
        next_wedge = tuple(sorted((index,) + wedge))
        output[(tuple(next_alpha), next_wedge)] += sign * exponent
    return output


def euler_contraction(basis):
    """i_E(xi^alpha dxi_I), E=sum xi_i partial/partial xi_i."""
    alpha, wedge = basis
    output = Counter()
    for position, index in enumerate(wedge):
        next_alpha = list(alpha)
        next_alpha[index] += 1
        next_wedge = wedge[:position] + wedge[position + 1:]
        sign = -1 if position % 2 else 1
        output[(tuple(next_alpha), next_wedge)] += sign
    return output


def apply(linear_map, vector):
    output = Counter()
    for basis, coefficient in vector.items():
        add_scaled(output, linear_map(basis), coefficient)
    return output


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))

    symbols = 5
    maximum_polynomial_degree = 6
    basis_count = 0
    positive_basis_count = 0
    by_total_degree = Counter()
    for polynomial_degree in range(maximum_polynomial_degree + 1):
        for alpha in weak_compositions(polynomial_degree, symbols):
            for exterior_degree in range(symbols + 1):
                for wedge in combinations(range(symbols), exterior_degree):
                    basis = (alpha, wedge)
                    basis_count += 1
                    total_degree = polynomial_degree + exterior_degree
                    by_total_degree[total_degree] += 1

                    d_basis = exterior_derivative(basis)
                    h_basis = euler_contraction(basis)
                    require(not apply(exterior_derivative, d_basis),
                            ("d squared is nonzero", basis))
                    require(not apply(euler_contraction, h_basis),
                            ("Euler contraction squared is nonzero", basis))

                    cartan = Counter()
                    add_scaled(cartan, apply(exterior_derivative, h_basis))
                    add_scaled(cartan, apply(euler_contraction, d_basis))
                    expected = Counter({basis: total_degree})
                    require(cartan == expected,
                            ("Cartan identity failed", basis, cartan,
                             expected))

                    if not total_degree:
                        continue
                    positive_basis_count += 1
                    normalized = Counter({
                        term: Fraction(value, total_degree)
                        for term, value in h_basis.items()
                    })
                    contraction = Counter()
                    add_scaled(contraction,
                               apply(exterior_derivative, normalized))
                    normalized_d = Counter()
                    for term, value in d_basis.items():
                        term_total = sum(term[0]) + len(term[1])
                        require(term_total == total_degree,
                                "d changed total Spencer degree")
                        add_scaled(normalized_d,
                                   euler_contraction(term),
                                   Fraction(value, term_total))
                    add_scaled(contraction, normalized_d)
                    require(contraction == Counter({basis: Fraction(1)}),
                            ("normalized Euler homotopy failed", basis,
                             contraction))

    ledger = {
        "theorem": "universal positive-degree Spencer acyclicity",
        "symbols": symbols,
        "maximum_polynomial_degree": maximum_polynomial_degree,
        "basis_count": basis_count,
        "positive_basis_count": positive_basis_count,
        "basis_by_total_degree": dict(sorted(by_total_degree.items())),
        "identities": [
            "d^2=0",
            "i_E^2=0",
            "d i_E+i_E d=(polynomial_degree+exterior_degree) id",
            "d H+H d=id in positive total degree over Q",
        ],
        "scope": (
            "the universal normally ordered differential-symbol Spencer "
            "complex only; physical fine-grade descent and augmented "
            "terminal compatibility are not asserted"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("universal Spencer ledger changed", digest))
    print("h3 universal Spencer Euler contraction: PASS")
    print("basis states:", basis_count)
    print("positive states contracted:", positive_basis_count)
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    audit()
