#!/usr/bin/env python3
"""Classify and exclude the first two-cell off-axis Euler packets.

Start with either affine cube-cut diagonal support-28 chart.  Adjoin two
ordered off-diagonal cells on disjoint physical edges with the same unordered
colour pair.  These are exactly the two-cell packets whose colour-incidence
parities can cancel, so they are the first packets capable of entering an
all-even diagonal source row.

The checker classifies all 2,520 labelled packets under the actual marked
support stabilizer in each target chart, tests their literal two-cell
hafnian contributions to all 96 permanent triangles, and replays an
unchanged Laurent-unit certificate for every packet.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/verify_n8_support28_one_offdiagonal_cell_permanent_triangle_gate.py"
)
DEPENDENCY_SHA256 = (
    "28dad0ad6d2767727cefbec4f364ac48f1d566ceabc9e878edd2174cc8e6e341"
)
EXPECTED_LEDGER_SHA256 = (
    "6aa810c966bfa10455bb632ee77b3880409b569b4a791d8a4f7316599fcde191"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    path = ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def packets(base):
    answer = []
    for first_edge, second_edge in combinations(base.EDGES, 2):
        if set(first_edge) & set(second_edge):
            continue
        for first_colour, second_colour in combinations(base.COLORS, 2):
            orientations = ((first_colour, second_colour),
                            (second_colour, first_colour))
            for first_orientation, second_orientation in product(
                    orientations, repeat=2):
                answer.append(((first_edge, first_orientation),
                               (second_edge, second_orientation)))
    require(len(answer) == 2520, len(answer))
    return tuple(answer)


def transform_support(base, support, vertex, colour):
    answer = {}
    for endpoints, values in support.items():
        image = edge(vertex[endpoints[0]], vertex[endpoints[1]])
        answer[image] = tuple(sorted(colour[value] for value in values))
    require(tuple(sorted(answer)) == base.EDGES, "support transform lost an edge")
    return answer


def support_stabilizer(base, support, chart):
    colour_actions = (
        ((0, 1, 2), (0, 2, 1))
        if chart == "pair-target-12" else tuple(permutations(base.COLORS))
    )
    actions = []
    for swap_endpoints in (False, True):
        for tail in permutations(range(2, 8)):
            vertex = (1, 0, *tail) if swap_endpoints else (0, 1, *tail)
            for colour in colour_actions:
                if transform_support(base, support, vertex, colour) == support:
                    actions.append((vertex, colour))
    expected = 4 if chart == "pair-target-12" else 12
    require(len(actions) == expected, (chart, len(actions), expected))
    return tuple(actions)


def transform_cell(cell, action):
    (left, right), (left_colour, right_colour) = cell
    vertex, colour = action
    moved_left, moved_right = vertex[left], vertex[right]
    moved_colours = (colour[left_colour], colour[right_colour])
    if moved_left < moved_right:
        return ((moved_left, moved_right), moved_colours)
    return ((moved_right, moved_left), tuple(reversed(moved_colours)))


def transform_packet(packet, action):
    return tuple(sorted(transform_cell(cell, action) for cell in packet))


def orbit_registry(all_packets, actions):
    packet_set = set(all_packets)
    unseen = set(all_packets)
    representatives = []
    size_histogram = Counter()
    while unseen:
        representative = min(unseen)
        orbit = {transform_packet(representative, action) for action in actions}
        require(orbit <= packet_set, ("action left packet universe", representative))
        require(orbit <= unseen, ("packet orbits overlapped", representative))
        representatives.append(representative)
        size_histogram[len(orbit)] += 1
        unseen.difference_update(orbit)
    encoded = json.dumps(representatives, separators=(",", ":"))
    return {
        "orbits": len(representatives),
        "orbit_size_histogram": sorted(size_histogram.items()),
        "representative_registry_sha256": sha256(encoded.encode()).hexdigest(),
        "first_representatives": representatives[:6],
    }


def two_cell_contributes(one, base, word, support, packet):
    """Whether the literal row gains a monomial using both marked cells."""
    marked_vertices = set()
    for endpoints, ordered_colours in packet:
        marked_vertices.update(endpoints)
        if tuple(word[vertex] for vertex in endpoints) != ordered_colours:
            return False
    require(len(marked_vertices) == 4, packet)
    remainder = tuple(vertex for vertex in base.VERTICES
                      if vertex not in marked_vertices)
    for matching in base.perfect_matchings(remainder):
        if all(word[left] == word[right]
               and word[left] in support[edge(left, right)]
               for left, right in matching):
            return True
    return False


def augmented_hafnian(base, word, support, packet):
    marks = dict(packet)
    answer = Counter()
    for matching in base.MATCHINGS:
        cells = []
        for endpoints in matching:
            left, right = endpoints
            colours = (word[left], word[right])
            if endpoints in marks and colours == marks[endpoints]:
                cells.append(
                    f"z{left}{right}_{colours[0]}{colours[1]}"
                )
            elif (colours[0] == colours[1]
                  and colours[0] in support[endpoints]):
                cells.append(base.variable(colours[0], endpoints))
            else:
                break
        else:
            answer[tuple(sorted(cells))] += 1
    return dict(answer)


def chart_audit(one, base, chart, support, all_packets):
    actions = support_stabilizer(base, support, chart)
    orbits = orbit_registry(all_packets, actions)
    triangles = base.permanent_triangles(support)
    require(len(triangles) == 96, (chart, len(triangles)))

    untouched_histogram = Counter()
    touched_row_histogram = Counter()
    touched_packets = 0
    minimum_untouched = len(triangles)
    minimum_packet_records = []
    for packet in all_packets:
        untouched = []
        touched_rows = 0
        for triangle in triangles:
            words = one.triangle_words(base, triangle)
            row_hits = tuple(
                two_cell_contributes(one, base, word, support, packet)
                for word in words
            )
            touched_rows += sum(row_hits)
            if not any(row_hits):
                untouched.append((triangle, words))
        require(untouched,
                ("two-cell packet met every permanent triangle", chart, packet))
        if len(untouched) < minimum_untouched:
            minimum_untouched = len(untouched)
            minimum_packet_records = []
        untouched_histogram[len(untouched)] += 1
        touched_row_histogram[touched_rows] += 1
        touched_packets += bool(touched_rows)

        # Check the full augmented coefficient on a surviving certificate.
        triangle, words = untouched[0]
        require(all(
            augmented_hafnian(base, word, support, packet)
            == base.hafnian_coefficient(word, support)
            for word in words
        ), ("selected two-cell certificate changed", chart, packet, words))
        unit = base.audit_selected_unit(
            triangle,
            support,
            expected_shape=triangle[:3],
            expected_words=words,
        )
        require(unit["rhs_coefficient"] == 2, (chart, packet, unit))
        if len(untouched) == minimum_untouched:
            minimum_packet_records.append({
                "source_labelled_packet": packet,
                "surviving_certificate_words": unit["words"],
                "surviving_certificate_shape": triangle[:3],
            })

    return {
        "chart": chart,
        "support_stabilizer_order": len(actions),
        "labelled_packets": len(all_packets),
        "orbit_registry": orbits,
        "packets_entering_some_triangle_row": touched_packets,
        "minimum_untouched_triangles": minimum_untouched,
        "minimum_packet_records": minimum_packet_records,
        "untouched_triangle_count_histogram": sorted(
            untouched_histogram.items()
        ),
        "total_touched_row_count_histogram": sorted(
            touched_row_histogram.items()
        ),
        "consequence": (
            "every two-cell Euler packet leaves a complete three-row "
            "permanent-triangle Laurent unit unchanged"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    actual = sha256((ROOT / DEPENDENCY).read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            ("pinned dependency changed", actual, DEPENDENCY_SHA256))
    one = load(DEPENDENCY, "n8_support28_two_cell_one_cell_dependency")
    one.pin_dependencies()
    base = one.load(
        "computations/audit_n8_support28_cube_cut_permanent_triangle_unit_independent.py",
        "n8_support28_two_cell_base",
    )
    pair_support = one.cut_support(base, base.CUBE_BITS)
    full_support = one.cut_support(base, one.FULL_TARGET_CUBE_BITS)
    all_packets = packets(base)

    charts = (
        chart_audit(one, base, "pair-target-12", pair_support, all_packets),
        chart_audit(one, base, "full-target-012", full_support, all_packets),
    )
    ledger = {
        "mode_independent": True,
        "dependency": {DEPENDENCY: DEPENDENCY_SHA256},
        "packet_definition": (
            "two ordered off-diagonal cells on disjoint physical edges with "
            "one common unordered endpoint-colour pair"
        ),
        "first_even_parity_atom": True,
        "charts": charts,
        "theorem": (
            "the first two-cell Euler-even off-axis packet cannot repair "
            "the affine support-28 coefficient fibre; a source must lower "
            "diagonal support or contain a larger off-axis packet"
        ),
        "next_scope": (
            "three-cell colour triangles and larger colour-Euler packets, "
            "or simultaneous packets capable of meeting every surviving "
            "permanent-triangle certificate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))

    print("N=8 support-28 two-offdiagonal Euler-packet gate: PASS")
    print("mode", arguments.mode)
    for chart in charts:
        registry = chart["orbit_registry"]
        print(chart["chart"], "stabilizer / orbits / sizes",
              chart["support_stabilizer_order"], registry["orbits"],
              registry["orbit_size_histogram"])
        print("  touched packets / min untouched / hist",
              chart["packets_entering_some_triangle_row"],
              chart["minimum_untouched_triangles"],
              chart["untouched_triangle_count_histogram"])
        print("  worst labelled packets",
              [record["source_labelled_packet"]
               for record in chart["minimum_packet_records"]])
    print("consequence: Laurent unit or diagonal support <= 47")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
