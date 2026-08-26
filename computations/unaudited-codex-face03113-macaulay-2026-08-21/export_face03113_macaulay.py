#!/usr/bin/env python3
"""Export a homogeneous Macaulay component for the (0,31,13) face.

Every column is a literal homogenized source generator times every homogeneous
multiplier of the required degree.  No term is truncated.  A positive solve
for t^N is therefore an exact affine unit certificate after Q replay.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))

import sympy as sp


HERE = Path(__file__).resolve().parent
SOURCE = (HERE.parent / "unaudited-codex-branch0-offdiag-support-strata-2026-08-21" /
          "results_recursive_face_charts.json")
KEY = "0:31:13"
DISCOVERY_ROWS = (7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def localizer_factor(record, label):
    value = record["localizers"][label]
    require(value.endswith("-1") and "*(" in value,
            f"unexpected {label} encoding")
    return value[value.index("*(") + 1:-2]


def weak_compositions(total, length, prefix=()):
    if length == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from weak_compositions(total - value, length - 1,
                                     prefix + (value,))


def digest(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, required=True)
    parser.add_argument("--full-rows", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(SOURCE.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    kept = ([row["raw_index"] for row in record["rows"]]
            if args.full_rows else list(DISCOVERY_ROWS))
    rows = [row for row in record["rows"] if row["raw_index"] in kept]
    selected = localizer_factor(record, "selected_base_terms")
    c_factor = localizer_factor(record, "both_live_c_numerators")
    sat = "s*(" + selected + ")*(" + c_factor + ")-1"
    labelled = [(f"raw_{row['raw_index']}_{row['label']}",
                 row["polynomial"]) for row in rows]
    labelled.append(("SAT_selected_base_times_C", sat))

    names = record["variable_names"] + ["s"]
    names = [name for name in names if any(
        re.search(rf"\b{re.escape(name)}\b", expression)
        for _, expression in labelled)]
    names.append("t")
    symbols = sp.symbols(" ".join(names))
    locals_map = dict(zip(names, symbols, strict=True))
    t_index = len(names) - 1

    generators = []
    for label, expression in labelled:
        poly = sp.Poly(sp.sympify(expression.replace("^", "**"),
                                  locals=locals_map), *symbols[:-1])
        require(poly.get_domain() in (sp.ZZ, sp.QQ),
                "generator is not rational")
        degree = int(poly.total_degree())
        terms = []
        for monomial, coefficient in poly.terms():
            require(coefficient.q == 1, "nonintegral source coefficient")
            exponent = tuple(int(value) for value in monomial) + (
                degree - sum(monomial),)
            terms.append((exponent, int(coefficient)))
        generators.append({"label": label, "degree": degree,
                           "terms": terms,
                           "source_expression_sha256":
                               sha256(expression.encode()).hexdigest()})
    require(args.degree >= max(row["degree"] for row in generators),
            "Macaulay degree is below a generator degree")

    multiplier_counts = []
    column_count = 0
    for generator in generators:
        multipliers = list(weak_compositions(
            args.degree - generator["degree"], len(names)))
        multiplier_counts.append(multipliers)
        column_count += len(multipliers)

    # First pass: complete row universe.  Repeated outputs within a column are
    # intentionally merged only after their exact integer coefficients add.
    row_keys = {tuple([0] * (len(names) - 1) + [args.degree])}
    for generator, multipliers in zip(
            generators, multiplier_counts, strict=True):
        for multiplier in multipliers:
            for exponent, _ in generator["terms"]:
                row_keys.add(tuple(a + b for a, b in
                                   zip(exponent, multiplier, strict=True)))
    sorted_rows = sorted(row_keys)
    row_index = {row: index for index, row in enumerate(sorted_rows)}
    target_key = tuple([0] * (len(names) - 1) + [args.degree])

    header = {
        "type": "header",
        "format": "krenn-homogeneous-macaulay-columns-v1",
        "face": KEY,
        "degree": args.degree,
        "variables": names,
        "row_count": len(sorted_rows),
        "column_count": column_count,
        "target": [[row_index[target_key], 1, 1]],
        "target_monomial": list(target_key),
        "kept_raw_rows": kept,
        "full_rows": args.full_rows,
        "source": str(SOURCE),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "generators": [{key: value for key, value in generator.items()
                        if key != "terms"} |
                       {"term_count": len(generator["terms"])}
                       for generator in generators],
        "generator_ledger_sha256": digest([
            {"label": generator["label"], "degree": generator["degree"],
             "terms": [[list(exponent), coefficient]
                       for exponent, coefficient in generator["terms"]]}
            for generator in generators]),
        "row_key_ledger_sha256": digest([list(row) for row in sorted_rows]),
        "scope_guard": (
            "Positive membership is exact after Q/source replay because all "
            "homogeneous multipliers and every column output are retained. "
            "Negative membership is bounded-degree only."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as output:
        output.write(json.dumps(header, sort_keys=True) + "\n")
        column = 0
        for generator, multipliers in zip(
                generators, multiplier_counts, strict=True):
            for multiplier in multipliers:
                entries = {}
                for exponent, coefficient in generator["terms"]:
                    row = tuple(a + b for a, b in
                                zip(exponent, multiplier, strict=True))
                    index = row_index[row]
                    entries[index] = entries.get(index, 0) + coefficient
                entries = [[index, coefficient]
                           for index, coefficient in sorted(entries.items())
                           if coefficient]
                require(entries, "zero Macaulay column")
                output.write(json.dumps({
                    "type": "column", "index": column,
                    "source_label": generator["label"],
                    "source_degree": generator["degree"],
                    "multiplier": list(multiplier),
                    "entries": entries,
                }, sort_keys=True) + "\n")
                column += 1
    require(column == column_count, "column census changed")
    print(json.dumps({
        "output": str(args.output), "degree": args.degree,
        "rows": len(sorted_rows), "columns": column_count,
        "kept_raw_rows": kept,
        "sha256": sha256(args.output.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
