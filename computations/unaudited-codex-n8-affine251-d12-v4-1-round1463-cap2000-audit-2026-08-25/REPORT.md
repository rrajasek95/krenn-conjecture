# Independent D12 round1363→1447 recovered cap2m audit

Status: `PASS_EXACT_FULLY_TELEMETERED_ROUND1447_RECOVERED_CHAIN`.

The sealed round1363 input is pinned by manifest `bc359255b558a91a02fee4fc76aee9394b3a91d08aa24dd4ef96652bf1e80fd6`, checkpoint `91d573bcfbb2e43f0832a595c899b7c5bd411845cb8323cbcff1c5d7728f92e1`, and cache `5c39cf56b3504a44f8e002f9ad3e42b533855d6217e5e5f9967543f6d77e0e5e`.

Accepted stages01–14 plus distinct `stage15_recovery_attempt2` cover exactly rounds1364–1447 with no gaps. All 15 checkpoint edges are descendants and all inherited cache records are byte-identical. The final state has 1,970,322 columns, support 2,136, target coefficient 1, and 29,678 columns of cap headroom. Independent replay checked 1,970,322 columns / 201,304,537 terms with zero failures.

The original Stage 15 is excluded: its atomic result is absent, its unmatched checkpoint/cache were never accepted, and it contributes zero coverage. Failure evidence SHA is `98e0e7993007bf14b9fd96a32c1548f410fa325943f92fc1ff7b75b4a2175472`; compaction execution SHA is `70775a9cf541afad739bf3e41fc687f96d0384528a4127404634552ea0e64a03`.

Resource blocks are 510.337634 s, 522.671661 s, and 515.460899 s, each below 540 s. Maximum accepted-stage RSS was 24,894,816 KiB, below 37,748,736 KiB. All accepted watchdogs pass with frozen provenance and atomic outputs.

Authoritative recovered endpoint:

- result: `a313bf00b597c3253edc32e33550ad4a0bb83d539e31eb77d3b34e6c617c22c6`
- checkpoint: `82d53e68e3f1bd483518996fed2dbffa80910163e8c7234f9ccce7c88afeb3cb`
- cache: `b806d22cac98ce4dd45928baf01401a8a7afaa12fcbd6d9c56f07cb1f9dab091`
- watchdog: `81c27fe5f12c066645f64f5620570af8c2d463dcbc520e5b065ce7a959e650c7`

Scope caveat: round1447 is an exact resumable state near the cap, not round1463 and not a terminal global dual.
