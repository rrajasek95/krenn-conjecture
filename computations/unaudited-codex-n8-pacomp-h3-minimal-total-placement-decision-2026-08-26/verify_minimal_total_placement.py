#!/usr/bin/env python3
"""Exact finite obstruction and minimal interface for the PAComp h=3 filler."""
from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
H = Path(__file__).resolve().parent
PINS = {
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-source-column-detector-census-2026-08-25/FINAL_MANIFEST.sha256": "e44dd3e2c386d42d07ab0d5443351694df0906960f44d1cfce3b85592677577a",
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-source-column-detector-census-2026-08-25/results_source_column_detector_census.json": "40f629bd815441e2e1a4390d148016a2b5b1b409a41b619ceaab43d62a85c122",
    ROOT / "computations/unaudited-codex-n8-pacomp-h3-switch-charge-nonimplication-referee-2026-08-25/FINAL_MANIFEST.sha256": "4ba7073930e2c59c5f760fb0e24309fe08b0086cb105f3d1ce1bae62b56f2800",
    ROOT / "computations/unaudited-codex-n8-pacomp-x23-total-carrier-et-construction-audit-2026-08-25/MANIFEST.sha256": "f4c40ad4801fcf2950af2871e46eb6971e3a5fee12f124a8f37367d6e343117b",
    ROOT / "computations/unaudited-codex-n8-pacomp-x23-et-dependency-circularity-audit-2026-08-25/MANIFEST.sha256": "42573cc253b38b66eee8324e671124657728373fbcb707fbf9df71a360116009",
    ROOT / "computations/unaudited-codex-n8-pacomp-x23-absolute-carrier-boundary-audit-2026-08-25/MANIFEST.sha256": "f443971c89f61ecd255e5e23840936b52f41e3aea10a29ef1c544239223bcdc4",
    ROOT / "computations/unaudited-codex-n8-pacomp-x23-minimal-generator-extension-2026-08-25/MANIFEST.sha256": "a13d2a726e1440e2f6406913adcd2c6674e7d9d3a5677e2c1d56031e9d7a1e24",
    ROOT / "computations/unaudited-codex-n8-pacomp-x23-physical-kappa-construction-attempt-2026-08-25/MANIFEST.sha256": "00899a99e57e9ced9eed7e3346cf54431037f688caab92f29a7e59d72ad95dc9",
    ROOT / "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py": "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    ROOT / "computations/verify_h3_gamma_star_executable_gen_phys_registry.py": "173ebdedcfdadd9891704223ea93731509c18a4d120aa34d6c7bc8a4f3aebddb",
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


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[columns[column][row] for column in range(len(columns))] for row in range(height)]
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


def embed(left, right, side: str):
    return tuple(left) + (Q(0),) * len(right) if side == "left" else (Q(0),) * len(left) + tuple(right)


for path, expected in PINS.items():
    require(path.is_file() and sha(path) == expected, (path, sha(path), expected))

census = json.loads((ROOT / "computations/unaudited-codex-n8-pacomp-h3-source-column-detector-census-2026-08-25/results_source_column_detector_census.json").read_text())
require(census["status"] == "PASS_NO_ADMISSIBLE_EXISTING_PRIMITIVE_HITS_L01_OR_R_RET", census["status"])
require(census["executable_registry"]["primitive_entries"] == 128 and census["executable_registry"]["registered_degree_zero_cross_operation_arrows"] == 0, "registry census")
require(census["detectors"]["eta_normalization"] == {"L01": 2, "histogram_on_100_admissible": {"0": 100}}, "eta census")
require(census["detectors"]["eta_r_normalization"] == {"R_ret": 1, "histogram_on_100_admissible": {"0": 100}}, "eta_r census")
require(census["one_step_reindexing_overclosure"]["images_checked"] == 28800 and census["one_step_reindexing_overclosure"]["eta_histogram"] == {"0": 28800} and census["one_step_reindexing_overclosure"]["eta_r_histogram"] == {"0": 28800}, "reindexing closure")

# Stronger-than-existing top presentation: all four formal K2,2 switches.
top_columns = (
    (1, 0, 1, 0),
    (1, 0, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 0, 1),
)
eta_top = (1, 1, -1, -1)
L01 = (2, 0, 0, 0)
require(rank(top_columns) == 3 and all(dot(eta_top, column) == 0 for column in top_columns), "top presentation")
require(dot(eta_top, L01) == 2 and rank(top_columns + (L01,)) == 4, "top target")

