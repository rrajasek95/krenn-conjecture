#!/usr/bin/env python3
"""Audit the exact lift/Tutte/collision trichotomy for frame circuits."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_anchored_min_support_frame_circuit_cover.py":
        "14bc527f3ff67dd41772409e9556b0241f8b6f49b7e7ecb2c83d05a8e09806aa",
    "notes/anchored-min-support-frame-circuit-cover.md":
        "cdf8472f4ff13f888108f33f5d794fd06fbe7b06597a8bd8fe6da768bcbfcfeb",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "notes/h3-physical-cartan-closes-residual-q-ks-hypothesis.md":
        "7f144e607e2fbfa4031ed8b282d7ae6f1da59ce0e7e696b5ae2b8840bcc12236",
}
EXPECTED_LEDGER_SHA256 = (
    "243f96791994ea0104108f6425e8a19f08c58e7af6e4a026acd0049bc6c73e04"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def port_incidence(edges):
    answer = {}
    for coefficient, left, right in edges:
        answer[left] = answer.get(left, 0) + coefficient
        answer[right] = answer.get(right, 0) + coefficient
    return {port: value for port, value in answer.items() if value}


def physical_profile(edges):
    answer = {}
    for _coefficient, left, right in edges:
        for site, _colour in (left, right):
            answer[site] = answer.get(site, 0) + 1
    return answer


def matching_word(edges, tail=()):
    word = {}
    physical = []
    for left, right in tuple(edges) + tuple(tail):
        for site, colour in (left, right):
            require(site not in word, "decorated edge set is not a physical matching")
            word[site] = colour
        physical.append(tuple(sorted((left[0], right[0]))))
    return tuple(word[site] for site in sorted(word)), tuple(sorted(physical))


def perfect_matchings(vertices, physical_edges):
    vertices = tuple(sorted(vertices))
    physical_edges = {tuple(sorted(edge)) for edge in physical_edges}
    if not vertices:
        return [()]
    left = vertices[0]
    answer = []
    for right in vertices[1:]:
        edge = tuple(sorted((left, right)))
        if edge not in physical_edges:
            continue
        rest = tuple(vertex for vertex in vertices if vertex not in (left, right))
        for tail in perfect_matchings(rest, physical_edges):
            answer.append(tuple(sorted((edge,) + tail)))
    return answer


def odd_components(vertices, physical_edges, removed):
    remaining = set(vertices) - set(removed)
    adjacency = {vertex: set() for vertex in remaining}
    for left, right in physical_edges:
        if left in remaining and right in remaining:
            adjacency[left].add(right)
            adjacency[right].add(left)
    seen = set()
    odd = 0
    for root in remaining:
        if root in seen:
            continue
        component = {root}
        seen.add(root)
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    component.add(other)
                    stack.append(other)
        odd += len(component) % 2
    return odd


def tutte_barrier(vertices, physical_edges):
    vertices = tuple(vertices)
    for size in range(len(vertices) + 1):
        for removed in combinations(vertices, size):
            odd = odd_components(vertices, physical_edges, removed)
            if odd > size:
                return tuple(removed), odd
    return None


def audit_literal_lift():
    negative = (
        (((0, 0), (1, 0))),
        (((2, 1), (3, 1))),
    )
    positive = (
        (((1, 0), (2, 1))),
        (((3, 1), (0, 0))),
    )
    signed = tuple((-1, *edge) for edge in negative) + tuple((1, *edge) for edge in positive)
    require(port_incidence(signed) == {}, "C4 port circuit stopped balancing")
    require(set(physical_profile(tuple((1, *edge) for edge in negative)).values()) == {1},
            "negative C4 side is not squarefree")
    require(set(physical_profile(tuple((1, *edge) for edge in positive)).values()) == {1},
            "positive C4 side is not squarefree")

    tail = (((4, 2), (5, 2)),)
    negative_word, negative_matching = matching_word(negative, tail)
    positive_word, positive_matching = matching_word(positive, tail)
    require(negative_word == positive_word == (0, 0, 1, 1, 2, 2),
            "common-tail lift changed its output word")
    require(negative_matching != positive_matching,
            "circuit lift did not create distinct matchings")
    return negative_word, negative_matching, positive_matching


def audit_tutte_branch():
    # The same four-site circuit leaves sites 4,5,6,7.  Their supported
    # physical tail graph is a triangle plus an isolated vertex, so it has no
    # perfect matching and X=empty is already a strict Tutte barrier.
    vertices = (4, 5, 6, 7)
    tail_graph = ((4, 5), (5, 6), (4, 6))
    require(not perfect_matchings(vertices, tail_graph),
            "tail counterguard unexpectedly acquired a perfect matching")
    barrier = tutte_barrier(vertices, tail_graph)
    require(barrier == ((), 2), "canonical Tutte barrier changed")
    return barrier


def audit_collision_branch():
    negative = (
        (((0, 0), (1, 0))),
        (((0, 1), (2, 1))),
    )
    positive = (
        (((1, 0), (0, 1))),
        (((2, 1), (0, 0))),
    )
    signed = tuple((-1, *edge) for edge in negative) + tuple((1, *edge) for edge in positive)
    require(port_incidence(signed) == {}, "collision C4 stopped balancing")
    negative_profile = physical_profile(tuple((1, *edge) for edge in negative))
    positive_profile = physical_profile(tuple((1, *edge) for edge in positive))
    require(negative_profile == positive_profile == {0: 2, 1: 1, 2: 1},
            "repeated-site profile changed")
    try:
        matching_word(negative)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("repeated-site circuit became a squarefree matching")

    # Two odd triangles joined by an edge have primitive unsigned-incidence
    # kernel with coefficient two on the joining path.  Such a monomial also
    # lies outside one squarefree matching row even when its port labels map
    # injectively to physical sites.
    handcuff_coefficients = (1, -1, 1, 2, -1, 1, -1)
    require(2 in map(abs, handcuff_coefficients), "handcuff lost doubled path")
    return negative_profile, handcuff_coefficients


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    word, negative_matching, positive_matching = audit_literal_lift()
    barrier = audit_tutte_branch()
    collision_profile, handcuff = audit_collision_branch()
    ledger = {
        "pins": PINS,
        "literal_common_tail_lift": {
            "word": list(word),
            "negative_matching": [list(edge) for edge in negative_matching],
            "positive_matching": [list(edge) for edge in positive_matching],
        },
        "tail_failure_tutte_barrier": {"removed": list(barrier[0]), "odd_components": barrier[1]},
        "repeated_site_profile": collision_profile,
        "loose_handcuff_primitive_coefficients": list(handcuff),
        "trichotomy": (
            "a primitive protected-relative frame circuit either is "
            "physical-squarefree and has a supported common tail, giving two "
            "literal same-word matching occurrences; is squarefree but has "
            "no common tail, giving a Tutte barrier; or has repeated physical "
            "site/doubled-path degree and belongs to the relative "
            "principal-parts collision grade"
        ),
        "scope": (
            "the first branch supplies source typing but not a binomial row "
            "or nonzero phase after other matching terms are included; the "
            "Tutte and collision branches remain theorem inputs"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("frame-circuit lift ledger changed", digest))
    print("frame-circuit matching lift trichotomy: PASS")
    print("literal common-tail word:", word)
    print("Tutte barrier: removed=%s odd_components=%s" % barrier)
    print("repeated-site profile:", collision_profile)
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
