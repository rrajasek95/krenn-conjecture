#!/usr/bin/env python3
"""Independently verify failure to lift the saved mod-4 dual to mod 8."""

from __future__ import annotations

import gzip
import hashlib
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATES = HERE / "certificates"


def main():
    matrix_path = HERE / "degree9_source_ideal_h27_integer.pkl"
    parity_path = HERE / "degree9_source_ideal_char2_h27.pkl"
    character_path = CERTIFICATES / "degree9_h27_integral_dual_mod4.pkl.gz"
    obstruction_path = CERTIFICATES / "degree9_h27_mod8_lift_obstruction.pkl.gz"
    with matrix_path.open("rb") as stream:
        matrix = pickle.load(stream)
    with parity_path.open("rb") as stream:
        parity = pickle.load(stream)
    with gzip.open(character_path, "rb") as stream:
        character = pickle.load(stream)
    with gzip.open(obstruction_path, "rb") as stream:
        obstruction = pickle.load(stream)

    assert obstruction["version"] == 1
    assert obstruction["field"] == "GF(2)"
    assert obstruction["group_order"] == 27
    assert obstruction["shape"] == matrix["shape"] == character["shape"]
    assert obstruction["base_modulus"] == character["modulus"] == 4
    assert obstruction["base_character_sha256"] == hashlib.sha256(
        character_path.read_bytes()
    ).hexdigest()

    number_rows, number_columns = matrix["shape"]
    lam = [0] * number_rows
    previous = -1
    for row, value in zip(character["support"], character["coefficients"]):
        assert previous < row < number_rows
        assert 0 < value < 4
        lam[row] = value
        previous = row

    offsets = matrix["offsets"]
    rows = matrix["row_indices"]
    coefficients = matrix["coefficients"]
    lift_rhs = bytearray(number_columns)
    for column in range(number_columns):
        total = matrix["column_sizes"][column] * sum(
            lam[rows[position]] * coefficients[position]
            for position in range(offsets[column], offsets[column + 1])
        )
        assert total % 4 == 0
        lift_rhs[column] = (total // 4) & 1

    dependency = obstruction["equation_support"]
    previous = -1
    row_parity = bytearray(number_rows)
    pairing = 0
    for column in dependency:
        assert previous < column < number_columns
        previous = column
        pairing ^= lift_rhs[column]
        for row in parity["columns"][column]:
            row_parity[row] ^= 1
    assert not any(row_parity)  # dependency lies in ker(A mod 2)
    assert pairing == 1        # but it detects the proposed lift RHS
    print(
        f"verified mod-8 lift obstruction: dependency support={len(dependency)}, "
        f"pairing=1",
        flush=True,
    )


if __name__ == "__main__":
    main()
