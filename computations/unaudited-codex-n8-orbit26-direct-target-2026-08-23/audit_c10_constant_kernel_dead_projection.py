#!/usr/bin/env python3
"""Exact dead-coordinate image of the 3780/5108 lower-kernel family."""

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRST_PATH = ROOT / "computations/verify_n8_chart26_first_homogeneous_spair.py"
PROVIDER = HERE / "direct_fh_unique_min_provider.txt"
DEAD = HERE / "c10_dead_projection.txt"
RESULT = HERE / "results_c10_constant_kernel_dead_projection.json"

spec = importlib.util.spec_from_file_location("c10_dead", FIRST_PATH)
FIRST = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(FIRST)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def subtract(big, small):
    rest = list(big)
    for value in small:
        try:
            rest.remove(value)
        except ValueError:
            return None
    return bytes(rest)


def divisors(row, degree):
    return sorted({bytes(row[i] for i in positions)
                   for positions in combinations(range(len(row)), degree)})


def providers():
    quadratic = defaultdict(Counter)
    for line in PROVIDER.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields and fields[0] == "L2":
            quadratic[int(fields[1])][bytes.fromhex(fields[2])] += int(fields[3])
    require(len(quadratic) == 240 and all(len(x) == 6 for x in quadratic.values()),
            "linear provider packet changed")
    return quadratic


def transfer_coefficient(row, multiplier, d2, d3, d4, h2, quadratic):
    complement = subtract(row, multiplier)
    require(complement is not None and len(complement) == 4, "bad multiplier")
    coefficient = d4.get(complement, 0)
    for term, value in d2.items():
        tail = subtract(complement, term)
        if tail is not None:
            coefficient -= value * h2.get(tail, 0)
    for term, value in d3.items():
        degree9 = bytes(sorted(multiplier + term))
        cell, remainder = degree9[0], degree9[1:]
        tail = subtract(row, remainder)
        if tail is not None and len(tail) == 2:
            coefficient -= value * quadratic[cell].get(tail, 0)
    return coefficient


def main():
    originals, _ = FIRST.original_basis()
    delta = Counter(originals[5108]); delta.subtract(originals[3780])
    delta = Counter({row: value for row, value in delta.items() if value})
    d2 = Counter({row: value for row, value in delta.items() if len(row) == 2})
    d3 = Counter({row: value for row, value in delta.items() if len(row) == 3})
    d4 = Counter({row: value for row, value in delta.items() if len(row) == 4})
    h2 = Counter({row: value for row, value in originals[3780].items() if len(row) == 2})
    quadratic = providers()

    dead = []
    lines = DEAD.read_text(encoding="ascii").splitlines()
    require(lines[0] == "KRENN_C10_DEAD_PROJECTION_V1 COUNT 12195", "dead header changed")
    for line in lines[1:]:
        tag, row, coefficient = line.split()
        require(tag == "ROW", "bad dead row")
        dead.append((bytes.fromhex(row), int(coefficient)))
    require(len(dead) == 12195, "dead census changed")

    touched_rows = 0
    nonzero_entries = 0
    multipliers = set()
    invariant = None
    first_touched = None
    for row, residual_coefficient in dead:
        hits = []
        for multiplier in divisors(row, 6):
            value = transfer_coefficient(row, multiplier, d2, d3, d4, h2, quadratic)
            if value:
                hits.append((multiplier, value))
                multipliers.add(multiplier)
        if hits:
            touched_rows += 1
            nonzero_entries += len(hits)
            if first_touched is None:
                first_touched = (row, residual_coefficient, hits)
        elif invariant is None:
            invariant = (row, residual_coefficient)

    require(invariant is not None, "constant-provider component touches every dead coordinate")
    result = {
        "format": "n8-orbit26-c10-constant-kernel-dead-projection-v1",
        "status": "EXACT_NONMEMBER_IN_3780_5108_CONSTANT_PROVIDER_COMPONENT",
        "degree12_quotient": "y10*t2 modulo all 2206 PM4/N4 quadratic leading columns",
        "deterministic_dead_projection_rows": len(dead),
        "constant_kernel_touched_dead_rows": touched_rows,
        "constant_kernel_untouched_dead_rows": len(dead) - touched_rows,
        "nonzero_dead_incidence_entries": nonzero_entries,
        "distinct_incident_y6_multipliers": len(multipliers),
        "one_coordinate_dual": {
            "row_y10": invariant[0].hex(),
            "deterministic_c10_pairing": invariant[1],
            "pm4_column_pairing": 0,
            "all_3780_5108_transferred_y6_kernel_pairing": 0,
            "tested_distinct_degree6_divisors": len(divisors(invariant[0], 6)),
        },
        "first_touched_control": None if first_touched is None else {
            "row_y10": first_touched[0].hex(),
            "deterministic_c10_coefficient": first_touched[1],
            "hits": [{"multiplier_y6": m.hex(), "coefficient": c}
                     for m, c in first_touched[2]],
        },
        "theorem": (
            "The displayed coordinate is absent from every literal PM4/N4 degree-ten "
            "leading column and from the transferred degree-ten tail of m*(G5108-G3780) "
            "for every y-degree-six multiplier m. Its nonzero deterministic C10 "
            "coefficient is therefore an exact dual obstruction to killing C10 using "
            "this complete constant-provider lower-kernel component."
        ),
        "scope": (
            "This is exact only for the lower-kernel component generated by normalized "
            "constant providers 3780/5108 plus the PM4/N4 degree-ten image. It does not "
            "annihilate unenumerated lower-kernel components and is not full ideal "
            "nonmembership."
        ),
        "source_sha256": {
            DEAD.name: sha256(DEAD.read_bytes()).hexdigest(),
            PROVIDER.name: sha256(PROVIDER.read_bytes()).hexdigest(),
            str(FIRST_PATH.relative_to(ROOT)): sha256(FIRST_PATH.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
