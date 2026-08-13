#!/usr/bin/env python3
"""Audit the affine raw occurrence-cut candidate for Gamma_1.

At occurrence order three, normalized residual-edge restriction followed by
reinsertion is

    R = (1/2) sum_e I_e D_e = id.

Tensoring this coefficient operator with the first based-loop moment
integral t d(t(1-t)) = -1/6 therefore gives the desired -1/6 top scalar.
This does not yet give a physical Gamma_1.  Before reinsertion, either marked
residual cut retains a lower centered occurrence class.  After both
normalizations it is -5/8 c_lower and is detected modulo every constant
carrier with value -15/2.  The two marked cut components are separately
labelled, so granting only the primitive/common-H0 cap p does not fill them.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/uniform-centered-occurrence-restriction-insertion-gate.md":
        "c3161b740606a19d1fb238921986a6ab3b9c2f9cec9d7bc9a9410059f8c213da",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "notes/scalar-unit-c1-weighted-endpoint-bockstein-gate.md":
        "c954f7c6d70368b7aee98208f68dc4c53ff6dae93e49cfa3862939707d00f7a3",
    "computations/verify_scalar_unit_c1_weighted_endpoint_bockstein_gate.py":
        "11fda4d929d1b064fe49ff9f45e077a2dd9bffdaec23a85b4be8a55d44561fa8",
    "notes/h3-c1-complete-augmented-carrier-rank-gate.md":
        "0b90bcae41a147dd51a60d64adfb60078272cf8ae8afda6366a0c2a619a966af",
    "computations/verify_h3_c1_complete_augmented_carrier_rank_gate.py":
        "27a15787cc31401a82f2d167130907170d5e073ede9143366845bf2e2e6bc397",
    "notes/h3-direct-free-normals-e14-pointed-composition-gate.md":
        "aa927470ffc926bc5639be94c76ab66c00cdabfa0082a0b94f6d117d7add0942",
    "computations/verify_h3_direct_free_normals_e14_pointed_composition_gate.py":
        "ea8cb46d5ee84b1973cb062df73b75c0704a0a31823b53e7187e737175964d53",
}
EXPECTED_LEDGER_SHA256 = (
    "314568d8bea3e4c120654a7a02c8d94b6e3b6903ecd45331f2507b9c2b78c41e"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load_occurrence_module():
    relative = (
        "computations/"
        "verify_uniform_centered_occurrence_restriction_insertion_gate.py"
    )
    specification = importlib.util.spec_from_file_location(
        "uniform_centered_occurrence_restriction", ROOT / relative
    )
    require(specification is not None and specification.loader is not None,
            "cannot load centered restriction module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def dot(left, right) -> Fraction:
    require(len(left) == len(right), "dot width")
    return sum((Fraction(a) * Fraction(b)
                for a, b in zip(left, right, strict=True)), Fraction(0))


def affine_moment_audit() -> dict[str, object]:
    # eta=t(1-t), so d eta=(1-2t)dt.  Exact polynomial integration gives
    # int d eta=0 and int t d eta=1/2-2/3=-1/6.
    eta_at_zero = Fraction(0)
    eta_at_one = Fraction(0)
    unweighted = Fraction(1) - Fraction(1)
    first_weighted = Fraction(1, 2) - Fraction(2, 3)
    require(eta_at_zero == eta_at_one == 0, "based loop changed endpoints")
    require(unweighted == 0, "based loop changed unweighted carrier")
    require(first_weighted == Fraction(-1, 6),
            "first based-loop moment changed")
    return {
        "eta": "t(1-t)",
        "eta_endpoints": [str(eta_at_zero), str(eta_at_one)],
        "integral_d_eta": str(unweighted),
        "integral_t_d_eta": str(first_weighted),
    }


def h3_shifted_restriction_audit() -> dict[str, object]:
    occurrence = load_occurrence_module()
    order = 3
    vertices = tuple(range(2 * order))
    source = occurrence.occurrences(vertices)
    source_count = occurrence.occurrence_count(order)
    lower_count = occurrence.occurrence_count(order - 1)
    require(len(source) == source_count == 90, "h3 occurrence count changed")
    require(lower_count == 12, "h2 occurrence count changed")

    marked = source[0]
    marked_edges = tuple(marked[2])
    require(len(marked_edges) == order - 1 == 2,
            "marked residual edge count changed")

    # The physical candidate uses the normalized Euler reconstruction
    # (1/(r-1)) sum I_eD_e and then the first affine moment -1/6.
    reconstruction_normalization = Fraction(1, order - 1)
    moment = Fraction(-1, 6)
    component_scale = reconstruction_normalization * moment
    require(component_scale == Fraction(-1, 12),
            "shifted component normalization changed")

    all_edges = tuple(occurrence.edge(left, right)
                      for left in vertices for right in vertices
                      if left < right)
    reconstruction_multiplicity = {item: 0 for item in source}
    marked_records = []
    unmarked_constant_values = []
    detector_matrix = []

    for selected in all_edges:
        complement = tuple(site for site in vertices if site not in selected)
        lower = occurrence.occurrences(complement)
        restricted_images = {}
        for item in source:
            image = occurrence.restrict_occurrence(item, selected)
            if image is None:
                continue
            restricted_images[image] = item
            reconstruction_multiplicity[item] += 1
        require(set(restricted_images) == set(lower),
                ("restriction stopped being bijective", selected))

        marked_image = occurrence.restrict_occurrence(marked, selected)
        raw = tuple(Fraction(source_count if item == marked_image else 0) - 1
                    for item in lower)
        shifted = tuple(component_scale * entry for entry in raw)

        if selected in marked_edges:
            require(marked_image is not None, "lost marked lower occurrence")
            centered = tuple(
                Fraction(lower_count if item == marked_image else 0) - 1
                for item in lower
            )
            constant = tuple(Fraction(1) for _ in lower)
            expected_raw = tuple(
                Fraction(15, 2) * center + Fraction(13, 2) * one
                for center, one in zip(centered, constant, strict=True)
            )
            require(raw == expected_raw,
                    ("h3 marked restriction formula changed", selected))
            expected_shifted = tuple(
                Fraction(-5, 8) * center + Fraction(-13, 24) * one
                for center, one in zip(centered, constant, strict=True)
            )
            require(shifted == expected_shifted,
                    ("affine marked restriction formula changed", selected))

            marked_index = lower.index(marked_image)
            comparison_index = next(
                index for index in range(len(lower)) if index != marked_index
            )
            detector = tuple(
                Fraction(1) if index == marked_index else
                Fraction(-1) if index == comparison_index else Fraction(0)
                for index in range(len(lower))
            )
            require(dot(detector, constant) == 0,
                    "primitive detector stopped killing common H0")
            require(dot(detector, shifted) == Fraction(-15, 2),
                    "shifted lower centered detector changed")
            detector_matrix.append(tuple(
                Fraction(1) if row == len(marked_records) else Fraction(0)
                for row in range(2)
            ))
            marked_records.append({
                "edge": list(selected),
                "raw_decomposition": "(15/2)c_lower+(13/2)1",
                "shifted_normalized_decomposition":
                    "(-5/8)c_lower-(13/24)1",
                "constant_killing_detector": "e_marked^*-e_other^*",
                "detector_value": str(dot(detector, shifted)),
            })
        else:
            require(marked_image is None, "unmarked cut retained marked item")
            require(set(shifted) == {Fraction(1, 12)},
                    ("unmarked shifted cut stopped being constant", selected))
            unmarked_constant_values.append(str(shifted[0]))

    require(set(reconstruction_multiplicity.values()) == {2},
            "sum I_eD_e stopped being 2 id")
    require(len(marked_records) == 2 and len(unmarked_constant_values) == 13,
            "h3 cut census changed")
    # The two detectors act on different labelled lower-cut summands.
    require(detector_matrix == [(Fraction(1), Fraction(0)),
                                (Fraction(0), Fraction(1))],
            "marked component detectors stopped being independent")

    top_scalar = moment * reconstruction_normalization * 2
    require(top_scalar == Fraction(-1, 6),
            "reinserted top scalar changed")
    return {
        "top_occurrence_count": source_count,
        "lower_occurrence_count_per_cut": lower_count,
        "raw_reconstruction": "sum_e I_e D_e=2 id",
        "normalized_reconstruction": "(1/2)sum_e I_e D_e=id",
        "affine_moment": str(moment),
        "reinserted_top_scalar": str(top_scalar),
        "marked_cut_count": len(marked_records),
        "marked_cuts": marked_records,
        "unmarked_cut_count": len(unmarked_constant_values),
        "unmarked_shifted_component": "(1/12)1_lower",
        "independent_marked_detectors": 2,
    }


def physical_typing_audit() -> dict[str, object]:
    restriction = (ROOT / (
        "notes/uniform-centered-occurrence-restriction-insertion-gate.md"
    )).read_text()
    c_one = (ROOT / (
        "notes/scalar-unit-c1-weighted-endpoint-bockstein-gate.md"
    )).read_text()
    complete = (ROOT / (
        "notes/h3-c1-complete-augmented-carrier-rank-gate.md"
    )).read_text()
    pointed = (ROOT / (
        "notes/h3-direct-free-normals-e14-pointed-composition-gate.md"
    )).read_text()
    require("word                 01211222" in restriction
            and "repeated-site type   P3+K2" in restriction,
            "restriction physical grade changed")
    require("has no affine path" in c_one
            and "no source-proved" in c_one,
            "fixed endpoint projector acquired a physical affine lift")
    require("An unshifted" in complete
            and "beta*c1" in complete,
            "shifted-versus-unshifted guard changed")
    require(r"p=(-Q,-\operatorname {ores})" in pointed
            and "same word/ridge/repeated grade" in pointed,
            "primitive pointed cap scope changed")
    require(r"h_v(H_0-u)e_{\rm Eq}" in restriction,
            "first physical Eq reset residual changed")

    return {
        "top_coefficient_grade": {
            "word": "01211222",
            "fine": "Q_(v,N)=t_v q_(v,N)",
            "repeated": "P3+K2",
        },
        "top_shadow_verdict": (
            "after same-edge reinsertion the shifted raw operator preserves "
            "the declared top coefficient label and acts by -1/6"
        ),
        "chain_verdict": (
            "D_e factors through separately labelled order-two occurrence "
            "modules; no pinned PP/Hasse source map fills their centered "
            "parts or transports their full word/fine/repeated labels"
        ),
        "effect_of_granting_p": (
            "the presently specified p=(-Q,-ores) grants the primitive/"
            "common-H0 cap and makes the scalar carrier available; it has "
            "no specified lower-centered restriction components, so both "
            "constant-killing detectors survive"
        ),
        "first_additional_physical_debt": (
            "a rho-compatible filler for the two marked order-two centered "
            "restriction faces, followed by the known reduced-Eq reset "
            "h_v(H0-u)e_Eq and complete protected/q transport"
        ),
        "not_a_terminal": (
            "the two occurrence-coordinate detectors are exact associated-"
            "graded obstructions, not physical terminal covectors until "
            "extended across the complete augmented source map"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gamma1 affine raw occurrence-cut gate",
        "pins": PINS,
        "affine_moment": affine_moment_audit(),
        "h3_shifted_restriction": h3_shifted_restriction_audit(),
        "physical_typing": physical_typing_audit(),
        "verdict": (
            "The canonical shifted raw occurrence operator has exactly the "
            "required -1/6 reinserted top shadow: (-1/6)(1/2)sum I_eD_e="
            "-1/6 id.  It is not Gamma1 in the physical complex.  Each of "
            "the two marked residual cuts retains -5/8 c_lower-13/24 H0; "
            "a constant-killing labelled detector reads -15/2 on either "
            "component.  Granting the current primitive cap p and common "
            "H0 removes neither centered component.  Thus raw affine "
            "restriction constructs the desired coefficient L1 column but "
            "does not prove its membership in the physical boundary D_Q.  "
            "The shortest positive addition is a rho-compatible physical "
            "lower-centered filler/totalization in word 01211222 and "
            "repeated P3+K2, with the reduced-Eq reset and q augmentation."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("affine raw occurrence ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("affine raw occurrence top residue: -1/6 EXACT")
    print("marked lower centered faces: two, detector value -15/2 each")
    print("physical Gamma1 after granting p: NOT CONSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
