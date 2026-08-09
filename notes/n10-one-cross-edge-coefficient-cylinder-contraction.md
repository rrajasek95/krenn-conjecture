# One cross edge does not obstruct the matched-pair cylinder contraction

## Outcome

The pure-anchor-preserving matched-pair contraction extends exactly across
one arbitrary cross edge.  Add one source joining vertex 8 or 9 to any old
vertex, in any endpoint colours and with any complex weight.  On every old
three-site cut, its cofactor contribution contracts either to zero or to an
already existing N=8 insertion column.

Therefore the contracted coefficient cylinder never grows modulo the N=8
cylinder.  Four simultaneous complete cut conditions at N=10 would descend
to the same four complete cut conditions at N=8.  Since the anchored N=8
source has only the three complete cuts \(z=2,3,4\), no one-cross-edge lift
can create a fourth.

No surviving cross-edge countermodel was found because there is an exact
one-cross-edge theorem.  A genuine failure of this induction mechanism needs
at least two cross edges.

## 1. Parity removes the cross edge from the full tensor

Retain the isolated diagonal pair

\[
                 g_{89}=E_{89;00}+E_{89;11}+E_{89;22}
\]

and add

\[
                         tE_{8v;\alpha\beta}              \tag{1}
\]

for an old vertex \(v\); the case with new endpoint 9 is symmetric.  If a
full ten-site perfect matching used (1), vertex 9 could no longer use edge
89 and would have no incident edge left.  Hence (1) occurs in no full
matching:

\[
                 H_{10}(t)=H_8\otimes g
                 \quad\text{for every }t.                \tag{2}
\]

In particular, the full residual is independent of \(t\).  This is the first
reason that testing a coefficient grid would be unnecessary.

## 2. The only possible cofactor contribution

Fix a cut \(C_z=\{z,6,7\}\) and let

\[
 U_8=\{0,\ldots,5\}\setminus\{z\},\qquad
 U_{10}=U_8\cup\{8,9\}.
\]

There are three cases.

1. If \(v\in C_z\), the cross edge is absent from every cofactor matching on
   \(U_{10}\).
2. If the hole is 8, vertex 9 is isolated, so the column is zero.
3. If \(v\in U_8\), the cross edge can occur only when the hole is 9.  It
   pairs 8 with \(v\), and the other four old shore vertices carry the
   ordinary cofactor \(H_{U_8\setminus\{v\}}\).

In the third case choose \(v\) itself as the controller in the contraction
from the preceding note.  Let \(h\) be the inserted colour at hole 9.  The
controlled diagonal contraction requires simultaneously

\[
                         h=\beta=\alpha.                 \tag{3}
\]

If (3) fails, the contracted cross column is zero.  If (3) holds, it is
literally

\[
 e_\alpha^{(v)}\otimes H_{U_8\setminus\{v\}}
             =c^{(8)}_{v,\alpha},                        \tag{4}
\]

one of the existing labelled N=8 insertion columns.  The same argument with
8 and 9 exchanged handles a cross edge incident to vertex 9.

Thus, for every old source family and every cut,

\[
            P_v\bigl({\cal S}^{(10)}_z(t)\bigr)
                       \subseteq {\cal S}^{(8)}_z
            \qquad(t\in\mathbb C).                       \tag{5}
\]

When \(v\) is on the boundary, any old shore vertex may be used as controller
because the cross contribution is already zero.

## 3. Descent of the cylinder condition

The controlled contraction still satisfies

\[
       P(H_{10}(t)-\Delta_{10,3})=H_8-\Delta_{8,3}.        \tag{6}
\]

If the N=10 residual rows belonged to the N=10 cofactor cylinder on a cut,
(5)--(6) would put every contracted N=8 residual row in the old cylinder.
Complete high-sector membership therefore descends cut by cut.

The lower one-crossing sector is the literal insertion factorization at both
orders, so no source-provenance condition is lost.  This remains a
finite-realizability argument and does not factor through the output tensor
or its border closure.

For nonzero \(t\), the new cofactor space is independent of the magnitude of
\(t\):

\[
        {\cal S}^{(10)}_z(t)
        ={\cal S}^{(10)}_z(0)+
          \operatorname{span}\{\text{cross directions}\}. \tag{7}
\]

Thus one exact nonzero representative is exhaustive.  The checker also uses
\(t=2\) to verify the affine identity coefficient by coefficient; it is not
a second grid sample.

## 4. Exact coordinate census

There are

\[
             2\cdot8\cdot3\cdot3=144
\]

endpoint-colour coordinates.  Swapping vertices 8 and 9 reduces these to 72
classes, and the checker verifies both representatives of every class.
Across all six cuts there are 864 coordinate-cut cases:

| contracted cross direction | cases |
|---|---:|
| exactly an old insertion column | 180 |
| zero because endpoint colours mismatch | 360 |
| zero because the old endpoint is on the boundary, or the relevant cofactor vanishes | 324 |
| outside the old N=8 cylinder | **0** |

As an independent direct audit, the checker reconstructs the actual N=10
cofactor spaces at weights 1 and 2.  None of the 864 coordinate-cut cases has
complete residual membership.  More importantly, (2), (5), and (7) make the
contraction conclusion exact for every complex weight.

## 5. The new sharp frontier

One cross edge cannot appear in a full matching and cannot enlarge a
contracted cylinder.  With two cross edges, both new vertices can instead
match to old vertices.  Then:

* the full tensor acquires a quadratic cross term;
* both new-hole families can be nonzero; and
* their contracted images need not be individual old insertion columns.

That two-cross-edge interaction is now the first possible obstruction to the
N to N+2 contraction.  The next bounded test should classify unordered pairs
of cross coordinates by their old endpoints and endpoint colours, separating
shared-old-endpoint pairs from disjoint pairs before doing any coefficient
search.

## Reproduction

    python3 computations/verify_n10_one_cross_edge_coefficient_cylinder_contraction.py
    python3 -O computations/verify_n10_one_cross_edge_coefficient_cylinder_contraction.py
    python3 -I computations/verify_n10_one_cross_edge_coefficient_cylinder_contraction.py
    python3 -S computations/verify_n10_one_cross_edge_coefficient_cylinder_contraction.py

The checker uses exact rational arithmetic and literal perfect-matching
expansions throughout.
