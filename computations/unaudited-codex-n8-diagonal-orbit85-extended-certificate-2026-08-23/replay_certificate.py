#!/usr/bin/env python3
"""Replay the compact orbit-85 arithmetic proof DAG and its tail guard."""

from __future__ import annotations

import collections
import importlib.util
import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "certificate_dag.json"
ENCODER = ROOT / "computations/verify_eight_site_diagonal_obstruction.py"
PROVENANCE = (ROOT / "computations/"
              "unaudited-codex-n8-diagonal-orbit85-clause-provenance-2026-08-23/"
              "check_provenance.py")


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sorted_clause(clause):
    return tuple(sorted(clause, key=lambda literal: (abs(literal), literal)))


def freeze(value):
    if isinstance(value, list):
        return tuple(freeze(item) for item in value)
    return value


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def main() -> None:
    # Replay every uniform source-clause identity first.
    provenance = load_module("orbit85_provenance", PROVENANCE)
    provenance.verify_a2()
    for terms in (3, 5, 7):
        provenance.verify_laplace(terms)
    provenance.verify_open_unit_clause()
    provenance.verify_c0()
    provenance.verify_xf()

    encoder_module = load_module("n8diag_certified", ENCODER)
    case, _orbit_size = encoder_module.orbit_reps(8)[85]
    encoder = encoder_module.Enc(8, case, k=4).build()
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(data["format"] == "n8diag-orbit85-extended-ns-dag-v1",
            "certificate format changed")

    antecedents = data["antecedents"]
    antecedent_ids = {row["id"] for row in antecedents}
    require(len(antecedent_ids) == len(antecedents) == 13670,
            "antecedent IDs are duplicated or incomplete")
    expected_kinds = {
        "mixed_diagonal_amplitude": 1638,
        "boolean_axiom": 5592,
        "selector_zero_link": 384,
        "selector_guarded_inverse": 384,
        "laplace_witness_definition": 5208,
        "inside_free_product_zero": 448,
        "outside_free_complement_localizer": 7,
        "unguarded_open_localizer": 9,
    }
    require(collections.Counter(row["kind"] for row in antecedents)
            == expected_kinds, "antecedent kind census changed")
    for row in antecedents:
        if row["kind"] == "outside_free_complement_localizer":
            require(len(row["split_rows"]) == 32,
                    "outside-free localizer lacks 32 residual splits")
            require(all(item["source_amplitude"] in antecedent_ids
                        for item in row["split_rows"]),
                    "outside-free localizer has a missing source row")

    node_clause = {}
    node_degree = {}
    seen_nodes = set()
    resolution_count = weakening_count = compile_count = 0
    amplitude_refs = []
    for node in data["proof_nodes"]:
        node_id = node["id"]
        require(node_id not in seen_nodes, f"duplicate node {node_id}")
        seen_nodes.add(node_id)
        operation = node["op"]
        if operation == "compile_clause":
            compile_count += 1
            cid = node["cnf_clause_id"]
            require(tuple(node["clause"]) == encoder.cls[cid - 1],
                    f"compiled clause {cid} differs from certified CNF")
            require(freeze(node["compiler"]["tag"]) == encoder.tags[cid - 1],
                    f"compiled tag {cid} differs from certified encoder")
            require(all(ref in antecedent_ids
                        for ref in node["compiler"]["antecedents"]),
                    f"compiled clause {cid} has missing antecedent")
            amplitude_refs += [
                ref for ref in node["compiler"]["antecedents"]
                if ref.startswith("amp:")
            ]
            node_clause[node_id] = tuple(node["clause"])
            node_degree[node_id] = node["compiler"]["arithmetic_degree_bound"]
        elif operation == "resolve_polynomials":
            resolution_count += 1
            require(node["left"] in node_clause and node["right"] in node_clause,
                    f"resolution node {node_id} has a forward reference")
            left = set(node_clause[node["left"]])
            right = set(node_clause[node["right"]])
            pivot = node["pivot_literal_in_right"]
            require(pivot in right and -pivot in left,
                    f"resolution node {node_id} has wrong pivot")
            left_without = left - {-pivot}
            right_without = right - {pivot}
            expected_left_factors = sorted_clause(right_without - left_without)
            expected_right_factors = sorted_clause(left_without - right_without)
            expected_result = sorted_clause(left_without | right_without)
            require(tuple(node["left_falsity_factors"]) == expected_left_factors,
                    f"left multiplier mismatch at {node_id}")
            require(tuple(node["right_falsity_factors"]) == expected_right_factors,
                    f"right multiplier mismatch at {node_id}")
            require(tuple(node["result_clause"]) == expected_result,
                    f"resolvent mismatch at {node_id}")
            # This is the arithmetic identity
            # m_B*M_(A or -x) + m_A*M_(B or x) = M_(A union B).
            node_clause[node_id] = expected_result
            node_degree[node_id] = max(
                node_degree[node["left"]] + len(expected_left_factors),
                node_degree[node["right"]] + len(expected_right_factors))
        elif operation == "weaken_polynomial":
            weakening_count += 1
            require(node["input"] in node_clause,
                    f"weakening node {node_id} has a forward reference")
            source = set(node_clause[node["input"]])
            added = set(node["added_falsity_factors"])
            expected = sorted_clause(source | added)
            require(tuple(node["result_clause"]) == expected,
                    f"weakening mismatch at {node_id}")
            node_clause[node_id] = expected
            node_degree[node_id] = (node_degree[node["input"]]
                                    + len(node["added_falsity_factors"]))
        else:
            raise RuntimeError(f"unknown proof operation {operation}")

    require((compile_count, resolution_count, weakening_count) == (502, 1652, 5),
            "proof operation census changed")
    require(data["root"] in node_clause and node_clause[data["root"]] == (),
            "root is not the empty-clause polynomial 1")
    require(max(node_degree.values()) == data["stats"]["max_arithmetic_degree_bound"],
            "arithmetic degree bound changed")
    require(len(seen_nodes) == data["stats"]["dag_nodes"] == 2159,
            "DAG node count changed")

    # Literal tail audit: all amplitude leaves have even colour-class sizes.
    # Enumerate all 105 matchings to verify coefficient order 1 is empty and
    # the coefficient-order-2 term census for every distinct leaf.
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105, "K8 matching census changed")
    distinct = sorted(set(amplitude_refs))
    profile_counts = collections.Counter()
    tail2_total = 0
    for identifier in distinct:
        masks = tuple(map(int, identifier.split(":")[1:]))
        sizes = tuple(sorted((mask.bit_count() for mask in masks), reverse=True))
        profile_counts[sizes] += 1
        word = {}
        for colour, mask in enumerate(masks):
            for site in range(8):
                if mask & (1 << site):
                    require(site not in word, "amplitude masks overlap")
                    word[site] = colour
        require(len(word) == 8, "amplitude masks do not partition K8")
        histogram = collections.Counter(
            sum(word[i] != word[j] for i, j in matching)
            for matching in matchings)
        require(histogram[1] == 0, f"linear tail term found in {identifier}")
        expected_tail2 = {(6, 2, 0): 90, (4, 4, 0): 72, (4, 2, 2): 30}[sizes]
        require(histogram[2] == expected_tail2,
                f"quadratic tail census changed for {identifier}")
        tail2_total += histogram[2]
    require(profile_counts == {(4, 2, 2): 154, (6, 2, 0): 22,
                               (4, 4, 0): 9},
            f"distinct amplitude profile census changed: {profile_counts}")
    require(tail2_total == 7248, "distinct Tail2 support count changed")
    require(len(amplitude_refs) == 569 and len(distinct) == 185,
            "tail amplitude reference census changed")

    print(json.dumps({
        "verdict": "VERIFIED_EXTENDED_RING_DAG_AND_QUADRATIC_TAIL_INTERFACE",
        "root": data["root"],
        "antecedents": len(antecedents),
        "proof_nodes": len(seen_nodes),
        "max_arithmetic_degree_bound": max(node_degree.values()),
        "epsilon_order_1_coefficient": 0,
        "first_possible_tail_order": 2,
        "distinct_tail_amplitude_leaves": len(distinct),
        "distinct_Tail2_monomial_occurrences": tail2_total,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
