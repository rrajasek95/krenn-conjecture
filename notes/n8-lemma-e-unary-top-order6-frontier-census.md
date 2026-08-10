# Order-six reachable-tail frontier

The exact concentrated identity now reaches off-diagonal order five.  A full
order-six Schur transport should not be launched blindly: its new quotient is
materially larger than the preceding one.

The deterministic direct-plateau census over `GF(1,000,003)` is

```text
order-six rows:                         12,835
minimum-order-six literal columns:       8,476
direct modular rank:                     7,918
direct modular quotient:                 4,917

full truncated rows through order six:  57,558
full literal columns through order six: 96,922.
```

The order-five quotient had dimension 948.  Thus the coordinate packet to be
carried is 5.187 times larger.  It would pass through the existing 44,638
pivots rather than the 25,714 pivots used at the preceding step; the simple
`quotient dimension x upstream pivots` workload proxy increases by 9.004.

This is an exact finite-field rank and dimension statement.  The modular rank
gives only a lower bound on the rational direct rank, so `4,917` is not
asserted as an exact `QQ` cokernel dimension.  No target tail, order-six
membership, or order-six obstruction was computed here.

The bounded continuation should carry only the particular corrected target
tail from order five and generate literal correction columns within its
reachable support component.  If that closure approaches all 4,917 modular
coordinates, the calculation has crossed the intended resource guard and
should stop.

Run

```text
.venv/bin/python computations/verify_n8_lemma_e_unary_top_order6_frontier_census.py
```

Frozen hashes:

```text
matrix:
7dd2f5e7fca787615932d0eb0e7d1af5b02a650796cf994004c384bb9e9c8dc3

ledger:
cb4e695ed5f4adde8b14106dd0cf24850c4f277dde540616c161219a300d1fc8
```
