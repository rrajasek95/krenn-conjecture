#!/usr/bin/env python3
"""Incremental persistent-basis continuation for full normalized Fh D12."""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import struct
import subprocess
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROOT_STAR_PATH = (
    ROOT / "computations/unaudited-codex-n8-chart26-fh-root-star-2026-08-23"
    / "audit_fh_root_star.py"
)
BINARY = HERE / "target/release/fh-d12-incremental"
BASIS = HERE / "incremental_basis.bin"
NEXT_BASIS = HERE / "incremental_basis_next.bin"
ROWS_STATE = HERE / "incremental_rows.bin"
ROUND_ROWS = HERE / "incremental_round_rows.bin"
ROW_MAP = HERE / "incremental_row_map.bin"
INPUT = HERE / "incremental_input.txt"
OUTPUT = HERE / "incremental_output.txt"
CHECKPOINT = HERE / "checkpoint_fh_degree12_incremental.json"
RESULTS = HERE / "results_fh_degree12_incremental.json"
ROUND_JOURNAL = HERE / "incremental_round_journal"
ROUND_CHECKPOINT = HERE / "checkpoint_fh_degree12_incremental_round.json"
PRIME = 1_073_741_827
WALL_CAP_SECONDS = 20 * 60
RSS_CAP_BYTES = 16 * 1024 ** 3
FROZEN = [
    (56, 1, 1, 2, 17, 15), (1438, 16, 16, 2, 37, 35),
    (4663, 51, 51, 2, 102, 93), (12410, 144, 144, 3, 129, 116),
    (21877, 260, 260, 2, 33, 31), (24501, 291, 291, 2, 20, 18),
    (26194, 309, 309, 2, 20, 17), (27771, 326, 326, 11, 103, 76),
    (34477, 402, 402, 5, 42, 32), (37304, 434, 434, 4, 24, 20),
    (39002, 454, 454, 14, 99, 78), (45934, 532, 532, 8, 56, 43),
    (49728, 575, 575, 26, 197, 139), (62095, 714, 714, 11, 64, 50),
    (66554, 764, 764, 33, 252, 183), (82434, 947, 947, 90, 793, 508),
    (125423, 1455, 1455, 177, 1587, 981),
    (208112, 2436, 2436, 4, 24, 18),
    (209578, 2454, 2454, 32, 282, 198),
    (226335, 2652, 2652, 10, 62, 48),
    (230423, 2700, 2700, 75, 596, 349),
    (260166, 3049, 3049, 279, 2134, 1151),
    (355170, 4200, 4200, 625, 4112, 2048),
    (522058, 6248, 6248, 906, 5250, 1790),
    (664133, 8038, 8038, 1495, 8451, 3198),
    (914940, 11236, 11236, 2753, 16592, 7291),
    (1473022, 18527, 18527, 4128, 22587, 7316),
]


class BoundedStop(Exception):
    pass


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


ROOT_STAR = load(ROOT_STAR_PATH, "n8_fh_d12_incremental_root")


def peak_rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if value > 10_000_000 else value * 1024)


def check_cap(started, label, wall_cap_seconds):
    elapsed = time.monotonic() - started
    if elapsed >= wall_cap_seconds or peak_rss_bytes() >= RSS_CAP_BYTES:
        raise BoundedStop({"label": label, "elapsed_seconds": elapsed,
                           "peak_rss_bytes": peak_rss_bytes()})


def record_column(column):
    return [column[0], column[1].hex()]


def parse_column(record):
    return int(record[0]), bytes.fromhex(record[1])


def save_rows_to(path, rows):
    with path.open("wb") as output:
        output.write(struct.pack("<Q", len(rows)))
        for row in rows:
            output.write(bytes([len(row)]))
            output.write(row)


def load_rows_from(path):
    with path.open("rb") as source:
        count = struct.unpack("<Q", source.read(8))[0]
        rows = []
        for _ in range(count):
            size = source.read(1)[0]
            rows.append(source.read(size))
        require(not source.read(1), "trailing row-state bytes")
    return tuple(rows)


