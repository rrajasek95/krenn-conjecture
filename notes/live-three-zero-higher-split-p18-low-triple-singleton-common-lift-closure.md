# Higher splits: the complete \(p=18\) low-triple common-lift closure

## 1. Result

On the no-extra-singular live-three-zero stratum, put

\[
                         p=h+k=18,\qquad 13\le h\le17.          \tag{1}
\]

Every equality profile with at most one triple value is impossible:

\[
\boxed{
\begin{aligned}
 &3\,2^b1^{h+17-2b} &&(0\le b\le9),\\
 &2^b1^{h+20-2b}    &&(1\le b\le11).
\end{aligned}}                                               \tag{2}
\]

For twenty of these families, fix all but one selected singleton.  Moving
the last singleton \(q\) transports
the saturated relation three-space by

\[
                         f_q(z)=(z-q)^2(z+q)                    \tag{3}
\]

into one common low-degree kernel.  Simple complementary values give
exact first-order rows, complementary doubles give exact second-order
rows, and the fixed complementary triple in the first line of (2) gives
an exact third-order row.  Their Wronskian cost forces the common kernel
to equal every transported three-space.  Coprime cubic divisibility closes
all but the endpoint \(3\,2^9 1^{h-1}\); at that endpoint the common space
is the full space of quadratic multiples of two cubics, which cannot obey
even one of its seven exact second-order rows.

For the last profile \(2^{11}1^{h-2}\), fix one selected double and move
the other.  Ten quintic lifts lie in a common degree-ten kernel.  Its
Wronskian bound and the pairwise intersections of the lifted three-spaces
force every pairwise quintic product into the kernel.  At any third double,
the resulting complete graph of exact second-order equations would put
seven distinct double values in one fibre of a degree-two rational map.

Together with the previously closed twenty-nine families having at least
two triples, (2) completes all fifty \(p=18\) equality profiles.

All structural conventions are retained: repeated values are nonzero,
distinct exceptional values are distinct and nonopposite, every exceptional
value is separated from the common pole, and at most one singleton value is
zero.

## 2. The common singleton lift

Write the profile as

\[
                         3^a2^b1^{h+20-3a-2b},\qquad a\in\{0,1\}. \tag{4}
\]

For now take \(0\le b\le9\) if \(a=1\), and \(1\le b\le10\) if
\(a=0\).  Choose

\[
 d=\min(b,2),\qquad s=h+2-2d                              \tag{5}
\]

double classes in role two and singleton layers in role one, respectively.
Fix \(s-1\) selected singletons and call the remaining singleton pool
\(P\).  For each \(q\in P\), use \(q\) as the last selected singleton.
The complementary truncated mass is eighteen.  Put \(R=b-d\), the number
of complementary doubles.  The exact counts are

\[
\begin{array}{c|c|c|c|c}
a&b&|P|&R&N\\ \hline
1&0,1&16&0&15\\
1&2,\ldots,9&20-2b&b-2&17-b\\
0&1&19&0&17\\
0&2,\ldots,10&23-2b&b-2&19-b.
\end{array}                                                   \tag{6}
\]

After selecting \(q\), the saturated complementary relation space is

\[
                         {\cal S}_q\subseteq
                \mathbb C[z]_{\le N-3},\qquad\dim{\cal S}_q=3. \tag{7}
\]

Indeed, if the complement has \(c\) value classes, then
\(N-3=c-4\).  Remove the last singleton selection while retaining all
fixed selected layers.  This is only a regular-unit normalization, not a
claim that the smaller selection is formal.  It gives common exact rows

