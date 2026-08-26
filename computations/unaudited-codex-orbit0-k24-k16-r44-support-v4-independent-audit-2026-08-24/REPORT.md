# Independent K24 K16 R4-4 support-v4 audit

Verdict: **ACCEPT one full relaunch after resource clearance and explicit approval.** This package launched no production computation.

The final producer source, binary, bounded control, input checkpoint, frozen 257-candidate ledger, validator, and literal-referee reports are hash-pinned by `audit_support_v4.py`. The v4 bounded run is scalar-identical to the old bounded run across all 29 recurrence/scalar fields and reports a positive nonzero-support histogram on exactly global bins 0 through 36, with zero positive support outside that set.

The independent replay checks all 257 distinct frozen candidate slots and record indices, exact global-bin formula, the 7/6 per-bin quota, and nonzero terminal charge. It also checks the seven candidates realized by the distributed control against the frozen rows and pins the separate exact literal replays of all 257 candidates. The upstream hostile suite has 18 passing cases under standard, optimized, and isolated Python modes.

Fail-closed ordering was checked directly in the pinned Rust source: the full-run exact support-key assertion and the `257`-sample assertion both precede the atomic sample-ledger write, which precedes the atomic result write. Thus no scalar/result can be accepted if support is outside bins 0..36, a realized bin is missing, or a frozen candidate fails to materialize.

The accepted command is recorded in the result JSON. Its bounded gate projects 364.809229 seconds, below the 600-second wall gate; the separate production contract retains the 16 GiB RSS ceiling. A distinct output path is required, and the historical failed attempt must never be recovered or overwritten.
