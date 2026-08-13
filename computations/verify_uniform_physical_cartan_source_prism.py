#!/usr/bin/env python3
"""Uniform source provenance of the endpoint-odd physical Cartan prism.

The complete perfect-matching tensor is equivariant under every local colour
change.  A physical site transposition disjoint from two root sites is an
automorphism of the complete presentation (and of a direct-free presentation
when it fixes the removed edge).  The signed Weyl target defect at the two
root sites is invariant under that transposition, so endpoint oddization
produces a genuine target-preserving relative source prism at every even
order.  Component incidence and augmented terminal grading are separate.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_matching_interference_head_invariance_cartan_gate.py":
        "17b84de9c22247d617b9919fb5cf18593300226619945c7e6b5f5cef029ab787",
    "computations/verify_oo_dark_potential_source_promotion_counterguard.py":
        "76bdd6c8ce19cc466995b235bade9114d7d2779b74bfcd25eea703c2d1de3db2",
}
EXPECTED_LEDGER_SHA256 = (
    "23516fe5ff27fda7e9906b5a0da9dcdbec3103a85b52d0006b972c856c3e5258"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


def decorated_monomial(matching, word):
    return tuple((left, right, word[left], word[right])
                 for left, right in matching)


def full_row(matchings, word):
    return tuple(decorated_monomial(matching, word) for matching in matchings)


def recolour_monomial(monomial, site, old, new):
    answer = list(monomial)
    positions = [index for index, cell in enumerate(answer)
                 if site in cell[:2]]
    require(len(positions) == 1,
            "a perfect matching lost unique site incidence")
    index = positions[0]
    left, right, a, b = answer[index]
    if left == site:
        require(a == old, "the root field met the wrong local colour")
        answer[index] = (left, right, new, b)
    else:
        require(right == site and b == old,
                "the root field met the wrong local colour")
        answer[index] = (left, right, a, new)
    return tuple(sorted(answer))


def transpose_site(site, first=0, second=1):
    if site == first:
        return second
    if site == second:
        return first
    return site


def transpose_word(word):
    answer = list(word)
    answer[0], answer[1] = answer[1], answer[0]
    return tuple(answer)


def transpose_monomial(monomial):
    answer = []
    for left, right, a, b in monomial:
        left = transpose_site(left)
        right = transpose_site(right)
        if left < right:
            answer.append((left, right, a, b))
        else:
            answer.append((right, left, b, a))
    return tuple(sorted(answer))


def signed_weyl_word(word, root_sites):
    answer = list(word)
    sign = 1
    for site in root_sites:
        if answer[site] == 1:
            answer[site] = 2
            sign *= -1
        elif answer[site] == 2:
            answer[site] = 1
    return tuple(answer), sign


def audit_order(size):
    require(size >= 6 and size % 2 == 0,
            "the Cartan prism needs an even order at least six")
    root_sites = (2, 3)
    forbidden = edge(size - 2, size - 1)
    require(not set(root_sites) & set((0, 1))
            and not set(forbidden) & set((0, 1)),
            "the audit sites are not disjoint")

    complete = tuple(perfect_matchings(range(size)))
    direct_free = tuple(matching for matching in complete
                        if forbidden not in matching)
    expected_complete = 1
    for odd in range(1, size, 2):
        expected_complete *= odd
    expected_direct_free = expected_complete
    smaller = 1
    for odd in range(1, size - 2, 2):
        smaller *= odd
    expected_direct_free -= smaller
    require(len(complete) == expected_complete
            and len(direct_free) == expected_direct_free,
            "the matching counts changed")

    root_words = 0
    root_terms_complete = 0
    root_terms_direct_free = 0
    for site in root_sites:
        for old, new in ((1, 2), (2, 1)):
            for word in product(range(3), repeat=size):
                if word[site] != old:
                    continue
                changed = list(word)
                changed[site] = new
                changed = tuple(changed)
                transported = Counter(
                    recolour_monomial(monomial, site, old, new)
                    for monomial in full_row(complete, word))
                require(transported == Counter(full_row(complete, changed)),
                        "complete-row local root covariance failed")
                transported_df = Counter(
                    recolour_monomial(monomial, site, old, new)
                    for monomial in full_row(direct_free, word))
                require(transported_df
                        == Counter(full_row(direct_free, changed)),
                        "direct-free local root covariance failed")
                root_words += 1
                root_terms_complete += len(complete)
                root_terms_direct_free += len(direct_free)

    swap_words = 0
    swap_terms_complete = 0
    swap_terms_direct_free = 0
    for word in product(range(3), repeat=size):
        require(Counter(transpose_monomial(monomial)
                        for monomial in full_row(complete, word))
                == Counter(full_row(complete, transpose_word(word))),
                "complete presentation lost transposition equivariance")
        require(Counter(transpose_monomial(monomial)
                        for monomial in full_row(direct_free, word))
                == Counter(full_row(direct_free, transpose_word(word))),
                "direct-free presentation lost transposition equivariance")
        swap_words += 1
        swap_terms_complete += len(complete)
        swap_terms_direct_free += len(direct_free)

    # The GHZ target has three monochromatic words.  Its signed Weyl defect
    # at root_sites is invariant under the disjoint endpoint transposition.
    delta = Counter({(colour,) * size: 1 for colour in range(3)})
    w_delta = Counter()
    for word, coefficient in delta.items():
        changed, sign = signed_weyl_word(word, root_sites)
        w_delta[changed] += coefficient * sign
    defect = Counter(w_delta)
    defect.subtract(delta)
    defect = Counter({word: value for word, value in defect.items() if value})
    transposed_defect = Counter()
    for word, coefficient in defect.items():
        transposed_defect[transpose_word(word)] += coefficient
    require(transposed_defect == defect,
            "endpoint oddization stopped killing the target defect")

    return {
        "order": size,
        "complete_matchings": len(complete),
        "direct_free_matchings": len(direct_free),
        "root_sites": list(root_sites),
        "endpoint_transposition": [0, 1],
        "fixed_forbidden_edge": list(forbidden),
        "root_words": root_words,
        "root_terms_complete": root_terms_complete,
        "root_terms_direct_free": root_terms_direct_free,
        "swap_words": swap_words,
        "swap_terms_complete": swap_terms_complete,
        "swap_terms_direct_free": swap_terms_direct_free,
        "endpoint_odd_target_defect": 0,
    }


def main():
    pin_dependencies()
    orders = [audit_order(size) for size in (6, 8)]
    ledger = {
        "pins": PINS,
        "finite_audits": orders,
        "uniform_theorem": (
            "for every even order, the complete perfect-matching tensor is "
            "equivariant under independent local colour changes.  Any "
            "physical transposition s disjoint from two signed-Weyl root "
            "sites is a source-presentation automorphism, and "
            "(1-s)(w-1)Delta=0.  Naturality of contraction on principal "
            "parts therefore makes K=(1-s)H_w a target-preserving physical "
            "relative Cartan prism.  The same holds in a direct-free chart "
            "when s fixes the removed edge"
        ),
        "component_consequence": (
            "source provenance of the word-changing connector is uniform; "
            "the remaining component theorem is only to choose its roots "
            "and transposition so that its critical-block projection or "
            "complementary residual has the required fine labels and "
            "transverse quotient visibility"
        ),
        "scope": (
            "this does not identify the connector with an occupied scalar "
            "cell, prove its critical-component projection nonzero, or "
            "supply branch-specific residue/terminal grading outside the "
            "canonical h=3 packet"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
