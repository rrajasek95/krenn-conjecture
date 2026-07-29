#!/usr/bin/env python3
"""Exclude the rank-(2,1,0) exact-three path boundary.

The path positions are ``B_00,B_01,B_10``.  Transposition puts any path
with a rank-two corner, one rank-one arm, and one zero arm into this ordered
rank pattern.  The incidence audit leaves only ``(Z1,S1,0)`` and
``(Z2,S2,0)``.  Every admissible status model has a projective-frame
singleton in an actual dead four-cross tensor.
"""

from __future__ import annotations

import hashlib

import verify_two_k4_exact_three_incidence_boundary as boundary3
import verify_two_k4_exact_three_matching_obstruction as frame


PATH = boundary3.POSITION_ORBITS["path"]


def main():
    survivors = tuple(
        row_matroids
        for row_matroids in boundary3.matroid_survivors("path")
        if tuple(item.rank for item in row_matroids) == (2, 1, 0)
    )
    assert tuple(
        tuple(item.name for item in row_matroids)
        for row_matroids in survivors
    ) == (("Z1", "S1", "0"), ("Z2", "S2", "0"))

    records = []
    model_counts = {}
    for row_matroids in survivors:
        names = tuple(item.name for item in row_matroids)
        models = frame.incidence_models(row_matroids, PATH)
        model_counts[names] = len(models)
        for masks in models:
            witness = frame.contraction_witness(row_matroids, masks, PATH)
            assert witness is not None, (names, masks)
            records.append((names, masks, witness))

    assert model_counts == {
        ("Z1", "S1", "0"): 480,
        ("Z2", "S2", "0"): 480,
    }
    assert len(records) == 960

    representatives = {
        ("Z1", "S1", "0"): (
            (0x8C, 0xF0, 0x60, 0x98),
            ((1, 1, 2, 0), (0, 1, 3), (1, 2, 0, 3)),
        ),
        ("Z2", "S2", "0"): (
            (0x2C, 0xF0, 0x64, 0x90),
            ((1, 0, 0, 1), (0, 1, 2), (2, 3, 1, 0)),
        ),
    }
    for names, (masks, witness) in representatives.items():
        assert (names, masks, witness) in records

    digest = hashlib.sha256(repr(sorted(records)).encode()).hexdigest()
    assert digest == (
        "420539678a6c51017cbc3d85cf2768fe08b31b3088f6cc7132b366d0d889ef5a"
    ), digest

    print(
        "PASS: exact-three path rank-(2,1,0) excluded "
        "(2 row types, 960 frame-singleton certificates)"
    )


if __name__ == "__main__":
    main()
