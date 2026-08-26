#!/usr/bin/env python3
"""Attach the terminal closure22 joint-semigroup separator to literal X5."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import json
import sys


ROOT = Path(__file__).resolve().parents[2]
FINE = ROOT / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
if str(FINE) not in sys.path:
    sys.path.insert(0, str(FINE))

from audit_closure22_joint_semigroup import projected_word
from audit_colour_holonomy_quotients import key_add, semigroup_key


UPSTREAM = FINE / "results_closure22_joint_cegar.json"
EXPECTED_UPSTREAM_SHA256 = "69f19e71df27d55cbe76a1e101fe2daad68d6b5a4a23d8d98e3f6e9a78d6bd75"
EXPECTED_LOGICAL_SHA256 = "b77fd6eb39eb8b6d1e4119569aa5afdd6449424be2da8557ebce945c61287c1d"
EDGES = tuple((u, v) for u in range(8) for v in range(u + 1, 8))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def subtract(left, right):
    difference = tuple(a - b for a, b in zip(left, right, strict=True))
    return difference if min(difference) >= 0 else None


def word_label(word):
    return "".join(map(str, word))


def literal_multiplier(translation):
    edge_occurrences = [
        edge for edge, count in zip(EDGES, translation[:28], strict=True)
        for _ in range(count)
    ]
    pair_occurrences = [
        (index // 3, index % 3)
        for index, count in enumerate(translation[28:]) for _ in range(count)
    ]
    require(len(edge_occurrences) == len(pair_occurrences) == 9,
            (len(edge_occurrences), len(pair_occurrences)))
    cells = tuple(
        (u, v, a, b)
        for (u, v), (a, b) in zip(edge_occurrences, pair_occurrences, strict=True)
    )
    require(semigroup_key(cells) == translation, "literal multiplier lift failed")
    return [list(cell) for cell in cells]


def serialize_translation(translation):
    return {
        "physical_edges": [
            [u, v, count]
            for (u, v), count in zip(EDGES, translation[:28], strict=True)
            if count
        ],
        "ordered_colour_pairs": [
            [index // 3, index % 3, count]
            for index, count in enumerate(translation[28:]) if count
        ],
    }


def crossing_rows(word, dual):
    generator = projected_word(word)
    translations = set()
    for column in dual:
        for term in generator:
            difference = subtract(column, term)
            if difference is not None:
                translations.add(difference)
    crossings = []
    for translation in translations:
        pairing = sum(
            coefficient * dual.get(key_add(translation, term), 0)
            for term, coefficient in generator.items()
        )
        if pairing:
            crossings.append((translation, pairing))
    return sorted(crossings)


def serialize_crossing(translation, pairing):
    return {
        "pairing": pairing,
        "translation": serialize_translation(translation),
        "literal_multiplier_cells": literal_multiplier(translation),
    }


def run_audit():
    upstream_bytes = UPSTREAM.read_bytes()
    upstream_hash = sha256(upstream_bytes).hexdigest()
    require(upstream_hash == EXPECTED_UPSTREAM_SHA256,
            (upstream_hash, EXPECTED_UPSTREAM_SHA256))
    upstream = json.loads(upstream_bytes)
    require(upstream["terminal_integer_is_full_semigroup_separator"], upstream)
    require(upstream["terminal_integer_crossing_translations"] == 0, upstream)
    require(upstream["terminal_integer_target_pairing"] == 1, upstream)
    require(upstream["terminal_integer_max_abs_translation_pairing"] == 0, upstream)
    dual = {
        tuple(item["column"]): item["coefficient"]
        for item in upstream["terminal_integer_dual"]
    }
    require(len(dual) == 100, len(dual))
    closure22 = set(upstream["source_words"])

    root_word = tuple(map(int, "01211222"))
    root_crossings = crossing_rows(root_word, dual)
    require(root_crossings, "rootless X5 word did not cross terminal separator")
    require(word_label(root_word) not in closure22, closure22)

    seven_one = []
    for base in range(3):
        for exceptional in range(3):
            if base == exceptional:
                continue
            for site in range(8):
                word = [base] * 8
                word[site] = exceptional
                crossings = crossing_rows(tuple(word), dual)
                if crossings:
                    seven_one.append({
                        "word": word_label(word),
                        "crossing_translations": len(crossings),
                        "pairing_histogram": dict(sorted(Counter(
                            pairing for _, pairing in crossings
                        ).items())),
                        "lex_crossing": serialize_crossing(*crossings[0]),
                    })
    require(len(seven_one) == 7, len(seven_one))
    require(all(item["word"] not in closure22 for item in seven_one), seven_one)

    result = {
        "status": "PASS terminal closure22 separator is killed by mandatory literal X5",
        "upstream_sha256": upstream_hash,
        "terminal_separator_support": len(dual),
        "terminal_separator_max_abs_coefficient": upstream[
            "terminal_integer_dual_balanced_max_abs"
        ],
        "terminal_target_pairing": upstream["terminal_integer_target_pairing"],
        "closure22_existing_word_crossings": upstream[
            "terminal_integer_crossing_translations"
        ],
        "rootless_word": word_label(root_word),
        "rootless_word_in_closure22": False,
        "rootless_crossing_translations": len(root_crossings),
        "rootless_pairing_histogram": dict(sorted(Counter(
            pairing for _, pairing in root_crossings
        ).items())),
        "rootless_lex_crossing": serialize_crossing(*root_crossings[0]),
        "seven_plus_one_total_orbit_words": 48,
        "seven_plus_one_fixed_separator_crossing_words": seven_one,
        "theorem_scope": (
            "A nonzero pairing proves that adjoining the displayed literal "
            "mixed-X5 row invalidates this terminal closure22 dual. It does "
            "not prove holonomy-target membership in the enlarged ideal and "
            "does not imply either holonomy rank three or rank at most two."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(logical.encode()).hexdigest()
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LOGICAL_SHA256,
                (digest, EXPECTED_LOGICAL_SHA256))
    result["logical_sha256"] = digest
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result_path = Path(__file__).with_name(
        "results_terminal_separator_spine_attachment.json"
    )
    if args.write_results:
        result_path.write_text(output)
    if args.check_results:
        require(result_path.read_text() == output, "stored result changed")
    print(output, end="")


if __name__ == "__main__":
    main()
