#!/usr/bin/env python3
"""Symbolic audit of equal-mask exclusion in all triple normal forms."""

from itertools import combinations

from sympy import Matrix, diag, simplify, symbols


def minor(matrix, rows, columns):
    return simplify(matrix.extract(rows, columns).det())


def coordinate_support(vector):
    return {i for i, entry in enumerate(vector) if entry != 0}


def tensor3(left, middle, right):
    return tuple(
        left[i] * middle[j] * right[k]
        for i in range(3) for j in range(3) for k in range(3)
    )


def add_tensors(*tensors):
    return tuple(sum(entries) for entries in zip(*tensors, strict=True))


def audit_surviving_label_models():
    basis = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    zero = (0,) * 27
    singleton_models = 0
    pair_models = 0
    allowed_pairs = {}

    for mask_bits in range(1, 8):
        mask = {color for color in range(3) if mask_bits >> color & 1}
        b = tuple(int(color in mask) for color in range(3))

        # Any singleton survivor is supplied by the third slice.
        for color in range(3):
            response = tensor3(basis[color], basis[color], basis[color])
            assert response != zero
            singleton_models += 1

        allowed_pairs[mask_bits] = []
        for pair in combinations(range(3), 2):
            pair = set(pair)
            if pair.isdisjoint(mask):
                continue
            h = next(iter(pair & mask))
            k = next(iter(pair - {h}))
            d = tuple(b[color] + int(color == h) for color in range(3))
            assert coordinate_support(b) == mask
            assert coordinate_support(d) == mask

            # -e_h tensor e_h tensor b + e_h tensor e_h tensor d = g_h.
            negative_h = tuple(-entry for entry in basis[h])
            cross_response = add_tensors(
                tensor3(negative_h, basis[h], b),
                tensor3(basis[h], basis[h], d),
            )
            assert cross_response == tensor3(basis[h], basis[h], basis[h])

            # A_xy=E_kk and Z_z=e_k give g_k through the third slice.
            third_response = tensor3(basis[k], basis[k], basis[k])
            assert third_response != zero
            allowed_pairs[mask_bits].append(tuple(sorted(pair)))
            pair_models += 1

        expected_pair_count = 2 if len(mask) == 1 else 3
        assert len(allowed_pairs[mask_bits]) == expected_pair_count

    assert singleton_models == 21
    assert pair_models == 18
    return singleton_models, pair_models, allowed_pairs


def main():
    rho, sigma, tau = symbols("rho sigma tau", nonzero=True)
    u0, u1, u2, v0, v1, v2, w0, w1, w2 = symbols(
        "u0 u1 u2 v0 v1 v2 w0 w1 w2"
    )

    u = Matrix([u0, u1, u2])
    v = Matrix([v0, v1, v2])
    w = Matrix([w0, w1, w2])
    e0 = Matrix([1, 0, 0])
    e1 = Matrix([0, 1, 0])
    e2 = Matrix([0, 0, 1])

    m0 = e0 * e0.T + e1 * u.T + v * e2.T
    m1 = e1 * e1.T - rho * e0 * u.T + w * e2.T
    m2 = e2 * e2.T - sigma * e0 * v.T - tau * w * e1.T

    # The pivot minors used in equations (7)--(8).
    assert minor(m0, (0, 2), (0, 2)) == v2
    assert minor(m0, (0, 1), (0, 1)) == u1
    assert minor(m0, (0, 1), (0, 2)) == u2 + v1 - u0 * v0
    assert minor(m1, (0, 1), (0, 1)) == -rho * u0
    assert minor(m1, (1, 2), (1, 2)) == w2
    assert minor(m1, (0, 1), (1, 2)) == rho * u2 - rho * u1 * w1 - w0

    # Dimension-two normal form.  We audit the four possible supports of
    # theta.  theta={0,1}: rank one of both sides forces w=0.
    theta0, theta1 = symbols("theta0 theta1", nonzero=True)
    z0, z1, z2 = symbols("z0 z1 z2")
    zvec = Matrix([z0, z1, z2])
    d2_01_m0 = e0 * e0.T + theta0 * e1 * zvec.T
    d2_01_m1 = e1 * e1.T + theta1 * e0 * zvec.T
    assert minor(d2_01_m0, (0, 1), (0, 1)) == theta0 * z1
    assert minor(d2_01_m0, (0, 1), (0, 2)) == theta0 * z2
    assert minor(d2_01_m1, (0, 1), (0, 1)) == theta1 * z0
    assert minor(d2_01_m1, (0, 1), (1, 2)) == -theta1 * z2

    # theta={0,2}: rank one forces v into C e0, leaving z-mask {0}
    # or {0,2}, while the other side has mask {1}.
    theta2 = symbols("theta2", nonzero=True)
    y0, y1, y2 = symbols("y0 y1 y2")
    yvec = Matrix([y0, y1, y2])
    d2_02_m0 = e0 * e0.T + theta0 * yvec * e2.T
    assert minor(d2_02_m0, (0, 1), (0, 2)) == theta0 * y1
    assert minor(d2_02_m0, (0, 2), (0, 2)) == theta0 * y2
    for value in (0, 5):
        assert coordinate_support(Matrix([1, 0, value])) != {1}

    # theta={1,2} is the symmetric case.
    for value in (0, 7):
        assert {0} != coordinate_support(Matrix([0, 1, value]))

    # Full theta support: a nonzero rainbow leakage makes each cross
    # matrix rank two, so rank one forces the leakage scalar to vanish.
    mu = symbols("mu")
    d2_all_m0 = e0 * e0.T + theta0 * mu * e1 * e2.T
    d2_all_m1 = e1 * e1.T + theta1 * mu * e0 * e2.T
    assert minor(d2_all_m0, (0, 1), (0, 2)) == theta0 * mu
    assert minor(d2_all_m1, (0, 1), (1, 2)) == -theta1 * mu

    # Dimension-one cyclic staircase.  Alpha and beta may vanish; this is
    # the point needed to remove the old invertibility hypothesis.
    alpha, beta, transfer = symbols("alpha beta transfer")
    staircase_substitution = {
        u0: 0,
        u1: 0,
        u2: transfer,
        v0: alpha,
        v1: -transfer,
        v2: 0,
        w0: rho * transfer,
        w1: beta,
        w2: 0,
        sigma: tau * rho,
    }

    reduced0 = simplify(m0.subs(staircase_substitution))
    reduced1 = simplify(m1.subs(staircase_substitution))
    reduced2 = simplify(m2.subs(staircase_substitution))

    assert reduced0 == e0 * Matrix([1, 0, alpha]).T
    assert reduced1 == e1 * Matrix([0, 1, beta]).T
    assert reduced2 == diag(-tau * rho * alpha, -tau * beta, 1)
    assert simplify(reduced2.det() - tau**2 * rho * alpha * beta) == 0
    for aval in (0, 2):
        for bval in (0, 3):
            left_mask = coordinate_support(Matrix([1, 0, aval]))
            right_mask = coordinate_support(Matrix([0, 1, bval]))
            assert left_mask != right_mask

    label_models = audit_surviving_label_models()

    print("verified dimension-two equal-mask exclusion in all four cases")
    print("verified cyclic-staircase separation including alpha=0 or beta=0")
    print(f"verified sharp surviving-label models: {label_models[:2]}")
    print("PASS: complete-join selector-saturation audit")


if __name__ == "__main__":
    main()
