# The eighth split: second-order closure of the all-double profile

## 1. Result

Consider

\[
                         (h,k;\lambda)=(8,2;2^{10}).       \tag{1}
\]

Thus \(p=10\), and the twenty exceptional labels form ten double value
classes.  Write their value set as \(V\).  Every value in \(V\) is
nonzero, distinct from \(\pm\mu\), and neither equal nor opposite to any
other value in \(V\).

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

The proof uses both sharp structures visible at this profile.

1. On every five-set of double values, selecting three doubles fully and
   two partially produces ten quadratic residuals.  After lifting the two
   missing mates, their sextics fill a four-dimensional common
   second-order residue kernel.
2. The two relations among the five value-residue rows dualize to a pencil
   of rational functions.  A sharp cancellation maps this pencil
   isomorphically onto \(\mathbb C[z]_{\le1}\).  The two images \(1,z\)
   force an exact Stieltjes equation on every five/five partition.
   Swapping one class across the partition puts nine distinct values in
   one degree-two fibre.

The independent full-core and antiderivative Wronskian route is exactly
one unit short.  It is included below because it identifies the only
equality case which the local second-order argument must remove.

## 2. Two partial doubles and a common sextic kernel

Assume for contradiction that every isolated-star pivot vanishes.  Fix a
five-element set \(T\subset V\), put \(O=V\setminus T\), and define

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C_O(z)=\prod_{u\in O}(z-u).                              \tag{2}
\]

For a pair \(\{x,y\}\subset T\), select one label at \(x\) and \(y\), and
both labels at the other three values of \(T\).  This is an eight-label
selection represented by five classes.  Its complement has the two
unselected mates at \(x,y\) as singleton row classes, together with the
five untouched doubles in \(O\).  The simultaneous-Hermite lemma gives

\[
                         0\ne q_{x,y}\in\mathbb C[z]_{\le2}. \tag{3}
\]

The associated rational dependence is

\[
 {q_{x,y}(z)(z-x)(z-y)C_O(z)^2\over
  (z+\mu)^3(z+x)^2(z+y)^2
  \prod_{t\in T\setminus\{x,y\}}(z+t)^3}.                \tag{4}
\]

Put

\[
 h_x(z)=z^2-x^2,\qquad
 P_{x,y}=h_xh_yq_{x,y}\in\mathbb C[z]_{\le6}.             \tag{5}
\]

Cancelling the two newly introduced factors in (5) rewrites (4) exactly
as

\[
 F_P(z)={C_O(z)^2P(z)\over
              (z+\mu)^3Q_T(z)^3},\qquad P=P_{x,y}.        \tag{6}
\]

Thus every \(P_{x,y}\) is killed by the same five residue functionals at
the poles \(-t\), \(t\in T\).  Define

\[
 K_T=\left\{P\in\mathbb C[z]_{\le6}:
       \operatorname {res}_{z=-t}F_P=0\quad(t\in T)\right\}. \tag{7}
\]

The numerator and denominator degrees in (6) are at most \(16\) and
\(18\), so \(F_P=O(z^{-2})\) for every \(P\in\mathbb C[z]_{\le6}\).
The residue theorem therefore shows that every \(P\in K_T\) is also
killed by the residue at \(-\mu\).

At each of these six nodes the regular cofactor in (6) is a unit.
Consequently every row is an exact second-order functional

\[
             L_\xi(P)=P''(\xi)+2Y_\xi P'(\xi)+M_\xi P(\xi).
                                                                    \tag{8}
\]

There is no loss of order at a partial anchor: equation (6) is identical
to the original rational function (4), and the factor \(h_x\) converts
the old simple-residue equation into (8) by the product rule.

Write

\[
 W_T=\operatorname {span}\{P_{x,y}:\{x,y\}\subset T\}
                         \subseteq K_T.                   \tag{9}
\]

## 3. The kernel has dimension at most four

Let \(d=\dim K_T\), let \(H=\gcd K_T\), and divide by \(H\).  At one of
the six nodes in (8), let \(\tau\) be the order of \(H\).

