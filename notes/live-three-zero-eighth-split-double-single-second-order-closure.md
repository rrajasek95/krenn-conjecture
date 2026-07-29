# The eighth split: second-order closure of the double/single profile

## 1. Result

Consider the last profile on the no-extra-singular \(h=8,\ k=2\)
frontier,

\[
                         (h,k;\lambda)=(8,2;2^9 1^2).    \tag{1}
\]

Write \(V\) for the nine double values and \(r,s\) for the two singleton
values.

**Theorem 1.1.**  Profile (1) is impossible.

The proof is the double-partial construction used for the all-double
profile, with one important change.  The two original singleton factors
turn the sharp image of the relation pencil from
\(\mathbb C[z]_{\le1}\) into a two-plane in
\(\mathbb C[z]_{\le2}\).  The two singleton poles then supply two
first-order rows on this three-dimensional space.  Both rows kill the
same two-plane, so they are proportional.  Their proportionality gives a
Stieltjes equation for every \(5/4\) partition of the double values; a
single swap puts all nine double values in one quadratic fibre.

Together with the all-double closure, this removes the final two profiles
in the preceding census and completes the no-extra-singular
\(h=8, k=2\) collision frontier.

## 2. Five formal doubles

Fix a five-set \(T\subset V\), put \(C=V\setminus T\), and set

\[
 Q(z)=\prod_{t\in T}(z+t),\qquad
 C(z)=\prod_{u\in C}(z-u),\qquad
 L(z)=(z-r)(z-s).                                      \tag{2}
\]

For a pair \(\{x,y\}\subset T\), select one label at \(x,y\) and both
labels at the other three members of \(T\).  This is an eight-label core
represented by five value classes.  Its complement contains the two
unselected mates at \(x,y\), the four untouched doubles in \(C\), and the
two original singletons \(r,s\).  At most one exceptional value is zero,
so at least one of \(r,s\) is a nonzero singleton row.  Every one of these
cores is therefore legal for the simultaneous-Hermite reduction, which
gives

\[
                         0\ne q_{x,y}\in\mathbb C[z]_{\le2}. \tag{3}
\]

The corresponding rational dependence is

\[
 {q_{x,y}(z)(z-x)(z-y)C(z)^2L(z)\over
  (z+\mu)^3(z+x)^2(z+y)^2
  \prod_{t\in T\setminus\{x,y\}}(z+t)^3}.              \tag{4}
\]

Put

\[
 h_x(z)=z^2-x^2,\qquad
 P_{x,y}=h_xh_yq_{x,y}\in\mathbb C[z]_{\le6}.           \tag{5}
\]

The identity

\[
 {z-x\over(z+x)^2}={z^2-x^2\over(z+x)^3}               \tag{6}
\]

rewrites (4), without changing the rational function, as

\[
 F_P(z)={C(z)^2L(z)P(z)\over (z+\mu)^3Q(z)^3},
 \qquad P=P_{x,y}.                                     \tag{7}
\]

Define the common five-row kernel

\[
 K_T=\left\{P\in\mathbb C[z]_{\le6}:
       \operatorname {res}_{z=-t}F_P=0\quad(t\in T)\right\},
 \qquad
 W_T=\operatorname {span}\{P_{x,y}:\{x,y\}\subset T\}. \tag{8}
\]

The numerator and denominator degrees in (7) are at most \(16\) and
\(18\).  Hence \(F_P=O(z^{-2})\), and the residue theorem makes the
residue at \(-\mu\) vanish for every \(P\in K_T\).  The factor
\(C^2L\) is a unit at all six nodes

\[
                         -\mu,\quad -t\ (t\in T).        \tag{9}
\]

This remains true if one singleton is zero.  Thus the six rows are exact
second-order functionals

\[
             P''(\xi)+2Y_\xi P'(\xi)+M_\xi P(\xi).      \tag{10}
\]

## 3. The complement-independent local kernel lemma

The local lemma in Sections 3--4 of
[the all-double closure](live-three-zero-eighth-split-all-double-second-order-closure.md)
depends only on the following facts:

1. \(K_T\subset\mathbb C[z]_{\le6}\) is killed by six exact rows of the
   form (10) at six distinct nodes;
2. the ten nonzero members of \(W_T\) have the divisibilities
   \(P_{x,y}\in h_xh_y\mathbb C[z]_{\le2}\);
3. the five quadratics \(h_t\) are pairwise coprime; and
4. the six squared nodes \(\mu^2,t^2\ (t\in T)\) are distinct.

All four statements hold here.  In particular, replacing the old
five-double complementary factor by \(C^2L\) changes only the coefficients
\(Y_\xi,M_\xi\), not their exact differential orders.

