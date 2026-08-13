# Structural proof sketches beyond case enumeration

## 1. Verdict on enumeration

The packet computations have been useful, but they should no longer be the
main proof method.  They have done three jobs:

1. found the correct local class (`-delta`) and its terminal signatures;
2. eliminated false implications such as physical C4 adjacency implying a
   typed source exchange, or a nonzero Fitting minor implying transverse
   rank; and
3. reduced the open proof to two interfaces which recur in every normalized
   packet.

Continuing to enumerate three, four, and higher extra-cell strata would
resolve successive matrices in a filtered complex without explaining why
the process terminates.  Enumeration should now be used only to falsify a
proposed structural lemma, verify a universal coordinate formula, or check
the smallest tight configuration.

The conjecture-level spine is

\[
 \text{minimum counterexample}
 \longrightarrow
 \text{maximum-anchor/minimum-support packet}
 \longrightarrow
 \text{physically typed comparison/carrier}
 \longrightarrow
 \text{active clean overlap}
 \longrightarrow
 (N-2)\text{-vertex descent}
 \longrightarrow
 \text{six-site contradiction}.
\]

Only the middle two arrows require new structural theorems.

The right division of labour is therefore:

```text
exact computation       discover/check local formulas and smallest guards
homological algebra     make source typing and correction indeterminacy exhaustive
matroid/rank theory     turn a typed local class into descent or support contraction
```

In particular, a fourth or fifth extra-cell census is not evidence for a
global induction unless it is the finite verification of a generator-level
identity used by one of the last two lines.

## 2. Proof sketch A: derived-fibre Cartan--covariance comparison

### Desired statement

Let `PP_src` be the complete multigraded principal-parts resolution of the
literal source equations in the repeated `P3+K2` grade.  Let `C_aug` be the
physical correction complex retaining source boundary, `D`, `W`, target,
ordinary residue, anchor incidence, and the eta/sigma terminal actions.

The required theorem is a physically typed relative comparison with the
following alternative.  It is important that it is a *comparison* theorem,
not a direct identification: the canonical order-six class and the five
marked non-Euler polars have different stabilizer characters.

> The endpoint-odd order-six class descends to a relative cell whose residue
> is `-delta`, whose protected readouts `D,W,target,anchor,pure-Eq` vanish,
> and whose ridge has the prescribed eta/sigma values; or the obstruction to
> that descent is a class in the physical relative homology.  If the physical
> terminal sees that class, it normalizes to the required relative generator.
> If the terminal kills it, the terminal descends and the augmented Fredholm
> alternative applies.

The point is that both solvability and genuine nonsolvability advance the
proof.  What is forbidden is using a chart-level or presentation-level
separator which has not descended to `C_aug`.

### Construction sketch

1. Regard the hafnian coefficient equations as an equivariant polynomial map
   `F`.  Resolve the derived fibre of `F` by its Koszul/principal-parts
   complex, keeping physical word and multidegree labels.
2. Use Hasse translation to totalize repeated derivatives.  The labelled
   Boolean coproduct supplies the alternating cobar signs and makes the
   complete source ideal stable under every face map.
3. Let the tail-colour `SL_2` Weyl action give one direction and endpoint
   transposition give the other.  On the endpoint-odd summand the Cartan
   prism

   \[
       K=(1-s)H_w,\qquad dK+Kd=(1-s)(w-1)
   \]

   kills the endpoint-even protected augmentations.
4. The secondary face of the totalized order-six class is the canonical
   four-corner packet `-delta`; the result is independent of a sparse choice
   of representative.
5. The unrecoloured order-six representative and the marked face polar have
   characters

   \[
      \gamma=(e_{x,0}-e_{x,1})
       +(e_{p,2}-e_{p,1})+(e_{q,2}-e_{q,1}),
   \]

   whereas the marked face polar has character

   \[
      \chi_v=\sum_{i\in F_v}(e_{i,0}-e_{i,m_i}).
   \]

   Their difference `beta_v=chi_v-gamma` is exactly a sum of seven local
   colour roots.  This gives the universal covariance prism and determines
   the degree of the comparison.  It does not yet identify that prism with
   the endpoint-recoloured physical face.
6. Construct the resulting site-colour contraction on the universal
   endpoint-recoloured operator symbols, then descend it through the complete
   labelled principal-parts/bar cone.  Read its repeated-grade endpoint as
   the physical marked non-Euler polar.  The commuting ridge must map to
   `-d Omega_v`; this is where the eta and sigma terminal laws and the
   physical meanings of `W` and anchor incidence enter.
