# K24 factorized direct-D17/D18 bounded producer

## Outcome

The optimized one-source-record prefix is exact as a **raw top-map `T` column ledger** for the strict 13 K24 lineages. It emits weighted H-column orbits, not K24 rows. The accepted prefix has 2,212,864 selected second-pivot occurrences, 2,165,760 nonzero H-column orbits, and 132,771,840 logically represented terminal K24 occurrences. All 2,165,760 TSV records were independently reread for sorting, hashes, the U24 lattice, H-orbit size, and exact `alpha = W/orbit_size`. Its 257 distributed literal witnesses replay the two pivots, exact divisor tuple, signed coefficient, one literal K24 output, 60-output fan, charge, self-pairing 60, and terminality.

This is not yet a sufficient relative K24 interface. The terminal map needed downstream is `A24_rel = T|ker(L)`: the package contains neither the lower map `L`/kernel restriction nor an exact lower-correction certificate. Consequently raw top columns cannot by themselves certify a relative residual or span. Prefix8 and every production interval remain blocked independently of compute resources. There is no complete K24 residual, relative-column, span, or conjecture claim.

## Exact source fold

The two sinks are kept separate throughout:

- `source_D17_R3_4`: seven IDs, 1,736,704 selected second pivots for source record 0;
- `source_D18_R2_4`: six IDs, 476,160 selected second pivots for source record 0.

For each literal source head, the engine selects every first pivot, emits every literal K3 or K2 first tail required by the frozen recurrence path, and then selects every second pivot of the intermediate K20 row. If the source orbit record has mass `m`, and the two literal divisor counts are `m1,m2`, the stored scaled column occurrence is exactly

`-m * U24/(m1*m2)`, with `U24 = 400591699200`.

The engine asserts the division before emitting. Its factor record is the mixed word together with the sorted degree-20 multiplier and an i128 scaled mass; the raw logical size is 37 bytes. No terminal row is written. The retained TSV has exactly

`canonical_column_key, orbit_size, W_num, W_den, alpha_num, alpha_den`,

where `W` is the collected orbit-total mass and `alpha=W/orbit_size`. Every division is exact.

## H collection and corrected ordering referee

The original exact producer checked all 384 actions per column. The optimized producer uses a proved orbit-fibre decomposition. First choose the minimum image of the mixed word in natural tuple order. The actions landing over that word form a stabilizer coset. Distinct multiplier images in that fibre give both the natural minimum pair and, after multiplication by the word-orbit size, the exact pair-orbit size.

For 72 of the 78 mixed words the minimum-word fibre has 32 actions and word orbit 12. The other six have 128 actions and word orbit 3. Thus the kernel examines 39.384615 actions on average instead of 384, a 9.75-fold action reduction.

An apparent ordering discrepancy was investigated and closed. The frozen structure maps and pinned provider transformations are the identical 384-element set. The provider caches its orbit using textual `repr` ordering, while the producer uses natural `(word tuple, multiplier bytes)` ordering. On the 257 distributed columns, every producer representative lies in the provider orbit, equals the natural minimum, and has the provider orbit size. There are 228 cases where provider-`repr` and natural minima differ; the audit treats substituting `repr` order as a hostile mutation.

## Byte equivalence and performance

The brute prefix used source SHA256 `e7843511acbb4c9fb5e64870f5a9722c418bcf8d39e62ac8c04e0cc9eea82453`. The optimized source is `a83376d4e68828e3b3f0af5c6ae9895bfda0db979a81ee35d5f87d48a8c5d47f`.

The following optimized outputs are byte-identical to the brute 384-action outputs:

- both group `compact/.../final.bin` files;
- both group TSVs;
- all 257 literal witnesses.

The result JSONs are identical after excluding only engine identity, cache diagnostics, timing diagnostics, and the containing directory prefix. Content hashes, exact counts, masses, charges, signs, U24, orbit histograms, and scope all match.

