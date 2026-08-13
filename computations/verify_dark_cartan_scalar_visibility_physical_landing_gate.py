#!/usr/bin/env python3
"""Turn dark-Cartan scalar visibility into an exact physical landing gate.

Assume the complete equality JG=JC*y and that G is visible in both deficient
endpoint quotient lines.  The scalar expansion contains one double-visible
column or two split-visible columns.  Locality classifies the first as the
diagonal cc cell on the selected edge; it supplies rank but not activity.
Split visibility likewise does not imply off-anchor incidence, offdiagonal
typing, a common crossed centre, or nonzero cofactors.  With those extra
physical data the pinned crossed-wedge theorem lands.  Without them the
sharp residual is exactly the existing pure-c coloop or injective no-wedge
five-lock branch.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_dark_cartan_terminal_safe_cancellation.py":
        "124963d21d779920322fcfc3d238351ce204093cc2587d1bba199ebc85b650d4",
    "computations/verify_h3_transverse_double_quotient_cartan_landing.py":
        "e2b536a2cc8e20883208dc098c84c6dabe15c5c01777f6018a8b72981274b5ae",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "computations/verify_h3_axis_target_coloop_four_hole_exchange.py":
        "5283fae67a31ea3c9794fc8bbf351f7da5bc8251490dbdffbef04bde1f2a987f",
}
EXPECTED_LEDGER_SHA256 = (
    "e00c992ff68837327c9d6d2dc77daadbd2b65e670f086aebe0a6e415f7c47418"
)

N = 8
COLOURS = tuple(range(3))
U, V, MISSING = 0, 1, 0
SELECTED_EDGE = (U, V)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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


def normalize_cell(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def local_colour(cell, site):
    left, right, left_colour, right_colour = cell
    if site == left:
        return left_colour
    if site == right:
        return right_colour
    return None


def visibility(cell):
    return (
        local_colour(cell, U) == MISSING,
        local_colour(cell, V) == MISSING,
    )


def canonical_anchor_reselection(five_lock):
    triple = tuple(five_lock.PURE_MATCHINGS[colour]
                   for colour in COLOURS)
    owners = tuple(colour for colour, matching in enumerate(triple)
                   if SELECTED_EDGE in matching)
    require(owners == (MISSING,),
            "the canonical selected edge lost its unique pure owner")
    alternate = next(matching for matching in perfect_matchings(range(N))
                     if SELECTED_EDGE not in matching)
    reselected = list(triple)
    reselected[MISSING] = alternate
    reselected = tuple(reselected)
    anchors = frozenset(pair for matching in reselected for pair in matching)
    require(SELECTED_EDGE not in anchors,
            "the pure-c avoiding reselection retained the selected edge")
    return triple, reselected, anchors, alternate


def audit_local_visibility_classification():
    cells = tuple(normalize_cell(left, right, a, b)
                  for left, right in combinations(range(N), 2)
                  for a, b in product(COLOURS, repeat=2))
    double = tuple(cell for cell in cells if visibility(cell) == (True, True))
    split_u = tuple(cell for cell in cells if visibility(cell) == (True, False))
    split_v = tuple(cell for cell in cells if visibility(cell) == (False, True))
    require(double == ((U, V, MISSING, MISSING),),
            ("double-visible locality classification changed", double))
    require(split_u and split_v,
            "the split-visible physical classes disappeared")

    double_cell = double[0]
    require(double_cell[:2] == SELECTED_EDGE
            and double_cell[2] == double_cell[3],
            "the double-visible cell stopped being diagonal on e")
    return {
        "physical_decorated_cells": len(cells),
        "double_visible_cells": len(double),
        "unique_double_visible_cell": list(double_cell),
        "u_only_visible_cells": len(split_u),
        "v_only_visible_cells": len(split_v),
        "locality_theorem": (
            "one scalar column visible in both endpoint quotients must be "
            "supported on e=uv and have endpoint heads (c,c)"
        ),
        "activity_guard": (
            "the unique double-visible scalar is diagonal; the target-"
            "augmented offdiagonal identity does not make it active"
        ),
    }


def audit_reselection_rank_and_typing(five_lock, nonanchor, private):
    _old, reselected, anchors, alternate = canonical_anchor_reselection(
        five_lock)
    left_columns = nonanchor.endpoint_anchor_columns(reselected, U, V)
    right_columns = nonanchor.endpoint_anchor_columns(reselected, V, U)
    require(len(set(left_columns)) == len(set(right_columns)) == 3,
            "pure-c reselection failed to repair the selected endpoint stars")

    # A diagonal cc cell on e is now off-anchor and double-visible, but the
    # activity identity has the explicit hypothesis b != a.  The marked
    # critical occurrence is offdiagonal, so it *does* force some active
    # determinant/cofactor mate; incidence decides whether that mate escapes.
    double_cell = normalize_cell(U, V, MISSING, MISSING)
    marked_offdiagonal = normalize_cell(U, V, 1, 2)
    require(edge(*double_cell[:2]) not in anchors
            and double_cell[2] == double_cell[3],
            "the double-visible diagonal guard changed")
    require(marked_offdiagonal[2] != marked_offdiagonal[3]
            and edge(*marked_offdiagonal[:2]) not in anchors,
            "the marked offdiagonal carrier failed to become nonanchor")

    private_core = private.load(
        "computations/verify_hafnian_private_site_matching_bijection_lemma.py",
        "dark_scalar_landing_private_core",
    )
    active_identity = private.target_augmented_identity(private_core, N)
    require(active_identity["exact_source_consequence"]
            == "sum_s Delta_us*C_s=-q_u",
            "the offdiagonal active identity changed")

    outside_u = tuple(edge(U, site) for site in range(N)
                      if site not in SELECTED_EDGE
                      and edge(U, site) not in anchors)
    outside_v = tuple(edge(V, site) for site in range(N)
                      if site not in SELECTED_EDGE
                      and edge(V, site) not in anchors)
    require(len(outside_u) >= 3 and len(outside_v) >= 3,
            "the reselected anchor lost its outside fan choices")
    return {
        "avoiding_pure_c_matching": [list(pair) for pair in alternate],
        "selected_edge_absent_from_reselected_anchor_union": True,
        "deleted_star_ranks_at_e": [3, 3],
        "double_visible_cc_cell": {
            "cell": list(double_cell),
            "off_anchor": True,
            "offdiagonal": False,
            "activity_forced": False,
        },
        "marked_offdiagonal_cell": {
            "cell": list(marked_offdiagonal),
            "off_anchor": True,
            "two_endpoint_rank_good": True,
            "some_active_determinant_cofactor_forced": True,
        },
        "outside_fan_candidates": [len(outside_u), len(outside_v)],
        "positive_double_column_criterion": (
            "the double-visible cc column supplies no second physical pair.  "
            "Landing occurs only if an active mate forced by the marked "
            "offdiagonal e-cell lies outside the reselected anchor union"
        ),
    }


def audit_split_visibility_guards(five_lock):
    _old, _reselected, anchors, alternate = canonical_anchor_reselection(
        five_lock)
    # Choose the pure-c alternate edge at each deficient endpoint.  Because
    # the alternate is a selected nonzero pure-c matching monomial, its cc
    # cells are genuinely occupied scalar columns, not merely available
    # coordinate types.  They are split-visible and anchor-contained.
    anchor_u = next(pair for pair in alternate if U in pair)
    anchor_v = next(pair for pair in alternate if V in pair)
    other_u = next(site for site in anchor_u if site != U)
    other_v = next(site for site in anchor_v if site != V)
    cell_u = normalize_cell(U, other_u, MISSING, MISSING)
    cell_v = normalize_cell(V, other_v, MISSING, MISSING)
    require(visibility(cell_u) == (True, False)
            and visibility(cell_v) == (False, True),
            "the anchor-contained split visibility guard changed")
    require(edge(*cell_u[:2]) in anchors and edge(*cell_v[:2]) in anchors,
            "the split guard unexpectedly escaped the anchor union")
    require(cell_u[2] == cell_u[3] and cell_v[2] == cell_v[3],
            "the split guard stopped being diagonal/inactivity-compatible")

    # A second exact guard keeps both split columns on e with opposite dark
    # endpoint heads.  They repair the two quotient lines separately but
    # still provide only one physical pair, hence not a four-good wedge.
    same_pair_u = normalize_cell(U, V, MISSING, 1)
    same_pair_v = normalize_cell(U, V, 1, MISSING)
    require(visibility(same_pair_u) == (True, False)
            and visibility(same_pair_v) == (False, True)
            and same_pair_u[:2] == same_pair_v[:2] == SELECTED_EDGE,
            "the same-pair split guard changed")

    return {
        "anchor_contained_split_guard": {
            "u_cell": list(cell_u),
            "v_cell": list(cell_v),
            "occupied_in_selected_pure_c_matching": True,
            "both_visible_in_required_split": True,
            "both_physical_pairs_off_anchor": False,
            "activity_forced_by_offdiagonal_identity": False,
        },
        "same_pair_split_guard": {
            "u_cell": list(same_pair_u),
            "v_cell": list(same_pair_v),
            "distinct_physical_pairs": False,
            "four_good_wedge": False,
        },
        "positive_split_criterion": [
            "two distinct physical pairs after fine-label aggregation",
            "both pairs outside the reselected anchor union",
            "a common crossed centre with distinct centre heads",
            "nonzero cofactor witnesses on both crossed components",
        ],
        "conclusion": (
            "two split-visible occupied scalar columns do not imply an "
            "active wedge until support, anchor, head, and cofactor typing "
            "are all retained"
        ),
    }


def audit_positive_and_residual_interfaces(dark, five_lock, four_hole):
    dark_ledger, dark_digest = dark.audit()
    require(dark_digest == dark.EXPECTED_LEDGER_SHA256,
            "terminal-safe dark cancellation ledger changed")
    require(dark_ledger["rank_consequence"].endswith(
                "two split-visible scalar columns"),
            "the scalar visibility alternative changed")

    # Smallest exact augmented equalities for the two visibility patterns.
    # The physical cell labels are supplied by the locality audits above;
    # these two matrices prove that complete equality and terminal darkness
    # impose no further activity or incidence condition.
    double_equality = dark.audit_instance(
        columns_c=((1, 1),),
        y=(1,),
        terminal_c=(0,),
        terminal_g=0,
        quotient_u=(1, 0),
        quotient_v=(0, 1),
    )
    split_equality = dark.audit_instance(
        columns_c=((1, 0), (0, 1)),
        y=(1, 1),
        terminal_c=(0, 0),
        terminal_g=0,
        quotient_u=(1, 0),
        quotient_v=(0, 1),
    )
    require(double_equality["double_visible_scalar_columns"] == [0]
            and double_equality["terminal_on_dark_kernel"] == "0",
            "the one-column complete-equality guard changed")
    require(not split_equality["double_visible_scalar_columns"]
            and split_equality["u_visible_scalar_columns"] == [0]
            and split_equality["v_visible_scalar_columns"] == [1]
            and split_equality["terminal_on_dark_kernel"] == "0",
            "the two-column complete-equality guard changed")

    crossed = five_lock.audit_crossed_wedge_landing()
    sharp = five_lock.audit_sharp_incidence_counterguard()
    kernels = five_lock.audit_lock_kernel_theorem()
    require(crossed["landing"]
            == "distinct-head four-good active overlap",
            "the positive crossed-wedge landing changed")
    require(not sharp["complementary_crossed_wedge"]
            and sharp["simultaneous_kernel"] == 0,
            "the injective no-wedge residual changed")

    e2 = four_hole.audit_e2_target_coloop_dichotomy()
    topology = four_hole.audit_tail_topology()
    require(topology["full_cycle_histogram"]
            == {"(6,)": 1, "(8,)": 6, "(4, 4)": 2},
            "the coloop carrier topology changed")
    return {
        "complete_dark_equality": "JG=JC*y",
        "visibility_alternative": (
            "one double-visible occupied scalar column or two split-visible "
            "occupied scalar columns"
        ),
        "smallest_complete_equality_guards": {
            "one_double": {
                "JC": [[1, 1]],
                "y": [1],
                "JG": [1, 1],
                "physical_label": "occupied diagonal A_uv^(c,c)",
                "activity_forced": False,
            },
            "two_split": {
                "JC": [[1, 0], [0, 1]],
                "y": [1, 1],
                "JG": [1, 1],
                "physical_labels": (
                    "occupied pure-c cells at u and v in the selected "
                    "avoiding matching"
                ),
                "off_anchor_wedge_forced": False,
            },
            "scope": (
                "exact augmented local quotient modules with physical cell "
                "labels, not standalone complete GHZ source packets"
            ),
        },
        "positive_crossed_wedge": crossed,
        "five_lock_kernel_branch": (
            "a noninjective same-star lock supplies an exact simultaneous "
            "anchor-safe switch"
        ),
        "five_lock_kernel_audits": len(kernels),
        "sharp_no_wedge_residual": sharp,
        "pure_c_coloop": {
            "E2_dichotomy": e2["dichotomy"],
            "single_cycle_carriers": {"C6": 1, "C8": 6},
            "recombining_C4_plus_C4": 2,
        },
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    dark = load(
        "computations/verify_dark_cartan_terminal_safe_cancellation.py",
        "dark_scalar_landing_cancellation",
    )
    nonanchor = load(
        "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py",
        "dark_scalar_landing_nonanchor",
    )
    private = load(
        "computations/verify_uniform_target_augmented_private_site_active_minor.py",
        "dark_scalar_landing_private",
    )
    five_lock = load(
        "computations/verify_uniform_five_lock_wedge_or_switch.py",
        "dark_scalar_landing_five_lock",
    )
    four_hole = load(
        "computations/verify_h3_axis_target_coloop_four_hole_exchange.py",
        "dark_scalar_landing_four_hole",
    )
    ledger = {
        "theorem": "dark Cartan scalar-visibility physical landing gate",
        "pinned_commits": ["00db7ee", "ea8c864", "605f625"],
        "local_visibility": audit_local_visibility_classification(),
        "pure_c_reselection": audit_reselection_rank_and_typing(
            five_lock, nonanchor, private),
        "split_visibility": audit_split_visibility_guards(five_lock),
        "positive_and_residual_interfaces":
            audit_positive_and_residual_interfaces(
                dark, five_lock, four_hole),
        "exact_landing_theorem": (
            "after a nonzero pure-c avoiding reselection, the marked "
            "offdiagonal e-cell has rank-(3,3) and forces an active fan.  If "
            "one forced active mate escapes the anchor union, e and that mate "
            "give four-good active rank.  Two scalar exits land directly only "
            "when they form the pinned off-anchor, distinct-head, cofactor-"
            "nonzero crossed wedge"
        ),
        "visibility_no_go": (
            "one double-visible scalar is the diagonal cc cell on e and does "
            "not force activity; two split-visible scalars can be diagonal, "
            "anchor-contained, or supported on the same physical pair.  "
            "Visibility alone therefore does not imply four-good activity"
        ),
        "smallest_exact_residual": (
            "either e is a literal pure-c target coloop, leaving the "
            "anchor-contained single-C6/C8 E2 carrier, or an avoiding "
            "reselection exists but every nonzero active mate remains "
            "anchor-contained and the same-star five-lock is injective with "
            "no complementary crossed off-anchor wedge"
        ),
        "scope": (
            "exact locality, rank, anchor-incidence, offdiagonal-activity, "
            "crossed-wedge, and h=3 coloop guards.  No activity conclusion is "
            "drawn from quotient visibility without a nonzero cofactor witness"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("dark scalar physical landing ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("dark Cartan scalar visibility -> physical landing: SHARP GUARD")
    print("one double-visible scalar: diagonal cc on e; activity not forced")
    print("two split-visible scalars: support/head/cofactor typing required")
    print("positive: escaping active fan or crossed off-anchor wedge")
    print("residual: pure-c coloop C6/C8 or injective no-wedge five-lock")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
