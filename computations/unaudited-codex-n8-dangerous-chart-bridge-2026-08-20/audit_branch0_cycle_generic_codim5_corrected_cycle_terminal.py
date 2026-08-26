#!/usr/bin/env python3
"""Freeze the corrected generic-cycle containment lane and its blockers."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_branch0_cycle_generic_codim5_corrected_cycle_terminal.json"


def load(name):
    return json.loads((HERE / name).read_text())


def file_sha(name):
    return sha256((HERE / name).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def timeout_record(manifest_name):
    manifest = load(manifest_name)
    require(len(manifest["stages"]) == 1
            and manifest["stages"][0]["status"] == "timeout"
            and manifest["stages"][0]["output"]["bytes"] == 0,
            f"{manifest_name} ceased to be a zero-output timeout")
    stage = manifest["stages"][0]
    return {"manifest": manifest_name,
            "manifest_sha256": file_sha(manifest_name),
            "elapsed_seconds": stage["elapsed_seconds"],
            "returncode": stage["returncode"],
            "output_bytes": 0}


def main():
    corrected = load("results_branch0_cycle_generic_qrs_codim3_export.json")
    structural = load("results_branch0_cycle_generic_codim5_d10_structural_split.json")
    k4 = load("results_branch0_cycle_generic_codim5_k4_leaf_exact_audit.json")
    prs = load("results_branch0_cycle_generic_codim5_b1_subresultant_chain.json")
    gcd_terminal = load("results_branch0_cycle_generic_codim5_b1_joint_gcd_terminal.json")
    slice2_export = load("results_branch0_cycle_generic_codim5_fourrow_slice2_c8open_export.json")
    slice2_run = load("results_branch0_cycle_generic_codim5_fourrow_slice2_c8open_p1073741827.manifest.json")
    h1_export = load("results_branch0_cycle_generic_codim5_fourrow_h1_sub_c8open_export.json")

    require(corrected["literal_delta_identity"]
            == "b0*A*Delta|pivot = b0*A*b1*d3-B*d1*d4"
            and corrected["true_delta_numerator_profile"]
            == [[8, 4, 1], [10, 5, 1]],
            "corrected Delta identity changed")
    require(structural["true_delta_identity"] == "TrueDeltaN=C8*D10"
            and structural["resultant_identity"]
            == "Res_b1(D10,P324)=unit*d1*K4*A*W64",
            "D10 structural split changed")
    require(k4["K5_status"] == "exact msolve positive-dimensional sentinel"
            and k4["N14_off_K5_status"] == "exact-Q UNIT",
            "K4 boundary control changed")
    require(prs["J_K_gcd"] == {
                "degree": 6,
                "sha256": "f39c68d63d2b4115a85e01618d701a14ad3ca769c685b62795f5a06ef31cd242",
                "terms": 19}
            and gcd_terminal["exact_gcd_before_live_normalization"] == "d4"
            and gcd_terminal["normalized_accumulator"] == "1",
            "PRS/gcd compression changed")
    require(slice2_run["status"] == "completed_modular_discovery"
            and slice2_run["stages"][0]["basis"]["unit"] is True
            and slice2_run["stages"][0]["elapsed_seconds"] < 1,
            "two-slice overslice control changed")
    require(h1_export["pivot_coefficient"] == 1
            and h1_export["hyperplane_must_fire"] is True
            and h1_export["hostile_constant_mutation_fired"] is True,
            "monic h1 substitution audit changed")

    one_slice_timeout = timeout_record(
        "results_branch0_cycle_generic_codim5_fourrow_slice1_c8open_p1073741827.manifest.json")
    h1_sub_timeout = timeout_record(
        "results_branch0_cycle_generic_codim5_fourrow_h1_sub_c8open_p1073741827.manifest.json")
    result = {
        "status": "UNAUDITED corrected generic-cycle terminal ledger",
        "exact_delta_correction": {
            "identity": corrected["literal_delta_identity"],
            "factorization": "TrueDeltaN=C8*D10",
            "C8_terms_degree": structural["C8_terms_degree"],
            "D10_terms_degree": structural["D10_terms_degree"],
            "export_result_sha256": corrected["result_sha256"],
        },
        "D10_boundary_control": {
            "P324_resultant": structural["resultant_identity"],
            "K4_result": k4["structural_theorem"],
            "K5_status": k4["K5_status"],
            "N14_status": k4["N14_off_K5_status"],
            "audit_result_sha256": k4["result_sha256"],
            "scope": "Boundary control only; D10=0 is excluded by actual Delta-open target.",
        },
        "unsaturated_PRS_compression": {
            "E1_profile": prs["E1"],
            "E0_profile": prs["E0"],
            "J_profile": prs["J"],
            "K_profile": prs["two_linear_root_determinant"]["K"],
            "gcd_J_K": "A exactly (19 terms, degree 6), audited live",
            "gcd_K_over_A_N1846": "d4 exactly, audited live",
            "normalized_accumulator": "1",
            "PRS_result_sha256": prs["result_sha256"],
            "gcd_terminal_result_sha256": gcd_terminal["result_sha256"],
            "nonclaim": gcd_terminal["nonclaim"],
        },
        "sliced_flatness_discovery": {
            "two_slice_export_result_sha256": slice2_export["result_sha256"],
            "two_slice_unit_runner_logical_sha256": slice2_run["logical_sha256"],
            "two_slice_unit_elapsed_seconds": slice2_run["stages"][0]["elapsed_seconds"],
            "one_slice_five_variable": one_slice_timeout,
            "monic_h1_substitution_result_sha256": h1_export["result_sha256"],
            "one_slice_four_variable": h1_sub_timeout,
            "finite_profile": None,
            "second_prime_launched": False,
        },
        "terminal_blocker": (
            "Neither source-faithful one-slice representation produced a "
            "basis or finite degree within 180 seconds. The two-slice UNIT is "
            "an overslice control only. Radical containment of D10 in the "
            "C8-open necessary core is not proved."),
        "smallest_next_exact_target": (
            "Inside the exact monic h1 quotient, pull the P324/P851 PRS "
            "relation E1*b1+E0 through the substitution. On E1!=0 eliminate "
            "b1 to a three-variable quotient and retain the exact base*C8 "
            "localizer times E1; separately audit the nonlive companion "
            "E1=E0=0 with the original four rows. A finite degree must land "
            "at p1 before any p2 or characteristic-zero promotion."),
        "scope": (
            "Exact identities over Q except the explicitly labelled p1 "
            "F4SAT discoveries. No modular UNIT, gcd-one statement, timeout, "
            "or boundary component is promoted to D10 radical containment."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("corrected generic-cycle terminal ledger: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
