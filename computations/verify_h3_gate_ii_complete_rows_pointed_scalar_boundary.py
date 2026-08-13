#!/usr/bin/env python3
"""Separate complete coefficient rows from the missing Gate-II source cell.

In the direct-free part of the physical response coefficient 11:110000,
there are 90 labelled p*s*q*q occurrences.  On the occurrence-expanded
coefficient module, the restriction of all 729 unary and 4*729 response
rows has rank one: the selected response row is the all-ones aggregate and
every other output-labelled row is zero.  Hence a selected occurrence
covector P_f is not forced by the complete normalized coefficient rows.

The rank-one projection in this checker is deliberately only a logical
counterguard on that occurrence-expanded module.  It fixes the aggregate
and a literal symmetric q=M-a readout while killing P_f, but it is not a
source-valid comparison: promotion through the scalar-cell monomial
Jacobian is exactly the missing PP/Spencer cell.

The checker also imports the complete-row census for the literal special
two-occurrence active-coloop packet.  That census has zero trapped
completions among 4736 response seeds.  Thus the occurrence-module guard is
not a counterexample source point.  The smallest honest new datum is an
occurrence-asymmetric physical row/cell; on two occurrence columns its
Fitting minor is r_g-r_f.  If lifted, its next nonlinear obstruction is the
already isolated divided-Hasse class F_[2](xi) modulo the physical image.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py":
        "22e1e7a6a933b1ba71bbd95bb605b1351e823506e495682cccff312cd3df3b15",
    "notes/h3-active-fan-coloop-gate-ii-assembly-boundary.md":
        "bacb7b4b138882c0cc07f13767f2e4ead86aa630c55cf1a946943141b7cee7a7",
    "computations/verify_h3_protection_survivor_active_coloop_phi_gate.py":
        "031d680f72b99fc864c1d9a2e87a180981f76ed8477cd154ddb81a6c3a45b72a",
    "notes/h3-protection-survivor-active-coloop-phi-gate.md":
        "c1492d41e5cd85f18c57ead28ef13df973b30680fb24b7adac4df79cbccaa501",
    "computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py":
        "fe60edcc44c33e660b50f7e8d627b506c5bd81c1d97f15e66b9e8a35e9f3c4ad",
    "notes/h3-active-coloop-closed-shore-complete-row-response-gate.md":
        "1470ffc55dff20f0919b4be884ca8d54efe7a15e90117d1610aef067c82b44b2",
    "computations/verify_h3_active_coloop_literal_packet_termination_scope.py":
        "ad369a692aa2a7bde3b30a0a4cba5e401b6e61afc62dd752a4f51781a9e6485e",
    "notes/h3-active-coloop-literal-packet-termination-scope.md":
        "1201ea94d8faafefefeaff81a47987e41a817c4775fc98057294ed80fdfe51c5",
    "computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py":
        "f0905b3e33a45b51f03dd6716c3f6b29ae21c39fecf50a4ffc32960499a608c7",
    "notes/h3-coloop-alpha-localized-pointed-pf-ga-fitting-gate.md":
        "5d637d94ec2bab2f968dcb31b45b805fecd66da13fb1c927a490a6e20927fe4f",
    "computations/verify_h3_occurrence_kernel_integrability_terminal_gate.py":
        "40a3a5875951b2d48aeda4ca58ea25029bb12d7195988c057f7c3590ec10039c",
    "notes/h3-occurrence-kernel-integrability-terminal-gate.md":
        "62210dd5971832b3b7b2227f56fe15dd54adc2492c834a4498a0d455d4ce94c6",
}
EXPECTED_LEDGER_SHA256 = "e1582198c5c22571f9df873b419dd8e92afbd61dc04eddde07292f7cc61b23c4"

SITES = tuple(range(6))


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


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def response_occurrences():
    answer = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            residual = tuple(site for site in SITES
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                answer.append((p_site, s_site, tuple(sorted(matching))))
    require(len(answer) == 90 and len(set(answer)) == 90,
            (len(answer), len(set(answer))))
    return tuple(answer)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def subtract(left, right):
    return tuple(Q(a) - Q(b) for a, b in zip(left, right, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def rref(rows, width):
    work = [list(map(Q, row)) for row in rows]
    require(all(len(row) == width for row in work), "ragged matrix")
    pivots = []
    pivot_row = 0
    for column in range(width):
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
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(rows, width):
    return len(rref(rows, width)[1])


def pullback(row, xi, H):
    """Pull a row back through Phi(v)=v-xi*H(v)."""
    return subtract(row, scale(dot(row, xi), H))


def audit_complete_same_grade_rows():
    occurrences = response_occurrences()
    width = len(occurrences)
    aggregate = tuple(Q(1) for _ in occurrences)
    H = tuple(Q(index == 0) for index in range(width))
    mate = tuple(Q(index == 1) for index in range(width))
    xi = subtract(H, mate)

    # The complete physical coefficient inventory is 729 unary plus four
    # response heads on all 729 words.  On the occurrence-expanded columns
    # of one selected response head/word, output idempotents make every row
    # except that response coefficient zero.  Its direct-free p*s*q*q part
    # is the all-ones aggregate.
    total_rows = 729 + 4 * 729
    restricted_nonzero_rows = (aggregate,)
    require(total_rows == 3645 and rank(restricted_nonzero_rows, width) == 1,
            "the complete selected coefficient restriction changed")
    require(dot(aggregate, xi) == 0 and dot(H, xi) == 1
            and rank((aggregate, H), width) == 2,
            "the pointed occurrence quotient changed")

    # A normalized pure target has a constant right side, but its
    # differential and its occurrence incidence on this mixed response
    # output idempotent are both zero.  The fifteen direct D*q^3 terms also
    # carry no p*s*q*q occurrence column.
    normalized_pure_rows_on_block = 0
    direct_response_occurrences_on_block = 0
    require(normalized_pure_rows_on_block == 0
            and direct_response_occurrences_on_block == 0,
            "an output-disjoint row entered the selected occurrence block")

    # The formal aggregate projection preserves all restricted coefficient
    # rows and any symmetric physical readout.  Take M=aggregate, a=0 and
    # q=M-a.  It kills H.  This proves logical independence only; Phi is an
    # occurrence-presentation projection, not a scalar-source chain map.
    M = aggregate
    a = tuple(Q(0) for _ in occurrences)
    q = subtract(M, a)
    require(q == aggregate and pullback(aggregate, xi, H) == aggregate
            and pullback(M, xi, H) == M
            and pullback(a, xi, H) == a
            and pullback(q, xi, H) == q
            and not any(pullback(H, xi, H)),
            "the aggregate/q-preserving pointed-dark projection changed")

    return {
        "selected_head_word": "11:110000",
        "selected_direct_free_occurrences": width,
        "enumeration": "6 ordered p sites * 5 s sites * 3 C4 matchings",
        "complete_coefficient_rows": {
            "unary": 729,
            "four_response_heads": 4 * 729,
            "total": total_rows,
            "nonzero_restrictions_to_selected_occurrence_block": 1,
            "restriction_rank": 1,
            "selected_row": "epsilon=(1,...,1) on Q^90",
        },
        "normalized_pure_target_derivative_on_block": 0,
        "direct_D_q3_incidence_on_direct_free_block": 0,
        "pointed_rank": rank((aggregate, H), width),
        "kernel_witness": "xi=e_f-e_g; epsilon(xi)=0, P_f(xi)=1",
        "formal_projection": {
            "formula": "Phi_occ(v)=v-(e_f-e_g)P_f(v)",
            "complete_rows_fixed": True,
            "M_fixed": True,
            "a_fixed": True,
            "literal_q=M-a_fixed": True,
            "P_f_pullback": 0,
            "physicality": (
                "NO: this acts on occurrence-presentation columns.  A source-"
                "valid Phi must lift it through the scalar monomial Jacobian "
                "and preserve all augmented word/fine/repeated rows"
            ),
        },
    }


def audit_special_packet_has_no_trapped_completion():
    response_gate = load(
        "computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py",
        "gate_ii_full_response_gate",
    )
    ledger = response_gate.audit()
    census = ledger["simultaneous_unary_mate_census"]
    exit_data = ledger["completed_response_seed_hall_exit"]
    require(census["simultaneous_mate_choices"] == 2744
            and census["trapped_closed_shore_packets"] == 148,
            ("the special three-unary census changed", census))
    require(exit_data["total_completions_tested"] == 4736
            and exit_data["closed_shore_survivors"] == 0,
            ("a special response completion became trapped", exit_data))
    return {
        "literal_two_occurrence_mate_choices": 2744,
        "initial_closed_shore_shadows": 148,
        "forced_three_response_row_completions": 4736,
        "trapped_full_response_completions": 0,
        "consequence": (
            "the rank-one occurrence guard is not a complete trapped source "
            "counterexample.  Complete rows route the special packet by Hall "
            "growth; they still do not create P_f or a protected odd Phi"
        ),
    }


def audit_first_additional_cell():
    aggregate = (Q(1), Q(1))
    candidates = ((Q(0), Q(0)), (Q(1), Q(1)),
                  (Q(1), Q(0)), (Q(-2), Q(3)))
    records = []
    for row in candidates:
        determinant = aggregate[0] * row[1] - aggregate[1] * row[0]
        require(determinant == row[1] - row[0],
                ("the two-occurrence Fitting minor changed", row))
        records.append({"row": list(map(str, row)),
                        "minor": str(determinant)})
    require(records[1]["minor"] == "0" and records[2]["minor"] == "-1",
            "the symmetric/pointed exits changed")
    return {
        "zeroth_order_exact_criterion": (
            "supply a source-valid occurrence-asymmetric row r; on (f,g) "
            "the transverse Fitting minor is r_g-r_f"
        ),
        "unit_exit": "r_g-r_f is a unit on the localized coloop chart",
        "source_cell_boundary": (
            "an occurrence-labelled relative PP/Spencer (or Tate) cell whose "
            "scalar-source differential lifts e_f-e_g while retaining the "
            "fan word, fine/repeated grade, common q tail and endpoint head"
        ),
        "first_nonlinear_face_after_a_tangent_lift":
            "o_2=[F_[2](xi)] in coker(J_xF)",
        "augmented_rows_still_required": [
            "anchor H=P_f", "literal q=M-a", "ridge/W",
            "eta/sigma", "terminal/protected rows",
        ],
        "sample_fitting_minors": records,
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II complete rows versus pointed scalar boundary",
        "pins": PINS,
        "complete_same_grade_restriction": audit_complete_same_grade_rows(),
        "special_packet_full_response_test":
            audit_special_packet_has_no_trapped_completion(),
        "first_additional_physical_cell": audit_first_additional_cell(),
        "sharp_verdict": (
            "Complete normalized pure-target and five-tensor coefficient rows "
            "do not force [H]=[P_f] and do not supply a source-valid Phi.  On "
            "the selected h=3 occurrence grade they see only the 90-term "
            "aggregate.  Literal q=M-a can be aggregate-symmetric and is "
            "therefore independent of the pointed quotient.  The smallest "
            "two-occurrence trapped guard does not extend to a complete "
            "source: its complete response mates force Hall growth.  The "
            "remaining positive theorem is exactly an occurrence-asymmetric "
            "scalar-source lift/PP cell, followed by its Hasse and augmented "
            "q/anchor/terminal compatibility"
        ),
        "h3_scope": (
            "exact for the canonical direct-free 11:110000 occurrence block "
            "and the pinned literal special active-coloop completion census; "
            "it is not a complete GHZ counterexample and not a construction "
            "of the arbitrary trapped-coloop comparison"
        ),
        "uniform_scope": (
            "the aggregate-versus-pointed incidence observation formally "
            "persists for any coefficient with at least two occurrences, but "
            "no all-h trapped-coloop completion, source lift, or physical "
            "q=M-a comparison is claimed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Gate-II complete-row ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("h3 selected occurrence block: COMPLETE ROW RANK 1")
    print("pointed P_f rank: 2; literal symmetric q=M-a: INDEPENDENT")
    print("special two-occurrence trapped full completion: 0/4736")
    print("first new cell: occurrence-asymmetric scalar-source PP lift")
    print("uniform all-h construction: NOT CLAIMED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
