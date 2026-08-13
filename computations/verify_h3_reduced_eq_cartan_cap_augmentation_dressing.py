#!/usr/bin/env python3
"""Solve the exact cap/Cartan augmentation dressing of the reduced-Eq cell.

The canonical six-label block has physical columns r0_i,T_i,varrho_i and
one placed endpoint-odd Cartan packet K_alpha.  With

    alpha=(e0-e5)+(e2-e3),

K_alpha has labelled residue alpha, protected rows zero, and the fixed
eta/sigma terminal tau.  This checker proves:

* the Eq-only Koszul core is not in the physical span; the six primitive
  covectors lower_i-Eq_i force its literal private/lower dressing;
* sum(lower_i)+ainc forces the anchor dressing;
* after these are supplied by B_i=r0_i-T_i, the nearest lift
  O_u=-B_u+varrho_u has residue u;
* O_u can be completed by the placed Cartan packet iff u is a multiple of
  alpha.  For u=alpha, O_alpha-K_alpha=-M_v exactly, including terminal;
* a single rho pair e0-e5 (or e2-e3) survives modulo the placed Cartan line.

Thus Cartan cancels the full four-corner alpha residue, but it does not give
arbitrary labelled residue sections.  The remaining quotient covectors are
the true augmentation obstruction for the normal Koszul cell.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_shared_loop_full_augmented_membership_dual.py":
        "108ffb00c5b742613b464d2d6c46dd967b6db4eac3fe2e1d967b32500e4a6abb",
    "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py":
        "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
    "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py":
        "96280ef01c70b4f3381e6d85d2c9fb64b1620850305a4346601fccbd7d63dc44",
}
EXPECTED_LEDGER_SHA256 = (
    "9764fecdf999c799e0a4aefb5ed90ce9897e6f6b6b779f200052ad86220ecff2"
)

N = 6
LOWER = slice(0, N)
EQ = slice(N, 2 * N)
W = slice(2 * N, 3 * N)
TARGET = slice(3 * N, 4 * N)
ORES = slice(4 * N, 5 * N)
AINC = ORES.stop
TERMINAL = slice(AINC + 1, AINC + 8)
ROWS = TERMINAL.stop

ALPHA = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
TAU = (Q(1), Q(1), Q(1), Q(1), Q(1), Q(1), Q(-1))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def unit(index):
    return tuple(Q(int(index == position)) for position in range(N))


def vector(*, lower=(), eq=(), w=(), target=(), ores=(), ainc=0,
           terminal=()):
    answer = [Q(0)] * ROWS
    for section, values in ((LOWER, lower), (EQ, eq), (W, w),
                            (TARGET, target), (ORES, ores),
                            (TERMINAL, terminal)):
        for index, value in enumerate(values):
            answer[section.start + index] = Q(value)
    answer[AINC] = Q(ainc)
    return tuple(answer)


def add(*columns):
    return tuple(sum((Q(column[row]) for column in columns), Q(0))
                 for row in range(ROWS))


def scale(value, column):
    return tuple(Q(value) * Q(entry) for entry in column)


def add6(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(N))


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


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


def combination(coefficients, columns):
    return add(*(scale(value, column) for value, column in
                 zip(coefficients, columns, strict=True)))


def old_columns():
    r0 = []
    cap = []
    response = []
    for index in range(N):
        e = unit(index)
        r0.append(vector(lower=e, eq=e, target=e, ainc=-1))
        cap.append(vector(w=tuple(-value for value in e), target=e))
        response.append(vector(w=e, ores=e))
    cartan = vector(ores=ALPHA, terminal=TAU)
    return r0, cap, response, cartan


def primitive_dressing_audit(r0, cap, response, cartan):
    known = r0 + cap + response + [cartan]

    # Every physical old/Cartan column has equal literal-lower and Eq rows.
    # These six independent covectors detect an Eq-only Koszul cell.
    lower_eq_duals = []
    for index in range(N):
        covector = vector(lower=unit(index),
                          eq=tuple(-value for value in unit(index)))
        require(all(dot(covector, column) == 0 for column in known),
                ("lower-Eq dual sees a physical column", index))
        core = vector(eq=tuple(-value for value in unit(index)))
        require(dot(covector, core) == 1,
                ("lower-Eq dual stopped detecting the core", index))
        lower_eq_duals.append(covector)

    anchor_dual = vector(lower=(Q(1),) * N, ainc=1)
    require(all(dot(anchor_dual, column) == 0 for column in known),
            "sum(lower)+ainc sees the physical cap/Cartan block")

    # A clean reduced-Eq core raises rank.  Supplying lower=-u and
    # ainc=sum(u) is exactly what kills the seven primitive covectors.
    core_alpha = vector(eq=tuple(-value for value in ALPHA))
    mandatory_alpha = vector(
        lower=tuple(-value for value in ALPHA),
        eq=tuple(-value for value in ALPHA),
        ainc=sum(ALPHA, Q(0)),
    )
    require(rank(known + [core_alpha]) == rank(known) + 1,
            "the Eq-only alpha core entered the known physical span")
    require(all(dot(covector, mandatory_alpha) == 0
                for covector in lower_eq_duals + [anchor_dual]),
            "the mandatory private/anchor dressing is incomplete")
    return {
        "primitive_lower_minus_Eq_covectors": N,
        "primitive_anchor_covector": "sum_i lower_i+ainc",
        "Eq_only_alpha_core_raises_rank": True,
        "mandatory_dressing": (
            "lower=-u, Eq=-u, ainc=sum(u), before residue/terminal"
        ),
    }


def cartan_completion_audit(r0, cap, response, cartan):
    b = [add(r0[index], scale(-1, cap[index])) for index in range(N)]

    def nearest(u):
        # O_u=-B_u+varrho_u.  It has zero W/target, lower=Eq=-u,
        # ainc=sum(u), and labelled residue u.
        return add(
            scale(-1, combination(u, b)),
            combination(u, response),
        )

    o_alpha = nearest(ALPHA)
    expected_o = vector(
        lower=tuple(-value for value in ALPHA),
        eq=tuple(-value for value in ALPHA),
        ores=ALPHA,
        ainc=sum(ALPHA, Q(0)),
    )
    require(o_alpha == expected_o,
            "O_alpha stopped being the nearest fully augmented lift")

    # The pinned literal formula is M_v=-O_alpha+K_alpha.
    mv = add(scale(-1, o_alpha), cartan)
    expected_mv = vector(lower=ALPHA, eq=ALPHA, terminal=TAU)
    require(mv == expected_mv,
            "the finite model stopped reproducing M_v=-O_alpha+K")
    completed_alpha = add(o_alpha, scale(-1, cartan))
    require(completed_alpha == scale(-1, mv),
            "Cartan residue cancellation stopped giving exactly -M_v")

    # A single rho-pair residue is not proportional to the placed alpha.
    # The explicit w-duals below annihilate alpha and detect the pair.
    pair_05 = tuple(a - b for a, b in
                    zip(unit(0), unit(5), strict=True))
    pair_23 = tuple(a - b for a, b in
                    zip(unit(2), unit(3), strict=True))
    require(add(vector(ores=pair_05), vector(ores=pair_23))
            == vector(ores=ALPHA),
            "the placed Cartan line stopped being the two-pair sum")

    # For any w with w.alpha=0, the covector
    # -Eq_w+W_w+target_w-ores_w kills r0,T,varrho,K.  Choose witnesses
    # separately for the two pair directions.
    witnesses = {
        "pair_05": (pair_05, add6(unit(0), unit(3))),
        "pair_23": (pair_23, add6(unit(2), unit(5))),
    }
    records = {}
    known = r0 + cap + response + [cartan, mv]
    for name, (u, w) in witnesses.items():
        require(dot(w, ALPHA) == 0 and dot(w, u) == 1,
                ("bad quotient witness", name))
        covector = vector(
            eq=tuple(-value for value in w),
            w=w,
            target=w,
            ores=tuple(-value for value in w),
        )
        require(all(dot(covector, column) == 0 for column in known),
                ("pair quotient dual sees a physical column", name))
        nearest_lift = nearest(u)
        clean_dressed = vector(
            lower=tuple(-value for value in u),
            eq=tuple(-value for value in u),
            ainc=sum(u, Q(0)),
        )
        # Any multiple of K changes terminal and residue only in ALPHA, so
        # this pairing is independent of the attempted Cartan coefficient.
        require(dot(covector, nearest_lift) == 0
                and dot(covector, clean_dressed) == 1
                and dot(covector, cartan) == 0,
                ("pair residue escaped its quotient dual", name))
        records[name] = {
            "u": [str(value) for value in u],
            "annihilating_w": [str(value) for value in w],
            "pairing_on_nearest_physical_lift": "0",
            "pairing_on_desired_residue_zero_dressing": "1",
            "pairing_on_Cartan": "0",
        }

    return {
        "B_i": "r0_i-T_i",
        "O_u": "-B_u+varrho_u",
        "O_u_signature": (
            "lower=Eq=-u, ainc=sum(u), W=target=0, ores=u"
        ),
        "placed_Cartan_residue": [str(value) for value in ALPHA],
        "placed_Cartan_terminal": [str(value) for value in TAU],
        "full_alpha_completion": {
            "identity": "O_alpha-K_alpha=-M_v",
            "signature": "lower=Eq=-alpha, terminal=-tau; other rows zero",
            "physical": True,
        },
        "single_pair_obstructions": records,
        "completion_criterion": (
            "the mandatory dressed O_u completes using the placed Cartan "
            "packet iff u lies in Q*alpha; the terminal coefficient is then "
            "forced by the same scalar"
        ),
    }


def q_and_scope_audit():
    return {
        "selected_Gate_I_odd_output": {
            "closed": True,
            "identity": "O_alpha-K_alpha=-M_v",
            "scope": (
                "normalized Y=1 canonical output-side repeated grade only; "
                "the 15-label input/lower comparison to this packet is not "
                "constructed by the Koszul identity"
            ),
            "Koszul_role": (
                "C_K supplies the unaugmented -F e_Eq core.  Identifying its "
                "complete labelled boundary with -M_v is precisely the still "
                "required source comparison, not a consequence of dtheta"
            ),
        },
        "physical_q": (
            "not determined by this augmented row solve.  It remains the "
            "protected quotient condition [q_target Phi-q_source]=0; a "
            "nonzero class is the relative-generator branch"
        ),
        "full_six_label_Cartan_orbit": {
            "constructed": False,
            "current_physical_span": "one canonical alpha line",
            "if_constructed": (
                "an equivariant Cartan orbit spanning the zero-sum residue "
                "hyperplane would complete every rho-odd u, with its forced "
                "linear combination of eta/sigma terminals"
            ),
        },
        "even_or_augmentation_one_u": (
            "B=r0-T forces ainc=sum(u) in O_u.  Requiring ainc=0 for "
            "sum(u)!=0 is still detected by sum(lower)+ainc and needs an "
            "independent primitive anchor cell"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    r0, cap, response, cartan = old_columns()
    dressing = primitive_dressing_audit(r0, cap, response, cartan)
    completion = cartan_completion_audit(r0, cap, response, cartan)
    scope = q_and_scope_audit()
    ledger = {
        "theorem": "exact Cartan/cap augmentation dressing of K_Eq",
        "pins": PINS,
        "row_order": (
            "lower_B0..B5, Eq_B0..B5, W_B0..B5, target_B0..B5, "
            "ores_B0..B5, ainc, eta/sigma_7"
        ),
        "physical_columns": {
            "r0_T_varrho": [N, N, N],
            "placed_endpoint_odd_Cartan": 1,
            "Mv_in_span": True,
        },
        "primitive_Koszul_dressing": dressing,
        "Cartan_completion": completion,
        "q_and_scope": scope,
        "true_remaining_augmentation": (
            "first attach lower=-u and ainc=sum(u) to the Eq core.  Then the "
            "remaining obstruction is the labelled residue class of u in "
            "Q^6/Q*alpha, together with its forced eta/sigma terminal.  For "
            "u=alpha this is already -M_v; for one rho pair it is nonzero"
        ),
        "frontier": (
            "the selected full-alpha odd output augmentation is already "
            "physical by the pinned M_v theorem.  Gate I is not closed: the "
            "remaining datum is the source-labelled map from the selected "
            "15-label/Koszul lower input to that physical -M_v output"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 reduced-Eq Cartan/cap augmentation dressing: PASS")
    print("full alpha: O_alpha-K_alpha=-M_v (physical)")
    print("single rho pair: NONZERO modulo the placed Cartan line")
    print("forced dressing: lower=Eq=-u, ainc=sum(u), terminal from Cartan")
    print("physical q: separate protected quotient condition")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
