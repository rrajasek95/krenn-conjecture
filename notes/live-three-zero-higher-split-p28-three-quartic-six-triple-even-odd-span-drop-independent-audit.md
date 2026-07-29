# Independent audit: the \(p=28\) \(4^3 3^6\) even--odd span drop

## 1. Verdict and scope

This audit independently reconstructs
[the \(4^3 3^6\) even--odd span argument](live-three-zero-higher-split-p28-three-quartic-six-triple-even-odd-span-drop.md).
The argument is sound.

Within the nine residual tuples of the first selected six-kernel boundary,
the argument applies to exactly

\[
                  (e,a,b,u)=(3,6,0,0),\qquad(3,6,1,-2).
                                                               \tag{1}
\]

It proves only that one member of the six-selection moving-triple family
has selected kernel dimension at most five.  It neither rules out that
selection nor closes either original collision profile.

## 2. Exact profile reconstruction

For \((3,6,0,0)\), choose one of the six triples in role two and all
\(h\) original singletons in role one.  For
\((3,6,1,-2)\), additionally hold the unique double fixed in role two
and choose all \(h-2\) original singletons.  In both cases the relation
complement for moving value \(i\) is

\[
                              4^3 3^5 1_i.                    \tag{2}
\]

It has nine classes and mass twenty-eight.  The relation-space theorem
therefore supplies

\[
                 {\cal S}_i\subseteq{\mathbb C}[z]_{\le5},
                 \qquad\dim{\cal S}_i=4.                     \tag{3}
\]

Restoring the selected triple replaces the residual simple row by a
triple row and gives the common baseline \(4^3 3^6\), of nine classes
and mass thirty.  The optional selected double is fixed throughout the
family and contributes no complementary row, so it does not change this
common lift.

Every other residual tuple has quartic count different from three or
triple count different from six.  Thus (1) is the exact applicability
list within the residual ledger.  The selection count is legal and the
selected \(q=6\) Wronskian equality is exact for all six splits

\[
 (h,k)=(22,6),(23,5),(24,4),(25,3),(26,2),(27,1).
                                                               \tag{4}
\]

## 3. Common-kernel dimension and exact pair intersections

For each triple value \(i\), let

\[
                       B_i=(z-i)^2(z+i)^2.                    \tag{5}
\]

The exact moving-triple transport gives

\[
       {\cal T}_i=B_i{\cal S}_i\subseteq{\cal K}
                          \subseteq{\mathbb C}[z]_{\le9},
       \qquad\dim{\cal T}_i=4.                               \tag{6}
\]

For the restored \(4^3 3^6\) baseline, a six-space has forced Wronskian
weight

\[
                    3(6-4)+6(6-3)=24,
                                                               \tag{7}
\]

equal to its cap \(6(10-6)=24\).  A seven-space would have forced weight

\[
                    3(7-4)+6(7-3)=33
                                                               \tag{8}
\]

against cap \(7(10-7)=21\).  Exact-row gcd corrections are
nonnegative.  Hence no seven-subspace can occur and

\[
                              \dim{\cal K}\le6.               \tag{9}
\]

The repeated values are distinct and pairwise nonopposite, so the
quartics \(B_i,B_j\) are coprime when \(i\ne j\).  Consequently

\[
 B_i{\mathbb C}[z]_{\le5}\cap B_j{\mathbb C}[z]_{\le5}
                 =B_iB_j{\mathbb C}[z]_{\le1}.               \tag{10}
\]

The right side has basis \(B_iB_j,zB_iB_j\) and dimension two.  On the
other hand, two four-spaces in the at-most-six-space (9) meet in
dimension at least two.  Since their intersection lies in (10), both
bounds are equalities:

\[
       {\cal T}_i\cap{\cal T}_j
            =\langle B_iB_j,zB_iB_j\rangle.                  \tag{11}
\]

This argument remains valid if the preliminary upper bound in (9) is
strict: in that case the dimension lower bound would exceed the
two-dimensional ambient intersection, giving an immediate contradiction.
Under the standing all-six-dimensional assumption, (11) therefore
holds for every pair.

## 4. Independent reconstruction of the five-product rank

Put \(t=z^2\) and \(a_i=i^2\), so \(B_i=(t-a_i)^2\).  Pairwise
nonopposition makes the six squares distinct.  Choose four of them,
labelled \(a_0,a_1,a_2,a_3\), and take the five edges

\[
                           01,\ 02,\ 03,\ 12,\ 13.            \tag{12}
\]

For the five corresponding polynomials

\[
                           (t-a_i)^2(t-a_j)^2                 \tag{13}
\]

the coefficient determinant in the ordered basis
\((1,t,t^2,t^3,t^4)\) factors as

\[
\begin{aligned}
 4&(a_0-a_1)^4(a_0-a_2)(a_0-a_3)\\
  &\quad{}\cdot(a_1-a_2)(a_1-a_3)(a_2-a_3)^2.                \tag{14}
\end{aligned}
\]

Every factor is nonzero for four distinct squares.  Thus these five
pair products form a basis of \({\mathbb C}[t]_{\le4}\).  Equation
(11) puts each product and its multiple by \(z\) in \({\cal K}\), so

\[
 {\mathbb C}[z^2]_{\le4}\subseteq{\cal K},
 \qquad z{\mathbb C}[z^2]_{\le4}\subseteq{\cal K}.            \tag{15}
\]

The first subspace is supported on exponents
\(\{0,2,4,6,8\}\), while the second is supported on
\(\{1,3,5,7,9\}\).  Their intersection is zero and each has dimension
five.  Therefore (15) forces a ten-dimensional direct sum inside
\({\cal K}\), contradicting (9).

Only four of the six moving values are needed for this last span
contradiction; all six are used to formulate the family in which the
existence of a dimension drop is asserted.

## 5. Independent executable audit

[verify_live_three_zero_higher_split_p28_three_quartic_six_triple_even_odd_span_drop_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_even_odd_span_drop_independent_audit.py)
does not import the primary checker.  It reconstructs both residual
selections at every split in (4), verifies the six- and seven-space
Wronskian arithmetic, checks all coprime pair-intersection dimensions,
refactors the symbolic determinant (14), tests the rank for every
four-subset of six concrete distinct squares, and builds the full
ten-by-ten even--odd coefficient matrix.
