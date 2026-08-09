# N=8 diagonal-8 modular plateau frontier

The exact diagonal-9 output has 308 critical source classes.  Of these, 274
have nonzero diagonal-8 initials, of raw modular rank 260 on 6,998 seed state
orbits.  Closing under all maximal even-complement fibres gives the finite
orbit-compressed sparse block

```text
rows:       7,077
columns:    3,267
nonzeros:  30,881
```

The incoming matrix has 46,146 nonzeros.  Deterministic sparse elimination
over three prime fields gives the same plateau rank 2,961, hence modular
kernel 306 and cokernel 4,116.  After quotienting by the plateau image,
exactly 26 of the 308 incoming classes have nonzero independent remainders.
The seven distinguished root descendants contribute six independent
remainders.

If the same ranks hold over `QQ`, the page dimensions would be

```text
source: 306 + 308 - 26 = 588
target: 4116 - 26       = 4090.
```

This is deliberately **not** asserted over `QQ`.  A nonzero 2,961 minor mod
`p` proves only `rank_Q >= 2961`; three agreeing primes do not provide an
upper-rank certificate.  The same guard applies to the quotient ranks 26 and
6.  The checker freezes canonical row, column, incidence, pivot, and remainder
hashes so a later sparse rational solver can operate on exactly this matrix.

## Localization guard

All rows and columns here are canonical `S8 x S3` orbit types.  This is an
exact orbit-compressed incidence calculation, not a labelled Macaulay matrix
inside one localized chart.  The earlier root-kernel combinations mix support
column orbits attached to different root charts, and canonicalization also
collapses multiple labelled fibre outputs into one orbit coefficient.
Therefore these transfers do not certify membership in any individual
`P_j` localization without a labelled/common-denominator lift.

The checker is `computations/analyze_n8_diagonal8_plateau_transfer.py`.  Its
frozen ledger SHA-256 is
`a31399cd4b5852641f476395053d54e14aad96b2d83d7d3ed306cb633cf41709`.
