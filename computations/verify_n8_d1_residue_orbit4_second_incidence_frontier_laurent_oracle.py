#!/usr/bin/env python3
"""Signed-Laurent/one-class oracle for the second 159-cell O4 frontier."""

from __future__ import annotations

import hashlib
import importlib
import os
import sys
from collections import Counter
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED = {
    "verify_n8_d1_residue_orbit4_incidence_frontier_odd_circuit.py":
        "95f75391b40d9e006b4580cf2fa5e34e4930ec87facb7bef5391b419af2c3507",
    "verify_n8_d1_dense_212_laurent_obstruction.py":
        "3c0153cc6e396e6c848b122fa8ac431763dc610e7058c3c156ef32d3c74ceea0",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned signed-Laurent source changed: " + filename)

Q = importlib.import_module(
    "verify_n8_d1_residue_orbit4_incidence_frontier_odd_circuit"
)
L = importlib.import_module("verify_n8_d1_dense_212_laurent_obstruction")
C, D = Q.C, Q.D

EXPECTED_GENERATOR_SHA256 = (
    "44468c0d48b0afb2d23f383864ca76c85d4689d173fcb7ad95714268458d339d"
)
EXPECTED_LEDGER_SHA256 = (
    "343fb371b70a29eecf2af120b05295a8737ae6e03d3690aa3de0039d15f8e7d2"
)

FRONTIER_MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0), (0, 3, 0, 1),
    (0, 4, 0, 1), (0, 4, 1, 0), (0, 5, 0, 1), (0, 5, 1, 0),
    (0, 6, 0, 1), (0, 6, 1, 0),
    (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 1, 0), (0, 7, 1, 1),
    (1, 2, 0, 1), (1, 2, 1, 0), (1, 3, 1, 0),
    (1, 6, 0, 0), (1, 6, 0, 1), (1, 6, 1, 0), (1, 6, 1, 1),
    (1, 7, 0, 1), (1, 7, 1, 0),
    (2, 7, 0, 0), (2, 7, 0, 1), (2, 7, 1, 0), (2, 7, 1, 1),
    (2, 7, 2, 0), (2, 7, 2, 1),
    (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0), (3, 6, 1, 1),
    (3, 6, 2, 0), (3, 6, 2, 1),
)


def gf2_signed_system(rows, names):
    """Solve d_i dot phase = 1 and return an exact odd-dependency witness."""
    basis = {}
    conflict = None
    for position, row in enumerate(rows):
        bits = 0
        for name, exponent in row["difference"].items():
            require(exponent.denominator == 1,
                    "a Laurent difference stopped being integral")
            if exponent.numerator % 2:
                bits ^= 1 << names[name]
        rhs = 1
        provenance = 1 << position
        while bits:
            pivot = bits.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (bits, rhs, provenance)
                break
            basis_bits, basis_rhs, basis_provenance = basis[pivot]
            bits ^= basis_bits
            rhs ^= basis_rhs
            provenance ^= basis_provenance
        else:
            if rhs:
                conflict = provenance
                break

    if conflict is not None:
        positions = tuple(index for index in range(len(rows))
                          if (conflict >> index) & 1)
        combined = Counter()
        for position in positions:
            combined.update({name: int(exponent)
                             for name, exponent
                             in rows[position]["difference"].items()})
        require(all(exponent % 2 == 0 for exponent in combined.values())
                and len(positions) % 2 == 1,
                "the GF(2) odd-dependency witness failed reconstruction")
        return {
            "consistent": False,
            "rank": len(basis),
            "odd_dependency_positions": list(positions),
            "odd_dependency_record_indices": [
                rows[position]["record_index"] for position in positions
            ],
        }

    solution = 0
    for pivot in sorted(basis):
        bits, rhs, _provenance = basis[pivot]
        lower = bits & ~(1 << pivot)
        parity = (lower & solution).bit_count() & 1
        if parity ^ rhs:
            solution |= 1 << pivot
    for row in rows:
        bits = 0
        for name, exponent in row["difference"].items():
            if exponent.numerator % 2:
                bits ^= 1 << names[name]
        require((bits & solution).bit_count() % 2 == 1,
                "the reconstructed plus-binomial sign solution failed")
    return {
        "consistent": True,
        "rank": len(basis),
        "phase_one_variables": sorted(
            name for name, index in names.items() if (solution >> index) & 1
        ),
    }


