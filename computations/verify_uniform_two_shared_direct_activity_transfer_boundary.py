#!/usr/bin/env python3
"""Common-class transfer theorem and winding-class obstruction after e:mm.

For one fixed complement matching class, the label-transfer equations have
the signless incidence matrix of a path or cycle.  An open path exposes an
endpoint, an odd cycle has determinant 2, and an even cycle has the
alternating kernel used for anchor-safe deletion.

The second audit gives a literal common-q family showing why matching-class
incidence is essential.  Two pure anchors share e, the third avoids it,
q_e^(m,m) is nonzero, its pure-m cofactor is zero, all three constant fibres
are normalized singletons, and one mixed fibre is an exact binomial.  Its
cancellation mate winds around every site.  At six sites the first omitted
full coefficient is the singleton word 001111.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_two_shared_anchor_unary_label_migration.py":
        "78ab24f1c39d79ea38a80fd80bf43e43624e57dada0345c2c98b30559f528dc6",
    "notes/uniform-two-shared-anchor-unary-label-migration.md":
        "2e794feae556d582dc1623e698e2e331cae44e0de36e9d59125740a908d3b1c9",
    "computations/verify_uniform_cycle_switch_localization_countermodel.py":
        "10a624da37e4d73984fce03dcf16e6f15446f154807d1b3aa7cadbdb86a185c5",
    "notes/uniform-cycle-switch-localization-countermodel.md":
        "af3f0ab3ce9da84020aa6f3ace7dd024ab721ae863f7dd06d55339dde0c7ca80",
}
EXPECTED_LEDGER_SHA256 = "6ffef57d02ee591a4fe948236ad50d50f6d1157132c55e5d67b675f10b31ad42"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return left, right, left_colour, right_colour


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            output.append(tuple(sorted((edge(first, second),) + tail)))
    return tuple(output)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rank(matrix):
    work = [[int(entry) for entry in row] for row in matrix]
    from fractions import Fraction as Q
    work = [[Q(entry) for entry in row] for row in work]
    pivot_row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def determinant(matrix):
    from fractions import Fraction as Q
    work = [[Q(entry) for entry in row] for row in matrix]
    value = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value *= -1
        diagonal = work[column][column]
        value *= diagonal
        work[column] = [entry / diagonal for entry in work[column]]
        for row in range(column + 1, len(work)):
            factor = work[row][column]
            work[row] = [entry - factor * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[column], strict=True)]
    return int(value)


def signless_cycle(size):
    matrix = [[0] * size for _ in range(size)]
    for column in range(size):
        matrix[column][column] = 1
        matrix[(column + 1) % size][column] = 1
    return matrix


def signless_path(edges):
    matrix = [[0] * edges for _ in range(edges + 1)]
    for column in range(edges):
        matrix[column][column] = 1
        matrix[column + 1][column] = 1
    return matrix


def audit_common_class_transfer_theorem():
    records = []
    for size in range(2, 13):
        cycle = signless_cycle(size)
        computed_rank = rank(cycle)
        computed_det = determinant(cycle)
        if size % 2:
            require(computed_rank == size and abs(computed_det) == 2,
                    f"odd transfer cycle changed at size {size}")
            outcome = "ordinary characteristic-zero unit"
        else:
            alternating = tuple(1 if index % 2 == 0 else -1
                                for index in range(size))
            require(computed_rank == size - 1 and computed_det == 0,
                    f"even transfer cycle rank changed at size {size}")
            require(all(sum(row[column] * alternating[column]
                            for column in range(size)) == 0
                        for row in cycle),
                    f"even alternating kernel changed at size {size}")
            outcome = "one-dimensional alternating deletion kernel"
        path = signless_path(size)
        require(rank(path) == size,
                f"open transfer path lost endpoint rank at length {size}")
        records.append({
            "edges": size,
            "cycle_rank": computed_rank,
            "cycle_determinant": computed_det,
            "cycle_outcome": outcome,
            "open_path_rank": size,
            "open_path_vertices": size + 1,
        })
    return records


def matching_avoiding(vertices, forbidden):
    for matching in perfect_matchings(tuple(vertices)):
        if not (set(matching) & set(forbidden)):
            return matching
    raise RuntimeError("no avoiding matching exists")


def build_winding_guard(order):
    require(order >= 6 and order % 2 == 0,
            "winding guard needs even order at least six")
    p0 = tuple(edge(site, site + 1) for site in range(0, order, 2))
    winding = tuple(sorted(
        [edge(site, site + 1) for site in range(1, order - 1, 2)]
        + [edge(order - 1, 0)]
    ))
    shared = edge(0, 1)

    # P1 shares exactly e with P0 and avoids every winding edge elsewhere.
    tail_vertices = tuple(range(2, order))
    forbidden_tail = (set(p0) | set(winding)) - {shared}
    p1_tail = matching_avoiding(tail_vertices, forbidden_tail)
    p1 = tuple(sorted((shared,) + p1_tail))
    require(set(p0) & set(p1) == {shared},
            "the first two anchors stopped being exactly two-shared at e")

    # P2 avoids e and every displayed cell class.  The small exact chooser
    # audits existence; the uniform note invokes the standard complement
    # matching argument.
    p2 = matching_avoiding(range(order), set(p0) | set(p1) | set(winding))
    require(shared not in p2, "the third anchor acquired e")

    mixed_word = (2, 2) + (0,) * (order - 2)
    source = {}
    for colour, matching in enumerate((p0, p1, p2)):
        for left, right in matching:
            source[cell(left, right, colour, colour)] = 1
    source[cell(0, 1, 2, 2)] = 1
    for index, (left, right) in enumerate(winding):
        source[cell(left, right, mixed_word[left], mixed_word[right])] = \
            -1 if index == 0 else 1
    return p0, p1, p2, winding, mixed_word, source


def compatible_terms(order, source, word):
    output = []
    for matching in perfect_matchings(tuple(range(order))):
        labels = tuple(cell(left, right, word[left], word[right])
                       for left, right in matching)
        value = 1
        for label in labels:
            value *= source.get(label, 0)
        if value:
            output.append((value, matching, labels))
    return tuple(output)


def audit_winding_class_guard(max_order):
    records = []
    for order in range(6, max_order + 1, 2):
        p0, p1, p2, winding, mixed_word, source = build_winding_guard(order)
        for colour, selected in enumerate((p0, p1, p2)):
            terms = compatible_terms(order, source, (colour,) * order)
            require(len(terms) == 1 and terms[0][1] == selected
                    and terms[0][0] == 1,
                    f"constant fibre {colour} changed at order {order}: {terms}")
        mixed = compatible_terms(order, source, mixed_word)
        require({term[1] for term in mixed} == {p0, winding}
                and sum(term[0] for term in mixed) == 0,
                f"winding mixed binomial changed at order {order}: {mixed}")

        # C_e^2 is the pure-two hafnian on the complement of sites 0,1.
        pure_two_cofactor = []
        for tail in perfect_matchings(tuple(range(2, order))):
            labels = tuple(cell(left, right, 2, 2) for left, right in tail)
            value = 1
            for label in labels:
                value *= source.get(label, 0)
            if value:
                pure_two_cofactor.append((value, tail))
        require(not pure_two_cofactor,
                f"inactive direct cell acquired a pure-two cofactor at {order}")

        # P0 union winding is one Hamilton alternating cycle, so the mate is
        # maximally delocalized rather than a common local complement class.
        adjacency = {site: [] for site in range(order)}
        for matching in (p0, winding):
            for left, right in matching:
                adjacency[left].append(right)
                adjacency[right].append(left)
        require(all(len(neighbours) == 2 for neighbours in adjacency.values()),
                "winding union stopped being two-regular")
        seen = set()
        stack = [0]
        while stack:
            site = stack.pop()
            if site in seen:
                continue
            seen.add(site)
            stack.extend(adjacency[site])
        require(len(seen) == order,
                "winding mate stopped using every site")
        records.append({
            "sites": order,
            "shared_edge": list(edge(0, 1)),
            "mixed_fibre_terms": len(mixed),
            "mixed_fibre_sum": sum(term[0] for term in mixed),
            "pure_third_cofactor_terms": 0,
            "winding_component_sites": len(seen),
        })
    return records


def audit_six_site_first_omitted_row():
    order = 6
    _p0, _p1, _p2, _winding, mixed_word, source = build_winding_guard(order)
    defects = []
    for word in itertools.product(range(3), repeat=order):
        value = sum(term[0] for term in compatible_terms(order, source, word))
        target = int(len(set(word)) == 1)
        if value != target:
            defects.append(("".join(map(str, word)), value - target,
                            compatible_terms(order, source, word)))
    require(len(defects) == 8,
            f"the six-site winding defect count changed: {len(defects)}")
    first_word, first_value, first_terms = defects[0]
    require(first_word == "001111" and first_value == 1
            and len(first_terms) == 1,
            f"the first omitted full row changed: {defects[0]}")
    require(sum(term[0] for term in compatible_terms(order, source, mixed_word)) == 0,
            "the displayed transfer row stopped being exact")
    return {
        "defect_count": len(defects),
        "defect_words": [word for word, _value, _terms in defects],
        "first_omitted_word": first_word,
        "first_omitted_coefficient": first_value,
        "first_omitted_matching": [list(pair) for pair in first_terms[0][1]],
        "interpretation": (
            "the complete 001111 row must supply a new winding-class mate; "
            "the displayed pure fibres and one exact mixed row do not identify it"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=12)
    args = parser.parse_args()
    require(args.max_order >= 6 and args.max_order % 2 == 0,
            "--max-order must be even and at least six")
    pin_dependencies()
    ledger = {
        "common_complement_class_transfer": audit_common_class_transfer_theorem(),
        "winding_class_guard": audit_winding_class_guard(args.max_order),
        "six_site_first_omitted_row": audit_six_site_first_omitted_row(),
        "theorem": (
            "within one literal complement matching class, transfer closure "
            "is exactly a signless path/cycle: an open path exposes an "
            "endpoint, an odd cycle has determinant two, and an even cycle "
            "has the alternating anchor-safe deletion kernel"
        ),
        "obstruction": (
            "the terminal direct label and normalized pure fibres do not "
            "force its pure-third cofactor or a common transfer class.  A "
            "cancellation mate may wind through every site"
        ),
        "first_missing_source_row": (
            "at six sites the literal two-shared guard has exact normalized "
            "constant fibres and exact mixed word 220000, but the first "
            "unmet complete coefficient is the singleton word 001111"
        ),
        "scope": (
            "the winding family is a physical common-q partial-row guard, "
            "not a full GHZ source.  It proves the matching-class hypothesis "
            "load-bearing and identifies the next row; full-row propagation "
            "may still force activity/reselection"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"two-shared activity-transfer ledger changed: {digest}")
    print("uniform two-shared direct-activity transfer boundary: PASS")
    print("common class: open endpoint / odd unit / even deletion kernel")
    print("winding class: direct q_e^(m,m) remains cofactor-inactive")
    print("six-site first omitted full word: 001111")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
