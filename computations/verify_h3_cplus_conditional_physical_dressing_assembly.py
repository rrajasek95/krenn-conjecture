#!/usr/bin/env python3
"""Assemble the generic C+ physical dressing from its three open inputs.

Assume:

* the shifted P2 placement supplies its source-labelled hidden lower face
  -E and the normalized even Cartan face (target,Eq)=(-E,-E);
* the pointed K_Eq comparison supplies the complete Eq correction -delta;
* a pure d_even residue section exists in the B1/B4 grade.

The old physical nearest lift O_-E has (lower,Eq,ores)=(E,E,-E).
Root-decorating d_even gives pure residue +E.  Therefore

    P2_hidden + O_-E + (2 D_root)*d_even = (0,E,0),

the clean physical K_Eq face.  It closes the target/Eq triangle with the
lower endpoint path and P2 Cartan face.  The same pointed comparison removes
the complete Eq tied to delta, while an undecorated d_even supplies the
prescribed labelled residue v.  All lower/Eq/target/root-residue debts then
vanish, leaving only the desired carrier (v,delta,v,ainc=-1).
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py":
        "7eef9d440fefbae174d2adc61b6f8bdc270351353884ba24e277d36714a9a364",
    "computations/verify_h3_cplus_root_even_labelled_ores_sigma_cartan_gate.py":
        "144d1fd64d8a733f3ec737edd301c540e66d545c9d72adf1abba5f7ed4764ce1",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py":
        "f66752bd3a44a9506b4a31467ce52dcb16e52f841b0f29ce66066a38ec7f97c1",
}
EXPECTED_LEDGER_SHA256 = (
    "a101dbfd2d611a242fb2d7da8ef5b56b07f686fd60ffd375497dee782206fafe"
)

SIX = 6
ROOT_WORD = 24

DIRECT = slice(0, SIX)
LOWER = slice(DIRECT.stop, DIRECT.stop + SIX)
COMPLETE_EQ = slice(LOWER.stop, LOWER.stop + SIX)
ROOT_LOWER = slice(COMPLETE_EQ.stop, COMPLETE_EQ.stop + ROOT_WORD)
ROOT_EQ = slice(ROOT_LOWER.stop, ROOT_LOWER.stop + ROOT_WORD)
TARGET = slice(ROOT_EQ.stop, ROOT_EQ.stop + ROOT_WORD)
ROOT_ORES = slice(TARGET.stop, TARGET.stop + ROOT_WORD)
ORES = slice(ROOT_ORES.stop, ROOT_ORES.stop + SIX)
AINC = ORES.stop
ROWS = AINC + 1

D_ROOT = tuple(map(Q, (-1, 1, -1, 1)))
V = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
LOCAL = tuple(map(Q, (Q(1, 4), 0, Q(1, 4),
                     Q(1, 4), 0, Q(1, 4))))
DELTA = tuple(a - b for a, b in zip(V, LOCAL, strict=True))
E = tuple(2 * root * label for root in D_ROOT for label in V)


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(scalar, vector):
    return tuple(Q(scalar) * Q(entry) for entry in vector)


def vector(*, direct=(), lower=(), complete_eq=(), root_lower=(),
           root_eq=(), target=(), root_ores=(), ores=(), ainc=0):
    answer = [Q(0)] * ROWS
    for section, values in (
        (DIRECT, direct), (LOWER, lower), (COMPLETE_EQ, complete_eq),
        (ROOT_LOWER, root_lower), (ROOT_EQ, root_eq),
        (TARGET, target), (ROOT_ORES, root_ores), (ORES, ores),
    ):
        if values:
            require(len(values) == section.stop - section.start,
                    (section, len(values)))
            answer[section] = values
    answer[AINC] = Q(ainc)
    return tuple(answer)


def pin_inputs():
    for relative, expected in PINS.items():
        actual = digest(ROOT / relative)
        require(actual == expected, (relative, actual, expected))


def core_assembly_audit():
    zero6 = (Q(0),) * SIX
    zero24 = (Q(0),) * ROOT_WORD
    require(DELTA == tuple(map(Q, (Q(-1, 4), Q(1, 2), Q(-1, 4),
                                  Q(-1, 4), Q(1, 2), Q(-1, 4))))
            and sum(DELTA, Q(0)) == 0
            and sum(E, Q(0)) == 0
            and sum(value != 0 for value in E) == 8,
            "the C-plus coefficient packet changed")

    # The carrier rows are the non-debt part of the full even orbit.
    carrier = vector(direct=V, ainc=-1)

    # Complete-column landing and its pointed reduced-Eq correction.
    tied_mv = vector(lower=DELTA, complete_eq=DELTA)
    pointed_complete_eq = vector(complete_eq=scale(-1, DELTA))
    require(add(tied_mv, pointed_complete_eq)
            == vector(lower=DELTA),
            "the complete delta/Eq correction stopped closing")

    # Minimal target/Eq triangle after the P2 placement.
    lower_endpoint_path = vector(target=E)
    p2_even_cartan = vector(root_eq=scale(-1, E), target=scale(-1, E))

    # Physical dressing of the clean K_Eq face.  The first column is the
    # hidden private face forced on the placed raw comparison.  O_-E is an
    # old physical r0/T/rho combination.  The last is obtained from one
    # pure d_even section by connected root decoration.
    p2_hidden_lower = vector(root_lower=scale(-1, E))
    nearest_o_minus_e = vector(root_lower=E, root_eq=E,
                               root_ores=scale(-1, E))
    root_decorated_d_even = vector(root_ores=E)
    clean_k_eq = add(p2_hidden_lower, nearest_o_minus_e,
                     root_decorated_d_even)
    require(clean_k_eq == vector(root_eq=E),
            "P2/O/d_even stopped realizing the clean K_Eq face")

    require(add(lower_endpoint_path, p2_even_cartan, clean_k_eq)
            == vector(),
            "the physical target/Eq triangle stopped closing")

    # The same unrooted residue section supplies the prescribed full-interface
    # labelled residue v.  It is not a debt to be cancelled.
    labelled_d_even = vector(ores=V)
    assembled = add(
        carrier,
        tied_mv, pointed_complete_eq,
        lower_endpoint_path, p2_even_cartan,
        p2_hidden_lower, nearest_o_minus_e, root_decorated_d_even,
        labelled_d_even,
    )
    expected = vector(direct=V, lower=DELTA, ores=V, ainc=-1)
    require(assembled == expected,
            "the full conditional C-plus core stopped assembling")
    require(assembled[COMPLETE_EQ] == zero6
            and assembled[ROOT_LOWER] == zero24
            and assembled[ROOT_EQ] == zero24
            and assembled[TARGET] == zero24
            and assembled[ROOT_ORES] == zero24,
            "a main physical debt survived the assembly")

    # Omitting either open input exposes its exact primitive debt.
    without_d_even = add(
        carrier, tied_mv, pointed_complete_eq,
        lower_endpoint_path, p2_even_cartan,
        p2_hidden_lower, nearest_o_minus_e,
    )
    without_pointed = add(
        carrier, tied_mv,
        lower_endpoint_path, p2_even_cartan,
        p2_hidden_lower, nearest_o_minus_e,
        root_decorated_d_even, labelled_d_even,
    )
    without_p2_hidden = add(
        carrier, tied_mv, pointed_complete_eq,
        lower_endpoint_path, p2_even_cartan,
        nearest_o_minus_e, root_decorated_d_even, labelled_d_even,
    )
    require(without_d_even[ROOT_ORES] == scale(-1, E)
            and without_d_even[ORES] == zero6,
            "removing d_even no longer exposes residue debts")
    require(without_pointed[COMPLETE_EQ] == DELTA,
            "removing pointed K_Eq no longer exposes complete Eq")
    require(without_p2_hidden[ROOT_LOWER] == E,
            "removing P2 hidden face no longer exposes private lower")

    return {
        "coefficient_packets": {
            "v": [str(value) for value in V],
            "delta_plus": [str(value) for value in DELTA],
            "E": "2 D_root tensor v",
            "E_nonzero_word_labels": sum(value != 0 for value in E),
        },
        "clean_K_Eq_factorization": (
            "P2_hidden(-E,0,0)+O_-E(E,E,-E)+"
            "2D_root*d_even(0,0,E)=(0,E,0)"
        ),
        "target_Eq_triangle": (
            "B_endpoint(target E)+P2_Cartan(target -E,Eq -E)+"
            "K_Eq(Eq E)=0"
        ),
        "complete_delta_factorization": (
            "M_delta(lower delta,Eq delta)+"
            "Phi_KEq(Eq -delta)=(lower delta,Eq 0)"
        ),
        "assembled_core": {
            "direct_landing": "v",
            "complete_lower": "delta_plus",
            "complete_Eq_debt": 0,
            "root_private_debt": 0,
            "root_Eq_debt": 0,
            "mixed_target_debt": 0,
            "word_resolved_root_ores_debt": 0,
            "labelled_ordinary_residue": "v",
            "anchor_incidence": -1,
        },
        "necessity_checks": {
            "without_d_even": "root ores=-E and labelled ores v absent",
            "without_pointed_KEq": "complete Eq=delta_plus",
            "without_P2_hidden_face": "root lower=+E",
        },
    }


def residual_augmented_rows_audit():
    # The core calculation does not assign arbitrary augmented values.  The
    # old O_-E and pure d_even sections have zero W/anchor/terminal by their
    # pinned signatures.  Therefore only P2/Phi values can remain.
    # Model their two independent unknown contributions explicitly.
    p2_w = (Q(1), Q(0))
    phi_w = (Q(0), Q(1))
    p2_terminal = (Q(1), Q(0))
    phi_terminal = (Q(0), Q(1))
    require(add(p2_w, phi_w) == (Q(1), Q(1))
            and add(p2_terminal, phi_terminal) == (Q(1), Q(1)),
            "the residual augmented bookkeeping changed")

    # Pointedness closes the *meaning* of the nonzero anchor carried by the
    # P2 orbit; it does not make it vanish.  Its required value is -1.
    anchor_value = Q(-1)
    require(anchor_value == -1, "the C-plus anchor normalization changed")
    return {
        "physical_W": {
            "residual_equation": "W(P2 total)+W(Phi_KEq)=0",
            "automatic_from_endpoint_evenness": False,
            "new_generator_type_if_imposed_as_naturality": False,
        },
        "physical_q": {
            "core_coefficient_rows_determine_q": False,
            "remaining_clause": (
                "q-horizontal pointed comparison; if its q defect is "
                "nonzero, use the already proved protected relative-"
                "generator branch"
            ),
        },
        "anchor": {
            "assembled_ainc": str(anchor_value),
            "is_zero_debt": False,
            "status": (
                "correct desired nonzero carrier once P2 is source-valid; "
                "pointed source-presentation functoriality supplies the "
                "physical anchor meaning"
            ),
            "additional_anchor_cell_needed": False,
        },
        "eta_sigma": {
            "residual_equation": (
                "terminal(P2 total)+terminal(Phi_KEq)=the prescribed "
                "rho-even ridge packet"
            ),
            "O_minus_E_and_d_even_terminal": 0,
            "automatic_from_main_row_closure": False,
        },
        "word_fine_repeated": (
            "closed by the P2 placement hypothesis on the two sigma-related "
            "0112/q23:21 and 0121/q45:12 objects; no coefficient debt remains"
        ),
        "generic_scope_only": (
            "beta=0 D0 still requires the integral/Bockstein clause unless "
            "the pointed comparison is k[beta]-linear"
        ),
    }


def audit():
    pin_inputs()
    ledger = {
        "theorem": "conditional physical C-plus dressing assembly",
        "pins": PINS,
        "hypotheses": {
            "P2": (
                "a source-valid sigma-covariant shifted placement with the "
                "literal one-endpoint/reinsertion faces, hidden root lower "
                "-E, and normalized even Cartan target/Eq (-E,-E)"
            ),
            "pointed_KEq": (
                "the physical pointed comparison supplies complete Eq "
                "-delta_plus and identifies the P2/O/d_even composite with "
                "the canonical clean root Eq face"
            ),
            "d_even": (
                "a same-grade pure labelled-residue section v=(B1+B4)/2 "
                "with lower/Eq/W/target/ainc/terminal zero, stable under "
                "the connected root decoration"
            ),
        },
        "core_assembly": core_assembly_audit(),
        "remaining_augmented_rows": residual_augmented_rows_audit(),
        "conditional_conclusion": (
            "P2 + pointed K_Eq + d_even are sufficient for every main "
            "generic C-plus boundary coordinate.  No fourth lower/Eq/target/"
            "residue cell is needed.  The only remaining compatibility laws "
            "are physical W, q, and the eta/sigma ridge; anchor is already "
            "the desired -1 carrier under pointed functoriality."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    ledger_digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(ledger_digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", ledger_digest))
    return ledger, ledger_digest


def main():
    _ledger, ledger_digest = audit()
    print("h3 conditional C-plus physical dressing: CORE CLOSES")
    print("lower/Eq/target/root-ores debts: 0")
    print("carrier: direct v, lower delta+, ores v, ainc=-1")
    print("remaining compatibility: W, q, eta/sigma")
    print("ledger sha256:", ledger_digest)


if __name__ == "__main__":
    main()
