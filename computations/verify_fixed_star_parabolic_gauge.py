#!/usr/bin/env python3
"""Exact audit of parabolic star tangents versus expansion gauges.

The one-row equation F_q(z)=e_0^J has a local parabolic symmetry at every
site.  At the quotient site j its infinitesimal action applies an arbitrary
endomorphism of V_j/Ce_0 to the known Psi-kernel vector.  This script checks,
over the integers, that applying such an endomorphism to an expansion gauge
is exactly another expansion gauge.

It also constructs a nontrivial five-site common-power star solution with a
Koszul cancellation, verifies F_q(z)=e_0^J by complete matching expansion,
and checks all four quotient-endomorphism directions inside Psi_(1,0).
"""

from __future__ import annotations

from itertools import combinations, product

from sympy import Matrix


Q = 3
J = tuple(range(5))
R = 0
QUOTIENT_COLORS = (1, 2)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def zero_matrix():
    return [[0 for _b in range(Q)] for _a in range(Q)]


def bridge_source():
    """A five-site one-row solution with a genuine transfer cancellation."""

    q = {pair: zero_matrix() for pair in combinations(J, 2)}
    # q_12=e0 e0-e1 e2, q_02=e0 e2, followed by the pure tail q_34.
    q[1, 2][0][0] = 1
    q[1, 2][1][2] = -1
    q[0, 2][0][2] = 1
    q[3, 4][0][0] = 1
    z = [[0 for _color in range(Q)] for _site in J]
    z[0][0] = 1
    z[1][1] = 1
    return q, z


def qentry(q, u, v, a, b):
    if u < v:
        return q[u, v][a][b]
    return q[v, u][b][a]


def hafnian_coefficient(q, vertices, coloring):
    local = dict(zip(vertices, coloring, strict=True))
    answer = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for u, v in matching:
            term *= qentry(q, u, v, local[u], local[v])
        answer += term
    return answer


def hafnian_tensor(q, vertices):
    vertices = tuple(vertices)
    return {
        coloring: hafnian_coefficient(q, vertices, coloring)
        for coloring in product(range(Q), repeat=len(vertices))
    }


def star_output(q, z):
    answer = {}
    for coloring in product(range(Q), repeat=len(J)):
        value = 0
        for site in J:
            outside = tuple(v for v in J if v != site)
            outside_coloring = tuple(coloring[v] for v in outside)
            value += z[site][coloring[site]] * hafnian_coefficient(
                q, outside, outside_coloring
            )
        answer[coloring] = value
    return answer


def metadata(j):
    answer = [("u", color) for color in QUOTIENT_COLORS]
    rest = tuple(v for v in J if v != j)
    for i, k in combinations(rest, 2):
        for color_i, color_j, color_k in product(
            range(Q), QUOTIENT_COLORS, range(Q)
        ):
            answer.append(("t", i, k, color_i, color_j, color_k))
    return tuple(answer)


def kernel_vector(q, z, j):
    """The domain vector in equation (7) of the dichotomy note."""

    vector = {item: 0 for item in metadata(j)}
    for color in QUOTIENT_COLORS:
        vector["u", color] = z[j][color]
    rest = tuple(v for v in J if v != j)
    for i, k in combinations(rest, 2):
        for color_i, color_j, color_k in product(
            range(Q), QUOTIENT_COLORS, range(Q)
        ):
            vector["t", i, k, color_i, color_j, color_k] = (
                z[i][color_i] * qentry(q, j, k, color_j, color_k)
                + qentry(q, j, i, color_j, color_i) * z[k][color_k]
            )
    return vector


def expansion_gauge(q, w, j):
    """G_j(w), with w[site] a two-vector in the quotient at j."""

    vector = {item: 0 for item in metadata(j)}
    rest = tuple(v for v in J if v != j)
    for offset, color_j in enumerate(QUOTIENT_COLORS):
        vector["u", color_j] = sum(w[site][offset] for site in rest)
    for i, k in combinations(rest, 2):
        for color_i, color_j, color_k in product(
            range(Q), QUOTIENT_COLORS, range(Q)
        ):
            offset = QUOTIENT_COLORS.index(color_j)
            vector["t", i, k, color_i, color_j, color_k] = -(
                w[i][offset] + w[k][offset]
            ) * qentry(q, i, k, color_i, color_k)
    return vector


