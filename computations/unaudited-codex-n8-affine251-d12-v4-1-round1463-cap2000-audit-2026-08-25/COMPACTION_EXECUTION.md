# Storage compaction execution

Executed after the sealed read-only audit `b2ff185339a9b0ebd88ec7221d4dae89ed73b77cac7438639bd3a556acb6b93d` diagnosed the round-1447 ENOSPC failure.

- Removed the unaccepted `stage15/vectors.bin.tmp` partial output.
- Removed only `checkpoint.bin` and `vectors.bin` from superseded rejected/failed portfolio attempts identified by the audit; their small failure telemetry remains.
- Removed only `checkpoint.bin` and `vectors.bin` from the independently sealed old `production_from_round1262_portfolio_cap1500/stage01` through `stage09` states.
- Preserved that chain's `stage10` endpoint, result/watchdog/stderr records, prior audit and manifest hashes.
- Preserved every current accepted `production_from_round1363_portfolio_cap2000/stage01` through `stage14` artifact and the round-1442 restart state.

The old full manifests that named the pruned stage payloads are intentionally no longer locally replayable; their recorded SHA-256 values and independent audit verdicts remain as provenance. Available filesystem space increased from 110 MiB before cleanup to 32 GiB after cleanup.

## Second compaction at round 1462

When the exact continuation reached round 1462, free space had fallen to 7.6 GiB, below the sealed 12 GiB relaunch floor. The following redundant payloads were removed while retaining their small results, telemetry, manifests, audits, and the byte-identical accepted candidates:

- `round1363-internal-sequential-portfolio-cap2000-design/portfolio/{checkpoint.bin,vectors.bin}`
- `round1363-internal-sequential-portfolio-cap2000-design/selected_control/{checkpoint.bin,vectors.bin}`
- `round1448-cap2250-gate/control_cap2000/{checkpoint.bin,vectors.bin}`

The retained accepted states are `round1363-.../cap2000_candidate` and `round1448-.../candidate_cap2250`. Free space increased from 7.6 GiB to 18 GiB. As above, manifests naming the intentionally pruned byte-identical controls remain provenance records but are no longer fully locally replayable.

## Third compaction after the sealed round-1463 audit

After independent audit `6d207999056a49fc5d94d63dda182e47348131078627b241bca024ca45e6c28d` and manifest `46e69f29a46d24fadd2163e301ad77127071981aad3c0ad2305882b214da6bbb` sealed the exact round-1463 endpoint, the following ancestor payloads were pruned:

- `production_from_round1448_cap2250/stage01..stage03/{checkpoint.bin,vectors.bin}`
- `round1448-cap2250-gate/candidate_cap2250/{checkpoint.bin,vectors.bin}`

The full accepted round-1463 `stage04` checkpoint/cache and every small result, watchdog, audit, report, and historical hash remain. Free space increased from 14 GiB to 30 GiB. Historical manifests naming those pruned ancestor payloads remain provenance records but are intentionally no longer fully locally replayable.

## Fourth compaction after the sealed round-1464 cap gate

After audit `042c875ebb95d1273e88161a410b3ebdb207d3c3a0b96bed3ddd58b3d080884d` sealed the byte-identical round-1464 cap-2.25m/control and cap-2.5m/candidate outputs, these redundant ancestor payloads were pruned:

- `round1464-direct-cap2500-gate/control_cap2250/{checkpoint.bin,vectors.bin}`
- `production_from_round1448_cap2250/stage04/{checkpoint.bin,vectors.bin}`

The accepted round-1464 `candidate_cap2500` checkpoint/cache remains the sole restart state. Small results, telemetry, audits, reports, and all historical hashes remain; manifests naming pruned files are provenance-only. Free space increased from 22 GiB to 26 GiB.

## Fifth compaction at the round-1483 storage hold

The recovered round-1447 chain had already been independently sealed by audit `63e65b41f251c6eee54ada1b629647cfb9151abd4643b2fce40fff649113d406`, replay `541b657181969f8310a5cde70bf2d53fb314c86193503fbc6c5c75512554b6bb`, and manifest `a60825d7f5c80b47ce3f74249a1727928cdec76559ae01fcc8ebc5e90bf71cd1`. After later descendants through round 1483 were accepted, the following ancestor payloads were pruned:

