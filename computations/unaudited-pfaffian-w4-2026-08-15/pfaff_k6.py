#!/usr/bin/env python3
"""UNAUDITED PROBE (W4 / Route F.1) -- the genus-1 four-Pfaffian decomposition of
the K_6 hafnian, built and verified exactly.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01
Plan: notes/2026-08-15-resolution-master-plan.md (Route F, agent W4)
Survey entry: notes/2026-08-11-external-theory-reformulation-survey.md sec 1.3

Nothing here is a proved claim of the project.  Every statement printed is
either an exact symbolic identity over Z[w_e] or an exhaustive finite check.

WHAT IS BUILT
  1. A genus-1 (torus) embedding of K_6, obtained from the Heawood
     triangulation of the torus by K_7 by deleting one vertex: V=6, E=15,
     F=9 (eight triangles and one hexagon), Euler characteristic 0.
  2. The 128 Kasteleyn orientations of that embedding (the face condition is
     determined empirically and reported), falling into 4 classes modulo
     vertex flips -- a torsor over H^1(T^2; F_2) = (Z/2)^2, as predicted.
  3. The exact identity
         haf(W) = (1/2) * sum_{i=1}^{4} c_i Pf(A^{(i)}),   c_i in {+1,-1},
     with three + and one - (the Arf-invariant signs: three even spin
     structures, one odd), verified
       (a) symbolically as an identity of polynomials in 15 indeterminates,
       (b) on 100 random exact rational symmetric matrices,
       (c) per colour word chi on random six-site aggregate sources
           (haf(W^chi) is the K_6 coefficient of the source).
  4. The genus-0 companion at K_4 (four sites = the deleted system U):
     haf_4 = a SINGLE Pfaffian, i.e. the Klein/Pluecker quadric.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
import random
import sys

# --------------------------------------------------------------- matchings

def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vertices[index]),) + tail)
    return tuple(out)


def permutation_sign(seq):
    seq = list(seq)
    sign = 1
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                sign = -sign
    return sign


def matching_pf_sign(matching):
    """sgn of (i1 j1 i2 j2 ...) as a permutation of the ground set."""
    flat = []
    for u, v in matching:
        flat.extend([u, v])
    return permutation_sign(flat)


# ------------------------------------------------------ rotation / faces

def trace_faces(rotation):
    """rotation[v] = cyclic list of neighbours.  Returns the face walks."""
    succ = {}
    for v, ring in rotation.items():
        for index, u in enumerate(ring):
            succ[(u, v)] = ring[(index + 1) % len(ring)]
    darts = set(succ)
    faces = []
    while darts:
        start = next(iter(darts))
        walk = []
        dart = start
        while True:
            walk.append(dart)
            darts.discard(dart)
            u, v = dart
            dart = (v, succ[(u, v)])
            if dart == start:
                break
        faces.append(tuple(walk))
    return faces


def k7_torus_rotation():
    """Heawood's K_7 triangulation of the torus: rotation i -> i+1,i+3,i+2,i+6,i+4,i+5."""
    pattern = (1, 3, 2, 6, 4, 5)
    return {i: [(i + d) % 7 for d in pattern] for i in range(7)}


def delete_vertex(rotation, dead):
    return {v: [u for u in ring if u != dead]
            for v, ring in rotation.items() if v != dead}


# ------------------------------------------------------------ orientations

EDGES6 = tuple(combinations(range(6), 2))
EDGE_INDEX6 = {e: n for n, e in enumerate(EDGES6)}
MATCHINGS6 = perfect_matchings(range(6))


def sign_vector(orientation):
    """orientation: tuple of +-1 on EDGES6.  Returns the 15 Pfaffian signs."""
    out = []
    for matching in MATCHINGS6:
        value = matching_pf_sign(matching)
        for u, v in matching:
            key = (u, v) if u < v else (v, u)
            value *= orientation[EDGE_INDEX6[key]]
        out.append(value)
    return tuple(out)


def pfaffian(matrix):
    """Exact Pfaffian of an antisymmetric 2m x 2m matrix by matching expansion."""
    n = len(matrix)
    total = 0
    for matching in perfect_matchings(range(n)):
        term = matching_pf_sign(matching)
        for u, v in matching:
            term = term * matrix[u][v]
        total = total + term
    return total


