#!/usr/bin/env python3
"""Verify the nine-orbit rank-one six-site fibre certificate.

The nine representatives below are the vertex/color-orbits occurring in an
UNSAT core of ``rankone_anchor_fibre_certificate.json``.  Every generated
clause is first reconstructed and semantically audited by the companion
certificate module.  We then add every S_6 x S_3 relabeling to the exact
Boolean shadow and check UNSAT.  Optional output is a DIMACS instance and a
deletion-free DRUP trace.
"""

from __future__ import annotations

import argparse
from itertools import permutations
from pathlib import Path

from pysat.solvers import Solver

import certify_rankone_anchor_fibre_cegar as certificate
import search_rankone_anchor_fibre_cegar as search


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


REPRESENTATIVES = (
    {
        "kind": "nested", "lower_word": "000001", "pair": [0, 1],
        "upper_word": "010001", "triple": [0, 1, 8],
    },
    {
        "kind": "nested", "lower_word": "000011", "pair": [1, 2],
        "upper_word": "010011", "triple": [1, 2, 4],
    },
    {
        "kind": "nested", "lower_word": "000011", "pair": [1, 2],
        "upper_word": "110011", "triple": [1, 2, 11],
    },
    {
        "kind": "nested", "lower_word": "000011", "pair": [1, 4],
        "upper_word": "000010", "triple": [1, 4, 7],
    },
    {
        "kind": "nested", "lower_word": "000011", "pair": [1, 4],
        "upper_word": "000010", "triple": [1, 4, 13],
    },
    {
        "kind": "nested", "lower_word": "000012", "pair": [1, 2],
        "upper_word": "010012", "triple": [1, 2, 4],
    },
    {
        "kind": "nested", "lower_word": "000012", "pair": [1, 4],
        "upper_word": "000010", "triple": [1, 4, 13],
    },
    {
        "kind": "rectangle", "target_word": "000001",
        "triple": [0, 1, 3], "pair": [1, 3],
        "b_word": "000100", "d_word": "001001", "e_word": "001100",
    },
    {
        "kind": "rectangle", "target_word": "000001",
        "triple": [0, 1, 3], "pair": [1, 3],
        "b_word": "000101", "d_word": "001000", "e_word": "001100",
    },
)


MATCHING_INDEX = {matching: index
                  for index, matching in enumerate(search.MATCHINGS)}


def transform_word(text, vertex_permutation, colour_permutation):
    old = tuple(map(int, text))
    new = [None] * 6
    for vertex in search.VERTICES:
        new[vertex_permutation[vertex]] = colour_permutation[old[vertex]]
    return "".join(map(str, new))


def matching_map(vertex_permutation):
    result = []
    for matching in search.MATCHINGS:
        image = tuple(sorted(
            tuple(sorted((vertex_permutation[u], vertex_permutation[v])))
            for u, v in matching
        ))
        result.append(MATCHING_INDEX[image])
    return tuple(result)


def transform_record(record, vertex_permutation, colour_permutation,
                     matching_image):
    word = lambda key: transform_word(
        record[key], vertex_permutation, colour_permutation
    )
    indices = lambda key: sorted(matching_image[i] for i in record[key])
    if record["kind"] == "nested":
        return {
            "kind": "nested",
            "lower_word": word("lower_word"),
            "pair": indices("pair"),
            "upper_word": word("upper_word"),
            "triple": indices("triple"),
        }
    return {
        "kind": "rectangle",
        "target_word": word("target_word"),
        "triple": indices("triple"),
        "pair": indices("pair"),
        "b_word": word("b_word"),
        "d_word": word("d_word"),
        "e_word": word("e_word"),
    }


def orbit_clauses(compatible):
    clauses = {}
    orbit_sizes = []
    colour_permutations = tuple(permutations(range(3)))
    for representative_index, representative in enumerate(REPRESENTATIVES):
        certificate.decode_and_audit(representative, compatible)
        this_orbit = set()
        for vertex_permutation in permutations(range(6)):
            image = matching_map(vertex_permutation)
            for colour_permutation in colour_permutations:
                record = transform_record(
                    representative, vertex_permutation, colour_permutation,
                    image,
                )
                clause = certificate.decode_and_audit(record, compatible)
                # A CNF clause is a set; sorting removes duplicates caused by
                # the interchangeable b,d roles in a rectangle witness.
                normalized = tuple(sorted(set(clause)))
                this_orbit.add(normalized)
                clauses.setdefault(normalized, representative_index)
        orbit_sizes.append(len(this_orbit))
    return tuple(clauses), tuple(orbit_sizes)


def write_proof(prefix, top, clauses, solver_name):
    prefix = Path(prefix)
    cnf_path = prefix.with_suffix(".cnf")
    proof_path = prefix.with_suffix(".drup")
    cnf_path.write_bytes(certificate.dimacs_bytes(top, clauses))
    with Solver(name=solver_name, with_proof=True,
                bootstrap_with=clauses) as solver:
        require(
            not solver.solve(),
            "not solver.solve()",
        )
        proof = solver.get_proof()
    require(
        proof is not None,
        "proof is not None",
    )
    additions = [line for line in proof if not line.startswith("d ")]
    proof_path.write_text("\n".join(additions) + "\n")
    print(
        f"wrote {cnf_path}, {proof_path}; "
        f"proof additions={len(additions)}",
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--write-prefix")
    parser.add_argument(
        "--proof-solver", default="glucose4",
        choices=("glucose3", "glucose4", "lingeling"),
    )
    args = parser.parse_args()
    formula, _incidence, compatible = search.build_formula()
    extra, sizes = orbit_clauses(compatible)
    clauses = formula.clauses + list(extra)
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        require(
            not solver.solve(),
            "not solver.solve()",
        )
    print(
        f"PASS nine-orbit certificate: base_variables={formula.top} "
        f"base_clauses={len(formula.clauses)} orbit_sizes={sizes} "
        f"distinct_orbit_clauses={len(extra)} total_clauses={len(clauses)}",
        flush=True,
    )
    if args.write_prefix:
        write_proof(args.write_prefix, formula.top, clauses, args.proof_solver)


if __name__ == "__main__":
    main()
