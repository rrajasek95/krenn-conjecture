# Direct round-1464 column-cap gate

Verdict: **PASS_EXACT_DIRECT_CAP_EXTENSION_EQUIVALENCE**. No continuation was launched.

The prior external sequential portfolio lane is excluded: its repair-first lane exceeded 330 seconds, produced no result, and was sealed fail-closed. This gate instead ran two sequential direct cold/rare hierarchical continuations from the independently accepted round-1463 checkpoint/cache (`1b4dde9f…` / `46744c37…`). Both used frozen v4.1 source/binary, 16 workers, nonincremental mode, native wall 120 seconds, the sealed <=155-second watchdog at wrapper wall 150 seconds, and a 36 GiB live RSS cap.

The control used cap 2,250,000 and the candidate cap 2,500,000. Both stopped exactly at round 1464 with 2,054,273 exposed columns, support 2,427, 4,744 new columns, and 1,301 new support rows. Their checkpoints are byte-identical at SHA-256 `0191363f5da4b5b74945dd48a51954195200957996c5d3ff43c5242c37a7c64f`; their caches are byte-identical at `9bb1b64f80def9014f0b031f4683da5bf00354b331cf2bc0541672ce02d67b29`.

After removing path and timing fields, the exact result difference is the singleton `column_cap`; removing it makes the semantic objects identical. In-memory changed-round and non-atomic-watchdog hostiles are rejected.

Telemetry:

- control: native 57.937126 seconds; watchdog 58.458481 seconds; peak RSS 23,890,368 KiB; atomic PASS
- candidate: native 56.382257 seconds; watchdog 56.897594 seconds; peak RSS 23,676,880 KiB; atomic PASS

The candidate remains held pending the assigned independent light audit.
