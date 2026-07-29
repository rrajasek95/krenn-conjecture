# Constructive counterexample search: exact obstruction to extending the signed two-color gadget

## 1. The attempted construction

Use vertices `0,...,5`.  The exact signed realization of
`Delta_(6,2)` has underlying support

\[
 B=\{01,02,05,12,13,23,34,45\}.                         \tag{1}
\]

Its complement has exactly two perfect matchings,

\[
 Q=\{03,14,25\},\qquad Q'=\{03,15,24\}.                 \tag{2}
\]

Thus these are the only ways to superpose a third-color matching whose
three underlying pairs are all absent from the two-color gadget.

The most literal superposition already fails visibly.  Keep the matrices of
`computations/verify_cancellation_example.py` and put `e_3 tensor e_3` with
weight one on every edge of `Q`.  Besides the three terms realizing
`Delta_(6,2)` and the all-3 term, the supported matchings give the four
singleton mixed tensors

\[
\begin{aligned}
 &(1,1,3,2,2,3), &&(2,1,3,2,2,3),\\
 &(3,2,2,3,1,1), &&(2,3,1,1,3,2),                          \tag{3}
\end{aligned}
\]

each with coefficient `+1`.  For `Q'`, there are three singleton mixed
coefficients (one has coefficient `-1`).  Hence simple superposition does
not work.

The next theorem is stronger: changing *all* matrices and weights on the
resulting eleven-pair support cannot repair the construction.

## 2. An arbitrary-matrix obstruction for the whole eleven-edge chart

**Theorem.**  Let `G` be either `B union Q` or `B union Q'`.  If
`A_uv=0` outside `G`, then no collection of arbitrary asymmetric complex
`3 by 3` matrices `A_uv` satisfies

\[
 \Phi(A)=\Delta_{6,3}.                                      \tag{4}
\]

**Proof.**  Both graphs have the following common abstract form.  Four
vertices form a complete graph `K_4`; call this set `C`.  The remaining
vertices are `x,y`, the edge `xy` is present, and each of `x,y` has two
neighbors in `C`.  Their two neighbor sets `U=N(x) \cap C` and
`V=N(y) \cap C` partition `C` into two pairs.  For `B union Q`, for example,

\[
 C=\{0,1,2,3\},\quad x=4,\quad y=5,\quad
 U=\{1,3\},\quad V=\{0,2\}.                                \tag{5}
\]

The graph degrees of `x` and `y` are three.  None of their incident
matrices can vanish: otherwise the star expansion at that vertex would
have partition rank at most two, while `Delta_(6,3)` has partition rank
three.  The cubic-vertex rigidity lemma (`notes/finite-obstruction.md`,
Lemma 7.1) therefore applies at both vertices.  Every edge incident to
`x` or `y` is a nonzero same-color basis tensor, and the three colors occur
once at each of these vertices.

Let the color of `xy` be `a`; call the other colors `b,c`.  For each
`r in {b,c}`, let `u_r in U` be the endpoint of the color-`r` edge from
`x`, and let `v_r in V` be the endpoint of the color-`r` edge from `y`.
All scalar edge factors mentioned below are nonzero.

First take the output slice in which the colors at `(x,y)` are `(a,a)`.
Only matchings using `xy` contribute, so the matching tensor on the core
must obey

\[
 H_C=\lambda e_a^{\otimes C},\qquad \lambda\ne0.             \tag{6}
\]

Now take a slice `(r,s)` at `(x,y)`, with `r,s in {b,c}`.  The two
peripheral edges are uniquely determined: they are `xu_r` and `yv_s`.
The remaining two core vertices have a unique joining edge, namely
`u_{\bar r}v_{\bar s}`, where the bar exchanges `b` and `c`.  Consequently
this entire slice consists of one nonzero peripheral scalar times

\[
 e_r^{(u_r)}\otimes e_s^{(v_s)}\otimes A_{u_{\bar r}v_{\bar s}}. \tag{7}
\]

For `r \ne s` the target slice is zero, so

\[
 A_{u_c v_b}=A_{u_b v_c}=0.                                 \tag{8}
\]

For `r=s`, the target slice is the corresponding constant tensor, so the
other two cross edges are nonzero pure tensors:

\[
 A_{u_c v_c}=\alpha e_b\otimes e_b,\qquad
 A_{u_b v_b}=\beta e_c\otimes e_c,qquad \alpha\beta\ne0.   \tag{9}
\]

Expand the four-vertex matching tensor `H_C`.  The cross matching using
the two edges in (8) vanishes.  The cross matching using (9) is a nonzero
simple tensor `T`; across the bipartition `U|V`, its left and right factors
are coordinate tensors involving only `b,c`.  The final core matching is
the product of the two within-pair matrices, say

\[
 S=A_{u_bu_c}\otimes A_{v_bv_c},                            \tag{10}
\]

which has matrix rank at most one across `U|V`.  Equation (6) would require

\[
 S=\lambda e_a^{\otimes C}-T.                               \tag{11}
\]

The two rank-one summands on the right have linearly independent left
factors and linearly independent right factors: the first uses color `a`
at both sites, while the second uses colors `b,c`.  Their difference has
matrix rank exactly two across `U|V`, contradicting (10).  This proves the
theorem. \(\square\)

## 3. A wider monomial-rank-one search

There is also an exact finite obstruction when every underlying pair is
allowed but each aggregate matrix has at most one nonzero coordinate entry.
Each supported perfect matching then produces one basis tensor.  The three
constant coefficients force three edge-disjoint monochromatic perfect
matchings.  Up to relabeling, their union is either the triangular prism or
`K_(3,3)`.  The other six pairs have `9^6` possible ordered endpoint-color
assignments.  Exhaustive enumeration in each case finds that some mixed
coloring is produced by exactly one perfect matching for every assignment
(the minimum number of singleton mixed fibers is six for the prism and four
for `K_(3,3)`).  Thus scalar weights cannot cancel all mixed outputs in this
monomial rank-one ansatz.

This last statement is an exact finite classification, but the eleven-edge
theorem above is the more conceptual obstruction and allows completely
arbitrary matrices on its support.

## 4. Eight-vertex endpoint labels and root-of-unity pairing

The six-vertex singleton phenomenon does not persist literally.  The exact
SAT search `computations/search_monomial_no_singleton_sat.py` finds an
endpoint-labeled `K_8` for which every one of the 38 mixed coloring fibers
has exactly two perfect matchings.  The independent audit
`computations/verify_monomial_n8_counterexample.py` nevertheless extracts
three fibers whose matching-ratio exponent vectors obey

\[
                         -d_1+d_6+d_{10}=0.
\]

Cancellation would set all three ratios to `-1`, while this relation forces
`R_6R_10/R_1=1`; hence the support has no nonzero complex edge weighting.

A broader finite sufficient search assigns every supported edge a phase in
`Z/mZ` and requires all mixed matching terms to cancel in equal-coloring
pairs, while leaving a positive phase-zero surplus in every constant fiber.
The script `computations/search_monomial_phase_pairing_sat.py` exhausts all
13 orbits of triples of edge-disjoint target matchings on eight vertices.
Cadical reports UNSAT for each orbit at `m=2,4,8`; the script independently
checks any returned model before accepting it.  Thus there is no
pairwise-cancelling monomial counterexample of these three root-of-unity
orders.  This remains a search result rather than a general obstruction:
fibers of three or more terms can cancel without a pairing, and a toric
solution of larger torsion order is not covered by the three runs.
