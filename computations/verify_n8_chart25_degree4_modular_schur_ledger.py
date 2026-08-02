#!/usr/bin/env python3
"""Lightweight ledger audit for the chart-25 d=4 modular Schur test."""

from hashlib import sha256
import json


EXPECTED_SHA256 = (
    "c8d8086cb97e5298300ac15b3e8fed6b0994a5d3b3bcdaf15b253ad5613a86af"
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
        "higher_projected_columns": 164499,
        "higher_projected_zero": 49071,
        "higher_projected_rank": 64221,
        "degree4_rank": 441879,
        "degree4_dual_dimension": 35864,
        "degree4_target_remainder": 3434,
        "lower_rank": 27904,
        "lower_kernel_dimension": 31584,
        "transfer_rank": 17224,
        "coupled_rank": 487007,
        "coupled_dual_dimension": 20440,
        "source_faithful_target_consistent": False,
        "source_faithful_remainder": 3306,
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
    require(59488 - ledger["lower_rank"]
            == ledger["lower_kernel_dimension"],
            "lower kernel dimension mismatch")
    require(ledger["lower_rank"] + ledger["degree4_rank"]
            + ledger["transfer_rank"] == ledger["coupled_rank"],
            "coupled rank decomposition mismatch")
    require(2264 + 27440 + 477743 - ledger["coupled_rank"]
            == ledger["coupled_dual_dimension"],
            "coupled nullity mismatch")
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    require(digest == EXPECTED_SHA256, "modular Schur ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 degree-four modular Schur ledger: PASS")
    print("primes:", ledger["primes"])
    print("A4 / transfer / coupled ranks:", ledger["degree4_rank"],
          ledger["transfer_rank"], ledger["coupled_rank"])
    print("source-faithful remainder:",
          ledger["source_faithful_remainder"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
