#!/usr/bin/env python3
"""SAT search for a W3 x W3 support using at most a given source count."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from w3w3_support_core import (
    OCCURRENCES,
    SOURCES,
    TARGET_WORDS,
    WORDS,
    audit_occurrence_support,
    audit_target_cover,
)


def require(condition: bool, detail) -> None:
    if not condition:
        raise RuntimeError(detail)


def equivalent_and(formula: CNF, output: int, inputs) -> None:
    inputs = tuple(inputs)
    formula.append([output] + [-value for value in inputs])
    for value in inputs:
        formula.append([-output, value])


def build_formula(maximum_sources: int, forbid_singletons: bool = True):
    require(0 <= maximum_sources <= len(SOURCES), maximum_sources)
    pool = IDPool()
    formula = CNF()
    source_variables = {
        source: pool.id("source_" + "_".join(map(str, source)))
        for source in SOURCES
    }
    occurrence_variables = {}
    encoded_words = WORDS if forbid_singletons else tuple(sorted(TARGET_WORDS))
    for word in encoded_words:
        local = []
        word_text = "".join(map(str, word))
        for matching_index, occurrence in enumerate(OCCURRENCES[word]):
            variable = pool.id(f"occurrence_{word_text}_{matching_index}")
            equivalent_and(
                formula,
                variable,
                (source_variables[source] for source in occurrence),
            )
            occurrence_variables[word, matching_index] = variable
            local.append(variable)
        if word in TARGET_WORDS:
            formula.append(local)
        elif forbid_singletons:
            # No forbidden coefficient may have exactly one monomial.
            for index, variable in enumerate(local):
                formula.append(
                    [-variable]
                    + [other for j, other in enumerate(local) if j != index]
                )

    cardinality = CardEnc.atmost(
        lits=list(source_variables.values()),
        bound=maximum_sources,
        vpool=pool,
        encoding=EncType.seqcounter,
    )
    formula.extend(cardinality.clauses)
    return formula, pool, source_variables, occurrence_variables


def dimacs_bytes(formula: CNF) -> bytes:
    lines = [f"p cnf {formula.nv} {len(formula.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in formula.clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def solve(
    maximum_sources: int,
    solver_name: str,
    with_proof: bool,
    forbid_singletons: bool = True,
):
    formula, pool, source_variables, occurrence_variables = build_formula(
        maximum_sources, forbid_singletons
    )
    started = time.monotonic()
    with Solver(
        name=solver_name,
        bootstrap_with=formula.clauses,
        with_proof=with_proof,
    ) as solver:
        satisfiable = solver.solve()
        elapsed = time.monotonic() - started
        model = solver.get_model() if satisfiable else None
        proof = solver.get_proof() if with_proof and not satisfiable else None
    positive = {literal for literal in (model or ()) if literal > 0}
    support = tuple(
        source for source, variable in source_variables.items() if variable in positive
    )
    if not satisfiable:
        audited = None
    elif forbid_singletons:
        audited = audit_occurrence_support(support, maximum_sources)
    else:
        audited = audit_target_cover(support, maximum_sources)
    payload = {
        "schema": (
            "w3w3-occurrence-support-v1"
            if forbid_singletons
            else "w3w3-target-cover-v1"
        ),
        "status": "sat" if satisfiable else "unsat",
        "maximum_sources": maximum_sources,
        "solver": solver_name,
        "elapsed_seconds": elapsed,
        "variables": formula.nv,
        "clauses": len(formula.clauses),
        "source_variables": len(source_variables),
        "occurrence_variables": len(occurrence_variables),
        "target_words": ["".join(map(str, word)) for word in sorted(TARGET_WORDS)],
        "forbidden_singleton_constraints": forbid_singletons,
        "audited_model": audited,
    }
    return formula, proof, payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-sources", type=int, default=9)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--target-cover-only", action="store_true")
    arguments = parser.parse_args()

    formula, proof, payload = solve(
        arguments.maximum_sources,
        arguments.solver,
        arguments.proof is not None,
        not arguments.target_cover_only,
    )
    raw_cnf = dimacs_bytes(formula)
    payload["cnf_sha256"] = hashlib.sha256(raw_cnf).hexdigest()
    if arguments.cnf is not None:
        arguments.cnf.write_bytes(raw_cnf)
    if arguments.proof is not None:
        require(payload["status"] == "unsat", "proof requested for SAT instance")
        # CaDiCaL emits optional deletion records.  Freeze a deletion-free
        # DRUP trace so the repository's deliberately small checker examines
        # every retained line as a reverse-unit-propagation addition.
        additions = tuple(
            line for line in (proof or ()) if not line.startswith("d ")
        )
        raw_proof = ("\n".join(additions) + "\n").encode("ascii")
        arguments.proof.write_bytes(raw_proof)
        payload["proof_sha256"] = hashlib.sha256(raw_proof).hexdigest()
        payload["proof_lines"] = len(additions)
        payload["proof_deletions_removed"] = len(proof or ()) - len(additions)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output is not None:
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
