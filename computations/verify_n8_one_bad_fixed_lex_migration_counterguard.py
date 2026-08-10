#!/usr/bin/env python3
"""Disprove a fixed-word lex potential for one-bad matching exchange.

The canonical singleton map of the twelve successor identities happens to
move forward in lexicographic target-word order.  That order is not uniform:

* the already frozen first/second exchange charts export both forward and
  backward private words under the same fixed site/colour order;
* a site relabelling reverses the first canonical migration; and
* the frozen independent C4 x C4 matching square is an equal-target,
  coefficient-consistent closed exchange cycle.

The last item is the sharp nonunit guard.  Its four matching monomials have
weights (1,-1,-1,1), so all four plus-binomial exchange rows vanish, their
closed character product is +1, and no parallel opposite-character pair is
present.  The full orbit-0 rectangle is still killed by its tensor fan; the
guard says that target-word order alone cannot supply that missing invariant.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_first_cross_mate_exchange.py":
        "e1d641d64bf0659d6b28ea64bf8a935e17c4da1c7e2c831f0dfb041fc78eaf0c",
    "computations/verify_n8_one_bad_second_top_mate_exchange.py":
        "1df9d9eb63220782d672dd89ce56759c6fb515c923cd9124d162ff0a40862ea5",
    "computations/verify_n8_one_bad_exchange_cycle_gate.py":
        "5348519a352fbdebfd211b68e2a9ed15792993da8f00ed220be09e269bd89447",
    "computations/verify_n8_one_bad_target_migration_dag.py":
        "c1b0fc7a5d5a5e656fad7578fa3ad6ffc54484935131bfe96d68e11c92c2fff1",
    "computations/verify_n8_one_bad_first_closed_exchange_census.py":
        "4e61eaa7e669fe6cf78ffbb2ec6746d001854d5bdc14fed1d0b309e0acd189bf",
    "computations/verify_n8_one_bad_even_cycle_rectangle_obstruction.py":
        "970d9a8dcd12a7cf49ac3b956b6c398db1b5dc45b2de62ba116e138e72fcc0fb",
}
EXPECTED_LEDGER_SHA256 = (
    "a91d5517358192349ed38b0c534bb5be061095c52a357a76908b9a06ae76ccd9"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FIRST_PATH = "computations/verify_n8_one_bad_first_cross_mate_exchange.py"
SECOND_PATH = "computations/verify_n8_one_bad_second_top_mate_exchange.py"
CYCLE_PATH = "computations/verify_n8_one_bad_exchange_cycle_gate.py"
MIGRATION_PATH = "computations/verify_n8_one_bad_target_migration_dag.py"
CLOSURE_PATH = "computations/verify_n8_one_bad_first_closed_exchange_census.py"
RECTANGLE_PATH = "computations/verify_n8_one_bad_even_cycle_rectangle_obstruction.py"


first = load_pinned("one_bad_first_exchange", FIRST_PATH)
base = first.load_base()
second = load_pinned("one_bad_second_exchange", SECOND_PATH)
cycle = load_pinned("one_bad_exchange_cycle", CYCLE_PATH)
migration = load_pinned("one_bad_target_migration", MIGRATION_PATH)
closure = load_pinned("one_bad_first_closure", CLOSURE_PATH)
rectangle = load_pinned("one_bad_rectangle", RECTANGLE_PATH)


def relation(left, right):
    require(left != right, "a private exported word repeated its source word")
    return "forward" if left < right else "backward"


def sharp_source(packet):
    a_matching, b_matching, _b_holes, c_matching, _c_holes = packet
    return (
        tuple((edge, (base.A, base.A)) for edge in a_matching)
        + tuple((edge, (base.B, base.B)) for edge in b_matching)
        + tuple((edge, (base.C, base.C)) for edge in c_matching)
    )


def channels(packet):
    _a_matching, _b_matching, b_holes, _c_matching, c_holes = packet
    return (
        ("bc", base.B, base.C, b_holes[0], c_holes[1]),
        ("cb", base.C, base.B, c_holes[0], b_holes[1]),
    )


def first_arrow_lex_audit():
    histogram = Counter()
    examples = {}
    private_words = 0
    for orbit, packet in enumerate(base.SHARP_REPRESENTATIVES):
        sharp = sharp_source(packet)
        for channel, left_colour, right_colour, left_hole, right_hole in (
                channels(packet)):
            fixed = ((left_hole, left_colour),
                     (right_hole, right_colour))
            response = first.endpoint_tensor(sharp, 2, fixed)
            require(len(response) == 1 and next(iter(response.values())) == 1,
                    "a sharp private response changed")
            response_word = next(iter(response))
            residual = tuple(site for site in base.SITES
                             if site not in (left_hole, right_hole))
            decorated = tuple(
                first.decorated_matching(matching, response_word)
                for matching in base.perfect_matchings(residual)
            )
            old = [matching for matching in decorated
                   if all(cell in sharp for cell in matching)]
            require(len(old) == 1, "a private response route changed")
            mates = [matching for matching in decorated
                     if frozenset(matching) != frozenset(old[0])]
            require(len(mates) == 2, "a first mate count changed")
            for mate in mates:
                top = first.endpoint_tensor(sharp + mate, 3)
                for target_word, coefficient in top.items():
                    if target_word == (base.A,) * 6 or coefficient != 1:
                        continue
                    target_matchings = first.top_decompositions(
                        base, sharp + mate, target_word
                    )
                    require(len(target_matchings) == 1
                            and any(cell in mate
                                    for cell in target_matchings[0]),
                            "a first-arrow private target lost provenance")
                    direction = relation(response_word, target_word)
                    histogram[orbit, direction] += 1
                    private_words += 1
                    examples.setdefault((orbit, direction), {
                        "channel": channel,
                        "source_word": list(response_word),
                        "target_word": list(target_word),
                        "mate": [[list(edge), list(colours)]
                                 for edge, colours in mate],
                    })
    require(histogram == Counter({
        (0, "forward"): 5,
        (0, "backward"): 3,
        (1, "backward"): 4,
    }) and private_words == 12,
            f"the first-arrow lex split changed: {histogram}")
    return {
        "private_target_words": private_words,
        "histogram": [[orbit, direction, count]
                      for (orbit, direction), count
                      in sorted(histogram.items())],
        "examples": [{"orbit": orbit, "direction": direction, **record}
                     for (orbit, direction), record in sorted(examples.items())],
        "all_endpoints_are_singleton_monomial_units": True,
    }


def second_arrow_lex_audit():
    # Re-run the already frozen theorem before refining it by word direction.
    frozen = second.audit_second_routes(base, first)
    require(frozen["second_route_charts"] == 168,
            "the frozen second-arrow chart count changed")

    all_matchings = tuple(base.perfect_matchings(base.SITES))
    histogram = Counter()
    examples = {}
    exported_words = 0
    for orbit, packet in enumerate(base.SHARP_REPRESENTATIVES):
        sharp = sharp_source(packet)
        for channel, left_colour, right_colour, left_hole, right_hole in (
                channels(packet)):
            fixed = ((left_hole, left_colour),
                     (right_hole, right_colour))
            response_word = next(iter(first.endpoint_tensor(sharp, 2, fixed)))
            residual = tuple(site for site in base.SITES
                             if site not in (left_hole, right_hole))
            response_matchings = tuple(
                first.decorated_matching(matching, response_word)
                for matching in base.perfect_matchings(residual)
            )
            old_response = [matching for matching in response_matchings
                            if all(cell in sharp for cell in matching)]
            require(len(old_response) == 1,
                    "the second-arrow old response changed")
            first_mates = [matching for matching in response_matchings
                           if frozenset(matching)
                           != frozenset(old_response[0])]
            for first_mate in first_mates:
                first_source = sharp + first_mate
                first_top = first.endpoint_tensor(first_source, 3)
                old_private = {
                    word for word, coefficient in first_top.items()
                    if word != (base.A,) * 6 and coefficient == 1
                }
                for source_word in sorted(old_private):
                    decorated = tuple(
                        first.decorated_matching(matching, source_word)
                        for matching in all_matchings
                    )
                    old_top = [matching for matching in decorated
                               if all(cell in first_source for cell in matching)]
                    require(len(old_top) == 1,
                            "a second-arrow source word changed")
                    alternatives = [
                        matching for matching in decorated
                        if frozenset(matching) != frozenset(old_top[0])
                    ]
                    require(len(alternatives) == 14,
                            "a second-arrow alternative count changed")
                    for top_mate in alternatives:
                        new_cells = tuple(cell for cell in top_mate
                                          if cell not in first_source)
                        second_source = first_source + new_cells
                        second_top = first.endpoint_tensor(second_source, 3)
                        new_private = {
                            word for word, coefficient in second_top.items()
                            if (word != (base.A,) * 6
                                and word not in old_private
                                and coefficient == 1)
                        }
                        require(new_private,
                                "a frozen second route lost its private target")
                        for target_word in new_private:
                            direction = relation(source_word, target_word)
                            histogram[orbit, direction] += 1
                            exported_words += 1
                            examples.setdefault((orbit, direction), {
                                "channel": channel,
                                "source_word": list(source_word),
                                "target_word": list(target_word),
                                "new_cells": [
                                    [list(edge), list(colours)]
                                    for edge, colours in new_cells
                                ],
                            })
    require(histogram == Counter({
        (0, "forward"): 197,
        (0, "backward"): 147,
        (1, "forward"): 68,
        (1, "backward"): 104,
    }) and exported_words == 516,
            f"the second-arrow lex split changed: {histogram}")
    return {
        "route_charts": frozen["second_route_charts"],
        "exported_private_words": exported_words,
        "histogram": [[orbit, direction, count]
                      for (orbit, direction), count
                      in sorted(histogram.items())],
        "examples": [{"orbit": orbit, "direction": direction, **record}
                     for (orbit, direction), record in sorted(examples.items())],
        "all_endpoints_are_singleton_monomial_units": True,
    }


def permute_word(word, permutation):
    answer = [None] * len(word)
    for old_site, colour in enumerate(word):
        answer[permutation[old_site]] = colour
    return tuple(answer)


def canonical_migration_relabelling_guard():
    edges, outcomes, _sources, _translated = migration.migration_edges()
    require(outcomes == Counter({
        "translated_one_class_unit": 14,
        "parallel_character_unit": 2,
    }), "the canonical target-migration theorem changed")
    translated = [edge for edge in edges
                  if edge["endpoint"]["type"]
                  == "translated_one_class_unit"]
    require(all(tuple(edge["origin_target"][1])
                < tuple(edge["endpoint"]["target_label"][1])
                for edge in translated),
            "a canonical migration stopped being forward")

    edge = next(edge for edge in translated
                if edge["origin_target"][1] == [0, 0, 0, 1, 0, 2]
                and edge["endpoint"]["target_label"][1]
                == [0, 0, 2, 1, 0, 1])
    permutation = (0, 1, 5, 3, 4, 2)  # swap sites 2 and 5
    source = permute_word(tuple(edge["origin_target"][1]), permutation)
    target = permute_word(
        tuple(edge["endpoint"]["target_label"][1]), permutation
    )
    require(target < source,
            "the site-relabelled canonical edge stopped being backward")
    return {
        "canonical_translated_edges": len(translated),
        "canonical_direction": "all forward",
        "site_relabelling": list(permutation),
        "relabelled_source_word": list(source),
        "relabelled_target_word": list(target),
        "relabelled_direction": "backward",
        "endpoint_certificate": "transported translated one-class unit",
        "meaning": (
            "absolute lex direction is not invariant under the site symmetry "
            "of the source equations"
        ),
    }


def occurrence(matching):
    return Counter(matching)


def equal_word_nonunit_square():
    gate = cycle.audit_first_commuting_square()
    require(gate["minimum_vertices_for_two_disjoint_C4s"] == 8
            and gate["four_binomial_holonomy"] == 1,
            "the frozen commuting square changed")
    matchings = tuple(tuple(tuple(edge) for edge in matching)
                      for matching in gate["square"])
    m00, m10, m11, m01 = matchings
    require(occurrence(m00) + occurrence(m11)
            == occurrence(m10) + occurrence(m01),
            "the equal-word square lost its occurrence identity")

    word = (0, 0, 1, 1, 2, 2, 0, 1)
    require(len(set(word)) == 3, "the guard word stopped being mixed")
    decorated = [
        tuple((edge, (word[edge[0]], word[edge[1]]))
              for edge in matching)
        for matching in matchings
    ]
    weights = Counter({cell: 1 for monomial in decorated for cell in monomial})
    # Independent C4 switches: one negative cell on each switched component.
    weights[((0, 3), (word[0], word[3]))] = -1
    weights[((4, 7), (word[4], word[7]))] = -1

    monomial_weights = [
        product([weights[cell] for cell in monomial])
        for monomial in decorated
    ]
    require(monomial_weights == [1, -1, 1, -1],
            f"the equal-word Laurent point changed: {monomial_weights}")
    pairs = ((1, 0), (2, 1), (3, 2), (0, 3))
    require(all(monomial_weights[left] + monomial_weights[right] == 0
                for left, right in pairs),
            "the explicit point stopped solving the four exchange rows")

    rows = []
    for left, right in pairs:
        row = Counter(decorated[left])
        row.subtract(decorated[right])
        rows.append(tuple(sorted((cell, exponent)
                                 for cell, exponent in row.items()
                                 if exponent)))
    require(len(set(rows)) == 4,
            "the equal-word square acquired parallel exchange rows")
    total = Counter()
    for row in rows:
        total.update(dict(row))
    require(not +total and not -total and (-1) ** len(rows) == 1,
            "the equal-word square acquired odd holonomy")
    return {
        "target_word": list(word),
        "matching_words_all_equal": True,
        "matchings": [[list(edge) for edge in matching]
                      for matching in matchings],
        "distinct_exchange_displacements": len(set(rows)),
        "closed_dependency_length": len(rows),
        "closed_character_product": 1,
        "parallel_opposite_character_pair": False,
        "localized_cell_point": [
            [f"{edge[0]}{edge[1]}:{colours[0]}{colours[1]}", value]
            for (edge, colours), value in sorted(weights.items())
        ],
        "matching_monomial_values": monomial_weights,
        "verdict": (
            "a source-faithful equal-target matching-exchange cycle is "
            "coefficient-consistent and has neither odd nor parallel "
            "character obstruction"
        ),
    }


def product(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def full_packet_units():
    classifications = {
        str(orbit): [closure.coefficient_audit(orbit, support)["type"]
                     for support in closure.sorted_supports(orbit)]
        for orbit in (0, 1)
    }
    require(classifications == {
        "0": ["odd_character_unit"],
        "1": ["one_class_laurent_unit"] * 8,
    }, "the first closed-packet coefficient classification changed")
    fan = rectangle.audit_shared_zero_fans()
    require(fan["complete_rectangle_ideal"] == "unit over QQ"
            and len(fan["unit_fans"]) == 4,
            "the full rectangle tensor unit changed")
    return {
        "first_closed_exchange_units": classifications,
        "orbit0_rectangle_tensor_fans": len(fan["unit_fans"]),
        "orbit0_complete_rectangle_ideal": fan["complete_rectangle_ideal"],
        "meaning": (
            "the equal-word character square is a genuine local nonunit, "
            "but full source coupling supplies a separate tensor unit"
        ),
    }


def main():
    first_lex = first_arrow_lex_audit()
    second_lex = second_arrow_lex_audit()
    relabelled = canonical_migration_relabelling_guard()
    square = equal_word_nonunit_square()
    packet_units = full_packet_units()
    backward = sum(record[2] for record in first_lex["histogram"]
                   if record[1] == "backward") + sum(
        record[2] for record in second_lex["histogram"]
        if record[1] == "backward"
    )
    require(backward == 258,
            "the combined backward-transition count changed")

    ledger = {
        "pins": PINS,
        "fixed_order": {
            "sites": [0, 1, 2, 3, 4, 5],
            "colours": [0, 1, 2],
            "comparison": "ordinary lexicographic target-word order",
        },
        "first_arrow_test": first_lex,
        "second_arrow_test": second_lex,
        "canonical_migration_symmetry_test": relabelled,
        "first_exact_equal_nonunit_transition": square,
        "full_orbit0_orbit1_packet_check": packet_units,
        "combined_backward_private_targets": backward,
        "verdict": (
            "fixed target-word lex monotonicity is false: backward private "
            "targets occur in both sharp orbits, site symmetry reverses a "
            "canonical migration, and the independent C4 x C4 square is an "
            "equal-target coefficient-consistent closed exchange"
        ),
        "missing_invariant": (
            "target words forget the matching/circuit provenance inside one "
            "fibre and depend on arbitrary site labels.  A valid termination "
            "order must include a source-labelled matching character or the "
            "global boundary-debt/tensor data which kills the orbit0 square"
        ),
        "scope": (
            "the already frozen first and second direct exchange charts, the "
            "sixteen singleton target migrations, the independent physical "
            "commuting square, and the nine first closed orbit0/orbit1 "
            "supports; this is not an enumeration of double repairs"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"fixed-lex counterguard ledger changed: {digest}")

    print("N=8 one-bad fixed-lex migration counterguard: PASS")
    print(f"backward private targets in frozen first/two-arrow data: {backward}")
    print("site-relabelled canonical migration: backward")
    print("equal-target C4xC4 cycle: exact Laurent point, holonomy +1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
