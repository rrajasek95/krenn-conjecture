#!/usr/bin/env python3
"""Independently check the frozen deletion-free RUP proof for m=10."""

from __future__ import annotations

import gzip
import hashlib
import importlib
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_AUDIT_SHA256 = (
    "40500a706dd0ba82a25df26cea95ff8231245c367f4350b9c2d9363ff1ffb64a"
)
AUDIT_PATH = os.path.join(HERE, "audit_n8_d1_m10_support_frontier.py")
with open(AUDIT_PATH, "rb") as handle:
    AUDIT_SHA256 = hashlib.sha256(handle.read()).hexdigest()
require(AUDIT_SHA256 == PINNED_AUDIT_SHA256,
        "the committed m=10 frontier audit changed")
A = importlib.import_module("audit_n8_d1_m10_support_frontier")
D = A.D

PROOF_PATH = os.path.join(
    HERE, "certificates", "n8_d1_m10_first_core.glucose42.drup.gz"
)
EXPECTED_RAW_SHA256 = (
    "12be9116c777e020d0362117aec555393a6be6119ee41ce955d13d8c1ac6647b"
)
EXPECTED_GZIP_SHA256 = (
    "edacb7215a32476d2b7c22def364be589c5d9ef7f507ec88b4442468c07c5bd1"
)
EXPECTED_LEDGER_SHA256 = (
    "9c18787620e328c8ff104891b31087074bf90788bb28f41973efeb3fc5ccf772"
)


class RUPDatabase:
    """Deletion-free DRUP checker with persistent two-watched literals."""

    def __init__(self, clauses, variable_count):
        self.variable_count = variable_count
        self.clauses = []
        self.watch_positions = []
        self.watches = {}
        self.root_assignment = [None] * (variable_count + 1)
        self.root_conflict = False
        self.propagations = 0
        units = []
        for clause in clauses:
            self._add_clause(tuple(clause), update_root=False)
            if not clause:
                self.root_conflict = True
            elif len(clause) == 1:
                units.append(clause[0])
        if not self.root_conflict:
            queue = []
            for literal in units:
                if not self._assign(self.root_assignment, literal, queue):
                    self.root_conflict = True
                    break
            if (not self.root_conflict
                    and self._propagate(self.root_assignment, queue)):
                self.root_conflict = True

    def _watch(self, literal, clause_index):
        self.watches.setdefault(literal, []).append(clause_index)

    def _add_clause(self, clause, update_root=True):
        clause_index = len(self.clauses)
        self.clauses.append(clause)
        if len(clause) >= 2:
            self.watch_positions.append([0, 1])
            self._watch(clause[0], clause_index)
            self._watch(clause[1], clause_index)
        elif len(clause) == 1:
            self.watch_positions.append([0, 0])
            self._watch(clause[0], clause_index)
        else:
            self.watch_positions.append([0, 0])
        if not update_root or self.root_conflict:
            return
        unresolved, satisfied = [], False
        for literal in clause:
            value = self.root_assignment[abs(literal)]
            if value is None:
                unresolved.append(literal)
            elif value == (literal > 0):
                satisfied = True
                break
        if satisfied:
            return
        if not unresolved:
            self.root_conflict = True
        elif len(unresolved) == 1:
            queue = []
            if (not self._assign(self.root_assignment, unresolved[0], queue)
                    or self._propagate(self.root_assignment, queue)):
                self.root_conflict = True

    @staticmethod
    def _assign(assignment, literal, queue):
        variable, value = abs(literal), literal > 0
        old = assignment[variable]
        if old is not None:
            return old == value
        assignment[variable] = value
        queue.append(literal)
        return True

    def _propagate(self, assignment, queue):
        head = 0
        while head < len(queue):
            literal = queue[head]
            head += 1
            self.propagations += 1
            false_literal = -literal
            watched = self.watches.get(false_literal, [])
            index = 0
            while index < len(watched):
                clause_index = watched[index]
                clause = self.clauses[clause_index]
                positions = self.watch_positions[clause_index]
                if len(clause) == 1:
                    return True
                if clause[positions[0]] == false_literal:
                    watch_index, other_index = 0, 1
                elif clause[positions[1]] == false_literal:
                    watch_index, other_index = 1, 0
                else:
                    watched[index] = watched[-1]
                    watched.pop()
                    continue
                other = clause[positions[other_index]]
                other_value = assignment[abs(other)]
                if other_value is not None and other_value == (other > 0):
                    index += 1
                    continue
                replacement = None
                for position, candidate in enumerate(clause):
                    if position in (positions[watch_index],
                                    positions[other_index]):
                        continue
                    value = assignment[abs(candidate)]
                    if value is None or value == (candidate > 0):
                        replacement = position
                        break
                if replacement is not None:
                    positions[watch_index] = replacement
                    watched[index] = watched[-1]
                    watched.pop()
                    self._watch(clause[replacement], clause_index)
                    continue
                if other_value is not None:
                    return True
                if not self._assign(assignment, other, queue):
                    return True
                index += 1
        return False

    def check_and_add(self, clause):
        require(all(0 < abs(literal) <= self.variable_count
                    for literal in clause),
                "a proof clause uses an out-of-range variable")
        if self.root_conflict:
            self._add_clause(clause)
            return True
        assignment = self.root_assignment.copy()
        queue = []
        for literal in clause:
            if not self._assign(assignment, -literal, queue):
                self._add_clause(clause)
                return True
        refuted = self._propagate(assignment, queue)
        if refuted:
            self._add_clause(clause)
        return refuted


