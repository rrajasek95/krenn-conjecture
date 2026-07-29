# The eighth split: fourth-order five-triple Robin-rectangle closure

## 1. Result

At \((h,k)=(8,4)\), the collision profile

\[
                         3^5 2^2 1^3                  \tag{1}
\]

is impossible on the no-extra-singular stratum.

Choose both double values and any three of the five triple values as the
five formal layers in all-order formal-five duality.  The resulting
relation pencil lies in the quartics.  Its Wronskian has the three chosen
triple values and the three singleton values as six distinct roots, so it
is exactly their product.  A residue identity for the associated
second-order polynomial equation turns the six Robin rows into one scalar
identity.  Taking a Boolean rectangle over the ten choices of three
triples then forces every four of the five triple values to sum to zero,
which is incompatible with their distinctness.

## 2. Ten saturated quartic pencils

Write

\[
 {\cal A}=\{a_1,\ldots,a_5\},\qquad
 {\cal D}=\{d_1,d_2\},\qquad
 {\cal R}=\{r_1,r_2,r_3\}                              \tag{2}
\]

for the triple, double, and singleton values.  Fix a three-set
\(S\subset{\cal A}\), let \(\{u,v\}={\cal A}\setminus S\), and take
the formal-five set to be \(T={\cal D}\cup S\).  Every one of its ten
two-partial cores is legal because the three original singleton classes
remain outside the core.

Put

\[
 L(z)=\prod_{r\in{\cal R}}(z-r),\quad
 U_S(z)=\prod_{s\in S}(z-s),\quad
 Q_T(z)=\prod_{t\in T}(z+t).                           \tag{3}
\]

The complementary polynomial is

\[
                  A_S(z)=L(z)U_S(z)(z-u)^3(z-v)^3.     \tag{4}
\]

It has eight distinct roots, exactly six of them simple.  The all-order
formal-five theorem gives an exact relation pencil

\[
                    {\cal S}_S\subset\mathbb C[z]_{\le4}. \tag{5}
\]

For every \(P\in{\cal S}_S\), its rational derivative is

\[
 { (z+\mu)^4Q_T(z)^2P(z)\over
   L(z)^2U_S(z)^2(z-u)^4(z-v)^4}.                      \tag{6}
\]

Indeed, the gcd factor in the general derivative formula is
\((z-u)^2(z-v)^2\), so each outside triple has exponent
\(2-2\cdot3=-4\).

Let \(X_S={\cal R}\cup S\).  At a simple root \(x\in X_S\), zero
residue in (6) is the common Robin row

\[
                         P'(x)+Y_{S,x}P(x)=0,           \tag{7}
\]

where

\[
\begin{aligned}
Y_{S,x}={}&{4\over x+\mu}
 +2\sum_{t\in{\cal D}\cup S}{1\over x+t}
 -2\sum_{y\in X_S\setminus\{x\}}{1\over x-y}\\
 &\hspace{35mm}-{4\over x-u}-{4\over x-v}.            \tag{8}
\end{aligned}
\]

## 3. The accessory-polynomial residue identity

Choose a basis \(f,g\) of \({\cal S}_S\) and define

\[
 W=fg'-f'g,\qquad V=f'g''-f''g'.                       \tag{9}
\]

For quartics, \(\deg W\le6\) and \(\deg V\le4\); the apparent top
terms cancel in both expressions.  The two basis polynomials solve

\[
                         Wy''-W'y'+Vy=0.                \tag{10}
\]

Every point of \(X_S\) is a root of \(W\) by (7).  These are six
distinct points, while \(W\ne0\), so

\[
                         W=\gamma L U_S,qquad\gamma\ne0. \tag{11}
\]

In particular all six roots are simple and none is a common base point
of the pencil.  Evaluating (10) at \(x\in X_S\) and using (7) gives

\[
                         V(x)=-W'(x)Y_{S,x}.             \tag{12}
\]

The rational function \(V/W\) is \(O(z^{-2})\) at infinity.  The sum
of its finite residues is therefore zero.  Equations (11)--(12) yield
the key identity

\[
                         \sum_{x\in X_S}Y_{S,x}=0       \tag{13}
\]

for every three-set \(S\subset{\cal A}\).

## 4. The five-triple Boolean rectangle

Let \(\epsilon_i\) be the indicator that \(a_i\in S\), and denote the
left side of (13) by \(E(S)\).  First, the simple-root interaction in
(8) cancels pairwise after summing over \(x\):

\[
 \sum_{x\in X_S}\sum_{y\in X_S\setminus\{x\}}{1\over x-y}=0. \tag{14}
\]

All terms involving \(\mu\), the two doubles, or a fixed singleton are
constant or linear in the indicators.  For an unordered pair of triple
values \(a_i,a_j\), the selected-selected plus-pole terms contribute

\[
                         {4\epsilon_i\epsilon_j\over a_i+a_j}. \tag{15}
\]

The selected-outside terms have no quadratic part, since

\[
 -4\left(
 {\epsilon_i(1-\epsilon_j)\over a_i-a_j}
 +{\epsilon_j(1-\epsilon_i)\over a_j-a_i}
 \right)
 =-{4(\epsilon_i-\epsilon_j)\over a_i-a_j}.            \tag{16}
\]

Consequently there are constants \(C,A_1,\ldots,A_5\), whose values are
irrelevant, such that

\[
 E(S)=C+\sum_iA_i\epsilon_i
       +4\sum_{i<j}{\epsilon_i\epsilon_j\over a_i+a_j}. \tag{17}
\]

Now take four distinct members \(a,b,c,d\) of \({\cal A}\), and call
the remaining member \(e\).  All four sets

\[
 \{e,a,c\},\quad\{e,a,d\},\quad
 \{e,b,c\},\quad\{e,b,d\}                            \tag{18}
\]

have size three, so (13) and the alternating rectangle of (17) give

\[
\begin{aligned}
0&={1\over a+c}-{1\over a+d}
   -{1\over b+c}+{1\over b+d}\\
 &= {(a-b)(c-d)(a+b+c+d)\over
       (a+c)(a+d)(b+c)(b+d)}.                          \tag{19}
\end{aligned}
\]

The standard distinct/nonopposite hypotheses make the four denominator
factors and the two difference factors nonzero.  Hence every four of the
five triple values have sum zero.  Comparing the equations obtained by
omitting two different triple values makes those two values equal, a
contradiction.  This proves (1).

## 5. Exact audit

[verify_live_three_zero_eighth_split_k4_five_triple_robin_rectangle_closure.py](../computations/verify_live_three_zero_eighth_split_k4_five_triple_robin_rectangle_closure.py)
checks all 100 formal cores, the exact complement and derivative
exponents, the quartic Wronskian/accessory degree bounds and differential
identity, the residue-sum condition, and the full symbolic Boolean
rectangle (including cancellation of every nuisance parameter).
