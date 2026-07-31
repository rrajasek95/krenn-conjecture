#!/usr/bin/env python3
"""Exact audit for the diagonal-anchor four-cut leakage transgression."""

from fractions import Fraction as Q


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def zero_matrix():
    return [[Q(0) for _ in range(3)] for _ in range(3)]


def eye_cell(c):
    out = zero_matrix()
    out[c][c] = Q(1)
    return out


def transpose(a):
    return [[a[j][i] for j in range(3)] for i in range(3)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(3)] for i in range(3)]


def scale(s, a):
    return [[s * a[i][j] for j in range(3)] for i in range(3)]


def mul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(3)), Q(0)) for j in range(3)]
        for i in range(3)
    ]


def equal(a, b):
    return all(a[i][j] == b[i][j] for i in range(3) for j in range(3))


def delta_frame(x, y, c):
    e = eye_cell(c)
    return scale(Q(-1), add(mul(transpose(x), e), mul(e, y)))


def phi_from_deltas(deltas, a):
    out = zero_matrix()
    for i in range(3):
        for j in range(3):
            left = sum(
                (deltas[k][i][k] * a[k][j] for k in range(3) if k != i),
                Q(0),
            )
            right = sum(
                (a[i][k] * deltas[k][k][j] for k in range(3) if k != j),
                Q(0),
            )
            out[i][j] = -left - right - a[i][j] * deltas[j][j][j]
    return out


def two_cycle(a, m, i, j):
    return a[j][i] * m[i][j] + a[i][j] * m[j][i]


def three_cycle(a, m, i, j, k):
    return (
        a[j][k] * a[k][i] * m[i][j]
        + a[k][i] * a[i][j] * m[j][k]
        + a[i][j] * a[j][k] * m[k][i]
    )


def target_four_cut_coefficients(base_colours, cut_colour, site_tangent):
    """Enumerate the constant/t parts of every target colour after the cut."""
    missing = [
        site for site, colour in enumerate(base_colours) if colour != cut_colour
    ]
    require(len(missing) == 4, "the mixed word is not 2+2+2")
    output = []
    for target_colour in range(3):
        # The coefficient of all four epsilon variables is the product of
        # their direction coordinates times the two uncut site factors.
        direction_product = Q(1)
        for _site in missing:
            direction_product *= Q(target_colour == cut_colour)
        uncut = [site for site in range(6) if site not in missing]
        constant = direction_product
        for site in uncut:
            constant *= Q(base_colours[site] == target_colour)
        linear = Q(0)
        for varied_site in uncut:
            term = direction_product * site_tangent[varied_site][target_colour]
            for site in uncut:
                if site != varied_site:
                    term *= Q(base_colours[site] == target_colour)
            linear += term
        output.append((constant, linear))
    return output


