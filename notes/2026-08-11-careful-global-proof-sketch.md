# Careful global proof sketch

Audit date: 2026-08-11.

This is a conditional proof skeleton.  Every arrow is labelled `PROVED`,
`FORMAL AFTER INPUT`, or `OPEN`.  The point is to show exactly how the local
matching-base work would imply Krenn's conjecture without silently assuming a
support-skeleton extraction theorem.

## 1. Extremal statement and tensor model

After aggregating parallel sources with the same physical edge and ordered
endpoint colours, write their total cell as `A_uv(i,j)`.  The perfect-matching
sum is the tensor

\[
 H_B(A)=\sum_M\prod_{uv\in M}A_{uv}
       \in (\mathbb C^D)^{\otimes B}.                      \tag{1}
\]

Monochromaticity is exactly

\[
                       H_B(A)=\Delta_{B,D}
                         :=\sum_{i=1}^{D}e_i^{\otimes B}.  \tag{2}
\]

Endpoint order, offdiagonal colours, and complex cancellation are retained in
(1).  Projecting a palette of size at least three onto any three colours gives
the ternary equation

\[
                         H_B(A)=\Delta_{B,3}.              \tag{3}
\]

Thus the upper bound for even `n>=6` follows once (3) is impossible.  The
support-only lower bounds are the parallel edges at `n=2`, a one-factorization
of `K4`, and the two alternating matchings of `C_n`.

Status: the reformulation, palette projection, lower bounds, `n=4` upper
bound, and terminal six-site ternary obstruction are `PROVED` in the proof
spine.

## 2. Outer induction: clean-pair descent

Assume a ternary solution of minimum even order `n>=8`.  Within that order,
choose a maximum-anchor and then minimum-support representative.  The proved
curvature-line and anchor-synchronization theorems select a physical pair
`p,q` and a projective cap line on which the deletion is generically active.
Let

\[
                         {\cal E}_{p,q}                    \tag{4}
\]

be the clean error restricted to that line.

If (4) has an **active zero**, exact clean-pair descent constructs

