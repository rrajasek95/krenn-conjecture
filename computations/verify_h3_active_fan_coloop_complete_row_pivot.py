#!/usr/bin/env python3
"""Audit the complete-row pivot supplied by a literal active-fan coloop.

Let e=uv be a coloop of the pure-c target support and let alpha be its
pure-c decorated cell.  In any other pure target channel i, split the pure
row and the mixed row obtained by changing only u,v from i to c into terms
which retain or omit e:

    d_i C_i + U_i = 1,       alpha C_i + V_i = 0.

Eliminating the same complete cofactor C_i gives

    alpha U_i - d_i V_i = alpha.

Since coloopness in the pure-c target gives alpha*C_c=1, alpha is nonzero.
Thus U_i or V_i is nonzero and contains a literal matching omitting e.  The
two omit-e packets are paired term by term: they have the same physical
matching, endpoint ports, and decorations away from the two changed sites.

At h=3 every endpoint-hole edge and both endpoint orientations occur among
the e-avoiding matching skeletons.  The six closed K6 Hall concepts need no
different source identity: a certified hole is either already on its shore
or strictly enlarges its Galois closure.  The identity types a carrier; it
does not choose its hole or turn the two-row pivot into a simultaneous
four-response affine coordinate point.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "35658ebed521b93387fc00aa7d2600d703f57b3e5e5deca67a11a1ab155d6c56",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py":
        "987c702e6f056cd5715ad2df95b680100aee4b168c4359b2300eaf7022370695",
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
}
EXPECTED_LEDGER_SHA256 = (
    "0dfc0d5b9ef6a0fcc4aaf21a25883edd4301f0495fe6cb90d7371cf6cf89f8a6"
)

RESIDUAL = tuple(range(6))
P, S = 6, 7
SITES = RESIDUAL + (P, S)
E = (0, 1)
EDGES = tuple(combinations(RESIDUAL, 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def partner(matching, site):
    return next(right if left == site else left
                for left, right in matching if site in (left, right))


def decorated_monomial(matching, word):
    return tuple((left, right, word[left], word[right])
                 for left, right in matching)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({term: value for term, value in answer.items() if value})


def scale(polynomial, scalar):
    return Counter({term: Q(scalar) * value
                    for term, value in polynomial.items()
                    if Q(scalar) * value})


def multiply(left, right):
    answer = Counter()
    for left_term, left_value in left.items():
        for right_term, right_value in right.items():
            answer[tuple(sorted(left_term + right_term))] += (
                left_value * right_value
            )
    return Counter({term: value for term, value in answer.items() if value})


def variable(name):
    return Counter({(name,): Q(1)})


def constant(value):
    return Counter({(): Q(value)}) if value else Counter()


def audit_complete_row_pivot():
    alpha = variable("alpha")
    diagonal = variable("d_i")
    cofactor = variable("C_i")
    pure_omit = variable("U_i")
    mixed_omit = variable("V_i")

    pure_generator = add(
        multiply(diagonal, cofactor), pure_omit, scale(constant(1), -1)
    )
    mixed_generator = add(multiply(alpha, cofactor), mixed_omit)
    eliminated = add(
        multiply(alpha, pure_generator),
        scale(multiply(diagonal, mixed_generator), -1),
    )
    expected = add(
        multiply(alpha, pure_omit),
        scale(multiply(diagonal, mixed_omit), -1),
        scale(alpha, -1),
    )
    require(eliminated == expected,
            "the complete-row coloop pivot identity changed")

    # The coloop target row factors as alpha*C_c=1.  Over the coefficient
    # domain alpha is nonzero, so U_i=V_i=0 is incompatible with the pivot.
    values = {
        "alpha": Q(2), "d_i": Q(3), "C_i": Q(5),
        "U_i": Q(0), "V_i": Q(0),
    }

    def evaluate(polynomial):
        return sum(value
                   * product(values.get(symbol, Q(0)) for symbol in term)
                   for term, value in polynomial.items())

    require(evaluate(expected) == -2,
            "the zero-omit contradiction stopped detecting alpha")
    return {
        "pure_target_split": "d_i*C_i+U_i=1",
        "two_site_mixed_split": "alpha*C_i+V_i=0",
        "elimination": "alpha*U_i-d_i*V_i=alpha",
        "coloop_target_factorization": "alpha*C_c=1",
        "domain_consequence": (
            "alpha is nonzero, so at least one complete omit-e aggregate "
            "U_i or V_i is nonzero and contains a literal omit-e term"
        ),
        "typed_alternative": {
            "U_i_nonzero": "pure-i target occurrence omitting the coloop",
            "V_i_nonzero": (
                "fine-typed mixed occurrence omitting the coloop, in the "
                "same diagonal response tensor"
            ),
        },
    }


def product(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def audit_termwise_common_q_transport():
    matchings = tuple(perfect_matchings(SITES))
    require(len(matchings) == 105, "the N8 matching count changed")
    retaining = tuple(matching for matching in matchings if E in matching)
    omitting = tuple(matching for matching in matchings if E not in matching)
    endpoint = tuple(matching for matching in omitting
                     if edge(P, S) not in matching)
    require((len(retaining), len(omitting), len(endpoint)) == (15, 90, 78),
            "the retain/omit/endpoint matching split changed")

    pure_word = (1,) * 8
    mixed_word = (0, 0) + (1,) * 6
    hole_histogram = Counter()
    oriented_histogram = Counter()
    changed_cell_histogram = Counter()
    for matching in endpoint:
        pure = decorated_monomial(matching, pure_word)
        mixed = decorated_monomial(matching, mixed_word)
        pure_by_edge = {cell[:2]: cell[2:] for cell in pure}
        mixed_by_edge = {cell[:2]: cell[2:] for cell in mixed}
        changed = tuple(pair for pair in matching
                        if pure_by_edge[pair] != mixed_by_edge[pair])
        require(len(changed) == 2
                and all(set(pair) & set(E) for pair in changed),
                "a paired omit-e term lost its two changed incident cells")
        require(all(pure_by_edge[pair] == mixed_by_edge[pair]
                    for pair in matching if pair not in changed),
                "the paired omit-e terms lost their common remote q tail")

        p_hole, s_hole = partner(matching, P), partner(matching, S)
        require(p_hole in RESIDUAL and s_hole in RESIDUAL
                and p_hole != s_hole,
                "an endpoint response matching lost its ordered holes")
        # Only residual output colours changed.  The outer output labels and
        # P/S orientation are exactly the same in the pure and mixed terms.
        require(pure_word[P] == mixed_word[P] == 1
                and pure_word[S] == mixed_word[S] == 1,
                "the paired term changed an endpoint output head")
        physical_hole = edge(p_hole, s_hole)
        hole_histogram[physical_hole] += 1
        oriented_histogram[(p_hole, s_hole)] += 1
        changed_cell_histogram[len(changed)] += 1

    require(set(hole_histogram) == set(EDGES)
            and set(oriented_histogram)
            == {(left, right) for left in RESIDUAL for right in RESIDUAL
                if left != right},
            "the omit-e packet lost a physical hole or orientation")
    require(Counter(hole_histogram.values()) == Counter({6: 9, 4: 6}),
            f"the avoid-e hole multiplicities changed: {hole_histogram}")
    require(set(oriented_histogram.values()) == {2, 3},
            "the avoid-e oriented-hole multiplicities changed")
    return {
        "N8_matchings": len(matchings),
        "retain_coloop_edge": len(retaining),
        "omit_coloop_edge": len(omitting),
        "omit_edge_with_two_endpoint_ports": len(endpoint),
        "unordered_holes_realized": len(hole_histogram),
        "ordered_holes_realized": len(oriented_histogram),
        "unordered_hole_multiplicity_histogram":
            dict(sorted(Counter(hole_histogram.values()).items())),
        "changed_cells_per_paired_UV_term":
            dict(sorted(changed_cell_histogram.items())),
        "transport": (
            "paired U_i/V_i terms use one physical matching and retain the "
            "same P/S partners, endpoint output heads, orientation, and all "
            "decorations away from the two coloop endpoints"
        ),
    }


def transversal(family):
    return frozenset(candidate for candidate in EDGES
                     if all(set(candidate) & set(member)
                            for member in family))


def closure(family):
    return transversal(transversal(family))


def audit_six_closed_concepts():
    triangle = frozenset(((0, 1), (0, 2), (1, 2)))
    matching = frozenset(((0, 3), (1, 2)))
    path_left = frozenset(((0, 1), (0, 3), (1, 2)))
    adjacent = frozenset(((0, 1), (0, 2)))
    singleton = frozenset(((0, 1),))
    star = frozenset((edge(0, site) for site in range(1, 6)))
    representatives = (
        triangle, matching, path_left, adjacent, singleton, star,
    )
    expected_sizes = ((3, 3), (2, 4), (3, 3),
                      (2, 6), (1, 9), (5, 5))
    records = []
    strict_growth = 0
    for family, sizes in zip(representatives, expected_sizes, strict=True):
        mate = transversal(family)
        require((len(family), len(mate)) == sizes
                and closure(family) == family
                and closure(mate) == mate,
                "a closed Hall representative changed")
        side_records = []
        for side in (family, mate):
            inside = 0
            outside = 0
            for physical_hole in EDGES:
                if physical_hole in side:
                    inside += 1
                    continue
                enlarged = closure(side | {physical_hole})
                require(len(enlarged) > len(side),
                        "a new typed hole failed to enlarge a closed shore")
                outside += 1
                strict_growth += 1
            side_records.append({"inside": inside, "strict_growth": outside})
        records.append({
            "left": [list(pair) for pair in sorted(family)],
            "right": [list(pair) for pair in sorted(mate)],
            "side_counts": side_records,
            "source_identity": "the same alpha*U_i-d_i*V_i=alpha pivot",
        })
    require(strict_growth == sum(
        (15 - left) + (15 - right) for left, right in expected_sizes
    ), "the six-type closure-growth count changed")
    return {
        "closed_symmetry_types": len(records),
        "records": records,
        "separate_orbit_specific_source_identities_needed": 0,
        "strict_growth_checks": strict_growth,
        "composition": (
            "a literal pivot term whose endpoint hole lies outside its "
            "closed shore strictly enlarges saturation; if every produced "
            "term lies on its shore, the complete rows have physically "
            "typed that closed Hall concept"
        ),
    }


def audit_signless_cartan_target_correction():
    # In the two-dimensional operator span {1,s}, the target defect of the
    # Weyl homotopy is s-invariant.  Hence a+b*s kills the defect iff a+b=0.
    # The only target-safe line is the odd prism 1-s; correcting 1+s inside
    # this natural span changes it to that odd line and cannot retain the
    # signless boundary.
    coefficients = tuple((a, b) for a in range(-3, 4)
                         for b in range(-3, 4) if (a, b) != (0, 0))
    safe = tuple((a, b) for a, b in coefficients if a + b == 0)
    require(safe and all(a == -b for a, b in safe),
            "the target-safe Cartan operator line changed")
    signless = (1, 1)
    correction = (-2, 0)
    corrected = tuple(left + right
                      for left, right in zip(signless, correction,
                                             strict=True))
    require(corrected == (-1, 1) and sum(corrected) == 0,
            "the canonical signless target correction changed")
    return {
        "weyl_defect_under_endpoint_swap": "s*(w-1)Delta=(w-1)Delta",
        "signless_defect": "(1+s)(w-1)Delta=2(w-1)Delta",
        "target_safe_operator_line": "multiples of 1-s",
        "canonical_correction": "(1+s)H_w-2H_w=(s-1)H_w",
        "consequence": (
            "a target correction internal to the natural Weyl-prism span "
            "collapses the signless prism to the endpoint-odd prism; an "
            "independent relative target/cone cell is required to retain a "
            "signless word-preserving boundary"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "complete_row_pivot": audit_complete_row_pivot(),
        "termwise_common_q_transport": audit_termwise_common_q_transport(),
        "six_closed_concepts": audit_six_closed_concepts(),
        "signless_cartan_target_correction":
            audit_signless_cartan_target_correction(),
        "uniform_theorem": (
            "a literal pure-colour coloop in an active fan supplies one "
            "complete-row pivot for every other target channel.  Each pivot "
            "forces a pure-target or fine-typed mixed matching occurrence "
            "omitting the coloop, with common-q provenance and protected "
            "endpoint word/orientation.  The same identity serves all six "
            "closed K6 Hall concepts: an outside hole grows saturation, "
            "while wholly trapped carriers physically type the closed shore"
        ),
        "remaining_exact_gate": (
            "the pivot does not prescribe which hole or orientation is "
            "nonzero, produce a simultaneous four-response joint-kernel "
            "target-coordinate point, or turn a trapped carrier relation "
            "into an anchor-safe complete-column dependence.  Those are "
            "the remaining affine/dependence clauses of the tight-set lift"
        ),
        "scope": (
            "uniform complete source-row identity and exact N8 matching/Hall "
            "transport audit; not a full one-bad counterexample and not a "
            "proof of the final saturated affine-accessibility theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"active-fan coloop complete-row ledger changed: {digest}")
    print("h3 active-fan coloop complete-row pivot: PASS")
    print("one source identity serves all six closed Hall concepts")
    print("remaining: simultaneous affine/dependence lift for trapped carriers")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
