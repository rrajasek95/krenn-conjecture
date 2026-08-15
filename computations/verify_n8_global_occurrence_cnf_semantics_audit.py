#!/usr/bin/env python3
"""Independent semantic audit of ``search_n8_global_occurrence_cnf.py``.

The audit does not ask the SAT solver for the advertised UNSAT result.  It
checks the translation layer which that result relies on:

* the matching-occurrence inventory is rebuilt independently;
* intended auxiliary-variable values are replayed through every CNF clause;
* two explicit relaxed SAT witnesses isolate the coordinate and no-singleton
  top-level clauses; and
* the sorted degree-branch list is compared with every 22-edge support graph
  containing the distinguished edge.

Run this file with normal Python, ``python -O``, and ``python -I``.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import inspect
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import random
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "search_n8_global_occurrence_cnf.py"
AUDITED_SEMANTIC_SHA256 = (
    "5c72f7d2ada2214737e53bef97712ba718cce3b124d35f5731ddd17b8e81b97c"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_source():
    digest = sha256(SOURCE.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location("n8_occurrence_cnf", SOURCE)
    require(spec is not None and spec.loader is not None, SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    semantic_payload = "\n".join((
        repr((module.N, module.COLORS, module.EDGES, module.TARGET_EDGE)),
        inspect.getsource(module.CNF),
        inspect.getsource(module.occurrence_inventory),
        inspect.getsource(module.build_instance),
    )).encode("utf-8")
    semantic_digest = sha256(semantic_payload).hexdigest()
    require(semantic_digest == AUDITED_SEMANTIC_SHA256,
            ("CNF semantics changed after the audit", semantic_digest,
             AUDITED_SEMANTIC_SHA256, "full source", digest))
    return module, digest, semantic_digest


CNF_SOURCE, SOURCE_DIGEST, SEMANTIC_DIGEST = load_source()
N = CNF_SOURCE.N
COLORS = CNF_SOURCE.COLORS
EDGES = CNF_SOURCE.EDGES
TARGET_EDGE = CNF_SOURCE.TARGET_EDGE


def independent_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in independent_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(independent_matchings(range(N)))


def independent_inventory():
    inventory = {}
    for matching_index, matching in enumerate(MATCHINGS):
        for edge_colours in product(COLORS, repeat=N // 2):
            word = [None] * N
            cells = []
            for edge, colour in zip(matching, edge_colours, strict=True):
                word[edge[0]] = colour
                word[edge[1]] = colour
                cells.append((edge, colour))
            inventory.setdefault(tuple(word), []).append(
                (matching_index, tuple(cells)))
    return inventory


INVENTORY = independent_inventory()


def word_counts(supports):
    counts = Counter()
    for matching in MATCHINGS:
        if not all(edge in supports for edge in matching):
            continue
        for colours in product(*(supports[edge] for edge in matching)):
            word = [None] * N
            for edge, colour in zip(matching, colours, strict=True):
                word[edge[0]] = colour
                word[edge[1]] = colour
            counts[tuple(word)] += 1
    return counts


def degrees(supports):
    return tuple(sum(edge in supports for edge in EDGES if vertex in edge)
                 for vertex in range(N))


def direct_defects(supports, support_size, target_support,
                   minimum_nonanchors, degree_sequence=None,
                   minimum_support_size=None):
    defects = set()
    if tuple(supports.get(TARGET_EDGE, ())) != tuple(target_support):
        defects.add("target")
    if support_size is not None:
        if len(supports) != support_size:
            defects.add("support")
    elif minimum_support_size is None or len(supports) < minimum_support_size:
        defects.add("support")
    if degree_sequence is not None and degrees(supports) != degree_sequence:
        defects.add("degree")
    nonanchors = sum(len(colours) >= 2 for colours in supports.values())
    if nonanchors < minimum_nonanchors:
        defects.add("nonanchor")
    for vertex in range(N):
        for colour in COLORS:
            if not any(supports.get(edge) == (colour,)
                       for edge in EDGES if vertex in edge):
                defects.add("coordinate")
    counts = word_counts(supports)
    for colour in COLORS:
        if counts[(colour,) * N] == 0:
            defects.add("pure")
    if any(len(set(word)) > 1 and count == 1
           for word, count in counts.items()):
        defects.add("no_singleton")
    return defects


def intended_assignment(instance, supports, minimum_nonanchors,
                        minimum_support_size=None):
    cnf, y, live, nonanchor, occurrence_variables, _word_variables = instance
    values = {}

    for edge in EDGES:
        colours = supports.get(edge, ())
        for colour in COLORS:
            values[y[edge, colour]] = colour in colours
        values[live[edge]] = bool(colours)
        for first, second in ((0, 1), (0, 2), (1, 2)):
            index = cnf.names[
                f"pair_{edge[0]}_{edge[1]}_{first}_{second}"
            ]
            values[index] = first in colours and second in colours
        values[nonanchor[edge]] = len(colours) >= 2
        for colour in COLORS:
            index = cnf.names[f"coordinate_{edge[0]}_{edge[1]}_{colour}"]
            values[index] = colours == (colour,)

    for (word, matching_index), occurrence in occurrence_variables.items():
        _index, cells = next(
            row for row in INVENTORY[word] if row[0] == matching_index
        )
        values[occurrence] = all(
            colour in supports.get(edge, ()) for edge, colour in cells
        )

    live_inputs = tuple(bool(supports.get(edge)) for edge in EDGES)
    nonanchor_inputs = tuple(len(supports.get(edge, ())) >= 2
                             for edge in EDGES)
    degree_inputs = {
        vertex: tuple(bool(supports.get(edge))
                      for edge in EDGES if vertex in edge)
        for vertex in range(N)
    }
    for name, variable in cnf.names.items():
        if "_state_" not in name:
            continue
        prefix, index_text, count_text = name.rsplit("_", 2)
        index = int(index_text)
        count = int(count_text)
        if prefix == "support_state":
            expected = sum(live_inputs[:index])
        elif prefix == "support_minimum_state":
            require(minimum_support_size is not None,
                    "minimum-support counter lacks its threshold")
            expected = min(minimum_support_size, sum(live_inputs[:index]))
        elif prefix == "nonanchor_state":
            expected = min(minimum_nonanchors,
                           sum(nonanchor_inputs[:index]))
        elif prefix.startswith("degree_") and prefix.endswith("_state"):
            vertex = int(prefix.split("_")[1])
            expected = sum(degree_inputs[vertex][:index])
        else:
            raise RuntimeError(("unknown counter state", name))
        values[variable] = count == expected

    require(len(values) == len(cnf.names),
            ("unassigned CNF auxiliaries", len(values), len(cnf.names),
             tuple(name for name, variable in cnf.names.items()
                   if variable not in values)[:10]))
    return values


def clause_holds(clause, values):
    return any(values[abs(literal)] == (literal > 0) for literal in clause)


def violated_family(clause, cnf):
    names = tuple(cnf.reverse[abs(literal)] for literal in clause)
    if len(clause) == 1 and names[0].startswith("y_"):
        return "target"
    if (len(clause) == 1
            and (names[0].startswith("support_state_")
                 or names[0].startswith("support_minimum_state_"))):
        return "support"
    if len(clause) == 1 and names[0].startswith("nonanchor_state_"):
        return "nonanchor"
    if len(clause) == 1 and names[0].startswith("degree_"):
        return "degree"
    if all(name.startswith("coordinate_") for name in names):
        return "coordinate"
    if all(name.startswith("occ_") for name in names):
        return "pure" if all(literal > 0 for literal in clause) \
            else "no_singleton"
    return "definition"


def replay(supports, support_size, target_support, minimum_nonanchors=4,
           degree_sequence=None, minimum_support_size=None):
    instance = CNF_SOURCE.build_instance(
        support_size, target_support, degree_sequence, minimum_nonanchors,
        minimum_support_size,
    )
    cnf = instance[0]
    values = intended_assignment(instance, supports, minimum_nonanchors,
                                 minimum_support_size)
    violated = tuple(clause for clause in cnf.clauses
                     if not clause_holds(clause, values))
    families = {violated_family(clause, cnf) for clause in violated}
    require("definition" not in families,
            ("intended auxiliaries violate a definition", violated[:3]))
    defects = direct_defects(supports, support_size, target_support,
                             minimum_nonanchors, degree_sequence,
                             minimum_support_size)
    require(families == defects,
            ("CNF/direct-semantics mismatch", families, defects,
             tuple(tuple(cnf.reverse[abs(item)] for item in clause)
                   for clause in violated[:4])))
    return cnf, values, families, len(violated)


def round_robin_factorization():
    order = list(range(N))
    factors = []
    for _round in range(N - 1):
        factor = tuple(sorted(tuple(sorted((order[index], order[-1-index])))
                              for index in range(N // 2)))
        factors.append(factor)
        order = [order[0], order[-1], *order[1:-1]]
    require(len({edge for factor in factors for edge in factor}) == len(EDGES),
            factors)
    return tuple(factors)


def positive_controls():
    # Full ternary support has every pure row and every mixed multiplicity at
    # least three.  It satisfies all clauses except literal coordinate-anchor
    # coverage, giving an exact SAT witness when those 24 clauses are removed.
    full = {edge: COLORS for edge in EDGES}
    _cnf, _values, families, full_violations = replay(
        full, len(EDGES), (0, 1, 2), 4
    )
    require(families == {"coordinate"}
            and full_violations == N * len(COLORS),
            (families, full_violations))
    _cnf, _values, minimum_families, minimum_violations = replay(
        full, None, (0, 1, 2), 4, minimum_support_size=18
    )
    require((minimum_families, minimum_violations) ==
            (families, full_violations),
            (minimum_families, minimum_violations,
             families, full_violations))

    # Three edge-disjoint singleton perfect matchings supply all coordinate
    # anchors and pure rows.  Four additional two-colour edges supply the
    # nonanchor threshold.  Hence this is an exact SAT witness after removing
    # only the mixed no-singleton clauses.
    factors = tuple(factor for factor in round_robin_factorization()
                    if TARGET_EDGE not in factor)[:3]
    require(len(factors) == 3, factors)
    anchored = {}
    for colour, factor in enumerate(factors):
        for edge in factor:
            anchored[edge] = (colour,)
    anchored[TARGET_EDGE] = (1, 2)
    unused = tuple(edge for edge in EDGES if edge not in anchored)
    for edge in unused[:3]:
        anchored[edge] = (0, 1)
    require(len(anchored) == 16, anchored)
    sequence = degrees(anchored)
    _cnf, _values, families, singleton_violations = replay(
        anchored, 16, (1, 2), 4, sequence
    )
    require(families == {"no_singleton"} and singleton_violations > 0,
            (families, singleton_violations))

    # Residual target-chart colour swap and the full target stabilizer do not
    # change the direct occurrence verdict.  The CNF has no hidden lex/order
    # clause, so both representatives replay with the same sole defect.
    swapped = {
        edge: tuple(sorted(2 if colour == 1 else 1 if colour == 2 else 0
                           for colour in colours))
        for edge, colours in anchored.items()
    }
    _cnf, _values, swapped_families, swapped_violations = replay(
        swapped, 16, (1, 2), 4
    )
    require((swapped_families, swapped_violations) ==
            (families, singleton_violations),
            (swapped_families, swapped_violations, families,
             singleton_violations))
    _cnf, _values, below_families, _below_violations = replay(
        anchored, None, (1, 2), 4, minimum_support_size=17
    )
    require(below_families == {"support", "no_singleton"}, below_families)
    return {
        "full_without_coordinate": (len(full), full_violations),
        "anchored_without_no_singleton":
            (len(anchored), sequence, swapped_violations),
    }


def randomized_replay():
    randomizer = random.Random(0x8C0F)
    checked = 0
    for target_support in ((1, 2), (0, 1, 2)):
        for _sample in range(6):
            supports = {TARGET_EDGE: target_support}
            for edge in EDGES:
                if edge == TARGET_EDGE:
                    continue
                colours = tuple(colour for colour in COLORS
                                if randomizer.randrange(2))
                if colours:
                    supports[edge] = colours
            minimum = randomizer.randrange(0, 7)
            replay(supports, len(supports), target_support, minimum)
            checked += 1
    return checked


def degree_branch_audit():
    declared = set()
    for degree0 in range(3, 8):
        for degree1 in range(3, degree0 + 1):
            for ascending in combinations_with_replacement(range(3, 8), 6):
                sequence = (degree0, degree1) + tuple(
                    sorted(ascending, reverse=True)
                )
                if sum(sequence) == 44:
                    declared.add(sequence)
    require(len(declared) == 182, len(declared))

    # At support 22 the complement has six edges.  Enumerating its choices is
    # the complete uncoloured support census, with the target edge retained.
    other_edges = tuple(edge for edge in EDGES if edge != TARGET_EDGE)
    realized = set()
    for omitted in combinations(other_edges, len(EDGES) - 22):
        live = set(EDGES).difference(omitted)
        sequence = degrees({edge: (0,) for edge in live})
        if min(sequence) < 3:
            continue
        canonical = (
            max(sequence[0], sequence[1]),
            min(sequence[0], sequence[1]),
            *sorted(sequence[2:], reverse=True),
        )
        realized.add(canonical)
    require(realized <= declared, tuple(sorted(realized - declared))[:8])
    require(len(realized) == 121, len(realized))

    unbranched = CNF_SOURCE.build_instance(22, (1, 2), None, 4)[0]
    require(not any(name.startswith("degree_") for name in unbranched.names),
            "unbranched CNF unexpectedly contains a degree restriction")
    branched = CNF_SOURCE.build_instance(
        22, (1, 2), min(realized), 4
    )[0]
    degree_clauses = [
        clause for clause in branched.clauses
        if any(branched.reverse[abs(literal)].startswith("degree_")
               for literal in clause)
    ]
    require(all(len({branched.reverse[abs(literal)].split("_")[1]
                         for literal in clause
                         if branched.reverse[abs(literal)].startswith(
                             "degree_")}) <= 1
                for clause in degree_clauses),
            "degree branch contains a cross-vertex ordering clause")
    return len(declared), len(realized), len(declared - realized)


def main():
    require(N == 8 and len(MATCHINGS) == 105, (N, len(MATCHINGS)))
    require(INVENTORY == CNF_SOURCE.OCCURRENCES,
            "independent matching-occurrence inventory differs")
    require(len(INVENTORY) == 1641
            and sum(map(len, INVENTORY.values())) == 8505,
            (len(INVENTORY), sum(map(len, INVENTORY.values()))))
    row_histogram = tuple(sorted(Counter(map(len, INVENTORY.values())).items()))
    require(row_histogram == ((3, 1260), (9, 210), (15, 168), (105, 3)),
            row_histogram)

    controls = positive_controls()
    random_cases = randomized_replay()
    declared, realized, empty = degree_branch_audit()
    print("CNF semantic equivalence: PASS")
    print("source sha256", SOURCE_DIGEST)
    print("audited semantic sha256", SEMANTIC_DIGEST)
    print("inventory", len(INVENTORY), 8505, row_histogram)
    print("positive controls", controls)
    print("random intended-assignment replays", random_cases)
    print("degree branches", declared, "realized", realized,
          "structurally empty", empty)
    print("verdict: no overconstraint; symmetry clauses are absent")


if __name__ == "__main__":
    main()
