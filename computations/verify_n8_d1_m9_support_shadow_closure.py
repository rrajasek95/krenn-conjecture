#!/usr/bin/env python3
"""Exact support-shadow closure of the N=8 D1 nine-cell frontier."""

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


PINNED_M8_SHA256 = (
    "198119a797af7516cce6994e4d8672bc6b0849a72b911f3b31f727570382326e"
)
M8_PATH = os.path.join(HERE, "verify_n8_d1_m8_support_shadow_closure.py")
with open(M8_PATH, "rb") as handle:
    M8_SHA256 = hashlib.sha256(handle.read()).hexdigest()
require(M8_SHA256 == PINNED_M8_SHA256,
        "the committed m=8 support-shadow source changed")
M8 = importlib.import_module("verify_n8_d1_m8_support_shadow_closure")
M7 = M8.M7
N = M8.N
V = M8.V
D = M8.D

EXPECTED_LEDGER_SHA256 = (
    "a57e3f9dc2d826b30190897c3cf6c1e84298f2ae47805e6a6fc9cc4a975f5811"
)


def monochrome_normal_forms_through_six(colour, off_sigma):
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
    valid, minimal = {}, {}
    for size in range(2, 7):
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
        minimal[size] = {
            support for support in supports
            if not any(smaller <= support
                       for earlier in range(2, size)
                       for smaller in minimal[earlier])
        }
    require({size: len(rows) for size, rows in valid.items()}
            == {2: 0, 3: 72, 4: 1179, 5: 8382, 6: 34657},
            "the one-colour support census through size six changed")
    require({size: len(rows) for size, rows in minimal.items()}
            == {2: 0, 3: 72, 4: 27, 5: 0, 6: 0},
            "a new minimal monochrome normal form appeared")
    require(minimal[3] == {state[0] for state in N.triple_states(colour)}
            and minimal[4] == {
                state[0] for state in N.special_four_supports(colour)[0]
            }, "the constructive 3/4 normal forms are incomplete")
    return {
        "off_monochrome_cells": len(monochrome),
        "valid_by_size": {size: len(rows)
                          for size, rows in sorted(valid.items())},
        "minimal_by_size": {size: len(rows)
                            for size, rows in sorted(minimal.items())},
    }


def mask_for(entries, cell_index):
    return sum(1 << cell_index[entry] for entry in entries)


def filter_additions_masked(state, additions, admissible, sigma, off_sigma,
                            off_cells, cell_index):
    """Intersect every exact repair condition using 128-bit support masks."""
    base, _units = state
    free_indices = [cell_index[entry]
                    for entry in off_cells if entry not in base]
    candidates = [sum(1 << index for index in selected)
                  for selected in itertools.combinations(free_indices,
                                                         additions)]
    initial = len(candidates)
    certificates = M8.repair_certificates(
        state, additions, admissible, sigma, off_sigma
    )
    used = 0
    for _word_key, repairs in certificates:
        repair_masks = [mask_for(repair, cell_index) for repair in repairs]
        survivors = [
            candidate for candidate in candidates
            if any(candidate & repair == repair for repair in repair_masks)
        ]
        if len(survivors) < len(candidates):
            used += 1
            candidates = survivors
        if not candidates:
            break
    return candidates, initial, used, len(certificates)


def mask_entries(mask, off_cells):
    return frozenset(entry for index, entry in enumerate(off_cells)
                     if mask & (1 << index))


def canonical_state(state, group):
    return min(M8.state_key(M8.map_state(state, mapping))
               for mapping in group)


def build_fixed_support_shadow(extras, admissible, sigma, off_sigma,
                               selected_fibres=None):
    """The exact m=8 builder specialized only by support cardinality."""
    extras = set(extras)
    require(len(extras) == 9 and extras <= off_sigma,
            "a residual support is not a nine-cell off-Sigma support")
    cnf = M8.CNF()
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


