#!/usr/bin/env python3
"""UNAUDITED PROBE (W7 / Route T.1) -- per-cone kill engine, version 2.

Pinned HEAD: a41949965d41e5c63fb4bc1caf7b20c0df017856

Version 1 (kill_engine.py) only used facts that come from a product all of
whose factors but one are UNITS.  Version 2 adds

  * BRANCH ELIMINATION.  The initial form of a word of content n factors as
    F_1(A_1) ... F_r(A_r) over the components of the colour-block graph, where
    (A_1,...,A_r) runs over all ordered partitions of the N sites into blocks of
    the prescribed sizes.  The equation says: for EVERY such partition some
    factor vanishes.  If a lemma forbids F_1 from vanishing on every
    configuration inside a ground set of size g, then some A_1 has
    F_1(A_1) != 0, and the same disjunctive statement must hold for the
    remaining factors inside the ground set of size g - |A_1|.  Recursively,

        IMPOSSIBLE([], g)   = True                 (empty product = 1 != 0)
        IMPOSSIBLE(L, g)    = OR_i [ SINGLE(L_i, g) AND
                                     IMPOSSIBLE(L minus i, g - size(L_i)) ]

    with SINGLE(C, g) = "the lemma catalogue forbids F_C from vanishing on all
    configurations of shape C inside a ground set of size g":

        isolated colour, block size 2   : True  (a single cell, a torus unit)
        isolated colour, block size 4   : True iff g >= 6      (LEMMA H4)
        isolated colour, block size >=6 : False (no lemma -- residue)
        two-colour full cross k+k, k=1  : True  (a single cell)
        two-colour full cross k+k, k=2  : True iff g >= 5      (LEMMA P2)
        everything else                 : False

    A content KILLS the cone if IMPOSSIBLE(all components, N).  A content
    FORCES component i to vanish identically if
    IMPOSSIBLE(all components except i, N - size_i); when component i is an
    isolated colour c of block size k this is the FACT
        haf(W_c[S]) = 0 for every k-subset S,
    recorded as a "forced level" k for colour c.

  * THE PURE-WORD LAYER.  On the colour-form family the pure word c has the
    single type m_cc = N/2, so all (N-1)!! matchings tie at (N/2) f(c,c) and

        f(c,c) > 0  =>  in_w(Phi_c - 1) = -1, a UNIT  -> the initial ideal is
                        everything (KILL, every cone);
        f(c,c) = 0  =>  in_w(Phi_c - 1) = h_c(V) - 1  (anchor 1);
        f(c,c) < 0  =>  in_w(Phi_c - 1) = h_c(V)      (anchor 0).

    LEMMA A (anchor collapse).  If the mixed part forces level k <= N-2 for
    colour c then, expanding the hafnian at any pivot, h_c(S) = 0 propagates
    upward two vertices at a time, so h_c(V) = 0 -- contradicting the anchor 1.
    Hence a cone with a forced level for colour c is killed unless f(c,c) < 0.

  The verdict for a point of the 6-dimensional colour-form family is therefore
  indexed by (g-face, sign pattern of (f(0,0),f(1,1),f(2,2))).
"""

from __future__ import annotations

from itertools import combinations
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from colour_form_fan import build  # noqa: E402
from kill_engine import components, is_unit_component  # noqa: E402

PAIRS = ((0, 1), (0, 2), (1, 2))
PAIR_INDEX = {p: i for i, p in enumerate(PAIRS)}


def comp_shape(n, m, comp):
    """('iso', colour, size) | ('cross', a, b, k) | ('other', ...)"""
    cols = sorted(comp)
    if len(cols) == 1:
        return ("iso", cols[0], n[cols[0]])
    if len(cols) == 2:
        a, b = cols
        k = m[PAIR_INDEX[(a, b)]]
        if n[a] == k and n[b] == k:
            return ("cross", a, b, k)
        return ("other2", a, b, n[a], n[b], k)
    return ("other3", tuple(cols), tuple(n[c] for c in cols), tuple(m))


def comp_size(n, comp):
    return sum(n[c] for c in comp)


def single_impossible(shape, ground):
    """SINGLE(C, g): does the lemma catalogue forbid F_C from vanishing on every
    configuration of shape C inside a ground set of size g?"""
    if shape[0] == "iso":
        size = shape[2]
        if size == 0:
            return True          # empty product is 1
        if size == 2:
            return True          # a single cell
        if size == 4:
            return ground >= 6   # LEMMA H4
        return False
    if shape[0] == "cross":
        k = shape[3]
        if k == 1:
            return True          # a single cell
        if k == 2:
            return ground >= 5   # LEMMA P2
        return False
    return False


def impossible(shapes, sizes, ground, memo=None):
    """IMPOSSIBLE(L, g) as in the docstring."""
    if memo is None:
        memo = {}
    key = (tuple(shapes), ground)
    if key in memo:
        return memo[key]
    if not shapes:
        memo[key] = True
        return True
    result = False
    for i in range(len(shapes)):
        if single_impossible(shapes[i], ground):
            rest_shapes = shapes[:i] + shapes[i + 1:]
            rest_sizes = sizes[:i] + sizes[i + 1:]
            if impossible(rest_shapes, rest_sizes, ground - sizes[i], memo):
                result = True
                break
    memo[key] = result
    return result


