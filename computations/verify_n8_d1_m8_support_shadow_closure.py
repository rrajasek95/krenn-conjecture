#!/usr/bin/env python3
"""Exact support-shadow closure of the N=8 D1 eight-cell frontier.

This checker is solver-free.  It exhaustively classifies the one-colour
monochromatic anchors, quotients the resulting two-colour branch states by
the D1 group, applies exact unique-fibre repair certificates, and finally
unit-refutes the remaining fixed-support shadows.
"""

from __future__ import annotations

import hashlib
import importlib
import itertools
import math
import os
import sys
from collections import Counter
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_M7_SHA256 = (
    "980c56dce8c6dc9e295d4fc9752e30938911e3c018ffc15ae3f33c619710d3e3"
)
M7_PATH = os.path.join(HERE, "verify_n8_d1_m7_support_shadow_closure.py")
with open(M7_PATH, "rb") as handle:
    M7_SHA256 = hashlib.sha256(handle.read()).hexdigest()
require(M7_SHA256 == PINNED_M7_SHA256,
        "the committed m=7 support-shadow source changed")
M7 = importlib.import_module("verify_n8_d1_m7_support_shadow_closure")
N = M7.N
V = N.V
D = V.D

EXPECTED_LEDGER_SHA256 = (
    "78204953d39924fe3bc46d405a577613e7901e022a29e91150ca4d5dd767ee19"
)


def map_set(values, mapping):
    return frozenset(V.map_cell(entry, mapping) for entry in values)


def state_key(state):
    return tuple(sorted(state[0])), tuple(sorted(state[1]))


def map_state(state, mapping):
    return map_set(state[0], mapping), map_set(state[1], mapping)


def state_pair_orbits(first_states, second_states, group):
    states = {
        (first[0] | second[0], first[1] | second[1])
        for first in first_states for second in second_states
    }
    labelled = len(states)
    representatives = []
    while states:
        seed = min(states, key=state_key)
        orbit = {map_state(seed, mapping) for mapping in group}
        states -= orbit
        representatives.append(seed)
    representatives.sort(key=state_key)
    return labelled, representatives


def monochrome_normal_forms(colour, off_sigma):
    monochrome = sorted(entry for entry in off_sigma
                        if entry[2:] == (colour, colour))
    require(len(monochrome) == 22,
            "a colour no longer has 22 off-Sigma monochrome cells")
    full_traces = {
        frozenset(V.cell(u, v, colour, colour) for u, v in matching
                  if V.cell(u, v, colour, colour) in off_sigma)
        for matching in V.MATCHINGS[V.SITES]
    }
    residue_matchings = {
        frozenset(V.cell(u, v, colour, colour) for u, v in matching)
        for matching in V.MATCHINGS[V.RESIDUE]
    }
    valid = {}
    for size in range(2, 6):
        supports = set()
        for chosen in itertools.combinations(monochrome, size):
            support = frozenset(chosen)
            if not any(trace <= support for trace in full_traces):
                continue
            if sum(matching <= support
                   for matching in residue_matchings) == 1:
                continue
            supports.add(support)
        valid[size] = supports
    require({size: len(rows) for size, rows in valid.items()}
            == {2: 0, 3: 72, 4: 1179, 5: 8382},
            "the one-colour support census changed")
    minimal_three = valid[3]
    minimal_four = {
        support for support in valid[4]
        if not any(smaller <= support for smaller in minimal_three)
    }
    minimal_five = {
        support for support in valid[5]
        if not any(smaller <= support
                   for smaller in minimal_three | minimal_four)
    }
    triple_supports = {state[0] for state in N.triple_states(colour)}
    special_four_supports = {
        state[0] for state in N.special_four_supports(colour)[0]
    }
    require(minimal_three == triple_supports
            and minimal_four == special_four_supports
            and len(minimal_four) == 27 and not minimal_five,
            "the 3/4 anchor normal forms are not exhaustive through size 5")
    return {
        "off_monochrome_cells": len(monochrome),
        "valid_by_size": {size: len(rows)
                          for size, rows in sorted(valid.items())},
        "minimal_three": len(minimal_three),
        "minimal_four": len(minimal_four),
        "minimal_five": len(minimal_five),
    }


