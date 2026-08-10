#!/usr/bin/env python3
"""Source-provenance target migration for the twelve one-bad successors.

The committed repair-mask theorem gives twelve one-class successor targets
and exactly sixteen singleton classes which can contaminate their ordinary
source identities.  This checker forgets support-search order and retains
only the algebraic data

    (target label, contaminating Laurent class, translated target label).

Every contaminant enters only its selected target source row.  Fourteen of
the sixteen resulting class systems contain a translated one-class target,
strictly later in lexicographic word order.  The other two contain two
reduced binomials with the same exponent displacement and respective
character values -1 and +1.  Their quotient is an exact parallel-character
unit.  The translated labels are disjoint from the source labels, so every
chain in this complete singleton-provenance map terminates after one edge.

This is a target/class theorem, not another repair-layer search.  It does not
classify double-cell source tails or later classes outside the sixteen
singleton contaminants frozen by the dependency.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_n8_one_bad_unit_repair_masks.py"
DEPENDENCY_SHA256 = (
    "d50ae7ab884e56cf3a1efb9a43da1cd3c9c7fa502e55113416b4c8c204c56435"
)
EXPECTED_LEDGER_SHA256 = (
    "daf29ded884f44c61a6e83e30f5000514699937ac03a8c20c88d7657be9b7fae"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


path = ROOT / DEPENDENCY
require(sha256(path.read_bytes()).hexdigest() == DEPENDENCY_SHA256,
        "the pinned successor repair-mask theorem changed")
spec = spec_from_file_location("one_bad_repair_masks", path)
R = module_from_spec(spec)
spec.loader.exec_module(R)
C = R.C


def class_trace(normal_form):
    return [[C.cell_name(cell), exponent]
            for cell, exponent in normal_form]


def source_packet(support):
    records = []
    for row, word, monomials in C.closure_fibres(1):
        live = tuple(monomial for monomial in monomials
                     if set(monomial) <= support)
        if live:
            records.append({
                "row": row,
                "word": word,
                "live": live,
                "full": monomials,
            })
    binomial_records = [
        index for index, record in enumerate(records)
        if len(record["live"]) == 2
    ]
    rows = [C.exponent_difference(
        records[index]["live"][0], records[index]["live"][1]
    ) for index in binomial_records]
    basis, dependencies = C.laurent_basis(rows)
    require(not any(C.character(dependency) == -1
                    for dependency in dependencies),
            "a target-migration packet acquired initial odd holonomy")
    return records, binomial_records, rows, basis


def multiply_character(ratios, dependence):
    value = Fraction(1)
    for position, exponent in dependence.items():
        require(exponent.denominator == 1,
                "a target-character dependence became fractional")
        value *= ratios[position] ** exponent.numerator
    return value


def dependence_trace(dependence, two_class_rows, ratios, records):
    return [{
        "multiplicity": coefficient,
        "source_record": two_class_rows[position][0],
        "source_label": [
            records[two_class_rows[position][0]]["row"],
            list(records[two_class_rows[position][0]]["word"]),
        ],
        "character_value": str(ratios[position]),
    } for position, coefficient in sorted(dependence.items())]


def classify_destination(support):
    records, binomial_records, rows, basis = source_packet(support)
    require(len(binomial_records) == 54 and len(basis) == 24,
            "a migration packet changed its initial Laurent lattice")
    reduced = [C.reduce_polynomial(record["live"], basis)
               for record in records]
    units = [index for index, polynomial in enumerate(reduced)
             if len(polynomial) == 1]
    histogram = dict(sorted(Counter(len(polynomial)
                                    for polynomial in reduced).items()))
    if units:
        target = units[0]
        normal_form, coefficient = next(iter(reduced[target].items()))
        require(coefficient, "a translated target coefficient vanished")
        return {
            "type": "translated_one_class_unit",
            "live_records": len(records),
            "plus_binomials": len(binomial_records),
            "laurent_rank": len(basis),
            "reduced_class_histogram": histogram,
            "unit_records": len(units),
            "target_record": target,
            "target_label": [records[target]["row"],
                             list(records[target]["word"])],
            "target_terms": len(records[target]["live"]),
            "target_class": class_trace(normal_form),
            "target_coefficient": coefficient,
        }

    two_class_rows = []
    displacements = []
    ratios = []
    for record_index, polynomial in enumerate(reduced):
        if len(polynomial) != 2:
            continue
        items = sorted(polynomial.items())
        (first, first_coefficient), (second, second_coefficient) = items
        two_class_rows.append((record_index, polynomial))
        displacements.append(C.exponent_difference(dict(first), dict(second)))
        ratios.append(-Fraction(second_coefficient, first_coefficient))

    character_basis, dependencies = C.laurent_basis(displacements)
    bad = [(dependence, multiply_character(ratios, dependence))
           for dependence in dependencies
           if multiply_character(ratios, dependence) != 1]
    require(bad, "a migration endpoint became character-consistent")
    dependence, value = min(
        bad,
        key=lambda item: (
            sum(abs(coefficient) for coefficient in item[0].values()),
            len(item[0]),
            tuple(sorted(item[0].items())),
        ),
    )
    require(value == -1 and len(dependence) == 2
            and set(dependence.values()) == {Fraction(-1), Fraction(1)},
            "the terminal parallel-character collision changed")
    left_position, right_position = sorted(dependence)
    require(displacements[left_position] == displacements[right_position],
            "the terminal rows stopped being parallel")
    require({ratios[left_position], ratios[right_position]}
            == {Fraction(-1), Fraction(1)},
            "the parallel rows lost their opposite characters")

    # Rebuild the exponent-zero and character-nontrivial dependency exactly.
    rebuilt = {}
    for position, coefficient in dependence.items():
        C.axpy(rebuilt, coefficient, displacements[position])
    require(not rebuilt and multiply_character(ratios, dependence) == -1,
            "the terminal holonomy failed exact reconstruction")
    return {
        "type": "parallel_character_unit",
        "live_records": len(records),
        "plus_binomials": len(binomial_records),
        "laurent_rank": len(basis),
        "reduced_class_histogram": histogram,
        "two_class_rows": len(two_class_rows),
        "two_class_rank": len(character_basis),
        "bad_dependencies": len(bad),
        "minimal_holonomy": str(value),
        "minimal_source_trace": dependence_trace(
            dependence, two_class_rows, ratios, records
        ),
    }


def migration_edges():
    edges = []
    source_labels = set()
    translated_labels = set()
    first_contaminants = Counter()

    for support_index, support in enumerate(C.sorted_supports(1)):
        base = R.identity_data(support)
        for first_mask in sorted(
                base["masks"],
                key=lambda mask: (len(mask), sorted(C.cell_name(cell)
                                                   for cell in mask))):
            if len(first_mask) != 1:
                continue
            successor_support = support | first_mask
            successor = R.identity_data(successor_support)
            origin = successor["target_label"]

            for contaminating_mask in sorted(
                    successor["masks"],
                    key=lambda mask: (len(mask), sorted(C.cell_name(cell)
                                                       for cell in mask))):
                if len(contaminating_mask) != 1:
                    continue
                source_labels.add(tuple(origin[1]))
                contaminating_cell = next(iter(contaminating_mask))
                provenance = successor["masks"][contaminating_mask]
                require(len(provenance) == 1,
                        "a singleton contaminant lost unique source provenance")
                source_record, monomial = provenance[0]
                require(source_record == successor["target"],
                        "a singleton contaminant left the selected target row")
                normal_form, coefficient, used = R.reduce_trace(
                    monomial, successor["basis"]
                )
                require(coefficient == 1
                        and dict(normal_form).get(contaminating_cell) == 1,
                        "a contaminating matching lost its positive new class")

                endpoint = classify_destination(
                    successor_support | contaminating_mask
                )
                if endpoint["type"] == "translated_one_class_unit":
                    translated = tuple(endpoint["target_label"][1])
                    require(tuple(origin[1]) < translated,
                            "a translated target stopped increasing lex order")
                    translated_labels.add(translated)

                first_cell = C.cell_name(next(iter(first_mask)))
                contaminating_name = C.cell_name(contaminating_cell)
                first_contaminants[contaminating_name] += 1
                edges.append({
                    "support": support_index,
                    "first_successor_cell": first_cell,
                    "origin_target": origin,
                    "origin_terms": successor["target_terms"],
                    "origin_class_sums": successor["trace_class_sums"],
                    "contaminating_cell": contaminating_name,
                    "contaminating_source_record": source_record,
                    "contaminating_matching": [C.cell_name(cell)
                                               for cell in monomial],
                    "contaminating_class": class_trace(normal_form),
                    "contaminating_basis_rows": len(used),
                    "endpoint": endpoint,
                })

    require(len(edges) == 16,
            "the complete successor singleton-provenance map changed")
    outcome_histogram = Counter(edge["endpoint"]["type"] for edge in edges)
    require(outcome_histogram == Counter({
        "translated_one_class_unit": 14,
        "parallel_character_unit": 2,
    }), "the target-migration endpoint split changed")
    require(first_contaminants == Counter({
        "25:01": 4,
        "25:02": 3,
        "25:22": 1,
        "34:10": 4,
        "34:12": 3,
        "34:22": 1,
    }), "the contaminating-class palette changed")

    # This proves acyclicity of the exact provenance graph without treating
    # support size as a potential: every genuine target edge is lex-increasing,
    # and no translated endpoint is a source vertex of this finite map.
    require(source_labels.isdisjoint(translated_labels),
            "the singleton target-migration map acquired a closed cycle: "
            f"{sorted(source_labels & translated_labels)}")
    return edges, outcome_histogram, source_labels, translated_labels


def abstract_character_lemma():
    # Two equations for the same quotient character, chi(d)=-1 and chi(d)=1,
    # have dependency (-1,+1), exponent sum zero, character holonomy -1.
    dependence = {0: Fraction(-1), 1: Fraction(1)}
    require(multiply_character([Fraction(-1), Fraction(1)], dependence) == -1,
            "the abstract parallel-character lemma changed")
    return {
        "finite_dag": (
            "a migration map strictly increasing in a finite target order "
            "has no closed chain"
        ),
        "closed_character_cycle": (
            "a cycle of equations chi(d_i)=r_i is inconsistent exactly when "
            "an integer zero-displacement dependency has product r_i^n_i "
            "different from 1"
        ),
        "parallel_collision": (
            "the same displacement assigned -1 and +1 has holonomy -1 and "
            "is a localized unit"
        ),
    }


def main():
    edges, outcomes, sources, translated = migration_edges()
    destination_histogram = Counter(
        tuple(edge["endpoint"]["target_label"][1])
        for edge in edges
        if edge["endpoint"]["type"] == "translated_one_class_unit"
    )
    require(destination_histogram == Counter({
        (0, 0, 2, 1, 0, 1): 1,
        (0, 0, 0, 2, 2, 2): 2,
        (0, 0, 2, 1, 2, 2): 2,
        (0, 0, 0, 2, 0, 1): 1,
        (0, 1, 2, 1, 0, 1): 2,
        (0, 1, 0, 1, 2, 2): 4,
        (0, 1, 0, 2, 0, 1): 2,
    }), "the translated-target palette changed")

    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "abstract_source_provenance_lemma": abstract_character_lemma(),
        "complete_singleton_migration_map": edges,
        "endpoint_histogram": dict(sorted(outcomes.items())),
        "source_target_words": [list(word) for word in sorted(sources)],
        "translated_target_words": [list(word)
                                    for word in sorted(translated)],
        "translated_target_histogram": [
            [list(word), count]
            for word, count in sorted(destination_histogram.items())
        ],
        "longest_migration_chain": 1,
        "coefficient_feasible_closed_cycles": 0,
        "verdict": (
            "all sixteen singleton contaminants of the twelve one-bad "
            "successor classes terminate algebraically: fourteen migrate "
            "strictly forward to a translated one-class target and two end "
            "in an exact parallel-character holonomy unit"
        ),
        "scope": (
            "the complete singleton-contaminant source map already frozen "
            "by the repair-mask theorem, considered only at Laurent-class "
            "and target-label level; double-cell tails and later classes "
            "outside this map are not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"target-migration DAG ledger changed: {digest}")

    print("N=8 one-bad target-migration DAG: PASS")
    print("singleton provenance edges: 16")
    print("endpoints: 14 translated targets + 2 parallel holonomy units")
    print("closed class cycles: 0 (longest chain 1)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
