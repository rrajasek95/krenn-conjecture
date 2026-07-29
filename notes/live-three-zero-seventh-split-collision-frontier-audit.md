# Independent audit of the seventh-split collision frontier

## 1. Outcome and scope

This is an independent audit of
[live-three-zero-seventh-split-collision-frontier.md](live-three-zero-seventh-split-collision-frontier.md).
It finds no discrepancy.  A dynamic-programming census by multiplicity
histograms reproduces every stated count, every small triple residual, the
closed double/single boundary, and the seven-family stable tail.  A separate
generating-function calculation verifies the deleted-\(e_7\) descent.

The audit does **not** promote any frontier profile to a closure.  Every
profile listed as residual below remains open.

The feasibility bound is important.  Since

\[
 t=r+8=p+9,\qquad r=p+1,
\]

the ambient inequality \(t\le2r-1\) is equivalent to

\[
                         p+9\le2p+1\iff p\ge8.               \tag{1}
\]

Thus \(p=7\) is only a formal one-step diagnostic and is not a seventh-split
stratum.

## 2. A census mechanism independent of integer-partition search

For profiles whose maximum multiplicity is at most six, encode the profile
by the histogram

\[
                 c=(c_1,c_2,\ldots,c_6),\qquad
                 \sum_{m=1}^6m c_m=M=p+9.                   \tag{2}
\]

The audit builds all such histograms by a six-stage unbounded-knapsack
dynamic program.  Separately, Euler's coin-change recurrence computes the
full partition number \(P(M)\).  Hence

\[
 \#H=P(M)-\#\{c:\text{(2) holds}\},                          \tag{3}
\]

because the omitted partitions are exactly those containing a part at least
seven.  This is structurally different from the main checker's recursive
partition generation and class-index search.

For a short witness, the audit allocates two distinct class identities of
sizes \(m,n\le6\), selects positive counts summing to seven, and directly
counts singleton classes left in the complement.

For a moving witness, let \(A\in\{1,2,3\}\) be the number of simple anchors
and let \(B=3,5,7\), respectively, be the required candidate count.  The
audit allocates:

1. a size-count vector \(a_m\) of \(A\) distinct nonzero anchor classes;
2. a distinct fixed class of size \(f_0\), from which \(f\ge1\) labels are
   selected;
3. a moving class of size \(m\), from which
   \(j=7-A-f\ge1\) labels are selected.

For a proposed moving class, the number of singleton row classes after the
selection is exactly

\[
 \sigma_m=
 a_2+\mathbf1_{f_0-f=1}
 +c_1-a_1-\mathbf1_{f_0=1}-\mathbf1_{m=1}
 +\mathbf1_{m-j=1}.                                        \tag{4}
\]

All role-availability and distinct-class constraints are imposed before
(4) is evaluated.  A class is a legal candidate precisely when \(m\ge j\)
and \(\sigma_m\ge1\).  Summing its available class count over
\(m=1,\ldots,6\) gives the exact number of distinct moving values.  The
thresholds \(B=3,5,7\) are the strict root-count thresholds for the
constant, linear, and quadratic residual determinants.

## 3. Zero-value legality

Structural pair-sum admissibility permits at most one zero exceptional
value, and that value must be a singleton class.  The audit therefore runs
each moving-role allocation in two states:

- no zero value;
- one designated zero singleton, when \(c_1>0\).

The designated zero is removed from the nonzero anchor inventory.  It may
still serve as the fixed or moving class, since those roles do not use the
opposite-pole anchor argument.  Formula (4) counts it like every other
singleton.  A profile is assigned to \(C,L\), or \(Q\) only when a legal
witness exists in every admissible zero state.  Singleton classes are
interchangeable at the multiplicity level, so one designated singleton
exhausts all possible locations of the unique zero.

## 4. Independently reproduced census

Using the priority order \(H,S,C,L,Q,R,D\), the independent counts are

\[
\begin{array}{c|rrrrrrr|r}
p&H&S&C&L&Q&R&D&\mathrm{total}\\ \hline
8 &134&119&13&7 &9 &14&1&297\\
9 &186&151&14&10&11&12&1&385\\
10&255&182&18&13&12&9&1&490\\
11&345&226&19&14&13&9&1&627\\
12&461&269&22&16&14&9&1&792\\
13&611&325&25&17&16&7&1&1002.
\end{array}                                                   \tag{5}
\]

For completeness, the infeasible formal value \(p=7\) gives

\[
 (H,S,C,L,Q,R,D)=(95,96,11,4,6,18,1),                       \tag{6}
\]

but (6) is not used as a geometric stratum.

No residual contains a class of size four, five, or six.  Writing a
triple-containing residual as \((q,d,s)\), the feasible residuals are

