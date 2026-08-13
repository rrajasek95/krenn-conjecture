#!/usr/bin/env python3
"""Singleton-mate closure and coloop gate for the h=3 axis-pure branch.

The support lower bound ``0ba6a00`` used a static no-singleton census.  This
checker replaces it by the structural closure operation forced by exactness:
if an off-target matching fibre has exactly one supported monomial M, an
exact source must contain another monomial N in that same fibre.  Adjoin the
missing coordinates of N and repeat.

For each of the 185 target-skeleton orbits, a branch-and-bound search chooses
the singleton with the fewest possible mates and explores every minimal
mate addition compatible with a support budget.  The closure is exhaustive:
every support satisfying the no-singleton necessary condition contains a
path in this tree, because it must contain a mate for the chosen singleton.

No closure exists through support 26.  At support 27 there are exactly 12
labelled closures, forming two S6 orbits which exchange under colours 1<->2.
Their common support type has:

* q:00 equal to one perfect matching F0;
* one bright colour supported on K_{2,2} over four sites;
* the other bright colour supported on K_{2,4};
* endpoint p/s rows supported on the matching four-site/two-site shores.

Every edge of F0 occurs in every pure-zero matching, hence is a literal
pure-colour coloop.  Thus the first possible coupled cancellation support is
already in the existing coloop branch.  The checker does not prove that the
support admits coefficients solving the full equations, nor close the
separate arbitrary-coloop normalization theorem.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import permutations
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = "computations/verify_h3_axis_pure_cancellation_support_lower_bound.py"
PINS = {
    BASE_PATH:
        "c7c501de4c4646b98e5525d616012bbced15957dcaaa836ebe38341c56385397",
    "notes/h3-axis-pure-cancellation-support-lower-bound.md":
        "b81542ec64eb0667c7c70109d15a0e92932d8e1ffeb124c87992a0abe96a41cc",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
}
EXPECTED_LEDGER_SHA256 = "17c8da7536f8e9b01e4fb6a30da1313080b03603453d751356dabdf17a26c7e4"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load_base():
    path = ROOT / BASE_PATH
    specification = importlib.util.spec_from_file_location(
        "axis_pure_support_base", path)
    require(specification is not None and specification.loader is not None,
            f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def singleton_mate_closure(base, terms_by_fibre, skeleton, budget):
    """Return all no-singleton closures and search statistics."""
    visited = set()
    closures = set()
    dead = Counter()
    branching = Counter()

    def visit(support):
        if support in visited:
            return
        visited.add(support)
        singleton_choices = []
        for fibre, terms in terms_by_fibre.items():
            if base.is_target_fibre(fibre) \
                    or base.fibre_count(terms, support) != 1:
                continue
            all_options = base.minimal_options(
                [term - support for term in terms if term - support]
            )
            options = tuple(option for option in all_options
                            if len(support | option) <= budget)
            if not options:
                family = base.row_family(fibre)
                dead[(len(support), family,
                      min(map(len, all_options), default=99))] += 1
                return
            singleton_choices.append((
                len(options), sum(map(len, options)),
                base.fibre_label(fibre), options,
            ))

        if not singleton_choices:
            closures.add(support)
            return

        _count, _cost, label, options = min(
            singleton_choices, key=lambda item: (item[0], item[1], item[2])
        )
        branching[(len(support), label, len(options))] += 1
        for option in options:
            visit(support | option)

    visit(skeleton)
    return closures, visited, dead, branching


def transport_support(base, support, permutation):
    return frozenset(base.transport_coordinate(coordinate, permutation)
                     for coordinate in support)


def full_site_orbits(base, closures):
    group = tuple(permutations(base.SITES))
    unseen = set(closures)
    orbits = []
    while unseen:
        support = min(unseen, key=base.support_key)
        orbit = {transport_support(base, support, permutation)
                 for permutation in group}
        unseen -= orbit
        orbits.append((min(orbit, key=base.support_key), len(orbit)))
    return tuple(sorted(orbits, key=lambda item: base.support_key(item[0])))


def colour_swap_12(support):
    answer = []
    for coordinate in support:
        if coordinate[0] == "q":
            kind, colour, physical = coordinate
            answer.append((kind, {1: 2, 2: 1}.get(colour, colour), physical))
        else:
            shore, label, site = coordinate
            answer.append((shore, {1: 2, 2: 1}.get(label, label), site))
    return frozenset(answer)


def pure_matching_support(base, support, colour):
    occupied = {
        coordinate[2] for coordinate in support
        if coordinate[0] == "q" and coordinate[1] == colour
    }
    return tuple(matching for matching in base.perfect_matchings(base.SITES)
                 if set(matching) <= occupied)


def graph_degrees(edges):
    degree = Counter()
    for left, right in edges:
        degree[left] += 1
        degree[right] += 1
    return tuple(sorted(degree.values()))


def star_sites(support, shore, label):
    return tuple(sorted(coordinate[2] for coordinate in support
                        if coordinate[:2] == (shore, label)))


def orbit_type(base, support):
    q_edges = {
        colour: frozenset(coordinate[2] for coordinate in support
                          if coordinate[0] == "q"
                          and coordinate[1] == colour)
        for colour in range(3)
    }
    pure = {colour: pure_matching_support(base, support, colour)
            for colour in range(3)}
    coloops = {
        colour: tuple(sorted(set.intersection(
            *(set(matching) for matching in pure[colour])
        ))) if pure[colour] else ()
        for colour in range(3)
    }

    require(len(q_edges[0]) == 3 and len(pure[0]) == 1
            and set(coloops[0]) == set(q_edges[0]),
            "the closure lost its pure-zero coloop matching")
    require(sorted(map(len, (q_edges[1], q_edges[2]))) == [4, 8],
            "the two bright q support sizes changed")
    # The degree tuples omit isolated vertices.  K2,2 is 2^4; K2,4 is
    # 4^2 2^4.
    bright_degrees = sorted((graph_degrees(q_edges[1]),
                             graph_degrees(q_edges[2])))
    require(bright_degrees == [
        (2, 2, 2, 2), (2, 2, 2, 2, 4, 4)
    ], ("the bright graph degree profiles changed", bright_degrees))

    star_profiles = {
        f"{shore}{label}": star_sites(support, shore, label)
        for shore in ("p", "s") for label in (1, 2)
    }
    require(sorted(map(len, star_profiles.values())) == [2, 2, 4, 4],
            "the endpoint shore sizes changed")
    require(star_profiles["p1"] == star_profiles["s1"]
            and star_profiles["p2"] == star_profiles["s2"],
            "the p/s shores stopped agreeing")

    return {
        "support_size": len(support),
        "q_support_sizes": {str(colour): len(q_edges[colour])
                            for colour in range(3)},
        "q_degree_profiles": {str(colour): list(graph_degrees(q_edges[colour]))
                              for colour in range(3)},
        "pure_matching_counts": {str(colour): len(pure[colour])
                                 for colour in range(3)},
        "pure_coloops": {str(colour): [list(item) for item in coloops[colour]]
                         for colour in range(3)},
        "endpoint_shores": {name: list(sites)
                            for name, sites in star_profiles.items()},
        "support": list(base.support_key(support)),
    }


def audit_closure():
    base = load_base()
    terms_by_fibre = base.all_matching_terms()
    representatives = base.skeleton_orbit_representatives(
        base.target_skeletons())

    budget_records = []
    closure27 = set()
    total_nodes27 = 0
    total_dead27 = Counter()
    total_branching27 = Counter()
    closures_by_skeleton27 = Counter()
    # Feasibility is monotone in the support budget, so emptiness at 26
    # proves emptiness for every smaller budget.  Auditing only 26 and 27
    # keeps the frozen checker fast while retaining the exact theorem.
    for budget in (26, 27):
        closures = set()
        nodes = 0
        for index, skeleton in enumerate(representatives):
            found, visited, dead, branching = singleton_mate_closure(
                base, terms_by_fibre, skeleton, budget)
            nodes += len(visited)
            closures |= {(index, support) for support in found}
            if budget == 27:
                closure27 |= {support for support in found}
                total_nodes27 += len(visited)
                total_dead27.update(dead)
                total_branching27.update(branching)
                if found:
                    closures_by_skeleton27[index] += len(found)
        budget_records.append({
            "support_budget": budget,
            "search_nodes": nodes,
            "closures": len(closures),
            "closure_sizes": dict(sorted(Counter(
                len(support) for _index, support in closures
            ).items())),
        })

    require(budget_records[0]["support_budget"] == 26
            and budget_records[0]["closures"] == 0,
            "a closure appeared at or below support 26")
    require(budget_records[-1]["closures"] == 12
            and budget_records[-1]["closure_sizes"] == {27: 12},
            "the first closure census changed")
    require(len(closure27) == 2 and total_nodes27 == 13615,
            ("the support-27 labelled closure audit changed",
             len(closure27), total_nodes27))
    require(closures_by_skeleton27 == {
        112: 1, 113: 1, 119: 1, 120: 1, 128: 1, 129: 1,
        141: 1, 142: 1, 156: 2, 157: 2,
    }, ("the closure skeleton incidences changed", closures_by_skeleton27))

    orbits = full_site_orbits(base, closure27)
    require(len(orbits) == 2
            and all(orbit_size == 45 for _support, orbit_size in orbits),
            "the support-27 S6 orbit structure changed")
    first_orbit = {transport_support(base, orbits[0][0], permutation)
                   for permutation in permutations(base.SITES)}
    require(colour_swap_12(orbits[1][0]) in first_orbit,
            "the two orbit types stopped being bright-colour transposes")
    orbit_types = [orbit_type(base, support) for support, _size in orbits]

    # Every q3 fibre with at least two matchings is an alternating-cycle
    # circuit.  On six sites, mate differences require either two or three
    # new q coordinates; this is the exchange cost which drives the closure.
    q_fibre_sizes = Counter()
    q_mate_costs = Counter()
    for fibre, terms in terms_by_fibre.items():
        if fibre[0] != "q3":
            continue
        q_fibre_sizes[len(terms)] += 1
        for index, left in enumerate(terms):
            for right in terms[index + 1:]:
                q_mate_costs[len(right - left)] += 1
    require(q_fibre_sizes == {1: 90, 3: 90, 15: 3}
            and q_mate_costs == {2: 405, 3: 180},
            "the unary matching-circuit exchange invariant changed")

    return {
        "target_skeleton_orbits": len(representatives),
        "budget_closure_census": budget_records,
        "first_closure_support": 27,
        "support27_labelled_closures": budget_records[-1]["closures"],
        "support27_distinct_F0_normalized_supports": len(closure27),
        "support27_skeleton_incidence": dict(sorted(
            closures_by_skeleton27.items())),
        "support27_search_nodes": total_nodes27,
        "support27_dead_states": sum(total_dead27.values()),
        "support27_branch_states": sum(total_branching27.values()),
        "full_site_orbits": len(orbits),
        "full_site_orbit_sizes": [size for _support, size in orbits],
        "bright_colour_swap_identifies_orbits": True,
        "orbit_types": orbit_types,
        "unary_matching_fibre_sizes": dict(sorted(q_fibre_sizes.items())),
        "unary_mate_new_coordinate_costs": dict(sorted(q_mate_costs.items())),
        "exchange_invariant": (
            "a singleton off-target monomial forces a mate in the same "
            "matching fibre; two matchings differ by alternating even cycles, "
            "and the missing half of those cycles is adjoined.  Iteration "
            "either exceeds the budget or reaches the K2,2/K2,4 coloop type."
        ),
        "theorem": (
            "no axis-purified support through 26 satisfies the necessary "
            "no-singleton full-row condition.  Every first support at 27 "
            "has a literal pure-zero perfect-matching coloop."
        ),
    }


def scope_and_landing():
    return {
        "minimum_support_consequence": (
            "a maximum-anchor/minimum-support exact axis source, if one "
            "exists, has support at least 27; at equality it lies in the "
            "literal pure-colour coloop branch"
        ),
        "what_is_not_claimed": (
            "the 27-coordinate supports satisfy only a necessary support "
            "condition; coefficient cancellation and the target equations "
            "may still be inconsistent"
        ),
        "existing_route_scope": (
            "the coloop is a literal pure-support coloop, exactly the output "
            "of the four-good-or-coloop matching theorem.  The separate "
            "arbitrary-coloop normalization/common-q landing remains open; "
            "this checker does not silently identify the support orbit with "
            "a normalized endpoint coloop packet"
        ),
        "next_theorem": (
            "either extend singleton-mate closure beyond the first stratum, "
            "or use the explicit K2,2/K2,4 incidence to normalize its F0 "
            "coloop into the committed target-coloop/Hall packet"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 axis-pure singleton-mate closure coloop gate",
        "pins": PINS,
        "closure_audit": audit_closure(),
        "scope_and_landing": scope_and_landing(),
        "verdict": (
            "the support-17 coupled-circuit stratum is empty.  In fact no "
            "axis-pure support through 26 can cancel every singleton full-"
            "row fibre.  The first possible supports occur at 27 in one "
            "structural type up to sites and bright-colour swap: pure-zero "
            "matching, bright K2,2, and bright K2,4.  Each retains all three "
            "pure-zero matching edges as literal coloops, so the first "
            "cancellation stratum enters the existing coloop branch."
        ),
        "scope": (
            "canonical h=3 axis-purified support geometry over a field. "
            "No coefficient solution at support 27, arbitrary-coloop "
            "normalization, or global GHZ emptiness is claimed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("axis-pure singleton-mate closure: EMPTY THROUGH SUPPORT 26")
    print("first closure: support 27 / labelled closures 12 / S6 orbits 2")
    print("orbit type: PURE-0 MATCHING + BRIGHT K2,2 + BRIGHT K2,4")
    print("bright-colour swap identifies the two orbits")
    print("first cancellation stratum: LITERAL PURE-0 COLOOP")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
