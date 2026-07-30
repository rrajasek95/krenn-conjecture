# Full-nine selector families have an exact small-matrix provenance class

## 1. Outcome

Fix one full-nine deleted-pair chart at \(h=3\), on the residual six-site
set \(W\).  Let \(I\) be the retained endpoint-label set, and let

\[
 d=(d_{ij})_{i,j\in I},
 \qquad
 d_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,             \tag{1}
\]

where the pure target tensors
\(X_i=\bigotimes_{x\in W}e_i^{(x)}\) are linearly independent.  Pair
matrices entrywise and put

\[
 E=\operatorname {Mat}_{I\times I},\qquad
 \Lambda=d^\perp,
 \qquad
 \Phi(\ell)=\sum_{i,j}\ell_{ij}p_i s_j.                  \tag{2}
\]

The fixed-chart **selector family** is

\[
                         C_{\rm sel}=\Phi(\Lambda).       \tag{3}
\]

It is important that (3) is a family, rather than one selected cap.  On
this whole family, (1) gives the literal top map

\[
 M_q\Phi(\ell)=D(\ell):=\sum_i\ell_{ii}X_i,
 \qquad M_q(b)=bq^{[2]}.                                  \tag{4}
\]

Let \(\lambda\in C_{\rm sel}^*\) be a desired physical coefficient,
curvature, or dark-cut functional.  Extend it linearly to the ambient
quadratic space and form its response matrix

\[
                         F_{ij}=\lambda(p_i s_j).          \tag{5}
\]

Different extensions change \(F\) only by a multiple of \(d\).  The exact
family-level source criterion is

\[
 \boxed{
 \begin{aligned}
 &\text{one top functional }\nu\text{ satisfies}
   \ \lambda(\Phi(\ell))=\nu(D(\ell))\quad(\ell\in\Lambda)\\
 &\hspace{35mm}\Longleftrightarrow\quad
 F\in \Delta+\mathbb C d,
 \qquad
 \Delta=\operatorname {span}\{E_{ii}:i\in I\}.
 \end{aligned}}                                           \tag{6}
\]

This remains exact when \(\Phi\) is noninjective.  If

\[
                         K=\ker(\Phi|_\Lambda),            \tag{7}
\]

then (4) implies \(D(K)=0\), and the literal selector-family provenance
module is

\[
 \boxed{
 {\mathfrak P}_{\rm sel}(d,\Phi)
    ={K^\perp\over \Delta+\mathbb C d}.}                  \tag{8}
\]

Here \(K^\perp\) is taken inside the matrix space using the entrywise
pairing.  Thus noninjectivity restricts which response tables descend to
functionals on \(C_{\rm sel}\); it does not alter the test (6) for one
that does descend.

On a completed \(2\times2\) missing square, (6) is especially small.  If

\[
 d=\begin{pmatrix}a&b\\c&e\end{pmatrix},\qquad
 F=\begin{pmatrix}f_{11}&f_{12}\\f_{21}&f_{22}\end{pmatrix},
\]

then

\[
 \boxed{
 F\in\Delta+\mathbb C d
 \quad\Longleftrightarrow\quad
 (f_{12},f_{21})\in\mathbb C(b,c).}                       \tag{9}
\]

When \((b,c)\ne(0,0)\), this is the single scalar equation

\[
                         \omega_d(F):=cf_{12}-bf_{21}=0.  \tag{10}
\]

When \(b=c=0\), both off-diagonal entries of \(F\) must vanish.  Hence the
generic missing-square obstruction is one-dimensional; it is not another
support census.

The oriented-curvature relocation theorem does not force (10).  At a
decorated residual edge, write

\[
 B=H^\rightarrow+H^\leftarrow,
 \qquad
 K^\rightarrow=ud-H^\rightarrow,
 \qquad
 K^\leftarrow=ud-H^\leftarrow.                            \tag{11}
\]

The physical edge-coefficient functional has response table \(F=B\), and

