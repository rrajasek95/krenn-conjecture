# Generalized Laurent elimination on sparse residual fibers

This note records a sound extension of the binomial-lattice tests in
`computations/verify_f3_toric_obstruction.py`.  It turns sparse fibers with
more than two terms into exact rational power relations and then detects
multiplicative contradictions among those powers.  The implementation is
`computations/generalized_laurent_elimination.py`.

## 1. Exact quotient and power-relation lemma

Fix a support chart and give each supported exceptional entry and each
supported rank-one factor coordinate a formal nonzero variable.  A supported
matching term is a Laurent monomial `x^a`.  Every mixed two-term coefficient
fiber gives

\[
 x^{d_i}=-1,\qquad d_i=a_i-b_i.                         \tag{1}
\]

Choose independent rows `B_1,...,B_r` among the `d_i` such that some
`r by r` coordinate minor of `B` has determinant `+1` or `-1`.  The selected
row lattice is then a direct summand of the ambient integer exponent lattice.
The checker additionally verifies that every other binomial difference is an
integer combination of the selected rows and that its required sign in (1)
agrees with the parity of that combination.

Every integer exponent now has a canonical decomposition

\[
 a=q+zB,
 \qquad x^a=(-1)^{\sum_i z_i}x^q,                       \tag{2}
\]

obtained with the inverse of the unimodular minor.  Reduce all terms of any
other mixed zero fiber by (2) and combine equal `q` classes.  One surviving
class is already impossible.  If exactly two classes remain, the fiber is

\[
 c_0x^{q_0}+c_1x^{q_1}=0
 \quad\Longrightarrow\quad
 x^e=-c_0/c_1=:r,
 \qquad e=q_1-q_0,                                     \tag{3}
\]

where `c_0,c_1` are nonzero integers and `r` is a nonzero rational number.

**Multiplicative dependency lemma.**  Given relations `x^{e_j}=r_j` from
(3), any integers `n_j` satisfying

\[
 \sum_j n_je_j=0                                       \tag{4}
\]

must also satisfy

\[
 \prod_j r_j^{n_j}=1.                                  \tag{5}
\]

Thus an exact dependency (4) for which the rational product in (5) is not
one rules out the support chart over every characteristic-zero field.  Prime
valuations and signs are simply convenient ways for (5) to fail.  Negative
`n_j` are valid because every chart variable, hence every Laurent monomial,
is nonzero.

The checker performs rational row reduction with provenance, clears
denominators to recover an integer dependency, and independently rechecks
both (4) and (5).  A synthetic regression test uses `x^u=-2` and
`x^(2u)=2`.

## 2. One exact `3P2` certificate

Take exceptional edges

\[
 F=\{01,23,45\}.
\]

All nine entries of each exceptional matrix are supported.  On each
rank-one edge below, the pair lists the factor support at the smaller and
larger endpoint:

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
02&(0),(0)&03&(2),(2)&04&(0),(1)\\
05&(012),(012)&12&(1),(0)&13&(012),(012)\\
14&(2),(2)&15&(1),(1)&24&(012),(012)\\
25&(2),(2)&34&(1),(1)&35&(0),(0).
\end{array}                                             \tag{6}
\]

Direct enumeration checks the forced-anchor condition, nonempty constant
fibers, and the absence of any one-term mixed fiber.  The exact two-term
fibers have a rank-25 basis with a coordinate minor of absolute determinant
one, and every redundant binomial has the forced odd sign.

Write `M_i` for matching index `i` in the lexicographic enumeration used by
`search_f5_support_sat.py`; the indices needed here are

\[
\begin{array}{c|l}
0&01,23,45\\
1&01,24,35\\
3&02,13,45\\
13&05,13,24\\
14&05,14,23.
\end{array}                                             \tag{7}
\]

Laurent reduction of three four-term fibers gives

\[
\begin{array}{c|c|c|c}
\text{coloring}&\text{exact support}&(c_0,c_1)&r\\ \hline
(0,0,0,0,1,0)&\{0,1,3,13\}&(-1,1)&1\\
(0,2,0,0,2,1)&\{0,3,13,14\}&(1,1)&-1\\
(0,2,1,0,2,0)&\{0,1,13,14\}&(-1,1)&1.
\end{array}                                             \tag{8}
\]

For their normalized power exponents, exact integer arithmetic gives

\[
 -e_1-e_2+e_3=0.                                        \tag{9}
\]

But the same combination of their values is

\[
 1^{-1}(-1)^{-1}1=-1\ne 1,                              \tag{10}
\]

