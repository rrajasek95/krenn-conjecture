#!/usr/bin/env python3
"""Source-faithful driver for the Rust normalized-Fh degree-12 CEGAR."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import subprocess
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROOT_STAR_PATH = (
    ROOT / "computations/unaudited-codex-n8-chart26-fh-root-star-2026-08-23"
    / "audit_fh_root_star.py"
)
ROOT_STAR_RESULT = ROOT_STAR_PATH.with_name("results_fh_root_star.json")
BINARY = HERE / "target/release/fh-d12-moddual"
CHECKPOINT = HERE / "checkpoint_fh_degree12_rust_cegar.json"
RESULTS = HERE / "results_fh_degree12_rust_cegar.json"
MATRIX_INPUT = HERE / "current_matrix_input.txt"
MATRIX_OUTPUT = HERE / "current_matrix_output.txt"
PRIME = 1_073_741_827
SECOND_PRIME = 1_073_741_789
WALL_CAP_SECONDS = 20 * 60
RSS_CAP_BYTES = 16 * 1024 ** 3
EXPECTED_ROOT_STAR_LOGICAL = (
    "57a5bb5aa092a6edb79644be16f8b07908f8533b6c59e33e1ef4727771b6aad1"
)
PYTHON_R22_LEDGER = [
    (56, 1, 1, 2, 17, 15),
    (1438, 16, 16, 2, 37, 35),
    (4663, 51, 51, 2, 102, 93),
    (12410, 144, 144, 3, 129, 116),
    (21877, 260, 260, 2, 33, 31),
    (24501, 291, 291, 2, 20, 18),
    (26194, 309, 309, 2, 20, 17),
    (27771, 326, 326, 11, 103, 76),
    (34477, 402, 402, 5, 42, 32),
    (37304, 434, 434, 4, 24, 20),
    (39002, 454, 454, 14, 99, 78),
    (45934, 532, 532, 8, 56, 43),
    (49728, 575, 575, 26, 197, 139),
    (62095, 714, 714, 11, 64, 50),
    (66554, 764, 764, 33, 252, 183),
    (82434, 947, 947, 90, 793, 508),
    (125423, 1455, 1455, 177, 1587, 981),
    (208112, 2436, 2436, 4, 24, 18),
    (209578, 2454, 2454, 32, 282, 198),
    (226335, 2652, 2652, 10, 62, 48),
    (230423, 2700, 2700, 75, 596, 349),
    (260166, 3049, 3049, 279, 2134, 1151),
    (355170, 4200, 4200, 625, 4112, 2048),
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


ROOT_STAR = load(ROOT_STAR_PATH, "n8_fh_d12_rust_cegar_root")


def peak_rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if value > 10_000_000 else value * 1024)


def check_cap(started, label):
    elapsed = time.monotonic() - started
    rss = peak_rss_bytes()
    if elapsed >= WALL_CAP_SECONDS or rss >= RSS_CAP_BYTES:
        raise BoundedStop({
            "label": label,
            "elapsed_seconds": elapsed,
            "peak_rss_bytes": rss,
        })


def column_record(column):
    return [column[0], column[1].hex()]


def parse_column(record):
    return int(record[0]), bytes.fromhex(record[1])


def write_checkpoint(columns, ledger, last_dual, status, started):
    payload = {
        "format": "n8-fh-degree12-rust-cegar-checkpoint-v1",
        "status": status,
        "next_round": len(ledger),
        "columns": [column_record(column) for column in sorted(columns)],
        "ledger": ledger,
        "last_dual": last_dual,
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "peak_rss_bytes_nonlogical": peak_rss_bytes(),
    }
    CHECKPOINT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def parse_moddual(path, ordered_rows, prime):
    lines = path.read_text().splitlines()
    require(lines, "Rust modular solver emitted no output")
    fields = lines[0].split()
    require(len(fields) == 6
            and fields[0] == "KRENN_FH_D12_MODDUAL_RESULT_V1"
            and int(fields[1]) == prime,
            "bad Rust modular result header")
    rank, remainder, support, target_pairing = map(int, fields[2:])
    dual = {}
    for line in lines[1:]:
        label, index, coefficient = line.split()
        require(label == "DUAL", "bad Rust dual record")
        row = ordered_rows[int(index)]
        value = int(coefficient)
        require(value and value < prime and row not in dual,
                "invalid Rust dual coefficient")
        dual[row] = value
    require(len(dual) == support, "Rust dual support census changed")
    return {
        "rank": rank,
        "remainder_support": remainder,
        "target_pairing": target_pairing,
        "dual": dual,
    }


def write_matrix(source_api, source, columns, rows, coefficient_fh, prime,
                 remaining_seconds, output_cache, started):
    ordered_rows = tuple(sorted(rows, key=lambda row: (-len(row), row)))
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    target = []
    for index, row in enumerate(ordered_rows):
        value = coefficient_fh(row) % prime
        if value:
            target.append((index, value))
    vectors = []
    for processed, column in enumerate(sorted(columns), 1):
        entries = output_cache.setdefault(
            column, source_api.invariant_entries(source, column)
        )
        vector = {
            row_index[row]: coefficient % prime
            for row, coefficient in entries.items() if coefficient % prime
        }
        require(vector, "a source column vanished in the invariant block")
        vectors.append((min(vector), len(vector), column, vector))
        if processed % 1024 == 0:
            print("PREP columns", processed, "/", len(columns),
                  "elapsed", round(time.monotonic() - started, 3), flush=True)
            check_cap(started, f"matrix_prep_{processed}")
    vectors.sort(key=lambda item: (item[0], item[1], item[2]))
    with MATRIX_INPUT.open("w", encoding="ascii") as output:
        output.write(
            f"KRENN_FH_D12_MODDUAL_V1 {prime} {len(rows)} "
            f"{len(vectors)} {max(1, remaining_seconds)}\n"
        )
        output.write("TARGET " + str(len(target)))
        for index, value in target:
            output.write(f" {index} {value}")
        output.write("\n")
        for _minimum, _support, _column, vector in vectors:
            output.write("VECTOR " + str(len(vector)))
            for index, value in sorted(vector.items()):
                output.write(f" {index} {value}")
            output.write("\n")
    return ordered_rows


def run_moddual(source_api, source, columns, rows, coefficient_fh, prime,
                output_cache, started):
    check_cap(started, "before_modular_solve")
    ordered_rows = write_matrix(
        source_api, source, columns, rows, coefficient_fh, prime,
        WALL_CAP_SECONDS, output_cache, started,
    )
    remaining = WALL_CAP_SECONDS - (time.monotonic() - started)
    if remaining <= 0:
        raise BoundedStop({
            "label": "after_matrix_prep",
            "elapsed_seconds": time.monotonic() - started,
            "peak_rss_bytes": peak_rss_bytes(),
        })
    with MATRIX_INPUT.open("rb") as input_file, MATRIX_OUTPUT.open("wb") as output_file:
        try:
            completed = subprocess.run(
                [str(BINARY)], stdin=input_file, stdout=output_file,
                check=False, timeout=remaining,
            )
        except subprocess.TimeoutExpired as error:
            raise BoundedStop({
                "label": "rust_modular_solve_hard_wall",
                "elapsed_seconds": time.monotonic() - started,
                "peak_rss_bytes": peak_rss_bytes(),
            }) from error
    require(completed.returncode == 0,
            f"Rust modular solver failed with {completed.returncode}")
    check_cap(started, "after_modular_solve")
    return parse_moddual(MATRIX_OUTPUT, ordered_rows, prime), ordered_rows


def crt_pair(left, right, p, q):
    return (left + p * (((right - left) * pow(p, -1, q)) % q)) % (p * q)


def exact_terminal_lift(source_api, source, columns, rows, coefficient_fh,
                        first, first_rows, output_cache, started):
    second, second_rows = run_moddual(
        source_api, source, columns, rows, coefficient_fh, SECOND_PRIME,
        output_cache, started,
    )
    if first_rows != second_rows or set(first["dual"]) != set(second["dual"]):
        return None, "two-prime dual supports differ"
    from sympy import ZZ
    from sympy.polys.modulargcd import _integer_rational_reconstruction
    modulus = PRIME * SECOND_PRIME
    exact = {}
    for row in first["dual"]:
        residue = crt_pair(
            first["dual"][row], second["dual"][row], PRIME, SECOND_PRIME
        )
        value = _integer_rational_reconstruction(residue, modulus, ZZ)
        if value is None:
            return None, "rational reconstruction failed"
        exact[row] = Fraction(int(value.p), int(value.q))
    target_pairing = sum(
        value * coefficient_fh(row) for row, value in exact.items()
    )
    if not target_pairing:
        return None, "reconstructed exact dual lost target pairing"
    candidates = source.bounded_incident_columns(
        exact, maximum_output_degree=12
    )
    for column in candidates:
        entries = output_cache.setdefault(
            column, source_api.invariant_entries(source, column)
        )
        if source_api.pairing(entries, exact):
            return None, "reconstructed exact dual misses an incident column"
    actual_columns = source.audit_expanded_dual(exact, candidates)
    return {
        "support": len(exact),
        "target_pairing": [target_pairing.numerator, target_pairing.denominator],
        "incident_invariant_column_orbits": len(candidates),
        "expanded_actual_incident_columns": actual_columns,
        "rows": [
            [row.hex(), value.numerator, value.denominator]
            for row, value in sorted(exact.items())
        ],
    }, None


def audit(resume=False):
    started = time.monotonic()
    root_result = json.loads(ROOT_STAR_RESULT.read_text())
    require(root_result["logical_sha256"] == EXPECTED_ROOT_STAR_LOGICAL,
            "root-star authority changed")
    require(BINARY.exists(), "build the Rust modular solver first")
    source_api, source = ROOT_STAR.load_source()
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
                total += coefficient * coefficient_fh(
                    quotient, colours[1:]
                )
        return total

    if resume and CHECKPOINT.exists():
        checkpoint = json.loads(CHECKPOINT.read_text())
        columns = {parse_column(record) for record in checkpoint["columns"]}
        ledger = list(checkpoint["ledger"])
    else:
        columns = set(source.bounded_incident_columns(
            {b"": Fraction(1)}, maximum_output_degree=12
        ))
        ledger = []
    rows = {b""}
    output_cache = {}
    for processed, column in enumerate(sorted(columns), 1):
        rows.update(output_cache.setdefault(
            column, source_api.invariant_entries(source, column)
        ))
        if processed % 1024 == 0:
            print("RESUME rows from columns", processed, "/", len(columns),
                  flush=True)
    last_dual_record = []
    terminal = None
    try:
        while True:
            round_index = len(ledger)
            modular, ordered_rows = run_moddual(
                source_api, source, columns, rows, coefficient_fh, PRIME,
                output_cache, started,
            )
            if not modular["dual"]:
                terminal = {
                    "status": "MODULAR_TARGET_PROJECTION_MEMBER_UNRESOLVED_EXACT",
                    "rank_mod_prime": modular["rank"],
                    "reason": "no exact source combination was reconstructed",
                }
                break
            candidates = source.bounded_incident_columns(
                modular["dual"], maximum_output_degree=12
            )
            violating = {}
            for processed, column in enumerate(sorted(candidates), 1):
                entries = output_cache.setdefault(
                    column, source_api.invariant_entries(source, column)
                )
                value = sum(
                    coefficient * modular["dual"].get(row, 0)
                    for row, coefficient in entries.items()
                ) % PRIME
                if value and column not in columns:
                    violating[column] = value
                if processed % 2048 == 0:
                    print("SCAN candidates", processed, "/", len(candidates),
                          "elapsed", round(time.monotonic() - started, 3),
                          flush=True)
                    check_cap(started, f"scan_{round_index}_{processed}")
            record = {
                "round": round_index,
                "rows": len(rows),
                "columns": len(columns),
                "rank": modular["rank"],
                "dual_support": len(modular["dual"]),
                "incident_column_orbits": len(candidates),
                "new_violating_column_orbits": len(violating),
                "target_pairing_mod_prime": modular["target_pairing"],
            }
            if round_index < len(PYTHON_R22_LEDGER):
                observed = tuple(record[key] for key in (
                    "rows", "columns", "rank", "dual_support",
                    "incident_column_orbits", "new_violating_column_orbits",
                ))
                require(observed == PYTHON_R22_LEDGER[round_index],
                        f"Rust/Python divergence at round {round_index}: {observed}")
                record["python_exact_q_shape_match"] = True
            ledger.append(record)
            last_dual_record = [
                [row.hex(), value] for row, value in sorted(modular["dual"].items())
            ]
            print("ROUND", round_index, "rows/cols/rank/dual/incident/new",
                  record["rows"], record["columns"], record["rank"],
                  record["dual_support"], record["incident_column_orbits"],
                  record["new_violating_column_orbits"], "elapsed",
                  round(time.monotonic() - started, 3), flush=True)
            if not violating:
                exact, error = exact_terminal_lift(
                    source_api, source, columns, rows, coefficient_fh,
                    modular, ordered_rows, output_cache, started,
                )
                terminal = ({
                    "status": "EXACT_FULL_FH_DEGREE12_NONMEMBERSHIP",
                    "exact_dual": exact,
                } if exact is not None else {
                    "status": "MODULAR_STALL_EXACT_LIFT_UNRESOLVED",
                    "reason": error,
                })
                break
            columns.update(violating)
            for column in violating:
                rows.update(output_cache[column])
            write_checkpoint(
                columns, ledger, last_dual_record,
                "RESUMABLE_AFTER_COMPLETED_ROUND", started,
            )
            check_cap(started, f"round_{round_index}_checkpoint")
    except BoundedStop as stopped:
        write_checkpoint(
            columns, ledger, last_dual_record,
            "BOUNDED_RESUMABLE_UNRESOLVED", started,
        )
        terminal = {
            "status": "BOUNDED_RESUMABLE_UNRESOLVED",
            "detail": stopped.args[0],
        }

    payload = {
        "format": "n8-fh-degree12-rust-cegar-v1",
        **terminal,
        "prime": PRIME,
        "second_prime_for_terminal_exact_lift": SECOND_PRIME,
        "completed_rounds": len(ledger),
        "last_completed_round": ledger[-1] if ledger else None,
        "checkpoint": CHECKPOINT.name,
        "ledger": ledger,
        "root_star_logical_sha256": root_result["logical_sha256"],
        "binary_sha256": sha256(BINARY.read_bytes()).hexdigest(),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "wall_cap_seconds": WALL_CAP_SECONDS,
        "rss_cap_bytes": RSS_CAP_BYTES,
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "peak_rss_bytes_nonlogical": peak_rss_bytes(),
        "scope": (
            "full normalized F^h and homogeneous degree12 mixed ideal only; "
            "no truncated C10, degree13, saturation, or global inference"
        ),
    }
    logical = {
        key: value for key, value in payload.items()
        if not key.endswith("_nonlogical")
    }
    payload["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    result = audit(args.resume)
    print(result["status"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
