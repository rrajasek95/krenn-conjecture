#!/usr/bin/env python3
"""Verify the saved GF(2) degree-nine source-ideal membership certificate."""

from __future__ import annotations

import gzip
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main():
    with (HERE / "degree9_source_ideal_char2_h27.pkl").open("rb") as stream:
        matrix = pickle.load(stream)
    with gzip.open(
        HERE / "certificates" / "degree9_char2_h27_membership.pkl.gz", "rb"
    ) as stream:
        certificate = pickle.load(stream)

    columns = matrix["columns"]
    assert certificate["field"] == "GF(2)"
    assert certificate["group_order"] == 27
    assert certificate["shape"] == (len(matrix["row_codes"]), len(columns))
    selected = certificate["selected_columns"]
    assert len(selected) == 77_179
    assert len(set(selected)) == len(selected)
    assert all(0 <= column < len(columns) for column in selected)

    result = set()
    for column in selected:
        result.symmetric_difference_update(columns[column])
    target = {row for row, value in enumerate(matrix["rhs"]) if value}
    assert result == target
    print(
        "verified GF(2) degree-nine membership: "
        f"XOR of {len(selected)} H-orbit columns equals all {len(target)} target rows"
    )


if __name__ == "__main__":
    main()