7. Apply the long exact sequence of the resulting mapping cone.  A zero connecting
   class gives the comparison cell.  A nonzero connecting class is tested by
   the physical terminal, giving the alternative above.

Steps 1--5 are now established at the universal/symbolic level: positive Spencer degrees contract, the Hasse
coproduct totalizes with the correct signs, the source ideal is stable, the
order-six secondary transfer is exactly `-delta`, endpoint-even readouts are
protected, the ridge commutes with the order-six construction, the character
separation is exact, and the covariance-prism degree is forced and
target-zero.  The sole unproved part is step 6: this symbolic contraction
must glue to the *physical endpoint-recoloured* order-six totalization while retaining
`W`, anchor, residue, eta, and sigma.  The prism has one normalized `H_0`
class, so covariance alone cannot erase this endpoint.  This is one explicit
gluing map, not another support census.

There is now an additional exact guard on how step 6 must be formulated.  The
literal fourth-derivative output of the primitive order-six face has site
profile `(2,1,2,1,2,1,1,2)` and contains monomials outside every compatible
old full-row-times-two-edge correction column.  Thus the primitive symbol is
genuinely a *relative* face.  The comparison must be built in an exhaustive
principal-parts/bar cone (or detected by its dual); termwise identification
with one of the old 90-term columns is false.

The grading bridge is now isolated in two layers.  For the unrecoloured
primitive representative, no common monomial multiplier carries the face
into a first repeated component.  Its unique normalized symbolic bridge type
is

\[
 q_{13}^{00}q_{45}^{00}\partial_{07:11}
\]

followed by local colour transport at sites `0,2,6,7`; it lands in the
repeated component joining faces `3` and `5`.  The endpoint-recoloured
physical class has the same site profile and the corresponding normalized
stub-level bridge, with `192` decorated presentations, but its abstract
contracted edge `07:01` occurs in zero literal terms.  Therefore the physical
arrow is neither an edge derivative nor an old-column identity.  It must be
the site-colour contraction in the relative principal-parts cone.  The next
task is no longer to guess a grade or search for a matching: it is to define
that contraction on operator symbols and check its augmented readouts.

Cyclic transport reduces even that task at the symbolic incidence level.
The canonical bridge lands on face edge `(3,5)`; its residual-site orbit
gives all five edges of the face cycle, whose integral incidence image is the
saturated rank-four sum-zero lattice.  These are the boundaries the physical
comparison cells must realize, not already-constructed literal edge chains.
After the edge orbit, exactly one primitive face aggregate remains.
Constructing that one aggregate vertex, or evaluating its surviving class by
the physical terminal, is the complete local comparison problem.

At the universal level that aggregate is already exact.  The order-six face
and each non-Euler marked polar have the same normalized coefficient one, so
their difference has zero face `H0`; the Euler contraction then fills every
positive Spencer degree.  Hence there is no residual universal Hasse
calculation.  The sole obstruction lies in the relative homology of the map
from this universal contraction to the physically labelled augmented
complex.  This is exactly the setting in which boundary, terminal-visible
kernel, and descended-terminal/Fredholm are the three exhaustive outcomes.

The first exact physical descent calculation now reaches the boundary of
the old source module.  In the complete first-Spencer-flat order-six block,
the zero-normalized faces-`3/5` bridge is soluble over `Q`, but its exact
solution uses no repeated completion column.  Requiring nonzero pure-row
aggregate is exactly inconsistent, and the aggregate vanishes on the whole
homogeneous kernel.  Hence neither a different sparse representative nor
another polynomial full-nine correction supplies the primitive vertex.
The remaining step is specifically the relative comparison cell, or the
promotion of this aggregate factorization to the physical terminal
separator; it is no longer an unspecified endpoint-membership search.

The cokernel branch is also no longer abstract.  In each of the five
repeated components, six literal private matching coordinates factor the
pure aggregate integrally.  The resulting five six-term duals occupy the
five face grades and formally pair as `I_5`; all are invisible to the known
`eta`, left non-Euler, and extra full-Jacobian stabilizer fields.  The
canonical faces-`3/5` dual is proved against the exact order-six bridge
matrix.  They also survive the complete **absolute** source resolution.
The one-chart repeated maps are injective, so `d1*d2=0` forces every higher
absolute landing to vanish; the doubled-chart kernel consists only of
pairwise presentation differences, and the natural Tate kernel is
coefficient-sum-zero in every complete label fibre.  Hence no higher
absolute bar cell, polynomial correction, chart copy, or natural Tate
syzygy can kill the class.  Thus the remaining comparison theorem may be
attacked from either side: promote this homogeneous dual through the
*relative* augmented cone, or exhibit the first genuinely relative cell
that kills it and thereby supplies the comparison.