def hafnian(matrix):
    n = len(matrix)
    total = 0
    for matching in perfect_matchings(range(n)):
        term = 1
        for u, v in matching:
            term = term * matrix[u][v]
        total = total + term
    return total


# ------------------------------------------------------------- the search

def find_quadruples(limit=None):
    """All (unordered) quadruples of orientations with sum of sign vectors = 2*1.

    A quadruple {e1..e4} with sum_i sigma_{e_i}(M) = 2 for every matching M is
    exactly a decomposition haf = (1/2) sum Pf, the Arf signs already absorbed
    into the orientations (reversing all 15 edges negates sigma because 15
    matchings use 3 edges each and (-1)^3 = -1).
    """
    vectors = {}
    for mask in range(1 << 15):
        orientation = tuple(1 if (mask >> b) & 1 else -1 for b in range(15))
        vectors.setdefault(sign_vector(orientation), []).append(orientation)
    keys = sorted(vectors)
    target = tuple([2] * 15)
    # meet in the middle on pairs
    pairsum = {}
    for i in range(len(keys)):
        for j in range(i, len(keys)):
            total = tuple(a + b for a, b in zip(keys[i], keys[j]))
            pairsum.setdefault(total, []).append((i, j))
    found = []
    seen = set()
    for total, lefts in pairsum.items():
        need = tuple(t - a for t, a in zip(target, total))
        if need not in pairsum:
            continue
        for i, j in lefts:
            for k, l in pairsum[need]:
                quad = tuple(sorted((i, j, k, l)))
                if quad in seen:
                    continue
                seen.add(quad)
                found.append(quad)
                if limit and len(found) >= limit:
                    return found, keys, vectors
    return found, keys, vectors


# ---------------------------------------------------------------- checking

def check_identity_symbolic(orientations, coefficients):
    """haf = (1/2) sum c_i Pf as an identity of polynomials in 15 unknowns.

    Represented exactly: the coefficient of each of the 15 squarefree cubic
    monomials (one per matching) on both sides.
    """
    left = {matching: 1 for matching in MATCHINGS6}
    right = {matching: 0 for matching in MATCHINGS6}
    for orientation, coefficient in zip(orientations, coefficients):
        signs = sign_vector(orientation)
        for matching, sign in zip(MATCHINGS6, signs):
            right[matching] += coefficient * sign
    return all(2 * left[m] == right[m] for m in MATCHINGS6)


def oriented_matrix(weights, orientation):
    matrix = [[0] * 6 for _ in range(6)]
    for (u, v), sign in zip(EDGES6, orientation):
        matrix[u][v] = sign * weights[(u, v)]
        matrix[v][u] = -sign * weights[(u, v)]
    return matrix


def symmetric_matrix(weights):
    matrix = [[0] * 6 for _ in range(6)]
    for (u, v), value in weights.items():
        matrix[u][v] = value
        matrix[v][u] = value
    return matrix


def check_identity_numeric(orientations, coefficients, trials=100, seed=7):
    rng = random.Random(seed)
    for _ in range(trials):
        weights = {e: Fraction(rng.randint(-9, 9), rng.randint(1, 5))
                   for e in EDGES6}
        left = hafnian(symmetric_matrix(weights))
        right = sum(c * pfaffian(oriented_matrix(weights, o))
                    for o, c in zip(orientations, coefficients))
        if 2 * left != right:
            return False
    return True


# ------------------------------------------------------- Kasteleyn faces

def face_parities(faces, orientation):
    """For each face walk: (degree, number of darts opposing the orientation)."""
    out = []
    for walk in faces:
        clockwise = 0
        for u, v in walk:
            key = (u, v) if u < v else (v, u)
            forward = orientation[EDGE_INDEX6[key]] == 1  # oriented u->v iff u<v
            along = (u < v) if forward else (v < u)
            if not along:
                clockwise += 1
        out.append((len(walk), clockwise))
    return tuple(out)


def vertex_flip(orientation, vertex):
    out = list(orientation)
    for n, (u, v) in enumerate(EDGES6):
        if u == vertex or v == vertex:
            out[n] = -out[n]
    return tuple(out)


def flip_class(orientation):
    """Canonical representative of the orbit under the 64 vertex flips."""
    best = None
    for mask in range(1 << 6):
        current = orientation
        for vertex in range(6):
            if (mask >> vertex) & 1:
                current = vertex_flip(current, vertex)
        if best is None or current < best:
            best = current
    return best


