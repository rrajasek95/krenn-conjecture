# Exact polarized six-site counterexamples, including the pair-cap form

## Outcome

The polarized six-site obstruction is false, even after imposing the
pair-deletion form that motivated it.

Let

\[
  q=\sum_{i<j}\sum_{a,b=0}^2 q_{ij}(a,b)x_{i,a}x_{j,b}
\]

in the site-square-zero algebra, and put

\[
  H_6(q)=\frac{q^3}{3!}.
\]

There are rational `q`, linear forms `p,s`, and `a=1` for which

\[
 z=q+3ps,
 \qquad
 D H_6(q)[z]=\frac{zq^2}{2}
   =\Delta_{6,3}:=\sum_{c=0}^2\prod_{i=0}^5x_{i,c}.       \tag{1}
\]

Thus neither the unrestricted equation nor the more precise
`z=a q+3ps` equation can obstruct an eight-site source through one fixed
pair/color cap.  The counterexample is finite, rational, and sparse; it is
not a border degeneration.

`computations/verify_polarized_paircap_counterexample.py` checks all 729
coefficients of (1) using exact rational arithmetic.

## 1. A nine-cell unrestricted example

Before giving the stronger example, the unrestricted equation has a very
small support witness.  Take the six nonzero cells of `q` to be

\[
\begin{array}{c|c}
\text{cell}&q_{ij}(a,b)\\ \hline
(23;0,0),(45;0,0)&1\\
(14;1,1),(35;1,1)&1\\
(05;2,2),(34;2,2)&1
\end{array}
\]

and take the three nonzero cells of `z` to be

\[
 z_{01}(0,0)=z_{02}(1,1)=z_{12}(2,2)=1.                 \tag{2}
\]

For each color, its `z` edge and its two `q` edges form a perfect
matching.  A direct incidence check shows that no other choice of one
`z` edge and two `q` edges is pairwise disjoint.  Hence (2) already gives
`zq^2/2=Delta_(6,3)`.

## 2. Rational pair-cap data

All cells not listed below are zero.  Define `q` by

\[
\begin{array}{c|r@{\qquad}c|r}
(ij;a,b)&q_{ij}(a,b)&(ij;a,b)&q_{ij}(a,b)\\ \hline
(01;1,0)&-1 &(03;0,0)&1\\
(03;1,1)&1  &(04;1,0)&-1\\
(04;1,1)&1  &(05;2,2)&1\\
(12;0,1)&-1 &(12;2,2)&1\\
(13;0,1)&-1 &(14;2,0)&-1\\
(15;1,1)&1/3&(23;1,1)&1\\
(24;1,0)&-1 &(25;0,0)&1/6\\
(34;1,0)&-1 &(34;2,2)&1/3
\end{array}                                                    \tag{3}
\]

and define the two linear forms by their site vectors

\[
\begin{array}{c|cccccc}
i&0&1&2&3&4&5\\ \hline
p_i&0&e_0&0&0&e_0&0\\
s_i&e_1&e_0+e_2&e_1&e_1&e_0&0.
\end{array}                                                    \tag{4}
\]

Here multiplication of linear forms gives, on an oriented pair `i<j`,

\[
 (ps)_{ij}=p_i\otimes s_j+s_i\otimes p_j.                 \tag{5}
\]

Set `a=1` and `z=q+3ps`.  For reference, the resulting nonzero cells of
`z` are

\[
\begin{array}{c|r@{\quad}c|r}
(01;1,0)&2 &(03;0,0)&1\\
(03;1,1)&1 &(04;1,0)&2\\
(04;1,1)&1 &(05;2,2)&1\\
(12;0,1)&2 &(12;2,2)&1\\
(13;0,1)&2 &(14;0,0)&6\\
(14;2,0)&2 &(15;1,1)&1/3\\
(23;1,1)&1 &(24;1,0)&2\\
(25;0,0)&1/6 &(34;1,0)&2\\
(34;2,2)&1/3.&&
\end{array}                                                    \tag{6}
\]

Equations (3)--(6) establish the pair-cap constraint cell by cell.

## 3. Exact coefficient check

For a coloring `c=(c_0,...,c_5)`, the coefficient of its monomial in
`zq^2/2` is

\[
 \sum_{M\in\operatorname{PM}(6)}\ \sum_{e\in M}
 z_e(c|_e)\prod_{f\in M\setminus\{e\}}q_f(c|_f).          \tag{7}
\]

With (3) and (6), only the following colorings have even one nonzero
summand in (7).  The last column lists those summands and their exact sum.

\[
\begin{array}{c|l|c}
c&\text{nonzero summand values}&\text{sum}\\ \hline
000000&1&1\\
011001&-1/3,-1/3,2/3&0\\
020000&-1/6,1/3,-1/6&0\\
100100&-1/3,1/6,-1/3,1,-1/3,-1/3,1/6&0\\
100110&-1/6,1/3,-1/6&0\\
100220&1/9,-1/18,-1/18&0\\
111101&-1/3,-1/3,2/3,2/3,-1/3,-1/3&0\\
111111&1/3,1/3,1/3&1\\
120100&-1/6,1/3,-1/6&0\\
201102&1,-2,-2,1,-2,-2,6&0\\
201222&-1/3,2/3,-1/3&0\\
221102&-1,2,-1&0\\
222102&-1,-1,2&0\\
222222&1/3,1/3,1/3&1.
\end{array}                                                    \tag{8}
\]

Every one of the other 715 colorings has no supported summand at all.
Thus (8) proves (1) directly over `Q`, and hence over `C`.

## 4. Consequence for pair deletion

The exact second-contraction identity for an eight-site source has the
quadratic factor

\[
 a_{cd}q+3p_cs_d.
\]

The example above realizes precisely this shape with `a_(cd)=1`.  It does
not by itself extend to a single eight-site source, because the other eight
color-pair caps must share the same two deleted stars and direct-edge
matrix.  What it proves is that no argument based on the isolated
six-site cap equation, even retaining its decomposable `ps` term, can be a
valid obstruction.  Any successful pair-deletion proof must use
compatibility between at least two caps (or additional data from the full
eight-site equation).

