#!/usr/bin/env python3
"""Audit the marked lift from an optical frame circuit to a source kernel.

The anchored minimum-support theorem gives a marked circuit in the kernel of
the unsigned port-incidence map B.  The rectangular anchor--Cartan theorem
needs a marked vector in the kernel of the complete labelled source map M.
These are different maps.  This checker freezes the exact relative lifting
criterion and its row-space/pivot obstruction.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_anchored_min_support_frame_circuit_cover.py":
        "14bc527f3ff67dd41772409e9556b0241f8b6f49b7e7ecb2c83d05a8e09806aa",
    "computations/verify_frame_circuit_matching_lift_trichotomy.py":
        "e0bdd386a63b17b67038ef8e8d0faf15ff041a1e8cb9f6f138e6a781233d44f1",
    "computations/verify_uniform_cartan_critical_component_placement_gate.py":
        "68c56c1a9144dd92fa803962697de60b78b58a125191450f1af1abcd1befe2a1",
    "computations/verify_rectangular_interference_anchor_cartan_alternative.py":
        "b3d4db9e58f374bfd1f99a43931cac87fdab109c5d33c2f1c7d110e51e8f9a0a",
}
EXPECTED_LEDGER_SHA256 = "d1f2dcfb7b390a3d4476c71bb3dbbe2b68e2a60d154561e465ce3d8e6ebd5d27"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return (), ()
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    pivots = []
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def append_row(matrix, row):
    return tuple(tuple(map(Q, old)) for old in matrix) + (tuple(map(Q, row)),)


def append_column(matrix, column):
    return tuple(tuple(map(Q, row)) + (Q(value),)
                 for row, value in zip(matrix, column, strict=True))


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def dot(left, right):
    return sum(Q(a) * Q(b) for a, b in zip(left, right, strict=True))


def solve(matrix, rhs):
    """Return one solution to matrix*x=rhs, or None."""
    augmented = append_column(matrix, rhs)
    reduced, pivots = rref(augmented)
    variables = len(matrix[0]) if matrix else 0
    if variables in pivots:
        return None
    answer = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            answer[pivot] = reduced[row][-1]
    require(mat_vec(matrix, answer) == tuple(map(Q, rhs)),
            "RREF solution reconstruction failed")
    return tuple(answer)


def marked_lift_or_separator(matrix, candidate, marked_covector):
    """Correct a candidate lift without changing its marked readout.

    For d=M*x0 and q=h*x0 != 0, seek z with M*z=-d and h*z=0.  If this is
    impossible, return lambda with lambda^T*M=h.  The separator then reads
    lambda^T*d=q, proving that the defect cannot be removed relatively.
    """
    matrix = tuple(tuple(map(Q, row)) for row in matrix)
    candidate = tuple(map(Q, candidate))
    marked_covector = tuple(map(Q, marked_covector))
    marked_value = dot(marked_covector, candidate)
    require(marked_value, "candidate lift lost its marked coordinate")
    defect = mat_vec(matrix, candidate)
    stacked = append_row(matrix, marked_covector)

    # h is nonzero on ker(M) exactly when appending h raises row rank.
    if rank(stacked) == rank(matrix) + 1:
        target = (Q(0),) * len(matrix) + (marked_value,)
        lifted = solve(stacked, target)
        require(lifted is not None, "anchor-visible lift system failed")
        correction = tuple(a - b for a, b in
                           zip(lifted, candidate, strict=True))
        require(mat_vec(matrix, lifted) == (Q(0),) * len(matrix),
                "corrected vector is not in the complete source kernel")
        require(dot(marked_covector, lifted) == marked_value
                and dot(marked_covector, correction) == 0,
                "relative correction changed the marked coordinate")
        require(tuple(a + b for a, b in
                      zip(defect, mat_vec(matrix, correction), strict=True))
                == (Q(0),) * len(matrix),
                "relative correction did not kill the complete defect")
        return {
            "outcome": "marked_kernel_lift",
            "marked_value": str(marked_value),
            "defect": list(map(str, defect)),
            "lifted_kernel": list(map(str, lifted)),
            "relative_correction": list(map(str, correction)),
        }

    # h kills ker(M), hence h belongs to row(M).  This is the exact dual
    # obstruction.  When h is a literal coordinate covector, lambda^T M=h
    # is a source-row combination isolating that marked occurrence.
    separator = solve(transpose(matrix), marked_covector)
    require(separator is not None, "row-space separator reconstruction failed")
    require(tuple(sum(separator[row] * matrix[row][column]
                      for row in range(len(matrix)))
                  for column in range(len(matrix[0]))) == marked_covector,
            "separator does not reproduce the marked covector")
    require(dot(separator, defect) == marked_value,
            "separator did not detect the uncorrectable defect")
    return {
        "outcome": "marked_row_separator",
        "marked_value": str(marked_value),
        "defect": list(map(str, defect)),
        "separator": list(map(str, separator)),
        "separator_on_defect": str(dot(separator, defect)),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))

    # Two identical unsigned port columns are the parallel frame circuit.
    # Its primitive signed kernel has a nonzero first (marked) coordinate.
    port_map = ((1, 1),)
    frame_circuit = (1, -1)
    marked = (1, 0)
    require(mat_vec(port_map, frame_circuit) == (Q(0),)
            and dot(marked, frame_circuit) == 1,
            "parallel frame circuit changed")

    # Exact chain lift: the complete source map agrees with the port map on
    # this packet, so the frame vector already is the desired kernel vector.
    exact = marked_lift_or_separator(
        ((1, 1),), frame_circuit, marked)
    require(exact["outcome"] == "marked_kernel_lift"
            and exact["defect"] == ["0"],
            "exact chain lift changed")

    # Contamination need not be fatal.  Here the literal two-term candidate
    # has complete-source defect 2, but an unmarked-coordinate correction
    # kills it while preserving the first coordinate.
    corrected = marked_lift_or_separator(
        ((1, -1),), frame_circuit, marked)
    require(corrected["outcome"] == "marked_kernel_lift"
            and corrected["lifted_kernel"] == ["1", "1"]
            and corrected["relative_correction"] == ["0", "2"],
            "relative contamination correction changed")

    # Sharp counterguard: the same optical frame circuit need not survive in
    # the complete source kernel.  The first source column is a coloop of M;
    # every M-kernel vector has zero marked coordinate.  The dual row exactly
    # isolates the marked source occurrence.
    obstructed = marked_lift_or_separator(
        ((1, 0),), frame_circuit, marked)
    require(obstructed["outcome"] == "marked_row_separator"
            and obstructed["separator"] == ["1"]
            and obstructed["separator_on_defect"] == "1",
            "marked pivot obstruction changed")

    # Exhaust all small complete maps against every marked candidate.  This
    # verifies that relative correction and row-space separator are exact
    # complements, not merely examples.
    counts = {"marked_kernel_lift": 0, "marked_row_separator": 0}
    packets = 0
    for entries in product((-1, 0, 1), repeat=4):
        matrix = (entries[:2], entries[2:])
        for candidate in product((-1, 0, 1), repeat=2):
            for h in ((1, 0), (0, 1)):
                if not dot(h, candidate):
                    continue
                record = marked_lift_or_separator(matrix, candidate, h)
                counts[record["outcome"]] += 1
                packets += 1

    ledger = {
        "pins": PINS,
        "parallel_port_circuit": {
            "B": [[1, 1]],
            "c": [1, -1],
            "marked_covector": [1, 0],
        },
        "exact_chain_lift": exact,
        "corrected_contamination_lift": corrected,
        "sharp_complete_source_obstruction": obstructed,
        "small_complete_packets_checked": packets,
        "small_outcomes": counts,
        "theorem": (
            "let x0 be a candidate complete-source lift of a port circuit "
            "with q=h(x0) nonzero and defect d=Mx0.  Exactly one holds: "
            "there is z in ker(h) with Mz=-d, so x0+z lies in ker(M) and "
            "retains q; or h lies in row(M), with a dual lambda satisfying "
            "lambda^T M=h and lambda^T d=q"
        ),
        "source_consequence": (
            "the anchored frame-circuit cover alone does not supply the "
            "anchor-visible kernel required by the rectangular Cartan "
            "alternative, because its circuit lies in ker(B), not ker(M). "
            "A marked-coordinate-preserving chain lift or relative defect "
            "correction is the exact missing input"
        ),
        "typed_exit": (
            "when h is the literal coordinate covector of the marked "
            "occurrence, the obstruction lambda^T M=h is a protected "
            "source-row combination isolating that occurrence: a localized "
            "pivot/source-unit exit.  For a noncoordinate physical anchor "
            "h it is only a Fredholm separator until its readout is landed"
        ),
        "prior_typed_exits": (
            "before this gate, failure of a common matching tail is the "
            "Tutte/Hall exit, while repeated physical degree is the "
            "principal-parts/Cartan-Spencer collision face"
        ),
        "minimal_positive_interface": (
            "construct Lambda on the common-tail frame circuit with "
            "h Lambda(c)=c_marked, and either prove M Lambda(c)=0 or provide "
            "a correction K(c) with M K(c)=M Lambda(c) and h K(c)=0.  Then "
            "(Lambda-K)c is the complete marked kernel vector; no square, "
            "corank-one, zero-holonomy component cover is needed"
        ),
        "scope": (
            "the checker proves the exact linear lift/separator alternative. "
            "It does not construct Lambda or K in the physical labelled "
            "source resolution, nor land a noncoordinate separator"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("source-kernel lift ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("frame-circuit complete-source kernel lift gate: PASS")
    print("small packets:", ledger["small_complete_packets_checked"])
    print("outcomes:", ledger["small_outcomes"])
    print("sharp obstruction:",
          ledger["sharp_complete_source_obstruction"]["outcome"])
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
