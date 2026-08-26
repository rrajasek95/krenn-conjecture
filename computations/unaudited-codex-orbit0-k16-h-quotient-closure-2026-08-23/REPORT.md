# Sound H-orbit closure of the lex K14 target

## Verdict

The order-384 H-orbit/mass provider is exact, but the target component remains
unresolved.  One complete expansion of the lex K14 orbit produces 106 source
column orbits and 7,485 row orbits; 7,484 rows remain queued.  The cap was
spent completing and literally replaying this first expansion.  No peel,
rank, membership, or dual inference is made from the open frontier.

## Exact frontier

The target is the complete H-orbit sum of

```text
000004080d1955627575797d97c4c6cfd3d7e0e6eaeef2f3
```

whose H-orbit has size 384.  Matrix coordinates use total orbit mass.  The
first complete row expansion is:

| quantity | value |
|---|---:|
| processed row orbits | 1 |
| source column orbits | 106 |
| row orbits | 7,485 |
| queued row orbits | 7,484 |
| K12 rows | 13 |
| K13 rows | 103 |
| K14 rows | 831 |
| K15 rows | 1,046 |
| K16 rows | 5,492 |

All 106 source-column orbits have size 384.  Among the rows, 7,483 have orbit
size 384 and two have orbit size 192.  None of the 5,492 encountered K16
representatives is a nonzero terminal of the frozen collected-residual DAFSA;
they are nevertheless retained because zero-residual K16 rows and all K12--15
rows are required for sound source closure.

## Mass and provenance guard

For a source-column representative `C`, the quotient entry is computed as

```text
entry(R,C) = |Orb_H(C)| *
             #{base matching terms of C canonicalizing to R}.
```

The first eight column orbits were replayed by explicitly expanding every one
of their 384 literal source columns.  Seven have 40,320 retained literal
occurrences and one has 4,992; all quotient masses agree exactly.  The same
eight columns pass all 3,072 source-action equivariance checks.  Column
records preserve the literal word, multiplier, row representative, orbit
size, entry mass, and base matching indices.

The row-representative digest is
`7544f686c337a46a3f9f09f6cd63a1eb1acdfe965ab6b66e1a34e3d2d3ee83ed`;
the column-representative digest is
`f102608ff89c7a0b63efe21e850d66b0c103a1ce83e347141e4d28ea20292f62`.

## Scope and replay

This is a resumable, source-faithful first frontier for the complete H-orbit
of one lex target.  It is not the full 1,848,174-row weighted K16 residual and
does not decide the filtered containment.  The run is intentionally frozen;
do not infer from row ownership until every incident column orbit is exposed.

```bash
python3 computations/unaudited-codex-orbit0-k16-h-quotient-closure-2026-08-23/run_k16_h_quotient_closure.py --seconds 285
```

Result logical SHA-256:
`4c65bde82d52406f7faaf9bbff9934c0e3ccd31c8db110d91df40dec0cde8496`.
