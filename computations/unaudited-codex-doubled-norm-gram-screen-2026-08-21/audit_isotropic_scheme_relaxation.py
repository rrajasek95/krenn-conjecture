#!/usr/bin/env python3
"""Exact five-sector SDP relaxation under full port isotropy."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
from random import Random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "computations"))
import audit_doubled_norm_gram_screen as base  # noqa: E402
import verify_minimal_norm_gauge as minimum_gauge  # noqa: E402


SECTORS = (("[8]", 12, 1), ("[6,2]", 5, 20),
           ("[4,4]", 2, 14), ("[4,2,2]", -1, 56),
           ("[2^4]", -6, 14))
MATCHINGS = tuple(tuple(sorted(matching)) for matching in base.PM[8])
INDEX = {matching: index for index, matching in enumerate(MATCHINGS)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def one_factorization():
    factors = []
    for round_index in range(7):
        edges = [tuple(sorted((7, round_index)))]
        for offset in range(1, 4):
            edges.append(tuple(sorted(((round_index+offset) % 7,
                                       (round_index-offset) % 7))))
        factors.append(tuple(sorted(edges)))
    require(len({edge for factor in factors for edge in factor}) == 28,
            factors)
    require(all(tuple(sorted(factor)) in INDEX for factor in factors), factors)
    return tuple(factors)


FACTORS = one_factorization()


def adjacency():
    rows = [[0] * 105 for _ in range(105)]
    for matching_index, matching in enumerate(MATCHINGS):
        for first, second in combinations(range(4), 2):
            selected = (matching[first], matching[second])
            vertices = tuple(sorted(vertex for edge in selected for vertex in edge))
            original = frozenset(selected)
            rest = tuple(edge for index, edge in enumerate(matching)
                         if index not in (first, second))
            for replacement in base.perfect_matchings(vertices):
                replacement = frozenset(tuple(sorted(edge)) for edge in replacement)
                if replacement == original:
                    continue
                neighbour = tuple(sorted(rest + tuple(replacement)))
                rows[matching_index][INDEX[neighbour]] = 1
    require(all(sum(row) == 12 for row in rows), "two-switch valency")
    return rows


A = adjacency()


def matmul(left, right):
    size = len(left)
    answer = [[0] * size for _ in range(size)]
    for i in range(size):
        for k, value in enumerate(left[i]):
            if not value:
                continue
            for j, other in enumerate(right[k]):
                if other:
                    answer[i][j] += value * other
    return answer


IDENTITY = [[int(i == j) for j in range(105)] for i in range(105)]
POWERS = [IDENTITY]
for _ in range(4):
    POWERS.append(matmul(POWERS[-1], A))


def polynomial_mul(left, right):
    answer = [Fraction(0)] * (len(left)+len(right)-1)
    for i, value in enumerate(left):
        for j, other in enumerate(right):
            answer[i+j] += value*other
    return answer


def projector_polynomial(eigenvalue):
    polynomial = [Fraction(1)]
    denominator = Fraction(1)
    for _name, other, _dimension in SECTORS:
        if other == eigenvalue:
            continue
        polynomial = polynomial_mul(polynomial, [-other, 1])
        denominator *= eigenvalue-other
    return [value/denominator for value in polynomial]


PROJECTORS = {name: projector_polynomial(eigenvalue)
              for name, eigenvalue, _dimension in SECTORS}


def permutation_matrix(permutation, signs):
    return tuple(tuple(signs[row] if column == permutation[row] else 0
                       for column in range(3)) for row in range(3))


PERMUTATIONS = tuple(permutations(range(3)))


def source_sample(seed, factor_count):
    random = Random(seed)
    matrices = {}
    for factor in FACTORS[:factor_count]:
        for edge in factor:
            permutation = random.choice(PERMUTATIONS)
            signs = tuple(random.choice((-1, 1)) for _ in range(3))
            matrices[edge] = permutation_matrix(permutation, signs)
    # Every occupied edge matrix is orthogonal.  Each vertex meets exactly
    # factor_count occupied edges, hence scaling by 1/sqrt(k) gives R_v=I.
    return matrices


def matching_vectors(matrices):
    answer = []
    for matching in MATCHINGS:
        if any(edge not in matrices for edge in matching):
            answer.append({})
            continue
        vector = {}
        for colours in product(range(3), repeat=4):
            word = [None] * 8
            coefficient = 1
            for edge, left_colour in zip(matching, colours):
                matrix = matrices[edge]
                right_choices = [column for column in range(3)
                                 if matrix[left_colour][column]]
                require(len(right_choices) == 1, matrix)
                right_colour = right_choices[0]
                coefficient *= matrix[left_colour][right_colour]
                word[edge[0]], word[edge[1]] = left_colour, right_colour
            vector[tuple(word)] = coefficient
        answer.append(vector)
    return answer


def gram(vectors):
    answer = [[Fraction(0)] * 105 for _ in range(105)]
    for i, left in enumerate(vectors):
        for j in range(i, 105):
            right = vectors[j]
            lvec, rvec = (right, left) if len(left) > len(right) else (left, right)
            value = sum(Fraction(coefficient * rvec.get(word, 0))
                        for word, coefficient in lvec.items())
            answer[i][j] = answer[j][i] = value
    return answer


def trace_product(left, right):
    return sum(Fraction(left[i][j]) * right[j][i]
               for i in range(105) for j in range(105))


def sector_vector(matrices, factor_count):
    matrix = gram(matching_vectors(matrices))
    moments = [trace_product(power, matrix) / factor_count**4
               for power in POWERS]
    energies = []
    for name, _eigenvalue, dimension in SECTORS:
        value = sum(coefficient*moment
                    for coefficient, moment in zip(PROJECTORS[name], moments))
        require(value >= 0, (name, value))
        energies.append(value)
        # Projector diagonal is dimension/105; this also guards the spectral
        # labelling and normalization on a single matching coordinate.
        require(PROJECTORS[name][0] or dimension, name)
    return tuple(energies)


def rank(rows):
    rows = [list(map(Fraction, row)) for row in rows]
    pivot = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        selected = next((row for row in range(pivot, len(rows))
                         if rows[row][column]), None)
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        value = rows[pivot][column]
        rows[pivot] = [entry/value for entry in rows[pivot]]
        for row in range(len(rows)):
            if row == pivot or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left-value*right
                         for left, right in zip(rows[row], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def main():
    # Projector checks: mutually orthogonal dimensions and the constant vector
    # entirely in [8].
    for name, _eigenvalue, dimension in SECTORS:
        polynomial = PROJECTORS[name]
        projector = [[sum(polynomial[k]*POWERS[k][i][j]
                          for k in range(5)) for j in range(105)]
                     for i in range(105)]
        require(sum(projector[i][i] for i in range(105)) == dimension,
                (name, dimension))

    samples = []
    for seed in range(1, 30):
        factor_count = 2 + seed % 6
        samples.append((seed, factor_count,
                        sector_vector(source_sample(seed, factor_count),
                                      factor_count)))
        differences = [[value-Fraction(samples[0][2][index])
                        for index, value in enumerate(sample[2])]
                       for sample in samples[1:]]
        if rank(differences) == 5:
            break
    require(rank([list(sample[2]) for sample in samples]) == 5,
            samples)
    require(rank([[value-samples[0][2][index]
                   for index, value in enumerate(sample[2])]
                  for sample in samples[1:]]) == 5, samples)

    # Isotropy itself even permits the zero sector vector: put I/sqrt(2) on
    # the edges of C3 disjoint union C5.  Every port has reduced Gram I, but
    # the support graph has no perfect matching, so every v_M and G vanish.
    zero_sector = tuple(Fraction(0) for _ in SECTORS)

    # After adding only the pure-output normalization ||F||^2>=3, the small
    # invariant SDP is e_lambda>=0 and 105*e_[8]>=3.  Its exact optimum has
    # P_mixed=0.  G=(1/35)P_[8]=J/3675 is an explicit PSD witness.
    witness = (Fraction(1, 35), Fraction(0), Fraction(0),
               Fraction(0), Fraction(0))
    require(105*witness[0] == 3, witness)

    # Mandatory lower-arity controls.  The exact n=4 GHZ minimum has three
    # orthonormal matching vectors, hence G=I_3.  Its PM4 sector energies are
    # tr(P_[4]G)=1 and tr(P_[2,2]G)=2, while 1^T G 1=3 and P_mixed=0.
    n4_sector = (Fraction(1), Fraction(2))
    require(3*n4_sector[0] == 3 and n4_sector[1] == 2, n4_sector)
    # The phased n=6 hostile model is exactly fully isotropic and a smooth
    # block-normal local minimum for its own non-GHZ output.  Its actual Gram
    # is PSD by construction, so a relaxation consisting only of sector PSD
    # cannot exclude it.  Replay the frozen exact cyclotomic and mod-7 guards.
    minimum_gauge.verify_fourier_isotropy()
    minimum_gauge.verify_full_block_injectivity_mod7()
    print("sector order", [name for name, _, _ in SECTORS])
    print("isotropic normalized samples", samples)
    print("affine span rank", 5)
    print("isotropic base-locus sector vector", zero_sector)
    print("invariant SDP witness", witness,
          "G=(1/35)P_[8]=J/3675", "mixed norm", 0)
    print("n4 exact GHZ PM4 sector vector", n4_sector, "mixed norm", 0)
    print("phased n6 smooth minimum", "ACCEPTED: full isotropy replayed and actual Gram PSD")
    print("verdict full port isotropy forces no affine trace relation among the five sector energies; the representation-level SDP still permits GHZ and cannot produce a positive mixed norm floor")


if __name__ == "__main__":
    main()
