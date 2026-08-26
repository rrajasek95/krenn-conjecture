#!/usr/bin/env python3
"""W25 -- INDEPENDENT exact decision of "does the pair (p,q) carry a witness?"

WITNESS at (p,q): an admissible cap K (s != 0 and K_00 K_11 K_22 != 0) with
E_pq(K) = 0 in every component.  Decided by Rabinowitsch saturation in Singular.

INDEPENDENCE FROM W23: the symbolic E is built from the W22-M CLOSED FORM
    E_w = Haf_U(sA+R)_w - s^{h-1} sum_ij K_ij H_B(A)_{w[p->i, q->j]},
whereas W23 builds it from the subset-sum-over-J expansion.  Agreement is both
an inter-probe control and a check of W22-M.

LEDGER 22: denominators are cleared before emission (sound: every term of
E_pq has total degree 2h in the blocks).
LEDGER 13: no generator is ever named after a ring variable (guard runs on
every emitted script).
LEDGER 19: every verdict is re-decided modulo at least two primes, chosen
p = 1 mod 3 (so cube roots of unity exist) and p = 1 mod 4.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x3core-w25-2026-08-15")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import w25_core as C                                            # noqa: E402

KVARS = tuple(f"zk{i}{j}" for i in range(3) for j in range(3))
# p = 1 mod 3 (cube roots of unity present) and p = 1 mod 4 (i present)
PRIMES = (1000003, 1000033, 32003)


def _sym_K():
    import sympy
    return [[sympy.Symbol(KVARS[3 * i + j]) for j in range(3)]
            for i in range(3)]


def _elt(x):
    """Source entry -> sympy expression (integers, or Z[omega] via zw)."""
    import sympy
    if C.is_om(x):
        assert x.a.denominator == 1 and x.b.denominator == 1, x
        return sympy.Integer(x.a.numerator) + sympy.Symbol("zw") * sympy.Integer(x.b.numerator)
    f = Fraction(x)
    assert f.denominator == 1, f"clear denominators first: {x}"
    return sympy.Integer(f.numerator)


def sym_cap_error(src, p, q, sites, ncol=C.NCOL):
    """E_pq(K) as sympy polynomials in the nine cap variables (W22-M form)."""
    import sympy
    sites = tuple(sorted(sites))
    n = C.sites_of(src)
    h = len(sites) // 2
    K = _sym_K()
    apq = C.oriented(src, p, q, ncol)
    s = sympy.expand(sum(K[i][j] * _elt(apq[i][j])
                         for i in range(ncol) for j in range(ncol)))
    R = {}
    for a, b in combinations(sites, 2):
        apa, aqa = C.oriented(src, p, a, ncol), C.oriented(src, q, a, ncol)
        apb, aqb = C.oriented(src, p, b, ncol), C.oriented(src, q, b, ncol)
        R[(a, b)] = [[sympy.expand(sum(
            K[i][j] * (_elt(apa[i][ca]) * _elt(aqb[j][cb])
                       + _elt(aqa[j][ca]) * _elt(apb[i][cb]))
            for i in range(ncol) for j in range(ncol)))
            for cb in range(ncol)] for ca in range(ncol)]

    def ent(tab, a, b, ca, cb):
        return tab[(a, b)][ca][cb] if a < b else tab[(b, a)][cb][ca]

    A = {(a, b): C.oriented(src, a, b, ncol) for a, b in combinations(sites, 2)}
    slot = {a: i for i, a in enumerate(sites)}
    mask = 0
    for a in sites:
        mask |= 1 << a
    eqs = []
    for word in product(range(ncol), repeat=len(sites)):
        wd = {a: word[slot[a]] for a in sites}

        def wt(i, j, wd=wd):
            return sympy.expand(s * _elt(ent(A, i, j, wd[i], wd[j]))
                                + ent(R, i, j, wd[i], wd[j]))

        first = C.haf_mask(wt, mask, {}, sympy.Integer(1), sympy.Integer(0))
        kc = sympy.Integer(0)
        for i in range(ncol):
            for j in range(ncol):
                full = dict(wd)
                full[p] = i
                full[q] = j
                fw = tuple(full[t] for t in range(n))
                hv = C.H(src, fw, n, ncol)
                if hv == 0:
                    continue
                kc = kc + K[i][j] * _elt(hv)
        tot = sympy.expand(first - (s ** (h - 1)) * kc)
        if tot != 0:
            eqs.append(tot)
    return eqs, s, [K[c][c] for c in range(ncol)]


def _sing(expr):
    import sympy
    e = sympy.expand(expr)
    txt = str(e).replace("**", "^").replace(" ", "")
    assert "/" not in txt, f"rational coefficient reached Singular: {txt[:80]}"
    return txt


def decide_pair(src, p, q, sites, tag, ncol=C.NCOL, timeout=3600,
                primes=PRIMES, omega=False):
    """('WITNESS'|'BLOCKED', dim over Q, {prime: dim}).

    omega=True puts the computation in Q(zw), zw^2+zw+1 = 0 (needed when the
    source itself has Z[omega] entries; harmless otherwise, but Singular
    forbids parameters in positive characteristic rings with minpoly, so the
    mod-p re-decision then adds zw as a variable with its minimal polynomial)."""
    isrc, _ = C.clear_denominators(src, ncol)
    if any(C.is_om(x) for m in isrc.values() for row in m for x in row):
        omega = True
    eqs, s, kap = sym_cap_error(isrc, p, q, sites, ncol)
    gens = [_sing(e) for e in eqs]
    nz = "(" + _sing(s) + ")*(" + ")*(".join(_sing(k) for k in kap) + ")"
    out = {}
    verdict, dimQ = None, None
    for char in (0,) + tuple(primes):
        if omega:
            if char == 0:
                head = [f'ring zzR=(0,zw),({",".join(KVARS)},zzt),dp;',
                        "minpoly=zw^2+zw+1;"]
                extra = ""
            else:
                head = [f'ring zzR={char},({",".join(KVARS)},zzt,zw),dp;']
                extra = ",zw^2+zw+1"
        else:
            head = [f'ring zzR={char},({",".join(KVARS)},zzt),dp;']
            extra = ""
        lines = head + [
            "ideal zzI=" + (",".join(gens) if gens else "0") + extra + ";",
            f"ideal zzJ=zzI,zzt*({nz})-1;",
            f'"DEC {tag} {char} "+string(dim(std(zzJ)));']
        script = "\n".join(lines)
        C.no_shadow_guard(script, set(KVARS) | {"zzt", "zw"})
        txt = C.run_singular(script, timeout=timeout)
        line = [ln for ln in txt.splitlines()
                if ln.startswith(f"DEC {tag} {char} ")]
        assert line, txt
        d = int(line[0].split()[-1])
        if char == 0:
            dimQ = d
            verdict = "BLOCKED" if d == -1 else "WITNESS"
        else:
            out[char] = d
    return verdict, dimQ, out


def cheap_witness(src, p, q, sites, ncol=C.NCOL, caps=None):
    """Sufficient (never necessary) test: try a fixed library of caps exactly.
    Returns the first K with E = 0 and K admissible, else None."""
    if caps is None:
        caps = cap_library()
    for K in caps:
        if not C.is_admissible(src, p, q, K, ncol):
            continue
        if not C.cap_error(src, p, q, K, sites, ncol):
            return K
    return None


def cap_library():
    """A small exact library: identity, antisymmetric caps I + E_ab - E_ba
    (W23-U2's cap), diagonal caps, and omega-twisted diagonal caps."""
    import itertools
    out = []
    I = [[Fraction(int(i == j)) for j in range(3)] for i in range(3)]
    out.append(I)
    for a, b in itertools.permutations(range(3), 2):
        K = [row[:] for row in I]
        K[a][b] += Fraction(1)
        K[b][a] -= Fraction(1)
        out.append(K)
    for d in itertools.product([Fraction(1), Fraction(-1), Fraction(2)],
                              repeat=3):
        out.append([[d[i] if i == j else Fraction(0) for j in range(3)]
                    for i in range(3)])
    w = C.OMEGA
    w2 = w * w
    for diag in ([C.Om(1), w, w2], [C.Om(1), w2, w], [C.Om(1), C.Om(1), w],
                 [C.Om(1), w, C.Om(1)]):
        out.append([[diag[i] if i == j else C.Om(0) for j in range(3)]
                    for i in range(3)])
    for a, b in itertools.permutations(range(3), 2):
        K = [[C.Om(int(i == j)) for j in range(3)] for i in range(3)]
        K[a][b] = K[a][b] + w
        K[b][a] = K[b][a] - w
        out.append(K)
    return out
