#!/usr/bin/env python3
"""Exact audit of the k=1 shared-line rank-drop boundary at h=3.

Assume the literal full-nine equations and write the unique endpoint-star
overlap as P u = S v = ell.  If Q=q^[3] has a mixed coefficient, the six
contracted rows put multiplication by G=ell*q^[2] in the four-dimensional
space <Q,X0,X1,X2>.  Since im(P)+im(S) has dimension five, a second kernel
line exists.  A lift (c,d) of that line gives

    M = c v^T + u d^T,

which is nonzero, has rank at most two, zero physical diagonal, zero direct
pairing, and response r(M)=ell*h with r(M)q^[2]=0.

The checker verifies the exact quotient construction, lift invariance,
nonvanishing, a six-site square-free fixture with invertible K_* and
r(K_*)^[3] != 0, and an exhaustive finite-field mutation guard for the
injectivity of the quotient-to-matrix map.  It does not promote the derived
dark cap to a source deletion; that is the sharply isolated next lemma.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_rank_deficient_latent_fullnine_boundary.py":
        "ae178897f9de221bd262c1d0de4277e945976c5e6b43f71c69e009f330b92d20",
    "notes/h3-rank-deficient-latent-fullnine-boundary.md":
        "8d8dd990b432306bba634b3529577aab7072ed5c4aaf73d7f0f894e2a1963e59",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)] if matrix else []


def matvec(matrix, vector):
    return [sum(entry * value for entry, value in zip(row, vector, strict=True))
            for row in matrix]


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


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    columns = len(matrix[0]) if matrix else 0
    free = [column for column in range(columns) if column not in pivots]
    answer = []
    for free_column in free:
        vector = [Q(0)] * columns
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        answer.append(vector)
    return answer


def outer(left, right):
    return [[x * y for y in right] for x in left]


def add_matrix(left, right):
    return [[x + y for x, y in zip(lrow, rrow, strict=True)]
            for lrow, rrow in zip(left, right, strict=True)]


def pairing(matrix, direct):
    return sum(matrix[i][j] * direct[i][j]
               for i in range(3) for j in range(3))


def linear_form(vector):
    return {1 << site: value for site, value in enumerate(vector) if value}


def multiply(left, right):
    answer = Counter()
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            answer[left_mask | right_mask] += left_value * right_value
    return {mask: value for mask, value in answer.items() if value}


def add_polynomials(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return {mask: value for mask, value in answer.items() if value}


def response(matrix, p_forms, s_forms):
    terms = []
    for i in range(3):
        for j in range(3):
            if matrix[i][j]:
                product = multiply(linear_form(p_forms[i]),
                                   linear_form(s_forms[j]))
                terms.append({mask: matrix[i][j] * value
                              for mask, value in product.items()})
    return add_polynomials(*terms)


def exact_fixture():
    # Five independent physical forms on six residual sites.  The fifth is
    # deliberately non-coordinate so that the scalar-zero response has a
    # nonzero square-free cube.
    f0 = (Q(1), Q(0), Q(0), Q(0), Q(0), Q(0))
    f1 = (Q(0), Q(1), Q(0), Q(0), Q(0), Q(0))
    f2 = (Q(0), Q(0), Q(1), Q(0), Q(0), Q(0))
    f3 = (Q(0), Q(0), Q(0), Q(1), Q(0), Q(0))
    f4 = (Q(0), Q(0), Q(0), Q(0), Q(1), Q(1))
    p_forms = (f0, f1, f2)
    s_forms = (
        f3,
        f4,
        tuple(f0[i] + f1[i] + f2[i] - f3[i] - f4[i]
              for i in range(6)),
    )
    p = transpose(p_forms)
    s = transpose(s_forms)
    union = [prow + srow for prow, srow in zip(p, s, strict=True)]
    require(rank(p) == rank(s) == 3, "the endpoint stars lost injectivity")
    require(rank(union) == 5, "the endpoint-star union is not k=1")

    u = (Q(1), Q(1), Q(1))
    v = (Q(1), Q(1), Q(1))
    ell = tuple(matvec(p, u))
    require(ell == tuple(matvec(s, v)), "Pu=Sv failed")

    # a=E_01 has trace zero, so K_*=I is scalar-zero.  Its unequal row and
    # column sums make Q genuinely independent of the three pure readouts in
    # the contracted multiplication table.
    direct = [[Q(0)] * 3 for _ in range(3)]
    direct[0][1] = Q(1)
    k_star = [[Q(int(i == j)) for j in range(3)] for i in range(3)]
    require(rank(k_star) == 3 and pairing(k_star, direct) == 0,
            "K_* is not invertible scalar-zero")

    r_star = response(k_star, p_forms, s_forms)
    r_star_cube = multiply(multiply(r_star, r_star), r_star)
    require(r_star_cube == {(1 << 6) - 1: Q(-12)},
            ("r(K_*)^3 fixture changed", r_star_cube))
    r_star_divided_cube = r_star_cube[(1 << 6) - 1] / Q(6)
    require(r_star_divided_cube == Q(-2),
            ("r(K_*)^[3] fixture changed", r_star_divided_cube))

    # Coordinates are X0,X1,X2,Q.  For (c,d), the six literal rows give
    # diag_i=c_i v_i+u_i d_i and
    # sigma=c^T a v+u^T a d.  A mixed coefficient of Q makes all four
    # coordinates independent.
    av = tuple(matvec(direct, v))
    uta = tuple(matvec(transpose(direct), u))
    psi = []
    for i in range(3):
        psi.append([Q(int(j == i)) * v[i] for j in range(3)]
                   + [Q(int(j == i)) * u[i] for j in range(3)])
    psi.append(list(av) + list(uta))
    require(rank(psi) == 4, "the mixed-top target map is not rank four")
    kernel = nullspace(psi)
    require(len(kernel) == 2, "the six-row kernel is not two-dimensional")

    overlap_lift = tuple(u) + tuple(-entry for entry in v)
    require(matvec(psi, overlap_lift) == [Q(0)] * 4,
            "the overlap relation does not kill the six rows")
    chosen_lift = (Q(1), Q(1), Q(0), Q(-1), Q(-1), Q(0))
    require(matvec(psi, chosen_lift) == [Q(0)] * 4,
            "the chosen second kernel lift is not killed")
    require(rank([list(overlap_lift), list(chosen_lift)]) == 2,
            "the chosen lift is only the overlap relation")

    c, d = chosen_lift[:3], chosen_lift[3:]
    cap = add_matrix(outer(c, v), outer(u, d))
    expected_cap = [[Q(0), Q(0), Q(1)],
                    [Q(0), Q(0), Q(1)],
                    [Q(-1), Q(-1), Q(0)]]
    require(cap == expected_cap, ("derived cap changed", cap))
    require(rank(cap) == 2, "the derived cap is not the expected rank two")
    require(tuple(cap[i][i] for i in range(3)) == (Q(0),) * 3,
            "the mixed-top cap diagonal is nonzero")
    require(pairing(cap, direct) == 0,
            "the mixed-top cap direct scalar is nonzero")

    h = tuple(matvec(union, chosen_lift))
    require(any(h), "the physical annihilator h vanished")
    expected_response = multiply(linear_form(ell), linear_form(h))
    require(response(cap, p_forms, s_forms) == expected_response,
            "r(M) is not the literal factor ell*h")

    # Changing a lift by the unique kernel of F must not change M.
    shifted = tuple(chosen_lift[i] + Q(7) * overlap_lift[i]
                    for i in range(6))
    shifted_cap = add_matrix(outer(shifted[:3], v),
                             outer(u, shifted[3:]))
    require(shifted_cap == cap, "the cap depends on the overlap lift")

    damaged = list(chosen_lift)
    damaged[0] += Q(1)
    require(matvec(psi, damaged) != [Q(0)] * 4,
            "mutation control did not leave the target-map kernel")

    return {
        "P_rank": rank(p),
        "S_rank": rank(s),
        "union_rank": rank(union),
        "overlap_relation": tuple(map(str, overlap_lift)),
        "target_map_rank": rank(psi),
        "target_map_kernel_dimension": len(kernel),
        "quotient_kernel_dimension": len(kernel) - 1,
        "K_star_rank": rank(k_star),
        "K_star_direct_scalar": str(pairing(k_star, direct)),
        "r_K_star_cube_full_coefficient": str(r_star_cube[(1 << 6) - 1]),
        "r_K_star_divided_cube_full_coefficient": str(r_star_divided_cube),
        "derived_cap": tuple(tuple(map(str, row)) for row in cap),
        "derived_cap_rank": rank(cap),
        "derived_cap_diagonal": tuple(str(cap[i][i]) for i in range(3)),
        "derived_cap_direct_scalar": str(pairing(cap, direct)),
        "derived_response_factor": "r(M)=ell*h",
        "literal_annihilator": "ell*h*q^[2]=0",
    }


def finite_field_injectivity(prime, exhaustive):
    """Mutation guard for M=0 iff (c,d) is the overlap relation.

    This is not the characteristic-zero proof (which is one line using a
    nonzero coordinate of u and v).  It exhausts the exact rank-one identity
    over F_3 so that a transpose/sign/lift mutation cannot pass unnoticed.
    """
    vectors = [tuple((number // (prime ** index)) % prime for index in range(3))
               for number in range(prime ** 3)]
    nonzero = [vector for vector in vectors if any(vector)]
    pairs = [(u, v) for u in nonzero for v in nonzero]
    if not exhaustive:
        pairs = pairs[:52]
    zero_matrices = 0
    tested = 0
    for u, v in pairs:
        relation = tuple(u) + tuple((-entry) % prime for entry in v)
        multiples = {
            tuple((scalar * entry) % prime for entry in relation)
            for scalar in range(prime)
        }
        for c in vectors:
            for d in vectors:
                tested += 1
                matrix = tuple(
                    (c[i] * v[j] + u[i] * d[j]) % prime
                    for i in range(3) for j in range(3)
                )
                if any(matrix):
                    continue
                zero_matrices += 1
                require(tuple(c) + tuple(d) in multiples,
                        ("theta acquired an extra kernel", prime, u, v, c, d))
    require(zero_matrices == len(pairs) * prime,
            ("wrong zero-matrix count", zero_matrices, len(pairs) * prime))
    return {
        "field": "F_%d" % prime,
        "uv_pairs": len(pairs),
        "lifts_tested": tested,
        "zero_matrices": zero_matrices,
        "expected_overlap_multiples": len(pairs) * prime,
    }


def build_ledger(mode):
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    # The full F_3 census is subsecond and keeps the signed ledger identical
    # in all advertised modes.  ``mode`` is retained as a CLI compatibility
    # flag and printed below, rather than changing theorem content.
    finite = finite_field_injectivity(3, True)
    return {
        "theorem": "k=1 mixed-top shared-line rank-drop boundary",
        "pins": PINS,
        "hypotheses": (
            "literal full-nine rows; P,S injective; dim(imP+imS)=5; "
            "Q=q^[3] has a mixed coefficient"
        ),
        "basis_free_construction": {
            "G": "ell*q^[2], where Pu=Sv=ell",
            "dimension_step": (
                "mu_G maps the five-dimensional physical star sum to "
                "span(Q,X0,X1,X2), so ker(mu_G) is nonzero"
            ),
            "quotient": "D=ker(mu_G o F)/ker(F), dim(D)>=1",
            "map": "theta([c,d])=c*v^T+u*d^T",
            "well_defined": "adding lambda*(u,-v) leaves theta unchanged",
            "injective": "theta=0 forces (c,d)=lambda*(u,-v)",
        },
        "literal_conclusion": (
            "every nonzero class yields nonzero M with rank(M)<=2, "
            "diag(M)=0, sigma(M)=0, r(M)=ell*h, and r(M)q^[2]=0"
        ),
        "fixture": exact_fixture(),
        "finite_field_mutation_guard": finite,
        "scope": {
            "exact": (
                "the rank-drop conclusion is forced inside any literal "
                "source satisfying the hypotheses"
            ),
            "not_claimed": (
                "a factorized dark q^[2]-annihilator is not yet proved to "
                "be a removable source summand or an active clean cap"
            ),
            "formal_fixture": (
                "the displayed six-site stars certify compatibility of the "
                "linear-algebra hypotheses, K_* invertibility, and "
                "r(K_*)^[3]!=0; no common q is supplied, so it is not an "
                "EqSystem source guard"
            ),
            "next_lemma": (
                "factorized-dark-annihilator descent: ell*h*q^[2]=0 with "
                "the retained nine rows implies a source-labelled deletion "
                "or an active/unit exit"
            ),
        },
    }


EXPECTED_LEDGER_SHA256 = (
    "966ed6c492acda585286e247d1885fc965b46b1d5b6e7ce04de20ccbddfa8cdc"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger(arguments.mode)
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("h3 k=1 overlap shared-line rank-drop: PASS")
    print("mode", arguments.mode)
    print("exact descent: rank-3 K_* -> nonzero factorized dark rank<=2 cap")
    print("terminal: ell*h*q^[2]=0; deletion/active promotion remains open")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
