#!/usr/bin/env python3
"""Verify the explicit Cartan prism for the signed SL2 Weyl element.

On polynomial differential forms in two variables put

    E = x d/dy,    F = y d/dx,
    L_E = d i_E + i_E d,    L_F = d i_F + i_F d.

The root unipotents exp(L_E), exp(-L_F), exp(L_E) multiply to the
signed Weyl action x -> -y, y -> x.  The finite Cartan series give an
explicit homotopy from that Weyl action to the identity.  The audit checks
all polynomial degrees through six and every exterior degree exactly over Q.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import factorial
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
    "computations/verify_h3_universal_spencer_euler_contraction.py":
        "4e4e4810dc49ab366555288ab7c696047cd3ce79ab7dc4b159b38047def8942b",
}
EXPECTED_LEDGER_SHA256 = (
    "bde6a55fb7061024ff741b38acd22f02d2299d7e77f704eebeb9298b7b5abbb2"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add_scaled(target, source, scalar=Q(1)):
    for basis, value in source.items():
        target[basis] += scalar * value
        if not target[basis]:
            del target[basis]


def apply(linear_map, vector):
    answer = Counter()
    for basis, value in vector.items():
        add_scaled(answer, linear_map(basis), value)
    return answer


def exterior_derivative(basis):
    a, b, wedge = basis
    answer = Counter()
    for index, exponent in enumerate((a, b)):
        if not exponent or index in wedge:
            continue
        next_exponents = [a, b]
        next_exponents[index] -= 1
        position = sum(entry < index for entry in wedge)
        sign = -1 if position % 2 else 1
        next_wedge = tuple(sorted((index,) + wedge))
        answer[(next_exponents[0], next_exponents[1], next_wedge)] += (
            sign * exponent
        )
    return answer


def interior(basis, field):
    """Contract by E=x d/dy or F=y d/dx."""
    a, b, wedge = basis
    answer = Counter()
    selected = 1 if field == "E" else 0
    if selected not in wedge:
        return answer
    position = wedge.index(selected)
    sign = -1 if position % 2 else 1
    next_wedge = wedge[:position] + wedge[position + 1:]
    if field == "E":
        answer[(a + 1, b, next_wedge)] += sign
    else:
        answer[(a, b + 1, next_wedge)] += sign
    return answer


def lie(basis, field):
    answer = apply(exterior_derivative, interior(basis, field))
    add_scaled(answer, apply(lambda term: interior(term, field),
                             exterior_derivative(basis)))
    return answer


def exponential(vector, field, sign=1):
    answer = Counter(vector)
    power = Counter(vector)
    for order in range(1, 20):
        power = apply(lambda term: lie(term, field), power)
        if not power:
            return answer
        add_scaled(answer, power, Q(sign ** order, factorial(order)))
    raise RuntimeError(("Lie series did not terminate", vector, field))


def root_homotopy(vector, field, sign=1):
    """i_(sign X) (exp(sign L_X)-1)/(sign L_X)."""
    answer = Counter()
    power = Counter(vector)
    for order in range(20):
        contracted = apply(lambda term: interior(term, field), power)
        add_scaled(answer, contracted,
                   Q(sign ** (order + 1), factorial(order + 1)))
        power = apply(lambda term: lie(term, field), power)
        if not power:
            return answer
    raise RuntimeError(("Cartan homotopy series did not terminate", vector,
                        field))


def compose(maps, vector):
    answer = Counter(vector)
    for linear_map in reversed(maps):
        answer = linear_map(answer)
    return answer


def signed_weyl_on_basis(basis):
    """Pullback of x -> -y, y -> x on monomial differential forms."""
    a, b, wedge = basis
    coefficient = (-1) ** a
    next_a, next_b = b, a
    transformed = []
    for index in wedge:
        if index == 0:  # dx -> -dy
            transformed.append(1)
            coefficient *= -1
        else:           # dy -> dx
            transformed.append(0)
    if len(transformed) == 2 and transformed[0] > transformed[1]:
        coefficient *= -1
    return Counter({(next_a, next_b, tuple(sorted(transformed))): coefficient})


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))

    x_map = lambda vector: exponential(vector, "E", 1)
    y_map = lambda vector: exponential(vector, "F", -1)
    h_x = lambda vector: root_homotopy(vector, "E", 1)
    h_y = lambda vector: root_homotopy(vector, "F", -1)

    def weyl(vector):
        return compose((x_map, y_map, x_map), vector)

    def weyl_homotopy(vector):
        # H_(x y x)=x y H_x + x H_y + H_x.
        answer = compose((x_map, y_map, h_x), vector)
        add_scaled(answer, compose((x_map, h_y), vector))
        add_scaled(answer, h_x(vector))
        return answer

    states = 0
    for degree in range(7):
        for a in range(degree + 1):
            b = degree - a
            for exterior_degree in range(3):
                for wedge in combinations(range(2), exterior_degree):
                    basis = (a, b, wedge)
                    vector = Counter({basis: Q(1)})
                    states += 1

                    for field, sign, root_map, root_h in (
                        ("E", 1, x_map, h_x),
                        ("F", -1, y_map, h_y),
                    ):
                        boundary = apply(exterior_derivative, root_h(vector))
                        add_scaled(boundary, root_h(
                            apply(exterior_derivative, vector)))
                        difference = root_map(vector)
                        add_scaled(difference, vector, -1)
                        require(boundary == difference,
                                ("root Cartan homotopy failed", basis,
                                 field, sign))

                    require(weyl(vector) == signed_weyl_on_basis(basis),
                            ("root factorization is not signed Weyl", basis))
                    boundary = apply(exterior_derivative,
                                     weyl_homotopy(vector))
                    add_scaled(boundary, weyl_homotopy(
                        apply(exterior_derivative, vector)))
                    difference = weyl(vector)
                    add_scaled(difference, vector, -1)
                    require(boundary == difference,
                            ("Weyl Cartan prism failed", basis))

    ledger = {
        "theorem": "explicit SL2 Weyl Cartan prism",
        "polynomial_degrees": [0, 6],
        "exterior_degrees": [0, 2],
        "basis_states": states,
        "weyl_factorization": "exp(L_E) exp(-L_F) exp(L_E)",
        "weyl_coordinate_action": ["x -> -y", "y -> x"],
        "homotopy": "x y H_x + x H_y + H_x",
        "identities": [
            "exp(+/-L)-1=dH+Hd",
            "w-id=dH_w+H_wd",
        ],
        "scope": (
            "universal Cartan/de Rham modules.  Descent of the root "
            "contractions to the physical labelled correction complex and "
            "their augmented terminal values remain unproved"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("SL2 Cartan prism ledger changed", digest))
    print("h3 SL2 Weyl Cartan prism: PASS")
    print("basis states:", states)
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    audit()
