#!/usr/bin/env python3
"""Full exact cut census on the occupied-modulus zero stratum.

This follows the twelve five-cross supports whose selected positive-degree
Fitting jump dies when the anchored old cell 23;21 is deleted.  It rebuilds
the literal N=10 source at the exact cross torus point and checks every
adjacent 3|7 cut, both crossing sectors, pure anchors, and target defects.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

import verify_n10_five_cross_occupied_modulus_incidence as incidence


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def tensor_add(module, tensor, word, coefficient):
    module.add_term(tensor, word, coefficient)


def crossing_sector(module, vertices, c_set, crossing_count, cells):
    left = set(c_set)
    tensor = {}
    for matching, word, coefficient in module.matching_terms(vertices, cells):
        crossings = sum((first in left) != (second in left) for first, second in matching)
        if crossings == crossing_count:
            tensor_add(module, tensor, word, coefficient)
    return tensor


def cut_record(data, cells, cut):
    module = data["module"]
    forced_pair = data["forced_pair"]
    vertices = data["provenance"].B10
    u_set = tuple(vertex for vertex in module.S if vertex != cut) + (8, 9)
    c_set = (cut, 6, 7)
    columns = forced_pair.insertion_columns(module, u_set, cells)
    basis = module.rational_basis(list(columns.values()))
    tensor = module.matching_tensor(vertices, cells)
    residual = forced_pair.tensor_difference(
        tensor, forced_pair.delta_tensor(vertices)
    )
    one_cross = crossing_sector(module, vertices, c_set, 1, cells)
    residual_rows = forced_pair.flatten_rows(
        residual, vertices, c_set, u_set
    )
    one_rows = forced_pair.flatten_rows(
        one_cross, vertices, c_set, u_set
    )
    residual_bad = tuple(
        sorted(
            (
                word,
                tuple(
                    sorted(
                        data["two_cell"].quotient_remainder(row, basis).items()
                    )
                ),
            )
            for word, row in residual_rows.items()
            if not module.rational_member(row, basis)
        )
    )
    one_bad = tuple(
        sorted(
            word
            for word, row in one_rows.items()
            if not module.rational_member(row, basis)
        )
    )
    constants = tuple(
        {
            forced_pair.word_index((colour,) * len(u_set)): Q(1)
        }
        for colour in range(3)
    )
    augmented = module.rational_basis(list(columns.values()) + list(constants))
    return {
        "rank": len(basis),
        "defect": len(augmented) - len(basis),
        "residual_bad": residual_bad,
        "one_bad": one_bad,
        "active": not residual_bad and not one_bad and len(augmented) > len(basis),
    }


def full_source(data, deleted_old, support, weights):
    module = data["module"]
    lifted = data["forced_pair"].lift_cells(module, deleted_old)
    return data["provenance"].add_weighted_coordinates(
        module, lifted, tuple(zip(support, weights))
    )


def main() -> None:
    dependence, matrix_cache, data, cases = incidence.setup()
    module = data["module"]
    sample = tuple(map(Q, matrix_cache.SAMPLE))
    deleted_old = incidence.add_weighted_old_coordinates(
        module,
        data["base"],
        ((incidence.OCCUPIED_MODULUS, Q(-1)),),
    )

    support_jump = Counter()
    for support, witnesses in cases.items():
        for metadata in witnesses:
            columns = dependence.changed_columns(
                data, support, metadata, deleted_old, sample
            )
            base_rank = incidence.column_rank(module, columns[:-1])
            augmented_rank = incidence.column_rank(module, columns)
            support_jump[support] += augmented_rank > base_rank
    lost_supports = tuple(sorted(support for support, jump in support_jump.items() if not jump))
    require(len(lost_supports) == 12, "zero-stratum lost-support count changed")

    active_cut_census = Counter()
    pure_census = Counter()
    mixed_count_census = Counter()
    cut_signature_census = {cut: Counter() for cut in module.S}
    first_record = None
    full_records = []
    for support in lost_supports:
        cells = full_source(data, deleted_old, support, sample)
        tensor = module.matching_tensor(data["provenance"].B10, cells)
        pure = tuple(
            tensor.get((colour,) * 10, Q(0))
            for colour in range(3)
        )
        mixed_count = sum(len(set(word)) > 1 for word in tensor)
        cut_records = tuple((cut, cut_record(data, cells, cut)) for cut in module.S)
        active_cuts = tuple(cut for cut, record in cut_records if record["active"])
        pure_census[pure] += 1
        mixed_count_census[mixed_count] += 1
        active_cut_census[active_cuts] += 1
        for cut, record in cut_records:
            cut_signature_census[cut][
                (
                    record["rank"],
                    record["defect"],
                    len(record["one_bad"]),
                    len(record["residual_bad"]),
                )
            ] += 1
        compact = (
            support,
            pure,
            mixed_count,
            tuple(
                (
                    cut,
                    record["rank"],
                    record["defect"],
                    len(record["one_bad"]),
                    len(record["residual_bad"]),
                )
                for cut, record in cut_records
            ),
        )
        full_records.append(compact)
        if first_record is None:
            first_record = compact

    require(
        pure_census == Counter({(Q(1), Q(1), Q(1)): 12}),
        "zero-stratum pure-anchor census changed",
    )
    require(
        mixed_count_census == Counter({48: 6, 40: 6}),
        "zero-stratum mixed-count census changed",
    )
    require(
        active_cut_census == Counter({(): 12}),
        "a zero-stratum support acquired a complete cut",
    )
    expected_cut_signatures = {
        0: Counter({(16, 3, 0, 7): 4, (18, 3, 0, 6): 4, (16, 3, 0, 5): 2, (18, 3, 0, 7): 2}),
        1: Counter({(21, 3, 0, 6): 4, (21, 3, 0, 7): 4, (21, 3, 0, 8): 4}),
        2: Counter({(21, 3, 0, 4): 12}),
        3: Counter({(21, 3, 0, 6): 8, (21, 3, 0, 5): 4}),
        4: Counter({(21, 3, 0, 8): 6, (21, 3, 0, 5): 2, (21, 3, 0, 6): 2, (21, 3, 0, 9): 2}),
        5: Counter({(18, 3, 0, 6): 4, (20, 3, 0, 7): 4, (18, 3, 0, 5): 2, (20, 3, 0, 5): 2}),
    }
    require(cut_signature_census == expected_cut_signatures, "zero-stratum cut signatures changed")

    print("N=10 occupied-modulus zero-stratum full cut audit: exact frontier")
    print(f"lost positive-degree supports: {len(lost_supports)}")
    print(f"pure-anchor census: {dict(sorted(pure_census.items(), key=repr))}")
    print(f"mixed tensor-count census: {dict(sorted(mixed_count_census.items()))}")
    print(f"active-cut census: {dict(sorted(active_cut_census.items(), key=repr))}")
    print(
        "cut signatures (rank,defect,one-bad,residual-bad): "
        f"{ {cut: dict(sorted(census.items())) for cut, census in cut_signature_census.items()} }"
    )
    print(f"first full record: {first_record}")
    first_cells = full_source(data, deleted_old, lost_supports[0], sample)
    first_cut_two = cut_record(data, first_cells, 2)
    require(
        first_cut_two["residual_bad"][0]
        == (
            (0, 0, 0),
            (
                (4, Q(1)),
                (8, Q(1)),
                (1008, Q(3)),
                (1010, Q(5)),
                (1014, Q(6)),
                (1016, Q(10)),
            ),
        ),
        "first zero-stratum radical witness changed",
    )
    print(f"first cut-2 radical witness: {first_cut_two['residual_bad'][0]}")
    print("scope: exact cross weights (1,2,3,5,7), not the full cross torus")


if __name__ == "__main__":
    main()
