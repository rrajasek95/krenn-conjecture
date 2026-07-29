# The eighth split at \(k=2\): one-triple partial-double closure

## 1. Result

At the current \(h=8,\ k=2\) collision frontier, consider the two
one-triple profiles

\[
                         3\,2^8 1,qquad 3\,2^7 1^3.       \tag{1}
\]

**Theorem 1.1.**  Both profiles in (1) are impossible on the
no-extra-singular stratum.

Fix the triple class and three double classes.  Partially selecting one of
the doubles and fully selecting the other two gives three nonzero linear
Hermite residuals.  Multiplication by \(z^2-x^2\) lifts them into one
cubic kernel.  Four exact order-two functionals force that kernel to have
dimension at most two, while coprimality forces the three lifts to span at
least two dimensions.  A rank-one-quadric ruling then shows that the three
original linear residuals are proportional.  Moving the third double
produces at least five roots of a nonzero polynomial of degree at most
four.

Combining this theorem with
[the preceding four-profile frontier](live-three-zero-eighth-split-k2-three-triple-double-closure.md)
leaves only the two all-double/single profiles \(2^{10}\) and \(2^9 1^2\).

## 2. Three partial-double residuals

Let \(a\) be the triple value and fix three double values

\[
                              T=\{t,u,v\}.                 \tag{2}
\]

For each \(x\in T\), select all three labels at \(a\), one label at
\(x\), and both labels at the other two members of \(T\).  This is a legal
eight-label core:

\[
                     R_x=a^3x\prod_{y\in T\setminus\{x\}}y^2. \tag{3}
\]

The unused mate of \(x\) is a singleton in the complement.  Four value
classes are represented, so the simultaneous-Hermite reduction gives

\[
                         0\ne q_x\in\mathbb C[z]_{\le1}.  \tag{4}
\]

The exact degrees are

\[
 \deg D_x=(k+1)+(3+1)+(1+1)+2(2+1)=15,
 \qquad \deg Q_x\le p+4-1=13.                            \tag{5}
\]

The complementary multiset has \(p+2=12\) labels, leaving the residual
degree bound one in (4).

## 3. Lifting into one formal cubic kernel

Put

\[
                         h_x(z)=z^2-x^2,qquad P_x=h_xq_x. \tag{6}
\]

Formally add the missing copy of \(x\).  Class by class,

\[
 {z-x\over(z+x)^2}\,q_x(z)
       ={1\over(z+x)^3}\,h_x(z)q_x(z).                  \tag{7}
\]

Thus the rational function is unchanged.  All three cubics \(P_x\) lie
in the common kernel \(K_T\subseteq\mathbb C[z]_{\le3}\) for the formal
core

\[
                              a^3t^2u^2v^2.               \tag{8}
\]

We only need four of its residue rows.  The order-three common pole at
\(-\mu\) gives an exact differential functional of order two.  Each of
the three fully selected double classes likewise gives an exact
order-two functional at its reflected pole.  Their four support nodes

\[
                         -\mu,-t,-u,-v                    \tag{9}
\]

are distinct: exceptional values are distinct and nonopposite, and are
structurally separated from \(\mu\).

These four rows have rank at least two.  Indeed, suppose their rank were
one and let \(L\ne0\) span their common row line.  A functional supported
at \(\xi\) of differential order at most two annihilates
\((z-\xi)^3\).  Hence \(L\) would annihilate all four cubics

\[
             (z+\mu)^3,\quad(z+t)^3,\quad(z+u)^3,\quad(z+v)^3. \tag{10}
\]

Cubics \((z-\xi_i)^3\) at four distinct nodes form a basis of
\(\mathbb C[z]_{\le3}\), by the Vandermonde determinant.  Thus \(L=0\),
a contradiction.  Therefore

\[
                              \dim K_T\le2.                \tag{11}
\]

On the other hand, the three nonzero \(P_x\) cannot span a line.  If they
did, a common cubic generator would be divisible by the three pairwise
coprime quadratics \(h_t,h_u,h_v\).  Hence their span has dimension at
least two, and (11) gives

\[
                 \operatorname{span}\{P_t,P_u,P_v\}=K_T,
                 \qquad \dim K_T=2.                       \tag{12}
\]

## 4. The quadric ruling

For a cubic \(f=c_0+c_1z+c_2z^2+c_3z^3\), write

\[
                         M_f=\begin{pmatrix}c_0&c_2\\c_1&c_3\end{pmatrix}.
                                                                    \tag{13}
\]

