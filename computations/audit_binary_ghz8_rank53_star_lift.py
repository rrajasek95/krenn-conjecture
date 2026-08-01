#!/usr/bin/env python3
"""Independently audit the exact rank-53 GHZ8 source and its star lift.

This checker deliberately imports no project module.  It reconstructs the
26-parameter chart, verifies its 256 identities in an independent Laurent
engine, specializes over Q, rebuilds the deletion-(3,4) differential, and
certifies the two-dimensional star kernel which replaces the collapsed
mixed endpoint packet.

Standard library only; all checks remain live under ``python3 -O`` and
``python3 -I -S``.
"""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product


VERTICES = tuple(range(8))
COLOURS = (0, 1)
WORDS8 = tuple(product(COLOURS, repeat=8))
DELETED = (3, 4)
REMAINING = tuple(vertex for vertex in VERTICES if vertex not in DELETED)
RESIDUAL_WORDS = tuple(product(COLOURS, repeat=6))
RESIDUAL_COLUMNS = tuple(
    (u, v, a, b)
    for u, v in combinations(REMAINING, 2)
    for a, b in product(COLOURS, repeat=2)
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class Laurent:
    """Sparse Laurent polynomials over Q, independent of the source checker."""

    __slots__ = ("coefficients", "variable_count")

    def __init__(self, coefficients, variable_count):
        self.variable_count = variable_count
        self.coefficients = {
            tuple(exponent): Q(coefficient)
            for exponent, coefficient in coefficients.items()
            if coefficient
        }

    @classmethod
    def constant(cls, value, variable_count):
        return cls(
            {(0,) * variable_count: Q(value)} if value else {}, variable_count
        )

    @classmethod
    def variable(cls, index, variable_count):
        exponent = [0] * variable_count
        exponent[index] = 1
        return cls({tuple(exponent): Q(1)}, variable_count)

    def coerce(self, other):
        if isinstance(other, Laurent):
            require(
                other.variable_count == self.variable_count,
                "incompatible Laurent rings",
            )
            return other
        return Laurent.constant(other, self.variable_count)

    def __bool__(self):
        return bool(self.coefficients)

    def __neg__(self):
        return Laurent(
            {exponent: -coefficient for exponent, coefficient in self.coefficients.items()},
            self.variable_count,
        )

    def __add__(self, other):
        other = self.coerce(other)
        answer = dict(self.coefficients)
        for exponent, coefficient in other.coefficients.items():
            answer[exponent] = answer.get(exponent, Q(0)) + coefficient
            if not answer[exponent]:
                del answer[exponent]
        return Laurent(answer, self.variable_count)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        answer = {}
        for left_exponent, left_coefficient in self.coefficients.items():
            for right_exponent, right_coefficient in other.coefficients.items():
                exponent = tuple(
                    left + right
                    for left, right in zip(left_exponent, right_exponent)
                )
                answer[exponent] = (
                    answer.get(exponent, Q(0))
                    + left_coefficient * right_coefficient
                )
                if not answer[exponent]:
                    del answer[exponent]
        return Laurent(answer, self.variable_count)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        require(len(other.coefficients) == 1, "denominator is not a monomial")
        ((denominator_exponent, denominator_coefficient),) = (
            other.coefficients.items()
        )
        return Laurent(
            {
                tuple(
                    left - right
                    for left, right in zip(exponent, denominator_exponent)
                ): coefficient / denominator_coefficient
                for exponent, coefficient in self.coefficients.items()
            },
            self.variable_count,
        )

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __eq__(self, other):
        return self.coefficients == self.coerce(other).coefficients


DEFAULT_PARAMETERS = {
    "x1600": Q(-1, 20),
    "x5700": Q(1, 60),
    "x5701": Q(49, 1000),
    "x0400": Q(-3, 2),
    "x1611": Q(6, 5),
    "x3700": Q(7, 5),
    "x2601": Q(-23, 50),
    "x0500": Q(-43, 125),
    "x0600": Q(-1, 2),
    "x0610": Q(3, 40),
    "x6701": Q(27, 100),
    "x0611": Q(7, 8),
    "x6710": Q(1, 5),
    "x4610": Q(-73, 50),
    "x0601": Q(7, 10),
    "x0510": Q(-47, 30),
    "x2600": Q(13, 6),
    "x5711": Q(-59, 24),
    "x0311": Q(-137, 50),
    "x5601": Q(-47, 24),
    "x6711": Q(-137, 2000),
    "x6700": Q(-41, 60),
    "x0700": Q(-3),
    "x0711": Q(-11, 4),
    "x0701": Q(9, 4),
    "x0710": Q(10),
}


def cell(name):
    require(len(name) == 5 and name[0] == "x", f"bad cell name {name}")
    answer = tuple(int(character) for character in name[1:])
    require(answer[0] < answer[1], f"bad oriented cell {name}")
    return answer


def build_chart(parameters):
    """Reconstruct the 45 cells from the 26 independent parameters."""

    require(set(parameters) == set(DEFAULT_PARAMETERS), "parameter set changed")
    require(all(parameters.values()), "a chart parameter is zero")
    cells = {cell(name): value for name, value in parameters.items()}

    def get(name):
        return cells[cell(name)]

    def put(name, value):
        cells[cell(name)] = value

    put("x2411", 1 / (get("x0311") * get("x1611") * get("x5711")))
    put("x1500", 1 / (get("x0400") * get("x2600") * get("x3700")))

    put("x1201", -get("x1600") * get("x2411") / get("x4610"))
    put("x1200", -get("x1500") * get("x2601") / get("x5601"))
    put("x1401", -get("x1200") * get("x4610") / get("x2600"))
    put("x2611", -get("x1201") * get("x5601") / get("x1500"))
    put("x4611", -get("x1401") * get("x2601") / get("x1200"))

    put("x0101", -get("x0500") * get("x1611") / get("x5601"))
    put("x0111", -get("x0510") * get("x1611") / get("x5601"))
    put("x1710", -get("x1611") * get("x5700") / get("x5601"))
    put("x1711", -get("x1611") * get("x5701") / get("x5601"))

    put(
        "x0201",
        -(
            get("x0500") * get("x1201") * get("x4610")
            + get("x0500") * get("x1600") * get("x2411")
            + get("x0600") * get("x1500") * get("x2411")
        )
        / (get("x1500") * get("x4610")),
    )
    put(
        "x0211",
        -(
            get("x0510") * get("x1201") * get("x4610")
            + get("x0510") * get("x1600") * get("x2411")
            + get("x0610") * get("x1500") * get("x2411")
        )
        / (get("x1500") * get("x4610")),
    )
    put(
        "x0100",
        -(
            get("x0201") * get("x1401") * get("x5601")
            + get("x0201") * get("x1500") * get("x4611")
            + get("x0500") * get("x1201") * get("x4611")
            + get("x0500") * get("x1401") * get("x2611")
            + get("x0601") * get("x1500") * get("x2411")
        )
        / (get("x2411") * get("x5601")),
    )
    put(
        "x0110",
        -(
            get("x0211") * get("x1401") * get("x5601")
            + get("x0211") * get("x1500") * get("x4611")
            + get("x0510") * get("x1201") * get("x4611")
            + get("x0510") * get("x1401") * get("x2611")
            + get("x0611") * get("x1500") * get("x2411")
        )
        / (get("x2411") * get("x5601")),
    )
    put(
        "x2710",
        -(
            get("x1201") * get("x4610") * get("x5700")
            + get("x1500") * get("x2411") * get("x6700")
            + get("x1600") * get("x2411") * get("x5700")
        )
        / (get("x1500") * get("x4610")),
    )
    put(
        "x2711",
        -(
            get("x1201") * get("x4610") * get("x5701")
            + get("x1500") * get("x2411") * get("x6701")
            + get("x1600") * get("x2411") * get("x5701")
        )
        / (get("x1500") * get("x4610")),
    )
    put(
        "x1700",
        -(
            get("x1201") * get("x4611") * get("x5700")
            + get("x1401") * get("x2611") * get("x5700")
            + get("x1401") * get("x2710") * get("x5601")
            + get("x1500") * get("x2411") * get("x6710")
            + get("x1500") * get("x2710") * get("x4611")
        )
        / (get("x2411") * get("x5601")),
    )
    put(
        "x1701",
        -(
            get("x1201") * get("x4611") * get("x5701")
            + get("x1401") * get("x2611") * get("x5701")
            + get("x1401") * get("x2711") * get("x5601")
            + get("x1500") * get("x2411") * get("x6711")
            + get("x1500") * get("x2711") * get("x4611")
        )
        / (get("x2411") * get("x5601")),
    )

    require(len(cells) == 45, "chart support changed")
    require(all(cells.values()), "chart acquired a zero cell")
    return cells


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def matching_coefficient(cells, vertices, assignment):
    answer = Q(0)
    for matching in perfect_matchings(tuple(vertices)):
        term = Q(1)
        for u, v in matching:
            term *= cells.get((u, v, assignment[u], assignment[v]), 0)
        answer += term
    return answer


def verify_ghz8(cells):
    for word in WORDS8:
        assignment = dict(zip(VERTICES, word))
        expected = Q(1) if len(set(word)) == 1 else Q(0)
        require(
            matching_coefficient(cells, VERTICES, assignment) == expected,
            f"GHZ8 coefficient failed at {word}",
        )


def differential_matrix(cells):
    matrix = []
    for word in RESIDUAL_WORDS:
        assignment = dict(zip(REMAINING, word))
        row = []
        for u, v, a, b in RESIDUAL_COLUMNS:
            if (assignment[u], assignment[v]) != (a, b):
                row.append(Q(0))
                continue
            rest = tuple(vertex for vertex in REMAINING if vertex not in (u, v))
            row.append(matching_coefficient(cells, rest, assignment))
        matrix.append(row)
    return matrix


def field_rank(matrix):
    rows = [list(row) for row in matrix]
    height = len(rows)
    width = len(rows[0]) if rows else 0
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, height) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        for row in range(rank + 1, height):
            if not rows[row][column]:
                continue
            multiplier = rows[row][column] / pivot_value
            rows[row] = [
                left - multiplier * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
        if rank == height:
            break
    return rank


def apply_matrix(matrix, vector):
    return [
        sum(entry * coordinate for entry, coordinate in zip(row, vector))
        for row in matrix
    ]


def endpoint_vectors(cells, endpoint, fixed_colour):
    answer = {}
    for residual in REMAINING:
        if residual < endpoint:
            answer[residual] = tuple(
                cells.get((residual, endpoint, colour, fixed_colour), Q(0))
                for colour in COLOURS
            )
        else:
            answer[residual] = tuple(
                cells.get((endpoint, residual, fixed_colour, colour), Q(0))
                for colour in COLOURS
            )
    return answer


def pair_packet(left, right):
    return [
        left[u][a] * right[v][b] + right[u][a] * left[v][b]
        for u, v, a, b in RESIDUAL_COLUMNS
    ]


def residual_source_vector(cells):
    return [cells.get(column, Q(0)) for column in RESIDUAL_COLUMNS]


def star_vector(h, centre, column):
    answer = []
    for u, v, a, b in RESIDUAL_COLUMNS:
        if v == centre:
            answer.append(h[u][a] * column[b])
        elif u == centre:
            answer.append(column[a] * h[v][b])
        else:
            answer.append(Q(0))
    return answer


def gauge_vectors(cells):
    """Basis for sum(lambda_r)=0 and G(lambda)_uv=(lambda_u+lambda_v)M_uv."""

    gauges = []
    anchor = REMAINING[-1]
    for vertex in REMAINING[:-1]:
        weights = {residual: Q(0) for residual in REMAINING}
        weights[vertex] = Q(1)
        weights[anchor] = Q(-1)
        gauges.append(
            [
                (weights[u] + weights[v]) * cells.get((u, v, a, b), Q(0))
                for u, v, a, b in RESIDUAL_COLUMNS
            ]
        )
    return gauges


def column_rank(vectors):
    if not vectors:
        return 0
    return field_rank([list(row) for row in zip(*vectors)])


def four_site_cofactor(cells, u, centre, assignment):
    rest = tuple(
        vertex for vertex in REMAINING if vertex not in (u, centre)
    )
    return matching_coefficient(cells, rest, assignment)


def star_factor(cells, h, centre, assignment):
    """The F_h factor in dPsi(S_column(h)) = column[x_centre] F_h."""

    return sum(
        h[vertex][assignment[vertex]]
        * four_site_cofactor(cells, vertex, centre, assignment)
        for vertex in REMAINING
        if vertex != centre
    )


def live_off_star_graph(cells, centre):
    vertices = tuple(vertex for vertex in REMAINING if vertex != centre)
    neighbours = {vertex: set() for vertex in vertices}
    for u, v in combinations(vertices, 2):
        if any(cells.get((u, v, a, b), Q(0)) for a, b in product(COLOURS, repeat=2)):
            neighbours[u].add(v)
            neighbours[v].add(u)
    return vertices, neighbours


def connected_nonbipartite(vertices, neighbours):
    colours = {vertices[0]: 0}
    stack = [vertices[0]]
    odd_cycle = False
    while stack:
        vertex = stack.pop()
        for neighbour in neighbours[vertex]:
            if neighbour not in colours:
                colours[neighbour] = 1 - colours[vertex]
                stack.append(neighbour)
            elif colours[neighbour] == colours[vertex]:
                odd_cycle = True
    return len(colours) == len(vertices) and odd_cycle


def verify_star_lift(cells, differential):
    p, q = DELETED
    U = {colour: endpoint_vectors(cells, p, colour) for colour in COLOURS}
    V = {colour: endpoint_vectors(cells, q, colour) for colour in COLOURS}
    W = {
        (a, b): cells.get((p, q, a, b), Q(0))
        for a, b in product(COLOURS, repeat=2)
    }
    M = residual_source_vector(cells)
    P = [
        entry + W[0, 1] * source_entry / 3
        for entry, source_entry in zip(pair_packet(U[0], V[1]), M)
    ]
    Q_packet = [
        entry + W[1, 0] * source_entry / 3
        for entry, source_entry in zip(pair_packet(U[1], V[0]), M)
    ]

    centre = 7
    e0 = (Q(1), Q(0))
    e1 = (Q(0), Q(1))
    S0 = star_vector(V[1], centre, e0)
    S1 = star_vector(V[1], centre, e1)

    require(U[0][centre] == (Q(7, 5), Q(0)), "U0 centre changed")
    require(P == [Q(7, 5) * entry for entry in S0], "P is not (7/5)S(e0)")
    require(not any(Q_packet), "Q is not zero")
    require(not any(apply_matrix(differential, S0)), "S(e0) left the kernel")

    # Since dPsi(S_u(h))(x)=u[x_z]F_h(x without z), S(e0) in the
    # kernel forces F_h=0 on all 2^5 words.  Check that factor directly,
    # then obtain the transverse S(e1) direction.
    for word in RESIDUAL_WORDS:
        assignment = dict(zip(REMAINING, word))
        require(
            star_factor(cells, V[1], centre, assignment) == 0,
            f"star factor nonzero at {word}",
        )
    require(not any(apply_matrix(differential, S1)), "S(e1) left the kernel")

    gauges = gauge_vectors(cells)
    require(all(not any(apply_matrix(differential, gauge)) for gauge in gauges),
            "a gauge vector left the kernel")
    require(column_rank(gauges) == 5, "gauge rank is not five")
    require(column_rank(gauges + [S0]) == 6, "first star class was absorbed")
    require(column_rank(gauges + [S0, S1]) == 7,
            "two star columns are not independent modulo gauge")
    require(60 - field_rank(differential) == 7, "kernel nullity is not seven")

    vertices, neighbours = live_off_star_graph(cells, centre)
    require(connected_nonbipartite(vertices, neighbours),
            "off-star live graph is not connected and nonbipartite")

    # A gauge supported on the centre star obeys lambda_u+lambda_v=0 on
    # every live off-star edge, together with sum lambda=0.  Full rank six
    # of these equations says only lambda=0 is possible.
    weight_columns = {vertex: index for index, vertex in enumerate(REMAINING)}
    constraints = []
    for u, v in combinations(vertices, 2):
        if v not in neighbours[u]:
            continue
        row = [Q(0)] * 6
        row[weight_columns[u]] = Q(1)
        row[weight_columns[v]] = Q(1)
        constraints.append(row)
    constraints.append([Q(1)] * 6)
    require(field_rank(constraints) == 6,
            "a nonzero star-supported gauge remains")


def main():
    parameter_names = tuple(sorted(DEFAULT_PARAMETERS))
    symbolic_parameters = {
        name: Laurent.variable(index, len(parameter_names))
        for index, name in enumerate(parameter_names)
    }
    require(len(parameter_names) == 26, "parameter count changed")
    verify_ghz8(build_chart(symbolic_parameters))

    cells = build_chart(DEFAULT_PARAMETERS)
    verify_ghz8(cells)
    differential = differential_matrix(cells)
    require(field_rank(differential) == 53, "full differential rank changed")
    require(field_rank(differential[1:-1]) == 51, "mixed rank changed")
    verify_star_lift(cells, differential)

    print("verified the independent 26-parameter Laurent GHZ8 chart")
    print("verified the rational deletion-(3,4) ranks 53/51")
    print("verified P=(7/5)S(e0), Q=0, and S(e1) in the kernel")
    print("verified kernel = five gauges + two star columns")
    print("verified the connected-nonbipartite off-star gauge obstruction")


if __name__ == "__main__":
    main()
