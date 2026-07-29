# The eighth split: four-triple single-double pair-drop closure

## 1. Result

At \((h,k)=(8,4)\), the collision profile

\[
                         3^4 2\,1^8                    \tag{1}
\]

is impossible on the no-extra-singular stratum.

The repeated exceptional values are structurally nonzero.  The value
classes are distinct and pairwise nonopposite, and at most one singleton
value is zero.

Give the double value formal role two and all eight singleton values
formal role one.  Lowering any pair of the nine formal layers produces
36 legal eight-label cores.  Their lifts lie in
\(\mathbb C[z]_{\le10}\).  A mixed parity argument shows that they span
at least four dimensions, while the nine exact value rows bound their
common kernel by four.

The nine rows consequently have two relations.  Duality maps those
relations injectively into polynomials of degree zero.  A
two-dimensional space cannot inject into the constants, giving the
contradiction.

## 2. Nine formal layers and 36 pair drops

Write \({\cal A}=\{a,b,c,d\}\) for the four triple values, \(x\) for the
double value, and \({\cal R}\) for the eight singleton values.  Put

\[
 Q(z)=z+x,\qquad H(z)=\prod_{r\in{\cal R}}(z+r),\qquad
 A(z)=\prod_{t\in{\cal A}}(z-t)^3.                     \tag{2}
\]

The formal target has total role \(2+8=10\).  Lower any two distinct
layers.  If one is the double and one a singleton, the core selects one
double label and seven singleton labels.  If both are singletons, it
selects both double labels and six singleton labels.  In the first case
the nonzero double mate remains; in the second case two singleton classes
remain, at least one nonzero.  Thus all \(\binom92=36\) cores are legal,
including when one singleton value is zero.

Use the lift factors

\[
                         f_x=z^2-x^2,\qquad
                         f_r=(z-r)(z+r)^2.              \tag{3}
\]

For a double--singleton drop the residual degree is at most five and the
two factors have total degree five.  For a two-singleton drop the bounds
are four and six.  Hence every nonzero lift

\[
                         P_{ij}=f_if_jq_{ij}            \tag{4}
\]

has degree at most ten.  The exact lift identities rewrite all 36
rational dependences as

\[
 F_P(z)={A(z)P(z)\over
              (z+\mu)^5Q(z)^3H(z)^2}.                 \tag{5}
\]

The numerator degree is at most \(12+10=22\), while the denominator
degree is \(5+3+16=24\), so \(F_P=O(z^{-2})\).

Let \(K\subset\mathbb C[z]_{\le10}\) be the common kernel of the selected
double row and the eight singleton rows, and let \(W\) be the span of
the lifts.  Then \(W\subseteq K\).

## 3. The kernel has dimension at most four

The double row has exact differential order two and each singleton row
has exact order one.  With unit gcd, a \(d\)-dimensional kernel has
forced Wronskian weight

\[
                         (d-2)+8(d-1)=9d-10,            \tag{6}
\]

while the degree cap in \(\mathbb C[z]_{\le10}\) is \(d(11-d)\).
Their difference is

\[
                         d^2-2d-10,                    \tag{7}
\]

which is positive for \(d\ge5\).  A simple gcd root at the order-two
node increases the deficit by \(d+1\); absorption there requires order
at least three and increases it by at least \(2d+2\).  Absorbing an
order-one node requires gcd order at least two and increases the deficit
by \(d+1\).  Other gcd roots only lower the cap.  Thus

\[
                         \dim K\le4.                    \tag{8}
\]

## 4. The pair-drop lifts span at least four dimensions

The nine factors in (3) are pairwise coprime.  For each layer \(i\), put

\[
                         U_i=W\cap f_i\mathbb C[z].     \tag{9}
\]

Every pair \(U_i,U_j\) has a nonzero intersection containing \(P_{ij}\).
No \(U_i\) can be a line: all eight \(P_{ij}\), \(j\ne i\), would then
be scalar multiples of one generator, and pairwise coprimality would
make the product of all nine factors divide that degree-ten polynomial.
Hence every \(U_i\) has dimension at least two.  This already excludes
\(\dim W\le2\), since in a plane all \(U_i\) would equal \(W\), again
making every member divisible by the degree-26 product of the factors.

Suppose \(\dim W=3\), and choose a basis
\({\bf P}=(P_0,P_1,P_2)\).  Every \(U_i\) has dimension at least two, so
the evaluation vectors \({\bf P}(v)\) and \({\bf P}(-v)\) are
proportional at each nonzero layer value \(v\).  The three parity minors

