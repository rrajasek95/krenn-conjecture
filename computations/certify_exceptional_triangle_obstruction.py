#!/usr/bin/env python3
"""Generate/replay the named support certificate for F=C3+3P1.

Every check below raises instead of asserting.  A bare ``assert`` is deleted
by ``python3 -O``, and here the witness audit and both UNSAT solves used to
sit *inside* assert tests, so ``-O`` skipped the entire semantic replay and
still printed the digest it had read out of the certificate file.
"""

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


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def dimacs_bytes(variables, clauses):
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def parse_supports(raw):
    supports = {}
    for raw_edge, raw_cells in raw:
        edge = tuple(raw_edge)
        cells = {tuple(cell) for cell in raw_cells}
        require(
            edge in base.ALL_EDGES and cells,
            f"support edge {edge} is not a nonempty edge of the graph",
        )
        require(cells <= set(base.CELLS), f"support of {edge} leaves the cells")
        supports[edge] = cells
    return supports


def build(records):
    formula, pool, _active = base.support_formula(EXCEPTIONAL)
    automorphisms = triangle.graph_automorphisms(EXCEPTIONAL)
    base_clauses = [list(clause) for clause in formula.clauses]
    clauses = list(base_clauses)
    counts = Counter()

    for index, record in enumerate(records):
        kind = record["kind"]
        supports = parse_supports(record["supports"])
        if kind == "partition-rank":
            require(
                triangle.deletion_witness(supports) is not None,
                f"no deletion witness for partition-rank block {index}",
            )
        else:
            require(kind == "triangle-rank", f"unknown witness kind {kind!r}")
            require(
                triangle.triangle_rank_witness(supports, EXCEPTIONAL) is not None,
                f"no triangle-rank witness for block {index}",
            )
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
            satisfiable = solver.solve()
            require(not satisfiable, f"{solver_name} reports SAT, expected UNSAT")


def write_proof(prefix, variables, clauses):
    cnf_path = prefix.with_suffix(".cnf")
    proof_path = prefix.with_suffix(".drup")
    cnf_path.write_bytes(dimacs_bytes(variables, clauses))
    with Solver(name="g4", with_proof=True, bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
        require(not satisfiable, "g4 reports SAT while emitting a proof")
        proof = solver.get_proof()
    require(proof, "g4 returned an empty proof")
    additions = [line for line in proof if not line.startswith("d ")]
    proof_path.write_text("\n".join(additions) + "\n")
    print(f"wrote deletion-free DRUP: {len(additions)} additions")


def generate(path, proof_prefix=None):
    artifact = {}
    require(
        triangle.audit("C3+3P1", EXCEPTIONAL, artifact_sink=artifact),
        "triangle audit of C3+3P1 failed",
    )
    require(artifact["transfers"] == 0, f"transfers={artifact['transfers']} != 0")
    variables, base_clauses, clauses, counts = build(artifact["records"])
    require(
        counts == artifact["witness_counts"],
        f"witness counts {counts} != {artifact['witness_counts']}",
    )
    require(
        sum(counts.values()) == artifact["support_blocks"],
        f"block total {sum(counts.values())} != {artifact['support_blocks']}",
    )
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
    require(payload["schema"] == SCHEMA, f"schema {payload['schema']!r} != {SCHEMA!r}")
    require(
        payload["exceptional_edges"] == [list(edge) for edge in sorted(EXCEPTIONAL)],
        "certificate is for a different exceptional edge set",
    )
    variables, base_clauses, clauses, counts = build(payload["records"])
    require(
        variables == payload["variables"],
        f"variables {variables} != {payload['variables']}",
    )
    require(
        len(base_clauses) == payload["base_clauses"],
        f"base clauses {len(base_clauses)} != {payload['base_clauses']}",
    )
    require(
        len(clauses) == payload["augmented_clauses"],
        f"augmented clauses {len(clauses)} != {payload['augmented_clauses']}",
    )
    require(counts == payload["counts"], f"counts {counts} != {payload['counts']}")
    base_digest = hashlib.sha256(dimacs_bytes(variables, base_clauses)).hexdigest()
    require(
        base_digest == payload["base_cnf_sha256"],
        f"base cnf sha256 {base_digest} != {payload['base_cnf_sha256']}",
    )
    augmented_digest = hashlib.sha256(dimacs_bytes(variables, clauses)).hexdigest()
    require(
        augmented_digest == payload["augmented_cnf_sha256"],
        f"augmented cnf sha256 {augmented_digest} != {payload['augmented_cnf_sha256']}",
    )
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
