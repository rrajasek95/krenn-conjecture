# Legacy chart 27 anchor ladder (zero-based chart 30)

Status: **UNAUDITED exact filtered progress; no localized-chart closure claim.**

This directory advances the twelve-anchor filtration for zero-based chart 30,
which independently maps to legacy one-based chart 27.  The named anchors are

```
x01_00 x02_11 x03_22 x14_11 x17_22 x23_00
x25_22 x36_11 x45_00 x46_22 x57_11 x67_00
```

Their complete stabilizer in `S8 x S3` has order six.  `K_anchor` is generated
by the other 240 endpoint cells.

## Exact K^6 terminal

The prior literal K^5 component had 21,596 rows and 82,383 columns.  At exact
K-degree five, the complete six-stabilizer quotient closure has 44,763 row
orbits and 140,847 column orbits.  The terminal closure layer adds no rows but
3,335 columns, so stopping when the row set first stabilizes would be wrong.
Every leading column has one or three literal outputs, without row-orbit
collisions: 118,657 singleton columns and 22,190 triples.

Literal singleton quotienting leaves 977 coupled row orbits.  The projected
triples give 544 distinct unary-pivot rows and 234 distinct unsigned edges.
There are 226 unrooted bipartite components, hence 226 exact quotient duals.
The previously chosen 1,664-term K^5 certificate violates 80 of them; this is
only an obstruction to that chosen lower lift, not K^6 nonmembership.

Including all lower orbit columns gives the complete augmented system

```
3,905 rows = 3,679 lower row orbits + 226 quotient duals
13,818 lower column orbits
```

Exact unit peeling removes 3,533 rows.  The 372-row core has rank 331 and
left-nullity 41 modulo both 1009 and 1013.  A selected 331-by-331 minor has
exact determinant 32.  Reverse exact peeling produces a 549-term lower orbit
solution and replays all 3,905 augmented equations over `Q`.

Completing the degree-five graph quotient uses 180 triple and 3,564 literal
singleton orbit terms.  The resulting 4,293-term six-transform-average
certificate has denominator LCM one and passes a full labelled rational replay:

```
H0 H1 H2 in I_mix + K_anchor^6  over Q.
```

This controls only anchor degrees below six.  Degrees six through twelve are
still required before `K_anchor^13 = 0` yields a full localized-chart identity.

The frozen exact result digest is
`1dc739a4ef4ef5c2e0e6d89d3621d15e0c547a0eaf4802bcc1f87b800e6a3097`.
The independent standard/`-O`/`-I -S` labelled replay digest is
`03f30aed3c24f99b38da050a1c5f1cec3a15089e4ad51aa1d29444781dbb9b45`.
Term deletion, missing orbit normalization, and the terminal column-only
closure layer are must-fire controls.

## K^7 frontier handoff

The exact degree-six residual of the frozen K^6 certificate has 29,669 row
orbits.  Python completed three closure layers before the validated Rust
engine took over:

```
seed:  29,669 / 0
L1:   113,232 / 86,526
L2:   217,315 / 323,186
L3:   290,914 / 583,793
```

`legacy27_degree6_seed.txt` contains the degree, twelve anchors, all six
stabilizer actions, and all exact rational residual coefficients in the generic
Rust seed format.  Its SHA256 is
`b24b9fc97c5afbb30314ebc156ccce39a3afa146766612606ab34a41ef9bb8bf`.
No K^7 rank or membership conclusion is drawn here before saturated closure
and peeling are replayed.

### Correction: chosen-section transfers are incomplete

A subsequent scope audit found that choosing one triple/singleton correction
for each lower column does **not** generate the full lower kernel.  The
minimum-degree-five leading matrix has rank 44,537 and internal kernel
dimension 96,310.  In particular, two different singleton columns can have
the same degree-five pivot row and different degree-six tails.  The frozen
exact witness has a six-term nonzero tail difference; see
`results_k7_internal_min5_kernel_trap.json` (digest `56955a53...`).

Thus the staged 9,954 chosen-section transfers in
`k7_lower_kernel_transfers_p1009.jsonl` are explicitly **restricted and
incomplete**.  They must not be used for a sound closure or obstruction.  The
full cutoff-below-six source ledger is

```
154,665 columns, rank 48,401, kernel dimension 106,264.
```

