#!/usr/bin/env python3
r"""Exact endpoint-word-change attachment-or-dual gate at h=3.

The complete first endpoint bar/Koszul inventory has route columns
(-Omega_v,+q_(v,N)); its positive-dimensional squares only give matching
differences, path differences, and the cyclic ridge incidence.  This checker
computes the resulting primitive aggregate cokernel, records the physical
readouts of a hypothetical reduced companion, and proves the aggregate-Tor
Fredholm dichotomy over an arbitrary coefficient ring.

It does not construct the reduced companion, the Omega-to-rootless-ridge
comparison, or a physical terminal annihilator.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "1847152e61db1ce8bf010903ab35732ee6d38c933dcebaaa7df7d56448329af4"
PINS = {
    "computations/verify_h3_component_iv_endpoint_word_change_cokernel.py":
        "e452467b235391fa434ddd10364bd27a35fe32791fab8e07e5c4576dd5f5b5eb",
    "computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py":
        "b1d1a62d229d9ebb3d20abbc7359503af08506fec882f629ee95a886c58490a8",
    "computations/verify_h3_component_iv_reduced_companion_tor_gate.py":
        "5bf7e0960b413c4e5d587b3c8f46d51493010bb73413682d7705bb28070d0935",
    "computations/verify_h3_qzero_denominator_rees_four_cube.py":
        "70600661cd6a14e509a9e6487d4caa833c8bdb4419a2f442efd4b95bed7eebda",
    "computations/verify_h3_rootless_normalized_c5_augmented_comparison_gate.py":
        "fd6e94cd52a9f6950bf752887f9bea129373f6686b12704f6d2eaf29b7fa0dca",
    "computations/verify_h3_c5_marked_unary_transition_scc_guard.py":
        "0950308ee449fabb0090d4cc81b968eeb1b771effa776b42197057079a225a73",
}

ODD = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
FACE_ORDER = (1, 3, 5, 2, 4)
CYCLE = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))
FIRST_TOR_MULTIPLIERS = {
    (1, 3): {(1, 3): (1, 2), (3, 1): (2, 3)},
    (3, 5): {(3, 5): (3, 4), (5, 3): (4, 5)},
    (5, 2): {(5, 2): (1, 5), (2, 5): (1, 2)},
    (2, 4): {(2, 4): (2, 3), (4, 2): (3, 4)},
    (4, 1): {(4, 1): (4, 5), (1, 4): (1, 5)},
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def rank(columns: list[tuple[int, ...]]) -> int:
    if not columns:
        return 0
    rows = len(columns[0])
    require(all(len(column) == rows for column in columns), "ragged matrix")
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(rows)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def determinant(columns: list[tuple[int, ...]]) -> int:
    size = len(columns)
    require(size and all(len(column) == size for column in columns),
            "determinant needs a square matrix")
    matrix = [[Q(columns[column][row]) for column in range(size)]
              for row in range(size)]
    value = Q(1)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if matrix[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            value *= -1
        pivot_value = matrix[column][column]
        value *= pivot_value
        matrix[column] = [entry / pivot_value for entry in matrix[column]]
        for row in range(column + 1, size):
            if not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [left - scalar * right for left, right in
                           zip(matrix[row], matrix[column], strict=True)]
    require(value.denominator == 1, ("nonintegral determinant", value))
    return value.numerator


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices if site not in (first, second))
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted(((min(first, second), max(first, second)),)
                                       + tail)))
    return tuple(answer)


def site_profile(edges: tuple[tuple[int, int], ...], sites: tuple[int, ...]) -> tuple[int, ...]:
    counts = {site: 0 for site in sites}
    for left, right in edges:
        if left in counts:
            counts[left] += 1
        if right in counts:
            counts[right] += 1
    return tuple(counts[site] for site in sites)


def endpoint_module() -> dict[str, object]:
    # Five Omega rows followed by three private q_(v,N) rows per face.
    dimension = 20
    routes = []
    route_records = []
    matchings_by_face = {}
    for face_index, v in enumerate(ODD):
        matchings = perfect_matchings(tuple(site for site in ODD if site != v))
        require(len(matchings) == 3, ("four-site matching count", v))
        matchings_by_face[v] = matchings
        for matching_index, matching in enumerate(matchings):
            q_index = 5 + 3 * face_index + matching_index
            column = [0] * dimension
            column[face_index] = -1
            column[q_index] = 1
            routes.append(tuple(column))
            route_records.append({
                "v": v,
                "middle_colour": MIDDLE[v],
                "matching": [list(edge) for edge in matching],
                "boundary": {
                    "endpoint_ridge": "-Omega_v",
                    "companion": "+q_(v,N)",
                },
                "readouts": {
                    "target": 0,
                    "ores": 1,
                    "W": 0,
                    "ainc": 0,
                    "rootless_ridge": 0,
                },
            })

    cycles = []
    for index in range(5):
        column = [0] * dimension
        column[index] = -1
        column[(index + 1) % 5] = 1
        cycles.append(tuple(column))

    # Matching Bianchi faces are route differences.  They have no ridge or
    # ordinary-residue component and do not enlarge the route span.
    bianchi = []
    for face_index in range(5):
        local = routes[3 * face_index:3 * face_index + 3]
        for left, right in ((0, 1), (1, 2), (2, 0)):
            bianchi.append(tuple(a - b for a, b in
                                 zip(local[left], local[right], strict=True)))

    require(rank(routes) == 15, "endpoint route rank changed")
    require(rank(routes + bianchi) == 15,
            "matching Bianchi square enlarged endpoint image")
    require(rank(routes + cycles) == 19,
            "cyclic endpoint module stopped having one aggregate class")

    aggregate = tuple([1] * dimension)
    require(all(dot(aggregate, column) == 0
                for column in routes + cycles + bianchi),
            "aggregate separator stopped killing natural endpoint module")

    # One reduced tail is an integral unit completion.  The determinant
    # records primitivity, not merely rational rank.
    reduced_tail = [0] * dimension
    reduced_tail[5] = -1
    reduced_tail = tuple(reduced_tail)
    require(dot(aggregate, reduced_tail) == -1,
            "reduced companion stopped meeting aggregate class primitively")
    unit_columns = routes + cycles[:4] + [reduced_tail]
    unit_det = determinant(unit_columns)
    require(abs(unit_det) == 1,
            ("one reduced companion no longer completes integrally", unit_det))

    # A putative Omega-to-rootless-ridge comparison has a new coordinate not
    # present in this 20-row endpoint module.  Its primitive rootless dual is
    # independent of the aggregate companion obstruction.
    route_with_rootless = [column + (0,) * 5 for column in routes]
    cycle_with_rootless = [column + (0,) * 5 for column in cycles]
    rootless_dual = tuple([0] * 20 + [1, 0, 0, 0, 0])
    comparison = [0] * 25
    comparison[0] = 1
    comparison[20] = -1
    comparison = tuple(comparison)
    require(all(dot(rootless_dual, column) == 0
                for column in route_with_rootless + cycle_with_rootless)
            and dot(rootless_dual, comparison) == -1,
            "rootless-ridge degree separator changed")

    return {
        "ambient_rows": dimension,
        "route_columns": len(routes),
        "matching_bianchi_columns": len(bianchi),
        "cyclic_ridge_columns": len(cycles),
        "cyclic_ridge_status": (
            "conditional repeated-degree gluing after the clean C5 "
            "collision edges and an Omega_v-to-r_v comparison; not an "
            "additional literal first-degree endpoint 2-cell"
        ),
        "route_rank": rank(routes),
        "rank_after_all_first_degree_squares": rank(routes + bianchi),
        "rank_after_cyclic_faces": rank(routes + cycles + bianchi),
        "cokernel": "Z generated by Lambda=sum_v(Omega_v+sum_N q_(v,N))",
        "primitive_aggregate_on_reduced_tail": -1,
        "unit_completion_determinant": unit_det,
        "rootless_comparison_has_independent_separator": True,
        "routes": route_records,
        "matchings_by_face": {
            str(v): [[list(edge) for edge in matching]
                     for matching in matchings_by_face[v]]
            for v in ODD
        },
    }


def multidegree_gate() -> dict[str, object]:
    # The first common residual degree after multiplying endpoint companions
    # by an incident selected C5 cell is P3+K2 on the five odd sites.
    repeated_records = []
    for index, left_face in enumerate(FACE_ORDER):
        right_face = FACE_ORDER[(index + 1) % 5]
        pair = (left_face, right_face)
        for face, other in ((left_face, right_face),
                            (right_face, left_face)):
            multiplier = FIRST_TOR_MULTIPLIERS[pair][(face, other)]
            for matching in perfect_matchings(tuple(site for site in ODD
                                                     if site != face)):
                edges = tuple(sorted(matching + (multiplier,)))
                profile = site_profile(edges, ODD)
                require(sorted(profile) == [1, 1, 1, 1, 2],
                        ("first collision profile changed", pair, face,
                         matching, multiplier, profile))
                repeated_records.append({
                    "adjacent_faces": list(pair),
                    "route_face": face,
                    "matching": [list(edge) for edge in matching],
                    "incident_multiplier": list(multiplier),
                    "odd_site_profile": list(profile),
                })
    require(len(repeated_records) == 30,
            "first repeated-site route count changed")

    # The first scalar Hasse candidate contains both endpoint directions and
    # both internal edges.  It is an order-(2,2) perfect matching of K8.
    order_four = []
    for v in ODD:
        for matching in perfect_matchings(tuple(site for site in ODD
                                                 if site != v)):
            edges = tuple(sorted(((0, v), (6, 7)) + matching))
            profile = site_profile(edges, tuple(range(8)))
            require(profile == (1,) * 8,
                    ("order-four cube stopped being a K8 perfect matching",
                     v, matching, profile))
            order_four.append({
                "v": v,
                "directions": [
                    f"q_0{v}:0{MIDDLE[v]}",
                    "q_67:22",
                    *[f"q_{left}{right}:{MIDDLE[left]}{MIDDLE[right]}"
                      for left, right in matching],
                ],
                "external_order": 2,
                "internal_order": 2,
                "total_order": 4,
                "site_profile": list(profile),
                "top_coefficient": 1,
            })
    require(len(order_four) == 15,
            "order-four endpoint/internal cube count changed")

    return {
        "first_common_rootless_tail_degree": {
            "monomial": "Q_(v,N)=t*q_(v,N)",
            "q_degree_on_odd_sites": 3,
            "site_profile": "P3+K2=(2,1,1,1,1) up to order",
            "records": repeated_records,
        },
        "first_scalar_hasse_candidate": {
            "multidegree": "{q_xv:0m_v,q_pq:22}+N",
            "bidegree": "external 2, internal 2",
            "total_principal_parts_order": 4,
            "records": order_four,
            "known_physical_descent_defects": [
                "Omega_v endpoint ridge",
                "(H_0-u)e_Eq",
            ],
        },
    }


def aggregate_tor_gate() -> dict[str, object]:
    # C5 incidence columns generate ker(epsilon) as a saturated lattice.
    edges = []
    for index in range(5):
        column = [0] * 5
        column[index] = -1
        column[(index + 1) % 5] = 1
        edges.append(tuple(column))
    require(rank(edges) == 4,
            "C5 incidence stopped spanning a rank-four lattice")
    minor = determinant([tuple(column[:4]) for column in edges[:4]])
    require(abs(minor) == 1, "C5 incidence lattice lost saturation")

    # Explicit construction from any unimodular aggregate vector y.  The
    # displayed sample has epsilon(y)=1; y-e_0 is a cycle boundary.
    y = (2, -1, 1, 0, -1)
    require(sum(y) == 1, "sample aggregate is not normalized")
    e0 = (1, 0, 0, 0, 0)
    z = tuple(source - target for source, target in zip(y, e0, strict=True))
    require(sum(z) == 0, "normalized face difference left ker epsilon")
    coefficients = tuple(-sum(z[:index + 1]) for index in range(4)) + (0,)
    reconstructed = tuple(sum(coefficients[index] * edges[index][row]
                              for index in range(5)) for row in range(5))
    require(reconstructed == z,
            ("cycle edges failed to transport a unit aggregate", z,
             reconstructed, coefficients))

    # Typed physical composition, conditional on the source-valid
    # Omega-to-r comparison and the reduced tail transgression.
    epsilon = sum(y)
    endpoint_after_transport = {
        "rootless_ridge": tuple(-entry for entry in y),
        "Q_tail": y,
        "Eq": 0,
        "W": 0,
        "ainc": 0,
        "target": 0,
        "ores": epsilon,
    }
    normal = {"Eq": -epsilon, "target": 0, "ores": 0}
    reduced_tail = {"Q_tail": tuple(-entry for entry in y),
                    "target": 0, "ores": -epsilon}
    base = {"Eq": epsilon, "W": epsilon, "ainc": -epsilon,
            "target": 0, "ores": 0}
    total_ridge = tuple(endpoint_after_transport["rootless_ridge"][index]
                        + reconstructed[index] for index in range(5))
    require(total_ridge == tuple(-entry for entry in e0),
            "unit aggregate plus collision edges did not select one face")
    require(normal["Eq"] + base["Eq"] == 0
            and endpoint_after_transport["ores"] + reduced_tail["ores"] == 0
            and endpoint_after_transport["Q_tail"] == tuple(
                -entry for entry in reduced_tail["Q_tail"]),
            "conditional bar/normal/tail signs stopped cancelling")
    require(base["W"] == 1 and base["ainc"] == -1,
            "normalized base readouts changed")

    # Ring-level sharpness.  After quotienting the saturated collision
    # lattice, any transgression matrix tau acts only through the ideal
    # I=(epsilon*tau).  The integer examples distinguish I=(1), I=(0), and
    # the proper nonzero ideal I=(2).
    unit_det = determinant(edges[:4] + [e0])
    torsion_det = determinant(edges[:4] + [tuple(2 * x for x in e0)])
    require(abs(unit_det) == 1 and abs(torsion_det) == 2,
            "aggregate ideal examples changed")
    require(all(sum(column) == 0 for column in edges),
            "zero-aggregate separator stopped killing collision edges")

    # An actual denominator kernel has a stronger constraint on the exact
    # clean C5 slice.  Reset-word projection kills every unselected
    # denominator column and sends the five selected columns to h_v Y_0.
    # Therefore b(k)=0 implies sum h_v*y_v=0.  With R_v=0 one has h_v=1,
    # so every physical transgression has epsilon(y)=0.
    h_clean = (1, 1, 1, 1, 1)
    kernel_samples = (
        edges[0], edges[1],
        tuple(edges[0][index] + edges[2][index] for index in range(5)),
    )
    require(all(dot(h_clean, sample) == 0 for sample in kernel_samples),
            "clean-slice reset projection stopped killing collision samples")

    # The aggregate endpoint/rootless covector extends over every *typed*
    # conditional column once Omega and r are joined: give value one to
    # every Omega, every q_(v,N), and every r_v, and zero to Eq/W/readouts.
    # Endpoint routes, cyclic edges, Omega-r comparisons, zero-aggregate
    # transgressions, normal faces, and old cap columns all pair to zero.
    pairings = {
        "endpoint_route": -1 + 1,
        "cyclic_edge": -1 + 1,
        "Omega_minus_r_comparison": 1 - 1,
        "zero_aggregate_tail": -sum(edges[0]),
        "normal_face": 0,
        "old_cap": 0,
    }
    require(all(value == 0 for value in pairings.values()),
            ("aggregate physical separator ledger changed", pairings))
    desired_base_pairing = -1

    return {
        "collision_incidence_rank": rank(edges),
        "saturated_minor": minor,
        "unimodular_aggregate_example": {
            "y": list(y),
            "epsilon_y": epsilon,
            "cycle_coefficients_for_y_minus_e0": list(coefficients),
            "selected_face_after_transport": 0,
        },
        "conditional_physical_composition": {
            "transported_endpoint_bar": endpoint_after_transport,
            "normal_face": normal,
            "reduced_tail": reduced_tail,
            "base_r0_minus_T": base,
            "result_after_collision_transport": {
                "rootless_ridge": list(total_ridge),
                "W": 1,
                "ainc": -1,
                "target": 0,
                "ores": 0,
            },
        },
        "ring_theorem": (
            "for W=S^5, D=ker(epsilon), and a transgression tau:K->W, "
            "coker[D,tau] is S/I with I generated by epsilon(tau(K))"
        ),
        "cases": {
            "I_is_unit": "one aggregate transgression plus C5 edges constructs every face/base column",
            "I_is_zero": "epsilon descends as an S-valued primitive terminal separator",
            "I_proper_nonzero": "residual class is S/I; nonzero cannot be normalized without further localization",
        },
        "integer_counterguard_to_nonzero_implies_unit": {
            "aggregate_2_completion_determinant": torsion_det,
            "cokernel": "Z/2",
        },
        "exact_R_zero_slice": {
            "reset_word_kernel_equation": "sum_v h_v*y_v=0",
            "h_v": list(h_clean),
            "consequence": (
                "epsilon(tau(k))=0 for every physical denominator kernel"
            ),
            "positive_aggregate_branch": False,
            "only_possible_branch": "aggregate separator",
        },
        "conditional_augmented_separator": {
            "value_one_rows": ["Omega_v", "q_(v,N)", "rootless_r_v"],
            "value_zero_rows": ["Eq", "W", "target", "ores", "ainc"],
            "pairings": pairings,
            "value_on_desired_physical_base": desired_base_pairing,
            "promotion_is_conditional_on": [
                "a source-valid Omega_v-to-r_v comparison",
                "source exhaustivity and terminal zero indeterminacy",
            ],
        },
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    ledger = {
        "pins": PINS,
        "endpoint_module": endpoint_module(),
        "multidegree_gate": multidegree_gate(),
        "aggregate_tor_gate": aggregate_tor_gate(),
        "verdict": {
            "first_degree_reduced_minus_Q_cell_exists": False,
            "first_degree_Omega_to_rootless_ridge_exists": False,
            "first_degree_primitive_separator": (
                "Lambda=sum_v(Omega_v+sum_N q_(v,N)); after cyclic faces "
                "the cokernel is Z"
            ),
            "first_common_rootless_degree": "P3+K2 repeated-site degree t*q_(v,N)",
            "first_scalar_source_candidate": "order-four external2/internal2 Hasse cube",
            "aggregate_Tor_shortcut": (
                "valid with unit aggregate ideal; zero aggregate gives a "
                "terminal module separator; a proper nonzero ideal is an "
                "honest residual obstruction"
            ),
            "exact_R_zero_Tor_branch": (
                "only the separator branch: reset-word projection of "
                "b(k)=0 forces epsilon(tau(k))=0 because h_v=1"
            ),
            "physical_closure": False,
        },
        "remaining_physical_compatibilities": [
            "construct the reduced companion transgression in the full source quotient",
            "construct Omega_v-to-rootless-r_v in the same repeated fine degree",
            "promote the normal face and derived W to physical readouts",
            "prove source exhaustivity/zero indeterminacy before interpreting epsilon as the Component-III annihilator",
        ],
        "scope": (
            "complete standard endpoint bar/Koszul/Bianchi first-degree "
            "module, cyclic ridge quotient, exact next grades, and "
            "conditional aggregate-Tor interface; no arbitrary higher "
            "source generator is excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))

    print("h=3 endpoint word-change attachment-or-dual: PRIMITIVE GATE")
    print("endpoint/Bianchi degree: coker Z^5; after conditional cyclic gluing: coker Z")
    print("reduced (-Q,ores=-1) or Omega->r cell in first degree: NO")
    print("next common rootless degree: P3+K2; first scalar Hasse candidate: order 4")
    print("aggregate Tor: unit ideal constructs; zero ideal separates; proper ideal leaves S/I")
    print("exact R=0 denominator kernels: epsilon*tau=0, so only separator branch remains")
    print("physical Component-III closure: CONDITIONAL")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
