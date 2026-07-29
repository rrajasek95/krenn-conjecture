#!/usr/bin/env python3
"""Lazy exact search for a twelve-site recurrence-shadow countermodel.

The recurrence formula is solved first without partition clauses.  Every
proper feasible three-colour partition in a model is then added as an exact
blocking clause.  Termination with SAT is a fully audited countermodel;
termination with UNSAT proves the twelve-site shadow impossible.  The
ordered color-zero deletion flag is a sound exhaustive symmetry break.
"""

from __future__ import annotations

import argparse
import itertools
from time import monotonic

from pysat.solvers import Solver

from verify_diagonal_recurrence_obstruction import (
    audit_countermodel,
    build,
    canonical_matching,
    even_masks,
)


def ordered_flag_units(n: int, z) -> list[int]:
    """Canonicalize one recursively extracted ordered color-zero matching."""
    full = (1 << n) - 1
    units = []
    prefix = 0
    suffix = full
    for u, v in canonical_matching(n):
        selected_edge = (1 << u) | (1 << v)
        units.append(z(0, selected_edge))
        if suffix != selected_edge:
            prefix |= selected_edge
            suffix ^= selected_edge
            units.append(z(0, suffix))
            units.append(-z(1, prefix))
            units.append(-z(2, prefix))
    return units


def feasible_families(n: int, positive: set[int], z):
    return tuple(
        frozenset(mask for mask in even_masks(n) if z(color, mask) in positive)
        for color in range(3)
    )


def violated_partition_clauses(n: int, families, z, limit: int):
    """Return up to ``limit`` exact no-cover clauses violated by one model."""
    full = (1 << n) - 1
    clauses = []
    total = 0
    for coloring in itertools.product(range(3), repeat=n):
        masks = [0, 0, 0]
        for vertex, color in enumerate(coloring):
            masks[color] |= 1 << vertex
        if any(mask.bit_count() % 2 for mask in masks) or full in masks:
            continue
        if all(masks[color] in families[color] for color in range(3)):
            total += 1
            if len(clauses) < limit:
                clauses.append([-z(color, masks[color]) for color in range(3)])
    return total, clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    # CaDiCaL supports adding clauses between solve calls.  Kissat's PySAT
    # wrapper is one-shot and must not be used for this incremental loop.
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument("--rounds", type=int, default=1000)
    parser.add_argument("--cuts-per-round", type=int, default=10000)
    args = parser.parse_args()

    n = 12
    started = monotonic()
    pool, cnf, z = build(n, include_partitions=False)
    units = ordered_flag_units(n, z)
    for literal in units:
        cnf.append([literal])
    print(
        f"base vars={pool.top} clauses={len(cnf.clauses)} units={len(units)}",
        flush=True,
    )

    cuts = 0
    with Solver(name=args.solver, bootstrap_with=cnf) as solver:
        for round_number in range(1, args.rounds + 1):
            sat = solver.solve()
            if not sat:
                print(
                    f"UNSAT after rounds={round_number - 1} cuts={cuts} "
                    f"seconds={monotonic() - started:.3f}",
                    flush=True,
                )
                return
            positive = {literal for literal in solver.get_model() if literal > 0}
            families = feasible_families(n, positive, z)
            total, clauses = violated_partition_clauses(
                n, families, z, args.cuts_per_round
            )
            print(
                f"round={round_number} feasible="
                f"{tuple(map(len, families))} violated={total} "
                f"adding={len(clauses)} cuts={cuts}",
                flush=True,
            )
            if not clauses:
                encoded = audit_countermodel(n, positive, z)
                print(
                    "EXACT RECURRENCE COUNTERMODEL (bit position = subset mask):",
                    *(hex(bits) for bits in encoded),
                    sep="\n",
                    flush=True,
                )
                return
            for clause in clauses:
                solver.add_clause(clause)
            cuts += len(clauses)

    raise SystemExit(f"round limit reached after {cuts} exact cuts")


if __name__ == "__main__":
    main()
