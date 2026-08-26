#!/usr/bin/env python3
"""Independent literal replay of the newest D11 triangle resume checkpoint."""

from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import time


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUTPUT = HERE / "production_resume_p1073741827_triangle_endpoint_colour"
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
SEED = HERE / "sealed_resume_input/selected.tsv"
PRIME, DEGREE, T = 1_073_741_827, 11, 361
PINS = {
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "seed_selected": "1f70a3220d6091e0877fd00d86c6ff9f06f25789e03cc854556e6d7ae34fb2a7",
    "selected": "9c70caaf26b71345b03565dbdf2edba8c52f06eca4ad74d6e7b888fa8a49cca5",
    "dual": "06ded311e326a66105d69ae7be2eb56c7ba9720ab19718f7cd173c09efb2ce02",
    "watchdog": "58bbbaea7968f237ef01980992466123f67beef259641079f6ff55b115505e09",
    "run_summary": "f387f5ee2b999e1e0371a452f3103c743987b3385780caffb2e88be7860bdec7",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def signed_terms(line: str):
    line = line.rstrip("\n,")
    answer, begin, sign = [], 0, 1
    if line[0] in "+-":
        sign, begin = (-1 if line[0] == "-" else 1), 1
    for index in range(begin, len(line)):
        if line[index] in "+-":
            answer.append((sign, line[begin:index]))
            sign, begin = (-1 if line[index] == "-" else 1), index + 1
    answer.append((sign, line[begin:]))
    return answer


def load_provider():
    assert sha(PROVIDER) == PINS["provider"]
    with PROVIDER.open() as stream:
        variables = stream.readline().rstrip("\n").split(",")
        assert len(variables) == 361 and int(stream.readline()) == PRIME
        names = {name: index for index, name in enumerate(variables)}
        generators = []
        for line in stream:
            raw, maximum = [], 0
            for coefficient, token in signed_terms(line):
                ids = () if token == "1" else tuple(sorted(names[value] for value in token.split("*")))
                maximum = max(maximum, len(ids))
                raw.append((ids, coefficient))
            combined = defaultdict(int)
            for ids, coefficient in raw:
                combined[tuple(sorted(ids + (T,) * (maximum - len(ids))))] += coefficient
            generators.append((maximum, tuple((row, coefficient) for row, coefficient in sorted(combined.items()) if coefficient)))
    assert len(generators) == 6571
    return tuple(generators)


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def parse_columns(path: Path, generators, dual=None):
    lines = path.read_text().splitlines()
    assert lines and lines[0] == "KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1"
    columns = []
    failures = []
    previous = None
    for line_number, line in enumerate(lines[1:], 2):
        kind, raw_generator, raw_degree, raw_multiplier = line.split("\t")
        generator, degree = int(raw_generator), int(raw_degree)
        multiplier = tuple(map(int, raw_multiplier.split(","))) if raw_multiplier else ()
        column = (generator, multiplier)
        assert kind == "COL" and 0 <= generator < len(generators)
        assert generators[generator][0] == degree
        assert len(multiplier) + degree == DEGREE and multiplier == tuple(sorted(multiplier))
        assert all(0 <= value <= T for value in multiplier)
        assert previous is None or previous < column
        previous = column
        columns.append(column)
        if dual is not None:
            pairing = sum(coefficient * dual.get(tuple(sorted(term + multiplier)), 0)
                          for term, coefficient in generators[generator][1]) % PRIME
            if pairing:
                failures.append({"line": line_number, "generator": generator, "pairing": pairing})
                if len(failures) >= 10:
                    break
    return columns, failures


def main() -> None:
    started = time.monotonic()
    paths = {name: OUTPUT / filename for name, filename in (
        ("selected", "selected.tsv"), ("dual", "dual.tsv"),
        ("watchdog", "watchdog.json"), ("run_summary", "run_summary.json"))}
    assert sha(PROVIDER) == PINS["provider"] and sha(SEED) == PINS["seed_selected"]
    for name, path in paths.items():
        assert sha(path) == PINS[name]
    assert not (OUTPUT / "result.json").exists()

    watchdog = json.loads(paths["watchdog"].read_text())
    assert watchdog["status"] == "FAIL_CLOSED_CHECKPOINT_AVAILABLE"
    assert watchdog["breach"] == "WALL_CAP" and watchdog["returncode"] == -15
    assert watchdog["elapsed_seconds"] >= 360 and watchdog["peak_rss_kib"] == 15_308_688
    assert watchdog["peak_rss_kib"] < watchdog["rss_limit_kib"] == 16 * 1024 * 1024
    assert not watchdog["result_exists"] and watchdog["restart_pair_available"]
    assert watchdog["restart_selected_sha256"] == PINS["selected"]
    assert watchdog["restart_dual_sha256"] == PINS["dual"]
    summary = json.loads(paths["run_summary"].read_text())
    assert summary["status"] == "FAIL_CLOSED"
    assert summary["watchdog_status"] == "FAIL_CLOSED_CHECKPOINT_AVAILABLE"
    assert summary["result_sha256"] is None and summary["result_status"] is None
    assert not summary["second_prime_launched"] and not summary["degree_twelve_launched"]

    dual_lines = paths["dual"].read_text().splitlines()
    assert dual_lines[0].split("\t") == ["KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1", str(PRIME), str(len(dual_lines) - 1), "1"]
    dual = {}
    previous = None
    for line in dual_lines[1:]:
        kind, raw, raw_value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(raw_value)
        assert kind == "ROW" and len(row) == DEGREE and row == tuple(sorted(row))
        assert all(0 <= item <= T for item in row)
        assert previous is None or previous < row
        assert row not in dual and 0 < value < PRIME
        dual[row], previous = value, row
    assert len(dual) == 80_922 and dual[(T,) * DEGREE] == 1

    generators = load_provider()
    columns, failures = parse_columns(paths["selected"], generators, dual)
    assert len(columns) == 230_091 and not failures
    seed_columns, seed_failures = parse_columns(SEED, generators)
    assert len(seed_columns) == 94_526 and not seed_failures
    assert set(seed_columns).issubset(columns)

    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_RESUME16_CHECKPOINT_AUDIT_V1",
        "status": "PASS_FAIL_CLOSED_CHECKPOINT_ADVANCED",
        "resource_terminal": "WALL_CAP",
        "mathematical_verdict": None,
        "prime": PRIME,
        "degree": DEGREE,
        "seed_selected_columns": len(seed_columns),
        "selected_columns": len(columns),
        "new_selected_columns": len(columns) - len(seed_columns),
        "seed_subset_preserved": True,
        "dual_support": len(dual),
        "target_coefficient": 1,
        "selected_pairings_replayed": len(columns),
        "pairing_failures": 0,
        "global_incident_scan_performed": False,
        "selected_sha256": PINS["selected"],
        "dual_sha256": PINS["dual"],
        "provider_sha256": PINS["provider"],
        "watchdog_sha256": PINS["watchdog"],
        "run_summary_sha256": PINS["run_summary"],
        "elapsed_seconds": time.monotonic() - started,
        "second_prime_launched": False,
        "other_branch_launched": False,
        "degree_twelve_launched": False,
    }
    atomic(OUTPUT / "checkpoint_audit.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
