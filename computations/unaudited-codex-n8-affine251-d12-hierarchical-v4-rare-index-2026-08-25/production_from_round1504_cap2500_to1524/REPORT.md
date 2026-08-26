# D12 v4.1 production: round 1504 to 1524

Verdict: **PASS_PRODUCER_HELD_FOR_INDEPENDENT_AUDIT**.

Eight accepted stages cover exactly rounds 1505–1524. Block A (1505–1516) used native90/wrapper115 and totals 423.732552 seconds. Cache restore then exhausted native90: one three-round attempt failed closed and one later run returned an atomic identity with zero coverage. Both are preserved and excluded. With explicit approval, Block B (1517–1524) changed only the resource gate to native120/wrapper150 and totals 330.441382 seconds. Frozen algebraic source/binary, cold/rare hierarchical mode, 16 workers, nonincremental setting, prime, and 2.5m column cap never changed.

Final round 1524 has 2,379,326 columns and support 3,484. Checkpoint SHA-256 is `376f83253a3f901f7ae565d8ded6cb31c9758203ef9a7a91657cd3d3b65501a0`; cache SHA-256 is `6a3aa33a4706beac36fd4860ccf96e693e56b9cf9eab5a15c66198668821fc07`.

Production is held pending independent accepted-edge descendant audit and full final-cache replay.
