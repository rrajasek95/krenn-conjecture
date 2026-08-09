#!/usr/bin/env python3
"""Exact Boolean support frontier for N=8 D1 with seven off-Sigma cells.

This is a necessary-condition SAT encoding, not a numerical solve and not a
claim that a Boolean survivor is an exact source.  Cell variables range over
all 217 E1-admissible aggregate cells.  Exactly seven of the 128 cells outside
Sigma are active; the six D1 live/harm/E2 cells are active.  A matching term
is live iff all of its cells are active.  Every target-pure fibre is nonempty,
and every target-zero full, six-site, or residue fibre has either zero or at
least two live matching terms (never exactly one).

The emitted DIMACS file uses shared Tseitin AND variables, prefix/suffix OR
variables for the ``not exactly one`` constraints, and an exact-seven
at-least recurrence through level eight.  A solver timeout is an OPEN result.
Any future SAT model must be rechecked by the direct fibre evaluator before it
is recorded; any UNSAT result still needs a checked proof certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import os
import shutil
import subprocess
import sys
import tempfile
from itertools import product
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_COVER_SHA256 = (
    "77f561ed78d9d2bfbd065541274299cd72d226f6a2a19a2e90faf7d74b4bbcc7"
)
COVER_PATH = os.path.join(
    HERE, "verify_n8_d1_minimal_off_sigma_support_cover.py"
)
with open(COVER_PATH, "rb") as handle:
    COVER_SHA256 = hashlib.sha256(handle.read()).hexdigest()
require(COVER_SHA256 == PINNED_COVER_SHA256,
        "the committed D1 support-domain source changed")

V = importlib.import_module("verify_n8_d1_minimal_off_sigma_support_cover")
D = V.D

EXPECTED_DIMACS_SHA256 = (
    "4f547d43acf27781c02a89d7c108bdcce8021d69181539a543ea5d887f6770d6"
)
EXPECTED_LEDGER_SHA256 = (
    "5e0a2de2749b4d63f5aca4c18349200f0231e516ca0c7209bd4608958521036f"
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
        require(literals, "an empty CNF clause was generated")
        self.clauses.append(tuple(literals))

    def and_var(self, inputs, key):
        inputs = tuple(sorted(set(inputs)))
        require(inputs, "empty matching-term conjunction")
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


def support_domains():
    admissible, sigma, off_sigma, kinds = V.reconstruct_support_domains()
    require(len(admissible) == 217 and len(sigma) == 89
            and len(off_sigma) == 128 and kinds == {"RR": 48, "SR": 80},
            "the D1 support domains changed")
    return admissible, sigma, off_sigma


def add_exact_seven(cnf, values):
    """Encode exactly seven true inputs via p[i,j] = (prefix has >=j)."""
    previous = {0: True}
    for index, value in enumerate(values, 1):
        current = {0: True}
        for level in range(1, min(index, 8) + 1):
            old_same = previous.get(level, False)
            old_lower = previous.get(level - 1, False)
            output = cnf.var(("COUNT", index, level))
            current[level] = output
            # output <-> old_same OR (old_lower AND value).
            if old_same is False and old_lower is True:
                cnf.add(-output, value)
                cnf.add(-value, output)
            elif old_same is False:
                cnf.add(-output, old_lower)
                cnf.add(-output, value)
                cnf.add(-old_lower, -value, output)
            elif old_lower is True:
                # The j=1 recurrence is output <-> old_same OR value.
                # Keeping all three clauses is load-bearing: replacing them
                # by output alone was the rejected exploratory encoding.
                cnf.add(-old_same, output)
                cnf.add(-value, output)
                cnf.add(-output, old_same, value)
            else:
                cnf.add(-output, old_same, old_lower)
                cnf.add(-output, old_same, value)
                cnf.add(-old_same, output)
                cnf.add(-old_lower, -value, output)
        previous = current
    cnf.add(previous[7])
    cnf.add(-previous[8])


def build_encoding():
    admissible, sigma, off_sigma = support_domains()
    cnf = CNF()
    cell_ids = {entry: cnf.var(("CELL", entry))
                for entry in sorted(admissible)}

    def matching_term(domain, word, matching):
        entries = []
        for u, v in matching:
            entry = V.cell(u, v, word[u], word[v])
            if entry not in admissible:
                return None
            entries.append(cell_ids[entry])
        return cnf.and_var(
            entries,
            ("TERM", tuple(domain), tuple(word[site] for site in domain),
             tuple(matching)),
        )

    def add_fibre(domain, values, pure):
        word = dict(zip(domain, values))
        terms = []
        for matching in V.MATCHINGS[tuple(domain)]:
            term = matching_term(domain, word, matching)
            if term is not None:
                terms.append(term)
        if pure:
            require(terms, "a target-pure fibre has no admissible matching")
            cnf.add(*terms)
            return
        if not terms:
            return
        if len(terms) == 1:
            cnf.add(-terms[0])
            return
        prefix, current = [None] * len(terms), None
        for index, term in enumerate(terms):
            prefix[index] = current
            current = cnf.or_var(
                current, term, ("PRE", tuple(domain), values, index)
            )
        suffix, current = [None] * len(terms), None
        for index in range(len(terms) - 1, -1, -1):
            suffix[index] = current
            current = cnf.or_var(
                current, terms[index],
                ("SUF", tuple(domain), values, index),
            )
        # If one term is live, another term must be live before or after it.
        for index, term in enumerate(terms):
            clause = [-term]
            if prefix[index] is not None:
                clause.append(prefix[index])
            if suffix[index] is not None:
                clause.append(suffix[index])
            cnf.add(*clause)

    add_exact_seven(cnf, [cell_ids[entry] for entry in sorted(off_sigma)])
    mandatory = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    for entry in sorted(mandatory):
        cnf.add(cell_ids[entry])

    fibre_count = 0
    for domain in (V.SITES, V.W1, V.W2, V.RESIDUE):
        for values in product(V.COLORS, repeat=len(domain)):
            pure = (len(set(values)) == 1 if domain == V.SITES
                    else set(values) == {2})
            add_fibre(domain, values, pure)
            fibre_count += 1
    require(fibre_count == 8100, "the support-fibre domain changed")
    return cnf, cell_ids, {
        "E1_admissible_cells": len(admissible),
        "Sigma_cells": len(sigma),
        "off_Sigma_cells": len(off_sigma),
        "off_Sigma_active": 7,
        "mandatory_D1_cells": len(mandatory),
        "fibres": fibre_count,
        "matching_term_ANDs": len(cnf.and_cache),
    }


def dimacs_bytes(cnf):
    chunks = ["p cnf %d %d\n" %
              (cnf.variable_count, len(cnf.clauses))]
    chunks.extend(" ".join(map(str, clause)) + " 0\n"
                  for clause in cnf.clauses)
    return "".join(chunks).encode("ascii")


def audit_semantics():
    # Exhaust the truth tables behind the two nontrivial recurrences.
    exact_cases = 0
    for values in product((False, True), repeat=10):
        prefix = {0: True}
        for index, value in enumerate(values, 1):
            prefix = {level: (prefix.get(level, False)
                              or (prefix.get(level - 1, False) and value))
                      for level in range(0, min(index, 8) + 1)}
            prefix[0] = True
        require((prefix[7] and not prefix[8]) == (sum(values) == 7),
                "exact-seven recurrence truth table failed")
        exact_cases += 1
    cancellation_cases = 0
    for length in range(1, 9):
        for values in product((False, True), repeat=length):
            prefix = [any(values[:index]) for index in range(length)]
            suffix = [any(values[index + 1:]) for index in range(length)]
            encoded = all((not values[index]) or prefix[index] or suffix[index]
                          for index in range(length))
            require(encoded == (sum(values) != 1),
                    "not-exactly-one truth table failed")
            cancellation_cases += 1
    return {"exact_counter_truth_rows": exact_cases,
            "cancellation_truth_rows": cancellation_cases}


def run_solver(path, timeout):
    executable = shutil.which("z3")
    if executable is None:
        return "UNAVAILABLE", "z3 is not on PATH"
    result = subprocess.run(
        (executable, "-T:%d" % timeout, path),
        text=True, capture_output=True, timeout=timeout + 10,
    )
    output = result.stdout.strip().splitlines()
    verdict = output[0] if output else "NO_OUTPUT"
    require(verdict in ("sat", "unsat", "unknown", "timeout"),
            "unexpected z3 output: %s" % result.stdout[:200])
    return verdict.upper(), result.stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-cnf")
    parser.add_argument("--solve", action="store_true")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    started = monotonic()
    semantics = audit_semantics()
    cnf, _cell_ids, domains = build_encoding()
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    if EXPECTED_DIMACS_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIMACS_SHA256,
                "the m=7 DIMACS encoding changed")
    ledger = {
        "pinned_cover_sha256": COVER_SHA256,
        "domains": domains,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "dimacs_bytes": len(payload),
        "dimacs_sha256": digest,
        "semantics": semantics,
        "status": "OPEN: no certified SAT or UNSAT verdict",
    }
    ledger_digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(ledger_digest == EXPECTED_LEDGER_SHA256,
                "the m=7 support-SAT ledger changed")
    if args.emit_cnf:
        with open(args.emit_cnf, "wb") as handle:
            handle.write(payload)
    verdict = "NOT_RUN"
    if args.solve:
        path = args.emit_cnf
        temporary = None
        if path is None:
            temporary = tempfile.NamedTemporaryFile(suffix=".cnf", delete=False)
            temporary.write(payload)
            temporary.close()
            path = temporary.name
        try:
            verdict, _output = run_solver(path, args.timeout)
        finally:
            if temporary is not None:
                os.unlink(temporary.name)
    print("n8 D1 m=7 exact support-SAT encoding: PASS")
    print("variables: %d; clauses: %d; matching terms: %d; bytes: %d"
          % (cnf.variable_count, len(cnf.clauses),
             domains["matching_term_ANDs"], len(payload)))
    print("sha256:", digest)
    print("solver verdict:", verdict,
          "(only a checked model/proof may change OPEN status)")
    print("ledger sha256:", ledger_digest)
    print("total: %.1f s" % (monotonic() - started))


if __name__ == "__main__":
    main()
