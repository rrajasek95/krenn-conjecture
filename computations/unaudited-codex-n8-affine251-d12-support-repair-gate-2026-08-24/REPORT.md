# Exact D12 round-731 support-repair gate

## Outcome

The bounded gate is exact and independently replayed, but the optimization is **rejected**. Both requested support restrictions solve all 315,301 exposed equations with target coefficient 1 and zero violations. They are 13.04x--14.28x faster than the sealed cold/rare solve, but their common global incident frontier has 10,466 columns versus 1,268 for cold/rare (8.253943x worse). The required "frontier no worse" promotion condition therefore fails.

No continuation beyond round 731 was run, no main-package source was edited, and no computation remains active.

## Frozen scope

- Provider: `canonical_triangle_pair_offdiag_full_p32003.ms`, 19,242,994 bytes, SHA-256 `75a82d82a979d75507e682fd339e83d4ae35949653d624fb541148bd3957dcff`.
- Round-730 checkpoint: 314,080 columns, support 484, SHA-256 `8bfd09b0b810933957cae3191c4725fc79e4734512da2a060ff398ad8566c7b2`.
- Round-731 checkpoint: 315,301 columns, sealed cold/rare support 499, SHA-256 `8f2e0779d64ca14a46d019519280a33cb60633ffe1909cacc96885fbbbcefc65`.
- Exact round-731 vector cache: 31,973,746 vector entries, SHA-256 `475a62b585429d3f0c96cd59c922124f5f46909a5bbe96266b989049afa2d523`.
- The sibling was cloned from the restored original affine251 source SHA-256 `241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`; its gate-specific source and binary are pinned in `PINS.json`.

The 1,221 newly exposed columns contain 116,135 distinct non-target rows. Of these, 66,332 do not occur in the prior 314,080-column universe. The two fail-closed systems were:

1. prior candidate support union the 66,332 new-only rows: 66,816 allowed variables;
2. prior candidate support union every non-target row in the new columns: 116,353 allowed variables.

Both systems were consistent and independently produced the identical 1,688-row candidate (SHA-256 `9c7210e82f9b38647d2ba84d9e1afbb4e7156bbe2724d049c6fb9d2cab3d7bd2`) and identical 10,466-column global frontier (SHA-256 `73505cf3265911fa7431c216f85cb63a300f46de26c7271195034192075476ea`). A one-hop enlargement was unnecessary because both requested systems were already consistent.

## Measurements and exact checks

| system | allowed | solve seconds | support | all-equation violations | global frontier |
|---|---:|---:|---:|---:|---:|
| prior + new-only rows | 66,816 | 0.759194833 | 1,688 | 0 | 10,466 |
| prior + full new-column row union | 116,353 | 0.831494875 | 1,688 | 0 | 10,466 |
| sealed cold/rare reference | n/a | 10.838951 | 499 | 0 | 1,268 |

The complete bounded process took 8.160865292 seconds and peaked at 1,913,056 KiB, below the 120-second/8-GiB gate. The independent audit streamed all 315,301 equations and all 31,973,746 cached vector entries, checked target=1, checked restriction membership, replayed both repair candidates and the reference, and recomputed exact sorted candidate/frontier hashes. The strict validator reports `PASS`; nine hostile mutations are rejected fail-closed (false promotion, wrong frontier, hidden violation, missing equation, continuation, candidate mismatch, RSS overrun, false verdict, plus the positive control).

## Verdict

`REJECT_FRONTIER_REGRESSION`. The restricted repair is an interesting fast exact solver control, but it is not a production optimization for the continuation: its downstream incident workload is 8.25x worse. No promotable optimization or active computation remains from this gate.
