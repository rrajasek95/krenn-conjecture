#!/usr/bin/env python3
"""Exact-Q replay of the Rust degree-17 F0^2*Delta separator."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
from hashlib import sha256
import importlib.util
from itertools import product
import json
from math import gcd, lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUST_SOURCE = HERE / "pure_square_cegar.rs"
RUST_RESULT = HERE / "results_pure_square_cegar_rust_p32003.json"
PYTHON_SOURCE = ROOT / "unaudited-codex-carrier-minor-pure-square-degree17-x5-2026-08-23" / "search_pure_square_carrier_minor_cegar.py"
COMMON_SOURCE = ROOT / "unaudited-codex-carrier-minor-coned-degree13-x5-2026-08-23" / "search_coned_carrier_minor_cegar.py"
DEG9_SOURCE = ROOT / "unaudited-codex-carrier-minor-degree9-x5-2026-08-23" / "audit_carrier_minor_degree9_x5.py"
OUT = HERE / "results_pure_square_separator_exact.json"
P = 32003
EXPECTED = {
    RUST_SOURCE: "1aab70090a5b3ca46388279a8f3f9dc6bb7d484c4c4ca6d33e6019721f59f532",
    RUST_RESULT: "9354f742bec952d3ed03da3e2f80291bd03224d1181f2d03e1906e50bf41a510",
    PYTHON_SOURCE: "b1c37e1e42fe05c234396b329c205420d7a216758710dc171291b2bd9efef484",
    COMMON_SOURCE: "519bbabc971396d086b3454d9f2ea28ec49a3316597f399a8e969944b265c093",
    DEG9_SOURCE: "02760ce5e08848f9930acb873dadd053c16dedebe72cd18e89e3c6789cdc265a",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_python_source():
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    spec = importlib.util.spec_from_file_location("pure_square_python", PYTHON_SOURCE)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, PYTHON_SOURCE)
    spec.loader.exec_module(module)
    return module


S = load_python_source()
C = S.C
D9 = S.D9
EDGES = tuple((u, v) for u in range(8) for v in range(u + 1, 8))


def parse_rust_monomial(ids):
    monomial = []
    for identifier in ids:
        edge_index, remainder = divmod(identifier, 9)
        colour_left, colour_right = divmod(remainder, 3)
        u, v = EDGES[edge_index]
        monomial.append((u, v, colour_left, colour_right))
    return tuple(sorted(monomial))


def rational_reconstruct(residue):
    candidates = []
    for denominator in range(1, 17):
        inverse = pow(denominator, P - 2, P)
        for numerator in range(-32, 33):
            if gcd(abs(numerator), denominator) != 1:
                continue
            if numerator * inverse % P == residue:
                value = Fraction(numerator, denominator)
                candidates.append(value)
    require(candidates, residue)
    candidates.sort(key=lambda value: (
        abs(value.numerator) + value.denominator,
        value.denominator, abs(value.numerator), value.numerator,
    ))
    best = candidates[0]
    require(sum(
        abs(value.numerator) + value.denominator
        == abs(best.numerator) + best.denominator
        for value in candidates
    ) == 1, (residue, candidates[:3]))
    return best


def integer_separator(record):
    rational = {
        parse_rust_monomial(entry["monomial"]):
        rational_reconstruct(entry["coefficient"])
        for entry in record["terminal_dual"]
    }
    denominator = reduce(lcm, (value.denominator for value in rational.values()), 1)
    integer = {
        monomial: int(value * denominator)
        for monomial, value in rational.items()
    }
    common = reduce(gcd, (abs(value) for value in integer.values()))
    integer = {monomial: value // common for monomial, value in integer.items()}
    return rational, integer, denominator, common


def exact_crossing_replay(functional, generators):
    labels = set()
    occurrences = 0
    for monomial in functional:
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = C.divides(monomial, term)
                if quotient is not None:
                    labels.add((word_index, quotient))
                    occurrences += 1
    by_word = Counter()
    nonzero = []
    intersection_histogram = Counter()
    for label in sorted(labels):
        by_word[D9.word_text(C.WORDS[label[0]])] += 1
        pairing = 0
        intersections = 0
        for monomial in C.row_monomials(label, generators):
            if monomial in functional:
                intersections += 1
                pairing += functional[monomial]
        intersection_histogram[intersections] += 1
        if pairing:
            nonzero.append((label, pairing))
    return labels, occurrences, by_word, intersection_histogram, nonzero


def validate_prefix(record):
    expected = {
        1: (4, 471, 420, 1, 4, 0, 1),
        15: (188, 16159, 86537, 7, 17, 0, 31999),
        28: (549, 47985, 196313, 33, 137, 2, 8),
        44: (1770, 127489, 1192963, 44, 175, 1, 6),
        69: (3258, 244678, 1849651, 119, 468, 4, 31975),
        90: (3924, 287797, 2711856, 6, 5, 0, 1),
        103: (4752, 333327, 5882357, 252, 279, 6, 24018),
        109: (5711, 391585, 12135624, 214, 172, 6, 31961),
    }
    for round_number, values in expected.items():
        row = record["rounds"][round_number - 1]
        actual = tuple(row[key] for key in (
            "rank_after", "columns_after", "basis_fill_after", "dual_support",
            "crossing_rows", "seed_index", "target_pairing",
        ))
        require(actual == values, (round_number, actual, values))
    return len(expected)


def audit(mutate=False):
    record = json.loads(RUST_RESULT.read_text())
    require(record["status"] == "SEPARATOR_MOD_P", record["status"])
    require((record["rounds_completed"], record["final_rank"],
             record["final_columns"], record["final_basis_fill"],
             record["final_dual_support"])
            == (130, 14979, 817554, 284356921, 102), record)
    prefix_checkpoints = validate_prefix(record)
    rational, functional, denominator, common = integer_separator(record)
    require(len(functional) == 102, len(functional))
    require({value.denominator for value in rational.values()} == {1, 2},
            {value.denominator for value in rational.values()})
    require(set(functional.values()) == {-8, -6, -4, -2, -1, 1, 2, 3, 4, 6, 10},
            set(functional.values()))
    if mutate:
        functional[min(functional)] += 1

    weight = (
        (3, 0, 0), (3, 0, 0), (3, 0, 0),
        (5, 0, 0), (5, 0, 0), (5, 0, 0),
        (3, 1, 1), (2, 3, 0),
    )
    require({D9.fine_weight_of_monomial(monomial) for monomial in functional}
            == {weight}, "separator fine weight")
    compatible = tuple(
        word for word in product(range(3), repeat=8)
        if all(weight[site][word[site]] for site in range(8))
    )
    require(compatible == ((0,) * 8,) + C.WORDS, compatible)
    generators = tuple(tuple(D9.amplitude(word)) for word in C.WORDS)
    labels, occurrences, by_word, intersection_histogram, nonzero = (
        exact_crossing_replay(functional, generators)
    )
    require(not nonzero, [
        [D9.word_text(C.WORDS[label[0]]), D9.monomial_text(label[1]), pairing]
        for label, pairing in nonzero[:3]
    ])
    require(len(labels) == 177, len(labels))

    oracle = S.TargetOracle()
    target_pairing = sum(
        coefficient * oracle.coefficient(monomial)
        for monomial, coefficient in functional.items()
    )
    require(target_pairing == 28, target_pairing)
    entries = [
        {"monomial": D9.monomial_text(monomial), "coefficient": coefficient}
        for monomial, coefficient in sorted(functional.items())
    ]
    separator_sha = sha256(json.dumps(
        entries, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    result = {
        "status": "PASS exact-Q nonmembership of F_00000000^2*Delta in degree-17 mixed X5",
        "target": {
            "formula": "F_00000000^2 * canonical Delta",
            "degree": 17,
            "delta_terms": len(oracle.delta),
            "pure_square_terms": len(oracle.pure_square),
            "fine_weight": [list(row) for row in weight],
            "target_pairing": target_pairing,
        },
        "fine_grade_word_census": {
            "all_compatible_words": [D9.word_text(word) for word in compatible],
            "pure_word_excluded_from_mixed_X5": "00000000",
            "mixed_words": [D9.word_text(word) for word in C.WORDS],
        },
        "rust_discovery": {
            "prime": P,
            "python_prefix_checkpoints_replayed": prefix_checkpoints,
            "python_prefix_through_round": 109,
            "rounds_including_terminal_scan": record["rounds_completed"],
            "final_rank": record["final_rank"],
            "final_columns": record["final_columns"],
            "final_basis_fill": record["final_basis_fill"],
            "terminal_dual_support": record["final_dual_support"],
            "elapsed_seconds_manifest": record["elapsed_seconds"],
        },
        "exact_separator": {
            "coefficient_ring": "Z",
            "support": len(functional),
            "rational_reconstruction_denominators": [1, 2],
            "clearing_denominator": denominator,
            "primitive_gcd_removed": common,
            "coefficient_set": sorted(set(functional.values())),
            "target_pairing": target_pairing,
            "quotient_occurrences_touching_support": occurrences,
            "distinct_translates_touching_support": len(labels),
            "translates_by_word": dict(by_word),
            "support_intersection_histogram": {
                str(key): value for key, value in sorted(intersection_histogram.items())
            },
            "nonzero_row_pairings": len(nonzero),
            "sha256": separator_sha,
            "entries": entries,
        },
        "theorem": (
            "The displayed primitive integer functional annihilates every "
            "degree-13 monomial translate of every mixed X5 amplitude in the "
            "target fine grade and pairs with F_00000000^2*Delta as 28. Hence "
            "the target is not in the degree-17 homogeneous mixed-X5 span over Q."
        ),
        "scope_guard": (
            "This is exact homogeneous nonmembership at the second pure "
            "saturation step. It does not by itself prove an all-k pattern, "
            "radical nonmembership, or a statement using F_00000000-1."
        ),
        "source_sha256": {str(path.relative_to(ROOT.parent)): digest
                          for path, digest in EXPECTED.items()},
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-separator", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate_separator)
    if args.check_results:
        require(OUT.exists() and json.loads(OUT.read_text()) == result,
                "stored result drift")
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    exact = result["exact_separator"]
    print(result["status"])
    print("round/rank/columns", result["rust_discovery"]["rounds_including_terminal_scan"],
          result["rust_discovery"]["final_rank"],
          result["rust_discovery"]["final_columns"])
    print("separator/touching/pairing", exact["support"],
          exact["distinct_translates_touching_support"], exact["target_pairing"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
