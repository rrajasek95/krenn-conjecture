#!/usr/bin/env python3
"""Independent literal replay of the D11 recovery restart pair."""
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
OUTPUT = HERE / "production_p1073741827_triangle_endpoint_colour"
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
PROVIDER_SHA = "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c"
PRIME, DEGREE, T = 1073741827, 11, 361

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def signed_terms(line):
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

def provider():
    assert sha(PROVIDER) == PROVIDER_SHA
    with PROVIDER.open() as stream:
        variables = stream.readline().rstrip("\n").split(",")
        assert len(variables) == 361 and int(stream.readline()) == PRIME
        names = {name: index for index, name in enumerate(variables)}
        generators = []
        for line in stream:
            raw, maximum = [], 0
            for coefficient, token in signed_terms(line):
                ids = () if token == "1" else tuple(sorted(names[x] for x in token.split("*")))
                maximum = max(maximum, len(ids))
                raw.append((ids, coefficient))
            combined = defaultdict(int)
            for ids, coefficient in raw:
                combined[tuple(sorted(ids + (T,) * (maximum - len(ids))))] += coefficient
            generators.append((maximum, tuple((row, c) for row, c in sorted(combined.items()) if c)))
    assert len(generators) == 6571
    return tuple(generators)

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    started = time.monotonic()
    watch = json.loads((OUTPUT / "watchdog.json").read_text())
    assert watch["status"] == "FAIL_CLOSED_CHECKPOINT_AVAILABLE" and watch["breach"] == "RSS_CAP"
    selected_path, dual_path = OUTPUT / "selected.tsv", OUTPUT / "dual.tsv"
    assert sha(selected_path) == watch["restart_selected_sha256"]
    assert sha(dual_path) == watch["restart_dual_sha256"]
    dual_lines = dual_path.read_text().splitlines()
    assert dual_lines[0].split("\t") == ["KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1", str(PRIME), str(len(dual_lines) - 1), "1"]
    dual = {}
    previous = None
    for line in dual_lines[1:]:
        kind, raw, value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(value)
        assert kind == "ROW" and len(row) == DEGREE and row == tuple(sorted(row))
        assert previous is None or previous < row
        assert row not in dual and 0 < value < PRIME
        dual[row], previous = value, row
    assert dual[(T,) * DEGREE] == 1
    generators = provider()
    lines = selected_path.read_text().splitlines()
    assert lines and lines[0] == "KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1"
    previous_column = None
    pairing_failures = []
    for index, line in enumerate(lines[1:]):
        kind, raw_generator, raw_degree, raw_multiplier = line.split("\t")
        generator, degree = int(raw_generator), int(raw_degree)
        multiplier = tuple(map(int, raw_multiplier.split(","))) if raw_multiplier else ()
        column = (generator, multiplier)
        assert kind == "COL" and generators[generator][0] == degree
        assert len(multiplier) + degree == DEGREE and multiplier == tuple(sorted(multiplier))
        assert previous_column is None or previous_column < column
        previous_column = column
        pairing = sum(coefficient * dual.get(tuple(sorted(term + multiplier)), 0)
                      for term, coefficient in generators[generator][1]) % PRIME
        if pairing:
            pairing_failures.append({"line": index + 2, "generator": generator, "pairing": pairing})
            if len(pairing_failures) >= 10:
                break
    assert not pairing_failures
    result = {"schema": "KRENN_X5_D11_TRIANGLE_RESTART_PAIR_AUDIT_V1", "status": "PASS_RESTART_PAIR",
              "prime": PRIME, "degree": DEGREE, "selected_columns": len(lines) - 1,
              "dual_support": len(dual), "target_coefficient": 1,
              "selected_pairings_replayed": len(lines) - 1, "pairing_failures": 0,
              "selected_sha256": sha(selected_path), "dual_sha256": sha(dual_path),
              "provider_sha256": PROVIDER_SHA, "watchdog_sha256": sha(OUTPUT / "watchdog.json"),
              "elapsed_seconds": time.monotonic() - started, "global_incident_scan_performed": False,
              "mathematical_verdict": None, "second_prime_launched": False, "degree_twelve_launched": False}
    atomic(OUTPUT / "checkpoint_audit.json", result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
