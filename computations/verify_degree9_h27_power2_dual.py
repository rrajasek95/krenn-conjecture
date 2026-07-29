#!/usr/bin/env python3
"""Independent verifier for a saved H27 integral dual modulo 2^k."""

from __future__ import annotations

import argparse
import gzip
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=HERE / "certificates" / "degree9_h27_integral_dual_mod4.pkl.gz",
    )
    args = parser.parse_args()

    with (HERE / "degree9_source_ideal_h27_integer.pkl").open("rb") as stream:
        matrix = pickle.load(stream)
    with (HERE / "degree9_source_ideal_char2_h27.pkl").open("rb") as stream:
        parity = pickle.load(stream)
    with gzip.open(args.certificate, "rb") as stream:
        certificate = pickle.load(stream)

    modulus = certificate["modulus"]
    assert modulus >= 4 and modulus & (modulus - 1) == 0
    assert certificate["version"] == 1
    assert certificate["group_order"] == 27
    assert certificate["shape"] == matrix["shape"]
    assert certificate["ring"] == f"Z/{modulus}Z"
    number_rows, number_columns = matrix["shape"]
    support = certificate["support"]
    saved_values = certificate["coefficients"]
    assert len(support) == len(saved_values)
    values = [0] * number_rows
    previous = -1
    for row, value in zip(support, saved_values):
        assert previous < row < number_rows
        assert 0 < value < modulus
        values[row] = value
        previous = row

    offsets = matrix["offsets"]
    rows = matrix["row_indices"]
    coefficients = matrix["coefficients"]
    for column in range(number_columns):
        total = matrix["column_sizes"][column] * sum(
            values[rows[position]] * coefficients[position]
            for position in range(offsets[column], offsets[column + 1])
        )
        assert total % modulus == 0, column

    pairing = sum(
        values[row] * matrix["row_sizes"][row]
        for row, is_target in enumerate(parity["rhs"])
        if is_target
    ) % modulus
    assert pairing == certificate["target_pairing"]
    assert pairing % 4 == 2
    print(
        f"verified integral H27 dual modulo {modulus}: "
        f"support={len(support)}, target pairing={pairing}",
        flush=True,
    )


if __name__ == "__main__":
    main()
