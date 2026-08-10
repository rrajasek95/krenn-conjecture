#!/usr/bin/env python3
"""Exact h=3 two-chart divisor-transport/Fitting obstruction.

This is deliberately a presentation-module calculation.  It audits the
completed 2x2 source-label block, the literal four-cut clean-tail identity,
and the residual Macaulay block over Q.  It does not assert that the displayed
cut-local coefficients extend to one global matching source.
"""

from fractions import Fraction as F
import hashlib
import json


EXPECTED_DIGEST = "236f1e4bd4a63ce4b11ef5b0c8b874fec361d99735681f146cd982454690d344"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def transpose(a):
    return [list(row) for row in zip(*a)]


def mat_vec(a, x):
    return [sum((v * y for v, y in zip(row, x)), F(0)) for row in a]


def rank(a):
    m = [list(map(F, row)) for row in a]
    if not m:
        return 0
    nr, nc = len(m), len(m[0])
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if m[i][c]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        scale = m[r][c]
        m[r] = [x / scale for x in m[r]]
        for i in range(nr):
            if i != r and m[i][c]:
                scale = m[i][c]
                m[i] = [x - scale * y for x, y in zip(m[i], m[r])]
        r += 1
        if r == nr:
            break
    return r


def determinant(a):
    m = [list(map(F, row)) for row in a]
    n = len(m)
    require(all(len(row) == n for row in m), "determinant needs square matrix")
    out = F(1)
    for c in range(n):
        pivot = next((i for i in range(c, n) if m[i][c]), None)
        if pivot is None:
            return F(0)
        if pivot != c:
            m[c], m[pivot] = m[pivot], m[c]
            out = -out
        p = m[c][c]
        out *= p
        for i in range(c + 1, n):
            if m[i][c]:
                scale = m[i][c] / p
                for j in range(c, n):
                    m[i][j] -= scale * m[c][j]
    return out


def flatten(a):
    return [a[0][0], a[0][1], a[1][0], a[1][1]]


def block_diag(a, b):
    za = [F(0)] * len(b)
    zb = [F(0)] * len(a)
    return [list(row) + za for row in a] + [zb + list(row) for row in b]


def residual_matrix(chi, b, c):
    """g*S_2 -> S_5/(v^3*S_2), g=chi*u^3+b*u^2v+c*uv^2+d*v^3."""
    return [
        [F(chi), F(0), F(0)],
        [F(b), F(chi), F(0)],
        [F(c), F(b), F(chi)],
    ]


def q(x):
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def main():
    # Static source-label block.  The crossed J row has zero target grade;
    # E00 and E11 are the two differently labelled diagonal anchors.
    e00 = [[F(1), F(0)], [F(0), F(0)]]
    e11 = [[F(0), F(0)], [F(0), F(1)]]
    direct = [[F(1), F(1)], [F(1), F(2)]]
    h_right = [[F(0), F(1)], [F(0), F(0)]]
    h_left = [[F(0), F(0)], [F(2), F(0)]]
    normal = [[F(0), F(1)], [F(2), F(0)]]
    crossed = [[F(0), F(1)], [F(-2), F(0)]]

    require(crossed == [[h_right[i][j] - h_left[i][j] for j in range(2)]
                        for i in range(2)], "crossed orientation sign changed")
    require(normal == [[h_right[i][j] + h_left[i][j] for j in range(2)]
                       for i in range(2)], "normal orientation sum changed")

    # B=-J/3+4d/3-4E00/3-8E11/3.
    relation = []
    for i in range(2):
        relation.append([])
        for j in range(2):
            relation[i].append(
                -crossed[i][j] / 3 + 4 * direct[i][j] / 3
                - 4 * e00[i][j] / 3 - 8 * e11[i][j] / 3
            )
    require(relation == normal, "two-anchor crossed transport relation failed")

    static = transpose([flatten(e00), flatten(e11), flatten(direct), flatten(crossed)])
    require(rank(static) == 4, "static completed-square span is not full")
    require(determinant(static) == -3, "unexpected static determinant")

    # Literal four-cut clean-tail bookkeeping in the free source grades
    # (q^[3], R q^[2], R^[2] q, R^[3]).  For F=alpha*q+R,
    # F^[3] minus alpha^2 times the physical mixed row
    # alpha*q^[3]+R*q^[2] is alpha*R^[2]q+R^[3].
    for alpha in (F(1), F(2), F(-3, 2)):
        full = [alpha ** 3, alpha ** 2, alpha, F(1)]
        physical = [alpha, F(1), F(0), F(0)]
        tail = [x - alpha ** 2 * y for x, y in zip(full, physical)]
        require(tail == [F(0), F(0), alpha, F(1)],
                "literal four-cut clean-tail identity failed")

    # The residual block is triangular.  Its top Fitting generator is chi^3.
    probes = [
        (F(1), F(0), F(0)),
        (F(2), F(-3), F(5)),
        (F(-2, 3), F(7, 5), F(-11, 4)),
        (F(0), F(1), F(2)),
    ]
    residual_facts = []
    for chi, b, c in probes:
        m = residual_matrix(chi, b, c)
        det = determinant(m)
        require(det == chi ** 3, "residual Fitting determinant is not chi^3")
        residual_facts.append({
            "chi": q(chi), "b": q(b), "c": q(c),
            "det": q(det), "rank": rank(m),
        })

    # The combined literal-grade presentation is block diagonal after the
    # exact static transport relation.  Thus its determinant is -3*chi^3.
    generic = block_diag(static, residual_matrix(F(1), F(3), F(-2)))
    boundary = block_diag(static, residual_matrix(F(0), F(1), F(2)))
    require(determinant(generic) == -3, "generic combined determinant changed")
    require(rank(generic) == 7, "generic two-chart module should fill its cokernel")
    require(determinant(boundary) == 0, "boundary determinant should vanish")
    require(rank(boundary) == 6, "generic chi=0 boundary should have cokernel one")

    # At chi=0, coefficient evaluation [u^5] is the explicit nonzero Q_f dual.
    eval_u5 = [F(1), F(0), F(0)]
    require(mat_vec(transpose(residual_matrix(F(0), F(1), F(2))), eval_u5)
            == [F(0), F(0), F(0)], "[u^5] does not annihilate boundary image")
    require(mat_vec(transpose(residual_matrix(F(1), F(3), F(-2))), eval_u5)
            != [F(0), F(0), F(0)], "[u^5] incorrectly kills generic image")

    ledger = {
        "scope": "h3-two-chart-completed-square-plus-one-literal-four-cut-grade",
        "static_columns": ["anchor_00", "anchor_11", "direct_d", "crossed_zero_J"],
        "static_det": q(determinant(static)),
        "transport_coefficients": ["-4/3", "-8/3", "4/3", "-1/3"],
        "clean_tail_grades": ["alpha*R^[2]*q", "R^[3]"],
        "residual_basis": ["u5", "u4v", "u3v2"],
        "fitting_generator": "-3*chi^3",
        "generic_combined_rank": rank(generic),
        "chi_zero_combined_rank": rank(boundary),
        "chi_zero_dual": "coefficient_of_u5",
        "probes": residual_facts,
        "verdict": "dual_exists_iff_chi_zero; retained_rows_do_not_force_chi_zero",
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 two-chart divisor-transport Fitting obstruction: PASS")
    print(f"static determinant: {q(determinant(static))}")
    print("combined determinant: -3*chi^3")
    print("Q_f dual: nonzero exactly on chi=0 boundary")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
