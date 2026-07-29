#!/usr/bin/env python3
"""Verify a six-site countermodel to bare binomial odd dependence.

The support has 48 distinct aggregate endpoint-colour cells; several cells
may share an underlying pair, but no aggregate coordinate is duplicated.
Exactly 108 coloring fibres are nonempty, and every one consists of two
perfect matchings.  A displayed +/-1 signing cancels all 105 mixed fibres
and gives one selected matching in each constant fibre product +1.

The other term in each constant fibre has product -1, so the three constant
*coefficients* vanish.  Thus this is not a Krenn counterexample.  It is an
exact counterexample to an incidence theorem whose hypothesis only asks for
three normalized constant matching monomials: the signing itself proves
that the mixed exponent differences have no odd integer dependency.
"""

from collections import Counter
from itertools import product

from verify_valuation_rainbow_descent_cycle import (
    COLORS,
    N,
    P0,
    P1,
    P2,
    perfect_matchings,
)


def build_support():
    support = {
        (0, 3, 2, 2),
        (0, 4, 0, 0),
        (0, 5, 1, 1),
    }
    support |= {
        (1, 2, a, b) for a, b in product(COLORS, repeat=2)
    }
    support |= {
        (1, 3, a, b) for a in (0, 2) for b in (0, 1)
    }
    support |= {
        (1, 4, 1, b) for b in (1, 2)
    }
    support |= {
        (1, 5, a, b) for a in COLORS for b in (0, 2)
    }
    support |= {
        (2, 3, a, b) for a in COLORS for b in (0, 1)
    }
    support |= {
        (2, 4, a, b) for a in COLORS for b in (1, 2)
    }
    support |= {
        (3, 4, a, b) for a in (0, 1) for b in (1, 2)
    }
    support |= {
        (3, 5, a, b) for a in (0, 1) for b in (0, 2)
    }
    support |= {
        (4, 5, a, b) for a in (1, 2) for b in (0, 2)
    }
    assert len(support) == 48
    return frozenset(support)


SUPPORT = build_support()

NEGATIVE = frozenset({
    (1, 5, 0, 0),
    (1, 5, 1, 0),
    (1, 5, 2, 0),
    (3, 4, 0, 1),
    (3, 4, 0, 2),
    (3, 4, 1, 1),
    (3, 4, 1, 2),
    (3, 5, 0, 2),
    (3, 5, 1, 2),
    (4, 5, 1, 2),
    (4, 5, 2, 2),
})
assert NEGATIVE <= SUPPORT


def weight(occurrence):
    assert occurrence in SUPPORT
    return -1 if occurrence in NEGATIVE else 1


def fibre_terms(coloring):
    answer = []
    for matching in perfect_matchings():
        decorated = frozenset(
            (u, v, coloring[u], coloring[v]) for u, v in matching
        )
        if not decorated <= SUPPORT:
            continue
        value = 1
        for occurrence in decorated:
            value *= weight(occurrence)
        answer.append((decorated, value))
    return answer


def main():
    fibres = {
        coloring: fibre_terms(coloring)
        for coloring in product(COLORS, repeat=N)
    }
    distribution = Counter(len(terms) for terms in fibres.values())
    assert distribution == Counter({0: 621, 2: 108})

    constant_terms = tuple(fibres[(color,) * N] for color in COLORS)
    assert all(len(terms) == 2 for terms in constant_terms)
    assert tuple(
        sum(value for _, value in terms) for terms in constant_terms
    ) == (0, 0, 0)

    selected = (frozenset(P0), frozenset(P1), frozenset(P2))
    for color in COLORS:
        term_values = dict(constant_terms[color])
        assert selected[color] in term_values
        assert term_values[selected[color]] == 1
        assert sorted(term_values.values()) == [-1, 1]

    mixed = [
        (coloring, terms)
        for coloring, terms in fibres.items()
        if len(set(coloring)) > 1 and terms
    ]
    assert len(mixed) == 105
    assert all(len(terms) == 2 for _, terms in mixed)
    assert all(sum(value for _, value in terms) == 0 for _, terms in mixed)
    assert all(sorted(value for _, value in terms) == [-1, 1]
               for _, terms in mixed)

    # This is the complete matching tensor: empty fibers contribute zero,
    # every mixed binomial cancels, and all three constant binomials cancel.
    assert all(sum(value for _, value in terms) == 0
               for terms in fibres.values())

    # The no-odd-dependency conclusion is mathematical and needs no Smith
    # computation.  For each mixed pair (M_c,N_c), this signing satisfies
    # w^(chi_M-chi_N)=-1.  Evaluating a putative relation
    # sum z_c(chi_M-chi_N)=0 would give 1=(-1)^(sum z_c), so sum z_c is even.
    for _coloring, ((left, left_value), (right, right_value)) in mixed:
        assert left_value == -right_value

    pair_multiplicities = Counter((u, v) for u, v, _a, _b in SUPPORT)
    assert max(pair_multiplicities.values()) == 9
    assert pair_multiplicities[1, 2] == 9
    assert len(pair_multiplicities) == 12

    print(
        "verified parallel-cell binomial countermodel: 48 cells, "
        "621 empty + 108 binomial fibers, all 105 mixed binomials cancel"
    )
    print(
        "selected constant matching products=(1,1,1), but each constant "
        "fiber is 1+(-1)=0; the complete matching tensor is zero"
    )
    print(
        "consequence: the mixed exponent rows admit the displayed sign "
        "character and therefore have no odd integer dependency"
    )


if __name__ == "__main__":
    main()
