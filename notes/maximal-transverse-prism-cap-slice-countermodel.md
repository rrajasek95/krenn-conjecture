# A maximal transverse cap slice retaining the exact prism root cover

## 1. Outcome

The four-parameter common-edge prism barrier extends much farther than its
original presentation suggests, but not to the whole cap space.

There is an exact ten-site aggregate edge family with four capped sites

\[
W=\{p,q,r,s\}
\]

and six boundary sites

\[
U=\{x_0,x_1,x_2,y_0,y_1,y_2\}
\]

having the following properties.

1. Its full cap space has dimension \(3^4=81\), and its complete top cap map
   has rank nine.
2. The unique maximal linear subspace on which the top image lies in
   \(\operatorname {span}\{X_0,X_1,X_2\}\) has codimension six and dimension
   \(75\).  The restricted image is exactly that three-dimensional span.
3. The unique maximal subspace on which the literal global-GHZ cap formula

   \[
   K\mathbin{\lrcorner}H_{10}(A)
      =\sum_{i=0}^2K(e_i^{\otimes W})X_i                 \tag{1}
   \]

   holds has codimension eight and dimension \(73\).
4. On both subspaces the actual common-edge cofactor map has image exactly
   the full four-parameter triangular-prism family.  Its mixed discrepancy
   ideal is

   \[
   I_{\mathcal D}=(z_0z_1z_2),
   \qquad h=sz_0z_1z_2\in I_{\mathcal D},               \tag{2}
   \]

   so the active saturation is the unit ideal.
5. A dense, top-inactive \(pq\) block makes the universal cap-adjugate
   identity detect all six off-diagonal rows omitted by the codimension-six
   slice, with nonzero coefficients.

Thus common-edge realizability plus the exact top GHZ formula on a very
large cap subspace does not force a clean cap or proper saturation.  Any
positive theorem must use caps outside the codimension-eight subspace.  This
is not a global Krenn counterexample: on the full cap space the top image has
rank nine, not three.

The exact audit is
[verify_maximal_transverse_prism_cap_slice.py](../computations/verify_maximal_transverse_prism_cap_slice.py).

## 2. The dense-direct ten-site source

Start with the two canonical ternary four-site modules on

\[
\{p,x_0,x_1,x_2\},\qquad \{q,y_0,y_1,y_2\}.
\]

Thus \(px_i\) and \(qy_i\) have the cell \(e_i e_i\), and the triangle edge
opposite \(x_i\), respectively \(y_i\), has the same cell.  Inside \(W\), put

\[
A_{pq}=a=
\begin{pmatrix}
1&2&3\\
4&5&7\\
8&11&13
\end{pmatrix},qquad
A_{rs}=e_0e_0,qquad
A_{pr}=e_1e_1,qquad
A_{qs}=e_2e_2.                                         \tag{3}
\]

All other entries vanish.  The dense block \(a\) belongs to no supported
ten-site matching: after using \(pq\), the two three-vertex shores cannot be
matched internally.  Every supported top matching instead uses \(rs\), one
edge \(px_i\), one edge \(qy_j\), and the two opposite triangle edges.  Put

\[
E_{ij}=e_i^{\otimes\{x_0,x_1,x_2\}}
       e_j^{\otimes\{y_0,y_1,y_2\}},qquad X_i=E_{ii}.
\]

Exact matching enumeration gives

\[
H_{10}(A)=\sum_{i,j=0}^2
 e_i^{(p)}e_j^{(q)}e_0^{(r)}e_0^{(s)}E_{ij}.            \tag{4}
\]

For a cap \(K\in(\bigotimes_{w\in W}V_w)^*\), write

\[
c_{ij}=K(i,j,0,0),qquad \kappa_i=K(i,i,i,i).
\]

The complete top cap map is therefore

\[
\tau(K)=K\mathbin{\lrcorner}H_{10}(A)
       =\sum_{i,j=0}^2c_{ij}E_{ij}.                     \tag{5}
\]

The nine \(c_{ij}\) are independent cap coordinates, so

\[
\operatorname {rank}\tau=9.                            \tag{6}
\]

In particular, merely enlarging the original four-parameter cap
prescription cannot turn this unchanged source into a full diagonal cap map.
A physical common-edge repair is necessary.

## 3. The two maximal cap slices

Define

\[
L_{\rm img}=\{K:c_{ij}=0\text{ for every }i\ne j\}.     \tag{7}
\]

The six equations in (7) are independent.  Equation (5) shows both that

\[
\dim L_{\rm img}=75,qquad
\tau(L_{\rm img})=\operatorname {span}\{X_0,X_1,X_2\}, \tag{8}
\]

and that every cap subspace whose top image is diagonal is contained in
\(L_{\rm img}\).  Hence (7) is the unique maximal such subspace.

The literal target formula (1) imposes two more equations:

\[
c_{11}=\kappa_1,qquad c_{22}=\kappa_2.                 \tag{9}
\]

For colour zero the analogous equality is automatic, since both sides are
the coordinate \(K(0,0,0,0)\).  The eight equations (7), (9) are independent.
Consequently

\[
L_{\rm GHZ}=\ker(\tau-\gamma),qquad
\gamma(K)=\sum_i\kappa_iX_i,qquad
\dim L_{\rm GHZ}=73.                                   \tag{10}
\]

Again maximality is exact: any linear subspace on which (1) holds is
contained in the kernel (10).

The original four-parameter cap slice embeds in \(L_{\rm GHZ}\).  Set

\[
c_{ii}=z_i,\quad c_{ij}=0\ (i\ne j),\quad
K(1,1,1,1)=z_1,\quad K(2,2,2,2)=z_2,\quad
K(1,2,1,2)=t,                                          \tag{11}
\]

