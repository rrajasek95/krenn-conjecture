# The eighth split: stable double-family five-set swap frontier

## 1. Scope and result

Consider the two stable no-selection families

\[
 \lambda=2^m,\quad k=2m-18,
 \qquad\text{or}\qquad
 \lambda=2^m1,\quad k=2m-17,\qquad m\geq12.              \tag{1}
\]

Put \(\epsilon=0\) in the first family and \(\epsilon=1\) in the second,
so

\[
                         k=2m-18+\epsilon.               \tag{2}
\]

When \(\epsilon=1\), write \(r\) for the singleton value and put
\(L(z)=z-r\); when \(\epsilon=0\), put \(L=1\).

This note does not close (1).  It gives the exact arbitrary-complement
dual map, all complementary residue rows, the complete one-value swap
law, and two fixed-degree overlap invariants:

1. every relation-numerator pencil has five prescribed triple
   ramifications and only a quadratic residual Wronskian factor;
2. derivative pencils belonging to adjacent five-sets have intersection
   dimension at most one.

Thus the successful small-target arguments cannot be extended by
identifying or transporting the whole relation pencil across a swap.  Any
closure of (1) must control the moving pencils themselves, or exploit the
fixed-degree numerator pencils across more than one swap.

## 2. Arbitrary-complement five-double duality

Let \(V\) be the \(m\)-element set of double values.  Fix a five-set
\(T\subset V\), put \(O=V\setminus T\), and write

\[
\begin{aligned}
 n&=|O|=m-5,\\
 Q_T(z)&=\prod_{t\in T}(z+t),\\
 C_O(z)&=\prod_{u\in O}(z-u),\\
 A_T(z)&=C_O(z)^2L(z).
\end{aligned}                                             \tag{3}
\]

Every formal-five pair drop is legal: the two partially selected double
layers leave two nonzero singleton mates.  The exact five-double kernel
theorem therefore gives

\[
 K_T\subseteq\mathbb C[z]_{\leq6},\qquad
                         \dim K_T=4.                     \tag{4}
\]

The five selected rows have rank three and hence a two-dimensional relation
space.  Its distinct-principal-part numerators form a two-plane

\[
                         {\cal N}_T\subseteq
                         \mathbb C[z]_{\leq7}.            \tag{5}
\]

For \(N\in{\cal N}_T\), define

