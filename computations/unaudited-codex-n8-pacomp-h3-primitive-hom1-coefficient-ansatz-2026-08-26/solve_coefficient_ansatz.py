#!/usr/bin/env python3
"""Solve the smallest source-labelled Lambda/Pi coefficient ansatz over Q."""
from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
H = Path(__file__).resolve().parent
PINS = {
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-total-constructor-composite-closure-decision-2026-08-26/MANIFEST.sha256": "d1955e8d6ed106f1653eca787bb7c7ce0fc497440361cd230c32b8262e020a50",
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-total-constructor-composite-closure-decision-2026-08-26/results_composite_closure_decision.json": "b82ede23a42ccfa8841bd2f190bc25d370ba20b847dd807019c4164f7ac2d85c",
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-minimal-total-placement-decision-2026-08-26/MANIFEST.sha256": "08ca6c914cb2d3a429a652f516a85ecd6008330d37ba0f2214c71e1651a354c3",
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-source-column-detector-census-2026-08-25/results_source_column_detector_census.json": "40f629bd815441e2e1a4390d148016a2b5b1b409a41b619ceaab43d62a85c122",
    ROOT / "computations/unaudited-codex-n8-pacomp-x23-absolute-carrier-boundary-audit-2026-08-25/MANIFEST.sha256": "f443971c89f61ecd255e5e23840936b52f41e3aea10a29ef1c544239223bcdc4",
    ROOT / "computations/unaudited-codex-n8-pacomp-x23-total-carrier-et-construction-audit-2026-08-25/MANIFEST.sha256": "f4c40ad4801fcf2950af2871e46eb6971e3a5fee12f124a8f37367d6e343117b",
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-switch-charge-nonimplication-referee-2026-08-25/FINAL_MANIFEST.sha256": "4ba7073930e2c59c5f760fb0e24309fe08b0086cb105f3d1ce1bae62b56f2800",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def transpose(columns):
    return tuple(tuple(Q(columns[column][row]) for column in range(len(columns))) for row in range(len(columns[0])))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    rows = [list(row) for row in transpose(columns)]
    height = len(rows)
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height) if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


for path, expected in PINS.items():
    require(path.is_file() and sha(path) == expected, (path, sha(path), expected))

closure = json.loads((ROOT / "computations/unaudited-codex-n8-pacomp-h3-total-constructor-composite-closure-decision-2026-08-26/results_composite_closure_decision.json").read_text())
require(closure["actual_constructor_search"]["existing_candidate_records"] == 0 and closure["source_derived_closure"]["operation_changing_atoms"] == 0, closure["actual_constructor_search"])

# Quotient reduction is exact. Every internal primitive, every allowed
# reindexing, and all four formal switch mates has top detector zero. The only
# genuine source columns with nonzero top shadow are Gamma_B and Gamma_C,
# which retain t_B and t_C respectively. Coordinates are (eta_top,t_B,t_C).
top_names = ("switch_aB", "switch_aC", "switch_bB", "switch_bC", "Gamma_B", "Gamma_C")
top_columns = (
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
)
top_matrix = transpose(top_columns)
top_target = (2, 0, 0)
top_farkas = (1, -1, -1)
require(all(dot(top_farkas, column) == 0 for column in top_columns) and dot(top_farkas, top_target) == 2, "top Farkas")
require(rank(top_columns) == 2 and rank(top_columns + (top_target,)) == 3, "top rank")

# In the face-complete retained quotient, all four generous source rows have
# eta_r=0 while R_ret has eta_r=1. Coordinates consist only of eta_r.
retained_names = ("face_A0", "face_A1", "face_B0", "face_B1")
retained_columns = ((0,), (0,), (0,), (0,))
retained_matrix = transpose(retained_columns)
lambda_retained_target = (1,)
pi_retained_target = (-1,)
retained_farkas = (1,)
require(all(dot(retained_farkas, column) == 0 for column in retained_columns), "retained Farkas")
require(dot(retained_farkas, lambda_retained_target) == 1 and dot(retained_farkas, pi_retained_target) == -1, "retained targets")
require(rank(retained_columns) == 0 and rank(retained_columns + (lambda_retained_target,)) == 1, "retained rank")

