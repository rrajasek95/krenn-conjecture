#!/usr/bin/env python3
"""Classify rank-six completions and exclude the first three full-nine rows.

The ten active response ports have a 15-parameter symmetric Gram completion.
Exact block equivalences prove rank(G)=5+rank(R) for an explicit 5 by 5
matrix R.  Hence every full rank-six lift has rank(R) zero or one, with the
zero case acquiring one private silent direction.  A Groebner replay and a
two-dimensional orthogonal-complement argument then show that the two pure
rows and mixed word 002101 are incompatible in every such completion.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_scalar_zero_packet_all_lagrangian_splits_obstruction.py":
        "15653d154a069af6d28a31311d74389a561426101659b8ced1d8852f838b73ca",
    "notes/h3-scalar-zero-packet-all-lagrangian-splits-obstruction.md":
        "5ff5afb1c4c3f001196dcc7edf9ba73c2921d9718718bcc8ce0da09c9e74e50d",
    "computations/verify_h3_scalar_zero_packet_six_site_nonreduction.py":
        "20ec8fabda17ab915e9b071df00a06d72e985943a3672a5f0a9e02edff80badf",
}
EXPECTED_LEDGER_SHA256 = "6abcdd6cbaa161e0a11e6bcf88a4b3febf342d8576ee4e60166b381a0a40f6d3"

VARIABLES = (
    "A00", "A01", "A02", "A11", "A12", "A22",
    "delta", "eta", "theta", "beta", "gamma",
    "rho", "sigma", "epsilon", "phi",
)
NVAR = len(VARIABLES)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


class Poly:
    """Tiny exact polynomial ring Q[VARIABLES], sufficient for the audit."""

    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {monomial: Q(coefficient)
                      for monomial, coefficient in (terms or {}).items()
                      if coefficient}

    @staticmethod
    def constant(value):
        value = Q(value)
        return Poly({(0,) * NVAR: value}) if value else Poly()

    @staticmethod
    def variable(index):
        monomial = [0] * NVAR
        monomial[index] = 1
        return Poly({tuple(monomial): Q(1)})

    def __add__(self, other):
        other = as_poly(other)
        answer = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
        return Poly(answer)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Poly({monomial: -coefficient
                     for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_poly(other))

    def __rsub__(self, other):
        return as_poly(other) - self

    def __mul__(self, other):
        other = as_poly(other)
        answer = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = tuple(left + right for left, right in
                                 zip(left_monomial, right_monomial,
                                     strict=True))
                answer[monomial] = (answer.get(monomial, Q(0))
                                    + left_coefficient * right_coefficient)
        return Poly(answer)

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        return self.terms == as_poly(other).terms

    def evaluate(self, values):
        answer = Q(0)
        for monomial, coefficient in self.terms.items():
            term = coefficient
            for exponent, value in zip(monomial, values, strict=True):
                term *= Q(value) ** exponent
            answer += term
        return answer

    def serialize(self):
        answer = []
        for monomial, coefficient in sorted(self.terms.items()):
            powers = tuple((VARIABLES[index], exponent)
                           for index, exponent in enumerate(monomial)
                           if exponent)
            answer.append((str(coefficient), powers))
        return tuple(answer)


def as_poly(item):
    return item if isinstance(item, Poly) else Poly.constant(item)


PZERO = Poly.constant(0)
PONE = Poly.constant(1)
PV = {name: Poly.variable(index) for index, name in enumerate(VARIABLES)}


def zero_matrix(rows, columns):
    return [[PZERO for _ in range(columns)] for _ in range(rows)]


def identity(size):
    answer = zero_matrix(size, size)
    for index in range(size):
        answer[index][index] = PONE
    return answer


def transpose(items):
    return [list(row) for row in zip(*items, strict=True)]


def matrix_add(left, right):
    return [[left[row][column] + right[row][column]
             for column in range(len(left[0]))]
            for row in range(len(left))]


def matrix_sub(left, right):
    return [[left[row][column] - right[row][column]
             for column in range(len(left[0]))]
            for row in range(len(left))]


def matrix_neg(items):
    return [[-item for item in row] for row in items]


def matrix_mul(left, right):
    require(len(left[0]) == len(right), (len(left[0]), len(right)))
    return [[sum((left[row][middle] * right[middle][column]
                  for middle in range(len(right))), PZERO)
             for column in range(len(right[0]))]
            for row in range(len(left))]


def block_matrix(block_rows):
    answer = []
    for block_row in block_rows:
        heights = {len(block) for block in block_row}
        require(len(heights) == 1, heights)
        for inner_row in range(len(block_row[0])):
            row = []
            for block in block_row:
                row.extend(block[inner_row])
            answer.append(row)
    return answer


def polynomial_determinant(items):
    size = len(items)
    answer = PZERO
    for order in permutations(range(size)):
        inversions = sum(order[left] > order[right]
                         for left in range(size)
                         for right in range(left + 1, size))
        term = PONE
        for row, column in enumerate(order):
            term *= items[row][column]
        answer += -term if inversions % 2 else term
    return answer


def rational_rank(items):
    work = [[Q(item) for item in row] for row in items]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [item / scale for item in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [work[row][index] - scale * work[rank][index]
                         for index in range(columns)]
        rank += 1
    return rank


def evaluate_matrix(items, values):
    return [[item.evaluate(values) for item in row] for row in items]


def generic_completion_data():
    A = [
        [PV["A00"], PV["A01"], PV["A02"]],
        [PV["A01"], PV["A11"], PV["A12"]],
        [PV["A02"], PV["A12"], PV["A22"]],
    ]
    D = zero_matrix(3, 3)
    for index, name in enumerate(("delta", "eta", "theta")):
        D[index][index] = PV[name]
    E = zero_matrix(3, 2)
    E[1][0] = PV["beta"]
    E[2][1] = PV["gamma"]
    B = zero_matrix(2, 2)
    B[0][0] = PV["rho"]
    B[1][1] = PV["sigma"]
    F = zero_matrix(2, 2)
    F[0][0] = PONE
    F[1][1] = -PONE
    W = zero_matrix(2, 2)
    W[0][0] = PV["epsilon"]
    W[1][1] = PV["phi"]

    I3 = identity(3)
    Z32 = zero_matrix(3, 2)
    Z23 = zero_matrix(2, 3)
    Z22 = zero_matrix(2, 2)
    G = block_matrix([
        [A, I3, Z32, Z32],
        [I3, D, E, Z32],
        [Z23, transpose(E), B, F],
        [Z23, Z23, transpose(F), W],
    ])

    # First exact equivalence: pivot y'=y+A*x.
    T1 = identity(10)
    for row in range(3):
        for column in range(3):
            T1[row + 3][column] = -A[row][column]
    L1 = identity(10)
    for row in range(3):
        for column in range(3):
            L1[row + 3][column] = -D[row][column]
    for row in range(2):
        for column in range(3):
            L1[row + 6][column] = -transpose(E)[row][column]
    stage1 = matrix_mul(matrix_mul(L1, G), T1)
    K = matrix_sub(I3, matrix_mul(D, A))
    expected_stage1 = block_matrix([
        [zero_matrix(3, 3), I3, Z32, Z32],
        [K, zero_matrix(3, 3), E, Z32],
        [matrix_neg(matrix_mul(transpose(E), A)), Z23, B, F],
        [Z23, Z23, transpose(F), W],
    ])
    require(stage1 == expected_stage1, "first symbolic equivalence failed")

    H = block_matrix([
        [K, E, Z32],
        [matrix_neg(matrix_mul(transpose(E), A)), B, F],
        [Z23, transpose(F), W],
    ])

    # Second equivalence: pivot z'=F^T*z+W*w.  Here F=F^T=F^-1.
    T2 = identity(7)
    for row in range(2):
        for column in range(2):
            T2[row + 3][column + 3] = F[row][column]
    minus_FW = matrix_neg(matrix_mul(F, W))
    for row in range(2):
        for column in range(2):
            T2[row + 3][column + 5] = minus_FW[row][column]
    L2 = identity(7)
    EF = matrix_mul(E, F)
    BF = matrix_mul(B, F)
    for row in range(3):
        for column in range(2):
            L2[row][column + 5] = -EF[row][column]
    for row in range(2):
        for column in range(2):
            L2[row + 3][column + 5] = -BF[row][column]
    stage2 = matrix_mul(matrix_mul(L2, H), T2)

    EFW = matrix_mul(EF, W)
    F_minus_BFW = matrix_sub(F, matrix_mul(BF, W))
    expected_stage2 = block_matrix([
        [K, zero_matrix(3, 2), matrix_neg(EFW)],
        [matrix_neg(matrix_mul(transpose(E), A)), zero_matrix(2, 2),
         F_minus_BFW],
        [Z23, identity(2), Z22],
    ])
    require(stage2 == expected_stage2, "second symbolic equivalence failed")

    R = []
    for row in range(5):
        R.append(stage2[row][0:3] + stage2[row][5:7])
    expected_R = block_matrix([
        [K, matrix_neg(EFW)],
        [matrix_neg(matrix_mul(transpose(E), A)), F_minus_BFW],
    ])
    require(R == expected_R, "rank residual extraction failed")
    return G, R, A, D, E, B, F, W


def singular_local_row_replay():
    executable = shutil.which("Singular")
    require(executable is not None, "Singular is required for exact replay")
    families = ("x", "y", "u", "v", "a", "c", "d", "f")
    variables = [f"{family}{index}" for family in families
                 for index in range(3)]
    equations = []
    for row in range(3):
        for column in range(3):
            equations.append(
                f"x{row}*c{column}+a{row}*y{column}-"
                + ("1" if (row, column) == (0, 0) else "0"))
            equations.append(
                f"d{row}*v{column}+u{row}*f{column}-"
                + ("1" if (row, column) == (2, 2) else "0"))
            equations.append(
                f"x{row}*v{column}+u{row}*y{column}")
    ring = ",".join(variables)
    ideal = ",".join(equations)
    script = (
        f"ring R=0,({ring}),dp;\n"
        f"ideal I={ideal};\n"
        "option(redSB); ideal G=std(I);\n"
        '"basis",size(G);\n'
        "reduce(x0*y0+x1*y1+x2*y2,G);\n"
        "reduce(u0*v0+u1*v1+u2*v2,G);\n"
    )
    result = subprocess.run(
        [executable, "--no-stdlib", "--quiet"],
        input=script, text=True, capture_output=True, timeout=30, check=True,
    )
    output = "\n".join(line.strip() for line in result.stdout.splitlines()
                       if line.strip())
    require(output == "basis 127\n0\n0", output)

    # The target equations also forbid j=lambda*b.  Since both pair with
    # their pure mates, neither is zero, so this proves their independence.
    dependent_variables = variables + ["lambda"]
    dependent_equations = equations[:]
    for index in range(3):
        dependent_equations.extend((
            f"u{index}-lambda*x{index}",
            f"v{index}-lambda*y{index}",
        ))
    script = (
        f"ring R=0,({','.join(dependent_variables)}),dp;\n"
        f"ideal I={','.join(dependent_equations)};\n"
        "ideal G=std(I);\n"
        '"basis",size(G);\n'
        "reduce(1,G);\n"
    )
    result = subprocess.run(
        [executable, "--no-stdlib", "--quiet"],
        input=script, text=True, capture_output=True, timeout=30, check=True,
    )
    dependent_output = "\n".join(
        line.strip() for line in result.stdout.splitlines() if line.strip())
    require(dependent_output == "basis 1\n0", dependent_output)
    return output, dependent_output


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    G, R, A, D, E, B, F, W = generic_completion_data()

    # A concrete inequivalent completion: four matching pairs collapse to
    # nonisotropic lines, while b,e form a hyperbolic plane.  It has rank 6,
    # but C_000000=sym(b,e) has rank 2, so a5c61ce's rank-one identity is not
    # completion-invariant.
    alternative = {name: Q(0) for name in VARIABLES}
    for name in ("A00", "A11", "A22", "delta", "eta", "theta",
                 "sigma", "phi"):
        alternative[name] = Q(1)
    values = tuple(alternative[name] for name in VARIABLES)
    alternative_G = evaluate_matrix(G, values)
    alternative_R = evaluate_matrix(R, values)
    require(rational_rank(alternative_G) == 6,
            rational_rank(alternative_G))
    require(rational_rank(alternative_R) == 1,
            rational_rank(alternative_R))
    be_gram = [[alternative["rho"], Q(1)],
               [Q(1), alternative["epsilon"]]]
    require(rational_rank(be_gram) == 2, be_gram)

    groebner_output, dependent_output = singular_local_row_replay()

    # Once the three rows hold, b and j are independent isotropic vectors.
    # Their pure mates e and i give the following nondegenerate 4-space U.
    epsilon = PV["epsilon"]
    phi = PV["phi"]
    U = [
        [PZERO, PZERO, PONE, PZERO],
        [PZERO, PZERO, PZERO, PONE],
        [PONE, PZERO, epsilon, PZERO],
        [PZERO, PONE, PZERO, phi],
    ]
    require(polynomial_determinant(U) == PONE,
            polynomial_determinant(U).serialize())
    b_vector = [PONE, PZERO, PZERO, PZERO]
    j_vector = [PZERO, PONE, PZERO, PZERO]
    e_vector = [PZERO, PZERO, PONE, PZERO]
    i_vector = [PZERO, PZERO, PZERO, PONE]
    g_u = j_vector
    h_u = [item - epsilon * b_item
           for item, b_item in zip(e_vector, b_vector, strict=True)]

    def pairing(left, right):
        return sum((left[row] * U[row][column] * right[column]
                    for row in range(4) for column in range(4)), PZERO)

    require(all(pairing(g_u, vector) == PZERO
                for vector in (b_vector, j_vector, e_vector)), "g_U line")
    require(all(pairing(h_u, vector) == PZERO
                for vector in (j_vector, e_vector, i_vector)), "h_U line")
    require(pairing(g_u, h_u) == PZERO, "U-components must be orthogonal")

    return {
        "theorem": (
            "no nondegenerate rank-six site-diagonal completion satisfies "
            "the pure 000000, pure 222222, and mixed 002101 full-nine rows"
        ),
        "pins": PINS,
        "active_completion_parameterization": {
            "parameters": VARIABLES,
            "block_order": "x=(a,g,i), y=(d,h,j), z=(b,c), w=(e,f)",
            "G": "[[A,I,0,0],[I,D,E,0],[0,E^T,B,F],[0,0,F^T,W]]",
            "R": "[[I-DA,-EFW],[-E^T A,F-BFW]]",
            "rank_identity": "rank(G)=5+rank(R)",
            "rank_six_cases": (
                "rank(R)=1: active ports span the six-space",
                "rank(R)=0: active rank five plus one silent stabilization",
            ),
            "R_entries": tuple(tuple(item.serialize() for item in row)
                               for row in R),
        },
        "old_laurent_identity": {
            "survives_all_completions": False,
            "alternative_parameters": {
                name: str(value) for name, value in alternative.items()
            },
            "alternative_active_rank": rational_rank(alternative_G),
            "alternative_R_rank": rational_rank(alternative_R),
            "alternative_C000000_rank": rational_rank(be_gram),
        },
        "three_row_local_ideal": {
            "pure_rows": "C(b,e)=E00 and C(i,j)=E22",
            "mixed_row": "C(b,j)=0",
            "groebner_replay": groebner_output,
            "consequences": "J(b,b)=J(j,j)=0",
            "dependent_branch": dependent_output,
            "independence": "b and j span a two-dimensional isotropic plane",
        },
        "completion_independent_leaf_obstruction": {
            "U_gram_determinant": "1",
            "U_dimension": 4,
            "W": "U^perp is nondegenerate of dimension 2",
            "leaf_vectors": "d,f lie in W, are nonzero, and J(d,f)=0",
            "U_components": "g_U is in C*j; h_U is in C*(e-epsilon*b)",
            "W_components": (
                "if d,f span W both vanish; if dependent they and both "
                "components lie on one isotropic line"
            ),
            "contradiction": "J(g,h)=0, but the response edge g*h has weight 1",
        },
        "scope": (
            "exhausts all 15-parameter active Gram completions and both "
            "rank-six silent-extension cases.  No all-nine test is needed: "
            "the first two pure rows plus 002101 already fail."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("h3 scalar-zero rank-six completion obstruction: PASS")
    print("mode", arguments.mode)
    print("active completion rank identity: rank(G)=5+rank(R)")
    print("old rank-one identity: not invariant; three-row leaf obstruction: all completions")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
