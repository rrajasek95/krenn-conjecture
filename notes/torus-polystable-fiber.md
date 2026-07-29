# Closed torus orbits and balanced supports in the exact fiber

## 1. The target-stabilizing torus

Let `B` have even cardinality `n`, put `V_v=C^3`, and write

\[
 W=\bigoplus_{u<v}V_u\otimes V_v,\qquad
 \Phi(A)=\sum_{M\in\operatorname{PM}(B)}
              \bigotimes_{uv\in M}A_{uv}.
\]

The target is

\[
 \Delta=\sum_{i=0}^2e_i^{\otimes B}.
\]

Consider the connected diagonal torus

\[
 T=T_\Delta=
 \left\{(\lambda_{v,i})\in(\mathbb C^*)^{B\times[3]}:
       \prod_{v\in B}\lambda_{v,i}=1\quad(i=0,1,2)\right\}.
                                                               \tag{1}
\]

It acts on a source coordinate by

\[
 A_{uv}(i,j)\longmapsto
 \lambda_{u,i}\lambda_{v,j}A_{uv}(i,j).                      \tag{2}
\]

The matching map is equivariant, and (1) fixes `Delta`.  Consequently the
affine fiber

\[
                         \mathcal F=\Phi^{-1}(\Delta)          \tag{3}
\]

is closed and `T`-invariant.

## 2. A closed orbit exists in every nonempty exact fiber

**Lemma 2.1 (polystable-fiber reduction).**  If `mathcal F` is nonempty,
then it contains a point `A` whose `T`-orbit is closed in `W`.  This point is
nonzero.

**Proof.**  Choose an orbit of minimum dimension among all `T`-orbits in
`mathcal F`.  An algebraic-group orbit is locally closed and open in its
closure.  If the chosen orbit were not closed, every orbit in its nonempty
boundary would have strictly smaller dimension.  The boundary is still in
`mathcal F`, because (3) is closed and invariant, contradicting minimality.
Thus the orbit is closed in `mathcal F`; since `mathcal F` is closed in
`W`, it is closed in `W` as well.  Finally `0` is not in (3), because
`Phi(0)=0` whereas `Delta` is nonzero.  \(\square\)

This argument is only the affine closed-orbit theorem specialized to a
torus; it does not require choosing a norm, a support-minimal point, or a
compact form of `T`.

## 3. Closed orbit is exactly strict incidence balance

For a nonzero coordinate

\[
                    s=(uv;i,j),
\]

let

\[
 a_s=e_{u,i}+e_{v,j}\in\mathbb Z^{B\times[3]}              \tag{4}
\]

be its ambient diagonal weight, and let `bar a_s` be its restriction to
`T`.  If `S(A)` is the set of nonzero source coordinates, the standard
torus orbit criterion says

\[
 T\mathbin{\cdot} A\text{ is closed}
 \quad\Longleftrightarrow\quad
 0\in\operatorname{relint}\operatorname{conv}
       \{\bar a_s:s\in S(A)\}.                              \tag{5}
\]

For completeness, if the right side fails, rational separation gives a
cocharacter `h` with
`<h,bar a_s> >= 0` for every supported weight and a strict inequality for
at least one.  The limit `lim_(t->0) h(t) A` exists, loses a nonzero weight
component, and is outside the orbit, so the orbit is not closed.

Conversely, relative-interior membership gives positive rational numbers
`q_s` with `sum_s q_s bar(a_s)=0`.  After clearing denominators,

\[
                         f=\prod_{s\in S(A)}z_s^{m_s}
\]

is a `T`-invariant coordinate monomial with every `m_s>0`, and `f(A)` is
nonzero.  It remains nonzero on the orbit closure, so no supported
coordinate can vanish at a boundary point.  Inside the coordinate torus
where precisely these coordinates are nonzero, `T dot A` is a coset of the
image of a torus homomorphism and is closed.  Hence the orbit has no
boundary.  This proves (5) without an appeal to an analytic norm.

Membership of zero in the relative interior in (5) is equivalent to a
strictly positive dependence