and let every other unspecified coordinate vanish.  The zero-colour
identification is already contained in \(c_{00}=K(0,0,0,0)=z_0\).

## 4. The complete cofactor map on the maximal slices

There are ten supported internal \(W\)-words.  The matching \(pq\mid rs\)
gives

\[
(i,j,0,0)\longmapsto a_{ij},qquad 0\le i,j\le2,
\]

and \(pr\mid qs\) gives

\[
(1,2,1,2)\longmapsto1.
\]

Therefore the scalar cofactor is

\[
s(K)=K\mathbin{\lrcorner}H_W(A)
    =\sum_{i,j}a_{ij}c_{ij}+K(1,2,1,2).                 \tag{12}
\]

Exact enumeration of every tensor \(H_{W\cup\{u,v\}}(A)\) gives only the
following boundary blocks:

* each of the six shore-triangle edges is its canonical rank-one cell
  multiplied by \(s(K)\);
* the cross-shore block \(x_i y_j\) is
  \(c_{ij}e_i e_j\);
* every other block is zero.

On \(L_{\rm img}\), put \(z_i=c_{ii}\).  The off-diagonal cross blocks vanish,
so the actual cofactor family is exactly the triangular prism

\[
D(s,z_0,z_1,z_2).
\]

Moreover

\[
s=z_0+5z_1+13z_2+K(1,2,1,2).                           \tag{13}
\]

Thus \(s,z_0,z_1,z_2\) are independent on both \(L_{\rm img}\) and
\(L_{\rm GHZ}\), and every member of the four-parameter prism family occurs.
The large ambient dimension should not be mistaken for a large effective
cofactor image: on \(L_{\rm GHZ}\), the combined top-and-cofactor map has
rank four and a \(69\)-dimensional common kernel.  Those kernel directions
are cap coordinates absent from every supported tensor used here.
Its six-site hafnian is

\[
H_6(D)=s^2\sum_{i=0}^2z_iX_i
       +z_0z_1z_2E_{012012}.                            \tag{14}
\]

Because \(\tau(K)=\sum_i z_iX_i\) on \(L_{\rm img}\), the actual cofactor
discrepancy is

\[
\mathcal D(K)=6\bigl(s(K)^2\tau(K)-H_6(D)\bigr)
              =-6z_0z_1z_2E_{012012}.                  \tag{15}
\]

Equations (2) follow immediately.  In particular, the root cover persists
on all \(75\) cap dimensions, not merely on a chosen four-plane.  On the
smaller \(L_{\rm GHZ}\), one also has \(z_i=\kappa_i\), so (15) is exactly the
large-target cap discrepancy.

## 5. The six transverse rows are adjugate-visible

Delete \(r,s\) from the edge table and retain the induced eight-site core on

\[
\{p,q,x_0,x_1,x_2,y_0,y_1,y_2\}.
\]

The dense block \(a\) is still top-inactive, and the top tensor of this core
is \(\sum_{i,j}e_i^{(p)}e_j^{(q)}E_{ij}\).  Its cofactor matrix is

\[
(\operatorname {Cof}_{ij}(a))=
\begin{pmatrix}
-12&4&4\\
7&-11&5\\
-1&5&-3
\end{pmatrix};                                         \tag{16}
\]

all nine entries are nonzero.  If \(B_{ij}\) denotes the common-edge
six-boundary family obtained by the matrix-unit cap at \(p,q\), the universal
cap-adjugate identity gives

\[
\det(B_{ij})=2\sum_{i,j=0}^2
 \operatorname {Cof}_{ij}(a)E_{ij}.                    \tag{17}
\]

Replacing the top tensor formally by an eight-site GHZ tensor would replace
the right side by only its three diagonal terms.  The discrepancy is

\[
2\sum_{i\ne j}\operatorname {Cof}_{ij}(a)E_{ij},       \tag{18}
\]

with exactly six nonzero rows.  These are precisely the six quotient
coordinates \(c_{ij}\), \(i\ne j\), omitted in (7).  Thus the codimension-six
gap is not invisible to common-edge algebra: the alternating determinant
detects every one of its rows.  What the prism slice demonstrates is that no
equation restricted to \(L_{\rm img}\) can use them, because all six cap
coordinates vanish there.

The remaining two quotient rows in \(L_{\rm img}/L_{\rm GHZ}\) are the
diagonal relocations

\[
K(1,1,0,0)-K(1,1,1,1),qquad
K(2,2,0,0)-K(2,2,2,2).                                 \tag{19}
\]

They involve the additional sites \(r,s\) and are not present in the
eight-site core (17).

## 6. Exact scope and next gate

This construction proves the following negative statement:

> There is no implication from common-edge realizability plus the exact
> global-GHZ cap formula on a high-dimensional proper cap subspace to proper
> cofactor saturation.  The implication already fails on a maximal
> codimension-eight subspace of an \(81\)-dimensional cap space.

It does **not** construct a ten-site global GHZ source, and it does not prove
that arbitrary modifications of the edge table cannot repair (4).  The full
top map still has the nine-dimensional image (6).  Because the added
dimensions inside \(L_{\rm GHZ}\) are a common kernel, the construction
specifically rules out arguments based on ambient codimension or on the
number of imposed cap equations.  It does not rule out a theorem requiring
many transverse caps that alter the effective lower cofactor family.

The concrete remaining extension problem is consequently finite and sharp.
A genuine repair must simultaneously

1. cancel the six off-diagonal rows in (18) while changing the common lower
   cap determinant required by (17); and
2. move the two diagonal rows in (19) from \(r=s=0\) to the globally pure
   \(r=s=i\) coordinates.

Those eight transverse equations, compared across overlapping physical-pair
adjugate identities, are information genuinely absent from the entire
maximal prism slice.
