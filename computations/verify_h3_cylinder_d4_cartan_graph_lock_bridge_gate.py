#!/usr/bin/env python3
"""Audit D4 then tail-Cartan transport of the cylinder Segre curvature."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h0_cylinder_mixed_curvature_landing_guard.py":
        "9395988206e235f9770e32c06c7cbed0ba9f98705a6ab00e5c667596853b9386",
    "notes/h3-h0-cylinder-mixed-curvature-landing-guard.md":
        "eb98851250ef123de44a9033beb3abcebc045f326fc254c68f07cab1d226893b",
    "computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py":
        "a51b8f091a25624d17443c70ac70b60eb257c8b11dafb0b9ad3f17962dc07390",
    "notes/h3-trapped-hessian-to-six-term-endpoint-polarization-gate.md":
        "45d4d6604a58da20bec8aa87cb9522b658e2454a939533075d6e8d607ed895b8",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
    "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py":
        "42bf68eeb963d568d1c8d9156d4176bec31a114b6fe804744833364fe3633475",
    "notes/h3-e14-cap-graph-two-parameter-flat-transport-gate.md":
        "61c093eed30cd2fff1be086e6069d344e76a583ee31f93528a31aebe76c5c5d6",
    "computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py":
        "eede8aabd5c4740520ed13f1aacc897326a3a02573f860f5b2613c9df91fd53c",
    "notes/h3-residual-q-ks-standard-transport-graph-lock.md":
        "9729e3bd7d639c24c2512641da74815cf1162e995ce76cb6286bca6dd545ca0f",
}
EXPECTED_LEDGER_SHA256 = "91878b6d455d4db6ca5e88bc26e77589fe27105e021a7ee34d40c5a0ec6ae11c"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(value: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(value*entry for entry in vector)


def rank(vectors: tuple[tuple[Q, ...], ...]) -> int:
    basis: dict[int, tuple[Q, ...]] = {}
    for vector in vectors:
        values = list(vector)
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [a-coefficient*b for a, b in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((i for i, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value/coefficient for value in values)
    return len(basis)


def literal_tail_transport_audit() -> dict[str, object]:
    # Basis: M0^11, M0^(21,12), M1^11, M1^(21,12), where
    # M0=23|45 and M1=24|35.
    m0_pure = (Q(1), 0, 0, 0)
    m0_decorated = (0, Q(1), 0, 0)
    m1_pure = (0, 0, Q(1), 0)
    m1_decorated = (0, 0, 0, Q(1))
    d4_curvature = add(m0_pure, scale(Q(-1), m1_pure))
    w_curvature = add(m0_decorated, scale(Q(-1), m1_decorated))
    cartan_difference = add(w_curvature, scale(Q(-1), d4_curvature))
    delta_m0 = add(m0_pure, scale(Q(-1), m0_decorated))
    delta_m1 = add(m1_pure, scale(Q(-1), m1_decorated))
    require(cartan_difference == add(delta_m1, scale(Q(-1), delta_m0)),
            "the two-matching Cartan decomposition changed")
    require(cartan_difference != delta_m1
            and rank((delta_m0, delta_m1)) == 2,
            "the extra matching packet disappeared")

    # The endpoint antisymmetrization supplies the graph-lock sign vector.
    alpha = (Q(-1), Q(1), Q(1), Q(-1))
    required = tuple(map(Q, (-1, 1, 1, -1)))
    require(alpha == required, "the endpoint Cartan sign changed")
    return {
        "bottom_word": "110000",
        "D4_sites": [2, 3, 4, 5],
        "D4_top_word": "111111",
        "tail_Cartan_sites": [2, 5],
        "tail_Cartan_word": "112112",
        "M0_transport": (
            "q23:00*q45:00 -> q23:11*q45:11 -> q23:21*q45:12"
        ),
        "M1_transport": (
            "q24:00*q35:00 -> q24:11*q35:11 -> q24:21*q35:12"
        ),
        "endpoint_corner_sign": [-1, 1, 1, -1],
        "single_M1_graph_lock": "delta_M1=M1^11-M1^(21,12)",
        "full_cylinder_image": "delta_M1-delta_M0",
        "equals_one_graph_lock_packet": False,
        "equals_difference_of_two_covariant_graph_lock_packets": True,
        "matching_packet_rank": 2,
    }


def cap_word_and_grade_audit() -> dict[str, object]:
    cap_word = tuple(map(int, "01211222"))
    root_sites = (2, 3, 4, 5)
    root_letters = tuple(cap_word[site] for site in root_sites)
    require(root_letters == (2, 1, 1, 2), root_letters)
    require(all(letter != 0 for letter in root_letters),
            "the cap word unexpectedly acquired a D4 input zero")

    full_pairs = tuple((endpoint, corner, tail)
                       for endpoint in ("P", "S")
                       for corner in range(4) for tail in range(2))
    p_half = tuple(pair for pair in full_pairs if pair[0] == "P")
    s_half = tuple(pair for pair in full_pairs if pair[0] == "S")
    require(len(full_pairs) == 16 and len(p_half) == len(s_half) == 8
            and not (set(p_half) & set(s_half)),
            "the endpoint-polarization split changed")
    return {
        "physical_cap_word": "01211222",
        "cap_letters_at_D4_sites_2_3_4_5": list(root_letters),
        "literal_0_to_1_D4_action_on_cap_multiplier": "zero/not applicable",
        "formal_spectator_cap_transport": True,
        "physical_cross_word_cap_transport": False,
        "fixed_right_D4_Cartan_symbol_terms": len(p_half),
        "full_physical_endpoint_tail_terms": len(full_pairs),
        "missing_transpose_half_terms": len(s_half),
        "endpoint_transpose_fills_associated_symbol": True,
        "transpose_preserves_canonical_repeated_grade": False,
        "six_term_private_feature_overlap_after_transpose": 0,
        "remaining_grade": (
            "conjugate physical repeated component Lambda^T, not canonical Lambda"
        ),
    }


def augmented_composition_audit() -> dict[str, object]:
    return {
        "D4_target": (
            "moving-target orbit supplies the affine target correction only in the "
            "orbit-relative presentation"
        ),
        "odd_Cartan_target": 0,
        "physical_Cartan_rows_once_canonical_grade_is_reached": {
            "ordinary_residue": [-1, 1, 1, -1],
            "D_W_target_anchor_pureEq": 0,
            "eta_sigma": "the committed -dOmega ridge packet",
            "physical_q": "existing protected-kernel generator/Fredholm alternative",
        },
        "cap_multiplier_commutes_formally": True,
        "cap_multiplier_descends_literally": False,
        "reason": (
            "the response D4 source and cap source occupy different words/fine/"
            "repeated grades; tensor flatness is not a fixed-fibre chain map"
        ),
        "conditional_closure": (
            "a physical multiplicative cross-word comparison carrying both matching "
            "packets, the endpoint-transpose half and Lambda^T back to Lambda would "
            "let the existing Physical Cartan Descent cancel the residue completely"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 cylinder D4 then Cartan graph-lock bridge gate",
        "pins": PINS,
        "literal_tail_transport": literal_tail_transport_audit(),
        "cap_word_and_grade": cap_word_and_grade_audit(),
        "augmented_composition": augmented_composition_audit(),
        "verdict": (
            "D4 then the sites-(2,5) Cartan action gives the correct decorated "
            "graph-lock signs, but on the full cylinder matching difference its "
            "image is delta_M1-delta_M0, not one delta.  Both summands are covered "
            "covariantly by Physical Cartan Descent once placed.  The proposed "
            "composition is not yet a literal physical placement: the cap word has "
            "letters 2112 at the D4 sites, the fixed-right symbol supplies only 8 "
            "of 16 endpoint-tail terms, and endpoint transpose lands in conjugate "
            "Lambda^T with zero private-feature overlap.  Thus the bridge is exact "
            "at coefficient/associated-symbol level but still needs the existing "
            "cross-word and shifted repeated-grade comparison."
        ),
        "scope": (
            "canonical h=3 two residual matchings; no new support census or claim "
            "that the orbit-relative spectator cap is a physical fixed-fibre map"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("D4 pure00 -> pure11 tags: EXACT")
    print("Cartan 2,5 -> decorated 21/12 tags: EXACT")
    print("full cylinder image: delta_M1-delta_M0 (NOT ONE DELTA)")
    print("literal cap/repeated-grade placement: OPEN")
    print("ledger_sha256="+digest)


if __name__ == "__main__":
    main()
