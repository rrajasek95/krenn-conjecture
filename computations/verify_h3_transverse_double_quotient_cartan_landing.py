#!/usr/bin/env python3
"""Classify transverse Cartan landing at two deficient star quotients.

Let e=uv be a physical edge which occurs in exactly one of three selected
pure anchor matchings, say the colour-c matching.  Deleting e leaves rank
two at both endpoint stars, and both one-dimensional cokernels select the
same missing colour c.

This has a useful exact consequence.  Same-word rows are invisible in both
quotients.  A one-site Cartan/root move can be visible on only one side; a
single double-visible head must change both endpoint colours to c (or be a
pair of split one-site exits).  If the pure-c target has a nonzero matching
avoiding e, reselecting it removes e from the whole anchor union.  Every
private-site fan mate outside the new union then forms a four-good active
wedge with e.

Failure is also concrete.  Either e is a coloop of the literal pure-c
matching support, or every active mate is trapped in the reselected anchor
union.  The first branch has the pinned common-q E2 alternative; at h=3 its
only non-recombining topologies are one C6 or C8.  The second branch is the
injective, no-complementary-wedge five-lock/Hall residual.  Same-cell tails
cannot repair it because they preserve the wrong endpoint labels.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_balanced_anchor_chart_cover.py":
        "3f30d143f3f069f6123bfb41d7ae26833ef508c572c42e09544fe5d415f70d55",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "computations/verify_uniform_decorated_anchor_companion_rank_no_go.py":
        "a0b9a5a3e7c1a1809db4c42c49303c1c43db26229437fc58d93fea7c5d110063",
    "computations/verify_matching_interference_head_invariance_cartan_gate.py":
        "17b84de9c22247d617b9919fb5cf18593300226619945c7e6b5f5cef029ab787",
    "computations/verify_h3_axis_target_coloop_four_hole_exchange.py":
        "5283fae67a31ea3c9794fc8bbf351f7da5bc8251490dbdffbef04bde1f2a987f",
}
EXPECTED_LEDGER_SHA256 = "0e34137efe92c16ebba1b37202ebc446e1a30ee8bb3d81ef1ebcda9e28b103c9"


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


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))


def edge(left, right):
    return tuple(sorted((left, right)))


def simple_anchor_quotients_and_reselection(balanced, nonanchor):
    """Audit every rank-(2,2) selected edge on the 31 N=8 anchor types."""
    representatives = balanced.anchor_orbits()
    require(len(representatives) == 31,
            "the balanced anchor orbit census changed")

    simple_edges = 0
    same_word_dark_heads = 0
    one_root_exits = 0
    two_root_corners = 0
    reselections = 0
    fan_candidate_histogram = Counter()
    total_offanchor_fan_candidates = 0

    for triple in representatives:
        membership = {}
        for colour, matching in enumerate(triple):
            for pair in matching:
                membership.setdefault(pair, []).append(colour)

        for deleted, owners in membership.items():
            if len(owners) != 1:
                continue
            simple_edges += 1
            missing = owners[0]
            left, right = deleted

            # Since e is owned only by Q_c, deleting it retains exactly the
            # other two pure colour rows at both endpoints.  The two quotient
            # covectors are therefore both the coordinate c covector.
            for endpoint in deleted:
                surviving = {
                    colour for colour, matching in enumerate(triple)
                    if next(pair for pair in matching if endpoint in pair)
                    != deleted
                }
                require(surviving == set(range(3)) - {missing},
                        ("a simple anchor lost its common missing colour",
                         triple, deleted, endpoint, surviving, missing))

            dark_colours = tuple(value for value in range(3)
                                 if value != missing)
            for old_left, old_right in product(dark_colours, repeat=2):
                # Fixed-word heads are dark on both sides.  Each one-root
                # edge is split-visible, and their commuting corner is the
                # first single head pair visible in both quotient lines.
                require((old_left == missing, old_right == missing)
                        == (False, False), "a dark word became visible")
                require((missing == missing, old_right == missing)
                        == (True, False), "left root visibility changed")
                require((old_left == missing, missing == missing)
                        == (False, True), "right root visibility changed")
                require((missing == missing, missing == missing)
                        == (True, True), "two-root visibility changed")
                same_word_dark_heads += 1
                one_root_exits += 2
                two_root_corners += 1

            # If one literal pure-c matching avoids e, it can replace Q_c.
            # Then e is absent from all three anchors, so the pinned physical
            # nonanchor theorem makes its off-diagonal decorations good and
            # active.  Also count the possible fan mates outside the new
            # anchor union; source equations decide which are nonzero.
            for alternate in balanced.MATCHINGS:
                if deleted in alternate:
                    continue
                reselected = list(triple)
                reselected[missing] = alternate
                reselected = tuple(reselected)
                anchors = set().union(*(set(value) for value in reselected))
                require(deleted not in anchors,
                        "an avoiding pure reselection retained the deleted edge")
                for endpoint, other in ((left, right), (right, left)):
                    columns = nonanchor.endpoint_anchor_columns(
                        reselected, endpoint, other
                    )
                    require(len(set(columns)) == 3,
                            "pure reselection failed to repair a deleted star")

                outside_counts = []
                for centre, other in ((left, right), (right, left)):
                    fan_edges = tuple(edge(centre, site)
                                      for site in range(balanced.N)
                                      if site not in (centre, other))
                    outside = tuple(pair for pair in fan_edges
                                    if pair not in anchors)
                    require(len(outside) >= 3,
                            "a reselected endpoint lost all offanchor fan mates")
                    outside_counts.append(len(outside))
                fan_candidate_histogram[tuple(outside_counts)] += 1
                total_offanchor_fan_candidates += sum(outside_counts)
                reselections += 1

    require(simple_edges == 249
            and same_word_dark_heads == 996
            and one_root_exits == 1992
            and two_root_corners == 996,
            "the simple-anchor/root-head census changed")
    require(reselections == 22410
            and total_offanchor_fan_candidates == 155700,
            "the pure-reselection/fan census changed")
    expected_histogram = Counter({
        (3, 3): 7497, (4, 3): 5295, (4, 4): 4248,
        (3, 4): 4173, (5, 4): 444, (4, 5): 312,
        (5, 3): 288, (3, 5): 90, (5, 5): 63,
    })
    require(fan_candidate_histogram == expected_histogram,
            ("the reselected fan histogram changed", fan_candidate_histogram))
    return {
        "anchor_orbits_mod_S8xS3": len(representatives),
        "simple_anchor_edges": simple_edges,
        "quotient_lines": (
            "both endpoint cokernels are the coordinate line of the unique "
            "pure colour c whose selected matching contains e"
        ),
        "same_word_double_dark_head_pairs": same_word_dark_heads,
        "one_site_root_exits_split_visible": one_root_exits,
        "two_site_root_corners_double_visible": two_root_corners,
        "one_site_root_can_be_double_visible": False,
        "avoiding_pure_matching_reselections": reselections,
        "minimum_offanchor_fan_mates_per_endpoint_after_reselection": 3,
        "offanchor_fan_mate_histogram": [
            [list(key), value]
            for key, value in sorted(fan_candidate_histogram.items())
        ],
        "offanchor_fan_mate_candidates_total":
            total_offanchor_fan_candidates,
        "physical_consequence": (
            "a nonzero pure-c matching avoiding e reselects Q_c and makes e "
            "absent from the anchor union; any nonzero private-site fan mate "
            "among the audited outside candidates gives a four-good active "
            "wedge with e"
        ),
    }


def source_and_residual_interfaces(head_gate, private_site, bidirectional,
                                   five_lock, companion, four_hole):
    fixed = head_gate.audit_fixed_word_head_invariance()
    changes = head_gate.audit_word_change_transversality()
    require(fixed["site_matching_occurrences"] == 3 ** 8 * 105 * 8,
            "the fixed-word head census changed")
    require(changes["local_head_rank"] == 2,
            "the one-site root quotient changed")

    private_core = private_site.load(
        "computations/verify_hafnian_private_site_matching_bijection_lemma.py",
        "double_quotient_private_core",
    )
    identities = bidirectional.audit_source_identities(
        private_site, private_core
    )
    typing = bidirectional.audit_bidirectional_typing()
    require(typing["type_count"] == 6,
            "the bidirectional private-site types changed")

    lock_kernel = five_lock.audit_lock_kernel_theorem()
    crossed = five_lock.audit_crossed_wedge_landing()
    sharp = five_lock.audit_sharp_incidence_counterguard()
    require(crossed["landing"] == "distinct-head four-good active overlap"
            and sharp["simultaneous_kernel"] == 0
            and not sharp["complementary_crossed_wedge"],
            "the sharp Hall/five-lock residual changed")

    labels = companion.audit_label_invariance()
    require(labels["audited_avoiding_matchings"] == 216,
            "same-cell label invariance changed")

    e2 = four_hole.audit_e2_target_coloop_dichotomy()
    topology = four_hole.audit_tail_topology()
    require(topology["full_cycle_histogram"]
            == {"(6,)": 1, "(8,)": 6, "(4, 4)": 2}
            and topology["union_matching_count_histogram"] == {2: 7, 4: 2},
            "the target-coloop four-hole topology changed")

    return {
        "fixed_word_head_invariance": {
            "site_matching_occurrences": fixed["site_matching_occurrences"],
            "same_word_transverse_quotient": 0,
        },
        "bidirectional_private_site": {
            "offdiagonal_types": typing["type_count"],
            "first_identity": identities["first_fan"][
                "exact_source_consequence"],
            "transposed_identity": identities["transposed_fan"][
                "exact_source_consequence"],
            "role": (
                "once a root exit supplies the missing head, the two exact "
                "fans supply active physical mates at the two endpoints"
            ),
        },
        "pure_target_coloop_exchange": {
            "E2_dichotomy": e2["dichotomy"],
            "four_hole_cycle_histogram": topology["full_cycle_histogram"],
            "recombining_C4_plus_C4_cases": 2,
            "single_even_cycle_cases": 7,
        },
        "five_lock_Hall_split": {
            "kernel_audits": len(lock_kernel),
            "complementary_wedge": crossed["landing"],
            "sharp_residual": (
                "injective same-star five-lock and no complementary crossed "
                "offanchor wedge"
            ),
        },
        "same_cell_companion_guard": labels["invariant"],
    }


def main():
    pin_dependencies()
    balanced = load(
        "computations/verify_n8_balanced_anchor_chart_cover.py",
        "double_quotient_balanced",
    )
    nonanchor = load(
        "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py",
        "double_quotient_nonanchor",
    )
    private_site = load(
        "computations/verify_uniform_target_augmented_private_site_active_minor.py",
        "double_quotient_private_site",
    )
    bidirectional = load(
        "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py",
        "double_quotient_bidirectional",
    )
    five_lock = load(
        "computations/verify_uniform_five_lock_wedge_or_switch.py",
        "double_quotient_five_lock",
    )
    companion = load(
        "computations/verify_uniform_decorated_anchor_companion_rank_no_go.py",
        "double_quotient_companion",
    )
    head_gate = load(
        "computations/verify_matching_interference_head_invariance_cartan_gate.py",
        "double_quotient_head_gate",
    )
    four_hole = load(
        "computations/verify_h3_axis_target_coloop_four_hole_exchange.py",
        "double_quotient_four_hole",
    )

    ledger = {
        "theorem": "transverse double-quotient Cartan landing classification",
        "selected_anchor_quotients":
            simple_anchor_quotients_and_reselection(balanced, nonanchor),
        "source_and_residual_interfaces": source_and_residual_interfaces(
            head_gate, private_site, bidirectional, five_lock, companion,
            four_hole,
        ),
        "exact_landing_alternative": (
            "at a rank-(2,2) selected edge e with missing colour c, a "
            "Cartan head is visible in both quotient lines exactly when its "
            "endpoint heads both have nonzero c-coordinate.  Same-word and "
            "one-root exits cannot do this; a two-root corner or two split "
            "exits can.  A nonzero pure-c matching avoiding e reselects the "
            "anchor, and any active fan mate outside the new anchor union "
            "gives a distinct-head four-good active wedge"
        ),
        "smallest_exact_residual": (
            "e is a literal pure-c target coloop, or after every available "
            "pure-c reselection all nonzero bidirectional fan mates remain "
            "anchor-contained.  Common-q E2 then gives an alternate target "
            "or a physical exchange carrier.  The exact surviving branches "
            "are: an anchor-contained single-C6/C8 E2 carrier in the coloop "
            "case, or an injective five-lock with no complementary offanchor "
            "wedge in the bidirectional Hall case.  Identifying these two "
            "branches requires additional carrier typing and is not assumed"
        ),
        "excluded_shortcuts": (
            "same-word matching interference and further tails of one fixed "
            "decorated cell preserve endpoint heads and cannot fill the "
            "opposite quotient line"
        ),
        "scope": (
            "exact quotient and selected-anchor geometry on all 31 N=8 "
            "anchor types, uniform head/private-site identities, and the "
            "complete h=3 four-hole topology.  Activity support in the final "
            "anchor-contained C6/C8 Hall web is not asserted"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("double-quotient ledger changed", digest))

    print("h3 transverse double-quotient Cartan landing: CLASSIFIED")
    print("simple selected edges: 249; both quotients miss the same colour")
    print("one-root exits: split-visible only; two-root corner: double-visible")
    print("avoiding pure reselections: 22410; >=3 offanchor mates per endpoint")
    print("residual: coloop C6/C8 carrier or injective no-wedge Hall web")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
