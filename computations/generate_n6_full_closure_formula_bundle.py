#!/usr/bin/env python3
"""Persist a deterministic full n=6 no-singleton CNF and semantic JSON."""

from __future__ import annotations

import argparse
from collections import Counter

import search_n6_full_closure_phase as phase
import search_parallel_binomial_nonzero_constants_cegar as toric


def generate(prefix, cap, minimum, add_known_phase_cores):
    searcher = phase.FullPhaseSearch(
        cap,
        "cadical195",
        proof_prefix=prefix,
        minimum=minimum,
    )
    try:
        if add_known_phase_cores:
            assert cap >= 35
            assert minimum is None or minimum <= 35
            selected = searcher.seed | phase.PHASE_HINT_ADDED
            fibres = searcher.exact_fibres(selected)
            histogram = Counter(
                len(terms)
                for word, terms in fibres.items()
                if len(set(word)) > 1
            )
            assert histogram == Counter({2: 71})
            mixed, rows = searcher.binomial_system(fibres)
            assert not toric.signed_quotient_lattice(
                rows, len(searcher.cells)
            )[0]
            triangles = searcher.unit_triangle_circuits(rows)
            assert len(triangles) == 73
            assert sum(
                searcher.add_phase_core(mixed, rows, indices)
                for indices in triangles
            ) == 73
        searcher.write_formula_bundle()
        print(
            f"PASS generated formula: variables={searcher.pool.top} "
            f"clauses={len(searcher.clauses)} "
            f"phase_cores={len(searcher.phase_core_records)}",
            flush=True,
        )
    finally:
        searcher.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix")
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--minimum", type=int)
    parser.add_argument("--add-known-phase-cores", action="store_true")
    args = parser.parse_args()
    generate(
        args.prefix,
        args.cap,
        args.minimum,
        args.add_known_phase_cores,
    )


if __name__ == "__main__":
    main()
