# Independent audit: the \(p=28\) all-quartic pure-fifth-pole frontier

## 1. Verdict and exact scope

This audit independently reconstructs
[the all-quartic pure-fifth-pole frontier](live-three-zero-higher-split-p28-all-quartic-pure-fifth-pole-frontier.md).
The theorem and the twelve displayed formal models are sound.

The important scope qualification is essential.  The result constructs
and classifies one saturated **selected-row** relation system.  It does
not reconstruct the unreduced response tensor, prove that the formal
rows arise from one collision-profile solution of the original
equations, close the profile \(4^7 1\), or give a counterexample to
Krenn's conjecture.

There are two harmless points of exposition worth making explicit.
First, the claim that \(N/(Q^3H^2)\) is a scalar multiple of the
prescribed principal part is a statement at each selected pole, not a
global proportionality of rational functions.  Section 4 below proves
that local statement.  Second, an exact section found in the linear
system may initially be defined only up to a nonzero scalar; dividing by
its leading coefficient makes the factor \(H\) monic, as required if
\(H\) is written literally as a product of monic linear factors.  Neither
point changes the theorem or any model.

## 2. Independent bookkeeping

At the first six-kernel threshold,

\[
                    p=28,\qquad h=28-k,\qquad 1\le k\le6.
                                                               \tag{1}
\]

For \(d=0,1,2\), the relevant residual tuple and its original profile are

\[
 (e,a,b,u)=(7,0,d,2-2d),
 \qquad 4^7 2^d1^{\,h+2-2d}.                               \tag{2}
\]

If only \(x\le d\) doubles were selected in role two, the formal
selection would require \(h+2-2x\) singleton classes, while (2) supplies
only \(h+2-2d\).  Therefore \(x\ge d\), so \(x=d\).  All doubles and all
singletons are forced into the stated roles.  In particular there is no
second moving-double family hidden in these tuples.

The selected system has

\[
 \begin{aligned}
 s&=h+2-2d,\\
 L&=d+s=h+2-d,\\
 D&=h+3-d=L+1,\\
 \deg(Q^3H^2)&=3d+2s=2h+4-d.
 \end{aligned}                                             \tag{3}
\]

A selected-row relation numerator therefore has degree at most

\[
             (2h+4-d)-(D+2)=h-1.                           \tag{4}
\]

For \(q=6\), the selected Wronskian gap is zero at every split in
(1), whereas for \(q=7\) it is twelve.  Thus every selected kernel has
dimension at most six.

Finally, the complement is \(4^7\), so

\[
              A=B^4,\qquad \deg B=7,\qquad \deg A=28.      \tag{5}
\]

The relation-space target is \(P_{7-4}=P_3\).  These identities recover
all role counts, degree bounds, and the three residual tuples in the
primary note.

## 3. Necessity of the pure fifth-pole identity

Put