def repair_certificates(state, additions, admissible, sigma, off_sigma):
    """Necessary extra-cell conditions from currently unique live fibres."""
    base, anchor_units = state
    mandatory = (set(V.BASE_UNITS) | set(base) | set(anchor_units)
                 | {V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2)})
    allowed = sigma | set(base)
    certificates = []
    seen_words = set()
    for domain in (V.RESIDUE, V.W1, V.W2, V.SITES):
        for matching in V.MATCHINGS[tuple(domain)]:
            choices = []
            for u, v in matching:
                on_edge = sorted(entry for entry in mandatory
                                 if entry[:2] == (u, v))
                if not on_edge:
                    break
                choices.append(on_edge)
            else:
                for selected in itertools.product(*choices):
                    word = {}
                    for u, v, i, j in selected:
                        word[u], word[v] = i, j
                    values = tuple(word[site] for site in domain)
                    word_key = tuple(domain), values
                    if word_key in seen_words:
                        continue
                    seen_words.add(word_key)
                    pure = (len(set(values)) == 1
                            if domain == V.SITES else set(values) == {2})
                    if pure:
                        continue
                    live = []
                    for other in V.MATCHINGS[tuple(domain)]:
                        cells = tuple(V.cell(u, v, word[u], word[v])
                                      for u, v in other)
                        if all(entry in allowed for entry in cells):
                            live.append(cells)
                    if len(live) != 1 or not set(live[0]) <= mandatory:
                        continue
                    repairs = set()
                    for other in V.MATCHINGS[tuple(domain)]:
                        cells = tuple(V.cell(u, v, word[u], word[v])
                                      for u, v in other)
                        if not all(entry in admissible for entry in cells):
                            continue
                        missing = frozenset(
                            entry for entry in cells
                            if entry in off_sigma and entry not in base
                        )
                        if missing and len(missing) <= additions:
                            repairs.add(missing)
                    repairs = {
                        repair for repair in repairs
                        if not any(smaller < repair for smaller in repairs)
                    }
                    certificates.append((word_key, tuple(sorted(
                        repairs, key=lambda row: tuple(sorted(row))
                    ))))
    return certificates


def filter_additions(state, additions, admissible, sigma, off_sigma):
    base, _units = state
    candidates = [
        frozenset(chosen)
        for chosen in itertools.combinations(sorted(off_sigma - set(base)),
                                               additions)
    ]
    certificates = repair_certificates(
        state, additions, admissible, sigma, off_sigma
    )
    used = []
    while candidates:
        choices = []
        for index, (word_key, repairs) in enumerate(certificates):
            survivors = [
                candidate for candidate in candidates
                if any(repair <= candidate for repair in repairs)
            ]
            if len(survivors) < len(candidates):
                choices.append((len(survivors), word_key, index, survivors))
        if not choices:
            break
        remaining, word_key, index, candidates = min(
            choices, key=lambda row: (row[0], row[1], row[2])
        )
        used.append({"domain": len(word_key[0]),
                     "word": list(word_key[1]),
                     "repair_terms": len(certificates[index][1]),
                     "remaining": remaining})
    return candidates, used, len(certificates)


class CNF:
    def __init__(self):
        self.ids = {}
        self.variable_count = 0
        self.clauses = []
        self.and_cache = {}

    def var(self, key):
        if key not in self.ids:
            self.variable_count += 1
            self.ids[key] = self.variable_count
        return self.ids[key]

    def add(self, *literals):
        self.clauses.append(tuple(literals))

    def and_var(self, inputs, key):
        inputs = tuple(sorted(set(inputs)))
        if not inputs:
            return True
        if len(inputs) == 1:
            return inputs[0]
        cache_key = ("AND", inputs)
        if cache_key in self.and_cache:
            return self.and_cache[cache_key]
        output = self.var(key)
        self.and_cache[cache_key] = output
        for value in inputs:
            self.add(-output, value)
        self.add(output, *(-value for value in inputs))
        return output

    def or_var(self, left, right, key):
        if left is None:
            return right
        if right is None:
            return left
        output = self.var(key)
        self.add(-left, output)
        self.add(-right, output)
        self.add(-output, left, right)
        return output


