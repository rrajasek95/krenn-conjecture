#!/usr/bin/env python3
"""Make the physical six-term alternative stable under all relative cells.

Let J0 be the complete protected physical map (boundary, W, target, ordinary
residue, and every other required zero row) on an arbitrary finite relative
source degree, and let q be the physically typed six-term anchor readout.
Exactly one rank event occurs:

* rank([J0;q])>rank(J0): some x in ker(J0) has q(x)!=0 and normalizes to the
  protected-zero relative anchor;
* rank([J0;q])=rank(J0): q=lambda J0, so (-lambda,1) is a left separator of
  the complete augmented column map.

This applies to the full relative extension at once; new relative generators
cannot form a third branch.  The five facewise readouts assemble through the
rank-four C5 edge lattice, whose sole primitive direction pairs to five.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_cyclic_physical_separator_or_aggregate_generator.py":
        "74a5f35448fcb860ed15e7201142ba9ea43aad7765f0ffaa7cf483c01780a261",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
    "computations/verify_h3_rootless_augmented_pentagon_fredholm_alternative.py":
        "0b0831391416f85302b5f2d89da0672e07dca4c73fc5f3893ad992abd48c1d2b",
}
EXPECTED_LEDGER_SHA256 = "7efd330f4d1b4bf4d7d6fc60e71c33df798896eb11c556b1122dc990636fd579"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rref(matrix):
    answer = [[Q(value) for value in row] for row in matrix]
    if not answer:
        return answer, ()
    rows = len(answer)
    columns = len(answer[0])
    pivots = []
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if answer[row][column]), None)
        if pivot is None:
            continue
        answer[pivot_row], answer[pivot] = answer[pivot], answer[pivot_row]
        value = answer[pivot_row][column]
        answer[pivot_row] = [entry / value for entry in answer[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not answer[row][column]:
                continue
            value = answer[row][column]
            answer[row] = [left - value * right for left, right in
                           zip(answer[row], answer[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return answer, tuple(pivots)


def rank(rows):
    return len(rref(rows)[1]) if rows else 0


def nullspace(rows, width):
    if not rows:
        return tuple(tuple(Q(int(index == free)) for index in range(width))
                     for free in range(width))
    reduced, pivots = rref(rows)
    free_columns = [column for column in range(width) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [Q(0)] * width
        vector[free] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(tuple(vector))
    return tuple(basis)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def solve_row_combination(rows, target):
    """Return lambda with lambda*rows=target, or None."""
    if not rows:
        return () if not any(target) else None
    # Solve rows^T lambda = target^T by reducing the augmented matrix.
    variables = len(rows)
    equations = [list(column) + [Q(value)] for column, value in
                 zip(zip(*rows, strict=True), target, strict=True)]
    reduced, pivots = rref(equations)
    if any(not any(row[:variables]) and row[variables] for row in reduced):
        return None
    solution = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            solution[pivot] = reduced[row][variables]
    require(all(sum(solution[index] * Q(rows[index][column])
                    for index in range(variables)) == Q(target[column])
                for column in range(len(target))),
            "row-combination reconstruction failed")
    return tuple(solution)


def audit_binary_matrices():
    cases = 0
    generator_cases = 0
    separator_cases = 0
    for height in range(3):
        for width in range(1, 5):
            entry_count = height * width + width
            for bits in product((0, 1), repeat=entry_count):
                flat_j = bits[:height * width]
                q = tuple(Q(value) for value in bits[height * width:])
                rows = tuple(tuple(Q(flat_j[row * width + column])
                                   for column in range(width))
                             for row in range(height))
                base_rank = rank(rows)
                augmented_rank = rank(rows + (q,))
                kernel = nullspace(rows, width)
                visible = next((vector for vector in kernel if dot(q, vector)),
                               None)
                combination = solve_row_combination(rows, q)
                if augmented_rank > base_rank:
                    require(visible is not None and combination is None,
                            "the generator branch lost its kernel witness")
                    normalized = tuple(value / dot(q, visible)
                                       for value in visible)
                    require(all(dot(row, normalized) == 0 for row in rows)
                            and dot(q, normalized) == 1,
                            "the normalized protected-zero anchor changed")
                    generator_cases += 1
                else:
                    require(visible is None and combination is not None,
                            "the separator branch lost its row factorization")
                    require(all(Q(q[column]) == sum(
                                combination[row] * rows[row][column]
                                for row in range(height))
                                for column in range(width)),
                            "the complete left separator changed")
                    separator_cases += 1
                cases += 1
    require(cases == 5050 and generator_cases and separator_cases,
            ("the exhaustive matrix census changed", cases,
             generator_cases, separator_cases))
    return {
        "binary_complete_maps": cases,
        "protected_zero_generator_cases": generator_cases,
        "physical_separator_cases": separator_cases,
    }


def audit_cyclic_aggregate():
    edges = (
        (-1, 0, 1, 0, 0),
        (0, 0, -1, 0, 1),
        (0, 1, 0, 0, -1),
        (0, -1, 0, 1, 0),
        (1, 0, 0, -1, 0),
    )
    ones = (1, 1, 1, 1, 1)
    require(rank(edges) == 4 and all(dot(ones, edge) == 0 for edge in edges),
            "the cyclic edge lattice changed")
    require(dot(ones, ones) == 5,
            "the primitive cyclic aggregate stopped pairing to five")
    return {
        "edge_lattice_rank": 4,
        "summed_face_readout_kills_edges": True,
        "primitive_aggregate_pairing": 5,
        "characteristic_zero_normalization": "divide by 5",
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "physical six-term alternative is stable under exhaustive relative extension",
        "matrix_audit": audit_binary_matrices(),
        "cyclic_aggregate": audit_cyclic_aggregate(),
        "exact_alternative": (
            "for the complete physical relative map J0 and six-term anchor "
            "readout q, either q is nonzero on ker J0 and normalizes a "
            "protected-zero relative anchor, or q=lambda J0 and (-lambda,1) "
            "annihilates every complete augmented correction column"
        ),
        "proof_consequence": (
            "once J0 and q are physically defined on the canonical exhaustive "
            "relative complex, no enumeration of future relative generators "
            "is needed and no third comparison branch exists"
        ),
        "remaining_input": (
            "define the protected physical map and the six-term/pentagon "
            "readout in one common repeated grade; the theorem does not "
            "construct that chain-level typing"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"six-term relative alternative ledger changed: {digest}")
    print("h3 six-term exhaustive relative extension alternative: PASS")
    print(f"matrix_cases={ledger['matrix_audit']['binary_complete_maps']}")
    print("relative extensions: generator or physical separator, no third branch")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
