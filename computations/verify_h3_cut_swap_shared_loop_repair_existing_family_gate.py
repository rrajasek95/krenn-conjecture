#!/usr/bin/env python3
"""Classify shared-loop C4 repairs and test the committed source families.

The three shared cut-swap labels have matchings 3,4,5 and repeated edge 02.
For each of the four equivariant support collapses, replacing one C4 in the
matching gives exactly four loop-free alternatives per shared label.  After
rho-equivariance these reduce to two target choices for the paired orbit
(pure-column orbits {0,5} or {2,3}) and two target choices for the fixed
orbit (pure columns 1 or 4).

These are exact candidate occurrence labels, not yet relative boundaries.
The committed frame-circuit result supplies the source typing of a same-word
C4 pair but explicitly not a binomial source row.  Moreover the existing
M_v, clean collision, and projected reduced-Eq families cannot furnish the
required repair: their literal pure-column coefficient vectors all have
augmentation zero.  A shared occurrence has augmentation one.  Adding a
pure r0 column restores augmentation but also contributes target=1 and
ainc=-1; every named repair family has both protected rows zero.  Hence the
smallest missing datum remains one protected-zero augmentation-one relative
column on each of the two rho orbits.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_frame_circuit_matching_lift_trichotomy.py":
        "e0bdd386a63b17b67038ef8e8d0faf15ff041a1e8cb9f6f138e6a781233d44f1",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_residual_q_reduced_eq_cap_factorization.py":
        "b6cea93a8a009fce3e97eac0b6321c1175686aa47bb374e82bed7f7e0f604cb4",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
}
EXPECTED_LEDGER_SHA256 = (
    "f6cc210b684071e9ad55416865fde99902b2709e742c6a12aee3437ac54151b1"
)

RHO = (0, 4, 2, 3, 1, 5)
SUPPORT_COLLAPSES = (
    (4, 2, 4, 1, 5, 3),
    (4, 2, 4, 3, 5, 1),
    (4, 5, 4, 1, 2, 3),
    (4, 5, 4, 3, 2, 1),
)
TARGET_ACTION = (5, 1, 3, 2, 4, 0)


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


def permute_edge(edge, permutation):
    return tuple(sorted(permutation[site] for site in edge))


def permute_matching(matching, permutation):
    return tuple(sorted(permute_edge(edge, permutation) for edge in matching))


def collapse_graph(matching, phi):
    graph = []
    for left, right in matching:
        edge = tuple(sorted((phi[left], phi[right])))
        if edge[0] == edge[1]:
            return None
        graph.append(edge)
    return tuple(sorted(graph))


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
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
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def unit(index, size=6):
    return tuple(Q(int(position == index)) for position in range(size))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "shared_repair_tangent",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "shared_repair_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "shared_repair_base",
    )
    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "shared_repair_literal",
    )
    reduced = load(
        "computations/verify_h3_residual_q_reduced_eq_cap_factorization.py",
        "shared_repair_reduced",
    )

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    pure_graphs = tuple(tuple(sorted((edge[0], edge[1])
                                    for edge in multiplier))
                        for multiplier, _boundary in pure)
    graph_index = {graph: index for index, graph in enumerate(pure_graphs)}
    require((left, right) == (3, 5) and len(pure) == len(graph_index) == 6,
            "the canonical six-column component changed")

    shared_indices = (3, 4, 5)

    def rho_index(index):
        return tangent.MATCHING_INDEX[
            permute_matching(tangent.MATCHINGS[index], RHO)
        ]

    require(tuple(rho_index(index) for index in shared_indices) == (5, 4, 3),
            "the shared rho orbit changed")

    collapse_records = []
    all_paired_target_orbits = set()
    all_fixed_target_choices = set()
    for values in SUPPORT_COLLAPSES:
        phi = dict(enumerate(values))
        alternatives = {}
        for shared_index in shared_indices:
            shared_matching = tangent.MATCHINGS[shared_index]
            candidates = []
            for candidate_index, candidate in enumerate(tangent.MATCHINGS):
                # A single C4 exchange of perfect matchings has one common
                # edge and four edges in the symmetric difference.
                if len(set(shared_matching) & set(candidate)) != 1:
                    continue
                image = collapse_graph(candidate, phi)
                if image not in graph_index:
                    continue
                candidates.append((candidate_index, graph_index[image]))
            require(len(candidates) == 4,
                    ("the C4 repair census changed", values, shared_index,
                     candidates))
            alternatives[shared_index] = tuple(candidates)

        paired = []
        for candidate_index, target_index in alternatives[3]:
            mate = rho_index(candidate_index)
            mate_record = next((record for record in alternatives[5]
                                if record[0] == mate), None)
            require(mate_record is not None
                    and mate_record[1] == TARGET_ACTION[target_index],
                    ("a paired repair lost equivariance", values,
                     candidate_index, mate_record))
            orbit = tuple(sorted((target_index, mate_record[1])))
            paired.append({
                "matching_choice": candidate_index,
                "rho_matching_choice": mate,
                "target_orbit": list(orbit),
            })
            all_paired_target_orbits.add(orbit)
        require({tuple(record["target_orbit"]) for record in paired}
                == {(0, 5), (2, 3)},
                ("paired target choices changed", values, paired))

        fixed_alternatives = alternatives[4]
        fixed_literal = tuple(record for record in fixed_alternatives
                              if rho_index(record[0]) == record[0])
        nonfixed = tuple(record for record in fixed_alternatives
                         if rho_index(record[0]) != record[0])
        require({record[0] for record in fixed_literal} == {7, 14}
                and {record[1] for record in fixed_literal} == {4}
                and {record[0] for record in nonfixed} == {1, 9}
                and {record[1] for record in nonfixed} == {1},
                ("fixed repair choices changed", values,
                 fixed_literal, nonfixed))
        all_fixed_target_choices.update((1, 4))
        collapse_records.append({
            "phi": list(values),
            "C4_alternatives_per_shared_label": {
                str(index): [[candidate, target] for candidate, target
                             in alternatives[index]]
                for index in shared_indices
            },
            "paired_orbit_choices": paired,
            "fixed_orbit_choices": [
                "rho-fixed matching 7 or 14 -> B4",
                "rho-average (matching 1 + matching 9)/2 -> B1",
            ],
        })
    require(all_paired_target_orbits == {(0, 5), (2, 3)}
            and all_fixed_target_choices == {1, 4},
            "the four collapses stopped having the common repair interface")

    # Existing exact M_v images: all four-corner alpha coefficient vectors
    # in the six pure columns.  They span precisely the augmentation-zero
    # hyperplane.  Clean collision differences lie in the same hyperplane;
    # projected reduced-Eq has no literal pure-column coefficient at all.
    mv_vectors = []
    for selected in combinations(range(6), 4):
        vector = [Q(0)] * 6
        for coefficient, index in zip(literal.ALPHA, selected, strict=True):
            vector[index] += coefficient
        mv_vectors.append(tuple(vector))
    collision_vectors = [
        tuple(left - right for left, right in zip(unit(i), unit(j), strict=True))
        for i, j in combinations(range(6), 2)
    ]
    reduced_eq_vector = (Q(0),) * 6
    known_vectors = mv_vectors + collision_vectors + [reduced_eq_vector]
    augmentation = (Q(1),) * 6
    require(len(mv_vectors) == 15
            and all(sum(vector) == 0 for vector in known_vectors)
            and rank(mv_vectors) == rank(known_vectors) == 5,
            "the known repair families left the augmentation-zero hyperplane")
    require(all(sum(a * b for a, b in zip(augmentation, vector,
                                          strict=True)) == 0
                for vector in known_vectors),
            "the occurrence-augmentation separator stopped killing known families")
    for target_index in (0, 1, 2, 3, 4, 5):
        require(rank(known_vectors) < rank(known_vectors + [unit(target_index)]),
                ("a unit shared occurrence entered the known span",
                 target_index))

    # The only named old column carrying one literal pure occurrence is r0.
    # Its protected (target,ainc)=(1,-1).  M_v, clean collision and reduced
    # Eq corrections all have (0,0), so none can turn that unit into the
    # protected-zero image required of the comparison.
    require(reduced.R0[:2] == (1, -1)
            and reduced.REDUCED_EQ[1:] == (0, 0, 0, 0)
            and literal.ALPHA == (Q(-1), Q(1), Q(1), Q(-1)),
            "the cap/reduced-Eq protected signatures changed")
    old_unit_signature = (Q(1), Q(1), Q(-1))  # occurrence,target,ainc
    named_family_signatures = ((Q(0), Q(0), Q(0)),) * len(known_vectors)
    require(old_unit_signature[1:] != (Q(0), Q(0))
            and all(signature == (Q(0), Q(0), Q(0))
                    for signature in named_family_signatures),
            "a named repair family acquired protected target/anchor output")

    ledger = {
        "theorem": "shared-loop C4 repair and existing-family gate",
        "pins": PINS,
        "shared_packet": {
            "matching_indices": list(shared_indices),
            "matchings": [
                [list(edge) for edge in tangent.MATCHINGS[index]]
                for index in shared_indices
            ],
            "rho_action": "3<->5, 4 fixed",
            "repeated_edge": "02",
        },
        "C4_repair_census": {
            "records": collapse_records,
            "candidate_C4_replacements_per_label_per_collapse": 4,
            "paired_rho_orbit_target_choices": [[0, 5], [2, 3]],
            "fixed_rho_orbit_target_choices": [1, 4],
            "distinct_target_orbit_assignments": 4,
            "typing_status": (
                "every replacement pair is a same-word single-C4 with one "
                "common matching edge, so it has the committed frame-circuit "
                "occurrence typing.  The frame theorem does not make that "
                "pair a binomial source boundary; a collision/relative C4 "
                "cell with the shifted repeated-edge direction is still needed"
            ),
        },
        "existing_family_span": {
            "pure_occurrence_module_dimension": 6,
            "Mv_alpha_columns": len(mv_vectors),
            "Mv_span_rank": rank(mv_vectors),
            "clean_collision_plus_Mv_plus_projected_reducedEq_rank":
                rank(known_vectors),
            "common_equation": "sum of six pure-column coefficients = 0",
            "shared_unit_augmentation": 1,
            "unit_in_existing_span": False,
            "primitive_separator": "pure-occurrence augmentation",
        },
        "protected_base_guard": {
            "old_r0_unit_signature_occurrence_target_ainc":
                [int(value) for value in old_unit_signature],
            "Mv_clean_collision_reducedEq_signature": [0, 0, 0],
            "can_cancel_r0_target_and_ainc": False,
            "smallest_missing_source_type": (
                "a protected-zero, occurrence-augmentation-one relative "
                "column for the rho-fixed shared orbit and one for the "
                "shared rho-pair.  Equivalently, construct one of the four "
                "C4 target-orbit assignments together with its shifted "
                "repeated-edge collision boundary"
            ),
        },
        "verdict": (
            "the loop 44 can be bypassed combinatorially by four C4 target-"
            "orbit assignments.  None is a committed physical comparison: "
            "the exact M_v/collision/reduced-Eq families are augmentation-zero, "
            "while a pure-column unit has uncancelled target and ainc"
        ),
        "nonclaims": [
            "the C4 candidate occurrence pairs are not promoted to source binomial rows",
            "arbitrary higher relative collision cells are not excluded",
            "the support-tail M_v construction remains valid independently of these zero-coefficient shared labels",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("shared-loop repair ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 shared-loop C4 repair census: PASS")
    print("paired orbit choices: {0,5} or {2,3}")
    print("fixed orbit choices: B1 or B4")
    print("existing Mv/collision/reduced-Eq span: augmentation-zero rank 5")
    print("remaining: two protected-zero augmentation-one relative images")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
