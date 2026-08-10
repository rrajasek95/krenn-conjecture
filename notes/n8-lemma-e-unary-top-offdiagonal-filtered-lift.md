# The diagonal unary-top identity lifts through off-diagonal order three

## Outcome

The concentrated one-bad identity in
[`n8-lemma-e-unary-top-diagonal-aggregate-identity.md`](n8-lemma-e-unary-top-diagonal-aggregate-identity.md)
is not obstructed by the first off-diagonal internal cells.  Retain all 135
entries `q_uv^ab` of the internal quadratic and filter the fine multidegree
of

\[
 F_{01}(1111)F_{23}(2222)H(000000)                         \tag{1}
\]

by the number of cells with `a != b`.  The complete source-labelled
Macaulay maps from the normalized packet's zero coefficient rows are onto
over `QQ` through filtration order three.

There is no order-one piece.  At the first possible off-diagonal order,

```text
orders 0+2: 3,228 monomials, 10,314 source multiples, rank 3,228;
orders 0+2+3: 11,118 monomials, 31,182 source multiples, rank 11,118.
```

Consequently (1) lies in the zero-row ideal modulo terms containing at least
four off-diagonal-colour cells.  This is a genuine characteristic-zero
existence statement with literal coefficient-row provenance.  It is **not**
full ideal membership: the fine degree of (1) is seven, so orders four
through seven remain.  In particular, the fact that a six-site hafnian has
degree three does not by itself terminate the multipliers in an ideal
identity.

## Complete fine-degree module

The colour tokens of (1) are

```text
site 0: {0,2}       site 1: {0,2}
site 2: {0,1}       site 3: {0,1}
site 4: {0,1,2}     site 5: {0,1,2}.
```

A basis monomial is therefore a perfect matching of these fourteen labelled
site-colour tokens, with tokens at the same physical site forbidden to pair.
The full basis has 61,128 monomials.  Its filtration census begins

```text
off-diagonal cells 0:   135
off-diagonal cells 1:     0
off-diagonal cells 2: 3,093
off-diagonal cells 3: 7,890.
```

The absence of order one is forced by colour parity.  At order three the
three cross-colour counts must have the unique signature

\[
                 (x_{01},x_{02},x_{12})=(1,1,1).       \tag{2}
\]

Indeed each colour has an even number of tokens, so each cross-colour degree
is even.  With three cross-colour cells, all three pair types must occur
once.  Thus the reported zero cokernel at order three includes the entire
cycle type (2); it is not a selected-channel census.

The 285 compatible zero rows are exactly

* 143 mixed coefficients of the full six-site top row;
* 35 non-target coefficients of each direct cofactor `F01,F23`;
* all 36 compatible coefficients of each cross cofactor `F03,F12`.

For every row, the checker enumerates every complementary token matching.
Multiplying the coefficient row by that matching gives a literal polynomial
multiple in the original 135-cell ring.  Projection to orders at most `k`
gives the filtered column.  No abstract row, chosen supported term, or cell
division is used.

## Why the modular computation proves a theorem over `QQ`

All entries of these matrices are integers.  Deterministic sparse column
elimination modulo the prime `1,000,003` produces a pivot in every row.  The
recorded pivot columns therefore select a square minor whose determinant is
nonzero modulo that prime.  The same integer determinant is nonzero, so each
matrix has full row rank over `QQ`.  This proves surjectivity over `QQ`, not
merely a modular lower-bound heuristic.

The checker separately reduces the 135-term target (1) to zero.  Full row
rank is stronger: every polynomial in the stated truncated fine-degree
space has a rational source-provenant lift.  The matrix and maximal-minor
column hashes freeze both the complete combinatorial map and the particular
minor used as the certificate.

## What remains

This calculation advances the concentrated-spoke one-bad packet by two
filtered layers, but it does not yet empty that chart.  A truncated lift can
introduce terms in the next filtration level through its multipliers.  An
all-order conclusion needs either

1. an exact source lift whose complementary multipliers force no terms above
   order three;
2. a filtered contraction controlling orders four through seven; or
3. direct full fine-degree membership.

A useful counterguard is that restricting every complementary multiplier to
be colour-diagonal is not enough: that 501-column submodule does not contain
(1) modulo `1,000,003`; its first residual has off-diagonal order two.  Thus a
theorem-completing identity genuinely needs off-diagonal multiplier tails,
not just the old diagonal lift rewritten.

The statement also retains the earlier concentrated holes `(01),(23)` and
fixed singular spokes.  It gives no multisite-star conclusion and therefore
does not by itself close the sole one-bad packet or prove the `N=8` theorem.

## Reproduction

Run

```text
.venv/bin/python computations/verify_n8_lemma_e_unary_top_offdiagonal_filtered_lift.py
.venv/bin/python -O computations/verify_n8_lemma_e_unary_top_offdiagonal_filtered_lift.py
```

The checker is dependency-free.  It rebuilds all token matchings, 285 source
rows, 41,496 filtered columns across the two cutoffs, and both maximal-minor
certificates.  The frozen ledger is

```text
SHA-256:
ed4a6232d00cf907e82be44d7705daf0ba311d2c3c18c3f89477ea94b036b1ea
```
