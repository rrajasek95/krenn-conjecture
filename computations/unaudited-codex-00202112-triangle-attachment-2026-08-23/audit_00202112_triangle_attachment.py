#!/usr/bin/env python3
"""Exact source audit of the unique full62 crossing from F_00202112."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINE = ROOT / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
if str(FINE) not in sys.path:
    sys.path.insert(0, str(FINE))

from audit_closure22_joint_semigroup import projected_word
from audit_colour_holonomy_quotients import (
    PM8, key_add, matching_term, semigroup_key,
)


SEPARATOR = (ROOT / "computations/unaudited-codex-profile71-terminal-char0-2026-08-23"
             / "results_full_profile71_terminal_char0.json")
SEPARATOR_SHA256 = "b261d6f47e0386db33b8ee6ac33fc4c069a833010c2b413054b3547ab516f015"
UPSTREAM = FINE / "results_closure22_plus_full_profile71_joint_cegar_rust_p32003.json"
UPSTREAM_SHA256 = "fa12b6726b7dbc7f448f860d6afc6ea0dd870d1dff0c2604712d4e9f513d7d0d"
MANIFEST = (ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22"
            / "canonical_triangle_incidence_manifest.json")
MANIFEST_SHA256 = "0b556f2f217e1a1f158edb66e64d74fa8f5f7b649be182c797c10711f378b529"
CROSSWORD = (ROOT / "computations/unaudited-codex-triangle-crossword-observation-2026-08-22"
             / "results_triangle_crossword_observation.json")
CROSSWORD_SHA256 = "80ea9a26eb958f174d4e172570cfb1fd9d1fdfd187518f8f02e95a8c2dd62e8f"
FIVE_SET = (ROOT / "computations/unaudited-codex-triangle-five-set-annihilator-2026-08-22"
            / "results_triangle_five_set_annihilator.json")
FIVE_SET_SHA256 = "6cd93663ed6bf392a24ee74cc1546cdcaa8b8124d07012910df69920bbf9abae"
OUT = HERE / "results_00202112_triangle_attachment.json"
EXPECTED_LOGICAL_SHA256 = "6157d8af0d9a0bc45f4600cdbea83799db937e93e3f74f2f8819822351abae3c"

WORD_LABEL = "00202112"
WORD = tuple(map(int, WORD_LABEL))
CAP = (6, 7)
TRIANGLE = (0, 1, 2)
OUTSIDE = (3, 4, 5)

# One literal degree-nine realization of the unique joint-semigroup
# translation.  Orientation is always increasing in the two site labels.
MULTIPLIER = (
    (0, 7, 0, 0),
    (1, 7, 0, 0),
    (2, 5, 0, 0),
    (3, 4, 0, 0),
    (3, 6, 0, 0),
    (3, 7, 1, 0),
    (4, 5, 1, 1),
    (4, 6, 1, 1),
    (5, 6, 1, 2),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_pinned(path, expected):
    raw = path.read_bytes()
    actual = sha256(raw).hexdigest()
    require(actual == expected, (str(path), actual, expected))
    return json.loads(raw), actual


def subtract(left, right):
    value = tuple(a - b for a, b in zip(left, right, strict=True))
    return value if min(value) >= 0 else None


def variable(cell):
    u, v, a, b = cell
    return f"A_{u}{v}[{a}{b}]"


def literal_term(cells):
    cells = tuple(sorted(cells))
    return {
        "coefficient": 1,
        "cells": [list(cell) for cell in cells],
        "monomial": " ".join(variable(cell) for cell in cells),
    }


def matching_crossings(matching, shore):
    shore = set(shore)
    return sum((u in shore) != (v in shore) for u, v in matching)


def run_audit():
    separator, separator_hash = load_pinned(SEPARATOR, SEPARATOR_SHA256)
    upstream, upstream_hash = load_pinned(UPSTREAM, UPSTREAM_SHA256)
    manifest, manifest_hash = load_pinned(MANIFEST, MANIFEST_SHA256)
    crossword, crossword_hash = load_pinned(CROSSWORD, CROSSWORD_SHA256)
    five_set, five_set_hash = load_pinned(FIVE_SET, FIVE_SET_SHA256)

    dual = {
        tuple(record["column"]): record["coefficient"]
        for record in separator["integer_separator"]
    }
    generator = projected_word(WORD)
    require(len(generator) == len(PM8) == 105, len(generator))

    translations = set()
    for column in dual:
        for term in generator:
            difference = subtract(column, term)
            if difference is not None:
                translations.add(difference)
    require(len(translations) == 1, len(translations))
    translation = translations.pop()
    require(semigroup_key(MULTIPLIER) == translation,
            (semigroup_key(MULTIPLIER), translation))

    crossings = []
    for matching_index, matching in enumerate(PM8):
        decorated = matching_term(WORD, matching)
        column = key_add(translation, semigroup_key(decorated))
        coefficient = generator[semigroup_key(decorated)]
        dual_coefficient = dual.get(column, 0)
        if dual_coefficient:
            crossings.append({
                "matching_index": matching_index,
                "matching": [list(edge) for edge in matching],
                "decorated_matching_term": literal_term(decorated),
                "generator_coefficient": coefficient,
                "separator_coefficient": dual_coefficient,
                "pairing_contribution": coefficient * dual_coefficient,
                "supported_column": list(column),
                "translated_literal_term": literal_term(MULTIPLIER + decorated),
            })
    require(len(crossings) == 1, crossings)
    crossing = crossings[0]
    require((crossing["matching_index"], crossing["pairing_contribution"])
            == (51, 1), crossing)
    matching = tuple(tuple(edge) for edge in crossing["matching"])
    require(matching == ((0, 4), (1, 5), (2, 3), (6, 7)), matching)

    # This is a direct cap matching and the remaining three edges are a
    # bijection T -> O.  Exactly 3!=6 perfect matchings have that shape.
    direct_shapes = {
        tuple(sorted((CAP,) + tuple((t, o) for t, o in zip(TRIANGLE, image))))
        for image in permutations(OUTSIDE)
    }
    require(len(direct_shapes) == 6 and matching in direct_shapes,
            (len(direct_shapes), matching))
    require(crossword["cramer_remainder_cap_partition"] == {
        "direct_A67": 6,
        "internal_triangle_response": 18,
        "outside_triangle_response": 36,
        "triangle_kernel_consequence": (
            "The 36 outside-triangle response terms vanish on ker(L_T); "
            "the unresolved remainder is exactly 6 direct-A67 plus 18 "
            "internal-triangle-response matchings."
        ),
    }, crossword["cramer_remainder_cap_partition"])

    # For each cyclic five-set cut C_t={6,7,t}, the direct matching has one
    # crossing (the edge from t to O); it lies in T1, the sector annihilated
    # by the universal five-set functional, never in the surviving T3 piece.
    cyclic = []
    for t in TRIANGLE:
        c_shore = CAP + (t,)
        count = matching_crossings(matching, c_shore)
        require(count == 1, (t, count))
        frozen = next(record for record in five_set["cyclic_partitions"]
                      if record["exposed_triangle_vertex"] == t)
        require((frozen["T1_matchings"], frozen["T3_matchings"],
                 frozen["T3_killed_by_L_triangle"],
                 frozen["T3_surviving_on_opposite_edge"])
                == (45, 60, 54, 6), frozen)
        cyclic.append({
            "exposed_triangle_vertex": t,
            "C_shore": list(c_shore),
            "W_five_set": frozen["five_set"],
            "matching_crossings": count,
            "sector": "T1 (annihilated by the five-set functional)",
        })

    # Provenance: the canonical branch contains this label exactly as one of
    # its 6,558 raw X5 rows.  The membership portion of the manifest contains
    # no word-row label at all, so membership is not the source of this row.
    require(WORD_LABEL not in upstream["source_words"], upstream["source_words"])
    require(upstream["all_word_scan"]["modular_cheapest_word"] == WORD_LABEL,
            upstream["all_word_scan"])
    require(upstream["all_word_scan"]["modular_cheapest_word_crossings"] == 1,
            upstream["all_word_scan"])
    require(len(manifest["full_X5_rows"]) == 6558, len(manifest["full_X5_rows"]))
    require(manifest["full_X5_rows"].count(WORD_LABEL) == 1,
            manifest["full_X5_rows"].count(WORD_LABEL))
    membership_manifest = dict(manifest)
    del membership_manifest["full_X5_rows"]
    require(WORD_LABEL not in json.dumps(membership_manifest, sort_keys=True),
            "word label unexpectedly appears outside full_X5_rows")
    require(set(manifest["blocker_right_sides"]) == {
        "triangle_endpoint_colour", "cap_endpoint_colour", "third_colour", "direct"
    }, manifest["blocker_right_sides"])

    literal_row = [literal_term(matching_term(WORD, matching)) for matching in PM8]
    translated_row = [
        literal_term(MULTIPLIER + matching_term(WORD, matching))
        for matching in PM8
    ]
    require(len({item["monomial"] for item in literal_row}) == 105,
            "literal row collided")
    require(len({item["monomial"] for item in translated_row}) == 105,
            "translated row collided")

    # A one-cell colour mutation is a hostile control: the physical graph is
    # unchanged but the joint colour-pair histogram changes and the crossing
    # pairing disappears.
    mutated_multiplier = MULTIPLIER[:-1] + ((5, 6, 1, 1),)
    mutated_translation = semigroup_key(mutated_multiplier)
    mutated_pairing = sum(
        coefficient * dual.get(key_add(mutated_translation, term), 0)
        for term, coefficient in generator.items()
    )
    require(mutated_pairing == 0, mutated_pairing)

    result = {
        "status": "PASS exact 00202112 crossing and triangle provenance audit",
        "pins": {
            "exact_full62_separator_sha256": separator_hash,
            "full62_terminal_upstream_sha256": upstream_hash,
            "canonical_triangle_manifest_sha256": manifest_hash,
            "triangle_crossword_sha256": crossword_hash,
            "triangle_five_set_sha256": five_set_hash,
        },
        "canonical_flag": {"cap_pair": list(CAP), "triangle": list(TRIANGLE),
                           "outside": list(OUTSIDE)},
        "word": WORD_LABEL,
        "word_profile": {
            "triangle_012": WORD_LABEL[0:3],
            "outside_345": WORD_LABEL[3:6],
            "cap_67": WORD_LABEL[6:8],
        },
        "literal_X5_row": {
            "equation": f"F_{WORD_LABEL}=sum_(M in PM8) prod_(uv in M) A_uv[w_u,w_v]=0",
            "term_count": len(literal_row),
            "terms": literal_row,
        },
        "literal_multiplier": {
            "degree": len(MULTIPLIER),
            "cells": [list(cell) for cell in MULTIPLIER],
            "monomial": " ".join(variable(cell) for cell in MULTIPLIER),
            "joint_semigroup_translation": list(translation),
        },
        "translated_literal_row": {
            "equation": f"({literal_term(MULTIPLIER)['monomial']}) F_{WORD_LABEL}=0",
            "term_count": len(translated_row),
            "terms": translated_row,
        },
        "separator_crossing": {
            "candidate_translations": 1,
            "nonzero_supported_terms": 1,
            "exact_integer_pairing": 1,
            "identity": f"lambda(pi(m F_{WORD_LABEL}))=1",
            "crossing": crossing,
        },
        "triangle_sector": {
            "classification": "direct A_67 with a T-to-O bijection",
            "direct_shape_count": len(direct_shapes),
            "frozen_cramer_remainder_counts": {"direct_A67": 6,
                                                "internal_triangle_response": 18,
                                                "outside_triangle_response": 36},
            "cyclic_five_set_cuts": cyclic,
            "consequence": (
                "The unique separator-visible monomial is one of the six "
                "unresolved direct-A67 shapes.  Every cyclic five-set "
                "contraction places it in T1 and annihilates it."
            ),
        },
        "canonical_branch_provenance": {
            "word_in_full_X5_rows": True,
            "word_index_in_full_X5_rows": manifest["full_X5_rows"].index(WORD_LABEL),
            "word_in_full62_generators": False,
            "four_blocker_cases": manifest["blocker_right_sides"],
            "membership_constructor": manifest["membership_equation_constructor"],
            "word_label_absent_outside_full_X5_manifest_field": True,
        },
        "hostile_colour_mutation": {
            "changed_cell": {"from": [5, 6, 1, 2], "to": [5, 6, 1, 1]},
            "mutated_exact_separator_pairing": mutated_pairing,
        },
        "verdict": (
            "Adjoining F_00202112 to full62 uses X5 directly.  Triangle "
            "geometry recognizes its sole crossing as one of the six "
            "direct-A67 remainder shapes, but the frozen membership/five-set "
            "identities do not supply that row: five-set contraction kills "
            "this T1 sector before its triangle identity is formed."
        ),
        "scope_guard": (
            "This is an exact source/provenance and contraction-sector audit, "
            "not a proof that F_00202112 is algebraically independent of the "
            "triangle-membership ideal after arbitrary polynomial multipliers."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(logical.encode()).hexdigest()
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LOGICAL_SHA256, (digest, EXPECTED_LOGICAL_SHA256))
    result["logical_sha256"] = digest
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered)
    if args.check_results:
        require(OUT.read_text() == rendered, "stored result changed")
    print(result["status"])
    print(result["separator_crossing"]["identity"])
    print(result["triangle_sector"]["classification"])
    print(result["verdict"])
    print("logical sha256", result["logical_sha256"])


if __name__ == "__main__":
    main()
