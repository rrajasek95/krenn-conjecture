#!/usr/bin/env python3
"""Separate exact support deletion from the first Hasse obstruction.

The selected three-spoke theorem is affine because no matching contains two
spokes incident with the same site.  This does not extend to arbitrary
occupied coordinates merely from multiaffinity.  The minimal algebraic
counterguard is

    ab = 1,       a+b = 2

at (a,b)=(1,1): (1,-1) is a Jacobian kernel direction, but its line has
quadratic defect -t^2 and the fibre is the nonreduced double point
Q[epsilon]/(epsilon^2).

The first literal diagonal matching realization is a three-occurrence C4
packet in word 001111.  This checker completes every minimal pure-one and
pure-two target row compatible with its pure-zero coloop.  Every one of the
12*15 completions exposes an exit-only private mixed target row.  This
closes the first recurrence seed, not arbitrary larger packets in which
additional same-grade occurrences can supply its mates.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_spoke_affine_rank_or_deletion_gate.py":
        "cca8b51508756c13f169c6fe079ef9681b645098463d1f64342b0364d0cd4c9c",
    "notes/h3-active-coloop-spoke-affine-rank-or-deletion-gate.md":
        "26a01b0823de811092bb502234eff06d95a13d5545514d4191c552a6dd2143cb",
    "computations/verify_h3_active_coloop_spoke_inequivalent_constant_block_guard_exit.py":
        "80e3f4fc0525c64ce1f022c1bd2d383ab271e92e1354b5e8f644a5c934253951",
    "notes/h3-active-coloop-spoke-inequivalent-constant-block-guard-exit.md":
        "882626e24eb4216e627673327b937e60c9d8c306d3df32ee308a16bbfcb1fbf0",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
}
EXPECTED_LEDGER_SHA256 = (
    "b71687870f21de466d954f0b3cf048db9aad18666a3ed1c3de65a75b1fd1866e"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load_matching_model():
    relative = (
        "computations/"
        "verify_h3_active_coloop_spoke_inequivalent_constant_block_guard_exit.py"
    )
    specification = importlib.util.spec_from_file_location(
        "projective_block_c4_matching_model", ROOT / relative
    )
    require(specification is not None and specification.loader is not None,
            "cannot import matching model")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module.load_split()


def row_value(terms) -> Q:
    return sum((term[-1] for term in terms), Q(0))


def multiaffine_hasse_or_delete() -> dict[str, object]:
    # G=ab-1 and F=a+b-2 at x=(1,1).  Both Jacobian rows are (1,1).
    point = (Q(1), Q(1))
    direction = (Q(1), Q(-1))
    jacobian = ((point[1], point[0]), (Q(1), Q(1)))
    first = tuple(sum(row[index] * direction[index]
                      for index in range(2)) for row in jacobian)
    require(first == (Q(0), Q(0)), first)

    # Along the literal affine line, F stays zero but G-1=-t^2.
    samples = {}
    for t in (Q(-2), Q(-1), Q(0), Q(1), Q(2)):
        a = point[0] + t * direction[0]
        b = point[1] + t * direction[1]
        samples[str(t)] = {
            "a": str(a), "b": str(b),
            "ab_minus_1": str(a * b - 1),
            "a_plus_b_minus_2": str(a + b - 2),
        }
        require(a * b - 1 == -t * t and a + b - 2 == 0,
                (t, a, b))

    # Eliminate b=2-a: ab-1=-(a-1)^2.  Hence the fibre has one reduced
    # point and a nonzero tangent nilpotent; neither coordinate can vanish.
    for a in (Q(0), Q(1), Q(2)):
        b = 2 - a
        require(a * b - 1 == -(a - 1) ** 2, (a, b))
    require(not (Q(0) * Q(2) == 1) and not (Q(2) * Q(0) == 1),
            "a coordinate-zero point entered the normalized fibre")

    # General exact replacement for the false implication.  For a
    # multiaffine row of degree d, the line expansion stops at d.  A kernel
    # direction integrates iff every higher divided-Hasse coefficient is
    # zero.  At minimum occupied support, such an anchor-safe direction is
    # therefore forbidden; a surviving direction has a first nonzero H_r.
    return {
        "minimal_multiaffine_system": ["ab=1", "a+b=2"],
        "occupied_point": ["1", "1"],
        "jacobian_rows": [[str(value) for value in row]
                            for row in jacobian],
        "kernel_direction": ["1", "-1"],
        "first_order_values": [str(value) for value in first],
        "line_defect": {"target": "-t^2", "block": "0"},
        "sample_check": samples,
        "fibre_elimination": "b=2-a, ab-1=-(a-1)^2",
        "fibre_ring": "Q[epsilon]/(epsilon^2)",
        "reduced_fibre_points": [["1", "1"]],
        "coordinate_zero_fibre_points": 0,
        "sharp_exact_replacement": (
            "J_x F(xi)=0 gives an exact support-deleting line precisely "
            "when every higher divided-Hasse coefficient "
            "F_[r](x;xi), r>=2, also vanishes"
        ),
        "minimum_support_consequence": (
            "an anchor-safe occupied-coordinate kernel direction either "
            "deletes support exactly or has a first nonzero Hasse face"
        ),
        "why_the_spoke_theorem_survives": (
            "the three selected spokes share site 2, so no matching "
            "contains two of them and every higher face is identically zero"
        ),
    }


def base_c4_packet(model):
    q_values = {
        # The normalized pure-zero target has one matching and coloop 01.
        model.q_label(0, 1, 0, 0): Q(1),
        model.q_label(2, 3, 0, 0): Q(1),
        model.q_label(4, 5, 0, 0): Q(1),
        # Three-occurrence residual C4 in the literal word 001111.
        model.q_label(2, 3, 1, 1): Q(1),
        model.q_label(4, 5, 1, 1): Q(1),
        model.q_label(2, 4, 1, 1): Q(1),
        model.q_label(3, 5, 1, 1): Q(1),
        model.q_label(2, 5, 1, 1): Q(1),
        model.q_label(3, 4, 1, 1): Q(-2),
    }
    supported = []
    for word in itertools.product(model.COLOURS, repeat=6):
        terms = model.target_terms(word, q_values)
        if terms:
            supported.append((model.word_label(word), terms, row_value(terms)))
    require([(word, len(terms), value) for word, terms, value in supported] == [
        ("000000", 1, Q(1)),
        ("000011", 1, Q(1)),
        ("001100", 1, Q(1)),
        ("001111", 3, Q(0)),
    ], supported)
    pure_zero = model.target_terms((0,) * 6, q_values)
    require(len(pure_zero) == 1 and pure_zero[0][0] ==
            ((0, 1), (2, 3), (4, 5)), pure_zero)

    # Vary the two factors of the first C4 occurrence oppositely.  Its
    # linear face cancels, but the complete C4 acquires -t^2.
    for t in (Q(-2), Q(-1), Q(0), Q(1), Q(2)):
        value = (1 + t) * (1 - t) + 1 - 2
        require(value == -t * t, (t, value))

    return q_values, {
        "pure_zero_target": "q01[00] q23[00] q45[00]=1",
        "pure_zero_matching_count": 1,
        "every_pure_zero_matching_contains_01": True,
        "c4_word": "001111",
        "c4_occurrence_values": ["1", "1", "-2"],
        "c4_value": "0",
        "c4_tangent": (
            "q23[11]=1+t, q45[11]=1-t; first face zero, "
            "second face -1 and line defect -t^2"
        ),
        "supported_base_target_rows": [
            {"word": word, "occurrences": len(terms), "value": str(value)}
            for word, terms, value in supported
        ],
        "nonzero_offdiagonal_q_cells": 0,
        "minimal_larger_block_reason": (
            "a nonzero target-zero block needs at least two occurrences; "
            "three is the first size beyond the two-occurrence guards"
        ),
    }


def complete_one_matching(model, q_values, matching, colour):
    """Add one minimal pure-colour occurrence without changing old cells."""
    answer = dict(q_values)
    product = Q(1)
    missing = []
    for left, right in matching:
        label = model.q_label(left, right, colour, colour)
        if label in answer:
            product *= answer[label]
        else:
            missing.append(label)
    if not missing:
        return None
    for label in missing[:-1]:
        answer[label] = Q(1)
    answer[missing[-1]] = Q(1) / product
    if row_value(model.target_terms((colour,) * 6, answer)) != 1:
        return None
    return answer


def c4_three_colour_recurrence(model, base_q) -> dict[str, object]:
    pure_one = []
    impossible_one = []
    for matching in model.MATCHINGS6:
        completion = complete_one_matching(model, base_q, matching, 1)
        if completion is None:
            impossible_one.append(matching)
        else:
            pure_one.append((matching, completion))
    require(len(pure_one) == 12 and len(impossible_one) == 3,
            (pure_one, impossible_one))
    require(all((0, 1) in matching for matching in impossible_one),
            impossible_one)

    mixed_words = tuple(
        word for word in itertools.product(model.COLOURS, repeat=6)
        if len(set(word)) != 1
    )
    private_histogram = Counter()
    witness_histogram = Counter()
    witness_profiles = Counter()
    all_mate_classes = Counter()
    example = None

    for pure_one_matching, one_q in pure_one:
        for pure_two_matching in model.MATCHINGS6:
            q_values = complete_one_matching(
                model, one_q, pure_two_matching, 2
            )
            require(q_values is not None,
                    (pure_one_matching, pure_two_matching))
            require([row_value(model.target_terms((colour,) * 6, q_values))
                     for colour in model.COLOURS] == [Q(1), Q(1), Q(1)],
                    (pure_one_matching, pure_two_matching))

            private = []
            witnesses = []
            for word in mixed_words:
                terms = model.target_terms(word, q_values)
                if len(terms) != 1 or not row_value(terms):
                    continue
                selected = terms[0]
                private.append((word, selected))
                classes = Counter()
                for alternate in model.MATCHINGS6:
                    if alternate == selected[0]:
                        continue
                    if any(word[left] != word[right]
                           for left, right in alternate):
                        classes["offdiagonal"] += 1
                        continue

                    extended = dict(q_values)
                    product = Q(1)
                    missing = []
                    for left, right in alternate:
                        label = model.q_label(
                            left, right, word[left], word[right]
                        )
                        if label in extended:
                            product *= extended[label]
                        else:
                            missing.append(label)
                    for label in missing[:-1]:
                        extended[label] = Q(1)
                    if missing:
                        extended[missing[-1]] = Q(1) / product
                    destroys_coloop = any(
                        (0, 1) not in matching
                        for matching, _cells, _value
                        in model.target_terms((0,) * 6, extended)
                    )
                    classes[
                        "coloop_destroying_diagonal"
                        if destroys_coloop else "trapped_diagonal"
                    ] += 1
                all_mate_classes.update(classes)
                if not classes["trapped_diagonal"]:
                    witnesses.append((word, selected, classes))
                    witness_profiles[tuple(sorted(classes.items()))] += 1

            require(witnesses,
                    (pure_one_matching, pure_two_matching, private))
            private_histogram[len(private)] += 1
            witness_histogram[len(witnesses)] += 1
            if example is None:
                word, selected, classes = witnesses[0]
                example = {
                    "pure_one_matching": repr(pure_one_matching),
                    "pure_two_matching": repr(pure_two_matching),
                    "private_word": model.word_label(word),
                    "selected_matching": repr(selected[0]),
                    "selected_value": str(selected[-1]),
                    "mate_profile": dict(sorted(classes.items())),
                }

    require(private_histogram == Counter({
        6: 40, 9: 32, 7: 32, 10: 24, 11: 16, 14: 12,
        8: 12, 5: 8, 16: 4,
    }), private_histogram)
    require(witness_histogram == Counter({
        4: 60, 3: 56, 6: 28, 5: 24, 8: 12,
    }), witness_histogram)
    require(witness_profiles == Counter({
        (("coloop_destroying_diagonal", 2), ("offdiagonal", 12)): 432,
        (("offdiagonal", 14),): 360,
    }), witness_profiles)
    require(all_mate_classes == Counter({
        "offdiagonal": 19152,
        "trapped_diagonal": 1488,
        "coloop_destroying_diagonal": 864,
    }), all_mate_classes)

    return {
        "minimal_pure_one_completions": len(pure_one),
        "pure_one_same_tail_completions_impossible": len(impossible_one),
        "impossible_reason": (
            "adjoining q01[11] multiplies the zero residual C4 sum; a "
            "normalized minimal pure-one target must use one of the twelve "
            "cross matchings"
        ),
        "minimal_pure_two_completions": len(model.MATCHINGS6),
        "completed_three_colour_packets": len(pure_one) * len(model.MATCHINGS6),
        "private_mixed_target_rows": sum(
            number * count for number, count in private_histogram.items()
        ),
        "private_count_histogram": dict(sorted(private_histogram.items())),
        "exit_only_witnesses": sum(
            number * count for number, count in witness_histogram.items()
        ),
        "exit_only_witness_histogram": dict(sorted(witness_histogram.items())),
        "exit_only_mate_profiles": {
            repr(profile): count for profile, count
            in sorted(witness_profiles.items(), key=lambda item: repr(item[0]))
        },
        "all_private_mate_classes": dict(sorted(all_mate_classes.items())),
        "every_minimal_completion_has_exit_only_private_row": True,
        "exit_meaning": (
            "every alternate either contains an offdiagonal decorated edge "
            "or creates a nonzero pure-zero matching omitting coloop 01"
        ),
        "representative": example,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    model = load_matching_model()
    base_q, c4 = base_c4_packet(model)
    ledger = {
        "theorem": "h3 projective-block Hasse-or-delete and first C4 recurrence",
        "pins": PINS,
        "multiaffine_support_lowering_guard": multiaffine_hasse_or_delete(),
        "minimal_literal_larger_block": c4,
        "complete_minimal_three_colour_recurrence":
            c4_three_colour_recurrence(model, base_q),
        "frontier_effect": (
            "minimum support plus multiaffinity does not turn an arbitrary "
            "Jacobian kernel vector into an affine deletion.  The exact "
            "replacement is delete-or-first-Hasse.  The smallest literal "
            "three-occurrence diagonal C4 seed exits after every minimal "
            "three-colour target completion"
        ),
        "remaining_scope": (
            "additional same-word occurrences can supply mates for the "
            "private rows.  A full induction still needs either a support "
            "deletion in that enlarged packet or the chart-complete "
            "C2+/C4/P2 Spencer placement; this checker does not infer it "
            "from the minimal recurrence"
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
    print("blanket multiaffine support-lowering: FALSE")
    print("exact replacement: DELETE OR FIRST NONZERO HASSE FACE")
    print("minimal literal larger block: THREE-OCCURRENCE C4")
    print("minimal three-colour completions: 180")
    print("exit-only private row in every completion: YES")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
