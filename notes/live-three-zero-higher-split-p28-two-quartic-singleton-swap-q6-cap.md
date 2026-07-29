# Higher splits: a \(p=28\) two-quartic singleton-swap \(q=6\) cap

## 1. Result and scope

Continue on the two residual \(p=28\) families whose moving-triple
complement restores to

\[
                             4^2 3^7 1.
\]

They are the two symbolic tuples

\[
                  (e,a,b,u)=(2,7,0,1),(2,7,1,-1).
                                                               \tag{1}
\]

Fix one of the seven exact-triple values \(x\).  A legal low-role
selection uses \(x\) in role two, uses the exact double as well in the
second family, and leaves exactly one ordinary singleton value
complementary.  Let \(q_s\) denote the selected-row-kernel dimension when
that complementary singleton is \(s\).

**Theorem 1.1 (singleton-swap cap).**  For fixed \(x\), at most one
ordinary singleton value \(s\) can have \(q_s=6\).  Every other choice has
\(q_s=5\).

Consequently, if \(N\) is the number of ordinary singleton classes, the
whole seven-by-\(N\) selection grid has at most seven six-dimensional
entries.  At least \(N-7\) singleton columns have all seven selected
kernels five-dimensional.  Explicitly,

\[
\begin{array}{c|c|c}
(e,a,b,u)&N&\text{all-\(q=5\) columns}\\ \hline
(2,7,0,1)&h+1&\text{at least }h-6,\\
(2,7,1,-1)&h-1&\text{at least }h-8.
\end{array}                                                   \tag{2}
\]

Since \(22\le h\le27\), the last column is at least sixteen and fourteen,
respectively.  This is still a dimension statement, not a collision-profile
closure.

## 2. Every entry is five- or six-dimensional

The first six-kernel boundary gives \(q_s\le6\): a seven-space has positive
Wronskian excess at every split \(h+k=28\).  The exact pair-drop span gives
\(q_s\ge4\).  If \(q_s=4\), the singleton-incidence argument in Sections
4--5 of the
[low-role selected-lift theorem](live-three-zero-higher-split-low-role-selected-lift-incidence-closure.md)
applies directly and gives a contradiction.  That part of the argument
does not use its separate low-\(h\) inequality, which was needed only to
deduce \(q\le4\).  Therefore

\[
                              q_s\in\{5,6\}.                 \tag{3}
\]

The complementary profile for either tuple in (1) is

\[
                             4^2 3^6 1_x1_s.                \tag{4}
\]

It has ten value classes, so a \(q_s=6\) selection has a four-dimensional
row-relation space

\[
                  {\cal S}_s\subseteq\mathbb C[z]_{\le6}.
                                                               \tag{5}
\]

## 3. The two-point moving-singleton kernel

Suppose that two distinct ordinary singleton values \(s,t\) both have
\(q_s=q_t=6\).  Fix all selected layers common to the two selections and
swap which of \(s,t\) is selected.  The exact moving-singleton factors are

\[
              f_s=(z-s)^2(z+s),\qquad
              f_t=(z-t)^2(z+t).                              \tag{6}
\]

Structural separation makes them coprime, including the possible case
that one of \(s,t\) is zero.  The exact transport gives one common space

\[
\begin{aligned}
 f_t{\cal S}_s&\subseteq{\cal K}_{s,t},\\
 f_s{\cal S}_t&\subseteq{\cal K}_{s,t}
                         \subseteq\mathbb C[z]_{\le9}.
\end{aligned}                                                \tag{7}
\]

The restored baseline rows consist of the two moving simple rows, two
fixed order-four rows, six fixed order-three rows, and the fixed simple
row at \(x\).  A five-space would therefore have forced Wronskian weight

\[
          2(5-1)+2(5-4)+6(5-3)+(5-1)=26,                   \tag{8}
\]

whereas its degree-nine cap is

\[
                         5(9+1-5)=25.                       \tag{9}
\]

The standard exact-row gcd corrections are nonnegative.  Hence

\[
                         \dim{\cal K}_{s,t}\le4.             \tag{10}
\]

Both transported spaces in (7) have dimension four, so equality holds
throughout:

\[
                 f_t{\cal S}_s={\cal K}_{s,t}
                              =f_s{\cal S}_t.                \tag{11}
\]

## 4. The fixed simple row gives the contradiction

The two cubic factors are coprime, and the ambient degree is nine.
Therefore

\[
 f_t\mathbb C[z]_{\le6}\cap f_s\mathbb C[z]_{\le6}
                  =f_sf_t\mathbb C[z]_{\le3},               \tag{12}
\]

a four-space.  Equations (10)--(11) force

\[
                 {\cal K}_{s,t}=f_sf_t\mathbb C[z]_{\le3},
 \qquad
                 {\cal S}_s=f_s\mathbb C[z]_{\le3}.          \tag{13}
\]

But every member of \({\cal S}_s\) obeys the exact simple complementary
row at the fixed value \(x\):

\[
                         (U_xS)'(x)=0,\qquad U_x(x)\ne0.      \tag{14}
\]

Structural separation gives \(f_s(x)\ne0\).  On the alleged full space
in (13), the functional in (14) has nonzero coefficient
\(U_x(x)f_s(x)\) on \(V'(x)\), where \(S=f_sV\).  In particular it is a
nonzero functional on \(\mathbb C[z]_{\le3}\), and cannot annihilate all
four of its dimensions.  This contradicts (13), so two \(q=6\) singleton
choices cannot coexist.

Equation (3) proves the first assertion of Theorem 1.1.  Summing the
at-most-one bound over the seven triple values gives at most seven
\(q=6\) grid entries.  Each column containing a \(q=6\) entry accounts for
at least one such entry, so at most seven columns are contaminated.  The
counts in (2) follow from the exact singleton numbers
\(N=h+u=h+1\) and \(N=h+u=h-1\).

## 5. Exact audit

[verify_live_three_zero_higher_split_p28_two_quartic_singleton_swap_q6_cap.py](../computations/verify_live_three_zero_higher_split_p28_two_quartic_singleton_swap_q6_cap.py)
checks both formal selections at every split, the five-space Wronskian
excess, the cubic intersection dimension, the nonzero fixed-simple-row
coefficient, and every grid count.

The
[independent audit](live-three-zero-higher-split-p28-two-quartic-singleton-swap-q6-cap-independent-audit.md)
reconstructs the conditional \(q=4\) incidence contradiction, the indexing
of selected versus complementary singleton, all gcd corrections, the
universal cubic resultant including a zero singleton, and the fixed-row
coefficient.
