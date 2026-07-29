# The eighth split: nine-double four-singleton rainbow closure

## 1. Result

At \((h,k)=(8,4)\), the collision profile

\[
                              2^9 1^4                    \tag{1}
\]

is impossible on the no-extra-singular stratum.

Choose three double values at formal role two and all four singleton
values at formal role one.  Lowering any pair of the seven layers gives
21 legal eight-label cores.  Their lifts span the exact
four-dimensional kernel of the seven selected value rows in
\(\mathbb C[z]_{\le8}\).  The seven rows therefore have two relations,
which dualize injectively to a plane in the quadratics.

At each of the six outside doubles, the exact order-two row has that
plane as its kernel.  Fixing two outside doubles and taking a third
Boolean difference over three disjoint selection swaps gives two cubic
edge identities.  On a suitable six-set of the remaining seven doubles,
these identities color the edges of \(K_6\) by the three cube roots of
one nonzero number, with every perfect matching rainbow.  Each color
class would have to be a five-edge star.  Three disjoint stars cannot
partition \(K_6\), giving the contradiction.

The argument uses only the standing structural assumptions.  Repeated
exceptional values are nonzero, distinct classes are pairwise
nonopposite, and at most one singleton value is zero.  No genericity or
division by a row jet is used.

## 2. Seven formal layers and 21 pair drops

Let \({\cal D}\) be the nine double values and \({\cal R}\) the four
singleton values.  Fix a three-set \(T\subset{\cal D}\), put
\(C={\cal D}\setminus T\), and define

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C_T(z)=\prod_{u\in C}(z-u),\qquad
 H(z)=\prod_{r\in{\cal R}}(z+r).                       \tag{2}
\]

Give every \(t\in T\) formal role two and every \(r\in{\cal R}\) formal
role one.  The total formal role is

\[
                              3\cdot2+4=10.             \tag{3}
\]

Lower any two distinct layers.  If two double layers are lowered, their
two nonzero mates remain as singleton complement rows.  If one double
and one singleton are lowered, the double mate and omitted singleton
remain.  If two singleton layers are omitted, both remain in the
complement and at least one is nonzero.  Thus all

\[
                              \binom72=21               \tag{4}
\]

cores are legal, including when one singleton value is zero.

Associate the coprime lift factors

\[
 f_t(z)=z^2-t^2,\qquad
 f_r(z)=(z-r)(z+r)^2.                                  \tag{5}
\]

If \(b\in\{0,1,2\}\) of the lowered layers are singletons, the core
represents \(7-b\) classes.  Its nonzero Hermite residual has degree at
most \(4-b\), while the two lift factors have total degree \(4+b\).
Every pair drop therefore gives

\[
                         0\ne P_{ij}=f_if_jq_{ij}
                              \in\mathbb C[z]_{\le8}.   \tag{6}
\]

The exact lift identities rewrite the original rational dependence as

\[
 F_P(z)={C_T(z)^2P(z)\over
              (z+\mu)^5Q_T(z)^3H(z)^2}.                \tag{7}
\]

The numerator degree is at most \(12+8=20\), and the denominator degree
is \(5+9+8=22\), so \(F_P=O(z^{-2})\).

Let \(K_T\subset\mathbb C[z]_{\le8}\) be the common kernel of the three
selected-double rows and four singleton rows, and let \(W_T\) be the
span of the 21 lifts.  Then

\[
                              W_T\subseteq K_T.          \tag{8}
\]

## 3. The selected rows give \(\dim K_T\le4\)

The three double rows have exact differential order two, and the four
singleton rows have exact order one.  If a \(d\)-dimensional kernel has
unit gcd at those nodes, its forced Wronskian weight is

\[
                    3(d-2)+4(d-1)=7d-10,               \tag{9}
\]

whereas the degree cap in \(\mathbb C[z]_{\le8}\) is \(d(9-d)\).
The deficit is

\[
                    (7d-10)-d(9-d)=d^2-2d-10,          \tag{10}
\]

which is positive for \(d\ge5\).

The gcd corrections only increase this deficit.  A simple gcd zero at
an order-two node adds \(d+1\); absorption there requires order at least
three and adds at least \(2d+2\).  At an order-one node, a simple gcd
zero would force the primitive space to have another common zero, while
absorption at order at least two adds \(d+1\).  Other gcd roots only
lower the degree cap.  Hence

\[
                              \dim K_T\le4.              \tag{11}
\]

## 4. The pair-drop span has dimension four

The seven factors in (5) are pairwise coprime and have total degree

\[
                              3\cdot2+4\cdot3=18>8.     \tag{12}
\]

For a formal layer \(i\), put

\[
                         U_i=W_T\cap f_i\mathbb C[z].   \tag{13}
\]

