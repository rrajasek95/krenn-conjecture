# The $p=28$ all-quartic core is a pure-fifth-pole frontier

## 1. Result and scope

Consider the last saturated baseline in the first selected six-kernel
ledger,

\[
                              4^7 1,
\]

and the three residual tuples

\[
 (e,a,b,u)=(7,0,0,2),\quad(7,0,1,0),\quad(7,0,2,-2).       \tag{1}
\]

Let $d=0,1,2$, respectively, be the number of selected exact doubles.
For every legal split put

\[
 p=28,\qquad h=28-k,\qquad s=h+2-2d.                       \tag{2}
\]

The complementary polynomial in the saturated selection is

\[
 A(z)=B(z)^4,\qquad B(z)=\prod_{i=1}^7(z-a_i),              \tag{3}
\]

and its relation four-space lies in

\[
                     \mathbb C[z]_{\leq 7-4}=\mathbb C[z]_{\leq3}.
\]

Thus the relation space is the complete cubic space.  That observation is
not itself contradictory.  The exact additional content is the following
pure-pole identity.

**Theorem 1.1 (pure-fifth-pole equivalence).**  Let

\[
 Q(z)=\prod_{j=1}^d(z+x_j),\qquad
 H(z)=\prod_{r\in R}(z+r),\qquad
 F(z)=(z+\mu)^kQ(z)^2H(z).                                \tag{4}
\]

Assume all displayed nodes satisfy the standard separation hypotheses.
The saturated relation construction has image

\[
                         \mathcal S=\mathbb C[z]_{\leq3}  \tag{5}
\]

if and only if there are nonzero constants $c_i$ such that

\[
 \boxed{\displaystyle
 {F(z)\over B(z)^5}=\sum_{i=1}^7{c_i\over(z-a_i)^5}.}      \tag{6}
\]

Equivalently,

\[
       F\in\mathcal V_B:=
       \operatorname {span}\left\{
          \left({B(z)\over z-a_i}\right)^5:1\leq i\leq7
       \right\},                                         \tag{7}
\]

a seven-dimensional linear system in degree thirty.

This is a sharp algebraic frontier, not a dimension-drop theorem.  In
fact, exact structurally separated formal models exist for

\[
\boxed{
\begin{array}{c|c|c}
d&\text{tuple in (1)}&\text{audited common-pole orders}\\
\hline
0&(7,0,0,2)&k=1,2,3,4,5,6\\
1&(7,0,1,0)&k=1,2,3,4\\
2&(7,0,2,-2)&k=1,2.
\end{array}}                                               \tag{8}
\]

For every model in (8), the selected-row kernel has dimension exactly
six and its relation space is exactly (5).  Consequently the selected
highest-jet rows, their common-pole consequence, and the complete dual
relation construction cannot by themselves force a return to dimension
five on the all-quartic core.

These are formal selected-row models.  They do **not** reconstruct the
original tensor, do not realize a collision profile in the original
equations, and are not counterexamples to Krenn's conjecture.

There is also no hidden moving-double overlap among the three tuples.
Uniformly, tuple $d$ has original profile

\[
                       4^7 2^d1^{\,h+2-2d}.              \tag{8a}
\]

If only $x\leq d$ doubles were put in role two, the selection would need
$h+2-2x$ singleton classes.  The profile supplies only $h+2-2d$, so
legality forces $x\geq d$ and hence $x=d$.  Thus every double and every
singleton in (8a) is forced into its displayed role.  In the pure-pole
coordinate, replacing two singleton layers by one selected double merely
moves a square factor from $H$ into $Q^2$ while leaving the same degree-30
section $F\in\mathcal V_B$.  It creates an osculation condition on $F$,
not a second independent relation system.

## 2. The quartic highest jets give pure fifth-order poles

The exact relation operator for (3) is

