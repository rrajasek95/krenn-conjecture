#!/usr/bin/env python3
"""Generate/replay the named support certificate for F=C3+3P1."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

from pysat.solvers import Solver

import search_f5_support_sat as base
import verify_color_sensitive_support_obstruction as triangle


SCHEMA = "exceptional-triangle-support-v1"
EXCEPTIONAL = base.THREE_EDGE_GRAPHS["C3+3P1"]
DEFAULT_CERTIFICATE = Path("computations/exceptional_triangle_support_certificate.json")


def dimacs_bytes(variables, clauses):
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def parse_supports(raw):
    supports = {}
    for raw_edge, raw_cells in raw:
        edge = tuple(raw_edge)
        cells = {tuple(cell) for cell in raw_cells}
        assert edge in base.ALL_EDGES and cells
        assert cells <= set(base.CELLS)
        supports[edge] = cells
    return supports


def build(records):
    formula, pool, _active = base.support_formula(EXCEPTIONAL)
    automorphisms = triangle.graph_automorphisms(EXCEPTIONAL)
    base_clauses = [list(clause) for clause in formula.clauses]
    clauses = list(base_clauses)
    counts = Counter()

    for record in records:
        kind = record["kind"]
        supports = parse_supports(record["supports"])
        if kind == "partition-rank":
            assert triangle.deletion_witness(supports) is not None
        else:
            assert kind == "triangle-rank"
            assert triangle.triangle_rank_witness(supports, EXCEPTIONAL) is not None
        counts[kind] += 1

        orbit = set()
        for vertex_permutation in automorphisms:
            for color_permutation in itertools.permutations(base.COLORS):
                mapped = triangle.transform_supports(
                    supports, vertex_permutation, color_permutation
                )
                orbit.add(
                    tuple(triangle.subsupport_escape_clause(pool, EXCEPTIONAL, mapped))
                )
        clauses.extend([list(clause) for clause in sorted(orbit)])
    return pool.top, base_clauses, clauses, dict(counts)


def solve_twice(clauses):
    for solver_name in ("g4", "cadical195"):
        with Solver(name=solver_name, bootstrap_with=clauses) as solver:
            assert not solver.solve(), solver_name


def write_proof(prefix, variables, clauses):
    cnf_path = prefix.with_suffix(".cnf")
    proof_path = prefix.with_suffix(".drup")
    cnf_path.write_bytes(dimacs_bytes(variables, clauses))
    with Solver(name="g4", with_proof=True, bootstrap_with=clauses) as solver:
        assert not solver.solve()
        proof = solver.get_proof()
    assert proof
    additions = [line for line in proof if not line.startswith("d ")]
    proof_path.write_text("\n".join(additions) + "\n")
    print(f"wrote deletion-free DRUP: {len(additions)} additions")


def generate(path, proof_prefix=None):
    artifact = {}
    assert triangle.audit("C3+3P1", EXCEPTIONAL, artifact_sink=artifact)
    assert artifact["transfers"] == 0
    variables, base_clauses, clauses, counts = build(artifact["records"])
    assert counts == artifact["witness_counts"]
    assert sum(counts.values()) == artifact["support_blocks"]
    solve_twice(clauses)
    payload = {
        "schema": SCHEMA,
        "exceptional_edges": [list(edge) for edge in sorted(EXCEPTIONAL)],
        "variables": variables,
        "base_clauses": len(base_clauses),
        "augmented_clauses": len(clauses),
        "counts": counts,
        "base_cnf_sha256": hashlib.sha256(dimacs_bytes(variables, base_clauses)).hexdigest(),
        "augmented_cnf_sha256": hashlib.sha256(dimacs_bytes(variables, clauses)).hexdigest(),
        "records": artifact["records"],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        f"wrote {path}: {len(artifact['records'])} support blocks; "
        f"sha256={payload['augmented_cnf_sha256']}"
    )
    if proof_prefix is not None:
        write_proof(proof_prefix, variables, clauses)


def replay(path, proof_prefix=None):
    payload = json.loads(path.read_text())
    assert payload["schema"] == SCHEMA
    assert payload["exceptional_edges"] == [list(edge) for edge in sorted(EXCEPTIONAL)]
    variables, base_clauses, clauses, counts = build(payload["records"])
    assert variables == payload["variables"]
    assert len(base_clauses) == payload["base_clauses"]
    assert len(clauses) == payload["augmented_clauses"]
    assert counts == payload["counts"]
    assert hashlib.sha256(dimacs_bytes(variables, base_clauses)).hexdigest() == payload["base_cnf_sha256"]
    assert hashlib.sha256(dimacs_bytes(variables, clauses)).hexdigest() == payload["augmented_cnf_sha256"]
    solve_twice(clauses)
    print(
        f"PASS exceptional triangle: {len(payload['records'])} named blocks "
        f"{counts}; sha256={payload['augmented_cnf_sha256']}"
    )
    if proof_prefix is not None:
        write_proof(proof_prefix, variables, clauses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--proof-prefix", type=Path)
    args = parser.parse_args()
    if args.generate:
        generate(args.certificate, args.proof_prefix)
    else:
        replay(args.certificate, args.proof_prefix)


if __name__ == "__main__":
    main()
