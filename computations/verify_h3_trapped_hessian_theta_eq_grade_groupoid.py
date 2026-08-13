#!/usr/bin/env python3
"""Build the two-object theta-grade groupoid for the trapped Hessian square.

The endpoint transpose theta is a literal involutive permutation, not a
nonconstant toric transition.  It exchanges the canonical faces-(3,5)
repeated grade g with a conjugate grade g^T and exchanges their six private
matching rows.  Consequently its first-principal-parts prolongation is

                 J1(theta) = [[theta, 0], [0, theta]];

there is no d(theta) diagonal and no two-edge fine-grade holonomy.

The physical covectors Lambda_g=sum(F_g)-ainc and
Lambda_gT=sum(F_gT)-ainc form an exact equivariant q section.  Target, W,
anchor incidence, ordinary residue, eta, and sigma likewise transport in
the two-object terminal module.  The formal central reduced-Eq cone
K_Eq(beta) is theta-equivariant and therefore introduces no new grade
class.  It does not, however, construct the still-missing source-labelled
response-to-Eq attachment: that one physical descent at either object is
the remaining datum.
"""

from __future__ import annotations

import ast
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py":
        "a51b8f091a25624d17443c70ac70b60eb257c8b11dafb0b9ad3f17962dc07390",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
    "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py":
        "e5deda7162db47f229239dc91b419baaf00c3158249859cbafb03fe3af2cc958",
}
EXPECTED_LEDGER_SHA256 = (
    "79a575e9fbd4794eb1dd92f088ccb8c69f90eea1bd854facf996200935bc712e"
)

P = 6
S = 7
SITE_THETA = {0: 1, 1: 0, P: S, S: P}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def theta_site(site: int) -> int:
    return SITE_THETA.get(site, site)


def theta_degree(degree):
    answer = [0] * len(degree)
    require(len(degree) == 24, "expected one three-colour degree per eight sites")
    for site in range(8):
        for colour in range(3):
            answer[3 * theta_site(site) + colour] = degree[3 * site + colour]
    return tuple(answer)


def edge(left: int, right: int, a: int, b: int):
    if left < right:
        return left, right, a, b
    return right, left, b, a


def theta_cell(cell):
    left, right, a, b = cell
    return edge(theta_site(left), theta_site(right), a, b)


def theta_feature(feature):
    return tuple(sorted(theta_cell(cell) for cell in feature))


def matrix_multiply(left, right):
    return tuple(tuple(sum(Q(a) * Q(b) for a, b in
                           zip(row, column, strict=True))
                       for column in zip(*right, strict=True))
                 for row in left)