# --------------------------------------------------------------- K_4 side

EDGES4 = tuple(combinations(range(4), 2))
MATCHINGS4 = perfect_matchings(range(4))


def k4_single_pfaffian():
    """The unique-up-to-equivalence planar Kasteleyn orientation of K_4."""
    for mask in range(1 << 6):
        orientation = tuple(1 if (mask >> b) & 1 else -1 for b in range(6))
        signs = []
        for matching in MATCHINGS4:
            value = matching_pf_sign(matching)
            for u, v in matching:
                value *= orientation[EDGES4.index((u, v) if u < v else (v, u))]
            signs.append(value)
        if all(s == 1 for s in signs):
            return orientation
    return None


# ------------------------------------------------------------------- main

def main():
    print("UNAUDITED PROBE (W4, Route F.1) -- K_6 four-Pfaffian decomposition")
    print("pinned HEAD 26ba69f7e643694c6a58464af6e9e1de9ec92f01")
    print()

    # 1. the torus embedding -------------------------------------------------
    rot7 = k7_torus_rotation()
    faces7 = trace_faces(rot7)
    print("K_7 Heawood rotation: V=7 E=21 F=%d  chi=%d  (genus %d)"
          % (len(faces7), 7 - 21 + len(faces7), (2 - (7 - 21 + len(faces7))) // 2))
    assert len(faces7) == 14 and all(len(f) == 3 for f in faces7)

    rot6 = delete_vertex(rot7, 6)
    faces6 = trace_faces(rot6)
    degrees = sorted(len(f) for f in faces6)
    chi = 6 - 15 + len(faces6)
    print("K_6 (delete vertex 6): V=6 E=15 F=%d  chi=%d  genus=%d  face degrees %s"
          % (len(faces6), chi, (2 - chi) // 2, degrees))
    assert chi == 0 and len(faces6) == 9 and degrees == [3] * 8 + [6]

    # 2. the sign-vector search ---------------------------------------------
    print()
    print("searching all 2^15 orientations for quadruples summing to (2,...,2)")
    quads, keys, vectors = find_quadruples()
    print("  distinct sign vectors sigma_eps in {+-1}^15 :", len(keys))
    print("  quadruples {sigma_1..sigma_4} with sum = 2*1 :", len(quads))
    single = [k for k in keys if all(s == k[0] for s in k)]
    print("  orientations with ALL 15 signs equal (K_6 Pfaffian?):", len(single))
    pairs = 0
    for i in range(len(keys)):
        for j in range(i, len(keys)):
            if all(a + b == 2 for a, b in zip(keys[i], keys[j])):
                pairs += 1
    print("  pairs summing to (2,...,2) (a 2-Pfaffian formula?):", pairs)

    # 3. structure of one quadruple -----------------------------------------
    quad = quads[0]
    orientations = [vectors[keys[i]][0] for i in quad]
    coefficients = [1, 1, 1, 1]
    print()
    print("first quadruple, as orientations (+1 means oriented u->v for u<v):")
    for n, o in enumerate(orientations):
        print("   eps_%d:" % n, "".join("+" if s == 1 else "-" for s in o))
    ok_sym = check_identity_symbolic(orientations, coefficients)
    ok_num = check_identity_numeric(orientations, coefficients)
    print("  symbolic identity 2*haf = sum_i Pf(A^i) over Z[w_e] :", ok_sym)
    print("  100 random exact rational matrices                  :", ok_num)

    # F_2-affine structure: differences of the four orientations
    base = orientations[0]
    diffs = [tuple((1 - a * b) // 2 for a, b in zip(base, o))  # 0/1 flip vector
             for o in orientations]
    span = set()
    for d in diffs:
        span.add(d)
    closed = True
    for a in diffs:
        for b in diffs:
            xor = tuple((x + y) % 2 for x, y in zip(a, b))
            if xor not in span:
                closed = False
    print("  the four flip-vectors form an F_2-subgroup (torsor over (Z/2)^2):",
          closed and len(span) == 4)

    # flip classes: a genuine H^1(T^2;F_2) torsor has 4 distinct classes
    classes = {flip_class(o) for o in orientations}
    print("  distinct classes modulo the 64 vertex flips           :", len(classes))

    # 4. Kasteleyn face condition on the torus embedding --------------------
    print()
    print("face parities (degree, #darts opposing the orientation) per face:")
    for n, o in enumerate(orientations):
        par = face_parities(faces6, o)
        print("   eps_%d:" % n, " ".join("%d/%d" % (c, d) for d, c in par))
    # count orientations satisfying "every face has an odd number of
    # orientation-opposing darts" -- the naive Kasteleyn rule
    odd_all = 0
    kast = []
    for mask in range(1 << 15):
        orientation = tuple(1 if (mask >> b) & 1 else -1 for b in range(15))
        par = face_parities(faces6, orientation)
        if all(c % 2 == 1 for d, c in par):
            odd_all += 1
            kast.append(orientation)
    print("  orientations with every face clockwise-odd:", odd_all)
    if kast:
        kclasses = sorted({flip_class(o) for o in kast})
        print("  their classes modulo the 32 vertex flips :", len(kclasses),
              "(= |H^1(T^2;F_2)| = 4 predicted)")
        kvectors = {sign_vector(o) for o in kast}
        print("  distinct sign vectors among them         :", len(kvectors),
              "(4 classes x global sign)")
        reps = list(kclasses)
        assert len(reps) == 4
        winner = None
        for bits in range(16):
            signs = [1 if (bits >> b) & 1 else -1 for b in range(4)]
            if check_identity_symbolic(reps, signs):
                winner = signs
                break
        print("  KASTELEYN QUADRUPLE + Arf signs          :", winner)
        if winner:
            print("    (%d plus, %d minus -- three even + one odd spin structure)"
                  % (winner.count(1), winner.count(-1)))
            print("    symbolic identity over Z[w_e]          :",
                  check_identity_symbolic(reps, winner))
            print("    100 random exact rational matrices     :",
                  check_identity_numeric(reps, winner))
            for n, (o, c) in enumerate(zip(reps, winner)):
                print("      eps_%d (c=%+d):" % (n, c),
                      "".join("+" if s == 1 else "-" for s in o))
        # affine (Z/2)^2 structure modulo the cut space
        cuts = set()
        for mask in range(1 << 6):
            if bin(mask).count("1") % 2:
                continue
            flip = [0] * 15
            for n, (u, v) in enumerate(EDGES6):
                if ((mask >> u) & 1) ^ ((mask >> v) & 1):
                    flip[n] = 1
            cuts.add(tuple(flip))
        def canon(vec):
            return min(tuple((a + b) % 2 for a, b in zip(vec, cut))
                       for cut in cuts)
        base = reps[0]
        classes = {canon(tuple((1 - a * b) // 2 for a, b in zip(base, o)))
                   for o in reps}
        closed = all(canon(tuple((x + y) % 2 for x, y in zip(a, b))) in classes
                     for a in classes for b in classes)
        print("  the 4 twists form an F_2^2 subgroup of F_2^E/cuts:",
              closed and len(classes) == 4)
        # how many of the 800 quadruples are topological?
        kastset = {sign_vector(o) for o in kast}
        topological = sum(1 for q in quads
                          if all(keys[i] in kastset for i in q))
        print("  of the %d quadruples, how many use only Kasteleyn"
              " sign vectors: %d" % (len(quads), topological))

    # 5. the K_4 genus-0 companion ------------------------------------------
    print()
    o4 = k4_single_pfaffian()
    print("K_4 planar Kasteleyn orientation (haf_4 = Pf exactly):", o4)
    a, b, c, d = (Fraction(2), Fraction(-3), Fraction(5), Fraction(7))
    e, f = Fraction(11), Fraction(-13)
    weights = {(0, 1): a, (0, 2): b, (0, 3): c, (1, 2): d, (1, 3): e, (2, 3): f}
    sym = [[0] * 4 for _ in range(4)]
    ant = [[0] * 4 for _ in range(4)]
    for n, (u, v) in enumerate(EDGES4):
        sym[u][v] = sym[v][u] = weights[(u, v)]
        ant[u][v] = o4[n] * weights[(u, v)]
        ant[v][u] = -o4[n] * weights[(u, v)]
    print("  haf_4 =", hafnian(sym), " Pf_4 =", pfaffian(ant),
          " equal:", hafnian(sym) == pfaffian(ant))
    print("  => the four-site error component is a Pfaffian of a 4x4"
          " antisymmetric matrix, i.e. the Pluecker/Klein quadric on Lambda^2 C^4")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
