#!/usr/bin/env python3
"""Audit the triangular rewrite boundary of the E14 private target terms.

The universal G11 target has 24 or 26 endpoint/q monomials absent from every
G11 zero row.  A candidate triangular reduction must pivot a monomial of a
source row that divides one of these private monomials.  Multiplying the row
by the quotient gives a rewrite rule.

This checker proves two exact facts.

* Every possible G11 rewrite rule has another private target monomial among
  its tails.  Hence G11 has no private-terminal pivot order.  In every chart
  its rewrite graph contains a two-cycle exchanging the two endpoint
  orientations of one selected bright tail.
* Unary rows have a private-terminal rule for every private monomial, so they
  break the G11 cycles.  The price is a genuine Buchberger attachment: in 204
  of the 228 endpoint-private chart occurrences the least possible maximum
  tail degree is four (and in the other 24 it is three).  Thus the
  next missing object is the complete unary-times-q S-pair/reduction, not an
  uninspected h=3 coefficient layer.  G22 lives in a different endpoint
  colour grade and cannot supply that reduction directly.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOP_PATH = "computations/verify_h3_c6_e14_three_cell_top_degree_boundary.py"
PINS = {
    TOP_PATH:
        "ac4ae4b8e2a351f4666cc2e196073663da94634ed4aac4c3f4e6b5dd92169313",
    "notes/h3-c6-e14-three-cell-top-degree-boundary.md":
        "75dc1e2d82e9b390fcf172eb3181f000c54b955e20a1b067fd11484df947f629",
}
EXPECTED_LEDGER_SHA256 = (
    "85b45cafa6a6c0f138f5c58606a2d0934b018da9ef9e6afa30b35cf3a1d90b7c"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path, name):
    spec = spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def row_terms(row):
    return tuple(
        (endpoint, monomial)
        for endpoint, polynomial in row.items()
        for monomial in polynomial
    )


def quotient(dividend, divisor):
    answer = list(dividend)
    for factor in divisor:
        if factor not in answer:
            return None
        answer.remove(factor)
    return tuple(sorted(answer))


def multiplied(monomial, multiplier):
    return tuple(sorted(monomial + multiplier))


def response_rules(private, responses, target_word):
    rules = []
    for source in sorted(private):
        endpoint, target_monomial = source
        for word, row in responses.items():
            if word == target_word:
                continue
            terms = row_terms(row)
            for pivot_endpoint, pivot in terms:
                if pivot_endpoint != endpoint:
                    continue
                multiplier = quotient(target_monomial, pivot)
                if multiplier is None:
                    continue
                tails = {
                    (tail_endpoint, multiplied(tail, multiplier))
                    for tail_endpoint, tail in terms
                    if (tail_endpoint, tail) != (pivot_endpoint, pivot)
                }
                rules.append({
                    "source": source,
                    "word": word,
                    "pivot": pivot,
                    "multiplier": multiplier,
                    "private_tails": tails & private,
                })
    return tuple(rules)


def unary_rules(private, unary, target_word):
    rules = []
    for source in sorted(private):
        endpoint, target_monomial = source
        for word, polynomial in unary.items():
            if word == target_word:
                continue
            terms = tuple(polynomial)
            for pivot in terms:
                # Empty/base pivots are not a source-valid new-cell
                # attachment.  Retaining them would trivialize the incidence
                # test without producing the required unary-times-q S-pair.
                if not pivot:
                    continue
                multiplier = quotient(target_monomial, pivot)
                if multiplier is None:
                    continue
                tails = {
                    (endpoint, multiplied(tail, multiplier))
                    for tail in terms if tail != pivot
                }
                rules.append({
                    "source": source,
                    "word": word,
                    "pivot": pivot,
                    "multiplier": multiplier,
                    "private_tails": tails & private,
                    "maximum_tail_degree": max(
                        (len(tail) + len(multiplier)
                         for tail in terms if tail != pivot),
                        default=0,
                    ),
                })
    return tuple(rules)


def display_term(term):
    endpoint, monomial = term
    return [list(endpoint), list(monomial)]


def display_word(word):
    return "".join(map(str, word))


def endpoint_site(variable):
    return variable.split("_")[1]


def audit():
    pin_dependencies()
    top = load(TOP_PATH, "e14_rewrite_top")
    two = top.load(top.TWO_CELL_PATH, "e14_rewrite_two")
    e14 = two.load(two.E14_PATH, "e14_rewrite_base")
    b4 = e14.load(e14.B4_PATH, "e14_rewrite_b4")

    charts = {}
    total_private = 0
    total_response_rules = 0
    total_unary_rules = 0
    minimum_unary_tail_degrees = Counter()
    cycle_types = Counter()

    for first_index in (1, 2, 3):
        for second_index in (1, 2, 3):
            _candidates, _names, responses, unary = two.universal(
                e14, b4, first_index, second_index
            )
            target_word = (1,) * 6
            target_terms = set(row_terms(responses[target_word]))
            zero_terms = set().union(*(
                set(row_terms(row))
                for word, row in responses.items() if word != target_word
            ))
            private = target_terms - zero_terms
            require(len(private) in {24, 26},
                    "the private target set changed")

            r_rules = response_rules(private, responses, target_word)
            require(r_rules, "the G11 private rewrite inventory is empty")
            require(all(rule["private_tails"] for rule in r_rules),
                    "a G11 private-terminal pivot appeared")

            # Freeze the smallest obstruction: a common zero row with a base
            # pivot on each endpoint orientation exchanges the two private
            # occurrences of the same selected q-tail monomial.
            two_cycles = []
            by_source = {}
            for rule in r_rules:
                by_source.setdefault(rule["source"], []).append(rule)
            for rule in r_rules:
                source = rule["source"]
                for other in rule["private_tails"]:
                    for reverse in by_source.get(other, ()): 
                        if (source in reverse["private_tails"]
                                and rule["word"] == reverse["word"]
                                and rule["multiplier"]
                                == reverse["multiplier"]):
                            canonical = tuple(sorted((source, other)))
                            two_cycles.append((canonical, rule, reverse))
            orientation_cycles = [
                record for record in two_cycles
                if (record[0][0][1] == record[0][1][1]
                    and endpoint_site(record[0][0][0][0])
                    == endpoint_site(record[0][1][0][1])
                    and endpoint_site(record[0][0][0][1])
                    == endpoint_site(record[0][1][0][0]))
            ]
            require(orientation_cycles,
                    "the endpoint-orientation two-cycle disappeared")
            cycle, forward, reverse = min(
                orientation_cycles, key=lambda record: record[0]
            )
            require(cycle[0][1] == cycle[1][1],
                    "the minimal cycle stopped sharing its q tail")
            require(endpoint_site(cycle[0][0][0])
                    == endpoint_site(cycle[1][0][1])
                    and endpoint_site(cycle[0][0][1])
                    == endpoint_site(cycle[1][0][0]),
                    "the minimal cycle stopped reversing endpoint orientation")
            cycle_types[(display_word(forward["word"]),
                         cycle[0][1])] += 1

            u_rules = unary_rules(private, unary, (0,) * 6)
            terminal_by_source = {}
            for rule in u_rules:
                if not rule["private_tails"]:
                    terminal_by_source.setdefault(
                        rule["source"], []
                    ).append(rule)
            require(set(terminal_by_source) == private,
                    "a private target term lacks a unary cycle-breaker")
            degree_profile = Counter()
            for source, rules in terminal_by_source.items():
                degree_profile[min(rule["maximum_tail_degree"]
                                   for rule in rules)] += 1
            require(set(degree_profile) <= {3, 4},
                    "the first unary S-pair degree changed")

            total_private += len(private)
            total_response_rules += len(r_rules)
            total_unary_rules += len(u_rules)
            minimum_unary_tail_degrees.update(degree_profile)
            charts[f"{first_index},{second_index}"] = {
                "private_target_term_count": len(private),
                "G11_divisibility_rule_count": len(r_rules),
                "G11_private_terminal_rule_count": 0,
                "unary_divisibility_rule_count": len(u_rules),
                "unary_private_terminal_source_count":
                    len(terminal_by_source),
                "minimum_unary_breaker_maximum_tail_degree":
                    dict(sorted(degree_profile.items())),
                "minimal_G11_two_cycle": {
                    "word": display_word(forward["word"]),
                    "first": display_term(cycle[0]),
                    "second": display_term(cycle[1]),
                    "common_pivot": list(forward["pivot"]),
                    "common_multiplier": list(forward["multiplier"]),
                },
            }

    require(total_private == 228,
            f"the nine-chart private total changed: {total_private}")
    require(total_response_rules == 1108,
            f"the G11 rewrite inventory changed: {total_response_rules}")
    require(total_unary_rules == 1088,
            f"the unary rewrite inventory changed: {total_unary_rules}")
    require(minimum_unary_tail_degrees == Counter({4: 204, 3: 24}),
            "the unary S-pair degree split changed: "
            f"{minimum_unary_tail_degrees}")

    ledger = {
        "pins": PINS,
        "charts": charts,
        "private_target_term_count": total_private,
        "G11_divisibility_rule_count": total_response_rules,
        "G11_private_terminal_rule_count": 0,
        "unary_divisibility_rule_count": total_unary_rules,
        "minimum_unary_breaker_maximum_tail_degree":
            dict(sorted(minimum_unary_tail_degrees.items())),
        "minimal_cycle_type_count": len(cycle_types),
        "minimal_cycle_types": [
            {
                "word": word,
                "q_tail": list(tail),
                "chart_count": count,
            }
            for (word, tail), count in sorted(cycle_types.items())
        ],
        "theorem": (
            "G11 alone has no triangular private-target reduction: all 1,108 "
            "literal divisibility pivots retain a private tail and every "
            "chart contains a two-cycle reversing the endpoint orientations "
            "of one common bright q tail"
        ),
        "cycle_breaker": (
            "complete unary rows have a private-terminal pivot for every one "
            "of the 228 endpoint-private occurrences, but 204 first require "
            "an output monomial of degree four and 24 require degree three"
        ),
        "minimal_missing_face": (
            "the source-provenant unary-times-q Buchberger S-pair, together "
            "with reductions of all its nonprivate degree-three/four tails; "
            "G22 is endpoint-colour-2 graded and cannot serve as the direct "
            "endpoint-colour-1 attachment"
        ),
        "scope": (
            "this is an exact divisibility/rewrite theorem on the nine "
            "universal minimal E14 charts.  It does not assert that all "
            "degree-four S-pair tails reduce, nor arbitrary-support "
            "emptiness or a full-source counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"private rewrite ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 C6 E14 private rewrite/S-pair boundary: PASS (exact)")
    print(f"private_terms={ledger['private_target_term_count']}")
    print(f"G11_rules={ledger['G11_divisibility_rule_count']}")
    print("unary_minimum_tail_degrees="
          f"{ledger['minimum_unary_breaker_maximum_tail_degree']}")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