def audit():
    started = monotonic()
    admissible, sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    off_cells = sorted(off_sigma)
    cell_index = {entry: index for index, entry in enumerate(off_cells)}
    require(len(off_cells) == 128, "the off-Sigma domain changed")
    group = V.d1_group()
    normal_forms = {
        "b": monochrome_normal_forms_through_six(0, off_sigma),
        "c": monochrome_normal_forms_through_six(1, off_sigma),
    }
    triples = [N.triple_states(colour) for colour in (0, 1)]
    special = [N.special_four_supports(colour)[0] for colour in (0, 1)]
    families = (
        ("3+3+3", triples[0], triples[1], 3, 5184, 132,
         38971680, 415862, 934),
        ("3+4+2", triples[0], special[1], 2, 2376, 64,
         464640, 33530, 441),
        ("4+3+2", special[0], triples[1], 2, 2376, 64,
         464640, 33530, 385),
        ("4+4+1", special[0], special[1], 1, 1089, 52,
         6240, 480, 0),
    )
    base_units = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    family_rows = {}
    direct_kills = Counter()
    residual_states = []
    for (name, first, second, additions, expected_labelled,
         expected_orbits, expected_raw, expected_filtered,
         expected_residual) in families:
        labelled, representatives = M8.state_pair_orbits(
            first, second, group
        )
        require((labelled, len(representatives))
                == (expected_labelled, expected_orbits),
                "the %s anchor-state quotient changed" % name)
        raw, filtered = 0, 0
        exact_kills = Counter()
        residual = 0
        repair_depths = Counter()
        for state in representatives:
            candidates, initial, used, _certificate_count = (
                filter_additions_masked(
                    state, additions, admissible, sigma, off_sigma,
                    off_cells, cell_index
                )
            )
            raw += initial
            filtered += len(candidates)
            repair_depths[used] += 1
            for candidate in candidates:
                extra = mask_entries(candidate, off_cells)
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
        require((raw, filtered, residual)
                == (expected_raw, expected_filtered, expected_residual),
                "the %s repair/unique census changed" % name)
        family_rows[name] = {
            "labelled_anchor_states": labelled,
            "anchor_state_orbits": len(representatives),
            "addition_choices_before_repairs": raw,
            "addition_choices_after_repairs": filtered,
            "exact_unique_fibre_kills": dict(sorted(exact_kills.items())),
            "residual_branch_candidates": residual,
            "repair_depth_histogram": dict(sorted(repair_depths.items())),
        }
    require(sum(row["addition_choices_before_repairs"]
                for row in family_rows.values()) == 39907200
            and sum(row["addition_choices_after_repairs"]
                    for row in family_rows.values()) == 483402,
            "the aggregate m=9 repair census changed")
    require(direct_kills == {4: 235008, 6: 185187, 8: 61447}
            and len(residual_states) == 1760,
            "the aggregate m=9 exact unique-fibre census changed")
    residual_state_orbits = {
        canonical_state(state, group) for state in residual_states
    }
    residual_supports = sorted({
        M8.canonical_support(state[0], group) for state in residual_states
    })
    require(len(residual_state_orbits) == 1315
            and len(residual_supports) == 1071,
            "the residual m=9 orbit quotient changed")

    compact_fibres = {
        (tuple(V.SITES), tuple(word), len(set(word)) == 1)
        for core in M7.CORE_WORDS for word in core
    }
    require(len(compact_fibres) == 78,
            "the inherited compact fibre palette changed")
    shadow_tally = Counter()
    shadow_rows = []
    for index, support in enumerate(residual_supports):
        compact = build_fixed_support_shadow(
            support, admissible, sigma, off_sigma, compact_fibres
        )
        refutation = M8.unit_refutation(compact.clauses)
        if refutation is not None:
            steps, conflict = refutation
            mode, cnf = "m7_palette", compact
        else:
            cnf = build_fixed_support_shadow(
                support, admissible, sigma, off_sigma, None
            )
            refutation = M8.unit_refutation(cnf.clauses)
            require(refutation is not None,
                    "a residual complete m=9 shadow was not refuted")
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
    require(shadow_tally == {"m7_palette": 442,
                             "complete_8100_fibres": 629},
            "the m=9 support-shadow RUP census changed")
    ledger = {
        "pinned_m8_sha256": M8_SHA256,
        "normal_forms": normal_forms,
        "families": family_rows,
        "anchor_state_orbits": sum(
            row["anchor_state_orbits"] for row in family_rows.values()
        ),
        "direct_unique_kills_by_domain": dict(sorted(direct_kills.items())),
        "residual_branch_candidates": len(residual_states),
        "residual_state_orbits": len(residual_state_orbits),
        "residual_support_orbits": len(residual_supports),
        "support_shadow_RUP": dict(sorted(shadow_tally.items())),
        "shadow_rows": shadow_rows,
        "status": ("all D1 supports with exactly nine nonzero off-Sigma "
                   "cells are impossible; D1 requires m >= 10"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the m=9 support-shadow closure ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 m=9 support-shadow closure: PASS (exact)")
    print("anchor-state orbits:", ledger["anchor_state_orbits"])
    print("branch choices: 39907200 -> 483402 by repair certificates")
    print("exact unique-fibre kills: 481642")
    print("residual: %d branches, %d state orbits, %d support orbits"
          % (ledger["residual_branch_candidates"],
             ledger["residual_state_orbits"],
             ledger["residual_support_orbits"]))
    print("support-shadow RUP:", ledger["support_shadow_RUP"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
