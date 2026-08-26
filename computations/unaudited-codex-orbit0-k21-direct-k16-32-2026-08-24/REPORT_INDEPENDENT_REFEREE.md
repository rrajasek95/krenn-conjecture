# Independent grouped D16 R:3-2 K21 referee

Status: `PASS_INDEPENDENT_GROUPED_SIX_D16_R_3_2_K21_TERMINAL_REFEREE`.

The original package manifest replays exactly. Its producer, result, and
manifest SHA-256 values are respectively `b4f0c4ae64d2d29d1febb2bd6beb4b2e745f944701404620c41cd591d781f73a`,
`92a6a9a27dbf0fc3c82f1dd6b71155cf81118f5e1bf9ff7b1fbb38ab313793ca`,
and `7c4e12c74af5ab0c376dd880b2100c8aca233b08fe28d50fbba4ee709a607a8a`.

Exactly the six IDs `D16:{224,233,242,323,332,422}|R:3-2` are covered.
Full equals irreducible charge is
`-643522419678967234560/U = -618475450368/385`. Counts, both response signs,
every observed `U/(m1*m2)` division, histogram totals, and cache-query identity
pass independently. Missing, duplicate, and reordered ID interfaces fail.

The producer's earlier sample audit stopped at first-pivot availability. This
referee additionally replayed all 91 nonzero witnesses in its distributed
257-record grid, spanning checkpoint indices 0 through 24,002,964. It followed
2,912 K3 tails to 1,264 pivotable K19 children, 1,336 second pivots, and 16,032
literal K21 children. Every continuation count and per-source charge matches
the producer ledger; every K21 signature is terminal and its literal cycle
charge is recomputed.

No full producer replay was performed. Scope remains the grouped six-ID scalar;
the source checkpoint has no packet labels, so individual-ID values are not
authorized and no other K21 path is inferred.