\[
 \mathcal E_{B,k}(N)=
 B\bigl((z+\mu)N'+(k+1)N\bigr)-4(z+\mu)B'N.              \tag{9}
\]

For every $S\in\mathcal S$, the relation numerator satisfies

\[
                  \mathcal E_{B,k}(N)=Q^2HS,              \tag{10}
\]

or, equivalently,

\[
 {d\over dz}\left({(z+\mu)^{k+1}N\over B^4}\right)
                       ={F(z)S(z)\over B(z)^5}.           \tag{11}
\]

At a quartic node $a_i$, put

\[
 U_i(z)={F(z)\over\prod_{j\ne i}(z-a_j)^5}.              \tag{12}
\]

The residue of the right side of (11) must vanish for every cubic $S$.
Taking successively

\[
                    S=1,(z-a_i),(z-a_i)^2,(z-a_i)^3
\]

shows that

\[
               U_i^{(4)}(a_i)=U_i^{(3)}(a_i)
                 =U_i''(a_i)=U_i'(a_i)=0.                \tag{13}
\]

Thus the principal part of $F/B^5$ at $a_i$ contains only its
fifth-order term.  Since

\[
                 \deg F=30,\qquad\deg B^5=35,
\]

there is no polynomial part at infinity.  Partial fractions now give
(6), with

\[
                         c_i=U_i(a_i)\ne0.                \tag{14}
\]

This extracts the exact information in the highest quartic jets.  The
four-space being all of $P_3$ is only the starting point; (13)--(14) are
the non-tautological consequence.

## 3. The pure-pole identity is also sufficient

Suppose (6) holds.  For any cubic $S$, Taylor expansion at $a_i$ is
exact:

\[
 S(z)=\sum_{j=0}^3{S^{(j)}(a_i)\over j!}(z-a_i)^j.
\]

Hence $FS/B^5$ has the rational primitive

\[
 G_{0,S}(z)=
 \sum_{i=1}^7c_i\sum_{j=0}^3
 {S^{(j)}(a_i)\over j!(j-4)}(z-a_i)^{j-4}.               \tag{15}
\]

Normalize it by

\[
                         G_S=G_{0,S}-G_{0,S}(-\mu).       \tag{16}
\]

The derivative $G_S'=FS/B^5$ has a zero of order $k$ at
$-\mu$.  Therefore $G_S$ has a zero of order $k+1$ there, and

\[
                       N_S={B^4G_S\over(z+\mu)^{k+1}}     \tag{17}
\]

is a polynomial.  At infinity, $G_S$ is bounded, so

\[
               \deg N_S\leq28-(k+1)=27-k=h-1.           \tag{18}
\]

Differentiating (17) recovers (10).  The four choices
$S=1,z,z^2,z^3$ give four independent relation numerators.  Conversely,
the exact relation map is injective into the four-dimensional target
$P_3$.  The selected rows therefore have exactly four relations.

Here sufficiency uses the full numerator correspondence, not just the
differential equation.  Equation (10) says that the logarithmic quotient
associated with $N_S$ is constant through the complete selected principal
part at every root of $QH$.  Thus $N_S/(Q^3H^2)$ is a scalar multiple of
the prescribed principal part at each selected node.  The degree bound
(18) is exactly the moment cancellation condition, so it reconstructs a
row relation.

There are

\[
 L=h+2-d
\]

selected rows on $P_D$, where $D=h+3-d=L+1$.  Their rank is $L-4$,
so their common kernel has dimension

\[
                    (D+1)-(L-4)=6.                       \tag{19}
\]

This also explains the common-pole row exactly: it is encoded by the
factor $(z+\mu)^k$ in $F$, which makes the normalized primitive in
(16) divisible to order $k+1$.  It supplies no further contradiction
once (6) holds.

## 4. Exact models and the residual osculation problem

The audit fixes

\[
          B(z)=\prod_{a=1}^7(z-a),\qquad -\mu=10,          \tag{20}
\]

and, for $d=1,2$, uses the selected repeated plus-poles $8,9$.
The seven sections in (7) are independent: evaluation at the seven
$a_i$'s gives a nonsingular diagonal matrix.

Root order $k$ at $10$ and double roots at the first $d$ points
among $8,9$ impose $k+2d$ homogeneous jet equations on the seven
coefficients in (7).  For every pair in (8), those equations have full
row rank and a nonzero kernel.  The checker chooses an exact integer
kernel vector and writes

\[
 F=(z-10)^k\prod_{j=1}^d(z-q_j)^2H(z),
       \qquad(q_1,q_2)=(8,9).                             \tag{21}
\]

It verifies over $\mathbb Q$ that

* every coefficient $c_i$ is nonzero;
* the displayed roots in (21) have exactly their claimed orders;
* $H$ is squarefree and coprime to $H(-z)$;
* $H$ is nonzero at both signs of every complement node, selected
  repeated node, and the common pole; and
* the four explicit primitives (15)--(17) are polynomials of degree at
  most $h-1$ and satisfy (10) identically.

Thus the roots of $H$, after sign reversal, are valid distinct,
pairwise nonopposite selected singleton values with every required
separation.

For the remaining parameter pairs

\[
             d=1, k=5,6,\qquad d=2, k=3,4,5,6,          \tag{22}
\]

the imposed jet load is at least seven.  At the fixed rational nodes in
(20)--(21), the corresponding matrix already has full column rank, so no
model remains there.  When the nodes and $B$ vary, however, rank can
drop on a special confluent-osculation locus.  The exact unresolved local
question is therefore:

\[
 \boxed{\text{Can an admissible member of }\mathcal V_B
 \text{ carry the divisor }
 k[-\mu]+2\sum_{j=1}^d[-x_j]\text{ for a pair in (22)?}} \tag{23}
\]

No generic dimension count proves that this special locus is empty.
More importantly, the $d=0$ models cover all six $p=28$ splits, so
even a complete answer to (23) would not close the all-quartic profile by
selected-row duality alone.  A successful next step must couple (6) to
another formal selection, to the unreduced tensor equations, or to a
global compatibility condition absent from this one-selection model.

## 5. Exact audit

[verify_live_three_zero_higher_split_p28_all_quartic_pure_fifth_pole_frontier.py](../computations/verify_live_three_zero_higher_split_p28_all_quartic_pure_fifth_pole_frontier.py)
constructs all twelve models in (8), checks every separation and exact
root order, verifies the four rational primitives and differential
identities, and audits the selected-kernel dimension arithmetic.  It also
checks the full-column-rank statement at the fixed nodes for (22).

The
[independent audit](live-three-zero-higher-split-p28-all-quartic-pure-fifth-pole-frontier-independent-audit.md)
reconstructs the local principal-part criterion and moment cancellation
needed to turn each primitive into an actual row relation, independently
builds all twelve monic separated models, and preserves the distinction
between a formal selected-row model and a tensor realization.
