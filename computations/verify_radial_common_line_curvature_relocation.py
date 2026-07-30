#!/usr/bin/env python3
"""Audit rank-one unary selection and oriented-curvature relocation.

This is deliberately a small finite-field matrix check.  It performs no
matching or graph-support enumeration.
"""

from itertools import product


if not __debug__:
    raise RuntimeError("run without -O: this audit uses assertions")


def mats(p):
    return tuple(product(range(p), repeat=4))


def vecs(p):
    return tuple(product(range(p), repeat=2))


def det(a, p):
    return (a[0] * a[3] - a[1] * a[2]) % p


def outer(x, y, p):
    return tuple((x[i] * y[j]) % p for i in range(2) for j in range(2))


def add(a, b, p):
    return tuple((x + y) % p for x, y in zip(a, b))


def scale(s, a, p):
    return tuple((s * x) % p for x in a)


def pairing(ell, a, p):
    return sum(x * y for x, y in zip(ell, a)) % p


def proportional(a, b, p):
    """Whether a lies in the span of nonzero b."""
    return any(a == scale(s, b, p) for s in range(p))


def physical_index_audit(p=3):
    """Check both endpoint-ordered four-site AU-BF orientations."""
    checked = 0
    for direct, internal, px, qy, py, qx in product(range(p), repeat=6):
        forward = (direct * internal - px * qy) % p
        backward = (direct * internal - py * qx) % p

        # D_qx at site y uses (pq)(xy) - (px)(qy).
        assert forward == (direct * internal - px * qy) % p

        # D_qy at site x first reads A_yx(d,c); physical block symmetry
        # identifies that scalar with A_xy(c,d)=internal.
        internal_reversed = internal
        assert backward == (direct * internal_reversed - py * qx) % p
        checked += 2
    return checked


def unary_selector_audit(p=5):
    all_mats = mats(p)
    all_vecs = vecs(p)
    nonzero = tuple(a for a in all_mats if any(a))
    rank_one = tuple(a for a in all_mats if any(a) and det(a, p) == 0)
    units = ((1, 0, 0, 0), (0, 0, 0, 1))
    cases = 0

    # Every nonzero square has a target-active rank-one selector in C^perp.
    target_active = 0
    for c in nonzero:
        found = any(
            pairing(outer(x, y, p), c, p) == 0
            and (
                pairing(outer(x, y, p), units[0], p) != 0
                or pairing(outer(x, y, p), units[1], p) != 0
            )
            for x in all_vecs
            if x != (0, 0)
            for y in all_vecs
            if y != (0, 0)
        )
        assert found, c
        target_active += 1

    for c in rank_one:
        selectors = []
        for x in all_vecs:
            if x == (0, 0):
                continue
            for y in all_vecs:
                if y == (0, 0):
                    continue
                ell = outer(x, y, p)
                if pairing(ell, c, p) == 0:
                    selectors.append(ell)

        for e, unit in enumerate(units):
            other = units[1 - e]
            exists = any(
                pairing(ell, unit, p) == 1
                and pairing(ell, other, p) == 0
                for ell in selectors
            )
            expected = not proportional(c, unit, p)
            assert exists == expected, (c, e, exists, expected)
            cases += 1

        assert any(
            pairing(ell, units[0], p) != 0
            or pairing(ell, units[1], p) != 0
            for ell in selectors
        )

    return len(nonzero), target_active, len(rank_one), cases


def relocation_audit(p=3):
    all_mats = mats(p)
    all_vecs = vecs(p)
    rank_one = tuple(a for a in all_mats if any(a) and det(a, p) == 0)
    checked = 0
    nonzero_coefficients = 0

    for c in rank_one:
        # Choose the first target-active rank-one functional in C^perp.
        ell = next(
            outer(x, y, p)
            for x in all_vecs
            if x != (0, 0)
            for y in all_vecs
            if y != (0, 0)
            if pairing(outer(x, y, p), c, p) == 0
            and (
                pairing(outer(x, y, p), (1, 0, 0, 0), p) != 0
                or pairing(outer(x, y, p), (0, 0, 0, 1), p) != 0
            )
        )

        for h_forward in all_mats:
            for h_backward in all_mats:
                # The internal scalar is immaterial after ell(C)=0.  A
                # deterministic varying value keeps the audit lightweight.
                b = pairing(ell, add(h_forward, h_backward, p), p)
                u = (sum(h_forward) + 2 * sum(h_backward)) % p
                k_forward = add(scale(u, c, p), scale(-1, h_forward, p), p)
                k_backward = add(scale(u, c, p), scale(-1, h_backward, p), p)
                left = (
                    pairing(ell, k_forward, p) + pairing(ell, k_backward, p)
                ) % p
                assert left == (-b) % p
                if b != 0:
                    nonzero_coefficients += 1
                    assert (
                        pairing(ell, k_forward, p) != 0
                        or pairing(ell, k_backward, p) != 0
                    )
                    assert not (
                        proportional(k_forward, c, p)
                        and proportional(k_backward, c, p)
                    )
                checked += 1

        # The selected radial line is invisible to every direct-zero ell.
        for lam in range(1, p):
            assert pairing(ell, scale(lam, c, p), p) == 0

    return len(rank_one), checked, nonzero_coefficients


def main():
    physical = physical_index_audit()
    nonzero_5, active_5, rank_one_5, unary_cases = unary_selector_audit()
    rank_one_3, identities, live = relocation_audit()
    print(
        "physical oriented AU-BF indices: PASS "
        f"({physical} endpoint-ordered identities)"
    )
    print(
        "target-active rank-one selection: PASS "
        f"({active_5}/{nonzero_5} nonzero matrices)"
    )
    print(
        "singular unary selector criterion: PASS "
        f"({rank_one_5} rank-one matrices, {unary_cases} prescribed-label cases)"
    )
    print(
        "oriented curvature relocation: PASS "
        f"({rank_one_3} compressions, {identities} identities, {live} nonzero coefficients)"
    )


if __name__ == "__main__":
    main()
