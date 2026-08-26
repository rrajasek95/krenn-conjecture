#!/usr/bin/env python3
"""First t-saturation step for the frozen N8 chart-26 degree-seven dual.

Reconstruct the exact 49-row degree-seven functional lambda.  At homogeneous
degree eight, columns whose normalized x-multiplier has degree at most three
are t-times old columns and are already killed.  Only multiplier-degree-four
columns are new.  Close their degree-eight top incidence from the columns on
which lambda has nonzero lower-boundary pairing and solve

    A_top^T z = - boundary(lambda)

exactly over Q.  A solution extends lambda; a literal dual of this relative
system proves that this particular lambda cannot extend.  Neither outcome is
silently promoted to unrestricted saturation without its stated scope.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D7_PATH = ROOT / "computations/verify_n8_chart26_normalized_degree7_closure.py"
RESULTS = HERE / "results_degree8_dual_extension.json"
QQ = Fraction
PRIME = 1_073_741_827
WALL_CAP_SECONDS = 300
ROW_GUARD = 2_000_000
COLUMN_GUARD = 200_000

EXPECTED_D7_SHA256 = (
    "9a6e9d4f7bfe2726c1655c4f7b0d5463a90c6a087fe1bf88a0f6cd34d400d99c"
)
EXPECTED_D7_LEDGER_SHA256 = (
    "2f4fcd2d53c69ea2ec44f7c3d9eb050bd577471be823c02a220e1c1e5d41a570"
)
EXPECTED_D7_DUAL_SHA256 = (
    "b0f137c8827d8da94525a53636bd30791e7c56722b09a74e8cdfd0c792e75fb3"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_d7():
    raw = D7_PATH.read_bytes()
    require(sha256(raw).hexdigest() == EXPECTED_D7_SHA256,
            "degree-seven checker digest changed")
    spec = importlib.util.spec_from_file_location("n8_degree7", D7_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(module.EXPECTED_LEDGER_SHA256 == EXPECTED_D7_LEDGER_SHA256,
            "degree-seven ledger pin changed")
    return module


def check_wall(started):
    if monotonic() - started > WALL_CAP_SECONDS:
        raise TimeoutError("degree-eight extension exceeded 300-second guard")


def reconstruct_degree7_dual(module, started):
    residual, _canonical_seed, _actual_seed = module.seed_residual()
    invariant_residual = {}
    for row, coefficient in residual.items():
        representative = module.canonical_normalized_row(row)
        previous = invariant_residual.setdefault(representative, coefficient)
        require(previous == coefficient, "seed residual lost invariance")

    rows, columns, _layers = module.top_degree_closure(invariant_residual)
    rank, target_remainder, _maximum_basis, dual, target_pairing = (
        module.exact_rank_and_target(rows, columns, invariant_residual)
    )
    forced = set()
    records = []
    while True:
        candidates, violating, _histogram = module.dual_violating_columns(
            dual, set(columns)
        )
        records.append((len(rows), len(columns), rank, len(dual),
                        len(candidates), len(violating)))
        if not violating:
            break
        forced.update(violating)
        rows, columns, _layers = module.top_degree_closure(
            invariant_residual, forced_columns=forced
        )
        rank, target_remainder, _maximum_basis, dual, target_pairing = (
            module.exact_rank_and_target(rows, columns, invariant_residual)
        )
        check_wall(started)
    require(records == [
        (20859, 298, 298, 3, 16, 13),
        (134041, 1849, 1849, 24, 38, 8),
        (216350, 2955, 2955, 37, 50, 6),
        (273857, 3721, 3721, 49, 56, 0),
    ], "degree-seven closure ledger changed")
    require(target_remainder == {b"": QQ(-1)} and target_pairing == -1,
            "degree-seven target class changed")
    require(len(dual) == 49 and dual.get(b"") == 1,
            "degree-seven dual changed")
    record = [[row.hex(), value.numerator, value.denominator]
              for row, value in sorted(dual.items())]
    digest = sha256(json.dumps(record, separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED_D7_DUAL_SHA256,
            "degree-seven dual digest changed")
    return dual, records


def invariant_entries(module, column):
    entries = defaultdict(int)
    for actual in module.normalized_column_orbit(column):
        for output, coefficient in module.normalized_column_outputs(actual):
            if output == module.canonical_normalized_row(output):
                entries[output] += coefficient
    return {row: value for row, value in entries.items() if value}


def pairing(entries, functional):
    return sum(QQ(coefficient) * functional.get(row, QQ(0))
               for row, coefficient in entries.items())


def relative_top_closure(module, initial_columns, started):
    columns = set(initial_columns)
    rows = set()
    for column in columns:
        rows.update(row for row in invariant_entries(module, column) if len(row) == 8)
    frontier = set(rows)
    layers = []
    while frontier:
        new_columns = set()
        for row in frontier:
            require(len(row) == 8, "relative top closure left degree eight")
            for column in module.top_incident_columns(row):
                if len(column[1]) == 4 and column not in columns:
                    new_columns.add(column)
        columns.update(new_columns)
        new_rows = set()
        for column in new_columns:
            new_rows.update(
                row for row in invariant_entries(module, column)
                if len(row) == 8 and row not in rows
            )
        layers.append((len(new_rows), len(new_columns)))
        rows.update(new_rows)
        frontier = new_rows
        require(len(rows) <= ROW_GUARD and len(columns) <= COLUMN_GUARD,
                "relative degree-eight closure exceeded size guard")
        check_wall(started)
    return tuple(sorted(rows)), tuple(sorted(columns)), tuple(layers)


def reduce_mod(vector, pivots, prime):
    vector = {index: value % prime for index, value in vector.items()
              if value % prime}
    while vector:
        pivot = min(vector)
        value = vector[pivot]
        if pivot not in pivots:
            inverse = pow(value, prime - 2, prime)
            pivots[pivot] = {
                index: coefficient * inverse % prime
                for index, coefficient in vector.items()
            }
            return True, {}
        for index, coefficient in pivots[pivot].items():
            result = (vector.get(index, 0) - value * coefficient) % prime
            if result:
                vector[index] = result
            else:
                vector.pop(index, None)
    return False, vector


def modular_relative_rank(row_vectors, target):
    pivots = {}
    for vector in row_vectors:
        reduce_mod(vector, pivots, PRIME)
    work = {}
    for index, value in target.items():
        residue = (value.numerator
                   * pow(value.denominator, PRIME - 2, PRIME)) % PRIME
        if residue:
            work[index] = residue
    while work:
        pivot = min(work)
        value = work[pivot]
        if pivot not in pivots:
            break
        for index, coefficient in pivots[pivot].items():
            result = (work.get(index, 0) - value * coefficient) % PRIME
            if result:
                work[index] = result
            else:
                work.pop(index, None)
    return len(pivots), work


def add_scaled(vector, source, scalar):
    for key, value in source.items():
        result = vector.get(key, QQ(0)) + scalar * value
        if result:
            vector[key] = result
        else:
            vector.pop(key, None)


def exact_relative_solve(rows, row_vectors, target, started):
    # Each basis record carries both its normalized equation vector and its
    # expression in the original degree-eight row vectors.
    pivots = {}
    for row, source in zip(rows, row_vectors):
        vector = {index: QQ(value) for index, value in source.items() if value}
        combination = {row: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = 1 / value
                vector = {index: coefficient * inverse
                          for index, coefficient in vector.items()}
                combination = {key: coefficient * inverse
                               for key, coefficient in combination.items()}
                pivots[pivot] = (vector, combination)
                break
            basis, basis_combination = pivots[pivot]
            add_scaled(vector, basis, -value)
            add_scaled(combination, basis_combination, -value)
        if len(pivots) % 250 == 0:
            check_wall(started)

    work = {index: QQ(value) for index, value in target.items() if value}
    solution = {}
    while work:
        pivot = min(work)
        value = work[pivot]
        if pivot not in pivots:
            break
        basis, basis_combination = pivots[pivot]
        add_scaled(work, basis, -value)
        add_scaled(solution, basis_combination, value)
    if not work:
        return len(pivots), solution, {}, {}

    # A literal functional on equation columns annihilating every top-row
    # vector and pairing nontrivially with the boundary target.
    selected = min(work)
    separator = {selected: QQ(1)}
    for pivot in sorted(pivots, reverse=True):
        basis, _combination = pivots[pivot]
        value = -sum(coefficient * separator.get(index, QQ(0))
                     for index, coefficient in basis.items() if index != pivot)
        if value:
            separator[pivot] = value
    return len(pivots), {}, work, separator


def run():
    started = monotonic()
    module = load_d7()
    degree7_dual, degree7_records = reconstruct_degree7_dual(module, started)

    bounded = module.bounded_incident_columns(degree7_dual, maximum_output_degree=8)
    new_candidates = sorted(column for column in bounded if len(column[1]) == 4)
    boundary = {}
    violating = []
    boundary_histogram = Counter()
    for column in new_candidates:
        value = pairing(invariant_entries(module, column), degree7_dual)
        if value:
            violating.append(column)
            boundary[column] = value
            boundary_histogram[value] += 1
    require(violating, "degree-seven dual already extends by zero unexpectedly")

    rows, columns, layers = relative_top_closure(module, violating, started)
    column_index = {column: index for index, column in enumerate(columns)}
    row_vectors = [defaultdict(int) for _ in rows]
    row_index = {row: index for index, row in enumerate(rows)}
    full_boundary = {}
    nnz = 0
    for column in columns:
        entries = invariant_entries(module, column)
        cindex = column_index[column]
        low = pairing(entries, degree7_dual)
        if low:
            full_boundary[cindex] = -low
        for row, coefficient in entries.items():
            if len(row) == 8:
                row_vectors[row_index[row]][cindex] += coefficient
                nnz += 1
    require({columns[index]: -value for index, value in full_boundary.items()
             if value} == boundary,
            "relative closure acquired an unseeded boundary column")

    modular_rank, modular_remainder = modular_relative_rank(
        row_vectors, full_boundary
    )
    check_wall(started)
    exact_rank, extension, exact_remainder, separator = exact_relative_solve(
        rows, row_vectors, full_boundary, started
    )
    require(exact_rank == modular_rank,
            "relative exact/modular ranks differ at the discovery prime")

    result = {
        "status": None,
        "degree7_checker_sha256": EXPECTED_D7_SHA256,
        "degree7_ledger_sha256": EXPECTED_D7_LEDGER_SHA256,
        "degree7_dual_sha256": EXPECTED_D7_DUAL_SHA256,
        "degree7_dual_support": len(degree7_dual),
        "degree7_reconstruction_records": [list(item) for item in degree7_records],
        "degree8_new_incident_columns": len(new_candidates),
        "degree8_initial_boundary_violations": len(violating),
        "degree8_initial_boundary_pairing_histogram": [
            [[value.numerator, value.denominator], count]
            for value, count in sorted(boundary_histogram.items())
        ],
        "degree8_relative_rows": len(rows),
        "degree8_relative_columns": len(columns),
        "degree8_relative_nnz": nnz,
        "degree8_relative_closure_layers": [list(item) for item in layers],
        "modular_prime": PRIME,
        "modular_top_rank": modular_rank,
        "modular_target_remainder_terms": len(modular_remainder),
        "exact_top_rank": exact_rank,
        "elapsed_seconds": monotonic() - started,
    }

    if extension:
        extended = dict(degree7_dual)
        extended.update(extension)
        incident = module.bounded_incident_columns(
            extended, maximum_output_degree=8
        )
        nonzero_pairings = {}
        for column in incident:
            value = pairing(invariant_entries(module, column), extended)
            if value:
                nonzero_pairings[column] = value
        require(not nonzero_pairings, "extended dual misses an incident column")
        require(extended.get(b"") == 1, "extended dual lost t^8 pairing")
        record = [[row.hex(), value.numerator, value.denominator]
                  for row, value in sorted(extended.items())]
        record_digest = sha256(json.dumps(
            record, separators=(",", ":")
        ).encode()).hexdigest()
        result.update({
            "status": "PASS exact degree-eight dual extension",
            "degree8_extension_rows": len(extension),
            "degree8_extended_dual_support": len(extended),
            "degree8_extended_dual_degree_histogram": dict(sorted(
                Counter(map(len, extended)).items()
            )),
            "degree8_extended_dual_coefficient_histogram": [
                [[value.numerator, value.denominator], count]
                for value, count in sorted(Counter(extended.values()).items())
            ],
            "degree8_extended_dual_incident_columns": len(incident),
            "degree8_extended_dual_sha256": record_digest,
            "degree8_extended_dual": record,
            "conclusion": "t^8 is not in the degree-eight homogeneous mixed ideal over Q",
            "scope_guard": "does not decide t^N for N>=9 or unrestricted t-saturation",
        })
    else:
        require(exact_remainder and separator,
                "relative exact solve returned neither extension nor obstruction")
        target_pairing = sum(
            value * separator.get(index, QQ(0))
            for index, value in full_boundary.items()
        )
        require(target_pairing, "relative separator lost its target pairing")
        for vector in row_vectors:
            require(not sum(QQ(value) * separator.get(index, QQ(0))
                            for index, value in vector.items()),
                    "relative separator does not annihilate a top row")
        result.update({
            "status": "PASS exact obstruction to extending the selected degree-seven dual",
            "exact_target_remainder_terms": len(exact_remainder),
            "relative_separator_support": len(separator),
            "relative_separator_target_pairing": [
                target_pairing.numerator, target_pairing.denominator
            ],
            "relative_separator": [
                [columns[index][0], columns[index][1].hex(),
                 value.numerator, value.denominator]
                for index, value in sorted(separator.items())
            ],
            "conclusion": "the frozen 49-row lambda does not extend by degree-eight top weights",
            "scope_guard": "does not by itself prove t^8 membership; another degree-seven representative may extend",
        })
    return result


def main():
    result = run()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print(
        "degree8 relative rows/columns/rank="
        f"{result['degree8_relative_rows']}/"
        f"{result['degree8_relative_columns']}/"
        f"{result['exact_top_rank']}"
    )
    print(f"elapsed_seconds={result['elapsed_seconds']:.3f}")


if __name__ == "__main__":
    main()
