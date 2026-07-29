# The eighth split: all-order low mixed-role incidence closure

## 1. Uniform statement

In the all-order mixed-role pair-drop theorem, every formal selection with

\[
                              d\in\{1,2,3\}              \tag{1}
\]

is impossible.  Together with the
[ten-singleton case](live-three-zero-eighth-split-all-order-ten-singleton-incidence-closure.md),
this eliminates every selection with \(0\leq d\leq3\), independently of
the common-pole order and complementary collision profile.

For a fixed \(d\), there are \(s=10-2d\) selected singleton factors

\[
 f_r(z)=(z-r)(z+r)^2                                    \tag{2}
\]

of degree three and \(d\) selected repeated factors

\[
 f_x(z)=z^2-x^2                                         \tag{3}
\]

of degree two.  At most one repeated layer may come from an exact triple,
and the triple--zero edge may be the unique missing pair-drop edge.  This
does not affect the singleton incidences used below.

Assuming all isolated-star pivots vanish, the all-order theorem gives

\[
 K=W\subseteq\mathbb C[z]_{\leq D},\qquad
 \dim K=4,\qquad D=11-d.                               \tag{4}
\]

For every selected factor define \(U_i=K\cap f_i\mathbb C[z]\).  Every
\(U_i\) has dimension at least two.

## 2. Cubic nodes in an even pencil

We need the gcd-sensitive pencil count from the ten-singleton proof in a
form which includes a possible zero singleton.

**Lemma 2.1.**  Let a polynomial pencil
\(V\subseteq\mathbb C[z]_{\leq N}\) have identically zero parity
determinant.  If it contains, for each of \(m\) distinct pairwise
nonopposite singleton values \(r\), a nonzero member divisible by (2), then

\[
                              m\leq N-2.                 \tag{5}
\]

After dividing the pencil gcd \(G\), parity makes the primitive pencil
\({\cal E}(z^2)\), with square-variable degree at most
\(n=\lfloor(N-\deg G)/2\rfloor\).  For a nonzero \(r\), either
\(G(-r)=0\), costing a distinct gcd root, or the corresponding member of
\({\cal E}\) has a double root at \(r^2\), costing a Wronskian root.  At
\(r=0\), either \(G(0)=0\), or evenness upgrades divisibility by \(z^3\)
to a fourth-order zero and again gives a double root in \(z^2\).  Therefore

\[
 m\leq \deg G+2\left\lfloor{N-\deg G\over2}\right\rfloor-2
   \leq N-2.                                             \tag{6}
\]

Selected repeated factors help force the parity determinant to vanish:
a member divisible by (3) makes that determinant vanish at the nonzero
opposite pair \(\{x,-x\}\).  They do not need to be counted in (5).

There is one strengthening when the pencil inherits an exact selected
singleton row.  If \(G(-r)=0\), a simple gcd zero would make that first-order
row force every member of the primitive square-variable pencil to vanish at
\(r^2\), contradicting primitivity.  Thus each gcd-absorbed cubic node costs
at least two gcd degrees.  If \(a\) nodes are absorbed, \(g=\deg G\), and
the square-variable degree is at most \(n\), then

\[
                 2a\leq g,\qquad g+2n\leq N,
 \qquad m\leq a+2n-2.                                   \tag{7}
\]

This includes \(r=0\): a simple zero of \(G\) makes the exact row force a
common zero of the primitive pencil at the origin.

## 3. Singleton incidence spaces are not planes

Fix a selected singleton index \(i\) and suppose \(\dim U_i=2\).  Dividing
by its cubic gives a pencil of degree

\[
                              N=D-3=8-d.                 \tag{8}
\]

Every legal neighbor supplies a section divisible by its neighbor factor.
The following table records the worst zero/missing-edge case:

\[
\begin{array}{c|c|c|c|c}
d&N&\text{other singleton factors}&
 \text{nonzero opposite pairs}&\deg\Delta\leq2N-1\\ \hline
1&7&7&\geq7&13\\
2&6&5&\geq6&11\\
3&5&3&\geq5&9.
\end{array}                                               \tag{9}
\]

