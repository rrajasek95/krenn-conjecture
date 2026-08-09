# Exact N=8 diagonal-10 plateau transfer

The first root-plateau transfer has seven source-kernel tails whose leading
parts occupy 147 diagonal-10 state orbits.  Closing those states under every
maximal even-complement fibre gives a finite, exact plateau block with

```text
target states: 459
source columns: 426
rank:           300
source kernel:  126
target cokernel:159
```

The closure assertion is important: every diagonal-10 maximum of every
incident maximal fibre is included.  Thus this is a full connected plateau,
not a truncated rewrite neighborhood.

## Spectral direction

The seven incoming vectors are independent before quotienting by plateau
relations, but each lies exactly in the 300-dimensional plateau image.  Their
projection to the 159-dimensional diagonal-10 target cokernel is zero.  They
therefore do **not** kill or reduce the seven diagonal-12 target/chart
cokernel classes.  Instead, all seven diagonal-12 **source-kernel** classes
continue after correction by diagonal-10 columns.

Adding those seven continued sources to the 426 plateau sources leaves

```text
126 + 7 = 133
```

critical source classes at this page, versus 159 critical diagonal-10 target
classes.  The seven correction representatives have 14, 36, 12, 38, 53, 18,
and 31 terms.  They are the deterministic lex choices; they are not claimed
unique modulo the 126 intrinsic plateau-kernel classes.

Those 126 intrinsic kernel classes also have nonzero full lower tails.  Of
the resulting **133** critical source tails, 91 lead at diagonal 9 and 42 at
diagonal 8.  Their diagonal-9 initials have rank 81.  Thus the next page must
transport all 133 classes, not only the seven distinguished root descendants.

## Corrected lower tails

Exact replay against the full fibres cancels every diagonal-10 term.  The
seven corrected tails have 7,025 terms.  Six lead at diagonal 9 and one at
diagonal 8.  Their level histogram and modular ranks are

| diagonal level | term occurrences | rank among seven tails |
|---:|---:|---:|
| 9 | 169 | 6 |
| 8 | 2,139 | 7 |
| 7 | 2,813 | 7 |
| 6 | 1,904 | 7 |

The next smallest exact block is therefore the closed diagonal-9 maximal
plateau seeded by all 91 nonzero leading tails, while retaining the seven
distinguished root descendants as a separate readout.  Contracting it will
decide which of the 133 source classes continue to level 8 and which acquire
nonzero target-cokernel classes.

The exact checker is
`computations/analyze_n8_diagonal10_plateau_transfer.py`.  Its frozen ledger
SHA-256 is
`97bdfccdfd35249f0ee28c310f45a7e99a89ff7b12cfae0272976b07c1f27f8b`.
