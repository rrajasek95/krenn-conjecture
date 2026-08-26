#!/usr/bin/env python3
"""Exact relative-cokernel audit for the lex C10 coefficient.

Let M_<10 be the full homogeneous-total-degree-12 normalized mixed Macaulay
map projected to encoded y degree at most nine.  Lower contraction choices
differ by ker(M_<10).  This checker asks whether the functional reading

    q = 0111202020494f4f50f8  (encoded y10*t^2)

vanishes on that kernel.  It starts from every literal source column which
emits q and performs shellwise exact inverse incidence on lower rows.  A row
is peeled only after every global source owner of it has been enumerated, so
each private-row elimination remains valid against the unmaterialized full
Macaulay matrix.  The run stops when all q owners are forced to zero, a
closed core survives, or the bounded gate lands.
"""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRST_PATH = ROOT / "computations/verify_n8_chart26_first_homogeneous_spair.py"
AGGREGATE = HERE / "results_full_y10_aggregate.json"
RESULTS = HERE / "results_c10_lower_kernel_invariance.json"
TOTAL_DEGREE = 12
GENERATOR_TOTAL_DEGREE = 4
MULTIPLIER_TOTAL_DEGREE = TOTAL_DEGREE - GENERATOR_TOTAL_DEGREE
LOWER_MAX_Y_DEGREE = 9
TARGET = bytes.fromhex("0111202020494f4f50f8")
TIME_CAP_SECONDS = 285.0
ROW_CAP = 1_500_000
COLUMN_CAP = 300_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("c10_kernel_first", FIRST_PATH)
FIRST = importlib.util.module_from_spec(spec)
require(spec.loader is not None, "cannot load normalized source")
spec.loader.exec_module(FIRST)


def quotient(dividend, divisor):
    answer = list(dividend)
    for value in divisor:
        require(value in answer, "requested non-divisor quotient")
        answer.remove(value)
    return bytes(answer)


def multiset_divisors(row, maximum_degree=4):
    seen = {b""}
    yield b""
    for degree in range(1, min(maximum_degree, len(row)) + 1):
        for positions in combinations(range(len(row)), degree):
            divisor = bytes(row[index] for index in positions)
            if divisor not in seen:
                seen.add(divisor)
                yield divisor


def multiply(left, right):
    return bytes(sorted(left + right))


