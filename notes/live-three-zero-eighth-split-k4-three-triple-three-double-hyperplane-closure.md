# The eighth split: three-double cubic-hyperplane closure

## 1. Result

At \((h,k)=(8,4)\), the collision profile

\[
                         3^3 2^3 1^7                    \tag{1}
\]

is impossible on the no-extra-singular stratum.

Fix one double value at formal role two and all seven singleton values at
formal role one.  The eight one-drop lifts span the exact
three-dimensional kernel in \(\mathbb C[z]_{\le7}\).  The three relations
among its eight value rows dualize injectively to a hyperplane in the
cubics.  Both outside-double residue rows have this same hyperplane as
their kernel.

There are three possible choices of the formal double.  Compatibility of
the two outside-double rows across those three choices forces, for the
three double values \(x,y,z\),

\[
 x^2+yz=5x(y+z),\qquad
 y^2+xz=5y(x+z),\qquad
 z^2+xy=5z(x+y).                                      \tag{2}
\]

Subtracting two equations makes distinct double values impossible.

## 2. The one-double/seven-singleton kernel

Write \({\cal A}=\{a,b,c\}\) for the triple values,
\({\cal V}=\{x,y,z\}\) for the double values, and \({\cal R}\) for the
seven singleton values.  Fix \(k\in{\cal V}\), put
\(C_k={\cal V}\setminus\{k\}\), and set

\[
\begin{aligned}
 Q_k(z)&=z+k,& H(z)&=\prod_{r\in{\cal R}}(z+r),\\
 A_k(z)&=\prod_{u\in C_k}(z-u)^2
                   \prod_{t\in{\cal A}}(z-t)^3.        \tag{3}
\end{aligned}
\]

The formal target gives role two to \(k\) and role one to every
singleton, for total role nine.  Lower the double role, or omit one
singleton, to obtain an eight-label core.  The corresponding lifts are

\[
 P_k=(z^2-k^2)q_k,\qquad
 P_r=(z-r)(z+r)^2q_r.                                  \tag{4}
\]

They are nonzero and have degree at most seven.  If a singleton is zero,
only its omitted core may be unavailable; the double drop and the other
six singleton drops remain available.  All available lifts lie in the
common kernel \(K_k\subset\mathbb C[z]_{\le7}\) of the eight value rows
of

\[
 F_P(z)={A_k(z)P(z)\over
              (z+\mu)^5Q_k(z)^3H(z)^2}.                \tag{5}
\]

The numerator degree is at most \(13+7=20\), while the denominator has
degree \(5+3+14=22\), so there is no residue at infinity.

The selected-double row has exact differential order two and the seven
singleton rows have exact order one.  For a \(d\)-dimensional kernel with
unit gcd at those nodes, their Wronskian weight minus the degree cap is

\[
 (d-2)+7(d-1)-d(8-d)=d^2-9.                            \tag{6}
\]

Every gcd correction is stricter: a basepoint at an order-one node has
order at least two, while a basepoint absorbed at the order-two node has
order at least three; the intermediate orders leave a nonzero reduced
local functional.  Hence \(\dim K_k\le3\).

The available lifts span at least three dimensions.  A line would have a
degree-seven generator divisible by all their pairwise-coprime quadratic
or cubic lift factors.  If they spanned a pencil, its parity determinant
would be odd of degree at most thirteen and vanish at zero and at both
signs of at least seven nonzero layer values.  It would therefore vanish
identically, so after removing the gcd the pencil would be even.  If
\(N=7\) singleton drops are available, or \(N=6\) when a zero drop is
missing, and \(m\) of their values are absorbed by the gcd, the
singleton double zeros in the squared variable would require

\[
 N-m\le
 2\left(\left\lfloor{7-m\over2}\right\rfloor-1\right). \tag{7}
\]

For \(N=7\) the two sides, for \(m=0,\ldots,5\), are
\((7,6,5,4,3,2)\) and \((4,4,2,2,0,0)\); for \(N=6\) they are
\((6,5,4,3,2,1)\) and the same right side.  Every comparison is strict,
and larger \(m\) leaves no pencil.  Thus

\[
                         \dim K_k=3.                    \tag{8}
\]

## 3. The cubic relation hyperplane

The eight value rows on the eight-dimensional space
\(\mathbb C[z]_{\le7}\) have rank five, hence three relations.  A relation
has a principal-part numerator

\[
 {N(z)\over Q_k(z)^3H(z)^2},\qquad \deg N\le8,          \tag{9}
\]

and distinct pole supports make the relation-to-\(N\) map injective.
Divide by (5):

\[
                         G_N(z)={(z+\mu)^5N(z)\over A_k(z)}. \tag{10}
\]

Put

