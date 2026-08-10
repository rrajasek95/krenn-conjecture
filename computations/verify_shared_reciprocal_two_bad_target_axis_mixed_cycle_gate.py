#!/usr/bin/env python3
"""Force a binary colour two-cycle in every large target-axis mixed escape.

The >=3-centre argument first kills the binary cofactors on the kernel
support.  With at most two holes left, two distinct pure images force the
remaining cofactors to split as pure-a and pure-c even for arbitrary binary
2x2 internal blocks.  A selected aa matching and cc matching contain
disjoint edges.  Their mixed 2+2 coefficient has three physical matching
terms; cancelling the named nonzero diagonal product requires one of the
other terms, hence two off-diagonal a/c cells of the same transition type.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(5))
A, C = range(2)
PINNED_LARGE_KERNEL_SHA256 = (
    "26d44835a02bdb9d39e8054753c0ce31dd15a8ac38212dcc07a6e6353f03f9fa"
)
EXPECTED_DIGEST = "67deace6e4c2c42383e10918d6c51caca812dc9bd69af6274d0b049860ec2897"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_large_kernel_exclusion.py"
    )
    require(path.exists(), "the large-kernel dependency is missing")
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINNED_LARGE_KERNEL_SHA256,
            f"the large-kernel dependency changed: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def audit_two_hole_tensor_split():
    """Audit the complete active-support split for two pure rows.

    A pure-d equation using hole h forces K_h to have factor e_d at the
    other hole.  Thus a nonzero cofactor cannot be active for both d=a,c.
    Each pure target needs an active hole, so on two holes the only possible
    active-support patterns are the two singleton bijections.
    """
    nonempty = ((0,), (1,), (0, 1))
    table = []
    survivors = []
    for a_support in nonempty:
        for c_support in nonempty:
            overlap = tuple(sorted(set(a_support) & set(c_support)))
            feasible = not overlap
            table.append({
                "a_support": a_support,
                "c_support": c_support,
                "overlap": overlap,
                "feasible": feasible,
            })
            if feasible:
                survivors.append((a_support, c_support))
    require(survivors == [((0,), (1,)), ((1,), (0,))],
            "the abstract two-hole pure split changed")
    return table, survivors


def compatible_terms(vertices, word):
    terms = []
    for matching in perfect_matchings(vertices):
        cells = tuple(
            (edge, word[edge[0]], word[edge[1]])
            for edge in matching
        )
        terms.append(cells)
    return terms


def audit_cycle_gate():
    records = []
    for h, k in combinations(SITES, 2):
        a_vertices = set(SITES) - {h}
        c_vertices = set(SITES) - {k}
        for a_matching in perfect_matchings(a_vertices):
            for c_matching in perfect_matchings(c_vertices):
                pairs = [
                    (a_edge, c_edge)
                    for a_edge in a_matching
                    for c_edge in c_matching
                    if set(a_edge).isdisjoint(c_edge)
                ]
                require(pairs,
                        "pure matching monomials lost their disjoint pair")
                a_edge, c_edge = pairs[0]
                vertices = tuple(sorted(set(a_edge) | set(c_edge)))
                hole = next(iter(set(SITES) - set(vertices)))
                word = {
                    **{site: A for site in a_edge},
                    **{site: C for site in c_edge},
                }
                terms = compatible_terms(vertices, word)
                selected = tuple(sorted((
                    (tuple(sorted(a_edge)), A, A),
                    (tuple(sorted(c_edge)), C, C),
                )))
                require(selected in terms,
                        "the named diagonal matching left its mixed word")
                alternate = [term for term in terms if term != selected]
                require(len(terms) == 3 and len(alternate) == 2,
                        "a binary 2+2 coefficient lost its three matchings")
                for term in alternate:
                    require(all(left != right for _edge, left, right in term),
                            "an alternate 2+2 matching was not off-diagonal")
                    require({tuple(sorted((left, right)))
                             for _edge, left, right in term} == {(A, C)},
                            "an alternate matching changed colour transition")

                records.append({
                    "bright_holes": (h, k),
                    "a_matching": a_matching,
                    "c_matching": c_matching,
                    "mixed_hole": hole,
                    "selected_diagonal_term": selected,
                    "alternate_two_cycles": alternate,
                })
    require(len(records) == 90,
            "the mixed-cycle gate census changed")
    return records


def audit_local_cancellation_guard():
    # Word 0011 on vertices 0,1,2,3.  The selected diagonal matching has
    # coefficient +1 and one off-diagonal alternate has coefficient -1.
    word = {0: A, 1: A, 2: C, 3: C}
    terms = compatible_terms((0, 1, 2, 3), word)
    weights = {
        ((0, 1), A, A): 1,
        ((2, 3), C, C): 1,
        ((0, 2), A, C): 1,
        ((1, 3), A, C): -1,
    }
    values = []
    for term in terms:
        value = 1
        for cell in term:
            value *= weights.get(cell, 0)
        values.append(value)
    require(values == [1, -1, 0],
            "the local mixed two-cycle cancellation guard changed")
    require(sum(values) == 0,
            "the local mixed coefficient stopped cancelling")
    return {"word": tuple(word[index] for index in range(4)),
            "matching_values": values}


def audit():
    pin_dependency()
    split_table, split_survivors = audit_two_hole_tensor_split()
    cycle_records = audit_cycle_gate()
    guard = audit_local_cancellation_guard()
    hole_histogram = Counter(record["mixed_hole"] for record in cycle_records)
    ledger = {
        "pinned_large_kernel_sha256": PINNED_LARGE_KERNEL_SHA256,
        "two_hole_split_table": split_table,
        "two_hole_split_survivors": split_survivors,
        "cycle_records": cycle_records,
        "mixed_hole_histogram": dict(sorted(hole_histogram.items())),
        "local_cancellation_guard": guard,
        "verdict": (
            "every arbitrary-binary large target-axis kernel escape with "
            "two bright pure images activates a doubled a/c transition"
        ),
        "scope": (
            "the kernel row is genuinely target-axis; arbitrary mixed "
            "kernel rows can receive the first parity transgression"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"the mixed-cycle gate ledger changed: {digest}")
    return digest, hole_histogram


def main():
    digest, histogram = audit()
    print("two-bad target-axis mixed-cycle gate: PASS")
    print("two-hole pure allocations: 2")
    print("pure matching-pair audits: 90")
    print("mixed-hole histogram:", dict(sorted(histogram.items())))
    print("every escape requires two off-diagonal cells of one transition")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
