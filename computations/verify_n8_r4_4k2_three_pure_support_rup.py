#!/usr/bin/env python3
"""Exact Boolean/RUP audit of the sharp r=4, 4K2 pure-support gate.

The checker builds a source-relaxing CNF for each of the two possible unions
of two pure perfect matchings.  Frozen deletion-free RUP proofs are replayed
by an independently committed checker.  A deterministic CDCL/RUP generator
is retained behind ``--solve``/``--write-proofs`` for reproducibility.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path
from time import monotonic


N = 8
V = tuple(range(N))
EDGES = tuple(combinations(V, 2))
PURE_REPS = {
    "C8": (
        {(0, 1), (2, 3), (4, 5), (6, 7)},
        {(0, 2), (1, 4), (3, 6), (5, 7)},
    ),
    "C4C4": (
        {(0, 1), (2, 3), (4, 5), (6, 7)},
        {(0, 2), (1, 3), (4, 6), (5, 7)},
    ),
}
ROOT = Path(__file__).resolve().parents[1]
RUP_CHECKER_PATH = ROOT / "computations/verify_n8_d1_m10_first_core_rup.py"
RUP_CHECKER_SHA256 = (
    "5b9a8f2ba5d5ce4e9a511396a78041bbd76b87b64741dd8adbc3391dfa7f97dc"
)
CERTIFICATE_PATHS = {
    name: ROOT / "computations/certificates" / (
        f"n8_r4_4k2_three_pure_{name.lower()}.drup.gz"
    )
    for name in PURE_REPS
}
EXPECTED = {
    "C8": {
        "proof_clauses": 4994,
        "raw_sha256": "29c5c943b2396ce4dcfb946c2918b7d37d1987bb108084de1c4c5bd37b606a5d",
        "gzip_sha256": "2f997683b1604c3bd5cc686004f200dcc2f2538c440f3570b2fe44fbf7090c32",
        "propagations": 561160,
    },
    "C4C4": {
        "proof_clauses": 16179,
        "raw_sha256": "eaadc7cf13e7f5dc87df6705124bd26dc8a45ce951cee954749c634958d43a66",
        "gzip_sha256": "7b7e0e1851fa61a2581e53defeff2a303c4ab1580c795ed6a06e8dafd1b4241b",
        "propagations": 2189919,
    },
}
EXPECTED_LEDGER_SHA256 = (
    "2c889ada85b92ac76eec89878d14ae9d3192f676933160fd37fdadfdb8e2c3f1"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(u, v):
    return (u, v) if u < v else (v, u)


class CNF:
    def __init__(self):
        self.ids = {}
        self.names = [None]
        self.clauses = []

    def var(self, *key):
        if key not in self.ids:
            self.ids[key] = len(self.names)
            self.names.append(key)
        return self.ids[key]

    def add(self, *clause):
        normalized = tuple(dict.fromkeys(clause))
        require(normalized and not any(-x in normalized for x in normalized),
                "invalid or tautological input clause")
        self.clauses.append(normalized)

    def exactly(self, values, count):
        values = tuple(values)
        require(0 <= count <= len(values), "invalid exact cardinality")
        # At most count: every count+1 variables contain a false one.
        for chosen in combinations(values, count + 1):
            self.add(*(-value for value in chosen))
        # At least count: every n-count+1 variables contain a true one.
        for chosen in combinations(values, len(values) - count + 1):
            self.add(*chosen)


def build_cnf(pure_pair, fixed_m=None, fixed_g=None, fixed_p=None):
    cnf = CNF()

    def m(u, v): return cnf.var("M", *edge(u, v))
    def g(u, v): return cnf.var("G", *edge(u, v))
    def a(u, v): return cnf.var("A", u, v)
    def essential(u, v): return cnf.var("E", u, v)
    def label(u, v, colour): return cnf.var("L", u, v, colour)
    def common(u, colour): return cnf.var("C", u, colour)
    def generic(u): return cnf.var("CG", u)
    def third(u, v): return cnf.var("P2", *edge(u, v))

    for u in V:
        cnf.exactly((m(u, v) for v in V if v != u), 1)
        cnf.exactly((g(u, v) for v in V if v != u), 1)
        cnf.exactly((a(u, v) for v in V if v != u), 3)
        cnf.exactly((essential(u, v) for v in V if v != u), 2)
        cnf.exactly([generic(u)] + [common(u, c) for c in range(3)], 1)
        cnf.exactly((third(u, v) for v in V if v != u), 1)
        for colour in range(3):
            cnf.exactly((label(u, v, colour) for v in V if v != u), 1)

    for u, v in EDGES:
        # The reciprocal matching is exactly the set of doubly oriented
        # selected pairs.  The good matching is disjoint from it.
        cnf.add(-m(u, v), -g(u, v))
        cnf.add(-m(u, v), a(u, v))
        cnf.add(-m(u, v), a(v, u))
        cnf.add(-a(u, v), -a(v, u), m(u, v))

        # G is exactly the selected pairs nonessential at both endpoints;
        # every other selected pair is essential at exactly one endpoint.
        cnf.add(-g(u, v), a(u, v), a(v, u))
        cnf.add(-g(u, v), -essential(u, v))
        cnf.add(-g(u, v), -essential(v, u))
        cnf.add(-essential(u, v), -essential(v, u))
        cnf.add(-essential(u, v), a(u, v), a(v, u))
        cnf.add(-essential(v, u), a(u, v), a(v, u))
        cnf.add(-a(u, v), g(u, v), essential(u, v), essential(v, u))
        cnf.add(-a(v, u), g(u, v), essential(u, v), essential(v, u))

        # Every directed selected arc carries exactly one head colour.
        for tail, head in ((u, v), (v, u)):
            labels = [label(tail, head, colour) for colour in range(3)]
            for value in labels:
                cnf.add(-value, a(tail, head))
            cnf.add(-a(tail, head), *labels)
            for left, right in combinations(labels, 2):
                cnf.add(-left, -right)
            # A nonessential incoming head fixes the common line to its axis.
            for colour in range(3):
                cnf.add(-label(tail, head, colour),
                        essential(head, tail), common(head, colour))

    def force_pure_edge(u, v, colour, condition=None):
        if condition is None:
            cnf.add(a(u, v), a(v, u))
        else:
            cnf.add(-condition, a(u, v), a(v, u))
        for tail, head in ((u, v), (v, u)):
            prefix = [] if condition is None else [-condition]
            cnf.add(*prefix, -a(tail, head), label(tail, head, colour))
            cnf.add(*prefix, a(tail, head), essential(head, tail),
                    common(head, colour), generic(head))

    for colour, matching in enumerate(pure_pair):
        for u, v in matching:
            force_pure_edge(u, v, colour)
    for u, v in EDGES:
        force_pure_edge(u, v, 2, third(u, v))

    for fixed, accessor in ((fixed_m, m), (fixed_g, g)):
        if fixed is not None:
            for u, v in EDGES:
                cnf.add(accessor(u, v) if (u, v) in fixed
                        else -accessor(u, v))
    if fixed_p is not None:
        for u, v in EDGES:
            cnf.add(third(u, v) if (u, v) in fixed_p else -third(u, v))

    metadata = {
        "variables": len(cnf.names) - 1,
        "clauses": len(cnf.clauses),
        "clause_lengths": dict(sorted(Counter(map(len, cnf.clauses)).items())),
    }
    return cnf, metadata


def perfect_matchings(vertices=V):
    if not vertices:
        yield frozenset()
        return
    first = vertices[0]
    for second in vertices[1:]:
        rest = tuple(v for v in vertices if v not in (first, second))
        for tail in perfect_matchings(rest):
            yield tail | {edge(first, second)}


MATCHINGS = tuple(perfect_matchings())
require(len(MATCHINGS) == 105, "K8 perfect-matching count changed")


def image_matching(matching, permutation):
    return frozenset(edge(permutation[u], permutation[v])
                     for u, v in matching)


def matching_union_cycle_type(first, second):
    require(len(first) == len(second) == 4 and not first & second,
            "the pure representatives ceased to be disjoint matchings")
    adjacency = {u: [] for u in V}
    for u, v in first | second:
        adjacency[u].append(v)
        adjacency[v].append(u)
    require(all(len(adjacency[u]) == 2 for u in V),
            "a pure representative ceased to cover every site twice")
    unseen, cycles = set(V), []
    while unseen:
        start = next(iter(unseen))
        stack, component = [start], set()
        while stack:
            site = stack.pop()
            if site in component:
                continue
            component.add(site)
            stack.extend(adjacency[site])
        unseen.difference_update(component)
        cycles.append(len(component))
    return tuple(sorted(cycles))


def reciprocal_orbit_representatives(pure_pair):
    first, second = map(frozenset, pure_pair)
    stabilizer = tuple(
        permutation for permutation in permutations(V)
        if image_matching(first, permutation) == first
        and image_matching(second, permutation) == second
    )
    seen, representatives = set(), []
    for matching in MATCHINGS:
        if matching in seen:
            continue
        orbit = {image_matching(matching, permutation)
                 for permutation in stabilizer}
        seen.update(orbit)
        representatives.append(min(orbit, key=lambda value: sorted(value)))
    require(len(seen) == 105, "reciprocal orbit cover changed")
    return stabilizer, tuple(representatives)


def matching_pair_orbit_representatives(pure_pair):
    first, second = map(frozenset, pure_pair)
    stabilizer = tuple(
        permutation for permutation in permutations(V)
        if image_matching(first, permutation) == first
        and image_matching(second, permutation) == second
    )
    pairs = tuple((m, g) for m in MATCHINGS for g in MATCHINGS if not m & g)
    unseen = set(pairs)
    representatives = []
    while unseen:
        pair = min(unseen, key=lambda value: (sorted(value[0]), sorted(value[1])))
        orbit = {
            (image_matching(pair[0], permutation),
             image_matching(pair[1], permutation))
            for permutation in stabilizer
        }
        unseen.difference_update(orbit)
        representatives.append(pair)
    require(len(pairs) == 6300, "disjoint ordered matching-pair count changed")
    return stabilizer, tuple(representatives)


def pure_pair_union_orbits():
    """Audit the two S8 orbits of ordered disjoint perfect matchings."""

    symmetric_group = tuple(permutations(V))
    pairs = {(first, second) for first in MATCHINGS for second in MATCHINGS
             if not first & second}
    require(len(pairs) == 6300,
            "ordered disjoint perfect-matching-pair count changed")
    orbit_sizes = []
    representatives = []
    while pairs:
        representative = min(
            pairs, key=lambda value: (sorted(value[0]), sorted(value[1]))
        )
        orbit = {
            (image_matching(representative[0], permutation),
             image_matching(representative[1], permutation))
            for permutation in symmetric_group
        }
        pairs.difference_update(orbit)
        orbit_sizes.append(len(orbit))
        representatives.append(representative)
    require(sorted(orbit_sizes) == [1260, 5040],
            "the two pure-matching union orbits changed")
    union_cycle_types = [matching_union_cycle_type(*pair)
                         for pair in representatives]
    require(set(union_cycle_types) == {(8,), (4, 4)},
            "the alternating union types ceased to be C8/C4+C4")
    require(matching_union_cycle_type(*PURE_REPS["C8"]) == (8,),
            "the frozen C8 CNF uses the wrong pure-pair representative")
    require(matching_union_cycle_type(*PURE_REPS["C4C4"]) == (4, 4),
            "the frozen C4+C4 CNF uses the wrong pure-pair representative")
    return tuple(sorted(orbit_sizes)), tuple(sorted(union_cycle_types))


def audit_pure_edge_disjointness():
    """Every selected rank-one witness block supports at most one pure colour."""

    cases = 0
    for forward, reverse in ((True, False), (False, True), (True, True)):
        forward_colours = range(3) if forward else (None,)
        reverse_colours = range(3) if reverse else (None,)
        for forward_colour in forward_colours:
            for reverse_colour in reverse_colours:
                supported = set(range(3))
                if forward:
                    supported &= {forward_colour}
                if reverse:
                    supported &= {reverse_colour}
                require(len(supported) <= 1,
                        "one witness block acquired two pure colours")
                cases += 1
    require(cases == 15, "the local pure-edge audit changed")
    return cases


def dimacs_bytes(cnf):
    lines = [f"p cnf {len(cnf.names) - 1} {len(cnf.clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n"
                 for clause in cnf.clauses)
    return "".join(lines).encode("ascii")


def proof_bytes(proof):
    return "".join(" ".join(map(str, clause)) +
                   (" 0\n" if clause else "0\n")
                   for clause in proof).encode("ascii")


def parse_proof(raw):
    proof = []
    for line_number, line in enumerate(raw.decode("ascii").splitlines(), 1):
        values = tuple(map(int, line.split()))
        require(values and values[-1] == 0,
                f"malformed RUP line {line_number}")
        proof.append(values[:-1])
    return tuple(proof)


def load_independent_rup_checker():
    require(sha256(RUP_CHECKER_PATH.read_bytes()).hexdigest()
            == RUP_CHECKER_SHA256,
            "the independent RUP checker dependency changed")
    spec = importlib.util.spec_from_file_location(
        "independent_rup", RUP_CHECKER_PATH
    )
    require(spec is not None and spec.loader is not None,
            "could not load the independent RUP checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.RUPDatabase


def independently_replay(cnf, proof, checker_class):
    checker = checker_class(cnf.clauses, len(cnf.names) - 1)
    require(not checker.root_conflict,
            "the input CNF was already unit-refutable")
    for index, clause in enumerate(proof):
        require(checker.check_and_add(clause),
                f"independent RUP failure at proof clause {index}")
    require(proof and proof[-1] == () and checker.root_conflict,
            "the independent proof replay did not end in empty")
    return checker.propagations


def propagate(clauses, variable_count, assumptions):
    values = [0] * (variable_count + 1)
    for literal in assumptions:
        variable, value = abs(literal), 1 if literal > 0 else -1
        if values[variable] == -value:
            return None
        values[variable] = value
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            unit = 0
            satisfied = False
            multiple = False
            for literal in clause:
                value = values[abs(literal)]
                if value and (value > 0) == (literal > 0):
                    satisfied = True
                    break
                if value == 0:
                    if unit:
                        multiple = True
                    else:
                        unit = literal
            if satisfied:
                continue
            if not unit:
                return None
            if not multiple:
                variable, value = abs(unit), 1 if unit > 0 else -1
                if values[variable] == -value:
                    return None
                if values[variable] == 0:
                    values[variable] = value
                    changed = True
    return values


class WatchedPropagation:
    """Fresh-assignment unit propagation with persistent watched literals."""

    def __init__(self, clauses, variable_count):
        self.variable_count = variable_count
        self.clauses = []
        self.watch_positions = []
        self.watchers = {}
        self.units = []
        self.root_conflict = False
        for clause in clauses:
            self.add_clause(clause)

    def add_clause(self, clause):
        clause = tuple(clause)
        index = len(self.clauses)
        self.clauses.append(clause)
        if not clause:
            self.watch_positions.append((0, 0))
            self.root_conflict = True
            return
        positions = (0, min(1, len(clause) - 1))
        self.watch_positions.append(positions)
        self.watchers.setdefault(clause[positions[0]], []).append(index)
        if positions[1] != positions[0]:
            self.watchers.setdefault(clause[positions[1]], []).append(index)
        else:
            self.units.append(clause[0])

    def propagate(self, assumptions):
        if self.root_conflict:
            return None
        values = [0] * (self.variable_count + 1)
        queue = []

        def enqueue(literal):
            variable, value = abs(literal), 1 if literal > 0 else -1
            if values[variable] == -value:
                return False
            if values[variable] == 0:
                values[variable] = value
                queue.append(literal)
            return True

        for literal in self.units:
            if not enqueue(literal):
                return None
        for literal in assumptions:
            if not enqueue(literal):
                return None
        cursor = 0
        while cursor < len(queue):
            false_literal = -queue[cursor]
            cursor += 1
            watched = self.watchers.get(false_literal, [])
            position = 0
            while position < len(watched):
                clause_index = watched[position]
                clause = self.clauses[clause_index]
                first, second = self.watch_positions[clause_index]
                if clause[first] == false_literal:
                    false_slot, other_slot = 0, second
                elif clause[second] == false_literal:
                    false_slot, other_slot = 1, first
                else:
                    # The index moved to another watched-literal list.
                    watched[position] = watched[-1]
                    watched.pop()
                    continue
                other = clause[other_slot]
                other_value = values[abs(other)]
                if other_value and ((other_value > 0) == (other > 0)):
                    position += 1
                    continue
                replacement = None
                for candidate_position, candidate in enumerate(clause):
                    if candidate_position in (first, second):
                        continue
                    value = values[abs(candidate)]
                    if not value or ((value > 0) == (candidate > 0)):
                        replacement = (candidate_position, candidate)
                        break
                if replacement is not None:
                    new_position, new_literal = replacement
                    if false_slot == 0:
                        self.watch_positions[clause_index] = (new_position, second)
                    else:
                        self.watch_positions[clause_index] = (first, new_position)
                    watched[position] = watched[-1]
                    watched.pop()
                    self.watchers.setdefault(new_literal, []).append(clause_index)
                    continue
                if other_value and ((other_value > 0) != (other > 0)):
                    return None
                if not enqueue(other):
                    return None
                position += 1
        return values


class TreeRUP:
    def __init__(self, cnf, max_nodes):
        self.variable_count = len(cnf.names) - 1
        self.clauses = list(cnf.clauses)
        self.input_count = len(self.clauses)
        self.proof = []
        self.nodes = 0
        self.max_nodes = max_nodes
        self.db = WatchedPropagation(self.clauses, self.variable_count)

    def add_rup(self, clause):
        clause = tuple(dict.fromkeys(clause))
        assumptions = tuple(-literal for literal in clause)
        require(self.db.propagate(assumptions) is None,
                "a learned tree clause is not RUP")
        self.clauses.append(clause)
        self.db.add_clause(clause)
        self.proof.append(clause)

    def choose(self, values):
        best = None
        best_open = self.variable_count + 1
        scores = Counter()
        for clause in self.clauses:
            if any(values[abs(lit)] and
                   ((values[abs(lit)] > 0) == (lit > 0)) for lit in clause):
                continue
            open_literals = [lit for lit in clause if values[abs(lit)] == 0]
            if len(open_literals) < best_open:
                best_open = len(open_literals)
                best = open_literals
            for literal in open_literals:
                scores[abs(literal)] += 1
        require(best, "a satisfying assignment survived the UNSAT search")
        variable = max((abs(lit) for lit in best), key=lambda x: scores[x])
        return variable

    def refute(self, decisions=()):
        self.nodes += 1
        require(self.nodes <= self.max_nodes,
                "tree-RUP node budget exceeded")
        values = self.db.propagate(decisions)
        parent_clause = tuple(-literal for literal in decisions)
        if values is None:
            self.add_rup(parent_clause)
            return
        variable = self.choose(values)
        self.refute(decisions + (variable,))
        # The first child may already make the parent assumptions conflict.
        if self.db.propagate(decisions) is None:
            self.add_rup(parent_clause)
            return
        self.refute(decisions + (-variable,))
        self.add_rup(parent_clause)


class CDCLRUP:
    """Small deterministic CDCL solver emitting deletion-free RUP clauses."""

    def __init__(self, cnf, max_conflicts):
        self.variable_count = len(cnf.names) - 1
        self.clauses = []
        self.watch_positions = []
        self.watchers = {}
        self.values = [0] * (self.variable_count + 1)
        self.levels = [0] * (self.variable_count + 1)
        self.reasons = [None] * (self.variable_count + 1)
        self.trail = []
        self.trail_limits = []
        self.qhead = 0
        self.activity = [0] * (self.variable_count + 1)
        self.proof = []
        self.conflicts = 0
        self.max_conflicts = max_conflicts
        self.root_conflict = False
        for clause in cnf.clauses:
            for literal in clause:
                self.activity[abs(literal)] += 1
            index = self.add_clause(clause)
            if len(clause) == 1 and not self.enqueue(clause[0], index):
                self.root_conflict = True

    @property
    def decision_level(self):
        return len(self.trail_limits)

    def add_clause(self, clause):
        clause = tuple(dict.fromkeys(clause))
        index = len(self.clauses)
        self.clauses.append(clause)
        if not clause:
            self.watch_positions.append((0, 0))
            self.root_conflict = True
            return index
        positions = (0, min(1, len(clause) - 1))
        self.watch_positions.append(positions)
        self.watchers.setdefault(clause[positions[0]], []).append(index)
        if positions[1] != positions[0]:
            self.watchers.setdefault(clause[positions[1]], []).append(index)
        return index

    def literal_value(self, literal):
        value = self.values[abs(literal)]
        return value if literal > 0 else -value

    def enqueue(self, literal, reason):
        variable = abs(literal)
        value = 1 if literal > 0 else -1
        if self.values[variable] == -value:
            return False
        if self.values[variable] == 0:
            self.values[variable] = value
            self.levels[variable] = self.decision_level
            self.reasons[variable] = reason
            self.trail.append(literal)
        return True

    def propagate(self):
        while self.qhead < len(self.trail):
            false_literal = -self.trail[self.qhead]
            self.qhead += 1
            watched = self.watchers.get(false_literal, [])
            position = 0
            while position < len(watched):
                clause_index = watched[position]
                clause = self.clauses[clause_index]
                first, second = self.watch_positions[clause_index]
                if clause[first] == false_literal:
                    false_slot, other_slot = 0, second
                elif clause[second] == false_literal:
                    false_slot, other_slot = 1, first
                else:
                    watched[position] = watched[-1]
                    watched.pop()
                    continue
                other = clause[other_slot]
                if self.literal_value(other) > 0:
                    position += 1
                    continue
                replacement = None
                for candidate_position, candidate in enumerate(clause):
                    if candidate_position in (first, second):
                        continue
                    if self.literal_value(candidate) >= 0:
                        replacement = (candidate_position, candidate)
                        break
                if replacement is not None:
                    new_position, new_literal = replacement
                    if false_slot == 0:
                        self.watch_positions[clause_index] = (new_position, second)
                    else:
                        self.watch_positions[clause_index] = (first, new_position)
                    watched[position] = watched[-1]
                    watched.pop()
                    self.watchers.setdefault(new_literal, []).append(clause_index)
                    continue
                if self.literal_value(other) < 0:
                    return clause_index
                if not self.enqueue(other, clause_index):
                    return clause_index
                position += 1
        return None

    def cancel_until(self, level):
        if self.decision_level <= level:
            return
        target = self.trail_limits[level]
        for literal in self.trail[target:]:
            variable = abs(literal)
            self.values[variable] = 0
            self.levels[variable] = 0
            self.reasons[variable] = None
        del self.trail[target:]
        del self.trail_limits[level:]
        self.qhead = min(self.qhead, len(self.trail))

    def analyze(self, conflict_index):
        learned = [0]
        seen = [False] * (self.variable_count + 1)
        path_count = 0
        trail_index = len(self.trail) - 1
        pivot = 0
        clause = self.clauses[conflict_index]
        while True:
            for literal in clause:
                variable = abs(literal)
                if variable == abs(pivot) or seen[variable] or self.levels[variable] == 0:
                    continue
                seen[variable] = True
                self.activity[variable] += 1
                if self.levels[variable] == self.decision_level:
                    path_count += 1
                else:
                    learned.append(literal)
            while trail_index >= 0 and not seen[abs(self.trail[trail_index])]:
                trail_index -= 1
            require(trail_index >= 0, "conflict analysis lost its UIP")
            pivot = self.trail[trail_index]
            trail_index -= 1
            seen[abs(pivot)] = False
            path_count -= 1
            if path_count == 0:
                learned[0] = -pivot
                break
            reason = self.reasons[abs(pivot)]
            require(reason is not None, "a non-UIP decision had no reason")
            clause = self.clauses[reason]
        if len(learned) == 1:
            backtrack = 0
        else:
            best = max(range(1, len(learned)),
                       key=lambda index: self.levels[abs(learned[index])])
            learned[1], learned[best] = learned[best], learned[1]
            backtrack = self.levels[abs(learned[1])]
        return tuple(learned), backtrack

    def decide(self):
        candidates = [variable for variable in range(1, self.variable_count + 1)
                      if self.values[variable] == 0]
        if not candidates:
            return None
        return max(candidates, key=lambda variable: (self.activity[variable],
                                                     -variable))

    def solve(self):
        if self.root_conflict:
            self.proof.append(())
            return False
        while True:
            conflict = self.propagate()
            if conflict is not None:
                self.conflicts += 1
                require(self.conflicts <= self.max_conflicts,
                        "CDCL conflict budget exceeded")
                if self.decision_level == 0:
                    self.proof.append(())
                    return False
                learned, backtrack = self.analyze(conflict)
                self.cancel_until(backtrack)
                index = self.add_clause(learned)
                self.proof.append(learned)
                require(self.enqueue(learned[0], index),
                        "learned asserting literal contradicted its backtrack")
                continue
            variable = self.decide()
            if variable is None:
                return True
            self.trail_limits.append(len(self.trail))
            require(self.enqueue(variable, None), "decision enqueue failed")


def replay_rup(cnf, proof):
    db = WatchedPropagation(cnf.clauses, len(cnf.names) - 1)
    for index, clause in enumerate(proof):
        require(db.propagate(tuple(-literal for literal in clause)) is None,
                f"proof clause {index} is not RUP")
        db.add_clause(clause)
    require(proof and proof[-1] == () and db.root_conflict,
            "deletion-free proof did not end in checked empty")


def audit_semantics():
    # Exhaust the small exact-cardinality building block truth tables.
    rows = 0
    for length in range(1, 8):
        for count in range(length + 1):
            cnf = CNF()
            variables = [cnf.var("X", i) for i in range(length)]
            cnf.exactly(variables, count)
            for mask in range(1 << length):
                assumptions = tuple(variable if mask & (1 << index) else -variable
                                    for index, variable in enumerate(variables))
                sat = propagate(cnf.clauses, length, assumptions) is not None
                require(sat == (mask.bit_count() == count),
                        "exact-cardinality CNF truth table failed")
                rows += 1
    # Independently compare the persistent watched propagator with the slow
    # truth-table propagation on all assumptions in the same small systems.
    watched_rows = 0
    for length in range(1, 7):
        for count in range(length + 1):
            cnf = CNF()
            variables = [cnf.var("W", i) for i in range(length)]
            cnf.exactly(variables, count)
            watched = WatchedPropagation(cnf.clauses, length)
            for mask in range(1 << length):
                assumptions = tuple(variable if mask & (1 << index)
                                    else -variable
                                    for index, variable in enumerate(variables))
                slow = propagate(cnf.clauses, length, assumptions) is not None
                fast = watched.propagate(assumptions) is not None
                require(slow == fast,
                        "watched and slow unit propagation disagreed")
                watched_rows += 1
    return rows, watched_rows


def generate_proofs(max_conflicts):
    generated = {}
    for name, pure_pair in PURE_REPS.items():
        cnf, _metadata = build_cnf(pure_pair)
        solver = CDCLRUP(cnf, max_conflicts)
        require(not solver.solve(), f"{name}: the three-pure CNF was SAT")
        replay_rup(cnf, solver.proof)
        generated[name] = tuple(solver.proof)
    return generated


def audit():
    truth_rows, watched_rows = audit_semantics()
    pure_edge_cases = audit_pure_edge_disjointness()
    orbit_sizes, union_types = pure_pair_union_orbits()
    checker_class = load_independent_rup_checker()
    rows = {}
    for name, pure_pair in PURE_REPS.items():
        cnf, metadata = build_cnf(pure_pair)
        encoded = dimacs_bytes(cnf)
        compressed = CERTIFICATE_PATHS[name].read_bytes()
        raw = gzip.decompress(compressed)
        proof = parse_proof(raw)
        propagations = independently_replay(cnf, proof, checker_class)
        expected = EXPECTED[name]
        actual = {
            "proof_clauses": len(proof),
            "raw_sha256": sha256(raw).hexdigest(),
            "gzip_sha256": sha256(compressed).hexdigest(),
            "propagations": propagations,
        }
        for key, value in expected.items():
            if value not in ("TO_BE_FROZEN", None):
                require(actual[key] == value,
                        f"{name}: frozen {key} changed")
        require(proof[-1] == (), f"{name}: proof lost its terminal empty")
        rows[name] = {
            **metadata,
            "dimacs_sha256": sha256(encoded).hexdigest(),
            **actual,
        }
    ledger = {
        "sites": N,
        "rank_one_witness_block_local_cases": pure_edge_cases,
        "ordered_disjoint_pure_matching_pairs": 6300,
        "pure_pair_orbit_sizes": orbit_sizes,
        "pure_pair_union_types": union_types,
        "truth_table_rows": truth_rows,
        "watched_propagation_comparison_rows": watched_rows,
        "independent_RUP_checker_sha256": RUP_CHECKER_SHA256,
        "orbits": rows,
        "verdict": (
            "no sharp all-flat r=4 equality packet with good graph 4K2 "
            "supports all three pure GHZ coefficients"
        ),
        "scope": (
            "Boolean relaxation of selected rank-one witness heads, exact "
            "r=4 reciprocal matching, exact 4K2 good matching, and two "
            "essential incidences/site; closes this sharp all-flat stratum, "
            "not other r=4 good graphs or the curved-overlap branch"
        ),
    }
    encoded_ledger = json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    digest = sha256(encoded_ledger).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the r=4 three-pure ledger changed")
    return ledger, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solve", action="store_true")
    parser.add_argument("--write-proofs", action="store_true")
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    args = parser.parse_args()
    if args.solve or args.write_proofs:
        started = monotonic()
        proofs = generate_proofs(args.max_nodes)
        for name, proof in proofs.items():
            raw = proof_bytes(proof)
            compressed = gzip.compress(raw, compresslevel=9, mtime=0)
            print(name, "generated clauses", len(proof),
                  "raw/gzip", len(raw), len(compressed),
                  "raw sha256", sha256(raw).hexdigest(),
                  "gzip sha256", sha256(compressed).hexdigest())
            if args.write_proofs:
                CERTIFICATE_PATHS[name].parent.mkdir(parents=True, exist_ok=True)
                CERTIFICATE_PATHS[name].write_bytes(compressed)
        print("generation seconds:", round(monotonic() - started, 3))
        if args.write_proofs:
            print("wrote frozen proof candidates; rerun normally to audit")
            return
    ledger, digest = audit()
    print("N=8 sharp r=4, 4K2 three-pure support: EMPTY")
    print("pure-pair orbit sizes:", ledger["pure_pair_orbit_sizes"])
    for name, row in ledger["orbits"].items():
        print(name, "CNF", row["variables"], row["clauses"],
              "RUP additions", row["proof_clauses"],
              "propagations", row["propagations"])
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
