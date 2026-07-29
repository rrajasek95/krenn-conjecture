#!/usr/bin/env python3
"""Exact audit of the minimal-valuation rainbow rewrite 2-cycle.

The thirteen rational aggregate cells below have three exactly normalized
constant fibres and one exact binomial mixed fibre.  The selected-triple
rewrite in that mixed fibre exchanges two globally minimum-valuation
locally-rainbow degree-nine monomials.  Thus valuation minimization alone
does not orient the rewrite.
"""

from collections import Counter
from fractions import Fraction
from itertools import product


N = 6
COLORS = range(3)

# A key is (u,v,a,b), with u<v and a (respectively b) the port at u
# (respectively v).  Only the displayed aggregate cells are nonzero.
ENTRIES = {
    # The selected colour-zero matching P0.
    (0, 4, 0, 0): Fraction(1, 2),
    (1, 2, 0, 0): Fraction(1),
    (3, 5, 0, 0): Fraction(1),
    # A second colour-zero matching S0, sharing 04 with P0.
    (1, 3, 0, 0): Fraction(1),
    (2, 5, 0, 0): Fraction(1),
    # The unique colour-one matching P1.
    (0, 5, 1, 1): Fraction(1),
    (1, 4, 1, 1): Fraction(1),
    (2, 3, 1, 1): Fraction(1),
    # The unique colour-two matching P2.
    (0, 3, 2, 2): Fraction(1),
    (1, 5, 2, 2): Fraction(1),
    (2, 4, 2, 2): Fraction(1),
    # The two new cells in the mixed cancellation mate N.
    (1, 2, 2, 1): Fraction(-1),
    (3, 5, 1, 2): Fraction(1),
}

P0 = {
    (0, 4, 0, 0),
    (1, 2, 0, 0),
    (3, 5, 0, 0),
}
S0 = {
    (0, 4, 0, 0),
    (1, 3, 0, 0),
    (2, 5, 0, 0),
}
P1 = {
    (0, 5, 1, 1),
    (1, 4, 1, 1),
    (2, 3, 1, 1),
}
P2 = {
    (0, 3, 2, 2),
    (1, 5, 2, 2),
    (2, 4, 2, 2),
}
R = {
    (0, 4, 0, 0),
    (1, 5, 2, 2),
    (2, 3, 1, 1),
}
MATE = {
    (0, 4, 0, 0),
    (1, 2, 2, 1),
    (3, 5, 1, 2),
}
MIXED_COLORING = (0, 2, 1, 1, 0, 2)


def perfect_matchings(vertices=frozenset(range(N))):
    """Enumerate underlying perfect matchings in lexicographic order."""
    if not vertices:
        yield ()
        return
    u = min(vertices)
    for v in sorted(vertices - {u}):
        for rest in perfect_matchings(vertices - {u, v}):
            yield ((u, v),) + rest


def fibre_terms(coloring):
    """Return all nonzero decorated matching terms in one coefficient."""
    answer = []
    for matching in perfect_matchings():
        decorated = []
        value = Fraction(1)
        for u, v in matching:
            occurrence = (u, v, coloring[u], coloring[v])
            if occurrence not in ENTRIES:
                break
            decorated.append(occurrence)
            value *= ENTRIES[occurrence]
        else:
            answer.append((frozenset(decorated), value))
    return answer


def endpoints(occurrence):
    u, v, a, b = occurrence
    return frozenset({(u, a), (v, b)})


def locally_rainbow_networks():
    """Enumerate matchings of all eighteen vertex/colour stubs."""
    all_stubs = frozenset((v, a) for v in range(N) for a in COLORS)
    by_stub = {stub: [] for stub in all_stubs}
    for occurrence in ENTRIES:
        for stub in endpoints(occurrence):
            by_stub[stub].append(occurrence)

    answer = []

    def visit(remaining, chosen):
        if not remaining:
            answer.append(frozenset(chosen))
            return

        def available(stub):
            return [
                occurrence
                for occurrence in by_stub[stub]
                if endpoints(occurrence) <= remaining
            ]

        stub = min(remaining, key=lambda item: (len(available(item)), item))
        for occurrence in available(stub):
            visit(remaining - endpoints(occurrence), chosen + [occurrence])

    visit(all_stubs, [])
    return answer