In the canonical faces-`3/5` block the dual is already physically typed.
The pure aggregate equals minus physical anchor incidence on every repeated
pure row, and both vanish on the endpoint-odd operator block.  Hence the
exact relation becomes

\[
  \Lambda=\sum_{i=1}^{6}m_i-\operatorname{ainc}.
\]

This covector kills the complete old/absolute block, all known stabilizers,
and the current relative `-delta` cell, while reading one on the desired
boundary-zero anchor.  Arbitrary new relative generators no longer require
an audit one by one.  On the complete protected map `J_0`, either `Lambda`
is nonzero on `ker J_0` and normalizes the relative anchor, or it kills the
kernel and factors as `Lambda=lambda J_0`, giving the complete physical left
separator.  The physical meaning of the canonical separator is no longer
missing; defining all rows in one common grade is.

The cyclic assembly is equally small.  Normalize the five facewise
covectors to value one.  Their sum kills the rank-four C5 incidence lattice
of covariance--Spencer edge comparisons.  It reads five on the sole
primitive aggregate direction.  Hence a physical aggregate cell gives the
relative generator after division by five, while its absence leaves the
summed physical separator.  The comparison frontier has therefore shrunk
to the relative aggregate family, not five separate facewise problems.

### What would count as a proof

It is enough to define the protected physical map on the generating source rows, identify
the all-derivation endpoint of each seven-cube, and show compatibility with
Hasse coproduct, endpoint transposition, and the ridge action.  Algebra
multiplicativity then extends it to every polynomial multiple.  There is no
need to enumerate every order-six operator or every cube vertex again.

## 3. Proof sketch B: one-sided transverse landing

Once the comparison produces a source-typed carrier, endpoint holonomy is
already controlled.  The remaining issue is not another residue identity;
it is whether the carrier supplies a missing physical head.

### Desired statement

At a maximum-anchor/minimum-support representative, let `u` range over the
at least two target-full internal sites supplied by the `h=3` unary target
together with the two bright full-nine four-covers.  Then a source-typed
carrier has one of two outcomes:

1. in one overlap cap `P,u` or `S,u`, its projection to the other endpoint's
   one-dimensional deficient quotient is nonzero; or
2. the complete source columns yield a same-row dependence touching an
   occupied carrier cell.

The first outcome gives ranks `(3,3)` in that overlap, hence an active clean
pair.  The second outcome deletes an occupied cell while preserving every
source tensor and every old mutual anchor, contradicting minimum support.

### Equivariant augmenting-path proof sketch

1. On the six residual sites, `q^[3]=X_0` makes colour zero full and
   full-nine incidence makes each bright colour full at at least four sites.
   Their intersection supplies at least two target-full internal sites.
   Choose one, call it `u`, and pass to an overlap cap having `u` as one
   endpoint.  Contract the selected anchor spans.  Since `u` already has
   rank three, only the other endpoint's one-dimensional deficient quotient
   remains.
2. The selected-anchor synchronization theorem removes the former site and
   colour guess.  Either a target-full site lies outside the two selected
   bright neighbours and its overlap is already rank `(3,3)`, or the two
   full sites are precisely those neighbours.  In the latter case the
   deleted selected bright arm is the missing quotient axis and its matching
   supplies a disjoint selected cofactor.  Relabelling gives the primitive
   `07:11 wedge 24:11` face.
3. Use occupied complete response columns as the ground set.  Permit an
   exchange edge only when it is certified by a literal common-tail source
   identity; physical matching adjacency alone is not an edge.
4. Starting from the physically active primitive face, follow the directed
   exchange graph.  Reaching a column visible in a deficient quotient
   finishes the rank landing.  A Hasse derivative direction without a
   physical active carrier is not a starting vertex.
5. If the visible-colour cofactors vanish, or every reachable column is
   quotient-dark, matroid-intersection duality
   gives a tight reachable set and a common covector.
6. Lift the covector through the *complete* source rows.  If the corresponding
   columns are dependent, the exact same-row update deletes support.  If they
   are independent, source exhaustivity must expose another typed exchange,
   contradicting tightness.

Stars, triangles, `K2,2` webs, and reciprocal five-locks are the smallest
tight sets in this argument.  Their previous enumeration is evidence for
the matroid statement, not the intended proof of it.

### Exact remaining difficulty

