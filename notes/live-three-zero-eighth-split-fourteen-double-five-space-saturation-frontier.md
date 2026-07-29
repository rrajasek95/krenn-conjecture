# The eighth split: fourteen-double five-space saturation frontier

## 1. Exact surviving branch

The decic four-space theorem leaves only one branch of the stable pure
profile

\[
                         (h,k;\lambda)=(8,10;2^{14}).   \tag{1}
\]

Fix four double values and let \(P\) be the ten-value pool.  For every
\(a\in P\), the fifth-choice relation pencil lifts to

\[
 {\cal U}_a=A_a{\cal S}_a\subseteq{\cal K}
 \subseteq\mathbb C[z]_{\leq10},\qquad
 A_a=(z+a)^2(z-a)^3,qquad \dim{\cal U}_a=2.           \tag{2}
\]

The previous note excludes \(\dim{\cal K}\leq4\), while the corrected
Wronskian estimate gives \(\dim{\cal K}\leq5\).  Hence a hypothetical
profile has

\[
                         \boxed{\dim{\cal K}=5}.        \tag{3}
\]

This note records every equality forced by (3), determines the exact
pair-intersection graph constraint, and shows why that graph alone cannot
close the branch.  The remaining obstruction is a genuinely polynomial
coupling between the osculating plane at \(a\) and the opposite two-jet at
\(-a\).

## 2. Wronskian equality

There are ten exact order-two rows.  For a gcd-free \(d\)-space in the
decics, forced Wronskian weight minus the degree cap is

\[
 10(d-2)-d(11-d)=d^2-d-20.                             \tag{4}
\]

At \(d=5\), both sides are thirty.  Every gcd correction is strict.  A gcd
root away from the ten nodes lowers the degree cap; at a node, a simple
gcd root adds six to the deficit, a double gcd root is incompatible with
gcd removal, and order at least three adds at least twelve.  Therefore

\[
 \gcd({\cal K})=1,qquad
 \boxed{\operatorname {Wr}({\cal K})
       =c\prod_{a\in P}(z-a)^3},\quad c\ne0.            \tag{5}
\]

There are no other finite Wronskian roots and no ramification at infinity.
If \(d_0<\cdots<d_4\leq10\) are the polynomial degrees of a row-reduced
basis, then
\(\deg\operatorname {Wr}=d_0+\cdots+d_4-10=30\).  Equality in the degree
cap therefore gives

\[
 (d_0,\ldots,d_4)=(6,7,8,9,10),\qquad
                 {\cal K}\cap\mathbb C[z]_{\leq5}=0.   \tag{5a}
\]

Let \(\nu_0<\cdots<\nu_4\) be the vanishing sequence of \({\cal K}\) at
\(a\).  Gcd-freeness gives \(\nu_0=0\).  The exact order-two row makes the
two-jet image have rank at most two, so at least three \(\nu_i\) are at
least three.  Its Wronskian weight is exactly three by (5).  The unique
possibility is

\[
                         \boxed{(\nu_0,\ldots,\nu_4)
                                      =(0,1,3,4,5).}    \tag{6}
\]

Consequently

\[
 {\cal V}_a:=\{F\in{\cal K}:\operatorname {ord}_aF\geq3\}
                         \quad\hbox{has dimension }3,  \tag{7}
\]

and \({\cal U}_a\subset{\cal V}_a\) is a hyperplane.  Since every member
of \({\cal U}_a\) also has order at least two at \(-a\),

\[
 \operatorname {rank}\bigl(j^1_{-a}|_{{\cal V}_a}\bigr)\leq1.     \tag{8}
\]

Equivalently, after dividing \({\cal V}_a\) by \((z-a)^3\), its residual
three-space has Wronskian weight at least two at \(-a\), with the usual
local-gcd correction.  Condition (8), not merely the dimensions in (7),
is the extra paired-point datum still available for a closure.

## 3. Pair intersections and their graph

For distinct \(a,b\in P\), structural noncollision gives
\(\gcd(A_a,A_b)=1\).  Since the product already has degree ten,

\[
 {\cal U}_a\cap{\cal U}_b
   \in\left\{0,\mathbb C A_aA_b\right\}.               \tag{9}
\]

Define a graph \(G\) on \(P\) by declaring \(ab\) to be an edge precisely
when the second alternative holds.

