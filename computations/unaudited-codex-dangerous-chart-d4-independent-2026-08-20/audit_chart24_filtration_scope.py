#!/usr/bin/env python3
"""Resolve the apparent zero24/legacy25 K-adic contradiction exactly.

The certified legacy chart-25 dual uses K36, generated outside its
36-coordinate carrier.  The new other27 scan uses K12, generated outside the
twelve pure anchors.  This checker aligns the raw representatives, transports
the full actual-row dual, replays the new cutoff-five certificate, and audits
the first cutoffs at which the transported dual can be seen by K12.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_ENGINE_PATH = HERE / "audit_d4.py"
OLD_DUAL_PATH = ROOT / "verify_n8_chart25_degree4_exact_dual.py"
UPSTREAM_PATH = (
    ROOT / "unaudited-codex-x4-quotient-eliminator-2026-08-20"
    / "results.json"
)
K5_PATH = (
    ROOT / "unaudited-codex-n8-other27-kadic-2026-08-20"
    / "results_k5_probe.json"
)
EXPECTED_UPSTREAM_SHA256 = (
    "7b61e3c5cc2422087ea6d6d2a4e393fdebfd5df88c4e6eb5805f894ab01f8162"
)
EXPECTED_K5_SHA256 = (
    "27531f499696af48a16a0d8a78e7ad79cd195ec489fc237f8ea6eaedb3f053f3"
)
EXPECTED_K5_CERTIFICATE_SHA256 = (
    "34daddc30105f2b4c154c089c04d4e0368a743273bff1f4bcef225f05d6c2c42"
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RAW = load("chart24_scope_raw", RAW_ENGINE_PATH)
OLD = load("chart24_scope_old", OLD_DUAL_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(vector, row, value):
    updated = vector.get(row, Fraction(0)) + Fraction(value)
    if updated:
        vector[row] = updated
    else:
        vector.pop(row, None)


def chart24_matching():
    require(sha256(UPSTREAM_PATH.read_bytes()).hexdigest()
            == EXPECTED_UPSTREAM_SHA256, "raw chart ledger changed")
    records = json.loads(UPSTREAM_PATH.read_text())[
        "pure_matching_orbits"
    ]["records"]
    record = next(record for record in records if record["orbit"] == 24)
    return tuple(tuple(tuple(edge) for edge in matching)
                 for matching in record["representative"])


def old_matching():
    groups = [[] for _ in range(3)]
    for u, v, a, b in OLD.BASE.FULL.SUPPORT_SET:
        require(a == b, "old pure support acquired a mixed cell")
        groups[a].append((u, v))
    return tuple(tuple(sorted(group)) for group in groups)


def representative_alignment(old, new):
    new_sets = tuple(set(matching) for matching in new)
    for colour_permutation in permutations(range(3)):
        for vertex_permutation in permutations(range(8)):
            if all({tuple(sorted((vertex_permutation[u],
                                  vertex_permutation[v])))
                    for u, v in old[colour]}
                   == new_sets[colour_permutation[colour]]
                   for colour in range(3)):
                return vertex_permutation, colour_permutation
    raise RuntimeError("legacy25 and zero24 representatives are not isomorphic")


def transform_cell(cell, vertex_permutation, colour_permutation):
    u, v, a, b = cell
    image_u, image_v = vertex_permutation[u], vertex_permutation[v]
    image_a, image_b = colour_permutation[a], colour_permutation[b]
    if image_u > image_v:
        image_u, image_v = image_v, image_u
        image_a, image_b = image_b, image_a
    return image_u, image_v, image_a, image_b


def transform_row(row, vertex_permutation, colour_permutation):
    return bytes(sorted(
        RAW.CELL_ID[transform_cell(OLD.BASE.COORDINATES[cell],
                                   vertex_permutation, colour_permutation)]
        for cell in row
    ))


def new_anchor_ids(matchings):
    return frozenset(
        RAW.CELL_ID[(u, v, colour, colour)]
        for colour, matching in enumerate(matchings) for u, v in matching
    )


def filtered_target(matchings, cutoff):
    anchors = new_anchor_ids(matchings)
    groups = []
    for colour in range(3):
        by_degree = defaultdict(list)
        for row in RAW.word_terms((colour,) * 8):
            degree = RAW.row_degree(row, anchors)
            if degree < cutoff:
                by_degree[degree].append(row)
        groups.append(by_degree)
    target = Counter()
    for degrees in product(range(cutoff), repeat=3):
        if sum(degrees) >= cutoff:
            continue
        for terms in product(*(groups[colour].get(degrees[colour], ())
                               for colour in range(3))):
            target[bytes(sorted(b"".join(terms)))] += 1
    return target


def pure_product_coefficient(row):
    groups = [[] for _ in range(3)]
    for cell in row:
        _u, _v, a, b = RAW.CELLS[cell]
        if a != b:
            return 0
        groups[a].append(cell)
    answer = 1
    for colour, group in enumerate(groups):
        answer *= Counter(RAW.word_terms((colour,) * 8))[
            bytes(sorted(group))
        ]
    return answer


def decode_k5_certificate():
    require(sha256(K5_PATH.read_bytes()).hexdigest() == EXPECTED_K5_SHA256,
            "other27 K5 result changed")
    records = json.loads(K5_PATH.read_text())["records"]
    record = next(record for record in records
                  if record["chart"] == 24 and record["cutoff"] == 5)
    payload = record["exact_membership"]["exact_certificate"]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    require(sha256(encoded.encode("ascii")).hexdigest()
            == EXPECTED_K5_CERTIFICATE_SHA256,
            "zero24 cutoff-five certificate changed")
    certificate = []
    for item in payload:
        certificate.append((
            Fraction(item["coefficient"]),
            (
                tuple(map(int, item["word"])),
                bytes(sorted(RAW.CELL_NAME_ID[name]
                             for name in item["multiplier"])),
            ),
        ))
    return record, tuple(certificate)


def audit():
    require(tuple(OLD.BASE.COORDINATES) == RAW.CELLS,
            "old and new endpoint-cell orderings differ")
    old = old_matching()
    new = chart24_matching()
    vertex_permutation, colour_permutation = representative_alignment(old, new)
    anchors = new_anchor_ids(new)

    old_support = frozenset(
        RAW.CELL_ID[transform_cell(cell, vertex_permutation,
                                   colour_permutation)]
        for cell in OLD.BASE.FULL.SUPPORT_SET
    )
    old_allowed = frozenset(
        RAW.CELL_ID[transform_cell(OLD.BASE.COORDINATES[cell],
                                   vertex_permutation, colour_permutation)]
        for cell in OLD.BASE.ALLOWED_IDS
    )
    require(old_support == anchors and len(anchors) == 12,
            "aligned old support is not the new twelve-anchor set")
    require(len(old_allowed) == 36 and anchors < old_allowed,
            "old carrier is not twelve anchors plus twenty-four extras")

    canonical_rows = []
    for row, value in OLD.FUNCTIONAL.items():
        transformed = transform_row(row, vertex_permutation,
                                    colour_permutation)
        canonical_rows.append({
            "old_row": row.hex(),
            "new_row": transformed.hex(),
            "value": value,
            "K36_degree": sum(cell not in old_allowed for cell in transformed),
            "K12_degree": RAW.row_degree(transformed, anchors),
        })
    require([item["K36_degree"] for item in canonical_rows] == [2, 2, 2, 4],
            "old four-row K36 degrees changed")
    require([item["K12_degree"] for item in canonical_rows] == [5, 6, 6, 6],
            "transported four-row K12 degrees changed")

    expanded_old, _orbit_sizes = OLD.expanded_functional()
    functional = {
        transform_row(row, vertex_permutation, colour_permutation): value
        for row, value in expanded_old.items()
    }
    require(len(functional) == 20, "transported actual dual lost rows")
    expanded_degree_histogram = Counter(
        RAW.row_degree(row, anchors) for row in functional
    )
    require(expanded_degree_histogram == Counter({6: 12, 5: 8}),
            "transported actual dual K12 degrees changed")

    record, certificate = decode_k5_certificate()
    target5 = filtered_target(new, 5)
    replay5 = Counter()
    full_certificate_pairing = Fraction(0)
    column_pairing_violations = []
    for coefficient, column in certificate:
        one_pairing = Fraction(0)
        for row in RAW.column_rows(column):
            if RAW.row_degree(row, anchors) < 5:
                replay5[row] += coefficient
            one_pairing += functional.get(row, Fraction(0))
        full_certificate_pairing += coefficient * one_pairing
        if one_pairing:
            column_pairing_violations.append((repr(column), str(one_pairing)))
    replay5 = Counter({row: value for row, value in replay5.items() if value})
    require(replay5 == target5, "independent zero24 cutoff-five replay failed")
    require(len(column_pairing_violations) == 4
            and full_certificate_pairing == Fraction(-3, 4),
            "full pairing of the cutoff-five certificate changed")

    full_target_pairing = sum(
        (value * pure_product_coefficient(row)
         for row, value in functional.items()),
        Fraction(0),
    )
    require(full_target_pairing == -1,
            "transported old dual target pairing changed")
    cutoff5_target_pairing = sum(
        (value * target5.get(row, 0) for row, value in functional.items()),
        Fraction(0),
    )
    require(cutoff5_target_pairing == 0,
            "old dual unexpectedly appears below K12 degree five")

    # Support-local cutoff calibration.  The four-row dual was constructed
    # after fixing the degree-zero chart identity.  It annihilates the old
    # min-K36=2 family, not all min-K36=0 source columns, so even restoring all
    # 20 rows at cutoff seven does not by itself produce a K12 dual.
    cutoff_audits = {}
    for cutoff in (6, 7):
        truncated_functional = {
            row: value for row, value in functional.items()
            if RAW.row_degree(row, anchors) < cutoff
        }
        incident = set()
        for row in truncated_functional:
            incident.update(RAW.incident_columns(row))
        violations = []
        for column in sorted(incident, key=repr):
            pairing = sum((truncated_functional.get(row, Fraction(0))
                           for row in RAW.column_rows(column)), Fraction(0))
            if pairing:
                violations.append((column, pairing))
        target_pairing = sum(
            (value * pure_product_coefficient(row)
             for row, value in truncated_functional.items()), Fraction(0)
        )
        cutoff_audits[str(cutoff)] = {
            "functional_rows": len(truncated_functional),
            "incident_source_columns": len(incident),
            "source_pairing_violations": len(violations),
            "source_pairing_violation_histogram": dict(sorted(Counter(
                str(value) for _column, value in violations
            ).items())),
            "target_pairing": str(target_pairing),
            "is_exact_dual": not violations and bool(target_pairing),
        }
    require(not cutoff_audits["6"]["is_exact_dual"]
            and not cutoff_audits["7"]["is_exact_dual"],
            "old affine cochain unexpectedly became a raw K12 dual")

    ledger = {
        "numbering": "zero24 is legacy one-based chart25",
        "old_matching": old,
        "new_matching": new,
        "old_to_new_vertex_permutation": vertex_permutation,
        "old_to_new_colour_permutation": colour_permutation,
        "aligned_anchor_sets_equal": True,
        "K12_anchors": len(anchors),
        "K36_allowed_cells": len(old_allowed),
        "K36_extra_cells": len(old_allowed - anchors),
        "canonical_dual_rows": canonical_rows,
        "expanded_dual_K12_degree_histogram": dict(sorted(
            expanded_degree_histogram.items()
        )),
        "zero24_cutoff5_rows": record["rows"],
        "zero24_cutoff5_columns": record["columns"],
        "zero24_cutoff5_certificate_terms": len(certificate),
        "zero24_cutoff5_exact_replay": True,
        "zero24_cutoff5_target_pairing": str(cutoff5_target_pairing),
        "zero24_full_certificate_pairing": str(full_certificate_pairing),
        "zero24_certificate_columns_nonannihilated": len(
            column_pairing_violations
        ),
        "zero24_full_target_pairing": str(full_target_pairing),
        "full_target_minus_full_certificate_pairing": str(
            full_target_pairing - full_certificate_pairing
        ),
        "cutoff_calibration": cutoff_audits,
        "scope_verdict": (
            "No contradiction: K36=outside36 and K12=outside12 are different. "
            "The old obstruction is invisible modulo K12^5.  Its four-row "
            "affine cochain does not annihilate all min-K36=0 columns, so no "
            "K12^6/K12^7 obstruction follows without a degree-zero Schur lift."
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    payload = {"ledger": ledger, "sha256": digest}
    (HERE / "chart24_filtration_scope.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print("zero24/legacy25 filtration-scope audit: PASS")
    print("canonical K36/K12 degrees:", [
        (item["K36_degree"], item["K12_degree"])
        for item in ledger["canonical_dual_rows"]
    ])
    print("cutoff calibration:", ledger["cutoff_calibration"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
