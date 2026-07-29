# Higher splits: the (C=8) singleton pair-line clique closure at (p=19)

## 1. Result

The only no-quartic (p=19) profile left after the large-pool
singleton closures is

\[
                         \boxed{2^{10}1^{h+1}}.                \tag{1}
\]

In the \((e;a,b,u)\) notation it is \((0;0,10,1)\).  Its
moving-singleton realization has pool size four and eight fixed double
classes, so it is the isolated \(C=8\) endpoint.  The degree-five
secant curve of that realization need not be developable: an exact
double row does not, by itself, give another zero of the secant second
fundamental determinant.  A different selection closes the endpoint.

**Theorem 1.1 (singleton pair-line clique).**  Profile (1) cannot occur
on the no-extra-singular live-three-zero stratum.

Select one double rather than two.  The ten resulting quintic lifts lie
in one degree-eleven kernel.  Every two lifted three-spaces meet in an
intrinsic quintic-pair line.  The one complementary singleton determines
the linear factor on that line.  At any tested double, the exact
second-order row then gives a bidegree-\((6,6)\) equation on a nine-vertex
clique.  Interpolation makes the equation an identity, while its exact
double-pole coefficient has a nonzero linear term.

Together with the independently established \(C=7\) and five-triple
closures, Theorem 1.1 closes the last of the ninety-four \(p=19\)
boundary families.

## 2. One selected double and the common undecic kernel

Let \({\mathscr D}\) be the ten-element set of exact-double values.
Choose one of the \(h+1\) singleton values and call it \(r\); select the
other \(h\) singleton layers.  For each \(i\in{\mathscr D}\), also
select the double class \(i\) in formal role two.  The formal complement
is

\[
                              2^9 1.                         \tag{2}
\]

The selected polynomial ambient degree is \(h+2\), and legal pair drops
give a four-dimensional subspace of the selected-row kernel.  The
selected \(q=6\) Wronskian gap is

\[
              22-h+\max(0,6-k)=9>0,\qquad h+k=19,             \tag{2a}
\]

so that kernel has dimension at most five.  If it had dimension four,
it would equal the pair-drop span; Sections 4--5 of the audited low-role
selected-lift incidence theorem exclude exactly that conditional
\(q=4\) branch (including the possible missing low-role edge).  Thus the
selected-row kernel is five-dimensional, and its exact relation space is

\[
                 {\cal S}_i\subseteq\mathbb C[z]_{\leq6},
                 \qquad \dim {\cal S}_i=3.                   \tag{3}
\]

Put

\[
                         g_i(z)=(z-i)^3(z+i)^2.               \tag{4}
\]

Remove the selected double while retaining the \(h\) fixed selected
singleton layers.  The baseline complement is \(2^{10}1\).  At a
double value \(v\), its common exact row is

\[
             J_v(T)=(U_vT)''(v),\qquad U_v(v)\ne0,           \tag{5}
\]

and at the singleton it is

\[
             J_r(T)=(U_rT)'(r),\qquad U_r(r)\ne0.            \tag{6}
\]

The units in (5)--(6) belong to this fixed baseline and are independent
of \(i\).  At every row other than \(i\), the quintic (4) is a regular
unit and transports the selected equation exactly.  At \(i\), its
cube kills the complete two-jet.  Thus

\[
 {\cal T}_i:=g_i{\cal S}_i\subseteq {\cal K}
       \subseteq\mathbb C[z]_{\leq11},
       \qquad \dim{\cal T}_i=3,                              \tag{7}
\]

where \({\cal K}\) is the common kernel of the ten rows (5) and the
row (6).

If \(D=\dim{\cal K}\geq6\), the displayed exact rows force Wronskian
weight at least

\[
                    10(D-2)+(D-1)=11D-21,                   \tag{8}
\]

whereas the degree-eleven cap is

\[
                              D(12-D).                       \tag{9}
\]

Their difference is \(D^2-D-21>0\) for \(D\geq6\).  The standard
exact-row gcd correction is nonnegative, so a common factor cannot evade
the inequality.  Hence

                              \dim{\cal K}\leq5.             \tag{10}

## 3. Every pair intersection is an intrinsic line

For distinct \(i,j\in{\mathscr D}\), structural nonopposition makes
\(g_i,g_j\) coprime.  Therefore

\[
 g_i\mathbb C[z]_{\leq6}\cap g_j\mathbb C[z]_{\leq6}
               =g_ig_j\mathbb C[z]_{\leq1}                 \tag{11}
\]

inside degree eleven.

If \(\dim{\cal K}=3\), two three-spaces in it would meet in dimension
three, larger than the two-dimensional ambient intersection (11).  If
\(\dim{\cal K}=4\), their intersection would be the full pencil in
(11).  But the common singleton row (6) cannot annihilate that pencil:
the member

\[
                         g_i(z)g_j(z)(z-r)                    \tag{12}
\]

