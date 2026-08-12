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

## 2. Proof sketch A: derived-fibre Cartan comparison

### Desired statement

Let `PP_src` be the complete multigraded principal-parts resolution of the
literal source equations in the repeated `P3+K2` grade.  Let `C_aug` be the
physical correction complex retaining source boundary, `D`, `W`, target,
ordinary residue, anchor incidence, and the eta/sigma terminal actions.

The required theorem is a physically typed relative comparison with the
following alternative:

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
5. Map this total cycle to the physical correction complex by the functorial
   tangent/cotangent comparison for the derived fibre.  The ridge component
   must map to `-d Omega_v`; this is where the eta and sigma terminal laws and
   the physical meanings of `W` and anchor incidence enter.
6. Apply the long exact sequence of the mapping cone.  A zero connecting
   class gives the comparison cell.  A nonzero connecting class is tested by
   the physical terminal, giving the alternative above.

Steps 1--4 are now established: positive Spencer degrees contract, the Hasse
coproduct totalizes with the correct signs, the source ideal is stable, the
order-six secondary transfer is exactly `-delta`, endpoint-even readouts are
protected, and the ridge commutes with the order-six construction.  The sole
unproved part is step 5: the functorial comparison must retain the *physical*
`W`, anchor, residue, eta, and sigma typings.  This is one map, not another
support census.

### What would count as a proof

It is enough to define the comparison on the generating source rows and show
that it commutes with Hasse coproduct and the endpoint/tail actions.  Algebra
multiplicativity then extends it to every polynomial multiple.  There is no
need to enumerate every order-six operator again.

## 3. Proof sketch B: one-sided transverse landing

Once the comparison produces a source-typed carrier, endpoint holonomy is
already controlled.  The remaining issue is not another residue identity;
it is whether the carrier supplies a missing physical head.

### Desired statement

At a maximum-anchor/minimum-support representative, let `u` range over the
at least two target-full internal sites supplied by the full-nine incidence
theorem.  Then a source-typed carrier has one of two outcomes:

1. in one overlap cap `P,u` or `S,u`, its projection to the other endpoint's
   one-dimensional deficient quotient is nonzero; or
2. the complete source columns yield a same-row dependence touching an
   occupied carrier cell.

The first outcome gives ranks `(3,3)` in that overlap, hence an active clean
pair.  The second outcome deletes an occupied cell while preserving every
source tensor and every old mutual anchor, contradicting minimum support.

### Augmenting-path proof sketch

1. Contract the selected anchor spans.  The target-full site `u` already has
   rank three, so only one deficient quotient line remains in each overlap.
2. Use occupied complete response columns as the ground set.  Permit an
   exchange edge only when it is certified by a literal common-tail source
   identity; physical matching adjacency alone is not an edge.
3. Starting from the comparison carrier, follow the directed exchange graph.
   Reaching a column visible in a deficient quotient finishes the rank
   landing.
4. If every reachable column is quotient-dark, matroid-intersection duality
   gives a tight reachable set and a common covector.
5. Lift the covector through the *complete* source rows.  If the corresponding
   columns are dependent, the exact same-row update deletes support.  If they
   are independent, source exhaustivity must expose another typed exchange,
   contradicting tightness.

Stars, triangles, `K2,2` webs, and reciprocal five-locks are the smallest
tight sets in this argument.  Their previous enumeration is evidence for
the matroid statement, not the intended proof of it.

### Exact remaining difficulty

Ordinary matroid intersection supplies the abstract tight set, but it does
not prove that its covector is represented by a literal same-tail source row.
The hard lemma is therefore **source-typed tight-set lifting**.  The full-nine
overlap reduction makes this one-sided; it no longer has to manufacture one
arm transverse to two deficient shores simultaneously.

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
- every stubborn finite chart has returned either a typing obstruction or a
  quotient-dark tight set, precisely the two proposed interfaces.

Evidence constraining it:

- a physical C4 is not automatically a typed exchange;
- a nonzero Fitting minor is not automatically transverse rank;
- a chart-odd presentation class is not a physical terminal class;
- vertex-gauge/Segre flatness does not kill relative homology; and
- a same-head carrier can remain dark in both physical quotient lines.

These guards do not argue for more enumeration.  They say exactly which
hypotheses the two structural theorems must retain.

## 6. Fastest proof programme

1. **Construct the physical comparison first.**  Define it functorially on
   the derived fibre and check it on generator families, with `W`, anchor,
   residue, eta, and sigma retained from the start.
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
