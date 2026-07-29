# Nonarchimedean normalization and its exact obstruction

## 1. The valuation linear program

Suppose the aggregate matrices have algebraic entries in a number field and
fix a prime above `2`.  Write

\[
 w_{uv}^{ab}=\nu(A_{uv}^{ab})
\]

for each nonzero entry; zero entries have valuation infinity and impose no
constraint.  A local diagonal gauge has valuations `t_{v,a}` and sends

\[
 w_{uv}^{ab}\longmapsto w_{uv}^{ab}+t_{u,a}+t_{v,b}.
\]

It preserves the diagonal target exactly when its scalars can be chosen with

\[
 \sum_v t_{v,a}=0\qquad(a=0,\ldots,q-1).                    \tag{1}
\]

Thus all aggregate entries can be made integral if and only if the following
rational linear program is feasible:

\[
 \begin{aligned}
 t_{u,a}+t_{v,b}&\ge -w_{uv}^{ab}
       &&\text{for every nonzero }A_{uv}^{ab},\\
 \sum_vt_{v,a}&=0&&\text{for every color }a.
 \end{aligned}                                               \tag{2}
\]

Allowing a finite ramified extension realizes any rational solution in the
value group.  After choosing scalars of the prescribed valuations, multiply
one scalar in each color by a unit so that its product over the vertices is
exactly one; this does not change (2).

There is an equally useful exact dual criterion.  Put a nonnegative rational
multiplicity `y_uv^{ab}` on the nonzero aggregate entries.  Call `y`
color-balanced if, for each fixed color `a`, its incidence degree at the mode
`(v,a)` is independent of `v`.  Farkas' lemma gives

\[
 \boxed{\text{(2) is feasible}\iff
 \sum_{uv,a,b}y_{uv}^{ab}w_{uv}^{ab}\ge0
 \text{ for every color-balanced }y\ge0.}                   \tag{3}
\]

Indeed, summing the proposed integral inequalities against a balanced `y`
cancels the gauge terms by (1), proving necessity.  Conversely a Farkas
certificate for infeasibility has nonnegative coefficients `y`; vanishing of
the coefficient of each `t_{v,a}` modulo the equality rows says precisely
that the incidence degrees are constant in `v`, and its strict inequality is
the negation of (3).  Clearing denominators makes the obstruction an integral
multiset of endpoint-colored aggregate entries.

If (2) were automatic for a hypothetical algebraic solution
`H_n(A)=Delta_(n,q)`, reduction modulo the prime would retain that identity in
characteristic two.  The matching sum is then the Pfaffian of the alternating
matrix on the vertex/color modes, restricted to one mode at every vertex.
The issue is that integrality is not automatic from a hafnian identity alone.

## 2. An actual exact counterexample to automatic normalization

Already for one color and six vertices, take the eight nonzero scalar edges

\[
\begin{array}{c|cccccccc}
uv&01&23&45&02&13&05&12&34\\ \hline
A_{uv}&1/2&1&1&-1/2&1&1&1&1.
\end{array}                                                   \tag{4}
\]

The support graph has exactly the three perfect matchings

\[
 01|23|45,\qquad02|13|45,\qquad05|12|34.                     \tag{5}
\]

Their products are `1/2,-1/2,1`, so the scalar hafnian is exactly one.  At
the 2-adic valuation the first two matching products have valuation `-1` and
the third has valuation zero.  Add the three incidence vectors in (5).  Every
vertex has degree three, so this is a balanced dual vector `y`, while

\[
 \sum_e y_e\nu(A_e)=-2.                                     \tag{6}
\]

By (3), no determinant-one local diagonal gauge can make all eight entries
2-integral.  Equivalently, if `sum_v t_v=0`, summing the nine edge
inequalities over the three matchings gives `-2>=0`, a contradiction.  This
is an actual rational solution, not merely tropical data, and every supported
edge belongs to a perfect matching.  Therefore the implication

\[
 H_n(A)=\Delta\quad\Longrightarrow\quad\text{(2) feasible}
\]

is false without using the full multicolor equations in an essential way.

## 3. The coefficientwise q=3 tropical conditions still do not suffice

There is also a sharp warning in the precise `n=6,q=3` format.  Give every
cell on underlying edges `01` and `02` valuation `-1`, and every cell on all
other underlying edges valuation zero.  For every one of the `3^6=729`
colorings, exactly six matching monomials have minimum valuation `-1`: the
three matching vertex `0` to `1` and the three matching it to `2`.  If all
initial residues are one, their initial-form sum is `6=0` in characteristic
two.  Thus every defining coefficient equation has the required repeated
minimum, and all 729 generator initial forms vanish at the all-ones residue
point.

Nevertheless (2) is infeasible.  In color zero, sum the three perfect
matchings

\[
 01|23|45,qquad02|14|35,qquad03|15|24.                     \tag{7}
\]

Their incidence multiset has degree three at every `(v,0)` mode and degree
zero at the other color modes, so it is color-balanced, while its total
valuation is again `-2`.  This is not claimed to lift to an exact
characteristic-zero `q=3` solution: it proves that the separate tropical
conditions (even together with a common residue solution of the displayed
initial forms) cannot establish normalization.  Any successful 2-adic route
must exploit higher consequences of the full coefficient ideal that rule out
the balanced negative cycle (7).

The exact audit for (4)--(7) is
`computations/verify_valuation_normalization_obstruction.py`.

## 4. The all-ones initial point fails at the next 2-adic order

Although the star valuation in Section 3 satisfies every generator initial
form at the all-ones residue point, that particular point does not lift even
one further 2-adic digit.  Write the entries on `01` and `02` as

\[
 2^{-1}(1+2z_{uv}^{ab})
\]

and all other entries as `1+2z_uv^{ab}`.  In a fixed coloring equation,
multiplication by `2` followed by reduction modulo `4` leaves precisely the
six minimum-valuation matching terms.  Their constant parts cancel, and the
next-order condition is a linear equation over `F_2`: the sum of the entry
bits occurring in those six matchings is zero for a nonconstant coloring and
one for the constant colorings.

The resulting `729`-row binary system has coefficient rank `45`, whereas its
augmentation has rank `46`.  A particularly small left-kernel certificate is
the XOR of the four coloring equations

\[
 000000,\qquad000001,\qquad000010,\qquad000011.             \tag{8}
\]

Every first-order variable occurs an even number of times in (8), while the
right-hand sides XOR to one.  Hence no choice of the `z` variables can lift
the all-ones initial point over `Q_2` (or over an unramified extension with
the same first-order expansion).

This is a genuine higher/deformation obstruction, but it is not yet an
exclusion of the valuation vector from the full tropical variety.  Other
torus-valued residue solutions of the initial ideal, or lifts after a
ramified extension, still have to be ruled out.  The exact rank computation
and the four-row certificate are audited by
`computations/verify_star_valuation_lift_obstruction.py`.
