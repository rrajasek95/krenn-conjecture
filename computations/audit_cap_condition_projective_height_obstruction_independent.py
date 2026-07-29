#!/usr/bin/env python3
"""Clean-room audit of the cap-condition projective-height obstruction.

This checker imports neither the primary note nor its checker.  In addition
to symbolic polynomial identities, it uses a small custom square-free tensor
algebra and a monomial-ideal audit of the radical and saturation claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb

import sympy as sy


SITE_COUNT = 6
EMPTY_WORD = (-1,) * SITE_COUNT
FROZEN_LEDGER_SHA256 = "de90db6ab15da34489530cfd9f5ae6f233cb0d01cbba32736a968ae12d5527dd"


@dataclass(frozen=True)
class SquareFreeTensor:
    """Sparse commutative tensor algebra with every site square zero."""

    terms: dict[tuple[int, ...], sy.Expr]

    @staticmethod
    def zero() -> "SquareFreeTensor":
        return SquareFreeTensor({})

    @staticmethod
    def one() -> "SquareFreeTensor":
        return SquareFreeTensor({EMPTY_WORD: sy.Integer(1)})

    @staticmethod
    def basis(assignments: dict[int, int], coefficient=1) -> "SquareFreeTensor":
        word = [-1] * SITE_COUNT
        for site, colour in assignments.items():
            assert 0 <= site < SITE_COUNT
            assert 0 <= colour < 3
            assert word[site] == -1
            word[site] = colour
        coefficient = sy.expand(coefficient)
        if coefficient == 0:
            return SquareFreeTensor.zero()
        return SquareFreeTensor({tuple(word): coefficient})

    def cleaned(self) -> "SquareFreeTensor":
        return SquareFreeTensor(
            {
                word: expanded
                for word, coefficient in self.terms.items()
                if (expanded := sy.expand(coefficient)) != 0
            }
        )

    def __add__(self, other: "SquareFreeTensor") -> "SquareFreeTensor":
        result = dict(self.terms)
        for word, coefficient in other.terms.items():
            result[word] = result.get(word, sy.Integer(0)) + coefficient
        return SquareFreeTensor(result).cleaned()

    def __neg__(self) -> "SquareFreeTensor":
        return self.scale(-1)

    def __sub__(self, other: "SquareFreeTensor") -> "SquareFreeTensor":
        return self + (-other)

    def scale(self, scalar) -> "SquareFreeTensor":
        return SquareFreeTensor(
            {word: sy.expand(scalar * coefficient)
             for word, coefficient in self.terms.items()}
        ).cleaned()

    def __mul__(self, other: "SquareFreeTensor") -> "SquareFreeTensor":
        result: dict[tuple[int, ...], sy.Expr] = {}
        for left_word, left_coefficient in self.terms.items():
            for right_word, right_coefficient in other.terms.items():
                if any(
                    left_word[site] != -1 and right_word[site] != -1
                    for site in range(SITE_COUNT)
                ):
                    continue
                word = tuple(
                    left_word[site] if left_word[site] != -1 else right_word[site]
                    for site in range(SITE_COUNT)
                )
                result[word] = (
                    result.get(word, sy.Integer(0))
                    + left_coefficient * right_coefficient
                )
        return SquareFreeTensor(result).cleaned()

    def power(self, exponent: int) -> "SquareFreeTensor":
        assert exponent >= 0
        result = SquareFreeTensor.one()
        for _ in range(exponent):
            result = result * self
        return result

    def degree_support(self) -> set[int]:
        return {
            sum(entry != -1 for entry in word)
            for word in self.terms
        }

    def canonical(self) -> list[tuple[str, str]]:
        return [
            (
                "".join("-" if colour == -1 else str(colour) for colour in word),
                str(sy.factor(coefficient)),
            )
            for word, coefficient in sorted(self.terms.items())
        ]


def deterministic_degree_two_element() -> SquareFreeTensor:
    # Supply a monochromatic perfect matching in each colour, with different
    # physical matchings.  Thus x^3 has components in all three target
    # directions X_i; the later cancellation cannot rely on x^3 being
    # independent of the GHZ span.  The last mixed term also exercises
    # square-free killing and non-target components.
    summands = (
        SquareFreeTensor.basis({0: 0, 1: 0}, 1),
        SquareFreeTensor.basis({2: 0, 3: 0}, 2),
        SquareFreeTensor.basis({4: 0, 5: 0}, -1),
        SquareFreeTensor.basis({0: 1, 2: 1}, 3),
        SquareFreeTensor.basis({1: 1, 4: 1}, -2),
        SquareFreeTensor.basis({3: 1, 5: 1}, 1),
        SquareFreeTensor.basis({0: 2, 3: 2}, 2),
        SquareFreeTensor.basis({1: 2, 5: 2}, 1),
        SquareFreeTensor.basis({2: 2, 4: 2}, 4),
        SquareFreeTensor.basis({0: 2, 4: 1}, -3),
    )
    result = SquareFreeTensor.zero()
    for summand in summands:
        result = result + summand
    assert result.degree_support() == {2}
    assert result.power(3).terms
    assert result.power(3).degree_support() == {6}
    for colour in range(3):
        pure_word = (colour,) * SITE_COUNT
        assert result.power(3).terms[pure_word] != 0
    return result


def audit_denominator_and_cube() -> dict[str, object]:
    s, c2, c4, c6, x, target = sy.symbols("s C2 C4 C6 x T")
    normalized_2 = c2 / s
    normalized_4 = c4 / s
    normalized_6 = c6 / s
    l2 = normalized_2
    l4 = normalized_4 - normalized_2**2 / 2
    l6 = (
        normalized_6
        - normalized_2 * normalized_4
        + normalized_2**3 / 3
    )
    logarithmic_condition = sy.factor(l6 + l4 * (x + l2))
    denominator_cleared = sy.expand(6 * s**3 * logarithmic_condition)
    claimed_d = sy.expand(
        6 * s**2 * (c6 + c4 * x)
        - 3 * s * c2**2 * x
        - c2**3
    )
    assert sy.expand(denominator_cleared - claimed_d) == 0

    # Every coefficient is cubic in the cap-linear data s,C2,C4,C6.
    polynomial = sy.Poly(claimed_d, s, c2, c4, c6)
    assert {sum(monomial) for monomial in polynomial.monoms()} == {3}

    ghz_replacement = target - c4 * x - c2 * x**2 / 2 - s * x**3 / 6
    under_ghz = sy.expand(claimed_d.subs(c6, ghz_replacement))
    cube_form = sy.expand(6 * s**2 * target - (s * x + c2) ** 3)
    assert sy.expand(under_ghz - cube_form) == 0

    # The normalized hafnian equation is the cube form divided by 6*s^3.
    normalized_hafnian = sy.expand((x + c2 / s) ** 3 / 6)
    target_value_from_d = target / s
    d_solved_target = (s * x + c2) ** 3 / (6 * s**2)
    assert sy.factor(
        normalized_hafnian
        - target_value_from_d.subs(target, d_solved_target)
    ) == 0

    # The universal bad locus only uses the displayed formal expression:
    # setting s=C2=0 annihilates D for arbitrary C4,C6,x.
    assert claimed_d.subs({s: 0, c2: 0}) == 0
    for monomial in polynomial.monoms():
        s_power, c2_power, _, _ = monomial
        assert s_power > 0 or c2_power > 0

    return {
        "logarithmic_condition": str(logarithmic_condition),
        "D": str(sy.factor(claimed_d)),
        "cap_degrees": sorted({sum(monomial) for monomial in polynomial.monoms()}),
        "cube_form": str(sy.factor(cube_form)),
        "universal_kernel_substitution": str(claimed_d.subs({s: 0, c2: 0})),
    }


def audit_square_free_signature() -> dict[str, object]:
    s, k0, k1, k2 = sy.symbols("s kappa_0 kappa_1 kappa_2")
    x = deterministic_degree_two_element()
    x2 = x.power(2)
    x3 = x.power(3)
    assert x2.degree_support() == {4}
    assert x3.degree_support() == {6}

    pure = [
        SquareFreeTensor.basis({site: colour for site in range(SITE_COUNT)})
        for colour in range(3)
    ]
    assert len({next(iter(tensor.terms)) for tensor in pure}) == 3
    target = (
        pure[0].scale(k0)
        + pure[1].scale(k1)
        + pure[2].scale(k2)
    )

    c2 = x.scale(-s)
    c4 = SquareFreeTensor.zero()
    c6 = target + x3.scale(sy.Rational(1, 3) * s)
    ghz_left = (
        c6
        + c4 * x
        + (c2 * x2).scale(sy.Rational(1, 2))
        + x3.scale(sy.Rational(1, 6) * s)
    )
    assert ghz_left == target

    direct_d = (
        (c6 + c4 * x).scale(6 * s**2)
        - (c2.power(2) * x).scale(3 * s)
        - c2.power(3)
    )
    expected_d = target.scale(6 * s**2)
    assert direct_d == expected_d
    cube_d = expected_d - (x.scale(s) + c2).power(3)
    assert cube_d == expected_d
    assert x.scale(s) + c2 == SquareFreeTensor.zero()

    # Check linearity of every abstract signature coefficient in the four cap
    # coordinates.  x is fixed and introduces no additional cap dependence.
    for tensor in (SquareFreeTensor.one().scale(s), c2, c4, c6):
        for coefficient in tensor.terms.values():
            poly = sy.Poly(coefficient, s, k0, k1, k2)
            assert all(sum(monomial) <= 1 for monomial in poly.monoms())

    nonzero_coordinates = {
        word: sy.factor(coefficient)
        for word, coefficient in expected_d.terms.items()
        if coefficient != 0
    }
    assert len(nonzero_coordinates) == 3
    assert set(nonzero_coordinates.values()) == {
        6 * s**2 * k0,
        6 * s**2 * k1,
        6 * s**2 * k2,
    }

    return {
        "x_terms": x.canonical(),
        "x2_terms": len(x2.terms),
        "x3_terms": len(x3.terms),
        "GHZ_residual": (ghz_left - target).canonical(),
        "D_residual": (direct_d - expected_d).canonical(),
        "D_nonzero_coordinates": [
            ("".join(str(colour) for colour in word), str(coefficient))
            for word, coefficient in sorted(nonzero_coordinates.items())
        ],
    }


def audit_projective_bounds() -> dict[str, object]:
    degree_two_coordinates = comb(6, 2) * 3**2
    assert degree_two_coordinates == 135
    bad_codimension_upper_bound = 1 + degree_two_coordinates
    assert bad_codimension_upper_bound == 136
    coordinate_equations_upper_bound = 3**6
    assert coordinate_equations_upper_bound == 729

    # For an N-dimensional affine cap space:
    # dim ker(s,C2) >= N-136, hence projective dimension >= N-137.
    # Height <=729 gives affine cone dimension >=N-729 and projective
    # dimension >=N-730.  N>729 ensures this cone has a nonzero point.
    cases = {}
    for cap_dimension in (730, 3**8):
        kernel_affine_lower = cap_dimension - bad_codimension_upper_bound
        kernel_projective_lower = kernel_affine_lower - 1
        krull_affine_lower = cap_dimension - coordinate_equations_upper_bound
        krull_projective_lower = krull_affine_lower - 1
        assert kernel_affine_lower > 0
        assert krull_affine_lower > 0
        assert kernel_projective_lower - krull_projective_lower == 593
        cases[str(cap_dimension)] = {
            "kernel_affine_lower": kernel_affine_lower,
            "kernel_projective_lower": kernel_projective_lower,
            "krull_affine_lower": krull_affine_lower,
            "krull_projective_lower": krull_projective_lower,
        }
    assert cases[str(3**8)]["kernel_projective_lower"] == 6424
    assert cases[str(3**8)]["krull_projective_lower"] == 5831

    return {
        "degree_two_coordinates": degree_two_coordinates,
        "bad_codimension_upper_bound": bad_codimension_upper_bound,
        "D_coordinate_upper_bound": coordinate_equations_upper_bound,
        "dimension_cases": cases,
    }


def monomial_divides(
    divisor: tuple[int, ...], dividend: tuple[int, ...]
) -> bool:
    return all(left <= right for left, right in zip(divisor, dividend, strict=True))


def minimal_hitting_sets(supports: tuple[frozenset[int], ...]) -> list[frozenset[int]]:
    variables = sorted(set().union(*supports))
    hitting: list[frozenset[int]] = []
    for size in range(len(variables) + 1):
        for subset_tuple in combinations(variables, size):
            subset = frozenset(subset_tuple)
            if not all(subset & support for support in supports):
                continue
            if any(previous <= subset for previous in hitting):
                continue
            hitting.append(subset)
    return hitting


def minimal_monomials(
    generators: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    answer = []
    for candidate in sorted(set(generators), key=lambda value: (sum(value), value)):
        if any(monomial_divides(previous, candidate) for previous in answer):
            continue
        answer.append(candidate)
    return tuple(answer)


def audit_ideal_and_saturation() -> dict[str, object]:
    # Exponent order is s,k0,k1,k2.
    generators = (
        (2, 1, 0, 0),
        (2, 0, 1, 0),
        (2, 0, 0, 1),
    )
    h_exponent = (1, 1, 1, 1)
    minimal_power = next(
        power
        for power in range(1, 8)
        if any(
            monomial_divides(generator, tuple(power * exponent for exponent in h_exponent))
            for generator in generators
        )
    )
    assert minimal_power == 2

    supports = tuple(
        frozenset(index for index, exponent in enumerate(generator) if exponent)
        for generator in generators
    )
    hitting_sets = minimal_hitting_sets(supports)
    assert hitting_sets == [
        frozenset({0}),
        frozenset({1, 2, 3}),
    ]

    # The two minimal primes are P_s=(s) and
    # P_k=(k0,k1,k2).  Their monomial intersection is generated by the
    # pairwise lcms s*k_i, exactly the radical of I_D.  The original ideal
    # itself is (s^2) intersect P_k.
    prime_s = ((1, 0, 0, 0),)
    prime_k = (
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    primary_s_squared = ((2, 0, 0, 0),)

    def monomial_intersection(
        left: tuple[tuple[int, ...], ...],
        right: tuple[tuple[int, ...], ...],
    ) -> tuple[tuple[int, ...], ...]:
        lcms = tuple(
            tuple(max(a, b) for a, b in zip(first, second, strict=True))
            for first, second in product(left, right)
        )
        return minimal_monomials(lcms)

    radical_exponents = (
        (1, 1, 0, 0),
        (1, 0, 1, 0),
        (1, 0, 0, 1),
    )
    assert set(monomial_intersection(prime_s, prime_k)) == set(radical_exponents)
    assert set(monomial_intersection(primary_s_squared, prime_k)) == set(generators)

    # Exhaust all zero/nonzero patterns.  The coordinate ideal vanishes
    # exactly when s=0 or all three kappas are zero.
    vanishing_patterns = []
    for nonzero_bits in product((False, True), repeat=4):
        ideal_vanishes = all(
            any(exponent and not nonzero_bits[index]
                for index, exponent in enumerate(generator))
            for generator in generators
        )
        expected = (not nonzero_bits[0]) or not any(nonzero_bits[1:])
        assert ideal_vanishes == expected
        if ideal_vanishes:
            vanishing_patterns.append(nonzero_bits)
    assert len(vanishing_patterns) == 9

    s, k0, k1, k2, t, dummy = sy.symbols(
        "s kappa_0 kappa_1 kappa_2 localization dummy"
    )
    ideal_polynomials = (s**2 * k0, s**2 * k1, s**2 * k2)
    h = s * k0 * k1 * k2

    # Direct radical and saturation certificates.
    radical_generators = (s * k0, s * k1, s * k2)
    h_squared_multiplier = k0 * k1**2 * k2**2
    assert sy.expand(h**2 - ideal_polynomials[0] * h_squared_multiplier) == 0
    assert all(sy.Poly(generator, s, k0, k1, k2).is_sqf
               for generator in radical_generators)

    # Explicit Rabinowitsch Bezout identity:
    # 1=(1-th)(1+th)+t^2*(h^2), with h^2 replaced by an I_D multiple.
    bezout = sy.expand(
        (1 - t * h) * (1 + t * h)
        + t**2 * h_squared_multiplier * ideal_polynomials[0]
    )
    assert bezout == 1

    # A different variable order from the primary checker, with an unused
    # dummy cap coordinate, confirms that adding coordinates changes nothing.
    localized_basis = sy.groebner(
        (
            ideal_polynomials[2],
            ideal_polynomials[0],
            ideal_polynomials[1],
            1 - t * h,
        ),
        dummy,
        k2,
        t,
        s,
        k0,
        k1,
        order="grlex",
        domain=sy.QQ,
    )
    assert localized_basis.contains(sy.Integer(1))

    affine_coordinates = tuple(
        6 * polynomial.subs({s: 1, k0: 1, k1: 1, k2: 1})
        for polynomial in ideal_polynomials
    )
    assert affine_coordinates == (6, 6, 6)

    return {
        "monomial_generators": generators,
        "minimal_h_power_in_I": minimal_power,
        "minimal_prime_hitting_sets": [sorted(value) for value in hitting_sets],
        "primary_decomposition": "(s^2) intersect (kappa_0,kappa_1,kappa_2)",
        "radical_generators": [str(value) for value in radical_generators],
        "vanishing_zero_nonzero_patterns": len(vanishing_patterns),
        "h2_multiplier": str(h_squared_multiplier),
        "Rabinowitsch_Bezout_residual": str(bezout - 1),
        "localized_basis_contains_one": localized_basis.contains(sy.Integer(1)),
        "affine_normalized_coordinates": [str(value) for value in affine_coordinates],
    }


def audit_cap_form_independence_and_scope() -> dict[str, object]:
    # For W={0,1}, the diagonal tensors g_i and h_W=e0 tensor e1 are four
    # distinct tensor-basis vectors.  Their evaluation forms are independent.
    tensor_words = tuple(product(range(3), repeat=2))
    g_words = ((0, 0), (1, 1), (2, 2))
    h_word = (0, 1)
    selected_words = g_words + (h_word,)
    assert len(set(selected_words)) == 4
    evaluation_matrix = sy.zeros(4, len(tensor_words))
    word_column = {word: index for index, word in enumerate(tensor_words)}
    for row, word in enumerate(selected_words):
        evaluation_matrix[row, word_column[word]] = 1
    assert evaluation_matrix.rank() == 4

    # K with value one on these four basis vectors witnesses the complement of
    # the four hyperplanes.  The remaining five coordinates are free dummies.
    witness = sy.ones(len(tensor_words), 1)
    evaluations = tuple(
        (evaluation_matrix * witness)[row, 0] for row in range(4)
    )
    assert evaluations == (1, 1, 1, 1)

    # This audit intentionally records the logical scope: C_j were assigned as
    # independent linear boundary-signature maps.  No edge variables or
    # hafnian cofactor equations were introduced, so the construction can
    # refute consequences of the linear GHZ identity but cannot be promoted to
    # a realizable aggregate-edge counterexample.
    supplied_relations = {
        "linear_cap_dependence",
        "top_GHZ_contraction",
        "independent_s_and_kappas",
    }
    omitted_relations = {
        "shared_edge_hafnian_cofactor_formulas",
        "pair_adjugate_identity",
        "common_star_product_relations",
    }
    assert supplied_relations.isdisjoint(omitted_relations)

    return {
        "W_size": 2,
        "cap_dimension": len(tensor_words),
        "independent_form_rank": evaluation_matrix.rank(),
        "open_set_witness_values": [int(value) for value in evaluations],
        "supplied_relations": sorted(supplied_relations),
        "deliberately_omitted_relations": sorted(omitted_relations),
        "scope": "abstract linear signature, not a common-edge realization",
    }


def build_ledger() -> dict[str, object]:
    return {
        "denominator_and_cube": audit_denominator_and_cube(),
        "square_free_signature": audit_square_free_signature(),
        "projective_bounds": audit_projective_bounds(),
        "ideal_and_saturation": audit_ideal_and_saturation(),
        "cap_forms_and_scope": audit_cap_form_independence_and_scope(),
    }


def main() -> None:
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if FROZEN_LEDGER_SHA256 != "TO_BE_FROZEN":
        assert digest == FROZEN_LEDGER_SHA256

    print("D cap degree:", ledger["denominator_and_cube"]["cap_degrees"])
    print("square-free GHZ and D residuals: zero")
    print("degree-two / D coordinate bounds:",
          ledger["projective_bounds"]["degree_two_coordinates"],
          ledger["projective_bounds"]["D_coordinate_upper_bound"])
    dimensions = ledger["projective_bounds"]["dimension_cases"][str(3**8)]
    print("bad / Krull projective bounds at |W|=8:",
          dimensions["kernel_projective_lower"],
          dimensions["krull_projective_lower"])
    print("minimal h power in I_D:",
          ledger["ideal_and_saturation"]["minimal_h_power_in_I"])
    print("localized basis contains 1:",
          ledger["ideal_and_saturation"]["localized_basis_contains_one"])
    print("abstract cap-form rank:",
          ledger["cap_forms_and_scope"]["independent_form_rank"])
    print("scope:", ledger["cap_forms_and_scope"]["scope"])
    print("ledger sha256:", digest)
    print("clean-room cap projective-height audit: PASS")


if __name__ == "__main__":
    main()
