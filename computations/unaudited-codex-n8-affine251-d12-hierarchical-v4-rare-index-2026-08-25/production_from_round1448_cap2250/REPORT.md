# D12 v4.1 round 1448 to 1463 producer report

Verdict: **PASS_PRODUCER_HELD_FOR_INDEPENDENT_AUDIT**.

Starting from the independently accepted 2.25m-cap round-1448 state, four atomic v4.1 cold/rare hierarchical stages cover exactly rounds 1449–1463 with no gap or overlap. All watchdogs passed under the 36 GiB cap. Aggregate watchdog time is 377.318548 seconds, below the 540-second block limit; observed peak RSS is 24,813,808 KiB.

The final round-1463 state has 2,049,529 exposed columns and support 2,389. Its checkpoint SHA-256 is `1b4dde9f009b4343099190e293913818b3df88dfc34c27653e7cfcd4acf08c8e`; its vector-cache SHA-256 is `46744c37b6c1ab30e6ce945a9f049e45683b4324470e661554f4ae4134b9d48c`.

Production is held. Continuation requires the assigned independent four-edge descendant audit and a full final-cache annihilation replay.
