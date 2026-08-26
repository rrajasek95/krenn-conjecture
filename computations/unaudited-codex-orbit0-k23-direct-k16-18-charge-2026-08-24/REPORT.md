# Exact grouped direct-K16 K23 charge fragment

Status: **PASS**, covering exactly the 18 scheduled IDs in the three grouped direct-K16 sinks `source_D16_R3_4`, `source_D16_R4_3`, and `source_D16_R2_2_3`. Because the retained direct-K16 checkpoint has canonical rows and collected coefficients but no packet labels, each recurrence sink is one source-faithful grouped scalar over the six packets `224,233,242,323,332,422`; no individual packet scalar is fabricated.

## Exact result

The common exact scale is `U = 400591699200`.

| Group | IDs | Terminal occurrences | Scaled charge | Exact charge |
|---|---:|---:|---:|---:|
| `source_D16_R3_4` | 6 | 122,506,961,280 | -513,238,474,044,726,312,960 | `-493262373888/385` |
| `source_D16_R4_3` | 6 | 37,977,734,400 | -198,502,467,495,831,797,760 | `-17343310848/35` |
| `source_D16_R2_2_3` | 6 | 87,859,444,608 | -576,585,529,193,622,896,640 | `-1662431566976/1155` |
| **Grouped 18-ID subtotal** | **18** | **248,344,140,288** | **-1,288,326,470,734,181,007,360** | **`-3714547946624/1155`** |

Full and irreducible charges and occurrence counts agree in every group. This is a strict K23 fragment only; it contains no K24 output, row output, membership, or conjecture claim.

## Frozen inputs and recurrence

- Direct-K16 checkpoint: `checkpoint_direct_k16.bin`, SHA-256 `93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3`; header `K16DIR1\0`, 24,097,095 fixed 32-byte records.
- Global source pins reproduced in all full sinks: signed coefficient `1464625152`, L1 coefficient `13978655136`, pivotable K16 rows `24003767`, and `p1` uses `129939187`.
- Sealed K23 group schedule: `k23_expected_scalar_groups.json`, SHA-256 `6d59f1a24771e3a5e595ab79d8d0309881edea085da62c34b8e70cf93757c9ab`.

Each source occurrence is folded literally. R3-4 and R4-3 use `+v*U/(m1*m2)` after two normalized response sign flips. R2-2-3 uses `-v*U/(m1*m2*m3)` after three flips. Every divisor is checked occurrencewise. The final K4 or K3 response is evaluated tail-by-tail, and every final child is asserted to have no available frozen pivot. Thus full equals irreducible by literal terminality, not by a scalar shortcut.

Exact intermediate pins are:

- R3-4: pivotable intermediate children `1295008880`, `p2=2041782688`, and `60*p2=122506961280` terminal K4 occurrences.
- R4-3: pivotable intermediate children and `p2` both `1186804200`, and `32*p2=37977734400` terminal K3 occurrences.
- R2-2-3: K18 children `1559270244`, pivotable K18 `807499618`, `p2=2049974172`, K20 children `24599690064`, pivotable K20 and `p3` both `2745607644`, and `32*p3=87859444608` terminal K3 occurrences.

## Gates and bounded production

The distributed 800,000-record gates measured:

- R3-4: `19.020327s`, conservative one-pass projection `572.918272s`, cache peak 155,723 keys, sampled RSS about 350 MB. It was therefore split into exact adjacent intervals `[0,12048547)` and `[12048547,24097095)`, completing in `214.595321s` and `124.888664s`.
- R4-3: `6.807600s`, projection `205.054232s`, cache peak 138,293 keys; full completion `128.961716s`.
- R2-2-3: `11.166383s`, projection `336.346731s`, cache peak 16,677 keys and sampled RSS 75,856 KiB; full completion `206.965017s`.

Each production command used eight workers, an external 540-second alarm, bounded per-piece terminal caches, and `.tmp` then rename output. No bulk row file was produced.

R3-4 shard0 received an interrupt request after another job restarted. The signal awaited escalation and reached no process; the original authorized session had already exited normally with code 0. Its complete stdout, exact command, binary/source hashes, independent interval byte scan, and all 129 literal witnesses were reconciled in `results_k23_direct_k16_34_shard0_reconciliation.json`. Shard0 was accepted without rerun. The no-gap merge reproduces all global source and intermediate pins.

## Witnesses and independent referee

There are 257 nonzero literal continuations per group, 771 total. R3-4 and R2-2-3 use the deterministic minimum source index in each of 257 global source strata. R4-3 has realized nonzero support only in global bins 0 through 36, so a read-only census enumerated exact continuations at one deterministic source record per realized bin and froze a 257-entry round-robin ledger. Its SHA-256 is `1c220eb97f7cc36138d4ff69feec26fb9a50d710802613fd423b3c060f861eed`; every realized bin supplied at least four candidates.

The independent Rust referee re-read checkpoint bytes and replayed every recorded source row, literal intermediate replacement, pivot availability/multiplicity, final tail charge, irreducibility, sign, `U` division, and nonzero contribution. Result: `PASS_INDEPENDENT_K23_DIRECT_K16_18_LITERAL_REPLAY`, 257+257+257 witnesses.

`verify_k23_direct_k16_18_package.py` pins every terminal JSON/sample/referee hash, exact coverage, source counts, group scalars, evidence paths, and subtotal. It passes under standard Python, `-O`, `-I -S`, and `-O -I -S`. Hostile missing, duplicate, extra-ID, and altered-scaled-charge manifests are all rejected explicitly without reliance on `assert`.
