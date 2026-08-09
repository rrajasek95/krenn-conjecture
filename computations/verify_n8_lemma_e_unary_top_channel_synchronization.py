#!/usr/bin/env python3
"""Exact channel classification for the one-bad unary-top packet.

Choose one nonzero monochromatic near-perfect matching from each of the two
diagonal response rows.  When their ordered hole pairs are disjoint, this
checker classifies every possible pair of matching channels.  The only core
which is invisible both to the mixed top equation and to the two off-diagonal
response rows is a two-centre P3+P3 configuration.  A literal rational model
shows that this silent core really occurs for one common Q^[2]; it fails only
the unary top equation Q^[3]=X0.

This is a principal-channel theorem, not an aggregate noncancellation claim.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json


SITES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))

EXPECTED_DIGEST = "27738a4135c5507a9fee355ea2d0772cc4e8720b210611e76d541d8fd7b15642"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for mate in vertices[1:]:
        remainder = tuple(
            vertex for vertex in vertices if vertex not in (first, mate)
        )
        for tail in perfect_matchings(remainder):
            answer.append((tuple(sorted((first, mate))),) + tail)
    return tuple(answer)


MATCHINGS4 = {
    frozenset(vertices): perfect_matchings(vertices)
    for vertices in combinations(SITES, 4)
}
MATCHINGS6 = perfect_matchings(SITES)


def component_signature(edges):
    adjacency = {site: set() for site in SITES}
    for left, right in set(edges):
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    components = []
    for root in SITES:
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        vertices = []
        twice_edges = 0
        while stack:
            vertex = stack.pop()
            vertices.append(vertex)
            twice_edges += len(adjacency[vertex])
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        components.append((len(vertices), twice_edges // 2))
    return tuple(sorted(components))


def decorated_full_matchings(first, second):
    cells = tuple((edge, 1) for edge in first) + tuple(
        (edge, 2) for edge in second
    )
    answer = set()
    for selected in combinations(cells, 3):
        vertices = [vertex for edge, _ in selected for vertex in edge]
        if len(set(vertices)) != 6:
            continue
        if {colour for _, colour in selected} != {1, 2}:
            continue
        answer.add(tuple(sorted(selected)))
    return answer


def missing_pair(edge, other):
    if set(edge) & set(other):
        return None
    occupied = set(edge) | set(other)
    if len(occupied) != 4:
        return None
    return frozenset(set(SITES) - occupied)


def classify_channels():
    census = Counter()
    silent_examples = []
    configurations = 0
    for holes1 in permutations(SITES, 2):
        unused = tuple(site for site in SITES if site not in holes1)
        for holes2 in permutations(unused, 2):
            if set(holes1) & set(holes2):
                continue
            complement1 = frozenset(set(SITES) - set(holes1))
            complement2 = frozenset(set(SITES) - set(holes2))
            for matching1 in MATCHINGS4[complement1]:
                for matching2 in MATCHINGS4[complement2]:
                    configurations += 1
                    top = decorated_full_matchings(matching1, matching2)
                    offdiag12 = frozenset((holes1[0], holes2[1]))
                    offdiag21 = frozenset((holes2[0], holes1[1]))
                    same_p = frozenset((holes1[0], holes2[0]))
                    same_s = frozenset((holes1[1], holes2[1]))
                    mixed_holes = Counter()
                    for edge1 in matching1:
                        for edge2 in matching2:
                            holes = missing_pair(edge1, edge2)
                            if holes is not None:
                                mixed_holes[holes] += 1
                    offdiag = (
                        mixed_holes[offdiag12] + mixed_holes[offdiag21]
                    )
                    signature = component_signature(matching1 + matching2)
                    if top:
                        require(not offdiag,
                                "top- and off-diagonal-visible cases overlapped")
                        kind = f"top-visible:{len(top)}"
                    elif offdiag:
                        require(offdiag == 2,
                                "off-diagonal visibility stopped being paired")
                        require(mixed_holes[offdiag12] == 1,
                                "the 12 cross response lost its core term")
                        require(mixed_holes[offdiag21] == 1,
                                "the 21 cross response lost its core term")
                        kind = "offdiagonal-visible"
                    else:
                        require(signature == ((3, 2), (3, 2)),
                                "a non-P3+P3 silent channel appeared")
                        require(mixed_holes == Counter({same_p: 1, same_s: 1}),
                                "the silent cross cofactors stopped being same-side")
                        kind = "two-centre-silent"
                        if len(silent_examples) < 3:
                            silent_examples.append({
                                "p1_s1_holes": holes1,
                                "p2_s2_holes": holes2,
                                "colour1_matching": matching1,
                                "colour2_matching": matching2,
                                "mixed_cofactor_holes": sorted(
                                    tuple(sorted(pair)) for pair in mixed_holes
                                ),
                            })
                    census[(kind, signature)] += 1

    require(configurations == 3240,
            "the ordered disjoint-channel census changed")
    expected = Counter({
        ("top-visible:2", ((2, 1), (2, 1), (2, 1))): 360,
        ("top-visible:1", ((2, 1), (4, 3))): 1440,
        ("offdiagonal-visible", ((3, 2), (3, 2))): 720,
        ("two-centre-silent", ((3, 2), (3, 2))): 720,
    })
    require(census == expected, "the channel topology ledger changed")
    return census, silent_examples


def matching_polynomial(cells, vertices):
    """Return the decorated matching tensor on ``vertices``.

    ``cells`` maps (edge, left_colour, right_colour) to a rational integer
    coefficient; all examples here have coefficient one.
    """
    vertices = tuple(sorted(vertices))
    answer = Counter()
    for matching in perfect_matchings(vertices):
        choices = []
        for edge in matching:
            local = []
            for (cell_edge, left_colour, right_colour), coefficient in cells.items():
                if cell_edge == edge and coefficient:
                    local.append((left_colour, right_colour, coefficient))
            choices.append(local)
        for selected in product(*choices):
            word = [-1] * 6
            coefficient = 1
            for edge, (left_colour, right_colour, value) in zip(matching, selected):
                word[edge[0]] = left_colour
                word[edge[1]] = right_colour
                coefficient *= value
            answer[tuple(word[site] for site in vertices)] += coefficient
    return Counter({word: value for word, value in answer.items() if value})


def cofactor_tensor(cells, holes):
    vertices = tuple(site for site in SITES if site not in holes)
    return matching_polynomial(cells, vertices)


def star_product(left_star, right_star, cofactors):
    answer = Counter()
    for left_site, left_vector in left_star.items():
        for right_site, right_vector in right_star.items():
            if left_site == right_site:
                continue
            holes = frozenset((left_site, right_site))
            cofactor = cofactors[holes]
            vertices = tuple(site for site in SITES if site not in holes)
            for left_colour, left_value in enumerate(left_vector):
                if not left_value:
                    continue
                for right_colour, right_value in enumerate(right_vector):
                    if not right_value:
                        continue
                    for cofactor_word, coefficient in cofactor.items():
                        word = [-1] * 6
                        word[left_site] = left_colour
                        word[right_site] = right_colour
                        for site, colour in zip(vertices, cofactor_word):
                            word[site] = colour
                        answer[tuple(word)] += (
                            left_value * right_value * coefficient
                        )
    return Counter({word: value for word, value in answer.items() if value})


def pure_tensor(colour):
    return Counter({(colour,) * 6: 1})


def audit_silent_model():
    # Ordered holes are (p_i site, s_i site).  The two near-perfect
    # matchings form 2-4-1 and 3-5-0, hence P3+P3.  Their only mixed
    # two-edge cofactors miss the same-side pairs {p1,p2} and {s1,s2}.
    q_cells = Counter({
        ((2, 4), 1, 1): 1,
        ((3, 5), 1, 1): 1,
        ((0, 5), 2, 2): 1,
        ((1, 4), 2, 2): 1,
    })
    zero = (0, 0, 0)
    e1 = (0, 1, 0)
    e2 = (0, 0, 1)
    p = ({}, {0: e1}, {2: e2})
    s = ({}, {1: e1}, {3: e2})
    cofactors = {
        frozenset(holes): cofactor_tensor(q_cells, frozenset(holes))
        for holes in combinations(SITES, 2)
    }

    rows = {}
    for left in COLORS:
        for right in COLORS:
            value = star_product(p[left], s[right], cofactors)
            target = pure_tensor(left) if left == right and left in (1, 2) else Counter()
            require(value == target,
                    f"silent common-Q^[2] row {(left, right)} changed")
            rows[f"{left}{right}"] = sorted(
                ("".join(map(str, word)), coefficient)
                for word, coefficient in value.items()
            )

    q3 = matching_polynomial(q_cells, SITES)
    require(not q3, "the silent common quadratic acquired a top matching")

    d_cells = Counter({
        ((0, 1), 1, 1): 1,
        ((2, 3), 2, 2): 1,
    })
    q_plus_d = q_cells + d_cells
    bent_top = matching_polynomial(q_plus_d, SITES)
    require(bent_top == pure_tensor(1) + pure_tensor(2),
            "the silent bend stopped producing exactly X1+X2")

    # The two nonzero dependent-line sites at each endpoint are distinct.
    p_lines = {0: 1, 2: 2}
    s_lines = {1: 1, 3: 2}
    require(len(set(p_lines)) == len(set(s_lines)) == 2,
            "the singular-spoke sites collided")
    require(set(p_lines).isdisjoint(s_lines),
            "the displayed four singular-spoke sites stopped being distinct")

    # A three-cell all-zero completion of q would supply X0, but every one
    # of the fifteen physical perfect matchings creates at least one mixed
    # matching in q+d+M0.  This is a finite guard, not an all-support claim.
    completion_histogram = Counter()
    for matching in MATCHINGS6:
        completed = q_plus_d + Counter({
            (edge, 0, 0): 1 for edge in matching
        })
        top = matching_polynomial(completed, SITES)
        mixed = {
            word: coefficient for word, coefficient in top.items()
            if len(set(word)) > 1
        }
        require(mixed, "a pure-zero three-cell completion became exact")
        completion_histogram[len(mixed)] += 1
    require(completion_histogram == Counter({1: 3, 2: 6, 3: 1, 5: 3, 6: 2}),
            "the pure-zero completion histogram changed")

    return {
        "q_cells": [list(edge) + [left, right]
                    for edge, left, right in sorted(q_cells)],
        "rows": rows,
        "q3": [],
        "bent_top": sorted(
            ("".join(map(str, word)), coefficient)
            for word, coefficient in bent_top.items()
        ),
        "nonzero_singular_lines": {
            "p": p_lines,
            "s": s_lines,
        },
        "pure_zero_completion_mixed_word_histogram": dict(
            sorted(completion_histogram.items())
        ),
    }


def main():
    census, examples = classify_channels()
    model = audit_silent_model()
    ledger = {
        "ordered_disjoint_channel_census": {
            f"{kind}|{signature}": count
            for (kind, signature), count in sorted(census.items())
        },
        "silent_examples": examples,
        "exact_silent_common_cofactor_model": model,
        "verdict": {
            "top_visible": 1800,
            "offdiagonal_visible": 720,
            "two_centre_silent": 720,
            "aggregate_packet": (
                "open: selecting one nonzero summand does not prevent "
                "additional same-word cancellation"
            ),
        },
        "scope": (
            "complete classification of pairs of selected diagonal response "
            "matching channels with disjoint ordered holes; the rational model "
            "has literal common Q^[2] provenance and all nine response rows, "
            "but Q^[3]=0 rather than X0"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"unary-top channel ledger changed: {digest}")
    print("N=8 unary-top channel synchronization: PASS")
    print("ordered disjoint channels: 3240")
    print("top-visible=1800; offdiagonal-visible=720; two-centre-silent=720")
    print("exact silent common-Q^[2] model: all nine rows; Q^[3]=0")
    print("full unary-top packet: OPEN at aggregate cancellation/top lift")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
