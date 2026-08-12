#!/usr/bin/env python3
"""Classify the nine h=3 four-base bridges through the response rows.

Five of the nine pure-zero physical C4 bridges from c44d784 contain at
least one selected response-hole edge.  The other four are silent at all
four selected holes.  For each silent bridge and each of the 3 x 3 selected
bright cofactor tails, this checker finds a literal fixed-port private zero
coefficient.  Its selected support has one monomial; each of the other two
residual matchings either contains a nonanchor off-diagonal cell or is a
same-word typed C4 exchange with the selected monomial.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_four_base_disconnected_unary_bridge.py":
        "d947a03540fedf42d6c5b3eaa37838d7f087659251d3a26fdcd1b8dd64ef092d",
    "notes/h3-four-base-disconnected-unary-bridge.md":
        "65fa33d6a61af853effc66f7edbe5b670d8f600f0c28770bd416fa25cff0ccd8",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = "e5991dfb5af90ecd42d0a81f295facb6027404dbf32193f06501a71b0e615d2b"

SITES = tuple(range(6))
BASES = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 1), (2, 4), (3, 5)),
    ((0, 2), (1, 5), (3, 4)),
    ((0, 5), (1, 2), (3, 4)),
)
BASE_UNION = set().union(*(set(base) for base in BASES))
RESPONSE_HOLES = {
    "G11": (0, 1),
    "G12": (0, 4),
    "G21": (1, 3),
    "G22": (3, 4),
}
FIXED_ROWS = {
    "G11": (0, 1, 1, 1),
    "G12": (0, 4, 1, 2),
    "G21": (3, 1, 2, 1),
    "G22": (3, 4, 2, 2),
}
BRIGHT_TAILS = {
    1: (
        ((2, 3), (4, 5)),
        ((2, 4), (3, 5)),
        ((2, 5), (3, 4)),
    ),
    2: (
        ((0, 1), (2, 5)),
        ((0, 2), (1, 5)),
        ((0, 5), (1, 2)),
    ),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


def is_c4(left, right):
    return len(set(left) ^ set(right)) == 4


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def audit_bridges():
    bridges = []
    for matching in MATCHINGS:
        adjacent = tuple(index for index, base in enumerate(BASES)
                         if is_c4(matching, base))
        if not (set(adjacent) & {0, 1} and set(adjacent) & {2, 3}):
            continue
        lifts = tuple(name for name, hole in RESPONSE_HOLES.items()
                      if hole in matching)
        bridges.append({
            "matching": matching,
            "name": matching_name(matching),
            "adjacent_base_indices": adjacent,
            "selected_response_lifts": lifts,
            "removed_hole_tails": {
                name: tuple(edge for edge in matching
                            if edge != RESPONSE_HOLES[name])
                for name in lifts
            },
        })
    require(len(bridges) == 9, "the nine physical bridges changed")
    visible = [record for record in bridges
               if record["selected_response_lifts"]]
    silent = [record for record in bridges
              if not record["selected_response_lifts"]]
    require(len(visible) == 5 and len(silent) == 4,
            "the selected-hole visibility split changed")
    require(Counter(name for record in visible
                    for name in record["selected_response_lifts"]) == Counter({
        "G11": 1, "G22": 1, "G12": 2, "G21": 2,
    }), "the response-lift row census changed")
    require({record["name"] for record in silent} == {
        "02|14|35", "03|12|45", "03|15|24", "05|14|23",
    }, "the four silent bridges changed")
    return bridges, visible, silent


def selected_support_terms(row, unary_matching, first_tail, second_tail):
    """Expand one fixed-port row on the three selected matching slices."""

    p_site, s_site, p_colour, s_colour = row
    q_cells = defaultdict(list)
    # The bridge is an extension of the old four-base packet.  Retain every
    # old pure-zero cell, not merely the three cells of the new matching.
    for physical in BASE_UNION | set(unary_matching):
        q_cells[physical].append((0, 0, "q00"))
    for physical in first_tail:
        q_cells[physical].append((1, 1, "q11"))
    for physical in second_tail:
        q_cells[physical].append((2, 2, "q22"))

    residual_sites = tuple(site for site in SITES
                           if site not in (p_site, s_site))
    polynomials = defaultdict(list)
    for tail in perfect_matchings(residual_sites):
        choices = tuple(q_cells[physical] for physical in tail)
        if any(not options for options in choices):
            continue
        for selected in product(*choices):
            word = [None] * 6
            word[p_site] = p_colour
            word[s_site] = s_colour
            factors = []
            for physical, (left_colour, right_colour, slice_name) in zip(
                    tail, selected, strict=True):
                word[physical[0]] = left_colour
                word[physical[1]] = right_colour
                factors.append((physical, slice_name))
            polynomials[tuple(word)].append({
                "tail": tail,
                "factors": tuple(factors),
            })
    return polynomials, residual_sites


def prescribed_mate(word, tail, anchor_union):
    cells = []
    for physical in tail:
        decoration = (word[physical[0]], word[physical[1]])
        offdiagonal = decoration[0] != decoration[1]
        cells.append({
            "physical_edge": physical,
            "decoration": decoration,
            "offdiagonal": offdiagonal,
            "outside_anchor_union": physical not in anchor_union,
        })
    external = any(cell["offdiagonal"] and cell["outside_anchor_union"]
                   for cell in cells)
    return {
        "tail": tail,
        "prescribed_cells": cells,
        "route": "nonanchor_offdiagonal" if external else "typed_same_tail_C4",
    }


def candidate_witnesses(unary_matching, first_tail, second_tail):
    anchor_union = (set(unary_matching) | {(0, 1), (3, 4)}
                    | set(first_tail) | set(second_tail))
    row_order = {name: index for index, name in enumerate(FIXED_ROWS)}
    candidates = []
    for row_name, row in FIXED_ROWS.items():
        polynomials, residual_sites = selected_support_terms(
            row, unary_matching, first_tail, second_tail
        )
        target_word = ((1,) * 6 if row_name == "G11" else
                       (2,) * 6 if row_name == "G22" else None)
        for word, selected_terms in polynomials.items():
            if word == target_word or len(selected_terms) != 1:
                continue
            selected = selected_terms[0]
            mates = tuple(prescribed_mate(word, tail, anchor_union)
                          for tail in perfect_matchings(residual_sites)
                          if tail != selected["tail"])
            require(len(mates) == 2,
                    "a four-residual-site coefficient lost a mate")
            # A diagonal anchor-contained mate would not be a useful typed
            # bridge.  Every retained candidate has a mixed decoration.
            if not all(any(cell["offdiagonal"]
                           for cell in mate["prescribed_cells"])
                       for mate in mates):
                continue
            external_count = sum(mate["route"] == "nonanchor_offdiagonal"
                                 for mate in mates)
            candidates.append({
                "row": row_name,
                "word": "".join(map(str, word)),
                "selected_tail": selected["tail"],
                "selected_factors": selected["factors"],
                "alternate_mates": mates,
                "external_mate_count": external_count,
                "typed_anchor_mate_count": 2 - external_count,
            })
    candidates.sort(key=lambda record: (
        -record["external_mate_count"],
        row_order[record["row"]], record["word"],
        record["selected_tail"], record["selected_factors"],
    ))
    return candidates


def audit_silent_bright_completion(silent):
    records = []
    for unary_record in silent:
        unary_matching = unary_record["matching"]
        for first_index, first_tail in enumerate(BRIGHT_TAILS[1], 1):
            for second_index, second_tail in enumerate(BRIGHT_TAILS[2], 1):
                candidates = candidate_witnesses(
                    unary_matching, first_tail, second_tail
                )
                require(candidates,
                        "a silent bridge/bright pair lost every private row")
                witness = candidates[0]
                require(witness["external_mate_count"] in (1, 2),
                        "a canonical private row has no nonanchor mate")
                require(witness["typed_anchor_mate_count"] in (0, 1),
                        "a canonical private row gained two trapped mates")
                records.append({
                    "unary_bridge": unary_record["name"],
                    "X1_tail_index": first_index,
                    "X2_tail_index": second_index,
                    "witness": witness,
                    "consequence": (
                        "after localizing the selected monomial, exactness "
                        "gives an ordinary unit if no mate is present; a "
                        "present mate is either a nonanchor offdiagonal "
                        "route or a same-word C4 sharing both fixed endpoint "
                        "factors"
                    ),
                })
    require(len(records) == 36,
            "the four-by-nine bright completion census changed")
    profile = Counter(
        (record["witness"]["external_mate_count"],
         record["witness"]["typed_anchor_mate_count"])
        for record in records
    )
    require(profile == Counter({(2, 0): 36}),
            f"the private-row route profile changed: {profile}")
    trapped = tuple(
        (record["unary_bridge"], record["X1_tail_index"],
         record["X2_tail_index"])
        for record in records
        if record["witness"]["typed_anchor_mate_count"]
    )
    require(not trapped,
            "a full-old-support chart acquired an anchor-contained mate")
    return records, profile, trapped


def audit():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    bridges, visible, silent = audit_bridges()
    bright_records, route_profile, trapped = audit_silent_bright_completion(
        silent
    )
    ledger = {
        "physical_bridge_records": bridges,
        "selected_response_visibility": {
            "visible_bridge_count": len(visible),
            "lift_occurrence_count": sum(
                len(record["selected_response_lifts"])
                for record in visible
            ),
            "silent_bridge_count": len(silent),
            "silent_bridges": tuple(record["name"] for record in silent),
        },
        "fixed_port_bright_completion": {
            "chart_count": len(bright_records),
            "route_profile": {
                "both_mates_nonanchor": route_profile[(2, 0)],
                "one_nonanchor_one_anchor_typed_C4": route_profile[(1, 1)],
            },
            "anchor_typed_chart_keys": trapped,
            "records": bright_records,
        },
        "theorem": (
            "five of the nine forced pure-zero bridges lift through the "
            "selected response holes.  Each of the four silent bridges, "
            "after arbitrary selected X1/X2 bright cofactor tails are "
            "adjoined on the fixed ports, has a private zero row yielding "
            "a localized unit or a nonanchor offdiagonal mate.  The "
            "same-word typed-C4 alternative is available abstractly but "
            "is not needed in any of the 36 full-old-support charts"
        ),
        "scope": (
            "the positive 36-chart statement is fixed-port and localized "
            "at the selected unary/bright monomials.  It does not classify "
            "additional core-port endpoint components.  A typed C4 edge is "
            "the source-valid input to the flat/nonflat carrier theorem, "
            "not by itself a proof of a nonzero minor or four-good rank"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"response-visibility ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 four-base bridge response visibility: PASS")
    print("physical bridges: 5 selected-hole visible, 4 fixed-port silent")
    print("visible response lift occurrences: 6")
    print("silent bright completion: 36/36 unit or nonanchor")
    print("route profile: 36 both alternatives offanchor")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
