#!/usr/bin/env python3
"""Reduce every evaluated h=3 active fan to four-good or a literal coloop.

For a physical pair p and each pure target colour c, let M_c be the complete
nonzero matching support of the pure-c coefficient.  The selected deleted-
star rank at either endpoint of p is exactly the number of colours for which
some matching in M_c avoids p.  Hence a source-provenant distinct-head active
fan on adjacent pairs e,f is four-good unless e or f is a literal coloop of
one of the three pure matching supports.

This argument uses the complete pure supports, so it is independent of
whether e is simple in one chosen anchor triple and of whether the fan is
contained in that chosen anchor union.  A balanced determinant supplies the
same entry on an actual zero mixed row: if every offdiagonal cell vanished,
the unique diagonal matching would equal both every balanced determinant
and the zero hafnian.  The checker exhausts all support families on K6
relative to one adjacent pair, all 27 ternary coloop-state assignments, and
a sharp adjacent-double-coloop/private-site guard.  It also replays the
balanced-only row and the committed normalized target-coloop closures.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_evaluated_determinant_transverse_landing_reduction.py":
        "73b7a1249c9856c4ac79e0c82a5bf8c024261d85199eef1781a51d4848732ca5",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    "computations/verify_uniform_axis_circuit_outside_endpoint_rank_restoration.py":
        "1af29dfddaf3127e758f07c53cf08189bda72df4e54a58a4e0ca78f6709874ac",
    "computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py":
        "e16f10abeb8d3ae8a40f2f6f57be9297d0bb49d7997214fe07861ef8dab6a307",
    "computations/verify_h3_c4_punctured_cube_alternate_target_lift.py":
        "15494dbdcf5d019d6fc858d2bad016a48dc966f63c672e739491a3692842c503",
    "computations/verify_h3_order6_double_coloop_conjugate_hall_interference.py":
        "3788b79a3d6965597207f9d96b8f09998d87bdb855da82636eb200c834985743",
    "computations/verify_h3_balanced_only_determinant_debt.py":
        "0e326c4a75b8afee0987c645cd2e7d9ca5feb85c80848bdca91823cc335171f6",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
}
EXPECTED_LEDGER_SHA256 = (
    "16840906f77635714d34915378e48c2d7c8902ba1a4ed520186aa28e49ab9f1a"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
WORD = (0, 0, 1, 1, 2, 2)
E = (0, 1)
F = (0, 2)


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


MATCHINGS = tuple(perfect_matchings(SITES))
require(len(MATCHINGS) == 15, "the K6 matching count changed")


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


def avoids(family, physical_edge):
    return any(physical_edge not in matching for matching in family)


def is_coloop(family, physical_edge):
    require(family, "pure matching support must be nonempty")
    return not avoids(family, physical_edge)


def certified_rank(families, physical_edge):
    # At either endpoint, one avoiding pure-c matching supplies a coordinate
    # (neighbour,c).  Different c occupy disjoint coordinate rows.
    return sum(avoids(family, physical_edge) for family in families)


def audit_all_support_families_for_adjacent_pair():
    status_histogram = Counter()
    nonempty_families = 0
    for mask in range(1, 1 << len(MATCHINGS)):
        family = tuple(matching for index, matching in enumerate(MATCHINGS)
                       if mask & (1 << index))
        e_coloop = is_coloop(family, E)
        f_coloop = is_coloop(family, F)
        # Adjacent edges cannot occur together in one perfect matching, so a
        # nonempty family cannot make both of them coloops.
        require(not (e_coloop and f_coloop),
                "adjacent pairs became coloops in one pure family")
        status = ("e_coloop" if e_coloop else
                  "f_coloop" if f_coloop else "neither")
        status_histogram[status] += 1
        nonempty_families += 1

    require(nonempty_families == 2 ** 15 - 1, "support-family count changed")
    require(status_histogram == {
        "neither": 32753, "e_coloop": 7, "f_coloop": 7,
    }, f"adjacent coloop status histogram changed: {status_histogram}")
    return {
        "nonempty_pure_support_families": nonempty_families,
        "status_histogram": dict(sorted(status_histogram.items())),
        "simultaneous_e_f_coloop_in_one_colour": 0,
    }


def audit_ternary_rank_alternative():
    # Every actual pure support has one of the three statuses audited above.
    # Enumerating status triples is therefore exhaustive for the rank
    # consequence, without pretending that arbitrary triples form a GHZ
    # source.
    rank_histogram = Counter()
    four_good = 0
    residual = 0
    for states in product(("neither", "e_coloop", "f_coloop"), repeat=3):
        rank_e = 3 - states.count("e_coloop")
        rank_f = 3 - states.count("f_coloop")
        rank_histogram[(rank_e, rank_f)] += 1
        if rank_e == rank_f == 3:
            require(states == ("neither",) * 3,
                    "rank-three pair retained a hidden coloop")
            four_good += 1
        else:
            require(any(state != "neither" for state in states),
                    "rank defect lost its literal coloop")
            residual += 1

    require(four_good == 1 and residual == 26,
            "ternary coloop-or-four-good split changed")
    return {
        "pure_support_status_assignments": 27,
        "four_good_assignments": four_good,
        "literal_coloop_assignments": residual,
        "rank_pair_histogram": [
            [list(key), count] for key, count in sorted(rank_histogram.items())
        ],
        "theorem": (
            "a distinct-head active fan e--f is four-good whenever every "
            "pure colour has an avoiding matching for each edge; otherwise "
            "one of the two physical edges is a literal pure-support coloop"
        ),
    }


def audit_sharp_adjacent_coloop_guard():
    # Three selected pure supports.  Colour 0 is concentrated on e, colour
    # 1 on f, and colour 2 avoids both.  The pairs are anchor-contained and
    # are adjacent at site 0.
    m0 = ((0, 1), (2, 3), (4, 5))
    m1 = ((0, 2), (1, 3), (4, 5))
    m2 = ((0, 3), (1, 2), (4, 5))
    families = ((m0,), (m1,), (m2,))
    require(is_coloop(families[0], E)
            and is_coloop(families[1], F)
            and certified_rank(families, E) == 2
            and certified_rank(families, F) == 2,
            "the adjacent two-colour coloop guard changed")
    anchors = set(m0) | set(m1) | set(m2)
    require(E in anchors and F in anchors,
            "the guard stopped being anchor-contained")

    # A literal local target-augmented private-site identity can coexist
    # with this matroid guard.  The reference offdiagonal cell is q_e=1;
    # the transition determinant to f is -1 and its common cofactor is 1.
    p_e, q_e = Q(1), Q(1)
    p_f, q_f, cofactor_f = Q(1), Q(0), Q(1)
    delta_ef = p_e * q_f - q_e * p_f
    require(delta_ef == -1 and q_e + delta_ef * cofactor_f == 0,
            "the sharp private-site identity guard changed")

    return {
        "pure_supports": [[list(pair) for pair in matching]
                          for matching in (m0, m1, m2)],
        "active_adjacent_pairs": [list(E), list(F)],
        "pure_coloops": {"colour_0": list(E), "colour_1": list(F)},
        "certified_deleted_star_ranks": {
            "e_both_endpoints": 2, "f_both_endpoints": 2,
        },
        "anchor_contained": True,
        "private_site_identity": "q_e + Delta_ef*C_f = 1-1 = 0",
        "distinct_centre_heads": True,
        "scope": (
            "exact matching-support and local private-site guard, not a "
            "complete GHZ source; it proves that a pure matroid augmenting "
            "path cannot eliminate the remaining coloop branch"
        ),
    }


def audit_balanced_zero_row_entry():
    """Land the balanced quotient by the mixed zero row, not by Laplace."""
    balanced = load(
        "computations/verify_h3_balanced_only_determinant_debt.py",
        "active_fan_balanced_only_debt",
    )
    balanced_ledger, balanced_digest = balanced.audit()
    require(balanced_digest
            == "1ba2fd09c0185a7cdfb96d348f33638cff6f0e5fd2c99e5dd988aff7b97bda50",
            "the balanced-only ledger changed")

    diagonal_matching = tuple(
        physical_edge for physical_edge in MATCHINGS[0]
        if WORD[physical_edge[0]] == WORD[physical_edge[1]]
    )
    # Do not depend on the recursion order of MATCHINGS: characterize the
    # unique matching all of whose decorated endpoint colours are diagonal.
    diagonal_matchings = tuple(
        matching for matching in MATCHINGS
        if all(WORD[left] == WORD[right] for left, right in matching)
    )
    require(diagonal_matchings == (((0, 1), (2, 3), (4, 5)),),
            "the unique diagonal matching changed")
    diagonal_matching = diagonal_matchings[0]

    balanced_cuts = tuple(tuple(cut)
                          for cut in balanced_ledger["balanced_cuts"])
    require(len(balanced_cuts) == 4, "the balanced cut count changed")
    for cut in balanced_cuts:
        left = set(cut)
        require(all((u in left) != (v in left)
                    for u, v in diagonal_matching),
                "the diagonal matching stopped crossing a balanced cut")

    # Freeze the exact balanced-only zero-row guard from aeb7e75.  It is not
    # a counterexample to transverse entry: ten of its cells are
    # offdiagonal.  No assertion is made that one of them is a Laplace
    # factor of the chosen balanced determinant.
    guard = balanced_ledger["rational_guard"]
    edge_values = {
        tuple(map(int, label)): Q(value)
        for label, value in zip(guard["edge_order"], guard["edge_values"],
                                strict=True)
    }
    offdiagonal_support = tuple(
        physical_edge for physical_edge in sorted(edge_values)
        if WORD[physical_edge[0]] != WORD[physical_edge[1]]
        and edge_values[physical_edge]
    )
    require(guard["hafnian"] == 0
            and guard["unbalanced_determinants"] == [0] * 6
            and guard["balanced_determinants"] == [3] * 4,
            "the balanced-only zero-row guard changed")
    require(offdiagonal_support == (
        (0, 2), (0, 3), (0, 4), (0, 5), (1, 4),
        (1, 5), (2, 4), (2, 5), (3, 4), (3, 5),
    ), "the balanced-only guard lost its offdiagonal entry")

    return {
        "balanced_determinant_covectors": 4,
        "balanced_quotient_dimension_mod_unbalanced":
            balanced_ledger["determinant_ranks"][
                "balanced_mod_unbalanced"],
        "unique_all_diagonal_matching": [list(pair)
                                          for pair in diagonal_matching],
        "zero_row_argument": (
            "if every offdiagonal cell of the 001122 row vanishes, its "
            "hafnian and each balanced cut determinant are, up to the "
            "determinant sign, the same diagonal product "
            "A01^00*A23^11*A45^22; hence H_001122=0 makes every balanced "
            "determinant zero"
        ),
        "exact_balanced_only_guard": {
            "hafnian": guard["hafnian"],
            "unbalanced_determinants": guard["unbalanced_determinants"],
            "balanced_determinants": guard["balanced_determinants"],
            "nonzero_offdiagonal_edges": [list(pair)
                                           for pair in offdiagonal_support],
        },
        "physical_consequence": (
            "a nonzero balanced determinant on an actual zero 001122 "
            "source row forces some nonzero offdiagonal cell somewhere in "
            "that row; the cell need not be a Laplace factor of the bright "
            "balanced determinant, and the target-augmented private-site "
            "identity supplies its source-provenant active fan"
        ),
    }


def audit_normalized_coloop_closures():
    hybrid = load(
        "computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py",
        "active_fan_target_coloop_hybrid",
    )
    punctured = load(
        "computations/verify_h3_c4_punctured_cube_alternate_target_lift.py",
        "active_fan_target_coloop_punctured",
    )
    double = load(
        "computations/verify_h3_order6_double_coloop_conjugate_hall_interference.py",
        "active_fan_target_double_coloop",
    )

    hybrid_result = hybrid.audit_hybrid_escape()
    require(sum(hybrid_result["residual_kind_histogram"].values()) == 110,
            "the normalized hybrid target-coloop closure changed")
    punctured_words = punctured.audit_words_and_routes()
    punctured_cube = punctured.audit_cube_identity()
    require(punctured_words["alternate_L_tail"] == ["04:11", "15:11"]
            and "A_z*F_t" in punctured_cube["source_certificate"],
            "the punctured-C4 alternate-target closure changed")
    double_result = double.audit()
    require(double_result["residual_packets"] == 270,
            "the normalized double-coloop closure changed")

    return {
        "hybrid_target_coloop_label_packets_closed": 110,
        "punctured_C4_outcome": (
            "alternate pure-one target matching or offanchor offdiagonal exit"
        ),
        "normalized_double_coloop_packets_closed":
            double_result["residual_packets"],
        "consequence": (
            "after the active fan coloop is placed in these source-labelled "
            "normal forms, C6/C8 and injective-five-lock are not independent "
            "residuals; the committed hybrid/cubical/conjugate rows route them"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "all_pure_support_families":
            audit_all_support_families_for_adjacent_pair(),
        "ternary_rank_alternative": audit_ternary_rank_alternative(),
        "sharp_adjacent_coloop_guard": audit_sharp_adjacent_coloop_guard(),
        "balanced_zero_row_entry": audit_balanced_zero_row_entry(),
        "normalized_coloop_closures": audit_normalized_coloop_closures(),
        "evaluated_determinant_consequence": (
            "an unbalanced nonzero evaluated determinant supplies a nonzero "
            "offdiagonal Laplace factor.  A balanced bright determinant on "
            "the actual zero mixed row supplies a nonzero offdiagonal row "
            "cell, though not necessarily a Laplace factor.  In either case "
            "the target-augmented private-site identity supplies a distinct-"
            "head active fan, and complete pure-support rank gives four-good "
            "or a literal pure-colour coloop on one fan edge, without "
            "simple-edge or anchor-escape hypotheses"
        ),
        "retired_residuals": (
            "non-simple ownership and whole-anchor containment do not remain "
            "rank obstructions.  An injective no-wedge five-lock can survive "
            "the complete-pure-support test only through a literal coloop"
        ),
        "first_remaining_theorem": (
            "active-fan coloop normalization: use complete mixed/response "
            "rows to place an arbitrary pure-colour coloop on a private-site "
            "fan into the committed normalized target-coloop or conjugate "
            "double-coloop packet, or produce an anchor-safe relation/free "
            "active carrier.  Pure matching matroids and the local private-"
            "site identity alone do not provide this source-labelled landing"
        ),
        "scope": (
            "exact uniform rank/matching-support theorem and exact replay of "
            "the h=3 normalized coloop closures.  No terminal comparison is "
            "used, and no arbitrary active fan is silently identified with "
            "an endpoint-affine target-coloop normal form"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"active-fan coloop ledger changed: {digest}")
    print("h3 active fan coloop-or-four-good: PASS")
    print("balanced zero-row determinant brightness enters the same fan")
    print("non-simple/anchor-contained selected-anchor branches retired")
    print("normalized target-coloop/double-coloop packets replayed")
    print("remaining: source-labelled active-fan coloop normalization")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
