# N=8 D1: residue-K4 two-hole completion family

Two further support patterns are instances of the same slice-completion
principle.  Write the residue matching tensor as

```text
P_kl=F_kl A+B_k E_l^T+C_l D_k^T,
```

with `P_22=E22` and every other `P_kl=0`.

## Opposite non-target holes

If `F_01=F_10=0`, rank-one cancellation gives

```text
B_0=r C_1, D_0=-r E_1,   B_1=s C_0, D_1=-s E_0.
```

The remaining slices make all three wedges

```text
W_ij=C_i E_j^T-C_j E_i^T
```

scalar multiples of `A`.  The row-2 completion has

```text
B_2=mu C_0-beta C_1,     D_2=beta E_1-mu E_0,
```

so its pure cross term is `mu W_02-beta W_12`.  Hence `E22` is a scalar
multiple of `A`, contradicting one non-target entry of `A`.

## The staircase four-hole pattern

Suppose instead

```text
F_11=F_12=F_20=F_21=0,      F_10 != 0.
```

The target-row holes make `C_0,C_1` proportional to `B_2` and `E_0,E_1`
proportional to `D_2`.  The two row-1 holes then make `B_1` proportional to
`B_2`, `D_1` proportional to `D_2`, and likewise force `C_2,E_2` into the
same two lines.  With normalized vectors `u,v`, the relevant columns are

```text
B_1=r u, D_1=r v, C_0=c u, E_0=-c v.
```

Therefore the `(1,0)` cross term cancels identically.  Its slice equation is
`F_10 A=0`, impossible because both factors are nonzero.

Only nonzero vectors are required; their individual coordinates need not all
be present.  Endpoint exchange, residue-site permutations, and exchange of
the two non-target colours give the full clause family.  The proof uses no
integer division and holds over every field.

The checker
[`verify_n8_d1_residue_k4_two_hole_completion_family.py`](../computations/verify_n8_d1_residue_k4_two_hole_completion_family.py)
audits dense 215- and 213-cell representatives, all 8,100 fibre shadows, and
the exact wedge/cancellation identities.  Its frozen ledger is
`42deab2d3c700f27fe19d5715800b4a9d508da7f06ad1006dc022a3ccf2bfa7f`.