def valuation_two(value):
    """The normalized 2-adic valuation of a nonzero Fraction."""
    assert value
    numerator = abs(value.numerator)
    denominator = value.denominator
    answer = 0
    while numerator % 2 == 0:
        numerator //= 2
        answer += 1
    while denominator % 2 == 0:
        denominator //= 2
        answer -= 1
    return answer


def monomial(network):
    answer = Fraction(1)
    for occurrence in network:
        answer *= ENTRIES[occurrence]
    return answer


def main():
    assert len(ENTRIES) == 13

    # The three target coefficients are normalized exactly, not only at the
    # level of valuations or residues.
    expected_constant_terms = {
        0: {(frozenset(P0), Fraction(1, 2)),
            (frozenset(S0), Fraction(1, 2))},
        1: {(frozenset(P1), Fraction(1))},
        2: {(frozenset(P2), Fraction(1))},
    }
    for color in COLORS:
        terms = fibre_terms((color,) * N)
        assert set(terms) == expected_constant_terms[color]
        assert sum((value for _, value in terms), Fraction()) == 1

    # The displayed mixed coefficient is an exact two-term cancellation.
    mixed_terms = fibre_terms(MIXED_COLORING)
    assert set(mixed_terms) == {
        (frozenset(R), Fraction(1, 2)),
        (frozenset(MATE), Fraction(-1, 2)),
    }
    assert sum((value for _, value in mixed_terms), Fraction()) == 0

    # In fact this sparse model satisfies all but four of the 726 mixed
    # equations.  Recording the complete error support makes the scope of
    # the countermodel exact and gives a compact target for stronger global
    # arguments.
    mixed_errors = {}
    for coloring in product(COLORS, repeat=N):
        if len(set(coloring)) == 1:
            continue
        value = sum(
            (term_value for _, term_value in fibre_terms(coloring)),
            Fraction(),
        )
        if value:
            mixed_errors[coloring] = value
    assert mixed_errors == {
        (0, 0, 0, 1, 0, 2): Fraction(1, 2),
        (0, 2, 1, 0, 0, 0): Fraction(-1, 2),
        (1, 0, 2, 0, 2, 1): Fraction(1),
        (2, 1, 0, 2, 1, 0): Fraction(1),
    }

    selected = frozenset(P0 | P1 | P2)
    complement = selected - R
    replacement = frozenset(complement | MATE)
    assert len(selected) == len(replacement) == 9
    assert monomial(selected) == Fraction(1, 2)
    assert monomial(replacement) == Fraction(-1, 2)
    assert monomial(selected) + monomial(replacement) == 0

    # Exhaust all supported perfect matchings of the eighteen stubs.  There
    # are four, and every one has the globally minimal valuation -1.  The
    # lower bound is also transparent: 04_00 is the only supported cell at
    # stub (0,0), hence it is forced, and it is the only nonunit cell.
    networks = locally_rainbow_networks()
    assert len(networks) == 4
    assert selected in networks
    assert replacement in networks
    valuations = Counter(valuation_two(monomial(state)) for state in networks)
    assert valuations == Counter({-1: 4})
    assert [e for e, value in ENTRIES.items() if valuation_two(value) < 0] == [
        (0, 4, 0, 0)
    ]
    assert all((0, 4, 0, 0) in state for state in networks)

    # The reverse move removes MATE and restores R.  Thus the exact binomial
    # relation itself supplies a directed two-cycle on the valuation plateau.
    assert replacement - MATE == complement
    assert frozenset((replacement - MATE) | R) == selected

    print(
        "verified 13-cell valuation countermodel: constants=(1,1,1), "
        "722/726 mixed fibres vanish, selected fibre=(1/2)+(-1/2)=0, "
        "four rainbow states all v2=-1, and the exact rewrite is a 2-cycle"
    )


if __name__ == "__main__":
    main()