\[
 B=2ud-(K^\rightarrow+K^\leftarrow).                      \tag{12}
\]

Thus it is top-realizable on the whole selector family exactly when

\[
 K^\rightarrow+K^\leftarrow\in\Delta+\mathbb C d.        \tag{13}
\]

Relocation proves that some rank-one selector detects one of the two
curvatures.  It does not prove the family identity (13).  Two diagonal
anchors supply precisely \(\Delta\), already present in (6).  The first
Bianchi crossed pairing controls the difference

\[
 J=H^\rightarrow-H^\leftarrow,
 \qquad
 K^\rightarrow-K^\leftarrow+J=0,                         \tag{14}
\]

not the sum in (12).  Even if a literal filtered-overlap argument grants
\(J\) as a source-valid family row, the exact enhanced criterion is only

\[
                         F\in\Delta+\mathbb C d+\mathbb C J. \tag{15}
\]

For a generic \(2\times2\) square, one crossed row spans the ambient
one-dimensional provenance quotient if and only if

\[
                              \omega_d(J)\ne0.             \tag{16}
\]

The Bianchi identity alone does not imply (16).  Section 5 gives a minimal
guard in which \(d\) is invertible, both assignment matrices have rank at
most one, both anchors are present, (14) holds, and even the crossed row is
granted as source-valid, but (15) fails.

This result has deliberately limited scope.  It distinguishes three
different objects.

1. \(C_{\rm sel}=\Phi(d^\perp)\) varies the contraction matrix inside one
   fixed full-nine chart.  Equations (6)--(16) concern this family only.
2. The physical binary cap line used by the rootless/Macaulay argument
   varies the clean coordinates and has cubic coordinate forms
   \(e_\omega(u,v)\).  It additionally requires one common degree-five
   functional for the three prolongations \(u^2,uv,v^2\).  A vanishing
   class in (8) supplies neither that varying-line compatibility nor the
   degree-two prolongation.
3. For one fixed \(\beta\) with \(M_q\beta\ne0\), one can always tune a
   top functional to reproduce one scalar \(\lambda(\beta)\).  That is the
   single-cap tautology and proves neither (6) nor a Macaulay annihilator.

Accordingly, (6) is the literal full-nine specialization of the filtered
source-provenance obstruction, not a completion of the conjecture.

## 2. Proof of the criterion, including a noninjective \(\Phi\)

Let \(T=\operatorname {span}\{X_i:i\in I\}\).  If
\(k\in K\), then \(\Phi(k)=0\), and (4) gives \(D(k)=0\).  Therefore there
is a well-defined map

\[
                         \overline D:C_{\rm sel}\to T,
 \qquad \overline D\Phi=D.                                \tag{17}
\]

A top realization of \(\lambda\) is exactly a factorization

\[
                         \lambda=\nu\,\overline D          \tag{18}
\]

for some \(\nu\in T^*\).  Write \(a_i=\nu(X_i)\) and
\(A=\sum_i a_iE_{ii}\in\Delta\).  Pulling (18) back to \(\Lambda\)
gives

\[
 \langle\ell,F-A\rangle=0\qquad(\ell\in\Lambda).         \tag{19}
\]

The annihilator of the hyperplane \(\Lambda=d^\perp\) is

\[
                         \Lambda^\perp=\mathbb C d         \tag{20}
\]

(with the evident zero-space interpretation if \(d=0\)).  Hence (19) is
equivalent to \(F-A\in\mathbb C d\), proving (6).

The response table \(F\) kills \(K\), since

\[
 \langle k,F\rangle=\lambda(\Phi(k))=0.                   \tag{21}
\]

Conversely every \(F\in K^\perp\) defines a functional on
\(C_{\rm sel}\) by

\[
                         \lambda_F(\Phi(\ell))
                                  =\langle\ell,F\rangle.   \tag{22}
\]

Two such matrices define the same functional exactly when their difference
lies in \(\mathbb C d\).  Thus

\[
 C_{\rm sel}^*\simeq K^\perp/\mathbb C d,                 \tag{23}
\]

