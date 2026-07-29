# The eighth split: final mixed-layer closure at third order

## 1. Result

Consider the last updated no-extra-singular profile at \(h=8,k=3\),

\[
                         \lambda=3^2 2^4 1^7.            \tag{1}
\]

Write \(a,b\) for the triple values, \(V\) for the four double values,
and \(R\) for the seven singleton values.  Every double and triple value
is nonzero.  At most one member of \(R\) is zero.

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

Fix one double at formal role two and all seven singletons at formal role
one.  Lowering any one layer gives an eight-label core.  The double drop
and every nonzero-singleton drop are legal; only the drop of a possible
zero singleton may be unavailable.  Their lifted residuals nevertheless
span a sharp three-dimensional kernel in \(\mathbb C[z]_{\le7}\).  The
proof is a degree-thirteen parity argument followed by a Wronskian count
at the six or seven nonzero squared singleton values.

The eight value rows then have three relations.  Duality sends them
injectively to a hyperplane in the cubics.  At each of the three outside
double values, the exact second-order residue row has that same hyperplane
as its kernel.  The hyperplane is therefore spanned by the three cubes
anchored at those values.  Comparing the resulting logarithmic-derivative
equation as the formal double moves puts the other three double values in
one fibre of a degree-two rational function.

## 2. One double and seven formal singleton layers

Fix \(x\in V\), put \(C=V\setminus\{x\}\), and define

\[
 Q_x(z)=z+x,\qquad H(z)=\prod_{r\in R}(z+r),\qquad
 A_x(z)=\prod_{u\in C}(z-u)^2(z-a)^3(z-b)^3.            \tag{2}
\]

The formal target assigns role two to \(x\) and role one to all seven
members of \(R\), for total role

\[
                              2+7=9.                    \tag{3}
\]

There are two kinds of one-label drop.

1. Lower the double role from two to one.  The core selects one label at
   \(x\) and all seven singleton labels.  It is legal because the nonzero
   mate at \(x\) remains in the complement.  Eight classes are represented,
   so its residual \(q_x\) has degree at most five.  Put

   \[
                              P_x=(z^2-x^2)q_x.          \tag{4}
   \]

2. Omit a singleton \(r\in R\).  The core selects both labels at \(x\)
   and the other six singleton labels.  If \(r\ne0\), it is legal because
   the omitted singleton is a nonzero complement row.  Seven classes are
   represented, so \(\deg q_r\le4\).  Put

   \[
                              P_r=(z-r)(z+r)^2q_r.       \tag{5}
   \]

If a singleton value is zero, the core omitting it need not be legal and
is not used.  The other six singleton drops and the double drop remain
legal.  Thus there are eight legal lifts when no singleton is zero and
seven otherwise.

The exact identities

\[
 {z-x\over(z+x)^2}={z^2-x^2\over(z+x)^3},
 \qquad
 z-r={(z-r)(z+r)^2\over(z+r)^2}                         \tag{6}
\]

show that all available lifts lie in \(\mathbb C[z]_{\le7}\) and rewrite
their original rational dependences as

\[
 F_P(z)={A_x(z)P(z)\over
              (z+\mu)^4Q_x(z)^3H(z)^2}.                 \tag{7}
\]

The numerator and denominator degrees are at most \(19\) and \(21\), so
\(F_P=O(z^{-2})\).

Let \(K_x\subset\mathbb C[z]_{\le7}\) be the common kernel of the residue
row at \(-x\) and the seven rows at \(-r\), \(r\in R\).  Let \(W_x\) be
the span of the seven or eight available lifts.  Then

\[
                              W_x\subseteq K_x.          \tag{8}
\]

The double row has exact differential order two, and the seven singleton
rows have exact order one.  The residue theorem also adds the exact
order-three common-pole row.

## 3. The kernel has dimension at most three

Let \(d=\dim K_x\).  With a unit gcd at the eight value nodes, the forced
Wronskian weight is

\[
                         (d-2)+7(d-1)=8d-9.             \tag{9}
\]

The degree cap for a \(d\)-space in \(\mathbb C[z]_{\le7}\) is
\(d(8-d)\), so the deficit is

\[
                              d^2-9.                    \tag{10}
\]

This is positive for every \(d\ge4\).  The gcd corrections are also
strictly positive: a simple gcd zero at the order-two node increases the
deficit by \(d+1\), absorption there at order at least three increases it
by at least \(2d+2\), and absorption at an order-one node at order at
least two increases it by at least \(d+1\).  Gcd orders two and one,
respectively, leave an exact order-zero equation and are impossible after
gcd removal.  Hence

\[
                              \dim K_x\le3.              \tag{11}
\]

## 4. The available lifts span three dimensions

