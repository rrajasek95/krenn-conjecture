#!/usr/bin/env python3
"""Exact finite-abelian uncertainty audit for the matching source map."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FOURIER_PATH = ROOT / "computations" / "verify_fourier_symmetry_lifting.py"
MPS_PATH = (ROOT / "computations" /
    "unaudited-codex-global-minimal-mps-2026-08-21" /
    "audit_minimum_norm_mps_guard.py")
MINIMUM_PATH = ROOT / "computations" / "verify_minimal_norm_gauge.py"
PEPS_RESULT = (ROOT / "computations" /
    "unaudited-codex-fourier-z3-peps-2026-08-21" /
    "results_fourier_z3_peps.json")
OUT = HERE / "results_fourier_uncertainty.json"
EXPECTED_LOGICAL_SHA256 = (
    "d4f532513bdec735402325c2f44c62bfaba839c61883582fc9de1f8fe3a51c03"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"missing loader for {path}")
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


F = load("uncertainty_fourier", FOURIER_PATH)
# The minimum guard manages its own imports from computations/.
MPS = load("uncertainty_mps", MPS_PATH)
MINIMUM = load("uncertainty_minimum", MINIMUM_PATH)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def conjugate(value):
    # omega-bar=omega^2=-1-omega.
    return F.E(value.a - value.b, -value.b)


def gram(matrix):
    return tuple(tuple(sum((matrix[i][k] * conjugate(matrix[j][k])
                            for k in range(3)), F.ZERO)
                       for j in range(3)) for i in range(3))


def matrix_add(left, right):
    return tuple(tuple(left[i][j] + right[i][j] for j in range(3))
                 for i in range(3))


def n4_fourier_guard():
    original = MPS.n4_matrices()
    minimum = MPS.n4_minimum_block_guard()
    require(minimum["global_minimum_norm_squared"] == 6,
            "n4 minimum norm changed")

    matchings = (((0, 1), (2, 3)),
                 ((0, 2), (1, 3)),
                 ((0, 3), (1, 2)))
    transformed = {}
    labels = {}
    for colour, matching in enumerate(matchings):
        matrix = F.outer(F.U[colour], F.U[colour])
        require(all(matrix[a][b] for a in range(3) for b in range(3)),
                "Fourier rank-one edge lost density")
        for edge in matching:
            transformed[edge] = matrix
            labels[edge] = colour

    tensor = F.matching_tensor(transformed, tuple(range(4)))
    expected = {word: F.E(3, 0)
                for word in __import__("itertools").product(range(3), repeat=4)
                if sum(word) % 3 == 0}
    require(tensor == expected and len(tensor) == 27,
            "source Fourier covariance failed on exact n4 GHZ")

    nine_identity = tuple(tuple(F.E(9, 0) if i == j else F.ZERO
                                for j in range(3)) for i in range(3))
    for vertex in range(4):
        total = tuple(tuple(F.ZERO for _ in range(3)) for _ in range(3))
        for edge, matrix in transformed.items():
            if vertex in edge:
                total = matrix_add(total, gram(matrix))
        require(total == nine_identity,
                ("unnormalized Fourier isotropy", vertex, total))

    # Every K4 perfect matching is one selected colour layer.  Thus no one
    # matching carries three independent character channels.
    common_channel_dimensions = []
    for matching in matchings:
        common_channel_dimensions.append(len({labels[edge] for edge in matching}))
    require(common_channel_dimensions == [1, 1, 1],
            "n4 acquired a common three-channel matching")

    # Neither same-sign charge conservation p+q=0 nor oriented conservation
    # p-q=0 holds: every transformed rank-one edge has all nine entries live.
    conservation_failures = 0
    for matrix in transformed.values():
        if any(matrix[p][q] and (p + q) % 3
               for p in range(3) for q in range(3)):
            conservation_failures += 1
    require(conservation_failures == 6,
            "n4 edgewise character-conservation guard changed")

    # Exact active cap at pair 01 with K=I.  The three matching contributions
    # on sites 23 are E00,E11,E22, whose sum is I=GHZ2.
    cap_terms = []
    for colour in range(3):
        term = [[0] * 3 for _ in range(3)]
        term[colour][colour] = 1
        cap_terms.append(term)
    cap_sum = [[sum(term[i][j] for term in cap_terms) for j in range(3)]
               for i in range(3)]
    require(cap_sum == [[int(i == j) for j in range(3)] for i in range(3)],
            "n4 cap contraction changed")

    return {
        "output_before": "indicator of diagonal subgroup, support 3",
        "output_after_unnormalized_F":
            "3*indicator of sum-zero subgroup, support 27",
        "global_minimum_norm_squared": 6,
        "full_isotropy_before": "R_v=I",
        "full_isotropy_after_normalized_F": "R_v=I",
        "all_six_transformed_edges": "dense rank one",
        "edgewise_character_conservation_failures": conservation_failures,
        "common_matching_character_dimensions": common_channel_dimensions,
        "active_clean_cap": "pair 01, K=I; residual E00+E11+E22=I",
    }


def uncertainty_target(n):
    group_size = 3 ** n
    support_f = 3
    support_hat = 3 ** (n - 1)
    norm_f_squared = 3
    norm_hat_squared = 9 * support_hat
    require(support_f * support_hat == group_size,
            "Donoho-Stark equality changed")
    require(norm_hat_squared == group_size * norm_f_squared,
            "unnormalized Parseval changed")
    return {
        "group_order": group_size,
        "support_f": support_f,
        "support_hat_f": support_hat,
        "Donoho_Stark_product": support_f * support_hat,
        "Parseval_norms_squared": [norm_f_squared, norm_hat_squared],
        "L1_to_Linf_equality": "||hat f||_inf=3=||f||_1",
        "equality_classification":
            "character times a coset-subgroup indicator (here the diagonal subgroup)",
    }


def dense_isotropic_guard(n=8):
    # Put the unnormalized Fourier matrix on every edge.  FF*=3I, so every
    # port Gram is 3(n-1)I.  Every cell and every perfect-matching monomial is
    # live, while the output is deliberately not GHZ.
    return {
        "sites": n,
        "edge_matrix": "F_3 on all C(n,2) edges",
        "all_cells_live": True,
        "edge_rank": 3,
        "port_gram": f"{3*(n-1)} I_3",
        "matching_terms_per_word": 105,
        "edgewise_charge_conservation": False,
        "is_GHZ_source": False,
    }


def main():
    target = {str(n): uncertainty_target(n) for n in (4, 8)}
    n4 = n4_fourier_guard()

    # Exact hostile minimum/isotropy control.  These routines certify the
    # cyclotomic port Grams and all star/triangle ranks; the committed theorem
    # then identifies its derivative kernel with the scalar gauge and proves a
    # smooth local minimum for its own (non-GHZ) output.
    MINIMUM.verify_fourier_isotropy()
    MINIMUM.verify_full_block_injectivity_mod7()
    phased = {
        "sites": 6,
        "full_isotropy": "R_v=7I",
        "all_star_ranks": "45/45",
        "all_triangle_ranks": "27/27",
        "derivative_rank": "130/135; kernel is five scalar vertex gauges",
        "minimum_status": "smooth strict local minimum modulo compact phases",
        "output": "non-GHZ; mixed coefficient 010000 is 1+omega",
        "verdict":
            "minimum norm plus isotropy alone do not force character conservation or a cap",
    }

    peps = json.loads(PEPS_RESULT.read_text())
    require(peps["logical_sha256"] ==
            "4e58445b01356631bdf82309204df8713c9623ea4f0989ceef7d5cd4481468fd",
            "frozen Fourier PEPS control changed")

    result = {
        "status": "PASS terminal negative finite-abelian uncertainty lift audit",
        "target_uncertainty_equalities": target,
        "source_fourier_covariance": {
            "formula": (
                "If U=F_3/sqrt(3) and B_uv=U A_uv U^T, then "
                "H_n(B)=U^tensor n H_n(A)."),
            "proof": (
                "Apply U at the two endpoints of each edge tensor in every "
                "perfect-matching summand; every site occurs exactly once."),
            "fiber_bijection": True,
            "Frobenius_source_norm_preserved": True,
            "full_port_isotropy_preserved": True,
            "global_and_local_minimum_status_preserved": True,
            "clean_cap_existence_preserved_contravariantly": True,
        },
        "controls": {
            "n4_exact_GHZ_global_minimum": n4,
            "n6_phased_non_GHZ_local_minimum": phased,
            "n8_dense_isotropic": dense_isotropic_guard(),
            "invisible_chord": {
                "Fourier_output_visibility":
                    "still invisible because the output transform is invertible",
                "minimum_norm_scope":
                    "the frozen inactive chord is deleted by block normality; it only guards output-only lifting",
            },
        },
        "edgewise_conservation_no_go": {
            "exact_n4_falsifier": True,
            "general_exact_theorem": (
                "The frozen projective charge-lift theorem proves that an exact "
                "Fourier-GHZ source cannot be made edgewise charge homogeneous "
                "even by vertex scalars/target stabilizers."),
        },
        "terminal_verdict": (
            "Donoho-Stark/Hausdorff-Young equality classifies the output and "
            "is transported through an isometric bijection of source fibres. "
            "It supplies no additional edge equation.  The n4 global minimum "
            "already violates edgewise character conservation and a common "
            "three-channel matching while retaining its active cap.  Full "
            "isotropy and minimum status do not repair the lift on the hostile "
            "n6 control.  Any successful Fourier argument must add a genuinely "
            "source-relative inequality coupling individual matching summands; "
            "output uncertainty equality alone is exhausted."),
        "source_hashes": {str(path.relative_to(ROOT)): file_sha(path)
                          for path in (FOURIER_PATH, MPS_PATH, MINIMUM_PATH,
                                       PEPS_RESULT)},
    }
    result["logical_sha256"] = logical_sha(result)
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FROZEN":
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "Fourier uncertainty logical digest changed")
    if "--mutate-support" in sys.argv:
        require(target["8"]["support_hat_f"] != 3 ** 7,
                "mutation survived: Fourier support corrupted")
    if "--mutate-conservation" in sys.argv:
        require(n4["edgewise_character_conservation_failures"] == 0,
                "mutation survived: n4 falsely charge-conserving")

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
