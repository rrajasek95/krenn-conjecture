# Full-nine deleted-star inverse: tensor-grade counterguard

## Scope

This note tests the strongest local star-inverse proposal on the committed
47-profile active curved-OO regression sector.  It does **not** construct an
exact GHZ source and it does not refute the active curved-overlap route.  It
does refute the proposed inference

> invert the three constant deleted-star pivots and use `adj(K)` to transport
> the exclusive `r=2` mixed Hessian into the `r=1` diagonal target channel.

The obstruction occurs even when the deleted star is literally the identity
and has no non-pivot summand.

The exact audit is

```text
python3 computations/verify_oo_c8_fullnine_star_inverse.py
```

It also independently reconstructs the 47 profiles before replaying the
adjugate test.

## Exact source-faithful equation

Use the canonical profile

```text
support = 01:21, 03:11, 17:11, 56:11
face    = 12111, 10111, 02111, 00111
```

with shared vertex `p=0`, second endpoint `r=4`, and common residual sites
`W={1,2,3,5,6,7}`.  The three constant columns of the deleted `r`-star are

```text
alpha_0=(5,0), alpha_1=(2,1), alpha_2=(3,2),
E=(A_{r,alpha_j})_{j=0,1,2}=I_3.
```

There are no other occupied deleted-star columns in this representative.
Let `Q=q^[3]` be the `pr` cofactor, let `d=A_pr=E_11`, and let
`K_{i,alpha}` be the six-site top tensor obtained after choosing the constant
`r`-star pivot `alpha` and the `p` output row `i`.  Literal matching recursion
at `r`, coefficient by coefficient, gives

```text
H_ij = d_ij Q + sum_alpha E_{j,alpha} K_{i,alpha}.       (1)
```

This is the exact source-faithful analogue of `E K=I`.  Crucially, the entries
of `K` in (1) are tensors on six labelled sites, not scalars.

## Where the scalar identity changes grade

To obtain a scalar `3x3` matrix, one can extract in row `i` the coefficient of
the pure residual word `i^6`.  These are three *different* coefficient
functionals.  On the representative this gives

```text
K_pure = diag(1, x_03:11 x_17:11 x_56:11, 1).
```

The determinant is the single Laurent monomial with checker mask `14`.  On
the pure-anchor chart it is normalized to one, so this scalar evaluation is
indeed invertible (in fact it becomes `I_3`).

Now apply the clean common-word second difference, fixing the exclusive
`q` colour to zero.  Applied to the same tensor-valued `K`, it gives

```text
nabla^2 K = x_17:11 x_56:11 E_12                 (mask 12).
```

Thus the nonzero active Hessian occupies the exclusive `r=2` column.  The
adjugate of `K_pure` is diagonal.  Multiplication on either side only rescales
`E_12`; it cannot create the required diagonal `E_11` channel.

This is not caused by an omitted physical neighbour: for this representative
`E=I_3` and the non-pivot remainder is zero.  The missing datum is a
source-faithful relation between the three row-dependent pure evaluations and
the mixed-face evaluation.  Equation (1) alone contains no such transport.

## Complete 47-profile replay

For each of the 47 committed clean `(q,r)=(0,2)` profiles the checker:

1. retains the three constant deleted-star pivots;
2. separates every variable cell incident to `r` as a nonlocal remainder;
3. forms the pure-output `K` and its exact polynomial adjugate;
4. forms the clean mixed-face Hessian of the same selected-pivot tensor; and
5. tests both `adj(K_pure) nabla^2 K` and
   `nabla^2 K adj(K_pure)` in the `(1,1)` channel.

The exact census is

```text
profiles                                  47
det(K_pure) term count                    1 in every profile
left adjugate reaches channel (1,1)       0 / 47
right adjugate reaches channel (1,1)      0 / 47
```

So determinant clearing does not repair the colour gate found in
`notes/oo-c8-main-face-head-column-transport-obstruction.md`.

## Consequence for the OO lane

Do not use a bare deleted-star inverse as the missing full-nine Bianchi
identity.  A viable next lemma must add a grade-changing, source-provenant
coupling—for example a head-column/off-diagonal fibre relation whose leading
term connects the mixed face to the row-dependent pure coefficient.  The
ordinary star inverse, even with perfect pivots, only acts within the chosen
coefficient grade.
