#!/usr/bin/env python3
"""Pair the lambda7/lambda8 control and top contractions with pure products.

The exact homogeneous grading is kept explicit.  The scalar calculations
called ``dehomogenized`` evaluate the actual normalized polynomial after
setting t=1; they are not homogeneous degree-12/24 saturation certificates.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TRANSFER_SCRIPT = (HERE.parent /
    "unaudited-codex-n8-degree8-transfer-audit-2026-08-23" /
    "audit_lambda7_lambda8_transfer.py")
CERTIFICATE = (HERE.parent /
    "unaudited-codex-n8-normalized-dfs-degree7-2026-08-23" /
    "results_degree8_rust_cegar.json")
CORE = (HERE.parent /
    "unaudited-codex-n8-normalized-dfs-degree7-2026-08-23" /
    "results_degree8_initial_core.json")
RESULT_PATH = HERE / "results_pure_product_pairings.json"
EXPECTED = {
    TRANSFER_SCRIPT: "a6197b5582369c2ea9c9729747e8260f5b96646676d1ebb02ba6440e40929e6a",
    CERTIFICATE: "5d39aa3d8d6ae83a8b2b357e148232fb1046e069c79bed5ff8e5ff970b6d8485",
    CORE: "0111fbb5c61c415d559d3927fcee1d4a451d546514ce9ffeef3f78502daa49b5",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    require(sha256(path.read_bytes()).hexdigest() == EXPECTED[path],
            f"source drift: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, str(path))
    spec.loader.exec_module(module)
    return module


def parse(record):
    return {
        bytes.fromhex(row): Fraction(numerator, denominator)
        for row, numerator, denominator in record
    }


def quotient_if_divides(target, factor):
    """Sorted-multiset quotient, or None if factor does not divide target."""
    answer = bytearray()
    i = j = 0
    while i < len(target) and j < len(factor):
        if target[i] < factor[j]:
            answer.append(target[i])
            i += 1
        elif target[i] == factor[j]:
            i += 1
            j += 1
        else:
            return None
    if j != len(factor):
        return None
    answer.extend(target[i:])
    return bytes(answer)


def audit(mutate=False):
    transfer = load(TRANSFER_SCRIPT, "pure_pair_transfer")
    source_module = transfer.load(transfer.AUDIT_PATH, "pure_pair_source")
    source = source_module.load_d7()
    core = json.loads(CORE.read_text())
    certificate = json.loads(CERTIFICATE.read_text())
    lambda7 = parse(core["degree7_dual"])
    lambda8 = parse(certificate["exact_extended_dual"])
    full7 = transfer.expand_invariant(source, lambda7)
    full8 = transfer.expand_invariant(source, lambda8)
    top8 = {row: value for row, value in full8.items() if len(row) == 8}

    pure = tuple(dict(source.normalized_generator(
        source.D5.word_code((colour,) * 8)
    )) for colour in range(3))
    require(all(len(polynomial) == 105 and polynomial.get(b"") == 1
                for polynomial in pure), "normalized pure polynomial changed")
    pure_terms = tuple(tuple(sorted(
        polynomial.items(), key=lambda item: (len(item[0]), item[0])
    )) for polynomial in pure)

    @lru_cache(None)
    def product_coefficient(target, colours):
        if not colours:
            return int(not target)
        colour = colours[0]
        total = 0
        for term, coefficient in pure_terms[colour]:
            if len(term) > len(target):
                break
            quotient = quotient_if_divides(target, term)
            if quotient is not None:
                total += coefficient * product_coefficient(quotient, colours[1:])
        return total

    factors = {"F": (0, 1, 2), "F2": (0, 1, 2, 0, 1, 2)}

    def pairing(functional, colours):
        return sum(value * product_coefficient(row, colours)
                   for row, value in functional.items())

    nonsupport = sorted(
        set(range(len(source.D5.COORDINATES))) - set(source.D5.SUPPORT_IDS)
    )
    channels = {
        coordinate: transfer.contract_coordinate(top8, coordinate)
        for coordinate in nonsupport
    }
    channels = {coordinate: channel for coordinate, channel in channels.items()
                if channel}
    require(len(channels) == 220, "top contraction channel count changed")

    scalar_pairings = {}
    channel_pairings = {}
    support_intersections = {}
    for name, colours in factors.items():
        scalars = {
            "lambda7": pairing(full7, colours),
            "lambda8": pairing(full8, colours),
            "lambda8_new_top_only": pairing(top8, colours),
        }
        values = {
            coordinate: pairing(channel, colours)
            for coordinate, channel in channels.items()
        }
        scalar_pairings[name] = {
            key: [value.numerator, value.denominator]
            for key, value in scalars.items()
        }
        full7_hits = [row for row in full7
                      if product_coefficient(row, colours)]
        full8_hits = [row for row in full8
                      if product_coefficient(row, colours)]
        top8_hits = [row for row in top8
                     if product_coefficient(row, colours)]
        channel_support = set().union(*(set(channel) for channel in channels.values()))
        channel_hits = [row for row in channel_support
                        if product_coefficient(row, colours)]
        support_intersections[name] = {
            "lambda7_rows": len(full7_hits),
            "lambda8_rows": len(full8_hits),
            "lambda8_top_rows": len(top8_hits),
            "union_of_channel_rows": len(channel_support),
            "channel_rows_hit": len(channel_hits),
            "lambda8_nonconstant_hit_rows": [
                row.hex() for row in full8_hits if row
            ],
        }
        channel_pairings[name] = {
            "nonzero": sum(value != 0 for value in values.values()),
            "zero": sum(value == 0 for value in values.values()),
            "value_histogram": [
                [[value.numerator, value.denominator], count]
                for value, count in sorted(Counter(values.values()).items())
            ],
            "nonzero_records": [
                [coordinate, *source.D5.COORDINATES[coordinate],
                 value.numerator, value.denominator]
                for coordinate, value in sorted(values.items()) if value
            ],
        }

    # The old exact degree-seven statement is recovered literally: only the
    # constant monomial of F or F^2 occurs on lambda7's support.
    for name, colours in factors.items():
        support_hits7 = [row for row in full7
                         if product_coefficient(row, colours)]
        require(support_hits7 == [b""],
                f"lambda7 acquired a nonconstant {name} support hit")
    require(scalar_pairings["F"]["lambda7"] == [1, 1]
            and scalar_pairings["F2"]["lambda7"] == [1, 1],
            "lambda7 constant pure pairing changed")

    if mutate:
        scalar_pairings["F"]["lambda7"] = [2, 1]
    require(scalar_pairings["F"]["lambda7"] == [1, 1],
            "hostile pure pairing mutation survived")

    result = {
        "format": "n8-chart26-pure-product-pairing-audit-v1",
        "status": "PASS exact pure-product grading/pairing control",
        "source_sha256": {
            str(path.relative_to(ROOT)): digest for path, digest in EXPECTED.items()
        },
        "normalized_pure_factors": {
            "three_colour_factors": 3,
            "terms_per_factor": 105,
            "factor_degree_histogram": dict(sorted(Counter(
                len(term) for term, _coefficient in pure_terms[0]
            ).items())),
            "F_total_homogeneous_degree": 12,
            "F2_total_homogeneous_degree": 24,
        },
        "dehomogenized_t_equals_1_pairings": scalar_pairings,
        "new_220_top_coordinate_contractions": channel_pairings,
        "pure_support_intersections": support_intersections,
        "homogeneous_degree_guard": {
            "lambda7_degree": 7,
            "lambda8_degree": 8,
            "new_channel_degree": 7,
            "Fh_degree": 12,
            "Fh_squared_degree": 24,
            "same_degree_pairings_defined": False,
            "inverse_system_contraction_by_Fh": (
                "zero for degree reasons on lambda7, lambda8, and every new "
                "degree-7 channel"
            ),
        },
        "verdict": (
            "The degree-7/8 critical controls do not yet carry a homogeneous "
            "pure-product class: F^h has degree 12.  Their t=1 scalar values "
            "are recorded exactly, but those values are truncations and cannot "
            "serve as a saturation separator or certificate."
        ),
        "smallest_target_relevant_lift": (
            "A conjecture-level inverse-system test needs a compatible dual in "
            "degree at least 12 pairing nontrivially with F^h (and degree at "
            "least 24 for (F^h)^2), with all lower contractions/source columns "
            "audited.  Multiplication by t through degrees 7 and 8 alone cannot "
            "supply this."
        ),
        "scope_guard": (
            "The all-support normalization is the exact Laurent quotient for "
            "the mixed ideal and pure-product nonvanishing.  This audit does "
            "not additionally impose the literal equations H_c=1."
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return json.loads(json.dumps(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.check_results:
        require(RESULT_PATH.exists()
                and json.loads(RESULT_PATH.read_text()) == result,
                "stored result changed")
    if args.write_results:
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("scalar", result["dehomogenized_t_equals_1_pairings"])
    print("channels", {
        key: value["nonzero"]
        for key, value in result["new_220_top_coordinate_contractions"].items()
    })
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