\[
                 \sum_{s\in S(A)}\alpha_s\bar a_s=0,
                 \qquad \alpha_s>0.                         \tag{6}
\]

Repeated weights cause no problem: split a positive coefficient among all
coordinates having that weight.  Define the weighted incidence at the
vertex-color port `(v,i)` by

\[
 d_{v,i}=\sum_{s\in S(A)}\alpha_s a_s(v,i).                 \tag{7}
\]

The characters of the ambient diagonal torus which restrict trivially to
`T` are precisely the span of the three column sums

\[
                         g_i=\sum_{v\in B}e_{v,i}.
\]

Therefore (6) is equivalent to

\[
                    d_{v,i}=c_i
       \quad\text{for every }v\in B\text{ and }i\in[3],     \tag{8}
\]

where `c_i` may depend on the color but not on the vertex.

Combining this observation with Lemma 2.1 gives the promised exact
reduction.

**Theorem 3.1 (balanced exact representative).**  If
`Phi^{-1}(Delta)` is nonempty, it contains a point `A` and strictly positive
weights on *every* nonzero endpoint-color entry of `A` for which (8) holds.
The weights may be chosen positive rational, and hence positive integral
after a common rescaling.  Moreover `c_i>0` for all three colors.

**Proof.**  Take the closed-orbit point from Lemma 2.1 and apply (5)--(8).
The equations have integer coefficients.  Rational points are dense in
their real solution space, so strict feasibility gives a positive rational
solution and clearing denominators gives an integral one.  Finally, the
coefficient of \(e_i^{\otimes B}\) in `Phi(A)` is one.  Some perfect-matching
monomial in that coefficient is consequently nonzero, so every vertex has
a supported occurrence of color `i`.  Positivity in (7) then gives
`c_i>0`.  \(\square\)

Thus the support can be viewed as a graph on the `3n` ports `(v,i)`, with a
supported `(uv;i,j)` entry joining `(u,i)` to `(v,j)`: positive integral
edge multiplicities make the port degrees constant across vertices within
each color.

There is a useful analytic strengthening: the balancing weights can be made
the actual squared magnitudes of a gauge-equivalent exact source.

**Lemma 3.2 (squared-magnitude balance).**  If the exact fiber is nonempty,
it contains a point `A` such that

\[
 \sum_{u\ne v}\sum_j |A_{uv}(i,j)|^2=c_i
       \qquad(v\in B,\ i\in[3]),                            \tag{9}
\]

with the endpoint order interpreted naturally and with every `c_i>0`.

**Proof.**  Start with the closed-orbit point in Lemma 2.1 and restrict to
the positive-real part of `T`, writing its elements as
`lambda_(v,i)=exp(x_(v,i))` with `sum_v x_(v,i)=0`.  Its squared norm is

\[
 f(x)=\sum_{s\in S(A)}|A_s|^2
             \exp(2\langle x,a_s\rangle).                  \tag{10}
\]

Condition (5) says that zero is in the relative interior of the convex hull
of the projected supported weights.  Hence (10) is coercive after quotienting
by the common kernel of those weights, and it attains a minimum.  (Along a
unit ray outside the kernel, relative-interior membership supplies a
supported weight with uniformly positive pairing, so the corresponding
exponential tends to infinity.)  At a minimizer, differentiation in every
`x` with zero color-column sums gives

\[
 \sum_s |(\lambda A)_s|^2\langle x,a_s\rangle=0.            \tag{11}
\]

The vector of squared port incidences is therefore orthogonal to every such
`x`; as in (8), it is constant over vertices separately in each color.  The
gauge lies in `T`, so it preserves the exact fiber.  Finally the nonzero
constant-color coefficient forces a supported color-`i` occurrence at every
vertex, giving `c_i>0`. `QED`

## 4. Balance plus anchors and coefficient supports is insufficient

The preceding reduction does not close the six-vertex problem, even when it
is combined with all currently used Boolean coefficient-support conditions.
The failure has a uniform exact support model.

**Proposition 4.1 (uniform balanced-anchor countermodel).**  For every even
`n >= 6`, there is a source point with all of the following properties.

