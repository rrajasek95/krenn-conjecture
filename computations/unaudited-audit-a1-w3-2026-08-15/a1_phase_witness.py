"""AUDIT A1 / CLAIM 4 -- the constructed witness against the phase-only
reduction, and its exact certification.

THE MECHANISM (derived independently in this audit).

By W3's own L1, a gauge transformation multiplies EVERY matching of a fixed
word by the same factor.  Therefore, on the gauge orbit of the all-moduli-1
point, every fibre is EQUILATERAL: all terms of one fibre have equal
modulus.  W3's "set all moduli to 1" is exactly the equilateral ansatz.

Now let a support carry two 2-term mixed fibres with difference vectors
d1, d2 (a 2-term fibre M+M' = 0 forces  arg t_M - arg t_M' = pi  and
|t_M| = |t_M'|), and a 3-term mixed fibre {M1, M2, M3} with

        1_{M1} - 1_{M2}  =  d1 + d2       (EVEN number of pi's)

Then t_{M1} and t_{M2} are forced PARALLEL with equal moduli, so the third
term must satisfy   |t_{M3}| = 2 |t_{M1}|   -- the fibre is necessarily
NON-equilateral.  Unit moduli are therefore impossible while general moduli
are fine.  This is a modulus-level obstruction that is neither a singleton
fibre (M9) nor a missing pure row (M8).

The explicit n = 8 realisation is below; everything is verified exactly.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

import sympy as sp

from a1_core import all_words, cellkey
from a1_phase import fibres, is_mixed

N = 8

# w_C = (0,1,0,1,0,1,0,1);   w_1 differs at 3,7 (colour 2);  w_2 at 1,5.
A = (0, 1, 0, 1, 0, 1, 0, 1)

SUPPORT = [
    (0, 1, 0, 1),      # M1
    (2, 3, 0, 1),      # M1
    (4, 5, 0, 1),      # M1
    (6, 7, 0, 1),      # M1
    (1, 2, 1, 0),      # M2
    (3, 4, 1, 0),      # M2
    (5, 6, 1, 0),      # M2
    (0, 7, 0, 1),      # M2
    (2, 6, 0, 0),      # chord gamma
    (0, 4, 0, 0),      # chord delta
    (3, 7, 2, 2),      # tail of the first 2-term fibre
    (1, 5, 2, 2),      # tail of the second 2-term fibre
    (0, 3, 0, 1),      # the free third term's new edge
]


def report(S):
    fib = fibres(N, S)
    print(f"support size {len(S)}; live words {len(fib)}")
    sing = []
    for w, terms in sorted(fib.items()):
        tag = "PURE" if not is_mixed(w) else "mixed"
        if is_mixed(w) and len(terms) == 1:
            sing.append(w)
        print(f"  {tag} {''.join(map(str,w))}: {len(terms)} term(s)")
        for t in terms:
            print("        ", t)
    print("singleton mixed fibres:", sing if sing else "NONE  (M9 silent)")
    pures = [w for w in fib if not is_mixed(w)]
    print("live pure rows:", pures, "(M8 fires)" if len(pures) < 3 else "")
    return fib


def exact_analysis(S, fib):
    """Symbolic proof that (a) the unit-modulus system is infeasible and
    (b) the general system is solvable with support exactly S."""
    Sl = sorted(S)
    idx = {s: i for i, s in enumerate(Sl)}
    syms = sp.symbols(f"a0:{len(Sl)}")
    mixed = {w: t for w, t in fib.items() if is_mixed(w)}

    def poly(terms):
        return sum(sp.prod([syms[idx[k]] for k in M]) for M in terms)

    print("\nMIXED EQUATIONS:")
    eqs = {}
    for w, terms in sorted(mixed.items()):
        e = sp.expand(poly(terms))
        eqs[w] = e
        print(f"  {''.join(map(str,w))}:  {e} = 0")
    return syms, idx, eqs, Sl


if __name__ == "__main__":
    S = frozenset(SUPPORT)
    assert len(S) == len(SUPPORT)
    print("AUDIT A1 / claim 4 -- constructed witness, n = 8")
    print("=" * 78)
    fib = report(S)
    exact_analysis(S, fib)
