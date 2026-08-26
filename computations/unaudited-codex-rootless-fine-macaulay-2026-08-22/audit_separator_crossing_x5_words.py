#!/usr/bin/env python3
"""Find minimal mixed-X5 rows which kill the 16-column joint separator.

The frozen closure22 separator is reconstructed exactly, including its
integer lift.  For every literal mixed word w and every degree-nine joint
semigroup translation which can meet one of the 16 supported columns, the
script computes the integer pairing with translated X_w.  No decorated
Macaulay matrix or full-ring Groebner basis is assembled.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations, product
import argparse
import json
from math import factorial
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_closure22_joint_semigroup import projected_word, run_audit
from audit_colour_holonomy_quotients import PM8, key_add, semigroup_key


RESULTS = HERE / "results_terminal_separator_new_x5_words.json"
FROZEN_RESULTS = HERE / "results_closure22_joint_cegar.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def word_label(word):
    return "".join(map(str, word))


def word_shape(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def full_word_orbit_size(shape):
    site_orbit = factorial(8)
    for count in shape:
        site_orbit //= factorial(count)
    unused = 3 - len(shape)
    colour_orbit = factorial(3) // factorial(unused)
    for multiplicity in Counter(shape).values():
        colour_orbit //= factorial(multiplicity)
    return site_orbit * colour_orbit


def full_word_orbit(word):
    answer = set()
    for site_permutation in permutations(range(8)):
        moved = tuple(word[site_permutation[index]] for index in range(8))
        for colour_permutation in permutations(range(3)):
            answer.add(tuple(colour_permutation[value] for value in moved))
    return answer


def subtract(left, right):
    difference = tuple(a - b for a, b in zip(left, right, strict=True))
    return difference if min(difference) >= 0 else None


def translation_metrics(translation):
    edge = translation[:28]
    colour = translation[28:]
    require(sum(edge) == sum(colour) == 9,
            (sum(edge), sum(colour), "translation is not degree nine"))
    return {
        "distinct_physical_edges": sum(value != 0 for value in edge),
        "max_physical_edge_multiplicity": max(edge),
        "distinct_ordered_colour_pairs": sum(value != 0 for value in colour),
        "max_ordered_colour_pair_multiplicity": max(colour),
    }


def serialize_translation(translation):
    edges = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
    return {
        "physical_edges": [
            [u, v, value] for (u, v), value in zip(edges, translation[:28], strict=True)
            if value
        ],
        "ordered_colour_pairs": [
            [index // 3, index % 3, value]
            for index, value in enumerate(translation[28:]) if value
        ],
    }


def literal_multiplier(translation):
    """Choose one audited decorated monomial realizing the joint key."""
    edges = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
    edge_occurrences = [
        edge for edge, value in zip(edges, translation[:28], strict=True)
        for _ in range(value)
    ]
    pair_occurrences = [
        (index // 3, index % 3)
        for index, value in enumerate(translation[28:]) for _ in range(value)
    ]
    require(len(edge_occurrences) == len(pair_occurrences) == 9,
            "joint translation did not admit the canonical literal lift")
    cells = [
        [u, v, a, b]
        for (u, v), (a, b) in zip(edge_occurrences, pair_occurrences, strict=True)
    ]
    require(semigroup_key(tuple(tuple(cell) for cell in cells)) == translation,
            "canonical literal multiplier does not realize the joint key")
    return cells


def scan():
    frozen = json.loads(FROZEN_RESULTS.read_text())
    separator_flag = frozen.get("terminal_integer_is_full_semigroup_separator", False)
    require(separator_flag,
            "frozen modular dual did not lift over Z")
    dual = {
        tuple(record["column"]): record["coefficient"]
        for record in frozen["terminal_integer_dual"]
    }
    require(len(dual) == 100, len(dual))
    closure_words = set(frozen["source_words"])

    records = []
    word_summaries = []
    shape_words = defaultdict(set)
    shape_rows = Counter()
    projected_rows = set()
    all_words = tuple(product(range(3), repeat=8))
    for word in all_words:
        if len(set(word)) == 1:
            continue
        generator = projected_word(word)
        translations = set()
        for dual_column in dual:
            for term_key in generator:
                difference = subtract(dual_column, term_key)
                if difference is not None:
                    translations.add(difference)
        crossings = []
        for translation in translations:
            pairing = sum(
                coefficient * dual.get(key_add(translation, term_key), 0)
                for term_key, coefficient in generator.items()
            )
            if not pairing:
                continue
            frozen_row = tuple(sorted(
                (key_add(translation, term_key), coefficient)
                for term_key, coefficient in generator.items()
            ))
            projected_rows.add(frozen_row)
            crossings.append((translation, pairing))
        if not crossings:
            continue
        label = word_label(word)
        shape = word_shape(word)
        shape_words[shape].add(label)
        shape_rows[shape] += len(crossings)
        word_summaries.append({
            "word": label,
            "shape": list(shape),
            "full_S8xS3_orbit_size": full_word_orbit_size(shape),
            "already_in_closure22": label in closure_words,
            "crossing_translations": len(crossings),
            "pairing_histogram": dict(sorted(Counter(
                pairing for _translation, pairing in crossings
            ).items())),
        })
        for translation, pairing in crossings:
            metrics = translation_metrics(translation)
            records.append({
                "word": label,
                "shape": list(shape),
                "already_in_closure22": label in closure_words,
                "translation": list(translation),
                "pairing": pairing,
                **metrics,
            })

    require(records, "no separator-crossing mixed row found")
    existing_records = [row for row in records if row["already_in_closure22"]]
    new_records = [row for row in records if not row["already_in_closure22"]]
    require(not existing_records,
            "terminal separator was crossed by an abstract closure22 translation")
    require(new_records, "no new-word crossing of the terminal separator")
    require((len(new_records), len({row["word"] for row in new_records}),
             len(projected_rows)) == (44127, 4294, 44127),
            (len(new_records), len({row["word"] for row in new_records}),
             len(projected_rows)))

    def literal_order(row):
        return (
            row["distinct_physical_edges"],
            row["distinct_ordered_colour_pairs"],
            row["max_physical_edge_multiplicity"],
            row["max_ordered_colour_pair_multiplicity"],
            row["word"], row["translation"],
        )

    best_new_literal = min(new_records, key=lambda row: (
        full_word_orbit_size(tuple(row["shape"])),
        *literal_order(row),
    ))
    new_word_summaries = [row for row in word_summaries
                          if not row["already_in_closure22"]]
    best_new_word = min(new_word_summaries, key=lambda row: (
        row["full_S8xS3_orbit_size"], row["crossing_translations"], row["word"]
    ))
    representative_word = tuple(map(int, best_new_word["word"]))
    orbit = full_word_orbit(representative_word)
    orbit_labels = {word_label(word) for word in orbit}
    missing_orbit_labels = sorted(orbit_labels - closure_words)
    crossing_orbit_labels = sorted(
        orbit_labels & {row["word"] for row in word_summaries}
    )

    shape_census = []
    for shape in sorted(shape_words, key=lambda row: (full_word_orbit_size(row), row)):
        shape_census.append({
            "shape": list(shape),
            "full_S8xS3_orbit_size": full_word_orbit_size(shape),
            "crossing_words": len(shape_words[shape]),
            "crossing_translated_rows": shape_rows[shape],
        })
    require(shape_census[0] == {
        "shape": [7, 1], "full_S8xS3_orbit_size": 48,
        "crossing_words": 7, "crossing_translated_rows": 87,
    }, shape_census[0])

    def serialize_killer(row):
        translation = tuple(row["translation"])
        return {
            **{key: value for key, value in row.items()
               if key != "translation"},
            "translation": serialize_translation(translation),
            "joint_translation_vector": row["translation"],
            "literal_multiplier_cells": literal_multiplier(translation),
            "source_provenance": (
                "the literal mixed amplitude row X_word=0, multiplied by the "
                "displayed degree-nine decorated monomial; its joint key is "
                "the displayed translation vector"
            ),
        }

    minimal_generator_rows = sorted(
        (row for row in new_records if row["word"] == best_new_word["word"]),
        key=lambda row: (row["translation"], row["pairing"]),
    )
    require(len(minimal_generator_rows) == 4, len(minimal_generator_rows))

    result = {
        "status": "PASS exact new-word crossings of terminal separator",
        "separator": {
            "support": len(dual),
            "coefficients": dict(sorted(Counter(dual.values()).items())),
            "target_pairing": frozen["terminal_integer_target_pairing"],
            "closure22_abstract_crossing_translations": frozen[
                "terminal_integer_crossing_translations"
            ],
            "closure22_abstract_crossing_words": frozen[
                "terminal_integer_crossing_words"
            ],
            "remainder_sha256": frozen["final_remainder_sha256"],
            "frozen_result_sha256": sha256(FROZEN_RESULTS.read_bytes()).hexdigest(),
        },
        "census": {
            "mixed_words": 3 ** 8 - 3,
            "crossing_words": len(word_summaries),
            "crossing_translated_rows": len(records),
            "distinct_projected_crossing_rows": len(projected_rows),
            "existing_closure22_crossing_words": 0,
            "existing_closure22_crossing_translated_rows": len(existing_records),
            "new_crossing_words": len(new_word_summaries),
            "new_crossing_translated_rows": len(new_records),
            "shape_orbits_with_crossings": len(shape_census),
            "shape_census": shape_census,
        },
        "minimal_new_literal_killer": serialize_killer(best_new_literal),
        "minimal_new_word_generator": best_new_word,
        "minimal_new_word_generator_crossing_rows": [
            serialize_killer(row) for row in minimal_generator_rows
        ],
        "minimal_new_symmetry_family": {
            "shape": best_new_word["shape"],
            "representative": best_new_word["word"],
            "full_S8xS3_orbit_size": len(orbit_labels),
            "already_present_closure22_words": sorted(orbit_labels & closure_words),
            "additional_words_to_complete_orbit": len(missing_orbit_labels),
            "additional_word_labels": missing_orbit_labels,
            "crossing_words_in_orbit": len(crossing_orbit_labels),
            "crossing_word_labels": crossing_orbit_labels,
            "why_it_kills": (
                "at least one translated row in this source-symmetry family "
                "pairs nontrivially with the primitive separator"
            ),
        },
        "word_summaries": sorted(word_summaries, key=lambda row: row["word"]),
        "scope": (
            "Exact characteristic-zero calculation in the joint 28-edge plus "
            "9 ordered-colour semigroup quotient. A nonzero pairing kills this "
            "specific terminal separator after adjoining the row. This does "
            "not prove the holonomy target belongs to the enlarged literal "
            "decorated ideal. S8xS3 shape counts are source-word orbits only; "
            "the joint quotient does not retain enough correlation to assert "
            "literal multiplier orbit transport."
        ),
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = scan()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored separator-crossing census changed")
    print(json.dumps({
        "status": result["status"],
        "census": result["census"],
        "minimal_new_literal_killer": result["minimal_new_literal_killer"],
        "minimal_new_word_generator": result["minimal_new_word_generator"],
        "minimal_new_symmetry_family": result["minimal_new_symmetry_family"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