def oracle(support):
    records = C.coefficient_generators(support)
    plus = L.plus_binomials(records)
    basis, dependencies = L.integer_laurent_basis(plus)
    odd_dependencies = [dependency for dependency in dependencies
                        if sum(dependency.values()) % 2]
    names = {"x_%d%d_%d%d" % cell: index
             for index, cell in enumerate(sorted(Q.allowed_support()))}
    signed = gf2_signed_system(plus, names)
    require(signed["consistent"] == (not odd_dependencies),
            "QQ dependency parity and the GF(2) signed system disagree")
    reduced_histogram = Counter()
    one_class = []
    for index, record in enumerate(records):
        reduced, _traces = L.reduce_record(record, basis)
        reduced_histogram[len(reduced)] += 1
        if len(reduced) == 1:
            one_class.append(index)
    return records, plus, basis, dependencies, signed, {
        str(classes): count
        for classes, count in sorted(reduced_histogram.items())
    }, one_class


def audit():
    started = monotonic()
    allowed = Q.allowed_support()
    old_support = allowed - set(Q.FRONTIER_MISSING)
    new_support = allowed - set(FRONTIER_MISSING)
    require(len(old_support) == len(new_support) == 159,
            "the two incidence-frontier sizes changed")
    require(set(Q.FRONTIER_MISSING) - set(FRONTIER_MISSING)
            == {(0, 2, 1, 0)}
            and set(FRONTIER_MISSING) - set(Q.FRONTIER_MISSING)
            == {(1, 2, 1, 0)},
            "the one-cell exchange between incidence frontiers changed")

    new = oracle(new_support)
    records, plus, basis, dependencies, signed, histogram, one_class = new
    require(len(records) == 4321
            and D.content_hash(records) == EXPECTED_GENERATOR_SHA256,
            "the second frontier coefficient input changed")
    require(len(plus) == 306 and len(basis) == 20
            and len(dependencies) == 286,
            "the second frontier plus-binomial lattice census changed")
    require(signed["consistent"] and signed["rank"] == 20,
            "the second frontier gained an odd signed dependency")
    require(not one_class,
            "a coefficient generator gained a one-class Laurent reduction")

    old_records = C.coefficient_generators(old_support)
    old_plus = L.plus_binomials(old_records)
    names = {"x_%d%d_%d%d" % cell: index
             for index, cell in enumerate(sorted(allowed))}
    old_signed = gf2_signed_system(old_plus, names)
    require(len(old_plus) == 315 and not old_signed["consistent"]
            and old_signed["rank"] == 21,
            "the killed frontier signed-lattice control changed")
    require(set(old_signed["odd_dependency_record_indices"])
            == {2471, 3648, 3738},
            "the control did not recover the checked three-circuit")

    ledger = {
        "pinned_sources": PINNED,
        "allowed_cells": len(allowed),
        "localized_cells": len(new_support),
        "missing_cells": [list(cell) for cell in FRONTIER_MISSING],
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "maximal_plus_binomials": len(plus),
        "laurent_rank_over_Q": len(basis),
        "dependency_generators": len(dependencies),
        "odd_dependency_generators": 0,
        "signed_gf2": signed,
        "reduced_class_histogram": histogram,
        "one_class_generators": one_class,
        "killed_frontier_control": {
            "plus_binomials": len(old_plus),
            "signed_gf2": old_signed,
        },
        "one_cell_exchange": {
            "restored": [0, 2, 1, 0],
            "removed": [1, 2, 1, 0],
        },
        "status": (
            "coefficient-open: the maximal plus-binomial signed character "
            "is consistent and no generator reduces to one Laurent class"
        ),
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the second-frontier Laurent ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("plus/rank/dependencies: %d/%d/%d" % (
        ledger["maximal_plus_binomials"], ledger["laurent_rank_over_Q"],
        ledger["dependency_generators"],
    ))
    print("odd dependencies / one-class generators: 0 / 0")
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
