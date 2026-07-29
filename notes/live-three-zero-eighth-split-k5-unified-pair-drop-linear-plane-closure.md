# The eighth split at \(k=5\): unified pair-drop kernel and seven linear-plane closures

## 1. Result and scope

Put \(h=8\), \(k=5\), and \(M=23\).  The following seven profiles on
the current no-extra-singular residual ledger are impossible:

\[
\begin{gathered}
 3^5 2^2 1^4,\qquad 3^5 2\,1^6,\qquad 3^5 1^8,\\
 3^4 2^3 1^5,\qquad 3^4 2^2 1^7,\qquad 3^4 1^{11},\\
 3^3 2^6 1^2.
\end{gathered}                                             \tag{1}
\]

The common input is a kernel lemma with \(d\) formal role-two layers and
\(s=10-2d\) formal singleton layers, where \(0\le d\le4\).  It remains
valid when exactly one role-two layer comes from an exact triple and one
pair-drop core is illegal because it lowers that triple together with a
zero singleton.  This missing-edge case is needed for the first three
profiles in (1).

The kernel lemma by itself is not a closure theorem.  It applies to all
but one of the 34 profiles in the ledger preceding (1), but usually its
dual polynomial target has degree at least two.  Exactly nine open
profiles have a linear target.  Six in (1) have complementary signature
\(3^4 1\), and the complementary singleton gives an immediate residue
contradiction.  Three have signature \(3^3 2^2\); the double-swap argument
closes \(3^3 2^6 1^2\), but it does not close
\(3^3 2^3 1^8\) or \(3^3 2^2 1^{10}\).  Those two remain open.

The same theorem recovers the already credited closures
\(3^4 2\,1^9\) and \(3^3 2^4 1^6\).  They receive no new census credit.

Repeated exceptional values are nonzero, distinct exceptional classes
are pairwise nonopposite, and at most one singleton value is zero.  These
are the standing structural facts on the no-extra-singular stratum.

## 2. Formal layers and the possibly missing pair

Choose \(d\) distinct repeated classes and give each formal role two.
Every chosen repeated class is an exact double except that at most one may
be an exact triple.  Choose \(s=10-2d\) distinct singleton classes and
give each formal role one.  Thus

\[
             2d+s=10,\qquad L:=d+s=10-d,
             \qquad D:=11-d.                             \tag{2}
\]

Lower two distinct formal layers.  The resulting core has role eight.
For a lowered repeated value \(x\) and an omitted singleton value \(r\),
use the lift factors

\[
                 f_x(z)=z^2-x^2,
        \qquad f_r(z)=(z-r)(z+r)^2.                      \tag{3}
\]

If \(b\in\{0,1,2\}\) lowered layers are singletons, the product of the
two lift factors has degree \(4+b\).  The core represents \(L-b\) value
classes, so its nonzero Hermite residual has degree at most

\[
                         L-b-3=7-d-b.                   \tag{4}
\]

Every legal pair-drop lift therefore has degree at most
\((4+b)+(7-d-b)=D\).

The existence, nonvanishing, and kernel membership of these lifts are the
formal pair-drop instance of the cubic-gauge/Hermite lift proved in
[the higher-split collision-exchange theorem](live-three-zero-higher-split-collision-exchange-wronskian.md),
Sections 3--4.  The two factor types (3), including the zero-singleton
case, and their simultaneous selected-row kernel are written out in
[the mixed pair-drop model](live-three-zero-eighth-split-k4-four-triple-mixed-layer-closure.md),
Sections 2--3.  Thus a legal core supplies a nonzero \(P_{ij}\), cubic
gauge multiplication supplies exactly the two factors in (3), and the
lifted response equations put \(P_{ij}\) in every selected residue-row
kernel.  We use no rank conclusion from those earlier special cases.

If all chosen repeated classes are doubles, every pair is legal.  With
one chosen triple, every pair is still legal except possibly the pair
formed by that triple and the zero singleton.  Indeed, lowering a double
leaves its nonzero mate as a singleton guard; lowering two singleton
layers leaves at least one nonzero singleton; and a chosen triple which
is not lowered leaves its nonzero third label as a singleton guard.  Only
the triple--zero pair can leave no such guard.  Thus the legal-pair graph
is either \(K_L\) or \(K_L\) with that one edge deleted.

Let \(P_{ij}\ne0\) denote the lift for a legal pair \(ij\), and put