instances = ("AB/q23", "AB/q45", "AC/q23", "AC/q45")
variables_per_instance = len(top_columns) + 2 * len(retained_columns)
require(variables_per_instance == 14, variables_per_instance)

# Materialize all 12 vector boundary equations: three per instance. In the
# exact quotient they expand to 20 rational scalar equations in 56 variables.
boundary_equations = []
for instance in instances:
    boundary_equations.extend([
        {"instance": instance, "unknowns": [f"lambda_top:{name}" for name in top_names], "matrix": [[str(entry) for entry in row] for row in top_matrix], "rhs": [str(entry) for entry in top_target], "name": "partial_0 Lambda_01=L01", "expanded_scalar_equations": 3},
        {"instance": instance, "unknowns": [f"lambda_retained:{name}" for name in retained_names], "matrix": [[str(entry) for entry in row] for row in retained_matrix], "rhs": [str(entry) for entry in lambda_retained_target], "name": "partial_1 Lambda_01=R_ret", "expanded_scalar_equations": 1},
        {"instance": instance, "unknowns": [f"pi_retained:{name}" for name in retained_names], "matrix": [[str(entry) for entry in row] for row in retained_matrix], "rhs": [str(entry) for entry in pi_retained_target], "name": "partial_0 Pi_r,01=-R_ret", "expanded_scalar_equations": 1},
    ])
require(len(boundary_equations) == 12 and sum(item["expanded_scalar_equations"] for item in boundary_equations) == 20, "boundary census")

# Coherence is imposed on the entire coefficient blocks. The signs are the
# frozen required character of the prior interface, not a claim that a source
# action on the missing records has already been built.
coherence_equations = [
    "tau(lambda_AB,q23)+lambda_AC,q23=0",
    "tau(lambda_AB,q45)+lambda_AC,q45=0",
    "tau(pi_AB,q23)+pi_AC,q23=0",
    "tau(pi_AB,q45)+pi_AC,q45=0",
    "sigma(lambda_AB,q23)-lambda_AB,q45=0",
    "sigma(lambda_AC,q23)-lambda_AC,q45=0",
    "sigma(pi_AB,q23)-pi_AB,q45=0",
    "sigma(pi_AC,q23)-pi_AC,q45=0",
]

# The five exact face requirements do not rescue the inconsistent quotient;
# they further restrict it. Record their literal source-labelled form.
face_checks = [
    {"name": "L01_PP_faces", "requirement": "36 terms; DQ,PS01,PS10 coefficients 2,-1,-1"},
    {"name": "relative_C4_mixed", "requirement": "+x'y'U and -x'y'U cancel termwise"},
    {"name": "retained_face", "requirement": "-2*d(D*q01)*r_DQ+d(p0*s1)*r_PS01+d(p1*s0)*r_PS10"},
    {"name": "Pi_correction", "requirement": "negative of retained_face"},
    {"name": "protected_descendants", "requirement": "q,anchor,W,ridge,residue,Eq readouts all zero"},
]

# Positive control: adjoining one genuinely new top primitive and one retained
# correction primitive makes the quotient equations solvable with coefficient
# one. This proves the no-go is about source availability, not normalization.
top_new = top_columns + (top_target,)
retained_new = retained_columns + ((1,),)
require(rank(top_new) == 3 and matvec(transpose(top_new), (0, 0, 0, 0, 0, 0, 1)) == top_target, "top positive control")
require(rank(retained_new) == 1 and matvec(transpose(retained_new), (0, 0, 0, 0, 1)) == (1,), "retained positive control")
require(matvec(transpose(retained_new), (0, 0, 0, 0, -1)) == (-1,), "Pi positive control")

certificates = {
    "top": {"left_witness": list(top_farkas), "witness_times_every_column": [str(dot(top_farkas, column)) for column in top_columns], "witness_times_rhs": str(dot(top_farkas, top_target)), "rank_A": 2, "rank_A_augmented": 3},
    "lambda_retained": {"left_witness": list(retained_farkas), "witness_times_every_column": ["0"] * 4, "witness_times_rhs": "1", "rank_A": 0, "rank_A_augmented": 1},
    "pi_retained": {"left_witness": list(retained_farkas), "witness_times_every_column": ["0"] * 4, "witness_times_rhs": "-1", "rank_A": 0, "rank_A_augmented": 1},
}

