#!/usr/bin/env python3
"""Exact sparse-matrix cache audit of five-cross pair blocks 106--119."""

from __future__ import annotations

import importlib.util
from collections import Counter, defaultdict
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_cached_blocks():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_cached_blocks_78_91.py"
    )
    spec = importlib.util.spec_from_file_location("cached_blocks", path)
    require(spec is not None and spec.loader is not None, "cannot load cache")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ACTIVE_LIBRARY_BLOCKS = (
    0, 1, 3, 5, 6, 7, 9, 12, 14, 16, 18, 19, 20, 22, 25,
    31, 32, 33, 43, 44, 45, 77, 79, 87, 89,
)


DIVISOR_SAMPLES = {
    "ac+1": (1, 2, -1, 3, 5),
    "ad+1": (1, 2, 3, -1, 5),
    "ad-1": (1, 2, 3, 1, 5),
    "ae+1": (1, 2, 3, 5, -1),
    "ace-d": (1, 5, 2, 6, 3),
    "bd+1": (2, 1, 3, -1, 5),
    "c+d": (2, 3, 1, -1, 5),
    "c-d": (2, 3, 1, 1, 5),
    "d+e": (2, 3, 5, 1, -1),
    "d-e": (2, 3, 5, 1, 1),
}


def direct_divisor_certificates(
    palette, five, bounded, data, exceptions
):
    certificates = []
    for case, determinant in exceptions:
        divisors = palette.non_torus_factors(determinant[3]["base"])
        require(divisors <= set(DIVISOR_SAMPLES), "new divisor type appeared")
        for divisor in sorted(divisors):
            special = five.five_cell_determinants(
                bounded,
                data,
                case[0],
                tuple(map(bounded.Q, DIVISOR_SAMPLES[divisor])),
            )
            base_ok = palette.divisor_has_no_torus_zero(
                divisor, special[3]["base"]
            )
            augmented = tuple(
                name
                for name, factors in special[3].items()
                if name.startswith("aug")
                and palette.divisor_has_no_torus_zero(divisor, factors)
            )
            require(
                base_ok and augmented,
                f"direct divisor chart did not close: {case[0]} / {divisor}",
            )
            certificates.append((case[0], divisor, augmented[0]))
    return tuple(certificates)


def main() -> None:
    cached_blocks = load_cached_blocks()
    matrix_cache = cached_blocks.load_cache_module()
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
    for block in range(105, 119):
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
        tuple(target_frontiers)
        == (
            (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
            (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
            (612, 240), (207, 75), (612, 344), (0, 0),
        ),
        "target affine/torus frontier changed",
    )
    require(
        (audited_supports, new_supports) == (834_960, 832_608),
        "target support count changed",
    )
    require(
        (library_cases, len(library_keys)) == (2_199, 3_676),
        "matrix-library census changed",
    )
    require(
        (len(transfer_hits), len(fresh_records), len(fresh_exceptions))
        == (281, 378, 17),
        "transfer hit/miss frontier changed",
    )

    exception_census = Counter(
        (
            tuple(sorted(palette.non_torus_factors(det[3]["base"]))),
            tuple(
                sorted(
                    {
                        factor
                        for name, factors in det[3].items()
                        if name.startswith("aug")
                        for factor in palette.non_torus_factors(factors)
                    }
                )
            ),
        )
        for _block, _case, det in fresh_exceptions
    )
    require(
        exception_census
        == Counter(
            {
                (("ad+1",), ("ad+1",)): 4,
                (("ae+1",), ("ae+1",)): 3,
                (("ace-d",), ("ace-d",)): 2,
                (("ad+1",), ("ad+1", "ae+1")): 2,
                (("ac+1",), ("ac+1",)): 1,
                (("ae+1",), ("ae+1", "bd+1")): 1,
                (("ad+1", "ad-1"), ("ad+1", "ad-1")): 1,
                (("d+e", "d-e"), ("d+e", "d-e")): 1,
                (("c+d",), ("c+d",)): 1,
                (
                    ("c+d", "c-d"),
                    ("-c+d", "ae+1", "c+d", "c-d"),
                ): 1,
            }
        ),
        "fresh divisor census changed",
    )
    divisor_certificates = direct_divisor_certificates(
        palette,
        five,
        bounded,
        data,
        tuple((case, determinant)
              for _block, case, determinant in fresh_exceptions),
    )
    require(len(divisor_certificates) == 20, "divisor chart count changed")
    closed_cumulative = 6_236_328 + new_supports
    remaining = 11_614_176 - closed_cumulative
    require(
        (closed_cumulative, remaining) == (7_068_936, 4_545_240),
        "cumulative frontier arithmetic changed",
    )
    print("N=10 five-cross cached pair blocks 106-119: exact frontier")
    print(f"library monomial cases/keys: {library_cases}/{len(library_keys)}")
    print(f"target supports: {audited_supports}; new supports: {new_supports}")
    print(
        "target affine/torus candidates: "
        f"{sum(x for x, _ in target_frontiers)}/"
        f"{sum(y for _, y in target_frontiers)}"
    )
    print(f"exact matrix transfer hits: {len(transfer_hits)}")
    print(f"fresh literal determinant records: {len(fresh_records)}")
    print(f"fresh non-monomial exceptions: {len(fresh_exceptions)}")
    print(f"fresh exception census: {exception_census}")
    print(f"fresh divisor charts: {len(divisor_certificates)}")
    print("literal survivors: 0")
    print(f"cumulative exact matrix-cache hits: {231 + len(transfer_hits)}")
    print(f"cumulative closed new grade-3-to-6 supports: {closed_cumulative}")
    print(f"remaining unaudited grade-3-to-6 supports: {remaining}")


if __name__ == "__main__":
    main()
