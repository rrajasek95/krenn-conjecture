#!/usr/bin/env python3
"""Close the 22 N=8 D1 m=7 support orbits by exact RUP cores.

The preceding anchor-normal-form audit reduces every seven-cell off-Sigma
support to 22 representatives.  For each representative this checker freezes
a small set of full eight-site fibres.  It reconstructs their Boolean support
shadow directly from matchings and verifies, without a SAT dependency, that
unit propagation derives a contradiction.  Thus the empty clause is RUP for
each frozen core.
"""

from __future__ import annotations

import hashlib
import importlib
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


PINNED_NORMAL_FORM_SHA256 = (
    "d47324308b9df4f3b8c6348bfd1cf23b6c08bbde6d65e468524d4906f328d21b"
)
NORMAL_FORM_PATH = os.path.join(
    HERE, "verify_n8_d1_m7_anchor_normal_form_cover.py"
)
with open(NORMAL_FORM_PATH, "rb") as handle:
    NORMAL_FORM_SHA256 = hashlib.sha256(handle.read()).hexdigest()
require(NORMAL_FORM_SHA256 == PINNED_NORMAL_FORM_SHA256,
        "the committed m=7 normal-form source changed")
N = importlib.import_module("verify_n8_d1_m7_anchor_normal_form_cover")
V = N.V
D = V.D


