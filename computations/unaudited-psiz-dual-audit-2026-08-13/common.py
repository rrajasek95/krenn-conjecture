#!/usr/bin/env python3
"""Shared exact-rational machinery for the psi_z dual-route probe.

UNAUDITED external probe.  Pinned HEAD 0a684ce0b11dd0a0e102f970f5ad69747d2cb4bb.
Everything is exact over Q (fractions.Fraction).  All committed code is read
from a `git archive HEAD` snapshot, never from the dirty worktree.
"""

from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import os
import sys
from pathlib import Path


SNAP = Path(os.environ.get(
    "PSIZ_SNAP",
    "/private/tmp/claude-501/-Users-rishi/f8396279-dd28-41de-876d-5c03a4d8d65a"
    "/scratchpad/psiz-audit/snap",
))
OUT = Path(__file__).resolve().parent
PINNED_HEAD = "0a684ce0b11dd0a0e102f970f5ad69747d2cb4bb"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    """Import a committed checker from the frozen snapshot."""
    path = SNAP / relative
    require(path.exists(), ("missing snapshot file", relative))
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
# exact linear algebra over Q
# --------------------------------------------------------------------------

def dot(left, right) -> Q:
    require(len(left) == len(right), ("dot width", len(left), len(right)))
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors):
    require(vectors and len({len(v) for v in vectors}) == 1, "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def _echelon(columns):
    """Return (pivot rows, reduced rows) of the matrix whose COLUMNS are given."""
    if not columns:
        return [], []
    height = len(columns[0])
    require(all(len(c) == height for c in columns), "rank height")
    work = [[Q(columns[c][r]) for c in range(len(columns))]
            for r in range(height)]
    pivots = []
    answer = 0
    for column in range(len(columns)):
        pivot = next((r for r in range(answer, height) if work[r][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [a - factor * b
                         for a, b in zip(work[row], work[answer], strict=True)]
        pivots.append(column)
        answer += 1
    return pivots, work[:answer]


def rank(columns) -> int:
    return len(_echelon(columns)[0])


def in_span(columns, target) -> bool:
    """Exact membership of `target` in the column span."""
    if not columns:
        return all(value == 0 for value in target)
    return rank(list(columns)) == rank(list(columns) + [tuple(target)])


def left_kernel(columns):
    """Basis of {psi : psi . c = 0 for every column c}, as row vectors."""
    if not columns:
        return []
    height = len(columns[0])
    # Solve psi * A = 0 where A has the columns as columns: i.e. the kernel of
    # A^T acting on R^height.  Build rows of A^T = the columns themselves.
    rows = [tuple(Q(v) for v in column) for column in columns]
    # Gaussian elimination on `rows` (each of length `height`).
    matrix = [list(row) for row in rows]
    pivots = []
    r = 0
    for column in range(height):
        pivot = next((i for i in range(r, len(matrix)) if matrix[i][column]),
                     None)
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        value = matrix[r][column]
        matrix[r] = [entry / value for entry in matrix[r]]
        for i in range(len(matrix)):
            if i == r or not matrix[i][column]:
                continue
            factor = matrix[i][column]
            matrix[i] = [a - factor * b
                         for a, b in zip(matrix[i], matrix[r], strict=True)]
        pivots.append(column)
        r += 1
    free = [c for c in range(height) if c not in pivots]
    basis = []
    for f in free:
        vector = [Q(0)] * height
        vector[f] = Q(1)
        for index, column in enumerate(pivots):
            vector[column] = -matrix[index][f]
        basis.append(tuple(vector))
    return basis


def primitive(vector):
    """Scale a rational vector to a primitive integer vector (sign-normalized)."""
    from math import gcd
    nonzero = [value for value in vector if value]
    if not nonzero:
        return tuple(vector)
    denominator = 1
    for value in nonzero:
        denominator = denominator * value.denominator // gcd(
            denominator, value.denominator)
    scaled = [int(value * denominator) for value in vector]
    g = 0
    for value in scaled:
        g = gcd(g, abs(value))
    scaled = [value // g for value in scaled]
    first = next(value for value in scaled if value)
    if first < 0:
        scaled = [-value for value in scaled]
    return tuple(scaled)


# --------------------------------------------------------------------------
# the four-coordinate chart square (0ffc23a conventions)
# --------------------------------------------------------------------------

CHART_BASIS = ("A_[a|b]", "A_[b|a]", "B", "C")
Z = tuple(map(Q, (1, 1, -1, -1)))          # the balanced class
PSI_Z = tuple(value / 4 for value in Z)    # normalized primitive dual
GAUGE = Z                                  # shore-sign gauge diag(1,1,-1,-1)

MATE_ROWS = (
    (Q(1), Q(0), Q(1), Q(0)),   # A_ab + B
    (Q(0), Q(1), Q(0), Q(1)),   # A_ba + C
    (Q(1), Q(0), Q(0), Q(1)),   # A_ab + C
    (Q(0), Q(1), Q(1), Q(0)),   # A_ba + B
)


def gauged_augmentation(square_vector) -> Q:
    """<z, v>: the gauged vertex augmentation of a chart-square vector."""
    return dot(GAUGE, square_vector)


def verify_chart_basis_conventions() -> dict:
    """Reproduce the master-obstruction note's facts EXACTLY.

    Any broken projection must fail here (mutation control D).
    """
    require(rank(MATE_ROWS) == 3, "mate rows lost rank 3")
    require(all(dot(Z, row) == 0 for row in MATE_ROWS),
            "z stopped annihilating the mate rows")
    require(rank(MATE_ROWS + (Z,)) == 4, "z is no longer the missing direction")
    require(left_kernel(list(MATE_ROWS)) and
            primitive(left_kernel(list(MATE_ROWS))[0]) == (1, 1, -1, -1),
            "z is not the unique annihilator")
    require(len(left_kernel(list(MATE_ROWS))) == 1,
            "the annihilator stopped being unique")
    require(dot(PSI_Z, Z) == 1 and
            all(dot(PSI_Z, row) == 0 for row in MATE_ROWS),
            "psi_z normalization changed")
    # Gate-II ordered projection and the operation-tag factorization.
    require((Z[0] + Z[1], Z[2], Z[3]) == (Q(2), Q(-1), Q(-1)),
            "Gate-II projection changed")
    chart_sign, matching_constant = (Q(1), Q(-1)), (Q(1), Q(1))
    require(tuple(a * b for a in chart_sign for b in matching_constant) == Z,
            "operation-tag factorization changed")
    # shore-sign gauge sends z to the constant class; image = ker(augmentation)
    gauged = tuple(tuple(GAUGE[i] * e for i, e in enumerate(column))
                   for column in MATE_ROWS)
    require(rank(gauged) == 3 and
            all(sum(column, Q(0)) == 0 for column in gauged),
            "the shore-sign gauge changed")
    require(gauged_augmentation(Z) == 4, "dE=z gauged augmentation != 4")
    return {
        "chart_basis": list(CHART_BASIS),
        "z": [str(v) for v in Z],
        "psi_z": [str(v) for v in PSI_Z],
        "mate_row_rank": 3,
        "rank_with_z": 4,
        "unique_annihilator": [1, 1, -1, -1],
        "gate_II_projection": [2, -1, -1],
        "gauged_augmentation_of_z": 4,
    }


# --------------------------------------------------------------------------
# the 30-coordinate augmented ambient (Gate-II chi_w nonfill conventions)
# --------------------------------------------------------------------------

LABELS = (
    *(f"B{j}" for j in range(4)),
    *(f"Eq{j}" for j in range(4)),
    "M", "ainc", "q", "P_f",
    *(f"target{j}" for j in range(4)),
    *(f"W{j}" for j in range(4)),
    *(f"ores{j}" for j in range(4)),
    "ridge", "eta_constant", "eta_u_over_t", "sigma_q22",
    "W_global", "common_tail_escape",
)
INDEX = {label: i for i, label in enumerate(LABELS)}
ALPHA = tuple(map(Q, (-1, 1, 1, -1)))


def vec(**entries):
    unknown = set(entries) - set(LABELS)
    require(not unknown, ("unknown labels", sorted(unknown)))
    return tuple(Q(entries.get(label, 0)) for label in LABELS)


def square_projection(column):
    """pi: ambient -> chart square.  The four B-corners ARE the chart basis."""
    require(len(column) == len(LABELS), "ambient width")
    return tuple(column[INDEX[f"B{j}"]] for j in range(4))


def psi_ambient(alpha=ALPHA, delta=Z):
    """The cap/Cartan extension of psi_z to the ambient, un-normalized (x4).

    B=delta, target=-delta, W=-delta, ores=delta, ridge=-alpha.delta,
    every other coefficient zero.  See 0ffc23a / the chi_w nonfill note.
    """
    return vec(**{
        **{f"B{j}": delta[j] for j in range(4)},
        **{f"target{j}": -delta[j] for j in range(4)},
        **{f"W{j}": -delta[j] for j in range(4)},
        **{f"ores{j}": delta[j] for j in range(4)},
        "ridge": -dot(alpha, delta),
    })