- `production_from_round1363_portfolio_cap2000/stage01..stage14/{checkpoint.bin,vectors.bin}`
- `production_from_round1363_portfolio_cap2000/stage15_recovery_attempt2/{checkpoint.bin,vectors.bin}`

All small success/failure evidence, audits, reports, and hashes remain. The active round-1483 chain and its restart checkpoint/cache were untouched. Free space increased from 8.9 GiB to 60 GiB; the old round-1447 manifests are now provenance-only rather than fully locally replayable.

## Sixth compaction after the sealed round-1484 audit

After audit `c9595f6d17635a26b8082397f8862bc41b1edb79257415818985cc6c8077c74c` and manifest `5abf95d2a3781a3d3e18836bc6d2310504e547095fd8a572a6976907a9fd47a8` sealed the five-edge continuation and final replay, these ancestor payloads were pruned:

- `production_from_round1464_cap2500_to1484/stage01..stage04/{checkpoint.bin,vectors.bin}`
- `round1464-direct-cap2500-gate/candidate_cap2500/{checkpoint.bin,vectors.bin}`

The complete round-1484 `stage05` checkpoint/cache remains the active restart state. Small gate/production/audit evidence and historical hashes remain. Free space increased from 56 GiB to 77 GiB; affected old manifests are provenance-only.

## Seventh compaction after the sealed round-1504 audit

After audit `84326f703fc2404bf2cd1a4b6efcbbe781467a235f81c571f331704c15badc7f` and manifest `96ee94456abd18a9ca01b12daf90eddf53274348214f76d819031f5edf699397` sealed the five-edge chain and all-column replay, these ancestor payloads were pruned:

- `production_from_round1484_cap2500_to1504/stage01..stage04/{checkpoint.bin,vectors.bin}`
- `production_from_round1464_cap2500_to1484/stage05/{checkpoint.bin,vectors.bin}`

The complete round-1504 `production_from_round1484.../stage05` checkpoint/cache remains the active restart state. Small evidence and hashes remain; affected historical manifests are provenance-only. Free space increased from 54 GiB to 76 GiB.

## Eighth compaction after the sealed round-1524 audit

After audit `bb477e89e63aafbceaca857f7132d0cbfebca007dd9b10906c97db2b74f6e0e9`, replay `58691230bb43b2ab186d718f28e245b65c0f336db70e03374da1c409e43a4c56`, and manifest `040409dd20d8c4811c03bf81f9c2064abbf2163b6025adc49a0e4cac8cbb8130` sealed the eight accepted edges through round 1524, the following ancestor payloads were pruned:

- `production_from_round1504_cap2500_to1524/stage01`, `stage02`, `stage03`, `stage03_recovery_cap1514`, `stage04_cap1516`, `stage05_cap1518`, `stage05_recovery120_cap1518`, `stage06_cap1520`, and `stage07_cap1522`: only `{checkpoint.bin,vectors.bin}` where present.
- `production_from_round1484_cap2500_to1504/stage05/{checkpoint.bin,vectors.bin}`.

The exact round-1524 restart payload remains at `production_from_round1504_cap2500_to1524/stage08_cap1524`, with checkpoint SHA `376f83253a3f901f7ae565d8ded6cb31c9758203ef9a7a91657cd3d3b65501a0` and cache SHA `6a3aa33a4706beac36fd4860ccf96e693e56b9cf9eab5a15c66198668821fc07`. All small results, failure/no-op evidence, watchdog telemetry, reports, audits, and historical hashes remain. Free space increased from 39 GiB to 77 GiB; affected historical manifests are provenance-only.

## Ninth compaction after the sealed round-1527 cap gate

After the exact round-1526 audit `8b3ed264a49a9aeaa0577e0c3a82b01b49907a866d0d826dfb5ab51b4dbc41e9` and cap-equivalence audit `a3b7d35c880d82cd31b9651eaf8dca9a5093a14fa20842e2032b173bf43ecd1f` / manifest `c7d94225663ea9f0c1249f907538ba1d23e2e682f91caa52a4abad9c450eb9ad` sealed the byte-identical 2.5m and 2.75m outputs, these redundant payloads were pruned:

- `round1527-direct-cap2750-gate/control_cap2500/{checkpoint.bin,vectors.bin}`.
- `production_from_round1524_cap2500_to1538/stage01_cap1526/{checkpoint.bin,vectors.bin}`.
- `production_from_round1504_cap2500_to1524/stage08_cap1524/{checkpoint.bin,vectors.bin}`.

