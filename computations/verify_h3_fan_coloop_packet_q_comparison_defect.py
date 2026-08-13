#!/usr/bin/env python3
"""Classify fan-coloop odd-packet disagreement as a physical q defect.

Let J,L and J0,L0 be complete protected maps and Phi a physical protected
comparison with J0*Phi=A*J.  On the fan and canonical odd packets write

    q=M-a,       q0=M0-a0,

where M is the complete weighted matching aggregate and a is physical
anchor incidence.  The odd-Cartan packet disagreement is

    o=[(M-M0 Phi)-(a-a0 Phi)] = [q-q0 Phi]

in L*/row(J).  It vanishes exactly when the two q rows agree on ker(J),
equivalently when the comparison extends to the augmented q maps.  If it
does not vanish, a protected-kernel witness has nonzero physical q on the
fan side or on its canonical image, giving the relative generator whenever
the q rows are terminals, and otherwise a literal typed packet exit.

This is the same quotient theorem as the protected physical-q comparison.
It is independent of the constructive anchor row h_phys: q transport does
not imply h_phys-e_tau lies in row(J) on a target circuit.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_fan_coloop_cartan_circuit_comparison_gate.py":
        "c652f10a8bac32f11f4c090a55687cf672ce3f96629384f0fbde9f08f440a1bd",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
    "computations/verify_protected_physical_comparison_first_source_cell.py":
        "0c93a7e67f1f48d114e343a282820477fe5a86649502500c5b00ee5e560b0245",
    "computations/verify_target_augmented_affine_circuit_cartan_guard.py":
        "7c72b58101cc77a0ca3e3c688b5de0742b4f118777f450f235d578691954d08f",
}
EXPECTED_LEDGER_SHA256 = (
    "f32c1f0c3fed7034c93e73fa078c520d14d5e28676551972869bd2202b0aae41"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def dot(left, right):
    return sum(Q(a) * Q(b) for a, b in zip(left, right, strict=True))


def mat_vec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def row_mat(vector, matrix):
    columns = tuple(zip(*matrix, strict=True))
    return tuple(dot(vector, column) for column in columns)


def mat_mul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(dot(row, column) for column in columns)
                 for row in left)


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


def subtract(left, right):
    return tuple(Q(a) - Q(b) for a, b in zip(left, right, strict=True))


def add(left, right):
    return tuple(Q(a) + Q(b) for a, b in zip(left, right, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def audit_defect_class_alternative():
    protected = ((Q(1), Q(0), Q(0)),)
    canonical = protected
    comparison = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    )
    codomain = ((Q(1),),)
    require(mat_mul(canonical, comparison)
            == mat_mul(codomain, protected),
            "the protected comparison square stopped commuting")
    kernel_witnesses = ((Q(0), Q(1), Q(0)),
                        (Q(0), Q(0), Q(1)))
    require(all(mat_vec(protected, witness) == (Q(0),)
                for witness in kernel_witnesses),
            "the protected kernel basis changed")

    # Fan-side visible mismatch.  Matching transports but anchor does not.
    source_matching = (Q(0), Q(1), Q(0))
    source_anchor = (Q(0), Q(0), Q(0))
    canonical_matching = (Q(0), Q(0), Q(0))
    canonical_anchor = (Q(0), Q(0), Q(0))
    q_source = subtract(source_matching, source_anchor)
    q_canonical = subtract(canonical_matching, canonical_anchor)
    q_canonical_pullback = row_mat(q_canonical, comparison)
    source_defect = subtract(q_source, q_canonical_pullback)
    source_witness = kernel_witnesses[0]
    require(dot(source_defect, source_witness) == 1
            and dot(q_source, source_witness) == 1
            and dot(q_canonical_pullback, source_witness) == 0
            and not in_row_space(source_defect, protected),
            "the fan-side q-visible defect changed")

    # Canonical-side visible mismatch.
    q_source = (Q(0), Q(0), Q(0))
    q_canonical = (Q(0), Q(0), Q(1))
    q_canonical_pullback = row_mat(q_canonical, comparison)
    canonical_defect = subtract(q_source, q_canonical_pullback)
    canonical_witness = kernel_witnesses[1]
    require(dot(canonical_defect, canonical_witness) == -1
            and dot(q_source, canonical_witness) == 0
            and dot(q_canonical_pullback, canonical_witness) == 1
            and not in_row_space(canonical_defect, protected),
            "the canonical-side q-visible defect changed")

    # The genuinely weaker success: neither M nor a transports separately,
    # but their defects agree and cancel in q.
    source_matching = (Q(0), Q(1), Q(0))
    source_anchor = (Q(0), Q(1), Q(0))
    canonical_matching = (Q(0), Q(0), Q(0))
    canonical_anchor = (Q(0), Q(0), Q(0))
    matching_defect = subtract(
        source_matching, row_mat(canonical_matching, comparison))
    anchor_defect = subtract(
        source_anchor, row_mat(canonical_anchor, comparison))
    transported_defect = subtract(matching_defect, anchor_defect)
    require(matching_defect == anchor_defect != (Q(0), Q(0), Q(0))
            and not in_row_space(matching_defect, protected)
            and transported_defect == (Q(0), Q(0), Q(0)),
            "the equal nonzero constituent-defect success changed")

    # General row-space success: q-q0 Phi=lambda J.  The augmented lower
    # row [-lambda,1] makes q transport along the protected comparison.
    q_source = (Q(2), Q(1), Q(-1))
    q_canonical = (Q(0), Q(1), Q(-1))
    q_canonical_pullback = row_mat(q_canonical, comparison)
    row_defect = subtract(q_source, q_canonical_pullback)
    lam = (Q(2),)
    require(row_defect == row_mat(lam, protected)
            and in_row_space(row_defect, protected),
            "the q row-space transport class changed")
    augmented_source = protected + (q_source,)
    # q0*Phi = q-lambda*J is the lower row of the usual block comparison.
    require(q_canonical_pullback
            == subtract(q_source, row_mat(lam, protected)),
            "the augmented q comparison identity changed")

    return {
        "protected_map": [[str(value) for value in row]
                          for row in protected],
        "fan_visible_defect": {
            "witness": [str(value) for value in source_witness],
            "q_fan": "1", "q_canonical_image": "0",
        },
        "canonical_visible_defect": {
            "witness": [str(value) for value in canonical_witness],
            "q_fan": "0", "q_canonical_image": "1",
        },
        "equal_nonzero_constituent_defects": {
            "delta_M": [str(value) for value in matching_defect],
            "delta_anchor": [str(value) for value in anchor_defect],
            "q_defect": [0, 0, 0],
        },
        "row_space_success": {
            "q_fan_minus_q0_Phi": [str(value) for value in row_defect],
            "lambda": [str(value) for value in lam],
            "identity": "q0*Phi=q-lambda*J",
        },
        "exact_alternative": (
            "[q-q0 Phi] nonzero gives x in ker(J) on which q(x) or "
            "q0(Phi x) is nonzero; zero class is equivalent to an augmented "
            "physical q comparison"
        ),
    }


def audit_oriented_split_after_transport():
    # Physical signless row S and actual odd Cartan D.  If D differs from
    # the desired odd packet D0 by lambda J, correct it with protected rows
    # before taking E_plus/minus.
    protected = ((Q(1), Q(0), Q(0), Q(0), Q(0)),)
    alpha, diagonal = Q(2), Q(3)
    signless = (alpha, alpha, -diagonal, -diagonal, -alpha)
    desired_odd = (alpha, -alpha, -diagonal, diagonal, Q(0))
    lam = Q(5)
    actual_odd = add(desired_odd, scale(lam, protected[0]))
    defect = subtract(actual_odd, desired_odd)
    require(in_row_space(defect, protected),
            "the corrected odd packet stopped transporting")
    corrected = subtract(actual_odd, scale(lam, protected[0]))
    plus = scale(Q(1, 2), add(signless, corrected))
    minus = scale(Q(1, 2), subtract(signless, corrected))
    require(plus == (alpha, 0, -diagonal, 0, -alpha / 2)
            and minus == (0, alpha, 0, -diagonal, -alpha / 2),
            "the q-transported S/D split changed")
    return {
        "packet_defect": [str(value) for value in defect],
        "protected_row_correction": "D0=D-lambda*J",
        "E_plus": [str(value) for value in plus],
        "E_minus": [str(value) for value in minus],
        "consequence": (
            "literal packet equality is stronger than necessary; equality "
            "of q classes modulo protected rows suffices for the oriented "
            "target-bearing split"
        ),
    }


def audit_anchor_independence():
    protected = ((Q(1), Q(0), Q(0)),)
    q_fan = (Q(0), Q(1), Q(0))
    q_canonical = q_fan
    q_defect = subtract(q_fan, q_canonical)
    anchor_fan = (Q(0), Q(0), Q(1))
    anchor_canonical = (Q(0), Q(0), Q(0))
    anchor_defect = subtract(anchor_fan, anchor_canonical)
    circuit = (Q(0), Q(0), Q(1))
    require(in_row_space(q_defect, protected)
            and not in_row_space(anchor_defect, protected)
            and mat_vec(protected, circuit) == (Q(0),)
            and dot(anchor_defect, circuit) == 1,
            "the q-transport/anchor-law independence guard changed")
    return {
        "q_comparison_defect": [0, 0, 0],
        "anchor_comparison_defect": [str(value) for value in anchor_defect],
        "target_circuit": [str(value) for value in circuit],
        "anchor_defect_on_circuit": "1",
        "consequence": (
            "q packet transport and the physical h_phys/e_tau circuit "
            "congruence are logically independent"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "q_defect_class_alternative": audit_defect_class_alternative(),
        "oriented_split_after_q_transport":
            audit_oriented_split_after_transport(),
        "physical_anchor_independence": audit_anchor_independence(),
        "fan_coloop_packet_theorem": (
            "for a source-valid protected odd-Cartan comparison Phi, the "
            "complete packet disagreement is the physical quotient class "
            "o=[(M-M0 Phi)-(a-a0 Phi)]=[q-q0 Phi].  If o is nonzero, "
            "row-space duality gives a protected-kernel witness and one of "
            "the two physical q readouts is nonzero: normalize it when q is "
            "the relative terminal, or route the corresponding saturated "
            "matching packet as a typed exit.  If o vanishes, correct the "
            "odd Cartan row by protected rows; then the physical signless "
            "pivot S splits into the two oriented target-bearing rows"
        ),
        "sharp_remaining_gate": (
            "construct the complete physical Phi in the fan-coloop fine "
            "grade and identify its weighted matching aggregate M and "
            "physical anchor incidence a.  Once this is done, packet "
            "disagreement has no third branch.  The constructive h_phys "
            "visibility on the resulting target circuit remains a separate "
            "anchor law"
        ),
        "scope": (
            "exact protected-row quotient theorem with literal linear "
            "witnesses.  It is conditional on physical q=M-a typing of both "
            "packet readouts and does not construct Phi or the anchor law"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"fan-coloop packet q-defect ledger changed: {digest}")
    print("h3 fan-coloop packet q comparison: EXACT QUOTIENT ALTERNATIVE")
    print("nonzero class -> physical q witness / typed exit or generator")
    print("zero class -> protected correction and oriented S/D split")
    print("remaining independent law: h_phys visibility on target circuit")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
