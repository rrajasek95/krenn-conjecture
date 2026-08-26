# Exact K22 direct D17--D19 source fold: 23 IDs

Status: **PASS** for the four frozen grouped scalars covering exactly 23 K22 IDs. This is a strict partial K22 fragment, not a complete 76-ID result and not a membership/conjecture claim.

The exact subtotal is

`910250654231506452480 / U = 79529288704/35`, with `U=400591699200`.

| group | IDs | source / pivotable / p1 | p2 | terminal K22 | scaled charge | exact charge |
|---|---:|---:|---:|---:|---:|---:|
| D17 R2-3 | 7 | 82,938,880 / 81,076,480 / 267,564,800 | 1,448,947,200 | 46,366,310,400 | 784632481068586106880 | 68553933824/35 |
| D17 R3-2 | 7 | 82,938,880 / 81,076,480 / 267,564,800 | 842,301,440 | 10,107,617,280 | 50007380854859366400 | 124833792 |
| D18 R2-2 | 6 | 152,251,200 / 137,817,600 / 260,736,000 | 230,937,600 | 2,771,251,200 | -15902862330455654400 | -39698432 |
| D19 R3 | 3 | 167,616,000 / 111,744,000 / 111,744,000 | -- | 3,575,808,000 | 91513654638516633600 | 228446208 |

The source coefficient is `-M`. Thus the one-response D19 contribution is `+M/m1`, and every two-response D17/D18 contribution is `-M/(m1*m2)`. For every literal terminal child, the response routine checks all frozen pivots and asserts `full_n=irreducible_n` and `full_q=irreducible_q` occurrencewise.

The 8-record/8-worker gate completed in 6.405440 seconds (388.33-second projection). The complete 485-record/8-worker run completed atomically in 410.380572 seconds. Observed process RSS peaked at 5,288,400 KiB (5.04 GiB), below 16 GiB. Caches were reset per source record; full peak cardinalities per record were 1,640,960 first-response keys and 522,062 terminal keys.

The independent referee replayed all 257 deterministic distributed samples (R8 indices `floor(j*484/256)`). For each it reconstructed the literal source family, first replacement, second pivot, every terminal K3/K2 child, 77-charge, irreducibility, divisor, sign, U-scaled unit, and nonzero contribution.

K23/K24 were deliberately not multiplexed: the K20-parent path would add 32+60 terminal tails to each required 12-tail response, which is not negligible and violates the measured-gate premise.

Recheck with:

```sh
python3 computations/unaudited-codex-orbit0-k22-direct23-source-fold-2026-08-24/verify_k22_direct23_package.py
computations/unaudited-codex-orbit0-k22-direct23-source-fold-2026-08-24/referee_k22_direct23_literals computations/unaudited-codex-orbit0-k22-direct23-source-fold-2026-08-24/results_k22_direct23.json.samples.tsv
python3 computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/assemble_k22_76_exact.py --audit-incomplete computations/unaudited-codex-orbit0-k22-direct23-source-fold-2026-08-24/k22_direct23_fragment_manifest.json /tmp/k22_direct23_partial_audit.json
```

Authoritative pins are checked by `verify_k22_direct23_package.py`: structure `55e382...`, aux `f8c783...`, cycle `8213a3...`, K4 tails `4cec01...`, and frozen expected groups `e2e2ba...`.
