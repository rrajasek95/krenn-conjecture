#!/usr/bin/env python3
"""Clean-room audit of the sole-defect three-distinct-lift obstruction.

This file imports no project code or frozen ledger.  It deliberately uses
maximal (rather than minimal) orbit representatives, alternative rational
coordinates for the deficient matroids, reversed endpoint/cell/equation
orders, rightmost-pivot elimination, and a reversed Singular variable order.
All ideals are affine and unsaturated over QQ.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import shutil
import subprocess
import time


SITES = (0, 1, 2, 3, 4, 5)
BAD = 0
GOOD_PERMS = tuple((0,) + p for p in permutations((1, 2, 3, 4, 5)))
PAIRS = tuple((v, u) for u, v in reversed(tuple(combinations(SITES, 2))))


def relabel_pair(pair, permutation):
    return tuple(sorted((permutation[pair[0]], permutation[pair[1]]), reverse=True))


def canonical_unordered(triple):
    """Maximal representative for S_5 on sites and S_3 on fields."""
    return max(
        tuple(sorted((relabel_pair(edge, p) for edge in triple), reverse=True))
        for p in GOOD_PERMS
    )


def canonical_coincident(labelled):
    """Maximal representative for S_5 and the equal-field swap 0 <-> 2."""
    return max(
        tuple(relabel_pair(labelled[index], p) for index in order)
        for p in GOOD_PERMS
        for order in ((0, 1, 2), (2, 1, 0))
    )


def orbit_data(kind):
    census = Counter()
    if kind == "coincident":
        # Select the distinguished field-1 edge, leaving the equal-field
        # edges as an unordered pair.  This enumerates 455*3=1365 objects.
        for edge_set in combinations(PAIRS, 3):
            for middle in edge_set:
                outer = tuple(sorted((set(edge_set) - {middle}), reverse=True))
                census[canonical_coincident((outer[0], middle, outer[1]))] += 1
        assert sum(census.values()) == 1365
    else:
        for edge_set in combinations(PAIRS, 3):
            census[canonical_unordered(edge_set)] += 1
        assert sum(census.values()) == 455
    expected = 26 if kind == "coincident" else 13
    assert len(census) == expected
    # Reverse the representatives yet again for the ideal stream.
    return tuple(sorted(census, reverse=True)), census


def local_model(kind):
    if kind == "circuit":
        # Three distinct lines, deliberately different from (e0,e1,e0+e1).
        return (2, 3, 3, 3, 3, 3), ((1, 1), (1, -1), (0, 1))
    if kind == "coincident":
        return (2, 3, 3, 3, 3, 3), ((1, 1), (1, -1), (1, 1))
    if kind == "rank1":
        return (1, 3, 3, 3, 3, 3), ((-2,), (3,), (5,))
    raise ValueError(kind)


def field_vector(site, field, bad_vectors):
    if site == BAD:
        return bad_vectors[field]
    # Reverse the three good-site coordinate axes.
    return tuple(int(coordinate == 2 - field) for coordinate in range(3))


def all_cells(dims):
    """All q coordinates, with the larger endpoint written first."""
    return tuple(
        (u, v, cu, cv)
        for u, v in PAIRS
        for cv in reversed(range(dims[v]))
        for cu in reversed(range(dims[u]))
    )


def cell_key(u, cu, v, cv):
    return (u, v, cu, cv) if u > v else (v, u, cv, cu)


def lift_terms(pair, field, bad_vectors):
    """Sparse degree-four coordinate expansion keyed by six-site words."""
    absent = frozenset(pair)
    terms = {(None,) * 6: Fraction(1)}
    for site in reversed(SITES):
        if site in absent:
            continue
        nxt = defaultdict(Fraction)
        for word, coefficient in terms.items():
            for coordinate, scalar in enumerate(field_vector(site, field, bad_vectors)):
                if scalar:
                    updated = list(word)
                    updated[site] = coordinate
                    nxt[tuple(updated)] += coefficient * scalar
        terms = dict(nxt)
    return {word: coefficient for word, coefficient in terms.items() if coefficient}


def target_terms(pairs, bad_vectors):
    target = defaultdict(Fraction)
    for field in (2, 1, 0):
        for word, coefficient in lift_terms(pairs[field], field, bad_vectors).items():
            target[word] += coefficient
    return {word: coefficient for word, coefficient in target.items() if coefficient}


def qf_matrix(pairs, dims, bad_vectors, cells):
    """Multiply all q cells by all F monomials and collect degree-six words."""
    index = {cell: column for column, cell in enumerate(cells)}
    rows = defaultdict(lambda: defaultdict(Fraction))
    for field in (2, 1, 0):
        for lift_word, lift_coefficient in lift_terms(
                pairs[field], field, bad_vectors).items():
            occupied = frozenset(site for site, value in enumerate(lift_word)
                                 if value is not None)
            for cell in cells:
                u, v, cu, cv = cell
                if u in occupied or v in occupied:
                    continue
                word = list(lift_word)
                word[u], word[v] = cu, cv
                rows[tuple(word)][index[cell]] += lift_coefficient
    ordered = tuple(
        {column: coefficient for column, coefficient in rows[word].items()
         if coefficient}
        for word in sorted(rows, reverse=True)
        if any(rows[word].values())
    )
    return ordered


def right_pivot_rref(source_rows):
    """Exact sparse RREF using the largest available pivot column."""
    pivots = {}
    for source in source_rows:
        row = {column: Fraction(value) for column, value in source.items() if value}
        for column in sorted(pivots, reverse=True):
            if column not in row:
                continue
            scale = row[column]
            for key, value in pivots[column].items():
                row[key] = row.get(key, Fraction(0)) - scale * value
                if not row[key]:
                    del row[key]
        if not row:
            continue
        pivot = max(row)
        scale = row[pivot]
        row = {column: value / scale for column, value in row.items()}
        for old in pivots.values():
            if pivot not in old:
                continue
            scale = old[pivot]
            for column, value in row.items():
                old[column] = old.get(column, Fraction(0)) - scale * value
                if not old[column]:
                    del old[column]
        pivots[pivot] = row
        pivots = dict(sorted(pivots.items(), reverse=True))
    return pivots


def linear_kernel(cells, pivots):
    free = tuple(column for column in reversed(range(len(cells)))
                 if column not in pivots)
    free_number = {column: number for number, column in enumerate(free)}
    expressions = {}
    for column, cell in enumerate(cells):
        if column in free_number:
            expressions[cell] = {free_number[column]: Fraction(1)}
        else:
            expressions[cell] = {
                free_number[key]: -coefficient
                for key, coefficient in pivots[column].items()
                if key != column and coefficient
            }
    return free, expressions


def add_polynomial(destination, source, scale=Fraction(1)):
    for monomial, coefficient in source.items():
        destination[monomial] += scale * coefficient
        if not destination[monomial]:
            del destination[monomial]


def multiply_linear(left, right):
    output = defaultdict(Fraction)
    for a, ca in left.items():
        for b, cb in right.items():
            output[tuple(sorted((a, b), reverse=True))] += ca * cb
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def q2_generators(dims, expressions, target):
    generators = []
    supports = tuple(reversed(tuple(combinations(SITES, 4))))
    # A different matching order from the primary stream.
    matchings = ((0, 3, 1, 2), (0, 2, 1, 3), (0, 1, 2, 3))
    for support in supports:
        coordinate_ranges = tuple(reversed(range(dims[site])) for site in support)
        words = tuple(product(*coordinate_ranges))
        for local in reversed(words):
            polynomial = defaultdict(Fraction)
            for i, j, k, ell in matchings:
                left = expressions[cell_key(
                    support[i], local[i], support[j], local[j]
                )]
                right = expressions[cell_key(
                    support[k], local[k], support[ell], local[ell]
                )]
                add_polynomial(polynomial, multiply_linear(left, right))
            full_word = [None] * 6
            for site, coordinate in zip(support, local):
                full_word[site] = coordinate
            constant = target.get(tuple(full_word), Fraction(0))
            if constant:
                polynomial[()] -= constant
                if not polynomial[()]:
                    del polynomial[()]
            if polynomial:
                generators.append(dict(polynomial))
    return tuple(generators)


def fraction_text(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def polynomial_text(polynomial):
    pieces = []
    for monomial in sorted(polynomial, key=lambda m: (len(m), m), reverse=True):
        coefficient = polynomial[monomial]
        if not monomial:
            term = fraction_text(coefficient)
        else:
            variables = "*".join(f"z{index}" for index in monomial)
            if coefficient == 1:
                term = variables
            elif coefficient == -1:
                term = f"-({variables})"
            else:
                term = f"{fraction_text(coefficient)}*({variables})"
        pieces.append(f"({term})")
    return "+".join(pieces)


def ledger_hash(pairs, cells, rows, pivots, generators):
    digest = hashlib.sha256()
    digest.update(repr(pairs).encode("ascii"))
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


def build_case(kind, pairs):
    dims, bad_vectors = local_model(kind)
    cells = all_cells(dims)
    rows = qf_matrix(pairs, dims, bad_vectors, cells)
    pivots = right_pivot_rref(rows)
    free, expressions = linear_kernel(cells, pivots)
    target = target_terms(pairs, bad_vectors)
    generators = q2_generators(dims, expressions, target)
    digest = ledger_hash(pairs, cells, rows, pivots, generators)
    return dims, cells, rows, pivots, free, generators, digest


def singular_unit(free_count, generators, timeout):
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required for the full independent audit")
    # Ring variable order is the reverse of the names assigned to free cells.
    variables = ",".join(f"z{i}" for i in reversed(range(free_count)))
    equations = ",".join(polynomial_text(poly) for poly in reversed(generators))
    program = (
        f"ring audit=0,({variables}),Dp;\n"
        f"ideal I={equations};\n"
        "ideal G=slimgb(I);\n"
        'print("AUDIT_SIZE");print(size(G));'
        'print("AUDIT_FIRST");print(G[1]);\n'
    )
    started = time.monotonic()
    result = subprocess.run(
        (executable, "-q"), input=program, text=True, capture_output=True,
        timeout=timeout,
    )
    seconds = time.monotonic() - started
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    status = "ERROR"
    if result.returncode == 0 and "AUDIT_SIZE" in lines and "AUDIT_FIRST" in lines:
        size = lines[lines.index("AUDIT_SIZE") + 1]
        first = lines[lines.index("AUDIT_FIRST") + 1]
        status = "UNIT" if size == first == "1" else f"NONUNIT:{size}:{first}"
    return status, seconds, result.stderr


# Filled after the clean-room streams are first reconstructed and frozen.
EXPECTED_COMBINED = {
    "circuit": "44030a6c1e715cef391076c048fcb95999048cb27b1e8433acb3a753f5beffbd",
    "coincident": "73931e0cd9b20455fc5a54d4bbf95e459ec847216596f6709620801a8e10f211",
    "rank1": "0706158f1d5883a2e0a75e32a34ac32765e27f5d0a13ee1924e36d44cd87f5d0",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", action="append",
                        choices=("circuit", "coincident", "rank1"))
    parser.add_argument("--case", action="append", type=int)
    parser.add_argument("--ledger-only", action="store_true")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()

    total_units = 0
    for kind in args.kind or ("rank1", "coincident", "circuit"):
        representatives, census = orbit_data(kind)
        print(kind, "orbits", len(representatives), "objects", sum(census.values()),
              "orbit sizes", dict(sorted(Counter(census.values()).items())), flush=True)
        combined = hashlib.sha256()
        selected = args.case if args.case is not None else range(len(representatives))
        for case in selected:
            pairs = representatives[case]
            dims, cells, rows, pivots, free, generators, digest = build_case(kind, pairs)
            status, seconds, stderr = ("SKIPPED", 0.0, "")
            if not args.ledger_only:
                status, seconds, stderr = singular_unit(len(free), generators, args.timeout)
                assert status == "UNIT", (kind, case, status, stderr)
                total_units += 1
            result = {
                "kind": kind, "case": case, "pairs": pairs, "dims": dims,
                "cells": len(cells), "rows": len(rows), "rank": len(pivots),
                "nullity": len(free), "generators": len(generators),
                "ledger": digest, "status": status, "seconds": round(seconds, 3),
            }
            print(result, flush=True)
            combined.update(f"{case}:{digest}\n".encode("ascii"))
        combined_digest = combined.hexdigest()
        print(kind, "independent combined ledger sha256", combined_digest, flush=True)
        if args.case is None and EXPECTED_COMBINED[kind]:
            assert combined_digest == EXPECTED_COMBINED[kind]

    if not args.ledger_only and args.case is None and args.kind is None:
        assert total_units == 52
    print("independent sole-defect distinct-lift audit: PASS", flush=True)


if __name__ == "__main__":
    main()
