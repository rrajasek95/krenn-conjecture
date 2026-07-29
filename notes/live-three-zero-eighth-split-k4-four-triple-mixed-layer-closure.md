# The eighth split: fourth-order mixed-layer closure of \(3^4 2^2 1^6\)

## 1. Result

At \(h=8,k=4\), consider

\[
                         \lambda=3^4 2^2 1^6.            \tag{1}
\]

Write \(a_1,\ldots,a_4\) for the four triple values, \(x,y\) for the
two double values, and \(R\) for the set of six singleton values.  The
repeated values are nonzero, and at most one member of \(R\) is zero.

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

Use both double layers at role two and all six singleton layers at role
one.  This formal target has total role ten.  Lowering any pair of its
eight layers produces one of \(28\) legal eight-label cores, and the
exact lifts of their Hermite residuals lie in one kernel in
\(\mathbb C[z]_{\le9}\).

The two double rows and six singleton rows bound this kernel by four
dimensions.  The mixed-parity argument from the third-order setting is
unchanged: if the lifts spanned only three dimensions, their parity
minors would have the sharp degree-seventeen divisor, forcing projective
evenness; the six singleton squares then violate the reduced Wronskian
bound.  Thus the kernel is exactly four-dimensional.

The eight value rows consequently have two relations.  Their dual
numerators have degree at most seven.  Here the complementary polynomial
has degree twelve, and the fourth-order common pole changes the leading
coefficient in the dual differential operator to

\[
                              n+5-12=n-7.
\]

The top term again cancels at \(n=7\), so the two-dimensional relation
space would inject into the constants.  This is impossible.

## 2. Eight formal layers and twenty-eight pair drops

Put

\[
\begin{split}
 Q(z)&=(z+x)(z+y),\\
 H(z)&=\prod_{r\in R}(z+r),\\
 A(z)&=\prod_{i=1}^4(z-a_i)^3.
\end{split}                                             \tag{2}
\]

The formal target assigns role two to \(x,y\) and role one to every
member of \(R\), hence has total role

\[
                              2+2+6=10.                 \tag{3}
\]

Associate to a double layer \(v\in\{x,y\}\) and a singleton layer
\(r\in R\) the coprime lift factors

\[
                f_v(z)=z^2-v^2,\qquad
                f_r(z)=(z-r)(z+r)^2.                   \tag{4}
\]

Choose any pair of the eight formal layers and lower both selected roles
by one.  The resulting core has total role eight.  If a double is
lowered, its nonzero mate remains as a singleton class in the complement.
If two original singletons are omitted, both remain in the complement
and at least one is nonzero.  Thus every one of the

\[
                              \binom82=28               \tag{5}
\]

pair drops is legal.

Let \(b\in\{0,1,2\}\) count the lowered singleton layers.  The core
represents \(8-b\) value classes, so the uniform Hermite bound gives

\[
                         0\ne q_{ij}\in
                         \mathbb C[z]_{\le5-b}.          \tag{6}
\]

The exact identities

\[
 {z-v\over(z+v)^2}={z^2-v^2\over(z+v)^3},
 \qquad
 z-r={(z-r)(z+r)^2\over(z+r)^2}                        \tag{7}
\]

fill a lowered double layer and formally restore an omitted singleton
layer.  Hence

\[
                         P_{ij}=f_if_jq_{ij}.            \tag{8}
\]

The two lift factors have total degree \(4+b\), and therefore

\[
                         0\ne P_{ij}\in
                         \mathbb C[z]_{\le9}             \tag{9}
\]

in all three cases.  Every original dependence is now written, without
changing it, as

\[
 F_P(z)={A(z)P(z)\over
              (z+\mu)^5Q(z)^3H(z)^2},
 \qquad P=P_{ij}.                                      \tag{10}
\]

The numerator and denominator degrees in (10) are at most \(21\) and
\(23\), respectively, so \(F_P=O(z^{-2})\).

Define

\[
\begin{split}
 K={}&\{P\in\mathbb C[z]_{\le9}:
       \operatorname {res}_{z=-x}F_P=
       \operatorname {res}_{z=-y}F_P=0,\\
 &\hspace{37mm}
       \operatorname {res}_{z=-r}F_P=0\quad(r\in R)\},\\
 W={}&\operatorname {span}\{P_{ij}:1\le i<j\le8\}.
\end{split}                                             \tag{11}
\]

Then \(W\subseteq K\).  The two double rows have exact differential order
two, while the six singleton rows have exact order one.  The residue
theorem also supplies the exact order-four row at the common pole
\(-\mu\), although the eight value rows already suffice below.

