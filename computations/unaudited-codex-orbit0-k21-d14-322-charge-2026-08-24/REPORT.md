# Exact singleton K21 charge: `D14:222|R:3-2-2`

Status: **PASS**, complete for exactly the one named lineage.  No K22 rows,
membership inference, or other K21 path is included.

## Exact result

At the common scale

```text
U = 400591699200
```

the full and irreducible 77-cycle charges agree:

```text
scaled charge = -832152508704647184384
exact charge  = -32834300375025536 / 15806175
```

The exact occurrence ledger is:

| stage | count |
|---|---:|
| R8 source records | 485 |
| literal D14 heads | 838,080 |
| selected first pivots | 6,619,280 |
| K3-to-K17 candidates | 211,816,960 |
| pivotable K17 children | 197,414,400 |
| selected second pivots | 815,482,880 |
| K2-to-K19 candidates | 9,785,794,560 |
| pivotable K19 children | 2,969,658,880 |
| selected third pivots | 5,075,412,480 |
| terminal K21 occurrences | 60,904,949,760 |
| irreducible K21 occurrences | 60,904,949,760 |

The source mass was independently reconstructed as `-40310784` with L1 mass
`385689600`.  The denominator histograms independently satisfy: their first,
second, and third weighted sums are the three selected-pivot counts; the
product histogram has 2,969,658,880 entries; and every product divides `U`.

## Sign and terminality

The direct D14 packet has coefficient `-M`.  Each normalized response changes
the sign, so the three responses `R:3-2-2` give terminal coefficient
`+M/(m1*m2*m3)`.  The reported charge can still be negative because it is the
signed 77-cycle pairing of those terminal rows.

Active-colour signature mass changes as

```text
10 --R3 (tail mass 1)--> 7 --R2 (tail mass 2)--> 5
   --R2 (tail mass 2)--> 3.
```

Every frozen pivot has mass four.  Hence every K21 child of mass three is
irreducible; the producer also asserted empty frozen availability for every
terminal response profile.  Full and irreducible counts and charges agree.

## Exact compression and provenance

Every source head is rebuilt literally from its R8 row and its three ordered
degree-2 factor tails.  The evaluator applies the frozen K14 `valid` policy at
the first pivot, then constructs literal `row17` and `row19` values by the
chosen `p1/K3` and `p2/K2` replacements.  Signature caches contain only the
finite tail/pivot plans and cannot change a coefficient or cycle response.

Compression begins at the terminal response.  Its key consists of the literal
20-cell path profile, signature, pivot, and degree.  Closing the eight boundary
endpoints with each literal K2 tail determines exactly the same cycle partition
as constructing the 24-cell child.  A bounded literal-row cache is confined to
one source head; its key is the exact sorted 24-cell `row19`.

The exported ledger contains one nonzero-charge source head in each of 257
equal bins over all 838,080 heads.  It records the literal D14, K17, and K19
rows and the selected `p1`, K3 tail, `p2`, K2 tail, `p3`, all three
denominators, and terminal response.  The independent Python referee rebuilt
all 257 source and intermediate rows and literally evaluated all 3,084 sampled
K21 children.  Every sampled child was terminal, and every literal terminal
sum matched the compressed response.

## Resource gate

The initial uncompressed eight-record gate took 32.97 seconds and projected
1,998.64 seconds, so no full run was launched.  Cross-slice response caching
reduced a 16-record gate to a 919.92-second projection, still a rejection.  The
final 32-record gate, with exact endpoint closure and bounded literal-row
deduplication, took 21.36 seconds and projected 323.69 seconds.  That gate
authorized the full eight-worker run.

The full run took 166.119057 seconds under a hard 600-second alarm.  An external
`ps` sample during the run observed 8,705,184 KiB RSS (about 8.30 GiB), below
the 16-GB limit.  Output was written atomically and consists only of aggregate
JSON plus the 257-row TSV; no bulk K17, K19, K21, or K22 row file was emitted.

## Replay

```bash
rustc -O computations/unaudited-codex-orbit0-k21-d14-322-charge-2026-08-24/run_k21_d14_322_charge.rs \
  -o computations/unaudited-codex-orbit0-k21-d14-322-charge-2026-08-24/run_k21_d14_322_charge

computations/unaudited-codex-orbit0-k21-d14-322-charge-2026-08-24/run_k21_d14_322_charge \
  --distributed-records 32 --workers 8 \
  --output computations/unaudited-codex-orbit0-k21-d14-322-charge-2026-08-24/results_prefix32_replay.json

python3 computations/unaudited-codex-orbit0-k21-d14-322-charge-2026-08-24/audit_k21_d14_322.py
```

Independent referee logical SHA-256:
`5eee6c42e61bc4d99d7a69b0a0105922e1a1e49d5d64028a6b8bf0d3ac6a10ec`.
