#!/usr/bin/env python3
"""Reconstruct and certify an exact integral degree-nine left-kernel vector.

The small characteristic-zero ``S_6 x S_3`` orbit matrix has an invariant
left-kernel functional separating the target.  Modular copies of the same
echelon functional can be combined by CRT and rational reconstruction.  This
script clears denominators, divides the coefficient gcd, audits the result
over the integers, and writes a compact certificate.

The reconstruction inputs are the files written by
``test_degree9_source_ideal.py --save-dual`` at distinct odd primes.  Enough
primes must be supplied for the final exact audit to pass.
"""

from __future__ import annotations

import argparse
import gzip
import math
import pickle
from pathlib import Path

from sympy.ntheory.modular import crt
from sympy.polys.domains import ZZ
from sympy.polys.modulargcd import _integer_rational_reconstruction


HERE = Path(__file__).resolve().parent


def valuation_two(value: int) -> int:
    value = abs(value)
    assert value
    return (value & -value).bit_length() - 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("duals", nargs="+", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE / "certificates" / "degree9_exact_integer_dual.pkl.gz",
    )
    args = parser.parse_args()

    modular = []
    seen_primes = set()
    for path in args.duals:
        with path.open("rb") as stream:
            payload = pickle.load(stream)
        prime = int(payload["prime"])
        if prime in seen_primes:
            continue
        seen_primes.add(prime)
        modular.append(payload)
    assert modular
    assert len({item["free_row"] for item in modular}) == 1

    primes = [int(item["prime"]) for item in modular]
    rows = sorted(set().union(*(item["y"] for item in modular)))
    rational = {}
    modulus = None
    for row in rows:
        residue, modulus = crt(
            primes, [int(item["y"].get(row, 0)) for item in modular], check=True
        )
        value = _integer_rational_reconstruction(int(residue), int(modulus), ZZ)
        if value is None:
            raise RuntimeError(
                f"rational reconstruction failed at row {row}; add more primes"
            )
        rational[row] = value
    assert modulus is not None

    with (HERE / "degree9_source_ideal_orbits.pkl").open("rb") as stream:
        matrix = pickle.load(stream)
    number_rows, number_columns = matrix["shape"]
    columns = [dict() for _ in range(number_columns)]
    for row, column, coefficient in matrix["entries"]:
        columns[column][row] = coefficient

    bad = []
    for column, entries in enumerate(columns):
        value = sum(
            rational.get(row, 0) * coefficient
            for row, coefficient in entries.items()
        )
        if value:
            bad.append((column, value))
    if bad:
        raise RuntimeError(
            f"reconstructed vector fails exact audit in {len(bad)} columns; "
            "add more primes"
        )

    denominator = math.lcm(
        *(int(value.denominator) for value in rational.values())
    )
    integral = {
        row: int(value.numerator) * (denominator // int(value.denominator))
        for row, value in rational.items()
    }
    coefficient_gcd = math.gcd(*(abs(value) for value in integral.values()))
    integral = {row: value // coefficient_gcd for row, value in integral.items()}
    assert math.gcd(*(abs(value) for value in integral.values())) == 1

    for entries in columns:
        assert (
            sum(integral.get(row, 0) * value for row, value in entries.items())
            == 0
        )
    pairing = sum(
        integral.get(row, 0) * int(value)
        for row, value in enumerate(matrix["b"])
    )
    assert pairing

    support = tuple(sorted(row for row, value in integral.items() if value))
    payload = {
        "version": 1,
        "ring": "Z",
        "symmetry_group": "S6 x S3",
        "symmetry_group_order": 4320,
        "basis": "normalized orbit averages",
        "shape": (number_rows, number_columns),
        "support": support,
        "coefficients": tuple(integral[row] for row in support),
        "target_pairing": pairing,
        "target_pairing_v2": valuation_two(pairing),
        "crt_modulus_bits": int(modulus).bit_length(),
        "number_modular_images": len(modular),
    }
    args.output.parent.mkdir(exist_ok=True)
    with gzip.open(args.output, "wb") as stream:
        pickle.dump(payload, stream, protocol=pickle.HIGHEST_PROTOCOL)
    print(
        f"wrote {args.output}: support={len(support)}, "
        f"max coefficient bits={max(abs(value).bit_length() for value in integral.values())}, "
        f"pairing={pairing}, v2={valuation_two(pairing)}, "
        f"CRT bits={int(modulus).bit_length()}",
        flush=True,
    )


if __name__ == "__main__":
    main()
