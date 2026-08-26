# Rep2 group16 torus-gauge decomposition design

Status: **exact design / zero run / no closure**. The consumed group16 source is SHA `79a2cf5c...`, chart `[0,0,0,1,"z",2,0,1]`, 91 variables and 6,577 generators. Its sealed lane stopped at the 240-second native wall with 2,043,080,704-byte peak RSS; groups 1–15 reached size-one unit bases in 5.85–23.27 seconds.

## Exact reduction

The supported-matching equations admit four verified edge-scaling characters. Every one of the 6,577 literal source polynomials is homogeneous under all four, with the expected guard weights. The saturated product makes `beta`, `abar`, and `A57[0,0]` units. Their 3×3 character matrix has determinant one, so the rational, root-free parameters

`lambda35=beta^-1`, `lambda57=A57[0,0]^-1`, and `lambda56=(abar*beta*A57[0,0])^-1`

set all three to one. This reduces the chart from 91 to 88 variables exactly.

The residual character scales `A67` and `A12` inversely. An exhaustive cover consists of nine opens `D(A67[i,j])` (87 variables each), then on `A67=0` nine opens `D(A12[i,j])` (78 variables each), and finally `A67=A12=0` (70 variables): 19 sources total. Each retains all 6,577 distinct, nontrivial generators. Forward gauge parameters and reverse torus action are explicit; no radicals or omitted complement occur.

## Obstruction and scope

The source-labelled support has only the identity vertex automorphism, and group16's simultaneous-S3 orbit is disjoint from groups 0–15. Thus no sound transport to an already closed group was found. The original `dp` order is retained; no block-order or performance claim is made. The prior attempt is consumed and cannot be reused or relaunched. These sources require independent design audit and separately authorized fresh pilots before any mathematical coverage.