def build_fixed_support_shadow(extras, admissible, sigma, off_sigma,
                               selected_fibres=None):
    extras = set(extras)
    require(len(extras) == 8 and extras <= off_sigma,
            "a residual support is not an eight-cell off-Sigma support")
    cnf = CNF()
    cell_ids = {entry: cnf.var(("CELL", entry)) for entry in sorted(sigma)}
    mandatory = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    for entry in sorted(mandatory):
        cnf.add(cell_ids[entry])

    def matching_term(domain, values, word, matching):
        factors = []
        for u, v in matching:
            entry = V.cell(u, v, word[u], word[v])
            if entry not in admissible:
                return False
            if entry in off_sigma:
                if entry not in extras:
                    return False
            else:
                factors.append(cell_ids[entry])
        return cnf.and_var(
            factors, ("TERM", tuple(domain), tuple(values), tuple(matching))
        )

    fibre_count = 0
    for domain in (V.SITES, V.W1, V.W2, V.RESIDUE):
        for values in itertools.product(V.COLORS, repeat=len(domain)):
            pure = (len(set(values)) == 1
                    if domain == V.SITES else set(values) == {2})
            fibre_key = tuple(domain), tuple(values), pure
            fibre_count += 1
            if (selected_fibres is not None
                    and fibre_key not in selected_fibres):
                continue
            word = dict(zip(domain, values))
            terms, constants = [], 0
            for matching in V.MATCHINGS[tuple(domain)]:
                term = matching_term(domain, values, word, matching)
                if term is True:
                    constants += 1
                elif term is not False:
                    terms.append(term)
            if pure:
                if constants == 0:
                    cnf.add(*terms)
                continue
            if constants >= 2:
                continue
            if constants == 1:
                cnf.add(*terms)
                continue
            if len(terms) == 1:
                cnf.add(-terms[0])
                continue
            if not terms:
                continue
            prefix, current = [None] * len(terms), None
            for index, term in enumerate(terms):
                prefix[index] = current
                current = cnf.or_var(
                    current, term, ("PRE", fibre_key, index)
                )
            suffix, current = [None] * len(terms), None
            for index in range(len(terms) - 1, -1, -1):
                suffix[index] = current
                current = cnf.or_var(
                    current, terms[index], ("SUF", fibre_key, index)
                )
            for index, term in enumerate(terms):
                clause = [-term]
                if prefix[index] is not None:
                    clause.append(prefix[index])
                if suffix[index] is not None:
                    clause.append(suffix[index])
                cnf.add(*clause)
    require(fibre_count == 8100, "the support-shadow fibre domain changed")
    return cnf


def unit_refutation(clauses):
    assignment = {}
    steps = 0
    while True:
        progress = False
        for clause_index, clause in enumerate(clauses):
            unresolved = []
            satisfied = False
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    unresolved.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unresolved:
                return steps, clause_index
            if len(unresolved) == 1:
                literal = unresolved[0]
                variable, value = abs(literal), literal > 0
                old = assignment.get(variable)
                if old is None:
                    assignment[variable] = value
                    steps += 1
                    progress = True
                else:
                    require(old == value,
                            "unit propagation assigned both polarities")
        if not progress:
            return None


def canonical_support(support, group):
    return min(tuple(sorted(map_set(support, mapping))) for mapping in group)


