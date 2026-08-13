#!/usr/bin/env python3
"""Locate the first E14 landing obstruction under silent-chord specialization.

The canonical word-000101 unary-times-q remainder has twelve terms.  This
checker reconstructs its complete 269-column unary/G11 first-hit module and
the pinned 22-support rational cokernel functional.  It proves two facts.

* The functional's entire pairing with the twelve-term target is carried by
  the single companion ``u05_01*v13_01*v24_11``.  The already identified
  decorated rootless core ``u05_01*v24_11*v34_10`` pairs to zero.
* Killing the whole missing chord q13 does not put the target in the old
  image.  Instead the obstruction moves to nine pure unary-target readout
  coordinates.  Killing both missing chords q04 and q13 leaves eight such
  coordinates.

Thus the first missing endpoint-word-change cell must include the target-
normal face; neither the decorated-core occurrence nor silent-chord
specialization alone supplies the physical E14 landing.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIRST = "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py"
PINS = {
    FIRST:
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
    "computations/verify_h3_relative_occurrence_e14_w_carrier_landing_gate.py":
        "37f571234346c8a90465a5e021bb5ed97b0caec68e31a8b80346d25f94c9f337",
    "notes/h3-relative-occurrence-e14-w-carrier-landing-gate.md":
        "a4a0e1be3cff6779f3641f6c3f1faa6431eac01b85a4cdf1bfbfc9d595d56888",
}
EXPECTED_LEDGER_SHA256 = (
    "0d66bbe5d6652511d98c3db1ed6f50872a02e228ac7d7347e01b9731588c489b"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path, name):
    spec = spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def reconstruct():
    first = load(FIRST, "e14_companion_first")
    first_ledger, first_digest = first.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256,
            "the first-hit dependency ledger changed")

    rewrite = first.load(first.REWRITE_PATH, "e14_companion_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "e14_companion_top")
    two = top.load(top.TWO_CELL_PATH, "e14_companion_two")
    e14 = two.load(two.E14_PATH, "e14_companion_base")
    b4 = e14.load(e14.B4_PATH, "e14_companion_b4")
    _candidates, _names, responses, unary = two.universal(e14, b4, 1, 1)

    endpoint = ("p1_0_1", "s1_1_1")
    pivot = ("u35_11",)
    multiplier = ("v2411",)
    word = (0, 0, 0, 1, 0, 1)
    factor, remainder = first.factor_unary(unary[word], pivot)
    require(factor == {(): Q(-1), ("v0400",): Q(1)}
            and len(remainder) == 12,
            "the canonical unary factor/remainder changed")
    target = {
        (endpoint, first.multiply_monomials(monomial, multiplier)): coefficient
        for monomial, coefficient in remainder.items()
    }

    response_rows = [
        (output_word, first.response_terms(row))
        for output_word, row in responses.items()
    ]
    unary_rows = [
        (output_word, tuple(polynomial.items()))
        for output_word, polynomial in unary.items()
    ]
    columns = {}
    for target_endpoint, target_monomial in target:
        for row_index, (output_word, row) in enumerate(response_rows):
            for row_endpoint, row_monomial, _coefficient in row:
                if row_endpoint != target_endpoint:
                    continue
                row_multiplier = first.quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                column = {
                    (output_endpoint,
                     first.multiply_monomials(output_monomial,
                                              row_multiplier)):
                        output_coefficient
                    for output_endpoint, output_monomial, output_coefficient
                    in row
                }
                if output_word == (1,) * 6:
                    column[(("target_G11",), row_multiplier)] = Q(-1)
                columns[("G11", row_index, row_multiplier)] = column
        for row_index, (output_word, row) in enumerate(unary_rows):
            for row_monomial, _coefficient in row:
                row_multiplier = first.quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                column = {
                    (target_endpoint,
                     first.multiply_monomials(output_monomial,
                                              row_multiplier)):
                        output_coefficient
                    for output_monomial, output_coefficient in row
                }
                if output_word == (0,) * 6:
                    column[(("target_unary",) + target_endpoint,
                            row_multiplier)] = Q(-1)
                columns[("unary", row_index, target_endpoint,
                         row_multiplier)] = column
    require(len(columns) == 269, "the first-hit column count changed")
    return first, first_ledger, endpoint, target, columns


def rational_dual(first, target, columns):
    pivots = {}
    for column in columns.values():
        first.add_exact_column(column, pivots)
    require(len(pivots) == 269, "the first-hit rank changed")
    reduced = first.exact_reduce(target, pivots)
    free = min(reduced)
    dual = {free: Q(1)}
    for leading in sorted(pivots, reverse=True):
        value = sum(
            coefficient * dual.get(coordinate, Q(0))
            for coordinate, coefficient in pivots[leading].items()
            if coordinate != leading
        )
        if value:
            dual[leading] = -value
    require(len(dual) == 22, "the first-hit dual support changed")
    require(all(sum(coefficient * dual.get(coordinate, Q(0))
                    for coordinate, coefficient in column.items()) == 0
                for column in columns.values()),
            "the first-hit dual stopped killing an old column")
    return pivots, dual


def set_edge_zero(vector, edge_prefixes):
    answer = defaultdict(Q)
    for (grade, monomial), coefficient in vector.items():
        if any(any(variable.startswith(prefix) for prefix in edge_prefixes)
               for variable in monomial):
            continue
        answer[(grade, monomial)] += coefficient
    return {coordinate: coefficient
            for coordinate, coefficient in answer.items() if coefficient}


def specialize(first, target, columns, prefixes):
    pivots = {}
    for column in columns.values():
        first.add_exact_column(set_edge_zero(column, prefixes), pivots)
    specialized_target = set_edge_zero(target, prefixes)
    reduced = first.exact_reduce(specialized_target, pivots)
    target_grade = ("target_unary", "p1_0_1", "s1_1_1")
    require(all(coordinate[0] == target_grade for coordinate in reduced),
            "the silent-chord residual left the target-normal summand")
    return {
        "zero_prefixes": list(prefixes),
        "rank_Q": len(pivots),
        "specialized_target_support": len(specialized_target),
        "reduced_support": len(reduced),
        "all_reduced_coordinates_are_unary_target_normal": True,
        "reduced": [
            [list(coordinate[1]), str(coefficient)]
            for coordinate, coefficient in sorted(reduced.items())
        ],
    }


def audit():
    pin_dependencies()
    first, first_ledger, endpoint, target, columns = reconstruct()
    _pivots, dual = rational_dual(first, target, columns)

    contributions = [
        (coordinate, coefficient, dual.get(coordinate, Q(0)),
         coefficient * dual.get(coordinate, Q(0)))
        for coordinate, coefficient in sorted(target.items())
        if coefficient * dual.get(coordinate, Q(0))
    ]
    detected = (endpoint, ("u05_01", "v1301", "v2411"))
    promoted = (endpoint, ("u05_01", "v2411", "v3410"))
    require(contributions == [(detected, Q(-1), Q(1), Q(-1))],
            f"the target pairing stopped being concentrated: {contributions}")
    require(target[promoted] == Q(1) and dual.get(promoted, Q(0)) == 0,
            "the decorated-core comparison changed")

    q13_zero = specialize(first, target, columns, ("v13",))
    both_zero = specialize(first, target, columns, ("v04", "v13"))
    require((q13_zero["rank_Q"], q13_zero["specialized_target_support"],
             q13_zero["reduced_support"]) == (211, 9, 9),
            "the q13-zero specialization changed")
    require((both_zero["rank_Q"], both_zero["specialized_target_support"],
             both_zero["reduced_support"]) == (185, 8, 8),
            "the q04=q13=zero specialization changed")

    ledger = {
        "theorem": "E14 companion / target-normal specialization gate",
        "pins": PINS,
        "canonical_first_hit": {
            "columns": 269,
            "rank_Q": 269,
            "target_support": 12,
            "dual_support": 22,
            "target_pairing": "-1",
            "unique_detected_coordinate": [list(detected[0]),
                                            list(detected[1])],
            "target_coefficient": "-1",
            "dual_coefficient": "1",
            "detected_site_profile": [2, 2, 1, 1, 1, 1, 1, 1],
            "promoted_decorated_core_coordinate": [list(promoted[0]),
                                                    list(promoted[1])],
            "promoted_target_coefficient": "1",
            "promoted_dual_coefficient": "0",
            "promoted_site_profile": [2, 1, 1, 1, 2, 1, 1, 1],
        },
        "silent_chord_specializations": {
            "q13_zero": q13_zero,
            "q04_q13_zero": both_zero,
        },
        "first_physical_requirement": (
            "a source-valid endpoint-word-change/relative P2 cell that "
            "carries the target-normal unary readout face as well as the "
            "occurrence coefficient; the decorated 2K2 core alone has zero "
            "pairing, and silent-chord specialization merely moves the "
            "obstruction into the target-normal summand"
        ),
        "scope": (
            "exact selected word-000101 first-hit module.  The specialized "
            "target-normal coordinates are not by themselves promoted to a "
            "physical terminal; later augmented columns may still fill them"
        ),
        "dependency_ledger": first_ledger["canonical_first_reduction"],
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    return ledger, digest


if __name__ == "__main__":
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            f"ledger changed: {digest}")
    canonical = ledger["canonical_first_hit"]
    print("h3 E14 companion / target-normal specialization: PASS (exact)")
    print("dual-visible target=" + "*".join(
        canonical["unique_detected_coordinate"][1]))
    print("decorated-core dual pairing="
          + canonical["promoted_dual_coefficient"])
    print("q13=0: rank 211, target-normal residual 9")
    print("q04=q13=0: rank 185, target-normal residual 8")
    print("physical endpoint-word-change/target-normal cone: OPEN")
    print(f"ledger_sha256={digest}")
