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
EXPECTED_DIGEST = "02acb31305bdd83a5def44e9e5a6b9a12bf38743d32be49aaefd7fe4158ff942"


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
    """Audit the rank-case proof of the two-hole tensor lemma.

    Write x_r K_h+K_k y_r=E_rr tensor w_r for r=0,1.  A
    nonzero proportional relation x_1=alpha*x_0 makes the difference of
    the two targets have flattening rank two at the second hole, while the
    left side has rank at most one.  The alpha=0 boundary is the pure
    singleton split.  If both local star spans have rank two, the two
    target matrices become multiples of one crossed matrix J, impossible.
    """
    proportional_flattening = (
        ("-alpha", 0, 0, 0),
        (0, 0, 0, 1),
    )
    proportional_minor = "-alpha"
    e00 = (1, 0, 0, 0)
    e11 = (0, 0, 0, 1)
    target_minor = e00[0] * e11[3] - e00[3] * e11[0]
    require(target_minor == 1,
            "the two pure matrix targets lost independence")
    rank_cases = {
        "rank_X_0_or_rank_Y_0":
            "one common cofactor would be two distinct pure tensors",
        "rank_X_1_nonzero_proportional":
            "rank-two target flattening has minor -alpha",
        "rank_Y_1_nonzero_proportional":
            "transpose of the rank-X argument",
        "rank_X_1_zero_boundary": "pure singleton split",
        "rank_Y_1_zero_boundary": "pure singleton split",
        "rank_X_2_rank_Y_2":
            "E00 and E11 would be multiples of one crossed matrix J",
    }

    # This is a census of the tensor lemma's resulting active supports,
    # not a replacement for the rank argument above.
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
    return {
        "proportional_target_flattening": proportional_flattening,
        "proportional_nonzero_minor": proportional_minor,
        "independent_target_vectors": [e00, e11],
        "independent_target_minor": target_minor,
        "rank_cases": rank_cases,
        "active_support_table": table,
        "singleton_allocations": survivors,
    }, survivors


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
    split_audit, split_survivors = audit_two_hole_tensor_split()
    cycle_records = audit_cycle_gate()
    guard = audit_local_cancellation_guard()
    hole_histogram = Counter(record["mixed_hole"] for record in cycle_records)
    ledger = {
        "pinned_large_kernel_sha256": PINNED_LARGE_KERNEL_SHA256,
        "two_hole_tensor_split_audit": split_audit,
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
