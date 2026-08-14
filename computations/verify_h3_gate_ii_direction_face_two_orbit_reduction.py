#!/usr/bin/env python3
"""Reduce the eighteen Gate-II direction faces to two equivariant seeds.

The direction half of dL01 is indexed by

    (C4 chart, complementary tail matching, edge of the chart),

so it has 3*3*2=18 literal entries.  This checker extracts those entries
from the pinned first-PP computation and computes the exact orbit quotient
under edge swaps, tail permutations, and the endpoint chart swap.

The result is deliberately conditional on equivariance.  It reduces the
positive construction burden; it does not construct the missing physical
comparison or identify differently tagged source objects.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "notes/h3-h2-l01-three-cap-first-pp-curvature-gate.md":
        "d43b196a448045b9cf40a9537e5a30d9aad658a9c8636047052a023b45c4db7f",
    "computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py":
        "fbd4815eb5c6d46b8dbcd018f6e75237f004e3f52b1ccf47631479b698f9db35",
    "notes/h3-gate-ii-switch-weyl-product-rule-idempotent-gate.md":
        "432a612161538958c069de828b1f0f0a3321e5bdaa758be104942140df768b7d",
}
EXPECTED_LEDGER_SHA256 = (
    "1191424fb7b3166aad01a3f50cb11ffa14245f4843db45daee8b3958427a91b5"
)

SELECTED = frozenset((0, 1, 6, 7))
CHART = {
    ((0, 1), (6, 7)): "DQ",
    ((0, 6), (1, 7)): "PS01",
    ((0, 7), (1, 6)): "PS10",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None, ("cannot load", relative))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def identity() -> tuple[int, ...]:
    return tuple(range(8))


def transposition(left: int, right: int) -> tuple[int, ...]:
    answer = list(range(8))
    answer[left], answer[right] = answer[right], answer[left]
    return tuple(answer)


def compose(first, second):
    return tuple(first[second[index]] for index in range(8))


def generated_group(generators):
    group = {identity()}
    changed = True
    while changed:
        changed = False
        for left in tuple(group):
            for right in generators:
                product = compose(left, right)
                if product not in group:
                    group.add(product)
                    changed = True
    return tuple(sorted(group))


def extract_faces():
    curvature = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "direction_two_orbit_curvature",
    )
    matchings, _directions, _tails, l01, _r01, _ah = curvature.polynomial_data()
    differential = curvature.differential(l01)
    direction = {
        key: -value for key, value in differential.items()
        if set(key[1]).issubset(SELECTED)
    }
    require(len(matchings) == 105 and len(differential) == 36
            and len(direction) == 18,
            "the pinned 18+18 first-PP split changed")

    faces = []
    for (matching, edge), coefficient in sorted(direction.items()):
        chart_edges = tuple(sorted(item for item in matching
                                   if set(item).issubset(SELECTED)))
        tail = tuple(sorted(item for item in matching
                            if set(item).isdisjoint(SELECTED)))
        require(chart_edges in CHART and len(tail) == 2,
                ("unexpected direction face", matching, edge))
        faces.append((CHART[chart_edges], chart_edges, tail, edge, Q(coefficient)))
    require(len({(c, t, e) for c, _ce, t, e, _v in faces}) == 18,
            "literal direction labels ceased to be distinct")
    return tuple(faces)


def move_pair(pair, permutation):
    return tuple(sorted((permutation[pair[0]], permutation[pair[1]])))


def move_face(face, permutation):
    _chart, chart_edges, tail, edge, _value = face
    moved_chart = tuple(sorted(move_pair(item, permutation)
                               for item in chart_edges))
    moved_tail = tuple(sorted(move_pair(item, permutation) for item in tail))
    moved_edge = move_pair(edge, permutation)
    require(moved_chart in CHART, ("chart left packet", moved_chart))
    return CHART[moved_chart], moved_tail, moved_edge


def orbit_partition(faces, group):
    keys = [(chart, tail, edge) for chart, _ce, tail, edge, _v in faces]
    lookup = {key: index for index, key in enumerate(keys)}
    parent = list(range(len(faces)))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left, right):
        left, right = find(left), find(right)
        if left != right:
            parent[max(left, right)] = min(left, right)

    for permutation in group:
        for index, face in enumerate(faces):
            image = move_face(face, permutation)
            require(image in lookup, ("group left face set", image))
            union(index, lookup[image])
    answer = {}
    for index in range(len(faces)):
        answer.setdefault(find(index), []).append(index)
    return tuple(sorted((tuple(indices) for indices in answer.values()),
                        key=lambda orbit: orbit[0]))


def audit():
    pin_dependencies()
    faces = extract_faces()

    # Edge swaps on the selected K4, all S4 permutations of the tail K4,
    # and (0 1), which fixes DQ and exchanges the two PS charts.
    edge_swaps = (
        (1, 0, 2, 3, 4, 5, 7, 6),
        (6, 7, 2, 3, 4, 5, 0, 1),
    )
    tail_permutations = []
    for image in permutations((2, 3, 4, 5)):
        permutation = list(range(8))
        for source, target in zip((2, 3, 4, 5), image, strict=True):
            permutation[source] = target
        tail_permutations.append(tuple(permutation))
    endpoint_swap = transposition(0, 1)

    groups = {
        "identity": (identity(),),
        "edge_V4": generated_group(edge_swaps),
        "edge_V4_x_tail_S4": generated_group(edge_swaps + tuple(tail_permutations)),
        "full": generated_group(edge_swaps + tuple(tail_permutations)
                                + (endpoint_swap,)),
    }
    require(tuple(map(len, groups.values())) == (1, 4, 96, 192),
            ("group orders changed", tuple(map(len, groups.values()))))

    tower = []
    for name, group in groups.items():
        orbits = orbit_partition(faces, group)
        orbit_values = []
        for orbit in orbits:
            values = {faces[index][4] for index in orbit}
            require(len(values) == 1, ("coefficient not invariant", name, orbit))
            orbit_values.append(next(iter(values)))
        tower.append({
            "group": name,
            "order": len(group),
            "orbit_count": len(orbits),
            "orbit_sizes": sorted(map(len, orbits)),
            "orbit_values": [str(value) for value in orbit_values],
        })

    require([entry["orbit_count"] for entry in tower] == [18, 9, 3, 2],
            ("orbit tower changed", tower))
    require(tower[-1]["orbit_sizes"] == [6, 12]
            and sorted(tower[-1]["orbit_values"]) == ["-2", "1"],
            ("final two-orbit quotient changed", tower[-1]))

    coefficients = {face[4] for face in faces}
    require(coefficients == {Q(-2), Q(1)}, "coefficient spectrum changed")
    # Any coefficient-preserving quotient needs at least two classes, so the
    # full physical label action reaches the sharp minimum.
    ledger = {
        "theorem": "h3 Gate-II eighteen direction faces reduce to two equivariant seeds",
        "pins": PINS,
        "literal_faces": 18,
        "literal_indexing": "3 C4 charts x 3 tail matchings x 2 chart edges",
        "coefficient_spectrum": ["-2 on DQ", "+1 on PS01 and PS10"],
        "orbit_tower": tower,
        "minimum_equivariant_seed_count": 2,
        "representatives": ["one DQ face", "one PS face"],
        "sharpness": (
            "the differential coefficient takes two distinct values, so no "
            "coefficient-preserving quotient can have one orbit"
        ),
        "scope": (
            "This is a label-faithful coefficient/orbit reduction conditional "
            "on a physical comparison equivariant for selected-edge swaps, "
            "tail relabelling, and endpoint chart swap.  It constructs no "
            "response-to-AugP2 word arrow, no mixed B/Eq incidence, and no "
            "source cell; it only reduces the 18 proper-face obligations to "
            "two natural seeds."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("direction two-orbit ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 Gate-II direction-face two-orbit reduction: PASS")
    print("literal faces: 18 -> edge V4: 9 -> tail S4: 3 -> chart swap: 2")
    print("exact natural seeds: DQ coefficient -2; PS coefficient +1")
    print("physical mixed B/Eq landing: STILL OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