\[
 F=(z+\mu)^kQ^2H,
 \qquad
 \mathcal E_{B,k}(N)
 =B\bigl((z+\mu)N'+(k+1)N\bigr)-4(z+\mu)B'N.              \tag{6}
\]

For a row relation with image \(S\in P_3\), exact differentiation gives

\[
 \frac d{dz}\left(\frac{(z+\mu)^{k+1}N}{B^4}\right)
       =\frac{FS}{B^5},
 \qquad
 \mathcal E_{B,k}(N)=Q^2HS.                              \tag{7}
\]

Fix a root \(a_i\) of \(B\), write

\[
 B=(z-a_i)B_i,
 \qquad U_i=\frac{F}{B_i^5},                              \tag{8}
\]

and note that \(U_i(a_i)\ne0\) by separation.  The right side of (7)
has local form

\[
                  \frac{U_i(z)S(z)}{(z-a_i)^5}.           \tag{9}
\]

Every derivative of a rational function has zero residue.  Applying
this to \(S=1,(z-a_i),(z-a_i)^2,(z-a_i)^3\), which are all in the full
image \(P_3\), gives successively

\[
 U_i^{(4)}(a_i)=U_i^{(3)}(a_i)
 =U_i''(a_i)=U_i'(a_i)=0.                                \tag{10}
\]

Thus \(F/B^5\) has only an order-five term at each of its seven finite
poles.  Since its numerator and denominator have degrees thirty and
thirty-five, respectively, there is no polynomial part at infinity.
Consequently

\[
 \frac F{B^5}=\sum_{i=1}^7\frac{c_i}{(z-a_i)^5},
 \qquad
 c_i=\frac{F(a_i)}{B_i(a_i)^5}\ne0,                      \tag{11}
\]

or equivalently

\[
                  F=\sum_{i=1}^7c_iB_i^5.                \tag{12}
\]

This proves necessity without a dimension heuristic: all four missing
Laurent coefficients at every quartic node are forced to vanish.

## 4. Sufficiency really reconstructs row relations

The main point requiring scrutiny is that a rational primitive must
recover relations among the original selected principal-part rows, not
merely solve (7).  The following local criterion makes that implication
exact.

Let

\[
 T=Q^3H^2,
 \qquad
 \Omega=\frac{B^4}{(z+\mu)^{k+1}T},
 \qquad
 R_N=\frac N{T},
 \qquad
 G_N=\frac{R_N}{\Omega}
      =\frac{(z+\mu)^{k+1}N}{B^4}.                       \tag{13}
\]

At a root of \(Q\), \(\Omega\) has a pole of order three.  Its complete
principal part is rescaled by one constant after multiplication by
\(G_N\) exactly when

\[
                   G_N-G_N(\alpha)=O((z-\alpha)^3).       \tag{14}
\]

At a root of \(H\), where the pole order is two, the corresponding
condition is

\[
                   G_N-G_N(\alpha)=O((z-\alpha)^2).       \tag{15}
\]

Differentiating (13) yields

\[
                  G_N'=\frac{(z+\mu)^k}{B^5}
                              \mathcal E_{B,k}(N).        \tag{16}
\]

All selected poles are disjoint from the roots of \(B(z)(z+\mu)\).
It follows immediately that (14)--(15) hold at every selected pole if
and only if

\[
                         Q^2H\mid\mathcal E_{B,k}(N).     \tag{17}
\]

Hence (17) says precisely that the principal part of \(R_N\) at each
selected pole is a scalar multiple of the one prescribed principal-part
row there.  This is the missing local-to-row step.

The remaining condition for a row relation is moment cancellation at
infinity.  By (3)--(4),

\[
        \deg N\le h-1
        \quad\Longrightarrow\quad
        R_N=O(z^{-D-2}).                                  \tag{18}
\]

Thus all \(D+1\) polynomial moments encoded by the selected rows vanish.
Conversely, those vanished moments give exactly the degree bound in
(4).  Since a proper rational function is the sum of its finite
principal parts, (14)--(18) establish a bijection between selected-row
relations and the numerators \(N\in P_{h-1}\) satisfying (17).  In
particular, a differential solution meeting the divisibility and degree
conditions is a genuine row relation.

Now suppose (11) holds.  For \(S\in P_3\), termwise integration gives

\[
 G_{0,S}=\sum_{i=1}^7c_i\sum_{j=0}^3
 \frac{S^{(j)}(a_i)}{j!(j-4)}(z-a_i)^{j-4},              \tag{19}
\]

with \(G_{0,S}'=FS/B^5\).  Normalize

\[
                         G_S=G_{0,S}-G_{0,S}(-\mu).       \tag{20}
\]

The derivative has a zero of order at least \(k\) at \(-\mu\), so
\(G_S\) has a zero of order at least \(k+1\) there.  Moreover \(B^4G_S\)
is a polynomial: multiplication by \(B^4\) clears every pole in (19).
Therefore

\[
                         N_S=\frac{B^4G_S}{(z+\mu)^{k+1}} \tag{21}
\]

is a polynomial.  Since \(G_S\) is bounded at infinity,

\[
                         \deg N_S\le27-k=h-1.             \tag{22}
\]

Equations (19)--(21) give

\[
                         \mathcal E_{B,k}(N_S)=Q^2HS,     \tag{23}
\]

so (17), (18), and the preceding bijection show that \(N_S\) is an
actual selected-row relation.

Finally, \(N\mapsto \mathcal E_{B,k}(N)/(Q^2H)\) is injective on relation
numerators.  If its image were zero, (16) would make \(G_N\) constant;
evaluation at \(-\mu\), where \(B(-\mu)\ne0\), forces the constant and
then \(N\) to vanish.  Hence the four choices \(S=1,z,z^2,z^3\) give four
independent relations and fill \(P_3\).  With \(L\) rows on \(P_D\), the
selected kernel dimension is

\[
                 (D+1)-(L-4)=6.                           \tag{24}
\]

This verifies both sufficiency and the exact \(q=6\) claim.

## 5. Independent exact models and rank ranges

For the concrete audit, take

\[
 B=\prod_{a=1}^7(z-a),\qquad -\mu=10,
 \qquad q_1=8,\quad q_2=9.                               \tag{25}
\]

The fifth-power system

\[
 \mathcal V_B=\operatorname{span}
 \left\{\left(\frac B{z-a_i}\right)^5:1\le i\le7\right\} \tag{26}
\]

has dimension seven because evaluation at the seven \(a_i\)'s is
diagonal with nonzero diagonal.  Order \(k\) at \(10\) and order two at
each of the first \(d\) points among \(8,9\) impose \(k+2d\) confluent
linear conditions.  The independent checker recomputes the exact ranks
at the fixed rational nodes.  The rank is

\[
                         \min(7,k+2d),                    \tag{27}
\]

for every \(d=0,1,2\) and \(1\le k\le6\).  Thus a nonzero section is
available exactly for

\[
 \begin{array}{c|c}
 d&k\\ \hline
 0&1,2,3,4,5,6\\
 1&1,2,3,4\\
 2&1,2.
 \end{array}                                               \tag{28}
\]

For all twelve pairs, the checker independently chooses and normalizes
an exact rational section.  It verifies that every fifth-pole
coefficient is nonzero and factors the section as

\[
          F=(z-10)^k\prod_{j=1}^d(z-q_j)^2H,              \tag{29}
\]

where \(H\) is monic, has the required degree \(h+2-2d\), is squarefree,
is coprime to \(H(-z)\), and is disjoint from both signs of every fixed
node.  It then constructs all four normalized primitives, checks (23)
as an exact polynomial identity, checks (14) at every rational repeated
pole and (15) collectively at every root of \(H\), checks (18), and
recovers kernel dimension six.

For the unmodelled fixed-node loads

\[
        (d,k)=(1,5),(1,6),(2,3),(2,4),(2,5),(2,6),        \tag{30}
\]

the confluent matrix has full column rank.  This says only that the
chosen rational nodes do not supply a model.  It does not rule out a
special rank-drop locus when all nodes vary, exactly as stated in the
primary note.

## 6. Executable audit

[verify_live_three_zero_higher_split_p28_all_quartic_pure_fifth_pole_frontier_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_all_quartic_pure_fifth_pole_frontier_independent_audit.py)
does not import the primary checker.  It reconstructs all confluent
ranks and forced-role counts, builds all twelve separated monic sections,
checks the pure fifth-pole congruences, and verifies the full
principal-part and moment criteria for the four row relations in every
model.
