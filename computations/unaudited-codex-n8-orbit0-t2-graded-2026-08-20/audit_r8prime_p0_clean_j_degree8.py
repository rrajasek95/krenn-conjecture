#!/usr/bin/env python3
"""Test P0 itself in the clean 16-generator binary ideal J."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPAN_PATH = HERE / "audit_r8prime_p0_binary_packet_span.py"
SPEC = importlib.util.spec_from_file_location("p0_span", SPAN_PATH)
SPAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SPAN)
EXPORT = SPAN.EXPORT
BASE = SPAN.BASE
OUT = HERE / "results_r8prime_p0_clean_j_degree8.json"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def alternating_words():
    words = []
    for choices in product((1, 2), repeat=4):
        word = []
        for colour in choices:
            word.extend((colour, 3 - colour))
        words.append(tuple(word))
    return tuple(words)


def transform_word(word, action):
    sites, colours = EXPORT.STABILIZER[action]
    moved = [None] * BASE.N
    for site, colour in enumerate(word):
        moved[sites[site]] = colours[colour]
    return tuple(moved)


def transform_column(column, action):
    word, multiplier = column
    transform = EXPORT.TRANSFORMS[action]
    return (transform_word(word, action),
            bytes(sorted(transform[cell] for cell in multiplier)))


def canonical_column(column):
    return min(transform_column(column, action) for action in SPAN.H_ACTIONS)


def main():
    raw = json.loads(SPAN.R8P.read_text())
    actual, target, _selected = SPAN.extract_p0(raw)
    words = alternating_words()
    require(len(words) == 16, "alternating word count changed")
    raw_columns = set()
    for word in words:
        mate = SPAN.complement(word)
        for matching in BASE.PM8:
            multiplier = BASE.term_ids(mate, matching)
            require(not any(cell in EXPORT.ANCHORS for cell in multiplier),
                    "alternating complement multiplier contains an anchor")
            raw_columns.add((word, multiplier))
    require(len(raw_columns) == 16 * 105, "raw clean-J column count changed")
    representatives = sorted({canonical_column(column)
                              for column in raw_columns})
    require(all(canonical_column(column) == column for column in representatives),
            "clean-J representative is not canonical")

    columns = []
    records = []
    for word, multiplier in representatives:
        vector = Counter()
        for term in BASE.word_terms(word):
            row = bytes(sorted(multiplier + term))
            require(not any(cell in EXPORT.ANCHORS for cell in row),
                    "clean-J output left K-degree eight")
            vector[SPAN.canonical_row(row)] += 1
        columns.append(vector)
        records.append({
            "word": "".join(map(str, word)),
            "multiplier": multiplier.hex(),
            "row_orbits": len(vector),
            "mass": sum(vector.values()),
        })

    solution, rank, inconsistent = SPAN.exact_solve(columns, target)
    certificate = []
    if solution is not None:
        for coefficient, record in zip(solution, records):
            if coefficient:
                certificate.append({
                    **record,
                    "coefficient": [coefficient.numerator,
                                    coefficient.denominator],
                })
    result = {
        "status": "UNAUDITED exact clean binary ideal audit",
        "input_r8prime_sha256": sha256(SPAN.R8P.read_bytes()).hexdigest(),
        "p0_labelled_support": len(actual),
        "p0_quotient_row_orbits": len(target),
        "clean_generators": len(words),
        "generator_condition": (
            "w is binary and opposite on every physical M0 pair; all 105 "
            "terms of H_w have K-degree four"
        ),
        "raw_degree8_columns": len(raw_columns),
        "invariant_column_orbits": len(representatives),
        "matrix_row_orbits": len(set(target).union(
            *(set(column) for column in columns))),
        "matrix_rank": rank,
        "p0_in_J": solution is not None,
        "first_inconsistent_row": None if inconsistent is None else
            [inconsistent[0].hex(), inconsistent[1].numerator,
             inconsistent[1].denominator],
        "certificate_terms": len(certificate),
        "certificate": certificate,
        "implication": (
            "If p0_in_J is true, multiplying the exact degree-eight identity "
            "by P0 proves P0^2 in J in degree sixteen, hence supplies the "
            "requested clean associated-graded source identity without a "
            "broad P0^2 component closure."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8' P0 clean-J degree8 audit: PASS")
    print("columns/rows/rank/in-J:", len(representatives),
          result["matrix_row_orbits"], rank, solution is not None)
    print("certificate terms:", len(certificate))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
