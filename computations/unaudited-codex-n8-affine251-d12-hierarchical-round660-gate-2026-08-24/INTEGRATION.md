# Promotion integration against the restored native D12 solver

## Baseline and tested implementation

Apply no integration unless the untouched native source first hashes to:

```text
241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0  computations/unaudited-codex-n8-affine251-orbit-membership-2026-08-24/src/main.rs
```

The tested sibling implementation is:

```text
d289bc12ba16759c10dc5335057e8c8ed8edb476abbacb228af5c44871672579  computations/unaudited-codex-n8-affine251-d12-hierarchical-round660-gate-2026-08-24/src/main.rs
89ae110e58ebbf478ead404d4f69662abc32db6e081cc37958fd808c646875aa  computations/unaudited-codex-n8-affine251-d12-hierarchical-round660-gate-2026-08-24/target/release/d12_hierarchical_round660
```

The executable harness is deliberately fixture-locked to the sealed round-660
hashes/counts.  It does **not** itself resume arbitrary checkpoints.  The
hierarchical kernel is generic in the equation collection and rare ordering;
after the integration below, the existing native outer CEGAR loop retains
responsibility for arbitrary checkpoint restore and continuation.

## Minimal integration patch plan

1. Extend the existing `--elimination` parser from `tree|vec` to
   `tree|vec|hierarchical`.  Fail closed unless `--workers 16`, effective
   strategy is exactly `cold`, and effective pivot is exactly `rare`.
   Portfolio, repair, incremental, first, and last modes keep their current
   implementations.

2. Port these dependency-free sibling symbols, replacing fixture `Row` with
   native `Mono` and passing `prime`, `target`, and `workers` explicitly:

   - `Term`, `Equation`, `Record`, and `Basis`;
   - `subtract_mod`, `multiply_mod`, `inverse_mod`, and `sub_scaled`;
   - `Basis::add`, `build_local`, `merge_bases`, and the hierarchical portion
     of `solve_hierarchical`.

3. Add a preparation function beside `sparse_solve_correction`:

   ```text
   sparse_solve_correction_hierarchical(
       sorted_columns, vectors, target, prime, exposed_frequency, workers
   ) -> Option<HashMap<Mono,u64>>
   ```

   It must perform the following exact conversion and include its time in the
   solver timer:

   - collect every non-target row in `exposed_frequency`;
   - sort rows by `(frequency[row], row)`, exactly matching
     `SparsePivot::Rare`;
   - assign dense rare ranks in that order;
   - for each column in existing strict `sorted_columns` order, form the
     augmented equation `non_target_terms = -target_coefficient`, map terms to
     rare ranks, and sort ranks strictly;
   - retain `rows_by_rank` for the final conversion back to `Mono`.

4. Partition the equation vector into 16 balanced contiguous intervals using
   quotient/remainder division.  Each thread calls `Basis::add` in its original
   interval order and returns either a normalized augmented echelon basis or
   local inconsistency.

5. Merge results deterministically in the fixed tree `16 -> 8 -> 4 -> 2 -> 1`.
   At each pair, retain the left basis and add right-basis rows in ascending
   rare-pivot order.  Any zero row with nonzero RHS is an exact inconsistency.
   Do not use hash-map iteration order to select or merge pivots.

6. Backsolve final pivots in descending rare-rank order with every free
   variable fixed to zero.  Reinsert `(target,1)`, omit zero values, and convert
   ranks back through `rows_by_rank`.

7. Before returning, keep the native full `sparse_pairing` verification over
   every exposed column.  During the first integration control, also run the
   current sequential cold/rare solver and require exact candidate-map equality
   before enabling single-path use.  If equality ever fails, do not compare
   support alone: disable promotion and compute the actual next frontier before
   accepting either candidate.

8. Hook this function only where the native loop currently invokes the cold,
   rare, non-incremental solve.  Leave `sparse_read_checkpoint`,
   `sparse_write_checkpoint`, `sparse_read_vectors`, and
   `sparse_write_vectors` byte-for-byte unchanged.  Therefore arbitrary native
   checkpoints and vector caches remain resumable and new accepted states use
   the identical existing persistence schemas.

## What is and is not supported

- Supported after the above integration: arbitrary restored native checkpoint
  states, followed by fixed single-strategy **cold/rare** rounds with 16
  workers; exact existing checkpoint/vector-cache schemas.
- Not supported by the tested kernel: repair bases, portfolio pivot comparison,
  incremental epochs, first/last pivots, or non-power-of-two worker trees.
- This gate proves byte identity at round 660.  The fixed total pivot order and
  pairwise row-space-preserving merges imply the same pivot set and free-zero
  solution mathematically, but every production round must still retain the
  full exposed-column verification and resource gates.

## First integrated control command

Use a distinct copy of the round-660 checkpoint/vector cache and the native
outer command, changing only `--elimination hierarchical`; keep `--pivot rare`,
`--strategy cold`, `--incremental no`, `--workers 16`, `--round-cap 660`,
`--wall-seconds 120`, and `--rss-gib 8`.  This must be a solve-only replay of
the already exposed state, not a round-661 continuation.  Require the emitted
checkpoint SHA-256 to remain
`92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155`
before enabling any later round.