def parse_proof(raw):
    clauses = []
    for line_number, raw_line in enumerate(raw.decode("ascii").splitlines(), 1):
        fields = raw_line.split()
        require(fields and fields[0] != "d",
                "the proof is not deletion-free at line %d" % line_number)
        numbers = [int(field) for field in fields]
        require(numbers[-1] == 0 and 0 not in numbers[:-1],
                "a malformed proof line was found")
        clauses.append(tuple(numbers[:-1]))
    return clauses


def audit():
    started = monotonic()
    frontier_ledger, frontier_digest, _encoded, _seconds = A.audit()
    admissible, sigma, off_sigma, _kinds = A.V.reconstruct_support_domains()
    group = A.V.d1_group()
    triples = [{state[0] for state in A.N.triple_states(colour)}
               for colour in (0, 1)]
    pairs = A.support_pair_orbits(triples[0], triples[1], group)
    base = pairs[0][0] | pairs[0][1]
    cnf = A.build_frontier_cnf(base, admissible, sigma, off_sigma)
    with open(PROOF_PATH, "rb") as handle:
        compressed = handle.read()
    require(hashlib.sha256(compressed).hexdigest() == EXPECTED_GZIP_SHA256,
            "the compressed DRUP artifact changed")
    raw = gzip.decompress(compressed)
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_RAW_SHA256,
            "the deletion-free DRUP payload changed")
    proof = parse_proof(raw)
    require(len(proof) == 4090 and proof[-1] == (),
            "the proof no longer has 4090 additions ending in empty")
    checker = RUPDatabase(cnf.clauses, cnf.variable_count)
    require(not checker.root_conflict,
            "the input CNF unexpectedly unit-refutes without the proof")
    for index, clause in enumerate(proof):
        require(checker.check_and_add(clause),
                "proof addition %d is not RUP" % index)
    require(checker.root_conflict,
            "the final empty clause did not close the root database")
    ledger = {
        "pinned_audit_sha256": AUDIT_SHA256,
        "frontier_ledger_sha256": frontier_digest,
        "frontier_dimacs_sha256": frontier_ledger["frontier"]["dimacs_sha256"],
        "proof_raw_sha256": EXPECTED_RAW_SHA256,
        "proof_gzip_sha256": EXPECTED_GZIP_SHA256,
        "input_variables": cnf.variable_count,
        "input_clauses": len(cnf.clauses),
        "proof_additions": len(proof),
        "unit_propagations": checker.propagations,
        "certificate": ("every deletion-free proof addition is RUP; the "
                        "last addition is the empty clause"),
        "conclusion": ("the lex-first complete m=10 3+3+4 base-support "
                       "family is empty"),
    }
    digest = D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "the checked m=10 RUP ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 m=10 first-core RUP: PASS (independently checked)")
    print("input: %d variables; %d clauses"
          % (ledger["input_variables"], ledger["input_clauses"]))
    print("proof: %d deletion-free additions; %d unit propagations"
          % (ledger["proof_additions"], ledger["unit_propagations"]))
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
