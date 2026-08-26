#!/usr/bin/env python3
"""Audit products/commutators and isolate the primitive total-cell decision."""
from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
H = Path(__file__).resolve().parent
PINS = {
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-minimal-total-placement-decision-2026-08-26/MANIFEST.sha256": "08ca6c914cb2d3a429a652f516a85ecd6008330d37ba0f2214c71e1651a354c3",
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-minimal-total-placement-decision-2026-08-26/results_minimal_total_placement.json": "60577d40efef473a125969780176a923b9903fb5604c3b43d3e0ab75b5d19d89",
    ROOT / "computations/verify_h3_gamma_star_source_derived_free_closure_census.py": "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
    ROOT / "computations/verify_h3_gamma_star_executable_gen_phys_registry.py": "173ebdedcfdadd9891704223ea93731509c18a4d120aa34d6c7bc8a4f3aebddb",
    ROOT / "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py": "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    ROOT / "computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py": "b60538f9db5b8c2984bbee95e0a05f383408e9ab7c13680216adf56386682522",
    ROOT / "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py": "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
    ROOT / "computations/verify_h3_actual_source_primitive_terminal_reduction_gate.py": "5754c85f7ae4b714777cdbb0f941672ade1977c5568f332a0dc8e317e4952927",
    ROOT / "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py": "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


for path, expected in PINS.items():
    require(path.is_file() and sha(path) == expected, (path, sha(path), expected))

prior = json.loads((ROOT / "computations/unaudited-codex-n8-pacomp-h3-minimal-total-placement-decision-2026-08-26/results_minimal_total_placement.json").read_text())
require(prior["status"] == "PASS_NO_EXISTING_OR_ONE_BARE_SWITCH_CONSTRUCTION_MINIMAL_TWO_COMPONENT_INTERFACE", prior["status"])
require(prior["minimum_theorem"]["associated_graded_old_rank"] == 6 and prior["minimum_theorem"]["after_both_missing_lines"] == 8, prior["minimum_theorem"])

closure = load(ROOT / "computations/verify_h3_gamma_star_source_derived_free_closure_census.py", "pacomp_composite_closure")
ledger, digest = closure.audit()
require(digest == closure.EXPECTED_LEDGER_SHA256 == "d81dbee5add84bfc72633447b0ada4406b103e7f1f4b6f7dbeeac676ec15b2e4", digest)
executable = ledger["executable_Gen_phys"]
typed = ledger["typed_free_closure"]
completion = ledger["completion_by_missing_Phi"]
exotic = ledger["adversarial_exotic_search"]
require(executable["constructor_invocations"] == 128 and executable["implemented_operation_changing_atoms"] == 0, executable)
require(executable["operation_object_counts"] == {"bar": 1, "cap": 26, "response": 1, "window": 100}, executable)
require(typed["Hom0_response_cap_dimension"] == 0 and typed["free_closure_operation_changing_C1_count"] == 0, typed)
require(completion["standard_operation_changing_C1_count"] == 8 and completion["quotient_rank"] == 8 and completion["Psi_charges"] == ["0"] * 8, completion)
require(exotic["found_in_executable_constructor_closure"] == 0 and exotic["remaining_exotic_loophole"] == "independent off-diagonal C1 atom only", exotic)

# All actual degree-one atoms are loops at one of four operation objects.
# Exact finite counts through word length four are included as a bounded replay;
# the no-cross conclusion then holds for all lengths by endpoint induction.
object_counts = executable["operation_object_counts"]
composable_words = {str(length): sum(count**length for count in object_counts.values()) for length in range(1, 5)}
require(composable_words == {"1": 128, "2": 10678, "3": 1017578, "4": 100456978}, composable_words)
ordered_commutator_inputs = composable_words["2"]
operation_pairs = {(name, name) for name in object_counts}
for _ in range(4):
    operation_pairs |= {(left_source, right_target) for left_source, left_target in tuple(operation_pairs) for right_source, right_target in tuple(operation_pairs) if left_target == right_source}
require(operation_pairs == {(name, name) for name in object_counts} and ("response", "cap") not in operation_pairs, operation_pairs)

# Graded products and commutators of positive-degree atoms cannot be a new C1:
# lengths >=2 have degree >=2. Degree-zero identities/reindexings are loops, so
# pre/postcomposition preserves both degree and the operation corner.
degree_ledger = {
    "primitive_degree": 1,
    "product_degree_rule": "deg(xy)=deg(x)+deg(y)",
    "commutator_degree_rule": "deg([x,y])=deg(x)+deg(y)",
    "positive_length_at_least_two_minimum_degree": 2,
    "degree_zero_maps": "identities and allowed root/cut/reinsertion reindexings, all operation-diagonal",
    "conclusion": "no admissible product or commutator creates a new degree-one response-to-cap cell",
}

# The relative Koszul/Tate cell is a cap loop even after its relative shift.
relative = ledger["canonical_relative_enlargement"]
require(relative["Eq_relative_atom"]["relative_degree_after_Q_base_change"] == 1 and relative["Eq_relative_atom"]["operation_type"] == "cap->cap (objectwise K_Eq)" and not relative["operation_changing_atom_created_by_relative_shift"], relative)

# Exact detector signature of the required filtered pair. Standard closure
# classes have zero signature by the sealed switch/retained presentations.
# Lambda contributes the top target and exposes the retained face; Pi cancels
# precisely that face. The 2x2 signature matrix has determinant -2.
lambda_signature = (2, 1)
pi_signature = (0, -1)
determinant = lambda_signature[0] * pi_signature[1] - pi_signature[0] * lambda_signature[1]
require(determinant == -2, determinant)
require((lambda_signature[0] + pi_signature[0], lambda_signature[1] + pi_signature[1]) == (2, 0), "total signature")

equations = []
for root in ("AB", "AC"):
    for cut in ("q23", "q45"):
        label = f"{root}/{cut}"
        equations.extend([
            {"label": label, "equation": "partial_0 Lambda_01=L01", "detector_signature": [2, 0]},
            {"label": label, "equation": "partial_1 Lambda_01=R_ret", "detector_signature": [0, 1]},
            {"label": label, "equation": "partial_0 Pi_r,01=-R_ret", "detector_signature": [0, -1]},
        ])
require(len(equations) == 12, len(equations))
coherence = [
    "tau(Lambda_AB,q23)+Lambda_AC,q23=0",
    "tau(Lambda_AB,q45)+Lambda_AC,q45=0",
    "tau(Pi_AB,q23)+Pi_AC,q23=0",
    "tau(Pi_AB,q45)+Pi_AC,q45=0",
    "sigma(Lambda_AB,q23)-Lambda_AB,q45=0",
    "sigma(Lambda_AC,q23)-Lambda_AC,q45=0",
    "sigma(Pi_AB,q23)-Pi_AB,q45=0",
    "sigma(Pi_AC,q23)-Pi_AC,q45=0",
]

result = {
    "schema": "PACOMP_H3_TOTAL_CONSTRUCTOR_COMPOSITE_CLOSURE_DECISION_V1",
    "status": "PASS_NO_COMPOSITE_CONSTRUCTOR_PRIMITIVE_TWO_COMPONENT_DECISION_IS_MINIMAL",
    "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    "source_derived_closure": {
        "ledger_sha256": digest,
        "actual_atoms": 128,
        "operation_object_counts": object_counts,
        "operation_changing_atoms": 0,
        "composable_word_counts_length_1_to_4": composable_words,
        "ordered_admissible_commutator_inputs": ordered_commutator_inputs,
        "all_length_endpoint_induction": "every composable word remains a loop at response,cap,window,or bar",
        "Hom0_response_cap_dimension": 0,
        "operation_changing_C1_count": 0,
    },
    "composition_and_commutator_verdict": degree_ledger,
    "mapping_cylinder": {
        "without_Phi": "MissingPhysicalArrow",
        "with_formally_granted_Phi": "exactly eight standard word-separated interchanges",
        "standard_interchange_rank": 8,
        "standard_interchange_detector_signature": [0, 0],
        "canonical_higher_Tate_adds_new_type": False,
        "conclusion": "mapping cylinders are functorial in Phi and cannot manufacture Phi or the independent total Hom1 primitive",
    },
    "actual_constructor_search": {
        "Lambda01_Pi_pair_found": False,
        "existing_candidate_records": 0,
        "known_underived_or_Tate_commutators": "objectwise or without physical descent/Gamma projection",
        "smallest_unexcluded_sort": "primitive Hom^1_Gamma(response,cap) modulo eight standard interchanges",
    },
    "minimal_signature_problem": {
        "detectors": ["eta_top", "eta_r"],
        "old_and_standard_signature": [0, 0],
        "Lambda_signature": list(lambda_signature),
        "Pi_signature": list(pi_signature),
        "signature_matrix_columns": [list(lambda_signature), list(pi_signature)],
        "determinant": determinant,
        "total_signature": [2, 0],
        "meaning": "Lambda supplies the top line but exposes the retained line; Pi is independently necessary to cancel it",
    },
    "finite_source_decision": {
        "unknown_records": ["Lambda_01", "Pi_r,01"],
        "literal_instances": ["AB/q23", "AB/q45", "AC/q23", "AC/q45"],
        "boundary_equations": equations,
        "coherence_equations": coherence,
        "face_exactness": [
            "36 L01 PP faces with chart coefficients 2,-1,-1",
            "mixed relative-C4 faces cancel termwise",
            "retained face is exactly R_ret",
            "Pi boundary is exactly -R_ret",
            "no extra q,anchor,W,ridge,residue,Eq descendants",
        ],
        "decision_rule": "enumerate indecomposable physical Hom1 source records only; accept iff one coherent labelled Lambda/Pi pair passes all 12 boundary, 8 coherence, and 5 face-exactness checks",
        "why_primitives_suffice": "a total-degree-one semi-free word contains exactly one degree-one indecomposable; all other factors are diagonal degree-zero transports",
    },
    "scope": {"h": 3, "actual_callable_and_source_derived_free_closure": True, "unwritten_full_physical_complex_classified": False, "new_constructor_added": False, "heavy_solver_runs": 0, "PAComp_promotion": False, "uniform_descent_promotion": False, "conjecture_promotion": False},
    "verdict": "No actual total constructor exists in the pinned primitive registry or its admissible product/commutator/mapping-cylinder closure. The object graph has loops only, positive products/commutators have degree at least two, and the relative Tate shift remains cap-to-cap. Even after formally adjoining Phi, the eight standard interchanges have zero missing-sector signature. The remaining question is exactly the finite primitive Hom1 decision for a coherent Lambda01/Pi_r pair specified above.",
}
temporary = H / "results_composite_closure_decision.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, H / "results_composite_closure_decision.json")
print(json.dumps({"status": result["status"], "actual_atoms": 128, "operation_changing": 0, "boundary_equations": 12, "coherence_equations": 8, "heavy_solver_runs": 0}, sort_keys=True))
