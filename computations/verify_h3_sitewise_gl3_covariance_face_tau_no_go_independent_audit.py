#!/usr/bin/env python3
"""Independent audit of the h=3 sitewise-covariance face calculation.

This deliberately does not import the audited checker.  Four-point matchings,
matrix-unit actions, target actions, and rational ranks are rebuilt below.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json


SITES = (1, 2, 3, 4, 5)
COLORS = (0, 1, 2)
MIXED = (1, 2, 1, 1, 2)
PURE = (0, 0, 0, 0, 0)


def check(test, message):
    if not test:
        raise RuntimeError(message)


def canonical_edge(i, a, j, b):
    check(i != j, "loop")
    return (i, a, j, b) if i < j else (j, b, i, a)


def four_pairings(face):
    a, b, c, d = face
    return (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))


def face_hafnian(face, word):
    answer = {}
    for pairing in four_pairings(face):
        monomial = tuple(sorted(
            canonical_edge(i, word[i - 1], j, word[j - 1])
            for i, j in pairing
        ))
        answer[monomial] = answer.get(monomial, 0) + 1
    return answer


def add_polynomial(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def add_tensor(left, right, scale=1):
    result = {word: dict(polynomial) for word, polynomial in left.items()}
    for word, polynomial in right.items():
        result[word] = add_polynomial(result.get(word, {}), polynomial, scale)
        if not result[word]:
            del result[word]
    return result


def universal_face_tensor(deleted):
    face = tuple(site for site in SITES if site != deleted)
    tensor = {}
    for face_word in product(COLORS, repeat=4):
        word = [0] * 5
        for site, color in zip(face, face_word):
            word[site - 1] = color
        tensor[tuple(word)] = face_hafnian(face, tuple(word))
    return tensor


def output_matrix_unit(tensor, site, new, old):
    answer = {}
    for word, polynomial in tensor.items():
        if word[site - 1] != old:
            continue
        changed = list(word)
        changed[site - 1] = new
        changed = tuple(changed)
        answer[changed] = add_polynomial(
            answer.get(changed, {}), polynomial
        )
    return answer


def replace_endpoint(edge, site, old, new):
    i, a, j, b = edge
    if i == site and a == old:
        return (i, new, j, b)
    if j == site and b == old:
        return (i, a, j, new)
    return None


def source_matrix_unit(tensor, site, new, old):
    """Apply sum q_old * partial/partial q_new at the named endpoint."""
    answer = {}
    for word, polynomial in tensor.items():
        derived = {}
        for monomial, coefficient in polynomial.items():
            for position, edge in enumerate(monomial):
                replacement = replace_endpoint(edge, site, new, old)
                if replacement is None:
                    continue
                changed = list(monomial)
                changed[position] = replacement
                changed = tuple(sorted(changed))
                derived[changed] = derived.get(changed, 0) + coefficient
        if derived:
            answer[word] = derived
    return answer


def apply_selected_corner(tensor, face, corner):
    answer = tensor
    for site, operator in zip(face, corner):
        old = MIXED[site - 1]
        if operator == "L":
            answer = output_matrix_unit(answer, site, 0, old)
        else:
            answer = source_matrix_unit(answer, site, 0, old)
    return answer


def parse_monomial(text):
    factors = []
    for factor in text.split("*"):
        ij, colors = factor.split("^")
        i, j = int(ij[1]), int(ij[2])
        a, b = int(colors[0]), int(colors[1])
        factors.append(canonical_edge(i, a, j, b))
    return tuple(sorted(factors))


EXPECTED_H = {
    1: "q23^21*q45^12 q24^21*q35^12 q25^22*q34^11",
    2: "q13^11*q45^12 q14^11*q35^12 q15^12*q34^11",
    3: "q12^12*q45^12 q14^11*q25^22 q15^12*q24^21",
    4: "q12^12*q35^12 q13^11*q25^22 q15^12*q23^21",
    5: "q12^12*q34^11 q13^11*q24^21 q14^11*q23^21",
}


def expected_polynomial(description):
    return {parse_monomial(term): 1 for term in description.split()}


def rank(rows):
    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix))
             if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def polynomial_rank(polynomials):
    basis = sorted({m for polynomial in polynomials for m in polynomial})
    rows = [[polynomial.get(monomial, 0) for monomial in basis]
            for polynomial in polynomials]
    return rank(rows)


def diagonal_target():
    return {(color,) * 5: {(): 1} for color in COLORS}


def audit_face(deleted):
    face = tuple(site for site in SITES if site != deleted)
    tensor = universal_face_tensor(deleted)
    check(len(tensor) == 81, f"face {deleted}: tensor size")
    check(all(sum(p.values()) == 3 for p in tensor.values()),
          f"face {deleted}: matching count")

    covariance_count = 0
    for site in face:
        for new in COLORS:
            for old in COLORS:
                check(
                    source_matrix_unit(tensor, site, new, old)
                    == output_matrix_unit(tensor, site, new, old),
                    f"face {deleted}: covariance at {site},{new}<-{old}",
                )
                covariance_count += 1

    expected_h = expected_polynomial(EXPECTED_H[deleted])
    direct_h = face_hafnian(face, MIXED)
    check(direct_h == expected_h, f"face {deleted}: displayed h formula")

    alternating_cube = {}
    corner_values = []
    target_cube = {}
    for corner in product("LD", repeat=4):
        value = apply_selected_corner(tensor, face, corner)
        check(value == {PURE: expected_h},
              f"face {deleted}: corner {''.join(corner)}")
        corner_values.append(value)
        sign = -1 if corner.count("D") % 2 else 1
        alternating_cube = add_tensor(alternating_cube, value, sign)

        target_value = apply_selected_corner(diagonal_target(), face, corner)
        check(target_value == {},
              f"face {deleted}: target corner {''.join(corner)} survived")
        target_cube = add_tensor(target_cube, target_value, sign)

    check(alternating_cube == {}, f"face {deleted}: nonzero cube")
    check(target_cube == {}, f"face {deleted}: nonzero target cube")
    check(corner_values[0] == corner_values[-1],
          f"face {deleted}: all-L/all-D lock")

    pure_tensor = tensor
    for site in face:
        pure_tensor = output_matrix_unit(pure_tensor, site, 0, 0)
    expected_g = face_hafnian(face, PURE)
    check(pure_tensor == {PURE: expected_g}, f"face {deleted}: pure face")

    return {
        "face": face,
        "tag": "".join(str(MIXED[site - 1]) for site in face),
        "covariance": covariance_count,
        "corners": len(corner_values),
        "target_corners_zero": 16,
        "h_terms": len(expected_h),
        "g_terms": len(expected_g),
    }, expected_h, expected_g


def main():
    ledgers = []
    h_polynomials = []
    g_polynomials = []
    for deleted in SITES:
        ledger, h, g = audit_face(deleted)
        ledgers.append(ledger)
        h_polynomials.append(h)
        g_polynomials.append(g)

    check([entry["tag"] for entry in ledgers]
          == ["2112", "1112", "1212", "1212", "1211"], "face tags")
    check(polynomial_rank(h_polynomials) == 5, "h rank")
    check(polynomial_rank(g_polynomials) == 5, "g rank")
    check(polynomial_rank(g_polynomials + h_polynomials) == 10, "g+h rank")

    # The two lists are literally equal face by face: covariance gives one
    # locked copy, not an additional relation or a chain nullhomotopy.
    all_l = []
    all_d = []
    for deleted in SITES:
        face = tuple(site for site in SITES if site != deleted)
        tensor = universal_face_tensor(deleted)
        all_l.append(apply_selected_corner(tensor, face, "LLLL")[PURE])
        all_d.append(apply_selected_corner(tensor, face, "DDDD")[PURE])
    check(all_l == all_d == h_polynomials, "cross-face residue lock")
    check(polynomial_rank(all_l) == polynomial_rank(all_d) == 5,
          "locked companion rank")

    payload = {
        "faces": ledgers,
        "local_covariance_checks": sum(x["covariance"] for x in ledgers),
        "universal_corners": sum(x["corners"] for x in ledgers),
        "target_corners_zero": sum(x["target_corners_zero"] for x in ledgers),
        "h_rank": polynomial_rank(h_polynomials),
        "g_rank": polynomial_rank(g_polynomials),
        "combined_rank": polynomial_rank(g_polynomials + h_polynomials),
        "all_L_equals_all_D": all_l == all_d,
        "scope": "bare covariance cube and constant cross-face cancellation only",
    }
    digest = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"))
                    .encode()).hexdigest()
    check(digest == "715d547ff6ec44e1be907193d64d64c7efe603476448fa3ac3d93c9db32f81b7",
          f"ledger digest changed: {digest}")

    print("independent sitewise GL(3) face audit: PASS")
    print("local identities 180; universal corners 80; target corners zero 80")
    print("ranks h=5, g=5, combined=10; all-L equals all-D facewise")
    print("scope: bare covariance cube and constant cross-face cancellation only")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
