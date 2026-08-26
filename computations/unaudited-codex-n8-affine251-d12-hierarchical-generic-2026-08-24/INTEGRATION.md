# Generic hierarchical D12 integration

This package is a sibling of the restored native sparse package.  It does not
modify that parent.  The promotion baseline is parent `src/main.rs` SHA-256
`241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`.

Apply the promotion patch from the parent package directory:

```sh
patch --dry-run -p1 -i ../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/hierarchical_generic_v3.patch
patch -p1 -i ../unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/hierarchical_generic_v3.patch
cargo build --release --bin sparse_d12_dual
```

The dry run and real application were independently exercised on a temporary
copy of the pinned parent.  The patched file had SHA-256
`173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a`,
identical to `sealed_v3/main.rs`.

The promoted hierarchical interface is intentionally narrow.  It must be
selected with all of:

```text
--workers 16 --pivot rare --strategy cold
--elimination hierarchical --incremental no
```

Any other hierarchical worker count, pivot, strategy, or incremental setting
fails before input or output access.  The kernel additionally rejects a prime
that does not fit `u32`.  Existing `tree` and `vec` modes are unchanged.

Resume is generic: the established `--checkpoint` and `--vector-cache` readers
load any valid native sparse checkpoint, the outer loop retains its existing
round/cap logic, and the hierarchical kernel consumes the current exposed
columns and frequencies.  No round number, column count, candidate, cache
fingerprint, or fixture path is compiled into the kernel.  Checkpoint and
vector-cache serializers are untouched.  The round-748 test emitted the exact
same checkpoint and cache bytes as the restored sequential kernel at round 749.

The rare order is exactly the established natural `(frequency,row)` order.
The fixed FNV hash only selects one of 16 rank-map shards; it never orders a
pivot.  Sixteen balanced source-order column chunks materialize compact
`(u32 rank,u32 residue)` equations, are reassembled in source order, and feed
16 local bases.  Bases merge in the deterministic `16→8→4→2→1` arity-two tree;
free variables are zero and all exposed columns are verified before return.

On macOS, run production through `sealed_v3/run_with_macos_rss_watchdog.py`.
The inherited native RSS sampler can report zero when sandbox policy blocks its
child `ps`.  The wrapper therefore polls the entire process group through
Darwin `PROC_PIDTASKINFO` every 250 ms and sends TERM then KILL at 36 GiB or 120
seconds.  It quarantines any final/temporary native output after an abort and
writes telemetry atomically.  Its exact accepted command is embedded in
`control_hierarchical/watchdog.json`.

