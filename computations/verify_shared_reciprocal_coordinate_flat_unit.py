#!/usr/bin/env python3
"""Close the three coordinate-flat budget-13 signatures coefficientwise.

The preceding projective checker leaves three flat signatures.  This checker
reconstructs the complete 6,561-row maximal-envelope coefficient system for
each signature and for every shared-head colour.  More importantly, it checks
an ordinary three-row unit certificate which is stable under deleting any
envelope cells.

If q and r are the outer endpoints of two flat rank-one arms sharing p, all
non-chord rows at q lie on one target line e_a and all non-chord rows at r
lie on a distinct target line e_c.  Hence every equal-colour (q=i,r=i)
slice must use the chord qr.  Writing D_ii for its diagonal coefficient and
F_i for the pure-i coefficient of the residual hafnian gives

    G_i       = D_ii F_i - 1,
    G_{i|j}   = D_ii F_j,
    G_j       = D_jj F_j - 1.

For i != j these original source generators satisfy, over Z,

    1 = F_i (D_jj G_{i|j} - D_ii G_j) - G_i.

Thus every coordinate-flat signature, and every support below its maximal
envelope, is empty over every field.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import verify_shared_reciprocal_budget13_overlap_frontier as overlap
import verify_shared_reciprocal_budget13_projective_compatibility as projective


ROOT = Path(__file__).resolve().parents[1]
COLORS = (0, 1, 2)
SITES = tuple(range(8))
P, Q, R = 0, 1, 2
COMMON = tuple(range(3, 8))
RESIDUAL = (P,) + COMMON
PINNED_PROJECTIVE_SHA256 = (
    "ba90af66ea140af93af5ec3e2fc04cbeaffc6c7c2cdc1226fa132e2afdc1ff14"
)
EXPECTED_LEDGER_SHA256 = (
    "63d01c3b76ca9bfcc7018f705347dfad917d042d202858ef494f8a50a550c1b7"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_budget13_projective_compatibility.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_PROJECTIVE_SHA256,
            "the projective compatibility dependency changed")


def add_term(polynomial, monomial, coefficient=1):
    monomial = tuple(sorted(monomial))
    polynomial[monomial] += coefficient
    if polynomial[monomial] == 0:
        del polynomial[monomial]


def add_polynomials(*polynomials):
    answer = Counter()
    for polynomial, scale in polynomials:
        for monomial, coefficient in polynomial.items():
            add_term(answer, monomial, scale * coefficient)
    return answer


def multiply(first, second):
    answer = Counter()
    for left, left_coefficient in first.items():
        for right, right_coefficient in second.items():
            add_term(answer, left + right,
                     left_coefficient * right_coefficient)
    return answer


def monomial_polynomial(*variables):
    return Counter({tuple(sorted(variables)): 1})


def maximal_support(state, head):
    support = frozenset(
        (left, right, left_color, right_color)
        for left in SITES
        for right in SITES
        if left < right
        for left_color in COLORS
        for right_color in COLORS
        if overlap.allowed_cell(
            state, head, left, right, left_color, right_color
        )
    )
    return support


def cell_monomial(cell, head):
    """Substitute the exact flat-star parametrization.

    Normalize the common p factor to e_b.  If the two direct coefficients
    are L,M, flatness writes the q-C and r-C stars as L*z and M*z.
    Every other maximal-envelope coefficient remains independent.
    """

    left, right, left_color, right_color = cell
    a, c, b, d = head
    require(b == d and a != c, "the head is not proportional-flat")
    if (left, right) == (P, Q):
        require((left_color, right_color) == (b, a),
                "the pq cell left its literal head")
        return ("L",)
    if (left, right) == (P, R):
        require((left_color, right_color) == (b, c),
                "the pr cell left its literal head")
        return ("M",)
    if left == Q and right in COMMON:
        require(left_color == a, "a q-C cell left the outgoing line")
        return ("L", f"z{right}_{right_color}")
    if left == R and right in COMMON:
        require(left_color == c, "an r-C cell left the outgoing line")
        return ("M", f"z{right}_{right_color}")
    return (f"x{left}{right}_{left_color}{right_color}",)


def generator(word, support, head):
    polynomial = Counter()
    for matching in overlap.MATCHINGS:
        cells = tuple(
            (left, right, word[left], word[right])
            for left, right in matching
        )
        if not set(cells) <= support:
            continue
        monomial = ()
        for cell in cells:
            monomial += cell_monomial(cell, head)
        add_term(polynomial, monomial)
    if len(set(word)) == 1:
        add_term(polynomial, (), -1)
    return polynomial


def residual_hafnian(color, support, head):
    polynomial = Counter()
    for matching in overlap.perfect_matchings(RESIDUAL):
        cells = tuple((left, right, color, color)
                      for left, right in matching)
        if not set(cells) <= support:
            continue
        monomial = ()
        for cell in cells:
            monomial += cell_monomial(cell, head)
        add_term(polynomial, monomial)
    return polynomial


def serial_polynomial(polynomial):
    return tuple(
        (monomial, coefficient)
        for monomial, coefficient in sorted(polynomial.items())
    )


def complete_system(state, head):
    support = maximal_support(state, head)
    rows = []
    histogram = Counter()
    variable_names = set()
    for word in product(COLORS, repeat=8):
        polynomial = generator(word, support, head)
        rows.append((word, serial_polynomial(polynomial)))
        histogram[len(polynomial)] += 1
        for monomial in polynomial:
            variable_names.update(monomial)
    payload = json.dumps(rows, separators=(",", ":"))
    return {
        "support": support,
        "rows": rows,
        "row_sha256": sha256(payload.encode()).hexdigest(),
        "term_histogram": dict(sorted(histogram.items())),
        "variables": tuple(sorted(variable_names)),
    }


def unit_certificate(state, head, first_color, second_color):
    support = maximal_support(state, head)
    first_residual = residual_hafnian(first_color, support, head)
    second_residual = residual_hafnian(second_color, support, head)
    require(first_residual and second_residual,
            "a maximal envelope lost a pure residual coefficient")

    first_word = (first_color,) * 8
    second_word = (second_color,) * 8
    mixed_word = tuple(
        first_color if site in (Q, R) else second_color
        for site in SITES
    )
    first_generator = generator(first_word, support, head)
    second_generator = generator(second_word, support, head)
    mixed_generator = generator(mixed_word, support, head)
    first_diagonal = monomial_polynomial(
        f"x{Q}{R}_{first_color}{first_color}"
    )
    second_diagonal = monomial_polynomial(
        f"x{Q}{R}_{second_color}{second_color}"
    )

    expected_first = add_polynomials(
        (multiply(first_diagonal, first_residual), 1),
        (monomial_polynomial(), -1),
    )
    expected_second = add_polynomials(
        (multiply(second_diagonal, second_residual), 1),
        (monomial_polynomial(), -1),
    )
    expected_mixed = multiply(first_diagonal, second_residual)
    require(first_generator == expected_first,
            "the first pure slice did not factor through the chord")
    require(second_generator == expected_second,
            "the second pure slice did not factor through the chord")
    require(mixed_generator == expected_mixed,
            "the mixed slice did not reuse the residual pure coefficient")

    inner = add_polynomials(
        (multiply(second_diagonal, mixed_generator), 1),
        (multiply(first_diagonal, second_generator), -1),
    )
    certificate = add_polynomials(
        (multiply(first_residual, inner), 1),
        (first_generator, -1),
    )
    require(certificate == monomial_polynomial(),
            f"the ordinary unit certificate failed: {certificate}")
    return {
        "first_word": first_word,
        "mixed_word": mixed_word,
        "second_word": second_word,
        "first_residual_terms": len(first_residual),
        "second_residual_terms": len(second_residual),
        "source_sha256": sha256(json.dumps(
            (
                serial_polynomial(first_generator),
                serial_polynomial(mixed_generator),
                serial_polynomial(second_generator),
            ),
            separators=(",", ":"),
        ).encode()).hexdigest(),
    }


def main():
    pin_dependency()
    signatures = projective.EXPECTED_FLAT_STATES
    require(len(signatures) == 3,
            "the projective checker stopped leaving three flat signatures")

    systems = []
    certificates = []
    for signature_index, state in enumerate(signatures):
        # The canonical exceptions are e2 at r and e1 at q.  Hence the
        # outgoing colours are a=1,c=2.  The common p colour b=d is arbitrary.
        for shared_color in COLORS:
            head = (1, 2, shared_color, shared_color)
            system = complete_system(state, head)
            systems.append({
                "signature": signature_index,
                "shared_color": shared_color,
                "localized_envelope_cells": len(system["support"]),
                "flat_variables": len(system["variables"]),
                "term_histogram": system["term_histogram"],
                "row_sha256": system["row_sha256"],
            })
            for first_color in COLORS:
                for second_color in COLORS:
                    if first_color == second_color:
                        continue
                    certificates.append({
                        "signature": signature_index,
                        "shared_color": shared_color,
                        "colors": (first_color, second_color),
                        **unit_certificate(
                            state, head, first_color, second_color
                        ),
                    })

    require(len(systems) == 9 and len(certificates) == 54,
            "the flat system/certificate census changed")
    expected_support_counts = [136] * 6 + [137] * 3
    require([row["localized_envelope_cells"] for row in systems]
            == expected_support_counts,
            "the three maximal envelopes changed")
    expected_histograms = [
        {0: 1458, 3: 3237, 4: 3, 9: 405, 15: 1296, 45: 108, 60: 54}
    ] * 6 + [
        {0: 1701, 3: 2589, 4: 3, 9: 324, 15: 1728, 45: 144, 60: 72}
    ] * 3
    require([row["term_histogram"] for row in systems]
            == expected_histograms,
            "the complete 6,561-row term histograms changed")

    ledger = {
        "pinned_projective_sha256": PINNED_PROJECTIVE_SHA256,
        "coordinate_flat_signatures": 3,
        "head_refinements": 9,
        "complete_rows_per_refinement": 6561,
        "systems": systems,
        "ordered_color_certificates": len(certificates),
        "certificate_source_hashes": sorted(
            {row["source_sha256"] for row in certificates}
        ),
        "ordinary_certificate": (
            "1=F_i*(D_jj*G_i_given_j-D_ii*G_j)-G_i"
        ),
        "deletion_stable": True,
        "coefficient_survivors": 0,
        "field_scope": "every_commutative_ring",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            f"the coordinate-flat unit ledger changed: {digest}")
    print("shared reciprocal coordinate-flat unit: PASS")
    print("complete coefficient systems:", len(systems), "x 6561 rows")
    print("maximal envelope cells:", expected_support_counts)
    print("ordinary three-row unit certificates:", len(certificates))
    print("coefficient survivors: 0")
    print("ledger_sha256=", digest, sep="")


if __name__ == "__main__":
    main()
