#!/usr/bin/env python3
"""W21-M2-GEO step 7: the CHARACTERISTIC-ZERO elimination that closes the
L-free word x = (1,1,2,2).

For x = (1,1,2,2) the four transversal labels are (0,1),(1,1),(2,2),(3,2) and
the DEAD CELLS forbid the following coincidences (proportional rows must have
the same zero pattern, and each block has at most one dead cell):

   site 4 : (2,2) is row 2 of A_{2,4}, whose dead cell (2,1) sits in it, so
            it has a zero in column 1; the only other dead row at site 4 is
            row 0 of A_{1,4} with its zero in column 0  ==>  VERTEX 2 ISOLATED
   site 5 : (1,1) has a zero in column 1, (3,2) has a zero in column 2, and
            no other row at site 5 has a zero  ==>  VERTICES 1 AND 3 ISOLATED
   site 6 : (0,1) has a zero in column 0; the only partner would be (2,0),
            which is not on this transversal  ==>  VERTEX 0 ISOLATED
   site 7 : (3,2) has a zero in column 1, no partner  ==>  VERTEX 3 ISOLATED

Lemma B kills three hyperplanes; Lemma C-strong kills two (it would need a
site with ALL FOUR points coincident); Lemma D kills one (worked out by hand
in the report).  The remaining case is dim V_j = 2 for all four j, and THAT is
what this script decides exactly over Q by Groebner elimination.

Normalisation: at each site take the two rows that are provably independent
(the isolated vertex and one other) to (1,0), (0,1) via the GL_2 gauge; then
use the 3-dimensional residual torus to set a2 = a4 = c2 = 1.
"""
from __future__ import annotations

import os
import subprocess
import sys
from itertools import permutations, product

import sympy as sp

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
P4 = list(permutations(range(4)))

a1, a2, a3, a4 = sp.symbols('a1 a2 a3 a4')
b1, b2, b3, b4 = sp.symbols('b1 b2 b3 b4')
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4')
d1, d2, d3, d4 = sp.symbols('d1 d2 d3 d4')

# M_j: rows indexed by the L-site 0..3, two columns.
M4 = [[0, 1], [a1, a2], [1, 0], [a3, a4]]      # rows 2,0 normalised
M5 = [[b1, b2], [1, 0], [b3, b4], [0, 1]]      # rows 1,3 normalised
M6 = [[1, 0], [0, 1], [c1, c2], [c3, c4]]      # rows 0,1 normalised
M7 = [[0, 1], [d1, d2], [d3, d4], [1, 0]]      # rows 3,0 normalised
Ms = [M4, M5, M6, M7]


def col(M, k):
    return [M[i][k] for i in range(4)]


def per4(cols):
    return sp.expand(sum(sp.prod([cols[j][p[j]] for j in range(4)])
                         for p in P4))


EQS = []
for choice in product((0, 1), repeat=4):
    EQS.append(per4([col(Ms[j], choice[j]) for j in range(4)]))

# the residual torus normalisation
SUB = {a2: 1, a4: 1, c2: 1}
EQS = [sp.expand(e.subs(SUB)) for e in EQS]
VARS = [a1, a3, b1, b2, b3, b4, c1, c3, c4, d1, d2, d3, d4]

# the minors that MUST be nonzero (isolated vertices)
NONZERO = [b1, b2, b3, b4, d2, d4, c4]
# a2, a4, c2 were normalised to 1 (they are among the required-nonzero minors)


def main():
    lines = []
    lines.append("ring R = 0, (%s, T), dp;" % ",".join(str(v) for v in VARS))
    prod_nz = "*".join(str(v) for v in NONZERO)
    ideal_terms = [str(e) for e in EQS] + ["T*(%s)-1" % prod_nz]
    lines.append("ideal I = %s;" % ",\n  ".join(ideal_terms))
    lines.append('option(redSB);')
    lines.append("ideal G = std(I);")
    lines.append('printf("dim = %s", dim(G));')
    lines.append('printf("G[1] = %s", G[1]);')
    lines.append('printf("size = %s", size(G));')
    lines.append('if (size(G)==1 and G[1]==1) '
                 '{ printf("VERDICT: EMPTY -- no solution over C"); } '
                 'else { printf("VERDICT: NONEMPTY or inconclusive"); }')
    lines.append("quit;")
    src = "\n".join(lines)
    path = os.path.join(HERE, "elim_x1122.sing")
    open(path, "w").write(src)
    print("wrote %s (%d equations, %d vars + T)"
          % (path, len(EQS), len(VARS)))
    print("running Singular ...", flush=True)
    out = subprocess.run(["Singular", "-q", path], capture_output=True,
                         text=True, timeout=100000)
    print(out.stdout[-4000:])
    print(out.stderr[-2000:])
    open(os.path.join(HERE, "log_elim_x1122.txt"), "w").write(
        out.stdout + "\n---\n" + out.stderr)


if __name__ == "__main__":
    main()
