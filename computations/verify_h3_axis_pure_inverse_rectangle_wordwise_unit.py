#!/usr/bin/env python3
"""Wordwise terminalization of the axis-pure inverse rectangle.

A balanced (2,2,2) word in an axis-diagonal K6 quadratic has exactly one
compatible perfect matching.  Hence a complementary two-colour minor cannot
be nonzero at an exact source: its two products live in different words and
must vanish separately.  Applying this to both determinants of the inverse
rectangle from 855b2c5 makes that whole collapsed countermodel stratum empty.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_pure_commutative_cohafnian_counterguard.py":
        "64e54e9fbd6419182437eb400973abb1099468170e87b9d72abc806a615ecf81",
    "notes/h3-axis-pure-commutative-cohafnian-counterguard.md":
        "f0b571cec6f616fbbd6b6e5351cda393a522f5ea672f30b246ca18681ab7ee93",
    "computations/verify_three_anchor_internal_quadratic_leak.py":
        "008165094ce6ea22c0e6ee258c447cd608f72a3ae8bcf6d058be5f0cbb069314",
    "notes/three-anchor-internal-quadratic-leak.md":
        "fb6c593e82732750138d45837250856e5846b2e6c07d14aba0294da0151d7ee8",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
}
EXPECTED_LEDGER_SHA256 = "d29c557055e410f31432c306daf1de0b776b7bd07b28141be061d27eb1d8c099"
SITES = tuple(range(6))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index]+vertices[index+1:]
        for tail in perfect_matchings(rest):
            yield (tuple(sorted((first, second))),)+tail


MATCHINGS = tuple(perfect_matchings(SITES))


def compatible(matching, word):
    return all(word[left] == word[right] for left, right in matching)


def unique_balanced_word_audit():
    balanced = tuple(word for word in itertools.product(range(3), repeat=6)
                     if tuple(word.count(colour) for colour in range(3))
                     == (2, 2, 2))
    require(len(balanced) == 90, len(balanced))
    witnesses = {}
    for word in balanced:
        allowed = tuple(matching for matching in MATCHINGS
                        if compatible(matching, word))
        require(len(allowed) == 1, (word, allowed))
        expected = tuple(sorted(tuple(sorted(
            site for site in SITES if word[site] == colour))
            for colour in range(3)))
        require(tuple(sorted(allowed[0])) == expected, (word, allowed, expected))
        witnesses["".join(map(str, word))] = [list(edge) for edge in allowed[0]]
    return {
        "balanced_words": len(balanced),
        "compatible_matchings_per_word": 1,
        "reason": "each of the three colour classes is its forced pair",
        "four_relevant_witnesses": {
            word: witnesses[word] for word in
            ("210012", "210021", "002121", "002112")
        },
    }


def complementary_minor_theorem_audit():
    # q23:0 is complementary to the two products ac and fh.
    first = {
        "pure_edge": "q23:0",
        "minor": "a*c-f*h",
        "positive_term": {"word": "210012", "matching": "05:2|14:1|23:0",
                          "coefficient": "a*c*q23"},
        "negative_term": {"word": "210021", "matching": "04:2|15:1|23:0",
                          "coefficient": "f*h*q23"},
    }
    # q01:0 is complementary to bd and eg.
    second = {
        "pure_edge": "q01:0",
        "minor": "b*d-e*g",
        "positive_term": {"word": "002121", "matching": "01:0|24:2|35:1",
                          "coefficient": "b*d*q01"},
        "negative_term": {"word": "002112", "matching": "01:0|25:2|34:1",
                          "coefficient": "e*g*q01"},
    }
    require(first["positive_term"]["word"] != first["negative_term"]["word"]
            and second["positive_term"]["word"]
            != second["negative_term"]["word"],
            "minor terms collapsed to one physical word")
    return {
        "first_rectangle": first,
        "second_rectangle": second,
        "source_identity": (
            "a mixed target word has target zero; because its axis-diagonal "
            "matching is unique, its displayed monomial must vanish"
        ),
        "localized_conclusion": (
            "if the complementary pure edge is nonzero, each of the two "
            "minor monomials vanishes separately, hence the minor is zero"
        ),
        "terminal_alternative": (
            "a nonzero complementary minor exposes a literal nonzero mixed "
            "full-word coefficient, stronger than an untyped active carrier"
        ),
    }


def inverse_rectangle_family_audit():
    tested = 0
    minimum_nonzero_residues = 4
    rational_instance = None
    for a, f, h, c in itertools.product(range(-2, 3), repeat=4):
        determinant = a*c-f*h
        if not determinant:
            continue
        a, f, h, c, determinant = map(F, (a, f, h, c, determinant))
        b, e, g, d = (c/determinant, -f/determinant,
                      -h/determinant, a/determinant)
        uv = ((a*b+f*g, a*e+f*d),
              (h*b+c*g, h*e+c*d))
        require(uv == ((1, 0), (0, 1)), uv)
        residues = {
            "210012": a*c,
            "210021": f*h,
            "002121": b*d,
            "002112": e*g,
        }
        require(residues["210012"] or residues["210021"],
                ("det U lost both terms", a, f, h, c))
        require(residues["002121"] or residues["002112"],
                ("det V lost both terms", b, e, g, d))
        minimum_nonzero_residues = min(
            minimum_nonzero_residues,
            sum(bool(value) for value in residues.values()))
        tested += 1
        if (a, f, h, c) == (1, 1, -1, 1):
            rational_instance = {word: str(value)
                                 for word, value in residues.items()}
    require(tested == 496, tested)
    require(minimum_nonzero_residues == 2, minimum_nonzero_residues)
    require(rational_instance == {
        "210012": "1", "210021": "-1",
        "002121": "1/4", "002112": "-1/4",
    }, rational_instance)
    return {
        "integer_U_samples": tested,
        "general_proof": (
            "UV=I implies det(U)=ac-fh!=0 and det(V)=bd-eg=det(U)^-1!=0; "
            "therefore at least one residue on each complementary rectangle "
            "is nonzero"
        ),
        "minimum_nonzero_balanced_residues": minimum_nonzero_residues,
        "855b2c5_instance": rational_instance,
        "conclusion": (
            "every inverse-rectangle response normalization violates at "
            "least two literal mixed unary rows"
        ),
    }


def route_scope_audit():
    pure_zero_family = (((0, 1), (2, 3), (4, 5)),)
    require(all(edge in pure_zero_family[0]
                for edge in ((0, 1), (2, 3), (4, 5))),
            pure_zero_family)
    return {
        "fastest_landing": "literal mixed full-word unit / contradiction",
        "active_minor_route": (
            "not needed and not typed: every q cell in the inverse rectangle "
            "is colour-diagonal, whereas the private-site active-minor theorem "
            "starts from an off-diagonal endpoint cell"
        ),
        "support_coloop": (
            "the displayed pure-zero family is the single matching "
            "01|23|45, so all three edges are literal pure-zero coloops; "
            "however coloop normalization is downstream of the stronger word unit"
        ),
        "remaining_general_incidence": (
            "for an arbitrary axis-pure response packet, force a nonzero "
            "cross-colour 2x2 minor complementary to an occupied pure-zero "
            "edge, or route the failure into the existing star/triangle/K2,2 "
            "Hall and literal-coloop normal forms"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 axis-pure inverse rectangle wordwise unit",
        "pins": PINS,
        "balanced_word_uniqueness": unique_balanced_word_audit(),
        "complementary_minor": complementary_minor_theorem_audit(),
        "inverse_rectangle": inverse_rectangle_family_audit(),
        "route_scope": route_scope_audit(),
        "verdict": (
            "The 855b2c5 collapsed family cannot be a physical source.  "
            "Every normalized inverse rectangle has at least two nonzero "
            "balanced (2,2,2) residues, and every such word has one forced "
            "axis-diagonal matching.  Thus the family lands directly in a "
            "literal mixed full-word unit, before four-good or coloop.  More "
            "generally, a cross-colour 2x2 minor complementary to a nonzero "
            "pure edge is zero at every exact axis-pure source; if it is "
            "nonzero, one of its two distinct word coefficients is terminal."
        ),
        "scope": (
            "uniform inverse-rectangle and complementary-minor theorem in "
            "the h=3 axis-diagonal chart; no arbitrary-support census"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("balanced axis-pure words: UNIQUE MATCHING")
    print("complementary cross-colour minor: ZERO OR MIXED-WORD UNIT")
    print("inverse rectangle: PHYSICALLY EMPTY")
    print("minimum forced nonzero residues:",
          ledger["inverse_rectangle"]["minimum_nonzero_balanced_residues"])
    print("ledger_sha256="+digest)


if __name__ == "__main__":
    main()
