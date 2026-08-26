# Direct-K16/K2 K18-parent exporter optimization plan

## Verdict

**A restartable three-gate full plan is feasible, but no full run was
launched.**  The useful exact optimization is child-signature caching, not a
new orbit quotient: derive each K18 signature by the literal K2 update and
cache `avail(signature)`.  This preserves the audited profile key, signed
coefficient, and reversible source witness exactly.

The authoritative full workload remains:

- 24,097,095 direct-K16 H-orbit checkpoint rows;
- 24,003,767 pivotable source rows and 129,939,187 first-pivot uses;
- 1,559,270,244 generated K18-parent occurrences;
- 807,499,618 pivotable K18-parent occurrences;
- six `D16:{224,233,242,323,332,422}|R:2-2` K20 IDs.

The 62,984,970,204 outgoing-use number is only the exact uncached bound
`78 * 807499618`, not an actual use census.

## Exact optimization

For each checkpoint record `(r,v16)`:

1. Compute `s16=sig(r)`, `P1=avail(s16)`, and `m1=|P1|` once.
2. For each `p1 in P1` and each of its 12 K2 tails, form the literal K18 row
   `r18=replace(r,A_p1,t1)` and derive
   `s18=child_sig(s16,p1,t1)`.
3. Look up `P2=avail(s18)` in a worker-local signature cache; set
   `m2=|P2|`.
4. Emit the unchanged audited key
   `(profile(r18,p2),s18,p2)` with exact weight
   `+v16*U/(m1*m2)` and the literal
   `(r18,source,p1,t1,p2,m1,m2)` witness.

Every `m1*m2 | U` division remains occurrencewise asserted.  Four
deterministic 2,000-row ranges were run through the audited baseline, cached
direct path, and an independent literal-row staging path.  All agreed exactly
on parent counts, outgoing uses, nonzero and zero profile keys, signed weight,
and use count.  The test also asserted
`child_sig(s16,p1,t1) == sig(r18)` literally.

Only 29--159 distinct child signatures occurred per 20,000-row distributed
sample shard.  Therefore the cache removes repeated 24-cell signature scans
and 78-pivot availability scans without quotienting the physical row or
profile.

## Orbit and row-cache guards

The checkpoint already consists of H-orbits.  On 1,024 deterministic rows
spread over eight checkpoint regions, 1,010 have trivial H stabilizer and
only 14 have stabilizer two.  Their 5,955 available first pivots reduce to
5,881 stabilizer-pivot orbits, merely **1.0126x** compression.  Orbit-aware
first-pivot grouping is therefore not a load-bearing optimization; the sample
is bounded and makes no full-checkpoint orbit claim.

In-memory literal K18-row coalescing was also tested.  It is exact for signed
profile weights and helps the heaviest high-`m1` region, but on the distributed
sample it created 4,809,897 child-row keys before reaching only 682,318
profile keys.  Externalizing that intermediate language would enlarge I/O.
It may be used as a worker-local microbatch optimization, but must not replace
the source-labelled profile record or use a single coarse-profile witness to
generate literal children.  The archived hidden-K16 audit already shows that
coarse profiles can contain multiple decorated physical orbits.

## Bounded benchmark

Eight parallel, distributed 20,000-row samples (160,000 source rows total)
gave:

- cached-direct CPU sum: 4.290813 s;
- worker-local row-stage CPU sum: 3.735790 s;
- 682,318 nonzero profile keys;
- exact cached-signature range: 29--159 states per shard.

Linear projections are deliberately non-load-bearing: 646.23 CPU seconds,
80.78 seconds at ideal eight-way balance, and 10.69 GB of atomic records.
They indicate the prior 2,024 s / 17.9 GB single-path prefix projection is
not a reason to reject staged gates, but they are neither runtime nor size
certificates.

## Restartable full plan

Use one process sharing the 735 MB checkpoint and immutable structure through
`Arc`, with eight workers and 64 contiguous source shards (about 376k records
each).  Each worker owns a small signature cache and a 250,000-key signed
profile sink.  Parts are locally sorted, atomically renamed, and authoritative
only after a shard manifest records source interval, counts, weights,
denominator histogram, and hashes.

Run three independent hard gates:

1. **Export gate, 600 s / 16 GB.** Schedule at most eight shards at once.  At
   450 s stop assigning shards; allow active shards to finish or stop
   resumably at 600 s.  Validate exact full parent totals before acceptance.
2. **External signed-merge gate, 600 s / 16 GB.** Merge all accepted parts,
   retain exact-zero counts and smallest literal witnesses, and replay source
   coverage plus signed sums.  Do not generate K20 rows.
3. **Charge gate, 600 s / 16 GB.** Stream 12 K2 responses per surviving
   merged profile to obtain the six full/irreducible 77-charges.  No row
   collection or K21 tails.

No full export, merge, or charge job was run in this audit.

## Artifacts

- exact benchmark/checker: `benchmark_k16_row_cache.rs`
- benchmark result: `results_k16_row_cache_benchmark.json`
- exact stabilizer sample: `audit_k16_stabilizer_sample.py`
- stabilizer result: `results_k16_stabilizer_sample.json`
- machine-readable plan: `results_k16_k2_restartable_plan.json`
