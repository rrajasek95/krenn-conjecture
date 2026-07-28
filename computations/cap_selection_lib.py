#!/usr/bin/env python3
"""Exact square-free site-algebra library for the cap-selection frontier.

Independent reconstruction layer for the Priority-1 attack on the
cap/prism/shared-pair-ideal side.  Nothing here imports from the existing
verifiers; every hafnian, pair chart, slice, and cofactor is recomputed
from first principles.

Conventions (identical to the notes):

* An aggregate edge family on an ordered site tuple ``sites`` is a dict
  ``{(u, v): {(cu, cv): coeff}}`` with ``u < v`` in site order and
  endpoint order retained (``cu`` at ``u``, ``cv`` at ``v``).
* The square-free algebra element is a dict
  ``{frozenset({(site, colour), ...}): coeff}``; multiplication is zero
  whenever supports share a site.
* ``H_S(A)`` is the hafnian over the induced edges of ``S``: the sum over
  perfect matchings of the product of block tensors.  No support,
  symmetry, or genericity assumption is used anywhere.

Coefficients may be any sympy expression or Fraction-compatible number.
"""

from __future__ import annotations

from itertools import product as iproduct

import sympy as sp

# ---------------------------------------------------------------------------
# square-free algebra
# ---------------------------------------------------------------------------


def alg_zero():
    return {}


def alg_add(a, b):
    out = dict(a)
    for key, coeff in b.items():
        val = out.get(key, 0) + coeff
        val = sp.expand(val) if isinstance(val, sp.Basic) else val
        if val == 0:
            out.pop(key, None)
        else:
            out[key] = val
    return out


def alg_scale(a, scalar):
    if scalar == 0:
        return {}
    out = {}
    for key, coeff in a.items():
        val = coeff * scalar
        val = sp.expand(val) if isinstance(val, sp.Basic) else val
        if val != 0:
            out[key] = val
    return out


def alg_mul(a, b):
    out = {}
    for ka, va in a.items():
        sites_a = {site for site, _ in ka}
        for kb, vb in b.items():
            if any(site in sites_a for site, _ in kb):
                continue
            key = ka | kb
            val = out.get(key, 0) + va * vb
            val = sp.expand(val) if isinstance(val, sp.Basic) else val
            if val == 0:
                out.pop(key, None)
            else:
                out[key] = val
    return out


def alg_equal(a, b):
    keys = set(a) | set(b)
    for key in keys:
        diff = a.get(key, 0) - b.get(key, 0)
        diff = sp.expand(diff) if isinstance(diff, sp.Basic) else diff
        if diff != 0:
            return False
    return True


# ---------------------------------------------------------------------------
# families and hafnians
# ---------------------------------------------------------------------------


def block_element(family, u, v, order):
    """The aggregate block on {u, v} as an algebra element (endpoint order)."""
    if order.index(u) > order.index(v):
        u, v = v, u
    out = {}
    for (cu, cv), coeff in family.get((u, v), {}).items():
        if coeff == 0:
            continue
        out[frozenset({(u, cu), (v, cv)})] = coeff
    return out


def perfect_matchings(sites):
    sites = tuple(sites)
    if not sites:
        yield ()
        return
    first, rest = sites[0], sites[1:]
    for idx, partner in enumerate(rest):
        remaining = rest[:idx] + rest[idx + 1 :]
        for sub in perfect_matchings(remaining):
            yield ((first, partner),) + sub


def hafnian(family, sites, order):
    """H_S(A) in the square-free algebra (sum over perfect matchings)."""
    total = {}
    for matching in perfect_matchings(sites):
        term = {frozenset(): 1}
        for u, v in matching:
            term = alg_mul(term, block_element(family, u, v, order))
            if not term:
                break
        if term:
            total = alg_add(total, term)
    return total


def contract_pure_boundary(family, w_sites, u_sites, colour, order):
    """G_colour = iota_{U, colour^{|U|}} H_B(A) as a tensor on w_sites.

    Enumerates all perfect matchings of B = W (disjoint) U and keeps only
    the coefficient terms whose U-part is the pure word colour^{|U|}.
    Returned as an algebra element supported on w_sites only.
    """
    b_sites = tuple(w_sites) + tuple(u_sites)
    u_set = set(u_sites)
    total = {}
    for matching in perfect_matchings(b_sites):
        term = {frozenset(): 1}
        dead = False
        for u, v in matching:
            block = block_element(family, u, v, order)
            # restrict U-endpoints to the pure colour
            restricted = {}
            for key, coeff in block.items():
                if any(site in u_set and col != colour for site, col in key):
                    continue
                stripped = frozenset(
                    (site, col) for site, col in key if site not in u_set
                )
                val = restricted.get(stripped, 0) + coeff
                if val == 0:
                    restricted.pop(stripped, None)
                else:
                    restricted[stripped] = val
            # NB: stripping is safe because every site occurs exactly once
            # in a matching, so no square-free collision can occur on the
            # stripped support within one matching product.
            term = alg_mul(term, restricted)
            if not term:
                dead = True
                break
        if not dead:
            total = alg_add(total, term)
    return total


