# D12 v4.1 short production: round 1464 to 1484

Verdict: **PASS_PRODUCER_HELD_FOR_INDEPENDENT_AUDIT**.

Starting from the independently accepted 2.5m-cap round-1464 state, five atomic cold/rare hierarchical stages cover exactly rounds 1465–1484 with no gap or overlap. All watchdogs passed under 36 GiB. Aggregate watchdog time is 474.920176 seconds, below 540 seconds; maximum observed RSS is 25,372,336 KiB.

The final round-1484 state has 2,142,848 exposed columns and support 2,483. Its checkpoint SHA-256 is `2aa00dfd9e170aece91aa92321f3629f11a35afce43020452ec561dbf6ef7ac3`; its cache SHA-256 is `4006f4d68afa7ad39d42d594757bc24a8a35d77f0dc9a4965d167a1b83d912bc`.

Production is held at the requested short target. Continuation requires the assigned independent five-edge audit and storage compaction.
