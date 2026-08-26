# Independent K24 charge-production referee

## Verdict

The exact charge interfaces cover precisely the frozen 10 scalar groups and
35 K24 IDs.  The DAG hash is
`9ee7c5b6c31b70a7e06f8a4909c8b9aa77a87444cb12992c9971b5259bb8a986`
and the common scale is `U=400591699200`.  No K25 ID or membership claim is
in scope.

The repaired physical producer is source-faithful and independently
replayable.  Its frozen v2 source hash is
`10670f0687168d4383cfeb679ce8521d4c8b1b5621092b7600a3ef1b6ee79f51`.
The repair changes no arithmetic: it adds the per-source head ordinal and
literal source row that were absent from the v1 sample ledger.  A K16
one-record control and formula-family prefix controls reproduce the old exact
charges, while the independent referee reconstructs the source head and every
pivot/tail transition from the frozen literal engine.

The frozen fast direct D17/D18 producer is arithmetically valid and is the
resource-feasible full scalar path.  It has source/binary hashes
`57a82f19...`/`c7b2e223...`; its prefix1 agrees with the v2 source in all
counts, both charges (`+825568674132787200` and
`-85322827196006400`), terminality, and normalized denominator histograms.
However, that binary drops its witness vector instead of serializing it.  Its
full output can therefore receive scalar/count PASS only.  Literal acceptance
requires the bounded sample-only companion to emit and replay exactly 257 bins
for each of the two groups; this is not a scalar rerun.

The landed full direct result passes that two-part protocol.  Its result hash
is `cc838dde...`; the exact charges are `4082223104/7` for D17 R3-4 and
`157204480` for D18 R2-4, with subtotal `5182654464/7`.  The separate sampler
ran in 4.072198 seconds without accumulating any family scalar, emitted 514
nonzero witnesses (257 per group), and the independent literal engine replayed
all 514.  The ledger/referee hashes are `0d57f495...`/`3cc8bab4...`.

The landed fast K14 result also passes exact structural and literal replay.
Its two charges are `276055879132032/1053745` (R3-3-4) and
`3437504767744/21505` (R4-2-4), subtotal
`444493612751488/1053745`.  All 514 frozen ledger rows replay, with exactly
257 bins per sink.  The producer selects the first realized head in a bin,
not the first nonzero head: 413 witnesses are nonzero and 101 are exact zero
responses.  This is disclosed and verified; no 257-nonzero-per-sink claim is
made for that ledger.

## Exact sign and terminal rules

Formula sources begin with the negative R8 orbit coefficient.  Each selected
pivot contributes the normalized `-1/m` response sign.  Hence the three-pivot
K14/K15 paths have positive source-normalized terminal units and the two-pivot
D17/D18 paths remain negative.  Direct K16 consumes its already-signed retained
coefficient and applies the same remaining-path parity.

For hidden18, the retained scaled weight is divided exactly by the two current
multiplicities, `w/(m3*m4)`.  For the hidden decorated pair, the retained
coefficient already includes the fixed decorated first-pivot normalization;
the remaining selected pivot gives `-w/m3`.  The referee reads the authoritative
binary record at every sampled index, checks the orbit identity, reconstructs
the K20 row, and recomputes all 60 terminal K4 tails.  Every checked response is
terminal and full equals irreducible.

## Validators

`validate_k24_charge.py shard` validates exact family/group/ID scope, interval,
U, all stage/count/cache/histogram identities, sample schema and distributed
bin placement.  `merge` requires a contiguous full `[0,N)` family partition,
rejects gaps/overlaps, and requires exactly bins `0..256` for every group.
`fast-direct-full` applies the frozen 485-slice D17/D18 scalar guards and reports
the literal-ledger condition explicitly.

`referee_k24_charge_literals` independently replays a supplied v2 or hidden
ledger without traversing the scalar shard.  It verifies source provenance,
literal rows, selected pivots, tail indices, multiplicities, signs, U-scaled
units, aggregate K4 charge, all-terminal tails, and nonzero contributions.

## Direct-K16 R4-4 sample repair

The first full R4-4 traversal failed atomically after its scalar loop because
equal source-index bins contain nonzero terminal support in only 37 of 257
bins.  It produced no result or ledger, and no scalar from that process is
accepted.  A read-only census froze 257 distinct nonzero literal
continuations: seven from each realized bin 0--34 and six from each of bins
35--36.  The candidate ledger hash is
`57b7f0cfa15b436b6b821922c426f19d15496eb7a1cd64e7e632acaa003d5fbf`;
all 257 candidates independently replay.

