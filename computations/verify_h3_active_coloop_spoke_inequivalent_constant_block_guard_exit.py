#!/usr/bin/env python3
"""Give the smallest inequivalent rank-two spoke guard and close it.

Literal word/head blocks cannot be added across grades.  After multiplying
the ith spoke derivative by the occupied x_i, a target-zero block has the
projective invariant [c:z1:z2:z3], c+z1+z2+z3=0.  Nonzero torus changes,
block rescaling, and spoke permutations preserve c=0 and spoke-support size.
Thus the two constant-free/support-two blocks of a8ef1a4 are not universal.

This checker constructs a literal four-occurrence inequivalent guard whose
two blocks each have one constant and one spoke occurrence.  It then appends
all 15*15 choices of pure-one and pure-two target matchings.  Every completed
packet has a private mixed unary row all of whose matching mates are either
offdiagonal or destroy the pure-zero coloop.  Hence the new minimal orbit
has an exact first complete-row exit, although arbitrary larger packets are
not thereby reduced to either minimal orbit.
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
    "computations/verify_h3_active_coloop_spoke_homogeneous_block_split_gate.py":
        "eedd0973a823995e9811cca114c9827e2d75df571e127d87232066e4f8333e79",
    "notes/h3-active-coloop-spoke-homogeneous-block-split-gate.md":
        "7c7255a02d27e8be88354edaabcdb7912f9d85ec49c8efbe092f2030d1b991c3",
    "computations/verify_h3_active_coloop_spoke_split_guard_three_colour_exit.py":
        "e263355cf95b5afd582a60dc476b68c65880341e98bc3d95d1b4a6c07aff2889",
    "notes/h3-active-coloop-spoke-split-guard-three-colour-exit.md":
        "8155c5f04f03d4e956cc338912b837bfa702d6e9fe43b467599f3ab589da4e4f",
}
EXPECTED_LEDGER_SHA256 = (
    "8c5bc2da19eefd0fd7956866393753b4183fcaaf1f9155afe450ba51948ff017"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load_split():
    relative = (
        "computations/"
        "verify_h3_active_coloop_spoke_homogeneous_block_split_gate.py"
    )
    specification = importlib.util.spec_from_file_location(
        "constant_block_guard_base", ROOT / relative
    )
    require(specification is not None and specification.loader is not None,
            "cannot import split checker")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def rank(rows) -> int:
    work = [list(map(Q, row)) for row in rows]
    pivot = 0
    for column in range(len(work[0])):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot], strict=True)]
        pivot += 1
    return pivot


def row_value(terms):
    return sum((term[-1] for term in terms), Q(0))


def guard_values(split):
    q_values = {
        split.q_label(0, 1, 0, 0): Q(1),
        # Occupied spokes x=(1,1,-1).
        split.q_label(2, 3, 0, 0): Q(1),
        split.q_label(2, 4, 0, 0): Q(1),
        split.q_label(2, 5, 0, 0): Q(-1),
        # Target mate row y=(-1,1,-1), so x dot y=1.
        split.q_label(4, 5, 0, 0): Q(-1),
        split.q_label(3, 5, 0, 0): Q(1),
        split.q_label(3, 4, 0, 0): Q(-1),
        # Common constant/spoke tails of the two response blocks.
        split.q_label(1, 2, 0, 0): Q(1),
        split.q_label(1, 3, 0, 0): Q(1),
    }
    p_values = {(0, 0, 0): Q(1)}
    s_values = {
        (1, 5, 1): Q(1),
        (1, 4, 1): Q(1),
    }
    d_values = {}
    return p_values, s_values, q_values, d_values


def invariant_classification() -> dict[str, object]:
    # At a target-zero block F_B=b_B+r_B*x=0, define c=b_B and
    # z_i=r_i*x_i.  Literal block scaling projectivizes (c,z); source torus
    # changes cancel in z_i, and residual-site symmetry only permutes z_i.
    a8 = (
        (Q(0), Q(1), Q(-1), Q(0)),
        (Q(0), Q(0), Q(1), Q(-1)),
    )
    constant_guard = (
        (Q(-1), Q(0), Q(1), Q(0)),
        (Q(1), Q(0), Q(0), Q(-1)),
    )
    require(all(sum(block) == 0 for block in a8 + constant_guard),
            (a8, constant_guard))
    a8_profiles = tuple((block[0] != 0,
                         sum(value != 0 for value in block[1:]))
                        for block in a8)
    constant_profiles = tuple((block[0] != 0,
                               sum(value != 0 for value in block[1:]))
                              for block in constant_guard)
    require(a8_profiles == ((False, 2), (False, 2))
            and constant_profiles == ((True, 1), (True, 1)),
            (a8_profiles, constant_profiles))
    return {
        "block_invariant": "[c_B:z_B1:z_B2:z_B3] in P(c+sum z=0)",
        "z_definition": "z_Bi=x_i*(partial F_B/partial x_i)",
        "allowed_literal_operations": (
            "nonzero scalar rescaling within one word/head block, nonzero "
            "source torus changes, and residual spoke permutations"
        ),
        "forbidden_operation": (
            "adding different word/head rows; it destroys literal word/fine "
            "typing and is not a physical source/chart operation"
        ),
        "orbit_space": (
            "finite configurations of projective points in P^2 modulo S3; "
            "already two full-support blocks have continuous moduli"
        ),
        "a8ef_profiles": [list(value) for value in a8_profiles],
        "new_profiles": [list(value) for value in constant_profiles],
        "inequivalent": True,
        "minimum_occurrence_argument": (
            "rank two across scalar blocks needs at least two blocks; if a "
            "block has only one source occurrence it is private, so a "
            "nonprivate guard needs at least two occurrences per block and "
            "at least four total.  Both a8ef and the new guard attain four"
        ),
    }


def literal_guard_audit(split):
    p_values, s_values, q_values, d_values = guard_values(split)
    mixed_words = tuple(
        word for word in itertools.product(split.COLOURS, repeat=6)
        if len(set(word)) != 1
    )
    target = split.target_terms((0,) * 6, q_values)
    require(len(target) == 3 and row_value(target) == 1
            and all((0, 1) in term[0] for term in target), target)

    supported_unary = []
    supported_response = []
    nonzero_response = []
    private_response = []
    for word in mixed_words:
        unary = split.target_terms(word, q_values)
        if unary:
            supported_unary.append((word, unary))
        for head_p in split.HEADS:
            for head_s in split.HEADS:
                terms = split.response_terms(
                    head_p, head_s, word,
                    p_values, s_values, q_values, d_values,
                )
                if terms:
                    supported_response.append((head_p, head_s, word, terms))
                if row_value(terms):
                    nonzero_response.append((head_p, head_s, word, terms))
                if len(terms) == 1:
                    private_response.append((head_p, head_s, word, terms))
    require(not supported_unary, supported_unary)
    require(not nonzero_response and not private_response,
            (nonzero_response, private_response))
    require(len(supported_response) == 2
            and all(len(record[-1]) == 2 for record in supported_response),
            supported_response)

    labels = tuple(
        f"R{head_p + 1}{head_s + 1}[{split.word_label(word)}]"
        for head_p, head_s, word, _terms in supported_response
    )
    require(labels == ("R12[000001]", "R12[000010]"), labels)
    occurrence_values = {
        label: [str(term[-1]) for term in record[-1]]
        for label, record in zip(labels, supported_response, strict=True)
    }
    require(occurrence_values == {
        "R12[000001]": ["-1", "1"],
        "R12[000010]": ["1", "-1"],
    }, occurrence_values)

    x = (Q(1), Q(1), Q(-1))
    y = (Q(-1), Q(1), Q(-1))
    rows = ((Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1)))
    require(sum(left * right for left, right
                in zip(x, y, strict=True)) == 1,
            (x, y))
    require(rank((y,) + rows) == 3, (y, rows))
    constants = (Q(-1), Q(1))
    require(all(constant + sum(left * right for left, right
                               in zip(row, x, strict=True)) == 0
                for constant, row in zip(constants, rows, strict=True)),
            (constants, rows, x))
    return {
        "pure_zero_target_occurrences": len(target),
        "pure_zero_target_values": [str(term[-1]) for term in target],
        "pure_zero_target_sum": str(row_value(target)),
        "every_pure_zero_matching_retains_01": True,
        "spokes_x": [str(value) for value in x],
        "target_row_y": [str(value) for value in y],
        "target_normalization": "x dot y=1",
        "supported_target_zero_unary_rows": 0,
        "supported_response_blocks": labels,
        "fine_occurrence_values": occurrence_values,
        "response_block_values": ["0", "0"],
        "response_restrictions": [
            [str(value) for value in row] for row in rows
        ],
        "rank_with_target": rank((y,) + rows),
        "rank_mod_target": rank((y,) + rows) - 1,
        "literal_private_rows": 0,
        "endpoint_holes": ["05", "04"],
        "all_endpoint_and_q_cells_diagonal": True,
        "all_holes_in_closed_star_at_0": True,
        "projective_blocks": [
            [str(value) for value in block]
            for block in (
                (Q(-1), Q(0), Q(1), Q(0)),
                (Q(1), Q(0), Q(0), Q(-1)),
            )
        ],
        "scope": (
            "literal full 729-word/four-response-head scan of the displayed "
            "support, with its pure-zero target normalization.  The pure-one "
            "and pure-two target rows are supplied in the exit audit below"
        ),
    }, (p_values, s_values, q_values, d_values)


def complete_three_colour_exit(split, values):
    _p_values, _s_values, base_q, _d_values = values
    mixed_words = tuple(
        word for word in itertools.product(split.COLOURS, repeat=6)
        if len(set(word)) != 1
    )
    witness_histogram = Counter()
    private_histogram = Counter()
    witness_profiles = Counter()
    all_private_mate_classes = Counter()
    example = None

    for pure_one_matching in split.MATCHINGS6:
        for pure_two_matching in split.MATCHINGS6:
            q_values = dict(base_q)
            for left, right in pure_one_matching:
                q_values[split.q_label(left, right, 1, 1)] = Q(1)
            for left, right in pure_two_matching:
                q_values[split.q_label(left, right, 2, 2)] = Q(1)
            require(row_value(split.target_terms((0,) * 6, q_values)) == 1
                    and row_value(split.target_terms((1,) * 6, q_values)) == 1
                    and row_value(split.target_terms((2,) * 6, q_values)) == 1,
                    (pure_one_matching, pure_two_matching))

            private = []
            witnesses = []
            for word in mixed_words:
                terms = split.target_terms(word, q_values)
                if len(terms) != 1 or not row_value(terms):
                    continue
                selected = terms[0]
                private.append((word, selected))
                classes = Counter()
                for alternate in split.MATCHINGS6:
                    if alternate == selected[0]:
                        continue
                    cross = tuple(
                        physical for physical in alternate
                        if word[physical[0]] != word[physical[1]]
                    )
                    if cross:
                        classes["offdiagonal"] += 1
                        continue
                    extended = dict(q_values)
                    for left, right in alternate:
                        extended[split.q_label(
                            left, right, word[left], word[right]
                        )] = Q(1)
                    destroys = any(
                        (0, 1) not in matching
                        for matching, _cells, _value
                        in split.target_terms((0,) * 6, extended)
                    )
                    if destroys:
                        classes["coloop_destroying_diagonal"] += 1
                    else:
                        classes["trapped_diagonal"] += 1
                all_private_mate_classes.update(classes)
                if not classes["trapped_diagonal"]:
                    witnesses.append((word, selected, classes))

            require(witnesses,
                    (pure_one_matching, pure_two_matching, private))
            private_histogram[len(private)] += 1
            witness_histogram[len(witnesses)] += 1
            for _word, _selected, classes in witnesses:
                witness_profiles[tuple(sorted(classes.items()))] += 1
            if example is None:
                word, selected, classes = witnesses[0]
                example = {
                    "pure_one_matching": repr(pure_one_matching),
                    "pure_two_matching": repr(pure_two_matching),
                    "private_word": split.word_label(word),
                    "selected_matching": repr(selected[0]),
                    "selected_value": str(selected[-1]),
                    "mate_profile": dict(sorted(classes.items())),
                }

    require(private_histogram == Counter({
        9: 72, 10: 44, 12: 24, 8: 16, 7: 16, 11: 12,
        16: 10, 6: 10, 14: 8, 13: 8, 22: 3, 18: 2,
    }), private_histogram)
    require(witness_histogram == Counter({
        4: 84, 5: 76, 3: 32, 6: 22, 8: 6, 10: 3, 2: 2,
    }), witness_histogram)
    require(witness_profiles == Counter({
        (("coloop_destroying_diagonal", 2), ("offdiagonal", 12)): 540,
        (("offdiagonal", 14),): 486,
    }), witness_profiles)
    require(all_private_mate_classes == Counter({
        "offdiagonal": 28404,
        "trapped_diagonal": 2520,
        "coloop_destroying_diagonal": 1080,
    }), all_private_mate_classes)

    return {
        "pure_one_matching_choices": len(split.MATCHINGS6),
        "pure_two_matching_choices": len(split.MATCHINGS6),
        "completed_packets": len(split.MATCHINGS6) ** 2,
        "private_mixed_unary_rows": sum(
            number * count for number, count in private_histogram.items()
        ),
        "private_row_count_histogram": dict(sorted(private_histogram.items())),
        "exit_only_witnesses": sum(
            number * count for number, count in witness_histogram.items()
        ),
        "exit_only_witness_count_histogram":
            dict(sorted(witness_histogram.items())),
        "exit_only_mate_profiles": {
            repr(profile): count for profile, count
            in sorted(witness_profiles.items(), key=lambda item: repr(item[0]))
        },
        "all_private_mate_classes":
            dict(sorted(all_private_mate_classes.items())),
        "every_completed_packet_has_exit_only_private_row": True,
        "exit_meaning": (
            "an offdiagonal decorated q edge enters the physical active-fan "
            "alternative; an all-diagonal mate in the second profile creates "
            "a nonzero pure-zero matching omitting 01 and destroys the named "
            "coloop"
        ),
        "representative": example,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    split = load_split()
    literal, values = literal_guard_audit(split)
    ledger = {
        "theorem": "h3 smallest inequivalent constant-block spoke guard exit",
        "pins": PINS,
        "literal_block_orbit_classification": invariant_classification(),
        "smallest_inequivalent_guard": literal,
        "first_complete_three_colour_exit":
            complete_three_colour_exit(split, values),
        "frontier_effect": (
            "arbitrary cross-block rank two does not reduce formally to the "
            "a8ef constant-free root-line pair.  The smallest other literal "
            "orbit has the same four-occurrence size and is closed by its "
            "first full three-colour target completion.  General entry still "
            "needs a reduction of larger projective block configurations to "
            "a private row, one of these minimal guards, or a typed exit"
        ),
        "scope": (
            "exact literal h=3 polynomial guard and 15*15 target-matching "
            "completion census.  Additional same-word occurrences in an "
            "arbitrary source can remove the displayed privacy; they are not "
            "silently eliminated by the projective classification"
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
    print("literal rank-two block orbit: NOT UNIQUE")
    print("smallest inequivalent guard: FOUR OCCURRENCES")
    print("completed pure1/pure2 packets: 225")
    print("exit-only private unary row in every packet: YES")
    print("remaining: REDUCE LARGER PROJECTIVE BLOCK CONFIGURATIONS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