# Each row is a fibre core for the correspondingly sorted survivor support.
# A word is ordered on sites 0,...,7.  A monochrome word is target-pure and
# must have a supported matching; every other word is target-zero and may not
# have exactly one supported matching.
CORE_WORDS = (
    ((0,0,0,0,0,2,0,0),(0,0,0,0,2,2,0,0),(0,0,0,1,0,2,2,0),(0,0,1,0,1,2,0,1),(0,1,0,1,0,0,1,0),(0,1,0,1,0,2,1,0),(0,1,1,1,0,2,1,2),(0,1,1,1,1,2,1,1),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,0,0,0),(0,0,0,0,0,0,2,2),(0,0,0,0,1,0,1,2),(0,0,0,0,1,0,2,1),(0,0,1,0,0,0,0,0),(0,0,1,0,1,0,1,2),(0,0,1,0,1,0,2,1),(0,2,0,2,0,1,1,2),(0,2,0,2,0,1,2,1),(0,2,1,2,0,1,1,2),(0,2,1,2,0,1,2,1),(0,2,1,2,1,2,1,2),(0,2,1,2,1,2,2,1),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,1,2,0,0),(0,0,0,0,2,2,0,0),(0,0,0,1,1,2,2,0),(0,0,1,0,1,2,0,1),(0,1,0,1,0,0,1,0),(0,1,0,1,1,2,1,0),(0,1,1,1,1,2,1,1),(0,1,1,1,1,2,1,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,2,2,0,0),(1,0,0,0,0,2,0,0),(1,0,0,0,2,1,0,0),(1,0,0,1,0,2,2,0),(1,0,0,1,2,1,2,0),(1,1,0,1,0,2,1,0),(1,1,0,1,2,1,1,0),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,2,2,0,0),(1,0,0,0,1,2,0,0),(1,0,0,0,2,1,0,0),(1,0,0,1,1,2,2,0),(1,0,0,1,2,1,2,0),(1,1,0,1,1,2,1,0),(1,1,0,1,2,1,1,0),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,0,0,2,2,0),(0,0,0,1,0,0,0,2),(0,1,0,0,0,1,0,2),(0,1,0,0,0,1,2,0),(0,1,0,1,0,1,1,1),(0,2,0,2,0,2,1,1),(1,1,1,0,1,1,0,2),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,0,0,2,2,1),(0,0,0,1,0,0,2,0),(0,1,0,0,0,1,0,2),(0,1,0,0,0,1,2,1),(0,1,0,1,0,1,1,1),(0,2,0,2,0,2,1,1),(1,1,1,0,1,1,2,1),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,0,2,0),(0,0,0,1,0,2,2,0),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,0,1,0,1,2,0),(0,2,0,2,0,2,1,1),(1,1,1,1,1,1,2,0),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,0,2,0),(0,0,0,1,0,2,2,1),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,0,1,0,1,2,1),(0,2,0,2,0,2,1,1),(1,1,1,1,1,1,2,1),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,0,2,0),(0,0,0,2,0,2,2,0),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,0,2,0,1,2,0),(0,2,0,2,0,2,1,1),(1,1,1,1,1,1,2,2),(1,1,1,2,1,1,2,0),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,0,2,0),(0,0,0,2,0,2,2,1),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,0,2,0,1,2,1),(0,2,0,2,0,2,1,1),(1,1,1,1,1,1,2,2),(1,1,1,2,1,1,2,1),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,0,0,2),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,1,0,2,1,0,2),(0,2,0,2,0,2,1,1),(1,1,1,0,1,1,0,2),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,0,1,2),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,1,0,2,1,0,2),(0,2,0,2,0,2,1,1),(1,1,1,0,1,1,0,2),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,0,2,2),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,1,0,2,1,0,2),(0,2,0,2,0,2,1,1),(1,1,1,0,1,1,0,2),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,1,0,2),(0,1,0,1,0,1,1,1),(0,2,0,2,0,1,0,2),(0,2,0,2,0,2,1,1),(0,2,1,2,2,1,0,2),(1,1,1,1,1,1,2,2),(1,2,1,2,1,1,0,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,1,1,2),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,1,0,2,1,0,2),(0,2,0,2,0,2,1,1),(1,1,1,0,1,1,0,2),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,1,0,0,0,1,0,2),(0,1,1,0,2,1,0,2),(0,2,0,2,0,2,1,1),(0,2,1,2,2,2,1,1),(1,1,1,0,1,1,0,2),(1,2,1,2,1,2,1,1),(2,2,2,2,2,2,2,2)),
    ((0,1,0,0,0,1,0,2),(0,1,1,0,2,1,0,2),(0,2,0,2,0,0,2,0),(0,2,1,2,2,0,2,0),(1,1,1,0,1,1,0,2),(1,1,1,1,1,1,2,2),(1,2,1,2,1,0,2,0),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,2,0,2),(0,0,0,1,0,2,1,2),(0,1,0,0,0,1,0,2),(0,1,0,1,0,1,1,1),(0,1,1,0,2,1,0,2),(0,2,0,2,0,2,1,1),(1,1,1,0,1,1,0,2),(1,1,1,1,1,1,2,2),(2,2,2,2,2,2,2,2)),
    ((0,2,1,2,0,2,0,2),(0,2,1,2,0,2,2,0),(1,1,1,1,1,1,2,2),(1,2,1,2,1,0,0,2),(1,2,1,2,1,0,2,0),(1,2,1,2,1,2,1,1),(2,2,2,2,2,2,2,2)),
    ((0,2,1,2,0,2,0,2),(0,2,1,2,0,2,2,0),(1,1,1,1,1,1,1,1),(1,1,1,1,1,1,2,2),(1,2,1,2,1,0,0,2),(1,2,1,2,1,0,2,0),(1,2,1,2,1,2,1,1),(2,2,2,2,2,2,2,2)),
    ((0,0,0,0,0,0,2,2),(0,2,0,2,0,1,1,2),(0,2,0,2,0,1,2,1),(0,2,0,2,0,2,0,0),(0,2,1,2,1,2,1,2),(0,2,1,2,1,2,2,1),(2,2,2,2,2,2,2,2)),
)

EXPECTED_LEDGER_SHA256 = (
    "4474bb261b5ff2581e7f50df3883faa8c432cc1f85064e047a210432d8ff98a7"
)


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


def survivor_supports():
    ledger, _digest, _seconds = N.audit()
    supports = {
        tuple(tuple(entry) for entry in row["extras"])
        for row in ledger["survivors"]
    }
    require(len(supports) == len(CORE_WORDS) == 22,
            "the anchor survivors no longer give 22 exact supports")
    return sorted(supports), ledger


