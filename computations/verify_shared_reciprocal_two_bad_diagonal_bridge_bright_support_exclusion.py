#!/usr/bin/env python3
"""Exclude two bright images from every minimal diagonal target bridge.

Work on five sites, with bridge sites 0,1 and residual sites 2,3,4.
For each non-target colour d, retain only the Boolean support of

    s_d=q_01(d,d),
    u_d,i=q_0i(d,d), v_d,i=q_1i(d,d),
    r_d,i=q_jk(d,d), {i,j,k}={2,3,4}.

The target-line factorization forces every off-target coefficient of K_0
and K_1 to vanish.  A support with exactly one monomial in such a row is
therefore impossible.  Mixed 2+2 rows additionally give the coordinatewise
zero products u_d,i r_e,i and v_d,i r_e,i for d!=e.

Project sites 0,1 modulo the target line and retain only output words with
no target colour.  The target-coloured cells cannot contribute to these
rows.  For each possible support of a bright preimage on sites 2,3,4, a
mixed row containing exactly one supported matching monomial cannot vanish
over an integral domain.  The checker deliberately allows every row with
zero or at least two monomials to cancel, so this is a relaxation of the
coefficient equations.

No one of the 12,540 bridge-compatible support pairs with a non-target
residual edge supports both bright systems.  A minimal bridge has such an
edge because its common factor Z is nonzero and cannot be pure target when
the missing pure tensor is outside im(Phi).
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json


SITES = tuple(range(5))
BRIDGE = (0, 1)
RESIDUAL = (2, 3, 4)
A, C = range(2)
BRIGHT = (A, C)
EXPECTED_DIGEST = "7565ab27a39b8feae40411a369c54dbf119410ba9daa24a1024e77c66d35b81c"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def support_configurations():
    """All one-colour supports not killed by an all-d bridge singleton."""

    answer = []
    # (s, u_0,u_1,u_2, v_0,v_1,v_2, r_0,r_1,r_2)
    for bits in product((0, 1), repeat=10):
        s = bits[0]
        u = bits[1:4]
        v = bits[4:7]
        r = bits[7:10]
        # The all-d coefficient in K_1 is sum_i u_i r_i; in K_0 it
        # is sum_i v_i r_i.  Exactly one nonzero monomial cannot sum to 0.
        if sum(u[index] and r[index] for index in range(3)) == 1:
            continue
        if sum(v[index] and r[index] for index in range(3)) == 1:
            continue
        answer.append((s, u, v, r))
    require(len(answer) == 370,
            "the local bridge-support census changed")
    return tuple(answer)


def bridge_pair_compatible(first, second, require_residual=True):
    configs = {A: first, C: second}
    for colour, other in ((A, C), (C, A)):
        _s, u, v, _r = configs[colour]
        other_r = configs[other][3]
        for index in range(3):
            # These are unique 2+2 matching coefficients in K_1,K_0.
            if u[index] and other_r[index]:
                return False
            if v[index] and other_r[index]:
                return False
    if require_residual and not any(first[3] + second[3]):
        return False
    return True


def support_cells(configs):
    cells = set()
    for colour, (s, u, v, r) in configs.items():
        if s:
            cells.add((BRIDGE, colour))
        for index, site in enumerate(RESIDUAL):
            if u[index]:
                cells.add(((0, site), colour))
            if v[index]:
                cells.add(((1, site), colour))
            if r[index]:
                edge = tuple(sorted(
                    residual for residual in RESIDUAL
                    if residual != site
                ))
                cells.add((edge, colour))
    return frozenset(cells)


def matchings4(vertices):
    a, b, c, d = vertices
    return (((a, b), (c, d)),
            ((a, c), (b, d)),
            ((a, d), (b, c)))


def projected_cofactor_terms(cells, hole, inserted_colour):
    """List literal matching terms in all non-target output words."""

    vertices = tuple(site for site in SITES if site != hole)
    terms = []
    for matching in matchings4(vertices):
        choices = []
        for edge in matching:
            edge = tuple(sorted(edge))
            entries = tuple(colour for candidate, colour in cells
                            if candidate == edge)
            if not entries:
                break
            choices.append(entries)
        else:
            for colours in product(*choices):
                word = {hole: inserted_colour}
                for edge, colour in zip(matching, colours):
                    word[edge[0]] = colour
                    word[edge[1]] = colour
                terms.append(tuple(word[site] for site in SITES))
    return tuple(terms)


def semantic_weight_masks(cells, bright_colour):
    """Return preimage supports not killed by a one-monomial mixed row.

    Masks use bits 1,2,4 for residual sites 2,3,4.  Rows with at least two
    terms are accepted without testing coefficient compatibility, making
    this oracle strictly weaker than the actual bright equations.
    """

    columns = tuple(
        projected_cofactor_terms(cells, hole, bright_colour)
        for hole in RESIDUAL
    )
    pure_word = (bright_colour,) * len(SITES)
    feasible = []
    for mask in range(1, 1 << len(RESIDUAL)):
        counts = Counter()
        for index, column in enumerate(columns):
            if mask & (1 << index):
                counts.update(column)
        if counts[pure_word] == 0:
            continue
        if any(word != pure_word and count == 1
               for word, count in counts.items()):
            continue
        feasible.append(mask)
    return tuple(feasible)


def audit_mutation(configurations):
    """Freeze a two-bright packet when the mixed bridge factor is absent."""

    first = (0, (0, 0, 1), (0, 1, 0), (0, 0, 0))
    second = (0, (0, 1, 0), (1, 0, 0), (0, 0, 0))
    require(first in configurations and second in configurations,
            "the zero-residual mutation configs left the census")
    require(bridge_pair_compatible(first, second,
                                   require_residual=False),
            "the zero-residual mutation lost bridge compatibility")
    cells = support_cells({A: first, C: second})
    masks = {
        A: semantic_weight_masks(cells, A),
        C: semantic_weight_masks(cells, C),
    }
    require(masks == {A: (1,), C: (4,)},
            "the zero-residual two-bright mutation changed")
    return {
        "cells": [[list(edge), colour]
                  for edge, colour in sorted(cells)],
        "bright_masks": masks,
        "scope": "K_0=K_1=0; not a minimal bridge",
    }


def audit():
    configurations = support_configurations()
    categories = Counter()
    compatible = 0
    for first in configurations:
        for second in configurations:
            if not bridge_pair_compatible(first, second):
                continue
            compatible += 1
            cells = support_cells({A: first, C: second})
            first_masks = semantic_weight_masks(cells, A)
            second_masks = semantic_weight_masks(cells, C)
            category = (
                "both" if first_masks and second_masks
                else "a_only" if first_masks
                else "c_only" if second_masks
                else "neither"
            )
            categories[category] += 1

    require(compatible == 12_540,
            "the compatible bridge-pair census changed")
    require(categories == Counter({
        "neither": 10_018,
        "a_only": 1_261,
        "c_only": 1_261,
    }), "the coupled semantic verdict changed")
    require(categories["both"] == 0,
            "a support survived both bright systems")

    mutation = audit_mutation(configurations)
    ledger = {
        "local_supports_per_colour": len(configurations),
        "raw_support_pairs": len(configurations) ** 2,
        "bridge_compatible_pairs_with_residual": compatible,
        "semantic_bright_categories": dict(sorted(categories.items())),
        "zero_residual_mutation": mutation,
        "verdict": (
            "no colour-diagonal minimal target-line bridge can have both "
            "non-target pure tensors in the common-cofactor image"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"diagonal bridge support ledger changed: {digest}")
    return digest


def main():
    digest = audit()
    print("diagonal target-bridge bright support exclusion: PASS")
    print("local supports / compatible pairs: 370 / 12540")
    print("semantic categories: neither=10018, a-only=1261, c-only=1261")
    print("supports admitting both bright systems: 0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
