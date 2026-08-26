# Post-audit compaction at round 1626

Status: PASS

Independent seal pins: audit `a11616069bccd77c1515946ca9d23d589533b575d98f25657903b6428843d5b6`, replay `8e5fc3a87ad3c0fdd40e474bb7f387862e0adc783165114ae3c2ea1a4e1e1e4c`, manifest `a1e5a4cc90635308341145f07ca51dd0f7b8ddb997df7b917d05f7f53f405684`. The replay covered3,528,325 columns with zero failures.

Pre-execution free space:61,158,440 KiB.

Exactly24 superseded payload paths are authorized; every small evidence file and the stage12 endpoint remain:

- `stage01_cap1615/checkpoint.bin`
- `stage01_cap1615/vectors.bin`
- `stage02_cap1616/checkpoint.bin`
- `stage02_cap1616/vectors.bin`
- `stage03_cap1617/checkpoint.bin`
- `stage03_cap1617/vectors.bin`
- `stage04_cap1618/checkpoint.bin`
- `stage04_cap1618/vectors.bin`
- `stage05_cap1619/checkpoint.bin`
- `stage05_cap1619/vectors.bin`
- `stage06_cap1620/checkpoint.bin`
- `stage06_cap1620/vectors.bin`
- `stage07_cap1621/checkpoint.bin`
- `stage07_cap1621/vectors.bin`
- `stage08_cap1622/checkpoint.bin`
- `stage08_cap1622/vectors.bin`
- `stage09_cap1623/checkpoint.bin`
- `stage09_cap1623/vectors.bin`
- `stage10_cap1624/checkpoint.bin`
- `stage10_cap1624/vectors.bin`
- `stage11_cap1625/checkpoint.bin`
- `stage11_cap1625/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-round1614-direct-cap3750-gate-2026-08-25/candidate_cap3750/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-round1614-direct-cap3750-gate-2026-08-25/candidate_cap3750/vectors.bin`

The deleted stage payload hashes remain pinned in `MANIFEST.sha256`. The old candidate hashes are checkpoint `4c84bb8978083a0b2437bcc10730b40fc260fce90068f597c408789546c7f76e` and cache `ab1da9e006abd643b977fe1af879c9f7c7ee99b80be95ac82fcb71c9a960d88d`.

Retained endpoint expected hashes: checkpoint `bbee936b4c53882f075c6afb9ec7284ddc36ba29608fa7bdb27062beb54ebdb3`, cache `0dd351df751dc83afecc8b456736b7b45e4c814538b3244a4d9b1f11180a5402`.

Post-execution verification: all24 enumerated paths are absent; free space increased to148,433,696 KiB; the retained checkpoint rehash is `bbee936b4c53882f075c6afb9ec7284ddc36ba29608fa7bdb27062beb54ebdb3` and cache rehash is `0dd351df751dc83afecc8b456736b7b45e4c814538b3244a4d9b1f11180a5402`. The frozen83,886,080 KiB two-clone floor passes.
