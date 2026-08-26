# K22 hidden decorated-pair two-sink fold: gated readiness report

Status: `PASS_COMPLETE_THREE_SHARDS_MERGED_AND_REFEREED`.

The final compiled consumer performs one logical, disjoint scan of the retained
`H16ORM1` decorated `(K16 parent,p2)` ledger and keeps two strictly separate
scalar sinks:

* `D14:222|R:2-3-3`: 32 K3 tails, every pivotable K19 pivot with exact third
  division, then 32 terminal K3 tails.
* `D14:222|R:2-4-2`: 60 K4 tails, every pivotable K20 pivot with exact third
  division, then 12 terminal K2 tails.

No K19, K20, or K22 row stream is emitted. The only row-bearing output is the
explicit 257-record literal audit ledger requested by the task.

## Exact guards

For every decorated input record the consumer validates row ordering, selected
pivot availability, orbit-stabilizer product 384, nonzero weight, and the exact
H16ORM1 header. For every continued intermediate it asserts
`U % (m2*m3) == 0` and `w2 % m3 == 0`, then uses `w3=-w2/m3`. Every realized
cached terminal response key is exhaustively expanded and every K22 child
signature is asserted nonpivotable before `full=irreducible`. Literal samples
independently build rows and require abstract/literal 77-cycle keys to agree.

The input ledger is pinned to SHA-256
`22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8`,
101,545,723 records of 53 bytes plus the 80-byte header. The auxiliary K4 table
is `4cec01e1...c35aa3` and the cycle table is `8213a3cb...d2397fc7`.

## Gates and bounded production plan

Both final-source prefixes passed:

* 4,096 records: completed; all 257 literal checks passed.
* 1,000,000 records with 8 workers: 5.956137 seconds. The R233/R242 literal
  ledgers contained 257/257 and 244/257 nonzero continuations, respectively.
  The full single-process projection is 604.820268 seconds, just outside the
  hard 600-second gate.

Production ran as three sequential exact intervals
`[0,33848574)`, `[33848574,67697148)`, and `[67697148,101545723)`, projected at
about 202 seconds each. Their actual walls were 186.193677, 47.335927, and
53.086846 seconds; the maximum was safely below 600 seconds. Each shard passed
`--global-samples`; the strict merger
requires their union to be exactly the 257 globally spaced indices. It also
rehashed the 5.0 GiB source and passed contiguous coverage plus every
mass/count/divisor/cache/terminal identity.

The response caches clear every 100,000 input records and additionally have a
hard 300,000-key cap per worker per sink. Observed 1M peaks were 270,524 and
204,404 keys. Direct RSS telemetry was unavailable because macOS process
introspection is sandbox-blocked; the hard key cap keeps the two-cache layout
comfortably inside the 16 GiB gate.

## Exact result

The strict merged result is
`results_hidden_pair_k22_charge.json`, SHA-256
`8dbe7573056067e8ae0d34ca126984e88fc5c00bc51cfa9d79a77439c0a98ce3`.

* `D14:222|R:2-3-3`: scaled charge
  `1049736142077535125504`, reduced charge
  `455614644998930176/173867925`; 3,249,463,136 first K3 evaluations,
  1,067,611,872 pivotable K19 children, 1,774,721,368 selected pivots, and
  56,791,083,776 terminal K3 occurrences.
* `D14:222|R:2-4-2`: scaled charge `26058341013666103296`, reduced charge
  `146883686269312/2258025`; 6,092,743,380 first K4 evaluations,
  1,011,364,980 pivotable K20 children/selected pivots, and 12,136,379,760
  terminal K2 occurrences.

Both sinks have `full=irreducible`. The global literal ledger has exactly 257
records and includes 212 nonzero R233 and 42 nonzero R242 continuations. The
independent source/count/hash/sample referee passed at
`results_hidden_pair_independent_referee.json`, SHA-256
`e428846ba3fa8e310405b754a1b2eb8fbf05c2a18b74f86223c67e98b23c4f45`.
The two-entry `k22_manifest_hidden_pair2_partial.json` also passed the frozen
strict assembler in partial-audit mode: exactly two covered IDs, no duplicates
or extras, and the expected 74 IDs still missing from this fragment alone.

## Reproduction

Compile:

```sh
rustc --edition=2021 --cfg 'feature="hidden_child_prefix"' --cfg 'feature="full_hidden_charge"' -C opt-level=3 -C target-cpu=native computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/run_k22_hidden_pair_fold.rs -o computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/run_k22_hidden_pair_fold
```

The completed run used the three intervals sequentially with 8 workers,
`--global-samples`, and the exact bounds in `full_shard_plan.json`; its strict
merge command was:

```sh
python3 computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/merge_k22_hidden_pair_shards.py --output computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/results_hidden_pair_k22_charge.json computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/results_shard_000.json computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/results_shard_001.json computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/results_shard_002.json
```

This package computes only the two named K22 charges. It makes no K23 claim,
residual claim, membership claim, or conjecture verdict.
