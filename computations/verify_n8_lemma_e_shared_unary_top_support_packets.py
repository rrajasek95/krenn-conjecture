#!/usr/bin/env python3
"""Support and coefficient guards for the normalized Lemma-E shared packet.

Normalize the deficient reciprocal arm to A_01=E_00.  Lemma E gives

    row_0(A_0x)=0 (x != 1),       H_{2,...,7}=e_0^tensor6.

The other shared reciprocal arm has outgoing colour one.  Up to the colour
stabilizer there are two head cases A_02=E_11 and A_02=E_21.  For each case
this checker freezes a deterministic deletion-irredundant support-shadow
packet for the literal residual unary-top equation and all nine pair rows.
The shadow is SAT, but three two-term source rows form an odd Laurent circuit,
so the corresponding full-support coefficient torus is empty.

This is a bounded frontier result.  It does not classify every support of the
normalized packet; in particular deletion-irredundant does not mean globally
minimum cardinality without a separate support-poset certificate.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json


COLORS = (0, 1, 2)
SITES = tuple(range(8))
P, Q, R = 0, 1, 2
RESIDUAL = tuple(range(2, 8))
EXPECTED_DIGEST = "125fa4d16c3e4e25dc7fda24706e398b27540acdb5416aa3a4973e5b18df6410"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS8 = tuple(perfect_matchings(SITES))
MATCHINGS6 = tuple(perfect_matchings(RESIDUAL))
require(len(MATCHINGS8) == 105 and len(MATCHINGS6) == 15,
        "perfect-matching counts changed")


# Cells are (left_site,right_site,left_colour,right_colour).
PACKETS = {
    # Shared arm A_02=E_11 (diagonal head case).  Together with fixed E_00
    # and E_11 this has 39 cells.
    1: (
        (0, 4, 2, 1), (0, 4, 2, 2), (0, 5, 2, 0),
        (0, 6, 1, 0), (0, 6, 1, 1), (1, 3, 2, 2),
        (1, 4, 1, 1), (1, 4, 1, 2), (1, 4, 2, 1),
        (1, 4, 2, 2), (1, 5, 1, 0), (1, 5, 2, 1),
        (1, 7, 2, 0), (1, 7, 2, 2), (2, 3, 0, 2),
        (2, 4, 1, 0), (2, 5, 0, 0), (2, 5, 0, 1),
        (2, 6, 2, 2), (2, 7, 0, 0), (2, 7, 0, 2),
        (2, 7, 1, 1), (3, 5, 0, 0), (3, 5, 0, 1),
        (3, 5, 1, 0), (3, 5, 1, 1), (3, 5, 2, 2),
        (3, 7, 0, 0), (3, 7, 0, 2), (3, 7, 1, 0),
        (3, 7, 1, 2), (4, 6, 0, 0), (4, 6, 0, 1),
        (5, 7, 2, 0), (5, 7, 2, 2), (6, 7, 0, 1),
        (6, 7, 1, 1),
    ),
    # Shared arm A_02=E_21 (off-diagonal head case).  Together with fixed
    # E_00 and E_21 this has 46 cells.
    2: (
        (0, 4, 2, 2), (0, 6, 1, 1), (1, 2, 1, 1),
        (1, 2, 1, 2), (1, 3, 2, 2), (1, 4, 1, 1),
        (1, 4, 2, 1), (1, 5, 2, 0), (1, 5, 2, 1),
        (1, 6, 1, 0), (1, 7, 2, 0), (1, 7, 2, 2),
        (2, 3, 0, 2), (2, 4, 1, 0), (2, 4, 2, 0),
        (2, 5, 0, 0), (2, 5, 0, 1), (2, 6, 0, 0),
        (2, 6, 1, 2), (2, 6, 2, 2), (2, 7, 0, 0),
        (2, 7, 0, 2), (2, 7, 1, 1), (2, 7, 2, 1),
        (3, 4, 0, 1), (3, 4, 1, 1), (3, 5, 0, 0),
        (3, 5, 0, 1), (3, 5, 1, 0), (3, 5, 1, 1),
        (3, 5, 2, 2), (3, 7, 0, 0), (3, 7, 0, 2),
        (3, 7, 1, 0), (3, 7, 1, 2), (3, 7, 2, 1),
        (4, 5, 1, 2), (4, 6, 0, 0), (4, 6, 1, 2),
        (5, 7, 0, 1), (5, 7, 1, 1), (5, 7, 2, 0),
        (5, 7, 2, 2), (6, 7, 0, 1),
    ),
}


CIRCUITS = {
    1: (
        ("residual", (0, 0, 0, 2, 0, 2, 0, 0)),
        ("full", (2, 2, 0, 2, 0, 0, 0, 0)),
        ("full", (2, 2, 2, 2, 1, 2, 2, 0)),
    ),
    2: (
        ("residual", (0, 0, 0, 0, 1, 0, 0, 1)),
        ("residual", (0, 0, 0, 2, 0, 0, 0, 1)),
        ("residual", (0, 0, 0, 2, 1, 2, 0, 1)),
    ),
}


EXPECTED_CIRCUIT_MONOMIALS = {
    1: (
        (
            ((2, 3, 0, 2), (4, 6, 0, 0), (5, 7, 2, 0)),
            ((2, 7, 0, 0), (3, 5, 2, 2), (4, 6, 0, 0)),
        ),
        (
            ((0, 5, 2, 0), (1, 3, 2, 2), (2, 7, 0, 0), (4, 6, 0, 0)),
            ((0, 5, 2, 0), (1, 7, 2, 0), (2, 3, 0, 2), (4, 6, 0, 0)),
        ),
        (
            ((0, 4, 2, 1), (1, 3, 2, 2), (2, 6, 2, 2), (5, 7, 2, 0)),
            ((0, 4, 2, 1), (1, 7, 2, 0), (2, 6, 2, 2), (3, 5, 2, 2)),
        ),
    ),
    2: (
        (
            ((2, 5, 0, 0), (3, 4, 0, 1), (6, 7, 0, 1)),
            ((2, 6, 0, 0), (3, 4, 0, 1), (5, 7, 0, 1)),
        ),
        (
            ((2, 3, 0, 2), (4, 6, 0, 0), (5, 7, 0, 1)),
            ((2, 5, 0, 0), (3, 7, 2, 1), (4, 6, 0, 0)),
        ),
        (
            ((2, 3, 0, 2), (4, 5, 1, 2), (6, 7, 0, 1)),
            ((2, 6, 0, 0), (3, 7, 2, 1), (4, 5, 1, 2)),
        ),
    ),
}


def fixed_cells(head):
    return frozenset(((P, Q, 0, 0), (P, R, head, 1)))


def monomials(word, matchings, support):
    answer = set()
    for matching in matchings:
        cells = tuple(sorted(
            (left, right, word[left], word[right])
            for left, right in matching
        ))
        if set(cells) <= support:
            answer.add(cells)
    return tuple(sorted(answer))


def is_residual_target(word):
    residual = word[2:]
    return len(set(residual)) == 1 and residual[0] == 0


def is_full_target(word):
    return len(set(word)) == 1


def support_shadow_violations(support):
    violations = []
    for residual_word in product(COLORS, repeat=6):
        word = (0, 0) + residual_word
        count = len(monomials(word, MATCHINGS6, support))
        target = is_residual_target(word)
        if (target and count == 0) or (not target and count == 1):
            violations.append(("residual", word, count, target))
    for word in product(COLORS, repeat=8):
        count = len(monomials(word, MATCHINGS8, support))
        target = is_full_target(word)
        if (target and count == 0) or (not target and count == 1):
            violations.append(("full", word, count, target))
    return tuple(violations)


def support_histogram(support):
    histogram = Counter()
    for residual_word in product(COLORS, repeat=6):
        word = (0, 0) + residual_word
        histogram[("residual", is_residual_target(word),
                   len(monomials(word, MATCHINGS6, support)))] += 1
    for word in product(COLORS, repeat=8):
        histogram[("full", is_full_target(word),
                   len(monomials(word, MATCHINGS8, support)))] += 1
    return histogram


def exponent(monomial):
    return Counter(monomial)


def subtract(left, right):
    answer = Counter(left)
    answer.subtract(right)
    return +answer, +(-answer)


def signed_vector(left, right):
    positive, negative = subtract(exponent(left), exponent(right))
    return positive, negative


def vector_add(first, second):
    positive = Counter(first[0]) + Counter(second[0])
    negative = Counter(first[1]) + Counter(second[1])
    common = positive & negative
    positive.subtract(common)
    negative.subtract(common)
    return +positive, +negative


def multiply_monomials(*monomials_):
    result = []
    for monomial in monomials_:
        result.extend(monomial)
    return tuple(sorted(result))


def polynomial_add(polynomial, monomial, coefficient):
    polynomial[monomial] += coefficient
    if not polynomial[monomial]:
        del polynomial[monomial]


def audit_circuit(head, support):
    equations = []
    for kind, word in CIRCUITS[head]:
        matchings = MATCHINGS6 if kind == "residual" else MATCHINGS8
        require(not (is_residual_target(word) if kind == "residual"
                     else is_full_target(word)),
                "a circuit word became a target word")
        found = monomials(word, matchings, support)
        require(len(found) == 2,
                f"head {head}: a circuit row stopped being binomial")
        equations.append(found)
    require(tuple(equations) == EXPECTED_CIRCUIT_MONOMIALS[head],
            f"head {head}: circuit monomials changed")

    (m10, m11), (m20, m21), (m30, m31) = equations
    require(vector_add(signed_vector(m10, m11),
                       signed_vector(m20, m21))
            == signed_vector(m30, m31),
            f"head {head}: odd exponent circuit changed")

    # Expand
    #   m20*m31*(m10+m11) - m11*m31*(m20+m21)
    #       + m11*m21*(m30+m31).
    # The middle terms cancel.  The exponent circuit identifies the two
    # remaining monomials, leaving 2*M.  Since every support cell is nonzero,
    # M is a Laurent unit and characteristic zero gives a contradiction.
    certificate = Counter()
    for monomial in (m10, m11):
        polynomial_add(certificate,
                       multiply_monomials(m20, m31, monomial), 1)
    for monomial in (m20, m21):
        polynomial_add(certificate,
                       multiply_monomials(m11, m31, monomial), -1)
    for monomial in (m30, m31):
        polynomial_add(certificate,
                       multiply_monomials(m11, m21, monomial), 1)
    unit_monomial = multiply_monomials(m10, m20, m31)
    require(certificate == Counter({unit_monomial: 2}),
            f"head {head}: Laurent unit certificate changed")
    return {
        "rows": [
            {"kind": kind, "word": "".join(map(str, word)),
             "monomials": [[list(cell) for cell in monomial]
                             for monomial in equation]}
            for (kind, word), equation in zip(CIRCUITS[head], equations,
                                               strict=True)
        ],
        "identity": (
            "m20*m31*E1-m11*m31*E2+m11*m21*E3=2*M; "
            "M is a support-torus unit"
        ),
        "characteristic": "zero (or not two)",
    }


def serial_histogram(histogram):
    return {
        f"{kind}:{'target' if target else 'zero'}:{count}": multiplicity
        for (kind, target, count), multiplicity
        in sorted(histogram.items())
    }


def audit_packet(head):
    fixed = fixed_cells(head)
    optional = frozenset(PACKETS[head])
    require(not fixed & optional and len(optional) == len(PACKETS[head]),
            f"head {head}: duplicate or overlapping support cells")
    support = fixed | optional

    require((P, Q, 0, 0) in support
            and all((P, Q, a, b) not in support
                    for a in COLORS for b in COLORS if (a, b) != (0, 0)),
            "the essential direct arm stopped being E00")
    require(not any(cell[0] == P and cell[2] == 0
                    for cell in support if cell[:2] != (P, Q)),
            "Lemma E1 lost its zero p_0 star")
    require({cell for cell in support if cell[:2] == (P, R)}
            == {(P, R, head, 1)},
            f"head {head}: the shared reciprocal arm stopped being E_head,1")

    violations = support_shadow_violations(support)
    require(not violations,
            f"head {head}: frozen support stopped satisfying the shadow")
    histogram = support_histogram(support)
    expected_histograms = {
        1: {
            "full:target:2": 3, "full:zero:0": 6337,
            "full:zero:2": 209, "full:zero:4": 12,
            "residual:target:2": 1, "residual:zero:0": 699,
            "residual:zero:2": 29,
        },
        2: {
            "full:target:2": 3, "full:zero:0": 6328,
            "full:zero:2": 218, "full:zero:4": 12,
            "residual:target:2": 1, "residual:zero:0": 668,
            "residual:zero:2": 60,
        },
    }
    require(serial_histogram(histogram) == expected_histograms[head],
            f"head {head}: support histogram changed")

    # Exact, solver-free deletion irredundancy: deleting each optional cell
    # from this fixed packet violates at least one necessary shadow row.
    deletion_witnesses = {}
    for cell in sorted(optional):
        found = support_shadow_violations(support - {cell})
        require(found, f"head {head}: optional cell is deletion-redundant: {cell}")
        kind, word, count, target = found[0]
        deletion_witnesses[str(cell)] = {
            "kind": kind, "word": "".join(map(str, word)),
            "count": count, "target": target,
        }

    return {
        "head": head,
        "fixed_cells": [list(cell) for cell in sorted(fixed)],
        "optional_cells": len(optional),
        "total_cells": len(support),
        "support_histogram": serial_histogram(histogram),
        "single_cell_deletion_witnesses": deletion_witnesses,
        "circuit": audit_circuit(head, support),
    }


def main():
    packets = [audit_packet(head) for head in (1, 2)]
    ledger = {
        "normalization": {
            "essential_arm": "A_01=E_00",
            "lemma_E1": "row_0(A_0x)=0 for x!=1",
            "lemma_E3": "H_{2,...,7}=e_0^tensor6",
            "shared_arm_cases": ["A_02=E_11", "A_02=E_21"],
        },
        "packets": packets,
        "verdict": {
            "support_shadow": "SAT in both head cases",
            "frozen_support_tori": "coefficient-empty by three-row odd circuits",
            "global_packet": "open outside the two frozen support packets",
        },
        "scope": (
            "literal site-square-zero residual unary-top plus all nine pair "
            "rows; frozen deletion-irredundant supports, not an exhaustive "
            "support-poset classification"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"Lemma-E shared packet ledger changed: {digest}")
    print("N=8 Lemma-E shared unary-top support packets: PASS")
    print("support shadow: SAT for head cases E11 and E21")
    print("frozen packets: 39 and 46 cells; every optional cell deletion-visible")
    print("coefficient tori: EMPTY by exact three-binomial odd circuits")
    print("global normalized packet: OPEN beyond the frozen supports")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
