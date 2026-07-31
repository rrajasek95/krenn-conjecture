#!/usr/bin/env python3
"""Lightweight exact audit of the three-anchor apolar/Bianchi reduction."""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations


W = tuple(range(6))
EDGES = tuple(combinations(W, 2))


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def edge(i, j):
    return (i, j) if i < j else (j, i)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


# Sparse integer polynomials in the fifteen formal edge variables.  A
# monomial is a sorted tuple of edge labels, so repeated variables survive.
def poly_var(e):
    return Counter({(e,): 1})


def poly_add(*values):
    answer = Counter()
    for value in values:
        answer.update(value)
    return +answer


def poly_scale(value, scalar):
    return +Counter({monomial: scalar * coefficient for monomial, coefficient in value.items()})


def poly_mul(left, right):
    answer = Counter()
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            answer[monomial] += coefficient_left * coefficient_right
    return +answer


def hafnian(vertices, entries, zero=0, one=1, add=None, multiply=None):
    add = add or (lambda values: sum(values, zero))
    multiply = multiply or (lambda values: product(values, one))
    return add(
        [multiply([entries[edge(*pair)] for pair in matching]) for matching in matchings(tuple(vertices))]
    )


def product(values, one=1):
    answer = one
    for value in values:
        answer *= value
    return answer


def audit_double_polar_identity():
    variables = {e: poly_var(e) for e in EDGES}
    zero = Counter()
    one = Counter({(): 1})
    add = lambda values: poly_add(*values)
    def multiply(values):
        answer = one
        for value in values:
            answer = poly_mul(answer, value)
        return answer

    full_hafnian = hafnian(W, variables, zero, one, add, multiply)
    first_polar = {
        e: hafnian(tuple(x for x in W if x not in e), variables, zero, one, add, multiply)
        for e in EDGES
    }

    for i, j in EDGES:
        complement = tuple(x for x in W if x not in (i, j))
        double_polar = hafnian(complement, first_polar, zero, one, add, multiply)
        radial = poly_mul(full_hafnian, variables[(i, j)])
        cross_star = Counter()
        for selected in combinations(complement, 2):
            other = tuple(x for x in complement if x not in selected)
            term = multiply(
                [variables[edge(i, x)] for x in selected]
                + [variables[edge(j, x)] for x in other]
            )
            cross_star.update(term)
        expected = poly_add(radial, poly_scale(cross_star, 2))
        require(double_polar == expected, ("double-polar defect", (i, j)))

    all_one = {e: 1 for e in EDGES}
    require(hafnian(W, all_one) == 15, "six-site all-one hafnian changed")
    first_one = {e: hafnian(tuple(x for x in W if x not in e), all_one) for e in EDGES}
    require(first_one[(0, 1)] == 3, "four-site all-one polar changed")
    require(hafnian((2, 3, 4, 5), first_one) == 27, "double polar all-one value changed")


def response_layers(q, r):
    layers = [0, 0, 0, 0]
    for matching in matchings(W):
        for mask in range(8):
            layers[mask.bit_count()] += product(
                r[edge(*pair)] if mask & (1 << position) else q[edge(*pair)]
                for position, pair in enumerate(matching)
            )
    return tuple(layers)


def permanent(rows, columns, entries):
    return sum(
        product(entries[edge(row, column)] for row, column in zip(rows, assigned))
        for assigned in permutations(columns)
    )


def theta(marked, a, b, q):
    marked = tuple(sorted(marked))
    outside = tuple(x for x in W if x not in marked)
    value = 0
    for inside_pair in combinations(marked, 2):
        remaining_marked = next(x for x in marked if x not in inside_pair)
        for outside_endpoint in outside:
            remaining_outside = tuple(x for x in outside if x != outside_endpoint)
            value += (
                a[edge(*inside_pair)]
                * b[edge(remaining_marked, outside_endpoint)]
                * q[edge(*remaining_outside)]
            )
    return value + permanent(marked, outside, b)


def theta_average(alpha, q, r):
    second = {e: 2 * alpha * r[e] for e in EDGES}
    return sum(theta(marked, second, r, q) for marked in combinations(W, 3))


def deterministic_arrays(seed):
    q = {}
    r = {}
    for i, j in EDGES:
        q[(i, j)] = ((seed + 2 * i - j) % 7) - 3
        r[(i, j)] = ((2 * seed - i + 3 * j) % 9) - 4
    return q, r


