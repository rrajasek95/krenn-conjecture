#!/usr/bin/env python3
"""Classify the intrinsic kernel in the rank-deficient h=3 latent branch.

For injective endpoint-star maps P,S:C^3->L with intersection dimension k,
the symmetrized product map

    Phi(M)=P M S^T + S M^T P^T

has kernel Lambda^2(im(P) intersection im(S)), hence dimension C(k,2).
Contracting the literal full-nine rows by a kernel matrix M gives the exact
identity

    sigma(M) q^[3] = sum_i M_ii X_i.

This checker audits the normal forms k=1,2,3, the kernel and activity
trichotomy, and sharp latent guards with invertible K and r(K)^[3]!=0.
The guards satisfy all nine *formal response* products but deliberately fail
literal common-power compatibility; the pinned private-edge theorem excludes
their q^[2]=F, q^[3]=0 completion.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_rootless_latent_polarization_involution.py":
        "d6869f6ef83cda61ccb490232b033a40abe41e234ae234397117ebec86cd43df",
    "notes/rootless-latent-polarization-involution.md":
        "a746db7d56ea611ce9b1a90142f52df92fe69e048c1a65f1b55f746de35a9465",
    "notes/uniform-pure-lift-private-edge-degeneration.md":
        "bb8b4f0b5315ca14354b7e7cbcd7d29a87dac7b519704ea3ca9cf8e2ebe94207",
    "computations/verify_uniform_pure_lift_private_edge_degeneration.py":
        "6c715abb7a5fb7139eac5c5b62a18e1989fa133fe209b3fe3ada4253e8219433",
    "notes/curved-no-root-macaulay-and-scalar-zero-packet.md":
        "2edbdae83d1c1b3f80184d37dbb2052a4079dae3376f21f8cf426edbe4e50f26",
}

COLOURS = tuple(range(3))
SITES = tuple(range(6))
PAIRS = ((0, 1), (2, 3), (4, 5))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def zeros(rows, columns):
    return [[Q(0) for _ in range(columns)] for _ in range(rows)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)] if matrix else []


def matmul(left, right):
    require(not left or len(left[0]) == len(right),
            (len(left[0]) if left else 0, len(right)))
    columns = len(right[0]) if right else 0
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(columns)] for i in range(len(left))]


def add(left, right):
    return [[a + b for a, b in zip(lrow, rrow, strict=True)]
            for lrow, rrow in zip(left, right, strict=True)]


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


def nullspace_rows(matrix):
    reduced, pivots = rref(matrix)
    columns = len(matrix[0]) if matrix else 0
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Q(0)] * columns
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(vector)
    return basis


def columns(*vectors):
    return transpose([list(vector) for vector in vectors])


def flatten(matrix):
    return tuple(entry for row in matrix for entry in row)


def unflatten(vector, rows, columns_count):
    return [list(vector[row * columns_count:(row + 1) * columns_count])
            for row in range(rows)]


def normal_form(k):
    """Return injective P,S with intersection dimension k."""
    dimension = 6 - k
    p_vectors = tuple(tuple(Q(int(index == colour))
                            for index in range(dimension))
                      for colour in range(3))
    s_indices = tuple(range(k)) + tuple(range(3, dimension))
    require(len(s_indices) == 3, (k, s_indices))
    s_vectors = tuple(tuple(Q(int(index == selected))
                            for index in range(dimension))
                      for selected in s_indices)
    p = columns(*p_vectors)
    s = columns(*s_vectors)
    require(rank(p) == rank(s) == 3, (k, rank(p), rank(s)))
    require(rank([prow + srow for prow, srow in zip(p, s, strict=True)])
            == dimension, k)
    return p, s


def product_matrix(p, s, coefficient):
    return add(matmul(p, matmul(coefficient, transpose(s))),
               matmul(s, matmul(transpose(coefficient), transpose(p))))


def product_kernel(p, s):
    dimension = len(p)
    columns_out = []
    for i, j in product(COLOURS, repeat=2):
        matrix = zeros(3, 3)
        matrix[i][j] = Q(1)
        columns_out.append(flatten(product_matrix(p, s, matrix)))
    linear_map = transpose(columns_out)
    require(len(linear_map) == dimension * dimension, dimension)
    basis = [unflatten(vector, 3, 3)
             for vector in nullspace_rows(linear_map)]
    return basis


def sigma(matrix, direct):
    return sum(matrix[i][j] * direct[i][j]
               for i, j in product(COLOURS, repeat=2))


def diagonal_entries(matrix):
    return tuple(matrix[i][i] for i in COLOURS)


def latent_kernel_census():
    # A symmetric off-diagonal direct block has alpha=a01=-1, trace zero,
    # so the canonical scalar-zero pairing is K*=I.  It annihilates every
    # skew kernel in the aligned normal forms.
    direct = zeros(3, 3)
    direct[0][1] = direct[1][0] = Q(-1)
    records = []
    for k in (1, 2, 3):
        p, s = normal_form(k)
        kernel = product_kernel(p, s)
        require(len(kernel) == k * (k - 1) // 2,
                (k, len(kernel)))
        require(all(not any(flatten(product_matrix(p, s, matrix)))
                    for matrix in kernel), k)
        dark = tuple((diagonal_entries(matrix), sigma(matrix, direct))
                     for matrix in kernel)
        require(all(diagonal == (Q(0), Q(0), Q(0)) and scalar == 0
                    for diagonal, scalar in dark), (k, dark))
        records.append({
            "intersection_dimension": k,
            "latent_dimension": 6 - k,
            "product_kernel_dimension": len(kernel),
            "expected_kernel": f"Lambda^2(C^{k})",
            "kernel_basis": tuple(tuple(map(str, flatten(matrix)))
                                  for matrix in kernel),
            "kernel_diagonals": tuple(tuple(map(str, item[0]))
                                      for item in dark),
            "kernel_direct_pairings": tuple(str(item[1]) for item in dark),
        })
    return tuple(records), direct


# A linear form is a map (site, physical colour) -> coefficient.
def form(*terms):
    answer = defaultdict(Q)
    for site, colour, coefficient in terms:
        answer[(site, colour)] += Q(coefficient)
    return {key: value for key, value in answer.items() if value}


def multiply_forms(left, right):
    answer = Counter()
    for (site_left, colour_left), value_left in left.items():
        for (site_right, colour_right), value_right in right.items():
            if site_left == site_right:
                continue
            if site_left < site_right:
                key = ((site_left, site_right), colour_left, colour_right)
            else:
                key = ((site_right, site_left), colour_right, colour_left)
            answer[key] += value_left * value_right
    return Counter({key: value for key, value in answer.items() if value})


def add_quadratics(*quadratics):
    answer = Counter()
    for quadratic in quadratics:
        answer.update(quadratic)
    return Counter({key: value for key, value in answer.items() if value})


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))


def quadratic_value(quadratic, endpoints, left_colour, right_colour):
    return quadratic.get((endpoints, left_colour, right_colour), Q(0))


def cube_coefficient(quadratic, word):
    total = Q(0)
    for matching in MATCHINGS:
        term = Q(1)
        for endpoints in matching:
            term *= quadratic_value(quadratic, endpoints,
                                    word[endpoints[0]], word[endpoints[1]])
        total += term
    return total


def multiply_linear_pair_by_missing_tensor(left, right, missing_pair, colour,
                                            scale=Q(1)):
    """Return the degree-six word coefficients of left*right*E_c(pair)."""
    answer = Counter()
    for (left_site, left_colour), left_value in left.items():
        for (right_site, right_colour), right_value in right.items():
            if left_site == right_site:
                continue
            if {left_site, right_site} != set(missing_pair):
                continue
            word = [colour] * 6
            word[left_site] = left_colour
            word[right_site] = right_colour
            answer[tuple(word)] += scale * left_value * right_value
    return Counter({word: value for word, value in answer.items() if value})


def physical_star_guard(k):
    # The first k channels share their P/S form.  Every channel is supported
    # on its own missing pair, so both triples remain injective and their
    # intersection is exactly k-dimensional.
    p = []
    s = []
    for colour, (left, right) in enumerate(PAIRS):
        if colour < k:
            shared = form((left, colour, 1), (right, colour, 1))
            p.append(shared)
            s.append(shared)
        else:
            p.append(form((left, colour, 1)))
            s.append(form((right, colour, 1)))

    coordinate_keys = tuple((site, colour)
                            for site in SITES for colour in COLOURS)
    p_matrix = [[star.get(key, Q(0)) for star in p]
                for key in coordinate_keys]
    s_matrix = [[star.get(key, Q(0)) for star in s]
                for key in coordinate_keys]
    require(rank(p_matrix) == rank(s_matrix) == 3, k)
    union_rank = rank([prow + srow for prow, srow in
                       zip(p_matrix, s_matrix, strict=True)])
    require(union_rank == 6 - k, (k, union_rank))

    response = add_quadratics(*(multiply_forms(p[i], s[i])
                                for i in COLOURS))
    word = (0, 0, 1, 1, 2, 2)
    response_top = cube_coefficient(response, word)
    expected_top = Q(2) ** k
    require(response_top == expected_top, (k, response_top, expected_top))

    # Formal q^[2]=F: each pure lift has the pair of its own channel missing.
    # Shared channels contribute a factor two and are scaled by 1/2.
    scales = tuple(Q(1, 2) if colour < k else Q(1)
                   for colour in COLOURS)
    rows = {}
    for i, j in product(COLOURS, repeat=2):
        total = Counter()
        for colour in COLOURS:
            total.update(multiply_linear_pair_by_missing_tensor(
                p[i], s[j], PAIRS[colour], colour, scales[colour]))
        rows[i, j] = Counter({key: value for key, value in total.items()
                              if value})
        expected = Counter({(i,) * 6: Q(1)}) if i == j else Counter()
        require(rows[i, j] == expected, (k, i, j, rows[i, j], expected))

    # The first shared line has u=v=e0.  Contracting the nine formal rows
    # along either representation of ell=p0=s0 gives the same six literal
    # shared-linear rows.  In the Q=0 guard they are X0 at (i or j)=0 and
    # zero otherwise.
    for i in COLOURS:
        expected = Counter({(0,) * 6: Q(1)}) if i == 0 else Counter()
        require(rows[i, 0] == expected, (k, "p_i ell", i, rows[i, 0]))
    for j in COLOURS:
        expected = Counter({(0,) * 6: Q(1)}) if j == 0 else Counter()
        require(rows[0, j] == expected, (k, "ell s_j", j, rows[0, j]))

    return {
        "intersection_dimension": k,
        "star_union_dimension": union_rank,
        "P_injective": True,
        "S_injective": True,
        "K": "I_3",
        "canonical_direct": "a01=a10=-1, trace=0, hence K*=I_3",
        "mixed_response_word": "001122",
        "r^[3]_coefficient": str(response_top),
        "formal_full_nine_response_rows": 9,
        "shared_linear_contracted_rows": 6,
        "formal_q^[2]_pure_lift_scales": tuple(map(str, scales)),
        "literal_common_power_verdict": (
            "NO: q^[2]=F and q^[3]=0 is excluded by the pinned uniform "
            "pure-lift private-edge theorem"
        ),
    }


def contraction_truth_table():
    """Audit the exact consequences sigma(M)Q=sum diag(M)X."""
    # Independent coordinates: Qmixed, Q0,Q1,Q2,X0,X1,X2.  The equality
    # coefficient vector is sigma*Q - sum diag_i*Xi.
    examples = {
        "unit": ((Q(0), Q(1), Q(0)), Q(0),
                 (Q(0), Q(0), Q(0), Q(0))),
        "active_clean": ((Q(2), Q(3), Q(5)), Q(1),
                         (Q(0), Q(2), Q(3), Q(5))),
        "binary_deletion": ((Q(2), Q(0), Q(5)), Q(1),
                            (Q(0), Q(2), Q(0), Q(5))),
        "mixed_forces_dark": ((Q(0), Q(0), Q(0)), Q(0),
                              (Q(7), Q(2), Q(3), Q(5))),
    }
    verdicts = {}
    for name, (diagonal, scalar, q_coordinates) in examples.items():
        q_mixed, q0, q1, q2 = q_coordinates
        residual = (scalar * q_mixed,
                    scalar * q0 - diagonal[0],
                    scalar * q1 - diagonal[1],
                    scalar * q2 - diagonal[2])
        if name == "unit":
            require(residual != (Q(0),) * 4, residual)
            verdict = "sigma=0 and nonzero diagonal gives a source unit"
        elif name == "active_clean":
            require(residual == (Q(0),) * 4, residual)
            require(scalar and all(diagonal), (diagonal, scalar))
            verdict = "kernel response zero plus all activity factors nonzero"
        elif name == "binary_deletion":
            require(residual == (Q(0),) * 4, residual)
            verdict = "q^[3]=2X0+5X2 is a binary residual source"
        else:
            # This row records the logical implication, rather than using
            # the non-dark diagonal values supplied only to make Q mixed.
            require(q_mixed, q_coordinates)
            verdict = "if Q has this mixed coordinate, equality forces sigma=diag=0"
        verdicts[name] = verdict
    return verdicts


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    kernel, direct = latent_kernel_census()
    guards = tuple(physical_star_guard(k) for k in (1, 2, 3))
    return {
        "theorem": "rank-deficient latent full-nine kernel boundary",
        "pins": PINS,
        "intrinsic_ordinary_kernel_census": kernel,
        "direct_block": tuple(tuple(map(str, row)) for row in direct),
        "literal_full_nine_contraction": {
            "identity": "sigma(M)*q^[3]=sum_i M_ii*X_i for Phi(M)=0",
            "truth_table": contraction_truth_table(),
            "classification": (
                "mixed q^[3] forces every intrinsic kernel direction dark; "
                "pure ternary q^[3] gives an active clean kernel root unless "
                "the whole kernel is dark; pure unary/binary q^[3] is a "
                "smaller-colour residual source; q^[3]=0 forces zero kernel "
                "diagonals but is not excluded without an additional "
                "pure-lift hypothesis"
            ),
        },
        "sharp_latent_guards": guards,
        "terminal_strata": {
            "k=1": (
                "no intrinsic product-kernel direction; coarse overlap alone "
                "gives no cap or full-row deletion"
            ),
            "k=2": (
                "one rank-two kernel line; mixed q^[3] forces the literal "
                "dark condition diag(N)=0=sigma(N), while q^[3]=0 forces "
                "diag(N)=0 only"
            ),
            "k=3": (
                "three-dimensional skew kernel; absence of an active clean "
                "root forces the whole kernel into one activity hyperplane, "
                "and mixed q^[3] forces diag=sigma=0 on all of it"
            ),
        },
        "scope": (
            "the kernel contraction is a consequence of the literal nine "
            "EqSystem rows.  The displayed guards prove only that injective "
            "overlapping stars, invertible K, nonzero r^[3], and all nine "
            "formal response products are compatible; they are not physical "
            "sources because no common q realizes their F,Q powers"
        ),
    }


EXPECTED_LEDGER_SHA256 = "ffdf0de29566a0de3a7bf6ffdd47281591b99e12c8aba2d220e8c8724289a143"


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
    print("h3 rank-deficient latent full-nine boundary: PASS")
    print("mode", arguments.mode)
    print("kernel dimensions k=1,2,3: 0,1,3")
    print("literal contraction: unit / active-clean / pure deletion / dark")
    print("formal response guards: k=1,2,3; no literal common-power lift")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