Thus the odd parity determinant vanishes identically in all three rows.  Lemma
2.1 would allow at most \(N-2=5\) singleton nodes for \(d=1\), and at most
four for \(d=2\).  The actual loads are seven and five.

At \(d=3\), the uncorrected bound is saturated: three cubic nodes in degree
five.  Apply (7).  The constraints \(2a\leq g\) and \(g+2n\leq5\) give

\[
                              a+2n-2\leq2,               \tag{10}
\]

strictly below the three cubic nodes.  Hence every singleton \(U_i\) has
dimension at least three for all three values of \(d\).

## 4. No selected factor is absorbed

Let \(a_3\) count selected singleton factors which divide all of \(K\), and
let \(a_2\) count such selected repeated factors.  Divide their pairwise
coprime product.  Every remaining singleton incidence space has dimension
three and forces Wronskian weight at least three at its double root.
Forced weight minus the four-space degree cap is

\[
\begin{array}{c|c}
d&3(s-a_3)-4\bigl((D-3a_3-2a_2)-3\bigr)\\ \hline
1&-4+9a_3+8a_2,\\
2&-6+9a_3+8a_2,\\
3&-8+9a_3+8a_2.
\end{array}                                               \tag{11}
\]

For \(d=1,2\), every nonzero absorption pattern makes the corresponding
expression positive; if the reduced degree is too small for a four-space,
the contradiction is earlier.  Thus no factor is absorbed in those cases.

For \(d=3\), every nonzero pattern is likewise contradictory except the
single equality case

\[
                              (a_3,a_2)=(0,1).            \tag{12}
\]

Consequently all selected singleton \(U_i\) are hyperplanes.  At \(d=3\),
either no factor is absorbed or exactly one selected quadratic factor is
absorbed by all of \(K\).

## 5. The pair-intersection pencil

Any four singleton hyperplanes have zero intersection, because a common
member would be divisible by four coprime cubics of total degree twelve,
while \(D\leq10\).  Hence every four quotient covectors are independent,
so pair intersections have dimension two and triple intersections have
dimension one.

Fix two singleton indices.  Divide their pair intersection by the two
cubic factors.  This gives a pencil of degree at most

\[
                              N'=D-6=5-d.                \tag{13}
\]

Each other singleton hyperplane meets the pair in a nonzero line, providing
a pencil member divisible by its cubic.  The terminal counts are

\[
\begin{array}{c|c|c|c|c}
d&N'&\text{cubic load}&\text{nonzero opposite pairs}
 &\deg\Delta\leq2N'-1\\ \hline
1&4&6&\geq5&7\\
2&3&4&\geq3&5.
\end{array}                                               \tag{14}
\]

The parity determinants again vanish.  Lemma 2.1 allows at most two cubic
nodes in the first row and one in the second, contradicting the loads six
and four.  This proves (1) for \(d=1,2\).

For \(d=3\), there are four singleton hyperplanes.  In the no-absorption
case they lie in \(K\subseteq\mathbb C[z]_{\leq8}\); in the equality case
(12), divide the common quadratic and obtain a four-space in
\(\mathbb C[z]_{\leq6}\).  In either case, any three hyperplanes have a
nonzero common member by dimension.  That member would be divisible by
three pairwise coprime cubics of total degree nine, exceeding both ambient
degree caps.  This contradiction finishes \(d=3\).

The argument stops at \(d=4\): there are only two selected singleton
hyperplanes, and the first quotient pencil's single remaining cubic node
does not exceed its exact capacity.  No \(d=4\) closure is asserted here.

## 6. Exact audit

[verify_live_three_zero_eighth_split_all_order_low_mixed_role_incidence_closure.py](../computations/verify_live_three_zero_eighth_split_all_order_low_mixed_role_incidence_closure.py)
checks all three zero/missing-edge parity counts, the zero-sensitive gcd and
Wronskian caps (6)--(7), the absorption deficits (11), both hyperplane
incidence chains, the terminal pencil counts, and the remaining \(d=4\)
boundary.
