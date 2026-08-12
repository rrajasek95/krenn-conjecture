#!/usr/bin/env python3
"""Classify the exact response landing of the silent separator 03|14|25.

The unary separator localizes q25^00.  Together with the two selected
diagonal endpoint holes it creates two nonzero augmented response bases

  O11=P0|S1|25|34,  O22=P3|S4|01|25.

They share the decorated tail q25^00 and differ by one alternating C6.  A
complete matching enumeration proves that its only one-step C4 shortcuts
are the two crossed response bases (using q13 or q04) and the direct PS cap.
Thus a crossed cell gives the requested typed bridge, while their absence
is exactly one finite chordless diagonal response lock.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_four_base_disconnected_unary_bridge.py":
        "d947a03540fedf42d6c5b3eaa37838d7f087659251d3a26fdcd1b8dd64ef092d",
    "notes/h3-four-base-disconnected-unary-bridge.md":
        "65fa33d6a61af853effc66f7edbe5b670d8f600f0c28770bd416fa25cff0ccd8",
    "computations/verify_uniform_axis_k3_unequal_tail_reduction.py":
        "ef4c7bc9554fbf6fc5a65aef754d35359c46e0bb67014bd20060114a34cd1843",
    "notes/uniform-axis-k3-unequal-tail-reduction.md":
        "352e02a73da833fb159b24d581e7a91653fe195a76fbe3cc5aa531fd3e141993",
    "computations/verify_even_cycle_flat_transport_vertex_gauge.py":
        "27b34edca2cd8b0acfc9b899c524c0e27d5edc4fc423a261712d22280ed838d4",
    "notes/even-cycle-flat-transport-vertex-gauge.md":
        "0b5dbaee9a1d4c93778778e833a0baa99741c5091f8f52058858990c65cdde3d",
}
EXPECTED_LEDGER_SHA256 = "9a87cb6b4f0a860de0fd3594e83be0e2050caba2668ce328118fd4cb0423df9b"

VERTICES = ("P", "S", "0", "1", "2", "3", "4", "5")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def edge(left, right):
    return tuple(sorted((left, right)))


def matching(*edges):
    return tuple(sorted(edges))


def perfect_matchings(vertices):
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(matching(edge(first, second), *tail))
    return answer


TAIL = edge("2", "5")
O11 = matching(edge("P", "0"), edge("S", "1"), TAIL, edge("3", "4"))
O22 = matching(edge("P", "3"), edge("S", "4"), edge("0", "1"), TAIL)
C12 = matching(edge("P", "0"), edge("S", "4"), edge("1", "3"), TAIL)
C21 = matching(edge("P", "3"), edge("S", "1"), edge("0", "4"), TAIL)
CAP = matching(edge("P", "S"), edge("0", "1"), edge("3", "4"), TAIL)


def is_c4(left, right):
    return len(set(left) ^ set(right)) == 4


def cycle_vertices_and_edges(left, right):
    common = set(left) & set(right)
    difference = set(left) ^ set(right)
    vertices = set().union(*(set(item) for item in difference))
    degrees = {vertex: sum(vertex in item for item in difference)
               for vertex in vertices}
    return common, difference, vertices, degrees


def audit_augmented_cycle():
    common, difference, vertices, degrees = cycle_vertices_and_edges(O11, O22)
    require(common == {TAIL}, "the two diagonal bases lost q25 as common tail")
    require(len(difference) == 6 and len(vertices) == 6,
            "the diagonal overlap stopped being one C6")
    require(set(degrees.values()) == {2},
            "the diagonal overlap symmetric difference stopped being a cycle")

    reduced_vertices = tuple(vertex for vertex in VERTICES
                             if vertex not in {"2", "5"})
    left_reduced = tuple(item for item in O11 if item != TAIL)
    right_reduced = tuple(item for item in O22 if item != TAIL)
    intermediates = []
    for candidate in perfect_matchings(reduced_vertices):
        if is_c4(left_reduced, candidate) and is_c4(candidate, right_reduced):
            added = set(candidate) - set(left_reduced) - set(right_reduced)
            require(len(added) == 1,
                    "a C6 shortcut stopped having one distance-three chord")
            intermediates.append((candidate, tuple(added)[0]))
    expected = {
        (tuple(item for item in C12 if item != TAIL), edge("1", "3")),
        (tuple(item for item in C21 if item != TAIL), edge("0", "4")),
        (tuple(item for item in CAP if item != TAIL), edge("P", "S")),
    }
    require(set(intermediates) == expected,
            f"the complete distance-three chord list changed: {intermediates}")

    require(is_c4(O11, C12) and is_c4(C12, O22),
            "q13 stopped giving the two-step typed C4 path")
    require(is_c4(O11, C21) and is_c4(C21, O22),
            "q04 stopped giving the two-step typed C4 path")
    require(set(O11) & set(C12) == {edge("P", "0"), TAIL}
            and set(C12) & set(O22) == {edge("S", "4"), TAIL},
            "the q13 path lost an identical augmented common tail")
    require(set(O11) & set(C21) == {edge("S", "1"), TAIL}
            and set(C21) & set(O22) == {edge("P", "3"), TAIL},
            "the q04 path lost an identical augmented common tail")
    return {
        "common_tail": "q25^00",
        "alternating_cycle": "P-0-1-S-4-3-P",
        "distance_three_chords": tuple(
            sorted("".join(chord) for _, chord in intermediates)
        ),
        "crossed_paths": (
            "O11--C12(q13)--O22",
            "O11--C21(q04)--O22",
        ),
        "direct_cap_path": "O11--CAP(PS)--O22",
    }


def audit_literal_rows():
    rows = {
        "G11": {
            "word": "110000",
            "target": 0,
            "term": ("p1@0^1", "s1@1^1", "q25^00", "q34^00"),
            "matching": O11,
        },
        "G22": {
            "word": "000220",
            "target": 0,
            "term": ("p2@3^2", "s2@4^2", "q01^00", "q25^00"),
            "matching": O22,
        },
        "G12_q13_chord": {
            "word": "100020",
            "target": 0,
            "term": ("p1@0^1", "s2@4^2", "q13^00", "q25^00"),
            "matching": C12,
        },
        "G21_q04_chord": {
            "word": "010200",
            "target": 0,
            "term": ("p2@3^2", "s1@1^1", "q04^00", "q25^00"),
            "matching": C21,
        },
    }
    require(all(record["target"] == 0 for record in rows.values()),
            "one overlap/chord word acquired a target coefficient")
    require(rows["G11"]["matching"] == O11
            and rows["G22"]["matching"] == O22
            and rows["G12_q13_chord"]["matching"] == C12
            and rows["G21_q04_chord"]["matching"] == C21,
            "a literal source row was assigned to the wrong matching")
    return rows


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    ledger = {
        "literal_full_response_rows": audit_literal_rows(),
        "augmented_response_cycle": audit_augmented_cycle(),
        "theorem": (
            "the silent unary separator localizes q25^00 and hence the two "
            "diagonal augmented bases O11,O22; any nonzero q13 or q04 block "
            "gives a source-labelled two-C4 shortcut, while absence of both "
            "and of the reduced packet's nonexistent PS edge is exactly the "
            "finite chordless two-chart diagonal C6 lock"
        ),
        "scope": (
            "this is the complete first response landing, not a claim that "
            "an arbitrary diagonal lock web is already source-unit; extra "
            "matching terms in the four coefficient rows remain complete"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"silent C6 response-lock ledger changed: {digest}")
    print("h3 silent C6 response lock: PASS")
    print("crossed q13/q04 chord, direct cap, or one chordless diagonal C6 lock")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
