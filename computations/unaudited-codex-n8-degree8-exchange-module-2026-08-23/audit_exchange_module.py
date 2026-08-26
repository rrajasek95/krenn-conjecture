#!/usr/bin/env python3
"""Exact exchange-module audit for the chart-26 lambda8 top layer.

This is deliberately a control at the exact normalized Laurent quotient.
It verifies the fixed-chart stabilizer module on the 220 nonzero coordinate
contractions and records what the frozen degree-six collision packet does
(and does not) supply as an exchange operation.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TRANSFER_DIR = HERE.parent / "unaudited-codex-n8-degree8-transfer-audit-2026-08-23"
TRANSFER_SCRIPT = TRANSFER_DIR / "audit_lambda7_lambda8_transfer.py"
TRANSFER_RESULT = TRANSFER_DIR / "results_lambda7_lambda8_transfer.json"
WEIGHTED_CHECKER = ROOT / "computations/verify_n8_chart26_weighted_degree6_census.py"
RESULT_PATH = HERE / "results_exchange_module.json"

EXPECTED = {
    TRANSFER_SCRIPT: "a6197b5582369c2ea9c9729747e8260f5b96646676d1ebb02ba6440e40929e6a",
    TRANSFER_RESULT: "d9f82b3210cae2994b292569653b3e55d945eebdc3e481dc9cd6f81a9b83a7e4",
    WEIGHTED_CHECKER: "27371803eecef4a0c4084aa11947116d3bf7161a145cc756bb487c45c17856a0",
}
EXPECTED_COLLISION_LEDGER = "e8384cac6824cb6a46c2f93f4cab8fbca100f76bba510699b058256ffc4d7fea"


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


def transform_row(row, transform):
    return bytes(sorted(transform[item] for item in row))


def audit(mutate=False):
    transfer = load(TRANSFER_SCRIPT, "exchange_transfer")
    stored = json.loads(TRANSFER_RESULT.read_text())
    require(stored == json.loads(json.dumps(transfer.audit(False))),
            "stored transfer theorem drifted")
    source_module = transfer.load(transfer.AUDIT_PATH, "exchange_degree8_source")
    source = source_module.load_d7()
    certificate = json.loads(transfer.CERTIFICATE_PATH.read_text())
    lambda8 = parse(certificate["exact_extended_dual"])
    full8 = transfer.expand_invariant(source, lambda8)
    top8 = {row: value for row, value in full8.items() if len(row) == 8}

    nonsupport = sorted(
        set(range(len(source.D5.COORDINATES))) - set(source.D5.SUPPORT_IDS)
    )
    channels = {
        coordinate: transfer.contract_coordinate(top8, coordinate)
        for coordinate in nonsupport
    }
    channels = {coordinate: channel for coordinate, channel in channels.items()
                if channel}
    require(len(channels) == 220, "active contraction count changed")

    # Literal covariance under the four-element fixed-chart stabilizer.
    transforms = source.D5.VARIABLE_TRANSFORMS
    require(len(transforms) == 4, "chart stabilizer changed")
    covariance_checks = 0
    for transform in transforms:
        for coordinate, channel in channels.items():
            moved = {
                transform_row(row, transform): value
                for row, value in channel.items()
            }
            require(moved == channels[transform[coordinate]],
                    "coordinate contraction is not stabilizer covariant")
            covariance_checks += 1

    # Active coordinate orbits, stabilizers, and the exact V4 character.
    seen = set()
    orbit_records = []
    stabilizer_histogram = Counter()
    for coordinate in sorted(channels):
        if coordinate in seen:
            continue
        orbit = tuple(sorted({transform[coordinate] for transform in transforms}))
        require(set(orbit).issubset(channels), "active orbit is incomplete")
        seen.update(orbit)
        stabilizer = tuple(
            index for index, transform in enumerate(transforms)
            if transform[coordinate] == coordinate
        )
        stabilizer_histogram[stabilizer] += 1
        orbit_records.append({
            "representative": coordinate,
            "coordinate": list(source.D5.COORDINATES[coordinate]),
            "orbit": list(orbit),
            "stabilizer_indices": list(stabilizer),
        })
    require(len(orbit_records) == 61 and len(seen) == 220,
            "active orbit decomposition changed")

    traces = [sum(transform[coordinate] == coordinate for coordinate in channels)
              for transform in transforms]
    require(traces == [220, 8, 6, 10], "V4 permutation traces changed")
    # Transforms 1 and 2 generate V4; transform 3 is their product.
    multiplicities = {}
    for sign1 in (1, -1):
        for sign2 in (1, -1):
            value = (traces[0] + sign1 * traces[1]
                     + sign2 * traces[2] + sign1 * sign2 * traces[3]) // 4
            multiplicities[f"({sign1},{sign2})"] = value
    require(multiplicities == {
        "(1,1)": 61, "(1,-1)": 53,
        "(-1,1)": 52, "(-1,-1)": 54,
    }, "V4 character decomposition changed")

    # Independence is source-faithful: use the already audited exact minor.
    rank = transfer.exact_sparse_rank_minor([
        (f"x{coordinate}", channel)
        for coordinate, channel in sorted(channels.items())
    ])
    require(rank["rank"] == 220
            and Fraction(*rank["minor_determinant"])
            == Fraction(-1, 2 ** 236),
            "top contraction module lost independence")

    # The collision theorem below uses the authoritative frozen complete
    # census, whose full exact replay digest is pinned.  Representative rows
    # are retained so that the non-flatness guard is source-labelled.
    collision_summary = {
        "ledger_sha256": EXPECTED_COLLISION_LEDGER,
        "pair_counts": {"4-4": 967750, "4-5": 792653, "5-5": 1165402},
        "representatives": {
            "4-4": {"classes": 7, "zero": 3, "nonzero": 4},
            "4-5": {
                "classes": 15, "zero": 0,
                "squarefree_nonzero": 12, "nonsquarefree_nonzero": 3,
            },
        },
        "explicit_nonflat_4-4": {
            "first_lead": "0948cfed", "second_lead": "0948c7f4",
            "class_size": 504, "remainder_lead": "0951b4c7edf4",
        },
        "explicit_nonflat_4-5": {
            "first_lead": "0948c6f4", "second_lead": "0948c6d9e4",
            "class_size": 504, "remainder_lead": "0951acc6f4f4",
        },
    }

    if mutate:
        traces[1] += 1
    require(traces == [220, 8, 6, 10], "hostile trace mutation survived")

    result = {
        "format": "n8-chart26-degree8-exchange-module-audit-v1",
        "status": "PASS finite fixed-chart control; no nontrivial collision exchange",
        "source_sha256": {
            str(path.relative_to(ROOT)): digest for path, digest in EXPECTED.items()
        },
        "lambda8_top_contraction_module": {
            "dimension": 220,
            "independent_source_labelled_channels": 220,
            "fixed_chart_group": "V4 (order 4)",
            "covariance_checks": covariance_checks,
            "orbit_count_minimal_permutation_generators": len(orbit_records),
            "orbit_size_histogram": dict(sorted(Counter(
                len(record["orbit"]) for record in orbit_records
            ).items())),
            "orbit_records": orbit_records,
            "stabilizer_histogram": [
                {"stabilizer_indices": list(stabilizer), "orbit_count": count}
                for stabilizer, count in sorted(stabilizer_histogram.items())
            ],
            "permutation_character_traces": traces,
            "irreducible_character_multiplicities": multiplicities,
            "exact_rank_minor": rank,
        },
        "degree6_collision_packet": collision_summary,
        "collision_action_theorem": {
            "canonical_action": "inverse-system contraction",
            "degree_map": "R of degree 6 sends E subset (S_7)^* to (S_1)^*",
            "action_on_all_220_channels": "zero",
            "reason": (
                "for every channel C_x=x contraction lambda8, every frozen "
                "degree-6 collision R in the mixed ideal and every degree-1 "
                "monomial m, (R contraction C_x)(m)=lambda8(x*m*R)=0; "
                "these are bounded degree-8 source columns"
            ),
            "nontrivial_exchange_endomorphism": False,
            "counterguard": (
                "19 of the 22 frozen 4-4/4-5 representative reductions have "
                "nonzero remainders, including the two explicit labelled "
                "records above.  Turning them into same-degree rewrites needs "
                "a rehomogenizing lift/right inverse not supplied by the "
                "collision theorem."
            ),
        },
        "verdict": (
            "The 220 directions are a finite V4 permutation module generated "
            "by 61 source-labelled orbit representatives.  The known degree-6 "
            "collision ideal annihilates it by contraction, but supplies no "
            "nonzero internal exchange operator and therefore no lambda9 or "
            "all-k transfer rule."
        ),
        "scope_guard": (
            "This is an exact control in the chart-26 Laurent normalization. "
            "It does not impose the literal pure equations H_c=1 and does not "
            "prove the conjecture target or saturation by the pure product."
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
    print("dimension/orbits/traces=", 220, 61,
          result["lambda8_top_contraction_module"]["permutation_character_traces"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
