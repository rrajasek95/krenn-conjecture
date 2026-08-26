#!/usr/bin/env python3
"""Bounded exact structural census for the orbit-zero terminal K24 page.

This does not construct a K24 residual or a Macaulay matrix.  It pins the
literal degree-24 provider, enumerates the finite word/matching decoration
types, proves a large ambient-orbit lower bound using doubled perfect
matchings, and exhibits a literal pair showing that cycle/content profiles do
not determine source incidence.
"""

from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HPL_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-lower-kernel-hpl-2026-08-23"
              / "audit_k16_lower_kernel_component.py")
D24_SOURCE = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
              / "audit_orbit0_t2_pivot_setup.py")
OUT = HERE / "results_k24_terminal_structure.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


HPL = load("k24_terminal_hpl", HPL_SOURCE)
D24 = load("k24_terminal_d24", D24_SOURCE)
F = HPL.F


def partition_count(total, minimum=2):
    @lru_cache(None)
    def visit(remainder, lower):
        if remainder == 0:
            return 1
        return sum(visit(remainder - part, part)
                   for part in range(lower, remainder + 1))
    return visit(total, minimum)


def abstract_colour_content_orbits():
    """Burnside count of component-content multisets totaling (8,8,8).

    A component contributes a nonnegative colour-count triple of total size at
    least two.  This is the complete abstract content universe, before asking
    whether physical site labels and the forbidden anchor edges realize it.
    """
    component_types = tuple(
        (a, b, c) for a in range(9) for b in range(9) for c in range(9)
        if a + b + c >= 2)
    fixed_counts = {}
    for colour_permutation in permutations(range(3)):
        unseen = set(component_types)
        orbit_weights = []
        while unseen:
            seed = min(unseen)
            orbit = set()
            current = seed
            while current not in orbit:
                orbit.add(current)
                current = tuple(current[colour_permutation[index]]
                                for index in range(3))
            unseen.difference_update(orbit)
            orbit_weights.append(tuple(sum(value[index] for value in orbit)
                                       for index in range(3)))
        dynamic = {(0, 0, 0): 1}
        for weight in orbit_weights:
            updated = {}
            for current, count in dynamic.items():
                multiplicity = 0
                while all(current[index] + multiplicity * weight[index] <= 8
                          for index in range(3)):
                    target = tuple(current[index] + multiplicity * weight[index]
                                   for index in range(3))
                    updated[target] = updated.get(target, 0) + count
                    multiplicity += 1
            dynamic = updated
        fixed_counts["".join(map(str, colour_permutation))] = \
            dynamic.get((8, 8, 8), 0)
    total = sum(fixed_counts.values())
    require(total % 6 == 0, total)
    return total // 6, fixed_counts


def move_word(word, action):
    sites, colours = F.EXPORT.STABILIZER[action]
    moved = [None] * 8
    for old_site, old_colour in enumerate(word):
        moved[sites[old_site]] = colours[old_colour]
    return tuple(moved)


def move_decoration(decoration, action):
    word, matching = decoration
    sites, _colours = F.EXPORT.STABILIZER[action]
    moved_matching = tuple(sorted(
        (min(sites[u], sites[v]), max(sites[u], sites[v]))
        for u, v in matching))
    return move_word(word, action), moved_matching


def orbit_census(items, actions, mover):
    seen = set()
    sizes = Counter()
    orbits = 0
    for item in items:
        if item in seen:
            continue
        orbit = {mover(item, action) for action in actions}
        seen.update(orbit)
        sizes[len(orbit)] += 1
        orbits += 1
    require(len(seen) == len(items), (len(seen), len(items)))
    return orbits, dict(sorted(sizes.items()))


def anchor_free_port_matching_count():
    """Count PMs on the 24 ports avoiding same-site cells and 12 anchors."""
    vertices = tuple(range(24))
    m0 = {tuple(edge) for edge in F.M0}

    def allowed(x, y):
        i, a = divmod(x, 3)
        j, b = divmod(y, 3)
        if i == j:
            return False
        edge = (min(i, j), max(i, j))
        return not (edge in m0 and a == b)

    adjacency = tuple(sum(1 << y for y in vertices
                          if y != x and allowed(x, y))
                      for x in vertices)

    @lru_cache(None)
    def count(mask):
        if mask == 0:
            return 1
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        choices = adjacency[first] & remainder
        answer = 0
        while choices:
            mate_bit = choices & -choices
            choices ^= mate_bit
            answer += count(remainder ^ mate_bit)
        return answer

    answer = count((1 << 24) - 1)
    return answer, count.cache_info().currsize