# Stronger-than-existing face-complete retained presentation.
retained_columns = (
    (1, 1, 1, 0, 0),
    (1, 0, 0, 1, 1),
    (1, 1, 0, 1, 0),
    (1, 0, 1, 0, 1),
)
eta_retained = (Q(1), Q(-1, 2), Q(-1, 2), Q(-1, 2), Q(-1, 2))
R_ret = (1, 0, 0, 0, 0)
require(rank(retained_columns) == 3 and all(dot(eta_retained, column) == 0 for column in retained_columns), "retained presentation")
require(dot(eta_retained, R_ret) == 1 and rank(retained_columns + (R_ret,)) == 4, "retained target")

# The two obligations live in distinct associated-graded targets. One ordinary
# homogeneous source column can raise this block-diagonal rank by at most one.
zero_top = (Q(0),) * len(L01)
zero_ret = (Q(0),) * len(R_ret)
block_columns = tuple(embed(column, zero_ret, "left") for column in top_columns) + tuple(embed(zero_top, column, "right") for column in retained_columns)
L_block = embed(L01, zero_ret, "left")
R_block = embed(zero_top, R_ret, "right")
require(rank(block_columns) == 6 and rank(block_columns + (L_block,)) == 7 and rank(block_columns + (R_block,)) == 7 and rank(block_columns + (L_block, R_block)) == 8, "two-line direct sum")

# Replay the literal fixed-window projection. It proves two switch-row
# families are necessary at the chart shadow but, by the top detector above,
# also proves that this shadow is not itself the absolute filler.
fixed = load(
    ROOT / "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
    "pacomp_min_fixed",
)
columns, detector, candidate_h, candidate_r, packet = fixed.audit_cartesian_physical_packet()
switch = fixed.audit_operation_switch_boundary(columns, candidate_h, candidate_r)
require(packet["internal_rank"] == 46 and packet["cokernel_dimension"] == 2, packet)
require(switch["rank_base_one_switch_candidate"] == [46, 47, 48] and switch["rank_base_two_switches_candidate"] == [46, 48, 48], switch)
require(switch["exact_projection_after_both_switches"] == "L=-4*(A+B+C)+3*(A+B)+3*(A+C)", switch)

# Genuine endpoint-choice near misses: exact top formula and protected faces.
A = (1, 0, 0, 0, 0)
B = (0, 1, 0, 0, 0)
C = (0, 0, 1, 0, 0)
tB = (0, 0, 0, 1, 0)
tC = (0, 0, 0, 0, 1)
gB = tuple(Q(x) for x in (1, -1, 0, 1, 0))
gC = tuple(Q(x) for x in (1, 0, -1, 0, 1))
T = tuple(Q(x) + Q(y) for x, y in zip(tB, tC, strict=True))
L_chart = tuple(Q(2) * Q(a) - Q(b) - Q(c) for a, b, c in zip(A, B, C, strict=True))
require(tuple(x + y for x, y in zip(gB, gC, strict=True)) == tuple(x + y for x, y in zip(T, L_chart, strict=True)), "Gamma formula")
require(gB[3:] == (1, 0) and gC[3:] == (0, 1), "forbidden endpoint faces")

retained_formula = "-2*((dD)*q01+D*(dq01))*r_DQ+((dp0)*s1+p0*(ds1))*r_PS01+((dp1)*s0+p1*(ds0))*r_PS10"
pi_formula = "2*((dD)*q01+D*(dq01))*r_DQ-((dp0)*s1+p0*(ds1))*r_PS01-((dp1)*s0+p1*(ds0))*r_PS10"

