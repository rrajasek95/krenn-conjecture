#!/usr/bin/env python3
"""Classify all mixed word orbits at the frozen rational 78-zero."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BRIDGE = (ROOT / "computations" /
          "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20")
VERIFY_PATH = HERE / "verify_pair_constant_78_counterexample.py"
OUT = HERE / "results_nonpairconstant_breakers.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXPORT = load_module("n8_breakers_export",
                     BRIDGE / "export_orbit0_cutoff_seed.py")
VERIFY = load_module("n8_breakers_verify", VERIFY_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def transform_word(word, action):
    sites, colours = EXPORT.STABILIZER[action]
    answer = [None] * 8
    for old_site in range(8):
        answer[sites[old_site]] = colours[word[old_site]]
    return tuple(answer)


def canonical_word(word):
    return min(transform_word(word, action)
               for action in range(len(EXPORT.STABILIZER)))


def encode_value(value):
    return f"{value.numerator}/{value.denominator}"


def main():
    values = VERIFY.assignment()
    orbits = defaultdict(list)
    for word in product(VERIFY.BASE.COLORS, repeat=VERIFY.BASE.N):
        if len(set(word)) == 1:
            continue
        orbits[canonical_word(word)].append(word)
    require(len(orbits) == 27, "mixed word orbit count changed")
    require(sum(map(len, orbits.values())) == 6558,
            "mixed literal word count changed")

    records = []
    for representative, words in sorted(orbits.items()):
        amplitudes = Counter()
        profiles = Counter()
        for word in words:
            value, _ = VERIFY.evaluate_word(word, values)
            amplitudes[value] += 1
            profiles[tuple(sorted(Counter(word).values(), reverse=True))] += 1
        require(len(profiles) == 1, "word orbit mixes colour profiles")
        profile = next(iter(profiles))
        nonzero_words = sum(count for value, count in amplitudes.items()
                            if value)
        records.append({
            "representative": "".join(map(str, representative)),
            "orbit_size": len(words),
            "colour_profile": list(profile),
            "nonzero_words_at_point": nonzero_words,
            "amplitudes": {
                encode_value(value): count
                for value, count in sorted(amplitudes.items())
            },
        })

    breakers = [record for record in records
                if record["nonzero_words_at_point"]]
    require([record["representative"] for record in breakers] == [
        "00000101", "00010111", "00010122", "00010212",
        "01010101", "01010202",
    ], "breaker orbit list changed")
    smallest = min(breakers, key=lambda record: record["orbit_size"])
    require((smallest["representative"], smallest["orbit_size"],
             smallest["nonzero_words_at_point"]) ==
            ("01010101", 48, 36), "smallest breaker changed")
    profile_332 = [record for record in records
                   if record["colour_profile"] == [3, 3, 2]]
    require(len(profile_332) == 5 and
            sum(record["orbit_size"] for record in profile_332) == 1680 and
            not any(record["nonzero_words_at_point"]
                    for record in profile_332),
            "(3,3,2) zero classification changed")

    # Sign mutation must change the breaker census.
    hostile = VERIFY.assignment(((VERIFY.Q(1), VERIFY.Q(2, 3)),
                                 (VERIFY.Q(0), VERIFY.Q(-1))))
    hostile_value, _ = VERIFY.evaluate_word(tuple(map(int, "00000011")),
                                            hostile)
    require(hostile_value != 0, "hostile mutation did not fire")

    result = {
        "status": "UNAUDITED exact rational mixed-word orbit census",
        "stabilizer_order": len(EXPORT.STABILIZER),
        "mixed_literal_words": sum(map(len, orbits.values())),
        "mixed_word_orbits": len(records),
        "breaker_orbits": len(breakers),
        "breaker_literal_words": sum(
            record["nonzero_words_at_point"] for record in breakers
        ),
        "smallest_breaker": smallest,
        "profile_332_orbits": len(profile_332),
        "profile_332_literal_words": sum(
            record["orbit_size"] for record in profile_332
        ),
        "profile_332_nonzero_words": 0,
        "records": records,
        "hostile_pairconstant_value": [hostile_value.numerator,
                                       hostile_value.denominator],
        "conclusion": (
            "Exactly six orbit-0 stabilizer word orbits detect the rational "
            "78-generator common zero. The smallest is 01010101 (orbit 48, "
            "36 nonzero evaluations). Every (3,3,2) generator still vanishes "
            "because the point has only same-colour cells; therefore the "
            "(3,3,2) family alone cannot remove this witness."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("non-pair-constant breaker census: PASS")
    print("mixed orbits / breakers:", len(records), len(breakers))
    print("smallest breaker:", smallest["representative"],
          smallest["orbit_size"], smallest["nonzero_words_at_point"])
    print("(3,3,2) orbits / words / nonzero:",
          len(profile_332), sum(r["orbit_size"] for r in profile_332), 0)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
