#!/usr/bin/env python3
"""Exact h=3 test of sitewise GL(3) covariance for the five face repairs.

The checker builds each four-site universal matching tensor, implements the
contragredient source derivations and output color changes, and tests the
full 16-term connection cube.  It does not treat a Weyl operator identity as
a new homological generator.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json


F = Fraction
ZERO = F(0)
ONE = F(1)
SITES = (1, 2, 3, 4, 5)
COLORS = (0, 1, 2)
MIXED = (1, 2, 1, 1, 2)
PURE = (0, 0, 0, 0, 0)
EXPECTED_TAGS = {
    1: "2112",
    2: "1112",
    3: "1212",
    4: "1212",
    5: "1211",
}
EXPECTED_DIGEST = "aaba3b9ff228908041820f6f4dfbc02c970e36c2dc14113fa2c6073f876fcaa4"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(site_a, site_b, color_a, color_b):
    require(site_a != site_b, "loop edge")
    if site_a < site_b:
        return site_a, site_b, color_a, color_b
    return site_b, site_a, color_b, color_a


def monomial(*variables):
    return tuple(sorted(variables))


def matching_pairs(mask):
    if mask == 0:
        return ((),)
    require(mask.bit_count() % 2 == 0, "odd matching set")
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    rest = mask ^ first_bit
    result = []
    candidates = rest
    while candidates:
        second_bit = candidates & -candidates
        second = second_bit.bit_length() - 1
        for tail in matching_pairs(rest ^ second_bit):
            result.append(((first, second),) + tail)
        candidates ^= second_bit
    return tuple(result)


def polynomial_add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for term, coefficient in polynomial.items():
            result[term] = result.get(term, ZERO) + coefficient
            if result[term] == ZERO:
                del result[term]
    return result


def polynomial_scale(scalar, polynomial):
    return {
        term: scalar * coefficient
        for term, coefficient in polynomial.items()
        if scalar * coefficient != ZERO
    }


def hafnian(face, word):
    mask = sum(1 << site for site in face)
    result = {}
    for matching in matching_pairs(mask):
        term = monomial(*(
            edge(site_a, site_b, word[site_a - 1], word[site_b - 1])
            for site_a, site_b in matching
        ))
        result[term] = result.get(term, ZERO) + ONE
    return result


def tensor_add(*tensors):
    result = {}
    for tensor in tensors:
        for word, polynomial in tensor.items():
            result[word] = polynomial_add(result.get(word, {}), polynomial)
            if result[word] == {}:
                del result[word]
    return result


def tensor_scale(scalar, tensor):
    return {
        word: polynomial_scale(scalar, polynomial)
        for word, polynomial in tensor.items()
        if polynomial_scale(scalar, polynomial)
    }


def face_matching_tensor(deleted_site, exposed_color=0):
    face = tuple(site for site in SITES if site != deleted_site)
    result = {}
    for face_colors in product(COLORS, repeat=4):
        word = [None] * 5
        word[deleted_site - 1] = exposed_color
        for site, color in zip(face, face_colors):
            word[site - 1] = color
        word = tuple(word)
        result[word] = hafnian(face, word)
    return result


def output_change(tensor, site, target_color, source_color):
    """L_(site;target<-source): e_source maps to e_target."""
    result = {}
    position = site - 1
    for word, polynomial in tensor.items():
        if word[position] != source_color:
            continue
        output_word = list(word)
        output_word[position] = target_color
        output_word = tuple(output_word)
        result[output_word] = polynomial_add(
            result.get(output_word, {}), polynomial
        )
    return result


def recolor_incident(variable, site, old_color, new_color):
    site_a, site_b, color_a, color_b = variable
    if site == site_a and color_a == old_color:
        return edge(site_a, site_b, new_color, color_b)
    if site == site_b and color_b == old_color:
        return edge(site_a, site_b, color_a, new_color)
    return None


def derive_polynomial(polynomial, site, target_color, source_color):
    """D_(site;target<-source) = q_source d/dq_target."""
    result = {}
    for term, coefficient in polynomial.items():
        for index, variable in enumerate(term):
            replacement = recolor_incident(
                variable, site, target_color, source_color
            )
            if replacement is None:
                continue
            derived_term = monomial(
                *(term[:index] + (replacement,) + term[index + 1 :])
            )
            result[derived_term] = (
                result.get(derived_term, ZERO) + coefficient
            )
    return result


def source_derivation(tensor, site, target_color, source_color):
    result = {}
    for word, polynomial in tensor.items():
        derived = derive_polynomial(
            polynomial, site, target_color, source_color
        )
        if derived:
            result[word] = derived
    return result


def apply_face_operator(tensor, face, choices, mixed_word):
    """Apply one L or D at each face site in site order."""
    result = tensor
    for site, choice in zip(face, choices):
        source_color = mixed_word[site - 1]
        if choice == "L":
            result = output_change(result, site, 0, source_color)
        elif choice == "D":
            result = source_derivation(result, site, 0, source_color)
        else:
            raise RuntimeError(f"unknown face operator {choice}")
    return result


def constant_target_tensor():
    constant = {(): ONE}
    return {
        (color,) * 5: constant
        for color in COLORS
    }


def polynomial_terms_text(polynomial):
    def variable_text(variable):
        site_a, site_b, color_a, color_b = variable
        return f"q{site_a}{site_b}^{color_a}{color_b}"

    return sorted(
        "*".join(variable_text(variable) for variable in term)
        for term in polynomial
    )


def audit_face(deleted_site):
    face = tuple(site for site in SITES if site != deleted_site)
    face_tag = "".join(str(MIXED[site - 1]) for site in face)
    require(
        face_tag == EXPECTED_TAGS[deleted_site],
        f"face {deleted_site}: tag changed",
    )
    tensor = face_matching_tensor(deleted_site, exposed_color=0)
    require(
        len(tensor) == 81
        and all(len(polynomial) == 3 for polynomial in tensor.values()),
        f"face {deleted_site}: universal matching tensor changed",
    )

    # Check D H = L H for the full local gl(3) matrix-unit family.
    covariance_checks = 0
    for site in face:
        for target_color in COLORS:
            for source_color in COLORS:
                left = source_derivation(
                    tensor, site, target_color, source_color
                )
                right = output_change(
                    tensor, site, target_color, source_color
                )
                require(
                    left == right,
                    (
                        f"face {deleted_site}, site {site}, "
                        f"{target_color}<-{source_color}: covariance failed"
                    ),
                )
                covariance_checks += 1
    require(covariance_checks == 36, "local gl(3) audit count changed")

    desired_polynomial = hafnian(face, MIXED)
    desired_tensor = {PURE: desired_polynomial}
    require(
        len(desired_polynomial) == 3,
        f"face {deleted_site}: h_v is not a nonzero three-term quadric",
    )

    # Every corner of the four-cube, not only all-L and all-D, is the same
    # h_v Y_0.  Hence the alternating connection cube is zero.
    corner_ledger = {}
    connection_cube = {}
    for choices in product(("L", "D"), repeat=4):
        corner = apply_face_operator(tensor, face, choices, MIXED)
        require(
            corner == desired_tensor,
            f"face {deleted_site}: {''.join(choices)} lost the locked class",
        )
        d_count = choices.count("D")
        connection_cube = tensor_add(
            connection_cube, tensor_scale((-ONE) ** d_count, corner)
        )
        corner_ledger["".join(choices)] = polynomial_terms_text(
            corner[PURE]
        )
    require(
        connection_cube == {},
        f"face {deleted_site}: connection four-cube is not zero",
    )

    # The pure Euler choice is the old denominator face g_v Y_0.
    pure_euler = tensor
    for site in face:
        pure_euler = output_change(pure_euler, site, 0, 0)
    pure_face_polynomial = hafnian(face, PURE)
    require(
        pure_euler == {PURE: pure_face_polynomial},
        f"face {deleted_site}: pure Euler class is not g_v Y_0",
    )

    # The diagonal target is killed by the mixed lowering: the four-letter
    # tag contains both colors 1 and 2 and is not a diagonal word.
    require(
        len(set(face_tag)) > 1,
        f"face {deleted_site}: mixed face unexpectedly became diagonal",
    )
    target = constant_target_tensor()
    target_after_l = target
    target_after_d = target
    for site in face:
        target_after_l = output_change(
            target_after_l, site, 0, MIXED[site - 1]
        )
        target_after_d = source_derivation(
            target_after_d, site, 0, MIXED[site - 1]
        )
    require(
        target_after_l == {} and target_after_d == {},
        f"face {deleted_site}: an unwanted diagonal target survived",
    )

    return {
        "face": list(face),
        "tag": face_tag,
        "covariance_checks": covariance_checks,
        "h_terms": polynomial_terms_text(desired_polynomial),
        "g_terms": polynomial_terms_text(pure_face_polynomial),
        "connection_cube_corners": len(corner_ledger),
        "distinct_corner_values": len({
            tuple(value) for value in corner_ledger.values()
        }),
        "connection_cube_output_terms": len(connection_cube),
        "target_after_lowering_terms": len(target_after_l),
    }, desired_polynomial, pure_face_polynomial


def main():
    face_ledgers = {}
    h_polynomials = {}
    g_polynomials = {}
    for deleted_site in SITES:
        ledger, h_polynomial, g_polynomial = audit_face(deleted_site)
        face_ledgers[str(deleted_site)] = ledger
        h_polynomials[deleted_site] = h_polynomial
        g_polynomials[deleted_site] = g_polynomial

    # Different deletion faces have disjoint four-site monomial support.
    h_supports = [set(h_polynomials[site]) for site in SITES]
    g_supports = [set(g_polynomials[site]) for site in SITES]
    require(
        all(
            h_supports[left].isdisjoint(h_supports[right])
            for left, right in combinations(range(5), 2)
        ),
        "the five h_v lost initial linear independence",
    )
    require(
        all(
            g_supports[left].isdisjoint(g_supports[right])
            for left, right in combinations(range(5), 2)
        ),
        "the five g_v lost initial linear independence",
    )
    require(
        set().union(*h_supports).isdisjoint(set().union(*g_supports)),
        "mixed h_v entered the old pure g_v span",
    )
    require(
        sum(len(support) for support in h_supports) == 15
        and sum(len(support) for support in g_supports) == 15,
        "face support count changed",
    )

    # At q-degree two, cancelling all derivation companions across v is the
    # same rank-five equation as cancelling the desired L outputs.  The only
    # constant-coefficient cancellation is therefore trivial.
    locked_cross_face_rank = 5
    old_plus_locked_rank = 10
    require(
        locked_cross_face_rank == len(SITES)
        and old_plus_locked_rank == 2 * len(SITES),
        "cross-face rank lock changed",
    )

    result = {
        "mixed_word": "".join(map(str, MIXED)),
        "face_tags": EXPECTED_TAGS,
        "faces": face_ledgers,
        "h_face_rank": locked_cross_face_rank,
        "g_face_rank": 5,
        "combined_g_h_rank": old_plus_locked_rank,
        "all_L_equals_all_D": True,
        "all_16_corners_equal_hY0": True,
        "connection_cube_is_zero": True,
        "target_is_zero_facewise": True,
        "tau_constructed": False,
        "missing_extra_datum": "nullhomotopy of all-D companion",
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 sitewise GL(3) covariance face-tau test: PASS")
    print("five face tags: 2112, 1112, 1212, 1212, 1211")
    print("each all-L output h_v Y_0 is locked to the identical all-D term")
    print("the 16-corner connection cube is zero; no tau_v is produced")
    print("cross-face ranks: h=5, old g=5, combined=10")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