For the double layer use \(f_x=z^2-x^2\), and for a nonzero singleton
drop use \(f_r=(z-r)(z+r)^2\).  These factors are pairwise coprime.  Their
product has degree \(23\) if all singleton drops are available and degree
\(20\) if the zero-singleton drop is omitted.  Thus the nonzero lifted
polynomials cannot span a line in degree seven.

Suppose they span a plane with basis \(p,q\).  Each available lift
divisible by \(f_v\) gives

\[
                         p(v)q(-v)-p(-v)q(v)=0.          \tag{12}
\]

The left side is an odd polynomial of degree at most thirteen.  If all
singleton values are nonzero, it vanishes at zero and at the sixteen
points \(\pm v\) supplied by the double and seven singletons.  If one
singleton is zero, the seven available nonzero layer values still supply
zero and fourteen opposite roots.  In both cases there are more than
thirteen roots, so (12) vanishes identically.

After removal of the pencil gcd \(G\), the primitive ratio is even.  The
same coprime-involution argument as in the three-dimensional parity lemma
gives

\[
                         W_x=G(z){\cal E}(z^2),          \tag{13}
\]

where \({\cal E}\subset\mathbb C[s]\) is a primitive pencil.  Put
\(g=\deg G\) and let \(n\) be the largest degree in \({\cal E}\).  Then

\[
                         n\le\left\lfloor{7-g\over2}\right\rfloor. \tag{14}
\]

Let \(N\) be the number of available singleton drops: \(N=7\) if no
singleton is zero and \(N=6\) otherwise.  Let \(m\) count their values
for which \(G(-r)=0\).  Then \(g\ge m\).  At any remaining singleton,
the special member \(P_r/G\) of \({\cal E}\) has a double zero at
\(s=r^2\).  Primitivity supplies another member nonzero there, so the
Wronskian of \({\cal E}\) has weight at least one.  Therefore

\[
 N-m\le\deg\operatorname {Wr}({\cal E})
       \le2(n-1)
       \le2\left(\left\lfloor{7-m\over2}\right\rfloor-1\right). \tag{15}
\]

For \(N=7\), the two sides for \(m=0,\ldots,5\) are

\[
                         (7,6,5,4,3,2)
                         \quad\hbox{and}\quad(4,4,2,2,0,0). \tag{16}
\]

For \(N=6\), they are

\[
                         (6,5,4,3,2,1)
                         \quad\hbox{and}\quad(4,4,2,2,0,0). \tag{17}
\]

Every displayed comparison is strict.  Larger \(m\) makes the bound in
(14) too small to contain a pencil.  Thus the lifts cannot span a plane.
Together with (8) and (11), this proves

\[
                         W_x=K_x,\qquad\dim K_x=3.       \tag{18}
\]

## 5. The cubic relation hyperplane

Put

\[
                         \Omega_x(z)={A_x(z)\over
                         (z+\mu)^4Q_x(z)^3H(z)^2}.       \tag{19}
\]

The eight value rows act on the eight-dimensional space
\(\mathbb C[z]_{\le7}\).  Equation (18) gives rank five and a
three-dimensional relation space.  For a relation \(c\), let \(J_c\) be
the corresponding sum of principal parts at the eight selected nodes.
The eight vanishing moments at infinity imply

\[
                         J_c(z)={N_c(z)\over Q_x(z)^3H(z)^2},
                         \qquad\deg N_c\le8.            \tag{20}
\]

The principal-part supports are distinct, so \(c\mapsto N_c\) is
injective.  Divide by (19):

\[
                         G_N(z)={(z+\mu)^4N(z)\over A_x(z)}. \tag{21}
\]

Define

