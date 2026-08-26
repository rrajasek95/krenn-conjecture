#!/usr/bin/env python3
"""Order-three/four formal lift and 728-carrier replay for the ten-cell jet."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit_active_cap_boundary_leading import (  # noqa: E402
    ALL_EDGES, COLOURS, MATCHING, MATCHING_SET, Y_INDEX, Y_LABELS,
    Z_LABELS, activity_rows, base_source, carrier_census, carrier_rows,
    correction_j_rows, perfect_matchings,
)
from audit_13block_environment import dense_rank  # noqa: E402

INVARIANT_RESULTS = HERE / "results_active_boundary_invariant_support.json"
OUT = HERE / "results_ten_cell_formal_lift.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def series_source(candidate_labels, correction=None):
    source = {}
    for edge in MATCHING:
        for colour in COLOURS:
            source.setdefault(edge + (colour, colour), {})[0] = Fraction(1)
    for label in candidate_labels:
        source.setdefault(label, {})[1] = Fraction(1)
    if correction:
        for label, (order, value) in correction.items():
            if value:
                source.setdefault(label, {})[order] = Fraction(value)
    return source


def coefficient_rows(source, target_order):
    """Literal matching expansion of [t^target_order] F(A(t))."""
    edge_cells = {}
    for edge in ALL_EDGES:
        cells = []
        for i in COLOURS:
            for j in COLOURS:
                for order, value in source.get(edge + (i, j), {}).items():
                    if order <= target_order and value:
                        cells.append((i, j, order, value))
        edge_cells[edge] = cells
    rows = Counter()
    raw_terms = 0
    for matching in perfect_matchings(tuple(range(8))):
        choices = [edge_cells[edge] for edge in matching]
        if any(not cells for cells in choices):
            continue
        for selected in product(*choices):
            if sum(item[2] for item in selected) != target_order:
                continue
            word = [None] * 8
            value = Fraction(1)
            for (u, v), (i, j, _, coefficient) in zip(matching, selected):
                word[u], word[v] = i, j
                value *= coefficient
            rows[tuple(word)] += value
            raw_terms += 1
    return {word: value for word, value in rows.items() if value}, raw_terms


def reduce_numeric_rhs(rhs):
    """Row-reduce J*z=-rhs and expose exact cokernel residuals."""
    jrows = correction_j_rows()
    basis = {}
    residuals = []
    provenance = {}
    for word in sorted(set(jrows) | set(rhs)):
        numeric = {index: Fraction(value)
                   for index, value in jrows.get(word, {}).items() if value}
        value = Fraction(rhs.get(word, 0))
        trace = {word: Fraction(1)}
        while numeric:
            pivot = min(numeric)
            if pivot not in basis:
                scalar = numeric[pivot]
                numeric = {index: item / scalar
                           for index, item in numeric.items()}
                value /= scalar
                trace = {key: item / scalar for key, item in trace.items()}
                basis[pivot] = (numeric, value, trace)
                break
            scalar = numeric[pivot]
            base_numeric, base_value, base_trace = basis[pivot]
            for index, item in base_numeric.items():
                numeric[index] = numeric.get(index, 0) - scalar * item
                if not numeric[index]:
                    del numeric[index]
            value -= scalar * base_value
            for key, item in base_trace.items():
                trace[key] = trace.get(key, 0) - scalar * item
                if not trace[key]:
                    del trace[key]
        else:
            if value:
                residuals.append((word, value, trace))
    require(len(basis) == 33, len(basis))
    directly_unreachable = sorted(word for word, value in rhs.items()
                                  if value and not jrows.get(word))
    return {
        "base_mixed_J_rank": len(basis),
        "compatible": not residuals,
        "nonzero_cokernel_residual_rows": len(residuals),
        "directly_unreachable_nonzero_literal_rows": len(directly_unreachable),
        "lex_first_directly_unreachable_word": (
            list(directly_unreachable[0]) if directly_unreachable else None),
        "lex_first_directly_unreachable_value": (
            str(rhs[directly_unreachable[0]]) if directly_unreachable else None),
        "lex_first_reduced_residual": (
            {
                "row_word": list(residuals[0][0]),
                "value": str(residuals[0][1]),
                "source_row_combination": [
                    [list(word), str(value)]
                    for word, value in sorted(residuals[0][2].items())],
            } if residuals else None),
    }


def carrier_records():
    base = base_source()
    records = []
    for p, q in ALL_EDGES:
        residual = tuple(v for v in range(8) if v not in (p, q))
        carriers = [("star", centre) for centre in residual]
        carriers += [("triangle", triangle)
                     for triangle in combinations(residual, 3)]
        for kind, carrier in carriers:
            rows = carrier_rows(base, p, q, kind, carrier)
            rank = dense_rank(rows)
            memberships = tuple(dense_rank(rows + [functional]) == rank
                                for functional in activity_rows(base, p, q))
            records.append((p, q, kind, carrier, rank, memberships))
    require(len(records) == 728, len(records))
    return records


def full_leading_carrier_replay(candidate_labels):
    candidate = {label: Fraction(1) for label in candidate_labels}
    census = Counter()
    failures = []
    for p, q, kind, carrier, base_rank, base_memberships in carrier_records():
        if any(base_memberships):
            order, rank, memberships = 0, base_rank, base_memberships
        else:
            # On the 104 base-active records L0=L1=0.  The first response is
            # the literal quadratic B2 obtained by evaluating rho on Y.
            rows = carrier_rows(candidate, p, q, kind, carrier)
            rank = dense_rank(rows)
            memberships = tuple(dense_rank(rows + [functional]) == rank
                                for functional in activity_rows(
                                    base_source(), p, q))
            order = 2
        mask = "".join("1" if item else "0" for item in memberships)
        census[order, kind, rank, mask] += 1
        if not any(memberships):
            failures.append((p, q, kind, carrier, order, rank, mask))
    require(not failures, failures[:1])
    return {
        "records": 728,
        "order_zero_base_blocked": sum(count for (order, _, _, _), count
                                       in census.items() if order == 0),
        "order_two_formerly_active_now_blocked": sum(
            count for (order, _, _, _), count in census.items() if order == 2),
        "leading_blocker_membership": "728/728",
        "profile": {
            f"order={order}:{kind}:rank={rank}:membership={mask}": count
            for (order, kind, rank, mask), count in sorted(census.items())},
        "scope": (
            "Leading-stratum replay: order zero for the 624 carriers already "
            "blocked at the base and order two for the 104 formerly active "
            "carriers.  It does not assert that every order-zero membership "
            "lifts to an exact Q((t)) row-space membership at higher order."
        ),
    }


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-drop-one-cell", action="store_true")
    args = parser.parse_args()
    frozen = json.loads(INVARIANT_RESULTS.read_text())
    labels = [tuple(label) for label in
              frozen["support_singleton_census"]["lex_first_support"]]
    if args.mutate_drop_one_cell:
        labels.pop()
    require(len(labels) == 10, labels)
    source = series_source(labels)
    h0, terms0 = coefficient_rows(source, 0)
    h2, terms2 = coefficient_rows(source, 2)
    h3, terms3 = coefficient_rows(source, 3)
    h4, terms4 = coefficient_rows(source, 4)
    pure0 = {word: value for word, value in h0.items() if len(set(word)) == 1}
    mixed0 = {word: value for word, value in h0.items() if len(set(word)) > 1}
    require(len(pure0) == 3 and len(mixed0) == 78 and terms0 == 81,
            (len(pure0), len(mixed0), terms0))
    require(not h2 and terms2 == 0, (len(h2), terms2))
    q3 = reduce_numeric_rhs(h3)
    q4_uncorrected = reduce_numeric_rhs(h4)
    require(not q3["compatible"], q3)
    carriers = full_leading_carrier_replay(labels)
    payload = {
        "status": "PASS hostile control: base fails exact fibre already at order zero",
        "source": {
            "base": "A_01=A_23=A_45=A_67=I3",
            "order_one_cells": [list(label) for label in labels],
            "order_one_coefficients": "all 1",
            "order_two_correction": "zero",
        },
        "order_zero_exactness_guard": {
            "pure_nonzero_words": len(pure0),
            "mixed_nonzero_words": len(mixed0),
            "raw_terms": terms0,
            "lex_first_mixed_word": list(min(mixed0)),
            "lex_first_mixed_value": str(mixed0[min(mixed0)]),
            "verdict": (
                "The common-matching I3 base is not GHZ8.  Therefore no formal "
                "exact-fibre lift starts here; higher-order data are diagnostics."
            ),
        },
        "order_two_replay": {
            "nonzero_output_rows": len(h2), "raw_terms": terms2,
            "verdict": "identically zero before quotient",
        },
        "order_three": {
            "nonzero_output_rows": len(h3), "raw_terms": terms3,
            "quotient_by_base_J": q3,
            "verdict": (
                "Conditional higher-order diagnostic: even after ignoring the "
                "order-zero failure, no order-three correction exists."
            ),
            "lex_first_literal_certificate": {
                "word": [0, 0, 0, 1, 0, 1, 1, 0],
                "matching": [[0, 1], [2, 6], [3, 4], [5, 7]],
                "cells": [[0, 1, 0, 0], [2, 6, 0, 1],
                          [3, 4, 1, 0], [5, 7, 1, 0]],
                "coefficient": "1",
                "base_J_row": "zero",
            },
        },
        "order_four_uncorrected_diagnostic": {
            "nonzero_output_rows": len(h4), "raw_terms": terms4,
            "quotient_by_base_J": q4_uncorrected,
            "scope": (
                "Raw A0+tY coefficient only.  Because order three is already "
                "incompatible, this is not a continuation equation and no "
                "order-four correction is claimed."
            ),
        },
        "all_carrier_leading_replay": carriers,
        "terminal_scope": (
            "This lane is not an exact-fibre jet: the base has 78 mixed outputs "
            "at order zero.  The order-three obstruction and carrier census are "
            "retained only as exact response diagnostics and must not be used in "
            "the full-fibre conormal proof."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("orders", (len(h0), terms0), (len(h2), terms2),
          (len(h3), terms3), (len(h4), terms4))
    print("q3", q3)
    print("q4 raw", q4_uncorrected)
    print("carriers", carriers["leading_blocker_membership"])
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
