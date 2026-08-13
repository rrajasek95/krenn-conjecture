#!/usr/bin/env python3
"""Audit the full physical augmentation matrix for the reduced-Eq cell.

This extends the Cartan/cap solve by separating derived Yw from physical W
and adjoining the physical q row.  In six canonical multiplier labels put

    B_i = r0_i-T_i,
    O_u = -B_u+rho_u.

The old columns force

    O_u=(lower=Eq=-u, ainc=sum(u), ores=u),

with Yw=W=target=q=0.  A granted primitive anchor column
A=(ainc=-1,q=1) removes ainc for augmentation-one u while preserving the
physical relation q+sum(lower)+ainc=0.  The one placed Cartan packet has
ores=alpha and terminal=tau.  Exact elimination gives the full criterion:

    desired D(u,zeta,q0) is in span
    iff u=c alpha, zeta=-c tau, and q0=sum(u).

For u=alpha this is O_alpha-K_alpha=-M_v, so the selected full-alpha odd
output is already physical.  Each individual rho pair and the even
(B1+B4)/2 direction retain a primitive labelled-residue cokernel class.

The checker also freezes a row-typing guard: a model with only one common
"W" coordinate has not by itself proved separate Yw and physical-W
naturality.  The committed M_v theorem directly supplies protected W=0 for
the full alpha aggregate; pairwise/even use still needs the relevant
columnwise Yw/W comparison if it is not part of the assumed rho section.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py":
        "3397fc0b7d773d97fb26e737eb490136c3062549951b07eca701ee46739ff2bb",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_interface_iii_augmented_cap_factorization.py":
        "06e64c5db2a59b8877cb112515d50779be95010801f19690f97060bf08621213",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py":
        "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
}
EXPECTED_LEDGER_SHA256 = (
    "4afd82854e324bfa9dba434600555b33e0b276b9f26af4a841a3996d04edf657"
)

N = 6
LOWER = slice(0, N)
EQ = slice(LOWER.stop, LOWER.stop + N)
YW = slice(EQ.stop, EQ.stop + N)
W = slice(YW.stop, YW.stop + N)
TARGET = slice(W.stop, W.stop + N)
ORES = slice(TARGET.stop, TARGET.stop + N)
AINC = ORES.stop
TERMINAL = slice(AINC + 1, AINC + 8)
QROW = TERMINAL.stop
ROWS = QROW + 1

ALPHA = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
TAU = (Q(1), Q(1), Q(1), Q(1), Q(1), Q(1), Q(-1))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def unit(index: int):
    return tuple(Q(index == position) for position in range(N))


def vector(*, lower=(), eq=(), yw=(), w=(), target=(), ores=(),
           ainc=0, terminal=(), q=0):
    answer = [Q(0)] * ROWS
    for section, values in (
        (LOWER, lower), (EQ, eq), (YW, yw), (W, w),
        (TARGET, target), (ORES, ores), (TERMINAL, terminal),
    ):
        for index, value in enumerate(values):
            answer[section.start + index] = Q(value)
    answer[AINC] = Q(ainc)
    answer[QROW] = Q(q)
    return tuple(answer)


def add(*columns):
    return tuple(sum((Q(column[row]) for column in columns), Q(0))
                 for row in range(ROWS))


def scale(value, column):
    return tuple(Q(value) * Q(entry) for entry in column)


def combination(coefficients, columns):
    return add(*(scale(coefficient, column) for coefficient, column in
                 zip(coefficients, columns, strict=True)))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns):
    if not columns:
        return 0
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(ROWS)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, ROWS)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(ROWS):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def old_full_columns():
    r0 = []
    cap = []
    response = []
    for index in range(N):
        e = unit(index)
        r0.append(vector(lower=e, eq=e, target=e, ainc=-1))
        # The diagonal full-row lift records separately that both the
        # derived Yw and physical W values are -e on T and +e on rho.
        cap.append(vector(yw=tuple(-value for value in e),
                          w=tuple(-value for value in e), target=e))
        response.append(vector(yw=e, w=e, ores=e))
    cartan = vector(ores=ALPHA, terminal=TAU)
    # This is the primitive anchor *hypothesis* used in the augmentation-one
    # branch.  Its q value is forced by physical q, not freely set to zero.
    anchor = vector(ainc=-1, q=1)
    return r0, cap, response, cartan, anchor


def physical_q_covector():
    return vector(lower=(Q(1),) * N, ainc=1, q=1)


def desired(u, *, terminal=(), q=None):
    q_value = sum(u, Q(0)) if q is None else Q(q)
    return vector(
        lower=tuple(-value for value in u),
        eq=tuple(-value for value in u),
        terminal=terminal,
        q=q_value,
    )


def sign_and_membership_audit(r0, cap, response, cartan, anchor):
    b = [add(r0[index], scale(-1, cap[index])) for index in range(N)]

    def nearest(u):
        return add(scale(-1, combination(u, b)),
                   combination(u, response))

    # Verify the signs independently of d170fdb.
    samples = (ALPHA,
               tuple(a - b for a, b in zip(unit(0), unit(5), strict=True)),
               (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0)))
    records = []
    for u in samples:
        actual = nearest(u)
        expected = vector(
            lower=tuple(-value for value in u),
            eq=tuple(-value for value in u),
            ores=u,
            ainc=sum(u, Q(0)),
        )
        require(actual == expected,
                ("the full-row O_u sign changed", u, actual))
        # If sum(u) is nonzero, the primitive anchor coefficient is exactly
        # sum(u); its q is then exactly the physical value sum(u).
        anchor_dressed = add(actual, scale(sum(u, Q(0)), anchor))
        require(anchor_dressed[AINC] == 0
                and anchor_dressed[QROW] == sum(u, Q(0)),
                "primitive anchor/q dressing changed")
        records.append({
            "u": [str(value) for value in u],
            "O_u_ainc": str(sum(u, Q(0))),
            "anchor_coefficient": str(sum(u, Q(0))),
            "after_anchor_q": str(anchor_dressed[QROW]),
        })

    # Full alpha completion, including separate Yw/W, eta/sigma, and q.
    o_alpha = nearest(ALPHA)
    completed_alpha = add(o_alpha, scale(-1, cartan))
    expected_alpha = desired(ALPHA,
                             terminal=tuple(-value for value in TAU))
    require(completed_alpha == expected_alpha,
            "O_alpha-K stopped being the fully augmented -M_v")
    require(rank(r0 + cap + response + [cartan, anchor])
            == len(r0 + cap + response + [cartan, anchor]),
            "the granted full physical columns lost independence")

    q_relation = physical_q_covector()
    require(all(dot(q_relation, column) == 0 for column in
                r0 + cap + response + [cartan, anchor, completed_alpha]),
            "a physical column violated q+sum(lower)+ainc=0")
    return b, nearest, records, completed_alpha


def residue_and_anchor_cokernel_audit(r0, cap, response, cartan, anchor,
                                      nearest):
    known_without_anchor = r0 + cap + response + [cartan]
    known = known_without_anchor + [anchor]
    pair_05 = tuple(a - b for a, b in
                    zip(unit(0), unit(5), strict=True))
    pair_23 = tuple(a - b for a, b in
                    zip(unit(2), unit(3), strict=True))
    even = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    tests = {
        "rho_pair_05": (pair_05, tuple(
            a + b for a, b in zip(unit(0), unit(3), strict=True))),
        "rho_pair_23": (pair_23, tuple(
            a + b for a, b in zip(unit(2), unit(5), strict=True))),
        "rho_even_B1_B4": (even, tuple(
            a + b for a, b in zip(unit(1), unit(4), strict=True))),
    }
    records = {}
    for name, (u, witness) in tests.items():
        require(dot(witness, ALPHA) == 0 and dot(witness, u) == 1,
                ("bad labelled-residue witness", name))
        # Either the Yw or physical-W version kills the diagonal old block.
        lambda_yw = vector(
            eq=tuple(-value for value in witness),
            yw=witness,
            target=witness,
            ores=tuple(-value for value in witness),
        )
        lambda_w = vector(
            eq=tuple(-value for value in witness),
            w=witness,
            target=witness,
            ores=tuple(-value for value in witness),
        )
        target = desired(u)
        require(all(dot(covector, column) == 0
                    for covector in (lambda_yw, lambda_w)
                    for column in known),
                ("a primitive residue dual sees the known block", name))
        require(dot(lambda_yw, target) == dot(lambda_w, target) == 1,
                ("a primitive residue dual lost its target pairing", name))
        require(rank(known + [target]) == rank(known) + 1,
                ("a residue-obstructed target entered the span", name))
        # The anchor family removes precisely the old sum(lower)+ainc dual
        # when sum(u)!=0, while leaving the residue witness untouched.
        anchor_dual = vector(lower=(Q(1),) * N, ainc=1)
        require(all(dot(anchor_dual, column) == 0
                    for column in known_without_anchor)
                and dot(anchor_dual, anchor) == -1,
                "the primitive anchor family stopped killing the anchor dual")
        records[name] = {
            "u": [str(value) for value in u],
            "sum_u": str(sum(u, Q(0))),
            "anchor_needed": bool(sum(u, Q(0))),
            "anchor_coefficient": str(sum(u, Q(0))),
            "forced_physical_q": str(sum(u, Q(0))),
            "primitive_residue_witness": [str(value) for value in witness],
            "lambda_Yw_on_target": "1",
            "lambda_W_on_target": "1",
            "rank_jump_after_granted_anchor": 1,
        }
    return records


def terminal_and_q_criterion_audit(r0, cap, response, cartan, anchor):
    known = r0 + cap + response + [cartan, anchor]

    # If u=c alpha, exact coefficients are unique on the independent old
    # columns: r0=-u,T=u,rho=u,K=-c,A=sum(u).  They force terminal=-c*tau
    # and q=sum(u).  Check several c.
    scalar_records = []
    for c in (Q(-3), Q(-1, 2), Q(0), Q(1), Q(5, 3)):
        u = tuple(c * value for value in ALPHA)
        built = add(
            combination(tuple(-value for value in u), r0),
            combination(u, cap),
            combination(u, response),
            scale(-c, cartan),
            scale(sum(u, Q(0)), anchor),
        )
        target = desired(u, terminal=tuple(-c * value for value in TAU))
        require(built == target,
                ("the full membership formula changed", c, built, target))
        scalar_records.append({
            "c": str(c),
            "terminal": [str(-c * value) for value in TAU],
            "q": str(target[QROW]),
        })

    # q is not optional once lower/anchor are physical.  Assigning q=0 to
    # an augmentation-one target is separated by the physical q relation.
    even = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    wrong_q = desired(even, q=0)
    q_relation = physical_q_covector()
    require(all(dot(q_relation, column) == 0 for column in known)
            and dot(q_relation, wrong_q) == -1,
            "the physical q compatibility dual changed")
    return {
        "membership_criterion": (
            "u=c*alpha, terminal=-c*tau, q=sum(u); the primitive anchor "
            "coefficient is sum(u)"
        ),
        "scalar_checks": scalar_records,
        "physical_q_relation": "q+sum(lower)+ainc=0",
        "augmentation_one_with_q_zero_pairing": "-1",
    }


def separated_yw_w_typing_guard(r0, cap, response, cartan):
    # Collapse away physical W.  Changing only W(rho) is invisible in the
    # old one-W-row presentation if that row was interpreted as Yw.  It does
    # change O_alpha on the separate physical-W row.
    bad_response = []
    for column in response:
        changed = list(column)
        for index in range(W.start, W.stop):
            changed[index] = Q(0)
        bad_response.append(tuple(changed))

    b = [add(r0[index], scale(-1, cap[index])) for index in range(N)]
    good = add(scale(-1, combination(ALPHA, b)),
               combination(ALPHA, response), scale(-1, cartan))
    bad = add(scale(-1, combination(ALPHA, b)),
              combination(ALPHA, bad_response), scale(-1, cartan))
    keep = tuple(index for index in range(ROWS)
                 if not (W.start <= index < W.stop))
    require(tuple(good[index] for index in keep)
            == tuple(bad[index] for index in keep)
            and all(good[index] == 0 for index in range(W.start, W.stop))
            and tuple(bad[W]) == tuple(-value for value in ALPHA),
            "the separated Yw/W hidden-row guard changed")
    return {
        "one_common_W_row_sufficient_for_separate_Yw_W": False,
        "hidden_mutation": "retain Yw(rho_i)=e_i but set physical W(rho_i)=0",
        "all_rows_except_physical_W_unchanged": True,
        "bad_full_alpha_physical_W": [str(-value) for value in ALPHA],
        "repair_for_selected_alpha": (
            "the committed physical M_v theorem directly asserts protected "
            "W=0 on the aggregate, so the selected alpha output is safe"
        ),
        "pair_even_warning": (
            "using individual rho sections in another projection still "
            "requires their columnwise physical-W typing"
        ),
    }


def pinned_m_v_input_scope_audit():
    mv = (ROOT / (
        "computations/verify_h3_literal_mv_cap_cartan_composition.py"
    )).read_text()
    first_flat = (ROOT / (
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py"
    )).read_text()
    require('M_v = -O_alpha + K' in mv
            and '"M_v_equals_minus_O_plus_K"' in mv
            and '"literal_boundary_support": 360' in mv
            and '"ordinary_residue": [0, 0, 0, 0]' in mv
            and '"D_W_target_ainc": [0, 0, 0, 0]' in mv,
            "the physical full-alpha M_v theorem changed")
    require('"known_relative_alpha_cell": relative_alpha_pairing' in first_flat
            and "relative_alpha_pairing = sum(alpha)" in first_flat,
            "the physical q value on the alpha cell changed")
    return {
        "physical_output_identity": "O_alpha-K_alpha=-M_v",
        "literal_lower_features": 360,
        "Eq": "-alpha",
        "ores_target_W_ainc_q": 0,
        "eta_sigma": "-tau",
        "input_map_constructed": False,
        "remaining_equation": (
            "identify the completed occurrence-Hessian/15-label lower input "
            "with the literal 360-feature boundary J3(M_v)"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    r0, cap, response, cartan, anchor = old_full_columns()
    b, nearest, signs, completed_alpha = sign_and_membership_audit(
        r0, cap, response, cartan, anchor
    )
    ledger = {
        "theorem": "full physical augmentation matrix for central reduced Eq",
        "pins": PINS,
        "row_order": (
            "lower_6, Eq_6, Yw_6, physical_W_6, target_6, ores_6, "
            "ainc, eta/sigma_7, q"
        ),
        "column_counts": {
            "r0": 6, "T": 6, "rho": 6,
            "placed_Cartan": 1, "granted_primitive_anchor": 1,
        },
        "independent_sign_audit": signs,
        "full_alpha": pinned_m_v_input_scope_audit(),
        "residual_primitive_cokernel": residue_and_anchor_cokernel_audit(
            r0, cap, response, cartan, anchor, nearest
        ),
        "terminal_and_q_criterion": terminal_and_q_criterion_audit(
            r0, cap, response, cartan, anchor
        ),
        "separated_Yw_W_guard": separated_yw_w_typing_guard(
            r0, cap, response, cartan
        ),
        "primitive_anchor_status": (
            "conditional source family: if granted, it removes the "
            "augmentation-one anchor dual and necessarily carries q=1.  "
            "It does not alter the labelled-residue quotient"
        ),
        "exact_verdict": (
            "the placed Cartan/cap packet completes exactly the full alpha "
            "odd output, namely -M_v.  It does not complete either single "
            "rho pair or the even B1/B4 direction.  After granting the "
            "primitive anchor family, their first residual is still one "
            "primitive labelled-residue cokernel class"
        ),
        "scope": (
            "exact finite augmented-row theorem.  The full-alpha output is "
            "physical by the pinned M_v theorem; the occurrence/15-label "
            "input-to-360-lower comparison, general Cartan orbit, primitive "
            "anchor source construction, and pair/even W typing are not "
            "asserted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("full physical augmentation ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 reduced-Eq full physical augmentation matrix: PASS")
    print("full alpha odd output: O_alpha-K_alpha=-M_v (physical)")
    print("single rho pairs/even B1+B4: primitive labelled-ores cokernel")
    print("anchor correction: conditional, with forced physical q=1")
    print("remaining odd work: 15-label input -> 360-feature lower equality")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
