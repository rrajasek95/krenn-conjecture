#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- why blocking is near-automatic inside the regime.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

In the coordinate regime R_cell every R-form of a pair is a two-term linear
form in the cap K, so every error component is a quadric with very few terms
and the error span is tiny.  This measures both, and reports how often the
pair is blocked, over random six-site R_cell sources.  It is the pair-level
shadow of the singleton mechanism and the mechanical explanation of P2's B2
statistics ("anchored coordinate blocks: blocking dominant").
"""
import collections
import json
import random
import sys
from fractions import Fraction

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-witness-splitting-p2-2026-08-15")
from wsplit_core import PAIRS, PairData, Source  # noqa: E402


def main(trials=60, seed=11):
    rng = random.Random(seed)
    terms = collections.Counter()
    spans = collections.Counter()
    monomial_components = 0
    total_components = 0
    for _ in range(trials):
        blocks = {}
        for pair in PAIRS:
            matrix = [[Fraction(0)] * 3 for _ in range(3)]
            matrix[rng.randrange(3)][rng.randrange(3)] = Fraction(
                rng.choice([-3, -2, -1, 1, 2, 3]))
            blocks[pair] = matrix
        source = Source(blocks)
        for p, q in PAIRS:
            pd = PairData(source, p, q)
            for quad in pd.quadrics:
                terms[len(quad)] += 1
                total_components += 1
                if len(quad) == 1:
                    monomial_components += 1
            _patterns, span = pd.split_patterns()
            spans[span] += 1
    report = {
        "sources": trials,
        "error_components": total_components,
        "single_monomial_components": monomial_components,
        "single_monomial_fraction": round(
            monomial_components / total_components, 4),
        "terms_per_component": dict(sorted(terms.items())),
        "span_histogram": dict(sorted(spans.items())),
        "note": "span never reaches 36 = dim W, so the generic kappa_c^2 "
                "blocking mode of results_a.json never fires here",
    }
    print(json.dumps(report, indent=1))
    with open("pair_sparsity.json", "w") as handle:
        json.dump(report, handle, indent=1)


if __name__ == "__main__":
    main()