def audit_bianchi_radial_comparison():
    q, r = deterministic_arrays(3)
    q0, q1, q2, q3 = response_layers(q, r)
    alpha = -Fraction(q1, q0)
    cut_sum = theta_average(alpha, q, r)
    require(alpha * q0 + q1 == 0, "selected source normalization changed")
    require(cut_sum == 8 * (alpha * q2 + q3), "twenty-cut readout changed")
    cap = {e: alpha * q[e] + r[e] for e in EDGES}
    require(hafnian(W, cap) == alpha * q2 + q3, "cap reformulation changed")

    c1 = {e: q1 * q[e] + q0 * r[e] for e in EDGES}
    c3 = {e: q3 * q[e] + q2 * r[e] for e in EDGES}
    for e in EDGES:
        left = q0 * c3[e] - q2 * c1[e]
        require(left == (q0 * q3 - q1 * q2) * q[e], ("Hankel identity", e))
        require(left == Fraction(q0 * cut_sum, 8) * q[e], ("Bianchi comparison", e))


def audit_landing_error_formula():
    q, r = deterministic_arrays(5)
    alpha = -3
    base_a = {e: 2 * alpha * r[e] for e in EDGES}
    marked = (0, 2, 5)
    outside = tuple(x for x in W if x not in marked)

    epsilon = {e: 0 for e in EDGES}
    delta = {e: 0 for e in EDGES}
    for position, inside_pair in enumerate(combinations(marked, 2), start=1):
        epsilon[edge(*inside_pair)] = position - 2
    for position, (x, y) in enumerate((pair for pair in EDGES if (pair[0] in marked) != (pair[1] in marked))):
        delta[(x, y)] = position % 5 - 2

    lifted_a = {e: base_a[e] + epsilon[e] for e in EDGES}
    lifted_b = {e: r[e] + delta[e] for e in EDGES}
    difference = theta(marked, lifted_a, lifted_b, q) - theta(marked, base_a, r, q)

    connection_error = 0
    for inside_pair in combinations(marked, 2):
        remaining = next(x for x in marked if x not in inside_pair)
        ell_lifted = 0
        ell_delta = 0
        for y in outside:
            other = tuple(x for x in outside if x != y)
            ell_lifted += lifted_b[edge(remaining, y)] * q[edge(*other)]
            ell_delta += delta[edge(remaining, y)] * q[edge(*other)]
        connection_error += epsilon[edge(*inside_pair)] * ell_lifted
        connection_error += base_a[edge(*inside_pair)] * ell_delta
    permanent_error = permanent(marked, outside, lifted_b) - permanent(marked, outside, r)
    require(difference == connection_error + permanent_error, "landing-error formula changed")


def audit_noncutwise_guard():
    q = {e: 0 for e in EDGES}
    for e in ((0, 1), (2, 3), (4, 5)):
        q[e] = 1
    u = (1, -1, 2, 0, 1, 1)
    v = (1, 2, -2, 1, -2, 1)
    r = {e: u[e[0]] * v[e[1]] + v[e[0]] * u[e[1]] for e in EDGES}
    alpha = -2
    second = {e: 2 * alpha * r[e] for e in EDGES}

    values = []
    for marked in combinations(W, 3):
        direct = theta(marked, second, r, q)
        values.append(direct)

    layers = response_layers(q, r)
    expected_values = [
        -12, -12, -12, -36, -20, 20, -28, 20, -4, -36,
        -44, -4, 20, -28, 20, -12, 20, 44, 52, 52,
    ]
    require(layers == (1, 2, 6, 12), ("guard layers", layers))
    require(alpha * layers[0] + layers[1] == 0, "guard lost selected source")
    require(alpha * layers[2] + layers[3] == 0, "guard lost cleanliness")
    require(values == expected_values, ("cutwise guard values", values))
    require(sum(values) == 0 and any(values), "cutwise cancellation guard changed")


def main():
    audit_double_polar_identity()
    audit_bianchi_radial_comparison()
    audit_landing_error_formula()
    audit_noncutwise_guard()
    print("PASS: formal double-polar defect H(H)=haf(A)A+2B on all 15 edges")
    print("PASS: reciprocal Hankel component is the q0*Q-scaled radial image of the 20-cut average")
    print("PASS: exact cut landing-error formula and clean/non-cutwise rank-two guard")


if __name__ == "__main__":
    main()
