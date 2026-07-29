#!/usr/bin/env python3
"""Exact two-physical-pair common-power audit with one deficient site.

Each of three nonempty field families is one of {P}, {Q}, or {P,Q};
same-singleton pairs of fields are omitted because the response singleton
lemma already excludes them.  The script constructs all site/field orbits,
the complete qF=0 kernel, and the unsaturated q^[2]=F ideal over QQ.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import cache
import hashlib
from itertools import combinations, permutations, product
import shutil
import subprocess
import time

from verify_sole_defect_distinct_common_power import (
    U,
    EDGES,
    add,
    field_vector,
    linear_expression,
    local_data,
    multiply,
    pure_lift,
    q_cells,
    sparse_rref,
)


EXPECTED_COMBINED = {
    "circuit": "160c496ed05d7ae56180c07fd59eb8b2e3fd94b07d4426c32d8e4417827039a6",
    "coincident": "0a8cd248765959003754da8ed277b71e571396eb6fcbf8aa3e23d85b7e4e805b",
    "rank1": "c25cbabf59c739dd062e4dcc98246a83a98a1d3d17457433e4a42e62007ed068",
}


def normalization_sites(first, second):
    """Good sites giving independent ratio/common coefficient rescalings."""
    good = set(range(1, 6))
    good_difference = (set(first) ^ set(second)) & good
    good_outside = good - set(first) - set(second)
    assert good_difference and good_outside
    x = min(good_difference)
    # Orient A to contain x and B not to contain x.
    oriented = (first, second) if x in first else (second, first)
    return oriented, x, min(good_outside)


def audit_coefficient_normalization():
    for first, second in combinations(EDGES, 2):
        (a, b), x, y = normalization_sites(first, second)
        assert x in a and x not in b
        assert y not in a and y not in b
        assert x != 0 and y != 0 and x != y
    return len(tuple(combinations(EDGES, 2)))


def map_edge(edge, site_permutation):
    return tuple(sorted((site_permutation[edge[0]], site_permutation[edge[1]])))


def field_orders(kind):
    if kind == "coincident":
        return ((0, 1, 2), (2, 1, 0))
    return tuple(permutations(range(3)))


def canonical(families, kind):
    site_permutations = ((0,) + tail for tail in permutations(range(1, 6)))
    return min(
        tuple(
            tuple(sorted(map_edge(edge, site_permutation) for edge in families[old]))
            for old in order
        )
        for site_permutation in site_permutations
        for order in field_orders(kind)
    )


def labelled_family_systems():
    for first, second in combinations(EDGES, 2):
        choices = ((first,), (second,), tuple(sorted((first, second))))
        for families in product(choices, repeat=3):
            if set().union(*map(set, families)) != {first, second}:
                continue
            same_singleton = any(
                families[r] == families[s] and len(families[r]) == 1
                for r, s in combinations(range(3), 2)
            )
            if not same_singleton:
                yield tuple(tuple(family) for family in families)


@cache
def orbit_census(kind):
    census = Counter(canonical(families, kind) for families in labelled_family_systems())
    assert sum(census.values()) == 105 * 13 == 1365
    expected_orbits = 31 if kind == "coincident" else 17
    assert len(census) == expected_orbits
    return census


@cache
def representatives(kind):
    return tuple(sorted(orbit_census(kind)))


def f_coefficients(families, dims, bad_vectors):
    by_support = Counter()
    for colour, family in enumerate(families):
        for pair in family:
            for local_word, coefficient in pure_lift(
                pair, colour, dims, bad_vectors
            ).items():
                support = tuple(site for site, coordinate in local_word)
                word = tuple(coordinate for site, coordinate in local_word)
                by_support[support, word] += coefficient
    return {key: value for key, value in by_support.items() if value}


def qf_rows(families, dims, bad_vectors, cell_index):
    rows = {}
    for colour, family in enumerate(families):
        for pair in family:
            lift = pure_lift(pair, colour, dims, bad_vectors)
            u, v = pair
            for cu in range(dims[u]):
                for cv in range(dims[v]):
                    column = cell_index[(pair, cu, cv)]
                    for local_word, coefficient in lift.items():
                        full = dict(local_word)
                        full[u], full[v] = cu, cv
                        word = tuple(full[site] for site in U)
                        row = rows.setdefault(word, {})
                        row[column] = row.get(column, Fraction(0)) + coefficient
    return tuple(
        {column: value for column, value in row.items() if value}
        for row in rows.values() if any(row.values())
    )


def build(case, kind):
    families = representatives(kind)[case]
    dims, bad_vectors = local_data(kind)
    cells = q_cells(dims)
    cell_index = {cell: index for index, cell in enumerate(cells)}
    rows = qf_rows(families, dims, bad_vectors, cell_index)
    pivots = sparse_rref(rows)
    free = tuple(index for index in range(len(cells)) if index not in pivots)
    variables = tuple(f"t{i}" for i in range(len(free)))
    free_variable = dict(zip(free, variables))
    expressions = {}
    for column, cell in enumerate(cells):
        if column in free_variable:
            expressions[cell] = free_variable[column]
        else:
            row = pivots[column]
            expressions[cell] = linear_expression(tuple(
                (free_variable[key], -value)
                for key, value in row.items() if key != column
            ))

    target = f_coefficients(families, dims, bad_vectors)
    generators = []
    matchings = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    for sites in combinations(U, 4):
        ranges = tuple(range(dims[site]) for site in sites)
        for word in product(*ranges):
            terms = []
            for i, j, k, l in matchings:
                left_sites = tuple(sorted((sites[i], sites[j])))
                right_sites = tuple(sorted((sites[k], sites[l])))
                left_word = (
                    (word[i], word[j]) if sites[i] < sites[j]
                    else (word[j], word[i])
                )
                right_word = (
                    (word[k], word[l]) if sites[k] < sites[l]
                    else (word[l], word[k])
                )
                terms.append(multiply(
                    expressions[(left_sites, *left_word)],
                    expressions[(right_sites, *right_word)],
                ))
            polynomial = add(*terms)
            constant = target.get((sites, word), 0)
            if constant:
                polynomial = add(polynomial, str(-constant))
            if polynomial != "0":
                generators.append(polynomial)
    return families, dims, cells, rows, pivots, variables, tuple(generators)


def ledger_digest(families, cells, rows, pivots, generators):
    digest = hashlib.sha256()
    digest.update(repr(families).encode("ascii"))
    digest.update(b"\nCELLS\n")
    digest.update(repr(cells).encode("ascii"))
    digest.update(b"\nROWS\n")
    for row in rows:
        digest.update(repr(tuple(sorted(row.items()))).encode("ascii"))
        digest.update(b"\n")
    digest.update(b"RREF\n")
    for pivot, row in pivots.items():
        digest.update(repr((pivot, tuple(sorted(row.items())))).encode("ascii"))
        digest.update(b"\n")
    digest.update(b"GENERATORS\n")
    for generator in generators:
        digest.update(generator.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def run(case, kind, timeout, run_ideal=True):
    families, dims, cells, rows, pivots, variables, generators = build(case, kind)
    digest = ledger_digest(families, cells, rows, pivots, generators)
    status = "SKIPPED"
    elapsed = 0.0
    stderr = ""
    if run_ideal:
        executable = shutil.which("Singular")
        if executable is None:
            raise SystemExit("Singular is required")
        program = (
            f"ring r=0,({','.join(variables)}),dp;\n"
            f"ideal I={','.join(generators)};\n"
            "ideal G=slimgb(I);\n"
            'print("SIZE");print(size(G));print("FIRST");print(G[1]);\n'
        )
        started = time.monotonic()
        result = subprocess.run(
            (executable, "-q"), input=program, text=True, capture_output=True,
            timeout=timeout,
        )
        elapsed = time.monotonic() - started
        stderr = result.stderr
        output = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
        status = "ERROR"
        if result.returncode == 0 and "SIZE" in output and "FIRST" in output:
            size = output[output.index("SIZE") + 1]
            first = output[output.index("FIRST") + 1]
            status = "UNIT" if size == first == "1" else f"NONUNIT:{size}:{first}"
    return {
        "case": case,
        "kind": kind,
        "families": families,
        "dims": dims,
        "cells": len(cells),
        "rows": len(rows),
        "rank": len(pivots),
        "nullity": len(variables),
        "generators": len(generators),
        "sha256": digest,
        "status": status,
        "seconds": elapsed,
        "stderr": stderr,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, action="append")
    parser.add_argument(
        "--kind", choices=("circuit", "coincident", "rank1"), action="append"
    )
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--ledger-only", action="store_true")
    args = parser.parse_args()

    print(
        "two-pair coefficient-normalization incidences:",
        audit_coefficient_normalization(),
        flush=True,
    )
    for kind in args.kind or ("circuit", "coincident", "rank1"):
        census = orbit_census(kind)
        reps = tuple(sorted(census))
        print(kind, "two-pair orbit count:", len(reps), flush=True)
        combined = hashlib.sha256()
        for case in args.case or range(len(reps)):
            result = run(case, kind, args.timeout, not args.ledger_only)
            print(result, flush=True)
            if not args.ledger_only:
                assert result["status"] == "UNIT", result
            combined.update(f'{case}:{result["sha256"]}\n'.encode("ascii"))
        combined_digest = combined.hexdigest()
        print(kind, "combined ledger sha256:", combined_digest, flush=True)
        if not args.case:
            assert combined_digest == EXPECTED_COMBINED[kind]
    print("sole-defect two-pair common-power audit: PASS")


if __name__ == "__main__":
    main()
