#!/usr/bin/env python3
"""Exact local audit for notes/n8-five-degenerate-triple-shores.md."""

import sympy as sp


def main():
    e = [sp.eye(3)[:, i] for i in range(3)]
    ks = (
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
        sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
    )

    ones = sp.ones(3, 1)
    a_pq = e[2] * e[2].T - e[0] * ones.T - ones * e[1].T
    assert a_pq == sp.Matrix([[-1, -2, -1], [0, -1, 0], [0, -1, 1]])
    assert a_pq.det() == 1

    # P_s=A_ps and Q_s=A_qs.  Sites 0--4 realize the exact witness pattern
    # S_0={0,1}, S_1={2,3}, S_2={0,4}.
    a = sp.Matrix([1, 1, 1])
    singleton_b = (
        sp.Matrix([2, 1, 1]),
        sp.Matrix([1, 2, 1]),
        sp.Matrix([1, 1, 2]),
    )
    blocks = {
        0: (e[0] * e[2].T, e[0] * e[0].T),
        1: (e[0] * a.T, e[0] * singleton_b[0].T),
        2: (e[0] * a.T, e[0] * singleton_b[1].T),
        3: (e[0] * a.T, e[0] * singleton_b[1].T),
        4: (e[0] * a.T, e[0] * singleton_b[2].T),
    }

    # The sixth site is the nondegenerate staircase chart.
    u = sp.Matrix([1, 1, 0])
    a_q5 = e[0] * e[0].T + e[1] * u.T + ones * e[2].T
    a_p5 = e[1] * e[1].T - e[0] * u.T + ones * e[2].T
    blocks[5] = (a_p5, a_q5)

    zero_sets = [set() for _ in range(3)]
    site_zero_colors = {}
    for site, (p, q) in blocks.items():
        zero_colors = {r for r, k in enumerate(ks)
                       if p * k * q.T == sp.zeros(3)}
        site_zero_colors[site] = zero_colors
        for r in zero_colors:
            zero_sets[r].add(site)

    assert zero_sets == [{0, 1}, {2, 3}, {0, 4}]
    assert set().union(*zero_sets) == {0, 1, 2, 3, 4}
    assert all(len(s) == 2 for s in zero_sets)
    assert all(len(colors) < 3 for colors in site_zero_colors.values())
    assert site_zero_colors[5] == set()

    # For non-triple sites the hard colors are exactly the zero colors.
    hard_counts = [sum(r in colors for colors in site_zero_colors.values())
                   for r in range(3)]
    assert hard_counts == [2, 2, 2]

    # Site zero is the exact double witness missing color one; its two row
    # lines span e_1^perp.
    p0, q0 = blocks[0]
    combined_rows = p0.col_join(q0).rowspace()
    assert len(combined_rows) == 2
    assert all(row[1] == 0 for row in combined_rows)

    # Audit the staircase identity coefficient by coefficient.
    for i in range(3):
        for j in range(3):
            for k in range(3):
                lhs = ((1 if i == 0 else 0) * a_q5[j, k]
                       + (1 if j == 1 else 0) * a_p5[i, k]
                       + (1 if k == 2 else 0) * a_pq[i, j])
                rhs = 1 if i == j == k else 0
                assert sp.expand(lhs - rhs) == 0
    assert all(a_p5 * k * a_q5.T != sp.zeros(3) for k in ks)

    print("PASS: five-site witness union and one-staircase sharpness audited")


if __name__ == "__main__":
    main()