**Lemma 3.1 (degree-two intersection graph).**

\[
                         \boxed{\Delta(G)\leq2}.        \tag{10}
\]

Indeed, if \(a\) had three neighbours \(b,c,d\), then the two-plane
\({\cal U}_a\) would contain

\[
                         A_aA_b,\quad A_aA_c,\quad A_aA_d.
\]

After division by \(A_a\), this would make \(A_b,A_c,A_d\) dependent.  But
their (z^5,z^4,z^3) coefficient minor is

\[
 -2(b-c)(b-d)(c-d)\ne0.                               \tag{11}
\]

Thus \(G\) is a disjoint union of paths and cycles.  At the level of the
three-planes, dimension alone gives

\[
 \dim({\cal V}_a\cap{\cal V}_b)\geq1,                 \tag{12}
\]

and every member of that intersection is divisible by
\((z-a)^3(z-b)^3\).  An edge occurs only when its common line also acquires
the two opposite double zeros.

The upper bound (10) does not force even one edge.

## 4. An exact empty-graph Grassmann model

The absence of a lower edge bound is not a weakness of dimension counting;
there is an exact rational model with ten nodes.  Let \(K_0=\mathbb Q^5\)
and put

\[
 v(t)=(1,t,t^2,t^3,t^4)^T,qquad
 U_t=\langle v(t),v'(t)\rangle,qquad
 V_t=\langle v(t),v'(t),v''(t)\rangle.                 \tag{13}
\]

For \(t\ne u\), the confluent Vandermonde minors are

\[
 \det[v(t),v'(t),v(u),v'(u)]_{0,1,2,3}=(t-u)^4,        \tag{14}
\]

and

\[
 \det[v(t),v'(t),v''(t),v(u),v'(u)]=2(t-u)^6.          \tag{15}
\]

Hence

\[
 \dim U_t=2,\quad \dim V_t=3,\quad U_t\subset V_t,
 \quad U_t\cap U_u=0,\quad \dim(V_t\cap V_u)=1.      \tag{16}
\]

