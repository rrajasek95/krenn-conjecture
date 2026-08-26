#!/usr/bin/env python3
"""Lift the 14-row abstract (K,cycle) certificate to literal mixed columns."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import argparse
import csv
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TAIL_DIR = (ROOT / "computations"
            / "unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23")
TAIL_SCRIPT = TAIL_DIR / "audit_kcycle_abstract_refinement.py"
TAIL_RESULT = TAIL_DIR / "results_kcycle_abstract_refinement.json"
TAIL_CERT = TAIL_DIR / "kcycle_abstract_aT_certificate.tsv"
NEXT_DIR = (ROOT / "computations"
            / "unaudited-codex-orbit0-k16-smallest-dual-next-page-2026-08-23")
NEXT_SCRIPT = NEXT_DIR / "audit_k16_smallest_dual_next_page.py"
D24_SCRIPT = (ROOT / "computations"
              / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
              / "audit_orbit0_t2_pivot_setup.py")
RESULT = HERE / "results_literal_kcycle_certificate.json"
CERT = HERE / "literal_kcycle_aT_certificate.tsv"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


NEXT = load("literal_kcycle_next", NEXT_SCRIPT)
TAIL = load("literal_kcycle_tail", TAIL_SCRIPT)
F = NEXT.F
D24 = NEXT.D24


def cell_id(left, right):
    left_site, left_colour = left
    right_site, right_colour = right
    require(left_site != right_site, "illegal same-site cell")
    if left_site < right_site:
        cell = (left_site, right_site, left_colour, right_colour)
    else:
        cell = (right_site, left_site, right_colour, left_colour)
    require(cell in F.BASE.CELL_ID, f"missing legal cell {cell}")
    return F.BASE.CELL_ID[cell]


def port_degrees(row):
    degrees = Counter()
    for cell in row:
        left_site, right_site, left_colour, right_colour = F.BASE.CELLS[cell]
        degrees[(left_site, left_colour)] += 1
        degrees[(right_site, right_colour)] += 1
    return degrees


def cycle_partition(row):
    adjacency = defaultdict(list)
    for cell in row:
        left_site, right_site, left_colour, right_colour = F.BASE.CELLS[cell]
        left = (left_site, left_colour)
        right = (right_site, right_colour)
        adjacency[left].append(right)
        adjacency[right].append(left)
    require(adjacency and set(map(len, adjacency.values())) == {2},
            "row is not 2-regular")
    seen = set()
    parts = []
    for start in sorted(adjacency):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        parts.append(size)
    return tuple(sorted(parts))


def literal_multiplier(word, closed_partition):
    """Four selected anchor paths plus A' union its completion matching P."""
    selected = []
    remaining_anchors = []
    selected_ports = set()
    unselected_ports = set()
    for left_site, right_site in F.M0:
        selected_colour = word[left_site]
        require(word[right_site] == selected_colour,
                "word is not pair-constant")
        left = (left_site, selected_colour)
        right = (right_site, selected_colour)
        selected_ports.update((left, right))
        selected.append(cell_id(left, right))
        for colour in range(3):
            if colour == selected_colour:
                continue
            left = (left_site, colour)
            right = (right_site, colour)
            unselected_ports.update((left, right))
            remaining_anchors.append((left, right, cell_id(left, right)))
    require(len(selected_ports) == 8 and len(unselected_ports) == 16
            and selected_ports.isdisjoint(unselected_ports),
            "port split changed")

    iterator = iter(remaining_anchors)
    anchor_prime = []
    completion = []
    closed_rows = []
    for length in closed_partition:
        require(length >= 2 and length % 2 == 0,
                "closed part is not an even alternating cycle")
        group = [next(iterator) for _ in range(length // 2)]
        anchor_prime.extend(record[2] for record in group)
        if length == 2:
            # A doubled remaining-anchor edge is a literal 2-cycle.
            completion.append(group[0][2])
            closed_rows.append(bytes(sorted((group[0][2], group[0][2]))))
        else:
            connectors = []
            for index, record in enumerate(group):
                connector = cell_id(record[1],
                                    group[(index + 1) % len(group)][0])
                require(connector not in F.A,
                        "nontrivial alternating connector became an anchor")
                connectors.append(connector)
                completion.append(connector)
            closed_rows.append(bytes(sorted(
                tuple(record[2] for record in group) + tuple(connectors))))
    try:
        next(iterator)
        require(False, "closed partition did not consume all eight A' edges")
    except StopIteration:
        pass

    multiplier = bytes(sorted(tuple(selected) + tuple(anchor_prime)
                              + tuple(completion)))
    closed_graph = bytes(sorted(tuple(anchor_prime) + tuple(completion)))
    require(len(selected) == 4 and len(anchor_prime) == len(completion) == 8
            and len(multiplier) == 20 and len(closed_graph) == 16,
            "literal multiplier bidegree changed")
    selected_degrees = port_degrees(bytes(selected))
    closed_degrees = port_degrees(closed_graph)
    require(set(selected_degrees) == selected_ports
            and set(selected_degrees.values()) == {1},
            "selected paths are not four length-one anchor paths")
    require(set(closed_degrees) == unselected_ports
            and set(closed_degrees.values()) == {2},
            "A' union P is not 2-regular on the other sixteen ports")
    require(cycle_partition(closed_graph) == tuple(sorted(closed_partition)),
            "literal closed graph has wrong cycle partition")
    return multiplier, bytes(sorted(selected)), bytes(sorted(anchor_prime)), bytes(sorted(completion))


def actual_profile_vector(word, multiplier):
    outputs = D24.degree24_column_rows((word, multiplier))
    require(len(outputs) == 105 and len(set(outputs)) == 105,
            "literal source column lost completion terms")
    answer = Counter()
    for output in outputs:
        degrees = port_degrees(output)
        require(len(degrees) == 24 and set(degrees.values()) == {2},
                "completed literal row is not balanced 2-regular")
        answer[(D24.row_k_degree(output), cycle_partition(output))] += 1
    return answer


def build(mutate=False):
    pinned = {
        TAIL_SCRIPT: "cca88a20f64ff1d1bb62b72aacf4a64dc468da277fde411e5cf684746c080138",
        TAIL_RESULT: "d11c9829de043e0001a5744e07fc000e14a6e7afeff24d6580374b74b958b091",
        TAIL_CERT: "c2cc168b34ed0e9b731e86d41c945c2e264bc157a315c84433ded20142daacf7",
        NEXT_SCRIPT: "409be1569ea132ce7c564076be08f81bd9fd211d457207bbfb439e7d36fb1906",
        D24_SCRIPT: "71111eabf3822bc08678f19de0b1faf3fb61af12dd5e36acf04313de56bf7e8b",
    }
    for path, expected in pinned.items():
        require(file_sha256(path) == expected, f"frozen input drift: {path}")
    tail_result = json.loads(TAIL_RESULT.read_text())
    require(tail_result["logical_sha256"]
            == "cf69d53b23e346a7cc56e16dd6f4ae74f0fea14841d00c786122ef41cbd0c26a",
            "abstract certificate theorem drift")
    with TAIL_CERT.open() as handle:
        abstract_rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(abstract_rows) == 14, "abstract certificate row count changed")

    pair_colours = [values for values in product(range(3), repeat=4)
                    if len(set(values)) > 1]
    require(len(pair_colours) == 78, "mixed pair-constant word count changed")
    records = []
    combined = Counter()
    columns = set()
    words = set()
    for index, (abstract, colours) in enumerate(zip(abstract_rows,
                                                    pair_colours,
                                                    strict=False)):
        word = F.word_from_pair_colours(colours)
        require(len(set(word)) > 1, "selected source word became pure")
        closed = tuple(int(value) for value
                       in abstract["closed_cycle_partition"].split(","))
        multiplier, selected, anchor_prime, completion = literal_multiplier(
            word, closed)
        if mutate and index == 0:
            multiplier = bytes(sorted(multiplier[:-1] + multiplier[-2:-1]))
        column = (word, multiplier)
        require(column not in columns and word not in words,
                "literal source label/column collision")
        columns.add(column)
        words.add(word)
        anchor_count = sum(cell in F.A for cell in multiplier)
        require(anchor_count == int(abstract["multiplier_anchor_count"]),
                "literal multiplier anchor count changed")
        vector = actual_profile_vector(word, multiplier)
        expected = TAIL.abstract_profile_vector(anchor_count, closed)
        require(vector == expected and len(vector) == 5,
                "literal column differs from abstract completion profile")
        certificate_coefficient = int(abstract["certificate_coefficient"])
        for coordinate, value in vector.items():
            combined[coordinate] += certificate_coefficient * value
        records.append({
            "source_word": "".join(map(str, word)),
            "pair_colours": list(colours),
            "mixed": True,
            "multiplier": multiplier.hex(),
            "selected_anchor_paths": selected.hex(),
            "remaining_anchor_matching_A_prime": anchor_prime.hex(),
            "completion_matching_P": completion.hex(),
            "multiplier_anchor_count": anchor_count,
            "closed_cycle_partition": list(closed),
            "certificate_coefficient": certificate_coefficient,
            "profile_vector": [
                {"K_degree": coordinate[0],
                 "cycle_partition": list(coordinate[1]),
                 "multiplicity": value}
                for coordinate, value in sorted(vector.items())
            ],
        })

    one_colour, _types = TAIL.one_colour_vector()
    target = TAIL.convolve(TAIL.convolve(one_colour, one_colour), one_colour)
    require(combined == target and sum(combined.values()) == 105 ** 3,
            "literal 14-column certificate does not equal structured a*T")
    require(len(columns) == len(words) == len(records) == 14,
            "literal certificate distinctness changed")

    header = ["source_word", "multiplier", "multiplier_anchor_count",
              "closed_cycle_partition", "certificate_coefficient"]
    lines = ["\t".join(header)]
    for record in records:
        lines.append("\t".join((
            record["source_word"], record["multiplier"],
            str(record["multiplier_anchor_count"]),
            ",".join(map(str, record["closed_cycle_partition"])),
            str(record["certificate_coefficient"]))))
    certificate_payload = "\n".join(lines) + "\n"
    result = {
        "format": "n8-orbit0-literal-kcycle-aT-certificate-v1",
        "status": "EXACT_LITERAL_14_COLUMN_KCYCLE_MEMBERSHIP",
        "pinned": {str(path.relative_to(ROOT)): digest
                   for path, digest in pinned.items()},
        "literal_columns": len(records),
        "distinct_mixed_source_words": len(words),
        "completion_terms_per_column": 105,
        "weighted_completion_mass": sum(combined.values()),
        "target_coordinates": len(target),
        "exact_certificate_equality": True,
        "records": records,
        "certificate_tsv_sha256": sha256(
            certificate_payload.encode("ascii")).hexdigest(),
        "construction": (
            "For each pair-constant nonconstant word, take the four selected "
            "anchor edges, the eight remaining anchor edges A', and a legal "
            "perfect matching P on the sixteen unselected ports. A' union P "
            "has the requested alternating-cycle partition; P agrees with A' "
            "on exactly the 2-cycles, giving anchor count 12+c."),
        "conclusion": (
            "The actual literal mixed-column image in the (K-degree, cycle-"
            "partition) quotient contains the structured a*T vector. Hence "
            "this quotient cannot separate a*T; this is quotient membership, "
            "not full polynomial-ideal membership."),
        "scope_guard": (
            "Fourteen explicit degree-24 mixed source columns and their exact "
            "105-term (K,cycle) images only. Equality is after projection to "
            "that quotient and does not lift coefficients row-by-row in the "
            "252-variable source ring."),
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(payload.encode("ascii")).hexdigest()
    return result, certificate_payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result, certificate = build(mutate=args.mutate)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    CERT.write_text(certificate)
    print("literal 14-column (K,cycle) certificate: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
