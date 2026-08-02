# A filtered Morse contraction would replace the layer-by-layer Macaulay solve

Research target only.  Krenn's conjecture remains open.  This note isolates
the exact theorem that would turn the observed singleton pivots and
same-leading-row diamonds into an all-orders certificate.  It does not claim
that the required matching exists on chart 25, chart 26, all 31 eight-site
charts, or the uniform two-chart source complex.

## 1. Two-term cancellation lemma

Let $k$ be a field and let $D:C_1\to C_0$ be a linear map.  Choose
splittings

\[
 C_1=U\oplus K,
 \qquad C_0=V\oplus H,
 \qquad
 D=\begin{pmatrix}A&B\\ C&E\end{pmatrix},                 \tag{1}
\]

where $A:U\to V$ is invertible.  Define the reduced, or Morse, map

\[
                    D_{\rm crit}=E-CA^{-1}B:K\to H.        \tag{2}
\]

Then, for $b=(b_V,b_H)\in V\oplus H$,

\[
 b\in\operatorname {im}D
 \quad\Longleftrightarrow\quad
 b_H-CA^{-1}b_V\in\operatorname {im}D_{\rm crit}.         \tag{3}
\]

Indeed the $V$-row of $D(u,z)=b$ gives
$u=A^{-1}(b_V-Bz)$; substitution in the $H$-row gives (3).
Thus cancelling the $U\leftrightarrow V$ pivots loses no source
provenance and transports the target by the same row operations.

There is an equally useful dual statement.  Every
$\lambda\in H^*$ with $\lambda D_{\rm crit}=0$ lifts uniquely to the
full left-kernel vector

\[
                 \bigl(-\lambda CA^{-1},\lambda\bigr),    \tag{4}
\]

and its target pairing is

\[
                 \lambda b_H-\lambda CA^{-1}b_V.          \tag{5}
\]

Formula (5) is the all-at-once version of the Schur--Bockstein pairing in
[`n8-filtered-macaulay-bockstein-schur-criterion.md`](n8-filtered-macaulay-bockstein-schur-criterion.md).

## 2. Acyclic unit matchings give the invertible block

Fix bases of $C_1,C_0$, and form the bipartite incidence graph of the
nonzero matrix entries of $D_0$.  Match some columns to distinct rows on
entries which are units in $k$.  Direct every unmatched incidence edge
from a column to a row and reverse every matched edge.  If the resulting
directed graph on the matched cells has no directed cycle, a topological
ordering makes the matched square block $A_0$ triangular with unit
diagonal.  Hence $A_0$ is invertible.  Its inverse is the signed sum over
directed alternating paths in the matching graph.

For the hafnian Macaulay maps all raw incidence coefficients are positive
integers before orbit averaging, and are $1$ on actual monomial columns.
It is therefore preferable to construct the matching before taking
stabilizer orbits.  An orbit-level matching is sufficient only after its
lift to actual rows and columns is shown to remain bijective and acyclic.
This guard prevents an orbit coefficient from being mistaken for a unit
pivot.

Singleton-support columns are forced pivots.  If several columns have the
same leading row, choosing one as pivot makes every difference with another
column a kernel direction; its later rows are exactly a Morse diamond.  The
large singleton and shared-leading-row populations in the current chart-25
and degree-six calculations are therefore structural evidence for a
matching, not yet a proof of acyclicity or of the critical-cell census.

## 3. Filtered perturbations and finite gradient paths

Now suppose $C_1,C_0$ carry a finite increasing filtration

\[
 0=F_{-1}\subset F_0\subset\cdots\subset F_L=C
\]

and

\[
                         D=D_0+\Delta,                     \tag{6}
\]

where every matrix entry of $\Delta$ raises filtration by at least one.
Assume an acyclic unit matching for $D_0$ supplies an invertible matched
block $A_0$.  On the matched cells write $A=A_0+\Delta_A$.  The operator

\[
                         N=A_0^{-1}\Delta_A                \tag{7}
\]

