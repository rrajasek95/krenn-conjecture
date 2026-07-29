#!/usr/bin/env python3
"""Clean-room audit of the arbitrary-star three-monomial obstruction.

This file deliberately does not import the primary checker.  It reconstructs
the two-endpoint response coefficients, enumerates all 15^3 colour-indexed
missing-pair triples (including repetitions), checks coordinate witnesses for
the two feasible graph types, and sends independently ordered generators for
the other three types to Singular over QQ.  The ideals are affine and
unsaturated: zero, dependent, dense, and cancelling star rows are all present.
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


VERTICES = tuple(range(6))
AXES = tuple(range(3))
PAIRS = tuple(combinations(VERTICES, 2))

# Deliberately different vertices, endpoint orientations, variable order, and
# generator order from the primary computation.
MODELS = {
    "K1_3": ((4, 5), (2, 5), (0, 5)),
    "K3": ((3, 5), (1, 3), (1, 5)),
    "P4": ((3, 5), (0, 3), (0, 2)),
    "P3_plus_K2": ((5, 2), (2, 4), (1, 3)),
    "three_K2": ((0, 5), (1, 4), (2, 3)),
}

UNORDERED_COUNTS = Counter(
    {"K1_3": 60, "K3": 20, "P4": 180, "P3_plus_K2": 180, "three_K2": 15}
)

# Filled after independently freezing the rendered generator streams.
EXPECTED_SHA256 = {
    "K1_3": "5db7d6a3e8a71ac92c07ecf8d1ad0d268c54806826c7ba20685aa9d7889bd783",
    "K3": "3c6580eed805be19a40c83a302d60b382323ac07fdd6057bea21c22ae69aee32",
    "P4": "e58f7e989eb125e5b5d9bf4217e77f8982dfa4d45eb6efad1eb056105627545c",
}

ROW_ORDER = (2, 0, 1)
AXIS_ORDER = (1, 2, 0)
GENERATOR_ROW_ORDER = (1, 2, 0)
GENERATOR_COLUMN_ORDER = (2, 0, 1)
GENERATOR_AXIS_A_ORDER = (2, 1, 0)
GENERATOR_AXIS_B_ORDER = (1, 0, 2)
EDGE_INDEX_ORDER = (2, 0, 1)


def shape(edge_triple):
    degrees = Counter(endpoint for edge in edge_triple for endpoint in edge)
    key = (len(degrees), tuple(sorted(degrees.values(), reverse=True)))
    table = {
        (4, (3, 1, 1, 1)): "K1_3",
        (3, (2, 2, 2)): "K3",
        (4, (2, 2, 1, 1)): "P4",
        (5, (2, 1, 1, 1, 1)): "P3_plus_K2",
        (6, (1, 1, 1, 1, 1, 1)): "three_K2",
    }
    return table[key]


def name(family, row, site, axis):
    return f"{family}{site}{axis}{row}"


def lhs_terms(edge, i, j, alpha, beta):
    """The two endpoint orders as a canonical pair of commutative monomials."""
    u, v = edge
    return (
        (name("a", i, u, alpha), name("b", j, v, beta)),
        (name("b", j, u, alpha), name("a", i, v, beta)),
    )


def equation_data(edges, k, i, j, alpha, beta):
    return lhs_terms(edges[k], i, j, alpha, beta), int(
        i == j == k and alpha == beta == k
    )


def response_space_separation(edges):
    """Different lift colours have disjoint response spaces, repeats included."""
    for k, ell in combinations(AXES, 2):
        outside = set(VERTICES) - set(edges[k]) - set(edges[ell])
        assert outside, (edges, k, ell)
        # At any such site the two spaces have independent fixed axes k and ell.
        witness_site = min(outside)
        assert k != ell and witness_site not in edges[k] and witness_site not in edges[ell]


def repeated_pair_certificate(edges):
    collisions = [(i, k) for i, k in combinations(AXES, 2) if edges[i] == edges[k]]
    assert collisions
    i, k = collisions[0]
    lhs_nonzero, rhs_nonzero = equation_data(edges, i, i, i, i, i)
    lhs_zero, rhs_zero = equation_data(edges, k, i, i, i, i)
    assert lhs_nonzero == lhs_zero
    assert (rhs_nonzero, rhs_zero) == (1, 0)


def zero_forms():
    return {
        family: {
            (row, site, axis): 0
            for row, site, axis in product(AXES, VERTICES, AXES)
        }
        for family in ("a", "b")
    }


def feasible_witness(model):
    edges = MODELS[model]
    forms = zero_forms()
    # The chosen P3+K2 representative is oriented 5 -> 2 -> 4; the matching
    # has arbitrary independent orientations.  In both cases edge k receives
    # p_k at its first endpoint and s_k at its second endpoint.
    for k, (tail, head) in enumerate(edges):
        forms["a"][k, tail, k] = 1
        forms["b"][k, head, k] = 1
    return edges, forms


def evaluate_response(forms, edge, i, j, alpha, beta):
    u, v = edge
    return (
        forms["a"][i, u, alpha] * forms["b"][j, v, beta]
        + forms["b"][j, u, alpha] * forms["a"][i, v, beta]
    )


def check_witness(model):
    edges, forms = feasible_witness(model)
    for k in AXES:
        for i, j, alpha, beta in product(AXES, repeat=4):
            observed = evaluate_response(forms, edges[k], i, j, alpha, beta)
            expected = int(i == j == k and alpha == beta == k)
            assert observed == expected, (
                model, k, i, j, alpha, beta, observed, expected
            )


def variables_for(edges):
    used = tuple(sorted({vertex for edge in edges for vertex in edge}, reverse=True))
    variables = tuple(
        name(family, row, site, axis)
        for family in ("b", "a")
        for site in used
        for axis in AXIS_ORDER
        for row in ROW_ORDER
    )
    assert len(variables) == 18 * len(used)
    assert len(set(variables)) == len(variables)
    return variables


def render_generator(edges, k, i, j, alpha, beta):
    terms, rhs = equation_data(edges, k, i, j, alpha, beta)
    # Reverse both the endpoint-term order and the factor order within each
    # monomial relative to the mathematical display.  The polynomial is the
    # same, but the frozen ledger is mechanically independent.
    rendered_terms = ["*".join(reversed(term)) for term in reversed(terms)]
    polynomial = "+".join(rendered_terms)
    if rhs:
        polynomial += "-1"
    return polynomial


def generators_for(edges):
    indices = tuple(
        (k, i, j, alpha, beta)
        for k in EDGE_INDEX_ORDER
        for beta in GENERATOR_AXIS_B_ORDER
        for alpha in GENERATOR_AXIS_A_ORDER
        for j in GENERATOR_COLUMN_ORDER
        for i in GENERATOR_ROW_ORDER
    )
    assert len(indices) == 243
    assert set(indices) == set(product(AXES, repeat=5))
    generators = tuple(
        render_generator(edges, k, i, j, alpha, beta)
        for k, i, j, alpha, beta in indices
    )
    return generators


def digest(generators):
    data = "\n".join(generators).encode("ascii") + b"\n"
    return hashlib.sha256(data).hexdigest()


def singular_input(model):
    edges = MODELS[model]
    variables = variables_for(edges)
    generators = generators_for(edges)
    ledger_hash = digest(generators)
    expected = EXPECTED_SHA256[model]
    if expected:
        assert ledger_hash == expected, (model, ledger_hash, expected)
    program = (
        f"ring independent_ring=0,({','.join(variables)}),dp;\n"
        f"ideal response_ideal={','.join(generators)};\n"
        "ideal independent_basis=slimgb(response_ideal);\n"
        f'print("MODEL {model}");\n'
        'print("BASIS_LENGTH");\nprint(size(independent_basis));\n'
        'print("FIRST_ELEMENT");\nprint(independent_basis[1]);\n'
    )
    return program, len(variables), len(generators), ledger_hash


def run_ideal(model, singular, timeout):
    program, variable_count, generator_count, ledger_hash = singular_input(model)
    started = time.monotonic()
    result = subprocess.run(
        (singular, "-q"),
        input=program,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=True,
    )
    elapsed = time.monotonic() - started
    assert not result.stderr.strip(), (model, result.stderr)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    length = lines[lines.index("BASIS_LENGTH") + 1]
    first = lines[lines.index("FIRST_ELEMENT") + 1]
    assert (length, first) == ("1", "1"), (model, result.stdout)
    return model, variable_count, generator_count, ledger_hash, elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-ideals", action="store_true")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    ordered = tuple(product(PAIRS, repeat=3))
    assert len(ordered) == 3375
    for edges in ordered:
        response_space_separation(edges)

    repeated = tuple(edges for edges in ordered if len(set(edges)) != 3)
    distinct = tuple(edges for edges in ordered if len(set(edges)) == 3)
    assert (len(repeated), len(distinct)) == (645, 2730)
    for edges in repeated:
        repeated_pair_certificate(edges)

    ordered_shape_counts = Counter(shape(edges) for edges in distinct)
    assert ordered_shape_counts == Counter(
        {model: 6 * count for model, count in UNORDERED_COUNTS.items()}
    )
    unordered_shape_counts = Counter(shape(edges) for edges in combinations(PAIRS, 3))
    assert unordered_shape_counts == UNORDERED_COUNTS

    check_witness("three_K2")
    check_witness("P3_plus_K2")

    print("colour-indexed pair triples checked:", len(ordered))
    print("repeated-pair contradictions:", len(repeated))
    print("ordered distinct triples:", len(distinct))
    print("unlabelled-edge-set census:", dict(sorted(unordered_shape_counts.items())))
    print("literal witnesses: three_K2, P3_plus_K2")

    for model in ("K1_3", "K3", "P4"):
        _, variables, generators, ledger_hash = singular_input(model)
        print(
            model,
            "ledger",
            "variables", variables,
            "generators", generators,
            "sha256", ledger_hash,
        )

    if args.skip_ideals:
        print("independent QQ unit-ideal replay skipped")
        return

    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular executable not found")
    outputs = []
    wall_start = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_ideal, model, singular, args.timeout): model
            for model in ("K1_3", "K3", "P4")
        }
        for future in as_completed(futures):
            outputs.append(future.result())
    for model, variables, generators, ledger_hash, elapsed in sorted(outputs):
        print(
            model,
            "unsaturated QQ ideal [1]",
            "variables", variables,
            "generators", generators,
            "sha256", ledger_hash,
            "seconds", f"{elapsed:.3f}",
        )
    print("parallel wall seconds:", f"{time.monotonic() - wall_start:.3f}")
    print("independent arbitrary-star monomial obstruction audit: PASS")


if __name__ == "__main__":
    main()
