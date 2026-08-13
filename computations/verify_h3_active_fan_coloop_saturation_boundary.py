#!/usr/bin/env python3
"""Freeze the finite saturation boundary for an h=3 active-fan coloop.

Once a physical complete-row lift supplies two nonempty effective endpoint
hole families A,B, failure to find disjoint holes says that A and B are
cross-intersecting.  On the fifteen edges of K6, the Galois operator

    T(A) = {e : e meets every edge of A}

turns this into a finite closure theorem.  Replacing A by T(T(A)) is
inflationary and idempotent; adding a genuinely new source-certified hole
strictly lowers the number of edges outside the closure.  The 446 closed
ordered concepts have only six S6-and-shore-swap orbit types.

This settles combinatorial termination after physical hole typing.  It does
not construct the load-bearing complete response-row lift from an arbitrary
private-site fan coloop to those effective hole families.  The checker also
replays the normalized h=3 target-coloop closures and the sharp lower Hall
boundaries so that this distinction cannot be lost.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "computations/verify_h3_axis_target_coloop_four_hole_exchange.py":
        "5283fae67a31ea3c9794fc8bbf351f7da5bc8251490dbdffbef04bde1f2a987f",
    "computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py":
        "e16f10abeb8d3ae8a40f2f6f57be9297d0bb49d7997214fe07861ef8dab6a307",
    "computations/verify_h3_c4_punctured_cube_alternate_target_lift.py":
        "15494dbdcf5d019d6fc858d2bad016a48dc966f63c672e739491a3692842c503",
    "computations/verify_h3_order6_double_coloop_conjugate_hall_interference.py":
        "3788b79a3d6965597207f9d96b8f09998d87bdb855da82636eb200c834985743",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "computations/verify_uniform_multisite_hall_star_source_reduction.py":
        "65ccab6e5830efd9f0dfa084c0d98391e89bad083fa7a41743b2fec7dde15bd5",
    "computations/verify_uniform_multisite_hall_star_colocated_unary_wedge_closure.py":
        "195c57ea9d315f685246e38f00a9b14a3fdf62de084ad84313d1fa953a9a9c29",
    "computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py":
        "987c702e6f056cd5715ad2df95b680100aee4b168c4359b2300eaf7022370695",
}
EXPECTED_LEDGER_SHA256 = (
    "769aba0337aa62354adb9353057f7eebff20a8dc29900a575ac5f8fbe321d4bb"
)

VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {physical_edge: index
              for index, physical_edge in enumerate(EDGES)}
FULL_MASK = (1 << len(EDGES)) - 1


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot import {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


MEETS = tuple(tuple(bool(set(left) & set(right))
                    for right in EDGES) for left in EDGES)


def mask_edges(mask):
    return tuple(EDGES[index] for index in range(len(EDGES))
                 if mask & (1 << index))


def transversal(mask):
    """All physical edges meeting every edge selected by mask."""
    return sum(
        1 << candidate for candidate in range(len(EDGES))
        if all(MEETS[candidate][selected]
               for selected in range(len(EDGES))
               if mask & (1 << selected))
    )


PERMUTATION_EDGE_MAPS = tuple(
    tuple(EDGE_INDEX[tuple(sorted((permutation[left], permutation[right])))]
          for left, right in EDGES)
    for permutation in permutations(VERTICES)
)


def permute_mask(mask, edge_map):
    return sum(1 << edge_map[index] for index in range(len(EDGES))
               if mask & (1 << index))


def orbit_key(left, right):
    images = []
    for edge_map in PERMUTATION_EDGE_MAPS:
        first = permute_mask(left, edge_map)
        second = permute_mask(right, edge_map)
        images.extend(((first, second), (second, first)))
    return min(images)


def audit_galois_saturation():
    families_with_mate = 0
    raw_shape_histogram = Counter()
    concepts = set()
    closure_preimages = Counter()
    for mask in range(1, FULL_MASK + 1):
        mate = transversal(mask)
        if not mate:
            continue
        families_with_mate += 1
        closure = transversal(mate)
        require(mask & ~closure == 0,
                "cross-intersection closure stopped being inflationary")
        require(transversal(transversal(closure)) == closure,
                "cross-intersection closure stopped being idempotent")
        require(transversal(closure) == mate,
                "Galois mate changed under closure")
        concept = (closure, mate)
        concepts.add(concept)
        closure_preimages[concept] += 1
        raw_shape_histogram[(len(mask_edges(closure)),
                             len(mask_edges(mate)))] += 1

    require(families_with_mate == 5141,
            "the nonempty cross-intersecting family count changed")
    require(len(concepts) == 446,
            "the closed ordered-concept count changed")

    orbit_concepts = Counter()
    orbit_preimages = Counter()
    for concept in concepts:
        key = orbit_key(*concept)
        orbit_concepts[key] += 1
        orbit_preimages[key] += closure_preimages[concept]
    require(len(orbit_concepts) == 6,
            "the S6-and-shore-swap concept orbit count changed")
    signature = sorted(
        (len(mask_edges(key[0])), len(mask_edges(key[1])),
         orbit_concepts[key], orbit_preimages[key])
        for key in orbit_concepts
    )
    require(signature == [
        (1, 9, 30, 3555),
        (2, 4, 90, 90),
        (2, 6, 120, 1200),
        (3, 3, 20, 20),
        (3, 3, 180, 180),
        (5, 5, 6, 96),
    ], f"the six closed-concept orbit signatures changed: {signature}")

    representatives = []
    for key in sorted(orbit_concepts,
                      key=lambda pair: (len(mask_edges(pair[0]))
                                        + len(mask_edges(pair[1])), pair)):
        representatives.append({
            "left": [list(pair) for pair in mask_edges(key[0])],
            "right": [list(pair) for pair in mask_edges(key[1])],
            "closed_ordered_concepts": orbit_concepts[key],
            "input_families_closing_to_orbit": orbit_preimages[key],
        })

    # A source-certified new edge outside a closed family strictly enlarges
    # its closure.  This is the only potential assertion used: no rule is
    # imposed on arbitrary reselections inside an unchanged closed family.
    strict_growth_checks = 0
    for closure, _mate in concepts:
        before = len(mask_edges(closure))
        for index in range(len(EDGES)):
            if closure & (1 << index):
                continue
            enlarged = transversal(transversal(closure | (1 << index)))
            require((closure | (1 << index)) & ~enlarged == 0
                    and len(mask_edges(enlarged)) > before,
                    "a new certified hole failed to enlarge saturation")
            strict_growth_checks += 1
    require(strict_growth_checks > 0,
            "the saturation-potential audit became vacuous")

    return {
        "nonempty_hole_families_with_cross_intersector": families_with_mate,
        "closed_ordered_concepts": len(concepts),
        "orbits_mod_S6_and_shore_swap": len(orbit_concepts),
        "orbit_signatures_left_right_concepts_preimages": signature,
        "orbit_representatives": representatives,
        "strict_new_hole_growth_checks": strict_growth_checks,
        "potential": (
            "15-|cl(A)|; every genuinely new source-certified hole outside "
            "the current Galois closure strictly lowers it, while saturating "
            "at once removes any possibility of a Hall/reselection cycle"
        ),
    }


def audit_committed_physical_routes():
    four_hole = load(
        "computations/verify_h3_axis_target_coloop_four_hole_exchange.py",
        "coloop_saturation_four_hole",
    )
    hybrid = load(
        "computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py",
        "coloop_saturation_hybrid",
    )
    punctured = load(
        "computations/verify_h3_c4_punctured_cube_alternate_target_lift.py",
        "coloop_saturation_punctured",
    )
    double = load(
        "computations/verify_h3_order6_double_coloop_conjugate_hall_interference.py",
        "coloop_saturation_double",
    )
    k22 = load(
        "computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py",
        "coloop_saturation_k22",
    )

    topology = four_hole.audit_tail_topology()
    require(topology["full_cycle_histogram"] == {
        "(4, 4)": 2, "(6,)": 1, "(8,)": 6,
    },
            "the four-hole target-coloop topology changed")
    hybrid_result = hybrid.audit_hybrid_escape()
    require(sum(hybrid_result["residual_kind_histogram"].values()) == 110,
            "the target-coloop hybrid normalization changed")
    punctured_words = punctured.audit_words_and_routes()
    punctured_cube = punctured.audit_cube_identity()
    require(punctured_words["alternate_L_tail"] == ["04:11", "15:11"]
            and "A_z*F_t" in punctured_cube["source_certificate"],
            "the final punctured-C4 target-coloop lift changed")
    double_result = double.audit()
    require(double_result["residual_packets"] == 270,
            "the conjugate double-coloop closure changed")
    k22_result = k22.audit_m3_complete_row_boundary()
    require("injective" in k22_result["unclosed_interface"],
            "the lower K2,2 M3 lock boundary changed")

    return {
        "four_distinct_hole_E2_topologies":
            topology["full_cycle_histogram"],
        "normalized_target_coloop_label_packets": 110,
        "final_punctured_C4_outcome": (
            "alternate pure-one target matching or offanchor offdiagonal exit"
        ),
        "normalized_double_coloop_packets":
            double_result["residual_packets"],
        "normalized_packet_verdict": (
            "after the active-fan coloop has the exact endpoint/common-q "
            "normal form, the committed later chain consumes its C6/C8, "
            "diagonal-return, punctured-C4, and double-coloop labels; the "
            "early 0556512 affine landing is not a surviving normalized "
            "target-coloop case"
        ),
        "lower_Hall_boundary": (
            "before that physical normalization, effective-hole saturation "
            "still permits the outer-centre Hall triangle and the strict "
            "K2,2 anchor-contained injective M3 five-lock/no-wedge packet"
        ),
        "M3_unclosed_interface": k22_result["unclosed_interface"],
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "finite_hole_saturation": audit_galois_saturation(),
        "committed_physical_routes": audit_committed_physical_routes(),
        "conditional_saturation_theorem": (
            "once complete source rows supply actual effective hole families "
            "and every nonzero residual is promoted to a new typed hole, "
            "the K6 process terminates: saturate by cl=T*T, take a target-"
            "line/free-fan exit if present, and otherwise face one of six "
            "closed Hall concepts.  A later hole strictly enlarges cl, so "
            "no separate move-by-move reselection potential is required"
        ),
        "missing_complete_row_lift": (
            "active-fan coloop tight-set lift: from Delta_ef*C_f!=0 and a "
            "literal pure-colour coloop, the complete mixed/unary/four-"
            "response rows must either give an anchor-safe complete-column "
            "dependence, a target-coordinate point, or a nonzero literal "
            "exchange outside the current Galois closure; otherwise they "
            "must realize the closed Hall covector with one common q tail, "
            "the correct endpoint orientations and response heads, all fine "
            "output grades, and protection of every selected mutual anchor"
        ),
        "theorem_level_scope": (
            "the finite K6 saturation closes termination and Hall-shadow "
            "classification only after physical hole typing.  It does not "
            "normalize an arbitrary active-fan coloop, prove affine line-"
            "hitting, lift an arbitrary Theorem-A circuit, handle repeated-"
            "site/determinant-dark entry, or close the injective M3 lock"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"active-fan coloop saturation ledger changed: {digest}")
    print("h3 active-fan coloop saturation boundary: PASS")
    print("closed ordered K6 Hall concepts: 446 in 6 S6/swap orbits")
    print("normalized target-coloop packets replayed to closure")
    print("remaining: complete-row active-fan tight-set lift")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
