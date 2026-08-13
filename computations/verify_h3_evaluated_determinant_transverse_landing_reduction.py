#!/usr/bin/env python3
"""Route an evaluated K3,3 determinant into the physical landing theorem.

An abstract alternating occurrence covector is not enough.  For an actual
decorated 3x3 cross-cut block B, det(B) != 0 on an unbalanced colour cut
forces an offdiagonal entry with a nonzero signed 2x2 Laplace cofactor.
The nonzero offdiagonal cell then invokes the complete target-augmented
private-site identity, which supplies the physical distinct-head
determinant/hafnian-cofactor fan.

If that cell is a simple selected edge, the existing transverse theorem now
routes it exactly to four-good/support deletion or to the pure-colour coloop
C6/C8 and injective five-lock no-wedge residuals.  Determinant nonvanishing
alone does not prove simplicity or anchor escape.  Balanced determinants
also have a sharp purely diagonal guard.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py":
        "ba2c32a41b1d070d2af24546819e838697aba0273e85586a796ee25a27f5a950",
    "computations/verify_dark_cartan_scalar_visibility_physical_landing_gate.py":
        "9b52a25c26e3556669e743d9391564895ae514aec9d81e4dee2a97b9133d23ed",
    "computations/verify_h3_transverse_double_quotient_cartan_landing.py":
        "e2b536a2cc8e20883208dc098c84c6dabe15c5c01777f6018a8b72981274b5ae",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    "computations/verify_rectangular_interference_anchor_cartan_alternative.py":
        "b3d4db9e58f374bfd1f99a43931cac87fdab109c5d33c2f1c7d110e51e8f9a0a",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "computations/verify_frame_circuit_complete_source_kernel_lift_gate.py":
        "81738d71a423635da70caf7f3d46ca334cb0ebee7cd8240a0b7a7410c386f76c",
}
EXPECTED_LEDGER_SHA256 = (
    "880bd758e4266538e5e9c9d2c96872e24e00ad78b11240b4026b6f18d7d86bec"
)

SITES = tuple(range(6))
WORD = (0, 0, 1, 1, 2, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def permutation_sign(values):
    inversions = sum(values[left] > values[right]
                     for left in range(len(values))
                     for right in range(left + 1, len(values)))
    return -1 if inversions % 2 else 1


def multiply(values):
    answer = Fraction(1)
    for value in values:
        answer *= Fraction(value)
    return answer


def determinant(matrix):
    size = len(matrix)
    require(all(len(row) == size for row in matrix),
            "determinant matrix is not square")
    return sum(
        Fraction(permutation_sign(permutation))
        * multiply(matrix[row][permutation[row]] for row in range(size))
        for permutation in permutations(range(size))
    )


def minor(matrix, deleted_row, deleted_column):
    return tuple(
        tuple(value for column, value in enumerate(row)
              if column != deleted_column)
        for row_index, row in enumerate(matrix)
        if row_index != deleted_row
    )


def cofactor(matrix, row, column):
    sign = -1 if (row + column) % 2 else 1
    return Fraction(sign) * determinant(minor(matrix, row, column))


def canonical_cuts():
    return tuple(tuple(subset) for subset in combinations(SITES, 3)
                 if 0 in subset)


CUTS = canonical_cuts()
require(len(CUTS) == 10, "unoriented cut count changed")


def cut_data(cut):
    left = tuple(sorted(cut))
    right = tuple(sorted(set(SITES) - set(left)))
    left_colours = tuple(WORD[site] for site in left)
    right_colours = tuple(WORD[site] for site in right)
    balanced = sorted(left_colours) == sorted(right_colours)
    return left, right, left_colours, right_colours, balanced


def absent_colour_row(cut):
    """Choose a row/column shore site whose colour is absent opposite."""
    left, right, left_colours, right_colours, balanced = cut_data(cut)
    require(not balanced, "an unbalanced row was requested on a balanced cut")
    for row, colour in enumerate(left_colours):
        if colour not in right_colours:
            return "row", row, left[row], colour
    for column, colour in enumerate(right_colours):
        if colour not in left_colours:
            return "column", column, right[column], colour
    raise RuntimeError("an unbalanced ternary cut had no absent-colour shore")


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(len(matrix)))
                 for column in range(len(matrix[0])))


def exhaustive_unbalanced_laplace_audit():
    records = []
    tested_matrices = 0
    nonsingular_matrices = 0
    for cut in CUTS:
        left, right, left_colours, right_colours, balanced = cut_data(cut)
        if balanced:
            continue
        side, position, site, colour = absent_colour_row(cut)
        row_colours = left_colours
        column_colours = right_colours
        if side == "column":
            row_colours, column_colours = column_colours, row_colours

        require(all(colour != other for other in column_colours),
                "the selected absent-colour line acquired a diagonal entry")
        require(row_colours[position] == colour,
                "the selected absent-colour position changed")

        local_nonsingular = 0
        for entries in product((-1, 0, 1), repeat=9):
            matrix = tuple(tuple(Fraction(entries[3 * row + column])
                                 for column in range(3))
                           for row in range(3))
            if side == "column":
                matrix = transpose(matrix)
            value = determinant(matrix)
            laplace_products = tuple(
                matrix[position][column] * cofactor(matrix, position, column)
                for column in range(3)
            )
            require(sum(laplace_products, Fraction(0)) == value,
                    "the selected Laplace expansion changed")
            if value:
                require(any(laplace_products),
                        "a nonzero determinant lost every offdiagonal Laplace term")
                local_nonsingular += 1
            tested_matrices += 1
        nonsingular_matrices += local_nonsingular
        records.append({
            "cut": list(cut),
            "left_colours": list(left_colours),
            "right_colours": list(right_colours),
            "absent_colour_side": side,
            "absent_colour_site": site,
            "absent_colour": colour,
            "matrices_checked": 3 ** 9,
            "nonsingular_matrices": local_nonsingular,
            "conclusion": (
                "det(B)!=0 forces A_e*Cof_e!=0 for an offdiagonal "
                "decorated cross-cut entry e"
            ),
        })

    require(len(records) == 6 and tested_matrices == 6 * 3 ** 9,
            "the exhaustive unbalanced determinant audit changed")
    require(nonsingular_matrices > 0,
            "the unbalanced determinant audit became vacuous")
    return {
        "unbalanced_cuts": len(records),
        "records": records,
        "matrices_checked": tested_matrices,
        "nonsingular_matrices": nonsingular_matrices,
    }


def balanced_diagonal_guard():
    cut = (0, 2, 4)
    left, right, left_colours, right_colours, balanced = cut_data(cut)
    require(balanced and left_colours == right_colours == (0, 1, 2),
            "the balanced guard cut changed")
    matrix = tuple(
        tuple(Fraction(int(row == column)) for column in range(3))
        for row in range(3)
    )
    support = tuple((left[index], right[index], left_colours[index],
                     right_colours[index]) for index in range(3))
    require(determinant(matrix) == 1
            and all(left_colour == right_colour
                    for _left, _right, left_colour, right_colour in support),
            "the purely diagonal determinant guard changed")
    return {
        "cut": list(cut),
        "evaluated_determinant": 1,
        "support": [list(cell) for cell in support],
        "offdiagonal_cells": 0,
        "private_site_active_identity_applicable": False,
        "verdict": (
            "evaluated determinant nonvanishing alone is not transverse"
        ),
    }


def unbalanced_anchor_contained_guard():
    # Across 012|345, the permutation (1,2,0) gives 04|15|23.  Its first
    # two cells have colour types 02 and 02 and the last is diagonal 11.
    cut = (0, 1, 2)
    left, right, left_colours, right_colours, balanced = cut_data(cut)
    require(not balanced, "the anchor-contained guard became balanced")
    selected = (1, 2, 0)
    matrix = tuple(
        tuple(Fraction(int(column == selected[row])) for column in range(3))
        for row in range(3)
    )
    matching = tuple(
        sorted((left[row], right[selected[row]]) for row in range(3))
    )
    offdiagonal = tuple(
        pair for pair in matching if WORD[pair[0]] != WORD[pair[1]]
    )
    require(abs(determinant(matrix)) == 1
            and len(offdiagonal) == 2
            and len({site for pair in offdiagonal for site in pair}) == 4,
            "the unbalanced anchor-contained guard changed")

    # Choose the selected three-anchor union to contain this matching.  This
    # is an incidence guard, not a complete GHZ source packet.  It proves
    # that determinant nonvanishing does not make the two offdiagonal cells
    # share a centre or escape the anchor web.
    anchor_union = set(matching)
    require(all(pair in anchor_union for pair in offdiagonal),
            "the guard stopped being anchor-contained")
    return {
        "cut": list(cut),
        "evaluated_determinant_absolute_value": 1,
        "nonzero_matching": [list(pair) for pair in matching],
        "offdiagonal_cells": [list(pair) for pair in offdiagonal],
        "offdiagonal_cells_share_centre": False,
        "all_nonzero_cells_anchor_contained": True,
        "verdict": (
            "the cross-cut determinant does not itself supply the escaping "
            "private-site fan or close the injective five-lock residual"
        ),
    }


def rectangular_rank_two_audit():
    # Complete protected rectangular bright packet: M=0, external g=1 and
    # anchor row h=1.  The augmented minor is a unit after localizing at its
    # nonzero value.  It closes algebraically; no scalar/four-good inference
    # is required.
    matrix = ((Fraction(0), Fraction(1)),
              (Fraction(1), Fraction(0)))
    value = determinant(matrix)
    require(value == -1,
            "the minimal rectangular two-rank unit changed")

    # Attaching the metadata "diagonal (c,c) on the selected edge" changes
    # no rank.  This replays why a label-free rank statement cannot itself
    # be called an active overlap; if the complete protected minor is not
    # available as a source unit, the physical labels must enter 32f3bdc.
    return {
        "base_rank": 0,
        "anchor_cartan_augmented_rank": 2,
        "augmented_minor": int(value),
        "complete_protected_outcome": "localized source unit",
        "four_good_pair_required": False,
        "label_free_guard": {
            "possible_cartan_head": "diagonal (c,c) on selected edge",
            "active_overlap_forced": False,
        },
    }


def marked_separator_typing_audit():
    # O is the free occurrence module for three matching terms of one
    # complete source row.  P is the actual one-dimensional physical row
    # domain.  The physical expansion map sends its generator to the sum of
    # all three occurrence coordinates.
    expansion = (Fraction(1), Fraction(1), Fraction(1))
    occurrence_selectors = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )
    pullbacks = tuple(sum(selector[index] * expansion[index]
                          for index in range(3))
                      for selector in occurrence_selectors)
    require(pullbacks == (1, 1, 1),
            "occurrence selectors unexpectedly separated a complete row")

    # On the free occurrence presentation, lambda*M=e_0^* really is an
    # occurrence pivot.  After restriction to the physical complete-row
    # domain it says only lambda*M_phys=1.  It does not annihilate the other
    # two matching terms because those are not independent physical columns.
    occurrence_map = (
        (Fraction(1), Fraction(0), Fraction(0)),
    )
    physical_map = (
        (sum(occurrence_map[0][index] * expansion[index]
             for index in range(3)),),
    )
    require(occurrence_map[0] == occurrence_selectors[0]
            and physical_map == ((Fraction(1),),),
            "the occurrence/physical restriction guard changed")

    return {
        "free_occurrence_domain_dimension": 3,
        "physical_complete_row_domain_dimension": 1,
        "physical_expansion_vector": [1, 1, 1],
        "three_occurrence_selector_pullbacks": list(map(int, pullbacks)),
        "conditional_positive_statement": (
            "if the constructed complete source map M genuinely has a free "
            "domain coordinate for the marked matching occurrence and h is "
            "that coordinate covector, then lambda^T M=h is a localized "
            "occurrence pivot/source unit"
        ),
        "current_typing_mismatch": (
            "the common-tail theorem gives a matching monomial inside one "
            "complete coefficient row.  The other matching terms are tied "
            "to the same physical generator, so the occurrence selector is "
            "a covector on a free occurrence presentation, not yet a "
            "covector on the actual complete-row source domain.  Its "
            "pullback selects the whole generator and does not annihilate "
            "the other occurrences"
        ),
        "aggregate_anchor_warning": (
            "the rectangular h may instead be the protected pure-anchor or "
            "anchor-incidence functional.  That is a covector on physical "
            "source columns, but it is not the coordinate selector of one "
            "matching occurrence"
        ),
        "verdict": (
            "the separator branch is automatically a source unit only "
            "after the marked occurrence-domain lift is constructed; using "
            "it now would assume the missing lift"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "unbalanced_laplace_audit": exhaustive_unbalanced_laplace_audit(),
        "balanced_diagonal_guard": balanced_diagonal_guard(),
        "unbalanced_anchor_contained_guard": (
            unbalanced_anchor_contained_guard()
        ),
        "rectangular_rank_two": rectangular_rank_two_audit(),
        "marked_separator_typing": marked_separator_typing_audit(),
        "physical_bridge": (
            "for an unbalanced evaluated decorated K3,3 minor, det(B)!=0 "
            "forces an offdiagonal cell e with nonzero signed 2x2 cross-cut "
            "cofactor.  Since e!=0, the complete target-augmented private-"
            "site identity independently forces a nonzero physical "
            "determinant/hafnian-cofactor fan with distinct centre heads"
        ),
        "simple_edge_landing_theorem": (
            "if such an e is a simple selected edge, then either no pure-c "
            "matching avoids e and the exact residual is the anchor-contained "
            "C6/C8 coloop carrier, or pure-c reselection makes e four-good.  "
            "An escaping active mate gives the distinct-head four-good "
            "overlap; otherwise the five-lock theorem gives anchor-safe "
            "deletion, a complementary crossed four-good wedge, or the "
            "injective no-complementary-wedge residual"
        ),
        "sharp_scope": (
            "evaluated determinant nonvanishing does not by itself imply a "
            "simple selected edge, anchor escape, three deleted-star heads, "
            "or identification of its signed 2x2 cofactor with the physical "
            "hafnian cofactor.  Balanced minors can be purely diagonal, and "
            "an unbalanced determinant-one monomial block can be entirely "
            "anchor-contained.  Thus neither named residual is closed by "
            "cross-cut determinant structure alone"
        ),
        "frontier": (
            "the remaining landing input is incidence/source typing: place "
            "a nonzero offdiagonal Laplace factor on the marked simple edge, "
            "or show that failure of simplicity is already an effective "
            "Hall/reselection exit.  Once simplicity holds, the existing "
            "coloop/five-lock theorem is exhaustive"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
