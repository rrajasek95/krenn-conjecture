#!/usr/bin/env python3
"""Exact rational 77-cycle charge-conservation ledger through K19."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
P = {
    "through_K18": (
        ROOT
        / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k18-2026-08-23"
        / "results_charge_ledger_through_k18.json"
    ),
    "K19": (
        ROOT
        / "computations/unaudited-codex-orbit0-k19-charge-2026-08-23"
        / "results_k19_charge.json"
    ),
}
OUT = HERE / "results_charge_ledger_through_k19.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def pair(value):
    return [value.numerator, value.denominator]


def main(write=True, mutate=False):
    prior = json.loads(P["through_K18"].read_text())
    k19 = json.loads(P["K19"].read_text())

    require(prior["status"] == "PASS exact charge-conservation ledger through K18",
            prior["status"])
    require(prior["original_structured_aT_charge"] == [0, 1],
            prior["original_structured_aT_charge"])
    require(k19["status"] == "PASS_EXACT_K19_CHARGE_ONLY_NO_K19_ROW_COLLECTION",
            k19["status"])
    require(k19["scope"] == (
        "Exact 77-cycle charge before and after the K19 pivotability filter. "
        "No K19 row collection, K20 tail, or ideal-membership claim."
    ), k19["scope"])

    normal = {
        degree: Fraction(*value)
        for degree, value in prior["normal_charges"].items()
    }
    q18_cumulative = Fraction(*prior["cumulative_normal_charge_K14_through_K18"])
    q19_record = k19["combined"]["K19_irreducible_charge"]
    q19 = Fraction(q19_record["numerator"], q19_record["denominator"])
    if mutate:
        q19 += 1
    require(q18_cumulative == Fraction(10_842_661_512_448, 6_545),
            q18_cumulative)
    require(q19 == Fraction(-14_857_399_077_330_176, 1_436_925), q19)
    normal["K19"] = q19

    cumulative = q18_cumulative + q19
    require(cumulative == Fraction(-137_246_362_298_070_016, 15_806_175),
            cumulative)
    required = -cumulative

    result = {
        "status": "PASS exact charge-conservation ledger through K19",
        "original_structured_aT_charge": [0, 1],
        "normal_charges": {degree: pair(value)
                           for degree, value in sorted(normal.items())},
        "cumulative_normal_charge_K14_through_K19": pair(cumulative),
        "required_total_normal_charge_K20_through_K24": pair(required),
        "convention_guard": {
            "target": "P=-R8prime*E0*E1*E2",
            "pivot_step": "a head coefficient c emits -c/m for every one of m selected pivots",
            "K19_entry": (
                "the exact K19-irreducible charge after the same all-dividing-pivot "
                "averaging convention; full prefilter K19 charge is not used"
            ),
            "policy_scope": (
                "the page split is conditional on completing this same deterministic "
                "policy; only the fully completed total charge is policy-independent"
            ),
        },
        "conservation_scope": (
            "The 77-functional annihilates each complete balanced 105-term source "
            "column and the structured target has charge zero. Therefore a completed "
            "reduction under the same deterministic convention must have total normal "
            "charge zero. The displayed K20..K24 value is only the exact aggregate "
            "compensation required after the frozen K14..K19 normals; it is not a "
            "degreewise prediction, a termination proof, or an ideal-membership claim."
        ),
        "pinned": {name: digest(path) for name, path in P.items()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    if write:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    import sys
    main(write="--no-write" not in sys.argv, mutate="--mutate" in sys.argv)
