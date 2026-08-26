# Complete K18 77-cycle charge after the hidden `[2,2]` repair

**Terminal result: PASS.**  The missing lineage `D14:222|R:2-2` was evaluated exactly from all 6,229,700 recovered nonzero profiles, and the corrected K18 charge now covers all 17 paths in the frozen K14--K24 recurrence DAG.

## Why profile aggregation is sound

For a fixed K2 tail, both quantities used by this computation are row-local:

- the 77-cycle charge depends only on the child row, hence on `(profile, pivot, K2 tail)`;
- K18 pivotability depends only on the child's support/signature, hence on `(signature, pivot, K2 tail)`.

Consequently each full or irreducible charge is a linear functional of the signed parent coefficient. Summing duplicate parents into a signed profile weight before emitting their 12 K2 tails gives the same answer as emitting every literal occurrence and cancelling afterward. This is a charge statement only; it does not construct a canonical K18 row checkpoint or any later tail.

The literal prefix guard checked all 752,136 children of the 62,678-key prefix. It independently summed the 694,172 canonical child rows (408,972 pivotable) and reproduced both profile sums exactly:

| quantity | scaled value |
|---|---:|
| full prefix charge | 5,001,460,982,954,459,136 |
| irreducible prefix charge | 3,397,187,219,754,516,480 |

## Missing `[2,2]` component

The full pass emitted 74,756,400 profile-tail terms and retained 39,922,118 irreducible terms. These are terms after signed profile aggregation, not literal source-occurrence counts.

| quantity | scaled by `U=400591699200` | reduced rational |
|---|---:|---:|
| full charge | 1,040,847,708,648,504,360,960 | `90351363597960448/34773585` |
| irreducible charge | 661,934,270,121,770,483,712 | `41042551470843904/24838275` |

The exact run took 6.55 seconds and stored no child rows.

## Corrected complete K18 charge

Adding the repaired path to the previously enumerated 16-path subtotal gives:

| scope | full | irreducible |
|---|---:|---:|
| old 16-path subtotal | `82802576789248/21505` | `2590664898048/935` |
| hidden `[2,2]` repair | `90351363597960448/34773585` | `41042551470843904/24838275` |
| **complete 17-path total** | **`224243130266174464/34773585`** | **`109863564487489024/24838275`** |

The DAG replay finds no missing or extra K18 paths. Coverage is: six direct K18 paths, one K14 `[4]`, three K15 `[3]`, six K16 `[2]`, and the recovered K14 `[2,2]` path.

## Replay and scope

- Missing-component runner: `run_full_hidden_k2_charge.rs` (SHA-256 `265d244ffa35f49e3dbb1df6d7217a1764722db875e8573950670d23421c58b3`)
- Missing-component result: `results_missing_k18_22_charge.json` (SHA-256 `d8a518ce2061c72c23a55205dd863501495c006407f43b68255e443026dd1684`)
- Assembly checker: `assemble_complete_k18_charge.py` (SHA-256 `75e633200f86a4560a84fd60ab8ae8e569b1161aa62489d1b60138568f59b8aa`)
- Complete result: `results_complete_k18_charge.json` (SHA-256 `419d2cb639200a9e07b74faa2f6576cba64951acf042a359dbd3a3d145a537cd`, logical SHA-256 `a8f22e290cfbfcfced076441a70ebed426877f568c6e534961e5759fdfb33e74`)

This proves the exact immediate full and irreducible 77-cycle charge at K18 for the complete frozen recurrence policy. It makes no K18 row-membership claim, emits no subsequent pivot tails, and does not address K20.
