#!/usr/bin/env python3
"""Scan the first complete-row recurrence of the split spoke guard.

The literal counterguard of a8ef1a4 satisfies every currently supported
mixed unary and four response coefficient, but it has no pure-one target.
Adjoin each of the 15 possible all-one perfect matchings.  For every newly
private mixed unary coefficient classify all fourteen matching mates.

For unary rows, every offdiagonal mate has two cross-colour edges and at
least one outside the closed star at zero; some diagonal mates destroy the
pure-zero coloop.  The new pure-one cells also create private response rows.
Most response mates have an outside certified edge; the remaining ones are
either offdiagonal inside the star or diagonal endpoint occurrences inside
the star.  A nonempty diagonal trapped recurrence remains, so the first
complete-row scan does not yet prove homogeneous synchronization.
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
    "computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py":
        "fe60edcc44c33e660b50f7e8d627b506c5bd81c1d97f15e66b9e8a35e9f3c4ad",
    "notes/h3-active-coloop-closed-shore-complete-row-response-gate.md":
        "1470ffc55dff20f0919b4be884ca8d54efe7a15e90117d1610aef067c82b44b2",
}
EXPECTED_LEDGER_SHA256 = (
    "8cec9e6c9e6cf6da1c3ba4f89a5042d608d1781e6ac5bd2f5b675b43a0f0f3a3"
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
    relative = PINS.keys().__iter__().__next__()
    specification = importlib.util.spec_from_file_location(
        "spoke_split_guard", ROOT / relative
    )
    require(specification is not None and specification.loader is not None,
            "cannot load spoke split guard")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def extend_q(split, q_values, matching, colour):
    answer = dict(q_values)
    for left, right in matching:
        answer[split.q_label(left, right, colour, colour)] = Q(1)
    return answer


def complete_supported_row_scan(split, q_values) -> dict[str, object]:
    mixed_unary = []
    private_mixed_unary = []
    nonzero_mixed_unary = []
    response = []
    private_response = []
    nonzero_response = []
    for word in itertools.product(split.COLOURS, repeat=6):
        if len(set(word)) == 1:
            continue
        target_terms = split.target_terms(word, q_values)
        if target_terms:
            mixed_unary.append((word, target_terms))
        value = sum((term[-1] for term in target_terms), Q(0))
        if len(target_terms) == 1:
            private_mixed_unary.append((word, target_terms[0]))
        if value:
            nonzero_mixed_unary.append((word, value))
        for head_p in split.HEADS:
            for head_s in split.HEADS:
                terms = split.response_terms(
                    head_p, head_s, word,
                    split.GUARD_P, split.GUARD_S, q_values, split.GUARD_D,
                )
                if terms:
                    response.append((head_p, head_s, word, terms))
                response_value = sum((term[-1] for term in terms), Q(0))
                if len(terms) == 1:
                    private_response.append((head_p, head_s, word, terms[0]))
                if response_value:
                    nonzero_response.append(
                        (head_p, head_s, word, response_value)
                    )
    return {
        "supported_mixed_unary": mixed_unary,
        "private_mixed_unary": private_mixed_unary,
        "nonzero_mixed_unary": nonzero_mixed_unary,
        "supported_response": response,
        "private_response": private_response,
        "nonzero_response": nonzero_response,
    }


def base_complete_row_silence(split) -> dict[str, object]:
    scan = complete_supported_row_scan(split, split.GUARD_Q)
    require(not scan["supported_mixed_unary"], scan["supported_mixed_unary"])
    require(len(scan["supported_response"]) == 2,
            scan["supported_response"])
    require(not scan["private_response"], scan["private_response"])
    require(not scan["nonzero_response"], scan["nonzero_response"])
    require(not scan["nonzero_mixed_unary"], scan["nonzero_mixed_unary"])
    blocks = tuple(
        f"R{head_p + 1}{head_s + 1}[{split.word_label(word)}]"
        for head_p, head_s, word, _terms in scan["supported_response"]
    )
    require(blocks == ("R21[000001]", "R21[000100]"), blocks)
    return {
        "mixed_unary_coefficients_with_occurrences": 0,
        "response_coefficients_with_occurrences": len(blocks),
        "response_blocks": blocks,
        "response_occurrences_per_block": [
            len(terms) for _hp, _hs, _word, terms
            in scan["supported_response"]
        ],
        "nonzero_target_zero_coefficients": 0,
        "private_target_zero_coefficients": 0,
        "consequence": (
            "the complete unary plus four-response scan on the displayed "
            "support is silent; no source equation forces a mate before a "
            "missing constant-colour target packet is supplied"
        ),
    }


def structural_response_occurrences(split, word):
    """All 15 direct plus 90 ordered-endpoint terms in one response row."""
    answer = []
    for matching in split.MATCHINGS6:
        cells = tuple(split.q_label(left, right, word[left], word[right])
                      for left, right in matching)
        answer.append(("D", None, None, matching, cells, Q(1)))
    for p_site in split.SITES:
        for s_site in split.SITES:
            if p_site == s_site:
                continue
            residual = tuple(site for site in split.SITES
                             if site not in (p_site, s_site))
            for matching in split.perfect_matchings(residual):
                cells = tuple(split.q_label(
                    left, right, word[left], word[right]
                ) for left, right in matching)
                answer.append(("PS", p_site, s_site, matching, cells, Q(1)))
    require(len(answer) == 105, len(answer))
    return tuple(answer)


def response_term_key(term):
    return term[0], term[1], term[2], term[3]


def classify_first_pure_one_recurrence(split) -> dict[str, object]:
    star = frozenset(split.edge(0, site) for site in range(1, 6))
    private_count_by_matching = Counter()
    private_response_count_by_matching = Counter()
    supported_unary_count_by_matching = Counter()
    nonzero_unary_count_by_matching = Counter()
    supported_response_count_by_matching = Counter()
    unary_row_occurrence_histogram = Counter()
    response_row_occurrence_histogram = Counter()
    unary_mate_classes = Counter()
    response_mate_classes = Counter()
    trapped_records = []
    trapped_response_records = []
    private_records = []
    private_response_records = []

    for target_matching in split.MATCHINGS6:
        q_values = extend_q(split, split.GUARD_Q, target_matching, 1)
        pure_one = split.target_terms((1,) * 6, q_values)
        require(len(pure_one) == 1 and pure_one[0][0] == target_matching,
                (target_matching, pure_one))
        scan = complete_supported_row_scan(split, q_values)
        require(len(scan["nonzero_response"])
                == len(scan["private_response"]),
                (target_matching, scan["nonzero_response"],
                 scan["private_response"]))
        private = scan["private_mixed_unary"]
        private_count_by_matching[len(private)] += 1
        private_response_count_by_matching[len(scan["private_response"])] += 1
        supported_unary_count_by_matching[
            len(scan["supported_mixed_unary"])
        ] += 1
        nonzero_unary_count_by_matching[
            len(scan["nonzero_mixed_unary"])
        ] += 1
        supported_response_count_by_matching[
            len(scan["supported_response"])
        ] += 1
        unary_row_occurrence_histogram.update(
            len(terms) for _word, terms in scan["supported_mixed_unary"]
        )
        response_row_occurrence_histogram.update(
            len(terms) for _hp, _hs, _word, terms
            in scan["supported_response"]
        )
        for word, selected in private:
            selected_matching = selected[0]
            require(selected_matching in (target_matching,) + split.MATCHINGS6,
                    selected_matching)
            private_records.append((target_matching, word, selected_matching))
            for alternate in split.MATCHINGS6:
                if alternate == selected_matching:
                    continue
                cross_edges = tuple(
                    physical for physical in alternate
                    if word[physical[0]] != word[physical[1]]
                )
                if cross_edges:
                    require(len(cross_edges) == 2, (word, alternate, cross_edges))
                    outside = tuple(edge for edge in cross_edges
                                    if edge not in star)
                    require(outside, (word, alternate, cross_edges, star))
                    unary_mate_classes[
                        "offdiagonal_with_outside_star"
                    ] += 1
                    continue

                # Test whether adjoining this all-diagonal word mate also
                # creates a non-coloop all-zero matching.
                extended = dict(q_values)
                for left, right in alternate:
                    extended[split.q_label(
                        left, right, word[left], word[right]
                    )] = Q(1)
                pure_zero_terms = split.target_terms((0,) * 6, extended)
                destroys = any((0, 1) not in matching
                               for matching, _cells, _value in pure_zero_terms)
                if destroys:
                    unary_mate_classes["diagonal_destroys_coloop"] += 1
                    continue
                unary_mate_classes["diagonal_trapped_recurrence"] += 1
                trapped_records.append({
                    "target_one_matching": repr(target_matching),
                    "private_word": split.word_label(word),
                    "selected_matching": repr(selected_matching),
                    "alternate_matching": repr(alternate),
                    "retains_coloop_edge": (0, 1) in alternate,
                    "star_holes": [repr(value) for value in sorted(
                        edge for edge in alternate if 0 in edge
                    )],
                })

        for head_p, head_s, word, selected in scan["private_response"]:
            private_response_records.append(
                (target_matching, head_p, head_s, word, selected)
            )
            selected_key = response_term_key(selected)
            alternatives = tuple(
                term for term in structural_response_occurrences(split, word)
                if response_term_key(term) != selected_key
            )
            require(len(alternatives) == 104, (selected_key, alternatives))
            for alternate in alternatives:
                cross_edges = tuple(
                    (left, right) for left, right, left_colour, right_colour
                    in alternate[-2] if left_colour != right_colour
                )
                endpoint_hole = (() if alternate[0] == "D" else
                                 (split.edge(alternate[1], alternate[2]),))
                outside = tuple(physical for physical
                                in cross_edges + endpoint_hole
                                if physical not in star)
                if outside:
                    response_mate_classes[
                        "certified_edge_outside_star"
                    ] += 1
                    continue
                if cross_edges:
                    response_mate_classes[
                        "offdiagonal_inside_star"
                    ] += 1
                    continue
                require(alternate[0] == "PS" and endpoint_hole,
                        (word, alternate, endpoint_hole))
                response_mate_classes[
                    "diagonal_endpoint_inside_star"
                ] += 1
                trapped_response_records.append({
                    "target_one_matching": repr(target_matching),
                    "private_block": (
                        f"R{head_p + 1}{head_s + 1}"
                        f"[{split.word_label(word)}]"
                    ),
                    "selected_occurrence": repr(selected_key),
                    "alternate_occurrence": repr(response_term_key(alternate)),
                    "endpoint_hole": repr(endpoint_hole[0]),
                })

    require(private_count_by_matching == Counter({3: 9, 5: 3, 2: 3}),
            private_count_by_matching)
    require(private_response_count_by_matching
            == Counter({2: 5, 1: 4, 4: 4, 3: 2}),
            private_response_count_by_matching)
    require(supported_unary_count_by_matching
            == Counter({4: 9, 6: 3, 3: 3}),
            supported_unary_count_by_matching)
    require(nonzero_unary_count_by_matching
            == Counter({4: 5, 3: 5, 6: 3, 2: 2}),
            nonzero_unary_count_by_matching)
    require(supported_response_count_by_matching
            == Counter({4: 5, 3: 4, 6: 4, 5: 2}),
            supported_response_count_by_matching)
    require(len(private_records) == 48, len(private_records))
    require(len(private_response_records) == 36,
            len(private_response_records))
    require(unary_mate_classes == Counter({
        "offdiagonal_with_outside_star": 576,
        "diagonal_destroys_coloop": 36,
        "diagonal_trapped_recurrence": 60,
    }), unary_mate_classes)
    require(response_mate_classes == Counter({
        "certified_edge_outside_star": 3240,
        "offdiagonal_inside_star": 180,
        "diagonal_endpoint_inside_star": 324,
    }), response_mate_classes)
    require(len(trapped_records) == 60, len(trapped_records))
    require(len(trapped_response_records) == 324,
            len(trapped_response_records))
    trapped_word_histogram = Counter(
        record["private_word"] for record in trapped_records
    )
    trapped_retain_histogram = Counter(
        record["retains_coloop_edge"] for record in trapped_records
    )
    require(trapped_retain_histogram == Counter({False: 42, True: 18}),
            trapped_retain_histogram)

    return {
        "pure_one_target_matching_choices": len(split.MATCHINGS6),
        "private_mixed_unary_rows": len(private_records),
        "private_mixed_response_rows": len(private_response_records),
        "nonzero_mixed_unary_rows": sum(
            count * number for number, count
            in nonzero_unary_count_by_matching.items()
        ),
        "nonzero_mixed_response_rows": len(private_response_records),
        "private_rows_per_target_matching_histogram":
            dict(sorted(private_count_by_matching.items())),
        "private_response_rows_per_target_matching_histogram":
            dict(sorted(private_response_count_by_matching.items())),
        "supported_unary_rows_per_target_matching_histogram":
            dict(sorted(supported_unary_count_by_matching.items())),
        "nonzero_unary_rows_per_target_matching_histogram":
            dict(sorted(nonzero_unary_count_by_matching.items())),
        "supported_response_rows_per_target_matching_histogram":
            dict(sorted(supported_response_count_by_matching.items())),
        "mixed_unary_occurrence_count_histogram":
            dict(sorted(unary_row_occurrence_histogram.items())),
        "mixed_response_occurrence_count_histogram":
            dict(sorted(response_row_occurrence_histogram.items())),
        "alternate_mates_per_private_row": len(split.MATCHINGS6) - 1,
        "all_unary_alternate_mates":
            len(private_records) * (len(split.MATCHINGS6) - 1),
        "unary_mate_classification":
            dict(sorted(unary_mate_classes.items())),
        "all_response_alternate_occurrences":
            len(private_response_records) * 104,
        "response_mate_classification":
            dict(sorted(response_mate_classes.items())),
        "offdiagonal_exit": (
            "every offdiagonal mate has exactly two cross-colour edges and "
            "at least one lies outside the closed star centred at 0"
        ),
        "diagonal_coloop_exit": (
            "36 all-diagonal mates create a nonzero pure-zero perfect "
            "matching omitting edge 01"
        ),
        "trapped_recurrence": {
            "unary_count": len(trapped_records),
            "response_count": len(trapped_response_records),
            "private_word_histogram": dict(sorted(trapped_word_histogram.items())),
            "alternate_retains_01_histogram": {
                str(key): value for key, value
                in sorted(trapped_retain_histogram.items())
            },
            "unary_representative": trapped_records[0],
            "response_representative": trapped_response_records[0],
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    split = load_split()
    ledger = {
        "theorem": "h3 split spoke guard first complete-row recurrence",
        "pins": PINS,
        "base_complete_row_scan": base_complete_row_silence(split),
        "first_missing_target_recurrence":
            classify_first_pure_one_recurrence(split),
        "frontier_effect": (
            "the split counterguard is not removed by its currently "
            "supported unary/response equations.  Supplying the mandatory "
            "pure-one target creates private mixed unary and response rows; "
            "most mates exit through offdiagonal/outside-star or coloop "
            "destruction, but 60 unary and 324 response diagonal closed-star "
            "mates remain trapped"
        ),
        "shortest_next_test": (
            "adjoin the independent pure-two target packet and scan the 60 "
            "trapped pure-one mates jointly across all words/four heads; "
            "either a second colour anchor forces an exit, or classify the "
            "finite simultaneous trapped core"
        ),
        "scope": (
            "exact h=3 polynomial support and complete unary/four-response "
            "scan for the a8ef1a4 guard plus one pure-one target matching. "
            "The target matching is assigned unit coefficient; this is a "
            "support/first-mate classification, not a complete source."
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
    print("base unary+four-response scan: SILENT")
    print("pure-one target choices: 15")
    print("private mixed unary/response rows: 48/36")
    print("unary mate exits offdiag/coloop: 576/36")
    print("response mate exits outside/offdiag-inside: 3240/180")
    print("diagonal closed-star recurrence unary/response: 60/324")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