\[
 W=\operatorname {span}\{P_{ij}:ij\text{ legal}\}
       \subseteq\mathbb C[z]_{\le D}.                    \tag{5}
\]

## 3. The selected-row kernel has dimension at most four

Let \(K\subseteq\mathbb C[z]_{\le D}\) be the common kernel of the
\(d\) exact order-two rows at the selected repeated values and the
\(s\) exact order-one rows at the selected singleton values.  Every lift
in (5) lies in \(K\).

More explicitly, after all other structural factors are absorbed into a
unit, the selected row at a repeated value \(x\) and at a singleton value
\(r\) has respectively the local form

\[
             P\longmapsto (B_xP)''(-x),\qquad
             P\longmapsto (B_rP)'(-r),                  \tag{5a}
\]

with \(B_x(-x)B_r(-r)\ne0\).  These are the exact local rows used both
in the Wronskian weights and in every gcd correction below.

Write \(q=\dim K\).  With unit gcd at the selected nodes, the forced
Wronskian weight is

\[
                    d(q-2)+s(q-1),                      \tag{6}
\]

whereas a \(q\)-space in \(\mathbb C[z]_{\le D}\) has Wronskian degree
at most \(q(D+1-q)\).  Using (2), the forced weight minus the degree cap
is

\[
 d(q-2)+(10-2d)(q-1)-q(12-d-q)
                         =q^2-2q-10.                    \tag{7}
\]

This is positive for \(q\ge5\).  The standard local gcd corrections do
not weaken the inequality.  At an order-two node, a simple gcd zero adds
\(q+1\) to the deficit; absorption has order at least three and adds at
least \(2q+2\).  At an order-one node, a simple gcd zero forces one more
common zero and absorption has order at least two, adding at least
\(q+1\).  A gcd root away from the selected nodes only lowers the degree
cap.  Consequently

\[
                              \dim K\le4.                \tag{8}
\]

## 4. The missing edge does not lower the lift span

For every formal layer \(i\), set

\[
                         U_i=W\cap f_i\mathbb C[z].      \tag{9}
\]

The total degree of all layer factors is

\[
                  2d+3s=30-4d.                         \tag{10}
\]

Suppose \(U_i\) were a line.  Every lift \(P_{ij}\) through a legal
neighbor \(j\) would then be proportional to its generator, so the
product of all neighbor factors would divide one polynomial of degree at
most \(D\).  Even at an endpoint of the possibly deleted edge, the
neighbor factors have degree

\[
                   (30-4d)-2-3=25-4d>D=11-d            \tag{11}
\]

for \(0\le d\le4\).  Every other vertex has a larger neighbor product.
Hence \(\dim U_i\ge2\) for every \(i\).  This excludes \(\dim W\le2\):
in a two-space every \(U_i\) would equal \(W\), making every member of
\(W\) divisible by the product (10), whose degree exceeds \(D\).

Assume \(\dim W=3\).  At every nonzero layer value \(v\), the two
evaluation vectors of a basis \({\bf P}\) at \(v\) and \(-v\) are
proportional because \(U_v\) is a plane.  Hence the three parity minors

\[
 P_i(z)P_j(-z)-P_i(-z)P_j(z)                            \tag{12}
\]

vanish at both signs of every nonzero layer value.  They are odd and
have degree at most \(2D-1=21-2d\).  If no singleton is zero, their
forced divisor has degree

\[
                         1+2L=21-2d.                    \tag{13}
\]

If a singleton is zero, an adapted basis of its plane \(U_0\) gives a
triple zero at the origin, and the other \(L-1\) opposite pairs give

\[
                         3+2(L-1)=21-2d.                \tag{14}
\]

Thus \({\bf P}(z)\times{\bf P}(-z)=\Delta(z){\bf c}\) for one constant
vector \({\bf c}\).  Dotting with \({\bf P}(z)\) shows that
\({\bf c}\ne0\) would be a constant relation among a basis, so all
parity minors vanish.  After removing the gcd \(G\) of \(W\), the
primitive space is projectively even:

\[
                         W=G(z){\cal E}(z^2),
                         \qquad\dim{\cal E}=3.          \tag{15}
\]

There is one useful correction at an absorbed singleton.  The exact
selected singleton row has the local form

\[
                         (B_rP)'(-r)=0,                 \tag{16}
\]

where \(B_r(-r)\ne0\).  If \(G\) had only a simple zero at \(-r\), then
substituting \(P=G E(z^2)\) into (16) would force
\(E(r^2)=0\) for every \(E\in{\cal E}\), contrary to primitivity after
that common square factor is absorbed into \(G\).  This also holds at
\(r=0\).  Therefore every absorbed singleton costs at least two degrees
of \(G\), not one.