Every \(U_i\cap U_j\) contains \(P_{ij}\ne0\).  No \(U_i\) can be a
line: the six members \(P_{ij}\), \(j\ne i\), would be scalar multiples
of one degree-eight generator, making the product of all seven factors
divide it.  Thus \(\dim U_i\ge2\), which also excludes
\(\dim W_T\le2\).

Suppose \(\dim W_T=3\), and choose a basis
\({\bf P}=(P_0,P_1,P_2)\).  At every nonzero layer value \(v\), both
evaluation functionals at \(v\) and \(-v\) vanish on the plane \(U_v\).
The three parity minors

\[
             P_i(z)P_j(-z)-P_i(-z)P_j(z)               \tag{14}
\]

are odd of degree at most fifteen.  If no singleton is zero, they vanish
at zero and at both signs of all seven layer values.  If a singleton is
zero, a basis adapted to its \(z^3\)-divisible plane makes every minor
vanish to order at least three at zero, while the other six values give
twelve more roots.  In either case every minor is a scalar multiple of
the same forced degree-fifteen odd divisor.

Consequently

\[
             {\bf P}(z)\mathbin\times{\bf P}(-z)=D(z){\bf c} \tag{15}
\]

for a constant vector \({\bf c}\).  If \({\bf c}\ne0\), taking its scalar
product with \({\bf P}(z)\) gives a constant relation among the basis
polynomials.  Thus all minors vanish.  After removing the gcd \(G\), the
primitive space is projectively even; primitivity makes the
proportionality factor under \(z\mapsto-z\) a constant \(\pm1\), and the
odd sign would leave a common factor \(z\).  Therefore

\[
                         W_T=G(z){\cal E}(z^2),
                         \qquad\dim{\cal E}=3.           \tag{16}
\]

Let \(m\) count singleton values \(r\) for which \(G(-r)=0\).  Because
\(W_T\subseteq K_T\), the exact order-one row excludes a simple gcd zero
at \(-r\): after factoring such a zero, the row would force every
primitive section to vanish there.  Hence

\[
                              \deg G\ge2m.               \tag{17}
\]

The degree of the square-variable space is at most \(4-m\).  At each of
the other \(4-m\) singleton values, the plane \(U_r\) gives two
independent members of \({\cal E}\) divisible by
\((s-r^2)^2\).  For \(r=0\), evenness upgrades divisibility by \(z^3\)
to divisibility by \(z^4=s^2\).  Primitivity supplies a third member
not divisible by \(s-r^2\), so the local vanishing sequence is at least
\((0,2,3)\) and contributes Wronskian weight two.  For \(m=0,1,2\), one
would need respectively

\[
\begin{array}{c|rrr}
m&0&1&2\\ \hline
2(4-m)&8&6&4\\
3((4-m)-2)&6&3&0.
\end{array}                                             \tag{18}
\]

Every column is impossible.  For \(m\ge3\), the square-variable degree
is at most one and cannot contain a three-space.  Thus
\(\dim W_T\ne3\).  Combining this with (8) and (11) gives

\[
                         W_T=K_T,\qquad\dim K_T=4.       \tag{19}
\]

## 5. The relation plane in the quadratics

The seven selected rows act on the nine-dimensional space
\(\mathbb C[z]_{\le8}\).  Equation (19) makes their rank five, so their
relation space has dimension two.  For a relation \(c\), sum the
corresponding principal parts of

\[
 \Omega_T(z)={C_T(z)^2\over
              (z+\mu)^5Q_T(z)^3H(z)^2}.                \tag{20}
\]

The relation annihilates \(1,z,\ldots,z^8\), hence the sum is
\(O(z^{-10})\).  Its denominator divides the degree-seventeen polynomial
\(Q_T^3H^2\), so it has the form

\[
                         J_c(z)={N_c(z)\over Q_T(z)^3H(z)^2},
                         \qquad\deg N_c\le7.            \tag{21}
\]

Disjoint principal-part supports make \(c\mapsto N_c\) injective.  Put

\[
                         G_N(z)={(z+\mu)^5N(z)\over C_T(z)^2}. \tag{22}
\]

