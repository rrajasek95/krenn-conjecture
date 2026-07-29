#!/usr/bin/env python3
"""Exact C audit of the fixed-interior two-star Segre obstruction.

The combinatorial part is reconstructed in Python.  The polynomial part is
sent to Singular over Q: each of the three diagonal fibres is decomposed
into its minimal associated components, and every triple of components is
checked against all six off-diagonal shared-star equations.  A unit standard
basis over Q remains a unit basis after extension to C.
"""

from __future__ import annotations

import collections
import itertools
import shutil
import subprocess
from fractions import Fraction
from functools import lru_cache


Q = Fraction
SIX = tuple(range(6))
COLOURS = tuple(range(3))

# The fixed six-site interior.  Endpoint order is literal.
INTERNAL_SOURCES = (
    (0, 1, 0, 0, 1),
    (4, 5, 0, 0, 1),
    (0, 2, 1, 1, 1),
    (1, 4, 1, 1, 1),
    (0, 4, 2, 2, 1),
    (1, 3, 2, 2, 1),
    (2, 5, 0, 0, 1),
    (3, 5, 1, 0, 1),
    (2, 3, 2, 1, 1),
)

U0 = (0, 0, 2, 1, 0, 0)
UPLUS = (
    (1, 2, 1, 2, 0, 0),
    (1, 1, 1, 1, 1, 0),
    (2, 2, 0, 2, 2, 0),
)
HS_SUPPORT = (U0,) + UPLUS

Word = tuple[int, ...]
Endpoint = tuple[int, int]


def aggregate():
    blocks = {}
    for u, v, colour_u, colour_v, weight in INTERNAL_SOURCES:
        block = blocks.setdefault((u, v), {})
        cell = (colour_u, colour_v)
        block[cell] = block.get(cell, Q(0)) + Q(weight)
    return blocks


@lru_cache(maxsize=None)
def matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def add(container, key, value):
    total = container.get(key, Q(0)) + value
    if total:
        container[key] = total
    else:
        container.pop(key, None)


def matching_tensor(vertices: tuple[int, ...], blocks):
    positions = {site: index for index, site in enumerate(vertices)}
    answer = {}
    for matching in matchings(vertices):
        choices = [tuple(blocks.get(edge, {}).items()) for edge in matching]
        if any(not choice for choice in choices):
            continue
        for selected in itertools.product(*choices):
            word = [-1] * len(vertices)
            coefficient = Q(1)
            for (u, v), ((colour_u, colour_v), weight) in zip(
                matching, selected
            ):
                word[positions[u]] = colour_u
                word[positions[v]] = colour_v
                coefficient *= weight
            add(answer, tuple(word), coefficient)
    return answer


def reconstruct_word_terms():
    """Return the symmetric endpoint pairs contributing to every six-word."""
    blocks = aggregate()
    assert matching_tensor(SIX, blocks) == {word: Q(1) for word in HS_SUPPORT}
    word_terms = collections.defaultdict(list)
    atom_count = 0
    for i in SIX:
        for j in range(i + 1, 6):
            rest = tuple(site for site in SIX if site not in (i, j))
            cofactor = matching_tensor(rest, blocks)
            assert all(value == 1 for value in cofactor.values())
            for rest_word in cofactor:
                for ci, cj in itertools.product(COLOURS, repeat=2):
                    assignment = dict(zip(rest, rest_word))
                    assignment[i] = ci
                    assignment[j] = cj
                    word = tuple(assignment[site] for site in SIX)
                    word_terms[word].append(((i, ci), (j, cj)))
                    atom_count += 1
    assert atom_count == 162
    assert len(word_terms) == 126
    assert collections.Counter(map(len, word_terms.values())) == {
        1: 96,
        2: 25,
        3: 4,
        4: 1,
    }
    assert all((colour,) * 6 in word_terms for colour in COLOURS)
    assert all(word in word_terms for word in HS_SUPPORT)
    return word_terms


TYPES = tuple((site, colour) for site in SIX for colour in COLOURS)


def variable(kind: str, boundary_colour: int, endpoint: Endpoint) -> str:
    site, internal_colour = endpoint
    return f"{kind}{boundary_colour}{site}{internal_colour}"


