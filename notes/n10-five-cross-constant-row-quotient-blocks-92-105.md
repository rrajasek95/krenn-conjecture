# Constant-row quotient and pair-block closure through block 105

## Outcome

Pair indices 91 through 104 close exactly.  The batch contains 834,960
supports; the same-vertex block at pair index 96 accounts for 2,352 prior
zero- or two-grade supports.  The remaining 832,608 grade-3-to-6 supports
reduce to 140 affine candidates and no coefficient-torus candidates.  Thus
there is no new literal determinant frontier in this batch.

The cumulative fixed-old five-cross closure is 6,236,328 supports, leaving
5,377,848 supports in the 196-block frontier.

The sharper result is a constant-layer quotient of the existing exact
matrix-witness library.  Of 5,359 winning augmented matrices from 1,909
fixed-old cases, 62 witnesses in 52 cases retain a rank jump after every row
containing a weight-degree-zero entry is deleted.  Consequently the earlier
obstruction is not confined to fixed-old constant-layer rows.

This is a positive structural lead, not an arbitrary-old-source identity.
The surviving positive-degree entries still have rational coefficients
computed from the anchored old source.

## Exact quotient certificate

For each augmented sparse polynomial matrix (A), delete any row with a
nonzero coefficient at cross-weight monomial (1).  On the remaining rows,
compare the first (c-1) columns with all (c) columns.  Two exact ranks are
computed:

1. rational rank at the nonzero point ((1,2,3,5,7)); and
2. the bipartite maximum-matching rank of the nonzero polynomial support.

The matching number is an upper bound on rank over the rational-function
field.  All 5,359 evaluated ranks attain this upper bound, so every reported
rank is the exact generic rank of that fixed-old polynomial matrix, rather
than a numerical specialization artifact.

The 62 surviving jumps have quotient records

| deleted rows | kept rows | base rank | augmented rank | witnesses |
|---:|---:|---:|---:|---:|
| 16 | 6 | 5 | 6 | 22 |
| 15 | 7 | 6 | 7 | 10 |
| 17 | 5 | 4 | 5 | 10 |
| 10 | 11 | 10 | 11 | 4 |
| 8 | 13 | 12 | 13 | 4 |
| 12 | 9 | 8 | 9 | 4 |
| 10 | 12 | 11 | 12 | 4 |
| 9 | 13 | 12 | 13 | 4 |

The first exact representative is

```text
((0,8,1,0), (0,8,1,2), (2,9,0,0), (3,9,1,0), (3,9,1,2))
```

with augmented witness `aug1`.  Ten constant-layer rows are deleted; the
base support has maximum matching 10 and the augmented support has maximum
matching 11.  Exact evaluation attains both bounds.  Its six permanent
grades are `(198,210,212,324,336,338)`.

## Scope and next implication

The quotient rules out the simplest no-go: it is false that every cached
obstruction disappears with the fixed-old constant layer.  It also exposes
a small incidence-level pattern—the extra augmented column increases the
matching number—which is the best current candidate for an
old-source-independent Fitting identity.

It does **not** yet prove that pattern for an arbitrary old source.  Row
support and nonvanishing of the remaining positive-degree coefficients were
both reconstructed from the anchored source.  A uniform theorem still needs
one of the following exact upgrades:

1. introduce symbolic old-source coefficients and prove that the ten-versus-
   eleven matching minor is a nonzero source-provenance monomial (or a unit
   modulo the four cylinder equations); or
2. show that admissible old-source deformation preserves the relevant row
   support and the nonvanishing factors.

No coefficient grid is used.

## Reproduction

```text
python3 computations/verify_n10_five_cross_constant_row_quotient_blocks_92_105.py
python3 -O computations/verify_n10_five_cross_constant_row_quotient_blocks_92_105.py
```

All matrix construction and rank arithmetic is exact over \(\mathbb Q\).
