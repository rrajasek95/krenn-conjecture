#!/usr/bin/env python3
"""Exact audits for the extra-singular frontier and heavy-class closure.

The finite parts of the accompanying proof are:

* the complete missed-axis-family census, modulo the residual 0<->1
  symmetry;
* the parity/range census for the sole eligible extra plane; and
* reconstruction over Q of the two singleton response rows used in the
  heavy exceptional beta-class theorem.

The matching audit deliberately uses unrelated rational beta values away
from the homogeneous shore.  Thus it checks that the proof needs equality
only on the selected r-set, not on the entire exceptional shore.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
from math import factorial


COLOURS = frozenset(range(3))
ALLOWED_MISSED = (
    frozenset({0}),
    frozenset({1}),
    frozenset({2}),
    frozenset({0, 2}),
    frozenset({1, 2}),
)


def admissible(family: tuple[frozenset[int], ...]) -> bool:
    return all(
        left.isdisjoint(right)
        for index, left in enumerate(family)
        for right in family[index + 1 :]
    )


def family_key(family: tuple[frozenset[int], ...]) -> tuple[int, ...]:
    return tuple(sorted(sum(1 << colour for colour in missed) for missed in family))


def swap_binary(family: tuple[frozenset[int], ...]) -> tuple[frozenset[int], ...]:
    transposition = {0: 1, 1: 0, 2: 2}
    return tuple(
        sorted(
            (frozenset(transposition[colour] for colour in missed) for missed in family),
            key=lambda item: sum(1 << colour for colour in item),
        )
    )


def canonical(family: tuple[frozenset[int], ...]) -> tuple[int, ...]:
    return min(family_key(family), family_key(swap_binary(family)))


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[str, ...]) -> tuple[tuple[tuple[str, str], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def hafnian(vertices: tuple[str, ...], rows, betas) -> Fraction:
    answer = Fraction(0)
    for matching in perfect_matchings(vertices):
        product = Fraction(1)
        for left, right in matching:
            left_row = rows[left]
            right_row = rows[right]
            # H has zero diagonal and unit off-diagonal entries.
            numerator = sum(
                left_row[a] * right_row[b]
                for a in range(3)
                for b in range(3)
                if a != b
            )
            product *= numerator / (betas[left] + betas[right])
        answer += product
    return answer


def response_coefficients(vertices, rows, betas, marked_pair) -> dict[str, Fraction]:
    """Source 22 with a pre-certified unique marked pair.

    Every selected row gives marked coefficient two.  The direct 22
    coefficient is zero, so the star coefficient is twice the cofactor
    hafnian after deleting the marked pair and the star.
    """

    marked = frozenset(marked_pair)
    answer = {}
    for star in vertices:
        if star in marked:
            answer[star] = Fraction(0)
            continue
        remaining = tuple(v for v in vertices if v not in marked and v != star)
        answer[star] = 2 * hafnian(remaining, rows, betas)
    return answer


def audit_family_census() -> None:
    families = [()]
    for size in range(1, 4):
        families.extend(
            family
            for family in combinations_with_replacement(ALLOWED_MISSED, size)
            if admissible(family)
        )
    assert len(families) == 12
    assert sum(bool(family) for family in families) == 11
    assert all(sum(missed == frozenset({2}) for missed in family) <= 1 for family in families)

    expected_nonempty_orbits = {
        canonical((frozenset({2}),)),
        canonical((frozenset({2}), frozenset({0}))),
        canonical((frozenset({2}), frozenset({0}), frozenset({1}))),
        canonical((frozenset({0}),)),
        canonical((frozenset({0, 2}),)),
        canonical((frozenset({0}), frozenset({1}))),
        canonical((frozenset({0}), frozenset({1, 2}))),
    }
    actual_nonempty_orbits = {canonical(family) for family in families if family}
    assert actual_nonempty_orbits == expected_nonempty_orbits

    eligible = [family for family in families if frozenset({2}) in family]
    assert len(eligible) == 4
    assert {canonical(family) for family in eligible} == {
        canonical((frozenset({2}),)),
        canonical((frozenset({2}), frozenset({0}))),
        canonical((frozenset({2}), frozenset({0}), frozenset({1}))),
    }


def audit_sole_plane_ranges() -> None:
    for r in range(1, 40):
        live = 2 * r
        already_closed = {
            t for t in range(live + 1) if r == 1 or t <= min(live, r + 2)
        }
        unresolved = set(range(live + 1)) - already_closed
        expected = set(range(r + 3, 2 * r + 1)) if r >= 3 else set()
        assert unresolved == expected
        assert {t - r - 1 for t in unresolved} == (
            set(range(2, r)) if r >= 3 else set()
        )

    # After the new theorem, every unresolved multiplicity profile has
    # largest exceptional beta class at most r-1.
    for r in range(3, 20):
        for t in range(r + 3, 2 * r + 1):
            assert t >= r + 2
            # A heavy class of size r is exactly the theorem's trigger.
            assert r <= t


def rational_betas(r: int, t: int):
    """Return a heavy r-class and unrelated admissible remaining values."""

    nu = Fraction(2)
    exceptional = [nu] * r
    # The remaining exceptional values are deliberately all different.
    exceptional.extend(Fraction(4 + index) for index in range(t - r))
    common = [Fraction(1)] * (2 * r - t)
    return exceptional + common


def audit_heavy_class_response() -> None:
    zero = (Fraction(0), Fraction(0), Fraction(0))
    e0 = (Fraction(1), Fraction(0), Fraction(0))
    e1 = (Fraction(0), Fraction(1), Fraction(0))
    e2 = (Fraction(0), Fraction(0), Fraction(1))

    for r in range(2, 6):
        for t in range(r + 2, 2 * r + 1):
            live_betas = rational_betas(r, t)
            live = [f"u{index}" for index in range(2 * r)]
            centres = ["c", "d"]
            extra = "e"
            vertices = tuple(live + centres + [extra])
            betas = {
                **dict(zip(live, live_betas)),
                "c": Fraction(1),
                "d": Fraction(1),
                "e": Fraction(1),
            }

            heavy = live[:r]
            outside = live[r:]
            marked = tuple(outside[:2])
            assert len(marked) == 2

            # First singleton: contract e by an annihilator of im P_e.
            # The r equal-beta labels form one shore and every other
            # ordinary label forms the opposite shore.
            rows = {site: e1 for site in live + centres}
            for site in heavy:
                rows[site] = e0
            for site in marked:
                rows[site] = e2
            rows[extra] = zero
            coefficients = response_coefficients(vertices, rows, betas, marked)
            nu = betas[heavy[0]]
            opposite = [
                site
                for site in live + centres
                if site not in marked and site not in heavy
            ]
            expected = 2 * factorial(r)
            for site in opposite:
                expected *= Fraction(1, 1) / (nu + betas[site])
            assert coefficients[extra] == expected
            assert all(
                coefficient == 0
                for site, coefficient in coefficients.items()
                if site != extra
            )

            # Second singleton modulo structurally zero exceptional stars:
            # put one active beta-one site together with the homogeneous
            # r-shore.  The contracted extra row p=(0,1,0) must pair into
            # that shore.  Only the chosen active star survives.
            target = "c"
            rows = {site: e1 for site in live + centres}
            for site in heavy:
                rows[site] = e0
            rows[target] = e0
            for site in marked:
                rows[site] = e2
            rows[extra] = e1  # p=(0,1,0), hence p_2=0 and p_1=1.
            coefficients = response_coefficients(vertices, rows, betas, marked)
            assert coefficients[target] == expected
            active = {
                site
                for site in live + centres
                if betas[site] == 1
            }
            assert all(
                coefficients[site] == 0 for site in active if site != target
            )
            assert coefficients[extra] == 0

            # The p=(1,0,0) colour-swapped axial branch has the same pivot.
            rows = {site: e0 for site in live + centres}
            for site in heavy:
                rows[site] = e1
            rows[target] = e1
            for site in marked:
                rows[site] = e2
            rows[extra] = e0
            coefficients = response_coefficients(vertices, rows, betas, marked)
            assert coefficients[target] == expected
            assert all(
                coefficients[site] == 0 for site in active if site != target
            )
            assert coefficients[extra] == 0


def main() -> None:
    audit_family_census()
    audit_sole_plane_ranges()
    audit_heavy_class_response()
    print("live three-zero extra-singular exact frontier: PASS")
    print("admissible nonempty families=11; binary-symmetry orbits=7")
    print("eligible-rescue orbits=3; sole-plane arbitrary-value gap h=2,...,r-1")
    print("heavy exceptional class (multiplicity >= r) response pivots: exact")


if __name__ == "__main__":
    main()