\[
\begin{array}{c|l}
p&(q,d,s)\\ \hline
8&(3,4,0),(3,3,2),(3,2,4),(3,1,6),(2,5,1),(2,3,5)\\
9&(6,0,0),(3,4,1),(3,2,5)\\
12&(7,0,0).
\end{array}                                                   \tag{7}
\]

There are none for \(p=10,11\), or any \(p\ge13\).

For double/single profiles \((2^d,1^s)\), the role-allocation engine
independently recovers

\[
 (d\ge8,s\ge4)\ \vee\ (d\ge9,s\ge3)\ \vee\
 (d\ge10,s\ge2)\ \vee\ d\ge11                              \tag{8}
\]

as the exact condition for a proved moving closure.  Indeed, the only
possible seven-label role pattern is \(1+1+1+2+2\).  If \(a\) anchors
come from double classes, there are \(d-1-a\) moving double candidates,
while zero-safe singleton availability requires
\(s\ge4-a\).  Taking \(a=0,1,2,3\) gives (8).

For \(8\le p\le12\), all residual double/single profiles have
\(s=p+9-2d\) and the following values of \(d\):

\[
\begin{array}{c|l}
p&d\\ \hline
8&1,2,3,4,5,6,7,8\\
9&1,2,3,4,5,6,7,8,9\\
10&1,2,3,4,5,6,7,8,9\\
11&1,2,3,4,5,6,7,9,10\\
12&1,2,3,4,5,6,7,10.
\end{array}                                                   \tag{9}
\]

Equations (7) and (9) are an exact enumeration of the feasible small
residual collision profiles.

## 5. Independent deleted-\(e_7\) check

At the smallest feasible value, \(|N|=p+2\ge10\).  If all transformed
values \(h_i\) are equal and nonzero, every deleted-pair pivot is

\[
                         7!\binom p7h^7\ne0.                 \tag{10}
\]

Otherwise choose \(h_j\ne h_k\).  The audit extracts elementary symmetric
functions as coefficients of

\[
                           \prod_i(1+h_i z),                  \tag{11}
\]

rather than summing subsets as in the main checker.  It verifies exactly

\[
 e_7(N\setminus\{i,j\})-e_7(N\setminus\{i,k\})
 =(h_k-h_j)e_6(N\setminus\{i,j,k\}).                         \tag{12}
\]

Thus all one-deletion \(e_6\)'s on \(W=N\setminus\{j,k\}\), where
\(|W|=p\ge8\), would vanish.  Coefficient extraction from (11) also gives

\[
 \sum_{i\in W}e_d(W\setminus\{i\})=(|W|-d)e_d(W),\qquad
 e_d(W)=e_d(W\setminus\{i\})+h_i e_{d-1}(W\setminus\{i\}). \tag{13}
\]

Since \(|W|-d\ne0\) for \(d=6,5,\ldots,1\) and every \(h_i\ne0\), (13)
descends to \(h_i=0\), a contradiction.  This independently confirms the
entire \(H\) sector.

## 6. Finite-to-uniform persistence

The histogram census at totals

\[
                         M=22,23,\ldots,28                    \tag{14}
\]

has exactly seven residual collision profiles at each total:

\[
                         (2^d,1^{M-2d}),\qquad1\le d\le7.    \tag{15}
\]

The checker retains the actual short or moving role allocation for every
handled histogram in the relevant range and verifies that the same role
allocation remains legal after appending a class of each size
\(1,2,\ldots,6\).  The zero cases are checked separately:

- appending a nonzero class preserves the old no-zero or old-zero witness;
- if a newly appended singleton is the unique zero, use the old no-zero
  witness.  All its old anchors are nonzero, and leaving the new zero class
  untouched supplies a singleton in every moving complement.

Appending a class of size at least seven instead enters \(H\).  These are
combinatorial role statements: the constants in the new residual polynomial
may change, but the moving lemmas are uniform in those constants.

Now take any profile of total at least 29, maximum at most six, and with a
part at least three.  Preserve one such part and delete whole other classes
until the total first falls below 29.  The resulting total lies between 23
and 28, because the last removed class has size at most six.  It cannot be a
residual by (14)--(15), and its concrete witness lifts back one class at a
time by persistence.  Hence no triple-containing residual occurs above the
finite base.  Applying (8) directly to the remaining profiles gives the
exact stable open frontier

\[
                 \boxed{(2^d,1^{p+9-2d}),\qquad1\le d\le7}
                 \qquad(p\ge13).                             \tag{16}
\]

Again, (16) is a residual list, not a closure claim.

## 7. Reproducible check

[verify_live_three_zero_seventh_split_collision_frontier_audit.py](../computations/verify_live_three_zero_seventh_split_collision_frontier_audit.py)
performs the histogram DP, Euler partition count, role-allocation census,
designated-zero checks, exact residual comparisons, generating-function
deleted-\(e_7\) identities, and concrete witness-persistence tests.  It is
independent of the main checker's partition recursion and index-level witness
enumeration and reports all residuals as open.
