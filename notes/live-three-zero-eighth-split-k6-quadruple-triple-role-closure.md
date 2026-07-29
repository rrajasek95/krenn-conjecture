# The eighth split: closure of the final (4^3 3^4) profile

## 1. Result

Work on the no-extra-singular live-three-zero stratum at

\[
                 (h,k;p)=(8,6;14).
\]

The only selection-free collision profile left by the general
fixed-numerator theorem is

\[
                             4^3 3^4.                    \tag{1}
\]

Write (a,b,c,d) for the four exact-triple values and (q_1,q_2,q_3)
for the three quadruple values.  All seven values are nonzero, distinct,
pairwise nonopposite, and separated from the common pole.

**Theorem 1.1.**  Profile (1) is impossible.

Choose three of the exact triples, give them role three, and give one
quadruple role one.  The formal role total is (3+3+3+1=h+2).
Lowering any two of the four layers gives a legal (h)-label core.  Its
nonzero Hermite residual lifts into one kernel in

\[
                             \mathbb C[z]_{\le5}.        \tag{2}
\]

The three order-three rows and one order-one row bound that kernel by four
dimensions.  The six pair lifts force dimension at least three.  In
dimension three, their opposite-root incidence makes the kernel
projectively even.  The role-one lift plane then forces the primitive
normal form

\[
                     (z+q)\mathbb C[z^2]_{\le2},        \tag{3}
\]

but the exact reflected first-order row at (-q) does not annihilate
(3).  Thus the kernel has dimension four.  Its four rows have a
two-dimensional relation space.  The complementary polynomial has only
four value classes, so exact differentiation maps that relation space
injectively into the constants, an impossibility.

## 2. The ((3,3,3,1)) formal target

Fix three exact-triple values (x_1,x_2,x_3) and one quadruple value
(q).  Let (y) be the fourth triple and let (u,v) be the other two
quadruple values.  After removing the formal roles, the complementary
polynomial has profile

\[
                    A(z)=(z-q)^3(z-u)^4(z-v)^4(z-y)^3.  \tag{4}
\]

In particular,

\[
                         \deg A=p=14,
             \qquad \deg\operatorname {rad}(A)=4.       \tag{5}
\]

Put

\[
 f_i(z)=z^2-x_i^2\quad(1\le i\le3),
 \qquad f_q(z)=(z-q)(z+q)^2.                             \tag{6}
\]

Lower two formal layers.  If two triple layers are lowered, the resulting
core has roles ((2,2,3,1)), represents four value classes, and has a
nonzero Hermite residual of degree at most one.  If a triple and the
role-one layer are lowered, the resulting core has roles ((2,3,3)),
represents three classes, and has a nonzero constant residual.  Every core
is legal: lowering an exact triple leaves its nonzero singleton mate in
the complement.

Restoring a lowered already represented layer at (x_i) multiplies its
rational dependence by (f_i).  Restoring the omitted role-one layer at
(q) multiplies it by (f_q).  Hence the six nonzero lifts have the form

\[
 \begin{aligned}
  P_{ij}&=f_if_j\ell_{ij}, &&\deg\ell_{ij}\le1
                         &&(1\le i<j\le3),\\
  P_{iq}&=\gamma_i f_if_q,&&\gamma_i\ne0
                         &&(1\le i\le3),                \tag{7}
 \end{aligned}
\]

and all have degree at most five.

For a polynomial (P\in\mathbb C[z]_{\le5}), set

\[
 F_P(z)={A(z)P(z)\over
       (z+\mu)^7\prod_{i=1}^3(z+x_i)^4(z+q)^2}.          \tag{8}
\]

The selected-pole rows are the four exact functionals

\[
 J_i(P)=(B_iP)^{(3)}(-x_i),\qquad
 J_q(P)=(B_qP)'(-q),                                    \tag{9}
\]

where every displayed local unit (B_i,B_q) is regular and nonzero at its named
point.  Define

