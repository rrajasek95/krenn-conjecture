#!/usr/bin/env python3
"""Verify terminal-safe cancellation of a dark Cartan potential.

Suppose a complete augmented map has scalar columns C and one physical
Cartan column g, with g=C y.  Then k=(-y,1) is a unit-coefficient kernel
class.  A physical terminal q gives an exact alternative:

* q(k) != 0: k normalizes to the relative generator;
* q(k) == 0: quotienting the domain by <k> preserves the augmented image,
  cokernel, and the image of q on the remaining kernel.

The second branch is a presentation cancellation, not a same-row support
deletion.  If g is visible in both deficient endpoint quotients, its scalar
expansion contains either one double-visible column or two split-visible
columns.  Landing those physical columns is a separate theorem.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_oo_dark_potential_source_promotion_counterguard.py":
        "76bdd6c8ce19cc466995b235bade9114d7d2779b74bfcd25eea703c2d1de3db2",
    "computations/verify_uniform_cartan_critical_component_placement_gate.py":
        "68c56c1a9144dd92fa803962697de60b78b58a125191450f1af1abcd1befe2a1",
    "computations/verify_h3_transverse_double_quotient_cartan_landing.py":
        "e2b536a2cc8e20883208dc098c84c6dabe15c5c01777f6018a8b72981274b5ae",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
}
EXPECTED_LEDGER_SHA256 = (
    "35210bb4345bd678bf8a52d08de8d56a650e50d5b4fa30b34a69f4eb0efbb612"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def mat_vec(matrix, vector):
    return tuple(sum(Q(entry) * Q(value)
                     for entry, value in zip(row, vector, strict=True))
                 for row in matrix)


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return (), ()
    rows = len(work)
    columns = len(work[0])
    pivots = []
    pivot_row = 0
    for column in range(columns):
        found = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if found is None:
            continue
        work[pivot_row], work[found] = work[found], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [a - factor * b
                         for a, b in zip(work[row], work[pivot_row],
                                         strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    columns = len(matrix[0]) if matrix else 0
    free = [column for column in range(columns) if column not in pivots]
    answer = []
    for free_column in free:
        vector = [Q(0)] * columns
        vector[free_column] = Q(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        answer.append(tuple(vector))
    return tuple(answer)


def column_matrix(columns):
    return transpose(columns)


def audit_instance(columns_c, y, terminal_c, terminal_g,
                   quotient_u, quotient_v):
    """Audit one exact dark instance.

    ``columns_c`` are codomain column vectors.  The last augmented column is
    their y-combination.  Quotient functionals live on the codomain.
    """
    g = tuple(sum(Q(coefficient) * Q(column[row])
                  for coefficient, column in zip(y, columns_c, strict=True))
              for row in range(len(columns_c[0])))
    columns = tuple(tuple(map(Q, column)) for column in columns_c) + (g,)
    matrix = column_matrix(columns)
    kernel = nullspace(matrix)
    k = tuple(-Q(value) for value in y) + (Q(1),)
    require(mat_vec(matrix, k) == (Q(0),) * len(matrix),
            "dark unit vector left the kernel")
    require(k in kernel or rank(column_matrix(kernel + (k,))) == len(kernel),
            "dark unit vector was not in the computed kernel")

    terminal = tuple(map(Q, terminal_c)) + (Q(terminal_g),)
    qk = sum(a * b for a, b in zip(terminal, k, strict=True))

    # The quotient L/<k> can use the scalar columns as representatives,
    # because e_g = sum y_i e_i modulo k.  Its augmented matrix is C.
    scalar_matrix = column_matrix(columns[:-1])
    require(rank(matrix) == rank(scalar_matrix),
            "unit-kernel quotient changed the augmented image")
    require(len(matrix[0]) - rank(matrix)
            == (len(scalar_matrix[0]) - rank(scalar_matrix)) + 1,
            "the unit kernel did not split off exactly one domain line")

    scalar_kernel = nullspace(scalar_matrix)
    if qk == 0:
        # Every full kernel vector is a scalar-kernel lift plus a multiple of
        # k.  Hence q has exactly the same image after quotienting by <k>.
        for vector in kernel:
            scalar_lift = tuple(Q(a) + Q(vector[-1]) * Q(b)
                                for a, b in zip(vector[:-1], y,
                                                strict=True))
            require(mat_vec(scalar_matrix, scalar_lift)
                    == (Q(0),) * len(scalar_matrix),
                    "full kernel did not descend to the scalar quotient")
            full_value = sum(a * b for a, b in
                             zip(terminal, vector, strict=True))
            scalar_value = sum(Q(a) * Q(b) for a, b in
                               zip(terminal_c, scalar_lift, strict=True))
            require(full_value == scalar_value,
                    "terminal image changed on the killed dark line")

    visible_u = [index for index, column in enumerate(columns_c)
                 if sum(Q(a) * Q(b)
                        for a, b in zip(quotient_u, column, strict=True))]
    visible_v = [index for index, column in enumerate(columns_c)
                 if sum(Q(a) * Q(b)
                        for a, b in zip(quotient_v, column, strict=True))]
    g_u = sum(Q(a) * Q(b) for a, b in zip(quotient_u, g, strict=True))
    g_v = sum(Q(a) * Q(b) for a, b in zip(quotient_v, g, strict=True))
    double = sorted(set(visible_u) & set(visible_v))
    if g_u and g_v:
        require(visible_u and visible_v,
                "double-visible g had no scalar visible columns")
        require(double or any(i != j for i in visible_u for j in visible_v),
                "visibility supplied neither one double nor two split columns")

    return {
        "rank_full": rank(matrix),
        "rank_quotient": rank(scalar_matrix),
        "kernel_full": len(kernel),
        "kernel_quotient": len(scalar_kernel),
        "terminal_on_dark_kernel": str(qk),
        "u_visible_scalar_columns": visible_u,
        "v_visible_scalar_columns": visible_v,
        "double_visible_scalar_columns": double,
        "g_double_visible": bool(g_u and g_v),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    # Type-split version of the smallest dark guard.  There is no same-row
    # scalar dependence, but the terminal-killed unit line can still be
    # removed from the augmented presentation.  Its two scalar columns are
    # respectively visible at the two deficient endpoint quotients.
    split = audit_instance(
        columns_c=((1, 0), (0, 1)),
        y=(1, 1),
        terminal_c=(0, 0),
        terminal_g=0,
        quotient_u=(1, 0),
        quotient_v=(0, 1),
    )
    require(split["terminal_on_dark_kernel"] == "0"
            and not split["double_visible_scalar_columns"]
            and split["u_visible_scalar_columns"] == [0]
            and split["v_visible_scalar_columns"] == [1],
            "type-split cancellation guard changed")

    # A terminal-detected dark class normalizes to the generator instead of
    # being quotiented out.
    detected = audit_instance(
        columns_c=((1, 0), (0, 1)),
        y=(1, 1),
        terminal_c=(0, 0),
        terminal_g=1,
        quotient_u=(1, 1),
        quotient_v=(1, -1),
    )
    require(detected["terminal_on_dark_kernel"] == "1",
            "detected dark generator stopped being primitive")

    # Exhaust small exact matrices to mutation-guard the rank and terminal
    # alternatives.  The last column is always a chosen scalar combination.
    exhaustive = 0
    terminal_killed = 0
    terminal_detected = 0
    visibility_packets = 0
    for flat in product((-1, 0, 1), repeat=4):
        columns_c = ((flat[0], flat[1]), (flat[2], flat[3]))
        if columns_c[0] == (0, 0) or columns_c[1] == (0, 0):
            continue
        for y in product((-1, 0, 1), repeat=2):
            if y == (0, 0):
                continue
            for terminal_c in product((-1, 0, 1), repeat=2):
                for terminal_g in (-1, 0, 1):
                    record = audit_instance(
                        columns_c=columns_c,
                        y=y,
                        terminal_c=terminal_c,
                        terminal_g=terminal_g,
                        quotient_u=(1, 0),
                        quotient_v=(0, 1),
                    )
                    exhaustive += 1
                    if record["terminal_on_dark_kernel"] == "0":
                        terminal_killed += 1
                    else:
                        terminal_detected += 1
                    if record["g_double_visible"]:
                        visibility_packets += 1

    ledger = {
        "pins": PINS,
        "theorem": (
            "if a complete Cartan column satisfies Jg=JC*y, then "
            "k=(-y,1) is a unit kernel class.  If a physically typed "
            "terminal q detects k, k/q(k) is the relative generator.  If "
            "q(k)=0, passage to L/<k> preserves im(J), coker(J), and "
            "q(ker J), while removing exactly one domain/kernel line"
        ),
        "rank_consequence": (
            "if the Cartan image is nonzero in both one-dimensional "
            "deficient endpoint quotients, its scalar expansion contains "
            "one double-visible scalar column or two split-visible scalar "
            "columns"
        ),
        "split_guard": split,
        "detected_guard": detected,
        "exhaustive_small_instances": exhaustive,
        "terminal_killed_instances": terminal_killed,
        "terminal_detected_instances": terminal_detected,
        "double_visible_cartan_instances": visibility_packets,
        "scope": (
            "this is a terminal-safe contraction of the augmented source "
            "presentation, not deletion of an original graph coefficient. "
            "Physical typing of q and landing the resulting double/split "
            "scalar columns at four-good rank remain separate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("dark Cartan terminal-safe cancellation: PASS")
    print("small exact instances:", ledger["exhaustive_small_instances"])
    print("terminal killed:", ledger["terminal_killed_instances"])
    print("terminal detected:", ledger["terminal_detected_instances"])
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
