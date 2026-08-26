# Complete exact K22 charge: 76 frozen IDs

Status: **PASS_COMPLETE_K22_76_ID_EXACT_Q**.

Exactly the seven authorized sealed families close the frozen K22 interface:

| family | IDs | scalar groups |
|---|---:|---:|
| profile-ready | 16 | 4 |
| hidden collected K18 | 2 | 2 |
| direct D17--D19 | 23 | 4 |
| hidden pair | 2 | 2 |
| grouped direct K15 | 12 | 4 |
| D14 source-three | 3 | 3 |
| grouped direct K16 | 18 | 3 |
| **total** | **76** | **22** |

The exact K22 charge is

`10952034054896691044352 / U = 4753487002993355488/173867925`, with `U=400591699200`.

Full and irreducible charges agree. Coverage is exactly 76/76 with empty missing, duplicate, and extra lists. Grouped scalars are counted once, irrespective of the number of IDs they cover. Every evidence file is byte-hash pinned in the manifest.

The frozen assembler produced byte-identical result JSON under standard Python, `-O`, and `-I -S` (SHA-256 `7e955126...`). Its self-test and the independent package audit reject missing, duplicated, unexpected, wrong-U, full/irreducible-mismatched, and bad-evidence-hash manifests under all three modes.

Pins:

- Complete manifest SHA-256: `731f6a111ce02ce2bfb40ccf465f0c7c631f1ed68106647ab5ca33288c82fdfe`
- Complete result SHA-256: `7e955126cf391d2b6cfcbbb694004a2a5a8915981332cd9cc80e26460d7624f1`
- Manifest logical SHA-256: `0e3eba5543651bb4ca23dfc13b311eeded912a55dffc6455b9a45d56019c8d75`
- Frozen DAG logical SHA-256: `ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66`

Replay:

```sh
python3 computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/build_k22_manifest_complete_76.py
python3 computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/assemble_k22_76_exact.py computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/k22_manifest_complete_76.json computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/results_k22_complete_76_exact.json
python3 computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/audit_k22_complete_76.py
```

Scope is complete K22 charge only. No K23 or K24 scalar, allocation, membership, or conjecture conclusion is inferred.