\[
 K=\bigcap_{i=1}^3\ker J_i\cap\ker J_q
       \subseteq\mathbb C[z]_{\le5},
 \qquad W=\operatorname {span}\{P_{ij},P_{iq}\}.       \tag{10}
\]

The exact lift identities give (W\subseteq K).

## 3. The kernel has dimension at most four

Let (D=\dim K).  An exact order-(m) row contributes Wronskian weight
at least (max(0,D-m)).  After removal of the polynomial gcd this gives

\[
 3\max(0,D-3)+\max(0,D-1)\le D(6-D).                    \tag{11}
\]

The usual gcd correction cannot weaken (11).  If the gcd has order
(t\le m) at an order-(m) row, the reduced row has exact order (m-t)
while the degree cap drops by (Dt); if (t>m), the row becomes automatic
but the cap still drops by (Dt).  Roots away from the four row nodes only
lower the cap.  Thus (11) remains necessary in every gcd stratum.

For (D=5), its left and right sides are respectively (10) and (5),
and the gap only grows at (D=6).  Therefore

\[
                              \dim K\le4.                \tag{12}
\]

For each formal layer (r\in\{x_1,x_2,x_3,q\}), put

\[
                         U_r=W\cap f_r\mathbb C[z].      \tag{13}
\]

Every (U_r\cap U_s) contains the corresponding nonzero lift.  No
(U_r) is a line: otherwise its three pair lifts would be proportional,
so their generator would be divisible by all four pairwise-coprime factors
in (6), whose product has degree

\[
                              2+2+2+3=9>5.              \tag{14}
\]

If (dim W=2), all four (U_r)'s would equal (W), giving the same
impossible common divisor.  Hence

\[
                              \dim W\ge3.                \tag{15}
\]

## 4. The reflected row excludes dimension three

Assume (dim K=3).  Equations (12), (15), and (W\subseteq K) give
(W=K), and every (U_r) has dimension at least two.  Choose a basis

\[
                         {\bf P}(z)=(P_0(z),P_1(z),P_2(z)).
\]

At every one of the four nonzero layer values (r), the evaluation
vectors ({\bf P}(r)) and ({\bf P}(-r)) annihilate the same plane
(U_r), and are therefore proportional.  The parity minors

\[
 M_{ij}(z)=P_i(z)P_j(-z)-P_i(-z)P_j(z)                  \tag{16}
\]

are odd of degree at most nine.  They vanish at the eight distinct points

\[
               \pm x_1,\ \pm x_2,\ \pm x_3,\ \pm q
\]

and, by oddness, at zero.  Hence all three minors are constant multiples
of the same degree-nine divisor.  Equivalently,

\[
                     {\bf P}(z)\mathbin\times{\bf P}(-z)
                                =D_0(z){\bf c}.          \tag{17}
\]

The cross product is orthogonal to ({\bf P}(z)).  If
({\bf c}\ne0), equation (17) gives a constant linear relation among the
basis polynomials.  Thus ({\bf c}=0), and all parity minors vanish.

Remove the gcd (G) of (K).  Primitivity now makes the proportionality
between the vectors at (z) and (-z) a constant sign.  The odd sign
would leave a common factor (z), so the sign is even.  Consequently

\[
                         K=G(z){\cal E}(z^2),            \tag{18}
\]

where ({\cal E}) is a three-dimensional space.  Three independent even
polynomials require degree at least four.  Since (K\subseteq\mathbb
C[z]_{\le5}),

\[
                              \deg G\le1,
 \qquad {\cal E}=\mathbb C[s]_{\le2}.                  \tag{19}
\]

The three lifts (P_{iq}=\gamma_i f_if_q) span the two-plane

\[
                 f_q\langle1,z^2\rangle\subseteq U_q.  \tag{20}
\]

If (G) had no zero at (-q), divisibility by the double factor
((z+q)^2) would put two independent quadratics in (s=z^2) in the
one-dimensional space divisible by ((s-q^2)^2).  If the sole zero of
(G) were at (q) or elsewhere, the same conclusion would hold at
(-q).  Therefore (18)--(20) force

