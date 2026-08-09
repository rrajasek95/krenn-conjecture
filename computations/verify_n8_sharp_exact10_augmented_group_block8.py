#!/usr/bin/env python3
"""Exhaust the next nonempty exact-ten least-cell block after block 6."""

from collections import Counter

import verify_n8_sharp_exact10_augmented_group_block6 as audit


audit.BLOCK = 8
audit.EXPECTED_BLOCK_CELL = (0, 2, 0, 0)
audit.EXPECTED_BLOCK_COUNT = 6316
audit.EXPECTED_OUTCOMES = Counter({"odd": 4501, "one-class": 1815})
audit.EXPECTED_LEDGER_SHA256 = (
    "da126cf5bb01a265d18d9445c7e6a21c45fade305ac6dc22e274b83b2cbb6450"
)


if __name__ == "__main__":
    audit.main()
