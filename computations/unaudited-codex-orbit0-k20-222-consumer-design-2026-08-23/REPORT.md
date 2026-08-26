# Complete K20 hidden/direct/profile immediate charge

**Terminal status: PASS, all 36/36 K20 path IDs have exact grouped charge.**  The former 30-ID partial is completed by the independently streamed K16/K2 aggregate over `D16:{224,233,242,323,332,422}|R:2-2`. The strict exact-Q assembler finds no missing, duplicate, or extra lineage IDs.

## Full `[2,2,2]` result

The charge-only pass consumed all 158,439,965 pivotable K18 parent orbits, with total scaled mass `724159651336720220160`.  It exhaustively derived and divided by `m3` for every parent, selecting 399,275,484 third pivots and accounting for 4,791,305,808 representative K2 tail terms.  Of these, 4,221,024,490 are K20-irreducible.

| charge | scaled by `U=400591699200` | reduced rational |
|---|---:|---:|
| full | `2274118864523560648704` | `269190206501368448/47418525` |
| irreducible | `2180843458743050600448` | `2839639920238347136/521603775` |

The response quotient had 5,173,958 distinct keys and 394,101,526 cache hits.  No K20 rows were collected.  Exact aggregate provenance is retained for every `(m2,m3)` class; 257 evenly spaced parents were also replayed literally and frozen in `results_k20_222_charge.json.samples.tsv`.

## Direct `D20:444` result

The literal source has 485 signed R8 records and `60^3` K4 factor choices, hence exactly 104,760,000 occurrences.  All are K20-irreducible.  The 72-cycle-partition profile ledger reconstructs both counts and the 77-charge exactly; a separate 257-row literal ledger pins source rows and charges.

The full and irreducible charges coincide:

```text
-12041901848361369600 / U = -30060288.
```

## Exact complete 36-path K20 charge

The former 30-path subtotal plus the grouped six-ID K16/K2 path gives

| charge | scaled numerator | reduced rational |
|---|---:|---:|
| full | `9591145053260687671296` | `12488470121433187072/521603775` |
| irreducible | `9340595834096436215808` | `12162234158979734656/521603775` |

The 17-ID profile subtotal alone is full `3803430392150074785792/U = 7146296281547008/752675` and irreducible `3740606478166067085312/U = 49197791432108416/5268725`. The independent validator checks the availability-ledger group mapping, group disjointness, all exact-Q/scaled equalities, and disjointness from the three literal IDs. It deliberately does not assign an aggregate group's scalar to its constituent IDs.

The K15/K3 grouped addend is full `1505666730204685762560/U = 1697405675284864/451605` and irreducible `1461387462129632378880/U = 1647487669247872/451605`. It covers exactly three disjoint DAG IDs. The producer intentionally aggregated their packet weights, so no individual-ID scalar is claimed.

The final grouped addend covers precisely these 6 IDs:

```text
D16:224|R:2-2  D16:233|R:2-2  D16:242|R:2-2
D16:323|R:2-2  D16:332|R:2-2  D16:422|R:2-2
```

Its full charge is `1702209416269710458880/U = 1635956577664/385`; its irreducible charge is `1655408397712331243520/U = 1590977133056/385`. The 281-way signed merge was replayed byte-for-byte over all 63,918,401 input records, and all 276 exported literal charge samples replay exactly. The complete totals above are charge-only: they are not a K20 row checkpoint or an ideal-membership verdict.

## Landed checkpoint validation

The validator streamed every record in both checkpoints.  It verified the 80-byte headers and records, `U`, exact file sizes, strict canonical-row order, nonzero coefficients, stored pivotability flags, and recomputed the complete signed mass sums:

| checkpoint | support | scaled signed mass |
|---|---:|---:|
| `H18PIV2` | 158,439,965 | `724159651336720220160` |
| `H18IRR2` | 110,465,931 | `1030607661835946557440` |

Both headers agree on 101,545,723 nonzero decorated-pair orbits and 1,218,548,676 generated K2 children.  Their combined mass is `1754767313172666777600`, exactly the producer's published total.

On 257 evenly spaced records from each checkpoint, the validator also replayed witness `p2/t2`, checked `orbit*stabilizer=384`, recovered the stored canonical child, and recomputed `m2`.  For all 257 pivotable samples it derived `m3`, verified divisibility, and regenerated all 8,124 selected-pivot K2 tails through the literal 77-cycle evaluator.  Every irreducible sample had an empty available-pivot set.

## Frozen input contract

The consumer reads the agreed `H18PIV2\0` format: an 80-byte header with scale `U=400591699200`, record size at bytes 28--29, and output-record count at bytes 48--55; then 80-byte records

```text
canonical K18 row[24], signed i128 orbit mass,
witness pair row[24], p2, tail2, pair uses u64,
orbit u16, stabilizer u16, pivotable flag, m2.
```

Every record is checked to be pivotable.  The consumer derives the complete available-pivot set from the literal row, sets `m3` to its size, verifies the only new exact division `w2 % m3 == 0`, and emits the 12 K2 tails for every selected `p3` with `w3=-w2/m3`.  The frozen arithmetic-plan theorem supplies the omitted upstream `m1` guard: `U` clears every realized `m1*m2*m3`; the checkpoint's signed mass already summarizes `m1` and earlier source multiplicities.

