#!/usr/bin/env python3
"""Close the diagonal-9 plateau reached after exact level-10 contraction."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D10_PATH = HERE / "analyze_n8_diagonal10_plateau_transfer.py"
SPEC = importlib.util.spec_from_file_location("n8_d10_transfer", D10_PATH)
D10 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D10)
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "599746a90b1eb36da7946f8669573b44cb3a4f6762ee2388905a51bde8b2bf0f"
)


def critical_tails_after_d10():
    root_tails = D10.root_transferred_tails()
    incoming10 = tuple({
        row: coefficient for row, coefficient in tail.items()
        if D10.TAIL.diagonal_count(row) == 10
    } for tail in root_tails)
    seeds10 = set().union(*(set(column) for column in incoming10))
    states10, _keys10, top10, full10 = D10.close_plateau(seeds10, 10)
    (_pivots10, _kernels10, intrinsic10,
     _solutions10, continued10) = D10.exact_transfer(
        states10, top10, full10, root_tails
    )
    return intrinsic10 + continued10


def main():
    incoming = critical_tails_after_d10()
    D10.require(len(incoming) == 133,
                "diagonal-10 critical source dimension changed")
    incoming9 = tuple({
        row: coefficient for row, coefficient in tail.items()
        if D10.TAIL.diagonal_count(row) == 9
    } for tail in incoming)
    active = tuple(column for column in incoming9 if column)
    seeds = set().union(*(set(column) for column in active))
    print("incoming/active/rank/seeds", len(incoming), len(active),
          D10.TAIL.rank_mod_prime(incoming9, 2147483647), len(seeds),
          flush=True)
    states, column_keys, top_columns, full_columns = D10.close_plateau(seeds, 9)
    modular_records = []
    for prime in (1009, 1000003, 2147483647):
        rank, remainder_terms, remainder_rank = D10.reduce_mod_prime(
            states, top_columns, incoming9, prime
        )
        distinguished_rank = D10.reduce_mod_prime(
            states, top_columns, incoming9[-7:], prime
        )[2]
        modular_records.append({
            "prime": prime,
            "plateau_rank": rank,
            "incoming_quotient_remainder_rank": remainder_rank,
            "incoming_nonzero_quotient_remainders": sum(
                bool(value) for value in remainder_terms
            ),
            "distinguished_quotient_remainder_rank": distinguished_rank,
        })
    (pivots, kernels, intrinsic_tails,
     solutions, continued_tails) = D10.exact_transfer(
        states, top_columns, full_columns, incoming,
        expected_rank=880, expected_kernel=175, level=9
    )
    all_tails = intrinsic_tails + continued_tails
    critical_targets = tuple(
        row for index, row in enumerate(states)
        if index not in frozenset(pivots)
    )
    levels = tuple(sorted({
        D10.TAIL.diagonal_count(row)
        for tail in all_tails for row in tail
    }, reverse=True))
    level_columns = {
        level: tuple({
            row: coefficient for row, coefficient in tail.items()
            if D10.TAIL.diagonal_count(row) == level
        } for tail in all_tails)
        for level in levels
    }
    distinguished = continued_tails[-7:]
    ledger = {
        "incoming_critical_source_classes": len(incoming),
        "incoming_level9_active_classes": len(active),
        "incoming_level9_initial_rank_mod_2147483647": (
            D10.TAIL.rank_mod_prime(incoming9, 2147483647)
        ),
        "incoming_level9_seed_states": len(seeds),
        "closed_level9_plateau_states": len(states),
        "closed_level9_plateau_columns": len(top_columns),
        "plateau_state_sha256": D10.sequence_digest(states),
        "plateau_column_sha256": D10.sequence_digest(column_keys),
        "modular_certificates": modular_records,
        "exact_plateau_rank": len(pivots),
        "intrinsic_plateau_source_kernel_dimension": len(kernels),
        "plateau_target_cokernel_dimension": len(critical_targets),
        "incoming_target_cokernel_projection_rank": 0,
        "combined_critical_source_dimension": len(kernels) + len(incoming),
        "combined_critical_target_dimension": len(critical_targets),
        "incoming_exact_nonzero_solutions": sum(bool(value) for value in solutions),
        "incoming_exact_solution_total_terms": sum(map(len, solutions)),
        "incoming_exact_solution_sha256": D10.sequence_digest(
            map(D10.encoded_sparse, solutions)
        ),
        "critical_target_state_sha256": D10.sequence_digest(critical_targets),
        "intrinsic_source_kernel_sha256": D10.sequence_digest(
            map(D10.encoded_sparse, kernels)
        ),
        "all_308_critical_source_tail_maximum_level_histogram": dict(sorted(
            Counter(max(map(D10.TAIL.diagonal_count, tail))
                    for tail in all_tails).items(), reverse=True
        )),
        "all_308_critical_source_tail_level_ranks_mod_2147483647": {
            level: D10.TAIL.rank_mod_prime(columns, 2147483647)
            for level, columns in level_columns.items()
        },
        "all_308_critical_source_tail_total_terms": sum(map(len, all_tails)),
        "all_308_critical_source_tail_sha256": D10.sequence_digest(
            map(D10.encoded_sparse, all_tails)
        ),
        "distinguished_root_descendant_tail_term_counts": list(map(
            len, distinguished
        )),
        "distinguished_root_descendant_maximum_levels": [
            max(map(D10.TAIL.diagonal_count, tail)) for tail in distinguished
        ],
        "distinguished_root_descendant_tail_sha256": D10.sequence_digest(
            map(D10.encoded_sparse, distinguished)
        ),
        "spectral_direction": (
            "all 133 incoming diagonal-10 critical source classes vanish "
            "in the diagonal-9 target cokernel and continue after exact "
            "correction; the previously retained target cokernels persist"
        ),
        "scope_guard": (
            "exact contraction of the reachable closed diagonal-9 maximal "
            "plateau; diagonal-8 and lower plateaus remain uncontracted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        D10.require(digest == EXPECTED_LEDGER_SHA256,
                    "diagonal-9 plateau transfer ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