\[
 P_i(z)P_j(-z)-P_i(-z)P_j(z)                           \tag{10}
\]

are odd of degree at most nineteen.  If no singleton is zero, they vanish
at zero and at both signs of all nine layer values.  If a singleton is
zero, its cubic factor gives order at least three at zero, while the
other eight values give sixteen further roots.  In both cases every
minor is a scalar multiple of one fixed degree-nineteen odd polynomial.
Writing the three minors as
\({\bf P}(z)\mathbin\times{\bf P}(-z)=D(z){\bf c}\), a nonzero constant
vector \({\bf c}\) would give a constant linear relation among the basis
polynomials.  Hence all minors vanish.

After removing the gcd \(G\), the primitive three-space is therefore
even:

\[
                         W=G(z){\cal E}(z^2),\qquad
                         \dim{\cal E}=3.                \tag{11}
\]

Put \(g=\deg G\), and let \(m\) count singleton values whose negative
node is absorbed by \(G\).  Then \(g\ge m\), and the square-variable
degree is at most \(\lfloor(10-m)/2\rfloor\).  At each of the other
\(8-m\) singleton values, two independent special members have a double
zero in the square variable, forcing Wronskian weight at least two.
Thus one would need

\[
 2(8-m)\le
 3\left(\left\lfloor{10-m\over2}\right\rfloor-2\right). \tag{12}
\]

For \(m=0,\ldots,6\), the left sides are
\((16,14,12,10,8,6,4)\), while the right sides are
\((9,6,6,3,3,0,0)\).  Every comparison is strict; for \(m\ge7\) the
degree cap cannot contain a three-space.  Therefore \(\dim W\ne3\).
Together with (8),

\[
                         W=K,\qquad\dim K=4.            \tag{13}
\]

## 5. Two relations cannot inject into constants

The nine value rows act on the eleven-dimensional space
\(\mathbb C[z]_{\le10}\).  Equation (13) makes their rank seven, so their
relation space has dimension two.  A relation gives a sum of principal
parts

\[
 {N(z)\over Q(z)^3H(z)^2},\qquad \deg N\le7.            \tag{14}
\]

Indeed, the denominator has degree nineteen and annihilation of
\(1,z,\ldots,z^{10}\) gives order at least twelve at infinity.  Distinct
pole supports make the relation-to-\(N\) map injective.

Divide by (5):

\[
                         G_N(z)={(z+\mu)^5N(z)\over A(z)}. \tag{15}
\]

Set

\[
 g_A=\prod_{t\in{\cal A}}(z-t)^2,\qquad
 R_A={A\over g_A},\qquad D_A={A'\over g_A}.             \tag{16}
\]

Then \(\deg R_A=4\), \(\deg D_A=3\), and the leading coefficient of
\(D_A\) is twelve.  Differentiation gives

\[
 G_N'={(z+\mu)^4g_A\over A^2}\,{\cal E}_A(N),           \tag{17}
\]

where

\[
 {\cal E}_A(N)=R_A\bigl((z+\mu)N'+5N\bigr)
                         -(z+\mu)D_AN.                 \tag{18}
\]

For \(n=\deg N\le7\), the nominal leading coefficient is
\(n+5-12=n-7\), so it cancels at \(n=7\); for smaller \(n\), the degree
is already at most ten.  Hence

\[
                         \deg{\cal E}_A(N)\le10.        \tag{19}
\]

The order-three contact at the selected double and order-two contact at
all eight singleton poles imply

\[
                         {\cal E}_A(N)=\gamma_NQ^2H,    \tag{20}
\]

because \(\deg(Q^2H)=2+8=10\).  The map \(N\mapsto\gamma_N\) is
injective: if \(\gamma_N=0\), then \(G_N\) is constant, and evaluation
of \((z+\mu)^5N=\gamma A\) at \(-\mu\) gives \(\gamma=N=0\).

Thus the two-dimensional relation space injects into the
one-dimensional constants, an impossibility.  This proves (1).

## 6. Exact audit

[verify_live_three_zero_eighth_split_k4_four_triple_single_double_pair_drop_closure.py](../computations/verify_live_three_zero_eighth_split_k4_four_triple_single_double_pair_drop_closure.py)
checks all 36 legal cores and both lift degrees, every gcd correction,
the exact degree-nineteen parity boundary including a zero singleton,
the reduced square-variable Wronskian table, the two relation counts,
the leading cancellation, and the final injection into constants.
