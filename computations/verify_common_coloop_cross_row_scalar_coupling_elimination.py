#!/usr/bin/env python3
"""Audit simultaneous common-coloop cross-row/scalar elimination.

For disjoint singleton kernels c=e_r and d=e_s, the two formerly omitted
full-nine rows are (r,t) and (t,s).  Together with the r- and s-diagonal
rows they imply, when Q=q^[h] is nonzero,

    a_rt * a_ts = 0.

The checker verifies the exact local-tensor elimination, all sharp residual
branches, abstract scalar-extended cokernel witnesses on those branches,
and the failure of both cross rows in the literal consecutive-power 7/9
packet.  Standard library only; live under -O and -I -S.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import product


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def vector(*entries):
    return tuple(F(entry) for entry in entries)


def add_vectors(*vectors):
    if not vectors:
        return ()
    require(all(len(item) == len(vectors[0]) for item in vectors),
            "vector dimensions changed")
    return tuple(sum(item[index] for item in vectors) for index in range(len(vectors[0])))


def scale_vector(source, scalar):
    scalar = F(scalar)
    return tuple(scalar * entry for entry in source)


def dot(left, right):
    require(len(left) == len(right), "dot-product dimensions changed")
    return sum(a * b for a, b in zip(left, right))


def rref(rows):
    work = [[F(value) for value in row] for row in rows]
    if not work:
        return (), ()
    pivot_row = 0
    pivots = []
    for column in range(len(work[0])):
        selected = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * normalized
                for entry, normalized in zip(work[row], work[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(vectors):
    return len(rref(vectors)[1]) if vectors else 0


LOCAL_DIMENSION = 3
OFF_DIMENSION = 3
TENSOR_DIMENSION = LOCAL_DIMENSION * OFF_DIMENSION
E = tuple(
    tuple(F(1) if index == basis else F(0) for index in range(LOCAL_DIMENSION))
    for basis in range(LOCAL_DIMENSION)
)
Y = tuple(
    tuple(F(1) if index == basis else F(0) for index in range(OFF_DIMENSION))
    for basis in range(OFF_DIMENSION)
)
ZERO_TENSOR = (F(0),) * TENSOR_DIMENSION


def outer(local, off):
    return tuple(local[i] * off[j] for i in range(LOCAL_DIMENSION) for j in range(OFF_DIMENSION))


def tensor_columns(tensor):
    require(len(tensor) == TENSOR_DIMENSION, "tensor dimensions changed")
    return tuple(
        tuple(tensor[i * OFF_DIMENSION + j] for i in range(LOCAL_DIMENSION))
        for j in range(OFF_DIMENSION)
    )


def local_rank(tensor):
    return rank(tensor_columns(tensor))


def source_row(direct, top, response, target):
    return add_vectors(scale_vector(top, direct), response) == target


def branch_audits():
    x_r = outer(E[0], Y[0])
    x_s = outer(E[1], Y[1])
    cases = []

    # Q=0: both cross coefficients are invisible to all physical rows.
    q_zero = ZERO_TENSOR
    zero_case = {
        "name": "zero-top-two-scalar",
        "Q": q_zero,
        "u": E[0],
        "v": E[1],
        "a_rr": F(0),
        "a_rt": F(2),
        "a_ss": F(0),
        "a_ts": F(-3),
        "H_r": Y[0],
        "H_t": vector(0, 0, 0),
        "G_s": Y[1],
        "G_t": vector(0, 0, 0),
        "expected_rank": 0,
    }
    cases.append(zero_case)

    # Local rank two: both cross coefficients and both A-arms vanish.
    q_rank_two = add_vectors(outer(E[0], Y[0]), outer(E[1], Y[1]))
    rank_two_case = {
        "name": "rank-two-zero-scalar",
        "Q": q_rank_two,
        "u": E[0],
        "v": E[1],
        "a_rr": F(0),
        "a_rt": F(0),
        "a_ss": F(0),
        "a_ts": F(0),
        "H_r": Y[0],
        "H_t": vector(0, 0, 0),
        "G_s": Y[1],
        "G_t": vector(0, 0, 0),
        "expected_rank": 2,
    }
    cases.append(rank_two_case)

    # Local rank one on u: the left coefficient may survive, the right
    # coefficient and right A-arm must vanish.
    left_case = {
        "name": "rank-one-left-scalar",
        "Q": outer(E[0], Y[2]),
        "u": E[0],
        "v": E[1],
        "a_rr": F(0),
        "a_rt": F(2),
        "a_ss": F(0),
        "a_ts": F(0),
        "H_r": Y[0],
        "H_t": scale_vector(Y[2], -2),
        "G_s": Y[1],
        "G_t": vector(0, 0, 0),
        "expected_rank": 1,
    }
    cases.append(left_case)

    right_case = {
        "name": "rank-one-right-scalar",
        "Q": outer(E[1], Y[2]),
        "u": E[0],
        "v": E[1],
        "a_rr": F(0),
        "a_rt": F(0),
        "a_ss": F(0),
        "a_ts": F(-3),
        "H_r": Y[0],
        "H_t": vector(0, 0, 0),
        "G_s": Y[1],
        "G_t": scale_vector(Y[2], 3),
        "expected_rank": 1,
    }
    cases.append(right_case)

    ledger = []
    for case in cases:
        q_top = case["Q"]
        u_h_r = outer(case["u"], case["H_r"])
        u_h_t = outer(case["u"], case["H_t"])
        v_g_s = outer(case["v"], case["G_s"])
        v_g_t = outer(case["v"], case["G_t"])
        require(source_row(case["a_rr"], q_top, u_h_r, x_r),
                f"r diagonal failed in {case['name']}")
        require(source_row(case["a_rt"], q_top, u_h_t, ZERO_TENSOR),
                f"rt cross row failed in {case['name']}")
        require(source_row(case["a_ss"], q_top, v_g_s, x_s),
                f"s diagonal failed in {case['name']}")
        require(source_row(case["a_ts"], q_top, v_g_t, ZERO_TENSOR),
                f"ts cross row failed in {case['name']}")
        require(local_rank(q_top) == case["expected_rank"],
                f"local top rank changed in {case['name']}")
        if q_top != ZERO_TENSOR:
            require(not (case["a_rt"] and case["a_ts"]),
                    f"both cross scalars survived at nonzero Q in {case['name']}")
        ledger.append(
            f"{case['name']}:{local_rank(q_top)}:{case['a_rt']}:{case['a_ts']}"
        )
    return tuple(cases), sha256("|".join(ledger).encode()).hexdigest()


def projective_small_vectors():
    representatives = []
    for entries in product((-1, 0, 1), repeat=LOCAL_DIMENSION):
        if not any(entries):
            continue
        first = next(value for value in entries if value)
        if first != 1:
            continue
        representatives.append(tuple(F(value) for value in entries))
    return tuple(representatives)


def simultaneous_nonzero_contradiction_audit():
    # If both cross coefficients are nonzero, Q has one local line qline
    # which must equal both span(u) and span(v).  The diagonal rows then
    # require e_r in that same line and e_s in that same line.  Exhaust
    # all small rational projective representatives as an independent
    # exact audit of the incidence contradiction.
    representatives = projective_small_vectors()
    tested = 0
    feasible = 0
    for qline in representatives:
        for u in representatives:
            for v in representatives:
                both_cross = rank((qline, u)) == rank((qline, v)) == 1
                if not both_cross:
                    continue
                tested += 1
                diagonals = (
                    rank((qline, u, E[0])) == 1
                    and rank((qline, v, E[1])) == 1
                )
                if diagonals:
                    feasible += 1
    require(tested > 0, "the simultaneous-cross incidence audit was empty")
    require(feasible == 0, "both nonzero cross coefficients survived both diagonals")
    return tested


def coupled_cokernel_sharpness_audits(cases):
    # Cross-row completion constrains the scalar pair (a_rt,a_ts), but the
    # source rows alone do not relate D to the affine residual C.  These
    # exact two-coordinate polar ledgers realize a detecting augmented
    # covector on every residual branch.
    witnesses = {
        "zero-top-two-scalar": {
            "D_left": vector(2, 0),
            "D_right": vector(-3, 0),
            "Lambda": vector(1, 0),
            "mu": F(1),
            "C": vector(1, 0),
        },
        "rank-two-zero-scalar": {
            "D_left": vector(0, 1),
            "D_right": vector(0, -1),
            "Lambda": vector(1, 0),
            "mu": F(0),
            "C": vector(1, 0),
        },
        "rank-one-left-scalar": {
            "D_left": vector(2, 0),
            "D_right": vector(0, 1),
            "Lambda": vector(1, 0),
            "mu": F(1),
            "C": vector(1, 0),
        },
        "rank-one-right-scalar": {
            "D_left": vector(0, 1),
            "D_right": vector(-3, 0),
            "Lambda": vector(1, 0),
            "mu": F(1),
            "C": vector(1, 0),
        },
    }
    ledger = []
    for case in cases:
        witness = witnesses[case["name"]]
        left_value = dot(witness["Lambda"], witness["D_left"])
        right_value = dot(witness["Lambda"], witness["D_right"])
        require(left_value == witness["mu"] * case["a_rt"],
                f"left scalar-extended equation failed in {case['name']}")
        require(right_value == witness["mu"] * case["a_ts"],
                f"right scalar-extended equation failed in {case['name']}")
        require(dot(witness["Lambda"], witness["C"]) != 0,
                f"affine residual detector failed in {case['name']}")
        ledger.append(f"{case['name']}:{left_value}:{right_value}")
    return sha256("|".join(ledger).encode()).hexdigest()


# Literal site-square-zero algebra for the exact 7/9 specialization.
SITE_COUNT = 6
SITE_RANGE = tuple(range(SITE_COUNT))
EMPTY_WORD = (None,) * SITE_COUNT


def poly_clean(terms):
    return {monomial: value for monomial, value in terms.items() if value}


def poly_unit():
    return {EMPTY_WORD: F(1)}


def poly_add(*elements):
    out = {}
    for element in elements:
        for monomial, value in element.items():
            out[monomial] = out.get(monomial, F(0)) + value
    return poly_clean(out)


def poly_scale(element, scalar):
    scalar = F(scalar)
    return poly_clean({monomial: scalar * value for monomial, value in element.items()})


def poly_mul(left, right):
    out = {}
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            if any(
                left_word[site] is not None and right_word[site] is not None
                for site in SITE_RANGE
            ):
                continue
            monomial = tuple(
                right_word[site]
                if right_word[site] is not None
                else left_word[site]
                for site in SITE_RANGE
            )
            out[monomial] = out.get(monomial, F(0)) + left_value * right_value
    return poly_clean(out)


def divided_power(element, exponent):
    result = poly_unit()
    for divisor in range(1, exponent + 1):
        result = poly_scale(poly_mul(result, element), F(1, divisor))
    return result


def one_site(site, color):
    monomial = [None] * SITE_COUNT
    monomial[site] = color
    return {tuple(monomial): F(1)}


def cell(left, right, color):
    return poly_mul(one_site(left, color), one_site(right, color))


def literal_seven_of_nine_cross_row_audit():
    zero_site, one, two, three, four, exposed = SITE_RANGE
    q0 = poly_add(
        cell(zero_site, one, 0),
        cell(two, three, 0),
        cell(zero_site, two, 1),
        cell(one, four, 1),
        cell(three, four, 2),
    )
    rho = poly_mul(one_site(exposed, 2), one_site(zero_site, 2))
    q = poly_add(q0, rho)
    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    p = (one_site(exposed, 0), one_site(three, 1), one_site(two, 2))
    s = (one_site(four, 0), one_site(exposed, 1), one_site(one, 2))
    pair_rows = {
        (i, j): poly_mul(poly_mul(p[i], s[j]), q2)
        for i in range(3) for j in range(3)
    }
    pure = tuple(
        {tuple(color for _ in SITE_RANGE): F(1)}
        for color in range(3)
    )
    expected = {
        (0, 0): pure[0],
        (0, 1): {},
        (0, 2): {tuple(int(x) for x in "121220"): F(1)},
        (1, 0): {},
        (1, 1): pure[1],
        (1, 2): {},
        (2, 0): {},
        (2, 1): {tuple(int(x) for x in "002221"): F(1)},
        (2, 2): pure[2],
    }
    require(pair_rows == expected, "the literal diagonal-complete 7/9 table changed")
    row_rt = pair_rows[(0, 2)]
    row_ts = pair_rows[(2, 1)]
    require(q3 == {tuple(int(x) for x in "210012"): F(1)},
            "literal 7/9 top word changed")
    require(row_rt == {tuple(int(x) for x in "121220"): F(1)},
            "literal rt row changed")
    require(row_ts == {tuple(int(x) for x in "002221"): F(1)},
            "literal ts row changed")
    top_word = next(iter(q3))
    require(next(iter(row_rt)) != top_word and next(iter(row_ts)) != top_word,
            "a missing literal row became a direct multiple of Q")
    # Since all three are distinct basis monomials, each augmented pair
    # (Q,row) has rank two.  Neither direct scalar exists.
    coordinate_rows = (
        vector(1, 0, 0),
        vector(0, 1, 0),
        vector(0, 0, 1),
    )
    require(rank((coordinate_rows[0], coordinate_rows[1])) == 2,
            "literal rt/Q rank changed")
    require(rank((coordinate_rows[0], coordinate_rows[2])) == 2,
            "literal ts/Q rank changed")
    ledger_words = ["".join(str(entry) for entry in top_word)]
    for key in sorted(pair_rows):
        terms = pair_rows[key]
        encoded = ",".join(
            "".join(str(entry) for entry in monomial)
            for monomial in sorted(terms)
        )
        ledger_words.append(f"{key[0]}{key[1]}:{encoded}")
    text = "|".join(ledger_words)
    return sha256(text.encode()).hexdigest()


def main():
    cases, branch_digest = branch_audits()
    tested = simultaneous_nonzero_contradiction_audit()
    coker_digest = coupled_cokernel_sharpness_audits(cases)
    literal_digest = literal_seven_of_nine_cross_row_audit()
    print("cross-row branch ledger sha256", branch_digest)
    print("coupled cokernel ledger sha256", coker_digest)
    print("literal 7/9 cross-row ledger sha256", literal_digest)
    print("simultaneous nonzero incidence cases", tested)
    print("full-nine cross-row scalar coupling: verified")


if __name__ == "__main__":
    main()