raises filtration and hence satisfies $N^{L+1}=0$.  Consequently

\[
 A^{-1}=\sum_{j=0}^{L}(-N)^jA_0^{-1}.                     \tag{8}
\]

This is an identity, not a formal infinite series.  Substituting (8) in
(2)--(5) expresses the complete reduced differential and target readout as
finite sums over alternating gradient paths, with every occurrence of
$\Delta$ strictly increasing filtration.

The layerwise Bockstein algorithm is Gaussian elimination of the same
formula in increasing filtration.  In particular:

* a leading left-null class killed by an earlier kernel tail is a gradient
  path which enters a matched diamond;
* a class surviving the source-relative connecting map is an unmatched
  row class of $D_{\rm crit}$; and
* repeatedly repairing only the current zero-frequency residual rows can
  cycle unless all previously imposed critical equations are retained,
  because different truncations are partial sums of (8).

The last point explains why the degree-six calculation must solve the
accumulated zero-row constraints simultaneously.

## 4. Exact sufficient criterion for a localized chart

Fix one balanced port multidegree in a localized matching chart and let
$b$ be the pure-product target in its literal mixed Macaulay component.
Suppose there is a matching with the following properties.

1. Every matched incidence coefficient is a unit after the permitted
   localization.
2. A well-founded statistic strictly decreases along every reversed
   matched edge followed by an unmatched edge.  Thus the matching is
   acyclic even after Laurent support translations.
3. The statistic and port multidegree bound every gradient path, so (8)
   uses a finite support power $P^N$.
4. In the reduced complex, the transported target in (3) is in
   \(\operatorname {im}D_{\rm crit}\).  In particular it is enough that
   there are no critical rows in its component.

Then

\[
                         P^N b\in I_{\rm mix}.             \tag{9}
\]

This is precisely the saturated identity needed by the 31-chart cover.
The proof is (3) with the finite inverse (8), followed by clearing the
finitely many Laurent support denominators.  No associated-graded
surjectivity claim, completion argument, or passage from finite jets to a
formal limit is involved.

The real mathematical task is therefore not another rank computation.  It
is to find a graph-theoretic statistic which makes the matching acyclic and
to identify the critical cells.  A finite classification by underlying
cubic support cannot be the uniform answer: uniquely three-edge-colourable
cubic graphs occur in infinite families.  A viable statistic has to be
recursive, for example through alternating-cycle modules, separators, or a
source-labelled lexicographic pivot which survives graph composition.

## 5. Interface with the uniform proof

The same lemma applies to the proposed full-nine two-chart complex once its
literal total differential is constructed.  There the unmatched part must
carry two typed readouts:

* the rootless residual-Macaulay functional; and
* the inactive target/odd-residue value.

A contraction of the complete-anchor relative kernel would make both
readouts single-valued: the indeterminacy is exactly the critical image in
(2).  Conversely, a nonzero unmatched middle cell is the precise obstruction
to the hoped-for zero-indeterminacy statement.  Thus the localized $n=8$
Macaulay calculations and the uniform two-chart Bockstein are instances of
one problem: construct a source-faithful acyclic matching and compute its
small critical complex.

## 6. Current concrete tests

For chart 25 through off-carrier degree two, the orbit calculation has 920
singleton columns and 2,988 of 3,690 columns on shared leading rows.  At the
next fixed degree-three continuation the corresponding counts are 6,464
singleton columns and 32,806 of 37,337 columns on 9,036 shared leading rows.
These counts should be refined by an actual-cell acyclicity check and a list
of unmatched types.

For the chart-26 degree-six calculation, the exact first repair is the
difference of two columns with one common leading degree-five row; its tail
has twelve degree-six rows.  This is the smallest possible nontrivial
gradient path in (8).  Later batches must be decomposed into the same
singleton/diamond paths, with the accumulated critical constraints retained.

Passing these tests would not yet prove the conjecture.  It would replace
the present sequence of very large filtered solves by one finite
combinatorial contraction and would expose, rather than hide, the genuinely
critical source classes.