The sole restart payload is the accepted `round1527-direct-cap2750-gate/candidate_cap2750` state, reverified after cleanup at checkpoint SHA `a18ac93c6cd33a6182cfa91342e4496de4f6e7cdd15ac15c737480747a0f8e3a` and cache SHA `1e5b9bbbfb2a4c7245c0e999d298675445737056c9dee24af3b1b917cf9cb7d9`. All small telemetry, audit records, reports, and hashes remain. Free space increased from 62 GiB to 76 GiB; affected historical manifests are provenance-only.

## Tenth compaction after the sealed round-1538 audit

After audit `ec7e14549b8d54112a0f502a22b1f908ebdd8566b97fe8e25fda20f313141159`, replay `7e571aa3dca04a1ca3300ce66b90c57eeba4a5df62df6fcdb9745824c66c4510`, and manifest `ceca434e7afc85e51b139781f4e32ec59bfc07834920dea9e2951b6fc964b2f0` sealed all six exact edges through round 1538, these ancestor payloads were pruned:

- `production_from_round1527_cap2750_to1538/stage01_cap1529` through `stage05_cap1537`: only `{checkpoint.bin,vectors.bin}`.
- `round1527-direct-cap2750-gate/candidate_cap2750/{checkpoint.bin,vectors.bin}`.

The sole restart payload is `production_from_round1527_cap2750_to1538/stage06_cap1538`, reverified after cleanup at checkpoint SHA `d436b820bdc1746d2c99a46e22fcc83dcd354836bce76223cb071fdb2aabf607` and cache SHA `c8527569930d927c9f4f2e1935635c8b9cb372444f6b8d6b991830d973d6f972`. Small results, watchdog telemetry, audits, reports, and historical hashes remain. Free space increased from 46 GiB to 76 GiB; affected historical manifests are provenance-only.

## Eleventh compaction after the sealed round-1550 audit

After audit `6f29cd96d8083fe5ace24c1937fbf8daa5eed34b9009168f3016edd59347a1f0`, replay `632f02be3980136464d1285edec9bf83777cd06e1ef439153d46bdd4c2593a4d`, and manifest `a4166eac14e97995f7486e75bdf016abe810565126347bf4c853b268179de3e4` sealed all six exact edges through round 1550, these ancestor payloads were pruned:

- `production_from_round1538_cap2750_to1550/stage01_cap1540` through `stage05_cap1548`: only `{checkpoint.bin,vectors.bin}`.
- `production_from_round1527_cap2750_to1538/stage06_cap1538/{checkpoint.bin,vectors.bin}`.

The sole restart payload is `production_from_round1538_cap2750_to1550/stage06_cap1550`, reverified after cleanup at checkpoint SHA `1c3e84f5cd97a44886b99d17f6f1a178d3cb5802c2254a95ad90f78dee9c10e3` and cache SHA `1ee5934a99dc70a15ecd651fec7ec1886891026bddf338c3f1b7430d066bdc12`. Small results, watchdog telemetry, audits, reports, and historical hashes remain. Free space increased from 45 GiB to 76 GiB; affected historical manifests are provenance-only.

## Twelfth compaction after the sealed round-1562 audit

After audit `3dc3165fc382de8084d52092c4a52f76c9551ec745a8e2238ef3d2ef1d109772`, replay `dfb6e90981f79c4a413370fd76fcbc8b23ac292e730177ede7b3027774b2fdd9`, and manifest `8184d24ffc503a89a042e50d83accd85e588cc4a377670071894cfdff711d629` sealed all six exact edges through round 1562, these ancestor payloads were pruned:

- `production_from_round1550_cap2750_to1562/stage01_cap1552` through `stage05_cap1560`: only `{checkpoint.bin,vectors.bin}`.
- `production_from_round1538_cap2750_to1550/stage06_cap1550/{checkpoint.bin,vectors.bin}`.

The sole restart payload is `production_from_round1550_cap2750_to1562/stage06_cap1562`, reverified after cleanup at checkpoint SHA `1273f400531e889b304d05ada9b0d3611747e7a108dd8791c116da063bdbe37e` and cache SHA `194b364a86d50d1763952c90389c7c5556094edd7ee139f5c48578c3b720d7fe`. Small results, watchdog telemetry, audits, reports, and historical hashes remain. Free space increased from 43 GiB to 75 GiB; affected historical manifests are provenance-only.

