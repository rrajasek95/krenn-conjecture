#!/usr/bin/env python3
"""Complete original-generator incidence at homogeneous degree nine."""

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRST_PATH = ROOT / "computations/verify_n8_chart26_first_homogeneous_spair.py"
RESULTS = HERE / "results_y10_dead_row_original_d9.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("y10_original_d9", FIRST_PATH)
FIRST = importlib.util.module_from_spec(spec)
require(spec.loader is not None, "cannot load original source checker")
spec.loader.exec_module(FIRST)


def quotient(dividend, divisor):
    answer = list(dividend)
    for value in divisor:
        require(value in answer, "requested non-divisor quotient")
        answer.remove(value)
    return bytes(answer)


def target_divisors(target, total_degree, target_t_exponent):
    by_t = {}
    all_rows = []
    for t_exponent in range(target_t_exponent + 1):
        y_degree = total_degree - t_exponent
        rows = sorted({
            bytes(target[index] for index in positions)
            for positions in combinations(range(len(target)), y_degree)
        })
        by_t[t_exponent] = rows
        all_rows.extend(rows)
    require(len(all_rows) == len(set(all_rows)),
            "divisors of different y degree collided")
    return sorted(all_rows, key=lambda row: (len(row), row)), by_t


def build_subterm_index(divisors, source_degree, multiplier_degree):
    index = defaultdict(set)
    for divisor in divisors:
        minimum = max(0, len(divisor) - multiplier_degree)
        maximum = min(source_degree, len(divisor))
        for degree in range(minimum, maximum + 1):
            for positions in combinations(range(len(divisor)), degree):
                row = bytes(divisor[index] for index in positions)
                index[row].add(divisor)
    return index


def main():
    target = bytes.fromhex("0111202020494f4f50f8")
    target_total_degree = 12
    target_t_exponent = 2
    divisors, by_t = target_divisors(target, 9, target_t_exponent)
    census = {key: len(value) for key, value in by_t.items()}
    subterm_index = build_subterm_index(divisors, 4, 5)
    originals, _lead_to_code = FIRST.original_basis()

    columns = defaultdict(Counter)
    source_terms_scanned = 0
    for code, polynomial in originals.items():
        for row, coefficient in polynomial.items():
            source_terms_scanned += 1
            for divisor in sorted(subterm_index.get(row, ())):
                multiplier = quotient(divisor, row)
                require(len(multiplier) <= 5, "multiplier exceeds total degree five")
                columns[(code, multiplier)][divisor] += coefficient
    cleaned = {}
    for key, values in columns.items():
        values = Counter({row: value for row, value in values.items() if value})
        if values:
            cleaned[key] = values
    columns = cleaned

    records = []
    row_incidence = Counter()
    seed_slices = Counter()
    for (code, multiplier), values in sorted(columns.items()):
        row_incidence.update(values.keys())
        record = {
            "source_code": code,
            "multiplier_y": multiplier.hex(),
            "multiplier_t_exponent": 5 - len(multiplier),
            "target_rows": [
                [row.hex(), value.numerator, value.denominator]
                for row, value in sorted(values.items())
            ],
        }
        records.append(record)
        if len(multiplier) == 5:
            lengths = {len(row) for row in values}
            require(len(lengths) == 1, "d9 seed crossed target t slices")
            seed_slices[9 - next(iter(lengths))] += 1
    new_seeds = [record for record in records
                 if record["multiplier_t_exponent"] == 0]
    require(not any(len(bytes.fromhex(row[0])) == 9
                    for record in new_seeds for row in record["target_rows"]),
            "a t-free y9 target divisor gained direct incidence")

    result = {
        "format": "n8-orbit26-y10-dead-row-original-d9-v1",
        "status": "D9_NEW_HEAD_REQUIRES_COLLISION_CLOSURE",
        "target_y10_row": target.hex(),
        "target_total_degree": target_total_degree,
        "target_t_exponent": target_t_exponent,
        "divisor_total_degree": 9,
        "divisor_census_by_t_exponent": {
            str(key): value for key, value in sorted(census.items())
        },
        "distinct_homogeneous_divisors": len(divisors),
        "original_generators": len(originals),
        "source_terms_scanned": source_terms_scanned,
        "incident_columns": len(records),
        "incident_target_rows": len(row_incidence),
        "incident_row_t_histogram": dict(sorted(Counter(
            9 - len(row) for row in row_incidence).items())),
        "new_t_free_y5_seed_columns": len(new_seeds),
        "new_seed_target_t_exponent_histogram": dict(sorted(seed_slices.items())),
        "direct_y9_target_incidences": 0,
        "incident_records": records,
        "scope": (
            "complete literal original-generator incidence at total degree nine; "
            "a shorter target pivot requires a kernel in the new t-free y5 head, "
            "while positive-t multiplier slices lie in t*M8"
        ),
        "source_sha256": sha256(FIRST_PATH.read_bytes()).hexdigest(),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("y10 homogeneous d9 original incidence: PASS")
    print("divisor census:", census)
    print("columns/rows/new-seeds/slices:", len(records), len(row_incidence),
          len(new_seeds), dict(sorted(seed_slices.items())))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
