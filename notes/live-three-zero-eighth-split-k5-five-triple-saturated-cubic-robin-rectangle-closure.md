# The eighth split at \(k=5\): two saturated-cubic closures

## 1. Result and five-triple inventory

At \((h,k,M)=(8,5,23)\), the collision profiles

\[
                    3^5 2^3 1^2,\qquad 3^4 2^4 1^3     \tag{1}
\]

is impossible on the no-extra-singular stratum.

After the first five fifth-order closures, the profiles containing five
exact triple classes are exactly

\[
                 3^5 2^d1^{8-2d},\qquad 0\le d\le3.    \tag{2}
\]

Choose five repeated classes as formal double layers.  If \(x\) of the
chosen classes are doubles, then the other \(5-x\) are triples, and the
complementary profile is

\[
                  3^x2^{d-x}1^{13-2d-x}.               \tag{3}
\]

Thus its numbers of roots and simple roots, its relation degree, and its
unused simple-root Wronskian degree are respectively

\[
 c=13-d-x,\qquad s=13-2d-x,\qquad
 n=c-4=9-d-x,qquad (2n-2)-s=3-x.                      \tag{4}
\]

Every candidate formal choice is legal.  Indeed, all profiles (2) have at
least two original singleton classes, so at least one remains nonzero even
under the exceptional zero placement.  The exact inventory has 84 formal
choices.  Equation (4) is saturated precisely when \(x=3\), which occurs
among the five-triple profiles only for the first profile in (1): select
all three doubles and any two of the five triples.  There are ten such
choices.

The second profile in (1) has a companion saturated selection.  Select
all four doubles and any one of its four triples.  Its complement is again
\(3^3 1^4\), so it gives four more cubic pencils.  Every pair-drop core is
legal: in the worst zero placement a double--double drop has five nonzero
singleton guards and a double--triple drop has three.

## 2. The five-triple saturated cubic pencil

Write \({\cal A}=\{a_1,\ldots,a_5\}\) for the triple values,
\({\cal D}=\{d_1,d_2,d_3\}\) for the double values, and
\({\cal R}=\{r_1,r_2\}\) for the singleton values.  Fix a two-set
\(S\subset{\cal A}\), put \({\cal O}={\cal A}\setminus S\), and choose
the formal-five set

\[
                              T={\cal D}\cup S.          \tag{5}
\]

All ten pair-drop cores are legal, including if one original singleton is
zero.  More precisely, in the worst zero placement a double--double drop
has five nonzero singleton guards, a double--triple drop has three, and the
unique triple--triple drop still has one.

Set

\[
 L(z)=\prod_{r\in{\cal R}}(z-r),\qquad
 U_S(z)=\prod_{s\in S}(z-s),\qquad
 Q_T(z)=\prod_{t\in T}(z+t).                            \tag{6}
\]

The complementary polynomial is

\[
                 A_S(z)=L(z)U_S(z)
                         \prod_{u\in{\cal O}}(z-u)^3.   \tag{7}
\]

It has seven distinct roots, exactly four simple.  The all-order
formal-five theorem gives an exact relation pencil

\[
                         {\cal S}_S\subset\mathbb C[z]_{\le3}. \tag{8}
\]

For every \(P\in{\cal S}_S\), its rational derivative has the form

\[
 { (z+\mu)^5Q_T(z)^2P(z)\over
   L(z)^2U_S(z)^2\displaystyle\prod_{u\in{\cal O}}(z-u)^4}. \tag{9}
\]

At a simple root \(x\in X_S={\cal R}\cup S\), its zero residue is the
Robin row

\[
                         P'(x)+Y_{S,x}P(x)=0,            \tag{10}
\]

where

\[
\begin{aligned}
Y_{S,x}={}&{5\over x+\mu}
 +2\sum_{t\in{\cal D}\cup S}{1\over x+t}
 -2\sum_{y\in X_S\setminus\{x\}}{1\over x-y}\\
 &\hspace{42mm}-4\sum_{u\in{\cal O}}{1\over x-u}.     \tag{11}
\end{aligned}
\]

## 3. The accessory residue sum

Choose a basis \(f,g\) of the cubic pencil and put

\[
 W=fg'-f'g,\qquad V=f'g''-f''g'.                       \tag{12}
\]

Then \(\deg W\le4\), \(\deg V\le2\), and both basis members solve

\[
                         Wy''-W'y'+Vy=0.                \tag{13}
\]

The four points of \(X_S\) are roots of the nonzero Wronskian.  They
saturate its degree, so

\[
                         W=\gamma L U_S,qquad\gamma\ne0. \tag{14}
\]

