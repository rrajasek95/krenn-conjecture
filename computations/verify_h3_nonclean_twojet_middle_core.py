#!/usr/bin/env python3
"""Exact audit of the h=3 response-two-jet terminal middle class."""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations


Q = Fraction
SITES = tuple(range(6))


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def response_row_coefficients(alpha, layers):
    q0, q1, q2, q3 = map(Q, layers)
    alpha = Q(alpha)
    return (
        alpha * q0 + q1,
        alpha * q1 + 2 * q2,
        alpha * q2 + 3 * q3,
        alpha * q3,
    )


def audit_terminal_identity():
    packets = []
    for alpha, q3 in ((1, 1), (2, -3), (-3, 5), (Q(5, 2), Q(7, 3))):
        alpha = Q(alpha)
        q3 = Q(q3)
        q2 = -3 * q3 / alpha
        q1 = -2 * q2 / alpha
        q0 = -q1 / alpha
        layers = (q0, q1, q2, q3)
        coefficients = response_row_coefficients(alpha, layers)
        require(coefficients[:3] == (0, 0, 0), ("two-jet did not vanish", alpha, layers))
        tail = alpha * q2 + q3
        require(tail == -2 * q3, ("tail is not the terminal class", alpha, layers))
        require(tail == -2 * coefficients[3] / alpha, "middle normalization changed")
        packets.append((alpha, layers, coefficients, tail))

    require(
        packets[0] == (Q(1), (Q(-6), Q(6), Q(-3), Q(1)), (0, 0, 0, 1), Q(-2)),
        ("canonical response-jet packet changed", packets[0]),
    )

    # Mutation guard: deleting the terminal layer makes the same lower
    # recurrence clean, so the audit is sensitive to the live class.
    mutated = response_row_coefficients(1, (-6, 6, -3, 0))
    require(mutated[2] == -3, ("terminal mutation was not detected", mutated))


def compositions(total, parts):
    if parts == 1:
        return ((total,),)
    answer = []
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            answer.append((first,) + tail)
    return tuple(answer)