## Why occurrencewise charge is sound

Both the 77-cycle value and the predicate “the K20 child has no further pivot” are functions of the child row and invariant under the order-384 H action.  Therefore their weighted sums commute with signed duplicate/orbit aggregation.  It is sound to evaluate them from each canonical K18 row's total H-orbit mass without collecting K20 rows.

The tiny fixture emitted 9,780 representative-tail terms from 815 selected third pivots.  Direct occurrencewise evaluation exactly equalled evaluation after signed collection to 5,633 child rows:

- full scaled charge: `115890056857681920`;
- irreducible scaled charge: `103968950592798720`.

This is an arithmetic and row-property test, not the production `[2,2,2]` value.

## Bounded provenance and scope

The consumer deliberately rejects full child-provenance output: 4.79 billion representative tails would violate the charge-only scope.  Instead, the result retains exact totals by every realized `(m2,m3)` class, while the 257-row TSV freezes source row, witness pair, pivot counts, tail counts, charges, orbit/stabilizer, and pair-use metadata for literal replay.  This is enough to audit the scalar computation but is not a canonical K20 coefficient checkpoint.

The K20 computation evaluated immediate scalar charge only.  No K20 child map, membership statement, or K21+ tail is claimed.

Replay:

```sh
rustc -O --edition=2021 \
  --cfg 'feature="hidden_child_prefix"' \
  --cfg 'feature="full_hidden_charge"' \
  computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23/consume_k18_222_to_k20.rs \
  -o /tmp/consume_k18_222_to_k20
/tmp/consume_k18_222_to_k20 --self-test
```

The `[2,2,2]` production used source SHA-256 `4b625dab5449dc319d94a0f62ca0998b92ac2f64895e207b0d35a46ed84b22a9` and binary SHA-256 `057375fdff3ff5d2924285a1e9ee4ed50e2147ce55a6560eab00cfa42e2fd90a`.  The direct-D20 extension has source SHA-256 `1df3172a5169c692e07acbc3c1eadf1d83a508ed1c19ac0737460fc7b2b8bb3c` and binary SHA-256 `e0f87800bdd812ba86557d66135b623505118daee837c154fdbf187605ee46cb`.

Landed-validation result: `results_landed_checkpoint_validation.json` (SHA-256 `6b75445fbfcca74c7d5017c17de95a8ec7af2acd07db9ecf0ad764a9bd810a5f`).

Production result: `results_k20_222_charge.json` (SHA-256 `a022874ad36361caf44de2473b4a5c7534ecfb9c082df046e3f26046fcc90a57`); sample ledger SHA-256 `ed3d273f60b3b9f8e1147377d8abfa1605d40e52096078a78242a2ba0a143bed`.

Direct result: `results_direct_d20_444_charge.json` (SHA-256 `3c428896b84ee2174ff44520d6c92c15455e38050b6dfd67f9dc1c2a3f8c1133`); profile ledger SHA-256 `d5fed9646691ccc7bcc6d6ad61903e31b0fc5b4eb0534572aca34a260caf724c`; sample ledger SHA-256 `3ac4f89954b86be970a76adeb7c3cb288047d3e48f5a17fc95677560d39130bd`.

The grouped profile source is `results_k20_17_path_profile_charge.json` (SHA-256 `48fdf06e272357bea970d00e9ec00631be1cbc024b9dfc6ee2ec61ba5f13835c`, logical `7e8b3d71...`). Its independent audit is `results_k20_17_path_independent_validation.json`.

The direct-six source is `computations/unaudited-codex-orbit0-direct-k18-profile-census-2026-08-23/results_direct_k18_k2_charge.json` (SHA-256 `82a5c213cb916523386f524242c8a5aba0e32dd91291d0f5c017de268b1541ad`, package logical `27b3442d...`). Its independent mapping/arithmetic audit is `results_direct6_k20_independent_validation.json`.

The K14/K4 source is `computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/results_k14_k4_k2_charge.json` (SHA-256 `0aec524a3b104965d97ed1f18e27d07355f58180c7751e9cda4db78488b67f31`, package logical `2a113720...`). Its independent audit is `results_k14_k4_k20_independent_validation.json`; all 490 source parts and the merged checkpoint remain untouched.

The K15/K3 source is `computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/results_k15_k3_group_charge.json` (SHA-256 `6de9c573ba136304e91db2a9fc83ad1ab2804cee5103102cd77ef568fb60fdb7`). Its independent mapping/arithmetic audit is `results_k15_k3_k20_independent_validation.json`; no K16 result is inferred.

Strict assembler: `assemble_k20_36_exact.py`. It passes complete synthetic coverage, proves a grouped scalar is summed once, and rejects missing-ID and duplicate-ID mutations. The authoritative manifest is `k20_path_manifest_complete.json`; the exact result is `results_complete_k20_36path_charge.json` (SHA-256 `ea4ccd5af21312fa1bd9b73e274c9a0ceea493560315b30bfb1b588d69b70b32`). `results_complete_k20_independent_audit.json` pins the new K16 charge, literal-sample referee, full-stream merge referee, exact-Q sum, and hostile deletion of all six final IDs.
