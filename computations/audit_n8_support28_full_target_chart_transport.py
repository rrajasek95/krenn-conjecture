#!/usr/bin/env python3
"""Full-target-chart extension of the support-28 permanent-triangle audit.

This checker fixes target support 012, exhausts the occurrence SAT models
modulo S2(target endpoints) x S6(other sites) x S3(colours), and transports
the literal three-row Laurent-unit computation from the pair-target chart.
"""

from __future__ import annotations

from collections import Counter
import importlib.util
from itertools import permutations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(name, filename):
    path = HERE / filename
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None
            and specification.loader is not None, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


BASE = load_local(
    "n8_support28_pair_target_independent",
    "audit_n8_support28_cube_cut_permanent_triangle_unit_independent.py",
)
SEMANTICS = load_local(
    "n8_global_occurrence_cnf_semantics",
    "verify_n8_global_occurrence_cnf_semantics_audit.py",
)
SOURCE = SEMANTICS.CNF_SOURCE


FULL_TARGET_SUPPORT = {
    (0, 1): (0, 1, 2),
    (0, 2): (2,),
    (0, 3): (0, 1),
    (0, 4): (0, 2),
    (0, 5): (1, 2),
    (0, 6): (1,),
    (0, 7): (0,),
    (1, 2): (0, 1),
    (1, 3): (2,),
    (1, 4): (1,),
    (1, 5): (0,),
    (1, 6): (0, 2),
    (1, 7): (1, 2),
    (2, 3): (0, 1, 2),
    (2, 4): (0,),
    (2, 5): (1,),
    (2, 6): (1, 2),
    (2, 7): (0, 2),
    (3, 4): (1, 2),
    (3, 5): (0, 2),
    (3, 6): (0,),
    (3, 7): (1,),
    (4, 5): (0, 1),
    (4, 6): (0, 1, 2),
    (4, 7): (2,),
    (5, 6): (2,),
    (5, 7): (0, 1, 2),
    (6, 7): (0, 1),
}

FULL_CUBE_BITS = {
    0: (0, 0, 0),
    1: (1, 1, 1),
    2: (0, 0, 1),
    3: (1, 1, 0),
    4: (1, 0, 1),
    5: (0, 1, 1),
    6: (0, 1, 0),
    7: (1, 0, 0),
}

EXPECTED_CANONICAL_SIGNATURE = (
    7, 1, 2, 3, 4, 5, 6,
    6, 5, 4, 3, 2, 1,
    3, 2, 5, 4, 7,
    1, 6, 7, 4,
    7, 6, 5,
    1, 2,
    3,
)


def support_signature(support):
    return tuple(sum(1 << colour for colour in support[endpoints])
                 for endpoints in SOURCE.EDGES)


def transform_support(support, vertex, colour):
    answer = {}
    for endpoints, colours in support.items():
        moved_edge = tuple(sorted(vertex[item] for item in endpoints))
        answer[moved_edge] = tuple(sorted(colour[item] for item in colours))
    return answer


def target_stabilizer_orbit():
    signatures = set()
    best = None
    best_maps = []
    for swap_endpoints in (False, True):
        for tail in permutations(range(2, 8)):
            vertex = {
                0: 1 if swap_endpoints else 0,
                1: 0 if swap_endpoints else 1,
                **dict(zip(range(2, 8), tail)),
            }
            for colour_tuple in permutations(SOURCE.COLORS):
                colour = dict(enumerate(colour_tuple))
                transformed = transform_support(
                    FULL_TARGET_SUPPORT, vertex, colour
                )
                signature = support_signature(transformed)
                signatures.add(signature)
                datum = (swap_endpoints, tail, colour_tuple)
                if best is None or signature < best:
                    best = signature
                    best_maps = [datum]
                elif signature == best:
                    best_maps.append(datum)
    require(best == EXPECTED_CANONICAL_SIGNATURE, best)
    require(len(signatures) == 720 and len(best_maps) == 12,
            (len(signatures), len(best_maps)))
    require(best_maps[0] ==
            (False, (2, 7, 4, 6, 5, 3), (1, 2, 0)), best_maps[0])
    return tuple(sorted(signatures)), best_maps[0]


