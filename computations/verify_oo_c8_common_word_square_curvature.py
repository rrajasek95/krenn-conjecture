#!/usr/bin/env python3
"""Discrete common-word Hessian audit on the 114 active OO regressions."""

from collections import Counter, defaultdict
from fractions import Fraction as F

import verify_oo_c8_active_leader_quotient as leader
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add_polynomial(target, polynomial, sign):
    for mask, coefficient in polynomial.items():
        target[mask] += sign * coefficient


def cofactor_word(arm, common_word, exclusive_colour):
    residual = tuple(vertex for vertex in base.VERTICES if vertex not in arm)
    colours = dict(zip(leader.COMMON, common_word, strict=True))
    exclusive = base.R if arm == frontier.ARMS[0] else base.Q
    colours[exclusive] = exclusive_colour
    return tuple(colours[vertex] for vertex in residual)


def hessian(polynomials, words):
    answer = defaultdict(F)
    for sign, word in zip((1, -1, -1, 1), words, strict=True):
        add_polynomial(answer, polynomials.get(word, {}), sign)
    return {mask: coefficient for mask, coefficient in answer.items() if coefficient}


def product(left, right):
    answer = defaultdict(F)
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            # A repeated source coordinate cannot occur twice in a matching
            # monomial product.  For the domain certificate we keep ordinary
            # Laurent multiplication, so exponent vectors add rather than
            # Boolean masks; encode them as tuples below.
            left_exponent = tuple(bool(left_mask & (1 << index)) for index in range(4))
            right_exponent = tuple(bool(right_mask & (1 << index)) for index in range(4))
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent, strict=True))
            answer[exponent] += left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def direct_commutator(blocks):
    first = base.direct_matrix(blocks, *frontier.ARMS[0])
    second = base.direct_matrix(blocks, *frontier.ARMS[1])
    first_second = base.matmul(first, second)
    second_first = base.matmul(second, first)
    return [
        [first_second[row][column] - second_first[row][column] for column in base.COLORS]
        for row in base.COLORS
    ]


def faces_for_words(first, second):
    differing = tuple(index for index, pair in enumerate(zip(first, second, strict=True)) if pair[0] != pair[1])
    distance = len(differing)
    if distance == 2:
        one, two = differing
        corner_one = list(first)
        corner_two = list(first)
        corner_one[one] = second[one]
        corner_two[two] = second[two]
        return ((first, tuple(corner_one), tuple(corner_two), second),)
    if distance == 1:
        changed = differing[0]
        faces = []
        for transverse in range(len(first)):
            if transverse == changed:
                continue
            for alternate in base.COLORS:
                if alternate == first[transverse]:
                    continue
                upper_first = list(first)
                upper_second = list(second)
                upper_first[transverse] = alternate
                upper_second[transverse] = alternate
                faces.append((first, second, tuple(upper_first), tuple(upper_second)))
        return tuple(faces)
    return ()


def main():
    blocks = base.build_packet()
    regressions = leader.no_compound_regressions(blocks)
    commutator = direct_commutator(blocks)
    require(commutator == [[0, 0, 0], [-1, 0, 0], [0, 0, 0]], "direct commutator changed")

    distance_census = Counter()
    face_census = Counter()
    leader_coefficients = Counter()
    transverse_choice_census = Counter()
    first_long_guard = None
    for support in regressions:
        records = tuple(
            leader.leading_record(blocks, support, arm)
            for arm in frontier.ARMS
        )
        distance = sum(
            first != second
            for first, second in zip(records[0]["common"], records[1]["common"], strict=True)
        )
        distance_census[distance] += 1
        if distance == 0:
            face_census["proportional_word"] += 1
            continue
        faces = faces_for_words(records[0]["common"], records[1]["common"])
        if not faces:
            face_census["no_common_two_face"] += 1
            if distance and first_long_guard is None:
                first_long_guard = (support, distance, records)
            continue
        face_audits = []
        for face in faces:
            hessians = []
            target_mixed = True
            for arm, record in zip(frontier.ARMS, records, strict=True):
                residual = tuple(vertex for vertex in base.VERTICES if vertex not in arm)
                exclusive = base.R if arm == frontier.ARMS[0] else base.Q
                exclusive_position = residual.index(exclusive)
                exclusive_colour = record["word"][exclusive_position]
                face_words = tuple(
                    cofactor_word(arm, common_word, exclusive_colour)
                    for common_word in face
                )
                target_mixed &= all(len(set(word)) > 1 for word in face_words)
                polynomials = frontier.cofactor_polynomials(blocks, support, arm)
                hessians.append(hessian(polynomials, face_words))
            if all(hessians) and product(*hessians):
                face_audits.append((target_mixed, hessians))
        require(face_audits, f"every cofactor face Hessian vanished: {support}")
        clean_faces = tuple(audit for audit in face_audits if audit[0])
        transverse_choice_census[(distance, len(faces), len(clean_faces))] += 1
        target_mixed, hessians = clean_faces[0] if clean_faces else face_audits[0]
        leader_coefficients[
            (
                hessians[0].get(records[0]["mask"], 0),
                hessians[1].get(records[1]["mask"], 0),
            )
        ] += 1
        target_kind = "mixed_target" if target_mixed else "target_contaminated"
        face_census[f"distance_{distance}_nonzero_square_{target_kind}"] += 1

    print("alternating-C8 common-word square curvature: PASS")
    print(f"distance census={dict(sorted(distance_census.items()))}")
    print(f"square disposition={dict(sorted(face_census.items()))}")
    print(f"leader Hessian coefficients={dict(sorted(leader_coefficients.items()))}")
    print(f"transverse clean-choice census={dict(sorted(transverse_choice_census.items()))}")
    print(f"direct-block commutator={commutator}")
    print(f"first distance>=3 guard={first_long_guard}")

    require(
        distance_census == Counter({1: 65, 3: 31, 5: 10, 4: 4, 2: 3, 0: 1}),
        "common-word distance census changed",
    )
    require(
        face_census
        == Counter({"distance_1_nonzero_square_mixed_target": 48,
                    "distance_1_nonzero_square_target_contaminated": 17,
                    "no_common_two_face": 45,
                    "distance_2_nonzero_square_mixed_target": 3,
                    "proportional_word": 1}),
        "common-word square disposition changed",
    )
    require(
        transverse_choice_census
        == Counter({(1, 8, 8): 45, (1, 8, 0): 17,
                    (1, 8, 7): 3, (2, 1, 1): 3}),
        "transverse square-choice census changed",
    )


if __name__ == "__main__":
    main()
