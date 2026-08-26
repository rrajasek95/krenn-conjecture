# Terminal K23 direct-K15 referee and 59-ID assembly

Status: **PASS**. All eight sealed production shards independently validate and form the exact no-gap interval partition `[0,485)`. The merged direct-K15 fragment contains four source-group scalars covering exactly the final 12 frozen K23 lineage IDs; packet labels `223/232/322` remain provenance labels and no unsupported individual scalar split was made.

The four scaled-by-`U` scalars, where `U = 400591699200`, are:

- `source_D15_R2_2_4`: `-404178265395076423680`
- `source_D15_R2_3_3`: `-585607827895067197440`
- `source_D15_R3_2_3`: `-573237209819205550080`
- `source_D15_R4_4`: `-109207097269561589760`

Their grouped subtotal is `-1672230400378910760960/U = -13196262629252768/3161235`. Full and irreducible charges agree for every sink. The merged result SHA-256 is `f7aa14df90a5a9b21a958e0d7d3f816865bf38efc64dbc68ba265402b76f321c`; the strict fragment SHA-256 is `7b16c53e372282a02aaa054fcd1abc3bf45159c2e9c190ab7d1ed47ca6ec10b5`.

The independent final referee recomputed all eight interval sums, source census, count arrays, denominator histograms, charges, exact rational rendering, and group-once semantics. It also replayed every row of the pinned cache-free literal evidence: 257 distributed nonzero sources, four sinks per source, 1,028 witness rows, exact signed-`U` divisions, packet counts `86/86/85` per sink, and terminal K23 children of anchor-signature mass 1. Its result SHA-256 is `90ff932ff39ace3f54707061276d8b21f4f23232a8ae15422006c6add1deae22` and logical SHA-256 is `8a3de5cfc7c45547469a597c1a4aa119bd895592dfc8720cf4a02864c0038f7d`.

One metadata-only bug was found: the sealed v1 merger summed the eight shard elapsed times and incorrectly submitted that aggregate to the single-run `<600s` gate. No shard or scalar was implicated. The sealed v1 interface remains unchanged; `merge_k23_direct_k15_shards_aggregate_v2.py` uses a distinct aggregate schema, proves every atomic shard is below 600 seconds, records sum `1677.178122s` and maximum `223.747247s`, and hostile-tests that aggregate-as-single-run is rejected.

Adding this 12-ID fragment to the pinned 47/59 baseline passes the frozen strict assembler and its hostile tests: K23 is complete at 59/59 IDs and 17/17 source groups, with no missing, duplicate, extra, regrouped, or reordered IDs. The exact K23 charge is

`full = irreducible = -6917513329639204282368/U = -428913276887351456/24838275`.

This closes the exact K23 charge interface only. It is not a K24 residual/span result and is not by itself a proof or disproof of the conjecture.
