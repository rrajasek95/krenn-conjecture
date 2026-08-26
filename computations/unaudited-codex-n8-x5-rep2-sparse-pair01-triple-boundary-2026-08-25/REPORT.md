# Rep2 exhaustive triple-coordinate pair01 boundary

## Outcome

Every full-pair01 amplitude chart obtained from the sealed 17-coordinate base
by admitting at most three of its 70 zero coordinates has unit ideal over
`Q`.  Hence any full-pair01 point on this source chart requires **at least
four additional amplitude coordinates**.

This strengthens the sealed `>=3` boundary by exhaustively covering all
`C(70,3)=54,740` triple charts.  It remains an amplitude-only sparse-support
theorem; guard, adjoint, incidence, and rank-nonzero equations are separate.

## Enumeration and normalization

All 54,740 literal triple supports were generated source-faithfully.  Taking
the byte-minimum over the six bijections from the three new coordinate names
to canonical names `extra0,extra1,extra2` reduced them to 3,366 exact
polynomial groups.  Canonical inputs total 11,464,016 bytes (largest 4,598
bytes); the full enumeration took 128.98 seconds and launched no ideals.

The launch projection from the sealed double-coordinate census was 127.4
seconds at its measured mean and 209.5 seconds conservatively, satisfying the
requested `<10,000` groups and `<15 min` gates.

## Exact-Q production and independent replay

All 3,366 groups were run sequentially with a hard 2-second per-lane gate and
900-second aggregate gate.  Production stopped only after exhaustion:

```text
UNIT       3,366
NONUNIT        0
failure        0
raw charts 54,740 / 54,740
wall       153.70 s
max lane     0.733 s
```

The independent audit then:

1. rebuilt the exact `C(70,3)` set and verified no missing/duplicate support;
2. regenerated all 54,740 raw programs with a separately implemented
   six-permutation canonicalizer and reproduced every normalized hash;
3. independently reran all 3,366 canonical Singular ideals, all unit.

The independent replay used 133.14 seconds for normalization and 116.82
seconds for the Q ideals.  The earlier 388 monomial-triple diagnostics are
not used; this exhaustive ledger supersedes their limited coverage.

## Exact scope

Combined with the sealed base/single/double package, the result covers exactly
all zero-, one-, two-, and three-coordinate extensions of the base17 chart.
There is no rational or algebraic-closure full-pair01 point on any such
chart.  Because every amplitude ideal is unit, there is no resulting point
on which to test guard, adjoint, or carrier incidence.

The next search must start at four additional coordinates.  It should not
enumerate `C(70,4)` naively; a necessary residual-monomial hitting condition
should first reduce the candidate support family.

Parent <=2 boundary manifest:
`52c4900fab9799096f4967dc04eaba223c36d640d787a87a5708652b2d187ee8`.