\[
 \begin{array}{rll}
  J_r(T)&=(U_rT)'(r),&r\in P,\\
  J_v(T)&=(U_vT)''(v),&v\in V,\\
  J_x(T)&=(U_xT)'''(x),&a=1,
 \end{array}                                                   \tag{8}
\]

where \(V\) is the complementary-double set and \(x\) is the unique
triple value.  Every displayed \(U\) is regular and nonzero at its named
point.  This follows directly from common-pole separation, distinctness,
and nonopposition; it remains true when one singleton is zero because all
repeated values are nonzero.

The exact regular-unit quotient between the selection using \(q\) and
the baseline is (3).  Thus, for every complementary value \(y\ne q\) and
the corresponding order \(m\in\{1,2,3\}\), the product rule gives

\[
       (U_y f_qS)^{(m)}(y)
           =(U_y^{(q)}S)^{(m)}(y)=0.                         \tag{9}
\]

Here the equality can harmlessly differ by a fixed nonzero normalization
scalar.  At \(y=q\), the square \((z-q)^2\) kills the value and first
derivative required by the baseline simple row.  At every other named
point, \(f_q\) is a unit: structural nonopposition excludes both roots
\(q\) and \(-q\).  Consequently

\[
 {\cal T}_q:=f_q{\cal S}_q\subseteq{\cal K}\subseteq
                 \mathbb C[z]_{\le N},\qquad\dim{\cal T}_q=3, \tag{10}
\]

where \({\cal K}\) is the common kernel of all rows in (8).

If \(q=0\), then \(f_q=z^3\), which only strengthens the vanishing at the
simple baseline row.  If zero belongs to the fixed selected set instead,
it appears in none of the common rows.  Thus (9)--(10) cover both possible
placements of the unique zero singleton without division by its value.

## 3. Wronskian forcing and the common divisor

Put \(D=\dim{\cal K}\).  An exact order-\(m\) row has nonzero highest-jet
coefficient, so the \((m+1)\)-jet image of \({\cal K}\) has rank at most
\(m\).  Its local Wronskian weight is therefore at least \(D-m\) when
\(D\ge m\).  Equations (6), (8), and the degree-\(N\) Wronskian cap give

\[
 |P|(D-1)+R(D-2)+a(D-3)\le D(N+1-D).                    \tag{11}
\]

For every row in (6), (11) simplifies exactly to

\[
                              D^2+D\le19.                       \tag{12}
\]

Since (10) gives \(D\ge3\), while (12) excludes \(D=4\), one has

\[
                              \boxed{D=3}.                       \tag{13}
\]

Thus \({\cal K}={\cal T}_q\) for every \(q\in P\), and every member of
\({\cal K}\) is divisible by

\[
                              F_P(z)=\prod_{q\in P}f_q(z).       \tag{14}
\]

The factors are pairwise coprime.  Indeed their root sets are
\(\{q,-q\}\), with the appropriate multiplicities, and distinct pool
values are neither equal nor opposite; \(f_0=z^3\) is also coprime to
every nonzero pool factor.  Hence the degree-at-most-\(N\) multiples of
(14) have dimension

\[
                         \max\{N-3|P|+1,0\}.                    \tag{15}
\]

This is less than three for every zero-triple row \(1\le b\le10\), and
for every one-triple row \(0\le b\le8\).  That contradicts (13).

The fixed triple row is essential in this uniform count.  Omitting it
would give only \(D^2\le16\) in the one-triple branch and leave an
artificial four-dimensional case.

## 4. The one-triple endpoint

It remains within the first line of (2) to treat \(b=9\).  Here

\[
                   |P|=2,\qquad R=7,\qquad N=8.                 \tag{16}
\]

Write \(P=\{q_1,q_2\}\).  Equation (13) and the two equalities
\({\cal K}={\cal T}_{q_i}\) show that every member of \({\cal K}\) is
divisible by \(f_{q_1}f_{q_2}\).  The space of its degree-at-most-eight
multiples is already three-dimensional, so

\[
             {\cal K}=f_{q_1}f_{q_2}\mathbb C[z]_{\le2}.       \tag{17}
\]

Choose any of the seven complementary double values \(v\).  It is
nonzero and is neither equal nor opposite to either \(q_i\).  The common
second-order row at \(v\) is

\[
                             J_v(T)=(U_vT)''(v),
                             \qquad U_v(v)\ne0.                 \tag{18}
\]

But the member

\[
                  T(z)=f_{q_1}(z)f_{q_2}(z)(z-v)^2\in{\cal K} \tag{19}
\]

has

\[
                  J_v(T)=2U_v(v)f_{q_1}(v)f_{q_2}(v)\ne0,      \tag{20}
\]

contradicting (18).  This closes every one-triple family.

## 5. The eleven-double endpoint

The only profile not covered above is

\[
                              2^{11}1^{h-2}.                     \tag{21}
\]

Let \({\mathscr D}\) be its eleven-element set of double values and let
\(Y\) be its singleton set.  For every pair \(\{i,j\}\subset{\mathscr D}\),
select those two doubles in role two and all \(h-2\) singleton layers in
role one.  The complement is \(2^9\), so saturation gives

\[
              {\cal S}_{i,j}\subseteq\mathbb C[z]_{\le5},
              \qquad\dim{\cal S}_{i,j}=3.                      \tag{22}
\]

Fix \(i\in{\mathscr D}\).  Retain only \(i\) and all singleton layers in
the baseline normalization, and put

\[
 g_j(z)=(z-j)^3(z+j)^2,
 \qquad
 U_{v,i}(z)=
 { (z+\mu)^k(z+i)^2\displaystyle\prod_{y\in Y}(z+y)
  \over
   \displaystyle\prod_{w\in{\mathscr D}\setminus\{i,v\}}(z-w)^3}.
                                                                    \tag{23}
\]

For \(v\ne i\), the second expression is regular and nonzero at \(v\).
Every denominator factor is nonzero because the double values are
distinct; every numerator factor is nonzero by common-pole separation and
nonopposition.  This includes a possible zero singleton, since \(v\ne0\).
Define

\[
 {\cal K}_i=\bigcap_{v\in{\mathscr D}\setminus\{i\}}
       \ker J_{v,i}\subseteq\mathbb C[z]_{\le10},
 \qquad J_{v,i}(T)=(U_{v,i}T)''(v).                         \tag{24}
\]

For the formal selection \(\{i,j\}\), the regular unit at every
\(v\notin\{i,j\}\) is exactly \(g_jU_{v,i}\).  At \(v=j\), the cube
\((z-j)^3\) kills the complete two-jet.  Hence the division-free product
rule gives

\[
              {\cal T}_{i,j}:=g_j{\cal S}_{i,j}
                    \subseteq{\cal K}_i,
              \qquad\dim{\cal T}_{i,j}=3.                       \tag{25}
\]

The unit \(U_{v,i}\) in (24) depends only on the fixed baseline \(i\) and
the tested value \(v\); crucially, it is independent of both moving
partners \(j,k\).

### 5.1 Pairwise products fill all intersections

Put \(D_i=\dim{\cal K}_i\).  The ten exact order-two rows give

\[
                         10(D_i-2)\le D_i(11-D_i).               \tag{26}
\]

Thus \(D_i\le5\).  For distinct \(j,k\ne i\), the quintics \(g_j,g_k\)
are coprime by nonopposition, and therefore

\[
 g_j\mathbb C[z]_{\le5}\cap g_k\mathbb C[z]_{\le5}
                         =\mathbb C\,g_jg_k                     \tag{27}
\]

inside \(\mathbb C[z]_{\le10}\).  If \(D_i\le4\), two three-spaces in
\({\cal K}_i\) would intersect in dimension at least two, contradicting
(27).  Consequently \(D_i=5\), every pairwise intersection in (27) is
the displayed line, and

\[
                         g_jg_k\in{\cal K}_i
                 \qquad(j,k\ne i,\ j\ne k).                    \tag{28}
\]

### 5.2 The exact second-order rows have no such complete graph

Fix \(v\in{\mathscr D}\setminus\{i\}\) and put

\[
                 \Omega={\mathscr D}\setminus\{i,v\},
                 \qquad |\Omega|=9.                            \tag{29}
\]

For distinct \(j,k\in\Omega\), equations (24) and (28) give

\[
                         (U_{v,i}g_jg_k)''(v)=0.                \tag{30}
\]

All three factors in the undifferentiated product are nonzero at \(v\).
With the same fixed baseline unit \(U=U_{v,i}\), define

\[
 \begin{aligned}
 A_j&={g_j'(v)\over g_j(v)},\\
 B_j&={g_j''(v)\over g_j(v)}
                +2{U'(v)\over U(v)}A_j,\\
 C&={U''(v)\over U(v)}.
 \end{aligned}                                                \tag{31}
\]

Dividing (30) by \(U(v)g_j(v)g_k(v)\) and using the product rule yields

\[
                         C+B_j+B_k+2A_jA_k=0                   \tag{32}
\]

for every distinct pair \(j,k\in\Omega\).  For distinct \(j,k,\ell\),
subtracting the equations for \((j,k)\) and \((j,\ell)\) gives

\[
                   B_k-B_\ell+2A_j(A_k-A_\ell)=0.             \tag{33}
\]

The first logarithmic jet is the explicit rational map

\[
 A_x={3\over v-x}+{2\over v+x}
                    ={5v+x\over v^2-x^2}.                      \tag{34}
\]

Every fibre of (34) has at most two points on the structurally allowed
domain \(x\ne\pm v\): the equation \(A_x=c\) is the nonzero polynomial

\[
                     c(v^2-x^2)-(5v+x)=0                       \tag{35}
\]

of degree at most two, whose coefficient of \(x\) is \(-1\).

If \(A_k\ne A_\ell\) for some pair in \(\Omega\), equation (33) makes
all seven values \(A_j\), \(j\in\Omega\setminus\{k,\ell\}\), equal,
contradicting (35).  If there is no such pair, all nine values \(A_j\)
are equal, again contradicting (35).  This proves (21) impossible.

## 6. Exact audit and ledger consequence

[verify_live_three_zero_higher_split_p18_low_triple_singleton_common_lift_closure.py](../computations/verify_live_three_zero_higher_split_p18_low_triple_singleton_common_lift_closure.py)
reconstructs every singleton-lift selection count, complementary mass and
relation degree; checks the three row orders and all Wronskian inequalities;
verifies the common-divisor dimensions and the \(b=9\) equality space;
checks the eleven-double quintic intersections and exact product-rule
normalization; verifies the degree-two fibre map symbolically; and
reconstructs the completed fifty-family \(p=18\) ledger.
