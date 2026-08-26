#!/usr/bin/env python3
"""Exact Q/Z lift of the boundary D12 r13 dual through global private rows."""

from collections import defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from math import gcd, lcm
import importlib.util
import json
from pathlib import Path
import resource
import time


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "run_d12_lazy_cegar.py"
CHECKPOINT = HERE / "checkpoint_d12_incremental_cegar.json"
RESULT = HERE / "results_d12_private_separator_exact.json"
P1 = 1_073_741_827
P2 = 1_073_741_789
WALL = 20 * 60
RSS = 12 * 1024 ** 3
QQ = Fraction


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None: raise RuntimeError(path)
    spec.loader.exec_module(module)
    return module


S = load(SOURCE_PATH, "chart1_boundary_exact_private_source")


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


def small_rational_lift(residue, prime, bound=64):
    candidates = set()
    for denominator in range(1, bound + 1):
        for numerator in range(-bound, bound + 1):
            value = QQ(numerator, denominator)
            if numerator * pow(denominator, -1, prime) % prime == residue:
                candidates.add(value)
    require(len(candidates) == 1,
            f"nonunique small rational lift {residue}: {sorted(candidates)}")
    return candidates.pop()


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

    target = {}
    for left, cl in provider.pure[0].items():
        for middle, cm in provider.pure[1].items():
            prefix = bytes(sorted(left + middle))
            for right, cr in provider.pure[2].items():
                row = bytes(sorted(prefix + right))
                representative = canonical_row(row)
                coefficient = cl * cm * cr
                previous = target.setdefault(representative, coefficient)
                require(previous == coefficient, "target invariance changed")
        check(started, "target")
    require(len(target) == 32965, "target support changed")

    checkpoint = json.loads(CHECKPOINT.read_text())
    sequence = [parse_column(record)
                for record in checkpoint["column_insertion_sequence"]]
    selected = set(sequence)
    require(len(sequence) == len(selected) == 7516, "selected sequence changed")

    old_modular = {bytes.fromhex(row): int(value)
                   for row, value in checkpoint["last_modular_dual"]}
    old_exact = {row: small_rational_lift(value, P1)
                 for row, value in old_modular.items()}
    require(len(old_exact) == 17, "r13 dual support changed")

    current_rows = set(target)
    old_q_failures = []
    old_p2_failures = []
    for position, column in enumerate(sequence, 1):
        entries = invariant_entries(column)
        current_rows.update(entries)
        q_pair = sum(QQ(coefficient) * old_exact.get(row, 0)
                     for row, coefficient in entries.items())
        p2_pair = sum(coefficient * (
            old_exact.get(row, 0).numerator
            * pow(old_exact.get(row, QQ(0)).denominator, -1, P2)
            if old_exact.get(row, 0) else 0
        ) for row, coefficient in entries.items()) % P2
        if q_pair: old_q_failures.append([position - 1, *parse_column([column[0], column[1].hex()]), q_pair])
        if p2_pair: old_p2_failures.append(position - 1)
        if position % 512 == 0:
            print("SELECTED", position, "/", len(sequence), "rows", len(current_rows),
                  "rss", peak_rss(), flush=True)
            check(started, f"selected_{position}")
    require(not old_q_failures, "small Q lift misses selected columns")
    require(not old_p2_failures, "small Q lift misses selected columns at p2")

    old_target_pairing = sum(QQ(coefficient) * old_exact.get(row, 0)
                             for row, coefficient in target.items())
    require(old_target_pairing, "old exact dual lost target pairing")
    old_target_pairing_p2 = sum(
        coefficient * old_exact.get(row, QQ(0)).numerator
        * pow(old_exact.get(row, QQ(0)).denominator, -1, P2)
        for row, coefficient in target.items() if old_exact.get(row, 0)
    ) % P2
    require(old_target_pairing_p2, "old dual target pairing vanished at p2")

    candidates = provider.incident_columns(old_exact)
    pending = []
    pending_entries = []
    pending_pairings = []
    for position, column in enumerate(sorted(candidates), 1):
        entries = invariant_entries(column)
        pairing = sum(QQ(coefficient) * old_exact.get(row, 0)
                      for row, coefficient in entries.items())
        if pairing and column not in selected:
            pending.append(column)
            pending_entries.append(entries)
            pending_pairings.append(pairing)
        if position % 256 == 0: check(started, f"old_incident_{position}")
    require(len(candidates) == 1204 and len(pending) == 1186,
            "r13 incident/violation census changed")

    # First establish shell-private ownership, then demand a row whose complete
    # incident-column census is the singleton owner column.
    owner_count = defaultdict(int)
    owner_xor = defaultdict(int)
    outside_rows = []
    for index, entries in enumerate(pending_entries):
        rows = tuple(row for row in entries if row not in current_rows)
        outside_rows.append(rows)
        for row in rows:
            owner_count[row] += 1
            owner_xor[row] ^= index
    shell_private = [[] for _ in pending]
    for row, count in owner_count.items():
        if count == 1: shell_private[owner_xor[row]].append(row)
    require(all(shell_private), "a pending column lost shell-private ownership")

    global_witnesses = []
    global_incident_histogram = defaultdict(int)
    for index, (column, rows) in enumerate(zip(pending, shell_private)):
        witness = None
        for row in sorted(rows, key=lambda item: (-len(item), item)):
            incident = provider.incident_columns_for_row(row)
            global_incident_histogram[len(incident)] += 1
            if set(incident) == {column}:
                witness = row
                break
        if witness is None:
            global_witnesses.append(None)
        else:
            global_witnesses.append(witness)
        if (index + 1) % 128 == 0:
            print("GLOBAL", index + 1, "/", len(pending), "found",
                  sum(row is not None for row in global_witnesses), flush=True)
            check(started, f"global_{index+1}")

    missing_global = [index for index, row in enumerate(global_witnesses)
                      if row is None]
    if missing_global:
        payload = {
            "format": "n8-chart1-boundary-d12-private-separator-exact-v1",
            "status": "GLOBAL_PRIVATE_LIFT_COUNTERGUARD",
            "old_dual_support": len(old_exact),
            "old_target_pairing": [old_target_pairing.numerator,
                                   old_target_pairing.denominator],
            "incident_column_orbits": len(candidates),
            "pending_column_orbits": len(pending),
            "columns_without_globally_singleton_incident_row": len(missing_global),
            "first_missing_columns": [[pending[index][0], pending[index][1].hex()]
                                      for index in missing_global[:20]],
            "tested_global_incident_size_histogram": sorted(global_incident_histogram.items()),
            "scope": "Exact no-solve counterguard; shell-private does not imply globally private.",
        }
    else:
        extended = dict(old_exact)
        witness_records = []
        for column, entries, pairing, row in zip(
                pending, pending_entries, pending_pairings, global_witnesses):
            coefficient = entries[row]
            require(row not in extended, "new private row already has dual weight")
            value = -pairing / coefficient
            extended[row] = value
            witness_records.append([
                column[0], column[1].hex(), row.hex(), coefficient,
                pairing.numerator, pairing.denominator,
                value.numerator, value.denominator,
            ])

        full_candidates = provider.incident_columns(extended)
        invariant_failures = []
        for position, column in enumerate(sorted(full_candidates), 1):
            entries = invariant_entries(column)
            pairing = sum(QQ(coefficient) * extended.get(row, 0)
                          for row, coefficient in entries.items())
            if pairing: invariant_failures.append([
                column[0], column[1].hex(), pairing.numerator, pairing.denominator
            ])
            if position % 256 == 0: check(started, f"full_invariant_{position}")
        require(not invariant_failures, "extended exact dual has new invariant crossings")

        # Clear denominators and primitive-normalize to an integral functional.
        denominator = reduce(lcm, (value.denominator for value in extended.values()), 1)
        integer = {row: value.numerator * (denominator // value.denominator)
                   for row, value in extended.items()}
        content = reduce(gcd, (abs(value) for value in integer.values() if value), 0)
        integer = {row: value // content for row, value in integer.items()}
        integer_target_pairing = sum(coefficient * integer.get(row, 0)
                                     for row, coefficient in target.items())
        require(integer_target_pairing, "integer dual lost target pairing")

        p2_failures = []
        expanded_failures = []
        expanded_actual_columns = 0
        for position, column in enumerate(sorted(full_candidates), 1):
            entries = invariant_entries(column)
            if sum(coefficient * integer.get(row, 0)
                   for row, coefficient in entries.items()) % P2:
                p2_failures.append([column[0], column[1].hex()])
            for actual in provider.column_orbit(column):
                value = QQ(0)
                for term, coefficient in provider.generator(actual[0]).items():
                    row = bytes(sorted(actual[1] + term))
                    representative_orbit = row_orbit(row)
                    value += (QQ(integer.get(representative_orbit[0], 0),
                                 len(representative_orbit)) * coefficient)
                if value:
                    expanded_failures.append([
                        actual[0], actual[1].hex(), value.numerator, value.denominator
                    ])
                expanded_actual_columns += 1
            if position % 128 == 0: check(started, f"literal_{position}")
        require(not p2_failures, "integer dual fails second-prime replay")
        require(not expanded_failures, "integer dual fails literal expanded replay")
        require(integer_target_pairing % P2,
                "integer target pairing vanishes at second prime")

        payload = {
            "format": "n8-chart1-boundary-d12-private-separator-exact-v1",
            "status": "EXACT_FULL_D12_NONMEMBER_FIRST_BOUNDARY",
            "old_dual": [[row.hex(), value.numerator, value.denominator]
                         for row, value in sorted(old_exact.items())],
            "old_target_pairing": [old_target_pairing.numerator,
                                   old_target_pairing.denominator],
            "old_target_pairing_mod_second_prime": old_target_pairing_p2,
            "pending_column_orbits": len(pending),
            "global_private_witnesses": len(global_witnesses),
            "witness_records": witness_records,
            "integer_dual": [[row.hex(), value]
                             for row, value in sorted(integer.items())],
            "integer_dual_support": len(integer),
            "integer_content_removed": content,
            "integer_target_pairing": integer_target_pairing,
            "integer_target_pairing_mod_second_prime": integer_target_pairing % P2,
            "full_incident_invariant_column_orbits": len(full_candidates),
            "expanded_actual_incident_columns": expanded_actual_columns,
            "second_prime": P2,
            "scope": (
                "Exact homogeneous degree12 Fh nonmembership in chart1 boundary "
                "A_02[0,0]=0 only; no saturation, radical, higher-degree, or atlas inference."
            ),
        }

    payload.update({
        "peak_rss_bytes_nonlogical": peak_rss(),
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "checkpoint_sha256": sha256(CHECKPOINT.read_bytes()).hexdigest(),
    })
    logical = {key: value for key, value in payload.items()
               if not key.endswith("_nonlogical")}
    payload["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"], payload["logical_sha256"], flush=True)


if __name__ == "__main__": main()
