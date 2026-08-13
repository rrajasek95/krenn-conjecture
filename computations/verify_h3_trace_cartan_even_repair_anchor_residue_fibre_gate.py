#!/usr/bin/env python3
"""Resolve the coarse tau_plus defect up to one labelled residue section.

Let v=(B1+B4)/2.  The negative reduced companion from the denominator-Tor
route has the correct lower tail and positive ordinary residue.  If a
same-grade pure labelled-residue section d_v exists, the physical cap and
split-residue cone gives

    (-A_v) + T_v + rho_v - 2 d_v
        = (lower=v, target=v, ainc=0, ores=0).

The required pure r0 image differs by only ainc=-1.  The already proved
anchor-fibre Fredholm alternative therefore turns this into either a
relative generator (ainc is nonzero on the protected kernel) or the physical
anchor separator (ainc vanishes there).

This is conditional for a sharp reason.  The committed scalar residue lift
and physical Cartan residue line span only <1,c>, where
c=(1,0,1,-1,0,-1).  The primitive covector
chi=(0,1,-1,0,1,-1) kills both and reads 1 on v.  Hence the cone needs a new
rho-even labelled residue section in the B1/B4 grades; the Cartan cell cannot
replace it.  The later literal M_v cap-Cartan theorem closes the old
output-terminal packet but has zero target/anchor/residue here and supplies
no such section.

The checker also sharpens the weighted denominator condition.  Nonconstant
h is not sufficient for either fixed selected projection: the direct and
rho-even choices impose h3+h5=0 and 2h3+h2+h5=0 respectively.  Both loci are
nonempty on the normalized C5 coefficient chart, but full denominator
membership and physical inactivity remain separate requirements.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py":
        "673b30ac4b68c8a3af42e9c0803b3d5a39796b366b3ac15b5fd8b31b02d8df5d",
    "computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py":
        "ee04e571ccd6eba9bac1bfbd9233a0d2adeb30c275e4156adefe75570c8911e6",
    "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py":
        "96280ef01c70b4f3381e6d85d2c9fb64b1620850305a4346601fccbd7d63dc44",
    "computations/verify_h3_rootless_c5_clean_aggregate_tor_separator.py":
        "3b5cb07412f08eaea2492d4b4f981ecc5618053c211942bead0512b30393ce67",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/unaudited-gate1-phi-probe-2026-08-12/REPORT.md":
        "998d0e40cc66b4e75623cab05b94a18c55e7bb3fdcef2370d149462b4dbd5e90",
}
EXPECTED_LEDGER_SHA256 = (
    "7c869d6660a62bcdb6e2874d848b82fb6f0c2b5fc1540435dbd3583d9d4b9fc5"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    return tuple(sum(Q(vector[index]) for vector in vectors)
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left, right):
    return sum(Q(a) * Q(b) for a, b in zip(left, right, strict=True))


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def face_hafnians(chords):
    """Five normalized C5 four-site hafnians in face order 1,...,5."""
    x13, x14, x24, x25, x35 = map(Q, chords)
    return (
        1 + x24 * x35 + x25,
        1 + x13 + x14 * x35,
        1 + x14 * x25 + x24,
        1 + x35 + x13 * x25,
        1 + x13 * x24 + x14,
    )


def vector(anchor, *, lower=None, ainc=0, w=None, target=None, ores=None):
    return anchor.vector(
        lower=(Q(0),) * 6 if lower is None else lower,
        ainc=Q(ainc),
        w=(Q(0),) * 6 if w is None else w,
        target=(Q(0),) * 6 if target is None else target,
        ores=(Q(0),) * 6 if ores is None else ores,
    )


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    even = load(
        "computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py",
        "even_anchor_residue_denominator",
    )
    anchor = load(
        "computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py",
        "even_anchor_residue_fibre",
    )
    scope = load(
        "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py",
        "even_anchor_residue_scope",
    )
    clean = load(
        "computations/verify_h3_rootless_c5_clean_aggregate_tor_separator.py",
        "even_anchor_residue_clean",
    )
    mv = load(
        "computations/verify_h3_literal_mv_cap_cartan_composition.py",
        "even_anchor_residue_mv",
    )

    even_ledger, even_digest = even.audit()
    require(even_digest == even.EXPECTED_LEDGER_SHA256,
            "the denominator even-repair theorem changed")
    require(even_ledger["protected_signature_obstruction"]["remaining_defect"]
            == [0, 1, -1, -1],
            "the coarse target/anchor/residue residual changed")

    # Work in the six target labels B0,...,B5.  Conditional on lifting the
    # scalar residue of -A to the same labelled direction v, the cap/rho/pure
    # residue cone cancels the complete residual except for physical anchor.
    zero = (Q(0),) * 6
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    require(sum(v) == 1, "the even B1/B4 direction lost augmentation one")

    minus_a = vector(anchor, lower=v, ores=v)
    cap = vector(anchor, w=scale(-1, v), target=v)
    split_residue = vector(anchor, w=v, ores=v)
    pure_residue = vector(anchor, ores=v)
    cone = add(cap, split_residue, scale(-2, pure_residue))
    near_hit = add(minus_a, cone)
    required_r0 = vector(anchor, lower=v, ainc=-1, target=v)
    anchor_defect = add(required_r0, scale(-1, near_hit))
    require(cone == vector(anchor, target=v, ores=scale(-1, v))
            and near_hit == vector(anchor, lower=v, target=v)
            and anchor_defect == vector(anchor, ainc=-1),
            "the exact cap/rho/residue cone identity changed")

    # Replay that the already proved fibre alternative is componentwise, not
    # restricted to the four candidates printed by its application ledger.
    x_v = add(required_r0, scale(-1, cap),
              scale(-1, split_residue), pure_residue)
    residual = add(required_r0, scale(-1, minus_a))
    proposed_coarse_piece = add(required_r0, scale(-1, x_v),
                                scale(-1, pure_residue))
    require(x_v == vector(anchor, lower=v, ainc=-1)
            and add(vector(anchor, lower=v), scale(-1, x_v))
                == vector(anchor, ainc=1)
            and proposed_coarse_piece == cone
            and residual == add(proposed_coarse_piece,
                                vector(anchor, ainc=-1)),
            "the componentwise anchor-fibre identity failed on the even line")
    anchor_ledger, anchor_digest = anchor.audit()
    require(anchor_digest == anchor.EXPECTED_LEDGER_SHA256
            and "relative generator" in anchor_ledger["sharp_alternative"]
                ["nonzero_q_on_kernel"]
            and "physical left separator" in anchor_ledger["sharp_alternative"]
                ["q_zero_on_kernel"],
            "the generator/separator terminal changed")

    # Exact first obstruction.  The committed scalar section can at most be
    # lifted diagonally and the physical Cartan adds the endpoint-odd line.
    # Neither reaches v; chi is a primitive label-residue separator.
    diagonal = (Q(1),) * 6
    cartan_line = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    chi = (Q(0), Q(1), Q(-1), Q(0), Q(1), Q(-1))
    require(rank((diagonal, cartan_line)) == 2
            and rank((diagonal, cartan_line, v)) == 3
            and dot(chi, diagonal) == dot(chi, cartan_line) == 0
            and dot(chi, v) == 1
            and dot(chi, scale(-2, v)) == -2,
            "the primitive even labelled-residue obstruction changed")
    # The dependency is content-pinned above.  Avoid replaying its expensive
    # complete-row census in every mode; its frozen theorem and literal source
    # sentence are enough to guard the scoped negative fact used here.
    scope_source = (ROOT / "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py").read_text()
    require(scope.EXPECTED_LEDGER_SHA256
            == "bdad46b583b0fcab4065314bf8bb957bd79b5b502e2e76680d438519857b671a"
            and '"six_multiplier_label_section_constructed": False'
                in scope_source,
            "a committed labelled pure-residue section appeared")

    # The unaudited probe's output-side conclusion is superseded: the literal
    # M_v theorem carries the full terminal packet.  But that exact composite
    # has zero target/anchor/ordinary residue, so it cannot change the present
    # coarse residual and does not supply a B1/B4-labelled residue section.
    report = (ROOT / "computations/unaudited-gate1-phi-probe-2026-08-12/REPORT.md").read_text()
    require("What persists is purely terminal" in report
            and "Do not cite on the spine" in report,
            "the unaudited Gate-I report changed status")
    mv_ledger, mv_digest = mv.audit()
    require(mv_digest == mv.EXPECTED_LEDGER_SHA256,
            "the literal M_v theorem changed")
    mv_exact = mv_ledger["composition"]["M_v_equals_minus_O_plus_K"]
    require(mv_exact["ordinary_residue"] == [0, 0, 0, 0]
            and mv_exact["D_W_target_ainc"] == [0, 0, 0, 0]
            and mv_exact["eta_z"] == "1+delta_(vz)*u_z/t"
            and mv_exact["sigma"] == "-q_pq^22",
            "the literal output-side terminal closure changed")

    # Weighted reset-word conditions for the two exact selected projections.
    y = (Q(0), Q(0), Q(1, 2), Q(0), Q(1, 2))
    y_even = (Q(0), Q(1, 4), Q(1, 2), Q(0), Q(1, 4))
    h_clean = (Q(1),) * 5
    h_generic_nonconstant = (Q(1), Q(2), Q(3), Q(4), Q(5))
    require(dot(h_clean, y) == dot(h_clean, y_even) == 1
            and dot(h_generic_nonconstant, y) != 0
            and dot(h_generic_nonconstant, y_even) != 0,
            "nonconstancy accidentally became sufficient")

    # Both fixed hyperplanes are genuinely nonempty in the normalized C5
    # coefficient chart.  Set all chords except 14 to zero.  The five face
    # hafnians are (1,1,1,1,1+x14), so x14=-2 realizes the direct equation
    # and x14=-4 realizes the rho-even equation.
    direct_chords = (Q(0), Q(-2), Q(0), Q(0), Q(0))
    even_chords = (Q(0), Q(-4), Q(0), Q(0), Q(0))
    h_direct = face_hafnians(direct_chords)
    h_even = face_hafnians(even_chords)
    require(h_direct == (1, 1, 1, 1, -1)
            and dot(h_direct, y) == 0
            and h_even == (1, 1, 1, 1, -3)
            and dot(h_even, y_even) == 0,
            "the off-clean weighted loci changed")

    # If y were allowed to vary, nonconstant h would permit an aggregate-one
    # solution after localizing at h_i-h_j.  Here y and y_even are locked by
    # the B1/B4 tail routing, so their two displayed equations are the exact
    # necessary conditions.  Even on those loci, h.y=0 is only one row of the
    # full selected-column membership problem.
    h_i, h_j = Q(2), Q(5)
    flexible_two_face_y = (-h_j / (h_i - h_j), h_i / (h_i - h_j))
    require(sum(flexible_two_face_y) == 1
            and dot((h_i, h_j), flexible_two_face_y) == 0,
            "the localized variable-y observation changed")
    _clean_trans, clean_records = clean.coordinate_separator()
    require(sum(record["m_word_coordinate_kind"] == "selected_h_v"
                for record in clean_records) == 5,
            "the literal reset-word row changed")

    ledger = {
        "theorem": "tau_plus even repair anchor/residue fibre gate",
        "pins": PINS,
        "pinned_commits": {
            "even_denominator_tail": "73ee225",
            "anchor_fibre_alternative": "8e1f858",
            "labelled_residue_scope": "e5eb1fe",
            "literal_Mv_output_terminal": "271df91",
        },
        "even_direction": {
            "target_labels": ["B0", "B1", "B2", "B3", "B4", "B5"],
            "v": [str(entry) for entry in v],
            "face3_multiplier34_output": "B4",
            "face5_multiplier45_output": "B1",
            "rho_parity": "even",
        },
        "conditional_construction": {
            "minus_A": "(lower,ainc,W,target,ores)=(v,0,0,0,v)",
            "same_grade_cone": "T_v+rho_v-2*d_v",
            "cone_signature": "(0,0,0,v,-v)",
            "near_hit": "minus_A+cone=(v,0,0,v,0)",
            "required_r0": "(v,-1,0,v,0)",
            "remaining_defect": "pure ainc=-1",
            "terminal": (
                "ainc nonzero on the protected fibre gives a normalized "
                "relative generator; ainc zero gives the physical anchor "
                "separator, with the bordered Cartan refinement from 8e1f858"
            ),
            "coarse_x_simplification": {
                "identity": "r0-x_v-d_v=T_v+rho_v-2*d_v",
                "status": "tautological, not a second construction",
                "reason": (
                    "x_v=r0-T_v-rho_v+d_v is source-typed only after the "
                    "same labelled d_v exists; the apparent simplification "
                    "therefore uses the missing section twice"
                ),
            },
        },
        "first_missing_source_cell": {
            "coarse_name": "d_even",
            "boundary": "labelled ores=(B1+B4)/2",
            "other_outputs": "lower=W=target=ainc=0",
            "fine_grade_requirement": (
                "its homogeneous source projections lie separately in the "
                "face3/multiplier34/B4 and face5/multiplier45/B1 grades; a "
                "coarse ungraded ores scalar is insufficient"
            ),
            "equivalent_stronger_supply": (
                "two fixed labelled sections d_B4 and d_B1 in those grades"
            ),
            "primitive_separator": [str(entry) for entry in chi],
            "separator_pairing_on_v": "1",
            "separator_pairing_on_required_minus_2v_correction": "-2",
            "physical_Cartan_can_replace_section": False,
        },
        "Gate_I_probe_scope": {
            "old_terminal_only_claim": "false/superseded by 271df91",
            "helps_current_even_residual": False,
            "reason": (
                "the literal cap-Cartan composite has zero target/anchor/ores "
                "and closes output terminals; it constructs neither d_fixed/"
                "d_pair nor the rho-even B1/B4 labelled section"
            ),
        },
        "weighted_reset_word": {
            "direct_projection": [str(entry) for entry in y],
            "direct_exact_condition": "h3+h5=0",
            "rho_even_projection": [str(entry) for entry in y_even],
            "rho_even_exact_condition": "2*h3+h2+h5=0",
            "nonconstant_h_sufficient": False,
            "direct_nonempty_C5_specialization": {
                "chords_13_14_24_25_35": [str(entry) for entry in direct_chords],
                "h": [str(entry) for entry in h_direct],
            },
            "rho_even_nonempty_C5_specialization": {
                "chords_13_14_24_25_35": [str(entry) for entry in even_chords],
                "h": [str(entry) for entry in h_even],
            },
            "inactive_status_of_specializations": "not established",
            "full_denominator_membership_from_weighted_equation": False,
        },
        "verdict": (
            "the coarse residual has an exact physical cone reduction to the "
            "anchor generator/separator alternative, conditional precisely "
            "on a rho-even B1/B4 labelled ordinary-residue section.  Existing "
            "Cartan and output-terminal constructions do not supply it"
        ),
        "beta_zero": "independent and untouched",
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("even repair anchor/residue ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 tau_plus even repair anchor/residue fibre: CONDITIONAL REDUCTION")
    print("cap+rho-2*d_even cancels target/residue; only ainc=-1 remains")
    print("terminal: relative generator or physical anchor separator")
    print("first missing cell: rho-even B1/B4 labelled pure-residue section")
    print("nonconstant h: possible but not sufficient for fixed selected y")
    print("Gate-I terminal probe: superseded; no d_even construction")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
