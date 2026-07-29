#!/usr/bin/env python3
"""Exact audits for notes/staircase-overlap-fixed-pair.md."""

from __future__ import annotations

import sympy as sp


def symbolic_cross_entry_audit() -> None:
    u0, u1, u2 = sp.symbols("u0 u1 u2")
    v0, v1, v2 = sp.symbols("v0 v1 v2")
    w0, w1, w2 = sp.symbols("w0 w1 w2")
    b0, b1 = sp.symbols("b0 b1", nonzero=True)

    e0, e1, e2 = (sp.eye(3)[:, i] for i in range(3))
    u = sp.Matrix([u0, u1, u2])
    v = sp.Matrix([v0, v1, v2])
    w = sp.Matrix([w0, w1, w2])

    q = e0 * e0.T + (e1 * u.T + v * e2.T) / b0
    p = e1 * e1.T + (-e0 * u.T + w * e2.T) / b1
    ks = (
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
        sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
    )
    entries = tuple(sp.factor((p * k * q.T)[1, 0]) for k in ks)
    assert entries == (v0 / b0, w1 / b1, -1)


def coefficient(tensor_term, i: int, j: int, k: int):
    return sp.expand(tensor_term(i, j, k))


def unlimited_overlap_audit() -> None:
    e0, e1, e2 = (sp.eye(3)[:, i] for i in range(3))
    v = sp.ones(3, 1)
    w = sp.ones(3, 1)
    a_pq = e2 * e2.T - e0 * v.T - w * e1.T
    assert a_pq.det() == 1

    ks = (
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
        sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
    )

    # Five independent third-site labels are enough to audit that no
    # cross-site compatibility is being used.  The same calculation works
    # for an arbitrary number of labels.
    for t_value in (-3, -1, 0, 2, 7):
        u = sp.Matrix([1, 1, t_value])
        a_qx = e0 * e0.T + e1 * u.T + v * e2.T
        a_px = e1 * e1.T - e0 * u.T + w * e2.T
        assert a_px.det() == -1
        assert a_qx.det() == 1

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    lhs = (
                        (1 if i == 0 else 0) * a_qx[j, k]
                        + (1 if j == 1 else 0) * a_px[i, k]
                        + (1 if k == 2 else 0) * a_pq[i, j]
                    )
                    rhs = 1 if i == j == k else 0
                    assert sp.expand(lhs - rhs) == 0

        cross_entries = tuple((a_px * kr * a_qx.T)[1, 0] for kr in ks)
        assert cross_entries == (1, 1, -1)


if __name__ == "__main__":
    symbolic_cross_entry_audit()
    unlimited_overlap_audit()
    print("PASS: fixed-pair staircase overlap and cross-entry audits")
