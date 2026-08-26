#!/usr/bin/env python3
"""Pair the base+raw10 degree-9 dual with the three remaining rows."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_d9_dual_against_omitted_rows.py"
FULL = HERE / "face03113_full16_d9.jsonl"
CORE = HERE / "face03113_plus10_d9_core.jsonl"
SOLVE = HERE / "results_face03113_plus10_d9_p1009.json"
OUTPUT = HERE / "results_plus10_d9_dual_remaining_rows.json"
REMAINING = (6, 9, 11)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = load("face03113_d9_base", BASE_PATH)


def main():
    payload = json.loads(BASE.SOURCE.read_text())
    record = next(row for row in payload["states"] if row["key"] == BASE.KEY)
    rows = {row["raw_index"]: row for row in record["rows"]}
    full_header = json.loads(FULL.open().readline())
    core_header = json.loads(CORE.open().readline())
    solve = json.loads(SOLVE.read_text())
    names = full_header["variables"]
    symbols = sp.symbols(" ".join(names))
    locals_map = dict(zip(names, symbols, strict=True))

    selected = BASE.localizer_factor(record, "selected_base_terms")
    c_factor = BASE.localizer_factor(record, "both_live_c_numerators")
    sat = "s*(" + selected + ")*(" + c_factor + ")-1"
    labelled = [(f"raw_{index}_{rows[index]['label']}",
                 rows[index]["polynomial"]) for index in range(6, 22)]
    labelled.append(("SAT_selected_base_times_C", sat))
    generators = []
    for label, expression in labelled:
        degree, terms = BASE.homogenize(expression, symbols, locals_map)
        generators.append({"label": label, "degree": degree, "terms": terms})
    target_key = tuple([0]*(len(names)-1) + [BASE.DEGREE])
    row_keys = {target_key}
    for generator in generators:
        for multiplier in BASE.weak_compositions(
                BASE.DEGREE-generator["degree"], len(names)):
            for exponent, _ in generator["terms"]:
                row_keys.add(tuple(a+b for a, b in
                                   zip(exponent, multiplier, strict=True)))
    sorted_rows = sorted(row_keys)
    BASE.require(len(sorted_rows) == full_header["row_count"]
                 and BASE.digest([list(row) for row in sorted_rows])
                 == full_header["row_key_ledger_sha256"],
                 "full16 row-universe replay failed")

    original_rows = core_header["target_component_original_rows"]
    dual = {sorted_rows[original_rows[index]]: coefficient % BASE.PRIME
            for index, coefficient in solve["left_dual"]}
    BASE.require(dual.get(target_key) == solve["left_dual_target_pairing"],
                 "plus10 target pairing transport failed")
    records = []
    for index in REMAINING:
        degree, terms = BASE.homogenize(rows[index]["polynomial"],
                                        symbols, locals_map)
        histogram = Counter()
        examples = []
        for multiplier in BASE.weak_compositions(
                BASE.DEGREE-degree, len(names)):
            pairing = sum(coefficient*dual.get(tuple(
                a+b for a, b in zip(exponent, multiplier, strict=True)), 0)
                          for exponent, coefficient in terms) % BASE.PRIME
            histogram[pairing] += 1
            if pairing and len(examples) < 8:
                examples.append({"multiplier": list(multiplier),
                                 "pairing": pairing})
        records.append({"raw_index": index, "label": rows[index]["label"],
                        "degree": degree,
                        "multiplier_count": sum(histogram.values()),
                        "nonzero_pairing_count":
                            sum(value for key, value in histogram.items() if key),
                        "nonzero_examples": examples})
    result = {
        "status": "UNAUDITED modular plus10 d9 dual remaining-row audit",
        "prime": BASE.PRIME, "degree": BASE.DEGREE,
        "base_rows": [*BASE.KEPT, 10], "remaining_rows": list(REMAINING),
        "base_solve_sha256": sha256(SOLVE.read_bytes()).hexdigest(),
        "base_rank": solve["rank"],
        "base_target_in_image": solve["target_in_image"],
        "dual_terms": len(dual),
        "dual_target_pairing": solve["left_dual_target_pairing"],
        "records": records,
        "scope_guard": "Finite-field degree-9 routing only.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("plus10 remaining-row audit: PASS")
    print([(row["raw_index"], row["nonzero_pairing_count"])
           for row in records])
    print(result["result_sha256"])


if __name__ == "__main__":
    main()