while top functionals give
\((\Delta+\mathbb C d)/\mathbb C d\).  Quotienting (23) by this subspace
proves (8).  It also proves that (6) is independent of the ambient
extension used in (5).

More generally, let \({\mathscr J}\subseteq K^\perp\) be the response-
matrix span of overlap rows which have already been proved literal,
grade-preserving, and source-valid on the same selector family.  Repeating
(19) gives the exact admitted-overlap module

\[
 {\mathfrak P}_{\rm sel}(d,\Phi;{\mathscr J})
       ={K^\perp\over\Delta+\mathbb C d+{\mathscr J}}.    \tag{24}
\]

A formal Bianchi matrix relation is not, by itself, membership in
\({\mathscr J}\); its other source grades must first be cancelled.  Formula
(15) grants that cancellation and takes \({\mathscr J}=\mathbb C J\).

## 3. The completed missing-square test

For a \(2\times2\) matrix, the diagonal entries of \(F-td\) can always be
absorbed into \(\Delta\).  Therefore

\[
 F\in\Delta+\mathbb C d
 \quad\Longleftrightarrow\quad
 f_{12}=tb,\quad f_{21}=tc\quad\text{for some }t,          \tag{25}
\]

which is (9).  If \((b,c)\ne(0,0)\), the space
\(\Delta+\mathbb C d\) has codimension one in \(E\), and (10) is a
nonzero defining equation for it.  Since \(K^\perp\) contains this
codimension-one space, the actual noninjective module (8) is either zero
or one-dimensional.

If the actual module (8) retains the ambient line, one source-valid crossed
row \(J\) kills it exactly when its class is nonzero, namely when
\(\omega_d(J)\ne0\).  Equivalently, this condition says that \(J\) spans
the ambient missing-square quotient.  This proves (16).  (If
noninjectivity has already made (8) zero, no crossed row is needed.)  If
\(b=c=0\), the obstruction is the full two-dimensional
off-diagonal plane.  One crossed row then realizes a desired \(F\) exactly
when

\[
             (f_{12},f_{21})\in
                    \mathbb C(J_{12},J_{21}),             \tag{26}
\]

and two crossed rows with independent off-diagonal pairs are necessary and
sufficient to close every class.

For the physical coefficient in (11), expansion of
\(\Phi(\ell)=\sum\ell_{ij}p_is_j\) at the decorated edge gives

\[
 [\Phi(\ell)]_{xy;c,d}=\langle\ell,B\rangle.              \tag{27}
\]

This proves that its response matrix is \(B\).  Equations (12)--(16) now
follow by direct matrix subtraction.

An individual oriented table \(K^\rightarrow\) deserves one additional
caution.  The scalar \(\ell(K^\rightarrow)\) descends from selectors to a
functional on \(C_{\rm sel}\) only if \(K^\rightarrow\) annihilates
\(K=\ker\Phi\) after restriction to \(\Lambda\).  Relocation needs only
one selected scalar and does not prove that descent.  The sum in (12), by
contrast, is the literal cap coefficient (27) and therefore always
descends.  The guard below makes \(\Phi\) injective, so it remains a
counterexample even after this possible issue is removed.

## 4. Relation to the Hessian filtered obstruction

The general filtered criterion asks whether a four-set pullback can be
represented, modulo rows invisible on the physical cap family, by a top
source functional and admitted overlap rows.  Equations (8) and (24) are
its finite selector-matrix incarnation after the literal full-nine rows
have identified

\[
                         M_q\Phi=D.                        \tag{28}
\]

No Hessian inverse is used here.  Conversely, a Hessian-compatible
physical functional still has to have response table in the denominator
of (24) before it is source-valid on this full-nine selector family.

There is no extra factor two in (28): the actual full-nine row contains
\(\Phi(\ell)q^{[2]}\).  The factor two in the separate identity
\(U_qL_q=2M_q\) appears only when a degree-four Hessian pullback is compared
to degree-six multiplication.

