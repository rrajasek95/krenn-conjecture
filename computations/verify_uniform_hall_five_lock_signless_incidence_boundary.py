#!/usr/bin/env python3
"""Exact signless-incidence theorem for common-provenance five-row locks.

After grouping opposite crossed lock columns by a common literal matching
tail, a source row containing exactly two columns with the same cofactor has
the form z_u+z_v.  Thus a connected critical block is the signless incidence
matrix of a graph.  A bipartite component has its alternating vertex vector
in the exact lock kernel.  An odd cycle has an integral alternating row
combination equal to 2*z_root, hence gives a localized source unit.

This checker also freezes the sharp boundary: unequal tail weights or one
unmatched extra row can destroy the bipartite kernel.  Consequently the
remaining M3 task is precisely to prove common matching provenance and
absence of extra columns, or route the extra cell through the pinned
two-shared-label or opposite-companion theorems.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py":
        "987c702e6f056cd5715ad2df95b680100aee4b168c4359b2300eaf7022370695",
    "notes/uniform-multisite-hall-k22-effective-hole-m3-boundary.md":
        "5df738886b3f6cdb84112abc99f35bc91b3a3e28cf820f01344cef8df90300ea",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_uniform_two_shared_anchor_unary_label_migration.py":
        "78ab24f1c39d79ea38a80fd80bf43e43624e57dada0345c2c98b30559f528dc6",
    "notes/uniform-two-shared-anchor-unary-label-migration.md":
        "2e794feae556d582dc1623e698e2e331cae44e0de36e9d59125740a908d3b1c9",
    "computations/verify_uniform_hall_third_colour_opposite_companion_wedge.py":
        "46337213f80c7a07b137140ecbfbff80ed3f72d6a97dbaf90a9ed0da30df8fde",
    "notes/uniform-hall-third-colour-opposite-companion-wedge.md":
        "2c59d8bf639ca3aff0f1388e236c5bdc551e6603353fd6fdc7bacd362fe6e7bc",
}
EXPECTED_LEDGER_SHA256 = "fbbb3079756c1b7b163936715686ee5dffc5727f0ea87442f7db9e6efdea045d"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rank(matrix):
    matrix = [[Q(entry) for entry in row] for row in matrix]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def signless_incidence(vertex_count, edges):
    matrix = []
    for left, right in edges:
        row = [0] * vertex_count
        row[left] = row[right] = 1
        matrix.append(row)
    return matrix


def matvec(matrix, vector):
    return [sum(entry * value for entry, value in zip(row, vector, strict=True))
            for row in matrix]


def row_combination(coefficients, matrix):
    return [sum(coefficient * matrix[row][column]
                for row, coefficient in enumerate(coefficients))
            for column in range(len(matrix[0]))]


def cycle_edges(size):
    return tuple((index, (index + 1) % size) for index in range(size))


def audit_cycle_certificates():
    audits = []
    for size in range(3, 10):
        matrix = signless_incidence(size, cycle_edges(size))
        if size % 2 == 0:
            alternating = [1 if index % 2 == 0 else -1
                           for index in range(size)]
            require(matvec(matrix, alternating) == [0] * size,
                    f"the even-cycle alternating kernel changed at {size}")
            require(rank(matrix) == size - 1,
                    f"the even-cycle rank changed at {size}")
            certificate = {
                "type": "bipartite kernel",
                "alternating_vertex_vector": alternating,
            }
        else:
            coefficients = [1 if index % 2 == 0 else -1
                            for index in range(size)]
            expected = [2] + [0] * (size - 1)
            require(row_combination(coefficients, matrix) == expected,
                    f"the odd-cycle 2z certificate changed at {size}")
            require(rank(matrix) == size,
                    f"the odd-cycle rank changed at {size}")
            certificate = {
                "type": "localized 2z unit",
                "alternating_row_coefficients": coefficients,
                "row_combination": expected,
            }
        audits.append({"cycle_length": size, "rank": rank(matrix),
                       "certificate": certificate})
    return audits


def bipartite_signs(vertex_count, edges):
    adjacency = [[] for _vertex in range(vertex_count)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    signs = [0] * vertex_count
    for start in range(vertex_count):
        if signs[start]:
            continue
        signs[start] = 1
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                wanted = -signs[vertex]
                if not signs[other]:
                    signs[other] = wanted
                    stack.append(other)
                elif signs[other] != wanted:
                    return None
    return signs


def audit_connected_graph_theorem():
    # These representatives include trees, even cycles with attached trees,
    # and odd cycles with attached trees.  The proof in the note is uniform:
    # propagate signs on a spanning tree; a same-sign extra edge is odd.
    graphs = {
        "tree": (5, ((0, 1), (1, 2), (1, 3), (3, 4))),
        "even_cycle_with_tail":
            (6, ((0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5))),
        "odd_cycle_with_tail":
            (6, ((0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5))),
    }
    audits = {}
    for name, (vertices, edges) in graphs.items():
        matrix = signless_incidence(vertices, edges)
        signs = bipartite_signs(vertices, edges)
        if signs is not None:
            require(matvec(matrix, signs) == [0] * len(edges)
                    and rank(matrix) == vertices - 1,
                    f"the connected bipartite theorem changed for {name}")
            audits[name] = {"bipartite": True, "rank": rank(matrix),
                            "kernel": signs}
        else:
            require(rank(matrix) == vertices,
                    f"the connected nonbipartite rank changed for {name}")
            audits[name] = {"bipartite": False, "rank": rank(matrix),
                            "odd_cycle_unit": True}
    return audits


def audit_provenance_counterguards():
    # Start with a signless C4.  Its alternating kernel is destroyed by one
    # extra unmatched source row.  Thus entry-minimality cannot use the graph
    # switch until every full-row column is accounted for.
    cycle = signless_incidence(4, cycle_edges(4))
    alternating = [1, -1, 1, -1]
    require(matvec(cycle, alternating) == [0, 0, 0, 0]
            and rank(cycle) == 3,
            "the base signless C4 guard changed")
    with_unmatched = cycle + [[1, 0, 0, 0]]
    require(rank(with_unmatched) == 4
            and matvec(with_unmatched, alternating)[-1] == 1,
            "the unmatched-row obstruction changed")

    # Unequal common-tail coefficients likewise invalidate the signless
    # alternating vector, even though the physical incidence graph is C4.
    weighted = [row[:] for row in cycle]
    weighted[0] = [1, 2, 0, 0]
    require(rank(weighted) == 4
            and matvec(weighted, alternating)[0] == -1,
            "the unequal-tail-weight obstruction changed")
    return {
        "signless_C4_rank": 3,
        "with_one_unmatched_row_rank": 4,
        "unequal_weight_C4_rank": 4,
        "conclusion": (
            "common matching class must give equal two-column coefficients "
            "and every column must be accounted for; incidence alone is "
            "insufficient"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "cycle_certificates": audit_cycle_certificates(),
        "connected_graph_theorem": audit_connected_graph_theorem(),
        "provenance_counterguards": audit_provenance_counterguards(),
        "conditional_source_theorem": (
            "if every common matching class contributes exactly the two "
            "opposite lock columns with one common cofactor and there are "
            "no extra full-row columns, and the component lies in one "
            "same-star square-zero switch space, each connected critical block is "
            "signless incidence.  Bipartite gives the exact alternating "
            "lock-kernel switch; nonbipartite contains an odd cycle whose "
            "integral row combination is 2 times a localized lock pivot"
        ),
        "routing_of_failed_hypotheses": (
            "a k-labelled endpoint/direct extra cell enters the pinned "
            "two-shared-anchor label migration; paired third-colour "
            "opposite companions enter the pinned active four-good wedge; "
            "any other unmatched/unequally weighted column is the exact "
            "remaining source-provenance obstruction"
        ),
        "scope": (
            "uniform integer graph/module theorem and sharp coefficient "
            "counterguards, not a claim that the M3 full rows already "
            "satisfy the signless common-provenance hypothesis"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall five-lock incidence ledger changed: {digest}")
    print("uniform Hall five-lock signless incidence boundary: PASS")
    print("bipartite component -> alternating exact lock kernel")
    print("odd component -> integral 2*pivot localized unit")
    print("sharp obstruction -> unequal provenance or unmatched full-row column")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
