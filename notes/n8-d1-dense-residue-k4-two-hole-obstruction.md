# N=8 D1: dense residue-K4 two-hole obstruction

The 215-cell D1 support containing every E1-admissible cell except

```text
x_67_20, x_67_21
```

is empty over every field.  The contradiction already occurs in the
four-site residue subsystem on sites `4,5,6,7`; no full eight-site
Groebner-basis calculation is needed.

Write the six residue blocks as

```text
A=A45, B=A46, C=A47, D=A56, E=A57, F=A67.
```

Every entry of `A,B,C,D,E` is localized nonzero.  In `F`, every entry is
localized nonzero except `F20=F21=0`.  The residue matching tensor is required
to equal the single pure tensor `e2^4`.

Put `u=B[:,2]` and `v=D[:,2]`.  The zero slices with residue colours
`(k,l)=(2,0),(2,1)` say

```text
u E_l^T + C_l v^T = 0.
```

Since every coordinate of `u,v,C_l,E_l` is nonzero, there are nonzero
scalars `c_l` such that

```text
C_l=c_l u,     E_l=-c_l v       (l=0,1).
```

The four slices with `k,l in {0,1}` then give

```text
B_k v^T-u D_k^T=r_k A           (k=0,1),
F_kl=r_k c_l.
```

Comparing the two rank-one decompositions yields a scalar `s` and vectors
`b,d` with

```text
B_0/r_0=b,          D_0/r_0=d,
B_1/r_1=b+s u,      D_1/r_1=d+s v,
A=b v^T-u d^T.
```

Let `w=C[:,2]`, `z=E[:,2]`, and
`alpha_k=F_k2/r_k`.  Subtracting the remaining two mixed slices and using
the pure slice `P=E22` gives

```text
(alpha_1-alpha_0-s F22) A + s P = 0.
```

The block `A` has every entry nonzero whereas `P` has only its `(2,2)` entry.
Looking first off `(2,2)` and then at `(2,2)` forces
`s=0` and `alpha_0=alpha_1=alpha`.

The surviving mixed equation is

```text
alpha A+b z^T+w d^T=0.
```

After substituting `A=b v^T-u d^T`, the elementary rank-one cancellation
lemma gives a scalar `lambda` such that

```text
w=alpha u+lambda b,       z=-alpha v-lambda d.
```

Indeed, from `b q^T+p d^T=0`, choose nonzero coordinates of `b,d`; one row
determines `q=-lambda d` and one column then determines `p=lambda b`.
Substitution in the pure slice now gives the exact collapse

```text
P = F22 A+u z^T+w v^T = (F22+lambda) A.
```

This is impossible because `P` is a coordinate matrix unit and `A` has full
support.  The proof uses no division by an integer, so it is valid in every
characteristic.

The checker
[`verify_n8_d1_dense_residue_k4_two_hole_obstruction.py`](../computations/verify_n8_d1_dense_residue_k4_two_hole_obstruction.py)
reconstructs the 215-cell support and all 8,100 fibre shadows, audits the
18 two-term and 63 three-term residue slices, and verifies every displayed
matrix identity as an exact sparse polynomial identity.  Its frozen ledger
SHA-256 is
`655afde6d006dca9f4831a48cb849b4cc19ca8c17bf63001a4fb02a53f3a6dbf`.

This result is a dense structural atom, not a closure of every D1 support.
It shows that near-full strata should be attacked through the rank geometry
of the four-site residue tensor rather than through increasingly long
eight-site Laurent circuits.
