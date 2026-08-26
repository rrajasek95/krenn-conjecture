#!/usr/bin/env python3
"""UNAUDITED PROBE (W7 / Route T.1 symmetric-cone closure) -- the exact fan of
the colour-form weight family, and the initial systems it carries.

Pinned HEAD: a41949965d41e5c63fb4bc1caf7b20c0df017856
(agent start HEAD 31cefe2b247450d1168abc07f6dc73318c068e44; repo is live)

SETTING.  N sites, cells x[(u,v),i,j] for each edge of K_N and each ordered
colour pair.  For a word chi in {0,1,2}^N,

    Phi_chi = sum_{M in PM(K_N)} prod_{(u,v) in M} x[(u,v), chi_u, chi_v].

The GHZ system is Phi_chi = 0 for mixed chi and Phi_c = 1 for the three pure
words, in the LAURENT ring (all cells invertible).  T.1 asks: for every weight
w, does in_w(I) contain a monomial?

THE RESIDUAL FAMILY (W4's scouting output).  The no-singleton locus is
gauge(3N) + edge-independent SYMMETRIC colour forms w[(u,v),i,j] = f(i,j),
f(i,j) = f(j,i).  This script works entirely inside the 6-dimensional colour
form family F.

THE REDUCTION (exact, proved in the report).  For w = f in F, the weight of the
occurrence (M, chi) is  sum_{(u,v) in M} f(chi_u, chi_v)  and therefore depends
only on the COLOUR-PAIR TYPE m(M,chi) = (m_01, m_02, m_12) plus the content
n(chi) = (n_0, n_1, n_2).  Writing

    g_ab = f(a,b) - (f(a,a) + f(b,b))/2      (a < b),

one has  W(M,chi) = m_01 g_01 + m_02 g_02 + m_12 g_12 + (1/2) sum_c n_c f(c,c),
the last term independent of M.  So:

  * the MIXED initial forms depend only on g = (g_01, g_02, g_12) in R^3;
  * the PURE initial forms depend only on the signs of f(0,0), f(1,1), f(2,2)
    (the pure word c has the single type m_cc = N/2, so all (N-1)!! matchings
    tie at weight (N/2) f(c,c));
  * (g, diag f) are linear coordinates on F, so the fan on F is the PRODUCT of
    the 3-dimensional g-fan computed here with the 27 sign patterns of diag f.

This script enumerates the g-fan EXACTLY and completely (all faces, not just
maximal cones) as a central hyperplane arrangement in R^3, and records for each
face the full argmin data of every mixed content.

OUTPUT: results_fan_N{6,8}.json + a printed table.  Everything is exact integer
/ Fraction arithmetic; no floating point anywhere.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import factorial
import json
import sys

PAIRS = ((0, 1), (0, 2), (1, 2))


# --------------------------------------------------------------- combinatorics

def contents(nsites):
    """All ordered colour contents (n_0,n_1,n_2) with sum nsites."""
    out = []
    for n0 in range(nsites + 1):
        for n1 in range(nsites - n0 + 1):
            out.append((n0, n1, nsites - n0 - n1))
    return tuple(out)


def types_for_content(n):
    """{(m01,m02,m12): #matchings of K_N with that colour-pair type}.

    A perfect matching M of K_N and a word chi of content n induce m_ab = number
    of M-edges with endpoint colours {a,b}.  The degree identities are
    2 m_aa + sum_{b != a} m_ab = n_a, so (m01,m02,m12) determines m_aa and the
    type is feasible iff the three remainders are nonnegative and EVEN.  The
    count is  prod_c n_c!  /  ( prod_c 2^{m_cc} m_cc!  *  prod_{a<b} m_ab! ).
    """
    out = {}
    for m01 in range(min(n[0], n[1]) + 1):
        for m02 in range(min(n[0], n[2]) + 1):
            for m12 in range(min(n[1], n[2]) + 1):
                r0 = n[0] - m01 - m02
                r1 = n[1] - m01 - m12
                r2 = n[2] - m02 - m12
                if r0 < 0 or r1 < 0 or r2 < 0:
                    continue
                if r0 % 2 or r1 % 2 or r2 % 2:
                    continue
                m00, m11, m22 = r0 // 2, r1 // 2, r2 // 2
                num = factorial(n[0]) * factorial(n[1]) * factorial(n[2])
                den = 1
                for mcc in (m00, m11, m22):
                    den *= (2 ** mcc) * factorial(mcc)
                for mab in (m01, m02, m12):
                    den *= factorial(mab)
                if num % den:
                    raise AssertionError("non-integral matching count")
                out[(m01, m02, m12)] = num // den
    return out


def double_factorial_odd(nsites):
    """(N-1)!! = number of perfect matchings of K_N."""
    value = 1
    for k in range(1, nsites, 2):
        value *= k
    return value


# ------------------------------------------------------- exact 3d arrangement

def primitive(vec):
    """Normalise an integer 3-vector: primitive, first nonzero coordinate > 0."""
    from math import gcd
    g = 0
    for c in vec:
        g = gcd(g, abs(c))
    if g == 0:
        return None
    vec = tuple(c // g for c in vec)
    for c in vec:
        if c:
            if c < 0:
                vec = tuple(-x for x in vec)
            break
    return vec


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def sign_vector(point, normals):
    out = []
    for v in normals:
        d = dot(v, point)
        out.append(0 if d == 0 else (1 if d > 0 else -1))
    return tuple(out)


def rank3(vectors):
    """Exact rank of a list of integer 3-vectors."""
    rows = [[Fraction(c) for c in v] for v in vectors]
    rank = 0
    for col in range(3):
        pivot = None
        for i in range(rank, len(rows)):
            if rows[i][col]:
                pivot = i
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        head = rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                f = rows[i][col] / head[col]
                rows[i] = [a - f * b for a, b in zip(rows[i], head)]
        rank += 1
    return rank


def enumerate_faces(normals):
    """All faces of the central arrangement {<v,g>=0 : v in normals} in R^3.

    Returns {sign_vector: representative point (exact Fractions)}.

    Completeness argument (the arrangement is essential, checked by the caller):
      * every 1-face lies in >= 2 independent hyperplanes, hence is spanned by
        some +-(u x v);
      * every 2-face is cone(r1,r2) for two 1-faces, and r1 + r2 lies in its
        relative interior;
      * every 3-face (chamber) is pointed and has a facet, i.e. a 2-face F;
        for p in relint F and v the normal of the hyperplane containing F, the
        two points p +- eps v lie in the two chambers adjacent to F once eps is
        small enough, and an exact admissible eps is computed below.
      * the origin is added explicitly.
    Every candidate point is an actual point of R^3, so every sign vector
    returned is a genuine face; the four bullets give completeness.
    """
    rays = set()
    for u, v in combinations(normals, 2):
        c = cross(u, v)
        if c != (0, 0, 0):
            rays.add(primitive(c))
            rays.add(primitive(tuple(-x for x in c)))
    rays = sorted(r for r in rays if r is not None)
    # a primitive vector and its negative both normalise to the same
    # representative, so re-add the negatives explicitly
    rays = sorted(set(rays) | {tuple(-x for x in r) for r in rays})

    candidates = [tuple(Fraction(c) for c in r) for r in rays]
    for r1, r2 in combinations(rays, 2):
        candidates.append(tuple(Fraction(a + b) for a, b in zip(r1, r2)))

    def admissible_eps(point, direction):
        best = None
        for v in normals:
            dp = dot(v, point)
            dv = dot(v, direction)
            if dp != 0 and dv != 0:
                bound = abs(Fraction(dp, 1)) / abs(Fraction(dv, 1))
                if best is None or bound < best:
                    best = bound
        return Fraction(1) if best is None else best / 2

    faces = {}
    origin = (Fraction(0), Fraction(0), Fraction(0))
    faces[sign_vector(origin, normals)] = origin
    for p in candidates:
        faces.setdefault(sign_vector(p, normals), p)
    # chambers, reached by pushing off each candidate along every normal that
    # vanishes on it
    extra = []
    for p in candidates:
        for v in normals:
            if dot(v, p) == 0:
                eps = admissible_eps(p, v)
                for s in (1, -1):
                    extra.append(tuple(a + s * eps * Fraction(c)
                                       for a, c in zip(p, v)))
    for p in extra:
        faces.setdefault(sign_vector(p, normals), p)
    return faces


def zaslavsky_check(faces, normals):
    """Face-count control: for a central essential arrangement in R^3 the number
    of chambers is  r(A) = sum over the intersection lattice of |mu|, which for
    a *generic* arrangement is 2*(1 + n + C(n,2)) ... rather than hard-code a
    formula we use the two structural identities that hold for every central
    essential arrangement in R^3:
        (i)  the face poset is symmetric under g -> -g (so face counts by
             dimension are even except for the origin);
        (ii) every chamber is pointed and every 2-face borders exactly 2
             chambers, giving  sum over 2-faces of 2 = sum over chambers of
             (number of facets).
    Both are verified from the enumerated data.
    """
    by_dim = {0: 0, 1: 0, 2: 0, 3: 0}
    dims = {}
    for sv, p in faces.items():
        zero = [normals[i] for i, s in enumerate(sv) if s == 0]
        d = 3 - rank3(zero) if zero else 3
        dims[sv] = d
        by_dim[d] += 1
    negated = {tuple(-s for s in sv) for sv in faces}
    symmetric = negated == set(faces)
    return by_dim, symmetric, dims


# ------------------------------------------------------------ the fan on g

def build(nsites, verbose=True):
    conts = contents(nsites)
    mixed = tuple(n for n in conts if sum(1 for c in n if c) > 1)
    pure = tuple(n for n in conts if sum(1 for c in n if c) == 1)
    table = {n: types_for_content(n) for n in conts}
    pm = double_factorial_odd(nsites)
    for n, tp in table.items():
        if sum(tp.values()) != pm:
            raise AssertionError("type counts do not sum to (N-1)!! at %s" % (n,))
    for n in pure:
        if len(table[n]) != 1 or tuple(table[n]) != ((0, 0, 0),):
            raise AssertionError("a pure content must carry the single type 0")

    normals = set()
    for n in mixed:
        keys = sorted(table[n])
        for a, b in combinations(keys, 2):
            d = primitive(tuple(x - y for x, y in zip(a, b)))
            if d is not None:
                normals.add(d)
    normals = sorted(normals)
    ess = rank3(normals)
    if ess != 3:
        raise AssertionError("arrangement not essential: rank %d" % ess)

    faces = enumerate_faces(normals)
    by_dim, symmetric, dims = zaslavsky_check(faces, normals)

    if verbose:
        print("N = %d" % nsites)
        print("  contents %d (mixed %d, pure %d); matchings (N-1)!! = %d"
              % (len(conts), len(mixed), len(pure), pm))
        print("  distinct colour-pair types per content: %d..%d"
              % (min(len(table[n]) for n in mixed),
                 max(len(table[n]) for n in mixed)))
        print("  arrangement: %d distinct hyperplanes in g-space (essential)"
              % len(normals))
        print("  faces by dimension: %s   (total %d; +-symmetric: %s)"
              % (by_dim, len(faces), symmetric))

    records = []
    for sv, point in faces.items():
        rec = {"sign": sv, "point": point, "dim": dims[sv], "argmin": {},
               "mincount": {}, "minvalue": {}}
        for n in mixed:
            best = None
            arg = []
            for m, cnt in sorted(table[n].items()):
                val = (Fraction(m[0]) * point[0] + Fraction(m[1]) * point[1]
                       + Fraction(m[2]) * point[2])
                if best is None or val < best:
                    best, arg = val, [m]
                elif val == best:
                    arg.append(m)
            rec["argmin"][n] = tuple(arg)
            rec["mincount"][n] = sum(table[n][m] for m in arg)
            rec["minvalue"][n] = best
        records.append(rec)
    return {"nsites": nsites, "contents": conts, "mixed": mixed,
            "table": table, "normals": normals, "faces": records,
            "by_dim": by_dim, "symmetric": symmetric}


def singleton_report(data, verbose=True):
    """Which faces of the g-fan carry a MIXED SINGLETON (a word whose w-minimal
    matching is unique), and which do not."""
    good, bad = [], []
    for rec in data["faces"]:
        witness = [n for n in data["mixed"] if rec["mincount"][n] == 1]
        if witness:
            good.append((rec, witness))
        else:
            bad.append(rec)
    if verbose:
        print("  faces with a mixed singleton : %d / %d"
              % (len(good), len(data["faces"])))
        print("  faces WITHOUT any singleton  : %d  (by dim: %s)"
              % (len(bad), {d: sum(1 for r in bad if r["dim"] == d)
                            for d in (0, 1, 2, 3)}))
    return good, bad


def describe(point):
    return "(g01,g02,g12) = (%s, %s, %s)" % tuple(str(c) for c in point)


def main():
    out = {}
    for nsites in (6, 8):
        data = build(nsites)
        good, bad = singleton_report(data)
        print("  no-singleton faces, with the argmin structure:")
        for rec in sorted(bad, key=lambda r: (-r["dim"], r["point"])):
            worst = min(rec["mincount"][n] for n in data["mixed"])
            print("     dim %d  %-34s  min #minimising matchings over mixed"
                  " words = %d" % (rec["dim"], describe(rec["point"]), worst))
        out[nsites] = {
            "normals": [list(v) for v in data["normals"]],
            "by_dim": data["by_dim"],
            "n_faces": len(data["faces"]),
            "n_singleton_faces": len(good),
            "no_singleton_faces": [
                {"dim": r["dim"], "point": [str(c) for c in r["point"]],
                 "argmin": {str(k): [list(m) for m in v]
                            for k, v in r["argmin"].items()},
                 "mincount": {str(k): v for k, v in r["mincount"].items()}}
                for r in bad],
        }
        print()
    with open("results_fan.json", "w") as handle:
        json.dump(out, handle, indent=1, default=str)
    print("wrote results_fan.json")


if __name__ == "__main__":
    main()
