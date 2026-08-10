#!/usr/bin/env python3
"""Exact minimal second-kernel gate above the repaired primitive cycle.

Inside the nonzero five-parameter primitive-cycle chart, direct bright
purity plus the only available K3/K4 column collision leaves the equation
2*z*w=0.  Over characteristic zero a third matching path is necessary.
It requires two new cells, 01:ta and 34:at.  Their product cancels the
factor-two residue, but their cross-products with the existing cc cells
create two private K2 words, so X_c leaves im(Phi).

The checker freezes the resulting rational rank-13/nullity-2 packet and
checks the full kernel-product span.  X_t still does not enter.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import sympy as sp

import verify_shared_reciprocal_two_bad_mixed_bright_completion as chart


ROOT = Path(__file__).resolve().parents[1]
PINNED_PRIMITIVE_SHA256 = (
    "eca801937ec369057428476cc405a3d0e5d9404f001d0b67c857e240174e1bd0"
)
EXPECTED_DIGEST = "8d5f4c3d0b076402176048178e44701f5b28f346c6d9108f096d060897c2f39c"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_mixed_primitive_cycle_gate.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_PRIMITIVE_SHA256,
            "the primitive-cycle dependency changed")


def parameter_cells(z, y, b, w, v, r=0, s=0):
    cells = chart.representative_cells()
    chart.put(cells, 0, 4, chart.T, chart.T, z)
    chart.put(cells, 1, 4, chart.A, chart.T, y)
    chart.put(cells, 0, 4, chart.A, chart.T, b)
    chart.put(cells, 1, 3, chart.A, chart.A, w)
    chart.put(cells, 0, 3, chart.T, chart.A, v)
    if r:
        chart.put(cells, 0, 1, chart.T, chart.A, r)
    if s:
        chart.put(cells, 3, 4, chart.A, chart.T, s)
    return cells


def symbolic_factor_two_gate():
    z, y, b, w, v = sp.symbols("z y b w v", nonzero=True)
    cells = parameter_cells(z, y, b, w, v)
    _phi, cofactors = chart.phi_matrix(cells)

    expected = {
        2: {
            (chart.C, chart.C, chart.C, chart.C): 1,
            (chart.A, chart.A, chart.A, chart.T): y + b * w,
            (chart.T, chart.A, chart.A, chart.T): v * y + z * w,
        },
        3: {
            (chart.T, chart.A, chart.A, chart.T): z + y,
            (chart.A, chart.A, chart.A, chart.T): b,
        },
        4: {
            (chart.A, chart.A, chart.A, chart.A): 1,
            (chart.T, chart.A, chart.A, chart.A): w + v,
        },
    }
    for hole, tensor in expected.items():
        require({word: sp.factor(value) for word, value
                 in cofactors[hole].items()} == tensor,
                f"the symbolic K_{hole} formula changed: {cofactors[hole]}")

    equations = {
        "K2_AAAT": y + b * w,
        "K2_TAAT": v * y + z * w,
        "K4_TAAA": w + v,
        "K3_private_TAAT": z + y,
    }
    substitution = {v: -w, y: -z, b: z / w}
    residue = sp.factor(equations["K2_TAAT"].subs(substitution))
    require(residue == 2 * z * w,
            f"the characteristic-zero residue changed: {residue}")
    return {
        "equations": {name: str(value) for name, value in equations.items()},
        "forced_substitution": {"v": "-w", "y": "-z", "b": "z/w"},
        "remaining_residue": str(residue),
    }


def symbolic_third_path():
    z, w, r = sp.symbols("z w r", nonzero=True)
    y = -z
    b = z / w
    v = -w
    s = -2 * z * w / r
    cells = parameter_cells(z, y, b, w, v, r, s)
    phi, cofactors = chart.phi_matrix(cells)

    expected_k2 = {
        (chart.C, chart.C, chart.C, chart.C): 1,
        (chart.C, chart.C, chart.A, chart.T): s,
        (chart.T, chart.A, chart.C, chart.C): r,
    }
    require({word: sp.factor(value) for word, value in cofactors[2].items()}
            == expected_k2,
            f"the minimal third-path K2 changed: {cofactors[2]}")

    pure_word = (chart.C,) * 5
    private_s = (chart.C, chart.C, chart.C, chart.A, chart.T)
    private_r = (chart.T, chart.A, chart.C, chart.C, chart.C)
    rows = {
        "pure": chart.WORDS.index(pure_word),
        "private_s": chart.WORDS.index(private_s),
        "private_r": chart.WORDS.index(private_r),
    }
    columns = {}
    for name, row in rows.items():
        columns[name] = [
            (chart.LABELS[column], sp.factor(phi[row, column]))
            for column in range(phi.cols) if phi[row, column] != 0
        ]
    require(columns == {
        "pure": [((2, chart.C), 1)],
        "private_s": [((2, chart.C), s)],
        "private_r": [((2, chart.C), r)],
    }, f"the two private bright rows changed: {columns}")
    return {
        "third_path_cells": ["01:ta=r", "34:at=s=-2zw/r"],
        "K2": {str(word): str(value) for word, value in expected_k2.items()},
        "private_rows": {
            name: [list(label), str(value)]
            for name, ((label, value),) in columns.items()
        },
    }


def rational_packet():
    cells = parameter_cells(
        z=1, y=-1, b=1, w=1, v=-1, r=1, s=-2
    )
    audit = chart.full_audit(cells)
    expected_summary = (13, 2, 24, 2, (True, False, False), False)
    require(audit["summary"] == expected_summary,
            f"the minimal two-kernel packet changed: {audit['summary']}")

    u = sp.zeros(len(chart.LABELS), 1)
    u[chart.LABELS.index((0, chart.T))] = 1
    u[chart.LABELS.index((1, chart.A))] = -1
    v = sp.zeros(len(chart.LABELS), 1)
    v[chart.LABELS.index((3, chart.A))] = 1
    v[chart.LABELS.index((4, chart.T))] = -1
    require(audit["phi"] * u == sp.zeros(len(chart.WORDS), 1),
            "the first tilted kernel changed")
    require(audit["phi"] * v == sp.zeros(len(chart.WORDS), 1),
            "the second tilted kernel changed")
    require(sp.Matrix.hstack(u, v).rank() == 2,
            "the two displayed kernels became dependent")

    expected_cofactors = {
        0: {
            (chart.A, chart.A, chart.C, chart.C): 1,
            (chart.A, chart.A, chart.A, chart.T): -2,
        },
        1: {
            (chart.T, chart.A, chart.C, chart.C): 1,
            (chart.T, chart.A, chart.A, chart.T): -2,
        },
        2: {
            (chart.C, chart.C, chart.C, chart.C): 1,
            (chart.C, chart.C, chart.A, chart.T): -2,
            (chart.T, chart.A, chart.C, chart.C): 1,
        },
        3: {(chart.A, chart.A, chart.A, chart.T): 1},
        4: {(chart.A, chart.A, chart.A, chart.A): 1},
    }
    require(audit["cofactors"] == expected_cofactors,
            f"the rational two-kernel cofactors changed: {audit['cofactors']}")
    return {
        "summary": list(expected_summary[:4]),
        "image_flags": list(expected_summary[4]),
        "Xt_in_augmented_span": expected_summary[5],
        "kernel_supports": [
            ["0:t", "1:a"],
            ["3:a", "4:t"],
        ],
    }


def main():
    pin_dependency()
    factor_two = symbolic_factor_two_gate()
    third_path = symbolic_third_path()
    rational = rational_packet()
    ledger = {
        "pinned_primitive_sha256": PINNED_PRIMITIVE_SHA256,
        "factor_two_gate": factor_two,
        "minimal_third_matching_path": third_path,
        "rational_two_kernel_packet": rational,
        "verdict": (
            "the minimal second kernel requires the two-cell 01/34 third "
            "matching; its unavoidable cross terms remove X_c, and X_t "
            "still stays outside the complete kernel-product span"
        ),
        "scope": (
            "the canonical repaired primitive-cycle chart with nonzero "
            "selected cells, over characteristic zero"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"mixed second-kernel ledger changed: {digest}")

    print("shared reciprocal two-bad mixed second kernel: PASS")
    print("zero-new-cell collision residue: 2*z*w")
    print("minimal third matching: two cells 01:ta and 34:at")
    print("two-kernel packet: X_c leaves im(Phi), X_t stays out of products")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
