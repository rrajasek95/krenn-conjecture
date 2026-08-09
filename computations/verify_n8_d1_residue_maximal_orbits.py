#!/usr/bin/env python3
"""Exact maximal-orbit census for the checked D1 residue support clauses."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

from pysat.solvers import Solver

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_branch63_candidate.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the pinned D1 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D, V = C.D, C.V

EXPECTED_CNF_SHA256 = (
    "5479362a3f988272af0333a275b8663a1e1bfb87d6989938314949342aca41ee"
)
EXPECTED_LEDGER_SHA256 = (
    "06a2e071717cfe28933134c1d456ed718009e63375676c58c01dc67065ba0525"
)
EXPECTED_HOLES = (
    ((4, 7, 2, 0), (4, 7, 2, 1),
     (5, 6, 0, 2), (5, 6, 1, 2), (5, 6, 2, 0), (5, 6, 2, 1),
     (5, 7, 2, 2), (6, 7, 0, 2), (6, 7, 1, 2)),
    ((4, 6, 2, 0), (4, 6, 2, 1),
     (4, 7, 0, 2), (4, 7, 1, 2),
     (5, 6, 0, 2), (5, 6, 1, 2),
     (5, 7, 2, 0), (5, 7, 2, 1)),
    ((4, 7, 0, 2), (4, 7, 1, 2), (4, 7, 2, 0), (4, 7, 2, 1),
     (5, 6, 0, 2), (5, 6, 1, 2), (5, 6, 2, 0), (5, 6, 2, 1)),
    ((4, 7, 0, 0), (4, 7, 0, 1), (4, 7, 1, 0), (4, 7, 1, 1),
     (4, 7, 2, 0), (4, 7, 2, 1),
     (5, 7, 0, 0), (5, 7, 0, 1), (5, 7, 1, 0), (5, 7, 1, 1),
     (5, 7, 2, 0), (5, 7, 2, 1),
     (6, 7, 0, 0), (6, 7, 0, 1), (6, 7, 0, 2),
     (6, 7, 1, 0), (6, 7, 1, 1), (6, 7, 1, 2),
     (6, 7, 2, 0), (6, 7, 2, 1)),
    ((4, 6, 2, 2), (4, 7, 2, 0), (4, 7, 2, 1),
     (5, 6, 2, 0), (5, 6, 2, 1), (5, 7, 2, 2),
     (6, 7, 0, 2), (6, 7, 1, 2), (6, 7, 2, 0), (6, 7, 2, 1)),
    ((4, 6, 2, 2), (4, 7, 2, 0), (4, 7, 2, 1),
     (5, 6, 2, 0), (5, 6, 2, 1),
     (5, 7, 0, 2), (5, 7, 1, 2),
     (6, 7, 2, 0), (6, 7, 2, 1)),
)


def build_cnf():
    cells = tuple(sorted(
        V.cell(u, v, i, j)
        for u, v in itertools.combinations(V.RESIDUE, 2)
        for i, j in itertools.product(V.COLORS, repeat=2)
    ))
    index = {cell: position + 1 for position, cell in enumerate(cells)}
    edges = tuple(itertools.combinations(V.RESIDUE, 2))
    clauses = []
    family_counts = {}

    def add(clause):
        clauses.append(list(dict.fromkeys(clause)))

    before = len(clauses)
    for colours in itertools.product(V.COLORS, repeat=4):
        word = dict(zip(V.RESIDUE, colours))
        terms = [tuple(index[V.cell(u, v, word[u], word[v])]
                       for u, v in matching)
                 for matching in V.MATCHINGS[V.RESIDUE]]
        if colours == (2, 2, 2, 2):
            for picks in itertools.product((0, 1), repeat=3):
                add([terms[matching][picks[matching]]
                     for matching in range(3)])
        else:
            for live in range(3):
                other = [matching for matching in range(3)
                         if matching != live]
                for picks in itertools.product((0, 1), repeat=2):
                    add([-terms[live][0], -terms[live][1],
                         terms[other[0]][picks[0]],
                         terms[other[1]][picks[1]]])
    family_counts["residue_support_shadow"] = len(clauses) - before

    before = len(clauses)
    for center in V.RESIDUE:
        neighbours = [site for site in V.RESIDUE if site != center]
        groups = [[index[V.cell(center, neighbour, 2, colour)]
                   for colour in (0, 1)] for neighbour in neighbours]
        for picks in itertools.product((0, 1), repeat=3):
            add([-groups[position][picks[position]] for position in range(3)])
    family_counts["target_star_quotient_61594a9"] = len(clauses) - before

    before = len(clauses)
    for special in edges:
        opposite = tuple(site for site in V.RESIDUE if site not in special)
        adjacent = set(edges) - {special, opposite}
        holes = {V.cell(*special, 0, 0), V.cell(*special, 1, 1)}
        required_adjacent = {
            V.cell(*edge, i, j) for edge in adjacent
            for i, j in itertools.product(V.COLORS, repeat=2)
        }
        required_special = {
            V.cell(*special, i, j)
            for i, j in ((0, 1), (0, 2), (1, 0),
                         (1, 2), (2, 0), (2, 1))
        }
        for i, j in itertools.product(V.COLORS, repeat=2):
            if (i, j) == (2, 2):
                continue
            required = (required_adjacent | required_special
                        | {V.cell(*opposite, i, j)})
            add([-index[cell] for cell in required]
                + [index[cell] for cell in holes])
    family_counts["same_diagonal_ad7912b"] = len(clauses) - before

    before = len(clauses)
    for special in edges:
        opposite = tuple(site for site in V.RESIDUE if site not in special)
        adjacent = set(edges) - {special, opposite}
        required_adjacent = {
            V.cell(*edge, i, j) for edge in adjacent
            for i, j in itertools.product(V.COLORS, repeat=2)
        }
        for surviving in (0, 1):
            other = 1 - surviving
            holes = {V.cell(*special, surviving, other),
                     V.cell(*special, other, surviving),
                     V.cell(*special, other, other)}
            diagonal = V.cell(*special, surviving, surviving)
            for i, j in itertools.product(V.COLORS, repeat=2):
                required = (required_adjacent
                            | {diagonal, V.cell(*opposite, i, j)})
                add([-index[cell] for cell in required]
                    + [index[cell] for cell in holes])
    family_counts["three_corner_ee41aef"] = len(clauses) - before

    before = len(clauses)
    for special in edges:
        opposite = tuple(site for site in V.RESIDUE if site not in special)
        adjacent = set(edges) - {special, opposite}
        holes = {V.cell(*special, i, j)
                 for i, j in itertools.product((0, 1), repeat=2)}
        required = {
            V.cell(*edge, i, j) for edge in adjacent
            for i, j in itertools.product(V.COLORS, repeat=2)
        }
        required |= {V.cell(*special, i, j)
                     for i, j in ((0, 2), (1, 2), (2, 0), (2, 1))}
        for i, j in itertools.product(V.COLORS, repeat=2):
            if (i, j) == (2, 2):
                continue
            packet = required | {V.cell(*opposite, i, j)}
            add([-index[cell] for cell in packet]
                + [index[cell] for cell in holes])
    family_counts["target_cross_82bb313"] = len(clauses) - before

    require(len(cells) == 54 and len(clauses) == 1204
            and family_counts == {
                "residue_support_shadow": 968,
                "target_star_quotient_61594a9": 32,
                "same_diagonal_ad7912b": 48,
                "three_corner_ee41aef": 108,
                "target_cross_82bb313": 48,
            }, "the residue maximal-orbit CNF dimensions changed")
    require(D.content_hash(clauses) == EXPECTED_CNF_SHA256,
            "the residue maximal-orbit CNF changed")
    return cells, index, clauses, family_counts


def image_support(support, permutation, swap):
    site_map = dict(zip(V.RESIDUE, permutation))
    colour_map = ({0: 1, 1: 0, 2: 2} if swap
                  else {0: 0, 1: 1, 2: 2})
    return frozenset(V.cell(site_map[u], site_map[v],
                            colour_map[i], colour_map[j])
                     for u, v, i, j in support)


def canonical_support(support):
    images = [image_support(support, permutation, swap)
              for permutation in itertools.permutations(V.RESIDUE)
              for swap in (False, True)]
    return min(images, key=lambda image: tuple(sorted(image)))


def maximize_model(solver, cells):
    if not solver.solve():
        return None
    positive = {literal for literal in solver.get_model()
                if 0 < literal <= len(cells)}
    for literal in range(1, len(cells) + 1):
        if literal in positive:
            continue
        if solver.solve(assumptions=sorted(positive | {literal})):
            positive |= {value for value in solver.get_model()
                         if 0 < value <= len(cells)}
    return frozenset(cells[literal - 1] for literal in positive)


def target_line_arcs(support):
    return [[center, neighbour]
            for center in V.RESIDUE for neighbour in V.RESIDUE
            if neighbour != center
            and not any(V.cell(center, neighbour, 2, colour) in support
                        for colour in (0, 1))]


def projection_support_profile(support):
    profile = {}
    for center in V.RESIDUE:
        rows = {}
        for neighbour in V.RESIDUE:
            if neighbour == center:
                continue
            rows[str(neighbour)] = [
                [colour for colour in V.COLORS
                 if V.cell(center, neighbour, source, colour) in support]
                for source in (0, 1)
            ]
        profile[str(center)] = rows
    return profile


def enumerate_orbits(cells, index, clauses):
    residue_set = set(cells)
    solver = Solver(name="cadical195", bootstrap_with=clauses)
    orbits = []
    while True:
        support = maximize_model(solver, cells)
        if support is None:
            break
        canonical = canonical_support(support)
        require(canonical not in orbits,
                "a maximal residue orbit was enumerated twice")
        orbits.append(canonical)
        images = {
            image_support(support, permutation, swap)
            for permutation in itertools.permutations(V.RESIDUE)
            for swap in (False, True)
        }
        for image in images:
            solver.add_clause([index[cell] for cell in cells
                               if cell not in image])
    require(not solver.solve(), "the maximal-orbit blocking CNF stayed SAT")

    # Check maximality against the original CNF, not the accumulated blockers.
    base = Solver(name="cadical195", bootstrap_with=clauses)
    for support in orbits:
        assumptions = [index[cell] for cell in support]
        require(base.solve(assumptions=assumptions),
                "an enumerated residue support is not feasible")
        for cell in residue_set - set(support):
            require(not base.solve(assumptions=assumptions + [index[cell]]),
                    "an enumerated residue support is not inclusion-maximal")
    holes = {tuple(sorted(residue_set - set(support))) for support in orbits}
    require(holes == set(EXPECTED_HOLES) and len(orbits) == 6,
            "the six maximal residue orbits changed")
    return sorted(orbits, key=lambda support: tuple(sorted(support)))


def audit():
    started = monotonic()
    cells, index, clauses, family_counts = build_cnf()
    orbits = enumerate_orbits(cells, index, clauses)
    residue_set = set(cells)
    orbit_records = []
    for support in orbits:
        images = {
            image_support(support, permutation, swap)
            for permutation in itertools.permutations(V.RESIDUE)
            for swap in (False, True)
        }
        orbit_records.append({
            "support_cells": len(support),
            "holes": [list(cell) for cell in sorted(residue_set - set(support))],
            "orbit_size": len(images),
            "target_line_arcs": target_line_arcs(support),
            "non_target_projection_supports":
                projection_support_profile(support),
            "support_sha256": D.content_hash([list(cell)
                                               for cell in sorted(support)]),
        })
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "variables": len(cells),
        "clauses": len(clauses),
        "clause_families": family_counts,
        "cnf_sha256": D.content_hash(clauses),
        "symmetry": "S4 on residue sites times S2 on non-target colours",
        "maximal_orbits": orbit_records,
        "maximal_orbit_count": len(orbits),
        "maximal_support_sizes": sorted(len(support) for support in orbits),
        "exhaustiveness": (
            "every orbit downset was blocked and the residual CNF was UNSAT; "
            "each representative was independently checked inclusion-maximal"
        ),
        "status": "six inclusion-maximal residue support orbits remain",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the residue maximal-orbit ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue maximal orbits: PASS (exact)")
    print("CNF:", ledger["variables"], "vars,", ledger["clauses"], "clauses")
    print("maximal support sizes:", ledger["maximal_support_sizes"])
    print("maximal orbits:", ledger["maximal_orbit_count"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
