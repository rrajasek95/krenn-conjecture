#!/usr/bin/env python3
"""Lightweight symbolic audit of the overlapping pair-cap Bianchi identities."""

from collections import Counter


def clean(poly):
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if coefficient})


def one():
    return Counter({(): 1})


def var(name):
    return Counter({(name,): 1})


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, scalar):
    return clean(Counter({monomial: scalar * coefficient
                          for monomial, coefficient in poly.items()}))


def sub(left, right):
    return add(left, scale(right, -1))


def mul(*polys):
    answer = one()
    for poly in polys:
        product = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                product[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = clean(product)
    return answer


def replace_divided_power(poly, z, z0, z1, z2, r):
    """Reduce z*Z1=(R-1)Z0 and z*Z2=(R-2)Z1 exactly."""
    r_minus_one = sub(r, one())
    r_minus_two = sub(r, scale(one(), 2))
    answer = Counter()
    for monomial, coefficient in poly.items():
        factors = list(monomial)
        if "z" in factors and "Z1" in factors:
            factors.remove("z")
            factors.remove("Z1")
            factors.append("Z0")
            term = scale(var_product(factors), coefficient)
            answer.update(mul(term, r_minus_one))
        elif "z" in factors and "Z2" in factors:
            factors.remove("z")
            factors.remove("Z2")
            factors.append("Z1")
            term = scale(var_product(factors), coefficient)
            answer.update(mul(term, r_minus_two))
        else:
            answer[monomial] += coefficient
    return clean(answer)


def var_product(names):
    answer = one()
    for name in names:
        answer = mul(answer, var(name))
    return answer


def audit():
    names = "A B C E F U x y t v z R Z0 Z1 Z2".split()
    symbols = {name: var(name) for name in names}
    A, B, C, E, F, U = (symbols[name] for name in "A B C E F U".split())
    x, y, t, v, z = (symbols[name] for name in "x y t v z".split())
    R, Z0, Z1, Z2 = (symbols[name] for name in "R Z0 Z1 Z2".split())

    p_pq = add(mul(R, x, y), mul(A, z))
    p_pr = add(mul(R, x, t), mul(B, z))
    p_qr = add(mul(R, y, t), mul(C, z))
    transition = sub(mul(A, t), mul(B, y))

    # Triangle cap transition and its normal-star companion.
    assert not sub(sub(mul(p_pq, t), mul(p_pr, y)), mul(transition, z))
    l_pq_r = add(mul(R, B, y), mul(R, C, x), mul(A, t))
    l_pr_q = add(mul(R, A, t), mul(R, C, x), mul(B, y))
    assert not add(
        sub(l_pq_r, l_pr_q),
        mul(sub(R, one()), transition),
    )

    d1 = transition
    d2 = sub(mul(B, y), mul(C, x))
    d3 = sub(mul(C, x), mul(A, t))
    assert not add(d1, d2, d3)
    assert not sub(sub(mul(p_pr, y), mul(p_qr, x)), mul(d2, z))
    assert not sub(sub(mul(p_qr, x), mul(p_pq, t)), mul(d3, z))

    # Four-site curvature and scalar first Bianchi identity.
    l_pq_s = add(mul(R, E, y), mul(R, F, x), mul(A, v))
    l_pr_s = add(mul(R, E, t), mul(R, U, x), mul(B, v))
    curvature = sub(mul(A, U), mul(B, F))
    curvature_identity = sub(
        add(mul(U, p_pq), mul(t, l_pq_s)),
        add(mul(F, p_pr), mul(y, l_pr_s), mul(transition, v), mul(curvature, z)),
    )
    assert not curvature_identity

    curvature_two = sub(mul(A, U), mul(E, C))
    curvature_three = sub(mul(B, F), mul(E, C))
    assert not add(curvature, scale(curvature_two, -1), curvature_three)

    # Direct double coefficients differ by the same scalar curvature.
    m_pq_rs = add(mul(R, B, F), mul(R, E, C), mul(A, U))
    m_pr_qs = add(mul(R, A, U), mul(R, E, C), mul(B, F))
    assert not add(
        sub(m_pq_rs, m_pr_qs),
        mul(sub(R, one()), curvature),
    )

    # Double coefficient of the pq cap equals R times the raw four-cut split.
    b_pq = add(
        mul(m_pq_rs, Z0),
        mul(add(mul(l_pq_r, v), mul(l_pq_s, t), mul(U, p_pq)), Z1),
        mul(p_pq, t, v, Z2),
    )

    raw_four_cut = add(
        mul(add(mul(A, U), mul(B, F), mul(E, C)), Z0),
        mul(add(
            mul(A, t, v), mul(B, y, v), mul(E, y, t),
            mul(C, x, v), mul(F, x, t), mul(U, x, y),
        ), Z1),
        mul(x, y, t, v, Z2),
    )
    target = mul(R, raw_four_cut)
    assert not sub(replace_divided_power(b_pq, z, Z0, Z1, Z2, R), target)

    # The pr cap gives the same normalized four-cut tensor.
    l_pr_q = add(mul(R, A, t), mul(R, C, x), mul(B, y))
    l_pr_s = add(mul(R, E, t), mul(R, U, x), mul(B, v))
    b_pr = add(
        mul(m_pr_qs, Z0),
        mul(add(mul(l_pr_q, v), mul(l_pr_s, y), mul(F, p_pr)), Z1),
        mul(p_pr, y, v, Z2),
    )
    assert not sub(replace_divided_power(b_pr, z, Z0, Z1, Z2, R), target)

    return 10


if __name__ == "__main__":
    identities = audit()
    print(
        "overlapping pair-cap Bianchi connection: PASS; "
        f"symbolic identities={identities}; coefficient ring=Z[R]"
    )
