#!/usr/bin/env python3
"""Incremental modular CEGAR for chart1/A_02[00]=0 at homogeneous D12.

The Rust child retains a sparse pivot basis across accepted rounds.  Python is
the literal source provider and owns all orbit expansion, checkpointing, and
terminal exact replay.  A modular MEMBER or separator is never a theorem.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import threading
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_PATH = HERE / "run_d12_lazy_cegar.py"
RESUME = HERE / "resume_d12_lazy_cegar.json"
BINARY = HERE / "rust-d12-incremental/target/release/chart1-boundary-d12-incremental"
CHECKPOINT = HERE / "checkpoint_d12_incremental_cegar.json"
RESULT = HERE / "results_d12_incremental_cegar.json"
STDERR = HERE / "d12_incremental_cegar.stderr.log"
PRIME = 1_073_741_827
SECOND_PRIME = 1_073_741_789
WALL_CAP_SECONDS = 20 * 60
RSS_CAP_BYTES = 16 * 1024 ** 3
MAX_ROUNDS = 500
QQ = Fraction


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


SOURCE = load(SOURCE_PATH, "chart1_boundary_incremental_source")


def peak_rss_bytes():
    own = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    children = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    own = int(own if own > 10_000_000 else own * 1024)
    children = int(children if children > 10_000_000 else children * 1024)
    return max(own, children)


def live_rss_bytes(pid):
    try:
        value = subprocess.check_output(
            ["ps", "-o", "rss=", "-p", str(pid)], text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return int(value) * 1024 if value else 0
    except (OSError, subprocess.SubprocessError, ValueError):
        return 0


def check_cap(started, label, engine=None):
    elapsed = time.monotonic() - started
    child = live_rss_bytes(engine.process.pid) if engine is not None else 0
    rss = max(peak_rss_bytes(), live_rss_bytes(os.getpid()) + child)
    if elapsed >= WALL_CAP_SECONDS or rss >= RSS_CAP_BYTES:
        raise BoundedStop({
            "label": label,
            "elapsed_seconds": elapsed,
            "peak_or_live_rss_bytes": rss,
        })


def column_record(column):
    return [column[0], column[1].hex()]


def parse_column(record):
    return int(record[0]), bytes.fromhex(record[1])


def atomic_json(path, payload):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def modular_line(tag, entries, row_index, prime):
    terms = []
    for row, coefficient in entries.items():
        value = coefficient % prime
        if value:
            terms.append((row_index[row], value))
    terms.sort()
    require(terms, f"{tag} vanished modulo {prime}")
    return tag + " " + str(len(terms)) + "".join(
        f" {index} {value}" for index, value in terms
    ) + "\n"


class IncrementalEngine:
    def __init__(self, prime, rows, target, stderr_handle, wall_seconds):
        self.prime = prime
        self.rows = list(rows)
        self.row_index = {row: index for index, row in enumerate(self.rows)}
        self.process = subprocess.Popen(
            [str(BINARY)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=stderr_handle, text=True, bufsize=1,
        )
        self.started = time.monotonic()
        self.wall_seconds = wall_seconds
        self.guard_stop = threading.Event()
        self.guard_reason = None
        def guard():
            while not self.guard_stop.wait(2.0):
                combined = live_rss_bytes(os.getpid()) + live_rss_bytes(self.process.pid)
                if combined >= RSS_CAP_BYTES:
                    self.guard_reason = {
                        "label": "combined_live_rss_cap",
                        "combined_live_rss_bytes": combined,
                    }
                    self.process.kill()
                    return
                if self.process.poll() is not None:
                    return
        self.guard_thread = threading.Thread(target=guard, daemon=True)
        self.guard_thread.start()
        require(self.process.stdin is not None and self.process.stdout is not None,
                "failed to open Rust pipes")
        self.input = self.process.stdin
        self.output = self.process.stdout
        self.input.write(f"KRENN_BOUNDARY_D12_INCREMENTAL_V1 {prime} {wall_seconds}\n")
        self.input.write("INIT " + str(len(self.rows)) + " " + str(len(target)))
        for row, coefficient in sorted(target.items(), key=lambda item: self.row_index[item[0]]):
            value = coefficient % prime
            require(value, "target coefficient vanished modulo prime")
            self.input.write(f" {self.row_index[row]} {value}")
        self.input.write("\n")
        self.input.flush()
        fields = self._read().split()
        require(fields == ["INITIALIZED", str(len(self.rows)), str(len(target))],
                f"bad Rust INIT reply: {fields}")

    def _read(self):
        line = self.output.readline()
        if not line:
            code = self.process.poll()
            if code is None:
                try: code = self.process.wait(timeout=2)
                except subprocess.TimeoutExpired: code = None
            if self.guard_reason is not None:
                raise BoundedStop(self.guard_reason)
            if code is not None and time.monotonic() - self.started >= self.wall_seconds - 2:
                raise BoundedStop({
                    "label": "rust_incremental_wall_cap",
                    "engine_exit_code": code,
                    "engine_elapsed_seconds": time.monotonic() - self.started,
                })
            if code is not None and code != 0:
                raise BoundedStop({
                    "label": "rust_incremental_abnormal_exit_unresolved",
                    "engine_exit_code": code,
                    "engine_elapsed_seconds": time.monotonic() - self.started,
                })
            raise RuntimeError(f"Rust incremental engine closed pipe (code {code})")
        return line.rstrip("\n")

    def extend(self, new_rows):
        new_rows = tuple(sorted(set(new_rows), key=lambda row: (len(row), row)))
        for row in new_rows:
            if row not in self.row_index:
                self.row_index[row] = len(self.rows)
                self.rows.append(row)
        self.input.write(f"EXTEND {len(self.rows)}\n")
        self.input.flush()
        require(self._read() == f"EXTENDED {len(self.rows)}", "bad Rust EXTEND reply")

    def add(self, columns, output_cache):
        columns = tuple(columns)
        self.input.write(f"ADD {len(columns)}\n")
        for column in columns:
            self.input.write(modular_line(
                "VECTOR", output_cache[column], self.row_index, self.prime
            ))
        self.input.flush()
        fields = self._read().split()
        require(len(fields) == 5 and fields[0] == "ADDED"
                and int(fields[1]) == len(columns), f"bad Rust ADD reply: {fields}")
        return {
            "rank": int(fields[2]),
            "rank_increment": int(fields[3]),
            "zero_columns": int(fields[4]),
        }

    def solve(self):
        self.input.write("SOLVE\n")
        self.input.flush()
        fields = self._read().split()
        require(len(fields) == 6 and fields[0] == "RESULT", f"bad SOLVE reply: {fields}")
        status = fields[1]
        result = {
            "status": status,
            "rank": int(fields[2]),
            "remainder_support": int(fields[3]),
            "dual_support": int(fields[4]),
            "target_pairing": int(fields[5]),
            "dual": {},
        }
        while True:
            record = self._read()
            if record == "END": break
            label, index, value = record.split()
            require(label == "DUAL", "bad dual row")
            row = self.rows[int(index)]
            require(row not in result["dual"], "duplicate dual row")
            result["dual"][row] = int(value)
        require(len(result["dual"]) == result["dual_support"], "dual support changed")
        require((status == "MEMBER") == (not result["dual"]), "bad modular status")
        return result

    def close(self):
        if self.process.poll() is None:
            try:
                self.input.write("QUIT\n")
                self.input.flush()
                self.process.wait(timeout=5)
            except (BrokenPipeError, subprocess.TimeoutExpired):
                self.process.terminate()
                try: self.process.wait(timeout=5)
                except subprocess.TimeoutExpired: self.process.kill()
        self.guard_stop.set()
        self.guard_thread.join(timeout=3)


def initialize(provider, target, selected, started):
    output_cache = {}
    rows = set(target)
    for position, column in enumerate(selected, 1):
        entries = provider.invariant_entries(column)
        require(entries, "selected invariant column is zero")
        output_cache[column] = entries
        rows.update(entries)
        if position % 512 == 0:
            print("PREP", position, "/", len(selected), "rows", len(rows), flush=True)
            check_cap(started, f"initial_prep_{position}")
    return tuple(sorted(rows, key=lambda row: (len(row), row))), output_cache


def write_checkpoint(selected, column_sequence, ledger, modular, status, started,
                     rows, retained_rank=None):
    payload = {
        "format": "n8-chart1-boundary-d12-incremental-checkpoint-v1",
        "status": status,
        "next_round": len(ledger),
        "selected_columns": [column_record(column) for column in sorted(selected)],
        "column_insertion_sequence": [column_record(column)
                                      for column in column_sequence],
        "selected_column_orbits": len(selected),
        "row_coordinates": len(rows),
        "retained_rank_mod_prime": retained_rank,
        "ledger": ledger,
        "last_modular_dual": [] if modular is None else [
            [row.hex(), value] for row, value in sorted(modular["dual"].items())
        ],
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "peak_rss_bytes_nonlogical": peak_rss_bytes(),
    }
    logical = {key: value for key, value in payload.items()
               if not key.endswith("_nonlogical")}
    payload["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    atomic_json(CHECKPOINT, payload)


def crt_pair(left, right, p, q):
    return (left + p * (((right - left) * pow(p, -1, q)) % q)) % (p * q)


def rebuild_modular(prime, rows, target, column_sequence, output_cache,
                    started, stderr_handle):
    remaining = max(1, int(WALL_CAP_SECONDS - (time.monotonic() - started)))
    engine = IncrementalEngine(prime, rows, target, stderr_handle, remaining)
    addition = engine.add(column_sequence, output_cache)
    answer = engine.solve()
    require(answer["rank"] == addition["rank"], "rebuilt rank mismatch")
    engine.close()
    return answer


def exact_nonmember_lift(provider, rows, target, actual_target,
                         column_sequence, output_cache, first, started, stderr_handle):
    second = rebuild_modular(
        SECOND_PRIME, rows, target, column_sequence, output_cache, started,
        stderr_handle
    )
    if second["status"] != "NONMEMBER":
        return None, "second prime reports member"
    if set(first["dual"]) != set(second["dual"]):
        return None, "two-prime dual supports differ"
    from sympy import ZZ
    from sympy.polys.modulargcd import _integer_rational_reconstruction
    modulus = PRIME * SECOND_PRIME
    exact = {}
    for row in first["dual"]:
        residue = crt_pair(first["dual"][row], second["dual"][row],
                           PRIME, SECOND_PRIME)
        value = _integer_rational_reconstruction(residue, modulus, ZZ)
        if value is None:
            return None, "two-prime rational reconstruction failed"
        exact[row] = QQ(int(value.p), int(value.q))
    pairing = sum(QQ(coefficient) * exact.get(row, 0)
                  for row, coefficient in target.items())
    if not pairing:
        return None, "reconstructed exact dual lost target pairing"
    candidates = provider.incident_columns(exact)
    for column in candidates:
        entries = output_cache.setdefault(column, provider.invariant_entries(column))
        value = sum(QQ(coefficient) * exact.get(row, 0)
                    for row, coefficient in entries.items())
        if value:
            return None, "reconstructed dual misses an invariant incident column"
        check_cap(started, "exact_invariant_separator_guard")
    expanded = 0
    for column in candidates:
        for actual in provider.column_orbit(column):
            value = QQ(0)
            for term, coefficient in provider.generator(actual[0]).items():
                row = bytes(sorted(actual[1] + term))
                representative = provider.canonical_row(row)
                value += exact.get(representative, 0) * coefficient / len(
                    provider.row_orbit(representative)
                )
            if value:
                return None, "exact lifted separator misses a literal expanded column"
            expanded += 1
        check_cap(started, "exact_expanded_separator_guard")
    actual_pairing = sum(
        QQ(coefficient) * exact.get(provider.canonical_row(row), 0)
        / len(provider.row_orbit(provider.canonical_row(row)))
        for row, coefficient in actual_target.items()
    )
    require(actual_pairing == pairing, "expanded target pairing changed")
    return {
        "support": len(exact),
        "target_pairing": [pairing.numerator, pairing.denominator],
        "incident_invariant_column_orbits": len(candidates),
        "expanded_actual_incident_columns": expanded,
        "rows": [[row.hex(), value.numerator, value.denominator]
                 for row, value in sorted(exact.items())],
    }, None


def exact_member_replay(provider, rows, target, actual_target, column_sequence, started):
    ordered_columns = tuple(column_sequence)
    rank, remainder, solution, _dual, _pairing = SOURCE.solve_span(
        provider, set(rows), ordered_columns, target
    )
    check_cap(started, "exact_member_solve")
    if remainder:
        return None, f"modular member did not lift: exact rank {rank}"
    image = Counter()
    expanded_columns = 0
    for position, coefficient in solution.items():
        for code, multiplier in provider.column_orbit(ordered_columns[position]):
            expanded_columns += 1
            for term, value in provider.generator(code).items():
                row = bytes(sorted(multiplier + term))
                image[row] += coefficient * value
                if not image[row]: del image[row]
        check_cap(started, "exact_member_expanded_replay")
    expected = {row: QQ(value) for row, value in actual_target.items() if value}
    require(dict(image) == expected, "exact member failed literal expanded replay")
    return {
        "rank": rank,
        "nonzero_selected_column_orbits": len(solution),
        "expanded_actual_columns": expanded_columns,
        "expanded_rows": len(image),
        "solution": [[ordered_columns[position][0],
                      ordered_columns[position][1].hex(),
                      value.numerator, value.denominator]
                     for position, value in sorted(solution.items())],
    }, None


def run(resume_incremental=False):
    started = time.monotonic()
    require(BINARY.exists(), "build rust-d12-incremental first")
    frozen_resume = json.loads(RESUME.read_text())
    require(frozen_resume["format"] == "n8-chart1-boundary-d12-cegar-resume-v1"
            and frozen_resume["selected_column_orbits"] == 2613,
            "frozen 2,613-column resume changed")
    provider = SOURCE.Provider()
    actual_target, target = provider.full_target(started)
    if resume_incremental and CHECKPOINT.exists():
        checkpoint = json.loads(CHECKPOINT.read_text())
        require(checkpoint["format"] == "n8-chart1-boundary-d12-incremental-checkpoint-v1",
                "incremental checkpoint format changed")
        selected = {parse_column(record) for record in checkpoint["selected_columns"]}
        column_sequence = [parse_column(record) for record in
                           checkpoint.get("column_insertion_sequence",
                                          checkpoint["selected_columns"])]
        ledger = list(checkpoint["ledger"])
    else:
        selected = {parse_column(record) for record in frozen_resume["selected_columns"]}
        column_sequence = sorted(selected)
        ledger = list(frozen_resume["accepted_ledger"])
    require(len(selected) == len(column_sequence)
            and set(column_sequence) == selected and len(selected) >= 2613,
            "resume column sequence changed")
    rows, output_cache = initialize(provider, target, column_sequence, started)
    engine = None
    terminal = None
    stop = None
    modular = None
    with STDERR.open("a", encoding="utf-8") as stderr_handle:
        try:
            remaining = max(1, int(WALL_CAP_SECONDS - (time.monotonic() - started)))
            engine = IncrementalEngine(PRIME, rows, target, stderr_handle, remaining)
            addition = engine.add(column_sequence, output_cache)
            if not resume_incremental:
                require(addition["rank"] == 2613
                        and addition["zero_columns"] == 0,
                        f"frozen resume basis changed: {addition}")
            elif checkpoint.get("retained_rank_mod_prime") is not None:
                require(addition["rank"] == checkpoint["retained_rank_mod_prime"],
                        f"incremental resume rank changed: {addition}")
            print("RESUME_READY rows/cols/rank", len(rows), len(selected),
                  addition["rank"], "elapsed", round(time.monotonic()-started, 3), flush=True)
            write_checkpoint(selected, column_sequence, ledger, None,
                             "RESUME_REBUILT", started, engine.rows,
                             addition["rank"])
            while len(ledger) < MAX_ROUNDS:
                check_cap(started, f"round_{len(ledger)}_start", engine)
                modular = engine.solve()
                if modular["status"] == "MEMBER":
                    engine.close(); engine = None
                    replay, error = exact_member_replay(
                        provider, rows, target, actual_target, column_sequence, started
                    )
                    terminal = ({"status": "EXACT_D12_MEMBER", "replay": replay}
                                if replay is not None else
                                {"status": "MODULAR_MEMBER_EXACT_REPLAY_UNRESOLVED",
                                 "reason": error})
                    break
                candidates = provider.incident_columns(modular["dual"])
                violating = {}
                for position, column in enumerate(sorted(candidates), 1):
                    entries = output_cache.setdefault(column, provider.invariant_entries(column))
                    value = sum(coefficient * modular["dual"].get(row, 0)
                                for row, coefficient in entries.items()) % PRIME
                    if value and column not in selected:
                        violating[column] = value
                    if position % 512 == 0:
                        print("SCAN", position, "/", len(candidates), flush=True)
                        check_cap(started, f"round_{len(ledger)}_scan_{position}", engine)
                record = {
                    "round": len(ledger), "rows": len(engine.rows),
                    "columns": len(selected), "rank": modular["rank"],
                    "target_remainder_support": modular["remainder_support"],
                    "dual_support": modular["dual_support"],
                    "target_pairing_mod_prime": modular["target_pairing"],
                    "incident_column_orbits": len(candidates),
                    "new_violating_column_orbits": len(violating),
                    "violation_pairing_histogram_mod_prime": sorted(
                        Counter(violating.values()).items()
                    ),
                }
                print("ROUND", record["round"], "rows/cols/rank/dual/inc/new",
                      record["rows"], record["columns"], record["rank"],
                      record["dual_support"], record["incident_column_orbits"],
                      record["new_violating_column_orbits"], "elapsed",
                      round(time.monotonic()-started, 3), flush=True)
                if not violating:
                    engine.close(); engine = None
                    exact, error = exact_nonmember_lift(
                        provider, rows, target, actual_target, column_sequence,
                        output_cache, modular, started, stderr_handle,
                    )
                    terminal = ({"status": "EXACT_D12_NONMEMBER", "dual": exact}
                                if exact is not None else
                                {"status": "MODULAR_STALL_EXACT_LIFT_UNRESOLVED",
                                 "reason": error})
                    ledger.append(record)
                    break
                additions = tuple(sorted(violating))
                new_rows = set()
                for column in additions:
                    new_rows.update(output_cache[column])
                genuinely_new = new_rows.difference(engine.row_index)
                if genuinely_new:
                    engine.extend(genuinely_new)
                addition = engine.add(additions, output_cache)
                record["accepted_rank_increment"] = addition["rank_increment"]
                record["accepted_zero_columns"] = addition["zero_columns"]
                record["post_accept_rank"] = addition["rank"]
                selected.update(additions)
                column_sequence.extend(additions)
                rows = tuple(engine.rows)
                ledger.append(record)
                write_checkpoint(
                    selected, column_sequence, ledger, modular,
                    "RESUMABLE_AFTER_ACCEPTED_ROUND", started, engine.rows,
                    addition["rank"],
                )
        except BoundedStop as error:
            stop = error.args[0]
            if engine is not None:
                rows = tuple(engine.rows)
            write_checkpoint(
                selected, column_sequence, ledger, modular,
                "BOUNDED_RESUMABLE_UNRESOLVED", started, rows,
                None if engine is None else modular["rank"] if modular else None,
            )
        finally:
            if engine is not None: engine.close()

    if terminal is None:
        terminal = {
            "status": "BOUNDED_RESUMABLE_UNRESOLVED",
            "detail": stop or {"label": "round_guard"},
        }
    payload = {
        "format": "n8-chart1-boundary-d12-incremental-cegar-v1",
        **terminal,
        "prime": PRIME,
        "second_prime_for_terminal_exact_lift": SECOND_PRIME,
        "resume_logical_sha256": frozen_resume["logical_sha256"],
        "completed_rounds": len(ledger),
        "last_completed_round": ledger[-1] if ledger else None,
        "selected_column_orbits": len(selected),
        "row_coordinates": len(rows),
        "checkpoint": CHECKPOINT.name,
        "binary_sha256": sha256(BINARY.read_bytes()).hexdigest(),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "provider_sha256": sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        "wall_cap_seconds": WALL_CAP_SECONDS,
        "rss_cap_bytes": RSS_CAP_BYTES,
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "peak_rss_bytes_nonlogical": peak_rss_bytes(),
        "scope": (
            "Full homogeneous degree12 Fh target in the chart1 all-anchor boundary "
            "A_02[0,0]=0, modulo every literal mixed-generator column orbit incident "
            "to accepted duals. Degree12 membership is not saturation/radical closure."
        ),
    }
    logical = {key: value for key, value in payload.items()
               if not key.endswith("_nonlogical")}
    payload["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    atomic_json(RESULT, payload)
    print(payload["status"], "logical", payload["logical_sha256"], flush=True)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    arguments = parser.parse_args()
    run(arguments.resume)
