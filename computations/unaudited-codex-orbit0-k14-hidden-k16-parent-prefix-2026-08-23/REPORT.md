# Hidden K14 -> K16 pivotable-parent recovery: measured prefix

## Result

`PASS_MEASURED_PREFIX`, not a full recovery and not a child-tail computation.
The deterministic 31/485 H-slice sample reconstructs 4,837,984 of the frozen
75,691,040 discarded pivotable K16 occurrences in 8.01 seconds.  They have
32,692,352 possible second-pivot uses and 1,394,334 nonzero labelled
path/signature/pivot profiles after exact coefficient collection.

## Exact convention and provenance

The target convention is `P=-R8'*E0*E1*E2`.  A first K14 pivot therefore has
coefficient `+mass/m1`; the stored parent coefficient is `+mass*U/m1`, where
`U=400591699200`.  The outgoing profile coefficient is `-mass*U/(m1*m2)`.
Every occurrence record contains the sorted labelled row, its U-scaled H-orbit
mass, anchor signature, and `(R8 slice, three factor-tail indices, p1, K2-tail
index, m1, m2)`.  With the pinned 78 anchor and K2/K3/K4 tail tables this is
sufficient to reproduce paths `(2,2)`, `(2,3)`, `(2,4)`, and `(2,2,2)`.

The profile file is deliberately a **labelled diagnostic**, not an H-canonical
quotient.  Its final key byte is wildcard zero: it describes the parent/pivot
environment shared by K2, K3, and K4 children.  The occurrence stream, not the
profile file alone, is the provenance-safe continuation interface.

## Atomic binary formats

Both files are written to `.tmp`, flushed, synced, and renamed.

- `H16PAR1`: 36-byte header `(magic[8], U:i128, modulus:u32, count:u64)`, then
  fixed 64-byte occurrence records: `row24, weight:i128, signature12, ri:u16,
  ia,ib,ic,p1,t1,m1,m2,reserved[3]`.
- `H16PRO1`: the same header, then sorted fixed 59-byte records:
  `path_profile29, signature12, p2, wildcard0, weight:i128`.

The exhaustive replay reconstructs all 4,837,984 rows from the source tuple,
checks every coefficient against its stored denominator, checks every
signature, and checks the sorted nonzero wildcard profile stream.  This local
replay does not independently recompute the valid-pivot sets.  Tail's
independent semantic replay recomputed valid `p1`, available `p2`, and all
12/32/60 tail families on 257 evenly spaced records; all passed.  The full
75,691,040 count remains a pinned frozen census, not something this prefix
recomputes.

## Full-size feasibility estimate

Scaling by the known full occurrence count gives about 126 seconds of serial
work, 511,477,120 outgoing-pivot uses, and exactly 4,844,226,596 bytes for the
full occurrence stream.  Linear scaling gives a conservative profile-file
upper estimate of 21.82 million records / 1.287 GB; observed unique-profile
growth is sublinear (1.675x when sampled H slices grow 1.938x).  The full run
should use atomic 16-H-slice occurrence/profile runs plus external merge, so
resident memory remains comparable to this prefix rather than scaling with
the final profile union.  No full run was launched.

## Scope

This recovers the missing parent interface only.  It does not emit any child
tail, reduce K18--K20, prove membership/nonmembership, or repair the retracted
K18/K19 charge totals by itself.