def save_rows(rows):
    save_rows_to(ROWS_STATE, rows)


def load_rows():
    return load_rows_from(ROWS_STATE)


def save_map(old_rows, row_index):
    with ROW_MAP.open("wb") as output:
        output.write(struct.pack("<Q", len(old_rows)))
        previous = -1
        for row in old_rows:
            value = row_index[row]
            require(value > previous, "row embedding is not order preserving")
            output.write(struct.pack("<I", value))
            previous = value


def parse_result(rows):
    lines = OUTPUT.read_text().splitlines()
    require(lines, "incremental Rust solver emitted no output")
    fields = lines[0].split()
    require(len(fields) == 8
            and fields[0] == "KRENN_FH_D12_INCREMENTAL_RESULT_V1"
            and int(fields[1]) == PRIME,
            "bad incremental result header")
    rank, remainder, support, pairing, old_count, new_count = map(int, fields[2:])
    require(new_count == len(rows), "incremental coordinate census changed")
    dual = {}
    for line in lines[1:]:
        label, index, coefficient = line.split()
        require(label == "DUAL", "bad dual line")
        dual[rows[int(index)]] = int(coefficient)
    require(len(dual) == support, "incremental dual census changed")
    return {"rank": rank, "remainder": remainder, "pairing": pairing,
            "dual": dual, "old_coordinates": old_count}


def save_checkpoint(processed, pending, ordered_rows, ledger, started):
    save_rows(ordered_rows)
    payload = {
        "format": "n8-fh-d12-incremental-checkpoint-v1",
        "status": "RESUMABLE_AFTER_COMPLETED_ROUND",
        "processed_columns": [record_column(c) for c in sorted(processed)],
        "pending_columns": [record_column(c) for c in sorted(pending)],
        "basis_file": BASIS.name,
        "rows_file": ROWS_STATE.name,
        "completed_rounds": len(ledger),
        "ledger": ledger,
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "peak_rss_bytes_nonlogical": peak_rss_bytes(),
    }
    CHECKPOINT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def sha256_file(path):
    digest = sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def journal_progress():
    answer = []
    if not ROUND_JOURNAL.exists():
        return answer
    for path in sorted(ROUND_JOURNAL.glob("batch_*.bin")):
        with path.open("rb") as source:
            require(source.read(16) == b"FH_D12_BATCH_V1\0",
                    "bad within-round batch magic")
            prime, coordinates, base_rank, start, end, records = struct.unpack(
                "<QQQQQQ", source.read(48))
        require(prime == PRIME and start == (answer[-1]["end"] if answer else 0),
                "within-round journal is not contiguous")
        answer.append({"file": path.name, "coordinates": coordinates,
                       "base_rank": base_rank, "start": start, "end": end,
                       "new_pivots": records, "bytes": path.stat().st_size})
    return answer


def save_round_checkpoint(round_index, ordered_rows, new_columns, ledger, status):
    batches = journal_progress()
    payload = {
        "format": "n8-fh-d12-incremental-within-round-v1",
        "status": status,
        "round": round_index,
        "base_frozen_tuple": [ledger[-1][key] for key in (
            "rows", "columns", "rank", "dual_support",
            "incident_column_orbits", "new_violating_column_orbits")],
        "row_coordinates": len(ordered_rows),
        "pending_columns_total": len(new_columns),
        "completed_pending_columns": batches[-1]["end"] if batches else 0,
        "journal_batches": batches,
        "basis_file": BASIS.name,
        "row_map_file": ROW_MAP.name,
        "row_map_sha256": sha256_file(ROW_MAP),
        "invariant": (
            "accepted r26 basis is immutable; each journal batch contains "
            "only newly admitted normalized pivots and is fsynced before an "
            "atomic rename"
        ),
    }
    if INPUT.exists():
        payload["materialized_input_file"] = INPUT.name
        payload["materialized_input_sha256"] = sha256_file(INPUT)
    if ROUND_ROWS.exists():
        payload["materialized_rows_file"] = ROUND_ROWS.name
        payload["materialized_rows_sha256"] = sha256_file(ROUND_ROWS)
    temporary = ROUND_CHECKPOINT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(ROUND_CHECKPOINT)


