#!/usr/bin/env python3
"""Resolve the P2-hidden/K_Eq/d_even circularity at the E14 D4 top.

The four codimension-one faces of the oriented D4 Boolean cell have signs
``(-1,+1,-1,+1)=D_root``.  This is exactly the root-word sign packet needed
by the C-plus physical dressing.  It is not yet the physical hidden packet:
one still needs the source-labelled face map sending each marked D3
occurrence to ``-(B1+B4)=-2*d_even`` in the repeated P3+K2 grade.

If the *same* pointed AugP2 section also sends the two normalized face-3/5
cap graphs to the labels B4 and B1, the apparent dependency cycle becomes
a finite transfer equation.  In the sign convention

    K=A+X+L*d,  z=C-K,  d=F*z,

one has ``(I+L*F)K=A+X+L*F*C``.  On the six-label alternating root sector,
``L=2*D_root tensor -`` and the normalized character retraction is
``F=D_root^t/8 tensor I``.  Hence ``L*F`` is a rank-six projector and
``det(I+L*F)=2^6``.  Thus the cycle is nonsingular over Q, but solving it
divides the alternating packet by two.  A desired integral/source-normalized
packet is obtained only when the right side has the corresponding evenness.
The coarse root-sum quotient instead produces a square-zero transfer and
cannot decide the complete labelled problem.

Thus there is no rational linear-algebra circularity.  Its remaining inputs
are the pointed source-labelled D3/cap occurrence-to-B1/B4 map and the
normalization/evenness of the actual augmented right side.  The orbit D4
theorem supplies its signs and top occurrence, but does not yet supply this
label map, factor two, or physical fine grade.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py":
        "42bf68eeb963d568d1c8d9156d4176bec31a114b6fe804744833364fe3633475",
    "notes/h3-e14-cap-graph-two-parameter-flat-transport-gate.md":
        "61c093eed30cd2fff1be086e6069d344e76a583ee31f93528a31aebe76c5c5d6",
    "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
    "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py":
        "e8014fdfd2263a8eb6bffff11e31c339b5b7965989a61324f8d118a91f791f46",
    "notes/h3-cplus-conditional-physical-dressing-assembly.md":
        "b3afd746e6c275ca23e0b3ee5f26dfbc763301ed7371be4377612709904c19c0",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_centered_base_denominator_deven_composition_gate.py":
        "ee8952a30b9d1a583f3d0e78b8289e5ed839d399d0865b0457315c969c117291",
    "notes/h3-centered-base-denominator-deven-composition-gate.md":
        "5a191c3f7cb9fb9da1d74d5d17f6455f8978a1622f697f7b13325a0541a05a3f",
    "computations/verify_h3_e14_keq_private_placement_residue_identification_gate.py":
        "89b0b694b525dba502314e61922cb884ef6ddd2f14fea68b3bafd5215aa40c70",
    "notes/h3-e14-keq-private-placement-residue-identification-gate.md":
        "36828d8503d929427eef55886cb68cbfe7c2431649c38382907835365bd5ed38",
}
EXPECTED_LEDGER_SHA256 = (
    "787eed809e29aa4284e09ac16a910721a86bc99be8823671f9eb51549bc9f0e2"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def matmul(left: tuple[tuple[Q, ...], ...],
           right: tuple[tuple[Q, ...], ...]) -> tuple[tuple[Q, ...], ...]:
    require(left and right and len(left[0]) == len(right),
            ("matrix product width", len(left[0]), len(right)))
    return tuple(tuple(sum((left_value * right[row][column]
                            for row, left_value in enumerate(left_line)),
                           Q(0))
                       for column in range(len(right[0])))
                 for left_line in left)


def matrix_add(left: tuple[tuple[Q, ...], ...],
               right: tuple[tuple[Q, ...], ...]) -> tuple[tuple[Q, ...], ...]:
    require(len(left) == len(right)
            and all(len(a) == len(b) for a, b in zip(left, right, strict=True)),
            "matrix add width")
    return tuple(tuple(a + b for a, b in zip(left_line, right_line, strict=True))
                 for left_line, right_line in zip(left, right, strict=True))


def matrix_scale(coefficient: Q,
                 matrix: tuple[tuple[Q, ...], ...]) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(coefficient * value for value in row) for row in matrix)


def identity(size: int) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(Q(row == column) for column in range(size))
                 for row in range(size))


def matrix_rank(matrix: tuple[tuple[Q, ...], ...]) -> int:
    # rank() expects columns rather than rows.
    return rank(tuple(tuple(matrix[row][column] for row in range(len(matrix)))
                      for column in range(len(matrix[0]))))


def determinant(matrix: tuple[tuple[Q, ...], ...]) -> Q:
    require(matrix and len(matrix) == len(matrix[0]), "determinant square")
    work = [list(row) for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, len(work)):
            value = work[row][column]
            if not value:
                continue
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return answer


def d4_last_boundary_signs() -> dict[str, object]:
    top = (0, 1, 2, 3)
    faces3 = tuple(combinations(top, 3))
    signs = []
    records = []
    for face in faces3:
        missing = next(direction for direction in top if direction not in face)
        position = tuple(sorted(face + (missing,))).index(missing)
        sign = (-1) ** position
        signs.append(Q(sign))
        records.append({
            "D3_face": list(face),
            "missing_root_index": missing,
            "boundary_sign_to_D4_top": sign,
        })
    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    require(tuple(signs) == d_root and sum(signs, Q(0)) == 0,
            ("the D4 last-boundary sign packet changed", records))
    return {
        "D3_face_order": [list(face) for face in faces3],
        "records": records,
        "oriented_last_boundary": [str(value) for value in signs],
        "D_root": [str(value) for value in d_root],
        "signs_equal_D_root": True,
        "aggregate_sign": 0,
    }


def label_and_factor_gate() -> dict[str, object]:
    # v=(B1+B4)/2, so the hidden face -E=-2D_root tensor v is obtained from
    # the D4 sign packet precisely if each D3 marked occurrence maps to
    # -(B1+B4).  The orbit theorem transports the occurrence tag with
    # coefficient one; it does not construct that two-label map.
    v = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    two_v = tuple(2 * entry for entry in v)
    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    e = tuple(2 * root * label for root in d_root for label in v)
    labelled_d3 = tuple(root * label for root in d_root
                        for label in tuple(-entry for entry in two_v))
    require(two_v == tuple(map(Q, (0, 1, 0, 0, 1, 0)))
            and labelled_d3 == tuple(-entry for entry in e)
            and sum(value != 0 for value in e) == 8,
            "the D3/B1-B4 hidden packet changed")

    orbit = load(
        "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py",
        "simultaneous_orbit",
    )
    orbit_ledger, orbit_digest = orbit.audit()
    require(orbit_digest == orbit.EXPECTED_LEDGER_SHA256,
            "the orbit D4 ledger changed")
    occurrence = orbit_ledger["marked_occurrence_local_system"]
    require(occurrence["root_transport_on_occurrence_tags"]
                == "identity with coefficient 1"
            and occurrence["formal_D4_of_c_f"] == "c_g"
            and not occurrence["bottom_same_grade_centered_cell_constructed"],
            ("the D4 occurrence scope changed", occurrence))
    return {
        "v_B0_to_B5": [str(value) for value in v],
        "two_v": [str(value) for value in two_v],
        "E": "2 D_root tensor v",
        "required_hidden": "-E",
        "required_D3_label_map": (
            "each marked D3 occurrence -> -(B1+B4)=-2v"
        ),
        "D4_orbit_supplies_signs": True,
        "D4_orbit_supplies_top_R": True,
        "D4_orbit_supplies_required_B1_B4_label_map": False,
        "D4_orbit_supplies_factor_two_and_P3K2_normalization": False,
        "physical_P2_hidden_from_current_D4_theorem": False,
        "conditional_image_after_label_map": "-2 D_root tensor v=-E",
    }


def simultaneous_rank_and_dependency_audit() -> dict[str, object]:
    # First quotient: (root lower, root Eq, root labelled ores), in units E.
    hidden = (Q(-1), Q(0), Q(0))
    old_o = (Q(1), Q(1), Q(-1))
    rooted_deven = (Q(0), Q(0), Q(1))
    clean = (Q(0), Q(1), Q(0))
    section_total = tuple(a + b for a, b in
                          zip(hidden, rooted_deven, strict=True))
    assembled = tuple(a + b for a, b in
                      zip(section_total, old_o, strict=True))
    require(assembled == clean
            and rank((hidden, old_o, rooted_deven)) == 3
            and rank((section_total, old_o)) == 2,
            "the simultaneous clean-K_Eq rank identity changed")

    # Add the private top R.  One new pointed section simultaneously carries
    # top R, hidden lower -E, and rooted labelled residue +E.  O_-E then
    # completes it to the full (R,E) comparison column.
    new_section = (Q(1), Q(-1), Q(0), Q(1))
    old_o_full = (Q(0), Q(1), Q(1), Q(-1))
    required_phi = (Q(1), Q(0), Q(1), Q(0))
    require(tuple(a + b for a, b in
                  zip(new_section, old_o_full, strict=True)) == required_phi
            and rank((new_section, old_o_full)) == 2,
            "the single-section Phi_orb assembly changed")

    # Omitting either derived face leaves a primitive coordinate debt.
    lower_dual = (Q(1), Q(0), Q(0))
    ores_dual = (Q(0), Q(0), Q(1))
    without_hidden = old_o
    without_deven = tuple(a + b for a, b in
                          zip(hidden, old_o, strict=True))
    require(sum(a * b for a, b in zip(lower_dual, without_hidden,
                                      strict=True)) == 1
            and sum(a * b for a, b in zip(ores_dual, without_deven,
                                          strict=True)) == -1,
            "the hidden/residue necessity pairings changed")
    return {
        "main_row_order": ["root lower/private", "root Eq", "root ores"],
        "P2_hidden": [-1, 0, 0],
        "old_O_minus_E": [1, 1, -1],
        "root_decorated_d_even": [0, 0, 1],
        "clean_K_Eq": [0, 1, 0],
        "unimodular_three_column_rank": 3,
        "one_new_section_faces_hidden_plus_deven": [-1, 0, 1],
        "rank_new_section_plus_old_O": 2,
        "full_row_order": ["private R", "root lower", "root Eq", "root ores"],
        "one_new_pointed_section": [1, -1, 0, 1],
        "old_O_full": [0, 1, 1, -1],
        "required_Phi_orb": [1, 0, 1, 0],
        "without_hidden_lower_dual_value": 1,
        "without_deven_ores_dual_value": -1,
    }


def noncircular_cap_rewrite_audit() -> dict[str, object]:
    # At either selected face, p=(-Q,-ores), n=(+Q,0), hence
    # z_cap=p+n=(0,-ores).  The cap graph transports z_cap as a whole.  The
    # face-3/5 label map can therefore define d_even from z_cap directly,
    # without first constructing n as a readout of the clean K_Eq being built.
    p = (Q(-1), Q(-1))
    n = (Q(1), Q(0))
    z_cap = tuple(a + b for a, b in zip(p, n, strict=True))
    require(z_cap == (Q(0), Q(-1)),
            "the p+n=z_cap identity changed")
    b1 = tuple(map(Q, (0, 1, 0, 0, 0, 0)))
    b4 = tuple(map(Q, (0, 0, 0, 0, 1, 0)))
    labelled_z3 = tuple(-entry for entry in b4)
    labelled_z5 = tuple(-entry for entry in b1)
    d_even = tuple(Q(-1, 2) * (left + right) for left, right in
                   zip(labelled_z3, labelled_z5, strict=True))
    expected = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    require(d_even == expected,
            "the direct labelled-zcap d_even formula changed")

    augmented = load(
        "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py",
        "simultaneous_augp2",
    )
    aug_ledger, aug_digest = augmented.audit()
    require(aug_digest == augmented.EXPECTED_LEDGER_SHA256,
            "the shortest AugP2 ledger changed")
    d_audit = aug_ledger["d_even_composition"]
    require(not d_audit["separate_d_even_hypothesis_after_these_faces"]
            and d_audit["formula"].startswith("d_even=-1/2"),
            ("the p+n+label d_even composition changed", d_audit))

    centered = load(
        "computations/verify_h3_centered_base_denominator_deven_composition_gate.py",
        "simultaneous_centered",
    ).audit()
    scope = centered["source_scope"]
    require(scope["invisible_n_status"].endswith(
                "physical n still requires the augmented K_Eq comparison")
            and scope["label_map_status"].endswith(
                "not a physical word/fine/repeated-grade chain map"),
            ("the old circular presentation scope changed", scope))
    return {
        "cap_coordinate_order": ["Q", "scalar ores"],
        "p": [-1, -1],
        "n": [1, 0],
        "z_cap_equals_p_plus_n": [0, -1],
        "direct_face3_label": "z_3 -> -B4",
        "direct_face5_label": "z_5 -> -B1",
        "direct_d_even_formula": "-1/2[(-B4)+(-B1)]=(B1+B4)/2",
        "d_even_requires_clean_K_Eq_after_zcap_rewrite": False,
        "old_p_plus_n_proof_looks_circular": True,
        "cycle_is_removed_if": (
            "the cap graph and its physical face-3/5 occurrence labels are "
            "part of the same pointed section, so z_cap is primitive input"
        ),
        "cycle_is_removed_by_current_physical_inventory": False,
        "reason": (
            "the old cap graph is only flat in the enriched tensor model; "
            "the direct z3/z5-to-B4/B1 source-labelled map is still missing"
        ),
    }


def coupled_transfer_matrix_audit() -> dict[str, object]:
    """Compute the feedback on the literal root x B-label quotient.

    The source-normalized rooted residue insertion is

        L(d)=2 D_root tensor d.

    The only D-character retraction which is a left inverse on this packet is

        F_D(x)_j=(1/8) sum_r D_root[r] x_(r,j).

    The factor 1/8 is the product of the alternating average 1/4 and the
    face-3/5 factor 1/2.  Consequently F_D L=I and L F_D is the projector
    onto the alternating root line, independently in each of the six B
    labels.  This is an exact rational computation.  It is conditional as a
    *physical* statement because the committed source inventory has not yet
    constructed F_D on arbitrary complete-row packets; it only fixes the
    selected face formula.

    For contrast, forgetting the root label by the average F_sum has
    F_sum L=0 since sum D_root=0.  Then L F_sum is square-zero.  That quotient
    is algebraically harmless but is precisely the coarse quotient which
    forgets the independent word-labelled residue rows.
    """
    roots = 4
    labels = 6
    width = roots * labels
    d_root = tuple(map(Q, (-1, 1, -1, 1)))

    # L: Q^6 -> Q^(4 x 6), with coordinates ordered root-major.
    insertion = tuple(tuple(
        2 * d_root[root] if label == source_label else Q(0)
        for source_label in range(labels)
    ) for root in range(roots) for label in range(labels))

    # F_D: Q^(4 x 6) -> Q^6, the normalized alternating retraction.
    alternating_face = tuple(tuple(
        d_root[root] / 8 if label == target_label else Q(0)
        for root in range(roots) for label in range(labels)
    ) for target_label in range(labels))

    f_l = matmul(alternating_face, insertion)
    transfer = matmul(insertion, alternating_face)
    id_labels = identity(labels)
    id_width = identity(width)
    require(f_l == id_labels,
            ("the normalized alternating face is no longer a retraction", f_l))
    require(matmul(transfer, transfer) == transfer
            and matrix_rank(transfer) == labels,
            "the alternating transfer stopped being a rank-six projector")

    coupled = matrix_add(id_width, transfer)
    coupled_inverse = matrix_add(id_width, matrix_scale(Q(-1, 2), transfer))
    require(matmul(coupled, coupled_inverse) == id_width
            and matmul(coupled_inverse, coupled) == id_width,
            "the coupled inverse I-P/2 changed")
    coupled_det = determinant(coupled)
    require(matrix_rank(coupled) == width and coupled_det == 2 ** labels,
            ("the coupled transfer determinant changed", coupled_det))

    # On every labelled alternating line, the full 24-dimensional equation
    # reduces to [2] K_D = RHS_D.  This is invertible over Q but is not a
    # unimodular integral/source-normalized operation.
    scalar_coupled = ((Q(2),),)
    require(determinant(scalar_coupled) == 2,
            "the one-label alternating transfer changed")

    # Coarse root average.  The normalization 1/4 is irrelevant to
    # square-zero-ness, but makes the root-trivial projection conventional.
    root_sum_face = tuple(tuple(
        Q(1, 4) if label == target_label else Q(0)
        for _root in range(roots) for label in range(labels)
    ) for target_label in range(labels))
    coarse_f_l = matmul(root_sum_face, insertion)
    coarse_transfer = matmul(insertion, root_sum_face)
    require(coarse_f_l == tuple(tuple(Q(0) for _ in range(labels))
                                for _ in range(labels))
            and matmul(coarse_transfer, coarse_transfer)
                == tuple(tuple(Q(0) for _ in range(width))
                         for _ in range(width))
            and matrix_rank(coarse_transfer) == labels,
            "the coarse root-sum transfer stopped being square-zero")
    coarse_coupled = matrix_add(id_width, coarse_transfer)
    require(determinant(coarse_coupled) == 1
            and matmul(coarse_coupled,
                       matrix_add(id_width, matrix_scale(-1, coarse_transfer)))
                == id_width,
            "the coarse square-zero transfer inverse changed")

    # Sign audit.  Starting from K=A+X+Ld and d=F(C-K), substitution gives
    # K=A+X+LFC-LFK, hence plus LFK on the left.  The opposite sign would
    # yield I-P and be singular on im L, so the cap/face orientation is
    # genuinely load-bearing.
    opposite = matrix_add(id_width, matrix_scale(-1, transfer))
    require(matrix_rank(opposite) == width - labels
            and determinant(opposite) == 0,
            "the opposite-sign singular guard changed")

    return {
        "equations": [
            "K=A+X+L d",
            "z=C-K",
            "d=F z",
            "(I+L F)K=A+X+L F C",
        ],
        "sign_audit": (
            "the plus sign follows because the K contribution to z is -K; "
            "moving -LF K from the right to the left gives +LF K"
        ),
        "literal_space": "Q^4_root tensor Q^6_(B0,...,B5)",
        "literal_dimension": width,
        "root_character": [str(value) for value in d_root],
        "L": "d -> 2 D_root tensor d",
        "F_D": "x_j -> (1/8) sum_r D_root[r] x_(r,j)",
        "F_D_L": "I_6",
        "L_F_D": "P_D tensor I_6",
        "transfer_rank": matrix_rank(transfer),
        "transfer_is_projector": True,
        "I_plus_transfer_rank": matrix_rank(coupled),
        "I_plus_transfer_determinant": int(coupled_det),
        "I_plus_transfer_inverse": "I-(1/2)P_D tensor I_6",
        "alternating_one_label_equation": "2 K_D=RHS_D",
        "rational_circularity": False,
        "integral_or_source_normalization_guard": (
            "RHS_D must be twice the desired normalized K_D; otherwise the "
            "unique rational solution has a new factor 1/2"
        ),
        "opposite_face_orientation": {
            "operator": "I-LF_D",
            "rank": matrix_rank(opposite),
            "determinant": 0,
            "kernel": "the six labelled D_root lines",
        },
        "coarse_root_sum_comparison": {
            "F_sum_L": "0 because sum(D_root)=0",
            "rank_L_F_sum": matrix_rank(coarse_transfer),
            "square_zero": True,
            "det_I_plus_L_F_sum": 1,
            "why_not_decisive": (
                "F_sum forgets the four word-labelled residue copies, the "
                "very protected rows required by the complete problem"
            ),
        },
        "physical_scope": (
            "the matrix calculation is exact after choosing the normalized "
            "D-character face retraction.  Existing commitments prove the "
            "selected z3/z5 coefficient formula but not a complete source-"
            "valid F_D on arbitrary 24-row packets, nor the evenness of the "
            "actual A+X+LFC packet"
        ),
    }


def shifted_ridge_and_dependency_graph() -> dict[str, object]:
    flat = load(
        "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py",
        "simultaneous_flat",
    )
    flat_ledger, flat_digest = flat.audit()
    require(flat_digest == flat.EXPECTED_LEDGER_SHA256,
            "the flat cap/central-incidence ledger changed")
    ridge = flat_ledger["shifted_Kahler_connection"]
    require(ridge["connection_one_face"] == "-d(q_xv^01) when root site i=v"
            and ridge["mixed_root_curvature"] == 0
            and ridge["terminal_readouts_preserved"]
            and not ridge["physical_shifted_connection_face_constructed"],
            ("the shifted ridge dependency changed", ridge))
    return {
        "existing_inputs": [
            "moving-target Boolean D4 cube and marked top R",
            "old physical O_-E column",
            "old unary U with T12=U+R",
            "normalized abstract cap graph z_cap",
            "matching-Bianchi coefficient label formulas",
        ],
        "one_independent_positive_input": (
            "one pointed source-labelled AugP2 orbit/cap section L whose "
            "D3 boundary maps to -(B1+B4), whose face-3/5 cap restrictions "
            "map z3,z5 to -B4,-B1, and whose top maps to R"
        ),
        "derived_in_order": [
            "P2_hidden=-E and d_even=v from two faces of L",
            "clean K_Eq=L_hidden+O_-E+root(d_even)",
            "Phi_orb=(R,E)",
            "T12 closure from old U+R",
        ],
        "dependency_cycle_after_zcap_rewrite": False,
        "shifted_ridge_connection": "-d(q_xv^01) at i=v",
        "shifted_ridge_curvature": 0,
        "shifted_ridge_terminal_dark": True,
        "shifted_ridge_physical_placement_is_part_of_L": True,
        "physical_q": (
            "after L is physically typed, use the existing transport-versus-"
            "relative-generator defect alternative"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14 D4/P2/K_Eq/d_even simultaneous totalization gate",
        "pins": PINS,
        "D4_last_boundary": d4_last_boundary_signs(),
        "physical_label_and_normalization_gate": label_and_factor_gate(),
        "simultaneous_rank_identity": simultaneous_rank_and_dependency_audit(),
        "noncircular_cap_rewrite": noncircular_cap_rewrite_audit(),
        "coupled_transfer_matrix": coupled_transfer_matrix_audit(),
        "ridge_and_dependency_graph": shifted_ridge_and_dependency_graph(),
        "verdict": (
            "The D4 last-boundary signs are exactly D_root, but the committed "
            "orbit theorem does not yet give P2_hidden=-E: it lacks the "
            "physical map D3 occurrence -> -(B1+B4), its factor two, and its "
            "P3+K2 normalization.  Conditional on one pointed AugP2 section "
            "supplying that map and the face-3/5 labelled cap graphs, the "
            "coupled equations have transfer LF=P_D tensor I_6, so I+LF "
            "has rank 24 and determinant 64.  There is no rational linear-"
            "algebra circularity, but the alternating packet is divided by "
            "two: source normalization requires the actual augmented right "
            "side to be even.  This and the literal F_D section are not yet "
            "proved.  The same section must carry the flat, terminal-dark "
            "shifted ridge connection and physical q comparison."
        ),
        "scope": (
            "canonical h=3 silent E14/root-even packet.  The sign, rank, and "
            "dependency and rational transfer statements are exact.  This "
            "proves a conditional construction criterion, not existence of "
            "its literal source-labelled occurrence/cap-to-B map or the "
            "needed even normalization of its augmented right side."
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
    _ledger, digest = audit()
    print("D4 last-boundary signs: (-1,+1,-1,+1)=D_root")
    print("current D4 gives physical P2_hidden=-E: NO (LABEL MAP MISSING)")
    print("D-character transfer: rank(LF)=6, det(I+LF)=64")
    print("rational circularity: NO; normalization/evenness guard: OPEN")
    print("section (R,-E,0,+E) + O_-E = Phi_orb (R,0,+E,0)")
    print("d_even comes from labelled z_cap=p+n; clean K_Eq not prerequisite")
    print("shifted ridge: flat terminal-dark connection, physical grade open")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
