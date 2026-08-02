#!/usr/bin/env python3
"""Lightweight withdrawal audit for the chart-25 d=4 modular Schur test."""

from hashlib import sha256
import json


EXPECTED_SHA256 = (
    "407120f38d5f7ecdb1fa45c5c1a4779b2fbc07989ac5da5dd05d9b8700428454"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def audit():
    ledger = {
        "primes": [1009, 1013, 1019],
        "leading_support_histogram": [
            [1, 241134], [2, 284312], [3, 31837], [4, 317493],
            [6, 28656], [9, 384], [12, 9792],
        ],
        "zero_fill_rank": 207143,
        "critical_core_rows": 270600,
        "two_support_columns": 257604,
        "balanced_core_components": 100085,
        "higher_projected_rank": 64221,
        "degree4_rank": 441879,
        "degree4_dual_dimension": 35864,
        "withdrawn_transfer_rank": 17224,
        "withdrawn_coupled_rank": 487007,
        "withdrawn_source_faithful_remainder": 3306,
        "withdrawal_reason": "quotient projection stopped at first free coordinate",
        "corrected_transfer_pending": True,
    }
    require(sum(count for _, count in ledger["leading_support_histogram"])
            == 913608, "leading column histogram mismatch")
    require(ledger["zero_fill_rank"] + ledger["critical_core_rows"]
            == 477743, "zero-fill/core row split mismatch")
    require(ledger["zero_fill_rank"]
            + ledger["critical_core_rows"]
            - ledger["balanced_core_components"]
            + ledger["higher_projected_rank"]
            == ledger["degree4_rank"], "degree-four rank decomposition mismatch")
    require(477743 - ledger["degree4_rank"]
            == ledger["degree4_dual_dimension"],
            "degree-four nullity mismatch")
    require(ledger["corrected_transfer_pending"],
            "withdrawn ledger was accidentally reinstated")
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    require(digest == EXPECTED_SHA256, "modular Schur ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 degree-four modular Schur withdrawal: PASS")
    print("primes:", ledger["primes"])
    print("surviving A4 rank:", ledger["degree4_rank"])
    print("withdrawn transfer/coupled ranks:",
          ledger["withdrawn_transfer_rank"],
          ledger["withdrawn_coupled_rank"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