def apply_quotient_endomorphism(vector, matrix, j):
    """Apply a 2x2 matrix to every barred-j factor of a domain vector."""

    answer = {item: 0 for item in metadata(j)}
    for output_offset, output_color in enumerate(QUOTIENT_COLORS):
        for input_offset, input_color in enumerate(QUOTIENT_COLORS):
            answer["u", output_color] += (
                matrix[output_offset][input_offset]
                * vector["u", input_color]
            )
    rest = tuple(v for v in J if v != j)
    for i, k in combinations(rest, 2):
        for color_i, output_color, color_k in product(
            range(Q), QUOTIENT_COLORS, range(Q)
        ):
            output_offset = QUOTIENT_COLORS.index(output_color)
            for input_offset, input_color in enumerate(QUOTIENT_COLORS):
                answer["t", i, k, color_i, output_color, color_k] += (
                    matrix[output_offset][input_offset]
                    * vector["t", i, k, color_i, input_color, color_k]
                )
    return answer


def apply_to_w(w, matrix):
    answer = {}
    for site, value in w.items():
        answer[site] = tuple(
            sum(matrix[row][column] * value[column] for column in range(2))
            for row in range(2)
        )
    return answer


def psi_image(q, vector, j):
    """Apply Psi over the integers, returning its sparse output tensor."""

    c_j = hafnian_tensor(q, tuple(v for v in J if v != j))
    d = {
        tuple(sorted((i, j, k))): hafnian_tensor(
            q, tuple(v for v in J if v not in (i, j, k))
        )
        for i, k in combinations(tuple(v for v in J if v != j), 2)
    }
    answer = {}
    for coloring in product(range(Q), repeat=len(J)):
        if coloring[j] == R:
            continue
        rest_coloring = tuple(coloring[v] for v in J if v != j)
        value = vector["u", coloring[j]] * c_j[rest_coloring]
        for i, k in combinations(tuple(v for v in J if v != j), 2):
            outside = tuple(v for v in J if v not in (i, j, k))
            outside_coloring = tuple(coloring[v] for v in outside)
            value += vector[
                "t", i, k, coloring[i], coloring[j], coloring[k]
            ] * d[tuple(sorted((i, j, k)))][outside_coloring]
        if value:
            answer[coloring] = value
    return answer


def column(vector, ordering):
    return [vector[item] for item in ordering]


def main():
    q, z = bridge_source()
    output = star_output(q, z)
    assert output == {
        coloring: int(coloring == (R,) * len(J)) for coloring in output
    }

    j = 1
    x = kernel_vector(q, z, j)
    w = {site: (0, 0) for site in J if site != j}
    w[0] = (1, 0)
    assert x == expansion_gauge(q, w, j)
    assert not psi_image(q, x, j)

    endomorphisms = (
        ((1, 0), (0, 0)),
        ((0, 1), (0, 0)),
        ((0, 0), (1, 0)),
        ((0, 0), (0, 1)),
    )
    parabolic = []
    for matrix in endomorphisms:
        tangent = apply_quotient_endomorphism(x, matrix, j)
        predicted = expansion_gauge(q, apply_to_w(w, matrix), j)
        assert tangent == predicted
        assert not psi_image(q, tangent, j)
        parabolic.append(tangent)

    ordering = metadata(j)
    gauges = []
    for site in J:
        if site == j:
            continue
        for offset in range(2):
            basis_w = {other: (0, 0) for other in J if other != j}
            value = [0, 0]
            value[offset] = 1
            basis_w[site] = tuple(value)
            gauges.append(expansion_gauge(q, basis_w, j))

    gauge_matrix = Matrix.hstack(*(
        Matrix(column(vector, ordering)) for vector in gauges
    ))
    augmented = Matrix.hstack(
        gauge_matrix,
        *(Matrix(column(vector, ordering)) for vector in parabolic),
    )
    parabolic_matrix = Matrix.hstack(*(
        Matrix(column(vector, ordering)) for vector in parabolic
    ))
    assert gauge_matrix.rank() == augmented.rank()
    # The chosen bridge has a one-dimensional span of w_i in the two-space,
    # so End(bar V_j) produces exactly 2*1 independent tangent vectors.
    assert parabolic_matrix.rank() == 2

    # The simultaneous stabilizer of all three pure target rows is diagonal:
    # at one site its Lie algebra has dimension three, not the seven of one
    # line parabolic.  Across five sites, the three product-one constraints
    # leave 3(|J|-1)=12 dimensions.
    simultaneous_stabilizer_dimension = 3 * len(J) - 3
    assert simultaneous_stabilizer_dimension == 12

    print(
        "fixed-star parabolic audit: PASS; "
        "exact J=5 bridge, parabolic_rank=2, "
        f"gauge_rank={gauge_matrix.rank()}, "
        f"augmented_rank={augmented.rank()}, "
        f"simultaneous_stabilizer_dim={simultaneous_stabilizer_dimension}"
    )


if __name__ == "__main__":
    main()
