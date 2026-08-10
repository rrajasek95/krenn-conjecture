# The filtered high-pair seven-row lift has a symmetric star defect

## Result

Fix the filtered Segre chart, the two positive-grade cells
`23:10,25:10`, and the maximal grade-zero envelope: all 24 face cells,
all diagonal cells, and arbitrary `p2,s2` support.  Tesla's canonical
seven-row combination is not a unit identity on this envelope.  It is

\[
  1+D,\qquad
  D=\sum_{0\leq i<j\leq5}(p_{2,i}s_{2,j}+p_{2,j}s_{2,i})C_{ij}.
\]

There are 66 literal source monomials in `D`, exactly 15 symmetric
off-diagonal star factors, and no diagonal-star term.  Thus the failure is
not arbitrary contamination: it is precisely the repeated-row/column
sector omitted by the frozen Boolean support.

## Exact factors

Writing `xuv_ab` for the endpoint-coloured residual cell, the nonzero
factors are

```text
C01 = -x02_12*x14_02*x35_22 -x04_12*x12_02*x35_22 -2*x24_22*x35_22
C02 = -x14_22*x35_22
C03 = -x15_22*x24_22
C04 = -x12_22*x35_22
C05 = -x13_22*x24_22
C12 = -x04_22*x35_22
C13 =  x02_20*x25_22*x45_21 +x04_20*x25_21*x45_22
       -x05_21*x25_22 -x05_21*x45_22 -x05_22*x24_22
C14 = -x02_22*x35_22
C15 =  x02_20*x23_22*x34_12 -x03_21*x23_22 +x03_21*x34_22
       -x03_22*x24_22 -x04_20*x23_21*x34_22
C23 = -x04_22*x15_22 -x05_22*x14_22
C24 = -x04_20*(x12_22*x35_22+x13_22*x25_22+x15_22*x23_22)
C25 = -x03_22*x14_22 -x04_22*x13_22
C34 = -x02_22*x15_22 -x05_22*x12_22
C35 = -x01_22*x24_22 -x02_22*x14_22 -x04_22*x12_22
C45 = -x02_22*x13_22 -x03_22*x12_22
```

The checker reconstructs these factors directly from literal matching
coefficients, rather than from a support shadow.

## The obvious source-row closure does not remove it

At the exact bidegrees occurring in `D`, take every mixed top row multiplied
by every ordered `p2_i*s2_j`, and every mixed `p2s2` response row multiplied
by either `1` or one residual `q` coordinate.  After duplicate removal this
is a 48,756-row family.  Exact sparse elimination over `Q` gives rank 48,426
and leaves all 66 terms of `D` unchanged.

Consequently the frozen seven-row certificate is a diagnostic, not a
maximal-envelope theorem.  Any extension must use a genuinely higher
nonlinear relation or another response sector; it cannot be obtained by the
natural degree-compatible mixed top/`p2s2` row closure.

## Scope

This is a sharp obstruction to the stated source-provenant linear lift.  It
does not prove that the full maximal-envelope ideal is proper, nor does it
exclude a higher-degree Nullstellensatz certificate.  It also does not
weaken the coefficient-emptiness result for Tesla's frozen minimum model.

Reproduce with:

```bash
python computations/verify_n8_one_bad_segre_filtered_high_pair_seven_row_defect.py
python -O computations/verify_n8_one_bad_segre_filtered_high_pair_seven_row_defect.py
```
