#!/usr/bin/env python3
"""Unary matching reselection on the bridge-dark Hall triangle.

For a pure-zero edge matrix Z on an even residual set U, write H_uv for
the hafnian after deleting u,v.  The literal site expansion is

    haf(Z) = sum_{v != u} z_uv H_uv.

Hence haf(Z)=1 and H_uv=0 for u in A, v in B force, at every u in A, a
nonzero product z_uw H_uw with w outside B.  A nonzero monomial of H_uw
then supplies a selected pure-zero perfect matching through the escape uw.

The checker verifies the matching partition uniformly through ten residual
sites and freezes a physical six-site guard: the complete unary tensor is
X0 and selected colour-one/two cofactors are nonzero, while H_ab=0.  Thus
the unary row forces reselection, not an A--B bridge by itself.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_hall_star_triangle_bridge_boundary.py":
        "99c2c0038fefd0da51ff46bbf4d29ab6c8cfb72a79c1acf74e6334e9b4fd239e",
    "notes/uniform-multisite-hall-star-triangle-bridge-boundary.md":
        "04dfba66088cf72a021fbb9c277ca89d2991b27de892cec2b23069c5a3a20139",
}
EXPECTED_LEDGER_SHA256 = "6c58ee37e2e6ea798df02e9c25dc535ec4e2e8e9af8cb78acfd4dabe25522fdf"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield (edge(first, second),) + tail


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def audit_site_recursion_partition():
    audits = []
    for size in (2, 4, 6, 8, 10):
        vertices = tuple(range(size))
        matchings = tuple(perfect_matchings(vertices))
        by_mate = {}
        for mate in vertices[1:]:
            tails = tuple(perfect_matchings(
                tuple(site for site in vertices if site not in (0, mate))))
            lifted = {
                tuple(sorted((edge(0, mate),) + tail)) for tail in tails
            }
            by_mate[mate] = lifted
        union = set().union(*by_mate.values())
        require(union == {tuple(sorted(matching)) for matching in matchings},
                f"site recursion missed a matching at residual size {size}")
        require(sum(len(block) for block in by_mate.values()) == len(union),
                f"site recursion blocks overlap at residual size {size}")
        audits.append({
            "residual_sites": size,
            "perfect_matchings": len(matchings),
            "mate_blocks": len(by_mate),
            "terms_per_block": len(next(iter(by_mate.values()))),
        })
    return audits


def coefficient(support, word):
    terms = []
    for matching in perfect_matchings(range(len(word))):
        labels = tuple((pair, word[pair[0]]) for pair in matching)
        if all(word[left] == word[right] for left, right in matching) \
                and all(label in support for label in labels):
            terms.append(labels)
    return tuple(terms)


def audit_six_site_bridge_dark_guard():
    # c=0, a=1, b=2.  The pure-zero matching escapes from a to 4 and
    # from b to 5, so the a-b cofactor is zero.  The two other colours
    # retain the exact selected cofactors required by the Hall triangle.
    c, a, b = 0, 1, 2
    m0 = (edge(0, 3), edge(1, 4), edge(2, 5))
    m1 = (edge(2, 3), edge(4, 5))       # holes c,a
    m2 = (edge(1, 3), edge(4, 5))       # holes b,c
    support = (
        {(pair, 0) for pair in m0}
        | {(pair, 1) for pair in m1}
        | {(pair, 2) for pair in m2}
    )
    nonzero_top = []
    for word in itertools.product(range(3), repeat=6):
        terms = coefficient(support, word)
        if terms:
            nonzero_top.append(("".join(map(str, word)), len(terms)))
    require(nonzero_top == [("000000", 1)],
            f"the bridge-dark guard stopped satisfying q^[3]=X0: {nonzero_top}")

    complement_ab = tuple(site for site in range(6) if site not in (a, b))
    h_ab_terms = tuple(perfect_matchings(complement_ab))
    supported_h_ab = [matching for matching in h_ab_terms
                      if all((pair, 0) in support for pair in matching)]
    require(not supported_h_ab,
            "the bridge-dark guard acquired a pure-zero a-b cofactor")
    require(all((pair, 1) in support for pair in m1)
            and all((pair, 2) in support for pair in m2),
            "a selected diagonal cofactor disappeared")

    # Identify the response rows which the guard deliberately does not
    # satisfy.  This prevents reading it as a one-bad counterexample.
    response_debts = {
        "11_holes_ca": ("1111", "1122"),
        "22_holes_bc": ("2211", "2222"),
        "21_holes_ba": ("0011", "0022"),
    }
    return {
        "sites": {"centre": c, "leaf1": a, "leaf2": b},
        "pure_zero_matching": [list(pair) for pair in m0],
        "selected_colour1_cofactor": [list(pair) for pair in m1],
        "selected_colour2_cofactor": [list(pair) for pair in m2],
        "nonzero_unary_outputs": nonzero_top,
        "H0_ab_supported_terms": len(supported_h_ab),
        "deliberately_missing_response_rows": response_debts,
    }


def audit_domain_inference():
    # A symbolic finite sum equal to one cannot have every term zero.  Once
    # all B-indexed terms are zero, an outside term is nonzero.  In a domain
    # its edge factor and cofactor are separately nonzero.
    terms = {"b0": 0, "b1": 0, "escape0": 2, "escape1": -1}
    require(sum(terms.values()) == 1,
            "the normalized bridge-dark site recursion guard changed")
    live_outside = tuple(name for name, value in terms.items()
                         if name.startswith("escape") and value)
    require(live_outside == ("escape0", "escape1"),
            "the abstract unary escape inference changed")
    return {
        "identity": "1=sum_(v!=a) z_av*H0_av",
        "dark_terms": ["z_ab*H0_ab=0 for b in B"],
        "consequence": (
            "some d outside B has z_ad*H0_ad nonzero; over a domain, "
            "choose a nonzero matching monomial in H0_ad and reselect M0 "
            "through a-d"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "site_recursion_audit": audit_site_recursion_partition(),
        "domain_inference": audit_domain_inference(),
        "six_site_sharp_guard": audit_six_site_bridge_dark_guard(),
        "theorem": (
            "if haf(Z)=1 and H0_ab=0 for all a in A,b in B, then every "
            "a in A has an active pure-zero escape a-d with d outside B; "
            "a selected unary matching can be reselected through a-d"
        ),
        "sharpness": (
            "the complete unary tensor and nonzero selected diagonal "
            "cofactor monomials do not force an A-B bridge; the complete "
            "diagonal and crossed response rows remain indispensable"
        ),
        "scope": (
            "uniform hafnian recursion over an integral domain plus a "
            "six-site source-labelled guard; not a full response packet"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"bridge-dark unary ledger changed: {digest}")
    print("uniform bridge-dark unary reselection: PASS")
    print("haf(Z)=1 -> every dark leaf has an active escape outside the opposite set")
    print("six-site guard: q^[3]=X0 and selected diagonal cofactors, but H0_ab=0")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
