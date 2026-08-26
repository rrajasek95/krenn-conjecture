# Hidden K16 K2 orbit-aware prefix audit

## Verdict

The requested 29-byte path-profile quotient is **not** source-faithful for
literal K2 collection.  On the frozen slice, 59,970 of 62,678 profile keys
contain more than one decorated `(literal parent row, second pivot)` H-orbit,
with as many as 48.  The TSV counterexample pins one key and two inequivalent
decorated representatives.  Therefore generating the 12 K2 children from the
single witness stored in each merged profile record is invalid.

The exact replacement is to externally merge H-canonical decorated-pair keys

```
(canonical_H(parent row, selected second pivot), coefficient mass,
 orbit size, stabilizer size)
```

and generate the 12-child family once per such key.  The bounded slice reduces
1,054,592 labelled parent/pivot uses to 261,696 nonzero decorated pair orbits,
then generates 3,140,352 children instead of 12,655,104.  Every observed pair
orbit has size 384 and trivial stabilizer.  Its collected child map agrees
exactly with the frozen 694,172-row checkpoint: zero coefficient, support, or
pivotability mismatches.

## Exact equivariance lemma

Let `D=(r,p)`, let `A_p` be its four-cell pivot anchor, and let `T_p` be the
literal 12-term K2 tail set.  The frozen H action permutes the 78 anchors and
the tail sets, and for every `h in H` and `t in T_p`,

```
h replace(r,A_p,t) = replace(hr,A_hp,ht).
```

Canonical child rows are H-invariant, so the canonical multiset of the 12
children depends only on the decorated-pair H-orbit.  Summing all already
scaled contributions `w2=-w1/m2` in that orbit and generating the family once
therefore preserves every literal coefficient.  No orbit-size division is
made: source orbit masses are already present in `w1`; the stored orbit and
stabilizer sizes are provenance metadata and replay guards.

## Compression and feasibility

The measured pair/child generation compression is 4.029836146 on the slice.
Scaling the measured decorated-orbit/profile ratio to the frozen 6,229,700
coarse profiles gives an explicitly non-load-bearing estimate of 26,010,524
decorated pair orbits and 312,126,288 generated K2 children.  This is about
19.7 times fewer tail generations than the 511,477,120 labelled second-pivot
uses times 12.  The optimized exact prefix takes about 3.1 seconds; a full
implementation should create sorted decorated-pair runs per parent run,
externally merge them (including exact-zero deletion), stream 12 tails per
merged key, and externally merge canonical child runs.  The estimated pair
ledger is about 1.38 GB at the frozen 53-byte record format.  Full counts and
runtime remain estimates until that external merge is run.

## Replay and scope

Compile and run from the repository root:

```sh
rustc -O --edition=2021 \
  --cfg 'feature="hidden_child_prefix"' \
  --cfg 'feature="full_hidden_charge"' \
  computations/unaudited-codex-orbit0-hidden-k16-orbit-profile-prefix-2026-08-23/audit_hidden_k16_pair_orbits.rs \
  -o /tmp/audit_hidden_k16_pair_orbits
/tmp/audit_hidden_k16_pair_orbits
```

Optimized, unoptimized, and overflow-checked builds have the same timing-free
logical digest:
`01c8794d3047e49c2a02381d8c535ee43a76eb90431907a3900120d2a90f8159`.
An independent referee also decoded all 261,696 ledger records, matched every
key/weight/use, checked 359,424 H pivot-tail transports, and reproduced the
same 694,172-row Cycle checkpoint; its report is
`computations/unaudited-codex-orbit0-hidden-decorated-h-action-referee-2026-08-23/REPORT.md`
(SHA-256 prefix `531e9a20`).
This package proves only the bounded frozen slice and the equivariant collector
lemma.  It does not assert the estimated full orbit count or perform the full
K2 collection.