has \(J_r\)-value \(U_r(r)g_i(r)g_j(r)\ne0\).  All factors are nonzero
by distinctness and nonopposition, including when \(r=0\).  Equations
(7) and (10) therefore give

                              \dim{\cal K}=5.                 \tag{13}

Now two transported three-spaces meet in dimension at least one.  The
same test (12) excludes a two-dimensional intersection, so every pair
has exactly one intrinsic line

\[
 {\cal T}_i\cap{\cal T}_j
     =\langle g_ig_j\ell_{ij}\rangle,
       \qquad0\ne\ell_{ij}\in\mathbb C[z]_{\leq1},
       \qquad\ell_{ij}=\ell_{ji}.                            \tag{14}
\]

The factor \(\ell_{ij}\) cannot vanish at \(r\).  Otherwise its simple
zero would again make (6) nonzero.  Normalize \(\ell_{ij}(r)=1\) and
write

\[
                  \ell_{ij}(z)=1+d_{ij}(z-r).                \tag{15}
\]

Define

\[
 a_x={g_x'(r)\over g_x(r)}
           ={5r+x\over r^2-x^2},
 \qquad
 \Lambda=-{U_r'(r)\over U_r(r)}.                            \tag{16}
\]

Applying the one common row (6) to the generator (14) determines every
linear factor without any division by \(r\):

\[
                         \boxed{d_{ij}=\Lambda-a_i-a_j}.      \tag{17}
\]

## 4. The nine-vertex double-row clique

Fix a tested double \(v\in{\mathscr D}\) and put

\[
                  \Omega={\mathscr D}\setminus\{v\},
                  \qquad |\Omega|=9.                         \tag{18}
\]

For every distinct \(x,y\in\Omega\), the generator in (14) obeys the
same exact second-order row (5) at \(v\).  Set

\[
\begin{aligned}
 A_x&={g_x'(v)\over g_x(v)}={5v+x\over v^2-x^2},\\
 R_x&={g_x''(v)\over g_x(v)}
       ={4(5v^2+2vx-x^2)\over(v^2-x^2)^2},\\
 u&={U_v'(v)\over U_v(v)},\qquad
 c={U_v''(v)\over U_v(v)},\\
 d_{xy}&=\Lambda-a_x-a_y,\\
 P_{xy}&=u+A_x+A_y,\\
 Q_{xy}&=c+R_x+R_y+2u(A_x+A_y)+2A_xA_y.
                                                               \tag{19}
\end{aligned}
\]

Exact product-rule expansion of
\((U_vg_xg_y[1+d_{xy}(z-r)])''(v)=0\) gives

\[
 E(x,y):=Q_{xy}\bigl(1+(v-r)d_{xy}\bigr)
                           +2P_{xy}d_{xy}=0                  \tag{20}
\]

on every off-diagonal pair of \(\Omega\).

Clear the structurally nonzero denominator

\[
 D(x,y)=(r^2-x^2)(r^2-y^2)
           (v^2-x^2)^2(v^2-y^2)^2.                          \tag{21}
\]

Then \(N(x,y)=D(x,y)E(x,y)\) has degree at most six in each
variable.  For fixed \(x\in\Omega\), it has the other eight elements
of \(\Omega\) as roots in \(y\), and hence is identically zero in
\(y\).  Every coefficient, viewed as a degree-at-most-six polynomial in
\(x\), then vanishes at all nine elements of \(\Omega\).  Therefore

                              N(x,y)\equiv0.                  \tag{22}

## 5. The exact pole coefficient is nonzero

Identity (22) is impossible.  The coefficient of the double pole at the
excluded value \(y=v\) is

\[
 \lim_{y\to v}(v-y)^2E(x,y)
       =6\left[1+(v-r)(\Lambda-a_x-a_v)\right].              \tag{23}
\]

It would have to vanish identically in \(x\).  Put

\[
                         K=1+(v-r)(\Lambda-a_v).
\]

After clearing \(r^2-x^2\), equation (23) would become

\[
             K(r^2-x^2)-(v-r)(5r+x)\equiv0.                 \tag{24}
\]

The coefficient of \(x\) in (24) is \(-(v-r)\ne0\), because a double
value and the complementary singleton are distinct value classes.  This
contradicts (22) and proves Theorem 1.1.

## 6. Exact audit

[verify_live_three_zero_higher_split_p19_c8_singleton_pair_line_clique_closure.py](../computations/verify_live_three_zero_higher_split_p19_c8_singleton_pair_line_clique_closure.py)
reconstructs the one-double formal selection for every higher split,
checks the relation and transport degrees, audits every common-kernel
dimension branch and the singleton exclusion of a full pair pencil,
derives the logarithmic jets and the exact bidegree-six numerator,
verifies the nine-vertex interpolation thresholds, and checks the
double-pole obstruction (23)--(24).
