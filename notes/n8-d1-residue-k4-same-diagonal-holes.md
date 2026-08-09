# N=8 D1: the same-diagonal two-hole residue orbit

The dense residue frontier with five full blocks and

```text
F00=F11=0
```

in the sixth block is empty over every field.  The proof uses only residue
purity and nonvanishing of the other `52` residue cells, so every cell
outside the residue K4 is free.

All displayed tensor identities are polynomial identities over `Z`.  The
proportionality and rank case split is performed over a field.  Consequently
the proof also applies after localizing any integral coefficient domain at
the named `52` cells and passing to its fraction field; no algebraic closure
or characteristic assumption is used.

Write the residue coefficient, sliced at sites `6,7`, as

```text
H_kl = F_kl*A + b_k tensor e_l + c_l tensor d_k,
```

where `A=A45`, while `b,c,d,e` are columns of the four adjacent blocks.
The two diagonal zero slices give rank-one cancellations

```text
b0=alpha*c0,  d0=-alpha*e0,
b1=beta*c1,   d1=-beta*e1.                            (1)
```

In particular, with

```text
Wkl = c_k tensor e_l-c_l tensor e_k,
```

the `(0,1),(0,2),(1,2)` slices make `W01,W02,W12` nonzero scalar multiples
of the full-support block `A`.  The factor multiplying `W01` is nonzero
because `F01`, `alpha`, and every entry of `A` are localized.

## Rank-two branch

If `W01` has rank two, both pairs `(c0,c1)` and `(e0,e1)` are independent.
The two proportional wedges then have the common-coefficient form

```text
c2=p*c0+q*c1,        e2=p*e0+q*e1.                   (2)
```

The transposed pair of slices similarly gives

```text
b2=-g*c0+f*c1,       d2=g*e0-f*e1.                  (3)
```

Direct expansion of (2)--(3) yields

```text
b2 tensor e2+c2 tensor d2 = -(f*p+g*q)*W01.          (4)
```

Thus the target slice `H22` is a scalar multiple of `A`.  This cannot equal
the coordinate matrix unit `E22`, because every entry of `A` is nonzero.

## Rank-one branch

If the nonzero `W01` has rank one, either `c0,c1` are proportional or
`e0,e1` are proportional.  In the first case, subtracting the corresponding
multiple of `W02` from `W12` forces `c2` onto the same line; the `(2,0)`
slice then forces `b2` onto it as well.  Every term in `H22` consequently
has the same full-support left factor.  Equality to `E22` would make that
factor the target coordinate line, a contradiction.  The right-dependent
case is symmetric.

This closes the sole residue orbit seen in the `50`-model census after
promoting the injective-tripod and all-boundary-pairing pure-lift clauses.
It supplies the missing dense atom between the earlier target-row and
opposite-off-diagonal two-hole obstructions.

The exact checker
[`verify_n8_d1_residue_k4_same_diagonal_holes.py`](../computations/verify_n8_d1_residue_k4_same_diagonal_holes.py)
reconstructs the maximal `215`-cell representative, checks all `8,100`
support fibres, and verifies the rank-two and both rank-one symbolic
factorizations coefficient by coefficient.
