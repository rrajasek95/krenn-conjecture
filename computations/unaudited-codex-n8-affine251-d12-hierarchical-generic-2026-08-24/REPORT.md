# Exact generic hierarchical D12 gate

## Verdict

**PASS — production-ready for the fixed cold + rare + 16-worker mode only.**

The new sibling resumes the accepted round-748 checkpoint/vector cache and
performs exactly one round to 749.  Its checkpoint, candidate, and
719,740,833-byte vector cache are byte-identical to the sealed sequential
result.  The independent referee replayed every one of 334,298 exposed columns
and all 33,907,235 stored vector terms with zero annihilation failures.

This is an integration/performance result, not a complete D12 membership or
conjecture claim.  No continuation beyond round 749 was run.

## Frozen lineage and evidence

- Restored parent source: `241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`.
- Restored parent binary: `a3761406b3ce0fc0ef658bfc876dcdb7727e6d6b10bae42a981f6e6a8c71f47a`.
- Accepted start checkpoint (round 748): `fe44b33e74b7e9ce00a7654fe8f027b0024b15e464bbaa372ec85ea92bc097c6`.
- Accepted start vector cache: `7af04cecc244e158af1df5b782cbe5b2e23d191b4d06b43a1c0c33911e5c6cab`.
- Provider input: `daa427528bbbeece064b09396023b66f32b804ba6d304178d19ced13e9b38a4e`.
- Sealed v3 source: `173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a`.
- Sealed v3 binary: `8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a`.
- macOS watchdog: `a1e6104726303960b256c9a9f6217299a71a4be5c00bb77fe451bf62935ed19b`.
- Upstream rank-gate source/integration: `d6e259fb67c9e51e3cd6c7c3d3684870a53c684584c0cf5b7fb1cc6b50a3ae44` / `520c6cf496071c7e198e435a43d451345c7abc4908fc30c337a8a1f4e84cc0fe`.

## Exact A/B result

Both kernels started from separate copies of the same accepted round-748
state.  The sequential comparator used the restored parent binary first; the
hierarchical run followed and was the only heavy process.

| Measure | Sequential tree | Hierarchical v3 |
|---|---:|---:|
| round | 749 | 749 |
| columns | 334,298 | 334,298 |
| new columns | 1,099 | 1,099 |
| candidate support | 418 | 418 |
| new support rows | 229 | 229 |
| solve seconds | 11.050344 | 2.585664 |
| solve speedup | — | **4.273696814×** |

The common output checkpoint SHA-256 is
`dda7fb5100adfcc24264993899ec2404a3beec0e0f1e96b4f3dd83a2be7d8621`.
The common vector-cache SHA-256 is
`93e3eeee9d7a356b4caaf59cae5c5b6671e64508004b448895d0296db0bd2bf1`.
Byte comparison, not only semantic comparison, passed for both files.  Because
the candidate and exposed column set are identical, the actual next frontier
is also identical.

Hierarchical phase timings were: natural owned sort 0.943361 s, 16 FNV rank-map
build 0.250911 s, parallel compact materialization 0.225443 s, local basis wall
0.062516 s (critical elimination 0.062190 s), arity-two merge 0.134990 s,
backsolve 0.182981 s, and native every-column verification 0.672468 s.

## Resource and fail-closed evidence

The Darwin process-group watchdog sampled every 250 ms.  It recorded 39 samples,
9.945263 s wall, and peak RSS 4,676,672 KiB (4.46 GiB), below the hard 36-GiB
threshold.  There was no breach; result/cache/checkpoint temporary files were
absent and final outputs were atomic.  The native JSON's `peak_rss_kib=0` is not
used as evidence because its sandboxed child `ps` is ineffective on this host.

Five hostile selections (workers, pivot, strategy, incremental mode, and bad
kernel name) returned code 2 before writing output.  The implementation accepts
hierarchical operation only for literal cold/rare/16-worker/nonincremental
configuration and a `u32` prime.  The full replay also validated the vector
cache's internal FNV fingerprint and target coefficient normalization.

## Artifact authority

Authoritative evidence is limited to `sealed_v3/`, `control_sequential/`,
`control_hierarchical/`, `results_independent_replay.json`,
`results_hostile_selftest.json`, the integration patch, and this report/manifest.
Earlier `v1`, `v2`, `unwatched`, `watchdog_blocked`, and `rlimit_blocked`
directories are diagnostic only.  In particular, v1 source/binary bytes were
not snapshotted before later compilation and have incomplete provenance; none
of those attempts is used for promotion.
