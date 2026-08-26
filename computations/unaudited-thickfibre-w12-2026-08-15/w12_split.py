#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- the SPLIT (cut-factorisation) kill.

    THEOREM W12-1 (split kill).  Let T be a template on the site set B,
    |B| = N even, and let B = L u R be a bipartition with |L| and |R| both
    EVEN.  Call a crossing edge pq (p in L, q in R) ACTIVE on a word w if the
    cell (w_p, w_q) is occupied in T_pq.  For a word w write F_w for its
    fibre sum, and F^L_u (resp. F^R_v) for the sum over perfect matchings of
    L (resp. R) supported on the sub-word u (resp. v).

    (a) If the active crossing edges on w contain no two vertex-disjoint
        edges, then every T-supported perfect matching of B is the union of
        a perfect matching of L and one of R, hence

                        F_w  =  F^L_{w|L} . F^R_{w|R}.

        [Proof: a supported matching using k crossing edges leaves |L| - k
        vertices of L to be matched inside L, so k is even; k >= 2 would
        exhibit two vertex-disjoint active crossing edges.]

    (b) Consequently, if there are colours c != c' such that all three of
        the words c^B, c'^B and w = c^L c'^R have that property, then T
        admits NO exact source: exactness gives
        F^L_c . F^R_c = F_{c^B} != 0  (so F^L_c != 0),
        F^L_{c'} . F^R_{c'} = F_{c'^B} != 0  (so F^R_{c'} != 0),
        while w is MIXED, so 0 = F_w = F^L_c . F^R_{c'} != 0.  Contradiction.

The certificate is purely combinatorial (it only reads the occupied-cell
pattern), it is EXACT, and it is not a lattice/binomial mechanism: it is the
statement that a fibre polynomial FACTORS and both factors are pinned nonzero
by constant words.  This is why it survives W8's immunity proposition.
"""

from __future__ import annotations

from itertools import combinations

import w12_core as C


def crossing_free_fibre(geo, template, word, L):
    """(fibre, uses_crossing) -- fibre indices and whether any uses a cut edge."""
    inL = [v in L for v in range(geo.size)]
    fib = C.fibre(geo, template, word)
    crossing = False
    for n in fib:
        for e in geo.medges[n]:
            u, v = geo.edges[e]
            if inL[u] != inL[v]:
                crossing = True
                break
        if crossing:
            break
    return fib, crossing


def active_crossing(geo, template, word, L):
    """Crossing edges whose cell is occupied on `word`."""
    inL = [v in L for v in range(geo.size)]
    out = []
    for e, mask in enumerate(template):
        if not mask:
            continue
        u, v = geo.edges[e]
        if inL[u] == inL[v]:
            continue
        if (mask >> (3 * word[u] + word[v])) & 1:
            out.append((u, v))
    return out


def star_like(edges):
    """True iff no two of the edges are vertex-disjoint."""
    for (a, b), (c, d) in combinations(edges, 2):
        if len({a, b, c, d}) == 4:
            return False
    return True


def even_bipartitions(size):
    """Unordered bipartitions {L,R} of range(size) with both parts even, >0."""
    seen = set()
    out = []
    for k in range(2, size - 1, 2):
        for L in combinations(range(size), k):
            Ls = frozenset(L)
            Rs = frozenset(range(size)) - Ls
            key = frozenset((Ls, Rs))
            if key in seen:
                continue
            seen.add(key)
            out.append((Ls, Rs))
    return out


def split_certificate(geo, template, verbose=False):
    """Search for a THEOREM W12-1(b) certificate.  Returns dict or None."""
    for (L, R) in even_bipartitions(geo.size):
        # cache: which constant words are crossing-free (and nonempty)?
        good_const = {}
        for c in range(C.Q):
            w = (c,) * geo.size
            fib, crossing = crossing_free_fibre(geo, template, w, L)
            good_const[c] = (bool(fib) and not crossing)
        for c in range(C.Q):
            if not good_const[c]:
                continue
            for cp in range(C.Q):
                if cp == c or not good_const[cp]:
                    continue
                w = tuple(c if v in L else cp for v in range(geo.size))
                fib, crossing = crossing_free_fibre(geo, template, w, L)
                if crossing:
                    continue
                # sanity: the mixed word's fibre must be nonempty here
                assert fib, "crossing-free split forces a nonempty fibre"
                return {
                    "L": sorted(L), "R": sorted(R), "c": c, "cprime": cp,
                    "mixed_word": list(w),
                    "fibre_const_c": len(C.fibre(geo, template, (c,) * geo.size)),
                    "fibre_const_cprime": len(C.fibre(geo, template,
                                                      (cp,) * geo.size)),
                    "fibre_mixed": len(fib),
                    "active_crossing_on_mixed":
                        [list(e) for e in active_crossing(geo, template, w, L)],
                }
    return None


def verify_split_certificate(geo, template, cert):
    """Re-derive the certificate from scratch; every clause must hold.

    Returns a dict of independently recomputed boolean clauses."""
    L = frozenset(cert["L"])
    R = frozenset(range(geo.size)) - L
    c, cp = cert["c"], cert["cprime"]
    checks = {}
    checks["L_even"] = (len(L) % 2 == 0 and len(L) > 0)
    checks["R_even"] = (len(R) % 2 == 0 and len(R) > 0)
    checks["partition"] = (sorted(L | R) == list(range(geo.size))
                           and not (L & R))
    checks["colours_differ"] = (c != cp)
    words = {"const_c": (c,) * geo.size, "const_cp": (cp,) * geo.size,
             "mixed": tuple(cert["mixed_word"])}
    checks["mixed_is_mixed"] = geo.is_mixed(words["mixed"])
    checks["mixed_word_shape"] = (words["mixed"]
                                  == tuple(c if v in L else cp
                                           for v in range(geo.size)))
    for tag, w in words.items():
        fib, crossing = crossing_free_fibre(geo, template, w, L)
        checks[f"{tag}_nonempty"] = bool(fib)
        checks[f"{tag}_crossing_free"] = (not crossing)
        # independent re-derivation of (a)'s hypothesis
        checks[f"{tag}_active_star"] = star_like(
            active_crossing(geo, template, w, L))
    # the factorisation itself, checked monomial-by-monomial
    checks["factorisation_holds"] = _factorisation_holds(geo, template, words,
                                                         L, R)
    return checks


def _left_right_matchings(geo, template, word, part):
    """Perfect matchings of `part` supported on `word` (as edge-index sets)."""
    part = sorted(part)
    out = []
    for pm in C.perfect_matchings(tuple(part)):
        eidx = []
        ok = True
        for (u, v) in pm:
            e = geo.eindex[(u, v)]
            if not ((template[e] >> (3 * word[u] + word[v])) & 1):
                ok = False
                break
            eidx.append(e)
        if ok:
            out.append(frozenset(eidx))
    return out


def _factorisation_holds(geo, template, words, L, R):
    """F_w's matching set == {left PM} x {right PM} for each of the 3 words."""
    for tag, w in words.items():
        lhs = {frozenset(geo.medges[n]) for n in C.fibre(geo, template, w)}
        left = _left_right_matchings(geo, template, w, L)
        right = _left_right_matchings(geo, template, w, R)
        rhs = {a | b for a in left for b in right}
        if lhs != rhs:
            return False
    return True