The brute prefix took 159.893838 seconds, of which 122.080710 seconds were exact labelled merge/H collection. The optimized prefix took 47.647184 seconds, with 7.806453 seconds in that phase: 3.356-fold end-to-end and 15.638-fold H-phase speedups. Both retained exactly 472,229,094 bytes before their atomic result.

Materializing the 60 rows per factor record would use 5,310,873,600 logical bytes for this prefix. Factorized raw records use 81,875,968 bytes, a 64.865-fold logical reduction. The entire retained working tree is an 11.246-fold reduction. After independent acceptance, the required retained core—two compact binaries, two TSVs, result, and witnesses—is 227,504,853 bytes.

## On-demand checks and exact charges

For every final nonzero H-column orbit, the producer reconstructs exactly the 60 K4 top outputs without storing them. It asserts 60 distinct rows, terminality of every row, literal self-pairing 60, row mass `60W`, and the column's exact terminal charge sum. Summing those checks gives prefix charges

- D17 R3-4: `14426112/7`;
- D18 R2-4: `-212992`.

“Pairing” here is the exact labelled top-column self-pairing check. It is not a claim that the global K24 Gram component or target span has been built.

## Fail-closed result schema

The earlier gate schema SHA256 `dd93eab99a72b9464ef35f3793d0068fdd86842fa2da33da9b02b986cf3e3dbe` is preserved as design provenance but explicitly superseded for producer-result validation. It omitted producer result fields while forbidding extras and assigned the wrong type to `literal_samples`.

`factorized_k24_bounded_result.schema.json` closes the actual prefix1/prefix8 result shape. `validate_k24_factorized_bounded_result.py` locks its required/property keysets to the executable validator and rereads all content. The positive optimized prefix passes. Hostile tests reject a wrong `literal_samples` type, an extra property, a missing property, a wrong engine hash, and an inexact orbit division.

## Prefix8 gate and restartable full schedule

Prefix8 is computationally designed but mathematically blocked. Its exact command and resource gates remain frozen only as provenance in `prefix8_and_restartable_merge_plan.json`. Linear prefix1 projections are 381.177472 seconds, 3,777,832,752 retained bytes, and 655,007,744 raw logical bytes. No clearance may launch it until a source-faithful `T|ker(L)` producer or an independently checked exact lower-correction certificate supersedes this raw-top interface.

If prefix8 passes, the restartable production design is 61 no-gap source shards `[8j,min(8(j+1),485))`, not the superseded eight 60/61-record shards. Each shard is accepted independently. The global merge is a sorted exact merge of each group's 39-byte compact records: equal canonical keys must have equal orbit sizes, i128 masses are summed, and only exact zeros are dropped. It must prove the full counts 842,301,440 and 230,937,600, the complete interval bitset, common hashes, and strict 13-ID coverage before deriving its two global TSVs and on-demand checks.

If prefix8 misses any gate, the fallback is 485 one-record atomic intervals. The current producer's `--production-shard` allowlist still contains the superseded large geometry, so production use is forbidden until that allowlist is replaced by the accepted schedule.

## Disk lifecycle

No cleanup is authorized by this package. Before independent per-shard acceptance, retain `raw/`, `raw_compact/`, `canonical/`, `compact/`, both TSVs, result, witnesses, and hashes. After independent PASS and a sealed manifest, delete only that shard's `raw/`, `raw_compact/`, and `canonical/`; retain both compact finals, both TSVs, result, witnesses, validation transcript, and hashes.

The measured retained core is 227,504,853 bytes per source-record prefix; its naive full projection is 110,339,853,705 bytes. Before each launch, require free space at least

`max(16 GiB, remaining_shards * max_accepted_post_cleanup_core_bytes + 8 GiB)`.

This is a restartable operational floor based on the largest accepted core and is recomputed after every shard. A separate explicit authorization is required to remove accepted shard cores, including after a global merge.
