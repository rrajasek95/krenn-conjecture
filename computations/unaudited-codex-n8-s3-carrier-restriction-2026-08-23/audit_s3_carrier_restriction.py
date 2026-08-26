#!/usr/bin/env python3
"""Exact carrier-response restrictions of all minimal S3 low-source duals.

The frozen residual52 incidence component has 28 minimal three-row exact
separators.  This script reconstructs all of them over Z and restricts their
rows to oriented response halves for the canonical carrier pair 67.  The
restriction records the colour pair (a,b) at the carrier endpoints, hence a
coordinate of K_ab.  No source closure or Groebner computation is performed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/unaudited-codex-n8-s3-source-component-2026-08-23/audit_s3_source_component.py"
SOURCE_RESULT = ROOT / "computations/unaudited-codex-n8-s3-source-component-2026-08-23/results_s3_source_component.json"
RESULT = HERE / "results_s3_carrier_restriction.json"
EXPECTED = {
    SOURCE: "a4d22563904e8dde445067b9e8c466cd048ea471ffdaac566b66202eec1ae189",
    SOURCE_RESULT: "7d27d9301ca81b4567db74fb872b324d068f1c90eae37caf5fe544adeb2b4b27",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_source():
    spec = importlib.util.spec_from_file_location("frozen_s3_source", SOURCE)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "cannot load frozen S3 source audit")
    spec.loader.exec_module(module)
    return module


def primitive(vector):
    divisor = 0
    for value in vector:
        divisor = gcd(divisor, abs(value))
    require(divisor, "zero vector has no primitive normalization")
    vector = tuple(value // divisor for value in vector)
    first = next(value for value in vector if value)
    if first < 0:
        vector = tuple(-value for value in vector)
    return vector


def exact_left_kernel(selected_rows, columns):
    """Primitive rank-two left kernel for a three-row stopping support."""
    vectors = []
    selected = set(selected_rows)
    for column in columns.values():
        if not selected.intersection(column):
            continue
        vector = tuple(column.get(row, 0) for row in selected_rows)
        if vector != (0, 0, 0):
            vectors.append(vector)
    for left in vectors:
        for right in vectors:
            cross = (
                left[1] * right[2] - left[2] * right[1],
                left[2] * right[0] - left[0] * right[2],
                left[0] * right[1] - left[1] * right[0],
            )
            if cross != (0, 0, 0):
                answer = primitive(cross)
                require(all(sum(a * b for a, b in zip(answer, vector)) == 0
                            for vector in vectors),
                        "three-row kernel is not one-dimensional over Z")
                return answer
    raise RuntimeError("three-row support has rank below two")


def carrier_views(row, coordinates, p=6, q=7):
    """All oriented response-half readings at carrier pair pq.

    A reading chooses distinct cells incident to p and q, whose other endpoints
    are distinct and avoid p,q.  The remaining cell is the residual multiplier.
    The carrier coordinate is the pair of colours seen at p,q.
    """
    cells = [coordinates[identifier] for identifier in row]
    answer = []
    for ip, cp in enumerate(cells):
        if p not in cp[:2]:
            continue
        for iq, cq in enumerate(cells):
            if iq == ip or q not in cq[:2]:
                continue
            remaining_positions = [index for index in range(len(cells))
                                   if index not in (ip, iq)]
            if len(remaining_positions) != 1:
                continue
            ir = remaining_positions[0]
            cr = cells[ir]
            if p in cr[:2] or q in cr[:2]:
                continue

            def endpoint_colour(cell, site):
                i, j, a, b = cell
                return a if i == site else b

            def other_endpoint(cell, site):
                i, j, _a, _b = cell
                return j if i == site else i

            up = other_endpoint(cp, p)
            uq = other_endpoint(cq, q)
            if up == uq or up in (p, q) or uq in (p, q):
                continue
            item = {
                "K": (endpoint_colour(cp, p), endpoint_colour(cq, q)),
                "response_edge": tuple(sorted((up, uq))),
                "response_output": (endpoint_colour(cp, up), endpoint_colour(cq, uq)),
                "multiplier": row[ir],
                "oriented_cells": (row[ip], row[iq]),
            }
            if item not in answer:
                answer.append(item)
    return answer


def rational_rank(matrix):
    """Rank over Q for a small integer row matrix."""
    from fractions import Fraction
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next((index for index in range(rank, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for index in range(len(work)):
            if index == rank or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [left - scale * right
                           for left, right in zip(work[index], work[rank])]
        rank += 1
    return rank


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"frozen input drift: {path}")
    S = load_source()
    N = S.load_normalized()
    D5 = N.D5
    polynomials = S.normalized_polynomials(D5)
    s3 = S.parse_kernel("S3")

    cubic_sources = defaultdict(list)
    for code, polynomial in polynomials.items():
        for row in polynomial:
            if len(row) == 3:
                cubic_sources[row].append(code)
    residual = {row: coefficient for row, coefficient in s3.items()
                if not cubic_sources.get(row)}
    rows, columns = S.build_low_component(residual, polynomials)
    _census, separating, row_index = S.stopping_set_census(rows, columns, residual)
    require(len(separating) == 28, "minimal separator count changed")

    restrictions = []
    coordinate_vectors = []
    unique_view_histogram = Counter()
    all_view_histogram = Counter()
    for support_indices in sorted(separating, key=lambda item: tuple(sorted(item))):
        selected_rows = tuple(rows[index] for index in sorted(support_indices))
        dual_vector = exact_left_kernel(selected_rows, columns)
        pairing = sum(coefficient * residual.get(row, 0)
                      for row, coefficient in zip(selected_rows, dual_vector))
        require(pairing, "enumerated exact dual stopped separating residual52")

        row_views = {row: carrier_views(row, D5.COORDINATES)
                     for row in selected_rows}
        unique_view_histogram.update((len(row_views[row]),) for row in selected_rows)
        vector = [0] * 9
        for row, coefficient in zip(selected_rows, dual_vector):
            for view in row_views[row]:
                a, b = view["K"]
                vector[3 * a + b] += coefficient
                all_view_histogram[(a, b)] += 1
        if mutate and not restrictions:
            vector[1] = 1
        coordinate_vectors.append(vector)
        restrictions.append({
            "dual": [[row.hex(), coefficient]
                     for row, coefficient in zip(selected_rows, dual_vector)],
            "target_pairing": pairing,
            "carrier67_K_vector": vector,
            "row_views": {
                row.hex(): [{
                    "K": list(view["K"]),
                    "response_edge": list(view["response_edge"]),
                    "response_output": list(view["response_output"]),
                    "multiplier": f"{view['multiplier']:02x}",
                    "oriented_cells": [f"{value:02x}" for value in view["oriented_cells"]],
                } for view in row_views[row]]
                for row in selected_rows
            },
        })

    nonzero_coordinates = sorted({index for vector in coordinate_vectors
                                  for index, value in enumerate(vector) if value})
    coordinate_rank = rational_rank(coordinate_vectors)
    require(coordinate_rank == 1 and nonzero_coordinates == [0],
            "carrier restriction unexpectedly reaches beyond K00")
    require(all(all(value == 0 for value in vector[1:])
                for vector in coordinate_vectors),
            "an off-diagonal/other-colour correction channel appeared")

    result = {
        "format": "n8-S3-minimal-dual-carrier-restriction-v1",
        "status": "FIXED_CARRIER_RESTRICTION_RANK_ONE_K00_ONLY",
        "frozen_inputs_sha256": {str(path.relative_to(ROOT)): digest
                                  for path, digest in EXPECTED.items()},
        "minimal_duals": len(restrictions),
        "fixed_carrier_pair": [6, 7],
        "coordinate_order": [f"K{a}{b}" for a in range(3) for b in range(3)],
        "restriction_rank_over_Q": coordinate_rank,
        "nonzero_coordinate_indices": nonzero_coordinates,
        "nonzero_coordinates": [f"K{index // 3}{index % 3}"
                                for index in nonzero_coordinates],
        "span_of_eight_direct_blocker_corrections": 0,
        "correction_codimension": 8,
        "row_carrier_view_count_histogram": {
            str(key[0]): value for key, value in sorted(unique_view_histogram.items())
        },
        "all_oriented_view_K_histogram": {
            f"K{a}{b}": value for (a, b), value in sorted(all_view_histogram.items())
        },
        "restrictions": restrictions,
        "interpretation": (
            "Every fixed-67 response half occurring in every minimal exact "
            "three-row low-source dual sees carrier endpoint colours (0,0). "
            "Thus these duals recover the leading support-unit K00 channel but "
            "none of the eight channels introduced by replacing K00 with the "
            "full direct form <K,A67>. Colour transport changes the chart/support "
            "unit and does not span the eight corrections inside this fixed chart."
        ),
        "scope": (
            "exact census of all 28 minimal size-three separators of the frozen "
            "degree-five y<=3 residual52 component, restricted to oriented "
            "response halves at fixed carrier pair 67; it does not classify "
            "larger-support duals or higher HPL corrections"
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(mutate=args.mutate)
    if not args.mutate:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                          encoding="ascii")
    print(json.dumps({key: result[key] for key in (
        "status", "minimal_duals", "restriction_rank_over_Q",
        "nonzero_coordinates", "correction_codimension", "logical_sha256"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
