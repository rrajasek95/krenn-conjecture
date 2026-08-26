#!/usr/bin/env python3
"""Exact-Q separator for the full closure22 + profile-(7,1) terminal block."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
import argparse
import json
import sys


ROOT = Path(__file__).resolve().parents[2]
FINE = ROOT / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
if str(FINE) not in sys.path:
    sys.path.insert(0, str(FINE))

from audit_closure22_joint_semigroup import projected_word
from audit_colour_holonomy_quotients import (
    PM8, key_add, matching_term, semigroup_key,
)
from audit_physical_graph_quotient import holonomy


UPSTREAM = FINE / "results_closure22_plus_full_profile71_joint_cegar_rust_p32003.json"
EXPECTED_UPSTREAM_SHA256 = "fa12b6726b7dbc7f448f860d6afc6ea0dd870d1dff0c2604712d4e9f513d7d0d"
SECOND_UPSTREAM = FINE / "results_closure22_plus_full_profile71_joint_cegar_rust_p32009.json"
EXPECTED_SECOND_UPSTREAM_SHA256 = "d03211f12cac5cd713f620a22024c5e9bf925d29f3809800897d19c2c393f163"
INDEPENDENT_DUAL = FINE / "results_closure22_plus_full_profile71_rational_dual.json"
EXPECTED_INDEPENDENT_DUAL_SHA256 = "5569880fe23ad93dceb2c47ecc85b36291e49925d05f8d7876e94bd3b7e71894"
EXPECTED_LOGICAL_SHA256 = "6a8e00fa771a76b1479fa9eba236dbcb3393450b2aa459c91af5e0aeac9fb69e"
AUDIT_PRIMES = (31991, 32003, 32009, 32749, 65521, 1000003, 1073741827)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def label(word):
    return "".join(map(str, word))


def subtract(left, right):
    difference = tuple(a - b for a, b in zip(left, right, strict=True))
    return difference if min(difference) >= 0 else None


def restricted_rows(source_words, support):
    support_index = {column: index for index, column in enumerate(support)}
    rows = set()
    translations_examined = 0
    for word_label in source_words:
        generator = projected_word(tuple(map(int, word_label)))
        translations = set()
        for column in support:
            for term in generator:
                difference = subtract(column, term)
                if difference is not None:
                    translations.add(difference)
        translations_examined += len(translations)
        for translation in translations:
            row = tuple(sorted(
                (support_index[column], coefficient)
                for term, coefficient in generator.items()
                if (column := key_add(translation, term)) in support_index
            ))
            if row:
                rows.add(row)
    return sorted(rows), translations_examined


def target_vector(support):
    support_index = {column: index for index, column in enumerate(support)}
    target = [0] * len(support)
    cone = semigroup_key(matching_term((0,) * 8, PM8[0]))
    for term, coefficient in holonomy().items():
        column = key_add(cone, semigroup_key(term))
        if column in support_index:
            target[support_index[column]] += coefficient
    return target


def modular_basis(rows, prime, return_selection=False):
    basis = {}
    selected = []
    for row_index, frozen_row in enumerate(rows):
        row = {
            column: coefficient % prime
            for column, coefficient in frozen_row if coefficient % prime
        }
        while row:
            pivot = min(row)
            if pivot not in basis:
                inverse = pow(row[pivot], prime - 2, prime)
                row = {
                    column: coefficient * inverse % prime
                    for column, coefficient in row.items() if coefficient % prime
                }
                basis[pivot] = row
                selected.append(row_index)
                break
            scale = row[pivot]
            for column, coefficient in basis[pivot].items():
                value = (row.get(column, 0) - scale * coefficient) % prime
                if value:
                    row[column] = value
                elif column in row:
                    del row[column]
    return (basis, selected) if return_selection else basis


def exact_null_vector(rows, selected_rows, column_count):
    basis = {}
    for row_index in selected_rows:
        row = {
            column: Fraction(coefficient)
            for column, coefficient in rows[row_index] if coefficient
        }
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {
                    column: coefficient / scale
                    for column, coefficient in row.items() if coefficient
                }
                basis[pivot] = row
                break
            scale = row[pivot]
            for column, coefficient in basis[pivot].items():
                value = row.get(column, Fraction(0)) - scale * coefficient
                if value:
                    row[column] = value
                elif column in row:
                    del row[column]
        else:
            raise RuntimeError("modularly independent row became dependent over Q")
    free_columns = sorted(set(range(column_count)) - set(basis))
    require(len(free_columns) == 1, free_columns)
    vector = [Fraction(0) for _ in range(column_count)]
    vector[free_columns[0]] = 1
    for pivot in sorted(basis, reverse=True):
        vector[pivot] = -sum(
            coefficient * vector[column]
            for column, coefficient in basis[pivot].items()
            if column != pivot
        )
    return vector, basis, free_columns[0]


def lcm(left, right):
    return abs(left * right) // gcd(left, right)


def primitive_integer_vector(vector):
    denominator = reduce(lcm, (value.denominator for value in vector), 1)
    integer = [
        value.numerator * (denominator // value.denominator)
        for value in vector
    ]
    common = reduce(gcd, (abs(value) for value in integer if value), 0)
    integer = [value // common for value in integer]
    return integer, denominator, common


def run_audit():
    upstream_bytes = UPSTREAM.read_bytes()
    upstream_hash = sha256(upstream_bytes).hexdigest()
    require(upstream_hash == EXPECTED_UPSTREAM_SHA256,
            (upstream_hash, EXPECTED_UPSTREAM_SHA256))
    upstream = json.loads(upstream_bytes)
    second_bytes = SECOND_UPSTREAM.read_bytes()
    second_hash = sha256(second_bytes).hexdigest()
    require(second_hash == EXPECTED_SECOND_UPSTREAM_SHA256,
            (second_hash, EXPECTED_SECOND_UPSTREAM_SHA256))
    second = json.loads(second_bytes)
    shape_fields = (
        "round", "rank_before", "crossing_candidates",
        "independent_rows_added", "rank_after",
    )
    first_shape = [tuple(record[field] for field in shape_fields)
                   for record in upstream["rounds"]]
    second_shape = [tuple(record[field] for field in shape_fields)
                    for record in second["rounds"]]
    require(first_shape == second_shape, "p32003/p32009 terminal shape changed")
    require((second["prime"], second["final_rank"],
             second["terminal_modular_dual_support"]) == (32009, 314887, 196),
            (second["prime"], second["final_rank"],
             second["terminal_modular_dual_support"]))
    source_words = upstream["source_words"]
    require(len(source_words) == len(set(source_words)) == 62, len(source_words))
    orbit = {
        label(word) for word in product(range(3), repeat=8)
        if sorted(word.count(colour) for colour in set(word)) == [1, 7]
    }
    require(len(orbit) == 48 and orbit <= set(source_words),
            (len(orbit), sorted(orbit - set(source_words))))
    require(upstream["added_complete_profile71_orbit"], upstream)
    require(upstream["terminal"] == "no existing-word exchange row crosses separator",
            upstream["terminal"])
    require(not upstream["target_reduced_to_zero"], upstream)

    support = sorted(tuple(record["column"])
                     for record in upstream["terminal_integer_dual"])
    require(len(support) == len(set(support)) == 196, len(support))
    rows, translations_examined = restricted_rows(source_words, support)
    require(len(rows) <= 1024 and len(support) <= 256,
            (len(rows), len(support), "hard exact gate exceeded"))
    require(len(rows) == 387, len(rows))
    require(max(map(len, rows)) == 9, max(map(len, rows)))
    target = target_vector(support)
    require([(index, value) for index, value in enumerate(target) if value]
            == [(191, 1), (193, 2), (195, 2)], target)

    modular_ranks = {}
    target_row = tuple((index, value) for index, value in enumerate(target) if value)
    for prime in AUDIT_PRIMES:
        row_rank = len(modular_basis(rows, prime))
        augmented_rank = len(modular_basis(rows + [target_row], prime))
        modular_ranks[str(prime)] = [row_rank, augmented_rank]
    require(set(map(tuple, modular_ranks.values())) == {(195, 196)}, modular_ranks)

    modular, selected = modular_basis(rows, 32003, return_selection=True)
    require(len(modular) == len(selected) == 195, len(modular))
    rational, exact_basis, free_column = exact_null_vector(rows, selected, len(support))
    require(len(exact_basis) == 195, len(exact_basis))
    require(not any(
        sum(Fraction(coefficient) * rational[column]
            for column, coefficient in row)
        for row in rows
    ), "rational separator failed an exact row")
    rational_target_pairing = sum(
        coefficient * rational[column]
        for column, coefficient in enumerate(target)
    )
    require(rational_target_pairing == 1, rational_target_pairing)

    integer, cleared_denominator, cleared_gcd = primitive_integer_vector(rational)
    integer_target_pairing = sum(
        coefficient * integer[column]
        for column, coefficient in enumerate(target)
    )
    if integer_target_pairing < 0:
        integer = [-value for value in integer]
        integer_target_pairing *= -1
    row_pairings = [
        sum(coefficient * integer[column] for column, coefficient in row)
        for row in rows
    ]
    require(not any(row_pairings), Counter(row_pairings))
    require((min(integer), max(integer), integer_target_pairing) == (-8, 8, 2),
            (min(integer), max(integer), integer_target_pairing))
    vector_digest = sha256(json.dumps(
        integer, separators=(",", ":")
    ).encode()).hexdigest()
    require(vector_digest ==
            "f7305b89a68af92f9440bc75cc2fcca251e8e90fed10963f8e3ce33ca5566243",
            vector_digest)

    independent_bytes = INDEPENDENT_DUAL.read_bytes()
    independent_hash = sha256(independent_bytes).hexdigest()
    require(independent_hash == EXPECTED_INDEPENDENT_DUAL_SHA256,
            (independent_hash, EXPECTED_INDEPENDENT_DUAL_SHA256))
    independent = json.loads(independent_bytes)
    require(independent["dual"] == [
        {"column": list(column), "coefficient": coefficient}
        for column, coefficient in zip(support, integer, strict=True)
        if coefficient
    ], "independent exact dual differs")
    require(independent["target_pairing"] == integer_target_pairing == 2,
            independent["target_pairing"])

    mutated = list(integer)
    mutated[0] += 1
    mutated_nonzero_rows = sum(
        sum(coefficient * mutated[column] for column, coefficient in row) != 0
        for row in rows
    )
    require(mutated_nonzero_rows > 0, mutated_nonzero_rows)

    result = {
        "status": "PASS exact-Q separator for full closure22+profile71 terminal matrix",
        "upstream_sha256": upstream_hash,
        "second_prime_upstream_sha256": second_hash,
        "independent_exact_dual_sha256": independent_hash,
        "two_prime_terminal_shape_identical": True,
        "source_words": len(source_words),
        "full_profile71_orbit_words": len(orbit),
        "terminal_modular_rank": upstream["final_rank"],
        "terminal_dual_support": len(support),
        "abstract_translations_examined": translations_examined,
        "distinct_restricted_integer_rows": len(rows),
        "restricted_row_nnz_histogram": {
            str(key): value for key, value in sorted(Counter(map(len, rows)).items())
        },
        "modular_rank_guards_row_augmented": modular_ranks,
        "exact_Q_row_rank": len(exact_basis),
        "exact_Q_augmented_rank": len(exact_basis) + 1,
        "free_column": free_column,
        "selected_independent_rows": len(selected),
        "selected_row_index_sha256": sha256(json.dumps(
            selected, separators=(",", ":")
        ).encode()).hexdigest(),
        "cleared_rational_denominator": cleared_denominator,
        "cleared_integer_gcd": cleared_gcd,
        "integer_separator_support": sum(value != 0 for value in integer),
        "integer_separator_min": min(integer),
        "integer_separator_max": max(integer),
        "integer_separator_target_pairing": integer_target_pairing,
        "integer_separator_max_abs_row_pairing": max(map(abs, row_pairings)),
        "integer_separator_vector_sha256": vector_digest,
        "integer_separator": [
            {"column": list(column), "coefficient": coefficient}
            for column, coefficient in zip(support, integer, strict=True)
            if coefficient
        ],
        "hostile_mutation_nonzero_row_pairings": mutated_nonzero_rows,
        "verdict": "target is not in the Q-span of the full terminal translated row matrix",
        "scope": (
            "Exact characteristic-zero separation in the abstract joint "
            "28-edge plus 9 ordered-colour semigroup. Every translation "
            "which can pair with the certificate support is checked over Z; "
            "the seven modular ranks are guards, not the proof."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(logical.encode()).hexdigest()
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LOGICAL_SHA256,
                (digest, EXPECTED_LOGICAL_SHA256))
    result["logical_sha256"] = digest
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result_path = Path(__file__).with_name("results_full_profile71_terminal_char0.json")
    if args.write_results:
        result_path.write_text(output)
    if args.check_results:
        require(result_path.read_text() == output, "stored result changed")
    print(output, end="")


if __name__ == "__main__":
    main()
