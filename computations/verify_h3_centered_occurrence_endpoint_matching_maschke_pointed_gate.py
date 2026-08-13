#!/usr/bin/env python3
"""Audit the endpoint/matching Maschke primitive for the h=3 centered face.

On the 90 marked response occurrences, the full site action is transitive.
Its Reynolds idempotent is exactly the already computed coefficient
projector Pi_end Pi_match.  Hence the action bar has the explicit boundary

    d(-90 Av_g [g|e_f]) = 90 e_f - 1 = c_f.

This is an honest statement in the homotopy-orbit/action-groupoid complex,
but it is not a boundary in the fixed pointed source presentation.  Under
canonical retained-label transport each bar endpoint returns to e_f and the
boundary is zero.  Raw label forgetting gives c_f but adds an augmentation-
zero relation and lowers fixed-source H0.  The minimal presentation-
preserving cone retains one graph coordinate u_f with d b=c_f-u_f; its
pointed value is 90 and its first cotangent face is dc_f=90 df-dR.

After the matching projector the selected first-PP face is
dc_01=30 db_01-dR.  Residual matching flips fix the aggregate db_01, so
Maschke contraction only removes its termwise standard character module;
it does not remove this invariant selected face.  Target is zero on the
orbit-relative bar, while cap/ridge transport occurs only in the later
01211222/P3+K2 comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(6))
N = 90
PINS = {
    "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py":
        "0ef88312cead100120e4600ea3a2d0616262a96bf27726d07817610d11b43f59",
    "computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py":
        "24c5504111da4f284d9d01a535de544a44ea1bae75430d98761e093cc6ca8482",
    "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py":
        "620b3e54e8e6ee09a0b616d0259c8d109b0359645b20d35db5fb876c8e7e0311",
    "computations/verify_h3_matching_face_residual_flip_semidirect_gate.py":
        "0769314fa55e0978a24680a16f5f5bd4bad8b176322d9709cb42c8b73e025f1e",
    "computations/verify_h3_endpoint_projector_common_c2plus_private_curvature_gate.py":
        "011e1882f9391a2e9ca1b58adce0cefdd4b3ced602f5ba823e1b3bbdadfdf6ce",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
}
EXPECTED_LEDGER_SHA256 = (
    "33b91b934118c8d9608fe09e2db3b1a547cff51d8e559dab688bffd67ff7713b"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


def occurrences() -> tuple[tuple[int, int, tuple[tuple[int, int], ...]], ...]:
    answer = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            rest = tuple(site for site in SITES
                         if site not in (p_site, s_site))
            for matching in perfect_matchings(rest):
                answer.append((p_site, s_site, matching))
    require(len(answer) == len(set(answer)) == N,
            "the h=3 occurrence inventory changed")
    return tuple(answer)


def act(occurrence, permutation):
    p_site, s_site, matching = occurrence
    return (
        permutation[p_site],
        permutation[s_site],
        tuple(sorted(edge(permutation[left], permutation[right])
                     for left, right in matching)),
    )


def inverse(permutation):
    answer = [0] * len(permutation)
    for source, target in enumerate(permutation):
        answer[target] = source
    return tuple(answer)


def unit(index: int, size: int = N) -> tuple[Q, ...]:
    return tuple(Q(position == index) for position in range(size))


def add(left, right, right_scale=Q(1)):
    return tuple(Q(a) + Q(right_scale) * Q(b)
                 for a, b in zip(left, right, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


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


def apply_operator(vector, neighbors, lookup):
    return tuple(sum((vector[lookup[value]] for value in neighbors[item]), Q(0))
                 for item in lookup)


def matching_neighbors(occurrence):
    p_site, s_site, matching = occurrence
    rest = tuple(site for site in SITES if site not in (p_site, s_site))
    return tuple((p_site, s_site, other)
                 for other in perfect_matchings(rest) if other != matching)


def endpoint_neighbors(occurrence):
    p_site, s_site, matching = occurrence
    answer = []
    for selected in SITES:
        if selected in (p_site, s_site):
            continue
        mate = next(other for pair in matching if selected in pair
                    for other in pair if other != selected)
        remainder = tuple(pair for pair in matching if selected not in pair)
        answer.append((selected, s_site,
                       tuple(sorted(remainder + (edge(p_site, mate),)))))
        answer.append((p_site, selected,
                       tuple(sorted(remainder + (edge(s_site, mate),)))))
    require(len(answer) == len(set(answer)) == 8,
            ("endpoint degree changed", occurrence))
    return tuple(answer)


def polynomial_apply(vector, roots, operator):
    answer = vector
    for root in roots:
        image = operator(answer)
        answer = tuple(left - Q(root) * right
                       for left, right in zip(image, answer, strict=True))
    return answer


def projector_and_bar_audit():
    occ = occurrences()
    lookup = {item: index for index, item in enumerate(occ)}
    marked_value = (0, 1, ((2, 3), (4, 5)))
    marked = lookup[marked_value]
    all_one = (Q(1),) * N
    centered = add(scale(N, unit(marked)), all_one, -1)

    match = {item: matching_neighbors(item) for item in occ}
    endpoint = {item: endpoint_neighbors(item) for item in occ}
    apply_a = lambda vector: apply_operator(vector, match, lookup)
    apply_b = lambda vector: apply_operator(vector, endpoint, lookup)

    # Check the coefficient projector as an operator, not only on e_f.
    for index in range(N):
        basis = unit(index)
        match_flat = scale(Q(1, 3), add(apply_a(basis), basis))
        projected = scale(Q(1, 240),
                          polynomial_apply(match_flat, (-2, 2, 4), apply_b))
        require(projected == scale(Q(1, N), all_one),
                ("Pi_end Pi_match ceased to be Reynolds", index))

    group = tuple(permutations(SITES))
    orbit_counts = [0] * N
    raw_boundaries = []
    retained_transport_failures = []
    for permutation in group:
        image_value = act(marked_value, permutation)
        image = lookup[image_value]
        orbit_counts[image] += 1
        raw_boundaries.append(add(unit(image), unit(marked), -1))
        transported = act(image_value, inverse(permutation))
        if transported != marked_value:
            retained_transport_failures.append((permutation, transported))
    require(len(group) == 720 and set(orbit_counts) == {8},
            ("the S6 orbit/stabilizer changed", orbit_counts))
    require(not retained_transport_failures,
            "canonical retained-label transport stopped returning to e_f")

    reynolds = tuple(Q(value, len(group)) for value in orbit_counts)
    require(reynolds == scale(Q(1, N), all_one),
            "the group Reynolds average changed")
    averaged_bar_boundary = add(reynolds, unit(marked), -1)
    require(scale(-N, averaged_bar_boundary) == centered,
            "the explicit Maschke primitive lost c_f")
    require(rank(raw_boundaries) == N - 1,
            "raw action bars stopped spanning the augmentation ideal")

    # The word stabilizer cannot supply the orbit-marginal part of c_f.
    # Build S2 on {0,1} times S4 on the remaining sites.
    word_stabilizer = []
    for first in permutations((0, 1)):
        for rest in permutations((2, 3, 4, 5)):
            image = [0] * 6
            image[0], image[1] = first
            image[2], image[3], image[4], image[5] = rest
            word_stabilizer.append(tuple(image))
    stabilizer_orbit = sorted({lookup[act(marked_value, permutation)]
                               for permutation in word_stabilizer})
    require(len(word_stabilizer) == 48 and len(stabilizer_orbit) == 6,
            "the selected word-stabilizer orbit changed")
    require(any(centered[index] for index in range(N)
                if index not in stabilizer_orbit),
            "c_f unexpectedly entered the marked word-stabilizer orbit")

    return {
        "occurrence_count": N,
        "full_site_group_order": len(group),
        "marked_stabilizer_order": orbit_counts[marked],
        "full_orbit_size": len(set(lookup[act(marked_value, g)] for g in group)),
        "projector_identity": (
            "Pi_end Pi_match=(B+2)(B-2)(B-4)(A+I)/(240*3)=J_90/90"
        ),
        "projector_checked_on_all_basis_vectors": True,
        "Maschke_bar_primitive": "H_f=-90*(1/720) sum_g [g|e_f]",
        "bar_boundary": "d H_f=90e_f-1_90=c_f",
        "raw_bar_boundary_rank": rank(raw_boundaries),
        "canonical_retained_label_transport_boundary": 0,
        "canonical_transport_reason": "g e_f transported by g^-1 is e_f",
        "word_stabilizer_order": len(word_stabilizer),
        "marked_word_stabilizer_orbit_size": len(stabilizer_orbit),
        "word_stabilizer_can_make_full_cf": False,
        "interpretation": (
            "the positive primitive lives in the homotopy-orbit/coinvariant "
            "complex; raw folding to one fixed object imposes the new "
            "augmentation-ideal relations"
        ),
    }, occ, lookup, marked, centered


def pointed_cone_audit(occ, lookup, marked, centered):
    all_one = (Q(1),) * N
    old_h0 = N - rank((all_one,))
    raw_h0 = N - rank((all_one, centered))
    complete_extended = all_one + (Q(0),)
    graph_boundary = centered + (Q(-1),)
    graph_h0 = N + 1 - rank((complete_extended, graph_boundary))
    require((old_h0, raw_h0, graph_h0) == (89, 88, 89),
            ("the pointed cone rank changed", old_h0, raw_h0, graph_h0))

    other = next(index for index in range(N) if index != marked)
    evaluation = [Q(0)] * N
    evaluation[marked] = 1
    evaluation[other] = -1
    evaluation = tuple(evaluation)
    require(dot(all_one, evaluation) == 0
            and dot(centered, evaluation) == 90,
            "the normalized pointed counterguard changed")

    # Matching numerator: (A+I)c_f=3c_01.
    marked_value = occ[marked]
    fixed_fibre = tuple(index for index, value in enumerate(occ)
                        if value[:2] == marked_value[:2])
    require(len(fixed_fibre) == 3, "the selected matching fibre changed")
    b01 = tuple(Q(index in fixed_fibre) for index in range(N))
    c01 = add(scale(30, b01), all_one, -1)
    match = {item: matching_neighbors(item) for item in occ}
    apply_a = lambda vector: apply_operator(vector, match, lookup)
    require(add(apply_a(centered), centered) == scale(3, c01),
            "(A+I)c_f=3c_01 changed")

    # Exact selected PP quotient from the independently pinned literal audit.
    # Coordinates are (db01, sum of the other 29 endpoint fibres, all-D).
    complete_dR = (Q(1), Q(1), Q(0))
    all_d = (Q(0), Q(0), Q(1))
    selected_db01 = (Q(1), Q(0), Q(0))
    dc01 = (Q(29), Q(-1), Q(0))
    separator = (Q(1), Q(-1), Q(0))
    require(rank((complete_dR, all_d)) == 2
            and rank((complete_dR, all_d, selected_db01)) == 3,
            "the selected PP rank obstruction changed")
    require(dot(separator, complete_dR) == dot(separator, all_d) == 0
            and dot(separator, selected_db01) == 1,
            "the selected PP separator changed")
    require(scale(Q(1, 30), add(complete_dR, dc01)) == selected_db01,
            "db01=(dR+dc01)/30 changed")

    return {
        "fixed_source_with_complete_row_H0": old_h0,
        "after_raw_cf_bar_H0": raw_h0,
        "presentation_preserved_by_raw_fold": False,
        "minimal_relative_cone": "d b_f=c_f-u_f",
        "cone_H0": graph_h0,
        "retained_graph_coordinate": "u_f",
        "normalized_point": {
            "f": 1,
            "one_other_occurrence": -1,
            "R": 0,
            "c_f": 90,
            "required_u_f": 90,
        },
        "first_cotangent_face": "d u_f=d c_f=90 d f-dR",
        "anchor_consequence_if_graph_descends": "90[du_f]=[du]",
        "matching_identity": "(A+I)c_f=3c_01",
        "selected_matching_fibre_size": len(fixed_fibre),
        "selected_PP_identity": "dc_01=30 db_01-dR; db_01=(dR+dc_01)/30",
        "selected_PP_rank_before_then_after_db01": [2, 3],
        "selected_PP_primitive_dual": [1, -1, 0],
        "conclusion": (
            "a presentation-preserving pointed cone makes c_f homologous "
            "to u_f, not zero; killing u_f is exactly the missing centered "
            "occurrence/selected-PP source cell"
        ),
    }


def augmented_face_audit():
    return {
        "orbit_relative_target": {
            "value": 0,
            "reason": "the GHZ target is invariant under literal site permutations",
        },
        "fixed_word_target": {
            "status": "later conditional face",
            "face": "18-term endpoint target normal N_f",
            "warning": (
                "returning every moved word to 11:110000 by signed Weyl/Cartan "
                "paths is extra structure, not the action-groupoid bar"
            ),
        },
        "anchor": {
            "status": "FIRST POINTED PROPER FACE",
            "face": "u_f with du_f=90df-dR",
        },
        "q_first_PP": {
            "status": "OPEN INVARIANT FACE",
            "face": "six-term db01, equivalently centered dc01=30db01-dR",
            "residual_V4_action": (
                "fixes aggregate db01; Maschke contracts only the three "
                "termwise standard-character directions"
            ),
        },
        "cap_ridge": {
            "status": "NOT REACHED BEFORE THE POINTED/PP FACE",
            "grade": "01211222 / t*q_(v,N) / repeated P3+K2",
            "first_conditional_cell": "primitive p_(v,N): (Q,ores)=(-1,-1)",
        },
        "after_fixed_word_target_correction": {
            "known_residual": (
                "rank-two protected curvature C2,C3; one B-natural "
                "second-Hasse totalization would carry both"
            ),
        },
        "sharp_order": [
            "coefficient Maschke primitive exists in homotopy orbits",
            "pointed scalar/graph conormal u_f remains",
            "selected invariant PP face dc01/db01 remains",
            "fixed-word target cone and its C2,C3 curvature are later",
            "cap/ridge/q/eta-sigma transport is later and differently graded",
        ],
    }


def audit():
    pin_dependencies()
    projector, occ, lookup, marked, centered = projector_and_bar_audit()
    ledger = {
        "theorem": (
            "h3 endpoint/matching Maschke action-groupoid versus pointed "
            "centered occurrence gate"
        ),
        "pins": PINS,
        "projector_and_action_bar": projector,
        "pointed_relative_cone": pointed_cone_audit(
            occ, lookup, marked, centered),
        "augmented_faces": augmented_face_audit(),
        "verdict": (
            "Pi_end Pi_match is exactly the S6 Reynolds projector, so c_f "
            "has an explicit Maschke bar primitive in the action-groupoid "
            "complex.  Canonical retained-label transport sends that boundary "
            "to zero.  Raw folding produces c_f only by changing fixed-source "
            "H0.  The minimal pointed cone preserves H0 but retains u_f with "
            "du_f=90df-dR; after matching its first literal invariant face is "
            "dc01=30db01-dR.  Target is zero orbit-relatively, while fixed-word "
            "target/cap/ridge/q transport remains downstream."
        ),
        "scope": (
            "canonical h=3 90-occurrence response packet over characteristic "
            "zero; proves the coefficient/action-groupoid construction and "
            "the first pointed/PP no-go, not the missing physical graph cell"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("Pi_end Pi_match: EXACT S6 REYNOLDS PROJECTOR")
    print("homotopy-orbit Maschke bar: dH=c_f")
    print("canonical retained-label fold: boundary 0")
    print("raw fixed-object fold: CHANGES H0 89 -> 88")
    print("minimal pointed cone: c_f homologous to retained u_f")
    print("first physical face: du_f=90df-dR; then dc01=30db01-dR")
    print("target/cap: downstream; residual V4 does not kill aggregate db01")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
