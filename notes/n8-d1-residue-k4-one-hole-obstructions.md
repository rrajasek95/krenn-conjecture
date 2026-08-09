# N=8 D1: residue-K4 one-hole obstructions

Let `A,B,C,D,E,F` denote the six edge blocks of the residue `K4` and require
their matching tensor to be `e2^4`.  Two complementary one-hole lemmas close
the dense 216-cell boundary.

## A target-row or target-column hole

Take `F_20=0`; the other cases follow by the allowed symmetries.  The zero
slice gives

```text
B_2=s C_0,        D_2=-s E_0.
```

Set `X=[C_0 C_1 C_2]`, `Y=[E_0 E_1 E_2]`, and
`W_ij=C_i E_j^T-C_j E_i^T`.  The remaining zero-target slices first make
`A` proportional to `W_01`, then give a nontrivial relation

```text
lambda W_02-alpha W_12-delta W_01=0.                 (1)
```

Thus (1) is `X S Y^T=0` for a nonzero alternating `3 x 3` matrix `S` of
rank two.  The pure slice is

```text
E22=X T Y^T
```

for another alternating matrix `T`.

The coordinatewise nonzero columns rule out rank one for `X` or `Y`, since
their images must contain the coordinate vector `e2`.  Sylvester's rank
inequality applied to `X S Y^T=0` therefore forces both ranks to equal two.
If `h=ker X`, alternation shows that `row(Y)=h^perp`, hence `ker Y=ker X`.
Choose coefficient coordinates with common kernel `e2`.  Then every
alternating product has the form

```text
[X0 0] [[0,c,0],[-c,0,0],[0,0,0]] [Y0 0]^T,
```

which has rank zero or two.  It cannot be the rank-one matrix unit `E22`.
This is the structural alternating-rank obstruction.

## A non-target off-diagonal hole

For `F_01=0`, rank-one cancellation gives

```text
B_0=r C_1,        D_0=-r E_1.
```

The `(0,0)` and `(0,2)` slices make `W_01` and `W_12` proportional to `A`.
Writing the next two slices as

```text
B_1=lambda C_0-alpha C_1,
D_1=alpha E_1-lambda E_0
```

makes the `(1,2)` slice equal `lambda W_02-alpha W_12`; its nonzero
coefficient forces `W_02` to be proportional to `A` as well.  Repeating the
same two-slice completion for row `2` makes the pure cross term a combination
of `W_02,W_12`.  Hence `E22` is proportional to `A`, contradicting any
non-target nonzero entry of `A`.

Both proofs use no division by an integer and hold over every field.  The
checker
[`verify_n8_d1_residue_k4_one_hole_obstructions.py`](../computations/verify_n8_d1_residue_k4_one_hole_obstructions.py)
reconstructs the two 216-cell instances, verifies all 8,100 fibre shadows,
and audits the slice and wedge identities exactly.  Its ledger is
`2dff9275aed7b2153ebda11dd90ea54aa79d4b79db9ee26ce3476688c76b3ad1`.
