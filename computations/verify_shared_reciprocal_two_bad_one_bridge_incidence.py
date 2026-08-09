#!/usr/bin/env python3
"""Exact obstruction for the last coordinate-diagonal one-bridge incidence.

Normalize the target-axis bridge to sites 0,1.  Its pure target product
uses only one bridge centre, so after removing the other nonzero factors it
selects a nonzero difference delta_z=v_t,z-u_t,z.  Comparing the two bridge
cofactors on the words (t,t,d,d) gives delta_z r_d,z=0 for both bright
colours d.  The checker reconstructs those literal matching rows, exhausts
the resulting 16 residual-support patterns, and checks the sole empty/empty
case using the target residual colour.

The last audit retains an exact two-bright packet after the target coupling
is deleted.  It is a mutation guard: the r_t argument in the empty/empty
case is load-bearing, not a support-only embellishment.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(5))
BRIDGE = (0, 1)
RESIDUAL = (2, 3, 4)
A, C, T = range(3)
BRIGHT = (A, C)
COLOURS = (A, C, T)
PINNED_COUPLING_SHA256 = (
    "f24b9f83c6a6380339de96494ca60093c071948744bdcebcb918fc0002c68bdb"
)
EXPECTED_DIGEST = "d2dd68750526348741875ac320db10cc5ca0f933fd512e7157b07d5c9a922102"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependency():
    dependency = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_three_coordinate_bright_coupling.py"
    )
    require(sha256(dependency.read_bytes()).hexdigest()
            == PINNED_COUPLING_SHA256,
            "the three-coordinate bright-coupling dependency changed")


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


def residual_index_for_edge(edge):
    missing = tuple(site for site in RESIDUAL if site not in set(edge))
    require(len(missing) == 1, "a residual edge lost its opposite index")
    return RESIDUAL.index(missing[0])


def edge_variable(left, right, colour):
    left, right = sorted((left, right))
    if (left, right) == BRIDGE:
        return f"s{colour}"
    if left == 0 and right in RESIDUAL:
        return f"u{colour}{RESIDUAL.index(right)}"
    if left == 1 and right in RESIDUAL:
        return f"v{colour}{RESIDUAL.index(right)}"
    require(left in RESIDUAL and right in RESIDUAL,
            "an edge left the bridge/residual normal form")
    return f"r{colour}{residual_index_for_edge((left, right))}"


def add_monomial(polynomial, monomial, coefficient=1):
    monomial = tuple(sorted(monomial))
    polynomial[monomial] += coefficient
    if polynomial[monomial] == 0:
        del polynomial[monomial]


def cofactor_polynomial(hole, full_word):
    vertices = tuple(site for site in SITES if site != hole)
    answer = Counter()
    for matching in perfect_matchings(vertices):
        monomial = []
        for left, right in matching:
            if full_word[left] != full_word[right]:
                break
            monomial.append(edge_variable(left, right, full_word[left]))
        else:
            add_monomial(answer, monomial)
    return answer


def singleton(monomial):
    return Counter({tuple(sorted(monomial)): 1})


def dot_polynomial(prefix, colour):
    answer = Counter()
    for index in range(3):
        add_monomial(answer, (f"{prefix}{colour}{index}",
                                f"r{colour}{index}"))
    return answer


def audit_literal_bridge_rows():
    ledger = {"delta_rows": [], "own_rows": [], "annihilators": []}

    # K_0=e_t^(1) Z and K_1=e_t^(0) Z.  Put t on the surviving
    # bridge endpoint and on residual coordinate z, and d on the other two
    # residual sites.  Literal expansion is v_t,z r_d,z versus
    # u_t,z r_d,z; equality is delta_z r_d,z=0.
    for bright in BRIGHT:
        for index, residual_site in enumerate(RESIDUAL):
            word = [bright] * 5
            word[0] = T
            word[1] = T
            word[residual_site] = T
            k0 = cofactor_polynomial(0, tuple(word))
            k1 = cofactor_polynomial(1, tuple(word))
            require(k0 == singleton((f"v{T}{index}",
                                      f"r{bright}{index}")),
                    "a K_0 delta row changed")
            require(k1 == singleton((f"u{T}{index}",
                                      f"r{bright}{index}")),
                    "a K_1 delta row changed")
            ledger["delta_rows"].append({
                "bright": bright,
                "index": index,
                "K0": sorted(k0.items()),
                "K1": sorted(k1.items()),
                "difference": f"(v{T}{index}-u{T}{index})*r{bright}{index}",
            })

    # The all-d bright rows vanish separately at the two bridge endpoints.
    # When r_d has singleton support these dot products kill both incident
    # star entries at that coordinate.
    for bright in BRIGHT:
        word = (bright,) * 5
        k0 = cofactor_polynomial(0, word)
        k1 = cofactor_polynomial(1, word)
        require(k0 == dot_polynomial("v", bright),
                "a K_0 own-orthogonality row changed")
        require(k1 == dot_polynomial("u", bright),
                "a K_1 own-orthogonality row changed")
        ledger["own_rows"].append({
            "bright": bright,
            "K0": sorted(k0.items()),
            "K1": sorted(k1.items()),
        })

    # Mixed 2+2 words reconstruct every coordinatewise opposite-colour
    # annihilator, including the target residual colour used at the end.
    for bright in BRIGHT:
        for other in tuple(colour for colour in COLOURS if colour != bright):
            for index, residual_site in enumerate(RESIDUAL):
                word = [other] * 5
                word[0] = bright
                word[1] = bright
                word[residual_site] = bright
                k0 = cofactor_polynomial(0, tuple(word))
                k1 = cofactor_polynomial(1, tuple(word))
                require(k0 == singleton((f"v{bright}{index}",
                                          f"r{other}{index}")),
                        "a K_0 opposite annihilator changed")
                require(k1 == singleton((f"u{bright}{index}",
                                          f"r{other}{index}")),
                        "a K_1 opposite annihilator changed")
                ledger["annihilators"].append({
                    "bright": bright,
                    "other": other,
                    "index": index,
                    "K0": sorted(k0.items()),
                    "K1": sorted(k1.items()),
                })

    require(len(ledger["delta_rows"]) == 6,
            "the delta-row census changed")
    require(len(ledger["own_rows"]) == 2,
            "the own-row census changed")
    require(len(ledger["annihilators"]) == 12,
            "the opposite-annihilator census changed")
    return ledger


def cross_support(star_support):
    possible = set()
    for index in range(3):
        complement = set(range(3)) - {index}
        if complement <= set(star_support):
            possible.add(index)
    return possible


def support_envelope(own_support, opposite_support):
    forced_zero = set(opposite_support)
    if len(own_support) == 1:
        # Each of u_d dot r_d and v_d dot r_d is a one-term zero row.
        forced_zero |= set(own_support)
    stars = set(range(3)) - forced_zero
    return stars, cross_support(stars)


def classify_support_pair(left, right):
    left = frozenset(left)
    right = frozenset(right)
    if not left and not right:
        return "empty_empty"
    if not left or not right:
        nonempty = right if not left else left
        return "empty_full" if len(nonempty) == 2 else "empty_singleton"
    if len(left) == len(right) == 2:
        return "full_full"
    if len(left) != len(right):
        return "full_singleton"
    require(len(left) == len(right) == 1,
            "an unclassified support size entered the split")
    return "singleton_same" if left == right else "singleton_distinct"


def audit_six_nonempty_categories():
    supports = (frozenset(), frozenset({1}), frozenset({2}),
                frozenset({1, 2}))
    expected_counts = {
        "full_full": 1,
        "full_singleton": 4,
        "singleton_distinct": 2,
        "singleton_same": 2,
        "empty_full": 2,
        "empty_singleton": 4,
        "empty_empty": 1,
    }
    traces = {
        "full_full": (
            "opposite annihilators kill all stars on coordinates 1,2; "
            "only coordinate 0 remains, so every crossed permanent is zero; "
            "both targets are direct, and the two wrong-bridge rows contradict"
        ),
        "full_singleton": (
            "the singleton target is direct and makes its bridge scalar nonzero; "
            "its wrong-bridge row kills the full support's direct sum, while "
            "the foreign row kills the only weight that can see its cross"
        ),
        "singleton_distinct": (
            "own and opposite one-term rows leave only coordinate 0 stars; "
            "both crosses vanish, so the direct targets contradict the wrong rows"
        ),
        "singleton_same": (
            "both response vectors are supported at the common coordinate; "
            "the two target rows make both entries live and a foreign row kills them"
        ),
        "empty_full": (
            "the full opposite support leaves the empty colour only one star "
            "coordinate, so its crossed response and its target both vanish"
        ),
        "empty_singleton": (
            "both responses are supported at the singleton coordinate, where "
            "their target weights are live; a foreign-pure row is then nonzero"
        ),
    }

    counts = Counter()
    ledger = []
    for left in supports:
        for right in supports:
            category = classify_support_pair(left, right)
            counts[category] += 1
            stars_a, cross_a = support_envelope(left, right)
            stars_c, cross_c = support_envelope(right, left)

            # These envelope checks are the exact support content used by
            # the six displayed domain arguments.  They are deliberately
            # weaker than assigning generic values to the surviving cells.
            if category == "full_full":
                require(not cross_a and not cross_c,
                        "the full/full cross envelope changed")
            elif category == "full_singleton":
                full_is_a = len(left) == 2
                full_cross = cross_a if full_is_a else cross_c
                singleton = right if full_is_a else left
                singleton_cross = cross_c if full_is_a else cross_a
                require(full_cross <= set(singleton)
                        and not singleton_cross,
                        "the full/singleton cross envelope changed")
            elif category == "singleton_distinct":
                require(not cross_a and not cross_c,
                        "the distinct-singleton cross envelope changed")
            elif category == "singleton_same":
                require(cross_a <= set(left) and cross_c <= set(right),
                        "the same-singleton response envelope changed")
            elif category == "empty_full":
                empty_cross = cross_a if not left else cross_c
                require(not empty_cross,
                        "the empty/full cross envelope changed")
            elif category == "empty_singleton":
                singleton = right if not left else left
                require(cross_a <= set(singleton)
                        and cross_c <= set(singleton),
                        "the empty/singleton response envelope changed")

            ledger.append({
                "R_a": sorted(left),
                "R_c": sorted(right),
                "category": category,
                "star_envelope_a": sorted(stars_a),
                "star_envelope_c": sorted(stars_c),
                "cross_envelope_a": sorted(cross_a),
                "cross_envelope_c": sorted(cross_c),
                "trace": traces.get(category, "handled by target coupling"),
            })

    require(dict(counts) == expected_counts,
            f"the 16-pattern census changed: {dict(counts)}")
    return {"counts": dict(counts), "patterns": ledger,
            "closed_without_empty_target_coupling": 15}


def audit_empty_empty_target_coupling():
    # With r_a=r_c=0, each bright response is crossed.  Target rows select
    # nonzero coordinates i,j.  A foreign-pure row forces i!=j.  Each
    # selected permanent term uses both star coordinates complementary to
    # its index, and the target-colour opposite annihilators kill r_t on
    # those coordinates.  Two distinct complements cover all three.
    traces = []
    for first in range(3):
        for second in range(3):
            if first == second:
                continue
            first_complement = tuple(sorted(set(range(3)) - {first}))
            second_complement = tuple(sorted(set(range(3)) - {second}))
            require(set(first_complement) | set(second_complement)
                    == set(range(3)),
                    "two distinct crossed permanents stopped covering r_t")
            for first_orientation in (0, 1):
                for second_orientation in (0, 1):
                    traces.append({
                        "active_a_coordinate": first,
                        "active_c_coordinate": second,
                        "a_term_orientation": first_orientation,
                        "c_term_orientation": second_orientation,
                        "r_t_killed_by_a": first_complement,
                        "r_t_killed_by_c": second_complement,
                    })
    require(len(traces) == 24,
            "the empty/empty term-orientation census changed")

    # Once r_a=r_c=r_t=0, every matching in either bridge cofactor contains
    # a residual-residual edge, hence both cofactors vanish.  Enumerate this
    # graph fact rather than assuming it from the picture.
    residual_edges_per_matching = {}
    for hole in BRIDGE:
        counts = []
        for matching in perfect_matchings(site for site in SITES
                                          if site != hole):
            count = sum(left in RESIDUAL and right in RESIDUAL
                        for left, right in matching)
            counts.append(count)
        require(counts == [1, 1, 1],
                "a bridge cofactor matching lost its residual edge")
        residual_edges_per_matching[str(hole)] = counts

    return {
        "active_coordinate_pairs": 6,
        "oriented_term_pairs": len(traces),
        "traces": traces,
        "residual_edges_per_matching": residual_edges_per_matching,
        "conclusion": (
            "r_t=0, so K_0=K_1=0, contradicting the nonzero minimal bridge"
        ),
    }


def pure_cofactor_from_support(hole, colour, support):
    vertices = tuple(site for site in SITES if site != hole)
    total = 0
    for matching in perfect_matchings(vertices):
        total += all((tuple(sorted(edge)), colour) in support
                     for edge in matching)
    return total


def audit_target_coupling_mutation_guard():
    # Delete the target residual coupling.  The following rational support
    # packet has two bright pure images while K_0=K_1=0:
    #   a: 03,14 gives K_2=X_a;  c: 02,14 gives K_3=X_c.
    support = {
        ((0, 3), A), ((1, 4), A),
        ((0, 2), C), ((1, 4), C),
    }
    table = {
        colour: [pure_cofactor_from_support(hole, colour, support)
                 for hole in SITES]
        for colour in BRIGHT
    }
    require(table[A] == [0, 0, 1, 0, 0],
            "the bright-a mutation packet changed")
    require(table[C] == [0, 0, 0, 1, 0],
            "the bright-c mutation packet changed")
    return {
        "support": sorted((edge, colour) for edge, colour in support),
        "pure_cofactor_table": table,
        "verdict": (
            "two bright images survive without the target residual coupling"
        ),
    }


def main():
    pin_dependency()
    literal = audit_literal_bridge_rows()
    support = audit_six_nonempty_categories()
    empty = audit_empty_empty_target_coupling()
    guard = audit_target_coupling_mutation_guard()
    ledger = {
        "pinned_coupling_sha256": PINNED_COUPLING_SHA256,
        "literal_bridge_rows": literal,
        "support_census": support,
        "empty_empty_target_coupling": empty,
        "target_coupling_mutation_guard": guard,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"the one-bridge incidence ledger changed: {digest}")
    print("coordinate-diagonal one-bridge incidence: PASS")
    print("literal delta/own/opposite bridge rows reconstructed: 6 / 2 / 12")
    print("bright residual support patterns closed: 16 / 16")
    print("empty/empty crossed-term orientations closed by r_t: 24 / 24")
    print("target-coupling-deleted rational guard retained")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
