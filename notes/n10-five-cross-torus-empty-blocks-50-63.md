# Torus-empty closure of five-cross pair blocks 50 through 63

## Outcome

Pair indices 49 through 62 close before the literal-rank stage.  Across
834,960 supports, 7,056 same-vertex supports have zero or two permanent
grades and belong to the earlier source-independent theorems.  Exact affine
reduction excludes all but 70 of the remaining 827,904 supports, and none of
those 70 meet the nonzero coefficient torus.

Thus this batch requires no determinant, divisor chart, or matrix-cache
lookup.  It has no literal survivor.

The cumulative exact five-cross pair closure is 3,745,560 supports.  The
remaining frontier contains 7,868,616 supports in 133 pair blocks.

This is a bounded fixed-old, fixed-cut N=10 statement, not an all-order
theorem or Krenn counterexample.

## Exact census

The first three blocks finish the pair family beginning with
\((1,8;1,2)\).  Only the middle block has affine candidates: 70, all torus
empty.

The next three blocks are same-old-vertex pairs beginning with
\((2,8;0,0)\).  Each has 2,268 two-grade and 84 zero-grade supports.  Every
grade-4 or grade-6 support fails already in the exact affine system.

The final eight blocks have distinct old endpoints and no affine candidate.
The full batch frontier is therefore

\[
                 70\text{ affine}\longrightarrow0\text{ torus}.
\]

No coefficient grid is used.

## Exhaustion estimate

Sixty-three of the 196 pair blocks are now complete, leaving 133.  At the
current 14-block batching scale this is ten more batches.  The recent two
batches closed 1,662,864 supports; only 174 cases reached literal rank, and
the exact sparse-matrix cache handled 53 of those without new determinants.

This makes finite N=10 exhaustion a plausible near-term computation rather
than an open-ended search.  The estimate is not a theorem about future
complexity: later blocks may introduce more torus cases, new matrix keys, or
deeper divisor intersections.  Even a complete exhaustion would close only
this fixed-old five-cross lane, not supply the missing all-order structural
identity.

## Reproduction

Run

```text
python3 computations/verify_n10_five_cross_torus_empty_blocks_50_63.py
python3 -O computations/verify_n10_five_cross_torus_empty_blocks_50_63.py
```

All affine arithmetic is exact over \(\mathbb Q\), and Singular performs the
torus saturations.
