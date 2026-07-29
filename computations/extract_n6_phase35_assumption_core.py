#!/usr/bin/env python3
"""Extract a solver-certified subset of the 73 exact-35 phase clauses."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import monotonic

import search_n6_full_closure_phase as phase
import verify_n6_full_closure_phase_certificate as replay


def extract(source_prefix, target_prefix, solver_name):
    source_prefix = Path(source_prefix)
    source_payload = json.loads(source_prefix.with_suffix(".json").read_text())
    assert source_payload["order"] == phase.N
    records = source_payload["phase_cores"]
    assert records

    source = phase.FullPhaseSearch(
        source_payload["cap"],
        solver_name,
        minimum=source_payload.get("minimum"),
    )
    try:
        assert len(source.clauses) == source_payload["base_clauses"]
        phase_clauses = [
            replay.core_clause_and_rows(source, record) for record in records
        ]
        selectors = tuple(
            range(source.pool.top + 1, source.pool.top + 1 + len(records))
        )
        for selector, clause in zip(selectors, phase_clauses, strict=True):
            source.solver.add_clause(clause + [-selector])

        started = monotonic()
        assert not source.solver.solve(assumptions=list(selectors))
        elapsed = monotonic() - started
        core = set(source.solver.get_core() or ())
        assert core and core <= set(selectors)
        chosen_indices = tuple(
            index for index, selector in enumerate(selectors) if selector in core
        )
        print(
            f"ASSUMPTION_CORE solver={solver_name} seconds={elapsed:.3f} "
            f"phase_clauses={len(records)} core={len(chosen_indices)}",
            flush=True,
        )
    finally:
        source.delete()

    target = phase.FullPhaseSearch(
        source_payload["cap"],
        "cadical195",
        proof_prefix=target_prefix,
        minimum=source_payload.get("minimum"),
    )
    try:
        target.phase_core_records = [records[index] for index in chosen_indices]
        target.clauses.extend(phase_clauses[index] for index in chosen_indices)
        _cnf, _proof, json_path, payload = target.write_formula_bundle()
        payload.update(
            {
                "assumption_core_source": str(source_prefix),
                "source_phase_cores": len(records),
                "selected_phase_core_indices": list(chosen_indices),
                "core_solver": solver_name,
                "core_seconds": elapsed,
            }
        )
        json_path.write_text(json.dumps(payload, indent=2) + "\n")
        print(
            f"PASS persisted reduced formula: variables={target.pool.top} "
            f"clauses={len(target.clauses)} "
            f"phase_cores={len(chosen_indices)}",
            flush=True,
        )
    finally:
        target.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_prefix")
    parser.add_argument("target_prefix")
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    extract(args.source_prefix, args.target_prefix, args.solver)


if __name__ == "__main__":
    main()
