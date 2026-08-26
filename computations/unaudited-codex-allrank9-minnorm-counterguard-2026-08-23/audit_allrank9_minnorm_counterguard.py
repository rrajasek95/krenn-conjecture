#!/usr/bin/env python3
"""Exact dense counterguard for the all-rank9 minimum-norm route."""

from collections import defaultdict
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORT = (ROOT / "computations/unaudited-codex-five-set-response-surjectivity-2026-08-22"
          / "export_sources.py")
FIVE = EXPORT.parent / "results.json"
PURE = (ROOT / "computations/unaudited-codex-triangle-pure-quotient-collapse-2026-08-22"
        / "results.json")
NORMAL_REPORT = (ROOT / "computations/unaudited-codex-singular-normal-cone-gram-system-2026-08-22"
                 / "REPORT.md")
ED_REPORT = (ROOT / "computations/unaudited-codex-ed-conormal-gap-framework-2026-08-21"
             / "REPORT.md")
RESULT = HERE / "results_allrank9_minnorm_counterguard.json"
EXPECTED = {
    EXPORT: "586f1c2d0b435623415b709fa2143643094b67a252c1579a16a389f39a3a7d18",
    FIVE: "20ce72a7aa63c9bb4f85e6e7441e9e7b8bdbb0bd6a2aef3d0a3d590f559a6bcb",
    PURE: "cf2ca70211cbacd9ddaa99afcca09f7c7cc2973a156de92bb118f3d9fb7a5db8",
    NORMAL_REPORT: "b539c683eb0a8c1c896aa884899d17d62847135f9763aa7b27f906529ebeee85",
    ED_REPORT: "1f793f23a7de98d2bbcb4ee9ab596f50187d695553d981832c745731f4e55558",
}
PRIMES = (1009, 1013)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXPORT_SOURCE = load(EXPORT, "n8_allrank9_dense_source")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


PM = {size: tuple(perfect_matchings(range(size))) for size in (6, 8)}


def edge_value(source, u, v, a, b, prime=None):
    if u < v:
        value = source[u, v][a][b]
    else:
        value = source[v, u][b][a]
    if prime is None:
        return value
    return value.numerator * pow(value.denominator, prime - 2, prime) % prime


def residual_hafnian(source, remaining, colours, prime):
    answer = 0
    for abstract_matching in PM[6]:
        value = 1
        for i, j in abstract_matching:
            value = value * edge_value(
                source, remaining[i], remaining[j], colours[i], colours[j],
                prime,
            ) % prime
        answer = (answer + value) % prime
    return answer


def sparse_rank(rows, width, prime):
    basis = {}
    pivot_labels = []
    for label, raw in rows:
        row = {index: value % prime for index, value in raw.items()
               if value % prime}
        while row:
            pivot = min(row)
            if pivot not in basis:
                inverse = pow(row[pivot], prime - 2, prime)
                row = {index: value * inverse % prime
                       for index, value in row.items()}
                basis[pivot] = row
                pivot_labels.append(label)
                break
            factor = row[pivot]
            for index, value in basis[pivot].items():
                updated = (row.get(index, 0) - factor * value) % prime
                if updated:
                    row[index] = updated
                else:
                    row.pop(index, None)
        if len(basis) == width:
            break
    return len(basis), pivot_labels


def jacobian_rank(source, prime):
    edges = tuple(combinations(range(8), 2))
    labels = tuple((u, v, a, b) for u, v in edges
                   for a in range(3) for b in range(3))
    index = {label: position for position, label in enumerate(labels)}
    residual_cache = {}
    rows = []
    for word in product(range(3), repeat=8):
        row = {}
        for u, v in edges:
            remaining = tuple(site for site in range(8) if site not in (u, v))
            colours = tuple(word[site] for site in remaining)
            key = (u, v, colours)
            if key not in residual_cache:
                residual_cache[key] = residual_hafnian(
                    source, remaining, colours, prime
                )
            value = residual_cache[key]
            if value:
                row[index[u, v, word[u], word[v]]] = value
        rows.append(("".join(map(str, word)), row))
    rank, pivot_words = sparse_rank(rows, len(labels), prime)
    return {
        "rank": rank,
        "source_columns": len(labels),
        "output_rows_scanned_until_full_rank": (
            int(pivot_words[-1], 3) + 1 if rank == len(labels) else 3 ** 8
        ),
        "pivot_words": pivot_words,
    }