## Thirteenth compaction after the sealed round-1563 cap gate

After audit `72d4e628243010d898a2554e1900c61a9a578eb25e2118227bd19d226fe6a366` and manifest `bf6e8bda1690f9a73617011def61a220b319baf7e7819056dc8dee90d647cad9` sealed the byte-identical 2.75m and 3.0m outputs, these redundant payloads were pruned:

- `round1563-direct-cap3000-gate/control_cap2750/{checkpoint.bin,vectors.bin}`.
- `production_from_round1550_cap2750_to1562/stage06_cap1562/{checkpoint.bin,vectors.bin}`.

The sole restart payload is the accepted `round1563-direct-cap3000-gate/candidate_cap3000` state, reverified after cleanup at checkpoint SHA `a21b5b592b5443504acc2a8625f482f6ae052cb990105bd36a7a877ae188a1fd` and cache SHA `06d202cf07a189090ae1d91298f10bcac8bcc384ea4052415c7fd4a5724445e1`. Small results, telemetry, audit records, reports, and hashes remain. Free space increased from 64 GiB to 75 GiB; affected historical manifests are provenance-only.

## Fourteenth compaction after the sealed round-1575 audit

After audit `18ef0df39c89db7fde0ad55624276556ceca17ab481135ee897415a365be3f01`, replay `2e0992a62e22eeba2a2f4d13104b1d569f00993a63c94c221bb24d1ca67cb48d`, and manifest `8ae211e3498528e33eb91686d9824298e6f76c7cc76e0f16c3cea624a5ca9c06` sealed all six exact edges through round 1575, these ancestor payloads were pruned:

- `production_from_round1563_cap3000_to1575/stage01_cap1565` through `stage05_cap1573`: only `{checkpoint.bin,vectors.bin}`.
- `round1563-direct-cap3000-gate/candidate_cap3000/{checkpoint.bin,vectors.bin}`.

The sole restart payload is `production_from_round1563_cap3000_to1575/stage06_cap1575`, reverified after cleanup at checkpoint SHA `2012b6bcb82d9b4e873a23bb359b9285c9f2bb8fef080e18457648b127faba89` and cache SHA `82f85642cd0f1cd1062f748ee2dd661b0e4044cf1695076f72c9dd241f726ce0`. Small results, watchdog telemetry, audits, reports, and historical hashes remain. Free space increased from 42 GiB to 75 GiB; affected historical manifests are provenance-only.

## Fifteenth compaction during the round-1583 disk hold

The active round-1575 to round-1587 chain stopped after exact stage04 at round 1583 because free space was 55.49 GiB, below its frozen 56 GiB launch floor. The old round-1161 to round-1261 production chain had already been independently sealed by audit `08a51b48b94a60e0bada4c9cb692b7824b7850ca464ec104f6d952d1b907d707` and manifest `6d6afafd615117f58c91eabb1e3ebb5f348918860636e3b2011cab668c0f8dc0`. The following superseded payloads were therefore pruned:

- `production_from_round1161_portfolio_cap1250/stage01` through `stage10`: only `{checkpoint.bin,vectors.bin}`.

All small results, telemetry, reports, audit records, and historical hashes remain. Every payload in the active round-1575 to round-1583 chain, plus its sealed round-1575 input, was preserved. Free space increased from 55.49 GiB to 78 GiB. The old round-1261 manifest is now provenance-only rather than fully locally replayable.

## Sixteenth compaction after the sealed round-1587 audit

After audit `f148d502cc6eaeb69c50b4fe033f290a664b56648db39da14139db2bd3acae33`, replay `3c09ec1597d970d91d09ae3ec9ab94ccd07e83548e09e3ad7d33b41f8edc7b52`, and manifest `ba2235a3208101134d823da5b648312bd70e900b4a3bd181250fd32005f6cbc4` sealed all six exact edges through round 1587, these ancestor payloads were pruned:

- `production_from_round1575_cap3000_to1587/stage01_cap1577` through `stage05_cap1585`: only `{checkpoint.bin,vectors.bin}`.
- `production_from_round1563_cap3000_to1575/stage06_cap1575/{checkpoint.bin,vectors.bin}`.

