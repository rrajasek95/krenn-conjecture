# N=8 D1: residue permutation-transversal obstruction

Write the residue matching slices as

```text
P_kl=F_kl A+B_k E_l^T+C_l D_k^T,
P_22=E22,                  P_kl=0 otherwise.
```

Let `pi` be a permutation of the three colors with `pi(2)!=2`.  Suppose one
residue edge has the three holes

```text
F_k,pi(k)=0,              k=0,1,2.                  (1)
```

Every adjacent vector is assumed nonzero, but its individual coordinates
need not all be present.

Each zero slice in (1) gives

```text
B_k=s_k C_pi(k),          D_k=-s_k E_pi(k).
```

For every other column `l`, its cross term is

```text
s_k (C_pi(k) E_l^T-C_l E_pi(k)^T)
```

and the slice equation makes this wedge a scalar multiple of `A`.  Because
`pi` is a permutation, the remaining slices expose all three wedges
`W_01,W_02,W_12`.  In particular, `pi(2)!=2` makes the pure cross term
`s_2 W_pi(2),2`, so

```text
E22=F_22 A+s_2 W_pi(2),2
```

is proportional to `A`.  Any non-target nonzero coordinate of `A`
contradicts this identity.  The argument is division-free and holds over
every field; cells outside the residue `K4` are irrelevant.

The exact checker
[`verify_n8_d1_residue_k4_permutation_transversal.py`](../computations/verify_n8_d1_residue_k4_permutation_transversal.py)
audits the representative `pi=(2,0,1)`, its 214-cell complete shadow, all
nine cross slices, and the complete three-wedge census.  Its frozen ledger
is `e5ab2f91ddf7f18a2d957d5133d66f3c82f52eb1b357413f44f5736162843c3b`.
