#!/usr/bin/env python3
"""Exact lightweight audit of the two-chart selector sum-channel guard."""


if not __debug__:
    raise RuntimeError("run without -O: this exact checker uses assertions")


def add(left, right):
    return tuple(x + y for x, y in zip(left, right))


def sub(left, right):
    return tuple(x - y for x, y in zip(left, right))


def scale(scalar, matrix):
    return tuple(scalar * x for x in matrix)


def transpose(matrix):
    return matrix[0], matrix[2], matrix[1], matrix[3]


def column(matrix, index):
    return matrix[index], matrix[index + 2]


def outer(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )


def determinant(matrix):
    return matrix[0] * matrix[3] - matrix[1] * matrix[2]


def omega(direct, response):
    return direct[2] * response[1] - direct[1] * response[2]


def chart_tables(blocks, chart, first_probe, second_probe):
    p, r, e, t, f, u = blocks
    if chart == "pq":
        direct = p
        forward = outer(column(r, first_probe), column(f, second_probe))
        backward = outer(column(e, second_probe), column(t, first_probe))
        residual = u[2 * first_probe + second_probe]
    elif chart == "pr":
        direct = r
        forward = outer(column(p, first_probe), column(u, second_probe))
        backward = outer(
            column(e, second_probe),
            column(transpose(t), first_probe),
        )
        residual = f[2 * first_probe + second_probe]
    elif chart == "ps":
        direct = e
        forward = outer(
            column(p, first_probe),
            column(transpose(u), second_probe),
        )
        backward = outer(
            column(r, second_probe),
            column(transpose(f), first_probe),
        )
        residual = t[2 * first_probe + second_probe]
    else:
        raise ValueError(chart)
    return direct, forward, backward, residual


def check_all_labeled_charts():
    h = 3
    direct = (1, 1, 1, 2)
    cross = (0, 1, 1, 2)
    blocks = (direct, direct, direct, cross, cross, cross)
    expected_nonzero = {(0, 0), (0, 1), (1, 0)}
    expected_pq = {
        (0, 0): ((0, 0, 0, 0), (0, 2, 0, 2), 2),
        (0, 1): ((1, 1, 1, 0), (1, 3, 1, 4), 2),
        (1, 0): ((-1, -1, -1, 0), (1, 3, 1, 4), 2),
        (1, 1): ((0, 0, 0, 0), (2, 4, 4, 8), 0),
    }
    audited_rows = 0

    assert determinant(direct) == 1
    assert determinant(cross) == -1
    assert omega(direct, direct) == 0
    assert omega(direct, (7, 0, 0, -11)) == 0

    for chart in ("pq", "pr", "ps"):
        seen_nonzero = set()
        for first_probe in range(2):
            for second_probe in range(2):
                d, forward, backward, residual = chart_tables(
                    blocks, chart, first_probe, second_probe
                )
                difference = sub(forward, backward)
                edge_sum = add(forward, backward)
                k_forward = sub(scale(residual, d), forward)
                k_backward = sub(scale(residual, d), backward)

                # Sum/difference curvature channels, equations (5)--(6).
                assert sub(k_forward, k_backward) == scale(-1, difference)
                assert add(k_forward, k_backward) == sub(
                    scale(2 * residual, d), edge_sum
                )
                assert omega(d, add(k_forward, k_backward)) == -omega(
                    d, edge_sum
                )

                # Every fixed-label Bianchi difference is already in
                # Delta + C d; the coefficient sum usually is not.
                assert omega(d, difference) == 0
                if omega(d, edge_sum):
                    seen_nonzero.add((first_probe, second_probe))
                    assert omega(d, edge_sum) == 2

                # Direct-double ledger, equations (7)--(8) and (14).
                m_base = add(scale(h, edge_sum), scale(residual, d))
                m_forward = add(
                    add(forward, scale(h, backward)),
                    scale(h * residual, d),
                )
                m_backward = add(
                    add(scale(h, forward), backward),
                    scale(h * residual, d),
                )
                assert sub(m_base, m_forward) == scale(
                    -(h - 1), k_forward
                )
                assert sub(m_base, m_backward) == scale(
                    -(h - 1), k_backward
                )
                assert sub(
                    sub(scale(2, m_base), m_forward), m_backward
                ) == scale(-(h - 1), add(k_forward, k_backward))

                # Since [difference]=0, equation (15) holds in the
                # one-dimensional quotient for every decorated label.
                edge_class = omega(d, edge_sum)
                assert omega(d, m_base) == h * edge_class
                assert 2 * omega(d, m_forward) == (h + 1) * edge_class
                assert 2 * omega(d, m_backward) == (h + 1) * edge_class

                # The two filtration grades cancel only after using
                # z z^[h-2] = (h-1) z^[h-1].
                assert add(
                    sub(m_base, m_forward),
                    scale(h - 1, k_forward),
                ) == (0, 0, 0, 0)
                assert add(
                    sub(m_base, m_backward),
                    scale(h - 1, k_backward),
                ) == (0, 0, 0, 0)

                if chart == "pq":
                    expected_difference, expected_sum, expected_class = (
                        expected_pq[(first_probe, second_probe)]
                    )
                    assert difference == expected_difference
                    assert edge_sum == expected_sum
                    assert edge_class == expected_class

                audited_rows += 1

        assert seen_nonzero == expected_nonzero

    # Equation (19), including its literal diagonal correction.
    _, forward, backward, _ = chart_tables(blocks, "pq", 0, 1)
    assert sub(forward, backward) == add(direct, (0, 0, 0, -2))

    # Two auxiliary sites give a private x_i y_j monomial to each of the
    # four products in any one chart; the same construction works for all
    # three charts because they share the p endpoint.
    private_signatures = {
        (i, j): tuple(int(position == 2 * i + j) for position in range(4))
        for i in range(2)
        for j in range(2)
    }
    assert len(set(private_signatures.values())) == 4
    assert all(sum(signature) == 1 for signature in private_signatures.values())

    assert audited_rows == 12
    return blocks, audited_rows


