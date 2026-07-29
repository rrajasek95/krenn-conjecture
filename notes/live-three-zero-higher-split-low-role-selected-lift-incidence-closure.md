# Higher splits: low-role selected-lift incidence closure

## 1. Statement

Work on the no-extra-singular live-three-zero collision stratum.  Put

\[
 p=h+k,\qquad M=2h+k+2,\qquad h\geq8,\quad k\geq1.
                                                               \tag{1}
\]

Suppose a formal pair-drop selection gives role two to
\(d\in\{0,1,2\}\) repeated classes and role one to

\[
                         s=h+2-2d                              \tag{2}
\]

singleton classes.  As usual, the repeated classes are exact doubles,
except that at most one may be an exact triple, and the triple--zero edge
may be the unique illegal pair-drop edge.  If

\[
                 13-h+\max(0,5-k)>0,                           \tag{3}
\]

then the isolated-star pivots cannot all vanish.

For the genuinely higher splits, condition (3) is exactly

\[
\begin{array}{c|c}
h&k\\ \hline
9\leq h\leq12&\text{arbitrary }k\geq1,\\
13&1\leq k\leq4,\\
14&1\leq k\leq3,\\
15&1\leq k\leq2,\\
16&k=1.
\end{array}                                                   \tag{4}
\]

The theorem also contains the already studied \(h=8,d\leq2\) range.
It is uniform in the complementary collision profile and uses no bound
on its number of value classes.

## 2. Pair drops give at least a four-space

There are

\[
 L=d+s=h+2-d,\qquad D=h+3-d                              \tag{5}
\]

selected layers, and every legal pair-drop lift lies in
\(\mathbb C[z]_{\leq D}\).  The factors belonging to a repeated layer
and a singleton layer are respectively

\[
 f_x(z)=z^2-x^2,\qquad f_r(z)=(z-r)(z+r)^2.                \tag{6}
\]

Let \(W\) be the span of the nonzero legal pair-drop lifts and let \(K\)
be the common kernel of the selected rows.  Thus \(W\subseteq K\).
The arbitrary-\(h\) pair-drop theorem applies because, for \(d\leq2\),

\[
 2s=2(h+2-2d)>
 3\left(\left\lfloor{h+3-d\over2}\right\rfloor-2\right).
                                                               \tag{7}
\]

It includes the possible missing triple--zero edge and gives

\[
                              \dim W\geq4.                 \tag{8}
\]

The exact lift and inequality are proved in
[the higher-split mixed pair-drop theorem](live-three-zero-higher-split-mixed-pair-drop-five-class-closure.md),
Sections 2--3.  Only its four-space conclusion is used here; the
five-complementary-class hypothesis of that note is not used.

## 3. The common-pole functional and the sharp kernel bound

The \(d\) repeated rows have exact local order two, while the \(s\)
singleton rows have exact local order one:

\[
 P\longmapsto(B_xP)''(-x),\qquad
 P\longmapsto(B_rP)'(-r),                                \tag{9}
\]

where the displayed local units do not vanish.  Let \(q=\dim K\).  With
no common polynomial factor, their forced Wronskian weight minus the
degree-\(D\) cap is

\[
\begin{split}
 d(q-2)+s(q-1)-q(D+1-q)
       &=q^2-2q-h-2.                                     \tag{10}
\end{split}
\]

There is one more local condition which is useful here.  For every
\(P\in K\), the corresponding rational function is

\[
 {A(z)P(z)\over
   (z+\mu)^{k+1}Q(z)^3H(z)^2},                           \tag{11}
\]

where \(Q\) and \(H\) are the products of the selected repeated and
singleton plus-pole factors.  The numerator and denominator degrees are

\[
 (h+k)+(h+3-d),\qquad
 (k+1)+3d+2s=2h+k+5-d,                                  \tag{12}
\]

so (11) is \(O(z^{-2})\).  Its selected-pole residues vanish by (9), and
there are no other finite poles except \(-\mu\).  The residue theorem
therefore gives the exact order-\(k\) functional

