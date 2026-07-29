#!/usr/bin/env python3
"""Exact audit of the arbitrary-star monomial base-locus obstruction.

On six sites, fix three possibly repeated missing pairs P_k and the pure four-site
monomials F_k of colour k on the complements.  This checker audits the
literal local equations equivalent to

    p_i s_j sum_k lambda_k F_k = delta_ij lambda_i X_i

for completely arbitrary site-supported three-colour linear forms p_i,s_j.
It first enumerates all 15^3 colour-indexed pair triples and checks the
literal one-equation contradiction for every repeated-pair triple.  It then
enumerates the five distinct-edge support-graph types, verifies explicit
solutions for the two feasible types, and asks Singular over QQ for unit
Groebner bases for the other three types.  No support, nonzero, rank, or
genericity conditions are imposed on the star rows.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from itertools import combinations, product
import shutil
import subprocess
import time


SITES = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))

REPRESENTATIVES = {
    "three_star": ((0, 1), (0, 2), (0, 3)),
    "triangle": ((0, 1), (0, 2), (1, 2)),
    "three_path": ((0, 1), (1, 2), (2, 3)),
    "two_path_plus_edge": ((0, 1), (1, 2), (3, 4)),
    "three_matching": ((0, 1), (2, 3), (4, 5)),
}

EXPECTED_TYPE_COUNTS = Counter({
    "three_star": 60,
    "triangle": 20,
    "three_path": 180,
    "two_path_plus_edge": 180,
    "three_matching": 15,
})

# Hashes cover the ordered QQ generator ledgers, not Singular formatting.
EXPECTED_GENERATOR_SHA256 = {
    "three_star": "6bbc861333ee4695fd0566ad1d781cfcb660c1ec5e3c32057dc225e847e60a46",
    "triangle": "6c02a565de695e6cd49f8f2d0d1660aefc2b85ba7291678f3b45235cb9efb760",
    "three_path": "ee68af14f146776443fc1479188c9e9cb4439850097a457e4f2cc895e426a905",
}


def graph_type(edges: tuple[tuple[int, int], ...]) -> str:
    degrees = Counter(vertex for edge in edges for vertex in edge)
    signature = (len(degrees), tuple(sorted(degrees.values())))
    return {
        (4, (1, 1, 1, 3)): "three_star",
        (3, (2, 2, 2)): "triangle",
        (4, (1, 1, 2, 2)): "three_path",
        (5, (1, 1, 1, 1, 2)): "two_path_plus_edge",
        (6, (1, 1, 1, 1, 1, 1)): "three_matching",
    }[signature]


def variable(kind: str, row: int, site: int, colour: int) -> str:
    return f"{kind}{row}{site}{colour}"


def response_generators(edges: tuple[tuple[int, int], ...]):
    """Return variables and every scalar coefficient of the local equations.

    For P_k={u,v}, the coefficient at local colours (a,b) is

      p_{i,u,a}s_{j,v,b} + s_{j,u,a}p_{i,v,b}
        - delta_{ij}delta_{ik}delta_{ak}delta_{bk}.
    """

    used = tuple(sorted({site for edge in edges for site in edge}))
    variables = tuple(
        variable(kind, row, site, colour)
        for kind, row, site, colour in product("ps", COLOURS, used, COLOURS)
    )
    equations = []
    for k, (u, v) in enumerate(edges):
        for i, j, a, b in product(COLOURS, repeat=4):
            equations.append(response_equation(edges, k, i, j, a, b))
    assert len(equations) == 3 * 3**4 == 243
    return variables, tuple(equations)


def response_equation(edges, k, i, j, a, b):
    """One scalar equation, with both endpoint orders retained literally."""
    u, v = edges[k]
    equation = (
        f"{variable('p', i, u, a)}*{variable('s', j, v, b)}"
        f"+{variable('s', j, u, a)}*{variable('p', i, v, b)}"
    )
    if i == j == k and a == b == k:
        equation += "-1"
    return equation


def verify_repeated_pair_conflict(edges):
    """A repeated pair forces the same response tensor to be zero and nonzero."""
    collisions = tuple(
        (i, k) for i in COLOURS for k in COLOURS if i < k and edges[i] == edges[k]
    )
    assert collisions
    i, k = collisions[0]
    forced_nonzero = response_equation(edges, i, i, i, i, i)
    forced_zero = response_equation(edges, k, i, i, i, i)
    assert forced_nonzero == forced_zero + "-1", (
        edges, i, k, forced_nonzero, forced_zero
    )


def ledger_digest(equations: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    for equation in equations:
        digest.update(equation.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def empty_forms():
    return {
        kind: {
            (row, site, colour): 0
            for row, site, colour in product(COLOURS, SITES, COLOURS)
        }
        for kind in "ps"
    }


def coordinate_witness(name: str):
    forms = empty_forms()
    if name == "three_matching":
        edges = REPRESENTATIVES[name]
        orientations = edges
    elif name == "two_path_plus_edge":
        edges = REPRESENTATIVES[name]
        orientations = ((0, 1), (1, 2), (3, 4))
    else:
        raise ValueError(name)
    for colour, (tail, head) in enumerate(orientations):
        forms["p"][colour, tail, colour] = 1
        forms["s"][colour, head, colour] = 1
    return edges, forms


def response_coefficient(forms, edge, i, j, a, b):
    u, v = edge
    return (
        forms["p"][i, u, a] * forms["s"][j, v, b]
        + forms["s"][j, u, a] * forms["p"][i, v, b]
    )


def verify_witness(name: str):
    edges, forms = coordinate_witness(name)
    for k, edge in enumerate(edges):
        for i, j, a, b in product(COLOURS, repeat=4):
            expected = int(i == j == k and a == b == k)
            assert response_coefficient(forms, edge, i, j, a, b) == expected


def singular_program(name: str):
    variables, equations = response_generators(REPRESENTATIVES[name])
    digest = ledger_digest(equations)
    assert digest == EXPECTED_GENERATOR_SHA256[name], (name, digest)
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "ideal G=slimgb(I);\n"
        f'print("TYPE {name}");\n'
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    return program, len(variables), len(equations), digest


def run_singular(name: str, executable: str, timeout: int):
    program, variable_count, equation_count, digest = singular_program(name)
    started = time.monotonic()
    result = subprocess.run(
        (executable, "-q"),
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if result.stderr.strip():
        raise AssertionError(f"{name}: Singular stderr:\n{result.stderr}")
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    try:
        size = lines[lines.index("BASIS_SIZE") + 1]
        first = lines[lines.index("BASIS_FIRST") + 1]
    except (ValueError, IndexError) as error:
        raise AssertionError(f"{name}: malformed Singular output:\n{result.stdout}") from error
    assert size == first == "1", (name, result.stdout)
    return name, variable_count, equation_count, digest, elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-ideals",
        action="store_true",
        help="only audit the graph census and the two explicit response tables",
    )
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    ordered_triples = tuple(product(EDGES, repeat=3))
    repeated = tuple(edges for edges in ordered_triples if len(set(edges)) < 3)
    distinct_ordered = tuple(edges for edges in ordered_triples if len(set(edges)) == 3)
    assert len(ordered_triples) == 15**3 == 3375
    assert len(repeated) == 645
    assert len(distinct_ordered) == 2730
    for edges in repeated:
        verify_repeated_pair_conflict(edges)

    ordered_counts = Counter(graph_type(edges) for edges in distinct_ordered)
    assert ordered_counts == Counter({name: 6 * count for name, count in EXPECTED_TYPE_COUNTS.items()})

    counts = Counter(graph_type(edges) for edges in combinations(EDGES, 3))
    assert sum(counts.values()) == 455
    assert counts == EXPECTED_TYPE_COUNTS, counts

    verify_witness("three_matching")
    verify_witness("two_path_plus_edge")

    print("colour-indexed missing-pair triples:", len(ordered_triples))
    print("repeated-pair triples rejected literally:", len(repeated))
    print("ordered distinct-pair triples:", len(distinct_ordered))
    print("unordered distinct labelled-edge sets:", sum(counts.values()))
    print("support graph census:", dict(sorted(counts.items())))
    print("explicit feasible response types: three_matching, two_path_plus_edge")

    if args.skip_ideals:
        print("three bad-type QQ ideals skipped by request")
        return

    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required for the exact QQ ideal audit")
    bad_types = ("three_star", "triangle", "three_path")
    outputs = []
    wall_started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_singular, name, executable, args.timeout): name
            for name in bad_types
        }
        for future in as_completed(futures):
            outputs.append(future.result())
    for name, variables, equations, digest, elapsed in sorted(outputs):
        print(
            name,
            "QQ ideal [1]",
            "variables", variables,
            "equations", equations,
            "sha256", digest,
            "seconds", f"{elapsed:.3f}",
        )
    print("parallel wall seconds:", f"{time.monotonic() - wall_started:.3f}")
    print("arbitrary-star monomial base-locus response classification: PASS")


if __name__ == "__main__":
    main()
