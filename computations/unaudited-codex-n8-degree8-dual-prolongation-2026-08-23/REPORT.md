# Exact first degree-eight boundary of the normalized N8 critical class

## Verdict

The frozen 49-row degree-seven separator does **not** prolong to degree eight
by multiplication by `t` alone.  Among the 190 genuinely new incident
columns, 146 pair nontrivially with the shifted functional.  These 146
constraints are exactly independent: each column has a degree-eight output
row which occurs in none of the other 189 new columns, so the selected entries
form a literal nonzero diagonal `146 x 146` minor.

Adding the corresponding 146 source-labelled private rows repairs the whole
first boundary, including all 190 columns, without a rank solve.  It does not
close the saturation step.  The repair is incident to 261 further columns and
the extended functional pairs nontrivially with 252 columns.  Thus `t` moves
the critical class into a larger exchange boundary; this computation neither
proves nor disproves degree-eight membership.

## Exact census

The checker reconstructs the archived degree-seven dual with digest
`b0f137c8827d8da94525a53636bd30791e7c56722b09a74e8cdfd0c792e75fb3`.
Its natural degree-eight incidence is:

| object | count |
|---|---:|
| old incident column orbits | 56 |
| all degree-at-most-eight incident column orbits | 246 |
| new multiplier-degree-four columns | 190 |
| columns crossing the shifted dual | 146 |
| distinct degree-eight output rows across all 190 | 13,254 |
| private-row repair packet | 146 |
| further columns exposed by the repair | 261 |
| columns crossing after the repair | 252 |

The 13,254 row incidences have frequency histogram
`1:12594, 2:646, 3:8, 4:6`; consequently every crossing column has many
private rows (between 30 and 90).  The first crossing pairings are
`-2:60, -1:8, 1:8, 2:70`.  The second boundary already contains pairings
`+-1`, `+-2`, and `+-4`, so it cannot be identified with the first packet by
a scalar rescaling.

The full 146-column ledger, including literal word, multiplier, selected
private row, coefficient, and repair weight, is frozen in
[`results_degree8_dual_prolongation.json`](results_degree8_dual_prolongation.json).
Its logical digest is
`cf37fd401cd2b53cfe7e0fe45132f9e409960e6bb617ce86574e49119cba9cdb`.

## Root `05a7` and the global class

The 78-word DFS packet gives root `05a7` five options.  Passing to every
mixed word adds exactly one option,

```text
canonical word 12012012, profile 332, multiplier 07.
```

Its literal contributor is word `21012012`, multiplier `05`, raw matching
term `3e6787a7`; normalization deletes support cells `3e,67,87` and leaves
`a7`.  The column has 55 outputs and meets four frozen tail roots.  Adding it
does not create a leaf: the all-mixed DFS reaches its 10,000,001-call cap with
no pivots.  Therefore the small cyclic core is a local manifestation of the
archived global degree-seven class, not evidence that multiplication by `t`
preserves that class.

## Scope and replay

This is an exact first-boundary calculation only.  It runs no degree-eight
ambient span solve and makes no claim about the saturation exponent.  Replay:

```sh
.venv/bin/python computations/unaudited-codex-n8-degree8-dual-prolongation-2026-08-23/audit_degree8_dual_prolongation.py --check-results
.venv/bin/python -O computations/unaudited-codex-n8-degree8-dual-prolongation-2026-08-23/audit_degree8_dual_prolongation.py --check-results
.venv/bin/python -I -S computations/unaudited-codex-n8-degree8-dual-prolongation-2026-08-23/audit_degree8_dual_prolongation.py --check-results
```

All three modes reproduce the logical digest above.  `--mutate` changes the
crossing census and is rejected.  Artifact SHA-256 values are:

```text
checker  0cb03707c4c2f4f3f4c408be2a7bba34de169d596b72d5a2273c916ac11c986f
result   e629248f2bce2dc273b2d8126ccab14a6735e85dde56911bdec033928ecbf568
```
