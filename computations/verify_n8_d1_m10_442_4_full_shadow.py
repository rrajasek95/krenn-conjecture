#!/usr/bin/env python3
"""Exact complete 8,100-fibre shadow for the smallest m=10 survivor."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_INHERITANCE_SHA256 = (
    "a35a788a520b9a6e77fab81e1febc3ecfcd6c0a379eef4d419bf03e34160727d"
)
SOURCE = os.path.join(
    HERE, "verify_n8_d1_m10_remaining_core_inheritance.py"
)
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_INHERITANCE_SHA256,
            "the committed m=10 inheritance source changed")
I = importlib.import_module("verify_n8_d1_m10_remaining_core_inheritance")
A, C, V, N, D = I.A, I.C, I.V, I.N, I.D
M9 = A.M9

EXPECTED_GLOBAL_442_4 = (
    1080299, 4266956,
    "be2ac535904a94bfcac66f52d412401f9f4e74887844db6e27e02b416cd7b05c",
)
EXPECTED_LEDGER_SHA256 = (
    "dc0c9226c2ab5db5115a8e3258918c49957ff99a132e168dddc9f2c882fa7dac"
)


def target_branch():
    branches, admissible, sigma, off_sigma = I.surviving_branches()
    state = next(state for family, index, state in branches
                 if (family, index) == ("442", 4))
    require(state[1] == frozenset(),
            "the frozen 442:4 branch gained anchor units")
    return state, admissible, sigma, off_sigma


def build_full_shadow(state, admissible, sigma, off_sigma):
    base, anchor_units = state
    require(len(base) == 8 and not anchor_units and base <= off_sigma,
            "the frozen branch support changed")
    cnf = A.M8.CNF()
    free = sorted(off_sigma - set(base))
    sigma_ids = {entry: cnf.var(("SIGMA", entry))
                 for entry in sorted(sigma)}
    off_ids = {entry: cnf.var(("EXTRA", entry)) for entry in free}
    A.add_exact(cnf, [off_ids[entry] for entry in free], 2)
    mandatory = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    for entry in sorted(mandatory | set(anchor_units)):
        cnf.add(sigma_ids[entry])

    def matching_term(domain, values, word, matching):
        factors = []
        for u, v in matching:
            entry = V.cell(u, v, word[u], word[v])
            if entry not in admissible:
                return False
            if entry in base:
                continue
            factors.append(sigma_ids[entry] if entry in sigma
                           else off_ids[entry])
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
    require(fibre_count == 8100,
            "the complete support-shadow fibre count changed")
    return cnf


def frozen_input():
    state, admissible, sigma, off_sigma = target_branch()
    cnf = build_full_shadow(state, admissible, sigma, off_sigma)
    return state, cnf


def build_fixed_full_shadow(extras, anchor_units, admissible, sigma,
                            off_sigma, selected_fibres=None):
    """Specialize all ten off-Sigma choices before Tseitin expansion."""
    extras = set(extras)
    require(len(extras) == 10 and extras <= off_sigma,
            "a specialized m=10 support does not have ten cells")
    cnf = A.M8.CNF()
    sigma_ids = {entry: cnf.var(("SIGMA", entry))
                 for entry in sorted(sigma)}
    mandatory = set(V.BASE_UNITS) | set(anchor_units) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    for entry in sorted(mandatory):
        cnf.add(sigma_ids[entry])
    cnf.clause_fibres = [None] * len(cnf.clauses)

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
                factors.append(sigma_ids[entry])
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
            clause_start = len(cnf.clauses)
            word = dict(zip(domain, values))
            terms, constants = [], 0
            for matching in V.MATCHINGS[tuple(domain)]:
                term = matching_term(domain, values, word, matching)
                if term is True:
                    constants += 1
                elif term is not False:
                    terms.append(term)
            def record_fibre_clauses():
                cnf.clause_fibres.extend(
                    [fibre_key] * (len(cnf.clauses) - clause_start)
                )
            if pure:
                if constants == 0:
                    cnf.add(*terms)
                record_fibre_clauses()
                continue
            if constants >= 2:
                record_fibre_clauses()
                continue
            if constants == 1:
                cnf.add(*terms)
                record_fibre_clauses()
                continue
            if len(terms) == 1:
                cnf.add(-terms[0])
                record_fibre_clauses()
                continue
            if not terms:
                record_fibre_clauses()
                continue
            prefix, current = [None] * len(terms), None
            for index, term in enumerate(terms):
                prefix[index] = current
                current = cnf.or_var(current, term,
                                     ("PRE", fibre_key, index))
            suffix, current = [None] * len(terms), None
            for index in range(len(terms) - 1, -1, -1):
                suffix[index] = current
                current = cnf.or_var(current, terms[index],
                                     ("SUF", fibre_key, index))
            for index, term in enumerate(terms):
                clause = [-term]
                if prefix[index] is not None:
                    clause.append(prefix[index])
                if suffix[index] is not None:
                    clause.append(suffix[index])
                cnf.add(*clause)
            record_fibre_clauses()
    require(fibre_count == 8100,
            "the specialized support-shadow fibre count changed")
    require(len(cnf.clause_fibres) == len(cnf.clauses),
            "the specialized clause-to-fibre ledger changed")
    return cnf


def direct_unique_certificate(state, admissible, sigma):
    """Return one mixed fibre with exactly one mandatory live matching."""
    base, anchor_units = state
    mandatory = (set(V.BASE_UNITS) | set(base) | set(anchor_units)
                 | {V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2)})
    allowed = sigma | set(base)
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
                    if len(live) == 1 and set(live[0]) <= mandatory:
                        return {
                            "domain": list(domain),
                            "word": list(values),
                            "unique_matching": [list(entry)
                                                for entry in live[0]],
                        }
    return None


def choose_dynamic_repair(state, additions, admissible, sigma, off_sigma):
    """Return an immediate obstruction or the smallest live repair DNF.

    This is the streaming counterpart of M8.repair_certificates: it avoids
    retaining every certificate when the search recomputes them at thousands
    of partial supports.
    """
    base, anchor_units = state
    mandatory = (set(V.BASE_UNITS) | set(base) | set(anchor_units)
                 | {V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2)})
    allowed = sigma | set(base)
    seen_words = set()
    best = None
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
                    ordered = tuple(sorted(
                        repairs, key=lambda row: tuple(sorted(row))
                    ))
                    if not ordered:
                        return {"obstruction": word_key, "repair": None}
                    candidate = len(ordered), word_key, ordered
                    if best is None or candidate < best:
                        best = candidate
    if best is None:
        return None
    return {"obstruction": best[1], "repair": best[2]}


def direct_complete_support_certificate(state, admissible, sigma):
    """Check pure-empty first, then the mixed unique-matching obstruction."""
    base, _anchor_units = state
    allowed = sigma | set(base)
    pure_words = [
        (tuple(V.SITES), (colour,) * len(V.SITES))
        for colour in V.COLORS
    ] + [
        (tuple(domain), (2,) * len(domain))
        for domain in (V.W1, V.W2, V.RESIDUE)
    ]
    for domain, values in pure_words:
        word = dict(zip(domain, values))
        live = []
        for matching in V.MATCHINGS[domain]:
            cells = tuple(V.cell(u, v, word[u], word[v])
                          for u, v in matching)
            if all(entry in allowed for entry in cells):
                live.append(cells)
        if not live:
            return {
                "kind": "pure_empty",
                "domain": list(domain),
                "word": list(values),
            }
    mixed = direct_unique_certificate(state, admissible, sigma)
    if mixed is not None:
        return {"kind": "mixed_unique", **mixed}
    return None


def unit_refutation_core_fibres(cnf):
    """Extract the input-fibre dependency core of root unit propagation."""
    require(hasattr(cnf, "clause_fibres")
            and len(cnf.clause_fibres) == len(cnf.clauses),
            "a fixed-shadow CNF lacks its clause-fibre ledger")
    assignment, reason = {}, {}
    conflict = None
    progress = True
    while progress and conflict is None:
        progress = False
        for clause_index, clause in enumerate(cnf.clauses):
            if any(assignment.get(abs(literal)) == (literal > 0)
                   for literal in clause):
                continue
            unresolved = [literal for literal in clause
                          if abs(literal) not in assignment]
            if not unresolved:
                conflict = clause_index
                break
            if len(unresolved) == 1:
                literal = unresolved[0]
                variable = abs(literal)
                assignment[variable] = literal > 0
                reason[variable] = clause_index
                progress = True
    if conflict is None:
        return None
    core_clauses, stack = {conflict}, [conflict]
    while stack:
        clause_index = stack.pop()
        for literal in cnf.clauses[clause_index]:
            if assignment.get(abs(literal)) != (literal < 0):
                continue
            source = reason.get(abs(literal))
            if source is not None and source not in core_clauses:
                core_clauses.add(source)
                stack.append(source)
    fibres = frozenset(
        cnf.clause_fibres[index] for index in core_clauses
        if cnf.clause_fibres[index] is not None
    )
    return {
        "assigned_variables": len(assignment),
        "conflict_clause": conflict,
        "core_clauses": len(core_clauses),
        "fibres": fibres,
    }


def audit():
    started = monotonic()
    branches, admissible, sigma, off_sigma = I.surviving_branches()
    off_cells = sorted(off_sigma)
    cell_index = {entry: index for index, entry in enumerate(off_cells)}
    pair_branches = [(family, index, state)
                     for family, index, state in branches
                     if family == "442"]
    require(len(pair_branches) == 22,
            "the transferable 4+4+2 branch family changed")
    require({family for family, _index, _state in branches} - {"442"}
            == {"334", "343", "433"}
            and len(branches) - len(pair_branches) == 246,
            "the non-pair template partition changed")
    # Three 433 branches were closed after surviving_branches() was frozen.
    non_pair_open = [(family, index) for family, index, _state in branches
                     if family != "442"
                     and (family, index) not in {
                         ("433", 46), ("433", 47), ("433", 48),
                     }]
    require(len(non_pair_open) == 243,
            "the pre-transfer 265-branch frontier changed")

    branch_rows, full_rup_rows = [], []
    for family, index, state in pair_branches:
        candidates, initial, used, certificate_count = (
            M9.filter_additions_masked(
                state, 2, admissible, sigma, off_sigma,
                off_cells, cell_index,
            )
        )
        require(initial == 7140,
                "a 4+4 base no longer has 7,140 extra-cell pairs")
        direct_rows = []
        residual = []
        for mask in candidates:
            additions = M9.mask_entries(mask, off_cells)
            complete_state = (
                frozenset(set(state[0]) | set(additions)), state[1]
            )
            certificate = direct_unique_certificate(
                complete_state, admissible, sigma
            )
            if certificate is None:
                residual.append(additions)
            else:
                direct_rows.append({
                    "additions": [list(entry)
                                  for entry in sorted(additions)],
                    "certificate": certificate,
                })
        for additions in residual:
            full_support = set(state[0]) | set(additions)
            cnf = build_fixed_full_shadow(
                full_support, state[1], admissible, sigma, off_sigma
            )
            refutation = A.M8.unit_refutation(cnf.clauses)
            require(refutation is not None,
                    "a residual complete 8,100-fibre shadow survived")
            steps, conflict_clause = refutation
            full_rup_rows.append({
                "branch": index,
                "additions": [list(entry) for entry in sorted(additions)],
                "variables": cnf.variable_count,
                "clauses": len(cnf.clauses),
                "dimacs_sha256": hashlib.sha256(
                    A.dimacs_bytes(cnf)
                ).hexdigest(),
                "unit_RUP_steps": steps,
                "conflict_clause": conflict_clause,
            })
        branch_rows.append({
            "branch": index,
            "anchor_units": len(state[1]),
            "raw_pairs": initial,
            "repair_certificates": certificate_count,
            "effective_repair_certificates": used,
            "repair_survivors": len(candidates),
            "direct_unique_closures": len(direct_rows),
            "direct_certificate_sha256": D.content_hash(direct_rows),
            "complete_shadow_unit_RUP_closures": len(residual),
        })

    require(sum(row["raw_pairs"] for row in branch_rows) == 157080
            and sum(row["repair_survivors"] for row in branch_rows) == 28879
            and sum(row["direct_unique_closures"]
                    for row in branch_rows) == 28868
            and len(full_rup_rows) == 11,
            "the complete 4+4+2 transfer census changed")
    target = next(row for row in branch_rows if row["branch"] == 4)
    require(target["repair_survivors"] == 36
            and target["direct_unique_closures"] == 36,
            "the frozen 442:4 complete-shadow certificate changed")
    ledger = {
        "pinned_inheritance_sha256": PINNED_INHERITANCE_SHA256,
        "pre_transfer_symbolic_branches": 265,
        "template_partition": {
            "4+4+2_pair_branches": len(pair_branches),
            "different_cardinality_nonmatches": len(non_pair_open),
        },
        "complete_fibres_per_fixed_support": 8100,
        "raw_extra_pairs": 157080,
        "repair_filtered_pairs": 28879,
        "direct_unique_fibre_closures": 28868,
        "complete_shadow_unit_RUP_closures": len(full_rup_rows),
        "branch_rows": branch_rows,
        "full_RUP_rows": full_rup_rows,
        "closed_4+4+2_branches": len(pair_branches),
        "remaining_symbolic_branches": len(non_pair_open),
        "status": ("the complete 4+4+2 m=10 family is empty; "
                   "m=10 remains open only in 3+3+4, 3+4+3, and 4+3+3"),
    }
    digest = D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "the complete 4+4+2 shadow ledger changed")
    return ledger, digest, monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-global-442-4", action="store_true")
    args = parser.parse_args()
    ledger, digest, seconds = audit()
    if args.build_global_442_4:
        _state, cnf = frozen_input()
        global_row = (cnf.variable_count, len(cnf.clauses),
                      hashlib.sha256(A.dimacs_bytes(cnf)).hexdigest())
        require(global_row == EXPECTED_GLOBAL_442_4,
                "the monolithic global 442:4 input changed")
        print("global 442:4 CNF: %d variables; %d clauses; sha256 %s"
              % global_row)
    print("n8 D1 m=10 complete 4+4+2 shadow: PASS (exact)")
    print("442:4: 7,140 pairs -> 36 -> 0")
    print("transfer: 22/22 remaining 4+4+2 branches closed")
    print("fixed supports: 28,868 direct unique; 11 unit-RUP")
    print("remaining m=10 symbolic branches: 243")
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
