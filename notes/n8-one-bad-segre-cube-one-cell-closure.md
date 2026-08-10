# One-cell closure of the Segre--K4 diagonal-carrier chart

## Exact result

Among the 76 decorated coordinates missing from the fixed Segre--K4 chart
with arbitrary `00`, `11`, and `22` cells, 60 leave the original six-row
unit unchanged.  Twelve more are killed by six explicit alternative
integral coefficient identities.  Thus 72 of the 76 one-cell extensions are
top-empty without using the response rows.

The six certificate groups are

```text
R1: 02:10, 04:12
R2: 02:12, 04:10
R3: 03:01, 13:01
R4: 03:20, 05:21
R5: 04:02, 14:02
R6: 05:01, 15:01
```

Each identity expresses the fifteen-term pure-zero hafnian as an integral
combination of mixed coefficients of the enlarged quadratic.  The checker
`computations/verify_n8_one_bad_segre_cube_one_cell_closure.py` expands and
verifies all twelve identities exactly; the recipes use only coefficients
`+1` and `-1` and between 9 and 15 multiplier terms.

## Four residual directions

Exactly four one-cell extensions are not closed by these degree-filtered
identities:

```text
02:20, 03:10, 04:20, 05:10.
```

They are all outgoing one-zero-endpoint cells from site 0, with two colour-1
and two colour-2 directions.  This is the first genuinely small endpoint
star packet exposed by the common unary top.  The next high-impact test is
to impose the four one-bad response rows on these four directions and decide
whether they force concentration/clean cap or admit a coefficient-feasible
carrier.

This is a one-coordinate theorem.  It does not exclude simultaneous
deformations, including interactions among directions that are individually
invisible.
