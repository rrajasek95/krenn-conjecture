#!/usr/bin/env python3
"""Exact two-cap response curvature and normalized packet counterguard."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations"
             / "unaudited-codex-fullrank-response-holonomy-no-go-2026-08-23"
             / "audit_fullrank_response_holonomy.py")
CORE_SHA256 = "eb85cbac3307f81bd8600b7cf2ace5d1ef10193b346a75aedda140227ce58945"
OUT = HERE / "results_crosscap_response_curvature.json"
CAPS = ((6, 7), (5, 7))
COMMON_EDGES = ((0, 1), (2, 3))
COLOURS = range(3)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_core():
    require(sha256(CORE_PATH.read_bytes()).hexdigest() == CORE_SHA256,
            "upstream fixed-cap checker changed")
    spec = importlib.util.spec_from_file_location("fixed_cap_core", CORE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load core")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = load_core()


def stored_dense_block(leaf, hub):
    return [[Fraction(
        1 + ((((leaf * 8 + hub) * 9 + a * 3 + b + 1) ** 2
              + 17 * leaf + 29 * hub + 5 * a + 7 * b) % 97)
    ) for b in COLOURS] for a in COLOURS]


def build_hub_leaf_source():
    source = {(u, v): C.zero_matrix(3, 3)
              for u in range(8) for v in range(u + 1, 8)}
    # Exact K_(3,5) support, hubs 5,6,7 and leaves 0,...,4.
    for leaf in range(5):
        for hub in (5, 6, 7):
            source[(leaf, hub)] = stored_dense_block(leaf, hub)
    return source


def response_map(source, cap, edge, mutate=False):
    p, q = cap
    a, b = edge
    rows = []
    for alpha in COLOURS:
        for beta in COLOURS:
            row = []
            for i in COLOURS:
                for j in COLOURS:
                    first = C.cell(source, p, a, i, alpha) * C.cell(
                        source, q, b, j, beta)
                    if mutate:
                        second = C.cell(source, p, b, i, alpha) * C.cell(
                            source, q, a, j, beta)
                    else:
                        second = C.cell(source, p, b, i, beta) * C.cell(
                            source, q, a, j, alpha)
                    row.append(first + second)
            rows.append(row)
    return rows


def normalize_pure_rows(source):
    """Add the sole leaf-leaf edge 01, one diagonal cell per colour."""
    coefficients = []
    for colour in COLOURS:
        probe = {edge: [row[:] for row in matrix]
                 for edge, matrix in source.items()}
        probe[(0, 1)][colour][colour] = Fraction(1)
        word = (colour,) * 8
        coefficient = C.amplitude(probe, word)
        require(coefficient, ("zero pure cofactor", colour))
        source[(0, 1)][colour][colour] = Fraction(1, coefficient)
        coefficients.append(coefficient)
    require([C.amplitude(source, (colour,) * 8) for colour in COLOURS]
            == [Fraction(1)] * 3, "pure normalization failed")
    return coefficients


def profile(word):
    return "+".join(map(str, sorted(Counter(word).values(), reverse=True)))


def word_packet(source):
    residual_words = ("010122", "012021")
    rows = []
    for residual in residual_words:
        for i in COLOURS:
            for j in COLOURS:
                word = tuple(map(int, residual)) + (i, j)
                rows.append(("".join(map(str, word)), profile(word),
                             C.amplitude(source, word)))
    require(all(not value for _, _, value in rows), rows)
    return residual_words, rows


def logical_digest(payload):
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"))
                  .encode()).hexdigest()


def run(mutate=False):
    source = build_hub_leaf_source()
    pure_coefficients = normalize_pure_rows(source)
    residual_words, rows = word_packet(source)

    maps = {(cap, edge): response_map(source, cap, edge, mutate=mutate)
            for cap in CAPS for edge in COMMON_EDGES}
    determinants = {key: C.determinant(matrix) for key, matrix in maps.items()}
    require(all(determinants.values()), ("response chart singular", determinants))
    inverses = {key: C.inverse(matrix) for key, matrix in maps.items()}
    adjugates = {key: C.scalar_matrix(determinants[key], inverses[key])
                 for key in maps}

    # T_e sends cap-67 K coordinates to cap-57 K coordinates by matching the
    # response on the common residual edge e.
    transitions = {
        edge: C.matmul(inverses[((5, 7), edge)], maps[((6, 7), edge)])
        for edge in COMMON_EDGES
    }
    curvature = C.matsub(transitions[(2, 3)], transitions[(0, 1)])
    curvature_rank = C.matrix_rank(curvature)
    require(curvature_rank > 0, "cross-cap curvature vanished")
    first_curvature = next((i, j, curvature[i][j])
                           for i in range(9) for j in range(9)
                           if curvature[i][j])

    # Clear the two destination determinants.  This is the degree-36
    # source polynomial whose vanishing is equivalent to path independence.
    d01 = determinants[((5, 7), (0, 1))]
    d23 = determinants[((5, 7), (2, 3))]
    cleared = C.matsub(
        C.scalar_matrix(d01, C.matmul(adjugates[((5, 7), (2, 3))],
                                      maps[((6, 7), (2, 3))])),
        C.scalar_matrix(d23, C.matmul(adjugates[((5, 7), (0, 1))],
                                      maps[((6, 7), (0, 1))])),
    )
    require(C.matrix_rank(cleared) == curvature_rank,
            (C.matrix_rank(cleared), curvature_rank))

    # Strong gauge obstruction, unchanged by the single diagonal 01 edge.
    h1 = C.even_cycle_transport(source, (6, 0, 7, 1))
    h2 = C.even_cycle_transport(source, (6, 0, 7, 2))
    commutator = C.matsub(C.matmul(h1, h2), C.matmul(h2, h1))
    commutator_rank = C.matrix_rank(commutator)
    require(commutator_rank > 0, "source accidentally channel diagonalizable")

    # Exact scope census: the chosen rows and pure targets pass, but this is
    # not a full X5 source.  Enumerate all top words to pin the failure count.
    amplitude_census = Counter()
    mixed_profile_census = Counter()
    nonzero_mixed = []
    for word in product(range(3), repeat=8):
        value = C.amplitude(source, word)
        if not value:
            amplitude_census["zero"] += 1
        elif len(set(word)) == 1:
            amplitude_census["pure_nonzero"] += 1
        else:
            amplitude_census["mixed_nonzero"] += 1
            mixed_profile_census[profile("".join(map(str, word)))] += 1
            if len(nonzero_mixed) < 20:
                nonzero_mixed.append(("".join(map(str, word)), C.fraction_string(value)))
    require(amplitude_census["pure_nonzero"] == 3, amplitude_census)
    require(amplitude_census["mixed_nonzero"] > 0,
            "accidental normalized full-X5 counterexample")

    profile_histogram = Counter(row_profile for _, row_profile, _ in rows)
    determinant_strings = {
        f"cap{cap[0]}{cap[1]}_R{edge[0]}{edge[1]}": C.fraction_string(value)
        for (cap, edge), value in determinants.items()
    }
    first_commutator = next((i, j, commutator[i][j])
                            for i in range(3) for j in range(3)
                            if commutator[i][j])
    core = {
        "status": "PASS exact cross-cap curvature counterguard",
        "upstream_checker": {
            "path": str(CORE_PATH.relative_to(ROOT)),
            "sha256": CORE_SHA256,
        },
        "caps": [list(cap) for cap in CAPS],
        "common_response_edges": [list(edge) for edge in COMMON_EDGES],
        "response_determinants": determinant_strings,
        "all_four_response_ranks": 9,
        "transition": "T_e=(R_e^57)^(-1) R_e^67",
        "cross_cap_curvature": {
            "rational_formula": "T_23-T_01",
            "cleared_source_degree": 36,
            "cleared_formula": (
                "delta_01^57 adj(R_23^57)R_23^67 "
                "- delta_23^57 adj(R_01^57)R_01^67"
            ),
            "rank": curvature_rank,
            "first_nonzero_entry": [first_curvature[0], first_curvature[1],
                                    C.fraction_string(first_curvature[2])],
        },
        "literal_rows": {
            "residual_words": list(residual_words),
            "full_words": [label for label, _, _ in rows],
            "row_count": len(rows),
            "profile_histogram": dict(sorted(profile_histogram.items())),
            "all_zero": True,
        },
        "pure_normalization": {
            "values": [1, 1, 1],
            "unique_leaf_edge": "01",
            "unnormalized_cofactor_coefficients": [
                C.fraction_string(value) for value in pure_coefficients
            ],
            "normalized_cells": [
                C.fraction_string(source[(0, 1)][colour][colour])
                for colour in COLOURS
            ],
        },
        "source_guard": {
            "support": "K_(hubs {5,6,7}, leaves {0,1,2,3,4}) plus diagonal edge 01",
            "source_sha256": C.source_digest(source),
            "top_amplitude_census": dict(sorted(amplitude_census.items())),
            "nonzero_mixed_profile_census": dict(sorted(
                mixed_profile_census.items())),
            "first_nonzero_mixed_rows": nonzero_mixed,
            "cycle_commutator_rank": commutator_rank,
            "first_nonzero_cycle_commutator_entry": [
                first_commutator[0], first_commutator[1],
                C.fraction_string(first_commutator[2]),
            ],
        },
        "scope_guard": (
            "The source satisfies the three pure normalizations and the 18 "
            "displayed literal full-X5 rows, including 12 profile332 rows, "
            "but not all 6558 mixed rows. It proves those rows do not make "
            "the cross-cap transition flat; it is not an exact GHZ source."
        ),
        "verdict": (
            "Overlapping caps produce a genuine degree-36 curvature, but it "
            "is not killed by pure normalization plus the smallest two "
            "profile332/422 cross-word packets. Any positive flatness theorem "
            "must use a larger jointly coupled mixed-row family; equality of "
            "one common response edge is only a chosen identification."
        ),
        "mutation": mutate,
    }
    core["logical_sha256"] = logical_digest(core)
    return core


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
                "PASS hostile crossed-orientation mutation changed artifact")
    if args.check_results:
        require(OUT.exists() and OUT.read_text() == text,
                "result artifact mismatch")
    if args.write_results:
        OUT.write_text(text)
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": result["logical_sha256"],
        "curvature_rank": result["cross_cap_curvature"]["rank"],
        "mixed_failures": result["source_guard"]["top_amplitude_census"][
            "mixed_nonzero"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