\[
\begin{aligned}
 {\cal E}_T(N)={}&
 C_OL\bigl((z+\mu)N'+(k+1)N\bigr)\\
 &-(z+\mu)\bigl(2C_O'L+C_OL'\bigr)N.                    \tag{6}
\end{aligned}
\]

Exact differentiation gives

\[
 {d\over dz}{(z+\mu)^{k+1}N\over C_O^2L}
 ={(z+\mu)^k\over C_O^3L^2}\,{\cal E}_T(N).             \tag{7}
\]

The triple contact at the five selected poles is equivalent to

\[
                         {\cal E}_T(N)=Q_T^2S_N.         \tag{8}
\]

If \(j=\deg N\leq7\), the nominal leading coefficient in (6) is

\[
             j+(k+1)-(2n+\epsilon)=j-7.                 \tag{9}
\]

It cancels at \(j=7\).  Hence

\[
\boxed{
 {\cal S}_T:=\{S_N:N\in{\cal N}_T\}
 \subseteq\mathbb C[z]_{\leq n+\epsilon-4},
 \qquad\dim{\cal S}_T=2.}                               \tag{10}
\]

The map is injective: \({\cal E}_T(N)=0\) makes the left side of (7)
constant, and evaluation at \(-\mu\) forces that constant and \(N\) to
vanish.  Every \(S\in{\cal S}_T\) therefore occurs in the rational
derivative

\[
                         G_S'(z)=
 { (z+\mu)^kQ_T(z)^2S(z)\over C_O(z)^3L(z)^2}.           \tag{11}
\]

For the two families, the target degrees in (10) are respectively
\(m-9\) and \(m-8\).

## 3. The full complementary row system

Fix \(u\in O\), write \(C_O=(z-u)C_u\), and set

\[
 B_{T,u}(z)=
 { (z+\mu)^kQ_T(z)^2\over C_u(z)^3L(z)^2}.              \tag{12}
\]

The zero residue of (11) at its triple pole \(u\) is

\[
 (B_{T,u}S)''(u)=0.                                     \tag{13}
\]

After normalization, this is the exact second-order row

\[
 S''(u)+2X_T(u)S'(u)+Z_T(u)S(u)=0,                     \tag{14}
\]

where

\[
\begin{aligned}
X_T(u)={}&{k\over u+\mu}
 +2\sum_{t\in T}{1\over u+t}
 -3\sum_{\substack{v\in O\\v\ne u}}{1\over u-v}
 -{2\epsilon\over u-r},\\
J_T(u)={}&-{k\over(u+\mu)^2}
 -2\sum_{t\in T}{1\over(u+t)^2}
 +3\sum_{\substack{v\in O\\v\ne u}}{1\over(u-v)^2}
 +{2\epsilon\over(u-r)^2},\\
Z_T(u)={}&X_T(u)^2+J_T(u).
\end{aligned}                                             \tag{15}
\]

When \(\epsilon=1\), the double pole at \(r\) gives the additional exact
first-order row

\[
 S'(r)+A_T(r)S(r)=0,\qquad
 A_T(r)={k\over r+\mu}
 +2\sum_{t\in T}{1\over r+t}
 -3\sum_{v\in O}{1\over r-v}.                           \tag{16}
\]

If \(S_0,S_1\) span \({\cal S}_T\) and
\(W_T=\operatorname{Wr}(S_0,S_1)\), subtracting the two equations (14)
gives the useful scalar consequence

\[
                         W_T'(u)+2X_T(u)W_T(u)=0
                         \qquad(u\in O).                 \tag{17}
\]

The singleton row similarly gives \(W_T(r)=0\).  Unlike the linear and
quadratic target cases, (14) is not a hyperplane which determines the
pencil when \(m\geq12\).

## 4. Fixed-degree numerator invariants

Choose a basis \(N_0,N_1\) of \({\cal N}_T\), let
\(S_i={\cal E}_T(N_i)/Q_T^2\), and orient

\[
                         W_N=N_0N_1'-N_1N_0'.            \tag{18}
\]

At every selected root \(-t\), equations (7)--(8) say that the two
functions

\[
                         {(z+\mu)^{k+1}N_i\over C_O^2L}
\]

are constant modulo \((z+t)^3\).  Their two-jets are therefore
proportional.  Equivalently,

\[
\boxed{
                         W_N=Q_T^2R_T,\qquad
                         R_T\in\mathbb C[z]_{\leq2}.}    \tag{19}
\]

There is also an exact mixed determinant identity.  Direct cancellation
in (6) gives

\[
 N_0{\cal E}_T(N_1)-N_1{\cal E}_T(N_0)
             =C_OL(z+\mu)W_N.
\]

Using (8) and (19) yields

\[
\boxed{
                         N_0S_1-N_1S_0
                         =C_OL(z+\mu)R_T.}               \tag{20}
\]

Both sides have the sharp degree \(n+\epsilon+3\).  The numerator-side
degree is fixed once and for all.  There is a small base-locus point which
is worth making explicit.  If every \(N\in{\cal N}_T\) vanished at one
selected point \(-t\), then \({\cal E}_T(N)(-t)=0\) and
\({\cal E}_T(N)'(-t)=0\), together with the structural units
\(C_OL(z+\mu)\) there, would successively force

\[
                         N(-t)=N'(-t)=N''(-t)=0.         \tag{20a}
\]

Thus each selected basepoint spends at least three degrees of the pencil
gcd.  If there were \(b\) such basepoints, the reduced rational map would
have degree at most \(7-3b\), while the other \(5-b\) selected points are
genuine ramification points of index at least three.  Riemann--Hurwitz
would give

\[
               2(5-b)\leq2(7-3b)-2,
\]

which forces \(b=0\).  Applying the same count to the total pencil gcd of
degree \(g\), now with all five genuine triple ramifications, gives

\[
                         10\leq2(7-g)-2,
                         \qquad g\leq1.                 \tag{20b}
\]

Consequently the reduced map \(N_0/N_1\) has degree six or seven, all five
selected points are genuine triple ramification points, and it has at most
two residual ramification units.  In particular no selected factor of
\(Q_T\) meets the pencil gcd in (19).

## 5. Exact one-value swap law

Let \(a\in T\), \(b\in O\), and form

\[
 T'=T\setminus\{a\}\cup\{b\},\qquad
 O'=O\setminus\{b\}\cup\{a\}.                           \tag{21}
\]

For a common outside value \(u\in O\cap O'\), put

\[
\begin{aligned}
\Phi_u(x)&={2\over u+x}+{3\over u-x}
           ={5u+x\over u^2-x^2},\\
\Psi_u(x)&={2\over(u+x)^2}+{3\over(u-x)^2},\\
\delta_u&=\Phi_u(b)-\Phi_u(a),\\
\eta_u&=\Psi_u(a)-\Psi_u(b).
\end{aligned}                                             \tag{22}
\]

Then (15) transforms exactly as

\[
\boxed{
\begin{aligned}
X_{T'}(u)&=X_T(u)+\delta_u,\\
J_{T'}(u)&=J_T(u)+\eta_u,\\
Z_{T'}(u)&=Z_T(u)+2X_T(u)\delta_u+\delta_u^2+\eta_u.
\end{aligned}}                                           \tag{23}
\]

In the singleton family,

\[
                         A_{T'}(r)-A_T(r)
                         =\Phi_r(b)-\Phi_r(a).           \tag{24}
\]

The full rational multiplier in (11) changes by

\[
 {G_{T'}'(S)\over G_T'(S)}
 ={(z+b)^2(z-b)^3\over(z+a)^2(z-a)^3}                  \tag{25}
\]

when the same formal multiplier \(S\) is inserted.

There is no closed transformation on \(S\) alone.  Put

\[
                         R_{a,b}(z)={z-a\over z-b}.
\]

For the same numerator \(N\), direct use of (6) gives

\[
 {\cal E}_{T'}(N)
 =R_{a,b}{\cal E}_T(N)
 -2(z+\mu)C_OLR_{a,b}'N.                               \tag{26}
\]

Thus, if \(N\) happened to lie in both numerator pencils, its two images
would obey

\[
 Q_{T'}^2S_{T'}^{[N]}
 =R_{a,b}Q_T^2S_T^{[N]}
 -2(z+\mu)C_OLR_{a,b}'N.                               \tag{27}
\]

The inhomogeneous \(N\)-term is the exact obstruction to transporting
the multiplier pencil using only the Stieltjes increments (23).

## 6. An eleven-value localization

Fix eleven double values \(E\subseteq V\) and call the remaining
\(b=m-11\) double values background.  Choose \(T\subset E\), \(|T|=5\).
There are six variable outside doubles in \(E\setminus T\).

In the pure family, \({\cal S}_T\) lies in a polynomial space of vector
dimension \(b+3\).  Its complementary double rows therefore span at most
\(b+1\) dimensions.  In the singleton family, first restrict the
\((b+4)\)-dimensional polynomial space to the exact singleton hyperplane
(16); again the double rows restrict to a space of dimension \(b+3\) and
span at most \(b+1\) dimensions.  Consequently,

\[
\boxed{\text{the \(b\) background rows together with any two variable
outside-double rows have rank at most \(b+1\).}}          \tag{28}
\]

For \(b=0\), the two variable rows are proportional; this is precisely the
finite \(m=11\) mechanism.  For \(b>0\), (28) is a moving
\((b+2)\)-row determinant.  The background rows also acquire the
quadratic swap increments (23), so the fourth Boolean difference used at
\(m=11\) no longer isolates only the two variable rows.

## 7. Adjacent pencils share at most one derivative

The exact swap multiplier also gives a sharp overlap obstruction.
Retain \(a,b\) from (21), write

\[
\begin{aligned}
 A_{a,b}(z)&=(z+b)^2(z-b)^3,\\
 B_{a,b}(z)&=(z+a)^2(z-a)^3,
\end{aligned}                                             \tag{29}
\]

and let \(U=V\setminus(T\cup\{b\})\), so \(|U|=m-6\).  Structural
noncollision makes \(A_{a,b}\) and \(B_{a,b}\) coprime.

If one rational derivative belongs to both adjacent derivative pencils,
say

\[
 { (z+\mu)^kQ_T^2S\over C_O^3L^2}
 ={ (z+\mu)^kQ_{T'}^2S'\over C_{O'}^3L^2},              \tag{30}
\]

then (25) gives

\[
                         B_{a,b}S=A_{a,b}S'.             \tag{31}
\]

Hence \(S=A_{a,b}E\) and \(S'=B_{a,b}E\).  Their common derivative is

\[
 { (z+\mu)^kQ_{T\cup\{b\}}(z)^2E(z)\over C_U(z)^3L(z)^2}.              \tag{32}
\]

Suppose two independent common derivatives existed.  After choosing the
antiderivative constants to make them vanish at \(-\mu\), they would have
the form

\[
                         {(z+\mu)^{k+1}M_i(z)\over
                          C_U(z)^2L(z)},\qquad
                         \deg M_i\leq5.                  \tag{33}
\]

The degree-five bound follows exactly from

\[
 2|U|+\epsilon-(k+1)
 =2(m-6)+\epsilon-(2m-17+\epsilon)=5.                  \tag{34}
\]

But (32) has double zeros at the six selected poles
\(-t\), \(t\in T\cup\{b\}\).  Repeating the numerator-Wronskian argument
would force

\[
 Q_{T\cup\{b\}}^2\mid\operatorname{Wr}(M_0,M_1).
\]

The divisor has degree twelve, while the Wronskian of two quintics has
degree at most eight.  This is impossible.  Therefore

\[
\boxed{\dim\bigl(\text{adjacent rational-derivative pencils}\bigr)
       \leq1.}                                           \tag{35}
\]

In particular, a swap can never identify the two full pencils and then
subtract their two basis rows as in the small linear target.  Equation
(35) is a barrier, not a closure: the two pencils may be disjoint, and no
dimension argument forces even the one common line.

## 8. Finite neighbors and the remaining task

The finite neighboring profiles use extra target-space coincidences and
remain logically separate:

* \(2^{10}\) has a full linear target;
* \(2^{11}\) has a quadratic target, so every outside row determines the
  same plane and the row-Boolean argument applies;
* \(2^{10}1\) is the six-complementary-class endpoint;
* \(2^{11}1\) has a cubic target cut by its singleton row, leading to the
  matching closure.

The single-swap obstruction above remains valid, but a later construction
does couple many five-sets at once.  Fixing a common four-double core and
varying the fifth embeds all multiplier pencils in one exactness kernel.
The resulting
[common-octic closure](live-three-zero-eighth-split-sixth-order-twelve-double-common-lift-closure.md)
excludes \(2^{12}\), and the
[common-nonic closures](live-three-zero-eighth-split-stable-double-nonic-common-lift-closures.md)
exclude \(2^{13}\) and \(2^{12}1\).  The later
[decic four-space closure](live-three-zero-eighth-split-stable-double-decic-four-space-closure.md)
excludes \(2^{13}1\) and every dimension-at-most-four branch of
\(2^{14}\), even though two lifted planes may meet along the degree-ten
product of their lift factors.  The first surviving boundary is now the
five-dimensional saturated kernel for \(2^{14}\).  Its
[exact frontier](live-three-zero-eighth-split-fourteen-double-five-space-saturation-frontier.md)
shows that the pair-intersection graph has maximum degree two but may be
empty at the level of all abstract Grassmann incidences.  A comparison
which assumes a common multiplier or numerator across one swap remains
invalid.

## 9. Exact audit

[verify_live_three_zero_eighth_split_stable_double_five_set_swap_frontier.py](../computations/verify_live_three_zero_eighth_split_stable_double_five_set_swap_frontier.py)
checks both degree ledgers, the arbitrary-complement derivative map, every
complementary row and swap sign, the Wronskian and mixed determinant
identities, the same-numerator transformation, the eleven-value rank
count, and the six-ramification overlap obstruction.
