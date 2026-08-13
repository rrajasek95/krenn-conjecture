#!/usr/bin/env python3
"""Compare the pointed occurrence conormal with the primitive cap ``p``.

The one-occurrence Hasse square is finite once a pointed occurrence section
is given.  Two previously isolated candidates must not be conflated:

* ``P_f`` is the graph/Koszul generator for the degree-zero relation
  ``u_f-u``; its conormal is the marked/global pointed row.
* ``p`` is the projected reduced cap with ``(Q,ores)=(-1,-1)`` and all
  protected/target rows zero.

They are independent faces/generators of one possible enriched comparison,
not a committed equality.  The universal occurrence graph makes ``f-u_f``
contractible, but not ``u_f-u``; adding the latter raises conormal rank.

A single literal ``p`` also does not generate the eight fixed-packet P2
private squares.  Those live in eight independent word blocks and the
marked packet has trivial site/root stabilizer.  One universal natural
*family* could instantiate all eight, but that is stronger than one column.
The primitive p projection has target zero, while the natural centered P2
lift has a nonzero mixed-target normal.  If that target cone is separately
granted, q23 reinsertion still produces an occurrence-labelled conormal.
Even in the strongest formal same-label use of p, its Q face can cancel the
conormal but its labelled ores face remains; scalar ores sees zero.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py":
        "77d13c31df34efa26b575497bdd7bb2cc9173e8d1907030541444551c7417804",
    "computations/verify_h2_p2_one_root_private_orbit_bright_dark_gate.py":
        "406c4be1a72a71c6c80fdf1c1929e64dce128847d5b20a02bb95e4a8582772d0",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "computations/verify_h2_lower_0112_bminus4_target_normal_gate.py":
        "8fffe45182c4bb304dabfbe9df568061a8049bec21949539bcae88f60f5d22e0",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py":
        "9e60fb8410288a192b8be3b59938e5e7ba4ea42b455fee67b94ca6ef37777fde",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    # Commits 1ff2e54, 46ec0f4, and 30b9023: the raw marked projector has a
    # scalar zero-face, its graph is contractible, and the formal occurrence
    # simplex proves only the scaled 90*du_f=du law before physical descent.
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
    "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py":
        "ce28ff5d25bf575c280a21c0e35c6dc1ebef54eb039ac94cdc25932a61b95829",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
}
EXPECTED_LEDGER_SHA256 = (
    "5d61c15a520af9790f864e45684029bc75bf5f3437e08fdcf38c21293ea69f81"
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
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
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


def unit(index: int, size: int):
    return tuple(Q(position == index) for position in range(size))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    graph = load(
        "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py",
        "pointed_cap_graph",
    )
    graph_ledger, graph_digest = graph.audit()
    require(graph_digest == graph.EXPECTED_LEDGER_SHA256,
            "the universal graph ledger changed")
    pointed = graph_ledger["first_pointed_obstruction"]
    require(pointed["old_conormal_rank"] == 3
            and pointed["rank_after_pointed_row"] == 4
            and pointed["required_pointed_row"] == "d(u_f-u)",
            "the pointed graph rank gate changed")

    # Reproduce the graph calculation in coordinates (f,G,u_f,H0,u).
    d_e = (Q(1), Q(0), Q(-1), Q(0), Q(0))
    d_m = (Q(0), Q(1), Q(1), Q(0), Q(0))
    d_f0 = (Q(0), Q(0), Q(0), Q(1), Q(-1))
    d_pointed = (Q(0), Q(0), Q(1), Q(0), Q(-1))
    tangent = (Q(1), Q(-1), Q(1), Q(0), Q(0))
    require(rank((d_e, d_m, d_f0)) == 3
            and rank((d_e, d_m, d_f0, d_pointed)) == 4
            and all(dot(row, tangent) == 0
                    for row in (d_e, d_m, d_f0))
            and dot(d_pointed, tangent) == 1,
            "the explicit pointed conormal calculation changed")

    cap = load(
        "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py",
        "pointed_cap_primitive",
    )
    cap_ledger, cap_digest = cap.audit()
    require(cap_digest == cap.EXPECTED_LEDGER_SHA256,
            "the primitive cap ledger changed")
    cap_packet = cap_ledger["physical_cap_quotient"]
    require(cap_packet["required_augmented_signature"]
            == [0, -1, 0, 0, 0, 0, -1, 0, 0, 0]
            and cap_packet["primitive_epsilon"] == -1
            and cap_ledger["coefficient_projector"][
                "scalar_zero_face_after_rational_normalization"] == "90*f(x)",
            "the primitive cap signature changed")

    # Small direct-sum quotient: (pointed conormal, Q boundary, scalar ores).
    # P_f and p are independent.  The invisible cap lift n is also distinct;
    # ordinary residue separates p from P_f and n.
    p_f = (Q(1), Q(0), Q(0))
    p = (Q(0), Q(-1), Q(-1))
    n = (Q(0), Q(1), Q(0))
    pointed_dual = (Q(1), Q(0), Q(0))
    residue_dual = (Q(0), Q(0), Q(1))
    require(rank((p_f, p)) == 2 and rank((p_f, p, n)) == 3
            and dot(pointed_dual, p_f) == 1
            and dot(pointed_dual, p) == dot(pointed_dual, n) == 0
            and dot(residue_dual, p) == -1
            and dot(residue_dual, p_f) == dot(residue_dual, n) == 0,
            "P_f, p, and n stopped being independent")

    orbit = load(
        "computations/verify_h2_p2_one_root_private_orbit_bright_dark_gate.py",
        "pointed_cap_orbit",
    )
    orbit_ledger, orbit_digest = orbit.audit()
    require(orbit_digest == orbit.EXPECTED_LEDGER_SHA256,
            "the eight-private orbit ledger changed")
    literal = orbit_ledger["literal_packet"]
    covariance = orbit_ledger["marked_packet_covariance"]
    require(literal["private_rank_mod_complete_rows"] == 8
            and covariance["site_root_stabilizer_size"] == 1
            and not covariance["one_seed_spans_fixed_packet"],
            "the fixed marked-packet covariance gate changed")

    # q23 multiplication preserves each word block.  One fixed section gives
    # one combined (q,dq) column; eight functorial instantiations give eight
    # independent columns.  It doubles the face data, not the word coverage.
    eight = tuple(unit(index, 8) for index in range(8))
    q_dq_columns = tuple(column + column for column in eight)
    require(rank(eight) == rank(q_dq_columns) == 8
            and rank((q_dq_columns[0],)) == 1,
            "q23 functoriality changed the fixed-word coverage rank")

    target = load(
        "computations/verify_h2_lower_0112_bminus4_target_normal_gate.py",
        "pointed_cap_target",
    )
    target_ledger, target_digest = target.audit()
    require(target_digest == target.EXPECTED_LEDGER_SHA256,
            "the P2 target-normal ledger changed")
    centered_target = target_ledger["centered_preimage_normal"]
    marked_target = target_ledger["marked_local_normal"]
    require(not centered_target["target_normal_zero"]
            and centered_target["primitive_mixed_dual_value"] == 2
            and marked_target["primitive_cap_target"] == 0,
            "the target-normal/p cap separation changed")

    private = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "pointed_cap_reinsertion",
    )
    private_ledger, private_digest = private.audit()
    require(private_digest == private.EXPECTED_LEDGER_SHA256,
            "the private reinsertion ledger changed")
    z = tuple(map(Q, private_ledger[
        "second_even_Bminus4_debt"]["preimage"]))
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(len(z)))
    require(sum(z, Q(0)) == 0 and dot(detector, z) == Q(35, 72),
            "the representative dq23 coefficient changed")

    # Strongest possible formal labelwise use of p: assign one p copy to each
    # occurrence coefficient z_i.  Its Q=-1 face cancels +dq23*z if (and only
    # if) an occurrence-to-Q label map is granted.  The same p copies leave
    # labelled ores=-z.  Scalar ores sees its sum, which is zero, while the
    # primitive occurrence detector remains nonzero.  The existing p theorem
    # provides only scalar ores, not this labelled section.
    dq_face = z
    p_q_face = scale(-1, z)
    p_labelled_ores = scale(-1, z)
    require(add(dq_face, p_q_face) == (Q(0),) * len(z)
            and sum(p_labelled_ores, Q(0)) == 0
            and dot(detector, p_labelled_ores) == Q(-35, 72),
            "the best-case labelled p/reinsertion residue changed")

    ledger = {
        "theorem": "pointed occurrence / primitive p / P2 propagation gate",
        "pins": PINS,
        "pointed_occurrence_generator": {
            "name": "P_f",
            "degree_zero_relation": "u_f-u",
            "conormal": "d(u_f-u)",
            "universal_graph_constructs_f_minus_u_f": True,
            "universal_graph_constructs_u_f_minus_u": False,
            "old_conormal_rank": 3,
            "rank_after_adjoining_P_f": 4,
            "adding_derived_diagonal_preserves_old_classical_fibre": False,
        },
        "primitive_cap_generator": {
            "name": "p_(v,N)",
            "full_word": cap_packet["full_source_word"],
            "fine_repeated_grade": cap_packet["first_common_fine_degree"],
            "row_order": cap_packet["row_order"],
            "signature": cap_packet["required_augmented_signature"],
            "Q": -1,
            "scalar_ores": -1,
            "target": 0,
            "protected_rows": 0,
            "epsilon": -1,
            "normalized_scalar_top": "90*f(x)",
            "physical_source_lift_constructed": False,
        },
        "P_f_vs_p": {
            "same_literal_generator": False,
            "quotient_rows": ["pointed conormal", "Q boundary", "scalar ores"],
            "P_f": [1, 0, 0],
            "p": [0, -1, -1],
            "invisible_n": [0, 1, 0],
            "rank_P_f_p": 2,
            "rank_P_f_p_n": 3,
            "separators": {
                "marked_tangent": "detects P_f, kills p and n",
                "ordinary_residue": "detects p, kills P_f and n",
            },
            "compatible_positive_interpretation": (
                "P_f and p may be two faces/domain generators of one enriched "
                "pointed total comparison, but identifying them is false"
            ),
        },
        "eight_private_squares": {
            "fixed_packet_private_rank": 8,
            "fixed_marked_site_root_stabilizer": "identity",
            "one_literal_p_section_spans_all_eight": False,
            "q23_multiplication_changes_word_coverage_rank": False,
            "rank_one_fixed_section_after_q_dq": 1,
            "rank_eight_instantiations_after_q_dq": 8,
            "positive_schema": (
                "one universal pointed-cap theorem natural in the marked "
                "occurrence and every ordered root pair can instantiate all "
                "eight sections; this is a family, not one fixed column"
            ),
        },
        "augmented_face_order": {
            "aggregate_top": (
                "the centered coefficient has occurrence augmentation zero "
                "but scalar zero-face 90*f(x) at response order three"
            ),
            "pointed_cap": "d(u_f-u), independent of the p projection",
            "direct_root_edge_target": {
                "p_target": 0,
                "centered_P2_target_normal_zero": False,
                "primitive_target_dual": "X_0011^*",
                "dual_value": 2,
                "first_missing_augmented_row_before_full_square": (
                    "occurrence-local mixed-target cone and its one-endpoint "
                    "Hasse cross face"
                ),
            },
            "full_labelled_square_target_commutator": 0,
            "reinsertion": "d(q23*S)=q23*dS+dq23*S",
            "representative_z_private_augmentation": 0,
            "representative_labelled_detector": "35/72",
            "best_case_same_label_p_Q_plus_dq": 0,
            "best_case_remaining_labelled_p_ores_detector": "-35/72",
            "scalar_ores_on_remaining_labelled_packet": 0,
            "next_missing_augmented_row_after_target_square": (
                "an occurrence-labelled Q/ores section and the physical "
                "occurrence-to-Q comparison; scalar p/ores does not define it"
            ),
        },
        "verdict": (
            "The graph conormal P_f and primitive cap p are complementary, "
            "not identical.  The universal graph does not make P_f a boundary "
            "on the old physical fibre, and one fixed p cannot span the eight "
            "private word blocks.  A universal enriched family could supply "
            "them, but it must include the mixed-target proper faces and an "
            "occurrence-labelled Q/ores reinsertion law; the current scalar p "
            "does neither"
        ),
        "scope": (
            "exact conormal/cap quotients, exact eight-word private rank, and "
            "the representative 0102 first-PP coefficient.  The best-case "
            "same-label cancellation is conditional on the unconstructed "
            "occurrence-to-Q map and is not asserted as a physical chain"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("pointed-cap propagation gate changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("P_f=d(u_f-u) versus p=(-Q,-ores): INDEPENDENT")
    print("universal graph makes P_f physical boundary: NO")
    print("one literal p spans eight fixed private words: NO")
    print("direct edge first residual: MIXED TARGET")
    print("after full square: LABELLED Q/ORES, detector -35/72")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
