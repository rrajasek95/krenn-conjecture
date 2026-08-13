#!/usr/bin/env python3
"""Test the tau_plus repair against the denominator-Tor companion family.

In the canonical faces-(3,5) target component, the denominator route has an
exact tail-level realization of the two deficient columns:

  face 3, multiplier 34, matching 14|25 -> B4,
  face 5, multiplier 45, matching 13|24 -> B1.

Both have repeated target site 4.  The selected C5 matching on either face
lands on B0.  Therefore a selected reduced companion A_3 or A_5, followed by
an ordinary matching-Bianchi difference, would construct the corresponding
off-cycle companion without changing protected readouts.  Half their sum
has tail -(B1+B4)/2; its negative has the desired positive tail.

This conditional construction is excluded on the exact clean C5 slice.  Its
selected projection y=(e3+e5)/2 has aggregate one, whereas the literal reset-
word coordinate of every denominator kernel imposes sum_v y_v=0 when all
h_v=1.  Rho-evenizing across the transformed C5 chart preserves aggregate
one.  Moreover -A has readouts (tail,target,ainc,ores)=(1,0,0,1), while a
pure r0 repair has (1,1,-1,0); a target/anchor/residue cone correction is
still required even off the clean slice.

Thus the A_vN family identifies the correct tails and repeated target grade,
but it neither exists with the required clean selected projection nor alone
has the tau_plus protected signature.  Beta=0 remains independent.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py":
        "645df036367a7fe60f3ce625dc37710f7e83129a84a3619005945ca6b4f0a486",
    "computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py":
        "b1d1a62d229d9ebb3d20abbc7359503af08506fec882f629ee95a886c58490a8",
    "computations/verify_h3_component_iv_reduced_companion_tor_gate.py":
        "5bf7e0960b413c4e5d587b3c8f46d51493010bb73413682d7705bb28070d0935",
    "computations/verify_h3_rootless_c5_clean_aggregate_tor_separator.py":
        "3b5cb07412f08eaea2492d4b4f981ecc5618053c211942bead0512b30393ce67",
    "computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py":
        "4f691d119469e76436e36566a1ca7307bc49a52f66b0687c1554a9e6531ec4de",
    "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py":
        "bd20b6320172f846d7c4aa38ec6ebba0c0cfea4c056b8758df19d31b5ab20231",
}
EXPECTED_LEDGER_SHA256 = (
    "a980f6b0ee0054b418a97b3b3176ccc4977e0a3eee4c8ebec6ee0000b82e432c"
)


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


def add(*vectors):
    return tuple(sum(Q(vector[index]) for vector in vectors)
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def site_profile(edges, sites=(1, 2, 3, 4, 5)):
    counts = {site: 0 for site in sites}
    for left, right in edges:
        counts[left] += 1
        counts[right] += 1
    return tuple(counts[site] for site in sites)


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    scope = load(
        "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py",
        "even_tor_scope",
    )
    ridge = load(
        "computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py",
        "even_tor_ridge",
    )
    pp = load(
        "computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py",
        "even_tor_pp",
    )
    shared = load(
        "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py",
        "even_tor_shared",
    )
    reduced = shared.load(
        "computations/verify_h3_residual_q_reduced_eq_cap_factorization.py",
        "even_tor_reduced",
    )
    support = scope.load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "even_tor_support",
    )
    complete = scope.load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "even_tor_complete",
    )
    base = scope.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "even_tor_base",
    )

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    pure_graphs = tuple(support.graph(multiplier)
                        for multiplier, _boundary in pure)
    graph_index = {graph: index for index, graph in enumerate(pure_graphs)}
    require((left, right) == (3, 5) and len(graph_index) == 6,
            "the canonical faces-(3,5) target changed")

    # Enumerate all thirty adjacent-face denominator tails.  Exactly the six
    # routes in the faces-(3,5) pair land in this canonical component.
    route_records = []
    canonical_routes = []
    for position, left_face in enumerate(ridge.FACE_ORDER):
        right_face = ridge.FACE_ORDER[(position + 1) % 5]
        for face, other in ((left_face, right_face),
                            (right_face, left_face)):
            multiplier = ridge.FIRST_TOR_MULTIPLIERS[
                (left_face, right_face)
            ][(face, other)]
            for matching in ridge.perfect_matchings(
                    tuple(site for site in ridge.ODD if site != face)):
                graph = tuple(sorted(matching + (multiplier,)))
                target = graph_index.get(graph)
                record = {
                    "face_pair": [left_face, right_face],
                    "route_face": face,
                    "other_face": other,
                    "multiplier": list(multiplier),
                    "matching": [list(edge) for edge in matching],
                    "target_B": target,
                    "site_profile": list(site_profile(graph)),
                }
                route_records.append(record)
                if target is not None:
                    canonical_routes.append(record)
    require(len(route_records) == 30 and len(canonical_routes) == 6,
            "the denominator/canonical target intersection changed")
    require([record["target_B"] for record in canonical_routes]
            == [0, 4, 5, 0, 1, 2],
            "the six canonical denominator tails changed")

    desired_b4 = next(record for record in canonical_routes
                      if record["target_B"] == 4)
    desired_b1 = next(record for record in canonical_routes
                      if record["target_B"] == 1)
    require(desired_b4 == {
                "face_pair": [3, 5], "route_face": 3, "other_face": 5,
                "multiplier": [3, 4], "matching": [[1, 4], [2, 5]],
                "target_B": 4, "site_profile": [1, 1, 1, 2, 1],
            } and desired_b1 == {
                "face_pair": [3, 5], "route_face": 5, "other_face": 3,
                "multiplier": [4, 5], "matching": [[1, 3], [2, 4]],
                "target_B": 1, "site_profile": [1, 1, 1, 2, 1],
            },
            "the B1/B4 denominator routes changed")

    selected_matchings, _inventory = pp.specialized_denominator_inventory()
    selected_face3 = tuple(sorted(selected_matchings[3]
                                  + (tuple(desired_b4["multiplier"]),)))
    selected_face5 = tuple(sorted(selected_matchings[5]
                                  + (tuple(desired_b1["multiplier"]),)))
    require(graph_index[selected_face3] == graph_index[selected_face5] == 0,
            "the selected face-3/5 denominator tails stopped landing on B0")

    # Exact matching-Bianchi transport.  R_N=(-Omega,+Q_N;ores=1), so
    # R_N-R_sel=(Q_N-Q_sel;ores=0).  If A_sel=(-Q_sel;ores=-1), then
    # A_N=A_sel-(R_N-R_sel)=(-Q_N;ores=-1).
    # Tail coordinates are (B0,...,B5); append ores as coordinate 6.
    selected_a = scale(-1, scope.unit(0)) + (Q(-1),)
    b4_difference = add(scope.unit(4), scale(-1, scope.unit(0))) + (Q(0),)
    b1_difference = add(scope.unit(1), scale(-1, scope.unit(0))) + (Q(0),)
    a_b4 = add(selected_a, scale(-1, b4_difference))
    a_b1 = add(selected_a, scale(-1, b1_difference))
    require(a_b4 == scale(-1, scope.unit(4)) + (Q(-1),)
            and a_b1 == scale(-1, scope.unit(1)) + (Q(-1),),
            "matching-Bianchi transport stopped constructing off-cycle A tails")
    even_a = scale(Q(1, 2), add(a_b1, a_b4))
    desired_tail_with_ores = (
        Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0), Q(0)
    )
    require(scale(-1, even_a)[:-1] == desired_tail_with_ores[:-1]
            and scale(-1, even_a)[-1] == 1,
            "the even A companion stopped giving the desired tail with ores defect")

    # Selected face projection.  Direct conditional construction uses
    # y=(e3+e5)/2.  Target involution s=(2 5) fixes face 3 and exchanges
    # faces 2,5; averaging with the transformed chart gives
    # y_even=(e3)/2+(e2+e5)/4.  Both have aggregate one.
    face_order = (1, 2, 3, 4, 5)
    y = tuple(Q(1, 2) if face in (3, 5) else Q(0)
              for face in face_order)
    s_face = {1: 1, 2: 5, 3: 3, 4: 4, 5: 2}
    sy = tuple(y[face_order.index(s_face[face])] for face in face_order)
    y_even = scale(Q(1, 2), add(y, sy))
    require(y == (Q(0), Q(0), Q(1, 2), Q(0), Q(1, 2))
            and sy == (Q(0), Q(1, 2), Q(1, 2), Q(0), Q(0))
            and y_even == (Q(0), Q(1, 4), Q(1, 2), Q(0), Q(1, 4))
            and sum(y) == sum(y_even) == 1,
            "the candidate/evenized selected projections changed")
    h_clean = (Q(1),) * 5
    require(sum(a * b for a, b in zip(h_clean, y, strict=True)) == 1
            and sum(a * b for a, b in zip(h_clean, y_even, strict=True)) == 1,
            "the clean reset-word obstruction vanished")

    # Universal weighted obstruction off the clean slice.
    weighted_direct = "(h_3+h_5)/2=0"
    weighted_even = "h_3/2+(h_2+h_5)/4=0"

    # Protected rows.  The exact reduced companion A has (-Q,ores=-1)
    # and zero target/ainc.  Negation corrects the Q-tail but has ores +1.
    # A pure r0 target unit has target 1, ainc -1, ores 0.
    row_order = ("tail_augmentation", "target", "ainc", "ores")
    minus_a_signature = (Q(1), Q(0), Q(0), Q(1))
    required_signature = (Q(1), Q(1), Q(-1), Q(0))
    signature_defect = add(required_signature, scale(-1, minus_a_signature))
    require(signature_defect == (Q(0), Q(1), Q(-1), Q(-1))
            and reduced.R0[:2] == (1, -1),
            "the A versus pure-r0 protected signature changed")

    ledger = {
        "theorem": "tau_plus even repair versus denominator-Tor transgression",
        "pins": PINS,
        "canonical_denominator_tail_inventory": {
            "all_adjacent_face_routes": len(route_records),
            "routes_in_faces_3_5_target_component": canonical_routes,
            "target_sequence": [record["target_B"]
                                for record in canonical_routes],
            "desired_B4_route": desired_b4,
            "desired_B1_route": desired_b1,
            "both_desired_routes_repeated_target_site": 4,
        },
        "conditional_selected_transgression_construction": {
            "selected_face3_matching": [list(edge)
                                         for edge in selected_matchings[3]],
            "selected_face5_matching": [list(edge)
                                         for edge in selected_matchings[5]],
            "both_selected_targets": "B0",
            "matching_Bianchi_formula": (
                "A_(v,N)=A_(v,Nsel)-(R_(v,N)-R_(v,Nsel))"
            ),
            "result": (
                "selected A3,A5 transgressions conditionally construct "
                "A_(3,14|25)=-B4 and A_(5,13|24)=-B1"
            ),
            "half_sum_negative_tail": "(B1+B4)/2",
        },
        "selected_projection_obstruction": {
            "direct_y_faces_1_to_5": [str(value) for value in y],
            "rho_transformed_y": [str(value) for value in sy],
            "rho_evenized_y": [str(value) for value in y_even],
            "direct_aggregate": str(sum(y)),
            "evenized_aggregate": str(sum(y_even)),
            "universal_weighted_condition_direct": weighted_direct,
            "universal_weighted_condition_evenized": weighted_even,
            "clean_C5_h": [1, 1, 1, 1, 1],
            "clean_reset_word_value_direct": 1,
            "clean_reset_word_value_evenized": 1,
            "denominator_kernel_exists_on_clean_C5": False,
            "reason": (
                "the literal selected reset-word coordinate imposes "
                "sum_v h_v*y_v=0 on every denominator kernel"
            ),
        },
        "protected_signature_obstruction": {
            "row_order": list(row_order),
            "negative_A_even_companion": [int(value)
                                           for value in minus_a_signature],
            "required_pure_r0_repair": [int(value)
                                         for value in required_signature],
            "remaining_defect": [int(value) for value in signature_defect],
            "needs": (
                "an independent same-grade target/anchor/residue cone "
                "correction even where the denominator kernel exists"
            ),
        },
        "beta_zero": {
            "status": "separate",
            "reason": (
                "the denominator tail calculation is on the generic trace "
                "comparison and does not supply the selected D0 unary jet"
            ),
        },
        "verdict": (
            "the reduced companion family contains exactly the two target "
            "tails B1 and B4 after matching-Bianchi transport, in the right "
            "repeated target-site grade.  But the required selected "
            "projection has aggregate one and is impossible on the clean "
            "C5 slice; off that slice it remains conditional on weighted "
            "denominator membership and still has a primitive protected "
            "target/anchor/residue mismatch"
        ),
        "nonclaims": [
            "the conditional A_vN tails are not declared source cells",
            "rho-even target invariance is not a proof of source-chart covariance",
            "the odd labelled-ores transgression is not identified with the even pure-r0 repair",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("even repair denominator-Tor ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 tau_plus even repair / denominator-Tor gate: PASS")
    print("exact conditional tails: face3 -> B4, face5 -> B1")
    print("matching-Bianchi transport from selected B0: exact")
    print("clean C5 selected projection aggregate: 1, hence obstructed")
    print("-A protected defect: target +1, ainc -1, ores -1 still needed")
    print("beta=0: separate D0 obligation")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
