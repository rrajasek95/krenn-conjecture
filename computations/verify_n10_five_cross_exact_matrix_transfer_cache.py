#!/usr/bin/env python3
"""Sound exact-matrix transfer cache beyond the first 35 pair blocks.

The coarse 188 factor signatures are not themselves transfer certificates.
This checker stores the actual square/augmented polynomial witness matrices
for the globally monomial cases, modulo simultaneous S5 weight relabelling,
and applies only exact matrix hits before computing any new determinant.
"""

from __future__ import annotations

import importlib.util
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_palette():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_affine_signature_palette.py"
    )
    spec = importlib.util.spec_from_file_location("signature_palette", path)
    require(spec is not None and spec.loader is not None, "cannot load palette")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PERMUTATIONS = tuple(permutations(range(5)))
SAMPLE = (1, 2, 3, 5, 7)


def permute_monomial(monomial, permutation):
    result = [0] * len(monomial)
    for old_index, exponent in enumerate(monomial):
        result[permutation[old_index]] = exponent
    return tuple(result)


def polynomial_key(polynomial, permutation):
    return tuple(
        sorted(
            (
                permute_monomial(monomial, permutation),
                (coefficient.numerator, coefficient.denominator),
            )
            for monomial, coefficient in polynomial.items()
        )
    )


def sparse_matrix_key(matrix, permutation):
    rows, columns, entries = matrix
    return (
        rows,
        columns,
        tuple(
            (row, column, polynomial_key(polynomial, permutation))
            for row, column, polynomial in entries
        ),
    )


def canonical_matrix_pair(base, augmented):
    return min(
        (
            sparse_matrix_key(base, permutation),
            sparse_matrix_key(augmented, permutation),
        )
        for permutation in PERMUTATIONS
    )


def torus_pair_block(
    palette, five, four, bounded, data, left_pair, right_coordinates
):
    affine_cache = {}
    records = Counter()
    affine_cases = []
    for right_triple in combinations(right_coordinates, 3):
        support = left_pair + right_triple
        grades = tuple(
            bounded.support_permanents(data, support, (bounded.Q(1),) * 5)
        )
        grade_count = len(grades)
        if grade_count < 3:
            records[(grade_count, "prior")] += 1
            continue
        if grades not in affine_cache:
            affine_cache[grades] = bounded.exact_affine_system(data, grades)
        system = affine_cache[grades]
        records[(grade_count, "affine" if system[0] else "excluded")] += 1
        if system[0]:
            affine_cases.append((support, grades, system))
    saturation = (
        five.torus_affine_saturation(
            four, bounded, data, affine_cases, ("a", "b", "c", "d", "e")
        )
        if affine_cases
        else {}
    )
    torus_cases = tuple(
        affine_cases[index]
        for index, survives in saturation.items()
        if survives
    )
    return records, tuple(affine_cases), torus_cases


def witness_matrices(bounded, data, support):
    module = data["module"]
    two_cell = data["two_cell"]
    sample = tuple(map(bounded.Q, SAMPLE))
    columns_at_sample = bounded.evaluated_columns(data, support, sample)
    labels, basis = bounded.independent_column_labels(module, columns_at_sample)
    polynomial_columns, polynomial_residual = bounded.raw_polynomial_data(
        data, support
    )
    pivot_rows = tuple(sorted(basis))
    require(len(labels) == len(pivot_rows), "pivot square changed")

    cells = data["provenance"].add_weighted_coordinates(
        module,
        data["lifted_base"],
        tuple(zip(support, sample)),
    )
    tensor = module.matching_tensor(data["provenance"].B10, cells)
    tensor = data["forced_pair"].tensor_difference(
        tensor, data["forced_pair"].delta_tensor(data["provenance"].B10)
    )
    residual_rows = data["forced_pair"].flatten_rows(
        tensor,
        data["provenance"].B10,
        (2, 6, 7),
        data["u_set"],
    )
    bad = {
        word: two_cell.quotient_remainder(vector, basis)
        for word, vector in residual_rows.items()
        if not module.rational_member(vector, basis)
    }

    base_entries = []
    for row_number, row in enumerate(pivot_rows):
        for column_number, label in enumerate(labels):
            polynomial = polynomial_columns[label].get(row, {})
            if polynomial:
                base_entries.append((row_number, column_number, polynomial))
    base = (len(labels), len(labels), tuple(base_entries))

    augmented = {}
    for number, (word, remainder) in enumerate(sorted(bad.items())):
        extra_row = min(remainder)
        rows = pivot_rows + (extra_row,)
        entries = []
        for row_number, row in enumerate(rows):
            for column_number, label in enumerate(labels):
                polynomial = polynomial_columns[label].get(row, {})
                if polynomial:
                    entries.append((row_number, column_number, polynomial))
            polynomial = polynomial_residual.get(word, {}).get(row, {})
            if polynomial:
                entries.append((row_number, len(labels), polynomial))
        augmented[f"aug{number}"] = (
            len(labels) + 1,
            len(labels) + 1,
            tuple(entries),
        )
    require(augmented, "candidate has no augmented witness matrix")
    return len(labels), bad, base, augmented


