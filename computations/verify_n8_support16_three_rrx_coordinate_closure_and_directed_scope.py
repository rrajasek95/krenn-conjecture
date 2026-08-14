#!/usr/bin/env python3
"""Close the four support-16 seal-three mutual-coordinate branches.

For each of the four graph orbits whose minimum clean-error face has three
RRX matchings, this checker:

* verifies the common degree-4/degree-4, overlap-two, common-x geometry;
* enumerates every coordinate-anchor/wildcard completion, modulo the global
  S_3 colour action;
* proves all but four completions by an immediate Laurent unit or by the
  one/two-binomial nonzero propagation used at seal two; and
* excludes the final four by an exact Boolean support consequence of all
  3^8 coefficient rows, checked by a standard-library watched-literal DPLL.

The Boolean consequence is deliberately weak but source-valid: a zero mixed
coefficient cannot have exactly one nonzero matching monomial, a nonzero pure
coefficient has at least one nonzero monomial, and every wildcard support edge
has at least one nonzero cell.  UNSAT therefore excludes complex coefficients.

The final audit addresses the directed-anchor scope honestly.  A noncoordinate
near vector in a marked private response role is already an active rank-one
zero by the imported tensor theorem.  Cubic-incident blocks are coordinate by
the cubic lemma.  The checker freezes the finite directed high/high incidence
set not reached by either mechanism; no claim silently coordinates it.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "edbbb640025dc393887eae711e218173bfea019a64ea58e2127dd8a7f618975f"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLOSURE = load_local(
    "n8_support16_two_rrx_for_seal_three",
    "verify_n8_support16_two_rrx_coordinate_mixed_closure.py",
)
SUPPORT16 = CLOSURE.SUPPORT16
N = 8
COLORS = (0, 1, 2)
NONANCHOR = -1
UNASSIGNED = -2

EXPECTED_COMPLETIONS = (19860, 30313, 27227, 27550)
EXPECTED_IMMEDIATE = (19856, 30265, 27155, 27526)
EXPECTED_SPARSE = (4, 48, 68, 24)
EXPECTED_BOOLEAN = (0, 0, 4, 0)


def try_sparse_certificate(matchings, states):
    """Return the sparse mixed certificate, or None if propagation stalls."""
    rows = CLOSURE.sparse_mixed_rows(matchings, states)
    known_nonzero = {
        ("anchor", edge) for edge, state in states.items() if state >= 0
    }
    used_words = set()
    propagation = []
    while True:
        singleton = next((
            (word, monomials[0]) for word, monomials in rows
            if len(monomials) == 1
            and all(variable in known_nonzero for variable in monomials[0])
        ), None)
        if singleton is not None:
            return {
                "binomial_nonzero_propagation": tuple(propagation),
                "singleton_zero_contradiction": singleton,
            }
        next_row = next((
            (word, monomials) for word, monomials in rows
            if len(monomials) == 2 and word not in used_words
            and any(
                all(variable in known_nonzero for variable in monomial)
                for monomial in monomials
            )
        ), None)
        if next_row is None:
            return None
        word, monomials = next_row
        used_words.add(word)
        known_nonzero.update(monomials[0])
        known_nonzero.update(monomials[1])
        propagation.append(next_row)


class WatchedDPLL:
    """Small exact CNF solver; watched positions persist across backtracking."""

    def __init__(self, variable_count, clauses, preferred_variables=()):
        self.variable_count = variable_count
        self.clauses = tuple(tuple(clause) for clause in clauses)
        self.assignment = [0] * (variable_count + 1)
        self.trail = []
        self.watch_positions = []
        self.watch_lists = {}
        self.root_units = []
        self.nodes = 0
        self.conflicts = 0
        self.preferred = tuple(dict.fromkeys(preferred_variables))
        require(all(
            literal != 0 and abs(literal) <= variable_count
            for clause in self.clauses for literal in clause
        ), "CNF contains an invalid literal")
        for index, clause in enumerate(self.clauses):
            require(clause, ("CNF contains an empty clause", index))
            if len(clause) == 1:
                self.watch_positions.append([0, 0])
                self._watch(clause[0], index)
                self.root_units.append(clause[0])
            else:
                self.watch_positions.append([0, 1])
                self._watch(clause[0], index)
                self._watch(clause[1], index)

    def _watch(self, literal, clause_index):
        self.watch_lists.setdefault(literal, []).append(clause_index)

    def _literal_true(self, literal):
        return self.assignment[abs(literal)] == (1 if literal > 0 else -1)

    def _literal_false(self, literal):
        return self.assignment[abs(literal)] == (-1 if literal > 0 else 1)

    def _set_literal(self, literal, queue):
        variable = abs(literal)
        value = 1 if literal > 0 else -1
        if self.assignment[variable] == -value:
            return False
        if self.assignment[variable] == 0:
            self.assignment[variable] = value
            self.trail.append(variable)
            queue.append(literal)
        return True

    def _propagate(self, queue):
        while queue:
            literal = queue.pop()
            false_literal = -literal
            watched = self.watch_lists.get(false_literal, [])
            position = 0
            while position < len(watched):
                clause_index = watched[position]
                clause = self.clauses[clause_index]
                watches = self.watch_positions[clause_index]
                if clause[watches[0]] == false_literal:
                    moving, other_index = 0, 1
                elif clause[watches[1]] == false_literal:
                    moving, other_index = 1, 0
                else:
                    position += 1
                    continue
                other = clause[watches[other_index]]
                if self._literal_true(other):
                    position += 1
                    continue
                replacement = next((
                    index for index, candidate in enumerate(clause)
                    if index not in watches and not self._literal_false(candidate)
                ), None)
                if replacement is not None:
                    watches[moving] = replacement
                    watched[position] = watched[-1]
                    watched.pop()
                    self._watch(clause[replacement], clause_index)
                    continue
                if self._literal_false(other):
                    self.conflicts += 1
                    return False
                if not self._set_literal(other, queue):
                    self.conflicts += 1
                    return False
                position += 1
        return True

    def _search(self):
        self.nodes += 1
        variable = next((
            candidate for candidate in self.preferred
            if self.assignment[candidate] == 0
        ), None)
        if variable is None:
            variable = next((
                candidate for candidate in range(1, self.variable_count + 1)
                if self.assignment[candidate] == 0
            ), None)
        if variable is None:
            return True
        mark = len(self.trail)
        for literal in (-variable, variable):
            queue = []
            if (self._set_literal(literal, queue)
                    and self._propagate(queue)
                    and self._search()):
                return True
            while len(self.trail) > mark:
                self.assignment[self.trail.pop()] = 0
        return False

    def solve(self):
        queue = []
        for literal in self.root_units:
            if not self._set_literal(literal, queue):
                self.conflicts += 1
                return False
        if not self._propagate(queue):
            return False
        return self._search()

    def model_satisfies(self):
        return all(any(self._literal_true(literal) for literal in clause)
                   for clause in self.clauses)


def audit_dpll_calibration():
    cases = (
        (2, ((1, 2), (-1, 2)), True),
        (1, ((1,), (-1,)), False),
        (2, ((1, 2), (1, -2), (-1, 2), (-1, -2)), False),
        (3, ((1, 2), (-1, 3), (-2, 3)), True),
    )
    ledger = []
    for variable_count, clauses, expected in cases:
        solver = WatchedDPLL(variable_count, clauses)
        actual = solver.solve()
        require(actual == expected,
                ("DPLL calibration changed", clauses, actual, expected))
        if actual:
            require(solver.model_satisfies(),
                    ("DPLL returned a nonmodel", clauses, solver.assignment))
        ledger.append((variable_count, clauses, actual, solver.nodes,
                       solver.conflicts))
    return tuple(ledger)


def coefficient_support_cnf(edges, matchings, states):
    variable_ids = {}
    variable_names = {}
    next_id = 0
    base_variables = []
    clauses = []

    def variable_id(name):
        nonlocal next_id
        if name not in variable_ids:
            next_id += 1
            variable_ids[name] = next_id
            variable_names[next_id] = name
        return variable_ids[name]

    # Every wildcard denotes a live support edge, so at least one of its
    # nine cells must be nonzero.
    for edge in edges:
        if states[edge] != NONANCHOR:
            continue
        live_clause = []
        for left in COLORS:
            for right in COLORS:
                variable = variable_id(("wildcard", edge, left, right))
                base_variables.append(variable)
                live_clause.append(variable)
        clauses.append(live_clause)

    encoded_monomials = set()
    row_histogram = Counter()
    for word in product(COLORS, repeat=N):
        monomials = tuple(
            monomial for matching in matchings
            if (monomial := CLOSURE.monomial_for(
                    matching, word, states)) is not None
        )
        if not monomials:
            continue
        row_histogram[len(monomials)] += 1
        activations = []
        for monomial in monomials:
            wildcard_factors = tuple(
                factor for factor in monomial if factor[0] == "wildcard"
            )
            if not wildcard_factors:
                activations.append(True)
                continue
            key = ("monomial", monomial)
            auxiliary = variable_id(key)
            activations.append(auxiliary)
            if key in encoded_monomials:
                continue
            encoded_monomials.add(key)
            factors = tuple(variable_id(factor)
                            for factor in wildcard_factors)
            # auxiliary iff every wildcard factor is nonzero.
            clauses.extend((-auxiliary, factor) for factor in factors)
            clauses.append((auxiliary, *(-factor for factor in factors)))

        if len(set(word)) == 1:
            # A nonzero pure coefficient has some nonzero monomial.
            if True not in activations:
                clauses.append(tuple(activations))
            continue

        # A zero mixed coefficient cannot contain exactly one nonzero term.
        for index, activation in enumerate(activations):
            alternatives = activations[:index] + activations[index + 1:]
            if activation is True:
                if True not in alternatives:
                    clauses.append(tuple(alternatives))
            elif True not in alternatives:
                clauses.append((-activation, *alternatives))

    require(all(clauses), "coefficient support CNF acquired an empty clause")
    digest = sha256(json.dumps(
        [list(clause) for clause in clauses], separators=(",", ":")
    ).encode()).hexdigest()
    return {
        "variable_count": next_id,
        "base_variables": tuple(base_variables),
        "clauses": tuple(tuple(clause) for clause in clauses),
        "row_histogram": dict(row_histogram),
        "cnf_sha256": digest,
    }


def boolean_support_unsat(edges, matchings, states):
    cnf = coefficient_support_cnf(edges, matchings, states)
    solver = WatchedDPLL(
        cnf["variable_count"], cnf["clauses"], cnf["base_variables"]
    )
    satisfiable = solver.solve()
    require(not satisfiable,
            ("final seal-three support guard survived", states,
             cnf["cnf_sha256"]))
    return {
        "wildcard_edges": tuple(edge for edge in edges
                                if states[edge] == NONANCHOR),
        "variable_count": cnf["variable_count"],
        "base_variable_count": len(cnf["base_variables"]),
        "clause_count": len(cnf["clauses"]),
        "row_histogram": cnf["row_histogram"],
        "cnf_sha256": cnf["cnf_sha256"],
        "DPLL_nodes": solver.nodes,
        "DPLL_conflicts": solver.conflicts,
        "satisfiable": satisfiable,
    }


def enumerate_graph_completions(record):
    edges = tuple(record["representative_edges"])
    incident = {
        vertex: tuple(edge for edge in edges if vertex in edge)
        for vertex in range(N)
    }
    states = {edge: UNASSIGNED for edge in edges}
    matchings = CLOSURE.support_matchings(edges)
    completion_count = 0
    immediate_count = 0
    sparse_count = 0
    boolean_states = []
    sparse_lengths = Counter()
    sample_immediate = None
    sample_sparse = None

    def recurse(index, seen_colours):
        nonlocal completion_count, immediate_count, sparse_count
        nonlocal sample_immediate, sample_sparse
        for vertex in range(N):
            visible = {states[edge] for edge in incident[vertex]
                       if states[edge] >= 0}
            remaining = sum(states[edge] == UNASSIGNED
                            for edge in incident[vertex])
            if 3 - len(visible) > remaining:
                return
        if index == len(edges):
            if any(
                {states[edge] for edge in incident[vertex]
                 if states[edge] >= 0} != set(COLORS)
                for vertex in range(N)
            ):
                return
            completion_count += 1
            immediate = CLOSURE.immediate_anchor_unit(matchings, states)
            if immediate is not None:
                immediate_count += 1
                if sample_immediate is None:
                    sample_immediate = immediate
                return
            sparse = try_sparse_certificate(matchings, states)
            if sparse is not None:
                sparse_count += 1
                sparse_lengths[len(sparse["binomial_nonzero_propagation"])] += 1
                if sample_sparse is None:
                    sample_sparse = {
                        "states": tuple(sorted(states.items())),
                        "certificate": sparse,
                    }
                return
            boolean_states.append(dict(states))
            return

        edge = edges[index]
        states[edge] = NONANCHOR
        recurse(index + 1, seen_colours)
        # Canonicalize the global S_3 action by allowing an old colour or the
        # next unseen colour, never a later unseen colour.
        for colour in range(min(len(seen_colours), 2) + 1):
            if colour < len(seen_colours):
                next_seen = seen_colours
            elif colour == len(seen_colours) and len(seen_colours) < 3:
                next_seen = seen_colours + (colour,)
            else:
                continue
            states[edge] = colour
            recurse(index + 1, next_seen)
        states[edge] = UNASSIGNED

    recurse(0, ())
    boolean_certificates = tuple(
        {
            "states": tuple(sorted(state.items())),
            "unsat": boolean_support_unsat(edges, matchings, state),
        }
        for state in boolean_states
    )
    return {
        "support_matching_count": len(matchings),
        "canonical_completion_count": completion_count,
        "full_colour_completion_count": 6 * completion_count,
        "immediate_anchor_units": immediate_count,
        "sparse_binomial_singletons": sparse_count,
        "sparse_length_histogram": dict(sparse_lengths),
        "boolean_support_unsat": len(boolean_certificates),
        "sample_immediate": sample_immediate,
        "sample_sparse": sample_sparse,
        "boolean_certificates": boolean_certificates,
    }


def audit_directed_scope(two_face_records):
    records = []
    totals = Counter()
    for record in two_face_records:
        edges = tuple(record["representative_edges"])
        adjacency = CLOSURE.adjacency_from_edges(edges)
        cubic_vertices = {
            vertex for vertex in range(N)
            if adjacency[vertex].bit_count() == 3
        }
        marked = set()
        face_edges = []
        for edge in edges:
            degree_pair = sorted(
                (adjacency[edge[0]].bit_count(),
                 adjacency[edge[1]].bit_count())
            )
            rrr, rrx, rrx_matchings, _p, _q = (
                SUPPORT16.SUPPORT15.response_counts(adjacency, edge)
            )
            if degree_pair != [3, 4] or (rrr, rrx, rrx_matchings) != (0, 2, 2):
                continue
            geometry = CLOSURE.two_rrx_geometry(adjacency, edges, edge)
            _p_endpoint, high = geometry["cap_endpoints"]
            face_edges.append(edge)
            marked.update(
                (high, tuple(sorted((high, private))))
                for private in geometry["high_privates"]
            )

        # A block incident to a cubic vertex is already same-colour
        # coordinate.  Only directed incidences on high/high edges can carry
        # a genuinely unlanded noncoordinate near vector.
        eligible = {
            (vertex, edge)
            for edge in edges if not (set(edge) & cubic_vertices)
            for vertex in edge
        }
        landed = eligible & marked
        unresolved = eligible - landed
        totals["eligible"] += len(eligible)
        totals["landed"] += len(landed)
        totals["unresolved"] += len(unresolved)
        records.append({
            "degree_sequence": record["degree_sequence"],
            "orbit_size": record["orbit_size"],
            "cubic_vertices": tuple(sorted(cubic_vertices)),
            "two_RRX_face_edges": tuple(face_edges),
            "marked_private_directed_incidences": tuple(sorted(marked)),
            "eligible_high_high_directed_incidences": tuple(sorted(eligible)),
            "landed_noncoordinate_active_roles": tuple(sorted(landed)),
            "unlanded_directed_incidences": tuple(sorted(unresolved)),
        })
    require(totals == Counter({
        "eligible": 488, "landed": 112, "unresolved": 376,
    }), ("directed scope residual totals changed", totals))
    first_two = tuple(
        (item["orbit_size"],
         len(item["eligible_high_high_directed_incidences"]),
         len(item["landed_noncoordinate_active_roles"]),
         len(item["unlanded_directed_incidences"]))
        for item in records[:2]
    )
    require(first_two == ((60, 20, 8, 12), (240, 20, 6, 14)),
            ("first directed residual records changed", first_two))
    return {
        "records": tuple(records),
        "totals": dict(totals),
        "interpretation": (
            "marked noncoordinate private response vectors are active-zero; "
            "unlanded high/high directed incidences remain finite"
        ),
    }


def audit_all():
    support16 = SUPPORT16.audit_census_and_orbits()
    three_records = sorted(
        (
            record for record in support16["terminal_orbits"]
            if record["route"] == "unresolved"
            and record["exit_data"]["minimum_response"][0] == 3
        ),
        key=lambda record: (
            0 if record["degree_sequence"]
                 == (5, 4, 4, 4, 4, 4, 4, 3) else 1,
            record["orbit_size"],
        ),
    )
    two_records = tuple(
        record for record in support16["terminal_orbits"]
        if record["route"] == "unresolved"
        and record["exit_data"]["minimum_response"][0] == 2
    )
    require(len(three_records) == 4 and len(two_records) == 22,
            ("support-16 residual split changed", len(two_records),
             len(three_records)))

    graph_ledgers = []
    for record in three_records:
        edges = tuple(record["representative_edges"])
        adjacency = CLOSURE.adjacency_from_edges(edges)
        geometry = CLOSURE.three_rrx_geometry(
            adjacency, edges, record["exit_data"]["minimum_response"][-1]
        )
        graph_ledgers.append({
            "degree_sequence": record["degree_sequence"],
            "orbit_size": record["orbit_size"],
            "triangles": record["triangles"],
            "squares": record["squares"],
            "representative_edges": edges,
            "three_RRX_geometry": geometry,
            "coordinate_closure": enumerate_graph_completions(record),
        })

    completions = tuple(
        item["coordinate_closure"]["canonical_completion_count"]
        for item in graph_ledgers
    )
    immediate = tuple(
        item["coordinate_closure"]["immediate_anchor_units"]
        for item in graph_ledgers
    )
    sparse = tuple(
        item["coordinate_closure"]["sparse_binomial_singletons"]
        for item in graph_ledgers
    )
    boolean = tuple(
        item["coordinate_closure"]["boolean_support_unsat"]
        for item in graph_ledgers
    )
    require(completions == EXPECTED_COMPLETIONS,
            ("seal-three completion counts changed", completions))
    require(immediate == EXPECTED_IMMEDIATE,
            ("seal-three immediate counts changed", immediate))
    require(sparse == EXPECTED_SPARSE,
            ("seal-three sparse counts changed", sparse))
    require(boolean == EXPECTED_BOOLEAN,
            ("seal-three Boolean counts changed", boolean))
    require(sum(completions) == 104950
            and sum(immediate) == 104802
            and sum(sparse) == 144
            and sum(boolean) == 4,
            "seal-three closure grand totals changed")
    sparse_histogram = Counter()
    for item in graph_ledgers:
        sparse_histogram.update(
            item["coordinate_closure"]["sparse_length_histogram"]
        )
    require(sparse_histogram == Counter({1: 52, 2: 92}),
            ("seal-three sparse length histogram changed", sparse_histogram))

    return {
        "seal_three_graphs": tuple(graph_ledgers),
        "canonical_completion_total": sum(completions),
        "full_colour_completion_total": 6 * sum(completions),
        "immediate_total": sum(immediate),
        "sparse_total": sum(sparse),
        "sparse_length_histogram": dict(sparse_histogram),
        "boolean_unsat_total": sum(boolean),
        "directed_scope": audit_directed_scope(two_records),
    }


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    calibration = audit_dpll_calibration()
    # This imported theorem is the exact justification for landing a
    # noncoordinate marked response vector in an active rank-one zero.
    rank_strata = CLOSURE.EDGE37.audit_anchor_placement_and_rank_strata()
    require(
        rank_strata["rank_strata"]["anchored_near_vector_noncoordinate"]
        == "active rank-one K via ker(w) meeting the coordinate torus",
        "imported noncoordinate landing theorem changed",
    )
    ledger = canonical({
        "DPLL_calibration": calibration,
        "seal_three_and_directed_scope": audit_all(),
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("seal-three coordinate closure ledger changed", digest))

    print("N=8 support-16 seal-three coordinate closure: PASS")
    print("  canonical / full-colour completions: 104950 / 629700")
    print("  immediate Laurent units: 104802")
    print("  sparse binomial-singleton closures: 144")
    print("  full support-CNF UNSAT closures: 4")
    print("  remaining seal-three mutual-coordinate orbits: 0")
    print("  directed noncoordinate scope: 112 landed / 376 finite unlanded")


if __name__ == "__main__":
    main()
