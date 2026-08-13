#!/usr/bin/env python3
"""Compare the h=2 endpoint-even B-4 lift with the h=3 C_plus gate.

The six unordered endpoint holes of a four-site order-two packet form the
octahedral module.  Label them so the physical involution acts as

    (B0 B5)(B2 B3), fixing B1,B4.

For c_i^+=6 B_i-H0, the integral tau-plus debt is exactly

    D6=(-1,2,-1,-1,2,-1)=(c_1^+ + c_4^+)/2,
    delta_plus=D6/4=(c_1^+ + c_4^+)/8.

Thus the lower coefficient projection of the missing root-even C_plus orbit
is one normalized B-4 endpoint-even class.  This does not identify the
physical cells: B-4 acts on twelve occurrence coordinates in words 0112 and
0121, while B0,...,B5 are complete P3+K2 output columns.  The source-labelled
restriction/reinsertion map between those modules remains missing.

The target comparison is sharp.  Literal diagonal target rows occupy only
the three monochromatic coordinates and cannot cancel the two mixed
coordinates of 2(w-1)Delta.  A correction internal to the two Cartan orbit
columns makes the signless vector odd.  Hence the minimum noncollapsing
extension is the independently target-bearing, rho-even C_plus cell.  Its
next boundary is R_plus=(1+rho)H_w d(P*), and the known formal Hasse filler
retains the forced reduced-Eq correction recorded by the full tau-plus
interface theorem.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "computations/verify_h2_lower_centered_orientation_terminal_fork.py":
        "6758c86ec151834d121e5b41b1dae677592cc4224c3aaad95d6f8321b826d3b2",
    "notes/h2-lower-centered-orientation-terminal-fork.md":
        "daa6d20d510be6472d9b1946a4854d6fd3322b61288f3fb77a8103b8a8b7d051",
    "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py":
        "c0a34736979eb8a5d059dce30224b3d22f3930e9afaf07916dbbf51b3539c15d",
    "computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py":
        "9679c047e440f48899f1385682bcf64b725e049da01a42b8134b40c3fda73177",
    "notes/h3-signless-cartan-adjacent-power-shared-cell-gate.md":
        "6f1b0e239ecc13e3577ed7f0cee051ab0e092ebfed5eb25240476ec613a271a1",
    "computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py":
        "ef63bd26210802cf300e263da44e178b4dd19abbf0fa5bba059b5d61afb9b782",
    "notes/h3-generic-cartan-adjacent-target-label-prolongation.md":
        "acbeaf6c50910244742ab00017b760bbaafd1f4ec6dccc8adb2ed8cefef7f8f3",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "notes/h3-tau-plus-full-interface-product-bianchi-extension-gate.md":
        "38c3fc7f9191dcc7ae16f368b5b861dd48f7e2cb0ad599bcb03f7ab26af40366",
}
EXPECTED_LEDGER_SHA256 = "0173b3e8fbb5fc377b71d6f024f28cd6bccfe5a732e8eeac7272804b49a20d7e"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors, "empty vector sum")
    return tuple(sum((vector[index] for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient: int | Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * value for value in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def unit(index: int, size: int) -> tuple[Q, ...]:
    answer = [Q(0)] * size
    answer[index] = Q(1)
    return tuple(answer)


def rank(vectors: tuple[tuple[Q, ...], ...] | list[tuple[Q, ...]]) -> int:
    basis: dict[int, tuple[Q, ...]] = {}
    for original in vectors:
        values = tuple(map(Q, original))
        for pivot in sorted(basis):
            if values[pivot]:
                values = add(values, scale(-values[pivot], basis[pivot]))
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        basis[pivot] = scale(1 / values[pivot], values)
    return len(basis)


def tensor(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(a * b for a in left for b in right)


def mat_vec(matrix: tuple[tuple[Q, ...], ...],
            vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(dot(row, vector) for row in matrix)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def even_hole_and_tau_debt_audit() -> dict[str, object]:
    # K4 edge/hole labels chosen so rho_sites=(0 1) induces exactly the
    # physical target action (B0 B5)(B2 B3), fixing B1,B4.
    holes = (
        (0, 2),  # B0
        (0, 1),  # B1
        (0, 3),  # B2
        (1, 3),  # B3
        (2, 3),  # B4
        (1, 2),  # B5
    )
    lookup = {hole: index for index, hole in enumerate(holes)}
    rho_site = (1, 0, 2, 3)

    def move_hole(hole: tuple[int, int]) -> tuple[int, int]:
        return tuple(sorted((rho_site[hole[0]], rho_site[hole[1]])))

    rho_b = tuple(lookup[move_hole(hole)] for hole in holes)
    require(rho_b == (5, 1, 3, 2, 4, 0),
            ("the B-label involution changed", rho_b))

    # Endpoint adjacency on the unordered-hole module joins two K4 edges
    # exactly when they share one endpoint.  Complementary holes are the
    # three nonedges of this octahedral graph.
    adjacency = tuple(tuple(
        Q(int(index != other and len(set(hole) & set(holes[other])) == 1))
        for other in range(6)) for index, hole in enumerate(holes))
    require(all(sum(row) == 4 for row in adjacency),
            "the even endpoint adjacency stopped having degree four")
    identity = tuple(tuple(Q(int(row == column)) for column in range(6))
                     for row in range(6))
    ones = (Q(1),) * 6
    require(mat_vec(adjacency, ones) == scale(4, ones),
            "the H0 line lost endpoint eigenvalue four")

    centered = tuple(add(scale(6, unit(index, 6)), scale(-1, ones))
                     for index in range(6))
    d6 = scale(Q(1, 2), add(centered[1], centered[4]))
    expected_d6 = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    require(d6 == expected_d6 and sum(d6, Q(0)) == 0,
            "the complementary-hole centered average changed")
    require(tuple(d6[index] for index in rho_b) == d6,
            "the tau-plus debt stopped being rho-even")

    v = scale(Q(1, 2), add(unit(1, 6), unit(4, 6)))
    local = scale(Q(1, 4), add(unit(0, 6), unit(2, 6),
                               unit(3, 6), unit(5, 6)))
    delta_plus = scale(Q(1, 4), d6)
    require(add(v, scale(-1, local)) == delta_plus
            and delta_plus == scale(Q(1, 8), add(centered[1], centered[4])),
            "the lower-c2/tau-plus normalization changed")

    # The tau debt lies in the -2 eigenspace.  Therefore it has the very
    # short B-4 preimage -D6/6 (and -delta/6 after normalization).
    require(mat_vec(adjacency, d6) == scale(-2, d6),
            "the tau debt left the -2 endpoint eigenspace")
    b_minus_four = tuple(tuple(adjacency[row][column]
                               - 4 * identity[row][column]
                               for column in range(6)) for row in range(6))
    preimage = scale(Q(-1, 6), delta_plus)
    require(mat_vec(b_minus_four, preimage) == delta_plus,
            "the B-4 preimage of delta_plus changed")
    require(rank(b_minus_four) == 5,
            "B-4 stopped spanning the even augmentation-zero module")
    return {
        "B_label_to_unordered_hole": {
            f"B{index}": list(hole) for index, hole in enumerate(holes)
        },
        "rho_sites": "(0 1)",
        "rho_B": "(B0 B5)(B2 B3), B1,B4 fixed",
        "endpoint_adjacency": "octahedral K4-edge adjacency",
        "endpoint_adjacency_degree": 4,
        "centered_hole_class": "c_i^+=6*B_i-H0",
        "integral_identity": "D6=(c_1^++c_4^+)/2",
        "D6": [int(value) for value in d6],
        "tau_plus_identity": "delta_plus=(c_1^++c_4^+)/8",
        "delta_plus": [str(value) for value in delta_plus],
        "v": [str(value) for value in v],
        "local_even_average": [str(value) for value in local],
        "v_minus_local": "delta_plus",
        "B_eigenvalue_on_D6": -2,
        "B_minus_4_preimage": "-delta_plus/6",
        "rank_B_minus_4": rank(b_minus_four),
    }


def target_normal_gate_audit() -> dict[str, object]:
    # Coordinates are pure0,pure1,pure2,mixed0,mixed2.  Literal diagonal
    # Hasse/target rows stay in the first three coordinates.  The two-root
    # Weyl defect has both mixed entries, hence raises rank from 3 to 4.
    pure = tuple(unit(index, 5) for index in range(3))
    root_defect_target = (Q(-1), Q(0), Q(-1), Q(1), Q(1))
    require(rank(pure) == 3 and rank(pure + (root_defect_target,)) == 4,
            "the diagonal/mixed target rank jump changed")
    mixed_dual = (Q(0), Q(0), Q(0), Q(1), Q(0))
    require(all(dot(mixed_dual, row) == 0 for row in pure)
            and dot(mixed_dual, root_defect_target) == 1,
            "the primitive mixed-target detector changed")

    # In the operator basis (H_w,rho H_w), the Weyl target defect is
    # rho-invariant.  Target zero therefore means a+b=0.  Correcting the
    # signless vector (1,1) within this span necessarily gives the odd line.
    signless = (Q(1), Q(1))
    correction = (Q(-2), Q(0))
    corrected = add(signless, correction)
    require(corrected == (Q(-1), Q(1)) and sum(corrected, Q(0)) == 0,
            "the internal target correction stopped collapsing to odd")
    require(corrected[1] == -corrected[0],
            "the target-safe Cartan line changed")
    return {
        "target_coordinates": [
            "pure0", "pure1", "pure2", "mixed0", "mixed2"
        ],
        "literal_diagonal_target_rank": 3,
        "rank_after_root_Weyl_defect": 4,
        "diagonal_Hasse_row_cancels_2_w_minus_1_Delta": False,
        "primitive_mixed_target_detector": list(map(int, mixed_dual)),
        "Cartan_orbit_basis": ["H_w", "rho H_w"],
        "signless_operator": [1, 1],
        "internal_correction": [-2, 0],
        "corrected_operator": [-1, 1],
        "corrected_parity": "rho-odd",
        "noncollapsing_requirement": (
            "one independent rho-even target-bearing relative cell C_plus"
        ),
    }


def full_interface_and_typing_audit() -> dict[str, object]:
    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    v = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    d6 = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    delta_plus = scale(Q(1, 4), d6)
    target = scale(-2, tensor(d_root, v))
    eq = scale(2, tensor(d_root, v))
    require(add(target, eq) == (Q(0),) * 24
            and sum(value != 0 for value in target) == 8,
            "the C_plus target/Eq packet changed")

    # The two symbols named B are deliberately kept distinct.  The lower
    # occurrence theorem has two 12-coordinate source packets.  The C_plus
    # theorem has one six-coordinate complete-output quotient.  Agreement
    # of delta_plus does not define a map between them.
    lower_source_dimensions = (12, 12)
    cplus_output_dimension = 6
    require(sum(lower_source_dimensions) == 24
            and cplus_output_dimension == len(v),
            "the source/output presentation dimensions changed")

    # The old fourth-Hasse projection is (Eq,w)=(1,1), whereas the desired
    # correction is (1,0).  This is the next primitive cross-term guard.
    old_filler = (Q(1), Q(1))
    required_eq = (Q(1), Q(0))
    eq_dual = (Q(1), Q(-1))
    require(dot(eq_dual, old_filler) == 0
            and dot(eq_dual, required_eq) == 1
            and rank((old_filler, required_eq)) == 2,
            "the reduced-Eq Hasse cross-term guard changed")

    # Audit exact scope phrases in the pinned theorems rather than silently
    # promoting the equal coefficient shadows to a physical chain map.
    lower_note = (ROOT / "notes/h2-lower-centered-orientation-terminal-fork.md").read_text()
    signless_note = (ROOT / "notes/h3-signless-cartan-adjacent-power-shared-cell-gate.md").read_text()
    generic_note = (ROOT / "notes/h3-generic-cartan-adjacent-target-label-prolongation.md").read_text()
    full_note = (ROOT / "notes/h3-tau-plus-full-interface-product-bianchi-extension-gate.md").read_text()
    require("A physical (B-4I) theorem must fill" in lower_note
            and "one-endpoint Cartan cross term" in lower_note,
            "the lower B-4 physical gate changed")
    require("independent relative target-cone direction" in signless_note
            and "mixed target words" in signless_note,
            "the signless target-cone gate changed")
    require("The remaining" in generic_note
            and "conditional lower expression" in generic_note
            and "R_+" in generic_note
            and "source-labelled shifted comparison" in generic_note,
            "the generic C_plus remainder gate changed")
    require("one rho-even, nondegenerate" in full_note
            and "source-valid relative product-rule/Bianchi" in full_note,
            "the full tau-plus interface gate changed")
    return {
        "C_plus_parity": "rho-even",
        "C_plus_upper_target": "-2*D_root tensor v",
        "D_root": [int(value) for value in d_root],
        "C_plus_complete_lower_landing": "delta_plus",
        "C_plus_reduced_Eq_face": "+2*D_root*(H0-u)*Eq tensor v",
        "C_plus_labelled_ordinary_residue": "v",
        "next_Cartan_Hasse_boundary": (
            "R_plus=(1+rho)H_w d(P*) in the literal adjacent filtration"
        ),
        "old_formal_filler_reduced_Eq_w": [1, 1],
        "required_reduced_Eq_w": [1, 0],
        "primitive_reduced_Eq_dual": [1, -1],
        "lower_occurrence_source_dimensions": list(lower_source_dimensions),
        "C_plus_complete_output_dimension": cplus_output_dimension,
        "letter_B_warning": (
            "B_endpoint is the adjacency operator on occurrence holes; "
            "B0,...,B5 are six complete P3+K2 output columns"
        ),
        "physical_restriction_reinsertion_map_constructed": False,
        "coefficient_projection_agrees": True,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h2 B-4 / h3 C-plus shared-interface gate",
        "pins": PINS,
        "even_hole_and_tau_debt": even_hole_and_tau_debt_audit(),
        "target_normal_gate": target_normal_gate_audit(),
        "full_interface_and_typing": full_interface_and_typing_audit(),
        "conditional_shared_theorem": (
            "A source-valid rho-equivariant restriction/reinsertion map that "
            "sends the lower endpoint B-4 family to delta_plus and carries "
            "its signless target, reduced-Eq, residue, word, and Hasse faces "
            "is exactly the missing C_plus full-interface orbit at these "
            "projections.  Conversely, a physical C_plus orbit whose two "
            "marked order-two restrictions are the B-4 endpoint family "
            "closes the odd-dark lower centered branch."
        ),
        "verdict": (
            "The lower B-4 and root-even C_plus gates have exactly the same "
            "rho-even coefficient landing: delta_plus=(c_1^++c_4^+)/8. "
            "They are not yet the same physical cell because no committed "
            "map carries the two twelve-coordinate lower occurrence packets "
            "to the six complete B_i columns.  Literal diagonal target rows "
            "cannot cancel the mixed Weyl defect, and an internal Cartan "
            "correction becomes odd.  The smallest common construction is "
            "one independent target-bearing C_plus product-rule orbit with "
            "the forced delta_plus, reduced-Eq, residue, and one-endpoint/"
            "R_plus Hasse faces."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("B-4/C-plus ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("delta_plus=(c1_plus+c4_plus)/8: EXACT COEFFICIENT MATCH")
    print("diagonal target-normal row cancels mixed defect: NO")
    print("internal Cartan correction: COLLAPSES TO ODD")
    print("B-4 equals physical C_plus: CONDITIONAL ON MISSING SOURCE MAP")
    print("minimal shared cell: ONE FULL RHO-EVEN PRODUCT-RULE ORBIT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
