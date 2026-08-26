# Full cached K16/K2 K18-parent export

## Verdict

`PASS_COMPLETE_64_SHARD_K16_CACHED_EXPORT`.  The export-only gate completed
all 64 deterministic contiguous source ranges in 85.824699 seconds, well
inside the 600-second bound.  It produced 281 atomic `K18PRF2` parts totaling
6,647,540,680 bytes.  No merge, charge evaluation, cleanup, row collection,
or K21 tail generation was performed.

## Production controls

Before the full gate, the production cached map was compared with the literal
baseline on the four frozen 2,000-row ranges.  Keys, signed weights, use
counts, and minimum source witnesses agreed exactly.  A separate `[0,100)`
end-to-end run wrote one part and the production verifier reconstructed all
4,243 records from the direct-K16 source checkpoint and replayed signatures,
profiles, pivots, denominators, source rows, and signed sums.

The production optimization is only the audited worker-local map
`child signature -> available pivots`.  Literal parent rows, profile keys,
signed `U/(m1*m2)` arithmetic, and reversible witnesses are unchanged.

## Exact full counts

- source rows: `24,097,095`;
- pivotable source rows: `24,003,767`;
- first-pivot uses: `129,939,187`;
- generated K18 parents: `1,559,270,244`;
- pivotable K18 parents: `807,499,618`;
- outgoing pivot uses: `2,049,974,172`;
- locally nonzero emitted records: `63,918,401`;
- signed mass at `U=400591699200`: `3218269567887566438400`.

All exact frozen global source/parent totals were met.  The denominator
histogram sums to 807,499,618, and weighting it by the second pivot count gives
2,049,974,172 outgoing uses.

## Acceptance and resource guards

Every shard was accepted only after its full parts were streamed by the
literal production verifier.  Each accepted manifest pins its range, kernel
ledger, verifier ledger, source and binary hashes, and the size/SHA-256 of
every part.  A separate post-run replay rehashed all 6.65 GB, checked exact
range coverage, totals, denominator identities, and confirmed zero temporary
files.

Free space was 242,719,956,992 bytes at launch and 236,071,890,944 bytes at
terminal.  The runner fixed concurrency at eight and used the previously
audited sub-16-GB process design.  Sandboxed `ps` denied RSS telemetry, so no
observed RSS number is claimed; this is the only resource-observability caveat.

## Artifacts

- `results_k16_cached_export.json`: terminal aggregate;
- `results_k16_cached_export_package_audit.json`: independent all-part replay;
- `results_k16_cached_production_controls.json`: baseline and tiny-run guards;
- `shards/shard_00.accepted.json` through `shard_63.accepted.json`: atomic
  acceptance manifests;
- producer and runner remain in
  `../unaudited-codex-orbit0-k16-k2-export-optimization-2026-08-23/`.

All parts and manifests are retained.  A later signed external merge is a
separate, currently unperformed gate.

Pinned SHA-256 digests: terminal result `322bfc5d9ed5381d...`, package audit
`4d7a3dbd93eb52bf...`, production controls `460b13ea99393673...`, producer
source `8753f475dc7b5165...`, producer binary `bb9c470b701d99df...`, and the
sorted concatenation of all 64 accepted manifests
`4e21b3738281b44c5281d7a900ed008b67107e85b7d011002a76f129fcc49b8a`.