The sole restart payload is `production_from_round1575_cap3000_to1587/stage06_cap1587`, reverified after cleanup at checkpoint SHA `f8c334186186173654878c9f33f4c0d5f1911724e9c95cf5069b2fbd0c89f8aa` and cache SHA `38a4ff6bb1d8f0d39cb7c4914e0e549629fe37df069db2436874cb5ce51f41ae`. Small results, watchdog telemetry, producer and audit reports, manifests, and historical hashes remain. Free space increased from 65.40 GiB to 100.23 GiB; affected historical producer manifests are provenance-only.

## Seventeenth compaction after the sealed round-1588 cap gate

After independent cap-gate audit `199b17ef8c8ae718ff5644dd4cd0ecf63b1eb18fdb5663255783ca52539e1df5` and manifest `f3575992d851e0ae5afb91423edb1092359008da82d64ab2b28e6a856ad13817` sealed byte-identical round-1588 control and candidate states, these superseded payloads were pruned:

- `round1588-direct-cap3250-gate/control_cap3000/{checkpoint.bin,vectors.bin}`.
- `production_from_round1575_cap3000_to1587/stage06_cap1587/{checkpoint.bin,vectors.bin}`.

The sole restart payload is `round1588-direct-cap3250-gate/candidate_cap3250`, reverified after cleanup at checkpoint SHA `e94a0965eb8d9a7bbb602726635093b9e0ca27a9d9af0ea38703a8bf3498d5b6` and cache SHA `c4ae2b91e86f4b373f078304d0d79416970bd636d97912b25eadc45c86428e05`. Small cap-gate results, watchdog telemetry, producer and independent audit reports, manifests, and historical hashes remain. Free space increased from 88.26 GiB to 100.20 GiB; affected historical manifests are provenance-only.

## Eighteenth compaction after the sealed round-1600 audit

After audit `81b35e8d3c0e3853534990cbc5c975e0db47248c60275bebb175913dd3f35997`, replay `e101f3adf101c6893353bd6e039ce41a72b4903a4389d1f298b3a2ad2980782d`, and manifest `56c2dbb8d6542530c9877933b2651688a5a0e0404a01a6ae6adea59fe8eee4d4` sealed all six exact edges through round 1600, these ancestor payloads were pruned:

- `production_from_round1588_cap3250_to1600/stage01_cap1590` through `stage05_cap1598`: only `{checkpoint.bin,vectors.bin}`.
- `round1588-direct-cap3250-gate/candidate_cap3250/{checkpoint.bin,vectors.bin}`.

The sole restart payload is `production_from_round1588_cap3250_to1600/stage06_cap1600`, reverified after cleanup at checkpoint SHA `b0f8e3f0789f703577929f4b4612155da1fde7d16ad35d541d6bad8563881a6c` and cache SHA `acd25d4324fc20e67009d1f4e2e5b1fccb04571ba31cc5dc44f0e9e44d23e2a7`. Small results, watchdog telemetry, producer and independent audit reports, manifests, and historical hashes remain. Free space increased from 70.21 GiB to 106.87 GiB; affected historical manifests are provenance-only.

## Nineteenth compaction after the sealed round-1601 cap gate

After independent cap-gate audit `ab839af1011cf3416628627739db8063066ff636b74557df39236c87d177f576` and manifest `6dad4784871c8041a528dacd7f4b3fd3605d7a45451d9c15cd672a68e7f469d7` sealed byte-identical round-1601 control and candidate states, these superseded payloads were pruned:

- `round1601-direct-cap3500-gate/control_cap3250/{checkpoint.bin,vectors.bin}`.
- `production_from_round1588_cap3250_to1600/stage06_cap1600/{checkpoint.bin,vectors.bin}`.

The sole restart payload is `round1601-direct-cap3500-gate/candidate_cap3500`, reverified after cleanup at checkpoint SHA `83955dbcc460c5fe39623e25b8337eb80bcfc9921eeafb4c1a887cfa6f5abb01` and cache SHA `c9d850754e9451015a3bf4fa6b51d6f0bb8c3ecdaeecbdef456abaa5fae7b046`. Small cap-gate results, watchdog telemetry, producer and independent audit reports, manifests, and historical hashes remain. Free space increased from 94.22 GiB to 106.84 GiB; affected historical manifests are provenance-only.

## Twentieth compaction during the round-1609 proactive disk hold

