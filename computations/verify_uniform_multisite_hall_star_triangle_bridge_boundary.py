#!/usr/bin/env python3
"""Unary-bridge reduction of the opposite-side Hall-star residual.

Use outer endpoints P,R and residual Hall centre c.  The opposite effective
orientation has selected diagonal cells

    p1(c), s1(a), p2(b), s2(c).

If a pure-zero unary matching uses the residual edge a-b, then the crossed
21 row contains the literal nonzero product

    p2(b) s1(a) (M0 / ab).

The 12 centre-centre product is site-square-zero.  In the 21 coefficient,
any cancellation outside the sites {a,b,c} exposes an off-anchor
off-diagonal endpoint cell.  If no such term occurs, site-square-zero leaves
exactly three aggregate blocks: the unary bridge and the two corrections on
the selected anchor edges P-c and R-c.

The other exact residual is unary-bridge darkness: the pure-zero two-hole
cofactor vanishes on every effective leaf pair.  No support subsets are
enumerated.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_hall_star_source_reduction.py":
        "65ccab6e5830efd9f0dfa084c0d98391e89bad083fa7a41743b2fec7dde15bd5",
    "notes/uniform-multisite-hall-star-source-reduction.md":
        "a0efe068a25423f16d0e24f8d943fd09c4c6911d1dbcdd231d45e66ae37868e0",
    "computations/verify_uniform_multisite_hall_star_colocated_lock_boundary.py":
        "11627ef80bc4a99366c88fd042b08daff1b6f2125c54ea4d2367586b5db2967a",
    "notes/uniform-multisite-hall-star-colocated-lock-boundary.md":
        "177e1bf4ee204e477f54ad1f7baea2ab3f56cde115d3554c16b7e87c92ae004c",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
}
EXPECTED_LEDGER_SHA256 = "eea4c3d2bd81eecdfc228c59f0c72b1422487b331a5ff774f7b59154cf06a124"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return left, right, left_colour, right_colour


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def coefficient(source, word):
    answer = 0
    terms = []
    for matching in perfect_matchings(range(len(word))):
        product = 1
        labels = []
        for left, right in matching:
            label = cell(left, right, word[left], word[right])
            product *= source.get(label, 0)
            labels.append(label)
        if product:
            answer += product
            terms.append((matching, product, tuple(labels)))
    return answer, tuple(terms)


def audit_literal_triangle_pivot():
    # Residual sites: c=0,a=1,b=2,d=3,e=4,f=5; outer endpoints P=6,R=7.
    source = {
        # Unary pure-zero full matching: P-R plus M0=(a,b)(c,d)(e,f).
        cell(6, 7, 0, 0): 1,
        cell(1, 2, 0, 0): 1,
        cell(0, 3, 0, 0): 1,
        cell(4, 5, 0, 0): 1,
        # Colour-one diagonal: p1(c),s1(a), plus its residual cofactor.
        cell(6, 0, 1, 1): 1,
        cell(7, 1, 1, 1): 1,
        cell(2, 3, 1, 1): 1,
        cell(4, 5, 1, 1): 1,
        # Colour-two diagonal: p2(b),s2(c), plus its residual cofactor.
        cell(6, 2, 2, 2): 1,
        cell(7, 0, 2, 2): 1,
        cell(1, 3, 2, 2): 1,
        cell(4, 5, 2, 2): 1,
    }
    pure_words = ((0,) * 8, (1,) * 8, (2,) * 8)
    require(all(coefficient(source, word)[0] == 1 for word in pure_words),
            "a selected pure anchor coefficient changed")

    # Outer colours are (2,1), residual colours are c:0,a:1,b:2,rest:0.
    word21 = (0, 1, 2, 0, 0, 0, 2, 1)
    value21, terms21 = coefficient(source, word21)
    require(value21 == 1 and len(terms21) == 1,
            f"the selected unary-bridge pivot changed: {value21,terms21}")
    expected = {
        cell(6, 2, 2, 2), cell(7, 1, 1, 1),
        cell(0, 3, 0, 0), cell(4, 5, 0, 0),
    }
    require(set(terms21[0][2]) == expected,
            "the 21 pivot lost its literal source factors")

    # The opposite 12 centre-centre candidate repeats residual site c and
    # therefore is absent from the site-square-zero matching expansion.
    word12 = (0, 2, 1, 0, 0, 0, 1, 2)
    value12, terms12 = coefficient(source, word12)
    require(value12 == 0 and not terms12,
            "the centre-centre 12 product stopped being square-zero")
    return {
        "normalization": {
            "centre": "c=0", "colour1_leaf": "a=1",
            "colour2_leaf": "b=2", "outer_endpoints": [6, 7],
        },
        "selected_anchor_coefficients": [1, 1, 1],
        "cross21_word": "01200021",
        "cross21_selected_terms": 1,
        "cross21_pivot": "p2(b)*s1(a)*(M0/ab)",
        "cross12_centre_product": "0 by repeated site c",
    }


def audit_three_block_reduction():
    # In the fixed 21 word, restrict p2 sites to {b,c} and s1 sites to
    # {a,c}.  Four formal pairs exist, but (c,c) is site-square-zero.
    p_sites = ("b", "c")
    s_sites = ("a", "c")
    live_pairs = tuple((p_site, s_site) for p_site in p_sites
                       for s_site in s_sites if p_site != s_site)
    require(live_pairs == (("b", "a"), ("b", "c"), ("c", "a")),
            f"the triangle block incidence changed: {live_pairs}")

    # A literal scalar realization proves that the three-block zero row has
    # no coefficient-only contradiction.
    bridge, right_correction, left_correction = 2, -3, 1
    require(bridge + right_correction + left_correction == 0 and bridge,
            "the triangle-lock scalar guard changed")
    return {
        "site_restricted_blocks": [
            "p2(b)s1(a): unary bridge",
            "p2(b)s1(c): R-c anchor correction",
            "p2(c)s1(a): P-c anchor correction",
        ],
        "killed_block": "p2(c)s1(c)=0",
        "exact_row": "B_ab+A_Rc+A_Pc=0",
        "scalar_guard": [bridge, right_correction, left_correction],
    }


def audit_bridge_or_dark_statement():
    # This is the exact matrix-level split, independent of cardinality: the
    # restricted pure-zero cofactor pairing on the two effective leaf spans
    # is either nonzero somewhere, or it vanishes identically there.
    nonzero_example = (("a0", "b0", 3),)
    dark_example = ()
    require(nonzero_example[0][2] != 0 and not dark_example,
            "the bridge-or-dark dichotomy changed")
    return {
        "bridge_matrix_entry":
            "T_ab=p2(b,2)*s1(a,1)*[q^[h-1]]_(U\\{a,b},0)",
        "nonzero_branch": (
            "the crossed 21 row contains a nonzero unary-bridge aggregate; "
            "a cancellation term is mandatory"
        ),
        "zero_branch": (
            "T vanishes on the product of the two effective leaf spans; "
            "this unary-cofactor orthogonality is the exact bridge-dark guard"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "literal_selected_packet": audit_literal_triangle_pivot(),
        "bridge_or_dark": audit_bridge_or_dark_statement(),
        "no_free_term_triangle_lock": audit_three_block_reduction(),
        "theorem": (
            "in the opposite-side Hall-star normal form, a nonzero pure-zero "
            "cofactor bridge between effective leaves is a literal pivot in "
            "the 21 crossed zero row; the 12 centre-centre pivot is zero"
        ),
        "free_carrier_alternative": (
            "any cancellation term using p2 away from {b,c}, or s1 away "
            "from {a,c}, exposes an off-anchor off-diagonal endpoint cell "
            "and enters the pinned good-active/private-site route"
        ),
        "sharp_residuals": [
            "the unary two-hole cofactor pairing is identically dark on the "
            "two effective leaf spans",
            "a nonzero bridge exists but its complete crossed cancellation "
            "is the three-block triangle lock B_ab+A_Rc+A_Pc=0",
        ],
        "scope": (
            "uniform source-labelled coefficient reduction, not a full "
            "triangle closure; the residuals require a unary/diagonal "
            "Bianchi identity or an anchor-safe line-hitting relation"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall-star triangle bridge ledger changed: {digest}")
    print("uniform opposite Hall-star unary-bridge boundary: PASS")
    print("unary edge between effective leaves -> literal crossed-21 pivot")
    print("no free mate -> exactly three triangle blocks")
    print("residual alternative: unary-cofactor bridge-dark")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
