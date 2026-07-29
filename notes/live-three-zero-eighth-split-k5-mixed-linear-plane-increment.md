# The eighth split at \(k=5\): two mixed linear-plane closures

## 1. Result

On the no-extra-singular \((h,k)=(8,5)\) stratum, neither of the
collision profiles

\[
             3^3 2^4 1^6,\qquad 3^4 2\,1^9                 \tag{1}
\]

can occur.  Both contradictions come from the same exact pair-drop
construction.  In the first profile select two double layers and all six
singleton layers.  In the second select the unique double layer and any
eight of the nine singleton layers.  The selected rows have a common
four-dimensional polynomial kernel; their two relations identify with
all linear polynomials.  An outside double in the first case gives a
quadratic-fibre obstruction, while the outside singleton in the second
case gives an immediate nonzero-unit contradiction.

Repeated exceptional values are nonzero, distinct exceptional classes
are pairwise nonopposite, and at most one singleton value is zero.  These
are the standing structural facts on this stratum.

## 2. The two exact pair-drop kernels

We use the following two instances of the mixed parity lemma.  They are
independent of the common-pole order.

**Lemma 2.1.**  Give formal role two to \(d\) distinct double classes and
formal role one to \(s\) distinct singleton classes, where

\[
             (d,s,D)=(2,6,9)\quad\hbox{or}\quad(1,8,10). \tag{2}
\]

Thus \(2d+s=10\).  Suppose every core obtained by lowering two different
formal layers is legal.  Lift a lowered double \(x\) by

\[
                   f_x(z)=z^2-x^2                     \tag{3}
\]

and an omitted singleton \(r\) by

\[
                   f_r(z)=(z-r)(z+r)^2.                \tag{4}
\]

Then all pair-drop lifts lie in \(\mathbb C[z]_{\le D}\), and they span
the exact four-dimensional kernel of the \(d\) order-two and \(s\)
order-one residue rows on that space.

**Proof.**  If \(b\in\{0,1,2\}\) of the two lowered layers are
singletons, their lift factors have total degree \(4+b\).  In the
\((2,6)\) case the core represents \(8-b\) classes, so its nonzero
Hermite residual has degree at most \(5-b\).  In the \((1,8)\) case
necessarily \(b=1,2\); the corresponding bounds are \(6-b\) and
\(4+b\).  Hence the total degree is respectively \(9\) and \(10\).

Let \(K\) be the common row kernel and let \(e=\dim K\).  With unit gcd,
the forced Wronskian weight minus the degree cap is, in both cases,

\[
 d(e-2)+s(e-1)-e(D+1-e)=e^2-2e-10.                   \tag{5}
\]

This is positive for \(e\ge5\).  A simple gcd zero at an order-two node
adds \(e+1\) to this deficit, absorption of that node adds at least
\(2e+2\), and absorption of an order-one node adds \(e+1\).  A gcd zero
elsewhere only lowers the degree cap.  Thus \(\dim K\le4\).

Let \(W\) be the pair-drop span and put
\(U_i=W\cap f_i\mathbb C[z]\) for each formal layer.  Pairwise
coprimality gives \(U_i\cap U_j\ne0\).  No \(U_i\) is a line: otherwise
all lifts through \(i\) would be proportional and the product of all
the other coprime factors would divide one polynomial of degree at most
\(D\).  This excludes \(\dim W\le2\).

If \(\dim W=3\), the three parity minors of a basis are odd of degree at
most \(2D-1\) and vanish at zero and at both signs of every formal-layer
value.  If a singleton value is zero, an adapted basis instead supplies
a triple zero at zero and the other opposite pairs.  In either case the
forced divisor has exactly degree \(2D-1\).  The cross-product identity
then makes the primitive three-space projectively even:

\[
                         W=G(z){\cal E}(z^2),
                         \qquad\dim{\cal E}=3.          \tag{6}
\]

If \(m\) singleton nodes are absorbed by \(G\), every other singleton
square has vanishing sequence at least \((0,2,3)\) in \({\cal E}\), and
therefore contributes two to its Wronskian.  Consequently one would need

