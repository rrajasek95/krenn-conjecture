#!/usr/bin/env python3
"""Extend the corrected filtered 77-cycle charge ledger through complete K21."""

from fractions import Fraction
from pathlib import Path
import hashlib
import json
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
K20_LEDGER = ROOT / (
    "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k20-"
    "2026-08-24/results_charge_ledger_through_k20.json"
)
K21_RESULT = ROOT / (
    "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/"
    "results_k21_complete_52_exact.json"
)
K21_MANIFEST = ROOT / (
    "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/"
    "k21_manifest_complete_52.json"
)
EXPECTED_FILE_SHA256 = {
    K20_LEDGER: "696f9205f9411cc58b1b17f014c97fdc6d9ce5fbb936c36cf42870ffb3db5c25",
    K21_RESULT: "4df5a6316a8bfac70efb793d27f7e72ea269b491d8a565ecedb17d7997f81340",
    K21_MANIFEST: "9085dec995d7bbbc26f4f875b43cc54c8f5ad9e9d34af413e6dd3a4a4889fe96",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256_bytes(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical_sha256(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def rational(value):
    if isinstance(value, str):
        return Fraction(value)
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def render(value):
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


def validate_and_build(k20, k21, manifest):
    require(
        k20.get("status") == "PASS_CORRECTED_COMPLETE_CHARGE_LEDGER_THROUGH_K20",
        "K20 ledger is not authoritative complete",
    )
    require(
        k21.get("status") == "PASS_COMPLETE_K21_52_ID_EXACT_Q",
        "K21 result is not authoritative complete",
    )
    require(k21.get("complete_claim") is True, "K21 complete flag is false")
    require(k21.get("required_paths") == 52, "K21 required-path count mismatch")
    require(k21.get("covered_paths") == 52, "K21 covered-path count mismatch")
    require(not k21.get("missing_paths"), "K21 has missing paths")
    require(not k21.get("duplicate_paths"), "K21 has duplicate paths")
    require(not k21.get("extra_paths"), "K21 has extra paths")
    require(
        k21.get("manifest_logical_sha256") == logical_sha256(manifest),
        "K21 manifest logical digest mismatch",
    )
    k21_full = rational(k21["full"])
    k21_irreducible = rational(k21["irreducible"])
    require(k21_full == k21_irreducible, "K21 full/irreducible mismatch")
    require(
        k21_irreducible == Fraction(-15276224591027275648, 521603775),
        "unexpected K21 exact charge",
    )
    through_k20 = rational(k20["cumulative_K14_through_K20"])
    require(
        through_k20 == Fraction(7534667963437738624, 521603775),
        "unexpected cumulative K20 charge",
    )
    cumulative = through_k20 + k21_irreducible
    require(
        cumulative == Fraction(-2580518875863179008, 173867925),
        "unexpected cumulative K21 charge",
    )
    charges = dict(k20["charges"])
    charges["K21"] = render(k21_irreducible)
    return {
        "status": "PASS_CORRECTED_COMPLETE_CHARGE_LEDGER_THROUGH_K21",
        "charges": charges,
        "coverage": {"K18": 17, "K19": 24, "K20": 36, "K21": 52},
        "cumulative_K14_through_K21": render(cumulative),
        "required_aggregate_K22_through_K24_compensation": render(-cumulative),
        "sources": {
            "through_K20": {
                "path": str(K20_LEDGER.relative_to(ROOT)),
                "sha256": EXPECTED_FILE_SHA256[K20_LEDGER],
            },
            "K21_manifest": {
                "path": str(K21_MANIFEST.relative_to(ROOT)),
                "sha256": EXPECTED_FILE_SHA256[K21_MANIFEST],
                "logical_sha256": logical_sha256(manifest),
            },
            "K21_result": {
                "path": str(K21_RESULT.relative_to(ROOT)),
                "sha256": EXPECTED_FILE_SHA256[K21_RESULT],
            },
        },
        "scope": (
            "Exact 77-cycle conservation ledger under the frozen filtered "
            "convention; aggregate only, not a degreewise prediction, residual "
            "checkpoint, ideal-membership result, or conjecture verdict."
        ),
    }


def load_pinned_inputs():
    for path, expected in EXPECTED_FILE_SHA256.items():
        require(sha256_bytes(path) == expected, f"file digest mismatch: {path}")
    return (
        json.loads(K20_LEDGER.read_text()),
        json.loads(K21_RESULT.read_text()),
        json.loads(K21_MANIFEST.read_text()),
    )


def self_test():
    k20, k21, manifest = load_pinned_inputs()
    result = validate_and_build(k20, k21, manifest)
    require(result["coverage"]["K21"] == 52, "good coverage rejected")
    hostile = json.loads(json.dumps(k21))
    hostile["covered_paths"] = 51
    try:
        validate_and_build(k20, hostile, manifest)
    except ValueError as error:
        require("covered-path" in str(error), "wrong incomplete-result rejection")
    else:
        raise AssertionError("incomplete K21 mutation accepted")
    hostile = json.loads(json.dumps(manifest))
    hostile["groups"] = hostile["groups"][:-1]
    try:
        validate_and_build(k20, k21, hostile)
    except ValueError as error:
        require("manifest logical digest" in str(error), "wrong manifest rejection")
    else:
        raise AssertionError("manifest deletion accepted")
    print(
        json.dumps(
            {
                "status": "PASS_CHARGE_LEDGER_THROUGH_K21_SELFTEST",
                "pinned_hashes": True,
                "incomplete_K21_rejected": True,
                "manifest_deletion_rejected": True,
            },
            sort_keys=True,
        )
    )


def main():
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return
    require(not sys.argv[1:], "usage: assemble_charge_ledger_through_k21.py [--self-test]")
    result = validate_and_build(*load_pinned_inputs())
    output = HERE / "results_charge_ledger_through_k21.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
