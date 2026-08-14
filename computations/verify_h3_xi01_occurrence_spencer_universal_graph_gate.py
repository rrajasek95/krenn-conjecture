#!/usr/bin/env python3
"""Build the minimal presentation-safe graph for the Xi_01 root row.

In the missing-0/doubled-S collision sector there are 45 collision
skeletons and 90 parent-labelled repair occurrences.  The incomplete root

    Xi_01 = a_PS d/da_P0 - a_S1 d/da_01

has weights +1 on 15 occurrences, -1 on 15, and zero on 60.  Parent
collection leaves the known 24-term residual R_01.

This checker compares three exact models.

* The rank-minimal graph d gamma=Xi_01-tau and its occurrence-natural lift
  d beta_i=c_i-t_i preserve H0 but retain tau.
* The canonical occurrence-to-collision cylinder
  d theta_i=c_i-k_{pi(i)} kills the fiber kernels only.  Its weighted row is
  d Theta_Xi=Xi_01-R_01, so Xi_01 is not absolute.
* An absolute R_01 column would fill Xi_01, but lowers collected H0 by one;
  it is precisely new physical data, not a consequence of the resolution.

The 30 active occurrences have 120 labelled first-PP flags.  Their first
unary restriction consists of two disjoint complete 15-term unary rows.
Keeping the root trigger and reinsertion arrow leaves all 120 flags; after
parent collection, 108 unlabelled face coordinates remain, twelve cancel,
and the 96 nonzero coordinates are the PP boundary of R_01.  The later
opposite-root unary face q01*H2345 likewise remains a relative carrier.

The full unsigned vertex transvection is also audited.  It produces the
symmetric coefficient-two collision row and formally returns A+B, but that
collision row is outside the squarefree physical source and has 180 PP
flags.  Thus it replaces the Xi obstruction by the already missing
symmetric collision cell; it does not create an absolute root square.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
import math


BASE_COMMITS = {
    "fullword_parent_inventory": "ba087c6",
    "uniform_standard_module": "a047c8f",
    "complete_response_collision": "b40cebc",
}
BASE_BLOBS = {
    "ba087c6:verify_h3_fullword_collision_sector_parent_inventory_gate.py":
        "beb11bfb1fbe9aee732cc7975b108270af9c2e70c6ff9155a45cf420e3eb6187",
    "a047c8f:verify_uniform_hyperbolic_collision_standard_representation_gate.py":
        "70512a57794bd7c6d75cb3c6e1bfc3956dc4652f6481144aab35519512896867",
    "b40cebc:verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py":
        "c0c6c075388a2eb2d5dad6d133166a3f211dd268183d3e2a5433d922e2ea8ceb",
}
EXPECTED_LEDGER_SHA256 = (
    "d03e2f193306945e6a1f0591566742a957039ff5e8b4d3c465d4820027a0bdcc"
)


Edge = tuple[int, int]
Monomial = tuple[Edge, ...]

NAMES = ("P", "S", "0", "1", "2", "3", "4", "5")
P, S, ZERO, ONE, TWO, THREE, FOUR, FIVE = range(8)
VERTICES = tuple(range(8))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge(left: int, right: int) -> Edge:
    require(left != right, ("loop", left))
    return tuple(sorted((left, right)))


def monomial(*edges: Edge) -> Monomial:
    return tuple(sorted(edges))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield monomial(edge(first, second), *tail)


def vertex_degree(value: Monomial) -> tuple[int, ...]:
    counts = Counter(site for item in value for site in item)
    return tuple(counts[site] for site in VERTICES)


def collision_skeletons() -> tuple[Monomial, ...]:
    available = tuple(vertex for vertex in VERTICES
                      if vertex not in (ZERO, S))
    answer = []
    for left, right in combinations(available, 2):
        rest = tuple(vertex for vertex in available
                     if vertex not in (left, right))
        for tail in perfect_matchings(rest):
            answer.append(monomial(edge(S, left), edge(S, right), *tail))
    require(len(answer) == len(set(answer)) == 45,
            "collision sector stopped having 45 skeletons")
    require({vertex_degree(value) for value in answer}
            == {(1, 2, 0, 1, 1, 1, 1, 1)},
            "collision operation degree changed")
    return tuple(sorted(answer))


COLLISIONS = collision_skeletons()


def parent_occurrences():
    answer = []
    for collision_index, collision in enumerate(COLLISIONS):
        arms = tuple(item for item in collision if S in item)
        require(len(arms) == 2, "collision lost a doubled-S arm")
        for target in arms:
            neighbour = target[0] if target[1] == S else target[1]
            source = edge(ZERO, neighbour)
            parent = monomial(*tuple(item for item in collision
                                     if item != target), source)
            require(vertex_degree(parent) == (1,) * 8,
                    ("repair stopped being squarefree", collision, target))
            answer.append((collision_index, collision, parent, source, target))
    require(len(answer) == len(set(answer)) == 90,
            "parent occurrence count changed")
    return tuple(sorted(answer))


OCCURRENCES = parent_occurrences()


def root_weight(source: Edge) -> Q:
    if source == edge(P, ZERO):
        return Q(1)
    if source == edge(ZERO, ONE):
        return Q(-1)
    return Q(0)


def topology_after_removal(value: Monomial, removed: Edge) -> str:
    face = list(value)
    face.remove(removed)
    positive = tuple(sorted((count for count in vertex_degree(
        tuple(face)) if count), reverse=True))
    lookup = {
        (1, 1, 1, 1, 1, 1): "3K2",
        (2, 1, 1, 1, 1): "P3+K2",
    }
    require(positive in lookup, ("unexpected PP topology", value, removed))
    return lookup[positive]


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns) -> int:
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
        pivot_value = rows[answer][column]
        rows[answer] = [value / pivot_value for value in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [left - factor * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def in_span(columns, value) -> bool:
    return rank(tuple(columns)) == rank(tuple(columns) + (tuple(value),))


def basis(width: int, position: int, coefficient=1):
    answer = [Q(0)] * width
    answer[position] = Q(coefficient)
    return tuple(answer)


def xi_and_collection_audit():
    weights = tuple(root_weight(item[3]) for item in OCCURRENCES)
    active = tuple(index for index, value in enumerate(weights) if value)
    require(Counter(weights)
            == Counter({Q(0): 60, Q(1): 15, Q(-1): 15}),
            "Xi_01 parent support changed")
    parent_even = (Q(1),) * 90
    parent_dual = tuple(value / 30 for value in weights)
    require(dot(parent_dual, parent_even) == 0
            and dot(parent_dual, weights) == 1,
            "parent Xi dual changed")

    residual = [Q(0)] * 45
    fiber_sizes = Counter()
    for occurrence, value in zip(OCCURRENCES, weights, strict=True):
        collision_index = occurrence[0]
        residual[collision_index] += value
        fiber_sizes[collision_index] += 1
    residual = tuple(residual)
    require(set(fiber_sizes.values()) == {2}
            and Counter(residual)
            == Counter({Q(0): 21, Q(1): 12, Q(-1): 12}),
            "collected R_01 changed")
    residual_dual = tuple(value / 24 for value in residual)
    collected_even = (Q(2),) * 45
    require(dot(residual_dual, collected_even) == 0
            and dot(residual_dual, residual) == 1,
            "collected residual dual changed")
    return weights, active, residual, {
        "parent_coordinates": 90,
        "collection_coordinates": 45,
        "collection_fiber_size": 2,
        "Xi_parent_support": {"+1": 15, "-1": 15, "0": 60},
        "R01_collected_support": {"+1": 12, "-1": 12, "0": 21},
        "parent_dual": "Xi_01/30",
        "collected_dual": "R_01/24",
        "standard_module": (
            "Xi_01 is the incidence image J(e_P-e_1), while the unsigned "
            "transvection is the constant/symmetric incidence line"
        ),
    }


def universal_graph_and_collection_audit(weights, active, residual):
    # Existing parent-even row is one old boundary in the 90 occurrence
    # coordinates.  Its quotient dimension is 89.
    parent_even = (Q(1),) * 90
    old_h0 = 90 - rank((parent_even,))
    require(old_h0 == 89, "parent-even H0 changed")

    # Rank-minimal aggregate graph d gamma=Xi-tau.  This preserves H0 but
    # cannot by itself carry the 120 distinct occurrence/reinsertion flags.
    aggregate_even = parent_even + (Q(0),)
    aggregate_graph = weights + (Q(-1),)
    aggregate_xi = weights + (Q(0),)
    aggregate_tau = (Q(0),) * 90 + (Q(1),)
    aggregate_dual = tuple(value / 30 for value in weights) + (Q(1),)
    aggregate_columns = (aggregate_even, aggregate_graph)
    require(91 - rank(aggregate_columns) == old_h0
            and not in_span(aggregate_columns, aggregate_xi)
            and not in_span(aggregate_columns, aggregate_tau)
            and in_span(aggregate_columns,
                        add(aggregate_xi, scale(-1, aggregate_tau)))
            and all(dot(aggregate_dual, column) == 0
                    for column in aggregate_columns)
            and dot(aggregate_dual, aggregate_xi)
            == dot(aggregate_dual, aggregate_tau) == 1,
            "aggregate Xi graph changed")

    # Occurrence-minimal graph: only the 30 nonzero root occurrences need
    # carrier copies.  It is the smallest literal lift retaining all 120 PP
    # flags.  A full functorial resolution can add the 60 zero-weight graphs;
    # both versions preserve the same H0=89.
    active_position = {occurrence: position
                       for position, occurrence in enumerate(active)}
    active_width = 90 + len(active)
    occurrence_columns = []
    for occurrence in active:
        column = [Q(0)] * active_width
        column[occurrence] = Q(1)
        column[90 + active_position[occurrence]] = Q(-1)
        occurrence_columns.append(tuple(column))
    occurrence_even = parent_even + (Q(0),) * len(active)
    occurrence_xi = weights + (Q(0),) * len(active)
    occurrence_tau = [Q(0)] * active_width
    occurrence_detector = [Q(value) / 30 for value in weights]
    for occurrence in active:
        value = weights[occurrence]
        occurrence_tau[90 + active_position[occurrence]] = value
        occurrence_detector.append(value / 30)
    occurrence_tau = tuple(occurrence_tau)
    occurrence_detector = tuple(occurrence_detector)
    occurrence_boundaries = (occurrence_even,) + tuple(occurrence_columns)
    require(rank(occurrence_boundaries) == 31
            and active_width - rank(occurrence_boundaries) == old_h0
            and in_span(occurrence_boundaries,
                        add(occurrence_xi, scale(-1, occurrence_tau)))
            and not in_span(occurrence_boundaries, occurrence_xi)
            and not in_span(occurrence_boundaries, occurrence_tau)
            and all(dot(occurrence_detector, column) == 0
                    for column in occurrence_boundaries)
            and dot(occurrence_detector, occurrence_xi)
            == dot(occurrence_detector, occurrence_tau) == 1,
            "occurrence-minimal Xi graph changed")

    full_width = 180
    full_graphs = []
    for occurrence in range(90):
        column = [Q(0)] * full_width
        column[occurrence] = Q(1)
        column[90 + occurrence] = Q(-1)
        full_graphs.append(tuple(column))
    full_even = parent_even + (Q(0),) * 90
    require(full_width - rank((full_even,) + tuple(full_graphs)) == old_h0,
            "full universal occurrence graph changed H0")

    # Canonical occurrence-to-collected cylinder.  Each parent coordinate
    # maps to its collision fiber coordinate.  It has the H0 of the collected
    # target (45 coordinates modulo its symmetric line), not that of the
    # parent-labelled source.
    collection_width = 90 + 45
    theta = []
    for occurrence_index, occurrence in enumerate(OCCURRENCES):
        column = [Q(0)] * collection_width
        column[occurrence_index] = Q(1)
        column[90 + occurrence[0]] = Q(-1)
        theta.append(tuple(column))
    collection_even = parent_even + (Q(0),) * 45
    collection_boundaries = tuple(theta) + (collection_even,)
    xi_extended = weights + (Q(0),) * 45
    residual_extended = (Q(0),) * 90 + residual
    weighted_theta = tuple(
        sum((weights[column] * theta[column][row]
             for column in range(90)), Q(0))
        for row in range(collection_width)
    )
    require(weighted_theta
            == add(xi_extended, scale(-1, residual_extended)),
            "weighted collection cylinder stopped giving Xi-R")

    # Pull R/24 back constantly along each two-parent fiber.  This kills
    # every cylinder graph and the symmetric row, and reads one on both Xi
    # and R, proving that neither is absolute in the cylinder.
    pulled_dual = tuple(residual[item[0]] / 24 for item in OCCURRENCES)
    pulled_dual += tuple(value / 24 for value in residual)
    collected_old_h0 = 45 - 1
    require(rank(tuple(theta)) == 90
            and rank(collection_boundaries) == 91
            and collection_width - rank(collection_boundaries)
            == collected_old_h0 == 44
            and all(dot(pulled_dual, column) == 0
                    for column in collection_boundaries)
            and dot(pulled_dual, xi_extended)
            == dot(pulled_dual, residual_extended) == 1
            and not in_span(collection_boundaries, xi_extended)
            and not in_span(collection_boundaries, residual_extended),
            "canonical occurrence-to-collection cylinder changed")

    # The missing absolute datum is exactly a column on R.  It makes Xi a
    # boundary and lowers the collected quotient dimension by one.
    filled = collection_boundaries + (residual_extended,)
    require(rank(filled) == 92
            and collection_width - rank(filled) == 43
            and in_span(filled, xi_extended),
            "an absolute R landing stopped filling Xi")
    return {
        "old_parent_presentation": {
            "coordinates": 90,
            "existing_parent_even_rank": 1,
            "H0": old_h0,
        },
        "rank_minimal_aggregate_graph": {
            "boundary": "d gamma_Xi=Xi_01-tau_Xi",
            "coordinates_rank_H0": [91, 2, 89],
            "Xi_absolute": False,
            "tau_retained": True,
            "warning": "one aggregate carrier does not retain 120 PP flags",
        },
        "occurrence_minimal_graph": {
            "active_parent_coordinates": len(active),
            "boundaries": "d beta_i=c_i-t_i for the 30 active occurrences",
            "weighted_boundary": "d sum_i(w_i beta_i)=Xi_01-tau_01",
            "coordinates_rank_H0": [active_width, 31, 89],
            "Xi_absolute": False,
            "normalized_extended_dual": "(Xi_01/30 on c, Xi_01/30 on t)",
        },
        "full_universal_occurrence_graph": {
            "coordinates": full_width,
            "graph_columns_plus_even_rank": 91,
            "H0": old_h0,
            "zero_weight_carrier_graphs": 60,
        },
        "canonical_occurrence_to_collection_cylinder": {
            "boundaries": "d theta_i=c_i-k_pi(i)",
            "weighted_boundary": "d Theta_Xi=Xi_01-R_01",
            "coordinates_rank_H0": [collection_width, 91, 44],
            "viewed_from_collected_target_H0_old_new": [44, 44],
            "viewed_from_parent_source_H0_old_new": [89, 44],
            "Xi_absolute": False,
            "retained_carrier": "R_01",
            "normalized_extended_dual":
                "pullback of R_01/24 along the two-parent fibers",
        },
        "absolute_filler_test": {
            "new_boundary": "d eta_R=R_01",
            "H0_before_after": [44, 43],
            "Xi_absolute_after_filler": True,
            "interpretation": (
                "this is a new rank-raising physical cell, not a formal "
                "consequence of occurrence resolution"
            ),
        },
    }


def pp_unary_reinsertion_audit(weights, active):
    parent_flags = []
    collected = Counter()
    collected_types = {}
    trigger_counts = Counter()
    unary_groups = defaultdict(Counter)
    for occurrence_index in active:
        collision_index, collision, _parent, source, target = (
            OCCURRENCES[occurrence_index]
        )
        coefficient = weights[occurrence_index]
        for removed in collision:
            face_list = list(collision)
            face_list.remove(removed)
            face = tuple(face_list)
            kind = topology_after_removal(collision, removed)
            if removed == target:
                trigger = "varied_target_unary"
                vertices = tuple(sorted(
                    set(site for item in face for site in item)
                ))
                unary_groups[(source, target, vertices)][face] += coefficient
            elif S in removed:
                trigger = "sibling_arm_unary"
            else:
                trigger = "tail_restriction"
            trigger_counts[trigger] += 1
            reinsertion_label = (occurrence_index, source, target, removed)
            parent_flags.append((reinsertion_label, face, coefficient, kind))
            key = (face, removed)
            collected[key] += coefficient
            collected_types[key] = kind
    require(len(parent_flags) == len(set(parent_flags)) == 120
            and Counter(value[3] for value in parent_flags)
            == Counter({"3K2": 60, "P3+K2": 60})
            and trigger_counts == Counter({
                "varied_target_unary": 30,
                "sibling_arm_unary": 30,
                "tail_restriction": 60,
            }), "Xi PP flag census changed")
    nonzero_collected = {key: value for key, value in collected.items()
                         if value}
    require(len(collected) == 108
            and len(nonzero_collected) == 96
            and sum(not value for value in collected.values()) == 12
            and Counter(nonzero_collected.values())
            == Counter({Q(1): 48, Q(-1): 48})
            and Counter(collected_types[key] for key in nonzero_collected)
            == Counter({"3K2": 48, "P3+K2": 48}),
            "collected Xi PP packet changed")

    expected_unary = {
        (edge(P, ZERO), edge(P, S), (S, ONE, TWO, THREE, FOUR, FIVE)):
            Q(1),
        (edge(ZERO, ONE), edge(S, ONE), (P, S, TWO, THREE, FOUR, FIVE)):
            Q(-1),
    }
    require(set(unary_groups) == set(expected_unary),
            ("varied-target unary fibers changed", unary_groups))
    unary_records = []
    for key, row in unary_groups.items():
        require(len(row) == 15
                and set(row.values()) == {expected_unary[key]}
                and set(row) == set(perfect_matchings(key[2])),
                ("unary face stopped being a complete row", key, row))
        source, target, vertices = key
        unary_records.append({
            "source_to_target":
                f"{NAMES[source[0]]}{NAMES[source[1]]}"
                f"->{NAMES[target[0]]}{NAMES[target[1]]}",
            "vertices": [NAMES[value] for value in vertices],
            "terms": len(row),
            "coefficient": str(expected_unary[key]),
            "reinsertion_label_retained": True,
        })

    # Presentation-safe face graphs: one carrier face for each of the 120
    # root-labelled PP flags.  They preserve the 120-dimensional face H0.
    face_width = 240
    face_graphs = []
    for flag in range(120):
        column = [Q(0)] * face_width
        column[flag] = Q(1)
        column[120 + flag] = Q(-1)
        face_graphs.append(tuple(column))
    require(rank(tuple(face_graphs)) == 120
            and face_width - rank(tuple(face_graphs)) == 120,
            "PP relative graph H0 changed")

    # If the root/reinsertion trigger is forgotten, the canonical PP
    # collection cylinder has target dimension 108.  Its weighted boundary
    # is the 96-support PP residual, not zero.
    collected_keys = tuple(sorted(collected, key=repr))
    key_index = {key: position for position, key in enumerate(collected_keys)}
    pp_width = 120 + len(collected_keys)
    pp_theta = []
    pp_weights = []
    for flag_index, (_reinsertion, face, coefficient, _kind) in enumerate(
            parent_flags):
        removed = parent_flags[flag_index][0][3]
        key = (face, removed)
        column = [Q(0)] * pp_width
        column[flag_index] = Q(1)
        column[120 + key_index[key]] = Q(-1)
        pp_theta.append(tuple(column))
        pp_weights.append(coefficient)
    weighted_pp_theta = tuple(
        sum((pp_weights[column] * pp_theta[column][row]
             for column in range(120)), Q(0))
        for row in range(pp_width)
    )
    parent_pp_vector = tuple(pp_weights) + (Q(0),) * len(collected_keys)
    collected_pp_vector = (Q(0),) * 120 + tuple(
        collected[key] for key in collected_keys
    )
    require(rank(tuple(pp_theta)) == 120
            and pp_width - rank(tuple(pp_theta)) == len(collected_keys) == 108
            and weighted_pp_theta
            == add(parent_pp_vector, scale(-1, collected_pp_vector))
            and not in_span(tuple(pp_theta), parent_pp_vector)
            and not in_span(tuple(pp_theta), collected_pp_vector),
            "PP collection cylinder stopped retaining the residual")

    # First opposite-root/reinsertion Cartan defect from b40cebc: q01 times
    # the three matchings on 2345 is a selected 3-of-15 unary block.  Its
    # graph preserves H0=14 and retains the class.
    unary_matchings = tuple(perfect_matchings(
        (ZERO, ONE, TWO, THREE, FOUR, FIVE)
    ))
    q_block = tuple(Q(1) if edge(ZERO, ONE) in value else Q(0)
                    for value in unary_matchings)
    unary_even = (Q(1),) * 15
    unary_dual = tuple(Q(1, 3) if value else Q(-1, 12)
                       for value in q_block)
    unary_even_extended = unary_even + (Q(0),)
    unary_graph = q_block + (Q(-1),)
    q_extended = q_block + (Q(0),)
    unary_carrier = (Q(0),) * 15 + (Q(1),)
    unary_dual_extended = unary_dual + (Q(1),)
    unary_boundaries = (unary_even_extended, unary_graph)
    require(Counter(q_block) == Counter({Q(0): 12, Q(1): 3})
            and 15 - rank((unary_even,)) == 14
            and 16 - rank(unary_boundaries) == 14
            and all(dot(unary_dual_extended, column) == 0
                    for column in unary_boundaries)
            and dot(unary_dual_extended, q_extended)
            == dot(unary_dual_extended, unary_carrier) == 1
            and not in_span(unary_boundaries, q_extended),
            "unary q01 reinsertion graph changed")
    return {
        "parent_labelled_first_PP": {
            "flags": len(parent_flags),
            "topologies": {"3K2": 60, "P3+K2": 60},
            "trigger_split": dict(sorted(trigger_counts.items())),
            "all_120_survive_with_root_and_reinsertion_labels": True,
        },
        "canonical_parent_forgetting": {
            "face_coordinates": len(collected),
            "zero_coordinates_after_collection": 12,
            "nonzero_residual_coordinates": len(nonzero_collected),
            "nonzero_topologies": {"3K2": 48, "P3+K2": 48},
            "weighted_boundary": "PP Xi_01 - PP R_01",
            "absolute": False,
        },
        "first_varied_edge_unary_face": {
            "description": (
                "deleting the varied target edge gives the signed difference "
                "of two disjoint complete 15-term unary rows"
            ),
            "rows": sorted(unary_records, key=lambda item: item["coefficient"]),
            "existing_unlabelled_unary_rows_erase_reinsertion_trigger": False,
        },
        "presentation_safe_PP_graph": {
            "coordinates_rank_H0": [face_width, 120, 120],
            "facewise_boundary": "d(PP beta_i)=f_i-s_i",
            "absolute_top_only_kill_is_chain_map": False,
        },
        "opposite_root_unary_reinsertion": {
            "face": "q01*H2345",
            "selected_complete_unary_coordinates": "3 of 15",
            "boundary": "d gamma_q=q01*H2345-t_q",
            "H0_old_relative": [14, 14],
            "absolute": False,
            "normalized_extended_dual":
                "1/3 on selected three, -1/12 on other twelve, 1 on t_q",
        },
    }


def derivation(polynomial: Counter[Monomial], replacements):
    answer: Counter[Monomial] = Counter()
    for value, coefficient in polynomial.items():
        for position, source in enumerate(value):
            if source not in replacements:
                continue
            target, factor = replacements[source]
            out = list(value)
            out[position] = target
            answer[monomial(*out)] += coefficient * factor
    return Counter({key: value for key, value in answer.items() if value})


def unsigned_transvection_shortcut_audit():
    # Full unsigned 0->S transvection acts on every 0-u edge.  On the
    # complete hafnian each collision has two parents and coefficient two.
    unsigned_parent = (Q(1),) * 90
    unsigned_collected = [Q(0)] * 45
    for occurrence in OCCURRENCES:
        unsigned_collected[occurrence[0]] += 1
    require(set(unsigned_collected) == {Q(2)},
            "unsigned transvection stopped giving the symmetric row")

    pp_types = Counter()
    for collision in COLLISIONS:
        for removed in collision:
            pp_types[topology_after_removal(collision, removed)] += 1
    require(pp_types == Counter({"3K2": 90, "P3+K2": 90}),
            "symmetric collision PP boundary changed")

    # On the local selected A=D*q01, unsigned X gives D*s1.  The opposite
    # unsigned Y differentiates both S-incident factors and returns A+B.
    D = edge(P, S)
    p0 = edge(P, ZERO)
    q01 = edge(ZERO, ONE)
    s1 = edge(S, ONE)
    A = monomial(D, q01)
    B = monomial(p0, s1)
    X = {edge(ZERO, vertex): (edge(S, vertex), Q(1))
         for vertex in VERTICES if vertex not in (ZERO, S)}
    Y = {edge(S, vertex): (edge(ZERO, vertex), Q(1))
         for vertex in VERTICES if vertex not in (ZERO, S)}
    first = derivation(Counter({A: Q(1)}), X)
    returned = derivation(first, Y)
    require(first == Counter({monomial(D, s1): Q(1)})
            and returned == Counter({A: Q(1), B: Q(1)}),
            ("unsigned opposite-root return changed", first, returned))

    # The operation-degree projection is zero on every physical matching.
    physical = tuple(perfect_matchings(VERTICES))
    require(len(physical) == 105
            and {vertex_degree(value) for value in physical} == {(1,) * 8}
            and set(physical).isdisjoint(COLLISIONS),
            "a symmetric collision became a squarefree physical row")
    return {
        "full_unsigned_parent_row": "one on all 90 repair occurrences",
        "collected_top": "coefficient 2 on all 45 collision monomials",
        "formal_local_opposite_return": "A+B",
        "symmetric_collision_top_in_squarefree_physical_source": False,
        "reason": (
            "physical rows have vertex degree (1,1,1,1,1,1,1,1); the "
            "symmetric top has degree (1,2,0,1,1,1,1,1)"
        ),
        "first_PP_flags": sum(pp_types.values()),
        "first_PP_topologies": dict(sorted(pp_types.items())),
        "absolute_root_square_constructed": False,
        "consequence": (
            "granting a physical symmetric collision cell with all 180 PP/"
            "AugP2 faces would make the unsigned route positive, but the "
            "transvection and canonical parent collection do not construct "
            "that cell"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    weights, active, residual, parent_data = xi_and_collection_audit()
    ledger = {
        "theorem": "h3 Xi_01 occurrence Spencer universal graph gate",
        "base_commits": BASE_COMMITS,
        "base_blob_sha256": BASE_BLOBS,
        "Xi01_parent_and_collection": parent_data,
        "minimal_graphs_and_H0":
            universal_graph_and_collection_audit(weights, active, residual),
        "first_PP_unary_and_reinsertion":
            pp_unary_reinsertion_audit(weights, active),
        "unsigned_vertex_transvection_shortcut":
            unsigned_transvection_shortcut_audit(),
        "verdict": (
            "The canonical occurrence resolution does not give an absolute "
            "Xi_01 boundary.  The H0-preserving universal graph gives "
            "d beta(Xi)=Xi_01-tau_01.  The occurrence-to-collection cylinder "
            "gives d Theta_Xi=Xi_01-R_01; its pulled-back R_01/24 dual kills "
            "the whole cylinder and reads one on both terms.  Only a new "
            "absolute R_01 (equivalently tau_01) landing fills Xi_01, and it "
            "lowers the collected H0 from 44 to 43.  Its 120 root/reinsertion-"
            "labelled PP faces and selected unary q01*H carrier remain part "
            "of that missing physical cell"
        ),
        "first_missing_absolute_datum": (
            "one source-labelled d eta_R=R_01 landing whose 120 occurrence "
            "PP faces give the retained carrier faces, whose varied-edge "
            "boundary compares the two complete 15-term unary rows, and "
            "whose opposite-root reinsertion lands the selected q01*H2345 "
            "class before the word/fine AugP2 and protected augmentations"
        ),
        "nonclaims": [
            "a monic graph is not called an absolute filler",
            "parent collection is not called annihilation of its nonzero image",
            "unlabelled unary rows are not called reinsertion-natural Spencer faces",
            "the symmetric unsigned collision polynomial is not called a physical row",
            "formal A+B return is not called an absolute root square",
        ],
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
    print("Xi_01 graph: H0 89 -> 89; RETAINED tau_01")
    print("occurrence collection: dTheta=Xi_01-R_01; NOT ABSOLUTE")
    print("first PP: 120 LABELLED; collected residual: 96 NONZERO")
    print("first unary/reinsertion: TWO 15-TERM ROWS, THEN q01*H CARRIER")
    print("unsigned root: FORMAL A+B, BUT SYMMETRIC COLLISION TOP NOT PHYSICAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
