# N=8 D1: residue-K4 shared-hole obstruction

A second dense four-site pattern has a shorter obstruction than the
two-hole target-row calculation.  Let

```text
A=A45, B=A46, C=A47, D=A56, E=A57, F=A67
```

and suppose the residue matching tensor is the pure coordinate tensor
`e2^4`.  Choose non-target colours `k,l in {0,1}`.  Assume

```text
F_kl=F_2l=0,
F_k2,F_22 != 0,
```

the block `A` has full support, and the relevant columns

```text
B_k,B_2,D_k,D_2,C_l,C_2,E_l,E_2
```

are coordinatewise nonzero.

The two zero slices at `(k,l)` and `(2,l)` are

```text
B_k E_l^T+C_l D_k^T=0,
B_2 E_l^T+C_l D_2^T=0.
```

The elementary rank-one cancellation lemma makes the adjacent columns
pairwise proportional.  Thus for some nonzero scalar `r`,

```text
B_k=r B_2,      D_k=r D_2.
```

Divide the mixed `(k,2)` slice by `r` and compare it with the pure `(2,2)`
slice.  Their cross terms are identical:

```text
0   = (F_k2/r) A+B_2 E_2^T+C_2 D_2^T,
E22 = F_22 A    +B_2 E_2^T+C_2 D_2^T.
```

Consequently

```text
E22=(F_22-F_k2/r) A.
```

This is impossible because `A` has every entry nonzero while `E22` is a
single coordinate matrix unit.  The same proof applies after permuting the
four residue sites or exchanging the two endpoints, giving the shared-row
version as well.  It is valid in every characteristic.

The fixed D1 instance has 214 localized cells and omits

```text
x_67_01, x_67_10, x_67_20.
```

The shared holes are `x_67_10,x_67_20`; the additional hole is irrelevant.
The checker
[`verify_n8_d1_residue_k4_shared_hole_obstruction.py`](../computations/verify_n8_d1_residue_k4_shared_hole_obstruction.py)
reconstructs this support, verifies all 8,100 fibre shadows and every required
nonzero cell, and audits the mixed/pure comparison as an exact sparse
polynomial identity.  The frozen ledger SHA-256 is
`293eca9104bcfd24995682795b598e2f81e1434f680d9f67222282c498621cf9`.

This is a support-monotone structural lemma on its required cells: arbitrary
additional holes outside the displayed columns do not affect it.  It can
therefore be inserted directly as a clause family in the D1 extension CEGAR.
