# N=8 D1: maximal residue orbit O4

Orbit O4 is not residue-empty.  Its three blocks incident to vertex `7` are

```text
C47=c tensor e2,   E57=e tensor e2,   F67=lambda*e2 tensor e2,
```

while the three opposite blocks are full.  Use the independent edge gauge to
set `lambda=1`.  Residue purity becomes, on sites `4,5,6`,

```text
A45 tensor e2 + B46 tensor e + c tensor D56 = e2 tensor e2 tensor e2.
```

The colour-`0,1` slices at site `6` give the complete family

```text
B[:,k]=alpha_k*c,       D[:,k]=-alpha_k*e       (k=0,1),
A=E22-B[:,2] tensor e-c tensor D[:,2].
```

All named parameters and all entries of `A` are generically nonzero.  The
checker verifies all `81` coefficients symbolically and freezes an explicit
rational point with

```text
c=e=(1,1,1),  alpha0=alpha1=1,
B[:,2]=(1,2,3),  D[:,2]=(4,5,6).
```

At this point `A_ij=delta_(i,j),(2,2)-B_i-D_j`, so every entry is nonzero and
`A22=-8`.

## Exact boundary implication

The maximal arbitrary-boundary chart has `197` localized cells and `7,237`
coefficient generators.  Four committed six-site records factor universally:

```text
4144 = x02_20 * R2222       4738 = x02_21 * R2222
6815 = x13_20 * R2222       6842 = x13_21 * R2222,
```

where

```text
R2222=x45_22*x67_22+x46_22*x57_22+x47_22*x56_22.
```

Residue purity is `R2222-1=0`, while each displayed mixed six-site equation
is zero.  Hence the ordinary polynomial identity

```text
g-m*(R2222-1)=m
```

puts the corresponding localized boundary cell in the ideal, over every
field.  Therefore every O4 support containing any of

```text
x02_20, x02_21, x13_20, x13_21
```

is empty.  The only O4 boundary subcube still requiring analysis has all four
cells absent.  This is an implication clause, not a claim that the entire O4
downset is closed.

The exact checker
[`verify_n8_d1_residue_orbit4_family_and_lift.py`](../computations/verify_n8_d1_residue_orbit4_family_and_lift.py)
verifies the symbolic family, the rational point, all `8,100` maximal support
fibres, the full generator hash
`10bcf6a8aae8028d7dcad5e7cca6cfd3df44070abd28d7964fd30d95d6dd2fd3`,
the four source records, and each unit identity.
