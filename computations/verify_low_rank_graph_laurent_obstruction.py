#!/usr/bin/env python3
"""Reproduce the exact characteristic-zero audits for rank graphs |F|<=3.

The seven Laurent cases use full support lex leaders and direct learned cuts;
the exceptional triangle uses its independent stabilizer/partition-rank
enumeration.  By default the wrapper checks the mathematical outcome and
which cut families were used; ``--strict-recorded-counts`` additionally
checks one recorded solver trajectory.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import itertools
import sys

import pysat

import search_f5_support_sat as base
import verify_color_sensitive_support_obstruction as triangle
import verify_f3_toric_obstruction as laurent


LAURENT_CASES = {
    # graph, transfers, single-fiber cuts, translated-trinomial cuts
    "3P2": (base.THREE_EDGE_GRAPHS["3P2"], 14, 1171, 0),
    "P3+P2+P1": (
        base.THREE_EDGE_GRAPHS["P3+P2+P1"],
        2,
        882,
        0,
    ),
    "P4+2P1": (base.THREE_EDGE_GRAPHS["P4+2P1"], 11, 196, 0),
    "2P2+2P1": (
        laurent.LOWER_EDGE_GRAPHS["2P2+2P1"], 17, 1475, 0
    ),
    "P3+3P1": (laurent.LOWER_EDGE_GRAPHS["P3+3P1"], 0, 698, 1),
    "P2+4P1": (laurent.LOWER_EDGE_GRAPHS["P2+4P1"], 23, 1108, 1),
    "6P1": (laurent.LOWER_EDGE_GRAPHS["6P1"], 12, 483, 1),
}
TRIANGLE_NAME = "C3+3P1"
ALL_CASES = (TRIANGLE_NAME,) + tuple(LAURENT_CASES)


def audit_graph_census():
    canonical = {
        0: {"6P1": laurent.LOWER_EDGE_GRAPHS["6P1"]},
        1: {"P2+4P1": laurent.LOWER_EDGE_GRAPHS["P2+4P1"]},
        2: {
            name: laurent.LOWER_EDGE_GRAPHS[name]
            for name in ("2P2+2P1", "P3+3P1")
        },
        3: dict(base.THREE_EDGE_GRAPHS),
    }

    def relabel(edges, permutation):
        return frozenset(
            tuple(sorted((permutation[u], permutation[v]))) for u, v in edges
        )

    expected = {
        0: {"6P1": 1},
        1: {"P2+4P1": 15},
        2: {"2P2+2P1": 45, "P3+3P1": 60},
        3: {"3P2": 15, "P3+P2+P1": 180, "P4+2P1": 180, "C3+3P1": 20},
    }
    for size, graphs in canonical.items():
        orbits = {
            name: {
                relabel(edges, permutation)
                for permutation in itertools.permutations(base.VERTICES)
            }
            for name, edges in graphs.items()
        }
        assert {name: len(orbit) for name, orbit in orbits.items()} == expected[size]
        candidates = {
            frozenset(edges)
            for edges in itertools.combinations(base.ALL_EDGES, size)
            if max(
                (sum(vertex in edge for edge in edges) for vertex in base.VERTICES),
                default=0,
            )
            <= 2
        }
        union = set().union(*orbits.values())
        assert sum(map(len, orbits.values())) == len(union) == len(candidates)
        assert union == candidates
    print("verified max-degree-two graph census for every 0<=|F|<=3")


class Tee(io.StringIO):
    """Capture verifier output while retaining a readable live transcript."""

    def write(self, value):
        sys.__stdout__.write(value)
        return super().write(value)

    def flush(self):
        sys.__stdout__.flush()
        return super().flush()


def terminal_line(transcript, name):
    prefix = f"{name}: UNSAT;"
    matches = [line for line in transcript.splitlines() if line.startswith(prefix)]
    assert len(matches) == 1, (name, matches)
    return matches[0]


def integer_field(terminal, key):
    prefix = f"{key}="
    payload = terminal.split("; ", 1)[1]
    field = next(part for part in payload.split(", ") if part.startswith(prefix))
    return int(field.removeprefix(prefix))


def run_laurent_case(name, strict_recorded_counts=False):
    (
        exceptional,
        expected_transfers,
        expected_single_cuts,
        expected_translated_cuts,
    ) = LAURENT_CASES[name]
    transcript = Tee()
    with contextlib.redirect_stdout(transcript):
        closed = laurent.audit_graph(
            name,
            exceptional,
            solver_name="cadical195",
            use_symmetry_orbit=False,
            static_rebuild_interval=0,
            use_lex_leaders=True,
            use_support_cuts=False,
        )
    assert closed
    terminal = terminal_line(transcript.getvalue(), name)
    semantic_fragments = (
        "toric_rank_cuts=0",
        "odd_cuts=0",
        "support_cuts=0",
    )
    for fragment in semantic_fragments:
        assert fragment in terminal, (name, fragment, terminal)
    observed_transfers = integer_field(terminal, "transfers")
    observed_single_cuts = integer_field(terminal, "single_fiber_cuts")
    observed_translated_cuts = integer_field(
        terminal, "translated_trinomial_cuts"
    )
    assert observed_single_cuts + observed_translated_cuts > 0
    if strict_recorded_counts:
        assert (
            observed_transfers,
            observed_single_cuts,
            observed_translated_cuts,
        ) == (
            expected_transfers,
            expected_single_cuts,
            expected_translated_cuts,
        ), (
            name,
            terminal,
            expected_transfers,
            expected_single_cuts,
            expected_translated_cuts,
        )
    print(
        f"VERIFIED Laurent audit: {name}; observed "
        f"transfers/single/translated={observed_transfers}/"
        f"{observed_single_cuts}/{observed_translated_cuts}; "
        f"recorded reference={expected_transfers}/"
        f"{expected_single_cuts}/{expected_translated_cuts}"
    )


def run_triangle_case(strict_recorded_counts=False):
    exceptional = base.THREE_EDGE_GRAPHS["C3+3P1"]
    transcript = Tee()
    with contextlib.redirect_stdout(transcript):
        closed = triangle.audit(TRIANGLE_NAME, exceptional)
    assert closed
    terminal = terminal_line(transcript.getvalue(), TRIANGLE_NAME)
    for fragment in (
        "transfers=0",
        "'triangle-rank':",
        "'partition-rank': 3",
    ):
        assert fragment in terminal, (fragment, terminal)
    if strict_recorded_counts:
        for fragment in ("support_blocks=32", "'triangle-rank': 29"):
            assert fragment in terminal, (fragment, terminal)
    print("VERIFIED recorded exceptional-triangle audit: C3+3P1")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--only",
        action="append",
        choices=ALL_CASES,
        help="run one case (repeatable); the default runs every proved case",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="run the triangle and the short P4+2P1 Laurent audit",
    )
    parser.add_argument(
        "--strict-recorded-counts",
        action="store_true",
        help=(
            "also require the recorded model-enumeration trajectory; "
            "UNSAT and cut soundness do not depend on these counts"
        ),
    )
    args = parser.parse_args()
    if args.only:
        selected = tuple(dict.fromkeys(args.only))
    elif args.quick:
        selected = (TRIANGLE_NAME, "P4+2P1")
    else:
        selected = ALL_CASES

    print(
        f"python-sat={pysat.__version__}; backend=cadical195; "
        "arithmetic checks=SymPy/Python integers"
    )
    audit_graph_census()
    for name in selected:
        if name == TRIANGLE_NAME:
            run_triangle_case(args.strict_recorded_counts)
        else:
            run_laurent_case(name, args.strict_recorded_counts)
    print(f"verified {len(selected)}/{len(selected)} selected rank-graph audits")


if __name__ == "__main__":
    main()
