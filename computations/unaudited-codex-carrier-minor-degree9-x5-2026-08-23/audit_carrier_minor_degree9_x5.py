#!/usr/bin/env python3
"""Exact fine-graded degree-9 X5 membership test for one carrier minor."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import permutations
import json
from math import gcd, lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_carrier_minor_degree9_x5.json"
SITES = tuple(range(8))
COLOURS = tuple(range(3))
T_EDGES = ((0, 1), (0, 2), (1, 2))
CAP_ROWS = ((0, 1), (1, 1), (2, 1))
WORDS = (
    (0, 0, 0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 0, 0, 1, 1),
    (0, 0, 0, 0, 0, 0, 2, 1),
)
OUTSIDE_DIR = (1, 1, 2, 2, 2, 2, 2, 2)
TARGET_SHA256 = "dae00b5e44a807a407571a8a12a73017f6ce0cc0b60ac43a8f027282a15a5965"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position in range(1, len(vertices)):
        v = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(SITES))
require(len(MATCHINGS) == 105, len(MATCHINGS))


def cell(u, v, a, b):
    return (u, v, a, b) if u < v else (v, u, b, a)


def monomial_text(monomial):
    return "*".join(f"A{u}{v}_{a}{b}" for u, v, a, b in monomial)


def word_text(word):
    return "".join(map(str, word))


def matching_monomial(matching, word, omitted=None):
    return tuple(sorted(cell(u, v, word[u], word[v])
                        for u, v in matching if (u, v) != omitted))


def amplitude(word):
    return Counter(matching_monomial(matching, word) for matching in MATCHINGS)


def cofactor(word, edge):
    return Counter(matching_monomial(matching, word, edge)
                   for matching in MATCHINGS if edge in matching)


def poly_add(left, right, scale=1):
    out = Counter(left)
    for monomial, coefficient in right.items():
        out[monomial] += scale * coefficient
        if not out[monomial]:
            del out[monomial]
    return out


def poly_mul(left, right):
    out = Counter()
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] += coefficient_left * coefficient_right
            if not out[monomial]:
                del out[monomial]
    return out


def determinant(rows):
    out = Counter()
    for permutation in permutations(range(3)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(3) for j in range(i + 1, 3))
        term = Counter({(): -1 if inversions % 2 else 1})
        for row, column in enumerate(permutation):
            term = poly_mul(term, rows[row][column])
        out = poly_add(out, term)
    return out


def target_minor():
    rows = []
    for cap_pair in CAP_ROWS:
        word = (0,) * 6 + cap_pair
        rows.append(tuple(cofactor(word, edge) for edge in T_EDGES))
    target = determinant(tuple(rows))
    require(target, "carrier minor vanished")
    require(set(map(len, target)) == {9}, set(map(len, target)))
    return target


def fine_weight_of_monomial(monomial):
    weight = [[0, 0, 0] for _ in SITES]
    for u, v, a, b in monomial:
        weight[u][a] += 1
        weight[v][b] += 1
    return tuple(tuple(row) for row in weight)


def target_weight():
    return (
        (1, 0, 0), (1, 0, 0), (1, 0, 0),
        (3, 0, 0), (3, 0, 0), (3, 0, 0),
        (1, 1, 1), (0, 3, 0),
    )


def multiplier_ports(word):
    target = target_weight()
    ports = []
    for site in SITES:
        for colour in COLOURS:
            count = target[site][colour] - int(word[site] == colour)
            require(count >= 0, (word, site, colour, count))
            ports.extend([(site, colour)] * count)
    require(len(ports) == 10, (word, ports))
    return tuple(sorted(ports))


def multiplier_monomials(word):
    ports = multiplier_ports(word)
    answer = set()

    def recurse(remaining, chosen):
        if not remaining:
            answer.add(tuple(sorted(chosen)))
            return
        left = remaining[0]
        used = set()
        for index in range(1, len(remaining)):
            right = remaining[index]
            if right[0] == left[0] or right in used:
                continue
            used.add(right)
            rest = remaining[1:index] + remaining[index + 1:]
            recurse(rest, chosen + (cell(left[0], right[0], left[1], right[1]),))

    recurse(ports, ())
    require(answer, word)
    require(all(len(monomial) == 5 for monomial in answer), word)
    expected = tuple(tuple(target_weight()[site][colour]
                           - int(word[site] == colour)
                           for colour in COLOURS) for site in SITES)
    require(all(fine_weight_of_monomial(monomial) == expected
                for monomial in answer), (word, expected))
    return tuple(sorted(answer))


def translated_rows():
    rows = []
    counts = {}
    for word in WORDS:
        generator = amplitude(word)
        multipliers = multiplier_monomials(word)
        counts[word_text(word)] = len(multipliers)
        for multiplier in multipliers:
            row = Counter({tuple(sorted(monomial + multiplier)): coefficient
                           for monomial, coefficient in generator.items()})
            require(set(map(len, row)) == {9}, (word, multiplier))
            rows.append((word, multiplier, row))
    return rows, counts


def exact_echelon(labelled_rows):
    basis = {}
    provenance = {}
    for label_index, (_, _, raw) in enumerate(labelled_rows):
        row = {monomial: Fraction(value) for monomial, value in raw.items()
               if value}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {column: value / scale for column, value in row.items()}
                basis[pivot] = row
                provenance[pivot] = label_index
                break
            scale = row[pivot]
            for column, value in basis[pivot].items():
                row[column] = row.get(column, Fraction(0)) - scale * value
                if not row[column]:
                    del row[column]
    return basis, provenance


def reduce_row(raw, basis):
    row = {monomial: Fraction(value) for monomial, value in raw.items() if value}
    while row:
        pivot = min(row)
        if pivot not in basis:
            break
        scale = row[pivot]
        for column, value in basis[pivot].items():
            row[column] = row.get(column, Fraction(0)) - scale * value
            if not row[column]:
                del row[column]
    return row


def integer_separator(rows, target, basis, remainder):
    free = min(remainder)
    functional = {free: Fraction(1)}
    for pivot in sorted(basis, reverse=True):
        value = -sum(coefficient * functional.get(column, Fraction(0))
                     for column, coefficient in basis[pivot].items()
                     if column != pivot)
        if value:
            functional[pivot] = value
    require(all(sum(Fraction(coefficient) * functional.get(column, 0)
                        for column, coefficient in row.items()) == 0
                for _, _, row in rows), "separator misses a translated row")
    pairing = sum(Fraction(coefficient) * functional.get(column, 0)
                  for column, coefficient in target.items())
    require(pairing, pairing)
    denominator = reduce(lcm, (value.denominator for value in functional.values()), 1)
    integer = {column: int(value * denominator)
               for column, value in functional.items() if value}
    common = reduce(gcd, (abs(value) for value in integer.values()))
    integer = {column: value // common for column, value in integer.items()}
    integer_pairing = sum(coefficient * integer.get(column, 0)
                          for column, coefficient in target.items())
    require(integer_pairing, integer_pairing)
    require(all(sum(coefficient * integer.get(column, 0)
                        for column, coefficient in row.items()) == 0
                for _, _, row in rows), "integer separator misses row")
    return integer, integer_pairing


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-target", action="store_true")
    args = parser.parse_args()
    target = target_minor()
    expected_weight = target_weight()
    require({fine_weight_of_monomial(monomial) for monomial in target}
            == {expected_weight}, "target fine grade")
    rows, multiplier_counts = translated_rows()
    row_columns = set()
    for _, _, row in rows:
        row_columns.update(row)
    all_columns = set(target) | row_columns
    basis, provenance = exact_echelon(rows)
    if args.mutate_target:
        first = min(target)
        target[first] += 1
    target_digest = sha256(json.dumps(
        [(monomial_text(monomial), coefficient)
         for monomial, coefficient in sorted(target.items())],
        separators=(",", ":")
    ).encode()).hexdigest()
    require(target_digest == TARGET_SHA256, (target_digest, TARGET_SHA256))
    remainder = reduce_row(target, basis)
    if remainder:
        private_columns = sorted(set(target) - row_columns)
        unit_private = next((column for column in private_columns
                             if abs(target[column]) == 1), None)
        if unit_private is not None:
            separator = {unit_private: target[unit_private]}
            pairing = 1
        else:
            separator, pairing = integer_separator(rows, target, basis, remainder)
        separator_entries = [
            {"monomial": monomial_text(monomial), "coefficient": coefficient}
            for monomial, coefficient in sorted(separator.items())
        ]
        separator_digest = sha256(json.dumps(
            separator_entries, sort_keys=True, separators=(",", ":")
        ).encode()).hexdigest()
        verdict = "NONMEMBER"
    else:
        separator_entries = []
        separator_digest = None
        pairing = 0
        verdict = "MEMBER"
        private_columns = []
    payload = {
        "status": f"PASS exact degree-9 carrier minor X5 test: {verdict}",
        "target": {
            "triangle": [0, 1, 2],
            "columns": ["01", "02", "12"],
            "residual_colour": 0,
            "cap_rows": ["01", "11", "21"],
            "degree": 9,
            "terms": len(target),
            "sha256": target_digest,
            "fine_weight": [list(row) for row in expected_weight],
        },
        "candidate_X5_words": [word_text(word) for word in WORDS],
        "multiplier_counts": multiplier_counts,
        "translated_rows": len(rows),
        "translated_row_columns": len(row_columns),
        "target_row_column_intersection": len(set(target) & row_columns),
        "target_private_columns": len(private_columns),
        "distinct_columns": len(all_columns),
        "exact_row_rank": len(basis),
        "target_remainder_terms": len(remainder),
        "target_in_degree9_X5_span": not remainder,
        "integer_separator": {
            "support": len(separator_entries),
            "target_pairing": pairing,
            "minimum_coefficient": min((entry["coefficient"]
                                        for entry in separator_entries), default=0),
            "maximum_coefficient": max((entry["coefficient"]
                                        for entry in separator_entries), default=0),
            "sha256": separator_digest,
            "entries": separator_entries,
        },
        "scope": (
            "Exhaustive fine-site-colour homogeneous degree-9 test. Exactly three "
            "mixed X5 word rows can enter this grade, and every degree-5 monomial "
            "multiplier with the complementary port degree is included. Pure "
            "normalization rows have incompatible fine degree. Nonmembership here "
            "does not exclude higher-degree/radical consequences."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    require(verdict == "NONMEMBER" and len(separator_entries) == 1
            and pairing == 1, (verdict, separator_entries, pairing))
    if args.write_results:
        HERE.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("rows/columns/rank", len(rows), len(all_columns), len(basis))
    print("multipliers", multiplier_counts)
    print("remainder/separator", len(remainder), len(separator_entries), pairing)
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
