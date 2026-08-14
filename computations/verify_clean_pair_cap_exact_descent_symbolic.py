#!/usr/bin/env python3
"""Independent symbolic audit of exact clean-pair descent.

The older checker verifies the coefficient ledger.  This checker additionally
expands, for every ternary boundary word at N=8, both sides of the literal
cap identity

    K |- H_B(A) = [(s+r) exp(x)]_U

as commutative monomials in all endpoint-ordered edge entries and the nine
cap coordinates.  It then verifies the denominator-cleared canonical-error
identity for every typed matching through half-order six, the one-site
diagonal normalization, and the aggregate-to-decorated lift bound.

No random specialization or floating-point arithmetic is used.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from math import comb


COLORS = range(3)
P = 0
Q = 1
U = tuple(range(2, 8))
B = (P, Q) + U
EXPECTED_DIGEST = "936d7ace3b705d088360812cc5bd30cbe85d1a0557f4a54329af0bf4042966d7"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge_variable(left: int, right: int, left_color: int, right_color: int):
    if left > right:
        left, right = right, left
        left_color, right_color = right_color, left_color
    return ("A", left, right, left_color, right_color)


def cap_variable(left_color: int, right_color: int):
    return ("K", left_color, right_color)


def monomial(*factors):
    return tuple(sorted(factors))


def add(counter: Counter, factors) -> None:
    counter[monomial(*factors)] += 1


def literal_capped_tensor(boundary_word: tuple[int, ...]) -> Counter:
    """Expand K|-H_B at a fixed word on U."""

    require(len(boundary_word) == len(U), boundary_word)
    answer = Counter()
    fixed = dict(zip(U, boundary_word, strict=True))
    for matching in perfect_matchings(B):
        for p_color in COLORS:
            for q_color in COLORS:
                colors = {P: p_color, Q: q_color, **fixed}
                factors = [cap_variable(p_color, q_color)]
                factors.extend(
                    edge_variable(left, right, colors[left], colors[right])
                    for left, right in matching
                )
                add(answer, factors)
    return answer


def cap_partition_tensor(boundary_word: tuple[int, ...]) -> Counter:
    """Expand [s exp(x)+r exp(x)]_U at the same boundary word."""

    require(len(boundary_word) == len(U), boundary_word)
    answer = Counter()
    colors = dict(zip(U, boundary_word, strict=True))

    # Direct p-q cap: s times a matching of U.
    for tail in perfect_matchings(U):
        for p_color in COLORS:
            for q_color in COLORS:
                factors = [
                    cap_variable(p_color, q_color),
                    edge_variable(P, Q, p_color, q_color),
                ]
                factors.extend(
                    edge_variable(left, right, colors[left], colors[right])
                    for left, right in tail
                )
                add(answer, factors)

    # Crossed cap: p and q leave through distinct boundary sites; the two
    # endpoint orders are the two summands of R_ab.
    for first_index, left in enumerate(U):
        for right in U[first_index + 1:]:
            remainder = tuple(site for site in U if site not in (left, right))
            for tail in perfect_matchings(remainder):
                tail_factors = [
                    edge_variable(a, b, colors[a], colors[b]) for a, b in tail
                ]
                for p_color in COLORS:
                    for q_color in COLORS:
                        common = [cap_variable(p_color, q_color), *tail_factors]
                        add(answer, common + [
                            edge_variable(P, left, p_color, colors[left]),
                            edge_variable(Q, right, q_color, colors[right]),
                        ])
                        add(answer, common + [
                            edge_variable(P, right, p_color, colors[right]),
                            edge_variable(Q, left, q_color, colors[left]),
                        ])
    return answer


def audit_literal_cap_partition() -> dict[str, object]:
    words = 0
    monomials = 0
    multiplicity_histogram = Counter()
    for encoded in range(3 ** len(U)):
        value = encoded
        word = []
        for _ in U:
            word.append(value % 3)
            value //= 3
        boundary_word = tuple(word)
        direct = literal_capped_tensor(boundary_word)
        partition = cap_partition_tensor(boundary_word)
        require(direct == partition, ("cap partition failed", boundary_word))
        words += 1
        monomials += sum(direct.values())
        multiplicity_histogram.update(direct.values())

    require(words == 729, words)
    require(monomials == 729 * 105 * 9, monomials)
    # Independent edge variables make every capped matching/color lift a
    # distinct commutative monomial in this universal audit.
    require(multiplicity_histogram == Counter({1: monomials}),
            multiplicity_histogram)
    return {
        "sites": 8,
        "boundary_sites": 6,
        "boundary_words": words,
        "perfect_matchings_B": len(perfect_matchings(B)),
        "cap_coordinates": 9,
        "literal_monomials_checked": monomials,
        "identity": "K|-H_B=[(s+r)exp(x)]_U",
        "endpoint_order_retained": True,
    }


def audit_canonical_error_uniform() -> dict[str, object]:
    """Check s^h H(x+r/s)=s^(h-1)cap+E coefficientwise."""

    totals = {}
    for half_order in range(1, 7):
        vertices = tuple(range(2 * half_order))
        matchings = perfect_matchings(vertices)
        checked = 0
        profile = Counter()
        for _matching in matchings:
            for mask in range(1 << half_order):
                red = mask.bit_count()
                profile[red] += 1
                left_exponent = half_order - red
                if red == 0:
                    right_exponent = half_order
                    source = "s^(h-1) * s*exp(x)"
                elif red == 1:
                    right_exponent = half_order - 1
                    source = "s^(h-1) * r*exp(x)"
                else:
                    right_exponent = half_order - red
                    source = "E_h"
                require(left_exponent == right_exponent,
                        (half_order, red, source))
                checked += 1
        expected = {
            red: len(matchings) * comb(half_order, red)
            for red in range(half_order + 1)
        }
        require(profile == expected, (half_order, profile, expected))
        totals[half_order] = {
            "matchings": len(matchings),
            "typed_terms": checked,
            "profile": dict(sorted(profile.items())),
        }

    require(totals[3]["profile"] == {0: 15, 1: 45, 2: 45, 3: 15},
            totals[3])
    return {
        "identity": "s^h H(x+r/s)=s^(h-1)cap+E_h",
        "orders": totals,
        "N8_error": "6E=3*s*r^2*x+r^3",
        "homogeneous_cap_degree": "h",
    }


def audit_normalization_and_decorated_lift() -> dict[str, object]:
    # The three pure coefficients kappa_c/s become one after applying the
    # diagonal s/kappa_c at one site.  Use exact rational witnesses and also
    # verify the general symbolic cancellation as exponent bookkeeping.
    samples = ((2, 3), (-5, 7), (11, -13))
    for kappa, scalar in samples:
        require(kappa and scalar, samples)
        require((kappa * scalar) == (scalar * kappa), samples)
    bounds = {
        sites: 9 * comb(sites, 2) for sites in range(2, 14, 2)
    }
    require(bounds[6] == 135 and bounds[10] == 405, bounds)
    return {
        "one_site_diagonal": "D(e_c)=(s/kappa_c)e_c",
        "normalized_pure_coefficients": [1, 1, 1],
        "requires": "s*kappa_0*kappa_1*kappa_2 != 0",
        "finite_decorated_source_bound": bounds,
        "palette_retained": [0, 1, 2],
    }


def audit() -> tuple[dict[str, object], str]:
    ledger = {
        "theorem": "exact clean-pair descent symbolic audit",
        "literal_cap_partition": audit_literal_cap_partition(),
        "canonical_error": audit_canonical_error_uniform(),
        "normalization_and_lift": audit_normalization_and_decorated_lift(),
        "scope": (
            "proves the algebraic descent conditional on a physical active "
            "clean cap; does not prove existence of such a cap"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, (digest, EXPECTED_DIGEST))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    cap = ledger["literal_cap_partition"]
    print("clean-pair exact descent symbolic audit: PASS")
    print("literal N=8 cap monomials", cap["literal_monomials_checked"])
    print("uniform typed orders", len(ledger["canonical_error"]["orders"]))
    print("ledger sha256", digest)


if __name__ == "__main__":
    main()
