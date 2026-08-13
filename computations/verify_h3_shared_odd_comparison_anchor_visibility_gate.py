#!/usr/bin/env python3
"""Separate automatic odd-packet closure from physical anchor visibility.

Once a source-valid protected odd comparison Phi exists, the physical
q=M-a quotient alternative has no packet-mismatch branch: a nonzero defect
is a protected-kernel witness, while a zero defect is corrected by protected
rows.  The remaining constructive condition is independent.  On the
corank-one target-circuit block A_D with circuit k it is

                         h_phys(k) != 0.

The smallest comparison theorem which forces this is transport of the
physical anchor row modulo protected rows, together with noncollapse of the
marked circuit.  Exact q transport alone does not imply either hypothesis.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_fan_coloop_packet_q_comparison_defect.py":
        "86db5c89196a183c5ddc2b1c2198029fa45ea1cdff1f7d239a74870cd4957e94",
    "computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py":
        "c652f10a8bac32f11f4c090a55687cf672ce3f96629384f0fbde9f08f440a1bd",
    "computations/verify_target_augmented_affine_circuit_cartan_guard.py":
        "7c72b58101cc77a0ca3e3c688b5de0742b4f118777f450f235d578691954d08f",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
}
EXPECTED_LEDGER_SHA256 = (
    "f74bfd6e0657ab983048d3c04f063b25109aafb9f9de97b417e6a5601eb6e0d9"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def mat_vec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def row_mat(vector, matrix):
    return tuple(dot(vector, column)
                 for column in zip(*matrix, strict=True))


def subtract(left, right):
    return tuple(Q(a) - Q(b) for a, b in zip(left, right, strict=True))


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


def in_row_space(row, matrix):
    return rank(tuple(matrix) + (tuple(map(Q, row)),)) == rank(matrix)


def audit_packet_alternative_is_exhaustive():
    protected = ((Q(1), Q(0), Q(0)),)
    comparison = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    )
    kernel_witness = (Q(0), Q(1), Q(0))

    # Nonzero quotient defect: already a positive q/typed-exit arm.
    q_source = (Q(0), Q(1), Q(0))
    q_canonical = (Q(0), Q(0), Q(0))
    visible_defect = subtract(q_source, row_mat(q_canonical, comparison))
    require(mat_vec(protected, kernel_witness) == (Q(0),)
            and dot(visible_defect, kernel_witness) == 1
            and not in_row_space(visible_defect, protected),
            "the nonzero packet-defect arm changed")

    # Zero quotient defect modulo protected rows: the odd row is corrected
    # and the S/D split proceeds.  Literal equality is not required.
    q_source = (Q(2), Q(1), Q(-1))
    q_canonical = (Q(0), Q(1), Q(-1))
    correctable_defect = subtract(
        q_source, row_mat(q_canonical, comparison))
    require(correctable_defect == (Q(2), Q(0), Q(0))
            and in_row_space(correctable_defect, protected),
            "the protected-row packet correction changed")
    return {
        "nonzero_class": "protected-kernel q witness / typed exit",
        "zero_class": "protected-row correction, then physical S/D split",
        "third_packet_branch": False,
    }


def audit_minimal_anchor_transport_theorem():
    # This is the actual first-row scalar pivot from e6b390a completed to
    # its corank-one target-circuit block.
    protected = (
        (Q(4), Q(-2), Q(-1)),
        (Q(3), Q(-2), Q(0)),
    )
    circuit = (Q(2), Q(3), Q(2))
    comparison = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    )
    canonical_anchor = (Q(0), Q(0), Q(1))
    correction_coefficients = (Q(2), Q(-1))
    correction = row_mat(correction_coefficients, protected)
    physical_anchor = tuple(left + right for left, right in
                            zip(canonical_anchor, correction, strict=True))

    require(rank(protected) == 2
            and mat_vec(protected, circuit) == (Q(0), Q(0)),
            "the corank-one target circuit changed")
    anchor_defect = subtract(
        physical_anchor, row_mat(canonical_anchor, comparison))
    require(anchor_defect == correction
            and in_row_space(anchor_defect, protected)
            and dot(physical_anchor, circuit)
            == dot(canonical_anchor, circuit) == 2,
            "anchor transport stopped preserving circuit visibility")

    # On a one-dimensional kernel the converse is exact after scaling:
    # any two nonzero functionals agree modulo row(A_D) after normalization.
    differently_scaled_anchor = tuple(
        3 * value + correction[index]
        for index, value in enumerate(canonical_anchor)
    )
    normalized = tuple(value / 3 for value in differently_scaled_anchor)
    normalized_defect = subtract(normalized, canonical_anchor)
    require(dot(differently_scaled_anchor, circuit) == 6
            and in_row_space(normalized_defect, protected),
            "the normalized corank-one converse changed")
    return {
        "target_circuit": [str(value) for value in circuit],
        "canonical_anchor_on_image_circuit": "2",
        "anchor_transport": "h_phys-h0*Phi=lambda*A_D",
        "physical_anchor_on_circuit": "2",
        "corank_one_converse": (
            "if h_phys(k) and h0(Phi k) are nonzero, rescale h_phys; "
            "then h_phys-h0*Phi lies in row(A_D)"
        ),
        "load_bearing_extra_hypothesis": "h0(Phi k)!=0",
    }


def audit_q_transport_does_not_imply_anchor_law():
    protected = (
        (Q(4), Q(-2), Q(-1)),
        (Q(3), Q(-2), Q(0)),
    )
    circuit = (Q(2), Q(3), Q(2))
    comparison = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    )
    q_source = (Q(0), Q(1), Q(0))
    q_canonical = q_source
    q_defect = subtract(q_source, row_mat(q_canonical, comparison))
    canonical_anchor = (Q(0), Q(0), Q(1))
    physical_dark = protected[0]
    anchor_defect = subtract(
        physical_dark, row_mat(canonical_anchor, comparison))
    require(in_row_space(q_defect, protected)
            and dot(canonical_anchor, circuit) == 2
            and dot(physical_dark, circuit) == 0
            and not in_row_space(anchor_defect, protected),
            "the exact q/anchor independence counterguard changed")

    # Even exact anchor transport is useless if Phi collapses the marked
    # kernel line.  This smaller guard freezes the noncollapse hypothesis.
    small_protected = ((Q(1), Q(0)),)
    collapsing_comparison = (
        (Q(1), Q(0)),
        (Q(0), Q(0)),
    )
    small_circuit = (Q(0), Q(1))
    small_canonical_anchor = (Q(0), Q(1))
    pulled_anchor = row_mat(small_canonical_anchor, collapsing_comparison)
    require(mat_vec(small_protected, small_circuit) == (Q(0),)
            and mat_vec(collapsing_comparison, small_circuit)
            == (Q(0), Q(0))
            and not any(pulled_anchor),
            "the marked-circuit collapse guard changed")
    return {
        "same_protected_Phi_and_exact_q_transport": True,
        "canonical_anchor_on_circuit": "2",
        "physical_anchor_on_circuit": "0",
        "consequence": (
            "the shared odd Phi and q quotient theorem do not imply the "
            "physical anchor row law"
        ),
        "second_guard": (
            "anchor-row transport alone does not help if Phi kills the "
            "marked circuit; target/marked-coordinate noncollapse is required"
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "shared odd comparison closes packet mismatch but not anchor visibility",
        "pins": PINS,
        "packet_alternative": audit_packet_alternative_is_exhaustive(),
        "minimal_anchor_transport": audit_minimal_anchor_transport_theorem(),
        "sharp_counterguards": audit_q_transport_does_not_imply_anchor_law(),
        "exact_remaining_source_statement": (
            "on the minimum target circuit k, construct the physical anchor "
            "row comparison h_phys-mu*h0*Phi=lambda*A_D with mu nonzero "
            "and prove h0(Phi*k) nonzero.  On the corank-one circuit block "
            "this is equivalent, after normalization, to h_phys(k) nonzero"
        ),
        "scope": (
            "exact linear-algebra composition and sharp formal counterguards. "
            "It begins after a complete physical odd Phi and q=M-a typing; "
            "it neither constructs Phi nor promotes the dark anchor guard "
            "to a full Krenn source packet"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"shared odd comparison/anchor ledger changed: {digest}")
    print("h3 shared odd comparison: PACKET CLOSED, ANCHOR SEPARATE")
    print("packet defect: q witness/typed exit or protected correction")
    print("remaining law: anchor transport plus marked-circuit noncollapse")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
