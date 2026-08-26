# K24 charge-first production interface

## Outcome

PASS for bounded production readiness, with no production launched.  The exact scalar-only interface covers all 35 K24 lineage IDs in 10 strict groups and six source families.  Its fail-closed assembler accepts a complete no-gap set of independently accepted shards only when the total equals

`829424811081283712 / 173867925`

or, at the frozen common scale `U = 400591699200`, the integer

`1910994764731277672448`.

This is a conservation/filtered-obstruction gate.  A mismatch would stop the K24 program before relative-column production.  A match does not by itself prove the relative K24 claim.

## Exact minimal charge schedule

The earlier 167-shard physical fallback is superseded for charge only by the source-linear family engines below.  The 83-shard partition is the smallest balanced integer partition, family by family, whose measured linear projection is strictly below the 450-second stop-scheduling threshold.  Every interval is explicit, disjoint, and exactly covers its frozen source.  A production shard remains subject to a 540-second internal wall guard, 600-second external alarm, 8 GiB family RSS guard, atomic outputs, and one-heavy-family-only scheduling.

| family | strict groups / IDs | source units | measured gate | shards | projected maximum | shard 0 |
|---|---:|---:|---:|---:|---:|---:|
| hidden collected K18 | 1 / 1 | 158,439,965 | 4,096 in 0.031146 s | 3 | 402 s | `[0,52813321)` |
| hidden decorated K16 pair | 1 / 1 | 101,545,723 | 4,096 in 0.174788 s | 10 | 434 s | `[0,10154572)` |
| K14 source formula | 2 / 2 | 485 | 8 in 33.128791 s | 5 | 402 s | `[0,97)` |
| grouped direct K15 source | 2 / 6 | 485 | 8 in 70.492407 s | 10 | 428 s | `[0,48)` |
| grouped direct K16 rows | 2 / 12 | 24,097,095 | 4,096 in 4.028044 s | 53 | 448 s | `[0,454662)` |
| direct D17/D18 formula | 2 / 13 | 485 | 8 in 9.625596 s | 2 | 292 s | `[0,242)` |

Total: 10 groups, 35 IDs, 83 shards.  If an independently accepted shard 0 implies a wall projection of at least 450 seconds, the only authorized schedule change is exact subdivision; no interval may be widened.

The sole authorized launcher form is:

```text
python3 computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/run_k24_charge_shard_guard.py <shard_id> <result.json> <resource.json>
```

The launcher resolves the frozen command from `k24_charge_production_plan_83.json`; hand-edited commands are outside the contract.  Start with exactly one family shard 0 after external resource clearance, independently validate it, and request the next interval only after acceptance.

## Exact semantics and acceptance

Both engines replay literal preterminal pivots, divide by every exact orbit divisor, and charge only terminal K4 responses.  They exhaustively assert terminality for all 60 K4 tails and record `full_charge_scaled_U == irreducible_charge_scaled_U`.  They emit scalar JSON and distributed witnesses only; no K24 rows or relative columns are materialized.

`k24_production_contract.py` is the executable authority.  It:

- re-hashes every frozen source, engine source, and binary;
- enforces schemas with closed key sets and exact family/group/ID equality;
- rejects distributed physical diagnostics as production intervals;
- proves interval no-gap/no-overlap coverage before summation;
- checks full/irreducible equality, i128 bounds, exact `U`, and resource evidence;
- requires a global 257-bin distributed literal witness ledger; and
- accepts the final charge only on exact equality with the scaled target above.

The hostile suite rejects 13 mutations: extra/missing keys, full/irreducible mismatch, wrong IDs, interval gaps/overlaps, unsorted B records, orbit mismatch, inexact orbit division, zero orbits, manifest extras, wrong B IDs, and an unready B-production allowlist.  The audit is identical under standard Python, `-O`, and `-I -S` (stdout SHA-256 `bf489966ac64b62f4a9c387238d928997e4df51e3cda38f99334207cacf07680`).  The direct D17/D18 one-record scalar charges also exactly match the independent factorized producer.

## Frozen pins

Engine pins:

- physical source `10670f0687168d4383cfeb679ce8521d4c8b1b5621092b7600a3ef1b6ee79f51`
- physical binary `21ef771613369867a4bb0bad7257cd7e04da11dffad68061b6f4c56dff231c8a`
- hidden source `88f79b2b21dca82d6afa485952cbdd42c734bb1b7e71cdc81687b1742accaac1`
- hidden binary `4c5a33f207d63cd9bde23756148b564a9fdb6c24691880d972a473ee086ecb1e`

Primary and common retained-source pins:

- hidden K18 ledger `442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8`
- decorated-pair ledger `22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8`
- physical structure `55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b`
- direct K16 rows `93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3`
- K17 auxiliary `f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab`
- K4 table `4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3`
- cycle auxiliary `8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7`

Contract pins:

- executable validator `3982138baf6167025c3a3c9b0455f4e101bd5929b17cd2fad48856112b04af75`
- guarded launcher `25ecddce233e74378fe69f411cf7ad62491292018b2280e964b2b5c69d6f6cfb`
- charge schema `ea4d741267bd8e4c125537be01c91800e8c41010ec284085e20890a6d25a5d71`
- B20 schema `eaaac95e02c17fd0c930b92c7f40504cfc6639e9293401c812a6aa9017ec9b62`
- expected 10-group contract `9ee7c5b6c31b70a7e06f8a4909c8b9aa77a87444cb12992c9971b5259bb8a986`

## B20 and relative scope

The exact 103-shard geometry and strict 39-byte natural-order B-record interface remain frozen in `k24_B20_production_plan_103.json`; the held upstream plan is pinned by `7625ca900d59e7cd39d306d9f2df9632d3d8350f1b8fb7ea983a219db88425b8`.  No B20 production has launched.  Five of six source families still lack B20 producers; the direct D17/D18 producer is prefix-tested but needs an exact 61-interval production-allowlist supersession.

Even a successful charge assembly only authorizes later B-source work.  The terminal relative map is `A24_rel = T | ker(L)`, so top ledgers alone are insufficient: the final proof still requires exact lower-correction/relative-column certificates.  The sparse closure gate is pinned by `0675c7cbf370ffdb5dc48b35e1350a6c53f9a9f2445abae2a0dd054a8f726d2b` and already shows that a naive source-unit column can exceed the one-million-column cap.

## Decision

The charge-first 35-ID computation is exact and launch-ready only at shard-0 granularity, pending explicit resource clearance and independent shard acceptance.  No charge production, B20 production, K25 computation, or relative K24 claim is made here.
