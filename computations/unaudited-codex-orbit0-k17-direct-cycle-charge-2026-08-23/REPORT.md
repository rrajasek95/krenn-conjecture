# Orbit-zero direct K17 cycle charge

The direct K17 input

`-R8' * [all E-layer profiles summing to 9]`

has seven profiles: the six permutations of `(2,3,4)` and `(3,3,3)`.
Their collected packet has 171,008 distinct coefficient-one terms per H
slice. Across 485 exact `R8'` H-slices this gives 82,938,880 factored
occurrences.

The exact 77-cycle charge split is:

| sector | occurrences | charge |
|---|---:|---:|
| raw direct K17 | 82,938,880 | +53,763,072 |
| K0-singleton-pivotable | 81,076,480 | +116,149,248 |
| irreducible | 1,862,400 | -62,386,176 |

Canonical signed collection of the irreducible sector leaves 1,439,337
nonzero order-384 H-orbits and replays charge `-62,386,176`. The residual TSV
has SHA-256
`d4597e8a2541af75ebccb93a492a33934b277929bf12077fd6ba17cc8dd180f2`.

Standard, optimized, and isolated replays agree; a one-unit packet mutation
fails. Logical digest:
`fb8fcf04ea18b701c1707a86b9b514a2640cf67b853ad24e1ece64dde078be80`.

## Replay

```sh
python3 audit_direct_k17_cycle_charge.py
python3 -O audit_direct_k17_cycle_charge.py --verify
python3 -I -S audit_direct_k17_cycle_charge.py --verify
python3 audit_direct_k17_cycle_charge.py --mutate --verify  # must fail
```

Strict scope: direct K17 input only. No K14/K15 reduction tails and no K18+
outputs are included.