def bilinear_expression(word_terms, a: int, b: int, word: Word) -> str:
    terms = []
    for left, right in word_terms[word]:
        terms.append(variable("p", a, left) + "*" + variable("q", b, right))
        terms.append(variable("p", a, right) + "*" + variable("q", b, left))
    return "+".join(terms)


def fibre_equations(word_terms, normal: str, a: int, b: int, target):
    """Equations for beta(p^a,q^b)=delta_ab e_a^6 modulo N."""
    exceptional = set(HS_SUPPORT)
    answer = []
    for word in word_terms:
        if word in exceptional:
            continue
        polynomial = bilinear_expression(word_terms, a, b, word)
        if target is not None and word == (target,) * 6:
            polynomial += "-1"
        answer.append(polynomial)

    if normal == "line":
        # N=<H_S>: all four exceptional coefficients are equal.
        base = bilinear_expression(word_terms, a, b, U0)
        for word in UPLUS:
            answer.append(
                bilinear_expression(word_terms, a, b, word) + "-(" + base + ")"
            )
    elif normal == "plane":
        # N=<u_0,u_+>: u_0 is free and the three u_+ coefficients are equal.
        base = bilinear_expression(word_terms, a, b, UPLUS[0])
        for word in UPLUS[1:]:
            answer.append(
                bilinear_expression(word_terms, a, b, word) + "-(" + base + ")"
            )
    else:
        raise ValueError(normal)
    return answer


EXPECTED = {
    "line": ((9, 11, 9), 891, 1125),
    "plane": ((15, 13, 14), 2730, 1116),
}


def singular_program(word_terms, normal: str) -> str:
    names = [
        variable(kind, boundary, endpoint)
        for kind in ("p", "q")
        for boundary in COLOURS
        for endpoint in TYPES
    ]
    diagonal = [
        fibre_equations(word_terms, normal, colour, colour, colour)
        for colour in COLOURS
    ]
    off_diagonal = []
    for a, b in itertools.product(COLOURS, repeat=2):
        if a != b:
            off_diagonal.extend(fibre_equations(word_terms, normal, a, b, None))
    expected_equations = EXPECTED[normal][2]
    assert sum(map(len, diagonal)) + len(off_diagonal) == expected_equations

    code = "ring r=0,(" + ",".join(names) + "),dp;\n"
    code += 'LIB "primdec.lib";\n'
    for colour in COLOURS:
        code += f"ideal I{colour}=" + ",".join(diagonal[colour]) + ";\n"
        code += f"list L{colour}=minAssGTZ(I{colour});\n"
    code += "ideal X=" + ",".join(off_diagonal) + ";\n"
    code += "int i,j,k,checked,live; ideal J,G;\n"
    code += "for(i=1;i<=size(L0);i++){\n"
    code += " for(j=1;j<=size(L1);j++){\n"
    code += "  for(k=1;k<=size(L2);k++){\n"
    code += "   checked++; J=L0[i]+L1[j]+L2[k]+X; G=std(J);\n"
    code += "   if(G[1]<>1){live++;}\n"
    code += "}}}\n"
    code += 'print("COMPONENTS"); size(L0); size(L1); size(L2);\n'
    code += 'print("CHECKED"); checked; print("LIVE"); live;\n'
    return code


def values_after_marker(output: str, marker: str, count: int):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    start = lines.index(marker) + 1
    return tuple(int(lines[start + offset]) for offset in range(count))


def audit_normal(word_terms, singular: str, normal: str) -> None:
    result = subprocess.run(
        [singular, "-q"],
        input=singular_program(word_terms, normal),
        text=True,
        capture_output=True,
        check=True,
        timeout=600,
    )
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    components, branch_count, _equation_count = EXPECTED[normal]
    assert values_after_marker(result.stdout, "COMPONENTS", 3) == components
    assert values_after_marker(result.stdout, "CHECKED", 1) == (branch_count,)
    assert values_after_marker(result.stdout, "LIVE", 1) == (0,)


def main() -> None:
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for this exact audit")
    word_terms = reconstruct_word_terms()
    for normal in ("line", "plane"):
        audit_normal(word_terms, singular, normal)
    print("fixed-interior two-star Segre obstruction: PASS")
    print("line normal: 9*11*9 = 891 component triples, all unit: PASS")
    print("plane normal: 15*13*14 = 2730 component triples, all unit: PASS")
    print("arbitrary complex shared-star weights and all diagonal targets: PASS")


if __name__ == "__main__":
    main()
