#!/usr/bin/env python3
"""Audit the universal dark-annihilator plane and its singular-cap export.

The full-nine equations imply, for every cap matrix M,

    sigma(M) q^[3] + r(M) q^[2] = sum_i M_ii X_i.

Consequently every off-diagonal M orthogonal to the direct block is dark.
This is a space of dimension at least five and contains three independent
rank-one row-supported directions.  Thus the bare rank<=2 dark-annihilator
input is universal, not an exceptional source-minimal event.

There is nevertheless a positive projective reduction.  Starting with an
invertible scalar-zero K_* whose three diagonal readouts are nonzero, the
whole dark plane preserves sigma, the diagonal readouts, and the contracted
response.  A trace-pairing dimension argument supplies M for which
K_*^{-1}M is not nilpotent; hence det(K_*+tM) is nonconstant and has a
nonzero complex root.  The root is a literal singular, at-most-two-channel
cap with the same contracted ternary packet.

The checker also gives a literal common-q first-derivative guard showing why
z q^[2]=0 is not by itself an occupied-cell/source deformation.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_k1_overlap_sharedline_rankdrop.py":
        "723c0c69c3c1bbe48df1f658e093280a3edbcfe0d14f02bdea5149a31037f500",
    "notes/h3-k1-overlap-sharedline-rankdrop.md":
        "3e7397e5abf8c544f483b85bf039ee8b537ecaaa049722ec0b651aa17dd5880f",
    "computations/verify_h3_rank_deficient_latent_fullnine_boundary.py":
        "ae178897f9de221bd262c1d0de4277e945976c5e6b43f71c69e009f330b92d20",
    "notes/h3-rank-deficient-latent-fullnine-boundary.md":
        "8d8dd990b432306bba634b3529577aab7072ed5c4aaf73d7f0f894e2a1963e59",
    "computations/verify_h3_scalar_zero_packet_six_site_nonreduction.py":
        "20ec8fabda17ab915e9b071df00a06d72e985943a3672a5f0a9e02edff80badf",
    "notes/h3-scalar-zero-packet-six-site-nonreduction.md":
        "22404c6a55c8c6a60cd3186eef3401212a60a4b6fcdc0cde5077fbab6892ff08",
}

COLOURS = tuple(range(3))
OFFDIAGONAL = tuple((i, j) for i in COLOURS for j in COLOURS if i != j)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return work, ()
    rows, columns = len(work), len(work[0])
    pivots = []
    current = 0
    for column in range(columns):
        pivot = next((row for row in range(current, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[current], work[pivot] = work[pivot], work[current]
        scale = work[current][column]
        work[current] = [entry / scale for entry in work[current]]
        for row in range(rows):
            if row == current or not work[row][column]:
                continue
            scalar = work[row][column]
            work[row] = [entry - scalar * base
                         for entry, base in
                         zip(work[row], work[current], strict=True)]
        pivots.append(column)
        current += 1
        if current == rows:
            break
    return work, tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def matmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))]
            for i in range(len(left))]


def identity(size):
    return [[Q(int(i == j)) for j in range(size)] for i in range(size)]


def add_scaled(left, scalar, right):
    return [[left[i][j] + scalar * right[i][j] for j in range(3)]
            for i in range(3)]


def determinant(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
                        - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                          - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                          - matrix[1][1] * matrix[2][0])
    )


def pairing(matrix, direct):
    return sum(matrix[i][j] * direct[i][j]
               for i, j in product(COLOURS, repeat=2))


def polynomial_add(left, right):
    size = max(len(left), len(right))
    return tuple((left[index] if index < len(left) else Q(0))
                 + (right[index] if index < len(right) else Q(0))
                 for index in range(size))


def polynomial_multiply(left, right):
    answer = [Q(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    return tuple(answer)


def determinant_pencil(base, direction):
    # Leibniz determinant over Q[t].
    answer = (Q(0),)
    for permutation in ((0, 1, 2), (0, 2, 1), (1, 0, 2),
                        (1, 2, 0), (2, 0, 1), (2, 1, 0)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(3) for j in range(i + 1, 3))
        term = (Q(1),)
        for row, column in enumerate(permutation):
            term = polynomial_multiply(
                term, (base[row][column], direction[row][column]))
        if inversions % 2:
            term = tuple(-coefficient for coefficient in term)
        answer = polynomial_add(answer, term)
    while len(answer) > 1 and answer[-1] == 0:
        answer = answer[:-1]
    return answer


def row_rank_one_witness(direct, row, modulus=None):
    columns = tuple(column for column in COLOURS if column != row)
    first, second = direct[row][columns[0]], direct[row][columns[1]]
    if modulus is None:
        coefficients = ((second, -first) if first or second
                        else (Q(1), Q(0)))
    else:
        if first % modulus or second % modulus:
            coefficients = (second % modulus, (-first) % modulus)
        else:
            coefficients = (1, 0)
    matrix = [[0] * 3 for _ in range(3)]
    matrix[row][columns[0]] = coefficients[0]
    matrix[row][columns[1]] = coefficients[1]
    return matrix


def finite_field_dark_plane_census(prime=3):
    vectors = tuple(product(range(prime), repeat=len(OFFDIAGONAL)))
    dimension_histogram = Counter()
    dark_vector_pairs = 0
    row_witnesses = 0
    for direct_vector in vectors:
        direct = [[0] * 3 for _ in range(3)]
        for (i, j), value in zip(OFFDIAGONAL, direct_vector, strict=True):
            direct[i][j] = value
        functional_rank = int(any(direct_vector))
        dimension = 6 - functional_rank
        dimension_histogram[dimension] += 1
        dark = sum(
            int(sum(m * a for m, a in
                    zip(matrix_vector, direct_vector, strict=True)) % prime == 0)
            for matrix_vector in vectors
        )
        require(dark == prime ** dimension,
                ("dark-plane dimension changed", direct_vector, dark, dimension))
        dark_vector_pairs += dark
        for row in COLOURS:
            witness = row_rank_one_witness(direct, row, prime)
            require(any(witness[row]), (direct_vector, row, witness))
            require(sum(witness[i][j] * direct[i][j]
                        for i, j in OFFDIAGONAL) % prime == 0,
                    ("row witness is not direct-dark", direct_vector, row))
            # A nonzero one-row matrix has rank exactly one.
            require(sum(any(witness[i][j] for j in COLOURS)
                        for i in COLOURS) == 1,
                    ("row witness lost rank-one support", direct_vector, row))
            row_witnesses += 1
    require(dimension_histogram == Counter({5: 728, 6: 1}),
            dimension_histogram)
    require(dark_vector_pairs == 177633, dark_vector_pairs)
    require(row_witnesses == 2187, row_witnesses)
    return {
        "field": "F_3",
        "direct_offdiagonal_blocks": len(vectors),
        "dark_dimension_histogram": dict(sorted(dimension_histogram.items())),
        "dark_vector_pairs": dark_vector_pairs,
        "rank_one_row_witnesses": row_witnesses,
    }


def trace_pairing_and_pencil_fixture():
    # Gram(E_ij,E_kl)=tr(E_ij E_kl)=delta_jk delta_il is nondegenerate.
    basis = tuple((i, j) for i, j in product(COLOURS, repeat=2))
    gram = [[Q(int(j == k and i == ell)) for k, ell in basis]
            for i, j in basis]
    require(rank(gram) == 9, "the trace pairing is degenerate")
    require(2 * 5 > 9,
            "a five-plane could be totally isotropic for the trace pairing")

    direct = [[Q(0)] * 3 for _ in range(3)]
    direct[0][1] = Q(1)
    k_star = identity(3)
    require(pairing(k_star, direct) == 0, "K_* is not scalar-zero")

    # Nonnilpotent dark rank-two direction: M=E_02+E_20.
    moving = [[Q(0), Q(0), Q(1)],
              [Q(0), Q(0), Q(0)],
              [Q(1), Q(0), Q(0)]]
    require(rank(moving) == 2 and pairing(moving, direct) == 0,
            "the moving cap is not rank-two dark")
    require(tuple(moving[i][i] for i in COLOURS) == (Q(0),) * 3,
            "the moving cap changed a diagonal readout")
    pencil = determinant_pencil(k_star, moving)
    require(pencil == (Q(1), Q(0), Q(-1)), pencil)
    singular = add_scaled(k_star, Q(1), moving)
    require(determinant(singular) == 0 and rank(singular) == 2,
            ("the displayed pencil root is not rank two", singular))
    require(tuple(singular[i][i] for i in COLOURS) == (Q(1),) * 3,
            "the singular cap lost a pure diagonal readout")
    require(pairing(singular, direct) == 0,
            "the singular cap is not scalar-zero")

    # A particular direction can lie in the constant-determinant branch.
    # Here N=E_10 is nonzero square-zero, so det(I+tN)=1.
    nilpotent = [[Q(0), Q(0), Q(0)],
                 [Q(1), Q(0), Q(0)],
                 [Q(0), Q(0), Q(0)]]
    require(pairing(nilpotent, direct) == 0, "nilpotent guard is not dark")
    require(not any(any(entry for entry in row)
                    for row in matmul(nilpotent, nilpotent)),
            "the nilpotent guard is not square-zero")
    require(determinant_pencil(k_star, nilpotent) == (Q(1),),
            "the nilpotent pencil determinant is not constant")

    return {
        "trace_pairing_rank": rank(gram),
        "dark_plane_minimum_dimension": 5,
        "maximum_totally_isotropic_dimension": 4,
        "nonnilpotent_fixture": {
            "M": tuple(tuple(map(str, row)) for row in moving),
            "rank_M": rank(moving),
            "det_K_plus_tM": tuple(map(str, pencil)),
            "root": "1",
            "rank_at_root": rank(singular),
            "diagonal_at_root": tuple(str(singular[i][i]) for i in COLOURS),
        },
        "nilpotent_fixture": {
            "M": tuple(tuple(map(str, row)) for row in nilpotent),
            "M_squared": "0",
            "det_K_plus_tM": ("1",),
        },
    }


def polynomial_product(left, right):
    answer = Counter()
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            answer[left_mask | right_mask] += left_value * right_value
    return {mask: value for mask, value in answer.items() if value}


def divided_edge_power(edges, degree):
    answer = Counter()
    edge_terms = tuple(edges.items())
    for selected in combinations(edge_terms, degree):
        occupied = 0
        coefficient = Q(1)
        for edge_mask, value in selected:
            if occupied & edge_mask:
                break
            occupied |= edge_mask
            coefficient *= value
        else:
            answer[occupied] += coefficient
    return {mask: value for mask, value in answer.items() if value}


def edge_mask(left, right):
    return (1 << left) | (1 << right)


def common_q_first_derivative_guard():
    # The six-cycle has two perfect matchings.  The chord z=02 has no
    # two-q-edge completion, but after the endpoint response ps=15 is added,
    # the remaining q-edge 34 completes a nonzero first derivative row.
    cycle = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5))
    q = {edge_mask(*edge): Q(1) for edge in cycle}
    q2 = divided_edge_power(q, 2)
    q3 = divided_edge_power(q, 3)
    z = {edge_mask(0, 2): Q(1)}
    ps = {edge_mask(1, 5): Q(1)}
    require(q3 == {(1 << 6) - 1: Q(2)}, ("six-cycle cube changed", q3))
    require(polynomial_product(z, q2) == {}, "z*q^[2] is not zero")
    full_derivative = polynomial_product(ps, polynomial_product(z, q))
    require(full_derivative == {(1 << 6) - 1: Q(1)},
            ("the uncontracted first derivative vanished", full_derivative))

    damaged = {edge_mask(0, 3): Q(1)}
    require(polynomial_product(damaged, q2) == {(1 << 6) - 1: Q(1)},
            "the chord mutation did not expose its q^[2] completion")
    return {
        "sites": 6,
        "q_support": tuple("%d%d" % edge for edge in cycle),
        "q^[3]_full_coefficient": str(q3[(1 << 6) - 1]),
        "z": "02",
        "p*s": "15",
        "z*q^[2]": "0",
        "p*s*z*q_full_coefficient": str(
            full_derivative[(1 << 6) - 1]),
        "scope": (
            "literal common-q square-free guard to the tangent/deletion "
            "implication; it does not satisfy the ternary full-nine rows"
        ),
    }


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    return {
        "theorem": "universal dark plane and singular-cap export",
        "pins": PINS,
        "full_nine_contraction": (
            "sigma(M)q^[3]+r(M)q^[2]=sum_i M_ii X_i"
        ),
        "universal_dark_plane": {
            "definition": "D_a={M:diag(M)=0 and <M,a>=0}",
            "dimension": "dim D_a>=5",
            "rank_one_supply": (
                "each of the three fixed physical rows contains a nonzero "
                "row-supported rank-one M in D_a"
            ),
            "consequence": "M in D_a implies r(M)q^[2]=0",
            "finite_field_mutation_guard": finite_field_dark_plane_census(),
        },
        "singular_cap_export": {
            "hypotheses": (
                "K_* invertible, sigma(K_*)=0, and all diag(K_*) nonzero"
            ),
            "trace_argument": (
                "K_*^{-1}D_a is a >=5-plane; if every member were nilpotent "
                "it would be totally isotropic for nondegenerate tr(XY), "
                "but a totally isotropic subspace of Mat3 has dimension <=4"
            ),
            "conclusion": (
                "some K=K_*+tM is singular, sigma(K)=0, diag(K)=diag(K_*), "
                "and r(K)q^[2]=r(K_*)q^[2]"
            ),
            "terminal": (
                "rank(K)<=2, so r(K) is a sum of at most two literal "
                "endpoint-product channels"
            ),
            "fixture": trace_pairing_and_pencil_fixture(),
        },
        "first_derivative_boundary": {
            "q_variation": "q -> q+t z, z=r(M)",
            "contracted_top_derivative": "z*q^[2]=0",
            "uncontracted_row_derivative": (
                "d(a_ij q^[3]+p_i s_j q^[2])=p_i s_j z q"
            ),
            "guard": common_q_first_derivative_guard(),
        },
        "scope": {
            "negative": (
                "the bare dark-annihilator input is a universal consequence "
                "of the six offdiagonal zero target rows and has no direct "
                "minimum-support/deletion content"
            ),
            "positive": (
                "the singular two-channel cap is forced source-validly, "
                "without an occurrence projector"
            ),
            "remaining": (
                "use the other eight shared rows/occurrence derivatives to "
                "exclude or land the singular two-channel scalar-zero packet"
            ),
        },
    }


EXPECTED_LEDGER_SHA256 = (
    "cc0a6f90398b744bc4ff1f75d4af67f6338e2dd2ed887e28f33b0498529eea76"
)


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
    print("h3 unified dark-annihilator singular-cap boundary: PASS")
    print("mode", arguments.mode)
    print("dark rank<=2 caps: universal five-plane shadow, not deletion")
    print("positive export: singular scalar-zero cap with <=2 channels")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