Let \(m\) be the number of selected singleton nodes \(r\) for which
\(G(-r)=0\).  The preceding exact row makes the zero at least double, so
\(\deg G\ge2m\), and the maximum square-variable degree in \({\cal E}\)
is at most

\[
                   n\le\left\lfloor{11-d-2m\over2}\right\rfloor.       \tag{17}
\]

At each of the other \(s-m\) singleton squares, the plane \(U_r\)
provides two independent members divisible by \((z+r)^2\).  In the
square variable their vanishing sequence is at least \((0,2,3)\), so
each contributes Wronskian weight at least two.  The squared values are
distinct.  A primitive three-space of maximum degree \(n\) would
therefore require

\[
 2(s-m)\le3(n-2)
 \le3\left(\left\lfloor{11-d-2m\over2}\right\rfloor-2\right).          \tag{18}
\]

For every \(0\le d\le4\) and \(0\le m\le s=10-2d\), either the right
side has degree too small to contain a three-space or the inequality is
strictly reversed.  Hence \(\dim W\ne3\).  Together with (8),

\[
                         \boxed{W=K,\qquad\dim K=4}.     \tag{19}
\]

This proves the unified kernel lemma, including its one-missing-edge
case.

## 5. Duality and the linear target

Let \(Q\) be the product of the selected role-two plus-pole factors and
\(H\) the product of the selected singleton plus-pole factors.  Let
\(A\) be the complementary polynomial after the full formal role-ten
selection.  Always \(\deg A=13\).  The lifted rational functions are

\[
              F_P(z)={A(z)P(z)\over
                    (z+\mu)^6Q(z)^3H(z)^2}.             \tag{20}
\]

There are \(L=10-d\) selected rows on the \((D+1)=(12-d)\)-dimensional
polynomial space.  Equation (19) makes their rank \(8-d\), so their
relation space has dimension two.  A relation among their distinct
principal parts has numerator

\[
                  {N(z)\over Q(z)^3H(z)^2},
                  \qquad \deg N\le7.                   \tag{21}
\]

The bound follows from the \(D+1=12-d\) annihilated moments and
\(\deg(Q^3H^2)=20-d\).  Distinct principal-part supports make the map
from relations to \(N\) injective.

Put