def main() -> None:
    palette = load_palette()
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
    for block in range(35):
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
            rank, bad, base, augmented = witness_matrices(
                bounded, data, case[0]
            )
            require(
                rank == determinant[0] and bad == determinant[2],
                "reconstructed audited witness changed",
            )
            winning_names = tuple(
                name
                for name, factors in determinant[3].items()
                if name.startswith("aug") and palette.torus_monomial(factors)
            )
            require(
                palette.torus_monomial(determinant[3]["base"])
                and winning_names,
                "audited global witness changed",
            )
            for name in winning_names:
                key = canonical_matrix_pair(base, augmented[name])
                cache[key].append((block, case[0], name))
                library_keys[key] += 1
            library_cases += 1
    require(library_cases == 1_758, "audited monomial library changed")

    target_records = Counter()
    target_frontiers = []
    transfer_hits = []
    fresh_records = []
    fresh_exceptions = []
    for block in range(35, 49):
        records, affine_cases, torus_cases = torus_pair_block(
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
            _rank, _bad, base, augmented = witness_matrices(
                bounded, data, case[0]
            )
            hit = next(
                (
                    (name, cache[key])
                    for name, matrix in augmented.items()
                    if (key := canonical_matrix_pair(base, matrix)) in cache
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
                tuple(map(bounded.Q, SAMPLE)),
            )
            fresh_records.append((block, case, determinant))
            winning_names = tuple(
                name
                for name, factors in determinant[3].items()
                if name.startswith("aug") and palette.torus_monomial(factors)
            )
            if palette.torus_monomial(determinant[3]["base"]) and winning_names:
                rank, bad, base, augmented = witness_matrices(
                    bounded, data, case[0]
                )
                require(
                    rank == determinant[0] and bad == determinant[2],
                    "fresh witness reconstruction changed",
                )
                for name in winning_names:
                    key = canonical_matrix_pair(base, augmented[name])
                    cache[key].append((block, case[0], name))
                continue
            fresh_exceptions.append((block, case, determinant))

    audited_supports = 14 * 59_640
    new_supports = sum(
        count
        for (grade_count, _status), count in target_records.items()
        if grade_count >= 3
    )
    require(len(library_keys) == 3_014, "exact matrix-library size changed")
    require(
        tuple(target_frontiers)
        == (
            (70, 0), (0, 0), (0, 0), (70, 0), (0, 0), (0, 0),
            (70, 0), (0, 0), (207, 75), (70, 27), (207, 72),
            (0, 0), (70, 0), (0, 0),
        ),
        "target affine/torus frontier changed",
    )
    require(
        (audited_supports, new_supports) == (834_960, 834_960),
        "target support count changed",
    )
    require(
        (len(transfer_hits), len(fresh_records), len(fresh_exceptions))
        == (53, 121, 23),
        "transfer hit/miss frontier changed",
    )

    exception_census = Counter(
        tuple(sorted(palette.non_torus_factors(det[3]["base"])))
        for _block, _case, det in fresh_exceptions
    )
    require(
        exception_census
        == Counter(
            {
                ("bc+1",): 12,
                ("bd+1",): 6,
                ("bd+1", "bd-1"): 4,
                ("be+1",): 1,
            }
        ),
        "fresh divisor census changed",
    )
    divisor_samples = {
        "be+1": (2, 1, 3, 5, -1),
        "bc+1": (2, 1, -1, 3, 5),
        "bd+1": (2, 1, 3, -1, 5),
        "bd-1": (2, 1, 3, 1, 5),
    }
    special_samples = {}
    for _block, case, determinant in fresh_exceptions:
        divisors = palette.non_torus_factors(determinant[3]["base"])
        require(divisors <= set(divisor_samples), "new divisor type appeared")
        special_samples[case[0]] = {
            divisor: divisor_samples[divisor] for divisor in divisors
        }
    divisor_certificates = palette.close_exceptional_divisors(
        five,
        bounded,
        data,
        tuple((case, determinant)
              for _block, case, determinant in fresh_exceptions),
        special_samples,
    )
    require(len(divisor_certificates) == 27, "fresh divisor charts changed")

    closed_cumulative = 2_082_696 + new_supports
    remaining = 11_614_176 - closed_cumulative
    require(
        (closed_cumulative, remaining) == (2_917_656, 8_696_520),
        "cumulative frontier arithmetic changed",
    )
    print("N=10 five-cross exact-matrix transfer cache: exact frontier")
    print(f"audited monomial library cases: {library_cases}")
    print(f"exact canonical matrix keys: {len(library_keys)}")
    print(f"next pair blocks: 14; supports: {audited_supports}")
    print(f"new grade-3-to-6 supports: {new_supports}")
    print(f"exact matrix transfer hits: {len(transfer_hits)}")
    print(f"fresh literal determinant records: {len(fresh_records)}")
    print(f"fresh non-monomial exceptions: {len(fresh_exceptions)}")
    print(f"fresh divisor charts: {len(divisor_certificates)}")
    print("literal survivors in the fourteen-block frontier: 0")
    print(f"cumulative closed new grade-3-to-6 supports: {closed_cumulative}")
    print(f"remaining unaudited grade-3-to-6 supports: {remaining}")


if __name__ == "__main__":
    main()
