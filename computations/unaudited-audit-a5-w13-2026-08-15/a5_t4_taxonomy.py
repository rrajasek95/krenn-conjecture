#!/usr/bin/env python3
"""A5 / claim 4: THEOREM W13.4' taxonomy, re-verified on MY battery.

For every A in the battery and every h, decide exactly (over Q, or over Q(i)
by realification for Gaussian-integer A) which of the C(h+3,3) L-monomials
s^a kappa_0^{b0} kappa_1^{b1} kappa_2^{b2} lie in L_h(A).

Reported against the claimed taxonomy:
  T1  a <= h-2, single colour                -> IN
  T2  two or more distinct kappa colours     -> OUT (hypothesis: A has no
                                                zero row and no zero column)
  T3  a = h                                  -> IN iff det A = 0 (h >= 3)
  T4  a = h-1, single colour                 -> conditional
"""
from __future__ import annotations
import json, random, sys
from fractions import Fraction
from itertools import product
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def rank3(M):
    return len(A.int_echelon([list(r) for r in M])[1])


def has_zero_line(M):
    return (any(all(x == 0 for x in row) for row in M)
            or any(all(M[i][j] == 0 for i in range(3)) for j in range(3)))


def _re(x):
    v = Fraction(x.real) if hasattr(x, "real") else Fraction(x)
    assert v.denominator == 1
    return int(v)


def _im(x):
    v = Fraction(x.imag) if hasattr(x, "imag") else Fraction(0)
    assert v.denominator == 1
    return int(v)


def realify_rows(rows):
    """Complex (Gaussian) rows -> real rows of double length, plus i*row.
    span_{Q(i)}(rows) realified = span_Q({re-im of row, re-im of i*row})."""
    out = []
    for r in rows:
        out.append([_re(x) for x in r] + [_im(x) for x in r])
        out.append([-_im(x) for x in r] + [_re(x) for x in r])
    return out


class GaussInt:
    __slots__ = ("real", "imag")

    def __init__(self, re, im=0):
        self.real, self.imag = Fraction(re), Fraction(im)

    def __add__(self, o):
        o = o if isinstance(o, GaussInt) else GaussInt(o)
        return GaussInt(self.real + o.real, self.imag + o.imag)
    __radd__ = __add__

    def __mul__(self, o):
        o = o if isinstance(o, GaussInt) else GaussInt(o)
        return GaussInt(self.real * o.real - self.imag * o.imag,
                        self.real * o.imag + self.imag * o.real)
    __rmul__ = __mul__

    def __sub__(self, o):
        o = o if isinstance(o, GaussInt) else GaussInt(o)
        return GaussInt(self.real - o.real, self.imag - o.imag)

    def __neg__(self):
        return GaussInt(-self.real, -self.imag)

    def __eq__(self, o):
        if isinstance(o, GaussInt):
            return self.real == o.real and self.imag == o.imag
        return self.imag == 0 and self.real == o

    def __bool__(self):
        return bool(self.real) or bool(self.imag)

    def __repr__(self):
        return f"({self.real}+{self.imag}i)"


def monomial_vec(h, svec, a, bs):
    f = A.ppow(A.var_poly(svec), a)
    for c, m in enumerate(bs):
        for _ in range(m):
            e = [0] * 9
            e[3 * c + c] = 1
            f = A.pmul(f, {tuple(e): 1})
    return A.poly_vec(f, h)


