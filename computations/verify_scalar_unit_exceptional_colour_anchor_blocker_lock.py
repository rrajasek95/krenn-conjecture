#!/usr/bin/env python3
"""Exact audits for the exceptional-colour anchor/blocker lock theorem."""

from __future__ import annotations

from fractions import Fraction as F


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def zero(n):
    return n, {}


def unit(n):
    return n, {(None,) * n: F(1)}


def clean(terms):
    return {monomial: coefficient for monomial, coefficient in terms.items() if coefficient}


def add(*elements):
    require(elements, "empty algebra sum")
    n = elements[0][0]
    out = {}
    for other_n, terms in elements:
        require(other_n == n, "algebra-size mismatch")
        for monomial, coefficient in terms.items():
            out[monomial] = out.get(monomial, F(0)) + coefficient
    return n, clean(out)


def scale(element, scalar):
    n, terms = element
    scalar = F(scalar)
    return n, clean({monomial: scalar * coefficient for monomial, coefficient in terms.items()})


def sub(left, right):
    return add(left, scale(right, -1))


def mul(left, right):
    n, left_terms = left
    other_n, right_terms = right
    require(n == other_n, "algebra-size mismatch")
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
    return n, clean(out)


def divided_power(element, exponent):
    n, _ = element
    result = unit(n)
    for k in range(1, exponent + 1):
        result = scale(mul(result, element), F(1, k))
    return result


def one_site(n, site, color, coefficient=1):
    if not coefficient:
        return zero(n)
    monomial = [None] * n
    monomial[site] = color
    return n, {tuple(monomial): F(coefficient)}


def cell(n, u, color_u, v, color_v, coefficient=1):
    return scale(mul(one_site(n, u, color_u), one_site(n, v, color_v)), coefficient)


def sum_elements(n, elements):
    result = zero(n)
    for element in elements:
        result = add(result, element)
    return result


def same(left, right):
    return left[0] == right[0] and clean(left[1]) == clean(right[1])


def full_word(n, color="a"):
    return (color,) * n


def coefficient(element, monomial):
    return element[1].get(tuple(monomial), F(0))


def project_grade(element, grade):
    n, terms = element
    return n, {
        monomial: value
        for monomial, value in terms.items()
        if sum(color is not None and color != "a" for color in monomial) == grade
    }


def defect_grade_audits():
    for h in range(3, 6):
        n = 2 * h
        q0 = sum_elements(n, [cell(n, 2 * i, "a", 2 * i + 1, "a", i + 1) for i in range(h)])
        q1 = sum_elements(n, [
            cell(n, 2 * i, "b", (2 * i + 3) % n, "a", F(i + 2, i + 1))
            for i in range(h)
        ])
        r0 = cell(n, 0, "a", 3, "a", 2)
        r1 = add(cell(n, 1, "b", 4, "a", -1), cell(n, 2, "a", 5, "b", 3))
        q = add(q0, q1)
        r = add(r0, r1)
        exceptional = add(divided_power(q, h), mul(r, divided_power(q, h - 1)))
        expected_zero = add(divided_power(q0, h), mul(r0, divided_power(q0, h - 1)))
        expected_one = add(
            mul(q1, divided_power(q0, h - 1)),
            mul(r1, divided_power(q0, h - 1)),
            mul(r0, mul(q1, divided_power(q0, h - 2))),
        )
        require(same(project_grade(exceptional, 0), expected_zero), f"grade-zero identity failed at h={h}")
        require(same(project_grade(exceptional, 1), expected_one), f"grade-one identity failed at h={h}")

        cofactor = add(divided_power(q, h - 1), mul(r, divided_power(q, h - 2)))
        expected_c1 = add(
            mul(q1, divided_power(q0, h - 2)),
            mul(r1, divided_power(q0, h - 2)),
            mul(r0, mul(q1, divided_power(q0, h - 3))),
        )
        require(same(project_grade(cofactor, 1), expected_c1), f"cofactor grade-one identity failed at h={h}")


