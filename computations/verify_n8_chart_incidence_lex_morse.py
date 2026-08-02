#!/usr/bin/env python3
"""Exact lexicographic algebraic-Morse census for the 31 n=8 charts.

The 31 pure target-row orbits meet exactly 31 mixed support-column orbits.
This checker builds their integer incidence matrix, tests ordinary support
matchings, and performs exact rational lexicographic column elimination.

The hoped-for matching with only charts 25 and 26 critical does not exist:
an explicit Hall set has deficiency five, and the integer incidence matrix
has rank only 24.  Lex elimination nevertheless gives an acyclic algebraic
unit matching after repaired-column operations.  Its critical row types are
charts 25 through 31 and its critical column types are recorded below.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "verify_n8_target_triple_localization_orbits.py"
SPEC = importlib.util.spec_from_file_location("n8_target_charts", SOURCE_PATH)
CHARTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHARTS)

SOURCE = CHARTS.SOURCE
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "0a1c27a864ed6b21734ddad26483c41e699b0a791d2717ad82e2d2b10d9d885f"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_scaled(target, source, scale):
    for index, coefficient in source.items():
        output = target.get(index, QQ(0)) + scale * coefficient
        if output:
            target[index] = output
        else:
            target.pop(index, None)


def replay(columns, representative):
    answer = {}
    for column, coefficient in representative.items():
        add_scaled(answer, columns[column], coefficient)
    return answer


def directed_cycle(edges, matching):
    """Return one alternating cycle in the Forman orientation, if present."""
    output = {("r", row): set() for row in edges}
    output.update({("c", column): set() for column in range(31)})
    for row, columns in edges.items():
        for column in columns:
            if matching.get(row) == column:
                output["r", row].add(("c", column))
            else:
                output["c", column].add(("r", row))

    state = {}
    stack = []
    position = {}

    def visit(vertex):
        state[vertex] = 1
        position[vertex] = len(stack)
        stack.append(vertex)
        for other in sorted(output[vertex]):
            if state.get(other, 0) == 0:
                cycle = visit(other)
                if cycle is not None:
                    return cycle
            elif state[other] == 1:
                return stack[position[other]:] + [other]
        stack.pop()
        position.pop(vertex)
        state[vertex] = 2
        return None

    for vertex in sorted(output):
        if state.get(vertex, 0) == 0:
            cycle = visit(vertex)
            if cycle is not None:
                return cycle
    return None


def maximum_support_matching(edges):
    """Deterministic augmenting-path maximum matching."""
    column_match = {}

    def augment(row, seen):
        for column in sorted(edges[row]):
            if column in seen:
                continue
            seen.add(column)
            if (column not in column_match
                    or augment(column_match[column], seen)):
                column_match[column] = row
                return True
        return False

    for row in sorted(edges):
        augment(row, set())
    return {row: column for column, row in column_match.items()}


def audit():
    rows = tuple(sorted(SOURCE.target_orbit_rows()))
    require(len(rows) == 31, "target chart count changed")
    row_index = {row: index for index, row in enumerate(rows)}
    columns = tuple(sorted(set().union(*(
        SOURCE.incident_columns(row) for row in rows
    ))))
    require(len(columns) == 31, "support-column orbit count changed")
    column_index = {column: index for index, column in enumerate(columns)}

    incidence_columns = []
    edges = {index: set() for index in range(31)}
    for column_number, column in enumerate(columns):
        entries = Counter(
            row_index[output]
            for output in SOURCE.column_outputs(column)
            if output in row_index
        )
        incidence_columns.append({
            row: QQ(coefficient) for row, coefficient in entries.items()
        })
        for row in entries:
            edges[row].add(column_number)

    # Replay the incidence relation from the row side as an independent check.
    for row_number, row in enumerate(rows):
        expected = {
            column_index[column] for column in SOURCE.incident_columns(row)
        }
        require(edges[row_number] == expected,
                f"row/column incidence mismatch on chart {row_number + 1}")

    require(sum(map(len, edges.values())) == 111,
            "support incidence nonzero count changed")
    coefficient_histogram = Counter(
        int(coefficient)
        for column in incidence_columns for coefficient in column.values()
    )
    require(coefficient_histogram == {1: 53, 2: 36, 3: 4,
                                      4: 13, 6: 2, 8: 3},
            "support incidence coefficient histogram changed")

    # Ordinary support matching already refutes the proposed two critical
    # charts.  Alternating reachability gives a sharp Hall witness.
    support_matching = maximum_support_matching(edges)
    require(len(support_matching) == 26,
            "ordinary support matching number changed")
    unmatched_rows = set(range(31)) - set(support_matching)
    column_match = {column: row for row, column in support_matching.items()}
    hall_rows = set(unmatched_rows)
    frontier = list(unmatched_rows)
    hall_columns = set()
    while frontier:
        row = frontier.pop()
        for column in edges[row]:
            if support_matching.get(row) == column:
                continue
            if column in hall_columns:
                continue
            hall_columns.add(column)
            if (column in column_match
                    and column_match[column] not in hall_rows):
                hall_rows.add(column_match[column])
                frontier.append(column_match[column])
    require(
        tuple(sorted(row + 1 for row in hall_rows))
        == (7, 8, 16, 17, 18, 20, 21, 23, 25, 26, 27, 28, 29),
        "Hall row witness changed",
    )
    require(
        tuple(sorted(column + 1 for column in hall_columns))
        == (13, 14, 17, 22, 24, 25, 27, 30),
        "Hall column witness changed",
    )
    require(
        set().union(*(edges[row] for row in hall_rows)) == hall_columns,
        "reported Hall columns are not the full neighbor set",
    )
    require(len(hall_rows) - len(hall_columns) == 5,
            "Hall deficiency changed")

    # The naive row-then-column lex matching is not a discrete-Morse
    # matching: it contains an explicit alternating four-cycle.
    raw_matching = {}
    used_columns = set()
    for row in range(31):
        available = sorted(edges[row] - used_columns)
        if available:
            raw_matching[row] = available[0]
            used_columns.add(available[0])
    require(len(raw_matching) == 24, "raw lex matching size changed")
    raw_cycle = directed_cycle(edges, raw_matching)
    require(
        raw_cycle == [
            ("r", 1), ("c", 1), ("r", 3), ("c", 6), ("r", 1)
        ],
        f"raw lex alternating cycle changed: {raw_cycle}",
    )

    # Exact lex column elimination.  Representatives retain provenance in
    # the original 31 support columns.  Every normalized tail is supported
    # strictly above its pivot row, which is the acyclicity statistic.
    pivots = {}
    pivot_columns = {}
    pivot_representatives = {}
    zero_representatives = {}
    repair_steps = 0
    for column_number, source in enumerate(incidence_columns):
        vector = dict(source)
        representative = {column_number: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                normalized = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                normalized_rep = {
                    column: coefficient / value
                    for column, coefficient in representative.items()
                }
                require(replay(incidence_columns, normalized_rep) == normalized,
                        "lex pivot provenance replay failed")
                require(normalized[pivot] == 1,
                        "lex pivot did not normalize to a unit")
                require(all(row > pivot for row in normalized if row != pivot),
                        "lex gradient tail failed to raise the chart index")
                pivots[pivot] = normalized
                pivot_columns[pivot] = column_number
                pivot_representatives[pivot] = normalized_rep
                break
            add_scaled(vector, pivots[pivot], -value)
            add_scaled(representative, pivot_representatives[pivot], -value)
            repair_steps += 1
            require(not vector or min(vector) > pivot,
                    "a lex repair did not raise its leading row")
        if not vector:
            require(not replay(incidence_columns, representative),
                    "zero repaired column did not replay")
            zero_representatives[column_number] = representative

    critical_rows = tuple(
        row + 1 for row in range(31) if row not in pivots
    )
    critical_columns = tuple(
        column + 1 for column in sorted(zero_representatives)
    )
    require(len(pivots) == 24, "lex incidence rank changed")
    require(critical_rows == (25, 26, 27, 28, 29, 30, 31),
            "lex critical chart types changed")
    require(critical_columns == (18, 19, 21, 23, 26, 29, 31),
            "lex critical column types changed")
    require(repair_steps == 118, "lex repair count changed")

    gradient_tails = tuple(
        (
            pivot + 1,
            pivot_columns[pivot] + 1,
            tuple(
                (row + 1, coefficient.numerator, coefficient.denominator)
                for row, coefficient in sorted(pivots[pivot].items())
                if row != pivot
            ),
        )
        for pivot in sorted(pivots)
    )
    tail_digest = sha256(
        json.dumps(gradient_tails, separators=(",", ":")).encode()
    ).hexdigest()

    critical_chart_records = {
        str(index): CHARTS.chart_record(rows[index - 1])
        for index in critical_rows
    }
    # Make the nested tuple records JSON-stable and human-readable.
    for record in critical_chart_records.values():
        record["mixed_types"] = [
            [list(key[0]), list(key[1]), multiplicity]
            for key, multiplicity in record["mixed_types"]
        ]
        record["cubic_components"] = list(record["cubic_components"])

    return {
        "target_chart_orbits": len(rows),
        "support_column_orbits": len(columns),
        "incidence_nonzeros": sum(map(len, edges.values())),
        "incidence_coefficient_histogram": {
            str(key): value for key, value in sorted(coefficient_histogram.items())
        },
        "ordinary_support_matching_number": len(support_matching),
        "hall_rows": [row + 1 for row in sorted(hall_rows)],
        "hall_columns": [column + 1 for column in sorted(hall_columns)],
        "hall_deficiency": len(hall_rows) - len(hall_columns),
        "raw_lex_matching_size": len(raw_matching),
        "raw_lex_cycle": [f"{kind}{index + 1}" for kind, index in raw_cycle],
        "lex_algebraic_rank": len(pivots),
        "lex_repair_steps": repair_steps,
        "lex_critical_rows": list(critical_rows),
        "lex_critical_columns": list(critical_columns),
        "gradient_tail_terms": sum(len(item[2]) for item in gradient_tails),
        "gradient_tail_sha256": tail_digest,
        "critical_chart_records": critical_chart_records,
        "two_critical_chart_proposal": False,
        "scope_guard": (
            "finite n=8 S8xS3 chart/support incidence only; no uniform "
            "classification of coloured cubic supports"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen chart-incidence Morse ledger changed")
    print(
        "n=8 chart-incidence Morse census: PASS; rank 24, "
        "critical charts 25-31 (not only 25/26); lex repaired tails acyclic"
    )
    print(json.dumps(ledger, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
