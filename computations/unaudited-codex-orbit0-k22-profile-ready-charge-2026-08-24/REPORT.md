# Exact K22 charge for the 16 profile-ready lineages

## Result

**PASS for exactly 16/76 frozen K22 lineage IDs.**  Full and K0-irreducible
77-charge coincide:

| quantity | exact value |
|---|---:|
| scaled by `U=400591699200` | `1404385704805649448960` |
| reduced charge | `226175290018432/64515` |
| retained profile records | `51,636,968` |
| exact K4 tail evaluations | `3,098,218,080` |
| full wall | `20.621095` seconds |

This is a strict 16-ID subtotal, not a complete K22 result.  The K22 assembler
accepts the partial evidence and reports exactly 60 missing IDs with status
`REJECT_INCOMPLETE_K22_76_ID_GATE`.

## Exact grouped coverage and charge

| frozen group | IDs | profile records | K4 tails | scaled charge | reduced charge |
|---|---:|---:|---:|---:|---:|
| direct D18 R4 | 6 | 979,091 | 58,745,460 | `142345959558237388800` | `355339264` |
| D14 R4-4 | 1 | 18,217,226 | 1,093,033,560 | `31117156531545047040` | `35079767013376/451605` |
| grouped D15 R3-4 | 3 | 25,564,391 | 1,533,863,460 | `410673513772236718080` | `154323560670784/150535` |
| grouped D16 R2-4 | 6 | 6,876,260 | 412,575,600 | `820249074943630295040` | `71665782592/35` |

The exact IDs are:

```text
D14:222|R:4-4
D15:{223,232,322}|R:3-4
D16:{224,233,242,323,332,422}|R:2-4
D18:{244,334,343,424,433,442}|R:4
```

The direct D18, D15, and D16 profile producers aggregated their named packet
groups before this run.  Their group scalars are exact and are added once; no
individual member scalar is claimed.  `D14:222|R:4-4` is a singleton scalar.

## Source-faithful terminal evaluation

The evaluator streams exactly four frozen interfaces:

| interface | SHA-256 |
|---|---|
| `direct_k18_enriched_profiles.bin` | `d77f2a84f220aad9f52fe81547ab730a6b834005b27e6f47172bb80cf5850da2` |
| `k14_k4_enriched_profiles.bin` | `5cc8c15b2333937ddfaefac1ec056b2f2fd899f5b89ea5b0276d374b05d92d7f` |
| `checkpoint_k15_k3_profiles_merged.bin` | `8b05f3fb8edcda062111d20089309abb85d4ccd8675d289947178b437139c1db` |
| `checkpoint_k16_k2_profiles_merged.bin` | `d23271184b8258634cbf6f0942c4b1068e04c505e206b08fd3638e1c9b03be03` |

All four already contain the exact normalized response coefficient at scale
`U`, including source signs and all prior pivot denominators.  Changing the
terminal tail from K2/K3 to K4 introduces no new sign or division.  Header
scale, record geometry, record/use/weight sums, complete input hashes, and
ordered nonzero records are guarded.

For every one of the 51,636,968 records, the producer reconstructs its literal
witness row and checks the stored signature, profile, selected pivot, source
metadata, and earlier exact-U denominator.  It performed 5,202 distributed
literal-row versus profile-cycle comparisons during the full pass.  It writes
no parent or K22 child rows and has no growing cache: eight 2-MiB sequential
buffers plus fixed source/tail/cycle tables keep the run structurally far
below the 16-GiB gate.

## Universal terminality

Every K18 parent signature has anchor sum 6.  A K0 pivot consumes four anchor
incidences and a K4 tail restores zero, so every resulting K22 child has anchor
sum `6-4=2`.  Every possible K0 pivot signature has sum 4; therefore no K22
child can contain a further pivot.  This proves full equals irreducible for all
four complete interfaces, independently of sampling.

The producer checks the parent sum and pivot sum exhaustively on all profile
records.  A separate Rust referee seeks 257 evenly distributed records in
each input, independently reconstructs all 1,028 literal witnesses, replays
all 60 K4 tails for each, and checks literal 77-charge plus child signature and
nonpivotability.  All 61,680 literal child checks pass.

## Bounded gates and independent audit

The 4,096-record prefix passed, followed by 65,536 records per interface:
262,144 profiles and 15,728,640 K4 tail evaluations in 0.115238 seconds.  This
projected about 23 seconds.  The gated full pass completed in 20.621095
seconds, under the 600-second ceiling.

The independent Python finalizer verifies:

- equality with the 16 profile-ready IDs in both the sealed K22 availability
  ledger and frozen recurrence DAG;
- all four complete source hashes, headers, signs, U, counts, uses, weights,
  and group/scalar arithmetic;
- the independent distributed literal referee;
- full/irreducible equality and exact rational reduction; and
- strict grouped assembly, including the exact 16/76 partial and 60-ID gap.

Final result SHA-256 is
`e784ebc4c004247b47b91375f6dc06cefaf6f85bae50588b3af204d02a6912e5`;
logical SHA-256 is
`79fc6eee893a59ddf0d3f8f25f7df49f5d315cf0ec1cc6eb3a2a466c941d3ff0`.

Replay the audits with:

```sh
computations/unaudited-codex-orbit0-k22-profile-ready-charge-2026-08-24/referee_k22_profile_samples
python3 computations/unaudited-codex-orbit0-k22-profile-ready-charge-2026-08-24/finalize_k22_profile_ready_charge.py
python3 computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/assemble_k22_76_exact.py --self-test
```

Scope: exact charge for the 16 named K22 lineages only.  No other K22 source
replay, K23/K24 run, row collection, residual, membership, or conjecture claim
is made.