\[
 g=\prod_{A(a)=0}(z-a)^{\operatorname{ord}_a(A)-1},
 \qquad R={A\over g},\qquad D_A={A'\over g},             \tag{22}
\]

and let \(c=\deg R\), the number of complementary value classes.  Exact
differentiation gives

\[
 {d\over dz}{(z+\mu)^6N\over A}
 ={(z+\mu)^5g\over A^2}{\cal E}_A(N),                  \tag{23}
\]

where

\[
 \mathcal E_A(N)=R\bigl((z+\mu)N'+6N\bigr)
                    -(z+\mu)D_AN.                      \tag{24}
\]

Since \(\operatorname{LC}(D_A)=13\), the nominal leading coefficient
for \(\deg N=n\le7\) is \(n+6-13=n-7\).  The top term cancels at
\(n=7\), and therefore \(\deg{\cal E}_A(N)\le c+6\).
Selected-pole contact gives

\[
                   {\cal E}_A(N)=Q^2H S_N,
                   \qquad S_N\in\mathbb C[z]_{\le c-4},               \tag{25}
\]

because \(\deg(Q^2H)=2d+s=10\).  This map is injective: if
\({\cal E}_A(N)=0\), then (23) is the derivative of a constant, and
evaluation at \(-\mu\), where \(A(-\mu)\ne0\), forces that constant and
\(N\) to vanish.

When \(c=5\), the two-dimensional relation space maps injectively onto
the two-dimensional space of linear polynomials.  Thus

\[
                         {\cal S}=\mathbb C[z]_{\le1}.  \tag{26}
\]

Every member in (26) occurs in the exact derivative (23), so all its
complementary residues vanish.

## 6. Complementary signature \(3^4 1\)

Suppose

\[
                         A(z)=(z-r)\prod_{a\in{\cal A}}(z-a)^3,
                         \qquad |{\cal A}|=4.           \tag{27}
\]

The simple root \(r\) may be an unselected original singleton or the
remaining label of the one selected triple.  In either case all other
factors in (23) are units at \(r\).  For every linear \(S\), the local
form of that exact derivative is

\[
                         {B_r(z)S(z)\over(z-r)^2},
                         \qquad B_r(r)\ne0.             \tag{28}
\]

Its residue vanishes, so \((B_rS)'(r)=0\) for every
\(S\in\mathbb C[z]_{\le1}\).  Taking \(S=z-r\) gives
\(B_r(r)=0\), a contradiction.

The six previously open profiles admitting (27) are exactly

\[
 3^5 2^2 1^4,\quad3^5 2\,1^6,\quad3^5 1^8,\quad
 3^4 2^3 1^5,\quad3^4 2^2 1^7,\quad3^4 1^{11}.          \tag{29}
\]

For the first three, select one triple and all available doubles, with
\((d,s)=(3,4),(2,6),(1,8)\); these are precisely the cases in which the
triple--zero edge may be missing.  For the last three, select all
doubles and respectively four, six, or ten singleton layers.  The same
argument also recovers the already credited profile \(3^4 2\,1^9\).

## 7. Complementary signature \(3^3 2^2\)

Now write

\[
 A(z)=(z-u)^2(z-v)^2\prod_{a\in{\cal A}}(z-a)^3,
                         \qquad |{\cal A}|=3.           \tag{30}
\]

All selected repeated layers are doubles.  Removing the cubic pole at a
complementary double \(u\) from (23), the remaining unit is

\[
 B_{T,u}(z)=
 { (z+\mu)^5Q_T(z)^2H(z)\over
   (z-v)^3\displaystyle\prod_{a\in{\cal A}}(z-a)^4}.   \tag{31}
\]

The zero residue condition is

\[
                         (B_{T,u}S)''(u)=0
                         \qquad(S\in\mathbb C[z]_{\le1}).              \tag{32}
\]

Taking \(S=z-u\) gives \(B_{T,u}'(u)=0\), hence

\[
 0={5\over u+\mu}+2\sum_{t\in T}{1\over u+t}
       +\sum_{r\in R}{1\over u+r}
       -{3\over u-v}-4\sum_{a\in{\cal A}}{1\over u-a}.               \tag{33}
\]

Fix \(u\), exchange a selected double \(x\) with the other
complementary double \(v\), and subtract the two instances of (33).  All
fixed terms cancel and give

\[
 {2\over u+x}+{3\over u-x}
 ={2\over u+v}+{3\over u-v}.                            \tag{34}
\]

Thus all double values other than \(u\) lie in one fibre of

\[
                  \Phi_u(t)={5u+t\over u^2-t^2}.        \tag{35}
\]

Every fibre is cut out by the nonzero polynomial
\(\lambda(u^2-t^2)-5u-t\), of degree at most two.  Therefore the swap
is contradictory whenever there are at least four double values in the
original profile.

Among the three previously open linear-target profiles with signature
\(3^3 2^2\), this closes exactly

\[
                              3^3 2^6 1^2.              \tag{36}
\]

The profiles \(3^3 2^3 1^8\) and \(3^3 2^2 1^{10}\) have only two or
zero selected/outside swaps for a fixed \(u\); (34) supplies at most the
allowed two points of a quadratic fibre.  They are not claimed closed.
The same calculation recovers the already credited
\(3^3 2^4 1^6\).

## 8. Exact census effect and audit

Before (1), the updated fifth-order ledger has 44 frozen profiles, ten
accepted closures, and 34 open profiles.  The unified kernel is
applicable to 33 of those 34 open profiles; the sole exception is
\(3^2 2^8 1\), which has too few singleton layers for every
\(0\le d\le4\).  Exactly the nine profiles listed in Sections 6 and 7
have a five-class complement and hence the full linear target (26).
Equations (28) and (34) close exactly the seven profiles in (1).  The
sequential ledger therefore becomes

\[
             44=17+27,\qquad
             2^9 1^5\text{ remains open}.              \tag{37}
\]

[verify_live_three_zero_eighth_split_k5_unified_pair_drop_linear_plane_closure.py](../computations/verify_live_three_zero_eighth_split_k5_unified_pair_drop_linear_plane_closure.py)
checks the degree formulas for every \(d\), the missing-edge neighbor
bound, all gcd/three-space inequalities, the relation count and leading
cancellation, the two complementary residue calculations, and an exact
enumeration of the 44-profile ledger.  The enumeration distinguishes
kernel applicability, linear-target applicability, actual closure, and
the two explicitly unclosed linear-target profiles.
