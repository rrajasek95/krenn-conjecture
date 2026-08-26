# K24 weighted-top-ledger logical sufficiency referee

## Verdict

**No: complete weighted response-column top ledgers alone do not certify the
load-bearing terminal/filtered membership claim.**  They do certify the
narrow, tautological statement that the row vector they define is in the span
of the raw K24 projections, provided exact equality with the frozen `R24` is
also checked.  That is not yet a lower-preserving lift.

Let `B` be the full filtered source map, `L=P_<24 B`, and `T=P_24 B`.  After
ascending reduction has fixed K19--K23, an admissible terminal adjustment
`delta_x` must satisfy `L(delta_x)=0`.  The load-bearing terminal operator is
therefore

```text
A24_rel = T restricted to ker(L)
```

(or the equivalent induced map in the reducer's explicitly certified relative
quotient), not `T` on every raw literal `(w,U)` column.

The response columns in the proposed ledgers are the same full columns used
earlier to cancel K20 parents.  Their coefficients generally satisfy
`L(x20)=-R20`, while their stored 60-tail fans are `T(x20)`.  Reusing `x20` to
subtract its top contribution restores the K20/lower component.  Thus exact
coverage of all 35 paths proves complete accounting of the generated top
contribution; it does not prove `x20` lies in the relative lower kernel.

A one-column counterexample makes the distinction exact.  Take
`L=[1]`, `T=[1]`, and `R24=[1]`.  Then `R24` lies in the raw top image, but
`ker(L)={0}`, so it does not lie in the relative image.  The full column is
`e_low+e_top`: subtracting it cancels the top and creates a lower term.

## Reconciliation of the three existing claims

The terminal-structure statement is correct if its `A24` denotes the induced
relative/associated-graded map.  Its literal description as all raw
`top(w,U)` projections omits the kernel/lift guard.  The filtered reducer makes
that guard unavoidable: it collects and fixes buckets in ascending degree,
and a later correction may not alter an earlier bucket.

The factorized schema's `constructive_span_certificate` is conditionally
correct for the vector defined by its weighted raw ledger.  It becomes a
certificate for the frozen terminal residual only after two independent exact
equalities are proved:

```text
T(x) = R24                 exact H-row-orbit mass equality
L(x) = 0                   exact lower balance
```

An exact compatible lower-correction ledger may replace the second equation.
When both hold, the coefficient vector is already constructive and no Gram
solve is needed.

When no such vector is available, a complete target-rooted Gram closure can
decide membership only if it is built from the **relative columns** of
`A24_rel`.  Gram closure on raw tops proves only raw projected-span membership
and cannot manufacture the missing lower lift.  A capped closure remains
inconclusive, and rank equality must still be paired with the exact norm check.

## Natural-order versus `repr`-order correction

The optimized producer canonically orders `(word tuple, multiplier bytes)` in
natural lexicographic order.  The provider's cached orbit is sorted by textual
`repr`.  They are the same 384-action orbit, but their chosen representatives
differ on 228 of 257 distributed columns.  This does not change an orbit-sum
vector; it does invalidate cross-ledger string equality, deduplication, or mass
collection unless both sides are normalized first.

Any K24 assembler must pin the H action and transform hashes and a
`canonical_order_id`, verify orbit membership and orbit size, recompute the
natural minimum, and merge only normalized keys.  Treating provider
`column_orbit(C)[0]` as the natural minimum is a hostile mutation.  This order
correction prevents false splits or matches; it does not supply the missing
lower-kernel certificate.

## Fail-closed guard

A constructive terminal PASS requires all 35 paths with no gap, duplicate, or
extra; the same frozen reducer and all-dividing-pivots convention;
multiplier-aware `(w,U)` columns; exact orbit divisions; natural-order
normalization; a frozen `R24` hash; exact `T(x)=R24`; and exact lower balance or
a compatible correction certificate.  Without those guards, the status is
`REJECT_K24_CONSTRUCTIVE_SPAN_CERTIFICATE` and no K24 membership claim follows.

This is a read-only theorem/referee.  It launches no K24 production or charge
run.