result = {
    "schema": "PACOMP_H3_PRIMITIVE_HOM1_COEFFICIENT_ANSATZ_V1",
    "status": "PASS_EXACT_Q_INCONSISTENT_FARKAS_CERTIFICATE_FOR_MAXIMAL_PINNED_ANSATZ",
    "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    "ansatz": {
        "scope": "quotient of the maximal pinned source ansatz by the joint detector-dark subspace",
        "instances": list(instances),
        "variables_per_instance": variables_per_instance,
        "total_variables_before_coherence": variables_per_instance * len(instances),
        "top_source_terms": list(top_names),
        "retained_source_terms": list(retained_names),
        "why_general_in_scope": "all 100 admissible primitives, 28,800 reindexings, internal composites, and eight standard interchanges map to zero in this quotient; Gamma_B/Gamma_C are the only nonzero top shadows and all four face-complete rows are retained",
    },
    "system": {
        "field": "Q",
        "polynomial_degree": 1,
        "boundary_vector_equations": boundary_equations,
        "boundary_vector_equation_count": 12,
        "expanded_boundary_scalar_equation_count": 20,
        "coherence_equations": coherence_equations,
        "coherence_equation_count": 8,
        "face_checks": face_checks,
        "face_check_count": 5,
    },
    "farkas_certificates": certificates,
    "solution": {"exists": False, "failure_before_coherence": True, "failure_before_face_checks": True, "valid_Lambda_formula": None, "valid_Pi_formula": None},
    "positive_control": {"new_top_primitive_signature": [2, 0, 0], "new_retained_primitive_signature": [1], "coefficients": {"Lambda_top": 1, "Lambda_retained": 1, "Pi_retained": -1}, "status": "PASS_FORMAL_FREE_EXTENSION_ONLY"},
    "minimal_new_data_after_no_go": {
        "top": "one primitive source record outside the pinned ansatz with quotient signature (eta,tB,tC)=(2,0,0)",
        "retained": "one primitive source record with eta_r=1, used with coefficients +1 for Lambda and -1 for Pi",
        "coherence": "the four labelled transports must satisfy all eight frozen tau/sigma equations",
    },
    "scope": {"h": 3, "maximal_pinned_and_formally_granted_switch_ansatz": True, "unregistered_primitive_Hom1_excluded": False, "heavy_external_solver_runs": 0, "PAComp_promotion": False, "uniform_descent_promotion": False, "conjecture_promotion": False},
    "verdict": "The exact Q system has no solution in the maximal pinned source-labelled ansatz, even before coherence or descendant checks. The top Farkas covector eta-t_B-t_C kills every switch/Gamma source term but reads 2 on L01. Independently eta_r kills every retained row but reads +1 on R_ret and -1 on its correction target. A valid total constructor therefore requires genuinely new primitive Hom1 source records with the two displayed quotient signatures; this no-go does not exclude such an unregistered primitive.",
}

temporary = H / "results_coefficient_ansatz.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, H / "results_coefficient_ansatz.json")
certificate = {
    "schema": "PACOMP_H3_PRIMITIVE_HOM1_FARKAS_CERTIFICATE_V1",
    "field": "Q",
    "top_matrix_rows": [[str(entry) for entry in row] for row in top_matrix],
    "top_rhs": [str(entry) for entry in top_target],
    "retained_matrix_rows": [[str(entry) for entry in row] for row in retained_matrix],
    "lambda_retained_rhs": ["1"],
    "pi_retained_rhs": ["-1"],
    "certificates": certificates,
    "status": "PASS_LITERAL_LEFT_KERNEL_WITNESSES",
}
temporary = H / "farkas_certificate.json.tmp"
temporary.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
os.replace(temporary, H / "farkas_certificate.json")
print(json.dumps({"status": result["status"], "variables": 56, "boundary_vector_equations": 12, "coherence_equations": 8, "face_checks": 5, "solution": False, "heavy_external_solver_runs": 0}, sort_keys=True))
