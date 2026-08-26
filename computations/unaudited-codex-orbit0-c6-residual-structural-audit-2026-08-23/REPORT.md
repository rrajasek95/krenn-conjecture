# Structural audit of the exact 884-row c<=6 residual

## Terminal census

The frozen packet consists of 884 distinct canonical `H`-orbits.  Every
stabilizer in the order-384 factor stabilizer `H` is trivial, so every orbit
has size 384.  The stored coefficients are `+384` on 426 orbits and `-384` on
458: labelled coefficients are therefore `+1/-1`, signed quotient mass is
-12,288, and absolute mass is 339,456.

The frozen K/cycle profile replays exactly:

| profile | orbits |
|---|---:|
| K13,c6 | 6 |
| K14,c6 | 14 |
| K15,c5 | 100 |
| K15,c6 | 64 |
| K16,c4 | 144 |
| K16,c5 | 324 |
| K16,c6 | 232 |

There are 14 cycle-length partitions, 141 dihedral coloured-necklace states,
and 39 unordered per-cycle colour-content types.  Full histograms are frozen
in the result JSON.

## Factors and stabilizers

The literal gcd of the 884 chosen canonical representatives is cell `00`
twice, namely `A_01[00]^2`.  It is a feature of this representative packet,
not an `H`-invariant factor: intersecting the factors over the full `H`-orbit
of any row gives degree zero in all 884 cases.

Profile gcd degrees/anchor degrees are:

```text
K13c6  17/11      K14c6  6/6
K15c5   3/3       K15c6  4/4
K16c4   2/2       K16c5  2/2       K16c6  2/2
```

Thus the common `A_01[00]^2` factor persists in every profile, with additional
chart-dependent factors only in lower-K packets.  None survives `H` transport.

## Cycle-Morse pivotability

Applying the proved literal four-distinct-cycle predicate:

- 266 orbits admit a certified mixed physical-PM pivot;
- 618 are unpivotable because no physical PM selects four distinct cycles;
- none fail for having fewer than four cycles.

The 618 unpivotables occupy six length partitions:

```text
2+2+2+18          144
2+2+2+2+16        336
2+2+2+2+2+14      112
2+2+2+2+4+12       12
2+2+2+2+6+10        2
2+2+2+4+14          12
```

They split into 93 coloured-necklace types, 15 colour-content types, and 25
`(K, length partition, colour-content)` signatures.  Every unpivotable row
has a monochromatic cycle, but so do all 266 pivotable rows.  Therefore the
smallest universal content feature is not a separating invariant; length and
colour content alone do not explain physical-PM failure.  The obstruction is
the site-labelled incidence of cycles.

## Scope

This is a structural census only.  It does not insert the 266 pivot columns,
expand their lower-cycle/K-shifted tails, or compute any source rank.  In
particular, pivotability does not by itself remove those rows from the full
relative cokernel, and the 618-row packet is not claimed to support a dual.

Replay:

```sh
python3 computations/unaudited-codex-orbit0-c6-residual-structural-audit-2026-08-23/audit_c6_residual_structure.py
```

Input residual byte SHA-256:
`a851b9b11c755c1c07358f0f6c123c1b7f1a42a2e7a2778e252e878b750185c5`.
Logical result SHA-256:
`e5a0f9e5e0fd6003a4bb62f8dc060576bf5d2572643029ac6c9ed140f5a692e8`.
