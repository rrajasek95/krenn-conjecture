#!/usr/bin/env python3
"""Realize the balanced C4 charge as two hyperbolic root returns.

This is a formal operation-space construction, not yet a physical source
attachment.  Put x=(D,p0,p1), y=(q01,s1,s0), and let

    S = (x0*y0+x1*y1+x2*y2)*H.

The infinitesimal GL3 action

    E_ij = x_i d/dx_j - y_j d/dy_i

annihilates S.  Two opposite-root returns on the direct chart x0*y0*H
produce x0*y0*H-xj*yj*H.  Their sum is exactly the Gate-II charge
2A-B-C.  The first faces are the collision monomials x_i*y_j*H, which
are independent of the three squarefree chart monomials.  Thus this gives
an exact candidate two-stage construction while locating its first missing
physical cells.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_balanced_chart_square_master_obstruction.py":
        "306980dc569795fa3ec2c8e6fdbdf2b67fa5d85cd75ebebe62be7db15b1e1a59",
    "notes/uniform-balanced-chart-square-master-obstruction.md":
        "c758fb43f88d9c02f5200921c6c50637bfe04402536edc3e947f74d108fbd93b",
    "computations/verify_uniform_chart_unipotent_shear_collision_gate.py":
        "6f05b788400279a8dd19c09acbb1e883eb74c8a9c21f9d00e2bc6a048543922e",
    "notes/uniform-chart-unipotent-shear-collision-gate.md":
        "7fe9e709dd414c101fb1178dc2dee5f5b1d98db0192a525c48cde1e5cfba5a63",
}
EXPECTED_LEDGER_SHA256 = (
    "0616507f6bbe943e89f24db376d716c25b82cdd76caef506d68b596a358c1370"
)

# Monomials are exponent tuples in x0,x1,x2,y0,y1,y2,H.
Monomial = tuple[int, int, int, int, int, int, int]
Polynomial = dict[Monomial, Q]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(*polys: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
    return clean(answer)


def scale(coefficient: int | Q, poly: Polynomial) -> Polynomial:
    return clean({monomial: Q(coefficient) * value
                  for monomial, value in poly.items()})


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm, strict=True))
            answer[monomial] = answer.get(monomial, Q(0)) + lc * rc
    return clean(answer)


def derivative(poly: Polynomial, variable: int) -> Polynomial:
    answer: Polynomial = {}
    for monomial, coefficient in poly.items():
        exponent = monomial[variable]
        if not exponent:
            continue
        out = list(monomial)
        out[variable] -= 1
        key = tuple(out)
        answer[key] = answer.get(key, Q(0)) + coefficient * exponent
    return clean(answer)


def variable(index: int) -> Polynomial:
    monomial = [0] * 7
    monomial[index] = 1
    return {tuple(monomial): Q(1)}


X = tuple(variable(index) for index in range(3))
Y = tuple(variable(index) for index in range(3, 6))
H = variable(6)


def root(i: int, j: int, poly: Polynomial) -> Polynomial:
    """E_ij=x_i*d_xj-y_j*d_yi for the hyperbolic GL3 action."""
    require(i != j and 0 <= i < 3 and 0 <= j < 3, (i, j))
    x_part = multiply(X[i], derivative(poly, j))
    y_part = multiply(Y[j], derivative(poly, 3 + i))
    return add(x_part, scale(-1, y_part))


def rank(polys: tuple[Polynomial, ...]) -> int:
    monomials = sorted({monomial for poly in polys for monomial in poly})
    rows = [[poly.get(monomial, Q(0)) for poly in polys]
            for monomial in monomials]
    answer = 0
    width = len(polys)
    for column in range(width):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [a - value * b for a, b in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()

    charts = tuple(multiply(multiply(X[index], Y[index]), H)
                   for index in range(3))
    complete = add(*charts)
    balanced = add(scale(2, charts[0]), scale(-1, charts[1]),
                   scale(-1, charts[2]))

    # Every root is an exact infinitesimal symmetry of the local hyperbolic
    # response.  This is stronger than cancellation only after projection.
    for i in range(3):
        for j in range(3):
            if i != j:
                require(root(i, j, complete) == {},
                        ("root stopped preserving complete response", i, j))

    first_faces: list[Polynomial] = []
    returns: list[Polynomial] = []
    reverse_returns: list[Polynomial] = []
    for j in (1, 2):
        first = root(0, j, charts[0])
        expected_first = scale(-1, multiply(multiply(X[0], Y[j]), H))
        require(first == expected_first, ("first collision changed", j))
        first_faces.append(first)

        returned = root(j, 0, first)
        expected_return = add(charts[0], scale(-1, charts[j]))
        require(returned == expected_return,
                ("opposite-root return changed", j))
        returns.append(returned)

        reverse_first = root(j, 0, charts[0])
        reverse_return = root(0, j, reverse_first)
        require(reverse_return == expected_return,
                ("reverse root path stopped agreeing", j))
        reverse_returns.append(reverse_return)

    require(add(*returns) == balanced,
            "two root returns stopped producing the balanced charge")

    # The three chart monomials and all six oriented collision monomials are
    # distinct fine/multidegrees.  No old chart combination supplies a first
    # collision face.
    all_collisions = tuple(
        multiply(multiply(X[i], Y[j]), H)
        for i in range(3) for j in range(3) if i != j
    )
    require(rank(charts) == 3, "chart rank changed")
    require(rank(charts + all_collisions) == 9,
            "collision faces stopped being independent of chart faces")

    # Diagonal hyperbolic generators x_i*d_xi-y_i*d_yi fix each A_i, so a
    # Cartan-only construction cannot create the balanced charge.
    for i in range(3):
        diagonal = add(multiply(X[i], derivative(charts[i], i)),
                       scale(-1, multiply(Y[i], derivative(charts[i], 3 + i))))
        require(diagonal == {}, ("diagonal action changed", i))

    ledger = {
        "theorem": "balanced C4 charge is a two-opposite-root return",
        "pins": PINS,
        "operation_coordinates": {
            "x": ["D", "p0", "p1"],
            "y": ["q01", "s1", "s0"],
            "charts": ["D*q01*H", "p0*s1*H", "p1*s0*H"],
        },
        "complete_response": "(D*q01+p0*s1+p1*s0)*H",
        "balanced_output": "(2*D*q01-p0*s1-p1*s0)*H",
        "root_formula": "E_ij=x_i*d_xj-y_j*d_yi",
        "all_six_roots_preserve_complete_response": True,
        "two_returns": ["A-B", "A-C"],
        "return_sum": "2A-B-C",
        "first_collision_faces": ["-D*s1*H", "-D*s0*H"],
        "reverse_collision_faces": ["p0*q01*H", "p1*q01*H"],
        "chart_rank": rank(charts),
        "chart_plus_collision_rank": rank(charts + all_collisions),
        "physical_scope": (
            "the operation-space GL3 action mixes D/P and Q/S roles.  Its "
            "collision monomials have missing/doubled augmented-vertex "
            "degree and are not existing squarefree source columns.  A "
            "physical proof must totalize both opposite-root squares with "
            "their collision, word/fine/repeated, q, anchor, W, residue and "
            "ridge faces; the identities here do not supply that chain map"
        ),
        "positive_attack": (
            "construct the two collision Tate families for roots 0<->1 and "
            "0<->2; their root returns automatically give exactly the two "
            "profile-changing families proved necessary for the balanced "
            "Gate-II filler"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("complete local response: preserved by all six hyperbolic roots")
    print("opposite-root returns: A-B and A-C; sum = 2A-B-C")
    print("first missing physical faces: four operation-collision monomials")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
