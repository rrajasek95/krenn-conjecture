#!/usr/bin/env python3
"""Export the source-labelled nonlinear row cores found by the tangent screen."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORTER = (ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22"
            / "export_canonical_triangle_branch_msolve.py")
RESULT = HERE / "results_canonical_triangle_ff_screen.json"


def load_exporter():
    spec = importlib.util.spec_from_file_location("triangle_exporter", EXPORTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fibre_row(source, word):
    terms = [source.matching_monomial(word, matching) for matching in source.PM8]
    if len(set(word)) == 1:
        terms.append("-1")
    return "+".join(terms).replace("+-", "-")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("branch")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = load_exporter()
    if args.branch not in source.BRANCHES:
        raise SystemExit(f"unknown branch {args.branch}")
    payload = json.loads(RESULT.read_text())
    record = next(item for item in payload["records"]
                  if item["seed"] == payload["seeds"][0]
                  and item["branch"] == args.branch)
    mixed = [item["word"] for item in record["selected_row_labels"]
             if item["kind"] == "mixed"]
    mixed.append(record["contradiction_row"]["word"])
    assert len(mixed) == len(set(mixed)) == 239
    rows = [fibre_row(source, tuple(map(int, word))) for word in mixed]
    rows.extend(fibre_row(source, (colour,) * 8) for colour in range(3))
    rows.extend(source.membership_rows(args.branch))
    rows.append(f"sy0*{source.xvar(0, 6, 0, 1)}-1")
    variables = source.source_variables() + source.witness_variables() + ["sy0"]
    assert len(rows) == 252 and len(variables) == 361
    output = args.output or HERE / f"core252_{args.branch}_p32003.ms"
    with output.open("w") as handle:
        handle.write(",".join(variables) + "\n32003\n")
        for index, row in enumerate(rows):
            handle.write(row)
            handle.write(",\n" if index + 1 < len(rows) else "\n")
    print(output)
    print(f"variables={len(variables)} equations={len(rows)} bytes={output.stat().st_size}")


if __name__ == "__main__":
    main()