\[
 g_A(z)=\prod_{u\in C}(z-u)(z-a)^2(z-b)^2,qquad
 R_A={A_x\over g_A},\qquad D_A={A_x'\over g_A}.         \tag{22}
\]

Then \(\deg R_A=5\), \(\deg D_A=4\), and the leading coefficient of
\(D_A\) is \(12\).  Differentiation gives

\[
 G_N'(z)={(z+\mu)^3g_A(z)\over A_x(z)^2}\,{\cal E}_A(N)(z), \tag{23}
\]

where

\[
 {\cal E}_A(N)=R_A\bigl((z+\mu)N'+4N\bigr)
                  -(z+\mu)D_A N.                       \tag{24}
\]

For \(n=\deg N\le8\), the nominal leading coefficient is
\(n+4-12=n-8\).  It cancels at \(n=8\), giving

\[
                              \deg {\cal E}_A(N)\le12.  \tag{25}
\]

The order-three contact at \(-x\) and order-two contacts at the seven
singleton nodes imply

\[
                         {\cal E}_A(N)=Q_x^2H\,S_N,
                         \qquad S_N\in\mathbb C[z]_{\le3}. \tag{26}
\]

As before, \(N\mapsto S_N\) is injective: a zero image makes \(G_N\)
constant, and evaluation of
\((z+\mu)^4N=\gamma A_x\) at \(-\mu\) gives \(N=0\).  Hence the three
relation numerators map to a three-dimensional hyperplane

\[
                         {\cal S}_x\subset\mathbb C[z]_{\le3}. \tag{27}
\]

Every \(S\in{\cal S}_x\) occurs in the rational derivative

\[
 G_S'(z)={ (z+\mu)^3(z+x)^2H(z)S(z)\over
               \displaystyle\prod_{u\in C}(z-u)^3(z-a)^4(z-b)^4}. \tag{28}
\]

## 6. Outside-double rows and the final swap

At an outside double \(u\in C\), write

\[
 B_u(z)={ (z+\mu)^3(z+x)^2H(z)\over
   \displaystyle\prod_{v\in C\setminus\{u\}}(z-v)^3(z-a)^4(z-b)^4}. \tag{29}
\]

This is a unit at \(u\).  The zero residue in (28) is the nonzero exact
second-order row

\[
                         S\longmapsto(B_uS)''(u).        \tag{30}
\]

Its kernel on the four-dimensional cubic space is a hyperplane containing
\({\cal S}_x\), hence is exactly \({\cal S}_x\).  In particular,
\((z-u)^3\in{\cal S}_x\).  The three cubes at the three distinct values in
\(C\) are independent, so

\[
                         {\cal S}_x=
                         \operatorname {span}\{(z-u)^3:u\in C\}. \tag{31}
\]

Fix \(u\in C\), and write \(C\setminus\{u\}=\{v,w\}\).  Normalize (30)
by \(B_u(u)\) and put

\[
                         Y_u={B_u'(u)\over B_u(u)}.      \tag{32}
\]

For \(\delta=u-v\), evaluation of the normalized row on \((z-v)^3\)
has the form

\[
                         \delta\bigl(6+6Y_u\delta+Z_u\delta^2\bigr). \tag{33}
\]

It vanishes for \(v\) and \(w\).  Comparing the constant and linear
coefficients of the quadratic in (33) gives

\[
                         Y_u=-{1\over u-v}-{1\over u-w}. \tag{34}
\]

On the other hand, the logarithmic derivative of (29) is

\[
 Y_u={3\over u+\mu}+{2\over u+x}
      +\sum_{r\in R}{1\over u+r}
      -3\sum_{v\in C\setminus\{u\}}{1\over u-v}
      -4\left({1\over u-a}+{1\over u-b}\right).        \tag{35}
\]

Equations (34)--(35) give

\[
 {3\over u+\mu}+{2\over u+x}
 +\sum_{r\in R}{1\over u+r}
 -2\sum_{v\in C\setminus\{u\}}{1\over u-v}
 -4\left({1\over u-a}+{1\over u-b}\right)=0.          \tag{36}
\]

The construction applies for every choice of the formal double \(x\).
Fix \(u\in V\), and let \(x,y\) be two other double values.  Compare
(36) with \(x\) selected and with \(y\) selected.  Every fixed term
cancels, leaving

\[
 {1\over u+x}+{1\over u-x}
             ={1\over u+y}+{1\over u-y}.                \tag{37}
\]

Thus the three values in \(V\setminus\{u\}\) lie in one fibre of

\[
                         \Psi_u(t)={2u\over u^2-t^2}.   \tag{38}
\]

For a fibre value \(\lambda\), the cleared equation is

\[
                         \lambda(u^2-t^2)-2u=0.         \tag{39}
\]

It is a nonzero polynomial of degree at most two because \(u\ne0\).
It cannot have the three distinct roots in \(V\setminus\{u\}\).  This
contradiction proves Theorem 1.1.

## 7. Final frontier and exact audit

All other profiles in the updated \(h=8,k=3\) no-extra-singular census
are closed by the five-triple, four-triple, formal-five, and terminal
three-triple theorems.  Theorem 1.1 removes the sole remaining profile,
so this collision frontier is empty.

[verify_live_three_zero_eighth_split_k3_two_triple_final_mixed_layer_closure.py](../computations/verify_live_three_zero_eighth_split_k3_two_triple_final_mixed_layer_closure.py)
checks every legal single-drop core including the possible missing zero
drop, both lift identities and degree bounds, the mixed-order kernel
estimate, both parity/ramification tables, the cubic relation hyperplane,
the three anchored cubes, the exact logarithmic-derivative equation, and
the final quadratic-fibre swap.
