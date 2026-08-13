#!/usr/bin/env python3
"""Audit the selected-fibre graph route to the E14 mixed K_Eq cell.

The marked occurrence coordinate used by P_f and the fixed-endpoint K4
fibre are not the same object: b_01 is the sum of three matching
occurrences.  A fresh monic graph z_01=b_01 is presentation-safe and its
Koszul product with F=H0-u is canonical.  It does not make b_01 a source
equation: the mixed boundary retains z_01*theta.  Killing z_01 changes the
classical fibre.  The fibre-preserving alternative is the centered class
c_01=30 b_01-R; over characteristic zero, epsilon_01=(epsilon_R+epsilon_c)/30.

The occurrence projector has the exact coefficient identity
(A+I)c_f=3c_01.  Thus a physical centered occurrence lift natural for the
matching operator would construct the selected edge and hence the mixed
cell.  Its first literal word face is the known six-term db_01 packet.
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
    "computations/verify_h3_fixed_endpoint_k4_central_eq_derived_intersection_gate.py":
        "cf0c07467805354ca9681327351de94cca08ef025b3e94328c957965437e5bc3",
    "notes/h3-fixed-endpoint-k4-central-eq-derived-intersection-gate.md":
        "323030914c65b6ab2dd98aad88f731e22f2bcd944770c7662872f8b11dc16678",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_p2_pointed_source_graph_slack_gate.py":
        "d36e26ef2c82b018b62228c159f1f17a63d0c19ed1fd342d7684cbf4e55b1098",
    "notes/h3-p2-pointed-source-graph-slack-gate.md":
        "f6ed7b1ee338f8c37404fcaf6f0b9252f8528b1fee722269d4934a4624556eff",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "notes/h3-e14-pointed-orbit-keq-mapping-cylinder-gate.md":
        "f5008f5b7e892b5ce5270faacee4ec9f2bffc2630b8dd15a55cb8f5c6800cb21",
}
EXPECTED_LEDGER_SHA256 = (
    "fb27970da3edf4ad7f92f9d4a3743a56935cd9b40daa47c7ec2ee07dff50f172"
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


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def occurrence_coordinate_is_not_fibre_coordinate() -> dict[str, object]:
    # Coordinates: (f,m1,m2,u_f,z_01).  The marked occurrence graph and
    # selected K4-fibre graph are both triangular monic extensions.
    graph_occurrence = tuple(map(Q, (-1, 0, 0, 1, 0)))
    graph_fibre = tuple(map(Q, (-1, -1, -1, 0, 1)))
    z_minus_u_f = tuple(map(Q, (0, 0, 0, -1, 1)))
    mates = tuple(map(Q, (0, 1, 1, 0, 0)))
    require(rank((graph_occurrence, graph_fibre)) == 2
            and add(z_minus_u_f, scale(-1, mates))
                == add(graph_fibre, scale(-1, graph_occurrence)),
            "the occurrence/fibre graph identity changed")

    # A concrete old-source point satisfies both graph equations but has
    # z_01 != u_f.  Adjoining their equality deletes it and, after graph
    # elimination, imposes m1+m2=0.
    point = tuple(map(Q, (1, 1, 0, 1, 2)))
    require(dot(graph_occurrence, point) == 0
            and dot(graph_fibre, point) == 0
            and dot(z_minus_u_f, point) == 1
            and dot(mates, point) == 1,
            "the graph fibre-change witness moved")
    return {
        "coordinate_order": ["marked f", "matching mate 1", "matching mate 2",
                             "u_f", "z_01"],
        "marked_occurrence_graph": "u_f-f=0",
        "selected_fibre_graph": "z_01-b_01=0, b_01=f+m1+m2",
        "both_graph_extensions_monic": True,
        "identity_on_graph": "z_01-u_f=m1+m2",
        "u_f_is_z_01": False,
        "reusing_P_f_coordinate_as_selected_fibre_coordinate": (
            "imposes m1+m2=0 and changes the classical source fibre"
        ),
        "deleted_point": {
            "f": 1, "m1": 1, "m2": 0, "u_f": 1, "z_01": 2,
        },
        "consequence": (
            "the coordinate already used by P_f cannot itself be the "
            "three-occurrence b_01 graph coordinate"
        ),
    }


def graph_koszul_square_audit() -> dict[str, object]:
    # In coefficient coordinates (b_01, all-other fibres, z_01), the actual
    # complete response is R=b+m, and the monic graph relation is z-b.
    response_R = tuple(map(Q, (1, 1, 0)))
    graph = tuple(map(Q, (-1, 0, 1)))
    selected_b = tuple(map(Q, (1, 0, 0)))
    basepoint_z = tuple(map(Q, (0, 0, 1)))
    separator = tuple(map(Q, (1, -1, 1)))
    require(rank((response_R, graph)) == 2
            and rank((response_R, graph, selected_b)) == 3
            and dot(separator, response_R) == 0
            and dot(separator, graph) == 0
            and dot(separator, selected_b) == 1,
            "the graph selected-fibre separator changed")

    # The point b=z=1, m=-1 is on R=z-b=0 but not on b=0.  Hence b is not
    # made into an equation by the graph extension.
    point = tuple(map(Q, (1, -1, 1)))
    require(dot(response_R, point) == dot(graph, point) == 0
            and dot(selected_b, point) == 1,
            "the selected graph nonmembership point changed")

    # The DGA has d eps_g=z-b and d theta=F.  The canonical mixed cell has
    # d kappa_g=(z-b)theta-eps_g F, and d^2=0.  The selected b*theta term is
    # accompanied by z*theta.  Adding tau with d tau=z gives
    # eps_b=tau-eps_g and d eps_b=b, but z=0 changes the classical fibre.
    d2_graph_square = Q(1) - Q(1)
    require(d2_graph_square == 0
            and add(basepoint_z, scale(-1, graph)) == selected_b,
            "the graph/basepoint Koszul identities changed")
    return {
        "coefficient_rows": ["b_01", "sum other b_ps", "z_01"],
        "available_equations": {
            "R": [1, 1, 0],
            "z_01-b_01": [-1, 0, 1],
        },
        "selected_b_01": [1, 0, 0],
        "rank_available_then_selected": [2, 3],
        "primitive_selected_dual": [1, -1, 1],
        "graph_mixed_cell": (
            "kappa_g=epsilon_g wedge theta, "
            "d kappa_g=(z_01-b_01)theta-epsilon_g(H0-u)e_Eq"
        ),
        "graph_mixed_d_squared": 0,
        "unwanted_proper_face": "z_01*theta accompanies -b_01*theta",
        "basepoint_repair": (
            "d tau=z_01; epsilon_01=tau-epsilon_g then "
            "d epsilon_01=b_01"
        ),
        "basepoint_repair_changes_fibre": "z_01=0, hence b_01=0",
        "presentation_safe_graph_alone_constructs_selected_equation": False,
    }


def centered_fibre_positive_reduction() -> dict[str, object]:
    # Thirty endpoint fibres.  R=1_30, b_01=e_01 and
    # c_01=30e_01-1_30.  Over characteristic zero, a physical generator for
    # c_01 plus the existing complete response generator gives epsilon_01.
    fibres = 30
    aggregate = (Q(1),) * fibres
    selected = (Q(1),) + (Q(0),) * (fibres - 1)
    centered_fibre = add(scale(fibres, selected), scale(-1, aggregate))
    reconstructed = scale(Q(1, fibres), add(aggregate, centered_fibre))
    require(reconstructed == selected
            and sum(centered_fibre, Q(0)) == 0,
            "the centered selected-fibre reconstruction changed")

    # Ninety occurrence coordinates: f is one marked matching occurrence,
    # b_01 is its three-element fixed-endpoint matching fibre.  For the
    # matching numerator M=A+I, M e_f=b_01 and M 1=3*1.  Therefore
    # M c_f=3 c_01 exactly.
    occurrences = 90
    occurrence_ones = (Q(1),) * occurrences
    e_f = (Q(1),) + (Q(0),) * (occurrences - 1)
    b_01 = (Q(1), Q(1), Q(1)) + (Q(0),) * (occurrences - 3)
    c_f = add(scale(occurrences, e_f), scale(-1, occurrence_ones))
    c_01_occurrence = add(scale(fibres, b_01), scale(-1, occurrence_ones))
    matching_of_c_f = add(scale(occurrences, b_01),
                          scale(-3, occurrence_ones))
    require(matching_of_c_f == scale(3, c_01_occurrence)
            and sum(c_f, Q(0)) == sum(c_01_occurrence, Q(0)) == 0,
            "(A+I)c_f=3c_01 changed")

    return {
        "endpoint_fibres": fibres,
        "centered_selected_fibre": "c_01=30*b_01-R",
        "rational_selected_edge": (
            "epsilon_01=(epsilon_R+epsilon_c01)/30, so "
            "d epsilon_01=b_01"
        ),
        "characteristic_requirement": "30 invertible (the proof works over Q[beta])",
        "occurrences": occurrences,
        "centered_marked_occurrence": "c_f=90*e_f-1_90",
        "matching_numerator": "M=A+I",
        "coefficient_identity": "M(c_f)=3*c_01",
        "positive_conditional_construction": (
            "a physical source-labelled c_f lift natural under M gives "
            "epsilon_c01=M(epsilon_cf)/3; combine with epsilon_R and form "
            "kappa_01=epsilon_01 wedge theta"
        ),
        "new_basepoint_needed_after_physical_centered_lift": False,
        "physical_centered_lift_currently_constructed": False,
    }


def literal_proper_face_and_scope() -> dict[str, object]:
    selected = load(
        "computations/verify_h3_fixed_endpoint_k4_central_eq_derived_intersection_gate.py",
        "selected_fibre_graph_dependency",
    )
    ledger, digest = selected.audit()
    require(digest == selected.EXPECTED_LEDGER_SHA256,
            "the selected-fibre dependency ledger changed")
    response = ledger["response_and_PP_provenance"]
    target = ledger["target_and_physical_scope"]
    require(response["fibre_rank_old_then_marked"] == [1, 2]
            and response["PP_rank_old_then_marked"] == [1, 2]
            and target["endpoint_target_normal_support"] == 18,
            "the selected-fibre physical scope changed")
    return {
        "bottom_head_word": response["response_head_word"],
        "selected_fibre": response["marked_fibre"],
        "first_literal_PP_face": response["marked_first_PP_face"],
        "first_PP_face_terms": 6,
        "first_PP_source_provenance": (
            "selected db_01, not the old complete dR=sum db_ps"
        ),
        "matching_face_target": 0,
        "endpoint_target_normal_support": 18,
        "endpoint_target_normal": target["endpoint_Cartan_target_normal"],
        "central_theta_scope": target["central_Tate_physical_scope"],
        "word_fine_repeated_descent": (
            "the graph and centered identities are formal presentation data. "
            "A physical lift must place db_01 and dz_01 in the same "
            "11:110000 fixed-endpoint PP object, then transport the endpoint "
            "cube to G11[111111]/E14 word 000101 and the cap faces to "
            "01211222 / t*q_(v,N) / P3+K2"
        ),
        "beta_scope": (
            "the centered split is defined over Q[beta] and has no beta "
            "torsion; beta=0 is covered only if the physical centered lift, "
            "theta, and all proper faces are integral in beta"
        ),
        "ridge_scope": (
            "the selected graph square has no shifted pq/xv ridge by itself; "
            "gamma=-dOmega remains the independent labelled Kahler face"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "selected-fibre graph / central-K_Eq Koszul gate",
        "pins": PINS,
        "occurrence_vs_fibre_coordinate": (
            occurrence_coordinate_is_not_fibre_coordinate()
        ),
        "presentation_safe_graph_square": graph_koszul_square_audit(),
        "centered_fibre_reduction": centered_fibre_positive_reduction(),
        "physical_face_and_scope": literal_proper_face_and_scope(),
        "verdict": (
            "Adjoining z_01-b_01 gives a canonical 2x2 graph/K_Eq Koszul "
            "cell but does not make b_01 a source equation: z_01*theta is "
            "the residual proper face.  Reusing the P_f occurrence coordinate "
            "or killing z_01 changes the classical fibre.  The unique "
            "fibre-preserving positive route is centered splitting: "
            "c_01=30b_01-R and (A+I)c_f=3c_01.  A physical centered c_f lift "
            "would therefore make the selected edge and kappa automatic; "
            "its first literal descent face is the six-term db_01 packet."
        ),
        "shortest_positive_input": (
            "one source-labelled centered occurrence lift c_f natural under "
            "the matching numerator and endpoint orbit, together with the "
            "already open clean physical central theta.  No extra selected "
            "basepoint is needed after that lift."
        ),
        "scope": (
            "canonical h=3 over Q[beta].  The graph/Koszul and centered "
            "identities are exact; existence of the physical c_f lift, "
            "endpoint target correction, cap/ridge/q typing, beta-integral "
            "descent, and terminal promotion remain open."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("P_f occurrence coordinate equals selected b_01 coordinate: NO")
    print("monic z_01-b_01 graph: PRESENTATION-SAFE")
    print("graph alone makes b_01 a source equation: NO (z_01*theta remains)")
    print("killing z_01: FILLS BUT CHANGES FIBRE")
    print("centered split c_01=30b_01-R: EXACT OVER Q")
    print("matching identity (A+I)c_f=3c_01: EXACT")
    print("first physical descent: selected six-term db_01 face")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