The active round-1601 to round-1613 chain stopped after exact round1609 because free space was `64,504,356` KiB, below the proactive64 GiB continuation threshold. The old round-1061 to round-1160 chain was independently sealed by audit `50a07613b21071f9981917be3b87cd6ff84b9bd63284a89760cf096cb4acf7e4`, replay `4fb3f3da96b111001e9d678217601e019f88ae05361b414b7f540c007bf8ed7f`, and manifest `e56759b60118d50402af20041477c93a2e0ac317556c7fd94b0cdf4d490e2c42`. Exactly14 payload files totaling12,892,568 KiB were pruned:

- `production_from_round1061_portfolio/stage01` through `stage07`: only `{checkpoint.bin,vectors.bin}` in each accepted stage.

All small old results, telemetry, reports, audit records, manifests, and historical hashes remain. Every artifact in the active round-1601 to round-1609 chain remains untouched. The current endpoint was reverified after cleanup at checkpoint SHA `a526aec2670403a0f1a6fc0da8264a71eb97ce3c2a94846a35caa530b4b6ebed` and cache SHA `8b95c9752f281dc6cf9f6b2125b4cb3b51dce8e8ba7100132915d64addd6efde`. Free space increased to `77,394,828` KiB. The old round-1160 producer manifest is now provenance-only rather than fully locally replayable.

## Twenty-first compaction during the round-1611 proactive disk hold

The active chain stopped after exact round1611 because free space was `63,508,308` KiB, below the proactive64 GiB continuation threshold. Two old superseded producer families were independently sealed and therefore selected:

- `production_from_round961/stage01` through `stage05`: only `{checkpoint.bin,vectors.bin}`; sealed by round1060 audit `db44359c43989b36232c0cb927439924fd8e9d627c4c17398ce27e4299123832`, replay `95b4f430358f4e398d0465fb75b7b1481a418e02722a705809664b87f6930657`, manifest `7c1649f025dfa9286955e4322a166ef2691a72443e8f1075adf4db6e4584365a`.
- `production_from_round1343_cap1750/stage01` through `stage03`: only `{checkpoint.bin,vectors.bin}`; sealed by round1362 audit `7386c9d8f24cba33a014f7b90930543ffd2246a265a237c571acd5f321bdb24d`, replay `d1065e121399c72b3787aaaec8ef8f5c042e4cdf94d6ec245b8ad25ea26ecb82`, manifest `ab0d32a92c64191d5f67c786f291462b740497deb01b6b4304a6e063e83b8021`.

Exactly16 payload files totaling17,075,600 KiB were removed. All small old results, telemetry, reports, audits, manifests, and historical hashes remain, and every active round-1601 to round-1611 artifact is untouched. The current endpoint reverified at checkpoint SHA `d93745bcbbf682962bede4ad95236ba94a5c518cbe41e9d73e433a3d11027da0` and cache SHA `1bd24f93ec20ca11e739268b5a0e89667faefb23e85fd3f03a608d4ea0c37596`. Free space increased to `79,030,468` KiB. Both old producer manifests are now provenance-only rather than fully locally replayable.

## Twenty-second compaction during the round-1636 disk hold

The active round-1627 to round-1639 chain stopped after exact round1636 because
free space was `75,839,904 KiB`, only `342,432 KiB` above the frozen
`75,497,472 KiB` prelaunch reserve. Read-only audit
`production_from_round1627_cap4000_to1639/STORAGE_AUDIT_R1636.md` SHA-256
`65c682d57b3d4a83b35d7c4e37d0cf952a1e1e07e2623a72357600cc894f8e6b`
enumerated exactly18 obsolete payloads totaling `30,085,734,229` logical bytes
(`28.019523 GiB`). Explicit authorization was then given to remove only the
following files (relative paths abbreviated below; every small evidence file
was retained):

