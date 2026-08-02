#!/usr/bin/env python3
"""Lightweight frozen-ledger audit for the full chart-25 d=4 census."""

from hashlib import sha256
import json


EXPECTED_SHA256 = (
    "e87b47332355db290841b80afff95c32d6519efe4bc0f6ac08d10273a83c70e1"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def audit():
    ledger = {
        "actual_degree4_rows": 119946,
        "degree4_target_row_orbits": 15443,
        "degree4_seed_row_orbits": 290127,
        "row_orbits": [2264, 27440, 477743],
        "column_orbits": [3690, 55798, 913608],
        "degree4_layers": [
            [135724, 632519],
            [45754, 225805],
            [4922, 47720],
            [1216, 5836],
            [0, 1728],
        ],
    }
    require(ledger["degree4_seed_row_orbits"]
            + sum(layer[0] for layer in ledger["degree4_layers"])
            == ledger["row_orbits"][2], "degree-four row census mismatch")
    require(sum(layer[1] for layer in ledger["degree4_layers"])
            == ledger["column_orbits"][2], "degree-four column census mismatch")
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    require(digest == EXPECTED_SHA256, "degree-four census ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 degree-four census ledger: PASS")
    print("row orbits:", ledger["row_orbits"])
    print("column orbits:", ledger["column_orbits"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
