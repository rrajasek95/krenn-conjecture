# The complete committed order-four output cascade misses the relative cap generator

Exact finite obstruction in the committed polynomial model.  This does not
exclude a genuinely new source-resolution row, an edge-dependent
localization, order five or higher, the curved OO overlap theorem, or Krenn's
conjecture.

## Outcome

The desired relative generator has augmented boundary

\[
 q=(0,+\kappa Y,0,0)                                  \tag{1}
\]

in `(Eq,w,target,ordinary-residue)` coordinates.  The complete
fine-multidegree output cascade of total ordinary order at most four was
formed from:

* every order-\(\le4\) multiset of differential directions in the bounded
  55-variable ring;
* every face of the fifteen literal four-direction Hasse cubes;
* all 6561 labelled full-nine rows and both chart copies;
* all fifteen denominator columns and all of their internal faces; and
* the split-cap columns `T,rho`, with physical target and ordinary residue.

After source relations are imposed, (1) is not in this module.  The exact
compressed physical rank is three, and adjoining (q) raises it to four.
An integral polynomial cokernel covector reads (+\kappa Y\) on (q).
Thus there is no source-provenant (n_c) in the committed order-four
module.

The obstruction names the smallest additional row exactly: a new
source-resolution generator whose edge-zero Eq boundary has no
homogenizing-\(u\) part, whose (w)-boundary is (+\kappa Y), and whose
target and ordinary residue are zero.  The formal fourth-Hasse generator
has those last three properties but fails the first one when projected to
the physical source.

## 1. Complete order-four direction census

For the fixed mixed word

```text
01211222
```

the direct-free mixed hafnian (A=H_m) is a sum of 90 squarefree quartic
matching monomials in 27 mixed edge variables.  The corresponding pure
row uses 27 disjoint pure edge variables, and the homogenizer (u) is the
55th variable.

The exact multiset census is

| ordinary order | direction multisets | containing `u` |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 55 | 1 |
| 2 | 1,540 | 55 |
| 3 | 29,260 | 1,540 |
| 4 | 424,270 | 29,260 |
| **total** | **455,126** | **30,856** |

At order four the exhaustive pruning is

| reason | count |
|---|---:|
| contains a pure edge | 367,605 |
| contains `u` | 29,260 |
| repeated mixed direction | 9,855 |
| four distinct mixed edges, not a matching of (A) | 17,460 |
| **q-zero matching top** | **90** |

This is the complete φ/weight reduction, not a search over the fifteen
previously selected cubes.  Lower order leaves an uncontracted mixed edge;
pure or (u) directions annihilate (A); repetitions vanish by
multiaffinity; and four distinct mixed directions return a scalar exactly
when they are one of the 90 monomials of (A).

Of these 90 tops, exactly 15 contain the physical `pq` edge.  They are
precisely the already committed five-deletion-times-three-matching cubes
and have sector placement

```text
pq-direct / pr-two-star.
```

The other 75 are `pq-two-star / pr-two-star`; they carry no direct-to-star
chart transfer.  The `pr`-direct count is zero because that block is the
fixed direct-free block.  Hence cross-selection tops are retained and
classified rather than silently discarded.

## 2. All lower faces and literal columns

The checker reruns the complete frozen reset/Hasse audit before doing the
new census.  Its literal data are:

* 15 selected cubes and all 16 faces of each;
* the exact identity

  \[
  [d,\pi_U]\mathcal N
       =(\partial_UH_m)(H_0-u)e_{\rm Eq},\qquad
  \operatorname {ores}(\pi_U\mathcal Z)
       =-\kappa Y\partial_UH_m                         \tag{2}
  \]

  for every nonbottom face;
* all fifteen denominator columns, including the `5,3,3,1` support ladder;
* the twenty distinct internal face/column leak polynomials, of rank 12
  over 22 monomials;
* all 6561 four-edge full-nine rows; and
* the chart-odd/even and cap target/residue ledgers.

At the q-zero face, ∂_U H_m=1.  Equation (2) says exactly that the
tempting cap value comes with the physical Eq defect

\[
                    (H_0-u)e_{\rm Eq}.                 \tag{3}
\]

