#!/usr/bin/env python3
"""Audit the exact diagonal alternating-cycle switch and its first lock web.

The all-order statement is the divided-power identity

    (q+d)^[h] - q^[h] = d q^[h-1]

when every cell of d meets one fixed site, hence d^[2]=0.  After inserting
two endpoint stars the four response differences are similarly

    p_i s_j ((q+d)^[h-1] - q^[h-1])
        = p_i s_j d q^[h-2].

The finite audit checks these five identities for h=3,...,8 and freezes a
nine-cell, colour-diagonal common-hafnian web.  Two terms in one word cancel
on a C4.  Deleting their two incident cells preserves that word but exposes
a second C4 word.  Thus a literal same-word switch has an exact joint lock;
cycle provenance alone does not manufacture a transverse endpoint head.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json


EXPECTED_LEDGER_SHA256 = (
    "4c41b02b4b6d2c0b93f26d697dfab91071d8d0be21f64d560d50daac332f30fd"
)


Cell = tuple[int, int, int, int]
Word = tuple[int, ...]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(counter):
    return Counter({key: value for key, value in counter.items() if value})


def cell(left, right, left_colour, right_colour):
    require(left < right, "cells must use increasing endpoint order")
    return (left, right, left_colour, right_colour)


def merge_assignment(ambient, assignments, coefficient):
    word = [None] * len(ambient)
    position = {site: index for index, site in enumerate(ambient)}
    for site, colour in assignments.items():
        require(site in position, "assignment left the ambient site set")
        require(word[position[site]] is None, "a physical site was repeated")
        word[position[site]] = colour
    require(all(colour is not None for colour in word), "word is incomplete")
    return tuple(word), coefficient


def matchings(q, sites):
    """Return the decorated perfect-matching tensor on ``sites``."""

    sites = tuple(sorted(sites))
    by_left = {}
    for edge, coefficient in q.items():
        if coefficient and edge[0] in sites and edge[1] in sites:
            by_left.setdefault(edge[0], []).append((edge, coefficient))

    output = Counter()

    def visit(remaining, assignments, coefficient):
        if not remaining:
            word, value = merge_assignment(sites, assignments, coefficient)
            output[word] += value
            return
        left = min(remaining)
        for edge, weight in by_left.get(left, ()):
            _, right, left_colour, right_colour = edge
            if right not in remaining:
                continue
            visit(
                remaining - {left, right},
                assignments | {left: left_colour, right: right_colour},
                coefficient * weight,
            )

    visit(set(sites), {}, Q(1))
    return clean(output)


def inserted_edge_tensor(q, inserted, sites):
    """Compute ``inserted * q^[k]`` on all sites."""

    sites = tuple(sorted(sites))
    output = Counter()
    for edge, coefficient in inserted.items():
        left, right, left_colour, right_colour = edge
        if left not in sites or right not in sites:
            continue
        remainder = tuple(site for site in sites if site not in (left, right))
        for word, value in matchings(q, remainder).items():
            assignments = {left: left_colour, right: right_colour}
            assignments.update(dict(zip(remainder, word, strict=True)))
            merged, total = merge_assignment(
                sites, assignments, coefficient * value
            )
            output[merged] += total
    return clean(output)


def response(q, p, s, sites):
    """Compute ``p*s*q^[h-1]`` with literal site provenance."""

    sites = tuple(sorted(sites))
    output = Counter()
    for p_site, p_colour, p_weight in p:
        for s_site, s_colour, s_weight in s:
            if p_site == s_site:
                continue
            remainder = tuple(
                site for site in sites if site not in (p_site, s_site)
            )
            for word, value in matchings(q, remainder).items():
                assignments = {p_site: p_colour, s_site: s_colour}
                assignments.update(dict(zip(remainder, word, strict=True)))
                merged, total = merge_assignment(
                    sites, assignments, p_weight * s_weight * value
                )
                output[merged] += total
    return clean(output)


def response_with_inserted_edge(q, p, s, inserted, sites):
    """Compute ``p*s*inserted*q^[h-2]``."""

    sites = tuple(sorted(sites))
    output = Counter()
    for p_site, p_colour, p_weight in p:
        for s_site, s_colour, s_weight in s:
            if p_site == s_site:
                continue
            occupied = {p_site, s_site}
            for edge, edge_weight in inserted.items():
                left, right, left_colour, right_colour = edge
                if occupied & {left, right}:
                    continue
                remainder = tuple(
                    site for site in sites
                    if site not in occupied | {left, right}
                )
                for word, value in matchings(q, remainder).items():
                    assignments = {
                        p_site: p_colour,
                        s_site: s_colour,
                        left: left_colour,
                        right: right_colour,
                    }
                    assignments.update(dict(zip(remainder, word, strict=True)))
                    merged, total = merge_assignment(
                        sites,
                        assignments,
                        p_weight * s_weight * edge_weight * value,
                    )
                    output[merged] += total
    return clean(output)


def subtract(left, right):
    keys = set(left) | set(right)
    return clean(Counter({key: left.get(key, 0) - right.get(key, 0)
                          for key in keys}))


def base_web():
    # Exactly four perfect matchings, in two cancelling word fibres.
    return {
        cell(0, 1, 1, 1): Q(1),
        cell(2, 3, 1, 1): Q(1),
        cell(4, 5, 0, 0): Q(1),
        cell(0, 2, 1, 1): Q(1),
        cell(1, 3, 1, 1): Q(-1),
        cell(2, 4, 1, 1): Q(1),
        cell(3, 5, 0, 0): Q(1),
        cell(0, 4, 1, 1): Q(-1),
        cell(1, 2, 1, 1): Q(1),
    }


def extended_web(h):
    require(h >= 3, "the base web has three matching edges")
    q = base_web()
    for index in range(h - 3):
        left = 6 + 2 * index
        q[cell(left, left + 1, 2, 2)] = Q(1)
    return q


def mutual_anchors(q):
    incidence = Counter()
    for left, right, left_colour, right_colour in q:
        incidence[(left, left_colour)] += 1
        incidence[(right, right_colour)] += 1
    return {
        edge for edge in q
        if incidence[(edge[0], edge[2])] == 1
        and incidence[(edge[1], edge[3])] == 1
    }


def audit_order(h):
    sites = tuple(range(2 * h))
    q = extended_web(h)
    removed = {
        cell(0, 1, 1, 1): -q[cell(0, 1, 1, 1)],
        cell(0, 2, 1, 1): -q[cell(0, 2, 1, 1)],
    }
    q_new = dict(q)
    for edge, change in removed.items():
        q_new[edge] += change
        if not q_new[edge]:
            del q_new[edge]

    # Every inserted cell meets site 0, so the divided square is literally
    # zero.  The exact finite difference therefore stops at first order.
    require(all(edge[0] == 0 for edge in removed),
            "the switch stopped being supported on one physical star")
    top = matchings(q, sites)
    top_new = matchings(q_new, sites)
    top_difference = subtract(top_new, top)
    predicted_top = inserted_edge_tensor(q, removed, sites)
    require(top_difference == predicted_top,
            f"top finite difference failed at h={h}")

    suffix = (2,) * (2 * (h - 3))
    first_word = (1, 1, 1, 1, 0, 0) + suffix
    lock_word = (1, 1, 1, 0, 1, 0) + suffix
    require(top[first_word] == 0 and top[lock_word] == 0,
            "the original two binomial rows stopped cancelling")
    require(top_new.get(first_word, 0) == 0,
            "the selected C4 binomial was not preserved")
    require(top_new[lock_word] == -1,
            "the second C4 stopped being the literal lock")

    # Four arbitrary multisite endpoint products audit all response slots.
    p1 = ((0, 1, Q(2)), (4, 0, Q(-1)))
    p2 = ((1, 2, Q(3)), (3, 1, Q(1)))
    s1 = ((2, 0, Q(1)), (5, 2, Q(-2)))
    s2 = ((0, 2, Q(1)), (4, 1, Q(3)))
    response_checks = 0
    for p, s in ((p1, s1), (p1, s2), (p2, s1), (p2, s2)):
        actual = subtract(response(q_new, p, s, sites), response(q, p, s, sites))
        predicted = response_with_inserted_edge(q, p, s, removed, sites)
        require(actual == predicted,
                f"response finite difference failed at h={h}")
        response_checks += 1

    old_anchors = mutual_anchors(q)
    new_anchors = mutual_anchors(q_new)
    deleted = set(removed)
    require(not (old_anchors & deleted),
            "a deleted same-coordinate cell became a mutual anchor")
    require(old_anchors <= new_anchors,
            "the deletion destroyed an old mutual anchor")
    require(len(q_new) == len(q) - 2, "the support drop changed")

    return {
        "h": h,
        "sites": len(sites),
        "support_before": len(q),
        "support_after": len(q_new),
        "selected_binomial_after_switch": str(top_new.get(first_word, 0)),
        "lock_coefficient_after_switch": str(top_new[lock_word]),
        "top_difference_terms": len(top_difference),
        "response_finite_difference_checks": response_checks,
        "old_mutual_anchors": len(old_anchors),
        "old_anchors_preserved": old_anchors <= new_anchors,
        "all_internal_cells_colour_diagonal": all(
            edge[2] == edge[3] for edge in q
        ),
    }


def main():
    audits = [audit_order(h) for h in range(3, 9)]
    ledger = {
        "theorem": (
            "for a same-site quadratic switch d with d^[2]=0, the exact "
            "five one-bad tensor differences are d*q^[h-1] and "
            "p_i*s_j*d*q^[h-2] for ij=11,12,21,22"
        ),
        "orders_audited": audits,
        "base_lock_web": {
            "cells": len(base_web()),
            "first_cycle": "01|23|45 versus 02|13|45",
            "second_cycle": "01|24|35 versus 04|12|35",
            "deleted_same_coordinate_cells": ["01:11", "02:11"],
            "selected_word": "111100",
            "lock_word": "111010",
            "all_cells_diagonal": True,
        },
        "verdict": (
            "the chosen binomial admits an exact support-lowering switch "
            "iff its full five-row lock vanishes; a second diagonal C4 can "
            "supply a nonzero lock without any transverse cycle head"
        ),
        "scope": (
            "the lock web is a genuine common-hafnian top-zero packet, not "
            "a full one-bad source: it omits q^[h]=X0 and the four required "
            "response targets.  It blocks a cycle-only overlap inference, "
            "not a theorem using all five exact one-bad rows"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(payload)
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
