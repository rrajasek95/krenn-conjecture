#!/usr/bin/env python3
"""No-solve private-row audit for boundary D12 accepted/pending columns."""

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import time


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "run_d12_lazy_cegar.py"
CHECKPOINT = HERE / "checkpoint_d12_incremental_cegar.json"
RESULT = HERE / "results_d12_private_ownership.json"
PRIME = 1_073_741_827
WALL = 600
RSS = 12 * 1024 ** 3


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None: raise RuntimeError(path)
    spec.loader.exec_module(module)
    return module


S = load(SOURCE_PATH, "chart1_boundary_private_source")


def require(condition, detail):
    if not condition: raise RuntimeError(detail)


def peak_rss():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if value > 10_000_000 else value * 1024)


def check(started, label):
    require(time.monotonic() - started < WALL, f"wall cap at {label}")
    require(peak_rss() < RSS, f"RSS cap at {label}")


def parse_column(record):
    return int(record[0]), bytes.fromhex(record[1])


def main():
    started = time.monotonic()
    provider = S.Provider()

    def row_orbit(row):
        return tuple(sorted(set(
            bytes(sorted(transform[value] for value in row))
            for transform in provider.transforms
        )))

    def canonical_row(row):
        return row_orbit(row)[0]

    def invariant_entries(column):
        answer = defaultdict(int)
        for code, multiplier in provider.column_orbit(column):
            for term, coefficient in provider.generator(code).items():
                row = bytes(sorted(multiplier + term))
                if row == canonical_row(row): answer[row] += coefficient
        return {row: value for row, value in answer.items() if value}

    # Target support directly, without the literal 992,250-row Counter.
    target_rows = set()
    for left in provider.pure[0]:
        for middle in provider.pure[1]:
            prefix = bytes(sorted(left + middle))
            for right in provider.pure[2]:
                target_rows.add(canonical_row(bytes(sorted(prefix + right))))
        check(started, "target")
    require(len(target_rows) == 32965, "target support changed")

    checkpoint = json.loads(CHECKPOINT.read_text())
    sequence = [parse_column(record)
                for record in checkpoint["column_insertion_sequence"]]
    require(len(sequence) == 7516 and len(set(sequence)) == 7516,
            "accepted sequence changed")
    old_count = 2613
    old_rows = set(target_rows)
    for position, column in enumerate(sequence[:old_count], 1):
        old_rows.update(invariant_entries(column))
        if position % 512 == 0: check(started, f"old_{position}")
    require(len(old_rows) == 125328, "frozen old interface changed")

    # Ownership beyond the old interface across all 4,903 accepted repairs.
    new_outputs = []
    owner_count = defaultdict(int)
    owner_xor = defaultdict(int)
    all_rows = set(old_rows)
    for local_id, column in enumerate(sequence[old_count:]):
        entries = invariant_entries(column)
        rows = tuple(row for row in entries if row not in old_rows)
        new_outputs.append(rows)
        all_rows.update(entries)
        for row in rows:
            owner_count[row] += 1
            owner_xor[row] ^= local_id
        if (local_id + 1) % 512 == 0:
            print("ACCEPTED", local_id + 1, "/", len(sequence)-old_count,
                  "new_rows", len(owner_count), "rss", peak_rss(), flush=True)
            check(started, f"accepted_{local_id+1}")

    private = [[] for _ in new_outputs]
    for row, count in owner_count.items():
        if count == 1:
            private[owner_xor[row]].append(row)
    covered = {index for index, rows in enumerate(private) if rows}
    witnesses = {
        index: min(rows, key=lambda row: (-len(row), row))
        for index, rows in enumerate(private) if rows
    }

    accepted_records = checkpoint["ledger"][7:]
    round_ranges = []
    cursor = 0
    for record in accepted_records:
        count = record["new_violating_column_orbits"]
        ids = range(cursor, cursor + count)
        round_ranges.append({
            "round": record["round"],
            "columns": count,
            "columns_with_global_private_new_row": sum(index in covered for index in ids),
            "private_new_rows": sum(len(private[index]) for index in ids),
        })
        cursor += count
    require(cursor == len(new_outputs), "round partition changed")

    # Literal source replay for the lex-first covered accepted column.
    first_id = min(covered)
    first_column = sequence[old_count + first_id]
    first_row = witnesses[first_id]
    literal_hits = []
    total = 0
    for code, multiplier in provider.column_orbit(first_column):
        for term, coefficient in provider.generator(code).items():
            if bytes(sorted(multiplier + term)) == first_row:
                literal_hits.append([code, multiplier.hex(), term.hex(), coefficient])
                total += coefficient
    first_entries = invariant_entries(first_column)
    require(total == first_entries[first_row], "literal private witness replay failed")

    # Current round-13 pending set from the durable modular dual.  This is a
    # structural census only; it does not update the accepted CEGAR ledger.
    dual = {bytes.fromhex(row): value
            for row, value in checkpoint["last_modular_dual"]}
    require(dual, "missing round13 modular dual")
    candidates = provider.incident_columns(dual)
    selected = set(sequence)
    pending = []
    pending_entries = []
    for position, column in enumerate(sorted(candidates), 1):
        entries = invariant_entries(column)
        pairing = sum(coefficient * dual.get(row, 0)
                      for row, coefficient in entries.items()) % PRIME
        if pairing and column not in selected:
            pending.append(column)
            pending_entries.append(entries)
        if position % 256 == 0: check(started, f"pending_scan_{position}")

    pending_owner_count = defaultdict(int)
    pending_owner_xor = defaultdict(int)
    pending_rows = []
    for local_id, entries in enumerate(pending_entries):
        rows = tuple(row for row in entries if row not in all_rows)
        pending_rows.append(rows)
        for row in rows:
            pending_owner_count[row] += 1
            pending_owner_xor[row] ^= local_id
    pending_private = [[] for _ in pending]
    for row, count in pending_owner_count.items():
        if count == 1: pending_private[pending_owner_xor[row]].append(row)
    pending_covered = [index for index, rows in enumerate(pending_private) if rows]

    payload = {
        "format": "n8-chart1-boundary-d12-private-ownership-v1",
        "status": "EXACT_NO_SOLVE_OWNERSHIP_CENSUS",
        "old_interface": {
            "columns": old_count,
            "rows_including_target": len(old_rows),
        },
        "accepted_repairs": {
            "columns": len(new_outputs),
            "distinct_new_rows": len(owner_count),
            "degree_one_new_rows": sum(value == 1 for value in owner_count.values()),
            "columns_with_global_private_new_row": len(covered),
            "all_columns_have_global_private_new_row": len(covered) == len(new_outputs),
            "private_rows_per_column_histogram": sorted(Counter(
                len(rows) for rows in private
            ).items()),
            "rounds": round_ranges,
            "lex_first_literal_witness": {
                "local_column_id": first_id,
                "column": [first_column[0], first_column[1].hex()],
                "row": first_row.hex(),
                "coefficient": first_entries[first_row],
                "literal_hits": literal_hits,
            },
        },
        "round13_pending": {
            "incident_column_orbits": len(candidates),
            "violating_unselected_column_orbits": len(pending),
            "distinct_new_rows": len(pending_owner_count),
            "degree_one_new_rows": sum(value == 1 for value in pending_owner_count.values()),
            "columns_with_private_new_row": len(pending_covered),
            "all_columns_have_private_new_row": len(pending_covered) == len(pending),
            "private_rows_per_column_histogram": sorted(Counter(
                len(rows) for rows in pending_private
            ).items()),
        },
        "peak_rss_bytes_nonlogical": peak_rss(),
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "scope": (
            "Exact invariant-output ownership relative to the accepted row interface; "
            "no Gaussian elimination, ideal membership, or terminal D12 inference."
        ),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "checkpoint_sha256": sha256(CHECKPOINT.read_bytes()).hexdigest(),
    }
    logical = {key: value for key, value in payload.items()
               if not key.endswith("_nonlogical")}
    payload["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"], payload["logical_sha256"], flush=True)


if __name__ == "__main__": main()