\[
 2(s-m)\le3\left(\left\lfloor{D-m\over2}\right\rfloor-2\right). \tag{7}
\]

For \((s,D)=(6,9)\), the two sides for \(m=0,\ldots,5\) are

\[
 (12,10,8,6,4,2)\quad\hbox{and}\quad(6,6,3,3,0,0),    \tag{8}
\]

and for \((s,D)=(8,10)\), for \(m=0,\ldots,6\), they are

\[
 (16,14,12,10,8,6,4)\quad\hbox{and}\quad(9,6,6,3,3,0,0). \tag{9}
\]

Every comparison is strict; larger \(m\) leaves square-variable degree
at most one.  Hence \(\dim W\ne3\).  Thus \(W=K\) and both have
dimension four. \(\square\)

## 3. Duality fills the linear polynomials

The two profiles share the following dual calculation.  Let \(Q\) be
the product of the selected double plus-pole factors and \(H\) the
product of the selected singleton plus-pole factors.  Let \(A\) be the
complementary polynomial after the full formal role-ten selection.  In
both cases

\[
              \deg A=13,\qquad \deg\operatorname{rad}(A)=5. \tag{10}
\]

The rational functions attached to the lifted kernel are

\[
              F_P(z)={A(z)P(z)\over(z+\mu)^6Q(z)^3H(z)^2}. \tag{11}
\]

The numerator degree is two below the denominator degree.  Lemma 2.1
makes the selected-row rank equal to \(D-3\).  Since the number of rows
is \(d+s=D-1\), their relation space has dimension two.

A relation among the principal parts annihilates
\(1,z,\ldots,z^D\).  In either case its numerator has the form

\[
                {N(z)\over Q(z)^3H(z)^2},
                \qquad\deg N\le7.                     \tag{12}
\]

Distinct principal-part supports make the relation-to-\(N\) map
injective.  Put

