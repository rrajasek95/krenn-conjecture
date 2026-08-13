#!/usr/bin/env python3
"""Decompose the L01 endpoint PP face and compare the C-plus inventory.

The 18 endpoint/direction terms of dL01 are

    (six marked-edge flags of K4) tensor (three tail matchings).

The tail sum is trivial.  On the six K4 edges the primitive coefficient is

    v_A=(2,2,-1,-1,-1,-1),

with the two 2's on the opposite edges of the selected matching A.  Its S4
orbit has three vectors, rank two and sum zero: it is the [2,2] irreducible.
Full endpoint-choice S4 coinvariants vanish.  The honest fixed-chart
stabilizer of A has one coinvariant, represented by v_A.

The endpoint-odd Cartan line is v_B-v_C and the objectwise K_Eq line is
constant/zero in this flag module; together they do not span v_A.  On the
other hand the h=2 B-4/C-plus coefficient D6 transports exactly to v_A.
Thus the formal endpoint-even C-plus cell is the unique correct coefficient
repair.  Its source-valid restriction/reinsertion map is explicitly still
open, so this is a conditional construction, not an existing physical span.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "notes/h3-h2-l01-three-cap-first-pp-curvature-gate.md":
        "d43b196a448045b9cf40a9537e5a30d9aad658a9c8636047052a023b45c4db7f",
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "notes/h2-b4-cplus-shared-interface-gate.md":
        "4c89253c18f4475371849a78c990e27b7d6af79193522cd5a583af80cc929fb8",
    "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py":
        "09ba792f229bb3a1e930b2c59b0de2356b08a7434c648aad9573d8382c652a52",
    "notes/h2-lower-even-cartan-jstar-target-cone-gate.md":
        "2f80cf6fa8d87a9acc4f3441bba5753b9b3c7de5c19e6c709d75969b7eb9d381",
    "computations/verify_h3_centered_shear_cylinder_curvature_physical_output_gate.py":
        "12f68bfbe0f320486992e943959be1bf516c1b1458e2a59b457f92d1a57d2d39",
    "notes/h3-centered-shear-cylinder-curvature-physical-output-gate.md":
        "a16ee3c67f562ddde475446aac52fa080fa5d1cc843435cca8669705f5f9bcdf",
    "computations/verify_h3_cylinder_theta_groupoid_frontier_correction.py":
        "3cdd19a68f0acafb975cb3d8d1660aaabde485af5aacb4672cb1fe2e5febe2cb",
    "notes/h3-cylinder-theta-groupoid-frontier-correction.md":
        "631caffa650b43eec817a8daa6588ee65618971c9f353fbda5c3623fd9b44a66",
    "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py":
        "bc35781e0f57bbd1202711e2dc818417d76fa87c69e33d3d4b01540e06865557",
    "notes/h3-h2-full-site-chart-swap-pointed-scalar-guard.md":
        "77771f8eee2a4bbaeb5a9575961efb9c7728833e28bca86d33102806aeffa6c2",
}
EXPECTED_LEDGER_SHA256 = (
    "848eba1faff0a945357fef62e9cb964a2d71b80535f1d26c41277dd82a58d6d0"
)

Edge = tuple[int, int]
Vector = tuple[Q, ...]

# The selected matching is A={01,23}.  B={02,13}, C={03,12}.
EDGES: tuple[Edge, ...] = ((0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2))
A_MATCHING = frozenset(((0, 1), (2, 3)))
V_A: Vector = tuple(map(Q, (2, 2, -1, -1, -1, -1)))
V_B: Vector = tuple(map(Q, (-1, -1, 2, 2, -1, -1)))
V_C: Vector = tuple(map(Q, (-1, -1, -1, -1, 2, 2)))
ODD_BC: Vector = tuple(left - right for left, right in
                       zip(V_B, V_C, strict=True))
CONSTANT: Vector = (Q(1),) * 6


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


def rank(columns: tuple[Vector, ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
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


def dot(left: Vector, right: Vector) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def permute_edge(edge: Edge, permutation: tuple[int, ...]) -> Edge:
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def act(vector: Vector, permutation: tuple[int, ...]) -> Vector:
    answer = [Q(0)] * len(EDGES)
    position = {edge: index for index, edge in enumerate(EDGES)}
    for index, edge in enumerate(EDGES):
        answer[position[permute_edge(edge, permutation)]] = vector[index]
    return tuple(answer)


def subtract(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def representation_audit() -> dict[str, object]:
    permutations = tuple(itertools.permutations(range(4)))
    orbit = tuple(sorted({act(V_A, permutation)
                          for permutation in permutations}))
    require(set(orbit) == {V_A, V_B, V_C}
            and rank(orbit) == 2
            and tuple(sum(entries, Q(0))
                      for entries in zip(*orbit, strict=True)) == (Q(0),) * 6,
            "the S4 orbit of the chart character changed")

    # Edge permutation Q^6 decomposes as 1 + [3,1] + [2,2].  V_A has zero
    # total and zero incidence sum at each vertex, so it lies in [2,2].
    vertex_incidence = tuple(tuple(Q(vertex in edge) for edge in EDGES)
                             for vertex in range(4))
    require(rank(vertex_incidence) == 4
            and dot(CONSTANT, V_A) == 0
            and all(dot(row, V_A) == 0 for row in vertex_incidence)
            and 6 - rank(vertex_incidence) == 2,
            "the [2,2] characterization changed")

    matching_stabilizer = tuple(
        permutation for permutation in permutations
        if frozenset(permute_edge(edge, permutation) for edge in A_MATCHING)
           == A_MATCHING
    )
    require(len(matching_stabilizer) == 8
            and all(act(V_A, permutation) == V_A
                    for permutation in matching_stabilizer),
            "the selected-matching stabilizer changed")

    basis = (V_A, V_B)
    full_relations = tuple(
        subtract(act(vector, permutation), vector)
        for permutation in permutations for vector in basis
    )
    matching_stabilizer_relations = tuple(
        subtract(act(vector, permutation), vector)
        for permutation in matching_stabilizer for vector in basis
    )
    require(rank(full_relations) == 2
            and rank(matching_stabilizer_relations) == 1,
            "the full/fixed coinvariant ranks changed")

    # In the fixed physical response chart, the two root/direction vertices
    # and the two endpoint vertices are not interchangeable.  The physical
    # root transpose and endpoint transpose generate C2 x C2, a subgroup of
    # the matching stabilizer.  It fixes V_A and contracts only V_B-V_C.
    endpoint_transpose = (1, 0, 2, 3)
    residual_transpose = (0, 1, 3, 2)
    fixed_chart_group = (
        (0, 1, 2, 3), endpoint_transpose, residual_transpose,
        tuple(endpoint_transpose[residual_transpose[index]]
              for index in range(4)),
    )
    fixed_chart_relations = tuple(
        subtract(act(vector, permutation), vector)
        for permutation in fixed_chart_group for vector in basis
    )
    require(act(V_A, endpoint_transpose) == V_A
            and act(V_A, residual_transpose) == V_A
            and act(ODD_BC, endpoint_transpose) == tuple(-entry
                                                         for entry in ODD_BC)
            and act(ODD_BC, residual_transpose) == tuple(-entry
                                                         for entry in ODD_BC)
            and len(set(fixed_chart_group)) == 4
            and rank(fixed_chart_relations) == 1,
            "the endpoint parity split changed")

    # The other S4 is the honest stabilizer acting on the four spectator
    # sites.  It permutes their three perfect matchings.  The packet uses the
    # invariant tail sum, so this action creates no further relation on V_A.
    tail_matchings = (
        frozenset(((0, 1), (2, 3))),
        frozenset(((0, 2), (1, 3))),
        frozenset(((0, 3), (1, 2))),
    )
    tail_position = {matching: index
                     for index, matching in enumerate(tail_matchings)}
    tail_actions = []
    for permutation in permutations:
        image = []
        for matching in tail_matchings:
            moved = frozenset(permute_edge(edge, permutation)
                              for edge in matching)
            image.append(tail_position[moved])
        tail_actions.append(tuple(image))
    require(len(set(tail_actions)) == 6,
            "the tail S4 stopped inducing S3")
    tail_sum = (Q(1), Q(1), Q(1))
    require(all(tuple(tail_sum[index] for index in action) == tail_sum
                for action in tail_actions),
            "the tail sum stopped being S4 invariant")
    tensor = tuple(value * tail for value in V_A for tail in tail_sum)
    require(len(tensor) == 18 and rank((tensor,)) == 1
            and sum(tensor, Q(0)) == 0,
            "the invariant tail tensor changed")
    return {
        "six_edge_order": [repr(edge) for edge in EDGES],
        "selected_matching": [repr(edge) for edge in sorted(A_MATCHING)],
        "primitive_chart_vector": [str(value) for value in V_A],
        "S4_orbit": [[str(value) for value in vector] for vector in orbit],
        "S4_orbit_size": len(orbit),
        "S4_orbit_rank": rank(orbit),
        "irreducible": "the two-dimensional [2,2] summand of Q[K4 edges]",
        "abstract_direction_vertex_S4_relation_rank": rank(full_relations),
        "abstract_direction_vertex_S4_coinvariant_dimension": (
            2 - rank(full_relations)
        ),
        "selected_matching_stabilizer_order": len(matching_stabilizer),
        "matching_stabilizer_relation_rank": rank(
            matching_stabilizer_relations
        ),
        "matching_stabilizer_coinvariant_dimension": (
            2 - rank(matching_stabilizer_relations)
        ),
        "physical_fixed_chart_group": "C2_endpoint x C2_root",
        "physical_fixed_chart_group_order": len(fixed_chart_group),
        "physical_fixed_chart_relation_rank": rank(fixed_chart_relations),
        "physical_fixed_chart_coinvariant_dimension": (
            2 - rank(fixed_chart_relations)
        ),
        "fixed_chart_survivor": [str(value) for value in V_A],
        "endpoint_parity": "V_A even; V_B-V_C odd",
        "spectator_tail_S4_image_order": len(set(tail_actions)),
        "tail_representation": "S4-invariant sum of three tail matchings",
        "eighteen_term_representation": "[2,2] tensor trivial_tail",
    }


def candidate_span_audit() -> dict[str, object]:
    # The actual committed endpoint-odd line and objectwise central line do
    # not span the endpoint-even [2,2] survivor.
    require(rank((CONSTANT, ODD_BC)) == 2
            and rank((CONSTANT, ODD_BC, V_A)) == 3,
            "the old odd/central span changed")
    primitive_dual = tuple(value / dot(V_A, V_A) for value in V_A)
    require(dot(primitive_dual, V_A) == 1
            and dot(primitive_dual, CONSTANT) == 0
            and dot(primitive_dual, ODD_BC) == 0,
            "the primitive fixed-chart dual changed")

    # Transport the exact h=2 hole order into the K4 edge order.  The D6
    # vector has coefficient 2 on the opposite holes 01 and 23.
    h2_hole_order = ((0, 2), (0, 1), (0, 3), (1, 3), (2, 3), (1, 2))
    d6_in_h2_order = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    d6_by_edge = dict(zip(h2_hole_order, d6_in_h2_order, strict=True))
    d6_in_edge_order = tuple(d6_by_edge[edge] for edge in EDGES)
    require(d6_in_edge_order == V_A,
            "the B-4/C-plus coefficient stopped being the chart vector")
    delta_plus = tuple(value / Q(4) for value in d6_in_edge_order)
    require(rank((CONSTANT, ODD_BC, delta_plus)) == 3,
            "the conditional C-plus repair stopped spanning the survivor")
    return {
        "committed_endpoint_odd_shadow": [str(value) for value in ODD_BC],
        "objectwise_K_Eq_flag_shadow": (
            "zero on the six occurrence flags (or the constant line before "
            "projection); no [2,2] component"
        ),
        "rank_odd_plus_central": rank((CONSTANT, ODD_BC)),
        "rank_after_chart_survivor": rank((CONSTANT, ODD_BC, V_A)),
        "primitive_survivor_dual": [str(value) for value in primitive_dual],
        "dual_on_constant": str(dot(primitive_dual, CONSTANT)),
        "dual_on_endpoint_odd": str(dot(primitive_dual, ODD_BC)),
        "dual_on_chart_survivor": str(dot(primitive_dual, V_A)),
        "h2_D6_hole_order": [repr(edge) for edge in h2_hole_order],
        "h2_D6": [str(value) for value in d6_in_h2_order],
        "transported_D6": [str(value) for value in d6_in_edge_order],
        "equals_L01_direction_primitive": True,
        "conditional_C_plus_lower_landing": [str(value) for value in delta_plus],
        "coefficient_span_after_C_plus": True,
    }


def physical_inventory_audit() -> dict[str, object]:
    shared = load(
        "computations/verify_h2_b4_cplus_shared_interface_gate.py",
        "l01_cplus_shared",
    )
    shared_ledger, shared_digest = shared.audit()
    require(shared_digest == shared.EXPECTED_LEDGER_SHA256,
            "the B-4/C-plus interface changed")
    interface = shared_ledger["full_interface_and_typing"]
    coefficient = shared_ledger["even_hole_and_tau_debt"]
    require(coefficient["D6"] == [-1, 2, -1, -1, 2, -1]
            and interface["coefficient_projection_agrees"]
            and not interface["physical_restriction_reinsertion_map_constructed"],
            "the conditional C-plus status changed")

    even = load(
        "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py",
        "l01_even_spencer",
    )
    even_ledger, even_digest = even.audit()
    require(even_digest == even.EXPECTED_LEDGER_SHA256,
            "the endpoint-even Cartan/Spencer gate changed")
    even_scope = even_ledger["physical_scope"]
    require(even_scope["physical_comparison_missing"],
            "the endpoint-even physical placement unexpectedly closed")

    shear = load(
        "computations/verify_h3_centered_shear_cylinder_curvature_physical_output_gate.py",
        "l01_keq_objectwise",
    )
    shear_ledger, shear_digest = shear.audit()
    require(shear_digest == shear.EXPECTED_LEDGER_SHA256
            and shear_ledger["transpose_groupoid_compression"]
                ["central_K_Eq_is_objectwise"],
            "the K_Eq objectwise theorem changed")

    chart = load(
        "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py",
        "l01_chart_reset",
    )
    chart_ledger, chart_digest = chart.audit()
    require(chart_digest == chart.EXPECTED_LEDGER_SHA256,
            "the endpoint-chart reset theorem changed")
    chart_audit = chart_ledger["literal_audit"]
    require(chart_audit["fixed_pointed_source_guard"]
                ["retained_chart_bar_boundary"] == 0
            and chart_audit["target_and_first_proper_face"]
                ["proper_face_occurrence_support"] == 9
            and chart_audit["target_and_first_proper_face"]
                ["proper_face_target_augmentation"] == "0"
            and "2 D q01-p0 s1-p1 s0" in
                chart_audit["target_and_first_proper_face"]
                    ["first_nonzero_proper_face"],
            "the pointed L01 chart face changed")
    return {
        "pinned_B4_Cplus_interface": shared_digest,
        "pinned_even_Spencer_Cartan": even_digest,
        "pinned_objectwise_K_Eq": shear_digest,
        "pinned_chart_reset_guard": chart_digest,
        "coefficient_verdict": (
            "YES: the transported D6/C-plus lower coefficient is exactly "
            "the primitive L01 endpoint flag vector"
        ),
        "physical_verdict": (
            "NO CURRENT SPAN: the C-plus restriction/reinsertion map and its "
            "P2 placement are explicitly conditional; endpoint-odd Cartan "
            "and objectwise K_Eq miss the fixed-chart [2,2] coinvariant"
        ),
        "C_plus_required_faces": {
            "parity": interface["C_plus_parity"],
            "upper_target": interface["C_plus_upper_target"],
            "complete_lower": interface["C_plus_complete_lower_landing"],
            "reduced_Eq": interface["C_plus_reduced_Eq_face"],
            "ordinary_residue": interface["C_plus_labelled_ordinary_residue"],
            "next_boundary": interface["next_Cartan_Hasse_boundary"],
        },
        "monoidal_h3_requirement": (
            "tensor the endpoint-even D6 cell with the invariant three-term "
            "tail H2345; its spectator Leibniz face is exactly the 18-term "
            "tail half already isolated in 2acaf90"
        ),
        "K_Eq_role": (
            "supplies the reduced-Eq correction objectwise after the C-plus "
            "placement; it cannot create the [2,2] occurrence coefficient"
        ),
        "Maschke_physicality": {
            "spectator_tail_S4": (
                "physical but fixes the invariant three-tail sum"
            ),
            "root_endpoint_fixed_chart_group": (
                "contracts the odd V_B-V_C line but fixes V_A"
            ),
            "abstract_direction_vertex_S4": (
                "has zero [2,2] coinvariants only after maps exchanging an "
                "endpoint direction with a residual direction"
            ),
            "same_three_cap_object": "does not contract V_A",
            "chart_changing_contraction": (
                "leaves the pointed graph face L01; its first PP face is "
                "the present dL01 packet, so using it here is circular"
            ),
            "new_independent_scalar": False,
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 L01 endpoint-flag S4 / C-plus span gate",
        "pins": PINS,
        "representation": representation_audit(),
        "candidate_span": candidate_span_audit(),
        "physical_inventory": physical_inventory_audit(),
        "verdict": (
            "The 18 endpoint/direction terms form [2,2] of the four direction "
            "vertices tensored with the S4-invariant three-tail sum.  The "
            "abstract direction-vertex S4 has zero coinvariants, but the "
            "honest fixed-chart root/endpoint group leaves exactly the line "
            "v_A=(2,2,-1,-1,-1,-1).  "
            "Endpoint-odd Cartan and objectwise K_Eq do not span it.  The "
            "transported h=2 B-4/C-plus vector D6 equals v_A exactly, so the "
            "formal endpoint-even Spencer/C-plus family is the unique correct "
            "coefficient repair.  Its source-labelled restriction/reinsertion "
            "and P2 placement remain unconstructed; K_Eq supplies only the "
            "subsequent reduced-Eq face.  Maschke contraction within the "
            "three-cap object does not remove v_A; enlarging to the chart-"
            "changing S4 leaves the already known pointed scalar L01 and is "
            "therefore circular at dL01."
        ),
        "shortest_positive_theorem": (
            "construct the physical endpoint-even C-plus/P2 cell for D6 and "
            "extend it monoidally over H2345.  The D6 top cancels the sole "
            "fixed-chart endpoint coinvariant, its tail Leibniz term matches "
            "the already isolated 18-term residual face, and objectwise K_Eq "
            "then supplies the reduced-Eq correction with target/residue/q/"
            "ridge rows retained"
        ),
        "scope": (
            "exact rational S4 representation and exact comparison with the "
            "pinned C-plus coefficient interface.  It does not promote the "
            "conditional C-plus formula to a physical source cell."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("endpoint flag representation: [2,2] tensor trivial tail")
    print("full S4 coinvariants: ZERO")
    print("fixed-chart coinvariants: ONE, vector (2,2,-1,-1,-1,-1)")
    print("endpoint-odd Cartan + objectwise K_Eq span: NO")
    print("transported D6 / conditional C-plus coefficient: EXACT MATCH")
    print("physical C-plus/P2 monoidal placement: STILL MISSING")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