\[
 \left.\left({d\over dz}\right)^k
   \left({A(z)P(z)\over Q(z)^3H(z)^2}\right)
 \right|_{z=-\mu}=0.                                    \tag{13}
\]

We record all gcd corrections, because they are what makes (3) exact.
Let \(G=\gcd K\).  At a singleton row, a simple zero of \(G\) would turn
(9) into a common value zero after division, contradicting maximality of
the gcd.  Thus a gcd zero there has order at least two.  Removing such a
row and its gcd factor improves (10) by at least \(q+1\).

At a repeated row, a gcd order one changes the exact order-two functional
to order one and improves (10) by \(q+1\).  Gcd order two is impossible:
after division, (9) would force a common value zero.  An order at least
three makes the row automatic but improves (10) by
\((t-1)q+2>0\).  Gcd roots away from all displayed nodes only lower the
degree cap and are likewise favorable.

Finally put \(t=\operatorname{ord}_{-\mu}G\).  If \(t\leq k\), (13)
becomes an exact order \(k-t\) functional on the reduced, base-point-free
space.  Its Wronskian weight is at least

\[
                         \max(0,q-k+t).                  \tag{14}
\]

If \(t>k\), the functional is automatic, but removing the gcd lowers the
Wronskian cap by \(qt\).  In either case, the contribution of the common
pole and its gcd is at least \(\max(0,q-k)\), with equality possible only
at \(t=0\).  Hence every \(q\)-space \(K\) would require

\[
             q^2-2q-h-2+\max(0,q-k)\leq0.               \tag{15}
\]

The left side is strictly increasing for \(q\geq5\).  At \(q=5\) it is

\[
                         13-h+\max(0,5-k).               \tag{16}
\]

Under (3), equations (8) and (15) therefore give

\[
                         K=W,\qquad \dim K=4.             \tag{17}
\]

## 4. Singleton incidence spaces are hyperplanes or absorbed

For each selected singleton \(r_i\), put

\[
                         U_i=K\cap f_{r_i}\mathbb C[z].  \tag{18}
\]

Within \(K\), divisibility by \(f_{r_i}\) imposes at most two additional
conditions: the exact first-order row in (9) supplies one of the three
local jet conditions.  This remains true at \(r_i=0\), where
\(f_{r_i}=z^3\).  Hence \(\dim U_i\geq2\).

Suppose \(U_i\) were a plane.  Dividing by \(f_{r_i}\) gives a pencil in

\[
                    \mathbb C[z]_{\leq N},\qquad N=D-3=h-d. \tag{19}
\]

Every other singleton supplies a member divisible by its cubic factor.
Every legal repeated neighbor supplies a member divisible by its even
quadratic factor.  The parity determinant of a basis is odd of degree at
most \(2N-1\).

There are at least \(N\) distinct nonzero opposite root pairs.  Indeed,
if a zero singleton is a neighbor, the count is

\[
                       (s-2)+d=N;                        \tag{20}
\]

if the fixed singleton is zero, the unique triple--zero edge may be
missing and the count is

\[
                       (s-1)+(d-1)=N.                    \tag{21}
\]

For \(d=0\), no edge is missing and a fixed zero gives \(s-1=N+1\)
pairs.  With no zero or missing edge the count is also larger.  Thus the
parity determinant vanishes identically.

After its gcd is removed, the primitive pencil is a pencil in \(z^2\).
If it contains a section divisible by \(f_r\) at \(m\) distinct singleton
nodes, including a possible zero node, the standard gcd plus Wronskian
count gives

\[
                         m\leq N-2.                      \tag{22}
\]

Here \(m=s-1=h+1-2d\), whereas

\[
                         m-(N-2)=3-d>0.                  \tag{23}
\]

This contradiction proves that every \(U_i\) is either a hyperplane in
\(K\) or all of \(K\).

## 5. Absorption does not create an escape

Let \(a_3\) selected singleton factors and \(a_2\) selected repeated
factors divide every member of \(K\).  Divide their pairwise coprime
product, of degree

\[
                         g=3a_3+2a_2.                    \tag{24}
\]

