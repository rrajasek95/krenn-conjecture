#!/usr/bin/env python3
"""Exact N=8 classification of four-or-more reciprocal witness pairs.

This checker separates what follows from the selected-witness and endpoint
essential-incidence axioms from what needs matching-coefficient exactness.
It proves the reciprocal-graph dichotomy and checks explicit local-incidence
counterguards for every 4<=r<=12.  In particular it audits why selected
degree three is not literal cubicity: unselected nonzero rank-one blocks may
remain.  The counterguards are not exact matching sources.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
from pathlib import Path


N = 8
COLORS = {0, 1, 2}
ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "computations/verify_n8_rankone_good_pair_essential_count.py":
        "45bdaae7b4cced397c80e6a7bb4fdb53961f15b2832c94cd3329093d82a730e4",
    "computations/verify_axis_purified_one_sided_pure_cover.py":
        "736c034c7b433b749317d5642b3852613bfe76041736fe1fadc94ad259eb481e",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(u, v):
    require(u != v, "loop is not a physical pair")
    return tuple(sorted((u, v)))


def pin_dependencies():
    for relative, expected in PINNED.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency drift: {relative}")


def reciprocal_graph_dichotomy():
    """No shared endpoint means a matching; four edges then cover K8."""

    all_edges = tuple(combinations(range(N), 2))
    four_matchings = []
    for chosen in combinations(all_edges, 4):
        degrees = [sum(u in pair for pair in chosen) for u in range(N)]
        if max(degrees) <= 1:
            require(degrees == [1] * N,
                    "four disjoint reciprocal pairs did not cover all sites")
            four_matchings.append(chosen)
    require(len(four_matchings) == 105,
            "perfect-matching count on eight labelled sites changed")
    # A graph with no shared endpoint is a matching, hence has at most N/2
    # edges.  Thus r>=5 is necessarily in the shared-endpoint branch.
    require(N // 2 == 4, "matching threshold changed")
    return len(four_matchings)


def selected_degree_three_ledger():
    """Count sites forced to have degree three only in the selected graph."""

    ledger = []
    for reciprocal in range(4, 13):
        single_arcs = 24 - 2 * reciprocal
        # A site has selected physical degree 3 plus the number of incoming
        # single arcs.  At most `single_arcs` sites receive one, so at least
        # 8-single_arcs sites have degree exactly three in the selected
        # witness graph.  This is *not* literal cubicity: blocks outside the
        # selected graph may remain nonzero.
        forced = max(0, N - single_arcs)
        ledger.append((reciprocal, single_arcs, forced))
    require(ledger == [
        (4, 16, 0), (5, 14, 0), (6, 12, 0), (7, 10, 0),
        (8, 8, 0), (9, 6, 2), (10, 4, 4), (11, 2, 6),
        (12, 0, 8),
    ], "reciprocal/single/cubic ledger changed")

    require(all(forced >= 4 for reciprocal, _single, forced in ledger
                if reciprocal >= 10),
            "high-reciprocity selected-degree threshold changed")
    return ledger


def axes_from_essential(essential, triples):
    """Build a coordinate-axis endpoint model from (common,e1,e2)."""

    axes = {}
    for u in range(N):
        first, second = sorted(essential[u])
        common, first_axis, second_axis = triples[u]
        axes[u] = {}
        for v in range(N):
            if v == u:
                continue
            axes[u][v] = (first_axis if v == first else
                          second_axis if v == second else common)
    return axes


def r4_matching_model():
    out = {u: ((u + 1) % N, (u + 2) % N, (u + 4) % N)
           for u in range(N)}
    essential = {
        0: (2, 6), 1: (2, 7), 2: (4, 6), 3: (1, 7),
        4: (0, 3), 5: (1, 3), 6: (4, 5), 7: (0, 5),
    }
    triples = {
        0: (0, 1, 2), 1: (1, 0, 2), 2: (2, 1, 0),
        3: (2, 0, 1), 4: (1, 0, 2), 5: (2, 1, 0),
        6: (0, 1, 2), 7: (1, 2, 0),
    }
    axes = axes_from_essential(essential, triples)
    # Restrict the generated complete endpoint table to selected pairs.
    selected = {edge(u, v) for u, neighbors in out.items() for v in neighbors}
    axes = {u: {v: a for v, a in axes[u].items() if edge(u, v) in selected}
            for u in range(N)}
    return out, axes


def r4_shared_model():
    out = {
        0: (1, 2, 4), 1: (0, 2, 5), 2: (0, 1, 4), 3: (1, 2, 4),
        4: (0, 5, 6), 5: (3, 6, 7), 6: (0, 2, 7), 7: (0, 1, 3),
    }
    essential = {
        0: (2, 6), 1: (3, 5), 2: (1, 3), 3: (4, 5),
        4: (0, 6), 5: (4, 7), 6: (2, 7), 7: (0, 1),
    }
    triples = {
        0: (0, 1, 2), 1: (2, 1, 0), 2: (0, 1, 2),
        3: (1, 2, 0), 4: (0, 1, 2), 5: (2, 1, 0),
        6: (2, 0, 1), 7: (1, 0, 2),
    }
    axes = axes_from_essential(essential, triples)
    selected = {edge(u, v) for u, neighbors in out.items() for v in neighbors}
    axes = {u: {v: a for v, a in axes[u].items() if edge(u, v) in selected}
            for u in range(N)}
    return out, axes


# The following exact endpoint-axis tables were found once and are replayed
# without a solver.  Each table assigns one coordinate line to each endpoint
# of every selected physical rank-one block.
MODELS = {
    "r4_matching": r4_matching_model(),
    "r4_shared": r4_shared_model(),
    "r5_shared": (
        {0:(3,4,5),1:(0,2,3),2:(1,4,7),3:(4,5,7),
         4:(0,2,3),5:(1,4,7),6:(2,3,7),7:(0,1,3)},
        {0:{1:1,3:2,4:0,5:1,7:0},1:{0:2,2:0,3:0,5:1,7:2},
         2:{1:0,4:2,6:2,7:1},3:{0:0,1:2,4:1,5:1,6:0,7:1},
         4:{0:1,2:1,3:2,5:0},5:{0:2,1:1,3:0,4:1,7:2},
         6:{2:0,3:2,7:1},7:{0:0,1:0,2:2,3:1,5:2,6:1}}),
    "r6_shared": (
        {0:(1,3,5),1:(3,6,7),2:(0,6,7),3:(0,4,6),
         4:(0,3,5),5:(3,4,7),6:(0,1,3),7:(0,4,5)},
        {0:{1:2,2:0,3:2,4:1,5:0,6:2,7:1},1:{0:0,3:0,6:1,7:2},
         2:{0:1,6:2,7:0},3:{0:2,1:1,4:0,5:1,6:0},
         4:{0:0,3:1,5:2,7:2},5:{0:1,3:1,4:2,7:0},
         6:{0:1,1:2,2:2,3:0},7:{0:1,1:0,2:1,4:2,5:0}}),
    "r7_shared": (
        {0:(1,3,7),1:(0,3,6),2:(4,5,6),3:(4,5,7),
         4:(2,3,7),5:(1,4,7),6:(2,5,7),7:(3,5,6)},
        {0:{1:2,3:1,7:0},1:{0:2,3:0,5:1,6:2},
         2:{4:1,5:2,6:0},3:{0:0,1:1,4:0,5:2,7:1},
         4:{2:0,3:0,5:2,7:1},5:{1:2,2:1,3:2,4:0,6:1,7:0},
         6:{1:0,2:2,5:1,7:2},7:{0:1,3:1,4:2,5:0,6:2}}),
    "r8_shared": (
        {0:(2,4,7),1:(0,3,4),2:(0,3,7),3:(1,4,5),
         4:(0,1,5),5:(0,3,7),6:(1,2,7),7:(0,2,6)},
        {0:{1:1,2:2,4:2,5:1,7:0},1:{0:2,3:1,4:0,6:0},
         2:{0:0,3:2,6:1,7:1},3:{1:0,2:0,4:1,5:2},
         4:{0:1,1:2,3:0,5:0},5:{0:0,3:2,4:1,7:2},
         6:{1:0,2:1,7:2},7:{0:2,2:1,5:0,6:2}}),
    "r9_shared": (
        {0:(6,3,7),1:(3,0,5),2:(4,7,3),3:(1,2,7),
         4:(2,6,1),5:(7,6,4),6:(0,5,4),7:(5,2,3)},
        {0:{1:2,3:2,6:1,7:0},1:{0:0,3:2,4:1,5:0},
         2:{3:1,4:2,7:0},3:{0:0,1:0,2:2,7:1},
         4:{1:1,2:0,5:0,6:2},5:{1:1,4:1,6:0,7:2},
         6:{0:2,4:0,5:1},7:{0:1,2:1,3:0,5:2}}),
    "r10_shared": (
        {0:(7,1,2),1:(0,2,3),2:(1,3,6),3:(2,4,7),
         4:(3,5,6),5:(4,6,7),6:(5,7,2),7:(6,0,3)},
        None),
    "r11_shared": (
        {0:(7,1,2),1:(0,2,5),2:(1,3,6),3:(2,4,7),
         4:(3,5,6),5:(4,6,1),6:(5,7,2),7:(6,0,3)},
        None),
    "r12_shared": (
        {u:((u - 1) % N, (u + 1) % N, (u + 4) % N) for u in range(N)},
        None),
}


def generated_complete_axes(out):
    """Choose exact coordinate endpoint lines on every physical block.

    Sorted outgoing neighbours receive colours 0,1,2 at their heads.  The
    remaining free endpoint factors are filled so each local aggregate star
    spans all three axes.  This includes every unselected physical block as
    a nonzero rank-one block, which is the counterguard to the false step
    'selected degree three implies literal cubic'.
    """

    axes = {u: {} for u in range(N)}
    for tail in range(N):
        for color, head in enumerate(sorted(out[tail])):
            axes[head][tail] = color
    for u in range(N):
        free = [v for v in range(N) if v != u and v not in axes[u]]
        missing = [a for a in sorted(COLORS) if a not in axes[u].values()]
        require(len(missing) <= len(free),
                "not enough free endpoint factors to span target space")
        for v, a in zip(free, missing):
            axes[u][v] = a
        for v in free[len(missing):]:
            axes[u][v] = 0
    return axes


def complete_counterguard_axes(out, axes):
    """Extend a frozen selected-edge model by nonzero unselected blocks."""

    if axes is None:
        return generated_complete_axes(out)
    result = {u: dict(axes[u]) for u in range(N)}
    for u in range(N):
        multiplicity = {a: tuple(result[u].values()).count(a) for a in COLORS}
        fill_axis = max(sorted(COLORS), key=lambda a: multiplicity[a])
        for v in range(N):
            if v != u and v not in result[u]:
                result[u][v] = fill_axis
    return result


def audit_counterguard(name, out, axes):
    axes = complete_counterguard_axes(out, axes)
    require(set(out) == set(range(N)) and set(axes) == set(range(N)),
            f"{name}: site set changed")
    require(all(len(out[u]) == 3 and len(set(out[u])) == 3 for u in range(N)),
            f"{name}: witness outdegree changed")

    directed = {(u, v) for u, neighbors in out.items() for v in neighbors}
    require(len(directed) == 24, f"{name}: directed witness count changed")
    selected = {edge(u, v) for u, v in directed}
    mutual = {edge(u, v) for u, v in directed if (v, u) in directed}
    expected_r = int(name[1:].split("_")[0])
    require(len(mutual) == expected_r and len(selected) == 24 - expected_r,
            f"{name}: reciprocal projection identity changed")

    selected_incident = {
        u: {v for v in range(N) if v != u and edge(u, v) in selected}
        for u in range(N)
    }
    require(all(set(axes[u]) == set(range(N)) - {u} for u in range(N)),
            f"{name}: complete endpoint-axis domain changed")
    require(all(set(axes[u].values()) == COLORS for u in range(N)),
            f"{name}: target flattening lost rank three")

    # The colour of u->v is the forced coordinate line at its head v.
    for u in range(N):
        outgoing_colors = {axes[v][u] for v in out[u]}
        require(outgoing_colors == COLORS,
                f"{name}: one tail lost a pure-colour witness")

    essential = {}
    for u in range(N):
        multiplicity = {a: tuple(axes[u].values()).count(a) for a in COLORS}
        essential[u] = {v for v, a in axes[u].items() if multiplicity[a] == 1}
        require(len(essential[u]) <= 2,
                f"{name}: complete noncubic star exceeded essential bound")

    selected_degree_three = tuple(
        u for u in range(N) if len(selected_incident[u]) == 3)
    # Every physical block in this local model is declared nonzero rank one,
    # so no site is a literal cubic site even when its selected degree is 3.
    require(all(len(axes[u]) == 7 for u in range(N)),
            f"{name}: unselected nonzero extension disappeared")

    if name.startswith("r4_"):
        # These sharp equality guards have two essential directions and one
        # common nonessential coordinate line at every site.  No edge is
        # essential at both endpoints.  The pinned one-sided pure-cover
        # theorem therefore excludes them once the three pure coefficient
        # rows are imposed; it does not follow from incidence alone.
        require(all(len(essential[u]) == 2 for u in range(N)),
                f"{name}: r4 equality lost two essentials per site")
        require(all(len({axes[u][v] for v in axes[u]
                         if v not in essential[u]}) == 1 for u in range(N)),
                f"{name}: common nonessential axis disappeared")
        require(all(not (v in essential[u] and u in essential[v])
                    for u, v in combinations(range(N), 2)),
                f"{name}: acquired a double-essential edge")

    if name == "r4_matching":
        require(all(sum(u in pair for pair in mutual) == 1 for u in range(N)),
                "r4 matching guard lost its perfect matching")
    else:
        require(any(sum(u in pair for pair in mutual) >= 2 for u in range(N)),
                f"{name}: shared-endpoint branch disappeared")
    return (len(selected), tuple(len(essential[u]) for u in range(N)),
            selected_degree_three)


def main():
    pin_dependencies()
    perfect_matchings = reciprocal_graph_dichotomy()
    ledger = selected_degree_three_ledger()
    census = {name: audit_counterguard(name, *model)
              for name, model in MODELS.items()}
    require(set(census) == {
        "r4_matching", "r4_shared", "r5_shared", "r6_shared",
        "r7_shared", "r8_shared", "r9_shared", "r10_shared",
        "r11_shared", "r12_shared",
    }, "counterguard census changed")
    print("labelled r=4 reciprocal perfect matchings:", perfect_matchings)
    print("(r, single arcs, forced selected-degree-3 sites):", ledger)
    for name, (pairs, essentials, selected_degree_three) in census.items():
        print(name, "selected", pairs, "essential", essentials,
              "selected-degree-3", selected_degree_three)
    print("r>=10: selected degree 3 is not literal cubicity")
    print("r=4..12: local incidence alone has no adjacent-cubic contradiction")
    print("N=8 r>=4 reciprocal classification: PASS")


if __name__ == "__main__":
    main()