def pure_word(w_sites, colour):
    return {frozenset((site, colour) for site in w_sites): 1}


# ---------------------------------------------------------------------------
# pair chart (delete two sites p, q; boundary = rest)
# ---------------------------------------------------------------------------


def pair_chart(family, p, q, boundary, order):
    """Return (a, ell, m, x): direct block, two star rows, internal quadratic.

    ell[i] is the boundary linear form (algebra element) obtained from the
    p-star with colour i at p; m[j] likewise at q.  Endpoint order of every
    block is retained literally.
    """
    a = [[family.get(tuple(sorted((p, q), key=order.index)), {}).get(
        (i, j) if order.index(p) < order.index(q) else (j, i), 0
    ) for j in range(3)] for i in range(3)]
    ell = [alg_zero() for _ in range(3)]
    mrow = [alg_zero() for _ in range(3)]
    for u in boundary:
        pu = block_element(family, p, u, order)
        qu = block_element(family, q, u, order)
        for key, coeff in pu.items():
            kd = dict(key)
            i = kd[p]
            ell[i] = alg_add(ell[i], {frozenset({(u, kd[u])}): coeff})
        for key, coeff in qu.items():
            kd = dict(key)
            j = kd[q]
            mrow[j] = alg_add(mrow[j], {frozenset({(u, kd[u])}): coeff})
    x = alg_zero()
    bset = list(boundary)
    for idx, u in enumerate(bset):
        for v in bset[idx + 1 :]:
            x = alg_add(x, block_element(family, u, v, order))
    return a, ell, mrow, x


def divided_power(x, k):
    """x^[k] = x^k / k! (unordered k-edge matching power)."""
    result = {frozenset(): 1}
    for _ in range(k):
        result = alg_mul(result, x)
    return alg_scale(result, sp.Rational(1, sp.factorial(k)))


def pair_slice(family, p, q, i, j, boundary, order):
    """D_ij = (e_i^* at p) (e_j^* at q) contracted into H_B(A), directly."""
    b_sites = (p, q) + tuple(boundary)
    total = {}
    for matching in perfect_matchings(b_sites):
        term = {frozenset(): 1}
        for u, v in matching:
            block = block_element(family, u, v, order)
            restricted = {}
            for key, coeff in block.items():
                kd = dict(key)
                if p in kd and kd[p] != i:
                    continue
                if q in kd and kd[q] != j:
                    continue
                stripped = frozenset(
                    (site, col) for site, col in key if site not in (p, q)
                )
                val = restricted.get(stripped, 0) + coeff
                if val == 0:
                    restricted.pop(stripped, None)
                else:
                    restricted[stripped] = val
            term = alg_mul(term, restricted)
            if not term:
                break
        if term:
            total = alg_add(total, term)
    return total


# ---------------------------------------------------------------------------
# caps and cofactors
# ---------------------------------------------------------------------------


def cap_contract(tensor, cap, w_sites):
    """Contract an algebra element (supported on w_sites ∪ rest) by a cap.

    ``cap`` maps colour words on w_sites (tuples) to coefficients.  Terms
    must cover every w-site (true for top tensors); remaining support is
    returned.
    """
    out = {}
    for key, coeff in tensor.items():
        kd = dict(key)
        if any(site not in kd for site in w_sites):
            continue
        word = tuple(kd[site] for site in w_sites)
        weight = cap.get(word, 0)
        if weight == 0:
            continue
        stripped = frozenset(
            (site, col) for site, col in key if site not in w_sites
        )
        val = out.get(stripped, 0) + coeff * weight
        val = sp.expand(val) if isinstance(val, sp.Basic) else val
        if val == 0:
            out.pop(stripped, None)
        else:
            out[stripped] = val
    return out


def cofactor_family(family, w_sites, boundary, cap, order):
    """A^K_{uv} = K ⌟ H_{W ∪ {u,v}}(A) for all boundary pairs u < v."""
    out = {}
    blist = list(boundary)
    for idx, u in enumerate(blist):
        for v in blist[idx + 1 :]:
            hw = hafnian(family, tuple(w_sites) + (u, v), order)
            contracted = cap_contract(hw, cap, w_sites)
            cell = {}
            for key, coeff in contracted.items():
                kd = dict(key)
                if set(kd) != {u, v}:
                    continue
                cell[(kd[u], kd[v])] = cell.get((kd[u], kd[v]), 0) + coeff
            out[(u, v)] = {k: c for k, c in cell.items() if c != 0}
    return out


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def words(length):
    return list(iproduct(range(3), repeat=length))


def tensor_coefficients(element, sites):
    """Dense coefficient vector of an algebra element on the given sites."""
    out = {}
    for key, coeff in element.items():
        kd = dict(key)
        if set(kd) != set(sites):
            continue
        out[tuple(kd[s] for s in sites)] = coeff
    return out
