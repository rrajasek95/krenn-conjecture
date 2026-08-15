#!/usr/bin/env python3
"""Compose marked divided-root P2 with lower iota and the cap augmentation.

The missing-site/deleted-edge marks canonically recover the two lower labels

    0112/q23:21 -> B1,       0121/q45:12 -> B4.

After endpoint-even coefficient iota their normalized sum is delta_plus.
The actual marked/cap augmentation, however, is coefficientwise B=Eq.  Thus
the first protected comparison boundary (required minus actual) is

    (delta_plus,0) - (delta_plus,delta_plus) = (0,-delta_plus).

At root-word resolution the same obstruction is the hidden debt
(-E,0,+E).  Even granting arbitrary Cartan residue endpoints, arbitrary
tied M endpoints, their root-word bars, and the target cone leaves a clean
Eq-only coordinate.  A relative dK=(H0-u)E also does not supply an absolute
preimage after normalization.  Hence the divided-root construction closes
the label/word/fine/PP part, but not the protected B/Eq descent.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py":
        "9b387023ee8cac6bb000d6936a8985cbc16bbad0a9f7deb3613c1f44c233a1f8",
    "computations/verify_h3_divided_root_marked_deletion_p2_naturality.py":
        "fd90cee45e302193bc1cc38f23d643818761451c26064001f3eef1d966ab11b8",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
    "computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py":
        "7eef9d440fefbae174d2adc61b6f8bdc270351353884ba24e277d36714a9a364",
    "computations/verify_h3_normalized_eq_base_change_tor_gate.py":
        "b7c409db8cff0141a153816d0d14525464c4fcadb0607b97da06181435059d50",
    "computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py":
        "2e7a8640482bcde91241bde7b067131e46c0188cbf276c1c1a43243177ef3b7f",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
}
EXPECTED_LEDGER_SHA256 = (
    "5b3702348c3a49e8e73e104c2553afaef708f3bcc7019bd815d04a9b358ff73c"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right
                         for left, right in zip(rows[row], rows[answer],
                                                strict=True)]
        answer += 1
    return answer


def unit(width: int, index: int):
    return tuple(Q(position == index) for position in range(width))


def marked_label_iota_audit(p2, divided, lower):
    p2_ledger, p2_digest = p2.audit()
    require(p2_digest == p2.EXPECTED_LEDGER_SHA256, p2_digest)
    divided_ledger, divided_digest = divided.audit()
    require(divided_digest == divided.EXPECTED_LEDGER_SHA256, divided_digest)
    lower_ledger, lower_digest = lower.audit()
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256, lower_digest)

    p2_faces = p2_ledger["root_restriction_reinsertion"]["cuts"]
    selected = divided_ledger["selected_q23_q45_P2"]
    iota = lower_ledger["coefficient_iota"]
    require([(row["cut"], row["physical_core_target_word"],
              row["target_q_colour"]) for row in p2_faces]
            == [("23", "0112", "21"), ("45", "0121", "12")],
            p2_faces)
    require(selected["strict_marked_BC_objects"]
            and selected["marked_derived_word_fine_repeated_landing_rank"] == 2
            and selected["delete_q23"]["marked_derived_face"]
                == "0112/q23:21"
            and selected["delete_q45"]["marked_derived_face"]
                == "0121/q45:12", selected)
    require([row["marked_hole_image"] for row in iota["cut_maps"]]
            == ["B1", "B4"]
            and all(row["admissible_K4_relabels_with_same_marked_image"] == 4
                    for row in iota["cut_maps"])
            and iota["endpoint_odd_image"] == ["0"] * 6,
            iota)

    # Each even cut has image 2*c_i^+, and the iota normalization is 1/16.
    one = (Q(1),) * 6
    c1 = add(scale(6, unit(6, 1)), scale(-1, one))
    c4 = add(scale(6, unit(6, 4)), scale(-1, one))
    cut23 = scale(Q(1, 8), c1)
    cut45 = scale(Q(1, 8), c4)
    delta = add(cut23, cut45)
    expected_delta = tuple(map(Q, (-Q(1, 4), Q(1, 2), -Q(1, 4),
                                   -Q(1, 4), Q(1, 2), -Q(1, 4))))
    require(delta == expected_delta
            and [str(value) for value in delta] == iota["delta_plus"],
            (delta, iota["delta_plus"]))
    return {
        "canonical_mark_reconstruction": (
            "(cofactor,original missing site) recovers the deleted edge"
        ),
        "source_provenant_decorated_faces": [
            "0112/q23:21", "0121/q45:12",
        ],
        "coefficient_labels": ["B1", "B4"],
        "word_fine_repeated_image_rank": 2,
        "endpoint_odd_image": 0,
        "cut23_normalized_image": [str(value) for value in cut23],
        "cut45_normalized_image": [str(value) for value in cut45],
        "sum": "delta_plus",
        "sum_vector": [str(value) for value in delta],
        "conclusion": (
            "the marks now make the B1/B4 coefficient label map canonical "
            "on the endpoint-even marked-derived faces; they do not choose "
            "between the protected B and Eq copies of that coefficient"
        ),
    }, cut23, cut45, delta


def protected_commutator_audit(cut23, cut45, delta, direct, cap):
    direct_ledger, direct_digest = direct.audit()
    require(direct_digest == direct.EXPECTED_LEDGER_SHA256, direct_digest)
    cap.pin_dependencies()
    cap_scope = cap.dependency_scope_audit()["cap_r0"]
    require(cap_scope["B_Eq_tied"]
            and cap_scope["differential"] == "d r_0=(H_0-u)e_Eq",
            cap_scope)

    zero = (Q(0),) * 6
    actual23 = cut23 + cut23
    actual45 = cut45 + cut45
    desired23 = cut23 + zero
    desired45 = cut45 + zero
    comm23 = add(desired23, scale(-1, actual23))
    comm45 = add(desired45, scale(-1, actual45))
    actual = add(actual23, actual45)
    desired = add(desired23, desired45)
    commutator = add(desired, scale(-1, actual))
    require(commutator == zero + scale(-1, delta)
            and add(comm23, comm45) == commutator,
            commutator)

    d6 = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    omega = d6 + scale(-1, d6)
    require(dot(omega, actual) == 0
            and dot(omega, desired) == 3
            and dot(omega, commutator) == 3,
            (dot(omega, actual), dot(omega, desired),
             dot(omega, commutator)))
    require(rank((actual23, actual45)) == 2
            and rank((comm23, comm45)) == 2
            and rank((actual23, actual45, desired23, desired45)) == 4,
            "the two-cut protected ranks changed")
    protected = direct_ledger["direct_derived_N_in_PAComp"][
        "first_protected_use_of_cap_modulo_Eq"]
    require(protected["termwise_N_readout"] == "(delta_plus,delta_plus)"
            and protected["required_physical_readout"] == "(delta_plus,0)"
            and protected["residual"] == "(0,-delta_plus)", protected)
    return {
        "actual_cap_top_is_tied": True,
        "actual_composite": "(delta_plus,delta_plus)",
        "required_physical_landing": "(delta_plus,0)",
        "defined_commutator_orientation": "required minus actual composite",
        "cut23_commutator": "(0,-c_1^+/8)",
        "cut45_commutator": "(0,-c_4^+/8)",
        "combined_first_commutator": "(0,-delta_plus)",
        "two_cut_commutator_rank": 2,
        "integral_dual": "(D6,-D6), D6=(-1,2,-1,-1,2,-1)",
        "dual_on_actual_required_commutator": ["0", "3", "3"],
        "target_commutator": 0,
        "first_PP_private_detector": "35/72",
        "first_PP_ordinary_residue": 0,
        "meaning": (
            "B1/B4 are no longer ambiguous labels.  What fails is the "
            "protected copy separation: the physical cap totalization "
            "duplicates each marked coefficient into Eq"
        ),
    }


def correction_inventory_audit(sigma, hidden, normalized):
    sigma_ledger, sigma_digest = sigma.audit()
    require(sigma_digest == sigma.EXPECTED_LEDGER_SHA256, sigma_digest)
    augmented = sigma_ledger["actual_augmented_residual"]
    dressing = sigma_ledger["root_word_physical_dressing"]
    require(augmented["complete_Eq_residual_after_target_Eq_cone"]
                ["residual"] == ["0", "-delta_plus"]
            and augmented["target_residual"] == 0
            and augmented["root_reduced_Eq_residual"] == 0
            and dressing["required_hidden_faces_on_raw_Cplus"]
                == {"lower_private": "-E", "word_resolved_ores": "+E"},
            (augmented, dressing))

    hidden_ledger, hidden_digest = hidden.audit()
    require(hidden_digest == hidden.EXPECTED_LEDGER_SHA256, hidden_digest)
    grant = hidden_ledger["strong_universal_grant"]
    require(grant["span"] == "{(x,x,z): x,z in Q^24}"
            and grant["rank"] == grant["rank_after_sigma_bars"] == 48
            and hidden_ledger["required_hidden_debt"]
                ["signature_lower_Eq_ores"] == ["-E", "0", "+E"]
            and hidden_ledger["primitive_dual"]["pairings_on_hidden_debt"]
                == ["2", "-2", "2", "-2"], hidden_ledger)

    normalized_ledger, normalized_digest = normalized.audit()
    require(normalized_digest == normalized.EXPECTED_LEDGER_SHA256,
            normalized_digest)
    relative = normalized_ledger["relative_versus_absolute_filler"]
    require(relative["relative_boundary_before_base_change"] == "dK_rel=t*E"
            and relative["relative_cap_homology_H0_H1"] == [1, 1]
            and relative["absolute_boundary"] == "dK_abs=E"
            and relative["absolute_cap_homology_H0_H1"] == [0, 0],
            relative)
    return {
        "already_closed": {
            "mixed_target": 0,
            "root_reduced_Eq": 0,
        },
        "still_forced": {
            "complete_Eq": "-delta_plus",
            "labelled_ordinary_residue": "v=(B1+B4)/2",
            "root_word_hidden_debt": "H=(-E,0,+E)",
        },
        "stronger_than_existing_K_Eq_target_ores_grant": {
            "granted_span": "K_u=(0,0,u), M_u=(u,u,0), and all endpoint bars",
            "span_rank_before_after_bars": [48, 48],
            "hidden_debt_raises_rank": True,
            "primitive_pairings": ["2", "-2", "2", "-2"],
        },
        "exact_hidden_decomposition": "H=-M_E+K_E+C_Eq",
        "missing_coordinate": "C_Eq=(0,E,0), an absolute clean Eq-only preimage",
        "relative_K_Eq_is_not_absolute": {
            "boundary": "(H0-u)E",
            "after_normalization_H0_H1": [1, 1],
        },
        "verdict": (
            "no existing K_Eq, target-cone, labelled-ores/Cartan endpoint, "
            "or root-word endpoint bar supplies the Eq-only correction"
        ),
    }


def audit():
    pin_dependencies()
    p2 = load(
        "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py",
        "p2_iota_p2",
    )
    divided = load(
        "computations/verify_h3_divided_root_marked_deletion_p2_naturality.py",
        "p2_iota_divided",
    )
    lower = load(
        "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py",
        "p2_iota_lower",
    )
    sigma = load(
        "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py",
        "p2_iota_sigma",
    )
    hidden = load(
        "computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py",
        "p2_iota_hidden",
    )
    normalized = load(
        "computations/verify_h3_normalized_eq_base_change_tor_gate.py",
        "p2_iota_normalized",
    )
    direct = load(
        "computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py",
        "p2_iota_direct",
    )
    cap = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "p2_iota_cap",
    )
    label_ledger, cut23, cut45, delta = marked_label_iota_audit(
        p2, divided, lower)
    ledger = {
        "theorem": "h3 divided-root P2/lower-iota protected B-Eq commutator gate",
        "pins": PINS,
        "marked_lower_iota": label_ledger,
        "protected_cap_commutator": protected_commutator_audit(
            cut23, cut45, delta, direct, cap),
        "existing_correction_inventory": correction_inventory_audit(
            sigma, hidden, normalized),
        "scope": (
            "exact endpoint-even rational h=3 marked-derived P2 orbit, both "
            "physical cuts, all six lower coefficient labels, actual tied "
            "cap readout, complete Eq, target, labelled ores and the 24 "
            "root-word coordinates.  This excludes the current correction "
            "inventory, not an unmodelled absolute bright physical primitive"
        ),
        "conclusion": (
            "The divided-root/missing-site data canonically constructs the "
            "B1/B4 coefficient augmentation and removes the old word/fine/"
            "operation ambiguity at the marked-derived level.  Composing "
            "with the actual cap totalization is nevertheless tied B=Eq.  "
            "Its first protected commutator is exactly (0,-delta_plus), "
            "with hidden root-word faces (-E,0,+E).  Existing K_Eq, target "
            "and ores/Cartan cells do not supply the required absolute "
            "Eq-only coordinate"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 divided-root P2/lower-iota protected commutator: SHARP NO-GO")
        print("mode", arguments.mode)
        print("B1/B4 coefficient labels: CANONICAL")
        print("actual cap landing: (delta_plus,delta_plus)")
        print("first commutator: (0,-delta_plus)")
        print("existing K_Eq/target/ores absolute correction: NONE")
        print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