The sound replacement is the whole-cutoff engine, which closes every mixed
source column of minimum K-degree below seven at once.  Its legacy27 seed is
`legacy27_cutoff7_target_seed.txt`, SHA
`82f89c025d34994c0452d57554a35660f78ecc46b36ada912dab5211521a4208`.
The exact target orbit counts by K-degree are

```
degree:       0  1   2   3    4    5     6
actual:       1  0  36  96  612  2304  9120
six-orbits:   1  0   7  18  108   384  1552
```

There are 2,070 target row orbits of total mass 12,169.  No Python whole
cutoff closure was launched.

### Whole-cutoff-seven interface

The validated Rust closure from that seed is complete at

```
577,305 row orbits / 1,447,685 source-column orbits.
```

Exact unit peeling removes 532,564 rows and leaves a
44,741-by-77,265 residual interface.  An independent Python engine rebuilt
the first layer from literal words and replayed all 77,265 retained columns,
including their orbit multiplicities.  The audited interface SHA256 is
`e25b8d81e5b7e7e8170a57322c36decccf404770234a8f9319c34565638cce2c`;
the interface-audit result digest is `898b15fb...`.

The residual incidence hypergraph has one connected component: all 44,741
rows, all 77,265 columns, and all 427 nonzero target coordinates lie in it.
Column supports split as 36,643 graph edges, 26,423 triples, and 14,199
higher-support hyperedges.  Thus connected-component parallelization cannot
reduce this solve.  The component-census digest is `d00f0b33...`.

Rows were then losslessly reordered by K-degree, and columns by minimum
remaining K-degree, support size, mass, and original index.  Every output
column retains `source_original_index`.  The filtration-ordered legacy27
interface has SHA256
`5251c84d594475153c5ca3939be377376f822dfe158e1e9f7bb14c218b4f392c`.
The permutation result digest is `34d509c7...`; no modular or rational
membership claim follows merely from this reindexing.

The p=1009 solve of this ordered interface completed in 775.606 seconds:

```
rank 42,232 / 44,741; target residual 0; 31,882 solution terms.
```

The selected coefficients were transported through `source_original_index`
and replayed on the original exact-integer interface with zero residual modulo
1009.  The modular solution SHA is `9cd15ca9...` and the replay-audit digest is
`3a4c9429...`.  This is a modular discovery only: an independent prime and an
exact-Q reconstruction are still required before asserting a K^7 lift.

As a must-fire control, the same permutation was applied to the frozen
chart26 cutoff-seven interface.  At p=1009 its reordered rank is 13,202 and
the target is in the image, exactly matching the original solve.  The
8,661-term reordered solution was mapped back through `source_original_index`
and replayed on the original interface with zero residual.  The ordered
control SHA is `5054daa8...`, its solution SHA is `04309595...`, and the
invariance-audit digest is `d7836779...`.

## Main artifacts

- `probe_legacy27_k6_orbits.py`: exact K-degree-five orbit closure.
- `k6_augmented_matrix.json` / `.jsonl`: multiplicity-preserving augmented
  lower-plus-dual system; JSON matrix digest `78a62528...`, JSONL digest
  `bee61982...`.
- `solve_k6_augmented_exact.py`: two-prime calibration and exact-Q core solve.
- `audit_legacy27_k6_exact.py`: final six-transform labelled replay.
- `replay_legacy27_k6.py`: independent three-mode replay.
- `probe_legacy27_k7_residual.py`: degree-six residual and Python census.
- `export_legacy27_degree6_seed.py`: generic Rust closure handoff.
- `audit_k7_internal_min5_kernel_trap.py`: exact audit invalidating the
  restricted chosen-section transfer approach.
- `export_legacy27_cutoff7_seed.py`: sound whole-cutoff Rust target seed.
- `audit_cutoff7_rust_interface.py`: independent exact interface replay.
- `audit_cutoff7_component_decomposition.py`: residual incidence-component
  census.
- `reorder_cutoff7_interface_by_filtration.py`: lossless degree ordering with
  old-column provenance.
- `verify_cutoff7_filtration_solution.py`: p=1009 solution transport and
  original-interface replay (modular only).
- `audit_filtration_reorder_chart26_control.py` and
  `verify_filtration_reorder_chart26_control.py`: frozen rank/membership
  invariance control and original-interface replay.
