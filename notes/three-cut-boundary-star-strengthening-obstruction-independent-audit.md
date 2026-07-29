# Independent audit: boundary-star strengthening obstruction

## 1. Verdict

The two one-star obstructions in
[the primary note](three-cut-boundary-star-strengthening-obstruction.md)
pass an independent exact reconstruction.

For either \(q=6\) or \(q=7\), all \(63=7\cdot3^2\) final aggregate
cell coefficients on the \(q\)-star may be chosen arbitrarily in
\(\mathbb C\).  With every block not incident to \(q\) fixed as stated:

1. none of the cuts \(z=0,1,5\) can satisfy the complete quotient
   identity, and their star-independent defect dimensions are exactly
   \((3,3,1)\);
2. on the site-\(7\) star, completeness of cut \(z=3\) is incompatible
   with \(h_{w_0}=h_{w_1}=0\);
3. on the site-\(6\) star, completeness of cut \(z=2\) is incompatible
   with \(h_{w_0}=h_{w_1}=0\); and
4. if \(h_{w_0}\) is allowed to return, cancelling the repaired
   \(67\)-cell kills \(w_1,w_2,w_3\) while preserving complete cuts
   \(2,3,4\) and defects \((1,1,2)\).

These are polynomial identities in arbitrary aggregate star cells, not a
finite scan.  Since their coefficients were reconstructed over
\(\mathbb Q\), they hold after scalar extension to \(\mathbb C\).

One route-consequence sentence in the primary note was too strong and has
been narrowed during this audit.  A complete fourth cut must evade the
one-star obstruction and attain \(h_{00000000}=1\), but it need not make
the all-zero internal coordinate enter the insertion space:
\(\epsilon_{0,z}\) may remain in \(K_{U_z}\).  This correction does not
alter either obstruction theorem.

The standalone checker is
[verify_three_cut_boundary_star_strengthening_obstruction_independent_audit.py](../computations/verify_three_cut_boundary_star_strengthening_obstruction_independent_audit.py).
It imports no code from the primary checker.

## 2. Endpoint-ordered reconstruction

For \(u<v\), an aggregate cell \(E_{ab}^{uv}\) assigns colour \(a\) at
site \(u\) and colour \(b\) at site \(v\).  I reconstructed the repaired
blocks as

\[
\begin{array}{c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}\\
02&E_{11}&14&E_{11}\\
36&E_{11}&57&E_{11}\\
04&E_{22}&13&E_{22}\\
27&E_{22}&56&E_{22}\\
25&E_{00}&35&E_{10}\\
23&E_{21}&67&-E_{12}.
\end{array}
\]

In particular, \(35=E_{10}\) is not symmetrized.  Direct enumeration of
all \(105\) perfect matchings gives

\[
 H_{\mathrm{base}}
   =e_1^{\otimes8}+e_2^{\otimes8}+e_{00210012},
\]

and, after the two repair cells,

\[
 H_{\mathrm{repaired}}
   =e_1^{\otimes8}+e_2^{\otimes8}
    -e_{12120012}-e_{11111012}-e_{22022012}.
\]

Thus, with

\[
\begin{aligned}
w_0&=00210012,&w_1&=12120012,\\
w_2&=11111012,&w_3&=22022012,
\end{aligned}
\]

the claimed values \(h_{w_0}=0\) and
\(h_{w_1}=h_{w_2}=h_{w_3}=-1\) are exact.

Freeing a \(q\)-star replaces its seven incident blocks by seven arbitrary
\(3\times3\) endpoint-ordered matrices.  Every perfect matching contains
exactly one \(q\)-incident edge.  Consequently every full-word coefficient
is a linear form in precisely these final star cells.  The independent
checker constructs all \(63\) formal variables and enumerates those linear
forms; it never specializes them to a bounded set of values.  Any such
matrix family is realized by at most one decorated source for every
nonzero cell, while arbitrary parallel sources give the same aggregate
coefficient by multilinearity.

## 3. Fourth-cut obstruction and exact defects

For \(z\in\{0,1,5\}\), put

\[
 U_z=\{0,1,2,3,4,5\}\setminus\{z\}.
\]

The insertion space \(\mathcal S_{U_z}\) uses only edges internal to the
six-set \(\{0,\ldots,5\}\), so it is unchanged by either star
specialization.  At the all-zero coordinate, the only compatible internal
edges are \(01,45,25\).  On \(U_0\) or \(U_1\), only \(45,25\) remain and
they meet at site \(5\); on \(U_5\), only \(01\) remains.  No four-site
cofactor can therefore contribute at the all-zero word.  Hence

\[
 \epsilon_{0,z}:=[0^5]^*\in K_{U_z}
 \qquad(z=0,1,5).
\]

