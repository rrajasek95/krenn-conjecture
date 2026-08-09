# Exact sparse-matrix closure of pair blocks 106 through 119

## Outcome

Pair indices 105 through 118 close exactly.  The batch contains 834,960
supports; the same-vertex block at pair index 115 contributes 2,352 prior
zero- or two-grade supports.  Thus 832,608 grade-3-to-6 supports are new.

Ten pair blocks are affine-empty.  The remaining three active blocks reduce
to 1,431 affine candidates and 659 coefficient-torus candidates.  Their
source-faithful closure is:

| route | cases |
|---|---:|
| exact cached sparse-matrix witness | 281 |
| fresh global monomial minor | 361 |
| fresh principal-divisor support | 17 |
| divisor charts | 20 |
| literal survivors | 0 |

The cumulative fixed-old five-cross closure is 7,068,936 supports, leaving
4,545,240 grade-3-to-6 supports in the 196-block frontier.  The cumulative
exact matrix-cache hit count grows from 231 to 512.

This is a fixed-old, fixed-cut N=10 theorem.  It is not a Krenn
counterexample or an arbitrary-old-source theorem.

## Sound matrix transfer

The cache library now uses the 21 earlier active blocks together with pair
indices 77, 79, 87, and 89.  After their exceptional divisor supports are
removed, the library contains 2,199 globally monomial cases and 3,676 exact
paired square/augmented matrix keys modulo simultaneous permutation of the
five cross weights.

Every one of the 659 target matrices is compared with this exact sparse
polynomial library.  The 281 hits transfer an actual square/augmented
determinant pair; factor signatures alone are not used.  Literal determinant
factorization is invoked only on the 378 misses.

Of those misses, 361 have a global torus-monomial square and augmented minor.
The remaining 17 supports have principal factors drawn from

```text
ac+1, ad+1, ad-1, ae+1, ace-d, bd+1,
c+d, c-d, d+e, d-e
```

Three generic bases have two components, so the 17 supports require 20
irreducible divisor charts.  On each component an exact nonzero torus point
is chosen, the literal matrix is rebuilt, and Singular verifies that the new
square and an augmented determinant have no zero anywhere on that localized
torus divisor.  All 20 components close in one layer.

No coefficient grid is used.

## Relation to the old-source dependence audit

The batch closure remains fixed-old.  Independently, the accompanying
constant-row dependence audit shows that the 62 positive-degree quotient
witnesses from the cache library are unchanged on every admissible anchored
one-cell old-source exactness chart.  That is evidence for a boundary-
incidence Fitting identity, but it does not transfer the present 659 target
certificates to arbitrary old sources.

## Reproduction

```text
python3 computations/verify_n10_five_cross_cached_blocks_106_119.py
python3 -O computations/verify_n10_five_cross_cached_blocks_106_119.py
```

All affine, matrix, determinant, and localized-divisor arithmetic is exact
over \(\mathbb Q\).
