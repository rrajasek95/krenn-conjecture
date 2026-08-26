# K24 grouped K16 R2-2-4 two-half readiness

Status: `READY_CONDITIONAL_SEQUENTIAL_TWO_HALVES`; this schedule audit launched no R2-2-4 production.

The strict grouped sink contains exactly the six frozen IDs `D16:{224,233,242,323,332,422}|R:2-2-4`.  The retained K16 checkpoint has no packet labels, so the six IDs must be charged once as one grouped scalar; individual packet charges are not reconstructable from this interface.

The frozen intervals are `[0,12048547)` and `[12048547,24097095)`.  They are contiguous, disjoint, and their lengths sum to the declared 24,097,095 records.  The 262,144-record distributed gate took 6.982861 seconds, giving 320.943190 and 320.943216 second linear projections for the halves.  Each half must run alone under `gtimeout 540`, with live RSS checks at 60 and 120 seconds and an abort threshold of 15 GiB.  The distributed gate does not itself certify contiguous-half RSS.

Commands, from the repository root, after explicit clearance:

```text
/usr/local/bin/gtimeout 540 computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/run_k24_charge_k16_r224 --start-record 0 --count-records 12048547 --workers 8 --output computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_shard0.json
/usr/local/bin/gtimeout 540 computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/run_k24_charge_k16_r224 --start-record 12048547 --count-records 12048548 --workers 8 --output computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_shard1.json
```

Validate each shard structurally before launching the next.  The merger accepts only those two exact non-distributed intervals, sums all source/count/histogram/cache/scalar fields, enforces the frozen full-source pins, and requires the union of shard ledgers to cover all 257 global source-index bins.  For the shared bin it deterministically retains the lowest record index.  Acceptance additionally requires the independent Rust referee to replay all 257 merged witnesses from the checkpoint through both K2 pivots and terminal K4, checking rows, pivot availability and multiplicities, `-U/(m1*m2*m3)`, terminal charge, and signed contribution.

The bounded 257-witness gate replay passed, and eleven hostile tests passed, including distributed-as-contiguous rejection in standard, optimized, and isolated Python modes plus mutations of source row, both intermediate rows, all three pivots, and the unit sign.  Exact pins and the merge commands are machine-readable in `results_k16_r224_two_half_schedule_audit.json`; hashes are frozen in `K16_R224_TWO_HALF_MANIFEST.sha256`.