For completeness, the dimension argument is recalled.  If
\(d=\dim K_T\), removal of the gcd and the six exact order-two rows gives,
for \(d\ge5\), the Wronskian deficit

\[
 (d-4)(d+3)+(d+1)n_1+2(d+1)n_3>0,                      \tag{11}
\]

where \(n_1\) counts nodes at which the gcd has order one and \(n_3\)
counts nodes at which it has order at least three.  A gcd order two is
impossible after gcd removal.  Therefore

\[
                              \dim K_T\le4.              \tag{12}
\]

The pairwise divisibilities force \(\dim W_T\ge3\).  If equality held,
the five planes

\[
              W_T\cap h_t\mathbb C[z]_{\le4}\qquad(t\in T) \tag{13}
\]

give the intersection classification

\[
              W_T=G(z){\cal E}(z^2),\qquad
              \dim{\cal E}=3,qquad \deg G\le2.         \tag{14}
\]

One way to see the only non-immediate case is to take a basis
\({\bf P}\) of \(W_T\).  The parity minors of
\({\bf P}(z),{\bf P}(-z)\) are odd of degree at most eleven and vanish at
\(0,\pm t\) for all five \(t\).  If their common cross-product constant
were nonzero, the basis would satisfy a constant linear relation; hence
the minors vanish and the primitive quotient of \({\bf P}\) is even.
This is (14).

