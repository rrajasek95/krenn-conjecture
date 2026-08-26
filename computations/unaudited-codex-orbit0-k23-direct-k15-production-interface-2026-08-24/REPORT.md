# K23 grouped direct-K15 production readiness

The sealed source and binary are ready for an eight-shard, source-linear K23 production run over four grouped scalars covering exactly 12 IDs. No shard was launched.

The producer source SHA256 is `c3ea65b5ac1221e1b0020e2f0a9753bd774826059ae16e24c05cd4f6f5706e8c`; the executable SHA256 is `a6bc9f1f1b217a4cfc8dc662ea1358e4c3ac012f40c49e6c07cf05b1e52faa04`. The validator also rehashes the structure, response, K4, cycle, and included engine inputs. It accepts only the exact eight intervals `[0,60)`, `[60,121)`, `[121,181)`, `[181,242)`, `[242,303)`, `[303,363)`, `[363,424)`, and `[424,485)` with eight workers.

Each shard validator closes the result keys, the four sink keys, U, source heads, strict grouped ID order, path degrees, full=irreducible counts and charges, denominator divisibility, terminal fan identities, sign/terminality text, wall time, and source/engine hashes. Its positive prefix32 test passes; ten hostile mutations covering structure, arithmetic, grouping, and interval gaps/overlaps fail.

`merge_k23_direct_k15_shards.py` requires exactly eight independently valid shard files and the exact no-gap interval bitset. It sums all scaled integers and histograms before dividing by U, checks the frozen full source census `(485 slices, 6,704,640 heads, mass 322,486,272, l1 3,085,516,800)`, and atomically writes the complete result, strict four-group/12-ID assembler fragment, and hash ledger. Individual packet charges remain null; no unsupported split of the grouped source scalar is introduced.

The independent cache-free Rust referee source and binary are pinned. Its retained 1,028-row ledger covers 257 distributed source slices from 0 through 484, all four sinks per source, and packet counts 86/86/85 per sink. The new audit independently checks every provenance coordinate, pivot/tail and divisor tuple, exact signed U formula, terminal fan, and aggregate against the sealed referee result. Terminality itself is asserted during the pinned literal Rust replay at anchor-signature mass 1.

Shard0 is ready but held until the active D14 production/merge is sealed and explicit resource clearance is received. Its command is frozen in `k23_direct_k15_production_contract.json`; family RSS is capped at 8 GiB, aggregate RSS at 16 GiB, launch projection at 540 seconds, and hard wall at 600 seconds. No row output or K24 claim is in scope.
