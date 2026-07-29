#!/usr/bin/env python3
"""Tiny exact audit of the uncontracted four-cut two-dark obstruction.

This checker is deliberately finite and dependency-free.  It verifies the
81 matrix-unit rows, their arbitrary matrix projection, and the three target
indices used by each of the two symmetric contradiction arguments.
"""

from itertools import product


COLOURS = range(3)


def target(a, b, c, d):
    """The target coefficient, represented by its surviving colour."""

    return a if a == b == c == d else None


def full_layer_coefficients(a, b, c, d, direct_pq, direct_ij,
                            cross_pq, cross_ij):
    """Four formal matching layers in the exact row (scalar coefficients)."""

    return (
        direct_pq[a][b] * direct_ij[c][d],
        direct_pq[a][b] * cross_ij[c][d],
        cross_pq[a][b] * direct_ij[c][d],
        cross_pq[a][b] * cross_ij[c][d],
    )


def audit_matrix_projection():
    # Fixed nonsymmetric integer data make endpoint-order mistakes visible.
    direct_pq = [[11 + 3 * a + b for b in COLOURS] for a in COLOURS]
    direct_ij = [[31 + 5 * c + 2 * d for d in COLOURS] for c in COLOURS]
    cross_pq = [[53 + 7 * a + 3 * b for b in COLOURS] for a in COLOURS]
    cross_ij = [[79 + 11 * c + 5 * d for d in COLOURS] for c in COLOURS]
    matrices = [
        [[int(a == r and b == s) for b in COLOURS] for a in COLOURS]
        for r, s in product(COLOURS, repeat=2)
    ]
    matrices.append([[1, -2, 3], [5, 0, -7], [11, 13, -17]])

    checked = 0
    for matrix in matrices:
        lam = sum(matrix[a][b] * direct_pq[a][b]
                  for a, b in product(COLOURS, repeat=2))
        q_value = sum(matrix[a][b] * cross_pq[a][b]
                      for a, b in product(COLOURS, repeat=2))
        for c, d in product(COLOURS, repeat=2):
            summed = tuple(
                sum(matrix[a][b] * full_layer_coefficients(
                    a, b, c, d, direct_pq, direct_ij,
                    cross_pq, cross_ij)[layer]
                    for a, b in product(COLOURS, repeat=2))
                for layer in range(4)
            )
            projected = (
                lam * direct_ij[c][d],
                lam * cross_ij[c][d],
                q_value * direct_ij[c][d],
                q_value * cross_ij[c][d],
            )
            assert summed == projected
            projected_target = matrix[c][c] if c == d else 0
            direct_target = sum(
                matrix[a][b] * int(target(a, b, c, d) is not None)
                for a, b in product(COLOURS, repeat=2)
            )
            assert direct_target == projected_target
            checked += 1
    return checked


def audit_three_row_patterns():
    checked = 0
    for r, s in product(COLOURS, repeat=2):
        if r == s:
            continue

        # If t_r v_r=t_s v_s=0, these rows share R_rr with scalar
        # multipliers u_rr and u_ss.
        assert target(r, r, r, r) == r
        assert target(s, s, s, s) == s
        assert target(r, r, s, s) is None

        # If x_r y_r=x_s y_s=0, these rows share S_rr with scalar
        # multipliers a_rr and a_ss.
        assert target(r, r, r, r) == r
        assert target(s, s, s, s) == s
        assert target(s, s, r, r) is None
        checked += 2
    assert checked == 12
    return checked


def audit_repeated_pair_boundary():
    # Section 5 of the predecessor note uses only colour zero in both
    # t and v.  Therefore colours one and two are a forbidden dark pair.
    t_live = {0}
    v_live = {0}
    dark = {c for c in COLOURS if c not in t_live or c not in v_live}
    assert dark == {1, 2}
    return tuple(sorted(dark))


def main():
    projections = audit_matrix_projection()
    decisive_rows = audit_three_row_patterns()
    dark = audit_repeated_pair_boundary()
    print("uncontracted four-cut two-dark obstruction: PASS")
    print(f"projected row instances={projections}; "
          f"decisive row patterns={decisive_rows}; forbidden dark pair={dark}")


if __name__ == "__main__":
    main()
