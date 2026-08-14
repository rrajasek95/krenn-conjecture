#!/usr/bin/env python3
"""Extend the private-factor landing to every complete cap response.

The original directed-incidence register marked a block private only in the
minimum two-RRX face that created the register.  This checker reopens every
literal cap response.  If all expanded monomials of one cap contain the
chosen directed nonanchor X, a left- or right-kernel cap covector kills the
whole response.  For every noncoordinate ternary vector w the covector can
be chosen with all three diagonal readouts nonzero.

This complete-response criterion lands 110 further stabilizer orbits (153
directed incidences) among the 259 anchor-completion guards.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "e9b172fd703bad9380afd357edd9978f5288fc580b91832f492b64266b48d227"
COLORS = (0, 1, 2)


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


PROTOTYPE = load_local(
    "n8_support16_prototype_for_complete_private_extension",
    "verify_n8_support16_two_cap_prototype_orbit_extension.py",
)
ORBIT = PROTOTYPE.ORBIT
LANDING = PROTOTYPE.LANDING


def active_kernel_matrix(support, side):
    """Construct K with diagonal units and w^T K=0 or K w=0.

    The construction is denominator-free on the chart where exactly the
    listed w coordinates are certified nonzero.  For each column j choose a
    pivot p_j in support distinct from j when necessary, then put

        K_jj = w_pj,   K_pj,j = -w_j.

    Transposition gives the right-kernel version.
    """
    support = tuple(sorted(support))
    require(len(support) >= 2, ("kernel chart is coordinate", support))
    w = tuple(
        LANDING.variable(index) if index in support else LANDING.zero()
        for index in COLORS
    )
    matrix = [[LANDING.zero() for _column in COLORS] for _row in COLORS]
    pivots = []
    for column in COLORS:
        pivot = next(index for index in support if index != column)
        pivots.append(pivot)
        matrix[column][column] = w[pivot]
        matrix[pivot][column] = LANDING.add(
            matrix[pivot][column], LANDING.scale(w[column], -1)
        )

    if side == "right":
        matrix = [list(row) for row in zip(*matrix)]
    require(side in ("left", "right"), ("bad kernel side", side))
    if side == "left":
        kernel = tuple(
            LANDING.add(*(LANDING.multiply(w[row], matrix[row][column])
                          for row in COLORS))
            for column in COLORS
        )
    else:
        kernel = tuple(
            LANDING.add(*(LANDING.multiply(matrix[row][column], w[column])
                          for column in COLORS))
            for row in COLORS
        )
    require(kernel == (LANDING.zero(),) * 3,
            ("private cap kernel did not vanish", support, side, kernel))
    diagonal = tuple(matrix[index][index] for index in COLORS)
    require(diagonal == tuple(w[pivot] for pivot in pivots),
            ("private cap diagonal changed", support, side, diagonal,
             pivots))
    require(all(entry != LANDING.zero() for entry in diagonal),
            ("private cap lost active diagonal", support, side, diagonal))
    return {
        "support": support,
        "side": side,
        "pivots": tuple(pivots),
        "matrix": tuple(tuple(row) for row in matrix),
        "kernel": kernel,
        "diagonal": diagonal,
    }


def audit_kernel_charts():
    ledgers = []
    for size in (2, 3):
        for support in combinations(COLORS, size):
            for side in ("left", "right"):
                ledgers.append(active_kernel_matrix(support, side))
    require(len(ledgers) == 8,
            ("noncoordinate kernel chart count changed", len(ledgers)))
    return tuple(ledgers)


def audit_complete_private_faces():
    terminal_records = ORBIT.terminal_two_rrx_records()
    # The dependency's finite graph census is deterministic but expensive;
    # reuse its exact records throughout this additive audit.
    ORBIT.terminal_two_rrx_records = lambda: terminal_records
    prototype_audit = PROTOTYPE.audit_all_orbits()
    route_orbits = Counter()
    route_incidences = Counter()
    private_role_degree_orbits = Counter()
    private_role_degree_incidences = Counter()
    private_face_count = Counter()
    private_through_count = Counter()
    private_ledgers = []
    unresolved_prototype_count = Counter()

    for item in prototype_audit["graph_ledgers"]:
        incidence = item["incidence"]
        if item["route"] == "forced-distinct-two-cap":
            route = "forced-distinct-two-cap"
        elif item["private_face_count"]:
            route = "complete-private-cap"
        elif len(item["prototype_faces"]) >= 2:
            route = "pure-normalization-collision-exit"
        else:
            route = "unresolved-at-most-one-prototype"
            unresolved_prototype_count[len(item["prototype_faces"])] += 1

        route_orbits[route] += 1
        route_incidences[route] += item["orbit_size"]
        if route != "complete-private-cap":
            continue

        record = terminal_records[item["graph_index"]]
        edges = tuple(record["representative_edges"])
        adjacency = ORBIT.adjacency_from_edges(edges)
        private_faces = []
        for cap_edge, through_count, residue_count in (
                item["all_source_response_shapes"]):
            if residue_count:
                continue
            expanded = ORBIT.expanded_response_monomials(
                adjacency, edges, cap_edge
            )
            require(len(expanded) == through_count,
                    ("private response expanded count changed",
                     item["graph_index"], incidence, cap_edge,
                     len(expanded), through_count))
            require(all(ORBIT.contains_directed_star(term, incidence)
                        for term in expanded),
                    ("zero-residue face lost literal privacy",
                     item["graph_index"], incidence, cap_edge))
            endpoint = incidence[0]
            require(endpoint in cap_edge,
                    ("private face does not contain endpoint", incidence,
                     cap_edge))
            side = "left" if cap_edge[0] == endpoint else "right"
            private_faces.append({
                "cap_edge": cap_edge,
                "kernel_side": side,
                "expanded_through_count": through_count,
                "factor_level_terms": tuple(
                    ORBIT.monomial_names(term)
                    for term in ORBIT.response_terms(
                        adjacency, edges, cap_edge
                    )
                ),
            })
            private_through_count[through_count] += 1

        require(len(private_faces) == item["private_face_count"],
                ("complete private face count changed", item, private_faces))
        private_face_count[len(private_faces)] += 1
        role_degree = (item["role"], item["near_degree"])
        private_role_degree_orbits[role_degree] += 1
        private_role_degree_incidences[role_degree] += item["orbit_size"]
        private_ledgers.append({
            "graph_index": item["graph_index"],
            "orbit_size": item["orbit_size"],
            "incidence": incidence,
            "role": item["role"],
            "near_degree": item["near_degree"],
            "private_faces": tuple(private_faces),
        })

    require(route_orbits == Counter({
        "forced-distinct-two-cap": 22,
        "complete-private-cap": 110,
        "pure-normalization-collision-exit": 1,
        "unresolved-at-most-one-prototype": 148,
    }), ("complete-private orbit partition changed", route_orbits))
    require(route_incidences == Counter({
        "forced-distinct-two-cap": 25,
        "complete-private-cap": 153,
        "pure-normalization-collision-exit": 1,
        "unresolved-at-most-one-prototype": 197,
    }), ("complete-private incidence partition changed", route_incidences))
    require(private_face_count == Counter({1: 105, 2: 5}),
            ("private faces per orbit changed", private_face_count))
    require(private_through_count == Counter({
        4: 52, 6: 23, 8: 20, 2: 19, 10: 1,
    }), ("private face size histogram changed", private_through_count))
    require(unresolved_prototype_count == Counter({0: 85, 1: 63}),
            ("final prototype split changed", unresolved_prototype_count))

    return {
        "route_orbits": tuple(sorted(route_orbits.items())),
        "route_incidences": tuple(sorted(route_incidences.items())),
        "private_faces_per_orbit": tuple(sorted(private_face_count.items())),
        "private_face_expanded_size": tuple(
            sorted(private_through_count.items())
        ),
        "private_role_degree_orbits": tuple(
            sorted(private_role_degree_orbits.items())
        ),
        "private_role_degree_incidences": tuple(
            sorted(private_role_degree_incidences.items())
        ),
        "unresolved_prototype_count": tuple(
            sorted(unresolved_prototype_count.items())
        ),
        "private_face_ledgers": tuple(private_ledgers),
        "uniform_criterion": (
            "if every expanded monomial of a physical cap response contains "
            "the same directed noncoordinate source-star block X, then a "
            "left/right kernel covector annihilates the complete response "
            "while retaining all three diagonal cap readouts"
        ),
        "support_scope": (
            "the criterion is not special to support 16 and remains valid "
            "at arbitrary support; only the finite counts use this census"
        ),
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
    ledger = canonical({
        "kernel_charts": audit_kernel_charts(),
        "complete_private_census": audit_complete_private_faces(),
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("complete private cap ledger changed", digest))

    print("N=8 support-16 complete private-cap extension: PASS")
    print("  private active-clean exits: 110 orbits / 153 incidences")
    print("  remaining: 148 orbits / 197 incidences")
    print("  remaining zero/one-prototype split: 85 / 63")
    print("  noncoordinate left/right kernel charts: 8")


if __name__ == "__main__":
    main()
