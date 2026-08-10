#!/usr/bin/env python3
"""Audit every canonical cap line on the fixed-dark-plane rational packet.

The packet in ``verify_n8_rank11_scalar_dark_plane_one_site_guard.py`` is a
six-site pair chart, hence determines an ordinary eight-site block array by
restoring its two endpoint sites.  This checker re-presents that same array
at every physical pair.  For each nonzero decorated direct entry it computes
the exact N=8 homogeneous cap error on

    K(z) = E_ab + z I,

takes the gcd of all output-word coefficient polynomials, and decides whether
the line contains an active clean point.  It is a bounded overlap diagnostic,
not a source point: the underlying guard already fails labelled joint rows.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product


Q = Fraction
COLORS = range(3)
SITES = range(8)
EXPECTED_DIGEST = "aed6ddc615f0cd5f564b7fd3c58720aca6864c6dbb06e1ec006907669b67c64e"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ptrim(value):
    value = list(value)
    while len(value) > 1 and not value[-1]:
        value.pop()
    return tuple(value)


def padd(left, right):
    out = [Q(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] += value
    return ptrim(out)


def pscale(scalar, value):
    return ptrim(tuple(scalar * entry for entry in value))


def pmul(left, right):
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return ptrim(out)


def pdivmod(numerator, denominator):
    numerator = list(ptrim(numerator))
    denominator = ptrim(denominator)
    require(denominator != (Q(0),), "polynomial division by zero")
    if len(numerator) < len(denominator):
        return (Q(0),), ptrim(numerator)
    quotient = [Q(0)] * (len(numerator) - len(denominator) + 1)
    while len(numerator) >= len(denominator) and any(numerator):
        shift = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[shift] = coefficient
        for index, value in enumerate(denominator):
            numerator[index + shift] -= coefficient * value
        numerator = list(ptrim(numerator))
    return ptrim(quotient), ptrim(numerator)


def pgcd(left, right):
    left, right = ptrim(left), ptrim(right)
    while right != (Q(0),):
        _, remainder = pdivmod(left, right)
        left, right = right, remainder
    if left == (Q(0),):
        return left
    return pscale(Q(1, 1) / left[-1], left)


def remove_root(poly, root):
    factor = (-root, Q(1))
    while len(poly) > 1:
        quotient, remainder = pdivmod(poly, factor)
        if remainder != (Q(0),):
            break
        poly = quotient
    return poly


def peval(poly, value):
    out = Q(0)
    for coefficient in reversed(poly):
        out = out * value + coefficient
    return out


def eadd(*elements):
    out = {}
    for element in elements:
        for word, coefficient in element.items():
            out[word] = padd(out.get(word, (Q(0),)), coefficient)
            if out[word] == (Q(0),):
                del out[word]
    return out


def escale(poly, element):
    return {word: pmul(poly, coefficient)
            for word, coefficient in element.items()
            if pmul(poly, coefficient) != (Q(0),)}


def emul(left, right):
    out = {}
    for u, a in left.items():
        for v, b in right.items():
            if any(x != -1 and y != -1 for x, y in zip(u, v)):
                continue
            word = tuple(x if x != -1 else y for x, y in zip(u, v))
            out[word] = padd(out.get(word, (Q(0),)), pmul(a, b))
            if out[word] == (Q(0),):
                del out[word]
    return out


def eeval(element, value):
    out = {}
    for word, polynomial in element.items():
        coefficient = peval(polynomial, value)
        if coefficient:
            out[word] = (coefficient,)
    return out


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        out.extend(((first, second),) + tail for tail in matchings(rest))
    return out


M8 = matchings(SITES)


def contracted_hafnian(blocks, endpoints, labels, z=Q(1)):
    """Direct 105-matching contraction, independent of the cap formula."""
    residual = tuple(site for site in SITES if site not in endpoints)
    out = {}

    def kval(first, second):
        return ((Q(1) if (first, second) == labels else Q(0))
                + (z if first == second else Q(0)))

    for matching in M8:
        edge_terms = []
        for u, v in matching:
            terms = [(a, b, cell(blocks, u, v, a, b))
                     for a, b in product(COLORS, repeat=2)
                     if cell(blocks, u, v, a, b)]
            if not terms:
                edge_terms = []
                break
            edge_terms.append((u, v, terms))
        if not edge_terms:
            continue
        for choices in product(*(terms for _, _, terms in edge_terms)):
            colours = {}
            coefficient = Q(1)
            for (u, v, _), (a, b, value) in zip(edge_terms, choices):
                colours[u], colours[v] = a, b
                coefficient *= value
            coefficient *= kval(colours[endpoints[0]], colours[endpoints[1]])
            if not coefficient:
                continue
            word = tuple(colours[site] for site in residual)
            out[word] = out.get(word, Q(0)) + coefficient
            if not out[word]:
                del out[word]
    return {word: (coefficient,) for word, coefficient in out.items()}


def atom_word(residual, site, colour):
    word = [-1] * len(residual)
    word[residual.index(site)] = colour
    return tuple(word)


def build_blocks():
    blocks = {}

    def put(u, v, a, b, value):
        if u > v:
            u, v, a, b = v, u, b, a
        blocks[(u, v, a, b)] = blocks.get((u, v, a, b), Q(0)) + Q(value)

    # Internal six-site quadratic q.
    put(0, 1, 0, 0, 1)
    put(1, 2, 0, 1, 1)
    put(3, 4, 0, 0, 1)
    put(1, 5, 0, 0, 1)
    put(1, 5, 1, 0, -1)
    put(1, 5, 2, 0, -1)
    put(2, 5, 0, 0, 1)

    p = (
        {(0, 0): 1, (1, 2): 1, (2, 1): 1,
         (3, 1): 1, (4, 1): 1, (5, 2): 1},
        {(1, 2): 1, (2, 0): 1,
         (3, 1): 1, (4, 1): 1, (5, 2): 1},
        {(3, 1): -1, (4, 1): -1, (5, 2): -1},
    )
    s = (
        {(3, 2): 1, (4, 1): 1, (5, 2): 1},
        {(1, 1): 1, (1, 2): 1, (2, 0): 1,
         (3, 2): -1, (4, 1): -1, (5, 2): -1},
        {(1, 0): 1, (3, 2): -1, (4, 1): -1, (5, 2): -1},
    )
    for colour in COLORS:
        for (site, residual_colour), value in p[colour].items():
            put(6, site, colour, residual_colour, value)
        for (site, residual_colour), value in s[colour].items():
            put(site, 7, residual_colour, colour, value)

    direct = ((1, -1, -1), (0, 0, 0), (0, 0, 0))
    for a in COLORS:
        for b in COLORS:
            if direct[a][b]:
                put(6, 7, a, b, direct[a][b])
    return {cell: value for cell, value in blocks.items() if value}


def cell(blocks, u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return blocks.get((u, v, a, b), Q(0))


def cap_line_error(blocks, endpoints, labels):
    p_site, q_site = endpoints
    a_label, b_label = labels
    residual = tuple(site for site in SITES if site not in endpoints)

    def k(i, j):
        return (Q(1) if (i, j) == labels else Q(0),
                Q(1) if i == j else Q(0))

    direct = (Q(0),)
    for i in COLORS:
        for j in COLORS:
            direct = padd(direct, pscale(
                cell(blocks, p_site, q_site, i, j), k(i, j)))

    q_internal = {}
    response = {}
    for u, v in combinations(residual, 2):
        for c, d in product(COLORS, repeat=2):
            word = [-1] * len(residual)
            word[residual.index(u)] = c
            word[residual.index(v)] = d
            word = tuple(word)
            q_value = cell(blocks, u, v, c, d)
            if q_value:
                q_internal[word] = (q_value,)
            r_value = (Q(0),)
            for i, j in product(COLORS, repeat=2):
                endpoint_product = (
                    cell(blocks, p_site, u, i, c)
                    * cell(blocks, q_site, v, j, d)
                    + cell(blocks, p_site, v, i, d)
                    * cell(blocks, q_site, u, j, c)
                )
                if endpoint_product:
                    r_value = padd(r_value, pscale(endpoint_product, k(i, j)))
            if r_value != (Q(0),):
                response[word] = r_value

    response2 = emul(response, response)
    response3 = emul(response2, response)
    error = eadd(
        escale(pscale(3, direct), emul(response2, q_internal)),
        response3,
    )
    coefficients = list(error.values())
    common = (Q(0),)
    for coefficient in coefficients:
        common = coefficient if common == (Q(0),) else pgcd(common, coefficient)
    return direct, ptrim(common), len(coefficients), q_internal, response


def has_active_root(common, direct, labels, identically_clean):
    if identically_clean:
        # A nonzero direct entry makes s(z) nonzero generically, and the
        # diagonal activity factors also exclude only finitely many z.
        return True
    if len(common) <= 1:
        return False
    forbidden = {Q(0)}
    if labels[0] == labels[1]:
        forbidden.add(Q(-1))
    if len(direct) > 1 and direct[1]:
        forbidden.add(-direct[0] / direct[1])
    reduced = common
    for root in forbidden:
        reduced = remove_root(reduced, root)
    return len(reduced) > 1


def main():
    blocks = build_blocks()
    require(len(blocks) == 37, ("eight-site support changed", len(blocks)))
    records = []
    for endpoints in combinations(SITES, 2):
        for labels in product(COLORS, repeat=2):
            direct_entry = cell(blocks, *endpoints, *labels)
            if not direct_entry:
                continue
            direct, common, row_count, q_internal, response = cap_line_error(
                blocks, endpoints, labels)
            identically_clean = row_count == 0
            records.append({
                "endpoints": endpoints,
                "labels": labels,
                "direct": tuple(str(value) for value in direct),
                "gcd": tuple(str(value) for value in common),
                "rows": row_count,
                "identically_clean": identically_clean,
                "active_clean": has_active_root(
                    common, direct, labels, identically_clean),
                "_q": q_internal,
                "_response": response,
            })

    active = [record for record in records if record["active_clean"]]
    nontrivial_active = [record for record in active
                         if not record["identically_clean"]]
    clean = [record for record in records
             if record["identically_clean"] or len(record["gcd"]) > 1]
    original = [record for record in records if record["endpoints"] == (6, 7)]
    require([(record["endpoints"], record["labels"], record["gcd"])
             for record in active] == [
                 ((0, 1), (0, 0), ("0",)),
                 ((0, 6), (0, 0), ("0",)),
                 ((1, 7), (0, 2), ("-1", "1")),
                 ((2, 5), (0, 0), ("0",)),
                 ((2, 7), (0, 1), ("-1", "1")),
                 ((3, 4), (0, 0), ("0",)),
             ], ("the active-clean lines changed", active))
    require([(record["endpoints"], record["labels"])
             for record in nontrivial_active] == [
                 ((1, 7), (0, 2)), ((2, 7), (0, 1))
             ], "the two nontrivial overlapping lines changed")
    require(all(not record["active_clean"] for record in original),
            "the original scalar chart acquired an active clean line")

    active_layer_counts = []
    for record in nontrivial_active:
        root = Q(1)
        q_at_root = eeval(record.pop("_q"), root)
        response_at_root = eeval(record.pop("_response"), root)
        response2 = emul(response_at_root, response_at_root)
        layer2 = emul(response2, q_at_root)
        layer3 = emul(response2, response_at_root)
        scalar = peval(tuple(Q(value) for value in record["direct"]), root)
        require(eadd(escale((3 * scalar,), layer2), layer3) == {},
                ("active clean cancellation changed", record))
        q3 = emul(emul(q_at_root, q_at_root), q_at_root)
        contracted_formula = eadd(
            escale((Q(scalar, 6),), q3),
            escale((Q(1, 2),), emul(
                response_at_root, emul(q_at_root, q_at_root))),
        )
        contracted_direct = contracted_hafnian(
            blocks, record["endpoints"], record["labels"])
        require(contracted_formula == contracted_direct,
                ("105-matching cap formula changed", record))
        active_layer_counts.append((
            record["endpoints"], len(response_at_root),
            len(layer2), len(layer3), scalar,
            len(contracted_direct),
        ))
    # Remove the bulky private elements from the remaining records too.
    for record in records:
        record.pop("_q", None)
        record.pop("_response", None)
    ledger = {
        "block_count": len(blocks),
        "line_count": len(records),
        "clean_line_count": len(clean),
        "active_clean_line_count": len(active),
        "nontrivial_active_clean_line_count": len(nontrivial_active),
        "nontrivial_active_layer_counts": active_layer_counts,
        "original_chart": original,
        "active_examples": active,
    }
    digest = sha256(repr(ledger).encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, ("ledger digest changed", digest, ledger))
    print("N=8 dark-plane all-pair canonical-line audit: passed")
    print(f"  blocks / canonical lines       : {len(blocks)} / {len(records)}")
    print(f"  clean / active / nontrivial    : "
          f"{len(clean)} / {len(active)} / {len(nontrivial_active)}")
    print(f"  original-chart lines           : {len(original)}")
    print(f"  direct aggregate matchings     : {len(M8)}")
    print(f"  ledger sha256                  : {digest}")


if __name__ == "__main__":
    main()
