#!/usr/bin/env python3
"""Exact rational join of the 19,528 named W33 binary-source records.

Each ternary X4 source has three exact binary faces.  This bounded census
asks whether three *stored* W33 binary sources can share their diagonal
colour layers, allowing target-preserving diagonal site-colour gauges.  It
then assembles every compatible rational triple and evaluates raw X4 rows.

The W33 pools are experimental inventories, not an exhaustive binary-source
classification.  Consequently a no-hit result is a precise finite-pool
terminal only, never evidence for universal X4-to-cap.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESPONSE_DIR = ROOT / "computations/unaudited-codex-response-star-2026-08-20"
sys.path.insert(0, str(RESPONSE_DIR))
from response_star_core import (  # noqa: E402
    response_star_record, response_triangle_record, source_from_json_blocks,
)


POOL_PATHS = (
    ROOT / "computations/unaudited-x4general-w33-2026-08-20/results_t2_A.json",
    ROOT / "computations/unaudited-x4general-w33-2026-08-20/results_t2_B.json",
)
W40_PATH = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
W25_PATH = ROOT / "computations/unaudited-x3core-w25-2026-08-15/OBJECT_W25-F8_n8_allblocked_X3.json"
PINNED = {
    POOL_PATHS[0]: "5aa7581537b76c803fd934b1c0fca97b2c99a2fb3168e9ecea8cf9e3b9db67f7",
    POOL_PATHS[1]: "93df3f43e0c95c60d339058d986e73b7700dcf856430edc696a4bd0e643b9f48",
    W40_PATH: "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    W25_PATH: "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}
SITES = tuple(range(8))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


PMS = tuple(perfect_matchings(SITES))


def empty_source(ncolors=3):
    return {edge: [[Fraction(0) for _ in range(ncolors)]
                   for _ in range(ncolors)] for edge in EDGES}


def cell(source, u, v, a, b):
    return source[(u, v)][a][b] if u < v else source[(v, u)][b][a]


def hafnian(source, word):
    total = Fraction(0)
    for matching in PMS:
        term = Fraction(1)
        for u, v in matching:
            term *= cell(source, u, v, word[u], word[v])
            if not term:
                break
        total += term
    return total


def off_count(word):
    return 8 - max(word.count(c) for c in COLORS)


def raw_profile(source, max_off=4):
    defects = Counter()
    rows = []
    for word in product(COLORS, repeat=8):
        word = tuple(word)
        off = off_count(word)
        if off > max_off:
            continue
        value = hafnian(source, word)
        target = Fraction(int(len(set(word)) == 1))
        if value != target:
            defects[off] += 1
            rows.append({"word": "".join(map(str, word)),
                         "value": str(value), "target": str(target)})
    return dict(sorted(defects.items())), rows


def singleton_332_words(source):
    occupied = {
        (u, v, i, j) for u, v in EDGES for i in COLORS for j in COLORS
        if source[(u, v)][i][j]
    }
    answer = []
    for word in product(COLORS, repeat=8):
        if sorted(Counter(word).values()) != [2, 3, 3]:
            continue
        count = 0
        for matching in PMS:
            if all((u, v, word[u], word[v]) in occupied for u, v in matching):
                count += 1
        if count == 1:
            answer.append("".join(map(str, word)))
    return answer


def singleton_x4_words(source):
    occupied = {
        (u, v, i, j) for u, v in EDGES for i in COLORS for j in COLORS
        if source[(u, v)][i][j]
    }
    answer = []
    for word in product(COLORS, repeat=8):
        word = tuple(word)
        if len(set(word)) == 1 or off_count(word) > 4:
            continue
        count = sum(
            all((u, v, word[u], word[v]) in occupied for u, v in matching)
            for matching in PMS
        )
        if count == 1:
            answer.append("".join(map(str, word)))
    return answer


def record_matrix(record, edge):
    raw = record["cells"].get(f"{edge[0]}{edge[1]}", (("0", "0"), ("0", "0")))
    return [[Fraction(raw[i][j]) for j in range(2)] for i in range(2)]


def oriented_face(record, swapped):
    face = {edge: [[Fraction(0), Fraction(0)] for _ in range(2)] for edge in EDGES}
    for edge in EDGES:
        matrix = record_matrix(record, edge)
        if swapped:
            matrix = [[matrix[1][1], matrix[1][0]],
                      [matrix[0][1], matrix[0][0]]]
        face[edge] = matrix
    return face


def layer(face, color):
    return tuple(face[edge][color][color] for edge in EDGES)


def support(layer_values):
    return tuple(edge for edge, value in zip(EDGES, layer_values) if value)


def gauge_to(target, source):
    """Return rational g with g_u*g_v*source_uv=target_uv.

    The named compatible triples all have the forced square parameter t^2=1,
    so choosing t=1 is rational.  The general Qbar graph test is nevertheless
    implemented and rejects inconsistent cycle ratios explicitly.
    """
    require(support(target) == support(source), "gauge support mismatch")
    adjacency = defaultdict(list)
    for edge, left, right in zip(EDGES, target, source):
        if not left:
            continue
        ratio = left / right
        u, v = edge
        adjacency[u].append((v, ratio))
        adjacency[v].append((u, ratio))
    forms = {}
    component_t2 = []
    for root in SITES:
        if root in forms or root not in adjacency:
            continue
        forms[root] = (Fraction(1), 1)
        stack = [root]
        t2 = None
        while stack:
            u = stack.pop()
            cu, pu = forms[u]
            for v, ratio in adjacency[u]:
                cv, pv = ratio / cu, -pu
                if v not in forms:
                    forms[v] = (cv, pv)
                    stack.append(v)
                    continue
                oldc, oldp = forms[v]
                if pv == oldp:
                    require(cv == oldc, "non-gauge-equivalent cycle ratio")
                else:
                    candidate = oldc / cv if pv == 1 else cv / oldc
                    if t2 is None:
                        t2 = candidate
                    else:
                        require(t2 == candidate, "incompatible odd-cycle square")
        component_t2.append(Fraction(1) if t2 is None else t2)
    require(all(value == 1 for value in component_t2),
            f"compatible pool join unexpectedly needs algebraic square roots: {component_t2}")
    gauge = [Fraction(1)] * 8
    for vertex, (coefficient, parity) in forms.items():
        gauge[vertex] = coefficient  # t=1, independent of parity
    for edge, left, right in zip(EDGES, target, source):
        if left:
            require(gauge[edge[0]] * gauge[edge[1]] * right == left,
                    "constructed gauge does not align layer")
    return tuple(gauge)


def gauge_face(face, gauges):
    answer = {edge: [[Fraction(0), Fraction(0)] for _ in range(2)] for edge in EDGES}
    for u, v in EDGES:
        for i in range(2):
            for j in range(2):
                answer[(u, v)][i][j] = (
                    gauges[i][u] * gauges[j][v] * face[(u, v)][i][j]
                )
    return answer


def assemble(face_ab, face_ac, face_bc):
    answer = empty_source()
    for edge in EDGES:
        answer[edge][0][0] = face_ab[edge][0][0]
        answer[edge][1][1] = face_ab[edge][1][1]
        answer[edge][2][2] = face_ac[edge][1][1]
        answer[edge][0][1], answer[edge][1][0] = face_ab[edge][0][1], face_ab[edge][1][0]
        answer[edge][0][2], answer[edge][2][0] = face_ac[edge][0][1], face_ac[edge][1][0]
        answer[edge][1][2], answer[edge][2][1] = face_bc[edge][0][1], face_bc[edge][1][0]
    return answer


def source_key(source):
    return tuple(cell(source, u, v, i, j) for u, v in EDGES for i in COLORS for j in COLORS)


def carrier_profile(source):
    star_passes, triangle_passes = [], []
    for p, q in EDGES:
        residual = tuple(v for v in SITES if v not in (p, q))
        for center in residual:
            rec = response_star_record(source, p, q, center)
            if rec["passes"]:
                star_passes.append({"pair": [p, q], "center": center,
                                    "rank": rec["rank"]})
        for triangle in combinations(residual, 3):
            rec = response_triangle_record(source, p, q, triangle)
            if rec["passes"]:
                triangle_passes.append({"pair": [p, q],
                                        "triangle": list(triangle),
                                        "rank": rec["rank"]})
    return star_passes, triangle_passes


def w40_source():
    record = json.loads(W40_PATH.read_text())
    return source_from_json_blocks(record["engine_audit"]["witness_B_integral"]["source"])


def w25_source():
    record = json.loads(W25_PATH.read_text())
    return source_from_json_blocks(record["blocks"])


def main():
    for path, expected in PINNED.items():
        require(digest(path) == expected, f"pinned input changed: {path}")
    pools = []
    pool_sizes = []
    for path in POOL_PATHS:
        records = json.loads(path.read_text())["pool"]
        pool_sizes.append(len(records))
        pools.extend(records)
    require(pool_sizes == [9751, 9777], pool_sizes)

    directed = defaultdict(list)
    for index, record in enumerate(pools):
        for swapped in (False, True):
            face = oriented_face(record, swapped)
            left, right = layer(face, 0), layer(face, 1)
            directed[(support(left), support(right))].append({
                "index": index, "swapped": swapped, "face": face,
                "left": left, "right": right,
            })
    vertices = set(item for edge in directed for item in edge)
    adjacency = defaultdict(set)
    for left, right in directed:
        adjacency[left].add(right)
    layer_triangles = sorted(
        (a, b, c) for a in vertices for b in adjacency[a]
        for c in adjacency[a].intersection(adjacency[b]) if (b, c) in directed
    )
    require(len(layer_triangles) == 12, len(layer_triangles))

    assembled = []
    raw_combinations = 0
    for a, b, c in layer_triangles:
        for ab in directed[a, b]:
            for ac0 in directed[a, c]:
                for bc0 in directed[b, c]:
                    raw_combinations += 1
                    try:
                        ga = gauge_to(ab["left"], ac0["left"])
                        gb = gauge_to(ab["right"], bc0["left"])
                        # First align AC's A layer and leave its C layer as the
                        # global C target; then align both layers of BC.
                        ac = gauge_face(ac0["face"], (ga, (Fraction(1),) * 8))
                        gc = gauge_to(layer(ac, 1), bc0["right"])
                        bc = gauge_face(bc0["face"], (gb, gc))
                    except RuntimeError:
                        continue
                    source = assemble(ab["face"], ac, bc)
                    assembled.append({
                        "records": [[ab["index"], ab["swapped"]],
                                    [ac0["index"], ac0["swapped"]],
                                    [bc0["index"], bc0["swapped"]]],
                        "source": source,
                    })
    require(raw_combinations == 42, raw_combinations)
    require(len(assembled) == 42, len(assembled))

    unique = {}
    for record in assembled:
        unique.setdefault(source_key(record["source"]), record)
    profiles = []
    hits = []
    unique_records = list(unique.values())
    for record in unique_records:
        defects, defect_rows = raw_profile(record["source"], 4)
        x4_singletons = singleton_x4_words(record["source"])
        row = {"records": record["records"], "X4_defects": defects,
               "defect_rows": defect_rows,
               "X4_singleton_words": x4_singletons,
               "singleton_332_words": singleton_332_words(record["source"]),
               "occupied_cells": sum(bool(x) for x in source_key(record["source"]))}
        profiles.append(row)
        if not defects:
            stars, triangles = carrier_profile(record["source"])
            row["carrier_passes"] = {"stars": stars, "triangles": triangles}
            hits.append(row)

    # Quotient the 36 coefficient points by literal occupied-cell support.
    support_groups = defaultdict(list)
    for index, record in enumerate(unique_records):
        support_groups[tuple(bool(x) for x in source_key(record["source"]))].append(index)
    support_strata = []
    for support_mask, indices in support_groups.items():
        singleton_lists = {tuple(profiles[index]["X4_singleton_words"])
                           for index in indices}
        require(len(singleton_lists) == 1, "singleton list changed on fixed support")
        singletons = list(next(iter(singleton_lists)))
        support_strata.append({
            "occupied_cells": sum(support_mask),
            "coefficient_source_indices": indices,
            "X4_singleton_words": singletons,
            "open_support_X4_obstructed": bool(singletons),
        })
    require(all(row["open_support_X4_obstructed"] for row in support_strata),
            "a named support stratum needs coefficient-ideal elimination")

    # A compact literal row cover for this finite census.  This is not a
    # source-ideal certificate; it records which raw equations kill every
    # assembled named point.
    coverage = defaultdict(set)
    for index, row in enumerate(profiles):
        for defect in row["defect_rows"]:
            coverage[defect["word"]].add(index)
    uncovered = set(range(len(profiles)))
    greedy_cover = []
    while uncovered:
        word = max(coverage, key=lambda key: (len(coverage[key] & uncovered), key))
        newly = coverage[word] & uncovered
        require(newly, "finite row cover stalled")
        greedy_cover.append({"word": word, "source_indices": sorted(newly)})
        uncovered -= newly

    # Mandatory external controls, independently rebuilt from pinned blocks.
    w40 = w40_source()
    w25 = w25_source()
    w40_defects, _ = raw_profile(w40, 4)
    w25_defects, _ = raw_profile(w25, 4)
    require(not w40_defects, w40_defects)
    require(w25_defects == {4: 78}, w25_defects)
    w40_singletons = singleton_332_words(w40)
    w25_singletons = singleton_332_words(w25)
    require(len(w40_singletons) == 3, w40_singletons)
    require(len(w25_singletons) == 20, len(w25_singletons))
    stars40, triangles40 = carrier_profile(w40)
    stars25, triangles25 = carrier_profile(w25)
    require(len(stars40) == 6 and not triangles40, (stars40, triangles40))
    require(not stars25 and not triangles25, (stars25, triangles25))

    controls = {
        "pinned_inputs": True,
        "pool_sizes": pool_sizes,
        "directed_support_edges": len(directed),
        "support_layer_vertices": len(vertices),
        "support_layer_triangles": len(layer_triangles),
        "raw_compatible_record_triples": raw_combinations,
        "rational_gauge_compatible_triples": len(assembled),
        "unique_assembled_sources": len(unique),
        "unique_occupied_support_strata": len(support_strata),
        "all_support_strata_have_X4_singleton": all(
            row["open_support_X4_obstructed"] for row in support_strata
        ),
        "W40": {"X4_defects": w40_defects, "star_passes": len(stars40),
                 "triangle_passes": len(triangles40),
                 "singleton_332_count": len(w40_singletons)},
        "W25": {"X4_defects": w25_defects, "star_passes": len(stars25),
                 "triangle_passes": len(triangles25),
                 "singleton_332_count": len(w25_singletons)},
    }
    result = {
        "status": "UNAUDITED_EXACT_FINITE_POOL_CENSUS",
        "scope": "literal diagonal-support joins among the 19,528 pinned W33 records, allowing exact rational diagonal gauges",
        "scope_warning": "The W33 inventories are not exhaustive; zero hits is not evidence for universal X4-to-cap.",
        "controls": controls,
        "assembled_profiles": profiles,
        "support_strata": support_strata,
        "greedy_raw_X4_row_cover": greedy_cover,
        "X4_hits": hits,
        "verdict": ("NO X4 SOURCE IN THE NAMED BINARY-POOL JOIN" if not hits
                    else f"{len(hits)} X4 SOURCES; carrier status recorded"),
    }
    (HERE / "results_binary_pool_join.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print("POOL JOIN:", len(unique), "unique assembled; X4 hits", len(hits))
    print("CONTROLS: W40 stars", len(stars40), "W25 passes", len(stars25) + len(triangles25))


if __name__ == "__main__":
    main()
