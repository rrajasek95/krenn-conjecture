#!/usr/bin/env python3
"""Pure-CNF search for the global N=8 diagonal-support obstruction.

This is an independent Boolean encoding of the occurrence layer used by
``verify_n8_global_support18_occurrence_sat_probe.py``.  It deliberately
contains no integer arithmetic.  In particular, for a mixed word with
occurrence indicators ``o_1,...,o_k``, the condition "the multiplicity is
not one" is encoded by the logically equivalent clauses

    o_i -> OR_{j != i} o_j                 (all i).

Exact support and degree constraints use deterministic one-hot counting
automata.  The resulting DIMACS instance can be handed directly to Z3's
SAT front end and is useful for the degree branches on which the QF_LIA
encoding times out.

This is a search utility, not a theorem checker: any UNSAT result intended
for the proof spine must subsequently be frozen/replayed, and any SAT model
must be audited against the literal cap exits and coefficient fibres.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from itertools import product
from pathlib import Path
import subprocess
import tempfile


N = 8
COLORS = (0, 1, 2)
EDGES = tuple((left, right) for left in range(N)
              for right in range(left + 1, N))
TARGET_EDGE = (0, 1)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(range(N)))
require(len(MATCHINGS) == 105, len(MATCHINGS))


class CNF:
    def __init__(self):
        self.names = {}
        self.reverse = {}
        self.clauses = []

    def variable(self, name):
        if name not in self.names:
            index = len(self.names) + 1
            self.names[name] = index
            self.reverse[index] = name
        return self.names[name]

    def add(self, *literals):
        clause = tuple(dict.fromkeys(int(value) for value in literals))
        require(clause and all(value for value in clause), clause)
        if any(-value in clause for value in clause):
            return
        self.clauses.append(clause)

    def equivalent_or(self, output, inputs):
        inputs = tuple(inputs)
        require(inputs, (output, inputs))
        self.add(-output, *inputs)
        for value in inputs:
            self.add(-value, output)

    def equivalent_and(self, output, inputs):
        inputs = tuple(inputs)
        require(inputs, (output, inputs))
        self.add(output, *(-value for value in inputs))
        for value in inputs:
            self.add(-output, value)

    def exactly_one(self, variables):
        variables = tuple(variables)
        require(variables, variables)
        self.add(*variables)
        for left in range(len(variables)):
            for right in range(left + 1, len(variables)):
                self.add(-variables[left], -variables[right])

    def exact_count(self, variables, target, prefix):
        """Deterministic one-hot automaton for sum(variables)=target."""
        variables = tuple(variables)
        require(0 <= target <= len(variables), (target, len(variables)))
        layers = []
        for index in range(len(variables) + 1):
            layer = tuple(self.variable(f"{prefix}_state_{index}_{count}")
                          for count in range(index + 1))
            self.exactly_one(layer)
            layers.append(layer)
        self.add(layers[0][0])
        for index, value in enumerate(variables, start=1):
            previous = layers[index - 1]
            following = layers[index]
            for count, state in enumerate(previous):
                # state & not value -> same count
                self.add(-state, value, following[count])
                # state & value -> count+1
                self.add(-state, -value, following[count + 1])
        self.add(layers[-1][target])

    def at_least(self, variables, target, prefix):
        """Saturated one-hot automaton for sum(variables)>=target."""
        variables = tuple(variables)
        require(0 <= target <= len(variables), (target, len(variables)))
        layers = []
        for index in range(len(variables) + 1):
            maximum = min(index, target)
            layer = tuple(self.variable(f"{prefix}_state_{index}_{count}")
                          for count in range(maximum + 1))
            self.exactly_one(layer)
            layers.append(layer)
        self.add(layers[0][0])
        for index, value in enumerate(variables, start=1):
            previous = layers[index - 1]
            following = layers[index]
            for count, state in enumerate(previous):
                same = count
                plus = min(target, count + 1)
                self.add(-state, value, following[same])
                self.add(-state, -value, following[plus])
        self.add(layers[-1][target])

    def dimacs(self):
        lines = [f"p cnf {len(self.names)} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0"
                     for clause in self.clauses)
        return "\n".join(lines) + "\n"


def occurrence_inventory():
    inventory = {}
    for matching_index, matching in enumerate(MATCHINGS):
        for edge_colours in product(COLORS, repeat=4):
            word = [None] * N
            cells = []
            for edge, colour in zip(matching, edge_colours, strict=True):
                word[edge[0]] = colour
                word[edge[1]] = colour
                cells.append((edge, colour))
            inventory.setdefault(tuple(word), []).append(
                (matching_index, tuple(cells)))
    require(sum(map(len, inventory.values())) == 105 * 3**4,
            sum(map(len, inventory.values())))
    return inventory


OCCURRENCES = occurrence_inventory()


def build_instance(support_size, target_support, degree_sequence=None,
                   minimum_nonanchors=4, minimum_support_size=None,
                   maximum_support_size=None):
    require(target_support in ((1, 2), (0, 1, 2)), target_support)
    require((support_size is None) != (minimum_support_size is None),
            (support_size, minimum_support_size))
    support_sum = (support_size if support_size is not None
                   else minimum_support_size)
    if maximum_support_size is not None:
        require(support_size is None, "maximum requires ranged support")
        require(minimum_support_size <= maximum_support_size <= len(EDGES),
                (minimum_support_size, maximum_support_size))
    if degree_sequence is not None:
        require(support_size is not None,
                "degree sequence requires exact support size")
        require(len(degree_sequence) == N
                and sum(degree_sequence) == 2 * support_size,
                degree_sequence)
    cnf = CNF()
    y = {(edge, colour): cnf.variable(
        f"y_{edge[0]}_{edge[1]}_{colour}")
         for edge in EDGES for colour in COLORS}
    live = {}
    nonanchor = {}
    coordinate = {}
    for edge in EDGES:
        bits = tuple(y[edge, colour] for colour in COLORS)
        live[edge] = cnf.variable(f"live_{edge[0]}_{edge[1]}")
        cnf.equivalent_or(live[edge], bits)

        pair_terms = []
        for first, second in ((0, 1), (0, 2), (1, 2)):
            pair = cnf.variable(
                f"pair_{edge[0]}_{edge[1]}_{first}_{second}")
            cnf.equivalent_and(pair, (bits[first], bits[second]))
            pair_terms.append(pair)
        nonanchor[edge] = cnf.variable(
            f"nonanchor_{edge[0]}_{edge[1]}")
        cnf.equivalent_or(nonanchor[edge], pair_terms)

        for colour in COLORS:
            exact = cnf.variable(
                f"coordinate_{edge[0]}_{edge[1]}_{colour}")
            coordinate[edge, colour] = exact
            # exact <-> y_colour & not y_other & not y_other
            selected = y[edge, colour]
            others = tuple(y[edge, item] for item in COLORS
                           if item != colour)
            cnf.add(-exact, selected)
            for other in others:
                cnf.add(-exact, -other)
            cnf.add(exact, -selected, *others)

    for colour in COLORS:
        literal = y[TARGET_EDGE, colour]
        cnf.add(literal if colour in target_support else -literal)

    if support_size is not None:
        cnf.exact_count(tuple(live.values()), support_size, "support")
    else:
        cnf.at_least(tuple(live.values()), support_sum, "support_minimum")
        if maximum_support_size is not None:
            cnf.at_least(
                tuple(-value for value in live.values()),
                len(live) - maximum_support_size,
                "support_maximum",
            )
    if degree_sequence is not None:
        for vertex, target in enumerate(degree_sequence):
            incident = tuple(live[edge] for edge in EDGES if vertex in edge)
            cnf.exact_count(incident, target, f"degree_{vertex}")
    cnf.at_least(tuple(nonanchor.values()), minimum_nonanchors, "nonanchor")

    for vertex in range(N):
        incident = tuple(edge for edge in EDGES if vertex in edge)
        for colour in COLORS:
            cnf.add(*(coordinate[edge, colour] for edge in incident))

    occurrence_variables = {}
    word_variables = {}
    for word, rows in OCCURRENCES.items():
        variables = []
        for matching_index, cells in rows:
            occurrence = cnf.variable(
                "occ_" + "".join(map(str, word)) + f"_{matching_index}")
            cnf.equivalent_and(
                occurrence,
                tuple(y[edge, colour] for edge, colour in cells),
            )
            occurrence_variables[word, matching_index] = occurrence
            variables.append(occurrence)
        variables = tuple(variables)
        word_variables[word] = variables
        if len(set(word)) == 1:
            cnf.add(*variables)
        else:
            for index, occurrence in enumerate(variables):
                cnf.add(-occurrence,
                        *(variables[other] for other in range(len(variables))
                          if other != index))

    return cnf, y, live, nonanchor, occurrence_variables, word_variables


def parse_degree_sequence(text):
    values = tuple(int(value) for value in text.replace(",", " ").split())
    require(len(values) == N, values)
    return values


def solve(cnf, timeout_seconds):
    temporary = Path(tempfile.mkdtemp(prefix="n8-occurrence-cnf-"))
    path = temporary / "instance.cnf"
    path.write_text(cnf.dimacs(), encoding="utf-8")
    try:
        completed = subprocess.run(
            ("z3", "-dimacs", f"-T:{timeout_seconds}", str(path)),
            text=True, capture_output=True, check=False,
        )
        lines = completed.stdout.splitlines()
        status_line = next((line for line in lines if line.startswith("s ")),
                           "")
        status = {
            "s SATISFIABLE": "sat",
            "s UNSATISFIABLE": "unsat",
            "s UNKNOWN": "unknown",
        }.get(status_line, "unknown")
        model = set()
        if status == "sat":
            for line in lines:
                if line.startswith("v "):
                    model.update(int(value) for value in line[2:].split()
                                 if int(value) > 0)
        return status, model, completed.stdout, completed.stderr
    finally:
        try:
            path.unlink()
            temporary.rmdir()
        except OSError:
            pass


def audit_model(model, y, support_size, target_support,
                degree_sequence=None, minimum_support_size=None,
                maximum_support_size=None):
    supports = {
        edge: tuple(colour for colour in COLORS if y[edge, colour] in model)
        for edge in EDGES
    }
    supports = {edge: colours for edge, colours in supports.items() if colours}
    if support_size is not None:
        require(len(supports) == support_size, len(supports))
    else:
        require(minimum_support_size is not None
                and len(supports) >= minimum_support_size,
                (len(supports), minimum_support_size))
        if maximum_support_size is not None:
            require(len(supports) <= maximum_support_size,
                    (len(supports), maximum_support_size))
    require(supports[TARGET_EDGE] == target_support,
            supports[TARGET_EDGE])
    degrees = tuple(sum(edge in supports for edge in EDGES if vertex in edge)
                    for vertex in range(N))
    if degree_sequence is not None:
        require(degrees == degree_sequence, (degrees, degree_sequence))
    histogram = Counter()
    for word, rows in OCCURRENCES.items():
        count = sum(all(colour in supports.get(edge, ())
                        for edge, colour in cells)
                    for _matching_index, cells in rows)
        histogram[count] += 1
        if len(set(word)) == 1:
            require(count >= 1, (word, count))
        else:
            require(count != 1, (word, count))
    return supports, tuple(sorted(histogram.items()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--support-size", type=int, default=22)
    parser.add_argument("--minimum-support-size", type=int)
    parser.add_argument("--maximum-support-size", type=int)
    parser.add_argument("--target-support", choices=("12", "012"),
                        default="12")
    parser.add_argument("--degree-sequence")
    parser.add_argument("--minimum-nonanchors", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--write-cnf", type=Path)
    parser.add_argument("--write-model", type=Path)
    parser.add_argument("--write-only", action="store_true")
    arguments = parser.parse_args()

    target_support = tuple(map(int, arguments.target_support))
    support_size = arguments.support_size
    if arguments.minimum_support_size is not None:
        require(arguments.support_size == 22,
                "omit --support-size when using --minimum-support-size")
        support_size = None
    degree_sequence = (parse_degree_sequence(arguments.degree_sequence)
                       if arguments.degree_sequence is not None else None)
    cnf, y, _live, _nonanchor, _occurrences, _words = build_instance(
        support_size, target_support, degree_sequence,
        arguments.minimum_nonanchors, arguments.minimum_support_size,
        arguments.maximum_support_size,
    )
    if arguments.write_cnf is not None:
        arguments.write_cnf.write_text(cnf.dimacs(), encoding="utf-8")
    if arguments.write_only:
        require(arguments.write_cnf is not None,
                "--write-only requires --write-cnf")
        print("variables", len(cnf.names), "clauses", len(cnf.clauses))
        print("degree_sequence", degree_sequence)
        return
    status, model, _stdout, stderr = solve(cnf, arguments.timeout)
    print("status", status)
    print("variables", len(cnf.names), "clauses", len(cnf.clauses))
    print("degree_sequence", degree_sequence)
    if status == "sat":
        supports, histogram = audit_model(
            model, y, support_size, target_support, degree_sequence,
            arguments.minimum_support_size, arguments.maximum_support_size)
        print("supports", tuple(sorted(supports.items())))
        print("word_multiplicity_histogram", histogram)
        if arguments.write_model is not None:
            payload = {
                "support_size": len(supports),
                "target_support": target_support,
                "minimum_nonanchors": arguments.minimum_nonanchors,
                "supports": tuple(
                    (edge, colours)
                    for edge, colours in sorted(supports.items())
                ),
                "word_multiplicity_histogram": histogram,
            }
            arguments.write_model.write_text(
                json.dumps(payload, sort_keys=True, separators=(",", ":"))
                + "\n",
                encoding="utf-8",
            )
    elif stderr.strip():
        print("solver_stderr", stderr.strip())


if __name__ == "__main__":
    main()
