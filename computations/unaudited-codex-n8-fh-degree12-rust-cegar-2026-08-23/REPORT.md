# Rust full-Fh degree-12 lazy CEGAR

## Result

`BOUNDED_RESUMABLE_UNRESOLVED`: no membership or nonmembership claim.

The Rust modular engine exactly reproduces every shape count in the
authoritative Python/Q ledger through round 22:

```text
rows 355,170; columns/rank 4,200; dual 625; incident 4,112; new 2,048.
```

It then continues four complete rounds.  The last accepted round is 26:

```text
rows                   1,473,022
column orbits/rank         18,527 / 18,527
dual support                4,128
incident column orbits     22,587
new crossing orbits         7,316
```

All 7,316 crossings were admitted and frozen, so the resumable round-27
checkpoint contains 25,843 literal invariant column orbits.  The round-27
modular solve remained full rank through vector 17,152, but was interrupted
at the 20-minute wall gate.  That partial round is discarded.

## Machinery and scope

The Rust engine uses deterministic least-coordinate sparse pivots over
`F_1073741827`.  The source-faithful Python orchestrator expands literal
normalized column orbits, computes actual `F^h` coefficients, scans every
incident orbit, and admits every nonzero crossing.  It writes a complete
checkpoint after each accepted round.  A modular stall is never promoted:
the driver requires a second prime, rational reconstruction, exact target and
column replay, and expansion to actual columns.

Artifacts:

- `checkpoint_fh_degree12_rust_cegar.json` — resumable r27 state;
- `src/main.rs` — sparse modular engine;
- `run_fh_degree12_rust_cegar.py` — source/orbit orchestrator;
- `package_bounded_result.py` and `results_fh_degree12_rust_cegar.json` —
  bounded replay ledger.

This is only the full normalized `F^h` homogeneous degree-12 problem.  It
makes no truncated-`C10`, degree-13, saturation, or unlocalized claim.

## Incremental-basis optimization

The follow-up engine stores the sparse echelon basis and remaps its row
coordinates order-preservingly as the interface grows.  It verifies before
every solve that every old column is zero on every newly discovered row, then
reduces only the pending crossing columns.  This reproduces **all six frozen
counts in every round 0 through 26**, including r23--r26 dual and crossing
counts, not merely ranks.

The incremental 20-minute run reached the r27 fill band.  It verified full
rank through 7,168 of the 7,316 pending columns, then stopped at the hard wall.
The partial basis was discarded atomically.  The resumable state remains the
fully accepted r26 basis:

```text
rows 1,473,022; processed/rank 18,527; pending crossings 7,316.
```

Use `run_fh_degree12_incremental.py --resume`.  The state is
`checkpoint_fh_degree12_incremental.json`, `incremental_basis.bin`, and
`incremental_rows.bin`; its bounded replay is
`package_incremental_bounded.py`.  No exact membership/separator verdict was
obtained.

## Atomic within-round continuation

The one permitted 600-second continuation preserved r26 and wrote a separate,
append-only r27 pivot journal.  Each 256-vector batch is flushed, `fsync`ed,
and atomically renamed.  The terminal durable state is:

```text
r27 row coordinates          1,997,290
pending columns                   7,316
durably reduced                   5,376
remaining                         1,940
full rank through                23,903
atomic batches                       21
```

There is still no modular stall and hence no exact membership or separator
verdict.  The 1,997,290-row table, row embedding, and complete Rust input are
serialized and hash-guarded, so a future continuation can bypass the roughly
330-second Python rematerialization and load the 21 journal batches directly:

```text
python3 run_fh_degree12_incremental.py \
  --resume-materialized-round --wall-cap-seconds N
```

The exact replay is `package_incremental_round_checkpoint.py`; logical digest
`a85d61d1183be2d94d6279f9456d46cc2527a626ebbfb0c58ef7597c7881f01d`.

## Structural r27 theorem and its boundary

No further rank solve is needed to establish the r27 rank increment.  Relative
to the accepted r26 row interface, the 7,316 pending columns create 524,268
new rows.  There are 447,520 degree-one ownership rows, and **every pending
column has a private coefficient-`+1` top row immediately**.  Hence the whole
r27 packet is independent over `Z` relative to r26.  The degree-eight
multipliers are exactly seven physical 2-factor shapes; the load-bearing
checker is `audit_r27_pending_structure.py` (logical `ff43d593...`).

Those leaves are not globally private.  All 447,520 have a distinct literal
homogeneous-D12 owner.  The selected 7,316-row collision shell has 58,497
columns and 67,635 incidences, including 51,181 columns outside r27.  Its
2-core is 3,942 rows by 7,180 columns with 15,400 coefficient-one edges.
Degree-two sign propagation followed by exact rational reduction of 858
collapsed hyperedges gives

```text
rank_Q = 3,178; left nullity = 764.
```

Both modular controls give rank 3,178.  Every one of the 51,181 external
owners has outputs beyond the r27 interface, so one-shell cellular closure
fails.  See `audit_r27_global_private_core.py` and
`audit_r27_owner_shell_topology.py` (logical `2b31f425...` and `e92e1fd6...`).

## Terminal homology seed and attachment

Extending the stored r26 modular dual by the selected private rows annihilates
all r27 columns.  Scope correction: two of the 7,316 selected rows, not zero,
have pure-target coefficient `+1`; the audited post-correction target pairing
is nevertheless nonzero (`600319282 mod 1073741827`).  Its canonical sparsest
class in the 764-dimensional exact integer core obstruction is

```text
+ 040809487997a8d7dbe1eff1
- 040809487984bbd7dbe1eff1
```

It annihilates all core columns over `Z`, pairs `97612875` with the modular
correction, and has 20 escaping owner columns.  Support one is impossible.

The one permitted exact attachment through those 20 owners collected 1,665
escape rows and imposed all 88 incident frozen-shell columns.  It is
inconsistent: the first exact residual is `-1` at literal column
`1:04088385b0c5e5f9`.  Thus this two-row class **dies on the first attachment**;
it is not promoted to a second shell.  See
`audit_r27_extended_dual_homology.py` and
`audit_r27_two_row_one_attachment.py` (logical `701d9d86...` and
`cb5d5fb7...`).

The fast terminal replay is `package_r27_structural_theorems.py`, logical
`1614b22dd85c350026874f7bc111fcfb3136868cc06bb4845cfc19de46cfeb6c`.
This retires this bounded exponent-one D12 lane; it is not an exact-Q full-Fh
membership verdict and makes no degree-13 or saturation claim.
