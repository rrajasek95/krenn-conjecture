#!/usr/bin/env python3
"""Audit the closure22 joint-semigroup separator against all literal X5 rows."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import sys


ROOT = Path(__file__).resolve().parents[2]
FINE = ROOT / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
if str(FINE) not in sys.path:
    sys.path.insert(0, str(FINE))

from audit_colour_holonomy_quotients import (
    PM8, key_add, matching_term, semigroup_key,
)
from audit_physical_graph_quotient import holonomy


RESULT = FINE / "results_closure22_joint_semigroup.json"
EXPECTED_RESULT_SHA256 = "3f5796331f1e71abc56344695c0620669663d39962664baff1ecfa59f77afdf1"
EXPECTED_LOGICAL_SHA256 = "4706ea6ed18bee8c78999a33122509b520100e91b2c35229c3b17703f34069f2"

EDGES = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
PAIRS = tuple((a, b) for a in range(3) for b in range(3))

SOURCE_MULTIPLIER_WITNESSES = {
    "00000010": (
        (0, 7, 0, 0), (1, 7, 0, 0), (2, 7, 0, 0),
        (3, 6, 0, 1), (3, 6, 1, 1), (3, 6, 1, 1),
        (4, 5, 1, 2), (4, 5, 1, 2), (4, 5, 2, 2),
    ),
    "01211222": (
        (0, 7, 0, 0), (1, 7, 0, 0), (2, 3, 0, 0),
        (3, 6, 0, 0), (3, 6, 0, 0), (4, 5, 0, 0),
        (4, 5, 1, 1), (4, 5, 1, 1), (6, 7, 1, 0),
    ),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def subtract(left, right):
    difference = tuple(a - b for a, b in zip(left, right, strict=True))
    return difference if min(difference) >= 0 else None


def word_name(word):
    return "".join(map(str, word))


def projected_word(word):
    row = defaultdict(int)
    for matching in PM8:
        row[semigroup_key(matching_term(word, matching))] += 1
    return dict(row)


def orbit_profile(word):
    counts = sorted(Counter(word).values(), reverse=True)
    return "+".join(map(str, counts))


def cap_triangle_profile(word):
    # Canonical labels: residual triangle 012, outside 345, cap 67.
    return (
        word[6], word[7],
        tuple(word[i] for i in (0, 1, 2)),
        tuple(word[i] for i in (3, 4, 5)),
    )


def readable_semigroup_key(key):
    return {
        "physical_edges": {
            f"{u}{v}": key[index]
            for index, (u, v) in enumerate(EDGES)
            if key[index]
        },
        "ordered_colour_pairs": {
            f"{a}{b}": key[28 + index]
            for index, (a, b) in enumerate(PAIRS)
            if key[28 + index]
        },
    }


def run_audit():
    actual_result_hash = hashlib.sha256(RESULT.read_bytes()).hexdigest()
    if EXPECTED_RESULT_SHA256 != "TO_BE_FILLED":
        require(actual_result_hash == EXPECTED_RESULT_SHA256,
                (actual_result_hash, EXPECTED_RESULT_SHA256))
    frozen = json.loads(RESULT.read_text())
    require(frozen["integer_dual_is_characteristic_zero_separator"], frozen)
    require(frozen["integer_dual_nonzero_row_pairings"] == 0, frozen)
    require(frozen["integer_dual_target_pairing"] == 1, frozen)
    dual = {
        tuple(item["column"]): item["coefficient"]
        for item in frozen["integer_dual"]
    }
    require(len(dual) == 16, len(dual))
    closure22 = set(frozen["source_words"])

    cone_key = semigroup_key(matching_term((0,) * 8, PM8[0]))
    target_columns = {
        key_add(cone_key, semigroup_key(term)) for term in holonomy()
    }

    killing = {}
    zero_touching = 0
    all_mixed = []
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        all_mixed.append(word)
        generator = projected_word(word)
        possible_quotients = set()
        for column in dual:
            for term in generator:
                difference = subtract(column, term)
                if difference is not None:
                    possible_quotients.add(difference)
        # Match the frozen Macaulay component exactly: a multiplier was
        # admitted only when some translated generator term met an actual
        # target column, not merely when it met a later echelon column.
        quotients = {
            quotient for quotient in possible_quotients
            if any(key_add(quotient, term) in target_columns
                   for term in generator)
        }
        pairings = []
        for quotient in quotients:
            pairing = sum(
                coefficient * dual.get(key_add(quotient, term), 0)
                for term, coefficient in generator.items()
            )
            if pairing:
                pairings.append((quotient, pairing))
        if pairings:
            lex_quotient, lex_pairing = min(pairings)
            killing[word_name(word)] = {
                "nonzero_translations": len(pairings),
                "pairing_values": sorted(Counter(value for _, value in pairings).items()),
                "lex_quotient": lex_quotient,
                "lex_pairing": lex_pairing,
                "profile": orbit_profile(word),
                "cap_triangle_profile": cap_triangle_profile(word),
                "in_closure22": word_name(word) in closure22,
            }
        elif quotients:
            zero_touching += 1

    require(not any(item["in_closure22"] for item in killing.values()),
            "the frozen separator does not annihilate closure22")
    by_profile = Counter(item["profile"] for item in killing.values())
    by_cap_pair = Counter(
        "pure" if item["cap_triangle_profile"][0] == item["cap_triangle_profile"][1]
        else "mixed"
        for item in killing.values()
    )
    by_triangle_palette = Counter(
        len(set(item["cap_triangle_profile"][2]))
        for item in killing.values()
    )
    selected_labels = (
        "00000010",  # seven-plus-one, exceptional cap endpoint
        "00001000",  # seven-plus-one, exceptional outside endpoint
        "01211222",  # the frozen rootless holonomy word
    )
    selected_killers = {}
    for label in selected_labels:
        if label not in killing:
            continue
        item = dict(killing[label])
        if label in SOURCE_MULTIPLIER_WITNESSES:
            witness = SOURCE_MULTIPLIER_WITNESSES[label]
            require(semigroup_key(witness) == item["lex_quotient"],
                    (label, semigroup_key(witness), item["lex_quotient"]))
            item["source_multiplier_cells"] = [list(cell) for cell in witness]
        item["lex_quotient"] = readable_semigroup_key(item["lex_quotient"])
        selected_killers[label] = item

    # The separator target is the cone-localized 3x3 triangle holonomy.
    # Every monomial in its 16-column dual support has total edge degree 13
    # and the same total ordered-colour-pair degree.
    degree_pairs = {
        (sum(column[:28]), sum(column[28:])) for column in dual
    }
    require(degree_pairs == {(13, 13)}, degree_pairs)

    result = {
        "status": "PASS exact-Z separator is broken by literal X5 rows",
        "pinned_joint_result_sha256": actual_result_hash,
        "dual_support": len(dual),
        "dual_target_pairing": frozen["integer_dual_target_pairing"],
        "all_mixed_x5_words": len(all_mixed),
        "closure22_words": len(closure22),
        "separator_killing_x5_words": len(killing),
        "separator_zero_but_touching_words": zero_touching,
        "killing_words_by_colour_count_profile": dict(sorted(by_profile.items())),
        "all_seven_plus_one_killing_labels": sorted(
            label for label, item in killing.items() if item["profile"] == "7+1"
        ),
        "killing_words_by_cap_pair_type": dict(sorted(by_cap_pair.items())),
        "killing_words_by_triangle_palette_size": {
            str(key): value for key, value in sorted(by_triangle_palette.items())
        },
        "selected_literal_killers": selected_killers,
        "lex_killing_word_labels": sorted(killing)[:32],
        "degree_pair": list(next(iter(degree_pairs))),
        "scope": (
            "A nonzero pairing proves only that the 16-column closure22 "
            "separator does not extend to the full X5 Macaulay row space. "
            "It does not prove target membership in the full X5 ideal."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(logical.encode()).hexdigest()
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
    path = Path(__file__).with_name("results_closure22_spine_attachment.json")
    if args.write_results:
        path.write_text(output)
    if args.check_results and path.read_text() != output:
        raise RuntimeError("stored result changed")
    print(output, end="")


if __name__ == "__main__":
    main()