If \(\deg G=1\) or \(2\), the degree bound makes
\({\cal E}=\mathbb C[z^2]_{\le2}\).  Restricting (10) to
\(G(z)R(z^2)\), according as \(G\) has local order zero, one, or two, the
coefficient of \(R''\), \(R'\), or \(R\) is respectively

\[
                    4\xi^2G(\xi),\qquad
                    4\xi G'(\xi),\qquad G''(\xi),       \tag{15}
\]

and is nonzero.  Thus no row can kill that whole space.  If \(G\) is
constant, \({\cal E}\) is a hyperplane in the cubics in \(z^2\).  The
six restricted rows would then be proportional to one annihilator, but
that annihilator would have all six distinct squared nodes as roots of
one cubic.  This is also impossible.  Consequently

\[
                         W_T=K_T,\qquad \dim K_T=4.       \tag{16}
\]

This verifies explicitly that the local equality survives the
\(C^2L\) complement, including the possible zero singleton.

## 4. The relation pencil maps injectively to quadratics

Put \(A=C^2L\) and

\[
                    \Omega(z)={A(z)\over(z+\mu)^3Q(z)^3}. \tag{17}
\]

By (16), the five value-residue rows on the seven-dimensional space
\(\mathbb C[z]_{\le6}\) have rank three.  Their relation space is
therefore exactly two-dimensional.

For a relation \(c=(c_t:t\in T)\), let

\[
 H_c(z)=\sum_{t\in T}c_t\,
                   \operatorname {pp}_{z=-t}\Omega(z). \tag{18}
\]

The relation says that the residue at infinity of \(P H_c\) vanishes for
\(P=1,z,\ldots,z^6\).  Since \(H_c\) is proper and its denominator divides
\(Q^3\),

\[
                 H_c(z)={N_c(z)\over Q(z)^3},
                 \qquad \deg N_c\le7.                  \tag{19}
\]

The map \(c\mapsto N_c\) is injective because the principal parts have
distinct supports.  Thus these numerators form a two-dimensional space
\({\cal N}_T\).

Divide (18) by (17):

\[
                   G_N(z)={(z+\mu)^3N(z)\over C(z)^2L(z)}. \tag{20}
\]

At every root \(-t\) of \(Q\), one has
\(G_N-c_t=O((z+t)^3)\), so \(G_N'\) has a double zero there.  Direct
differentiation gives

\[
 G_N'(z)={(z+\mu)^2\over C(z)^3L(z)^2}\,{\cal E}(N)(z), \tag{21}
\]

where

\[
 {\cal E}(N)=
 CL\bigl((z+\mu)N'+3N\bigr)
 -(z+\mu)\bigl(2C'L+CL'\bigr)N.                        \tag{22}
\]

It follows that

\[
                         {\cal E}(N)=Q^2S_N.             \tag{23}
\]

Here \(\deg C=4,\ \deg L=2\), and \(\deg N\le7\).  If
\(n=\deg N\), the nominal leading coefficient in (22) is

\[
                         n+3-(2\cdot4+2)=n-7.            \tag{24}
\]

It cancels when \(n=7\), while for \(n\le6\) the nominal degree is at
most twelve.  Since \(\deg Q^2=10\),

\[
                          S_N\in\mathbb C[z]_{\le2}.     \tag{25}
\]

The map \(N\mapsto S_N\) has zero kernel.  Indeed, \(S_N=0\) makes
\(G_N\) constant.  A nonzero constant would give

\[
                 (z+\mu)^3N=\gamma C^2L,                \tag{26}
\]

which fails at \(z=-\mu\), where \(C^2L\) is nonzero.  Hence
\(N=0\).  Since \({\cal N}_T\) has dimension two, its image

\[
                  {\cal S}_T=\{S_N:N\in{\cal N}_T\}
                         \subset\mathbb C[z]_{\le2}      \tag{27}
\]

is **exactly** two-dimensional.

Combining (21) and (23), every \(S\in{\cal S}_T\) occurs in a rational
derivative

\[
                       G_S'(z)=
 { (z+\mu)^2Q(z)^2S(z)\over C(z)^3L(z)^2}.              \tag{28}
\]

## 5. The two singleton rows

Fix one singleton, say \(r\), and write \(L=(z-r)(z-s)\).  At \(r\),
equation (28) has the form

\[
 {B_r(z)S(z)\over(z-r)^2},\qquad
 B_r(z)={ (z+\mu)^2Q(z)^2\over C(z)^3(z-s)^2}.           \tag{29}
\]

The derivative of a rational function has zero residue at every finite
pole.  Since \(B_r(r)\ne0\), every \(S\in{\cal S}_T\) therefore satisfies

\[
                    S'(r)+Y_rS(r)=0,qquad
                    Y_r={B_r'(r)\over B_r(r)}.           \tag{30}
\]

This is a nonzero first-order row on the three-dimensional quadratic
space, so its kernel has dimension two.  The same holds at \(s\).  Both
kernels contain the exactly two-dimensional space \({\cal S}_T\) from
(27); hence both equal \({\cal S}_T\), and the two rows are proportional.

In the basis \(1,z,z^2\), the normalized row at a node \(x\) is

\[
                     \rho_x(Y)=(Y,1+xY,2x+x^2Y).         \tag{31}
\]

For distinct \(r,s\), direct comparison of all three entries gives

\[
 \rho_r(Y_r)=\gamma\rho_s(Y_s)\quad\Longrightarrow\quad
 Y_r=-{2\over r-s},\quad Y_s={2\over r-s},\quad\gamma=-1. \tag{32}
\]

Only \(r-s\ne0\) was divided out in this calculation.  In particular,
(32) remains valid when either singleton value is zero.

Taking the logarithmic derivative in (29) gives

\[
 Y_r={2\over r+\mu}
     +2\sum_{t\in T}{1\over r+t}
     -3\sum_{u\in C}{1\over r-u}
     -{2\over r-s}.                                    \tag{33}
\]

The last term cancels the forced value in (32), leaving

\[
 {2\over r+\mu}
 +2\sum_{t\in T}{1\over r+t}
 -3\sum_{u\in C}{1\over r-u}=0.                        \tag{34}
\]

The analogous equation holds at \(s\).  We need only (34) at one of the
two singletons.

## 6. Partition swap and the zero-singleton audit

The construction applies to every partition \(V=T\sqcup C\) with
\(|T|=5,\ |C|=4\).  Fix any two distinct double values \(a,b\).  Choose a
partition with \(a\in T,\ b\in C\), and compare (34) with the partition
obtained by swapping \(a,b\).  All other terms cancel:

\[
 2\left({1\over r+b}-{1\over r+a}\right)
 -3\left({1\over r-a}-{1\over r-b}\right)=0.            \tag{35}
\]

Thus every two members of \(V\) have the same image under

\[
 \Phi_r(x)={2\over r+x}+{3\over r-x}
           ={5r+x\over r^2-x^2}.                        \tag{36}
\]

All nine distinct double values lie in one fibre, say
\(\Phi_r(x)=\lambda\).  Its fibre polynomial is

\[
                    \lambda(r^2-x^2)-5r-x.              \tag{37}
\]

This is a nonzero polynomial of degree at most two because its linear
coefficient is \(-1\).  It cannot have nine distinct roots.  If \(r=0\),
the same equation is \(-\lambda x^2-x=0\); every double value is nonzero,
and the contradiction is unchanged.  This proves Theorem 1.1.

## 7. Exact audit

[verify_live_three_zero_eighth_split_double_single_second_order_closure.py](../computations/verify_live_three_zero_eighth_split_double_single_second_order_closure.py)
checks all \(1260\) formal-five-double cores, their complements and the
exact lift (6), the complement-independent six-row Wronskian bound, the
three-dimensional intersection obstruction, the \(C^2L\) differential
factorization and sharp degree drop, the exact two-dimensional image,
the singleton residue rows and their proportionality (including a zero
node), the partition swap, and the nonzero quadratic fibre.
