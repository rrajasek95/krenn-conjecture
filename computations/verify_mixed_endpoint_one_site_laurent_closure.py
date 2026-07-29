#!/usr/bin/env python3
"""Replay the exact Laurent-closure obstruction through 32 active cells."""

from __future__ import annotations

from search_mixed_endpoint_one_site_support import (
    ROW_GEOMETRIES,
    SupportSystem,
    run_laurent_cegar,
)


EXPECTED = {
    "path-edge": {
        "status": "obstructed-through-bound",
        "rounds": 32,
        "cost": 33,
        "active": (),
        "ledger": "6b19a3776861df1d6a7b4a2280ecd624df2b79d431c2c22bf0722847722f8969",
    },
    "matching": {
        "status": "obstructed-through-bound",
        "rounds": 30,
        "cost": 34,
        "active": (),
        "ledger": "fbde1edf4126a9172fa3bb03634b41fee5fd55c456d12445e33b4449b70a8d16",
    },
}


def main():
    for name, rows in ROW_GEOMETRIES.items():
        system = SupportSystem(rows)
        result = run_laurent_cegar(
            name, system, bound=32, max_rounds=100, verbose=False
        )
        assert result == EXPECTED[name]
        print(name, result)
    print("no mixed-endpoint one-site Laurent-compatible support through 32: PASS")


if __name__ == "__main__":
    main()
