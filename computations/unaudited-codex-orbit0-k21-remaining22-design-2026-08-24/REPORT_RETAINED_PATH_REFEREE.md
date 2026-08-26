# Retained-path K21 referee

Status: `PASS_INDEPENDENT_TERMINAL_REFEREE_D14_222_R_2_2_3_K21_CHARGE`.

The strict singleton `D14:222|R:2-2-3` contributes full = irreducible scaled
charge `-1965744419617576058880` at `U=400591699200`, hence the reduced exact
scalar `-511912609275410432/104320755`. The current producer source is pinned
at SHA-256 `3a9d6f821e72d9782311b3e96378134df203099f3ef04d4c9f4b741d07c7062a`
and its current result at
`3bff6d8b0bcb7fc2c3508ab69f18d8df60f5d5ffa0aead0db33d3b40c677313d`.

The referee checked the complete 33-group `(m2,m3)` ledger: 158,439,965
parents, 399,275,484 selected third pivots, 12,776,815,488 K3 children, all
`U mod (m2*m3)=0`, and the exact group charge sum. It also checked the third
response sign `w3=-w2/m3`, the unweighted response cache keyed by
`(profile29,signature12,pivot)`, and the identities misses = 5,173,958 =
distinct keys and hits + misses = selected pivots.

Terminality is universal: every K18 parent has anchor sum 6, every one of the
78 K0 pivot signatures consumes 4, and all 78 families x 32 K3 tails restore
1, so every K21 child has sum 3 and cannot contain a K0 pivot. Independently,
257 evenly distributed checkpoint records (including both endpoints) replayed
their retained witness to the canonical K18 parent, then checked all 677
third-pivot responses and 21,664 literal children: every child signature was
terminal and every literal charge key equalled its abstract cache key.

The exact 80-byte `H18PIV2` header, file length, prior frozen input digest and
prior full-input referee were pinned. Missing, duplicate, and adjacent lineage
IDs fail the strict singleton guard. Scope excludes a second 158,439,965-row
pass and excludes inference to any of the other 21 missing K21 paths.
