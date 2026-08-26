#!/usr/bin/env python3
"""Exact formula/policy referee for the not-yet-constructed K17 bucket."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from math import gcd
import importlib.util
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23"
          / "filtered_k24_reducer.py")
K16_RUN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
           / "results_filtered_k16_run.json")
K15 = K16_RUN.with_name("checkpoint_direct_k15.bin")
K16_COLLECTION = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
                  / "results_orbit0_k16_literal_residual.json")
SIGN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-sign-referee-2026-08-23"
        / "results_filtered_k16_sign_referee.json")
OUT = HERE / "results_filtered_k17_interface.json"
RECORD = struct.Struct("<24sq")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    state = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def main(write_results=False):
    d = load("filtered_k17_design", DESIGN)
    run = json.loads(K16_RUN.read_text())
    collection = json.loads(K16_COLLECTION.read_text())
    sign = json.loads(SIGN.read_text())
    require(run["K15_checkpoint"]["reduced"] == [0, 0, 0],
            run["K15_checkpoint"])
    require(sign["status"].startswith("EXACT_SIGN_RETRACTION"), sign["status"])
    require(collection["collection"]["literal_pivot_uses"] == 6_619_280,
            collection["collection"]["literal_pivot_uses"])

    # Exact source transport for all tail layers, not only the K2 layer used
    # by the frozen collector.
    tail_transport_checks = Counter()
    for action in d.H:
        for pivot in range(78):
            moved = d.CTX.pivot_permutations[action][pivot]
            for degree in (2, 3, 4):
                actual = {d.F.move_row(tail, action)
                          for tail in d.CTX.tails[pivot][degree]}
                expected = set(d.CTX.tails[moved][degree])
                require(actual == expected, (action, pivot, moved, degree))
                tail_transport_checks[degree] += len(actual)

    # Precompute the all-dividing-pivot count on each anchor support.  Every
    # anchor head is squarefree, so support (not multiplicity) is sufficient.
    anchor_cells = d.CTX.anchor_cells
    anchor_position = {cell: i for i, cell in enumerate(anchor_cells)}
    masks = []
    for vector in d.CTX.vectors:
        require(set(vector) <= {0, 1} and sum(vector) == 4, vector)
        masks.append(sum((value != 0) << i for i, value in enumerate(vector)))
    pivot_count = [sum(support & mask == mask for mask in masks)
                   for support in range(1 << 12)]

    denominator_histogram = Counter()
    pivot_count_histogram = Counter()
    records = 0
    with K15.open("rb") as stream:
        require(stream.read(8) == b"K15CHK1\0", "K15 magic")
        count = struct.unpack("<Q", stream.read(8))[0]
        previous = None
        for records in range(1, count + 1):
            raw = stream.read(RECORD.size)
            require(len(raw) == RECORD.size, records)
            row, mass = RECORD.unpack(raw)
            require(mass and (previous is None or previous < row), records)
            previous = row
            support = 0
            for cell in row:
                index = anchor_position.get(cell)
                if index is not None:
                    support |= 1 << index
            choices = pivot_count[support]
            require(choices > 0, (row.hex(), mass))
            denominator = choices // gcd(choices, abs(mass))
            pivot_count_histogram[choices] += 1
            denominator_histogram[denominator] += 1
        require(not stream.read(1), "K15 trailing bytes")
    require(records == count == 5_311_211, (records, count))

    direct_per_slice = 6 * 12 * 32 * 60 + 32 ** 3
    require(direct_per_slice == 171_008, direct_per_slice)
    direct_raw = 485 * direct_per_slice
    k14_k3_raw = collection["collection"]["literal_pivot_uses"] * 32

    result = {
        "status": "PASS_EXACT_K17_COMPONENT_FORMULA_AND_POLICY_AUDIT",
        "K17_formula": [
            {
                "component": "direct",
                "formula": "-R8prime*(E2*E3*E4 over six orders + E3^3)",
                "raw_occurrences_per_R8_H_slice": direct_per_slice,
                "raw_occurrences": direct_raw,
            },
            {
                "component": "K14_to_K17",
                "formula": (
                    "+R8prime*E2^3 leading-head coefficients, averaged over the "
                    "frozen 25-cover-valid K14 pivots, times their 32 K3 tails"
                ),
                "recorded_K14_pivot_uses": 6_619_280,
                "raw_K3_tail_occurrences": k14_k3_raw,
                "sign": "positive of R8prime after the exact telescope orientation",
            },
            {
                "component": "K15_to_K17",
                "formula": (
                    "for each collected direct K15 mass p, average source coefficient "
                    "p over every dividing K0 pivot and add -p/choices times each of "
                    "its 12 K2 tails"
                ),
                "K15_H_orbits": records,
                "all_K15_rows_pivotable": True,
                "pivot_count_histogram": {
                    str(k): v for k, v in sorted(pivot_count_histogram.items())
                },
                "source_coefficient_denominator_histogram_after_cancellation": {
                    str(k): v for k, v in sorted(denominator_histogram.items())
                },
            },
        ],
        "no_K16_feed": "a K16 pivot emits first at K18",
        "policy": {
            "K14": "frozen 25-cover-valid-pivot average (not all pivots)",
            "K15": "average all literal dividing K0 pivots",
            "K17_reduction_after_collection": "average all literal dividing K0 pivots",
            "H_equivariance": (
                "divisibility sets are transported by the H pivot permutation and "
                "equal averaging is invariant"
            ),
            "policy_dependence": (
                "defined and H-equivariant, but not proved confluent or independent "
                "of the chosen all-pivot convention"
            ),
        },
        "tail_transport_checks": {
            str(k): v for k, v in sorted(tail_transport_checks.items())
        },
        "engineering_guard": (
            "The K17 provider must use exact rationals: K15 all-pivot averaging has "
            f"denominators {sorted(denominator_histogram)} after cancellation."
        ),
        "scope": (
            "This proves the source-labelled formula and policies defining K17. "
            "It does not construct/collect the K17 bucket, evaluate its charge, or "
            "advance to K18."
        ),
        "pinned": {
            str(DESIGN.relative_to(ROOT)): digest(DESIGN),
            str(K16_RUN.relative_to(ROOT)): digest(K16_RUN),
            str(K15.relative_to(ROOT)): digest(K15),
            str(K16_COLLECTION.relative_to(ROOT)): digest(K16_COLLECTION),
            str(SIGN.relative_to(ROOT)): digest(SIGN),
        },
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "direct_raw_occurrences": direct_raw,
        "K14_K3_raw_occurrences": k14_k3_raw,
        "K15_H_orbits": records,
        "K15_denominators": sorted(denominator_histogram),
        "logical_sha256": logical,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
