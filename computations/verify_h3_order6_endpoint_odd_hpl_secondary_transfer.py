#!/usr/bin/env python3
"""Compose the exact order-six first-flat lift with augmented HPL.

This audit records a theorem about the *bounded physical operator module*:
the 343-term order-six vector lies in the kernel of the literal source and
singleton-prolongation maps, while its pair projection is the prescribed
``-delta`` class.  Hence that pair projection is a genuine secondary
transfer (the ``D_2`` page), not a face of a chosen sparse representative.

The endpoint-odd Cartan theorem kills the protected augmentations and the
word-degree audit places the two fine pieces in one total module degree.
What remains is the comparison from this filtered operator module to the
complete repeated-grade physical correction complex; this checker does not
silently identify those two complexes.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py":
        "ef9bd416986f7dc8c07ffa3b396d1c1f92237c8e1a0539ecbb0ddbeaadb1c18e",
    "computations/verify_augmented_hpl_terminal_bockstein_lemma.py":
        "a616e5d83d52189c1d64093d0ba80abc0dc43e4b419241a871713a622b043a49",
    "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py":
        "24ec9e3c1d1f9b689fa5a47faf9900c16724dc215fee0a41a0b653f410427fb3",
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
}
EXPECTED_LEDGER_SHA256 = "85887afc1e4d409d533005f4cd2de667301fc40fa0c88af31077829fa744311a"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    affine = load(
        "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py",
        "order6_hpl_affine",
    )
    affine_result = affine.audit()
    require(affine_result["eligible_order6_columns"] == 8_580,
            "order-six physical operator inventory changed")
    require(affine_result["exact_solution_terms"] == 343,
            "first-flat solution size changed")
    require(affine_result["first_spencer_face_support"] == 0,
            "first transferred face stopped vanishing")
    require(affine_result["nonzero_fine_shift_shadow_count"] == 2,
            "the secondary shadow stopped having two word components")
    require(affine_result["second_spencer_face_support"] > 0,
            "the secondary transfer unexpectedly vanished")

    hpl = load(
        "computations/verify_augmented_hpl_terminal_bockstein_lemma.py",
        "order6_hpl_abstract",
    )
    hpl_ledger, hpl_digest = hpl.audit()
    require(hpl_digest == hpl.EXPECTED_DIGEST,
            "augmented HPL ledger changed")
    require(hpl_ledger["second_transfer"] == {"D": 1},
            "abstract secondary-transfer normalization changed")

    endpoint = load(
        "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py",
        "order6_hpl_endpoint",
    )
    endpoint_ledger, endpoint_digest = endpoint.audit()
    require(endpoint_digest == endpoint.EXPECTED_LEDGER_SHA256,
            "endpoint-odd Cartan ledger changed")
    require(endpoint_ledger["mixed_boundary_alpha"] == [-1, 1, 1, -1],
            "endpoint-odd secondary target changed")

    ridge = load(
        "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py",
        "order6_hpl_ridge",
    )
    ridge_result = ridge.audit()
    require(ridge_result["complete_hasse_tower_can_tensor_with_ridge_jet"],
            "the terminal ridge stopped commuting with the source tower")

    ledger = {
        "theorem": "order-six minus-delta is an endpoint-odd HPL secondary transfer",
        "bounded_physical_operator_module": {
            "columns": affine_result["eligible_order6_columns"],
            "exact_rank": affine_result["exact_row_rank"],
            "solution_terms": affine_result["exact_solution_terms"],
            "solution_sha256": affine_result["exact_solution_sha256"],
            "literal_source_output": 0,
            "first_transfer_support": affine_result[
                "first_spencer_face_support"
            ],
            "secondary_transfer_support": affine_result[
                "second_spencer_face_support"
            ],
            "fine_word_components": affine_result[
                "nonzero_fine_shift_shadow_count"
            ],
        },
        "hpl_identification": {
            "D1": "literal singleton coefficient-prolongation map",
            "D2": "pair shadow induced on ker(source,D1)",
            "D2_value": "-delta=(-1,+1,+1,-1)",
            "canonical_on_D1_homology": True,
        },
        "word_grade": (
            "the two fine shifts have one common total source-module degree "
            "after the pure/mixed word degrees are included"
        ),
        "endpoint_odd_protection": endpoint_ledger[
            "endpoint_even_augmentations_killed"
        ],
        "ridge_commutation": ridge_result["formal_interchange_identity"],
        "proved_consequence": (
            "minus-delta is a source-provenant secondary operation in the "
            "complete bounded order-six physical operator block; it is not "
            "a defect peculiar to a sparse representative"
        ),
        "remaining_comparison": (
            "construct/identify the filtered chain map from this operator "
            "module to the complete labelled repeated P3+K2 correction "
            "complex, carrying D2 to ordinary residue and the commuting "
            "ridge to eta/sigma"
        ),
        "scope": (
            "exact secondary-transfer identification; no assertion that the "
            "bounded operator module is already the full physical correction "
            "complex, and no transverse-rank landing"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("order-six HPL ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 order-six endpoint-odd HPL secondary transfer: PASS")
    print("source/D1: 0/0; D2: -delta")
    print("protected augmentations: zero by endpoint oddness")
    print("operator-to-physical-correction comparison: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