def audit(resume=False, wall_cap_seconds=WALL_CAP_SECONDS,
          stop_after_accepted_round=False):
    started = time.monotonic()
    require(BINARY.exists(), "build incremental Rust binary")
    source_api, source = ROOT_STAR.load_source()
    output_cache = {}
    pure_terms = tuple(tuple(sorted(
        source.normalized_generator(source.D5.word_code((colour,) * 8)).items(),
        key=lambda item: (len(item[0]), item[0]),
    )) for colour in range(3))

    @lru_cache(None)
    def coefficient_fh(row, colours=(0, 1, 2)):
        if not colours:
            return int(not row)
        total = 0
        for term, coefficient in pure_terms[colours[0]]:
            if len(term) > len(row):
                break
            quotient = ROOT_STAR.quotient_if_divides(row, term)
            if quotient is not None:
                total += coefficient * coefficient_fh(quotient, colours[1:])
        return total

    if resume:
        frozen = json.loads(CHECKPOINT.read_text())
        processed = {parse_column(x) for x in frozen["processed_columns"]}
        pending = {parse_column(x) for x in frozen["pending_columns"]}
        ledger = list(frozen["ledger"])
        old_rows = load_rows()
        require(BASIS.exists(), "checkpoint basis missing")
        if len(ledger) == len(FROZEN):
            observed = tuple(ledger[-1][key] for key in (
                "rows", "columns", "rank", "dual_support",
                "incident_column_orbits", "new_violating_column_orbits"))
            require(observed == FROZEN[-1]
                    and len(processed) == 18_527 and len(pending) == 7_316,
                    "frozen r26 continuation guard changed")
    else:
        processed = set()
        pending = set(source.bounded_incident_columns(
            {b"": Fraction(1)}, maximum_output_degree=12
        ))
        ledger = []
        old_rows = ()
        for path in (BASIS, NEXT_BASIS, ROWS_STATE):
            if path.exists():
                path.unlink()

    terminal = None
    while True:
        check_cap(started, f"round_{len(ledger)}_start", wall_cap_seconds)
        new_columns = set(pending)
        current_columns = processed | new_columns
        rows = set(old_rows)
        for column in new_columns:
            rows.update(output_cache.setdefault(
                column, source_api.invariant_entries(source, column)
            ))
        new_rows = rows - set(old_rows)
        for column in processed:
            entries = output_cache.setdefault(
                column, source_api.invariant_entries(source, column)
            )
            require(not (set(entries) & new_rows),
                    "an old column is nonzero on a newly discovered row")
        ordered_rows = tuple(sorted(rows, key=lambda row: (-len(row), row)))
        row_index = {row: index for index, row in enumerate(ordered_rows)}
        if old_rows:
            save_map(old_rows, row_index)
        save_rows_to(ROUND_ROWS, ordered_rows)

        target = []
        for index, row in enumerate(ordered_rows):
            value = coefficient_fh(row) % PRIME
            if value:
                target.append((index, value))
            if index and index % 500_000 == 0:
                print("TARGET", index, "/", len(ordered_rows), "elapsed",
                      round(time.monotonic() - started, 3), flush=True)
                check_cap(started, f"target_{index}", wall_cap_seconds)
        vectors = []
        for column in new_columns:
            vector = {row_index[row]: coefficient % PRIME
                      for row, coefficient in output_cache[column].items()
                      if coefficient % PRIME}
            vectors.append((min(vector), len(vector), column, vector))
        vectors.sort(key=lambda item: (item[0], item[1], item[2]))
        with INPUT.open("w", encoding="ascii") as output:
            output.write(f"KRENN_FH_D12_INCREMENTAL_V1 {PRIME} "
                         f"{len(ordered_rows)} {len(vectors)} {WALL_CAP_SECONDS}\n")
            output.write("TARGET " + str(len(target)))
            for index, value in target:
                output.write(f" {index} {value}")
            output.write("\n")
            for _minimum, _support, _column, vector in vectors:
                output.write("VECTOR " + str(len(vector)))
                for index, value in sorted(vector.items()):
                    output.write(f" {index} {value}")
                output.write("\n")

        save_round_checkpoint(len(ledger), ordered_rows, new_columns, ledger,
                              "READY_OR_PARTIALLY_REDUCED")
        remaining = wall_cap_seconds - (time.monotonic() - started)
        if remaining <= 0:
            raise BoundedStop({"label": "after_input", "elapsed_seconds":
                               time.monotonic() - started})
        arguments = [str(BINARY), str(BASIS) if old_rows else "-",
                     str(ROW_MAP) if old_rows else "-", str(NEXT_BASIS),
                     str(ROUND_JOURNAL)]
        with INPUT.open("rb") as input_file, OUTPUT.open("wb") as output_file:
            try:
                completed = subprocess.run(arguments, stdin=input_file,
                    stdout=output_file, check=False, timeout=remaining)
            except subprocess.TimeoutExpired as error:
                save_round_checkpoint(len(ledger), ordered_rows, new_columns,
                                      ledger, "INTERRUPTED_RESUMABLE")
                raise BoundedStop({"label": "incremental_hard_wall",
                    "elapsed_seconds": time.monotonic() - started,
                    "within_round_checkpoint": ROUND_CHECKPOINT.name,
                    "completed_pending_columns": (
                        journal_progress()[-1]["end"]
                        if journal_progress() else 0)}) from error
        require(completed.returncode == 0,
                f"incremental Rust failed with {completed.returncode}")
        modular = parse_result(ordered_rows)
        NEXT_BASIS.replace(BASIS)
        require(modular["rank"] == len(current_columns),
                "incremental column rank stopped being full")

        candidates = source.bounded_incident_columns(
            modular["dual"], maximum_output_degree=12
        )
        violating = set()
        for index, column in enumerate(candidates, 1):
            entries = output_cache.setdefault(
                column, source_api.invariant_entries(source, column)
            )
            value = sum(coefficient * modular["dual"].get(row, 0)
                        for row, coefficient in entries.items()) % PRIME
            if value and column not in current_columns:
                violating.add(column)
            if index % 4096 == 0:
                print("SCAN", index, "/", len(candidates), flush=True)
                check_cap(started, f"scan_{len(ledger)}_{index}",
                          wall_cap_seconds)
        record = {
            "round": len(ledger), "rows": len(rows),
            "columns": len(current_columns), "rank": modular["rank"],
            "dual_support": len(modular["dual"]),
            "incident_column_orbits": len(candidates),
            "new_violating_column_orbits": len(violating),
        }
        if len(ledger) < len(FROZEN):
            observed = tuple(record[key] for key in (
                "rows", "columns", "rank", "dual_support",
                "incident_column_orbits", "new_violating_column_orbits"))
            require(observed == FROZEN[len(ledger)],
                    f"incremental/frozen divergence round {len(ledger)}: {observed}")
            record["frozen_shape_match"] = True
        ledger.append(record)
        print("ROUND", record, "elapsed", round(time.monotonic()-started, 3),
              flush=True)
        if not violating:
            terminal = {"status": "MODULAR_STALL_EXACT_Q_REPLAY_REQUIRED"}
            processed = current_columns
            pending = set()
            old_rows = ordered_rows
            save_checkpoint(processed, pending, old_rows, ledger, started)
            break
        processed = current_columns
        pending = violating
        old_rows = ordered_rows
        save_checkpoint(processed, pending, old_rows, ledger, started)
        accepted_journal = HERE / f"incremental_round_journal_r{record['round']}_accepted"
        require(not accepted_journal.exists(), "accepted journal archive exists")
        ROUND_JOURNAL.replace(accepted_journal)
        save_round_checkpoint(record["round"], old_rows, new_columns, ledger,
                              "ROUND_ACCEPTED_AND_SCANNED")
        if stop_after_accepted_round:
            terminal = {
                "status": "ROUND_ACCEPTED_SCAN_ONLY",
                "next_crossing_column_orbits": len(violating),
                "next_round_allowed_by_4096_guard": len(violating) <= 4096,
            }
            break

    payload = {"format": "n8-fh-d12-incremental-result-v1", **terminal,
               "completed_rounds": len(ledger), "last_round": ledger[-1],
               "checkpoint": CHECKPOINT.name,
               "scope": "modular full-Fh degree12 only; exact-Q terminal replay required"}
    RESULTS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def package_current_interface():
    """Serialize the already-frozen r27 coordinate interface without solving."""
    source_api, source = ROOT_STAR.load_source()
    frozen = json.loads(CHECKPOINT.read_text())
    ledger = list(frozen["ledger"])
    processed = {parse_column(x) for x in frozen["processed_columns"]}
    pending = {parse_column(x) for x in frozen["pending_columns"]}
    old_rows = load_rows()
    require(len(ledger) == len(FROZEN) and len(processed) == 18_527
            and len(pending) == 7_316, "r26 materialization census changed")
    observed = tuple(ledger[-1][key] for key in (
        "rows", "columns", "rank", "dual_support",
        "incident_column_orbits", "new_violating_column_orbits"))
    require(observed == FROZEN[-1], "r26 frozen tuple changed")
    rows = set(old_rows)
    for index, column in enumerate(pending, 1):
        rows.update(source_api.invariant_entries(source, column))
        if index % 1024 == 0:
            print("INTERFACE", index, "/", len(pending), flush=True)
    ordered_rows = tuple(sorted(rows, key=lambda row: (-len(row), row)))
    require(len(ordered_rows) == 1_997_290,
            "materialized r27 row census changed")
    save_rows_to(ROUND_ROWS, ordered_rows)
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    save_map(old_rows, row_index)
    with INPUT.open("rb") as stream:
        header = stream.readline().decode("ascii").split()
    require(header[:4] == ["KRENN_FH_D12_INCREMENTAL_V1", str(PRIME),
                            "1997290", "7316"],
            "materialized input header changed")
    save_round_checkpoint(27, ordered_rows, pending, ledger,
                          "INTERRUPTED_RESUMABLE_MATERIALIZED")
    payload = {
        "status": "PASS", "round": 27,
        "row_coordinates": len(ordered_rows),
        "pending_columns": len(pending),
        "journal_completed_columns": journal_progress()[-1]["end"],
        "round_rows_sha256": sha256_file(ROUND_ROWS),
        "row_map_sha256": sha256_file(ROW_MAP),
        "input_sha256": sha256_file(INPUT),
    }
    print(json.dumps(payload, sort_keys=True))
    return payload


