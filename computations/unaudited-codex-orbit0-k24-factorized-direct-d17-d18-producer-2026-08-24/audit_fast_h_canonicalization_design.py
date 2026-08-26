#!/usr/bin/env python3
"""Prove the minimum-word-fibre replacement for the 384-action scan."""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVIDER = (ROOT / "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23"
            / "k24_factorized_gram_provider.py")
WITNESSES = HERE / "prefix1/literal_witnesses.tsv"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_provider():
    spec = importlib.util.spec_from_file_location("k24_fast_h_provider", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "provider loader")
    spec.loader.exec_module(module)
    return module


def fast_canonical_and_orbit(column, provider):
    word, multiplier = column
    word_images = [(action, provider.move_word(word, action))
                   for action in provider.H]
    minimum_word = min(image for _action, image in word_images)
    fibre_actions = [action for action, image in word_images
                     if image == minimum_word]
    fibre_multipliers = {
        bytes(sorted(provider.F.EXPORT.TRANSFORMS[action][cell]
                     for cell in multiplier))
        for action in fibre_actions
    }
    word_orbit_size = len({image for _action, image in word_images})
    # Orbit-fibre theorem: H acts transitively on the word orbit, and every
    # word fibre has the same number of distinct multiplier images.
    orbit_size = word_orbit_size * len(fibre_multipliers)
    return (minimum_word, min(fibre_multipliers)), orbit_size, len(fibre_actions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--witnesses", type=Path, default=WITNESSES)
    args = parser.parse_args()
    provider = load_provider()
    require(len(provider.H) == 384, "H order")
    words = [(a, a, b, b, c, c, d, d)
             for a in range(3) for b in range(3)
             for c in range(3) for d in range(3)
             if len({a, b, c, d}) > 1]
    require(len(words) == 78, "mixed word census")
    fibre_histogram = Counter()
    word_orbit_histogram = Counter()
    for word in words:
        images = [provider.move_word(word, action) for action in provider.H]
        minimum = min(images)
        fibre_histogram[sum(image == minimum for image in images)] += 1
        word_orbit_histogram[len(set(images))] += 1

    lines = args.witnesses.read_text().splitlines()
    require(len(lines) == 258, "257 witness rows")
    tested = 0
    repr_order_divergences = 0
    for line in lines[1:]:
        fields = line.split("\t")
        column = (tuple(map(int, fields[12])), bytes.fromhex(fields[13]))
        brute_orbit = provider.column_orbit(column)
        fast_canonical, fast_orbit, _actions = fast_canonical_and_orbit(column, provider)
        natural_canonical = min(brute_orbit)
        recorded_canonical = provider.parse_column_key(fields[14])
        require(recorded_canonical in brute_orbit, ("recorded rep outside orbit", fields[2]))
        require(recorded_canonical == natural_canonical,
                ("producer is not natural-order minimum", fields[2]))
        require(fast_canonical == natural_canonical, ("canonical mismatch", fields[2]))
        require(fast_orbit == len(brute_orbit) == int(fields[15]),
                ("orbit mismatch", fields[2]))
        if brute_orbit[0] != natural_canonical:
            # The provider intentionally sorts its cached orbit with key=repr.
            # Confusing that representational convention with natural tuple
            # ordering is the hostile mutation this audit guards against.
            repr_order_divergences += 1
        tested += 1

    weighted_actions = sum(size * count for size, count in fibre_histogram.items())
    mean_actions = weighted_actions / 78
    print(json.dumps({
        "status": "PASS_EXACT_MINIMUM_WORD_FIBRE_CANONICALIZATION_DESIGN",
        "theorem": ("canonical pair images occur over the minimum word; the actions over "
                    "that word form a stabilizer coset, and total pair-orbit size is "
                    "word-orbit-size times distinct multiplier images in that fibre"),
        "H_order": 384,
        "mixed_words": 78,
        "minimum_word_fibre_action_histogram": dict(sorted(fibre_histogram.items())),
        "word_orbit_size_histogram": dict(sorted(word_orbit_histogram.items())),
        "mean_actions_per_column": mean_actions,
        "brute_actions_per_column": 384,
        "action_reduction_ratio": 384 / mean_actions,
        "distributed_literal_columns_replayed": tested,
        "all_producer_representatives_in_provider_orbit": True,
        "all_producer_representatives_equal_natural_minimum": True,
        "all_fast_canonical_and_orbit_equal_natural_bruteforce": True,
        "provider_repr_order_vs_natural_order_divergences": repr_order_divergences,
        "hostile_repr_as_natural_guard": repr_order_divergences > 0,
        "scope": "canonicalization referee only; this audit launches no producer",
    }, indent=2))


if __name__ == "__main__":
    main()
