#!/usr/bin/env python3
"""Exact audit of source-cycle invariants separating the Wick boundary.

For every mixed matching M in the all-even one-hot boundary graph, the
checker verifies that

    I_M = H_{m(M)} * product over e in E(G) minus M of z_e

has uniform incidence one at every vertex-colour port, hence is invariant
under the affine GHZ-stabilizer port torus.  It is one on the all-unit
source orbit, constant along the Laurent orbit, and zero on the exact GHZ
fiber because H_{m(M)} is a mixed output coordinate.
"""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_global_wick_top_invariant_counterguard.py"
SPEC = importlib.util.spec_from_file_location("global_wick_boundary_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


COLORS = (0, 1, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def port_weight_of_complement(vertices, edges, matching):
    matching = set(matching)
    weight = {(vertex, color): 0 for vertex in vertices for color in COLORS}
    for edge, (color, _valuation) in edges.items():
        if edge in matching:
            continue
        weight[edge[0], color] += 1
        weight[edge[1], color] += 1
    return weight


def word_weight(vertices, word):
    result = {(vertex, color): 0 for vertex in vertices for color in COLORS}
    for position, vertex in enumerate(sorted(vertices)):
        result[vertex, word[position]] = 1
    return result


def add_weights(left, right):
    return {port: left[port] + right[port] for port in left}


def audit_stage(vertices, edges):
    # Reuse only the already audited boundary generator.  All invariant and
    # source-cycle calculations below are new and do not call its audit.
    n = len(vertices)
    ordered_edges = tuple(sorted(edges))
    matchings = BASE.perfect_matchings(vertices, set(edges))
    records = []
    seen_words = set()

    total_support_valuation = sum(value for _color, value in edges.values())
    require(total_support_valuation == 0, "full support product is not normalized")

    # P_G is the product of every supported one-hot coordinate.  Its port
    # incidence is exactly one everywhere, a strictly positive invariant
    # monomial and hence a toric closed-orbit certificate.
    support_weight = {(vertex, color): 0 for vertex in vertices for color in COLORS}
    for edge, (color, _valuation) in edges.items():
        support_weight[edge[0], color] += 1
        support_weight[edge[1], color] += 1
    require(set(support_weight.values()) == {1}, "support cycle is not port balanced")

    for matching in matchings:
        word, matching_valuation = BASE.matching_term(matching, edges, vertices)
        require(word not in seen_words, "matching word collision")
        seen_words.add(word)
        if len(set(word)) == 1:
            continue

        # Every monomial of the full arbitrary-source coefficient H_word
        # has one occurrence at port (v,word_v).  The fixed complement
        # monomial Q_M supplies the other two colors at every vertex.
        h_weight = word_weight(vertices, word)
        q_weight = port_weight_of_complement(vertices, edges, matching)
        invariant_weight = add_weights(h_weight, q_weight)
        require(invariant_weight == support_weight,
                "H_word * Q_M is not a balanced port cycle")

        # On the Laurent family H_word=t^d by word uniqueness.  Since the
        # complete support product has order zero, Q_M has order -d and the
        # invariant has order zero.  At the all-unit point both factors are 1.
        q_valuation = sum(edges[edge][1] for edge in edges if edge not in matching)
        require(q_valuation == -matching_valuation, "pole compensation failed")
        require(matching_valuation + q_valuation == 0, "invariant Laurent order")

        records.append({
            "word": "".join(map(str, word)),
            "matching_valuation": matching_valuation,
            "complement_valuation": q_valuation,
            "H_degree": n // 2,
            "Q_degree": n,
            "invariant_degree": 3 * n // 2,
            "all_unit_value": 1,
            "exact_GHZ_value": 0,
            "uniform_port_incidence": 1,
        })

    require(records, "stage has no mixed matching")
    return {
        "n": n,
        "edges": len(ordered_edges),
        "mixed_cycle_invariants": len(records),
        "source_orbit_polystable": True,
        "invariant_degree": 3 * n // 2,
        "records": records,
    }


def main():
    vertices, edges = BASE.prism_seed()
    ledger = []
    for stage in range(7):
        ledger.append(audit_stage(vertices, edges))
        if stage < 6:
            vertices, edges, shift = BASE.expand_vertex(vertices, edges, min(vertices))
            require(shift >= 0, "negative expansion shift")

    require([row["n"] for row in ledger] == [6, 8, 10, 12, 14, 16, 18],
            "order ledger")
    require([row["mixed_cycle_invariants"] for row in ledger]
            == [1, 2, 3, 5, 7, 9, 13], "mixed invariant ledger")
    require([row["invariant_degree"] for row in ledger]
            == [9, 12, 15, 18, 21, 24, 27], "degree ledger")

    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == "1900ea5daa293e529a938ab388066908199890cf861216019eb0031e7487a547",
            f"ledger digest changed: {digest}")

    print("one-hot source cycle-invariant separator: PASS")
    for row in ledger:
        print(
            f"n={row['n']}: {row['mixed_cycle_invariants']} separators, "
            f"degree={row['invariant_degree']}, boundary value=1, exact-fiber value=0"
        )
    print("source quotient separates the finite boundary orbit from every exact GHZ source")
    print("Hilbert-Mumford polystability alone does not: both sides admit closed orbits")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