The exact constant-word defects can also be read off before any star is
chosen.  On \(U_0\) and \(U_1\), each of the all-zero, all-one, and
all-two coordinates annihilates the insertion space, giving defect \(3\).
On \(U_5\), the all-zero coordinate is absent, while

\[
 02\cup14
 \quad\text{and}\quad
 04\cup13
\]

give pure-one and pure-two four-site cofactors, respectively.  Thus the
defect is \(1\).  Exact sparse rank reduction independently confirms
\((3,3,1)\).

It remains to inspect the full all-zero coefficient.  A matching has one
edge incident to the freed center \(q\).  If that edge does not meet the
other boundary site, the other boundary site must use one of its fixed
nonstar blocks, all of which have nonzero colour there.  If the star edge
is \(67\), the remaining six sites would need an all-zero perfect matching,
but \(01,45,25\) contain none.  The formal linear form is therefore

\[
                         h_{00000000}=0
\]

for all \(63\) complex star cells.  The complete quotient identity,
contracted by \(\epsilon_{0,z}\) in the \(000\) complement row, instead
forces \(h_{00000000}=1\).  This proves the three impossibilities without
assuming that cuts \(2,3,4\) stay complete.

## 4. Site-\(7\) cumulative identity

For the free site-\(7\) star, write

\[
 x=A_{27}[22],\qquad y=A_{67}[12].
\]

Compatible fixed completions give the exact symbolic forms

\[
 h_{22222222}=x,\qquad
 h_{w_0}=x+y,\qquad
 h_{w_1}=y.
\]

The first uses \(04,13,56\); the two \(w_0\) completions are

\[
 01,27,36,45
 \quad\text{and}\quad
 01,23,45,67,
\]

and the sole \(w_1\) completion is \(02,13,45,67\).  Every other one of
the \(63\) star cells has coefficient zero in these three forms.  Hence

\[
            h_{22222222}-h_{w_0}+h_{w_1}=0.             \tag{1}
\]

On \(U_3=(0,1,2,4,5)\), the all-two coordinate annihilates every
insertion generator: \(04\) is the only compatible internal edge, so no
four-site cofactor can be all two.  Its target contraction is \(e_2\).
Completeness of cut \(z=3\) therefore forces

\[
                         h_{22222222}=1.                 \tag{2}
\]

Equations (1)--(2) rule out \(h_{w_0}=h_{w_1}=0\).

## 5. Site-\(6\) cumulative identity

For the free site-\(6\) star, set

\[
 p=A_{36}[11],\qquad r=A_{46}[01],\qquad y=A_{67}[12],
\]

and \(v=12120111\).  Exact matching enumeration gives

\[
\begin{aligned}
h_{11111111}&=p,&h_v&=r,\\
h_{w_0}&=p+r+y,&h_{w_1}&=y.
\end{aligned}
\]

Thus

\[
 h_{11111111}+h_v-h_{w_0}+h_{w_1}=0.                   \tag{3}
\]

In the order \(U_2=(0,1,3,4,5)\), define

\[
 \beta_6=[11111]^*+[12201]^*.
\]

At the first coordinate, \(14\) is the only compatible internal edge; at
the second, \(13\) is the only one.  Both coordinate functionals
separately annihilate every four-site cofactor insertion.  Moreover
\(\delta_{U_2}(\beta_6)=e_1\).  In complement row \(111\), the selected
full words are exactly \(11111111\) and \(v\), so a complete cut \(z=2\)
forces

\[
                         h_{11111111}+h_v=1.             \tag{4}
\]

Equations (3)--(4) again exclude \(h_{w_0}=h_{w_1}=0\).

## 6. Literal three-word undo and scope

Appending \(+E_{12}^{67}\) cancels the repaired
\(-E_{12}^{67}\) aggregate cell.  The \(23=E_{21}\) block remains
internally visible, but the full matching expansion is exactly

\[
 H_B=e_1^{\otimes8}+e_2^{\otimes8}+e_{w_0}.
\]

Thus \(w_1,w_2,w_3\) vanish while \(h_{w_0}=1\).  Independent exact
row-space tests of

\[
 H_B-\Delta_{8,3}\in
 V_{(z,6,7)}\otimes\mathcal S_{U_z}
\]

give complete cuts \(z=2,3,4\), and direct constant-word rank differences
give defects \((1,1,2)\).  This confirms that only cumulative vanishing,
including \(w_0\), has the asserted obstruction.

The result is deliberately fixed-background.  It says nothing about an
arbitrary decorated graph after internal blocks are changed, and a
simultaneous two-star modification lies outside either \(63\)-parameter
family.  It is not a Krenn counterexample or a global four-cut theorem.