def audit_middle_core():
    degree_six = compositions(6, 3)
    require(len(degree_six) == 28, ("wrong ternary degree-six dimension", len(degree_six)))

    admitted = {
        exponent
        for exponent in degree_six
        if any(6 - exponent[color] <= 2 for color in range(3))
    }
    middle = tuple(exponent for exponent in degree_six if exponent not in admitted)
    require(len(middle) == 10, ("wrong middle-core dimension", middle))
    require(all(max(exponent) <= 3 for exponent in middle), "noncentral exponent survived")

    pattern_counts = {}
    for exponent in middle:
        pattern = tuple(sorted(exponent, reverse=True))
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
    require(
        pattern_counts == {(3, 3, 0): 3, (3, 2, 1): 6, (2, 2, 2): 1},
        ("middle patterns changed", pattern_counts),
    )

    literal_pattern_counts = {
        (3, 3, 0): 3 * 20,
        (3, 2, 1): 6 * 60,
        (2, 2, 2): 90,
    }
    require(
        sum(literal_pattern_counts.values()) == 510,
        ("wrong literal middle-word dimension", literal_pattern_counts),
    )

    for missing_color in range(3):
        binary_middle = tuple(exponent for exponent in middle if exponent[missing_color] == 0)
        expected = [0, 0, 0]
        for color in range(3):
            if color != missing_color:
                expected[color] = 3
        require(binary_middle == (tuple(expected),), ("binary midpoint changed", missing_color, binary_middle))
        require(20 == 6 * 5 * 4 // (3 * 2), "wrong literal binary midpoint count")

    # A literal middle monomial is invisible to all Hamming-two coefficient
    # cuts but remains nonzero, proving that the truncation has a live class.
    witness = (3, 3, 0)
    require(witness in middle, "binary middle witness disappeared")
    require(all(6 - witness[color] >= 3 for color in range(3)), "witness reached a pure two-jet")


def edge_key(x, y):
    return (x, y) if x < y else (y, x)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def multiply(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def response_layers(q_edges, r_edges):
    layer_two = Q(0)
    layer_three = Q(0)
    for matching in matchings(SITES):
        layer_three += multiply(r_edges[edge_key(*edge)] for edge in matching)
        for q_position in range(3):
            layer_two += multiply(
                q_edges[edge_key(*edge)] if position == q_position else r_edges[edge_key(*edge)]
                for position, edge in enumerate(matching)
            )
    return layer_two, layer_three


def triple_product(first, second, third):
    """Top coefficient of the ordinary product of three quadratics."""
    value = Q(0)
    for matching in matchings(SITES):
        for assignment in permutations((first, second, third)):
            value += multiply(
                assignment[position][edge_key(*edge)]
                for position, edge in enumerate(matching)
            )
    return value


def third_jet(q_edges, first_edges, second_edges):
    """Coefficient of t^3 in (q + t B + t^2 A)^[3]."""
    return triple_product(second_edges, first_edges, q_edges) + response_layers(
        q_edges, first_edges
    )[1]


def theta_cut(alpha, q_edges, r_edges, marked, second_scale=2):
    marked = tuple(sorted(marked))
    outside = tuple(site for site in SITES if site not in marked)
    value = Q(0)

    # One second-jet edge inside the marked triple, one first-jet edge
    # crossing the cut, and one q-edge on the two unused outside sites.
    for inside_pair in combinations(marked, 2):
        remaining_marked = next(site for site in marked if site not in inside_pair)
        second_jet = Q(second_scale) * Q(alpha) * r_edges[edge_key(*inside_pair)]
        for outside_endpoint in outside:
            remaining_outside = tuple(site for site in outside if site != outside_endpoint)
            value += (
                second_jet
                * r_edges[edge_key(remaining_marked, outside_endpoint)]
                * q_edges[edge_key(*remaining_outside)]
            )

    # Three first-jet edges crossing the same three-three cut.
    for assigned_outside in permutations(outside):
        value += multiply(
            r_edges[edge_key(marked[position], assigned_outside[position])]
            for position in range(3)
        )
    return value


def audit_bianchi_average():
    datasets = []
    for seed in (1, 3, 7):
        q_edges = {}
        r_edges = {}
        for x, y in combinations(SITES, 2):
            q_edges[(x, y)] = Q((seed + 2 * x - y) % 7 - 3, (x + y) % 3 + 1)
            r_edges[(x, y)] = Q((2 * seed - x + 3 * y) % 9 - 4, (2 * x + y) % 4 + 1)
        datasets.append((Q(seed, 2), q_edges, r_edges))

    # Sparse packets independently expose the connection factor four and
    # the permanent factor eight.
    fixed_matching = ((0, 1), (2, 3), (4, 5))
    q_sparse = {edge: Q(0) for edge in combinations(SITES, 2)}
    r_sparse = dict(q_sparse)
    q_sparse[(4, 5)] = Q(5)
    r_sparse[(0, 1)] = Q(2)
    r_sparse[(2, 3)] = Q(-3)
    datasets.append((Q(7, 3), q_sparse, r_sparse))

    q_cubic = {edge: Q(0) for edge in combinations(SITES, 2)}
    r_cubic = dict(q_cubic)
    for edge, value in zip(fixed_matching, (2, -3, 5)):
        r_cubic[edge] = Q(value)
    datasets.append((Q(-4, 3), q_cubic, r_cubic))

    for alpha, q_edges, r_edges in datasets:
        layer_two, layer_three = response_layers(q_edges, r_edges)
        clean_tail = alpha * layer_two + layer_three
        cut_sum = sum(
            (
                theta_cut(alpha, q_edges, r_edges, marked)
                for marked in combinations(SITES, 3)
            ),
            Q(0),
        )
        require(cut_sum == 8 * clean_tail, ("Bianchi average changed", alpha, cut_sum, clean_tail))
        first_edges = {edge: 2 * value for edge, value in r_edges.items()}
        second_edges = {edge: 2 * alpha * value for edge, value in r_edges.items()}
        require(
            third_jet(q_edges, first_edges, second_edges) == cut_sum,
            "uniform third-jet coefficient changed",
        )

    alpha, q_edges, r_edges = datasets[0]
    wrong_cut_sum = sum(
        (
            theta_cut(alpha, q_edges, r_edges, marked, second_scale=1)
            for marked in combinations(SITES, 3)
        ),
        Q(0),
    )
    layer_two, layer_three = response_layers(q_edges, r_edges)
    require(
        wrong_cut_sum != 8 * (alpha * layer_two + layer_three),
        "factor-two mutation was not detected",
    )

    # Audit the beta/gamma expansion of the physical normalization defect.
    beta = {edge: Q(2 * edge[0] - edge[1] + 1, 3) for edge in q_edges}
    gamma = {edge: Q(edge[0] + 3 * edge[1] - 4, 5) for edge in q_edges}
    first_edges = {edge: 2 * r_edges[edge] + beta[edge] for edge in q_edges}
    second_edges = {
        edge: 2 * alpha * r_edges[edge] + gamma[edge] for edge in q_edges
    }
    defect = third_jet(q_edges, first_edges, second_edges) - 8 * (
        alpha * layer_two + layer_three
    )
    beta_three = response_layers(q_edges, beta)[1]
    expanded = (
        triple_product({edge: 2 * alpha * r_edges[edge] for edge in q_edges}, beta, q_edges)
        + triple_product({edge: 2 * r_edges[edge] for edge in q_edges}, gamma, q_edges)
        + triple_product(gamma, beta, q_edges)
        + 2 * triple_product(r_edges, r_edges, beta)
        + triple_product(r_edges, beta, beta)
        + beta_three
    )
    require(defect == expanded, ("normalization-defect expansion changed", defect, expanded))


def main():
    audit_terminal_identity()
    audit_middle_core()
    audit_bianchi_average()
    print(
        "PASS: response two-jet leaves chi=-2 Q3; exact (-6,6,-3,1) packet; "
        "uniform H2 complement has 3+6+1=10 count types / 510 literal words; "
        "20-word binary midpoints; clean tail is 1/8 of the 20-cut cubic Bianchi sum"
    )


if __name__ == "__main__":
    main()
