#!/usr/bin/env python3
"""Exact audit that the fixed nine-cell q has no pair-cap preimage.

For the q in the unrestricted polarized eight-site countermodel, this
checker reconstructs q^[3] and q^[4], isolates seven forced Gram entries of
R=ps, and verifies their characteristic-zero ideal is the unit ideal.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import shutil
import subprocess


SITES = tuple(range(8))
COLOURS = tuple(range(3))
Q_CELLS = (
    (2, 3, 0),
    (4, 5, 0),
    (6, 7, 0),
    (0, 1, 1),
    (3, 6, 1),
    (5, 7, 1),
    (0, 2, 2),
    (1, 4, 2),
    (5, 6, 2),
)


def disjoint(cells):
    endpoints = [site for i, j, _ in cells for site in (i, j)]
    return len(endpoints) == len(set(endpoints))


def q_three_terms():
    """The unordered terms of q^3/3!, with their two missing sites."""
    answer = []
    for cells in combinations(Q_CELLS, 3):
        if not disjoint(cells):
            continue
        used = {site for i, j, _ in cells for site in (i, j)}
        missing = tuple(sorted(set(SITES) - used))
        colours = {site: colour for i, j, colour in cells for site in (i, j)}
        answer.append((missing, colours, cells))
    return tuple(answer)


def ps_word_map(three_terms):
    """Map a top word to the R_(u,c),(v,d) entries contributing to it."""
    result = defaultdict(list)
    for (u, v), fixed, _ in three_terms:
        for colour_u, colour_v in product(COLOURS, repeat=2):
            word = tuple(
                colour_u if site == u else
                colour_v if site == v else
                fixed[site]
                for site in SITES
            )
            result[word].append(((u, colour_u), (v, colour_v)))
    return dict(result)


def q_four_tensor():
    """Compute q^4/4! by unordered disjoint four-cell selections."""
    result = Counter()
    for cells in combinations(Q_CELLS, 4):
        if not disjoint(cells):
            continue
        word = [None] * 8
        for i, j, colour in cells:
            word[i] = word[j] = colour
        assert all(value is not None for value in word)
        result[tuple(word)] += 1
    return result


def singular_unit_audit():
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for the exact unit-ideal audit")

    # Each mode X has coordinates (p_X,s_X), and
    # beta(X,Y)=p_X*s_Y+s_X*p_Y.  The seven equations below are precisely
    # the three pure coefficients and four uniquely supported mixed zeros.
    program = r"""
ring r=0,(pA,sA,pB,sB,pC,sC,pD,sD,pE,sE,pF,sF),dp;
poly AB=pA*sB+sA*pB;
poly CD=pC*sD+sC*pD;
poly EF=pE*sF+sE*pF;
poly AF=pA*sF+sA*pF;
poly BF=pB*sF+sB*pF;
poly AC=pA*sC+sA*pC;
poly CF=pC*sF+sC*pF;
ideal I=4*AB-1,4*CD-1,4*EF-1,AF,BF,AC,CF;
ideal G=std(I);
print("BASIS_SIZE");
print(size(G));
print("BASIS_FIRST");
print(G[1]);
"""
    result = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=120,
    )
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    size_index = lines.index("BASIS_SIZE")
    first_index = lines.index("BASIS_FIRST")
    assert lines[size_index + 1] == "1", result.stdout
    assert lines[first_index + 1] == "1", result.stdout


def main():
    three_terms = q_three_terms()
    assert len(three_terms) == 19
    word_map = ps_word_map(three_terms)
    assert len(word_map) == 165
    assert Counter(map(len, word_map.values())) == {1: 163, 4: 2}

    ordinary = q_four_tensor()
    assert ordinary == Counter({
        (1, 1, 0, 0, 0, 0, 0, 0): 1,
        (2, 2, 2, 1, 2, 1, 1, 1): 1,
    })

    # A=(0,0), B=(1,0), C=(2,1), D=(4,1), E=(3,2), F=(7,2).
    # In (a*q+4*p*s)q^[3]=Delta, division by four gives
    # a*q^[4]+ps*q^[3]=Delta/4.  None of the following seven words occurs
    # in q^[4], and every one has the asserted unique ps contributor.
    selected = {
        (0,) * 8: (((0, 0), (1, 0)),),
        (1,) * 8: (((2, 1), (4, 1)),),
        (2,) * 8: (((3, 2), (7, 2)),),
        (0, 2, 0, 0, 2, 2, 2, 2): (((0, 0), (7, 2)),),
        (2, 0, 2, 1, 0, 0, 1, 2): (((1, 0), (7, 2)),),
        (0, 2, 1, 1, 2, 1, 1, 1): (((0, 0), (2, 1)),),
        (1, 1, 1, 1, 0, 0, 1, 2): (((2, 1), (7, 2)),),
    }
    for word, contributors in selected.items():
        assert tuple(word_map[word]) == contributors
        assert ordinary[word] == 0

    singular_unit_audit()

    print("fixed-q eight-site pair-cap obstruction: PASS")
    print("19 q^[3] terms give 165 words (163 singleton, two fourfold): PASS")
    print("three pure and four mixed singleton Gram equations reconstructed: PASS")
    print("a*q^[4] is absent from all seven selected words: PASS")
    print("seven-equation characteristic-zero ideal is [1]: PASS")


if __name__ == "__main__":
    main()
