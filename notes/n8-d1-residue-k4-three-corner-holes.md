# N=8 D1: the three-corner residue obstruction

Suppose one residue block has the non-target corner pattern

```text
F00 != 0,       F01=F10=F11=0.
```

If the four blocks adjacent to this edge are full and the opposite block has
one localized off-target entry, residue purity is impossible over every
field.  All boundary cells and all unnamed residue cells are arbitrary.

Slice the residue coefficient at the endpoints of `F`:

```text
H_kl = F_kl*A + b_k tensor e_l + c_l tensor d_k.
```

The zero `01` and `10` slices are cancellations of two nonzero decomposable
tensors, hence over the fraction field

```text
b0=r*c1, d0=-r*e1,       b1=s*c0, d1=-s*e0,
```

with `r,s` nonzero.  Put

```text
W = c0 tensor e1-c1 tensor e0.
```

The zero `11` slice is `s*W=0`, while the cross term in the `00` slice is
`-r*W`.  Equivalently, the division-free identity after this normal form is

```text
s*H00+r*H11 = s*F00*A.
```

Both left-hand generators vanish.  The right side has a localized nonzero
entry because `s`, `F00`, and the named off-target entry of `A` are nonzero,
a contradiction.  The identity is over `Z`; only the standard rank-one
proportionality step passes from a localized integral domain to its fraction
field.  No characteristic or algebraic-closure assumption occurs.

This closes the `51/54` residue orbit found immediately after promoting the
weakened same-diagonal obstruction: its canonical holes are
`F01,F10,F11`, and all five other residue blocks are full.

The exact checker
[`verify_n8_d1_residue_k4_three_corner_holes.py`](../computations/verify_n8_d1_residue_k4_three_corner_holes.py)
reconstructs the maximal `214`-cell support, verifies its complete `8,100`
fibre shadow, audits the `38`-cell localized sufficient hypothesis, and
checks the tensor identity coefficient by coefficient.
