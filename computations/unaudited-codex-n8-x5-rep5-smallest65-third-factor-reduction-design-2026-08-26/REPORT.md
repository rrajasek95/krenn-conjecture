# Rep5 smallest-65 third factor reduction design

This exact-Q, design-only package continues the sealed strict-zero lineage from source SHA-256 `4cd663b6...`. It runs no Singular process and adds no closure claim.

The input has 65 variables, 3,483 generators, and 128,231 terms. Its grading has full rank 65 (nullity zero), its exact constant-linear rank is 38, it has no inactive or affine/monic coordinate, and its incidence graph is one 65-coordinate component.

The exhaustive coordinate-factor census finds 32 candidates. The maximum count is 162; the frozen objective selects `a24_10`. The exact `D(a24_10) union V(a24_10)` cover reconstructs to `66/3484/128233` and `64/3321/118979`. The latter is strictly smaller in variables, generators, terms, and degree mass. Forward and reverse identities are independently reconstructed.

All 42 available literal 2x2 minors and three complete 3x3 determinants were checked: none matches or divides a generator. This is not an ideal- or radical-membership test and does not exclude deeper rank reductions.

The authoritative three-guard-chart, nine-stratum coverage statement and its independent referee are hash-pinned. This package refines only one local descendant branch; it neither discards the other eight strata nor promotes global rep5 closure. Twenty hostile mutations fail closed.
