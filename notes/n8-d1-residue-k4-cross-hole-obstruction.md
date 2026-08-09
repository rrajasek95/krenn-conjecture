# N=8 D1: residue-K4 cross-hole obstruction

Write the six residue blocks on sites `4,5,6,7` as

```text
A=A45, B=A46, C=A47, D=A56, E=A57, F=A67.
```

Suppose their matching tensor is the pure coordinate tensor `e2^4`.  Let
`k,l,m` be colours with `l != m`, and take `2` as the target colour.  Assume

```text
F_kl=F_2m=0,       F_km,F_k2,F_22 != 0,
```

the displayed columns of the four adjacent blocks are coordinatewise
nonzero, and `A` has one nonzero entry away from `(2,2)`.

The two zero slices force nonzero scalars `r,s` with

```text
B_k=r C_l,  D_k=-r E_l,     B_2=s C_m,  D_2=-s E_m.
```

The `(k,m)` slice therefore says that

```text
W=C_l E_m^T-C_m E_l^T
```

is a nonzero scalar multiple of `A`.  The `(k,2)` slice similarly makes
`C_l E_2^T-C_2 E_l^T` a multiple of `W`.  Rank-one cancellation gives
scalars `alpha,mu` such that

```text
C_2=alpha C_m-mu C_l,       E_2=alpha E_m-mu E_l.
```

Consequently the missing third wedge completes automatically:

```text
C_m E_2^T-C_2 E_m^T=mu W.
```

The pure `(2,2)` slice is therefore `E22=lambda A`, impossible at the
non-target witness entry and then at `(2,2)`.  The argument is symmetric in
the endpoints and valid over every field.

The fixed D1 instance omits `x_67_01,x_67_20` and retains 215 localized
cells.  The exact checker
[`verify_n8_d1_residue_k4_cross_hole_obstruction.py`](../computations/verify_n8_d1_residue_k4_cross_hole_obstruction.py)
reconstructs the support, checks all 8,100 fibre shadows, and verifies the
wedge-completion identities as sparse polynomials.  Its frozen ledger is
`00041a7241a912a88f105b2f3e474ae6c5618c64c791edb438e8bc0ffec45757`.
