#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- completeness of the colour-triple orbit reduction.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Closes soft spot 5 of the W2 report.  The eight-site exhaustion enumerates the
13 representatives produced by the committed `colored_triple_orbits`.  Here we
enumerate EVERY ordered triple of pairwise edge-disjoint perfect matchings of
K_n and check it is carried into a representative by a vertex permutation plus
a permutation of the three colours.

Cost control: it suffices, for each of the three choices of which matching
plays colour 0, to apply ONE permutation sending it to the canonical matching
and then reuse the committed `canonical_pair` reduction (which already
minimises over the canonical matching's stabiliser and the 1<->2 swap).
"""
import sys
from itertools import permutations
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations")
import search_monomial_no_singleton_sat as S


def relabel(matching, pi):
    return tuple(sorted((min(pi[u], pi[v]), max(pi[u], pi[v]))
                        for u, v in matching))


def sender(matching, size):
    """A permutation carrying `matching` onto the canonical matching."""
    pi = [0] * size
    for slot, (u, v) in enumerate(sorted(matching)):
        pi[u], pi[v] = 2 * slot, 2 * slot + 1
    return tuple(pi)


def main(size=8):
    vertices = tuple(range(size))
    matchings = tuple(S.perfect_matchings(vertices))
    reps = set(S.colored_triple_orbits(size))
    canonical = S.canonical_matching(size)
    stabilizer = tuple(S.stabilizer_of_canonical_matching(size))

    def canonical_pair(second, third):
        forms = []
        for pi in stabilizer:
            a, b = relabel(second, pi), relabel(third, pi)
            forms.extend(((a, b), (b, a)))
        return min(forms)

    print(f"n={size}: {len(matchings)} perfect matchings, "
          f"{len(reps)} representatives", flush=True)
    triples = []
    for a in matchings:
        sa = set(a)
        for b in matchings:
            if sa & set(b):
                continue
            sab = sa | set(b)
            for c in matchings:
                if sab & set(c):
                    continue
                triples.append((a, b, c))
    print(f"ordered pairwise-disjoint triples: {len(triples)}", flush=True)
    uncovered = []
    for triple in triples:
        hit = False
        for lead in range(3):
            rest = [triple[i] for i in range(3) if i != lead]
            pi = sender(triple[lead], size)
            assert relabel(triple[lead], pi) == canonical
            pair = canonical_pair(relabel(rest[0], pi), relabel(rest[1], pi))
            if (canonical,) + pair in reps:
                hit = True
                break
        if not hit:
            uncovered.append(triple)
    print(f"covered: {len(triples) - len(uncovered)}/{len(triples)}   "
          f"uncovered: {len(uncovered)}", flush=True)
    assert not uncovered, uncovered[:2]
    print("ORBIT REDUCTION COMPLETE", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
