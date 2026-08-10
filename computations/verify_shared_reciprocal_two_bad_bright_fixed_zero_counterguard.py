#!/usr/bin/env python3
"""Freeze the first exact fixed-zero evasion of the private-row charts.

The pinned seven-cell rational common quadratic has X_a,X_c in im(Phi),
dim pi_t ker(Phi)=2, and X_t outside im(Phi).  This checker strengthens its
scope: the full affine fibres Phi^-1(X_a) and Phi^-1(X_c) both evaluate to
zero at site 2.  Therefore no choice of bright representatives enters the
zero-free whole-kernel flag branches.

The same q has no all-target four-site cofactor.  Its controller response
R=sum P_z,t K_z(t,t,t,t) is identically zero, whereas the pinned full-row
common-radical theorem forces D_tt*R=1.  Thus it is an exact normalization
counterguard, not a point of the full branch-(iii) source ideal.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import sympy as sp

import verify_shared_reciprocal_two_bad_mixed_bright_completion as chart


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_shared_reciprocal_two_bad_common_radical_provenance_system.py":
        "0f038dc17dbe711797318a1277cf68f751b6bb01423ccbb8eef0888ba96bedea",
    "computations/verify_shared_reciprocal_two_bad_bright_whole_kernel_site_flag.py":
        "0c15867705ac57b9c5fa5e03317d1c7b25bfbc6aed53a8e1172a1d46eb41df07",
}
EXPECTED_DIGEST = "afdad773a71ad0b1b4cd4da546b44fcfba228bea75471e14f60e3005aecfd185"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def pure_vector(colour):
    return sp.Matrix([
        int(word == (colour,) * len(chart.SITES)) for word in chart.WORDS
    ])


def displayed_cells():
    return {
        ((1, 2), chart.A, chart.A): sp.Rational(3, 5),
        ((0, 2), chart.A, chart.A): sp.Rational(4, 5),
        ((3, 4), chart.A, chart.A): sp.S.One,
        ((0, 1), chart.C, chart.C): sp.S.One,
        ((2, 3), chart.C, chart.C): sp.S.One,
        ((0, 2), chart.C, chart.A): sp.S.One,
        ((0, 2), chart.T, chart.A): sp.S.One,
    }


def sparse_row(entries):
    vector = sp.zeros(len(chart.LABELS), 1)
    for label, value in entries.items():
        vector[chart.LABELS.index(label)] = value
    return vector


def audit_counterguard():
    cells = displayed_cells()
    phi, cofactors = chart.phi_matrix(cells)
    require(phi.rank() == 11 and len(phi.nullspace()) == 4,
            "the seven-cell counterguard rank changed")

    preimage_a = sparse_row({(0, chart.A): sp.Rational(5, 3)})
    preimage_c = sparse_row({(4, chart.C): sp.S.One})
    require(phi * preimage_a == pure_vector(chart.A),
            "the counterguard lost its X_a preimage")
    require(phi * preimage_c == pure_vector(chart.C),
            "the counterguard lost its X_c preimage")
    require(phi.rank() < phi.row_join(pure_vector(chart.T)).rank(),
            "the counterguard acquired X_t in im(Phi)")

    kernels = (
        sparse_row({
            (0, chart.A): sp.Rational(-4, 3),
            (0, chart.C): sp.Rational(-5, 3),
            (0, chart.T): sp.Rational(-5, 3),
            (1, chart.A): sp.S.One,
        }),
        sparse_row({(3, chart.A): sp.S.One}),
        sparse_row({(3, chart.C): sp.S.One}),
        sparse_row({(3, chart.T): sp.S.One}),
    )
    require(all(phi * vector == sp.zeros(len(chart.WORDS), 1)
                for vector in kernels),
            "a displayed counterguard kernel row stopped vanishing")
    require(sp.Matrix.hstack(*kernels).rank() == 4,
            "the displayed kernel rows stopped being a basis")

    target_projection = sp.Matrix([
        [vector[chart.LABELS.index((site, chart.T))]
         for site in chart.SITES]
        for vector in kernels
    ])
    require(target_projection.rank() == 2,
            "the counterguard target projection changed")
    require({index for index in range(target_projection.cols)
             if any(target_projection[row, index]
                    for row in range(target_projection.rows))} == {0, 3},
            "the minimal target pair changed")

    kernel_zero_sites = tuple(
        site for site in chart.SITES
        if all(vector[chart.LABELS.index((site, colour))] == 0
               for vector in kernels for colour in range(3))
    )
    require(kernel_zero_sites == (2, 4),
            "the whole-kernel zero-evaluation sites changed")
    fixed_zero_a = tuple(
        site for site in kernel_zero_sites
        if all(preimage_a[chart.LABELS.index((site, colour))] == 0
               for colour in range(3))
    )
    fixed_zero_c = tuple(
        site for site in kernel_zero_sites
        if all(preimage_c[chart.LABELS.index((site, colour))] == 0
               for colour in range(3))
    )
    require(fixed_zero_a == (2, 4) and fixed_zero_c == (2,),
            "the affine bright-fibre fixed-zero sets changed")

    pure_target_word = (chart.T,) * 4
    target_cofactors = tuple(
        sp.factor(cofactors[hole].get(pure_target_word, 0))
        for hole in chart.SITES
    )
    require(target_cofactors == (0,) * 5,
            "the fixed-zero counterguard acquired a pure-target cofactor")

    return {
        "cells": len(cells),
        "phi_rank": phi.rank(),
        "kernel_dimension": len(kernels),
        "target_projection_dimension": target_projection.rank(),
        "minimal_target_pair": [0, 3],
        "affine_Xa_fixed_zero_sites": list(fixed_zero_a),
        "affine_Xc_fixed_zero_sites": list(fixed_zero_c),
        "pure_target_cofactors": [int(value) for value in target_cofactors],
        "full_row_exclusion": "R=0 contradicts D_tt*R=1",
    }


def main():
    pin_dependencies()
    counterguard = audit_counterguard()
    ledger = {
        "pins": PINS,
        "counterguard": counterguard,
        "verdict": (
            "bright images and a two-dimensional target projection do not "
            "force a zero-free private-row chart; a fixed-zero affine "
            "bright fibre is the first exact evasion"
        ),
        "scope": (
            "literal rational five-site common quadratic; excluded from "
            "the full branch-(iii) ideal by the pure-target chord equation"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"bright fixed-zero counterguard ledger changed: {digest}")

    print("shared reciprocal bright fixed-zero counterguard: PASS")
    print("both affine bright fibres vanish at site 2")
    print("dim pi_t ker(Phi)=2 on target pair {0,3}")
    print("full-row guard: R=0 contradicts D_tt*R=1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