def analyse(Amat, h, rng, complexA=False):
    svec = [Amat[i][j] for i in range(3) for j in range(3)]
    rows = A.L_rows(h, svec, rng)
    if complexA:
        rows = realify_rows(rows)
    ech, piv = A.int_echelon(rows)
    out = {}
    for a in range(h + 1):
        for bs in product(range(h + 1), repeat=3):
            if a + sum(bs) != h:
                continue
            v = monomial_vec(h, svec, a, bs)
            if complexA:
                v = [_re(x) for x in v] + [_im(x) for x in v]
            out[(a,) + bs] = A.in_span_exact(ech, piv, v)
    return out, (len(piv) // 2 if complexA else len(piv))


def classify(h, key):
    a, b0, b1, b2 = key
    ncol = sum(1 for b in (b0, b1, b2) if b)
    if ncol >= 2:
        return "T2 multi-colour"
    if a == h:
        return "T3 s^h"
    if a <= h - 2:
        return "T1 monochrome a<=h-2"
    return "T4 a=h-1 monochrome"


def main():
    rng = random.Random(2718)
    battery = []
    for i in range(4):
        M = [[rng.randint(-5, 5) for _ in range(3)] for _ in range(3)]
        battery.append((f"random{i}", M, False))
    battery += [
        ("identity", [[1, 0, 0], [0, 1, 0], [0, 0, 1]], False),
        ("diag(1,2,3)", [[1, 0, 0], [0, 2, 0], [0, 0, 3]], False),
        ("all-ones J", [[1, 1, 1], [1, 1, 1], [1, 1, 1]], False),
        ("rank1 uv^T nonzero", [[u * v for v in (1, 2, 3)] for u in (1, -2, 5)], False),
        ("rank2 no zero line", [[1, 2, 3], [4, 5, 6], [5, 7, 9]], False),
        ("repeated rows", [[1, 2, 3], [1, 2, 3], [4, 5, 6]], False),
        ("entries sum to zero", [[1, 2, -3], [4, -5, 1], [-5, 3, 2]], False),
        ("2x2 minor zero", [[1, 2, 5], [2, 4, 1], [7, 3, 2]], False),
        ("J - 3I", [[-2, 1, 1], [1, -2, 1], [1, 1, -2]], False),
        ("circulant", [[1, 2, 3], [3, 1, 2], [2, 3, 1]], False),
        ("perm matrix", [[0, 1, 0], [0, 0, 1], [1, 0, 0]], False),
        ("one zero entry", [[0, 1, 1], [1, 1, 1], [1, 1, 1]], False),
        ("ZERO ROW (excluded)", [[0, 0, 0], [1, 2, 3], [4, 5, 6]], False),
        ("ZERO COL (excluded)", [[1, 0, 3], [4, 0, 6], [7, 0, 9]], False),
        ("single cell E22 (excluded)", [[0, 0, 0], [0, 0, 0], [0, 0, 1]], False),
        ("single cell 5*E22 (excluded)", [[0, 0, 0], [0, 0, 0], [0, 0, 5]], False),
        ("zero matrix (excluded)", [[0] * 3 for _ in range(3)], False),
        ("complex generic", [[GaussInt(rng.randint(-3, 3), rng.randint(-3, 3))
                              for _ in range(3)] for _ in range(3)], True),
        ("complex rank1", [[GaussInt(1, 1) * GaussInt(u) * GaussInt(v)
                            for v in (1, 2, 3)] for u in (1, 2, 1)], True),
        ("complex det=0 (i-circulant)",
         [[GaussInt(1), GaussInt(0, 1), GaussInt(-1)],
          [GaussInt(0, 1), GaussInt(-1), GaussInt(0, -1)],
          [GaussInt(-1), GaussInt(0, -1), GaussInt(1)]], True),
    ]
    results = []
    for h in (2, 3, 4):
        for name, M, cpx in battery:
            table, dimL = analyse(M, h, rng, complexA=cpx)
            d = det3(M)
            zl = has_zero_line(M)
            rk = None if cpx else rank3(M)
            viol = []
            for key, inside in table.items():
                cls = classify(h, key)
                if cls == "T2 multi-colour" and inside:
                    viol.append(("T2 violated (multi-colour IS in L_h)", key))
                if cls == "T1 monochrome a<=h-2" and not inside:
                    viol.append(("T1 violated (monochrome NOT in L_h)", key))
                if cls == "T3 s^h" and h >= 3:
                    want = (d == 0)
                    if inside != want:
                        viol.append((f"T3 violated (in={inside}, det==0 is {want})", key))
            t4 = {str(k): v for k, v in table.items() if classify(h, k) == "T4 a=h-1 monochrome"}
            rec = {"h": h, "A": name, "det": str(d), "rank": rk, "zero_line": zl,
                   "dimL": dimL, "violations": [f"{a} {b}" for a, b in viol],
                   "T4_table": t4,
                   "n_in": sum(1 for v in table.values() if v),
                   "n_monomials": len(table)}
            results.append(rec)
            flag = "  <-- VIOLATION" if viol and not zl else ("  (excluded A)" if viol else "")
            print(f"h={h} A={name:30s} det={str(d):>12s} zeroline={zl!s:5s} dimL={dimL:4d} "
                  f"in={rec['n_in']:3d}/{rec['n_monomials']:3d} viol={len(viol)}{flag}",
                  flush=True)
            for a_, b_ in viol:
                print(f"      {a_} at {b_}", flush=True)
    json.dump(results, open(OUT + "results_t4_taxonomy.json", "w"), indent=1)


if __name__ == "__main__":
    main()