def check_filtered_packet(blocks):
    h = 3
    d, forward, backward, residual = chart_tables(blocks, "pq", 0, 0)
    edge_sum = add(forward, backward)
    difference = sub(forward, backward)
    k_forward = sub(scale(residual, d), forward)
    k_backward = sub(scale(residual, d), backward)

    assert residual == 0
    assert forward == backward == (0, 1, 0, 1)
    assert difference == (0, 0, 0, 0)
    assert edge_sum == (0, 2, 0, 2)
    assert sub(k_forward, k_backward) == scale(-1, difference)
    assert add(k_forward, k_backward) == sub(scale(2 * residual, d), edge_sum)

    m_base = add(scale(h, edge_sum), scale(residual, d))
    m_forward = add(
        add(forward, scale(h, backward)),
        scale(h * residual, d),
    )
    m_backward = add(
        add(scale(h, forward), backward),
        scale(h * residual, d),
    )

    assert m_base == (0, 6, 0, 6)
    assert m_forward == m_backward == (0, 4, 0, 4)
    assert sub(m_base, m_forward) == scale(-(h - 1), k_forward)
    assert sub(m_base, m_backward) == scale(-(h - 1), k_backward)
    assert sub(
        sub(scale(2, m_base), m_forward), m_backward
    ) == scale(-(h - 1), add(k_forward, k_backward))

    # These are nonzero direct-double classes.  The known source-valid
    # rows pair each with the opposite internal-curvature contribution.
    assert omega(d, edge_sum) == 2
    assert omega(d, m_base) == 6
    assert omega(d, m_forward) == omega(d, m_backward) == 4
    assert (
        omega(d, sub(m_base, m_forward))
        + (h - 1) * omega(d, k_forward)
        == 0
    )
    assert (
        omega(d, sub(m_base, m_backward))
        + (h - 1) * omega(d, k_backward)
        == 0
    )


def main():
    blocks, audited_rows = check_all_labeled_charts()
    check_filtered_packet(blocks)
    print(
        "all fixed-label crossed rows in pq/pr/ps: class-zero PASS "
        f"({audited_rows} rows)"
    )
    print("three nonzero selector sum classes per chart: PASS")
    print("sum/difference and direct-double quotient ledger: exact PASS")
    print("normal/direct-double filtered cancellation: exact PASS")


if __name__ == "__main__":
    main()