- If \(\tau=0\), the reduced vanishing sequence omits order \(2\), giving
  Wronskian weight at least \(d-2\).
- If \(\tau=1\), the product rule leaves an exact order-one functional,
  giving weight at least \(d-1\).
- If \(\tau=2\), the reduced functional has exact order zero and would
  force every reduced section to vanish.  This contradicts removal of the
  gcd.
- If \(\tau\ge3\), the condition is automatic, but the gcd has spent at
  least three degrees at that node.

Let \(n_1\) count nodes of the second type and \(n_3\) nodes of the fourth
type.  The other \(6-n_1-n_3\) nodes are of the first type, and

\[
 \deg H\ge n_1+3n_3.                                     \tag{10}
\]

The reduced Wronskian has degree at most \(d(7-\deg H-d)\).  The forced
weight minus this upper bound is at least

\[
 (d-4)(d+3)+(d+1)n_1+2(d+1)n_3.                          \tag{11}
\]

For \(d\ge5\), (11) is strictly positive.  Hence

\[
                              \dim K_T\le4.                \tag{12}
\]

For later orientation, \(d=4\) is an exact equality case.  It forces
\(\gcd K_T=1\), minimal weight two at all six nodes, and

\[
 \operatorname {Wr}(K_T)
       \doteq (z+\mu)^2Q_T(z)^2.                          \tag{13}
\]

## 4. The ten lifted residuals cannot span three dimensions

The quadratics \(h_t\), \(t\in T\), are pairwise coprime.  The ten
polynomials in (9) cannot span a line: a common generator would be
divisible by all five \(h_t\), of total degree ten.  They cannot span a
two-plane either.  Indeed, put

\[
 {\cal U}_t=W_T\cap h_t\mathbb C[z]_{\le4}.               \tag{14}
\]

Every pair \({\cal U}_t,{\cal U}_s\) has nonzero intersection.  In a
two-dimensional \(W_T\), either all the proper \({\cal U}_t\) are the
same line, producing a polynomial divisible by all five \(h_t\), or some
\({\cal U}_t=W_T\); factoring that common \(h_t\) reduces the other four
pairwise intersections to the same impossible conclusion.  Thus

\[
                              \dim W_T\ge3.                \tag{15}
\]

Suppose now that \(\dim W_T=3\).  If some \({\cal U}_t\) were a line,
its nonzero generator would lie in every other \({\cal U}_s\), again
giving divisibility by all five quadratics.  Hence every
\({\cal U}_t\) has dimension at least two.

At most one \({\cal U}_t\) can equal \(W_T\).  If exactly one does, say
\({\cal U}_a=W_T\), then for \(s,t\ne a\) the element \(P_{s,t}\) is a
scalar multiple of \(h_ah_sh_t\).  These products span

\[
                         W_T=h_a\mathbb C[z^2]_{\le2}.    \tag{16}
\]

It remains to treat the case in which all five \({\cal U}_t\) are
planes.  Choose a basis \({\bf P}(z)=(P_0(z),P_1(z),P_2(z))\) of \(W_T\).
Since (14) has codimension one, the two evaluation vectors
\({\bf P}(t)\) and \({\bf P}(-t)\) are proportional for every \(t\in T\).
Each parity minor

\[
 P_i(z)P_j(-z)-P_i(-z)P_j(z)                             \tag{17}
\]

is odd, has degree at most eleven, and vanishes at
\(0,\pm t\) for all five \(t\in T\).  Thus all three minors are scalar
multiples of

\[
                         z\prod_{t\in T}(z^2-t^2).        \tag{18}
\]

If their constant cross-product vector were nonzero, the plane spanned by
\({\bf P}(z)\) and \({\bf P}(-z)\) would be independent of \(z\).  All
three basis polynomials would then satisfy one constant linear relation.
Therefore every minor in (17) is identically zero.

