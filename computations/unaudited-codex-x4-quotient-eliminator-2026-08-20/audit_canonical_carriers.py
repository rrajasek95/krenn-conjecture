#!/usr/bin/env python3
"""Canonical selected-skeleton carrier census and W40 packet readout."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CORE_SPEC = importlib.util.spec_from_file_location(
    "codex_quotient_skeleton_core", HERE / "audit_quotient_skeleton.py")
core = importlib.util.module_from_spec(CORE_SPEC)
CORE_SPEC.loader.exec_module(core)
RESULTS_PATH = HERE / "results.json"
EXPECTED_RESULTS_SHA256 = "7b61e3c5cc2422087ea6d6d2a4e393fdebfd5df88c4e6eb5805f894ab01f8162"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def mate_map(matching):
    answer = {}
    for u, v in matching:
        answer[u], answer[v] = v, u
    require(set(answer) == set(range(8)), "matching mate map")
    return answer


def occurrence_record(triple, color, pair):
    p, q = pair
    require(pair in triple[color], (color, pair, "not a selected occurrence"))
    response_edges = []
    response_details = []
    pair_shared_colors = []
    for other_color in range(3):
        if other_color == color:
            continue
        mates = mate_map(triple[other_color])
        if mates[p] == q:
            pair_shared_colors.append(other_color)
            continue
        response_edge = tuple(sorted((mates[p], mates[q])))
        response_edges.append(response_edge)
        response_details.append({
            "color": other_color,
            "edge": list(response_edge),
            "p_mate": mates[p],
            "q_mate": mates[q],
        })
    response_edges = tuple(response_edges)
    forced_edges = tuple(sorted(set(response_edges)))
    residual = tuple(site for site in range(8) if site not in (p, q))
    carrier_family = []
    if not forced_edges:
        kind = "empty"
        carrier_family.extend({"carrier_type": "star", "carrier": [center]}
                              for center in residual)
        carrier_family.extend({"carrier_type": "triangle", "carrier": list(triangle)}
                              for triangle in core.combinations(residual, 3))
    elif len(forced_edges) == 1:
        kind = "single"
        u, v = forced_edges[0]
        carrier_family.extend((
            {"carrier_type": "star", "carrier": [u]},
            {"carrier_type": "star", "carrier": [v]},
        ))
        carrier_family.extend(
            {"carrier_type": "triangle", "carrier": sorted((u, v, third))}
            for third in residual if third not in (u, v)
        )
    else:
        require(len(forced_edges) == 2, (color, pair, forced_edges))
        intersection = set(forced_edges[0]).intersection(forced_edges[1])
        if intersection:
            kind = "intersecting"
            center = next(iter(intersection))
            owners = []
            for detail in response_details:
                if detail["p_mate"] == center:
                    owners.append("p")
                elif detail["q_mate"] == center:
                    owners.append("q")
                else:
                    raise RuntimeError("intersecting response edge lost its center owner")
            star_orientation = "split" if len(set(owners)) == 2 else "same-endpoint"
            carrier_family.extend((
                {"carrier_type": "star", "carrier": [center]},
                {"carrier_type": "triangle",
                 "carrier": sorted(set(forced_edges[0] + forced_edges[1]))},
            ))
        else:
            kind = "disjoint"
            star_orientation = None
    if kind != "intersecting":
        star_orientation = None
    return {
        "color": color,
        "pair": list(pair),
        "response_edges": [list(edge) for edge in response_edges],
        "response_details": response_details,
        "forced_response_edges": [list(edge) for edge in forced_edges],
        "pair_shared_colors": pair_shared_colors,
        "kind": kind,
        "intersecting_star_orientation": star_orientation,
        "complete_forced_support_carrier_family": carrier_family,
    }


def classify_triple(triple):
    records = []
    for color, matching in enumerate(triple):
        for pair in matching:
            records.append(occurrence_record(triple, color, pair))
    require(len(records) == 12, "selected occurrence census")
    return records


def port_mate(triple):
    mate = [-1] * 24
    for color, matching in enumerate(triple):
        for u, v in matching:
            left, right = 3 * u + color, 3 * v + color
            mate[left], mate[right] = right, left
    require(all(value >= 0 for value in mate), "port matching incomplete")
    return tuple(mate)


def color_transform(mate, permutation):
    answer = [-1] * 24
    for vertex in range(8):
        for color in range(3):
            target = 3 * vertex + permutation[color]
            other_vertex, other_color = divmod(mate[3 * vertex + color], 3)
            answer[target] = 3 * other_vertex + permutation[other_color]
    return tuple(answer)


def vertex_components(mate):
    adjacency = [set() for _ in range(8)]
    for port, other in enumerate(mate):
        adjacency[port // 3].add(other // 3)
    unseen = set(range(8))
    components = []
    while unseen:
        root = min(unseen)
        component = {root}
        frontier = [root]
        while frontier:
            vertex = frontier.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    frontier.append(other)
        unseen -= component
        components.append(component)
    return tuple(components)


def rooted_component_code(mate, component, root):
    order = [root]
    labels = {root: 0}
    for vertex in order:
        for color in range(3):
            other_vertex = mate[3 * vertex + color] // 3
            if other_vertex not in labels:
                labels[other_vertex] = len(order)
                order.append(other_vertex)
    require(set(order) == component, "rooted component traversal")
    code = []
    for vertex in order:
        for color in range(3):
            other_vertex, other_color = divmod(mate[3 * vertex + color], 3)
            code.append(3 * labels[other_vertex] + other_color)
    return tuple(code)


def legacy_canonical_key(triple):
    """Independently reproduce the legacy sorted 31-chart key."""
    mate = port_mate(triple)
    candidates = []
    for color_perm in permutations(range(3)):
        transformed = color_transform(mate, color_perm)
        components = tuple(sorted(
            min(rooted_component_code(transformed, component, root)
                for root in component)
            for component in vertex_components(transformed)
        ))
        candidates.append(components)
    return min(candidates)


def permutation_covariance(triple):
    transforms = [
        ((1, 0, 2, 3, 4, 5, 6, 7), (0, 1, 2)),
        ((1, 2, 3, 4, 5, 6, 7, 0), (0, 1, 2)),
        ((0, 1, 2, 3, 4, 5, 6, 7), (1, 0, 2)),
        ((0, 1, 2, 3, 4, 5, 6, 7), (1, 2, 0)),
    ]
    original = classify_triple(triple)
    for site_perm, color_perm in transforms:
        transformed = [None] * 3
        for color, matching in enumerate(triple):
            new_color = color_perm[color]
            transformed[new_color] = tuple(sorted(
                (min(site_perm[u], site_perm[v]), max(site_perm[u], site_perm[v]))
                for u, v in matching
            ))
        transformed_records = {
            (record["color"], tuple(record["pair"])): record
            for record in classify_triple(tuple(transformed))
        }
        for record in original:
            new_color = color_perm[record["color"]]
            new_pair = tuple(sorted(site_perm[site] for site in record["pair"]))
            image = transformed_records[new_color, new_pair]
            forced_edges = sorted(
                tuple(sorted(site_perm[site] for site in edge))
                for edge in record["forced_response_edges"]
            )
            response_edges = sorted(
                tuple(sorted(site_perm[site] for site in edge))
                for edge in record["response_edges"]
            )
            carrier_family = sorted(
                (member["carrier_type"],
                 tuple(sorted(site_perm[site] for site in member["carrier"])))
                for member in record["complete_forced_support_carrier_family"]
            )
            image_family = sorted(
                (member["carrier_type"], tuple(member["carrier"]))
                for member in image["complete_forced_support_carrier_family"]
            )
            require(image["kind"] == record["kind"],
                    "canonical occurrence type is not covariant")
            require(sorted(map(tuple, image["forced_response_edges"])) == forced_edges,
                    "forced response edges are not covariant")
            require(sorted(map(tuple, image["response_edges"])) == response_edges,
                    "response-edge multiplicity is not covariant")
            require(image_family == carrier_family,
                    "complete forced carrier family is not covariant")
            require(sorted(image["pair_shared_colors"])
                    == sorted(color_perm[color]
                              for color in record["pair_shared_colors"]),
                    "shared-pair colour record is not covariant")
            require(image["intersecting_star_orientation"]
                    == record["intersecting_star_orientation"],
                    "split/same-endpoint orientation is not covariant")
    return len(transforms) * 12


def carrier_row_data(source, p, q, carrier_type, carrier):
    residual = tuple(site for site in range(8) if site not in (p, q))
    if carrier_type == "star":
        center = carrier[0]
        forbidden = tuple(edge for edge in core.combinations(residual, 2)
                          if center not in edge)
    else:
        triangle_edges = set(core.combinations(tuple(carrier), 2))
        forbidden = tuple(edge for edge in core.combinations(residual, 2)
                          if edge not in triangle_edges)
    rows = [row for edge in forbidden
            for row in core.response_block(source, p, q, *edge)]
    rowspace, _ = core.rref(rows)
    quotient = core.nullspace(rowspace)
    activities = core.activity_rows(source, p, q)
    restrictions = tuple(core.restrict(row, quotient) for row in activities)
    blocked = tuple(not any(row) for row in restrictions)
    return rowspace, quotient, blocked, not any(blocked)


def packet_projection(source, p, q, carrier_type, carrier, quotient):
    residual = tuple(site for site in range(8) if site not in (p, q))
    if carrier_type == "star":
        center = carrier[0]
        allowed = tuple(edge for edge in core.combinations(residual, 2)
                        if center in edge)
    else:
        allowed = tuple(core.combinations(tuple(carrier), 2))
    atomic = {edge: core.response_block(source, p, q, *edge)
              for edge in core.combinations(residual, 2)}
    activities = core.activity_rows(source, p, q)
    defects = Counter()
    examples = []
    for values in product(range(3), repeat=6):
        word = [None] * 8
        for site, color in zip(residual, values):
            word[site] = color
        target = [Fraction(0)] * 9
        if len(set(values)) == 1:
            target[3 * values[0] + values[0]] = 1
        h6 = core.hafnian(source, word, residual)
        rhs = [h6 * value for value in activities[3]]
        for a, b in allowed:
            rest = tuple(site for site in residual if site not in (a, b))
            h4 = core.hafnian(source, word, rest)
            row = atomic[a, b][3 * word[a] + word[b]]
            rhs = [x + h4 * y for x, y in zip(rhs, row)]
        defect = core.restrict(tuple(x - y for x, y in zip(target, rhs)), quotient)
        shell = "x4" if max(values.count(color) for color in range(3)) >= 4 else "full-only"
        if any(defect):
            defects[shell] += 1
            if len(examples) < 12:
                examples.append({
                    "residual_word": "".join(map(str, values)),
                    "shell": shell,
                    "defect": [str(value) for value in defect],
                })
    return dict(defects), examples


def source_triple(source):
    lives = core.pure_live_matchings(source)
    require([len(items) for items in lives] == [1, 1, 1],
            "W40 selected matching uniqueness")
    return tuple(items[0] for items in lives)


def w40_readout(source):
    triple = source_triple(source)
    occurrence_records = classify_triple(triple)
    block_size_histogram = dict(sorted(Counter(
        sum(bool(value) for matrix_row in source[edge] for value in matrix_row)
        for edge in core.EDGES
    ).items()))
    rows = []
    for occurrence in occurrence_records:
        p, q = occurrence["pair"]
        for family_member in occurrence["complete_forced_support_carrier_family"]:
            carrier_type = family_member["carrier_type"]
            carrier = family_member["carrier"]
            rowspace, quotient, blocked, active = carrier_row_data(
                source, p, q, carrier_type, carrier)
            defects, examples = packet_projection(
                source, p, q, carrier_type, carrier, quotient)
            rows.append({
                **occurrence,
                "chosen_carrier_type": carrier_type,
                "chosen_carrier": carrier,
                "rank": len(rowspace),
                "quotient_dimension": len(quotient),
                "activity_in_rowspace": list(blocked),
                "active": active,
                "packet_defects": defects,
                "first_packet_defects": examples,
            })
    return {
        "occurrence_histogram": dict(sorted(Counter(
            record["kind"] for record in occurrence_records).items())),
        "physical_block_support_size_histogram": block_size_histogram,
        "full_3_by_3_blocks": block_size_histogram.get(9, 0),
        "canonical_intersecting_stars": rows,
        "active_count": sum(record["active"] for record in rows),
        "full_only_projected_defects": sum(
            record["packet_defects"].get("full-only", 0) for record in rows),
    }


def main():
    results_sha = sha256(RESULTS_PATH.read_bytes()).hexdigest()
    require(results_sha == EXPECTED_RESULTS_SHA256,
            ("quotient result changed", results_sha))
    upstream = json.loads(RESULTS_PATH.read_text())
    orbit_records = []
    covariance_checks = 0
    triples_by_orbit = {}
    legacy_keys = {}
    for record in upstream["pure_matching_orbits"]["records"]:
        triple = tuple(tuple(tuple(edge) for edge in matching)
                       for matching in record["representative"])
        triples_by_orbit[record["orbit"]] = triple
        legacy_keys[record["orbit"]] = legacy_canonical_key(triple)
    sorted_legacy_keys = sorted(set(legacy_keys.values()))
    require(len(sorted_legacy_keys) == 31, "legacy chart key count")
    legacy_chart = {orbit: sorted_legacy_keys.index(key) + 1
                    for orbit, key in legacy_keys.items()}

    for record in upstream["pure_matching_orbits"]["records"]:
        triple = triples_by_orbit[record["orbit"]]
        occurrences = classify_triple(triple)
        histogram = dict(sorted(Counter(item["kind"] for item in occurrences).items()))
        orientation_histogram = dict(sorted(Counter(
            item["intersecting_star_orientation"] for item in occurrences
            if item["kind"] == "intersecting"
        ).items()))
        covariance_checks += permutation_covariance(triple)
        orbit_records.append({
            "orbit": record["orbit"],
            "legacy_one_based_chart": legacy_chart[record["orbit"]],
            "orbit_size": record["orbit_size"],
            "type_histogram": histogram,
            "intersecting_orientation_histogram": orientation_histogram,
            "occurrences": occurrences,
        })

    all_disjoint = [record["orbit"] for record in orbit_records
                    if record["type_histogram"] == {"disjoint": 12}]
    require(all_disjoint == [25, 26, 27, 28], all_disjoint)
    require([legacy_chart[orbit] for orbit in all_disjoint] == [28, 29, 30, 31],
            {orbit: legacy_chart[orbit] for orbit in all_disjoint})
    require(orbit_records[24]["type_histogram"]
            == {"disjoint": 2, "intersecting": 8, "single": 2}, orbit_records[24])
    split_spoke_orbits = [record["orbit"] for record in orbit_records
                          if record["intersecting_orientation_histogram"].get("split", 0)]
    require(split_spoke_orbits == [7, 11, 14, 17, 18, 19, 20, 24, 29, 30],
            split_spoke_orbits)

    w40, _w25 = core.load_sources()
    w40_result = w40_readout(w40)
    require(w40_result["occurrence_histogram"]
            == {"disjoint": 2, "intersecting": 8, "single": 2}, w40_result)
    require(w40_result["active_count"] == 6, w40_result)
    require(w40_result["physical_block_support_size_histogram"]
            == {0: 11, 1: 14, 2: 3}, w40_result)
    require(w40_result["full_3_by_3_blocks"] == 0, w40_result)
    require(all(not row["packet_defects"].get("x4", 0)
                for row in w40_result["canonical_intersecting_stars"]),
            "W40 canonical carrier acquired an X4 packet defect")

    result = {
        "schema": "codex.x4_canonical_carriers.v2",
        "status": "PASS",
        "scope": "selected-skeleton carrier census and exact W40 packet calibration; no universal contradiction",
        "quotient_results_sha256": results_sha,
        "theorem": {
            "definition": (
                "For selected occurrence (color c,pair pq), the other two pure "
                "matchings induce zero, one, or two residual response edges. "
                "Two distinct intersecting edges define their unique minimal "
                "star and three-vertex containing triangle. Coincident edges "
                "define two endpoint stars and four containing triangles; no "
                "canonical endpoint may be chosen without extra data. Disjoint "
                "edges do not define a containing clean carrier and remain a separate case."
            ),
            "all_disjoint_orbits": all_disjoint,
            "all_disjoint_legacy_charts": [legacy_chart[orbit]
                                            for orbit in all_disjoint],
            "non_disjoint_orbits": [record["orbit"] for record in orbit_records
                                    if record["type_histogram"] != {"disjoint": 12}],
            "split_spoke_orbits": split_spoke_orbits,
            "two_spoke_cramer_template": (
                "At a split-spoke star, a three-row X4 packet varying the "
                "centre colour and having exactly two effective arm cofactors "
                "plus one live singleton spike forces the complementary 2x2 "
                "arm minor to vanish. A second packet at another spike colour "
                "and the same endpoint-colour key gives a five-row Laurent unit. "
                "This is a proved local template, not universal packet entry."
            ),
            "smallest_failed_bridge_lemma": (
                "A split canonical-star occurrence does not imply entry into "
                "the two-column five-row packet: W40 has eight split "
                "occurrences, but its physical block support-size histogram "
                "is 0:11, 1:14, 2:3, so it has no full 3-by-3 block and hence "
                "cannot have the template's two effective full neighbours. "
                "The carrier census supplies forced pure response edges, not "
                "the compatible singleton spikes and cofactor isolation."
            ),
        },
        "orbit_records": orbit_records,
        "W40": w40_result,
        "controls": {
            "site_color_covariance_checks": covariance_checks,
            "W40_x4_projected_packet_defects": sum(
                row["packet_defects"].get("x4", 0)
                for row in w40_result["canonical_intersecting_stars"]),
            "W40_split_occurrences_without_full_blocks": 8,
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "canonical_carriers.json").write_text(payload)
    print(json.dumps({
        "status": result["status"],
        "all_disjoint_orbits": all_disjoint,
        "W40_active_canonical_stars": w40_result["active_count"],
        "W40_full_only_projected_defects": w40_result["full_only_projected_defects"],
        "sha256": sha256(payload.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
