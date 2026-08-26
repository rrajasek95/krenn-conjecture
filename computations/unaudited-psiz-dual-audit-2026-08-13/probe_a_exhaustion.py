#!/usr/bin/env python3
"""TASK A: the exhaustive same-grade physical column inventory versus psi_z.

Method.  Every committed column family is placed in the 30-coordinate
augmented ambient of `verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py`
(the module the balanced-square dual actually lives on), projected to the
four chart coordinates (A_[a|b],A_[b|a],B,C) = the four B-corners, and paired
both with the bare chart dual psi_z and with every admissible augmented
extension of it.

Two tests are reported for each column, and they are NOT the same:

  (i)  the bare cone criterion of the h3-balanced-square note: is the gauged
       vertex augmentation <z, pi(c)> nonzero?
  (ii) the augmented criterion: does c leave SOME extension of psi_z alive?

Test (i) is satisfied by named columns that manifestly do not fill (r0_j is
the standard example), because those columns carry extra rows outside the
square.  Test (ii) is the operative one; it is exactly "is the balanced face
in the image of the full same-grade map".

For families whose readout into these rows is NOT committed (the 171-column
full-q Jacobian, the anchor/q terminal, occurrence-Q, ridge/eta/sigma), we
do not guess a vector: we quantify over the WHOLE coordinate subspace the
family can occupy and check whether every admissible extension of psi_z
annihilates all of it.  That is strictly stronger than testing one column.

UNAUDITED external probe.  Exact over Q.  Pinned HEAD 0a684ce.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json

import common
from common import (require, rank, left_kernel, dot, add, scale, vec, LABELS,
                    INDEX, ALPHA, Z, PSI_Z, square_projection,
                    gauged_augmentation, in_span, primitive)


# ==========================================================================
# 1.  The inventory
# ==========================================================================

def cap_cartan_columns(p_f=(Q(0),) * 4):
    """r0_j, T_j, rho_j, K exactly as the committed nonfill checker builds them."""
    columns = []
    for corner in range(4):
        columns.append((f"r0_{corner}", "cap (augmented cap column)", vec(**{
            f"B{corner}": 1, f"Eq{corner}": 1, f"target{corner}": 1,
            "M": -1, "ainc": -1, "q": 0, "P_f": p_f[corner]})))
        columns.append((f"T_{corner}", "cap (target/W)", vec(**{
            f"W{corner}": -1, f"target{corner}": 1})))
        columns.append((f"rho_{corner}", "cap (W/ordinary residue)", vec(**{
            f"W{corner}": 1, f"ores{corner}": 1})))
    columns.append(("K", "endpoint-odd Cartan residue + ridge/eta/sigma", vec(**{
        **{f"ores{c}": ALPHA[c] for c in range(4)},
        "ridge": 1, "eta_constant": 1, "eta_u_over_t": 1, "sigma_q22": -1})))
    return tuple(columns)


def k22_companion_columns():
    """The four balanced K2,2 companion/mate columns (0ffc23a, master note).

    These are genuine chart-square columns: they touch the four corners and
    nothing else.  They are exactly the rows F_A0,F_A1,F_B0,F_B1 of the
    recurrent-core complete-row model, read as columns of the square.
    """
    signless = ((1, 0, 1, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 1, 0, 1))
    return tuple(
        (f"K22_companion_{index}", "K2,2 companion (chart square)",
         vec(**{f"B{c}": value for c, value in enumerate(column) if value}))
        for index, column in enumerate(signless))


def normalized_pure_target_columns():
    """The two normalized pure-target selectors, adjoined as ACTUAL columns."""
    return (
        ("pure_target_2", "normalized pure-target selector", vec(target2=1)),
        ("pure_target_3", "normalized pure-target selector", vec(target3=1)),
    )


def aggregate_and_global_columns():
    """TIER 3: transported from an adjacent grade, not independently committed
    as four-corner columns.  Retained because they only SHRINK the surviving
    dual space, so including them makes the extension verdict harder, not
    easier.

    W_global and common_tail_escape are deliberately ABSENT: no committed
    checker constructs any column with nonzero entry there.  They occur only
    in the LABELS tuple and in protected-zero assertions, i.e. they are guard
    rows, and they are reported as such by `guard_rows_with_no_column()`.
    """
    return (
        ("ores_aggregate",
         "aggregate scalar ordinary-residue column (repair-45 A.5, six-label "
         "grade; transported)",
         vec(**{f"ores{c}": 1 for c in range(4)})),
        ("ridge_only", "labelled ridge column (ridge/Kahler grade)",
         vec(ridge=1)),
        ("eta_constant", "ridge terminal contraction eta_constant",
         vec(eta_constant=1)),
        ("eta_u_over_t", "ridge terminal contraction eta_u/t",
         vec(eta_u_over_t=1)),
        ("sigma_q22", "ridge terminal contraction sigma_q22",
         vec(sigma_q22=1)),
    )


def guard_rows_with_no_column():
    return {
        "rows": ["W_global", "common_tail_escape"],
        "status": (
            "no committed checker constructs a column with nonzero entry in "
            "these rows; they occur only in the LABELS tuple and in "
            "protected-zero assertions of the chi_w nonfill and balanced-"
            "square cone gates.  They are excluded from the inventory"),
    }


def q_anchor_columns():
    """The physical q terminal / anchor incidence family.

    We do NOT admit bare M or bare ainc selectors: a column with q != M-ainc
    violates the literal physical identity that every committed checker
    imposes.  The admissible family is exactly the one the committed nonfill
    checker stresses, q = M - ainc with arbitrary pointed anchor, plus the
    bare pointed conormal P_f, which IS constructible as the difference of
    two r0 corners with different anchor values (the committed 81-assignment
    pointed-anchor stress).
    """
    columns = [
        ("P_f_pointed_conormal",
         "pointed conormal P_f = r0_j(P_f=1)-r0_j(P_f=0)", vec(P_f=1)),
    ]
    for matching in (-1, 0, 1):
        for anchor in (-1, 0, 1):
            for pointed in (-1, 0, 1):
                columns.append((
                    f"q_literal_M{matching}_a{anchor}_P{pointed}",
                    "literal q=M-ainc stress column",
                    vec(M=matching, ainc=anchor, q=matching - anchor,
                        P_f=pointed)))
    return tuple(columns)


def q_identity_violating_columns():
    """Reported separately: they would violate the literal q=M-ainc row."""
    return (
        ("ainc_bare", "bare anchor incidence (VIOLATES q=M-ainc)", vec(ainc=1)),
        ("M_bare", "bare selected matching sum (VIOLATES q=M-ainc)", vec(M=1)),
    )


def mv_o_alpha_columns():
    """O_alpha and the literal M_v mapping-cone image (two-gate sketch (1))."""
    core = {name: value for name, _kind, value in cap_cartan_columns()}
    o_alpha = tuple(Q(0) for _ in LABELS)
    for corner in range(4):
        o_alpha = add(o_alpha, scale(ALPHA[corner], add(
            scale(-1, core[f"r0_{corner}"]),
            core[f"T_{corner}"], core[f"rho_{corner}"])))
    m_v = add(scale(-1, o_alpha), core["K"])
    return (
        ("O_alpha", "cap composite sum_j alpha_j(-r0_j+T_j+rho_j)", o_alpha),
        ("M_v", "literal mapping-cone image M_v=-O_alpha+K", m_v),
    )


def full_inventory():
    named = (cap_cartan_columns() + k22_companion_columns()
             + normalized_pure_target_columns()
             + aggregate_and_global_columns() + q_anchor_columns()
             + mv_o_alpha_columns())
    seen = set()
    answer = []
    for name, kind, value in named:
        require(name not in seen, ("duplicate column name", name))
        seen.add(name)
        answer.append((name, kind, value))
    return tuple(answer)


# ==========================================================================
# 2.  Families whose readout is not committed: quantify over their support
# ==========================================================================

UNCOMMITTED_SUPPORTS = {
    "full_q_Jacobian_171_columns": (
        ["M", "ainc", "q", "P_f"],
        "the 171-column simultaneous-q scalar-source Jacobian and its "
        "three-term product-rule anchor conormal.  Their codomain is the "
        "unary/response coefficient rows; the only rows of the balanced "
        "grade they can populate are the scalar q/anchor/pointed rows"),
    "ridge_eta_sigma_terminal": (
        ["ridge", "eta_constant", "eta_u_over_t", "sigma_q22"],
        "the residual-q terminal ridge/Kahler identification rows"),
    "reduced_Eq_block": (
        [f"Eq{c}" for c in range(4)],
        "the reduced-Eq / occurrence-Q readout block"),
    "global_W_and_tail_escape": (
        ["W_global", "common_tail_escape"],
        "the global W row and the common-tail escape row"),
    "occurrence_Q_and_0102_dq": (
        [f"Eq{c}" for c in range(4)] + ["q", "ridge"],
        "the occurrence-Q, word-0102 and dq23 reinsertion readouts; the "
        "committed checkers give them only occurrence-private coordinates, "
        "whose images in this grade are confined to the Eq/q/ridge rows "
        "(verify_h3_gate_ii_psidelta_same_grade_extension_chain.py: 'the "
        "occurrence-local section and dq23 reinsertion have no q/W/ridge "
        "readouts')"),
}


# ==========================================================================
# 3.  The exhaustion
# ==========================================================================

def exhaust():
    conventions = common.verify_chart_basis_conventions()
    inventory = full_inventory()
    columns = [value for _n, _k, value in inventory]
    names = [name for name, _k, _v in inventory]

    balanced_face = vec(**{f"B{c}": Z[c] for c in range(4)})
    target_companion = vec(**{f"target{c}": -Z[c] for c in range(4)})

    # ---- the two committed duals ---------------------------------------
    psi_plain = common.psi_ambient()
    psi_pure_safe = vec(**{
        **{f"B{c}": Z[c] for c in range(4)},
        "Eq2": 1, "Eq3": 1, "target0": -1, "target1": -1,
        "W0": -1, "W1": -1, "ores0": 1, "ores1": 1})

    # ---- per-column report ----------------------------------------------
    per_column = []
    for name, kind, value in inventory:
        square = square_projection(value)
        per_column.append({
            "column": name,
            "provenance": kind,
            "chart_square_projection": [str(v) for v in square],
            "gauged_augmentation": str(gauged_augmentation(square)),
            "bare_cone_criterion_met": gauged_augmentation(square) != 0,
            "pairing_with_plain_psi": str(dot(psi_plain, value)),
            "pairing_with_pure_safe_psi": str(dot(psi_pure_safe, value)),
        })

    # ---- rank / membership: the decisive test ---------------------------
    inventory_rank = rank(columns)
    rank_with_face = rank(columns + [balanced_face])
    face_in_image = in_span(columns, balanced_face)
    require(face_in_image == (rank_with_face == inventory_rank),
            "membership and rank disagree")

    # ---- the FULL space of admissible extensions ------------------------
    # D = {Psi : Psi.J = 0} ; the extensions of psi_z are those with
    # Psi(balanced_face) = 4 (equivalently nonzero, then normalize).
    kernel = left_kernel(columns)
    detecting = [psi for psi in kernel if dot(psi, balanced_face) != 0]
    require(bool(detecting) == (not face_in_image),
            "detector existence disagrees with membership")

    # canonical primitive representative of the extension space
    canonical = None
    if detecting:
        base = detecting[0]
        canonical = primitive(scale(Q(4) / dot(base, balanced_face), base))
        require(all(dot(canonical, column) == 0 for column in columns)
                and dot(canonical, balanced_face) != 0,
                "the canonical extension failed its own test")

    # dimension of the extension space (affine): dim ker - 1
    extension_affine_dimension = len(kernel) - 1 if detecting else None

    # the residual freedom, and what removes it: the literal q=M-ainc row is
    # itself a covector annihilating the whole admissible q family, so it is a
    # trivial direction of the extension space.  Adjoining it as a ROW (i.e.
    # imposing q=M-ainc on the terminal) makes the extension exactly unique.
    q_identity_covector = vec(M=1, ainc=-1, q=-1)
    require(all(dot(q_identity_covector, column) == 0 for column in columns),
            "the q=M-ainc covector stopped annihilating the inventory")
    trivial = [q_identity_covector, vec(W_global=1), vec(common_tail_escape=1)]
    linear_part = [psi for psi in kernel if dot(psi, balanced_face) == 0]
    require(rank(linear_part) == rank(trivial) == 3
            and all(in_span(trivial, psi) for psi in linear_part),
            ("the residual freedom is not exactly the three trivial "
             "directions", [{LABELS[i]: str(v) for i, v in enumerate(psi) if v}
                            for psi in linear_part]))
    unique_modulo = {
        "residual_freedom": [
            {LABELS[i]: str(v) for i, v in enumerate(psi) if v}
            for psi in linear_part],
        "residual_freedom_dimension": rank(linear_part),
        "identified_as": [
            "the literal q=M-ainc identity covector (it annihilates every "
            "admissible q column by definition)",
            "W_global: a guard row carrying no committed column",
            "common_tail_escape: a guard row carrying no committed column",
        ],
        "q_identity_covector_annihilates_inventory": True,
        "extension_unique_modulo_the_three_trivial_directions": True,
    }

    # ---- exhaustion over the uncommitted families -----------------------
    uncommitted = {}
    for family, (support, description) in UNCOMMITTED_SUPPORTS.items():
        basis = [vec(**{label: 1}) for label in support]
        # can ANY column supported on this family fill the class?
        fills = [label for label, column in zip(support, basis, strict=True)
                 if not all(dot(psi, column) == 0 for psi in detecting)]
        # equivalently: does adjoining the WHOLE subspace fill the face?
        whole = in_span(columns + basis, balanced_face)
        uncommitted[family] = {
            "support_rows": support,
            "description": description,
            "any_column_in_this_family_can_fill": bool(fills) or whole,
            "rows_that_would_matter": fills,
            "balanced_face_in_span_after_adjoining_whole_subspace": whole,
        }

    # ---- the structural theorem behind the verdict -----------------------
    # Every committed column satisfies <delta, c_B> = <delta, c_Eq>.  That
    # single law is what keeps the class alive, and it is checked column by
    # column here rather than asserted.
    law = []
    for name, kind, value in inventory:
        b_value = dot(Z, square_projection(value))
        eq_value = dot(Z, tuple(value[INDEX[f"Eq{c}"]] for c in range(4)))
        law.append({"column": name, "delta_dot_B": str(b_value),
                    "delta_dot_Eq": str(eq_value), "law_holds": b_value == eq_value})
    require(all(entry["law_holds"] for entry in law),
            ("the B/Eq law failed", [e for e in law if not e["law_holds"]]))
    b_eq_law = {
        "statement": (
            "every column of the exhaustive inventory satisfies "
            "<delta, c_B> = <delta, c_Eq>"),
        "verified_column_by_column": True,
        "columns_checked": len(law),
        "why_it_holds": (
            "the only committed columns with nonzero B block are r0_j "
            "(B=e_j, Eq=e_j) and M_v (B=alpha, Eq=alpha), which tie B to Eq "
            "identically; and the four K2,2 companion columns, whose B block "
            "is a signless bipartite edge and therefore already has gauged "
            "augmentation zero.  Every other column has B=Eq=0"),
        "consequence": (
            "Psi = sum_j delta_j (B_j - Eq_j) annihilates the entire "
            "inventory while reading the balanced face as 4"),
    }

    # ---- what a filler MUST look like -----------------------------------
    # c fills iff Psi(c) is a nonzero constant over the whole extension
    # affine space, i.e. c is NOT annihilated by the linear part.
    # The unambiguous test: c fills iff the balanced face enters the span
    # after adjoining c.  Applied to every ambient row selector.
    filler_rows = [label for label in LABELS
                   if in_span(columns + [vec(**{label: 1})], balanced_face)]

    # ---- cross-frontier convergence -------------------------------------
    # verify_h3_shared_loop_full_augmented_membership_dual.py, from a
    # completely different frontier (the Gate-I shared-loop repairs, six-label
    # grade), reaches its own sharp frontier: "one new relative column must
    # carry Eq=-u and physical ainc=+1 with every other listed row zero".
    # Transport that prescription here with u=delta.  ainc is accompanied by
    # q=-ainc so that the literal q=M-ainc row is respected.
    convergent = vec(**{f"Eq{c}": -Z[c] for c in range(4)}, ainc=1, q=-1)
    convergent_pure_eq = vec(**{f"Eq{c}": -Z[c] for c in range(4)})
    cross_frontier = {
        "source": ("computations/verify_h3_shared_loop_full_augmented_"
                   "membership_dual.py, docstring line 26 and ledger "
                   "'sharp_frontier'"),
        "quoted_prescription": (
            "one new relative column must carry Eq=-u and physical ainc=+1 "
            "with every other listed row zero"),
        "transported_column_u_equals_delta": {
            LABELS[i]: str(v) for i, v in enumerate(convergent) if v},
        "pairing_with_canonical_psi": (
            str(dot(canonical, convergent)) if canonical else None),
        "fills_the_balanced_class": in_span(
            columns + [convergent], balanced_face),
        "pure_Eq_part_alone_fills": in_span(
            columns + [convergent_pure_eq], balanced_face),
        "verdict": (
            "the SAME missing column closes both frontiers.  The shared-loop "
            "Gate-I repair problem and the balanced chart square are blocked "
            "by one datum: a source-valid column carrying an unbalanced "
            "reduced-Eq readout with no matching literal/B content"),
    }
    require(cross_frontier["fills_the_balanced_class"]
            and cross_frontier["pure_Eq_part_alone_fills"],
            ("the shared-loop prescription did not fill the balanced class",
             cross_frontier))

    ledger = {
        "probe": "TASK A: exhaustive same-grade inventory versus psi_z",
        "pinned_head": common.PINNED_HEAD,
        "chart_basis_conventions_reproduced": conventions,
        "ambient": {"labels": list(LABELS), "dimension": len(LABELS)},
        "inventory_size": len(inventory),
        "inventory_rank": inventory_rank,
        "rank_after_adjoining_balanced_face": rank_with_face,
        "balanced_face_in_image": face_in_image,
        "per_column": per_column,
        "bare_cone_criterion_summary": {
            "columns_with_nonzero_gauged_augmentation": [
                entry["column"] for entry in per_column
                if entry["bare_cone_criterion_met"]],
            "warning": (
                "these columns satisfy the note's BARE square cone criterion "
                "but do NOT fill the class, because they carry further rows "
                "in the same grade.  The bare criterion is necessary only "
                "for a column that lives in the square alone"),
        },
        "augmented_criterion": {
            "columns_with_nonzero_plain_psi_pairing": [
                entry["column"] for entry in per_column
                if entry["pairing_with_plain_psi"] != "0"],
            "columns_with_nonzero_pure_safe_psi_pairing": [
                entry["column"] for entry in per_column
                if entry["pairing_with_pure_safe_psi"] != "0"],
        },
        "extension_space": {
            "left_kernel_dimension": len(kernel),
            "detecting_directions": len(detecting),
            "affine_dimension_of_psi_z_extensions": extension_affine_dimension,
            "canonical_primitive_extension": (
                {LABELS[i]: int(v) for i, v in enumerate(canonical) if v}
                if canonical else None),
            "canonical_value_on_balanced_face": (
                str(dot(canonical, balanced_face)) if canonical else None),
            "canonical_value_on_target_companion": (
                str(dot(canonical, target_companion)) if canonical else None),
        },
        "B_Eq_law": b_eq_law,
        "guard_rows_with_no_committed_column": guard_rows_with_no_column(),
        "residual_freedom_and_q_identity": unique_modulo,
        "q_identity_violating_columns_excluded": [
            {"column": name, "provenance": kind}
            for name, kind, _v in q_identity_violating_columns()],
        "cross_frontier_convergence": cross_frontier,
        "uncommitted_family_exhaustion": uncommitted,
        "filler_characterization": {
            "rows_a_filler_must_touch": filler_rows,
            "statement": (
                "a same-grade physical column c fills the balanced class iff "
                "Psi(c) != 0 for every admissible extension Psi, equivalently "
                "iff c has nonzero component along one of the listed rows "
                "modulo the inventory span"),
        },
    }
    return ledger, inventory, columns, balanced_face, detecting, kernel


def main():
    ledger, *_ = exhaust()
    (common.OUT / "out_a.json").write_text(json.dumps(ledger, indent=1))
    print("TASK A: exhaustive same-grade inventory versus psi_z")
    print(f"  chart-basis conventions reproduced EXACTLY: "
          f"rank-3 mate rows, unique annihilator z, gauged aug(z)=4")
    print(f"  inventory columns: {ledger['inventory_size']}   "
          f"rank {ledger['inventory_rank']} -> "
          f"{ledger['rank_after_adjoining_balanced_face']} with the face")
    print(f"  balanced face in the image: {ledger['balanced_face_in_image']}")
    print("  bare-square cone criterion met by: "
          + ", ".join(ledger["bare_cone_criterion_summary"][
              "columns_with_nonzero_gauged_augmentation"]))
    print("  nonzero pairing with the plain psi: "
          + str(ledger["augmented_criterion"][
              "columns_with_nonzero_plain_psi_pairing"]))
    print("  nonzero pairing with the pure-safe psi: "
          + str(ledger["augmented_criterion"][
              "columns_with_nonzero_pure_safe_psi_pairing"]))
    print(f"  psi_z extension affine dimension: "
          f"{ledger['extension_space']['affine_dimension_of_psi_z_extensions']}")
    print("  canonical extension: "
          + str(ledger["extension_space"]["canonical_primitive_extension"]))
    print("  rows a filler must touch: "
          + str(ledger["filler_characterization"]["rows_a_filler_must_touch"]))
    cf = ledger["cross_frontier_convergence"]
    print("  CROSS-FRONTIER: the shared-loop gate's own prescribed missing "
          "column (Eq=-u, ainc=+1)")
    print(f"    transported with u=delta -> fills the balanced class: "
          f"{cf['fills_the_balanced_class']} "
          f"(canonical psi pairing {cf['pairing_with_canonical_psi']})")
    for family, entry in ledger["uncommitted_family_exhaustion"].items():
        print(f"  {family:<34s} can fill: "
              f"{entry['any_column_in_this_family_can_fill']}")


if __name__ == "__main__":
    main()
