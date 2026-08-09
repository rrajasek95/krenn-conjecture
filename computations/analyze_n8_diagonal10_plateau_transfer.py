#!/usr/bin/env python3
"""Close and test the diagonal-10 plateau hit by the root transferred tails."""

from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TAIL_PATH = HERE / "verify_n8_root_plateau_transferred_tail.py"
SPEC = importlib.util.spec_from_file_location("n8_root_tail", TAIL_PATH)
TAIL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TAIL)
SOURCE = TAIL.SOURCE
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "97bdfccdfd35249f0ee28c310f45a7e99a89ff7b12cfae0272976b07c1f27f8b"
)
GRAPH_PATH = HERE / "analyze_n8_even_rewrite_state_graph.py"
GRAPH_SPEC = importlib.util.spec_from_file_location("n8_even_graph_d10", GRAPH_PATH)
GRAPH = importlib.util.module_from_spec(GRAPH_SPEC)
GRAPH_SPEC.loader.exec_module(GRAPH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def root_transferred_tails():
    roots = tuple(sorted(SOURCE.target_orbit_rows()))
    root_index = {row: index for index, row in enumerate(roots)}
    columns = tuple(sorted(set().union(*(
        SOURCE.incident_columns(row) for row in roots
    ))))
    full_columns = []
    top_columns = []
    for column in columns:
        full = Counter(SOURCE.column_outputs(column))
        full_columns.append({row: QQ(value) for row, value in full.items()})
        top_columns.append({
            root_index[row]: QQ(value)
            for row, value in full.items() if row in root_index
        })
    pivots = {}
    pivot_representatives = {}
    zero_representatives = {}
    for column_number, source in enumerate(top_columns):
        vector = dict(source)
        representative = {column_number: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                pivot_representatives[pivot] = {
                    column: coefficient / value
                    for column, coefficient in representative.items()
                }
                break
            TAIL.add_scaled(vector, pivots[pivot], -value)
            TAIL.add_scaled(representative, pivot_representatives[pivot], -value)
        if not vector:
            zero_representatives[column_number] = representative
    return tuple(
        TAIL.replay(full_columns, representative)
        for _column, representative in sorted(zero_representatives.items())
    )


def is_even_column(column):
    edges = SOURCE.mate_edges(SOURCE.decode_key(column))
    return all(size % 2 == 0 for size in GRAPH.component_sizes(edges))


def close_plateau(seeds, level):
    states = set(seeds)
    queue = deque(sorted(seeds))
    columns = {}
    while queue:
        row = queue.popleft()
        require(TAIL.diagonal_count(row) == level,
                "plateau queue left its diagonal level")
        for column in SOURCE.incident_columns(row):
            if column in columns or not is_even_column(column):
                continue
            entries = Counter(SOURCE.column_outputs(column))
            maximum = max(map(TAIL.diagonal_count, entries))
            if maximum != level:
                continue
            top = {
                other: QQ(coefficient)
                for other, coefficient in entries.items()
                if TAIL.diagonal_count(other) == level
            }
            require(row in top, "incident maximal fibre lost its source")
            full = {
                other: QQ(coefficient)
                for other, coefficient in entries.items()
            }
            columns[column] = (top, full)
            for other in top:
                if other not in states:
                    states.add(other)
                    queue.append(other)
        if len(states) % 250 == 0:
            print("plateau closure states/columns", len(states), len(columns),
                  flush=True)
    require(all(set(top) <= states for top, _full in columns.values()),
            "plateau column escaped the closed state set")
    keys = tuple(sorted(columns))
    return (tuple(sorted(states)), keys,
            tuple(columns[key][0] for key in keys),
            tuple(columns[key][1] for key in keys))


def reduce_mod_prime(states, columns, incoming, prime):
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
    remainder_rank = TAIL.rank_mod_prime(
        tuple({row: QQ(value) for row, value in vector.items()}
              for vector in remainders), prime
    )
    return len(basis), tuple(map(len, remainders)), remainder_rank


def exact_transfer(states, top_columns, full_columns, incoming):
    """Contract the plateau exactly and return quotient/corrected tails."""
    row_index = {row: index for index, row in enumerate(states)}
    indexed_top = tuple({
        row_index[row]: coefficient for row, coefficient in column.items()
    } for column in top_columns)
    pivots = {}
    pivot_representatives = {}
    kernel_representatives = {}
    for column_number, source in enumerate(indexed_top):
        vector = dict(source)
        representative = {column_number: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                pivot_representatives[pivot] = {
                    column: coefficient / value
                    for column, coefficient in representative.items()
                }
                break
            TAIL.add_scaled(vector, pivots[pivot], -value)
            TAIL.add_scaled(representative, pivot_representatives[pivot], -value)
        if not vector:
            kernel_representatives[column_number] = representative
    require(len(pivots) == 300 and len(kernel_representatives) == 126,
            "exact diagonal-10 plateau rank/nullity changed")

    corrected = []
    incoming_solutions = []
    quotient_remainders = []
    for source in incoming:
        vector = {
            row_index[row]: coefficient
            for row, coefficient in source.items() if row in row_index
        }
        solution = {}
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                break
            value = vector[pivot]
            TAIL.add_scaled(vector, pivots[pivot], -value)
            TAIL.add_scaled(solution, pivot_representatives[pivot], value)
        quotient_remainders.append(vector)
        incoming_solutions.append(solution)
        full = dict(source)
        for column, coefficient in solution.items():
            TAIL.add_scaled(full, full_columns[column], -coefficient)
        require(not any(TAIL.diagonal_count(row) == 10 for row in full),
                "exact plateau correction retained a diagonal-10 term")
        corrected.append(full)
    require(all(not remainder for remainder in quotient_remainders),
            "an incoming tail survives the exact diagonal-10 cokernel")
    kernel_representatives = tuple(
        kernel_representatives[column]
        for column in sorted(kernel_representatives)
    )
    intrinsic_tails = tuple(
        TAIL.replay(full_columns, representative)
        for representative in kernel_representatives
    )
    require(all(tail for tail in intrinsic_tails),
            "an intrinsic plateau kernel vanished in the full module")
    require(all(not any(TAIL.diagonal_count(row) == 10 for row in tail)
                for tail in intrinsic_tails),
            "an intrinsic plateau-kernel tail retained diagonal level 10")
    return (tuple(pivots), kernel_representatives,
            intrinsic_tails, tuple(incoming_solutions), tuple(corrected))


def encoded_sparse(vector):
    return tuple(
        (key, coefficient.numerator, coefficient.denominator)
        for key, coefficient in sorted(vector.items())
    )


def sequence_digest(values):
    digest = sha256()
    for value in values:
        digest.update(repr(value).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def main():
    tails = root_transferred_tails()
    incoming10 = tuple({
        row: coefficient for row, coefficient in tail.items()
        if TAIL.diagonal_count(row) == 10
    } for tail in tails)
    seeds = set().union(*(set(column) for column in incoming10))
    print("incoming diagonal-10 seeds", len(seeds), flush=True)
    states, column_keys, top_columns, full_columns = close_plateau(seeds, 10)
    modular_records = []
    for prime in (1009, 1000003, 2147483647):
        rank, remainder_terms, remainder_rank = reduce_mod_prime(
            states, top_columns, incoming10, prime
        )
        modular_records.append({
            "prime": prime,
            "plateau_rank": rank,
            "incoming_quotient_remainder_terms": list(remainder_terms),
            "incoming_quotient_remainder_rank": remainder_rank,
        })
    pivots, kernels, intrinsic_tails, solutions, corrected = exact_transfer(
        states, top_columns, full_columns, tails
    )
    critical_targets = tuple(
        row for index, row in enumerate(states) if index not in frozenset(pivots)
    )
    levels = tuple(sorted({
        TAIL.diagonal_count(row) for tail in corrected for row in tail
    }, reverse=True))
    corrected_level_columns = {
        level: tuple({
            row: coefficient for row, coefficient in tail.items()
            if TAIL.diagonal_count(row) == level
        } for tail in corrected)
        for level in levels
    }
    all_critical_tails = intrinsic_tails + corrected
    all_levels = tuple(sorted({
        TAIL.diagonal_count(row)
        for tail in all_critical_tails for row in tail
    }, reverse=True))
    all_level_columns = {
        level: tuple({
            row: coefficient for row, coefficient in tail.items()
            if TAIL.diagonal_count(row) == level
        } for tail in all_critical_tails)
        for level in all_levels
    }
    ledger = {
        "incoming_level10_seed_states": len(seeds),
        "closed_level10_plateau_states": len(states),
        "closed_level10_plateau_columns": len(top_columns),
        "plateau_state_sha256": sequence_digest(states),
        "plateau_column_sha256": sequence_digest(column_keys),
        "modular_certificates": modular_records,
        "exact_plateau_rank": len(pivots),
        "intrinsic_plateau_source_kernel_dimension": len(kernels),
        "plateau_target_cokernel_dimension": len(critical_targets),
        "continued_root_source_classes": len(tails),
        "combined_critical_source_dimension": len(kernels) + len(tails),
        "incoming_target_cokernel_projection_rank": 0,
        "incoming_exact_solution_term_counts": list(map(len, solutions)),
        "incoming_exact_solution_sha256": sequence_digest(
            map(encoded_sparse, solutions)
        ),
        "critical_target_state_sha256": sequence_digest(critical_targets),
        "intrinsic_source_kernel_sha256": sequence_digest(
            encoded_sparse(representative)
            for representative in kernels
        ),
        "intrinsic_source_kernel_tail_term_counts": list(map(
            len, intrinsic_tails
        )),
        "intrinsic_source_kernel_tail_maximum_level_histogram": dict(sorted(
            Counter(max(map(TAIL.diagonal_count, tail))
                    for tail in intrinsic_tails).items(), reverse=True
        )),
        "intrinsic_source_kernel_tail_sha256": sequence_digest(
            map(encoded_sparse, intrinsic_tails)
        ),
        "corrected_lower_tail_term_counts": list(map(len, corrected)),
        "corrected_lower_tail_maximum_levels": [
            max(map(TAIL.diagonal_count, tail)) for tail in corrected
        ],
        "corrected_lower_tail_level_histogram": dict(sorted(Counter(
            TAIL.diagonal_count(row)
            for tail in corrected for row in tail
        ).items(), reverse=True)),
        "corrected_lower_tail_level_ranks_mod_2147483647": {
            level: TAIL.rank_mod_prime(columns, 2147483647)
            for level, columns in corrected_level_columns.items()
        },
        "corrected_lower_tail_sha256": sequence_digest(
            map(encoded_sparse, corrected)
        ),
        "all_133_critical_source_tail_maximum_level_histogram": dict(sorted(
            Counter(max(map(TAIL.diagonal_count, tail))
                    for tail in all_critical_tails).items(), reverse=True
        )),
        "all_133_critical_source_tail_level_ranks_mod_2147483647": {
            level: TAIL.rank_mod_prime(columns, 2147483647)
            for level, columns in all_level_columns.items()
        },
        "all_133_critical_source_tail_sha256": sequence_digest(
            map(encoded_sparse, all_critical_tails)
        ),
        "spectral_direction": (
            "all seven root source-kernel tails vanish in the diagonal-10 "
            "target cokernel and continue after exact plateau correction; "
            "the seven diagonal-12 target/chart cokernel classes are not "
            "reduced by this source differential"
        ),
        "scope_guard": (
            "exact contraction of the reachable closed diagonal-10 maximal "
            "plateau; diagonal-9 and lower plateaus remain uncontracted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "diagonal-10 plateau transfer ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
