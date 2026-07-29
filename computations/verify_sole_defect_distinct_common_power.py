#!/usr/bin/env python3
"""Exact checker for three distinct lifts with one deficient local frame.

The script constructs the complete qF=0 kernel and q^[2]=F ideal for all
distinguished-site orbits of three distinct missing pairs: 13 orbits for the
rank-two circuit and rank-one types, and 26 for the rank-two coincident-pair
type.  Every ideal is computed unsaturated over QQ.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import shutil
import subprocess
import time


U = tuple(range(6))
EDGES = tuple(combinations(U, 2))
UNORDERED_REPRESENTATIVES = (
    ((0, 1), (0, 2), (0, 3)),
    ((0, 1), (0, 2), (1, 2)),
    ((0, 1), (0, 2), (1, 3)),
    ((0, 1), (0, 2), (3, 4)),
    ((0, 1), (1, 2), (1, 3)),
    ((0, 1), (1, 2), (2, 3)),
    ((0, 1), (1, 2), (3, 4)),
    ((0, 1), (2, 3), (2, 4)),
    ((0, 1), (2, 3), (4, 5)),
    ((1, 2), (1, 3), (1, 4)),
    ((1, 2), (1, 3), (2, 3)),
    ((1, 2), (1, 3), (2, 4)),
    ((1, 2), (1, 3), (4, 5)),
)

# In the coincident type fields 0 and 2 are the equal pair and field 1 is
# distinguished.  These are the 26 orbits under S_5 at the bad site and the
# swap 0 <-> 2.
COINCIDENT_REPRESENTATIVES = (
    ((0, 1), (0, 2), (0, 3)),
    ((0, 1), (0, 2), (1, 2)),
    ((0, 1), (0, 2), (1, 3)),
    ((0, 1), (0, 2), (2, 3)),
    ((0, 1), (0, 2), (3, 4)),
    ((0, 1), (1, 2), (0, 2)),
    ((0, 1), (1, 2), (0, 3)),
    ((0, 1), (1, 2), (1, 3)),
    ((0, 1), (1, 2), (2, 3)),
    ((0, 1), (1, 2), (3, 4)),
    ((0, 1), (2, 3), (0, 4)),
    ((0, 1), (2, 3), (1, 2)),
    ((0, 1), (2, 3), (1, 4)),
    ((0, 1), (2, 3), (2, 4)),
    ((0, 1), (2, 3), (4, 5)),
    ((1, 2), (0, 1), (1, 3)),
    ((1, 2), (0, 1), (2, 3)),
    ((1, 2), (0, 1), (3, 4)),
    ((1, 2), (0, 3), (1, 4)),
    ((1, 2), (0, 3), (4, 5)),
    ((1, 2), (1, 3), (1, 4)),
    ((1, 2), (1, 3), (2, 3)),
    ((1, 2), (1, 3), (2, 4)),
    ((1, 2), (1, 3), (3, 4)),
    ((1, 2), (1, 3), (4, 5)),
    ((1, 2), (3, 4), (1, 5)),
)

EXPECTED_COMBINED = {
    "circuit": "29a338ee82a625787b6a755f392c718fb06f2daca3974a4ef6e9956376eacb07",
    "coincident": "dc8b15a0d3cc09e53a49c850e6b55b1f5938f47c6534d4e61f190ac72fb488fc",
    "rank1": "263028527daeecd8561a6b847f7247452e46ba4f51c7bdb528a3a747da279b65",
}


def representatives(kind):
    return COINCIDENT_REPRESENTATIVES if kind == "coincident" else UNORDERED_REPRESENTATIVES


def local_data(kind):
    if kind == "circuit":
        return (2, 3, 3, 3, 3, 3), ((1, 0), (0, 1), (1, 1))
    if kind == "coincident":
        return (2, 3, 3, 3, 3, 3), ((1, 0), (0, 1), (1, 0))
    if kind == "rank1":
        return (1, 3, 3, 3, 3, 3), ((1,), (1,), (1,))
    raise ValueError(kind)


def field_vector(site, colour, bad_vectors):
    if site == 0:
        return bad_vectors[colour]
    return tuple(int(index == colour) for index in range(3))


def q_cells(dims):
    cells = []
    for edge in EDGES:
        u, v = edge
        for cu in range(dims[u]):
            for cv in range(dims[v]):
                cells.append((edge, cu, cv))
    return tuple(cells)


def pure_lift(pair, colour, dims, bad_vectors):
    occupied = tuple(site for site in U if site not in pair)
    terms = {(): Fraction(1)}
    for site in occupied:
        nxt = {}
        for prefix, coefficient in terms.items():
            for coordinate, value in enumerate(field_vector(site, colour, bad_vectors)):
                if value:
                    nxt[prefix + ((site, coordinate),)] = coefficient * value
        terms = nxt
    return terms


def f_coefficients(pairs, dims, bad_vectors):
    by_support = Counter()
    for colour, pair in enumerate(pairs):
        for local_word, coefficient in pure_lift(pair, colour, dims, bad_vectors).items():
            support = tuple(site for site, coordinate in local_word)
            word = tuple(coordinate for site, coordinate in local_word)
            by_support[support, word] += coefficient
    return {key: value for key, value in by_support.items() if value}


def qf_rows(pairs, dims, bad_vectors, cells, cell_index):
    rows = {}
    for colour, pair in enumerate(pairs):
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
    return tuple({c: v for c, v in row.items() if v}
                 for row in rows.values() if any(row.values()))


def sparse_rref(source_rows):
    pivots = {}
    for source in source_rows:
        row = {column: Fraction(value) for column, value in source.items() if value}
        for column in sorted(pivots):
            if column not in row:
                continue
            scale = row[column]
            for key, value in pivots[column].items():
                row[key] = row.get(key, Fraction(0)) - scale * value
                if not row[key]:
                    del row[key]
        if not row:
            continue
        column = min(row)
        scale = row[column]
        row = {key: value / scale for key, value in row.items()}
        for old in pivots.values():
            if column not in old:
                continue
            scale = old[column]
            for key, value in row.items():
                old[key] = old.get(key, Fraction(0)) - scale * value
                if not old[key]:
                    del old[key]
        pivots[column] = row
        pivots = dict(sorted(pivots.items()))
    return pivots


def linear_expression(terms):
    pieces = []
    for variable, coefficient in terms:
        if coefficient == 1:
            pieces.append(variable)
        elif coefficient == -1:
            pieces.append(f"-({variable})")
        elif coefficient.denominator == 1:
            pieces.append(f"({coefficient.numerator})*({variable})")
        else:
            pieces.append(
                f"({coefficient.numerator}/{coefficient.denominator})*({variable})"
            )
    return "0" if not pieces else "(" + ")+(".join(pieces) + ")"


def add(*terms):
    terms = tuple(term for term in terms if term != "0")
    return "0" if not terms else terms[0] if len(terms) == 1 else "(" + ")+(".join(terms) + ")"


def multiply(left, right):
    return "0" if left == "0" or right == "0" else f"({left})*({right})"


def build(case, kind):
    pairs = representatives(kind)[case]
    dims, bad_vectors = local_data(kind)
    cells = q_cells(dims)
    cell_index = {cell: index for index, cell in enumerate(cells)}
    rows = qf_rows(pairs, dims, bad_vectors, cells, cell_index)
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

    target = f_coefficients(pairs, dims, bad_vectors)
    generators = []
    matching_patterns = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    for sites in combinations(U, 4):
        ranges = tuple(range(dims[site]) for site in sites)
        for word in product(*ranges):
            terms = []
            for i, j, k, l in matching_patterns:
                left_sites = tuple(sorted((sites[i], sites[j])))
                right_sites = tuple(sorted((sites[k], sites[l])))
                left_word = (word[i], word[j]) if sites[i] < sites[j] else (word[j], word[i])
                right_word = (word[k], word[l]) if sites[k] < sites[l] else (word[l], word[k])
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
    return pairs, dims, cells, rows, pivots, variables, tuple(generators)


def ledger_digest(cells, rows, pivots, generators):
    digest = hashlib.sha256()
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
    pairs, dims, cells, rows, pivots, variables, generators = build(case, kind)
    digest = ledger_digest(cells, rows, pivots, generators)
    if not run_ideal:
        return {
            "case": case, "kind": kind, "pairs": pairs, "dims": dims,
            "cells": len(cells), "rows": len(rows), "rank": len(pivots),
            "nullity": len(variables), "generators": len(generators),
            "sha256": digest, "status": "SKIPPED", "seconds": 0.0,
            "stderr": "",
        }
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
    output = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    status = "ERROR"
    if result.returncode == 0 and "SIZE" in output and "FIRST" in output:
        size = output[output.index("SIZE") + 1]
        first = output[output.index("FIRST") + 1]
        status = "UNIT" if size == first == "1" else f"NONUNIT:{size}:{first}"
    return {
        "case": case, "kind": kind, "pairs": pairs, "dims": dims,
        "cells": len(cells), "rows": len(rows), "rank": len(pivots),
        "nullity": len(variables), "generators": len(generators),
        "sha256": digest, "status": status, "seconds": elapsed,
        "stderr": result.stderr,
    }


def orbit_census(kind):
    permutations_fixing_zero = tuple((0,) + p for p in permutations(range(1, 6)))
    if kind == "coincident":
        def canonical(labelled):
            return min(
                tuple(tuple(sorted((p[labelled[i][0]], p[labelled[i][1]])))
                      for i in order)
                for p in permutations_fixing_zero
                for order in ((0, 1, 2), (2, 1, 0))
            )
        census = Counter()
        for edges in combinations(EDGES, 3):
            for singleton in edges:
                equal = sorted(set(edges) - {singleton})
                census[canonical((equal[0], singleton, equal[1]))] += 1
        assert sum(census.values()) == 1365
    else:
        def canonical(edges):
            return min(tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in edges))
                       for p in permutations_fixing_zero)
        census = Counter(canonical(edges) for edges in combinations(EDGES, 3))
        assert sum(census.values()) == 455
    assert tuple(sorted(census)) == tuple(sorted(representatives(kind)))
    return census


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, action="append")
    parser.add_argument("--kind", choices=("circuit", "coincident", "rank1"), action="append")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--ledger-only", action="store_true")
    args = parser.parse_args()
    for kind in args.kind or ("circuit", "coincident", "rank1"):
        print(kind, "distinguished-site orbit census:", dict(orbit_census(kind)), flush=True)
        combined = hashlib.sha256()
        for case in args.case or range(len(representatives(kind))):
            result = run(case, kind, args.timeout, not args.ledger_only)
            print(result, flush=True)
            if not args.ledger_only:
                assert result["status"] == "UNIT", result
            combined.update(f'{case}:{result["sha256"]}\n'.encode("ascii"))
        combined_digest = combined.hexdigest()
        print(kind, "combined ledger sha256:", combined_digest, flush=True)
        if not args.case:
            assert combined_digest == EXPECTED_COMBINED[kind]
    print("sole-defect distinct-lift common-power obstruction: PASS")


if __name__ == "__main__":
    main()
