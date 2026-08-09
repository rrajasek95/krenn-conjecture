# Exact closure of five-cross pair blocks 22 through 35

## Outcome

Two more complete seven-block batches close exactly.  They are survivor-pair
indices 21 through 34, or blocks 22 through 35 in one-based language.  The
audit processes 834,960 supports; 2,352 same-vertex supports have zero or two
permanent grades and belong to the earlier theorems.  The other 832,608 new
grade-3-to-6 supports all fail the literal cut-2 source equations.

Exact affine reduction leaves 1,038 candidates, rank-one torus saturation
leaves 208, and evaluated-column certificates exclude all 208.  There are
100 global monomial exclusions and 108 principal-divisor exclusions.  No
literal survivor appears.

Together with blocks 1 through 21, the cumulative exact closure is
2,082,696 of the 11,614,176 five-cross pair supports.  The remaining
unaudited frontier contains 9,531,480 supports.

This is a fixed-old, fixed-cut N=10 theorem, not a Krenn counterexample or an
all-order argument.

## Exact census

| pair index | pair | affine signatures | affine | torus | divisors |
|---:|---|---:|---:|---:|---:|
| 21 | \((0,8;1,2),(6,8;0,0)\) | 324 | 0 | 0 | 0 |
| 22 | \((0,8;1,2),(6,8;1,0)\) | 401 | 207 | 28 | 0 |
| 23 | \((0,8;1,2),(6,8;2,0)\) | 265 | 0 | 0 | 0 |
| 24 | \((0,8;1,2),(7,8;0,0)\) | 191 | 0 | 0 | 0 |
| 25 | \((0,8;1,2),(7,8;1,0)\) | 221 | 207 | 6 | 0 |
| 26 | \((0,8;1,2),(7,8;2,0)\) | 148 | 0 | 0 | 0 |
| 27 | \((1,8;1,0),(1,8;1,2)\) | 251 | 70 | 0 | 0 |
| 28 | \((1,8;1,0),(2,8;0,2)\) | 325 | 0 | 0 | 0 |
| 29 | \((1,8;1,0),(2,8;1,2)\) | 422 | 70 | 0 | 0 |
| 30 | \((1,8;1,0),(2,8;2,2)\) | 382 | 0 | 0 | 0 |
| 31 | \((1,8;1,0),(3,8;1,2)\) | 723 | 207 | 75 | 58 |
| 32 | \((1,8;1,0),(4,8;1,2)\) | 304 | 70 | 27 | 21 |
| 33 | \((1,8;1,0),(5,8;1,2)\) | 693 | 207 | 72 | 29 |
| 34 | \((1,8;1,0),(6,8;0,2)\) | 283 | 0 | 0 | 0 |

The 108 non-monomial generic pivots have one irreducible rank divisor each:

\[
          ac+1\quad(11),\qquad ad+1\quad(47),\qquad
          ae+1\quad(50).
\]

For every support and divisor \(f\), the checker selects a pivot at an exact
nonzero rational point of \(f=0\), recomputes the global square and augmented
residual determinants, and verifies

\[
              \langle f,\det M_f,tabcde-1\rangle=(1).
\]

Thus the special pivot is nonzero everywhere on its torus divisor and the
generic pivot covers the complement.  These are source-faithful divisor
certificates, not samples from a coefficient grid.

The next pair is

\[
                  \{(1,8;1,0),(6,8;1,2)\}.
\]

No symmetry transfer to that block is asserted.

## Reproduction

Run

```text
python3 computations/verify_n10_five_cross_pair_blocks_22_35.py
python3 -O computations/verify_n10_five_cross_pair_blocks_22_35.py
```

The checker uses exact rational arithmetic and Singular torus saturation,
factorization, and localized unit-ideal calculations.
