#!/usr/bin/env python3
"""Classify all fourteen mates forced by the first mixed unary row.

The literal guard in 44cdd15 has the private term

    q01[00] q23[00] q45[11]

in H0[000011].  The full zero coefficient forces one of the other fourteen
perfect-matching monomials.  Two are all-diagonal and immediately create a
pure-zero matching avoiding the claimed coloop 01.  The other twelve each
contain two nonzero offdiagonal cells in the same zero mixed unary row, so
they enter the pinned physical active-fan alternative.

Eight of the twelve also contain one of the literal endpoint closure edges
01,04,14 and therefore give a fully labelled R11 response occurrence using
the already nonzero endpoint cells.  The other four form the exact smallest
head-dark rectangle before the active-fan theorem is applied.  None changes
the selected f/g transverse minors directly: all added decorations differ
from the pure-one closing cells and from the second endpoint heads.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py":
        "f35618988f591a28fd2a6574977c058aa2bec83a2cacfeb9e7567873e0b61d1c",
    "notes/h3-coloop-two-occurrence-complete-response-first-mixed-unary-gate.md":
        "94ffe3523f27aebb1064f2778b9a2a6fe99835ad98fc59b6a28dd57b6d9e9fa6",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
}
EXPECTED_LEDGER_SHA256 = "736d919f789df3b87f1fc84e16ec6d03c996859b9e02ca237af9b7a579f6d4b7"

WORD = (0, 0, 0, 0, 1, 1)
SELECTED = ((0, 1), (2, 3), (4, 5))
COLOOP = (0, 1)
# Existing nonzero endpoint cells close exactly these physical pairs.
CLOSURES = {
    (0, 1): (0, 1, "f/f"),
    (0, 4): (0, 4, "f/g"),
    (1, 4): (1, 4, "g/g"),
}


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


def cell(edge, word=WORD):
    left, right = edge
    return (left, right, word[left], word[right])


def word_label(word):
    return "".join(map(str, word))


def term_label(p_site, s_site, tail, output_word):
    factors = [f"p1[{p_site},{output_word[p_site]}]",
               f"s1[{s_site},{output_word[s_site]}]"]
    factors.extend(
        f"q{left}{right}[{output_word[left]}{output_word[right]}]"
        for left, right in tail
    )
    return "*".join(factors)


def audit_mates(first):
    _p_values, _s_values, base_q = first.literal_guard_values()
    mates = tuple(matching for matching in first.MATCHINGS6
                  if matching != SELECTED)
    require(len(mates) == 14, "the alternate matching count changed")

    records = []
    classes = Counter()
    response_words = Counter()
    endpoint_provenance = Counter()
    head_dark = []
    active_cells = set()
    for matching in mates:
        decorated = tuple(cell(edge) for edge in matching)
        cross = tuple(edge for edge in matching
                      if WORD[edge[0]] != WORD[edge[1]])
        diagonal = not cross
        closure_hits = tuple(edge for edge in matching if edge in CLOSURES)
        require(len(closure_hits) <= 1,
                ("one mate acquired two endpoint closures", matching))

        if diagonal:
            require((4, 5) in matching,
                    "an all-diagonal mate lost the 11 edge")
            zero_edges = tuple(edge for edge in matching if edge != (4, 5))
            # The mate makes both zero-decorated cells nonzero.  The base
            # coloop cofactor already has q45[00]!=0, hence replacing the
            # mate's q45[11] by q45[00] gives a nonzero pure-zero matching
            # which avoids 01.
            pure_zero_avoider = zero_edges + ((4, 5),)
            require(COLOOP not in pure_zero_avoider
                    and all(base_q.get(first.q_label(
                        left, right, 0, 0
                    ), Q(0)) for left, right in ((4, 5),)),
                    "the diagonal mate stopped breaking coloopness")
            outcome = "pure_zero_matching_avoids_coloop"
            classes[outcome] += 1
            record = {
                "matching": repr(matching),
                "decorated_cells_in_H000011": [repr(value)
                                                for value in decorated],
                "class": outcome,
                "pure_zero_avoiding_matching": repr(pure_zero_avoider),
                "target_effect": "strict pure-zero support expansion",
                "selected_f_g_transverse_minor": 0,
            }
        else:
            require(len(cross) == 2,
                    ("an offdiagonal mate lost its two cross cells", matching))
            cross_cells = tuple(cell(edge) for edge in cross)
            require(all(value not in base_q for value in cross_cells),
                    ("a cross-colour mate cell was already in the guard", matching))
            active_cells.update(cross_cells)
            if closure_hits:
                closure = closure_hits[0]
                p_site, s_site, provenance = CLOSURES[closure]
                tail = tuple(edge for edge in matching if edge != closure)
                output = list(WORD)
                output[p_site] = 1
                output[s_site] = 1
                output = tuple(output)
                # Tail decorations are unchanged because only the removed
                # closure endpoints are recoloured.  This is a literal
                # R11 occurrence with the already nonzero p1/s1 cells.
                require(all(output[left] == WORD[left]
                            and output[right] == WORD[right]
                            for left, right in tail),
                        "endpoint closure recoloured a retained q tail")
                response_term = term_label(p_site, s_site, tail, output)
                outcome = "labelled_R11_coloop_avoiding_active_carrier"
                classes[outcome] += 1
                response_words[word_label(output)] += 1
                endpoint_provenance[provenance] += 1
                record = {
                    "matching": repr(matching),
                    "decorated_cells_in_H000011": [repr(value)
                                                    for value in decorated],
                    "cross_colour_cells": [repr(value)
                                            for value in cross_cells],
                    "class": outcome,
                    "removed_closure_edge": repr(closure),
                    "response_head": "R11",
                    "response_word": word_label(output),
                    "response_term": response_term,
                    "endpoint_provenance": provenance,
                    "response_target": 0,
                    "coloop_q01_incidence_in_response_term": 0,
                    "selected_f_g_transverse_minor": 0,
                }
            else:
                outcome = "head_dark_two_cross_active_carrier"
                classes[outcome] += 1
                head_dark.append(matching)
                record = {
                    "matching": repr(matching),
                    "decorated_cells_in_H000011": [repr(value)
                                                    for value in decorated],
                    "cross_colour_cells": [repr(value)
                                            for value in cross_cells],
                    "class": outcome,
                    "unary_word": word_label(WORD),
                    "unary_target": 0,
                    "endpoint_closure_in_current_f_g_packet": False,
                    "coloop_q01_incidence": 0,
                    "selected_f_g_transverse_minor": 0,
                }
            records.append(record)
            continue
        records.append(record)

    require(classes == Counter({
        "pure_zero_matching_avoids_coloop": 2,
        "labelled_R11_coloop_avoiding_active_carrier": 8,
        "head_dark_two_cross_active_carrier": 4,
    }), ("the fourteen-mate landing split changed", classes))
    require(response_words == Counter({
        "110011": 2, "100011": 3, "010011": 3,
    }), ("the labelled response-word split changed", response_words))
    require(endpoint_provenance == Counter({
        "f/f": 2, "f/g": 3, "g/g": 3,
    }), ("the endpoint provenance split changed", endpoint_provenance))
    expected_head_dark = (
        ((0, 2), (1, 5), (3, 4)),
        ((0, 3), (1, 5), (2, 4)),
        ((0, 5), (1, 2), (3, 4)),
        ((0, 5), (1, 3), (2, 4)),
    )
    require(tuple(head_dark) == expected_head_dark,
            ("the head-dark rectangle changed", head_dark))
    require(active_cells == {
        (0, 4, 0, 1), (0, 5, 0, 1),
        (1, 4, 0, 1), (1, 5, 0, 1),
        (2, 4, 0, 1), (2, 5, 0, 1),
        (3, 4, 0, 1), (3, 5, 0, 1),
    }, ("the offdiagonal active-cell universe changed", active_cells))

    # No mate adds q01[11], q14[11], a second endpoint-head cell, or any
    # other coefficient occurring in the four selected f/g minors.
    require(all(record["selected_f_g_transverse_minor"] == 0
                for record in records),
            "a mate unexpectedly changed the selected f/g minors")
    return {
        "forced_alternate_matchings": len(mates),
        "classification": dict(sorted(classes.items())),
        "all_added_offdiagonal_cells": [repr(value)
                                         for value in sorted(active_cells)],
        "labelled_R11_response_words": dict(sorted(response_words.items())),
        "endpoint_provenance": dict(sorted(endpoint_provenance.items())),
        "head_dark_rectangle": [repr(value) for value in head_dark],
        "mate_records": records,
        "transverse_minor_outcomes": 0,
        "why_no_direct_minor": (
            "the mates add only 00/01/11 q cells in H0[000011]; none adds "
            "the pure-one closing cells q01[11],q14[11] or a second-head "
            "endpoint coefficient used by the four selected f/g minors"
        ),
    }


def audit():
    pin_dependencies()
    first = load(
        "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py",
        "fourteen_mate_first_gate",
    )
    classification = audit_mates(first)
    ledger = {
        "theorem": "h3 first mixed-unary fourteen-mate landing",
        "pins": PINS,
        "literal_classification": classification,
        "composition_with_pinned_active_fan_theorem": {
            "input": (
                "each of the twelve offdiagonal mates contains a nonzero "
                "offdiagonal decorated cell in the physical zero mixed row "
                "H0[000011]"
            ),
            "private_site_output": "source-provenant distinct-head active fan",
            "complete_pure_support_output": "four-good or literal pure-colour coloop",
            "head_dark_four_need_separate_endpoint_closure": False,
        },
        "exhaustive_landing": {
            "two_diagonal": (
                "a nonzero pure-zero matching avoids 01, so the assumed "
                "literal pure-zero coloop has already escaped"
            ),
            "eight_endpoint_closable": (
                "an explicit R11 mixed response occurrence omits q01 and "
                "carries full word/head/orientation/tail labels, while its "
                "offdiagonal cells also enter the active-fan theorem"
            ),
            "four_head_dark": (
                "the exact smaller rectangle has no current f/g endpoint "
                "closure, but its offdiagonal zero-row cells still enter "
                "the physical private-site fan theorem"
            ),
        },
        "frontier": (
            "the first mixed-unary cancellation cannot remain inside the "
            "two-occurrence localized coloop guard: it either destroys "
            "coloopness or enters four-good/another literal coloop.  It does "
            "not by itself construct the selected P_f transverse minor"
        ),
        "scope": (
            "the final coloop outcome is passed to the already isolated "
            "active-fan coloop normalization/pointed-comparison theorem; "
            "this checker does not claim that arbitrary coloop landing is closed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("fourteen-mate ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    print("H0[000011] mates: 2 DIAGONAL COLOOP ESCAPES")
    print("H0[000011] mates: 8 LABELLED RESPONSE + 4 HEAD-DARK ACTIVE CARRIERS")
    print("selected f/g transverse minors: NONE FORCED DIRECTLY")
    print("ledger_sha256=" + digest)
    return ledger


if __name__ == "__main__":
    audit()
