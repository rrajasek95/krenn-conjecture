#!/usr/bin/env python3
"""Exact invariant degree-seven unit for the sharp one-bad packet.

The full constant-connected Macaulay component has 70,398 target monomials
and 110,898 source rows.  Its order-eight packet automorphism group fixes the
unit.  Reynolds averaging therefore reduces unit membership to the invariant
source image.  This checker builds that image exactly, proves a modular rank
lower bound, constructs a full rational annihilator basis, and verifies that
every annihilator kills the unit coordinate.  Hence the unit lies in the
ordinary degree-seven row space over Q.
"""

from __future__ import annotations

from collections import defaultdict
from functools import reduce
from math import gcd
from hashlib import sha256
import json
from pathlib import Path

from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix

import verify_n8_one_bad_whole_packet_macaulay as BASE


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "computations/verify_n8_one_bad_whole_packet_macaulay.py"
BASE_SHA256 = "a2ff6af9d39aaed2ad720415273cf9643e883debc1d93151cd8ebb63026667ea"
EXPECTED_DIGEST = "29a20c51764a9d8d714938ffca134438c4f198f881161ce021add86385470dab"
PRIME = 1_000_003

GROUP = (
    ((0, 1, 2, 3, 4, 5), (0, 1, 2)),
    ((0, 1, 3, 2, 5, 4), (1, 0, 2)),
    ((0, 1, 4, 5, 2, 3), (0, 1, 2)),
    ((0, 1, 5, 4, 3, 2), (1, 0, 2)),
    ((1, 0, 2, 3, 4, 5), (0, 1, 2)),
    ((1, 0, 3, 2, 5, 4), (1, 0, 2)),
    ((1, 0, 4, 5, 2, 3), (0, 1, 2)),
    ((1, 0, 5, 4, 3, 2), (1, 0, 2)),
)


def variable_maps():
    return tuple(
        tuple(
            BASE.variable(site_permutation[u], site_permutation[v],
                          colour_permutation[a], colour_permutation[b])
            for u, v, a, b in BASE.VARIABLE_DATA
        )
        for site_permutation, colour_permutation in GROUP
    )


def act(monomial, variable_map):
    return tuple(sorted(variable_map[index] for index in monomial))


def canonical_generators(generators):
    return tuple(sorted(
        tuple(sorted(generator.items())) for generator in generators
    ))


def verify_group(variable_maps_):
    generators = BASE.packet_generators(0)
    canonical = canonical_generators(generators)
    for variable_map in variable_maps_:
        image = [
            {act(monomial, variable_map): coefficient
             for monomial, coefficient in generator.items()}
            for generator in generators
        ]
        if canonical_generators(image) != canonical:
            raise RuntimeError("the displayed order-eight group is not an automorphism")