contradicting the multiplicative dependency lemma.  This is a sign
obstruction extracted from four-term fibers; it is not merely a count of
support models.

Run the solver-independent audit with

```sh
uv run python computations/verify_generalized_laurent_3p2.py
```

The verifier reconstructs all fibers directly from (6), checks the support
axioms, verifies the unimodular binomial quotient, derives (8), and rechecks
(9)--(10).  The chart was found by a SAT search with fixed nonzero-minor
witnesses, but no SAT solver participates in this certificate audit.

## 3. Scope

This certificate eliminates the single labeled support chart (6).  It does
not yet prove that every surviving `3P2` chart, every `P4+2P1` chart, or every
residual graph with `|F|<=3` supplies such a dependency.  The reusable finite
task is now precise: on each stabilized survivor, form the exact binomial
quotient, extract all one- and two-class reductions, and either exhibit a
multiplicative dependency or retain the chart for a stronger elimination
step.

## 4. Four-fiber certificates on both two-edge graphs

Two individual support charts from the residual `F=2` search admit a still
smaller specialization of the same lemma.  In each chart, three exact
binomial fibers have differences `d_1,d_2,d_3`, and one exact trinomial has
matching exponents `a,b,c`.

For the `2P2+2P1` chart with exceptional edges `{01,23}`, the source
colorings are

\[
 (0,0,0,0,0,1),\quad(0,0,0,0,0,2),\quad(0,0,0,0,1,2),
\]

each with exact matching support `{1,14}`.  The target coloring
`(0,0,0,0,1,1)` has exact support `{0,1,14}`, and direct integer exponent
comparison gives

\[
 a_{14}-a_1=-d_1+d_2-d_3.                               \tag{11}
\]

The coefficient sum on the right is odd, so the three source equations
force `x^{a_14}=-x^{a_1}`.  Those target terms cancel and the target equation
would say that its remaining supported term `x^{a_0}` is zero.

For the `P3+3P1` chart with exceptional edges `{01,12}`, source colorings

\[
 (0,0,0,0,1,1),\quad(0,0,1,0,0,0),\quad(0,0,1,0,1,0)
\]

all have exact support `{2,9}`.  Coloring `(0,0,0,0,0,1)` has exact support
`{1,2,9}`, and

\[
 a_9-a_2=-d_1-d_2+d_3.                                  \tag{12}
\]

Again the odd combination cancels the two indicated target terms and leaves
the supported term `x^{a_1}` equal to zero.

`computations/verify_small_laurent_f2_certificates.py` hardcodes the two
complete support charts, reconstructs all 729 coefficient fibers, audits the
forced anchors and support conditions, and checks (11)--(12) coordinate by
coordinate.  It invokes no SAT solver.  These small certificates explain two
representative cuts; the separate dynamic CEGAR exhaustion is what closes all
support charts of the two graph types.

Finally, `computations/test_generalized_laurent_elimination.py` adversarially
checks the reusable engine on seven families: a compatible power dependency
that must not be cut, an inconsistent rational-power dependency, unequal
values for one exponent, a one-class obstruction, a redundant odd sign
cycle, a nonprimitive lattice that must be declined, and forty random
unimodular coordinate shears.

## 5. Representative one-edge and empty-graph certificates

The same minimal pattern already occurs on individual charts below `F=2`.
For a `P2+4P1` chart, three `{0,4}` binomial fibers with colorings

\[
 (0,0,0,0,0,1),\quad(0,0,0,0,0,2),\quad(0,0,0,0,1,2)
\]

combine with coefficients `(-1,1,-1)`.  They force the matching-0 and
matching-4 terms to cancel in the `{0,4,11}` fiber at coloring
`(0,0,0,0,1,1)`, leaving the supported matching-11 monomial equal to zero.

On a representative empty-exceptional-graph chart, the three exact
binomial fibers

\[
\begin{array}{c|c}
(0,2,0,0,0,1)&\{9,10\}\\
(0,2,0,0,1,1)&\{3,6\}\\
(0,2,0,0,2,1)&\{4,7\}
\end{array}
\]

have exponent differences `d_1,d_2,d_3` satisfying

\[
 -d_1-d_2+d_3=0.
\]

The coefficient sum is odd, so multiplying the three binomial equations
gives the direct contradiction `1=-1`.

`computations/verify_small_laurent_f1_f0_certificates.py` independently
reconstructs both complete charts, audits all support conditions, and checks
these integer identities without SAT.  As above, these are minimal examples
of the learned obstruction; the full lexicographic CEGAR run is responsible
for exhaustive closure of each graph type.