def check_fixture(x, y, a, site_tangent, f):
    base_colours = [0, 0, 1, 1, 2, 2]
    deltas = []
    for c in range(3):
        target_coefficients = target_four_cut_coefficients(
            base_colours, c, site_tangent
        )
        for d, (constant_d, linear_d) in enumerate(target_coefficients):
            if d != c:
                require(
                    constant_d == 0 and linear_d == 0,
                    "four-cut retained the wrong target colour",
                )
        constant, tau = target_coefficients[c]
        require(constant == 1, "raw diagonal-anchor four-cut is not E_cc")

        e = eye_cell(c)
        raw_derivative = scale(tau, e)
        normalized_derivative = add(raw_derivative, delta_frame(x, y, c))
        delta = sub(normalized_derivative, raw_derivative)
        require(equal(delta, delta_frame(x, y, c)), "tau did not cancel")

        for i in range(3):
            for j in range(3):
                if i != c and j != c:
                    require(delta[i][j] == 0, "frame defect escaped row/column c")
        for i in range(3):
            if i != c:
                require(delta[i][c] == -x[c][i], "X index/sign mismatch")
                require(delta[c][i] == -y[c][i], "Y index/sign mismatch")
        require(delta[c][c] == -x[c][c] - y[c][c], "diagonal sum mismatch")
        deltas.append(delta)

    k_connection = add(mul(transpose(x), a), mul(a, y))
    phi = phi_from_deltas(deltas, a)
    d = zero_matrix()
    for i in range(3):
        d[i][i] = x[i][i]
    reconstructed = add(phi, sub(mul(d, a), mul(a, d)))
    require(equal(k_connection, reconstructed), "connection reconstruction failed")

    leakage = scale(f, k_connection)
    phi_scaled = scale(f, phi)
    for i in range(3):
        for j in range(i + 1, 3):
            require(
                two_cycle(a, leakage, i, j) == two_cycle(a, phi_scaled, i, j),
                "two-cycle holonomy did not descend to anchor defects",
            )
    for i, j, k in ((0, 1, 2), (0, 2, 1), (1, 0, 2)):
        require(
            three_cycle(a, leakage, i, j, k)
            == three_cycle(a, phi_scaled, i, j, k),
            "three-cycle holonomy did not descend to anchor defects",
        )

    gauge = [Q(5), Q(-2), Q(7)]
    x_gauge = [row[:] for row in x]
    y_gauge = [row[:] for row in y]
    for i in range(3):
        x_gauge[i][i] += gauge[i]
        y_gauge[i][i] -= gauge[i]
    gauge_deltas = [delta_frame(x_gauge, y_gauge, c) for c in range(3)]
    require(all(equal(deltas[c], gauge_deltas[c]) for c in range(3)), "gauge changed defects")
    gauge_connection = add(mul(transpose(x_gauge), a), mul(a, y_gauge))
    for i in range(3):
        for j in range(i + 1, 3):
            require(
                two_cycle(a, gauge_connection, i, j)
                == two_cycle(a, k_connection, i, j),
                "gauge changed two-cycle",
            )
    require(
        three_cycle(a, gauge_connection, 0, 1, 2)
        == three_cycle(a, k_connection, 0, 1, 2),
        "gauge changed three-cycle",
    )

    mutated = [row[:] for row in phi]
    mutated[0][1] += Q(1)
    require(
        not equal(k_connection, add(mutated, sub(mul(d, a), mul(a, d)))),
        "mutation failed to detect a Phi entry error",
    )


def main():
    fixtures = [
        (
            [[Q(2), Q(-1), Q(3)], [Q(4), Q(1), Q(-2)], [Q(5), Q(6), Q(-3)]],
            [[Q(-2), Q(7), Q(1)], [Q(3), Q(-4), Q(5)], [Q(6), Q(-1), Q(2)]],
            [[Q(1), Q(2), Q(-3)], [Q(4), Q(-2), Q(5)], [Q(7), Q(3), Q(6)]],
            [
                [Q(1), Q(-1), Q(2)],
                [Q(3), Q(0), Q(-2)],
                [Q(-4), Q(5), Q(1)],
                [Q(2), Q(7), Q(-3)],
                [Q(6), Q(-5), Q(4)],
                [Q(-2), Q(3), Q(8)],
            ],
            Q(11),
        ),
        (
            [[Q(0), Q(2), Q(-1)], [Q(3), Q(0), Q(4)], [Q(-2), Q(5), Q(0)]],
            [[Q(0), Q(-3), Q(6)], [Q(1), Q(0), Q(-4)], [Q(7), Q(2), Q(0)]],
            [[Q(0), Q(5), Q(2)], [Q(-3), Q(0), Q(7)], [Q(4), Q(-1), Q(0)]],
            [[Q(i - j) for j in range(3)] for i in range(6)],
            Q(-3),
        ),
    ]
    for fixture in fixtures:
        check_fixture(*fixture)

    print(
        "diagonal-anchor four-cut leakage holonomy transgression: PASS; "
        "frame defects and two-/three-cycle descent exact"
    )


if __name__ == "__main__":
    main()