Taking \(t=1,\ldots,10\) gives an exact ten-node empty graph.  The abstract
rank-one paired jet can also be included: in the basis
(v(t),v'(t),v''(t)), let \(\phi_t\) kill the first two vectors and send
the third to one, and define \(J_t(x)=(\phi_t(x),0)\).  Then

\[
                         \ker J_t=U_t,qquad\rank J_t=1.              \tag{17}
\]

Thus (7), (8), (9), and (12), regarded only as Grassmann and rank
incidences, admit an exact empty-edge realization.  This model is not
claimed to be a decic polynomial kernel: it deliberately omits the fact
that all \(J_t\) must arise from the same polynomial evaluation and
derivative maps at the paired points \(-t\).  That omitted common origin is
exactly what a positive continuation must exploit.

There is also no Schubert dimension contradiction in the local data.  The
condition (6) is the codimension-three class \(\sigma_{111}\) in
\(\operatorname {Gr}(5,11)\).  The exact Pieri recursion gives

\[
                         [\sigma_{6^5}]\,\sigma_{111}^{10}=3396>0.   \tag{18}
\]

This does not incorporate (8), but it confirms that ten weight-three
osculating conditions have precisely the expected top dimension rather
than an automatic excess-intersection contradiction.

## 5. What can still close the branch

The intersection graph is therefore a useful upper-structure invariant,
not a contradiction.  Any successful next lemma must retain at least one
of the following common polynomial features:

1. the ten rank-one maps (j^1_{-a}|_{{\cal V}_a}) all come from the same
   degree-ten ambient coordinate;
2. the Wronskian has the exact global value (5), with no residual divisor;
3. for every pair, the unavoidable line in
   \({\cal V}_a\cap{\cal V}_b\) has a quartic quotient after removing the
   two triple factors, and an edge is the exceptional quotient that gains
   both prescribed opposite double zeros.

A promising formulation is therefore a paired-osculating Schubert lemma,
not a lower bound on the number of edges of \(G\).

## 6. Relation to a stable all-order mechanism

For a pure stable family with \(p\) pool values, a \(d\)-space reaches the
same exact order-two Wronskian equality precisely when

\[
 p(d-2)=d(p+1-d)\quad\Longleftrightarrow\quad
                         p=\binom d2.                  \tag{19}
\]

At every such triangular threshold the minimal local vanishing sequence
is

\[
                         (0,1,3,4,\ldots,d).            \tag{20}
\]

The present \(p=10,d=5\) case is the first five-space member; the next is
\(p=15,d=6\).  Between them, a five-space has Wronskian slack

\[
                         2p-20,                         \tag{21}
\]

and the ambient common-multiple space for two lift factors has dimension
\(p-9\), rather than the single line at \(p=10\).  Thus the equality pattern
suggests a stable triangular Schubert tower, but not a stable contradiction.
An all-order proof would need a paired-point theorem uniform in the slack
divisor and in these growing pair-intersection spaces.

## 7. First common-coordinate reductions

Before the audit, two first common-coordinate reductions sharpen the open
problem.

### 7.1 Parity ranks two and three are impossible

Write \(F=E(w)+zO(w)\), with \(E\in\mathbb C[w]_{\leq5}\) and
\(O\in\mathbb C[w]_{\leq4}\).  The two lift members at \(a\) give

\[
 \operatorname {rank}
 \begin{pmatrix}E(s)\\E'(s)\\O(s)\\O'(s)\\E''(s)+aO''(s)
 \end{pmatrix}\leq3,qquad s=a^2.                     \tag{22}
\]

Since \(0\notin P\), (5) makes the fourth jet at zero nonsingular.  A
pure-even subspace injects there into the three even jet coordinates, so
the odd projection rank \(r_o\) is at least two.

If \(r_o=2\), the Wronskian of the two independent odd quartics has degree
at most six.  At at least four pool squares, \(O,O'\) are independent.
At each such square (22) makes the two-jet image of the three-dimensional
pure-even kernel have rank at most one.  After the local gcd correction,
its minimum vanishing sequence is \((0,3,4)\), of Wronskian weight four.
Four squares therefore cost at least sixteen units, while a three-space
of quintics has Wronskian degree at most nine.

If \(r_o=3\), at most three squares have
\(\operatorname {rank}(O,O')\leq1\).  At each of the other at least seven
squares, the rows \(E,E',E''\), projected to the two-dimensional pure-even
kernel, have rank at most one.  Thus the Wronskian of its two quintics and
its derivative both vanish.  The resulting seven double roots exceed the
degree-eight cap.  Hence

\[
                         \boxed{r_o\in\{4,5\}.}         \tag{23}
\]

The rank-four case has one pure-even quintic \(A\) and an odd hyperplane;
the rank-five case is the graph of a map
\(\mathbb C[w]_{\leq4}\to\mathbb C[w]_{\leq5}\).  These are the two exact
remaining parity branches.

### 7.2 The paired five-jet covariant

For a basis row \(F=(F_1,\ldots,F_5)\), define

\[
 D_{\cal K}(x)=\det
 \begin{pmatrix}
 F(x)\\F'(x)\\F''(x)\\F(-x)\\F'(-x)
 \end{pmatrix}.                                       \tag{24}
\]

For a monomial Plücker coordinate indexed by
\(0\leq i_1<\cdots<i_5\leq10\), its contribution to (24) is a constant
times

\[
                         x^{i_1+\cdots+i_5-4}.          \tag{25}
\]

The smallest and largest exponents are six and thirty-six.  Thus
\(D_{\cal K}=x^6\widetilde D_{\cal K}\), with
\(\deg\widetilde D_{\cal K}\leq30\).  At every \(a\in P\), the two
columns supplied by \({\cal U}_a\) vanish in all five rows of (24), so the
matrix has corank at least two.  Its determinant consequently has a double
zero.  With \(C(x)=\prod_{a\in P}(x-a)\),

\[
 \boxed{D_{\cal K}(x)=x^6C(x)^2R(x),qquad\deg R\leq10,}              \tag{26}
\]

where \(R\) is allowed to be zero.

The new residual \(R\) is not determined by the Wronskian \(C^3\) at the
linear Plücker level.  For example, the monomial index sets

\[
 (0,1,2,3,6),qquad(0,1,2,4,5)
\]

contribute to the same degree of the Wronskian, but the ratio of their
coefficients in \(x^{-6}D_{\cal K}\) and in the Wronskian is respectively
\(4/45\) and \(-4/45\).  Any comparison of \(R\) with \(C\) must therefore
use the Grassmann--Plücker relations or the exact residue realization,
not only (5).

The full paired rank condition does, however, determine \(R\) up to one
remaining degenerate alternative.  Elementary row operations between the
five jets in (24) and the parity rows in (22) give the exact identity

\[
 D_{\cal K}(x)=-64x^6J(x),\qquad
 J(x)=\det\begin{pmatrix}
 E\\E'\\O\\O'\\E''+xO''
 \end{pmatrix}_{w=x^2}.                               \tag{27}
\]

Write \(J=J_0(w)+xJ_1(w)\).  Every four-by-four minor of
\((E,E',O,O')\) has degree at most fourteen and vanishes at all ten pool
squares.  Hence

\[
 \Delta(w)=\prod_{a\in P}(w-a^2)=C(x)C(-x)             \tag{28}
\]

divides both \(J_0\) and \(J_1\).  On the other hand, (26)--(27) give
\(C(x)^2\mid J(x)\).  Structural noncollision makes \(C(x)\) and \(C(-x)\)
coprime, while \(\deg_xJ\leq30\).  Therefore

\[
 \boxed{J\equiv0\quad\hbox{or}\quad
        J(x)=\kappa C(x)^2C(-x),\qquad\kappa\ne0.}      \tag{29}
\]

In the nonzero branch the residual in (26) is exactly a scalar multiple of
\(C(-x)\).  Equivalently,

\[
\begin{aligned}
 J_0(w)&={\kappa\over2}\Delta(w)(C(x)+C(-x)),\\
 J_1(w)&={\kappa\over2x}\Delta(w)(C(x)-C(-x)).         \tag{30}
\end{aligned}
\]

Thus the earlier unequal Plücker weights explain why the Wronskian alone
does not give (29), while the four-row incidence supplies exactly the
missing factor.  In fact the globally degenerate alternative in (29) is
impossible.  Let

\[
 P(w)=*\bigl(E\wedge E'\wedge O\wedge O'\bigr)
                         =\Delta(w)Q(w).               \tag{31}
\]

The fourth jet at zero is nonsingular, so the first four parity rows are
independent at \(w=0\); hence \(P\ne0\) and \(Q\ne0\).  If \(J\equiv0\),
then \(P\cdot(E''+xO'')=0\) for both signs of \(x\).  Thus

\[
                         Q\cdot E''=Q\cdot O''=0       \tag{32}
\]

identically, in addition to the four cofactor orthogonalities in (31).
For an independent parameter \(u\), put

\[
                         G_u(z)=\sum_{j=1}^5Q_j(u)F_j(z).             \tag{33}
\]

All even and odd derivatives through order two in the square variable
vanish at \(z^2=u\), so

\[
 G_u(z)=(z^2-u)^3\bigl(H_0(z)+uH_1(z)\bigr),\qquad
                         \deg H_i\leq4.                \tag{34}
\]

Here \(\deg_uQ\leq4\), which explains the affine quotient in \(u\).  The
\(u^4\) coefficient of (34) is \(-H_1\in{\cal K}\).  Equation (5a) forces
\(H_1=0\); then the \(u^3\) coefficient is
\(-H_0\in{\cal K}\), so \(H_0=0\).  This makes \(G=0\), contradicting
\(Q\ne0\) and the independence of the basis \(F_j\).  Therefore

\[
 \boxed{J(x)=\kappa C(x)^2C(-x),\qquad\kappa\ne0.}     \tag{35}
\]

### 7.3 Odd projection rank four is impossible

Suppose \(r_o=4\).  Choose a basis adapted to the one-dimensional
pure-even kernel and write

\[
 E=(T,A),\qquad O=({\bf O},0),\qquad
 R=A'T-AT',\qquad M=*(R\wedge{\bf O}\wedge{\bf O}').
\]

Here \(T,R,{\bf O}\) have four components and \(A\ne0\).  A direct
determinant reduction of (27) gives

\[
 \boxed{A J
   =\det\!\begin{pmatrix}R\\{\bf O}\\{\bf O}'\\
              R'-xA{\bf O}''\end{pmatrix}
   =M\mathbin{\cdot}R'-xA\,M\mathbin{\cdot}{\bf O}''.} \tag{36}
\]

At every pool square \(s=a^2\), the full five-row matrix in (22) has rank
at most three.  In particular \(M(s)=0\), so

\[
                         M(w)=\Delta(w)Q(w).           \tag{37}
\]

Every component of \(R=A'T-AT'\) has degree at most eight: the only
putative degree-nine term cancels.  A two-function Wronskian of quartics
has degree at most six.  Thus every component of \(M\) has degree at most
fourteen, and

\[
                         \deg Q_i\leq4.                \tag{38}
\]

Call a square \(s\) bad when
\(\operatorname {rank}({\bf O}(s),{\bf O}'(s))\leq1\).
The four-space spanned by the components of \({\bf O}\) is a hyperplane
in \(\mathbb C[w]_{\leq4}\), whose four-function Wronskian has degree at
most four.  At a gcd-free bad point the least vanishing sequence is
\((0,2,3,4)\), of weight three; a base point costs weight four.
Consequently at most one of the ten pool squares is bad.

At a regular pool square, the rank-three condition says that both
\(R\) and \(R'-aA{\bf O}''\) lie in
\(\langle{\bf O},{\bf O}'\rangle\).  Differentiating the exterior
product defining \(M\), and using the simplicity of the root of
\(\Delta\), gives

\[
 \Delta'(s)Q(s)=M'(s)
   \in\mathbb C\,*({\bf O}''\wedge{\bf O}\wedge{\bf O}').
\]

It follows that \(Q(s)\mathbin{\cdot}{\bf O}''(s)=0\).  The scalar
\[
                         L(w)=Q(w)\mathbin{\cdot}{\bf O}''(w)
\]
has degree at most \(4+2=6\), but it vanishes at at least nine pool
squares.  Hence \(L\equiv0\).

Put
\[
 C_o(w)=\frac{C(x)-C(-x)}{2x}.
\]
The odd part of (36), followed by (35), now reads

\[
 -\Delta\,Q\mathbin{\cdot}{\bf O}''
       =J_1=\kappa\Delta C_o.                          \tag{39}
\]

Thus \(C_o=0\), so \(C(x)=C(-x)\).  This would make the nonzero root set
\(P\) invariant under \(a\mapsto-a\), contrary to structural
noncollision.  Therefore

\[
                         \boxed{r_o\ne4.}              \tag{40}
\]

### 7.4 Odd projection rank five is impossible

It remains to close \(r_o=5\).  Normalize the odd projection to

\[
 {\bf O}(w)=(1,w,w^2,w^3,w^4),
\]

and regard the even projection as a linear operator

\[
 T:\mathbb C[u]_{\leq4}\longrightarrow\mathbb C[w]_{\leq5},
 \qquad {\cal K}=\{(Tq)(w)+zq(w):q\in\mathbb C[w]_{\leq4}\}.        \tag{41}
\]

For the moving Taylor polynomials \(e_k(u,w)=(u-w)^k\), put

\[
\begin{aligned}
 b_k(w)&=(T e_k)(w),\\
 L&=(b_2,b_3,b_4),\\
 M_k&=b_k'+k b_{k-1},\qquad M=(M_2,M_3,M_4),\\
 N_k&=M_k'+k M_{k-1},\qquad N=(N_2,N_3,N_4).
\end{aligned}                                                     \tag{42}
\]

The correction terms account for differentiating the moving input basis:
\(M_k=(T'e_k)(w)\) and \(N_k=(T''e_k)(w)\).  The space
\(\langle e_2,e_3,e_4\rangle\) is exactly the kernel of the value and
first-derivative rows of \({\bf O}\), while its second-derivative row is
\(2(1,0,0)\).  Therefore, at every pool square \(s=a^2\), (22) restricts
to

\[
 \operatorname {rank}
 \begin{pmatrix}
 L(s)\\ M(s)\\ N(s)/2+a(1,0,0)
 \end{pmatrix}\leq1.                                  \tag{43}
\]

Set

\[
 \Pi=L\times M=(\Pi_0,\Pi_1,\Pi_2).
\]

The sharp degree caps are

\[
 \deg L_i\leq(7,8,9)_i,\qquad
 \deg M_i\leq(6,7,8)_i,\qquad
 \deg \Pi_i\leq(14,13,12)_i.
\]

Equation (43) makes \(\Pi\) vanish at all ten pool squares, and hence

\[
 \Pi=\Delta H,\qquad
 \deg(H_0,H_1,H_2)\leq(4,3,2).                         \tag{44}
\]

There is now a decisive moving-basis identity.  Direct differentiation,
using the definitions in (42), gives

\[
 \boxed{\Pi_0'=(L\times N)_0+3\Pi_1.}                 \tag{45}
\]

Indeed, \(\Pi_0=L_1M_2-L_2M_1\), and the four correction terms from
\(L_1',L_2',M_1',M_2'\) cancel except for
\(3(L_2M_0-L_0M_2)=3\Pi_1\).

At a pool square, (43) first gives \(\Pi_1(s)=0\).  It also gives
\[
 L(s)\times\bigl(N(s)/2+a(1,0,0)\bigr)=0.
\]
The first component of \(L\times(1,0,0)\) is zero, so
\((L\times N)_0(s)=0\).  Thus (45) yields \(\Pi_0'(s)=0\).  Since every
root of \(\Delta\) is simple, (44) now gives

\[
                         \Delta'(s)H_0(s)=0
\]

at all ten distinct pool squares.  But \(\deg H_0\leq4\), and therefore

\[
                         \boxed{H_0\equiv0.}           \tag{46}
\]

To identify this component invariantly, let
\[
 {\cal P}^\sharp=*(T(w)\wedge T'(w)\wedge{\bf O}\wedge{\bf O}')=\Delta Q,
\]
where \(T(w)\) denotes the row \(q\mapsto(Tq)(w)\).
Translation from the monomial basis to
\((1,u-w,(u-w)^2,(u-w)^3,(u-w)^4)\) is unipotent, and the last three
coordinates of \({\cal P}^\sharp\) in this basis are exactly \(L\times M\).
Consequently, if \(q_w(u)=\sum_iQ_i(w)u^i\), then

\[
 q_w(u)=(u-w)^2
 \bigl(H_0(w)+H_1(w)(u-w)+H_2(w)(u-w)^2\bigr).
\]

In particular,

\[
 Q\mathbin{\cdot}{\bf O}''
   =\left.\partial_u^2q_w(u)\right|_{u=w}=2H_0=0.      \tag{47}
\]

But (27), (35), and \({\cal P}^\sharp=\Delta Q\) say

\[
 \Delta\bigl(Q\mathbin{\cdot}T''
       +xQ\mathbin{\cdot}{\bf O}''\bigr)
       =J=\kappa\Delta\bigl(C_e(w)+xC_o(w)\bigr).
\]

Equation (47) forces \(C_o=0\).  As in the rank-four branch, this makes
\(C\) even and contradicts \(P\cap(-P)=\varnothing\).  Hence

\[
                         \boxed{r_o\ne5.}              \tag{48}
\]

Together, (23), (40), and (48) exclude every possible parity rank.
Thus the pure fourteen-double five-space branch is impossible.

Finally, the rational-normal-quartic model in Section 4 cannot itself lift
to the evaluation curve of \({\cal K}\).  Gcd-freeness makes the evaluation
map \(\phi:\mathbb P^1\to\mathbb P^4\) basepoint-free with
\(\phi^*\mathcal O(1)=\mathcal O(10)\).  A factorization through a rational
normal quartic would require \(10=4e\) for an integer covering degree \(e\).
Adding the missing two degrees as a common factor is forbidden by (5).
More generally, the only possible nonbirational nondegenerate factorization
has covering degree two and image degree five; at a branch point its
minimum pulled-back vanishing sequence has weight ten, incompatible with
(6).  Thus the actual evaluation curve is birational of degree ten.  This
is the first invariant that blocks the exact abstract empty-graph model;
the paired-coordinate argument above now excludes both remaining parity
branches.

## 8. Exact audit

[verify_live_three_zero_eighth_split_fourteen_double_five_space_saturation_frontier.py](../computations/verify_live_three_zero_eighth_split_fourteen_double_five_space_saturation_frontier.py)
checks the saturated Wronskian ledger, uniqueness of the vanishing sequence,
the degree-two graph lemma, the exact empty-graph rational-normal-quartic
configuration, the Pieri coefficient (3396), the triangular equality
formula (19), the parity-rank-two/three exclusions, every degree and
coefficient in the paired covariants (24)--(35), the rank-four exclusion
(36)--(40), and the moving-Taylor rank-five exclusion (41)--(48).