def exact_orbit_exhaustion(orbit, timeout_seconds=120):
    # First replay the printed representative against every literal CNF
    # clause using the separately audited intended auxiliary assignment.
    _cnf, _values, families, violations = SEMANTICS.replay(
        FULL_TARGET_SUPPORT, 28, (0, 1, 2), 4
    )
    require(not families and violations == 0, (families, violations))

    # Then forbid every support in its true marked orbit.  UNSAT proves that
    # there is no second full-target support-28 orbit.
    cnf, y, *_rest = SOURCE.build_instance(28, (0, 1, 2), None, 4, None)
    for signature in orbit:
        clause = []
        for endpoints, bitmask in zip(SOURCE.EDGES, signature, strict=True):
            for colour in SOURCE.COLORS:
                selected = bool(bitmask & (1 << colour))
                literal = y[endpoints, colour]
                clause.append(-literal if selected else literal)
        cnf.add(*clause)
    status, _model, stdout, stderr = SOURCE.solve(cnf, timeout_seconds)
    require(status == "unsat", (status, stdout[-1000:], stderr[-1000:]))
    return len(cnf.names), len(cnf.clauses)


def coefficient_transport():
    triangles = BASE.permanent_triangles(FULL_TARGET_SUPPORT)
    colour_counts = Counter(item[0] for item in triangles)
    require(len(triangles) == 96
            and colour_counts == {0: 32, 1: 32, 2: 32},
            (len(triangles), colour_counts))
    selected = BASE.audit_selected_unit(
        triangles[0],
        FULL_TARGET_SUPPORT,
        expected_shape=(0, (0, 2), (1, 3, 4)),
        expected_words=((0, 0, 0, 0, 1, 2, 1, 2),
                        (0, 0, 0, 1, 0, 2, 2, 1),
                        (0, 1, 0, 0, 0, 2, 2, 1)),
    )
    require(selected["words"] ==
            ("00001212", "00010221", "01000221"), selected)
    return len(triangles), tuple(sorted(colour_counts.items())), selected


def main():
    require(tuple(sorted(FULL_TARGET_SUPPORT)) == SOURCE.EDGES,
            "full-target support lost a graph edge")
    require(FULL_TARGET_SUPPORT[SOURCE.TARGET_EDGE] == SOURCE.COLORS,
            FULL_TARGET_SUPPORT[SOURCE.TARGET_EDGE])
    require(Counter(map(len, FULL_TARGET_SUPPORT.values())) ==
            {1: 12, 2: 12, 3: 4},
            Counter(map(len, FULL_TARGET_SUPPORT.values())))
    for endpoints in SOURCE.EDGES:
        expected = tuple(colour for colour in SOURCE.COLORS
                         if FULL_CUBE_BITS[endpoints[0]][colour]
                         != FULL_CUBE_BITS[endpoints[1]][colour])
        require(FULL_TARGET_SUPPORT[endpoints] == expected,
                (endpoints, FULL_TARGET_SUPPORT[endpoints], expected))
    require(FULL_CUBE_BITS[0] == (0, 0, 0)
            and FULL_CUBE_BITS[1] == (1, 1, 1), FULL_CUBE_BITS)
    histogram = BASE.occurrence_histogram(FULL_TARGET_SUPPORT)
    require(histogram == ((0, 1332), (2, 204), (4, 54),
                          (6, 48), (24, 3)), histogram)

    orbit, canonical_map = target_stabilizer_orbit()
    cnf_shape = exact_orbit_exhaustion(orbit)
    triangles, triangle_colours, selected = coefficient_transport()
    print("support-28 full-target chart: ONE ORBIT, EMPTY COEFFICIENT FIBRE")
    print("target stabilizer / orbit / stabilizer", 8640, len(orbit),
          8640 // len(orbit))
    print("canonical map", canonical_map)
    print("orbit-blocked CNF variables/clauses", cnf_shape)
    print("occurrence histogram", histogram)
    print("permanent triangles", triangles, triangle_colours)
    print("selected transported unit", selected)


if __name__ == "__main__":
    main()
