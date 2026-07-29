#!/usr/bin/env python3
"""Independent exact audit of the fixed-interior two-star Segre obstruction.

No primary module is imported.  Matching cofactors and bilinear coordinate
polynomials are reconstructed from endpoint-ordered sources.  A freshly
generated Singular/Q computation decomposes each diagonal fiber and checks
an exact unit standard basis for every component triple after adjoining all
six ordered off-diagonal fibers.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, product
import shutil
import subprocess


SITES = tuple(range(6))
COLOURS = (0, 1, 2)
SOURCES = (
    (0, 1, 0, 0), (4, 5, 0, 0),
    (0, 2, 1, 1), (1, 4, 1, 1),
    (0, 4, 2, 2), (1, 3, 2, 2),
    (2, 5, 0, 0), (3, 5, 1, 0),
    (2, 3, 2, 1),
)

U0 = (0, 0, 2, 1, 0, 0)
UPLUS = (
    (1, 2, 1, 2, 0, 0),
    (1, 1, 1, 1, 1, 0),
    (2, 2, 0, 2, 2, 0),
)
HS_WORDS = (U0,) + UPLUS


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        mate = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            result.append(((first, mate),) + tail)
    return tuple(result)


def edge_blocks():
    result = {}
    for left, right, colour_left, colour_right in SOURCES:
        assert left < right
        result[(left, right)] = (colour_left, colour_right)
    return result


def matching_tensor(vertices: tuple[int, ...], blocks):
    position = {site: index for index, site in enumerate(vertices)}
    result = defaultdict(int)
    for matching in perfect_matchings(vertices):
        if any(edge not in blocks for edge in matching):
            continue
        word = [-1] * len(vertices)
        for left, right in matching:
            word[position[left]], word[position[right]] = blocks[left, right]
        result[tuple(word)] += 1
    return dict(result)


EXPECTED_COFACTORS = {
    (0, 1): ((2, 1, 0, 0),),
    (0, 2): ((1, 1, 1, 0), (2, 2, 0, 0)),
    (0, 3): ((1, 0, 1, 0),),
    (0, 4): ((2, 0, 2, 0),),
    (0, 5): ((1, 2, 1, 1),),
    (1, 2): ((2, 1, 2, 0),),
    (1, 3): ((1, 1, 0, 0), (2, 0, 2, 0)),
    (1, 4): ((1, 1, 1, 0),),
    (1, 5): ((2, 2, 1, 2),),
    (2, 3): ((0, 0, 0, 0),),
    (2, 4): ((0, 0, 1, 0),),
    (2, 5): ((2, 2, 2, 2),),
    (3, 4): ((0, 0, 0, 0),),
    (3, 5): ((1, 1, 1, 1),),
    (4, 5): ((0, 0, 2, 1), (1, 2, 1, 2)),
}


def reconstruct_atoms():
    blocks = edge_blocks()
    assert matching_tensor(SITES, blocks) == {word: 1 for word in HS_WORDS}
    observed_cofactors = {}
    atoms = defaultdict(list)
    for i, j in combinations(SITES, 2):
        rest = tuple(site for site in SITES if site not in (i, j))
        cofactor = matching_tensor(rest, blocks)
        observed_cofactors[i, j] = tuple(sorted(cofactor))
        assert all(coefficient == 1 for coefficient in cofactor.values())
        for rest_word in cofactor:
            for colour_i, colour_j in product(COLOURS, repeat=2):
                assignment = dict(zip(rest, rest_word))
                assignment[i] = colour_i
                assignment[j] = colour_j
                word = tuple(assignment[site] for site in SITES)
                atoms[word].append((i, colour_i, j, colour_j))
    assert observed_cofactors == EXPECTED_COFACTORS
    assert sum(map(len, atoms.values())) == 162
    assert len(atoms) == 126
    assert Counter(map(len, atoms.values())) == {1: 96, 2: 25, 3: 4, 4: 1}
    assert all((colour,) * 6 in atoms for colour in COLOURS)
    return atoms


ENDPOINTS = tuple(product(SITES, COLOURS))


def name(star: str, boundary_colour: int, site: int, internal_colour: int):
    # Names differ deliberately from the primary p/q convention.
    return f"{star}{boundary_colour}_{site}_{internal_colour}"


def coordinate_polynomial(atoms, boundary6: int, boundary7: int, word):
    terms = []
    for i, colour_i, j, colour_j in atoms[word]:
        terms.append(
            name("x", boundary6, i, colour_i)
            + "*" + name("y", boundary7, j, colour_j)
        )
        terms.append(
            name("x", boundary6, j, colour_j)
            + "*" + name("y", boundary7, i, colour_i)
        )
    return "+".join(terms)


def fiber_equations(atoms, normal: str, a: int, b: int, diagonal_colour):
    exceptional = set(HS_WORDS)
    equations = []
    for word in sorted(atoms):
        if word in exceptional:
            continue
        expression = coordinate_polynomial(atoms, a, b, word)
        if diagonal_colour is not None and word == (diagonal_colour,) * 6:
            expression += "-1"
        equations.append(expression)

    if normal == "line":
        base = coordinate_polynomial(atoms, a, b, U0)
        for word in UPLUS:
            equations.append(
                coordinate_polynomial(atoms, a, b, word) + "-(" + base + ")"
            )
    elif normal == "plane":
        base = coordinate_polynomial(atoms, a, b, UPLUS[0])
        for word in UPLUS[1:]:
            equations.append(
                coordinate_polynomial(atoms, a, b, word) + "-(" + base + ")"
            )
    else:
        raise AssertionError(normal)
    return equations


EXPECTED = {
    "line": ((9, 11, 9), 891, 1125, 125),
    "plane": ((15, 13, 14), 2730, 1116, 124),
}


def make_singular_program(atoms, normal: str):
    variables = [
        name(star, boundary, site, colour)
        for star in ("x", "y")
        for boundary in COLOURS
        for site, colour in ENDPOINTS
    ]
    assert len(variables) == 108 == len(set(variables))

    diagonal = [
        fiber_equations(atoms, normal, colour, colour, colour)
        for colour in COLOURS
    ]
    off_diagonal = []
    for a, b in product(COLOURS, repeat=2):
        if a != b:
            off_diagonal.extend(fiber_equations(atoms, normal, a, b, None))

    _components, _triples, total_count, per_fiber = EXPECTED[normal]
    assert all(len(equations) == per_fiber for equations in diagonal)
    assert len(off_diagonal) == 6 * per_fiber
    assert sum(map(len, diagonal)) + len(off_diagonal) == total_count

    lines = [
        "ring R=0,(" + ",".join(variables) + "),dp;",
        'LIB "primdec.lib";',
    ]
    for colour in COLOURS:
        lines.append(f"ideal D{colour}=" + ",".join(diagonal[colour]) + ";")
        lines.append(f"list M{colour}=minAssGTZ(D{colour});")
    lines.append("ideal OFF=" + ",".join(off_diagonal) + ";")
    lines.extend([
        "int i,j,k,total,units,nonunits; ideal J,G;",
        "for(i=1;i<=size(M0);i++){",
        " for(j=1;j<=size(M1);j++){",
        "  for(k=1;k<=size(M2);k++){",
        "   total++; J=M0[i]+M1[j]+M2[k]+OFF; G=std(J);",
        "   if(reduce(1,G)==0){units++;}else{nonunits++;}",
        "}}}",
        'print("COUNTS"); size(M0); size(M1); size(M2);',
        'print("TOTAL"); total; print("UNITS"); units;',
        'print("NONUNITS"); nonunits;',
    ])
    return "\n".join(lines) + "\n"


def marker_values(output: str, marker: str, count: int):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    start = lines.index(marker) + 1
    return tuple(int(lines[start + index]) for index in range(count))


def run_exact_certificate(atoms, normal: str, singular: str):
    completed = subprocess.run(
        [singular, "-q"],
        input=make_singular_program(atoms, normal),
        text=True,
        capture_output=True,
        check=True,
        timeout=600,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    component_counts, triples, _equations, _per_fiber = EXPECTED[normal]
    assert marker_values(completed.stdout, "COUNTS", 3) == component_counts
    assert marker_values(completed.stdout, "TOTAL", 1) == (triples,)
    assert marker_values(completed.stdout, "UNITS", 1) == (triples,)
    assert marker_values(completed.stdout, "NONUNITS", 1) == (0,)


def main():
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    atoms = reconstruct_atoms()
    for normal in ("line", "plane"):
        run_exact_certificate(atoms, normal, singular)
    print("independent fixed-interior two-star Segre audit: PASS")
    print("cofactors: 162 atoms, 126 coordinates, multiplicities 96/25/4/1")
    print("line: 9*11*9=891 exact unit component triples")
    print("plane: 15*13*14=2730 exact unit component triples")
    print("all 108 star entries and all nine target boundary fibers retained")
    print("scope: fixed interior only; boundary block 67 is absorbed")


if __name__ == "__main__":
    main()