\[
                              G(z)\doteq z+q.             \tag{21}
\]

Here (doteq) means equality up to a nonzero scalar.  But the exact
role-one row in (9) must annihilate every

\[
                         P=(z+q)E(z^2),\qquad \deg E\le2.
\]

Since (P(-q)=0), that row reduces to

\[
                  J_q(P)=B_q(-q)P'(-q)
                        =B_q(-q)E(q^2),                 \tag{22}
\]

up to the same harmless nonzero normalization.  Taking (E=1) makes
(22) nonzero, a contradiction.  Thus dimension three is impossible, and

\[
                              \boxed{\dim K=4}.          \tag{23}
\]

## 5. Two relations cannot map into the constants

The four rows (9) act on the six-dimensional space
(mathbb C[z]_{\le5}).  Equation (23) gives row rank two, hence a
two-dimensional relation space ({\cal R}).

For a relation (c\in{\cal R}), sum the corresponding principal parts of
the rational function

\[
 \Omega(z)={A(z)\over
       (z+\mu)^7\prod_{i=1}^3(z+x_i)^4(z+q)^2}.          \tag{24}
\]

After removing the common-pole factor, its selected denominator has degree
(4+4+4+2=14).  Since the relation annihilates
(1,z,\ldots,z^5), the resulting numerator (N_c) has degree at most

\[
                              14-(5+2)=7.                \tag{25}
\]

Distinct principal-part supports make (c\mapsto N_c) injective.

Put (g=A/\operatorname {rad}(A)), (R=A/g), and (D_A=A'/g).  By
(4)--(5),

\[
                     \deg R=4,\qquad\deg D_A=3,
                     \qquad\operatorname {LC}(D_A)=14. \tag{26}
\]

Exact differentiation gives

\[
 {d\over dz}{(z+\mu)^7N\over A}
 ={(z+\mu)^6g\over A^2}{\cal E}_A(N),                  \tag{27}
\]

where

\[
 {cal E}_A(N)=R\bigl((z+\mu)N'+7N\bigr)
                         -(z+\mu)D_AN.                  \tag{28}
\]

For (n=\deg N\le7), the nominal leading coefficient is

\[
                         n+7-\deg A=n-7.                \tag{29}
\]

It cancels at (n=7), while (n\le6) already gives degree at most ten.
Thus

\[
                         \deg {\cal E}_A(N)\le10.       \tag{30}
\]

The selected contact orders in the principal-part relation imply

\[
       \prod_{i=1}^3(z+x_i)^3(z+q)\mid {\cal E}_A(N).   \tag{31}
\]

The divisor in (31) also has degree ten, so

\[
       {\cal E}_A(N)=\gamma_N
              \prod_{i=1}^3(z+x_i)^3(z+q)              \tag{32}
\]

for one scalar (gamma_N).  The map (N\mapsto\gamma_N) is injective:
if (gamma_N=0), equation (27) makes ((z+\mu)^7N/A) constant;
evaluation at (-\mu), where (A(-\mu)\ne0), makes that constant and
then (N) zero.

Thus the two-dimensional relation space ({\cal R}) injects into the
one-dimensional space of constants, a contradiction.  This proves
Theorem 1.1.

## 6. Exact audit and consequence

[verify_live_three_zero_eighth_split_k6_quadruple_triple_role_closure.py](../computations/verify_live_three_zero_eighth_split_k6_quadruple_triple_role_closure.py)
checks the role and complement counts, all six legal pair drops, lift
degrees and coprimality, the Wronskian dimension bound, the sharp parity
divisor, the reflected-row normal form, the two-relation count, and the
degree-ten differential cancellation.

This is the last selection-free no-extra-singular (h=8) collision profile
left in the audited eighth-split ledger; together with the previously
promoted closures, it completes that ledger.
