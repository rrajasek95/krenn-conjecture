#!/usr/bin/env python3
"""Exact rational 77-cycle charge-conservation ledger through K18."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
P = {
    "origin": ROOT / "computations/unaudited-codex-orbit0-k16-cycle-partition-referee-2026-08-23/results_balanced_cycle_partition_referee.json",
    "K16": ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/results_filtered_k16_run.json",
    "K17": ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/results_filtered_k17_run.json",
    "K18": ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/results_k18_charge.json",
}
OUT = HERE / "results_charge_ledger_through_k18.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def pair(value):
    return [value.numerator, value.denominator]


def main():
    data = {name: json.loads(path.read_text()) for name, path in P.items()}
    assert data["origin"]["original_structured_aT_guard"]["pairing"] == 0
    assert data["K16"]["K14_checkpoint"]["head_reduced_to_zero"] is True
    assert data["K16"]["K15_checkpoint"]["reduced"] == [0, 0, 0]
    q16 = Fraction(data["K16"]["K16_checkpoint"]
                   ["reduced_cycle_functional"]["integer_pairing"])
    q17 = Fraction(data["K17"]["cycle_replay"]["components"]
                   ["combined"]["cycle_pairing"])
    q18_record = data["K18"]["total"]["K18_irreducible_charge"]
    q18 = Fraction(q18_record["numerator"], q18_record["denominator"])
    assert q16 == Fraction(375_127_296)
    assert q17 == Fraction(-9_747_200_926_208, 6_545)
    assert q18 == Fraction(2_590_664_898_048, 935)
    cumulative = q16 + q17 + q18
    assert cumulative == Fraction(10_842_661_512_448, 6_545)
    required = -cumulative
    result = {
        "status": "PASS exact charge-conservation ledger through K18",
        "original_structured_aT_charge": [0, 1],
        "normal_charges": {
            "K14": [0, 1],
            "K15": [0, 1],
            "K16": pair(q16),
            "K17": pair(q17),
            "K18": pair(q18),
        },
        "cumulative_normal_charge_K14_through_K18": pair(cumulative),
        "required_total_normal_charge_K19_through_K24": pair(required),
        "zero_guards": {
            "K14": "all K14 heads are canceled; minimum response increment is 2",
            "K15": "the exact K15 checkpoint is wholly K0-pivotable and reduces to empty",
            "K0_through_K13": (
                "dependency theorem a*T in I_mix+K^14 gives no lower normal; "
                "this script does not replay that earlier reduction"
            ),
        },
        "conservation_scope": (
            "The 77-functional annihilates complete 105-term balanced source columns. "
            "Therefore a completed deterministic filtered reduction of the structured "
            "zero-charge target must have total normal charge zero. The displayed K19..K24 "
            "value is the exact aggregate required under the current pivot convention, "
            "not a degreewise prediction or proof that the completion exists."
        ),
        "pinned": {name: digest(path) for name, path in P.items()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
