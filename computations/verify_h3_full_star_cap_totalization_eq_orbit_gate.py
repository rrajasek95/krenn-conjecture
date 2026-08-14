#!/usr/bin/env python3
"""Apply the site-0 full-star Euler action to the literal h3 cap cube.

For the canonical cap matching

    M = 01 23 45 67

the full Hasse cap totalization is

    N = tau(H_m)(r_0-T) - tau(H_0-u) r_m.

The diagonal part of the literal trigger star is the vertex Euler operator
sum_i x_0i d/dx_0i.  On the translated/homogenized cube its natural action
also contains u d/du and eps_01 d/d eps_01.  This checker proves that the
extended action fixes N coefficientwise and retains the q23 and q45 proper
faces.  It then computes the first descent obstruction: projection to the
underived top is not a chain map, and its commutator is exactly
(H_0-u)e_Eq.  Thus the wanted transported Eq square occurs as a nonzero
associativity/descent defect, not as a constructed physical filler.

The checker also pins the already forced endpoint-even dq23:21 conormal,
its sigma mate, and the hidden lower/word-residue faces which would have to
be carried by any future occurrence-local P2 placement.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py":
        "deb84776e620dbf800b24a3a317545259ab6b902d9d07be48bd6ce93e0c6adce",
    "computations/verify_h3_endpoint_even_literal_operator_algebra_r0_action_gate.py":
        "42a30f9cd823a67a0733dfb6961ed224e228caa3236140c2e0803db686839ef7",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
    "computations/verify_h3_cplus_w_yw_cap_factorization.py":
        "0b42e8c7d9e308c93774e59eae030403f3c264e2bfe4b31e7782a0e57b78a506",
}
EXPECTED_LEDGER_SHA256 = "5da0aa4be82c58333e181bb324245453077ba39791f070bb322518351f139841"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def vertex_hasse_euler(polynomial, *, endpoint_epsilon=None,
                       homogenizer=False):
    """Euler action in the site-0, endpoint-Hasse, homogenizer directions."""
    answer = {}
    for term, coefficient in polynomial.items():
        weight = sum(
            1 for item in term
            if item[0] == "w" and 0 in item[1:3]
        )
        if endpoint_epsilon is not None:
            weight += term.count(endpoint_epsilon)
        if homogenizer:
            weight += term.count(("homogenizing", "u"))
        if weight:
            answer[term] = Q(weight) * coefficient
    return answer


def module_euler(full, element, *, endpoint_epsilon=None,
                 homogenizer=False):
    return {
        generator: value
        for generator, coefficient in element.items()
        if (value := vertex_hasse_euler(
            coefficient,
            endpoint_epsilon=endpoint_epsilon,
            homogenizer=homogenizer,
        ))
    }


def canonical_cap_cube(full) -> dict[str, object]:
    deleted = 1
    matching = ((2, 3), (4, 5))
    internal = full.internal_variables(matching)
    marked_u, marked_t = full.endpoint_variables(deleted)
    eps_u, eps_t, eps_e, eps_f = tuple(
        ("eps", name) for name in ("u", "t", "e", "f")
    )
    directions = {
        marked_u: eps_u,
        marked_t: eps_t,
        internal[0]: eps_e,
        internal[1]: eps_f,
    }
    require(marked_u == ("w", 0, 1, 0, 1)
            and marked_t == ("w", 6, 7, 2, 2)
            and internal == (
                ("w", 2, 3, 2, 1),
                ("w", 4, 5, 1, 2),
            ), (marked_u, marked_t, internal))

    chain, boundary, differential, target, ores = (
        full.translated_totalization(directions)
    )
    record = full.audit_one_cube(deleted, matching)
    require(record["indexed_hasse_cycle_terms"] == 17
            and record["denominator_selected_columns_by_internal_face"]
                == [5, 3, 3, 1]
            and record["top_chain"] == "r_0-T"
            and record["top_boundary"] == "Y*w"
            and record["target"] == record["ordinary_residue"] == 0,
            record)

    all_epsilons = (eps_u, eps_t, eps_e, eps_f)
    top = full.module_coefficient(chain, all_epsilons, all_epsilons)
    require(top == {
        "r_0": full.constant(), "T": full.constant(-1)
    }, top)

    # Omitting the eps_e coefficient retains the physical 23:21 factor;
    # omitting eps_f retains the sigma-paired 45:12 factor.
    q23_face = full.module_coefficient(
        chain, (eps_u, eps_t, eps_f), all_epsilons)
    q45_face = full.module_coefficient(
        chain, (eps_u, eps_t, eps_e), all_epsilons)
    expected_q23 = full.variable(internal[0])
    expected_q45 = full.variable(internal[1])
    require(q23_face == {
        "r_0": expected_q23, "T": full.scale(-1, expected_q23)
    }, q23_face)
    require(q45_face == {
        "r_0": expected_q45, "T": full.scale(-1, expected_q45)
    }, q45_face)

    return {
        "directions": directions,
        "epsilons": all_epsilons,
        "chain": chain,
        "boundary": boundary,
        "differential": differential,
        "target": target,
        "ores": ores,
        "record": record,
        "labels": {
            "parent": "01:01*23:21*45:12*67:22",
            "word": "01211222",
            "endpoint_directions": ["01:01", "67:22"],
            "internal_directions": ["23:21", "45:12"],
            "q23_face": "q23:21*(r0-T)",
            "q45_face": "q45:12*(r0-T)",
        },
    }


def full_star_action_audit(full, cube) -> dict[str, object]:
    directions = cube["directions"]
    eps_u = cube["epsilons"][0]
    tau_hm = full.translate(full.H_MIXED, directions)

    # Each matching contains exactly one edge incident to site 0, hence the
    # diagonal trigger star sum_i I_0i D_0i is Euler and fixes H_m.
    require(vertex_hasse_euler(full.H_MIXED) == full.H_MIXED,
            "site-0 Euler stopped fixing H_m")
    require(vertex_hasse_euler(full.H_PURE) == full.H_PURE,
            "site-0 Euler stopped fixing H_0")

    # Physical Euler alone misses precisely the translated 01 direction.
    other_directions = {
        item: epsilon for item, epsilon in directions.items()
        if epsilon != eps_u
    }
    missing_endpoint = full.scale(-1, full.multiply(
        full.variable(eps_u),
        full.translate(
            full.derivative(full.H_MIXED, (next(
                item for item, epsilon in directions.items()
                if epsilon == eps_u
            ),)),
            other_directions,
        ),
    ))
    physical_defect = full.add(
        vertex_hasse_euler(tau_hm), full.scale(-1, tau_hm))
    require(physical_defect == missing_endpoint
            and len(physical_defect) == 24,
            (len(physical_defect), len(missing_endpoint)))

    # The natural divided-Hasse and homogenizer directions repair both
    # losses.  The corrected action fixes every coefficient of N.
    require(vertex_hasse_euler(
        tau_hm, endpoint_epsilon=eps_u) == tau_hm,
        "divided-Hasse Euler stopped fixing tau(H_m)")
    require(vertex_hasse_euler(
        full.F_PURE, homogenizer=True) == full.F_PURE,
        "homogenized Euler stopped fixing H_0-u")
    corrected = module_euler(
        full, cube["chain"], endpoint_epsilon=eps_u, homogenizer=True)
    require(corrected == cube["chain"],
            "corrected full-star action stopped fixing N")
    require(full.apply_module_map(corrected, cube["differential"])
            == cube["boundary"], "corrected action changed dN")
    require(not full.apply_module_map(corrected, cube["target"])
            and not full.apply_module_map(corrected, cube["ores"]),
            "corrected action acquired target/ores")

    return {
        "diagonal_trigger_identity":
            "sum_i I_0i D_0i=sum_i x_0i*d/dx_0i",
        "matching_species_Euler_identity": "E_0(H_m)=H_m",
        "physical_Euler_defect":
            "-eps_01*tau_other(D_01 H_m)",
        "physical_Euler_defect_support": len(physical_defect),
        "corrected_operator":
            "E_0 + u*d/du + eps_01*d/d(eps_01)",
        "corrected_operator_on_N": "N",
        "corrected_boundary": "tau(H_m)*Y*w",
        "target": 0,
        "ordinary_residue": 0,
        "interpretation": (
            "the literal full-star action exists on the complete translated "
            "Hasse/homogenized cap cube"
        ),
    }


def underived_eq_defect_audit(full, cube) -> dict[str, object]:
    all_epsilons = cube["epsilons"]
    top = full.module_coefficient(
        cube["chain"], all_epsilons, all_epsilons)
    original_differential = {
        "r_0": {"eq": full.F_PURE},
        "r_m": {"eq": full.H_MIXED},
        "T": {"w": full.scale(-1, full.CAP_Y)},
        "rho": {"w": full.constant()},
    }
    projected_boundary = full.apply_module_map(top, original_differential)
    require(projected_boundary == {
        "eq": full.F_PURE, "w": full.CAP_Y
    }, projected_boundary)
    top_of_boundary = full.module_coefficient(
        cube["boundary"], all_epsilons, all_epsilons)
    require(top_of_boundary == {"w": full.CAP_Y}, top_of_boundary)
    commutator = full.module_add(
        projected_boundary, full.module_scale(-1, top_of_boundary))
    require(commutator == {"eq": full.F_PURE}, commutator)
    require(len(full.F_PURE) == 91
            and full.F_PURE.get((("homogenizing", "u"),)) == -1,
            "H_0-u normalization changed")

    return {
        "projection": "pi_top to the underived physical cap presentation",
        "d_pi_top_N": "(H_0-u)*e_Eq + Y*w",
        "pi_top_dN": "Y*w",
        "commutator": "[d,pi_top]N=(H_0-u)*e_Eq",
        "commutator_polynomial_terms": len(full.F_PURE),
        "homogenizer_coefficient": "-1",
        "commutator_nonzero": True,
        "is_exact_required_transported_square": True,
        "status": (
            "the desired Eq square is the first nonzero descent/module-"
            "associativity defect, not the boundary of a physical filler"
        ),
    }


def augmented_face_audit(operator_gate, private_gate, cone_gate,
                         cplus_gate) -> dict[str, object]:
    operator_ledger, operator_digest = operator_gate.audit()
    require(operator_digest == operator_gate.EXPECTED_LEDGER_SHA256,
            operator_digest)
    private_ledger, private_digest = private_gate.audit()
    require(private_digest == private_gate.EXPECTED_LEDGER_SHA256,
            private_digest)
    cone_ledger, cone_digest = cone_gate.audit()
    require(cone_digest == cone_gate.EXPECTED_LEDGER_SHA256, cone_digest)
    cplus_ledger, cplus_digest = cplus_gate.audit()
    require(cplus_digest == cplus_gate.EXPECTED_LEDGER_SHA256, cplus_digest)

    target = operator_ledger["augmented_source_target_pair_action"]
    export = operator_ledger["first_typed_Leibniz_export"]
    typed = export["typed_export"]
    reinsertion = private_ledger["q23_reinsertion"]
    actual = cone_ledger["actual_augmented_residual"]
    dressing = cone_ledger["root_word_physical_dressing"]
    cap_table = cplus_ledger["root_even_factorization"]
    require(target[
        "independent_target_obstruction_after_augmented_pair_action"] == 0
        and typed["detector_value"] == "35/72"
        and typed["augmentation"] == "0"
        and reinsertion["product_rule"]
            == "d(q23*a)=q23*d(a)+dq23*a"
        and actual["target_residual"] == 0
        and actual["root_reduced_Eq_residual"] == 0
        and dressing["required_hidden_faces_on_raw_Cplus"] == {
            "lower_private": "-E", "word_resolved_ores": "+E"
        }
        and cap_table["table"]["B_E=(r0-T)_E"] == {
            "Eq": "+E", "Yw": "+E", "W": "+E",
            "target": "0", "ainc": "-sum(E)=0"
        }, (target, typed, reinsertion, actual, dressing, cap_table))

    return {
        "universal_proper_faces_supplied_by_N": [
            "q23:21*(r0-T)", "q45:12*(r0-T)"
        ],
        "source_labelled_P2_landing_supplied_by_N": False,
        "conditional_q23_Leibniz_rule": reinsertion["product_rule"],
        "forced_0102_dq23_face": {
            "coefficient_dimension": typed["coefficient_dimension"],
            "endpoint_parity": typed["endpoint_parity"],
            "augmentation": typed["augmentation"],
            "detector": typed["primitive_detector"],
            "detector_value": typed["detector_value"],
            "ordinary_residue": typed["ordinary_residue_value"],
        },
        "sigma_mate": {
            "word": "0121",
            "cut": "q45:12",
            "detector_value": "35/72 after sigma transport",
        },
        "root_even_cap_top": cap_table["table"]["B_E=(r0-T)_E"],
        "hidden_faces_required_on_raw_Cplus": dressing[
            "required_hidden_faces_on_raw_Cplus"],
        "remaining_complete_Eq": actual[
            "complete_Eq_residual_after_target_Eq_cone"]["residual"],
        "remaining_labelled_residue": actual[
            "labelled_ordinary_residue_residual"][
                "forced_class_mod_old_diagonal_Cartan_span"],
        "target_obstruction_after_augmented_pair": 0,
        "warning": (
            "N supplies the universal q faces in the derived Hasse cube, "
            "but it does not identify them with the occurrence-local P2 "
            "vectors; 35/72 is forced only after that landing is granted"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    full = load(
        "computations/verify_h3_full_hasse_koszul_cap_totalization.py",
        "full_star_cap_totalization_full_hasse",
    )
    operator_gate = load(
        "computations/verify_h3_endpoint_even_literal_operator_algebra_r0_action_gate.py",
        "full_star_cap_totalization_operator",
    )
    private_gate = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "full_star_cap_totalization_private",
    )
    cone_gate = load(
        "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py",
        "full_star_cap_totalization_cone",
    )
    cplus_gate = load(
        "computations/verify_h3_cplus_w_yw_cap_factorization.py",
        "full_star_cap_totalization_cplus",
    )
    cube = canonical_cap_cube(full)
    ledger = {
        "theorem": "h3 full-star action on explicit cap totalization Eq orbit",
        "pins": PINS,
        "canonical_cube": {
            **cube["labels"],
            "indexed_Hasse_terms": cube["record"][
                "indexed_hasse_cycle_terms"],
            "proper_face_support": cube["record"][
                "denominator_selected_columns_by_internal_face"],
            "top": cube["record"]["top_chain"],
            "top_boundary": cube["record"]["top_boundary"],
        },
        "full_star_divided_Hasse_action":
            full_star_action_audit(full, cube),
        "first_underived_module_associativity_defect":
            underived_eq_defect_audit(full, cube),
        "augmented_and_typed_faces": augmented_face_audit(
            operator_gate, private_gate, cone_gate, cplus_gate),
        "verdict": (
            "The corrected full-star divided-Hasse Euler operator acts "
            "strictly on the complete translated/homogenized cap "
            "totalization and retains both q23 and q45 proper faces.  Its "
            "top projection does not descend to the underived physical "
            "Eq/P2 presentation: the first commutator is exactly "
            "(H_0-u)e_Eq, with homogenizer coefficient -1.  Hence the "
            "wanted Eq square has been identified source-exactly but occurs "
            "as the obstruction, not as a filler.  Target normals already "
            "close.  A physical solution still requires an occurrence-local "
            "P2 landing carrying the hidden (-E,+E) lower/ores pair and the "
            "forced dq23/dq45 conormals"
        ),
        "scope": (
            "exact rational canonical cube M=01*23*45*67 in word 01211222; "
            "all 17 indexed Hasse terms and the [5,3,3,1] proper-face "
            "support; endpoint-even quotient; q23 representative and sigma "
            "mate; protected Eq/Yw/W/target/ainc table and hidden root-word "
            "lower/ores signatures.  This is not a construction of the "
            "occurrence-local P2 placement, a transferred SDR action, or a "
            "global all-matching response-to-cap map"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("full-star cap-totalization ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "cube", "action", "defect", "faces"), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        defect = ledger["first_underived_module_associativity_defect"]
        faces = ledger["augmented_and_typed_faces"]
        print(f"h3 full-star cap Eq orbit ({arguments.mode}): PASS")
        print("full translated Hasse action: STRICT")
        print("underived descent:", defect["commutator"])
        print("target obstruction:",
              faces["target_obstruction_after_augmented_pair"])
        print("forced dq23 detector:",
              faces["forced_0102_dq23_face"]["detector_value"])
        print("physical Eq/P2 orbit constructed: NO")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