| Removed checkpoint/cache payload | Bytes | Pre-delete SHA-256 |
| --- | ---: | --- |
| `round1464-external-sequential-six-cap2500-design/lane00_repair_first/checkpoint.bin` | 30,793,148 | `1b4dde9f009b4343099190e293913818b3df88dfc34c27653e7cfcd4acf08c8e` |
| same `vectors.bin` | 4,444,850,137 | `46744c37b6c1ab30e6ce945a9f049e45683b4324470e661554f4ae4134b9d48c` |
| `production_from_round1363_portfolio_cap2000/stage15/checkpoint.bin` | 29,599,730 | `82d53e68e3f1bd483518996fed2dbffa80910163e8c7234f9ccce7c88afeb3cb` |
| same `vectors.bin` | 4,221,170,622 | `1fd9cd661feef3957c0dda310b3213ff11784a48c520b76d73323e950a9db7c1` |
| `round1363-internal-sequential-portfolio-cap2000-design/cap2000_candidate/checkpoint.bin` | 23,854,415 | `91d573bcfbb2e43f0832a595c899b7c5bd411845cb8323cbcff1c5d7728f92e1` |
| same `vectors.bin` | 3,439,222,065 | `5c39cf56b3504a44f8e002f9ad3e42b533855d6217e5e5f9967543f6d77e0e5e` |
| `production_from_round1262_portfolio_cap1500/stage10/checkpoint.bin` | 22,418,438 | `7e3174c8a87bccd1af517ce3adba98eded04cf31a203c079d213ee067831aca5` |
| same `vectors.bin` | 3,231,636,588 | `852c711f33392140621f98d73037605370211d83eaaef232052577e6cdc3f99b` |
| `round1262-internal-sequential-portfolio-cap1500/selected_control/checkpoint.bin` | 18,635,867 | `2d9f65c918f2eac295c8e642f60d57d43458fe98efd40aed325062c10254225e` |
| same `vectors.bin` | 2,686,377,737 | `00437f95d845567b9082a25a97be738fd4a94d14e20e1afec556f9f95c726a9e` |
| same package `portfolio/checkpoint.bin` | 18,635,867 | `2d9f65c918f2eac295c8e642f60d57d43458fe98efd40aed325062c10254225e` |
| same package `portfolio/vectors.bin` | 2,686,377,737 | `00437f95d845567b9082a25a97be738fd4a94d14e20e1afec556f9f95c726a9e` |
| same package `cap1500_candidate/checkpoint.bin` | 18,635,867 | `2d9f65c918f2eac295c8e642f60d57d43458fe98efd40aed325062c10254225e` |
| same package `cap1500_candidate/vectors.bin` | 2,686,377,737 | `00437f95d845567b9082a25a97be738fd4a94d14e20e1afec556f9f95c726a9e` |
| `round1343-cap1750-gate/cap1750_candidate/checkpoint.bin` | 22,483,538 | `d2dbdee814cecca8f8528d84d2f386d3f042a54b62039a0350a834b5a1949dcf` |
| same `vectors.bin` | 3,241,090,599 | `d5517dfdc00cb7c2e0844b2459385576dd84211eceebe3a0cb94815a1cd7a2c6` |
| same gate `cap1500_control/checkpoint.bin` | 22,483,538 | `d2dbdee814cecca8f8528d84d2f386d3f042a54b62039a0350a834b5a1949dcf` |
| same gate `cap1500_control/vectors.bin` | 3,241,090,599 | `d5517dfdc00cb7c2e0844b2459385576dd84211eceebe3a0cb94815a1cd7a2c6` |

All 18 paths were verified absent. All small failure evidence, results,
watchdogs, audits, reports, and manifests remain. The active round-1627 to
round-1636 chain, its accepted input, and `stage09_refused_wrapper155_attempt`
remain untouched. Free space rose to `105,257,964 KiB`, a measured physical
recovery of `29,418,060 KiB`.

The accepted round1636 endpoint was rehashed after cleanup: result
`636e6abd9ae0e00819d87f2963275921669e95d09955d1fbc24c9b5b7691d8a2`,
watchdog
`b9d87616b11ccb79680746e06d058ffcf52fd05fd4b72ce7515254eb0307d89f`,
checkpoint
`5f29efd99b81830a3aea35707ff91acc7847d0d86b1bc4277c9b076794ebd1a9`,
and cache
`8553a5bff1404d882bd604987bf15ecc1c548677411e6a64e32ac1d78b3e09e9`.
Historical manifests naming removed payloads remain provenance records but are
intentionally no longer fully locally replayable.

## Twenty-third compaction after the sealed round-1639 audit

Independent audit
`a99a307f99bd88f8b363ca73bbc3af631a333bab228fbdb43c3e604382150387`,
replay `4996c85de7aedf853ba6428e948b69e88a5a07d170614ce9fea5f98714d3c5e5`,
and manifest
`de3d1a5e390e0545d5f4c5bca7b7f20fa9205056a772bbd8d1ca841e7ae98b0c`
sealed all twelve exact descendant edges and the full round-1639 cache replay.
Input cap-gate audit `c43b18138cbca585e5256ee5809e94ed16d96eefa3771b695cd93850c53d039b`
and manifest
`20441719604745ddcdb7c12a75111bb27aa3ee4477d12c4b135c76fc5069530f`
sealed the superseded round-1627 input. After an explicit 24-file authorization,
only the following `checkpoint.bin` / `vectors.bin` pairs were removed:

