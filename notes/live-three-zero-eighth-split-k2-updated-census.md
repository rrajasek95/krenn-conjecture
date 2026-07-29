# The eighth split at \(k=2\): updated exact collision census

## 1. Frozen baseline

Put

\[
 h=t-r-1=8,\qquad p=r-1=10,\qquad k=p-h=2,
 \qquad M=p+h+2=20.                                      \tag{1}
\]

This note freezes the exact no-extra-singular collision census after the
following proved routes, in this order:

1. the earlier \(H/S/C/L/Q/V\) routes of the higher-split collision
   frontier;
2. the all-\(k\) constant-core common-pole moving-role theorem;
3. the antiderivative--Wronskian theorem for legal full exchange and
   collision excess at most eight;
4. the one-bad-core repair when there are exactly \(h=8\) singleton
   classes, followed by the same antiderivative theorem.

The old sequential census was

\[
\begin{array}{c|rrrrrrrr}
 &H&S&C&L&Q&V&R&D\\ \hline
 (h,p)=(8,10)&263&270&22&14&12&3&42&1.
\end{array}                                                \tag{2}
\]

Here \(D\) is the all-distinct profile and the other 626 partitions are
collision profiles.  The three additional routes close respectively

\[
                             5,\qquad18,\qquad3             \tag{3}
\]

of the 42 old residual profiles.  These three subsets of the old residual
slice are pairwise disjoint.  Thus the updated sequential census is

\[
\begin{array}{c|rrrrrrrrrrr}
 &H&S&C&L&Q&V&M&A&O&R_2&D\\ \hline
 (8,10)&263&270&22&14&12&3&5&18&3&16&1.
\end{array}                                                \tag{4}
\]

The new letters in (4) mean moving role \(M\), ordinary legal-exchange
antiderivative \(A\), and one-bad-core repair \(O\).  The subscript on
\(R_2\) records \(k=2\), not a new proof route.

## 2. Exact tests for the three added routes

Write a multiplicity profile as

\[
 \lambda=(\lambda_1\ge\cdots\ge\lambda_c),\qquad
 e=M-c=20-c,                                               \tag{5}
\]

and let \(n_1,n_2\) count its singleton and double classes.

### 2.1 The moving-role route \(M\)

The selected core has the form

\[
                         A^rB^sx^j,\qquad r+s+j=8,         \tag{6}
\]

with three distinct value classes.  Every candidate \(x\) must have
multiplicity at least \(j\), and its complementary multiset must contain a
singleton class.  At \(k=2\), the cleared common-pole coefficient is a
nonzero polynomial of degree at most four in \(x\).  Hence five distinct
legal candidates are impossible.  Literal indexed search gives exactly
five old-residual closures:

\[
 \begin{gathered}
 4^3 2^4,\qquad
 3^5 2^2 1,\qquad
 3^3 2^4 1^3,\\
 3^2 2^6 1^2,\qquad
 3^2 2^5 1^4.
 \end{gathered}                                            \tag{7}
\]

The theorem, including the nonidentity of the degree-four polynomial and
the possible zero singleton, is proved in
[the all-\(k\) common-pole note](live-three-zero-higher-split-constant-core-common-pole.md).

### 2.2 The legal-exchange antiderivative route \(A\)

Every one-label-per-class eight-core is legal exactly when

\[
                         n_1\ge9\quad\hbox{or}\quad
                         n_2\ge c-7.                       \tag{8}
\]

When \(c\ge9\), (8) gives full cubic exchange.  The rational
antiderivative has numerator degree at most \(e-1\), and its collision-node
Wronskian deficit is at least \(d^2-e\) for a space of dimension
\(d\ge3\).  Thus every such profile with \(1\le e\le8\) is impossible.
Applied to the old residual slice, this closes exactly 18 profiles.

### 2.3 The one-bad-core route \(O\)

If \(n_1=8\), the all-singleton eight-core is the unique illegal core.
The eight available deletions of each special nine-core span at least three
dimensions, repairing exchange from size nine upward.  Combining this
with \(e\le8\) closes exactly the following three additional old residuals:

\[
             3^4 1^8,\qquad 3^2 2^3 1^8,
             \qquad 2^6 1^8.                              \tag{9}
\]

The repair, including the zero-singleton parity edge, is proved in
[the one-bad-core note](live-three-zero-eighth-split-one-bad-core-repair.md),
and the terminal deficit is proved in
[the antiderivative--Wronskian note](live-three-zero-higher-split-antiderivative-wronskian.md).

## 3. Route overlaps

On the old residual slice the three added route sets satisfy

\[
 M\cap A=M\cap O=A\cap O=\varnothing.                    \tag{10}
\]

This disjointness is special to the old residual slice, not a claim that
the theorems have disjoint hypotheses.  On all 626 collision partitions
of 20, their exact intersections with the old sequential categories are

\[
\begin{array}{c|rrrrrrrr|r}
 &H&S&C&L&Q&V&R&D&\text{total}\\ \hline
 M&75&181&17&11&7&2&5&0&298\\
 A& 3& 18& 2& 4&8&0&18&0& 53\\
 O& 0&  3& 0& 0&2&0& 3&0&  8.
\end{array}                                                \tag{11}
\]

The intrinsic pairwise overlap sizes on the same full collision universe
are

\[
             |M\cap A|=29,\qquad |M\cap O|=4,
             \qquad |A\cap O|=0,\qquad |M\cap A\cap O|=0. \tag{12}
\]

Equations (10)--(12) distinguish theorem overlap from incremental census
credit and prevent double-counting.

## 4. The sixteen residual profiles

Order profiles lexicographically by

\[
                            (c,e,\lambda),                 \tag{13}
\]

where \(\lambda\) is its weakly decreasing tuple.  The updated residual
set is exactly

\[
\begin{array}{c|c|l}
c&e&\lambda\\ \hline
 6&14&4^2 3^4\\
 7&13&3^6 2\\
 8&12&3^4 2^4\\
 8&12&3^6 1^2\\
 9&11&3^5 2 1^3\\
10&10&2^{10}\\
10&10&3\,2^8 1\\
10&10&3^4 2^2 1^4\\
10&10&3^5 1^5\\
11& 9&2^9 1^2\\
11& 9&3\,2^7 1^3\\
11& 9&3^3 2^3 1^5\\
11& 9&3^4 2 1^6\\
12& 8&3^2 2^4 1^6\\
12& 8&3^3 2^2 1^7\\
13& 7&3\,2^5 1^7.
\end{array}                                                \tag{14}
\]

Consequently the first unresolved profile in this frozen baseline is

\[
                              \boxed{4^2 3^4}.             \tag{15}
\]

For clean incremental bookkeeping, if a later exact \(k=2\) role-swap
theorem removes (15), the next profile in the frozen order is

\[
                              \boxed{3^6 2}.               \tag{16}
\]

Equation (16) is only the mechanically identified successor here; this
note does not pre-credit a route not included in Section 1.

## 5. Exact audit

[verify_live_three_zero_eighth_split_k2_updated_census.py](../computations/verify_live_three_zero_eighth_split_k2_updated_census.py)
independently enumerates all partitions of 20, imports the frozen
\(H/S/C/L/Q/V\) classifier, performs the literal five-candidate moving-role
search, checks (8), identifies the unique illegal singleton core in every
profile credited to \(O\), reconstructs both the residual-slice
disjointness and the global overlap table, and compares the ordered output
term by term with (14).
