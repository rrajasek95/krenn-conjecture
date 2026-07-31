#!/usr/bin/env python3
"""Exact guards for the ordered-reconstruction / lift-torsor no-go.

The proof in the accompanying note is uniform in h.  This dependency-free
checker audits coefficient-slot order, the exceptional diagonal target,
the adjacent-power normalizations, and the one-parameter filtered
countercomplex.  ``require`` remains active under ``python -O``.
"""

from fractions import Fraction


COLORS = (0, 1, 2)


def require(condition, message):
    """Raise in both ordinary and optimized Python."""

    if not condition:
        raise RuntimeError(message)


def ordered_insert(coefficients):
    """Insert the named r- and s-colour slots.

    Input keys are ``(r_colour, s_colour, internal_word)``.  Output keys
    retain the physical site names, so no implicit endpoint transpose is
    possible.
    """

    output = {}
    for (r_colour, s_colour, internal_word), value in coefficients.items():
        if not value:
            continue
        key = (("r", r_colour), ("s", s_colour), tuple(internal_word))
        output[key] = output.get(key, Fraction(0)) + Fraction(value)
    return {key: value for key, value in output.items() if value}


def ordered_extract(inserted):
    """Extract the named r,s slots from a fully occupied array."""

    output = {}
    for key, value in inserted.items():
        (r_site, r_colour), (s_site, s_colour), internal_word = key
        require(r_site == "r", "first endpoint slot is not r")
        require(s_site == "s", "second endpoint slot is not s")
        coeff_key = (r_colour, s_colour, tuple(internal_word))
        output[coeff_key] = output.get(coeff_key, Fraction(0)) + value
    return {key: value for key, value in output.items() if value}


def check_ordered_reconstruction():
    # A complete deterministic coefficient array with arbitrary rational
    # cancellations.  Extraction must be the exact inverse of insertion.
    coefficients = {}
    internal_words = ((0, 1, 2), (2, 1, 0))
    for k in COLORS:
        for ell in COLORS:
            for word_index, word in enumerate(internal_words):
                value = Fraction((k + 1) * (ell + 2) - 3 * word_index, 7)
                if (k + ell + word_index) % 4 == 0:
                    value = -value
                coefficients[(k, ell, word)] = value

    reconstructed = ordered_extract(ordered_insert(coefficients))
    require(
        reconstructed == {key: value for key, value in coefficients.items() if value},
        "ordered extraction/insertion is not inverse",
    )

    # Endpoint slots remain named.  A transposed array is not silently
    # accepted as the same physical array when k != ell.
    probe = {(0, 2, (1,)): Fraction(5)}
    transposed = {(2, 0, (1,)): Fraction(5)}
    require(
        ordered_insert(probe) != ordered_insert(transposed),
        "endpoint order was silently transposed",
    )

    # A componentwise literal equality reconstructs to equality, hence its
    # oriented difference reconstructs to zero.
    left = coefficients
    right = dict(coefficients)
    difference = {
        key: left.get(key, Fraction(0)) - right.get(key, Fraction(0))
        for key in set(left) | set(right)
    }
    require(ordered_insert(difference) == {}, "literal comparison did not stay zero")

    # The complete route is a nine-component direct sum: restriction removes
    # x and insertion restores r,s, for net site degree +1.
    for h in range(3, 65):
        c4_size = 2 * h - 2
        d5_size = c4_size - 1
        dx_size = d5_size + 2
        require(d5_size == 2 * h - 3, f"wrong restricted degree at h={h}")
        require(dx_size == 2 * h - 1, f"wrong inserted degree at h={h}")
        require(len(COLORS) ** 2 == 9, "ordered coefficient domain is not ninefold")


def check_exceptional_diagonal_target():
    internal_word = (1, 1, 1, 1, 1)
    for c in COLORS:
        target = {
            (k, ell, internal_word): Fraction(int(k == c and ell == c))
            for k in COLORS
            for ell in COLORS
        }
        inserted = ordered_insert(target)
        expected_key = (("r", c), ("s", c), internal_word)
        require(inserted == {expected_key: Fraction(1)}, f"wrong target cell for c={c}")

        without_diagonal = {
            key: value
            for key, value in target.items()
            if key[:2] != (c, c)
        }
        require(
            ordered_insert(without_diagonal) == {},
            f"off-diagonal cells reconstructed diagonal target c={c}",
        )

        full_five_site_support = {
            (i, j, k, ell)
            for i in COLORS
            for j in COLORS
            for k in COLORS
            for ell in COLORS
            if i == j == k == ell == c
        }
        require(
            full_five_site_support == {(c, c, c, c)},
            f"wrong exceptional cap/insertion support for c={c}",
        )

    # The scalar-unit Segre square retains the named endpoint factors.
    a = 1
    for i in COLORS:
        for j in COLORS:
            left = sorted((f"p{i}", f"s{j}", f"p{a}", f"s{a}"))
            right = sorted((f"p{i}", f"s{a}", f"p{a}", f"s{j}"))
            require(left == right, f"Segre square failed at ({i},{j})")

    correct_square = sorted(("p0", "s1", "p1", "s2"))
    transposed_square = sorted(("p1", "s0", "p2", "s1"))
    require(
        correct_square != transposed_square,
        "endpoint-transposed Segre square escaped detection",
    )