\[
 g=\prod_{A(a)=0}(z-a)^{\operatorname{ord}_a(A)-1},
 \quad R={A\over g},\quad D_A={A'\over g}.             \tag{13}
\]

Then \(\deg R=5\), \(\deg D_A=4\), and
\(\operatorname{LC}(D_A)=13\).  Direct differentiation gives

\[
 {d\over dz}{(z+\mu)^6N\over A}
 ={(z+\mu)^5g\over A^2}{\cal E}_A(N),                 \tag{14}
\]

where

\[
 {\cal E}_A(N)=R\bigl((z+\mu)N'+6N\bigr)
                   -(z+\mu)D_AN.                      \tag{15}
\]

For \(n=\deg N\le7\), the nominal leading coefficient is

\[
                         n+6-13=n-7.                  \tag{16}
\]

It cancels at \(n=7\), so \(\deg{\cal E}_A(N)\le11\).
Contact at the selected poles gives

\[
                         {\cal E}_A(N)=Q^2H S_N,
                         \qquad S_N\in\mathbb C[z]_{\le1}, \tag{17}
\]

because \(\deg(Q^2H)=2d+s=10\).  The map \(N\mapsto S_N\) is
injective: a zero image makes \((z+\mu)^6N/A\) constant, and evaluation
at \(-\mu\), where \(A(-\mu)\ne0\), forces that constant and \(N\) to
vanish.  Both the relation space and \(\mathbb C[z]_{\le1}\) have
dimension two.  Therefore

\[
                         {\cal S}=\mathbb C[z]_{\le1}. \tag{18}
\]

Every linear \(S\) in (18) occurs in the exact rational derivative (14),
so its residue vanishes at every complementary pole as well.

## 4. The profile \(3^3 2^4 1^6\)

Let \({\cal D}\) be the four double values, \({\cal A}\) the three
triple values, and \({\cal R}\) the six singleton values.  Choose a
two-set \(T\subset{\cal D}\), and write
\(C={\cal D}\setminus T\).  Here

\[
 A(z)=\prod_{u\in C}(z-u)^2
            \prod_{a\in{\cal A}}(z-a)^3.              \tag{19}
\]

All 28 pair drops are legal.  A lowered double leaves its nonzero mate;
two omitted singletons leave two distinct singleton classes, at least
one of which is nonzero.

Equation (17) and cancellation in (14) give, for every linear \(S\),

\[
 {d\over dz}{(z+\mu)^6N(S)\over A}
 ={(z+\mu)^5Q_T(z)^2H(z)S(z)\over
   \displaystyle\prod_{u\in C}(z-u)^3
               \prod_{a\in{\cal A}}(z-a)^4}.          \tag{20}
\]

Fix \(u\in C\), and remove \((z-u)^{-3}\) from the right side; call
the remaining unit \(B_{T,u}\).  Its zero residue is

\[
                         (B_{T,u}S)''(u)=0
                         \qquad(S\in\mathbb C[z]_{\le1}). \tag{21}
\]

Taking \(S=z-u\) gives \(B_{T,u}'(u)=0\).  Thus

\[
0={5\over u+\mu}+2\sum_{t\in T}{1\over u+t}
 +\sum_{r\in{\cal R}}{1\over u+r}
 -{3\over u-v}-4\sum_{a\in{\cal A}}{1\over u-a},     \tag{22}
\]

where \(C=\{u,v\}\).

Fix \(u\), and take distinct \(x,v\in{\cal D}\setminus\{u\}\).
Let \(w\) be the fourth double value.  Compare (22) for
\(T=\{x,w\}\), with outside pair \(\{u,v\}\), and for
\(T=\{v,w\}\), with outside pair \(\{u,x\}\).  Every fixed term
cancels, leaving

\[
 {2\over u+x}+{3\over u-x}
 ={2\over u+v}+{3\over u-v}.                           \tag{23}
\]

Hence the three values in \({\cal D}\setminus\{u\}\) lie in one
fibre of

\[
             \Phi_u(t)={2\over u+t}+{3\over u-t}
                       ={5u+t\over u^2-t^2}.            \tag{24}
\]

A fibre \(\Phi_u(t)=\lambda\) is cut out by

\[
                         \lambda(u^2-t^2)-5u-t=0.      \tag{25}
\]

Its coefficient of \(t\) is \(-1\), so it is a nonzero polynomial of
degree at most two.  It cannot contain three distinct double values.

## 5. The profile \(3^4 2\,1^9\)

Let \(x\) be the unique double value, let \({\cal A}\) be the four
triple values, and choose eight singleton values as the formal set
\(R\).  Denote the remaining singleton value by \(r\).  All 36 pair
drops are legal: a double--singleton drop leaves the nonzero double mate,
and a two-singleton drop leaves three singleton classes, at most one of
which is zero.  The complementary polynomial is

\[
                         A(z)=(z-r)
                              \prod_{a\in{\cal A}}(z-a)^3. \tag{26}
\]

For every linear \(S\), (14)--(18) now give an exact derivative of the
form

\[
             {B_r(z)S(z)\over(z-r)^2},                \tag{27}
\]

where \(B_r(r)\ne0\); all its other displayed factors are units at
\(r\).  Its residue must vanish:

\[
                         (B_rS)'(r)=0
                         \qquad(S\in\mathbb C[z]_{\le1}). \tag{28}
\]

Taking \(S=z-r\) gives \(B_r(r)=0\), a contradiction.  This proves both
closures in (1).

## 6. Exact audit

[verify_live_three_zero_eighth_split_k5_mixed_linear_plane_increment.py](../computations/verify_live_three_zero_eighth_split_k5_mixed_linear_plane_increment.py)
checks every pair-drop core and zero-singleton guard, both sharp kernel
instances, the fifth-order leading cancellation, the two-dimensional
linear target, all 24 ordered double swaps (twelve unordered), the quadratic fibre, the
outside-singleton residue, and membership of both profiles in the exact
fifth-order residual ledger.