1. For every vertex `v` and color `i`, an incident rank-one edge has the
   coordinate factor `e_i` at both endpoints.  Thus it satisfies the forced
   directed-anchor conclusion, in a stronger same-color form.
2. Every coloring has at least two supported perfect-matching monomials.
   In particular, every constant fiber is nonempty and no mixed fiber is a
   singleton.
3. Its support is strictly `T`-balanced; assigning weight one to every
   supported endpoint-color entry gives `d_(v,i)=7` for every `(v,i)`.
   Consequently its `T`-orbit is closed.
4. Every active matrix not used as a rank-one anchor can be chosen
   invertible with full `3 by 3` support.

**Proof.**  A one-factorization of `K_n` supplies five pairwise edge-disjoint
perfect matchings

\[
                         P,P',Q_0,Q_1,Q_2.                  \tag{12}
\]

(For a direct construction, use vertices `infinity` and `Z/(n-1)`, and in
round `r` pair `infinity` with `r` and `r+k` with `r-k`.)  Put the
full-support invertible matrix `I+J` on every edge of `P union P'`, where
`J` is the all-ones matrix, and put `e_i e_i^T` on every edge of `Q_i`.
Set all other matrices to zero.

The matching `Q_i` gives the requested color-`i` anchor at every vertex.
For an arbitrary coloring, both `P` and `P'` select only nonzero entries of
`I+J`, so they give two distinct supported monomials.  At a fixed port
`(v,i)`, each of the two full-support matching edges contributes its three
cells in row or column `i`, while the unique `Q_i` edge contributes one.
Thus its incidence is `3+3+1=7`, proving strict balance.  Finally
`det(I+J)=4`, so the non-anchor matrices are invertible.  \(\square\)

At `n=6`, one completely explicit choice is

\[
\begin{aligned}
 P&=\{01,23,45\},&P'&=\{05,12,34\},\\
 Q_0&=\{02,14,35\},&Q_1&=\{03,15,24\},\\
 Q_2&=\{04,13,25\}.&&
\end{aligned}                                               \tag{13}
\]

Here `P union P'` is a six-cycle and the three anchor matchings form its
cubic complement.  This is exactly the saturated `F=C_6` support chart.
Every triangle also contains a basis edge, so the coordinate-torus-zero
condition is vacuous on this model.  That chart is eliminated only after
using numerical binomial relations among four coefficient fibers: the free
rectangles in `proofs/saturated-rank-graph-obstruction.md` force every
`2 by 2` minor of a cycle matrix to vanish.  Proposition 4.1 shows that
closed-orbit balance, forced anchors, rank witnesses, and the
constant-nonempty/mixed-no-singleton support rules cannot replace that
algebraic cancellation step, either for `n=6` or uniformly in even order.

This countermodel is nevertheless excluded uniformly by genuine
Laurent/source-ideal relations.  On the rank-one stratum, clean mixed fibers
differing at one vertex force the ratio of the two universal Hamilton-cycle
monomials to be color-independent.  More strongly, the five factors can be
chosen so that the three anchor factors form a 3-connected cubic graph.
Robust clean coloring rectangles then force every `2 by 2` minor of each
universal-cycle matrix to vanish, reducing arbitrary full matrices to the
rank-one argument; activating one anchor chord finally leaves a single
nonzero mixed monomial.  The uniform proof is
`proofs/uniform-five-factor-toric-obstruction.md`.  It shows exactly why the
Boolean and moment-map conditions miss the contradiction, while isolating
the remaining global gap: an arbitrary balanced support may have additional
edges contributing to all of these clean fibers.

That gap cannot be removed by taking another target-torus support face.
Lemma 9.1 of the cited proof observes that every matching monomial in a fixed
coloring has the same target-torus weight.  Under a finite nonnegative
one-parameter limit, survival of one monomial therefore forces survival of
every supported monomial in the same coefficient fiber.  Thus target-torus
minimality can neither isolate the two clean Hamilton-cycle terms nor discard
their extra cancellation mates; a non-torus ideal identity or a separate
structural absence theorem is necessary.
