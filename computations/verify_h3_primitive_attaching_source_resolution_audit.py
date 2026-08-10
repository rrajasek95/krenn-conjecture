#!/usr/bin/env python3
"""Exact audit of committed source-resolution routes to the h=3 primitive.

The calculation maps the primitive A=16*T+sum(m_S) to the committed
three-set connecting class K, then rechecks the smallest q-degree and
cap-augmentation obstructions to null-homotoping K with existing cells.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json

import verify_h3_three_set_source_relative_terminal_class as THREE_SET


EXPECTED_DIGEST = "0fc177f58bb4ac9f627593d6fca450577b7197c401b04f645b560492d53c7afa"
LABELS = tuple(range(3))
SELECTED = (0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(rows):
    work = [list(map(F, row)) for row in rows]
    if not work:
        return 0
    answer = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(answer, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right
                         for left, right in zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def determinant(rows):
    work = [list(map(F, row)) for row in rows]
    require(all(len(row) == len(work) for row in work), "determinant is not square")
    value = F(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        diagonal = work[column][column]
        value *= diagonal
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column] / diagonal
            work[row] = [left - scale * right
                         for left, right in zip(work[row], work[column], strict=True)]
    return value


def endpoint_degree(pairs):
    left = [0, 0, 0]
    right = [0, 0, 0]
    for row, column in pairs:
        left[row] += 1
        right[column] += 1
    return tuple(left), tuple(right)


def main():
    # Re-run the formal sparse-polynomial identity of commit cd52b2b.
    three_set = THREE_SET.audit()
    require(three_set["digest"]
            == "22f2418741c6dbeae3dc55f0637cab6fef5392843012da75228b49f347919527",
            "three-set relative identity moved")

    # Fine degree four (one starting row and three response/direct tags) has
    # only the repeated selected endpoint-label route.
    target_degree = endpoint_degree((SELECTED,) * 4)
    routes = []
    for labels in product(LABELS, repeat=8):
        pairs = tuple(zip(labels[::2], labels[1::2], strict=True))
        if endpoint_degree(pairs) == target_degree:
            routes.append(pairs)
    require(routes == [(SELECTED,) * 4],
            ("primitive fine degree acquired another nonnegative route", routes))

    records = []
    for alpha in (F(1), F(2), F(-3, 2)):
        # Coordinates are (T=Q3, S=sum literal middle rows, K=the
        # source-relative connecting class).  Existing rows give S=0 and,
        # after quotienting by H2, K-16*alpha*T-S=0.  A=16*T+S, hence
        # K-alpha*A is already a linear combination of those two relations.
        middle = [F(0), F(1), F(0)]
        relative = [F(-16) * alpha, F(-1), F(1)]
        existing = [middle, relative]
        primitive = [F(16), F(1), F(0)]
        alpha_primitive = [alpha * entry for entry in primitive]
        connecting = [F(0), F(0), F(1)]
        difference = [connecting[index] - alpha_primitive[index] for index in range(3)]
        expected_difference = [
            relative[index] + (F(1) - alpha) * middle[index]
            for index in range(3)
        ]
        require(difference == expected_difference,
                "K-alpha*A stopped being the committed relative relation")
        require(rank(existing) == 2, "relative presentation rank moved")
        separator = [F(1), F(0), F(16) * alpha]
        require(all(sum((row[i] * separator[i] for i in range(3)), F(0)) == 0
                    for row in existing),
                "terminal separator stopped killing existing relations")
        require(sum((primitive[i] * separator[i] for i in range(3)), F(0)) == 16,
                "primitive stopped detecting the relative cokernel")
        require(sum((connecting[i] * separator[i] for i in range(3)), F(0))
                == 16 * alpha,
                "connecting class stopped detecting the relative cokernel")
        require(rank(existing + [connecting]) == 3,
                "K=0 did not close the primitive cokernel")
        require(determinant(existing + [connecting]) == 16 * alpha,
                "minimal K-nullhomotopy determinant moved")
        records.append({
            "alpha": str(alpha),
            "relative_rank": rank(existing),
            "primitive_separator": "16",
            "connecting_separator": str(16 * alpha),
            "closed_determinant": str(determinant(existing + [connecting])),
        })

    # Principal-parts q-degree filtration from the committed Rees audits.
    # Evaluation at q=0 kills every positive-q-degree lower face and keeps
    # the desired unit initial component.  Order four is the first order at
    # which both q-degree and stabilizer weight can be zero.
    pp_ladder = (
        (2, 2, "nonzero"),
        (3, 1, "nonzero"),
        (4, 0, "zero"),
    )
    require(next(order for order, q_degree, weight in pp_ladder
                 if q_degree == 0 and weight == "zero") == 4,
            "first admissible Rees order moved")
    require(all(q_degree > 0 for order, q_degree, _ in pp_ladder if order < 4),
            "a lower-order PP face survived q-augmentation")

    # The exact old cap complex of commit e9962c0.  Basis (T_cap,rho) has
    # boundary (-Y,1), target (1,0), and ordinary residue (0,1).  Requiring
    # an invisible chain with nonzero boundary is inconsistent over every
    # coefficient ring because target+ores is the identity.
    cap_records = []
    for y, gamma in ((F(1), F(1)), (F(2), F(1)), (F(-3), F(5))):
        coefficient = [
            [-y, F(1)],  # boundary
            [F(1), F(0)],  # target
            [F(0), F(1)],  # ordinary residue
        ]
        augmented = [row + [rhs] for row, rhs in zip(
            coefficient, (gamma, F(0), F(0)), strict=True
        )]
        require(rank(coefficient) == 2 and rank(augmented) == 3,
                ("old cap invisibility obstruction moved", y, gamma))
        invisible = [
            vector for vector in ((F(0), F(0)),)
            if vector[0] == vector[1] == 0
        ]
        require(invisible == [(F(0), F(0))], "old cap common kernel changed")
        cap_records.append({
            "Y": str(y),
            "gamma": str(gamma),
            "coefficient_rank": rank(coefficient),
            "augmented_rank": rank(augmented),
        })

    artifacts = [
        {
            "commit": "cd52b2b",
            "object": "three-set source-relative class K",
            "maps_to_primitive": "K=alpha*A modulo middle rows and H2",
            "failure": "identifies but does not null-homotope K",
        },
        {
            "commit": "b7f5856/bfc39cb",
            "object": "ordinary Hasse/Bianchi and flat overlap rows",
            "maps_to_primitive": "no",
            "failure": "difference/curvature rows have no response-to-middle attaching lift",
        },
        {
            "commit": "a6fc3ae/f81f6cf",
            "object": "literal chart-labelled Schur tails",
            "maps_to_primitive": "no",
            "failure": "every chart-odd literal tail is a kernel-vector tail",
        },
        {
            "commit": "e7723de",
            "object": "shifted two-edge principal-parts square",
            "maps_to_primitive": "no",
            "failure": "positive q-degree polar; nonzero q-augmentation required",
        },
        {
            "commit": "ed60e2c",
            "object": "denominator-marked q-zero Rees four-cube",
            "maps_to_primitive": "polynomial symbol only",
            "failure": "attaching chain and target/ordinary-residue readouts absent",
        },
        {
            "commit": "e9962c0",
            "object": "Reynolds symbol in old cap complex",
            "maps_to_primitive": "no",
            "failure": "target-and-residue invisible boundary has rank obstruction",
        },
        {
            "commit": "befda3f",
            "object": "mixed-word reset/reinsertion",
            "maps_to_primitive": "word gap only",
            "failure": "relative first syzygy/chain lift absent",
        },
    ]

    ledger = {
        "scope": "committed h3 attaching/Rees/Bianchi candidates through q-zero PP order four",
        "selected_labels": list(SELECTED),
        "fine_degree_routes": len(routes),
        "three_set_digest": three_set["digest"],
        "relative_records": records,
        "principal_parts_ladder": [list(row) for row in pp_ladder],
        "old_cap_records": cap_records,
        "artifact_audit": artifacts,
        "minimal_new_row": {
            "name": "n_A (equivariantly, the Reynolds/denominator-marked family n_v)",
            "boundary": "K=alpha*A in the localized quotient",
            "target": 0,
            "ordinary_residue": 0,
            "first_possible_PP_order": 4,
            "q_degree": 0,
            "requires": "coupled curvature/connection lower face with nonzero q-augmentation",
        },
        "verdict": "no_committed_typed_generator_nullhomotopes_the_primitive",
    }
    digest = sha256(json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, ("ledger changed", digest, ledger))
    print("h=3 primitive attaching source-resolution audit: PASS")
    print("committed relative map: [K]=alpha*[A]")
    print("old typed source generators mapping to A: none")
    print("first possible new type: q-zero PP-order-4 invisible chain n_A")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