\[
                  H_{B\setminus\{p,q\}}(A')
                       =\Delta_{B\setminus\{p,q\},3}.     \tag{5}
\]

This contradicts minimum order, with the six-site theorem as the terminal
case.  Therefore the one remaining conjecture-level statement is:

> **Clean-point theorem (`OPEN`).**  Every synchronized ternary packet of
> even order at least eight has an active zero of its selected clean error.

Everything below is an attack on this one theorem.  There is one exhaustive
dual route, from the rootless/all-inactive split, and a potentially shorter
constructive route through the synchronized one-bad/affine packet.  The latter
becomes a complete alternative only after a uniform source-entry theorem;
that entry is not currently proved.

## 3. Constructive subroute: interference straightening (Theorem A)

The exact scope starts **after** a synchronized maximum-anchor,
minimum-support one-bad packet has been obtained.  A general synchronized
source is not yet known to reselect into this normal form.  Accordingly,
Theorem A can presently close that packet and inform the global mechanism,
but it does not by itself cover the entire clean-point theorem.  A uniform
entry theorem would promote the following subroute to an independent global
proof.

### 3.1 Literal presentation

At fixed order, preserve the complete tensor (3).  Generate the presentation
by literal occurrences

```text
(coefficient word, endpoint ports, physical perfect matching, decorated tail).
```

Two occurrences have a certified exchange edge only when a physical `C4`
switch retains the same decorated complementary tail and supplies the
opposite determinant orientation.  A coefficient equation is an attaching
relation, not automatically an exchange edge or a filled higher cell.

This distinction is load-bearing: physical matching adjacency alone loses
the source typing needed for a finite support move.

### 3.2 Local trichotomy

For one endpoint star, fix the opposite star and its common `q` tail.  The
complete response-column map has the following linear alternatives:

1. an affine fibre meets a physical coordinate target line;
2. two complete columns are proportional;
3. a quotient `2x2`/Fitting minor is nonzero.

Alternative 1 supplies the desired concentrated endpoint coordinate.
Alternative 2 gives an exact one-sided kernel move and contradicts
minimum support.  Alternative 3 is not yet geometric: a source-labelled
pure/mixed companion with the same tail must turn the minor into a literal
determinant/cofactor carrier.

Status: the linear trichotomy and proportional-column move are `PROVED`.
The same-tail promotion is `PROVED` on typed `C4` packets and important fixed
port/private-row charts, but is `OPEN` uniformly.

### 3.3 First-separator reduction

Choose an occurrence outside the joined typed component at minimum flip
distance

\[
 \delta(M,N)=\sum_{C\subset M\triangle N}(|C|/2-1).       \tag{6}
\]

Whole-component switching proves that a minimum separator is a single even
alternating cycle.  A supported typed distance-three chord shortens it.  Thus
the first genuine defects are:

```text
delta=1: a physical C4 lacking its source-labelled opposite orientation;
delta=2: a chordless C6 whose first transgression has unmatched endpoint words.
```

Flat nonempty cycle geometry is already solved by vertex-gauge transport; a
connected, typed, source-exhaustive star is proportional and reducible.  The
missing issue is source connectivity/exhaustivity, not cycle geometry.

### 3.4 Earliest open incidence theorem

In the canonical `C6`, the first residual word is invisible to every selected
response port.  Unary exactness forces six anchor-contained cancellation
matchings, but their `q` tails alone are not Hall holes and do not define
endpoint columns.  The required statement is:

> **Spoke-to-hole synchronization (`OPEN`).**  Unary top plus all complete
> response rows either synchronize endpoint line sites into an ordered
> response hole with the required colours and a nonzero common cofactor, or
> produce a target-line joint-kernel move, a source unit, or a free carrier.

After such a column exists, **endpoint-word completeness modulo Hall** must
give a same-tail opposite orientation, an outside carrier, or a literal
star/triangle/`K2,2` Hall/Fitting attachment.  Separate translated-face line
sites do not prove this pairing.

There is now one exact base case.  In the minimal rational silent-`C6`
packet, after the bright pure tails are added, arbitrary endpoint mass on
all four core ports is impossible: a complete diagonal target coefficient
`aP-1` and a complete mixed zero coefficient `bP` share the same bilinear
endpoint polynomial.  Their source-row combination is a unit in all nine
bright charts.  Hence this first `C6` obstruction cannot survive by
core-port reselection alone.  A surviving packet must add internal
decorated `q` tails which contaminate the paired rows, or leave the core
envelope and enter an already named outside route.

There is also a complementary dense result at the earlier invisible word.
When all eight canonical `z=012111` matching monomials are nonzero, three
shifted response binomials plus the unary row have an odd-holonomy
certificate equal to twice a localized unit.  Thus the dense packet must
produce an external offdiagonal `q` mate or an actual extra endpoint-hole
column.  The remaining spoke-to-hole theorem is confined to support
degenerations; after a column is produced, its rank/support landing is still
the separate open step.

The support-degenerate word is now classified more precisely.  If the
optional `E13` pair survives, its common `q13:11` cell occurs in a literal
shifted response coefficient and supplies the typed chord.  If only `E14`
survives, its common `q14:11` cell is response-silent until the corresponding
physical hole-`14` endpoint product is nonzero.  This is the smallest exact
spoke-to-hole attachment gate; it replaces a vague search over all six
competitors.

Even that minimal `E14` enlargement is not a full survivor.  Across all nine
bright completions, its new term enters one target and one zero coefficient
with the same complete endpoint polynomial, so their combination is a source
unit.  A surviving support degeneration must therefore add a second
asymmetric internal tail (or leave through an outside endpoint).  The next
finite A-test is now a two-tail source-exhaustivity problem, not the bare
spoke-to-hole product.

### 3.5 Landing and termination

A typed carrier may still have deleted-star ranks `(2,2,3,3)`.  A second
uniform theorem must either produce a transverse, distinct-head four-good
pair or perform another anchor-safe support reduction.

The inner iteration needs a well-founded potential.  Current evidence points
to a lexicographic refinement of

```text
(unresolved affine fibres,
 endpoint support,
 typed components,
 minimum flip distance,
 source-typing debt,
 unresolved Hall/Fitting rank,
 deleted-star rank deficit).
```

Coordinate-line hits, kernel contractions, typed joins, and chord shortening
have proved local decreases.  A global decrease for Hall returns and rank
repairs is `OPEN`; it must not be inferred from finite chart closure.

If source entry, synchronization, landing, and this decrease theorem hold,
the inner iteration yields an active clean point and the outer descent (5)
finishes the proof.  Without source entry, the result closes the one-bad
subbranch but must still be consumed inside the exhaustive B/C architecture.

## 4. Exhaustive dual route: no active clean point (Theorems B/C)

Instead suppose the selected line has no active clean zero.  The exact
two-chart gcd split is:

1. the clean-error coordinates are rootless on a chart; or
2. roots exist, but every root is inactive.

There is no third case.

### 4.1 Rootless chart (Theorem B)

Rootlessness makes the residual Macaulay map surjective.  An abstract
functional is insufficient; it must have literal source provenance.  The
physical non-Euler jets, marked Hessian `h_v`, presentation syzygy `k_v`, and
derived filler

```text
d b_v = k_v,
d n_v = h_v Yw,
(tgt,ores)(n_v)=0,
chart(n_v)=-S_v
```

are `PROVED` in the indexed presentation.

The missing comparison must physically lift the adjacent repeated-site
pentagon differences and identify

```text
derived Yw -> physical W,
```

while preserving boundary, target, ordinary residue, and fine grade.  Once
this physical typing exists, correction indeterminacy is a useful dichotomy:

- a kernel class detected by anchor incidence normalizes to the required
  relative generator;
- otherwise the five polar columns are well defined in the physical cokernel,
  and the proved Fredholm alternative gives the terminal annihilator or the
  same relative-generator output.

The physically typed comparison is `OPEN`; the derived inputs and the linear
generator-or-annihilator alternative are `PROVED`.

The comparison must genuinely change source type.  Rootless pentagon
syzygies first occur in repeated-site degree `P3 disjoint-union K2`, while
the constructed chart and normal Hasse fillers are site-squarefree.  A
single-face collision has a private ordinary residue; only an adjacent
two-face S-pair cancels it, and that pair has physical anchor incidence zero.
Thus the first new cells are zero-anchor collision edges with the known
degree-five compatibility.  Chart `-S_v` is not physical anchor incidence;
the separate primitive anchor combination or dual annihilator is supplied
only after the physical polar map exists and Fredholm is applied.

The collision edge itself is now nearly explicit: the denominator/PP S-pair
has the correct repeated-site ridge boundary, but physical descent contributes
`delta_v*(H_0-u)*e_Eq`.  The exact first new source datum is a zero-anchor
reduced Eq face cancelling that term.  Its five cyclic defects already obey
the required degree-five compatibility.

### 4.2 All roots inactive (Theorem C)

The face-open derived candidate is `(kappa/h_v)n_v`.  On the dense
cyclotomic stratum of the simultaneous face-zero locus, the normal/Rees lift
is all-order after adding the complete normal Hasse face.  These are derived
chart statements, not physical cap columns.

The comparison from Theorem B must extend to this normal face and identify
the candidate with the physical inactive cap coordinate.  The nondense
face-zero locus is now finite: regular isolated-vertex `C4`, `K4-e`, and
generic `K4` inherit the derived normal repair; intersecting star/triangle
supports and one cyclotomic rank-four `K4` remain.  The horizontal
rootless/inactive comparison and diagonal inactive routing also remain
`OPEN`.  Once a physical cap exists, the Omega/Bezout and certificate-bracket
prolongations are `PROVED`.

If B/C close every rootless/inactive chart pairing, the assumption of no
active clean zero is contradictory.  The outer descent then applies.

## 5. Relation to support-skeleton extraction

It would be sufficient to select one nonzero monochromatic perfect matching
per colour whose union contains no further perfect matching.  That union,
with unit weights, is an unweighted witness with the same palette.  This is
the most transparent extremal interpretation of the conjecture.

The proposed proof does **not** assume that stronger extraction theorem.
Theorem A tries to realize it locally by deleting cancellation complexity,
but it may instead produce an active pair and descend in order.  Theorems B/C
are the dual fallback for cancellation homology that cannot be eliminated.
Thus the actual proof target is weaker and more robust:

```text
support straightening OR order descent OR a terminal contradiction.
```

## 6. Exact remaining load-bearing theorems

The proof closes if either the exhaustive B/C route is completed, or A is
completed together with uniform source entry.  The current load-bearing
theorems are:

1. uniform entry into the synchronized one-bad packet, if A is to be a
   standalone global route;
2. spoke-to-hole synchronization and endpoint-word completeness modulo Hall;
3. active carrier rank landing plus a well-founded inner decrease theorem;
4. one physically typed derived-to-physical comparison for Theorem B;
5. its compatible extension over inactive face-zero strata and the final
   horizontal/diagonal routing for Theorem C.

The first three complete the constructive route.  The last two complete the
exhaustive dual route.  Some overlap is expected: a terminal Hall/Fitting
class from A may be exactly the physical correction class evaluated by B/C.
Establishing that comparison would reduce the number of independent hard
theorems, but it must be proved rather than imposed as a unification
principle.
