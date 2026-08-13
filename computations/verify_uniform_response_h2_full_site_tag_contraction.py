#!/usr/bin/env python3
"""Uniform all-order contraction of response second-Hasse direction tags.

For response order h on 2h residual sites, adjoin the two response endpoints
P,S.  The variables d,p_i,s_i,q_ij are precisely the edges PS,Pi,Si,ij of
K_(2h+2), and the response polynomial is its hafnian.  A nonzero Hasse[2]
direction is a two-edge matching on four sites.  For each four-set there
are three direction tags, and every complementary perfect matching gives
the same lower tail.  Hence the incidence component is

    K_{3,(2h-3)!!}.

The centered tag module has two dimensions per four-set.  The stabilizer
S4 of that four-set is transitive on its three perfect matchings, so its
coinvariants, and therefore all full-site coinvariants, vanish over Q.

The checker exhausts the literal incidence census and orbit claims through
h=6 and pins the h=3 full-rank computation.  The proof is the displayed
uniform combinatorial argument, not extrapolation from the finite sweep.
"""

from __future__ import annotations

from collections import defaultdict, deque
from hashlib import sha256
import importlib.util
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_full_site_groupoid_tag_contraction.py":
        "eb2acb53ca9364ff4639985996f75321800d74b798858cda04084e997a15aa23",
    "notes/h3-h2-full-site-groupoid-tag-contraction.md":
        "47394c03902597892a2a4c01bc488dfc34f782e635e822e946304e1d5686faf1",
}
EXPECTED_LEDGER_SHA256 = "ba7707e27bb111705953439d0d842af0fc762634dc0e04f816cc258a388e50cb"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def odd_double_factorial(value: int) -> int:
    require(value >= -1 and value % 2 == 1, value)
    if value <= 0:
        return 1
    return math.prod(range(1, value + 1, 2))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def pairings_of_four(sites: tuple[int, int, int, int]):
    answer = tuple(
        tuple(sorted(tuple(sorted(edge)) for edge in matching))
        for matching in perfect_matchings(tuple(sorted(sites)))
    )
    require(len(answer) == len(set(answer)) == 3, (sites, answer))
    return tuple(sorted(answer))


def act_matching(matching, permutation):
    return tuple(sorted(tuple(sorted((permutation[left], permutation[right])))
                        for left, right in matching))


def orbit_count(items, generators) -> int:
    unseen = set(items)
    count = 0
    while unseen:
        count += 1
        start = next(iter(unseen))
        unseen.remove(start)
        queue = deque((start,))
        while queue:
            item = queue.popleft()
            for permutation in generators:
                image = act_matching(item, permutation)
                if image in unseen:
                    unseen.remove(image)
                    queue.append(image)
    return count


def audit_order(h: int):
    residual = 2 * h
    site_count = residual + 2
    sites = tuple(range(site_count))
    components = tuple(itertools.combinations(sites, 4))
    pair_tags = tuple(
        matching
        for component in components
        for matching in pairings_of_four(component)
    )
    expected_components = math.comb(site_count, 4)
    expected_pairs = 3 * expected_components
    tails_per_component = odd_double_factorial(2 * h - 3)
    require(len(components) == expected_components
            and len(pair_tags) == len(set(pair_tags)) == expected_pairs,
            (h, len(components), len(pair_tags)))

    # Each direction pair covers one four-set.  A lower tail is any perfect
    # matching of its complement, giving K_(3,m) for that component.
    checked_incidences = 0
    for component in components:
        complement = tuple(site for site in sites if site not in component)
        tails = tuple(perfect_matchings(complement))
        require(len(tails) == tails_per_component, (h, component, len(tails)))
        checked_incidences += 3 * len(tails)

        # A transposition inside the four-set sends the first direction
        # matching to a distinct one, so its centered differences are zero
        # in full-site coinvariants.
        local = pairings_of_four(component)
        found_images = set()
        for left, right in itertools.combinations(component, 2):
            permutation = list(range(site_count))
            permutation[left], permutation[right] = right, left
            found_images.add(act_matching(local[0], permutation))
        require(set(local).issubset(found_images),
                (h, component, local, found_images))

    generators = []
    for index in range(site_count - 1):
        permutation = list(range(site_count))
        permutation[index], permutation[index + 1] = index + 1, index
        generators.append(tuple(permutation))
    require(orbit_count(pair_tags, generators) == 1,
            (h, "two-edge matching action not transitive"))

    return {
        "h": h,
        "physical_sites": site_count,
        "four_set_components": expected_components,
        "direction_pairs": expected_pairs,
        "tails_per_component": tails_per_component,
        "incidences": checked_incidences,
        "component_graph": f"K_3_{tails_per_component}",
        "centered_tag_dimension": 2 * expected_components,
        "direction_pair_orbits_under_full_site_group": 1,
        "four_set_orbits_under_full_site_group": 1,
        "coinvariant_dimension_over_Q": 0,
    }


def audit():
    pin_dependencies()
    h3 = load(
        "computations/verify_h3_h2_full_site_groupoid_tag_contraction.py",
        "h3_full_site_tag",
    )
    _h3_ledger, h3_digest = h3.audit()
    require(h3_digest
            == "32598f0d35eb7b57b5885481d9d7590bb85a9f27a0f4de8078a9955b46c51ffe",
            h3_digest)
    orders = [audit_order(h) for h in range(2, 7)]
    require(orders[1]["centered_tag_dimension"] == 140
            and orders[1]["tails_per_component"] == 3,
            orders[1])

    ledger = {
        "theorem": "uniform response-H2 full-site direction-tag contraction",
        "pins": PINS,
        "orders_exhaustively_audited": orders,
        "uniform_proof": {
            "response_as_extended_hafnian": (
                "d,p_i,s_i,q_ij are edges PS,Pi,Si,ij of K_(2h+2)"
            ),
            "component": "one four-set, three two-edge matchings, (2h-3)!! complementary tails",
            "local_contraction": (
                "the S4 stabilizer of the four-set is transitive on its "
                "three matchings, so both centered differences vanish in coinvariants"
            ),
            "characteristic": "zero (Maschke/exact coinvariants)",
        },
        "physical_scope": (
            "conditional on a termwise source-valid PP comparison natural "
            "under changing the exposed response endpoint sites; this theorem "
            "does not construct that comparison or downstream word-grade carriers"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    for order in ledger["orders_exhaustively_audited"]:
        print("h={h}: components={four_set_components}, tags={direction_pairs}, "
              "tails/component={tails_per_component}, coinvariants=0".format(**order))
    print("uniform proof: S4 acts transitively on the three matchings of every four-set")
    print("physical endpoint-choice-natural PP comparison: STILL REQUIRED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
