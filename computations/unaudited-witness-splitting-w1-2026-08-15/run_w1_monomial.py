#!/usr/bin/env python3
"""UNAUDITED PROBE (W1, task C) -- exhaustive death of the MONOMIAL regime.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Lemma J.1 claims that blocking everywhere forces the coordinate/monomial
regime; lemma J.2 must then kill exact sources in that regime.  At six
sites the monomial regime is finite combinatorics, so J.2's six-site case
can be settled exhaustively -- which is what this script does.

MONOMIAL REGIME.  Every block is A_uv = w_uv e_{a_uv} (x) e_{b_uv} with
w_uv != 0 (or A_uv = 0).  Write the two HALF-EDGE colours of the edge uv as
c_uv(u) = a_uv (the colour uv puts at u) and c_uv(v) = b_uv.

CLASS LEMMA.  A perfect matching M covers every site exactly once, so the
monomial product over M is nonzero on exactly ONE word,
    omega(M)_u = c_{M(u)}(u),
and therefore
    H_6(A)_w = sum_{M : omega(M) = w} prod_{e in M} w_e,
every other word having coefficient zero.  Consequently the GHZ system in
the monomial regime is the MATCHING-CLASS system:
    * every mixed class must cancel (sum of its weight products = 0);
    * every pure class must sum to 1 (so each colour needs a monochromatic
      matching);
    * a mixed class of SIZE ONE cannot cancel with nonzero weights -- this
      is exactly the singleton/O2 mechanism of J.2.

This script enumerates, exhaustively and up to relabelling of sites and a
global colour permutation, every half-edge colouring of K_6 with all
fifteen blocks nonzero (the dense stratum) and checks whether some mixed
class is a singleton.  The class lemma itself is checked numerically
against the independent coefficient routine.

Usage: python3 run_w1_monomial.py [--jobs 8]
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from itertools import combinations, permutations, product
import json
import random
import time

from w1_core import (PAIRS, SITES, Source, all_coefficients, exactness_metrics,
                     perfect_matchings, require, structure_metrics)

MATCHINGS = perfect_matchings(SITES)
EDGES = tuple(PAIRS)


def matching_edges(matching):
    return tuple(tuple(sorted(edge)) for edge in matching)


MATCHING_EDGES = tuple(matching_edges(m) for m in MATCHINGS)


def disjoint_triples():
    """Ordered triples of pairwise edge-disjoint perfect matchings."""
    out = []
    for i, j, k in product(range(15), repeat=3):
        a, b, c = (set(MATCHING_EDGES[i]), set(MATCHING_EDGES[j]),
                   set(MATCHING_EDGES[k]))
        if a & b or a & c or b & c:
            continue
        out.append((i, j, k))
    return out


def relabel_matching(index, permutation):
    edges = frozenset(tuple(sorted((permutation[u], permutation[v])))
                      for u, v in MATCHING_EDGES[index])
    for other, candidate in enumerate(MATCHING_EDGES):
        if frozenset(candidate) == edges:
            return other
    raise ValueError("permutation did not map a matching to a matching")


def triple_orbits():
    """S_6 (sites) x S_3 (global colour) orbits of the ordered triples."""
    triples = disjoint_triples()
    index = {triple: n for n, triple in enumerate(triples)}
    seen = set()
    representatives = []
    for triple in triples:
        if triple in seen:
            continue
        orbit = set()
        for permutation in permutations(range(6)):
            mapped = tuple(relabel_matching(m, permutation) for m in triple)
            for order in permutations(range(3)):
                orbit.add(tuple(mapped[o] for o in order))
        seen |= orbit
        representatives.append((triple, len(orbit)))
    return triples, representatives


DEAD = None
STATES = (DEAD,) + tuple(product(range(3), repeat=2))     # 1 + 9 = 10


def half_edge_colours(triple, free_assignment, free_edges):
    """colour[(edge, endpoint)] for the whole graph; dead edges are absent."""
    colours = {}
    for colour, index in enumerate(triple):
        for edge in MATCHING_EDGES[index]:
            colours[(edge, edge[0])] = colour
            colours[(edge, edge[1])] = colour
    for edge, state in zip(free_edges, free_assignment):
        if state is DEAD:
            continue
        colours[(edge, edge[0])] = state[0]
        colours[(edge, edge[1])] = state[1]
    return colours


def classes(colours):
    """Partition of the LIVE matchings by their word omega(M)."""
    table = defaultdict(list)
    for index, edges in enumerate(MATCHING_EDGES):
        word = [0] * 6
        alive = True
        for edge in edges:
            if (edge, edge[0]) not in colours:
                alive = False
                break
            word[edge[0]] = colours[(edge, edge[0])]
            word[edge[1]] = colours[(edge, edge[1])]
        if alive:
            table[tuple(word)].append(index)
    return table


def scan_triple(job):
    """Every state of the six free edges: is some MIXED class a singleton?

    The six non-triple edges range over ten states (dead, or one of the nine
    monomial colourings), so this scan is a COMPLETE classification of the
    monomial regime with nonzero pure coefficients, up to relabelling of the
    sites and a global colour permutation: any such source has three pairwise
    disjoint monochromatic matchings (its pure classes), which is the triple,
    and its other six blocks are arbitrary.
    """
    triple, limit = job
    used = set()
    for index in triple:
        used |= set(MATCHING_EDGES[index])
    free_edges = tuple(edge for edge in EDGES if edge not in used)
    require(len(free_edges) == 6, "a disjoint triple uses nine of fifteen edges")
    survivors = []
    singleton_free = 0
    total = 0
    histogram = Counter()
    dead_histogram = Counter()
    for assignment in product(STATES, repeat=6):
        total += 1
        colours = half_edge_colours(triple, assignment, free_edges)
        table = classes(colours)
        singletons = [word for word, members in table.items()
                      if len(members) == 1 and len(set(word)) > 1]
        histogram[len(singletons)] += 1
        if not singletons:
            singleton_free += 1
            dead = sum(1 for state in assignment if state is DEAD)
            dead_histogram[dead] += 1
            if len(survivors) < limit:
                survivors.append({
                    "assignment": [list(state) if state is not DEAD else None
                                   for state in assignment],
                    "free_edges": [list(edge) for edge in free_edges],
                    "dead_edges": dead,
                    "classes": {"".join(map(str, word)): members
                                for word, members in table.items()}})
    return {"triple": list(triple), "total": total,
            "singleton_free": singleton_free,
            "singleton_free_by_dead_count": {str(k): v for k, v
                                             in sorted(dead_histogram.items())},
            "singleton_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "survivors": survivors}


def build_source(triple, assignment, free_edges, weights):
    blocks = {}
    colours = half_edge_colours(triple, assignment, free_edges)
    for edge in EDGES:
        table = [[Fraction(0)] * 3 for _ in range(3)]
        a = colours[(edge, edge[0])]
        b = colours[(edge, edge[1])]
        table[a][b] = Fraction(weights[edge])
        blocks[edge] = table
    return Source(blocks)


def control_class_lemma(trials=200, seed=5):
    """W9: the class lemma against the independent coefficient routine."""
    rng = random.Random(seed)
    triples = disjoint_triples()
    checked = 0
    for _ in range(trials):
        triple = rng.choice(triples)
        used = set()
        for index in triple:
            used |= set(MATCHING_EDGES[index])
        free_edges = tuple(edge for edge in EDGES if edge not in used)
        assignment = tuple((rng.randrange(3), rng.randrange(3))
                           for _ in free_edges)
        weights = {edge: Fraction(rng.choice([-3, -2, -1, 1, 2, 3]))
                   for edge in EDGES}
        source = build_source(triple, assignment, free_edges, weights)
        colours = half_edge_colours(triple, assignment, free_edges)
        table = classes(colours)
        coefficients = all_coefficients(source)
        for word, values in coefficients.items():
            total = Fraction(0)
            for index in table.get(word, []):
                term = Fraction(1)
                for edge in MATCHING_EDGES[index]:
                    term *= weights[edge]
                total += term
            require(values == total,
                    f"W9 class lemma failed at {word}: {values} vs {total}")
            checked += 1
        # a singleton mixed class really has a nonzero coefficient
        for word, members in table.items():
            if len(members) == 1 and len(set(word)) > 1:
                require(coefficients[word] != 0, "W9 singleton must not vanish")
    return {"coefficients_checked": checked}


def control_random_monomial(trials=400, seed=9):
    """W10: the theorem end-to-end on random monomial sources.

    Independent of the orbit reduction and of the class bookkeeping: build a
    random monomial source, keep it if all three pure GHZ coefficients are
    nonzero, and check with the coefficient/fibre routines that some MIXED
    word has exactly one surviving term (hence a nonzero coefficient).
    """
    from w1_core import MIXED_WORDS, support_fibres
    from run_b_strata import STRATA
    from run_c_pure_hunt import anchored_source
    rng = random.Random(seed)
    kept = 0
    singleton_counts = []
    scan_agreements = 0
    triples = disjoint_triples()
    for index in range(trials):
        if index % 2 == 0:
            # P2's own anchored constructor (independent of this file)
            source = anchored_source(rng, rng.choice(list(STRATA)))
            if source is None:
                continue
            combinatorial = None
        else:
            triple = rng.choice(triples)
            used = set()
            for member in triple:
                used |= set(MATCHING_EDGES[member])
            free_edges = tuple(edge for edge in EDGES if edge not in used)
            assignment = tuple(rng.choice(STATES) for _ in free_edges)
            weights = {edge: Fraction(rng.choice([-3, -2, -1, 1, 2, 3]))
                       for edge in EDGES}
            colours = half_edge_colours(triple, assignment, free_edges)
            blocks = {}
            for edge in EDGES:
                table = [[Fraction(0)] * 3 for _ in range(3)]
                if (edge, edge[0]) in colours:
                    table[colours[(edge, edge[0])]][colours[(edge, edge[1])]] = \
                        weights[edge]
                blocks[edge] = table
            source = Source(blocks)
            table = classes(colours)
            combinatorial = {word for word, members in table.items()
                             if len(members) == 1 and len(set(word)) > 1}
        coefficients = all_coefficients(source)
        if any(coefficients[(c,) * 6] == 0 for c in range(3)):
            continue
        kept += 1
        fibres = support_fibres(source)
        singletons = {w for w in MIXED_WORDS if fibres[w] == 1}
        require(singletons,
                "W10 monomial source with nonzero pures and no singleton "
                "mixed class")
        for word in singletons:
            require(coefficients[word] != 0, "W10 singleton must not vanish")
        if combinatorial is not None:
            require(combinatorial == singletons,
                    "W10 the scan's class model disagrees with the fibres")
            scan_agreements += 1
        singleton_counts.append(len(singletons))
    return {"sampled": trials, "with_nonzero_pures": kept,
            "scan_model_agreements": scan_agreements,
            "min_singletons": min(singleton_counts, default=None),
            "max_singletons": max(singleton_counts, default=None)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--survivors", type=int, default=20)
    parser.add_argument("--out", default="results_monomial.json")
    parser.add_argument("--all-triples", action="store_true",
                        help="scan every ordered triple, not one per orbit")
    args = parser.parse_args()

    print("W9 class lemma control:", control_class_lemma(), flush=True)
    print("W10 random monomial   :", control_random_monomial(), flush=True)
    triples, representatives = triple_orbits()
    print(f"ordered disjoint triples: {len(triples)}; "
          f"orbits: {len(representatives)} "
          f"(sizes {[size for _t, size in representatives]})", flush=True)

    jobs = [(triple, args.survivors) for triple in
            (triples if args.all_triples
             else [triple for triple, _size in representatives])]
    start = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for number, result in enumerate(pool.map(scan_triple, jobs), 1):
            results.append(result)
            print(f"  triple {number}/{len(jobs)}: "
                  f"{result['singleton_free']}/{result['total']} singleton-free "
                  f"({time.time()-start:.0f}s)", flush=True)

    summary = {
        "ordered_triples": len(triples),
        "orbits": len(representatives),
        "orbit_sizes": [size for _t, size in representatives],
        "scanned_triples": len(jobs),
        "colourings_per_triple": results[0]["total"] if results else 0,
        "total_colourings": sum(row["total"] for row in results),
        "singleton_free_total": sum(row["singleton_free"] for row in results),
        "singleton_histogram": dict(Counter(
            {int(k): v for row in results
             for k, v in row["singleton_histogram"].items()})),
    }
    merged = Counter()
    for row in results:
        for key, value in row["singleton_histogram"].items():
            merged[int(key)] += value
    summary["singleton_histogram"] = {str(k): merged[k] for k in sorted(merged)}
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "results": results}, handle, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
