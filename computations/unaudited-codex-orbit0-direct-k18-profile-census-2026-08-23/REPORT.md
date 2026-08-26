# Direct K18 six-lineage enriched-profile census

## Verdict

**PASS, complete for the direct K18 stream only.**  All 152,251,200 direct
K18 parents were enumerated in 16 atomic source-record intervals; exactly
137,817,600 are K0-pivotable.  Their 260,736,000 outgoing pivot uses compress
to 979,091 nonzero signed enriched profiles.  The construction, merge, and an
independent full-checkpoint replay all finished far below the 300 s / 12 GB
gate.

This packet covers the six direct K18-to-K20 lineages
`244|2`, `424|2`, `442|2`, `433|2`, `343|2`, and `334|2`.  It does **not**
cover the K14-, K15-, or K16-derived K18 parent streams.

## Exact census

| lineage | full parents | pivotable parents | outgoing pivot uses |
|---|---:|---:|---:|
| `D18:244|R:2` | 20,952,000 | 17,460,000 | 24,444,000 |
| `D18:424|R:2` | 20,952,000 | 20,952,000 | 62,856,000 |
| `D18:442|R:2` | 20,952,000 | 17,460,000 | 24,444,000 |
| `D18:433|R:2` | 29,798,400 | 29,798,400 | 55,872,000 |
| `D18:343|R:2` | 29,798,400 | 22,348,800 | 37,248,000 |
| `D18:334|R:2` | 29,798,400 | 29,798,400 | 55,872,000 |
| **total** | **152,251,200** | **137,817,600** | **260,736,000** |

The 16 atomic outputs contain 6,995,702 nonzero keys before the external
merge.  The merge leaves 979,091 keys and records 27,831 cross-run exact-zero
keys.  The signed coefficient sum at the fixed global scale
`U=400591699200` is

`-2655476097643708416000`.

The atomic files occupy 503,694,640 bytes and the merged checkpoint occupies
70,494,808 bytes.  Relative to pivotable parents the merged support is a
140.76x compression; relative to outgoing uses it is a 266.30x compression.

## Enriched key and sufficiency

Each 72-byte record stores

`lineage(1), path/cycle profile(29), anchor signature(12), outgoing pivot(1), signed weight i128(16), uses u64(8), literal witness (ri u16 + three factor indices)`.

The profile, signature, and pivot determine the twelve K2 response charges
and their K0-pivotability, while the witness reconstructs a literal source
parent and was replayed against every merged key.  Thus the packet is
sufficient for exact occurrencewise **signed charge** evaluation without
re-enumerating 137.8 million parents.  Exact-zero signed profiles are omitted;
therefore the retained `uses` field is not a census of all cancelling literal
occurrences.  This does not affect linear full or irreducible charge.

Because the compressed tail pass was only `979091 * 12 = 11,749,092` literal
evaluations, it was completed inside the same gate (3.69 s):

| quantity | scaled by U | unscaled |
|---|---:|---:|
| full K20 charge from direct6 | 156,805,717,532,560,588,800 | 391,435,264 |
| irreducible K20 charge from direct6 | 160,750,257,466,775,961,600 | 401,282,048 |

These are the aggregate of the six direct lineages only, not a complete K20
charge.

## Replay and artifacts

- Builder/evaluator: `run_direct_k18_profile_census.rs`
- Merged checkpoint: `direct_k18_enriched_profiles.bin`
- Census result: `results_direct_k18_profile_census.json`
- K2 charge result: `results_direct_k18_k2_charge.json`
- Independent replay: `audit_direct_k18_profile_census.py`
- Replay result and per-run hash manifest:
  `results_direct_k18_profile_census_replay.json`

Pinned SHA-256 values:

- source: `a3d1b2d81ccef45870409d28e255be09e784e44347d673ff245103bd80eff9c2`
- merged checkpoint: `d77f2a84f220aad9f52fe81547ab730a6b834005b27e6f47172bb80cf5850da2`
- census result: `325c873857d27230797ea86a2b0c5f5a8b986b66dbaad1def315eec42374c967`
- charge result: `82a5c213cb916523386f524242c8a5aba0e32dd91291d0f5c017de268b1541ad`
- replay script: `3a65c49b7bb92449880f10f5881fed879fed100fbc38695cb81fa5aae64e65d5`
- replay result: `3d3a0c0c6dd534ba22b1fffd1b41ff3a28929011be22b15d6f223d590aa7eeae`

The replay checks all 16 interval headers and coverage `[0,485)`, exact sizes,
all file digests, merged strict key order, every merged nonzero weight, total
weight/uses/counts, and the twelve-tail count.  A hostile `+1` mutation of one
stored signed weight fails the pinned total-sum guard.
