#!/usr/bin/env python3
"""Repair an exact binary n=8 realization into a ternary one.

The fixed 0/1 block is the rational Delta_(8,2) realization audited by
``verify_n8_pair_cap_obstruction.py``.  A best four-edge colour-2 matching
is added.  All absent cells wholly inside the 0/1 colour block are forbidden,
so later support choices cannot change that binary sub-tensor; every optional
cell has colour 2 at at least one endpoint.

The 17-cell seed has four mixed singleton fibres, three mixed binomials, and
pure fibre sizes (1,2,1).  The generic exact sparse CEGAR engine searches for
an unrestricted multi-term completion over the complex torus.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product

import search_n8_sparse_triple_completion as sparse


# Vertices in the source verifier are numbered 1,...,8; these are the same
# cells after shifting to 0,...,7.  Only support is fixed here: the completion
# search may choose any nonzero complex weights on the retained chart.
BINARY_SUPPORT = frozenset({
    (0, 1, 0, 0), (0, 1, 1, 0),
    (2, 3, 0, 0), (1, 3, 0, 0), (0, 2, 1, 0),
    (0, 5, 1, 1), (1, 2, 1, 1), (3, 4, 1, 1),
    (0, 4, 1, 1), (3, 5, 1, 1),
    (4, 6, 0, 0), (5, 7, 0, 0), (6, 7, 1, 1),
})

THIRD_MATCHING = frozenset({
    (0, 3, 2, 2), (1, 2, 2, 2),
    (4, 7, 2, 2), (5, 6, 2, 2),
})

SEED = BINARY_SUPPORT | THIRD_MATCHING
ALL_CELLS = frozenset(
    (u, v, left, right)
    for u, v in combinations(range(sparse.N), 2)
    for left, right in product(range(sparse.Q), repeat=2)
)
FORBIDDEN = frozenset(
    cell for cell in ALL_CELLS
    if cell[2] < 2 and cell[3] < 2 and cell not in BINARY_SUPPORT
)


def audit_seed(solver_name, forbidden=FORBIDDEN):
    search = sparse.SparseCompletionSearch(
        None, solver_name, seed_cells=SEED, forbidden_cells=forbidden
    )
    try:
        fibres = sparse.exact_fibres(search, SEED)
        histogram = Counter(
            len(terms) for colouring, terms in fibres.items()
            if len(set(colouring)) > 1
        )
        pure_sizes = [
            len(fibres[(colour,) * sparse.N]) for colour in range(sparse.Q)
        ]
        assert len(SEED) == 17
        assert histogram == {1: 4, 2: 3}
        assert pure_sizes == [1, 2, 1]
        assert len(FORBIDDEN) == 99
        return histogram, pure_sizes
    finally:
        search.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=28)
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--core-batch", type=int, default=256)
    parser.add_argument("--keep-survivors", type=int, default=100)
    parser.add_argument("--audit-seed", action="store_true")
    parser.add_argument("--allow-binary-changes", action="store_true")
    args = parser.parse_args()
    forbidden = frozenset() if args.allow_binary_changes else FORBIDDEN
    histogram, pure_sizes = audit_seed(args.solver, forbidden)
    print(
        f"SEED_AUDIT cells=17 forbidden={len(forbidden)} "
        f"mixed={dict(histogram)} pure={pure_sizes}",
        flush=True,
    )
    if args.audit_seed:
        return
    sparse.run(
        args.cap, args.solver, args.max_rounds, args.core_batch,
        False, args.keep_survivors,
        seed_cells=SEED, forbidden_cells=forbidden,
    )


if __name__ == "__main__":
    main()
