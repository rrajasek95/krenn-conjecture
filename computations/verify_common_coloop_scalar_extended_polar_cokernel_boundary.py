#!/usr/bin/env python3
"""Audit the scalar-extended common-coloop polar-cokernel boundary.

The clean equation and scalar constraint must be dualized together before
passing to a fixed-scalar response quotient.  This checker independently
verifies the augmented primal/dual criterion and two complementary literal
consecutive-power guards:

* a tensor-cokernel guard whose contracted target is supplied by the wrong
  individual source row; and
* a diagonal-complete 7/9 guard in which the only two omitted rows are
  exactly the direct coefficients capable of moving the scalar.

Standard library only; live under -O and -I -S.  Research evidence only.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


N = 6
SITES = tuple(range(N))
COLORS = tuple(range(3))
EXPOSED = 5
EMPTY = (None,) * N


def clean(terms):
    return {monomial: value for monomial, value in terms.items() if value}


def zero():
    return {}


def unit():
    return {EMPTY: F(1)}


def add(*elements):
    out = {}
    for element in elements:
        for monomial, coefficient in element.items():
            out[monomial] = out.get(monomial, F(0)) + coefficient
    return clean(out)


def scale(element, scalar):
    scalar = F(scalar)
    return clean({monomial: scalar * value for monomial, value in element.items()})


def mul(left, right):
    out = {}
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            if any(
                left_word[site] is not None and right_word[site] is not None
                for site in SITES
            ):
                continue
            monomial = tuple(
                right_word[site]
                if right_word[site] is not None
                else left_word[site]
                for site in SITES
            )
            out[monomial] = out.get(monomial, F(0)) + left_value * right_value
    return clean(out)


def divided_power(element, exponent):
    result = unit()
    for divisor in range(1, exponent + 1):
        result = scale(mul(result, element), F(1, divisor))
    return result


def one_site(site, color, value=1):
    monomial = [None] * N
    monomial[site] = color
    return {tuple(monomial): F(value)} if value else zero()


def cell(left, right, color, value=1):
    return scale(mul(one_site(left, color), one_site(right, color)), value)


def word(text):
    require(len(text) == N, "word length mismatch")
    return tuple(None if symbol == "." else int(symbol) for symbol in text)


def coefficient(element, monomial):
    return element.get(monomial, F(0))


def rref(source):
    work = [[F(value) for value in row] for row in source]
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


def matrix_rank(rows):
    return len(rref(rows)[1]) if rows else 0


def columns_to_rows(columns):
    if not columns:
        return ()
    return tuple(
        tuple(columns[column][row] for column in range(len(columns)))
        for row in range(len(columns[0]))
    )


def augmented_consistent(columns, right_side):
    source = columns_to_rows(columns)
    require(len(source) == len(right_side), "augmented output dimensions changed")
    augmented = tuple(
        tuple(row) + (right_side[index],)
        for index, row in enumerate(source)
    )
    return matrix_rank(source) == matrix_rank(augmented)


def dot(left, right):
    require(len(left) == len(right), "dot-product dimensions changed")
    return sum(a * b for a, b in zip(left, right))


def dual_detects(columns, right_side, witness):
    require(all(dot(witness, column) == 0 for column in columns),
            "dual witness misses an augmented source column")
    return dot(witness, right_side) != 0


def tensor_digest(elements):
    lines = []
    for name, element in elements:
        encoded = []
        for monomial, value in sorted(
            element.items(),
            key=lambda item: tuple(-1 if x is None else x for x in item[0]),
        ):
            text = "".join("." if x is None else str(x) for x in monomial)
            encoded.append(f"{text}:{value.numerator}/{value.denominator}")
        lines.append(f"{name}=" + ",".join(encoded))
    return sha256("\n".join(lines).encode()).hexdigest()


def augmented_duality_audits():
    cases = (
        {
            "name": "consistent-source",
            "columns": ((F(1), F(0), F(1)), (F(0), F(1), F(1))),
            "right": (F(2), F(3), F(5)),
            "witnesses": (),
            "consistent": True,
        },
        {
            "name": "tensor-cokernel",
            "columns": ((F(0), F(0), F(0)), (F(0), F(0), F(0))),
            "right": (F(0), F(1), F(0)),
            "witnesses": ((F(0), F(1), F(0)),),
            "consistent": False,
        },
        {
            "name": "scalar-cokernel",
            "columns": ((F(0), F(0), F(0)), (F(0), F(0), F(0))),
            "right": (F(0), F(0), F(1)),
            "witnesses": ((F(0), F(0), F(1)),),
            "consistent": False,
        },
        {
            "name": "mixed-cokernel",
            "columns": ((F(1), F(0), F(1)), (F(0), F(1), F(1))),
            "right": (F(1), F(1), F(3)),
            "witnesses": ((F(1), F(1), F(-1)),),
            "consistent": False,
        },
    )
    ledger = []
    for case in cases:
        actual = augmented_consistent(case["columns"], case["right"])
        require(actual == case["consistent"],
                f"augmented primal classification changed in {case['name']}")
        for witness in case["witnesses"]:
            require(dual_detects(case["columns"], case["right"], witness),
                    f"augmented dual witness failed in {case['name']}")
        require(actual or case["witnesses"],
                f"an inconsistent case lacks a dual witness in {case['name']}")
        ledger.append(f"{case['name']}:{int(actual)}:{len(case['witnesses'])}")
    return sha256("|".join(ledger).encode()).hexdigest()


def tensor_cokernel_row_provenance_guard():
    zero_site, one, two, three, four, exposed = SITES
    z = tuple(one_site(site, 2) for site in range(EXPOSED))
    local0 = one_site(exposed, 0)
    local1 = one_site(exposed, 1)
    local2 = one_site(exposed, 2)

    q0 = mul(z[3], z[4])
    rho = mul(local2, z[0])
    q = add(q0, rho)
    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    require(q3 == zero(), "the tensor-cokernel guard acquired a top power")

    p = (local0, z[1], z[3])
    s = (z[2], local1, z[4])
    pair_rows = {
        (i, j): mul(mul(p[i], s[j]), q2)
        for i in COLORS for j in COLORS
    }
    x2 = {word("222222"): F(1)}
    require(
        {key: value for key, value in pair_rows.items() if value}
        == {(1, 0): x2},
        "the contracted tensor-cokernel row provenance changed",
    )

    # K0=E10+E22 has kappa_2=1.  Its contracted response equals X2,
    # although the individual tensor is supplied by the off-diagonal 10
    # row and the actual 22 row is zero.
    bar_r = add(mul(z[1], z[2]), mul(z[3], z[4]))
    contracted = mul(bar_r, q2)
    require(contracted == x2, "the contracted target guard changed")
    require(pair_rows[(1, 0)] == x2 and pair_rows[(2, 2)] == zero(),
            "the target provenance defect disappeared")

    first_polar = mul(bar_r, q0)
    second_polar = divided_power(bar_r, 2)
    require(first_polar == second_polar == {word(".2222."): F(1)},
            "the two polar coefficients changed")

    # The direct matrix has only a22=1.  It fixes sigma0=1 on K0 and
    # vanishes on the singleton tangent T=(e0 tensor D)+(C tensor e1).
    tangent = (
        mul(local0, z[2]),
        mul(local0, z[4]),
        mul(z[1], local1),
        mul(z[3], local1),
    )
    polar_at_one = add(first_polar, second_polar)
    require(all(mul(arm, polar_at_one) == zero() for arm in tangent),
            "a tangent arm escaped the tensor-cokernel polar kernel")

    c_at_one = mul(rho, second_polar)
    require(c_at_one == x2, "the actual affine residual changed")
    require(coefficient(c_at_one, word("222222")) == 1,
            "the X2 detector misses the affine residual")

    return (
        ("row-guard-q0", q0),
        ("row-guard-rho", rho),
        ("row-guard-q2", q2),
        ("row-guard-row10", pair_rows[(1, 0)]),
        ("row-guard-row22", pair_rows[(2, 2)]),
        ("row-guard-bar-r", bar_r),
        ("row-guard-D-linear", first_polar),
        ("row-guard-D-constant", second_polar),
        ("row-guard-C-at-one", c_at_one),
    )


def diagonal_complete_seven_of_nine_guard():
    zero_site, one, two, three, four, exposed = SITES
    q0 = add(
        cell(zero_site, one, 0),
        cell(two, three, 0),
        cell(zero_site, two, 1),
        cell(one, four, 1),
        cell(three, four, 2),
    )
    rho = mul(one_site(exposed, 2), one_site(zero_site, 2))
    q = add(q0, rho)
    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)

    p = (
        one_site(exposed, 0),
        one_site(three, 1),
        one_site(two, 2),
    )
    s = (
        one_site(four, 0),
        one_site(exposed, 1),
        one_site(one, 2),
    )
    pair_rows = {
        (i, j): mul(mul(p[i], s[j]), q2)
        for i in COLORS for j in COLORS
    }
    x = tuple({word(str(color) * N): F(1)} for color in COLORS)
    expected = {
        (0, 0): x[0],
        (0, 1): zero(),
        (0, 2): {word("121220"): F(1)},
        (1, 0): zero(),
        (1, 1): x[1],
        (1, 2): zero(),
        (2, 0): zero(),
        (2, 1): {word("002221"): F(1)},
        (2, 2): x[2],
    }
    require(pair_rows == expected, "the diagonal-complete 7/9 table changed")
    exact_rows = tuple(
        key for key in pair_rows
        if key not in ((0, 2), (2, 1))
    )
    require(all(
        pair_rows[(i, j)] == (x[i] if i == j else zero())
        for i, j in exact_rows
    ), "one of the seven supplied physical rows failed")

    # Q is nonzero.  Hence every direct coefficient on the seven already
    # exact rows is forced to zero.  On T=(e0 tensor D)+(C tensor e1), the
    # only untested scalar coefficients are a02 and a21.
    require(q3 == {word("210012"): F(1)}, "the 7/9 top power changed")
    known_scalar_entries = ((0, 0), (0, 1), (1, 1))
    require(all(key in exact_rows for key in known_scalar_entries),
            "a known singleton scalar entry became omitted")
    omitted_scalar_entries = ((0, 2), (2, 1))
    require(all(key not in exact_rows for key in omitted_scalar_entries),
            "an omitted singleton scalar entry became supplied")

    # Neither omitted tensor can be repaired by a direct multiple of Q:
    # each is a distinct basis word.  Thus the 7/9 packet has no full-nine
    # extension, and those are exactly the rows needed to move the scalar.
    for key in omitted_scalar_entries:
        require(len(pair_rows[key]) == 1 and len(q3) == 1,
                f"omitted row {key} stopped being monomial")
        require(next(iter(pair_rows[key])) != next(iter(q3)),
                f"omitted row {key} became a direct multiple of Q")

    bar_r = mul(p[2], s[2])
    first_polar = mul(bar_r, q0)
    second_polar = divided_power(bar_r, 2)
    require(first_polar == {word(".2222."): F(1)}
            and second_polar == zero(),
            "the diagonal-complete polar action changed")
    raw_arms = (
        mul(p[0], s[0]),
        mul(p[0], s[2]),
        mul(p[1], s[1]),
        mul(p[2], s[1]),
    )
    require(all(mul(arm, first_polar) == zero() for arm in raw_arms),
            "a raw singleton arm escaped the 7/9 polar kernel")

    # With the seven forced direct entries and K0=E22, sigma0=0 and the
    # actual C(z) is zero.  At z=0 the augmented system is consistent but
    # inactive.  Every z!=0 is detected solely by the scalar output row.
    c_polynomial = mul(rho, second_polar)
    require(c_polynomial == zero(), "the 7/9 affine residual became nonzero")
    zero_columns = tuple((F(0), F(0)) for _ in raw_arms)
    require(augmented_consistent(zero_columns, (F(0), F(0))),
            "the inactive z=0 augmented system became inconsistent")
    require(not augmented_consistent(zero_columns, (F(0), F(1))),
            "a nonzero scalar became attainable without an omitted row")
    require(dual_detects(zero_columns, (F(0), F(1)), (F(0), F(1))),
            "the scalar-only cokernel witness failed")

    return (
        ("seven-q0", q0),
        ("seven-rho", rho),
        ("seven-q2", q2),
        ("seven-Q", q3),
        ("seven-row00", pair_rows[(0, 0)]),
        ("seven-row11", pair_rows[(1, 1)]),
        ("seven-row22", pair_rows[(2, 2)]),
        ("seven-missing02", pair_rows[(0, 2)]),
        ("seven-missing21", pair_rows[(2, 1)]),
        ("seven-D-linear", first_polar),
        ("seven-D-constant", second_polar),
        ("seven-C", c_polynomial),
    )


def main():
    dual_digest = augmented_duality_audits()
    tensors = (
        tensor_cokernel_row_provenance_guard()
        + diagonal_complete_seven_of_nine_guard()
    )
    literal_digest = tensor_digest(tensors)
    print("augmented dual ledger sha256", dual_digest)
    print("literal source-row ledger sha256", literal_digest)
    print("scalar-extended polar cokernel: verified")
    print("contracted row-provenance guard: verified")
    print("diagonal-complete 7/9 scalar boundary: verified")


if __name__ == "__main__":
    main()
