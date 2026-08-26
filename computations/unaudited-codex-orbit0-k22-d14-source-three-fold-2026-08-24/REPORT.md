# K22 D14 source-three scalar fold

Status: `PASS_COMPLETE_AND_INDEPENDENTLY_REFEREED` for exactly
`D14:222|R:3-2-3`, `D14:222|R:3-3-2`, and `D14:222|R:4-2-2`.

## Exact results

At `U = 400591699200`:

| lineage | scaled charge | reduced exact charge | terminal occurrences |
|---|---:|---:|---:|
| `D14:222|R:3-2-3` | `964781571518500995072` | `12689151561428096/5268725` | 162,413,199,360 |
| `D14:222|R:3-3-2` | `196633985739550064640` | `517240071915904/1053745` | 32,253,788,160 |
| `D14:222|R:4-2-2` | `16769984550131957760` | `2700793739392/64515` | 16,504,588,800 |

Full and irreducible occurrences and charges agree individually for all three
sinks. The authoritative result is `results_k22_d14_source_three.json`,
SHA-256 `99bec5f72757b20449aff9d7869669e36faab0f61411d482eab13d7523a562cc`.

## Source-linear computation

One scan of all 485 frozen orbit0 records rebuilds all 838,080 literal D14
heads. The three response schedules are kept degree-separated:

* R323: K3 to K17, K2 to K19, terminal K3.
* R332: K3 to K17, K3 to K20, terminal K2.
* R422: K4 to K18, K2 to K20, terminal K2.

Each source head and both of its preterminal rows are literal. Signature caches
only retain tail/pivot plans. Exact row deduplication is confined to one source
head, and compression starts only at the terminal complete key
`(profile,signature,pivot,degree)`. No K17/K18/K19/K20/K22 row file is emitted.

The direct D14 coefficient is `-M`. Three recurrence responses flip the sign
three times, so the terminal coefficient is `+M/(m1*m2*m3)`. The evaluator
asserts `U % (m1*m2*m3) == 0` at every realized path. Every cached response is
expanded on its first occurrence and every K22 child is asserted nonpivotable
before full is identified with irreducible.

## Literal referee

The producer exported 257 distributed literal witnesses per sink, 771 total.
The independent referee rebuilt every sampled source head and both intermediate
rows, rechecked all three pivots and denominators, and literally constructed
and charged 14,392 terminal K22 children. All were nonpivotable and every
literal terminal charge equaled its compressed producer response.

The referee result is `results_k22_d14_source_three_audit.json`, SHA-256
`2e56e70e2fc6a1545c3f28e82b8a2b219727ad480f9de512d17d07d5f5a806d5`,
with logical SHA-256
`6bf869754ae7a8e67758f16ad3be4a2c383566d2943693711ab8a1be526b2b8b`.

## Resource gates

Representative globally distributed gates passed as follows:

| records | wall seconds | projected full seconds | peak cache keys/worker |
|---:|---:|---:|---:|
| 8 | 8.365320 | 507.147500 | 866,918 |
| 32 | 25.570492 | 387.552762 | 2,445,956 |
| 64 | 56.566792 | 428.670220 | 2,933,454 |

The terminal cache has a hard cap of 3,000,000 keys per worker. The full
8-worker run finished in 357.888906 seconds, below the hard 600-second gate,
with producer peak 2,993,326 keys per worker. External live snapshots at 37
and 90 seconds showed stable RSS of 4,407,424 and 4,407,520 KiB (about 4.20
GiB), below 16 GiB.

## Scope

`k22_manifest_d14_source_three_partial.json` supplies three singleton scalar
groups for the frozen strict 76-ID assembler. This package does not claim the
other 73 K22 IDs, K23, membership, a residual, or a conjecture verdict.
