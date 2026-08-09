#!/usr/bin/env python3
"""Exact sparse-matrix cache audit of five-cross pair blocks 78--91."""

from __future__ import annotations

import importlib.util
from collections import Counter, defaultdict
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_cache_module():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_exact_matrix_transfer_cache.py"
    )
    spec = importlib.util.spec_from_file_location("matrix_cache", path)
    require(spec is not None and spec.loader is not None, "cannot load cache")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ACTIVE_LIBRARY_BLOCKS = (
    0, 1, 3, 5, 6, 7, 9, 12, 14, 16, 18, 19, 20, 22, 25,
    31, 32, 33, 43, 44, 45,
)


def main() -> None:
    matrix_cache = load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 9
    )
    pair_survivors = five.universal_pair_survivors(
        data, left_coordinates, right_coordinates
    )
    require(len(pair_survivors) == 196, "pair-survivor count changed")

    cache = defaultdict(list)
    library_cases = 0
    library_keys = Counter()
    constant_term_witnesses = 0
    for block in ACTIVE_LIBRARY_BLOCKS:
        audit = palette.audit_pair_block(
            five,
            four,
            bounded,
            data,
            pair_survivors[block],
            right_coordinates,
        )
        exception_supports = {case[0] for case, _record in audit["exceptions"]}
        for case, determinant in audit["determinants"]:
            if case[0] in exception_supports:
                continue
            rank, bad, base, augmented = matrix_cache.witness_matrices(
                bounded, data, case[0]
            )
            require(
                rank == determinant[0] and bad == determinant[2],
                "reconstructed library witness changed",
            )
            winning_names = tuple(
                name
                for name, factors in determinant[3].items()
                if name.startswith("aug") and palette.torus_monomial(factors)
            )
            require(
                palette.torus_monomial(determinant[3]["base"])
                and winning_names,
                "library global witness changed",
            )
            if any(
                (0, 0, 0, 0, 0) in polynomial
                for _row, _column, polynomial in base[2]
            ):
                constant_term_witnesses += 1
            for name in winning_names:
                key = matrix_cache.canonical_matrix_pair(base, augmented[name])
                cache[key].append((block, case[0], name))
                library_keys[key] += 1
            library_cases += 1

    target_records = Counter()
    target_frontiers = []
    transfer_hits = []
    fresh_records = []
    fresh_exceptions = []
    for block in range(77, 91):
        records, affine_cases, torus_cases = matrix_cache.torus_pair_block(
            palette,
            five,
            four,
            bounded,
            data,
            pair_survivors[block],
            right_coordinates,
        )
        target_records.update(records)
        target_frontiers.append((len(affine_cases), len(torus_cases)))
        for case in torus_cases:
            _rank, _bad, base, augmented = matrix_cache.witness_matrices(
                bounded, data, case[0]
            )
            hit = next(
                (
                    (name, cache[key])
                    for name, matrix in augmented.items()
                    if (
                        key := matrix_cache.canonical_matrix_pair(base, matrix)
                    ) in cache
                ),
                None,
            )
            if hit is not None:
                transfer_hits.append((block, case[0], hit))
                continue

            determinant = five.five_cell_determinants(
                bounded,
                data,
                case[0],
                tuple(map(bounded.Q, matrix_cache.SAMPLE)),
            )
            fresh_records.append((block, case, determinant))
            winning_names = tuple(
                name
                for name, factors in determinant[3].items()
                if name.startswith("aug") and palette.torus_monomial(factors)
            )
            if palette.torus_monomial(determinant[3]["base"]) and winning_names:
                rank, bad, base, augmented = matrix_cache.witness_matrices(
                    bounded, data, case[0]
                )
                require(
                    rank == determinant[0] and bad == determinant[2],
                    "fresh witness reconstruction changed",
                )
                for name in winning_names:
                    key = matrix_cache.canonical_matrix_pair(base, augmented[name])
                    cache[key].append((block, case[0], name))
                continue
            fresh_exceptions.append((block, case, determinant))

    audited_supports = 14 * 59_640
    new_supports = sum(
        count
        for (grade_count, _status), count in target_records.items()
        if grade_count >= 3
    )
    require(
        (library_cases, len(library_keys), constant_term_witnesses)
        == (1_909, 3_313, 1_909),
        "matrix-library census changed",
    )
    require(
        tuple(target_frontiers)
        == (
            (207, 67), (70, 0), (207, 79), (0, 0), (70, 0),
            (0, 0), (0, 0), (70, 0), (0, 0), (0, 0),
            (207, 67), (70, 0), (207, 79), (0, 0),
        ),
        "target affine/torus frontier changed",
    )
    require(
        (audited_supports, new_supports) == (834_960, 832_608),
        "target support count changed",
    )
    require(
        (len(transfer_hits), len(fresh_records), len(fresh_exceptions))
        == (178, 114, 2),
        "transfer hit/miss frontier changed",
    )

    exception_census = Counter(
        tuple(sorted(palette.non_torus_factors(det[3]["base"])))
        for _block, _case, det in fresh_exceptions
    )
    require(
        exception_census == Counter({("bd+1",): 2}),
        "fresh divisor census changed",
    )
    special_samples = {
        case[0]: {"bd+1": (2, 1, 3, -1, 5)}
        for _block, case, _determinant in fresh_exceptions
    }
    divisor_certificates = palette.close_exceptional_divisors(
        five,
        bounded,
        data,
        tuple((case, determinant)
              for _block, case, determinant in fresh_exceptions),
        special_samples,
    )
    require(len(divisor_certificates) == 2, "fresh divisor charts changed")

    closed_cumulative = 4_571_112 + new_supports
    remaining = 11_614_176 - closed_cumulative
    require(
        (closed_cumulative, remaining) == (5_403_720, 6_210_456),
        "cumulative frontier arithmetic changed",
    )
    print("N=10 five-cross cached pair blocks 78-91: exact frontier")
    print(f"library monomial cases: {library_cases}")
    print(f"library exact matrix keys: {len(library_keys)}")
    print(f"library witnesses with old-source constant terms: "
          f"{constant_term_witnesses}")
    print(f"target supports: {audited_supports}; new supports: {new_supports}")
    print(f"target affine/torus candidates: "
          f"{sum(x for x, _ in target_frontiers)}/"
          f"{sum(y for _, y in target_frontiers)}")
    print(f"exact matrix transfer hits: {len(transfer_hits)}")
    print(f"fresh literal determinant records: {len(fresh_records)}")
    print(f"fresh non-monomial exceptions: {len(fresh_exceptions)}")
    print(f"fresh divisor charts: {len(divisor_certificates)}")
    print("new divisor types/depth: 0; literal survivors: 0")
    print("old-source-independent matrix witnesses certified: 0")
    print(f"cumulative exact matrix-cache hits: {53 + len(transfer_hits)}")
    print(f"cumulative closed new grade-3-to-6 supports: {closed_cumulative}")
    print(f"remaining unaudited grade-3-to-6 supports: {remaining}")


if __name__ == "__main__":
    main()
