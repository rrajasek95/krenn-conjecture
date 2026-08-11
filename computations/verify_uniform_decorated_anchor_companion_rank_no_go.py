#!/usr/bin/env python3
"""All companion rows preserve the wrong endpoint label on an anchor edge.

For a fixed decorated cell q_uv^{ij}, every full-output row using that cell
has endpoint colours i,j, independently of the common colour on the other
sites.  Avoiding matching mates can change physical partners but retain
those endpoint rows.  Hence the full family of same-cell companion rows
cannot repair a missing pure-k column at an endpoint where k differs from
the corresponding decoration label.

The checker freezes a six-site, three-companion-row guard entirely inside
the union of three selected pure matchings.  All three complete rows cancel,
yet deleting the decorated Q0 edge has ranks (2,3).  This is a source-row
guard, not a full GHZ source.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
}
EXPECTED_LEDGER_SHA256 = "ae38d44b325daa78b1aedb3774c7ace31392c20fb6461d2f4c4a305b7f3af685"


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


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def coefficient_terms(source, word):
    terms = []
    for matching in perfect_matchings(range(len(word))):
        labels = tuple(cell(left, right, word[left], word[right])
                       for left, right in matching)
        value = Q(1)
        for label in labels:
            value *= source.get(label, Q(0))
        if value:
            terms.append((value, labels))
    return tuple(terms)


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    pivot_row = 0
    if not matrix:
        return 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value
                             for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


PURE_MATCHINGS = {
    0: (edge(0, 1), edge(2, 3), edge(4, 5)),
    1: (edge(0, 2), edge(1, 3), edge(4, 5)),
    2: (edge(0, 3), edge(1, 2), edge(4, 5)),
}
ANCHOR_UNION = set().union(*map(set, PURE_MATCHINGS.values()))


def build_guard():
    source = {
        # Three pure target matchings.
        cell(0, 1, 0, 0): Q(1),
        cell(2, 3, 0, 0): Q(1),
        cell(4, 5, 0, 0): Q(1),
        cell(0, 2, 1, 1): Q(1),
        cell(1, 3, 1, 1): Q(1),
        cell(4, 5, 1, 1): Q(1),
        cell(0, 3, 2, 2): Q(1),
        cell(1, 2, 2, 2): Q(1),
        cell(4, 5, 2, 2): Q(1),
        # Decorated Q0 edge e=01 with endpoint labels (1,0).
        cell(0, 1, 1, 0): Q(1),
        # Complete avoiding mate for rest colour 0.
        cell(0, 2, 1, 0): Q(1),
        cell(1, 3, 0, 0): Q(-1),
        # Complete avoiding mate for rest colour 1.
        cell(2, 3, 1, 1): Q(1),
        cell(1, 3, 0, 1): Q(-1),
        # Complete avoiding mate for rest colour 2.
        cell(2, 3, 2, 2): Q(1),
        cell(0, 3, 1, 2): Q(1),
        cell(1, 2, 0, 2): Q(-1),
    }
    return source


def audit_three_complete_companion_rows(source):
    records = []
    for rest_colour in range(3):
        word = (1, 0) + (rest_colour,) * 4
        terms = coefficient_terms(source, word)
        require(len(terms) == 2 and sum(term[0] for term in terms) == 0,
                f"companion row {word} stopped being a complete binomial: {terms}")
        through = tuple(term for term in terms
                        if edge(0, 1) in {label[:2] for label in term[1]})
        avoiding = tuple(term for term in terms
                         if edge(0, 1) not in {label[:2] for label in term[1]})
        require(len(through) == len(avoiding) == 1,
                f"companion row {word} lost its through/avoiding split")
        records.append({
            "word": "".join(map(str, word)),
            "term_coefficients": [str(term[0]) for term in terms],
            "through_matching": [list(label[:2]) for label in through[0][1]],
            "avoiding_matching": [list(label[:2]) for label in avoiding[0][1]],
        })
    return records


def endpoint_star_rank(source, endpoint):
    # Delete e=01.  Rows are the endpoint colours; columns are literal
    # (neighbour, neighbour-colour) coordinates.
    columns = []
    for label, value in source.items():
        if not value:
            continue
        left, right, left_colour, right_colour = label
        if edge(left, right) == edge(0, 1):
            continue
        if left == endpoint:
            columns.append((left_colour, (right, right_colour)))
        elif right == endpoint:
            columns.append((right_colour, (left, left_colour)))
    coordinate_labels = sorted({column for _, column in columns})
    matrix = []
    for row in range(3):
        entries = []
        for coordinate in coordinate_labels:
            entries.append(sum(
                source[label]
                for label in source
                if edge(label[0], label[1]) != edge(0, 1)
                and ((label[0] == endpoint
                      and label[2] == row
                      and (label[1], label[3]) == coordinate)
                     or (label[1] == endpoint
                         and label[3] == row
                         and (label[0], label[2]) == coordinate))
            ))
        matrix.append(entries)
    computed = rank(matrix)
    nonzero_rows = [row for row, entries in enumerate(matrix) if any(entries)]
    require(computed == len(nonzero_rows),
            "the guard acquired a dependence among its nonzero endpoint rows")
    return computed, nonzero_rows, columns


def audit_rank_boundary(source):
    left_rank, left_rows, left_columns = endpoint_star_rank(source, 0)
    right_rank, right_rows, right_columns = endpoint_star_rank(source, 1)
    require((left_rank, right_rank) == (2, 3),
            f"the all-companion guard rank profile changed: {(left_rank,right_rank)}")
    require(left_rows == [1, 2] and right_rows == [0, 1, 2],
            "the missing endpoint target row changed")
    return {
        "deleted_pair": [0, 1],
        "ranks": [left_rank, right_rank],
        "left_rows": left_rows,
        "right_rows": right_rows,
        "left_literal_columns": [[row, list(column)]
                                  for row, column in left_columns],
        "right_literal_columns": [[row, list(column)]
                                   for row, column in right_columns],
        "missing": "pure-0 row at endpoint 0",
    }


def audit_anchor_containment(source):
    support_pairs = {edge(label[0], label[1]) for label in source}
    require(support_pairs <= ANCHOR_UNION,
            f"the guard acquired an off-anchor pair: {support_pairs-ANCHOR_UNION}")
    pure_values = {}
    for colour in range(3):
        word = (colour,) * 6
        value = sum(term[0] for term in coefficient_terms(source, word))
        require(value == 1,
                f"pure target {colour} changed in the guard: {value}")
        pure_values[str(colour)] = str(value)
    return {
        "anchor_union": [list(pair) for pair in sorted(ANCHOR_UNION)],
        "support_physical_pairs": [list(pair) for pair in sorted(support_pairs)],
        "pure_target_coefficients": pure_values,
    }


def audit_label_invariance():
    records = []
    for left_colour, right_colour in itertools.permutations(range(3), 2):
        for rest_colour in range(3):
            word = (left_colour, right_colour) + (rest_colour,) * 4
            for matching in perfect_matchings(range(6)):
                if edge(0, 1) in matching:
                    continue
                left_mate = next(pair[1] if pair[0] == 0 else pair[0]
                                 for pair in matching if 0 in pair)
                right_mate = next(pair[1] if pair[0] == 1 else pair[0]
                                  for pair in matching if 1 in pair)
                require(word[0] == left_colour and word[1] == right_colour,
                        "an avoiding companion changed an endpoint label")
                records.append((left_colour, right_colour, rest_colour,
                                left_mate, right_mate))
    require(len(records) == 216,
            f"the all-colour companion-label census changed: {len(records)}")
    return {
        "audited_avoiding_matchings": len(records),
        "invariant": (
            "for every rest colour and every avoiding matching, endpoint "
            "rows remain the fixed decoration labels (i,j)"
        ),
    }


def main():
    pin_dependencies()
    source = build_guard()
    ledger = {
        "complete_companion_rows": audit_three_complete_companion_rows(source),
        "anchor_containment": audit_anchor_containment(source),
        "deleted_star_boundary": audit_rank_boundary(source),
        "uniform_label_invariance": audit_label_invariance(),
        "theorem": (
            "all companion rows of one decorated cell preserve its two "
            "endpoint labels.  They cannot repair a missing pure-k row at "
            "an endpoint whose decoration label differs from k"
        ),
        "sharp_guard": (
            "at six sites all three complete rest-colour rows cancel using "
            "only selected-anchor physical pairs, while the decorated Q0 "
            "edge retains deleted ranks (2,3)"
        ),
        "next_source_input": (
            "a pure-k matching reselected away from the edge, an off-anchor "
            "escape, or a genuinely new direct cell whose endpoint label "
            "is k at the deficient endpoint; another tail of q_e^{ij} "
            "cannot suffice"
        ),
        "scope": (
            "complete three-row source guard and uniform rank no-go, not a "
            "full GHZ source; other mixed output rows of the guard need not vanish"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"decorated-anchor companion ledger changed: {digest}")
    print("uniform decorated-anchor companion-rank no-go: PASS")
    print("all three complete companion rows cancel inside the anchor union")
    print("deleted decorated Q0 edge retains ranks (2,3)")
    print("same-cell companions cannot supply the missing endpoint row")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