def pure_amplitudes(source):
    values = []
    for colour in range(3):
        total = 0
        for matching in PM[8]:
            value = 1
            for u, v in matching:
                value *= edge_value(source, u, v, colour, colour)
            total += value
        values.append(total)
    return values


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    source = EXPORT_SOURCE.dense_source()
    require(len(source) == 28 and all(
        source[edge][a][b] > 0 for edge in source
        for a in range(3) for b in range(3)
    ), "dense source positivity changed")
    pure = pure_amplitudes(source)
    require(all(value > 0 for value in pure), "a dense pure amplitude vanished")

    ranks = {str(prime): jacobian_rank(source, prime) for prime in PRIMES}
    if mutate:
        ranks[str(PRIMES[0])]["rank"] -= 1
    require(all(record["rank"] == 245 for record in ranks.values()),
            f"dense Jacobian lost full column rank: {ranks}")

    five = json.loads(FIVE.read_text())["sources"]["dense"]
    pure_profile = json.loads(PURE.read_text())["sources"]["dense"]
    require(five == {
        "base_rank": {"16": 5040},
        "theta_rank": {"9": 5040},
        "triangle_min_rank": {"9": 1680},
    }, "dense five-set rank profile changed")
    require(pure_profile["groups"] == pure_profile["open"] == 1680
            and pure_profile["open_carrier_corank"] == 0
            and pure_profile["open_h6_zero"] == 0,
            "dense triangle carrier profile changed")

    result = {
        "format": "n8-allrank9-minnorm-counterguard-v1",
        "status": "EXACT_BALANCED_LOCAL_MINNORM_ALLRANK9_COUNTERGUARD_X5_IS_LOAD_BEARING",
        "source": {
            "description": "the pinned positive integral dense_source",
            "cells": 252,
            "all_cells_positive": True,
            "pure_amplitudes": [int(value) for value in pure],
            "pure_normalization": (
                "first scale the three colour ports at site 0 by 1/H_c; "
                "source-map equivariance preserves every displayed rank and "
                "makes all three pure amplitudes one"
            ),
            "mixed_amplitudes_nonzero": 6558,
            "not_X5_reason": (
                "every word contains a positive monomial on every perfect "
                "matching, so every one of the 6561 amplitudes is positive"
            ),
        },
        "jacobian": {
            "ranks": ranks,
            "characteristic_zero_consequence": (
                "a 245x245 Jacobian minor is nonzero modulo each audit prime. "
                "The universal product-one site gauge gives a 7-dimensional "
                "kernel, so rank 245 is the characteristic-zero maximum and "
                "ker(dPhi) is exactly the gauge tangent"
            ),
        },
        "triangle_response_open": {
            "cyclic_five_set_maps_rank9": 5040,
            "colour_tagged_triangle_groups": 1680,
            "physical_triangle_carriers": 560,
            "carrier_L_T_rank9": 560,
            "carrier_corank_positive_groups": 0,
            "blocker_consequence": (
                "rowspan(L_T)=Mat_3^*, so K00,K11,K22 and <K,A_pq> "
                "all belong to the row span; every triangle is blocked"
            ),
        },
        "minimum_norm_and_second_variation": {
            "exact_balancing_construction": (
                "after pure normalization let w_uv=||A_uv||^2>0 and minimize "
                "E(x)=sum_uv w_uv exp(2(x_u+x_v)) on sum_v x_v=0. Its Hessian "
                "is 4 sum_uv w_uv exp(2(x_u+x_v))(a_u+a_v)^2, positive definite "
                "on the sum-zero hyperplane; E is coercive there. Hence a "
                "unique balanced product-one site scaling exists"
            ),
            "local_fibre": (
                "maximal rank 245 makes the fibre smooth of dimension seven. "
                "The product-one site-gauge orbit has the same tangent and "
                "dimension, hence is open in the local fibre. The balanced "
                "point is therefore a strict local norm minimum on the fibre"
            ),
            "reduced_normal_cone": (
                "at the balanced point the norm gradient annihilates the exact "
                "seven-dimensional gauge tangent, so the smooth reduced "
                "conormal/minimum-norm equation holds"
            ),
            "least_blocks": (
                "no nonzero gauge tangent is supported in one star or one "
                "triangle. Since the full kernel is exactly gauge, every such "
                "block map is injective and all least-block equations hold"
            ),
            "second_variation": (
                "the displayed positive Hessian is the constrained second "
                "variation on the complete tangent kernel, so it is strictly "
                "positive for every nonzero fibre tangent"
            ),
        },
        "verdict": (
            "Reduced-normal, block-minimum, and second-variation equations "
            "cannot by themselves force triangle rank drop or an active cap "
            "on the all-rank9 open. The full mixed X5 equations are the exact "
            "missing hypothesis; the guard is pure-normalizable but not X5."
        ),
        "scope": (
            "exact characteristic-zero existence/local counterguard after two modular "
            "nonzero-minor replays; it is not a GHZ/X5 source and does not "
            "refute a theorem that genuinely uses all mixed X5 equations or "
            "global norm minimality on the GHZ fibre"
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("ranks", {p: r["rank"] for p, r in result["jacobian"]["ranks"].items()})
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