Each plane

\[
                       S_x=h_x\mathbb C[z]_{\le1}         \tag{14}
\]

is one ruling line of the smooth rank-one quadric

\[
                         \det M_f=c_0c_3-c_1c_2=0.        \tag{15}
\]

The projective line \(\mathbb P(K_T)\) meets the three distinct ruling
lines \(\mathbb P(S_t),\mathbb P(S_u),\mathbb P(S_v)\) at the three
distinct points \([P_t],[P_u],[P_v]\).  A quadratic restricted to a line
cannot have three distinct zeros unless it vanishes identically.  Hence
\(\mathbb P(K_T)\) lies on (15).  It is not any one of the lines in
(14), so it lies in the opposite ruling.  Equivalently, there is a single
nonzero linear polynomial \(H_T\) such that

\[
                        K_T=H_T\operatorname{span}\{1,z^2\},
 \qquad                 P_x\doteq h_xH_T\quad(x\in T).   \tag{16}
\]

Cancelling \(h_x\) in the integral domain \(\mathbb C[z]\) gives

\[
                              q_x\doteq H_T\qquad(x\in T). \tag{17}
\]

In particular, \(H_T\) satisfies the partial-double simple Robin row at
all three members of \(T\), one supplied by each original core (3).

## 5. Moving the third double

Fix two double values \(t,u\), and let \(v\) move through all other double
classes.  For the displayed row formulas, as usual, reflect all exceptional-value
coordinates and reuse the letters \(t,u,v\) for the corresponding Robin
nodes.  This simultaneous sign change preserves distinctness,
nonoppositeness, the gauges \(z^2-x^2\), and every root count.

Applied to \(T=\{t,u,v\}\), equation (17) gives a common nonzero linear
polynomial killed by the rows

\[
\begin{split}
 S_t(v)&=(Y_t,1+tY_t),&Y_t&=A+\chi_2(t,v),\\
 S_u(v)&=(Y_u,1+uY_u),&Y_u&=B+\chi_2(u,v),                \tag{18}
\end{split}
\]

where \(A,B\) contain the fixed triple contribution and the fixed other
double contribution, and

\[
 \chi_j(s,v)={j\over v-s}-{j+1\over v+s}
             ={(2j+1)s-v\over v^2-s^2}.                 \tag{19}
\]

After multiplying the first row by \(v^2-t^2\) and the second by
\(v^2-u^2\), every row entry has degree at most two in \(v\).  Their
determinant \(\widehat D_{t,u}(v)\) therefore has degree at most four.
Every moving double value is a root.  There are

\[
                         d-2=6\quad\hbox{or}\quad5        \tag{20}
\]

such values for the two profiles in (1), strictly more than four.  Thus
\(\widehat D_{t,u}\) would be identically zero.

It is not.  At the formal endpoints \(v=t\) and \(v=-t\), the cleared
first row becomes respectively

\[
                         4t(1,t),\qquad6t(1,t).           \tag{21}
\]

The double value \(t\) is structurally nonzero.  If the determinant were
identically zero, the cleared \(u\)-row would have to be proportional to
\((1,t)\) at both endpoints.  After division by the nonzero factors
\(t^2-u^2\), these two requirements differ by

\[
 (u-t)\bigl(\chi_2(u,t)-\chi_2(u,-t)\bigr)
                         ={2t\over t+u}\ne0.              \tag{22}
\]

This contradicts identical vanishing and proves Theorem 1.1.  Equation
(22) is the exact two-simple-row endpoint obstruction; no genericity or
positivity is used.

## 6. Final two-profile frontier

Removing (1) from the four-profile frontier leaves exactly

\[
\begin{array}{c|c|l}
c&e&\lambda\\ \hline
10&10&2^{10}\\
11& 9&2^9 1^2.
\end{array}                                                \tag{23}
\]

Thus every remaining \(h=8,k=2\) collision profile is double/single.

## 7. Exact audit

[verify_live_three_zero_eighth_split_k2_one_triple_partial_double_closure.py](../computations/verify_live_three_zero_eighth_split_k2_one_triple_partial_double_closure.py)
checks all selection/complement and Hermite degrees, the exact lift (7),
the four-node Vandermonde rank argument, the coprime lift span and quadric
ruling, the common partial rows, the degree-four moving determinant, both
endpoint rows, the nonzero difference (22), and the two-profile update
(23).
