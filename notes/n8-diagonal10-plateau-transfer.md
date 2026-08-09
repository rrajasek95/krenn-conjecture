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
plateau seeded by the six nonzero leading tails.  Contracting it will decide
whether those six continue to level 8 or acquire nonzero target-cokernel
classes.  The seventh continued source already starts at level 8.

The exact checker is
`computations/analyze_n8_diagonal10_plateau_transfer.py`.  Its frozen ledger
SHA-256 is
`4fbe1712d8cd33d152f22c8b6f2739aa7c89cf5d329c11990a1b47b97d363574`.