The support-v4 source/binary hashes are `64c0a694...`/`6f61d411...`.
On the same distributed 262,144-record control, the old and new executables
agree exactly on 29 scalar/count/histogram/cache/provenance fields, including
charge `-5997775755852840960`; only sample routing, support metadata, and time
differ.  The v4 control also emits the complete observed nonzero-record
support histogram: its positive key set is exactly bins 0--36 and its outside
count is zero.  A full run has the same exact-set assertion before output, and
the independent validator repeats it.  Eighteen hostile tests, including
standard/optimized/isolated Python, reject scalar mutations, missing,
duplicated, or corrupted candidates, missing realized bins, and positive
support outside the frozen set.
The one-full-run relaunch is accepted only with the frozen four hashes,
external 600-second alarm, no competing heavy process, atomic distinct output,
and post-run exact 257-candidate replay.  This package did not launch it.

## Direct-K16 R2-2-4 schedule

The distributed 262,144-record gate ran in 6.982861 seconds and projects a
monolithic 641.886406 seconds, so a one-pass launch is rejected.  The fastest
accepted exact schedule is two sequential contiguous halves
`[0,12048547)` and `[12048547,24097095)`, projected at about 320.94 seconds
each.  The prepared merger requires exact no-gap/no-overlap intervals, global
source/count pins, all recurrence/histogram/cache/sign/U identities, and a
deterministic minimum-index choice for the shared sample bin 128.  The merged
ledger must cover all 257 bins and pass independent replay of both K2
intermediates and the terminal K4 response.  The distributed prefix's 257
samples already pass that replay.  Because contiguous pieces are larger than
the distributed gate pieces, each half remains conditional on live RSS checks
below 15 GiB; no R2-2-4 production was launched.

## Hidden-decorated full result

The singleton `D14:222|R:2-4-4` full result passes independent structural and
literal review.  Its result/ledger hashes are `5ee0aff3...`/`4d8d74d6...`;
the recomputed source hash is `22f91fc8...`.  The exact scaled charge is
`97324923903254986752`, or `1280052134670336/5268725` after division by U.
The full interval is `[0,101545723)`, with 1,011,364,980 selected p3
occurrences and 60,681,898,800 terminal K4 occurrences; full equals
irreducible.

The independent Rust referee re-seeks all 257 deterministic source records
and rebuilds each stored aggregate from all 60 first K4 tails, every available
p3, and all 60 terminal K4 responses.  It checks the exact row, p2, retained
weight, uses, orbit/stabilizer, multiplicities, sign, terminal weight, charge,
and terminality.  All 257 replay, and a 17-case structural/literal hostile
suite passes under standard, optimized, and isolated Python.  No scalar shard
was rerun.

Typical commands are:

```text
python3 validate_k24_charge.py shard --family direct17 --result SHARD.json --samples SHARD.json.samples.tsv --start A --end B --output SHARD.referee.json
./referee_k24_charge_literals --family direct17 --samples SHARD.json.samples.tsv --output SHARD.literal-referee.json
python3 validate_k24_charge.py fast-direct-full --result FULL.json --output FULL.scalar-referee.json
./produce_k24_direct17_distributed_literals --workers 8 --output direct17.sample-only.json
```

## Hostile controls

The general fifteen-case suite passes under standard Python, `python -O`, and isolated
`python -I -S`.  The validators reject wrong U, legacy/incomplete provenance,
extra IDs, wrong interval, terminal/full/irreducible disagreements, cache-count
corruption, source-row/ordinal mutations, unavailable pivots, and sign/unit
mutations.  The R4-4 repair adds eighteen support-specific controls, and the
R2-2-4 merger/literal interface adds eleven bounded controls.  Their results
are `results_k24_charge_referee_hostile_selftest.json`,
`results_k16_r44_support_patch_hostile_selftest.json`, and
`results_k16_r224_referee_hostile_selftest.json`.

## Grouped-K15 two-half production contract

The remaining K15 family is frozen as exactly two source-faithful grouped
scalars covering six IDs: `D15:{223,232,322}|R:2-3-4` and
`D15:{223,232,322}|R:3-2-4`.  The source-backed sample-only patch has frozen
source/binary hashes `594701a2...`/`230918d0...`; its eight-slice control is
scalar-identical to the original engine and independently replays all eight
emitted literals.  Its 11.658095-second runtime projects the exact contiguous
halves `[0,242)` and `[242,485)` at 352.657374 and 354.114636 seconds,
respectively, both below the 540-second external gate.

`run_k15_frozen_half.py` verifies all frozen hashes, refuses overwrite, runs
only one exact half with eight workers, validates it, independently replays
its source-backed ledger, and publishes provenance only after both checks.
`validate_merge_k15_fast.py` accepts only the two provenance-pinned no-gap
halves, enforces the exact DAG set, grouped-scalar-once semantics, source
pins, sign/U and terminal/full/irreducible identities, then requires bins
0--256 separately for both groups and replays all 514 witnesses before
publishing a strict six-ID fragment.  Thirty bounded hostile cases pass under
standard, optimized, and isolated Python.  Memory is slice-bounded (the
terminal cache is reset per R8 slice); launch remains conditional on live RSS
checks with a 15-GiB abort threshold because the sandbox did not expose a
direct prefix peak-RSS counter.  Exact commands and hashes are in
`results_k15_two_half_schedule_audit.json`.

No full K15 charge production was launched by this contract audit.