| Removed pair | Logical bytes | Checkpoint SHA-256 | Cache SHA-256 |
| --- | ---: | --- | --- |
| `production_from_round1627_cap4000_to1639/stage01_cap1628` | 7,778,299,591 | `c0fb9e17adb46e673793764d27a33bc90f9f8848f447deb8f700c47b23f648a0` | `d99b03cba91a41910651155e915eba773e91f0af77799add1b2cb2a5a3592558` |
| `stage02_cap1629` | 7,829,780,094 | `0bca25a8bb159759834aec67246f161ef3a55facbfbab187db2170414c442829` | `46d2b90238ba9903a46a1b1a53b6f184fd803545c334279d933393f5e018f29f` |
| `stage03_cap1630` | 7,878,931,665 | `3d31c264851af243a087e1b73adc57dc72025cf2e037adfd52c27b9ac03c2001` | `2c59fab0b9f958c48909590de4cff1edbb3e5f094b2b8983cde69bc757b0e1e3` |
| `stage04_cap1631` | 7,929,050,263 | `0de6b8295b5748c8a8320b0b8d60c7d53a7eef6842dd140792c37bb8f2b768ba` | `b3fc6e72c6376c3c77b27f3e7bf1194dfa96f787698e4bd348c66ca3e38adcbe` |
| `stage05_cap1632` | 7,991,866,413 | `e57beb640390ec9ba52fae4d92aeeb2269cd1147664bd065fea6d90229711724` | `d3c8069d9322c61eb61c852d053b00d7d723d51eb67de18643e8c9474f66c928` |
| `stage06_cap1633` | 8,064,101,310 | `a116ad43391afefc48566c9ebdca0740fe05eb84b66eb707a7e023eb393b7513` | `fadb9065a7282244e7512cbf023b23050e871a781b8bb948384adb2203a1036c` |
| `stage07_cap1634` | 8,117,610,457 | `f98fe5f757edf86b3b9ed1465811b5177f097df711cd74db86e7dc69149b9b82` | `2aea413a930a1ecd829b834738a5b12dc90e34d73f425ec7430850b7b9459eab` |
| `stage08_cap1635` | 8,181,112,710 | `83c6880c204ff1b26b486b24bc3c8688161e3a7065c6a3cb9dbfba2d965395b0` | `97fdb106abb96a90c0a8e2be225f9d75a71f570e5d93e3e228a1bf7df3fa77c6` |
| `stage09_cap1636` | 8,271,512,865 | `5f29efd99b81830a3aea35707ff91acc7847d0d86b1bc4277c9b076794ebd1a9` | `8553a5bff1404d882bd604987bf15ecc1c548677411e6a64e32ac1d78b3e09e9` |
| `stage10_cap1637` | 8,373,250,635 | `e023904608f10820540436db441015889847fef46df5070bdbaf6d62d5e58409` | `b8b63baf8f870f8f02fbf0d0e1670c7726960fa8d89e39350da2e57a37acb9b1` |
| `stage11_cap1638` | 8,493,656,326 | `fbd7b331b841db3f39b39756329dffd883c1be70f4b18eabcc737f1a00d5c473` | `9194444687fd3ed732bac86726586ccebcabadd4c3c4dc486664b5883e555b17` |
| `round1627-direct-cap4000-gate/candidate_cap4000` | 7,732,170,228 | `40a76f726f40fb022909f219b6ace5d8ee5f04fb5847cb1e37a3cea2829e308e` | `4ae60b262d5bdcea3488ed0bb194e95d338bb962beb172cec33e9ddc76de8eeb` |

Exactly 24 files totaling `96,641,342,557` logical bytes (`90.004264 GiB`)
were removed. Free space rose from `79,197,948 KiB` to `165,607,036 KiB`, a
measured physical recovery of `86,409,088 KiB`. All stage results, watchdogs,
logs, plans, amendments, refusal evidence, producer/audit reports, and manifests
remain. The protected `stage09_refused_wrapper155_attempt` pair and complete
`stage12_cap1639` endpoint remain. Historical manifests naming removed payloads
are retained as provenance but are intentionally no longer fully locally
replayable.
