#!/usr/bin/env python3
"""Audit the first decoration rows for the nine c44d784 C4 bridges.

The selected endpoint holes are 01,04,13,34.  Four forced bridges contain
one crossed hole, one contains both diagonal holes, and four contain no
selected hole.  After choosing one pure-11 and one pure-22 target cofactor,
the last four bridges have an exact 5/4 split among the nine bright charts:
five charts give a two-term mixed-unary C4 row and four have no occurrence
of the bridge outside the pure-zero unary word.
"""

from __future__ import annotations

from collections import Counter
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
    "computations/verify_h3_silent_c6_first_bright_unary_escape.py":
        "bf0100b52bd21f412f8e09ebb8017d4465a8be849ae2b9c0e8a2dbe679725d35",
    "notes/h3-silent-c6-first-bright-unary-escape.md":
        "13bbba4edca4854eb484dbf8050532a480fb8e81605d57f85738d80d71b12e70",
}
EXPECTED_LEDGER_SHA256 = "bf2f107bdf19d2bcd8206a9d70fe73f457bec0afb55a37475228573fb009c2a5"

SITES = tuple(range(6))
A = ((0, 1), (2, 3), (4, 5))
B = ((0, 1), (2, 4), (3, 5))
K = ((0, 2), (1, 5), (3, 4))
L = ((0, 5), (1, 2), (3, 4))
BASES = (A, B, K, L)
BASE_NAMES = {base: name for base, name in zip(BASES, "ABKL")}
BASE_UNION = set().union(*(set(base) for base in BASES))

RESPONSE_HOLES = {
    "G11": (0, 1),
    "G12": (0, 4),
    "G21": (1, 3),
    "G22": (3, 4),
}
CROSSED_HOLES = {RESPONSE_HOLES["G12"], RESPONSE_HOLES["G21"]}

