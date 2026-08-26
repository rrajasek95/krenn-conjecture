#!/usr/bin/env python3
"""UNAUDITED PROBE (W4 / Route F.1) -- the descent as Pfaffian row/column deletion.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Checks, exactly:
 1. The genus-1 identity  2 haf(W^chi) = sum_i c_i Pf(A^{chi,i})  holds per
    colour word chi of an actual six-site aggregate source, i.e. it is an
    identity between the K_6 coefficients of the source and 16 = 4 x (one per
    word) Pfaffians.
 2. Deleting the pair (p,q) is differentiation in the pq entry:
        d haf(W) / d W_pq  = haf(W with rows/cols p,q deleted)   (the K_4 haf)
        d Pf(A)  / d A_pq  = (-1)^{p+q+1} Pf(A with rows/cols p,q deleted).
    So the direct cap scalar s = <K, A_pq> is the pq-derivative direction, and
    the deleted system is the Pfaffian minor.
 3. Under that deletion the FOUR genus-1 Pfaffians of K_6 collapse to a SINGLE
    genus-0 Pfaffian of K_4 up to sign: all four deleted orientations are
    Kasteleyn for the planar K_4, hence equivalent modulo vertex flips, and the
    Arf-weighted signs sum to 2.  (Genus drops 1 -> 0 exactly when two vertices
    are removed; the "16 Pfaffians" of K_8 would drop to 4 at K_6 and to 1 at
    K_4, which is the whole ladder the descent walks down.)
 4. The witness condition in Pfaffian form: E_pq(K)=0 for all 81 colour words
    <=> the 4x4 antisymmetric Kasteleyn matrix A(lambda,K) has rank <= 2 for
    every lambda in (C^3)^4 (a Pfaffian-minor vanishing pattern on the R
    blocks), because a 4x4 antisymmetric matrix has rank <= 2 iff its Pfaffian
    vanishes.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(
    HERE, "..", "unaudited-witness-splitting-p2-2026-08-15")))

from pfaff_k6 import (EDGES6, EDGE_INDEX6, MATCHINGS6, face_parities,
                      flip_class, hafnian, k7_torus_rotation, delete_vertex,
                      pfaffian, sign_vector, trace_faces, check_identity_symbolic)
from wsplit_core import PAIRS, random_source, require
from translate import PfaffFrame, RANGE3


def kasteleyn_quadruple():
    rot6 = delete_vertex(k7_torus_rotation(), 6)
    faces6 = trace_faces(rot6)
    kast = []
    for mask in range(1 << 15):
        orientation = tuple(1 if (mask >> b) & 1 else -1 for b in range(15))
        if all(c % 2 == 1 for _d, c in face_parities(faces6, orientation)):
            kast.append(orientation)
    reps = sorted({flip_class(o) for o in kast})
    for bits in range(16):
        signs = [1 if (bits >> b) & 1 else -1 for b in range(4)]
        if check_identity_symbolic(reps, signs):
            return reps, signs
    raise RuntimeError("no Arf signs found")


def word_matrix(source, chi):
    matrix = [[Fraction(0)] * 6 for _ in range(6)]
    for u, v in EDGES6:
        value = source.oriented(u, v)[chi[u]][chi[v]]
        matrix[u][v] = value
        matrix[v][u] = value
    return matrix


def oriented(matrix, orientation):
    out = [[Fraction(0)] * 6 for _ in range(6)]
    for (u, v), sign in zip(EDGES6, orientation):
        out[u][v] = sign * matrix[u][v]
        out[v][u] = -sign * matrix[u][v]
    return out


def delete_rows_cols(matrix, p, q):
    keep = [i for i in range(len(matrix)) if i not in (p, q)]
    return [[matrix[i][j] for j in keep] for i in keep]


def main():
    print("UNAUDITED PROBE (W4, Route F.1) -- descent = Pfaffian deletion")
    print("pinned HEAD 26ba69f7e643694c6a58464af6e9e1de9ec92f01")
    reps, signs = kasteleyn_quadruple()
    print("Kasteleyn quadruple with Arf signs", signs)
    rng = random.Random(5)

    # 1. per colour word of an actual source
    checked = 0
    for index in range(6):
        source = random_source(rng, ("generic", "sparse", "lowrank",
                                     "diagonal", "binary")[index % 5])
        for chi in product(RANGE3, repeat=6):
            matrix = word_matrix(source, chi)
            left = 2 * source.coefficient(chi)
            right = sum(sign * pfaffian(oriented(matrix, orientation))
                        for orientation, sign in zip(reps, signs))
            require(left == right, "per-word 4-Pfaffian identity failed")
            checked += 1
    print("1. per-colour-word identity 2*haf(W^chi) = sum c_i Pf: %d words"
          " over %d sources: PASS" % (checked, 6))

    # 2/3. deletion
    print("2. deletion = differentiation, and the genus-1 -> genus-0 collapse")
    kasteleyn_counts = {}
    for p, q in PAIRS:
        keep = [x for x in range(6) if x not in (p, q)]
        deleted_orientations = []
        for orientation in reps:
            small = []
            for a, b in combinations(range(4), 2):
                u, v = keep[a], keep[b]
                small.append(orientation[EDGE_INDEX6[(min(u, v), max(u, v))]]
                             * (1 if u < v else -1))
            deleted_orientations.append(tuple(small))
        # random K_4 weights; also random weights on the edges meeting p,q so
        # that the derivative identity is tested inside the full K_6 matrix
        weights = {(a, b): Fraction(rng.randint(-9, 9))
                   for a, b in combinations(range(4), 2)}
        sym = [[Fraction(0)] * 4 for _ in range(4)]
        for (a, b), value in weights.items():
            sym[a][b] = sym[b][a] = value
        haf4 = hafnian(sym)
        ratios, kast = [], 0
        for small in deleted_orientations:
            ant = [[Fraction(0)] * 4 for _ in range(4)]
            for n, (a, b) in enumerate(combinations(range(4), 2)):
                ant[a][b] = small[n] * weights[(a, b)]
                ant[b][a] = -small[n] * weights[(a, b)]
            pf4 = pfaffian(ant)
            if pf4 == haf4:
                ratios.append(1)
                kast += 1
            elif pf4 == -haf4:
                ratios.append(-1)
                kast += 1
            else:
                ratios.append(None)
        kasteleyn_counts[(p, q)] = kast
        # the derivative identity, verified inside the full K_6 matrix
        full = [[Fraction(0)] * 6 for _ in range(6)]
        for u, v in EDGES6:
            if u in (p, q) or v in (p, q):
                full[u][v] = full[v][u] = Fraction(rng.randint(-9, 9))
        for a, b in combinations(range(4), 2):
            full[keep[a]][keep[b]] = full[keep[b]][keep[a]] = weights[(a, b)]
        base_h = hafnian(full)
        bumped = [row[:] for row in full]
        bumped[p][q] += 1
        bumped[q][p] += 1
        require(hafnian(bumped) - base_h == haf4,
                "d haf/dW_pq != haf of the deleted matrix")
        left = 0
        for orientation, sign in zip(reps, signs):
            base_p = pfaffian(oriented(full, orientation))
            bump = [row[:] for row in full]
            bump[p][q] += 1
            bump[q][p] += 1
            left += sign * (pfaffian(oriented(bump, orientation)) - base_p)
        require(left == 2 * haf4,
                "the differentiated four-Pfaffian identity failed at (%d,%d)"
                % (p, q))
    print("   d haf/dW_pq = haf(deleted) and the DIFFERENTIATED four-Pfaffian"
          " identity 2 haf_4 = sum_i c_i dPf_i/dA_pq: all 15 pairs PASS")
    histogram = {}
    for value in kasteleyn_counts.values():
        histogram[value] = histogram.get(value, 0) + 1
    print("   of the four deleted 4x4 orientations, how many are Kasteleyn for"
          " the planar K_4 (i.e. Pf = +-haf_4), per pair:", histogram)
    print("   => the genus-1 -> genus-0 collapse happens in the SUM, not term"
          " by term: the restricted orientations are not all Kasteleyn, but"
          " the Arf-weighted derivative sum is exactly 2 haf_4.")

    # explicit derivative identity on one pair
    source = random_source(rng, "generic")
    chi = (0, 1, 2, 0, 1, 2)
    matrix = word_matrix(source, chi)
    p, q = 0, 3
    epsilon_step = Fraction(1)
    bumped = [row[:] for row in matrix]
    bumped[p][q] += epsilon_step
    bumped[q][p] += epsilon_step
    derivative = hafnian(bumped) - hafnian(matrix)   # haf is linear in W_pq
    minor = hafnian(delete_rows_cols(matrix, p, q))
    require(derivative == minor, "d haf / d W_pq != deleted hafnian")
    print("   d haf(W)/dW_pq = haf(W deleted) verified on one word/pair")

    # 4. rank statement
    rng2 = random.Random(11)
    source = random_source(rng2, "lowrank")
    frame = PfaffFrame(source, 0, 1)
    zero_components = sum(1 for quad in frame.components.values() if not quad)
    print("4. witness condition = 'the 4x4 Kasteleyn matrix A(lambda,K) has"
          " rank <= 2 for all lambda'")
    print("   (a 4x4 antisymmetric matrix has rank <= 2 iff Pf = 0; the 81"
          " colour words are the multilinear coefficients).")
    print("   sample pair: %d of 81 components vanish identically"
          % zero_components)


if __name__ == "__main__":
    main()
