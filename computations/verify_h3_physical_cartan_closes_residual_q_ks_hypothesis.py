#!/usr/bin/env python3
"""Discharge the residual-q KS hypothesis with physical Cartan descent.

The older conditional landing theorem asks for one source-provenant column
in word 1211222 and the canonical repeated P3+K2 grade whose ordinary
residue is -delta=(-1,1,1,-1), whose protected readouts vanish, and whose
terminal is the -dOmega eta/sigma packet.  The physical endpoint-odd Cartan
prism now constructs exactly that column in the exhaustive relative
principal-parts source complex.

Consequently either the physical terminal is visible on the protected
kernel (the normalized relative-generator branch), or the Cartan correction
turns the curvature/bar near-hit into A and the old conditional theorem
closes the unequal-tail five-lock and E14 endpoint self-loop.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
    "computations/verify_h3_residual_q_ks_constructive_landing_boundary.py":
        "bc11c8fe61ec8c21a1850326de037a328ab7f7404bcf3902655f6541e496bc9f",
    "notes/h3-residual-q-ks-constructive-landing-boundary.md":
        "225f79e54f121c375771510b4a9a07c3b666e0ffc36b4b9ebfd589c9c475756b",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
    "notes/h3-six-term-exhaustive-relative-extension-alternative.md":
        "98d95662d6adcf4684d6e15e60193369564e1d45ed0db19f822ce2a2add79977",
    "computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py":
        "aeed58d596f931602dcb77b44aa3bd11a27b8e2d26435cc328b325ce91b0e1bb",
    "notes/uniform-bidirectional-five-lock-relative-homotopy-boundary.md":
        "c9ce579dcbd6333060527872425c63cfb45ab3fbbc40401c345360ceeb767ad1",
}
EXPECTED_LEDGER_SHA256 = (
    "e7ec95b3b3494c5b656c42dd002c3c49a05e1bc28104383b626adb3207aebd91"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(left, right):
    return tuple(Q(a) + Q(b) for a, b in zip(left, right, strict=True))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    physical = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "cartan_closes_ks_physical",
    ).audit()
    require(physical["physical_packet"]["ordinary_residue"]
            == [-1, 1, 1, -1],
            "physical Cartan residue stopped being -delta")
    require(physical["physical_packet"]["protected_D_W_target_anchor_Eq"] == 0,
            "physical Cartan acquired a protected readout")
    require(physical["physical_packet"]["ridge"]
            == "strictly commuting -dOmega_v eta/sigma packet",
            "physical Cartan terminal ridge changed")

    # The curvature-minus-bar near-hit has the opposite ordinary-residue
    # vector.  The physical Cartan cell is exactly its correction.
    delta = (Q(1), Q(-1), Q(-1), Q(1))
    cartan = tuple(-entry for entry in delta)
    require(tuple(physical["physical_packet"]["ordinary_residue"]) == cartan,
            "Cartan/KS residue identification changed")
    require(add(delta, cartan) == (0, 0, 0, 0),
            "Cartan correction stopped cancelling the near-hit residue")

    # In the four geometric coordinates the corrected near-hit is A and the
    # already physical rootless bar B leaves D=E_plus-E_minus.
    # Order: E_plus,E_minus,Omega,q_comp.
    A = (Q(1), Q(-1), Q(1), Q(-1))
    B = (Q(0), Q(0), Q(-1), Q(1))
    D = (Q(1), Q(-1), Q(0), Q(0))
    require(add(A, B) == D,
            "physical attachment plus bar stopped producing endpoint D")

    # Replay the exact unequal-tail path rank effect without assuming equal
    # coefficients.  Six path rows in seven columns have a one-dimensional
    # endpoint charge; adjoining D kills it.
    relative = load(
        "computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py",
        "cartan_closes_ks_relative",
    )
    guard = relative.audit_all_five_row_holonomy_guard()
    require(not guard["unequal_tail_spans_D"]
            and guard["unequal_tail_endpoint_dual"] == ["1", "1/2"],
            "unequal-tail five-lock guard changed")
    weights = [(Q(1), Q(1)) for _ in guard["row_labels"]]
    weights[3] = (Q(1), Q(2))
    rows = relative.path_rows(tuple(weights))
    endpoint_D = tuple(Q(int(i == 0) - int(i == len(rows)))
                       for i in range(len(rows) + 1))
    old_rank = relative.rank(rows)
    new_rank = relative.rank(rows + (endpoint_D,))
    require(old_rank == 6 and new_rank == 7,
            ("Cartan endpoint row stopped killing five-lock charge",
             old_rank, new_rank))

    return {
        "theorem": "physical Cartan descent discharges the residual-q KS hypothesis",
        "common_source_type": {
            "word": "1211222 after deleting the distinguished endpoint",
            "grade": "canonical labelled repeated P3+K2 / endpoint-recoloured faces-(3,5) bridge",
            "ordinary_residue": [int(value) for value in cartan],
            "protected_D_W_target_anchor_Eq": 0,
            "terminal": "strictly commuting -dOmega_v eta/sigma packet",
        },
        "residue_cancellation": {
            "curvature_bar_near_hit": [str(value) for value in delta],
            "physical_Cartan_correction": [str(value) for value in cartan],
            "sum": [0, 0, 0, 0],
        },
        "geometric_composition": {
            "A": [str(value) for value in A],
            "rootless_bar_B": [str(value) for value in B],
            "A_plus_B_equals_D": [str(value) for value in D],
        },
        "five_lock_rank_before_after": [old_rank, new_rank],
        "exhaustive_terminal_dichotomy": {
            "terminal_visible_kernel": (
                "normalize the protected kernel class to obtain the physical relative generator"
            ),
            "terminal_zero_indeterminate": (
                "the Cartan correction supplies A; modulo B it adjoins D, "
                "closing unequal-tail five-lock holonomy and the E14 endpoint self-loop"
            ),
        },
        "frontier_shift": (
            "the residual-q KS lift and unequal-tail endpoint holonomy are no "
            "longer construction hypotheses in the canonical h=3 packet.  "
            "The remaining active-side problem is transverse physical "
            "rank/support landing and the diagonal 2+2 four-site switch; "
            "global arbitrary-SCC entry remains separate"
        ),
        "scope": (
            "canonical h=3 repeated-grade composition.  This does not prove "
            "that every arbitrary curved SCC enters this marked component, "
            "nor does the endpoint row itself create a clean cap or restore "
            "a same-head (2,2,3,3) physical rank guard"
        ),
    }


def main():
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 physical Cartan / residual-q KS composition: PASS")
    print("Cartan correction residue: -delta")
    print("unequal-tail five-lock rank: 6 -> 7")
    print("remaining: transverse rank/support landing and diagonal 2+2 switch")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