Writing \(R=C_T\) and \(D=2C_T'\), direct differentiation gives

\[
 G_N'(z)={(z+\mu)^4C_T(z)\over C_T(z)^4}\,
                         {\cal E}_T(N)(z),              \tag{23}
\]

where

\[
 {\cal E}_T(N)=
 C_T\bigl((z+\mu)N'+5N\bigr)-2(z+\mu)C_T'N.            \tag{24}
\]

If \(n=\deg N\le7\), the nominal leading coefficient of degree \(n+6\)
in (24) is

\[
                              n+5-12=n-7.               \tag{25}
\]

It cancels at \(n=7\), while smaller \(n\) already give degree at most
twelve.  The order-three contacts at the selected doubles and
order-two contacts at the singleton poles therefore imply

\[
                         {\cal E}_T(N)=Q_T^2H\,S_N,
                         \qquad S_N\in\mathbb C[z]_{\le2}. \tag{26}
\]

The map \(N\mapsto S_N\) is injective.  A zero image makes \(G_N\)
constant, and evaluation of
\((z+\mu)^5N=\gamma C_T^2\) at \(-\mu\) gives \(\gamma=N=0\).
The relation space consequently maps onto a plane

\[
                         {\cal S}_T\subset\mathbb C[z]_{\le2}. \tag{27}
\]

Every \(S\in{\cal S}_T\) occurs in

\[
                         G_S'(z)=
 { (z+\mu)^4Q_T(z)^2H(z)S(z)\over C_T(z)^3}.            \tag{28}
\]

## 6. Six proportional outside-double rows

For \(u\in C={\cal D}\setminus T\), write
\(C_T=(z-u)C_u\) and set

\[
\begin{aligned}
 B_{T,u}(z)&={ (z+\mu)^4Q_T(z)^2H(z)\over C_u(z)^3},\\
 Y_T(u)&={B_{T,u}'(u)\over B_{T,u}(u)},\qquad
 Z_T(u)={B_{T,u}''(u)\over B_{T,u}(u)}.
\end{aligned}                                          \tag{29}
\]

The zero residue at the order-three pole \(u\) is the nonzero row

\[
 L_{T,u}(S)=S''(u)+2Y_T(u)S'(u)+Z_T(u)S(u)=0.           \tag{30}
\]

Its kernel on the quadratics is a plane containing (27), hence equals
\({\cal S}_T\).  All six rows (30) are therefore proportional.

For two outside values \(u\ne v\), put

\[
\begin{gathered}
 \delta=u-v,\qquad
 p=\delta Y_T(u),\quad q=\delta Y_T(v),\\
 U=\delta^2Z_T(u),\qquad V=\delta^2Z_T(v),\qquad
 R=q-p+2pq.
\end{gathered}                                         \tag{31}
\]

Associate to (30) its characteristic quadratic

\[
 \chi_u(s)=L_{T,u}((z-s)^2)
       =2+4Y_T(u)(u-s)+Z_T(u)(u-s)^2.                  \tag{32}
\]

Evaluate the proportional rows on \((z-u)^2\), \((z-v)^2\), and
\((z-u)(z-v)\), and cross-multiply.  No row value is divided out.  The
two resulting identities are

\[
                         U(1-q)=2R,\qquad
                         V(1+p)=2R.                    \tag{33}
\]

They remain valid when any of \(U,V,1+p,1-q\) vanishes.

## 7. Three disjoint swaps

Fix \(u,v\in{\cal D}\), keep them outside, and write
\(E={\cal D}\setminus\{u,v\}\), so \(|E|=7\).  As the selected three-set
\(T\subset E\) varies, logarithmic differentiation of (29) gives

\[
\begin{aligned}
 Y_T(u)&=\kappa_u+\sum_{x\in T}\Phi_u(x),&
 \dot Y_T(u)&=\eta_u+\sum_{x\in T}\Psi_u(x),\\
 Z_T(u)&=Y_T(u)^2+\dot Y_T(u),&
 \Phi_u(x)&={2\over u+x}+{3\over u-x}
             ={5u+x\over u^2-x^2},\\
 &&\Psi_u(x)&=-{2\over(u+x)^2}-{3\over(u-x)^2}.
\end{aligned}                                          \tag{34}
\]

The same formulas hold at \(v\).  The constants \(\kappa,\eta\) are
independent of \(T\).

Choose six members of \(E\), arrange them in three pairs
\((a_i,b_i)\), and leave the seventh member outside.  Selecting one
endpoint of each pair gives eight valid three-sets \(T\).  Define the
swap increments

\[
 \alpha_i=\delta\bigl(\Phi_u(a_i)-\Phi_u(b_i)\bigr),
 \qquad
 \beta_i=\delta\bigl(\Phi_v(a_i)-\Phi_v(b_i)\bigr).     \tag{35}
\]

Here \(p,q\) are affine Boolean functions, while
\(U=p^2+\text{affine}\) and \(V=q^2+\text{affine}\).
The third mixed differences of (33) are exactly

\[
\begin{aligned}
 \alpha_1\alpha_2\beta_3+
 \alpha_1\alpha_3\beta_2+
 \alpha_2\alpha_3\beta_1&=0,\\
 \beta_1\beta_2\alpha_3+
 \beta_1\beta_3\alpha_2+
 \beta_2\beta_3\alpha_1&=0.
\end{aligned}                                          \tag{36}
\]

All lower Boolean degrees, including every \(\Psi\)-term, cancel.

## 8. Choosing a clean six-set

For a fixed anchor \(u\), every fibre of \(\Phi_u\) has size at most
two: after clearing its structurally nonzero denominator,
\(\Phi_u(x)=\lambda\) becomes

\[
                         \lambda(u^2-x^2)-5u-x=0,       \tag{37}
\]

a nonzero polynomial of degree at most two.  Thus the pairs
\(\{x,y\}\subset E\) with \(\Phi_u(x)=\Phi_u(y)\) form a matching
\(M_u\).  Define \(M_v\) similarly.

The two matchings have at most one common edge.  Indeed, a common
collision \(\{x,y\}\) satisfies

\[
\begin{aligned}
 xy+5u(x+y)+u^2&=0,\\
 xy+5v(x+y)+v^2&=0.
\end{aligned}                                          \tag{38}
\]

Since \(u\ne v\), subtraction gives

\[
                         x+y=-{u+v\over5},\qquad xy=uv. \tag{39}
\]

These sum and product determine the unordered pair uniquely.

We now delete one vertex from \(E\).  A matching on seven vertices
restricts to a perfect matching after a deletion for at most one choice:
it must already consist of three edges, and the deleted vertex must be
its unique unmatched vertex.  If \(M_u\) and \(M_v\) have no common
edge, avoid their at most two bad deletions.  If they share the unique
edge \(\{x,y\}\), delete either endpoint.  That endpoint is matched in
both matchings, so it cannot be a bad unmatched deletion for either.

We obtain a six-set \(F\subset E\) such that

1. no edge of \(F\) lies in both \(M_u\) and \(M_v\);
2. neither \(M_u|_F\) nor \(M_v|_F\) is a perfect matching.

## 9. The impossible rainbow coloring of \(K_6\)

Take any perfect matching of \(F\), orient its three edges arbitrarily,
and use them as the pairs in (35).  Suppose \(\alpha_1=0\).  The first
equation in (36), together with \(\beta_1\ne0\), forces one of
\(\alpha_2,\alpha_3\) to vanish; say \(\alpha_2=0\).  Then
\(\beta_2\ne0\), and the second equation forces \(\alpha_3=0\).  This
would make the perfect matching lie in \(M_u|_F\), contrary to the
choice of \(F\).  The same argument with \(u,v\) exchanged excludes a
zero \(\beta_i\).

The orientation-independent edge ratios

\[
                              r_i={\beta_i\over\alpha_i} \tag{40}
\]

are therefore defined and nonzero.  Dividing (36) by
\(\alpha_1\alpha_2\alpha_3\) gives

\[
                         r_1+r_2+r_3=0,\qquad
                         r_1r_2+r_1r_3+r_2r_3=0.        \tag{41}
\]

Thus the three ratios in every perfect matching are the three distinct
cube roots of one nonzero number.  In particular, disjoint edges have
ratios with the same cube.  The disjointness graph \(KG(6,2)\) is
connected, so there is one \(c\ne0\) such that

\[
                              r_e^3=c                  \tag{42}
\]

for every edge \(e\) of \(K_6\).  Color an edge by which of the three
cube roots of \(c\) its ratio equals.  Equation (41) says that every
perfect matching is rainbow.

There are fifteen perfect matchings of \(K_6\), and every edge belongs
to three of them.  Since every perfect matching contains exactly one
edge of each color, every color class has five edges.  A color class is
intersecting: two disjoint edges extend to a perfect matching and could
not have the same color.

Finally, every five-edge intersecting family in \(K_6\) is a star.  To
see this directly, take two of its edges \(ab,ac\).  Every further edge
must contain \(a\) or equal \(bc\).  If \(bc\) occurs, no fourth edge can
meet all three sides of that triangle; hence a five-edge family consists
of all five edges through \(a\).  But two stars in \(K_6\) always share
the edge joining their centers.  Three disjoint color classes cannot all
be stars.  This contradiction proves (1).

## 10. Exact audit

[verify_live_three_zero_eighth_split_k4_nine_double_four_singleton_rainbow_closure.py](../computations/verify_live_three_zero_eighth_split_k4_nine_double_four_singleton_rainbow_closure.py)
checks all 1764 legal cores and lift degrees, every gcd correction, the
sharp degree-fifteen parity boundary including a zero singleton, the
strengthened \(g\ge2m\) reduced-Wronskian table, the relation count and
degree-two dual target, the normalized outside rows, both division-free
pair identities, and the exact third Boolean differences.  It also
exhausts the seven-vertex deletion lemma for all matching pairs with at
most one common edge, verifies the fibre formulas, and enumerates the
\(K_6\) perfect matchings and their exact five-edge transversals.
