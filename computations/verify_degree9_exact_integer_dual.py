#!/usr/bin/env python3
"""Independently verify the exact integral degree-nine dual certificate."""

from __future__ import annotations

import gzip
import hashlib
import math
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent


def valuation_two(value: int) -> int:
    value = abs(value)
    assert value
    return (value & -value).bit_length() - 1


def main() -> None:
    certificate_path = (
        HERE / "certificates" / "degree9_exact_integer_dual.pkl.gz"
    )
    with gzip.open(certificate_path, "rb") as stream:
        certificate = pickle.load(stream)
    with (HERE / "degree9_source_ideal_orbits.pkl").open("rb") as stream:
        matrix = pickle.load(stream)

    assert certificate["version"] == 1
    assert certificate["ring"] == "Z"
    assert certificate["shape"] == matrix["shape"] == (3102, 1314)
    support = certificate["support"]
    coefficients = certificate["coefficients"]
    assert len(support) == len(coefficients)
    assert tuple(sorted(set(support))) == tuple(support)
    dual = dict(zip(support, coefficients))
    assert all(value for value in coefficients)
    assert math.gcd(*(abs(value) for value in coefficients)) == 1

    column_pairings = [0] * matrix["shape"][1]
    for row, column, value in matrix["entries"]:
        column_pairings[column] += dual.get(row, 0) * value
    assert all(value == 0 for value in column_pairings)

    target_pairing = sum(
        dual.get(row, 0) * int(value)
        for row, value in enumerate(matrix["b"])
    )
    assert target_pairing == certificate["target_pairing"]
    assert valuation_two(target_pairing) == certificate["target_pairing_v2"] == 12

    digest = hashlib.sha256(certificate_path.read_bytes()).hexdigest()
    print(
        "verified exact integral degree-nine dual: "
        f"support={len(support)}, target pairing v2=12, sha256={digest}",
        flush=True,
    )


if __name__ == "__main__":
    main()
