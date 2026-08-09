# N=8 D1: exceptional blocked-row residue closure

The last sharp blocked-colour quotient support is empty already on its
residue `K4`.  Write the six edge matrices as

```text
A=A45, B=A46, C=A47, D=A56, E=A57, F=A67
```

and require their three-matching tensor to equal `e2^4`.  At vertex `4`,
row `1` of `A,B,C` is zero, while

```text
row0(A)=u,  row0(B)=v,  row0(C)=gamma*e2.
```

The vectors `u,v` have full support.  The target rows of `A,B,C` also have
full support.  The opposite blocks `E,F` are full, and

```text
supp(D)={02,12,20,21,22}.                         (1)
```

Cells outside these six blocks play no role.

## A reusable three-line Koszul lemma

For nonzero lines `u in U`, `v in V`, and `e in W`, every relation

```text
u tensor F + E tensor v + D tensor e = 0
```

has the form

```text
F=-v tensor t+p tensor e,
E= u tensor t+x tensor e,
D=-u tensor p-x tensor v.                         (2)
```

These are the three pairwise-intersection syzygies.  Their nine parameters
have one triple-intersection gauge, so their image has dimension eight.
After sending the three lines to coordinate lines, the full relation map
has rank `19` on its `27`-dimensional domain and hence the same
eight-dimensional kernel.  The checker exhibits determinant-unit minors of
sizes `19` and `8` for the relation and parameter maps, while the displayed
triple gauge supplies the complementary upper bound.  Thus this rank audit,
and hence (2), remains valid in every characteristic: it is not just an
ansatz.  This gives a reusable normal form for any blocked-colour row;
additional support flags constrain `p,x`.

## The blocked-row normal form

Use the edge gauge to normalize `gamma=1`.  The row-0 tensor equation is

```text
u_j F_kl + v_k E_jl + delta(l,2) D_jk = 0.        (3)
```

For `l=0,1`, rank-one cancellation gives nonzero `t_l` with

```text
E_l=t_l u,                 F_l=-t_l v.             (4)
```

For `l=2`, the upper-left `2*2` zero block in (1) applies the same lemma to
the restrictions of `u F_2^T+E_2 v^T`.  Hence, for scalars
`lambda,q,r`,

```text
E_2=lambda*u-q*e2,         F_2=-lambda*v-r*e2,
D=r*u*e2^T+q*e2*v^T.                              (5)
```
The four off-target entries of `D` ensure `q,r` are nonzero.  This is the
proposed quotient filtration made exact: the universal Koszul form (2)
fixes the common rank-one part, and the five-cell flag forces its two lift
vectors `p,x` onto the target lines, giving (5).

## The pure row collapses to the opposite edge

Let `a,b,c` be row `2` of `A,B,C`.  For `l=0,1`, its zero slices are

```text
t_l (u b^T-a v^T)+c_l D=0.                        (6)
```

Because `D,t_0,t_1,c_0,c_1` are nonzero, (6) synchronizes
`c_l=h t_l` and gives

```text
u b^T-a v^T=-hD.
```

Equality of the two nonzero rank-one sides then yields a scalar `s` such
that

```text
a=s*u+h*q*e2,              b=s*v-h*r*e2.           (7)
```

Substitute (5)--(7) in the remaining `l=2` slice.  The `u v^T` terms
cancel, as do the two `e2 e2^T` terms, leaving the exact identity

```text
E22=(c_2-lambda*h-s) D.                            (8)
```

This is impossible.  A nonzero scalar multiple of `D` retains its
off-target entries, while the zero multiple misses `E22`.  Thus the sharp
blocked-row support has no coefficient model over any field.

The checker
[`verify_n8_d1_residue_blocked_row_exception.py`](../computations/verify_n8_d1_residue_blocked_row_exception.py)
reconstructs the maximal 202-cell representative, checks all 8,100 fibre
shadows, verifies its exact six-edge support, and replays every identity as
a sparse polynomial identity.  Its frozen ledger SHA-256 is
`12228ed0ac3a408d83927bda4c49ea9634491ccca808eff120f064e1eb5ff6c2`.
