#!/usr/bin/env python3
"""Build the minimal relative graph for uniform cross-chart companions.

After fixing one selected direction edge and one tail edge, the remaining
complete response coefficient is a perfect-matching sum on 2h-2 vertices.
Distinguish the two surviving chart vertices r,s.  The fixed-chart terms F
contain rs.  Every other term c has a unique parent p(c) in F, obtained by
the four-cycle switch

    rs, yz  <->  ry, sz  (or rz, sy).

Each fixed term has 2h-4 companions.  The presentation-safe source schema
is the monic relative graph

    d theta_M = z_M-u_M,
    d phi_c   = t_c-(z_c-z_p(c)),
    Gamma_c   = phi_c+theta_c-theta_p(c),
    d Gamma_c = t_c-(u_c-u_p(c)).

It resolves the original occurrence algebra with t retained.  Summing gives

    P-(2h-3)F = T-d Gamma_sum,

so T is exactly the cross-chart completion carrier.  Common-edge PP faces
are the same graph one order lower.  Retained operation labels put the four
switch-cycle faces in the known C2+/C4/P2 list.  At h=3 the two companions split into one odd
Cartan line and one even T line; the latter is exactly the conditional C+
coefficient pinned by 7b67277.

This constructs the formal source DGA and verifies d^2/PP functoriality.  It
does not land t in the physical augmented complex.  The conditional C+/P2
interface has the required even coefficient projection, but its physical
restriction/reinsertion map is open and its DQ/PS faces still need the
generic relative-C4 primitive.  Moreover the top fixed-chart Spencer
generator with scalar face L_h is an additional homological cell; the lower
packet schema is not a replacement for that top generator.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_response_h2_chart_direction_spencer_packet_gate.py":
        "46b53933a080d0b8eeceee695ecd0d4c6d72224d7d0fea4352176b410b8b7fe4",
    "notes/uniform-response-h2-chart-direction-spencer-packet-gate.md":
        "d57b734cbbb99f5088cdd01e803522ffcd5b55dc2123525ae6d744de6e9a0445",
    "computations/verify_h3_h2_l01_endpoint_flag_s4_cplus_span_gate.py":
        "3ab94cb5293deeef5777588c15e308e4ac8974ffcff4272ee021432b6633089d",
    "notes/h3-h2-l01-endpoint-flag-s4-cplus-span-gate.md":
        "dcbb22545c23d209f2ee3cf654f00d4d76cae8b200dc886214abda9a7016c29f",
    "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py":
        "4dfb2846c698e5603dadeb1a73add17a7984ccedbad25e3bb09b6aa4170e62ce",
    "notes/h2-p2-relative-occurrence-graph-resolution-gate.md":
        "101f1040df04e5f6a3ca7c5034c1a3a713903704936207619c5ec8e00d59df37",
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "notes/h2-b4-cplus-shared-interface-gate.md":
        "4c89253c18f4475371849a78c990e27b7d6af79193522cd5a583af80cc929fb8",
    "computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py":
        "24c5504111da4f284d9d01a535de544a44ea1bae75430d98761e093cc6ca8482",
    "notes/h2-endpoint-role-groupoid-pointed-bar-gate.md":
        "2476b8ca7974f3b5fba02905d0430565d22e9f5c863337748ae8f5eb757a8de2",
    "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py":
        "026eb42fac96e2c21e6466f51322a18d45d975bcf5f48e0dc33f9cfa740d8d41",
    "notes/h3-pure-trapped-h2-c2-c4-p2-descent-reduction.md":
        "699a9debf8de2646249f949e80312baa58251a1f36639bed249d40e2dc74b2ea",
}
EXPECTED_LEDGER_SHA256 = (
    "891417e16e2eacce959d576a8b2e2a09d61e3c97a9aede9c9216211ba326dc16"
)

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


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


def odd_double_factorial(value: int) -> int:
    require(value >= -1 and value % 2 == 1, value)
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def rank(columns: list[tuple[Q, ...]] | tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(row) for row in zip(*columns, strict=True)]
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


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(value: int | Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(value) * entry for entry in vector)


def unit(index: int, size: int) -> tuple[Q, ...]:
    return tuple(Q(place == index) for place in range(size))


def switch_parent(child: Matching, fixed_edge: Edge = (0, 1)) -> Matching:
    require(fixed_edge not in child, ("child already fixed", child))
    r, s = fixed_edge
    r_edge = next(edge for edge in child if r in edge)
    s_edge = next(edge for edge in child if s in edge)
    y = r_edge[1] if r_edge[0] == r else r_edge[0]
    z = s_edge[1] if s_edge[0] == s else s_edge[0]
    require(y not in fixed_edge and z not in fixed_edge and y != z,
            (child, r_edge, s_edge))
    rest = tuple(edge for edge in child if edge not in (r_edge, s_edge))
    return tuple(sorted(rest + (fixed_edge, tuple(sorted((y, z))))))


def block_vector(u, z, t):
    return tuple(u) + tuple(z) + tuple(t)


def presentation_matrix_audit(matchings: tuple[Matching, ...],
                              fixed: tuple[Matching, ...],
                              companions: tuple[Matching, ...],
                              parent_index: tuple[int, ...]) -> dict[str, int]:
    """Explicitly audit the monic DGA in the h=3 and h=4 packets."""
    occurrence_count = len(matchings)
    companion_count = len(companions)
    position = {matching: index for index, matching in enumerate(matchings)}
    zero_u = (Q(0),) * occurrence_count
    zero_t = (Q(0),) * companion_count
    theta = []
    for index in range(occurrence_count):
        theta.append(block_vector(scale(-1, unit(index, occurrence_count)),
                                  unit(index, occurrence_count), zero_t))
    phi = []
    gamma = []
    for cindex, child in enumerate(companions):
        child_index = position[child]
        pindex = parent_index[cindex]
        phi_column = block_vector(
            zero_u,
            add(scale(-1, unit(child_index, occurrence_count)),
                unit(pindex, occurrence_count)),
            unit(cindex, companion_count),
        )
        phi.append(phi_column)
        gamma_column = add(phi_column, theta[child_index],
                           scale(-1, theta[pindex]))
        expected = block_vector(
            add(scale(-1, unit(child_index, occurrence_count)),
                unit(pindex, occurrence_count)),
            zero_u, unit(cindex, companion_count),
        )
        require(gamma_column == expected,
                ("Gamma boundary changed", cindex))
        gamma.append(gamma_column)

    graph = theta + phi
    require(rank(graph) == occurrence_count + companion_count,
            "the switch graph sequence stopped being monic")

    # The augmentation is u -> (u,u,t_c=u_c-u_parent).  Together with the
    # graph boundaries it spans the full extended degree-zero module.
    augmentation = []
    for index in range(occurrence_count):
        t_values = tuple(
            Q(position[child] == index) - Q(parent_index[cindex] == index)
            for cindex, child in enumerate(companions)
        )
        augmentation.append(block_vector(
            unit(index, occurrence_count), unit(index, occurrence_count),
            t_values,
        ))
    height = 2 * occurrence_count + companion_count
    require(rank(graph + augmentation) == height,
            "the relative switch graph stopped resolving the old fibre")

    # Setting t=0 is not a resolution: it identifies every child with its
    # fixed parent and leaves only one degree-zero class per fixed star.
    t_zero = [block_vector(zero_u, zero_u, unit(index, companion_count))
              for index in range(companion_count)]
    require(height - rank(graph + t_zero) == len(fixed),
            "the illegal t=0 quotient dimension changed")

    aggregate_gamma = add(*gamma) if gamma else (Q(0),) * height
    parent_degree = 0 if not fixed else companion_count // len(fixed)
    full_indicator = (Q(1),) * occurrence_count
    fixed_set = set(fixed)
    fixed_indicator = tuple(Q(matching in fixed_set) for matching in matchings)
    completion = add(full_indicator,
                     scale(-(parent_degree + 1), fixed_indicator))
    expected_aggregate = block_vector(
        scale(-1, completion), zero_u, (Q(1),) * companion_count
    )
    require(aggregate_gamma == expected_aggregate,
            "P-(2h-3)F=T-dGamma changed")
    return {
        "degree_zero_dimension": height,
        "graph_boundary_rank": rank(graph),
        "augmentation_rank": rank(augmentation),
        "graph_plus_augmentation_rank": rank(graph + augmentation),
        "H0_dimension": height - rank(graph),
        "H0_after_illegal_t_zero": height - rank(graph + t_zero),
    }


def audit_order(h: int) -> dict[str, object]:
    vertices = tuple(range(2 * h - 2))
    fixed_edge = (0, 1)
    matchings = tuple(perfect_matchings(vertices))
    fixed = tuple(matching for matching in matchings if fixed_edge in matching)
    companions = tuple(matching for matching in matchings
                       if fixed_edge not in matching)
    position = {matching: index for index, matching in enumerate(matchings)}
    parents = tuple(switch_parent(child, fixed_edge) for child in companions)
    require(all(parent in fixed for parent in parents), "a parent left F")
    parent_index = tuple(position[parent] for parent in parents)

    expected_fixed = odd_double_factorial(2 * h - 5)
    expected_companions = (2 * h - 4) * expected_fixed
    expected_full = odd_double_factorial(2 * h - 3)
    require((len(fixed), len(companions), len(matchings))
            == (expected_fixed, expected_companions, expected_full),
            (h, len(fixed), len(companions), len(matchings)))

    parent_histogram = {parent: parents.count(parent) for parent in fixed}
    require(set(parent_histogram.values()) == {2 * h - 4},
            (h, parent_histogram))

    # The four-cycle is exact: parent and child share h-3 spectator edges,
    # and each has two private edges.  Removing a common edge commutes with
    # the parent map and gives the same schema one response order lower.
    common_face_count = 0
    child_cycle_face_count = 0
    parent_cycle_face_count = 0
    for child, parent in zip(companions, parents, strict=True):
        common = set(child).intersection(parent)
        child_only = set(child).difference(parent)
        parent_only = set(parent).difference(child)
        require(len(common) == h - 3
                and len(child_only) == len(parent_only) == 2,
                (h, child, parent, common, child_only, parent_only))
        for edge in common:
            lower_child = tuple(item for item in child if item != edge)
            lower_parent = tuple(item for item in parent if item != edge)
            require(switch_parent(lower_child, fixed_edge) == lower_parent,
                    (h, child, parent, edge))
        common_face_count += len(common)
        child_cycle_face_count += len(child_only)
        parent_cycle_face_count += len(parent_only)

    require(common_face_count == len(companions) * (h - 3)
            and child_cycle_face_count == parent_cycle_face_count
                == 2 * len(companions),
            (h, common_face_count, child_cycle_face_count,
             parent_cycle_face_count))

    # Each fixed parent/tail edge has two oriented children.  Their difference
    # is endpoint-odd; their sum is the endpoint-even carrier required by C+.
    orientation_pairs = len(companions) // 2
    require(orientation_pairs == len(fixed) * (h - 2),
            (h, orientation_pairs, len(fixed)))

    matrix = None
    if h <= 4:
        matrix = presentation_matrix_audit(
            matchings, fixed, companions, parent_index
        )
        require(matrix["H0_dimension"] == len(matchings)
                and matrix["H0_after_illegal_t_zero"] == len(fixed),
                matrix)
    return {
        "h": h,
        "remaining_vertices_after_two_varied_edges": len(vertices),
        "complete_lower_packet_occurrences": len(matchings),
        "fixed_chart_occurrences": len(fixed),
        "cross_chart_companions": len(companions),
        "companions_per_fixed_parent": 2 * h - 4,
        "canonical_parent_unique": len(set(parents)) == len(fixed),
        "orientation_pairs": orientation_pairs,
        "proper_faces": {
            "common_spectator_faces": common_face_count,
            "common_face_is_order_h_minus_1_switch_graph": True,
            "child_only_cycle_faces": child_cycle_face_count,
            "parent_only_cycle_faces": parent_cycle_face_count,
            "cycle_face_topology": "C2plus/C4/P2 by retained operation label",
        },
        "aggregate_identity": (
            f"P-{2 * h - 3}F = T-d(Gamma_sum)"
        ),
        "explicit_presentation_matrix": matrix,
    }


def audit_pinned_interfaces() -> dict[str, object]:
    uniform = load(
        "computations/verify_uniform_response_h2_chart_direction_spencer_packet_gate.py",
        "switch_dga_uniform_pin",
    )
    _uniform_ledger, uniform_digest = uniform.audit()
    require(uniform_digest == uniform.EXPECTED_LEDGER_SHA256, uniform_digest)

    flag = load(
        "computations/verify_h3_h2_l01_endpoint_flag_s4_cplus_span_gate.py",
        "switch_dga_flag_pin",
    )
    flag_ledger, flag_digest = flag.audit()
    require(flag_digest == flag.EXPECTED_LEDGER_SHA256, flag_digest)
    flag_span = flag_ledger["candidate_span"]
    flag_physical = flag_ledger["physical_inventory"]
    require(flag_span["equals_L01_direction_primitive"]
            and flag_span["coefficient_span_after_C_plus"]
            and "NO CURRENT SPAN" in flag_physical["physical_verdict"],
            (flag_span, flag_physical))

    graph = load(
        "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py",
        "switch_dga_p2_pin",
    )
    graph_ledger, graph_digest = graph.audit()
    require(graph_digest == graph.EXPECTED_LEDGER_SHA256
            and graph_ledger["relative_graph_DGA"]
                ["one_universal_family_not_eight_unrelated_columns"]
            and graph_ledger["root_PP_functoriality"]
                ["labelled_cobar_square_generated"],
            graph_ledger)

    cplus = load(
        "computations/verify_h2_b4_cplus_shared_interface_gate.py",
        "switch_dga_cplus_pin",
    )
    cplus_ledger, cplus_digest = cplus.audit()
    require(cplus_digest == cplus.EXPECTED_LEDGER_SHA256,
            cplus_digest)
    interface = cplus_ledger["full_interface_and_typing"]
    require(interface["coefficient_projection_agrees"]
            and not interface["physical_restriction_reinsertion_map_constructed"],
            interface)

    groupoid = load(
        "computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py",
        "switch_dga_groupoid_pin",
    )
    groupoid_ledger, groupoid_digest = groupoid.audit()
    require(groupoid_digest == groupoid.EXPECTED_LEDGER_SHA256,
            groupoid_digest)
    two_object = groupoid_ledger["two_object_groupoid"]
    require(two_object["canonical_fold_boundary_rank"] == 0
            and two_object["raw_fold_odd_rank"] == 6,
            two_object)

    lower = load(
        "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py",
        "switch_dga_lower_types_pin",
    )
    lower_ledger, lower_digest = lower.audit()
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256,
            lower_digest)
    c4_residual = lower_ledger["C4"]["generic_flat_internal_residual"]
    require("relative-C4" in c4_residual["missing_cell"]
            and "operation type" in c4_residual["why_not_P2_by_relabeling"],
            c4_residual)
    return {
        "uniform_direction_ledger": uniform_digest,
        "endpoint_flag_Cplus_ledger": flag_digest,
        "P2_relative_graph_ledger": graph_digest,
        "Cplus_shared_interface_ledger": cplus_digest,
        "endpoint_role_groupoid_ledger": groupoid_digest,
        "lower_C2plus_C4_P2_ledger": lower_digest,
        "Cplus_coefficient_is_kappa_weighted_even_carrier": True,
        "Cplus_physical_restriction_reinsertion_constructed": False,
        "generic_relative_C4_constructed": False,
        "objectwise_K_Eq_after_full_Cplus_is_additional": False,
        "top_fixed_chart_Spencer_generator_still_required": True,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    interfaces = audit_pinned_interfaces()
    orders = tuple(audit_order(h) for h in range(2, 7))
    h3 = orders[1]
    require(h3["complete_lower_packet_occurrences"] == 3
            and h3["fixed_chart_occurrences"] == 1
            and h3["cross_chart_companions"] == 2
            and h3["proper_faces"] == {
                "common_spectator_faces": 0,
                "common_face_is_order_h_minus_1_switch_graph": True,
                "child_only_cycle_faces": 4,
                "parent_only_cycle_faces": 4,
                "cycle_face_topology": "C2plus/C4/P2 by retained operation label",
            }, h3)
    ledger = {
        "theorem": "uniform chart cross-companion relative switch DGA gate",
        "pins": PINS,
        "pinned_interfaces": interfaces,
        "relative_switch_DGA": {
            "objects": (
                "all matchings M in one complete lower coefficient; fixed "
                "F contains rs and every companion c has canonical C4-switch parent p(c)"
            ),
            "degree_zero_new": ["z_M", "t_c"],
            "degree_one": ["theta_M", "phi_c"],
            "d_theta": "z_M-u_M",
            "d_phi": "t_c-(z_c-z_p(c))",
            "Gamma": "phi_c+theta_c-theta_p(c)",
            "d_Gamma": "t_c-(u_c-u_p(c))",
            "d_squared": 0,
            "presentation_safe": (
                "the equations are monic first in z_M and then in t_c; H0 is the original occurrence algebra"
            ),
            "illegal_absolute_step": (
                "t=0 identifies every companion occurrence with its fixed parent and changes H0"
            ),
            "aggregate_boundary": "P-(2h-3)F = T-d(Gamma_sum)",
        },
        "PP_functoriality": {
            "linear_face_rule": (
                "Xu and Xz are the same labelled occurrence face, Xtheta is "
                "its graph lift, Xt=X(z_c-z_p(c)), Xphi=0"
            ),
            "commutator_with_d": 0,
            "common_edge_face": "the identical switch DGA at order h-1",
            "switch_cycle_face": (
                "two child-only plus two parent-only faces per companion; "
                "retained operation labels classify them as C2plus, C4, or P2"
            ),
            "orientation_split": (
                "two children per switched tail edge split into an odd "
                "Cartan line and the even aggregate carrier T"
            ),
        },
        "orders_exhaustively_audited": orders,
        "verdict": (
            "The cross-chart 2h-4 companions have a uniform presentation-safe "
            "relative graph and no new proper-face topology.  Common faces "
            "recurse in h; the four-cycle faces are exactly the known C2plus/"
            "C4/P2 list.  At h=3 the kappa-weighted even aggregate is the "
            "D6=[2,2] coefficient identified in 7b67277, while the odd "
            "orientation is the Cartan line.  The conditional Cplus/P2 "
            "interface therefore has the correct even projection, but is not "
            "the whole chart-complete schema: its physical map is open and "
            "the DQ/PS arm still contains the separately pinned generic "
            "relative-C4 primitive.  Above those lower faces, a top fixed-"
            "chart Spencer generator carrying L_h remains an independent "
            "homological cell.  A complete Cplus interface already includes "
            "the objectwise central-Eq correction; central Eq is not a further cell."
        ),
        "first_exact_no_go": (
            "setting the switch carrier t to zero changes H0 from the complete "
            "packet dimension (2h-3)!! to the fixed-chart dimension (2h-5)!!. "
            "Equivalently, existing coefficient Cplus/P2 formulas do not define "
            "the required physical map t -> augmented outputs."
        ),
        "shortest_positive_theorem": (
            "construct one natural augmented map from the relative switch "
            "carrier family t_c to the physical rho-even Cplus/P2 orbit, "
            "including its DQ/PS same-grade relative-C4 face.  Require "
            "compatibility with common-edge recursion, then compose with the "
            "separate top L_h chart-Spencer cell.  The full Cplus interface "
            "then supplies central Eq without another cell"
        ),
        "scope": (
            "exact matching-switch graph DGA and formal labelled PP faces, "
            "not a physical word/fine/repeated/q/anchor/W/ridge landing"
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
    print("relative switch graph: PRESENTATION-SAFE, d^2=0")
    print("aggregate: P-(2h-3)F = T-dGamma")
    print("common faces: RECURSIVE; cycle faces: C2plus/C4/P2 ONLY")
    print("Cplus/P2 even carrier landing: EXACT COEFFICIENT, PHYSICALLY OPEN")
    print("generic same-grade relative-C4 face: STILL REQUIRED")
    print("additional top L_h Spencer generator: REQUIRED")
    print("additional central-Eq cell after full Cplus: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
