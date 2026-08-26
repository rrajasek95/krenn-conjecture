#!/usr/bin/env python3
"""All-k valuation audit for pure powers times the cross-cap 10-minor."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K1_PATH = HERE / "audit_crosscap_pure_cone_k1.py"
K1_SHA256 = "fed7765f1733ce5d21bed9a3f69a4b13a068f7f11e02ae0d2609df91b6a60328"
OUT = HERE / "results_crosscap_all_k_valuation.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_k1():
    require(sha256(K1_PATH.read_bytes()).hexdigest() == K1_SHA256,
            "k1 checker changed")
    spec = importlib.util.spec_from_file_location("crosscap_k1", K1_PATH)
    require(spec is not None and spec.loader is not None, "cannot load k1")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


K = load_k1()
C = K.C


def weight_at_k(k):
    base = (
        (3, 3, 3), (3, 3, 3), (1, 0, 0), (1, 0, 0),
        (0, 0, 0), (3, 3, 3), (1, 0, 0), (4, 3, 3),
    )
    return tuple(tuple(value + (k if colour == 0 else 0)
                       for colour, value in enumerate(row))
                 for row in base)


def compatible_words(weight):
    return tuple(word for word in product(range(3), repeat=8)
                 if all(weight[site][word[site]] for site in range(8)))


def specialize(source, t):
    answer = {edge: [row[:] for row in matrix]
              for edge, matrix in source.items()}
    answer[(0, 1)][0][0] = Fraction(t)
    return answer


def supported_matchings(source):
    answer = []
    for matching in C.MATCHINGS:
        if all(any(C.cell(source, u, v, a, b)
                   for a in range(3) for b in range(3))
               for u, v in matching):
            answer.append(matching)
    return tuple(answer)


def word_text(word):
    return "".join(map(str, word))


def run(mutate=False):
    seed = 1
    base = K.diagonal_hub_leaf_source(seed)
    minor0, matrices0 = K.canonical_minor(base, mutate=mutate)
    require(minor0 and all(C.determinant(matrix) for matrix in matrices0),
            "base response open failed")

    source1 = specialize(base, 1)
    source2 = specialize(base, 2)
    minor1, _ = K.canonical_minor(source1, mutate=mutate)
    minor2, _ = K.canonical_minor(source2, mutate=mutate)
    require(minor0 == minor1 == minor2, (minor0, minor1, minor2))

    support = supported_matchings(source1)
    require(len(support) == 6, len(support))
    require(all((0, 1) in matching for matching in support), support)

    pure = (0,) * 8
    pure0 = C.amplitude(base, pure)
    pure1 = C.amplitude(source1, pure)
    pure2 = C.amplitude(source2, pure)
    require(pure0 == 0 and pure1 and pure2 == 2 * pure1,
            (pure0, pure1, pure2))

    reference_compatible = None
    k_checks = []
    for k in range(1, 9):
        weight = weight_at_k(k)
        compatible = compatible_words(weight)
        if reference_compatible is None:
            reference_compatible = compatible
        require(compatible == reference_compatible, (k, compatible))
        require(len(compatible) == 81 and pure in compatible, len(compatible))
        mixed = tuple(word for word in compatible if word != pure)
        values1 = [C.amplitude(source1, word) for word in mixed]
        values2 = [C.amplitude(source2, word) for word in mixed]
        require(not any(values1) and not any(values2), (k, values1, values2))
        coefficient = (pure1 ** k) * minor0
        require(coefficient, (k, coefficient))
        k_checks.append({
            "k": k,
            "target_degree": 20 + 4 * k,
            "compatible_words": 81,
            "compatible_mixed_words": 80,
            "mixed_generator_order": "infinity",
            "target_order": k,
            "target_leading_coefficient": C.fraction_string(coefficient),
        })

    # Literal reason the same 80 words persist: sites 2,3,4,6 only carry
    # colour zero, while sites 0,1,5,7 carry all three colours.
    forced = {2: 0, 3: 0, 4: 0, 6: 0}
    require(all(all(word[site] == colour for site, colour in forced.items())
                for word in reference_compatible), "forced word drift")

    result = {
        "status": "PASS exact all-k cross-cap valuation separation",
        "upstream": {
            "path": str(K1_PATH.relative_to(ROOT)),
            "sha256": K1_SHA256,
        },
        "family": {
            "formula": "diagonal K_(3,5) hub-leaf source + t*A_01[0,0]",
            "base_seed": seed,
            "base_source_sha256": C.source_digest(base),
            "supported_perfect_matchings": len(support),
            "every_supported_matching_uses_01": True,
            "F_00000000": f"{C.fraction_string(pure1)}*t",
            "crosscap_minor": C.fraction_string(minor0),
            "crosscap_minor_independent_of_t": True,
        },
        "fine_grade_theorem": {
            "target": "F_00000000^k * canonical cross-cap 10-minor",
            "k_range": "all integers k>=1",
            "forced_word_coordinates": {str(site): colour
                                        for site, colour in forced.items()},
            "free_word_coordinates": [0, 1, 5, 7],
            "compatible_word_count": 81,
            "compatible_mixed_word_count": 80,
            "compatible_words": [word_text(word)
                                 for word in reference_compatible],
        },
        "valuation_theorem": {
            "target_order": "k",
            "compatible_mixed_generator_order": "infinity",
            "compatible_translated_row_order": "infinity for every polynomial multiplier",
            "reason": (
                "A supported amplitude must use A_01[0,0], hence w0=w1=0. "
                "The remaining diagonal K_(3,5) matching pairs the forced "
                "zero-colour leaves 2,3,4 with hubs 5,6,7, so w5=w6=w7=0. "
                "Together with forced w6=0, the only compatible nonzero word "
                "is the pure word 00000000."
            ),
            "first_k_attaining_target_order": None,
        },
        "bounded_replay_k1_through_k8": k_checks,
        "consequence": (
            "For every k>=1, F_00000000^k times the canonical cross-cap "
            "10-minor is outside the homogeneous ideal generated by all "
            "mixed X5 amplitudes over Q. Pure-power coning can never prove "
            "this flatness minor."
        ),
        "scope_guard": (
            "The theorem is for homogeneous mixed-X5 membership and the one "
            "canonical minor. It does not decide the inhomogeneous normalized "
            "ideal, radical membership, or wider minors involving every site."
        ),
        "mutation": mutate,
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-crossed-orientation", action="store_true")
    args = parser.parse_args()
    result = run(mutate=args.mutate_crossed_orientation)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.mutate_crossed_orientation:
        require(OUT.exists() and OUT.read_text() == text,
                "PASS hostile orientation mutation changed artifact")
    if args.check_results:
        require(OUT.exists() and OUT.read_text() == text,
                "result artifact mismatch")
    if args.write_results:
        OUT.write_text(text)
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": result["logical_sha256"],
        "target_order": result["valuation_theorem"]["target_order"],
        "mixed_order": result["valuation_theorem"][
            "compatible_mixed_generator_order"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
