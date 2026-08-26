# Full hidden K14 -> K16 pivotable-parent recovery

## Terminal result

`PASS_FULL_HIDDEN_K16_PARENT_RECOVERY` in the parent/profile/provider scope.
The 31 disjoint atomic runs cover all 485 frozen H slices and reproduce exactly
75,691,040 discarded pivotable K16 parent occurrences.  They retain exact
signed coefficients, literal representative rows, anchor signatures, source
factor/pivot/tail labels, and both pivot counts.

The runs contain 511,477,120 possible second-pivot uses.  Their 21,116,357
sorted nonzero labelled profile records externally merge to 6,585,438 distinct
keys before cleanup, 355,738 exact-zero keys, and 6,229,700 final nonzero keys.
The parent scaled coefficient sum is
`-146230609431055564800`; the second-response profile sum is its opposite.

The recovery phase took 125.9 seconds and the exact external merge 1.4 seconds,
inside the 300-second / 12-GB gate.  Parent files total 4,844,227,800 bytes;
profile runs total 1,245,866,303 bytes; the merged profile file is 367,552,332
bytes (SHA-256 `8e7630fb3edf77d6f56cbace019e1a7a1c2e61720da995aafccf7b120633e3e8`).

## Restartable children

`stream_hidden_k16_children` accepts
`DEGREE RUN_START PARENT_START PARENT_COUNT OUTPUT`.  It rereads the exact
parent occurrence, recomputes all available second pivots, asserts the stored
`m2` and divisibility, and emits the pinned 12/32/60 K2/K3/K4 tail families
with coefficient `-w1/m2`.  Restart coordinates and parent ordinal remain in
each output record.  One-parent format guards emit exactly 36, 96, and 180
children at degrees 2, 3, and 4.

## Replay and scope

The finalizer hashes every parent/profile run, checks the exact interval chain,
headers, sizes, denominator ledgers, coefficient sums, and frozen total.  It
also scans the complete merged profile stream for strict ordering, wildcard
tags, nonzero weights, and the exact total sum.  Result logical SHA-256:
`2de1bf3a6bd482222d87a4942c5cee3bfff2ecd2c39aec59f06506a595e9da31`.

This is a source-faithful recovery/provider interface only.  No K18/K19/K20
child-tail charge was evaluated, no downstream reduction was performed, and
no membership or nonmembership conclusion follows yet.
