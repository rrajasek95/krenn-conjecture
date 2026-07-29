# Exact two-star Segre obstruction for every fourth fixed-interior cut

## 1. Result and scope

Fix the nine aggregate cells internal to
\(S=\{0,1,2,3,4,5\}\):

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
25&E_{00}&35&E_{10}&23&E_{21}.
\end{array}                                                \tag{1}
\]

Allow every cell on both boundary stars \(i6,i7\), \(i\in S\), and on
the boundary block \(67\) to have an arbitrary complex weight.  There is
no choice of those weights for which the complete quotient identities hold
on \(z=2,3,4\) and on any one of \(z=0,1,5\).

This resolves the actual shared-endpoint factorization problem left open by
the fixed-interior cylinder calculation.  It is stronger than a bounded
weight scan and is not the false relaxation in which the star cross
monomials are independent.  All \(108\) entries on the two stars are
variables, their products are kept factorized, and all three unit diagonal
target coefficients are retained.

The result is fixed-interior only.  It does not exclude a fourth cut after
changing cells internal to \(S\), and therefore is not a global theorem
about arbitrary Krenn instances.

The standalone exact audit is
[`verify_three_cut_two_boundary_star_fourth_cut_segre_obstruction.py`](../computations/verify_three_cut_two_boundary_star_fourth_cut_segre_obstruction.py).
It uses Singular's exact rational minimal-prime and standard-basis
algorithms; no floating-point computation occurs.

## 2. The shared-star bilinear map

For \(i\in S\), internal colour \(c\), and boundary colours \(a,b\), write

\[
 p^a_{i,c}=A_{i6}[c,a],\qquad
 q^b_{i,c}=A_{i7}[c,b],\qquad
 r_{ab}=A_{67}[a,b].                                      \tag{2}
\]

Thus each \(p^a\) and \(q^b\) is an eighteen-coordinate vector.  If
\(T_{ij}=H_{S\setminus\{i,j\}}\), define the six-site tensor

\[
 \beta(p^a,q^b)=
 \sum_{i<j}\sum_{c,d}
 \left(p^a_{i,c}q^b_{j,d}+p^a_{j,d}q^b_{i,c}\right)
 e_c^{(i)}e_d^{(j)}\otimes T_{ij}.                        \tag{3}
\]

The two summands for \(i<j\) are the two literal possibilities: site \(6\)
is paired to \(i\) and site \(7\) to \(j\), or conversely.  In particular,
the terms in (3) share the \(p\)'s and \(q\)'s; none is freed as an
independent monomial.

The full matching tensor sliced at the boundary word \((a,b)\) is exactly

\[
                         H_{ab}=r_{ab}H_S+\beta(p^a,q^b). \tag{4}
\]

Direct expansion of (1) gives

\[
 H_S=[002100]+[121200]+[111110]+[220220].                 \tag{5}
\]

Set

\[
 u_0=[002100],\qquad
 u_+=[121200]+[111110]+[220220].                          \tag{6}
\]

The exact cylinder intersections proved previously say that cuts
\(2,3,4,5\) force

\[
                         H-\Delta_{8,3}\in
                         \langle H_S\rangle\otimes V_{67},            \tag{7}
\]

whereas cuts \(2,3,4,0\), or cuts \(2,3,4,1\), force

\[
                         H-\Delta_{8,3}\in
                         \langle u_0,u_+\rangle\otimes V_{67}.        \tag{8}
\]

The \(r_{ab}H_S\) term in (4) already lies in either residual space, so it
can be absorbed without restriction.  Consequently (7) is equivalent to
the nine factorized equations

\[
 \beta(p^a,q^b)-\delta_{ab}[a^6]\in\langle H_S\rangle
                         \qquad(0\leq a,b<3),             \tag{9}
\]

and (8) is equivalent to the same equations modulo
\(\langle u_0,u_+\rangle\).  Notice that (9) imposes coefficient one at
\([0^8],[1^8],[2^8]\), and zero at the other six pure internal/boundary
combinations.  The diagonal target is not discarded during elimination.

## 3. Exact cofactor reconstruction

In increasing site order, the nonzero deleted-pair cofactors of (1) are