The roots are therefore simple.  Evaluating (13) there and using (10)
gives \(V(x)=-W'(x)Y_{S,x}\).  Since \(V/W=O(z^{-2})\) at infinity, the
sum of its finite residues is zero.  Hence every two-set \(S\) obeys

\[
                              \sum_{x\in X_S}Y_{S,x}=0. \tag{15}
\]

## 4. The choose-two rectangle

Let \(\epsilon_i\) indicate \(a_i\in S\), and call the left side of
(15) \(E(S)\).  The simple-root interactions in (11) cancel in opposite
ordered pairs.  Terms involving \(\mu\), the fixed doubles, or the fixed
singletons are constant or linear in the indicators.  For two selected
triple values, the plus-pole terms contribute

\[
                         {4\epsilon_i\epsilon_j\over a_i+a_j}. \tag{16}
\]

For a selected/outside pair, the two possible orientations sum to

\[
 -4\left({\epsilon_i(1-\epsilon_j)\over a_i-a_j}
 +{\epsilon_j(1-\epsilon_i)\over a_j-a_i}\right)
 =-{4(\epsilon_i-\epsilon_j)\over a_i-a_j},             \tag{17}
\]

which is linear.  Therefore

\[
 E(S)=C+\sum_i A_i\epsilon_i
       +4\sum_{i<j}{\epsilon_i\epsilon_j\over a_i+a_j}. \tag{18}
\]

For distinct \(a,b,c,d\in{\cal A}\), take the alternating rectangle on
the two-sets \(\{a,c\},\{a,d\},\{b,c\},\{b,d\}\).  Equations
(15) and (18) give

\[
0={4(a-b)(c-d)(a+b+c+d)\over
       (a+c)(a+d)(b+c)(b+d)}.                           \tag{19}
\]

All difference and denominator factors are nonzero by distinctness and
the no-opposite hypothesis.  Thus every four of the five triple values
sum to zero.  Comparing the equations obtained by omitting two different
values makes those values equal, a contradiction.  This proves the first
closure in (1).

## 5. The four-triple choose-one moments

For the second profile in (1), write \({\cal A}=\{a_1,a_2,a_3,a_4\}\)
for the triple values, \({\cal D}\) for the four double values, and
\({\cal R}=\{r_1,r_2,r_3\}\) for the original singleton values.  Select
all four doubles and one triple \(a\).  Its simple set is

\[
                              X_a={\cal R}\cup\{a\}.    \tag{20}
\]

The construction in Sections 2--3 applies verbatim: the complement is
\(3^3 1^4\), the relation pencil is cubic, and its Wronskian is a nonzero
multiple of \(\prod_{x\in X_a}(z-x)\).  Here the two universal leading
coefficients of the accessory polynomial provide two additional moments.
Indeed, if the Wronskian is normalized as

\[
 W=z^4+w_3z^3+\cdots,
\]

then a direct cubic-basis calculation gives

\[
                         V=6z^2+3w_3z+v_0.             \tag{21}
\]

Since

\[
 {V(z)\over W(z)}=-\sum_{x\in X_a}{Y_{a,x}\over z-x},
\]

comparison at infinity, using \(w_3=-\sum_{x\in X_a}x\), yields

\[
 \sum_{x\in X_a}Y_{a,x}=0,\qquad
 \sum_{x\in X_a}xY_{a,x}=-6,\qquad
 \sum_{x\in X_a}x^2Y_{a,x}=-3\sum_{x\in X_a}x.        \tag{22}
\]

Let \(\sigma=\sum_{r\in{\cal R}}r\).  At a fixed singleton \(r\), split
its Robin coefficient into a part independent of the selected triple and
the two varying interactions:

\[
 Y_{a,r}=K_r+{2\over r+a}+{2\over r-a}.                \tag{23}
\]

The last term combines the simple-root interaction \(-2/(r-a)\) with the
restored outside-triple term \(+4/(r-a)\).  Put

\[
 K_j=\sum_{r\in{\cal R}}r^jK_r,qquad
 p(a)=\sum_{r\in{\cal R}}{1\over r+a}.                 \tag{24}
\]

If \(M_j(a)=\sum_{x\in X_a}x^jY_{a,x}\), the selected-root term cancels
from \(M_1-aM_0\) and \(M_2-aM_1\).  Equation (23) gives exactly

\[
\begin{aligned}
 M_1-aM_0&=K_1-aK_0+12-4ap(a),\\
 M_2-aM_1&=K_2-aK_1+4\sigma-12a+4a^2p(a).             \tag{25}
\end{aligned}
\]

Substitute the three moment values (22).  The first line gives
\(4ap(a)=K_1-aK_0+18\).  Eliminating \(p(a)\) from the second gives

\[
                         K_0a^2-3a-K_2-7\sigma=0.      \tag{26}
\]

All four distinct triple values satisfy the same polynomial (26).  It has
degree at most two and is nonzero because its linear coefficient is
\(-3\).  This contradiction proves the second closure in (1).

## 6. Exact audit

[verify_live_three_zero_eighth_split_k5_five_triple_saturated_cubic_robin_rectangle_closure.py](../computations/verify_live_three_zero_eighth_split_k5_five_triple_saturated_cubic_robin_rectangle_closure.py)
isolates all four open five-triple profiles, inventories all 84 formal
choices and 3,240 core/zero scenarios, and proves that the first profile
in (1) is their unique saturated case.  It audits all 140 pair-drop cores
for the fourteen saturated pencils, checks (9)--(15), symbolically reduces
the complete Robin rectangle to (19), derives the universal accessory
moments (22), and verifies the choose-one elimination (23)--(26).
