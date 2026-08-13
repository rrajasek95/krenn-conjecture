#!/usr/bin/env python3
"""Finite classification of face-complete flat signed matching components.

After Laurent normalization, a unique mate for every mandatory boundary
face gives one fixed-point-free involution tau_j on the occurrence set for
each retained face direction j.  Rows are e_x+e_tau_j(x).  The union is a
regular labelled multigraph.

For each connected component:

* non-bipartite means an odd sign circuit and full row rank;
* bipartite means one alternating cokernel charge;
* every tau_j bijects the two shores, hence they have equal size and the
  charge has total augmentation zero (is occurrence-centered).

The checker exhausts every involution family on 2,4,6 vertices (up to 3
directions), audits exact ranks and odd-cycle certificates, and freezes the
sharp guards: partial path completion and an unequal edge weight can leave
or destroy the centered conclusion respectively.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_signed_matching_holonomy_boundary_counterguard.py":
        "12bb763f3ca2f2dde30f6a8f932fd6d8b9fa3c970e1e3aab2f46592bcde93547",
    "notes/uniform-signed-matching-holonomy-boundary-counterguard.md":
        "afa8c41df024b2c6b9b7b7088346880059ca54cdb060216bd9009ca5066aae37",
    "computations/verify_oo_binomial_scc_holonomy_cokernel.py":
        "de1f73dd7b225780c3c2a4269038a6d113ab5a07bcfed1090d0b92dbbc24fb6c",
    "notes/oo-binomial-scc-holonomy-cokernel.md":
        "05364928d3f9d78756a1c290702b2025f40d5024ecfb01050b2b9d230556480c",
    "computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py":
        "34bf365f2a9e154a10feab8fa7cc83b0aba519f4124b8e28ed959f280a51e721",
    "notes/uniform-hall-five-lock-signless-incidence-boundary.md":
        "4da56337a9cc6b8434a06b6cf1e4c9118334ebf695f4679e8183232f4733cb1b",
    "computations/verify_uniform_one_bad_square_zero_clean_cap.py":
        "a943fffdc3ce86aa5506e6774ec3a6a8ff10c70491225417152a1298e2754883",
    "notes/uniform-one-bad-square-zero-clean-cap.md":
        "2af5f90040152079c094e03b0b1bb794761a07d2418182586ab06848ee820c2e",
}
EXPECTED_DIGEST = "ed24a127573b9a43b32c7b6aee5369abc1c60c78d45a355808d3be7b15f8fe81"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def rank(rows, width):
    work = [[Q(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def involution_from_matching(size, matching):
    answer = [None] * size
    for left, right in matching:
        answer[left] = right
        answer[right] = left
    require(all(value is not None for value in answer),
            "a fixed-point-free involution lost a vertex")
    return tuple(answer)


def labelled_edges(involutions):
    records = []
    for label, involution in enumerate(involutions):
        for vertex, other in enumerate(involution):
            if vertex < other:
                records.append((vertex, other, label))
    return tuple(records)


def components(size, edges):
    adjacency = [[] for _ in range(size)]
    for left, right, _label in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(size))
    answer = []
    while unseen:
        root = min(unseen)
        seen = {root}
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        unseen -= seen
        answer.append(tuple(sorted(seen)))
    return tuple(answer)


def bipartition(component, edges):
    allowed = set(component)
    adjacency = {vertex: [] for vertex in component}
    for left, right, _label in edges:
        if left in allowed:
            require(right in allowed, "an edge crossed a connected component")
            adjacency[left].append(right)
            adjacency[right].append(left)
    colour = {component[0]: 0}
    queue = deque([component[0]])
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in colour:
                colour[other] = 1 - colour[vertex]
                queue.append(other)
            elif colour[other] == colour[vertex]:
                return None
    return tuple(tuple(vertex for vertex in component if colour[vertex] == side)
                 for side in (0, 1))


def component_rows(component, edges, size):
    allowed = set(component)
    rows = []
    for left, right, _label in edges:
        if left not in allowed:
            continue
        row = [0] * size
        row[left] = row[right] = 1
        rows.append(tuple(row))
    return tuple(rows)


def find_odd_cycle(component, edges):
    allowed = set(component)
    adjacency = {vertex: [] for vertex in component}
    for edge_index, (left, right, _label) in enumerate(edges):
        if left in allowed:
            adjacency[left].append((right, edge_index))
            adjacency[right].append((left, edge_index))
    parent = {component[0]: (None, None)}
    parity = {component[0]: 0}
    queue = deque([component[0]])
    while queue:
        vertex = queue.popleft()
        for other, edge_index in adjacency[vertex]:
            if other not in parity:
                parity[other] = 1 - parity[vertex]
                parent[other] = (vertex, edge_index)
                queue.append(other)
                continue
            if parity[other] != parity[vertex]:
                continue

            # Tree paths to the first common ancestor plus this same-parity
            # edge give an odd closed walk; reduce the common prefix.
            left_path = []
            current = vertex
            while current is not None:
                left_path.append(current)
                current = parent[current][0]
            right_path = []
            current = other
            while current is not None:
                right_path.append(current)
                current = parent[current][0]
            right_set = set(right_path)
            ancestor = next(value for value in left_path if value in right_set)
            left_segment = left_path[:left_path.index(ancestor) + 1]
            right_segment = right_path[:right_path.index(ancestor)]
            cycle = tuple(left_segment + list(reversed(right_segment)))
            require(len(cycle) % 2 == 1,
                    f"the reconstructed odd cycle is even: {cycle}")
            return cycle
    return None


def audit_family(size, involutions):
    edges = labelled_edges(involutions)
    records = []
    for component in components(size, edges):
        rows = component_rows(component, edges, size)
        sides = bipartition(component, edges)
        component_rank = rank(rows, size)
        if sides is None:
            cycle = find_odd_cycle(component, edges)
            require(cycle is not None and len(cycle) % 2 == 1
                    and component_rank == len(component),
                    ("odd component audit", component, cycle, component_rank))
            records.append({
                "vertices": list(component),
                "bipartite": False,
                "rank": component_rank,
                "odd_cycle_length": len(cycle),
            })
            continue

        left, right = sides
        require(len(left) == len(right),
                f"a face-complete flat component has unequal shores: {sides}")
        charge = [0] * size
        for vertex in left:
            charge[vertex] = 1
        for vertex in right:
            charge[vertex] = -1
        require(sum(charge) == 0
                and all(sum(a * b for a, b in zip(row, charge, strict=True)) == 0
                        for row in rows)
                and component_rank == len(component) - 1,
                ("centered flat component audit", component, charge,
                 component_rank))

        # Every direction is a global involution and hence maps this
        # connected component to itself.  Its restriction bijects shores.
        for involution in involutions:
            require({involution[vertex] for vertex in component}
                    == set(component),
                    "a mate involution escaped its component")
            require({involution[vertex] for vertex in left} == set(right)
                    and {involution[vertex] for vertex in right} == set(left),
                    "a face direction stopped bijecting the two shores")
        records.append({
            "vertices": list(component),
            "bipartite": True,
            "rank": component_rank,
            "shore_sizes": [len(left), len(right)],
            "charge_augmentation": sum(charge),
        })
    return tuple(records)


def exhaustive_involution_census():
    ledger = []
    total_families = 0
    total_components = Counter()
    for size in (2, 4, 6):
        matchings = tuple(perfect_matchings(range(size)))
        involutions = tuple(involution_from_matching(size, matching)
                            for matching in matchings)
        size_families = 0
        size_components = Counter()
        for direction_count in range(1, min(3, len(involutions)) + 1):
            # Repetitions matter: two face directions can have the same mate
            # involution and give parallel source rows.
            for indices in itertools.combinations_with_replacement(
                    range(len(involutions)), direction_count):
                family = tuple(involutions[index] for index in indices)
                records = audit_family(size, family)
                size_families += 1
                for record in records:
                    key = ("flat" if record["bipartite"] else "odd",
                           len(record["vertices"]))
                    size_components[key] += 1
        total_families += size_families
        total_components.update(size_components)
        ledger.append({
            "vertices": size,
            "perfect_matchings_or_involutions": len(involutions),
            "families_through_three_directions": size_families,
            "component_histogram": {
                repr(key): value for key, value in sorted(size_components.items())
            },
        })
    return total_families, total_components, ledger


def sharp_guards():
    # Dropping one face from a C4 path leaves a connected bipartite component
    # with shores 2 and 1.  Its charge is not occurrence-centered.
    path_rows = (
        (1, 1, 0),
        (0, 1, 1),
    )
    path_charge = (1, -1, 1)
    require(rank(path_rows, 3) == 2
            and all(sum(a * b for a, b in zip(row, path_charge, strict=True)) == 0
                    for row in path_rows)
            and sum(path_charge) == 1,
            "the incomplete-path noncentered guard changed")

    # A complete C4 has centered alternating charge.  One unequal coefficient
    # destroys the flat character while preserving unweighted incidence.
    square = (
        (1, 1, 0, 0),
        (0, 1, 1, 0),
        (0, 0, 1, 1),
        (1, 0, 0, 1),
    )
    square_charge = (1, -1, 1, -1)
    weighted = list(square)
    weighted[0] = (1, 2, 0, 0)
    require(rank(square, 4) == 3 and sum(square_charge) == 0
            and rank(weighted, 4) == 4,
            "the unequal-character square guard changed")
    return {
        "incomplete_path": {
            "rows": [list(row) for row in path_rows],
            "flat_charge": list(path_charge),
            "charge_augmentation": sum(path_charge),
            "missing_hypothesis": "one mate direction is not total",
        },
        "unequal_weight_square": {
            "unweighted_rank": rank(square, 4),
            "weighted_rank": rank(weighted, 4),
            "meaning": (
                "incidence completeness without Laurent-character flatness "
                "can already be a unit"
            ),
        },
    }


def four_port_interface():
    # The theorem does not assert that every centered charge is a physical
    # finite source switch.  It does identify the exact extra hypothesis
    # under which the pinned square-zero one-bad cap consumes it.
    directions = {
        "p1": "one residual site",
        "p2": "one residual site",
        "s1": "one residual site",
        "s2": "one residual site",
    }
    return {
        "centered_charge_source_safe_if": (
            "all occurrences in the component are variations in one common "
            "physical same-star four-port switch space"
        ),
        "four_port_support": directions,
        "square_zero_consequence": [
            "p1^[2]=0", "p2^[2]=0", "s1^[2]=0", "s2^[2]=0"
        ],
        "landing": (
            "after the normalized one-bad response rows are retained, the "
            "pinned cap K=((1,0,0),(0,1,1),(0,-1,1)) is active and clean"
        ),
        "not_proved_here": (
            "an arbitrary occurrence-centered charge is not automatically "
            "a physical same-star switch or a normalized one-bad packet"
        ),
    }


def main():
    pin_dependencies()
    family_count, component_histogram, finite = exhaustive_involution_census()
    ledger = {
        "pins": PINS,
        "finite_exhaustion": finite,
        "total_involution_families": family_count,
        "total_component_histogram": {
            repr(key): value for key, value in sorted(component_histogram.items())
        },
        "uniform_theorem": (
            "let every retained mandatory boundary-face direction have a "
            "unique same-character binomial mate at every occurrence.  Its "
            "mate map is a fixed-point-free involution.  In each connected "
            "component, a nonbipartite mate graph has odd signed holonomy; "
            "a bipartite flat graph has one alternating cokernel charge.  "
            "Every mate involution bijects its shores, so the charge has "
            "augmentation zero and is occurrence-centered"
        ),
        "sharp_guards": sharp_guards(),
        "four_port_interface": four_port_interface(),
        "remaining_obligation": (
            "prove that actual full source rows either satisfy unique total "
            "same-character face mating, expose a singleton/extra column, "
            "or place the resulting centered charge in a common physical "
            "same-star four-port switch space"
        ),
        "scope": (
            "uniform finite graph/character theorem with exhaustive small "
            "census; not a proof that arbitrary decorated hafnian boundary "
            "rows satisfy the total involution hypothesis"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"boundary-complete flat ledger changed: {digest}")
    print("uniform boundary-complete flat-even component theorem: PASS")
    print(f"involution families audited: {family_count}")
    print("nonbipartite component -> odd signed holonomy")
    print("flat bipartite component -> occurrence-centered charge")
    print("missing total face -> noncentered path charge is possible")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
