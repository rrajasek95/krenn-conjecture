#!/usr/bin/env python3
"""Close the minimal split-spoke guard after all three target colours.

Starting from b3cdd37, enforce coefficients rather than retaining its 384
support-level trapped unary/response mates.  Every trapped unary mate changes
the pure-one target from 1 to 0.  Among response mates, exact cancellation,
the pure-zero/pure-one normalizations, and absence of an already outside-star
occurrence leave 120 labelled (100 value-distinct) states.

Adjoin each of the 15 possible pure-two target matchings.  Every one of the
1800 labelled completions has a private nonzero unary word in which each of
the three colours occurs twice.  Its selected perfect matching is the unique
all-diagonal matching of that word.  Every alternate therefore has a
cross-colour edge outside the closed star at zero.  Thus the minimal split
counterguard cannot survive three-colour target completion.

This closes that literal counterguard, not every arbitrary cross-block rank-
two response packet.
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
    "computations/verify_h3_active_coloop_spoke_split_guard_complete_row_recurrence.py":
        "dea4aa432359668513e3c66660d25fda09754da14f64439a01ef63fe887bb51f",
    "notes/h3-active-coloop-spoke-split-guard-complete-row-recurrence.md":
        "e559d4be2455705bf4be121424f21468b7a60cf83fe11b08a9e84336ecb4d5ba",
    "computations/verify_h3_active_coloop_spoke_homogeneous_block_split_gate.py":
        "eedd0973a823995e9811cca114c9827e2d75df571e127d87232066e4f8333e79",
    "notes/h3-active-coloop-spoke-homogeneous-block-split-gate.md":
        "7c7255a02d27e8be88354edaabcdb7912f9d85ec49c8efbe092f2030d1b991c3",
}
EXPECTED_LEDGER_SHA256 = (
    "53b1f14b3aa61887af43489c9740bc41f71f3421206147f9af571a6544cdacac"
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
        "three_colour_split_guard", ROOT / relative
    )
    require(specification is not None and specification.loader is not None,
            "cannot import split guard")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def row_value(terms):
    return sum((term[-1] for term in terms), Q(0))


def target_value(split, q_values, colour):
    return row_value(split.target_terms((colour,) * 6, q_values))


def pure_zero_coloop_survives(split, q_values) -> bool:
    return all((0, 1) in matching for matching, _cells, _value
               in split.target_terms((0,) * 6, q_values))


def add_product_with_value(factors, desired_value) -> bool:
    """Set missing factors deterministically so their product is desired."""
    missing = []
    old_product = Q(1)
    for values, label in factors:
        value = values.get(label, Q(0))
        if value:
            old_product *= value
        else:
            missing.append((values, label))
    if not missing:
        return False
    for values, label in missing[:-1]:
        values[label] = Q(1)
    values, label = missing[-1]
    values[label] = desired_value / old_product
    return True


def has_outside_response_occurrence(split, p_values, s_values, q_values,
                                    d_values) -> bool:
    star = frozenset(split.edge(0, site) for site in range(1, 6))
    for word in itertools.product(split.COLOURS, repeat=6):
        if len(set(word)) == 1:
            continue
        for head_p in split.HEADS:
            for head_s in split.HEADS:
                terms = split.response_terms(
                    head_p, head_s, word,
                    p_values, s_values, q_values, d_values,
                )
                for term in terms:
                    certified = (() if term[0] == "D" else
                                 (split.edge(term[1], term[2]),))
                    certified += tuple(
                        (left, right)
                        for left, right, left_colour, right_colour in term[-2]
                        if left_colour != right_colour
                    )
                    if any(physical not in star for physical in certified):
                        return True
    return False


def construct_first_colour_closed_states(split):
    """Return exact normalized closed-star states after one response mate."""
    star = frozenset(split.edge(0, site) for site in range(1, 6))
    mixed_words = tuple(
        word for word in itertools.product(split.COLOURS, repeat=6)
        if len(set(word)) != 1
    )
    census = Counter()
    states = []

    for target_matching in split.MATCHINGS6:
        q_values = dict(split.GUARD_Q)
        for left, right in target_matching:
            q_values[split.q_label(left, right, 1, 1)] = Q(1)
        require(target_value(split, q_values, 0) == 1
                and target_value(split, q_values, 1) == 1,
                (target_matching, q_values))

        # Every structurally trapped unary mate in b3cdd37 is diagonal.  Its
        # coefficient is forced to cancel the private mixed unary term, and
        # the same new monomial then changes H[111111] from 1 to 0.
        unary_trapped = 0
        for word in mixed_words:
            selected_terms = split.target_terms(word, q_values)
            if len(selected_terms) != 1:
                continue
            selected = selected_terms[0]
            for alternate in split.MATCHINGS6:
                if alternate == selected[0]:
                    continue
                cells = tuple(split.q_label(
                    left, right, word[left], word[right]
                ) for left, right in alternate)
                if any(cell[2] != cell[3] for cell in cells):
                    continue
                extended = dict(q_values)
                if not add_product_with_value(
                    [(extended, cell) for cell in cells], -selected[-1]
                ):
                    continue
                if row_value(split.target_terms(word, extended)) != 0:
                    continue
                if target_value(split, extended, 0) != 1:
                    continue
                if not pure_zero_coloop_survives(split, extended):
                    continue
                unary_trapped += 1
                require(target_value(split, extended, 1) == 0,
                        (target_matching, word, alternate,
                         target_value(split, extended, 1)))
        census["unary_coefficient_valid_but_pure_one_destroyed"] += unary_trapped

        # Construct each all-diagonal response alternate whose endpoint hole
        # lies in the closed star.  The new occurrence coefficient is forced
        # to be the negative of the private selected term.
        for word in mixed_words:
            for head_p in split.HEADS:
                for head_s in split.HEADS:
                    selected_terms = split.response_terms(
                        head_p, head_s, word,
                        split.GUARD_P, split.GUARD_S, q_values, split.GUARD_D,
                    )
                    if len(selected_terms) != 1:
                        continue
                    selected = selected_terms[0]
                    for p_site in split.SITES:
                        for s_site in split.SITES:
                            if (p_site == s_site
                                    or split.edge(p_site, s_site) not in star):
                                continue
                            residual = tuple(
                                site for site in split.SITES
                                if site not in (p_site, s_site)
                            )
                            for alternate in split.perfect_matchings(residual):
                                cells = tuple(split.q_label(
                                    left, right, word[left], word[right]
                                ) for left, right in alternate)
                                if any(cell[2] != cell[3] for cell in cells):
                                    continue
                                occurrence_key = (
                                    "PS", p_site, s_site, alternate
                                )
                                if occurrence_key == selected[:4]:
                                    continue
                                census["structural_diagonal_star_response"] += 1
                                p_values = dict(split.GUARD_P)
                                s_values = dict(split.GUARD_S)
                                extended = dict(q_values)
                                factors = [
                                    (p_values, (head_p, p_site, word[p_site])),
                                    (s_values, (head_s, s_site, word[s_site])),
                                ] + [(extended, cell) for cell in cells]
                                if not add_product_with_value(
                                    factors, -selected[-1]
                                ):
                                    continue
                                value = row_value(split.response_terms(
                                    head_p, head_s, word,
                                    p_values, s_values, extended, split.GUARD_D,
                                ))
                                if value:
                                    continue
                                census["exact_response_cancellations"] += 1
                                require(target_value(split, extended, 0) == 1,
                                        (target_matching, word, occurrence_key))
                                if not pure_zero_coloop_survives(
                                    split, extended
                                ):
                                    continue
                                if target_value(split, extended, 1) != 1:
                                    census["pure_one_normalization_destroyed"] += 1
                                    continue
                                if has_outside_response_occurrence(
                                    split, p_values, s_values,
                                    extended, split.GUARD_D,
                                ):
                                    census["already_outside_star"] += 1
                                    continue
                                census["normalized_closed_star_state"] += 1
                                states.append({
                                    "target_one_matching": target_matching,
                                    "cancelled_block": (
                                        head_p, head_s, word
                                    ),
                                    "alternate_occurrence": occurrence_key,
                                    "p": p_values,
                                    "s": s_values,
                                    "q": extended,
                                    "d": dict(split.GUARD_D),
                                })

    require(census == Counter({
        "unary_coefficient_valid_but_pure_one_destroyed": 60,
        "structural_diagonal_star_response": 324,
        "exact_response_cancellations": 270,
        "pure_one_normalization_destroyed": 24,
        "already_outside_star": 126,
        "normalized_closed_star_state": 120,
    }), census)
    value_keys = {
        (tuple(sorted(state["p"].items())),
         tuple(sorted(state["s"].items())),
         tuple(sorted(state["q"].items())))
        for state in states
    }
    require(len(states) == 120 and len(value_keys) == 100,
            (len(states), len(value_keys)))
    return states, census, len(value_keys)


def three_colour_private_exit(split, states):
    star = frozenset(split.edge(0, site) for site in range(1, 6))
    rainbow_words = tuple(
        word for word in itertools.product(split.COLOURS, repeat=6)
        if Counter(word) == Counter({0: 2, 1: 2, 2: 2})
    )
    require(len(rainbow_words) == 90, len(rainbow_words))

    witness_histogram = Counter()
    labelled = 0
    value_packets = set()
    example = None
    alternate_checks = 0
    for state in states:
        for target_two_matching in split.MATCHINGS6:
            q_values = dict(state["q"])
            for left, right in target_two_matching:
                q_values[split.q_label(left, right, 2, 2)] = Q(1)
            require(target_value(split, q_values, colour=0) == 1
                    and target_value(split, q_values, colour=1) == 1
                    and target_value(split, q_values, colour=2) == 1,
                    (state, target_two_matching))
            value_packets.add((
                tuple(sorted(state["p"].items())),
                tuple(sorted(state["s"].items())),
                tuple(sorted(q_values.items())),
            ))

            witnesses = []
            for word in rainbow_words:
                terms = split.target_terms(word, q_values)
                if len(terms) != 1 or not terms[0][-1]:
                    continue
                selected = terms[0]
                # Since every colour class has size two, there is exactly
                # one all-diagonal perfect matching: pair equal colours.
                diagonal = tuple(
                    matching for matching in split.MATCHINGS6
                    if all(word[left] == word[right]
                           for left, right in matching)
                )
                require(diagonal == (selected[0],),
                        (word, selected, diagonal))
                for alternate in split.MATCHINGS6:
                    if alternate == selected[0]:
                        continue
                    cross = tuple(
                        physical for physical in alternate
                        if word[physical[0]] != word[physical[1]]
                    )
                    require(cross and any(edge not in star for edge in cross),
                            (word, selected[0], alternate, cross, star))
                    alternate_checks += 1
                witnesses.append((word, selected))
            require(witnesses, (state, target_two_matching))
            witness_histogram[len(witnesses)] += 1
            labelled += 1
            if example is None:
                word, selected = witnesses[0]
                example = {
                    "pure_one_matching": repr(
                        state["target_one_matching"]
                    ),
                    "pure_two_matching": repr(target_two_matching),
                    "private_word": "".join(map(str, word)),
                    "selected_matching": repr(selected[0]),
                    "selected_value": str(selected[-1]),
                    "private_witnesses_in_packet": len(witnesses),
                }

    expected_histogram = Counter({
        3: 722, 4: 466, 2: 408, 5: 134,
        1: 32, 6: 30, 7: 8,
    })
    require(labelled == 1800
            and len(value_packets) == 1500
            and witness_histogram == expected_histogram,
            (labelled, len(value_packets), witness_histogram))
    require(alternate_checks
            == sum(number * count * 14
                   for number, count in witness_histogram.items()),
            alternate_checks)
    return {
        "normalized_first_colour_labelled_states": len(states),
        "pure_two_target_matching_choices": len(split.MATCHINGS6),
        "three_colour_labelled_packets": labelled,
        "three_colour_value_distinct_packets": len(value_packets),
        "rainbow_private_witness_count_histogram":
            dict(sorted(witness_histogram.items())),
        "private_witnesses_total": sum(
            number * count for number, count in witness_histogram.items()
        ),
        "alternate_matchings_checked": alternate_checks,
        "all_packets_have_exit_only_private_row": True,
        "reason": (
            "a 2+2+2 word has one all-diagonal matching.  The private "
            "selected occurrence is that matching; every alternate has a "
            "cross-colour edge, and a perfect matching cannot put all its "
            "cross edges in one star"
        ),
        "representative": example,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    split = load_split()
    states, first_census, distinct = construct_first_colour_closed_states(split)
    ledger = {
        "theorem": "h3 split spoke guard three-colour private exit",
        "pins": PINS,
        "coefficient_valid_first_colour_core": {
            "census": dict(sorted(first_census.items())),
            "labelled_states": len(states),
            "value_distinct_states": distinct,
            "correction_to_support_recurrence": (
                "the 60 unary support mates all destroy H111=1.  Of 324 "
                "structural response mates, 270 cancel their selected row; "
                "24 then destroy H111 and 126 already create an outside-star "
                "response occurrence, leaving 120 labelled states"
            ),
        },
        "third_colour_exit": three_colour_private_exit(split, states),
        "frontier_effect": (
            "the smallest two-word/four-occurrence split-rank counterguard "
            "cannot occur in a complete three-colour target packet.  After "
            "the only coefficient-valid closed-star first-colour recurrence, "
            "the third target colour forces a private 2+2+2 unary row whose "
            "every mate is an offdiagonal outside-star Hall exit"
        ),
        "scope": (
            "exact h=3 coefficient and support theorem for the literal "
            "minimal counterguard a8ef1a4 and its deterministic first mate. "
            "It does not prove that every arbitrary rank-two cross-block "
            "packet reduces to this guard; homogeneous private-tail "
            "synchronization remains the general theorem."
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
    print("coefficient-valid normalized closed-star states: 120")
    print("three-colour labelled/value packets: 1800/1500")
    print("private 2+2+2 unary witness in every packet: YES")
    print("every witness mate outside/offdiagonal: YES")
    print("minimal split guard after full target completion: CLOSED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
