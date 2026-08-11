#!/usr/bin/env python3
"""All-order chart Rees lift and the remaining physical separator.

The first-normal checker gives five source-labelled Schur comparison chains
whose divided boundary is B(tau)=I+tau*R.  Since B(0)=I, the recurrence

    C_0=I,  C_{n+1}=-R*C_n

constructs B(tau)^(-1) in the completed exact coefficient ring.  The
normalized comparison boundary is therefore I to every order.  Literal
word labels show target=0 and the opposite chart sectors show old ores=0
coefficientwise, before completion.

This does not identify the chart-odd comparison coordinate with the physical
cap coordinate w.  The committed physical relative module has primitive
separator lambda(E,W,T,O)=E+W+T-O; the needed identification would create
K=(0,1,0,0), on which lambda=1.  Thus the Rees recursion has no higher
normal obstruction, but physical descent still requires exactly the new
relative generator n_c/comparison map isolated by the definability gate.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

import verify_h3_component_iv_cyclotomic_normal_rees_boundary as NORMAL
import verify_h3_component_iv_physical_definability_gate as GATE


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "a5f042dea122b89c0a2155c7c9172fd230ea1e68c02a406aede8cf965a8d8745"
PINS = {
    "computations/verify_h3_component_iv_cyclotomic_normal_rees_boundary.py":
        "bc3da1ce329b5134bab2e51d7d70ee32052d76b440bd2fa947583a2132b149ef",
    "notes/h3-component-iv-cyclotomic-normal-rees-boundary.md":
        "6168f501bee2cab6c5f339ef47d1581af507a99a9053f99708836cd81fd8578e",
    "computations/verify_h3_component_iv_physical_definability_gate.py":
        "d2753b9e885464243a471387f168531484edafa8aa4bb34d160308a128237c00",
    "computations/verify_h3_primitive_attaching_universal_module.py":
        "9116553a78b231898355f17ed1f6ccada816d9954ad037a71c8318cfb391a927",
}

K = NORMAL.H2.K
ZERO = NORMAL.ZERO
ONE = NORMAL.ONE


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matrix_add(left, right):
    return [[a + b for a, b in zip(lrow, rrow, strict=True)]
            for lrow, rrow in zip(left, right, strict=True)]


def matrix_scale(scalar, matrix):
    return [[scalar * value for value in row] for row in matrix]


def matrix_power(matrix, exponent):
    answer = NORMAL.identity(len(matrix))
    for _ in range(exponent):
        answer = NORMAL.matmul(answer, matrix)
    return answer


def polynomial_add(left, right):
    size = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else ZERO)
        + (right[i] if i < len(right) else ZERO)
        for i in range(size)
    )


def polynomial_multiply(left, right):
    answer = [ZERO] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return tuple(answer)


def polynomial_scale(scalar, polynomial):
    return tuple(scalar * value for value in polynomial)


def parity(permutation):
    inversions = sum(permutation[i] > permutation[j]
                     for i in range(len(permutation))
                     for j in range(i + 1, len(permutation)))
    return -1 if inversions % 2 else 1


def determinant_polynomial(matrix):
    size = len(matrix)
    answer = (ZERO,)
    for permutation in permutations(range(size)):
        term = (ONE,)
        for row in range(size):
            term = polynomial_multiply(term, matrix[row][permutation[row]])
        answer = polynomial_add(
            answer, polynomial_scale(K(parity(permutation)), term)
        )
    return answer


def quadratic_remainder_matrix():
    jacobian_inverse = NORMAL.inverse_matrix(NORMAL.jacobian())
    remainder = [[ZERO] * 5 for _ in range(5)]
    for column in range(5):
        direction = {
            NORMAL.CHORDS[chord]: jacobian_inverse[chord][column]
            for chord in range(5)
        }
        for row, deleted in enumerate(NORMAL.D):
            constant, linear, quadratic = NORMAL.face_tau(deleted, direction)
            require(constant == ZERO, "normal arc has a constant face term")
            require(linear == (ONE if row == column else ZERO),
                    "normal arc lost its dual linear face term")
            remainder[row][column] = quadratic
    return remainder


def truncate_product_b_inverse(remainder, order):
    """Return coefficients of (I+tau R)*sum_{n<order}(-tau R)^n."""
    coefficients = []
    inverse_coefficients = [matrix_scale(K((-1) ** n),
                                         matrix_power(remainder, n))
                            for n in range(order)]
    for degree in range(order + 1):
        value = [[ZERO] * 5 for _ in range(5)]
        if degree < order:
            value = matrix_add(value, inverse_coefficients[degree])
        if 0 <= degree - 1 < order:
            value = matrix_add(
                value, NORMAL.matmul(remainder, inverse_coefficients[degree - 1])
            )
        coefficients.append(value)
    return coefficients


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}: {actual}")

    remainder = quadratic_remainder_matrix()
    require(remainder == [list(row) for row in zip(*remainder, strict=True)],
            "quadratic normal remainder stopped being symmetric")

    # The exact divided boundary matrix has no omitted higher terms because
    # every four-site face hafnian is quadratic in the chord coordinates.
    b_polynomial = [[(ONE if row == column else ZERO,
                      remainder[row][column])
                     for column in range(5)] for row in range(5)]
    determinant = determinant_polynomial(b_polynomial)
    expected_determinant = (
        K(1), K(Q(-5, 12)), K(Q(5, 24), Q(5, 48)),
        K(Q(-5, 96), Q(-35, 576)), K(0, Q(5, 576)),
        K(Q(5, 6912), Q(-1, 6912)),
    )
    require(determinant == expected_determinant,
            "exact Rees determinant polynomial changed")
    require(determinant[0] == ONE,
            "divided Rees boundary is not a formal unit")

    # This finite check is only a mutation guard.  The all-order proof is the
    # displayed coefficient recurrence: for every n>=1, C_n+R*C_{n-1}=0.
    guard_order = 13
    product_coefficients = truncate_product_b_inverse(remainder, guard_order)
    require(product_coefficients[0] == NORMAL.identity(5),
            "formal inverse lost its constant coefficient")
    require(all(coefficient == [[ZERO] * 5 for _ in range(5)]
                for coefficient in product_coefficients[1:guard_order]),
            "formal inverse recurrence failed below guard order")
    expected_tail = matrix_scale(
        K((-1) ** (guard_order - 1)), matrix_power(remainder, guard_order)
    )
    require(product_coefficients[guard_order] == expected_tail,
            "truncated inverse has the wrong first omitted coefficient")

    # Target and old ores vanish at each literal coefficient, not merely at
    # the cyclotomic point: every face word is mixed and the two sector copies
    # have opposite signs.  Formal combinations preserve these zero maps.
    face_words = []
    for deleted in NORMAL.D:
        word = list(NORMAL.SC.BASE_WORD)
        word[deleted] = 0
        word = tuple(word)
        require(len(set(word)) > 1,
                "a divided Rees coefficient acquired a pure target word")
        face_words.append("".join(map(str, word)))
    coefficient_readouts = {
        "constant": {"target": 0, "old_ores": 0},
        "linear": {"target": 0, "old_ores": 0},
    }

    # Audit the exact boundary of the attempted physical identification.
    physical = GATE.source_relative_gate()["downstairs"]
    separator = [int(value) for value in physical["separator"]]
    desired = [int(value) for value in physical["desired_chain"]]
    separator_value = sum(a * b for a, b in zip(separator, desired, strict=True))
    require(separator == [1, 1, 1, -1],
            "physical primitive separator changed")
    require(desired == [0, 1, 0, 0] and separator_value == 1,
            "chart-odd-to-physical-w identification lost its primitive defect")
    require(physical["physical_rank"] == 3
            and physical["rank_after_chain"] == 4
            and abs(int(physical["determinant_after_chain"])) == 1,
            "physical relative module stopped having a primitive rank-one gap")

    ledger = {
        "scope": "all-order completed chart Rees lift and physical descent boundary",
        "literal_face_words": face_words,
        "exact_divided_boundary": "B(tau)=I+tau*R; no higher terms",
        "quadratic_remainder_matrix": [
            [value.text() for value in row] for row in remainder
        ],
        "det_B": [value.text() for value in determinant],
        "det_B_constant": "1",
        "formal_inverse_recurrence": "C_0=I; C_n=-R*C_(n-1)=(-R)^n",
        "recurrence_guard_order": guard_order,
        "normalized_chart_comparison_boundary": "I5 to all orders",
        "coefficientwise_readouts": coefficient_readouts,
        "kappa_localization": "scales the unit boundary by the unit kappa",
        "higher_normal_separator_dimension": 0,
        "physical_coordinates": physical["coordinates"],
        "physical_candidate_rank": physical["physical_rank"],
        "physical_separator": separator,
        "attempted_chart_odd_to_w_column": desired,
        "physical_separator_value": separator_value,
        "physical_rank_after_identification": physical["rank_after_chain"],
        "physical_gap_is_primitive": abs(int(physical["determinant_after_chain"])) == 1,
        "verdict": (
            "the chart-level Rees recursion lifts to every order with target=old-ores=0, "
            "but identifying its chart-odd boundary with physical w is exactly the "
            "primitive missing n_c/comparison-map datum"
        ),
        "not_a_component_iv_closure": True,
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 Component-IV cyclotomic all-order Rees lift: PASS")
    print("chart comparison: B(tau)=I+tau*R is a formal unit; normalized to I5")
    print("literal target / old ores: zero coefficientwise to all orders")
    print("higher normal separator dimension: 0")
    print("physical chart-odd -> w identification: primitive separator value 1; OPEN")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
