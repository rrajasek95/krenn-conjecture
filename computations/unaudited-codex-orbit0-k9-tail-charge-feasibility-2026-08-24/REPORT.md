# Exact omitted K9--K12 tail charge

## Result

The bounded literal replay passes.  For

`R_tail = (H0 H1 H2) - S_9607`

in omitted K-degrees 9 through 12, pairing `a R_tail` with the pinned
77-cycle functional gives

| degree | target | source | target - source |
|---:|---:|---:|---:|
| K9 | 245,760 | 19,055,616 | -18,809,856 |
| K10 | -1,170,432 | -16,093,440 | 14,923,008 |
| K11 | 331,776 | 3,313,152 | -2,981,376 |
| K12 | 13,824 | -2,290,176 | 2,304,000 |
| **total** |  |  | **-4,564,224** |

Thus K10--K12 contribute +14,245,632 and complete the retained K9 value
-18,809,856 to exactly -4,564,224.  This is the missing correction required
by the independently computed +4,564,224 charge of the truncated input
`-R8' E0 E1 E2`.

## Independent guards

- The evaluator checks pinned SHA-256 digests for the 9,607-term seed, the
  retained K9 quotient ledger, its seed metadata, and the 77-functional.
- It evaluates 105^3 target outputs and 9,607 x 105 source-column outputs
  literally, split by K-degree.
- It separately pairs all 49,988 retained H-coinvariant K9 orbit masses and
  obtains the same -18,809,856.
- Standard and `python3 -O` runs have identical logical result SHA-256
  `e18048edf346a8d6516f817bb820a9f26df6c5633cee9b594520b498c8c638b6`.
- The strict validator passes in both modes and rejects a mutated total.

## Scope

This closes the scalar conservation interface for the omitted tail.  It does
not reduce the tail rows, compute their K24 residual, decide relative terminal
membership, cover the other chart orbits, or prove/disprove the conjecture.

