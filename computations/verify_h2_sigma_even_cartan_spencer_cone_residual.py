#!/usr/bin/env python3
"""Construct the minimal sigma-even target/Eq cone and freeze its residual.

For each of the two lower order-two cuts, let N_c be the primitive mixed
target normal of the exact B-4 preimage.  The three boundary columns

    lower B path       (target,Eq) = ( N_c,  0),
    h=2 J* Cartan cone (target,Eq) = (-N_c,-N_c),
    reduced-Eq Spencer (target,Eq) = ( 0,   N_c)

sum to zero.  Every proper pair has rank two, so this is the minimal
target/Eq cone.  The cut symmetry sigma=(2 5)(3 4) exchanges its two object
copies, hence one sigma-covariant orbit suffices.

This derived target/Eq construction is not the physical iota.  The actual
six-output complete Eq correction is -delta_plus.  The full interface
prescribes labelled residue v=(B1+B4)/2 and the two physical word placements
0112/q23:21 and 0121/q45:12, but the even J* Cartan residue and literal word
image are undefined until the shifted placement P2 is constructed.  The two
word restrictions are one sigma orbit but independent objectwise rows.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py":
        "09ba792f229bb3a1e930b2c59b0de2356b08a7434c648aad9573d8382c652a52",
    "notes/h2-lower-even-cartan-jstar-target-cone-gate.md":
        "2f80cf6fa8d87a9acc4f3441bba5753b9b3c7de5c19e6c709d75969b7eb9d381",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
    "notes/h2-lower-delta-plus-iota-target-rank-gate.md":
        "f4ffa65a59fab2999510167d8aaae1433690ce920f985836a9e99cc4b23f953c",
    "computations/verify_h3_generic_cplus_lower_quotient_smith_gate.py":
        "f4ee0503c4639b79a655bdbab94d02218c99b348bee8f3c46f9554b7e803e3e0",
    "notes/h3-generic-cplus-lower-quotient-smith-gate.md":
        "c8ab8922b05e81819029a51d09475de746173c727313c1a5ff7c6d3aca24f2e5",
    "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py":
        "9bd2c9f482dc3277d07bd96a4e2189034e766f97e7800d3864179a75e03cef17",
    "notes/h3-cplus-root-even-koszul-physical-dressing-gate.md":
        "c21d7e3e140d2d86d040f9928c787011a7b49e9c58493f812086065c05715e9b",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "notes/h3-tau-plus-full-interface-product-bianchi-extension-gate.md":
        "38c3fc7f9191dcc7ae16f368b5b861dd48f7e2cb0ad599bcb03f7ab26af40366",
}
EXPECTED_LEDGER_SHA256 = (
    "db0ba608a436c18c0b7fd9a14acfe37aa6d48aafe1171346dec3377c30da940e"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def unit(index, size):
    answer = [Q(0)] * size
    answer[index] = Q(1)
    return tuple(answer)


def target_eq_cone_audit():
    lower = load(
        "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py",
        "sigma_cone_lower",
    )
    cuts = (
        ("0112/q23:21", (0, 1, 4, 5)),
        ("0121/q45:12", (0, 1, 2, 3)),
    )
    columns = []
    records = []
    normals = []
    for label, sites in cuts:
        normal, _diagonal = lower.cut_target_normal(sites)
        n = lower.dense(normal)
        zero = (Q(0),) * len(n)
        lower_b = n + zero
        jstar_cartan = scale(-1, n) + scale(-1, n)
        spencer = zero + n
        require(add(lower_b, jstar_cartan, spencer)
                == (Q(0),) * (2 * len(n)),
                ("target/Eq cone stopped closing", label))
        require(rank((lower_b, jstar_cartan, spencer)) == 2
                and all(rank(pair) == 2 for pair in (
                    (lower_b, jstar_cartan),
                    (lower_b, spencer),
                    (jstar_cartan, spencer),
                )), ("the three-term cone stopped being minimal", label))
        columns.extend((lower_b, jstar_cartan, spencer))
        normals.append(normal)
        records.append({
            "cut": label,
            "primitive_normal_support": len(normal),
            "lower_B_target_Eq": ["N_c", "0"],
            "normalized_h2_Jstar_Cartan_target_Eq": ["-N_c", "-N_c"],
            "root_decorated_K_Eq_Spencer_target_Eq": ["0", "+N_c"],
            "total": [0, 0],
            "three_column_rank": 2,
            "every_proper_pair_rank": 2,
        })

    # Each cut contributes an independent two-row cone.  The six columns
    # therefore have rank four and a two-dimensional relation space, one
    # relation per object.  Sigma exchanges those two relations.
    require(rank(columns) == 4, "the two-cut cone rank changed")
    sigma = (0, 1, 5, 4, 3, 2, 6, 7)
    require(lower.move_sparse(normals[0], sigma) == normals[1],
            "sigma stopped transporting the target/Eq cone")
    return {
        "cut_cones": records,
        "combined_six_column_rank": rank(columns),
        "combined_kernel_dimension": 2,
        "cut_symmetry": "sigma=(2 5)(3 4)",
        "sigma_exchanges_the_two_kernel_relations": True,
        "minimum_new_equivariant_cell_types": (
            "one sigma-orbit of h2 Jstar even Cartan cells and its "
            "canonical root-decorated K_Eq Spencer face"
        ),
        "target_closed": True,
        "root_reduced_Eq_closed": True,
    }


def order_normalization_audit():
    records = []
    for h in (2, 3):
        for alpha, beta in ((Q(2), Q(3)), (Q(-5, 2), Q(7))):
            jstar = -h * alpha * beta
            normalized_input = Q(1, h * h * alpha * beta) * jstar
            require(normalized_input == Q(-1, h),
                    "the universal trace coefficient changed")
            # P_h supplies h, and evenization supplies two.
            normalized_target = 2 * h * normalized_input
            require(normalized_target == -2,
                    "the normalized target stopped being order independent")
            records.append({
                "h": h,
                "alpha": str(alpha),
                "beta": str(beta),
                "Jstar": f"-{h}*alpha*beta*I",
                "normalized_trace_coefficient": str(normalized_input),
                "normalized_even_target": str(normalized_target),
            })
    return {
        "formula": (
            "Jstar_h=-h alpha beta I; "
            "(h^2 alpha beta)^-1 Jstar_h=-I/h"
        ),
        "intrinsic_P_h_factor": "h",
        "endpoint_evenization_factor": 2,
        "normalized_target_all_orders": "-2*(w-1)Delta",
        "h2_restriction_matches_h3_Cplus_target": True,
        "records": records,
    }


def actual_augmented_residual_audit():
    d6 = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    delta = scale(Q(1, 4), d6)
    zero6 = (Q(0),) * 6
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    local = (Q(1, 4), Q(0), Q(1, 4),
             Q(1, 4), Q(0), Q(1, 4))
    require(add(v, scale(-1, local)) == delta,
            "the b6ee603 lower quotient changed")

    # The known complete realization ties lower and Eq.  The target/root-Eq
    # cone above does not change this separate complete-output tie.
    known_tied = delta + delta
    desired = delta + zero6
    complete_eq_residual = add(desired, scale(-1, known_tied))
    require(complete_eq_residual == zero6 + scale(-1, delta),
            "the complete Eq residual changed")
    private_eq_dual = d6 + scale(-1, d6)
    require(dot(private_eq_dual, known_tied) == 0
            and dot(private_eq_dual, desired) == 3,
            "the normalized complete Eq dual changed")

    # The full interface prescribes residue v.  The committed diagonal and
    # old Cartan residue lines miss it.  The new even J* Cartan residue is not
    # termwise defined before P2, so this is a forced quotient target/guard,
    # not a computed value of the unplaced cone.
    diagonal_residue = (Q(1),) * 6
    cartan_residue = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    residue_dual = (Q(0), Q(1), Q(-1), Q(0), Q(1), Q(-1))
    require(dot(residue_dual, diagonal_residue) == 0
            and dot(residue_dual, cartan_residue) == 0
            and dot(residue_dual, v) == 1,
            "the labelled residue residual changed")

    # Objectwise word coordinates: diagonal cap, the 0112 placement, and
    # the 0121 placement.  The formal J*/Spencer cone is in the first line;
    # the physical lower restriction asks for the other two.  Sigma swaps
    # them, so the invariant residual is one orbit line, while objectwise
    # placement has rank two.
    diagonal_word = unit(0, 3)
    word_23 = unit(1, 3)
    word_45 = unit(2, 3)
    sigma_even_word = scale(Q(1, 2), add(word_23, word_45))
    sigma_odd_word = scale(Q(1, 2), add(word_23, scale(-1, word_45)))
    require(rank((word_23, word_45)) == 2
            and rank((diagonal_word, word_23, word_45)) == 3
            and rank((sigma_even_word, sigma_odd_word)) == 2,
            "the physical word residual changed")

    return {
        "actual_six_output_lower": {
            "direct_omitted_pair": "v=(B1+B4)/2",
            "local_order2_face": "(B0+B2+B3+B5)/4",
            "relative_landing": "delta_plus=v-local",
        },
        "complete_Eq_residual_after_target_Eq_cone": {
            "known_tied_packet": ["delta_plus", "delta_plus"],
            "desired": ["delta_plus", "0"],
            "residual": ["0", "-delta_plus"],
            "integral_private_Eq_dual_value": 12,
        },
        "labelled_ordinary_residue_residual": {
            "forced_class_mod_old_diagonal_Cartan_span": "v=(B1+B4)/2",
            "primitive_dual": [0, 1, -1, 0, 1, -1],
            "dual_value": 1,
            "even_Jstar_Cartan_residue_before_P2": "undefined",
            "status": "prescribed full-interface class, not evaluated cone residue",
        },
        "word_residual": {
            "formal_cone_word": "diagonal identity-cap object",
            "physical_object_words": [
                "0112 with q23:21 reinsertion",
                "0121 with q45:12 reinsertion",
            ],
            "objectwise_word_quotient_rank": 2,
            "sigma_even_orbit_rank": 1,
            "physical_midpoint_word_hits_from_old_formal_totalization": 0,
        },
        "target_residual": 0,
        "root_reduced_Eq_residual": 0,
    }


def root_word_physical_dressing_audit():
    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    e = scale(2, tuple(root * label for root in d_root for label in v))
    zero = (Q(0),) * len(e)
    require(len(e) == 24 and sum(value != 0 for value in e) == 8,
            "the root-word Eq decoration changed")

    # Rows are lower/private, Eq, W, target, word-resolved ores, anchor.
    clean = e + e  # convenient width seed; actual vector below is 5*24+1
    del clean
    desired = zero + e + zero + zero + zero + (Q(0),)
    nearest = e + e + zero + zero + scale(-1, e) + (Q(0),)
    debt = add(nearest, scale(-1, desired))
    expected_debt = e + zero + zero + zero + scale(-1, e) + (Q(0),)
    require(debt == expected_debt,
            "the nearest physical K_Eq dressing debt changed")

    # Root summation forgets precisely the nonzero word-resolved data.
    def coarse(values):
        return tuple(sum((values[6 * root + label]
                          for root in range(4)), Q(0))
                     for label in range(6))

    require(coarse(e) == zero[:6]
            and coarse(scale(-1, e)) == zero[:6],
            "the root-even dressing stopped being coarse-dark")

    actual_local = (0, 2, 3, 5)
    fixed_dual = (Q(0), Q(1), Q(0), Q(0), Q(1), Q(0))
    require(all(fixed_dual[index] == 0 for index in actual_local)
            and dot(fixed_dual, v) == 1,
            "the actual/fixed source-grade separator changed")
    return {
        "root_word_coefficient": "E=2 D_root tensor v",
        "nonzero_root_word_labels": 8,
        "clean_derived_Spencer_signature": {
            "lower_private": 0,
            "Eq": "+E",
            "W": 0,
            "target": 0,
            "word_resolved_ores": 0,
            "anchor": 0,
        },
        "nearest_checked_physical_lift": {
            "lower_private": "+E",
            "Eq": "+E",
            "W": 0,
            "target": 0,
            "word_resolved_ores": "-E",
            "coarse_six_ores": 0,
            "anchor": 0,
        },
        "actual_augmented_debt_after_nearest_lift": {
            "lower_private": "+E",
            "word_resolved_ores": "-E",
        },
        "required_hidden_faces_on_raw_Cplus": {
            "lower_private": "-E",
            "word_resolved_ores": "+E",
        },
        "actual_local_source_B_span": ["B0", "B2", "B3", "B5"],
        "required_fixed_plane": ["B1", "B4"],
        "fixed_plane_dual_value_on_v": 1,
        "root_decoration_changes_matching_or_repeated_edge": False,
    }


def hasse_and_physical_scope_audit():
    h2_note = (ROOT /
        "notes/h2-lower-even-cartan-jstar-target-cone-gate.md").read_text()
    full_note = (ROOT /
        "notes/h3-tau-plus-full-interface-product-bianchi-extension-gate.md").read_text()
    b6_note = (ROOT /
        "notes/h3-generic-cplus-lower-quotient-smith-gate.md").read_text()
    dressing_note = (ROOT /
        "notes/h3-cplus-root-even-koszul-physical-dressing-gate.md").read_text()
    require("That image is undefined until" in h2_note
            and "source-labelled placement" in h2_note,
            "the h2 P2 typing guard changed")
    require("hits no selected midpoint source word" in full_note
            and "labelled ordinary residue `v`" in full_note,
            "the full Cplus word/residue interface changed")
    require("smallest complete-column correction" in b6_note
            and "(0,-\\delta_+)" in b6_note,
            "the b6ee603 complete Eq residual changed")
    require("lower/private}=+E" in dressing_note
            and "word-resolved residue" in dressing_note,
            "the root-word physical dressing debt changed")
    return {
        "exact_formal_Hasse_remainder": (
            "R2+=-1/2(1+S)H_w d(P2(I)) in each cut, together with the "
            "occurrence-local one-endpoint product-rule face"
        ),
        "literal_value_before_P2": "undefined",
        "reason": (
            "the diagonal identity-cap object and the two occurrence-local "
            "word/fine/repeated objects are not joined by a committed "
            "source-labelled P2 map"
        ),
        "constructed_here": (
            "the minimal sigma-covariant target/reduced-Eq mapping cone"
        ),
        "not_constructed_here": (
            "the physical P2 descent carrying complete Eq=-delta_plus, "
            "labelled residue v, the two word faces, ridge/protected rows, "
            "and the Hasse remainder"
        ),
        "comparison_with_b6ee603": (
            "exact agreement on complete Eq and the forced interface: after "
            "target/root Eq close, b6ee603 prescribes "
            "(-delta_plus,v,two cut words); ores and word remain undefined "
            "on the unplaced even cone.  The word-resolved physical dressing "
            "further exposes hidden (+E,-E) lower/residue debts which are "
            "coarse-dark in b6ee603"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h2 sigma-even Cartan-Spencer cone residual",
        "pins": PINS,
        "minimal_target_Eq_cone": target_eq_cone_audit(),
        "h2_h3_normalization": order_normalization_audit(),
        "actual_augmented_residual": actual_augmented_residual_audit(),
        "root_word_physical_dressing": root_word_physical_dressing_audit(),
        "Hasse_and_physical_scope": hasse_and_physical_scope_audit(),
        "verdict": (
            "The h2 Jstar even Cartan cell and the canonical root-decorated "
            "K_Eq face form the minimal sigma-covariant cone cancelling "
            "both mixed target and root reduced Eq on the two lower B-4 "
            "objects.  This closes the output-side target/Eq triangle but "
            "does not construct physical iota.  The complete Eq correction "
            "is exactly -delta_plus.  In agreement with b6ee603, the full "
            "interface further prescribes labelled residue v and two "
            "objectwise word placements forming one sigma orbit, but their "
            "values on the even cone, and the Hasse value, remain undefined "
            "until the source-labelled P2 comparison is supplied.  The "
            "nearest physical K_Eq dressing sharpens this with word-resolved "
            "lower/private +E and residue -E debts, requiring hidden -E/+E "
            "faces on the raw Cplus cell."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("sigma-even Cartan-Spencer ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("sigma-covariant h2 Jstar/Spencer derived target-Eq cone: CONSTRUCTED")
    print("mixed target and root reduced Eq residual: ZERO")
    print("complete Eq exact: -delta_plus; forced ores/word: v / TWO CUT WORDS")
    print("nearest physical K_Eq dressing debt: lower +E / word-ores -E")
    print("literal Hasse value before P2: UNDEFINED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