def row_profile(row):
    adjacency = [[] for _ in range(24)]
    for cell in row:
        u, v, a, b = F.BASE.CELLS[cell]
        x, y = 3 * u + a, 3 * v + b
        adjacency[x].append(y)
        adjacency[y].append(x)
    require(all(len(neighbours) == 2 for neighbours in adjacency),
            "row is not port-balanced")
    seen = set()
    contents = []
    for seed in range(24):
        if seed in seen:
            continue
        queue = deque([seed])
        seen.add(seed)
        content = [0, 0, 0]
        while queue:
            vertex = queue.popleft()
            content[vertex % 3] += 1
            for other in adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        contents.append(tuple(content))
    cycle_partition = tuple(sorted(sum(content) for content in contents))
    content_images = []
    for colour_permutation in permutations(range(3)):
        image = []
        for content in contents:
            moved = [0, 0, 0]
            for old in range(3):
                moved[colour_permutation[old]] = content[old]
            image.append(tuple(moved))
        content_images.append(tuple(sorted(image)))
    return cycle_partition, min(content_images)


def doubled_matching_row(edges):
    cells = []
    ports = set()
    for (u, a), (v, b) in edges:
        require((u, a) not in ports and (v, b) not in ports,
                "port matching repeated a port")
        ports.update(((u, a), (v, b)))
        if u > v:
            u, v, a, b = v, u, b, a
        cell = F.BASE.CELL_ID[(u, v, a, b)]
        require(cell not in F.A, "counterguard used an anchor")
        cells.extend((cell, cell))
    require(len(ports) == 24, len(ports))
    return bytes(sorted(cells))


