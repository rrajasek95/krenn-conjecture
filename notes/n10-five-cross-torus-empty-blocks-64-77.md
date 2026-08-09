# Torus-empty closure of five-cross pair blocks 64 through 77

## Outcome

Pair indices 63 through 76 close before literal rank.  The 14 blocks contain
834,960 supports.  Four same-vertex blocks contribute 9,408 zero- or
two-grade supports already covered by earlier source-independent theorems.
Of the 825,552 new grade-3-to-6 supports, only 70 pass exact affine
reduction, and none meet the nonzero coefficient torus.

No determinant, matrix-cache lookup, or divisor chart is required.  The
cache-hit total therefore remains 53, and no new divisor complexity appears.

The cumulative fixed-old five-cross pair closure is 4,571,112 supports.
The remaining frontier contains 7,043,064 supports in 119 pair blocks.

This is a bounded fixed-old, fixed-cut N=10 theorem, not a Krenn
counterexample or an all-order identity.

## Batch structure

The batch finishes the family beginning with \((2,8;0,0)\), audits the full
family beginning with \((2,8;0,2)\), and starts the family beginning with
\((2,8;1,0)\).  Ten distinct-endpoint blocks have no affine candidate.
Three same-vertex blocks also have no affine candidate.  The fourth
same-vertex block has the only 70 affine candidates, with exact frontier

\[
                        70\longrightarrow0
\]

after torus saturation.

This is the second consecutive 14-block torus-empty batch.  Together they
close 1,653,456 new supports without a literal determinant.

## Exhaustion status

Seventy-seven of 196 pair blocks are complete; 119 remain, or nine more
14-block batches at the current scale.  The last 42 audited blocks closed
2,488,416 new supports, with only 174 literal cases.  Fifty-three of those
were exact sparse-matrix cache hits.

Finite N=10 exhaustion therefore remains a near-term, bounded computation.
This extrapolation can fail only in cost, not finiteness: later blocks may
produce denser torus frontiers or deeper divisor covers.  A full exhaustion
would still close only this N=10 fixed-old lane and would not replace the
needed uniform structural argument.

No coefficient grid is used.

## Reproduction

Run

```text
python3 computations/verify_n10_five_cross_torus_empty_blocks_64_77.py
python3 -O computations/verify_n10_five_cross_torus_empty_blocks_64_77.py
```

All affine arithmetic is exact over \(\mathbb Q\); Singular performs the
torus saturations.
