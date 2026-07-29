#!/usr/bin/env python3
"""Generate the exact-35 semantic CNF bundle without running an UNSAT proof."""

from __future__ import annotations

import argparse
from collections import Counter

import search_n6_full_closure_phase as phase
import search_parallel_binomial_nonzero_constants_cegar as toric


def generate(prefix):
    searcher = phase.FullPhaseSearch(
        35,
        "cadical195",
        proof_prefix=prefix,
        minimum=35,
    )
    try:
        selected = searcher.seed | phase.PHASE_HINT_ADDED
        assert len(selected) == 35
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
            f"PASS generated exact-35 formula: variables={searcher.pool.top} "
            f"clauses={len(searcher.clauses)} phase_cores=73",
            flush=True,
        )
    finally:
        searcher.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix")
    args = parser.parse_args()
    generate(args.prefix)


if __name__ == "__main__":
    main()
