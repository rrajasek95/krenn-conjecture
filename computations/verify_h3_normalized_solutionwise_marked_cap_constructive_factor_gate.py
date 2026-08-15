#!/usr/bin/env python3
"""Separate solutionwise B projection from physical cap realization.

At t=H0-u=0 the marked top projection is a chain map, so the surviving Eq
cokernel does not obstruct the bare selected coefficient map to B.  But the
Eq class does not vanish under this base change: it survives in H0.  More
importantly for the constructive branch, the marked parent/collision object
has no current realization as an actual cap covector K with the R-algebra
multiplication and contraction used by the private-site and clean-descent
theorems.  That missing realization is independent of t.
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
    "computations/verify_h3_normalized_eq_base_change_tor_gate.py":
        "b7c409db8cff0141a153816d0d14525464c4fcadb0607b97da06181435059d50",
    "computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py":
        "2e7a8640482bcde91241bde7b067131e46c0188cbf276c1c1a43243177ef3b7f",
    "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py":
        "9b387023ee8cac6bb000d6936a8985cbc16bbad0a9f7deb3613c1f44c233a1f8",
    "computations/verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py":
        "d04ad992bde820edcc79b2660e64a141db8ff52a39a6a78be6c470105467106a",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_clean_pair_cap_exact_descent_symbolic.py":
        "d6507c2afa341ce5c15056feddf92b9a171e2a5c80652617b595c7c7cf35acf5",
}
EXPECTED_LEDGER_SHA256 = (
    "5cc82789e11d4ff6c86a2787ce62a3cb6cc5d08c1d39c8b4bc48d40c9b69f496"
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


def solutionwise_base_change_audit(normalized):
    normalized_ledger, normalized_digest = normalized.audit()
    require(normalized_digest == normalized.EXPECTED_LEDGER_SHA256,
            normalized_digest)
    comparison = normalized_ledger["normalized_comparison"]
    relative = normalized_ledger["relative_versus_absolute_filler"]
    require(comparison["evident_map_is_chain_map_after_base_change"]
            and comparison["mapping_cone_homology_H0_H1_H2"] == [1, 0, 0]
            and comparison["surviving_class"] == "E=e_Eq"
            and relative["relative_cap_homology_H0_H1"] == [1, 1],
            (comparison, relative))

    # The B projection exists on the t=0 fibre, but it is a quotient map,
    # not a proof that the Eq coordinate of the tied lift became zero.
    tied = tuple(map(Q, (1, 1)))
    b_projection = tuple(map(Q, (1, 0)))
    eq_class = tuple(map(Q, (0, 1)))
    omega = tuple(map(Q, (1, -1)))
    require(dot(omega, tied) == 0
            and dot(omega, b_projection) == 1
            and dot(omega, eq_class) == -1
            and rank((tied, b_projection)) == 2,
            "the normalized B/Eq fibre changed")
    return {
        "base_change": "t=H0-u=0",
        "what_vanishes": "the chain-map defect t*e_Eq",
        "what_does_not_vanish": "the fibre class e_Eq",
        "mapping_cone_H0_H1_H2": [1, 0, 0],
        "solutionwise_B_top_projection_is_chain_map": True,
        "solutionwise_B_top_projection_is_quasi_isomorphism": False,
        "tied_lift_equals_B_only_after_base_change": False,
        "B_only_projection_is_available_as_a_quotient": True,
        "warning": (
            "R/(t) tensor R/(t) is R/(t), not zero: t-torsion is supported "
            "on the exact-source fibre rather than killed by restricting to it"
        ),
    }


def current_constructive_interface_audit(direct, p2, private, clean):
    # The full surrounding Schreyer replay is hash-pinned.  This interface
    # uses only its exact downstream PAComp type census.
    chase = direct.end_to_end_pacomp_chase()
    require(not chase["nonzero_active"]
                ["physical_active_cap_is_statable_on_N_alone"]
            and chase["private_site_identity"]["status_on_N"] == "NOT DEFINED"
            and chase["N_to_Nminus2_reconstruction"]["status_on_N"]
                == "NOT DEFINED", chase)

    # The newer divided-root theorem closes the word/P2 and first-PP defects
    # which the older end-to-end ledger listed as its second local failure.
    p2_ledger, p2_digest = p2.audit()
    require(p2_digest == p2.EXPECTED_LEDGER_SHA256, p2_digest)
    restricted = p2_ledger["root_restriction_reinsertion"]
    pointed = p2_ledger["pointed_occurrence_and_dq"]
    require(restricted["two_cut_word_image_rank"] == 2
            and pointed["pointed_occurrence_section_in_marked_derived_category"]
            and pointed["dq23_detector"] == "35/72",
            (restricted, pointed))

    # Replay one literal target-augmented private-site identity.  It consumes
    # physical cells and multiplication, not parent labels.
    private_module = private.load(
        "computations/verify_hafnian_private_site_matching_bijection_lemma.py",
        "solutionwise_private_dependency",
    )
    identity = private.target_augmented_identity(private_module, 8)
    require(identity["exact_source_consequence"]
            == "sum_s Delta_us*C_s=-q_u", identity)

    # The full 6,890,625-monomial clean-cap replay is hash-pinned.  Only its
    # already frozen input theorem is needed for this interface audit.
    clean_input = clean.audit_normalization_and_decorated_lift()
    require(clean_input["requires"] == "s*kappa_0*kappa_1*kappa_2 != 0",
            clean_input)

    # A finite type guard after t=0.  The constructed marked object has a
    # parent coefficient and a target augmentation, but no actual K row.
    # The required realization is independent of t and raises rank.
    marked_target = tuple(map(Q, (1, 1, 0)))
    physical_cap = tuple(map(Q, (1, 1, 1)))
    cap_realization_dual = tuple(map(Q, (0, 0, 1)))
    require(rank((marked_target,)) == 1
            and rank((marked_target, physical_cap)) == 2
            and dot(cap_realization_dual, marked_target) == 0
            and dot(cap_realization_dual, physical_cap) == 1,
            "the cap-realization type guard changed")
    return {
        "newly_closed_before_this_audit": [
            "derived response-to-cap word/operation section",
            "both q23/q45 P2 restrictions",
            "pointed occurrence and first q/dq PP faces",
        ],
        "first_t_independent_missing_map": (
            "ev_cap,A:N tensor_R R/(t) -> Cap_phys(A;p,q)"
        ),
        "required_properties_of_ev_cap": [
            "pointed and R/(t)-linear for the actual source algebra",
            "sends the selected marked class to an actual cap covector K",
            "reflects normalized target/nonvanishing",
            "commutes with physical multiplication and cofactor contraction",
        ],
        "rank_guard_coordinates": ["parent coefficient", "target", "actual K"],
        "marked_target_vector": [1, 1, 0],
        "required_physical_cap_vector": [1, 1, 1],
        "cap_realization_dual": [0, 0, 1],
        "private_site_requires": identity["source_identity"],
        "clean_descent_requires": clean_input["requires"],
        "why_this_is_not_t_torsion": (
            "the K-realization, source multiplication, cofactors and the "
            "nonvanishing product s*kappa_0*kappa_1*kappa_2 are absent "
            "after t has already been set to zero"
        ),
    }


def audit():
    pin_dependencies()
    normalized = load(
        "computations/verify_h3_normalized_eq_base_change_tor_gate.py",
        "solutionwise_normalized",
    )
    direct = load(
        "computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py",
        "solutionwise_direct",
    )
    p2 = load(
        "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py",
        "solutionwise_p2",
    )
    private = load(
        "computations/verify_uniform_target_augmented_private_site_active_minor.py",
        "solutionwise_private",
    )
    clean = load(
        "computations/verify_clean_pair_cap_exact_descent_symbolic.py",
        "solutionwise_clean",
    )
    ledger = {
        "theorem": "h3 normalized solutionwise marked-cap constructive factor gate",
        "pins": PINS,
        "solutionwise_base_change": solutionwise_base_change_audit(normalized),
        "constructive_PAComp_interface": current_constructive_interface_audit(
            direct, p2, private, clean),
        "constructive_verdict": (
            "normalization is enough for the bare B coefficient projection "
            "and an absolute Eq preimage is therefore not logically required "
            "for a future constructive proof.  It is not enough for the "
            "current PAComp proof: no solutionwise physical cap-realization "
            "map to K, multiplication/private-site contraction, or active-clean "
            "nonvanishing theorem has been constructed"
        ),
        "terminal_verdict": (
            "the surviving e_Eq fibre class remains relevant to universal "
            "comparison and Fredholm promotion; it does not vanish merely "
            "because its multiple t*e_Eq is the chain-map defect"
        ),
        "scope": (
            "exact normalized two-term comparison, the now-constructed h3 "
            "marked word/P2/first-PP maps, the literal N=8 private-site "
            "identity, and the exact clean-pair descent input.  This does not "
            "exclude a new conservative solutionwise ev_cap construction"
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
        print("h3 normalized solutionwise marked-cap factor: SHARP FORK")
        print("mode", arguments.mode)
        print("bare B coefficient projection at t=0: YES")
        print("e_Eq fibre class vanishes at t=0: NO")
        print("physical cap realization/private-site/descent: NOT CONSTRUCTED")
        print("first t-independent datum: ev_cap,A to an actual covector K")
        print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
