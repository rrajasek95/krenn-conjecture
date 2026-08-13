#!/usr/bin/env python3
"""Complete-row audit of the two sharp active-coloop Hall traps.

The recurrence boundary in 5ddaa7e exhibited a closed endpoint triangle and
a nine-edge/singleton shore using only the first mixed unary coefficient
000011.  This checker appends the other two nonzero mixed unary coefficients
of the literal two-occurrence guard, exhausts their matching mates, and then
scans every unary and four response word on the resulting support packets.

The triangle is eliminated.  Of 14^3 simultaneous unary-mate choices, 728
already break the pure-zero coloop and 288 put a new occurrence directly in
the selected pure-one target response row.  The remaining 1728 all-offdiagonal
choices have only 148 closed-shore shadows, each a unique nine-edge/singleton
concept.  Every one of those 148 shadows leaves the same three complete R11
mixed coefficients private.  Hence a full GHZ source must add a response mate;
the exact structural alternatives are recorded below.  This is an exact
complete-row reduction, not a claim that the added mate has already landed in
the final transverse/terminal theorem.
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
    "computations/verify_h3_active_coloop_forced_mate_recurrence_potential_boundary.py":
        "f08e9bc7e7a2a6d561426890c60120b96b37334fb54337d06845fe78d3ffe984",
    "notes/h3-active-coloop-forced-mate-recurrence-potential-boundary.md":
        "3a6823f8b5e8d555883ecbb188137a8d6ec54351d54292ccd06ede3035c4f3aa",
    "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py":
        "f35618988f591a28fd2a6574977c058aa2bec83a2cacfeb9e7567873e0b61d1c",
    "notes/h3-coloop-two-occurrence-complete-response-first-mixed-unary-gate.md":
        "94ffe3523f27aebb1064f2778b9a2a6fe99835ad98fc59b6a28dd57b6d9e9fa6",
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "35658ebed521b93387fc00aa7d2600d703f57b3e5e5deca67a11a1ab155d6c56",
    "notes/h3-active-fan-coloop-saturation-boundary.md":
        "4431948d139c45f8619928878b0dde0cba39ddc9a0942bd6a899bd9d53daa1d6",
}
EXPECTED_LEDGER_SHA256 = "a9e19c224d7f6bd847ab964d30bec36da3a6cfaede72e8f9f301fb44fa9e0cec"

SITES = tuple(range(6))
COLOURS = tuple(range(3))
SELECTED = ((0, 1), (2, 3), (4, 5))
COLOOP = (0, 1)
MIXED_WORDS = (
    (0, 0, 0, 0, 1, 1),
    (0, 0, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 1),
)
CLOSURES = frozenset(((0, 1), (0, 4), (1, 4)))


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


def edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def q_label(left: int, right: int, left_colour: int, right_colour: int):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return (left, right, left_colour, right_colour)


def decorated(matching, word):
    return tuple(q_label(left, right, word[left], word[right])
                 for left, right in matching)


def word_label(word) -> str:
    return "".join(map(str, word))


def closed_concepts(saturation):
    concepts = set()
    for mask in range(1, saturation.FULL_MASK + 1):
        mate = saturation.transversal(mask)
        if mate:
            concepts.add((saturation.transversal(mate), mate))
    require(len(concepts) == 446,
            "the closed ordered Hall-concept count changed")
    return tuple(sorted(concepts))


def mask_edges(saturation, mask):
    return frozenset(tuple(value) for value in saturation.mask_edges(mask))


def alternate_records(first, word):
    records = []
    for matching in first.MATCHINGS6:
        if matching == SELECTED:
            continue
        cells = decorated(matching, word)
        cross_edges = frozenset(
            physical for physical in matching
            if word[physical[0]] != word[physical[1]]
        )
        closures = frozenset(physical for physical in matching
                             if physical in CLOSURES)
        records.append({
            "matching": matching,
            "cells": cells,
            "cross_edges": cross_edges,
            "closures": closures,
            "diagonal": not cross_edges,
        })
    require(len(records) == 14, "an alternate packet changed size")
    require(sum(record["diagonal"] for record in records) == 2,
            ("a mixed word lost its two diagonal mates", word))
    return tuple(records)


def certified_edges(records):
    answer = set()
    for record in records:
        answer.update(record["cross_edges"])
        # A closure is certified only because the literal guard already has
        # the corresponding nonzero p1/s1 endpoint pair.  Keeping it separate
        # from cross q support is essential to the source typing.
        answer.update(record["closures"])
    return frozenset(answer)


def audit_three_unary_packets(first, saturation):
    packets = tuple(alternate_records(first, word) for word in MIXED_WORDS)
    concepts = closed_concepts(saturation)
    triangle = frozenset(CLOSURES)

    stages = Counter()
    trapped = []
    for records in product(*packets):
        first_record, second_record, third_record = records
        if first_record["diagonal"] or second_record["diagonal"]:
            stages["pure_zero_coloop_escape"] += 1
            continue
        if third_record["diagonal"]:
            # The word 001111 has 01 as its unique zero-zero edge.  Deleting
            # that closure and using p1[0,1]s1[1,1] turns either diagonal mate
            # into a literal extra R11[111111] target occurrence.
            require(COLOOP in third_record["matching"],
                    "the 001111 diagonal mate lost the coloop edge")
            stages["pure_one_target_response_occurrence"] += 1
            continue

        stages["all_three_offdiagonal"] += 1
        edges = certified_edges(records)
        fits = tuple((left, right) for left, right in concepts
                     if edges <= mask_edges(saturation, left))
        if not fits:
            stages["strict_outside_closed_shore"] += 1
            continue
        require(len(fits) == 1,
                ("a trapped packet stopped having a unique concept", edges, fits))
        left, right = fits[0]
        left_edges = mask_edges(saturation, left)
        right_edges = mask_edges(saturation, right)
        require(len(left_edges) == 9 and len(right_edges) == 1,
                ("a triangle or non-singleton trap survived", left_edges,
                 right_edges))
        trapped.append({
            "records": records,
            "certified_edges": edges,
            "shore": left_edges,
            "dual": next(iter(right_edges)),
        })

    require(stages == Counter({
        "pure_zero_coloop_escape": 728,
        "pure_one_target_response_occurrence": 288,
        "all_three_offdiagonal": 1728,
        "strict_outside_closed_shore": 1580,
    }), ("the three-word stage census changed", stages))
    require(len(trapped) == 148, "the final trapped support count changed")
    duals = Counter(item["dual"] for item in trapped)
    expected_duals = Counter({
        (0, 1): 48,
        (0, 4): 18, (1, 4): 18,
        (0, 2): 12, (0, 3): 12, (1, 2): 12, (1, 3): 12,
        (2, 4): 8, (3, 4): 8,
    })
    require(duals == expected_duals,
            ("the nine-edge dual histogram changed", duals))
    return packets, trapped, {
        "simultaneous_mate_choices": 14 ** 3,
        "pure_zero_coloop_escapes": stages["pure_zero_coloop_escape"],
        "new_pure_one_target_response_occurrences":
            stages["pure_one_target_response_occurrence"],
        "all_three_offdiagonal": stages["all_three_offdiagonal"],
        "offdiagonal_with_strict_outside_shore_growth":
            stages["strict_outside_closed_shore"],
        "trapped_closed_shore_packets": len(trapped),
        "triangle_survivors": 0,
        "surviving_concept_type": "nine-edge/singleton only",
        "dual_singleton_histogram": {
            repr(key): value for key, value in sorted(duals.items())
        },
    }


def response_occurrences(first, head_p, head_s, word, p_support, s_support,
                         q_support):
    occurrences = []
    for p_site in SITES:
        if (head_p, p_site, word[p_site]) not in p_support:
            continue
        for s_site in SITES:
            if (p_site == s_site
                    or (head_s, s_site, word[s_site]) not in s_support):
                continue
            remaining = tuple(site for site in SITES
                              if site not in (p_site, s_site))
            for matching in first.perfect_matchings(remaining):
                cells = decorated(matching, word)
                if all(cell in q_support for cell in cells):
                    occurrences.append((p_site, s_site, matching))
    return tuple(occurrences)


def unary_occurrences(first, word, q_support):
    return tuple(matching for matching in first.MATCHINGS6
                 if all(cell in q_support for cell in decorated(matching, word)))


def private_zero_rows(first, p_support, s_support, q_support):
    rows = []
    for word in product(COLOURS, repeat=6):
        unary = unary_occurrences(first, word, q_support)
        # Every nonconstant GHZ word has zero target.  We still compute the
        # three constant words, but do not infer a private-zero obligation
        # without selecting their target head/normalization.
        mixed = len(set(word)) != 1
        if mixed and len(unary) == 1:
            rows.append(("U", word, unary[0]))
        for head_p in (0, 1):
            for head_s in (0, 1):
                occurrences = response_occurrences(
                    first, head_p, head_s, word,
                    p_support, s_support, q_support,
                )
                if mixed and len(occurrences) == 1:
                    rows.append((f"R{head_p + 1}{head_s + 1}",
                                 word, occurrences[0]))
    return tuple(rows)


def row_key(row):
    return row[0] + "[" + word_label(row[1]) + "]"


def audit_complete_row_scan(first, trapped):
    p_values, s_values, base_q_values = first.literal_guard_values()
    p_support = frozenset(p_values)
    s_support = frozenset(s_values)
    private_packets = []
    count_histogram = Counter()
    for item in trapped:
        q_support = set(base_q_values)
        for record in item["records"]:
            q_support.update(record["cells"])
        private = private_zero_rows(
            first, p_support, s_support, frozenset(q_support)
        )
        require(private, "a trapped support acquired no private complete row")
        private_packets.append(private)
        count_histogram[len(private)] += 1

    universal = set(map(row_key, private_packets[0]))
    for packet in private_packets[1:]:
        universal.intersection_update(map(row_key, packet))
    expected = {
        "R11[110000]",
        "R11[110011]",
        "R11[111100]",
    }
    require(universal == expected,
            ("the universal private complete rows changed", universal))
    expected_histogram = Counter({
        4: 4, 5: 7, 6: 14, 7: 26, 8: 9, 9: 4, 10: 8,
        11: 19, 12: 5, 13: 2, 14: 8, 15: 9, 16: 9, 17: 9,
        18: 7, 19: 6, 20: 2,
    })
    require(count_histogram == expected_histogram,
            ("the private-row histogram changed", count_histogram))
    return {
        "rows_scanned_per_support": 729 * 5,
        "mixed_zero_target_rows_used_for_private_obligations": 726 * 5,
        "private_zero_row_count_range": [
            min(count_histogram), max(count_histogram)
        ],
        "private_row_count_histogram": {
            str(key): value for key, value in sorted(count_histogram.items())
        },
        "universal_private_rows": sorted(universal),
        "logical_effect": (
            "each displayed coefficient currently has exactly one nonzero "
            "source occurrence and zero target; a complete GHZ source must "
            "add an alternate response occurrence in all three rows"
        ),
    }


def structural_response_occurrences(first, word):
    p_values, s_values, _q_values = first.literal_guard_values()
    occurrences = []
    for p_site in SITES:
        if (0, p_site, word[p_site]) not in p_values:
            continue
        for s_site in SITES:
            if (p_site == s_site or (0, s_site, word[s_site]) not in s_values):
                continue
            remaining = tuple(site for site in SITES
                              if site not in (p_site, s_site))
            for matching in first.perfect_matchings(remaining):
                occurrences.append((p_site, s_site, matching,
                                    decorated(matching, word)))
    return tuple(occurrences)


def occurrence_label(record):
    p_site, s_site, matching, _cells = record
    return f"P{p_site}S{s_site}:" + "|".join(
        f"{left}{right}" for left, right in matching
    )


def audit_forced_response_seed(first):
    words = {
        "110000": (1, 1, 0, 0, 0, 0),
        "110011": (1, 1, 0, 0, 1, 1),
        "111100": (1, 1, 1, 1, 0, 0),
    }
    selected = {
        "110000": "P0S1:23|45",
        "110011": "P0S1:23|45",
        "111100": "P0S1:23|45",
    }
    alternatives = {}
    classes = {}
    for label, word in words.items():
        records = structural_response_occurrences(first, word)
        labels = tuple(occurrence_label(record) for record in records)
        require(selected[label] in labels,
                ("a universal private occurrence disappeared", label, labels))
        alternates = tuple(record for record in records
                           if occurrence_label(record) != selected[label])
        alternatives[label] = [occurrence_label(record) for record in alternates]
        counts = Counter()
        for p_site, s_site, _matching, cells in alternates:
            cross = sum(left_colour != right_colour
                        for _left, _right, left_colour, right_colour in cells)
            if (p_site, s_site) != (0, 1):
                counts["changed_endpoint_occurrence"] += 1
            elif cross:
                counts["same_endpoint_two_cross_tail"] += 1
            else:
                counts["same_endpoint_pure_zero_tail"] += 1
        classes[label] = dict(sorted(counts.items()))

    require(tuple(map(len, alternatives.values())) == (2, 8, 2),
            ("the response-mate sizes changed", alternatives))
    require(classes == {
        "110000": {"same_endpoint_pure_zero_tail": 2},
        "110011": {
            "changed_endpoint_occurrence": 6,
            "same_endpoint_two_cross_tail": 2,
        },
        "111100": {"same_endpoint_two_cross_tail": 2},
    }, ("the response-mate classes changed", classes))

    # The two fixed-endpoint rows are the two sides of one literal tail
    # square.  Their alternates have exactly the advertised decorations.
    require(alternatives["110000"] == [
        "P0S1:24|35", "P0S1:25|34"
    ], alternatives["110000"])
    require(alternatives["111100"] == [
        "P0S1:24|35", "P0S1:25|34"
    ], alternatives["111100"])
    return {
        "common_nonzero_endpoint_factor": "p1[0,1]*s1[1,1]",
        "private_selected_tail": "23|45",
        "required_alternate_counts": {
            label: len(values) for label, values in alternatives.items()
        },
        "alternate_occurrences": alternatives,
        "alternate_classes": classes,
        "normalized_seed": {
            "R11[110000]": (
                "forces 24|35 or 25|34 with 00 decorations; with "
                "alpha=q01[00] this is a second pure-zero target matching "
                "through the same literal coloop"
            ),
            "R11[111100]": (
                "forces the same two tails with 10 decorations, hence a "
                "literal same-head two-cross response carrier omitting q01"
            ),
            "R11[110011]": (
                "forces either the complementary 01 two-cross tail or one "
                "of six changed-endpoint response occurrences"
            ),
        },
        "sharp_remaining_landing": (
            "prove that this three-row labelled response seed lands in the "
            "committed normalized target-coloop/four-good chain.  The scan "
            "does not identify its cross-word coefficients with the open "
            "pointed occurrence covector P_f"
        ),
    }


def audit_response_seed_hall_exit(first, saturation, trapped):
    """Every way to complete the three private rows exits closed Hall shores.

    A nonzero alternate response occurrence certifies its endpoint closure as
    an effective response hole and each of its cross-colour q edges as an
    active physical hole.  This is exactly the edge shadow used by the pinned
    first-mate and saturation theorems.  Multiple alternate occurrences only
    enlarge the certified set, so it suffices to select one per private row.
    """
    words = (
        (1, 1, 0, 0, 0, 0),
        (1, 1, 0, 0, 1, 1),
        (1, 1, 1, 1, 0, 0),
    )
    selected = "P0S1:23|45"
    alternate_packets = tuple(
        tuple(record for record in structural_response_occurrences(first, word)
              if occurrence_label(record) != selected)
        for word in words
    )
    require(tuple(map(len, alternate_packets)) == (2, 8, 2),
            "the response completion packet changed")
    concepts = closed_concepts(saturation)
    tested = 0
    survivors = []
    added_edge_histogram = Counter()
    for item in trapped:
        for completion in product(*alternate_packets):
            edges = set(item["certified_edges"])
            before = frozenset(edges)
            for p_site, s_site, _matching, cells in completion:
                edges.add(edge(p_site, s_site))
                edges.update((left, right)
                             for left, right, left_colour, right_colour in cells
                             if left_colour != right_colour)
            added_edge_histogram[len(edges - before)] += 1
            fits = tuple((left, right) for left, right in concepts
                         if edges <= mask_edges(saturation, left))
            if fits:
                survivors.append((item["dual"], completion, fits))
            tested += 1
    require(tested == 148 * 2 * 8 * 2 == 4736,
            ("the response completion count changed", tested))
    require(not survivors,
            ("a completed response seed stayed in a closed shore",
             survivors[:3]))
    require(sum(added_edge_histogram.values()) == tested,
            "the added-edge histogram lost a completion")
    return {
        "response_mate_choices_per_trapped_packet": "2*8*2=32",
        "total_completions_tested": tested,
        "closed_shore_survivors": len(survivors),
        "added_certified_edge_count_histogram": {
            str(key): value
            for key, value in sorted(added_edge_histogram.items())
        },
        "monotonicity": (
            "if a zero coefficient contains several alternate occurrences, "
            "choose any one; the additional certified edges cannot restore "
            "containment in a closed shore"
        ),
        "physical_composition": (
            "cross-colour q cells enter the pinned active-fan hole theorem; "
            "a nonzero p1/s1 occurrence certifies its removed endpoint pair "
            "as the same effective response hole used in ab3e510/5ddaa7e"
        ),
        "conclusion": (
            "completion of all three private response coefficients forces a "
            "certified hole outside every current closed shore, hence strict "
            "Hall-closure growth; neither the triangle nor the nine-edge trap "
            "can be a complete unary-plus-response source packet"
        ),
    }


def audit():
    pin_dependencies()
    first = load(
        "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py",
        "closed_shore_first_gate",
    )
    saturation = load(
        "computations/verify_h3_active_fan_coloop_saturation_boundary.py",
        "closed_shore_saturation",
    )
    _packets, trapped, three_unary = audit_three_unary_packets(
        first, saturation
    )
    complete_row_scan = audit_complete_row_scan(first, trapped)
    forced_response_seed = audit_forced_response_seed(first)
    response_hall_exit = audit_response_seed_hall_exit(
        first, saturation, trapped
    )
    ledger = {
        "theorem": "h3 active-coloop closed-shore complete-row response gate",
        "pins": PINS,
        "three_mixed_unary_words": [word_label(word) for word in MIXED_WORDS],
        "simultaneous_unary_mate_census": three_unary,
        "complete_unary_plus_four_response_scan": complete_row_scan,
        "forced_response_seed": forced_response_seed,
        "completed_response_seed_hall_exit": response_hall_exit,
        "exact_verdict": (
            "After all three mixed unary coefficients are imposed, the "
            "closed triangle of 5ddaa7e has no survivor.  The only closed "
            "support shadows are 148 exact nine-edge/singleton packets.  "
            "Every such packet leaves R11[110000], R11[110011], and "
            "R11[111100] private, so complete response equations force the "
            "same explicit three-row alternate-occurrence seed.  All 4736 "
            "ways to choose one response mate in each row leave every closed "
            "K6 shore.  Thus the certified Hall closure grows strictly: the "
            "two sharp traps are not complete source packets"
        ),
        "scope": (
            "Boolean support census plus literal coefficient identities for "
            "the pinned two-occurrence guard.  Nonzero means a source cell is "
            "present; no generic-value noncancellation beyond a private "
            "single occurrence is used.  The conclusion is strict certified "
            "Hall growth/active-fan entry, not an identification of these "
            "cross-word rows with the open pointed occurrence covector P_f"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("closed-shore response ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    print("closed triangle after three unary words: ELIMINATED")
    print("nine-edge/singleton support survivors: 148")
    print("universal private complete rows: R11[110000,110011,111100]")
    print("completed response-seed closed-shore survivors: 0/4736")
    print("ledger_sha256=" + digest)
    return ledger


if __name__ == "__main__":
    audit()
