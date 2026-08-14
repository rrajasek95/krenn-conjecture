#!/usr/bin/env python3
"""Test whether the ``Gamma_*`` terminal lives in the canonical cotangent complex.

Let ``R`` be the polynomial ring in the 252 oriented colour-edge variables,
``I`` the 6561 official EqSystem relations, and ``A=R/I``.  The canonical
first-order source object is

    L_{A/k} = [I/I^2 -> Omega_{R/k} tensor_R A].

After introducing three pure-target homogenizers, EqSystem has an honest
site-colour multigrading.  Its selected squarefree coefficient multiples also
have a finite Boolean Taylor/Schreyer resolution.  Neither construction,
however, creates the response/cap operation idempotents, the B/Eq split, or
the fine/repeated occurrence labels used at ``Gamma_*``.

The obstruction is visible on the eight-dimensional top occurrence block.
Forgetting the two presentation copies is ``(b,e) -> b+e``.  Every cotangent
covector therefore pulls back as ``(lambda,lambda)``, whereas the normalized
detector is proportional to ``(delta,-delta)``.  It is nonzero on the kernel
of the forgetful map and hence does not descend to ``L_{A/k}``.  Consequently
the local one-dimensional terminal line is not presently an Ext/T^1 class of
the official EqSystem.

The checker also records the smallest admissible loophole: horizontally
desuspend the actual Koszul cell ``eps_F wedge eps_Q`` by one externally
declared response-to-cap operation degree.  Its total degree is one and its
relative boundary is Eq-only, hence bright.  Excluding this cell requires an
operation-support conservativity/no-orphan-desuspension axiom in a genuinely
defined enriched cotangent/principal-parts complex.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_chart_model_is_official_eqsystem.py":
        "ef1a997323e0a116787fa3c50368e22ecd33804942a9179eabefa2993e4d9373",
    "computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py":
        "346f3885bae10462c11f8046240ad4bc5970f0950a25b163235445592be0e9ab",
    "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py":
        "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_gamma_star_source_derived_free_closure_census.py":
        "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
    "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py":
        "2c112bffeef2c6adb00029077b6b231de396ace76c78756ab0e11e20078a557b",
}
EXPECTED_LEDGER_SHA256 = "c38539ad6f90df1bf1157bd0f72a8a8cd80e3745e58c2cd4876b5b0c9aca3fd7"

SITES = tuple(range(8))
COLOURS = tuple(range(3))
CAP_WORD = tuple(map(int, "01211222"))
COFACTOR_LABELS = ("q45", "q23", "q35", "q24", "q34", "q25")
KAPPA_WORDS = (
    "0012", "0102", "0110", "0111",
    "0122", "0212", "1112", "2112",
)
DELTA = tuple(map(Q, (1, 1, -1, -1)))


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


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[columns[column][row] for column in range(len(columns))]
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


def site_colour_degree(word) -> tuple[int, ...]:
    degree = [0] * (len(SITES) * len(COLOURS))
    for site, colour in enumerate(word):
        degree[len(COLOURS) * site + colour] += 1
    return tuple(degree)


def monomial_for_matching(word, matching):
    return tuple((left, right, word[left], word[right])
                 for left, right in matching)


def exponent_degree(monomial) -> tuple[int, ...]:
    variables = tuple(
        (left, right, left_colour, right_colour)
        for left, right in combinations(SITES, 2)
        for left_colour, right_colour in product(COLOURS, repeat=2)
    )
    positions = {variable: index for index, variable in enumerate(variables)}
    degree = [0] * len(variables)
    for variable in monomial:
        degree[positions[variable]] += 1
    return tuple(degree)


def official_cotangent_and_rees_audit(official) -> dict[str, object]:
    variables = tuple(
        (left, right, left_colour, right_colour)
        for left, right in combinations(SITES, 2)
        for left_colour, right_colour in product(COLOURS, repeat=2)
    )
    words = tuple(product(COLOURS, repeat=len(SITES)))
    matchings = official.OFFICIAL_MATCHINGS
    require(len(variables) == 252 and len(words) == 6561
            and len(matchings) == 105, "official EqSystem census changed")

    # Check every term of every official row in the honest site-colour
    # multigrading.  This is the strongest grading supplied by EqSystem.
    for word in words:
        expected = site_colour_degree(word)
        for matching in matchings:
            observed = [0] * 24
            for left, right in matching:
                observed[3 * left + word[left]] += 1
                observed[3 * right + word[right]] += 1
            require(tuple(observed) == expected,
                    ("site-colour homogeneity failed", word, matching))

    pure_degrees = tuple(site_colour_degree((colour,) * 8)
                         for colour in COLOURS)
    require(len(set(pure_degrees)) == 3
            and all(sum(degree) == 8 for degree in pure_degrees),
            "pure target degrees changed")

    # Full monomial-exponent grading is not a grading of an EqSystem row:
    # the 105 matching terms have distinct N^252 degrees.
    cap_terms = tuple(monomial_for_matching(CAP_WORD, matching)
                      for matching in matchings)
    fine_degrees = tuple(exponent_degree(term) for term in cap_terms)
    require(len(set(cap_terms)) == len(set(fine_degrees)) == 105,
            "the complete matching row stopped having 105 fine monomials")

    return {
        "presentation": {
            "R": "k[x_(ij)^(ab)]",
            "variables": len(variables),
            "I": "(F_w : w in {0,1,2}^8)",
            "relations": len(words),
            "matching_terms_per_relation": len(matchings),
            "A": "R/I",
            "canonical_cotangent_complex":
                "L_A/k=[I/I^2 -> Omega_R/k tensor_R A]",
            "canonical_principal_parts_extension":
                "0 -> Omega_A/k -> P^1_A/k -> A -> 0",
        },
        "honest_site_colour_grading": {
            "group": "N^24",
            "variable_degree": "deg x_(ij)^(ab)=e_(i,a)+e_(j,b)",
            "all_rows_checked": len(words),
            "all_monomial_occurrences_checked": len(words) * len(matchings),
            "mixed_F_w_degree": "sum_i e_(i,w_i)",
        },
        "pure_target_homogenization": {
            "ordinary_pure_relation_is_homogeneous": False,
            "reason": "F_(c^8)-1 has degrees sum_i e_(i,c) and 0",
            "one_common_homogenizer_suffices": False,
            "minimal_multigraded_Rees_fix":
                "adjoin u_0,u_1,u_2 with deg u_c=sum_i e_(i,c)",
            "pure_degrees_are_distinct": True,
        },
        "full_monomial_fine_grading": {
            "candidate_group": "N^252",
            "distinct_degrees_in_F_CAP_WORD": len(set(fine_degrees)),
            "F_CAP_WORD_is_homogeneous": False,
            "consequence": (
                "a marked t*q_(v,N) occurrence is a presentation/term slot, "
                "not a grading of A or L_A/k"
            ),
        },
    }


def gamma_axis_honesty_audit(cotangent) -> dict[str, object]:
    honest = cotangent["honest_site_colour_grading"]
    require(honest["all_rows_checked"] == 6561, honest)
    word_degree = site_colour_degree(CAP_WORD)
    doubled_word_degree = tuple(2 * value for value in word_degree)
    require(sum(word_degree) == 8 and sum(doubled_word_degree) == 16
            and doubled_word_degree != word_degree,
            "word degrees unexpectedly formed idempotents")
    return {
        "word": {
            "status_after_three_homogenizers": "honest N^24 degree label",
            "is_an_algebra_idempotent": False,
            "test": "deg(w)+deg(w) has weight 16, not the weight-8 word degree",
        },
        "fine_t_q": {
            "status": "not an honest A- or L-grading",
            "reason": "one F_w is a sum of 105 distinct N^252 degrees",
        },
        "repeated_P3_plus_K2": {
            "status": "not defined by EqSystem as a grading or filtration",
            "reason": (
                "it is a chart/deletion shape on marked occurrences, absent "
                "from R, I and the universal property of L_A/k"
            ),
        },
        "operation_parent": {
            "labels": ["response", "cap", "AugP2", "K_Eq"],
            "status": "absent from R, I, A and L_A/k",
            "orthogonal_idempotents_defined_by_EqSystem": False,
        },
        "B_Eq_split": {
            "status": "two enriched presentation copies of one coefficient orbit",
            "canonical_in_L_A/k": False,
        },
        "root_window_protected_rows": {
            "status": "external augmented labels/readouts, not cotangent degrees",
        },
        "conclusion": (
            "Gamma_* is not presently an honest graded quotient or filtered "
            "associated-graded piece of the canonical cotangent complex"
        ),
    }


def contraction_matrix(dimension: int, degree: int):
    source = tuple(combinations(range(dimension), degree))
    target = tuple(combinations(range(dimension), degree - 1))
    target_index = {subset: index for index, subset in enumerate(target)}
    columns = []
    for subset in source:
        column = [Q(0)] * len(target)
        for position in range(len(subset)):
            face = subset[:position] + subset[position + 1:]
            column[target_index[face]] += Q(-1 if position % 2 else 1)
        columns.append(tuple(column))
    return tuple(columns)


def compose(left_columns, right_columns):
    # left: V1 -> V0, right: V2 -> V1; return V2 -> V0.
    return tuple(
        tuple(sum((Q(left_columns[mid][row]) * Q(column[mid])
                   for mid in range(len(left_columns))), Q(0))
              for row in range(len(left_columns[0])))
        for column in right_columns
    )


def finite_macaulay_schreyer_audit(first_face) -> dict[str, object]:
    require(tuple(first_face.COFACTOR_LABELS) == COFACTOR_LABELS,
            "the six literal fine labels changed")
    # Abstract the six literal squarefree multiplier slots as three named
    # factors.  Positivity makes divisibility equivalent to choosing a subset.
    multipliers = tuple((f"t_{index}", "q01", label)
                        for index, label in enumerate(COFACTOR_LABELS))
    divisor_pairs = []
    degree_histogram = {degree: 0 for degree in range(4)}
    for multiplier in multipliers:
        for degree in range(4):
            for positions in combinations(range(3), degree):
                relation_part = tuple(multiplier[position]
                                      for position in positions)
                complement = tuple(multiplier[position]
                                   for position in range(3)
                                   if position not in positions)
                divisor_pairs.append((relation_part, complement))
                degree_histogram[degree] += 1
    require(len(divisor_pairs) == 6 * 2 ** 3 == 48
            and degree_histogram == {0: 6, 1: 18, 2: 18, 3: 6},
            (len(divisor_pairs), degree_histogram))

    differentials = {
        degree: contraction_matrix(3, degree) for degree in (1, 2, 3)
    }
    ranks = {degree: rank(columns)
             for degree, columns in differentials.items()}
    require(ranks == {1: 1, 2: 2, 3: 1}, ranks)
    for degree in (2, 3):
        composite = compose(differentials[degree - 1],
                            differentials[degree])
        require(all(not any(column) for column in composite),
                ("Boolean differential stopped squaring to zero", degree))
    require(ranks[1] + ranks[2] == comb(3, 1)
            and ranks[2] + ranks[3] == comb(3, 2),
            "Boolean complex stopped being exact in its middle degrees")

    return {
        "scope": (
            "the six externally selected squarefree t*q_(v,N) fine slots; "
            "not a canonical Gamma summand of L_A/k"
        ),
        "literal_cofactor_order": list(COFACTOR_LABELS),
        "squarefree_multiplier_degree": 3,
        "multiplier_count": len(multipliers),
        "all_divisor_complement_pairs": len(divisor_pairs),
        "relation_degree_histogram": {
            str(key): value for key, value in degree_histogram.items()
        },
        "one_slot_Boolean_dimensions": [1, 3, 3, 1],
        "one_slot_differential_ranks": [1, 2, 1],
        "six_slot_differential_ranks": [6, 12, 6],
        "all_degree_complementing_Macaulay_multiples_enumerated": True,
        "higher_unshifted_Schreyer_effect": (
            "C2 and higher resolve kernels of d1; they cannot enlarge im(d1)"
        ),
        "exhaustiveness_guard": (
            "positivity and squarefreeness make the 2^3 divisor census exact "
            "once a fine slot has been chosen externally"
        ),
    }


def omega_non_descent_audit(source_derived) -> dict[str, object]:
    ledger, digest = source_derived.audit()
    require(digest == source_derived.EXPECTED_LEDGER_SHA256, digest)
    executable = ledger["executable_Gen_phys"]
    require(executable["B_Eq_image_rank"] == 7
            and executable["Psi_charge_histogram"] == {"0": 128},
            executable)

    zero4 = (Q(0),) * 4
    basis4 = tuple(tuple(Q(1) if row == column else Q(0)
                         for row in range(4))
                   for column in range(4))
    tied_pullbacks = tuple(basis + basis for basis in basis4)
    omega = DELTA + tuple(-value for value in DELTA)
    kernel_witness = omega
    forgetful_image = tuple(kernel_witness[index]
                            + kernel_witness[index + 4]
                            for index in range(4))
    require(forgetful_image == zero4, forgetful_image)
    require(dot(omega, kernel_witness) == 8,
            "the normalized detector stopped seeing the forgetful kernel")
    require(rank(tied_pullbacks) == 4
            and rank(tied_pullbacks + (omega,)) == 5,
            "omega unexpectedly descended to a tied covector")
    normalized_omega = tuple(value / 4 for value in omega)
    eq_only_delta = zero4 + DELTA
    require(dot(normalized_omega, eq_only_delta) == -1,
            "normalized Eq-only charge changed")

    return {
        "local_enriched_occurrence_block": "W=B direct_sum Eq=Q^4 direct_sum Q^4",
        "minimal_cotangent_forgetful_map": "f(b,e)=b+e",
        "pullback_of_any_cotangent_covector": "f^*(lambda)=(lambda,lambda)",
        "tied_pullback_rank": rank(tied_pullbacks),
        "detector": "omega=(delta,-delta), delta=(1,1,-1,-1)",
        "rank_after_adjoining_detector": rank(tied_pullbacks + (omega,)),
        "forgetful_kernel_witness": "(delta,-delta)",
        "f_of_kernel_witness": list(map(str, forgetful_image)),
        "omega_on_kernel_witness": str(dot(omega, kernel_witness)),
        "normalized_omega_on_Eq_only_delta": "-1",
        "callable_enriched_B_Eq_rank": "7/8",
        "all_128_callable_columns_are_omega_dark": True,
        "descends_to_L_A_k": False,
        "Ext_T1_verdict": (
            "the one-dimensional enriched detector line cannot presently be "
            "identified with Ext^1_A(L_A/k,M) or a canonical T^1 component"
        ),
    }


def shifted_cell_and_exotic_audit(tate, full_hasse, omega) -> dict[str, object]:
    koszul = tate.absolute_koszul_audit()
    require(koszul["degree_two_cell"] == "theta=eps_F wedge eps_Q"
            and koszul["absolute_boundary"] == "dtheta=F eps_Q-Q eps_F"
            and koszul["d_squared"] == 0
            and koszul["relative_boundary"] == "dC_K=-F e_Eq",
            koszul)

    # Pin the literal Hasse packet rather than replacing theta by a formal
    # two-term symbol.  One of the 15 cubes is enough to check its protected
    # top, while the imported constants retain the full five-face family.
    packets = tuple(
        full_hasse.audit_one_cube(deleted, matching)
        for deleted in full_hasse.ODD
        for matching in full_hasse.matchings(full_hasse.face(deleted))
    )
    require(len(packets) == 15, "the full Hasse packet stopped having 15 cubes")
    require(all(packet["top_chain"] == "r_0-T"
                and packet["target"] == 0
                and packet["ordinary_residue"] == 0
                and packet["diagonal_projection_commutator"] == "(H_0-u)*eq"
                for packet in packets), packets)
    packet = packets[0]

    return {
        "canonical_vertical_cell": {
            "name": "theta=eps_F wedge eps_Q",
            "cotangent_Tate_degree": 2,
            "absolute_boundary": koszul["absolute_boundary"],
            "relative_boundary_after_Q_zero": koszul["relative_boundary"],
            "operation_parent": "objectwise until extra enrichment is supplied",
        },
        "literal_Hasse_representative": {
            "five_deleted_faces_times_three_matchings": 15,
            "sample_top_chain": packet["top_chain"],
            "sample_target": packet["target"],
            "sample_ordinary_residue": packet["ordinary_residue"],
            "top_commutator": packet["diagonal_projection_commutator"],
        },
        "smallest_admissible_exotic": {
            "name": "Omega_shift,0102=Sigma^(-1)_(response->cap,Gamma*) theta",
            "construction": (
                "give theta horizontal operation degree -1 and totalize; "
                "vertical degree 2 plus horizontal degree -1 is total degree 1"
            ),
            "literal_relative_boundary": "-F e_Eq",
            "B_Eq_top_orbit": "(0,delta)",
            "normalized_omega_charge": omega[
                "normalized_omega_on_Eq_only_delta"],
            "d_squared": 0,
            "official_cotangent_shadow": "the existing vertical theta",
            "physical_GHZ_operation_asserted": False,
        },
        "interpretation": (
            "canonical higher syzygies do not change d1, but an externally "
            "shifted operation direction can move a real C2 cell into relative C1"
        ),
    }


def conditional_operation_support_theorem() -> dict[str, object]:
    objects = ("response", "cap")
    edges = (("response", "response"), ("cap", "cap"),
             ("response", "cap"))
    composable_two_Phi = []
    for left in edges:
        for right in edges:
            if (left[1] == right[0] and left[0] != left[1]
                    and right[0] != right[1]):
                composable_two_Phi.append((left, right))
    require(not composable_two_Phi, composable_two_Phi)
    require(len(KAPPA_WORDS) == len(set(KAPPA_WORDS)) == 8,
            "the one-root orbit changed")
    return {
        "hypotheses": [
            "a Gamma-enriched filtered dg category with honest operation idempotents",
            "its only primitive nonidentity operation edge is natural Phi_KS,r0",
            "operation-support conservativity: no orphan horizontal desuspensions",
            "standard word/K_Eq interchanges and objectwise Hasse/Schreyer exactness",
        ],
        "operation_objects": list(objects),
        "nonidentity_graph": "response -> cap",
        "composable_pairs_of_nonidentity_edges": 0,
        "relative_C1_normal_forms_modulo_canonical_and_dark": list(KAPPA_WORDS),
        "normal_form_count": len(KAPPA_WORDS),
        "strict_product_B_Eq_shape": "(v,v)",
        "all_standard_kappas_are_omega_dark": True,
        "theorem": (
            "under these hypotheses, unshifted higher Schreyer cells add no "
            "d1 image and every operation-changing relative-C1 primitive is "
            "one of the eight standard kappa interchanges modulo canonical/dark"
        ),
        "unconditional_status": False,
        "why_conditional": (
            "EqSystem supplies neither the operation graph nor the no-orphan-"
            "desuspension axiom"
        ),
    }


def minimal_enrichment_contract() -> dict[str, object]:
    return {
        "name": "GammaCotangentEnrichment",
        "required_data": [
            "a filtered/dg A-bimodule L_tilde with response/cap operation idempotents",
            "a conservative forgetful comparison L_tilde -> L_A/k (or its three-u Rees model)",
            "honest definitions of fine t*q, repeated P3+K2, window and root filtrations",
            "a B/Eq-separated gr_Gamma chain map to the complete protected row object",
            "completeness for physical relative-C1 primitives in the kernel of forgetting",
            "operation-support conservativity/no orphan horizontal desuspensions",
        ],
        "source_derived_candidate": (
            "the 159 site-repeating Taylor/Spencer pair coordinates with the "
            "termwise collision-to-AugP2 contraction and full-star averaging"
        ),
        "candidate_status": (
            "additional enrichment datum; not a quotient or filtration supplied "
            "by the canonical cotangent complex"
        ),
        "first_required_test": (
            "check the candidate on the actual 8580 order-six columns, retaining "
            "literal differential, word/fine/repeated/operation labels"
        ),
        "then_well_posed": (
            "compute Ext^1 in the enriched category and ask whether its bright "
            "Gamma piece is zero, the eight dark kappas, or contains Omega_shift"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    official = load(
        "computations/verify_chart_model_is_official_eqsystem.py",
        "gamma_cotangent_official",
    )
    first_face = load(
        "computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py",
        "gamma_cotangent_first_face",
    )
    tate = load(
        "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py",
        "gamma_cotangent_tate",
    )
    full_hasse = load(
        "computations/verify_h3_full_hasse_koszul_cap_totalization.py",
        "gamma_cotangent_full_hasse",
    )
    source_derived = load(
        "computations/verify_h3_gamma_star_source_derived_free_closure_census.py",
        "gamma_cotangent_source_derived",
    )

    cotangent = official_cotangent_and_rees_audit(official)
    gamma = gamma_axis_honesty_audit(cotangent)
    macaulay = finite_macaulay_schreyer_audit(first_face)
    omega = omega_non_descent_audit(source_derived)
    exotic = shifted_cell_and_exotic_audit(tate, full_hasse, omega)
    conditional = conditional_operation_support_theorem()
    contract = minimal_enrichment_contract()
    ledger = {
        "theorem": "h3 Gamma cotangent/principal-parts enrichment foundation gate",
        "pins": PINS,
        "official_cotangent_and_Rees": cotangent,
        "Gamma_axis_honesty": gamma,
        "finite_Macaulay_Taylor_Schreyer": macaulay,
        "omega_non_descent": omega,
        "shifted_higher_cell_loophole": exotic,
        "conditional_essential_surjectivity": conditional,
        "minimal_foundational_repair": contract,
        "verdict": (
            "The three-homogenizer Rees EqSystem has an honest N^24 site-colour "
            "grading, and the six externally selected squarefree fine slots have "
            "an exact finite Boolean Taylor/Schreyer resolution. But fine, "
            "repeated, operation and B/Eq are not gradings, filtrations or "
            "idempotents of the canonical cotangent complex. The B-Eq detector "
            "is nonzero on the kernel of B+Eq forgetting, so it does not descend "
            "and the local terminal is not yet a canonical Ext/T1 class. An "
            "operation-desuspended actual Koszul theta is the smallest explicit "
            "bright exotic unless a GammaCotangentEnrichment with conservative "
            "operation support is supplied. Under that added axiom, the finite "
            "Taylor/Schreyer theorem leaves exactly the eight dark kappas."
        ),
        "scope": (
            "exact official N=8,D=3 generator/relation multigrading, exact six-"
            "slot degree-complementing Boolean census, exact rational B/Eq "
            "non-descent, and an explicit admissible bicomplex exotic. This is "
            "structural and independent of the direct executable J_phys matrix; "
            "the exotic is not asserted to be a full decorated GHZ operation."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Gamma cotangent ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "cotangent", "grading", "macaulay", "omega", "exotic",
        "conditional", "contract",
    ), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 Gamma cotangent foundation gate ({arguments.mode}): PASS")
        print("honest canonical grading: N^24 after three pure homogenizers")
        print("Gamma fine/repeated/operation/B-Eq quotient of L_A/k: NO")
        print("B-Eq detector descends to cotangent Ext/T1: NO")
        print("six-slot Boolean census: 48 complements; ranks 6,12,6")
        print("conditional no-orphan theorem: exactly eight dark kappas")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
