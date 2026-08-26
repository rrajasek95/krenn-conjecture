#!/usr/bin/env python3
"""Audit the proposed chart-26 degree-eight factorization threshold.

This is a bounded structural census.  It does not close the degree-eight
inverse-incidence graph.  It proves the t-divisibility reduction below the
new y^4 head, enumerates every alternative original leading divisor at the
205 target-rooted y^4 seeds, and tests the resulting two-column S-pairs on
the shorter y^7*t and y^6*t^2 target divisors.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRST_PATH = ROOT / "computations/verify_n8_chart26_first_homogeneous_spair.py"
D7_PATH = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_y10_d7_staged_blocks.json"
D8_PATH = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_y10_dead_row_original_d8.json"
RESULT = HERE / "results_d8_factorization_threshold.json"

EXPECTED = {
    FIRST_PATH: "48a74185944b32455ac450a1715cc4cae1d2a4b3f482ff4220219d051e2e433b",
    D7_PATH: "90a107b47957ec102a74994fd460a861b66e0c8e6aaffbc3e546919f0ecda2f4",
    D8_PATH: "1b09e4a0941b96feb32cbb1a846dfd5582237a5dfb5267ae829492dae2f706f5",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def quotient(dividend, divisor):
    answer = list(dividend)
    for value in divisor:
        if value not in answer:
            return None
        answer.remove(value)
    return bytes(answer)


def add(output, row, value):
    value = output.get(row, Fraction(0)) + value
    if value:
        output[row] = value
    else:
        output.pop(row, None)


def multiply(left, right):
    return bytes(sorted(left + right))


def divisors(row, degree):
    seen = set()
    for positions in combinations(range(len(row)), degree):
        item = bytes(row[index] for index in positions)
        if item not in seen:
            seen.add(item)
            yield item


def physical_matching(D5, row):
    edges = tuple(sorted(tuple(D5.COORDINATES[cell][:2]) for cell in row))
    degree = Counter(site for edge in edges for site in edge)
    require(len(edges) == 4 and degree == Counter({site: 1 for site in range(8)}),
            "a degree-four original lead stopped being a perfect matching")
    return edges


def exchange_type(D5, left, right):
    left_edges = set(physical_matching(D5, left))
    right_edges = set(physical_matching(D5, right))
    difference = left_edges ^ right_edges
    adjacency = defaultdict(set)
    for a, b in difference:
        adjacency[a].add(b)
        adjacency[b].add(a)
    components = []
    unseen = set(adjacency)
    while unseen:
        start = min(unseen)
        stack = [start]
        component = set()
        while stack:
            site = stack.pop()
            if site in component:
                continue
            component.add(site)
            stack.extend(adjacency[site] - component)
        unseen -= component
        components.append(len(component))
    physical_common = left_edges & right_edges
    exact_common = set(left) & set(right)
    relabelled_common = []
    for edge in sorted(physical_common):
        left_cell = next(cell for cell in left
                         if tuple(D5.COORDINATES[cell][:2]) == edge)
        right_cell = next(cell for cell in right
                          if tuple(D5.COORDINATES[cell][:2]) == edge)
        if left_cell != right_cell:
            relabelled_common.append({
                "edge": list(edge),
                "left_cell": f"{left_cell:02x}",
                "right_cell": f"{right_cell:02x}",
                "left_coordinate": list(D5.COORDINATES[left_cell]),
                "right_coordinate": list(D5.COORDINATES[right_cell]),
            })
    if not components:
        physical_type = "LABEL_ONLY"
    else:
        physical_type = "+".join(f"C{size}" for size in sorted(components))
    return {
        "physical_type": physical_type,
        "cycle_lengths": sorted(components),
        "common_physical_edges": [list(edge) for edge in sorted(physical_common)],
        "common_exact_cells": [f"{cell:02x}" for cell in sorted(exact_common)],
        "relabelled_common_edges": relabelled_common,
    }


def s_pair(polynomials, first_code, first_multiplier,
           second_code, second_multiplier, first_term=None):
    first = polynomials[first_code]
    second = polynomials[second_code]
    first_lead = (first_term if first_term is not None
                  else min(row for row in first if len(row) == 4))
    second_lead = min(row for row in second if len(row) == 4)
    first_coefficient = Fraction(first[first_lead])
    second_coefficient = Fraction(second[second_lead])
    output = {}
    for row, value in first.items():
        add(output, multiply(row, first_multiplier),
            second_coefficient * Fraction(value))
    for row, value in second.items():
        add(output, multiply(row, second_multiplier),
            -first_coefficient * Fraction(value))
    common_top = multiply(first_lead, first_multiplier)
    require(common_top == multiply(second_lead, second_multiplier)
            and common_top not in output, "S-pair failed to cancel common top")
    return output


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    FIRST = load("d8_threshold_first", FIRST_PATH)
    D5 = FIRST.D5
    polynomials, lead_to_code = FIRST.original_basis()
    d7 = json.loads(D7_PATH.read_text())
    d8 = json.loads(D8_PATH.read_text())
    require(d7["logical_sha256"]
            == "30e98f20fd4f5f7a08b43295cf6eb93b46cefc96a232dc44ed0a03c72538251a"
            and d7["new_head_kernel_dimension"] == 0
            and d7["singleton_pivot_columns"] == 10411,
            "degree-seven standardness input changed")
    require(d8["logical_sha256"]
            == "e5388aeb4ff6adfe87d30457a933c5dddadc3c7b5a6a96344b1179ac9570b0ce"
            and d8["new_t_free_y4_seed_columns"] == 205
            and d8["direct_y8_target_incidences"] == 0,
            "degree-eight seed input changed")

    target = bytes.fromhex(d8["target_y10_row"])
    target_sites = Counter(site for cell in target
                           for site in D5.COORDINATES[cell][:2])
    require(target_sites[5] == 0, "target multiplier support gained site 5")
    target_short = {
        bytes(target[index] for index in positions)
        for degree in (6, 7)
        for positions in combinations(range(len(target)), degree)
    }

    # A universal factorization-only threshold is false already at degree 5:
    # the frozen first homogeneous S-pair has |u|=1 on both sides and is a
    # decorated relabelling exchange on the same physical matching.
    first_left = bytes.fromhex("0948c6f4")
    first_right = bytes.fromhex("0948c6f5")
    first_lcm = bytes(sorted(set(first_left) | set(first_right)))
    first_exchange = exchange_type(D5, first_left, first_right)
    require(len(quotient(first_lcm, first_left)) == 1
            and len(quotient(first_lcm, first_right)) == 1
            and first_exchange["physical_type"] == "LABEL_ONLY"
            and len(first_exchange["relabelled_common_edges"]) == 1,
            "degree-five decorated counterguard changed")

    seeds = sorted({
        (record["source_code"], bytes.fromhex(record["multiplier_y"]))
        for record in d8["incident_records"]
        if record["multiplier_t_exponent"] == 0
    })
    require(len(seeds) == 205 and all(len(multiplier) == 4
                                      for _code, multiplier in seeds),
            "t-free degree-eight seeds changed")

    exchanges = {}
    for code, multiplier in seeds:
        lead = FIRST.leading_monomial(polynomials[code])
        require(len(lead) == 4, "source lead changed degree")
        top = multiply(lead, multiplier)
        for alternative in divisors(top, 4):
            other_code = lead_to_code.get(alternative)
            if other_code is None or alternative == lead:
                continue
            other_multiplier = quotient(top, alternative)
            left = (code, multiplier)
            right = (other_code, other_multiplier)
            key = tuple(sorted((left, right)))
            if key in exchanges:
                continue
            profile = exchange_type(D5, lead, alternative)
            # Since the target multiplier has no site 5, every alternative
            # lead must use the unique site-5 cell supplied by the first lead.
            site5_left = next(cell for cell in lead
                              if 5 in D5.COORDINATES[cell][:2])
            site5_right = next(cell for cell in alternative
                               if 5 in D5.COORDINATES[cell][:2])
            require(site5_left == site5_right,
                    "alternative target-rooted lead changed the site-5 cell")
            spoly = s_pair(polynomials, code, multiplier,
                           other_code, other_multiplier)
            target_hits = {row: value for row, value in spoly.items()
                           if row in target_short and value}
            exchanges[key] = {
                "left_code": code,
                "left_word": "".join(map(str, D5.decode_word(code))),
                "left_lead": lead.hex(),
                "left_multiplier": multiplier.hex(),
                "right_code": other_code,
                "right_word": "".join(map(str, D5.decode_word(other_code))),
                "right_lead": alternative.hex(),
                "right_multiplier": other_multiplier.hex(),
                "exchange": profile,
                "site5_cell": f"{site5_left:02x}",
                "site5_coordinate": list(D5.COORDINATES[site5_left]),
                "S_pair_degree_profile": {
                    str(degree): count for degree, count
                    in sorted(Counter(map(len, spoly)).items())
                },
                "shorter_target_hits": [[row.hex(), value.numerator, value.denominator]
                                         for row, value in sorted(target_hits.items())],
            }

    type_histogram = Counter(record["exchange"]["physical_type"]
                             for record in exchanges.values())
    feeding = [record for record in exchanges.values()
               if record["shorter_target_hits"]]
    feeding_histogram = Counter(record["exchange"]["physical_type"]
                                for record in feeding)
    require(not any("C8" in kind for kind in type_histogram),
            "a target-rooted C8 exchange survived the site-5 guard")
    require(set(type_histogram) <= {"LABEL_ONLY", "C4", "C6", "C4+C4"},
            "unexpected matching-exchange type")

    examples = {}
    for kind in sorted(type_histogram):
        examples[kind] = next(record for record in exchanges.values()
                              if record["exchange"]["physical_type"] == kind)
    feeding_examples = {}
    for kind in sorted(feeding_histogram):
        feeding_examples[kind] = next(record for record in feeding
                                      if record["exchange"]["physical_type"] == kind)

    # The leading-row divisor packet above is only the root edge.  For the
    # structural closure census, inspect every degree-four matching term M of
    # each seed provider and every alternative original leading divisor N of
    # M*u.  These are exactly the one-hop inverse-top-incidence exits used by
    # the staged closure, but no transitive solve is performed here.
    one_hop = {}
    for code, multiplier in seeds:
        for matching_term, matching_coefficient in polynomials[code].items():
            if len(matching_term) != 4:
                continue
            top = multiply(matching_term, multiplier)
            for alternative in divisors(top, 4):
                other_code = lead_to_code.get(alternative)
                if other_code is None or alternative == matching_term:
                    continue
                other_multiplier = quotient(top, alternative)
                key = (code, multiplier, matching_term,
                       other_code, other_multiplier, alternative)
                if key in one_hop:
                    continue
                profile = exchange_type(D5, matching_term, alternative)
                site5_left = next(cell for cell in matching_term
                                  if 5 in D5.COORDINATES[cell][:2])
                site5_right = next(cell for cell in alternative
                                   if 5 in D5.COORDINATES[cell][:2])
                require(site5_left == site5_right,
                        "one-hop alternative changed the site-5 cell")
                spoly = s_pair(polynomials, code, multiplier,
                               other_code, other_multiplier,
                               first_term=matching_term)
                target_hits = {row: value for row, value in spoly.items()
                               if row in target_short and value}
                one_hop[key] = {
                    "left_code": code,
                    "left_word": "".join(map(str, D5.decode_word(code))),
                    "left_matching_term": matching_term.hex(),
                    "left_matching_coefficient": [
                        Fraction(matching_coefficient).numerator,
                        Fraction(matching_coefficient).denominator,
                    ],
                    "left_multiplier": multiplier.hex(),
                    "right_code": other_code,
                    "right_word": "".join(map(str, D5.decode_word(other_code))),
                    "right_lead": alternative.hex(),
                    "right_multiplier": other_multiplier.hex(),
                    "exchange": profile,
                    "site5_cell": f"{site5_left:02x}",
                    "shorter_target_hits": [[row.hex(), value.numerator,
                                             value.denominator]
                                            for row, value in sorted(target_hits.items())],
                }
    one_hop_histogram = Counter(record["exchange"]["physical_type"]
                                for record in one_hop.values())
    one_hop_feeding = [record for record in one_hop.values()
                       if record["shorter_target_hits"]]
    one_hop_feeding_histogram = Counter(
        record["exchange"]["physical_type"] for record in one_hop_feeding
    )
    require(not any("C8" in kind for kind in one_hop_histogram),
            "one-hop C8 exchange survived the site-5 guard")
    one_hop_examples = {
        kind: next(record for record in one_hop.values()
                   if record["exchange"]["physical_type"] == kind)
        for kind in sorted(one_hop_histogram)
    }
    one_hop_feeding_examples = {
        kind: next(record for record in one_hop_feeding
                   if record["exchange"]["physical_type"] == kind)
        for kind in sorted(one_hop_feeding_histogram)
    }

    # Test the sharpened unique-perfect-matching formulation on every
    # target-derived decorated multiplier U through |U|=5.  A compatible
    # provider is required to have a literal normalized term q with q*U
    # dividing the target and with source t-exponent at most two (|q|>=2).
    # Its leading matching M is private exactly when M*U has no other
    # original leading-matching divisor.
    term_sources = defaultdict(list)
    for code, polynomial in polynomials.items():
        for term in polynomial:
            if 2 <= len(term) <= 4:
                term_sources[term].append(code)
    unique_pm_by_degree = {}
    unique_pm_failures = []
    for multiplier_degree in range(0, 6):
        multipliers = sorted({
            bytes(target[index] for index in positions)
            for positions in combinations(range(len(target)), multiplier_degree)
        })
        records = []
        for multiplier in multipliers:
            remaining = quotient(target, multiplier)
            require(remaining is not None, "target multiplier stopped dividing target")
            compatible_reasons = {}
            for term_degree in range(2, min(4, len(remaining)) + 1):
                for term in divisors(remaining, term_degree):
                    for code in term_sources.get(term, ()):
                        compatible_reasons.setdefault(code, term)
            private = []
            nonprivate_details = []
            for code, reason in sorted(compatible_reasons.items()):
                lead = FIRST.leading_monomial(polynomials[code])
                top = multiply(lead, multiplier)
                owners = sorted({lead_to_code[item]
                                 for item in divisors(top, 4)
                                 if item in lead_to_code})
                require(code in owners, "own leading matching stopped dividing top")
                if owners == [code]:
                    private.append((code, lead, reason))
                else:
                    nonprivate_details.append({
                        "code": code,
                        "word": "".join(map(str, D5.decode_word(code))),
                        "lead_matching": lead.hex(),
                        "target_incident_source_term": reason.hex(),
                        "alternative_owners": [
                            {
                                "code": owner,
                                "word": "".join(map(str, D5.decode_word(owner))),
                                "lead_matching": FIRST.leading_monomial(
                                    polynomials[owner]
                                ).hex(),
                                "exchange": exchange_type(
                                    D5, lead,
                                    FIRST.leading_monomial(polynomials[owner])
                                ),
                            }
                            for owner in owners if owner != code
                        ],
                    })
            record = {
                "multiplier": multiplier.hex(),
                "compatible_providers": len(compatible_reasons),
                "private_providers": len(private),
            }
            if private:
                code, lead, reason = private[0]
                record["lex_private_witness"] = {
                    "code": code,
                    "word": "".join(map(str, D5.decode_word(code))),
                    "lead_matching": lead.hex(),
                    "target_incident_source_term": reason.hex(),
                    "top_row": multiply(lead, multiplier).hex(),
                }
            elif compatible_reasons:
                failure = {
                    "degree": multiplier_degree,
                    **record,
                }
                if not unique_pm_failures:
                    failure["all_compatible_provider_obstructions"] = nonprivate_details
                unique_pm_failures.append(failure)
            records.append(record)
        unique_pm_by_degree[str(multiplier_degree)] = {
            "target_multipliers": len(multipliers),
            "with_compatible_provider": sum(
                bool(record["compatible_providers"]) for record in records
            ),
            "with_private_provider": sum(
                bool(record["private_providers"]) for record in records
            ),
            "minimum_private_providers": min(
                (record["private_providers"] for record in records
                 if record["compatible_providers"]), default=0
            ),
            "records": records,
        }

    if mutate:
        target_sites[5] = 1
    require(target_sites[5] == 0, "hostile target-site mutation survived")

    result = {
        "format": "n8-orbit26-d8-factorization-threshold-audit-v1",
        "status": "TARGET_SPECIFIC_THRESHOLD_TRUE_BUT_UNIVERSAL_FACTORIZATION_LEMMA_FALSE",
        "target": target.hex(),
        "lower_multiplier_threshold": {
            "statement": (
                "At total source degree eight, every column with encoded-y "
                "multiplier length below four contains t and is t times a "
                "degree-seven column. The frozen target-rooted degree-seven "
                "closure peels all 10,411 new-head columns and has kernel zero; "
                "therefore these lower multiplier layers cannot create a pivot."
            ),
            "scope": "target-specific consequence of the exact d7 theorem, not a universal matching-factorization theorem",
            "d7_closed_columns": d7["closed_y7_columns"],
            "d7_singleton_pivots": d7["singleton_pivot_columns"],
            "d7_kernel_dimension": d7["new_head_kernel_dimension"],
        },
        "universal_counterguard": {
            "left_lead": first_left.hex(),
            "right_lead": first_right.hex(),
            "lcm": first_lcm.hex(),
            "multiplier_length_each": 1,
            "exchange": first_exchange,
            "frozen_nonzero_remainder_terms": 180,
            "verdict": (
                "decorated source labels already admit a nonzero top cancellation "
                "at |u|=1; factorization alone does not imply peelability"
            ),
        },
        "degree8_new_head": {
            "t_free_seed_columns": len(seeds),
            "direct_y8_target_rows": d8["direct_y8_target_incidences"],
            "alternative_leading_exchange_pairs": len(exchanges),
            "exchange_type_histogram": dict(sorted(type_histogram.items())),
            "exchange_examples": examples,
            "shorter_tail_feeding_pairs": len(feeding),
            "shorter_tail_feeding_type_histogram": dict(sorted(feeding_histogram.items())),
            "shorter_tail_feeding_examples": feeding_examples,
            "one_hop_all_matching_terms": {
                "exchange_exits": len(one_hop),
                "exchange_type_histogram": dict(sorted(one_hop_histogram.items())),
                "exchange_examples": one_hop_examples,
                "shorter_tail_feeding_exits": len(one_hop_feeding),
                "shorter_tail_feeding_type_histogram": dict(sorted(
                    one_hop_feeding_histogram.items()
                )),
                "shorter_tail_feeding_examples": one_hop_feeding_examples,
                "scope": (
                    "all degree-four matching terms of the 205 seed providers "
                    "and all alternative original leading divisors; no transitive "
                    "inverse-incidence closure"
                ),
            },
            "site5_guard": (
                "the target monomial contains no coordinate incident to site 5. "
                "Thus M*u contains exactly M's site-5 cell, every alternative "
                "perfect-matching lead N uses that same decorated cell, and M/N "
                "cannot differ on all eight sites. C8 is impossible."
            ),
        },
        "target_derived_unique_PM_test_through_u5": {
            "by_multiplier_degree": unique_pm_by_degree,
            "failures": unique_pm_failures,
            "verdict": (
                "every target-derived decorated multiplier with at least one "
                "literal compatible provider has a compatible provider whose "
                "leading perfect matching is the unique original leading "
                "matching divisor of M*U"
                if not unique_pm_failures else
                "the proposed unique-perfect-matching selection fails on the "
                "displayed smallest target-derived decorated multiplier"
            ),
            "scope_guard": (
                "finite exact chart26 target-derived multipliers only; this does "
                "not assert the statement for arbitrary off-target decorated U"
            ),
        },
        "theorem": (
            "The first new target-specific layer is |u_y|=4 only because lower "
            "layers are t times the exactly peeled degree-seven module. At the "
            "205 new seeds, alternative decorated matching leads are classified "
            "by the displayed exact census. The no-site-5 target guard excludes "
            "C8; only the enumerated label/C4/C6 (and, if present, disconnected "
            "C4+C4) types can feed the y10*t2 shorter tails."
        ),
        "scope": (
            "all 205 literal t-free target-rooted d8 seed columns and every "
            "alternative original leading divisor of their top rows; this is not "
            "the transitive inverse-incidence closure or a degree-eight membership solve"
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("types", result["degree8_new_head"]["exchange_type_histogram"])
    print("feeding", result["degree8_new_head"]["shorter_tail_feeding_type_histogram"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
