#!/usr/bin/env python3
"""Exact audits for the scalar-unit star-fibre carrier boundary.

This is deliberately dependency-free.  It evaluates the coloured
site-square-zero algebra over ``fractions.Fraction`` and uses explicit
runtime checks, so ``python -O`` does not disable any test.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations


COLORS = ("a", "b", "c")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def clean(terms):
    return {m: c for m, c in terms.items() if c}


def zero(n):
    return (n, {})


def unit(n):
    return (n, {(None,) * n: F(1)})


def add(*elements):
    require(elements, "add needs an element")
    n = elements[0][0]
    out = {}
    for n_other, terms in elements:
        require(n_other == n, "algebra-size mismatch in add")
        for monomial, coefficient in terms.items():
            out[monomial] = out.get(monomial, F(0)) + coefficient
    return (n, clean(out))


def neg(element):
    n, terms = element
    return (n, {m: -c for m, c in terms.items()})


def sub(left, right):
    return add(left, neg(right))


def scale(element, scalar):
    n, terms = element
    scalar = F(scalar)
    return (n, clean({m: scalar * c for m, c in terms.items()}))


def mul(left, right):
    n, left_terms = left
    n_right, right_terms = right
    require(n == n_right, "algebra-size mismatch in mul")
    out = {}
    for left_monomial, left_coefficient in left_terms.items():
        for right_monomial, right_coefficient in right_terms.items():
            result = list(left_monomial)
            valid = True
            for site, color in enumerate(right_monomial):
                if color is None:
                    continue
                if result[site] is not None:
                    valid = False
                    break
                result[site] = color
            if valid:
                result = tuple(result)
                out[result] = out.get(result, F(0)) + left_coefficient * right_coefficient
    return (n, clean(out))


def divided_power(element, exponent):
    n, _ = element
    result = unit(n)
    for k in range(1, exponent + 1):
        result = scale(mul(result, element), F(1, k))
    return result


def one_site(n, site, color, coefficient=1):
    monomial = [None] * n
    monomial[site] = color
    return (n, {tuple(monomial): F(coefficient)}) if coefficient else zero(n)


def cell(n, u, color_u, v, color_v, coefficient=1):
    return scale(mul(one_site(n, u, color_u), one_site(n, v, color_v)), coefficient)


def word(n, color):
    return (color,) * n


def coefficient(element, monomial):
    return element[1].get(tuple(monomial), F(0))


def same(left, right):
    return left[0] == right[0] and clean(left[1]) == clean(right[1])


def sum_elements(n, elements):
    result = zero(n)
    for element in elements:
        result = add(result, element)
    return result


def rank(vectors):
    if not vectors:
        return 0
    matrix = [list(vector) for vector in vectors]
    rows = len(matrix)
    columns = len(matrix[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((r for r in range(pivot_row, rows) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for r in range(rows):
            if r == pivot_row or not matrix[r][column]:
                continue
            factor = matrix[r][column]
            matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def vector_of_form(form):
    n, terms = form
    vector = []
    for site in range(n):
        for color in COLORS:
            monomial = [None] * n
            monomial[site] = color
            vector.append(terms.get(tuple(monomial), F(0)))
    return vector


def params(**changes):
    result = {
        "x": F(2), "y": F(1), "z": F(-1), "w": F(1),
        "u": F(1), "v": F(1),
        "A": F(1), "B": F(0), "S": F(-1),
        "P": F(1), "T": F(1), "C": F(1), "D": F(1),
    }
    result.update({name: F(value) for name, value in changes.items()})
    return result


def packet(values):
    n = 6
    q = sum_elements(n, [
        cell(n, 2, "b", 3, "b", values["x"]),
        cell(n, 4, "b", 5, "b", values["y"]),
        cell(n, 3, "b", 4, "b", values["z"]),
        cell(n, 2, "b", 5, "b", values["w"]),
        cell(n, 1, "c", 4, "c", values["u"]),
        cell(n, 3, "c", 5, "c", values["v"]),
    ])
    p = {
        "a": add(one_site(n, 3, "b", values["A"]),
                 one_site(n, 5, "b", values["B"])),
        "b": one_site(n, 0, "b", values["P"]),
        "c": one_site(n, 2, "c", values["C"]),
    }
    s = {
        "a": one_site(n, 4, "b", values["S"]),
        "b": one_site(n, 1, "b", values["T"]),
        "c": one_site(n, 0, "c", values["D"]),
    }
    response = {(i, j): mul(p[i], s[j]) for i in COLORS for j in COLORS}
    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    rows = {}
    for i in COLORS:
        for j in COLORS:
            row = mul(response[i, j], q2)
            if i == "a" and j == "a":
                row = add(row, q3)
            rows[i, j] = row
    carrier = add(q, scale(response["a", "a"], F(1, 2)))
    theta = mul(response["a", "a"], carrier)
    z_bb = mul(response["b", "b"], theta)
    return {
        "q": q, "p": p, "s": s, "R": response, "rows": rows,
        "H": carrier, "Theta": theta, "Zbb": z_bb,
    }


def expected_scalar_word(n, scalar, color):
    if not scalar:
        return zero(n)
    return (n, {word(n, color): F(scalar)})


MIXED_WORD = tuple("ccbbcb")


def audit_parameter_formula(values):
    data = packet(values)
    rows = data["rows"]
    bb = values["P"] * values["T"] * (
        values["x"] * values["y"] + values["z"] * values["w"])
    cc = values["C"] * values["D"] * values["u"] * values["v"]
    cross = values["D"] * values["u"] * (
        values["A"] * values["w"] + values["B"] * values["x"])
    carrier = values["P"] * values["T"] * values["S"] * (
        values["A"] * values["w"] + values["B"] * values["x"])

    require(same(rows["b", "b"], expected_scalar_word(6, bb, "b")),
            "bb formula failed")
    require(same(rows["c", "c"], expected_scalar_word(6, cc, "c")),
            "cc formula failed")
    require(same(rows["a", "c"], (6, {MIXED_WORD: cross}) if cross else zero(6)),
            "selected-cross singleton formula failed")
    require(same(data["Zbb"], expected_scalar_word(6, carrier, "b")),
            "common-carrier formula failed")
    require(same(rows["a", "a"], zero(6)), "exceptional row should be identically zero")
    for i, j in (("a", "b"), ("b", "a"), ("b", "c"),
                 ("c", "a"), ("c", "b")):
        require(same(rows[i, j], zero(6)), f"row {(i, j)} should vanish")
    require(same(divided_power(data["R"]["a", "a"], 2), zero(6)),
            "selected response square should vanish")
    require(values["P"] * values["T"] * values["S"] * cross
            == values["D"] * values["u"] * carrier,
            "cross/carrier conservation identity failed")
    return data


def edge_support(values):
    p_site = 6
    q_site = 7
    edges = []

    def include(left, right, weight):
        if weight:
            edges.append((frozenset((left, right)), weight))

    include((2, "b"), (3, "b"), values["x"])
    include((4, "b"), (5, "b"), values["y"])
    include((3, "b"), (4, "b"), values["z"])
    include((2, "b"), (5, "b"), values["w"])
    include((1, "c"), (4, "c"), values["u"])
    include((3, "c"), (5, "c"), values["v"])
    include((p_site, "a"), (3, "b"), values["A"])
    include((p_site, "a"), (5, "b"), values["B"])
    include((p_site, "b"), (0, "b"), values["P"])
    include((p_site, "c"), (2, "c"), values["C"])
    include((q_site, "a"), (4, "b"), values["S"])
    include((q_site, "b"), (1, "b"), values["T"])
    include((q_site, "c"), (0, "c"), values["D"])
    include((p_site, "a"), (q_site, "a"), F(1))
    return edges


def audit_anchors(values):
    edges = edge_support(values)
    incidence = {}
    for endpoints, _ in edges:
        for endpoint in endpoints:
            incidence[endpoint] = incidence.get(endpoint, 0) + 1
    anchors = {endpoints for endpoints, _ in edges
               if all(incidence[endpoint] == 1 for endpoint in endpoints)}
    expected = {
        frozenset(((6, "b"), (0, "b"))),
        frozenset(((7, "b"), (1, "b"))),
        frozenset(((6, "c"), (2, "c"))),
        frozenset(((7, "c"), (0, "c"))),
    }
    require(expected <= anchors, "one of the four complementary anchors was lost")


def audit_guard_and_sharp_rewrite():
    original = params()
    data = audit_parameter_formula(original)
    require(original["P"] * original["T"] *
            (original["x"] * original["y"] + original["z"] * original["w"]) == 1,
            "guard bb normalization failed")
    require(original["C"] * original["D"] * original["u"] * original["v"] == 1,
            "guard cc normalization failed")
    require(coefficient(data["rows"]["a", "c"], MIXED_WORD) == 1,
            "guard selected-cross residual should be one")
    require(coefficient(data["Zbb"], word(6, "b")) == -1,
            "guard carrier should be -X_b")
    require(original["z"] - original["A"] * original["S"] == 0,
            "guard marked curvature should vanish")
    require(rank([vector_of_form(data["p"][i]) for i in COLORS]) == 3,
            "guard p-star is not good")
    require(rank([vector_of_form(data["s"][i]) for i in COLORS]) == 3,
            "guard s-star is not good")
    audit_anchors(original)

    q = data["q"]
    r = data["R"]["a", "a"]
    for t, expected_bb in ((F(0), F(1)), (F(1), F(0))):
        q_t = add(q, scale(r, t))
        f_bb = mul(data["R"]["b", "b"], divided_power(q_t, 2))
        f_cc = mul(data["R"]["c", "c"], divided_power(q_t, 2))
        require(same(f_bb, expected_scalar_word(6, expected_bb, "b")),
                "guard endpoint bb table failed")
        require(same(f_cc, expected_scalar_word(6, 1, "c")),
                "guard endpoint cc table failed")

    repaired = params(B=F(-1, 2))
    repaired_data = audit_parameter_formula(repaired)
    for i in COLORS:
        for j in COLORS:
            if (i, j) == ("a", "a"):
                require(same(repaired_data["rows"][i, j], zero(6)),
                        "repaired exceptional row changed unexpectedly")
            else:
                expected = expected_scalar_word(6, 1, i) if i == j else zero(6)
                require(same(repaired_data["rows"][i, j], expected),
                        f"repaired row {(i, j)} is not exact")
    require(same(repaired_data["Zbb"], zero(6)),
            "repairing ac should kill the common carrier")
    require(repaired["z"] - repaired["A"] * repaired["S"] == 0,
            "repair should preserve marked zero curvature")
    audit_anchors(repaired)

    mutated = params(B=F(-1, 2) + F(1, 7))
    mutated_data = audit_parameter_formula(mutated)
    require(coefficient(mutated_data["rows"]["a", "c"], MIXED_WORD) != 0,
            "cross mutation was not detected")
    require(coefficient(mutated_data["Zbb"], word(6, "b")) != 0,
            "carrier mutation was not detected")


def nonlinear_values(t):
    t = F(t)
    amplitude = 1 + t * t
    return params(
        A=amplitude,
        B=-amplitude / 2,
        z=-amplitude,
        y=1 + t * t / 2,
    )


def audit_nonlinear_eight_row_family():
    for t in (F(0), F(1), F(2), F(-2), F(3, 2)):
        values = nonlinear_values(t)
        data = audit_parameter_formula(values)
        require(values["P"] * values["T"] *
                (values["x"] * values["y"] + values["z"] * values["w"]) == 1,
                "nonlinear bb row failed")
        require(values["C"] * values["D"] * values["u"] * values["v"] == 1,
                "nonlinear cc row failed")
        require(coefficient(data["rows"]["a", "c"], MIXED_WORD) == 0,
                "nonlinear selected-cross row failed")
        require(same(data["Zbb"], zero(6)), "nonlinear carrier should vanish")
        require(values["z"] - values["A"] * values["S"] == 0,
                "nonlinear marked curvature changed")
        require(same(divided_power(data["q"], 3), zero(6)),
                "nonlinear family unexpectedly changed the top target")
        require(rank([vector_of_form(data["p"][i]) for i in COLORS]) == 3,
                "nonlinear p-star lost goodness")
        require(rank([vector_of_form(data["s"][i]) for i in COLORS]) == 3,
                "nonlinear s-star lost goodness")
        audit_anchors(values)
    second_difference = (nonlinear_values(0)["A"]
                         - 2 * nonlinear_values(1)["A"]
                         + nonlinear_values(2)["A"])
    require(second_difference != 0, "family accidentally became affine")


def full_normal_carrier(q, r, h):
    n = q[0]
    terms = []
    for ell in range(h - 1):
        terms.append(scale(
            mul(divided_power(q, h - 2 - ell), divided_power(r, ell)),
            F(1, ell + 1),
        ))
    return sum_elements(n, terms)


def audit_star_fibre_linearization():
    for h in range(3, 6):
        n = 2 * h
        q_cells = []
        for k in range(h):
            q_cells.append(cell(n, 2 * k, "b", 2 * k + 1, "b", k + 1))
            q_cells.append(cell(n, 2 * k + 1, "c", (2 * k + 2) % n, "c", F(1, k + 1)))
        q = sum_elements(n, q_cells)
        d = sum_elements(n, [
            cell(n, 0, "a", site, COLORS[site % 3], F(site, site + 1))
            for site in range(1, n)
        ])
        require(same(divided_power(d, 2), zero(n)), "star direction did not square to zero")
        replacement = add(q, d)
        for exponent in range(1, h + 1):
            expected = add(divided_power(q, exponent),
                           mul(d, divided_power(q, exponent - 1)))
            require(same(divided_power(replacement, exponent), expected),
                    f"star-fibre linearization failed at h={h}, exponent={exponent}")

        p = {
            "a": add(one_site(n, 1, "a"), one_site(n, 3, "b", 2)),
            "b": one_site(n, 2, "b"),
            "c": one_site(n, 4, "c"),
        }
        s = {
            "a": add(one_site(n, 5, "a"), one_site(n, 2, "c", -1)),
            "b": one_site(n, 3, "b"),
            "c": one_site(n, 1, "c"),
        }
        response = {(i, j): mul(p[i], s[j]) for i in COLORS for j in COLORS}
        for i in COLORS:
            for j in COLORS:
                old = mul(response[i, j], divided_power(q, h - 1))
                new = mul(response[i, j], divided_power(replacement, h - 1))
                if (i, j) == ("a", "a"):
                    old = add(old, divided_power(q, h))
                    new = add(new, divided_power(replacement, h))
                    expected_difference = add(
                        mul(d, divided_power(q, h - 1)),
                        mul(response[i, j], mul(d, divided_power(q, h - 2))),
                    )
                else:
                    expected_difference = mul(
                        response[i, j], mul(d, divided_power(q, h - 2)))
                require(same(sub(new, old), expected_difference),
                        f"nine-row star difference failed at h={h}, row={(i, j)}")

        r = response["a", "a"]
        old_h = full_normal_carrier(q, r, h)
        new_h = full_normal_carrier(replacement, r, h)
        j_terms = []
        for ell in range(h - 2):
            j_terms.append(scale(
                mul(divided_power(q, h - 3 - ell), divided_power(r, ell)),
                F(1, ell + 1),
            ))
        second_carrier = sum_elements(n, j_terms)
        require(same(sub(new_h, old_h), mul(d, second_carrier)),
                f"common-carrier update failed at h={h}")


def has_perfect_matching(n, edges):
    adjacency = {site: set() for site in range(n)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    def recurse(remaining):
        if not remaining:
            return True
        u = min(remaining)
        for v in adjacency[u] & remaining:
            if recurse(remaining - {u, v}):
                return True
        return False

    return recurse(set(range(n)))


def audit_exceptional_top_barrier():
    for h in range(3, 7):
        n = 2 * h
        q = sum_elements(n, [
            cell(n, 2 * k, "b", 2 * k + 1, "b", k + 1)
            for k in range(h)
        ])
        r = cell(n, 1, "b", 2, "b", -1)
        for centre in range(n):
            d = sum_elements(n, [
                cell(n, centre, "a", other, "a", other + 1)
                for other in range(n) if other != centre
            ])
            replacement = add(q, d)
            exceptional = add(
                divided_power(replacement, h),
                mul(r, divided_power(replacement, h - 1)),
            )
            require(coefficient(exceptional, word(n, "a")) == 0,
                    f"one-star perturbation created X_a at h={h}")

        all_a_matching = sum_elements(n, [
            cell(n, 2 * k, "a", 2 * k + 1, "a", k + 2)
            for k in range(h)
        ])
        replacement = add(q, all_a_matching)
        pure_a = coefficient(divided_power(replacement, h), word(n, "a"))
        expected = F(1)
        for k in range(h):
            expected *= k + 2
        require(pure_a == expected, f"all-a matching coefficient failed at h={h}")

        for number_of_centres in range(h):
            centres = set(range(number_of_centres))
            supported_edges = {
                (u, v) for u, v in combinations(range(n), 2)
                if u in centres or v in centres
            }
            require(not has_perfect_matching(n, supported_edges),
                    f"fewer than h stars unexpectedly supported a perfect matching at h={h}")
        centres = set(range(h))
        supported_edges = {
            (u, v) for u, v in combinations(range(n), 2)
            if u in centres or v in centres
        }
        require(has_perfect_matching(n, supported_edges),
                f"h-star threshold was not sharp at h={h}")


def main():
    for values in (
        params(),
        params(x=3, y=2, z=-2, w=F(5, 3), u=4, v=F(2, 5),
               A=F(7, 3), B=-2, S=5, P=2, T=-3, C=4, D=F(3, 2)),
        params(x=-2, y=F(4, 3), z=5, w=-1, u=F(2, 7), v=3,
               A=-4, B=F(5, 2), S=-3, P=F(7, 4), T=2, C=-5, D=6),
    ):
        audit_parameter_formula(values)
    audit_guard_and_sharp_rewrite()
    audit_nonlinear_eight_row_family()
    audit_star_fibre_linearization()
    audit_exceptional_top_barrier()
    print("scalar-unit nine-row star-fibre carrier conservation boundary: PASS")
    print("all symbolic-shape identities, four anchors, and both omitted rows: PASS")
    print("nonlinear eight-row family and h-star top-change threshold: PASS")


if __name__ == "__main__":
    main()