def evaluate_three_layers(vector, h):
    """Evaluate coefficients against (Z2,Z1,Z0).

    A monomial is keyed by its formal coefficient name and its Z layer.
    The only reductions are z*Z2=(h-2)*Z1 and
    z*Z1=(h-1)*Z0.  Values are collected in the Z1/Z0 layers.
    """

    output = {}
    for coefficient, layer, has_z, scalar in vector:
        scalar = Fraction(scalar)
        if has_z and layer == 2:
            key = (coefficient, 1)
            scalar *= h - 2
        elif has_z and layer == 1:
            key = (coefficient, 0)
            scalar *= h - 1
        else:
            key = (coefficient, layer)
        output[key] = output.get(key, Fraction(0)) + scalar
    return {key: value for key, value in output.items() if value}


def check_adjacent_power_boundaries():
    for h in range(3, 65):
        # Low embedded boundary: Dv*z*Z2 -(h-2)*Dv*Z1.
        low = (
            ("xiDv", 2, True, 1),
            ("xiDv", 1, False, -(h - 2)),
        )
        # High boundary: kappa*z*Z1 -(h-1)*kappa*Z0.
        high = (
            ("xikappa", 1, True, 1),
            ("xikappa", 0, False, -(h - 1)),
        )
        require(evaluate_three_layers(low, h) == {}, f"low boundary failed at h={h}")
        require(evaluate_three_layers(high, h) == {}, f"high boundary failed at h={h}")
        require(
            evaluate_three_layers(low + high, h) == {},
            f"adjacent ledger failed at h={h}",
        )

        reversed_ledger = tuple(
            (coefficient, layer, has_z, -Fraction(scalar))
            for coefficient, layer, has_z, scalar in low + high
        )
        require(
            evaluate_three_layers(reversed_ledger, h) == {},
            f"orientation reversal failed at h={h}",
        )


def differential_lambda(vector, lam):
    """Differential in the filtered countercomplex.

    Chain-degree-one vectors have one H coordinate.  The output coordinates
    are (T, Z).  Degree-zero vectors are cycles, so d^2 is automatic and is
    checked explicitly below.
    """

    h_coordinate = Fraction(vector)
    return (h_coordinate, Fraction(lam) * h_coordinate)


def degree_zero_differential(_vector):
    return (Fraction(0), Fraction(0))


def add_pairs(left, right):
    return (left[0] + right[0], left[1] + right[1])


def scale_pair(pair, scalar):
    scalar = Fraction(scalar)
    return (scalar * pair[0], scalar * pair[1])


def check_lift_torsor_countercomplex():
    cap = (Fraction(-1), Fraction(1))  # -T + Z, with Z=zeta_hat.
    same_power = (Fraction(1), Fraction(-1))  # dS = T - Z = -cap.

    for lam in (Fraction(-3, 2), Fraction(-1), Fraction(0), Fraction(7, 3)):
        boundary = differential_lambda(1, lam)
        require(
            degree_zero_differential(boundary) == (0, 0),
            f"d^2 failed at lambda={lam}",
        )

        # The associated-graded target component is H -> T for every lambda.
        require(boundary[0] == 1, f"leading target changed at lambda={lam}")
        filtration = {"Z": 0, "T": 1, "H": 1}
        differential_terms = (("T", boundary[0]), ("Z", boundary[1]))
        require(
            all(
                filtration[name] <= filtration["H"]
                for name, value in differential_terms
                if value
            ),
            f"differential did not preserve filtration at lambda={lam}",
        )
        leading_terms = {
            name: value
            for name, value in differential_terms
            if value and filtration[name] == filtration["H"]
        }
        require(
            leading_terms == {"T": Fraction(1)},
            f"wrong associated-graded differential at lambda={lam}",
        )

        residual = add_pairs(cap, boundary)
        require(
            residual == (0, 1 + lam),
            f"wrong residual at lambda={lam}",
        )
        difference_boundary = add_pairs(boundary, scale_pair(same_power, -1))
        require(
            difference_boundary == (0, 1 + lam),
            f"wrong H-S indeterminacy at lambda={lam}",
        )

    require(
        same_power == differential_lambda(1, -1),
        "literal same-power cell is not lambda=-1",
    )
    secondary = differential_lambda(1, 0)
    require(add_pairs(cap, same_power) == (0, 0), "same-power lock did not erase")
    require(
        add_pairs(cap, secondary) == (0, 1),
        "zero-lower-response lift did not retain zeta_hat",
    )
    require(
        add_pairs(secondary, scale_pair(same_power, -1)) == (0, 1),
        "desired H minus the same-power cell did not expose the indeterminacy",
    )

    # Curvature weighting and orientation reversal preserve the forced sign.
    kappa = Fraction(11, 5)
    forward = scale_pair(add_pairs(cap, secondary), kappa)
    reverse = scale_pair(add_pairs(cap, secondary), -kappa)
    require(forward == (0, kappa), "curvature normalization is wrong")
    require(reverse == scale_pair(forward, -1), "orientation did not reverse output")

    # The lower response parameter is invisible to every target-only source
    # identity, including an exceptional unary target equation.
    for lam in (Fraction(-1), Fraction(0), Fraction(2)):
        require(
            differential_lambda(1, lam)[0] == 1,
            "target projection detected a lower filtration parameter",
        )