def resume_materialized_round(wall_cap_seconds):
    """Resume only the frozen, serialized r27 reduction and scan once."""
    started = time.monotonic()
    frozen = json.loads(CHECKPOINT.read_text())
    ledger = list(frozen["ledger"])
    processed = {parse_column(x) for x in frozen["processed_columns"]}
    pending = {parse_column(x) for x in frozen["pending_columns"]}
    require(len(ledger) == 27 and len(processed) == 18_527
            and len(pending) == 7_316, "materialized-resume base changed")
    observed = tuple(ledger[-1][key] for key in (
        "rows", "columns", "rank", "dual_support",
        "incident_column_orbits", "new_violating_column_orbits"))
    require(observed == FROZEN[-1], "materialized-resume r26 guard changed")
    interface = json.loads(ROUND_CHECKPOINT.read_text())
    require(interface["row_coordinates"] == 1_997_290
            and interface["pending_columns_total"] == 7_316
            and interface["materialized_rows_sha256"] == sha256_file(ROUND_ROWS)
            and interface["materialized_input_sha256"] == sha256_file(INPUT)
            and interface["row_map_sha256"] == sha256_file(ROW_MAP),
            "materialized r27 interface changed")
    ordered_rows = load_rows_from(ROUND_ROWS)
    require(len(ordered_rows) == 1_997_290, "r27 row table changed")
    arguments = [str(BINARY), str(BASIS), str(ROW_MAP), str(NEXT_BASIS),
                 str(ROUND_JOURNAL)]
    with INPUT.open("rb") as input_file, OUTPUT.open("wb") as output_file:
        try:
            completed = subprocess.run(arguments, stdin=input_file,
                stdout=output_file, check=False, timeout=wall_cap_seconds)
        except subprocess.TimeoutExpired as error:
            save_round_checkpoint(27, ordered_rows, pending, ledger,
                                  "INTERRUPTED_RESUMABLE_MATERIALIZED")
            raise BoundedStop({
                "label": "materialized_incremental_hard_wall",
                "elapsed_seconds": time.monotonic() - started,
                "within_round_checkpoint": ROUND_CHECKPOINT.name,
                "completed_pending_columns": journal_progress()[-1]["end"],
            }) from error
    require(completed.returncode == 0,
            f"materialized incremental Rust failed with {completed.returncode}")
    modular = parse_result(ordered_rows)
    NEXT_BASIS.replace(BASIS)
    current_columns = processed | pending
    require(modular["rank"] == len(current_columns),
            "r27 materialized column rank stopped being full")
    source_api, source = ROOT_STAR.load_source()
    candidates = source.bounded_incident_columns(
        modular["dual"], maximum_output_degree=12)
    violating = set()
    for index, column in enumerate(candidates, 1):
        entries = source_api.invariant_entries(source, column)
        value = sum(coefficient * modular["dual"].get(row, 0)
                    for row, coefficient in entries.items()) % PRIME
        if value and column not in current_columns:
            violating.add(column)
        if index % 4096 == 0:
            print("SCAN", index, "/", len(candidates), flush=True)
            check_cap(started, f"materialized_scan_{index}", wall_cap_seconds)
    record = {
        "round": 27, "rows": len(ordered_rows),
        "columns": len(current_columns), "rank": modular["rank"],
        "dual_support": len(modular["dual"]),
        "incident_column_orbits": len(candidates),
        "new_violating_column_orbits": len(violating),
        "materialized_resume": True,
    }
    ledger.append(record)
    save_checkpoint(current_columns, violating, ordered_rows, ledger, started)
    accepted_journal = HERE / "incremental_round_journal_r27_accepted"
    require(not accepted_journal.exists(), "r27 accepted journal already exists")
    ROUND_JOURNAL.replace(accepted_journal)
    status = ("MODULAR_STALL_EXACT_Q_REPLAY_REQUIRED" if not violating
              else "ROUND_ACCEPTED_SCAN_ONLY")
    payload = {
        "format": "n8-fh-d12-incremental-result-v1",
        "status": status, "completed_rounds": len(ledger),
        "last_round": record,
        "next_round_allowed_by_4096_guard": len(violating) <= 4096,
        "scope": "modular full-Fh degree12; one accepted r27 scan only",
    }
    RESULTS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--wall-cap-seconds", type=int,
                        default=WALL_CAP_SECONDS)
    parser.add_argument("--stop-after-accepted-round", action="store_true")
    parser.add_argument("--package-current-interface", action="store_true")
    parser.add_argument("--resume-materialized-round", action="store_true")
    args = parser.parse_args()
    try:
        require(0 < args.wall_cap_seconds <= WALL_CAP_SECONDS,
                "wall cap must be in 1..1200 seconds")
        require(not (args.package_current_interface
                     and args.resume_materialized_round),
                "choose one materialized action")
        if args.package_current_interface:
            require(args.resume is False and args.stop_after_accepted_round is False,
                    "interface packaging takes no run-mode flags")
            result = package_current_interface()
        elif args.resume_materialized_round:
            require(args.resume is False and args.stop_after_accepted_round is False,
                    "materialized resume takes no other run-mode flags")
            result = resume_materialized_round(args.wall_cap_seconds)
        else:
            result = audit(args.resume, args.wall_cap_seconds,
                           args.stop_after_accepted_round)
    except BoundedStop as stopped:
        result = {"format": "n8-fh-d12-incremental-result-v1",
                  "status": "BOUNDED_RESUMABLE_UNRESOLVED",
                  "detail": stopped.args[0]}
        RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
