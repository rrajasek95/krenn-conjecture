#!/usr/bin/env python3
"""Exact experiments for a controlled perturbation of the internal 23 block.

The fixed eight internal cells are retained and

    A_23 = t E_21 + s E_00.

For a rational specialization (t,s), this script reconstructs the cylinder
intersections and can ask Singular whether the actual two-star factorized
equations have a complex point.  It is an exploration driver, not by itself
a uniform theorem in the parameters.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import shutil
import subprocess
from fractions import Fraction

import verify_three_cut_fourth_cut_fixed_interior_intersection as cylinders
import verify_three_cut_two_boundary_star_fourth_cut_segre_obstruction as segre


Q = Fraction
SIX = tuple(range(6))
COLOURS = tuple(range(3))
E0 = (0, 0, 0, 0, 0, 0)
U0 = cylinders.U0
UPLUS = cylinders.TAIL_SUM


def blocks_at(t: Q, s: Q):
    blocks = cylinders.aggregate()
    block = {}
    if t:
        block[(2, 1)] = t
    if s:
        block[(0, 0)] = s
    blocks[(2, 3)] = block
    return blocks


def scaled(vector, scalar):
    return {word: scalar * value for word, value in vector.items() if scalar * value}


def vector_sum(*vectors):
    answer = {}
    for vector in vectors:
        for word, value in vector.items():
            cylinders.add(answer, word, value)
    return answer


def normal_basis(t: Q, s: Q, normal: str):
    moving = vector_sum(scaled(U0, t), {E0: s} if s else {})
    hs = vector_sum(moving, UPLUS)
    if normal == "line":
        return [hs]
    if normal == "plane":
        return [moving, UPLUS] if moving else [UPLUS]
    raise ValueError(normal)


def reconstruct_word_terms(blocks):
    word_terms = collections.defaultdict(list)
    for i in SIX:
        for j in range(i + 1, 6):
            rest = tuple(site for site in SIX if site not in (i, j))
            cofactor = cylinders.matching_tensor(rest, blocks)
            for rest_word, coefficient in cofactor.items():
                for ci, cj in itertools.product(COLOURS, repeat=2):
                    assignment = dict(zip(rest, rest_word))
                    assignment[i] = ci
                    assignment[j] = cj
                    word = tuple(assignment[site] for site in SIX)
                    word_terms[word].append((((i, ci), (j, cj)), coefficient))
    return word_terms


def variable(kind, boundary_colour, endpoint):
    site, internal_colour = endpoint
    return f"{kind}{boundary_colour}{site}{internal_colour}"


def qtext(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def bilinear(word_terms, a, b, word):
    terms = []
    for (left, right), coefficient in word_terms.get(word, ()):
        factor = qtext(coefficient)
        terms.append(factor + "*" + variable("p", a, left) + "*" + variable("q", b, right))
        terms.append(factor + "*" + variable("p", a, right) + "*" + variable("q", b, left))
    return "+".join(terms) if terms else "0"


def membership_rows(basis, coordinates):
    """Return exact annihilator rows for membership in span(basis)."""
    span = cylinders.echelon(basis)
    pivots = tuple(span)
    rows = []
    for coordinate in coordinates:
        if coordinate in span:
            continue
        row = {coordinate: Q(1)}
        for pivot in pivots:
            value = -span[pivot].get(coordinate, Q(0))
            if value:
                row[pivot] = value
        rows.append(row)
    return rows


def fibre_equations(word_terms, basis, a, b, target):
    normal_coordinates = {
        word for vector in basis for word in vector
    }
    target_coordinates = {(colour,) * 6 for colour in COLOURS}
    coordinates = tuple(
        sorted(set(word_terms) | normal_coordinates | target_coordinates)
    )
    # The explicit union includes every normal and target coordinate even if
    # a specialization makes a beta coordinate disappear.
    rows = membership_rows(basis, coordinates)
    answer = []
    target_word = (target,) * 6 if target is not None else None
    for row in rows:
        terms = []
        constant = Q(0)
        for word, coefficient in row.items():
            expression = bilinear(word_terms, a, b, word)
            terms.append(qtext(coefficient) + "*(" + expression + ")")
            if word == target_word:
                constant -= coefficient
        if constant:
            terms.append(qtext(constant))
        answer.append("+".join(terms))
    return answer


def singular_program(word_terms, basis, active_colours):
    types = tuple((site, colour) for site in SIX for colour in COLOURS)
    names = [
        variable(kind, boundary, endpoint)
        for kind in ("p", "q")
        for boundary in active_colours
        for endpoint in types
    ]
    diagonal = {
        c: fibre_equations(word_terms, basis, c, c, c)
        for c in active_colours
    }
    off_diagonal = []
    for a, b in itertools.product(active_colours, repeat=2):
        if a != b:
            off_diagonal.extend(fibre_equations(word_terms, basis, a, b, None))
    code = "ring r=0,(" + ",".join(names) + "),dp;\n"
    code += 'LIB "primdec.lib";\n'
    for colour in active_colours:
        code += f"ideal I{colour}=" + ",".join(diagonal[colour]) + ";\n"
        code += f"list L{colour}=minAssGTZ(I{colour});\n"
    code += "ideal X=" + ",".join(off_diagonal) + ";\n"
    code += "int i,j,k,checked,live; ideal J,G;\n"
    if tuple(active_colours) == (0, 1, 2):
        code += "for(i=1;i<=size(L0);i++){\n"
        code += " for(j=1;j<=size(L1);j++){\n"
        code += "  for(k=1;k<=size(L2);k++){\n"
        code += "   checked++; J=L0[i]+L1[j]+L2[k]+X; G=std(J);\n"
        code += "   if(G[1]<>1){live++; print(\"LIVE_TRIPLE\"); i;j;k;}\n"
        code += "}}}\n"
        code += 'print("COMPONENTS"); size(L0); size(L1); size(L2);\n'
    elif len(active_colours) == 2:
        left, right = active_colours
        code += f"for(i=1;i<=size(L{left});i++){{\n"
        code += f" for(j=1;j<=size(L{right});j++){{\n"
        code += f"  checked++; J=L{left}[i]+L{right}[j]+X; G=std(J);\n"
        code += "  if(G[1]<>1){live++; print(\"LIVE_PAIR\"); i;j;}\n"
        code += "}}\n"
        code += f'print("COMPONENTS"); size(L{left}); size(L{right});\n'
    else:
        raise ValueError("active colours must be exactly two or all three")
    code += 'print("CHECKED"); checked; print("LIVE"); live;\n'
    return code, tuple(len(diagonal[c]) for c in active_colours), len(off_diagonal)


def same_span(observed, expected):
    left = cylinders.echelon(observed)
    right = cylinders.echelon(expected)
    return (
        len(left) == len(right)
        and all(cylinders.member(v, left) for v in expected)
        and all(cylinders.member(v, right) for v in observed)
    )


def audit_cylinders(blocks, t, s):
    moving = vector_sum(scaled(U0, t), {E0: s} if s else {})
    hs = vector_sum(moving, UPLUS)
    expected = {
        (2, 3, 4, 0): [moving, UPLUS] if moving else [UPLUS],
        (2, 3, 4, 1): [moving, UPLUS] if moving else [UPLUS],
        (2, 3, 4, 5): [hs],
    }
    for cuts, basis in expected.items():
        observed = cylinders.cylinder_intersection(cuts, blocks)
        print("cuts", cuts, "dimension", len(observed), "expected_span", same_span(observed, basis))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--t", type=Q, default=Q(1))
    parser.add_argument("--s", type=Q, default=Q(0))
    parser.add_argument("--normal", choices=("line", "plane"), default="plane")
    parser.add_argument("--singular", action="store_true")
    parser.add_argument(
        "--active-colours", default="0,1,2",
        help="comma-separated boundary colours retained in the exact Segre system",
    )
    args = parser.parse_args()

    blocks = blocks_at(args.t, args.s)
    audit_cylinders(blocks, args.t, args.s)
    word_terms = reconstruct_word_terms(blocks)
    print("reachable_words", len(word_terms), "weighted_atoms", sum(len(v) for v in word_terms.values()))
    basis = normal_basis(args.t, args.s, args.normal)
    print("normal", args.normal, "dimension", len(cylinders.echelon(basis)))
    if not args.singular:
        return
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    active_colours = tuple(int(value) for value in args.active_colours.split(","))
    if active_colours not in ((0, 1, 2), (0, 1), (0, 2), (1, 2)):
        raise SystemExit("active colours must be 0,1,2 or an increasing pair")
    program, diagonal_counts, off_count = singular_program(
        word_terms, basis, active_colours
    )
    print("equations", diagonal_counts, off_count)
    result = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=1800,
    )
    if result.stderr.strip():
        print(result.stderr)
    print(result.stdout)


if __name__ == "__main__":
    main()
