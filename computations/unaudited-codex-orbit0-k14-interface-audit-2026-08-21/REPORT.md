# Orbit-zero `K14 -> K16` anchor promotion

## Result

On the frozen orbit-zero anchors-one chart, let `a` be the twelve-anchor
product, `T=H0 H1 H2`, `I_mix` the literal mixed-word source ideal, and `K`
the nonanchor ideal.  The previously audited interface was

`a*T in I_mix + K^14`.

The present source-labelled replay promotes this exactly to

`a*T in I_mix + K^16`.

There are `3^4-3=78` nonconstant colour assignments on the four anchor
pairs.  Each corresponding literal mixed amplitude has one and only one
`K0` anchor monomial, no `K1` monomial, and twelve `K2` terms.  Among the
`485*1728=838080` exact relative factored `K14` occurrences, every occurrence
is divisible by at least one of these 78 singleton anchors.  Subtracting the
corresponding literal source multiple cancels that occurrence and creates
only terms of `K`-degree at least 16.  Thus this is filtered ideal
containment, not merely a support heuristic.

The pivot multiplicity is between 3 and 35 (mean `12.361111`).  Restricting
back to the three rows used in the original telescoping construction leaves
`582000` occurrences, so the full 78-row family is load-bearing.

## Bounded `K16` profile

For each of the 216 anchor multiplicity signatures at `K14`, the checker
chooses the literal singleton pivot that minimizes `K16` tails not divisible
by another one of the 78 `K0` anchors.  Under the factor stabilizer these 216
signatures form 33 orbits.

* 114 signatures admit a pivot whose twelve `K2` tails all reduce again.
* 96 signatures have best surviving-tail count 6.
* 6 signatures have best surviving-tail count 10.
* The resulting provisional `K16` anchor antichain has 240 signatures,
  `2467680` weighted occurrences, and 50 factor-stabilizer orbits.

The 50-orbit profile crosses the agreed 20-orbit expansion cap, so no orbit
fanout or Macaulay computation was launched.

This second-stage profile is only exact associated-graded divisibility for a
chosen single pivot per signature.  It is **not** a claim of `K16` ideal
membership: it does not yet collect coefficients, exploit linear
combinations of competing pivots, or transfer hidden initial forms from
lower filtration degrees.

## Exact finite cover obstruction

A second checker retains every one of the 78 available pivots and all twelve
literal `K2` terms before projecting only their nonanchor labels to anchor
multiplicity signatures.  Of the 33 `K14` stabilizer types, 19 have zero in
the exact rational affine hull of their projected tail columns.  The other
14 have an exact affine inconsistency.

Deletion-minimal rational inconsistency cores give 40 symmetry-orbit hitting
clauses.  Their exact minimum hitting set has size 25: cardinality bounds 0
through 24 are unsatisfiable and 25 is satisfiable.  Independently, choosing
only one literal pivot per type also has exact minimum global union 25 from a
57-orbit candidate universe.

Consequently no different choice or rational linear combination of the 78
singleton reductions can compress the `K16` anchor tail below 25
factor-stabilizer orbit types.  This conclusion is robust under restoring
the forgotten nonanchor labels: literal cancellation implies cancellation
after projection, so the projected 25-orbit lower bound is a necessary one.
It is an obstruction to iterating the singleton mechanism, not a claim that
the 25 projected orbit types constitute the collected `K16` polynomial.

## Scope and next target

The theorem applies to the orbit-zero anchors-one chart.  It does not cover
the other 30 charts and is not by itself a global `X5 -> cap` certificate.
It nevertheless strengthens the chart-local fallback and leaves only the
finite symmetry-aware `K16` source-incidence problem before any further
filtration promotion.

The finite cover/linear-incidence target is now terminal: it proves the
20-orbit cap cannot be met by singleton iteration.  Any continuation must
introduce genuinely new source columns (for example initial forms transferred
from lower filtration degree) or a representation-level compression of the
25 necessary anchor-tail orbits.  Expanding the 25 orbit types directly was
explicitly not attempted.

## Replay

The checker passed with identical logical digest under standard Python,
`python3 -O`, and `python3 -I -S`:

`9d5e7a8148220b16ff7306ad29a3635fd9cadd79204e02a7569d95e197886311`.

The finite K16 cover checker likewise passed all three modes with logical
digest

`a411a1c11d40b950e86556d63d82596db2f9fcfe21e7a67cbe39bae1d9208920`.
