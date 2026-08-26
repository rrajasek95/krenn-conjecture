#!/usr/bin/env python3
"""Pair the frozen degree-9 dual with all omitted literal-row columns.

The existing p=1009 left dual certifies that t^9 is outside the homogeneous
degree-9 component of the 12-row discovery subsystem.  This script rebuilds
the complete monomial universe independently, transports that dual back from
the peeled target component, and evaluates it on *every* degree-9 multiple
of the four omitted literal rows 6,9,10,11.  If all pairings vanish, the same
dual is a certificate for the full 16-row degree-9 component.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = (ROOT / "unaudited-codex-branch0-offdiag-support-strata-2026-08-21" /
          "results_recursive_face_charts.json")
MAC = ROOT / "unaudited-codex-face03113-macaulay-2026-08-21"
FULL = MAC / "face03113_subset_d9.jsonl"
CORE = MAC / "face03113_subset_d9_target_core.jsonl"
SOLVE = MAC / "results_face03113_subset_d9_core.p1009.json"
OUTPUT = HERE / "results_d9_dual_against_omitted_rows.json"
KEY = "0:31:13"
PRIME = 1009
KEPT = (7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)
OMITTED = (6, 9, 10, 11)
DEGREE = 9


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def weak_compositions(total, length, prefix=()):
    if length == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from weak_compositions(total-value, length-1, prefix+(value,))


def localizer_factor(record, label):
    value = record["localizers"][label]
    require(value.endswith("-1") and "*(" in value,
            f"unexpected localizer {label}")
    return value[value.index("*(")+1:-2]


def homogenize(expression, symbols, locals_map):
    poly = sp.Poly(sp.sympify(expression.replace("^", "**"),
                              locals=locals_map), *symbols[:-1])
    require(poly.get_domain() in (sp.ZZ, sp.QQ), "nonrational generator")
    degree = int(poly.total_degree())
    terms = []
    for monomial, coefficient in poly.terms():
        require(coefficient.q == 1, "nonintegral source coefficient")
        terms.append((tuple(int(value) for value in monomial) +
                      (degree-sum(monomial),), int(coefficient)))
    return degree, terms


def main():
    payload = json.loads(SOURCE.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    rows = {row["raw_index"]: row for row in record["rows"]}
    full_header = json.loads(FULL.open().readline())
    core_header = json.loads(CORE.open().readline())
    solve = json.loads(SOLVE.read_text())
    require(full_header["degree"] == core_header["degree"] == DEGREE
            and full_header["kept_raw_rows"] == list(KEPT)
            and solve["prime"] == PRIME and not solve["target_in_image"],
            "frozen degree-9 interface changed")
    names = full_header["variables"]
    symbols = sp.symbols(" ".join(names))
    locals_map = dict(zip(names, symbols, strict=True))

    selected = localizer_factor(record, "selected_base_terms")
    c_factor = localizer_factor(record, "both_live_c_numerators")
    sat = "s*(" + selected + ")*(" + c_factor + ")-1"
    kept_labelled = [(f"raw_{index}_{rows[index]['label']}",
                      rows[index]["polynomial"]) for index in KEPT]
    kept_labelled.append(("SAT_selected_base_times_C", sat))
    kept_generators = []
    for label, expression in kept_labelled:
        degree, terms = homogenize(expression, symbols, locals_map)
        kept_generators.append({"label": label, "degree": degree,
                                "terms": terms})
    require(digest([{"label": row["label"], "degree": row["degree"],
                     "terms": [[list(exponent), coefficient]
                               for exponent, coefficient in row["terms"]]}
                    for row in kept_generators])
            == full_header["generator_ledger_sha256"],
            "independent generator ledger replay failed")

    target_key = tuple([0]*(len(names)-1) + [DEGREE])
    row_keys = {target_key}
    for generator in kept_generators:
        for multiplier in weak_compositions(
                DEGREE-generator["degree"], len(names)):
            for exponent, _ in generator["terms"]:
                row_keys.add(tuple(a+b for a, b in
                                   zip(exponent, multiplier, strict=True)))
    sorted_rows = sorted(row_keys)
    require(len(sorted_rows) == full_header["row_count"]
            and digest([list(row) for row in sorted_rows])
            == full_header["row_key_ledger_sha256"],
            "independent row universe replay failed")

    original_rows = core_header["target_component_original_rows"]
    dual_by_key = {}
    for core_index, coefficient in solve["left_dual"]:
        original_index = original_rows[core_index]
        dual_by_key[sorted_rows[original_index]] = coefficient % PRIME
    require(dual_by_key.get(target_key) ==
            solve["left_dual_target_pairing"] % PRIME,
            "target/dual pairing transport failed")

    omitted_records = []
    nonzero_total = 0
    for index in OMITTED:
        degree, terms = homogenize(rows[index]["polynomial"],
                                   symbols, locals_map)
        histogram = Counter()
        examples = []
        count = 0
        for multiplier in weak_compositions(DEGREE-degree, len(names)):
            pairing = 0
            for exponent, coefficient in terms:
                key = tuple(a+b for a, b in
                            zip(exponent, multiplier, strict=True))
                pairing += coefficient*dual_by_key.get(key, 0)
            pairing %= PRIME
            histogram[pairing] += 1
            if pairing:
                count += 1
                if len(examples) < 8:
                    examples.append({"multiplier": list(multiplier),
                                     "pairing": pairing})
        nonzero_total += count
        omitted_records.append({
            "raw_index": index, "label": rows[index]["label"],
            "degree": degree,
            "multiplier_count": sum(histogram.values()),
            "nonzero_pairing_count": count,
            "pairing_histogram": [[value, multiplicity]
                                  for value, multiplicity in
                                  sorted(histogram.items())],
            "nonzero_examples": examples,
        })

    result = {
        "status": "UNAUDITED exact-interface modular d9 omitted-row dual audit",
        "face": KEY, "prime": PRIME, "degree": DEGREE,
        "kept_raw_rows": list(KEPT), "omitted_raw_rows": list(OMITTED),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "full_input_sha256": sha256(FULL.read_bytes()).hexdigest(),
        "core_input_sha256": sha256(CORE.read_bytes()).hexdigest(),
        "solve_sha256": sha256(SOLVE.read_bytes()).hexdigest(),
        "dual_terms": len(dual_by_key),
        "dual_target_pairing": solve["left_dual_target_pairing"],
        "omitted_records": omitted_records,
        "total_nonzero_omitted_column_pairings": nonzero_total,
        "conclusion": ("The frozen dual extends to the full 16-row d9 "
                       "component." if nonzero_total == 0 else
                       "At least one omitted-row column breaks the frozen dual."),
        "scope_guard": ("This is a finite-field degree-9 statement only. "
                        "It neither proves affine nonmembership nor a Q-unit."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    HERE.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("omitted-row d9 dual audit: PASS")
    print("nonzero counts", [(row["raw_index"],
                              row["nonzero_pairing_count"])
                             for row in omitted_records])
    print("result sha256", result["result_sha256"])


if __name__ == "__main__":
    main()
