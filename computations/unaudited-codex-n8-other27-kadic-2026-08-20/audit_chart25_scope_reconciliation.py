#!/usr/bin/env python3
"""Reconcile the legacy-chart25 four-row dual with the anchor K-adic scan.

The old dual uses K_36, the ideal outside a 36-coordinate carrier.  The new
scan uses K_12, the ideal outside only the twelve selected pure anchors.  This
checker transports the old actual-row functional to the new representative,
replays the new K_12^5 certificate with an independent raw hafnian engine,
and audits the old dual on the K_12 degree-five/six ladder.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SCAN_RESULTS = HERE / "results_k5_probe.json"
RAW_ORBITS = (
    HERE.parent / "unaudited-codex-x4-quotient-eliminator-2026-08-20"
    / "results.json"
)
OLD_DUAL_PATH = ROOT / "computations/verify_n8_chart25_degree4_exact_dual.py"
OLD_BASE_PATH = ROOT / "computations/analyze_n8_chart25_degree2_lift.py"

N = 8
COLORS = range(3)
EDGES = tuple(combinations(range(N), 2))
CELLS = tuple((u, v, a, b) for u, v in EDGES
              for a in COLORS for b in COLORS)
CELL_ID = {cell: index for index, cell in enumerate(CELLS)}
NAME_ID = {f"x{u}{v}_{a}{b}": index
           for index, (u, v, a, b) in enumerate(CELLS)}
EXPECTED_NEW_TO_OLD = (
    (0, 2, 3, 1, 4, 6, 7, 5),
    (1, 2, 0),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


OLD = load_module("codex_old_chart25_exact_dual", OLD_DUAL_PATH)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(N)))
require(len(PM8) == 105, "raw perfect-matching census changed")


def transform_cell(cell, site_permutation, color_permutation):
    u, v, a, b = cell
    new_u, new_v = site_permutation[u], site_permutation[v]
    new_a, new_b = color_permutation[a], color_permutation[b]
    if new_u < new_v:
        return new_u, new_v, new_a, new_b
    return new_v, new_u, new_b, new_a


def raw_zero24_anchors():
    payload = json.loads(RAW_ORBITS.read_text())
    record, = (item for item in payload["pure_matching_orbits"]["records"]
               if item["orbit"] == 24)
    triple = tuple(tuple(tuple(edge) for edge in matching)
                   for matching in record["representative"])
    anchors = frozenset(
        CELL_ID[u, v, color, color]
        for color, matching in enumerate(triple) for u, v in matching
    )
    require(len(anchors) == 12, "zero24 lost a selected anchor")
    return triple, anchors


def find_relabeling(new_anchor_cells, old_anchor_cells):
    for color_permutation in permutations(range(3)):
        for site_permutation in permutations(range(8)):
            image = {
                transform_cell(cell, site_permutation, color_permutation)
                for cell in new_anchor_cells
            }
            if image == old_anchor_cells:
                answer = site_permutation, color_permutation
                require(answer == EXPECTED_NEW_TO_OLD,
                        ("first exact relabeling changed", answer))
                return answer
    raise RuntimeError("zero24 and legacy25 supports are not relabelings")


def term_ids(word, matching):
    return bytes(sorted(
        CELL_ID[u, v, word[u], word[v]] for u, v in matching
    ))


@lru_cache(maxsize=None)
def word_terms(word):
    return tuple(term_ids(word, matching) for matching in PM8)


@lru_cache(maxsize=None)
def column_rows(column):
    word, multiplier = column
    return tuple(bytes(sorted(multiplier + term)) for term in word_terms(word))


@lru_cache(maxsize=None)
def incident_columns(row):
    decoded = tuple(CELLS[index] for index in row)
    answer = set()
    for selected in combinations(range(12), 4):
        word = [None] * 8
        vertices = []
        for index in selected:
            u, v, a, b = decoded[index]
            vertices.extend((u, v))
            word[u], word[v] = a, b
        if len(set(vertices)) != 8 or len(set(word)) == 1:
            continue
        selected_set = frozenset(selected)
        multiplier = bytes(row[index] for index in range(12)
                           if index not in selected_set)
        answer.add((tuple(word), multiplier))
    return tuple(sorted(answer, key=repr))


def row_degree(row, anchors):
    return sum(index not in anchors for index in row)


def pure_product_coefficient(row):
    groups = [[] for _ in COLORS]
    for index in row:
        _u, _v, a, b = CELLS[index]
        if a != b:
            return 0
        groups[a].append(index)
    value = 1
    for color in COLORS:
        value *= Counter(word_terms((color,) * 8))[bytes(sorted(groups[color]))]
    return value


def filtered_target(anchors, cutoff):
    groups = []
    for color in COLORS:
        by_degree = {}
        for term in word_terms((color,) * 8):
            degree = row_degree(term, anchors)
            if degree < cutoff:
                by_degree.setdefault(degree, []).append(term)
        groups.append(by_degree)
    target = Counter()
    for degrees in product(range(cutoff), repeat=3):
        if sum(degrees) >= cutoff:
            continue
        for terms in product(*(groups[color].get(degrees[color], ())
                               for color in COLORS)):
            target[bytes(sorted(b"".join(terms)))] += 1
    return target


def add_scaled(target, source, scale):
    for row, value in source.items():
        new = target.get(row, Fraction(0)) + scale * value
        if new:
            target[row] = new
        else:
            target.pop(row, None)


def transported_old_functional(old_to_new):
    expanded_old = {}
    for representative, value in OLD.FUNCTIONAL.items():
        orbit = {
            bytes(sorted(transform[index] for index in representative))
            for transform in OLD.BASE.TRANSFORMS
        }
        for row in orbit:
            require(row not in expanded_old, "old dual row orbits overlap")
            expanded_old[row] = Fraction(value, len(orbit))
    require(len(expanded_old) == 20, "old exact dual no longer expands to 20 rows")
    return {
        bytes(sorted(old_to_new[index] for index in row)): value
        for row, value in expanded_old.items()
    }


def decode_new_certificate():
    payload = json.loads(SCAN_RESULTS.read_text())
    record, = (item for item in payload["records"]
               if item["chart"] == 24 and item["cutoff"] == 5)
    certificate = []
    for item in record["exact_membership"]["exact_certificate"]:
        certificate.append((
            Fraction(item["coefficient"]),
            (tuple(map(int, item["word"])),
             bytes(sorted(NAME_ID[name] for name in item["multiplier"]))),
        ))
    require(len(certificate) == 2222,
            "new legacy25 K_anchor^5 certificate changed")
    return certificate


def audit():
    require(tuple(OLD.BASE.COORDINATES) == CELLS,
            "old and new coordinate byte order differs")
    triple, anchors = raw_zero24_anchors()
    old_support_cells = set(OLD.BASE.FULL.SUPPORT_SET)
    relabeling = find_relabeling(
        {CELLS[index] for index in anchors}, old_support_cells
    )
    site_permutation, color_permutation = relabeling
    new_to_old = tuple(
        CELL_ID[transform_cell(cell, site_permutation, color_permutation)]
        for cell in CELLS
    )
    old_to_new = [None] * len(CELLS)
    for new, old in enumerate(new_to_old):
        old_to_new[old] = new
    old_to_new = tuple(old_to_new)
    transported_support = frozenset(
        old_to_new[OLD.BASE.COORDINATE_ID[cell]] for cell in old_support_cells
    )
    require(transported_support == anchors,
            "transported legacy25 support is not zero24's anchor set")
    transported_allowed = frozenset(
        old_to_new[index] for index in OLD.BASE.ALLOWED_IDS
    )
    require(len(transported_allowed) == 36
            and anchors < transported_allowed
            and len(transported_allowed - anchors) == 24,
            "old 36-coordinate carrier did not transport exactly")

    quotient_old_degrees = tuple(sorted(
        sum(index not in OLD.BASE.ALLOWED_IDS for index in row)
        for row in OLD.FUNCTIONAL
    ))
    quotient_anchor_degrees = tuple(sorted(
        sum(old_to_new[index] not in anchors for index in row)
        for row in OLD.FUNCTIONAL
    ))
    require(quotient_old_degrees == (2, 2, 2, 4), quotient_old_degrees)
    require(quotient_anchor_degrees == (5, 6, 6, 6),
            quotient_anchor_degrees)

    functional = transported_old_functional(old_to_new)
    expanded_old_histogram = Counter(
        sum(index not in transported_allowed for index in row)
        for row in functional
    )
    expanded_anchor_histogram = Counter(
        row_degree(row, anchors) for row in functional
    )
    require(expanded_old_histogram == {2: 16, 4: 4},
            expanded_old_histogram)
    require(expanded_anchor_histogram == {5: 8, 6: 12},
            expanded_anchor_histogram)

    certificate = decode_new_certificate()
    target5 = filtered_target(anchors, 5)
    replay5 = {}
    full_column_violations = []
    full_certificate_pairing = Fraction(0)
    for position, (coefficient, column) in enumerate(certificate):
        outputs = column_rows(column)
        add_scaled(
            replay5,
            Counter(row for row in outputs if row_degree(row, anchors) < 5),
            coefficient,
        )
        pairing = sum((functional.get(row, Fraction(0)) for row in outputs),
                      Fraction(0))
        if pairing:
            minimum_old_degree = min(
                sum(index not in transported_allowed for index in row)
                for row in outputs
            )
            full_column_violations.append(
                (position, pairing, minimum_old_degree)
            )
            full_certificate_pairing += coefficient * pairing
    expected5 = {row: Fraction(value) for row, value in target5.items()}
    require(replay5 == expected5,
            "independent raw engine rejected the 2,222-term K_anchor^5 replay")
    require(len(full_column_violations) == 4
            and Counter(item[2] for item in full_column_violations) == {0: 4}
            and full_certificate_pairing == Fraction(-3, 4),
            ("old cochain/new certificate lower-column pairing changed",
             len(full_column_violations), full_certificate_pairing))
    require(not set(functional).intersection(target5),
            "old functional unexpectedly survives below K_anchor degree five")

    cutoff_ledgers = {}
    for cutoff in (5, 6, 7):
        restricted = {
            row: value for row, value in functional.items()
            if row_degree(row, anchors) < cutoff
        }
        columns = set().union(*(incident_columns(row) for row in restricted)) \
            if restricted else set()
        violations = []
        for column in sorted(columns, key=repr):
            outputs = column_rows(column)
            pairing = sum((restricted.get(row, Fraction(0))
                           for row in outputs), Fraction(0))
            if pairing:
                minimum_old_degree = min(
                    sum(index not in transported_allowed for index in row)
                    for row in outputs
                )
                violations.append((column, pairing, minimum_old_degree))
        target_pairing = sum(
            value * pure_product_coefficient(row)
            for row, value in restricted.items()
        )
        cutoff_ledgers[str(cutoff)] = {
            "functional_rows": len(restricted),
            "incident_raw_columns": len(columns),
            "source_column_violations": len(violations),
            "violation_minimum_K_old_histogram": dict(sorted(Counter(
                minimum for _column, _pairing, minimum in violations
            ).items())),
            "violations_on_minimum_K_old_at_least_2": sum(
                minimum >= 2 for _column, _pairing, minimum in violations
            ),
            "target_pairing": str(target_pairing),
            "first_violation_pairing": (
                str(violations[0][1]) if violations else None
            ),
        }
    require(cutoff_ledgers["5"] == {
        "functional_rows": 0,
        "incident_raw_columns": 0,
        "source_column_violations": 0,
        "violation_minimum_K_old_histogram": {},
        "violations_on_minimum_K_old_at_least_2": 0,
        "target_pairing": "0",
        "first_violation_pairing": None,
    }, cutoff_ledgers["5"])
    require(cutoff_ledgers["6"]["functional_rows"] == 8
            and cutoff_ledgers["6"]["source_column_violations"] > 0,
            "degree-five fragment unexpectedly became a dual")
    require(cutoff_ledgers["7"]["functional_rows"] == 20
            and cutoff_ledgers["7"]["source_column_violations"] == 52
            and cutoff_ledgers["7"]["violation_minimum_K_old_histogram"]
            == {0: 52}
            and cutoff_ledgers["7"]["violations_on_minimum_K_old_at_least_2"] == 0
            and cutoff_ledgers["7"]["target_pairing"] == "-1",
            "full old cochain K_anchor^7 scope calibration changed")

    ledger = {
        "status": "EXACT SCOPE RECONCILIATION PASS",
        "raw_zero24_representative": [[list(edge) for edge in matching]
                                       for matching in triple],
        "new_anchor_ids": sorted(anchors),
        "old_support_ids_before_transport": sorted(
            OLD.BASE.COORDINATE_ID[cell] for cell in old_support_cells
        ),
        "new_to_old_relabeling": {
            "site_permutation": list(site_permutation),
            "color_permutation": list(color_permutation),
        },
        "transported_support_equals_new_anchors": True,
        "K_old_allowed_coordinates": len(transported_allowed),
        "K_anchor_allowed_coordinates": len(anchors),
        "carrier_extras_regraded_into_K_anchor": 24,
        "quotient_row_degrees_K_old": list(quotient_old_degrees),
        "quotient_row_degrees_K_anchor": list(quotient_anchor_degrees),
        "expanded_row_degree_histogram_K_old": dict(sorted(
            expanded_old_histogram.items()
        )),
        "expanded_row_degree_histogram_K_anchor": dict(sorted(
            expanded_anchor_histogram.items()
        )),
        "new_K_anchor5_certificate_terms": len(certificate),
        "new_K_anchor5_independent_exact_replay": True,
        "new_certificate_old_cochain_column_violations": len(
            full_column_violations
        ),
        "new_certificate_violation_minimum_K_old_histogram": dict(sorted(
            Counter(item[2] for item in full_column_violations).items()
        )),
        "new_certificate_full_old_cochain_pairing": str(
            full_certificate_pairing
        ),
        "new_certificate_truncated_K_anchor5_cochain_pairing": "0",
        "anchor_ladder": cutoff_ledgers,
        "verdict": (
            "No contradiction: K_old is outside 36 coordinates, whereas "
            "K_anchor is outside 12. The old four-row functional is zero "
            "modulo K_anchor^5; its degree-five fragment is not a dual "
            "modulo K_anchor^6. Even with all degree-five/six rows, 52 "
            "minimum-K_old-zero columns hit the cochain, so it is not a "
            "K_anchor^7 dual without reconstructing the full Schur lift."
        ),
        "source_pins": {
            str(OLD_DUAL_PATH.relative_to(ROOT)): sha256(
                OLD_DUAL_PATH.read_bytes()).hexdigest(),
            str(OLD_BASE_PATH.relative_to(ROOT)): sha256(
                OLD_BASE_PATH.read_bytes()).hexdigest(),
            str(RAW_ORBITS.relative_to(ROOT)): sha256(
                RAW_ORBITS.read_bytes()).hexdigest(),
            str(SCAN_RESULTS.relative_to(ROOT)): sha256(
                SCAN_RESULTS.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    ledger["sha256"] = sha256(encoded.encode()).hexdigest()
    return ledger


def main():
    ledger = audit()
    (HERE / "chart25_scope_reconciliation.json").write_text(
        json.dumps(ledger, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "status": ledger["status"],
        "K_old_degrees": ledger["quotient_row_degrees_K_old"],
        "K_anchor_degrees": ledger["quotient_row_degrees_K_anchor"],
        "anchor_ladder": ledger["anchor_ladder"],
        "sha256": ledger["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
