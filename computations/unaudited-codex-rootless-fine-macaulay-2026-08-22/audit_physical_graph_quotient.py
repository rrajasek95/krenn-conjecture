#!/usr/bin/env python3
"""Exact physical-multigraph quotient of the rootless H/chi packets."""

from collections import Counter, defaultdict
from itertools import permutations, product
import json

P = 32003
ROOT = (0, 1, 2, 1, 1, 2, 2, 2)
SLICES = (
    (0, 1, 2, 1, 1, 2, 2, 2),
    (0, 1, 2, 0, 0, 0, 0, 0),
    (0, 1, 2, 1, 1, 1, 1, 1),
)
T_EDGES = ((0, 1), (0, 2), (1, 2))


def pms(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    u = vertices[0]
    out = []
    for pos in range(1, len(vertices)):
        v = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in pms(rest):
            out.append(((min(u, v), max(u, v)),) + tail)
    return tuple(out)


PM8 = pms(range(8))
PM6 = pms(range(6))


def cell(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return (u, v, a, b)


def parity(perm):
    return -1 if sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3)) % 2 else 1


def cofactors(word, selected):
    out = []
    for matching in PM8:
        if selected in matching:
            out.append(tuple(sorted(cell(u, v, word[u], word[v]) for u, v in matching if (u, v) != selected)))
    assert len(out) == 15
    return out


def add(poly, term, coefficient):
    poly[term] = (poly[term] + coefficient) % P
    if poly[term] == 0:
        del poly[term]


def holonomy():
    cof = [[cofactors(word, edge) for edge in T_EDGES] for word in SLICES]
    out = defaultdict(int)
    for perm in permutations(range(3)):
        sign = parity(perm)
        for a, b, c in product(cof[0][perm[0]], cof[1][perm[1]], cof[2][perm[2]]):
            add(out, tuple(sorted(a + b + c)), sign)
    assert len(out) == 18630
    return dict(out)


def response_terms(edge, alpha, beta, colour):
    u, v = edge
    return (
        (cell(6, u, colour, alpha), cell(7, v, colour, beta)),
        (cell(6, v, colour, beta), cell(7, u, colour, alpha)),
    )


def chi():
    out = defaultdict(int)
    for matching in PM6:
        for ordinary in range(3):
            rs = [x for x in range(3) if x != ordinary]
            for cp in permutations(range(3)):
                for orientations in product(range(2), repeat=2):
                    term = [cell(6, 7, cp[0], cp[0])]
                    u, v = matching[ordinary]
                    term.append(cell(u, v, ROOT[u], ROOT[v]))
                    for k in range(2):
                        u, v = matching[rs[k]]
                        term.extend(response_terms((u, v), ROOT[u], ROOT[v], cp[k + 1])[orientations[k]])
                    add(out, tuple(sorted(term)), 1)
        for cp in permutations(range(3)):
            for orientations in product(range(2), repeat=3):
                term = []
                for k, (u, v) in enumerate(matching):
                    term.extend(response_terms((u, v), ROOT[u], ROOT[v], cp[k])[orientations[k]])
                add(out, tuple(sorted(term)), 1)
    assert len(out) == 1800
    return dict(out)


def localizers():
    edges = ((3, 4), (3, 5), (4, 5))
    out = set()
    for choices in product(range(2), repeat=3):
        colours = {}
        for offset, site in enumerate((3, 4, 5)):
            incident = [e for e in edges if site in e]
            colours[(incident[choices[offset]], site)] = 0
            colours[(incident[1 - choices[offset]], site)] = 1
        out.add(tuple(sorted(cell(u, v, colours[((u, v), u)], colours[((u, v), v)]) for u, v in edges)))
    assert len(out) == 8
    return sorted(out)


def physical_graph(term):
    return tuple(sorted((u, v) for u, v, _, _ in term))


def degree_sequence(graph):
    degree = [0] * 8
    for u, v in graph:
        degree[u] += 1
        degree[v] += 1
    return tuple(degree)


def packet_profile(poly):
    by_graph = defaultdict(lambda: [0, 0])
    for term, coefficient in poly.items():
        graph = physical_graph(term)
        by_graph[graph][0] += 1
        by_graph[graph][1] = (by_graph[graph][1] + coefficient) % P
    return by_graph


def main():
    h = holonomy()
    c = chi()
    loc = localizers()
    c_loc = defaultdict(int)
    for term, coefficient in c.items():
        for multiplier in loc:
            add(c_loc, tuple(sorted(term + multiplier)), coefficient)
    hp = packet_profile(h)
    cp = packet_profile(c_loc)
    hg = set(hp)
    cg = set(cp)
    both = hg & cg
    h_projected_nonzero = sum(values[1] != 0 for values in hp.values())
    c_projected_nonzero = sum(values[1] != 0 for values in cp.values())
    assert h_projected_nonzero == 0
    result = {
        "status": "PASS exact physical-multigraph quotient",
        "holonomy_terms": len(h),
        "clean_localized_terms": len(c_loc),
        "holonomy_physical_graphs": len(hg),
        "clean_physical_graphs": len(cg),
        "common_physical_graphs": len(both),
        "holonomy_only_physical_graphs": len(hg - cg),
        "clean_only_physical_graphs": len(cg - hg),
        "holonomy_projected_polynomial_terms": h_projected_nonzero,
        "clean_projected_polynomial_terms": c_projected_nonzero,
        "holonomy_degree_sequences": {str(k): v for k, v in Counter(degree_sequence(g) for g in hg).items()},
        "clean_degree_sequences": {str(k): v for k, v in Counter(degree_sequence(g) for g in cg).items()},
        "common_graph_term_totals": {
            "holonomy": sum(hp[g][0] for g in both),
            "clean": sum(cp[g][0] for g in both),
        },
        "coefficient_sum_agreement_on_common_graphs": sum(hp[g][1] == cp[g][1] for g in both),
        "lex_holonomy_only_graph": str(min(hg - cg)) if hg - cg else None,
        "lex_clean_only_graph": str(min(cg - hg)) if cg - hg else None,
        "scope": "Forgets every endpoint colour and retains the complete labelled physical edge multiset. Coefficient sums are reduced modulo 32003 only after exact decorated-term collection.",
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
