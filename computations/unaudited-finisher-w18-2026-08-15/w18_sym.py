#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- orbit propagation of kills inside a class.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

The template problem is equivariant for the group S_8 x S_3 (relabel sites /
permute colours): T carries an exact source iff g.T does, for every g.  Inside
one support-graph class the subgroup that preserves the class representative
is Aut(G) x S_3, so a verified kill of T is simultaneously a verified kill of
every g.T with g in Aut(G) x S_3, and a REASON SET maps to a reason set.

`run_equivariance_control` checks the claim numerically rather than assuming
it: it applies random group elements to templates and re-verifies (SC),
fibre sizes, and the kill certificate.
"""

from __future__ import annotations

from itertools import permutations

import w18_core as C
import w18_graphs as G


def class_group(mask):
    """Aut(G) x S_3 as a list of (site permutation, colour permutation)."""
    autos = G.automorphisms(mask)
    return [(tuple(pi), tuple(sig))
            for pi in autos for sig in permutations(range(3))]


def map_cell(e, i, j, pi, sig):
    u, v = C.EDGES[e]
    a, b = pi[u], pi[v]
    ii, jj = sig[i], sig[j]
    if a > b:
        a, b = b, a
        ii, jj = jj, ii
    return C.EIDX[(a, b)], ii, jj


def map_literal(lit, pi, sig):
    kind, e, i, j = lit[0], lit[1], lit[2], lit[3]
    e2, i2, j2 = map_cell(e, i, j, pi, sig)
    return (kind, e2, i2, j2)


def reason_orbit(reason, group, cap=48):
    """Distinct images of a reason set under the group."""
    out = []
    seen = set()
    for (pi, sig) in group:
        img = tuple(sorted(map_literal(l, pi, sig) for l in reason))
        if img in seen:
            continue
        seen.add(img)
        out.append([list(x) for x in img])
        if len(out) >= cap:
            break
    return out


def template_orbit(T, group, cap=48):
    out = []
    seen = set()
    for (pi, sig) in group:
        img = C.apply_perm(T, pi, sig)
        if img in seen:
            continue
        seen.add(img)
        out.append(img)
        if len(out) >= cap:
            break
    return out


def compose(g1, g2):
    """(g1 . g2) acting as g1(g2(.)) on templates."""
    pi1, sig1 = g1
    pi2, sig2 = g2
    return (tuple(pi1[pi2[p]] for p in range(C.N)),
            tuple(sig1[sig2[c]] for c in range(C.Q)))


IDENT = (tuple(range(C.N)), tuple(range(C.Q)))


def _closure(gens, cap):
    H = {IDENT}
    frontier = [IDENT]
    while frontier:
        a = frontier.pop()
        for b in gens:
            c = compose(a, b)
            if c not in H:
                H.add(c)
                frontier.append(c)
                if len(H) > cap:
                    return None
    return H


def class_subgroup(mask, cap=48):
    """A SUBGROUP of Aut(G) x S_3 of order <= cap (contains the colour S_3).

    A subgroup -- not just a capped list -- is what makes lex-leader symmetry
    breaking sound alongside orbit-closed nogoods: the nogood set is closed
    under H, so the lex-min element of an H-orbit of a surviving assignment
    survives too.
    """
    gens = [(tuple(range(C.N)), sig) for sig in permutations(range(C.Q))]
    H = _closure(gens, cap)
    if H is None:
        return [IDENT]
    for pi in G.automorphisms(mask):
        pi = tuple(pi)
        if pi == tuple(range(C.N)):
            continue
        trial = _closure(list(H) + [(pi, tuple(range(C.Q)))], cap)
        if trial is not None:
            H = trial
    return sorted(H)