def main():
    started = time.monotonic()
    require(TOTAL_DEGREE - len(TARGET) == 2,
            "lex C10 target lost its t^2 exponent")
    aggregate = json.loads(AGGREGATE.read_text())
    require(aggregate["PM4_incidence"]["lex_dead_row"] == TARGET.hex()
            and aggregate["PM4_incidence"]["lex_dead_coefficient"] == -4,
            "frozen deterministic C10 coefficient changed")
    originals, _lead_to_code = FIRST.original_basis()

    term_sources = defaultdict(list)
    for code, polynomial in originals.items():
        for term, coefficient in polynomial.items():
            term_sources[term].append((code, coefficient))

    def owners(row):
        answer = {}
        for term in multiset_divisors(row, 4):
            multiplier = quotient(row, term)
            if len(multiplier) > MULTIPLIER_TOTAL_DEGREE:
                continue
            for code, coefficient in term_sources.get(term, ()):
                column = (code, multiplier)
                answer[column] = answer.get(column, 0) + coefficient
        return {column: coefficient for column, coefficient in answer.items()
                if coefficient}

    lower_output_cache = {}

    def lower_outputs(column):
        cached = lower_output_cache.get(column)
        if cached is not None:
            return cached
        code, multiplier = column
        answer = Counter()
        for term, coefficient in originals[code].items():
            row = multiply(multiplier, term)
            if len(row) <= LOWER_MAX_Y_DEGREE:
                answer[row] += coefficient
        answer = {row: coefficient for row, coefficient in answer.items()
                  if coefficient}
        lower_output_cache[column] = answer
        return answer

    # Exhaustive q-owner census.
    q_columns = Counter()
    q_source_terms = {}
    for term in multiset_divisors(TARGET, 4):
        multiplier = quotient(TARGET, term)
        if len(multiplier) > MULTIPLIER_TOTAL_DEGREE:
            continue
        for code, coefficient in term_sources.get(term, ()):
            column = (code, multiplier)
            q_columns[column] += coefficient
            q_source_terms[column] = term
    q_columns = Counter({column: coefficient for column, coefficient
                         in q_columns.items() if coefficient})
    require(len(q_columns) == 7 and set(q_columns.values()) == {1},
            "lex C10 owner census changed")
    q_owner_set = set(q_columns)

    active_columns = set(q_owner_set)
    forced_zero = set()
    expanded_columns = set()
    row_to_columns = {}
    column_to_rows = defaultdict(set)
    peel_ledger = []
    shell_records = []
    stop = None

    shell = 0
    while not q_owner_set <= forced_zero:
        shell += 1
        frontier = sorted(active_columns - expanded_columns)
        if not frontier:
            stop = "CLOSED_CORE_WITH_Q_OWNERS"
            break
        new_rows = set()
        for position, column in enumerate(frontier, 1):
            for row in lower_outputs(column):
                if row not in row_to_columns:
                    new_rows.add(row)
            expanded_columns.add(column)
            if position % 2048 == 0 and time.monotonic() - started > TIME_CAP_SECONDS:
                stop = "TIME_CAP_DURING_COLUMN_EXPANSION"
                break
        if stop:
            break

        new_owner_columns = set()
        for position, row in enumerate(sorted(new_rows), 1):
            row_owners = owners(row)
            require(row_owners, "a lower row has no literal owner")
            row_to_columns[row] = row_owners
            for column in row_owners:
                column_to_rows[column].add(row)
                if column not in active_columns and column not in forced_zero:
                    active_columns.add(column)
                    new_owner_columns.add(column)
            if position % 2048 == 0:
                elapsed = time.monotonic() - started
                if elapsed > TIME_CAP_SECONDS:
                    stop = "TIME_CAP_DURING_OWNER_ENUMERATION"
                    break
                if (len(row_to_columns) > ROW_CAP
                        or len(active_columns) + len(forced_zero) > COLUMN_CAP):
                    stop = "SIZE_CAP_DURING_OWNER_ENUMERATION"
                    break
        if stop:
            break

        # All owners of every known row are literal and complete.  Peeling a
        # globally private row therefore forces its sole live column to zero
        # in every vector of ker(M_<10), independently of unexpanded rows.
        queue = deque(sorted(
            row for row, row_owners in row_to_columns.items()
            if len(set(row_owners) & active_columns) == 1
        ))
        shell_peeled = 0
        shell_q_peeled = 0
        while queue:
            row = queue.popleft()
            incident = set(row_to_columns[row]) & active_columns
            if len(incident) != 1:
                continue
            column = next(iter(incident))
            active_columns.remove(column)
            forced_zero.add(column)
            shell_peeled += 1
            if column in q_owner_set:
                shell_q_peeled += 1
            peel_ledger.append((shell, column, row,
                                row_to_columns[row][column]))
            for touched in sorted(column_to_rows[column]):
                if len(set(row_to_columns[touched]) & active_columns) == 1:
                    queue.append(touched)

        shell_records.append({
            "shell": shell,
            "expanded_frontier_columns": len(frontier),
            "new_rows": len(new_rows),
            "new_owner_columns": len(new_owner_columns),
            "peeled_columns": shell_peeled,
            "peeled_q_owners": shell_q_peeled,
            "active_columns_after_peel": len(active_columns),
            "q_owners_remaining": len(q_owner_set - forced_zero),
            "cumulative_rows": len(row_to_columns),
            "cumulative_columns": len(active_columns | forced_zero),
        })
        if time.monotonic() - started > TIME_CAP_SECONDS:
            stop = "TIME_CAP_AFTER_SHELL"
            break
        if (len(row_to_columns) > ROW_CAP
                or len(active_columns) + len(forced_zero) > COLUMN_CAP):
            stop = "SIZE_CAP_AFTER_SHELL"
            break

    invariant = q_owner_set <= forced_zero
    if invariant:
        status = "EXACT_LEX_C10_COEFFICIENT_INVARIANT"
        stop = "ALL_Q_OWNERS_FORCED_ZERO"
    elif stop == "CLOSED_CORE_WITH_Q_OWNERS":
        status = "C10_INVARIANCE_CLOSED_CORE_UNDECIDED"
    else:
        status = "C10_INVARIANCE_CAP_UNRESOLVED"

    target_witnesses = []
    for shell_index, column, row, coefficient in peel_ledger:
        if column not in q_owner_set:
            continue
        target_witnesses.append({
            "source_code": column[0],
            "multiplier_y": column[1].hex(),
            "multiplier_t_exponent": (
                MULTIPLIER_TOTAL_DEGREE - len(column[1])
            ),
            "q_source_term": q_source_terms[column].hex(),
            "q_coefficient": q_columns[column],
            "forcing_shell": shell_index,
            "private_lower_row": row.hex(),
            "private_lower_y_degree": len(row),
            "private_coefficient": [coefficient.numerator,
                                    coefficient.denominator],
        })
    target_witnesses.sort(key=lambda item: (
        item["source_code"], item["multiplier_y"]
    ))

    result = {
        "format": "n8-orbit26-c10-lower-kernel-invariance-v2",
        "status": status,
        "stop_reason": stop,
        "target_row_y10": TARGET.hex(),
        "target_total_degree": TOTAL_DEGREE,
        "target_t_exponent": TOTAL_DEGREE - len(TARGET),
        "deterministic_scale4_coefficient": -4,
        "relative_map": (
            "ell: ker(M_total12 projected to y<=9) -> Q, "
            "ell(v)=coefficient of target y10*t2 in M(v)"
        ),
        "target_owner_columns": len(q_owner_set),
        "target_owners_forced_zero": len(q_owner_set & forced_zero),
        "target_owners_remaining": len(q_owner_set - forced_zero),
        "target_owner_witnesses": target_witnesses,
        "shell_records": shell_records,
        "known_lower_rows": len(row_to_columns),
        "known_global_owner_columns": len(active_columns | forced_zero),
        "forced_zero_columns": len(forced_zero),
        "active_columns": len(active_columns),
        "unexpanded_active_columns": len(active_columns - expanded_columns),
        "peel_ledger_digest": sha256(b"".join(
            shell_index.to_bytes(2, "big")
            + column[0].to_bytes(2, "big") + column[1] + row
            + f"{coefficient.numerator}/{coefficient.denominator}".encode("ascii")
            for shell_index, column, row, coefficient in peel_ledger
        )).hexdigest(),
        "theorem": (
            "Every source column capable of changing the lex C10 coordinate is "
            "one of the seven q owners. At each shell every global owner of every "
            "used lower row is enumerated before private-row peeling, so each "
            "elimination is valid in the full unmaterialized Macaulay matrix. "
            "If all seven q owners are forced to zero, ell vanishes on the entire "
            "lower kernel and the scale-four coefficient -4 is independent of all "
            "lower contraction choices."
        ),
        "scope": (
            "full normalized mixed-generator Macaulay domain at homogeneous total "
            "degree12, fixed orbit26 chart and one lex y10 coordinate; coefficient "
            "invariance does not by itself prove full ideal nonmembership"
        ),
        "caps": {
            "seconds": TIME_CAP_SECONDS,
            "rows": ROW_CAP,
            "columns": COLUMN_CAP,
        },
        "source_sha256": {
            str(FIRST_PATH.relative_to(ROOT)):
                sha256(FIRST_PATH.read_bytes()).hexdigest(),
            str(AGGREGATE.relative_to(ROOT)):
                sha256(AGGREGATE.read_bytes()).hexdigest(),
        },
    }
    logical = dict(result)
    encoded = json.dumps(logical, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("lex C10 lower-kernel audit:", status)
    print("shells/q forced/remaining/rows/columns/active:", len(shell_records),
          len(q_owner_set & forced_zero), len(q_owner_set - forced_zero),
          len(row_to_columns), len(active_columns | forced_zero),
          len(active_columns))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