After removing the polynomial gcd \(G\) of the three basis members, the
primitive vector is projectively even.  If
\({\bf R}={\bf P}/G\), then
\({\bf R}(-z)=\lambda(z){\bf R}(z)\).  Coprimality makes both numerator
and denominator of \(\lambda\) constant; applying the involution twice
gives \(\lambda=\pm1\).  The odd sign would put a common factor \(z\) in
all entries.  Hence the reduced space is even.  Together with (16), both
cases have the uniform form

\[
                    W_T=G(z)\,{\cal E}(z^2),\qquad
                    \dim{\cal E}=3,\qquad \deg G\le2.     \tag{19}
\]

If \(\deg G=1\) or \(2\), the degree-six bound makes
\({\cal E}=\mathbb C[s]_{\le2}\).  Restrict (8) at a nonzero node
\(\xi\) to \(G(z)R(z^2)\).  According as the local order of \(G\) is
zero, one, or two, the coefficient of \(R''\), \(R'\), or \(R\) is
respectively

\[
                     4\xi^2G(\xi),\qquad
                     4\xi G'(\xi),\qquad G''(\xi),        \tag{20}
\]

and is nonzero.  Thus a row in (8) cannot annihilate the whole
\(\mathbb C[s]_{\le2}\).

It follows that \(G\) is constant.  Then \({\cal E}\) is a hyperplane in
\(\mathbb C[s]_{\le3}\).  All six rows in (8), restricted to this
four-dimensional cubic space, must be proportional to its one
annihilator.  But a second-order row at \(s=s_0\) annihilates
\((s-s_0)^3\).  If its common coefficient vector is
\((c_0,c_1,c_2,c_3)\), then every one of the six squared nodes satisfies

\[
                   c_0s_0^3-3c_1s_0^2+3c_2s_0-c_3=0.    \tag{21}
\]

The nodes \(t^2\), \(t\in T\), and \(\mu^2\) are six distinct numbers.
Equation (21) would make a cubic identically zero, contradicting the
nonzero row.  Therefore \(\dim W_T\ne3\).

Combining this with (12) and (15) gives the sharp local conclusion

\[
                         W_T=K_T,\qquad \dim K_T=4.       \tag{22}
\]

## 5. Dualizing the two row relations

Let

\[
 \Omega_T(z)={C_O(z)^2\over(z+\mu)^3Q_T(z)^3}.            \tag{23}
\]

The five value-residue rows on \(\mathbb C[z]_{\le6}\) have kernel
dimension four by (22), hence rank three.  Their relation space is
two-dimensional.

Fix a relation \(c=(c_t:t\in T)\).  At each pole \(-t\), take the
principal part of \(\Omega_T\), and put

\[
 H_c(z)=\sum_{t\in T}c_t\,
              \operatorname {pp}_{z=-t}\Omega_T(z).      \tag{24}
\]

For every \(P\in\mathbb C[z]_{\le6}\), the relation says that the sum of
the finite residues of \(P H_c\) is zero.  Equivalently, the residue at
infinity vanishes for \(P=1,z,\ldots,z^6\).  Thus

\[
                         H_c(z)=O(z^{-8}).                \tag{25}
\]

The denominator of (24) divides \(Q_T^3\), of degree fifteen.  Therefore

\[
                  H_c(z)={N_c(z)\over Q_T(z)^3},
                  \qquad \deg N_c\le7.                   \tag{26}
\]

The map \(c\mapsto N_c\) is injective: a zero \(H_c\) has zero principal
part at each distinct pole, forcing every \(c_t=0\).  Hence the
numerators in (26) form a two-dimensional space \({\cal N}_T\).

Divide (24) by (23):

\[
             G_N(z):={H_c(z)\over\Omega_T(z)}
                    ={(z+\mu)^3N(z)\over C_O(z)^2}.       \tag{27}
\]

Near \(-t\), the difference \(H_c-c_t\Omega_T\) is analytic.  Since
\(\Omega_T\) has an exact triple pole,

\[
                         G_N(z)-c_t=O((z+t)^3).           \tag{28}
\]

Thus \(G_N'\) has a double zero at every root of \(Q_T\).  Direct
differentiation gives

\[
 G_N'(z)={(z+\mu)^2\over C_O(z)^3}\,{\cal D}_O(N)(z),     \tag{29}
\]

where

\[
 {\cal D}_O(N)=
 C_O\bigl((z+\mu)N'+3N\bigr)
       -2(z+\mu)C_O'N.                                   \tag{30}
\]

Equations (28)--(30) imply

\[
                       {\cal D}_O(N)=Q_T^2S_N.            \tag{31}
\]

This is the sharp degree drop.  If \(n=\deg N\le7\), the nominal leading
coefficient of degree \(n+5\) in (30) is \(n+3-2\cdot5=n-7\).
For \(n=7\) it cancels; for \(n\le6\) the degree is already at most
eleven.  Hence

\[
                         S_N\in\mathbb C[z]_{\le1}.       \tag{32}
\]

The map \(N\mapsto S_N\) has zero kernel.  Indeed, \(S_N=0\) makes
\(G_N\) constant.  A nonzero constant would give

\[
                         (z+\mu)^3N=c\,C_O^2,             \tag{33}
\]

which is impossible at \(z=-\mu\), since \(C_O(-\mu)\ne0\).  Thus
\(N=0\).  Both spaces in (32) have dimension two, so

\[
                   {\cal N}_T\xrightarrow[\ \cong\ ]{{\cal D}_O/Q_T^2}
                   \mathbb C[z]_{\le1}.                  \tag{34}
\]

This proves, without a generic-rank assumption, that there are relation
numerators \(N_0,N_1\) for which \(S_{N_0}=1\) and \(S_{N_1}=z\).

## 6. Rational derivatives and the partition-swap contradiction

For \(S=1\) and \(S=z\), equations (29)--(34) say

\[
                         G_S'(z)=
 { (z+\mu)^2Q_T(z)^2S(z)\over C_O(z)^3}.                 \tag{35}
\]

The left side is the derivative of a rational function.  Every finite
residue on the right side must therefore vanish.

Fix \(u\in O\), put \(C_u=C_O/(z-u)\), and define the local unit

\[
                         A_u(z)=
 { (z+\mu)^2Q_T(z)^2\over C_u(z)^3}.                     \tag{36}
\]

For \(S=1\), the local expression in (35) is
\(A_u(z)/(z-u)^3\), whose residue is \(A_u''(u)/2\).  For \(S=z\), its
residue is

\[
                         {u\over2}A_u''(u)+A_u'(u).       \tag{37}
\]

Both residues vanish, so \(A_u'(u)=0\).  Since \(A_u(u)\ne0\), its
logarithmic derivative gives

\[
 {2\over u+\mu}
 +2\sum_{t\in T}{1\over u+t}
 -3\sum_{\substack{v\in O\\v\ne u}}{1\over u-v}=0
                    \qquad(u\in O).                      \tag{38}
\]

The construction applies to every five/five partition \(V=T\sqcup O\).
Fix any three distinct values \(u,a,b\in V\).  Choose a partition with
\(u,b\in O\) and \(a\in T\), and compare (38) with the partition obtained
by swapping \(a\) and \(b\).  All other terms cancel, leaving

\[
 2\left({1\over u+b}-{1\over u+a}\right)
 -3\left({1\over u-a}-{1\over u-b}\right)=0.             \tag{39}
\]

Equivalently,

\[
                         \Phi_u(a)=\Phi_u(b),             \tag{40}
\]

where

\[
 \Phi_u(x)={2\over u+x}+{3\over u-x}
           ={5u+x\over u^2-x^2}.                         \tag{41}
\]

For fixed \(u\), equation (40) holds for every two values in
\(V\setminus\{u\}\).  Thus nine distinct values lie in one fibre of
\(\Phi_u\).  But the fibre equation \(\Phi_u(x)=\lambda\) is

\[
                         \lambda(u^2-x^2)-5u-x=0.         \tag{42}
\]

It is a nonzero polynomial of degree at most two, even when its quadratic
coefficient vanishes, because the coefficient of \(x\) is \(-1\).
This contradiction proves Theorem 1.1.

## 7. The independent global Wronskian equality case

For (1), the full value-core exchange is legal and gives

\[
                 K\subset\mathbb C[z]_{\le9},\qquad
                 d:=\dim K\ge3.                           \tag{43}
\]

The collision excess is \(e=10\).  In the antiderivative construction,
let \(J\subset\mathbb C[z]_{\le9}\) be the injective image of \(K\), let
\(g=\deg\gcd J\), and let \(a\) count absorbed collision multiplicity.
The gcd-corrected deficit is

\[
                         d^2-10+d(g-a)+a.                 \tag{44}
\]

For \(d\ge4\), (44) is positive.  For \(d=3\), any nonzero gcd is also
impossible: a gcd away from the ten collision nodes contributes \(3g\),
while absorbing \(a\ge1\) nodes requires \(g\ge2a\).  The sole survivor
of (44) is therefore

\[
                         d=3,\qquad \gcd J=1.             \tag{45}
\]

At each positive collision value, \(J\) has vanishing sequence at least
\((0,2,3)\), so its Wronskian is divisible by

\[
                         B(z)^2,\qquad
                         B(z)=\prod_{v\in V}(z-v).         \tag{46}
\]

The degree bound is \(3(9-3+1)=21\), while \(\deg B^2=20\).  Hence

\[
                         \operatorname {Wr}(J)
                         =B(z)^2L(z),\qquad \deg L\le1.   \tag{47}
\]

The full-core Wronskian is simultaneously sharp.  Its ten reflected Robin
nodes contribute twenty, and the exact order-two common-pole functional
contributes one.  The complete gcd/common-pole inequality leaves only

\[
 \gcd K=1,\qquad
 \operatorname {Wr}(K)\doteq
        (z+\mu)\prod_{v\in V}(z+v)^2,                    \tag{48}
\]

again of the maximal degree \(21\).  Any \(d\ge4\), any reflected
basepoint, any common-pole base order, or any extra gcd root makes the
inequality strict.

Thus the global route reduces (1) to the exact pair of equality forms
(47)--(48), but does not alone contradict them.  Sections 2--6 eliminate
precisely this remaining equality profile.

## 8. Zero, gcd, and nonopposite audit

Every exceptional class in (1) is repeated, so no exceptional value can
be zero.  The standing cyclic reduction also has \(\mu\ne0\).  Structural
admissibility gives

\[
 u-v\ne0,\qquad u+v\ne0,\qquad u+\mu\ne0,\qquad u-\mu\ne0 \tag{49}
\]

whenever the values involved are distinct classes.  These facts ensure
that the \(h_t\) are pairwise coprime, the six squared nodes in (21) are
distinct, all local cofactors in (6) and (36) are units, and every
denominator in (38)--(42) is nonzero.

The local gcd alternatives are exhausted in (10)--(11), including the
often missed order-two common-root case.  Polynomial gcds in the
three-dimensional intersection classification are retained as the factor
\(G\) in (19) and ruled out by the exact coefficients (20).  The dual
relation map has no kernel by the structural evaluation at \(-\mu\) in
(33).  Finally, the fibre polynomial (42) remains nonzero if
\(\lambda=0\).

## 9. Exact audit

[verify_live_three_zero_eighth_split_all_double_second_order_closure.py](../computations/verify_live_three_zero_eighth_split_all_double_second_order_closure.py)
checks all \(2520\) legal partial-pair cores, the exact double lift and
degree counts, every local gcd order in the six-node Wronskian bound, the
quadratic-product ranks and parity degree, the restriction coefficients
(20), the cubic dual identity (21), the relation-numerator degree drop,
the differential and pencil determinant identities, the two triple-pole
residues, the partition swap and fibre degree, and the unique global
\(K/J\) Wronskian equality frontier.