The remaining singleton incidence spaces are hyperplanes in the resulting
four-space of polynomials of degree at most \(D-g\).  Since this ambient
space contains a four-space, \(D-g\geq3\), and hence

\[
 s-a_3\geq h+2-2d-{h-d-2a_2\over3}\geq4.                \tag{25}
\]

Thus at least four singleton hyperplanes remain.  If they are all the
same, a nonzero member
can be chosen which, before division, is divisible by every selected
singleton factor and every absorbed repeated factor.  This is impossible,
because

\[
           3s+2a_2-D=2h+3-5d+2a_2>0.                   \tag{26}
\]

Consequently two remaining singleton hyperplanes, say \(U_i,U_j\), are
distinct.  Their intersection is a plane.  Divide it by
\(f_{r_i}f_{r_j}\).  If \(D-g<7\), the existence of this
two-dimensional divisible space is already impossible.  Otherwise the
resulting pencil has degree at most

\[
                  N'=D-g-6=h-d-3-g.                    \tag{27}
\]

Every other remaining singleton hyperplane meets this pair in a nonzero
line, producing a pencil member divisible by the corresponding cubic.
There are \(m=s-a_3-2\) such nodes and at least
\(m-1=s-a_3-3\) nonzero ones.  If \(N'<3\), even one such nonzero
cubic-divisible member is impossible.  Otherwise their opposite roots force the parity
determinant to vanish, since

\[
 2(s-a_3-3)-(2N'-1)=5-2d+4a_3+4a_2>0.                 \tag{28}
\]

The square-pencil cap (22) then gives \(m\leq N'-2\), but in fact

\[
                    m-(N'-2)=5-d+2a_3+2a_2>0.           \tag{29}
\]

This final contradiction proves the theorem.  Notice that the terminal
argument uses only singleton hyperplanes, so the possible missing
triple--zero edge has disappeared completely.

## 6. Why the argument stops at a five-space

The threshold in (16) is structural for selected-lift incidence.  In a
five-dimensional row kernel, each \(U_i\) has codimension at most two.
For any two singleton nodes, the four evaluations at their two signs have
a nonzero common kernel automatically.  The exact Robin rows then upgrade
the two negative-sign zeros to double zeros.  Thus all pair lifts can
exist without imposing any further condition on a five-space.

There is also a global polynomial-linear-series boundary model.  Put
\(L=h+2\), \(D=h+3\), and \(h\geq13\).  In
\(\operatorname{Gr}(5,D+1)\), requiring a five-space to have vanishing
sequence

\[
                         (0,2,3,4,5)                     \tag{30}
\]

at one prescribed node is the codimension-four osculating Schubert
condition \(\sigma_{1^4}\).  The repeated product
\(\sigma_{1^4}^{L}\) is nonzero.  One explicit Pieri endpoint is

\[
                         (L-3,L-3,L-3,L-3,12),           \tag{31}
\]

which fits the \(5\times(L-3)\) Grassmannian rectangle.  It is reached by
omitting row five in \(L-12\) successive vertical four-strips, then
omitting rows four, three, two, and one three times each.  The classical
osculating-Schubert degeneration therefore supplies such five-spaces at
general distinct nodes.

At each node (29) is exactly a base-point-free Robin row.  Choosing the
nodes pairwise nonopposite, the four signed evaluations belonging to any
two nodes have a nonzero common kernel in the five-space, and hence give
a polynomial divisible by the two cubic factors.  This is a countermodel
to any attempt to extend Sections 4--5 using only row-kernel dimension and
pair-lift incidence.

This Schubert boundary is **not** asserted to be a collision-profile
realization: it does not reconstruct one complementary polynomial \(A\)
or the original tensor equations.  It only identifies precisely what a
new multi-drop or global compatibility input would have to defeat.

## 7. Exact audit

[verify_live_three_zero_higher_split_low_role_selected_lift_incidence_closure.py](../computations/verify_live_three_zero_higher_split_low_role_selected_lift_incidence_closure.py)
checks (3)--(8), every gcd correction in Section 3, both zero/missing-edge
counts, the two parity and square-pencil inequalities after arbitrary
absorption, and the Pieri boundary path.