result = {
    "schema": "PACOMP_H3_MINIMAL_TOTAL_PLACEMENT_DECISION_V1",
    "status": "PASS_NO_EXISTING_OR_ONE_BARE_SWITCH_CONSTRUCTION_MINIMAL_TWO_COMPONENT_INTERFACE",
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    "source_provenance": {
        "implemented_primitives": 128,
        "admissible_fixed_window_primitives": 100,
        "registered_degree_zero_cross_operation_arrows": 0,
        "allowed_reindexing_images_checked": 28800,
        "detector_histograms": {"eta": {"0": 28800}, "eta_r": {"0": 28800}},
        "conclusion": "no expression in the pinned callable constructors and allowed one-step reindexings supplies either quotient column",
    },
    "near_misses": {
        "dGamma_B": "t_B+D*q01*H-p0*s1*H",
        "dGamma_C": "t_C+D*q01*H-p1*s0*H",
        "sum": "d(Gamma_B+Gamma_C)=T+L01",
        "forbidden_faces": ["t_B", "t_C"],
        "why_not_filler": "subtracting T requires exactly the absent absolute carrier E_T and does not resolve the retained-r lift",
    },
    "top_exact_obstruction": {
        "strong_presentation": "all four formal K2,2 switch mates granted",
        "target_dimension": 4,
        "boundary_rank": 3,
        "annihilator": list(eta_top),
        "target": list(L01),
        "detector_value": 2,
        "rank_after_target": 4,
        "conclusion": "a bare switch edge, all four switch edges, and their linear combinations cannot have boundary L01",
    },
    "retained_exact_obstruction": {
        "strong_presentation": "all four face-complete retained rows granted",
        "target_dimension": 5,
        "boundary_rank": 3,
        "annihilator": [str(value) for value in eta_retained],
        "target": list(R_ret),
        "detector_value": 1,
        "rank_after_target": 4,
        "literal_retained_face": retained_formula,
    },
    "projection_warning": {
        "fixed_window_rank_ladder_one_family": [46, 47, 48],
        "fixed_window_rank_ladder_two_families": [46, 48, 48],
        "chart_shadow_identity": "L=-4*(A+B+C)+3*(A+B)+3*(A+C)",
        "logical_role": "both DQ-to-PS switch families are necessary at chart level, but the exact four-corner detector proves their full lifted edges are not sufficient for an absolute L01 filler",
    },
    "minimum_theorem": {
        "associated_graded_old_rank": 6,
        "after_either_missing_line": 7,
        "after_both_missing_lines": 8,
        "bare_homogeneous_new_columns_required": 2,
        "one_bare_cross_operation_sufficient": False,
        "one_total_constructor_schema_possible_only_if": "it emits two nonzero filtration components and all their source labels; calling this one schema does not make it a one-column construction",
    },
    "exact_formal_total_interface": {
        "top_component": "partial_0 Lambda_01=L01=(2*D*q01-p0*s1-p1*s0)*H_2345",
        "first_proper_component": "partial_1 Lambda_01=R_ret=" + retained_formula,
        "correction_component": "partial_0 Pi_r,01=-R_ret=" + pi_formula,
        "totalization": "Lambda_01^tot=Lambda_01+Pi_r,01 has the L01 leading boundary and cancels the first retained-r face",
        "equivalent_absolute_carrier": "E_T=Gamma_B+Gamma_C-Lambda_01^tot; its leading boundary is T=t_B+t_C",
        "symmetry": ["tau-anti-equivariant", "cut-sigma covariant", "AB and AC are two literal root-labelled instances, not an unlabelled sum"],
        "physical_status": "FORMAL_FREE_EXTENSION_ONLY_NOT_EMITTED_BY_PINNED_SOURCE",
    },
    "minimal_finite_decision_problem": {
        "unknown": "one root-natural TotalLambda01 constructor schema",
        "literal_instances": ["AB/q23", "AB/q45", "AC/q23", "AC/q45"],
        "required_checks": [
            "exact top boundary L01 with no t_B/t_C face",
            "all 18 selected tail faces with coefficients 2,-1,-1",
            "all 18 endpoint/direction faces with coefficients 2,-1,-1",
            "termwise cancellation of the two mixed relative-C4 faces",
            "retained face equals R_ret exactly",
            "Pi_r correction boundary equals -R_ret exactly",
            "no extra q/anchor/W/ridge/residue/Eq descendants",
            "AB/AC root naturality and q23/q45 cut covariance",
        ],
        "acceptance": "a source-provenant constructor emitting all four labelled instances and passing the eight literal identities; otherwise the two detector certificates remain valid",
    },
    "scope": {"h": 3, "pinned_executable_source_only": True, "new_physical_constructor_added": False, "solves": 0, "PAComp_promotion": False, "uniform_descent_promotion": False, "conjecture_promotion": False},
    "verdict": "The smallest bare cross-operation is rigorously insufficient. Existing source operations cannot construct either missing quotient column. The exact minimal positive object is one root-natural total-constructor schema with two associated-graded components Lambda_01 and Pi_r,01 (four labelled AB/AC x q23/q45 instances). Its chain formulas are fixed above, reducing existence to eight finite source-provenance checks; no such physical constructor is presently registered.",
}

temporary = H / "results_minimal_total_placement.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, H / "results_minimal_total_placement.json")
print(json.dumps({"status": result["status"], "old_rank": 6, "rank_with_both": 8, "physical_construction": False, "solves": 0}, sort_keys=True))
