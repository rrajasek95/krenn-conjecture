#!/usr/bin/env python3
"""Linear-algebra guard to active-minor + third-axis-component -> curved OO.

Minimum support makes the complete response columns independent, but their
independence may live entirely in cofactor-tail directions.  All occupied
columns can retain one common local axis.  This checker gives the smallest
k=3 realization with an active determinant/cofactor product, a third
occupied response column, and deleted-star profile (2,2,3,3), while every
active rank-one arm has the same outer head.  The construction extends by
adding independent tails for arbitrary k>=3.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_axis_circuit_k2_contraction_obstruction.py":
        "131e468bce4cefbc49f6ff8b7ee0152078d96fb946bb2a01340b9399967a71b7",
    "notes/uniform-axis-circuit-k2-contraction-obstruction.md":
        "68761b970a8795ae6a8ce18c695d9a216a7463c7f3d95a551055e1f6cee6e036",
    "computations/verify_uniform_one_bad_flat_hessian_active_minor_transgression.py":
        "e6984d42afb1bc35b3948b526e13430322703f6b5a737f7c0364474eba64b412",
    "notes/uniform-one-bad-flat-hessian-active-minor-transgression.md":
        "ce8037d603971ca7cbf718d9febb8e43fadcb494fc7e027525f26c16bf7c1960",
}
EXPECTED_LEDGER_SHA256 = (
    "9e75521a53ad851d714d25b1dac54e32ba2129ec0a5288fa1a8c90922ef6a742"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def rank(columns):
    if not columns:
        return 0
    rows = len(columns[0])
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(rows)]
    output = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(output, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[output], matrix[pivot] = matrix[pivot], matrix[output]
        value = matrix[output][column]
        matrix[output] = [entry / value for entry in matrix[output]]
        for row in range(rows):
            if row == output or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right
                           in zip(matrix[row], matrix[output], strict=True)]
        output += 1
    return output


def determinant2(first, second, coordinates=(0, 1)):
    left, right = coordinates
    return first[left] * second[right] - first[right] * second[left]


def audit_order(k):
    # The complete response space is local_axis tensor tail_space.  Suppress
    # the fixed nonzero local_axis factor; the k tail basis vectors remain
    # independent even though every physical port has that same local line.
    response_columns = tuple(
        tuple(Q(int(row == column)) for row in range(k))
        for column in range(k)
    )
    target = tuple(Q(1) for _ in range(k))
    require(rank(response_columns) == k
            and tuple(sum(column[row] for column in response_columns)
                      for row in range(k)) == target,
            f"the minimum response circuit changed at k={k}")

    # Three occupied physical arms at one centre.  The active pair has
    # independent centre heads h0,h1 but all outer heads equal ell0.  The
    # third occupied component repeats the local h1/ell0 geometry while its
    # cofactor tail is the independent response column C2.
    h0 = (Q(1), Q(0), Q(0))
    h1 = (Q(0), Q(1), Q(0))
    h2 = (Q(0), Q(0), Q(1))
    outer_heads = (h0, h0, h0)
    centre_heads = (h0, h1, h1)
    cofactor_activities = (Q(1), Q(1), Q(1))
    active_minor = determinant2(centre_heads[0], centre_heads[1])
    outer_minor = determinant2(outer_heads[0], outer_heads[1])
    require(active_minor == 1 and outer_minor == 0
            and all(cofactor_activities),
            "the active same-head port guard changed")
    require(rank(outer_heads) == 1,
            "the third axis component created a distinct outer head")

    # One common full centre-star presentation realizes exactly the required
    # deletion asymmetry.  Deleting arm u leaves span(h1,h2), rank two;
    # deleting arm v leaves span(h0,h1,h2), rank three.  The third occupied
    # axis component is the repeated h1 column and does not raise the former.
    arm_u, arm_v, third_axis, background = h0, h1, h1, h2
    centre_delete_u = (arm_v, third_axis, background)
    centre_delete_v = (arm_u, third_axis, background)
    outer_u_delete_centre = (h0, h1)
    outer_v_delete_centre = (h0, h1, h2)
    profile = (
        rank(centre_delete_u),
        rank(outer_u_delete_centre),
        rank(centre_delete_v),
        rank(outer_v_delete_centre),
    )
    require(profile == (2, 2, 3, 3),
            f"the deleted-star profile changed at k={k}: {profile}")

    # Extra response columns at k>3 use new independent tails but may repeat
    # the same h1/ell0 local port.  Hence neither minimum support nor a third
    # (or later) occupied column changes the local rank/head ledger.
    return {
        "k": k,
        "response_column_rank": rank(response_columns),
        "target_coefficients": [1] * k,
        "chosen_self_square": "lambda_0*lambda_1=1",
        "active_centre_minor": str(active_minor),
        "active_cofactor_values": [str(value) for value in cofactor_activities],
        "outer_head_span_rank": rank(outer_heads),
        "outer_head_minor": str(outer_minor),
        "deleted_star_profile": list(profile),
        "third_column": (
            "independent cofactor tail C2 with repeated local h1 tensor ell0"
        ),
    }


def main():
    pin_dependencies()
    audits = tuple(audit_order(k) for k in range(3, 11))
    require(all(record["deleted_star_profile"] == [2, 2, 3, 3]
                and record["outer_head_span_rank"] == 1 for record in audits),
            "the uniform same-head guard changed")

    ledger = {
        "dependencies": PINS,
        "representative_exact_audits": audits,
        "counterguard": {
            "response_geometry": (
                "C_i=a tensor w_i with one fixed local axis a and independent "
                "cofactor tails w_i; thus the C_i are minimum-support "
                "independent although their local port span has rank one"
            ),
            "active_data": (
                "two centre heads h0,h1 have determinant one, all three "
                "cofactors are nonzero, and all outer heads equal ell0"
            ),
            "rank_data": "deleted-star profile (2,2,3,3)",
            "oo_failure": (
                "there is no distinct-head pair: every active rank-one arm "
                "has outer-head span one"
            ),
        },
        "verdict": (
            "an active determinant/cofactor product plus a third occupied "
            "minimum axis component does not force a distinct-head active "
            "rank-(3,3,3,3) pair; the port maps can remain (2,2,3,3)"
        ),
        "missing_hypothesis": (
            "a source-labelled incidence theorem coupling independence of "
            "the response tails to a transverse local outer head, together "
            "with a nonzero cofactor and the missing rank-three minors at "
            "both deficient deleted stars"
        ),
        "scope": (
            "smallest k=3 coordinate-free rank guard and its tail-space "
            "extension to all k>=3; not a physical source, support census, "
            "or counterexample to a theorem using additional full rows"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"third-axis rank guard ledger changed: {digest}")

    print("uniform axis-circuit third-component rank guard: PASS")
    print("minimum response columns: independent through k=10")
    print("active centre minor/cofactors: nonzero")
    print("outer-head span: 1; deleted-star profile: (2,2,3,3)")
    print("missing input: source incidence from tail rank to transverse port rank")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
