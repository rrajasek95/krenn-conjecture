# Exact-matrix transfer cache through pair block 49

## Outcome

The coarse 188 determinant-factor signatures do contain genuine transferable
certificates, but factor equality alone is not sound enough to replay a
witness.  A certified cache must identify the actual polynomial square and
augmented matrices under the same weight-variable map.

Using that stronger key, pair indices 35 through 48 close exactly.  They
contain 834,960 new grade-3-to-6 supports.  Exact affine reduction leaves
764 candidates and torus saturation leaves 174.  Of those 174 literal
cases:

| route | cases |
|---|---:|
| exact cached matrix witness | 53 |
| fresh global monomial minor | 98 |
| fresh divisor cover | 23 |
| literal survivors | 0 |

The 23 divisor supports close with 27 exact charts.  The cumulative
five-cross pair closure is therefore 2,917,656 supports, leaving 8,696,520
unaudited.

This remains a fixed-old, fixed-cut N=10 theorem.  It is not an all-order
identity or a Krenn counterexample.

## Sound cache key

The first 35 blocks contain 1,758 globally monomial literal exclusions.
Some supports have several usable augmented residual words, giving 3,014
stored matrix keys.  For every stored witness the checker reconstructs:

1. the deterministic evaluated-column rank at exact weights
   \((1,2,3,5,7)\);
2. the selected square pivot matrix as a sparse matrix of polynomials in
   \(a,b,c,d,e\); and
3. each augmented residual matrix whose determinant is a torus monomial.

The paired square/augmented matrices are minimized under all 120
simultaneous permutations of \(a,b,c,d,e\).  Coefficients, zero pattern,
row positions, and column positions are retained exactly.  Therefore a key
collision gives equality of the two polynomial matrices after an explicit
weight relabelling, so the stored nonzero determinant witness transfers.

This is deliberately stricter than the earlier factor signature.  It does
not infer transfer from equal determinant factorizations, and it does not
yet quotient by nontrivial row or column permutations or scalings.  Hence
its 53 hits are certified but not a maximal reuse count.

Divisor witnesses are also omitted from the automatic cache: equality of a
generic pivot does not by itself transfer the special pivot charts on its
rank-drop divisor.  Those cases are recomputed and certified directly.

## The next 14 blocks

Pair indices 35 through 41 have 210 affine candidates but none meet the
coefficient torus.  Pair indices 42 through 48 contribute the 174 torus
cases.  Before a cache lookup, each torus case is reduced only to its exact
sparse witness matrices; no determinant is computed.

Fifty-three matrices hit the audited cache.  The 121 misses are the only
cases for which Singular computes new literal determinants.  Ninety-eight
are global torus monomials.  The other 23 have divisor census

\[
 (bc+1):12,\qquad (bd+1):6,\qquad
 (bd+1)(bd-1):4,\qquad (be+1):1.
\]

For each irreducible divisor, an exact special pivot is recomputed and its
square and augmented determinant are proved nonzero on the localized torus
divisor.  The four two-component supports use two charts apiece, producing
27 charts total.

## Interpretation

The 53 hits show that the factor-signature collapse was not merely a
coincidence: source-distinct pair blocks can share the same literal
polynomial witness.  The stricter matrix cache also states the current
limit honestly.  It cannot reuse the remaining factor collisions without
an exact row/column/unit conjugacy, and it cannot reuse divisor cases until
their special charts are included in the keyed presentation.

The next structural improvement is therefore concrete: canonicalize the
full paired matrices under row and column permutations and rational unit
scalings, then extend each divisor cache entry by its complete chart cover.

No coefficient grid is used.

## Reproduction

Run

```text
python3 computations/verify_n10_five_cross_exact_matrix_transfer_cache.py
python3 -O computations/verify_n10_five_cross_exact_matrix_transfer_cache.py
```

All source and matrix arithmetic is exact over \(\mathbb Q\); Singular is
invoked only for fresh determinants and localized divisor certification.
