# Certificate-signature collapse across the first 35 pair blocks

## Outcome

The distinct source-faithful leaf maps do not force distinct literal
certificates.  Across pair indices 0 through 34, the exact block audits have
2,004 torus-affine candidates.  Their evaluated-column witnesses collapse to
188 canonical certificate signatures:

| certificate kind | cases | canonical signatures |
|---|---:|---:|
| global monomial | 1,758 | 122 |
| divisor cover | 246 | 66 |
| total | 2,004 | 188 |

Seventy-six signatures occur in at least two different pair blocks.  Those
cross-block signatures cover 1,649 of the 2,004 cases.  Thus 82 percent of
the audited literal frontier already uses certificate types shared between
source-distinct blocks.

This is positive evidence for a reusable determinant identity.  It is not
yet a matrix-conjugacy theorem and does not transfer the unaudited blocks.

## Canonical equivalence

For each torus case the checker retains:

1. the evaluated coefficient-column rank;
2. the number of residual words outside that sampled span;
3. the complete factorizations of one square pivot and one augmented
   residual minor;
4. for a divisor case, the irreducible generic divisor support and whether
   the existing cover has depth one or two.

It forgets pivot-row names, augmented-word names, nonzero rational factors,
and determinant sign.  It then minimizes the paired square/augmented
factorization under all 120 simultaneous permutations of the five weights
\(a,b,c,d,e\).  The same weight permutation acts on both determinants;
they are not normalized independently.

The 2,004 cases have only nine coarse rank/bad-row signatures even before
factor data are considered.  Adding full factorization data gives the 188
signatures above.  The divisor total includes the single depth-two cover
from pair block 20, so that exceptional geometry is not conflated with a
principal one-layer chart.

## Interpretation and stopping rule

The collapse is strictly coarser than equality of polynomial matrices.
Two minors can have the same factorization after weight relabeling even if
their ambient column matroids or their remaining minors differ.  Therefore
the 76 cross-block collisions are candidates for a common Fitting-ideal
template, not proof that the underlying coefficient cylinders are
conjugate.

They nevertheless sharpen the structural route.  Full leaf fingerprints
give 196 distinct types, while the literal witnesses seen so far use 188
factor types across 2,004 cases, and most cases lie in types shared between
blocks.  The next admissible structural test is to take the dominant shared
signatures and compare the complete polynomial matrix presentations—or a
generating set of maximal and augmented Fitting minors—under simultaneous
row, column, and weight permutations.  A successful conjugacy there would
turn many blockwise exclusions into one identity.  A mismatch in their
full Fitting ideals would certify that determinant factor coincidence alone
is too coarse.

No coefficient grid is used.

## Reproduction

Run

```text
python3 computations/verify_n10_five_cross_certificate_signature_collapse.py
python3 -O computations/verify_n10_five_cross_certificate_signature_collapse.py
```

The checker reconstructs all first-35-block affine/torus audits over
\(\mathbb Q\), factors determinants with Singular, and canonicalizes the
exact factors with SymPy.
