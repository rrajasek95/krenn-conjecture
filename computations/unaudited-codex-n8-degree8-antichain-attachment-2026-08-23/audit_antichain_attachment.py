#!/usr/bin/env python3
"""Apply the frozen 34-column correction as an exact cochain attachment.

The coefficients frozen by the antichain-cell package are degree-eight row
weights.  Thus the honest operation is extension of the pure-target dual
cochain, followed by computation of its new coboundary on source columns.
This checker exports that complete bounded boundary and guards against the
incorrect interpretation as primal source-column coefficients.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from time import monotonic

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKET_DIR = ROOT / "computations/unaudited-codex-n8-degree8-antichain-cells-2026-08-23"
PACKET_SCRIPT = PACKET_DIR / "audit_degree8_antichain_cells.py"
PACKET_RESULT = PACKET_DIR / "results_degree8_antichain_cells.json"
OUT = HERE / "results_antichain_attachment.json"
EXPECTED_PACKET_LOGICAL = "4b33611aa61c89ea34de63a4a07b002d0dfde8c7960151a88d888efb305edea2"
Q = Fraction


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def fraction_record(value):
    value = Q(value)
    return [value.numerator, value.denominator]


def histogram(values):
    counter = Counter(values)
    return {str(key): value for key, value in sorted(counter.items(), key=lambda x: str(x[0]))}


def fh_coefficient_function(M):
    """Coefficient oracle for the literal normalized F^h at total degree 12."""
    pure_terms = tuple(tuple(sorted(
        M.normalized_generator(M.D5.word_code((colour,) * 8)).items(),
        key=lambda item: (len(item[0]), item[0])
    )) for colour in range(3))

    def quotient_if_divides(target, factor):
        answer = bytearray()
        left = right = 0
        while left < len(target) and right < len(factor):
            if target[left] < factor[right]:
                answer.append(target[left])
                left += 1
            elif target[left] == factor[right]:
                left += 1
                right += 1
            else:
                return None
        if right != len(factor):
            return None
        answer.extend(target[left:])
        return bytes(answer)

    @lru_cache(None)
    def coefficient(row, colours=(0, 1, 2)):
        if not colours:
            return int(not row)
        total = 0
        for term, value in pure_terms[colours[0]]:
            if len(term) > len(row):
                break
            quotient = quotient_if_divides(row, term)
            if quotient is not None:
                total += value * coefficient(quotient, colours[1:])
        return total

    return coefficient


def run(mutate=False):
    started = monotonic()
    frozen = json.loads(PACKET_RESULT.read_text(encoding="utf-8"))
    require(frozen["logical_sha256"] == EXPECTED_PACKET_LOGICAL,
            "frozen 34-column package digest changed")

    P = load("antichain_packet", PACKET_SCRIPT)
    A = load("attachment_prolong", P.PROLONG)
    D = load("attachment_extend", P.EXTEND)
    W = load("attachment_weighted", P.WEIGHTED)
    M = A.load_checker()

    target, first_functional, old_boundary, cache = P.exact_extended_functional(A, M)
    antichain = P.decode_columns(M)
    require(len(old_boundary) == 252 and len(antichain) == 34,
            "attachment input boundary changed")

    leaf_correction, hard, _leaf_records = P.private_leaf_packet(
        A, M, antichain, first_functional, cache
    )
    after_leaves = dict(first_functional)
    for row, value in leaf_correction.items():
        after_leaves[row] = after_leaves.get(row, Q(0)) + value
        if not after_leaves[row]:
            after_leaves.pop(row)
    rounds, hard_correction, hard_columns = P.hard_cell_closure(
        A, D, M, hard, after_leaves, cache, started
    )

    attached = dict(after_leaves)
    for row, value in hard_correction.items():
        attached[row] = attached.get(row, Q(0)) + value
        if not attached[row]:
            attached.pop(row)
    require(A.pairing(attached, target) == -1 and attached.get(b"") == 1,
            "attachment changed the normalized pure-target pairing")

    coefficient_fh = fh_coefficient_function(M)
    fh_pairing_before = sum(value * coefficient_fh(row)
                            for row, value in first_functional.items())
    fh_pairing_after = sum(value * coefficient_fh(row)
                           for row, value in attached.items())
    correction_fh_pairing = fh_pairing_after - fh_pairing_before
    require(fh_pairing_before == fh_pairing_after == 1
            and correction_fh_pairing == 0,
            "t^4-shifted attachment changed its literal F^h pairing")

    incident = M.bounded_incident_columns(attached, 8)
    boundary = {}
    for column in incident:
        value = A.pairing(attached, A.column_entries(M, column, cache))
        if value:
            boundary[column] = value

    # Every correction row was closed against all of its incident columns,
    # so attachment cannot create a new exterior column at this degree.
    require(set(boundary) <= old_boundary,
            "34-column attachment created a new degree-eight boundary column")
    require(not (set(boundary) & antichain),
            "34-column attachment left an antichain crossing")

    indices = P.lower_indices(W)
    degree5_witnesses = {
        column: P.cell_incidence(A, M, W, indices, column, "d5")
        for column in boundary
    }
    require(all(degree5_witnesses.values()),
            "post-attachment boundary exposed a non-degree5 cell")

    killed_old = old_boundary - set(boundary)
    require(antichain <= killed_old, "attachment did not kill the whole antichain")
    if mutate:
        require(set(boundary) & antichain,
                "hostile surviving-antichain mutation survived")

    target_record = [
        [row.hex(), *fraction_record(value)]
        for row, value in sorted(target.items())
    ]
    boundary_records = []
    for column, value in sorted(boundary.items()):
        record = P.column_record(A, M, column)
        record.update({
            "pairing": fraction_record(value),
            "degree5_source_legs": len(degree5_witnesses[column]),
            "multiplier_skeleton": W.skeleton_type(column[1]),
            "top_skeleton": W.skeleton_type(W.FIRST.multiply(
                column[1], indices["code_to_lead"][column[0]]
            )),
        })
        boundary_records.append(record)

    correction_record = [
        [row.hex(), *fraction_record(value), "leaf"]
        for row, value in sorted(leaf_correction.items())
    ] + [
        [row.hex(), *fraction_record(value), "hard11"]
        for row, value in sorted(hard_correction.items())
    ]
    correction_record.sort()

    result = {
        "verdict": "PASS_FH_Y8_T4_34_COLUMN_COCHAIN_ATTACHMENT;POST_BOUNDARY_IS_DEGREE5_EXCHANGE_SUPPORTED",
        "scope": (
            "exact degree-eight coboundary of the normalized pure-target dual "
            "after the frozen local 34-column attachment; no claim at degree "
            "nine and no contraction of the remaining exchange boundary"
        ),
        "variance_guard": {
            "operation": "dual cochain extension by degree-eight row weights",
            "not_proved": "a primal source-column chain correction of F^h",
            "reason": (
                "the frozen 23+43 coefficients index output rows, whereas a "
                "primal correction would require coefficients indexing mixed-generator columns"
            ),
        },
        "frozen_packet": {
            "logical_sha256": EXPECTED_PACKET_LOGICAL,
            "result_file_sha256": hashlib.sha256(PACKET_RESULT.read_bytes()).hexdigest(),
        },
        "pure_target_residual": {
            "support": len(target),
            "pairing_before": fraction_record(A.pairing(first_functional, target)),
            "pairing_after": fraction_record(A.pairing(attached, target)),
            "constant_pairing_after": fraction_record(attached.get(b"", 0)),
            "sha256": hashlib.sha256(json.dumps(
                target_record, separators=(",", ":")
            ).encode()).hexdigest(),
            "rows": target_record,
        },
        "literal_Fh_degree12_shift": {
            "operation": "multiply the complete degree-eight cochain and source columns by t^4",
            "total_degree": 12,
            "top_bidegree": "y^8 t^4",
            "Fh_pairing_before": fraction_record(fh_pairing_before),
            "Fh_pairing_after": fraction_record(fh_pairing_after),
            "attachment_only_Fh_pairing": fraction_record(correction_fh_pairing),
            "interpretation": (
                "the attachment is a literal target-preserving cochain map in "
                "the y8/t4 layer of the actual homogeneous pure target"
            ),
            "scope_guard": (
                "this lies in the independently reported acyclic y-degree<=9 "
                "region and does not touch the first y10/t2 quadratic core"
            ),
        },
        "attachment": {
            "leaf_rows": len(leaf_correction),
            "hard_rows": len(hard_correction),
            "total_row_weights": len(correction_record),
            "row_weights": correction_record,
            "hard_rounds": rounds,
            "hard_incident_columns": len(hard_columns),
        },
        "degree8_boundary": {
            "before_columns": len(old_boundary),
            "after_columns": len(boundary),
            "killed_old_columns": len(killed_old),
            "killed_antichain_columns": len(antichain),
            "new_exterior_columns": len(set(boundary) - old_boundary),
            "pairing_histogram": histogram(boundary.values()),
            "word_profile_histogram": histogram(
                A.word_profile(M, column[0]) for column in boundary
            ),
            "degree5_source_leg_histogram": histogram(
                len(witnesses) for witnesses in degree5_witnesses.values()
            ),
            "all_survivors_have_degree5_source_legs": True,
            "first_genuinely_new_cell": None,
            "columns": boundary_records,
        },
        "attachment_lemma": (
            "After multiplication by t^4, the 66-row invariant cochain "
            "attachment preserves literal F^h pairing one, kills the complete "
            "34-column complement and creates no new degree-eight crossing. "
            "Its remaining coboundary is supported entirely on translated "
            "legs of the frozen complete degree-five Buchberger cells."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = run(args.mutate)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered, encoding="utf-8")
    if args.check_results:
        require(OUT.read_text(encoding="utf-8") == rendered,
                "frozen attachment result changed")
    print(json.dumps({
        "verdict": result["verdict"],
        "before_after": [
            result["degree8_boundary"]["before_columns"],
            result["degree8_boundary"]["after_columns"],
        ],
        "killed_old": result["degree8_boundary"]["killed_old_columns"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
