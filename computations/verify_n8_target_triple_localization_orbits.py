#!/usr/bin/env python3
"""Audit the 31 localized pure-matching charts at n=8.

A chart is an S_8 x S_3 orbit of an ordered triple of pure perfect matching
monomials.  The checker records the exact orbit size and the mixed support
one-factors available in the corresponding coloured cubic multigraph.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "analyze_n8_full_s8s3_pure_product_membership.py"
SPEC = importlib.util.spec_from_file_location("n8_s8s3", SOURCE_PATH)
SOURCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE)

EXPECTED_LEDGER_SHA256 = (
    "8b6dc91610d0e4a8663d067211c1cdf7be2c3615027b49c81e144e99a400c0a9"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def component_sizes(edges):
    adjacency = [set() for _ in range(8)]
    for first, second in edges:
        left, right = first // 3, second // 3
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(range(8))
    sizes = []
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
        sizes.append(len(component))
    return tuple(sorted(sizes, reverse=True))


def selected_word(selected):
    word = [None] * 8
    for first, second in selected:
        left, left_colour = divmod(first, 3)
        right, right_colour = divmod(second, 3)
        require(word[left] is None and word[right] is None,
                "selected support edges repeat a vertex")
        word[left] = left_colour
        word[right] = right_colour
    require(all(value is not None for value in word),
            "selected support edges do not cover every vertex")
    return tuple(word)


def chart_record(row):
    mate = SOURCE.decode_key(row)
    edges = SOURCE.mate_edges(mate)
    require(len(edges) == 12, "target row is not a 24-port matching")
    mixed_types = Counter()
    pure = 0
    for selected in combinations(edges, 4):
        vertices = [port // 3 for edge in selected for port in edge]
        if len(set(vertices)) != 8:
            continue
        word = selected_word(selected)
        if len(set(word)) == 1:
            pure += 1
            continue
        selected_set = frozenset(selected)
        complement = tuple(edge for edge in edges if edge not in selected_set)
        require(len(complement) == 8, "support complement has wrong size")
        colour_counts = tuple(sorted(Counter(word).values(), reverse=True))
        cycles = component_sizes(complement)
        require(sum(cycles) == 8, "support complement lost vertices")
        mixed_types[colour_counts, cycles] += 1
    require(pure == 3, "target support does not have its three pure factors")
    require(sum(mixed_types.values()) > 0,
            "target support has no mixed one-factor")
    stabilizer = SOURCE.stabilizer_order(row)
    require(SOURCE.GROUP_ORDER % stabilizer == 0,
            "target stabilizer does not divide S8 x S3")
    return {
        "stabilizer": stabilizer,
        "orbit": SOURCE.GROUP_ORDER // stabilizer,
        "cubic_components": component_sizes(edges),
        "mixed_factors": sum(mixed_types.values()),
        "mixed_types": tuple(sorted(mixed_types.items())),
    }


def audit():
    rows = tuple(sorted(SOURCE.target_orbit_rows()))
    require(len(rows) == 31, "target matching triples do not have 31 orbits")
    records = tuple(chart_record(row) for row in rows)
    require(sum(record["orbit"] for record in records) == 105 ** 3,
            "localized chart orbits do not exhaust the pure target support")
    minimum_indices = tuple(
        index for index, record in enumerate(records, 1)
        if record["mixed_factors"] == 2
    )
    require(minimum_indices == (25, 26),
            "the two minimally coupled charts changed")
    support_mate = [-1] * 24
    for left, right, colour in SOURCE.SOURCE.COLOURED_SUPPORT:
        first, second = 3 * left + colour, 3 * right + colour
        support_mate[first] = second
        support_mate[second] = first
    support_key = SOURCE.canonical_key(tuple(support_mate))
    require(rows.index(support_key) + 1 == 26,
            "the expanded-prism support is no longer chart 26")
    require(records[24]["stabilizer"] == 8
            and records[24]["mixed_types"]
            == ((((4, 4), (8,)), 2),),
            "chart 25 extremal structure changed")
    require(records[25]["stabilizer"] == 4
            and records[25]["mixed_types"]
            == ((((4, 2, 2), (5, 3)), 2),),
            "chart 26 extremal structure changed")
    ledger = "".join(f"{index}:{row}:{record}\n"
                     for index, (row, record) in enumerate(zip(rows, records), 1))
    digest = sha256(ledger.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "localized chart ledger digest changed")
    return records, digest


def main():
    records, digest = audit()
    print("localized target-triple charts:", len(records))
    print("labelled target monomials:", sum(item["orbit"] for item in records))
    print("stabilizer histogram:", dict(sorted(Counter(
        item["stabilizer"] for item in records
    ).items())))
    print("cubic-component histogram:", dict(sorted(Counter(
        item["cubic_components"] for item in records
    ).items())))
    print("mixed-factor histogram:", dict(sorted(Counter(
        item["mixed_factors"] for item in records
    ).items())))
    print("minimum mixed factors:", min(item["mixed_factors"] for item in records))
    print("maximum mixed factors:", max(item["mixed_factors"] for item in records))
    print("minimally coupled charts:", (25, 26))
    print("expanded-prism chart:", 26)
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
