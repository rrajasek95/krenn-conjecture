#!/usr/bin/env python3
"""Compare endpoint-triangle residual flips with the A+I matching face."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_endpoint_correspondence_square_triangle_holonomy_gate.py":
        "8709a1a8ee50de543d01969c6c1fe657c2b53c934aa8be88cc7aa58e4a92fadd",
    "notes/h3-endpoint-correspondence-square-triangle-holonomy-gate.md":
        "4862304a66b38d9b7570253ae7e8aff06a479553b128fd4f998e50818cdf6a07",
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "notes/h3-e14-selected-fibre-graph-keq-koszul-gate.md":
        "98cae28b58267abcffc47b571e52581a354950ef684df5f28b58dca88c60c6e7",
    "computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py":
        "80c9e21304bb679292671c1f344a154d4ae102c1219c4c7e1f3aad9c948be7ac",
    "notes/h3-endpoint-projector-post-bminus4-target-rank-gate.md":
        "62cba9a83f0fba0e74f1274d4dea8968d31bdd45b96cf80b2e862e0107018fab",
}
EXPECTED_LEDGER_SHA256 = (
    "81e1af78ed28743afb896e72ff7d96943318a0d978b9358709751823731e5288"
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
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * value for value in vector)


def rank(vectors) -> int:
    basis = {}
    for original in vectors:
        values = [Q(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [left - coefficient * right for left, right in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def unit(index: int, size: int):
    return tuple(Q(position == index) for position in range(size))


def edge(left: int, right: int):
    return tuple(sorted((left, right)))


def permute_edge(value, permutation):
    return edge(permutation.get(value[0], value[0]),
                permutation.get(value[1], value[1]))


def coefficient_matching_audit() -> dict[str, object]:
    matchings = (
        ((2, 3), (4, 5)),
        ((2, 4), (3, 5)),
        ((2, 5), (3, 4)),
    )
    matchings = tuple(tuple(sorted(matching)) for matching in matchings)
    lookup = {matching: index for index, matching in enumerate(matchings)}

    def action(permutation, vector):
        answer = [Q(0)] * 3
        for index, coefficient in enumerate(vector):
            image = tuple(sorted(permute_edge(value, permutation)
                                 for value in matchings[index]))
            answer[lookup[image]] += coefficient
        return tuple(answer)

    tau23 = {2: 3, 3: 2}
    tau45 = {4: 5, 5: 4}
    e0, e1, e2 = (unit(index, 3) for index in range(3))
    b01 = add(e0, e1, e2)
    require(action(tau23, e0) == action(tau45, e0) == e0
            and action(tau23, e1) == action(tau45, e1) == e2
            and action(tau23, e2) == action(tau45, e2) == e1
            and action(tau23, b01) == action(tau45, b01) == b01,
            "the residual-flip action on matching coefficients changed")

    # A is adjacency on the three perfect matchings, so A+I=J3.  Its image
    # is the invariant line.  The residual flip boundary has the independent
    # standard direction e2-e1.
    matching_face = b01
    isotropy_direction = add(e2, scale(-1, e1))
    require(add(action(tau23, isotropy_direction),
                scale(-1, isotropy_direction))
                == scale(-2, isotropy_direction),
            "the flip standard eigenline changed")
    # M=A+I is the all-ones operator.  It kills the image of tau-I on both
    # sides, so the interaction is semidirect rather than identification.
    def matching_projection(vector):
        return scale(sum(vector, Q(0)), b01)

    for basis in (e0, e1, e2):
        flip_boundary = add(action(tau23, basis), scale(-1, basis))
        require(matching_projection(flip_boundary) == (Q(0),) * 3
                and add(action(tau23, matching_projection(basis)),
                        scale(-1, matching_projection(basis)))
                    == (Q(0),) * 3,
                "(A+I)(tau-I) or (tau-I)(A+I) changed")
    require(rank((matching_face,)) == 1
            and rank((matching_face, isotropy_direction)) == 2,
            "the invariant/flip matching splitting changed")
    return {
        "matching_basis": ["23|45", "24|35", "25|34"],
        "A_plus_I": "J_3",
        "A_plus_I_image": "span(1,1,1)",
        "tau23_on_matching_basis": [0, 2, 1],
        "tau45_on_matching_basis": [0, 2, 1],
        "marked_matching_fixed": True,
        "selected_fibre_b01_fixed": True,
        "isotropy_standard_direction": [0, -1, 1],
        "operator_relation": (
            "(A+I)(tau-I)=(tau-I)(A+I)=0 for tau=tau23,tau45"
        ),
        "tau_is_polynomial_in_A": False,
        "reason_not_polynomial": (
            "A acts as the scalar -1 on the two-dimensional standard "
            "matching module, whereas tau has +1 and -1 eigenlines there"
        ),
        "rank_matching_face_then_isotropy": [1, 2],
        "conclusion": (
            "the triangle flips lie in the stabilizer of the marked "
            "matching and commute with A+I, but are not the A+I boundary"
        ),
    }


def centered_occurrence_audit() -> dict[str, object]:
    base = load(
        "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py",
        "matching_flip_centered_base",
    )
    occurrences = base.occurrences()
    lookup = {value: index for index, value in enumerate(occurrences)}
    marked_value = (0, 1, ((2, 3), (4, 5)))
    marked = lookup[marked_value]
    ones = (Q(1),) * 90

    def action(permutation, vector):
        answer = [Q(0)] * 90
        for index, coefficient in enumerate(vector):
            p_site, s_site, matching = occurrences[index]
            image = (
                permutation.get(p_site, p_site),
                permutation.get(s_site, s_site),
                tuple(sorted(permute_edge(value, permutation)
                             for value in matching)),
            )
            answer[lookup[image]] += coefficient
        return tuple(answer)

    e_f = unit(marked, 90)
    c_f = add(scale(90, e_f), scale(-1, ones))
    fibre01 = tuple(Q(value[0] == 0 and value[1] == 1)
                    for value in occurrences)
    c01 = add(scale(30, fibre01), scale(-1, ones))
    tau23 = {2: 3, 3: 2}
    tau45 = {4: 5, 5: 4}
    for permutation in (tau23, tau45):
        require(action(permutation, e_f) == e_f
                and action(permutation, c_f) == c_f
                and action(permutation, fibre01) == fibre01
                and action(permutation, c01) == c01,
                "a centered occurrence class lost flip invariance")

    matching_cf = add(base.apply_matching(c_f, occurrences, lookup), c_f)
    require(matching_cf == scale(3, c01),
            "(A+I)c_f=3c01 changed under the flip audit")
    return {
        "c_f": "90e_f-1_90",
        "c_01": "30b_01-1_90",
        "tau23_c_f_minus_c_f": 0,
        "tau45_c_f_minus_c_f": 0,
        "tau23_c01_minus_c01": 0,
        "tau45_c01_minus_c01": 0,
        "matching_identity": "(A+I)c_f=3c_01",
        "matching_identity_is_flip_equivariant": True,
        "isotropy_bar_boundary_on_centered_top": 0,
    }


def principal_parts_flip_audit() -> dict[str, object]:
    # Terms retain which factor is differentiated.  The first two are the
    # two derivatives of the fixed matching, followed by the four cross
    # matching terms.
    terms = (
        ((2, 3), (4, 5)),
        ((4, 5), (2, 3)),
        ((2, 4), (3, 5)),
        ((3, 5), (2, 4)),
        ((2, 5), (3, 4)),
        ((3, 4), (2, 5)),
    )
    lookup = {term: index for index, term in enumerate(terms)}

    def permutation_on_terms(permutation):
        return tuple(lookup[(permute_edge(differentiated, permutation),
                             permute_edge(plain, permutation))]
                     for differentiated, plain in terms)

    def action(term_permutation, vector):
        answer = [Q(0)] * 6
        for index, coefficient in enumerate(vector):
            answer[term_permutation[index]] += coefficient
        return tuple(answer)

    tau23 = permutation_on_terms({2: 3, 3: 2})
    tau45 = permutation_on_terms({4: 5, 5: 4})
    require(tau23 == (0, 1, 5, 4, 3, 2)
            and tau45 == (0, 1, 4, 5, 2, 3),
            ("the PP residual-flip permutations changed", tau23, tau45))
    face = (Q(1),) * 6
    require(action(tau23, face) == action(tau45, face) == face,
            "the six-term matching face lost flip invariance")

    boundary_vectors = []
    for term_permutation in (tau23, tau45):
        for index in range(6):
            boundary_vectors.append(add(
                action(term_permutation, unit(index, 6)),
                scale(-1, unit(index, 6)),
            ))
    require(rank(tuple(boundary_vectors)) == 3
            and rank((face,) + tuple(boundary_vectors)) == 4,
            "the PP invariant/isotropy ranks changed")
    return {
        "PP_term_order": [
            "dq23*q45", "q23*dq45", "dq24*q35",
            "q24*dq35", "dq25*q34", "q25*dq34",
        ],
        "tau23_permutation": list(tau23),
        "tau45_permutation": list(tau45),
        "six_term_db01_fixed_by_both_flips": True,
        "six_term_bar_boundary": 0,
        "rank_of_termwise_flip_boundaries": 3,
        "rank_after_six_term_invariant_face": 4,
        "primitive_examples": [
            "q25*dq34-dq24*q35",
            "dq25*q34-dq24*q35",
        ],
        "conclusion": (
            "the aggregate matching PP face is an invariant vector.  The "
            "triangle isotropy lives in the independent three-dimensional "
            "standard module of the four cross terms; obtaining it requires "
            "termwise/occurrence-local PP bars, not merely db_01."
        ),
    }


def normalized_v4_bar_contraction_audit() -> dict[str, object]:
    # Restrict to the four cross terms (indices 2,3,4,5).  The two residual
    # flips generate the regular V4 action.  Its augmentation-zero module is
    # the direct sum of the three nontrivial rational character lines.
    tau23 = (3, 2, 1, 0)
    tau45 = (2, 3, 0, 1)

    def act(permutation, vector):
        answer = [Q(0)] * 4
        for index, coefficient in enumerate(vector):
            answer[permutation[index]] += coefficient
        return tuple(answer)

    characters = (
        (Q(1), Q(-1), Q(-1), Q(1)),
        (Q(1), Q(-1), Q(1), Q(-1)),
        (Q(1), Q(1), Q(-1), Q(-1)),
    )
    eigenvalues = (
        (Q(1), Q(-1)),
        (Q(-1), Q(1)),
        (Q(-1), Q(-1)),
    )
    for vector, (e23, e45) in zip(characters, eigenvalues, strict=True):
        require(act(tau23, vector) == scale(e23, vector)
                and act(tau45, vector) == scale(e45, vector),
                "the V4 PP character splitting changed")
    require(rank(characters) == 3
            and all(sum(vector, Q(0)) == 0 for vector in characters),
            "the V4 standard character basis changed")

    # On a -1 character, d[tau|y]=(tau-1)y=-2y.  Hence the normalized
    # contracting homotopy is h(y)=-1/2[tau|y].
    chosen = (tau45, tau23, tau23)
    chosen_names = ("tau45", "tau23", "tau23")
    for vector, permutation in zip(characters, chosen, strict=True):
        boundary = add(act(permutation, vector), scale(-1, vector))
        require(scale(Q(-1, 2), boundary) == vector,
                "the normalized C2 bar contraction changed")

    embedded = tuple((Q(0), Q(0)) + vector for vector in characters)
    aggregate = (Q(1),) * 6
    require(rank(embedded) == 3
            and rank((aggregate,) + embedded) == 4,
            "the normalized bar/invariant splitting changed")
    return {
        "residual_isotropy_group_on_cross_terms": "V4=<tau23,tau45>",
        "cross_term_character_basis": [
            [str(value) for value in vector] for vector in characters
        ],
        "character_eigenvalues_tau23_tau45": [
            [str(left), str(right)] for left, right in eigenvalues
        ],
        "chosen_C2_contractions": list(chosen_names),
        "normalized_homotopy": "h(y)=-1/2[tau|y]",
        "boundary_identity": "d h(y)=y on each nontrivial character line",
        "characteristic_requirement": "2 invertible (valid over Q[beta])",
        "standard_PP_module_contractible": True,
        "aggregate_db01_contracted": False,
        "conditional_source_hypothesis": (
            "the pointed centered response section is termwise PP-natural "
            "under the literal residual site flips, so [tau|y] is a physical "
            "source bar with transported fine labels"
        ),
        "aggregate_matching_column_implies_hypothesis": False,
        "augmented_rows_of_normalized_bars": {
            "GHZ_target": 0,
            "central_Eq_incidence": 0,
            "marked_anchor_and_centered_top": 0,
            "aggregate_six_term_q": 0,
            "ordinary_coefficient_augmentation": 0,
            "fine_grade": (
                "an orbit-labelled PP bar, not a column in one frozen "
                "individual dq-edge label"
            ),
        },
    }


def physical_typing_and_semidirect_scope() -> dict[str, object]:
    holonomy = load(
        "computations/verify_h3_endpoint_correspondence_square_triangle_holonomy_gate.py",
        "matching_flip_holonomy_dependency",
    )
    ledger, digest = holonomy.audit()
    require(digest == holonomy.EXPECTED_LEDGER_SHA256,
            "the endpoint holonomy ledger changed")
    triangles = ledger["three_step_holonomy"]
    require(triangles["marked_triangle_23"]["on_GHZ_Delta"] == "identity"
            and triangles["marked_triangle_45"]["on_GHZ_Delta"] == "identity",
            "a triangle flip acquired GHZ target normal")
    return {
        "coefficient_and_PP_head_word": "11:110000",
        "matching_decorations": "q23:00*q45:00 and its three K4 matchings",
        "matching_PP_face": "six dq-labelled terms in the same response word",
        "triangle_flip_target_readout": 0,
        "triangle_flip_central_Eq_incidence": 0,
        "triangle_flip_on_marked_anchor_and_c_f": 0,
        "triangle_flip_on_aggregate_six_term_physical_q_face": 0,
        "nonzero_row": (
            "mixed word/path-labelled PP standard module, e.g. "
            "X_000100-X_001000"
        ),
        "cap_and_repeated_grade": (
            "no construction: response word 110000 does not provide an "
            "isotropy bar in cap word 01211222 / t*q_(v,N) / P3+K2"
        ),
        "E14_word_transport": (
            "no construction: the aggregate matching face does not itself "
            "transport the bar to G11[111111] or unary word 000101"
        ),
        "semidirect_positive_statement": (
            "a full occurrence-local matching PP object with the residual-"
            "flip action extends to a semidirect endpoint/matching action-"
            "groupoid nerve; its isotropy bars are canonical faces"
        ),
        "current_matching_face_alone_supplies_that_object": False,
        "source_cell_count": (
            "the isotropy bar is independent of the aggregate db_01 column, "
            "although one coherent higher semidirect totalization may package "
            "both rather than treating them as separate conjecture theorems"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 matching face / residual-flip semidirect gate",
        "pins": PINS,
        "matching_coefficients": coefficient_matching_audit(),
        "centered_occurrence": centered_occurrence_audit(),
        "principal_parts": principal_parts_flip_audit(),
        "normalized_V4_bar_contraction": (
            normalized_v4_bar_contraction_audit()
        ),
        "physical_typing_and_semidirect_scope": (
            physical_typing_and_semidirect_scope()
        ),
        "verdict": (
            "The endpoint-triangle holonomies (2 3),(4 5) are stabilizers of "
            "the marked matching.  They fix c_f, c_01, b_01, and the aggregate "
            "six-term db_01 face, and commute with A+I.  Therefore adding the "
            "required matching PP face does not itself fill triangle "
            "isotropy: its bar boundary is zero.  On the six individual PP "
            "terms the flips generate a rank-three standard module, disjoint "
            "from the invariant matching face.  A termwise occurrence-local "
            "isotropy bar is an additional source face relative to the "
            "aggregate column.  Over Q[beta] its standard module is "
            "canonically contracted by normalized C2 bars once the pointed "
            "section is termwise flip-equivariant; under that stronger "
            "source-natural hypothesis it is not a new independent input."
        ),
        "scope": (
            "exact h=3 coefficient, centered-occurrence, first-PP, target, "
            "anchor and Eq-incidence audit.  It does not construct the "
            "termwise physical PP bar or its cap/E14 grade transport."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256, ("ledger", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("residual flips fix c_f,c_01,b_01,db_01: YES")
    print("A+I matching face closes triangle isotropy: NO")
    print("termwise PP isotropy rank:",
          ledger["principal_parts"]["rank_of_termwise_flip_boundaries"])
    print("semidirect totalization can package both: CONDITIONAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
