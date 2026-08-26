#!/usr/bin/env python3
"""Exact k=1 pure-amplitude cone audit for the cross-cap 10-minor."""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = HERE / "audit_crosscap_response_curvature.py"
UPSTREAM_SHA256 = "93e5c85bde206c7d5a8ac28750bc5bde75083a84faebf2ba3e29de919bc2e238"
OUT = HERE / "results_crosscap_pure_cone_k1.json"
PORTS = tuple((site, colour) for site in range(8) for colour in range(3))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_upstream():
    require(sha256(UPSTREAM.read_bytes()).hexdigest() == UPSTREAM_SHA256,
            "upstream cross-cap checker changed")
    spec = importlib.util.spec_from_file_location("crosscap", UPSTREAM)
    require(spec is not None and spec.loader is not None, "cannot load upstream")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


U = load_upstream()
C = U.C


def coned_grade():
    base = (
        (3, 3, 3), (3, 3, 3), (1, 0, 0), (1, 0, 0),
        (0, 0, 0), (3, 3, 3), (1, 0, 0), (4, 3, 3),
    )
    return tuple(tuple(value + int(colour == 0)
                       for colour, value in enumerate(row))
                 for row in base)


def compatible_words(weight):
    return tuple(word for word in product(range(3), repeat=8)
                 if all(weight[site][word[site]] for site in range(8)))


def residual_degrees(weight, word):
    return tuple(weight[site][colour] - int(word[site] == colour)
                 for site, colour in PORTS)


@lru_cache(maxsize=None)
def count_partite_multigraphs(degrees):
    """Count monomials with the port degrees and no same-site edge."""
    if not any(degrees):
        return 1
    vertex = next(index for index, degree in enumerate(degrees) if degree)
    site = PORTS[vertex][0]
    degree = degrees[vertex]
    allowed = tuple(index for index in range(vertex + 1, len(degrees))
                    if degrees[index] and PORTS[index][0] != site)
    if sum(degrees[index] for index in allowed) < degree:
        return 0
    mutable = list(degrees)
    mutable[vertex] = 0
    total = 0

    def distribute(position, remaining):
        nonlocal total
        if remaining == 0:
            total += count_partite_multigraphs(tuple(mutable))
            return
        if position == len(allowed):
            return
        if sum(mutable[index] for index in allowed[position:]) < remaining:
            return
        index = allowed[position]
        maximum = min(mutable[index], remaining)
        original = mutable[index]
        for used in range(maximum + 1):
            mutable[index] = original - used
            distribute(position + 1, remaining - used)
        mutable[index] = original

    distribute(0, degree)
    return total


def diagonal_hub_leaf_source(seed):
    source = {(u, v): C.zero_matrix(3, 3)
              for u in range(8) for v in range(u + 1, 8)}
    for leaf in range(5):
        for hub in (5, 6, 7):
            for colour in range(3):
                source[(leaf, hub)][colour][colour] = (
                    2 + ((seed * 19 + leaf * 23 + hub * 29
                          + colour * 31 + leaf * hub * (colour + 1)) % 97)
                )
    return source


def canonical_minor(source, mutate=False):
    ae = U.response_map(source, (5, 7), (0, 1), mutate=mutate)
    be = U.response_map(source, (6, 7), (0, 1), mutate=mutate)
    af = U.response_map(source, (5, 7), (2, 3), mutate=mutate)
    bf = U.response_map(source, (6, 7), (2, 3), mutate=mutate)
    matrices = (ae, be, af, bf)
    if not all(C.determinant(matrix) for matrix in matrices):
        return None, matrices
    selected = [list(ae[row]) + [be[row][0]] for row in range(9)]
    selected.append(list(af[0]) + [bf[0][0]])
    return C.determinant(selected), matrices


def find_diagonal_guard(mutate=False):
    for seed in range(1, 1000):
        source = diagonal_hub_leaf_source(seed)
        minor, matrices = canonical_minor(source, mutate=mutate)
        if not minor:
            continue
        # The pure directional derivative in A_01[0,0].
        tangent = {edge: [row[:] for row in matrix]
                   for edge, matrix in source.items()}
        tangent[(0, 1)][0][0] = 1
        pure_derivative = C.amplitude(tangent, (0,) * 8)
        if pure_derivative:
            return seed, source, minor, matrices, pure_derivative
    raise RuntimeError("no diagonal guard in bounded seed range")


def word_text(word):
    return "".join(map(str, word))


def profile(word):
    counts = sorted(Counter(word).values(), reverse=True)
    return "+".join(map(str, counts))


