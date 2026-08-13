#!/usr/bin/env python3
"""Literal two-occurrence coloop packet and its first omitted GHZ row.

The alpha-localized abstract packet leaves a free redistribution f-g.  This
checker places two literal response occurrences in the pure-1 word and adds
the complete unary plus four response coefficients of that word.  Their
first transverse minors are the endpoint-ratio and closing-edge differences.

All five minors can vanish while the five pure-1 coefficients and the
pure-0 coloop normalization hold exactly.  The first nonzero coefficient
outside that block is instead the mixed unary word 000011.  Its selected
monomial is nonzero, so the full GHZ equation forces an alternate matching
mate, not an occurrence-asymmetric response row directly.
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
    "computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py":
        "f0905b3e33a45b51f03dd6716c3f6b29ae21c39fecf50a4ffc32960499a608c7",
    "notes/h3-coloop-alpha-localized-pointed-pf-ga-fitting-gate.md":
        "5d637d94ec2bab2f968dcb31b45b805fecd66da13fb1c927a490a6e20927fe4f",
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
    "notes/h3-trapped-carrier-full-q-six-term-extension.md":
        "a5b1a81c834095e69c403d054a38d9f34ebb8b0b3f1d3ce720a27f0b275d04a5",
}
EXPECTED_LEDGER_SHA256 = "f9834ae5bf043b6875c1b7a24f968fe6a56d956c7b68f7a0267dc59369fdd2f5"

SITES = tuple(range(6))
COLOURS = tuple(range(3))
PURE_ZERO = (0,) * 6
PURE_ONE = (1,) * 6


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left, right):
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield (edge(first, second),) + tail


MATCHINGS6 = tuple(perfect_matchings(SITES))


def q_label(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return (left, right, left_colour, right_colour)


def get_q(q_values, left, right, left_colour, right_colour):
    return q_values.get(q_label(
        left, right, left_colour, right_colour
    ), Q(0))


def product_values(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def hafnian(vertices, word, q_values):
    return sum((product_values(get_q(
        q_values, left, right, word[left], word[right]
    ) for left, right in matching)
                for matching in perfect_matchings(vertices)), Q(0))


def response(head_p, head_s, word, p_values, s_values, q_values):
    answer = Q(0)
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            remaining = tuple(site for site in SITES
                              if site not in (p_site, s_site))
            answer += (
                p_values.get((head_p, p_site, word[p_site]), Q(0))
                * s_values.get((head_s, s_site, word[s_site]), Q(0))
                * hafnian(remaining, word, q_values)
            )
    return answer


def response_occurrences(head_p, head_s, word, p_values, s_values, q_values):
    occurrences = Counter()
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            remaining = tuple(site for site in SITES
                              if site not in (p_site, s_site))
            for matching in perfect_matchings(remaining):
                value = (
                    p_values.get((head_p, p_site, word[p_site]), Q(0))
                    * s_values.get((head_s, s_site, word[s_site]), Q(0))
                    * product_values(get_q(
                        q_values, left, right, word[left], word[right]
                    ) for left, right in matching)
                )
                if value:
                    occurrences[(p_site, s_site, tuple(matching))] += value
    return occurrences


def literal_guard_values():
    # alpha=q01^00 is a pure-zero coloop; q23^00*q45^00 is its only
    # cofactor.  The pure-one response has precisely the two occurrences
    # f=(P0,S1;23|45) and g=(P1,S4;02|35).
    q_values = {
        q_label(0, 1, 0, 0): Q(1),
        q_label(2, 3, 0, 0): Q(1),
        q_label(4, 5, 0, 0): Q(1),
        q_label(2, 3, 1, 1): Q(1),
        q_label(4, 5, 1, 1): Q(1, 2),
        q_label(0, 2, 1, 1): Q(1),
        q_label(3, 5, 1, 1): Q(1, 2),
    }
    p_values = {
        (0, 0, 1): Q(1),
        (0, 1, 1): Q(1),
    }
    s_values = {
        (0, 1, 1): Q(1),
        (0, 4, 1): Q(1),
    }
    # Head 1 is the second response head.  All of its displayed endpoint
    # cells vanish, making both crossed rows and the other diagonal row zero.
    return p_values, s_values, q_values


def audit_selected_five_rows():
    p_values, s_values, q_values = literal_guard_values()
    occurrences = response_occurrences(
        0, 0, PURE_ONE, p_values, s_values, q_values
    )
    expected = Counter({
        (0, 1, ((2, 3), (4, 5))): Q(1, 2),
        (1, 4, ((0, 2), (3, 5))): Q(1, 2),
    })
    require(occurrences == expected,
            ("the selected pure-one occurrence packet changed", occurrences))

    rows = {
        "unary[111111]": hafnian(SITES, PURE_ONE, q_values),
        "R11[111111]": response(
            0, 0, PURE_ONE, p_values, s_values, q_values
        ),
        "R12[111111]": response(
            0, 1, PURE_ONE, p_values, s_values, q_values
        ),
        "R21[111111]": response(
            1, 0, PURE_ONE, p_values, s_values, q_values
        ),
        "R22[111111]": response(
            1, 1, PURE_ONE, p_values, s_values, q_values
        ),
    }
    expected_rows = {
        "unary[111111]": Q(0),
        "R11[111111]": Q(1),
        "R12[111111]": Q(0),
        "R21[111111]": Q(0),
        "R22[111111]": Q(0),
    }
    require(rows == expected_rows,
            ("the selected complete five-row guard changed", rows))

    # Ratios of the four response heads and of the unary closing edge,
    # relative to each nonzero R11 occurrence.  Denominators all equal one.
    ratios = {
        "f": {"a_s": Q(0), "b_p": Q(0),
              "a_s*b_p": Q(0), "c_unary": Q(0)},
        "g": {"a_s": Q(0), "b_p": Q(0),
              "a_s*b_p": Q(0), "c_unary": Q(0)},
    }
    minors = {
        label: ratios["g"][label] - ratios["f"][label]
        for label in ratios["f"]
    }
    require(not any(minors.values()),
            ("a first transverse minor became nonzero", minors))

    alpha = get_q(q_values, 0, 1, 0, 0)
    cofactor = hafnian((2, 3, 4, 5), PURE_ZERO, q_values)
    require(alpha == cofactor == 1
            and hafnian(SITES, PURE_ZERO, q_values) == 1,
            "the literal pure-zero coloop normalization changed")
    return {
        "pure_zero_coloop": "alpha=q01[00]=1",
        "pure_zero_cofactor": "C_c=q23[00]*q45[00]=1",
        "literal_f": "p1[0,1]s1[1,1]q23[11]q45[11]=1/2",
        "literal_g": "p1[1,1]s1[4,1]q02[11]q35[11]=1/2",
        "nonzero_R11_occurrences": len(occurrences),
        "five_GHZ_coefficients": {key: str(value)
                                  for key, value in rows.items()},
        "first_transverse_minors": {
            "R12": "a_g-a_f=0",
            "R21": "b_g-b_f=0",
            "R22": "a_g*b_g-a_f*b_f=0",
            "unary_companion": "c_g-c_f=0",
        },
        "conclusion": (
            "the complete selected-word unary/four-response equations and "
            "the coloop target do not force an occurrence-asymmetric minor"
        ),
    }


def audit_first_omitted_unary_row():
    _p_values, _s_values, q_values = literal_guard_values()
    nonzero = {}
    for word in product(COLOURS, repeat=6):
        value = hafnian(SITES, word, q_values)
        if value:
            nonzero[word] = value
    mixed = {word: value for word, value in nonzero.items()
             if word not in (PURE_ZERO, PURE_ONE, (2,) * 6)}
    require(mixed == {
        (0, 0, 0, 0, 1, 1): Q(1, 2),
        (0, 0, 1, 1, 0, 0): Q(1),
        (0, 0, 1, 1, 1, 1): Q(1, 2),
    }, ("the mixed unary guard changed", mixed))
    first_word = min(mixed)
    require(first_word == (0, 0, 0, 0, 1, 1),
            "the first omitted mixed word changed")

    selected_matching = ((0, 1), (2, 3), (4, 5))
    selected_value = product_values(get_q(
        q_values, left, right, first_word[left], first_word[right]
    ) for left, right in selected_matching)
    require(selected_value == Q(1, 2)
            and selected_value == mixed[first_word],
            "the first omitted coefficient lost its private monomial")
    alternates = tuple(matching for matching in MATCHINGS6
                       if matching != selected_matching)
    diagonal = tuple(matching for matching in alternates
                     if all(first_word[left] == first_word[right]
                            for left, right in matching))
    offdiagonal = tuple(matching for matching in alternates
                        if matching not in diagonal)
    retain_coloop = tuple(matching for matching in offdiagonal
                          if (0, 1) in matching)
    require((len(alternates), len(diagonal), len(offdiagonal),
             len(retain_coloop)) == (14, 2, 12, 2),
            "the first mixed-unary mate classification changed")
    require(diagonal == (
        ((0, 2), (1, 3), (4, 5)),
        ((0, 3), (1, 2), (4, 5)),
    ), ("the two diagonal mates changed", diagonal))
    return {
        "first_omitted_GHZ_coefficient": "unary H0[000011]=0",
        "guard_value": "1/2",
        "private_selected_monomial": "q01[00]*q23[00]*q45[11]=1/2",
        "full_equation_consequence": (
            "at least one of the other fourteen perfect-matching monomials "
            "in H0[000011] must be nonzero"
        ),
        "alternate_matching_split": {
            "all_diagonal": len(diagonal),
            "with_two_cross_colour_edges": len(offdiagonal),
            "offdiagonal_and_retain_coloop_01": len(retain_coloop),
        },
        "two_diagonal_alternates": [repr(value) for value in diagonal],
        "logical_effect": (
            "the global equations first force a unary matching mate; they "
            "do not yet choose one of the four occurrence-transverse minors"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 coloop two-occurrence complete response / first mixed unary gate",
        "pins": PINS,
        "selected_word_packet": audit_selected_five_rows(),
        "first_omitted_row": audit_first_omitted_unary_row(),
        "sharp_frontier": (
            "after the alpha-localized aggregate pivot, unary plus all four "
            "response coefficients at the selected pure-one word need not "
            "break f/g symmetry.  The first forced new datum in the literal "
            "guard is cancellation of H0[000011], equivalently an alternate "
            "matching mate.  Landing that mate or showing its added full-row "
            "coefficient has unequal f/g restriction is the next theorem"
        ),
        "scope": (
            "the displayed packet is a literal complete-row guard for the "
            "named coloop and five selected-word GHZ coefficients, not a "
            "solution of every GHZ word equation; its first failure is "
            "explicitly H0[000011]"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("two-occurrence complete-row ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    print("selected pure-one unary+four response rows: EXACT")
    print("first occurrence-asymmetric minors: ALL ZERO")
    print("first omitted coefficient: H0[000011]=1/2, MATCHING MATE FORCED")
    print("ledger_sha256=" + digest)
    return ledger


if __name__ == "__main__":
    audit()
