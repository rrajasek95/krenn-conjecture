#!/usr/bin/env python3
"""Modular census of the diagonal-8 plateau after exact level-9 transfer."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D9_PATH = HERE / "analyze_n8_diagonal9_plateau_transfer.py"
SPEC = importlib.util.spec_from_file_location("n8_d9_transfer", D9_PATH)
D9 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D9)
D10 = D9.D10
EXPECTED_LEDGER_SHA256 = (
    "a31399cd4b5852641f476395053d54e14aad96b2d83d7d3ed306cb633cf41709"
)


def critical_tails_after_d9():
    incoming = D9.critical_tails_after_d10()
    incoming9 = tuple({
        row: coefficient for row, coefficient in tail.items()
        if D10.TAIL.diagonal_count(row) == 9
    } for tail in incoming)
    seeds9 = set().union(*(
        set(column) for column in incoming9 if column
    ))
    states9, _keys9, top9, full9 = D10.close_plateau(seeds9, 9)
    (_pivots9, _kernels9, intrinsic9,
     _solutions9, continued9) = D10.exact_transfer(
        states9, top9, full9, incoming,
        expected_rank=880, expected_kernel=175, level=9
    )
    return intrinsic9 + continued9


def modular_reduce(states, columns, incoming, prime):
    row_index = {row: index for index, row in enumerate(states)}
    basis = {}
    for source in columns:
        vector = {
            row_index[row]: int(coefficient) % prime
            for row, coefficient in source.items()
        }
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                inverse = pow(vector[pivot], -1, prime)
                basis[pivot] = {
                    row: coefficient * inverse % prime
                    for row, coefficient in vector.items()
                    if coefficient * inverse % prime
                }
                break
            scale = vector[pivot]
            for row, coefficient in basis[pivot].items():
                value = (vector.get(row, 0) - scale * coefficient) % prime
                if value:
                    vector[row] = value
                else:
                    vector.pop(row, None)
    remainders = []
    for source in incoming:
        vector = {
            row_index[row]: (coefficient.numerator
                * pow(coefficient.denominator, -1, prime)) % prime
            for row, coefficient in source.items()
            if row in row_index
        }
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                break
            scale = vector[pivot]
            for row, coefficient in basis[pivot].items():
                value = (vector.get(row, 0) - scale * coefficient) % prime
                if value:
                    vector[row] = value
                else:
                    vector.pop(row, None)
        remainders.append(vector)
    remainder_rank = D10.TAIL.rank_mod_prime(tuple(
        {row: D10.QQ(value) for row, value in vector.items()}
        for vector in remainders
    ), prime)
    return tuple(sorted(basis)), tuple(remainders), remainder_rank


def sparse_digest(vectors):
    return D10.sequence_digest(
        tuple(sorted(vector.items())) for vector in vectors
    )


def main():
    incoming = critical_tails_after_d9()
    D10.require(len(incoming) == 308,
                "diagonal-9 critical source dimension changed")
    incoming8 = tuple({
        row: coefficient for row, coefficient in tail.items()
        if D10.TAIL.diagonal_count(row) == 8
    } for tail in incoming)
    active = tuple(column for column in incoming8 if column)
    seeds = set().union(*(set(column) for column in active))
    print("incoming/active/rank/seeds", len(incoming), len(active),
          D10.TAIL.rank_mod_prime(incoming8, 2147483647), len(seeds),
          flush=True)
    states, column_keys, top_columns, _full_columns = D10.close_plateau(seeds, 8)
    modular_records = []
    for prime in (1009, 1000003, 2147483647):
        pivots, remainders, remainder_rank = modular_reduce(
            states, top_columns, incoming8, prime
        )
        _dist_pivots, distinguished, distinguished_rank = modular_reduce(
            states, top_columns, incoming8[-7:], prime
        )
        modular_records.append({
            "prime": prime,
            "plateau_rank": len(pivots),
            "plateau_pivot_sha256": D10.sequence_digest(pivots),
            "incoming_quotient_remainder_rank": remainder_rank,
            "incoming_nonzero_quotient_remainders": sum(map(bool, remainders)),
            "incoming_remainder_sha256": sparse_digest(remainders),
            "distinguished_quotient_remainder_rank": distinguished_rank,
            "distinguished_nonzero_quotient_remainders": sum(
                map(bool, distinguished)
            ),
            "distinguished_remainder_sha256": sparse_digest(distinguished),
        })
    ledger = {
        "incoming_critical_source_classes": len(incoming),
        "incoming_level8_active_classes": len(active),
        "incoming_level8_initial_rank_mod_2147483647": (
            D10.TAIL.rank_mod_prime(incoming8, 2147483647)
        ),
        "incoming_level8_seed_states": len(seeds),
        "closed_level8_plateau_states": len(states),
        "closed_level8_plateau_columns": len(top_columns),
        "plateau_sparse_nonzeros": sum(map(len, top_columns)),
        "incoming_sparse_nonzeros": sum(map(len, incoming8)),
        "plateau_state_sha256": D10.sequence_digest(states),
        "plateau_column_sha256": D10.sequence_digest(column_keys),
        "plateau_incidence_sha256": sparse_digest(top_columns),
        "incoming_incidence_sha256": D10.sequence_digest(
            map(D10.encoded_sparse, incoming8)
        ),
        "modular_certificates": modular_records,
        "modular_plateau_rank_lower_bound_for_Q": 2961,
        "modular_incoming_quotient_rank_lower_bound_for_Q": 26,
        "modular_distinguished_quotient_rank_lower_bound_for_Q": 6,
        "modular_page_dimensions_if_Q_ranks_match": {
            "source": 306 + 308 - 26,
            "target": 4116 - 26,
        },
        "exact_export": (
            "orbit-compressed rows are the sorted canonical plateau_state "
            "keys; orbit-compressed columns are the sorted canonical "
            "plateau_column keys; coefficients are "
            "the multiplicities in the maximal diagonal-8 part of "
            "SOURCE.column_outputs(column); incoming columns are reconstructed "
            "by critical_tails_after_d9 and filtered to diagonal 8"
        ),
        "chart_localization_certificate": False,
        "scope_guard": (
            "exact S8xS3 orbit-compressed sparse matrix export and three-prime "
            "modular ranks only; no exact Q upper-rank/dependence certificate "
            "and no common-denominator lift to an individual P_j chart, so "
            "the 2961/26/6 values are Q lower bounds and not localized "
            "membership certificates"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        D10.require(digest == EXPECTED_LEDGER_SHA256,
                    "diagonal-8 modular plateau ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