\[
 g_k=\prod_{u\in C_k}(z-u)\prod_{t\in{\cal A}}(z-t)^2,
 \qquad R_k={A_k\over g_k},\qquad D_k={A_k'\over g_k}. \tag{11}
\]

Here \(\deg R_k=5\), \(\deg D_k=4\), and \(D_k\) has leading coefficient
thirteen.  Direct differentiation gives

\[
 G_N'={(z+\mu)^4g_k\over A_k^2}\,{\cal E}_k(N),         \tag{12}
\]

where

\[
 {\cal E}_k(N)=
 R_k\bigl((z+\mu)N'+5N\bigr)-(z+\mu)D_kN.              \tag{13}
\]

For \(n=\deg N\le8\), the nominal leading coefficient in (13) is
\(n+5-13=n-8\).  It cancels at \(n=8\), so
\(\deg{\cal E}_k(N)\le12\).  The order-three contact at \(-k\) and the
seven order-two contacts at the singleton poles give

\[
                    {\cal E}_k(N)=Q_k^2H\,S_N,
                         \qquad S_N\in\mathbb C[z]_{\le3}. \tag{14}
\]

This map is injective.  A zero image would make \(G_N\) constant, and
evaluation of \((z+\mu)^5N=\gamma A_k\) at \(-\mu\) gives
\(\gamma=N=0\).  The three relation numerators therefore map onto a
cubic hyperplane

\[
                         {\cal S}_k\subset\mathbb C[z]_{\le3}. \tag{15}
\]

Every member occurs in

\[
 G_S'=
 { (z+\mu)^4(z+k)^2H(z)S(z)\over
   \displaystyle\prod_{u\in C_k}(z-u)^3
             \prod_{t\in{\cal A}}(z-t)^4}.             \tag{16}
\]

At an outside double \(u\in C_k\), remove the factor
\((z-u)^{-3}\) from (16) and call the remaining unit \(B_u^{(k)}(z)\).
Zero residue is the nonzero row

\[
                         L_u^{(k)}(S)
                         =\bigl(B_u^{(k)}S\bigr)''(u)=0. \tag{17}
\]

Its kernel is a hyperplane containing (15), hence equals
\({\cal S}_k\).  Thus the two outside-double rows for a fixed \(k\) have
the same kernel.

## 4. A two-row cubic lemma

Let \(u\ne v\), put \(\delta=u-v\), and suppose two normalized
second-order rows on the cubics have one kernel.  Write

\[
 Y_u={B_u'(u)\over B_u(u)},\quad
 Z_u={B_u''(u)\over B_u(u)},\qquad
 Y_v={B_v'(v)\over B_v(v)},\quad
 Z_v={B_v''(v)\over B_v(v)}.                           \tag{18}
\]

Associate to a row its characteristic cubic

\[
 \chi_u(t)={L_u((z-t)^3)\over B_u(u)}
 =(u-t)\{6+6Y_u(u-t)+Z_u(u-t)^2\}.                    \tag{19}
\]

Equal kernels make \(\chi_u,\chi_v\) proportional.  Each row kills its
own anchored cube, and because the kernels agree, it also kills the
other one.  Consequently

\[
 Z_u\delta^2=-6(1+\delta Y_u),\qquad
 Z_v\delta^2= 6(\delta Y_v-1).                         \tag{20}
\]

After using (20), the two cubics factor as \(s(s-\delta)\) times two
linear polynomials, with \(s=u-t\).  Proportionality of those linear
factors gives, without dividing by either \(Z\),

\[
                         \delta^2Z_uZ_v=6(Z_u+Z_v).     \tag{21}
\]

Put \(p=\delta Y_u\), \(q=\delta Y_v\).  Substitution of (20) into
(21) yields the division-free invariant

\[
                         pq+2q-2p-3=0.                 \tag{22}
\]

## 5. Compatibility of the three formal choices

For a double value \(u\), remove all double-dependent factors from
\(B_u^{(k)}\) and denote the first two logarithmic jets of the remaining
unit by \(F_u,G_u\).  If \(k\) is formal and \(v\) is the other outside
double, then

\[
\begin{aligned}
Y_u^{(k)}&=F_u+{2\over u+k}-{3\over u-v},\\
Z_u^{(k)}&=(Y_u^{(k)})^2+G_u-{2\over(u+k)^2}
                                  +{3\over(u-v)^2}.     \tag{23}
\end{aligned}
\]

Use the first equation of (20) once with \(k\) formal and \(v\) outside,
and once with \(v\) formal and \(k\) outside.  Both expressions contain
the same \(G_u\).  Subtraction and exact factorization give

\[
 2F_u(u+v)(u+k)+2u+v+k=0,
\]

so, using the nonopposite hypotheses,

\[
                         F_u=-{1\over2}
             \left({1\over u+v}+{1\over u+k}\right).   \tag{24}
\]

Now fix formal \(k\) and outside doubles \(u,v\).  Substitute (23)--(24)
into (22).  Clearing only the structurally nonzero factors
\((u-v)^2(u+v)^2(u+k)(v+k)\) leaves

\[
                         k^2+uv-5k(u+v)=0.              \tag{25}
\]

Applying (25) with \(k=x,y,z\) gives (2).  The difference of its first
two equations is

\[
                         (x-y)(x+y-6z)=0.               \tag{26}
\]

Distinctness gives \(x+y=6z\).  Cyclically,
\(x+z=6y\); subtracting these two identities yields \(7(y-z)=0\).
This contradicts distinctness in characteristic zero and proves (1).

## 6. Exact audit

[verify_live_three_zero_eighth_split_k4_three_triple_three_double_hyperplane_closure.py](../computations/verify_live_three_zero_eighth_split_k4_three_triple_three_double_hyperplane_closure.py)
checks every formal core, all lift and dual degrees, the sharp
three-dimensional kernel including the possible zero singleton, the
leading-coefficient cancellation, the two-row characteristic-cubic
lemma including \(Z=0\), the exact baseline-jet subtraction, and the
three-double contradiction.
