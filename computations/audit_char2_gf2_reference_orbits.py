#!/usr/bin/env python3
"""Exhaust the six-site GF(2) search over reference-matrix isomorphism classes.

An alternating 6-by-6 matrix over GF(2) is the adjacency matrix of a simple
graph.  It is nonsingular exactly when its perfect-matching parity is odd.
There are 47 such graph isomorphism classes.  Fixing one representative of
each class removes the expensive reference-color symmetry from
``search_char2_gf2.py``.

The default invocation runs all 47 exact SAT instances.  On the reference
machine this takes about 95 seconds with CaDiCaL 1.9.5.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path
import subprocess
import sys
import time

import networkx as nx


N = 6
EDGE_ORDER = tuple(itertools.combinations(range(N), 2))


def perfect_matching_parity(vertices, edges):
    if not vertices:
        return 1
    first = vertices[0]
    answer = 0
    for second in vertices[1:]:
        if tuple(sorted((first, second))) not in edges:
            continue
        rest = tuple(vertex for vertex in vertices
                     if vertex not in (first, second))
        answer ^= perfect_matching_parity(rest, edges)
    return answer


def nonsingular_reference_representatives():
    six_vertex_graphs = [graph for graph in nx.graph_atlas_g()
                         if len(graph) == N]
    # The graph atlas contains one representative of every unlabeled simple
    # graph with at most seven vertices; there are 156 at order six.
    assert len(six_vertex_graphs) == 156

    answer = []
    for graph in six_vertex_graphs:
        edges = {tuple(sorted(edge)) for edge in graph.edges()}
        if not perfect_matching_parity(tuple(range(N)), edges):
            continue
        mask = sum(1 << index for index, edge in enumerate(EDGE_ORDER)
                   if edge in edges)
        answer.append((len(edges), mask))
    answer.sort()
    assert len(answer) == 47
    return tuple(answer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=47)
    args = parser.parse_args()

    representatives = nonsingular_reference_representatives()
    if not 0 <= args.start <= args.stop <= len(representatives):
        parser.error("require 0 <= start <= stop <= 47")

    search_script = Path(__file__).with_name("search_char2_gf2.py")
    started = time.time()
    for orbit, (edge_count, mask) in enumerate(
        representatives[args.start:args.stop], args.start
    ):
        run = subprocess.run(
            (
                sys.executable,
                str(search_script),
                "--reference-mask",
                hex(mask),
                "--solver",
                args.solver,
            ),
            check=True,
            capture_output=True,
            text=True,
        )
        result = next(
            line for line in run.stdout.splitlines() if line.startswith("sat=")
        )
        print(
            f"orbit={orbit:02d} edges={edge_count:02d} "
            f"mask={mask:#06x} {result}",
            flush=True,
        )
        if not result.startswith("sat=False"):
            print(run.stdout, end="")
            raise AssertionError(f"countermodel in reference orbit {orbit}")

    elapsed = time.time() - started
    print(
        f"verified UNSAT for reference orbits [{args.start},{args.stop}) "
        f"in {elapsed:.2f}s"
    )
    if args.start == 0 and args.stop == len(representatives):
        print("verified all 47 nonsingular GF(2) reference-matrix classes")


if __name__ == "__main__":
    main()
