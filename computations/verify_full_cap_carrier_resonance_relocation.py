#!/usr/bin/env python3
"""Lightweight finite-field audit of carrier-resonance relocation lemmas.

This checks only the 2x2 linear algebra used in the accompanying note:

* simultaneous arbitrary-functional selection;
* existence of a rank-one C-isotropic diagonal target;
* rank-one curvature selection when K is not proportional to C; and
* the singular common-line classification of radial resonances.

The coefficient-span theorem itself is the formal coefficient extraction
from the full-nine identity and does not require a matching enumeration.
"""

from itertools import product


if not __debug__:
    raise RuntimeError("run without -O: this audit uses assertions")


P = 5
MATS = [x for x in product(range(P), repeat=4) if any(x)]


def add(a, b):
    return tuple((x + y) % P for x, y in zip(a, b))


def scale(t, a):
    return tuple(t * x % P for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b)) % P


def det(a):
    return (a[0] * a[3] - a[1] * a[2]) % P


def normalize(a):
    i = next(i for i, x in enumerate(a) if x)
    inv = pow(a[i], -1, P)
    return scale(inv, a)


def proportional(a, b):
    return normalize(a) == normalize(b)


def rank_one_projective():
    answer = set()
    for xi in product(range(P), repeat=2):
        if not any(xi):
            continue
        for eta in product(range(P), repeat=2):
            if not any(eta):
                continue
            ell = (
                xi[0] * eta[0] % P,
                xi[0] * eta[1] % P,
                xi[1] * eta[0] % P,
                xi[1] * eta[1] % P,
            )
            answer.add(normalize(ell))
    return sorted(answer)


RANK_ONE = rank_one_projective()
PROJECTIVE = sorted({normalize(a) for a in MATS})


def audit_arbitrary_selection():
    target_functionals = [
        ell for ell in PROJECTIVE if ell[0] or ell[3]
    ]
    masks = {}
    for v in PROJECTIVE:
        mask = 0
        for i, ell in enumerate(target_functionals):
            if dot(ell, v):
                mask |= 1 << i
        masks[v] = mask
    checked = 0
    for k in PROJECTIVE:
        for w in PROJECTIVE:
            assert masks[k] & masks[w]
            checked += 1
    return checked


def audit_rank_one_selection():
    target_cases = 0
    curvature_cases = 0
    for c in PROJECTIVE:
        admissible = [
            ell
            for ell in RANK_ONE
            if dot(ell, c) == 0 and (ell[0] or ell[3])
        ]
        assert admissible
        target_cases += 1

        for k in PROJECTIVE:
            if k == c:
                continue
            assert any(dot(ell, k) for ell in admissible)
            curvature_cases += 1
    return target_cases, curvature_cases


def audit_radial_resonance():
    low_rank = [(0, 0, 0, 0)] + [a for a in MATS if det(a) == 0]
    zero_u = nonzero_u = 0
    for h in (3, 4):
        inv_h = pow(h, -1, P)
        for c in PROJECTIVE:
            for hmat in low_rank:
                for u in range(P):
                    # W = (u/h) C + H + G = 0 determines G.
                    gmat = scale(
                        -1,
                        add(scale(u * inv_h % P, c), hmat),
                    )
                    if det(gmat):
                        continue
                    kmat = add(scale(u, c), scale(-1, hmat))
                    if not any(kmat) or not proportional(kmat, c):
                        continue

                    lam = next(
                        kmat[i] * pow(c[i], -1, P) % P
                        for i in range(4)
                        if c[i]
                    )
                    assert lam
                    assert det(c) == 0
                    assert hmat == scale((u - lam) % P, c)
                    expected_g = scale(
                        (lam - (h + 1) * u * inv_h) % P,
                        c,
                    )
                    assert gmat == expected_g
                    if any(hmat):
                        assert proportional(hmat, c)
                    if any(gmat):
                        assert proportional(gmat, c)
                    if u:
                        nonzero_u += 1
                    else:
                        zero_u += 1
    return zero_u, nonzero_u


def main():
    arbitrary = audit_arbitrary_selection()
    target, curvature = audit_rank_one_selection()
    zero_u, nonzero_u = audit_radial_resonance()
    print(
        "arbitrary simultaneous selection: PASS "
        f"({arbitrary:,} nonzero K/W pairs)"
    )
    print(
        "rank-one direct-zero selection: PASS "
        f"({target:,} target cases, {curvature:,} nonradial curvature cases)"
    )
    print(
        "radial resonance classification: PASS "
        f"({zero_u:,} U=0, {nonzero_u:,} U!=0 packets)"
    )


if __name__ == "__main__":
    main()
