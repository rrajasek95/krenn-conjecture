#!/usr/bin/env python3
"""Clean-room audit of the sole-defect two-physical-pair obstruction.

No primary checker or primary ledger is imported.  The low-level algebra
comes from the companion clean-room distinct-lift audit; this file rebuilds
the normalization census, 1,365 family systems, 65 group orbits, qF kernels,
and unsaturated q^[2]-F ideals with the independent coordinate/order choices
documented there.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product

from audit_sole_defect_distinct_common_power_independent import (
    GOOD_PERMS,
    PAIRS,
    SITES,
    all_cells,
    lift_terms,
    linear_kernel,
    local_model,
    q2_generators,
    right_pivot_rref,
    singular_unit,
)


def coefficient_character(pair):
    absent = frozenset(pair)
    return tuple(int(site not in absent) for site in (1, 2, 3, 4, 5))


def normalization_census():
    """Find a unimodular good-site minor for every distinct pair choice."""
    minor_counts = Counter()
    witnesses = {}
    for first, second in combinations(PAIRS, 2):
        row_first = coefficient_character(first)
        row_second = coefficient_character(second)
        good = (1, 2, 3, 4, 5)
        unimodular = []
        for left, right in combinations(range(5), 2):
            determinant = (
                row_first[left] * row_second[right]
                - row_first[right] * row_second[left]
            )
            if abs(determinant) == 1:
                unimodular.append((good[left], good[right], determinant))
        assert unimodular, (first, second)
        witnesses[(first, second)] = max(unimodular)
        minor_counts[len(unimodular)] += 1

        # The explicit ratio/common construction is recovered from any
        # x in the good symmetric difference and y outside the union.
        symmetric_good = (set(first) ^ set(second)) & set(good)
        outside_good = set(good) - set(first) - set(second)
        assert symmetric_good and outside_good
        assert any(
            abs(
                row_first[x - 1] * row_second[y - 1]
                - row_first[y - 1] * row_second[x - 1]
            ) == 1
            for x in symmetric_good for y in outside_good
        )
    assert len(witnesses) == 105
    return witnesses, minor_counts


def raw_family_systems():
    """The 13 allowed systems on each unordered physical-pair set."""
    count_by_profile = Counter()
    for first, second in combinations(PAIRS, 2):
        double = tuple(sorted((first, second), reverse=True))
        choices = ((first,), (second,), double)
        local_count = 0
        for families in product(choices, repeat=3):
            union = frozenset().union(*(frozenset(family) for family in families))
            if union != frozenset((first, second)):
                continue
            if any(
                len(families[r]) == len(families[s]) == 1
                and families[r] == families[s]
                for r, s in combinations(range(3), 2)
            ):
                continue
            profile = tuple(sorted(map(len, families), reverse=True))
            count_by_profile[profile] += 1
            local_count += 1
            yield tuple(tuple(family) for family in families)
        assert local_count == 13
    assert count_by_profile == Counter({
        (2, 2, 2): 105,
        (2, 2, 1): 630,
        (2, 1, 1): 630,
    })


def mapped_edge(edge, site_permutation):
    return tuple(sorted(
        (site_permutation[edge[0]], site_permutation[edge[1]]), reverse=True
    ))


def field_orders(kind):
    if kind == "coincident":
        return ((0, 1, 2), (2, 1, 0))
    return tuple(permutations((0, 1, 2)))


def canonical(families, kind):
    # Maximal, not minimal, representatives and descending family members.
    return max(
        tuple(
            tuple(sorted(
                (mapped_edge(edge, site_permutation)
                 for edge in families[old_field]), reverse=True
            ))
            for old_field in order
        )
        for site_permutation in GOOD_PERMS
        for order in field_orders(kind)
    )


def orbit_data(kind):
    census = Counter(canonical(families, kind) for families in raw_family_systems())
    assert sum(census.values()) == 1365
    assert len(census) == (31 if kind == "coincident" else 17)
    return tuple(sorted(census, reverse=True)), census


def target_terms(families, bad_vectors):
    output = defaultdict(Fraction)
    for field in (2, 1, 0):
        for pair in reversed(families[field]):
            for word, coefficient in lift_terms(pair, field, bad_vectors).items():
                output[word] += coefficient
    return {word: coefficient for word, coefficient in output.items() if coefficient}


def qf_matrix(families, bad_vectors, cells):
    """Literal generic multiplication, including collection across lifts."""
    index = {cell: column for column, cell in enumerate(cells)}
    rows = defaultdict(lambda: defaultdict(Fraction))
    for field in (2, 1, 0):
        for pair in reversed(families[field]):
            for lift_word, coefficient in lift_terms(pair, field, bad_vectors).items():
                occupied = frozenset(site for site, coordinate in enumerate(lift_word)
                                     if coordinate is not None)
                for cell in cells:
                    u, v, cu, cv = cell
                    if u in occupied or v in occupied:
                        continue
                    word = list(lift_word)
                    word[u], word[v] = cu, cv
                    rows[tuple(word)][index[cell]] += coefficient
    return tuple(
        {column: coefficient for column, coefficient in rows[word].items()
         if coefficient}
        for word in sorted(rows, reverse=True)
        if any(rows[word].values())
    )


def ledger_hash(families, cells, rows, pivots, generators):
    digest = hashlib.sha256()
    digest.update(repr(families).encode("ascii"))
    for title, stream in (
        (b"CELLS", cells),
        (b"ROWS", rows),
        (b"PIVOTS", tuple(pivots.items())),
        (b"GENERATORS", generators),
    ):
        digest.update(b"\n" + title + b"\n")
        for item in stream:
            if isinstance(item, dict):
                item = tuple(sorted(item.items(), reverse=True))
            digest.update(repr(item).encode("ascii") + b"\n")
    return digest.hexdigest()


def build_case(kind, families):
    dims, bad_vectors = local_model(kind)
    cells = all_cells(dims)
    rows = qf_matrix(families, bad_vectors, cells)
    pivots = right_pivot_rref(rows)
    free, expressions = linear_kernel(cells, pivots)
    target = target_terms(families, bad_vectors)
    generators = q2_generators(dims, expressions, target)
    digest = ledger_hash(families, cells, rows, pivots, generators)
    return dims, cells, rows, pivots, free, generators, digest


EXPECTED_COMBINED = {
    "circuit": "7b55e9a776e9cda65ba0921b9deb97bfee6f6c2ec60c7832d2cc0444e01cae39",
    "coincident": "4d1670d84f3875602ec140cf6e7b9245f79ed76ec799894a1d6bc5855640bc33",
    "rank1": "b512dc69f4514173f6c77528e2ecf295d626b68be051be6065cadeae98c361e0",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", action="append",
                        choices=("circuit", "coincident", "rank1"))
    parser.add_argument("--case", action="append", type=int)
    parser.add_argument("--ledger-only", action="store_true")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()

    witnesses, minor_counts = normalization_census()
    print("normalization configurations", len(witnesses),
          "unimodular-minor count distribution", dict(sorted(minor_counts.items())),
          flush=True)
    total_units = 0
    for kind in args.kind or ("rank1", "coincident", "circuit"):
        representatives, census = orbit_data(kind)
        print(kind, "orbits", len(representatives), "systems", sum(census.values()),
              "orbit sizes", dict(sorted(Counter(census.values()).items())), flush=True)
        selected = args.case if args.case is not None else range(len(representatives))
        combined = hashlib.sha256()
        for case in selected:
            families = representatives[case]
            dims, cells, rows, pivots, free, generators, digest = build_case(
                kind, families
            )
            status, seconds, stderr = ("SKIPPED", 0.0, "")
            if not args.ledger_only:
                status, seconds, stderr = singular_unit(len(free), generators, args.timeout)
                assert status == "UNIT", (kind, case, status, stderr)
                total_units += 1
            print({
                "kind": kind, "case": case, "families": families, "dims": dims,
                "cells": len(cells), "rows": len(rows), "rank": len(pivots),
                "nullity": len(free), "generators": len(generators),
                "ledger": digest, "status": status, "seconds": round(seconds, 3),
            }, flush=True)
            combined.update(f"{case}:{digest}\n".encode("ascii"))
        combined_digest = combined.hexdigest()
        print(kind, "independent combined ledger sha256", combined_digest, flush=True)
        if args.case is None and EXPECTED_COMBINED[kind]:
            assert combined_digest == EXPECTED_COMBINED[kind]

    if not args.ledger_only and args.case is None and args.kind is None:
        assert total_units == 65
    print("independent sole-defect two-pair audit: PASS", flush=True)


if __name__ == "__main__":
    main()