def run(mutate=False):
    # Small exact controls for the multigraph/monomial recursion.
    test = [0] * 24
    for index in (0, 3, 6, 9):
        test[index] = 1
    require(count_partite_multigraphs(tuple(test)) == 3, "four-port DP control")
    test = [0] * 24
    test[0] = test[3] = 2
    require(count_partite_multigraphs(tuple(test)) == 1, "double-edge DP control")
    test = [0] * 24
    test[0] = test[1] = 1
    require(count_partite_multigraphs(tuple(test)) == 0, "same-site DP control")

    weight = coned_grade()
    compatible = compatible_words(weight)
    pure = (0,) * 8
    mixed = tuple(word for word in compatible if word != pure)
    require(len(compatible) == 81 and len(mixed) == 80,
            (len(compatible), len(mixed)))

    multiplier_counts = {}
    profile_counts = Counter()
    total_rows = 0
    for word in mixed:
        count = count_partite_multigraphs(residual_degrees(weight, word))
        require(count, word)
        multiplier_counts[word_text(word)] = count
        profile_counts[profile(word)] += 1
        total_rows += count

    seed, source, minor, matrices, pure_derivative = find_diagonal_guard(
        mutate=mutate)
    response_determinants = [C.determinant(matrix) for matrix in matrices]
    require(all(response_determinants), response_determinants)

    # At the K_(3,5) base every top amplitude vanishes.  In the direction
    # d/dA_01[0,0], diagonal stars make every compatible mixed derivative
    # vanish, while the pure derivative is nonzero.
    require(all(C.amplitude(source, word) == 0 for word in compatible),
            "base top row nonzero")
    tangent_source = {edge: [row[:] for row in matrix]
                      for edge, matrix in source.items()}
    tangent_source[(0, 1)][0][0] = 1
    mixed_derivatives = {
        word_text(word): C.amplitude(tangent_source, word)
        for word in mixed
    }
    require(not any(mixed_derivatives.values()), mixed_derivatives)
    require(C.amplitude(tangent_source, pure) == pure_derivative,
            "pure derivative drift")
    derivative_support = []
    for word in product(range(3), repeat=8):
        derivative = C.amplitude(tangent_source, word)
        if derivative:
            derivative_support.append((word_text(word), derivative))
    compatible_labels = {word_text(word) for word in compatible}
    compatible_derivative_support = [
        item for item in derivative_support if item[0] in compatible_labels
    ]
    require(compatible_derivative_support == [("00000000", pure_derivative)],
            compatible_derivative_support)
    target_pairing = pure_derivative * minor
    require(target_pairing, target_pairing)

    multiplier_histogram = Counter(multiplier_counts.values())
    result = {
        "status": "PASS exact k=1 pure-cone cross-cap separator",
        "upstream": {
            "path": str(UPSTREAM.relative_to(ROOT)),
            "sha256": UPSTREAM_SHA256,
        },
        "target": {
            "formula": "F_00000000 * canonical degree-20 cross-cap 10-minor",
            "source_degree": 24,
            "fine_weight": [list(row) for row in weight],
        },
        "compatible_word_census": {
            "all_count": len(compatible),
            "mixed_count": len(mixed),
            "pure_words": [word_text(pure)],
            "mixed_profile_counts": dict(sorted(profile_counts.items())),
            "mixed_words": [word_text(word) for word in mixed],
        },
        "translated_row_universe": {
            "multiplier_degree": 20,
            "counts_by_word": multiplier_counts,
            "count_value_histogram": {
                str(value): count for value, count in sorted(
                    multiplier_histogram.items())
            },
            "exact_total_rows": total_rows,
            "dp_cache_states": count_partite_multigraphs.cache_info().currsize,
            "dp_controls": {
                "four_distinct_unit_ports": 3,
                "one_double_edge": 1,
                "same_site_pair": 0,
            },
            "materialized": False,
        },
        "separator": {
            "type": "first directional jet at an exact zero-output source",
            "base_support": "diagonal K_(hubs {5,6,7}, leaves {0,...,4})",
            "base_seed": seed,
            "base_source_sha256": C.source_digest(source),
            "direction": "d/dA_01[0,0]",
            "all_81_compatible_amplitudes_at_base_zero": True,
            "all_80_mixed_first_derivatives_zero": True,
            "compatible_derivative_support": ["00000000"],
            "global_derivative_support_count": len(derivative_support),
            "pure_first_derivative": C.fraction_string(pure_derivative),
            "canonical_minor_at_base": C.fraction_string(minor),
            "target_pairing": C.fraction_string(target_pairing),
            "response_determinants": [
                C.fraction_string(value) for value in response_determinants
            ],
            "proof": (
                "For every multiplier m and mixed generator F_w, "
                "d(mF_w)=m*dF_w+(dm)*F_w=0 at the base. For the target, "
                "d(F_0 P)=dF_0*P is nonzero."
            ),
        },
        "exact_nonmembership": (
            "F_00000000 times the canonical cross-cap 10-minor is not in "
            "the degree-24 homogeneous ideal generated by all mixed X5 rows "
            "over Q."
        ),
        "scope_guard": (
            "This closes only k=1 homogeneous coning. It does not decide "
            "membership using the inhomogeneous equations F_c-1, higher pure "
            "powers, radical membership, or a wider all-site response minor."
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
        "compatible_mixed_words": result["compatible_word_census"]["mixed_count"],
        "translated_rows": result["translated_row_universe"]["exact_total_rows"],
        "target_pairing": result["separator"]["target_pairing"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
