# Chart 25 has an exact four-row obstruction at degree four

The complete source-faithful chart-25 lift through off-carrier degree four is
inconsistent over characteristic zero.  Equivalently, the exact identity

\[
                  H_0H_1H_2\in I_{\mathrm{mix}}+K^4
\]

proved at the preceding layer does not extend modulo \(K^5\), even after all
kernel freedom from the degree-two and degree-three source blocks is retained.

The obstruction is much smaller than the discovery matrices suggest.  In the
canonical invariant row basis it has only four nonzero values:

| filtration degree | canonical coordinate-id row | value |
|---:|---|---:|
| 2 | `0 13 17 76 98 126 171 188 220 224 229 243` | -2 |
| 2 | `0 13 17 77 98 126 171 184 220 224 230 243` | -1 |
| 2 | `0 13 17 79 94 126 171 188 220 224 232 243` | -1 |
| 4 | `0 13 17 94 98 126 171 184 188 220 224 243` | 1 |

All coefficients are integers.  No rational reconstruction or modular rank
inference is used in the theorem.

## Exhaustive annihilation is support-local

A mixed Macaulay column can pair nontrivially with this functional only if one
of its matching terms is one of the four displayed rows.  Factoring every
displayed row in every possible way and then passing to chart-stabilizer
representatives recovers exactly

```text
minimum K-degree 2: 9 columns
minimum K-degree 3: 0 columns
minimum K-degree 4: 0 columns.
```

The exact pairing is zero on all nine columns.  This is an exhaustive proof
for the complete source families, not a sample: every other one of the 59,488
older column-orbits and 913,608 degree-four column-orbits misses the support
of the functional and therefore pairs to zero.

In particular, it also annihilates all 31,584 transferred lower-kernel tails.
Indeed a transferred tail is obtained from a linear combination of older
source columns whose lower part cancels; annihilation of every full older
column is stronger than checking one chosen kernel basis.

## Exact target pairing

On the three degree-two support rows, the target coordinates are

\[
                         (-1,0,0).
\]

On the degree-four row, the raw target coordinate is \(-1\).  Exactly three
columns of the frozen degree-three certificate meet this row, with total
contribution \(2\), so the degree-four tail coordinate is \(1\).  The complete
pairing is therefore

\[
                     (-2)(-1)+(-1)0+(-1)0+1\cdot1=3.
\]

Thus the functional annihilates the entire source image but not the target.

## The modular rank bug that exposed the cell

The first discovery run reported transfer rank 17,224 modulo three primes.
That number was invalid and has been withdrawn.  Its quotient reducer stopped
as soon as it met a free coordinate.  A later combination of two transferred
vectors could cancel that free coordinate and expose an already-used higher
pivot; the transfer reducer then incorrectly counted the exposed pivot as a
new direction.

A common echelon of the stored higher and transfer families modulo 1009 gives
true additional transfer rank 6,006, not 17,224.  The corrected target still
survives.  The permanent checker includes the minimal two-tail regression:
the old early-stop algorithm reports rank two, while the common echelon has
rank one.  These modular figures explain the discovery but play no role in
the exact four-row certificate.

## Scope and reproduction

This is an exact finite-order, unsaturated obstruction on chart 25.  It rules
out the unmultiplied degree-four lift.  It does **not** by itself rule out
support localization, a higher power of the target, or hidden \(t\)-torsion
after homogenization, and therefore is not a proof of the full conjecture.

The permanent checker is

```sh
python3 computations/verify_n8_chart25_degree4_exact_dual.py
python3 -O computations/verify_n8_chart25_degree4_exact_dual.py
python3 -I computations/verify_n8_chart25_degree4_exact_dual.py
python3 -S computations/verify_n8_chart25_degree4_exact_dual.py
```

It reconstructs the four rows, exhausts their incident mixed columns, decodes
the frozen characteristic-zero degree-three certificate, evaluates the four
target coordinates directly, and freezes the structural ledger digest
`382b0894d2746707882b3660ea5ddd04f013f813b64d5133b4d872b95078c21b`.
