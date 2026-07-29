#!/usr/bin/env python3
"""Explore exact response-product feasibility for pure (2,2,1) supports.

This imports the independently generated 195 support orbits from
``explore_two_two_one_common_power.py``.  All coefficients are normalized to
one.  For every support it can construct the literal coefficient ideal of

    p_i s_j F = delta_ij X_i

with arbitrary three-coordinate components at every used site.  Cancellation
between the two same-colour lifts is retained by collecting equal six-site
words before emitting generators.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from itertools import product
import shutil
import subprocess
import time

import explore_two_two_one_common_power as common_power


U = common_power.U
COLOURS = common_power.COLOURS
REPRESENTATIVE_DATA = common_power.REPRESENTATIVE_DATA
REPRESENTATIVES = common_power.REPRESENTATIVES


def variable(kind, row, site, colour):
    return f"{kind}{row}{site}{colour}"


def response_monomials(edge, i, j, a, b):
    u, v = edge
    return (
        f"{variable('p', i, u, a)}*{variable('s', j, v, b)}",
        f"{variable('s', j, u, a)}*{variable('p', i, v, b)}",
    )


def response_generators(support, diagonal_only=False):
    x_edges, y_edges, z = support
    groups = (x_edges, y_edges, (z,))
    used = tuple(sorted({site for group in groups for edge in group for site in edge}))
    if diagonal_only:
        row_pairs = tuple((i, i) for i in COLOURS)
    else:
        row_pairs = tuple(product(COLOURS, repeat=2))
    variables = tuple(
        variable(kind, row, site, colour)
        for kind, row, site, colour in product("ps", COLOURS, used, COLOURS)
    )
    equations = []
    for i, j in row_pairs:
        for k, group in enumerate(groups):
            coefficients = defaultdict(list)
            for edge in group:
                u, v = edge
                for a, b in product(COLOURS, repeat=2):
                    word = [k] * len(U)
                    word[u], word[v] = a, b
                    coefficients[tuple(word)].extend(
                        response_monomials(edge, i, j, a, b)
                    )
            target_word = (k,) * len(U)
            if i == j == k and target_word not in coefficients:
                coefficients[target_word] = []
            for word in sorted(coefficients):
                terms = coefficients[word]
                equation = "+".join(terms) if terms else "0"
                if i == j == k and word == target_word:
                    equation += "-1"
                equations.append(equation)
    return variables, tuple(equations)


def coordinate_witnesses(support):
    """Enumerate simple private-edge coordinate solutions."""
    x_edges, y_edges, z = support
    groups = (x_edges, y_edges, (z,))
    union = set(x_edges + y_edges + (z,))
    private = []
    for i, group in enumerate(groups):
        others = set().union(*(set(other) for j, other in enumerate(groups) if j != i))
        private.append(tuple(edge for edge in group if edge not in others))
    output = []
    for selected in product(*private):
        for orientations in product((0, 1), repeat=3):
            endpoints = tuple(
                (edge[orientation], edge[1 - orientation])
                for edge, orientation in zip(selected, orientations)
            )
            if all(
                p_site == s_site
                or common_power.edge(p_site, s_site) not in union
                for i, (p_site, _) in enumerate(endpoints)
                for j, (_, s_site) in enumerate(endpoints)
                if i != j
            ):
                output.append((selected, orientations, endpoints))
    return tuple(output)


def forms_from_coordinate_witness(witness):
    _, _, endpoints = witness
    forms = {
        kind: {
            (row, site, colour): 0
            for row, site, colour in product(COLOURS, U, COLOURS)
        }
        for kind in "ps"
    }
    for colour, (p_site, s_site) in enumerate(endpoints):
        forms["p"][colour, p_site, colour] = 1
        forms["s"][colour, s_site, colour] = 1
    return forms


def response_value(forms, edge, i, j, a, b):
    u, v = edge
    return (
        forms["p"][i, u, a] * forms["s"][j, v, b]
        + forms["s"][j, u, a] * forms["p"][i, v, b]
    )


def audit_coordinate_witness(support, witness):
    forms = forms_from_coordinate_witness(witness)
    x_edges, y_edges, z = support
    groups = (x_edges, y_edges, (z,))
    for i, j in product(COLOURS, repeat=2):
        for k, group in enumerate(groups):
            coefficients = Counter()
            for edge in group:
                u, v = edge
                for a, b in product(COLOURS, repeat=2):
                    word = [k] * len(U)
                    word[u], word[v] = a, b
                    coefficients[tuple(word)] += response_value(forms, edge, i, j, a, b)
            coefficients += Counter()
            expected = Counter({(i,) * len(U): 1}) if i == j == k else Counter()
            assert coefficients == expected, (support, witness, i, j, k, coefficients, expected)


def ledger_digest(generators):
    digest = hashlib.sha256()
    for generator in generators:
        digest.update(generator.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def run(orbit, timeout, diagonal_only):
    support = REPRESENTATIVES[orbit - 1]
    variables, generators = response_generators(support, diagonal_only)
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
    try:
        result = subprocess.run(
            (executable, "-q"), input=program, text=True, capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return orbit, support, len(variables), len(generators), digest, "TIMEOUT", time.monotonic() - started, ""
    elapsed = time.monotonic() - started
    if result.returncode:
        return orbit, support, len(variables), len(generators), digest, "ERROR", elapsed, result.stderr
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    try:
        size = lines[lines.index("BASIS_SIZE") + 1]
        first = lines[lines.index("BASIS_FIRST") + 1]
    except (ValueError, IndexError):
        return orbit, support, len(variables), len(generators), digest, "MALFORMED", elapsed, result.stdout
    status = "UNIT" if size == first == "1" else f"NONUNIT:{size}:{first}"
    return orbit, support, len(variables), len(generators), digest, status, elapsed, ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--distinct", type=int, action="append")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--diagonal-only", action="store_true")
    parser.add_argument("--include-witnesses", action="store_true")
    parser.add_argument("--skip-ideals", action="store_true")
    args = parser.parse_args()

    witness_data = {}
    for orbit, support in enumerate(REPRESENTATIVES, 1):
        witnesses = coordinate_witnesses(support)
        if witnesses:
            audit_coordinate_witness(support, witnesses[0])
            witness_data[orbit] = witnesses
    print("coordinate-witness orbits:", len(witness_data))
    print("coordinate-witness labelled supports:", sum(
        REPRESENTATIVE_DATA[orbit - 1][1] for orbit in witness_data
    ))
    print("coordinate-witness orbit numbers:", tuple(witness_data))
    print("coordinate-witnesses by distinct pairs:", dict(sorted(Counter(
        common_power.distinct_pair_count(REPRESENTATIVES[orbit - 1])
        for orbit in witness_data
    ).items())))

    selected = list(args.orbit or range(1, len(REPRESENTATIVES) + 1))
    if args.distinct:
        selected = [
            orbit for orbit in selected
            if common_power.distinct_pair_count(REPRESENTATIVES[orbit - 1]) in args.distinct
        ]
    if not args.include_witnesses:
        selected = [orbit for orbit in selected if orbit not in witness_data]
    if args.skip_ideals:
        return

    outputs = []
    wall_started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run, orbit, args.timeout, args.diagonal_only): orbit
            for orbit in selected
        }
        for future in as_completed(futures):
            result = future.result()
            outputs.append(result)
            print("completed orbit", result[0], result[5], "seconds", f"{result[6]:.3f}", flush=True)
    for result in sorted(outputs):
        orbit, support, variable_count, equation_count, digest, status, elapsed, detail = result
        print(
            "orbit", orbit, "support", support,
            "distinct", common_power.distinct_pair_count(support),
            "variables", variable_count, "equations", equation_count,
            "sha256", digest, status, "seconds", f"{elapsed:.3f}",
        )
        if detail:
            print(detail)
    print("parallel wall seconds:", f"{time.monotonic() - wall_started:.3f}")


if __name__ == "__main__":
    main()