def build_core(extras, words):
    admissible, sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    extras = set(extras)
    require(len(extras) == 7 and extras <= off_sigma,
            "a survivor is not a seven-cell off-Sigma support")
    cnf = CNF()
    cell_ids = {entry: cnf.var(("CELL", entry)) for entry in sorted(sigma)}
    mandatory = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    require(mandatory <= sigma, "a mandatory D1 cell left Sigma")
    for entry in sorted(mandatory):
        cnf.add(cell_ids[entry])

    def matching_term(word, matching):
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
        return cnf.and_var(factors, ("TERM", tuple(word), tuple(matching)))

    for values in words:
        require(len(values) == 8 and set(values) <= set(V.COLORS),
                "a frozen core word is malformed")
        word = dict(zip(V.SITES, values))
        terms, constant_terms = [], 0
        for matching in V.MATCHINGS[V.SITES]:
            term = matching_term(word, matching)
            if term is True:
                constant_terms += 1
            elif term is not False:
                terms.append(term)
        pure = len(set(values)) == 1
        if pure:
            require(constant_terms == 0,
                    "a frozen pure fibre became identically supported")
            cnf.add(*terms)
            continue
        if constant_terms >= 2:
            continue
        if constant_terms == 1:
            cnf.add(*terms)
            continue
        if len(terms) == 1:
            cnf.add(-terms[0])
            continue
        prefix, current = [None] * len(terms), None
        for index, term in enumerate(terms):
            prefix[index] = current
            current = cnf.or_var(current, term,
                                 ("PRE", tuple(values), index))
        suffix, current = [None] * len(terms), None
        for index in range(len(terms) - 1, -1, -1):
            suffix[index] = current
            current = cnf.or_var(current, terms[index],
                                 ("SUF", tuple(values), index))
        for index, term in enumerate(terms):
            clause = [-term]
            if prefix[index] is not None:
                clause.append(prefix[index])
            if suffix[index] is not None:
                clause.append(suffix[index])
            cnf.add(*clause)
    return cnf


def unit_refutation(clauses):
    """Return a deterministic unit-propagation trace ending in conflict."""
    assignment = {}
    trace = []
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
                return trace, clause_index
            if len(unresolved) == 1:
                literal = unresolved[0]
                variable, value = abs(literal), literal > 0
                old = assignment.get(variable)
                if old is not None:
                    require(old == value,
                            "unit propagation assigned both polarities")
                else:
                    assignment[variable] = value
                    trace.append((literal, clause_index))
                    progress = True
        require(progress, "the frozen core is not RUP-refutable")


def audit():
    started = monotonic()
    supports, normal_form_ledger = survivor_supports()
    rows = []
    core_sizes = Counter()
    for index, (support, words) in enumerate(zip(supports, CORE_WORDS)):
        require(tuple(sorted(set(words))) == words,
                "a frozen fibre core is not sorted and duplicate-free")
        cnf = build_core(support, words)
        trace, conflict = unit_refutation(cnf.clauses)
        used = {abs(literal) for clause in cnf.clauses for literal in clause}
        core_sizes[len(words)] += 1
        rows.append({
            "support_index": index,
            "support": [list(entry) for entry in support],
            "core_words": [list(word) for word in words],
            "used_variables": len(used),
            "clauses": len(cnf.clauses),
            "unit_steps": len(trace),
            "conflict_clause": conflict,
            "trace_sha256": D.content_hash(trace),
        })
    ledger = {
        "pinned_normal_form_sha256": NORMAL_FORM_SHA256,
        "normal_form_ledger_sha256": N.EXPECTED_LEDGER_SHA256,
        "normal_form_survivor_sha256": normal_form_ledger["survivor_sha256"],
        "support_orbits": len(supports),
        "core_size_histogram": dict(sorted(core_sizes.items())),
        "certificate": ("for every support, the exact Tseitin support-shadow "
                        "core is refuted by unit propagation; equivalently "
                        "the empty clause is RUP"),
        "rows": rows,
        "status": ("all 22 m=7 off-Sigma support orbits are impossible; "
                   "there is no exact-ideal survivor"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the m=7 support-shadow closure ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    variables = [row["used_variables"] for row in ledger["rows"]]
    clauses = [row["clauses"] for row in ledger["rows"]]
    steps = [row["unit_steps"] for row in ledger["rows"]]
    print("n8 D1 m=7 support-shadow closure: PASS (exact)")
    print("support orbits: %d; RUP-refuted: %d"
          % (ledger["support_orbits"], len(ledger["rows"])))
    print("fibre-core sizes:", ledger["core_size_histogram"])
    print("used variables: %d..%d; clauses: %d..%d; unit steps: %d..%d"
          % (min(variables), max(variables), min(clauses), max(clauses),
             min(steps), max(steps)))
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
