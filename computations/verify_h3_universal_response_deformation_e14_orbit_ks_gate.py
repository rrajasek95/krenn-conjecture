#!/usr/bin/env python3
"""Audit the universal centered-response deformation as the E14 KS seed.

For the ninety occurrence response ``R=sum_M f_M`` consider

    R_s=R-s*N*f,  N=90.

Its derivative is ``-N*f``, whose class modulo the original response line
is ``-c_f`` for ``c_f=N*f-R``.  Thus this one-parameter family canonically
realizes the desired relative Kodaira--Spencer class.  It is not equivariant
under endpoint motion: an endpoint path sends the marked occurrence to a
different one.  The minimal equivariant replacement is the universal
augmentation-zero parameter family

    R_z=R-N*sum_M z_M f_M,  sum_M z_M=0.

Its tangent map is ``-N`` times the identity on the centered occurrence
module.  It commutes exactly with matching and endpoint adjacency, so all
B-polynomial curvatures from fa1a397 are induced automatically.

Tensoring this family with the moving-target D4 orbit is formally flat:
occurrence parameters and the four colour roots act on different factors.
The top KS class is the centered pure-target occurrence c_g, with the affine
target unit removed by the orbit-relative D4 cone.  This is a positive
orbit-relative construction; no fixed-label pullback is needed formally.

It still does not give a chain in the old fixed physical correction complex.
The transitivity triangle has nonzero conormal/KS class c_f.  A comparison
must send the new relative Tate/KS generator to the physical AugP2/E14
complex.  This is the first exact obstruction, and it is the same missing
source-labelled centered occurrence section, now presented canonically.

The cap graph and shifted ridge are formally horizontal over the response
parameter; the D4 ridge connection remains the known terminal-dark
``-d(q_xv^01)`` face.  Physical q is not defined on the new KS generator,
so q-horizontality cannot be asserted before the comparison exists.  Once a
protected physical comparison is built, its q defect is handled by the
existing transport-versus-relative-generator alternative.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
N = 90
PINS = {
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "notes/h3-centered-occurrence-same-grade-physical-gate.md":
        "b183f3b5dab83fa79d17c3f539b9f146e3be176a96bfe52b267529148b64134a",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
    "notes/h3-scaled-occurrence-anchor-bridge-alternative.md":
        "d89d40b3ff69e0d7dc8105b1aa1eea40dceabc84007c1b9759d1a2932ecba572",
    "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py":
        "42bf68eeb963d568d1c8d9156d4176bec31a114b6fe804744833364fe3633475",
    "notes/h3-e14-cap-graph-two-parameter-flat-transport-gate.md":
        "61c093eed30cd2fff1be086e6069d344e76a583ee31f93528a31aebe76c5c5d6",
    "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
    "notes/h3-e14-orbit-relative-d4-target-cone-gate.md":
        "6268689c54144cc09b6be596b81d8b4aa741e0590a83e664ec3f6e65b89187bf",
    "computations/verify_h3_endpoint_projector_common_c2plus_private_curvature_gate.py":
        "011e1882f9391a2e9ca1b58adce0cefdd4b3ced602f5ba823e1b3bbdadfdf6ce",
    "notes/h3-endpoint-projector-common-c2plus-private-curvature-gate.md":
        "a84bf36aec408b35ef8979190faa313e8f6188b4af2fd13e10a602d97d25e30f",
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "notes/h3-e14-selected-fibre-graph-keq-koszul-gate.md":
        "98cae28b58267abcffc47b571e52581a354950ef684df5f28b58dca88c60c6e7",
}
EXPECTED_LEDGER_SHA256 = "769845c7dc831d448d582f8108ea4fc71782c1df8e7e08d742a5dda378660d85"


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


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
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
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def universal_centered_ks_audit() -> dict[str, object]:
    response = (Q(1),) * N
    selected = (Q(1),) + (Q(0),) * (N - 1)
    centered = add(scale(N, selected), scale(-1, response))
    one_parameter_derivative = scale(-N, selected)
    relative_derivative = add(one_parameter_derivative, response)
    require(relative_derivative == scale(-1, centered)
            and sum(centered, Q(0)) == 0
            and rank((response, centered)) == 2,
            "the universal selected KS class changed")

    # The augmentation-zero parameter h_f=e_f-one/N maps to -c_f.  On the
    # full centered subspace, multiplication by -N is an isomorphism over
    # the characteristic-zero theorem field.
    h_f = add(selected, scale(Q(-1, N), response))
    require(scale(-N, h_f) == scale(-1, centered),
            "the augmentation-zero parameter normalization changed")
    return {
        "response": "R=sum_M f_M",
        "one_parameter_family": "R_s=R-s*N*f",
        "one_parameter_derivative": "-N*f",
        "relative_class_modulo_R": "-c_f, c_f=N*f-R",
        "one_parameter_family_endpoint_equivariant": False,
        "minimal_equivariant_family": (
            "R_z=R-N*sum_M z_M f_M on sum_M z_M=0"
        ),
        "selected_centered_parameter": "h_f=e_f-(1/N)1",
        "KS_of_h_f": "-N*h_f=-c_f",
        "centered_parameter_dimension": N - 1,
        "KS_rank": N - 1,
        "KS_isomorphism_over_characteristic_zero": True,
        "source_family_is_monic_in_the_response_equation": True,
    }


def matching_endpoint_equivariance_audit() -> dict[str, object]:
    base = load(
        "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py",
        "universal_response_deformation_base",
    )
    occurrences = base.occurrences()
    lookup = {value: index for index, value in enumerate(occurrences)}
    ones = (Q(1),) * N

    def centered(vector):
        return add(scale(N, vector),
                   scale(-sum(vector, Q(0)), ones))

    def matching(vector):
        return add(base.apply_matching(vector, occurrences, lookup), vector)

    def endpoint(vector):
        return base.apply_endpoint(vector, occurrences, lookup)

    # C=N I-J commutes with every regular adjacency.  Verify on all basis
    # occurrence parameters, not only the selected tangent.
    for index in range(N):
        basis = base.unit(index, N)
        require(centered(matching(basis)) == matching(centered(basis))
                and centered(endpoint(basis)) == endpoint(centered(basis)),
                ("universal KS lost A/B equivariance", index))
    require(matching(ones) == scale(3, ones)
            and endpoint(ones) == scale(8, ones),
            "the occurrence adjacencies stopped being regular")

    curvature = load(
        "computations/verify_h3_endpoint_projector_common_c2plus_private_curvature_gate.py",
        "universal_response_deformation_curvature",
    )
    curvature_ledger, curvature_digest = curvature.audit()
    require(curvature_digest == curvature.EXPECTED_LEDGER_SHA256,
            "the endpoint curvature ledger changed")
    b_natural = curvature_ledger["B_polynomial_naturality"]
    require(b_natural["new_coefficient_generators_beyond_v0"] == 0
            and b_natural["one_B_natural_schema_carries_both_curvatures"],
            "the B-polynomial compression changed")
    return {
        "matching_degree": 3,
        "endpoint_degree": 8,
        "centered_KS_commutes_with_A_plus_I": True,
        "centered_KS_commutes_with_B": True,
        "basis_occurrences_checked": N,
        "C2_induced_polynomial": b_natural["C2_as_B_polynomial"],
        "C3_induced_polynomial": b_natural["C3_as_B_polynomial"],
        "coefficient_level_B_natural_schema": True,
        "physical_augmented_B_naturality_constructed": False,
    }


def d4_orbit_relative_family_audit() -> dict[str, object]:
    # Occurrence parameters and the four Boolean roots act on tensor factors.
    vertices = tuple(product((0, 1), repeat=4))
    edges = []
    squares = []
    for vertex in vertices:
        for direction in range(4):
            if vertex[direction]:
                continue
            target = list(vertex)
            target[direction] = 1
            edges.append((vertex, direction, tuple(target)))
        for left in range(4):
            for right in range(left + 1, 4):
                if vertex[left] or vertex[right]:
                    continue
                squares.append((vertex, left, right))
    require(len(edges) == 32 and len(squares) == 24,
            "the response-parameter/D4 tensor cube changed")

    orbit = load(
        "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py",
        "universal_response_deformation_orbit",
    )
    orbit_ledger, orbit_digest = orbit.audit()
    require(orbit_digest == orbit.EXPECTED_LEDGER_SHA256,
            "the orbit-relative D4 ledger changed")
    moving = orbit_ledger["moving_target_boolean_cube"]
    occurrence = orbit_ledger["marked_occurrence_local_system"]
    require(moving["moving_target_coefficients_by_order"] == [0, 0, 0, 0, 1]
            and occurrence["root_transport_on_occurrence_tags"]
                == "identity with coefficient 1"
            and occurrence["formal_D4_of_c_f"] == "c_g",
            "the D4 response-KS transport changed")
    return {
        "formal_family": (
            "R_(z,t)=g_t R-N sum_M z_M g_t f_M-Delta(t) on sum z=0"
        ),
        "occurrence_parameter_D4_edges": len(edges),
        "mixed_squares": len(squares),
        "mixed_curvature": 0,
        "root_transport_on_occurrence_tags": "coefficient 1",
        "bottom_KS": "-c_f in word 11:110000",
        "top_KS": "-c_g in G11[111111]",
        "affine_target_unit_removed_orbit_relatively": True,
        "fixed_label_pullback_needed_formally": False,
        "formal_orbit_relative_KS_construction": True,
    }


def fixed_physical_comparison_obstruction_audit() -> dict[str, object]:
    # Quotient coordinates (complete response R, centered c_f, new KS/Tate
    # generator epsilon_s).  The old fixed source sees only R.  The universal
    # family supplies d epsilon_s=c_f.  Forgetting epsilon_s raises the fixed
    # source rank by one, so a comparison/splitting is genuinely new data.
    response = (Q(1), Q(0), Q(0))
    centered = (Q(0), Q(1), Q(0))
    ks_generator = (Q(0), Q(0), Q(1))
    require(rank((response,)) == 1
            and rank((response, centered)) == 2
            and rank((response, centered, ks_generator)) == 3,
            "the KS transitivity quotient changed")
    dual = (Q(0), Q(1), Q(0))
    require(sum(left * right for left, right in
                zip(dual, response, strict=True)) == 0
            and sum(left * right for left, right in
                    zip(dual, centered, strict=True)) == 1,
            "the primitive fixed-fibre KS dual changed")
    return {
        "total_family": "presentation-safe monic response deformation",
        "special_fibre": "s=0 recovers the original response equation R",
        "relative_Tate_generator": "epsilon_s with d epsilon_s=c_f",
        "special_fibre_augmentation_exists": True,
        "flat_base_change_supplies_KS_splitting": False,
        "old_fixed_physical_source_contains_a_chosen_epsilon_s_image": False,
        "old_source_rank_then_centered_KS": [1, 2],
        "primitive_conormal_dual": [0, 1, 0],
        "first_exact_obstruction": (
            "construct a source-labelled comparison from epsilon_s in the "
            "relative response/cotangent complex to the fixed physical "
            "AugP2/E14 correction complex"
        ),
        "universal_family_alone_is_fixed_fibre_nullhomotopy": False,
        "interpretation": (
            "the family is flat and has its pointed s=0 augmentation; it "
            "canonically constructs the KS extension class but supplies no "
            "splitting/nullhomotopy of that class in the old fibre"
        ),
    }


def augmented_horizontal_readouts_audit() -> dict[str, object]:
    flat = load(
        "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py",
        "universal_response_deformation_flat",
    )
    flat_ledger, flat_digest = flat.audit()
    require(flat_digest == flat.EXPECTED_LEDGER_SHA256,
            "the cap/ridge flatness ledger changed")
    cap = flat_ledger["formal_C_times_D4_cap_local_system"]
    ridge = flat_ledger["shifted_Kahler_connection"]
    typing = flat_ledger["literal_physical_descent"]
    require(cap["root_curvature"] == 0
            and cap["root_holonomy"] == "identity"
            and ridge["mixed_root_curvature"] == 0
            and ridge["terminal_readouts_preserved"]
            and not ridge["physical_shifted_connection_face_constructed"],
            "the cap/ridge response-family scope changed")
    return {
        "response_parameter_on_cap_factor": "trivial",
        "cap_graph_s_horizontal": True,
        "cap_graph_D4_mixed_curvature": 0,
        "ridge_s_connection": 0,
        "ridge_D4_connection": ridge["connection_one_face"],
        "ridge_D4_mixed_curvature": ridge["mixed_root_curvature"],
        "ridge_terminal_eta_sigma_preserved": True,
        "formal_ridge_horizontal": True,
        "physical_ridge_horizontal": False,
        "physical_ridge_obstruction": typing["reason"],
        "physical_q_on_relative_KS_generator_defined": False,
        "q_first_typing_failure": (
            "q=sum6m-ainc is a cochain on the complete physical relative "
            "domain; the new epsilon_s has no physical image or assigned "
            "q value before the fixed-fibre comparison is constructed"
        ),
        "q_horizontality_can_be_demanded_now": False,
        "q_after_protected_comparison": (
            "use the existing defect alternative: q transports if the "
            "defect vanishes, and a nonzero defect yields the relative "
            "generator, provided both endpoint q readouts are physically typed"
        ),
        "new_independent_q_theorem_required": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "universal centered response deformation / E14 orbit KS gate",
        "pins": PINS,
        "universal_centered_KS": universal_centered_ks_audit(),
        "matching_endpoint_equivariance": matching_endpoint_equivariance_audit(),
        "D4_orbit_relative_family": d4_orbit_relative_family_audit(),
        "fixed_physical_comparison_obstruction": (
            fixed_physical_comparison_obstruction_audit()
        ),
        "augmented_horizontal_readouts": augmented_horizontal_readouts_audit(),
        "verdict": (
            "The family R_s=R-sNf canonically realizes -c_f modulo the old "
            "response line.  Its augmentation-zero 89-parameter completion "
            "is A/B-equivariant and induces the two endpoint curvatures as "
            "B-polynomials without new coefficient generators.  Tensoring "
            "with the moving-target D4 orbit gives a flat formal family and "
            "carries c_f to c_g with the target unit removed.  The first "
            "physical obstruction is the nonzero KS transitivity class: the "
            "new epsilon_s is not a chain in the old fixed physical complex. "
            "Cap/ridge are formally horizontal, but literal ridge grade and "
            "q on epsilon_s remain undefined until that comparison exists."
        ),
        "shortest_positive_theorem": (
            "map the universal relative KS generator epsilon_s, equivariantly "
            "over the endpoint/D4 action groupoid, into the complete physical "
            "AugP2/E14 complex.  Require its image to carry the existing flat "
            "cap graph and shifted ridge.  Then endpoint B-polynomial faces "
            "and D4 target correction are automatic; physical q closes by "
            "the established defect-versus-generator alternative."
        ),
        "scope": (
            "canonical h=3 characteristic-zero response occurrence module, "
            "endpoint action groupoid, and four-root E14 orbit.  The universal "
            "KS and formal orbit-relative statements are exact.  No fixed-"
            "physical comparison, literal cap/ridge grade map, q extension, "
            "or terminal promotion is constructed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("R_s derivative modulo R: -c_f (CANONICAL RELATIVE KS)")
    print("89-parameter centered family: A/B-EQUIVARIANT")
    print("D4 moving-target tensor: FORMALLY FLAT, c_f -> c_g")
    print("fixed physical comparison: OPEN AT epsilon_s -> AugP2/E14")
    print("cap/ridge horizontal: FORMAL YES; LITERAL GRADE OPEN")
    print("physical q on epsilon_s: UNTYPED; DEFECT ALTERNATIVE AFTER COMPARISON")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