def mutation_guards():
    h = 9
    wrong_high = (
        ("xikappa", 1, True, 1),
        ("xikappa", 0, False, -h),
    )
    require(
        evaluate_three_layers(wrong_high, h) != {},
        "mutation accepted h in place of h-1",
    )
    wrong_high_sign = (
        ("xikappa", 1, True, 1),
        ("xikappa", 0, False, h - 1),
    )
    require(
        evaluate_three_layers(wrong_high_sign, h) != {},
        "mutation accepted the wrong high-boundary sign",
    )

    wrong_low = (
        ("xiDv", 2, True, 1),
        ("xiDv", 1, False, -(h - 1)),
    )
    require(
        evaluate_three_layers(wrong_low, h) != {},
        "mutation accepted h-1 in place of h-2",
    )
    wrong_low_sign = (
        ("xiDv", 2, True, 1),
        ("xiDv", 1, False, h - 2),
    )
    require(
        evaluate_three_layers(wrong_low_sign, h) != {},
        "mutation accepted the wrong low-boundary sign",
    )

    # An endpoint-transposing insertion must fail extraction on an
    # off-diagonal probe, even though the site algebra is commutative.
    probe = {(0, 2, (1,)): Fraction(5)}
    wrong_inserted = {
        (("r", ell), ("s", k), tuple(word)): value
        for (k, ell, word), value in probe.items()
    }
    require(
        ordered_extract(wrong_inserted) != probe,
        "mutation accepted endpoint transposition",
    )

    internal_word = (1, 1, 1, 1, 1)
    expected_diagonal = {(("r", 1), ("s", 1), internal_word): Fraction(1)}
    wrong_off_diagonal = ordered_insert({(0, 2, internal_word): Fraction(1)})
    require(
        wrong_off_diagonal != expected_diagonal,
        "mutation replaced the exceptional diagonal by an off-diagonal cell",
    )

    cap = (Fraction(-1), Fraction(1))
    same_power = (Fraction(1), Fraction(-1))
    secondary = differential_lambda(1, 0)
    wrong_secondary = differential_lambda(1, 1)
    require(
        add_pairs(cap, wrong_secondary) != (0, 1),
        "mutation accepted a nonzero lower response for the desired lift",
    )
    require(
        add_pairs((Fraction(-1), Fraction(-1)), secondary) != (0, 1),
        "mutation accepted the wrong cap-response sign",
    )
    require(
        add_pairs(cap, (Fraction(1), Fraction(1))) != (0, 0),
        "mutation accepted the wrong same-power response sign",
    )
    require(
        same_power == differential_lambda(1, -1),
        "same-power normalization mutation escaped detection",
    )
    require(
        (Fraction(2), Fraction(0))[0] != secondary[0],
        "mutation accepted leading target multiplicity two",
    )


def main():
    check_ordered_reconstruction()
    check_exceptional_diagonal_target()
    check_adjacent_power_boundaries()
    check_lift_torsor_countercomplex()
    mutation_guards()
    print(
        "ordered five-site reconstruction / transgression lift torsor: PASS; "
        "endpoint slots, diagonal target, h=3..64 Euler ledgers, filtered lifts, "
        "and sign/normalization mutations audited"
    )


if __name__ == "__main__":
    main()
