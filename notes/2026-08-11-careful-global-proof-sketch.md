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

The entire first one-cell two-tail layer is now exhausted as well.  Across
the `1,020` possible chart/cell extensions, complete response rows first
reduce the apparent defects, and complete unary rows then make every one of
them an ordinary source unit.  Thus no first extra internal cell—diagonal or
offdiagonal—survives as a new `C6` topology.  The earliest local survivor
must contain at least two simultaneously new internal cells which
cross-contaminate the paired unary/response collisions, or an outside-core
endpoint component.  This does not settle arbitrary multisite components,
active-rank landing, or termination.

The complete two-cell layer is empty too.  All `57,291` unordered pairs of
new internal cells retain a literal two-row unit: `51,615` in the base
`G11` comparison, `2,850` in an alternate `G11` word, `2,818` in the unary
row, and the final eight `K4,2` records in `G22`.  Therefore the earliest
same-chart local survivor requires at least three simultaneous new internal
cells.  This is strong evidence for a module-level exhaustivity theorem, but
does not replace global multisite connectivity or rank/termination.

The three-cell top degree is now empty too.  All `2,126,208` simultaneous
three-new-internal-cell specializations are literal source units
(`c13911e`).  Because the physical equations are multiaffine cubic, this
exhausts the local monomial types.  It does not by itself prove the
arbitrary-support statement: the witnessing zero row varies with the
triple, and the universal target has `24/26` private degree-one/two
monomials.  What remains is a triangular/Rees or standard-basis gluing
lemma, not a four-cell census.

The first gluing syzygy is explicit.  Response-row leading terms form
endpoint-orientation two-cycles in every chart.  Unary rows break all `228`
cycles, but the honest multiplied S-pairs introduce nonprivate tails of
degree three (`24` cases) or four (`204` cases); `G22` lies in a different
endpoint grade (`6e5878e`).  The next finite proof object is precisely the
reduction of these unary-times-q Buchberger tails.

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

This source type is sufficient at every normal order needed below.  A single
polynomial collision/reduced-Eq family prolongs functorially through orders
one, two, and three without new multidegrees or readout defects.  Its cyclic
edge matrix still has rank four in each grade, so one separate polynomial
primitive-anchor family is necessary and sufficient to fill the aggregate
cokernel.  The remaining `Yw -> W` identification is independent.  Thus the
full B/C comparison needs exactly these two physical generator families plus
the terminal readout map, not a new family for each singular normal stratum.

On the selected nonzero `C5` torus there is a further simplification.  A
target-preserving degree-two etale site-colour gauge normalizes all five
cycle cells to one, fixes the marked colour-zero cells and non-Euler jets,
preserves every augmented readout, and descends under its deck involution.
It kills the five selected pure-Eq defects.  Hence the exact `C5`
specialization already has clean physical collision edges.  On the general
selected-cycle chart the only remaining edge boundary is the off-cycle tail
difference `R_v-R_w`.  These tails are not yet Theorem A objects: no common
endpoint-star column or identical decorated complement tail has been
supplied.  A source-labelled tail-to-endpoint attachment theorem is required
before the A connectivity mechanism can replace the B comparison.

The tail attachment itself is now exact once a forced response hole is
active.  With off-cycle chords `A,...,E`, the five residuals are

```text
R1=CE+D, R2=A+BE, R3=BD+C, R4=E+AD, R5=AC+B.
```

All ten monomials are distinct.  The complete six-term response coefficient
of any active forced hole routes exhaustively to a source unit, a same-tail
proportional deletion/Fitting carrier, or a different-tail `C4` off-anchor
or Hall/lock case.  The sharp preceding obstruction is that internal `C5`
data do not force the endpoint product at that hole to be nonzero.  Thus #2
has reduced to the same response-hole accessibility/affine line-hitting
lemma as Theorem A; rank landing remains downstream.

The alleged response-dark subcase is now gone.  A nonzero `R_v-R_w`
contains an off-cycle chord whose complete physical column is zero and
minimum-support deletable, or nonzero and source-forces a unary/response
carrier (`d5b8ebc`).  Hence the general residual-tail branch has already
reached the common affine/Fitting/Hall rank-landing gate.

On the exact normalized `R_v=0` specialization, path #1 is sharper than a
missing-column formulation suggests.  The clean collision lattice is
saturated rank four, so one physical augmented base column carrying derived
`Yw` to physical `W` would propagate to the other four faces and make
Fredholm available.  But the marked unary row cannot construct it: after
the direct-zero normalization its mates remain in five reset-word
components (`467d545`, `f3e4b01`).  Nor can a positive aggregate Tor class
construct it.  The literal clean denominator identity forces every such
image to have coordinate sum zero (`ba52560`).

