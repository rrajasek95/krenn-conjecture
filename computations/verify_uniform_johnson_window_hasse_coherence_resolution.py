#!/usr/bin/env python3
"""Verify the all-m Johnson-window Hasse coherence calculation.

For m=h-1 tail edges, h=3 windows are the two-subsets of [m].  One-edge
overlaps form J(m,2)=L(K_m).  Attach one inherited triangle on every
three-set and the three disjoint-edge Beck--Chevalley squares on every
four-set.  Over Q this 2-complex has H1=0.  Its H2 dimension is

    3*C(m,4)-2*C(m,3)+C(m,2)-1.

The first nonzero case is m=5, where H2 is the sign-twisted standard S5
module.  Five oriented 3-cell boundaries B_a span it with sum B_a=0.  On
m=6, the six embedded five-set packets have effective domain dimension 24,
image rank 19 and five overlap relations.  Bounded exact modular checks show
that embedded five-set packets span H2 through m=9; the paired note gives the
all-m Boolean-Hasse deletion-resolution proof and identifies all higher
coherence modules.

The final ledger distinguishes fixed-tail coherence from full source
coverage.  One fixed four-site h=3 partition covers only
3*(2m-5)!! of (2m-1)!! tail matchings.  Strong Hasse-linearity prolongs a
single natural Phi_KS,r0/P_f on each fixed tail, but normalized descent over
the remaining matching cover is a separate physical datum.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h5_pointed_phi_two_spectator_beck_chevalley_coherence.py":
        "55f363146627bf44974d28556bd669b4c1908cab9bb187b9a389e2cbd23fd650",
    "notes/h5-pointed-phi-two-spectator-beck-chevalley-coherence.md":
        "c56d667abc5e4d5396a76972c383e87412dd74ebdb25b029e2d8e8a08307f365",
    "computations/verify_h4_pointed_phi01_fixed_tail_h3_restriction_gate.py":
        "db1f9c4ccdf8b95cdbc681427ce5caa473385293f0e49f9817b185707e93e5b2",
    "notes/h4-pointed-phi01-fixed-tail-h3-restriction-gate.md":
        "78a1dc43506279ef639685d6053eaecd683d12937f503a01c3016f62302b46f0",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "notes/h3-hasse-coproduct-cosimplicial-totalization.md":
        "9bb749b3b45a6b0248699bf54364cb304f89e01a4a4ad654963aad3534893ba4",
    "computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py":
        "0eedcb3f03e98ea18b549e2b6e21d7082cf368d8e3bc77fd3f104a178104c25a",
    "notes/uniform-hyperbolic-collision-pp-augp2-spectator-naturality-gate.md":
        "73fd2ff870db0d5344255cee1f2b4008bc19ba5058114f51b312d5a011eb760d",
}
EXPECTED_LEDGER_SHA256 = (
    "f28171256cfd416de9b7813b3fa2935da8f02fdabf811fecd6eb763a792b5799"
)
ODD_PRIME = 1_000_003

Window = tuple[int, int]
GraphEdge = tuple[Window, Window]
Face = tuple[Window, ...]
Vector = tuple[int, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def odd_double_factorial(value: int) -> int:
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def rank_mod(vectors: tuple[Vector, ...] | list[Vector], prime: int) -> int:
    if not vectors:
        return 0
    work = [[entry % prime for entry in vector] for vector in vectors]
    width = len(work[0])
    require(all(len(vector) == width for vector in work), "rank width")
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], prime - 2, prime)
        work[pivot_row] = [(entry * inverse) % prime
                           for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [(entry - value * base) % prime
                         for entry, base in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def rank_q(vectors: tuple[Vector, ...] | list[Vector]) -> int:
    if not vectors:
        return 0
    work = [list(map(Q, vector)) for vector in vectors]
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * base for entry, base in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


@dataclass(frozen=True)
class JohnsonModel:
    m: int
    vertices: tuple[Window, ...]
    edges: tuple[GraphEdge, ...]
    faces: tuple[Face, ...]
    face_names: tuple[str, ...]
    face_supports: tuple[frozenset[int], ...]
    face_boundaries: tuple[Vector, ...]


def canonical_window(left: int, right: int) -> Window:
    require(left != right, "loop window")
    return tuple(sorted((left, right)))


def face_boundary(vertices: tuple[Window, ...], edges: tuple[GraphEdge, ...],
                  face: Face) -> Vector:
    answer = [0] * len(edges)
    for left, right in zip(face, face[1:] + face[:1]):
        oriented = (left, right)
        edge = tuple(sorted(oriented, key=vertices.index))
        require(edge in edges, ("non-Johnson face edge", face, edge))
        answer[edges.index(edge)] += 1 if edge == oriented else -1
    return tuple(answer)


def johnson_model(m: int) -> JohnsonModel:
    require(m >= 2, "m must be at least two")
    vertices = tuple(combinations(range(m), 2))
    edges = tuple((left, right) for left, right in combinations(vertices, 2)
                  if len(set(left) & set(right)) == 1)
    faces: list[Face] = []
    names: list[str] = []
    supports: list[frozenset[int]] = []
    for triple in combinations(range(m), 3):
        a, b, c = triple
        faces.append(((a, b), (a, c), (b, c)))
        names.append("T" + "".join(map(str, triple)))
        supports.append(frozenset(triple))
    for quadruple in combinations(range(m), 4):
        a, b, c, d = quadruple
        squares = (
            ((a, b), (a, c), (c, d), (b, d)),
            ((a, b), (a, d), (c, d), (b, c)),
            ((a, c), (a, d), (b, d), (b, c)),
        )
        for index, square in enumerate(squares):
            faces.append(square)
            names.append("Q" + "".join(map(str, quadruple)) +
                         f"_{index}")
            supports.append(frozenset(quadruple))
    boundaries = tuple(face_boundary(vertices, edges, face) for face in faces)
    return JohnsonModel(m, vertices, edges, tuple(faces), tuple(names),
                        tuple(supports), boundaries)


def vertex_boundary(model: JohnsonModel, edge_vector: Vector) -> Vector:
    require(len(edge_vector) == len(model.edges), "edge-vector width")
    answer = [0] * len(model.vertices)
    for coefficient, (left, right) in zip(edge_vector, model.edges,
                                           strict=True):
        answer[model.vertices.index(left)] -= coefficient
        answer[model.vertices.index(right)] += coefficient
    return tuple(answer)


def add(*vectors: Vector) -> Vector:
    require(vectors and all(len(vector) == len(vectors[0])
                            for vector in vectors), "add width")
    return tuple(sum(entries) for entries in zip(*vectors, strict=True))


def scaled(value: int, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


def four_vertex_star_identity_audit() -> dict[str, object]:
    model = johnson_model(4)
    index = {name: position for position, name in enumerate(model.face_names)}
    star = face_boundary(model.vertices, model.edges,
                         ((0, 1), (0, 2), (0, 3)))
    right = add(
        model.face_boundaries[index["T012"]],
        scaled(-1, model.face_boundaries[index["T013"]]),
        model.face_boundaries[index["T023"]],
        model.face_boundaries[index["T123"]],
        model.face_boundaries[index["Q0123_0"]],
        scaled(-1, model.face_boundaries[index["Q0123_1"]]),
        model.face_boundaries[index["Q0123_2"]],
    )
    require(scaled(2, star) == right,
            "four-vertex star reduction identity changed")
    return {
        "oriented_identity": (
            "2*S_0(1,2,3)=T012-T013+T023+T123+Q0-Q1+Q2"
        ),
        "identity_verified_coefficientwise": True,
        "denominator_needed": 2,
        "line_graph_cycle_lemma": (
            "cycles of L(K_m) are generated by K_m triangle images and "
            "triangles in vertex-star cliques"
        ),
        "consequence_over_Q": (
            "top triangles and BC squares span every Johnson cycle"
        ),
        "characteristic_two_warning": (
            "the star reduction cannot divide by two; the bounded mod-2 "
            "audit retains one H1 class for every m>=4"
        ),
    }


def h2_formula(m: int) -> int:
    return 3 * choose(m, 4) - 2 * choose(m, 3) + choose(m, 2) - 1


def bounded_johnson_rank_audit() -> dict[str, object]:
    records = []
    for m in range(2, 10):
        model = johnson_model(m)
        vertices = choose(m, 2)
        edges = 3 * choose(m, 3)
        triangles = choose(m, 3)
        squares = 3 * choose(m, 4)
        require(len(model.vertices) == vertices
                and len(model.edges) == edges
                and len(model.faces) == triangles + squares,
                ("Johnson counts", m))
        require(all(vertex_boundary(model, boundary) == (0,) * vertices
                    for boundary in model.face_boundaries),
                ("a face stopped being a cycle", m))
        edge_rank = 0 if vertices == 1 else vertices - 1
        cycle_dimension = edges - edge_rank
        odd_rank = rank_mod(model.face_boundaries, ODD_PRIME)
        require(odd_rank == cycle_dimension,
                ("odd-characteristic face rank", m, odd_rank,
                 cycle_dimension))
        mod2_rank = rank_mod(model.face_boundaries, 2)
        expected_mod2_h1 = 1 if m >= 4 else 0
        require(cycle_dimension - mod2_rank == expected_mod2_h1,
                ("mod-two Johnson H1", m, cycle_dimension, mod2_rank))
        h2 = len(model.faces) - odd_rank
        require(h2 == h2_formula(m), ("H2 formula", m, h2))
        records.append({
            "m": m,
            "h": m + 1,
            "vertices": vertices,
            "edges": edges,
            "top_triangles": triangles,
            "BC_squares": squares,
            "cycle_space_dimension": cycle_dimension,
            "face_boundary_rank_over_Q": odd_rank,
            "H1_over_Q": 0,
            "H2_over_Q": h2,
            "H1_over_F2": expected_mod2_h1,
        })
    require([record["H2_over_Q"] for record in records[1:7]] ==
            [0, 0, 4, 19, 55, 125],
            "the m=3..8 H2 sequence changed")
    return {
        "records": records,
        "closed_counts": {
            "V": "C(m,2)",
            "E": "3*C(m,3)",
            "triangles": "C(m,3)",
            "BC_squares": "3*C(m,4)",
            "cycle_dimension": "3*C(m,3)-C(m,2)+1",
            "face_rank_over_Q": "3*C(m,3)-C(m,2)+1",
            "H1_over_Q": 0,
            "H2_over_Q": "3*C(m,4)-2*C(m,3)+C(m,2)-1",
        },
        "first_nonzero_H2": {"m": 5, "h": 6, "dimension": 4},
        "scope": (
            "odd-prime rank plus the cycle-space upper bound certifies the "
            "displayed rational ranks for m<=9; the all-m proof is the "
            "line-graph generator lemma and four-vertex identity"
        ),
    }


def cycle_sign(sequence: list[Window], canonical: Face) -> int:
    for position in range(len(sequence)):
        if tuple(sequence[position:] + sequence[:position]) == canonical:
            return 1
    reversed_sequence = list(reversed(sequence))
    for position in range(len(sequence)):
        if tuple(reversed_sequence[position:] +
                 reversed_sequence[:position]) == canonical:
            return -1
    raise RuntimeError(("cycles have different vertex sets", sequence,
                        canonical))


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(permutation[left] > permutation[right]
                     for left in range(len(permutation))
                     for right in range(left + 1, len(permutation)))
    return -1 if inversions % 2 else 1


def act_window(window: Window, permutation: tuple[int, ...]) -> Window:
    return canonical_window(permutation[window[0]], permutation[window[1]])


def act_face_coefficients(model: JohnsonModel, coefficients: Vector,
                          permutation: tuple[int, ...]) -> Vector:
    require(len(coefficients) == len(model.faces)
            and len(permutation) == model.m, "face action width")
    answer = [0] * len(model.faces)
    face_sets = {frozenset(face): index
                 for index, face in enumerate(model.faces)}
    require(len(face_sets) == len(model.faces), "face vertex sets collide")
    for coefficient, face in zip(coefficients, model.faces, strict=True):
        if not coefficient:
            continue
        moved = [act_window(window, permutation) for window in face]
        index = face_sets[frozenset(moved)]
        answer[index] += coefficient * cycle_sign(moved, model.faces[index])
    return tuple(answer)


def face_relation_boundary(model: JohnsonModel, coefficients: Vector) -> Vector:
    require(len(coefficients) == len(model.faces), "relation width")
    answer = [0] * len(model.edges)
    for coefficient, boundary in zip(coefficients, model.face_boundaries,
                                      strict=True):
        for index, value in enumerate(boundary):
            answer[index] += coefficient * value
    return tuple(answer)


def canonical_five_relations() -> tuple[JohnsonModel, tuple[Vector, ...]]:
    model = johnson_model(5)
    coefficient = {
        "T123": -1, "T124": 1, "T134": -1, "T234": 1,
        "Q0123_0": -1, "Q0123_1": 1, "Q0123_2": -1,
        "Q0124_0": 1, "Q0124_1": -1, "Q0124_2": 1,
        "Q0134_0": -1, "Q0134_1": 1, "Q0134_2": -1,
        "Q0234_0": 1, "Q0234_1": -1, "Q0234_2": 1,
    }
    b0 = tuple(coefficient.get(name, 0) for name in model.face_names)
    relations = []
    for distinguished in range(5):
        permutation = list(range(5))
        permutation[0], permutation[distinguished] = (
            permutation[distinguished], permutation[0]
        )
        permutation = tuple(permutation)
        moved = act_face_coefficients(model, b0, permutation)
        relations.append(scaled(permutation_sign(permutation), moved))
    return model, tuple(relations)


def s5_standard_three_cell_audit() -> dict[str, object]:
    model, relations = canonical_five_relations()
    require(all(face_relation_boundary(model, relation) ==
                (0,) * len(model.edges) for relation in relations),
            "one five-tail relation stopped being an H2 cycle")
    require(add(*relations) == (0,) * len(model.faces)
            and rank_q(relations) == 4,
            "five labelled relations stopped spanning rank four")

    # Verify the full signed S5 covariance, not only character values.
    for permutation in permutations(range(5)):
        permutation = tuple(permutation)
        sign = permutation_sign(permutation)
        for distinguished in range(5):
            moved = act_face_coefficients(
                model, relations[distinguished], permutation
            )
            require(moved == scaled(sign,
                                    relations[permutation[distinguished]]),
                    ("signed-standard action", permutation, distinguished))
    return {
        "m": 5,
        "h": 6,
        "H2_dimension": 4,
        "labelled_candidate_3_cells": 5,
        "boundary_relation": "sum_a boundary(K_a)=0",
        "boundary_rank": 4,
        "S5_action": "sigma boundary(K_a)=sgn(sigma) boundary(K_sigma(a))",
        "H2_representation": "sgn tensor Std_5",
        "ordinary_Std_5_without_orientation_twist": False,
        "physical_interpretation": (
            "five oriented triple-spectator Hasse cells with one local "
            "sum relation are the minimal natural h=6 coherence family"
        ),
    }


def embed_local_relation(local: JohnsonModel, relation: Vector,
                         labels: tuple[int, ...],
                         global_model: JohnsonModel) -> Vector:
    require(local.m == len(labels) == 5, "local embedding labels")
    global_face_sets = {frozenset(face): index
                        for index, face in enumerate(global_model.faces)}
    answer = [0] * len(global_model.faces)
    for coefficient, face in zip(relation, local.faces, strict=True):
        if not coefficient:
            continue
        moved = [canonical_window(labels[left], labels[right])
                 for left, right in face]
        index = global_face_sets[frozenset(moved)]
        answer[index] += coefficient * cycle_sign(
            moved, global_model.faces[index]
        )
    return tuple(answer)


def higher_local_five_set_audit() -> dict[str, object]:
    local, relations = canonical_five_relations()
    records = []
    for m in range(5, 10):
        model = johnson_model(m)
        embedded = []
        for labels in combinations(range(m), 5):
            embedded.extend(embed_local_relation(local, relation, labels,
                                                 model)
                            for relation in relations)
        span_rank = rank_mod(embedded, ODD_PRIME)
        expected = h2_formula(m)
        effective_local_domain = 4 * choose(m, 5)
        require(span_rank == expected
                and all(face_relation_boundary(model, relation) ==
                        (0,) * len(model.edges) for relation in embedded),
                ("local five-set H2 generation", m, span_rank, expected))
        records.append({
            "m": m,
            "h": m + 1,
            "raw_labelled_3_cells": 5 * choose(m, 5),
            "local_sum_relations": choose(m, 5),
            "effective_local_3_cell_domain": effective_local_domain,
            "boundary_span_rank": span_rank,
            "higher_overlap_kernel": effective_local_domain - span_rank,
        })
    require(records[1] == {
        "m": 6,
        "h": 7,
        "raw_labelled_3_cells": 30,
        "local_sum_relations": 6,
        "effective_local_3_cell_domain": 24,
        "boundary_span_rank": 19,
        "higher_overlap_kernel": 5,
    }, "the six-tail five-set overlap calculation changed")
    return {
        "records": records,
        "all_m_Hasse_resolution_modules": (
            "C_r=direct_sum_{|A|=r+2}(sgn_A tensor Std_A), "
            "dim C_r=(r+1)*C(m,r+2), for r>=3"
        ),
        "differential": (
            "alternating labelled deletion/restriction; coassociativity "
            "makes consecutive maps compose to zero"
        ),
        "H2_generation": (
            "the r=3 five-set cells map onto H2(X_m); their kernel is the "
            "image of r=4 six-set cells, recursively"
        ),
        "first_higher_overlap": (
            "m=6: six local five-set packets have dimension 24 and image "
            "rank 19, leaving the sign-standard five-dimensional six-set "
            "overlap supplied by the next Hasse module"
        ),
        "bounded_exact_generation_check": "m=5..9 over odd prime 1000003",
    }


def higher_module_euler_audit() -> dict[str, object]:
    records = []
    for m in range(5, 15):
        alternating = 0
        terms = []
        for degree in range(3, m - 1):
            dimension = (degree + 1) * choose(m, degree + 2)
            sign = -1 if (degree - 3) % 2 else 1
            alternating += sign * dimension
            terms.append({"degree": degree, "dimension": dimension,
                          "Euler_sign": sign})
        require(alternating == h2_formula(m),
                ("higher Hasse Euler identity", m, alternating,
                 h2_formula(m)))
        records.append({"m": m, "H2": h2_formula(m),
                        "higher_module_terms": terms})
    return {
        "records": records,
        "closed_identity": (
            "H2(X_m)=sum_{r=3}^{m-2}(-1)^(r-3)(r+1)C(m,r+2)"
        ),
        "coherence_consequence": (
            "the 2-complex has nonzero H2 from m=5 onward, so triangles "
            "and squares prove path independence but not all higher "
            "coherence; the full Hasse deletion tower is essential"
        ),
    }


def fixed_partition_coverage_audit() -> dict[str, object]:
    records = []
    for m in range(2, 10):
        total = odd_double_factorial(2 * m - 1)
        fixed = (total if m == 2 else
                 3 * odd_double_factorial(2 * m - 5))
        # At m=2 the fixed four-site window is already the whole tail.
        presentations = choose(m, 2)
        remaining = total - fixed
        require(0 <= remaining < total or m == 2,
                ("fixed partition coverage", m, fixed, total))
        records.append({
            "m": m,
            "h": m + 1,
            "total_tail_matchings": total,
            "fixed_four_site_partition_matchings": fixed,
            "remaining_cross_partition_matchings": remaining,
            "h3_window_presentations_per_full_matching": presentations,
            "fixed_partition_fraction": (
                "1" if m == 2 else "3/((2m-1)(2m-3))"
            ),
        })
    return {
        "records": records,
        "closed_form": {
            "total": "(2m-1)!!",
            "fixed_partition_for_m>=3": "3*(2m-5)!!",
            "remaining_for_m>=3": "(2m-1)!!-3*(2m-5)!!",
            "coverage_fraction_for_m>=3": "3/((2m-1)(2m-3))",
            "window_multiplicity": "C(m,2)",
        },
        "remaining_descent_datum": (
            "a normalized source-labelled Cech/coequalizer descent over "
            "all C(m,2) window presentations of every full matching, "
            "retaining word/fine/repeated/operation and all protected rows, "
            "and landing in the complete physical source/terminal block"
        ),
        "division_available_over_Q": "divide the window sum by C(m,2)",
        "why_division_is_not_descent": (
            "normalization fixes multiplicity but does not construct the "
            "labelled overlap maps or prove physical-source exhaustivity"
        ),
    }


def conditional_all_h_prolongation() -> dict[str, object]:
    return {
        "hypotheses": [
            "one pointed normalized source-labelled Phi_KS,r0/P_f schema, "
            "natural in every labelled two-edge h3 window and carrying its "
            "selected db01 plus all protected cap rows",
            "a strong symmetric-monoidal action of the full oriented "
            "Boolean/matching Hasse species on the physical complexes",
            "chain Leibniz, graded shuffle, restriction/reinsertion "
            "Beck-Chevalley, the five-set K_a cells and every higher "
            "alternating deletion coherence",
            "Hasse-linearity of PP/AugP2, target, B/Eq, M, anchor/q, W, "
            "ordinary residue, P_f, ridge, eta and sigma",
        ],
        "fixed_tail_conclusion": (
            "for every h>=3 and every fixed full tail matching, Phi has a "
            "window-independent coherent prolongation; H1=0 makes all "
            "one-edge paths agree and the higher Hasse modules kill H2 and "
            "all subsequent coherence kernels"
        ),
        "new_operation_generator_beyond_Phi": False,
        "higher_cells_are": (
            "source Hasse/Beck-Chevalley coherences, not new response-to-cap "
            "operation switches"
        ),
        "does_not_imply_full_PAComp": True,
        "additional_global_hypothesis": (
            "normalized complete matching-cover descent/exhaustivity as "
            "stated in the coverage ledger"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform Johnson-window Hasse coherence resolution",
        "pins": PINS,
        "four_vertex_cycle_reduction": four_vertex_star_identity_audit(),
        "bounded_ranks_and_all_m_formulas": bounded_johnson_rank_audit(),
        "first_physical_three_cell_target": s5_standard_three_cell_audit(),
        "local_five_set_higher_resolution": higher_local_five_set_audit(),
        "higher_module_Euler_identity": higher_module_euler_audit(),
        "conditional_all_h_prolongation": conditional_all_h_prolongation(),
        "fixed_partition_coverage_and_descent":
            fixed_partition_coverage_audit(),
        "verdict": (
            "Over Q, the triangle and disjoint-edge Beck-Chevalley face "
            "boundaries span the cycle space of J(m,2) for every m, so H1 "
            "vanishes and fixed-tail path independence has no new operation "
            "obstruction.  The 2-complex has H2 dimension "
            "3*C(m,4)-2*C(m,3)+C(m,2)-1, first equal to four at m=5/h=6. "
            "That first coherence is sgn tensor Std_5: five oriented "
            "three-cells with one sum relation.  Their five-set instances "
            "generate all higher H2, with six-set and subsequent Hasse "
            "modules supplying their overlap relations.  Hence one natural "
            "Phi plus strong full Hasse-linearity prolongs coherently on "
            "each fixed tail.  Complete matching-cover descent remains a "
            "separate physical input."
        ),
        "scope": (
            "all-m rational combinatorial proof with exact finite rank, "
            "signed-S5 and local-generation checks.  It identifies the "
            "required physical higher-cell representation but does not "
            "construct those cells in the decorated PP/AugP2 source, prove "
            "protected-row Hasse-linearity, matching-cover exhaustivity or "
            "existence of Phi.  Characteristic two retains a separate H1 "
            "class and is outside the characteristic-zero proof."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform Johnson coherence ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "h1", "h2", "s5",
                                           "higher", "coverage", "theorem"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"uniform Johnson-window coherence ({arguments.mode}): PASS")
        print("H1(X_m;Q)=0 for all m (line-graph triangles + BC squares)")
        print("H2=3*C(m,4)-2*C(m,3)+C(m,2)-1")
        print("first H2 at m=5: sgn tensor Std_5, dimension 4")
        print("m=6 local 3-cells: effective 24 -> boundary rank 19; kernel 5")
        print("one Phi + strong full Hasse-linearity: fixed-tail prolongation")
        print("complete matching-cover descent: STILL SEPARATE")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
