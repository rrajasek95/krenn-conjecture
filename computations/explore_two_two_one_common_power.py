#!/usr/bin/env python3
"""Explore exact common-power ideals for the pure (2,2,1) profile.

The support is represented by ``(X,Y,Z)``: X and Y are unordered pairs of
distinct missing pairs carrying colours zero and one, and Z is the sole
colour-two missing pair.  Cross-colour repetitions are retained.  The two
two-term colours may be interchanged.

For each S6 orbit, this script constructs the *full* coefficient matrix of
qF=0, computes its exact rational RREF, substitutes a basis for its kernel
into every coefficient of q^[2]-F, and optionally asks Singular whether the
resulting unsaturated affine ideal is the unit ideal.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import shutil
import subprocess
import time


U = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {pair: index for index, pair in enumerate(EDGES)}
N_Q_CELL = len(EDGES) * len(COLOURS) ** 2
SITE_PERMUTATIONS = tuple(permutations(U))
PAIR_SETS = tuple(combinations(EDGES, 2))


def edge(u, v):
    return (u, v) if u < v else (v, u)


def normalize(x_edges, y_edges, z):
    x_edges = tuple(sorted(x_edges))
    y_edges = tuple(sorted(y_edges))
    z = edge(*z)
    return min((x_edges, y_edges, z), (y_edges, x_edges, z))


def support_orbit(support):
    x_edges, y_edges, z = support
    output = set()
    for permutation in SITE_PERMUTATIONS:
        x_image = tuple(edge(permutation[u], permutation[v]) for u, v in x_edges)
        y_image = tuple(edge(permutation[u], permutation[v]) for u, v in y_edges)
        z_image = edge(permutation[z[0]], permutation[z[1]])
        output.add(normalize(x_image, y_image, z_image))
    return output


def representatives():
    all_supports = {
        normalize(x_edges, y_edges, z)
        for x_edges in PAIR_SETS
        for y_edges in PAIR_SETS
        for z in EDGES
    }
    seen = set()
    output = []
    for support in sorted(all_supports):
        if support in seen:
            continue
        orbit = support_orbit(support)
        assert support in orbit
        assert not seen.intersection(orbit)
        output.append((support, len(orbit)))
        seen.update(orbit)
    assert seen == all_supports
    assert len(all_supports) == 83475
    assert len(output) == 195
    return tuple(output)


REPRESENTATIVE_DATA = representatives()
REPRESENTATIVES = tuple(support for support, _ in REPRESENTATIVE_DATA)


def distinct_pair_count(support):
    x_edges, y_edges, z = support
    return len(set(x_edges + y_edges + (z,)))


def q_index(pair, cu, cv):
    return 9 * EDGE_INDEX[pair] + 3 * cu + cv


def qf_rows(support):
    """Sparse coefficient rows for qF=0, with no support separation."""
    x_edges, y_edges, z = support
    rows = {}
    for pair, colour in (
        *((pair, 0) for pair in x_edges),
        *((pair, 1) for pair in y_edges),
        (z, 2),
    ):
        u, v = pair
        for cu, cv in product(COLOURS, repeat=2):
            word = [colour] * len(U)
            word[u], word[v] = cu, cv
            row = rows.setdefault(tuple(word), {})
            column = q_index(pair, cu, cv)
            row[column] = row.get(column, Fraction(0)) + 1
    return tuple(row for row in rows.values() if row)


def sparse_rref(source_rows):
    """Return exact RREF as a pivot-column dictionary of sparse rows."""
    pivots = {}
    for source in source_rows:
        row = {
            column: Fraction(value)
            for column, value in source.items()
            if value
        }
        for column in sorted(pivots):
            if column not in row:
                continue
            scale = row[column]
            for key, value in pivots[column].items():
                row[key] = row.get(key, Fraction(0)) - scale * value
                if row[key] == 0:
                    del row[key]
        if not row:
            continue
        column = min(row)
        scale = row[column]
        row = {key: value / scale for key, value in row.items()}
        for old_column, old_row in pivots.items():
            if column not in old_row:
                continue
            old_scale = old_row[column]
            for key, value in row.items():
                old_row[key] = old_row.get(key, Fraction(0)) - old_scale * value
                if old_row[key] == 0:
                    del old_row[key]
        pivots[column] = row
        pivots = dict(sorted(pivots.items()))
    return pivots


def kernel_basis(pivots):
    free = tuple(column for column in range(N_Q_CELL) if column not in pivots)
    basis = []
    for column in free:
        vector = {column: Fraction(1)}
        for pivot, row in pivots.items():
            if column in row:
                vector[pivot] = -row[column]
        basis.append(vector)
    return free, tuple(basis)


def audit_kernel(support):
    rows = qf_rows(support)
    pivots = sparse_rref(rows)
    free, basis = kernel_basis(pivots)
    assert len(pivots) + len(basis) == N_Q_CELL
    for vector in basis:
        for row in rows:
            assert sum(
                value * vector.get(column, Fraction(0))
                for column, value in row.items()
            ) == 0
    return len(pivots), len(free), pivots, basis


def fraction_string(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def linear_expression(terms):
    pieces = []
    for variable, coefficient in terms:
        coefficient = Fraction(coefficient)
        if not coefficient:
            continue
        if coefficient == 1:
            term = variable
        elif coefficient == -1:
            term = f"-({variable})"
        else:
            term = f"({fraction_string(coefficient)})*({variable})"
        pieces.append(term)
    return "0" if not pieces else "(" + ")+(".join(pieces) + ")"


def parameterization(support):
    rank, nullity, pivots, basis = audit_kernel(support)
    variables = tuple(f"t{index}" for index in range(nullity))
    by_column = [[] for _ in range(N_Q_CELL)]
    for variable, vector in zip(variables, basis):
        for column, coefficient in vector.items():
            by_column[column].append((variable, coefficient))
    values = {}
    for pair in EDGES:
        for cu, cv in product(COLOURS, repeat=2):
            column = q_index(pair, cu, cv)
            values[pair, cu, cv] = linear_expression(by_column[column])
    return variables, values, rank


def add(*terms):
    terms = tuple(term for term in terms if term != "0")
    if not terms:
        return "0"
    if len(terms) == 1:
        return terms[0]
    return "(" + ")+(".join(terms) + ")"


def multiply(left, right):
    if left == "0" or right == "0":
        return "0"
    return f"({left})*({right})"


def cell(values, u, v, cu, cv):
    if u < v:
        return values[(u, v), cu, cv]
    return values[(v, u), cv, cu]


def equations(support):
    variables, values, rank = parameterization(support)
    x_edges, y_edges, z = support
    target = Counter()
    for pair, colour in (
        *((pair, 0) for pair in x_edges),
        *((pair, 1) for pair in y_edges),
        (z, 2),
    ):
        sites = tuple(u for u in U if u not in pair)
        target[sites, (colour,) * 4] += 1
    patterns = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    output = []
    for sites in combinations(U, 4):
        for colours in product(COLOURS, repeat=4):
            polynomial = add(*(
                multiply(
                    cell(values, sites[i], sites[j], colours[i], colours[j]),
                    cell(values, sites[k], sites[l], colours[k], colours[l]),
                )
                for i, j, k, l in patterns
            ))
            constant = target[sites, colours]
            if constant:
                polynomial = add(polynomial, str(-constant))
            if polynomial != "0":
                output.append(polynomial)
    return variables, tuple(output), rank


def ledger_digest(generators):
    digest = hashlib.sha256()
    for generator in generators:
        digest.update(generator.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def run(orbit, timeout):
    support = REPRESENTATIVES[orbit - 1]
    variables, generators, rank = equations(support)
    digest = ledger_digest(generators)
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=slimgb(I);\n"
        'print("BASIS_SIZE"); print(size(G));\n'
        'print("BASIS_FIRST"); print(G[1]);\n'
    )
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    result = subprocess.run(
        (executable, "-q"), input=program, text=True, capture_output=True,
        timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if result.returncode:
        return orbit, support, rank, len(variables), len(generators), digest, "ERROR", elapsed, result.stderr
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    try:
        size = lines[lines.index("BASIS_SIZE") + 1]
        first = lines[lines.index("BASIS_FIRST") + 1]
    except (ValueError, IndexError):
        return orbit, support, rank, len(variables), len(generators), digest, "MALFORMED", elapsed, result.stdout
    status = "UNIT" if size == first == "1" else f"NONUNIT:{size}:{first}"
    return orbit, support, rank, len(variables), len(generators), digest, status, elapsed, ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--distinct", type=int, action="append")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--skip-ideals", action="store_true")
    args = parser.parse_args()

    counts = tuple(count for _, count in REPRESENTATIVE_DATA)
    distinct_orbits = Counter(distinct_pair_count(s) for s in REPRESENTATIVES)
    distinct_labelled = Counter()
    for support, count in REPRESENTATIVE_DATA:
        distinct_labelled[distinct_pair_count(support)] += count
    orbit_digest = hashlib.sha256()
    for support, count in REPRESENTATIVE_DATA:
        orbit_digest.update(f"{support}:{count}\n".encode("ascii"))
    print("raw labelled supports:", len(PAIR_SETS) ** 2 * len(EDGES))
    print("colour-swap normalized labelled supports:", sum(counts))
    print("support orbits:", len(REPRESENTATIVES))
    print("orbit-size histogram:", dict(sorted(Counter(counts).items())))
    print("orbits by distinct physical pairs:", dict(sorted(distinct_orbits.items())))
    print("labelled by distinct physical pairs:", dict(sorted(distinct_labelled.items())))
    print("orbit-ledger sha256:", orbit_digest.hexdigest())

    selected = list(args.orbit or range(1, len(REPRESENTATIVES) + 1))
    if args.distinct:
        selected = [
            orbit for orbit in selected
            if distinct_pair_count(REPRESENTATIVES[orbit - 1]) in args.distinct
        ]
    if any(orbit < 1 or orbit > len(REPRESENTATIVES) for orbit in selected):
        raise SystemExit(f"--orbit must lie in 1..{len(REPRESENTATIVES)}")

    ranks = Counter()
    for orbit in selected:
        rank, nullity, _, _ = audit_kernel(REPRESENTATIVES[orbit - 1])
        ranks[rank, nullity] += 1
    print("selected qF rank/nullity histogram:", dict(sorted(ranks.items())))
    if args.skip_ideals:
        return

    outputs = []
    wall_started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run, orbit, args.timeout): orbit for orbit in selected
        }
        for future in as_completed(futures):
            result = future.result()
            outputs.append(result)
            print(
                "completed orbit", result[0], result[6],
                "seconds", f"{result[7]:.3f}", flush=True,
            )
    for result in sorted(outputs):
        orbit, support, rank, nullity, equation_count, digest, status, elapsed, detail = result
        print(
            "orbit", orbit, "support", support,
            "distinct", distinct_pair_count(support),
            "qF", f"{rank}/{nullity}", "equations", equation_count,
            "sha256", digest, status, "seconds", f"{elapsed:.3f}",
        )
        if detail:
            print(detail)
    print("parallel wall seconds:", f"{time.monotonic() - wall_started:.3f}")


if __name__ == "__main__":
    main()