Consequently the clean branch is now a dual problem.  Cyclic gluing reduces
the first endpoint/Bianchi cokernel from five face classes to one primitive
aggregate class.  An explicit candidate separator reads one on the endpoint
ridge, q-companion, and rootless ridge classes and zero on Eq, W, target,
residue, and anchor incidence (`a4c687c`).  The full physical-kernel audit
shows that this coarse covector does not descend: five target stabilizers
pair with it as `-5-u_z/t`, and they kill the entire nonzero covector space
on the old endpoint/companion/rootless inventory (`586f885`, `d7ff17d`).
The formally unique scalar correction on those five directions is itself
detected by two other physical stabilizers and is not source-typed
(`a9f64aa`).

The remaining theorem must therefore construct genuinely new physical
comparison data in repeated-site `P3 disjoint-union K2` degree: a
source-valid `Omega_v <-> r_v` map whose stabilizer variation supplies
`5+u_z/t`, together with derived `Yw -> W` and the reduced-Eq correction.
If its indeterminacy has nonzero anchor readout, `0373033` turns that failure
directly into the required relative generator; otherwise the comparison
defines the polar map and Fredholm finishes the rank alternative.

The smallest source type is now explicit.  It is a same-labelled-companion
lift `(-r_v,+Q_(v,N);ores=1)` in repeated `P3 disjoint-union K2` degree;
subtracting the endpoint bar gives exactly `-t_v Omega_v+r_v`.  No existing
source family contains it (`947ce8e`, `3e64181`).  Cyclic homogenization
first occurs in degree `abcde`, but its aggregate has lower boundary
`5abcde`, so ordinary matching, Pluecker, and incidence cells cannot fill
it.  The positive object is a relative augmentation `U` with
`d_0U=abcde`, after which the corrected package `A-5U` is a cycle
(`252bdc8`).  This is a single named cell, not an indefinite higher-order
search.

Nor is `U` hidden in the existing top degree: `abcde` occurs only as a pure
unary multiplier with anchor `-1` and target `+1`.  A primitive augmented
functional separates it from the target/anchor-zero `U`, and the complete
top source map is injective (`6c76d22`).

This does not add a third independent theorem.  The old target/cap rows
already form `x=(1,-1,0,0,0)`.  If anchor incidence is nonzero on the
kernel preserving lower boundary, W, target, and residue, that kernel
element is the primitive relative generator.  If a physical cyclic
comparison `A=(5,0,0,0,0)` is built, then `A-5x` is exactly such an element
(`c094bbb`).  Hence the construction-or-generator dichotomy absorbs `U`;
the single real construction remains `A`, equivalently the physical
`Omega <-> r` comparison.

The universal typed quotient confirms that no polynomial bookkeeping can
skip the accessibility step.  Before localization, the five cyclic tail
differences span a four-dimensional quotient: every complete unary or
response occurrence has positive endpoint-use grade and projects to zero in
the bare-tail summand.  The exact missing inventory is ten unary spokes and
forty response brackets (eighty orientations).  On path #1, the nearest
existing base column `r_0-T` already has the correct `W`, anchor, target, and
residue but is separated from the desired column by two primitive defects:
one reduced pure-Eq face and one ridge vertex.  No audited cap/PP/normal
column supplies them.  Hence the remaining physical theorem must construct
these attachments on the residual-tail branch, while the exact clean branch
must promote its forced aggregate separator rather than merely combine
existing coarse rows.

### 4.2 All roots inactive (Theorem C)

The face-open derived candidate is `(kappa/h_v)n_v`.  On the dense
cyclotomic stratum of the simultaneous face-zero locus, the normal/Rees lift
is all-order after adding the complete normal Hasse face.  These are derived
chart statements, not physical cap columns.

The comparison from Theorem B must extend to this normal face and identify
the candidate with the physical inactive cap coordinate.  The nondense
face-zero locus is now finite: regular isolated-vertex `C4`, `K4-e`, and
generic `K4` inherit the derived normal repair.  Every singular first-order
stratum also has a literal weighted-normal escape by order at most three:
the cyclotomic rank-four `K4` missing covector is hit at order two, while the
intersecting supports have explicit degree profiles using only orders two
and three beyond their first-normal span.  Hence there is no remaining
set-theoretic singular-support separator.  What remains is chain-level:
the complete derived second-normal companions (and the third-normal
triangular companions for the one-edge/three-star strata) now exist, have
zero target/old residue, and assemble rank-five boundary systems on every
stratum.  Their first failure is exactly the same physical comparison as in
Theorem B: the normal-indexed mixed row has no homogeneous site-squarefree
physical image.  Thus only the site-collision/primitive-anchor cells and the
physical `Yw -> W` comparison remain.  The horizontal
rootless/inactive comparison and diagonal inactive routing remain `OPEN`.
Once a physical cap exists, the Omega/Bezout and certificate-bracket
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
