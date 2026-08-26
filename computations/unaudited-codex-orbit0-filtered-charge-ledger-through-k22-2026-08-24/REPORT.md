# Corrected exact charge ledger through complete K22

Status: **PASS_CORRECTED_COMPLETE_CHARGE_LEDGER_THROUGH_K22**.

The complete K22 charge is `4753487002993355488/173867925` over 76/76 frozen IDs. Adding it to the pinned cumulative K14--K21 charge gives

`cumulative(K14..K22) = 144864541808678432/11591195`.

The degree charges now pinned are:

| degree | exact charge | coverage where applicable |
|---|---:|---:|
| K14 | 0 | -- |
| K15 | 0 | -- |
| K16 | 375127296 | -- |
| K17 | -9747200926208/6545 | -- |
| K18 | 109863564487489024/24838275 | 17 |
| K19 | -2117855228554753792/173867925 | 24 |
| K20 | 12162234158979734656/521603775 | 36 |
| K21 | -15276224591027275648/521603775 | 52 |
| K22 | 4753487002993355488/173867925 | 76 |

The unallocated conservation residual after K22 is `-144864541808678432/11591195`. It is aggregate arithmetic only; `future_degree_allocation` is explicitly null, so the ledger assigns no charge or membership statement to K23 or K24.

The assembler pins the complete through-K21 ledger, K22 manifest, and K22 result by SHA-256; standard, optimized, and isolated self-tests reject incomplete K22 and deleted-manifest-group mutations.

Replay:

```sh
python3 computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k22-2026-08-24/assemble_charge_ledger_through_k22.py --self-test
python3 computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k22-2026-08-24/assemble_charge_ledger_through_k22.py
```