The denominator top gives the same pair: its readout is a chain map if and
only if its ordinary residue is zero.  Killing the leak (3) kills the
cap/residue readout.  The strict chart difference is globally boundaryless
and capless; the chart-even combination carries the cap graph and is not
invisible.

## 3. The four-coordinate complete quotient

Set every labelled edge variable to zero and retain the coefficient of the
unique homogenizing factor (u e_{\rm Eq}).  Equivalently, factor the
edge-zero Eq boundary by (u).  This is legitimate for arbitrary
polynomial row coefficients because the committed full-nine convention is

\[
 F_\alpha|_{\mathrm{edges}=0}
       =-\operatorname {tgt}(g_\alpha)u.                \tag{4}
\]

Use coordinates

\[
       (u e_{\rm Eq},w,\operatorname {tgt},
                         \operatorname {ores}).         \tag{5}
\]

Every literal physical column in the complete finite module specializes
to the span of the following four types:

\[
\begin{array}{c|rrrr}
 &u e_{\rm Eq}&w&\operatorname {tgt}&\operatorname {ores}\\ \hline
\text{full-nine target row}&-1&0&1&0\\
T&0&-Y&1&0\\
\rho&0&1&0&1\\
\text{q-zero Hasse/denominator top}&-1&Y&0&0.
\end{array}                                             \tag{6}
\]

The last column is the first column minus the `T` column.  All lower
positive-q faces specialize to zero, every strict chart difference is
zero, and arbitrary polynomial multiples remain in this span by (4).
Thus (6) is the compressed **complete** physical module, not a selected
sample.  It has rank three.

Now define

\[
                \Lambda=(Y,1,Y,-1).                    \tag{7}
\]

Direct substitution gives

\[
 \Lambda C=0\quad\text{for every column }C\text{ of (6)},
 \qquad
 \Lambda(q)=\kappa Y\ne0.                              \tag{8}
\]

Equivalently, the determinant of the first three independent physical
columns together with (q) is

\[
                         -\kappa Y.                     \tag{9}
\]

On the active curvature/cap open, this is nonzero.  Equations (7)--(9) are
the promised integral/rational cokernel certificate.  They also explain
the formal/physical distinction without a slogan: upstairs the prolonged
top is (q); diagonal physical projection adds the `-1` Eq entry and turns
it into the fourth column of (6), on which Λ vanishes.

## 4. The `u`-containing operator lemma

The secondary hybrid check is simple but should be stated narrowly.  Both
(A) and (A^2) are independent of (u).  Therefore every differential
monomial of ordinary order at most four containing \(\partial_u\) satisfies

\[
                 \partial_TA=\partial_T(A^2)=0.         \tag{10}
\]

A polynomial coefficient written on the left does not change zero.  Hence
such terms cannot alter either the unit normalization (D(A)) or the
(A^2)-**generator** constraint.  The checker counts all 30,856 such
multisets and tests (10) at every order.

This does **not** say that ∂_u is irrelevant on arbitrary multiples
(fA^2): Leibniz can differentiate (f).  It therefore does not close the
variable-coefficient hybrid operator problem in every ideal-level
formulation.  It proves only the simple load-bearing lemma requested here.

## 5. Scope and reproduction

The completeness claim is relative to the committed polynomial codomain:
the existing full-nine row module, its identical pq/pr copies, the complete
denominator presentation, the split cap, and their order-four principal
parts.  Polynomial coefficients are arbitrary.  The result does not
exclude:

* a genuinely new row in a larger, presently uncommitted source resolution;
* localization by an edge-dependent source equation (which is zero on the
  source and is excluded by the polynomial-source hypothesis);
* order five or higher; or
* a different physical ordinary-residue comparison.

Those are real scope boundaries.  Within the stated module, the rank and
cokernel certificate are exact and order four is closed, so the calculation
stops before order five as requested.

Run

```text
python3 computations/verify_oo_complete_order4_spencer_output_cascade.py
python3 -O computations/verify_oo_complete_order4_spencer_output_cascade.py
```

The checker reruns the frozen full reset/Hasse lock, exhausts all 455,126
direction multisets, verifies the 90/15/75 top-sector census, checks the
four-coordinate module and determinant, and audits the (u)-operator
lemma.  Frozen digest:

```text
6bd1fe74846c6e3fbcb04618ebb369922593060791e97216c76d376f82e36206
```
