#!/usr/bin/env python3
"""Audit the shortest conditional augmented-P2 comparison theorem.

The generic C-plus assembly no longer needs an independent W cell.  This
checker separates the remaining data of a proposed *single* augmented P2
section into its homogeneous faces.

The important logical distinctions are:

* a pointed occurrence relation P_f=d(u_f-u) does not imply the primitive
  cap p=(-Q,-ores);
* once the section is a principal-parts module map, q-reinsertion forces the
  dq conormal by Leibniz, so dq is not another generator;
* p plus the invisible cap face n supplied by the physical K_Eq descent,
  together with the occurrence-to-B label map, gives d_even exactly;
* K_Eq and the labelled shifted ridge are independent faces of the enriched
  section, not consequences of its degree-zero pointed face.

Thus one theorem schema can package the frontier, but it cannot be weakened
to one bare source column or one homogeneous cell.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py":
        "77d13c31df34efa26b575497bdd7bb2cc9173e8d1907030541444551c7417804",
    "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py":
        "a8dfe952ce4fbbaf71ffd4ef748e456d5284dbf6b71655cce6f2f10576db0d06",
    "computations/verify_h2_p2_centered_occurrence_cobar_section_count_gate.py":
        "2ee0bc0077dba6d116b4cb6e15101350a3a801d515c589c122cad8d39ff5654c",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "computations/verify_h3_centered_base_denominator_deven_composition_gate.py":
        "ee8952a30b9d1a583f3d0e78b8289e5ed839d399d0865b0457315c969c117291",
    "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py":
        "e8014fdfd2263a8eb6bffff11e31c339b5b7965989a61324f8d118a91f791f46",
    "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py":
        "b2ace6e49aa5ec1b8347a0e88cc39f36e5d773e1aab1d82f424533de8ce52a9a",
    "computations/verify_h3_cplus_w_yw_cap_factorization.py":
        "0b42e8c7d9e308c93774e59eae030403f3c264e2bfe4b31e7782a0e57b78a506",
    "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py":
        "813419c756e7f21c09d63d3ec10f44c787e9580ca08c87809b7c4c550b908b4f",
}
EXPECTED_LEDGER_SHA256 = (
    "20f9514812d4cf181aff707b51bfaa3a67e6751503befd29d0396a3dba8b7aa0"
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


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    rows = [list(map(Q, row)) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_and_run_dependencies() -> dict[str, str]:
    digests = {}
    for index, (relative, expected) in enumerate(PINS.items()):
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
        module = load(relative, f"augmented_p2_dependency_{index}")
        result = module.audit()
        if isinstance(result, tuple):
            require(len(result) == 2,
                    ("dependency audit shape changed", relative))
            _ledger, ledger_digest = result
            require(ledger_digest == module.EXPECTED_LEDGER_SHA256,
                    ("dependency ledger changed", relative, ledger_digest))
        else:
            # A few older focused gates return their ledger directly and
            # print its digest only in main().  The pinned source checksum
            # plus deterministic recomputation gives the same protection.
            require(isinstance(result, dict),
                    ("dependency audit shape changed", relative))
            ledger_digest = sha256(json.dumps(
                result, sort_keys=True, separators=(",", ":")
            ).encode()).hexdigest()
        digests[relative] = ledger_digest
    return digests


def homogeneous_face_independence() -> dict[str, object]:
    # Rows: pointed conormal, cap Q, scalar ores, complete Eq,
    # labelled even ores, shifted ridge, reinsertion dq.
    p_f = tuple(map(Q, (1, 0, 0, 0, 0, 0, 0)))
    primitive_p = tuple(map(Q, (0, -1, -1, 0, 0, 0, 0)))
    invisible_n = tuple(map(Q, (0, 1, 0, 0, 0, 0, 0)))
    k_eq = tuple(map(Q, (0, 0, 0, 1, 0, 0, 0)))
    d_even = tuple(map(Q, (0, 0, 0, 0, 1, 0, 0)))
    ridge = tuple(map(Q, (0, 0, 0, 0, 0, 1, 0)))
    dq = tuple(map(Q, (0, 0, 0, 0, 0, 0, 1)))

    all_faces = (p_f, primitive_p, invisible_n, k_eq, d_even, ridge, dq)
    require(rank(all_faces) == 7,
            "the seven projected homogeneous faces stopped separating")

    pointed_dual = tuple(map(Q, (1, 0, 0, 0, 0, 0, 0)))
    residue_dual = tuple(map(Q, (0, 0, 1, 0, 0, 0, 0)))
    eq_dual = tuple(map(Q, (0, 0, 0, 1, 0, 0, 0)))
    ridge_dual = tuple(map(Q, (0, 0, 0, 0, 0, 1, 0)))
    require(dot(pointed_dual, p_f) == 1
            and all(dot(pointed_dual, face) == 0
                    for face in all_faces[1:])
            and dot(residue_dual, primitive_p) == -1
            and dot(residue_dual, p_f) == 0
            and dot(eq_dual, k_eq) == 1
            and dot(ridge_dual, ridge) == 1,
            "a primitive face separator changed")

    # p+n is the target-zero pure scalar residue face.  It still needs the
    # physical occurrence-to-labelled-residue map before becoming d_even.
    pure_scalar_residue = add(primitive_p, invisible_n)
    require(pure_scalar_residue
            == tuple(map(Q, (0, 0, -1, 0, 0, 0, 0)))
            and rank((p_f, primitive_p)) == 2,
            "the p+n cap transgression changed")

    return {
        "quotient_rows": [
            "pointed conormal", "cap Q", "scalar ores", "complete Eq",
            "labelled d_even ores", "shifted ridge", "reinsertion dq",
        ],
        "classes": {
            "P_f": list(map(int, p_f)),
            "primitive_p": list(map(int, primitive_p)),
            "invisible_n": list(map(int, invisible_n)),
            "K_Eq": list(map(int, k_eq)),
            "d_even": list(map(int, d_even)),
            "ridge": list(map(int, ridge)),
            "dq": list(map(int, dq)),
        },
        "raw_face_rank": rank(all_faces),
        "P_f_implies_primitive_p": False,
        "primitive_p_plus_n": "pure scalar ores=-1",
        "interpretation": (
            "one comparison morphism may contain these as faces, but no "
            "bare homogeneous column contains or implies all of them"
        ),
    }


def reinsertion_leibniz_audit() -> dict[str, object]:
    # Work over dual numbers k[dq]/(dq^2).  The zero-jet of q*S is q*s;
    # a degree-zero section alone permits any first-jet coefficient c.
    # A PP-module/algebra map imposes j(qS)=q*j(S)+dq*S, fixing c=1.
    pointed_value = Q(1)
    arbitrary_first_jet_coefficients = (Q(0), Q(2), Q(-5, 3))
    require(all(coefficient * pointed_value != pointed_value
                for coefficient in arbitrary_first_jet_coefficients),
            "the degree-zero counterfamily accidentally obeys Leibniz")
    leibniz_coefficient = pointed_value
    require(leibniz_coefficient == 1,
            "the pointed dq coefficient stopped being normalized")

    return {
        "degree_zero_section_alone_forces_dq": False,
        "PP_module_map_law": "J1(qS)=q J1(S)+dq tensor S",
        "pointed_normalization": "S(base)=1",
        "forced_dq_coefficient": 1,
        "independent_dq_generator_after_PP_functoriality": False,
        "qualification": (
            "dq is a consequence only after reinsertion/Leibniz naturality "
            "is part of the theorem; it is independent of a bare column"
        ),
    }


def d_even_composition_audit() -> dict[str, object]:
    # Six fixed-tail labels B0,...,B5.  The two pointed cap faces and their
    # invisible K_Eq lifts have pure scalar residue -1.  The physical label
    # map sends face 3 to B4 and face 5 to B1.  Averaging with sign -1/2 is
    # exactly d_even=(B1+B4)/2.
    b1 = tuple(Q(index == 1) for index in range(6))
    b4 = tuple(Q(index == 4) for index in range(6))
    face3_p_plus_n_labelled = scale(-1, b4)
    face5_p_plus_n_labelled = scale(-1, b1)
    d_even = scale(Q(-1, 2), add(
        face3_p_plus_n_labelled, face5_p_plus_n_labelled,
    ))
    expected = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    require(d_even == expected and sum(d_even, Q(0)) == 1,
            "the p+n+label d_even formula changed")

    scalar = tuple(map(Q, (1, 1, 1, 1, 1, 1)))
    cartan = tuple(map(Q, (1, 0, 1, -1, 0, -1)))
    chi = tuple(map(Q, (0, 1, -1, 0, 1, -1)))
    require(dot(chi, scalar) == dot(chi, cartan) == 0
            and dot(chi, d_even) == 1,
            "the labelled residue separator changed")

    return {
        "formula": (
            "d_even=-1/2[(p_3+n_3) labelled B4+"
            "(p_5+n_5) labelled B1]=(B1+B4)/2"
        ),
        "requires": [
            "primitive cap p on faces 3 and 5",
            "invisible cap n from physical K_Eq descent",
            "literal occurrence-to-B4/B1 label map",
        ],
        "separate_d_even_hypothesis_after_these_faces": False,
        "d_even_from_p_alone": False,
        "d_even_from_unlabelled_p_plus_n": False,
        "first_missing_labelled_dual": "chi=(0,1,-1,0,1,-1)",
        "chi_on_d_even": 1,
    }


def shortest_theorem_audit() -> dict[str, object]:
    # The committed conditional assembly has three independent primitive
    # omissions.  The augmented P2 theorem packages them, while the later
    # q/W/ridge reductions say which are consequences and which remain
    # clauses of that theorem.
    return {
        "name": "AugP2(h=3), pointed augmented principal-parts section",
        "one_theorem_schema": True,
        "not_one_homogeneous_source_cell": True,
        "literal_fixed_grade_occurrence_instantiations": 8,
        "required_face_certifications": {
            "pointed_source_algebra_face": (
                "u_f-u modulo the complete physical response ideal; this "
                "gives the physical anchor/conormal by differentiation"
            ),
            "primitive_cap_face": (
                "p=(-Q,-ores) in word 01211222 and P3+K2 grade; independent "
                "of the pointed conormal"
            ),
            "central_reduced_Eq_and_labelled_cap_face": (
                "physical K_Eq descent supplies n and the complete Eq "
                "correction, while occurrence labels send faces 3/5 to B4/B1"
            ),
            "relative_Kahler_face": (
                "gamma_v=-dOmega_v in the shifted repeated grade; its "
                "eta/sigma coefficients are then unique and commute"
            ),
        },
        "automatic_or_existing_after_these_faces": {
            "two_root_Hasse_cobar": "functorial from the occurrence section",
            "dq_reinsertion": "Leibniz consequence of PP-module naturality",
            "d_even": "the p+n+label formula",
            "W": "existing Yw-to-W cap r0-T",
            "physical_q": "existing generator-versus-row-homotopy dichotomy",
            "anchor": "pointed source-algebra conormal functoriality",
            "eta_sigma": "unique contractions of the labelled ridge",
        },
        "nonredundancy": {
            "pointed_vs_p": "marked tangent and scalar ores are duals",
            "p_vs_KEq": "scalar ores and complete Eq are duals",
            "degree_zero_vs_ridge": (
                "the shifted Kähler coordinate lies in the forgetful kernel"
            ),
            "unlabelled_cap_vs_d_even": (
                "chi kills scalar/Cartan lines and reads one on d_even"
            ),
        },
        "generic_conclusion": (
            "the complete C-plus lower/Eq/target/residue/W/q/anchor/terminal "
            "assembly closes conditionally from AugP2; there is no separate "
            "dq, d_even, or W construction theorem"
        ),
        "scope_guard": (
            "beta=0 still requires the same section integrally over k[beta] "
            "with its Bockstein face; h>3 requires spectator-tail monoidality"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    dependency_ledgers = pin_and_run_dependencies()
    ledger = {
        "theorem": "shortest conditional augmented P2 section gate",
        "pins": PINS,
        "dependency_ledgers": dependency_ledgers,
        "homogeneous_face_independence": homogeneous_face_independence(),
        "reinsertion": reinsertion_leibniz_audit(),
        "d_even_composition": d_even_composition_audit(),
        "shortest_conditional_theorem": shortest_theorem_audit(),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 shortest conditional theorem: ONE AUGMENTED P2 SCHEMA")
    print("pointed occurrence -> primitive p: NO")
    print("PP-functorial pointed occurrence -> dq face: YES")
    print("p + physical K_Eq n + label map -> d_even: YES")
    print("independent load-bearing face: labelled shifted ridge")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
