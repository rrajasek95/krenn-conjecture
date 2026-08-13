#!/usr/bin/env python3
"""The marked trapped-carrier polar is not supplied by Euler/Hasse alone.

The selected response coefficient is the mixed word 110000 in head 11.
It is a sum of 90 literal endpoint/matching occurrences.  Every occurrence
has the same site/colour character, so every target-compatible diagonal
Euler field acts on the *aggregate* response row by one scalar.  In
contrast, the product of the three movable coefficient Euler operators for

    p1[0,1] s1[1,1] q23[0,0] q45[0,0]

selects precisely that occurrence.  At an actual trapped source the mixed
response coefficient is zero while the selected occurrence is nonzero.
Thus this projector does not preserve the source equation and its
differential is not an old Jacobian row.  The same calculation shows that
homogeneity, target normalization, and a six-term row already in row(A)
cannot remove the surviving anchor conormal.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
    "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py":
        "ba2c32a41b1d070d2af24546819e838697aba0273e85586a796ee25a27f5a950",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
}
EXPECTED_LEDGER_SHA256 = (
    "7394dc51c712cc04191433944d87d72afd8833bc75701644a22c026bf0729feb"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
WORD = (1, 1, 0, 0, 0, 0)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def p_variable(site: int):
    return ("p", 0, site, WORD[site])


def s_variable(site: int):
    return ("s", 0, site, WORD[site])


def q_variable(left: int, right: int):
    if left > right:
        left, right = right, left
    return ("q", left, right, WORD[left], WORD[right])


def response_occurrences():
    occurrences = []
    for left_site in SITES:
        for right_site in SITES:
            if left_site == right_site:
                continue
            complement = tuple(site for site in SITES
                               if site not in (left_site, right_site))
            for matching in perfect_matchings(complement):
                occurrences.append(tuple(sorted((
                    p_variable(left_site),
                    s_variable(right_site),
                    *(q_variable(left, right) for left, right in matching),
                ))))
    require(len(occurrences) == 90 and len(set(occurrences)) == 90,
            "the literal mixed response occurrence count changed")
    return tuple(occurrences)


def selected_occurrence():
    return tuple(sorted((
        p_variable(0), s_variable(1), q_variable(2, 3), q_variable(4, 5)
    )))


def site_colour_incidence(monomial):
    incidence = Counter()
    for variable in monomial:
        if variable[0] in {"p", "s"}:
            _kind, _head, site, colour = variable
            incidence[site, colour] += 1
        else:
            _kind, left, right, a, b = variable
            incidence[left, a] += 1
            incidence[right, b] += 1
    return tuple(incidence[site, colour]
                 for site in SITES for colour in COLOURS)


def movable_part(monomial):
    # dac1248 fixes s and varies p plus every q coordinate.
    return tuple(variable for variable in monomial if variable[0] != "s")


def logarithmic_projector(occurrences, selected_variables):
    selected_variables = frozenset(selected_variables)
    return tuple(index for index, monomial in enumerate(occurrences)
                 if selected_variables.issubset(monomial))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def audit():
    actual_pins = {}
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
        actual_pins[relative] = actual

    occurrences = response_occurrences()
    marked = selected_occurrence()
    marked_index = occurrences.index(marked)

    # Every response monomial covers every output site exactly once and has
    # the selected word's colour there.  Hence a physical diagonal target
    # stabilizer has one common character on all 90 terms.
    expected_incidence = tuple(int(colour == WORD[site])
                               for site in SITES for colour in COLOURS)
    incidences = tuple(site_colour_incidence(term) for term in occurrences)
    require(set(incidences) == {expected_incidence},
            "the response row stopped being one site/colour weight space")

    stabilizer_records = []
    for weights_flat in (
        # Three representative GHZ-stabilizer weights.  Each colour sum is
        # zero; the mixed character may be zero or nonzero.
        (1, 0, 0, -1, 0, 0) + (0,) * 12,
        (1, 0, 0, 0, 0, 0, -1, 0, 0) + (0,) * 9,
        (0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0),
    ):
        require(len(weights_flat) == 18, "bad stabilizer weight width")
        require(all(sum(weights_flat[3 * site + colour]
                        for site in SITES) == 0
                    for colour in COLOURS),
                "a test field moved a pure GHZ target")
        characters = tuple(dot(weights_flat, incidence)
                           for incidence in incidences)
        require(len(set(characters)) == 1,
                "a physical diagonal field split occurrences")
        stabilizer_records.append(str(characters[0]))

    # Since s is fixed, the three movable factors of f suffice.  Their
    # logarithmic coefficient projector has support exactly one.  With only
    # the two q factors, both endpoint orientations survive.
    marked_movable = movable_part(marked)
    require(len(marked_movable) == 3,
            "the full-pq marked differential changed arity")
    pq_projection = logarithmic_projector(occurrences, marked_movable)
    q_projection = logarithmic_projector(
        occurrences, tuple(variable for variable in marked
                           if variable[0] == "q")
    )
    require(pq_projection == (marked_index,),
            "the movable raw Euler projector stopped isolating f")
    require(len(q_projection) == 2,
            "the q-only projector stopped retaining two endpoint orientations")

    # Formal evaluation at an actual trapped source: R_11,110000=0 because
    # the GHZ response target X1 has no mixed word, while the marked anchor
    # occurrence is active.  Normalizing f(x)=1 loses no information.
    f_value = Q(1)
    mate_values = [Q(0)] * len(occurrences)
    mate_values[marked_index] = f_value
    cancellation_index = next(index for index in range(len(occurrences))
                              if index != marked_index)
    mate_values[cancellation_index] = -f_value
    aggregate_value = sum(mate_values, Q(0))
    projected_value = sum(mate_values[index] for index in pq_projection)
    require(aggregate_value == 0 and projected_value == f_value,
            "the active mixed-row projector counterguard changed")

    # On the dac1248 p,q domain every term has degree 3, whereas f has the
    # same degree by itself.  Homogeneity only returns 3R, which vanishes at
    # the mixed target; the occurrence projector returns 3f or f depending
    # on normalization and is nonzero.
    movable_degrees = tuple(len(movable_part(term)) for term in occurrences)
    require(set(movable_degrees) == {3},
            "fixed-s response homogeneity changed")
    aggregate_euler_value = sum(degree * value for degree, value
                                in zip(movable_degrees, mate_values,
                                       strict=True))
    marked_euler_value = len(marked_movable) * f_value
    require(aggregate_euler_value == 0 and marked_euler_value == 3,
            "Euler aggregate/occurrence separation changed")

    # The two-occurrence physical quotient is R=f+g at (f,g)=(1,-1).
    # Its tangent (1,-1) preserves the response and changes the marked
    # occurrence.  Taking Lambda=dR realizes the dac1248 sole survivor after
    # forgetting all other rows.  This is a literal response-row quotient,
    # not a claim that a full trapped source with all other rows exists.
    d_response = (Q(1), Q(1))
    d_marked = (Q(1), Q(0))
    tangent = (Q(1), Q(-1))
    lambda_row = d_response
    require(dot(d_response, tangent) == 0,
            "the literal cancellation tangent moved the mixed response")
    require(dot(d_marked, tangent) == 1,
            "the literal cancellation tangent lost marked visibility")
    require(lambda_row == d_response,
            "the six-term-in-old-row guard changed")

    return {
        "theorem": "trapped-carrier occurrence Euler/source-validity gate",
        "pins": actual_pins,
        "actual_response": {
            "head_word": "11:110000",
            "target_coefficient": 0,
            "literal_occurrences": len(occurrences),
            "marked_occurrence": (
                "p1[0,1]s1[1,1]q23[0,0]q45[0,0]"
            ),
            "marked_index": marked_index,
            "movable_degree_with_s_fixed": 3,
        },
        "physical_euler": {
            "site_colour_incidence_profiles": len(set(incidences)),
            "representative_mixed_characters": stabilizer_records,
            "conclusion": (
                "every target-compatible diagonal Euler/Hasse operator "
                "acts on the aggregate response coefficient; none selects "
                "the marked occurrence"
            ),
        },
        "raw_occurrence_projector": {
            "movable_selected_factors": [repr(value)
                                           for value in marked_movable],
            "support": len(pq_projection),
            "q_only_support": len(q_projection),
            "actual_source_value_of_response": str(aggregate_value),
            "actual_source_value_after_projection": str(projected_value),
            "first_source_validity_defect": "f(x), normalized here to 1",
        },
        "homogeneity": {
            "E_pq(response)(x)": str(aggregate_euler_value),
            "E_pq(f)(x)": str(marked_euler_value),
            "conclusion": "Euler returns 3R, not the marked polar df",
        },
        "literal_two_occurrence_quotient_guard": {
            "equation": "R=f+g=0",
            "point": ["1", "-1"],
            "tangent": ["1", "-1"],
            "dR_on_tangent": "0",
            "df_on_tangent": "1",
            "Lambda": "dR (hence Lambda is already in row(A))",
            "scope": (
                "a quotient of the literal 90-term response row showing "
                "that response homogeneity, active support, and target "
                "normalization do not themselves exclude the survivor; "
                "not a full unary-plus-four-response source point"
            ),
        },
        "minimal_remaining_datum": (
            "either infinitesimal occurrence rigidity df(T_x S)=0 on the "
            "actual fixed-right source fibre, or an occurrence-labelled "
            "relative/Spencer cell with scalar zero-face -f(x) (equivalently "
            "a target coordinate u_f with f-u_f=0).  A target-zero raw "
            "coefficient projector is impossible because its first defect "
            "is the active scalar f(x)"
        ),
        "lambda_consequence": (
            "under the sole survivor hypothesis Lambda in row(A), adding "
            "Lambda to a proposed correction cannot change the conormal "
            "class [H]; the occurrence-normalization datum remains separate"
        ),
        "formal_arc_gate": {
            "tangent": "xi in ker(A) with H(xi)!=0",
            "order_two_equation": "A*xi_2 = -D2F(xi,xi)",
            "obstruction_space": "coker(A) in the physical output-row space",
            "six_term_space": "row(A) subset of the source cotangent space",
            "typing_verdict": (
                "Lambda in row(A) implies Lambda(xi)=0; it does not imply "
                "D2F(xi,xi) is in image(A).  A source-valid comparison from "
                "the output obstruction complex to the six-term relative "
                "complex is required before Lambda can control prolongation"
            ),
            "first_missing_comparison": (
                "a chain map kappa_2:coker(A)->Q[Lambda] carrying every "
                "quadratic obstruction, followed by coherent higher maps; "
                "without it the formal-arc route is untyped"
            ),
        },
        "scope": (
            "conditional at any actual unary-compatible trapped source "
            "carrying the displayed nonzero marked occurrence.  It excludes "
            "Euler/homogeneity and uncorrected coefficient-Hasse shortcuts; "
            "it does not prove that the full source has the two-occurrence "
            "tangent or that H is independent of row(A)"
        ),
    }


def main() -> None:
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("occurrence Euler/source ledger changed", digest))
    print("h3 trapped-carrier occurrence Euler/source gate: PASS")
    print("mixed response 11:110000: 90 occurrences, one common character")
    print("raw pqq Euler projector: selected support 1, source defect f(x)!=0")
    print("homogeneity gives 3R, not df; Lambda in row(A) cannot repair [H]")
    print("minimal datum: infinitesimal occurrence rigidity or target-corrected cell")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