\[
\begin{array}{c|l@{\qquad}c|l@{\qquad}c|l}
01&2100&02&1110+2200&03&1010\\
04&2020&05&1211&12&2120\\
13&1100+2020&14&1110&15&2212\\
23&0000&24&0010&25&2222\\
34&0000&35&1111&45&0021+1212.
\end{array}                                                \tag{10}
\]

Every displayed coefficient is one.  Inserting all nine colour pairs into
the two deleted sites gives \(162\) bilinear atoms.  After collisions, they
occupy \(126\) six-site words, with exact multiplicity distribution

\[
 \#\{w:m_w=1,2,3,4\}=(96,25,4,1).                        \tag{11}
\]

The checker reconstructs (5), (10), and (11) directly from all perfect
matchings of the fixed internal blocks.  Equations (9) are then generated
coordinate by coordinate from those cofactors.

For the line normal form \(N=\langle H_S\rangle\), the four coefficients
on the support of (5) are required to be equal.  For the plane normal form
\(N=\langle u_0,u_+\rangle\), the \(u_0\) coefficient is free and the other
three coefficients are required to be equal.  Every other one of the 126
reachable coordinates is set to its literal target value.  Unreachable
coordinates are identically zero on both sides.

## 4. Componentwise unit-ideal certificate

Fix one of the two residual spaces \(N\).  For each colour \(c\), let
\(I_c(N)\) be the rational polynomial ideal for the single diagonal fibre

\[
                         \beta(p^c,q^c)-[c^6]\in N.       \tag{12}
\]

Let \(X(N)\) be the ideal for all six ordered off-diagonal fibres

\[
                         \beta(p^a,q^b)\in N
                         \qquad(a\ne b).                  \tag{13}
\]

Exact `minAssGTZ` decomposition gives the following numbers of minimal
components of the three diagonal fibres:

\[
\begin{array}{c|ccc|c|c}
N&c=0&c=1&c=2&\text{component triples}&
  \text{coordinate equations}\\ \hline
\langle H_S\rangle&9&11&9&891&1125\\
\langle u_0,u_+\rangle&15&13&14&2730&1116.
\end{array}                                                \tag{14}
\]

Write the resulting minimal primes as \(P_{c,s}(N)\).  For every one of the
component triples in both rows of (14), exact standard-basis reduction gives

\[
 \operatorname{std}\left(
   P_{0,i}(N)+P_{1,j}(N)+P_{2,k}(N)+X(N)
 \right)=\langle1\rangle.                                 \tag{15}
\]

There are no surviving triples: all \(891+2730=3621\) bases in (15) are
the unit ideal.

To see why this is a complete complex certificate, any common zero of the
full system must solve each diagonal ideal \(I_c(N)\).  Over an algebraic
closure it therefore lies on one minimal component for each \(c\), hence
on one of the triples checked in (15).  But the six off-diagonal equations
then add \(X(N)\), and (15) says that triple has no zero.  A unit identity
over \(\mathbb Q\) remains a unit identity after extending scalars to
\(\mathbb C\).

## 5. Consequence for the three-cut route

The earlier formal three-atom construction succeeds only because it treats
three products from (3) as independent.  Equations (12)--(15) prove that
no actual pair of shared stars realizes that formal point, even after all
other star cells and the \(67\) block are made arbitrary.

Combining (7)--(8) with (15) excludes all three possible fourth cuts:

\[
\begin{array}{c|c|c}
\text{fourth cut}&\text{forced residual}&\text{Segre result}\\ \hline
5&\langle H_S\rangle\otimes V_{67}&\text{no solution}\\
0&\langle u_0,u_+\rangle\otimes V_{67}&\text{no solution}\\
1&\langle u_0,u_+\rangle\otimes V_{67}&\text{no solution}.
\end{array}                                                \tag{16}
\]

Thus the repaired six-site interior is now closed under arbitrary complex
changes on both boundary stars: it can support the known three complete
cuts, but it cannot be upgraded to a fourth without perturbing the
interior itself.

The
[independent audit](three-cut-two-boundary-star-fourth-cut-segre-obstruction-independent-audit.md)
reconstructs all endpoint cofactors and fibre equations without importing
the primary checker, then independently verifies all \(891+2730\) exact
componentwise unit certificates.