## 3. The value-row kernel has dimension at most four

Let \(d=\dim K\).  If the polynomial gcd of \(K\) is a unit at all eight
value nodes, the two order-two rows force Wronskian weight \(2(d-2)\),
and the six order-one rows force weight \(6(d-1)\).  A \(d\)-space in
\(\mathbb C[z]_{\le9}\) has Wronskian degree at most \(d(10-d)\).
The forced weight minus this cap is

\[
                         d^2-2d-10,                     \tag{12}
\]

which is positive for every \(d\ge5\).

Gcd corrections only increase the deficit.  At an order-two node, a
simple gcd zero adds \(d+1\), an order-two zero is excluded after gcd
removal, and absorption at order at least three adds at least \(2d+2\).
At an order-one node, a simple gcd zero is excluded and absorption at
order at least two adds at least \(d+1\).  A gcd root away from the eight
nodes only lowers the degree cap.  Consequently

\[
                              \dim K\le4.                \tag{13}
\]

## 4. The pair-drop span has dimension at least four

The eight lift factors in (4) are pairwise coprime and have total degree

\[
                         2+2+6\cdot3=22>9.              \tag{14}
\]

For each layer put

\[
                         U_i=W\cap f_i\mathbb C[z].      \tag{15}
\]

Every \(U_i\cap U_j\) contains the nonzero lift \(P_{ij}\).  No \(U_i\)
can be a line: otherwise the seven \(P_{ij}\), \(j\ne i\), would be
scalar multiples of one polynomial, and the product of all eight
pairwise-coprime \(f_j\) would divide a polynomial of degree at most nine.
This also rules out \(\dim W=2\), so \(\dim W\ge3\).

Assume \(\dim W=3\).  Then every \(U_i\) is a plane or all of \(W\).
Choose a basis
\({\bf P}(z)=(P_0(z),P_1(z),P_2(z))\).  At a nonzero layer value \(v\),
both evaluation functionals at \(v\) and \(-v\) vanish on \(U_v\);
therefore \({\bf P}(v)\) and \({\bf P}(-v)\) are proportional.  Each
parity minor

\[
             M_{ij}(z)=P_i(z)P_j(-z)-P_i(-z)P_j(z)      \tag{16}
\]

is odd, has degree at most seventeen, and vanishes at \(\pm v\).

If no singleton is zero, the forced roots are zero and the sixteen
opposite layer roots.  If a singleton is zero, its lift factor is
\(z^3\); a basis adapted to \(U_0\) makes every minor vanish to order at
least three at zero, together with the other seven opposite pairs.  In
both cases every minor is a scalar multiple of one fixed odd divisor of
degree seventeen.  Thus

\[
                         {\bf P}(z)\mathbin\times{\bf P}(-z)
                              =D(z){\bf c}               \tag{17}
\]

for a constant vector \({\bf c}\).  If \({\bf c}\ne0\), its scalar
product with \({\bf P}(z)\) is a constant linear relation among the basis
polynomials.  Hence \({\bf c}=0\), and all parity minors vanish.

Remove the gcd \(G\) of \(W\).  The primitive basis vector is projectively
even: its proportionality factor under \(z\mapsto-z\) is constant and
equals \(\pm1\), while the odd sign would leave the forbidden common
factor \(z\).  Therefore

\[
                         W=G(z){\cal E}(z^2),            \tag{18}
\]

where \({\cal E}\subset\mathbb C[s]\) is a primitive
three-dimensional space.  Let \(g=\deg G\), and let \(n\) be the largest
degree in \({\cal E}\).  Then

\[
                         n\le\left\lfloor{9-g\over2}\right\rfloor. \tag{19}
\]

Let \(m\) count singleton values \(r\in R\) with \(G(-r)=0\), so
\(g\ge m\).  For each of the other \(6-m\) singleton values, at least
two independent members of \({\cal E}\) are divisible by
\((s-r^2)^2\).  This includes \(r=0\), because an even polynomial
divisible by \(z^3\) is divisible by \(z^4=s^2\).  Primitivity supplies
a third member not divisible by \(s-r^2\), so the vanishing sequence is
at least \((0,2,3)\) and contributes Wronskian weight at least two.
The six squared values are distinct.  Therefore

\[
 2(6-m)\le\deg\operatorname {Wr}({\cal E})
      \le3(n-2)
      \le3\left(\left\lfloor{9-m\over2}\right\rfloor-2\right). \tag{20}
\]

