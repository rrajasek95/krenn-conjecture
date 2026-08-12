#!/usr/bin/env python3
"""First bright-target completion of the silent-C6 rational guard.

Normalize one pure-11 matching in H_01 and one pure-22 matching in H_34.
Every one of the six possible bright matchings contains an edge whose
pure-zero deleted cofactor is nonzero.  The unary mixed word with the bright
colour exactly at that edge then has nonzero coefficient.  Any cancellation
matching omitting the bright edge uses exactly two off-diagonal cells.

Thus a full bright completion immediately supplies a decorated external
mate (or one of the missing q04/q13 chords).  It need not supply a chord or
a same-star kernel: one of the nine simultaneous bright-pair choices keeps
both crossed tensors zero at this first layer, and every active edge has
chord-avoiding mate topologies.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SWITCH_PATH = (
    "computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py"
)
PINS = {
    "computations/verify_h3_silent_c6_five_lock_injective_no_wedge_guard.py":
        "0b4345441622f1defe74dd64c1b1877a70d2916e91df2df22ba13fa25000d702",
    "notes/h3-silent-c6-five-lock-injective-no-wedge-guard.md":
        "3853adf6006c66f2e69de4162babc00090c8257acfd9cf337e29752a68153fe0",
    SWITCH_PATH:
        "f99c185403bf2e86b7352c555cd02d85bfed0df668b8a87b44a725c3db7edc71",
}
EXPECTED_LEDGER_SHA256 = (
    "cffcaf1f7946df044e889d9dee25304da93eb3d15eaaf0889fcb970625076c3e"
)
SITES = tuple(range(6))
MISSING_CHORDS = {(0, 4), (1, 3)}
Q00_WEIGHTS = {
    (0, 1): Q(-2), (0, 2): Q(1), (0, 3): Q(1), (0, 5): Q(1),
    (1, 2): Q(1), (1, 4): Q(-3), (1, 5): Q(1),
    (2, 3): Q(-1), (2, 4): Q(-1), (2, 5): Q(1),
    (3, 4): Q(2), (3, 5): Q(1), (4, 5): Q(1),
}
BRIGHT = {
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


def load_switch():
    spec = spec_from_file_location("silent_c6_bright_switch", ROOT / SWITCH_PATH)
    require(spec is not None and spec.loader is not None,
            "cannot load matching expansion dependency")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


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


ALL_MATCHINGS = perfect_matchings(SITES)


def deleted_cofactor(edge):
    remainder = tuple(site for site in SITES if site not in edge)
    answer = Q(0)
    for matching in perfect_matchings(remainder):
        value = Q(1)
        for factor in matching:
            value *= Q00_WEIGHTS.get(factor, Q(0))
        answer += value
    return answer


def bright_word(edge, colour):
    word = [0] * len(SITES)
    for site in edge:
        word[site] = colour
    return tuple(word)


def omitting_mate_records(edge, colour):
    word = bright_word(edge, colour)
    records = []
    for matching in ALL_MATCHINGS:
        if edge in matching:
            continue
        decorated = tuple(
            (factor, (word[factor[0]], word[factor[1]]))
            for factor in matching
        )
        offdiagonal = tuple(
            factor for factor, label in decorated if label[0] != label[1]
        )
        require(len(offdiagonal) == 2,
                "an omitting mate lost the two-offdiagonal parity rule")
        records.append({
            "matching": matching,
            "decorated_cells": decorated,
            "offdiagonal_edges": offdiagonal,
            "uses_q04_or_q13": any(
                factor in MISSING_CHORDS for factor in matching
            ),
        })
    require(len(records) == 12,
            "a bright edge stopped having twelve omitting matchings")
    return records


def response_endpoints(colour):
    if colour == 1:
        return ((0, 1, Q(1)),), ((1, 1, Q(1)),)
    return ((3, 2, Q(1)),), ((4, 2, Q(1)),)


def q00(switch):
    return {
        switch.cell(left, right, 0, 0): value
        for (left, right), value in Q00_WEIGHTS.items()
    }


def add_bright_matching(switch, q, matching, colour):
    answer = dict(q)
    for edge in matching:
        answer[switch.cell(*edge, colour, colour)] = Q(1)
    return answer


def audit_single_bright_matchings(switch):
    records = []
    for colour in (1, 2):
        p, s = response_endpoints(colour)
        for index, matching in enumerate(BRIGHT[colour], 1):
            q = add_bright_matching(switch, q00(switch), matching, colour)
            tensor = switch.response(q, p, s, SITES)
            pure_word = (colour,) * 6
            require(tensor[pure_word] == 1,
                    "a normalized bright matching lost its pure target")

            cofactors = {edge: deleted_cofactor(edge) for edge in matching}
            active = tuple(edge for edge, value in cofactors.items() if value)
            require(active,
                    "a bright matching lost every unary-active edge")

            active_records = []
            for edge in active:
                word = bright_word(edge, colour)
                top = switch.matchings(q, SITES)
                require(top[word] == cofactors[edge] and top[word],
                        "the unary first-bright coefficient changed")
                mates = omitting_mate_records(edge, colour)
                chord = sum(record["uses_q04_or_q13"] for record in mates)
                require(chord < len(mates),
                        "a bright edge unexpectedly forced q04/q13")
                active_records.append({
                    "edge": edge,
                    "unary_word": "".join(map(str, word)),
                    "deleted_q00_cofactor": str(cofactors[edge]),
                    "omitting_mate_topologies": len(mates),
                    "mates_using_q04_or_q13": chord,
                    "mates_avoiding_q04_and_q13": len(mates) - chord,
                    "offdiagonal_cells_per_mate": 2,
                })

            records.append({
                "colour": colour,
                "bright_matching_index": index,
                "bright_matching": matching,
                "pure_target_coefficient": str(tensor[pure_word]),
                "edge_cofactors": {"%d%d" % edge: str(value)
                                   for edge, value in cofactors.items()},
                "unary_active_edges": active_records,
            })
    require(len(records) == 6, "the six bright choices changed")
    return records


def audit_simultaneous_pairs(switch):
    p1, s1 = response_endpoints(1)
    p2, s2 = response_endpoints(2)
    records = []
    crossed_dark = []
    for first_index, second_index in product(range(3), repeat=2):
        q = add_bright_matching(
            switch, q00(switch), BRIGHT[1][first_index], 1
        )
        q = add_bright_matching(
            switch, q, BRIGHT[2][second_index], 2
        )
        g12 = switch.response(q, p1, s2, SITES)
        g21 = switch.response(q, p2, s1, SITES)
        record = {
            "X1_matching_index": first_index + 1,
            "X2_matching_index": second_index + 1,
            "G12_nonzero_coefficients": len(g12),
            "G21_nonzero_coefficients": len(g21),
            "both_crossed_dark": not g12 and not g21,
        }
        records.append(record)
        if record["both_crossed_dark"]:
            crossed_dark.append(record)
    require(len(crossed_dark) == 1
            and crossed_dark[0]["X1_matching_index"] == 3
            and crossed_dark[0]["X2_matching_index"] == 1,
            "the unique crossed-dark first-bright pair changed")
    return records, crossed_dark[0]


def audit():
    pin_dependencies()
    switch = load_switch()
    singles = audit_single_bright_matchings(switch)
    pairs, crossed_dark = audit_simultaneous_pairs(switch)
    ledger = {
        "pins": PINS,
        "single_bright_matchings": singles,
        "simultaneous_bright_pairs": pairs,
        "unique_crossed_dark_pair": crossed_dark,
        "theorem": (
            "each normalized pure X1 or X2 matching contains a physical "
            "edge e with nonzero pure-zero deleted cofactor.  The unary "
            "mixed coefficient supported at e is therefore nonzero.  In "
            "any full source completion some matching omitting e must "
            "cancel it, and every such mate has exactly two offdiagonal "
            "decorations"
        ),
        "sharp_split": (
            "the first bright layer always forces a distinct decorated "
            "top-row mate, but does not force q04/q13 or a same-star "
            "kernel: every active edge has chord-avoiding mate topologies, "
            "and the pair X1=25|34, X2=01|25 keeps both crossed response "
            "tensors zero before its forced unary mates are added"
        ),
        "scope": (
            "exact first bright coefficient over the rational zero-fibre "
            "guard; the forced mate is a source consequence, while routing "
            "its two new offdiagonal decorations through later response "
            "rows is a separate decorated-anchor obligation"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"first bright completion ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 silent C6 first bright unary escape: PASS (exact)")
    print("six bright matchings: each has a unary-active edge")
    print("forced omitting mate: exactly two offdiagonal decorations")
    print("unique crossed-dark pair: X1=25|34, X2=01|25")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