Passing (24) also remains static at one fixed chart.  To reach the
Macaulay contradiction, one must construct compatible filtered rows along
the physical binary cap line and prolong the same construction by
\(u^2,uv,v^2\), producing one nonzero degree-five cokernel functional.
Nothing in the matrix quotient performs that step automatically.

## 5. A minimal two-anchor/Bianchi guard

Take

\[
 d=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
 H^\rightarrow=E_{12},\qquad
 H^\leftarrow=-E_{21},\qquad u=1.                         \tag{29}
\]

Thus \(d\) is invertible and both assignment matrices have rank at most
one.  The edge and crossed tables are

\[
 B=H^\rightarrow+H^\leftarrow
   =\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
 J=H^\rightarrow-H^\leftarrow
   =\begin{pmatrix}0&1\\1&0\end{pmatrix}.                \tag{30}
\]

The two oriented curvatures are

\[
 K^\rightarrow=d-H^\rightarrow
   =\begin{pmatrix}1&0\\1&2\end{pmatrix},\qquad
 K^\leftarrow=d-H^\leftarrow
   =\begin{pmatrix}1&1\\2&2\end{pmatrix}.                \tag{31}
\]

They obey the exact Bianchi relation

\[
                         K^\rightarrow-K^\leftarrow+J=0.  \tag{32}
\]

Moreover

\[
 J=d-\operatorname {diag}(1,2)
       \in\Delta+\mathbb C d,
 \qquad
 \omega_d(B)=2\ne0.                                      \tag{33}
\]

Hence the crossed row adds no provenance class, while the physical edge
coefficient has the unique nonzero class.

This failure is visible on the one selector

\[
 z=E_{12}-E_{21}.                                         \tag{34}
\]

Indeed

\[
 \langle z,d\rangle=0,\qquad D(z)=0,\qquad
 \langle z,J\rangle=0,\qquad
 \langle z,B\rangle=2.                                   \tag{35}
\]

Thus every combination of the two top anchors and the crossed row vanishes
on \(z\), while the desired edge functional does not.

The relocation conclusion is present as well.  With

\[
 \eta=(1,1)^{\mathsf T},\qquad
 \xi=(3,-2)^{\mathsf T},\qquad
 \ell_*=\xi\eta^{\mathsf T},                             \tag{36}
\]

one has

\[
 \langle\ell_*,d\rangle=0,\qquad
 D(\ell_*)=3X_1-2X_2\ne0,\qquad
 \langle\ell_*,B\rangle=5
   =-\langle\ell_*,K^\rightarrow+K^\leftarrow\rangle.   \tag{37}
\]

So a rank-one, target-active selector carries the edge and oriented
curvature data, yet no one top-plus-crossed functional realizes that edge
functional on the whole selector family.

For a completely formal full-row realization, take four independent cap
symbols \(v_{ij}\), set \(\Phi(\ell)=\sum\ell_{ij}v_{ij}\), and define

\[
 M(v_{ij})=\delta_{ij}X_i-d_{ij}Q.                        \tag{38}
\]

Then

\[
                         d_{ij}Q+M(v_{ij})=\delta_{ij}X_i \tag{39}
\]

holds for all four rows, \(\Phi\) is injective, and (4) holds on
\(d^\perp\).  Grant the family functional with response table \(J\) as an
additional source-valid crossed row.  Equations (35) still prove failure.

This is a filtered small-matrix guard, not a global Krenn source.  Its
role is exact: no argument using only the full-row target map, two diagonal
anchors, rank-one oriented assignments, and the Bianchi difference can
deduce (15).  A positive proof must show that the actual crossed/overlap
packet has nonzero class (16), or supply a second source-valid row, before
undertaking the separate physical-line prolongation.

The dependency-free
[checker](../computations/verify_full_nine_selector_family_source_provenance.py)
exhausts (9), (10), and (16) over a small finite field and verifies every
integer identity in the guard.  It performs no matching-support search.