def primitive_row(entries):
    values = [coefficient for _column, coefficient in entries]
    divisor = reduce(gcd, (abs(value) for value in values), 0)
    entries = tuple((column, coefficient // divisor)
                    for column, coefficient in entries)
    if entries[-1][1] < 0:
        entries = tuple((column, -coefficient)
                        for column, coefficient in entries)
    return entries


def build():
    maps = variable_maps()
    verify_group(maps)
    columns, row_map = BASE.constant_component(0, 7)

    representative = {}
    orbit_size = {}
    for monomial in columns:
        if monomial in representative:
            continue
        orbit = {act(monomial, variable_map) for variable_map in maps}
        if not orbit <= columns:
            raise RuntimeError("the D=7 component is not group-stable")
        canonical = min(orbit)
        for image in orbit:
            representative[image] = canonical
        orbit_size[canonical] = len(orbit)

    representatives = tuple(sorted(orbit_size, key=lambda item: (len(item), item)))
    index = {monomial: position
             for position, monomial in enumerate(representatives)}
    compressed = set()
    for source in row_map.values():
        totals = defaultdict(int)
        for monomial, coefficient in source.items():
            totals[representative[monomial]] += coefficient
        entries = tuple(sorted(
            (index[monomial], coefficient * (len(GROUP) // orbit_size[monomial]))
            for monomial, coefficient in totals.items() if coefficient
        ))
        if entries:
            compressed.add(primitive_row(entries))
    rows = tuple(sorted(compressed, key=lambda row: (len(row), row)))
    return representatives, rows, len(columns), len(row_map)


def modular_rank(rows):
    basis = {}
    for source in rows:
        row = {column: coefficient % PRIME
               for column, coefficient in source if coefficient % PRIME}
        while row:
            pivot = max(row)
            old = basis.get(pivot)
            if old is None:
                inverse = pow(row[pivot], -1, PRIME)
                basis[pivot] = {
                    column: coefficient * inverse % PRIME
                    for column, coefficient in row.items()
                }
                break
            scale = row[pivot]
            for column, coefficient in old.items():
                value = (row.get(column, 0) - scale * coefficient) % PRIME
                if value:
                    row[column] = value
                else:
                    row.pop(column, None)
    return len(basis)


def exact_annihilator_audit(representatives, rows):
    entries = {
        row_index: {column: ZZ(coefficient) for column, coefficient in row}
        for row_index, row in enumerate(rows)
    }
    matrix = DomainMatrix.from_dod(
        entries, (len(rows), len(representatives)), ZZ
    ).to_field()
    annihilators = matrix.nullspace()
    require(annihilators.shape == (452, 9411),
            ("rational annihilator shape", annihilators.shape))
    annihilator_rows = annihilators.to_dod()
    require(all(0 not in row for row in annihilator_rows.values()),
            "a rational annihilator detects the unit coordinate")

    # DomainMatrix returns one null vector per free column.  Check
    # independence without rerunning a second large RREF: every returned row
    # must have a coordinate absent from all other returned rows.
    column_support = defaultdict(set)
    for annihilator_index, row in annihilator_rows.items():
        for column in row:
            column_support[column].add(annihilator_index)
    private_rows = {
        next(iter(indices)) for indices in column_support.values()
        if len(indices) == 1
    }
    require(len(private_rows) == 452,
            "rational annihilator rows lost their private free coordinates")
    annihilator_rank = len(private_rows)

    # Independent exact replay of A*N^T=0 using the sparse row ledgers.
    by_column = defaultdict(list)
    for annihilator_index, row in annihilator_rows.items():
        for column, coefficient in row.items():
            by_column[column].append((annihilator_index, coefficient))
    for source in rows:
        values = defaultdict(lambda: 0)
        for column, coefficient in source:
            for annihilator_index, right in by_column.get(column, ()):
                values[annihilator_index] += coefficient * right
        require(all(not value for value in values.values()),
                "the returned annihilator basis does not kill the source image")
    return {
        "rational_annihilator_dimension": annihilators.shape[0],
        "annihilator_rank": annihilator_rank,
        "unit_coordinate_nonzero_annihilators": 0,
    }


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    base_hash = sha256(BASE_PATH.read_bytes()).hexdigest()
    require(base_hash == BASE_SHA256, ("base checker changed", base_hash))
    representatives, rows, raw_columns, raw_rows = build()
    orbit_histogram = defaultdict(int)
    maps = variable_maps()
    for representative in representatives:
        orbit_histogram[len({act(representative, item) for item in maps})] += 1
    require((raw_columns, raw_rows) == (70398, 110898),
            "raw degree-seven frontier changed")
    require(len(representatives) == 9411,
            "invariant target orbit count changed")
    require(dict(orbit_histogram) == {1: 40, 2: 139, 4: 944, 8: 8288},
            ("target orbit histogram", dict(orbit_histogram)))
    require(len(rows) == 14651 and sum(map(len, rows)) == 62323,
            "primitive Reynolds row ledger changed")
    rank_mod_prime = modular_rank(rows)
    require(rank_mod_prime == 8959, ("modular rank", rank_mod_prime))
    exact = exact_annihilator_audit(representatives, rows)

    # The modular rank is a lower bound on rank_Q.  The 452 independent
    # rational annihilators give rank_Q <= 9411-452=8959, so they span the
    # full annihilator.  Since all have zero unit coordinate, the unit lies
    # in the rational row image.
    require(rank_mod_prime + exact["rational_annihilator_dimension"]
            == len(representatives), "rank/nullity closure changed")
    BASE.orbit_isomorphism_check()
    ledger = {
        "base": {"path": str(BASE_PATH.relative_to(ROOT)), "sha256": base_hash},
        "group_order": len(GROUP),
        "raw_component": {"columns": raw_columns, "rows": raw_rows},
        "invariant_target_orbits": len(representatives),
        "target_orbit_histogram": dict(sorted(orbit_histogram.items())),
        "primitive_reynolds_rows": len(rows),
        "primitive_reynolds_nonzeros": sum(map(len, rows)),
        "prime": PRIME,
        "rank_mod_prime": rank_mod_prime,
        "exact": exact,
        "rank_Q": rank_mod_prime,
        "augmented_rank_Q": rank_mod_prime,
        "certificate_degree": 7,
        "two_sharp_orbits": "isomorphic by site swap (2 4)",
        "verdict": "the unrestricted fixed-star one-bad scalar ideal is unit in degree seven over Q",
        "scope": "independent algebraic closure of an already cap-closed fixed-star packet; not arbitrary multisite-star concentration",
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger digest", digest))
    print("N=8 one-bad invariant D7 unit: PASS")
    print("raw columns/rows: 70398 / 110898")
    print("invariant columns/rows/nonzeros: 9411 / 14651 / 62323")
    print("rank_Q=augmented_rank_Q=8959; annihilator dimension=452")
    print("both sharp fixed-star packets are unit at certificate degree 7")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
