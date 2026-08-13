#!/usr/bin/env python3
"""Extend the Gate-II delta dual through the named same-grade families.

At degree zero, grant the complete 105-term response R, the selected
three-term A*H coefficient shadow, and the endpoint-odd B-C occurrence
shadow.  (Granting A*H is stronger than the current physical inventory.)
The root-even candidate is L=(2A-B-C)H.  A primitive sparse dual, supported
on matching-paired B and C occurrences plus one outside occurrence, kills
all three granted columns and detects L.  The first column which kills this
nonfill class is exactly the nine-term local block projector R01, because
L=3*A*H-R01.

A covariant three-cap realization of R01 has first PP boundary dR01.  The
same corrected dual extends to the complete first-PP response, d(AH), and
d(B-C), and its only nonzero pairing with dL is on the 18 endpoint/direction
terms.  Thus the obstruction moves to, rather than disappears at, the
endpoint-even first-PP Spencer face.

The labelled two-root descent of that face reaches the known word-0102
private vector.  Its primitive endpoint-even detector kills the complete
response and the target/Eq cone but has value -13/6.  Unlabelled recursive
B-4 repair is not nilpotent; the finite object is the labelled Hasse square
with one missing occurrence-local section and its dq23 reinsertion face.
The labelled residue then adds no further direction under the pinned
pointed/cap/d_even hypotheses.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py":
        "a80e5ec2a1aaa90814b412d13b1c7981f345bb41ca5a5450d5361ae2bc9f5773",
    "notes/h3-gate-ii-chiw-chart-complete-h2-face.md":
        "95fcde72841aa4b859ffa0711fb30149cd9d3406ad44dcba228445f0023c5505",
    "computations/verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py":
        "18cb73805ffca0a080bc061c88cb42f6c0c83d57efd60c574455b757009785b4",
    "notes/h3-h2-chart-scalar-capped-c4-augmented-gate.md":
        "baee4965bcb9315fc7e9f51693aebcf3cfb6c8a147c76144eb287f7c9c74c998",
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "notes/h3-h2-l01-three-cap-first-pp-curvature-gate.md":
        "d43b196a448045b9cf40a9537e5a30d9aad658a9c8636047052a023b45c4db7f",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "notes/h2-p2-0112-one-endpoint-hasse-placement-gate.md":
        "5b17afb39c796d79021e0c16fb9e9d0e65c33acc9c7d1b8b6185747bd1450ab5",
    "computations/verify_h2_p2_recursive_bminus4_nonnilpotence_value_gate.py":
        "7eac171559ca35c1808ea54471cf4bd7f570a9b8cc4738f01e29bbb6f736deb3",
    "notes/h2-p2-recursive-bminus4-nonnilpotence-value-gate.md":
        "bd8998c1a7c684cf045da2d36fd7b5f1acb5c662a66cf78e97462df2589f6b3d",
    "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py":
        "0a4215db2b91843753cc636b489a81f8e30a8c3de234979c74c9f852d74e3d8a",
    "notes/h3-p2-labelled-ores-cut-even-deven-gauge-gate.md":
        "0477f14ab8725708711ff098c68ae29f10625516024cc2a93413c780ea466054",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "notes/h3-gate-ii-chiw-nonfill-full-augmented-dual.md":
        "f7fd790075f7cf3d31b9d4a6035fa6bc476a3bdc16ce4bda97b777b153664568",
}
EXPECTED_LEDGER_SHA256 = (
    "9f31bb2def3b2c83fca9b78cb1c68f10efdb98a2c6bdbd4031603ed4149341c7"
)


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


def add(*vectors):
    require(vectors and len({len(value) for value in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns):
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


def vector(order, values):
    return tuple(Q(values.get(label, 0)) for label in order)


def degree_zero_response_extension(curvature) -> dict[str, object]:
    matchings, directions, tails, l01, r01, ah = curvature.polynomial_data()
    response = {matching: Q(1) for matching in matchings}
    odd = {}
    for direction_index, direction in enumerate(directions):
        coefficient = (Q(0), Q(1), Q(-1))[direction_index]
        for tail in tails:
            odd[tuple(sorted(direction + tail))] = coefficient
    order = tuple(matchings)
    old = tuple(vector(order, values) for values in (response, ah, odd))
    candidate = vector(order, l01)
    block = vector(order, r01)
    require(rank(old) == 3 and rank(old + (candidate,)) == 4
            and rank(old + (block,)) == 4
            and rank(old + (block, candidate)) == 4,
            "the degree-zero response/block-projector ranks changed")
    require(candidate == add(scale(3, old[1]), scale(-1, block)),
            "L01=3AH-R01 stopped holding in the full response module")

    # Sparse primitive corrected dual: take one B and one C occurrence with
    # the same tail, and -2 on one occurrence outside the nine-term block.
    selected_tail = tails[0]
    b_occurrence = tuple(sorted(directions[1] + selected_tail))
    c_occurrence = tuple(sorted(directions[2] + selected_tail))
    outside = next(matching for matching in matchings if matching not in r01)
    dual_values = {b_occurrence: Q(1), c_occurrence: Q(1), outside: Q(-2)}
    dual = vector(order, dual_values)
    require(gcd(*(abs(int(value)) for value in dual if value)) == 1
            and all(dot(dual, column) == 0 for column in old)
            and dot(dual, candidate) == Q(-2)
            and dot(dual, block) == Q(2),
            "the degree-zero corrected primitive dual changed")
    return {
        "granted_occurrence_columns": [
            "complete R", "A*H coefficient shadow (strong grant)",
            "endpoint-odd (B-C)H occurrence shadow",
        ],
        "old_rank": rank(old),
        "rank_with_chi_w_L01": rank(old + (candidate,)),
        "first_rank_raising_column": "R01=(A+B+C)H, nine terms",
        "rank_with_R01": rank(old + (block,)),
        "identity_after_R01": "L01=3*A*H-R01",
        "corrected_primitive_dual": {
            "support": [
                "+1 on one B occurrence", "+1 on its C mate",
                "-2 on one occurrence outside R01",
            ],
            "old_column_values": [str(dot(dual, column)) for column in old],
            "value_on_L01": str(dot(dual, candidate)),
            "value_on_R01": str(dot(dual, block)),
        },
        "consequence": (
            "the occurrence correction kills the actual complete response "
            "and endpoint-odd shadow even after the nonphysical A*H shadow "
            "is granted.  A physical R01 projector would fill L01 and "
            "terminate the nonfill branch"
        ),
    }


def first_pp_extension(curvature) -> dict[str, object]:
    matchings, directions, tails, l01, r01, ah = curvature.polynomial_data()
    response = {matching: Q(1) for matching in matchings}
    odd = {}
    for direction_index, direction in enumerate(directions):
        coefficient = (Q(0), Q(1), Q(-1))[direction_index]
        for tail in tails:
            odd[tuple(sorted(direction + tail))] = coefficient
    d_response = curvature.differential(response)
    d_ah = curvature.differential(ah)
    d_odd = curvature.differential(odd)
    d_l01 = curvature.differential(l01)
    d_r01 = curvature.differential(r01)
    order = tuple(d_response)
    old = tuple(vector(order, values)
                for values in (d_response, d_ah, d_odd))
    candidate = vector(order, d_l01)
    block = vector(order, d_r01)
    require(rank(old) == 3 and rank(old + (candidate,)) == 4
            and rank(old + (block,)) == 4
            and rank(old + (block, candidate)) == 4,
            "the first-PP response/block-projector ranks changed")
    require(candidate == add(scale(3, old[1]), scale(-1, block)),
            "dL01=3d(AH)-dR01 stopped holding")

    selected_tail = tails[0]
    b_occurrence = tuple(sorted(directions[1] + selected_tail))
    c_occurrence = tuple(sorted(directions[2] + selected_tail))
    b_label = (b_occurrence, directions[1][0])
    c_label = (c_occurrence, directions[2][0])
    outside_label = next(label for label in d_response
                         if label[0] not in r01)
    require(b_label in d_l01 and c_label in d_l01,
            "the chosen direction labels left dL01")
    dual = vector(order, {
        b_label: Q(1), c_label: Q(1), outside_label: Q(-2),
    })
    require(all(dot(dual, column) == 0 for column in old)
            and dot(dual, candidate) == Q(-2)
            and dot(dual, block) == Q(2),
            "the first-PP corrected dual changed")

    action_sites = {0, 1, 6, 7}
    tail_half = {label: value for label, value in d_l01.items()
                 if set(label[1]).isdisjoint(action_sites)}
    direction_half = {label: value for label, value in d_l01.items()
                      if set(label[1]).issubset(action_sites)}
    tail_vector = vector(order, tail_half)
    direction_vector = vector(order, direction_half)
    require(len(tail_half) == len(direction_half) == 18
            and add(tail_vector, direction_vector) == candidate
            and dot(dual, tail_vector) == 0
            and dot(dual, direction_vector) == Q(-2),
            "the first-PP tail/direction obstruction moved")
    return {
        "granted_occurrence_columns": [
            "dR", "d(A*H) coefficient shadow (strong grant)",
            "d((B-C)H) occurrence shadow",
        ],
        "old_rank": rank(old),
        "rank_with_dL01": rank(old + (candidate,)),
        "rank_with_dR01": rank(old + (block,)),
        "differentiated_identity": "dL01=3*d(AH)-dR01",
        "corrected_dual_values": {
            "old": [str(dot(dual, column)) for column in old],
            "dL01": str(dot(dual, candidate)),
            "dR01": str(dot(dual, block)),
            "tail_18": str(dot(dual, tail_vector)),
            "endpoint_direction_18": str(dot(dual, direction_vector)),
        },
        "exact_next_face": {
            "support": 18,
            "type": "endpoint/direction first-PP part of dL01",
            "six_labelled_marginals": [6, 6, -3, -3, -3, -3],
            "primitive_profile": [2, 2, -1, -1, -1, -1],
        },
        "consequence": (
            "the occurrence correction also kills the actual first-PP "
            "response and odd shadows, even with d(AH) granted.  A covariant "
            "three-cap R01 projector does not give a terminal for free: its "
            "first proper boundary is exactly the rank-raising endpoint/"
            "direction face"
        ),
    }


def downstream_word_0102_extension(p2, recursive, ores) -> dict[str, object]:
    p2_ledger, p2_digest = p2.audit()
    require(p2_digest == p2.EXPECTED_LEDGER_SHA256,
            "the word-0102 placement gate changed")
    word_data = p2_ledger["one_endpoint_Hasse_faces"]
    representative = tuple(map(Q, word_data["representative_occurrence_vector"]))
    size = len(representative)
    one = (Q(1),) * size
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(size))
    require(sum(detector, Q(0)) == 0
            and dot(detector, representative) == Q(-13, 6)
            and rank((one,)) == 1
            and rank((one, representative)) == 2,
            "the word-0102 corrected detector changed")

    recursive_ledger, recursive_digest = recursive.audit()
    require(recursive_digest == recursive.EXPECTED_LEDGER_SHA256
            and recursive_ledger["raw_recursive_operator"]["trace_R_squared"]
                == "109/3"
            and recursive_ledger["finite_labelled_replacement"]
                ["second_cobar_boundary"] == 0,
            "the finite-labelled/nonrecursive P2 conclusion changed")

    ores_ledger, ores_digest = ores.audit()
    require(ores_digest == ores.EXPECTED_LEDGER_SHA256
            and not ores_ledger["response_gauge_identity"]
                ["requires_new_labelled_direction"]
            and ores_ledger["conditional_closure"]
                ["does_not_construct_hypotheses"],
            "the labelled-residue closure scope changed")
    return {
        "word": "0102",
        "old_occurrence_columns": ["complete response line"],
        "target_Eq_cone_projection": 0,
        "rank_before_private_face": 1,
        "rank_after_private_face": 2,
        "representative_private_vector": [str(value) for value in representative],
        "primitive_detector": "+e0+e3-e1-e6",
        "detector_on_complete_response": str(dot(detector, one)),
        "detector_on_private_face": str(dot(detector, representative)),
        "all_eight_word_blocks": {
            "complete_response_rank": word_data["rank_complete_rows"],
            "rank_after_private_faces": word_data["rank_after_faces"],
        },
        "unlabelled_recursive_repair": {
            "trace_R_squared": recursive_ledger["raw_recursive_operator"]
                ["trace_R_squared"],
            "nilpotent": recursive_ledger["raw_recursive_operator"]["nilpotent"],
        },
        "finite_source_object": (
            "one labelled two-root Hasse square; second cobar boundary zero"
        ),
        "first_missing_column": p2_ledger["first_absent_column"],
        "next_product_rule_face": "dq23:21 reinsertion of the 0102 section",
        "labelled_residue_after_section": (
            "complete-response gauge plus d_even; no new labelled direction "
            "under the pointed/cap/mixed-target hypotheses"
        ),
        "accepted_terminal_status": (
            "NO: the detector is only defined on the occurrence-private "
            "word block; q, W, labelled ridge and the physical readout on "
            "the missing section/reinsertion have not been supplied"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    curvature = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "gate_ii_extension_curvature",
    )
    p2 = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "gate_ii_extension_p2",
    )
    recursive = load(
        "computations/verify_h2_p2_recursive_bminus4_nonnilpotence_value_gate.py",
        "gate_ii_extension_recursive",
    )
    ores = load(
        "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py",
        "gate_ii_extension_ores",
    )
    ledger = {
        "theorem": "h3 Gate-II psi_delta same-grade extension chain",
        "pins": PINS,
        "degree_zero_response_and_block_projector":
            degree_zero_response_extension(curvature),
        "first_PP_response_and_three_cap": first_pp_extension(curvature),
        "downstream_word_0102":
            downstream_word_0102_extension(p2, recursive, ores),
        "verdict": (
            "The occurrence projection of the delta dual can be corrected "
            "across the actual complete response and endpoint-odd shadows, "
            "even after granting A*H and d(AH), which are stronger than the "
            "current physical inventory.  The first "
            "rank-raising degree-zero column is the nine-term R01 projector; "
            "if physical it fills L01 exactly.  The smallest covariant "
            "three-cap attempt to construct R01 has one unavoidable proper "
            "face: the 18 endpoint/direction terms of dL01 with primitive "
            "profile (2,2,-1,-1,-1,-1).  Its labelled descent reaches the "
            "word-0102 private vector detected by +e0+e3-e1-e6 with value "
            "-13/6.  These are associated-graded occurrence corrections, "
            "not a single full cochain.  The last detector is not an accepted physical "
            "terminal because the occurrence-local section and dq23 "
            "reinsertion have no q/W/ridge readouts.  Thus no corrected full "
            "Psi is presently constructed; the exact next face is that one "
            "labelled endpoint-even section, not a new residue direction"
        ),
        "shortest_positive_object": (
            "one source-valid covariant three-cap/labelled-Hasse square whose "
            "degree-zero boundary supplies R01, whose endpoint-direction PP "
            "face supplies the word-0102 occurrence-local section, and whose "
            "dq23 reinsertion is typed in q/W/labelled-ridge rows"
        ),
        "scope": (
            "exact canonical h3 K8 occurrence and first-PP matrices, exact "
            "h2 word-0102 occurrence quotient, and the pinned conditional "
            "residue closure.  It does not assert that the missing physical "
            "three-cap/Hasse square exists or that an associated-graded "
            "detector is a full augmented terminal"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Gate-II extension chain ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("psi_delta through R/AH/odd and first PP: EXTENDS")
    print("first degree-zero rank raiser: R01 BLOCK PROJECTOR")
    print("covariant R01 proper face: 18 ENDPOINT/DIRECTION TERMS")
    print("downstream 0102 detector: -13/6")
    print("full accepted terminal: NO; LABELLED SECTION + dq23 FACE OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
