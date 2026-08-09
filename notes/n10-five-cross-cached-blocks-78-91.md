# Exact sparse-matrix cache closure of pair blocks 78 through 91

## Outcome

Pair indices 77 through 90 close exactly.  The batch contains 834,960
supports; one same-vertex block contributes 2,352 prior zero- or two-grade
supports.  Exact affine reduction leaves 1,108 candidates, and 292 meet the
coefficient torus.

The sound sparse-matrix cache handles most of the literal frontier:

| route | cases |
|---|---:|
| exact cached matrix witness | 178 |
| fresh global monomial minor | 112 |
| fresh principal-divisor chart | 2 |
| literal survivors | 0 |

Thus the batch closes 832,608 new grade-3-to-6 supports.  The cumulative
fixed-old five-cross closure is 5,403,720, leaving 6,210,456 supports.

The cumulative exact matrix-cache hit count grows from 53 to 231.  No new
divisor factor or chart depth appears.

This is a fixed-old, fixed-cut N=10 theorem, not an all-order identity or a
Krenn counterexample.

## Cache library and literal frontier

Only previously torus-active blocks are needed to rebuild the cache.  The
21 active library blocks through pair index 48 contain 1,909 globally
monomial literal cases and produce 3,313 exact paired square/augmented
matrix keys after simultaneous \(S_5\) weight canonicalization.

The four torus-active target blocks have frontiers

\[
 67,\quad79,\quad67,\quad79,
\]

for 292 cases total.  Before any determinant is computed, their exact
sparse polynomial witness matrices are compared with the library.  The 178
hits transfer an actual nonzero square/augmented determinant pair, not just
its factorization.  Singular is invoked only on the 114 misses.

Of those misses, 112 produce global torus monomials.  The remaining two
have the already-known divisor \(bd+1\).  At an exact point of \(bd+1=0\),
each recomputed square and augmented pivot is nonzero on the entire localized
torus divisor.  Both supports close in one chart.

## Old-source-independence audit

Every one of the 1,909 cached witness matrices contains at least one nonzero
constant-term entry inherited from the fixed old-source column layer.  The
matrix key also retains those rational coefficients exactly.  Consequently
none of the present cache hits is certified as an incidence-only determinant
identity independent of the old source.

This is a necessary warning, not a proof that no uniform identity exists.
A genuinely old-source-independent theorem would need either:

1. a symbolic cancellation showing the determinant is unchanged under
   arbitrary admissible deformation of the old constant/linear layers; or
2. a quotient presentation eliminating those layers before the Segre
   square/augmented minor is formed.

The observed cross-block matrix equality is therefore structural reuse
inside the anchored source, not yet the missing arbitrary-source theorem.

No coefficient grid is used.

## Reproduction

Run

```text
python3 computations/verify_n10_five_cross_cached_blocks_78_91.py
python3 -O computations/verify_n10_five_cross_cached_blocks_78_91.py
```

All source, affine, and matrix arithmetic is exact over \(\mathbb Q\);
Singular handles torus saturation, fresh determinant factorization, and
localized divisor certification.