Ordinary matroid intersection supplies the abstract tight set, but it does
not prove that its covector is represented by a literal same-tail source row.
Nor does abstract colour symmetry prove that the visible arm retains a
nonzero physical cofactor.  The hard lemma is therefore **source-typed
tight-set/orbit lifting**: the full site-colour orbit of primitive faces must
either contain a nonzero quotient-visible cofactor or lift the resulting
dark orbit to a complete-row dependence.  The full-nine overlap reduction
makes this one-sided; it no longer has to manufacture one arm transverse to
two deficient shores simultaneously.

## 4. Assembly

Assume the two statements above.

1. Choose a minimum counterexample, then maximize mutual anchors and minimize
   occupied scalar support.
2. The existing curvature-line and packet reductions select the local cap.
3. Apply the derived-fibre Cartan comparison.  A terminal-visible obstruction
   is already the required relative generator; otherwise obtain the physical
   `-delta` carrier and a well-defined terminal/Fredholm map.
4. Apply one-sided transverse landing.  The dependence branch contradicts
   minimum support, so an active clean overlap exists.
5. Apply the proved exact clean-pair descent and remove two vertices.
6. Repeat the same lexicographic choice.  The process reaches the already
   proved six-site contradiction.

The same physical comparison also supplies the five rootless columns used
by the downstream Fredholm argument.  The inactive horizontal comparison is
then a compatibility problem, not a separate reconstruction of the local
class.

## 5. Evidence for and against this architecture

Evidence for it:

- the universal Spencer and Hasse layers are now structurally acyclic;
- the secondary transfer is canonical and equals the required residue;
- endpoint oddness removes five formerly separate readout conditions;
- same-row dependence gives an exact anchor-safe deletion;
- full-nine incidence reduces double-transverse rank restoration to a
  one-sided quotient test; and
- the order-six/polar weight mismatch is exactly seven local covariance
  roots, so the missing comparison has five explicit target-zero prisms
  rather than an unspecified correction; and
- every stubborn finite chart has returned either a typing obstruction or a
  quotient-dark tight set, precisely the two proposed interfaces.

Evidence constraining it:

- a physical C4 is not automatically a typed exchange;
- a nonzero Fitting minor is not automatically transverse rank;
- a chart-odd presentation class is not a physical terminal class;
- vertex-gauge/Segre flatness does not kill relative homology; and
- a same-head carrier can remain dark in both physical quotient lines.
- covariance transport has a surviving `H_0` endpoint and therefore cannot,
  by itself, identify the order-six and polar classes.

These guards do not argue for more enumeration.  They say exactly which
hypotheses the two structural theorems must retain.

## 6. Fastest proof programme

1. **Construct one principal-parts site-colour contraction first.**  Define
   it on the endpoint-recoloured order-six operator symbols in the normalized
   faces-`3/5` degree.  Prove its boundary formula and retain `W`, anchor,
   residue, eta, and sigma from the start.  Cyclic incidence then propagates
   it to the other four faces and leaves only one aggregate class.
2. **Prove source-typed tight-set lifting.**  Work in one overlap with a
   target-full site; use the complete-row matroid, not physical matching
   supports.
3. **Assemble immediately.**  Do not wait for a classification of every
   Hall web or every higher support tier.
4. Use computation only to test the smallest candidate counterexample to
   either theorem and to verify the generator-level comparison formulas.

This programme turns the remaining work from an open-ended family of cases
into two theorem-sized obligations.  The first is homological and
source-typing-sensitive; the second is matroidal and rank-sensitive.

## 7. Three proof sketches at increasing strength

The following versions should be kept separate while the argument is being
completed.

### Minimal local theorem

In the fixed repeated grade, form the complete relative source complex and
the difference between the all-derivation covariance endpoint and the
order-six face.  Either that difference is a boundary, or a physical dual
cocycle detects it.  This proves only the local carrier/separator/generator
alternative.  It is the first theorem to establish.

### Descent theorem

Assume the boundary branch produces the primitive endpoint-arm/cofactor
family.  Across the full site-colour orbit, either one arm is visible at one
of the two target-full overlap sites, or the dark reachable set yields a
complete-row dependence touching occupied support.  The two outcomes give,
respectively, a clean `(3,3)` overlap or an anchor-safe support deletion.

### Conjecture theorem

Choose a minimum-order counterexample and then a maximum-anchor,
minimum-support representative.  Apply the local theorem.  A physical dual
or terminal-visible kernel is already the rootless relative exit.  Otherwise
apply the descent theorem; the deletion branch contradicts minimal support,
and the visible branch invokes exact clean-pair descent.  Re-minimize and
iterate until the proved six-site contradiction.

This layering matters.  The local theorem does not need to classify every
Hall web, and the descent theorem does not need to reconstruct the derived
comparison.  Their only shared datum is the physically typed primitive
carrier and its complete-row orbit.