def audit():
    started = monotonic()
    admissible, sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    group = V.d1_group()
    normal_forms = {
        "b": monochrome_normal_forms(0, off_sigma),
        "c": monochrome_normal_forms(1, off_sigma),
    }
    triples = [N.triple_states(colour) for colour in (0, 1)]
    special = [N.special_four_supports(colour)[0] for colour in (0, 1)]
    families = (
        ("3+3+2", triples[0], triples[1], 2, 5184, 132),
        ("3+4+1", triples[0], special[1], 1, 2376, 64),
        ("4+3+1", special[0], triples[1], 1, 2376, 64),
        ("4+4", special[0], special[1], 0, 1089, 52),
    )
    base_units = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    family_rows = {}
    direct_kills = Counter()
    residual_states = []
    for name, first, second, additions, expected_labelled, expected_orbits in families:
        labelled, representatives = state_pair_orbits(first, second, group)
        require((labelled, len(representatives))
                == (expected_labelled, expected_orbits),
                "the %s anchor-state quotient changed" % name)
        after_repairs = 0
        before_repairs = 0
        exact_kills = Counter()
        residual = 0
        repair_depths = Counter()
        for state in representatives:
            before_repairs += math.comb(
                len(off_sigma) - len(state[0]), additions
            )
            candidates, used, _certificate_count = filter_additions(
                state, additions, admissible, sigma, off_sigma
            )
            after_repairs += len(candidates)
            repair_depths[len(used)] += 1
            for extra in candidates:
                final_state = state[0] | extra, state[1]
                certificate = N.unique_certificate(
                    final_state, sigma, base_units
                )
                if certificate is None:
                    residual_states.append(final_state)
                    residual += 1
                else:
                    exact_kills[certificate["domain"]] += 1
                    direct_kills[certificate["domain"]] += 1
        family_rows[name] = {
            "labelled_anchor_states": labelled,
            "anchor_state_orbits": len(representatives),
            "addition_choices_before_repair_constraints": before_repairs,
            "addition_choices_after_repair_constraints": after_repairs,
            "exact_unique_fibre_kills": dict(sorted(exact_kills.items())),
            "residual_branch_candidates": residual,
            "repair_depth_histogram": dict(sorted(repair_depths.items())),
        }
    require(sum(row["addition_choices_after_repair_constraints"]
                for row in family_rows.values()) == 9891,
            "the repair-filtered m=8 branch census changed")
    require(sum(row["addition_choices_before_repair_constraints"]
                for row in family_rows.values()) == 989832,
            "the unfiltered m=8 branch census changed")
    require(direct_kills == {4: 3399, 6: 3749, 8: 2503}
            and len(residual_states) == 240,
            "the exact m=8 unique-fibre census changed")
    residual_supports = sorted({
        canonical_support(state[0], group) for state in residual_states
    })
    require(len(residual_supports) == 165,
            "the residual m=8 supports no longer form 165 orbits")

    compact_fibres = {
        (tuple(V.SITES), tuple(word), len(set(word)) == 1)
        for core in M7.CORE_WORDS for word in core
    }
    require(len(compact_fibres) == 78,
            "the inherited m=7 compact fibre palette changed")
    shadow_tally = Counter()
    shadow_rows = []
    for index, support in enumerate(residual_supports):
        compact = build_fixed_support_shadow(
            support, admissible, sigma, off_sigma, compact_fibres
        )
        refutation = unit_refutation(compact.clauses)
        if refutation is not None:
            steps, conflict = refutation
            mode, cnf = "m7_palette", compact
        else:
            cnf = build_fixed_support_shadow(
                support, admissible, sigma, off_sigma, None
            )
            refutation = unit_refutation(cnf.clauses)
            require(refutation is not None,
                    "a residual complete support shadow was not refuted")
            steps, conflict = refutation
            mode = "complete_8100_fibres"
        shadow_tally[mode] += 1
        shadow_rows.append({
            "support_index": index,
            "support": [list(entry) for entry in support],
            "certificate": mode,
            "variables": cnf.variable_count,
            "clauses": len(cnf.clauses),
            "unit_steps": steps,
            "conflict_clause": conflict,
        })
    require(shadow_tally == {"m7_palette": 123,
                             "complete_8100_fibres": 42},
            "the m=8 support-shadow RUP census changed")
    ledger = {
        "pinned_m7_sha256": M7_SHA256,
        "normal_forms": normal_forms,
        "families": family_rows,
        "anchor_state_orbits": sum(
            row["anchor_state_orbits"] for row in family_rows.values()
        ),
        "direct_unique_kills_by_domain": dict(sorted(direct_kills.items())),
        "residual_branch_candidates": len(residual_states),
        "residual_support_orbits": len(residual_supports),
        "support_shadow_RUP": dict(sorted(shadow_tally.items())),
        "shadow_rows": shadow_rows,
        "status": ("all D1 supports with exactly eight nonzero off-Sigma "
                   "cells are impossible; D1 requires m >= 9"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the m=8 support-shadow closure ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 m=8 support-shadow closure: PASS (exact)")
    print("anchor-state orbits:", ledger["anchor_state_orbits"])
    print("branch choices: 989832 -> 9891 by repair certificates")
    print("exact unique-fibre kills: 9651")
    print("residual: %d branch candidates over %d support orbits"
          % (ledger["residual_branch_candidates"],
             ledger["residual_support_orbits"]))
    print("support-shadow RUP:", ledger["support_shadow_RUP"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
