#!/usr/bin/env python3
"""Boundary of the tempting reduced-Eq/cap factorization.

The standard two-tail transport is graph-locked: in endpoint-odd
coordinates its main boundary D and ordinary residue R agree.  This checker
shows that the missing residue-only vector factors through the projected
pure-row/target-cap/residue-cap block if a unit reduced-Eq face is supplied.
It then proves why this does not lift to a literal source chain: the pure
row has private matching-boundary pivots which the projected cap and reduced
Eq signatures do not see.

For one oriented tail corner use rows

    (pure_Eq, ainc, W, target, ores).

The existing columns and the missing reduced face are

    r0  = ( 1,-1, 0,1,0),
    T   = ( 0, 0,-1,1,0),
    rho = ( 0, 0, 1,0,1),
    C   = (-1, 0, 0,0,0).

Then K=-r0+T+rho-C=(0,1,0,0,1).  Taking the four endpoint/tail
coefficients alpha=(-1,1,1,-1) (the required -delta) cancels ainc and
leaves precisely the residue-only KS correction.  Conversely the
coefficients of C are forced blockwise, so this construction is equivalent
to the endpoint-odd reduced-Eq aggregate modulo the old cap block.

Thus the calculation is a useful quotient identity but not a source-type
merger.  Any positive cell must cancel the private full-nine boundary as
well as carry the eta/sigma terminal comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "ed2be2dd157747104cf454b0062a6818689aa0562cc6484171e0f90aa52b9b88"
PINS = {
    "computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py":
        "eede8aabd5c4740520ed13f1aacc897326a3a02573f860f5b2613c9df91fd53c",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_residual_q_eta_one_cell_fiber_product_gate.py":
        "4e84ad031b97ee67e1336c9a9d785acd3c581c2d80aeeb005d4eee784f91eccb",
    "computations/verify_h3_residual_q_physical_duality_interface_counterguard.py":
        "6f7fa68eb081a1dd3c3754cff5e1974e54c4df81c8ce6d36ffe8d37efba953ba",
    "computations/verify_h3_residual_q_ks_constructive_landing_boundary.py":
        "bc11c8fe61ec8c21a1850326de037a328ab7f7404bcf3902655f6541e496bc9f",
}

ROWS = ("pure_Eq", "ainc", "W", "target", "ores")
R0 = (1, -1, 0, 1, 0)
T = (0, 0, -1, 1, 0)
RHO = (0, 0, 1, 0, 1)
REDUCED_EQ = (-1, 0, 0, 0, 0)
K = (0, 1, 0, 0, 1)

# Add one literal private matching-boundary pivot owned by r0.  The complete
# full-nine audit supplies at least 42 such pivots per relevant column; one
# is enough to refute lifting the projected identity.
R0_LITERAL = R0 + (1,)
T_LITERAL = T + (0,)
RHO_LITERAL = RHO + (0,)
REDUCED_EQ_PROJECTED = REDUCED_EQ + (0,)
K_LITERAL = K + (0,)

CORNER_ORDER = ("P+q00", "P-q00", "P+q11", "P-q11")
ALPHA = (-1, 1, 1, -1)  # required -delta


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def add(*vectors):
    return tuple(sum(Q(vector[i]) for vector in vectors)
                 for i in range(len(vectors[0])))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def dot(left, right):
    return sum(Q(a) * Q(b) for a, b in zip(left, right, strict=True))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def solve(columns, target):
    """Return the unique rational coefficients when columns have full rank."""
    height = len(target)
    width = len(columns)
    augmented = [[Q(columns[col][row]) for col in range(width)] + [Q(target[row])]
                 for row in range(height)]
    pivot_row = 0
    pivots = []
    for column in range(width):
        pivot = next((row for row in range(pivot_row, height)
                      if augmented[row][column]), None)
        if pivot is None:
            continue
        augmented[pivot_row], augmented[pivot] = augmented[pivot], augmented[pivot_row]
        value = augmented[pivot_row][column]
        augmented[pivot_row] = [entry / value for entry in augmented[pivot_row]]
        for row in range(height):
            if row == pivot_row or not augmented[row][column]:
                continue
            value = augmented[row][column]
            augmented[row] = [left - value * right for left, right in
                              zip(augmented[row], augmented[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    require(all(any(row[col] for col in range(width)) or not row[-1]
                for row in augmented), "inconsistent linear system")
    require(len(pivots) == width, "solution is not unique")
    answer = [Q(0)] * width
    for row, column in enumerate(pivots):
        answer[column] = augmented[row][-1]
    require(add(*(scale(answer[i], columns[i]) for i in range(width)))
            == tuple(map(Q, target)), "solution reconstruction failed")
    return tuple(answer)


def one_corner_factorization() -> dict[str, object]:
    old = (R0, T, RHO)
    full = old + (REDUCED_EQ,)
    phi = (1, 1, 0, 0, 0)  # pure Eq + physical anchor incidence
    require(all(dot(phi, column) == 0 for column in old),
            "the reduced-Eq separator stopped killing the old cap block")
    require(dot(phi, REDUCED_EQ) == -1 and dot(phi, K) == 1,
            "the primitive reduced-Eq pairing changed")
    require(rank(old) == 3 and rank(full) == 4,
            "one-corner cap ranks changed")
    coefficients = solve(full, K)
    require(coefficients == tuple(map(Q, (-1, 1, 1, -1))),
            ("cap factorization changed", coefficients))
    require(add(scale(-1, R0), T, RHO, scale(-1, REDUCED_EQ)) == K,
            "displayed cap factorization failed")
    return {
        "row_order": list(ROWS),
        "old_columns": {"r0": list(R0), "T": list(T), "rho": list(RHO)},
        "reduced_Eq_face_C": list(REDUCED_EQ),
        "residue_anchor_cell_K": list(K),
        "unique_coefficients_r0_T_rho_C": [str(value) for value in coefficients],
        "identity": "K=-r0+T+rho-C=(0,1,0,0,1)",
        "primitive_separator": "pure_Eq+ainc",
        "old_rank_full_rank": [rank(old), rank(full)],
    }


def four_corner_factorization() -> dict[str, object]:
    require(sum(ALPHA) == 0, "endpoint-odd coefficients stopped summing to zero")
    blocks = [scale(coefficient, K) for coefficient in ALPHA]
    aggregate = add(*blocks)
    require(aggregate == (0, 0, 0, 0, 0),
            "coarse aggregate should cancel after forgetting tail labels")

    # Retain the four separate ordinary-residue coordinates.  The strict
    # readouts are common, so only ainc is summed while residue remains
    # corner-labelled.
    labelled = {
        "pure_Eq": sum(ALPHA[i] * K[0] for i in range(4)),
        "ainc": sum(ALPHA[i] * K[1] for i in range(4)),
        "W": sum(ALPHA[i] * K[2] for i in range(4)),
        "target": sum(ALPHA[i] * K[3] for i in range(4)),
        "residue_corners": list(ALPHA),
    }
    require(labelled == {
        "pure_Eq": 0, "ainc": 0, "W": 0, "target": 0,
        "residue_corners": [-1, 1, 1, -1],
    }, "four-corner KS aggregate changed")

    # Since the one-corner solution is unique, the coefficient on C in
    # corner j is -alpha_j.  Thus, modulo the old cap columns, the desired
    # KS class is exactly the endpoint-odd reduced-Eq aggregate.
    forced_c = tuple(-value for value in ALPHA)
    require(forced_c == (1, -1, -1, 1),
            "forced reduced-Eq coefficients changed")
    return {
        "corner_order": list(CORNER_ORDER),
        "required_minus_delta": list(ALPHA),
        "strict_aggregate_readouts": labelled,
        "forced_reduced_Eq_coefficients": list(forced_c),
        "reduced_Eq_aggregate": (
            "C_(P+q00)-C_(P-q00)-C_(P+q11)+C_(P-q11)"
        ),
        "equivalence_mod_old_cap": (
            "residual-q KS correction exists iff the displayed endpoint-odd "
            "reduced-Eq aggregate exists in the same labelled repeated grade"
        ),
    }


def literal_private_pivot_counterguard() -> dict[str, object]:
    columns = (R0_LITERAL, T_LITERAL, RHO_LITERAL, REDUCED_EQ_PROJECTED)
    require(rank(columns) == 4 and rank(columns + (K_LITERAL,)) == 5,
            "the literal private pivot stopped obstructing the cap lift")
    # Row order is old five rows plus one literal private boundary feature.
    separator = (0, 1, 0, 0, 0, 1)  # ainc + private
    require(all(dot(separator, column) == 0 for column in columns),
            "the private-pivot separator stopped killing the projected lift")
    require(dot(separator, K_LITERAL) == 1,
            "the private-pivot separator stopped detecting K")

    # Four copies have distinct private pivots because literal injectivity
    # makes the matching monomial owned by its own row/multiplier column.
    private_residual = tuple(-coefficient for coefficient in ALPHA)
    require(private_residual == (1, -1, -1, 1)
            and any(private_residual),
            "the four-corner private residual unexpectedly vanished")
    return {
        "literal_row_order": list(ROWS) + ["one_r0_private_boundary_pivot"],
        "r0_literal": list(R0_LITERAL),
        "projected_T_rho_C": [list(T_LITERAL), list(RHO_LITERAL),
                                list(REDUCED_EQ_PROJECTED)],
        "desired_K_literal": list(K_LITERAL),
        "old_plus_projected_C_rank": rank(columns),
        "rank_after_K": rank(columns + (K_LITERAL,)),
        "primitive_separator": "ainc+private",
        "separator_vector": list(separator),
        "four_corner_distinct_private_residual": list(private_residual),
        "structural_input": (
            "the pinned complete full-nine repeated-degree module is "
            "injective and gives at least 42 private boundary features per "
            "column, so the added private row is not a fabricated source type"
        ),
        "verdict": (
            "the normalized five-row factorization does not lift unless the "
            "new reduced-Eq/relative cell also carries the negative of every "
            "private full-nine boundary feature of r0"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    ledger = {
        "theorem": "residual-q reduced-Eq/cap factorization boundary",
        "one_corner": one_corner_factorization(),
        "four_corner": four_corner_factorization(),
        "literal_private_pivot_counterguard": literal_private_pivot_counterguard(),
        "fine_grade_guard": (
            "each r0,T,rho,C quartet must be multiplied by the same literal "
            "endpoint orientation, tail corner, complementary matching, and "
            "incident-cycle factor in the labelled repeated P3+K2 grade; no "
            "t-u scalar multiplication or cross-word relabelling is used"
        ),
        "remaining_physical_terminal_conditions": {
            "eta_z": "dr_v(eta_z)=-dOmega_v(eta_z)=1+delta_vz*u_z/t",
            "eta_aggregate": "5+u_z/t",
            "sigma": "-q_pq^22 facewise",
            "strict_D_W_target_ainc": [0, 0, 0, 0],
        },
        "consequence": (
            "the cap quotient has the advertised -delta factorization, but "
            "literal private matching-boundary pivots prevent reversing that "
            "quotient.  A positive relative cell must simultaneously cancel "
            "the complete r0 boundary, realize the reduced Eq face, and carry "
            "the eta/sigma terminal comparison"
        ),
        "scope": (
            "exact normalized quotient identity plus a literal private-pivot "
            "counterguard; it constructs neither the physical reduced-Eq "
            "face nor its terminal comparison and does not imply transverse "
            "four-good rank"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h3 residual-q reduced-Eq/cap factorization: QUOTIENT ONLY")
    print("one corner: K=-r0+T+rho-C=(0,1,0,0,1)")
    print("four corners: anchor cancels, residue=-delta")
    print("literal lift: blocked by private full-nine boundary pivot")
    print("remaining datum: relative cell cancelling private boundary + eta/sigma")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