# The q tails of a selected pure diagonal target matching.  The endpoint
# edge is supplied by the corresponding p/s port, not by q.
BRIGHT_11 = (
    ((2, 3), (4, 5)),
    ((2, 4), (3, 5)),
    ((2, 5), (3, 4)),
)
BRIGHT_22 = (
    ((0, 1), (2, 5)),
    ((0, 2), (1, 5)),
    ((0, 5), (1, 2)),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return answer


MATCHINGS = tuple(perfect_matchings(SITES))


def is_c4(left, right):
    return len(set(left) ^ set(right)) == 4


def word_with_diagonal_edge(edge, colour):
    word = [0] * 6
    word[edge[0]] = colour
    word[edge[1]] = colour
    return tuple(word)


def supported_top_matchings(word, cells):
    answer = []
    for matching in MATCHINGS:
        if all((edge, (word[edge[0]], word[edge[1]])) in cells
               for edge in matching):
            answer.append(matching)
    return tuple(answer)


def forced_bridges():
    overlap = ((0, 1), (2, 5), (3, 4))
    avoiding = tuple(matching for matching in MATCHINGS
                     if (0, 1) not in matching and (3, 4) not in matching)
    candidates = (overlap,) + avoiding
    bridges = []
    for matching in candidates:
        adjacent = tuple(base for base in BASES if is_c4(matching, base))
        if (any(base in (A, B) for base in adjacent)
                and any(base in (K, L) for base in adjacent)):
            bridges.append(matching)
    require(len(bridges) == 9, "the c44d784 bridge list changed")
    return tuple(bridges)


def response_triangle(hole):
    remaining = tuple(site for site in SITES if site not in hole)
    return tuple(tuple(sorted((hole,) + tail))
                 for tail in perfect_matchings(remaining))


def audit_response_rows(bridges):
    records = []
    occurrence_counts = Counter()
    for bridge in bridges:
        rows = []
        for row, hole in RESPONSE_HOLES.items():
            if hole not in bridge:
                continue
            triangle = response_triangle(hole)
            require(bridge in triangle and len(triangle) == 3,
                    "a fixed-hole cofactor stopped being a triangle")
            rows.append({
                "row": row,
                "hole": hole,
                "literal_word": {
                    "G11": "110000", "G12": "100020",
                    "G21": "010200", "G22": "000220",
                }[row],
                "matching_triangle": triangle,
            })
        cross_count = sum(item["hole"] in CROSSED_HOLES for item in rows)
        occurrence_counts[(len(rows), cross_count)] += 1
        records.append({"bridge": bridge, "response_rows": rows})

    require(occurrence_counts == Counter({(1, 1): 4, (0, 0): 4,
                                          (2, 0): 1}),
            f"selected-hole occurrence split changed: {occurrence_counts}")

    overlap = ((0, 1), (2, 5), (3, 4))
    overlap_record = next(item for item in records
                          if item["bridge"] == overlap)
    require({row["row"] for row in overlap_record["response_rows"]}
            == {"G11", "G22"},
            "the overlap bridge lost its two diagonal rows")
    require({tuple(row["matching_triangle"])
             for row in overlap_record["response_rows"]} == {
                 tuple(response_triangle((0, 1))),
                 tuple(response_triangle((3, 4))),
             }, "the overlap bridge cofactor triangles changed")

    cross_records = [item for item in records
                     if any(row["hole"] in CROSSED_HOLES
                            for row in item["response_rows"])]
    for item in cross_records:
        row = item["response_rows"][0]
        other = set(row["matching_triangle"]) - {item["bridge"]}
        require(len(other) == 2, "a crossed cofactor lost a mate")
        require(any(not any(is_c4(candidate, base) for base in BASES)
                    for candidate in other),
                "a crossed cofactor lost its C6 separator")
    return records


def audit_bright_rows(bridges):
    records = []
    cross_avoiding = [bridge for bridge in bridges
                      if not (set(bridge) & CROSSED_HOLES)]
    require(len(cross_avoiding) == 5,
            "the crossed-hole-avoiding bridge count changed")

    fully_hole_free = [bridge for bridge in cross_avoiding
                       if not (set(bridge) & set(RESPONSE_HOLES.values()))]
    require(len(fully_hole_free) == 4,
            "the fully selected-hole-free bridge count changed")

    chart_counts = Counter()
    two_term_rows = []
    silent_charts = []
    for bridge in fully_hole_free:
        for i, j in product(range(3), repeat=2):
            a_tail = BRIGHT_11[i]
            b_tail = BRIGHT_22[j]
            cells = ({(edge, (0, 0)) for edge in BASE_UNION | set(bridge)}
                     | {(edge, (1, 1)) for edge in a_tail}
                     | {(edge, (2, 2)) for edge in b_tail})
            candidates = []
            for colour, tail in ((1, a_tail), (2, b_tail)):
                for edge in sorted(set(bridge) & set(tail)):
                    word = word_with_diagonal_edge(edge, colour)
                    support = supported_top_matchings(word, cells)
                    candidates.append((edge, colour, word, support))

            if not candidates:
                # With no bright-decorated edge on the bridge and no selected
                # endpoint hole, the bridge has no occurrence outside 0^6 in
                # this minimal decorated envelope.
                chart_counts["silent"] += 1
                silent_charts.append({
                    "bridge": bridge,
                    "A_index": i + 1,
                    "B_index": j + 1,
                    "reason": "no bridge edge occurs in either bright q tail",
                })
                continue

            chart_counts["two_term"] += 1
            for edge, colour, word, support in candidates:
                require(len(support) == 2 and bridge in support,
                        "a first bright bridge row stopped being binomial")
                mate = next(item for item in support if item != bridge)
                require(mate in BASES and is_c4(bridge, mate),
                        "the binomial mate stopped being an old C4 base")
                require(edge in bridge and edge in mate,
                        "the bright decorated common edge changed")
                two_term_rows.append({
                    "bridge": bridge,
                    "A_index": i + 1,
                    "B_index": j + 1,
                    "word": "".join(map(str, word)),
                    "bright_common_edge": edge,
                    "bright_colour": colour,
                    "mate": BASE_NAMES[mate],
                    "complete_top_support": support,
                })

    require(chart_counts == Counter({"two_term": 20, "silent": 16}),
            f"the hole-free bright chart split changed: {chart_counts}")
    require(len(two_term_rows) == 24,
            "the number of literal binomial bright rows changed")

    silent_by_bridge = Counter(item["bridge"] for item in silent_charts)
    require(set(silent_by_bridge.values()) == {4},
            "a hole-free bridge does not have exactly four silent charts")
    records.extend(two_term_rows)
    return {
        "crossed_hole_avoiding_bridges": cross_avoiding,
        "fully_selected_hole_free_bridges": fully_hole_free,
        "chart_split": dict(sorted(chart_counts.items())),
        "literal_binomial_rows": records,
        "silent_charts": silent_charts,
        "boundary": (
            "the overlap bridge is already visible in G11 and G22; each "
            "of the other four crossed-hole-avoiding bridges has five "
            "bright charts with a literal two-term unary C4 row and four "
            "charts with no bridge occurrence beyond the pure-zero word"
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    bridges = forced_bridges()
    ledger = {
        "bridge_count": len(bridges),
        "response_hole_audit": audit_response_rows(bridges),
        "bright_decoration_audit": audit_bright_rows(bridges),
        "theorem": (
            "selected-hole response rows synchronize five of nine physical "
            "bridges only partially: the overlap bridge joins both old "
            "cofactor triangles, four crossed-hole bridges enter crossed "
            "triangles, and the four fully hole-free bridges require a "
            "bright edge shared with an old base"
        ),
        "scope": (
            "the sixteen silent bright charts are exact first-layer guards, "
            "not full-source packets: arbitrary extra decorated q cells can "
            "supply the missing mixed unary mates"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"bridge synchronization ledger changed: {digest}")
    print("h3 four-base C4 bridge decoration synchronization: PASS")
    print("selected holes: overlap 2 diagonal rows; 4 crossed; 4 absent")
    print("hole-free bright charts: 20 binomial / 16 silent")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