def perfect_matchings(n, edges):
    adjacency = {site: set() for site in range(n)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    def recurse(remaining):
        if not remaining:
            return [()]
        u = min(remaining)
        results = []
        for v in sorted(adjacency[u] & remaining):
            edge = (min(u, v), max(u, v))
            for rest in recurse(remaining - {u, v}):
                results.append((edge,) + rest)
        return results

    return recurse(set(range(n)))


def sharp_anchor_charge_audits():
    for h in range(3, 9):
        n = 2 * h
        p_edges = {(2 * i, 2 * i + 1) for i in range(h)}
        blockers = set()
        paired_limit = h - (h % 2)
        for i in range(0, paired_limit, 2):
            blockers.add((2 * i, 2 * (i + 1)))
        if h % 2:
            blockers.add((2 * (h - 1), 0))
        require(len(blockers) == (h + 1) // 2, f"sharp blocker count failed at h={h}")
        covered = set()
        incidence_sum = 0
        for blocker in blockers:
            hit = set()
            for endpoint in blocker:
                hit.add(endpoint // 2)
            covered |= hit
            incidence_sum += len(hit)
        require(covered == set(range(h)), f"blocker cover failed at h={h}")
        require(incidence_sum >= h, f"incidence charge failed at h={h}")
        matchings = perfect_matchings(n, p_edges | blockers)
        canonical = tuple(sorted(p_edges))
        require(len(matchings) == 1 and tuple(sorted(matchings[0])) == canonical,
                f"blocker support acquired another perfect matching at h={h}")
        incidence = {site: 0 for site in range(n)}
        for u, v in p_edges | blockers:
            incidence[u] += 1
            incidence[v] += 1
        for u, v in p_edges:
            require(incidence[u] > 1 or incidence[v] > 1,
                    f"factor edge remained an anchor at h={h}")


def supported_all_a_cells(element):
    n, terms = element
    cells = []
    for monomial, value in terms.items():
        sites = [site for site, color in enumerate(monomial) if color is not None]
        if len(sites) == 2 and all(monomial[site] == "a" for site in sites):
            cells.append((sites[0], sites[1], value))
    return cells


def euler_sum(q, r, h):
    n = q[0]
    cofactor = add(divided_power(q, h - 1), mul(r, divided_power(q, h - 2)))
    total = F(0)
    for u, v, q_value in supported_all_a_cells(q):
        basis = cell(n, u, "a", v, "a")
        total += q_value * coefficient(mul(basis, cofactor), full_word(n))
    return total


def euler_audits():
    for h in range(3, 9):
        n = 2 * h
        factor = sum_elements(n, [cell(n, 2 * i, "a", 2 * i + 1, "a", i + 1) for i in range(h)])
        product = F(1)
        for i in range(h):
            product *= i + 1
        q_exact = scale(factor, 1)  # Q_a is product, so normalize one factor below.
        q_exact = add(q_exact, cell(n, 0, "a", 1, "a", F(1, product) - 1))
        require(coefficient(divided_power(q_exact, h), full_word(n)) == 1,
                f"exact-cancellation Q normalization failed at h={h}")
        require(euler_sum(q_exact, zero(n), h) == h,
                f"exact-cancellation Euler charge failed at h={h}")

        near = sum_elements(n, [cell(n, 2 * i, "a", 2 * i + 1, "a") for i in range(1, h)])
        response = cell(n, 0, "a", 1, "a")
        require(coefficient(divided_power(near, h), full_word(n)) == 0,
                f"binary Q should vanish at h={h}")
        require(coefficient(mul(response, divided_power(near, h - 1)), full_word(n)) == 1,
                f"binary response normalization failed at h={h}")
        require(euler_sum(near, response, h) == h - 1,
                f"binary Euler charge failed at h={h}")


def aggregate_edges_for_fan(h, rho, q_after=None):
    n = 2 * h
    selected_p = n
    selected_q = n + 1
    edges = []
    if q_after is None:
        for i in range(h):
            edges.append(((2 * i, "a"), (2 * i + 1, "a"), F(1)))
        for j in range(1, h):
            edges.append(((0, "a"), (2 * j, "a"), F(1)))
    else:
        for monomial, value in q_after[1].items():
            sites = [site for site, color in enumerate(monomial) if color is not None]
            if value and len(sites) == 2:
                edges.append(((sites[0], monomial[sites[0]]),
                              (sites[1], monomial[sites[1]]), value))
    edges.append(((selected_p, "a"), (1, "a"), F(1)))
    for j in range(1, h):
        edges.append(((selected_q, "a"), (2 * j + 1, "a"), rho[j]))
    edges.append(((selected_p, "a"), (selected_q, "a"), F(1)))
    return [edge for edge in edges if edge[2]]


def mutual_anchors(edges):
    incidence = {}
    for left, right, _ in edges:
        incidence[left] = incidence.get(left, 0) + 1
        incidence[right] = incidence.get(right, 0) + 1
    return {
        frozenset((left, right))
        for left, right, _ in edges
        if incidence[left] == 1 and incidence[right] == 1
    }


def fan_audits():
    for h in range(3, 9):
        n = 2 * h
        factors = [cell(n, 2 * i, "a", 2 * i + 1, "a") for i in range(h)]
        blockers = {j: cell(n, 0, "a", 2 * j, "a") for j in range(1, h)}
        q = sum_elements(n, factors + list(blockers.values()))
        rho = {j: F(1) for j in range(1, h - 1)}
        rho[h - 1] = F(-(h - 2))
        p = one_site(n, 1, "a")
        s = sum_elements(n, [one_site(n, 2 * j + 1, "a", rho[j]) for j in range(1, h)])
        r = mul(p, s)
        exceptional = add(divided_power(q, h), mul(r, divided_power(q, h - 1)))
        target = n, {full_word(n): F(1)}
        require(same(exceptional, target), f"fan exceptional row failed at h={h}")
        require(coefficient(divided_power(q, h), full_word(n)) == 1,
                f"fan direct top failed at h={h}")
        require(coefficient(mul(r, divided_power(q, h - 1)), full_word(n)) == 0,
                f"fan response cancellation failed at h={h}")
        require(all(not project_grade(exceptional, grade)[1] for grade in range(1, 2 * h + 1)),
                f"fan acquired a mixed grade at h={h}")
        before_anchors = mutual_anchors(aggregate_edges_for_fan(h, rho))
        for i in range(h):
            factor_key = frozenset(((2 * i, "a"), (2 * i + 1, "a")))
            require(factor_key not in before_anchors, f"fan factor became an anchor at h={h}, i={i}")

        cofactor = add(divided_power(q, h - 1), mul(r, divided_power(q, h - 2)))
        f0_basis = cell(n, 0, "a", 1, "a")
        c_f = coefficient(mul(f0_basis, cofactor), full_word(n))
        require(c_f == 1, f"fan factor cofactor failed at h={h}")
        for j in range(1, h):
            g_basis = cell(n, 0, "a", 2 * j, "a")
            c_g = coefficient(mul(g_basis, cofactor), full_word(n))
            require(c_g == rho[j], f"fan blocker cofactor failed at h={h}, j={j}")
            d = add(scale(g_basis, -1), scale(f0_basis, rho[j]))
            require(same(divided_power(d, 2), zero(n)), f"fan switch not square-zero at h={h}, j={j}")
            changed_q = add(q, d)
            changed_exceptional = add(
                divided_power(changed_q, h),
                mul(r, divided_power(changed_q, h - 1)),
            )
            require(same(changed_exceptional, target),
                    f"normalized fan deletion failed at h={h}, j={j}")
            require(len(changed_q[1]) < len(q[1]),
                    f"fan deletion did not lower support at h={h}, j={j}")
            after_anchors = mutual_anchors(aggregate_edges_for_fan(h, rho, changed_q))
            require(before_anchors <= after_anchors,
                    f"fan deletion destroyed an old anchor at h={h}, j={j}")


def main():
    defect_grade_audits()
    sharp_anchor_charge_audits()
    euler_audits()
    fan_audits()
    print("scalar-unit exceptional-colour anchor blocker lock: PASS")
    print("defect grades, Euler charges, and sharp incidence cover: PASS")
    print("uniform response-active fan and normalized deletions h=3..8: PASS")


if __name__ == "__main__":
    main()
