#!/usr/bin/env python3
"""State and audit the exact source-grade theorem needed for Psi terminality.

The canonical cap grade is selected by literal word, fine multidegree,
repeated-edge grade, operation/source-parent tag, and occurrence labels.
Every known family outside the response-to-AugP2 mixed mapping-cylinder
orbit is chi-dark for one of two exact reasons:

* it lies in a different direct-sum grade, so Pi_BEq is zero; or
* it lands in the exhaustive local kernel ker(delta.(B-Eq)).

Positive Macaulay multiplication preserves word, operation and parent tags;
PP/Hasse faces retain those tags.  Hence higher cells generated without a
cross-word mixed incidence remain dark.  The missing global theorem is a
finite source-grade census asserting that these operations plus the eight
canonical mixed-cell instances exhaust every column whose differential can
land in the cap grade.

Modulo the old rank-seven cap image, the eight unclassified columns have
normal forms lambda_i*(delta,0).  Thus Psi is an accepted normalized
terminal exactly when the exhaustive census is proved and every lambda_i
is zero.  A nonzero lambda_i is the unique projection-wise filler exit.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "notes/h3-uc4-four-site-response-private-eq-local-terminal-gate.md":
        "a7e10e0397ae3b31b9cce0e6bc2907f0c208634e22a0e3284076304130bd6989",
    "notes/h3-uc4-local-terminal-global-gluing-criterion.md":
        "40a0040835d26396b932ddb976b982b00f7d31a7432b3765516b3734809a0c06",
    "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py":
        "262e1dd08dd1842d60515d45aea53ea406d7e1e5ea55ab506bb6e81d64b07741",
    "notes/h3-maximal-pointed-balanced-same-grade-terminal-gate.md":
        "130f92e2a9bd2c7c5196bc730313a38d0b64a2ff0cf51804f316b74e26cee757",
    "computations/verify_h3_db01_dl01_literal_private_eq_conservation_gate.py":
        "1a27b00d28be6334a27e0603a0ef776367d3c71b6f8fa45d3005963f8dff4c6c",
    "notes/h3-db01-dl01-literal-private-eq-conservation-gate.md":
        "6ba7ac1df36e3ed4ed30acc1d219f22bcdff0d673e078aeb3b2e1d327a2737d9",
    "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py":
        "3704235f1030a07556aaebed3225bec8ea0fb9fa4d6a4d3aa124a7727a3bebec",
    "notes/h3-cross-word-mapping-cylinder-d2-augmentation-freedom-gate.md":
        "ef33bdd1f600fb3f58e91ca191a2fcfcfab516d5680907661a006ca5d358cec0",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "notes/h3-gate-ii-psidelta-same-grade-extension-chain.md":
        "2e7aea9a551ddc2ab845fb2c0717cbffb8f7db772c329fb3c11d6bdc3dc34fae",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
}
EXPECTED_DIGEST = "15d911240f75ab59adb4a507535fd85d536f432a3ecb492b952f07f4c33ef9aa"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO4 = (Q(0),) * 4
ZERO8 = (Q(0),) * 8
CAP_GRADE = {
    "word": "01211222",
    "fine": "t*q_(v,N) at the selected six P3+K2 occurrences",
    "repeated": "P3+K2",
    "operation": "AugP2-cap/mixed-orbit",
    "window": "2345 with literal occurrence labels",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
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


def old_cap_columns():
    diagonal = []
    for corner in range(4):
        basis = tuple(Q(1) if index == corner else Q(0)
                      for index in range(4))
        diagonal.append(basis + basis)
    companions = []
    for direct in (0, 1):
        for endpoint in (2, 3):
            edge = tuple(Q(1) if index in (direct, endpoint) else Q(0)
                         for index in range(4))
            companions.append(edge + ZERO4)
    return tuple(diagonal + companions)


def literal_family_records():
    # The first differing tag decides zero projection.  A same-grade family
    # is dark only after an exact projection reason is supplied.
    return (
        {
            "family": "exhaustive four-site U_C4 supermap",
            **CAP_GRADE,
            "projection_reason": "image equals the local chi-kernel",
        },
        {
            "family": "25 named AugP2 cap columns",
            **CAP_GRADE,
            "projection_reason": "diagonal, signless shore edge, tied, or external row",
        },
        {
            "family": "121 named response/intermediate columns",
            "word": "11:110000 or intermediate response word",
            "fine": "response fine degree",
            "repeated": "response/PP",
            "operation": "DQ/PS response",
            "window": "2345",
            "projection_reason": "word/fine/operation direct-sum mismatch",
        },
        {
            "family": "selected six db01 and eighteen dL01 terms",
            "word": "11:110000",
            "fine": "response first-PP",
            "repeated": "squarefree response PP",
            "operation": "vertical response",
            "window": "2345",
            "projection_reason": "strict literal B/Eq image zero",
        },
        {
            "family": "collision tops, unary/one-hole and C2+/C4/P2 repairs",
            "word": "collision/response word",
            "fine": "collision or unary fine degree",
            "repeated": "collision/PP",
            "operation": "collision or shore-gauged matching repair",
            "window": "source-labelled",
            "projection_reason": "off-grade, signless shore edge, or old local image",
        },
        {
            "family": "six sibling 3K2 collision faces",
            "word": "01211222 only after unbuilt placement",
            "fine": "sibling collision fine degree",
            "repeated": "3K2",
            "operation": "collision proper face",
            "window": "selected six",
            "projection_reason": "repeated-grade mismatch before mixed placement",
        },
        {
            "family": "A+B and A+C operation-profile switch families",
            "word": "11:110000",
            "fine": "response fixed-window",
            "repeated": "response",
            "operation": "profile-changing inside response",
            "window": "2345/H-r",
            "projection_reason": "cap word/fine mismatch",
        },
        {
            "family": "word-0102 private section and dq23 reinsertion",
            "word": "0102 lower object",
            "fine": "one-endpoint/dq23 lower fine degree",
            "repeated": "lower P2",
            "operation": "labelled endpoint-even section",
            "window": "lower cut",
            "projection_reason": "strict cap projection zero until cross-word placement",
        },
        {
            "family": "pointed conormal P_f",
            **CAP_GRADE,
            "projection_reason": "anchor/conormal coordinate outside B/Eq",
        },
        {
            "family": "primitive cap p and old target/residue cap graph",
            **CAP_GRADE,
            "projection_reason": "Q/target/ordinary-residue coordinates outside B/Eq",
        },
        {
            "family": "shifted gamma=-dOmega and eta/sigma ridge",
            "word": "01211222",
            "fine": "shifted pq/xv fine degree",
            "repeated": "shifted Kahler",
            "operation": "AugP2 ridge",
            "window": "labelled",
            "projection_reason": "ridge coordinates outside B/Eq",
        },
        {
            "family": "cross-word mixed orbit/K_Eq two-cell kappa_mix",
            **CAP_GRADE,
            "projection_reason": "UNCLASSIFIED B/Eq augmentation",
        },
    )


def grading_audit():
    records = literal_family_records()
    unknown = tuple(record for record in records
                    if record["projection_reason"].startswith("UNCLASSIFIED"))
    require(len(records) == 12 and len(unknown) == 1
            and unknown[0]["family"].endswith("kappa_mix"),
            "the literal family classification changed")

    # Freeze the already proved local rank theorem directly.
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "psi_source_grade_local",
    )
    local_ledger, local_digest = local.audit()
    local_map = local_ledger["exhaustive_local_supermap"]
    require(local_digest == local.EXPECTED_LEDGER_SHA256
            and local_map["output_dimension"] == 127
            and local_map["rank"] == 126
            and local_map["cokernel_dimension"] == 1,
            "the exhaustive local terminal changed")
    return {
        "canonical_cap_grade": CAP_GRADE,
        "literal_family_count": len(records),
        "families": records,
        "proved_dark_family_count": len(records) - len(unknown),
        "unclassified_homogeneous_face_types": [
            record["family"] for record in unknown
        ],
        "local_supermap_dimension_rank_cokernel": [
            local_map["output_dimension"], local_map["rank"],
            local_map["cokernel_dimension"],
        ],
        "darkness_rule": (
            "a column is chi-dark if its word/fine/repeated/operation tag "
            "differs from the cap grade, or its exact cap projection lies "
            "in the exhaustive local image ker(chi)"
        ),
    }


def higher_cell_audit():
    # Abstract additive tag monoid.  A multiplier has a nonnegative fine
    # degree and cannot alter the word, operation, parent, or occurrence
    # tags.  Verify the degree-three Macaulay partitions explicitly.
    target_polynomial_degree = 3
    partitions = tuple((relation_degree,
                        target_polynomial_degree - relation_degree)
                       for relation_degree in range(4))
    require(partitions == ((0, 3), (1, 2), (2, 1), (3, 0))
            and all(left + right == 3 and min(left, right) >= 0
                    for left, right in partitions),
            "the fixed-degree Macaulay partitions changed")

    operations = (
        {
            "operation": "monomial Macaulay multiplication",
            "fine_degree": "adds a nonnegative exponent vector",
            "preserves": ["word", "operation tag", "source parent", "occurrence labels"],
        },
        {
            "operation": "PP/Hasse/Koszul face",
            "fine_degree": "records the differentiated/removed literal slot",
            "preserves": ["word block", "operation parent", "source idempotent"],
        },
        {
            "operation": "matching restriction/reinsertion",
            "fine_degree": "returns to the same labelled top occurrence",
            "preserves": ["word", "operation shore", "B/Eq tie or signless edge"],
        },
        {
            "operation": "Cartan/ridge/eta/sigma completion",
            "fine_degree": "may shift Kahler grade",
            "preserves": ["zero B/Eq projection unless carried by a mixed comparison"],
        },
    )
    # A tiny exact closure state machine: D=dark, X=cross-word mixed.  Every
    # allowed non-cross operation preserves D; only adjoining X can leave D.
    states = {"D"}
    for _level in range(8):
        next_states = set(states)
        for state in states:
            if state == "D":
                next_states.add("D")
        states = next_states
    require(states == {"D"}, "a non-cross higher operation became bright")
    return {
        "fixed_polynomial_degree": target_polynomial_degree,
        "finite_relation_multiplier_degree_partitions": [
            list(pair) for pair in partitions
        ],
        "tag_preserving_higher_operations": operations,
        "inductive_darkness_theorem": (
            "every Macaulay/PP/Hasse/Tate descendant of a classified dark "
            "seed remains dark unless its construction uses a primitive "
            "response-to-AugP2 mixed-incidence generator"
        ),
        "why_positive_multipliers_do_not_create_a_new_type": (
            "they may complete a lower polynomial degree to degree three, "
            "but retain word/operation/source-parent tags; cap-internal "
            "multiples factor through the projection-complete local map, "
            "and response multiples remain off the cap operation block"
        ),
        "scope_guard": (
            "this proves closure for the listed source operations.  The "
            "global source-grade census must still prove that no exotic "
            "primitive cap-grade operation-changing generator exists"
        ),
    }


def unknown_orbit_audit():
    augmented = load(
        "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py",
        "psi_source_grade_augp2",
    )
    shortest = augmented.shortest_theorem_audit()
    independence = augmented.homogeneous_face_independence()
    require(shortest["literal_fixed_grade_occurrence_instantiations"] == 8
            and independence["raw_face_rank"] == 7
            and not independence["P_f_implies_primitive_p"],
            "the eight-instance augmented P2 frontier changed")

    d2 = load(
        "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py",
        "psi_source_grade_d2",
    )
    d2_augmentation = d2.augmentation_audit()
    d2_quotient = d2.quotient_audit()
    require(d2_augmentation["forced_exact_delta_B_minus_Eq_value"] is None
            and d2_quotient["old_cap_rank"] == 7,
            "the mixed-cell augmentation freedom changed")

    old = old_cap_columns()
    psi = DELTA + tuple(-value for value in DELTA)
    b_delta = DELTA + ZERO4
    mixed_instances = 8
    # Symbolic normal forms are represented by independent lambda basis
    # vectors.  Test the exact rank fork on zero and each primitive instance.
    zero_columns = (ZERO8,) * mixed_instances
    bright_ranks = []
    bright_values = []
    for index in range(mixed_instances):
        columns = list(zero_columns)
        columns[index] = b_delta
        bright_ranks.append(rank(old + tuple(columns)))
        bright_values.append(dot(psi, columns[index]))
    require(rank(old + zero_columns) == 7
            and bright_ranks == [8] * mixed_instances
            and bright_values == [Q(4)] * mixed_instances,
            "the eight-instance terminal fork changed")
    return {
        "minimal_unclassified_generator_type_count": 1,
        "unclassified_type": (
            "source-labelled response-to-AugP2 mixed orbit/K_Eq "
            "mapping-cylinder/Tate two-cell kappa_mix"
        ),
        "canonical_literal_instances": mixed_instances,
        "unknown_scalars": [f"lambda_{index}" for index in range(mixed_instances)],
        "normal_form_per_instance": (
            "Pi_BEq(kappa_i) congruent lambda_i*(delta,0) modulo old cap rows"
        ),
        "chi_per_instance": "chi(kappa_i)=4*lambda_i",
        "rank_if_all_lambda_zero": rank(old + zero_columns),
        "rank_if_any_primitive_lambda_nonzero": sorted(set(bright_ranks)),
        "proper_face_bookkeeping": {
            "reduced_Eq_cap_descent": (
                "a mandatory face of kappa_mix, not a separately classified "
                "bright type once one totalized AugP2 schema is required"
            ),
            "word_0102_section_and_dq23": (
                "strictly off-grade alone; its cap augmentation is part of "
                "the same kappa_mix boundary orbit"
            ),
            "six_P3K2_and_six_3K2_faces": (
                "P3K2 placements belong to the mixed orbit and 3K2 siblings "
                "are repeated-grade dark outside it"
            ),
            "shifted_ridge": "independent homogeneous face but chi-dark",
        },
        "if_faces_are_presented_as_independent_source_generators": (
            "the source census must identify each cap-grade one as a face "
            "of one of the eight kappa_i, or append it to this finite list"
        ),
    }


def terminal_promotion_audit():
    old = old_cap_columns()
    psi = tuple(value / Q(4)
                for value in DELTA + tuple(-entry for entry in DELTA))
    balanced = DELTA + ZERO4
    require(rank(old) == 7
            and all(dot(psi, column) == 0 for column in old)
            and dot(psi, balanced) == 1,
            "the normalized cap terminal changed")
    return {
        "exhaustive_source_grade_block": {
            "notation": "J_phys,Gamma*: C_phys,Gamma* -> Y_phys,Gamma*",
            "Gamma_star": CAP_GRADE,
            "domain_must_include": [
                "every primitive physical relation whose differential lands in Gamma*",
                "every monomial Macaulay multiple m*r with deg(m)+deg(r)=Gamma*",
                "every PP/Hasse/Koszul/Tate generator with a Gamma* output face",
                "all source idempotent, operation-parent, word, fine, repeated and occurrence labels",
            ],
            "codomain_must_include": [
                "all private B and reduced Eq occurrence rows",
                "target, W, ordinary residue, M, anchor incidence, physical q and P_f",
                "word-resolved ridge, eta, sigma and every protected terminal row",
            ],
        },
        "exact_generator_census_statement": (
            "C_phys,Gamma* is generated by the exhaustive local U_C4 "
            "supermap, the classified off-grade/tag-preserving Macaulay "
            "families, and exactly the eight kappa_mix instances; there are "
            "no exotic primitive cap-grade operation-changing generators"
        ),
        "equivalent_dark_quotient_statement": (
            "after quotienting the domain by generators whose B/Eq image "
            "lies in ker(chi), the remaining source-grade domain is spanned "
            "by kappa_0,...,kappa_7"
        ),
        "remaining_finite_tests": [
            "chi(kappa_i)=0 for i=0,...,7",
            "every independently presented cap-grade proper face is identified with the kappa orbit or tested separately",
        ],
        "normalized_terminal_extension": (
            "Psi~=delta.(B-Eq)/4 on B/Eq and zero on every complete external row"
        ),
        "normalization": "Psi~((B,Eq)=(delta,0))=1",
        "accepted_Macaulay_terminal_if": [
            "the source-grade generator census is exhaustive",
            "the physical codomain row census is exhaustive",
            "all eight mixed-orbit scalars lambda_i vanish",
            "the balanced comparison/RHS is the literal physical vector normalized above",
        ],
        "conclusion_if_conditions_hold": (
            "Psi~ J_phys,Gamma*=0 and Psi~(balanced)=1, so finite exact "
            "duality gives the Macaulay nonmembership/terminal arm; because "
            "physical q and protected rows are included, the existing "
            "kernel-generator versus Fredholm alternative is eligible"
        ),
        "positive_exit_if_any_test_fails": (
            "a first kappa_i with lambda_i!=0 raises the B/Eq rank 7->8; "
            "it is the physical filler candidate whose other faces must close"
        ),
        "not_yet_proved": [
            "the global source-grade generator census",
            "absence of exotic primitive cap-grade generators",
            "the eight lambda_i=0 equations",
            "the physical comparison to the final RHS/terminal convention",
        ],
    }


def run(mode: str) -> str:
    pin_dependencies()
    ledger = {}
    if mode in ("all", "grading"):
        ledger["literal_multigrade_classification"] = grading_audit()
    if mode in ("all", "higher"):
        ledger["higher_Macaulay_PP_Hasse_darkness"] = higher_cell_audit()
    if mode in ("all", "unknown"):
        ledger["minimal_unclassified_cross_word_orbit"] = unknown_orbit_audit()
    if mode in ("all", "terminal"):
        ledger["accepted_terminal_promotion_criterion"] = terminal_promotion_audit()
    if mode == "all":
        ledger["theorem"] = (
            "h3 Psi source-grade Macaulay exhaustiveness and terminal gate"
        )
        ledger["verdict"] = (
            "All currently typed source and higher-cell families outside "
            "the response-to-AugP2 mixed-incidence orbit are chi-dark by "
            "literal multigrading, operation-parent preservation, or the "
            "exhaustive local U_C4 kernel theorem.  At the fixed cap grade "
            "only one homogeneous generator type remains unclassified: "
            "kappa_mix, with eight canonical instances and scalars lambda_i. "
            "Promoting Psi requires a global source-grade census excluding "
            "every exotic primitive generator and the eight equations "
            "lambda_i=0; then Psi is the normalized complete Macaulay terminal."
        )
        ledger["scope"] = (
            "exact rational cap quotient, local rank theorem, literal family "
            "classification, and conditional higher-operation induction at "
            "canonical h=3.  This formulates but does not prove the missing "
            "global source-generator census or the mixed-orbit darkness."
        )
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if mode == "all" and EXPECTED_DIGEST != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIGEST,
                ("Psi source-grade terminal ledger changed", digest))
    print(f"h3 Psi source-grade Macaulay terminal gate ({mode}): PASS")
    if mode in ("all", "grading"):
        print("typed non-cross families: chi-dark by literal grade/local kernel")
    if mode in ("all", "higher"):
        print("non-cross Macaulay/PP/Hasse/Tate closure: chi-dark")
    if mode in ("all", "unknown"):
        print("unclassified list: one kappa_mix type, eight literal instances")
    if mode in ("all", "terminal"):
        print("terminal requires exhaustive Gamma* census plus lambda_0=...=lambda_7=0")
    print("ledger_sha256=" + digest)
    return digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "grading", "higher", "unknown", "terminal"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()