def content_analysis(n, argmin, nsites):
    """Return (kill, facts) for one mixed content in one cone.

    kill  : bool -- the content alone is torus-infeasible.
    facts : list of ('level', colour, k) forced vanishing statements.
    """
    if len(argmin) != 1:
        # the initial form is a sum over several types; only the shared unit
        # components can be divided out, and no product rule applies.  We keep
        # the (sound) singleton test: a unique minimising matching.
        return False, []
    m = argmin[0]
    comps = components(n, m)
    shapes = [comp_shape(n, m, c) for c in comps]
    sizes = [comp_size(n, c) for c in comps]
    kill = impossible(shapes, sizes, nsites)
    facts = []
    if not kill:
        for i, sh in enumerate(shapes):
            rest_shapes = shapes[:i] + shapes[i + 1:]
            rest_sizes = sizes[:i] + sizes[i + 1:]
            if impossible(rest_shapes, rest_sizes, nsites - sizes[i]):
                if sh[0] == "iso":
                    facts.append(("level", sh[1], sh[2]))
                else:
                    facts.append(("block", sh))
    return kill, facts


def run(nsites):
    data = build(nsites, verbose=False)
    mixed = data["mixed"]
    rows = []
    for rec in data["faces"]:
        kills = []
        levels = {}            # colour -> minimum forced vanishing level
        blocks = []
        singleton = None
        for n in mixed:
            if rec["mincount"][n] == 1:
                singleton = n
            kill, facts = content_analysis(n, rec["argmin"][n], nsites)
            if kill:
                kills.append(n)
            for fact in facts:
                if fact[0] == "level":
                    c, k = fact[1], fact[2]
                    if c not in levels or k < levels[c]:
                        levels[c] = k
                else:
                    blocks.append((n, fact[1]))
        rows.append({"dim": rec["dim"], "point": rec["point"],
                     "singleton": singleton, "kills": kills,
                     "levels": levels, "blocks": blocks,
                     "argmin": rec["argmin"], "mincount": rec["mincount"]})
    return data, rows


SIGNS = ("+", "0", "-")


def verdict(row, sigma, nsites):
    """Verdict for one (g-face, diagonal sign pattern).  Returns the name of the
    first applicable certificate, or None."""
    if any(s == "+" for s in sigma):
        return "pure-unit"
    if row["singleton"] is not None:
        return "singleton"
    if row["kills"]:
        return "mixed-product"
    for c, k in row["levels"].items():
        if k <= nsites - 2 and sigma[c] == "0":
            return "anchor-collapse"
    return None


def main():
    summary = {}
    for nsites in (6, 8):
        data, rows = run(nsites)
        patterns = [(a, b, c) for a in SIGNS for b in SIGNS for c in SIGNS]
        total = len(rows) * len(patterns)
        closed = 0
        open_pairs = []
        by_cert = {}
        for row in rows:
            for sigma in patterns:
                v = verdict(row, sigma, nsites)
                if v:
                    closed += 1
                    by_cert[v] = by_cert.get(v, 0) + 1
                else:
                    open_pairs.append((row, sigma))
        print("N = %d" % nsites)
        print("  g-fan faces %d x 27 diagonal sign patterns = %d cells of the"
              " 6-dimensional colour-form fan" % (len(rows), total))
        print("  CLOSED %d / %d   by certificate: %s" % (closed, total, by_cert))
        print("  OPEN   %d" % len(open_pairs))
        # which g-faces are closed for EVERY sign pattern
        allsig = [row for row in rows
                  if all(verdict(row, s, nsites) for s in patterns)]
        print("  g-faces closed for every diagonal sign pattern : %d / %d"
              % (len(allsig), len(rows)))
        opensig = {}
        for row, sigma in open_pairs:
            opensig[sigma] = opensig.get(sigma, 0) + 1
        print("  open cells by sign pattern: %s"
              % {"".join(k): v for k, v in sorted(opensig.items())})
        # residual structure of the open g-faces
        openrows = {}
        for row, sigma in open_pairs:
            key = (row["dim"], tuple(str(c) for c in row["point"]))
            openrows.setdefault(key, []).append("".join(sigma))
        print("  open g-faces %d (by dim %s)"
              % (len(openrows),
                 {d: sum(1 for k in openrows if k[0] == d) for d in (0, 1, 2, 3)}))
        summary[nsites] = {
            "faces": len(rows), "cells": total, "closed": closed,
            "by_cert": by_cert, "open": len(open_pairs),
            "faces_closed_all_signs": len(allsig),
            "open_by_sign": {"".join(k): v for k, v in sorted(opensig.items())},
            "open_faces": [{"dim": k[0], "point": list(k[1]), "signs": v}
                           for k, v in sorted(openrows.items())],
        }
        print()
    with open("results_kill2.json", "w") as handle:
        json.dump(summary, handle, indent=1, default=str)
    print("wrote results_kill2.json")


if __name__ == "__main__":
    main()
