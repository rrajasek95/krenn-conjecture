#!/usr/bin/env python3
"""Exact 33-type census of the orbit-zero K16 same-head local star.

This deliberately works in the 12-anchor multiplicity quotient.  It retains
all 78 literal singleton heads and all twelve K2 tails before projection, but
never materializes the 701,717,184-row collected literal residual.  Since
projection is linear, an affine obstruction in this quotient is also an
obstruction for every literal refinement of the same anchor type.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import argparse
import ast
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_DIR = ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
K14_SOURCE = K14_DIR / "audit_orbit0_k14_interface.py"
COVER = K14_DIR / "results_k16_anchor_cover.json"
LEX_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-lower-kernel-hpl-2026-08-23"
LEX_RESULT = LEX_DIR / "results_k16_lower_kernel_component.json"
RESULT = HERE / "results_k16_local_star_census.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def exact_rank(rows):
    """Fraction-free-sized exact row rank; matrices here are at most 38x35."""
    pivots = {}
    for source in rows:
        row = [Fraction(value) for value in source]
        while True:
            pivot = next((index for index, value in enumerate(row) if value), None)
            if pivot is None:
                break
            if pivot not in pivots:
                scale = row[pivot]
                row = [value / scale for value in row]
                pivots[pivot] = row
                break
            scale = row[pivot]
            old = pivots[pivot]
            row = [left - scale * right
                   for left, right in zip(row, old, strict=True)]
    return len(pivots)


K14 = load("orbit0_k16_local_star_k14", K14_SOURCE)
F = K14.FROZEN


def mixed_pivots():
    cells = tuple(sorted(F.A))
    answer = []
    for colours in product(range(3), repeat=4):
        if len(set(colours)) == 1:
            continue
        word = F.word_from_pair_colours(colours)
        anchor = F.BASE.term_ids(word, F.M0)
        tails = tuple(term for term in F.BASE.word_terms(word)
                      if F.row_k_degree(term) == 2)
        require(len(tails) == 12, (colours, len(tails)))
        anchor_vector = tuple(Counter(anchor)[cell] for cell in cells)
        tail_vectors = tuple(tuple(Counter(tail)[cell] for cell in cells)
                             for tail in tails)
        answer.append((colours, anchor_vector, tail_vectors))
    require(len(answer) == 78, len(answer))
    return tuple(answer)


def census(mutate=False):
    require(file_sha256(K14_SOURCE)
            == "7a9891d5fc4d8964518147c0202e0f29b7393e7bed3a7651beb053eb4402c19a",
            "K14 source drift")
    require(file_sha256(COVER)
            == "5efffe78e3fd9c42ca91be2a6a10bb7d4d4cc0fa13d986ca411cc692c999dfdf",
            "33-type cover drift")
    require(file_sha256(LEX_RESULT)
            == "ef1abb6415e5af60d161f2254496f69b63467f0ccbc753f11c8fc2a84bee5866",
            "lex-star referee drift")

    cover = json.loads(COVER.read_text())
    candidate_data = cover["single_pivot_cover"]["candidate_data"]
    signatures = tuple(sorted(ast.literal_eval(label) for label in candidate_data))
    require(len(signatures) == 33 and len(set(signatures)) == 33,
            "K14 type census changed")
    pivots = mixed_pivots()

    records = []
    profile_histogram = Counter()
    for type_index, signature in enumerate(signatures):
        live = tuple((colours, anchor, tails)
                     for colours, anchor, tails in pivots
                     if all(left >= right
                            for left, right in zip(signature, anchor, strict=True)))
        require(live, signature)
        columns = []
        for _colours, anchor, tails in live:
            base = tuple(left - right
                         for left, right in zip(signature, anchor, strict=True))
            column = Counter(tuple(left + right
                                   for left, right in zip(base, tail, strict=True))
                             for tail in tails)
            columns.append(column)

        # Hostile guard: losing even one literal K2 occurrence invalidates the
        # augmentation functional used in the uniform obstruction theorem.
        if mutate and type_index == 0:
            first_row = min(columns[0])
            columns[0][first_row] -= 1
            if columns[0][first_row] == 0:
                del columns[0][first_row]

        masses = tuple(sum(column.values()) for column in columns)
        require(set(masses) == {12}, "hostile mutation/literal K2 tail loss fired")
        rows = tuple(sorted(set().union(*(set(column) for column in columns))))
        matrix = [[column.get(row, 0) for column in columns] for row in rows]
        tail_rank = exact_rank(matrix)
        head_kernel_dimension = len(columns) - 1
        differences = [[row[index] - row[0]
                        for index in range(1, len(columns))]
                       for row in matrix]
        lower_transfer_rank = exact_rank(differences)
        stacked_rank = exact_rank(matrix + [[1] * len(columns)])
        affine_zero = stacked_rank == tail_rank + 1
        owner_histogram = Counter(sum(column.get(row, 0) != 0
                                      for column in columns)
                                  for row in rows)

        # The all-rows augmentation epsilon sends every B_p to 12.  Hence
        # ker(B) is contained in ker(sum), D has rank rank(B)-1, and zero can
        # never be an affine combination of the columns.
        require(not affine_zero, (signature, "unexpected affine zero"))
        require(lower_transfer_rank == tail_rank - 1,
                (signature, lower_transfer_rank, tail_rank))
        residual_lower_kernel_dimension = len(columns) - tail_rank
        require(residual_lower_kernel_dimension
                == head_kernel_dimension - lower_transfer_rank,
                "rank-nullity mismatch")

        profile = (len(columns), len(rows), tail_rank,
                   lower_transfer_rank, residual_lower_kernel_dimension)
        profile_histogram[profile] += 1
        records.append({
            "canonical_anchor_signature": list(signature),
            "pivot_count": len(columns),
            "projected_tail_rows": len(rows),
            "projected_tail_rank_over_Q": tail_rank,
            "common_head_kernel_dimension": head_kernel_dimension,
            "projected_lower_kernel_transfer_rank_over_Q": lower_transfer_rank,
            "residual_lower_kernel_dimension": residual_lower_kernel_dimension,
            "zero_in_projected_affine_tail_hull": affine_zero,
            "projected_private_rows": owner_histogram[1],
            "projected_row_owner_histogram": {
                str(key): owner_histogram[key] for key in sorted(owner_histogram)
            },
        })

    lex = json.loads(LEX_RESULT.read_text())
    star = lex["same_head_schreyer_star"]
    lex_signature = tuple(lex["lex_factorized_head"]["canonical_anchor_signature"])
    lex_record = next(record for record in records
                      if tuple(record["canonical_anchor_signature"]) == lex_signature)
    require((lex_record["pivot_count"], lex_record["projected_tail_rows"],
             lex_record["projected_tail_rank_over_Q"],
             lex_record["projected_lower_kernel_transfer_rank_over_Q"])
            == (8, 21, 8, 7), "lex projected referee mismatch")
    require((star["pivot_count"], star["distinct_K16_rows"],
             star["tail_matrix_rank_over_Q"],
             star["transferred_lower_kernel_rank_over_Q"])
            == (8, 42, 8, 7), "literal lex referee mismatch")

    lex_projected_profile_count = sum(
        record["pivot_count"] == 8
        and record["projected_tail_rows"] == 21
        and record["projected_tail_rank_over_Q"] == 8
        and record["projected_lower_kernel_transfer_rank_over_Q"] == 7
        for record in records
    )
    require(lex_projected_profile_count == 4, lex_projected_profile_count)

    payload = {
        "format": "n8-orbit0-k16-local-star-census-v1",
        "status": "EXACT_33_TYPE_PROJECTED_STAR_CENSUS_AFFINE_OBSTRUCTION_UNIFORM",
        "source": {
            "K14_factor_stabilizer_types": len(signatures),
            "factor_stabilizer_order": 384,
            "literal_singleton_pivots": len(pivots),
            "literal_K2_tails_per_pivot": 12,
        },
        "uniform_theorem": {
            "affine_obstructed_types": sum(
                not row["zero_in_projected_affine_tail_hull"] for row in records),
            "affine_solvable_types": sum(
                row["zero_in_projected_affine_tail_hull"] for row in records),
            "augmentation_functional": (
                "epsilon is the sum of all projected tail-row coordinates; "
                "epsilon(B_p)=12 for every literal singleton pivot p"
            ),
            "consequence": (
                "B*alpha=0 forces sum(alpha)=0, so B*alpha=0 and "
                "sum(alpha)=1 is impossible for all 33 types. Because anchor "
                "projection is linear, every literal refinement is also "
                "affine-obstructed at this uncorrected twelve-tail star."
            ),
            "lower_kernel_formula": (
                "ker(B) is contained in the common-head kernel; therefore "
                "rank(B restricted to ker(sum))=rank(B)-1 and the residual "
                "lower-kernel dimension is pivot_count-rank(B)."
            ),
        },
        "profile_histogram": [
            {
                "pivot_count": profile[0],
                "projected_tail_rows": profile[1],
                "projected_tail_rank": profile[2],
                "projected_lower_transfer_rank": profile[3],
                "residual_lower_kernel_dimension": profile[4],
                "K14_types": count,
            }
            for profile, count in sorted(profile_histogram.items())
        ],
        "types": records,
        "lex_8_pivot_referee": {
            "canonical_anchor_signature": list(lex_signature),
            "projected_profile": {
                "pivots": 8, "rows": 21, "tail_rank": 8,
                "lower_transfer_rank": 7,
            },
            "literal_profile": {
                "pivots": 8, "rows": 42, "tail_rank": 8,
                "lower_transfer_rank": 7,
                "owner_histogram": star["row_owner_degree_histogram"],
            },
            "types_with_same_projected_8_21_8_7_profile": (
                lex_projected_profile_count
            ),
            "verdict": (
                "The affine obstruction is uniform across all 33 types, but "
                "the numerical 8-pivot profile is not: it is one of twelve "
                "projected profiles and occurs in four types. The literal "
                "42-row split is provenance specific to the pinned lex head."
            ),
        },
        "scope_guard": (
            "Exact for the uncorrected same-head star after projecting only "
            "tail rows to the 12 anchor multiplicities. It proves literal "
            "affine noncancellation by functoriality, but projected ranks are "
            "only lower bounds for literal ranks. It does not include second "
            "singleton reductions, lower-filtration transfers, the collected "
            "K16 residual, or any other chart."
        ),
        "pinned": {
            str(K14_SOURCE.relative_to(ROOT)): file_sha256(K14_SOURCE),
            str(COVER.relative_to(ROOT)): file_sha256(COVER),
            str(LEX_RESULT.relative_to(ROOT)): file_sha256(LEX_RESULT),
        },
    }
    logical = sha256(json.dumps(payload, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    payload["logical_sha256"] = logical
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    payload = census(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "logical_sha256": payload["logical_sha256"],
        "uniform_theorem": payload["uniform_theorem"],
        "profile_histogram": payload["profile_histogram"],
        "lex_8_pivot_referee": payload["lex_8_pivot_referee"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
