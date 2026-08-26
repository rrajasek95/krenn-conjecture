# Round 849 to 850 rare-order benchmark result

The frozen read-only gate passes. Complete baseline and incremental order vectors agree at both states: 27,357,752 round-849 rows hash to `8c2bdb66...`, and 27,392,895 round-850 rows hash to `71429998...` under both constructions.

Round 850 changes 74,482 rows across 16 frequency buckets. Incremental commit plus flatten took 0.242379 seconds versus 1.234000 seconds for the existing full sort, a 5.0912x order-phase speedup. The complete gate used 15.204 seconds wall and peaked at 3,741,824 KiB, far below 120 seconds/36 GiB.

The accepted portfolio and fixed cold/rare artifacts were independently rehashed after the gate: both checkpoints are `c2ea7cc0...` and both vector caches are `df181c0b...`. This is an accepted-state byte-identity guard, not a claim that the order-only gate emitted new state; it wrote neither checkpoint nor cache.

The index is promotable to a cloned-source integration replay. Production promotion remains fail-closed on one final guard: the integrated sibling must reproduce checkpoint `c2ea7cc0...` and cache `df181c0b...` for exactly round 849 to 850 before the production source is edited.
