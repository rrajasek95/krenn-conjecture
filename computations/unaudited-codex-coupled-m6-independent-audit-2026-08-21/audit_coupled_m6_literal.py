#!/usr/bin/env python3
"""Independent literal-source audit of the coupled-m6 column-star candidate."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_coupled_m6_literal.json"
ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
W = (Fraction(0), Fraction(1))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


# Exact Q(w), w^2+w+1=0.  No derived E2/E3/E4 formula is imported.
def qa(x, y):
    return x[0] + y[0], x[1] + y[1]


def qn(x):
    return -x[0], -x[1]


def qm(x, y):
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c - b * d


def qi(x):
    a, b = x
    norm = a * a - a * b + b * b
    require(norm != 0, x)
    return (a - b) / norm, -b / norm


def qs(x, y):
    return qm(x, qi(y))


def pa(x, y):
    answer = dict(x)
    for degree, coefficient in y.items():
        answer[degree] = qa(answer.get(degree, ZERO), coefficient)
        if answer[degree] == ZERO:
            del answer[degree]
    return answer


def pn(x):
    return {degree: qn(coefficient) for degree, coefficient in x.items()}


def pm(x, y):
    answer = {}
    for left_degree, left_coefficient in x.items():
        for right_degree, right_coefficient in y.items():
            degree = left_degree + right_degree
            value = qm(left_coefficient, right_coefficient)
            answer[degree] = qa(answer.get(degree, ZERO), value)
    return {degree: coefficient for degree, coefficient in answer.items()
            if coefficient != ZERO}


def pscale(x, coefficient):
    return {degree: qm(value, coefficient) for degree, value in x.items()
            if qm(value, coefficient) != ZERO}


def pdivmod(numerator, denominator):
    require(denominator, "zero polynomial divisor")
    remainder = dict(numerator)
    quotient = {}
    denominator_degree = max(denominator)
    denominator_lead = denominator[denominator_degree]
    while remainder and max(remainder) >= denominator_degree:
        degree = max(remainder) - denominator_degree
        coefficient = qs(remainder[max(remainder)], denominator_lead)
        quotient[degree] = qa(quotient.get(degree, ZERO), coefficient)
        remainder = pa(remainder, pn(pm({degree: coefficient}, denominator)))
    return quotient, remainder


def pgcd(left, right):
    left, right = dict(left), dict(right)
    while right:
        _quotient, remainder = pdivmod(left, right)
        left, right = right, remainder
    if not left:
        return {}
    return pscale(left, qi(left[max(left)]))


def normalize_row(row):
    nonzero = [entry for entry in row if entry]
    if not nonzero:
        return row
    common = nonzero[0]
    for entry in nonzero[1:]:
        common = pgcd(common, entry)
        if len(common) == 1 and 0 in common:
            break
    divided = []
    for entry in row:
        if not entry:
            divided.append({})
            continue
        quotient, remainder = pdivmod(entry, common)
        require(not remainder, (entry, common, remainder))
        divided.append(quotient)
    first = next(entry for entry in divided if entry)
    return [pscale(entry, qi(first[max(first)])) for entry in divided]


def row_echelon(rows):
    work = [[dict(entry) for entry in row] for row in rows]
    pivots = []
    basis_indices = []
    row_index = 0
    for column in range(9):
        pivot_index = next((index for index in range(row_index, len(work))
                            if work[index][column]), None)
        if pivot_index is None:
            continue
        work[row_index], work[pivot_index] = work[pivot_index], work[row_index]
        pivot = work[row_index][column]
        for index in range(row_index + 1, len(work)):
            coefficient = work[index][column]
            if not coefficient:
                continue
            work[index] = normalize_row([
                pa(pm(pivot, left), pn(pm(coefficient, right)))
                for left, right in zip(work[index], work[row_index], strict=True)
            ])
        pivots.append(column)
        row_index += 1
        if row_index == len(work):
            break
    # Recover a lex-first raw-row basis independently by rank increments.
    rank = row_index
    if rank:
        current = []
        for index, row in enumerate(rows):
            trial_rank = row_rank(current + [row], recover_basis=False)
            if trial_rank > len(current):
                current.append(row)
                basis_indices.append(index)
            if len(current) == rank:
                break
    return rank, tuple(pivots), tuple(basis_indices)


def row_rank(rows, recover_basis=True):
    if not rows:
        return 0
    if recover_basis:
        return row_echelon(rows)[0]
    work = [[dict(entry) for entry in row] for row in rows]
    row_index = 0
    for column in range(9):
        pivot_index = next((index for index in range(row_index, len(work))
                            if work[index][column]), None)
        if pivot_index is None:
            continue
        work[row_index], work[pivot_index] = work[pivot_index], work[row_index]
        pivot = work[row_index][column]
        for index in range(row_index + 1, len(work)):
            coefficient = work[index][column]
            if coefficient:
                work[index] = normalize_row([
                    pa(pm(pivot, left), pn(pm(coefficient, right)))
                    for left, right in zip(work[index], work[row_index], strict=True)
                ])
        row_index += 1
        if row_index == len(work):
            break
    return row_index


def determinant(matrix):
    size = len(matrix)
    state = {0: {0: ONE}}
    for row_index in range(size):
        next_state = {}
        for mask, value in state.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                inversions = sum(bool(mask & (1 << later))
                                 for later in range(column + 1, size))
                sign = -1 if inversions % 2 else 1
                term = pm(value, matrix[row_index][column])
                if sign < 0:
                    term = pn(term)
                new_mask = mask | (1 << column)
                next_state[new_mask] = pa(next_state.get(new_mask, {}), term)
        state = next_state
    return state.get((1 << size) - 1, {})


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def build_literal_source():
    source = {}

    def add(u, v, a, b, degree, coefficient):
        require(u < v, (u, v))
        key = (u, v, a, b)
        source[key] = pa(source.get(key, {}), {degree: coefficient})

    left = {
        (0, 1): ONE, (2, 3): ONE, (0, 2): ONE, (0, 3): ONE,
        (1, 3): W, (1, 2): qm(W, W),
    }
    for (u, v), coefficient in left.items():
        add(u, v, 0, 0, 0, coefficient)
    for u, v in combinations(range(4, 8), 2):
        add(u, v, 0, 0, 0, ONE)
    for i in range(4):
        for j in (4, 5, 6):
            add(i, j, 1, 0, 1, ONE)
        add(i, 4, 1, 1, 1, ONE)
        add(i, 5, 1, 1, 2, ONE)
    for u, v in ((4, 5), (6, 7)):
        add(u, v, 1, 1, 1, ONE)
    for u, v in combinations(range(4), 2):
        add(u, v, 1, 1, 2, (Fraction(-2), Fraction(0)))
    return source


def cell(source, u, v, a, b):
    return source.get((u, v, a, b), {}) if u < v else source.get((v, u, b, a), {})


def amplitude(source, word):
    answer = {}
    for matching in PM8:
        term = {0: ONE}
        for u, v in matching:
            term = pm(term, cell(source, u, v, word[u], word[v]))
            if not term:
                break
        answer = pa(answer, term)
    return answer


def response_row(source, p, q, a, b, alpha, beta):
    answer = []
    for i in range(3):
        for j in range(3):
            first = pm(cell(source, p, a, i, alpha),
                       cell(source, q, b, j, beta))
            second = pm(cell(source, p, b, i, beta),
                        cell(source, q, a, j, alpha))
            answer.append(pa(first, second))
    return answer


def leading(polynomial):
    if not polynomial:
        return None
    degree = min(polynomial)
    coefficient = polynomial[degree]
    return degree, [str(coefficient[0]), str(coefficient[1])]


def word_string(word):
    return "".join(map(str, word))


def build():
    source = build_literal_source()
    amplitudes = {word: amplitude(source, word)
                  for word in product(range(3), repeat=8)}
    nonzero = {word: polynomial for word, polynomial in amplitudes.items()
               if polynomial}
    mixed = {word: polynomial for word, polynomial in nonzero.items()
             if len(set(word)) > 1}
    omitted = []
    for word, polynomial in sorted(mixed.items()):
        for degree, coefficient in sorted(polynomial.items()):
            if degree in (4, 5):
                omitted.append((word, degree, coefficient))
    mixed_below6 = [(word, degree, coefficient)
                    for word, polynomial in sorted(mixed.items())
                    for degree, coefficient in sorted(polynomial.items())
                    if degree < 6]

    # Independently recover exactly the base-active rank-zero carriers, then
    # audit all four blocker memberships over Q(w)(t).  A nonzero augmented
    # minor is a literal leading obstruction to membership.
    carrier_records = []
    for p, q in combinations(range(8), 2):
        direct = [cell(source, p, q, i, j) for i in range(3) for j in range(3)]
        direct0 = [{0: value.get(0, ZERO)} if value.get(0, ZERO) != ZERO else {}
                   for value in direct]
        if not any(direct0):
            continue
        residual = tuple(site for site in range(8) if site not in (p, q))
        carriers = []
        for centre in residual:
            carriers.append(("star", f"star:pq={p}{q}:centre={centre}",
                             [edge for edge in combinations(residual, 2)
                              if centre not in edge]))
        for triangle in combinations(residual, 3):
            allowed = set(combinations(triangle, 2))
            carriers.append(("triangle",
                             f"triangle:pq={p}{q}:sites={''.join(map(str, triangle))}",
                             [edge for edge in combinations(residual, 2)
                              if edge not in allowed]))
        for kind, label, edges in carriers:
            rows = []
            row_labels = []
            for a, b in edges:
                for alpha in range(3):
                    for beta in range(3):
                        rows.append(response_row(source, p, q, a, b, alpha, beta))
                        row_labels.append(f"{a}{b}:{alpha}{beta}")
            base_rows = [[{0: entry.get(0, ZERO)}
                          if entry.get(0, ZERO) != ZERO else {}
                          for entry in row] for row in rows]
            if row_rank(base_rows) != 0:
                continue
            rank, pivot_columns, basis_indices = row_echelon(rows)
            blockers = []
            for colour in range(3):
                row = [{} for _ in range(9)]
                row[3 * colour + colour] = {0: ONE}
                blockers.append((f"K{colour}{colour}", row))
            blockers.append(("direct", direct))
            memberships = []
            raw_basis = [rows[index] for index in basis_indices]
            for blocker_name, blocker in blockers:
                augmented_rank, augmented_pivots, _indices = row_echelon(
                    raw_basis + [blocker])
                member = augmented_rank == rank
                witness = None
                if not member:
                    columns = augmented_pivots
                    matrix = [[row[column] for column in columns]
                              for row in raw_basis + [blocker]]
                    minor = determinant(matrix)
                    require(minor, (label, blocker_name, columns))
                    witness = {
                        "columns": list(columns),
                        "leading": leading(minor),
                    }
                memberships.append({
                    "blocker": blocker_name,
                    "in_response_rowspace": member,
                    "augmented_rank": augmented_rank,
                    "witness_minor": witness,
                })
            carrier_records.append({
                "kind": kind,
                "label": label,
                "response_rank_over_Qw_t": rank,
                "lex_basis_row_labels": [row_labels[index]
                                         for index in basis_indices],
                "pivot_columns": list(pivot_columns),
                "blockers": memberships,
                "remains_active": not any(row["in_response_rowspace"]
                                          for row in memberships),
            })
    require(len(carrier_records) == 72, len(carrier_records))
    blocker_membership_histogram = Counter(
        (record["kind"], row["blocker"], row["in_response_rowspace"])
        for record in carrier_records for row in record["blockers"]
    )
    active = [record["label"] for record in carrier_records
              if record["remains_active"]]

    lex_mixed = min(mixed_below6, key=lambda row: (row[1], row[0])) \
        if mixed_below6 else None
    lex_omitted = min(omitted, key=lambda row: (row[0], row[1])) \
        if omitted else None
    result = {
        "status": "PASS independent literal coupled-m6 audit",
        "literal_source": {
            "nonzero_cells": len(source),
            "cell_terms": sum(len(polynomial) for polynomial in source.values()),
            "field": "Q(w), w^2+w+1=0",
            "source_rows_rebuilt": True,
            "derived_E2_E3_E4_imported": False,
        },
        "amplitude_replay": {
            "all_words_tested": len(amplitudes),
            "nonzero_word_polynomials": len(nonzero),
            "nonzero_mixed_word_polynomials": len(mixed),
            "order4_omitted_nonzero_coefficients": sum(degree == 4
                                                       for _word, degree, _c in omitted),
            "order5_omitted_nonzero_coefficients": sum(degree == 5
                                                       for _word, degree, _c in omitted),
            "mixed_nonzero_coefficients_below_order6": len(mixed_below6),
            "lex_first_mixed_below_order6": None if lex_mixed is None else {
                "word": word_string(lex_mixed[0]),
                "degree": lex_mixed[1],
                "coefficient": [str(lex_mixed[2][0]), str(lex_mixed[2][1])],
            },
            "lex_first_omitted_order4_5": None if lex_omitted is None else {
                "word": word_string(lex_omitted[0]),
                "degree": lex_omitted[1],
                "coefficient": [str(lex_omitted[2][0]), str(lex_omitted[2][1])],
            },
            "mixed_below_order6_packet": [
                {"word": word_string(word), "degree": degree,
                 "coefficient": [str(coefficient[0]), str(coefficient[1])]}
                for word, degree, coefficient in mixed_below6
            ],
            "omitted_order4_5_packet": [
                {"word": word_string(word), "degree": degree,
                 "coefficient": [str(coefficient[0]), str(coefficient[1])]}
                for word, degree, coefficient in omitted
            ],
            "pure_word_polynomials": {
                word_string(word): {str(degree): [str(value[0]), str(value[1])]
                                    for degree, value in sorted(amplitudes[word].items())}
                for word in ((0,) * 8, (1,) * 8, (2,) * 8)
            },
        },
        "carrier_replay": {
            "base_active_rank_zero_carriers": len(carrier_records),
            "kind_histogram": dict(sorted(Counter(row["kind"]
                                                   for row in carrier_records).items())),
            "generic_response_rank_histogram": {
                f"{kind}:rank{rank}": count for (kind, rank), count in sorted(
                    Counter((row["kind"], row["response_rank_over_Qw_t"])
                            for row in carrier_records).items())
            },
            "blocker_membership_histogram": {
                f"{kind}:{blocker}:member={member}": count
                for (kind, blocker, member), count
                in sorted(blocker_membership_histogram.items())
            },
            "carriers_remaining_active_over_Qw_t": len(active),
            "active_labels": active,
            "records": carrier_records,
        },
        "verdict": (
            "OBSTRUCTED by lex-first mixed coefficient below order 6"
            if lex_mixed else
            ("OBSTRUCTED by persistent active carrier"
             if active else "PASSES audited literal rows and blocker memberships")
        ),
        "scope": (
            "The blocker audit is exact over Q(w)(t) for all 72 carriers that "
            "are active rank-zero at the frozen base, using the three Kdd "
            "blockers and the literal direct-pair blocker."
        ),
    }
    return result


def main(write_results=False):
    result = build()
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": logical,
        "amplitude_replay": {key: value for key, value
                             in result["amplitude_replay"].items()
                             if key not in {"omitted_order4_5_packet",
                                            "mixed_below_order6_packet"}},
        "carrier_replay": {key: value for key, value
                           in result["carrier_replay"].items()
                           if key not in {"records", "active_labels"}},
        "verdict": result["verdict"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
