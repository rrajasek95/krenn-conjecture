#!/usr/bin/env python3
"""Test the SDR/HPL repair of the full-star cap top projection.

The preceding exact cube computation gives

    [d,pi_top] N = (H_0-u)e_Eq.

This checker first proves the categorical obstruction: pi_top cannot be the
projection in an SDR before that commutator is killed, since every SDR
projection is a chain map.  It then builds the unique normalized universal
repair.  Adjoining K with dK=(H_0-u)e_Eq gives the standard two-by-two SDR;
homological perturbation changes the inclusion by -K and terminates after
one step.  The K direction is killed by the retraction, so transfer does not
produce a physical P2 arrow.  Source provenance still requires K itself to
be realized in the two occurrence-local q23/q45 objects.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py":
        "ce4d98c0160c86692c876879f90b69ae684d6d16bb3211d8ffe9a30fdc8c4e91",
    "computations/verify_h3_endpoint_even_literal_operator_algebra_r0_action_gate.py":
        "42a30f9cd823a67a0733dfb6961ed224e228caa3236140c2e0803db686839ef7",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
}
EXPECTED_LEDGER_SHA256 = "e2316ed92ad68bc9caf7bc52fa052b47e03f2572f508ed26bd3debd8f6783441"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(left, right):
    require(len(left) == len(right), (len(left), len(right)))
    return tuple(tuple(a + b for a, b in zip(lrow, rrow, strict=True))
                 for lrow, rrow in zip(left, right, strict=True))


def scale(value, matrix):
    return tuple(tuple(Q(value) * item for item in row) for row in matrix)


def matmul(left, right):
    require(left and right and len(left[0]) == len(right),
            (len(left[0]), len(right)))
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(sum((a * b for a, b in zip(row, column, strict=True)),
                           Q(0))
                       for column in columns)
                 for row in left)


def identity(size):
    return tuple(tuple(Q(row == column) for column in range(size))
                 for row in range(size))


def unaugmented_sdr_obstruction(cap_gate) -> dict[str, object]:
    ledger, digest = cap_gate.audit()
    require(digest == cap_gate.EXPECTED_LEDGER_SHA256, digest)
    defect_record = ledger["first_underived_module_associativity_defect"]
    require(defect_record["commutator"]
            == "[d,pi_top]N=(H_0-u)*e_Eq"
            and defect_record["homogenizer_coefficient"] == "-1",
            defect_record)

    # Derived top orbit X: dN=Y.  Underived physical orbit C before a K
    # filler: dB=Y+Eq.  The fixed top projection sends N to B and Y to Y.
    d_x = ((Q(1),),)                 # rows Y; columns N
    d_c = ((Q(1),), (Q(1),))        # rows Y,Eq; columns B
    pi_1 = ((Q(1),),)                # N -> B, written C1 <- X1
    pi_0 = ((Q(1),), (Q(0),))        # Y -> Y, written C0 <- X0
    chain_defect = add(matmul(d_c, pi_1),
                       scale(-1, matmul(pi_0, d_x)))
    require(chain_defect == ((Q(0),), (Q(1),)), chain_defect)

    # If dh+hd=id-i*pi, the right side commutes with d.  Hence i*pi, and in
    # particular pi in an SDR, must be a chain map.  The displayed rank-one
    # defect makes such an h impossible before adding a filler.
    return {
        "local_degree_one_basis": ["N (derived)", "B=r0-T (physical)"],
        "physical_degree_zero_basis": ["Y*w", "(H0-u)*Eq"],
        "d_derived_N": [1],
        "d_physical_B": [1, 1],
        "top_projection_chain_defect": [0, 1],
        "defect_rank": 1,
        "homogenizer_normalization": -1,
        "SDR_with_pi_top_exists": False,
        "reason": (
            "[d,dh+hd]=0 for every h, while [d,id-i*pi_top] contains the "
            "nonzero Eq defect"
        ),
        "HPL_expression_pAhAi_defined_on_physical_complex": False,
    }


def universal_one_cell_repair() -> dict[str, object]:
    # C1=(B,K), C0=(Y,Eq).  Start with the split differential d0 and regard
    # Delta(B)=Eq as the perturbation measured by the cap commutator.
    d0 = ((Q(1), Q(0)), (Q(0), Q(1)))
    delta = ((Q(0), Q(0)), (Q(1), Q(0)))
    d = add(d0, delta)
    require(d == ((Q(1), Q(0)), (Q(1), Q(1))), d)

    d_x = ((Q(1),),)
    p1 = ((Q(1), Q(0)),)             # B -> N, K -> 0
    p0 = ((Q(1), Q(0)),)             # Y -> Y, Eq -> 0
    i1 = ((Q(1),), (Q(0),))          # N -> B before perturbation
    i0 = ((Q(1),), (Q(0),))          # Y -> Y
    h = ((Q(0), Q(0)), (Q(0), Q(1))) # h(Eq)=K

    require(matmul(d0, i1) == matmul(i0, d_x)
            and matmul(p0, d0) == matmul(d_x, p1),
            "split maps stopped being chain maps")
    require(matmul(p1, i1) == identity(1)
            and matmul(p0, i0) == identity(1),
            "split p*i stopped being the identity")
    require(matmul(h, d0) == add(identity(2), scale(-1, matmul(i1, p1)))
            and matmul(d0, h) == add(
                identity(2), scale(-1, matmul(i0, p0))),
            "split Euler homotopy identity changed")

    # Standard first HPL correction to the inclusion.  Since Delta*K=0,
    # every higher correction vanishes.
    first_correction = scale(-1, matmul(h, matmul(delta, i1)))
    require(first_correction == ((Q(0),), (Q(-1),)), first_correction)
    corrected_i1 = add(i1, first_correction)
    require(corrected_i1 == ((Q(1),), (Q(-1),))
            and matmul(d, corrected_i1) == matmul(i0, d_x),
            "B-K stopped cancelling the Eq commutator")
    require(matmul(delta, matmul(h, matmul(delta, i1)))
            == ((Q(0),), (Q(0),)),
            "the HPL series stopped terminating")

    # Retraction kills the correction direction.  Thus a projected higher
    # term cannot turn this universal contractible K into a physical P2
    # operation; retaining/source-labelling K is the missing datum.
    require(matmul(p1, first_correction) == ((Q(0),),),
            "the contractible K direction survived retraction")
    return {
        "universal_added_cell": "K",
        "boundary": "dK=(H0-u)*e_Eq",
        "split_homotopy": "h((H0-u)*e_Eq)=K; h(Y*w)=0",
        "first_HPL_inclusion_correction": "-K",
        "corrected_inclusion": "i'(N)=B-K",
        "corrected_chain_equation": "d(B-K)=Y*w",
        "higher_HPL_terms": 0,
        "retraction_of_K": 0,
        "projected_second_transfer_term": 0,
        "uniqueness": (
            "with coefficient of B normalized to one and no degree-one "
            "cycle added, the coefficient of K is uniquely -1"
        ),
        "interpretation": (
            "HPL does not synthesize the physical Eq/P2 operation; it says "
            "exactly which extra cell must already be retained"
        ),
    }


def physical_grade_gate(operator_gate, private_gate) -> dict[str, object]:
    operator_ledger, operator_digest = operator_gate.audit()
    require(operator_digest == operator_gate.EXPECTED_LEDGER_SHA256,
            operator_digest)
    private_ledger, private_digest = private_gate.audit()
    require(private_digest == private_gate.EXPECTED_LEDGER_SHA256,
            private_digest)
    face = operator_ledger["first_M_N_q01_cyclic_module_relation"]
    export = operator_ledger["first_typed_Leibniz_export"]
    typed = export["typed_export"]
    physical = face["current_literal_Hom_response_cap"]
    reinsertion = private_ledger["q23_reinsertion"]
    require(physical == 0
            and not export["current_source_contains_required_occurrence_local_section"]
            and typed["detector_value"] == "35/72"
            and reinsertion["ordinary_residue_aggregate"] == 0,
            (face, export, reinsertion))
    return {
        "formal_K_grade": "contractible translated-Hasse/Eq fibre",
        "required_physical_K_grades": [
            "0112/q23:21/P2", "0121/q45:12/P2"
        ],
        "current_literal_Hom_response_cap": physical,
        "formal_retraction_hits_required_P2_grades": False,
        "first_required_q_face": "0102/dq23:21",
        "first_q_face_detector": typed["primitive_detector"],
        "first_q_face_detector_value": typed["detector_value"],
        "sigma_mate": "0121/dq45:12 with value 35/72",
        "ordinary_residue_aggregate": reinsertion[
            "ordinary_residue_aggregate"],
        "sharp_failure": (
            "the universal K is derived/off-operation-grade.  Giving it the "
            "two P2 word/fine/repeated labels is precisely the missing "
            "physical constructor, not a consequence of cubical contraction"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    cap_gate = load(
        "computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py",
        "cap_top_hpl_cap_gate",
    )
    operator_gate = load(
        "computations/verify_h3_endpoint_even_literal_operator_algebra_r0_action_gate.py",
        "cap_top_hpl_operator_gate",
    )
    private_gate = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "cap_top_hpl_private_gate",
    )
    ledger = {
        "theorem": "h3 cap top SDR/HPL transfer no-go and universal repair",
        "pins": PINS,
        "unaugmented_SDR_obstruction": unaugmented_sdr_obstruction(cap_gate),
        "universal_one_cell_HPL_repair": universal_one_cell_repair(),
        "physical_word_fine_operation_gate": physical_grade_gate(
            operator_gate, private_gate),
        "verdict": (
            "The proposed HPL transfer cannot start with pi_top in the "
            "current physical complex because pi_top is not a chain map.  "
            "The exact rank-one obstruction is (H0-u)e_Eq.  Universally, "
            "one cell K with that boundary gives an explicit SDR and the "
            "HPL correction i'(N)=B-K; the series terminates immediately.  "
            "But K is killed by retraction and lives in the derived Hasse/"
            "Eq fibre, so the projected correction is zero.  Promoting K to "
            "the two occurrence-local P2 word/fine/operation grades is "
            "exactly the missing physical axiom and conditionally forces "
            "the 35/72 dq23/dq45 faces"
        ),
        "scope": (
            "exact normalized local orbit of the canonical h3 cap cube; "
            "standard two-by-two rational SDR and complete terminating HPL "
            "series; current literal Hom and q23/sigma typed detector.  This "
            "does not classify arbitrary enlarged source algebras or prove "
            "that a physical P2-labelled K cannot exist in an unmodeled "
            "constructor"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("cap top SDR/HPL ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "obstruction", "repair", "physical"), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        obstruction = ledger["unaugmented_SDR_obstruction"]
        repair = ledger["universal_one_cell_HPL_repair"]
        physical = ledger["physical_word_fine_operation_gate"]
        print(f"h3 cap top SDR/HPL gate ({arguments.mode}): PASS")
        print("unaugmented pi_top SDR:",
              "YES" if obstruction["SDR_with_pi_top_exists"] else "NO")
        print("universal correction:",
              repair["first_HPL_inclusion_correction"])
        print("projected correction:",
              repair["projected_second_transfer_term"])
        print("physical P2 landing:",
              physical["formal_retraction_hits_required_P2_grades"])
        print("dq detector:", physical["first_q_face_detector_value"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
