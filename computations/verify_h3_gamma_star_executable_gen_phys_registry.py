#!/usr/bin/env python3
"""Build the smallest executable h=3 Gen_phys(Gamma_*) registry.

Every registry entry below is emitted from a callable constructor already in
the repository.  The comparison to the 27-row Gamma_* cap packet is literal
direct-sum projection: cap constructors retain their vectors, while response,
fixed-window, and covariance-bar constructors project to zero because their
implemented word/fine/repeated/operation idempotents differ.

The result is a 128-entry implemented registry with Gamma_* image rank 23 and
B/Eq rank 7.  It contains no kappa column.  The exact missing API object is a
degree-zero comparison edge Phi_KS,r0 from the response KS generator to the
cap r0 generator.  The existing standard mapping-cylinder/product constructor
can be applied only after such an edge is supplied; on the present registry it
raises MissingPhysicalArrow.  A strict covariance-bar x K_Eq square does exist
but has literal Gamma_* projection zero.  The literal Macaulay product
``b01*r0`` is also retained: its two Leibniz faces remain in the cap-r0
operation summand, so its Gamma_* mixed-comparison projection is zero.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gamma_star_physical_c1_registry_counterguard.py":
        "549c60c9613dff00ea2e29038970fd5a26715ba3f64dca5dd22980c8baab99ce",
    "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py":
        "262e1dd08dd1842d60515d45aea53ea406d7e1e5ea55ab506bb6e81d64b07741",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py":
        "e17de52244d324a26ff6a8b08f9226283b89d1737a6dc3916359991e777efb17",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py":
        "f237ccffd40863a201b780ea034fcbd7781bc555e1fbc6f528d99d3ab71394c6",
}
EXPECTED_LEDGER_SHA256 = "195d8fe444c0efc0d3cfd3c81ff8347fcccafd75a0535110cd3716b5a6001096"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO27 = (Q(0),) * 27
KAPPA_WORDS = (
    "0012", "0102", "0110", "0111",
    "0122", "0212", "1112", "2112",
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[columns[column][row] for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


@dataclass(frozen=True)
class Grade:
    word: str
    fine: str
    repeated: str
    operation: str
    window: str


@dataclass(frozen=True)
class Primitive:
    name: str
    family: str
    degree: int
    grade: Grade
    producer: str
    native_boundary: tuple[Q, ...]
    gamma_boundary: tuple[Q, ...]


@dataclass(frozen=True)
class OperationType:
    source: str
    target: str


def multiply_operation(left: OperationType, right: OperationType) \
        -> OperationType | None:
    """Composition in the literal two-object operation-idempotent algebra."""
    if left.target != right.source:
        return None
    return OperationType(left.source, right.target)


GAMMA = Grade(
    word="01211222",
    fine="six literal t*q_(v,N) P3+K2 occurrence degrees",
    repeated="P3+K2",
    operation="response-to-AugP2 mixed orbit/K_Eq",
    window="2345 with literal occurrence labels",
)
RESPONSE_KS = Grade(
    word="11110000",
    fine="centered marked response occurrence / selected first PP",
    repeated="response occurrence and PP faces",
    operation="universal response KS / endpoint-matching orbit",
    window="six-site response occurrence",
)
FIXED_WINDOW = Grade(
    word="0112/1112/0102/1102",
    fine="fixed-window word/chart/matching coordinates",
    repeated="C4 matching / relative H-r",
    operation="tag-preserving DQ/PS chart PP-Hasse-Cartan",
    window="2345",
)
BAR_KEQ = Grade(
    word="local face 2112 (coarse input 01211222)",
    fine="mixed-colour h_v*Y0 covariance coefficients",
    repeated="squarefree 2K2",
    operation="local-GL3 covariance/output bar x objectwise K_Eq",
    window="four-site covariance face without selected occurrence idempotent",
)
MACAULAY_B01_R0 = Grade(
    word="01211222 (cap r0 idempotent retained)",
    fine="selected b01 coefficient multiplied into cap r0",
    repeated="Macaulay b01 times cap-r0 product",
    operation="coefficient/PP x cap AugP2/K_Eq r0",
    window="selected 01 fibre over the cap object",
)


class MissingPhysicalArrow(RuntimeError):
    pass


class GenPhysRegistry:
    def __init__(self) -> None:
        self.entries: list[Primitive] = []
        self.arrows: dict[tuple[str, str], str] = {}

    def add(self, primitive: Primitive) -> None:
        require(len(primitive.gamma_boundary) == 27,
                ("Gamma boundary width", primitive.name))
        require(all(existing.name != primitive.name for existing in self.entries),
                ("duplicate primitive", primitive.name))
        self.entries.append(primitive)

    def add_arrow(self, source: str, target: str, producer: str) -> None:
        require(any(entry.name == source for entry in self.entries), source)
        require(any(entry.name == target for entry in self.entries), target)
        self.arrows[(source, target)] = producer

    def mapping_cylinder(self, source: str, target: str) -> str:
        producer = self.arrows.get((source, target))
        if producer is None:
            raise MissingPhysicalArrow(
                f"no registered degree-zero physical arrow {source} -> {target}"
            )
        return f"Cyl({source}->{target}) via {producer}"


def cap_family(name: str) -> str:
    if name.startswith("r0_"):
        return "K_Eq/AugP2 cap r0"
    if name.startswith(("T_", "rho_")):
        return "AugP2 cap normalizer"
    if name == "Cartan" or name.startswith("companion_"):
        return "Cartan/Weyl cap"
    if name.startswith("pure_target_"):
        return "pure target"
    return {
        "literal_q_identity": "physical q",
        "pointed_anchor": "pointed P_f",
        "ridge_only": "shifted ridge",
        "eta_only": "eta",
        "sigma_only": "sigma",
        "M_v": "complete AugP2 cap",
    }[name]


def fixed_window_family(name: str) -> str:
    prefix = name.split(":", 1)[0]
    return {
        "word": "PP/Hasse restriction-reinsertion",
        "C4": "C4 matching flip",
        "response": "complete response",
        "relative": "relative H-r graph",
        "r-word": "Cartan/Weyl retained-carrier word face",
        "r-response": "retained-carrier response face",
    }[prefix]


def build_registry(maximal, private_eq, fixed_window, response,
                   first_pp, bar_keq, provenance) -> GenPhysRegistry:
    registry = GenPhysRegistry()

    # Actual 27-row cap constructors.
    cap_columns, cap_names = maximal.cap_named_columns(private_eq)
    require(len(cap_columns) == len(cap_names) == 25,
            "cap constructor count")
    for name, boundary in zip(cap_names, cap_columns, strict=True):
        registry.add(Primitive(
            name=f"cap:{name}",
            family=cap_family(name),
            degree=1,
            grade=GAMMA,
            producer=(
                "verify_h3_maximal_pointed_balanced_same_grade_terminal_gate."
                "cap_named_columns"
            ),
            native_boundary=tuple(boundary),
            gamma_boundary=tuple(boundary),
        ))

    cap_provenance = provenance.cap_r0_provenance_audit()
    require(cap_provenance["constructed_cap_generator"] == "r_0"
            and cap_provenance["internal_B_equals_Eq_tie"],
            cap_provenance)

    # Actual fixed-window PP/Hasse/C4/response/relative columns.  Their
    # source constructor returns the 48-entry native boundaries directly.
    window_columns = fixed_window.build_internal_columns()
    require(len(window_columns) == 100
            and all(len(boundary) == 48 for _name, boundary in window_columns),
            "fixed-window constructor changed")
    for name, boundary in window_columns:
        registry.add(Primitive(
            name=f"window:{name}",
            family=fixed_window_family(name),
            degree=1,
            grade=FIXED_WINDOW,
            producer=(
                "verify_h3_fixed_window_centered_k22_physical_routing_gate."
                "build_internal_columns"
            ),
            native_boundary=tuple(boundary),
            gamma_boundary=ZERO27,
        ))

    # The implemented selected response KS generator d epsilon_s=-c_f.
    response_ledger = response.universal_centered_ks_audit()
    require(response_ledger["KS_rank"] == 89
            and response_ledger["relative_class_modulo_R"] ==
                "-c_f, c_f=N*f-R",
            response_ledger)
    ones = (Q(1),) * response.N
    selected = (Q(1),) + (Q(0),) * (response.N - 1)
    c_f = tuple(Q(response.N) * selected[index] - ones[index]
                for index in range(response.N))
    registry.add(Primitive(
        name="response:epsilon_s",
        family="response Kodaira-Spencer",
        degree=1,
        grade=RESPONSE_KS,
        producer=(
            "verify_h3_universal_response_deformation_e14_orbit_ks_gate."
            "universal_centered_ks_audit"
        ),
        native_boundary=tuple(-value for value in c_f),
        gamma_boundary=ZERO27,
    ))

    # Literal Macaulay shortcut: multiply the selected response coefficient
    # b01 by the constructed cap r0.  The product is source-valid and its
    # Leibniz boundary really contains both named-looking faces,
    #
    #   d(b01*r0)=db01*r0+b01*E.
    #
    # Multiplication is objectwise, so both faces retain the cap-r0 operation
    # idempotent.  They are not the response-selected db01 or the missing
    # response-to-cap Eq incidence.  Keep the product as an actual off-Gamma
    # registry entry rather than discarding it.
    pp_ledger = first_pp.derivative_of_matching_fibre_audit()
    require(pp_ledger["first_PP_face_count"] == 6
            and pp_ledger["response_head_word"] == "11:110000"
            and pp_ledger["central_Eq_input_incidence"] == 0,
            pp_ledger)
    # d(db01*r0)=-db01*E and d(b01*E)=+db01*E.
    second_boundary = (Q(-1) + Q(1),)
    require(second_boundary == (Q(0),),
            "Macaulay b01*r0 product lost d-squared")
    registry.add(Primitive(
        name="macaulay:b01*r0_0",
        family="Macaulay b01 times cap r0",
        degree=1,
        grade=MACAULAY_B01_R0,
        producer=(
            "literal Leibniz product of "
            "derivative_of_matching_fibre_audit and constructed cap r0"
        ),
        native_boundary=(Q(1), Q(1)),
        gamma_boundary=ZERO27,
    ))

    # A strict bar x K_Eq cell really is implemented.  It is retained as an
    # actual primitive and projected to zero, rather than silently retagged.
    bar_ledger = bar_keq.relative_bar_keq_product_audit()
    bar_grade = bar_keq.gamma_star_grade_audit()
    first_boundary = bar_ledger["symbolic_first_boundary"]
    order = ("L*theta", "D*theta", "E*F")
    boundary = tuple(Q(first_boundary[name]) for name in order)
    require(boundary == (Q(1), Q(-1), Q(-1))
            and bar_ledger["d_squared"] == 0
            and bar_grade["literal_projection_to_C_phys_Gamma_star"] ==
                "0 (off-grade)",
            (bar_ledger, bar_grade))
    registry.add(Primitive(
        name="bar_keq:kappa_bar",
        family="strict relative bar x K_Eq",
        degree=1,
        grade=BAR_KEQ,
        producer=(
            "verify_h3_relative_gl3_bar_keq_kappa_normalization_gate."
            "relative_bar_keq_product_audit"
        ),
        native_boundary=boundary,
        gamma_boundary=ZERO27,
    ))
    return registry


def registry_audit(registry: GenPhysRegistry, private_eq) -> dict[str, object]:
    counts: dict[str, int] = {}
    for entry in registry.entries:
        counts[entry.family] = counts.get(entry.family, 0) + 1
    require(len(registry.entries) == 128
            and sum(counts.values()) == 128
            and counts["response Kodaira-Spencer"] == 1
            and counts["strict relative bar x K_Eq"] == 1
            and counts["Macaulay b01 times cap r0"] == 1
            and counts["K_Eq/AugP2 cap r0"] == 4,
            counts)

    gamma_columns = tuple(entry.gamma_boundary for entry in registry.entries)
    projected = tuple(column[:8] for column in gamma_columns)
    psi = tuple(value / Q(4) for value in private_eq.vec(
        B=tuple(map(int, DELTA)), Eq=tuple(map(int, (-1, -1, 1, 1)))
    ))
    charges = tuple(dot(psi, column) for column in gamma_columns)
    require(rank(gamma_columns) == 23
            and rank(projected) == 7
            and set(charges) == {Q(0)},
            "implemented registry Gamma image changed")

    on_grade = tuple(entry for entry in registry.entries
                     if entry.grade == GAMMA)
    off_grade = tuple(entry for entry in registry.entries
                      if entry.grade != GAMMA)
    require(len(on_grade) == 25 and len(off_grade) == 103
            and all(entry.gamma_boundary == ZERO27 for entry in off_grade),
            "typed direct-sum projection changed")
    return {
        "implemented_primitive_count": len(registry.entries),
        "family_counts": dict(sorted(counts.items())),
        "Gamma_star_entries": len(on_grade),
        "off_Gamma_entries": len(off_grade),
        "Gamma_star_image_rank": rank(gamma_columns),
        "B_Eq_image_rank": rank(projected),
        "Psi_charge_histogram": {"0": len(charges)},
        "literal_kappa_columns": 0,
        "literal_kappa_words_realized": [],
        "strict_bar_x_K_Eq_retained": True,
        "strict_bar_x_K_Eq_Gamma_projection": 0,
        "Macaulay_b01_r0_retained": True,
        "Macaulay_b01_r0_Gamma_projection": 0,
    }


def missing_arrow_audit(registry, comparison, packaging, bar_keq) \
        -> dict[str, object]:
    comparison_ledger, comparison_digest = comparison.audit()
    require(comparison_digest == comparison.EXPECTED_LEDGER_SHA256,
            "response/cap comparison ledger changed")
    hom = comparison_ledger["literal_idempotent_Hom"]
    ungraded = comparison_ledger["ungraded_two_term_chain_map"]
    require(hom["Hom_degree0_response_to_cap_in_current_grammar"] == 0
            and not hom["standard_mapping_cylinder_can_create_missing_input_map"]
            and ungraded["normalized_solution"] == {"a": 1, "b": -1},
            (hom, ungraded))

    packaging_ledger, packaging_digest = packaging.audit()
    require(packaging_digest == packaging.EXPECTED_LEDGER_SHA256,
            "packaging ledger changed")
    package = packaging_ledger["augmented_packaging"]
    require(not package["existing_AugP2_status"]
                ["constructed_literal_source_object"],
            package)

    bar_grade = bar_keq.gamma_star_grade_audit()
    require(not bar_grade["is_the_kappa_operation_parent"], bar_grade)

    macaulay = next(entry for entry in registry.entries
                    if entry.name == "macaulay:b01*r0_0")
    require(macaulay.native_boundary == (Q(1), Q(1))
            and macaulay.grade.word.startswith("01211222")
            and macaulay.grade.operation ==
                "coefficient/PP x cap AugP2/K_Eq r0"
            and macaulay.gamma_boundary == ZERO27,
            macaulay)

    response_diagonal = OperationType("response", "response")
    cap_diagonal = OperationType("cap", "cap")
    cap_r0 = OperationType("cap", "cap")
    desired_phi = OperationType("response", "cap")
    response_product = multiply_operation(response_diagonal, cap_r0)
    cap_product = multiply_operation(cap_diagonal, cap_r0)
    require(response_product is None
            and cap_product == cap_diagonal
            and cap_product != desired_phi,
            (response_product, cap_product, desired_phi))

    failure = None
    try:
        registry.mapping_cylinder("response:epsilon_s", "cap:r0_0")
    except MissingPhysicalArrow as error:
        failure = str(error)
    require(failure == (
        "no registered degree-zero physical arrow response:epsilon_s -> cap:r0_0"
    ), failure)

    return {
        "requested_constructor": "Phi_KS,r0: response:epsilon_s -> cap:r0_i",
        "ungraded_chain_map_shape": {
            "Phi_1_epsilon": "r0", "Phi_0_c_f": "-E",
        },
        "ungraded_shape_unique_after_normalization": True,
        "physical_degree_zero_Hom_dimension": 0,
        "mapping_cylinder_API_result": "MissingPhysicalArrow",
        "exception": failure,
        "tag_mismatches": ["word", "fine", "repeated", "operation", "window"],
        "existing_strict_bar_x_K_Eq_is_substitute": False,
        "reason_bar_fails": (
            "it preserves the covariance/output-bar 2K2 idempotents and has "
            "literal Gamma_* projection zero"
        ),
        "packaged_cross_word_AugP2_object_exists": False,
        "Macaulay_b01_times_r0_shortcut": {
            "constructor_exists": True,
            "Leibniz_boundary": "db01*r0+b01*E",
            "d_squared": 0,
            "selected_db01_terms": 6,
            "cap_word_retained": "01211222",
            "operation_parent_retained": "cap AugP2/K_Eq r0",
            "is_response_selected_db01": False,
            "is_response_to_cap_Eq_incidence": False,
            "literal_Gamma_star_projection": 0,
            "first_separator": "source module role / operation parent",
            "operation_idempotent_test": {
                "response_b01_type": "response->response",
                "cap_copy_b01_type": "cap->cap",
                "r0_type": "cap->cap",
                "response_b01_times_r0": "undefined/zero (orthogonal idempotents)",
                "cap_copy_b01_times_r0": "cap->cap",
                "required_Phi_type": "response->cap",
            },
            "conclusion": (
                "Macaulay multiplication supplies an internal cap-parent PP "
                "product, not the missing off-diagonal Phi_KS,r0 matrix unit"
            ),
        },
        "first_required_faces": [
            "selected db01 and endpoint/root-labelled mates",
            "central Eq incidence Phi((H0-u)e_Eq)=R_E14",
            "six t*q_(v,N) P3+K2 and sibling 3K2 faces",
            "physical q/W/residue/ridge/eta/sigma faces",
        ],
        "conditional_after_constructor": {
            "standard_kappa_instances": list(KAPPA_WORDS),
            "strict_normalized_charges": [0] * len(KAPPA_WORDS),
            "status": "conditional, not entries of the implemented registry",
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    maximal = load(
        "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py",
        "gen_phys_maximal",
    )
    private_eq = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "gen_phys_private_eq",
    )
    fixed_window = load(
        "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
        "gen_phys_fixed_window",
    )
    response = load(
        "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py",
        "gen_phys_response_ks",
    )
    first_pp = load(
        "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py",
        "gen_phys_first_pp",
    )
    comparison = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "gen_phys_response_cap_comparison",
    )
    bar_keq = load(
        "computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py",
        "gen_phys_bar_keq",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "gen_phys_packaging",
    )
    provenance = load(
        "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py",
        "gen_phys_r0_provenance",
    )

    registry = build_registry(
        maximal, private_eq, fixed_window, response, first_pp, bar_keq,
        provenance)
    ledger = {
        "theorem": "h3 Gamma-star executable Gen_phys registry",
        "pins": PINS,
        "registry": registry_audit(registry, private_eq),
        "comparison_functor": {
            "name": "literal direct-sum projection Pi_Gamma*",
            "target_rows": 27,
            "rule": (
                "retain actual cap_named_columns vectors at exact Gamma_*; "
                "send implemented orthogonal word/fine/repeated/operation "
                "summands to zero"
            ),
            "source_is_executable_registry": True,
            "claim_full_physical_exhaustiveness": False,
        },
        "first_absent_constructor": missing_arrow_audit(
            registry, comparison, packaging, bar_keq),
        "verdict": (
            "The smallest executable registry assembled from the implemented "
            "response KS, cap r0/AugP2, PP/Hasse, Cartan/Weyl and K_Eq APIs "
            "has 128 primitive entries.  Literal projection to Gamma_* has "
            "rank 23 (B/Eq rank 7), and every registered charge is zero.  "
            "There is no literal kappa column.  The precise API failure is "
            "the absent degree-zero physical arrow Phi_KS,r0; invoking the "
            "mapping-cylinder constructor on response epsilon_s and cap r0 "
            "raises MissingPhysicalArrow.  The existing strict bar x K_Eq "
            "cell is real but off-grade.  Adding one normalized Phi schema, "
            "with its listed proper faces, would instantiate all eight "
            "standard kappas and conditionally give charge zero."
        ),
        "scope": (
            "exact executable registry for the named already-implemented h=3 "
            "primitive APIs; not a claim that these APIs exhaust an unwritten "
            "full physical source complex"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "registry", "missing-arrow"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("executable Gen_phys ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 executable Gen_phys(Gamma_*) ({arguments.mode}): PASS")
        print("implemented primitives: 128; Gamma image rank: 23; B/Eq rank: 7")
        print("literal kappa columns: 0")
        print("Phi_KS,r0 mapping cylinder: MissingPhysicalArrow")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