For \(m=0,\ldots,5\), the left- and right-hand sides are

\[
\begin{array}{c|rrrrrr}
m&0&1&2&3&4&5\\ \hline
2(6-m)&12&10&8&6&4&2\\
3(\lfloor(9-m)/2\rfloor-2)&6&6&3&3&0&0.
\end{array}                                             \tag{21}
\]

Every column is impossible.  If \(m=6\), (19) gives \(n\le1\), too small
for a three-dimensional polynomial space.  This excludes \(\dim W=3\).
Together with (13),

\[
                         W=K,\qquad \dim K=4.            \tag{22}
\]

## 5. The relation plane cannot inject into the constants

Set

\[
                         \Omega(z)={A(z)\over
                         (z+\mu)^5Q(z)^3H(z)^2}.         \tag{23}
\]

The eight value rows act on the ten-dimensional space
\(\mathbb C[z]_{\le9}\).  By (22), they have rank six, so their relation
space is two-dimensional.  For a relation \(c\), sum the corresponding
principal parts:

\[
                         J_c(z)=\sum_i c_i
                         \operatorname {pp}_i\Omega(z). \tag{24}
\]

The relation annihilates \(1,z,\ldots,z^9\), hence \(J_c=O(z^{-11})\).
Its denominator divides \(Q^3H^2\), of degree eighteen.  Thus

\[
                         J_c(z)={N_c(z)\over Q(z)^3H(z)^2},
                         \qquad \deg N_c\le7.           \tag{25}
\]

The disjoint principal-part supports make \(c\mapsto N_c\) injective.
After division by (23), put

\[
                         G_N(z)={(z+\mu)^5N(z)\over A(z)}. \tag{26}
\]

At a double node, \(G_N-c_i\) vanishes to order at least three; at a
singleton node it vanishes to order at least two.  Hence

\[
                         Q(z)^2H(z)\mid G_N'(z)          \tag{27}
\]

after removal of factors that are units at those nodes.

Define

\[
 g_A(z)=\prod_{i=1}^4(z-a_i)^2,\qquad
 R_A={A\over g_A},\qquad D_A={A'\over g_A}.             \tag{28}
\]

Then

\[
 \deg A=12,\quad \deg g_A=8,\quad
 \deg R_A=4,\quad \deg D_A=3,\quad \operatorname {LC}(D_A)=12. \tag{29}
\]

Direct differentiation gives

\[
 G_N'(z)={(z+\mu)^4g_A(z)\over A(z)^2}\,
                 {\cal E}_A(N)(z),                     \tag{30}
\]

where

\[
 {\cal E}_A(N)=R_A\bigl((z+\mu)N'+5N\bigr)
                  -(z+\mu)D_A N.                       \tag{31}
\]

If \(n=\deg N\le7\), the nominal leading coefficient of degree \(n+4\)
is

\[
                              n+5-12=n-7.               \tag{32}
\]

It vanishes when \(n=7\), while \(n\le6\) already gives degree at most
ten.  Therefore

\[
                              \deg{\cal E}_A(N)\le10.   \tag{33}
\]

Structural coprimality in (27)--(30), together with
\(\deg(Q^2H)=10\), now forces

\[
                         {\cal E}_A(N)=\gamma_NQ^2H.    \tag{34}
\]

Thus the two-dimensional relation numerator space maps linearly into
the one-dimensional space of constants \(\gamma_N\).  This map is
injective.  If \(\gamma_N=0\), then \(G_N'=0\), so

\[
                         (z+\mu)^5N=\gamma A.           \tag{35}
\]

Evaluation at \(-\mu\), where \(A(-\mu)\ne0\), gives \(\gamma=0\) and
then \(N=0\).  A two-dimensional space cannot inject into the constants,
which proves Theorem 1.1.

## 6. Census consequence and exact audit

On the current sequential \(h=8,k=4\) frontier, Theorem 1.1 closes the
unique twelve-class profile

\[
                              3^4 2^2 1^6.              \tag{36}
\]

[verify_live_three_zero_eighth_split_k4_four_triple_mixed_layer_closure.py](../computations/verify_live_three_zero_eighth_split_k4_four_triple_mixed_layer_closure.py)
checks all \(28\) legal pair-drop cores and lift degrees, the
gcd-corrected mixed-order kernel bound, both parity-divisor cases, the
reduced Wronskian table, the two-relation count, the exact differential
factorization, the degree-ten cancellation, and the one-profile census
increment.