def main():
    anchors, _packet = HPL.fractionless_packet()
    h_actions = HPL.factor_stabilizer(anchors)
    g_actions = tuple(range(len(F.EXPORT.STABILIZER)))
    require(len(h_actions) == 384 and len(g_actions) == 2304,
            (len(h_actions), len(g_actions)))
    require(len(F.A) == 12 and len(F.BASE.PM8) == 105,
            (len(F.A), len(F.BASE.PM8)))

    words = tuple(word for word in product(range(3), repeat=8)
                  if len(set(word)) > 1)
    require(len(words) == 6558, len(words))

    top_terms_by_word = Counter()
    top_decorations = []
    m0 = set(F.M0)
    for word in words:
        top = 0
        for matching in F.BASE.PM8:
            anchor_free = all(not (edge in m0 and word[edge[0]] == word[edge[1]])
                              for edge in matching)
            if anchor_free:
                top += 1
                top_decorations.append((word, matching))
        top_terms_by_word[top] += 1
    require(top_terms_by_word == {60: 78, 68: 648, 78: 1944,
                                  90: 2592, 105: 1296},
            top_terms_by_word)
    require(len(top_decorations) == 569736, len(top_decorations))

    word_h_orbits, word_h_sizes = orbit_census(words, h_actions, move_word)
    word_g_orbits, word_g_sizes = orbit_census(words, g_actions, move_word)
    decoration_h_orbits, decoration_h_sizes = orbit_census(
        top_decorations, h_actions, move_decoration)
    decoration_g_orbits, decoration_g_sizes = orbit_census(
        top_decorations, g_actions, move_decoration)
    require((word_h_orbits, word_g_orbits,
             decoration_h_orbits, decoration_g_orbits)
            == (83, 27, 1757, 366),
            (word_h_orbits, word_g_orbits,
             decoration_h_orbits, decoration_g_orbits))

    doubled_rows, matching_dp_states = anchor_free_port_matching_count()
    require(doubled_rows == 61597706812, doubled_rows)
    abstract_contents, content_fixed_counts = abstract_colour_content_orbits()
    require(abstract_contents == 525346,
            (abstract_contents, content_fixed_counts))

    first_edges = (
        ((1, 1), (6, 2)), ((5, 0), (7, 2)), ((0, 2), (4, 0)),
        ((3, 0), (4, 2)), ((1, 0), (6, 0)), ((2, 1), (7, 1)),
        ((3, 1), (0, 0)), ((2, 0), (1, 2)), ((7, 0), (3, 2)),
        ((0, 1), (4, 1)), ((5, 1), (2, 2)), ((5, 2), (6, 1)),
    )
    second_edges = (
        ((3, 2), (7, 2)), ((1, 0), (3, 0)), ((0, 0), (6, 1)),
        ((2, 1), (1, 2)), ((4, 0), (1, 1)), ((4, 2), (3, 1)),
        ((5, 0), (7, 1)), ((4, 1), (7, 0)), ((0, 1), (6, 2)),
        ((6, 0), (2, 2)), ((5, 2), (0, 2)), ((5, 1), (2, 0)),
    )
    first = doubled_matching_row(first_edges)
    second = doubled_matching_row(second_edges)
    first_profile = row_profile(first)
    second_profile = row_profile(second)
    first_incidence = len(D24.incident_degree24_columns(first))
    second_incidence = len(D24.incident_degree24_columns(second))
    require(D24.row_k_degree(first) == D24.row_k_degree(second) == 24,
            "counterguard escaped K24")
    require(first_profile == second_profile
            and first_profile[0] == (2,) * 12,
            (first_profile, second_profile))
    require((first_incidence, second_incidence) == (6, 8),
            (first_incidence, second_incidence))

    result = {
        "status": "PASS bounded exact K24 terminal structural census",
        "literal_model": {
            "row": "24-cell monomial; every one of 24 site-colour ports has degree 2; no anchor cell",
            "edge_multiplicity_range": [0, 2],
            "port_graph": "2-regular multigraph with cycle lengths >=2",
            "column": "U*H_w, w mixed, |U|=20; K24 projection retains exactly the anchor-free matching terms of H_w",
        },
        "groups": {
            "factor_stabilizer_H": len(h_actions),
            "fixed_chart_stabilizer": len(g_actions),
            "full_S8xS3": 241920,
            "full_group_guard": "S8xS3 transports the anchor chart; it does not act within the fixed K24 filtration",
        },
        "row_profiles": {
            "cycle_partition_types": partition_count(24),
            "abstract_global_S3_cycle_colour_content_types": abstract_contents,
            "abstract_content_Burnside_fixed_counts": content_fixed_counts,
            "frozen_K17_residual_realized_content_types_control": 6800,
            "abstract_content_guard": (
                "525346 is an abstract superset before physical-site and anchor "
                "realizability; 6800 was only the frozen K17 residual census"
            ),
            "doubled_anchor_free_port_matching_rows": doubled_rows,
            "matching_DP_states": matching_dp_states,
            "H_row_orbit_lower_bound_from_doubled_rows":
                (doubled_rows + len(h_actions) - 1) // len(h_actions),
            "chart_stabilizer_row_orbit_lower_bound_from_doubled_rows":
                (doubled_rows + len(g_actions) - 1) // len(g_actions),
            "S8xS3_transport_orbit_lower_bound_if_all_charts_are_joined":
                (doubled_rows + 241920 - 1) // 241920,
        },
        "source_decorations": {
            "mixed_words": len(words),
            "word_top_term_count_histogram": dict(sorted(top_terms_by_word.items())),
            "anchor_free_word_matching_decorations": len(top_decorations),
            "H_word_orbits": word_h_orbits,
            "H_word_orbit_size_histogram": word_h_sizes,
            "chart_word_orbits": word_g_orbits,
            "chart_word_orbit_size_histogram": word_g_sizes,
            "full_S8xS3_word_profile_orbits": 9,
            "H_top_decoration_orbits": decoration_h_orbits,
            "H_top_decoration_orbit_size_histogram": decoration_h_sizes,
            "chart_top_decoration_orbits": decoration_g_orbits,
            "chart_top_decoration_orbit_size_histogram": decoration_g_sizes,
        },
        "profile_insufficiency_counterguard": {
            "common_cycle_partition": list(first_profile[0]),
            "common_global_S3_colour_content": [list(value)
                                                 for value in first_profile[1]],
            "first_row": first.hex(),
            "first_literal_incident_columns": first_incidence,
            "second_row": second.hex(),
            "second_literal_incident_columns": second_incidence,
            "conclusion": "cycle partition and cycle colour content do not determine literal source incidence",
        },
        "exact_terminal_criterion": (
            "After K19..K23 have produced a literal H-invariant residual R24, "
            "R24 vanishes in the terminal relative cokernel iff it lies in the "
            "span of the K24 projections of all literal U*H_w columns.  Reynolds "
            "averaging permits the equivalent H-orbit-mass matrix."
        ),
        "cycle_Morse_reduction": (
            "A K24 row with a mixed physical perfect-matching divisor selecting "
            "four distinct port cycles is a unit top pivot; every other K24 term "
            "of that column has fewer cycles.  The remaining exact block consists "
            "of rows with <=3 cycles, no such physical matching, or only pure such matchings."
        ),
        "boundedness_verdict": (
            "The 320-coordinate partition and 525346-coordinate abstract content "
            "projections are bounded necessary quotients, "
            "not exact rank models.  Literal H-orbit incidence remains enormous; a "
            "source-faithful terminal test needs full port/site/color provenance or "
            "an additional theorem identifying a complete quotient."
        ),
        "source_sha256": {
            str(HPL_SOURCE.relative_to(ROOT)): sha256(HPL_SOURCE.read_bytes()).hexdigest(),
            str(D24_SOURCE.relative_to(ROOT)): sha256(D24_SOURCE.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