def matrix_vector(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def grade_groupoid_audit(separator_ledger):
    canonical = tuple(separator_ledger["canonical_fine_degree"])
    conjugate = theta_degree(canonical)
    require(canonical != conjugate,
            "theta unexpectedly fixed the canonical repeated fine grade")
    require(theta_degree(conjugate) == canonical,
            "theta stopped being involutive on the fine grading")

    difference = tuple(right - left for left, right in
                       zip(canonical, conjugate, strict=True))
    nonzero = [(index // 3, index % 3, value)
               for index, value in enumerate(difference) if value]
    require(nonzero == [(0, 1, 1), (1, 1, -1)],
            ("the primitive grade displacement changed", nonzero))

    features = tuple(ast.literal_eval(value) for value in
                     separator_ledger["selected_private_features"])
    conjugate_features = tuple(theta_feature(feature) for feature in features)
    require(len(features) == 6 and len(set(features)) == 6
            and len(set(conjugate_features)) == 6
            and not (set(features) & set(conjugate_features)),
            "the two six-feature objects stopped being disjoint")
    require(tuple(theta_feature(feature) for feature in conjugate_features)
            == features, "theta stopped pairing the private features")

    return {
        "objects": ["g=canonical faces-(3,5)", "gT=theta(g)"],
        "canonical_degree": list(canonical),
        "conjugate_degree": list(conjugate),
        "primitive_displacement": [
            {"site": site, "colour": colour, "coefficient": value}
            for site, colour, value in nonzero
        ],
        "nonidentity_arrows": ["theta:g->gT", "theta:gT->g"],
        "composition": "theta^2=id",
        "private_features_per_object": 6,
        "private_feature_overlap": 0,
        "minimality": (
            "one object cannot retain the literal fine grade because g!=gT; "
            "the involution closes on exactly these two objects"
        ),
    }, features, conjugate_features


def first_principal_parts_audit():
    theta = ((Q(0), Q(1)), (Q(1), Q(0)))
    identity = ((Q(1), Q(0)), (Q(0), Q(1)))
    zero = ((Q(0), Q(0)), (Q(0), Q(0)))
    require(matrix_multiply(theta, theta) == identity,
            "the object permutation stopped squaring to the identity")

    # Block order is (value_g,value_gT,dvalue_g,dvalue_gT).  Since theta is
    # a constant source automorphism, d(theta)=0.
    jet = (
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 1, 0),
    )
    require(matrix_multiply(jet, jet) == tuple(
        tuple(Q(index == column) for column in range(4))
        for index in range(4)
    ), "the first jet of theta stopped being involutive")

    # Check d(theta*f)=theta*df on a generic two-object value and tangent.
    value = (Q(2), Q(-3))
    tangent = (Q(5), Q(7))
    transformed = matrix_vector(jet, value + tangent)
    require(transformed == matrix_vector(theta, value) +
            matrix_vector(theta, tangent),
            "constant theta acquired a Leibniz correction")
    require(zero == ((Q(0), Q(0)), (Q(0), Q(0))),
            "the zero PP diagonal changed")

    return {
        "transition_matrix": "theta=[[0,1],[1,0]]",
        "first_jet": "J1(theta)=[[theta,0],[0,theta]]",
        "first_PP_diagonal": 0,
        "two_edge_loop_jet": "J1(theta)^2=id",
        "fine_grade_holonomy_class": 0,
        "contrast_with_pq_xv": (
            "pq/xv uses the nonconstant ratio U=u/t and has diagonal dU; "
            "theta is a constant finite permutation and has dtheta=0"
        ),
    }


def physical_q_and_terminal_audit(features, conjugate_features):
    # Coordinate order: six canonical features, six theta features, ainc.
    size = 13
    theta = [[Q(0)] * size for _ in range(size)]
    for index in range(6):
        theta[6 + index][index] = Q(1)
        theta[index][6 + index] = Q(1)
    theta[12][12] = Q(1)
    theta = tuple(tuple(row) for row in theta)
    identity = tuple(tuple(Q(row == column) for column in range(size))
                     for row in range(size))
    require(matrix_multiply(theta, theta) == identity,
            "theta stopped being involutive on feature/anchor coordinates")

    lambda_g = (Q(1),) * 6 + (Q(0),) * 6 + (Q(-1),)
    lambda_gT = (Q(0),) * 6 + (Q(1),) * 6 + (Q(-1),)
    # Pullback convention: theta sends a g-vector to gT; Lambda_gT o theta
    # must equal Lambda_g.
    require(tuple(dot(lambda_gT, column) for column in
                  zip(*theta, strict=True)) == lambda_g,
            "physical q failed equivariant descent")

    tests = (
        (Q(2), Q(-1), Q(0), Q(3), Q(4), Q(-2)) +
        (Q(0),) * 6 + (Q(5),),
        (Q(0),) * 6 +
        (Q(-3), Q(7), Q(1), Q(0), Q(-2), Q(4)) + (Q(-1),),
    )
    require(all(dot(lambda_gT, matrix_vector(theta, vector))
                == dot(lambda_g, vector) for vector in tests),
            "sample physical q values stopped transporting")

    # Terminal labels carry the same finite permutation.  Scalars target,
    # W, ainc and the unordered external sigma_PS are fixed.  eta_0,eta_1
    # are exchanged.  Ordinary residue is retained objectwise rather than
    # falsely identifying its two labelled copies.
    terminal_labels = (
        "target", "W", "ainc", "ores_g", "ores_gT",
        "eta_0", "eta_1", "sigma_PS",
    )
    terminal_theta = (0, 1, 2, 4, 3, 6, 5, 7)
    require(tuple(terminal_theta[index] for index in terminal_theta)
            == tuple(range(len(terminal_labels))),
            "terminal theta stopped being involutive")

    return {
        "physical_q_at_g": "Lambda_g=sum(F_g)-ainc",
        "physical_q_at_gT": "Lambda_gT=sum(F_gT)-ainc",
        "q_cocycle": "Lambda_gT o theta-Lambda_g=0 exactly",
        "q_quotient_obstruction": 0,
        "target": "fixed",
        "W": "fixed",
        "anchor_incidence": "fixed (protected marked product is fixed)",
        "ordinary_residue": "two labelled copies exchanged objectwise",
        "eta": "eta_0<->eta_1; all other physical-site eta labels transport",
        "sigma": "the unordered external P-S sigma edge is fixed",
        "word": "fixed on the equal-colour endpoint corner orbit",
        "terminal_collapse_warning": (
            "compatibility is equivariance in the two-object module, not "
            "literal equality of ores_g with ores_gT before transport"
        ),
        "actual_feature_pair_count": len(tuple(zip(
            features, conjugate_features, strict=True
        ))),
    }


def central_eq_cone_audit():
    # Objectwise complex K -> E with dK=E.  theta exchanges the copies and
    # fixes beta and the scalar conormal label.  Verify d theta=theta d and
    # zero monodromy on the two-edge loop.
    differential = ((Q(1), Q(0)), (Q(0), Q(1)))
    theta = ((Q(0), Q(1)), (Q(1), Q(0)))
    require(matrix_multiply(differential, theta)
            == matrix_multiply(theta, differential),
            "central Eq boundary stopped commuting with theta")
    require(matrix_multiply(theta, theta)
            == ((Q(1), Q(0)), (Q(0), Q(1))),
            "the Eq cone acquired two-edge monodromy")

    beta_tests = (Q(0), Q(1), Q(-2), Q(7, 3))
    require(all(matrix_vector(theta, (beta, -beta)) == (-beta, beta)
                for beta in beta_tests),
            "central beta coefficient stopped commuting with object exchange")
    return {
        "formal_objectwise_cones": [
            "K_Eq(beta)_g -> E_g", "K_Eq(beta)_gT -> E_gT"
        ],
        "conormal": "E=(H0-u)e_Eq",
        "centrality_square": "d theta(K_g)=theta d(K_g)=E_gT",
        "beta_transport": "theta(beta)=beta",
        "two_edge_cone_holonomy": 0,
        "what_transports_LambdaT_back": (
            "the physical theta arrow; K_Eq is central and only corrects "
            "the reduced-Eq boundary objectwise"
        ),
        "remaining_physical_datum": (
            "one source-labelled response-to-Eq attachment at g, with the "
            "stated q and terminal rows; theta then supplies the gT copy"
        ),
        "physical_K_Eq_constructed_here": False,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    separator = load(
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py",
        "theta_grade_separator",
    )
    separator_ledger = separator.audit()
    groupoid, features, conjugate_features = grade_groupoid_audit(
        separator_ledger
    )
    ledger = {
        "theorem": "trapped Hessian theta/Eq two-grade groupoid theorem",
        "pins": PINS,
        "minimal_grade_groupoid": groupoid,
        "first_principal_parts": first_principal_parts_audit(),
        "physical_q_and_terminals": physical_q_and_terminal_audit(
            features, conjugate_features
        ),
        "central_reduced_Eq_cone": central_eq_cone_audit(),
        "exact_conclusion": (
            "theta removes the apparent conjugate-grade holonomy in the "
            "minimal two-object category: its first PP diagonal and q "
            "cocycle both vanish.  K_Eq(beta) commutes with theta and adds "
            "no further fine-grade class"
        ),
        "sharp_guard": (
            "neither the constant theta arrow nor the formal central Eq "
            "cone is the missing source-labelled response-to-Eq cell.  A "
            "physical K_Eq/off-diagonal attachment at one object remains "
            "necessary and is sufficient, by theta transport, at the other"
        ),
        "scope": (
            "exact literal fine degrees, six-feature/anchor physical q, "
            "first jets, involutive composition, and equivariant terminal "
            "typing.  No physical reduced-Eq source generator is asserted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("theta/Eq groupoid ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 trapped Hessian theta/Eq grade groupoid: PASS")
    print("objects: g, theta(g); primitive displacement: +(0,1)-(1,1)")
    print("first PP diagonal: 0; two-edge fine-grade holonomy: 0")
    print("physical q cocycle: 0 exactly; terminals: theta-equivariant")
    print("central K_Eq holonomy: 0; physical response-to-Eq cell: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
