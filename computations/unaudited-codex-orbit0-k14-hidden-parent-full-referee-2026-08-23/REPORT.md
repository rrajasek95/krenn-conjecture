# Independent full hidden-parent recovery referee

## Verdict

`PASS_INDEPENDENT_FULL_HIDDEN_PARENT_REFEREE`.  Cycle's full recovery is
source-faithful and complete for the parent/profile interface.  The 31 atomic
runs partition the 485 H slices exactly once and reconstruct precisely

```text
75,691,040 pivotable K16 parents
511,477,120 second-pivot uses.
```

The parent signed mass is `-146230609431055564800` at scale
`U=400591699200`; the outgoing profile mass is its negative, as required by
the second cancellation sign.

## Independent checks

- Every run header, interval, record size, file size, and SHA-256 agrees with
  the final ledger.  The interval chain is `[0,16),…,[480,485)` with no gap or
  overlap; it contains 838,080 K14 heads.
- First/middle/last parent records from every run (93 total) were replayed from
  literal R8 and factor-tail provenance.  Their valid first pivots, all second
  pivots, denominators, rows, signatures, and `+mass*U/m1` coefficients agree.
- An independent hash-map implementation reaggregated all 21,116,357 labelled
  profile records.  It reproduced 6,585,438 distinct keys, 355,738 exact-zero
  keys, and the byte-identical 6,229,700-record nonzero merged stream.
- The merged stream is strictly sorted, nonzero, wildcard-tagged, and has
  SHA-256 `8e7630fb3edf77d6f56cbace019e1a7a1c2e61720da995aafccf7b120633e3e8`.
- Corrected K2/K3/K4 provider guards were reconstructed byte-for-byte from the
  first parent: 36, 96, and 180 children, respectively, with 12/32/60 tails per
  second pivot and the sign `-weight/m2`.

## Scope

This accepts the full hidden-parent and labelled-profile recovery plus the
restartable child-provider interface.  It does not bulk-emit child tails,
compute their charges, reduce K18--K20, or restore the retracted ledgers by
itself.  Standard, optimized, and isolated Python replays agree.
